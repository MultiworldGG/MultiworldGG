import asyncio
import os
import time
import traceback
from typing import TYPE_CHECKING, Any, Optional

import Utils
from CommonClient import get_base_parser, gui_enabled, logger, server_loop
from NetUtils import ClientStatus, NetworkItem

import dolphin_memory_engine as dolphin

from . import game_data, game_state, items, locations, patches, mem_addresses, ar_codes, version, options
from .items import ItemType, MkddItemData
from .command_processor import MkddCommandProcessor, DME_DOLPHIN_PROCESS_NAME_ENV_VARIABLE
from .ut_common_client_importer import CommonContext, tracker_loaded, UT_VERSION

if TYPE_CHECKING:
    import kvui


CONNECTION_REFUSED_GAME_STATUS = "Dolphin failed to connect. Please load a ROM for Mario Kart Double Dash (USA). Trying again in 5 seconds..."
CONNECTION_LOST_STATUS = "Dolphin connection was lost. Please restart your emulator and make sure Mario Kart Double Dash is running."
CONNECTION_CONNECTED_STATUS = "Dolphin connected successfully."
CONNECTION_INITIAL_STATUS = "Dolphin connection has not been initiated."


class MkddContext(CommonContext):
    """
    The context for Mario Kart Double Dash client.

    This class manages all interactions with the Dolphin emulator and the Archipelago server for Mario Kart Double Dash.
    """

    command_processor = MkddCommandProcessor
    game: str = version.get_game_name()
    compatible_version: str = "v1.0"
    items_handling: int = 0b111

    def __init__(self, server_address: Optional[str], password: Optional[str]) -> None:
        """
        Initialize the Mkdd context.

        :param server_address: Address of the Archipelago server.
        :param password: Password for server authentication.
        """
        super().__init__(server_address, password)
        # Client data.
        self.unhandled_items: list[tuple[NetworkItem, int]] = []
        self.last_item_handled: int = -1
        self.last_rcvd_index: int = -1
        self.mkdd_locations_checked: set[int] = set()
        self.victory_sent: bool = False
        self.latest_error: str|None = None

        self.dolphin_sync_task: Optional[asyncio.Task[None]] = None
        self.dolphin_status: str = CONNECTION_INITIAL_STATUS

        # Options.
        self.options: options.MkddOptions = options.init_options()
        self.trophy_requirement: int = 0

        # Game data.
        self.game_state: game_state.MkddGameState = game_state.MkddGameState(mem_addresses.MkddMemAddressesUsa)
        self.game_state.options = self.options
        self.trophies: int = 0 # Trophies aren't anything ingame, so it isn't part of game state.
        self.victory: bool = False


    def reset_server_state(self):
        """
        Disconnect the client from the server and reset game state variables.
        """
        self.unhandled_items = []
        self.last_rcvd_index = -1
        self.last_item_handled = -1
        self.mkdd_locations_checked = set()
        self.victory_sent: bool = False
        self.game_state = game_state.MkddGameState(mem_addresses.MkddMemAddressesUsa)
        self.game_state.options = self.options
        self.trophies = 0
        self.trophy_requirement = 0
        self.victory = False
        if self.dolphin_status == CONNECTION_CONNECTED_STATUS:
            self.game_state.sync_state()
        sync_ui(self)
        super().reset_server_state()


    async def server_auth(self, password_requested: bool = False) -> None:
        """
        Authenticate with the Archipelago server.

        :param password_requested: Whether the server requires a password. Defaults to `False`.
        """
        if password_requested and not self.password:
            await super(MkddContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()


    def on_package(self, cmd: str, args: dict[str, Any]) -> None:
        """
        Handle incoming packages from the server.

        :param cmd: The command received from the server.
        :param args: The command arguments.
        """
        match cmd:
            case "Connected":
                slot_data: dict = args.get("slot_data")
                host_version: str = slot_data.get("version")
                if not host_version.startswith(self.compatible_version):
                    self.gui_error("Incompatible seed/client",
                        f"The seed was generated using version {host_version} of MKDDAP.\n" +
                        f"Client's version: {version.get_version()}"
                    )
                    self.disconnect()
                    return
                
                if "death_link" in slot_data:
                    Utils.async_start(self.update_death_link(bool(args["slot_data"]["death_link"])))
                
                self.options.update_from_slot_data(slot_data)
                self.trophy_requirement = slot_data["trophy_requirement"]
                self.game_state.cups_courses = slot_data["cups_courses"]

                self.game_state.character_item_total_weights = slot_data.get("character_item_total_weights")
                self.game_state.global_items_total_weights = slot_data.get("global_items_total_weights")

                self.mkdd_locations_checked = set(args.get("checked_locations"))
                if self.dolphin_status == CONNECTION_CONNECTED_STATUS:
                    self.game_state.sync_state()
                    self.game_state.queue_ingame_message("Connected!")
                sync_ui(self)
            case "ReceivedItems":
                if args["index"] >= self.last_rcvd_index:
                    self.last_rcvd_index = args["index"]
                    for item in args["items"]:
                        self.unhandled_items.append((item, self.last_rcvd_index))
                        self.last_rcvd_index += 1
                self.unhandled_items.sort(key=lambda v: v[1])
            case "RoomUpdate":
                self.mkdd_locations_checked.update(args.get("checked_locations", set()))
            case "PrintJSON":
                if args.get("type") == "ItemSend":
                    to_player: int = args["receiving"]
                    nw_item: NetworkItem = args["item"]
                    from_player: int = nw_item.player
                    item_name: str = self.item_names.lookup_in_slot(nw_item.item, to_player)
                    if to_player == self.slot and from_player == self.slot:
                        self.game_state.queue_ingame_message(f"You found your\n{item_name}")
                    elif to_player == self.slot:
                        from_player_name: str = self.player_names[from_player]
                        self.game_state.queue_ingame_message(f"{from_player_name} found your\n{item_name}")
                    elif from_player == self.slot:
                        to_player_name: str = self.player_names[to_player]
                        self.game_state.queue_ingame_message(f"You found {to_player_name}'s\n{item_name}")
        # Relay packages to the tracker also.
        super().on_package(cmd, args)


    def make_gui(self) -> type["kvui.GameManager"]:
        """
        Initialize the GUI for Mario Kart Double Dash client.

        :return: The client's GUI.
        """
        # Late importing so that kvui doesn't create window before it's time.
        from kvui import GameManager
        from . import gui
        base_class: type = GameManager
        ut_title: str = ""
        # Use Universal Tracker gui only if it's recent enough version.
        if tracker_loaded and UT_VERSION >= "v0.2.12":
            base_class = super().make_gui()
            ut_title = f" | Universal Tracker {UT_VERSION}"
        return gui.make_gui(base_class, ut_title)


###### Dolphin connection ######
def apply_ar_code(code: list[int]):
    for i in range(0, len(code), 2):
        command = (code[i] & 0xFE00_0000) >> 24
        address = (code[i] & 0x01FF_FFFF) | 0x8000_0000
        if command == 0x04:
            dolphin.write_word(address, code[i + 1])
        elif command == 0x00:
            dolphin.write_byte(address, code[i + 1])
        else:
            logger.warn(f"Unknown AR code: {command:2x}")


def apply_dict_patch(code: dict[int, list[int]]):
    for start_address, rows in code.items():
        address = start_address
        for row in rows:
            dolphin.write_word(address, row)
            address += 4


def apply_patch():
    apply_dict_patch(patches.character_selection)
    apply_dict_patch(patches.kart_selection)
    apply_dict_patch(patches.update_menu_pointer)
    apply_dict_patch(patches.cup_selection)
    apply_dict_patch(patches.vehicle_class_selector)
    apply_dict_patch(patches.time_trial_items)
    apply_dict_patch(patches.item_shuffle)
    apply_dict_patch(patches.item_box)
    apply_dict_patch(patches.rolling_item_box)
    apply_dict_patch(patches.force_item_shuffle)
    apply_dict_patch(patches.item_box)
    apply_dict_patch(patches.car_item_box)
    apply_dict_patch(patches.disable_start_pos_shuffle)
    apply_dict_patch(patches.spawn_item)
    apply_dict_patch(patches.draw_string)
    apply_dict_patch(patches.invalidate_cache)
    apply_ar_code(ar_codes.lap_modifier)
    apply_ar_code(ar_codes.gp_course_selection)
    apply_ar_code(ar_codes.fireball_limit)
    apply_ar_code(ar_codes.bomb_limit)
    apply_ar_code(ar_codes.disable_reverse_lakitu)
    logger.info("Patch Applied.")


def sync_ui(ctx: MkddContext) -> None:
    if ctx.ui:
        ctx.ui.update_characters(ctx.game_state.unlocked_characters)
        ctx.ui.update_karts(ctx.game_state.unlocked_karts)
        ctx.ui.update_speed_upgrades(ctx.game_state.engine_upgrade_level, 3)
        ctx.ui.update_cups(ctx.game_state.unlocked_cups)
        ctx.ui.update_cc(ctx.game_state.unlocked_vehicle_class)
        ctx.ui.update_trophies(ctx.trophies, ctx.trophy_requirement)


def give_item(ctx: MkddContext, item: MkddItemData) -> None:
    """
    Give an item to the player in-game.

    :param ctx: Mario Kart Double Dash client context.
    :param item_name: Name of the item to give.
    """
    if ctx.last_item_handled < 0 and items.TAG_SYNC_ONLY in item.tags:
        return

    if item.item_type == ItemType.CHARACTER:
        ctx.game_state.unlocked_characters.append(item.address)
    elif item.item_type == ItemType.KART:
        ctx.game_state.unlocked_karts.append(item.address)
    elif item.item_type == ItemType.KART_UPGRADE:
        ctx.game_state.kart_upgrades[item.address].append(item.meta)
    elif item.name == items.PROGRESSIVE_ENGINE:
        ctx.game_state.engine_upgrade_level += 1
    elif item.item_type == ItemType.CUP:
        ctx.game_state.unlocked_cups.append(item.address)
    elif item.item_type == ItemType.TT_COURSE:
        ctx.game_state.unlocked_courses.append(item.address)
    elif item.name == items.PROGRESSIVE_CLASS:
        ctx.game_state.unlocked_vehicle_class = min(ctx.game_state.unlocked_vehicle_class + 1, 3)
    elif item.name == items.PROGRESSIVE_CUP_SKIP:
        ctx.game_state.unlocked_cup_skips = min(ctx.game_state.unlocked_cup_skips + 1, 3)
    elif item.name == items.PROGRESSIVE_TIME_TRIAL_ITEM:
        ctx.game_state.time_trial_items = min(ctx.game_state.time_trial_items + 1, len(game_data.TT_ITEM_TABLE) - 1)
    elif item.item_type == ItemType.ITEM_UNLOCK:
        if item.meta["character"] == None:
            ctx.game_state.global_items.append(item.meta["item"])
        else:
            ctx.game_state.character_items[item.meta["character"]].append(item.meta["item"])
    elif item.name == items.PROGRESSIVE_STARTING_POSITION:
        ctx.game_state.starting_position = max(0, ctx.game_state.starting_position - 1)
    elif item.name == items.OVERLAPPING_START_TRAP:
        ctx.game_state.overlapping_start_traps += 1
    elif item.item_type == items.ItemType.RAIN_TRAP:
        ctx.game_state.rain_trap_queue.append(item.name)
    elif item.name == items.RANDOM_ITEM:
        ctx.game_state.queued_items += 1
    elif item.name == items.TROPHY:
        ctx.trophies += 1
    elif item.name == items.VICTORY:
        ctx.victory = True


def give_items(ctx: MkddContext) -> None:
    """
    Give the player all outstanding items they have yet to receive.

    :param ctx: Mario Kart Double Dash client context.
    """
    if len(ctx.unhandled_items) == 0:
        return
    last_item = ctx.last_item_handled
    for item, idx in ctx.unhandled_items:
        if ctx.last_item_handled < idx:
            give_item(ctx, items.data_table[item.item])
            last_item = idx
    ctx.last_item_handled = last_item
    ctx.game_state.sync_state()
    sync_ui(ctx)
    ctx.unhandled_items.clear()


async def check_locations(ctx: MkddContext) -> None:
    """
    Iterate through all locations and check whether the player has checked each location.

    Update the server with all newly checked locations since the last update. If the player has completed the goal,
    notify the server.

    :param ctx: Mario Kart Double Dash client context.
    """
    new_location_names: set[str] = set()

    if ctx.trophies >= ctx.trophy_requirement:
        new_location_names.add(locations.TROPHY_GOAL)
    
    if ctx.game_state.state_valid:
        new_location_names |= ctx.game_state.check_item_box_locations()
        new_location_names |= ctx.game_state.check_route_locations()
        new_location_names |= ctx.game_state.check_finish_course_locations()
        new_location_names |= ctx.game_state.check_take_lead_locations()
        new_location_names |= ctx.game_state.check_gp_race_locations()
        new_location_names |= ctx.game_state.check_gp_cup_locations()
        new_location_names |= ctx.game_state.check_all_cup_tour_locations()
        new_location_names |= ctx.game_state.check_tt_locations()

    new_locations = {locations.name_to_id.get(loc_name) for loc_name in new_location_names}
    new_locations.discard(None)
    ctx.mkdd_locations_checked.update(new_locations)
    # Send the list of newly-checked locations to the server.
    mkdd_locations_checked = ctx.mkdd_locations_checked.difference(ctx.checked_locations)
    if mkdd_locations_checked:
        await ctx.send_msgs([{"cmd": "LocationChecks", "locations": mkdd_locations_checked}])


def update_game(ctx: MkddContext) -> None:
    """
    Update game state such as controlling character selection.

    :param ctx: Mario Kart Double Dash client context.
    """
    apply_ar_code(ar_codes.unlock_everything)
    ctx.game_state.handle_character_menu()
    ctx.game_state.apply_shuffled_courses()
    ctx.game_state.apply_item_box_items()
    ctx.game_state.update_item_box_visuals(ctx.mkdd_locations_checked)
    ctx.game_state.apply_lap_counts()
    ctx.game_state.handle_all_cup_tour()
    ctx.game_state.apply_course_availability()
    ctx.game_state.add_course_selection_texts()
    ctx.game_state.add_pause_texts()
    ctx.game_state.apply_speed_modifiers()
    ctx.game_state.apply_kart_stats()
    ctx.game_state.handle_starting_position()
    ctx.game_state.handle_overlapping_start_trap()
    ctx.game_state.handle_rain_traps()


async def check_current_course_changed(ctx: MkddContext) -> None:
    """
    Check if the player has moved to a new stage.
    If so, update all trackers with the new stage name.

    :param ctx: Mario Kart Double Dash client context.
    """
    if ctx.game_state.course_changed:
        # Send a Bounced message containing the new stage name to all trackers connected to the current slot.
        data_to_send = {"mkdd_course_name": ctx.game_state.current_course.name}
        message = {
            "cmd": "Bounce",
            "slots": [ctx.slot],
            "data": data_to_send,
        }
        await ctx.send_msgs([message])


async def dolphin_sync_task(ctx: MkddContext) -> None:
    """
    The task loop for managing the connection to Dolphin.
    While connected, read the emulator's memory to look for any relevant changes made by the player in the game.

    :param ctx: Mario Kart Double Dash client context.
    """
    logger.info("Starting Dolphin connector. Use /dolphin for status information.")
    while not ctx.exit_event.is_set():
        dolphin_name = os.getenv(DME_DOLPHIN_PROCESS_NAME_ENV_VARIABLE) or "Dolphin"
        try:
            if dolphin.is_hooked() and ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
                if ctx.ui:
                    ctx.ui.show_launch_button(False)
                if ctx.slot is not None:
                    give_items(ctx)

                    ctx.game_state.update()
                    await check_current_course_changed(ctx)
                    await check_locations(ctx)
                    update_game(ctx)

                    if ctx.victory and not ctx.victory_sent:
                        await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                        ctx.victory_sent = True
                else:
                    ctx.game_state.print_ingame(304, 13, "Waiting connection to server", 0)
                ctx.game_state.flush_ingame_text() # Show text regardless of connection to server.
                await asyncio.sleep(0.1)
            else:
                if ctx.ui:
                    ctx.ui.set_launch_func(ctx.command_processor._cmd_launch)
                    ctx.ui.show_launch_button(True)
                if ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
                    logger.warning(f"Connection to {dolphin_name} lost, reconnecting...")
                    ctx.dolphin_status = CONNECTION_LOST_STATUS
                logger.info(f"Attempting to connect to {dolphin_name}...")
                dolphin.hook()
                if dolphin.is_hooked():
                    if dolphin.read_bytes(0x80000000, 6) != b"GM4E01":
                        logger.info(CONNECTION_REFUSED_GAME_STATUS)
                        ctx.dolphin_status = CONNECTION_REFUSED_GAME_STATUS
                        dolphin.un_hook()
                        await asyncio.sleep(5)
                    else:
                        logger.info(CONNECTION_CONNECTED_STATUS)
                        ctx.dolphin_status = CONNECTION_CONNECTED_STATUS
                        apply_patch()
                        ctx.game_state.sync_state()
                        give_items(ctx)
                else:
                    logger.info(f"Connection to {dolphin_name} failed, attempting again in 5 seconds...")
                    ctx.dolphin_status = CONNECTION_LOST_STATUS
                    await asyncio.sleep(5)
                    continue
        except Exception as error:
            dolphin.un_hook()
            if str(error).startswith("Could not write memory") or str(error).startswith("Could not read memory"):
                logger.warning(f"Connection to {dolphin_name} was lost.")
            else:
                logger.warning("Unexpected error happened. Use /error to get details.")
            logger.debug(traceback.format_exc())
            ctx.latest_error = traceback.format_exc()
            ctx.dolphin_status = CONNECTION_LOST_STATUS
            await asyncio.sleep(5)
            continue


def main(*args) -> None:
    """
    Run the main async loop for Mario Kart Double Dash client.

    :param connect: Address of the Archipelago server.
    :param password: Password for server authentication.
    """
    Utils.init_logging("Mario Kart Double Dash Client")

    async def _main(connect: Optional[str], password: Optional[str]) -> None:
        ctx = MkddContext(connect, password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")

        # Runs Universal Tracker's internal generator
        if tracker_loaded:
            ctx.run_generator()
            ctx.tags.remove("Tracker")

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        await asyncio.sleep(1)

        ctx.dolphin_sync_task = asyncio.create_task(dolphin_sync_task(ctx), name="DolphinSync")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.dolphin_sync_task:
            await asyncio.sleep(3)
            await ctx.dolphin_sync_task

    parser = get_base_parser(description="Mario Kart Double Dash Client.")
    parser.add_argument('--name', default=None, help="Slot Name to connect as.")
    parser.add_argument("url", nargs="?", help="Archipelago connection url")
    args = parser.parse_args(args)

    from CommonClient import handle_url_arg
    args = handle_url_arg(args, parser=parser)

    import colorama

    colorama.init()
    asyncio.run(_main(args.connect, args.password))
    colorama.deinit()


if __name__ == "__main__":
    parser = get_base_parser()
    args = parser.parse_args()
    main(args)
