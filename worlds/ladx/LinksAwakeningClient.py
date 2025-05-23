import ModuleUpdate
ModuleUpdate.update()

import Utils
apname = Utils.instance_name if Utils.instance_name else "Archipelago"

import asyncio
import base64
import binascii
import colorama
import io
import os
import re
import select
import shlex
import socket
import struct
import sys
import subprocess
import time
import typing


from CommonClient import (CommonContext, ClientCommandProcessor, get_base_parser, gui_enabled, logger,
                          server_loop)
from NetUtils import ClientStatus
from . import Common
from .GpsTracker import GpsTracker
from .ItemTracker import ItemTracker
from .Items import links_awakening_items
from .Locations import links_awakening_location_meta_to_id
from .Tracker import LocationTracker, MagpieBridge
from .TrackerConsts import storage_key

links_awakening_location_id_to_meta = {v:k for k,v in links_awakening_location_meta_to_id.items()}

class GameboyException(Exception):
    pass


class RetroArchDisconnectError(GameboyException):
    pass


class InvalidEmulatorStateError(GameboyException):
    pass


class BadRetroArchResponse(GameboyException):
    pass


def magpie_logo():
    from kivy.uix.image import CoreImage
    binary_data = """
iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAAAXN
SR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA
7DAcdvqGQAAADGSURBVDhPhVLBEcIwDHOYhjHCBuXHj2OTbAL8+
MEGZIxOQ1CinOOk0Op0bmo7tlXXeR9FJMYDLOD9mwcLjQK7+hSZ
wgcWMZJOAGeGKtChNHFL0j+FZD3jSCuo0w7l03wDrWdg00C4/aW
eDEYNenuzPOfPspBnxf0kssE80vN0L8361j10P03DK4x6FHabuV
ear8fHme+b17rwSjbAXeUMLb+EVTV2QHm46MWQanmnydA98KsVS
XkV+qFpGQXrLhT/fqraQeQLuplpNH5g+WkAAAAASUVORK5CYII="""
    binary_data = base64.b64decode(binary_data)
    data = io.BytesIO(binary_data)
    return CoreImage(data, ext="png").texture


class LAClientConstants:
    # Connector version
    VERSION = 0x01
    #
    # Memory locations of LADXR
    ROMGameID = 0x0051  # 4 bytes
    SlotName = 0x0134
    # Unused
    # ROMWorldID = 0x0055
    # ROMConnectorVersion = 0x0056
    wTradeSequenceItem1 = 0xDB40
    wTradeSequenceItem2 = 0xDB7F
    wLinkHealth = 0xDB5A
    wAddHealthBuffer = 0xDB93
    wSubtractHealthBuffer = 0xDB94
    # RO: We should only act if this is higher then 6, as it indicates that the game is running normally
    wGameplayType = 0xDB95
    # RO: Starts at 0, increases every time an item is received from the server and processed
    wLinkSyncSequenceNumber = 0xDDF6
    wLinkStatusBits = 0xDDF7          # RW:
    #      Bit0: wLinkGive* contains valid data, set from script cleared from ROM.
    wLinkGiveItem = 0xDDF8  # RW
    wLinkGiveItemFrom = 0xDDF9  # RW
    # All of these six bytes are unused, we can repurpose
    # wLinkSendItemRoomHigh = 0xDDFA  # RO
    # wLinkSendItemRoomLow = 0xDDFB  # RO
    # wLinkSendItemTarget = 0xDDFC  # RO
    # wLinkSendItemItem = 0xDDFD  # RO
    # wLinkSendShopItem = 0xDDFE # RO, which item to send (1 based, order of the shop items)
    # RO, which player to send to, but it's just the X position of the NPC used, so 0x18 is player 0
    # wLinkSendShopTarget = 0xDDFF


    wRecvIndex = 0xDDFD # Two bytes
    wCheckAddress = 0xC0FF - 0x4
    WRamCheckSize = 0x4
    WRamSafetyValue = bytearray([0]*WRamCheckSize)

    wRamStart = 0xC000
    hRamStart = 0xFF80
    hRamSize = 0x80

    MinGameplayValue = 0x06
    MaxGameplayValue = 0x1A
    VictoryGameplayAndSub = 0x0102

