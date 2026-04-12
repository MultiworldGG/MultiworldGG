"""
This module serves as an entrypoint into the Rabi-Ribi AP world.
"""
import math
import logging
import settings
from collections import defaultdict
from itertools import chain
from typing import Any, ClassVar, Dict, List, Optional, Set, TextIO, Union
from BaseClasses import ItemClassification, MultiWorld, Tutorial
from Fill import swap_location_item
from Options import Accessibility, OptionError, Toggle
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, Type, components, launch_subprocess
from .existing_randomizer.dataparser import RandomizerData
from .existing_randomizer.randomizer import parse_args
from .items import RabiRibiItem, RabiRibiItemData, item_data_table, item_groups, shufflable_gift_items, shufflable_gift_items_plurkwood, item_table, filler_items, get_base_item_list
from .locations import all_locations, location_groups
from .names import ItemName, LocationName
from .options import RabiRibiOptions
from .regions import RegionHelper
from .utility import (
    get_rabi_ribi_base_id,
    convert_existing_rando_name_to_ap_name
)
from . import ut_helpers

logger = logging.getLogger('Rabi-Ribi')

def launch_client():
    """Launch a rabi ribi client instance"""
    from worlds.rabi_ribi.client.client import launch
    launch_subprocess(launch, name="RabiRibiClient")

components.append(Component(
    "Rabi-Ribi Client",
    func=launch_client,
    component_type=Type.CLIENT
))

class RabiRibiSettings(settings.Group):
    class GameInstallationPath(settings.UserFolderPath):
        """
        The installation folder of the game.
        """
        description = "Rabi-Ribi Installation Path"

    class UTPackPath(settings.FilePath):
        """
        The Poptracker pack for Rabi-Ribi.
        """
        description = "Rabi-Ribi Poptracker Path"
        required = False

    game_installation_path: GameInstallationPath = GameInstallationPath("C:/Program Files (x86)/Steam/steamapps/common/Rabi-Ribi")
    ut_pack_path : Union[UTPackPath, str] = UTPackPath()

class RabiRibiWeb(WebWorld):
    """Web integration for Rabi-Ribi"""
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Rabi-Ribi integration for MultiworldGG multiworld games.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Phie", "PsyMarth"]
    )]

