import asyncio
import struct
import subprocess
import traceback
import typing

import settings

import Patch
import Utils
from CommonClient import ClientCommandProcessor, CommonContext, get_base_parser, gui_enabled, logger, server_loop
import dolphin_memory_engine as dolphin

try:
    from Utils import instance_name as apname
except ImportError:
    apname = "Archipelago"

from NetUtils import NetworkItem, ClientStatus
from .Data import location_gsw_info, location_to_unit
from .Items import items_by_id

RECEIVED_INDEX = 0x803DB860
RECEIVED_ITEM_ARRAY = 0x80001000
RECEIVED_LENGTH = 0x80000FFC
SEED = 0x80003210
GP_BASE = 0x803DAC18
GSWF_BASE = 0x178
GSW0 = 0x174
GSW_BASE = 0x578
ROOM = 0x803DF728
SHOP_POINTER = 0x8041EB60
SHOP_ITEM_OFFSET = 0x2F
SHOP_ITEM_PURCHASED = 0xD7

# GameCube disc header Game ID - used to verify DME is hooked to the correct process
GAME_ID_ADDRESS = 0x80000000
EXPECTED_GAME_ID = b"G8ME01"

def _check_universal_tracker_version() -> bool:
    import re
    if tracker_loaded:
        match = re.search(r"v\d+.(\d+).(\d+)", UT_VERSION)
        if len(match.groups()) < 2:
            return False
        if int(match.groups()[0]) < 2:
            return False
        if int(match.groups()[1]) < 12:
            return False
        return True
    return False

tracker_loaded = False
try:
    from worlds.tracker.TrackerClient import TrackerGameContext as cmmCtx, UT_VERSION
    tracker_loaded = True
except ModuleNotFoundError:
    from CommonClient import CommonContext as cmmCtx
    tracker_loaded = False

def validate_connection() -> bool:
    """Verify DME is hooked to TTYD by checking the GameCube disc Game ID in memory."""
    try:
        game_id = dolphin.read_bytes(GAME_ID_ADDRESS, 6)
        return game_id == EXPECTED_GAME_ID
    except Exception:
        return False

def read_string(address: int, length: int):
    try:
        return dolphin.read_bytes(address, length).decode().strip("\0")
    except Exception as e:
        logger.error(f"Error reading string from address {hex(address)}: {e}")
        return ""

def get_rom_item_id(item: NetworkItem):
    return items_by_id[item.item].rom_id

def _get_bit_address(bit_number: int) -> tuple:
    word_index = bit_number >> 5
    bit_position = bit_number & 0x1F
    word_address = GP_BASE + (word_index * 4) + GSWF_BASE
    byte_within_word = 3 - (bit_position >> 3)
    byte_address = word_address + byte_within_word
    bit = bit_position & 0x7
    return byte_address, bit

def gswf_set(bit_number: int):
    result = _get_bit_address(bit_number)
    if not result: return False
    byte_address, bit = result
    current_byte = dolphin.read_byte(byte_address)
    bit_mask = 1 << bit
    new_byte = current_byte | bit_mask
    dolphin.write_byte(byte_address, new_byte)
    return result

def gswf_check(bit_number: int) -> bool:
    result = _get_bit_address(bit_number)
    if not result: return False
    byte_address, bit = result
    current_byte = dolphin.read_byte(byte_address)
    bit_mask = 1 << bit
    return bool(current_byte & bit_mask)

def gsw_set(index, value):
    dolphin.write_word(GP_BASE + GSW0, value) if index == 0 else dolphin.write_byte(GP_BASE + index + GSW_BASE, value)

def gsw_check(index):
    return dolphin.read_word(GP_BASE + GSW0) if index == 0 else dolphin.read_byte(GP_BASE + index + GSW_BASE)


class TTYDCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: cmmCtx):
        super().__init__(ctx)

    def _cmd_set_gswf(self, bit_number: int):
        """Used to manually set a GSWF bit."""
        byte_address, bit = gswf_set(int(bit_number))
        logger.info(f"Bit {bit} written at {byte_address}")

    def _cmd_check_gswf(self, bit_number: int):
        """Used to manually check a GSWF bit."""
        result = gswf_check(int(bit_number))
        logger.info(f"GSWF Check: 0x{format(result, 'x')}")

    def _cmd_set_gsw(self, gsw: int, value: int):
        """Used to manually set a GSW flag."""
        gsw_set(int(gsw), int(value))

    def _cmd_check_gsw(self, gsw: int):
        """Used to manually check a GSW flag."""
        result = gsw_check(int(gsw))
        logger.info(f"GSWF Check: {result}")