class RAGameboy():
    cache = []
    last_cache_read = None
    socket = None

    def __init__(self, address, port) -> None:
        self.cache_start = LAClientConstants.wRamStart
        self.cache_size = LAClientConstants.hRamStart + LAClientConstants.hRamSize - LAClientConstants.wRamStart

        self.address = address
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        assert (self.socket)
        self.socket.setblocking(False)

    async def send_command(self, command, timeout=1.0):
        self.send(f'{command}\n')
        response_str = await self.async_recv()
        self.check_command_response(command, response_str)
        return response_str.rstrip()

    async def get_retroarch_version(self):
        return await self.send_command("VERSION")

    async def get_retroarch_status(self):
        return await self.send_command("GET_STATUS")

    def set_checks_range(self, checks_start, checks_size):
        self.checks_start = checks_start
        self.checks_size = checks_size

    def set_location_range(self, location_start, location_size, critical_addresses):
        self.location_start = location_start
        self.location_size = location_size
        self.critical_location_addresses = critical_addresses

    def send(self, b):
        if type(b) is str:
            b = b.encode('ascii')
        self.socket.sendto(b, (self.address, self.port))

    def recv(self):
        select.select([self.socket], [], [])
        response, _ = self.socket.recvfrom(4096)
        return response

    async def async_recv(self, timeout=1.0):
        response = await asyncio.wait_for(asyncio.get_event_loop().sock_recv(self.socket, 4096), timeout)
        return response

    async def check_safe_gameplay(self, throw=True):
        async def check_wram():
            check_values = await self.async_read_memory(LAClientConstants.wCheckAddress, LAClientConstants.WRamCheckSize)

            if check_values != LAClientConstants.WRamSafetyValue:
                if throw:
                    raise InvalidEmulatorStateError()
                return False
            return True

        if not await check_wram():
            if throw:
                raise InvalidEmulatorStateError()
            return False

        gameplay_value = await self.async_read_memory(LAClientConstants.wGameplayType)
        gameplay_value = gameplay_value[0]
        # In gameplay or credits
        if not (LAClientConstants.MinGameplayValue <= gameplay_value <= LAClientConstants.MaxGameplayValue) and gameplay_value != 0x1:
            if throw:
                logger.info("invalid emu state")
                raise InvalidEmulatorStateError()
            return False
        if not await check_wram():
            if throw:
                raise InvalidEmulatorStateError()
            return False
        return True

    # We're sadly unable to update the whole cache at once
    # as RetroArch only gives back some number of bytes at a time
    # So instead read as big as chunks at a time as we can manage
    async def update_cache(self):
        # First read the safety address - if it's invalid, bail
        self.cache = []

        if not await self.check_safe_gameplay():
            return False

        attempts = 0
        while True:
            # RA doesn't let us do an atomic read of a large enough block of RAM
            # Some bytes can't change in between reading location_block and hram_block
            location_block = await self.read_memory_block(self.location_start, self.location_size)
            hram_block = await self.read_memory_block(LAClientConstants.hRamStart, LAClientConstants.hRamSize)
            verification_block = await self.read_memory_block(self.location_start, self.location_size)

            valid = True
            for address in self.critical_location_addresses:
                if location_block[address - self.location_start] != verification_block[address - self.location_start]:
                    valid = False

            if valid:
                break

            attempts += 1

            # Shouldn't really happen, but keep it from choking
            if attempts > 5:
                return False

        checks_block = await self.read_memory_block(self.checks_start, self.checks_size)

        if not await self.check_safe_gameplay():
            return False

        self.cache = bytearray(self.cache_size)

        start = self.checks_start - self.cache_start
        self.cache[start:start + len(checks_block)] = checks_block

        start = self.location_start - self.cache_start
        self.cache[start:start + len(location_block)] = location_block

        start = LAClientConstants.hRamStart - self.cache_start
        self.cache[start:start + len(hram_block)] = hram_block

        self.last_cache_read = time.time()
        return True

    async def read_memory_block(self, address: int, size: int):
        block = bytearray()
        remaining_size = size
        while remaining_size:
            chunk = await self.async_read_memory(address + len(block), remaining_size)
            remaining_size -= len(chunk)
            block += chunk
        return block

    async def read_memory_cache(self, addresses):
        if not self.last_cache_read or self.last_cache_read + 0.1 < time.time():
            await self.update_cache()
        if not self.cache:
            return None
        assert (len(self.cache) == self.cache_size)
        for address in addresses:
            assert self.cache_start <= address <= self.cache_start + self.cache_size
        r = {address: self.cache[address - self.cache_start]
             for address in addresses}
        return r

    async def async_read_memory_safe(self, address, size=1):
        # whenever we do a read for a check, we need to make sure that we aren't reading
        # garbage memory values - we also need to protect against reading a value, then the emulator resetting
        #
        # ...actually, we probably _only_ need the post check

        # Check before read
        if not await self.check_safe_gameplay():
            return None

        # Do read
        r = await self.async_read_memory(address, size)

        # Check after read
        if not await self.check_safe_gameplay():
            return None

        return r

    def check_command_response(self, command: str, response: bytes):
        if command == "VERSION":
            ok = re.match(r"\d+\.\d+\.\d+", response.decode('ascii')) is not None
        else:
            ok = response.startswith(command.encode())
        if not ok:
            logger.warning(f"Bad response to command {command} - {response}")
            raise BadRetroArchResponse()

    def read_memory(self, address, size=1):
        command = "READ_CORE_MEMORY"

        self.send(f'{command} {hex(address)} {size}\n')
        response = self.recv()

        self.check_command_response(command, response)

        splits = response.decode().split(" ", 2)
        # Ignore the address for now
        if splits[2][:2] == "-1":
            raise BadRetroArchResponse()

        # TODO: check response address, check hex behavior between RA and BH

        return bytearray.fromhex(splits[2])

    async def async_read_memory(self, address, size=1):
        command = "READ_CORE_MEMORY"

        self.send(f'{command} {hex(address)} {size}\n')
        response = await self.async_recv()
        self.check_command_response(command, response)
        response = response[:-1]
        splits = response.decode().split(" ", 2)
        try:
            response_addr = int(splits[1], 16)
        except ValueError:
            raise BadRetroArchResponse()

        if response_addr != address:
            raise BadRetroArchResponse()

        ret = bytearray.fromhex(splits[2])
        if len(ret) > size:
            raise BadRetroArchResponse()
        return ret

    def write_memory(self, address, bytes):
        command = "WRITE_CORE_MEMORY"

        self.send(f'{command} {hex(address)} {" ".join(hex(b) for b in bytes)}')
        select.select([self.socket], [], [])
        response, _ = self.socket.recvfrom(4096)
        self.check_command_response(command, response)
        splits = response.decode().split(" ", 3)

        assert (splits[0] == command)

        if splits[2] == "-1":
            logger.info(splits[3])


