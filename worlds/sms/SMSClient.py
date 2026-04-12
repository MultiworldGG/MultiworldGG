from __future__ import annotations

import copy
import os
import sys
import asyncio
import collections
import time
import traceback
from typing import Optional
from dataclasses import dataclass

import ModuleUpdate
import Utils
apname = Utils.instance_name if Utils.instance_name else "Archipelago"
from NetUtils import ClientStatus
from CommonClient import gui_enabled, logger, get_base_parser, ClientCommandProcessor, \
    server_loop
from .options import SmsOptions
from .bit_helper import change_endian, bit_flagger, extract_bits
from .regions import ALL_REGIONS, get_location_name_to_id
from .items import TICKET_ITEMS
import dolphin_memory_engine as dme
from . import addresses
from settings import get_settings

ModuleUpdate.update()

TRACKER_LOADED = False
try:
    from worlds.tracker.TrackerClient import TrackerGameContext as SuperContext
    TRACKER_LOADED = True
except ModuleNotFoundError:
    from CommonClient import CommonContext as SuperContext

CONNECTION_REFUSED_GAME_STATUS = (
    "Dolphin failed to connect. Please load a randomized ROM for Super Mario Sunshine. Trying again in 5 seconds..."
)
CONNECTION_REFUSED_SAVE_STATUS = (
    "Dolphin failed to connect. Please load into the save file. Trying again in 5 seconds..."
)
CONNECTION_LOST_STATUS = (
    "Dolphin connection was lost. Please restart your emulator and make sure Super Mario Sunshine is running."
)
CONNECTION_CONNECTED_STATUS = "Dolphin connected successfully."
CONNECTION_INITIAL_STATUS = "Dolphin connection has not been initiated."

ticket_listing = []
world_flags = {}

DEBUG = False
GAME_VER = 0x3a
AP_WORLD_VERSION_NAME = "0.6.7"
CLIENT_VERSION = "0.6.0"

DME_DOLPHIN_PROCESS_NAME_ENV_VARIABLE = "DME_DOLPHIN_PROCESS_NAME"


@dataclass
class NozzleItem:
    nozzle_name: str
    ap_item_id: int


NOZZLES: list[NozzleItem] = [
    NozzleItem("Spray Nozzle", 523000),
    NozzleItem("Hover Nozzle", 523001),
    NozzleItem("Rocket Nozzle", 523002),
    NozzleItem("Turbo Nozzle", 523003),
    NozzleItem("Yoshi", 53013)
]

class SmsCommandProcessor(ClientCommandProcessor):
    def _cmd_connect(self, address: str = "") -> bool:
        if isinstance(self.ctx, SmsContext):
            logger.info(f"Dolphin Status: {self.ctx.dolphin_status}")

    def _cmd_resync(self):
        """Manually trigger a resync."""
        self.output("Syncing items.")
        self.ctx.syncing = True
        refresh_collection_counts(self.ctx)

    def _cmd_change_dolphin_process_name(self, process_name: str):
        """Specify the name of the Dolphin process to connect to. "" for system default."""
        self.ctx.hook_check = False
        self.ctx.hook_name = process_name
        logger.info(f"Changing Dolphin process name to: {process_name if process_name else ""}")
        from . import SuperMarioSunshineSettings
        settings: SuperMarioSunshineSettings = get_settings().sms_options
        settings.dolphin_process_name = SuperMarioSunshineSettings.DolphinProcessName(process_name)
        get_settings().save()
        log_msg: str = f"Dolphin process name set to {process_name or "default"}. You must open a new client for this to take effect."
        logger.info(log_msg)
        Utils.messagebox("Close SMS Client to take effect", log_msg)
        Utils.async_start(unhook_dolphin(self.ctx))

