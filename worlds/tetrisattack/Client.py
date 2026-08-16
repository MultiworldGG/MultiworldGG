import logging
import struct
import textwrap
import typing
import time
from struct import pack

from NetUtils import ClientStatus, color
from worlds.AutoSNIClient import SNIClient
from . import item_table, location_table
from .Items import progressive_items
from .Rom import GOALS_POSITION, DEATHLINKHINT, MASKED_VERSION, SRAM_FACTOR, SCSHOCKPANELS_PER_CHECK, \
    WORLD_VERSION, STRING_DATA, STRING_DATA_SIZE
from .data.Constants import VS_CLEARS_END, CLEARED_SHOCK_PANELS, VS_CLEARS_START

if typing.TYPE_CHECKING:
    from SNIClient import SNIContext

snes_logger = logging.getLogger("SNES")

# FXPAK Pro protocol memory mapping used by SNI
ROM_START = 0x000000
WRAM_START = 0xF50000
WRAM_SIZE = 0x20000
SRAM_START = 0xE00000

TETRISATTACK_APVERSION = ROM_START + 0x007FB0
APVERSION_SIZE = 0x06
TETRISATTACK_ROMHASH_START = ROM_START + 0x007FC0
ROMHASH_SIZE = 0x15

GAME_STATE = WRAM_START + 0x02A0
STATUS_MESSAGE = WRAM_START + 0xFFB0
SNI_BAND_OFFSET = 0x400
SRAM_SNI_BAND_START = SRAM_START + SNI_BAND_OFFSET
SNI_BAND_SIZE = 0x12
SNI_RECEIVED_ITEM_NUMBER = 0x00
SNI_RECEIVED_ITEM_ID = 0x02
SNI_RECEIVED_ITEM_ACTION = 0x04
SNI_RECEIVED_ITEM_ARG = 0x06
SNI_RECEIVE_CHECK = 0x08
SNI_MESSAGE_REQUEST = 0x0A
SNI_DEATHLINK_TRIGGER = 0x0C
SNI_DEATHLINK_EVENT = 0x0E
SNI_MESSAGE_ID = 0x10
SRAM_SNI_MESSAGE = SRAM_START + 0x0412
STAGECLEARLASTSTAGE_COMPLETED = SRAM_START + location_table["Stage Clear Last Stage Clear"].code
PUZZLEL6_COMPLETED = SRAM_START + location_table["Puzzle Round 6 Clear"].code
EXTRAPUZZLEL6_COMPLETED = SRAM_START + location_table["Extra Puzzle Round 6 Clear"].code
STAGECLEARSHOCKPANEL_ID = SRAM_START + item_table["Stage Clear ! Panel Bundle"].code
VSSTAGES_COMPLETED = SRAM_START + 0x225
SRAM_AP_REGION_OFFSET = 0x020
SRAM_AP_REGION_END = pow(2, SRAM_FACTOR)
SRAM_AP_REGION_LENGTH = SRAM_AP_REGION_END - SRAM_AP_REGION_OFFSET

ACTION_CODE_NOOP = 0
ACTION_CODE_RECEIVED_ITEM = 2
ACTION_CODE_LAST_STAGE = 3
ACTION_CODE_MARK_COMPLETE = 5
ACTION_CODE_RECEIVED_SCORE = 7
ACTION_CODE_RECEIVED_SHOCK_PANELS = 10