class LinksAwakeningClient():
    socket = None
    gameboy = None
    tracker = None
    auth = None
    game_crc = None
    collect_enabled = True
    deathlink_status = None
    queue_trade_item_fix = False
    retroarch_address = None
    retroarch_port = None
    gameboy = None

    def msg(self, m):
        logger.info(m)
        s = f"SHOW_MSG {m}\n"
        self.gameboy.send(s)

    def __init__(self, retroarch_address="127.0.0.1", retroarch_port=55355):
        self.retroarch_address = retroarch_address
        self.retroarch_port = retroarch_port
        pass

    stop_bizhawk_spam = False
    async def wait_for_retroarch_connection(self):
        if not self.stop_bizhawk_spam:
            logger.info("Waiting on connection to Retroarch...")
            self.stop_bizhawk_spam = True
        self.gameboy = RAGameboy(self.retroarch_address, self.retroarch_port)

        while True:
            try:
                version = await self.gameboy.get_retroarch_version()
                NO_CONTENT = b"GET_STATUS CONTENTLESS"
                status = NO_CONTENT
                core_type = None
                GAME_BOY = b"game_boy"
                while status == NO_CONTENT or core_type != GAME_BOY:
                    status = await self.gameboy.get_retroarch_status()
                    if status.count(b" ") < 2:
                        await asyncio.sleep(1.0)
                        continue
                    GET_STATUS, PLAYING, info = status.split(b" ", 2)
                    if status.count(b",") < 2:
                        await asyncio.sleep(1.0)
                        continue
                    core_type, rom_name, self.game_crc = info.split(b",", 2)
                    if core_type != GAME_BOY:
                        logger.info(
                            f"Core type should be '{GAME_BOY}', found {core_type} instead - wrong type of ROM?")
                        await asyncio.sleep(1.0)
                        continue
                self.stop_bizhawk_spam = False
                logger.info(f"Connected to Retroarch {version.decode('ascii', errors='replace')} "
                            f"running {rom_name.decode('ascii', errors='replace')}")
                return
            except (BlockingIOError, TimeoutError, ConnectionResetError):
                await asyncio.sleep(1.0)
                pass

    async def reset_auth(self):
        auth = binascii.hexlify(await self.gameboy.async_read_memory(0x0134, 12)).decode()
        self.auth = auth

    async def wait_and_init_tracker(self, magpie: MagpieBridge):
        await self.wait_for_game_ready()
        self.tracker = LocationTracker(self.gameboy)
        self.item_tracker = ItemTracker(self.gameboy)
        self.gps_tracker = GpsTracker(self.gameboy)
        magpie.gps_tracker = self.gps_tracker

    async def give_item(self, item):
        # Spin until we either:
        # get an exception from a bad read (emu shut down or reset)
        # beat the game
        # the client handles the last pending item
        status = (await self.gameboy.async_read_memory_safe(LAClientConstants.wLinkStatusBits))[0]
        while not (await self.is_victory()) and status & 1 == 1:
            time.sleep(0.1)
            status = (await self.gameboy.async_read_memory_safe(LAClientConstants.wLinkStatusBits))[0]

        item_id = item.item - Common.BASE_ID
        # The player name table only goes up to 100, so don't go past that
        # Even if it didn't, the remote player _index_ byte is just a byte, so 255 max
        from_player = item.player
        if from_player > 100:
            from_player = 100

        self.gameboy.write_memory(LAClientConstants.wLinkGiveItem, [item_id, from_player])
        status |= 1
        status = self.gameboy.write_memory(LAClientConstants.wLinkStatusBits, [status])

    async def recved_item_from_ap(self, ctx, item, next_index):
        if item.location <= 0 or item.player != ctx.slot: # items from server or other slots
            await self.give_item(item)
        next_index += 1
        self.gameboy.write_memory(LAClientConstants.wRecvIndex, struct.pack(">H", next_index))

    # The key location is blocked from collection unless the value location
    # has also been checked.
    dependent_location_meta_ids = {
        "0x301-0": "0x301-1", # Tunic Fairy Item 1 -> Tunic Fairy Item 2
        "0x301-1": "0x301-0", # Tunic Fairy Item 2 -> Tunic Fairy Item 1
        "0x106": "0x102",     # Moldorm Heart Container -> Full Moon Cello
        "0x12B": "0x12A",     # Genie Heart Container -> Conch Horn
        "0x15A": "0x159",     # Slime Eye Heart Container -> Sea Lily's Bell
        "0x166": "0x162",     # Angler Fish Heart Container -> Surf Harp
        "0x185": "0x182",     # Slime Eel Heart Container -> Wind Marimba
        "0x1BC": "0x1B5",     # Facade Heart Container -> Coral Triangle
        "0x223": "0x22C",     # Evil Eagle Heart Container -> Organ of Evening Calm
        "0x234": "0x230",     # Hot Head Heart Container -> Thunder Drum
    }
    dependent_location_ids = {
        links_awakening_location_meta_to_id[k]: links_awakening_location_meta_to_id[v]
        for k, v in dependent_location_meta_ids.items()}

    async def collect(self, ctx):
        if not self.gps_tracker.room or self.gps_tracker.is_transitioning:
            return
        unhandled_locations = ctx.checked_locations - ctx.handled_locations
        for id, dep in self.dependent_location_ids.items():
            if id in unhandled_locations and dep not in ctx.checked_locations:
                unhandled_locations.remove(id)
        current_room = '0x' + hex(self.gps_tracker.room)[2:].zfill(3).upper()
        for id in unhandled_locations:
            meta_id = links_awakening_location_id_to_meta[id]
            is_checked = next(x for x in self.tracker.all_checks if x.id == meta_id).value
            if(is_checked):
                ctx.handled_locations.add(id)
                continue
            if(current_room == meta_id[:5]):
                continue
            check = self.tracker.meta_to_check[meta_id]
            did_collect = await self.collect_check(check)
            ctx.handled_locations.add(id)
            if did_collect:
                self.queue_trade_item_fix = True
                our_item = next((x for x in ctx.recvd_checks.values() if x.location == id), None)
                if our_item:
                    await self.give_item(our_item)
            break # one per cycle

    async def collect_check(self, check):
        current_value = int.from_bytes(await self.gameboy.async_read_memory(check.address), 'big')
        already_collected = bool(current_value & check.mask)
        if not already_collected:
            new_value = current_value | check.mask
            self.gameboy.write_memory(check.address, [new_value])
        return not already_collected

    trade_items = {
        "TRADING_ITEM_YOSHI_DOLL": "0x2A6-Trade",
        "TRADING_ITEM_RIBBON": "0x2B2-Trade",
        "TRADING_ITEM_DOG_FOOD": "0x2FE-Trade",
        "TRADING_ITEM_BANANAS": "0x07B-Trade",
        "TRADING_ITEM_STICK": "0x087-Trade",
        "TRADING_ITEM_HONEYCOMB": "0x2D7-Trade",
        "TRADING_ITEM_PINEAPPLE": "0x019-Trade",
        "TRADING_ITEM_HIBISCUS": "0x2D9-Trade",
        "TRADING_ITEM_LETTER": "0x2A8-Trade",
        "TRADING_ITEM_BROOM": "0x0CD-Trade",
        "TRADING_ITEM_FISHING_HOOK": "0x2F5-Trade",
        "TRADING_ITEM_NECKLACE": "0x0C9-Trade",
        "TRADING_ITEM_SCALE": "0x297-Trade",
        "TRADING_ITEM_MAGNIFYING_GLASS": None,
    }
    async def fix_trade_items(self, recvd_checks):
        expected_trade_items = []
        held_trade_items = []
        for item, location in self.trade_items.items():
            item_id = next(x.item_id for x in links_awakening_items
                           if x.ladxr_id == item) + Common.BASE_ID
            item_received = next((x for x in recvd_checks.values()
                                  if x.item == item_id), False)
            all_checks = [x for x in self.tracker.all_checks if x.id == location]
            remaining_checks = [x for x in self.tracker.remaining_checks if x.id == location]
            destination_checked = location and (not remaining_checks or (len(remaining_checks) < len(all_checks)))
            expected_trade_items.append(int(item_received and not destination_checked))

            inventory = self.item_tracker.itemDict[item].value
            if item in self.item_tracker.extraItems:
                inventory -= self.item_tracker.extraItems[item]
            held_trade_items.append(inventory)
        if expected_trade_items != held_trade_items:
            trade1 = 0
            for i, x in enumerate(expected_trade_items[:8]):
                trade1 += x << i
            trade2 = 0
            for i, x in enumerate(expected_trade_items[8:]):
                trade2 += x << i
            self.gameboy.write_memory(LAClientConstants.wTradeSequenceItem1, [trade1])
            self.gameboy.write_memory(LAClientConstants.wTradeSequenceItem2, [trade2])


    should_reset_auth = False
    async def wait_for_game_ready(self):
        logger.info("Waiting on game to be in valid state...")
        while not await self.gameboy.check_safe_gameplay(throw=False):
            if self.should_reset_auth:
                self.should_reset_auth = False
                raise GameboyException("Resetting due to wrong archipelago server")
        logger.info("Game connection ready!")

    async def is_victory(self):
        return (await self.gameboy.read_memory_cache([LAClientConstants.wGameplayType]))[LAClientConstants.wGameplayType] == 1

    async def main_tick(self, ctx, item_get_cb, win_cb, deathlink_cb):
        cache_is_fresh = await self.gameboy.update_cache()
        await self.tracker.readChecks(item_get_cb)
        await self.item_tracker.readItems()
        await self.gps_tracker.read_location()
        await self.gps_tracker.read_entrances()

        if not ctx.slot or not self.tracker.has_start_item():
            return

        # fix trade items during transitions when inventory is stable
        if self.queue_trade_item_fix and cache_is_fresh and self.gps_tracker.is_transitioning:
            await self.fix_trade_items(ctx.recvd_checks)
            self.queue_trade_item_fix = False
            return

        if await self.is_victory():
            await win_cb()

        current_health = (await self.gameboy.read_memory_cache([LAClientConstants.wLinkHealth]))[LAClientConstants.wLinkHealth]
        health_to_remove = (await self.gameboy.read_memory_cache([LAClientConstants.wSubtractHealthBuffer]))[LAClientConstants.wSubtractHealthBuffer]

        if self.deathlink_status == 'pending':
            self.gameboy.write_memory(LAClientConstants.wAddHealthBuffer, [0]) # Stop any health gain
            self.gameboy.write_memory(LAClientConstants.wLinkHealth, [1]) #  Almost dead
            self.gameboy.write_memory(LAClientConstants.wSubtractHealthBuffer, [1]) # Deal remaining damage this way to trigger medicine
            self.deathlink_status = 'in_progress'
            return
        elif self.deathlink_status == 'in_progress':
            if not current_health: # Died from deathlink
                self.deathlink_status = 'complete'
                self.queue_trade_item_fix = True
            elif not health_to_remove: # Survived deathlink (medicine)
                self.deathlink_status = None
            return
        elif not self.deathlink_status and not current_health: # Died naturally
            await deathlink_cb()
            self.deathlink_status = 'complete'
        elif self.deathlink_status == 'complete' and current_health:
            self.deathlink_status = None

        # receive items
        recv_index = struct.unpack(">H", await self.gameboy.async_read_memory(LAClientConstants.wRecvIndex, 2))[0]
        if recv_index in ctx.recvd_checks:
            item = ctx.recvd_checks[recv_index]
            await self.recved_item_from_ap(ctx, item, recv_index)
            return

        # collect
        if self.collect_enabled and cache_is_fresh:
            await self.collect(ctx)

