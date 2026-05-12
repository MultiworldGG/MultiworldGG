import asyncio
import json
import os
import multiprocessing
import zipfile
from asyncio import StreamReader, StreamWriter

# CommonClient import first to trigger ModuleUpdater
from CommonClient import CommonContext, server_loop, gui_enabled, \
    ClientCommandProcessor, logger, get_base_parser
from Utils import async_start, init_logging
try:
    from Utils import instance_name as apname
except ImportError:
    apname = "Archipelago"
from worlds import network_data_package
from .. import OOTWorld, launch_rom
from ..Rom import Rom, compress_rom_file
from ..N64Patch import apply_patch_file


CONNECTION_TIMING_OUT_STATUS = "Connection timing out. Please restart your emulator."
CONNECTION_REFUSED_STATUS = "Connection refused. Please start your emulator and load your OoT AP ROM."
CONNECTION_RESET_STATUS = "Connection was reset. Please restart your emulator."
CONNECTION_TENTATIVE_STATUS = "Initial Connection Made"
CONNECTION_CONNECTED_STATUS = "Connected"
CONNECTION_INITIAL_STATUS = "Connection has not been initiated"

"""
Payload: bridge -> client
{
    playerName: string,
    locations: dict,
    deathlinkActive: bool,
    isDead: bool,
    gameComplete: bool
}

Payload: client -> bridge
{
    items: list,
    playerNames: list,
    triggerDeath: bool
}

deathlink_pending: we need to kill the player
deathlink_sent_this_death: we interacted with the multiworld on this death, waiting to reset with living link

"""

oot_loc_name_to_id = network_data_package["games"]["Ocarina of Time"]["location_name_to_id"]

script_version: int = 7

def get_item_value(ap_id):
    return ap_id - 66000


class OoTCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx):
        super().__init__(ctx)

    def _cmd_n64(self):
        """Check N64 Connection State"""
        if isinstance(self.ctx, OoTContext):
            logger.info(f"N64 Status: {self.ctx.n64_status}")

    def _cmd_deathlink(self):
        """Toggle deathlink from client. Overrides default setting."""
        if isinstance(self.ctx, OoTContext):
            self.ctx.deathlink_client_override = True
            self.ctx.deathlink_enabled = not self.ctx.deathlink_enabled
            async_start(self.ctx.update_death_link(self.ctx.deathlink_enabled), name="Update Deathlink")


class OoTContext(CommonContext):
    command_processor = OoTCommandProcessor
    items_handling = 0b001  # full local

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.game = 'Ocarina of Time'
        self.n64_streams: (StreamReader, StreamWriter) = None
        self.n64_sync_task = None
        self.n64_status = CONNECTION_INITIAL_STATUS
        self.awaiting_rom = False
        self.location_table = {}
        self.collectible_table = {}
        self.collectible_override_flags_address = 0
        self.collectible_offsets = {}
        self.deathlink_enabled = False
        self.deathlink_pending = False
        self.deathlink_sent_this_death = False
        self.deathlink_client_override = False
        self.version_warning = False
        self.pending_display_items: list = []
        self._unknown_location_warnings: set[str] = set()

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(OoTContext, self).server_auth(password_requested)
        if not self.auth:
            self.awaiting_rom = True
            logger.info('Awaiting connection to emulator to get player information')
            return

        await self.send_connect()

    def on_deathlink(self, data: dict):
        self.deathlink_pending = True
        super().on_deathlink(data)

    def run_gui(self):
        from kvui import GameManager

        class OoTManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = apname + " Ocarina of Time Client"

        self.ui = OoTManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    def on_package(self, cmd, args):
        if cmd == 'Connected':
            slot_data = args.get('slot_data', None)
            if slot_data:
                self.collectible_override_flags_address = slot_data.get('collectible_override_flags', 0)
                self.collectible_offsets = slot_data.get('collectible_flag_offsets', {})
        elif cmd == 'PrintJSON':
            if args.get('type') == 'ItemSend':
                network_item = args.get('item')
                if network_item and network_item.player == self.slot:
                    receiving_slot = args.get('receiving', 0)
                    if receiving_slot != self.slot:
                        try:
                            item_name = self.item_names.lookup_in_slot(network_item.item, receiving_slot)
                            player_name = self.player_names.get(receiving_slot, f'Player {receiving_slot}')
                            self.pending_display_items.append({'item': item_name, 'player': player_name})
                        except Exception:
                            pass