class SmsContext(SuperContext):
    command_processor = SmsCommandProcessor
    game = "Super Mario Sunshine"
    tags = {"AP"}
    items_handling = 0b111  # full remote

    options: SmsOptions
    hook_name: str = ""
    hook_check = True

    lives_given = 0
    lives_switch = False

    plaza_episode = 0

    goal = 50
    corona_message_given = False
    blue_status = 1
    fludd_start = 0
    bianco_flag = 0
    ticket_mode = False
    victory = False
    checked_yoshi_egg = False

    ap_nozzles_received = []

    # Current Shine/Blue Coins and Recv Shine/Blue Coin
    curr_shines: int = 0
    req_shine: int = 0
    curr_blue_coins: int = 0
    req_blue_coins: int = 0

    def __init__(self, server_address, password):
        super(SmsContext, self).__init__(server_address, password)
        self.send_index: int = 0
        self.syncing = False
        self.awaiting_bridge = False
        self.dolphin_sync_task: Optional[asyncio.Task[None]] = None
        self.dolphin_status: str = CONNECTION_INITIAL_STATUS
        self.awaiting_rom: bool = False
        self.has_send_death: bool = False

        from . import SuperMarioSunshineSettings
        settings: SuperMarioSunshineSettings = get_settings().sms_options
        if settings.dolphin_process_name:
            os.environ[DME_DOLPHIN_PROCESS_NAME_ENV_VARIABLE] = settings.dolphin_process_name
        elif DME_DOLPHIN_PROCESS_NAME_ENV_VARIABLE in os.environ:
            del os.environ[DME_DOLPHIN_PROCESS_NAME_ENV_VARIABLE]

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(SmsContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    @property
    def endpoints(self):
        if self.server:
            return [self.server]
        else:
            return []

    def on_package(self, cmd: str, args: dict):
        super().on_package(cmd, args)

        if cmd == "Connected":
            slot_data = args.get("slot_data")
            self.goal = slot_data.get("corona_mountain_shines")
            temp = slot_data.get("blue_coin_sanity")
            if temp:
                self.blue_status = temp
            temp = slot_data.get("starting_nozzle")
            if temp:
                self.fludd_start = temp
            temp = slot_data.get("ticket_mode")
            if temp:
                self.ticket_mode = temp

            self.req_shine = self.goal
            self.req_blue_coins = slot_data.get("blue_coin_maximum", 0)

            if "death_link" in slot_data:
                Utils.async_start(self.update_death_link(bool(slot_data["death_link"])))


    def on_deathlink(self, data: dict):
        super().on_deathlink(data)
        source = data.get('source', 'Unknown')
        cause = data.get('cause', 'No cause specified')
        logger.info(f"DeathLink received! Source: {source}")
        logger.info(f"DeathLink message: {cause}")
        logger.info("Killing Mario now...")
        kill_mario(self)

    def get_corona_goal(self):
        if self.goal:
            return self.goal
        else:
            return 50

    def make_gui(self):
        # Performing local import to prevent additional UIs to appear during the patching process.
        # This appears to be occurring if a spawned process does not have a UI element when importing kvui/kivymd.
        from .sms_tab import build_gui, GameManager, MDLabel

        ui: type[GameManager] = super().make_gui()
        class SMSGuiWrapper(ui):
            shine_count: MDLabel
            blue_coins: MDLabel
            tickets: MDLabel
            base_title = "Super Mario Sunshine Client"

            def build(self):
                container = super().build()

                self.base_title += f" |  {apname}"
                build_gui(self)

                return container

            def update_corona_shine_count(self, shine_count: int, shines_required: int):
                self.shine_count.text = f"{shine_count} / {shines_required}"

            def update_blue_coins(self, blue_coins: int, coins_req: int):
                self.blue_coins.text = f"{blue_coins} / {coins_req}"

            def update_ticket_list(self, ticket_list: set[str]):
                self.tickets.text = "; ".join(ticket_list)

        return SMSGuiWrapper


storedShines = []
curShines = []
storedBlues = []
curBlues = []
storedNozzleBoxes = []
curNozzleBoxes = []

DELAY_SECONDS = .5
LOCATION_OFFSET = 523000

def read_string(console_address: int, strlen: int) -> str:
    return dme.read_bytes(console_address, strlen).split(b"\0", 1)[0].decode()


def game_start():
    for _ in range(0, addresses.SMS_SHINE_BYTE_COUNT):
        storedShines.append(0x00)
        curShines.append(0x00)
    for _ in range(0, addresses.SMS_BLUECOIN_BYTE_COUNT):
        storedBlues.append(0x00)
        curBlues.append(0x00)
    for _ in range(0, addresses.NOZZLE_BOXES_BYTE_COUNT):
        storedNozzleBoxes.append(0x00)
        curNozzleBoxes.append(0x00)

# Apparently when you beat the game it considers current stage AS FILE SELECT
# Therefore it wasn't sending out the Victory check
def in_file_select():
    return dme.read_byte(addresses.SMS_CURRENT_STAGE) == 15


async def game_watcher(ctx: SmsContext):
    previous_lives = None

    while not ctx.exit_event.is_set():
        if not dme.is_hooked() or ctx.slot is None:
            await asyncio.sleep(5)
            continue

        # if in_file_select():
        #     await asyncio.sleep(1)
        #     continue

        await handle_stages(ctx)
        await location_watcher(ctx)

        if "DeathLink" in ctx.tags:
            await check_death(ctx, previous_lives)
            try:
                previous_lives = dme.read_word(dme.read_word(addresses.SMS_FLAGS_PTR) + addresses.LIVES_COUNT_OFFSET)
            except:
                pass

        sync_msg = [{'cmd': 'Sync'}]
        if ctx.locations_checked:
            sync_msg.append({"cmd": "LocationChecks", "locations": list(ctx.locations_checked)})
        await ctx.send_msgs(sync_msg)

        #Gravi01 Begin
        refresh_collection_counts(ctx)
        ctx.lives_switch = True
        #Gravi01 End

        if ctx.victory and not ctx.finished_game:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True

        await asyncio.sleep(0.2)
        ctx.lives_switch = False


async def check_death(ctx: SmsContext, previous_lives):
    """Check if Mario died by comparing current lives with previous lives, then send DeathLink."""
    if ctx.slot is None or previous_lives is None:
        return

    try:
        current_lives = dme.read_word(dme.read_word(addresses.SMS_FLAGS_PTR) + addresses.LIVES_COUNT_OFFSET)
        if (current_lives < previous_lives != 255) or (current_lives == 0 and previous_lives == 255):
            if not ctx.has_send_death and time.time() >= ctx.last_death_link + 6: #prevent more double-deaths
                ctx.has_send_death = True
                player_name = ctx.player_names[ctx.slot] if ctx.slot in ctx.player_names else "Player"
                await ctx.send_death(f"{player_name} died!")
                logger.info(f"Sent DeathLink: Mario died (lives {previous_lives} -> {current_lives})")
        else:
            ctx.has_send_death = False
    except Exception as e:
        logger.error(f"Error checking death: {e}")


async def location_watcher(ctx):
    for x in range(0, addresses.SMS_SHINE_BYTE_COUNT):
        targ_location = dme.read_word(addresses.SMS_FLAGS_PTR) + x
        cache_byte = dme.read_byte(targ_location)
        curShines[x] = cache_byte
        if storedShines[x] != curShines[x]:
            memory_changed(ctx, x, curShines[x], "Shine")
            storedShines[x] = curShines[x]

    # If possible, check if blue coin sanity is enabled or not
    for x in range(0, addresses.SMS_BLUECOIN_BYTE_COUNT):
        targ_location = dme.read_word(addresses.SMS_FLAGS_PTR) + addresses.BLUECOIN_LOC_OFFSET + x
        cache_byte = dme.read_byte(targ_location)
        curBlues[x] = cache_byte
        if storedBlues[x] != curBlues[x]:
            memory_changed(ctx, x+15, curBlues[x], "Blue Coin") # Add 15 to 'x' to align with blue coin IDs
            storedBlues[x] = curBlues[x]

    for x in range(0, addresses.NOZZLE_BOXES_BYTE_COUNT):
        targ_location = dme.read_word(addresses.SMS_FLAGS_PTR) + addresses.NOZZLE_BOXES_OFFSET + x
        cache_byte = dme.read_byte(targ_location)
        curNozzleBoxes[x] = cache_byte
        if storedNozzleBoxes[x] != curNozzleBoxes[x]:
            memory_changed(ctx, x+108, curNozzleBoxes[x], "Nozzle")
            storedNozzleBoxes[x] = curNozzleBoxes[x]

    # Check corresponds to Shadow Mario Yoshi Egg Chase
    delfino_yoshi_unlock = dme.read_byte(dme.read_word(addresses.SMS_FLAGS_PTR) + addresses.DELFINO_YOSHI_OFFSET)
    if (delfino_yoshi_unlock & 0x80) and not ctx.checked_yoshi_egg:
        ctx.checked_yoshi_egg = True
        memory_changed(ctx, 113, delfino_yoshi_unlock, "Yoshi")
    return


async def handle_stages(ctx):
    #Gravi01  change to connection status
    next_stage = dme.read_byte(addresses.SMS_NEXT_STAGE)
    cur_stage = dme.read_byte(addresses.SMS_CURRENT_STAGE)
    if next_stage == 0x01: # Delfino Plaza
        next_episode = dme.read_byte(addresses.SMS_NEXT_EPISODE)

        # If starting Fluddless without ticket mode on, open Bianco Hills
        if not ctx.bianco_flag and ctx.fludd_start == 2 and ctx.ticket_mode == 0:
            ctx.bianco_flag |= dme.read_byte(TICKETS[0].address)
            dme.write_byte(TICKETS[0].address, ctx.bianco_flag)
            open_stage(TICKETS[0])
        # Sets plaza state to 8 if in ticket mode and goal hasn't been reached
        if ctx.ticket_mode == 1 and next_episode != 0x8 and not ctx.corona_message_given:
            dme.write_byte(addresses.SMS_NEXT_EPISODE, 8)
    if cur_stage != next_stage:
        await send_map_id(next_stage, ctx)
        if ctx.ticket_mode:
            await resolve_tickets(next_stage, ctx)


async def dolphin_sync_task(ctx: SmsContext) -> None:
    logger.info("Starting Dolphin connector. Use /dolphin for status information.")
    while not ctx.exit_event.is_set():
        try:
            if dme.is_hooked() and ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
                # if ctx.slot is not None:
                #     # await give_items(ctx)
                #     # await check_locations(ctx)
                #     # await check_current_stage_changed(ctx)
                #     # self._cmd_resync()
                # else:
                if ctx.awaiting_rom:
                    await ctx.server_auth()

                # If the client's ui has loaded
                if ctx.ui:
                    ctx.curr_shines = len([recv_item for recv_item in ctx.items_received if
                        ctx.item_names.lookup_in_game(recv_item.item) == "Shine Sprite"])
                    ctx.curr_blue_coins = len([recv_item for recv_item in ctx.items_received if
                         ctx.item_names.lookup_in_game(recv_item.item) == "Blue Coin"])
                    ctx.ui.update_corona_shine_count(ctx.curr_shines, ctx.req_shine)
                    ctx.ui.update_blue_coins(ctx.curr_blue_coins, ctx.req_blue_coins)

                    if ctx.ticket_mode:
                        ticket_list: set[str] = set([ctx.item_names.lookup_in_game(recv_item.item).replace(" Ticket", "")
                            for recv_item in ctx.items_received if ctx.item_names.lookup_in_game(recv_item.item) in TICKET_ITEMS])
                        ctx.ui.update_ticket_list(ticket_list)

                await asyncio.sleep(0.1)
            else:
                if ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
                    logger.info("Connection to Dolphin lost, reconnecting...")
                    ctx.dolphin_status = CONNECTION_LOST_STATUS
                logger.info("Attempting to connect to Dolphin...")
                dme.hook()
                if dme.is_hooked():
                    if dme.read_bytes(0x80000000, 6) != b"GMSEAP":
                        logger.info(CONNECTION_REFUSED_GAME_STATUS)
                        ctx.dolphin_status = CONNECTION_REFUSED_GAME_STATUS
                        dme.un_hook()
                        await asyncio.sleep(5)
                    else:
                        logger.info(CONNECTION_CONNECTED_STATUS)
                        ctx.dolphin_status = CONNECTION_CONNECTED_STATUS
                        ctx.locations_checked = set()
                        await asyncio.sleep(5)
                else:
                    logger.info("Connection to Dolphin failed, attempting again in 5 seconds...")
                    ctx.dolphin_status = CONNECTION_LOST_STATUS
                    await unhook_dolphin(ctx)
                    await asyncio.sleep(5)
                    continue
        except Exception:
            logger.info("Connection to Dolphin failed, attempting again in 5 seconds...")
            logger.error(traceback.format_exc())
            ctx.dolphin_status = CONNECTION_LOST_STATUS
            await unhook_dolphin(ctx)
            await asyncio.sleep(5)
            continue

async def unhook_dolphin(ctx: SmsContext):
    dme.un_hook()
    if ctx.hook_check:
        await ctx.disconnect()
    else:
        ctx.hook_check = True

async def arbitrary_ram_checks(ctx):
    while not ctx.exit_event.is_set():
        if not dme.is_hooked() or ctx.slot is None:
            await asyncio.sleep(5)
            continue

        activated_bits = dme.read_byte(addresses.ARB_NOZZLES_ENABLER)

        for noz in ctx.ap_nozzles_received:
            if noz < 4:
                activated_bits = bit_flagger(activated_bits, noz, True)
                dme.write_byte(addresses.ARB_FLUDD_ENABLER, 0x1)
                dme.write_byte(addresses.ARB_NOZZLES_ENABLER, activated_bits)
        await asyncio.sleep(DELAY_SECONDS)


def memory_changed(ctx: SmsContext, bit_pos, cached_byte, loc_type: str):
    if DEBUG: logger.info(f"memory_changed: {cached_byte}, bit_pos: {bit_pos}")
    bit_list = []

    bit_found = extract_bits(cached_byte, bit_pos)
    bit_list.extend(bit_found)

    # if DEBUG: logger.info("bit_list: " + str(bit_list))
    parse_bits(bit_list, ctx, loc_type)


def send_victory(ctx: SmsContext):
    if ctx.victory:
        return

    ctx.victory = True
    ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
    logger.info("Congratulations on completing your seed!")
    time.sleep(.05)
    logger.info("ARCHIPELAGO SUPER MARIO SUNSHINE CREDITS:")
    time.sleep(.05)
    logger.info("MrsMarinaRose - Client, Modding and Patching")
    time.sleep(.05)
    logger.info("Hatkirby - APworld")
    time.sleep(.05)
    logger.info("ScorelessPine - Original Manual")
    time.sleep(.05)
    logger.info("Fedora - Logic and testing")
    time.sleep(.05)
    logger.info("J2Slow - Logic and testing")
    time.sleep(.05)
    logger.info("Quizzeh - Extra testing")
    time.sleep(.05)
    # logger.info("DoubleDubbel - The Incredible Name For The Randomizer ISO")
    # time.sleep(.05)
    logger.info("Spicynun - Additional research")
    time.sleep(.05)
    logger.info("JoshuaMKW - Sunshine Toolset")
    time.sleep(.05)
    logger.info("All Archipelago core devs")
    time.sleep(.05)
    logger.info("Nintendo EAD")
    time.sleep(.05)
    logger.info("...and you. Thanks for playing!")
    return


def parse_bits(all_bits, ctx: SmsContext, parse_type: str):
    if DEBUG:
        logger.info("parse_bits: %s", str(all_bits))
    if len(all_bits) == 0:
        return

    for x in all_bits:
        if x != 119 and x <= 911:
            for sms_region in ALL_REGIONS.values():
                possible_locs: list[str] = []
                match parse_type:
                    case "Shine":
                        possible_locs: list[str] = [f"{sms_region.name} - {shine_loc.name}" for shine_loc in
                            sms_region.shines if shine_loc.in_game_bit == x]
                    case "Blue Coin":
                        possible_locs: list[str] = [f"{sms_region.name} - {blue_loc.name}" for blue_loc in
                            sms_region.blue_coins if blue_loc.in_game_bit == x]
                    case "Nozzle":
                        possible_locs: list[str] = [f"{sms_region.name} - {nozz_loc.name}" for nozz_loc in
                            sms_region.nozzle_boxes if nozz_loc.in_game_bit == x]
                    case _:
                        continue

                if not possible_locs:
                    continue

                ctx.locations_checked.add(get_location_name_to_id()[possible_locs[0]])
                if DEBUG:
                    logger.info("checks to send: %s", possible_locs[0])
        elif x == 119:
            send_victory(ctx)


def get_shine_id(location, value):
    temp = location + value - dme.read_word(addresses.SMS_FLAGS_PTR)
    shine_id = int(temp)
    return shine_id


def refresh_item_count(ctx, item_id, targ_address):
    counts = collections.Counter(received_item.item for received_item in ctx.items_received)
    temp = change_endian(counts[item_id])
    #Gravi01 Begin      #Stacktrace where the original Exception was thrown. Keeping the changes in this place as well, you still land here without connection, due to it being an async task
    if ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
        try:
            dme.write_word(targ_address, temp)
        except Exception:
            logger.info("Connection to Dolphin lost, reconnecting...")
            ctx.dolphin_status = CONNECTION_LOST_STATUS
            dme.un_hook()
    #Gravi01 End


def refresh_all_items(ctx: SmsContext):
    counts = collections.Counter(received_item.item for received_item in ctx.items_received)
    for item in counts:
        if counts[item] > 0:
            unpack_item(item, ctx)
    if counts[523004] >= ctx.get_corona_goal():
        activate_ticket(999999)
        if not ctx.corona_message_given:
            logger.info("Corona Mountain requirements reached! Reload Delfino Plaza to unlock.")
            ctx.corona_message_given = True


def refresh_collection_counts(ctx):
    #if DEBUG: logger.info("refresh_collection_counts")
    refresh_item_count(ctx, 523004, dme.read_word(addresses.SMS_FLAGS_PTR) + addresses.SHINE_COUNT_OFFSET)
    if ctx.blue_status == 1:
        refresh_item_count(ctx, 523014, dme.read_word(addresses.SMS_FLAGS_PTR) + addresses.BLUECOIN_COUNT_OFFSET)
    refresh_all_items(ctx)


def check_world_flags(byte_location, byte_pos, bool_setting):
    if world_flags.get(byte_location):
        byte_value = world_flags.get(byte_location)
    else:
        byte_value = dme.read_byte(byte_location)
    byte_value = bit_flagger(byte_value, byte_pos, bool_setting)
    world_flags.update({byte_location: byte_value})
    return byte_value


def open_stage(ticket):
    value = check_world_flags(ticket.address, ticket.bit_position, True)
    value |= dme.read_byte(ticket.address)
    dme.write_byte(ticket.address, value)
    return


def special_noki_handling():
    dme.write_byte(addresses.SMS_NOKI_REQ, addresses.SMS_NOKI_LO)
    return


def unpack_item(item, ctx):
    if 522999 < item < 523004:
        activate_nozzle(item, ctx)
    elif item == 523013:
        activate_yoshi(ctx)
    elif 523004 < item < 523012:
        activate_ticket(item)

@dataclass
class Ticket:
    item_name: str
    item_id: int
    bit_position: int
    course_id: int
    address: int = 0x805789f8
    active: bool = False


TICKETS: list[Ticket] = [
    Ticket("Bianco Hills Ticket", 523005, 5, 2, 0x805789f8),
    Ticket("Ricco Harbor Ticket", 523006, 6, 3, 0x805789f8),
    Ticket("Gelato Beach Ticket", 523007, 7, 4, 0x805789f8),
    Ticket("Pinna Park Ticket", 523008, 1, 5, 0x805789f9),
    Ticket("Noki Bay Ticket", 523009, 3, 9, 0x805789fd),
    Ticket("Sirena Beach Ticket", 523010, 3, 6, 0x805789f9),
    Ticket("Pianta Village Ticket", 523011, 4, 8, 0x805789f9),
    Ticket("Corona Mountain Ticket", 999999, 6, 34, 0x805789fd)
]


def activate_ticket(id: int):
    for tickets in TICKETS:
        if id == tickets.item_id:
            tickets.active = True
            handle_ticket(tickets)
            if not ticket_listing.__contains__(tickets.item_name):
                ticket_listing.append(tickets.item_name)


def handle_ticket(tick: Ticket):
    if not tick.active:
        return
    if tick.item_name == "Noki Bay Ticket":
        special_noki_handling()
    open_stage(tick)
    return

# Not even used
def refresh_all_tickets():
    for tickets in TICKETS:
        handle_ticket(tickets)


def activate_nozzle(id, ctx):
    if id == 523000:
        if not ctx.ap_nozzles_received.__contains__(0):
            ctx.ap_nozzles_received.append(0)
    elif id == 523001:
        if not ctx.ap_nozzles_received.__contains__(1):
            ctx.ap_nozzles_received.append(1)
    elif id == 523002:
        if not ctx.ap_nozzles_received.__contains__(2):
            ctx.ap_nozzles_received.append(2)
        # rocket nozzle
    elif id == 523003:
        if not ctx.ap_nozzles_received.__contains__(3):
            ctx.ap_nozzles_received.append(3)
        # turbo nozzle
    return


def activate_yoshi(ctx):
    dme.write_byte(0x80417A03, 0x01)
    if not ctx.ap_nozzles_received.__contains__(4):
        ctx.ap_nozzles_received.append(4)
    return


def kill_mario(ctx: SmsContext):
    """Uses the same logic as Gecko code death trigger"""
    if ctx.slot is not None and dme.is_hooked() and ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
        try:
            pointer_addr = 0x8040E178
            pointer_value = int.from_bytes(dme.read_bytes(pointer_addr, 4), byteorder="big")
            actual_target = pointer_value + 0x4C

            dme.write_bytes(actual_target, (0x4020).to_bytes(2, byteorder="big"))
            ctx.has_send_death = True
        except Exception as e:
            logger.error(f"Failed to kill Mario - connection may be lost: {e}")
    return


async def resolve_tickets(stage, ctx):
    for tick in TICKETS:
        if tick.course_id == stage and not tick.active:
            logger.info("Entering a stage without a ticket! Initiating bootout...")
            # Byte 1 should correspond to Delfino Plaza
            dme.write_byte(addresses.SMS_NEXT_STAGE, 1)
            dme.write_byte(addresses.SMS_CURRENT_STAGE, 1)
            await send_map_id(1, ctx)
        else:
            await send_map_id(stage, ctx)
    return

# Checks to see if player changed stages to update map_id for Poptracker
async def send_map_id(map_id, ctx):
    await ctx.send_msgs([{
        "cmd": "Set",
        "key": f"sms_map_{ctx.team}_{ctx.slot}",
        "default": 0,
        "want_reply": False,
        "operations": [{"operation": "replace", "value": map_id}]
    }])


def main(*launch_args: str):
    import colorama
    from .iso_helper.sms_rom import SMSPatch

    server_address: str = ""
    rom_path: str = ""

    parser = get_base_parser()
    parser.add_argument("apsms_file", default="", type=str, nargs="?", help="Path to a APSMS File")
    args = parser.parse_args(launch_args)

    if args.apsms_file:
        sms_patch = SMSPatch()
        try:
            sms_manifest = sms_patch.read_contents(args.apsms_file)
            server_address = sms_manifest["server"]
            rom_path = sms_patch.patch(args.apsms_file)
        except Exception as ex:
            logger.error("Unable to patch your Super Mario Sunshine. Additional Details:\n" + str(ex))
            Utils.messagebox("Cannot Patch Super Mario Sunshine", "Unable to patch your Super Mario Sunshine ROM as " +
                "expected. Additional details:\n" + str(ex), True)
            raise ex

    async def _main(connect, password):
        ctx = SmsContext(server_address if server_address else connect, password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")

        # ctx._main()

        if TRACKER_LOADED:
            ctx.run_generator()
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        await asyncio.sleep(1)

        game_start()

        ctx.dolphin_sync_task = asyncio.create_task(dolphin_sync_task(ctx), name="SmsDolphinSync")

        progression_watcher = asyncio.create_task(game_watcher(ctx), name="SmsProgressionWatcher")
        arbitrary = asyncio.create_task(arbitrary_ram_checks(ctx), name="SmsArbitraryWatcher")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.dolphin_sync_task:
            await ctx.dolphin_sync_task

        if progression_watcher:
            await progression_watcher

        if arbitrary:
            await arbitrary

    colorama.just_fix_windows_console()
    asyncio.run(_main(args.connect, args.password))
    colorama.deinit()


if __name__ == "__main__":
    Utils.init_logging("SMSClient", exception_logger="Client")
    main(*sys.argv[1:])