all_tasks = set()

def create_task_log_exception(awaitable) -> asyncio.Task:
    async def _log_exception(awaitable):
        try:
            return await awaitable
        except Exception as e:
            logger.exception(e)
            pass
        finally:
            all_tasks.remove(task)
    task = asyncio.create_task(_log_exception(awaitable))
    all_tasks.add(task)

class LinksAwakeningCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx):
        super().__init__(ctx)

    def _cmd_fix_trade_items(self):
        """Forces fix of trade items. Ideally you should never need to trigger this manually."""
        if isinstance(self.ctx, LinksAwakeningContext):
            self.ctx.client.queue_trade_item_fix = True

    def _cmd_toggle_collect(self):
        """Toggles collect."""
        if isinstance(self.ctx, LinksAwakeningContext):
            self.ctx.client.collect_enabled = not self.ctx.client.collect_enabled
            if self.ctx.client.collect_enabled:
                logger.info("Collect enabled")
            else:
                logger.info("Collect disabled")

    def _cmd_deathlink(self):
        """Toggles deathlink."""
        if isinstance(self.ctx, LinksAwakeningContext):
            Utils.async_start(self.ctx.update_death_link("DeathLink" not in self.ctx.tags))

    def _cmd_die(self):
        """Die."""
        if isinstance(self.ctx, LinksAwakeningContext):
            self.ctx.client.deathlink_status = 'pending'

