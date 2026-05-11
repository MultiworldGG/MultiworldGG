from typing import TYPE_CHECKING
import json
import os

from NetUtils import ClientStatus
from typing import Optional

from worlds.sly1.Sly1Interface import Sly1Episode, Sly1Interface
from worlds.sly1.data.Constants import ADDRESSES, LEVELS, BOSSES, MOVES, MOVE_NAMES
from worlds.sly1.Locations import location_table, minigame_locations, bottle_amounts, KEY_LOCATION_NAMES, KEY_CACHE_BASE
from worlds.sly1.Items import from_id, bottles

SAVE_FILE = "sly1_item_progress.json"

if TYPE_CHECKING:
    from worlds.sly1.Sly1Client import Sly1Context

async def update(ctx: 'Sly1Context', ap_connected: bool) -> None:
    """Called continuously"""
    if ap_connected and ctx.slot_data is not None:
        check_levels(ctx)
        check_maps(ctx)
        check_keys(ctx)
        check_bottles(ctx)
        check_bosses(ctx)
        await handle_checks(ctx)
        await handle_received(ctx)
        check_hubs(ctx)
        await handle_goal(ctx)
        ctx.game_interface.write_names(ctx)
        ctx.game_interface.write_anticheat()

async def init(ctx: 'Sly1Context', ap_connected: bool) -> None:
    """Called when the player connects to the AP server"""
    if ap_connected:
        ctx.in_game = True
        ctx.game_interface.write_anticheat()

def check_levels(ctx: 'Sly1Context') -> None:
    """Checks for completion of keys, vaults, and hourglasses"""
    level_addresses = ADDRESSES["SCUS-97198"]["levels"]

    for episode_index, episode_levels in enumerate(level_addresses):
        for level_index, level_address in enumerate(episode_levels):
            value = ctx.game_interface._read32(level_address)
            level_name = list(LEVELS.values())[episode_index][level_index]

            key = (value >> 1) & 1
            vault = (value >> 2) & 1
            hourglass = (value >> 3) & 1

            if key:
                ctx.level_keys[episode_index][level_index] = True
            if vault:
                ctx.vaults[episode_index][level_index] = True
                if level_name in ctx.openable_vaults and level_name not in ctx.opened_vaults:
                    ctx.openable_vaults.remove(level_name)
                    ctx.opened_vaults.append(level_name)
            if hourglass:
                ctx.hourglasses[episode_index][level_index] = True

def check_maps(ctx: 'Sly1Context') -> None:
    map_addresses = ADDRESSES["SCUS-97198"]["maps"]

    for i in range(0, 4):
        if ctx.game_interface._read32(map_addresses[i]) != 1:
            ctx.game_interface._write32(map_addresses[i], 1)

def check_keys(ctx: 'Sly1Context') -> None:
    key_addresses = ADDRESSES["SCUS-97198"]["keys"]
    move_address = ADDRESSES["SCUS-97198"]["thief moves"]
    moves = ctx.thief_moves
    all_moves = ctx.all_moves

    for i in range(0, 4):
        if  ctx.game_interface._read32(key_addresses[i]) != ctx.inven_keys[i]:
            ctx.game_interface._write32(key_addresses[i], ctx.inven_keys[i])
    #Remove Hacking from player's inventory if they have every move.
    #Otherwise, vaults will be empty.
    #This is a temporary workaround.
    if (moves & all_moves) == all_moves:
        moves &= ~MOVES["Hacking"]

    if moves != ctx.last_written_moves and not Sly1Interface.moves_locked:
        ctx.game_interface._write32(move_address, moves)
        ctx.last_written_moves = moves

def check_hubs(ctx: 'Sly1Context') -> None:
    if ctx.slot_data is None:
        return
    hub_addresses = ADDRESSES["SCUS-97198"]["hubs"]

    for i in range(0, 4):
        curr_val = ctx.game_interface._read32(hub_addresses[i])
        if ctx.hubs[i] is True and curr_val == 0:
            ctx.game_interface._write32(hub_addresses[i], 1)
        elif ctx.hubs[i] is False and curr_val > 0:
            ctx.game_interface._write32(hub_addresses[i], 0)

