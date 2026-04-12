import asyncio, time
import copy, sys, re
import os
from typing import Any

# AP related imports
import NetUtils, Utils
from CommonClient import get_base_parser, gui_enabled, server_loop
from settings import get_settings

# 3rd Party related imports
import dolphin_memory_engine as dme

# Local related imports
from .client.contexts.base_context import BaseContext, logger
from .Regions import REGION_LIST
from .iso_helper.LM_Rom import LMUSAAPPatch
from .Items import *
from .Locations import ALL_LOCATION_TABLE, SELF_LOCATIONS_TO_RECV
from .Helper_Functions import byte_string_strip_null_terminator, LMDynamicAddresses
from .client.links.energy_link.energy_link import EnergyLinkConstants
from .client.links.energy_link.energy_link_command_processor import EnergyLinkCommandProcessor
from .client.constants import *
from .client.display_in_game import LMDisplayQueue

from .client.luigismansion_settings import LuigisMansionSettings, DolphinProcessName

DME_DOLPHIN_PROCESS_NAME_ENV_VARIABLE = "DME_DOLPHIN_PROCESS_NAME"

# This is the address that holds the player's slot name.
# This way, the player does not have to manually authenticate their slot name.
SLOT_NAME_ADDR = 0x80327740
SLOT_NAME_STR_LENGTH = 64

# This Play State address lets us know if the game is playable and ready. This should have a value of 2
# Map ID is used to confirm Luigi is loading into the Mansion or one of the boss maps.
CURR_PLAY_STATE_ADDR = 0x803A3AE4
CURR_MAP_ID_ADDR = 0x804D80A4

# This address is used to check/set the player's health for DeathLink. (2 bytes / Half word)
CURR_HEALTH_ADDR = 0x803D8B40
CHECK_DEATH_ACTIVE = 0x804D07FB
CURR_HEALTH_OFFSET = 0xB8

# This Furniture address table contains the start of the addresses used for currently loaded in Furniture.
# Since multiple rooms can be loaded into the background, several hundred addresses must be checked.
# Each furniture flag and ID are 4 Bytes / Word.
# Flag Offset will contain whether the current piece of furniture has been interacted with or not.
# This flag follows the 2 rooms away rule and resets between reloading the game / save file.
# A Flag with value 0x00 indicates no interaction, 0x01 indicates it has been interacted with and has either
# dropped something or had dust, and 0x02 indicates an important item, such as a Mario Item or Elemental Medal.
FURNITURE_MAIN_TABLE_ID = 0x803CD760
FURNITURE_ADDR_COUNT = 800
FURN_FLAG_OFFSET = 0x8C
FURN_ID_OFFSET = 0xBC

# This is a word of length 0x04 which contains the last received index of the item that was given to Luigi
# This index is updated every time a new item is received. This is located within the save data
LAST_RECV_ITEM_ADDR = 0x803CDEBA
# This is a duplicate of the above, except not located in the save data. If a user forgets to save since they last
# recevied an item, this will prevent a trap death loop.
NON_SAVE_LAST_RECV_ITEM_ADDR = 0x803D5CC0

# These addresses are related to displaying text in game.
RECV_DEFAULT_TIMER_IN_HEX = "96" # 5 Seconds
RECV_ITEM_DISPLAY_TIMER_ADDR = 0x804DDA6C
RECV_ITEM_DISPLAY_VIZ_ADDR = 0x804DDA70
RECV_ITEM_NAME_ADDR = 0x804DE528
RECV_ITEM_LOC_ADDR = 0x804DE550
RECV_ITEM_SENDER_ADDR = 0x804DE570
RECV_MAX_STRING_LENGTH = 24
RECV_LINE_STRING_LENGTH = 26
FRAME_AVG_COUNT = 30

# This is the flag address we use to determine if Luigi is currently in an Event.
# If this flag is on, do NOT send any items / receive them.
EVENT_FLAG_RECV_ADDRR = 0x803D33B1

# This address will monitor when you capture the final boss, King Boo
KING_BOO_ADDR = 0x803D5DBF

# This address is used to deal with the current display for Captured Boos
BOO_COUNTER_DISPLAY_ADDR = 0x803A3CC4
BOO_COUNTER_DISPLAY_OFFSET = 0x77

# These addresses and bits are used to turn on flags for Boo Count related events.
# BOO_WASHROOM_FLAG_ADDR = 0x803D339C
# BOO_WASHROOM_FLAG_BIT = 4
BOO_BALCONY_FLAG_ADDR = 0x803D3399
BOO_BALCONY_FLAG_BIT = 2
BOO_FINAL_FLAG_ADDR = 0x803D33A2
BOO_FINAL_FLAG_BIT = 5


def read_short(console_address: int):
    return int.from_bytes(dme.read_bytes(console_address, 2))


def write_short(console_address: int, value: int):
    dme.write_bytes(console_address, value.to_bytes(2))


def read_string(console_address: int, strlen: int):
    return byte_string_strip_null_terminator(dme.read_bytes(console_address, strlen))


def check_if_addr_is_pointer(addr: int):
    return 2147483648 <= dme.read_word(addr) <= 2172649471


async def write_bytes_and_validate(addr: int, ram_offset: list[str] | None, curr_value: bytes) -> None:
    if not ram_offset:
        dme.write_bytes(addr, curr_value)
    else:
        dme.write_bytes(dme.follow_pointers(addr, ram_offset), curr_value)


