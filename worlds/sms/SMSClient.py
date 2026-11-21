import copy
import os
import sys
import asyncio
import time
from typing import Optional

import ModuleUpdate
ModuleUpdate.update() # Handles updated packages on source, does nothing on frozen.

import dolphin_memory_engine as dme

import Utils
apname = Utils.instance_name if Utils.instance_name else "Archipelago"
from CommonClient import gui_enabled, logger, get_base_parser, ClientCommandProcessor, server_loop
from settings import get_settings
from NetUtils import ClientStatus

from .constants import *
from .addresses import *
from .bit_helper import bit_flagger, get_flag_val
from .regions import ALL_REGIONS
from .items import REGULAR_PROGRESSION_ITEMS, TICKET_ITEMS

TRACKER_LOADED = False
try:
    from worlds.tracker.TrackerClient import TrackerGameContext as SuperContext
    TRACKER_LOADED = True
except ModuleNotFoundError:
    from CommonClient import CommonContext as SuperContext


class Ticket:
    item_name: str
    bit_position: int
    address: int

    def __init__(self, itm_name: str, bit_pos: int, addr: int):
        self.item_name = itm_name
        self.bit_position = bit_pos
        self.address = addr

def read_string(console_address: int, strlen: int) -> str:
    str_val: str = ""
    try:
        str_bytes: bytes = dme.read_bytes(console_address, strlen)
        int_val: int = int.from_bytes(str_bytes)
        if int_val == 0:
            return str_val
        str_val = str_bytes.split(b"\0", 1)[0].decode()
    except Exception as ex:
        logger.error(f"Read string error found: {ex}")
    return str_val


class SmsCommandProcessor(ClientCommandProcessor):
    def _cmd_dolphin(self):
        """Prints the current Dolphin status to the client."""
        if isinstance(self.ctx, SmsContext):
            logger.info(f"Dolphin Status: {self.ctx.dolphin_status}")

    def _cmd_change_dolphin_process_name(self, process_name: str):
        """Specify the name of the Dolphin process to connect to. "" for system default."""
        self.ctx.hook_name = process_name
        logger.info(f"Changing Dolphin process name to: {process_name if process_name else ""}")
        from .sms_settings import SuperMarioSunshineSettings
        settings: SuperMarioSunshineSettings = get_settings().sms_options
        settings.dolphin_process_name = SuperMarioSunshineSettings.DolphinProcessName(process_name)
        get_settings().save()
        log_msg: str = f"Dolphin process name set to {process_name or "default"}. You must open a new client for this to take effect."
        logger.info(log_msg)
        Utils.messagebox("Close SMS Client to take effect", log_msg, True)
        Utils.async_start(self.ctx.disconnect())


