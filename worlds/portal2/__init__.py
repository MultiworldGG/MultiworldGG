from math import ceil
import sys
from typing import Any, ClassVar

from BaseClasses import ItemClassification, MultiWorld, Region, Tutorial
from Options import PerGameCommonOptions
import Utils
import settings
from worlds.AutoWorld import WebWorld, World
from worlds.generic.Rules import add_item_rule
from .Options import CutsceneLevels, Portal2Options, portal2_option_groups, portal2_option_presets, GameModeOption, LogicDifficultyOption
from .Items import Portal2Item, game_item_table, item_table, junk_items, trap_items
from .Locations import *
from .ItemNames import portal_gun_2

from . import Components as components

debug_mode = False

class Portal2Settings(settings.Group):
    class Portal2ExtrasFilePath(settings.UserFilePath):
        """The file path of the extras.txt file (used to generate the menu in game)"""
        description = "Portal 2 extras.txt file inside the mod"

    is_windows = sys.platform == "win32"
    is_linux = sys.platform == "linux"
    extras_path = "C:/Program Files (x86)/Steam/steamapps/sourcemods/Portal2Archipelago/scripts/extras.txt" if is_windows else \
                    "$HOME/.local/share/Steam/steamapps/sourcemods/Portal2Archipelago/scripts/extras.txt" if is_linux else "" # May may be user specific so cannot auto select
    menu_file: Portal2ExtrasFilePath = Portal2ExtrasFilePath(extras_path)

    class Portal2NetConPort(int):
        """The port set in the portal 2 launch options e.g. 3000"""

    default_portal2_port: Portal2NetConPort = Portal2NetConPort(3000)

class Portal2WebWorld(WebWorld):
    game = "Portal 2"
    theme = "partyTime"

    setup_en = Tutorial(
        tutorial_name="Setup Guide",
        description="A guide to playing Portal 2 in MultiworldGG.",
        language="English",
        file_name="setup_en.md",
        link="setup/en",
        authors=["GlassToadstool"]
    )

    tutorials = [setup_en]

    option_groups = portal2_option_groups
    option_presets = portal2_option_presets