class LinksAwakeningContext(CommonContext):
    tags = {"AP"}
    game = Common.LINKS_AWAKENING
    command_processor = LinksAwakeningCommandProcessor
    items_handling = 0b111
    want_slot_data = True
    la_task = None
    client = None
    # TODO: does this need to re-read on reset?
    found_checks = set()
    handled_locations = set()
    recvd_checks = {}
    last_resend = time.time()

    magpie_enabled = False
    magpie = None
    magpie_task = None
    won = False

    @property
    def slot_storage_key(self):
        return f"{self.slot_info[self.slot].name}_{storage_key}"

    def __init__(self, server_address: typing.Optional[str], password: typing.Optional[str], magpie: typing.Optional[bool]) -> None:
        self.client = LinksAwakeningClient()
        self.slot_data = {}

        if magpie:
            self.magpie_enabled = True
            self.magpie = MagpieBridge()
        super().__init__(server_address, password)

    def run_gui(self) -> None:
        import webbrowser
        from kvui import GameManager, ImageButton
        from kivy.clock import Clock,mainthread

        class LADXManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago"),
                ("Tracker", "Tracker"),
            ]
            base_title = f"{apname} {Common.LINKS_AWAKENING} Client"

            @mainthread
            def open_magpie(self, *args):
                try:
                    webbrowser.open('https://magpietracker.us/?enable_autotracker=1')
                except Exception as e:
                    logging.exception("Failed to open browser: %s", e)

            def build(self):
                b = super().build()

                if self.ctx.magpie_enabled:
                    button = ImageButton(texture=magpie_logo(), fit_mode="cover", size=(30,30), image_size=(30, 30), size_hint_x=None)

                    button.pos_hint = {'center_y': 0.5}
                    
                    button.bind(on_press=lambda _: Clock.schedule_once(self.open_magpie, 0))
                    self.connect_layout.add_widget(button)
                return b

        self.ui = LADXManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    async def send_new_entrances(self, entrances: typing.Dict[str, str]):
        # Store the entrances we find on the server for future sessions
        message = [{
            "cmd": "Set",
            "key": self.slot_storage_key,
            "default": {},
            "want_reply": False,
            "operations": [{"operation": "update", "value": entrances}],
        }]

    async def send_new_entrances(self, entrances: typing.Dict[str, str]):
        # Store the entrances we find on the server for future sessions
        message = [{
            "cmd": "Set",
            "key": self.slot_storage_key,
            "default": {},
            "want_reply": False,
            "operations": [{"operation": "update", "value": entrances}],
        }]
        await self.send_msgs(message)

    had_invalid_slot_data = None
    def event_invalid_slot(self):
        # The next time we try to connect, reset the game loop for new auth
        self.had_invalid_slot_data = True
        self.auth = None
        # Don't try to autoreconnect, it will just fail
        self.disconnected_intentionally = True
        CommonContext.event_invalid_slot(self)

    async def send_deathlink(self):
        if "DeathLink" in self.tags:
            logger.info("DeathLink: Sending death to your friends...")
            self.last_death_link = time.time()
            await self.send_msgs([{
                "cmd": "Bounce", "tags": ["DeathLink"],
                "data": {
                    "time": self.last_death_link,
                    "source": self.slot_info[self.slot].name,
                    "cause": self.slot_info[self.slot].name + " had a nightmare."
                }
            }])

    async def send_victory(self):
        if not self.won:
            message = [{"cmd": "StatusUpdate",
                        "status": ClientStatus.CLIENT_GOAL}]
            logger.info("victory!")
            await self.send_msgs(message)
            self.won = True

    async def request_found_entrances(self):
        await self.send_msgs([{"cmd": "Get", "keys": [self.slot_storage_key]}])

        # Ask for updates so that players can co-op entrances in a seed
        await self.send_msgs([{"cmd": "SetNotify", "keys": [self.slot_storage_key]}])

    async def request_found_entrances(self):
        await self.send_msgs([{"cmd": "Get", "keys": [self.slot_storage_key]}])

        # Ask for updates so that players can co-op entrances in a seed
        await self.send_msgs([{"cmd": "SetNotify", "keys": [self.slot_storage_key]}])

    def on_deathlink(self, data: typing.Dict[str, typing.Any]) -> None:
        self.client.deathlink_status = 'pending'
        super(LinksAwakeningContext, self).on_deathlink(data)

    def new_checks(self, item_ids, ladxr_ids):
        self.found_checks.update(item_ids)
        create_task_log_exception(self.check_locations(self.found_checks))
        if self.magpie_enabled:
            create_task_log_exception(self.magpie.send_new_checks(ladxr_ids))

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(LinksAwakeningContext, self).server_auth(password_requested)

        if self.had_invalid_slot_data:
            # We are connecting when previously we had the wrong ROM or server - just in case
            # re-read the ROM so that if the user had the correct address but wrong ROM, we
            # allow a successful reconnect
            self.client.should_reset_auth = True
            self.had_invalid_slot_data = False

        while self.client.auth == None:
            await asyncio.sleep(0.1)

            # Just return if we're closing
            if self.exit_event.is_set():
                return
        self.auth = self.client.auth
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            self.game = self.slot_info[self.slot].game
            self.slot_data = args.get("slot_data", {})
            # This is sent to magpie over local websocket to make its own connection
            self.slot_data.update({
                "server_address": self.server_address,
                "slot_name": self.player_names[self.slot],
                "password": self.password,
                "client_version": Common.VERSION,
            })
            if self.slot_data.get("death_link"):
                Utils.async_start(self.update_death_link(True))

            # We can process linked items on already-checked checks now that we have slot_data
            if self.client.tracker:
                checked_checks = set(self.client.tracker.all_checks) - set(self.client.tracker.remaining_checks)
                self.add_linked_items(checked_checks)

        # TODO - use watcher_event
        if cmd == "ReceivedItems":
            for index, item in enumerate(args["items"], start=args["index"]):
                self.recvd_checks[index] = item

        if cmd == "Retrieved" and self.magpie_enabled and self.slot_storage_key in args["keys"]:
            self.client.gps_tracker.receive_found_entrances(args["keys"][self.slot_storage_key])

        if cmd == "SetReply" and self.magpie_enabled and args["key"] == self.slot_storage_key:
            self.client.gps_tracker.receive_found_entrances(args["value"])

    async def sync(self):
        sync_msg = [{'cmd': 'Sync'}]
        await self.send_msgs(sync_msg)

    async def run_game_loop(self):
        def on_item_get(ladxr_checks):
            checks = [links_awakening_location_meta_to_id[check.id] for check in ladxr_checks]
            self.new_checks(checks, [check.id for check in ladxr_checks])

            self.add_linked_items(ladxr_checks)

        async def victory():
            await self.send_victory()

        async def deathlink():
            await self.send_deathlink()

        if self.magpie_enabled:
            self.magpie_task = asyncio.create_task(self.magpie.serve())

        # yield to allow UI to start
        await asyncio.sleep(0)

        while True:
            try:
                # TODO: cancel all client tasks
                if not self.client.stop_bizhawk_spam:
                    logger.info("(Re)Starting game loop")
                self.found_checks.clear()
                self.handled_locations.clear()
                # On restart of game loop, clear all checks, just in case we swapped ROMs
                # this isn't totally neccessary, but is extra safety against cross-ROM contamination
                self.recvd_checks.clear()
                await self.client.wait_for_retroarch_connection()
                await self.client.reset_auth()
                # If we find ourselves with new auth after the reset, reconnect
                if self.auth and self.client.auth != self.auth:
                    # It would be neat to reconnect here, but connection needs this loop to be running
                    logger.info("Detected new ROM, disconnecting...")
                    await self.disconnect()
                    continue

                if not self.recvd_checks:
                    await self.sync()

                await self.client.wait_and_init_tracker(self.magpie)

                min_tick_duration = 0.1
                last_tick = time.time()
                while True:
                    await self.client.main_tick(self, on_item_get, victory, deathlink)

                    now = time.time()
                    tick_duration = now - last_tick
                    sleep_duration = max(min_tick_duration - tick_duration, 0)
                    await asyncio.sleep(sleep_duration)

                    last_tick = now

                    if self.last_resend + 5.0 < now:
                        self.last_resend = now
                        await self.check_locations(self.found_checks)
                    if self.magpie_enabled:
                        try:
                            self.magpie.set_checks(self.client.tracker.all_checks)
                            await self.magpie.set_item_tracker(self.client.item_tracker)
                            if self.slot_data and "slot_data" in self.magpie.features and not self.magpie.has_sent_slot_data:
                                self.magpie.slot_data = self.slot_data
                                await self.magpie.send_slot_data()

                            if self.client.gps_tracker.needs_found_entrances:
                                await self.request_found_entrances()
                                self.client.gps_tracker.needs_found_entrances = False

                            new_entrances = await self.magpie.send_gps()
                            if new_entrances:
                                await self.send_new_entrances(new_entrances)
                        except Exception:
                            # Don't let magpie errors take out the client
                            pass
                    if self.client.should_reset_auth:
                        self.client.should_reset_auth = False
                        raise GameboyException("Resetting due to wrong archipelago server")
            except (GameboyException, asyncio.TimeoutError, TimeoutError, ConnectionResetError):
                await asyncio.sleep(1.0)

