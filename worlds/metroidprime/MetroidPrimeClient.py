import asyncio
import json
import multiprocessing
import os
import struct
import subprocess
import traceback
from typing import Any, DefaultDict, Dict, List, Optional, Tuple, cast
import zipfile
import py_randomprime  # type: ignore

from CommonClient import (
    ClientCommandProcessor,
    CommonContext,
    get_base_parser,
    logger,
    server_loop,
    gui_enabled,
)
from NetUtils import ClientStatus, HintStatus
from settings import get_settings
import Utils
apname = Utils.instance_name if Utils.instance_name else "Archipelago"
from .Config import make_version_specific_changes
from .PrimeUtils import get_apworld_version
from .Items import suit_upgrade_table
from .ClientReceiveItems import handle_receive_items
from .NotificationManager import NotificationManager
from .Container import construct_hook_patch
from .DolphinClient import (
    DolphinException,
    assert_no_running_dolphin,
    get_num_dolphin_instances,
)
from .Locations import METROID_PRIME_LOCATION_BASE, PICKUP_LOCATIONS
from .MetroidPrimeInterface import (
    HUD_MESSAGE_DURATION,
    ConnectionState,
    InventoryItemData,
    MetroidPrimeInterface,
    MetroidPrimeLevel,
    MetroidPrimeSuit,
)


class MetroidPrimeCommandProcessor(ClientCommandProcessor):
    ctx: "MetroidPrimeContext"

    def __init__(self, ctx: "MetroidPrimeContext"):
        super().__init__(ctx)

    def _cmd_test_hud(self, *args: List[Any]):
        """Send a message to the game interface."""
        self.ctx.notification_manager.queue_notification(" ".join(map(str, args)))

    def _cmd_status(self, *args: List[Any]):
        """Display the current dolphin connection status."""
        logger.info(f"Connection status: {status_messages[self.ctx.connection_state]}")

    def _cmd_deathlink(self):
        """Toggle deathlink from client. Overrides default setting."""
        self.ctx.death_link_enabled = not self.ctx.death_link_enabled
        Utils.async_start(
            self.ctx.update_death_link(self.ctx.death_link_enabled),
            name="Update Deathlink",
        )
        message = (
            f"Deathlink {'enabled' if self.ctx.death_link_enabled else 'disabled'}"
        )
        logger.info(message)
        self.ctx.notification_manager.queue_notification(message)

    def _cmd_toggle_gravity_suit(self):
        """Toggles the gravity suit functionality on/off if the player has received it. Note that this will not change the player's current suit they are wearing but disables the functionality of the gravity suit."""
        self.ctx.gravity_suit_enabled = not self.ctx.gravity_suit_enabled
        self.ctx.notification_manager.queue_notification(
            f"{'Enabling' if self.ctx.gravity_suit_enabled else 'Disabling'} Gravity Suit..."
        )

    def _cmd_set_cosmetic_suit(self, input: str):
        """Set the cosmetic suit of the player. This will not affect the player's current suit but will change the appearance of the suit in the game. Note that if you start a new seed without closing the client, the option will persist. If you close the client and get a new suit, you may need to re set this."""
        if input == "None":
            logger.info("Removing cosmetic suit")
            self.ctx.cosmetic_suit = None
            suit = self.ctx.game_interface.get_highest_owned_suit()
            self.ctx.game_interface.set_cosmetic_suit_by_id(
                suit_upgrade_table[suit.value].id
            )
            self.ctx.game_interface.set_current_suit(
                self.ctx.game_interface.get_current_cosmetic_suit()
            )
            return
        suit = MetroidPrimeSuit.get_by_key(input)
        if suit is None:
            options = ", ".join(
                [suit.name for suit in MetroidPrimeSuit if "Fusion" not in suit.name]
                + ["None"]
            )
            logger.warning(
                f"Invalid cosmetic suit: {suit}. Valid options are: {options}"
            )
            return
        logger.info(f"Setting cosmetic suit to: {suit.name} Suit")
        self.ctx.cosmetic_suit = suit


status_messages = {
    ConnectionState.IN_GAME: "Connected to Metroid Prime",
    ConnectionState.IN_MENU: "Connected to game, waiting for game to start",
    ConnectionState.DISCONNECTED: "Unable to connect to the Dolphin instance, attempting to reconnect...",
    ConnectionState.MULTIPLE_DOLPHIN_INSTANCES: "Warning: Multiple Dolphin instances detected, client may not function correctly.",
}