class SmsContext(SuperContext):
    command_processor = SmsCommandProcessor
    game: str = WORLD_NAME
    items_handling: int = 0b111  # full remote
    corona_message_given: bool = False
    has_send_death: bool = False
    rom_loaded: bool = False
    password_required: bool = False
    victory: bool = False

    tickets: dict[int, Ticket] = {
        0x2: Ticket("Bianco Hills Ticket", 5, 0x805789f8),
        0x3: Ticket("Ricco Harbor Ticket", 6, 0x805789f8),
        0x4: Ticket("Gelato Beach Ticket", 7, 0x805789f8),
        0x5: Ticket("Pinna Park Ticket", 1, 0x805789f9),
        0x9: Ticket("Noki Bay Ticket", 3, 0x805789fd),
        0x6: Ticket("Sirena Beach Ticket", 3, 0x805789f9),
        0x8: Ticket("Pianta Village Ticket", 4, 0x805789f9),
        0x34: Ticket("Corona Mountain Ticket", 6, 0x805789fd),
    }

    # Current Shine/Blue Coins and Recv Shine/Blue Coin
    curr_shines: int = 0
    req_shine: int = 0
    curr_blue_coins: int = 0
    req_blue_coins: int = 0
    blue_coin_sanity: bool = False
    has_receive_death: bool = False
    starting_nozzle: int
    ticket_mode: int

    # Tracker related variables
    map_id: int = 0
    episode_id: int = 0
    curr_stage: int
    next_stage: int
    curr_ep: int
    next_ep: int

    def __init__(self, server_address, password):
        super(SmsContext, self).__init__(server_address, password)
        self.dolphin_sync_task: Optional[asyncio.Task[None]] = None
        self.dolphin_status: str = CONNECTION_INITIAL_STATUS
        self.tags = {"AP"} # UT reasons, not doing this makes it a tracker.

        from . import SuperMarioSunshineSettings
        settings: SuperMarioSunshineSettings = get_settings().sms_options
        if settings.dolphin_process_name:
            os.environ[DME_DOLPHIN_PROCESS_NAME] = settings.dolphin_process_name
        elif DME_DOLPHIN_PROCESS_NAME in os.environ:
            del os.environ[DME_DOLPHIN_PROCESS_NAME]

    async def disconnect(self, allow_autoreconnect: bool = False) -> None:
        """Disconnect from the server, unhook from Dolphin Memory Engine and set flags."""
        await super().disconnect()
        dme.un_hook()
        self.set_dolphin_status(CONNECTION_LOST_STATUS)

    async def server_auth(self, password_requested: bool = False) -> None:
        """
        Authenticate with the Archipelago server. This function will be called as part of the init RoomInfo call
        in CommonClient, however we will exit if the rom is not loaded yet.

        Args:
            password_requested (bool): Whether the server requires a password. Defaults to `False`.
        """
        if not self.rom_loaded:
            logger.info(DOLPHIN_DIDNT_LOAD_ROM_CORRECTLY)
            return

        await super().server_auth(password_requested)
        await super().send_connect()

    def on_package(self, cmd: str, args: dict):
        super().on_package(cmd, args)

        match cmd:
            case "RoomInfo":
                self.password_required = bool(args["password"])

            case "Connected":
                slot_data = args["slot_data"]
                self.req_shine = slot_data["required_shines"]
                self.blue_coin_sanity = slot_data["blue_coin_sanity"]
                self.ticket_mode = int(slot_data["level_access"])
                self.starting_nozzle = slot_data["starting_nozzle"]
                self.req_blue_coins = slot_data["blue_coin_maximum"]
                Utils.async_start(self.update_death_link(bool(slot_data["death_link"])))

    async def dme_loop(self) -> None:
        """Main loop that checks in game values using Dolphin Memory Engine."""
        try:
            # If DME is not already hooked or connected in any way
            if not dme.is_hooked() and not await self.try_hook():
                return

            if not self.dolphin_status == CONNECTION_CONNECTED_STATUS:
                # checks the id of the game as a string
                romgameid: str = read_string(0x80000000, 6)
                if romgameid != GAME_ID:
                    dme.un_hook()
                    self.set_dolphin_status(DOLPHIN_DIDNT_LOAD_ROM_CORRECTLY)
                    await wait_for_next_loop(WAIT_TIMER_LONG_TIMEOUT)
                    return

                if not self.auth:
                    slot_name: str = read_string(SLOT_NAME_OFF, SMS_PLAYER_NAME_BYTE_LENGTH)
                    if slot_name == "":
                        dme.un_hook()
                        self.set_dolphin_status(DOLPHIN_DIDNT_LOAD_ROM_CORRECTLY)
                        await wait_for_next_loop(WAIT_TIMER_LONG_TIMEOUT)
                        return
                    self.auth = slot_name

                # Inform the player we are ready and waiting for them to connect.
                if not self.rom_loaded:
                    self.set_dolphin_status(CONNECTION_VERIFY_SERVER)
                    self.rom_loaded = True
                    await self.server_auth(self.password_required)

                if not self.slot:
                    await wait_for_next_loop(WAIT_TIMER_LONG_TIMEOUT)
                    return

                self.set_dolphin_status(CONNECTION_CONNECTED_STATUS)

            # Update Client Labels with Data
            self.curr_shines = self.get_item_count(523004) + self.get_item_count(523141)
            self.ui.update_corona_shine_count(self.curr_shines, self.req_shine)
            if self.blue_coin_sanity == 1:
                blue_count: int = self.get_item_count(523014)
                self.ui.update_blue_coins(blue_count, self.req_blue_coins)
            if self.ticket_mode == 1:
                ticket_list: set[str] = set([self.item_names.lookup_in_game(recv_item.item).replace(" Ticket", "") for
                    recv_item in self.items_received if self.item_names.lookup_in_game(recv_item.item) in TICKET_ITEMS])
                self.ui.update_ticket_list(ticket_list if ticket_list else ["No tickets yet..."])

            # Needs to always happen / be set to ensure Fludd is being properly set before mario loads in.
            self.re_send_nozzles()

            # Need to always set Corona Boat cutscene triggered, which allows Corona to properly unlock itself
            flag_ptr: int = dme.read_word(SMS_FLAGS_PTR)
            flag_val: int = dme.read_byte(flag_ptr + DELFINO_YOSHI_OFFSET)
            dme.write_byte(flag_ptr + DELFINO_YOSHI_OFFSET, bit_flagger(flag_val, 0x2, True))

            self.curr_stage = dme.read_byte(SMS_CURRENT_STAGE)
            self.next_stage = dme.read_byte(SMS_NEXT_STAGE)
            self.curr_ep = dme.read_byte(SMS_CURRENT_EPISODE)
            self.next_ep = dme.read_byte(SMS_NEXT_EPISODE)

            # Check Send Victory on any stage that isn't file select.
            if self.curr_stage != 0:
                await self.send_victory()

            # If mario is in some cutscene or in the intro movie scene.
            # If on stage select, don't do anything else, ignore and continue.
            # However, when you beat the game it considers current stage AS FILE SELECT
            # Therefore, we should check that as well.
            if dme.read_word(GP_MARIO) == 0 or self.curr_stage == 15:
                return

            self.give_fludd()

            await self.handle_stages()
            await self.location_watcher()
            self.sms_give_items()

            if "DeathLink" in self.tags:
                await self.check_death()

            if self.curr_shines >= self.req_shine:
                self.open_stage(self.tickets[0x34]) # Open Corona Mountain
                if not self.corona_message_given:
                    logger.info("Corona Mountain requirements reached! Reload Delfino Plaza to unlock.")
                    self.corona_message_given = True

            self.re_send_progression()

        except Exception as dmeEx:
            logger.error(f"Unable to connect to Super Mario Sunshine. Details ({type(dmeEx).__name__}): {dmeEx}")
            await self.disconnect()
            await wait_for_next_loop(WAIT_TIMER_LONG_TIMEOUT)

    async def try_hook(self) -> bool:
        """Try to hook the Dolphin Memory Engine process into dolphin."""
        dme.hook()

        if dme.get_status() == dme.get_status().noEmu or dme.get_status() == dme.get_status().notRunning:
            dme.un_hook()
            self.set_dolphin_status(CONNECTION_INITIAL_STATUS)
            await wait_for_next_loop(WAIT_TIMER_LONG_TIMEOUT)
            return False

        return True

    async def dolphin_loop(self) -> None:
        """Continuously check and communicate with Dolphin until the user disconnects."""
        logger.info("Starting Dolphin connector. Use /dolphin for status information.")
        while not self.exit_event.is_set():
            try:
                await self.dme_loop()
                await wait_for_next_loop(WAIT_TIMER_SHORT_TIMEOUT)

            except Exception as dolphinEx:
                logger.error(f"Something went wrong when connecting to Dolphin Memory Engine. Details ({type(dolphinEx).__name__}): {dolphinEx}")

    def set_dolphin_status(self, status: str) -> None:
        """
        Set the dolphin status and log it to the client.

        Args:
            status (str): The status that should be set and logged.
        """
        self.dolphin_status = status
        logger.info(self.dolphin_status)

    def give_fludd(self):
        if dme.read_byte(ARB_FLUDD_ENABLER) != 1:
            return

        # Prevent this from giving Fludd on non-ticket mode and not picked up fludd yet.
        if self.ticket_mode == 0 and (self.curr_stage == 0 or self.next_stage == 0):
            dme.write_byte(ARB_FLUDD_APPLIED, 0x1)
            return

        # For Secret Stages, ensure fludd isn't given
        if (0x1E <= self.curr_stage <= 0x33) or (0x1E <= self.next_stage <= 0x33):
            dme.write_byte(ARB_FLUDD_APPLIED, 0x1)
            return

        mario_ptr = dme.read_word(ORIG_MARIO_PTR)
        if mario_ptr == 0:
            return

        mario_flags = dme.read_word(mario_ptr + MARIO_FLAG_OFFSET)
        if not (mario_flags & MARIO_FLAG_HAS_FLUDD):
            dme.write_byte(ARB_FLUDD_APPLIED, 0x0)

    def on_deathlink(self, data: dict):
        super().on_deathlink(data)
        # Allows for death links to be received only while in a playable state to avoid dolphin errors
        game_state = dme.read_byte(GAME_STATE)
        if game_state != 4:
            return

        source = data.get('source', 'Unknown')
        cause = data.get('cause', 'No cause specified')
        logger.info(f"DeathLink received! Source: {source}")
        logger.info(f"DeathLink message: {cause}")
        logger.info("Killing Mario now...")
        self.has_receive_death = True
        self.kill_mario()

        # Wait for mario to be alive again, then reset.
        game_state = 0
        wait_mario_alive = time.time() + 30
        while game_state != 4 and time.time() <= wait_mario_alive:
            game_state = dme.read_byte(GAME_STATE)
            if game_state == 4:
                self.has_receive_death = False
                break
        return

    def kill_mario(self):
        """Uses the same logic as Gecko code death trigger"""
        if self.slot is not None and dme.is_hooked() and self.dolphin_status == CONNECTION_CONNECTED_STATUS:
            dme.write_bytes(dme.follow_pointers(GP_MARIO, [0x4C]),
                            (0x4020).to_bytes(2, byteorder="big"))
        return

    def make_gui(self):
        # Performing local import to prevent additional UIs to appear during the patching process.
        # This appears to be occurring if a spawned process does not have a UI element when importing kvui/kivymd.
        from .sms_tab import build_gui, GameManager, MDLabel

        ui: type[GameManager] = super().make_gui()
        class SMSGuiWrapper(ui):
            shine_count: MDLabel
            blue_coins: MDLabel
            tickets: MDLabel
            base_title = f"Super Mario Sunshine Client v{WORLD_VERSION}"

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

    async def handle_stages(self):
        # TODO move to its own thread, probably would prevent error stated below.
        if self.next_stage == 0x01:  # Delfino Plaza
            # If starting Fluddless without ticket mode on, open Bianco Hills
            if self.starting_nozzle == 2 and self.ticket_mode == 0:
                self.open_stage(self.tickets[0x2])

            if self.ticket_mode == 1 and self.next_ep in [0, 1, 5, 6, 7]:
                next_episode = 8
                dme.write_byte(SMS_NEXT_EPISODE, next_episode)

        if self.curr_stage != self.next_stage:
            await self.send_map_id(self.next_stage)
            if (self.ticket_mode == 1 and self.next_stage != 0x34 and self.next_stage in self.tickets.keys() and
                not self.has_item(self.tickets[self.next_stage].item_name)):
                # If there is an error around function 80178E48, it's probably trying to draw/init the shine select
                #   menu, which doesn't exist for Delfino Plaza.
                logger.info("Entering a stage without a ticket! Initiating boot-out...")
                # Byte 1 should correspond to Delfino Plaza
                dme.write_byte(SMS_NEXT_STAGE, 1)
                delfino_state: int = 1 if not self.curr_shines > self.req_shine else 8
                dme.write_byte(SMS_CURRENT_STAGE, 1)
                dme.write_byte(SMS_NEXT_EPISODE, delfino_state)
                await self.send_map_id(1)
                return

        if ((self.next_stage < 0x0D and self.next_stage != 0x07) and
                (self.next_ep != self.curr_ep) and (self.next_ep != 0xFF)):
            if self.next_stage == 0x01:
                await self.send_episode_id(-1)
            else:
                await self.send_episode_id(self.next_ep)
        elif self.next_stage >= 0x0D:
            await self.send_episode_id(-1)

    def open_stage(self, ticket):
        byte_value = bit_flagger(dme.read_byte(ticket.address), ticket.bit_position, True)
        dme.write_byte(ticket.address, byte_value)

    # Checks to see if player changed stages to update map_id for Poptracker
    async def send_map_id(self, map_id):
        if self.map_id == map_id:
            return

        self.map_id = map_id
        await self.send_msgs([{
            "cmd": "Set",
            "key": f"sms_map_{self.team}_{self.slot}",
            "default": 0,
            "want_reply": False,
            "operations": [{"operation": "replace", "value": map_id}]
        }])

    async def send_episode_id(self, episode_id):
        if self.episode_id == episode_id:
            return

        self.episode_id = episode_id
        await self.send_msgs([{
            "cmd": "Set",
            "key": f"sms_episode_{self.team}_{self.slot}",
            "default": 0,
            "want_reply": False,
            "operations": [{"operation": "replace", "value": episode_id}]
        }])

    async def location_watcher(self):
        local_bit_list: bytes = dme.read_bytes(dme.read_word(SMS_FLAGS_PTR), TOTAL_FLAG_BYTE_COUNT)

        local_missing_locs = copy.deepcopy(self.missing_locations)
        for mis_loc_id in local_missing_locs:
            # Get the loc name, then I can get Region name + Shine Name / Blue Coin / Nozzle Box
            loc_full_name = self.location_names.lookup_in_game(mis_loc_id)
            reg_name, loc_name = loc_full_name.split(" - ", 1)
            sms_reg = ALL_REGIONS[reg_name]

            # TODO when new locations are made, make a location type on the location object to remove extra loops here.
            # If the location is a shine
            if sms_reg.shines and any([shine for shine in sms_reg.shines if loc_name == shine.name]):
                in_game_bit: int = [shine.in_game_bit for shine in sms_reg.shines if loc_name == shine.name][0]
                if get_flag_val(local_bit_list, in_game_bit):
                    self.locations_checked.add(mis_loc_id)

            # If the location is a blue coin
            elif sms_reg.blue_coins and any([bc for bc in sms_reg.blue_coins if loc_name == bc.name]):
                in_game_bit: int = [bc.in_game_bit for bc in sms_reg.blue_coins if loc_name == bc.name][0]
                if get_flag_val(local_bit_list, in_game_bit):
                    self.locations_checked.add(mis_loc_id)

            # If the location is a nozzle box
            elif sms_reg.nozzle_boxes and any([nb for nb in sms_reg.nozzle_boxes if loc_name == nb.name]):
                in_game_bit: int = [nb.in_game_bit for nb in sms_reg.nozzle_boxes if loc_name == nb.name][0]
                if get_flag_val(local_bit_list, in_game_bit):
                    self.locations_checked.add(mis_loc_id)

        # Check corresponds to Shadow Mario Yoshi Egg Chase
        # delfino_yoshi_unlock = dme.read_byte(dme.read_word(SMS_FLAGS_PTR) + DELFINO_YOSHI_OFFSET)
        # if (delfino_yoshi_unlock & 0x80) and not ctx.checked_yoshi_egg:
        #     ctx.checked_yoshi_egg = True
        #     memory_changed(ctx, 113, delfino_yoshi_unlock, "Yoshi") # Swapped to self.locations_checked.add()

        await self.check_locations(self.locations_checked)
        return

    async def check_death(self):
        """Check if Mario died by checking if in the 'Mario is dying' game mode, then send DeathLink."""
        game_state = dme.read_byte(GAME_STATE)

        # Check to see if Mario is dying
        if game_state == 7:

            # Only sends a death link if they are the person dying and have not been sent a death link
            if not self.has_send_death and not self.has_receive_death:
                player_name = self.player_names[self.slot]
                await self.send_death(f"{player_name} died!")
                logger.info(f"Sent DeathLink: Mario died")

            # Set variables to combat niche cases where a death link is sent during an abnormal time
            # i.e. game paused, cutscene, shine get, etc.
            self.has_send_death = True
            self.has_receive_death = False

        # Allows for death links to be sent once respawned
        elif game_state == 4:
            self.has_send_death = False

    def sms_give_items(self):
        last_recv_idx: int = dme.read_word(dme.read_word(SMS_FLAGS_PTR) + RECEIVED_ITEM_OFFSET)
        if last_recv_idx >= len(self.items_received):
            return

        for item_id in self.items_received[last_recv_idx:]:
            item_name = self.item_names.lookup_in_game(item_id.item)

            if item_name == "1-UP":
                self.increase_lives()

            last_recv_idx += 1

        dme.write_word(dme.read_word(SMS_FLAGS_PTR) + RECEIVED_ITEM_OFFSET, last_recv_idx)
        return

    def activate_nozzle(self, noz_id: int):
        activated_bits = dme.read_byte(ARB_NOZZLES_ENABLER)
        activated_bits = bit_flagger(activated_bits, noz_id, True)
        dme.write_byte(ARB_FLUDD_ENABLER, 0x1)
        dme.write_byte(ARB_NOZZLES_ENABLER, activated_bits)

    def activate_yoshi(self):
        dme.write_byte(YOSHI_ADDRESS, 0x01)
        return

    def get_item_count(self, item_id: int):
        return len([recv_item for recv_item in self.items_received if recv_item.item == item_id])

    def receive_shine_sprite(self):
        dme.write_word(dme.read_word(SMS_FLAGS_PTR) + SHINE_COUNT_OFFSET, self.curr_shines)
        return

    def receive_blue_coin(self):
        blue_count: int = self.get_item_count(523014)
        dme.write_word(dme.read_word(SMS_FLAGS_PTR) + BLUECOIN_COUNT_OFFSET, blue_count)
        return

    def increase_lives(self):
        current_lives: int = dme.read_word(dme.read_word(SMS_FLAGS_PTR) + LIVES_COUNT_OFFSET)
        if current_lives >= 99:
            return

        dme.write_word(dme.read_word(SMS_FLAGS_PTR) + LIVES_COUNT_OFFSET, current_lives + 1)
        return

    async def send_victory(self):
        if self.victory:
            return

        corona_byte: int = dme.read_byte(dme.read_word(SMS_FLAGS_PTR) + SMS_SHINE_BYTE_COUNT - 1)
        beat_corona: bool = (corona_byte & (1 << 7)) > 0

        if not beat_corona:
            return

        self.victory = True
        await self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
        logger.info("Congratulations on completing your seed!")
        await asyncio.sleep(.05)
        logger.info("ARCHIPELAGO SUPER MARIO SUNSHINE CREDITS:")
        await asyncio.sleep(.05)
        logger.info("MrsMarinaRose - Client, Modding and Patching")
        await asyncio.sleep(.05)
        logger.info("Hatkirby - APworld")
        await asyncio.sleep(.05)
        logger.info("ScorelessPine - Original Manual")
        await asyncio.sleep(.05)
        logger.info("Fedora - Logic and testing")
        await asyncio.sleep(.05)
        logger.info("J2Slow - Logic and testing")
        await asyncio.sleep(.05)
        logger.info("Quizzeh - Extra testing")
        await asyncio.sleep(.05)
        # logger.info("DoubleDubbel - The Incredible Name For The Randomizer ISO")
        # time.sleep(.05)
        logger.info("Spicynun - Additional research")
        await asyncio.sleep(.05)
        logger.info("JoshuaMKW - Sunshine Toolset")
        await asyncio.sleep(.05)
        logger.info("All Archipelago core devs")
        await asyncio.sleep(.05)
        logger.info("Nintendo EAD")
        await asyncio.sleep(.05)
        logger.info("...and you. Thanks for playing!")
        return

    def re_send_nozzles(self):
        for nozzle_name, nozzle_id in REGULAR_PROGRESSION_ITEMS.items():
            if not any([x.item for x in self.items_received if nozzle_id == x.item]):
                continue

            match nozzle_name:
                case "Spray Nozzle":
                    self.activate_nozzle(0)
                case "Hover Nozzle":
                    self.activate_nozzle(1)
                case "Rocket Nozzle":
                    self.activate_nozzle(2)
                case "Turbo Nozzle":
                    self.activate_nozzle(3)
                case "Yoshi":
                    self.activate_yoshi()
        return

    def re_send_progression(self):
        self.re_send_nozzles()
        for ticket_id, sms_ticket in self.tickets.items():
            if self.has_item(sms_ticket.item_name):
                self.open_stage(self.tickets[ticket_id])

        self.receive_blue_coin()
        self.receive_shine_sprite()
        return

    def has_item(self, item_name: str):
        if item_name == "Corona Mountain Ticket":
            if not self.curr_shines > self.req_shine:
                return False
            return True

        return any([recv_item for recv_item in self.items_received if
            self.item_names.lookup_in_game(recv_item.item) == item_name])


async def wait_for_next_loop(time_to_wait: float) -> None:
    await asyncio.sleep(time_to_wait)

def main(*launch_args: str):
    import colorama
    from .iso_helper.sms_rom import SMSPatch
    from .dolphin_launcher import DolphinLauncher

    server_address: str = ""
    rom_path: str = ""

    parser = get_base_parser()
    parser.add_argument("apsms_file", default="", type=str, nargs="?", help="Path to a APSMS File")
    args = parser.parse_args(launch_args)
    dolphin_launcher: DolphinLauncher = DolphinLauncher()

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

        if TRACKER_LOADED:
            ctx.run_generator()
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        await asyncio.sleep(1)

        ctx.dolphin_sync_task = asyncio.create_task(ctx.dolphin_loop(), name="SmsDolphinSync")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.dolphin_sync_task:
            await ctx.dolphin_sync_task

    Utils.asyncio.run(dolphin_launcher.launch_dolphin_async(rom_path))
    colorama.just_fix_windows_console()
    asyncio.run(_main(args.connect, args.password))
    colorama.deinit()


if __name__ == "__main__":
    Utils.init_logging(CLIENT_NAME, exception_logger="Client")
    main(*sys.argv[1:])