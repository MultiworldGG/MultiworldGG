"""
This module is responsible for patching the game's map files per world.
This is done on the client side upon connect to allow for a smoother setup experience.
"""
import os
import struct
from typing import Any, List, Optional

from Options import Option
from worlds.rabi_ribi import RabiRibiWorld
from worlds.rabi_ribi.client.client import RabiRibiContext
from worlds.rabi_ribi.existing_randomizer.dataparser import RandomizerData
from worlds.rabi_ribi.existing_randomizer.mapfileio import (
    ItemModifier,
    grab_original_maps,
    MAP_ITEMS_OFFSET,
    MAP_TILES0_OFFSET,
    MAP_SIZE
)
from worlds.rabi_ribi.existing_randomizer.randomizer import (
    apply_item_specific_fixes,
    apply_map_transition_shuffle,
    apply_start_location_shuffle,
    get_default_areaids,
    insert_items_into_map,
    parse_args,
    pre_modify_map_data
)
from worlds.rabi_ribi.existing_randomizer.utility import to_index
from worlds.rabi_ribi.items import lookup_item_id_to_name
from worlds.rabi_ribi.locations import lookup_location_id_to_name
from worlds.rabi_ribi.names import LocationName
from worlds.rabi_ribi.options import AttackMode, RabiRibiOptions
from worlds.rabi_ribi.utility import convert_ap_name_to_existing_rando_name

class Allocation():
    """
    This class mimics the existing randomizer's Allocation class.
    It sets the appropriate fields such that we can call the existing randomizer's
    data manipulation and file write functions.
    """

    def __init__(self, ctx: RabiRibiContext, randomizer_data: RandomizerData):
        self.map_modifications = []
        self.item_at_item_location = self.set_location_info(
            ctx.slot,
            ctx.locations_info
        )

        if not ctx.slot_data:
            raise RuntimeError("Missing slot data while attempting to patch maps")

        map_transition_shuffle_order: List[int] = ctx.slot_data["map_transition_shuffle_order"]

        self.map_modifications += randomizer_data.default_map_modifications
        self.walking_left_transitions = [randomizer_data.walking_left_transitions[x] for x in map_transition_shuffle_order]

        start_location_name = convert_ap_name_to_existing_rando_name(ctx.slot_data["start_location"])
        self.start_location = next((location for location in randomizer_data.start_locations
                                    if location.location == start_location_name), randomizer_data.start_locations[0])

    def set_location_info(self, slot_num, location_info):
        return {
            convert_ap_name_to_existing_rando_name(lookup_location_id_to_name[location.location]):
            convert_ap_name_to_existing_rando_name(lookup_item_id_to_name[location.item]) \
                if location.player == slot_num else "ANOTHER_PLAYERS_ITEM"
            for location in location_info.values()
        }

def patch_map_files(ctx: RabiRibiContext):
    """
    Patch the map files to make map modifications (item changes / room changes, etc).

    :RabiRibiContext ctx: The Rabi Ribi Context instance.
    """
    if not ctx.slot_data or not ctx.custom_seed_subdir:
        raise RuntimeError("Missing seed info while attempting to patch maps")

    map_source_dir = f"{RabiRibiWorld.settings.game_installation_path}/data/area"
    grab_original_maps(map_source_dir, ctx.custom_seed_subdir)
    settings = initialize_settings(ctx)
    attack_mode = ctx.slot_data["attackMode"]
    picked_templates = ctx.slot_data["picked_templates"]
    if attack_mode == AttackMode.option_hyper:
        settings.hyper_attack_mode = True
    elif attack_mode == AttackMode.option_super:
        settings.super_attack_mode = True
    area_ids = get_default_areaids()
    randomizer_data = RandomizerData(settings)
    item_modifier = ItemModifier(
        area_ids,
        map_source_dir
    )
    allocation = Allocation(ctx, randomizer_data)
    map_modifications = allocation.map_modifications
    for template in picked_templates:
        map_modifications.append(os.path.join('existing_randomizer', 'maptemplates', 'constraint_shuffle', f'CS_{template}.txt'))

    pre_modify_map_data(item_modifier, settings, map_modifications, randomizer_data.config_data)
    apply_item_specific_fixes(item_modifier, allocation)
    apply_map_transition_shuffle(item_modifier, randomizer_data, settings, allocation)
    apply_start_location_shuffle(item_modifier, settings, allocation)
    insert_items_into_map(item_modifier, randomizer_data, settings, allocation)

    if (ctx.custom_seed_subdir):
        item_modifier.save(ctx.custom_seed_subdir)

    embed_seed_player_into_mapdata(ctx, item_modifier)
    create_custom_text_file(ctx)

