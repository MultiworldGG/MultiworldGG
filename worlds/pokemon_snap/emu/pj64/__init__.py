from typing import Optional, Any, Sequence
import base64, os, re, time, asyncio

import Utils
from CommonClient import logger, server_loop, get_base_parser, gui_enabled

from .pj64_connector import PJ64Context, pj64connect, pj64disconnect, pj64_read_memory, pj64_write_memory
from .pj64_constants import *
from .update_pj64_config import safe_load_pj64_config
from ..ut_helper import has_invalid_universal_tracker, universal_tracker_loaded
from .. import PokemonSnapGenericEmuClient, PokemonSnapGenericCommandProcessor
from ... import addresses as addr
from ...client import PokemonSnapClient
from ...constants import CLIENT_NAME, MIN_UNIVERSAL_TRACKER_VERSION

if universal_tracker_loaded:
    from worlds.tracker.TrackerClient import TrackerGameContext as CommonContext, UT_VERSION
else:
    from CommonClient import CommonContext

class PokemonSnapCommandProcessor(PokemonSnapGenericCommandProcessor):
    def __init__(self, ctx: CommonContext, server_address: str = None):
        super().__init__(ctx, server_address)

    def _cmd_pj64_status(self):
        """Gets the current status of the Project 64 connection."""
        if isinstance(self.ctx, PokemonSnapContext):
            logger.info(f"Project64 Status: {self.ctx.pj64_status}")


class PokemonSnapContext(CommonContext, PJ64Context, PokemonSnapGenericEmuClient):
    client: "PokemonSnapClient"
    command_processor = PokemonSnapCommandProcessor
    game = "Pokemon Snap"
    items_handling = 0b111
    tracker_enabled: bool = False
    instance_id: float | None
    pj64_sync_task: Optional[asyncio.Task[None]] = None
    pj64_status: str

    def __init__(self, server_address, password, ap_port):
        """
        Initialize the Pokemon Snap Universal Context.

        :param server_address: Address of the Archipelago server.
        :param password: Password for server authentication.
        """
        CommonContext.__init__(self, server_address, password)
        PJ64Context.__init__(self, ap_port)
        self.client = PokemonSnapClient()
        self.instance_id = None
        self.tracker_enabled = universal_tracker_loaded
        self.pj64_status = INITIAL_STATUS
        self.ap_port = ap_port
        self.slot_data = {}

    def on_package(self, cmd: str, args: dict):
        """
        Handle incoming packages from the server.

        :param cmd: The command received from the server.
        :param args: The command arguments.
        """
        CommonContext.on_package(self, cmd, args)
        match cmd:
            case "PrintJSON":
                if args.get("type", "") == "Countdown" and len(list(args.get("data", []))) > 0 and \
                        "starting countdown of " in args["data"][0]["text"].lower():
                    countdown_var: int = int(re.search(r"\d+", args["data"][0]["text"]).group())
                    print(str(countdown_var))

            case "Connected":  # On Connect
                self.slot_data = args.get("slot_data", {})

            case "Bounced":
                if "tags" not in args:
                    return
                if not hasattr(self, "instance_id"):
                    self.instance_id = time.time()

    def _main(self):
        if self.tracker_enabled:
            self.run_generator()
            self.tags.remove("Tracker")
        else:
            logger.warning("Could not find Universal Tracker.")

    def make_gui(self):
        if universal_tracker_loaded and has_invalid_universal_tracker(UT_VERSION):
            Utils.messagebox("Universal Tracker needs updated",
            f"Please update your Universal Tracker. The version currently installed is {UT_VERSION}.", error=True)
            raise ImportError(f"Need to update universal tracker version to at least v{'.'.join(map(str, MIN_UNIVERSAL_TRACKER_VERSION))}.")

        # Performing local import to prevent additional UIs to appear during the patching process.
        # This appears to be occurring if a spawned process does not have a UI element when importing kvui/kivymd.
        from kvui import GameManager
        ui: type[GameManager] = CommonContext.make_gui(self)
        class UniversalWrapper(ui):
            base_title: str = "Pokemon Snap Client"

            def build(self):
                container = super().build()
                if universal_tracker_loaded:
                    self.base_title += f" | Universal Tracker {UT_VERSION}"
                return container

        return UniversalWrapper

    async def _expansion_loaded(self) -> bool:
        magic = (await pj64_read_memory(self, "u32", addr.EXPANSION_MAGIC, 4))[0]
        return magic == addr.EXPANSION_LOADED

    async def _read_auth_token(self):
        """Read the per-seed auth token from the ROM as base64, or None."""
        try:
            if self.streams is None or not await self._expansion_loaded():
                return None
            raw = bytes(await pj64_read_memory(self, "u8", addr.AUTH_ADDR, addr.AUTH_LEN))
            if not raw or raw == addr.UNPATCHED_AUTH:
                return None
            return base64.b64encode(raw).decode("ascii")
        except Exception:
            return None

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)

        notified = False
        while not self.auth and not self.exit_event.is_set():
            token = await self._read_auth_token()
            if token:
                self.auth = token
                break
            if not notified:
                logger.info("Waiting to read the connect token from a patched, running Pokemon Snap ROM...")
                notified = True
            await asyncio.sleep(3)

        if not self.auth:
            return

        await self.send_connect()


    async def wait_for_next_loop(self, time_to_wait: float):
        await asyncio.sleep(time_to_wait)

    async def pj64_sync_main_task(self):
        logger.info(f"Using {CLIENT_NAME}...")
        logger.info("Starting Project64 connector. Use /pj64_status for status information.")

        try:
            while not self.exit_event.is_set():
                try:
                    if not self.pj64_status == CONNECTED_STATUS:
                        if not self.pj64_status == CONNECTING_STATUS:
                            if not await pj64connect(self):
                                self.pj64_status = DISCONNECTED_STATUS
                                logger.info(self.pj64_status)
                                await self.wait_for_next_loop(5)
                                continue
                            self.pj64_status = CONNECTING_STATUS
                            logger.info(self.pj64_status)

                        # Wait for AP login and the patched ROM to be running.
                        if not self.slot or not await self._expansion_loaded():
                            await self.wait_for_next_loop(1)
                            continue

                        self.pj64_status = CONNECTED_STATUS
                        logger.info(self.pj64_status)
                    if self.slot and await self._expansion_loaded(): 
                        await self.client.check_snap_locations(self, self)
                        await self.client.receive_snap_items(self, self)
                    await self.wait_for_next_loop(0.125)

                except Exception as ex:
                    logger.error(f"Project64 connection lost: {ex}")
                    pj64disconnect(self)
                    self.pj64_status = DISCONNECTED_STATUS
                    logger.info(DISCONNECTED_STATUS)
                    await self.wait_for_next_loop(5)
                    continue
        except Exception as threadEx:
            logger.error("Something went horribly wrong with the Pokemon Snap client. Details: " + str(threadEx))
    
    async def read(self, ctx: "PokemonSnapContext", read_list: Sequence[tuple[int, int, str]]):
        return [await pj64_read_memory(ctx, type, address, size) for address, size, type in read_list]

    async def write(self, ctx: "PokemonSnapContext", write_list: Sequence[tuple[int, Sequence[int], str]]):
        return [await pj64_write_memory(ctx, type, address, values) for address, values, type in write_list]


