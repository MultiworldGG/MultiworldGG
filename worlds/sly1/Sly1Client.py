from typing import Optional
import asyncio
import multiprocessing
import traceback
import os

# Move up two directories from the client script location
launcher_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
os.chdir(launcher_dir)

from CommonClient import get_base_parser, logger, server_loop, gui_enabled
import Utils
apname = Utils.instance_name if Utils.instance_name else "Archipelago"

from worlds.sly1.Sly1Interface import Sly1Interface, Sly1Episode
from worlds.sly1.Callbacks import init, update
from worlds.sly1.data.Constants import LEVELS, MOVES

# Load Universal Tracker
tracker_loaded: bool = False
try:
    from worlds.tracker.TrackerClient import (
        TrackerCommandProcessor as ClientCommandProcessor,
        TrackerGameContext as CommonContext,
        UT_VERSION
    )

    tracker_loaded = True
except ImportError:
    from CommonClient import ClientCommandProcessor, CommonContext

class Sly1CommandProcessor(ClientCommandProcessor):
    def _cmd_vaults(self):
        """Print the names of levels with vaults you can open"""
        if isinstance(self.ctx, Sly1Context):
            if self.ctx.slot_data is None:
                logger.info("Connect to a slot first!")
            elif self.ctx.slot_data.get("ItemCluesanityBundleSize") == 0:
                logger.info("Just do it like in vanilla, dummy!")
            elif not self.ctx.openable_vaults:
                logger.info("No vaults available to open")
            else:
                logger.info(f"Can open: {', '.join(self.ctx.openable_vaults)}")

    def _cmd_check_goal(self):
        """Check your progress towards your goal"""
        if isinstance(self.ctx, Sly1Context):
            if self.ctx.slot_data is None:
                logger.info("Connect to a slot first!")
            elif self.ctx.slot_data.get("UnlockClockwerk", 1) == 1:
                logger.info(f"{self.ctx.bosses_beaten} bosses out of {self.ctx.slot_data.get("RequiredBosses")}")
            else:
                logger.info(f"{self.ctx.goal_pages} pages out of {self.ctx.slot_data.get("RequiredPages")}")