def check_bottles(ctx: 'Sly1Context') -> None:
    if ctx.slot_data is None:
        return
    bundle_size = ctx.slot_data.get("ItemCluesanityBundleSize")
    if bundle_size is None:
        bundle_size = ctx.slot_data.get("CluesanityBundleSize")
    if bundle_size is None or bundle_size == 0:
        return
    bottle_addresses = ADDRESSES["SCUS-97198"]["bottle addresses"]

    for episode_index, episodes in enumerate(bottle_addresses):
        for level_index, level_address in enumerate(episodes):
            if level_address == 0:
                continue
            level_name = list(LEVELS.values())[episode_index][level_index]
            if level_name not in bottle_amounts:
                continue
            rec_bottles = ctx.bottles[episode_index][level_index] * bundle_size
            if rec_bottles >= bottle_amounts[level_name].bottle_amount:
                rec_bottles = bottle_amounts[level_name].bottle_amount
                if level_name not in ctx.openable_vaults and level_name not in ctx.opened_vaults:
                    ctx.openable_vaults.append(level_name)
            ctx.game_interface._write32(level_address, rec_bottles)

def check_bosses(ctx):
    if ctx.slot_data is None:
        return
    required_bosses = ctx.slot_data.get("RequiredBosses", 4)
    fits_address = ADDRESSES["SCUS-97198"]["fits progress"]

    if ctx.slot_data.get("UnlockClockwerk", 1) == 1:
        goal_met = ctx.bosses_beaten >= required_bosses
    else:
        goal_met = ctx.goal_pages >= ctx.slot_data.get("RequiredPages", 0)

    current_fits = ctx.game_interface._read32(fits_address)
    if goal_met:
        if current_fits != 53:
            ctx.game_interface._write32(fits_address, 53)
            if ctx.slot_data.get("FastClockwerk", 0) == 1:
                ctx.game_interface._write32(0x27DB6C, 1)
    elif current_fits > 21:
        ctx.game_interface._write32(fits_address, 21)

async def handle_checks(ctx: 'Sly1Context') -> None:
    """Send checks to the multiworld"""
    if ctx.slot_data is None:
        return

    #Paris Files
    if ctx.game_interface.check_paris_files():
        location_name = "Paris Files"
        if location_name in location_table:
            location_code = location_table[location_name].ap_code
            if location_code not in ctx.locations_checked:
                ctx.locations_checked.add(location_code)


    #Keys, Vaults, and Hourglasses
    for episode_index, (episode_name, level_list) in enumerate(LEVELS.items()):
        for level_index, level_name in enumerate(level_list):
            if ctx.level_keys[episode_index][level_index]:
                location_name = f"{level_name} Key"
                if location_name in location_table:
                    location_code = location_table[location_name].ap_code
                    if location_code not in ctx.locations_checked:
                        ctx.locations_checked.add(location_code)
                # Minigame Caches
                minigame_name = level_name + " Key"
                if minigame_name in minigame_locations:
                    for i in range(1, 11):
                        location_code = minigame_locations[minigame_name].ap_code + i
                        if location_code not in ctx.locations_checked:
                            ctx.locations_checked.add(location_code)
                # Key Caches
                if level_name + " Key" in KEY_LOCATION_NAMES:
                    key_index = KEY_LOCATION_NAMES.index(level_name + " Key")
                    for i in range(10):
                        location_code = KEY_CACHE_BASE + (key_index * 10) + i
                        if location_code in ctx.server_locations and location_code not in ctx.locations_checked:
                            ctx.locations_checked.add(location_code)
            if ctx.vaults[episode_index][level_index]:
                location_name = f"{level_name} Vault"
                if location_name in location_table:
                    location_code = location_table[location_name].ap_code
                    if location_code not in ctx.locations_checked:
                        ctx.locations_checked.add(location_code)
            if ctx.hourglasses[episode_index][level_index]:
                location_name = f"{level_name} Hourglass"
                if location_name in location_table:
                    location_code = location_table[location_name].ap_code
                    if location_code not in ctx.locations_checked:
                        ctx.locations_checked.add(location_code)

    #Clue Bottles
    bottle_n = ctx.slot_data.get("LocationCluesanityBundleSize", 0)
    if bottle_n is None:
        bottle_n = ctx.slot_data.get("CluesanityBundleSize", 0)

    if bottle_n != 0:
        level_addresses = ADDRESSES["SCUS-97198"]["levels"]
        for episode_index, episode_levels in enumerate(level_addresses):
            for level_index, level_address in enumerate(episode_levels):
                episode_name = list(LEVELS.keys())[episode_index]
                level_name = LEVELS[episode_name][level_index]
                if (level_index == 1) or (level_name in minigame_locations):
                    continue
                value = ctx.game_interface._read32(level_address + 104)
                value2 = ctx.game_interface._read8(level_address + 108)

                collected = bin(value).count("1") + bin(value2).count("1")
                if collected > 0:
                    for i in range(1, collected + 1):
                        if i%bottle_n == 0 or i == bottle_amounts[level_name].bottle_amount:
                            location_code = bottle_amounts[level_name].ap_code + i - 1
                            if location_code not in ctx.locations_checked:
                                ctx.locations_checked.add(location_code)

    #Bosses
    boss_value = ctx.game_interface._read32(ADDRESSES["SCUS-97198"]["game completion"])
    ctx.bosses_beaten = 0
    for boss_name, bit in BOSSES:
        if (boss_value >> bit) & 1:
            ctx.bosses_beaten += 1
            location_code = location_table[boss_name].ap_code
            if location_code not in ctx.locations_checked:
                ctx.locations_checked.add(location_code)

    await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": ctx.locations_checked}])

