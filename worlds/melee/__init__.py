import threading


from typing import List
from BaseClasses import MultiWorld, Location, Tutorial
from worlds.AutoWorld import World, WebWorld
from .Items import get_item_names_per_category, item_table
from .Options import SSBMOptions, ssbm_option_groups
from .static_location_data import location_ids, location_name_groups
from .in_game_data import global_trophy_table
from worlds.LauncherComponents import Component, Type, components, launch_subprocess, icon_paths
from Utils import local_path
from .generator_main import (generate_early, create_regions, create_items, set_rules, generate_output,
                             create_item, fill_slot_data, modify_multidata, get_filler_item_name, SSBMItem)


def run_client(*args):
    print("Running SSBM Client")
    from .Client import launch
    launch_subprocess(launch, name="SSBMClient", args=args)


components.append(
    Component("Super Smash Bros. Melee Client", func=run_client, component_type=Type.CLIENT, icon="melee_ap_logo")
)

icon_paths["melee_ap_logo"] = local_path("worlds/melee/data", "melee_ap_logo.png")


class SSBMWeb(WebWorld):
    theme = "ocean"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Melee randomizer"
        "and connecting to a MultiworldGG server.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Pink Switch"]
    )

    tutorials = [setup_en]

    option_groups = ssbm_option_groups


class SSBMWorld(World):
    """
    Super Smash Bros. Melee is a 2.5D fighting game for the Nintendo GameCube. It was first released on Nov 21st, 2001.
    Like its predecessor, Melee features unique gameplay in comparison to that of other fighting games. 
    Characters have simple movesets that lack complicated button inputs and lengthy inescapable combos, instead emphasizing movement and ringouts. 
    """
    
    game = "Super Smash Bros. Melee"
    option_definitions = SSBMOptions
    data_version = 1
    required_client_version = (0, 6, 1)
    origin_region_name = "Game Base"

    item_name_to_id = {item: item_table[item].code for item in item_table}
    location_name_to_id = location_ids
    item_name_groups = get_item_names_per_category()
    location_name_groups = location_name_groups

    web = SSBMWeb()
    # topology_present = True

    options_dataclass = SSBMOptions
    options: SSBMOptions

    locked_locations: List[str]
    location_cache: List[Location]

    generate_early = generate_early
    create_items = create_items
    create_item = create_item
    create_regions = create_regions
    fill_slot_data = fill_slot_data
    modify_multidata = modify_multidata
    generate_output = generate_output
    get_filler_item_name = get_filler_item_name
    set_rules = set_rules

    def __init__(self, multiworld: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        super().__init__(multiworld, player)

        self.locked_locations = []
        self.location_cache = []
        self.goal_count = 1
        self.picked_trophies = set()
        self.all_trophies = global_trophy_table.copy()
        self.all_adventure_trophies = False
        self.all_classic_trophies = False
        self.all_allstar_trophies = False
        self.location_count = 174
        self.required_item_count = 49