class RabiRibiWorld(World):
    """
    Rabi-Ribi is a hybrid Bullet-Hell Metroidvania developped by CreSpirit and GameYue,
    released in 2016. It follows bunny-girl Erina and her fairy companion Ribbon in this
    cute, action-packed, and possibly pretty difficult adventure.
    """
    game: str = "Rabi-Ribi"
    options_dataclass = RabiRibiOptions
    options: RabiRibiOptions
    settings: ClassVar[RabiRibiSettings]
    web: WebWorld = RabiRibiWeb()

    base_id: int = get_rabi_ribi_base_id()
    topology_present: bool = False

    item_name_groups: Dict[str, Set[str]] = item_groups
    location_name_groups: Dict[str, Set[str]] = location_groups

    item_name_to_id = item_table
    location_name_to_id: Dict[str, int] = all_locations

    total_locations: int
    required_egg_count: int
    start_location: str
    picked_templates: List[str]
    map_transition_shuffle_order: List[int]
    map_transition_shuffle_spoiler: List[str]
    filler_items: Optional[List[str]] = None
    existing_randomizer_args: Any
    randomizer_data: RandomizerData

    # Universal Tracker Settings
    ut_can_gen_without_yaml = True
    glitches_item_name = ItemName.glitched_logic
    tracker_world = ut_helpers.TRACKER_WORLD

    def generate_early(self) -> None:
        """Set world specific generation properties"""
        # Universal Tracker: Load options from slot data instead of YAML
        ut_helpers.apply_options_from_slot_data_if_available(self)

        if self.options.encourage_eggs_in_late_spheres.value and self.options.rainbow_shot_in_logic.value:
            raise OptionError(f"Rabi-Ribi: Rainbow Egg In Logic is not compatible with Encourage Eggs in Late Spheres. "
                              f"Player {self.player} ({self.player_name}) needs to disable one of these options.")

        self.existing_randomizer_args = self._convert_options_to_existing_randomizer_args()
        self.randomizer_data = RandomizerData(self.existing_randomizer_args)

        # Will be configurable later, but for now always force eggs to be local
        self.options.local_items.value.add(ItemName.easter_egg)

    def create_item(self, name: str, force_classification: Optional[ItemClassification] = None) -> RabiRibiItem:
        """Create a Rabi-Ribi item for this player"""
        # Universal Tracker: Allow creation of a fake event to represent out of logic checks
        if name == ItemName.glitched_logic:
            return RabiRibiItem(name, ItemClassification.progression, None, self.player)

        data: RabiRibiItemData = item_data_table[name]
        classification = force_classification if force_classification is not None else data.classification
        return RabiRibiItem(name, classification, data.code, self.player)

    def create_event(self, name: str) -> RabiRibiItem:
        """Create a Rabi-Ribi event to help logic"""
        return RabiRibiItem(name, ItemClassification.progression, None, self.player)

    def create_regions(self) -> None:
        """
        Define regions and locations.
        This also defines access rules for the regions and locations.
        """
        self.topology_present = bool(self.options.shuffle_map_transitions.value)

        region_helper = RegionHelper(self)

        # Generate a world seed using the existing randomizer
        if ut_helpers.should_regenerate_seed_for_universal_tracker(self):
            # Universal Tracker: Regenerate the seed used on the connected server
            passthrough = self.multiworld.re_gen_passthrough["Rabi-Ribi"] # type: ignore
            region_helper.regenerate_seed_for_universal_tracker(passthrough)
        else:
            # Use standard generation
            region_helper.generate_seed()

        region_helper.set_regions()
        region_helper.connect_regions()
        self.total_locations = region_helper.set_locations()
        region_helper.set_events()

        region_helper.configure_slot_data()
        region_helper.configure_region_spoiler_log_data()

    def get_filler_item_name(self) -> str:
        """Called when the item pool needs to be filled with additional items to match location count."""
        if self.filler_items is None:
            # Create a list of lists for every potion, then flatten and shuffle
            all_potions_grouped = [([key] * value) for key, value in filler_items.items()]
            self.filler_items = list(chain(*all_potions_grouped))
            self.random.shuffle(self.filler_items)
        if len(self.filler_items) == 0:
            # All potions placed
            return ItemName.nothing
        return self.filler_items.pop(0)

    def create_items(self) -> None:
        base_item_list = get_base_item_list(self.options, self.randomizer_data)
        self.multiworld.itempool.extend(map(self.create_item, base_item_list))

        max_egg_locations_in_pool = self.total_locations - len(base_item_list)
        total_egg_count = min(max_egg_locations_in_pool, self.options.max_number_of_easter_eggs.value)
        self.required_egg_count = max(math.floor(total_egg_count * (self.options.percentage_of_easter_eggs.value / 100.0)), 1)
        filler_egg_count = total_egg_count - self.required_egg_count

        self.multiworld.itempool.extend([self.create_item(ItemName.easter_egg) for _ in range(self.required_egg_count)])
        self.multiworld.itempool.extend([self.create_item(ItemName.easter_egg, ItemClassification.useful) for _ in range(filler_egg_count)])

        junk = self.total_locations - len(base_item_list) - total_egg_count
        self.multiworld.itempool += [self.create_item(self.get_filler_item_name()) for _ in range(junk)]

    def fill_slot_data(self) -> dict:
        return {
            "required_egg_count": self.required_egg_count,
            "attackMode": self.options.attack_mode.value,
            "apply_beginner_mod": bool(self.options.apply_beginner_mod.value),
            "include_plurkwood": bool(self.options.include_plurkwood.value),
            "include_warp_destination": bool(self.options.include_warp_destination.value),
            "include_post_game": bool(self.options.include_post_game.value),
            "include_post_irisu": bool(self.options.include_post_irisu.value),
            "include_halloween": bool(self.options.include_halloween.value),
            "picked_templates": self.picked_templates,
            "map_transition_shuffle_order": self.map_transition_shuffle_order,
            "start_location": self.start_location,
            "shuffle_music": bool(self.options.shuffle_music.value),
            "shuffle_backgrounds": bool(self.options.shuffle_backgrounds.value),
            "allow_laggy_backgrounds": bool(self.options.allow_laggy_backgrounds.value),
            "allow_difficult_backgrounds": bool(self.options.allow_difficult_backgrounds.value),
            "shuffle_backgrounds": bool(self.options.shuffle_backgrounds.value),
            "death_link": bool(self.options.death_link.value),
            "options": self.options.as_dict(
                "knowledge",
                "trick_difficulty",
                "block_clips_required",
                "semi_solid_clips_required",
                "zips_required",
                "darkness_without_light_orb",
                "underwater_without_water_orb",
                "carrot_shooter_in_logic",
                "event_warps_in_logic",
                "include_plurkwood",
                "include_warp_destination",
                "include_post_game",
                "include_post_irisu",
                "include_halloween",
                "number_of_constraint_changes",
                "shuffle_map_transitions",
                "shuffle_start_location",
                "max_number_of_easter_eggs",
                "percentage_of_easter_eggs",)
        }

    def set_rules(self) -> None:
        """
        Set remaining rules (for now this is just the win condition).
        """
        self.multiworld.completion_condition[self.player] = \
            lambda state: state.has(ItemName.easter_egg, self.player, self.required_egg_count)

    def write_spoiler_header(self, spoiler_handle: TextIO) -> None:
        if self.options.shuffle_start_location.value:
            spoiler_handle.write(f'\nStart Location ({self.player_name}): {self.start_location}')

        if self.options.shuffle_map_transitions.value:
            spoiler_handle.write(f'\n\nMap Transitions ({self.player_name}):\n')
            for entrance in self.map_transition_shuffle_spoiler:
                spoiler_handle.write(f'\n{entrance}')

        if self.options.number_of_constraint_changes.value > 0:
            spoiler_handle.write(f'\n\nApplied Map Constraints ({self.player_name}):\n')
            for template in self.picked_templates:
                spoiler_handle.write(f'\n{convert_existing_rando_name_to_ap_name(template)}')

    def _convert_options_to_existing_randomizer_args(self):
        args = parse_args()
        args.ap_options = self.options
        args.open_mode = True
        args.shuffle_gift_items = True
        args.shuffle_map_transitions = self.options.shuffle_map_transitions.value
        args.shuffle_start_location = self.options.shuffle_start_location.value
        args.constraint_changes = self.options.number_of_constraint_changes.value

        return args

    @staticmethod
    def _handle_encourage_eggs_in_late_spheres(multiworld: MultiWorld):
        worlds_with_option_enabled = set([
            world.player for world in multiworld.get_game_worlds("Rabi-Ribi")
            if isinstance(world, RabiRibiWorld) and world.options.encourage_eggs_in_late_spheres.value
        ])
        rr_player_spheres = defaultdict(list)
        for sphere in multiworld.get_spheres():
            # For minimal accessibility, get_spheres() returns an empty sphere
            # before returning a sphere containing unreachable locations
            if len(sphere) == 0:
                break
            new_player_spheres = defaultdict(list)
            for location in sphere:
                if location.game == "Rabi-Ribi" and location.player in worlds_with_option_enabled:
                    new_player_spheres[location.player].append(location)
            for player, sphere in new_player_spheres.items():
                rr_player_spheres[player].append(sphere)
        for player, spheres in rr_player_spheres.items():
            first_half_of_spheres = spheres[:len(spheres)//2]
            second_half_of_spheres = spheres[len(spheres)//2:]
            egg_locations_to_swap = []
            swappable_pool = []
            for sphere in first_half_of_spheres:
                for location in sphere:
                    if location.item.name == ItemName.easter_egg:
                        egg_locations_to_swap.append(location)
            for sphere in second_half_of_spheres:
                for location in sphere:
                    if location.item.classification == ItemClassification.filler:
                        swappable_pool.append(location)
            multiworld.random.shuffle(swappable_pool)
            for old_position, new_position in zip(egg_locations_to_swap, swappable_pool):
                swap_location_item(old_position, new_position, check_locked=False)

    @classmethod
    def stage_post_fill(cls, multiworld) -> None:
        cls._handle_encourage_eggs_in_late_spheres(multiworld)

    # Methods for the universal tracker, not called in standard gen
    @staticmethod
    def interpret_slot_data(slot_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        This method exists as a hook for Universal Tracker. When this method is implemented in a world, Universal Tracker
        will perform a second world generation attempt when the player connects to the server, allowing the world access
        to slot_data to set variables that were randomly assigned during generation.
        """
        # https://github.com/FarisTheAncient/Archipelago/blob/tracker/worlds/tracker/docs/re-gen-passthrough.md
        return slot_data