artifact_hint_scans: Dict[str, int] = {
    "Artifact of Truth": 852090318,
    "Artifact of Strength": 3026038624,
    "Artifact of Elder": 2130803909,
    "Artifact of Wild": 1644448893,
    "Artifact of Lifegiver": 2841157592,
    "Artifact of Warrior": 801959286,
    "Artifact of Chozo": 3834658515,
    "Artifact of Nature": 365333510,
    "Artifact of Sun": 3734658979,
    "Artifact of World": 4223573402,
    "Artifact of Spirit": 820137535,
    "Artifact of Newborn": 3061202065,
}


class MetroidPrimeContext(CommonContext):
    current_level_id = 0
    previous_level_id = 0
    is_pending_death_link_reset = False
    command_processor = MetroidPrimeCommandProcessor
    game_interface: MetroidPrimeInterface
    notification_manager: NotificationManager
    game = "Metroid Prime"
    items_handling = 0b111
    dolphin_sync_task: Optional[asyncio.Task[Any]] = None
    connection_state = ConnectionState.DISCONNECTED
    slot_data: Dict[str, Utils.Any] = {}
    death_link_enabled = False
    gravity_suit_enabled: bool = True
    previous_location_str: str = ""
    cosmetic_suit: Optional[MetroidPrimeSuit] = None
    slot_name: Optional[str] = None
    last_error_message: Optional[str] = None
    apmp1_file: Optional[str] = None

    def __init__(
        self, server_address: str, password: str, apmp1_file: Optional[str] = None
    ):
        super().__init__(server_address, password)
        self.game_interface = MetroidPrimeInterface(logger)
        self.notification_manager = NotificationManager(
            HUD_MESSAGE_DURATION, self.game_interface.send_hud_message
        )
        self.apmp1_file = apmp1_file

    def on_deathlink(self, data: Utils.Dict[str, Utils.Any]) -> None:
        super().on_deathlink(data)
        self.game_interface.set_alive(False)

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(MetroidPrimeContext, self).server_auth(password_requested)
        await self.get_username()
        self.tags = set()
        await self.send_connect()

    def on_package(self, cmd: str, args: Dict[str, Any]) -> None:
        if cmd == "Connected":
            self.slot_data = args["slot_data"]
            if "death_link" in args["slot_data"]:
                self.death_link_enabled = bool(args["slot_data"]["death_link"])
                Utils.async_start(
                    self.update_death_link(bool(args["slot_data"]["death_link"]))
                )

    def run_gui(self):
        from kvui import GameManager

        class MetroidPrimeManager(GameManager):
            logging_pairs = [("Client", "Archipelago")]
            base_title = f"{apname} Metroid Prime Client"

        self.ui = MetroidPrimeManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


def update_connection_status(ctx: MetroidPrimeContext, status: ConnectionState):
    if ctx.connection_state == status:
        return
    else:
        logger.info(status_messages[status])
        if get_num_dolphin_instances() > 1:
            logger.info(status_messages[ConnectionState.MULTIPLE_DOLPHIN_INSTANCES])
        ctx.connection_state = status


async def dolphin_sync_task(ctx: MetroidPrimeContext):
    try:
        # This will not work if the client is running from source
        version = get_apworld_version()
        logger.info(f"Using metroidprime.apworld version: {version}")
    except:
        pass

    if ctx.apmp1_file:
        Utils.async_start(patch_and_run_game(ctx.apmp1_file))

    logger.info("Starting Dolphin Connector, attempting to connect to emulator...")

    while not ctx.exit_event.is_set():
        try:
            connection_state = ctx.game_interface.get_connection_state()
            update_connection_status(ctx, connection_state)
            if connection_state == ConnectionState.IN_MENU:
                await handle_check_goal_complete(
                    ctx
                )  # It will say the player is in menu sometimes
            if connection_state == ConnectionState.IN_GAME:
                await _handle_game_ready(ctx)
            else:
                await _handle_game_not_ready(ctx)
                await asyncio.sleep(1)
        except Exception as e:
            if isinstance(e, DolphinException):
                logger.error(str(e))
            else:
                logger.error(traceback.format_exc())
            await asyncio.sleep(3)
            continue


async def handle_checked_location(
    ctx: MetroidPrimeContext, current_inventory: Dict[str, InventoryItemData]
):
    """Checks for active memory relays in each worlds"""
    checked_locations: List[int] = []
    i = 0
    for mlvl, memory_relay in PICKUP_LOCATIONS:
        if ctx.game_interface.is_memory_relay_active(f"{mlvl.value:X}", memory_relay):
            checked_locations.append(METROID_PRIME_LOCATION_BASE + i)
        i += 1
    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": checked_locations}])