class LMCommandProcessor(EnergyLinkCommandProcessor):
    def _cmd_dolphin(self):
        """Prints the current Dolphin status to the client."""
        if isinstance(self.ctx, LMContext):
            logger.info(f"Dolphin Status: {self.ctx.dolphin_status}")

    def _cmd_deathlink(self):
        """Toggle deathlink from client. Overrides default setting."""
        if isinstance(self.ctx, LMContext):
            Utils.async_start(self.ctx.network_engine.update_tags_async(not "DeathLink" in self.ctx.tags,
                "DeathLink"), name="Update Deathlink")

    def _cmd_jakeasked(self):
        """Provide debug information from Dolphin's RAM addresses while playing Luigi's Mansion,
        if the devs ask for it."""
        if isinstance(self.ctx, LMContext):
            Utils.async_start(self.ctx.get_debug_info(), name="Get Luigi's Mansion Debug info")

    def _cmd_change_dolphin_process_name(self, process_name: str):
        """Specify the name of the Dolphin process to connect to. "" for system default."""
        self.ctx.hook_check = False
        self.ctx.hook_name = process_name
        logger.info(f"Changing Dolphin process name to: {process_name if process_name else ""}")
        lm_settings.dolphin_process_name = DolphinProcessName(process_name)
        get_settings().save()
        log_msg: str = f"Dolphin process name set to {process_name or "default"}. You must open a new client for this to take effect."
        logger.info(log_msg)
        Utils.messagebox("Close LM Client to take effect", log_msg)