async def handle_goal(ctx: 'Sly1Context') -> None:
    if 10020233 in ctx.locations_checked:
        await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])

async def handle_received(ctx: 'Sly1Context') -> None:
    """Receive items from the multiworld"""
    if ctx.slot_data is None:
        return

    start_index = ctx.last_received_index if hasattr(ctx, "last_received_index") else 0

    all_states = load_saved_state()
    current_seed = str(ctx.slot_data.get("Seed"))
    network_items = ctx.items_received
    received_count = len(network_items)

    state = all_states.get(current_seed, {
        "received_count": 0
    })

    for i in range(start_index, len(network_items)):
        network_item = network_items[i]
        item = from_id(network_item.item)
        player = ctx.player_names[network_item.player]

        if (10020001 <= item.ap_code <= 10020014) and (Sly1Interface.moves_locked is False):
            m = item.ap_code - 10020001
            ctx.inven_moves[m] += 1

            move_name = MOVE_NAMES[m]
            move_data = MOVES[move_name]

            if isinstance(move_data, list):
                move_level = ctx.inven_moves[m] - 1
                if move_level < len(move_data):
                    ctx.thief_moves |= move_data[move_level]
            else:
                ctx.thief_moves |= move_data
        if 10020015 <= item.ap_code <= 10020018:
            k = item.ap_code - 10020015
            ctx.inven_keys[k] += 1
        if item.ap_code == 10020019 and (state["received_count"] < received_count):
            charms = ctx.game_interface._read32(ADDRESSES["SCUS-97198"]["charms"])
            if charms < 2:
                charms += 1
                ctx.game_interface._write32(ADDRESSES["SCUS-97198"]["charms"], charms)
            else:
                lives = ctx.game_interface._read32(ADDRESSES["SCUS-97198"]["lives"])
                lives += 1
                if lives > 99:
                    lives = 99
                ctx.game_interface._write32(ADDRESSES["SCUS-97198"]["lives"], lives)
        if item.ap_code == 10020020 and (state["received_count"] < received_count):
            lives = ctx.game_interface._read32(ADDRESSES["SCUS-97198"]["lives"])
            lives += 1
            if lives > 99:
                lives = 99
            ctx.game_interface._write32(ADDRESSES["SCUS-97198"]["lives"], lives)
        if 10020021 <= item.ap_code <= 10020024:
            l = item.ap_code - 10020021
            ctx.hubs[l] = True
            ctx.names_dirty = True
        if (10020026 <= item.ap_code <= 10020029) and (state["received_count"] < received_count):
            await ctx.game_interface.activate_trap(item.ap_code)
        if 10020030 <= item.ap_code <= 10020048:
            for name, data in bottles.items():
                if data.ap_code == item.ap_code:
                    bottle_level = name.replace(" Bottle(s)", "")

                    for episode_index, (world, levels) in enumerate(LEVELS.items()):
                        if bottle_level in levels:
                            level_index = levels.index(bottle_level)
                            ctx.bottles[episode_index][level_index] += 1
            ctx.names_dirty = True
        if item.ap_code == 10020049:
            ctx.goal_pages += 1

    ctx.last_received_index = len(network_items)
    state["received_count"] = received_count
    save_state(current_seed, state)

def load_saved_state():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            print(f"[Warning] Failed to load save file: {e}")
            return {}
    return {}

def save_state(seed, new_state):
    all_states = load_saved_state()
    all_states[str(seed)] = new_state
    with open(SAVE_FILE, "w") as f:
        json.dump(all_states, f, indent=4)

def get_blueprint(episode: int) -> Optional[str]:
    blueprint_mapping = {
        Sly1Episode.Tide_of_Terror: "ToT Blueprints",
        Sly1Episode.Sunset_Snake_Eyes: "SSE Blueprints",
        Sly1Episode.Vicious_Voodoo: "VV Blueprints",
        Sly1Episode.Fire_in_the_Sky: "FitS Blueprints",
    }
    return blueprint_mapping.get(Sly1Episode(episode))

def get_bit_value(move_data):
    return move_data[0] if isinstance(move_data, list) else move_data