def _patch_and_launch(patch_file: str) -> str:
    """Turn a dragged-in .apsnap patch into a ROM and start the emulator on it.

    Returns the Archipelago server address embedded in the patch (set when the
    patch was downloaded from a room), or an empty string if none.
    """
    from ...rom import PokemonSnapProcedurePatch

    rom_path = os.path.splitext(patch_file)[0] + ".z64"
    server = ""
    try:
        patch = PokemonSnapProcedurePatch(patch_file)
        patch.read()
        server = patch.server or ""
        if not os.path.exists(rom_path):
            patch.patch(rom_path)
            logger.info(f"Patched ROM created at {rom_path}")
        else:
            logger.info(f"Using existing patched ROM at {rom_path}")
    except Exception as ex:
        logger.error(f"Failed to create the patched ROM: {ex}")
        Utils.messagebox(f"{CLIENT_NAME} Patch Error", str(ex), True)
        return server

    from settings import get_settings
    snap_options = get_settings()["pokemon_snap_options"]
    return _launch_pj64(server, rom_path, snap_options["emulator_settings"])

def _launch_pj64(server: str, rom_path: str, emulator_settings: dict[str, Any]):
    try:
        safe_load_pj64_config()
    except Exception as ex:
        logger.warning(f"Could not update the Project64 config automatically: {ex}")
    
    if not emulator_settings["auto_start"]:
        logger.info(f"Auto-start is off; open this ROM in your emulator: {rom_path}")
        return server

    exe = str(emulator_settings["path"])
    if not os.path.exists(exe):
        exe = Utils.user_path(exe)
    if not os.path.exists(exe):
        logger.info(f"No emulator configured; open this ROM in Project64: {rom_path}")
        return server

    # PJ64 3.0 finds Scripts/ and Config/ relative to the cwd, so run it from there.
    import subprocess
    exe = os.path.abspath(exe)
    subprocess.Popen([exe, os.path.abspath(rom_path)], cwd=os.path.dirname(exe))
    logger.info(f"Launched {exe} with {rom_path}")
    logger.info("If the client doesn't connect, start ap_psnap_pj64_adapter_30.js via "
                "Debugger -> Scripts in Project64.")
    return server

def launch(*launch_args: str):
    async def _main(connect, password):
        try:
            ap_port = safe_load_pj64_config()
            ctx = PokemonSnapContext(connect, password, ap_port)
            ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")

            ctx.pj64_sync_task = asyncio.create_task(ctx.pj64_sync_main_task(), name="PokemonSnap_PJ64Sync")

            # Runs Universal Tracker's internal generator
            ctx._main()

            if gui_enabled:
                ctx.run_gui()
            ctx.run_cli()
            await ctx.wait_for_next_loop(5)

            await ctx.exit_event.wait()
            await ctx.shutdown()

            if ctx.pj64_sync_task:
                await ctx.pj64_sync_task
        except Exception as clientEx:
            client_msg: str = (f"An unknown error occurred while running Pokemon Snap's client.\n" +
                f"Additional details:\n") + str(clientEx)
            logger.error(client_msg)
            Utils.messagebox(f"{CLIENT_NAME} Client Issue", client_msg, True)
            raise clientEx
    
    Utils.init_logging(CLIENT_NAME)
    logger.info(f"Starting {CLIENT_NAME}...")

    parser = get_base_parser()
    parser.add_argument("patch_file", default="", type=str, nargs="?",
                        help="Path to an .apsnap patch file to apply and launch.")
    args = parser.parse_args(launch_args)

    server_address: str = args.connect or ""
    if args.patch_file:
        patch_server = _patch_and_launch(args.patch_file)
        # --connect wins; else use the patch's embedded room address.
        if patch_server and not args.connect:
            server_address = patch_server
            logger.info(f"Connecting to the server address from the patch: {server_address}")

    import colorama
    colorama.just_fix_windows_console()
    asyncio.run(_main(server_address, args.password))
    colorama.deinit()