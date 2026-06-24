"""
Archipelago init file for Mario Kart Double Dash!!
"""
import logging
import math
from typing import Any

from BaseClasses import Region, ItemClassification, Tutorial
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import Component, components, icon_paths, launch_subprocess

from . import game_data, locations, items, regions, version
from .items import MkddItem
from .locations import MkddLocation, MkddLocationData
from .options import MkddOptions
from .regions import MkddRegionData
from .rules import MkddRules
from .settings import MkddSettings

class MkddWebWorld(WebWorld):
    theme = "ocean"
    option_groups = options.option_groups
    tutorials = [
        Tutorial(
            tutorial_name="Setup Guide",
            description="A guide to setting up Mario Kart Double Dash for MultiworldGG.",
            language="English",
            file_name="setup_en.md",
            link="setup/en",
            authors=["aXu"],
        )
    ]


class MkddWorld(World):
    """
    The fourth entry in Mario Kart series, Double Dash shakes up the gameplay by introducing 2 drivers per vehicle.
    """
    game = version.get_game_name()
    web = MkddWebWorld()

    options_dataclass = MkddOptions
    options: MkddOptions
    settings: MkddSettings

    item_name_to_id = items.name_to_id
    item_name_groups = items.groups
    location_name_to_id = locations.name_to_id
    location_name_groups = locations.groups

    # Universal Tracker.
    ut_can_gen_without_yaml = True
    glitches_item_name = items.SKIP_DIFFICULTY

    def __init__(self, world, player):
        self.current_locations: list[MkddLocationData] = []
        self.current_regions: dict[str, MkddRegionData] = {}
        self.current_entrances: set[str] = set()

        self.cups_courses: list[list[int]] = []
        self.character_item_total_weights: dict[str, list[int]] = {}
        self.global_items_total_weights: list[int] = []

        self.trophy_requirement: int = 0

        self.logger: logging.Logger = logging.getLogger("MKDD Logger")
        super(MkddWorld, self).__init__(world, player)

    def generate_early(self):
        # Calculate max number of trophies.
        max_requirement: int = self.options.shuffle_extra_trophies.value
        if self.options.grand_prix_trophies:
            max_requirement += 16
        if max_requirement == 0:
            self.options.shuffle_extra_trophies.value = 1
            self.logger.warning(f"{self.player_name}: No trophies in the pool, adding 1.")
        self.trophy_requirement = max(1, int(max_requirement * self.options.trophy_requirement_percent / 100))

        # Universal Tracker passthrough.
        if hasattr(self.multiworld, "re_gen_passthrough"):
            slot_data: dict = self.multiworld.re_gen_passthrough["Mario Kart Double Dash"]
            self.options.update_from_slot_data(slot_data)
            self.trophy_requirement = slot_data["trophy_requirement"]


    def create_regions(self) -> None:
        # Course shuffle (entrance rando). If using Universal Tracker, get shuffled tracks from slot data.
        # Course order is kept in a list[list[int]], where first index is cup, and second index points to a course inside that cup.
        if hasattr(self.multiworld, "re_gen_passthrough"):
            slot_data = self.multiworld.re_gen_passthrough["Mario Kart Double Dash"]
            self.cups_courses = slot_data["cups_courses"]
        else:
            all_courses: list[int] = list(range(16))
            if self.options.course_shuffle == options.CourseShuffle.option_shuffle_once:
                self.random.shuffle(all_courses)
            self.cups_courses: list[list[int]] = []
            for i in range(0, 16, 4):
                self.cups_courses.append([
                    all_courses[i],
                    all_courses[i + 1],
                    all_courses[i + 2],
                    all_courses[i + 3],
                ])

        # Create regions.
        for region_name, region_data in regions.data_table.items():
            if self.options.goal == options.Goal.option_trophies and region_name == game_data.CUPS[game_data.CUP_ALL_CUP_TOUR]:
                continue
            if self.options.time_trials == options.TimeTrials.option_disable and regions.TAG_TIME_TRIALS in region_data.tags:
                continue
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)
            self.current_regions[region_name] = region_data

        for region_name, region_data in self.current_regions.items():
            # Connect regions.
            region = self.get_region(region_name)
            region.add_exits([exit for exit in region_data.connecting_regions if exit in self.current_regions.keys()])
            if region_name in game_data.NORMAL_CUPS:
                cup_no = game_data.CUPS.index(region_name)
                region.add_exits([game_data.RACE_COURSES[self.cups_courses[cup_no][i]].name + " GP" for i in range(4)])
            self.current_entrances.update([e.name for e in region.exits])

            # Create locations.
            for id, location_data in enumerate(locations.data_table):
                if self.options.time_trials != options.TimeTrials.option_include_staff_ghosts and locations.TAG_TT_GHOST in location_data.tags:
                    continue
                if not self.options.grand_prix_trophies and locations.TAG_CUP_TROPHY in location_data.tags:
                    continue
                if locations.TAG_ITEM_BOX in location_data.tags:
                    if not self.options.add_custom_item_boxes and locations.TAG_ITEM_BOX_CUSTOM in location_data.tags:
                        continue
                    match self.options.item_boxes_as_locations:
                        case options.ItemBoxesAsLocations.option_disabled:
                            continue
                        case options.ItemBoxesAsLocations.option_interesting_locations:
                            if locations.TAG_ITEM_BOX_INTERESTING not in location_data.tags:
                                continue
                        case options.ItemBoxesAsLocations.option_box_groups:
                            if locations.TAG_ITEM_BOX_GROUP not in location_data.tags:
                                continue
                        case options.ItemBoxesAsLocations.option_boxsanity:
                            if locations.TAG_ITEM_BOX_SANITY not in location_data.tags:
                                continue
                            if self.options.add_custom_item_boxes and locations.TAG_ITEM_BOX_REPLACEABLE in location_data.tags:
                                continue
                if not self.options.shortcuts_as_locations and locations.TAG_SHORTCUT in location_data.tags:
                    continue
                if id > 0 and location_data.region == region_name:
                    region.add_locations({location_data.name: id})
                    self.current_locations.append(location_data)
        
        # Locked items.
        if self.options.grand_prix_trophies:
            for cup in game_data.NORMAL_CUPS:
                for vehicle_class in range(4):
                    self.get_location(locations.get_loc_name_trophy(cup, vehicle_class))\
                        .place_locked_item(self.create_item(items.TROPHY))
        if self.options.goal == options.Goal.option_all_cup_tour:
            self.get_location(locations.TROPHY_GOAL).place_locked_item(self.create_item(game_data.CUPS[game_data.CUP_ALL_CUP_TOUR]))
            self.get_location(locations.WIN_ALL_CUP_TOUR).place_locked_item(self.create_item("Victory"))
        elif self.options.goal == options.Goal.option_trophies:
            self.get_location(locations.TROPHY_GOAL).place_locked_item(self.create_item("Victory"))
        
    
    def _random_from(self, pool: list[str], count: int = 1) -> list[str]:
        """Returns random choices from given pool, taking into account player defined starting inventory."""
        ret: list[str] = []
        current_count: int = 0
        for item in self.options.start_inventory_from_pool:
            if item in pool:
                pool.remove(item)
                current_count += 1
        while current_count < count:
            item_name: str = self.random.choice(pool)
            ret.append(item_name)
            pool.remove(item_name)
            current_count += 1
        return ret


    def create_items(self) -> None:
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))
        # (item_name, count)
        precollected: list[str] = []
        # Give 1 cup, can't be All Star Cup.
        precollected.extend(self._random_from(game_data.NORMAL_CUPS.copy()))
        # Give 1 time trial track.
        if self.options.time_trials != options.TimeTrials.option_disable:
            precollected.extend(self._random_from([items.get_item_name_tt_course(c.name) for c in game_data.RACE_COURSES]))
        # Give 2 random characters to begin.
        precollected.extend(self._random_from([character.name for character in game_data.CHARACTERS], 2))
        # Give 1 kart in each weight class.
        for weight in range(3):
            precollected.extend(self._random_from([kart.name for kart in game_data.KARTS if kart.weight == weight]))
        if not self.options.speed_upgrades:
            precollected.append(items.PROGRESSIVE_ENGINE)
            # Set minimum difficulty on "hard", otherwise the seed can be unbeatable.
            if self.options.logic_difficulty.value < game_data.ENGINE_UPGRADE_USEFULNESS:
                self.options.logic_difficulty.value = game_data.ENGINE_UPGRADE_USEFULNESS
                self.logger.warning(f"{self.player_name}: No engine upgrades are available, setting difficulty to hard.")
        for item in precollected:
            self.multiworld.push_precollected(self.create_item(item))

        # Generic items by predetermined counts.
        item_pool: list[MkddItem] = []
        for item in items.data_table:
            if self.options.time_trials == options.TimeTrials.option_disable and (item.item_type == items.ItemType.TT_COURSE or item.name == items.PROGRESSIVE_TIME_TRIAL_ITEM):
                continue
            if item.classification != ItemClassification.filler:
                count = item.count
                count -= precollected.count(item.name)
                for i in range(count):
                    item_pool.append(self.create_item(item.name))
        
        for i in range(self.options.shuffle_extra_trophies):
            item_pool.append(self.create_item(items.TROPHY))

        if self.options.speed_upgrades:
            for i in range(3):
                item_pool.append(self.create_item(items.PROGRESSIVE_ENGINE))
        
        # Kart upgrades generation.
        if self.options.kart_upgrades > 0:
            kart_weights = [5 for _ in game_data.KARTS]
            upgrade_weights = [math.ceil(self.options.kart_upgrades / len(game_data.KART_UPGRADES)) for _ in game_data.KART_UPGRADES]
            up_karts = self.random.sample(game_data.KARTS, self.options.kart_upgrades, counts = kart_weights)
            upgrades = self.random.sample(game_data.KART_UPGRADES, self.options.kart_upgrades, counts = upgrade_weights)
            for i in range(self.options.kart_upgrades):
                item_pool.append(self.create_item(items.get_item_name_kart_upgrade(upgrades[i].name, up_karts[i].name)))

        # Item box item generation.
        # Give mostly bad items as global items.
        items_left: list[game_data.Item] = [item for item in game_data.ITEMS if item != game_data.ITEM_NONE]
        weights: list[str] = [1000 - item.usefulness ** 3 for item in game_data.ITEMS if item != game_data.ITEM_NONE]
        global_items: list[game_data.Item] = []
        for i in range(self.options.items_for_everybody):
            item = self.random.sample(items_left, 1, counts = weights)[0]
            item_pool.append(self.create_item(items.get_item_name_character_item(None, item.name)))
            global_items.append(item)
            idx = items_left.index(item)
            items_left.pop(idx)
            weights.pop(idx)

        # If there's too much global items there's going to be multiples.
        # Make the pool bigger to avoid every character having the same items.
        if len(items_left) < self.options.start_items_per_character + self.options.items_per_character:
            items_left = [item for item in game_data.ITEMS if item != game_data.ITEM_NONE]
        # Character specific items.
        # Use items that aren't used as global items.
        items_left_characters_pool: list[game_data.Item] = items_left.copy()
        weights = [1 for _ in items_left]
        items_per_character: dict[game_data.Character, list[game_data.Item]] = {character:[] for character in game_data.CHARACTERS}
        for i in range(self.options.start_items_per_character + self.options.items_per_character):
            for character in game_data.CHARACTERS:
                # Try rolling for unique items.
                for j in range(50):
                    item = self.random.sample(items_left, 1, counts = weights)[0]
                    if item not in items_per_character[character]:
                        break
                    # If item hasn't been found after 10 tries, try refilling the pool.
                    elif j == 10:
                        items_left = items_left_characters_pool.copy()
                        weights = [10 - item.usefulness for item in items_left]

                items_per_character[character].append(item)
                if i < self.options.start_items_per_character:
                    self.multiworld.push_precollected(self.create_item(items.get_item_name_character_item(character.name, item.name)))
                else:
                    item_pool.append(self.create_item(items.get_item_name_character_item(character.name, item.name)))
                idx = items_left.index(item)
                weights[idx] -= 1
                if weights[idx] == 0:
                    items_left.pop(idx)
                    weights.pop(idx)
                if len(items_left) == 0:
                    # Refill the pool with some balancing.
                    items_left = items_left_characters_pool.copy()
                    weights = [10 - item.usefulness for item in items_left]
        

        self.character_item_total_weights = {character.name:[] for character in game_data.CHARACTERS}
        for i in range(8):
            self.global_items_total_weights.append(sum([item.get_weight(i, self.options.frantic_items) for item in global_items]))
            for character in game_data.CHARACTERS:
                self.character_item_total_weights[character.name].append(
                    sum([item.get_weight(i, self.options.frantic_items) for item in items_per_character[character]])
                )

        remove_items: bool = True
        ensure_star: bool = True
        if len(item_pool) > total_locations:
            self.logger.warning(f"{self.player_name}: Too many items, removing {len(item_pool) - total_locations} items from the pool.")
        while remove_items or ensure_star:
            # Remove some items if there are more items than locations.
            while len(item_pool) > total_locations:
                item: items.MkddItem = self.random.choice(item_pool)
                item_type: items.ItemType = items.data_table[item.code].item_type
                if item_type == items.ItemType.KART_UPGRADE:
                    item_pool.remove(item)
                if item_type == items.ItemType.ITEM_UNLOCK:
                    item_pool.remove(item)
                    ensure_star = True
            remove_items = False
            
            # In case the user has specified no items, force at least one boost item for all locations be reachable.
            if self.options.shortcuts_as_locations and ensure_star:
                for item in item_pool:
                    item_data: items.MkddItemData = items.data_table[item.code]
                    if (
                            item_data.item_type == items.ItemType.ITEM_UNLOCK
                            and item_data.meta["item"] == game_data.ITEM_STAR):
                        ensure_star = False
                        break
                if ensure_star:
                    item_pool.append(self.create_item(items.get_item_name_character_item(game_data.CHARACTERS[0].name, game_data.ITEM_STAR.name)))
                    remove_items = True
            ensure_star = False

        remaining_item_count = total_locations - len(item_pool)
        trap_count = int(remaining_item_count * self.options.trap_chance / 100)
        traps = [
            items.BANANA_RAIN_TRAP,
            items.SHELL_RAIN_TRAP,
            items.BOMB_RAIN_TRAP,
            items.OVERLAPPING_START_TRAP,
        ]
        trap_weights = [
            self.options.banana_rain_trap_weight.value,
            self.options.shell_rain_trap_weight.value,
            self.options.bomb_rain_trap_weight.value,
            self.options.overlapping_start_trap_weight.value,
        ]
        item_pool += [self.create_item(self.random.sample(traps, 1, counts=trap_weights)[0]) for _ in range(trap_count)]
        item_pool += [self.create_item(self.get_filler_item_name()) for _ in range(remaining_item_count - trap_count)]
        
        self.multiworld.itempool += item_pool

    def create_item(self, name: str) -> MkddItem:
        idx = items.name_to_id[name]
        item_data = items.data_table[idx]
        return MkddItem(name, item_data.classification, idx, self.player)

    def get_filler_item_name(self) -> str:
        return items.RANDOM_ITEM
    
    def set_rules(self) -> None:
        rules = MkddRules(self)
        rules.set_rules()
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
    
    def collect(self, state, item) -> bool:
        change = super().collect(state, item)
        if change:
            rules.add_item(state, self.player, item)
        return change

    def remove(self, state, item) -> bool:
        change = super().remove(state, item)
        if change:
            rules.add_item(state, self.player, item, -1)
        return change

    def extend_hint_information(self, hint_data: dict[int, dict[int, str]]):
        hints: dict[int, str] = {}
        for course_no, course in enumerate(game_data.RACE_COURSES):
            entrance: str = ""
            for cup_no, cup in enumerate(self.cups_courses):
                if course_no in cup:
                    entrance = game_data.CUPS[cup_no]
                    break
            for loc in self.multiworld.get_locations(self.player):
                if course.name in locations.data_table[loc.address].tags:
                    hints[loc.address] = entrance
        hint_data[self.player] = hints

    def fill_slot_data(self) -> dict[str, Any]:
        # Fill in lap data into custom lap table.
        # Priority: custom > short > vanilla.
        new_lap_counts: dict[str, int] = {}
        for course in game_data.RACE_COURSES:
            if course.name in self.options.custom_lap_counts:
                new_lap_counts[course.name] = self.options.custom_lap_counts[course.name]
            elif self.options.shorter_courses:
                new_lap_counts[course.name] = int(math.ceil(course.laps * 2 / 3))
            else:
                new_lap_counts[course.name] = course.laps
        self.options.custom_lap_counts.value = new_lap_counts
        return {
            "version": version.get_version(),
            "trophy_requirement": self.trophy_requirement,
            "cups_courses": self.cups_courses,
            "character_item_total_weights": self.character_item_total_weights,
            "global_items_total_weights": self.global_items_total_weights,
            **self.options.to_slot_data(),
        }
    
    # Rerun Universal Tracker with received options.
    @staticmethod
    def interpret_slot_data(slot_data: dict[str:Any]) -> dict[str:Any]:
        return slot_data


def launch_client(*args):
    from .mkdd_client import main
    launch_subprocess(main, name="MKDD Client", args=args)

icon_paths["MKDD"] = "ap:worlds.mario_kart_double_dash/images/icon.png"

components.append(
    Component(
        "Mario Kart Double Dash Client",
        func=launch_client,
        game_name=version.get_game_name(),
        icon="MKDD",
        supports_uri=True
    )
)
