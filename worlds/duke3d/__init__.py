import io
import json
import math
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# Compatibility across Python versions
try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files  # noqa

from BaseClasses import ItemClassification, MultiWorld, Region
from worlds.AutoWorld import World

from . import resources
from .base_classes import D3DItem, D3DLevel, LocationDef
from .id import GAME_ID, local_id, net_id
from .items import all_items, item_groups
from .levels import all_episodes, all_levels
from .options import Difficulty, Duke3DOptions
from .rules import Rules
from .web_world import Duke3DWebWorld

with files(resources).joinpath("id_map.json").open() as id_file:
    game_ids = json.load(id_file)


class D3DWorld(World):
    """
    Duke Nukem 3D is a 1996 first-person shooter featuring the adventures of the titular Duke Nukem, 
    who fights against an alien invasion on Earth, in a setting with unique risqué humor, a mix of pop-culture 
    satire and lampooning of over-the-top Hollywood action heroes.
    """

    game = "Duke Nukem 3D"
    author: str = "rand(0)"
    build_game_id = GAME_ID
    game_full_name = "Duke Nukem 3D"
    item_name_to_id = {
        name: net_id(loc_id) for name, loc_id in game_ids["items"].items()
    }
    location_name_to_id = {
        name: net_id(loc_id) for name, loc_id in game_ids["locations"].items()
    }
    item_name_groups = item_groups
    id_checksum = game_ids["checksum"]
    options_dataclass = Duke3DOptions
    options: Duke3DOptions
    web = Duke3DWebWorld()

    def __init__(self, world: MultiWorld, player: int):
        self.included_levels: List[D3DLevel] = []
        self.starting_levels: List[D3DLevel] = []
        self.used_locations: Set[str] = set()
        # Add the id checksum of our location and item ids for consistency check with clients
        self.slot_data: Dict[str, Any] = {
            "checksum": self.id_checksum,
            "settings": {"dynamic": {}, "maximum": {}},
        }
        self.rules: Optional[Rules] = None
        # Filled later from options
        self.fuel_per_pickup: Dict[str, int] = {}
        self._target_density: Optional[int] = None

        super().__init__(world, player)

    @classmethod
    def local_id(cls, ap_id: int) -> int:
        return local_id(ap_id)

    @classmethod
    def net_id(cls, short_id: int) -> int:
        return net_id(short_id)

    @property
    def target_density(self) -> int:
        """
        Cached version of _target_density, so we don't constantly calculate it
        """
        if self._target_density is None:
            density = self.options.location_density
            if density == self.options.location_density.option_balanced:
                # bump up the value by 1 if secret areas are not enabled
                if not self.options.include_secrets and self.options.goal in (
                    self.options.goal.option_beat_all_levels,
                    self.options.goal.option_beat_all_bosses,
                ):
                    density += 1
            self._target_density = density
        return self._target_density

    def use_location(self, location: Optional[LocationDef] = None) -> bool:
        """
        Specify if a certain location should be included, based on world settings
        """
        if location is None:
            return False
        if location.density > self.target_density:
            return False
        if (
            location.type == "sector"
            and self.options.goal
            in (
                self.options.goal.option_beat_all_levels,
                self.options.goal.option_beat_all_bosses,
            )
            and not self.options.include_secrets
        ):
            return False
        return True

    def calculate_levels(self):
        level_count = self.options.level_count
        # total number of starting levels to include, based on the total count
        if level_count < 6:
            start_count = 1
        elif level_count < 14:
            start_count = 2
        elif level_count < 24:
            start_count = 3
        else:
            start_count = 4
        shuffle_start = self.options.shuffle_starting_levels
        goal_bosses = self.options.goal == self.options.goal.option_beat_all_bosses
        level_candidates = []

        # Shuffle episodes so we pick random start levels if the start count is lower than the
        episode_options = [1, 2, 3, 4]
        ep_option_reference = [
            self.options.episode1,
            self.options.episode2,
            self.options.episode3,
            self.options.episode4,
        ]
        self.multiworld.random.shuffle(episode_options)
        for episode_id in episode_options:
            if ep_option_reference[episode_id - 1]:
                episode = all_episodes[episode_id - 1]
                if not shuffle_start and len(self.starting_levels) < start_count:
                    # add the first level to the starting levels, and the rest into the randomize pool
                    self.starting_levels.append(episode.levels[0])
                    self.included_levels.append(episode.levels[0])
                    episode_pool = episode.levels[1 : episode.maxlevel]
                else:
                    episode_pool = episode.levels[: episode.maxlevel]
                # If our goal is to kill bosses, include the boss levels!
                if goal_bosses:
                    for level in episode_pool:
                        if level.has_boss:
                            self.included_levels.append(level)
                # If E1L7 is enabled, add it in
                if episode_id == 1 and self.options.include_e1l7:
                    episode_pool.append(episode.levels[-1])
                # extend our candidate pool to pull from with all remaining eligible levels
                level_candidates.extend(
                    [
                        level
                        for level in episode_pool
                        if level not in self.included_levels
                    ]
                )
        # randomize the levels so we can pull from them
        self.multiworld.random.shuffle(level_candidates)
        # if we have random starting levels, sample them from the start of the shuffled list
        # this conveniently excludes boss levels from being immediately unlocked in all bosses mode!
        if shuffle_start:
            self.starting_levels = level_candidates[:start_count]
        # and then fill the included levels to the desired count
        self.included_levels.extend(
            level_candidates[: level_count - len(self.included_levels)]
        )

    def define_dynamic_item_props(self, item_name: str, new_props: Dict[str, Any]):
        """
        Creates a dynamic item definition entry with updated props.

        This is useful for dynamically scaling numeric values of items based on difficulty settings
        """
        item = all_items[item_name]
        item_data = {
            "name": item.name,
            "type": item.type,
        }
        if item.persistent:
            item_data["persistent"] = True
        if item.unique:
            item_data["unique"] = True
        if item.silent:
            item_data["silent"] = True
        item_data.update(**item.props)
        item_data.update(**new_props)

        self.slot_data["settings"]["dynamic"][str(item.ap_id)] = item_data

    def generate_early(self) -> None:
        # difficulty settings
        self.fuel_per_pickup = {
            "Jetpack": self.options.fuel_per_jetpack.value,
            "Scuba Gear": self.options.fuel_per_scuba_gear.value,
            "Steroids": self.options.fuel_per_steroids.value,
        }
        self.define_dynamic_item_props(
            "Jetpack", {"capacity": self.fuel_per_pickup["Jetpack"]}
        )
        self.define_dynamic_item_props(
            "Jetpack Capacity", {"capacity": self.fuel_per_pickup["Jetpack"]}
        )
        self.define_dynamic_item_props(
            "Scuba Gear", {"capacity": self.fuel_per_pickup["Scuba Gear"]}
        )
        self.define_dynamic_item_props(
            "Scuba Gear Capacity", {"capacity": self.fuel_per_pickup["Scuba Gear"]}
        )
        self.define_dynamic_item_props(
            "Steroids", {"capacity": self.fuel_per_pickup["Steroids"]}
        )
        self.define_dynamic_item_props(
            "Steroids Capacity", {"capacity": self.fuel_per_pickup["Steroids"]}
        )

        # Configure rules
        self.rules = Rules(self)

        # Generate level pool
        self.calculate_levels()

        # Initial level unlocks
        for level in self.starting_levels:
            self.options.start_inventory.value[level.unlock] = 1
        for level in self.included_levels:
            if self.options.area_maps == self.options.area_maps.option_start_with:
                self.options.start_inventory.value[level.map] = 1
        self.slot_data["settings"]["difficulty"] = self.options.skill_level.value
        self.slot_data["settings"]["lock"] = {}
        if self.options.unlock_abilities:
            self.slot_data["settings"]["lock"].update(
                {
                    "crouch": True,
                    "jump": True,
                    "run": True,
                    "dive": True,
                }
            )
        if self.options.unlock_interact:
            self.slot_data["settings"]["lock"].update(
                {
                    "open": True,
                    "use": True,
                }
            )
        self.slot_data["settings"]["no_save"] = not self.options.allow_saving.value
        self.slot_data["settings"]["steroids_duration"] = self.fuel_per_pickup[
            "Steroids"
        ]

    def create_regions(self):
        self.used_locations = set()
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)
        for level in self.included_levels:
            level_region = level.create_region(self)
            self.used_locations |= level.used_locations
            menu_region.connect(level_region, None, self.rules.level(level))
        self.slot_data["locations"] = [
            self.location_name_to_id[loc] for loc in self.used_locations
        ]
        self.slot_data["levels"] = [
            self.item_name_to_id[level.unlock] for level in self.included_levels
        ]

        goal_exits = self.options.goal in {
            self.options.goal.option_beat_all_levels,
            self.options.goal.option_all,
        }
        goal_secrets = self.options.goal in {
            self.options.goal.option_collect_all_secrets,
            self.options.goal.option_all,
        }
        goal_bosses = self.options.goal == self.options.goal.option_beat_all_bosses
        goal_counts = {"Exit": 0, "Secret": 0, "Boss": 0}
        for level in self.included_levels:
            for location in level.locations.values():
                if location.name not in self.used_locations:
                    continue
                if goal_exits and location.type == "exit":
                    goal_counts["Exit"] += 1
                elif goal_secrets and location.type == "sector":
                    goal_counts["Secret"] += 1
                elif goal_bosses and location.type == "exit" and level.has_boss:
                    goal_counts["Boss"] += 1

        goal_percentage = self.options.goal_percentage
        if goal_percentage < 100:
            for goal_type in ("Exit", "Secret", "Boss"):
                goal_counts[goal_type] = math.ceil(
                    0.01 * goal_percentage * goal_counts[goal_type]
                )

        self.slot_data["goal"] = {
            "Exit": {"id": self.item_name_to_id["Exit"], "count": goal_counts["Exit"]},
            "Secret": {
                "id": self.item_name_to_id["Secret"],
                "count": goal_counts["Secret"],
            },
            "Boss": {"id": self.item_name_to_id["Boss"], "count": goal_counts["Boss"]},
        }
        self.multiworld.completion_condition[self.player] = (
            self.rules.count("Exit", goal_counts["Exit"])
            & self.rules.count("Secret", goal_counts["Secret"])
            & self.rules.count("Boss", goal_counts["Boss"])
        )

    WEAPON_NAMES = (
        "Pistol",
        "Shotgun",
        "Chaingun",
        "RPG",
        "Pipebomb",
        "Shrinker",
        "Devastator",
        "Tripmine",
        "Freezethrower",
        "Expander",
    )

    def create_item(self, item: str) -> D3DItem:
        item_def = all_items.get(item)
        if item_def.progression:
            classification = ItemClassification.progression
        elif item_def.persistent:
            classification = ItemClassification.useful
        elif item_def.type == "trap":
            classification = ItemClassification.trap
        else:
            classification = ItemClassification.filler
        ret = D3DItem(item, classification, self.item_name_to_id[item], self.player)
        return ret

    def create_event(self, event_name: str) -> D3DItem:
        return D3DItem(event_name, ItemClassification.progression, None, self.player)

    def get_filler_item_name(self) -> str:
        # This should never be required with the item pool calculations, so we don't need any junk ratio logic here
        return "Nothing"

    def create_junk(self, count: int) -> List[D3DItem]:
        difficulty = self.options.difficulty
        if difficulty == self.options.difficulty.option_extreme:
            ratios = {
                "Nothing": 40,
                "Pity Heal": 80,
                "Medpak": 30,
                "Armor": 10,
                "Atomic Health": 12,
                "Holo Duke": 7,
                "Chaingun Ammo": 3,
                "RPG Ammo": 3,
                "Devastator Ammo": 3,
                "Ego Boost": 2,
                "Buff Up": 1,
                "Sturdy Armor": 2,
                "Heavy Armor": 1,
                "First Aid Kit": 2,
                # Oh, you got lucky!
                "Shrinker Capacity": 1,
                "Expander Capacity": 1,
                "RPG Capacity": 1,
            }
            trap_ratios = {
                "Celebration Trap": 4,
                "Shrink Trap": 4,
                "Death Trap": 6,
                "Appreciation Trap": 2,
                "Paranoia Trap": 0,
                "Battlelord Trap": 6,
                "Caffeine Trap": 5,
                "Octabrain Trap": 2,
                "Lizard Trap": 6,
                "Busted!": 7,
                "Ooze Trap": 0,
            }
        elif difficulty == self.options.difficulty.option_hard:
            ratios = {
                "Pity Heal": 20,
                "Medpak": 40,
                "Armor": 30,
                "Atomic Health": 28,
                "First Aid Kit": 8,
                "Protective Boots": 4,
                "Ego Boost": 5,
                "Buff Up": 3,
                "Sturdy Armor": 5,
                "Heavy Armor": 3,
                "Plutonium Health": 2,
                # And some lucky additions!
                "RPG Capacity": 2,
                "Chaingun Capacity": 2,
                "Shrinker Capacity": 2,
                "Devastator Capacity": 2,
                "Steroids Capacity": 1,
                "Jetpack Capacity": 1,
            }
            trap_ratios = {
                "Celebration Trap": 3,
                "Shrink Trap": 3,
                "Death Trap": 4,
                "Appreciation Trap": 4,
                "Paranoia Trap": 2,
                "Battlelord Trap": 3,
                "Caffeine Trap": 7,
                "Octabrain Trap": 4,
                "Lizard Trap": 4,
                "Busted!": 4,
                "Ooze Trap": 2,
            }
        elif difficulty == self.options.difficulty.option_medium:
            ratios = {
                "Medpak": 20,
                "Armor": 20,
                "Atomic Health": 13,
                "Pistol Capacity": 5,
                "Ego Boost": 5,
                "Plutonium Health": 5,
                "Buff Up": 7,
                "Sturdy Armor": 5,
                "Heavy Armor": 7,
                "RPG Capacity": 3,
                "Chaingun Capacity": 3,
                "Shrinker Capacity": 2,
                "Expander Capacity": 2,
                "Devastator Capacity": 1,
                "First Aid Kit": 10,
                "Protective Boots": 5,
                "Steroids Capacity": 3,
                "Uranium Health": 2,
                # And some lucky additions!
                "Jetpack Capacity": 1,
                "Scuba Gear Capacity": 1,
            }
            trap_ratios = {
                "Celebration Trap": 3,
                "Shrink Trap": 2,
                "Death Trap": 2,
                "Appreciation Trap": 3,
                "Paranoia Trap": 4,
                "Battlelord Trap": 2,
                "Caffeine Trap": 5,
                "Octabrain Trap": 3,
                "Lizard Trap": 3,
                "Busted!": 2,
                "Ooze Trap": 6,
            }
        else:
            ratios = {
                "Armor": 20,
                "Atomic Health": 15,
                "Plutonium Health": 10,
                "Uranium Health": 5,
                "Ego Boost": 3,
                "Buff Up": 14,
                "Sturdy Armor": 3,
                "Heavy Armor": 14,
                "Pistol Capacity": 4,
                "RPG Capacity": 4,
                "Chaingun Capacity": 2,
                "Shrinker Capacity": 3,
                "Expander Capacity": 3,
                "Devastator Capacity": 2,
                "First Aid Kit": 15,
                "Protective Boots": 7,
                "Steroids Capacity": 5,
                "Jetpack Capacity": 2,
                "Scuba Gear Capacity": 2,
            }
            trap_ratios = {
                "Celebration Trap": 4,
                "Shrink Trap": 3,
                "Death Trap": 0,
                "Appreciation Trap": 4,
                "Paranoia Trap": 8,
                "Battlelord Trap": 0,
                "Caffeine Trap": 5,
                "Octabrain Trap": 2,
                "Lizard Trap": 3,
                "Busted!": 1,
                "Ooze Trap": 10,
            }
        # create sample lists
        pool = []
        for key, value in ratios.items():
            pool += [key] * value
        trap_pool = []
        for key, value in trap_ratios.items():
            trap_pool += [key] * value
        # and just generate items at the appropriate ratios
        trap_count = math.floor((self.options.trap_percentage / 100.0) * count)
        return [
            self.create_item(self.multiworld.random.choice(pool))
            for _ in range(count - trap_count)
        ] + [
            self.create_item(self.multiworld.random.choice(trap_pool))
            for _ in range(trap_count)
        ]

    def create_item_list(self, item_list: List[str]) -> List[D3DItem]:
        return [self.create_item(item) for item in item_list]

    DIFF_TO_REQ_MAPPING = {
        Difficulty.option_easy: {
            "Jetpack": (400, 800),
            "Scuba Gear": (2000, 3500),
            "Steroids": (150, 300),
        },
        Difficulty.option_medium: {
            "Jetpack": (300, 500),
            "Scuba Gear": (1250, 2000),
            "Steroids": (100, 200),
        },
        Difficulty.option_hard: {
            "Jetpack": (200, 300),
            "Scuba Gear": (400, 1000),
            "Steroids": (50, 50),
        },
        Difficulty.option_extreme: {
            "Jetpack": (200, 200),
            "Scuba Gear": (400, 400),
            "Steroids": (50, 50),
        },
    }

    def generate_inventories(
        self, inv_type: str
    ) -> Tuple[List[D3DItem], List[D3DItem]]:
        required, total = self.DIFF_TO_REQ_MAPPING.get(
            self.options.difficulty, self.options.difficulty.option_medium
        )[inv_type]

        required_cnt = math.ceil(float(required) / self.fuel_per_pickup[inv_type])
        total_cnt = math.ceil(float(total) / self.fuel_per_pickup[inv_type])

        # One base item and rest is capacity, unless we have progressive inventories
        progressive = self.options.progressive_inventories
        if progressive:
            main_name = f"Progressive {inv_type}"
            cap_name = main_name
        else:
            main_name = inv_type
            cap_name = f"{inv_type} Capacity"
        required_list = [self.create_item(main_name)] + [
            self.create_item(cap_name) for _ in range(required_cnt - 1)
        ]
        # Fill pool with capacity up to total amount
        useful_list = [
            self.create_item(cap_name) for _ in range(total_cnt - len(required_list))
        ]
        return required_list, useful_list

    # Tuples of starting max and target max
    DIFF_TO_MAX_MAPPING = {
        Difficulty.option_easy: {
            "Pistol": (200, 400),
            "Shotgun": (25, 60),
            "Chaingun": (150, 500),
            "RPG": (10, 40),
            "Pipebomb": (10, 25),
            "Shrinker": (10, 40),
            "Devastator": (20, 150),
            "Tripmine": (5, 15),
            "Freezethrower": (50, 250),
            "Expander": (30, 100),
        },
        Difficulty.option_medium: {
            "Pistol": (120, 300),
            "Shotgun": (20, 45),
            "Chaingun": (100, 350),
            "RPG": (5, 30),
            "Pipebomb": (5, 15),
            "Shrinker": (5, 20),
            "Devastator": (15, 100),
            "Tripmine": (3, 10),
            "Freezethrower": (40, 180),
            "Expander": (20, 75),
        },
        Difficulty.option_hard: {
            "Pistol": (80, 200),
            "Shotgun": (10, 25),
            "Chaingun": (75, 200),
            "RPG": (3, 20),
            "Pipebomb": (2, 10),
            "Shrinker": (3, 10),
            "Devastator": (10, 75),
            "Tripmine": (1, 5),
            "Freezethrower": (30, 125),
            "Expander": (15, 60),
        },
        Difficulty.option_extreme: {
            "Pistol": (48, 125),
            "Shotgun": (7, 15),
            "Chaingun": (50, 140),
            "RPG": (2, 15),
            "Pipebomb": (1, 5),
            "Shrinker": (1, 5),
            "Devastator": (10, 60),
            "Tripmine": (1, 3),
            "Freezethrower": (20, 90),
            "Expander": (10, 45),
        },
    }

    def useful_items_per_difficulty(self, available_slots: int) -> List[D3DItem]:
        if available_slots <= 0:
            # Out of space already, can abort
            return []

        ret_items = {}
        # We want about 35% of remaining slots to be filled with ammo expansions, so calculated the amount we get
        # for each of the 10 weapons
        expansions_per_weapon = math.ceil(available_slots * 0.035)
        for weapon in self.WEAPON_NAMES:
            start, target = self.DIFF_TO_MAX_MAPPING.get(
                self.options.difficulty, self.options.difficulty.option_medium
            )[weapon]
            self.slot_data["settings"]["maximum"][weapon.lower()] = start
            difference = target - start
            if difference <= 0:
                continue
            capacity_per = math.ceil(float(difference) / expansions_per_weapon)
            count = math.ceil(float(difference) / capacity_per)
            # configure the capacity for each upgrade dynamically
            self.define_dynamic_item_props(
                f"{weapon} Capacity",
                {"capacity": capacity_per, "ammo": math.ceil(capacity_per / 2.0)},
            )
            # and add the right count to our pool
            if self.options.progressive_weapons:
                ret_items[f"Progressive {weapon}"] = count
            else:
                ret_items[f"{weapon} Capacity"] = count

        # Is there a good comprehension for this?
        ret = []
        for key, count in ret_items.items():
            ret += [self.create_item(key) for _ in range(count)]
        return ret

    def create_items(self):
        itempool = []  # Absolutely mandatory progression items
        useful_items = (
            []
        )  # Stuff that should be in the world if there's enough locations
        used_locations = self.used_locations.copy()
        # Place goal items and level key cards
        # ToDo remove this code duplications
        goal_exits = self.options.goal in {
            self.options.goal.option_beat_all_levels,
            self.options.goal.option_all,
        }
        goal_secrets = self.options.goal in {
            self.options.goal.option_collect_all_secrets,
            self.options.goal.option_all,
        }
        goal_bosses = self.options.goal == self.options.goal.option_beat_all_bosses
        for level in self.included_levels:
            for location in level.locations.values():
                if (
                    goal_exits
                    and location.name in self.used_locations
                    and location.type == "exit"
                ):
                    self.multiworld.get_location(
                        location.name, self.player
                    ).place_locked_item(self.create_item("Exit"))
                    used_locations.remove(location.name)
                elif (
                    goal_secrets
                    and location.name in self.used_locations
                    and location.type == "sector"
                ):
                    self.multiworld.get_location(
                        location.name, self.player
                    ).place_locked_item(self.create_item("Secret"))
                    used_locations.remove(location.name)
                elif (
                    goal_bosses
                    and location.name in self.used_locations
                    and location.type == "exit"
                    and level.has_boss
                ):
                    self.multiworld.get_location(
                        location.name, self.player
                    ).place_locked_item(self.create_item("Boss"))
                    used_locations.remove(location.name)
            # create and fill event items
            for event in level.events:
                prefixed_event = f"{level.prefix} {event}"
                self.multiworld.get_location(
                    prefixed_event, self.player
                ).place_locked_item(self.create_event(prefixed_event))
            itempool += [self.create_item(item) for item in level.items]
            if level.unlock not in self.options.start_inventory.value:
                itempool.append(self.create_item(level.unlock))
            if self.options.area_maps == self.options.area_maps.option_unlockable:
                useful_items.append(self.create_item(level.map))

        if self.options.unlock_abilities:
            itempool += self.create_item_list(
                [
                    "Jump",
                    "Sprint",
                    "Crouch",
                ]
            )

        if self.options.unlock_interact:
            itempool += self.create_item_list(["Open", "Use"])

        # Add progression items
        progressive_weapons = self.options.progressive_weapons
        # Place explosive weapons into the required itempool
        if progressive_weapons:
            itempool += self.create_item_list(
                [
                    "Progressive RPG",
                    "Progressive Pipebomb",
                    "Progressive Tripmine",
                    "Progressive Devastator",
                ]
            )
        else:
            itempool += self.create_item_list(
                ["RPG", "Pipebomb", "Tripmine", "Devastator"]
            )
        # Get progression inventory based on difficulty settings
        required, useful = self.generate_inventories("Jetpack")
        itempool += required
        useful_items += useful
        required, useful = self.generate_inventories("Scuba Gear")
        # If no level requires diving we just place all of them in the useful list, as we don't care if they
        # get discarded for seeds with very restricted available location slots
        need_dive = False
        for level in self.included_levels:
            if level.must_dive:
                need_dive = True
                break
        if need_dive:
            itempool += required
        else:
            useful_items += required
        useful_items += useful
        required, useful = self.generate_inventories("Steroids")
        itempool += required
        useful_items += useful

        # Can fail now if we don't even have enough slots for our required items
        if len(itempool) > len(used_locations):
            raise RuntimeError(
                "Not enough locations for all mandatory items with these settings!"
            )

        # Add one copy of each remaining weapon to the pool
        if progressive_weapons:
            useful_items += self.create_item_list(
                [
                    "Progressive Shotgun",
                    "Progressive Chaingun",
                    "Progressive Shrinker",
                    "Progressive Freezethrower",
                    "Progressive Expander",
                ]
            )
        else:
            useful_items += self.create_item_list(
                ["Shotgun", "Chaingun", "Shrinker", "Freezethrower", "Expander"]
            )

        # count out remaining slots left to be filled
        open_slots = len(used_locations) - (len(itempool) + len(useful_items))
        useful_items += self.useful_items_per_difficulty(open_slots)

        if len(itempool) + len(useful_items) > len(used_locations):
            discarded = len(itempool) + len(useful_items) - len(used_locations)
            print(
                f"Had to discard {discarded} useful items from the pool: Not enough locations available"
            )

        # Add as much useful stuff as can fit
        # shuffle up the useful items so random ones get discarded if required
        self.multiworld.random.shuffle(useful_items)
        itempool.extend(useful_items[: len(used_locations) - len(itempool)])

        # Add filler
        itempool += self.create_junk(len(used_locations) - len(itempool))

        self.multiworld.itempool += itempool

    def fill_slot_data(self) -> Dict[str, Any]:
        return self.slot_data

    # Used to supply the Universal Tracker with level shuffle data
    def interpret_slot_data(self, slot_data: Dict[str, Any]):
        menu_region = self.multiworld.get_region("Menu", self.player)
        unlocklist = slot_data["levels"]
        for level in all_levels:
            if self.item_name_to_id[level.unlock] in unlocklist:
                level_region = level.create_region(self)
                menu_region.connect(level_region, None, self.rules.level(level))
                for event in level.events:
                    prefixed_event = f"{level.prefix} {event}"
                    event_loc = self.multiworld.get_location(
                        prefixed_event, self.player
                    )
                    event_loc.place_locked_item(self.create_event(prefixed_event))