async def handle_check_goal_complete(ctx: MetroidPrimeContext):
    if ctx.game_interface.current_game:
        current_level = ctx.game_interface.get_current_level()
        if current_level == MetroidPrimeLevel.End_of_Game:
            await ctx.send_msgs(
                [{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}]
            )


async def handle_tracker_level(ctx: MetroidPrimeContext):
    current_level = ctx.game_interface.get_current_level()
    if current_level is None:
        level = 0
    else:
        level = current_level.value

    await ctx.send_msgs([{
        'cmd': 'Set',
        'key': f'metroidprime_level_{ctx.team}_{ctx.slot}',
        'default': 0,
        'want_reply': False,
        'operations': [{'operation': 'replace', 'value': level}]
    }])


async def handle_artifact_hints(ctx: MetroidPrimeContext, scans: Dict[int, bool]):
    artifact_locations: Optional[Dict[str, Tuple[int, int]]] = ctx.slot_data.get("artifact_locations")
    if not artifact_locations:
        return

    scanned_hints: DefaultDict[int, List[int]] = DefaultDict(list)
    for artifact_name, asset_id in artifact_hint_scans.items():
        if scans.get(asset_id):
            location, player = artifact_locations[artifact_name]
            scanned_hints[player].append(location)
    await ctx.send_msgs([
        {"cmd": "CreateHints", "locations": locations, "player": player, "status": HintStatus.HINT_PRIORITY}
        for player, locations in scanned_hints.items()
    ])


async def handle_check_deathlink(ctx: MetroidPrimeContext):
    health = ctx.game_interface.get_current_health()
    if health <= 0 and ctx.is_pending_death_link_reset == False and ctx.slot:
        await ctx.send_death(ctx.player_names[ctx.slot] + " ran out of energy.")
        ctx.is_pending_death_link_reset = True
    elif health > 0 and ctx.is_pending_death_link_reset == True:
        ctx.is_pending_death_link_reset = False


async def _handle_game_ready(ctx: MetroidPrimeContext):
    if ctx.server:
        ctx.last_error_message = None
        if not ctx.slot:
            await asyncio.sleep(1)
            return
        ctx.game_interface.update_relay_tracker_cache()
        current_inventory = ctx.game_interface.get_current_inventory()
        await handle_receive_items(ctx, current_inventory)
        ctx.notification_manager.handle_notifications()
        await handle_checked_location(ctx, current_inventory)
        await handle_check_goal_complete(ctx)
        await handle_tracker_level(ctx)
        scans = ctx.game_interface.get_scans()
        await handle_artifact_hints(ctx, scans)

        if ctx.death_link_enabled:
            await handle_check_deathlink(ctx)
        await asyncio.sleep(0.5)
    else:
        message = "Waiting for player to connect to server"
        if ctx.last_error_message is not message:
            logger.info("Waiting for player to connect to server")
            ctx.last_error_message = message
        await asyncio.sleep(1)


async def _handle_game_not_ready(ctx: MetroidPrimeContext):
    """If the game is not connected or not in a playable state, this will attempt to retry connecting to the game."""
    ctx.game_interface.reset_relay_tracker_cache()
    if ctx.connection_state == ConnectionState.DISCONNECTED:
        ctx.game_interface.connect_to_game()
    elif ctx.connection_state == ConnectionState.IN_MENU:
        await asyncio.sleep(3)