def initialize_settings(ctx: RabiRibiContext):
    settings = parse_args()
    settings.open_mode = True
    settings.num_hard_to_reach = ctx.slot_data["required_egg_count"]
    settings.shuffle_gift_items = True

    # Need a unique seed to ensure that the background and music shuffles can be regenerated if needed.
    settings.random_seed = ctx.seed_player
    settings.shuffle_music = ctx.slot_data["shuffle_music"]
    settings.shuffle_backgrounds = ctx.slot_data["shuffle_backgrounds"]
    settings.shuffle_start_location = True # Always apply start location shuffle to enable start room.
    settings.apply_beginner_mod = ctx.slot_data["apply_beginner_mod"]
    settings.no_laggy_backgrounds = True if "allow_laggy_backgrounds" not in ctx.slot_data else not ctx.slot_data["allow_laggy_backgrounds"]
    settings.no_difficult_backgrounds = True if "allow_difficult_backgrounds" not in ctx.slot_data else not ctx.slot_data["allow_difficult_backgrounds"]
    return settings

def remove_exclamation_point_from_map(ctx: RabiRibiContext, area_id: int, x: int, y: int):
    """
    This method removes a specified item from the map. This is used to delete
    items from other worlds (represented by exclamation point items) on the map
    after the player collects it. This is needed because the item being visible
    is directly linked to whether the exclamation point item is in the player's
    inventory. We always set that value to false so that the player can see all
    of the exclamation points, but we want to delete the ones the player has already
    obtained.
    """
    EXCLAMATION_POINT_ITEM_ID = 43
    f = open(f"{ctx.custom_seed_subdir}/area{area_id}.map", "r+b")
    f.seek(MAP_ITEMS_OFFSET)
    tiledata_items = list(struct.unpack('%dh' % MAP_SIZE, f.read(MAP_SIZE*2)))
    index = to_index((x, y))

    if tiledata_items[index] == EXCLAMATION_POINT_ITEM_ID:
        tiledata_items[index] = 0
        f.seek(MAP_ITEMS_OFFSET)
        f.write(struct.pack('%dh' % MAP_SIZE, *tiledata_items))
        f.close()

def embed_seed_player_into_mapdata(ctx: RabiRibiContext, item_modifier):
    if not ctx.seed_player_id:
        raise RuntimeError("Missing seed player ID while embedding seed in map")

    for area_id, _ in item_modifier.stored_datas.items():
        with open(f"{ctx.custom_seed_subdir}/area{area_id}.map", "r+b") as f:
            f.seek(MAP_TILES0_OFFSET)
            f.write(ctx.seed_player_id.encode())
            f.close()

def create_custom_text_file(ctx: RabiRibiContext):
    start_location = ctx.slot_data["start_location"]
    required_egg_count = ctx.slot_data["required_egg_count"] if "required_egg_count" in ctx.slot_data else 5
    with open(f"{ctx.custom_seed_subdir}/story_text.rbrb", "w") as f:
        f.write("\r\n")
        f.write("Starting Forest\r\n")
        f.write("Forgotten Cave II\r\n")
        f.write(f"{LocationName.start_location_to_area_name[start_location]}\r\n")
        f.write(f"Required Eggs: {required_egg_count}\r\n")