class TetrisAttackSNIClient(SNIClient):
    game = "Tetris Attack"
    patch_suffix = ".aptatk"
    awaiting_deathlink_event = False
    currently_dead = False
    all_goals = None
    deathlink_hint = None
    shock_panels_per_check = None
    looked_through_locations = False
    string_constants = None
    time_of_version_fail = 0
    total_writes = 0

    messages_received = 0
    last_message = ""
    deathlink_message = ""
    last_stage_clear = "???"

    async def validate_rom(self, ctx: "SNIContext") -> bool:
        from SNIClient import snes_read
        from Utils import __version__

        rom_prefix = await snes_read(ctx, TETRISATTACK_APVERSION, APVERSION_SIZE)
        expected_prefix = f'ATK{__version__.replace(".", "")[0:3]}'
        prefix_bytes = bytearray(expected_prefix, 'utf8')
        if rom_prefix is None:
            return False
        rom_hash = await snes_read(ctx, TETRISATTACK_ROMHASH_START, ROMHASH_SIZE)
        expected_hash = f'{format(MASKED_VERSION, "X")}'
        hash_bytes = bytearray(expected_hash, 'utf8')
        if rom_hash is None:
            snes_logger.error(f'Failed to read ROM name hash')
            return False
        if not rom_hash.startswith(hash_bytes):
            if time.time() > self.time_of_version_fail + 20 and rom_prefix.startswith(prefix_bytes[0:3]):
                hash_string = rom_hash.decode('utf-8')
                end_pos = hash_string.find('|')
                if end_pos < 1:
                    end_pos = 1
                string_constants = await snes_read(ctx, STRING_DATA, 0x8)
                if string_constants is None:
                    snes_logger.error(
                        f'ROM patch version {hash_string[0:end_pos]} does not match expected apworld version {expected_hash}, this apworld expects seeds generated in {WORLD_VERSION}')
                else:
                    version_string = rom_hash.decode('ascii')
                    snes_logger.error(
                        f'ROM patch version {hash_string[0:end_pos]} ({version_string}) does not match expected apworld version {expected_hash} ({WORLD_VERSION}), this apworld expects seeds generated in {WORLD_VERSION}')
                self.time_of_version_fail = time.time()
            return False
        if ctx.game != self.game and not rom_prefix.startswith(prefix_bytes):
            prefix_string = rom_prefix.decode('utf-8')
            snes_logger.warning(
                f'ROM AP version {prefix_string} does not match the current instance {expected_prefix}, unexpected behavior may occur!')

        ctx.game = self.game
        ctx.items_handling = 0b111  # remote items
        ctx.rom = rom_hash

        return True

    async def deathlink_kill_player(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, DeathState
        self.awaiting_deathlink_event = True
        # TODO_AFTER: Fetch the contents of the deathlink message
        self.deathlink_message = "Received deathlink"
        snes_buffered_write(ctx, SRAM_SNI_BAND_START + SNI_DEATHLINK_EVENT, pack("H", 1))
        await snes_flush_writes(ctx)
        ctx.death_state = DeathState.dead
        ctx.last_death_link = time.time()

    async def game_watcher(self, ctx: "SNIContext") -> None:
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read

        rom = await snes_read(ctx, TETRISATTACK_ROMHASH_START, ROMHASH_SIZE)
        if rom != ctx.rom:
            snes_logger.info(f'Game was switched off, disconnecting...')
            ctx.rom = None
            self.all_goals = None
            self.deathlink_hint = None
            self.string_constants = None
            self.shock_panels_per_check = None
            self.looked_through_locations = False
            return

        if self.all_goals is None:
            self.all_goals = await snes_read(ctx, GOALS_POSITION, 0x3)
        if self.deathlink_hint is None:
            self.deathlink_hint = await snes_read(ctx, DEATHLINKHINT, 0x1)
        if self.string_constants is None:
            self.string_constants = await snes_read(ctx, STRING_DATA, STRING_DATA_SIZE)
        if self.shock_panels_per_check is None:
            self.shock_panels_per_check = await snes_read(ctx, SCSHOCKPANELS_PER_CHECK, 0x1)
        if not ctx.slot:
            return

        # Initial conditions are good, let's interact
        if "Deathlink" not in ctx.tags:
            if self.deathlink_hint is not None and self.deathlink_hint[0] != 0:
                await ctx.update_death_link(True)

        # Grab the entire Archipelago SRAM region
        sram_bytes = await snes_read(ctx, SRAM_START + SRAM_AP_REGION_OFFSET, SRAM_AP_REGION_LENGTH + SNI_BAND_SIZE)
        if sram_bytes is None:
            snes_logger.error(f'Failed to read SRAM')
            return
        sni_16_bit_data = struct.unpack("9H", sram_bytes[SNI_BAND_OFFSET - SRAM_AP_REGION_OFFSET:])

        # Check if topped out or ran out of moves
        if "DeathLink" in ctx.tags and ctx.last_death_link + 1 < time.time():
            game_state = await snes_read(ctx, GAME_STATE, 0x1)
            if game_state is not None:
                deathlink_trigger = sni_16_bit_data[SNI_DEATHLINK_TRIGGER >> 1]
                if deathlink_trigger > 0:
                    if self.awaiting_deathlink_event:
                        self.awaiting_deathlink_event = False
                    else:
                        self.deathlink_message = get_deathlink_message(ctx.player_names[ctx.slot], deathlink_trigger)
                    self.currently_dead = True
                    ctx.last_death_link = time.time()
                    snes_buffered_write(ctx, SRAM_SNI_BAND_START + SNI_DEATHLINK_TRIGGER, pack("H", 0))
                elif game_state[0] != 5:
                    self.currently_dead = False
                if not self.awaiting_deathlink_event:
                    await ctx.handle_deathlink_state(self.currently_dead, self.deathlink_message)

        # Check if game is ready to receive
        if sni_16_bit_data[SNI_RECEIVED_ITEM_ACTION >> 1] > 0x00:
            return
        received_item_count = sni_16_bit_data[SNI_RECEIVED_ITEM_NUMBER >> 1]
        receive_check = sni_16_bit_data[SNI_RECEIVE_CHECK >> 1]
        if receive_check < received_item_count < 32768:
            return

        # Look through goal checks
        if not ctx.finished_game:
            goals_met = False
            if self.all_goals is not None:
                goals_met = True
                if self.all_goals[0] != 0:
                    sc_last_stage_clear = sram_bytes[
                        STAGECLEARLASTSTAGE_COMPLETED % SRAM_AP_REGION_END - SRAM_AP_REGION_OFFSET]
                    if (sc_last_stage_clear & (1 << 6)) == 0:
                        goals_met = False
                    else:
                        sc_last_stage_clear = sram_bytes[
                            (STAGECLEARLASTSTAGE_COMPLETED + 0x101) % SRAM_AP_REGION_END - SRAM_AP_REGION_OFFSET]
                        if (sc_last_stage_clear & (1 << 6)) == 0:
                            goals_met = False
                puzzle_goaled = True
                extra_goaled = True
                if (self.all_goals[1] & 1) != 0:
                    pz_6_10_clear = sram_bytes[PUZZLEL6_COMPLETED % SRAM_AP_REGION_END - SRAM_AP_REGION_OFFSET]
                    if (pz_6_10_clear & (1 << 6)) == 0:
                        puzzle_goaled = False
                    else:
                        pz_6_10_clear = sram_bytes[
                            (PUZZLEL6_COMPLETED + 0x101) % SRAM_AP_REGION_END - SRAM_AP_REGION_OFFSET]
                        if (pz_6_10_clear & (1 << 6)) == 0:
                            puzzle_goaled = False
                if (self.all_goals[1] & 2) != 0:
                    pz_s_6_10_clear = sram_bytes[EXTRAPUZZLEL6_COMPLETED % SRAM_AP_REGION_END - SRAM_AP_REGION_OFFSET]
                    if (pz_s_6_10_clear & (1 << 6)) == 0:
                        extra_goaled = False
                    else:
                        pz_s_6_10_clear = sram_bytes[
                            (EXTRAPUZZLEL6_COMPLETED + 0x101) % SRAM_AP_REGION_END - SRAM_AP_REGION_OFFSET]
                        if (pz_s_6_10_clear & (1 << 6)) == 0:
                            extra_goaled = False
                if (self.all_goals[1] & 4) != 0:  # Flag for one goal being enough
                    if not puzzle_goaled and not extra_goaled:
                        goals_met = False
                elif not puzzle_goaled or not extra_goaled:
                    goals_met = False
                if self.all_goals[2] != 0:
                    goal_stage = ((self.all_goals[2] >> 2) & 3) + 8
                    goal_stage_clear = sram_bytes[
                        (VSSTAGES_COMPLETED + goal_stage) % SRAM_AP_REGION_END - SRAM_AP_REGION_OFFSET]
                    if (goal_stage_clear & (1 << 6)) == 0:
                        goals_met = False
                    else:
                        goal_stage_clear = sram_bytes[
                            (VSSTAGES_COMPLETED + goal_stage + 0x101) % SRAM_AP_REGION_END - SRAM_AP_REGION_OFFSET]
                        if (goal_stage_clear & (1 << 6)) == 0:
                            goals_met = False
            if goals_met:
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                ctx.finished_game = True

        # Look through location checks
        new_checks = []
        for loc_id in ctx.missing_locations:
            if not loc_id in ctx.locations_checked:
                loc_addr = loc_id % SRAM_AP_REGION_END
                loc_obtained = sram_bytes[loc_addr - SRAM_AP_REGION_OFFSET]
                if loc_addr == CLEARED_SHOCK_PANELS:
                    # Cleared shock panels is a 16-bit number, the required number is encoded by the ID's multiple of 1 KiB
                    loc_obtained += sram_bytes[loc_addr - SRAM_AP_REGION_OFFSET + 1] << 8
                    required_groups = loc_id // SRAM_AP_REGION_END
                    is_new_check = loc_obtained >= required_groups * self.shock_panels_per_check[0]
                else:
                    # Locations that are separated by a multiple of 1 KiB are the same, meaning they give multiple items
                    # The game fills up to bit 6 with the value 0x7F
                    bitmask = 1 << (loc_id // SRAM_AP_REGION_END)
                    is_new_check = (loc_obtained & bitmask) != 0
                if is_new_check:
                    location = ctx.location_names.lookup_in_game(loc_id)
                    self.last_stage_clear = evaluate_stage_clear(location, loc_id) or self.last_stage_clear
                    new_checks.append(loc_id)
                    snes_logger.info(
                        f"New check: {location} ({len(ctx.checked_locations) + len(new_checks)}/{len(ctx.server_locations)})")
        if len(new_checks) > 0:
            await ctx.send_msgs([{"cmd": "LocationChecks", "locations": new_checks}])
            ctx.locations_checked.update(new_checks)
        elif not self.looked_through_locations:
            snes_logger.info(f"No new location checks ({len(ctx.checked_locations)}/{len(ctx.server_locations)})")
        self.looked_through_locations = True

        # Check for new items
        old_item_count = received_item_count
        if received_item_count >= 32768:
            received_item_count = 0
            old_item_count = -1
        action_code = ACTION_CODE_NOOP
        while received_item_count < len(ctx.items_received):
            item = ctx.items_received[received_item_count]
            received_item_count += 1
            progressive_count = 0
            for i in range(received_item_count):
                if ctx.items_received[i].item == item.item:
                    progressive_count += 1
            if item.item < SRAM_AP_REGION_OFFSET:  # Progressive item
                current_count = get_current_progressive_count(item.item, sram_bytes)
                if current_count < progressive_count:
                    logging.info("Received %s #%d from %s (%s) (%d/%d in list)" % (
                        color(ctx.item_names.lookup_in_game(item.item), "red", "bold"),
                        current_count + 1,
                        color(ctx.player_names[item.player], "yellow"),
                        ctx.location_names.lookup_in_slot(item.location, item.player), received_item_count,
                        len(ctx.items_received)))
                    snes_logger.info("Granting %s #%d (%d/%d)" % (
                        ctx.item_names.lookup_in_game(item.item),
                        current_count + 1, received_item_count, len(ctx.items_received)))
                    item_id_range = get_progressive_item_addr_range(item.item)
                    new_item_id = item_id_range[0] + current_count
                    if new_item_id >= item_id_range[1]:
                        snes_logger.warning(
                            f"Too many copies of {ctx.item_names.lookup_in_game(item.item)} to fit into SRAM, maximum of {item_id_range[1] - item_id_range[0]}")
                    else:
                        snes_buffered_write(ctx, SRAM_SNI_BAND_START + SNI_RECEIVED_ITEM_ID, pack("H", new_item_id))
                        snes_buffered_write(ctx, SRAM_SNI_BAND_START + SNI_RECEIVED_ITEM_ARG, pack("H", 1))
                        action_code = ACTION_CODE_RECEIVED_ITEM
                        break
                else:
                    logging.info("Already have %d copies of %s (%d/%d in list)" % (
                        current_count,
                        color(ctx.item_names.lookup_in_game(item.item), "red", "bold"),
                        received_item_count,
                        len(ctx.items_received)))
            else:  # Unique item
                count_multiplier = 1
                item_addr = item.item % SRAM_AP_REGION_END
                already_obtained = sram_bytes[item_addr - SRAM_AP_REGION_OFFSET]
                if item_addr == STAGECLEARSHOCKPANEL_ID - SRAM_START:
                    already_obtained += sram_bytes[item_addr - SRAM_AP_REGION_OFFSET + 1] << 8
                    count_multiplier = self.shock_panels_per_check[0]
                if already_obtained // count_multiplier < progressive_count:
                    logging.info("Received %s from %s (%s) (%d/%d in list)" % (
                        color(ctx.item_names.lookup_in_game(item.item), "red", "bold"),
                        color(ctx.player_names[item.player], "yellow"),
                        ctx.location_names.lookup_in_slot(item.location, item.player), received_item_count,
                        len(ctx.items_received)))
                    snes_logger.info("Granting %s (%d/%d)" % (
                        ctx.item_names.lookup_in_game(item.item),
                        received_item_count, len(ctx.items_received)))
                    snes_buffered_write(ctx, SRAM_SNI_BAND_START + SNI_RECEIVED_ITEM_ID, pack("H", item_addr))
                    snes_buffered_write(ctx, SRAM_SNI_BAND_START + SNI_RECEIVED_ITEM_ARG,
                                        pack("H", progressive_count * count_multiplier))
                    action_code = ACTION_CODE_RECEIVED_ITEM
                    if item_addr == STAGECLEARSHOCKPANEL_ID - SRAM_START:
                        action_code = ACTION_CODE_RECEIVED_SHOCK_PANELS
                    elif 0x100 <= item.item <= 0x125:
                        action_code = ACTION_CODE_RECEIVED_SCORE
                    break
                else:
                    logging.info("Already have %s (%d/%d in list)" % (
                        color(ctx.item_names.lookup_in_game(item.item), "red", "bold"), received_item_count,
                        len(ctx.items_received)))
        if received_item_count > old_item_count:
            snes_buffered_write(ctx, SRAM_SNI_BAND_START + SNI_RECEIVED_ITEM_ACTION, pack("H", action_code))
            snes_buffered_write(ctx, SRAM_SNI_BAND_START + SNI_RECEIVED_ITEM_NUMBER, pack("H", received_item_count))

        # Check for collected locations
        else:
            collected_loc = 0
            collection_bitmask = 0
            for loc_id in ctx.checked_locations:
                loc_addr = loc_id % SRAM_AP_REGION_END
                if loc_addr != CLEARED_SHOCK_PANELS:
                    # The multiple of 0x400 determines the bit to look at; if enough bits are set this way,
                    #   the game will stop displaying the AP sprite even if not completed locally
                    # Shock panel checks cannot be skipped
                    loc_obtained = sram_bytes[loc_addr - SRAM_AP_REGION_OFFSET]
                    bitmask = 1 << (loc_id // SRAM_AP_REGION_END)
                    if (loc_obtained & bitmask) == 0:
                        location = ctx.location_names.lookup_in_game(loc_id)
                        snes_logger.info(f"Marking as collected ingame: {location}")
                        collected_loc = loc_addr
                        collection_bitmask = bitmask
                        break
            if collected_loc != 0:
                snes_buffered_write(ctx, SRAM_SNI_BAND_START + SNI_RECEIVED_ITEM_ID, pack("H", collected_loc))
                snes_buffered_write(ctx, SRAM_SNI_BAND_START + SNI_RECEIVED_ITEM_ARG, pack("H", collection_bitmask))
                snes_buffered_write(ctx, SRAM_SNI_BAND_START + SNI_RECEIVED_ITEM_ACTION,
                                    pack("H", ACTION_CODE_MARK_COMPLETE))
                snes_buffered_write(ctx, SRAM_SNI_BAND_START + SNI_RECEIVE_CHECK, pack("H", 0xFFFF))

        if ctx.slot:
            self.total_writes += 1
            status_message = ('\x13' + ctx.player_names[ctx.slot] +
                              '\n\x12AP\x11' + ctx.server_version.as_simple_string() + '\x12 GEN\x11' + ctx.generator_version.as_simple_string() +
                              '\n\x12WORLD\x11' + WORLD_VERSION +
                              '\n\x12SNI \x11')
            status_message += '.' * (self.total_writes % 8)
            status_message += 'O'
            status_message += '.' * (7 - (self.total_writes % 8))
            message_bytes = bytearray((' ' + status_message).encode('ascii', 'tatkencode'))[:76]
            message_bytes[0] = len(status_message)
            snes_buffered_write(ctx, STATUS_MESSAGE, message_bytes)

        message_request = sni_16_bit_data[SNI_MESSAGE_REQUEST >> 1]
        current_message_id = sni_16_bit_data[SNI_MESSAGE_ID >> 1]
        sni_message = ''
        new_message_id = 0
        match message_request:
            case 0:  # Blank
                if current_message_id != 0:
                    self.last_stage_clear = "???"
                sni_message = ''
            case 1:  # Deathlink
                sni_message = self.deathlink_message
                new_message_id = 1 + self.messages_received << 4
            case 2:  # Last
                # TODO_AFTER: Implement last message received in chat
                sni_message = self.last_message
                new_message_id = 2 + self.messages_received << 4
            case 3 | 4 | 5 | 6 | 7:  # Stage Clear
                if self.last_stage_clear != "???":
                    sni_message = f'You cleared\x12 {self.last_stage_clear}\x11!'
                new_message_id = 3 + len(ctx.checked_locations) << 4
            case 8:  # Special Stage Survived
                if self.deathlink_hint[0] > 0:
                    sni_message = '\nYou survived a Special Stage!'
                    new_message_id = 8
            case _:
                sni_message = 'Message ' + message_request
        if new_message_id != current_message_id:
            sni_message = break_up_message(sni_message)
            message_bytes = bytearray((' ' + sni_message).encode('ascii'))[:766]
            message_bytes[0] = len(sni_message)
            snes_buffered_write(ctx, SRAM_SNI_BAND_START + SNI_MESSAGE_ID, pack("H", new_message_id))
            snes_buffered_write(ctx, SRAM_SNI_MESSAGE, message_bytes)

        await snes_flush_writes(ctx)


def get_current_progressive_count(item_id: int, sram_bytes: bytes) -> int:
    item_id_range = get_progressive_item_addr_range(item_id)
    if item_id_range[1] <= item_id_range[0] + 1:
        return sram_bytes[item_id_range[0] - SRAM_AP_REGION_OFFSET]
    current_count = 0
    for i in range(item_id_range[0], item_id_range[1]):
        if sram_bytes[i - SRAM_AP_REGION_OFFSET] > 0:
            current_count += 1
    return current_count


def get_progressive_item_addr_range(item_id) -> (int, int):
    """Returns the address range of the provided item ID, exclusive end"""
    item = progressive_items[item_id]
    return item.starting_id, item.starting_id + item.amount


def evaluate_stage_clear(location, loc_id):
    if "Stage Clear ! Panels Check" in location:
        return None
    if "Stage Clear Round " in location:
        return f"SC Round {location[18]}"
    if "Extra Puzzle Round " in location:
        return f"PZ Extra Round {location[19]}"
    if "Puzzle Round " in location:
        return f"PZ Round {location[13]}"
    if "Stage Clear " in location:
        return f"SC {location[12:15]}"
    if "Extra Puzzle " in location:
        return f"PZ Extra {location[13:17]}"
    if "Puzzle " in location:
        return f"PZ {location[7:11]}"
    if VS_CLEARS_START <= loc_id < VS_CLEARS_END:
        return f"VS Stage {loc_id - VS_CLEARS_START + 1}"
    if VS_CLEARS_START + (4 << SRAM_FACTOR) <= loc_id < VS_CLEARS_END + (4 << SRAM_FACTOR):
        return f"VS Stage {loc_id - VS_CLEARS_START + 1} on Normal"
    if VS_CLEARS_START + (5 << SRAM_FACTOR) <= loc_id < VS_CLEARS_END + (5 << SRAM_FACTOR):
        return f"VS Stage {loc_id - VS_CLEARS_START + 1} on Hard"
    if VS_CLEARS_START + (6 << SRAM_FACTOR) <= loc_id < VS_CLEARS_END + (6 << SRAM_FACTOR):
        return f"VS Stage {loc_id - VS_CLEARS_START + 1} on V.Hard"
    return None


def get_deathlink_message(player_name: str, deathlink_code: int) -> str:
    match deathlink_code:
        case 1:
            return f"{player_name} topped out"
        case 2:
            return f"{player_name} couldn't keep things simple"
        case 3:
            return f"{player_name} couldn't do Chains and Combos"
        case 4:
            return f"{player_name} ran out of moves"
        case 5:
            return f"{player_name} let the puzzle rise too high"
        case 16:
            return f"{player_name} lost to Lakitu"
        case 17:
            return f"{player_name} lost to Bumpty"
        case 18:
            return f"{player_name} lost to Poochy"
        case 19:
            return f"{player_name} lost to Flying Wiggler"
        case 20:
            return f"{player_name} lost to Froggy"
        case 21:
            return f"{player_name} lost to Gargantua Blargg"
        case 22:
            return f"{player_name} lost to Lunge Fish"
        case 23:
            return f"{player_name} lost to Raphael the Raven"
        case 24:
            return f"{player_name} lost to Hookbill the Koopa"
        case 25:
            return f"{player_name} lost to Naval Piranha"
        case 26:
            return f"{player_name} lost to Kamek"
        case 27:
            return f"{player_name} lost to Bowser"
        case 32:
            return f"{player_name} topped out simultaneously with Lakitu"
        case 33:
            return f"{player_name} topped out simultaneously with Bumpty"
        case 34:
            return f"{player_name} topped out simultaneously with Poochy"
        case 35:
            return f"{player_name} topped out simultaneously with Flying Wiggler"
        case 36:
            return f"{player_name} topped out simultaneously with Froggy"
        case 37:
            return f"{player_name} topped out simultaneously with Gargantua Blargg"
        case 38:
            return f"{player_name} topped out simultaneously with Lunge Fish"
        case 39:
            return f"{player_name} topped out simultaneously with Raphael the Raven"
        case 40:
            return f"{player_name} topped out simultaneously with Hookbill the Koopa"
        case 41:
            return f"{player_name} topped out simultaneously with Naval Piranha"
        case 42:
            return f"{player_name} topped out simultaneously with Kamek"
        case 43:
            return f"{player_name} topped out simultaneously with Bowser"
        case _:
            return f"{player_name} died somehow ({deathlink_code})"


def break_up_message(message: str) -> str:
    new_message = textwrap.wrap(message, 12)
    if len(new_message) > 4:
        new_message = textwrap.wrap(message, 16)
        if len(new_message) > 4:
            new_message = textwrap.wrap(message, 20)
    del new_message[4:]
    return '\n'.join(new_message)