async def run_game(romfile: str):
    metroidprime_options = get_settings()["metroidprime_options"]
    auto_start: bool = metroidprime_options.get(
        "rom_start", True
    )

    if auto_start is True and assert_no_running_dolphin():
        import webbrowser

        webbrowser.open(romfile)
    elif os.path.isfile(auto_start) and assert_no_running_dolphin():
        subprocess.Popen(
            [str(auto_start), romfile],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


_GC_GAME_VERSIONS: dict[tuple[str, int], str] = {
    ("E", 0): "0-00",
    ("E", 1): "0-01",
    ("E", 2): "0-02",
    ("E", 48): "kor",
    ("P", 0): "pal",
    ("J", 0): "jpn",
}

def get_version_from_iso(path: str) -> str:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Couldn't get version for iso {path}!")

    with open(path, "rb") as f:
        # detecting any non-ISO format
        f.seek(0x200, 0)
        if f.read(4).decode("utf-8") == "NKIT":
            raise Exception("NKit format is not supported! Please dump your ISO from your disc.")

        f.seek(0, 0)
        file_format = f.read(3).decode("utf-8")
        if file_format in ["RVZ", "WIA"]:
            raise Exception(f"{file_format} format is not supported! Please dump your ISO from your disc.")

        f.seek(0, 0)
        gcz_magic = struct.unpack('<H', f.read(2))[0]
        if gcz_magic == 0xB10B:
            raise Exception("GCZ format is not supported! Please dump your ISO from your disc.")

        f.seek(0, 0)
        if f.read(3).decode("utf-8") == "CISO":
            raise Exception("CISO format is not supported! Please dump your ISO from your disc.")

        # detecting game infos
        f.seek(0, 0)
        game_id = f.read(6).decode("utf-8")
        f.read(1)
        game_rev = f.read(1)[0]
        if game_id[:3] != "GM8":
            raise Exception("This is not Metroid Prime GC")

        result = _GC_GAME_VERSIONS.get((game_id[3], game_rev), None)

        if result is None:
            raise Exception(
                f"Unknown version of Metroid Prime GC (game_id : {game_id} | game_rev : {game_rev})"
            )

        return result


def get_options_from_apmp1(apmp1_file: str) -> Dict[str, Any]:
    with zipfile.ZipFile(apmp1_file) as zip_file:
        with zip_file.open("options.json") as file:
            options_json = file.read().decode("utf-8")
            options_json = json.loads(options_json)
    return cast(Dict[str, Any], options_json)


def get_randomprime_config_from_apmp1(apmp1_file: str) -> Dict[str, Any]:
    with zipfile.ZipFile(apmp1_file) as zip_file:
        with zip_file.open("config.json") as file:
            config_json = file.read().decode("utf-8")
            config_json = json.loads(config_json)
    return config_json


async def patch_and_run_game(apmp1_file: str):
    metroidprime_options = get_settings()["metroidprime_options"]
    apmp1_file = os.path.abspath(apmp1_file)
    input_iso_path = metroidprime_options["rom_file"]
    base_name = os.path.splitext(apmp1_file)[0]
    output_path = f"{base_name}.iso"

    if not os.path.exists(output_path):
        if not zipfile.is_zipfile(apmp1_file):
            raise Exception(f"Invalid APMP1 file: {apmp1_file}")

        config_json = get_randomprime_config_from_apmp1(apmp1_file)
        options_json = get_options_from_apmp1(apmp1_file)

        build_progressive_beam_patch = False
        if options_json:
            build_progressive_beam_patch = options_json["progressive_beam_upgrades"]

        try:
            game_version = get_version_from_iso(input_iso_path)

            config_json["gameConfig"]["updateHintStateReplacement"] = (
                construct_hook_patch(game_version, build_progressive_beam_patch)
            )

            notifier = py_randomprime.ProgressNotifier(  # type: ignore
                lambda progress, message: print("Generating ISO: ", progress, message)  # type: ignore
            )
            logger.info("--------------")
            logger.info(f"Input ISO Path: {input_iso_path}")
            logger.info(f"Output ISO Path: {output_path}")
            disc_version: str = str(py_randomprime.rust.get_iso_mp1_version(os.fspath(input_iso_path)))  # type: ignore
            config_json = make_version_specific_changes(config_json, disc_version)
            logger.info(f"Disc Version: {disc_version}")
            logger.info("Patching ISO...")
            py_randomprime.patch_iso(input_iso_path, output_path, config_json, notifier)  # type: ignore
            logger.info("Patching Complete")

        except BaseException as e:
            logger.error(f"Failed to patch ISO: {e}")
            # Delete the output file if it exists since it will be corrupted
            if os.path.exists(output_path):
                os.remove(output_path)

            raise RuntimeError(f"Failed to patch ISO: {e}")
        logger.info("--------------")

    Utils.async_start(run_game(output_path))


def launch():
    Utils.init_logging("MetroidPrime Client")

    async def main():
        multiprocessing.freeze_support()
        logger.info("main")
        parser = get_base_parser()
        parser.add_argument(
            "apmp1_file", default="", type=str, nargs="?", help="Path to an apmp1 file"
        )
        args = parser.parse_args()

        ctx = MetroidPrimeContext(args.connect, args.password, args.apmp1_file)

        if args.apmp1_file:
            slot = get_options_from_apmp1(args.apmp1_file)["player_name"]
            if slot:
                ctx.auth = slot

        logger.info("Connecting to server...")
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="Server Loop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        logger.info("Running game...")
        ctx.dolphin_sync_task = asyncio.create_task(
            dolphin_sync_task(ctx), name="Dolphin Sync"
        )

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.dolphin_sync_task:
            await asyncio.sleep(3)
            await ctx.dolphin_sync_task

    import colorama

    colorama.init()

    asyncio.run(main())
    colorama.deinit()


if __name__ == "__main__":
    launch()