class LMContext(BaseContext):
    command_processor = LMCommandProcessor
    game = RANDOMIZER_NAME
    items_handling = 0b111

    def __init__(self, server_address, password):
        """
        Initialize the LM context.

        :param server_address: Address of the Archipelago server.
        :param password: Password for server authentication.
        """
        super().__init__(server_address, password)

        # Handle various Dolphin connection related tasks
        self.instance_id = None
        self.dolphin_sync_task: Optional[asyncio.Task[None]] = None
        self.rom_loaded = False
        self.password_required = False
        self.dolphin_status = CONNECTION_INITIAL_STATUS

        # All used when death link is enabled.
        self.is_luigi_dead = False
        self.last_health_checked = time.time()

        # Value for Luigi's max health and starting location
        self.luigimaxhp = 100
        self.spawn = "Foyer"

        # Track if the user has pickup animations turned on.
        self.pickup_anim_on = False

        # Used for handling received items to the client.
        self.already_mentioned_rank_diff = False
        self.game_clear = False
        self.last_not_ingame = time.time()
        self.boosanity = False
        #self.boo_washroom_count = None
        self.boo_balcony_count = None
        self.boo_final_count = None
        self.arg_seed = ""

        # Used for handling various weird item checks.
        self.last_map_id = 0

        # Used to let poptracker autotrack Luigi's room
        self.last_room_id = 0

        # Filters in-game messaging to what the user desires.
        self.self_item_messages = 0

        # Know whether to send in-game hints to the multiworld or not
        self.send_hints: int = 0
        self.portrait_hints: int = 0
        self.hints = {}

        # Boolossus difficulty
        self.boolossus_difficulty: int = 1

        # Last received index to track locally in the client
        self.last_received_idx: int = 0
        self.non_save_last_recv_idx: int = 0

        # Dictionary of Dynamic RAM address that change for
        self.lm_dynamic_addr: LMDynamicAddresses = LMDynamicAddresses()
        self.lm_dynamic_addr.update_item_addresses()

        # Useful for displaying various in-game messages
        self.display_class = LMDisplayQueue(self)

    async def disconnect(self, allow_autoreconnect: bool = False):
        """
        Disconnect the client from the server and reset game state variables.

        :param allow_autoreconnect: Allow the client to auto-reconnect to the server. Defaults to `False`.

        """
        await super().disconnect(allow_autoreconnect)
        self.auth = None
        dme.un_hook()
        self.dolphin_status = CONNECTION_LOST_STATUS
        self.already_fired_events = False
        self.rom_loaded = False

    def on_package(self, cmd: str, args: dict):
        """
        Handle incoming packages from the server.

        :param cmd: The command received from the server.
        :param args: The command arguments.
        """
        super().on_package(cmd, args)
        match cmd:
            case "PrintJSON":
                if args.get("type", "") == "Countdown" and len(list(args.get("data", []))) > 0 and \
                    "starting countdown of " in args["data"][0]["text"].lower():

                    countdown_var: int = int(re.search(r"\d+", args["data"][0]["text"]).group())
                    print(str(countdown_var))

            case "Connected": # On Connect
                super().on_connected(args)
                slot_data = args["slot_data"]
                # Make sure the world version matches
                if not slot_data["apworld version"] == CLIENT_VERSION:
                    local_version = str(slot_data["apworld version"]) if (
                        str(slot_data["apworld version"])) else "N/A"
                    raise Utils.VersionException(f"Error! Server was generated with a different {RANDOMIZER_NAME} " +
                        f"APWorld version.\nThe client version is {CLIENT_VERSION}!\nPlease verify you are using the " +
                        f"same APWorld as the generator, which is '{local_version}'")

                self.arg_seed = str(slot_data["seed"])
                self.boosanity = bool(slot_data["boosanity"])
                self.pickup_anim_on = bool(slot_data["pickup animation"])
                self.wallet.rank_requirement = int(slot_data["rank requirement"])
                #self.boo_washroom_count = int(slot_data["washroom boo count"])
                self.boo_balcony_count = int(slot_data["balcony boo count"])
                self.boo_final_count = int(slot_data["final boo count"])
                self.luigimaxhp = int(slot_data["luigi max health"])
                self.spawn = str(slot_data["spawn_region"])
                self.boolossus_difficulty = int(slot_data["boolossus_difficulty"])
                self.send_hints = bool(slot_data["send_hints"])

                # Update Tags for relevant links
                Utils.async_start(self.network_engine.update_tags_async(bool(slot_data[EnergyLinkConstants.INTERNAL_NAME]),
                    EnergyLinkConstants.FRIENDLY_NAME), name=f"Update {EnergyLinkConstants.FRIENDLY_NAME}")
                Utils.async_start(self.network_engine.update_tags_async(bool(slot_data["death_link"]),
                    "DeathLink"), name="Update Deathlink")

                # Fire off all the non_essential tasks here.
                Utils.async_start(self.non_essentials_async_tasks(), "LM Non-Essential Tasks")
                Utils.async_start(self.display_class.display_in_game(), "LM - Display Items in Game")
                self.ring_link.reset_ringlink()

                # Update the Text for Caught/Received Boos based on boosanity enabled.
                if not self.boosanity:
                    self.ui.important_labels["Boos"].text = "Caught Boos"
                else:
                    self.ui.important_labels["Boos"].text = "Received Boos"

                # Lastly Update the Client tab with details of the Balcony Boo Count / King Boo
                self.ui.update_king_boo_label(self.boo_final_count)
                self.ui.update_balcony_boo_label(self.boo_balcony_count)

            case "Bounced":
                if not (self.check_ingame() and self.check_alive()):
                    return

                if "tags" not in args:
                    return
                if not hasattr(self, "instance_id"):
                    self.instance_id = time.time()
                self.trap_link.on_bounced(args, self.get_item_count_by_id(8148))
                self.ring_link.on_bounced(args)

            case "SetReply":
                if not (self.check_ingame() and self.check_alive()):
                    return

                self.energy_link.try_update_energy_request(args)

            case "ConnectionRefused":
                self.dolphin_status = AP_REFUSED_STATUS
                logger.error(self.dolphin_status)

            case "RoomInfo":
                self.password_required = bool(args['password'])

    async def server_auth(self, password_requested: bool = False):
        """
        Authenticate with the Archipelago server. This function will be called as part of the init RoomInfo call
        in CommonClient, however we will exit if the rom is not loaded yet.

        :param password_requested: Whether the server requires a password. Defaults to `False`.
        """
        if not self.rom_loaded:
            logger.info("ROM is not loaded yet, waiting for dolphin to be connected before trying again.")
            return

        if password_requested and not self.password:
            logger.info('Enter the password required to join this game:')
            self.password = await self.console_input()
        await self.send_connect()

    def on_deathlink(self, data: dict[str, Any]):
        """
        Handle a DeathLink event.

        :param data: The data associated with the DeathLink event.
        """
        super().on_deathlink(data)
        self.is_luigi_dead = True
        self.set_luigi_dead()
        return

    def get_luigi_health(self) -> int:
        return read_short(dme.follow_pointers(CURR_HEALTH_ADDR, [CURR_HEALTH_OFFSET]))

    def check_alive(self):
        # Our health gets messed up in the Lab, so we can just ignore that location altogether.
        if dme.read_word(CURR_MAP_ID_ADDR) == 1:
            return True

        if self.get_luigi_health() > 0:
            self.last_health_checked = time.time()
            self.is_luigi_dead = False
            return True

        self.last_health_checked = time.time()
        return False

    def check_ingame(self):
        # The game has an address that lets us know if we are in a playable state or not.
        # This isn't perfect indicator however as although the game says ready, we still map be loading in,
        # warping around, etc.
        int_play_state = dme.read_word(CURR_PLAY_STATE_ADDR)
        if not int_play_state == 2:
            self.ring_link.reset_ringlink()
            self.last_not_ingame = time.time()
            return False

        curr_map_id = dme.read_word(CURR_MAP_ID_ADDR)

        # This checks for if we warped to another boss arena, which resets our health, so we need a slight delay.
        if curr_map_id != self.last_map_id:
            self.last_map_id = curr_map_id
            self.last_not_ingame = time.time()
            self.already_mentioned_rank_diff = False
            Utils.async_start(self.lm_update_non_savable_ram(), "LM - Update Non-Saveable RAM - Map Change")
            Utils.async_start(self.give_progression_again(), "LM - Give Progression Items")
            return False

        # These are the only valid maps we want Luigi to have checks with or do health detection with.
        # Map 2 is main mansion, 3 is the training room, 6 is the gallery, 9 is final boss (King Boo)
        # 11 is the boolossus arena, and 13 is bogmire's arena.
        if curr_map_id in (2, 3, 6, 9, 10, 11, 13):
            if not time.time() > (self.last_not_ingame + (CHECKS_WAIT*LONGER_MODIFIER)):
                return False

            # Even though this is the main mansion map, if the map is unloaded for any reason, there won't be a valid
            # room id, therefore we should not perform any checks yet.
            if curr_map_id == 2:
                bool_loaded_in_map = check_if_addr_is_pointer(ROOM_ID_ADDR)
                if bool_loaded_in_map:
                    current_room_id = dme.read_word(dme.follow_pointers(ROOM_ID_ADDR, [ROOM_ID_OFFSET]))
                    if current_room_id != self.last_room_id:
                        Utils.async_start(self.send_msgs([{
                            "cmd": "Set",
                            "key": f"lm_room_{self.team}_{self.slot}",
                            "default": 0,
                            "want_reply": False,
                            "operations": [{"operation": "replace", "value": current_room_id}]
                        }]), name="Update Luigi Mansion Room ID")
                        self.last_room_id = current_room_id
                        Utils.async_start(self.lm_update_non_savable_ram(), "LM - Update Non-Saveable RAM - Room Change")
                return bool_loaded_in_map
            elif curr_map_id == 3:
                curr_val = dme.read_byte(MEMORY_CONSTANTS.TRAINING_BUTTON_LAYOUT_SCREEN)
                if (curr_val & (1 << 0)) > 0:
                    Utils.async_start(self.lm_update_non_savable_ram(), "LM - Update Non-Saveable RAM - Training Room")
            return True

        self.last_not_ingame = time.time()
        return False

    def set_luigi_dead(self):
        write_short(dme.follow_pointers(CURR_HEALTH_ADDR, [CURR_HEALTH_OFFSET]), 0)
        return

    async def get_debug_info(self):
        if not (dme.is_hooked() and self.dolphin_status == CONNECTION_CONNECTED_STATUS) or not self.check_ingame():
            logger.info(f"Unable to use this command until you are in a {RANDOMIZER_NAME} ROM, loaded and connected.")
            return

        flag_addr_start = 0x803D3399
        for flag_addr_index in range(0, 32):
            current_flag_num = flag_addr_index*8
            curr_val = dme.read_byte(flag_addr_start + flag_addr_index)

            for flag_bit in range(0,8):
                flag_val = "True" if (curr_val & (1 << flag_bit)) > 0 else "False"
                logger.info("Flag #" + str(current_flag_num+flag_bit) + " is set to: " + flag_val)
        return

    def check_ram_location(self, loc_data, addr_to_update, curr_map_id, map_to_check) -> bool:
        """
        Checks a provided location in ram to see if the location was interacted with. This includes
        furniture, plants, entering rooms, etc.

        It should be noted that although reading 800 bytes in RAM is preferable for furniture, it actually has a lot
        of pointers and instead will cause just as many reads to dynamically get bulk data if not more than it would to
        just read data 4 bytes at a time. For context, it's a static address + the current offset, then you add
        either the furniture id offset or the flag offset to get the furniture id, and it's value respectively.
        """
        match loc_data.type:
            case "Furniture" | "Plant":
                # Check all possible furniture addresses.
                for current_offset in range(0, FURNITURE_ADDR_COUNT, 4):
                    # Only check if the current address is a pointer
                    current_addr = FURNITURE_MAIN_TABLE_ID + current_offset
                    if not check_if_addr_is_pointer(current_addr):
                        continue

                    furn_id = dme.read_word(dme.follow_pointers(current_addr, [FURN_ID_OFFSET]))
                    if not furn_id == loc_data.jmpentry:
                        continue

                    furn_flag = dme.read_word(dme.follow_pointers(current_addr, [FURN_FLAG_OFFSET]))
                    if furn_flag > 0:
                        return True
            case "Map":
                if curr_map_id in map_to_check:
                    return True
            case _:
                byte_size = 1 if addr_to_update.ram_byte_size is None else addr_to_update.ram_byte_size
                if not addr_to_update.pointer_offset is None:
                    curr_val = int.from_bytes(dme.read_bytes(dme.follow_pointers(addr_to_update.ram_addr,
                        [addr_to_update.pointer_offset]), byte_size))
                    if (curr_val & (1 << addr_to_update.bit_position)) > 0:
                        return True
                else:
                    curr_val = int.from_bytes(dme.read_bytes(addr_to_update.ram_addr, byte_size))
                    if (curr_val & (1 << addr_to_update.bit_position)) > 0:
                        return True
        return False

    async def lm_check_locations(self):
        # There will be different checks on different maps.
        current_map_id: int = dme.read_word(CURR_MAP_ID_ADDR)
        current_room_id: int = 0
        if current_map_id in [2,6]: # Check if we're in the Mansion or the Gallery
            current_room_id = dme.read_word(dme.follow_pointers(ROOM_ID_ADDR, [ROOM_ID_OFFSET]))

        local_missing_locs = copy.deepcopy(self.missing_locations)
        for mis_loc in local_missing_locs:
            local_loc = self.location_names.lookup_in_game(mis_loc)
            lm_loc_data = ALL_LOCATION_TABLE[local_loc]
            if current_map_id not in lm_loc_data.map_id:
                continue

            # Some locations, like Gold Portraits require multiple RAM address to be true simultaneously. Keep track of
            # all of these booleans in a list and check if all true to send the check.
            all_true_list: list[bool] = []

            # This only checks if one address in the ram list is true, not all, so any location in the list can be true
            #   to consider the location as "checked"
            for loc_addr in lm_loc_data.update_ram_addr:
                # If in main mansion map
                if current_map_id == 2:
                    # If special moving Toad, room_to_check should be the spawn room id
                    if lm_loc_data.code == 617:
                        room_to_check: int = REGION_LIST[self.spawn].in_game_room_id
                    else:
                        room_to_check = loc_addr.in_game_room_id if not loc_addr.in_game_room_id is None else current_room_id
                    if not room_to_check == current_room_id:
                        continue

                if lm_loc_data.all_true:
                    all_true_list.append(self.check_ram_location(lm_loc_data, loc_addr, current_map_id, lm_loc_data.map_id))
                    continue

                if self.check_ram_location(lm_loc_data, loc_addr, current_map_id, lm_loc_data.map_id):
                    self.locations_checked.add(mis_loc)
                    break

            if lm_loc_data.all_true:
                if all(loc_true for loc_true in all_true_list):
                    self.locations_checked.add(mis_loc)

        await self.check_locations(self.locations_checked)

        # If on final boss with King Boo
        if current_map_id == 9:
            beat_king_boo = dme.read_byte(KING_BOO_ADDR)
            if (beat_king_boo & (1 << 5)) > 0 and not self.game_clear:
                if self.wallet.check_rank_requirement():
                    self.game_clear = True
                else:
                    if not self.already_mentioned_rank_diff:
                        logger.info("Unfortunately, you do NOT have enough money to satisfy the rank" +
                                f"requirements.\nYou are missing: '{(self.wallet.get_rank_requirement() - self.wallet.get_wallet_worth()):,}'")
                        self.already_mentioned_rank_diff = True

        if not self.finished_game and self.game_clear:
            logger.info("Congratulations on completing LM Rando! You completed " + "{:.2f}".format(
                (len(self.checked_locations) / len(self.server_locations)) * 100)+"% of the total checks")
            self.finished_game = True
            await self.send_msgs([{
                "cmd": "StatusUpdate",
                "status": NetUtils.ClientStatus.CLIENT_GOAL,
            }])
        return

    def get_item_count_by_id(self, item_id: int) -> int:
        return len([netItem for netItem in self.items_received if netItem.item == item_id])

    # Through god knows how many hours of debugging, we have figured out that LM will change bytes due to certain
    # Events in game, however it is currently unknown when they trigger and the average user does not know how to
    # debug breakpoints in Dolphin. Instead, just give all the progressive items again and be done with it.
    async def give_progression_again(self):
        progressive_items: dict[str, LMItemData] = {**ITEM_TABLE}

        try:
            for (key, val) in progressive_items.items():
                if key in ["Vacuum Upgrade", "Gold Diamond", "Progressive Flower", "Poltergust 3000"] or \
                    LMItem.get_apid(val.code) not in self.items_received:
                    continue

                for addr_to_update in val.update_ram_addr:
                    byte_size = 1 if addr_to_update.ram_byte_size is None else addr_to_update.ram_byte_size
                    ram_offset = None
                    if addr_to_update.pointer_offset:
                        ram_offset = [addr_to_update.pointer_offset]

                    if not addr_to_update.pointer_offset is None:
                        curr_val = int.from_bytes(dme.read_bytes(dme.follow_pointers(addr_to_update.ram_addr,
                            [addr_to_update.pointer_offset]), byte_size))
                    else:
                        curr_val = int.from_bytes(dme.read_bytes(addr_to_update.ram_addr, byte_size))

                    curr_val = (curr_val | (1 << addr_to_update.bit_position))
                    await write_bytes_and_validate(addr_to_update.ram_addr, ram_offset, curr_val.to_bytes(byte_size, 'big'))
        except Exception as genericEx:
            logger.error("Unable to give progression items as expected due to an error. Details: " + str(genericEx))

        return

    # TODO Review these loops as something could be skipped over.
    async def give_lm_items(self):
        last_recv_idx = dme.read_word(LAST_RECV_ITEM_ADDR)
        if len(self.items_received) == last_recv_idx:
            return

        self.last_received_idx = last_recv_idx
        self.non_save_last_recv_idx = dme.read_word(NON_SAVE_LAST_RECV_ITEM_ADDR)
        recv_items = self.items_received[last_recv_idx:]
        for item in recv_items:
            last_recv_idx += 1
            lm_item_name = self.item_names.lookup_in_game(item.item)
            lm_item = ALL_ITEMS_TABLE[lm_item_name]

            # Add the item to the display items queue to display when it can
            if self.self_item_messages == 0:
                self.display_class.items_received.append(item)
            elif self.self_item_messages == 1 and lm_item.classification == IC.progression:
                self.display_class.items_received.append(item)

            # If the user is subscribed to send items and the trap is a valid trap and the trap was not already
            # received (to prevent sending the same traps over and over to other TrapLinkers if Luigi died)
            if self.trap_link.is_enabled() and item.item in trap_id_list and last_recv_idx > self.non_save_last_recv_idx:
                await self.trap_link.send_trap_link_async(lm_item_name)

            # Filter for only items where we have not received yet. If same slot, only receive locations from pre-set
            # list of locations, otherwise accept other slots. Additionally accept only items from a pre-approved list.
            if item.item in RECV_ITEMS_IGNORE or (item.player == self.slot and not
            (item.location in SELF_LOCATIONS_TO_RECV or item.item in RECV_OWN_GAME_ITEMS or item.location < 0)):
                self.update_received_idx(last_recv_idx)
                continue

            # Sends remote currency items from the server to the client.
            if lm_item.type == "Money":
                currency_receiver = CurrencyReceiver(self.wallet)
                currency_receiver.send_to_wallet(lm_item)
                self.update_received_idx(last_recv_idx)
                continue
            elif lm_item.type == "Trap" and (self.non_save_last_recv_idx >= last_recv_idx or
                (item.item == 8147 and self.get_item_count_by_id(8148) < 1) or
                (lm_item_name == "Ghost" and self.last_map_id != 2)): # TODO Remove when either ghost trap stop dropping hearts or another workaround to do.
                # Skip this trap item to avoid Luigi dying in an infinite trap loop.
                # Also skip No Vac Trap if we don't have a vacuum
                self.update_received_idx(last_recv_idx)
                continue

            for addr_to_update in lm_item.update_ram_addr:
                byte_size = 1 if addr_to_update.ram_byte_size is None else addr_to_update.ram_byte_size
                ram_offset = None if not addr_to_update.pointer_offset else [addr_to_update.pointer_offset]

                if item.item in trap_id_list:
                    curr_val = addr_to_update.item_count
                elif item.item == 8140:  # Progressive Flower, 00EB, 00EC, 00ED
                    flower_count: int = self.get_item_count_by_id(8140)
                    curr_val = min(flower_count + 234, 237)
                    ram_offset = None
                elif item.item == 8064:  # If it's a vacuum upgrade
                    curr_val: int = min(self.get_item_count_by_id(8064), 5)
                    ram_offset = None
                elif not addr_to_update.item_count is None:
                    if not ram_offset is None:
                        curr_val = int.from_bytes(dme.read_bytes(dme.follow_pointers(addr_to_update.ram_addr,
                            [addr_to_update.pointer_offset]), byte_size))
                        if item.item in HEALTH_RELATED_ITEMS:
                            curr_val = min(curr_val + addr_to_update.item_count, self.luigimaxhp)
                        else:
                            curr_val += addr_to_update.item_count
                    else:
                        curr_val = int.from_bytes(dme.read_bytes(addr_to_update.ram_addr, byte_size))
                        curr_val += addr_to_update.item_count
                else:
                    if not addr_to_update.pointer_offset is None:
                        curr_val = int.from_bytes(dme.read_bytes(dme.follow_pointers(addr_to_update.ram_addr,
                            [addr_to_update.pointer_offset]), byte_size))
                        curr_val = (curr_val | (1 << addr_to_update.bit_position))
                    else:
                        curr_val = int.from_bytes(dme.read_bytes(addr_to_update.ram_addr, byte_size))
                        if not addr_to_update.bit_position is None:
                            curr_val = (curr_val | (1 << addr_to_update.bit_position))
                        else:
                            curr_val += 1

                await write_bytes_and_validate(addr_to_update.ram_addr, ram_offset, curr_val.to_bytes(byte_size, 'big'))

            # Update the last received index to ensure we don't receive the same item over and over.
            self.update_received_idx(last_recv_idx)
            await self.wait_for_next_loop(0.5)

    def update_received_idx(self, last_recv_idx: int):
        self.last_received_idx = last_recv_idx
        dme.write_word(LAST_RECV_ITEM_ADDR, last_recv_idx)

        # Lastly, update the non-saveable received index with the current last received index.
        if last_recv_idx > self.non_save_last_recv_idx:
            self.non_save_last_recv_idx = last_recv_idx
            dme.write_word(NON_SAVE_LAST_RECV_ITEM_ADDR, last_recv_idx)

    async def lm_update_non_savable_ram(self):
        try:
            # Get the dynamic changing address dict first.
            dynamic_addr: dict = self.lm_dynamic_addr.dynamic_addresses

            # Always adjust the Vacuum speed as saving and quitting or going to E. Gadds lab could reset it back to normal.
            vac_count = self.get_item_count_by_id(8148)
            vac_speed = min(self.get_item_count_by_id(8064), 5)

            vac_timer_addr: int = int(dynamic_addr["Client"]["Player_Weapon_Trap_Timer"], 16)
            if not self.trap_link.check_vac_trap_active(vac_timer_addr) and vac_count > 0:
                for item in [8064, 8148]:
                    lm_item_name = self.item_names.lookup_in_game(item)
                    lm_item = ALL_ITEMS_TABLE[lm_item_name]
                    for update_addr in lm_item.update_ram_addr:
                        if lm_item_name == "Poltergust 3000" and vac_count > 0:  # If we're checking against our vacuum-on address
                            curr_val = 1
                            dme.write_bytes(update_addr.ram_addr, curr_val.to_bytes(update_addr.ram_byte_size, 'big'))
                            vacc_flag = dme.read_byte(0x803D33A3) # Read and set flag 82
                            vacc_flag = (vacc_flag | (1 << 2))
                            dme.write_byte(0x803D33A3, vacc_flag)
                        else:
                            dme.write_bytes(update_addr.ram_addr, vac_speed.to_bytes(update_addr.ram_byte_size, 'big'))

            # Always adjust Pickup animation issues if the user turned pick up animations off.
            if not self.pickup_anim_on:
                crown_helper_val = "00000001"
                pickup_addr: int = int(dynamic_addr["Client"]["Play_King_Boo_Gem_Fast_Pickup"], 16)
                dme.write_bytes(pickup_addr, bytes.fromhex(crown_helper_val))

            # Always update Boolossus difficulty
            boolossus_diff_addr: int = int(dynamic_addr["Client"]["Boolossus_Mini_Boo_Difficulty"], 16)
            dme.write_bytes(boolossus_diff_addr, self.boolossus_difficulty.to_bytes(4,'big'))

            # Always update the flower to have the correct amount of flowers in game
            flower_recv: int = self.get_item_count_by_id(8140)
            flower_count = min(flower_recv + 234, 237)
            flower_item = self.item_names.lookup_in_game(8140)
            flower_item_data = ALL_ITEMS_TABLE[flower_item]
            for flwr_addr in flower_item_data.update_ram_addr:
                dme.write_bytes(flwr_addr.ram_addr, flower_count.to_bytes(flwr_addr.ram_byte_size, 'big'))

            # Always update the gold diamond count to have the correct amount of diamonds in game
            diamond_recv: int = self.get_item_count_by_id(8065)
            diamond_item = self.item_names.lookup_in_game(8065)
            diamond_item_data = ALL_ITEMS_TABLE[diamond_item]
            for diam_addr_update in diamond_item_data.update_ram_addr:
                dme.write_bytes(diam_addr_update.ram_addr, diamond_recv.to_bytes(diam_addr_update.ram_byte_size, 'big'))

            # Make it so the displayed Boo counter always appears even if you don't have boo radar or if you haven't caught
            # a boo in-game yet.
            if self.boosanity:
                # This allows the in-game display to work correctly.
                dme.write_bytes(0x803D5E0B, bytes.fromhex("01"))

                # Update the in-game counter to reflect how many boos you got.
                boo_received_list = [item.item for item in self.items_received if item.item in BOO_AP_ID_LIST]

                for boo_item in boo_received_list:
                    lm_item_name = self.item_names.lookup_in_game(boo_item)
                    lm_item = ALL_ITEMS_TABLE[lm_item_name]
                    for addr_to_update in lm_item.update_ram_addr:
                        curr_val = dme.read_byte(addr_to_update.ram_addr)
                        curr_val = (curr_val | (1 << addr_to_update.bit_position))
                        dme.write_byte(addr_to_update.ram_addr, curr_val)

                curr_boo_count = len(set(boo_received_list))
                if curr_boo_count >= self.boo_balcony_count:
                    boo_val = dme.read_byte(BOO_BALCONY_FLAG_ADDR)
                    dme.write_byte(BOO_BALCONY_FLAG_ADDR, (boo_val | (1 << BOO_BALCONY_FLAG_BIT)))
                if curr_boo_count >= self.boo_final_count:
                    boo_val = dme.read_byte(BOO_FINAL_FLAG_ADDR)
                    dme.write_byte(BOO_FINAL_FLAG_ADDR, (boo_val | (1 << BOO_FINAL_FLAG_BIT)))
        except Exception as genericEx:
            logger.error("Unable to update the non-saveable ram as expected due to an error. Details: " + str(genericEx))

        return

    async def check_death(self):
        if self.is_luigi_dead or self.get_luigi_health() > 0:
            return

        # If this is 0 and our health is 0, it means are health address pointer could have changed
        # between using a mouse hole or teleporting to a new map, so Luigi may not actually be dead.
        death_screen_check: int = dme.read_byte(CHECK_DEATH_ACTIVE)
        if death_screen_check > 0x20:
            return

        if not self.is_luigi_dead and time.time() >= float(self.last_death_link + (CHECKS_WAIT * LONGER_MODIFIER * 3)):
            self.is_luigi_dead = True
            self.set_luigi_dead()
            await self.send_death(self.player_names[self.slot] + " scared themselves to death.")

    async def manage_wallet_async(self):
        try:
            while self.slot:
                if not (self.check_ingame() and self.check_alive()):
                    await self.wait_for_next_loop(0.5)
                    continue

                await self.wait_for_next_loop(0.5)
        except Exception as generic_ex:
            logger.error("Critical error with watching currencies async tasks. Details: " + str(generic_ex))

    async def non_essentials_async_tasks(self):
        try:
            while self.slot:
                if not self.check_ingame():
                    await self.wait_for_next_loop(0.5)
                    continue

                # Since DeathLink has to check in_game separately but not health, we will do this outside of
                # the below statements
                if "DeathLink" in self.tags:
                    await self.check_death()

                if not self.check_alive():
                    await self.wait_for_next_loop(0.5)
                    # Resets the logic for determining the currency differences,
                    # needs to be updated to reset inside of wallet_manager.
                    # self.ring_link.reset_ringlink()
                    continue

                if self.trap_link.is_enabled():
                    await self.trap_link.handle_traplink_async()
                if self.ring_link.is_enabled():
                    await self.handle_ringlink_async()

                # Async thread related tasks
                if self.send_hints:
                    await self.lm_send_hints()
                if self.call_mario:
                    await self.check_mario_yell()

                await self.wait_for_next_loop(0.5)
        except Exception as genericEx:
            logger.error("Critical error while running non-essential async tasks. Details: " + str(genericEx))

    async def dolphin_sync_main_task(self):
        logger.info(f"Using {RANDOMIZER_NAME} client {CLIENT_VERSION}")
        logger.info("Starting Dolphin connector. Use /dolphin for status information.")

        try:
            while not self.exit_event.is_set():
                try:
                    # If DME is not already hooked or connected in any way
                    if not dme.is_hooked():
                        dme.hook()
                        if dme.get_status() == dme.get_status().noEmu or dme.get_status() == dme.get_status().notRunning:
                            dme.un_hook()
                            self.dolphin_status = CONNECTION_INITIAL_STATUS
                            logger.info(self.dolphin_status)
                            await self.wait_for_next_loop(WAIT_TIMER_LONG_TIMEOUT)
                            continue

                    if not self.dolphin_status == CONNECTION_CONNECTED_STATUS:
                        # Check if Game ID is 0, which means something failed to load for Dolphin for some reason.
                        game_id_bytes: bytes = dme.read_bytes(0x80000000, 20)
                        if int.from_bytes(game_id_bytes, "big") == 0:
                            logger.info(DOLPHIN_DIDNT_LOAD_ROM_CORRECTLY)
                            self.dolphin_status = DOLPHIN_DIDNT_LOAD_ROM_CORRECTLY
                            dme.un_hook()
                            await self.wait_for_next_loop(WAIT_TIMER_LONG_TIMEOUT)
                            continue

                        # If the Game ID is a standard one, the randomized ISO has not been loaded - so disconnect
                        game_id = byte_string_strip_null_terminator(game_id_bytes)
                        if game_id in LM_GC_IDs:
                            logger.info(CONNECTION_REFUSED_STATUS)
                            self.dolphin_status = CONNECTION_REFUSED_STATUS
                            dme.un_hook()
                            await self.wait_for_next_loop(WAIT_TIMER_LONG_TIMEOUT)
                            continue

                        # If we are not connected to server, check for player name in RAM address
                        if not self.auth:
                            self.auth = read_string(SLOT_NAME_ADDR, SLOT_NAME_STR_LENGTH)

                            # If no player name is found, disconnect DME and inform player
                            if not self.auth:
                                self.auth = None
                                self.dolphin_status = NO_SLOT_NAME_STATUS
                                logger.info(self.dolphin_status)
                                dme.un_hook()
                                await self.wait_for_next_loop(WAIT_TIMER_LONG_TIMEOUT)
                                continue

                        # Reset the locations_checked while we wait
                        self.locations_checked = set()

                        # Inform the player we are ready and waiting for them to connect.
                        if not self.rom_loaded:
                            self.dolphin_status = CONNECTION_VERIFY_SERVER
                            logger.info(self.dolphin_status)
                            self.rom_loaded = True
                            await self.server_auth(self.password_required)

                        if not self.slot:
                            await self.wait_for_next_loop(WAIT_TIMER_LONG_TIMEOUT)
                            continue

                        arg_seed = read_string(0x80000001, len(str(self.arg_seed)))
                        if arg_seed != self.arg_seed:
                            raise Exception(
                                f"Incorrect Randomized {RANDOMIZER_NAME} ISO file selected. The seed does not match." +
                                "Please verify that you are using the right ISO/seed/APLM file.")

                        logger.info(CONNECTION_CONNECTED_STATUS)
                        self.dolphin_status = CONNECTION_CONNECTED_STATUS

                    # At this point, we are verified as connected. Update UI elements in the LMCLient tab.
                    if self.ui:
                        if self.boosanity:
                            boo_count = len(([item.item for item in self.items_received if item.item in BOO_AP_ID_LIST]))
                        else:
                            boo_count = sum(bin(byte).count('1') for byte in dme.read_bytes(0x803D5E04, 8))
                        self.ui.update_boo_count_label(boo_count)
                        self.ui.get_wallet_value()
                        self.ui.update_flower_label(self.get_item_count_by_id(8140))
                        self.ui.update_vacuum_label(self.get_item_count_by_id(8064))

                    if not (self.check_ingame() and self.check_alive()):
                        await self.wait_for_next_loop(WAIT_TIMER_SHORT_TIMEOUT)
                        # Resets the logic for determining the currency differences,
                        # needs to be updated to reset inside of wallet_manager.
                        self.ring_link.reset_ringlink()
                        continue

                    # Lastly check any locations and update the non-save able ram stuff
                    await self.lm_check_locations()
                    await self.give_lm_items()
                    await self.wait_for_next_loop(WAIT_TIMER_SHORT_TIMEOUT)
                except Exception as ex:
                    dme.un_hook()
                    logger.error(str(ex))
                    logger.info("Connection to Dolphin failed, attempting again in 5 seconds...")
                    self.dolphin_status = CONNECTION_LOST_STATUS
                    await self.disconnect()
                    await self.wait_for_next_loop(WAIT_TIMER_LONG_TIMEOUT)
                    continue
        except Exception as threadEx:
            logger.error("Something went horribly wrong with the Luigis Mansion client. Details: " + str(threadEx))