def run_game(romfile: str) -> None:
    auto_start = typing.cast(typing.Union[bool, str],
                            Utils.get_options()["ladx_beta_options"].get("rom_start", True))
    if auto_start is True:
        import webbrowser
        webbrowser.open(romfile)
    elif isinstance(auto_start, str):
        args = shlex.split(auto_start)
        # Specify full path to ROM as we are going to cd in popen
        full_rom_path = os.path.realpath(romfile)
        args.append(full_rom_path)
        try:
            # set cwd so that paths to lua scripts are always relative to our client
            if getattr(sys, 'frozen', False):
                # The application is frozen
                script_dir = os.path.dirname(sys.executable)
            else:
                script_dir = os.path.dirname(os.path.realpath(__file__))

            subprocess.Popen(args, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=script_dir)
        except FileNotFoundError:
            logger.error(f"Couldn't launch ROM, {args[0]} is missing")

def launch(*launch_args):
    async def main():
        parser = get_base_parser(description="Link's Awakening Client.")
        parser.add_argument("--url", help="Archipelago connection url")
        parser.add_argument("--no-magpie", dest='magpie', default=True, action='store_false', help="Disable magpie bridge")
        parser.add_argument('diff_file', default="", type=str, nargs="?",
                            help='Path to a .apladx Archipelago Binary Patch file')

        args = parser.parse_args(launch_args)

        if args.diff_file:
            import Patch
            logger.info("patch file was supplied - creating rom...")
            meta, rom_file = Patch.create_rom_file(args.diff_file)
            if "server" in meta and not args.connect:
                args.connect = meta["server"]
            logger.info(f"wrote rom file to {rom_file}")


        ctx = LinksAwakeningContext(args.connect, args.password, args.magpie)

        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

        # TODO: nothing about the lambda about has to be in a lambda
        ctx.la_task = create_task_log_exception(ctx.run_game_loop())
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        # Down below run_gui so that we get errors out of the process
        if args.diff_file:
            run_game(rom_file)

        await ctx.exit_event.wait()
        await ctx.shutdown()

    Utils.init_logging("LinksAwakeningContext", exception_logger="Client")

    colorama.just_fix_windows_console()
    asyncio.run(main())
    colorama.deinit()