def get_payload(ctx: OoTContext):
    if ctx.deathlink_enabled and ctx.deathlink_pending:
        trigger_death = True
        ctx.deathlink_sent_this_death = True
    else:
        trigger_death = False

    pending_display_items = ctx.pending_display_items
    ctx.pending_display_items = []

    payload = json.dumps({
            "items": [get_item_value(item.item) for item in ctx.items_received],
            "playerNames": [name for (i, name) in ctx.player_names.items() if i != 0],
            "triggerDeath": trigger_death,
            "collectibleOverrides": ctx.collectible_override_flags_address,
            "collectibleOffsets": ctx.collectible_offsets,
            "pendingDisplayItems": pending_display_items,
        })
    return payload


async def parse_payload(payload: dict, ctx: OoTContext, force: bool):

    # Refuse to do anything if ROM is detected as changed
    if ctx.auth and payload['playerName'] != ctx.auth:
        logger.warning("ROM change detected. Disconnecting and reconnecting...")
        ctx.deathlink_enabled = False
        ctx.deathlink_client_override = False
        ctx.finished_game = False
        ctx.location_table = {}
        ctx.collectible_table = {}
        ctx.deathlink_pending = False
        ctx.deathlink_sent_this_death = False
        ctx.pending_display_items = []
        ctx.auth = payload['playerName']
        await ctx.send_connect()
        return

    # Turn on deathlink if it is on, and if the client hasn't overriden it
    if payload['deathlinkActive'] and not ctx.deathlink_enabled and not ctx.deathlink_client_override:
        await ctx.update_death_link(True)
        ctx.deathlink_enabled = True

    # Game completion handling
    if payload['gameComplete'] and not ctx.finished_game:
        await ctx.send_msgs([{
            "cmd": "StatusUpdate",
            "status": 30
        }])
        ctx.finished_game = True

    # Locations handling
    locations = payload['locations']
    collectibles = payload['collectibles']

    # An empty table may be serialized as a list. Verify types for safety:
    if isinstance(locations, list):
        locations = {}
    if isinstance(collectibles, list):
        collectibles = {}

    if ctx.location_table != locations or ctx.collectible_table != collectibles:
        ctx.location_table = locations
        ctx.collectible_table = collectibles
        locs1 = []

        unknown_locations = []
        for loc, checked in ctx.location_table.items():
            if not checked:
                continue
            loc_id = oot_loc_name_to_id.get(loc)
            if loc_id is None:
                unknown_locations.append(loc)
                continue
            locs1.append(loc_id)

        for loc in unknown_locations:
            if loc not in ctx._unknown_location_warnings:
                logger.warning(f"Ignoring unknown OoT location from connector: {loc}")
                ctx._unknown_location_warnings.add(loc)

        locs2 = [int(loc) for loc, b in ctx.collectible_table.items() if b]
        await ctx.send_msgs([{
            "cmd": "LocationChecks",
            "locations": locs1 + locs2
        }])

    # Deathlink handling
    if ctx.deathlink_enabled:
        if payload['isDead']: # link is dead
            ctx.deathlink_pending = False
            if not ctx.deathlink_sent_this_death:
                ctx.deathlink_sent_this_death = True
                await ctx.send_death()
        else: # link is alive
            ctx.deathlink_sent_this_death = False