class Sly1Context(CommonContext):
    command_processor = Sly1CommandProcessor
    game_interface: Sly1Interface
    game = "Sly Cooper and the Thievius Raccoonus"
    items_handling = 0b111
    pcsx2_sync_task: Optional[asyncio.Task] = None
    is_connected_to_game: bool = False
    is_connected_to_server: bool = False
    slot_data: Optional[dict[str, Utils.Any]] = None
    last_error_message: Optional[str] = None
    openable_vaults: list[str] = []
    opened_vaults: list[str] = []
    current_scene_key = None
    last_written_moves: int = -1
    first_hideout = False

    #Game state
    current_episode: Optional[Sly1Episode] = None
    thief_moves: int = 0
    bosses_beaten: int = 0
    SAVE_FILE = "sly1_item_progress.json"

    #Items and checks
    inven_keys: list[int] = [0, 0, 0, 0]
    inven_moves: list[int] = [0 for _ in MOVES]
    level_keys: list[list[bool]] = [
        [False for _ in levels[0]] for levels in LEVELS.values()
    ]
    vaults: list[list[bool]] = [
        [False for _ in levels[0]] for levels in LEVELS.values()
    ]
    hourglasses: list[list[bool]] = [
        [False for _ in levels[0]] for levels in LEVELS.values()
    ]
    bottles: list[list[int]] = [
        [0 for _ in levels[0]] for levels in LEVELS.values()
    ]
    hubs: list[bool] = [False, False, False, False]
    goal_pages: int = 0
    all_moves = 0
    for name, move in MOVES.items():
        if "Blueprints" in name:
            continue
        if isinstance(move, list):
            for level in move:
                all_moves |= level
        else:
            all_moves |= move

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.version = [0,3,4]
        self.game_interface = Sly1Interface(logger)
        self.names_dirty = True

    def run_generator(self):
        if tracker_loaded:
            super().run_generator()

    def make_gui(self):
        ui = super().make_gui()
        ui.base_title = f"Sly 1 Client v{'.'.join([str(i) for i in self.version])}"
        if tracker_loaded:
            ui.base_title += f" | Universal Tracker {UT_VERSION}"

        # AP version is added behind this automatically
        ui.base_title += f" | {apname}"
        return ui

    async def server_auth(self, password_requested: bool = False) -> None:
        if password_requested and not self.password:
            await super(Sly1Context, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        super().on_package(cmd, args)
        if cmd == "Connected":
            self.slot_data = args["slot_data"]
            self.current_scene_key = f"sly1_current_scene_T{self.team}_{self.slot}"

def update_connection_status(ctx: Sly1Context, status: bool):
    if ctx.is_connected_to_game == status:
        return

    if status:
        logger.info("Connected to Sly 1")
    else:
        logger.info("Unable to connect to the PCSX2 instance, attempting to reconnect...")

    ctx.is_connected_to_game = status

async def pcsx2_sync_task(ctx: Sly1Context):
    logger.info("Starting Sly 1 Connector, attempting to connect to emulator...")
    ctx.game_interface.connect_to_game()
    while not ctx.exit_event.is_set():
        try:
            is_connected = ctx.game_interface.get_connection_state()
            update_connection_status(ctx, is_connected)
            if is_connected:
                await _handle_game_ready(ctx)
            else:
                await _handle_game_not_ready(ctx)
        except ConnectionError:
            ctx.game_interface.disconnect_from_game()
        except Exception as e:
            if isinstance(e, RuntimeError):
                logger.error(str(e))
            else:
                logger.error(traceback.format_exc())
            await asyncio.sleep(3)
            continue

async def _handle_game_ready(ctx: Sly1Context) -> None:
    current_address = ctx.game_interface.get_current_address()
    current_episode = ctx.game_interface.get_current_episode()
    current_level = ctx.game_interface.get_current_level_name()

    ctx.game_interface.skip_cutscene(ctx)

    #if ctx.is_loading:
        #if not ctx.game_interface.is_loading():
            #ctx.is_loading = False
            #await asyncio.sleep(1)
        #await asyncio.sleep(0.1)
        #return

    #if ctx.game_interface.is_loading():
        #ctx.is_loading = True
        #return

    connected_to_server = (ctx.server is not None) and (ctx.slot is not None)

    new_connection = ctx.is_connected_to_server != connected_to_server
    if ctx.current_episode != current_episode or new_connection:
        ctx.current_episode = current_episode
        ctx.is_connected_to_server = connected_to_server
        await init(ctx, connected_to_server)
        await ctx.game_interface.write_name_pointers()

    await update(ctx, connected_to_server)

    if ctx.server:
        ctx.last_error_message = None
        if not ctx.slot:
            await asyncio.sleep(1)
            return

        await asyncio.sleep(0.1)
    else:
        message = "Waiting for player to connect to server"
        if ctx.last_error_message is not message:
            logger.info("Waiting for player to connect to server")
            ctx.last_error_message = message
        await asyncio.sleep(1)


async def _handle_game_not_ready(ctx: Sly1Context):
    """If the game is not connected, this will attempt to retry connecting to the game."""
    ctx.game_interface.connect_to_game()
    await asyncio.sleep(3)

def launch_client():
    Utils.init_logging("Sly1 Client")

    async def main():
        multiprocessing.freeze_support()
        logger.info("main")
        parser = get_base_parser()
        args = parser.parse_args()
        ctx = Sly1Context(args.connect, args.password)

        logger.info("Connecting to server...")
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="Server Loop")
        ctx.tags.add("Client")

        if tracker_loaded:
            ctx.run_generator()
            ctx.tags.remove("Tracker")

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        logger.info("Running game...")
        ctx.pcsx2_sync_task = asyncio.create_task(pcsx2_sync_task(ctx), name="PCSX2 Sync")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.pcsx2_sync_task:
            await asyncio.sleep(3)
            await ctx.pcsx2_sync_task

    import colorama

    colorama.init()

    asyncio.run(main())
    colorama.deinit()

if __name__ == "__main__":
    launch_client()