class Portal2World(World):
    """Portal 2 is a first person puzzle adventure where you shoot solve test chambers using portal mechanics and other map specific items"""
    game = "Portal 2"  # name of the game/world
    options_dataclass = Portal2Options  # options the player can set
    options: Portal2Options  # typing hints for option results
    settings: ClassVar[Portal2Settings]
    web = Portal2WebWorld()

    BASE_ID = 98275000

    ut_can_gen_without_yaml = True

    goal_location = "Finale 4 Completion"

    item_name_to_id = {}
    location_name_to_id = {}
    location_name_groups = location_groups
    
    for key, value in item_table.items():
        item_name_to_id[key] = value.id

    for key, value in all_locations_table.items():
        location_name_to_id[key] = value.id
    
    def __init__(self, multiworld, player):
        super().__init__(multiworld, player)
        self.maps_in_use: list[str] = []
        self.chapter_maps_dict: dict[str, list[str]] = {}
        self.location_logic: dict[str, list[str]] = {}

    # Helper Functions

    def create_item(self, name: str):
        return Portal2Item(name, item_table[name].classification, self.item_name_to_id[name], self.player)
    
    def create_location(self, name, id, parent):
        return Portal2Location(self.player, name, id, parent)
    
    def get_filler_item_name(self):
        return self.random.choice(junk_items)
    
    def create_randomized_maps(self) -> dict[str, list[str]]:
        def pick_maps(number: int) -> None:
            self.random.shuffle(map_pool)
            for _ in range(number):
                map_choice = map_pool.pop(0)
                used_maps.append(map_choice)
                
                if self.options.game_mode == GameModeOption.CHAOTIC:
                    random_chapter = self.random.randint(1, 8)
                    chapter_maps[f"Chapter {random_chapter}"].append(map_choice)
                else:
                    chapter_maps[f"Chapter {all_locations_table[map_choice].chapter}"].append(map_choice)

        chapter_maps: dict[str, list[str]] = {f"Chapter {i}": [] for i in range(1,9)}

        map_pool: list[str] = []
        used_maps: list[str] = []

        # Only consider map completion entries (exclude cutscenes and other non-map locations)
        possible_maps = [name for name in sorted(self.maps_in_use) if all_locations_table[name].chapter != 9]
        
        proportion_map_pick: float = self.options.early_playability_percentage / 100

        # Maps with no requirements
        map_pool += [name for name in possible_maps if len(self.location_logic[name]) == 0]
        pick_maps(ceil(len(map_pool) * proportion_map_pick))
        
        # Maps with just portal gun upgrade
        map_pool += [name for name in possible_maps if len(self.location_logic[name]) <= 2
                     and name not in used_maps and name not in map_pool]
        pick_maps(ceil(len(map_pool) * proportion_map_pick))

        # All other maps
        map_pool += [name for name in possible_maps if name not in used_maps and name not in map_pool]
        pick_maps(len(map_pool))

        return chapter_maps
    
    def create_in_level_check(self, name: str, requirements: list[str], entrance_region: Region):
        # Use a distinct region name for in-level checks so they don't collide
        # with the map's main end region ("{map} End").
        new_region = Region(f"{name} Check", self.player, self.multiworld)
        self.multiworld.regions.append(new_region)
        new_region.add_locations({name: self.location_name_to_id[name]}, Portal2Location)
        entrance_region.connect(new_region, f"Get {name}", lambda state, _item_reqs=requirements: state.has_all(_item_reqs, self.player))

    def create_connected_maps(self, chapter_number: int, map_location_names: list[str] | None = None):
        chapter_name = f"Chapter {chapter_number}"
        chapter_region = Region(chapter_name, self.player, self.multiworld)
        self.multiworld.regions.append(chapter_region)

        # Get all map locations for that chapter
        if map_location_names is None:
            map_location_names = [name for name in maps_in_chapters[chapter_name] if name in self.maps_in_use and all_locations_table[name].chapter == chapter_number]
            # Add them to chapter maps for menu gen and UT
            self.chapter_maps_dict[chapter_name] = map_location_names
            
        map_prefix = [name.removesuffix(" Completion") for name in map_location_names]

        last_region: Region | None = None
        for name, map_name in zip(map_prefix, map_location_names):
            region_start = Region(f"{name} Start", self.player, self.multiworld)
            self.multiworld.regions.append(region_start)
            region_end = Region(f"{name} End", self.player, self.multiworld)
            self.multiworld.regions.append(region_end)
            region_end.add_locations({map_name: self.location_name_to_id[map_name]}, Portal2Location)
            item_reqs = self.location_logic[map_name]
            region_start.connect(region_end, f"Beat {name}", lambda state, _item_reqs=item_reqs: state.has_all(_item_reqs, self.player))

            # Additional locations
            for sub_location in sub_locations_in_maps.get(map_name, []):
                if sub_location in item_location_table:
                    item_check_reqs = item_location_table[sub_location].required_items
                    self.create_in_level_check(sub_location, item_check_reqs, region_start)
                elif self.options.wheatley_monitors and sub_location in wheatley_monitor_table:
                    wheatley_requirements = wheatley_monitor_table[sub_location].required_items
                    self.create_in_level_check(sub_location, wheatley_requirements, region_start)
                elif self.options.ratman_dens and sub_location in ratman_den_locations_table:
                    ratman_requirements = ratman_den_locations_table[sub_location].required_items
                    self.create_in_level_check(sub_location, ratman_requirements, region_start)
            
            # Connect to chapter region if there was no previous level or if open world
            if self.options.game_mode == GameModeOption.OPEN_WORLD or last_region == None:
                chapter_region.connect(region_start)
            else:
                last_region.connect(region_start)
                
            last_region = region_end

        return chapter_region, last_region

    # Overridden methods called by Main.py in execution order

    def generate_early(self):
        self.multiworld.early_items[self.player][portal_gun_2] = 1

        # Universal Tracker Support
        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if re_gen_passthrough and self.game in re_gen_passthrough:
            slot_data: dict[str, Any] = re_gen_passthrough[self.game]

            if "chapter_dict" in slot_data:
                self.chapter_maps_dict = slot_data.get("chapter_dict", {})
                self.chapter_maps_dict = {f"Chapter {key}": value for key, value in self.chapter_maps_dict.items()}

            for key, value in slot_data.items():
                if hasattr(self.options, key):
                    getattr(self.options, key).value = value

        self.maps_in_use = list(map_complete_table)
        # Cutscene levels option
        if self.options.cutscene_levels:
            self.maps_in_use += list(cutscene_completion_table)

        # Remove maps that have been put in the Remove Locations option
        for location in self.options.remove_locations:
            if location in self.maps_in_use:
                self.maps_in_use.remove(location)

        # Update logic for speedrun option
        self.location_logic = {location: data.required_items for location, data in all_locations_table.items()}
        if self.options.logic_difficulty == LogicDifficultyOption.SPEEDRUNNER:
            for map_location in self.maps_in_use:
                if map_location in speedrun_logic_table:
                    self.location_logic[map_location] = speedrun_logic_table[map_location]

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)

        if not (self.chapter_maps_dict or self.options.game_mode == GameModeOption.OPEN_WORLD):
            self.chapter_maps_dict = self.create_randomized_maps()
        # Add chapters to those regions
        for i in range(1,9):
            if self.options.game_mode == GameModeOption.OPEN_WORLD:
                chapter_region, last_region = self.create_connected_maps(i)
            else:
                chapter_region, last_region = self.create_connected_maps(i, self.chapter_maps_dict[f"Chapter {i}"])
            
            menu_region.connect(chapter_region, f"Chapter {i} Entrance")
        

        # Chapter 9
        chapter_9_region, last_region = self.create_connected_maps(9, self.chapter_maps_dict.get("Chapter 9"))
        menu_region.connect(chapter_9_region, f"Chapter 9 Entrance")

        # Add Goal Region and Event
        end_game_region = Region("End Game", self.player, self.multiworld)
        last_region.connect(end_game_region, f"End Game Entrance")
        self.multiworld.regions.append(end_game_region)
        end_game_region.add_event("Beat Final Level", "Victory", None, Portal2Location, None, True)
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def create_items(self):
        itempool = [self.create_item(item_name) for item_name in game_item_table.keys()]

        filler_count = len(self.multiworld.get_unfilled_locations(self.player)) - len(itempool)
        trap_percentage: int = self.options.trap_fill_percentage.value
        trap_fill_number: int = min(round(trap_percentage / 100 * filler_count), filler_count)
        trap_weights: list[int] = [self.options.motion_blur_trap_weight.value,
                                   self.options.fizzle_portal_trap_weight.value,
                                   self.options.butter_fingers_trap_weight.value,
                                   self.options.cube_confetti_trap_weight.value,
                                   self.options.slippery_floor_trap_weight.value]  # in the same order as the traps appear in trap_items list

        if sum(trap_weights) > 0 and trap_fill_number > 0:
            traps = self.random.choices(trap_items, weights=trap_weights, k=trap_fill_number)
            itempool.extend(self.create_item(trap) for trap in traps)

        # Fill remaining with filler item
        filler_count = len(self.multiworld.get_unfilled_locations(self.player)) - len(itempool)
        itempool.extend(self.create_item(self.get_filler_item_name()) for _ in range(filler_count))

        self.multiworld.itempool.extend(itempool)

    def set_rules(self):
        # Stop any progression items from being in the final location
        add_item_rule(self.multiworld.get_location(self.goal_location, self.player), 
                      lambda item: item.name not in game_item_table or item.player != self.player)
    
    def fill_slot_data(self):
        if debug_mode:
            state = self.multiworld.get_all_state(False)
            state.update_reachable_regions(self.player)
            Utils.visualize_regions(self.multiworld.get_region("Menu", self.player), f"output/map_Player{self.player}.puml", show_entrance_names=True, regions_to_highlight=state.reachable_regions[self.player])
        
        # Return the chapter map orders e.g. {chapter1: ['sp_a1_intro2', 'sp_a1_intro5', ...], chapter2: [...], ...}
        # This is for generating and updating the Extras menu (level select screen) in portal 2 at the start and when checks are made
        excluded_option_names = list(PerGameCommonOptions.type_hints.keys())
        included_option_names: list[str] = [option_name for option_name in self.options_dataclass.type_hints if option_name not in excluded_option_names]
        slot_data = self.options.as_dict(*included_option_names, toggles_as_bools=True)
        slot_data.update({
            "goal_map_code": all_locations_table[self.goal_location].map_name,
            "location_name_to_id": self.location_name_to_id,
            "chapter_dict": {int(name[-1]): values for name, values in self.chapter_maps_dict.items()}
        })
        # Check if portal gun items are in their locations
        if self.multiworld.find_item(portal_gun_2, self.player).name == portal_gun_2:
            slot_data["portal_gun_upgrade_inplace"] = True

        if self.multiworld.find_item(potatos, self.player).name == potatos:
            slot_data["potatos_inplace"] = True
            
        return slot_data