class TTYDContext(cmmCtx):
    command_processor = TTYDCommandProcessor
    game = "Paper Mario: The Thousand-Year Door"
    tags = {"AP"}
    dolphin_connected: bool = False
    seed_verified: bool = False
    slot_data: dict | None = {}
    checked_locations = set()
    previous_room = None
    death_sent: bool = False

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.items_handling = 0b101

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(TTYDContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        super().on_package(cmd, args)
        if cmd in {"Connected"}:
            self.slot = args["slot"]
            self.slot_data = args["slot_data"]
            self.team = args["team"]
            if "death_link" in args["slot_data"]:
                Utils.async_start(self.update_death_link(bool(args["slot_data"]["death_link"])))
        elif cmd == "Retrieved":
            if "keys" not in args:
                logger.warning(f"invalid Retrieved packet to TTYDClient: {args}")
                return
        elif cmd == "RoomInfo":
            self.seed_name = args["seed_name"]

    def on_deathlink(self, data: typing.Dict[str, typing.Any]) -> None:
        super().on_deathlink(data)
        trigger_death(self)

    async def disconnect(self, allow_autoreconnect: bool = False):
        await super().disconnect()
        self.slot = None
        self.slot_data = None
        self.team = None
        self.checked_locations = set()
        self.seed_name = None
        self.seed_verified = False

    def make_gui(self) -> "type[kvui.GameManager]":
        from kvui import GameManager
        class TTYDManager(GameManager):
            logging_pairs = [("Client", "Archipelago")]
            base_title = f"{apname} TTYD Client"
        if not _check_universal_tracker_version():
            return TTYDManager
        class TrackerManager(super().make_gui()):
            logging_pairs = [("Client", "Archipelago")]
            base_title = f"{apname} TTYD Client with {UT_VERSION}"
        return TrackerManager

    async def receive_items(self):
        current_length = dolphin.read_word(RECEIVED_LENGTH)
        if current_length > 255:
            return  # Garbage data, skip
        if current_length > 0:
            return
        index = dolphin.read_word(RECEIVED_INDEX)
        if index > len(self.items_received):
            return  # Garbage data, skip
        items = min(len(self.items_received) - index, 255)
        if items <= 0:
            return
        item_ids = [get_rom_item_id(self.items_received[i]) for i in range(index, index + items)]
        packed_data = struct.pack(f'>{len(item_ids)}H', *item_ids)
        dolphin.write_bytes(RECEIVED_ITEM_ARRAY, packed_data)
        dolphin.write_word(RECEIVED_LENGTH, items)
        dolphin.write_word(RECEIVED_INDEX, index + items)


    async def check_ttyd_locations(self):
        locations_to_send = set()
        try:
            for location, gsw_info in location_gsw_info.items():
                gsw_type, offset, value = gsw_info
                if offset == 0:
                    continue
                if 78780850 <= location <= 78780973:
                    offset = 0x117A + location_to_unit[location][0]
                if gsw_type.value == 0:
                    if gsw_check(offset) >= value:
                        locations_to_send.add(location)
                elif gsw_type.value == 1:
                    if gswf_check(offset):
                        locations_to_send.add(location)
            if len(locations_to_send) > 0:
                self.checked_locations &= locations_to_send
                await self.send_msgs([{"cmd": 'LocationChecks', "locations": locations_to_send}])
        except Exception as e:
            logger.error(traceback.format_exc())

    async def check_death(self):
        death_byte = dolphin.read_byte(0x80003240)
        if death_byte > 1:
            return  # Garbage data, skip
        if death_byte == 1:
            dolphin.write_byte(0x80003240, 0)
            if not self.death_sent:
                await self.send_death(self.player_names[self.slot] + " had no life shrooms.")
            self.death_sent = False

    def save_loaded(self) -> bool:
        value = dolphin.read_byte(0x80003228)
        if value > 1:
            return False  # Garbage data
        return value > 0


async def _run_game(rom: str):
    import os
    auto_start = settings.get_settings().ttyd_options.rom_start

    if auto_start is True:
        dolphin_path = settings.get_settings().ttyd_options.dolphin_path
        subprocess.Popen(
            [
                dolphin_path,
                f"--exec={os.path.realpath(rom)}",
            ],
            cwd=Utils.local_path("."),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

async def _patch_and_run_game(patch_file: str):
    metadata, output_file = Patch.create_rom_file(patch_file)
    Utils.async_start(_run_game(output_file))
    return metadata


# Sends player items from server
# Checks for player status to see if they are in/loading a level
# Checks location status inside of levels
async def ttyd_sync_task(ctx: TTYDContext):
    logger.info("Starting Dolphin connector...")
    while not ctx.exit_event.is_set():
        if dolphin.is_hooked() and ctx.dolphin_connected:
            if ctx.slot:
                try:
                    if not validate_connection():
                        logger.info("TTYD is no longer running. Disconnecting from Dolphin.")
                        dolphin.un_hook()
                        ctx.dolphin_connected = False
                        ctx.seed_verified = False
                        await asyncio.sleep(3)
                        continue
                    if not ctx.seed_verified:
                        logger.info("Checking ROM seed...")
                        seed = read_string(SEED, 0x10)
                        if seed not in ctx.seed_name:
                            await ctx.disconnect()
                            logger.info("ROM Seed does not match Room seed. Please make sure you are using the correct patch.")
                            dolphin.un_hook()
                            await asyncio.sleep(3)
                            continue
                        ctx.seed_verified = True
                        logger.info("ROM Seed verified successfully.")
                    if "DeathLink" in ctx.tags:
                        await ctx.check_death()
                    if not ctx.save_loaded():
                        await asyncio.sleep(0.5)
                        continue
                    current_room = read_string(ROOM, 6)
                    if ctx.previous_room != current_room:
                        ctx.previous_room = current_room
                        await ctx.send_msgs([{
                            "cmd": "Set",
                            "key": f"ttyd_room_{ctx.team}_{ctx.slot}",
                            "default": 0,
                            "want_reply": False,
                            "operations": [{"operation": "replace", "value": current_room}]
                        }])
                    await ctx.receive_items()
                    await ctx.check_ttyd_locations()
                    goal = ctx.slot_data.get("goal", 0)
                    if goal == 1: # Shadow Queen
                        if not ctx.finished_game and gsw_check(1708) >= 18:
                            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                    elif goal == 2: # Crystal Stars
                        star_count = dolphin.read_byte(0x8000323B)
                        if not ctx.finished_game and star_count <= 7 and star_count >= ctx.slot_data["goal_stars"]:
                            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                    else:
                        if not ctx.finished_game and gswf_check(5085):
                            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                    await asyncio.sleep(.5)
                except Exception as e:
                    logger.info(traceback.format_exc())
                    dolphin.un_hook()
                    ctx.dolphin_connected = False
                    await asyncio.sleep(1)
            else:
                await asyncio.sleep(1)
        else:
            try:
                logger.info("Attempting to connect to Dolphin...")
                dolphin.hook()
                if not dolphin.is_hooked():
                    logger.info("Connection to Dolphin failed... Attempting again")
                    ctx.dolphin_connected = False
                    await ctx.disconnect()
                    await asyncio.sleep(3)
                    continue
                if not validate_connection():
                    logger.info("Dolphin hooked but TTYD is not running. "
                                "Please load Paper Mario: The Thousand-Year Door.")
                    dolphin.un_hook()
                    ctx.dolphin_connected = False
                    await asyncio.sleep(5)
                    continue
                logger.info("Dolphin connected successfully.")
                ctx.dolphin_connected = True
            except Exception as e:
                dolphin.un_hook()
                logger.info("Connection to Dolphin failed... Attempting again")
                logger.error(traceback.format_exc())
                ctx.dolphin_connected = False
                await ctx.disconnect()
                await asyncio.sleep(3)
                continue

def trigger_death(ctx: TTYDContext):
    if ctx.slot is not None and dolphin.is_hooked() and ctx.dolphin_connected and validate_connection():
        ctx.death_sent = True
        dolphin.write_byte(0x8000323F, 1)


def launch(*args):
    async def main(args):
        if args.patch_file:
            await asyncio.create_task(_patch_and_run_game(args.patch_file))
        ctx = TTYDContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
        if gui_enabled:
            if tracker_loaded:  # UT Connection
                ctx.run_generator()
            ctx.run_gui()
        ctx.run_cli()
        ctx.gl_sync_task = asyncio.create_task(ttyd_sync_task(ctx), name="Gauntlet Legends Sync Task")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

    parser = get_base_parser()
    parser.add_argument("patch_file", default="", type=str, nargs="?", help="Path to an APTTYD file")
    args = parser.parse_args(args)

    import colorama

    colorama.just_fix_windows_console()
    asyncio.run(main(args))
    colorama.deinit()