def main(*launch_args: str):
    from .client.dolphin_launcher import DolphinLauncher
    import colorama

    # DME seems to only load the environment variables value once, then after the first hook it never retrieves it again.
    # It is in our best interest to set this up first, then call hook later
    lm_settings: LuigisMansionSettings = get_settings().luigismansion_options
    if lm_settings.dolphin_process_name:
        os.environ[DME_DOLPHIN_PROCESS_NAME_ENV_VARIABLE] = lm_settings.dolphin_process_name
    elif DME_DOLPHIN_PROCESS_NAME_ENV_VARIABLE in os.environ:
        del os.environ[DME_DOLPHIN_PROCESS_NAME_ENV_VARIABLE]

    server_address: str = ""
    rom_path: str = ""

    Utils.init_logging(CLIENT_NAME)
    logger.info(f"Starting LM Client {CLIENT_VERSION}")
    dolphin_launcher: DolphinLauncher = DolphinLauncher()

    parser = get_base_parser()
    parser.add_argument('aplm_file', default="", type=str, nargs="?", help='Path to an APLM file')
    args = parser.parse_args(launch_args)

    if args.aplm_file:
        lm_usa_patch = LMUSAAPPatch()
        try:
            lm_usa_manifest = lm_usa_patch.read_contents(args.aplm_file)
            server_address = lm_usa_manifest["server"]
            rom_path= lm_usa_patch.patch(args.aplm_file)
        except Exception as ex:
            err_msg: str = (f"Unable to patch your {RANDOMIZER_NAME} ROM as expected.\n" +
                f"APWorld Version: '{CLIENT_VERSION}'\nAdditional details:\n") + str(ex)
            logger.error(err_msg)
            Utils.messagebox(f"Cannot Patch {RANDOMIZER_NAME}", err_msg, True)
            raise ex

    async def _main(connect, password):
        try:
            ctx = LMContext(server_address if server_address else connect, password)
            ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")

            # Runs Universal Tracker's internal generator
            ctx._main()

            if gui_enabled:
                ctx.run_gui()
            ctx.run_cli()
            await ctx.wait_for_next_loop(WAIT_TIMER_LONG_TIMEOUT)

            ctx.dolphin_sync_task = asyncio.create_task(ctx.dolphin_sync_main_task(), name="DolphinSync")

            await ctx.exit_event.wait()
            await ctx.shutdown()

            if ctx.dolphin_sync_task:
                await ctx.dolphin_sync_task
        except Exception as clientEx:
            client_msg: str = (f"An unknown error occurred while running {RANDOMIZER_NAME}'s client.\n" +
                f"APWorld Version: '{CLIENT_VERSION}'\nAdditional details:\n") + str(clientEx)
            logger.error(client_msg)
            Utils.messagebox(f"Main Client Issue {RANDOMIZER_NAME}", client_msg, True)
            raise clientEx

    Utils.asyncio.run(dolphin_launcher.launch_dolphin_async(rom_path))

    colorama.just_fix_windows_console()
    asyncio.run(_main(args.connect, args.password))
    colorama.deinit()

if __name__ == "__main__":
    Utils.init_logging(CLIENT_NAME, exception_logger="Client")
    main(*sys.argv[1:])