async def n64_sync_task(ctx: OoTContext):
    logger.info("Starting N64 connector. Use /n64 for status information.")
    while not ctx.exit_event.is_set():
        error_status = None
        if ctx.n64_streams:
            (reader, writer) = ctx.n64_streams
            msg = get_payload(ctx).encode()
            writer.write(msg)
            writer.write(b'\n')
            try:
                await asyncio.wait_for(writer.drain(), timeout=1.5)
                try:
                    data = await asyncio.wait_for(reader.readline(), timeout=10)
                    if not data:
                        raise ConnectionResetError
                    data_decoded = json.loads(data.decode())
                    reported_version = data_decoded.get('scriptVersion', 0)
                    if reported_version >= script_version:
                        if ctx.game is not None and 'locations' in data_decoded:
                            # Not just a keep alive ping, parse
                            try:
                                await parse_payload(data_decoded, ctx, False)
                            except Exception:
                                logger.exception("Failed to parse OoT payload; continuing connection loop.")
                        if not ctx.auth:
                            ctx.auth = data_decoded['playerName']
                            if ctx.awaiting_rom:
                                await ctx.server_auth(False)
                    else:
                        if not ctx.version_warning:
                            logger.warning(f"Bridge script version {reported_version}, expected {script_version}. "
                                "Please update to the latest version. "
                                f"Your connection to the {apname} server will not be accepted.")
                            ctx.version_warning = True
                except asyncio.TimeoutError:
                    error_status = CONNECTION_TIMING_OUT_STATUS
                    writer.close()
                    ctx.n64_streams = None
                except ConnectionResetError as e:
                    error_status = CONNECTION_RESET_STATUS
                    writer.close()
                    ctx.n64_streams = None
            except TimeoutError:
                error_status = CONNECTION_TIMING_OUT_STATUS
                writer.close()
                ctx.n64_streams = None
            except ConnectionResetError:
                error_status = CONNECTION_RESET_STATUS
                writer.close()
                ctx.n64_streams = None
            if ctx.n64_status == CONNECTION_TENTATIVE_STATUS:
                if not error_status:
                    logger.info("Successfully Connected to N64")
                    ctx.n64_status = CONNECTION_CONNECTED_STATUS
                else:
                    ctx.n64_status = f"Was tentatively connected but error occured: {error_status}"
            elif error_status:
                if ctx.n64_status != error_status:
                    logger.info("Lost connection to N64 and attempting to reconnect. Use /n64 for status updates")
                ctx.n64_status = error_status
            if error_status:
                await asyncio.sleep(1)
        else:
            try:
                ctx.n64_streams = await asyncio.wait_for(asyncio.open_connection("localhost", 28921), timeout=10)
                ctx.n64_status = CONNECTION_TENTATIVE_STATUS
            except TimeoutError:
                ctx.n64_status = CONNECTION_TIMING_OUT_STATUS
                continue
            except ConnectionRefusedError:
                ctx.n64_status = CONNECTION_REFUSED_STATUS
                await asyncio.sleep(1)
                continue


async def run_game(romfile):
    launch_rom(romfile, logger)


async def patch_and_run_game(apz5_file):
    apz5_file = os.path.abspath(apz5_file)
    base_name = os.path.splitext(apz5_file)[0]
    decomp_path = base_name + '-decomp.z64'
    comp_path = base_name + '.z64'
    rom_file_name = OOTWorld.settings.rom_file
    rom = Rom(rom_file_name)

    sub_file = None
    if zipfile.is_zipfile(apz5_file):
        for name in zipfile.ZipFile(apz5_file).namelist():
            if name.endswith('.zpf'):
                sub_file = name
                break

    apply_patch_file(rom, apz5_file, sub_file=sub_file)
    rom.write_to_file(decomp_path)
    compress_rom_file(decomp_path, comp_path)
    os.remove(decomp_path)
    async_start(run_game(comp_path))


def main(*launcher_args: str):

    init_logging("OoTClient")

    async def main():
        multiprocessing.freeze_support()
        parser = get_base_parser()
        parser.add_argument('apz5_file', default="", type=str, nargs="?",
                            help='Path to an APZ5 file')
        args = parser.parse_args(launcher_args)

        if args.apz5_file:
            logger.info("APZ5 file supplied, beginning patching process...")
            async_start(patch_and_run_game(args.apz5_file))

        ctx = OoTContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="Server Loop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        # Start the native emulator bridge (serves on localhost:28921)
        from .bridge import n64_bridge_task
        asyncio.create_task(n64_bridge_task(ctx), name="N64 Bridge")

        ctx.n64_sync_task = asyncio.create_task(n64_sync_task(ctx), name="N64 Sync")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.n64_sync_task:
            await ctx.n64_sync_task

    import colorama

    colorama.just_fix_windows_console()

    asyncio.run(main())
    colorama.deinit()
