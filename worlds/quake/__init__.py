import json
import math
from random import Random
from .levels import SL, HIPSL, ROGUESL, MG1SL, DOPASL
from typing import Any, Dict, List, Optional, Set, Tuple
from BaseClasses import CollectionState, Tutorial

# Compatibility across Python versions
try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files  # noqa

from BaseClasses import ItemClassification, MultiWorld, Region
from worlds.AutoWorld import World, WebWorld

from . import resources
from .base_classes import Q1Item, Q1Level, LocationDef
from .id import GAME_ID, local_id, net_id
from .items import all_items, item_groups
from .levels import (
    all_episodes_q1,
    all_episodes_hip,
    all_episodes_rogue,
    all_episodes_mg1,
    all_episodes_dopa,
)
from .options import Difficulty, Q1Options
from .rules import Rules

with files(resources).joinpath("id_map.json").open() as id_file:
    game_ids = json.load(id_file)


class Q1Web(WebWorld):
    setup_en = Tutorial(
        "Setup Guide",
        "A guide to setting up the Quake 1 Randomizer for MultiworldGG",
        "English",
        "setup_en.md",
        "setup/en",
        ["rand(0)"]
    )

    tutorials = [setup_en]

class Q1World(World):
    """
    One of the most classic shooters of all time, now reimagined. Replace ALL the monsters and objects in a level with another of the same type. 
    That first Grunt you encounter in E1M1? Now it could be an Enforcer, a Knight... or maybe a Shambler!
    """

    game = "Quake 1"
    game_id = GAME_ID
    game_full_name = "Quake 1"

    item_name_to_id = {
        name: net_id(loc_id) for name, loc_id in game_ids["items"].items()
    }
    location_name_to_id = {
        name: net_id(loc_id) for name, loc_id in game_ids["locations"].items()
    }
    item_name_groups = item_groups
    id_checksum = game_ids["checksum"]
    options_dataclass = Q1Options
    options: Q1Options
    web = Q1Web()

    def __init__(self, world: MultiWorld, player: int):
        self.included_levels: List[Q1Level] = []
        self.starting_levels: List[Q1Level] = []
        self.used_locations: Set[str] = set()
        # Add the id checksum of our location and item ids for consistency check with clients
        self.slot_data: Dict[str, Any] = {
            "checksum": self.id_checksum,
            "settings": {"dynamic": {}, "maximum": {}},
        }
        self.rules: Optional[Rules] = None

        self.seed = getattr(world, "re_gen_passthrough", {}).get(
            "Quake 1", world.random.getrandbits(64)
        )

        print("__init__ world.random seed: ", self.seed)

        world.random = Random(self.seed)

        # store location spawn preset data as a list of dicts
        self.location_presets = [
            # iconic
            {
                "item_armor1": 100,
                "item_armor2": 100,
                "item_armorInv": 100,
                "weapon_lightning": 100,
                "weapon_nailgun": 100,
                "weapon_supernailgun": 100,
                "weapon_supershotgun": 100,
                "weapon_grenadelauncher": 100,
                "weapon_rocketlauncher": 100,
                "item_health (Small Medkit)": 0,
                "item_health (Large Medkit)": 0,
                "item_health (Megahealth)": 100,
                "item_cells": 0,
                "item_rockets": 0,
                "item_shells": 0,
                "item_spikes": 0,
                "item_artifact_envirosuit": 100,
                "item_artifact_invisibility": 100,
                "item_artifact_invulnerability": 100,
                "item_artifact_super_damage": 100,
                "item_key1": 100,
                "item_key2": 100,
                "item_sigil": 100,
                "item_weapon": 100,
                # hipnotic
                "item_artifact_empathy_shields": 100,
                "item_hornofconjuring": 100,
                "item_artifact_wetsuit": 100,
                "weapon_laser_gun": 100,
                "weapon_mjolnir": 100,
                "weapon_proximity_gun": 100,
                # rogue
                "item_sphere": 100,
                "item_random_powerup": 100,
                "item_powerup_belt": 100,
                "item_powerup_shield": 100,
                "item_flag": 100,
                "item_flag_team1": 100,
                "item_flag_team2": 100,
                "item_lava_spikes": 0,
                "item_multi_rockets": 0,
                "item_plasma": 0,
            },
            # balanced
            {
                "item_armor1": 100,
                "item_armor2": 100,
                "item_armorInv": 100,
                "weapon_lightning": 100,
                "weapon_nailgun": 100,
                "weapon_supernailgun": 100,
                "weapon_supershotgun": 100,
                "weapon_grenadelauncher": 100,
                "weapon_rocketlauncher": 100,
                "item_health (Small Medkit)": 25,
                "item_health (Large Medkit)": 25,
                "item_health (Megahealth)": 100,
                "item_cells": 25,
                "item_rockets": 25,
                "item_shells": 25,
                "item_spikes": 25,
                "item_artifact_envirosuit": 100,
                "item_artifact_invisibility": 100,
                "item_artifact_invulnerability": 100,
                "item_artifact_super_damage": 100,
                "item_key1": 100,
                "item_key2": 100,
                "item_sigil": 100,
                "item_weapon": 100,
                # hipnotic
                "item_artifact_empathy_shields": 100,
                "item_hornofconjuring": 100,
                "item_artifact_wetsuit": 100,
                "weapon_laser_gun": 100,
                "weapon_mjolnir": 100,
                "weapon_proximity_gun": 100,
                # rogue
                "item_sphere": 100,
                "item_random_powerup": 100,
                "item_powerup_belt": 100,
                "item_powerup_shield": 100,
                "item_flag": 100,
                "item_flag_team1": 100,
                "item_flag_team2": 100,
                "item_lava_spikes": 25,
                "item_multi_rockets": 25,
                "item_plasma": 25,
            },
            # dense
            {
                "item_armor1": 100,
                "item_armor2": 100,
                "item_armorInv": 100,
                "weapon_lightning": 100,
                "weapon_nailgun": 100,
                "weapon_supernailgun": 100,
                "weapon_supershotgun": 100,
                "weapon_grenadelauncher": 100,
                "weapon_rocketlauncher": 100,
                "item_health (Small Medkit)": 50,
                "item_health (Large Medkit)": 50,
                "item_health (Megahealth)": 100,
                "item_cells": 50,
                "item_rockets": 50,
                "item_shells": 50,
                "item_spikes": 50,
                "item_artifact_envirosuit": 100,
                "item_artifact_invisibility": 100,
                "item_artifact_invulnerability": 100,
                "item_artifact_super_damage": 100,
                "item_key1": 100,
                "item_key2": 100,
                "item_sigil": 100,
                "item_weapon": 100,
                # hipnotic
                "item_artifact_empathy_shields": 100,
                "item_hornofconjuring": 100,
                "item_artifact_wetsuit": 100,
                "weapon_laser_gun": 100,
                "weapon_mjolnir": 100,
                "weapon_proximity_gun": 100,
                # rogue
                "item_sphere": 100,
                "item_random_powerup": 100,
                "item_powerup_belt": 100,
                "item_powerup_shield": 100,
                "item_flag": 100,
                "item_flag_team1": 100,
                "item_flag_team2": 100,
                "item_lava_spikes": 50,
                "item_multi_rockets": 50,
                "item_plasma": 50,
            },
            # all
            {
                "item_armor1": 100,
                "item_armor2": 100,
                "item_armorInv": 100,
                "weapon_lightning": 100,
                "weapon_nailgun": 100,
                "weapon_supernailgun": 100,
                "weapon_supershotgun": 100,
                "weapon_grenadelauncher": 100,
                "weapon_rocketlauncher": 100,
                "item_health (Small Medkit)": 100,
                "item_health (Large Medkit)": 100,
                "item_health (Megahealth)": 100,
                "item_cells": 100,
                "item_rockets": 100,
                "item_shells": 100,
                "item_spikes": 100,
                "item_artifact_envirosuit": 100,
                "item_artifact_invisibility": 100,
                "item_artifact_invulnerability": 100,
                "item_artifact_super_damage": 100,
                "item_key1": 100,
                "item_key2": 100,
                "item_sigil": 100,
                "item_weapon": 100,
                # hipnotic
                "item_artifact_empathy_shields": 100,
                "item_hornofconjuring": 100,
                "item_artifact_wetsuit": 100,
                "weapon_laser_gun": 100,
                "weapon_mjolnir": 100,
                "weapon_proximity_gun": 100,
                # rogue
                "item_sphere": 100,
                "item_random_powerup": 100,
                "item_powerup_belt": 100,
                "item_powerup_shield": 100,
                "item_flag": 100,
                "item_flag_team1": 100,
                "item_flag_team2": 100,
                "item_lava_spikes": 100,
                "item_multi_rockets": 100,
                "item_plasma": 100,
            },
        ]

        super().__init__(world, player)

    def interpret_slot_data(self, slot_data: Dict[str, Any]):
        # If the seed is not specified in the slot data, this mean the world was generated before Universal Tracker support.
        seed_str = slot_data.get("ut_s")  # Get the string value
        if seed_str is not None:
            try:
                seed = int(seed_str)  # Try converting to an integer
            except ValueError:
                try:
                    seed = float(seed_str)  # If not an int, try float
                except ValueError:
                    print(
                        f"Could not convert '{seed_str}' to a number."
                    )  # If it's neither!
                    seed = 0
        else:
            print("Key 'ut_s' not found in slot_data.")
        return seed

    @classmethod
    def local_id(cls, ap_id: int) -> int:
        return local_id(ap_id)

    @classmethod
    def net_id(cls, short_id: int) -> int:
        return net_id(short_id)

    def use_location(self, location: Optional[LocationDef] = None) -> bool:
        """
        Specify if a certain location should be included, based on world settings.
        This filters items out by multiplayer spawns and secret-goal settings.
        """
        if location is None:
            return False
        if (
            location.classname != "trigger_changelevel"
            and location.classname != "trigger_secret"
        ):
            if location.mp and not self.options.include_mp_items:
                return False
        if (
            location.classname == "trigger_secret"
            and self.options.goal
            in (
                self.options.goal.option_beat_all_levels,
                self.options.goal.option_beat_all_bosses,
            )
            and not self.options.include_secrets
        ):
            return False
        # dont include all kills if the option is disabled
        if location.classname == "all_kills" and not self.options.include_allkills:
            return False
        return True

    def calculate_levels(self):

        level_count = self.options.level_count
        start_count = self.options.starting_level_count

        shuffle_start = self.options.shuffle_starting_levels
        goal_bosses = self.options.goal == self.options.goal.option_beat_all_bosses

        level_candidates = []

        # Shuffle episodes so we pick random start levels
        if self.options.basegame == self.options.basegame.option_quake:
            episode_options = [1, 2, 3, 4]
            all_episodes = all_episodes_q1
            special_levels = SL()
        elif self.options.basegame == self.options.basegame.option_hipnotic:
            episode_options = [1, 2, 3]
            all_episodes = all_episodes_hip
            special_levels = HIPSL()
        elif self.options.basegame == self.options.basegame.option_rogue:
            episode_options = [1, 2]
            all_episodes = all_episodes_rogue
            special_levels = ROGUESL()
        elif self.options.basegame == self.options.basegame.option_mg1:
            episode_options = [1, 2, 3, 4, 5]
            all_episodes = all_episodes_mg1
            special_levels = MG1SL()
        elif self.options.basegame == self.options.basegame.option_dopa:
            episode_options = [1]
            all_episodes = all_episodes_dopa
            special_levels = DOPASL()
        else:
            episode_options = [1, 2, 3, 4]

        ep_option_reference = [
            self.options.episode1,
            self.options.episode2,
            self.options.episode3,
            self.options.episode4,
            self.options.episode5,
        ]

        # check for user error in episode selection (yaml)
        if not any(ep_option_reference[i - 1] for i in episode_options):
            valid_indices = [opt - 1 for opt in episode_options]
            random_index = self.multiworld.random.choice(valid_indices)
            random_option = ep_option_reference[random_index]
            random_option.value = True
            # raise RuntimeError("No episode selected. Please fix your yaml.")

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

        if shuffle_start:
            self.starting_levels = level_candidates[:start_count]

        # and then fill the included levels to the desired count
        self.included_levels.extend(
            level_candidates[: level_count - len(self.included_levels)]
        )

        # If the hub/end level is included, add it
        if self.options.include_hub:
            self.included_levels.append(special_levels.levels[0])
        if self.options.include_end:
            self.included_levels.append(special_levels.levels[1])

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

    DIFF_TO_FACTOR_MAPPING = {
        Difficulty.option_easy: 1,
        Difficulty.option_medium: 0.5,
        Difficulty.option_hard: 0.25,
        Difficulty.option_extreme: 0.125,
    }

    def generate_early(self) -> None:
        # Difficulty settings
        # Adds a mult factor for healing/armor items based on difficulty
        factor = self.DIFF_TO_FACTOR_MAPPING.get(self.options.difficulty)
        self.define_dynamic_item_props("Small Medkit", {"factor": factor})
        self.define_dynamic_item_props("Large Medkit", {"factor": factor})
        self.define_dynamic_item_props("Megahealth", {"factor": factor})

        self.define_dynamic_item_props("Green Armor", {"factor": factor})
        self.define_dynamic_item_props("Yellow Armor", {"factor": factor})
        self.define_dynamic_item_props("Red Armor", {"factor": factor})

        # Configure rules
        self.rules = Rules(self)

        # Generate level pool
        self.calculate_levels()

        for level in self.included_levels:
            if self.options.area_maps == self.options.area_maps.option_start_with:
                self.options.start_inventory.value[level.map] = 1
        basegame_lut = ["id1", "hipnotic", "rogue", "mg1", "dopa"]
        self.slot_data["settings"]["basegame"] = basegame_lut[
            self.options.basegame.value
        ]
        self.slot_data["settings"]["difficulty"] = self.options.skill_level.value
        self.slot_data["settings"]["lock"] = {}
        self.slot_data["settings"]["shell_recharge"] = self.options.shell_recharge.value
        self.slot_data["settings"][
            "traps_as_progressive"
        ] = self.options.traps_as_progressive.value
        self.slot_data["settings"][
            "powerup_recharge"
        ] = self.options.powerup_recharge.value
        if self.options.unlock_abilities:
            self.slot_data["settings"]["lock"].update(
                {
                    "crouch": True,
                    "jump": True,
                    "run": True,
                    "dive": True,
                    "grenadejump": True,
                    "rocketjump": True,
                }
            )
        if self.options.damage_remover_abilities:
            self.slot_data["settings"]["lock"].update(
                {
                    "rocketdmgsaver": True,
                    "grenadedmgsaver": True,
                }
            )
        if self.options.unlock_interact:
            self.slot_data["settings"]["lock"].update(
                {
                    "door": True,
                    "button": True,
                    "shootswitch": True,
                }
            )
        # TODO: Implement no_save
        # self.slot_data["settings"]["no_save"] = not self.options.allow_saving.value
        # fix not enough locations in dopa:
        if (
            self.options.basegame.value == self.options.basegame.option_dopa
            and self.options.included_locations_preset.value
            == self.options.included_locations_preset.option_iconic
        ):
            self.options.included_locations_preset.value = (
                self.options.included_locations_preset.option_balanced
            )

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
                if goal_exits and location.classname == "trigger_changelevel":
                    goal_counts["Exit"] += 1
                elif goal_secrets and location.classname == "trigger_secret":
                    goal_counts["Secret"] += 1
                elif (
                    goal_bosses
                    and location.classname == "trigger_changelevel"
                    and level.has_boss
                ):
                    goal_counts["Boss"] += 1
        goal_percentage = self.options.goal_percentage
        if goal_percentage < 100:
            for goal_type in ("Exit", "Secret", "Boss"):
                goal_counts[goal_type] = math.ceil(
                    0.01 * goal_percentage * goal_counts[goal_type]
                )
        self.slot_data["goal"] = {
            "Exit": {
                "id": self.item_name_to_id["Exit"],
                "count": goal_counts["Exit"],
            },
            "Secret": {
                "id": self.item_name_to_id["Secret"],
                "count": goal_counts["Secret"],
            },
            "Boss": {
                "id": self.item_name_to_id["Boss"],
                "count": goal_counts["Boss"],
            },
        }
        self.multiworld.completion_condition[self.player] = (
            self.rules.count("Exit", goal_counts["Exit"])
            & self.rules.count("Secret", goal_counts["Secret"])
            & self.rules.count("Boss", goal_counts["Boss"])
        )

        # Reroll if our random level unlock does not unlock enough sphere 1 locations
        num_early_locs = 0
        depth = 0
        levels_tried = []

        while depth < len(self.included_levels):
            state = CollectionState(self.multiworld, True)
            # print("Attempt ", depth + 1)
            for level in self.starting_levels:
                # print("Starting Level: ", level.prefix, level.name)
                state.collect(self.create_item(level.unlock))
            for level in self.starting_levels:
                levels_tried.append(level)
            # TODO: Re-enable this when AP 0.6.0 goes live
            # sweep_locations = self.get_locations()
            sweep_locations = self.multiworld.get_locations()
            state.sweep_for_advancements(locations=sweep_locations)

            num_early_locs = sum(
                1
                for loc in self.multiworld.get_reachable_locations(state, self.player)
                if loc.address and not loc.item
            )

            # print("Number of early locations: ", num_early_locs)
            depth += 1

            # Break out of the loop if we found a valid sphere 1
            if num_early_locs > 0:
                break

            # Remove candidates if they didnt work
            level_candidate = self.multiworld.random.choice(self.included_levels)
            while level_candidate in levels_tried:
                level_candidate = self.multiworld.random.choice(self.included_levels)
            self.starting_levels.pop()
            self.starting_levels.append(level_candidate)

        for level in self.starting_levels:
            # print("Final Starting Level: ", level.prefix, level.name)
            self.options.start_inventory.value[level.unlock] = 1
            self.multiworld.push_precollected(self.create_item(level.unlock))

    AMMO_NAMES = (
        "Shells",
        "Spikes",
        "Rockets",
        "Cells",
    )

    # TODO: Improve
    # Hacky way to fix UT progression items
    ut_overwrite_prog_list = []
    other_items = ["Small Medkit", "Large Medkit", "Megahealth"]
    for item_set in item_name_groups.values():
        ut_overwrite_prog_list.extend(item_set)

    ut_overwrite_prog_list.extend(other_items)

    def create_item(self, item: str, progression: bool = False) -> Q1Item:
        item_def = all_items.get(item)
        # Hacky way to fix UT
        if (
            hasattr(self.multiworld, "re_gen_passthrough")
            and item in self.ut_overwrite_prog_list
        ):
            classification = ItemClassification.progression
        elif progression:
            classification = ItemClassification.progression
        elif item_def.progression:
            classification = ItemClassification.progression
        elif item_def.persistent:
            classification = ItemClassification.useful
        elif item_def.type == "trap":
            classification = ItemClassification.trap
        else:
            classification = ItemClassification.filler
        ret = Q1Item(item, classification, self.item_name_to_id[item], self.player)
        return ret

    def create_event(self, event_name: str) -> Q1Item:
        return Q1Item(event_name, ItemClassification.progression, None, self.player)

    def get_filler_item_name(self) -> str:
        # This should never be required with the item pool calculations, so we don't need any junk ratio logic here
        return "Nothing"

    def create_junk(self, count: int) -> List[Q1Item]:
        difficulty = self.options.difficulty
        # TODO: Create difficulty based distribution of items
        if difficulty == self.options.difficulty.option_extreme:
            ratios = {
                "Nothing": 40,
                "Heal (+1)": 40,
                "Armor (+1)": 40,
                "Shotgun Ammo (+1)": 40,
                "Nail Ammo (+1)": 40,
                "Rocket Ammo (+1)": 40,
                "Cell Ammo (+1)": 40,
                # "Green Armor": 2,
                # "Small Medkit": 30,
                # "Large Medkit": 10,
                # "Megahealth": 1,
                "Quad Damage": 1,
                "Invulnerability": 1,
                "Biosuit": 1,
                "Invisibility": 1,
                "Backpack": 1,
            }
            trap_ratios = {
                "Low Health Trap": 6,
                "Death Trap": 6,
                "Mouse Trap": 3,
                "Sound Trap": 1,
                "Jump Trap": 2,
            }
        elif difficulty == self.options.difficulty.option_hard:
            ratios = {
                "Nothing": 30,
                "Heal (+1)": 30,
                "Armor (+1)": 30,
                "Shotgun Ammo (+1)": 30,
                "Nail Ammo (+1)": 30,
                "Rocket Ammo (+1)": 30,
                "Cell Ammo (+1)": 30,
                # "Green Armor": 3,
                # "Yellow Armor": 2,
                # "Small Medkit": 3,
                # "Large Medkit": 2,
                # "Megahealth": 1,
                "Quad Damage": 2,
                "Invulnerability": 2,
                "Biosuit": 2,
                "Invisibility": 2,
                "Backpack": 2,
            }
            trap_ratios = {
                "Low Health Trap": 4,
                "Death Trap": 4,
                "Mouse Trap": 3,
                "Sound Trap": 1,
                "Jump Trap": 2,
            }
        elif difficulty == self.options.difficulty.option_medium:
            ratios = {
                "Nothing": 20,
                "Heal (+1)": 20,
                "Armor (+1)": 20,
                "Shotgun Ammo (+1)": 20,
                "Nail Ammo (+1)": 20,
                "Rocket Ammo (+1)": 20,
                "Cell Ammo (+1)": 20,
                # "Green Armor": 4,
                # "Yellow Armor": 3,
                # "Red Armor": 1,
                # "Small Medkit": 3,
                # "Large Medkit": 2,
                # "Megahealth": 3,
                "Quad Damage": 3,
                "Invulnerability": 3,
                "Biosuit": 3,
                "Invisibility": 3,
                "Backpack": 3,
            }
            trap_ratios = {
                "Low Health Trap": 1,
                "Death Trap": 1,
                "Mouse Trap": 3,
                "Sound Trap": 3,
                "Jump Trap": 3,
            }
        else:
            ratios = {
                "Nothing": 10,
                "Heal (+1)": 10,
                "Armor (+1)": 10,
                "Shotgun Ammo (+1)": 10,
                "Nail Ammo (+1)": 10,
                "Rocket Ammo (+1)": 10,
                "Cell Ammo (+1)": 10,
                # "Green Armor": 5,
                # "Yellow Armor": 4,
                # "Red Armor": 2,
                # "Small Medkit": 3,
                # "Large Medkit": 2,
                # "Megahealth": 10,
                "Quad Damage": 5,
                "Invulnerability": 5,
                "Biosuit": 5,
                "Invisibility": 5,
                "Backpack": 5,
            }
            trap_ratios = {
                "Low Health Trap": 1,
                "Death Trap": 1,
                "Mouse Trap": 4,
                "Sound Trap": 8,
                "Jump Trap": 8,
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

    def create_item_list(self, item_list: List[str]) -> List[Q1Item]:
        return [self.create_item(item) for item in item_list]

    HEALTH_DIFF_TO_REQ_MAPPING = {
        Difficulty.option_easy: {
            "Small Medkit": (2, 20),
            "Large Medkit": (2, 20),
            "Megahealth": (2, 20),
        },
        Difficulty.option_medium: {
            "Small Medkit": (4, 15),
            "Large Medkit": (4, 15),
            "Megahealth": (4, 15),
        },
        Difficulty.option_hard: {
            "Small Medkit": (8, 10),
            "Large Medkit": (8, 10),
            "Megahealth": (8, 10),
        },
        Difficulty.option_extreme: {
            "Small Medkit": (10, 10),
            "Large Medkit": (10, 10),
            "Megahealth": (10, 10),
        },
    }

    def generate_health(self, inv_type: str) -> Tuple[List[Q1Item], List[Q1Item]]:
        required, total = self.HEALTH_DIFF_TO_REQ_MAPPING.get(
            self.options.difficulty, self.options.difficulty.option_medium
        )[inv_type]
        required_list = [self.create_item(inv_type, True) for _ in range(required)]
        # Fill pool with capacity up to total amount
        useful_list = [
            self.create_item(inv_type) for _ in range(total - len(required_list))
        ]
        return required_list, useful_list

    ARMOR_DIFF_TO_REQ_MAPPING = {
        Difficulty.option_easy: {
            "Green Armor": (10, 10),
            "Yellow Armor": (10, 10),
            "Red Armor": (4, 4),
        },
        Difficulty.option_medium: {
            "Green Armor": (20, 20),
            "Yellow Armor": (20, 20),
            "Red Armor": (4, 4),
        },
        Difficulty.option_hard: {
            "Green Armor": (20, 20),
            "Yellow Armor": (20, 20),
            "Red Armor": (8, 8),
        },
        Difficulty.option_extreme: {
            "Green Armor": (40, 40),
            "Yellow Armor": (20, 20),
            "Red Armor": (5, 5),
        },
    }

    def generate_armor(self, inv_type: str) -> Tuple[List[Q1Item], List[Q1Item]]:
        required, total = self.ARMOR_DIFF_TO_REQ_MAPPING.get(
            self.options.difficulty, self.options.difficulty.option_medium
        )[inv_type]
        # armor is never progressive but also not optional
        required_list = [self.create_item(inv_type, False) for _ in range(required)]
        # Fill pool with capacity up to total amount
        useful_list = [
            self.create_item(inv_type) for _ in range(total - len(required_list))
        ]
        return required_list, useful_list

    INV_DIFF_TO_REQ_MAPPING = {
        Difficulty.option_easy: {
            "Quad Damage": (1, 5),
            "Invulnerability": (1, 5),
            "Biosuit": (1, 5),
            "Invisibility": (1, 5),
            "Backpack": (5, 10),
        },
        Difficulty.option_medium: {
            "Quad Damage": (1, 3),
            "Invulnerability": (1, 3),
            "Biosuit": (1, 3),
            "Invisibility": (1, 3),
            "Backpack": (5, 8),
        },
        Difficulty.option_hard: {
            "Quad Damage": (1, 2),
            "Invulnerability": (1, 2),
            "Biosuit": (1, 2),
            "Invisibility": (1, 2),
            "Backpack": (5, 6),
        },
        Difficulty.option_extreme: {
            "Quad Damage": (1, 1),
            "Invulnerability": (1, 1),
            "Biosuit": (1, 1),
            "Invisibility": (1, 1),
            "Backpack": (5, 5),
        },
    }

    def generate_inventories(
        self, inv_type: str, prog_override_amount: int = 0
    ) -> Tuple[List[Q1Item], List[Q1Item]]:
        required, total = self.INV_DIFF_TO_REQ_MAPPING.get(
            self.options.difficulty, self.options.difficulty.option_medium
        )[inv_type]

        # One base item and rest is capacity, unless we have progressive inventories
        progressive = self.options.progressive_inventories
        if progressive:
            main_name = f"Progressive {inv_type}"
            cap_name = main_name
        else:
            main_name = inv_type
            cap_name = f"{inv_type} Capacity"
        required_list = [self.create_item(main_name, True)] + [
            self.create_item(cap_name, True)
            for _ in range(required - 1 + prog_override_amount)
        ]
        # Fill pool with capacity up to total amount
        useful_list = [
            self.create_item(cap_name) for _ in range(total - len(required_list))
        ]
        return required_list, useful_list

    # TODO: Update these
    DIFF_TO_MAX_MAPPING = {
        Difficulty.option_easy: {
            "Shotgun": (25, 50),
            "Super Shotgun": (25, 50),
            "Nailgun": (30, 100),
            "Super Nailgun": (30, 100),
            "Grenade Launcher": (5, 50),
            "Rocket Launcher": (5, 50),
            "Proximity Gun": (5, 50),
            "Thunderbolt": (15, 200),
            "Mjolnir": (15, 200),
            "Laser Cannon": (15, 200),
            "Lava Nailgun Upgrade": (30, 100),
            "Lava Super Nailgun Upgrade": (30, 100),
            "Multi-Grenade Upgrade": (5, 50),
            "Multi-Rocket Upgrade": (5, 50),
            "Plasma Gun Upgrade": (15, 100),
        },
        Difficulty.option_medium: {
            "Shotgun": (25, 50),
            "Super Shotgun": (25, 50),
            "Nailgun": (30, 100),
            "Super Nailgun": (30, 100),
            "Grenade Launcher": (5, 50),
            "Rocket Launcher": (5, 50),
            "Proximity Gun": (5, 50),
            "Thunderbolt": (15, 200),
            "Mjolnir": (15, 200),
            "Laser Cannon": (15, 200),
            "Lava Nailgun Upgrade": (30, 100),
            "Lava Super Nailgun Upgrade": (30, 100),
            "Multi-Grenade Upgrade": (5, 50),
            "Multi-Rocket Upgrade": (5, 50),
            "Plasma Gun Upgrade": (15, 100),
        },
        Difficulty.option_hard: {
            "Shotgun": (25, 50),
            "Super Shotgun": (25, 50),
            "Nailgun": (30, 100),
            "Super Nailgun": (30, 100),
            "Grenade Launcher": (5, 50),
            "Rocket Launcher": (5, 50),
            "Proximity Gun": (5, 50),
            "Thunderbolt": (15, 200),
            "Mjolnir": (15, 200),
            "Laser Cannon": (15, 200),
            "Lava Nailgun Upgrade": (30, 100),
            "Lava Super Nailgun Upgrade": (30, 100),
            "Multi-Grenade Upgrade": (5, 50),
            "Multi-Rocket Upgrade": (5, 50),
            "Plasma Gun Upgrade": (15, 100),
        },
        Difficulty.option_extreme: {
            "Shotgun": (25, 50),
            "Super Shotgun": (25, 50),
            "Nailgun": (30, 100),
            "Super Nailgun": (30, 100),
            "Grenade Launcher": (5, 50),
            "Rocket Launcher": (5, 50),
            "Proximity Gun": (5, 50),
            "Thunderbolt": (15, 200),
            "Mjolnir": (15, 200),
            "Laser Cannon": (15, 200),
            "Lava Nailgun Upgrade": (30, 100),
            "Lava Super Nailgun Upgrade": (30, 100),
            "Multi-Grenade Upgrade": (5, 50),
            "Multi-Rocket Upgrade": (5, 50),
            "Plasma Gun Upgrade": (15, 100),
        },
    }

    # Map Weapon Name to Ammo Type
    WPN_TO_AMMO_MAPPING = {
        "Shotgun": "Shells",
        "Super Shotgun": "Shells",
        "Nailgun": "Spikes",
        "Super Nailgun": "Spikes",
        "Grenade Launcher": "Rockets",
        "Rocket Launcher": "Rockets",
        "Proximity Gun": "Rockets",
        "Thunderbolt": "Cells",
        "Mjolnir": "Cells",
        "Laser Cannon": "Cells",
        "Lava Nailgun Upgrade": "Lava Nails",
        "Lava Super Nailgun Upgrade": "Lava Nails",
        "Multi-Grenade Upgrade": "Multi Rockets",
        "Multi-Rocket Upgrade": "Multi Rockets",
        "Plasma Gun Upgrade": "Plasma",
    }

    hip_weapons = ["Proximity Gun", "Mjolnir", "Laser Cannon"]
    rogue_weapons = [
        "Lava Nailgun Upgrade",
        "Lava Super Nailgun Upgrade",
        "Multi-Grenade Upgrade",
        "Multi-Rocket Upgrade",
        "Plasma Gun Upgrade",
    ]
    WEAPON_NAMES = [
        "Shotgun",
        "Super Shotgun",
        "Nailgun",
        "Super Nailgun",
        "Grenade Launcher",
        "Rocket Launcher",
        "Thunderbolt",
    ]

    ALL_KILLS_WEAPONS = [
        "Super Shotgun",
        "Nailgun",
        "Super Nailgun",
        "Thunderbolt",
        "Laser Cannon",
    ]

    def useful_items_per_difficulty(self, available_slots: int) -> List[Q1Item]:
        if available_slots <= 0:
            # Out of space already, can abort
            return []

        ret_items = {}
        # We want about 35% of remaining slots to be filled with ammo expansions, so calculated the amount we get
        # for each of the 10 weapons
        expansions_per_weapon = math.ceil(available_slots * 0.035)

        if self.options.basegame == self.options.basegame.option_hipnotic:
            self.WEAPON_NAMES.extend(self.hip_weapons)
        if self.options.basegame == self.options.basegame.option_rogue:
            self.WEAPON_NAMES.extend(self.rogue_weapons)

        for weapon in self.WEAPON_NAMES:
            start, target = self.DIFF_TO_MAX_MAPPING.get(
                self.options.difficulty, self.options.difficulty.option_medium
            )[weapon]
            ammo = self.WPN_TO_AMMO_MAPPING[weapon]
            self.slot_data["settings"]["maximum"][ammo.lower()] = start
            difference = target - start
            if difference <= 0:
                continue
            capacity_per = math.ceil(float(difference) / expansions_per_weapon)
            count = math.ceil(float(difference) / capacity_per)
            # configure the capacity for each upgrade dynamically
            self.define_dynamic_item_props(
                f"{ammo} Capacity",
                {"capacity": capacity_per, "ammo": math.ceil(capacity_per / 2.0)},
            )
            # and add the right count to our pool
            if self.options.progressive_weapons:
                ret_items[f"Progressive {weapon}"] = count
            else:
                ret_items[f"{ammo} Capacity"] = count

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
        # Place goal items and level keys
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
                    and location.classname == "trigger_changelevel"
                ):
                    self.multiworld.get_location(
                        location.name, self.player
                    ).place_locked_item(self.create_item("Exit"))
                    used_locations.remove(location.name)
                elif (
                    goal_secrets
                    and location.name in self.used_locations
                    and location.classname == "trigger_secret"
                ):
                    self.multiworld.get_location(
                        location.name, self.player
                    ).place_locked_item(self.create_item("Secret"))
                    used_locations.remove(location.name)
                elif (
                    goal_bosses
                    and location.name in self.used_locations
                    and location.classname == "trigger_changelevel"
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
            # Starting level unlocks were included earlier
            if level not in self.starting_levels:
                itempool.append(self.create_item(level.unlock))
            if self.options.area_maps == self.options.area_maps.option_unlockable:
                useful_items.append(self.create_item(level.map))

        unlock_abilities_array = [
            "Jump",
            "Dive",
            "Grenade Jump",
            "Rocket Jump",
            "Run",
        ]
        if self.options.unlock_abilities:
            itempool += self.create_item_list(unlock_abilities_array)
        else:
            for unlock in unlock_abilities_array:
                self.multiworld.push_precollected(self.create_item(unlock))

        unlock_interact_array = ["Door", "Button", "Shoot Switch"]
        if self.options.unlock_interact:
            itempool += self.create_item_list(unlock_interact_array)
        else:
            for unlock in unlock_interact_array:
                self.multiworld.push_precollected(self.create_item(unlock))

        if self.options.damage_remover_abilities:
            itempool += self.create_item_list(
                ["Grenade Damage Remover", "Rocket Damage Remover"]
            )

        # Add progression items
        progressive_weapons = self.options.progressive_weapons
        # Place explosive weapons into the required itempool
        if progressive_weapons:
            itempool += self.create_item_list(
                [
                    "Progressive Grenade Launcher",
                    "Progressive Rocket Launcher",
                ]
            )
            if self.options.basegame == self.options.basegame.option_hipnotic:
                itempool.append(self.create_item("Progressive Proximity Gun"))
            # difficult combat
            itempool.append(self.create_item("Progressive Thunderbolt", 1))
            itempool.append(self.create_item("Progressive Super Shotgun", 1))
            itempool.append(self.create_item("Progressive Super Nailgun", 1))
            itempool.append(self.create_item("Progressive Nailgun", 1))
            if self.options.basegame == self.options.basegame.option_hipnotic:
                itempool.append(self.create_item("Progressive Laser Cannon", 1))
        else:
            itempool += self.create_item_list(["Grenade Launcher", "Rocket Launcher"])
            if self.options.basegame == self.options.basegame.option_hipnotic:
                itempool.append(self.create_item("Proximity Gun"))
            # difficult combat
            itempool.append(self.create_item("Thunderbolt", 1))
            itempool.append(self.create_item("Super Shotgun", 1))
            itempool.append(self.create_item("Super Nailgun", 1))
            itempool.append(self.create_item("Nailgun", 1))
            if self.options.basegame == self.options.basegame.option_hipnotic:
                itempool.append(self.create_item("Laser Cannon", 1))

        # Get progression inventory based on difficulty settings
        required, useful = self.generate_health("Small Medkit")
        itempool += required
        useful_items += useful
        required, useful = self.generate_health("Large Medkit")
        itempool += required
        useful_items += useful
        required, useful = self.generate_health("Megahealth")
        itempool += required
        useful_items += useful

        required, useful = self.generate_armor("Green Armor")
        itempool += required
        useful_items += useful
        required, useful = self.generate_armor("Yellow Armor")
        itempool += required
        useful_items += useful
        required, useful = self.generate_armor("Red Armor")
        itempool += required
        useful_items += useful

        # Invulnerability or Biosuit is required for some locations
        need_invuln = False
        need_bio = False
        for level in self.included_levels:
            if level.must_invuln:
                need_invuln = True
            if level.must_bio:
                need_bio = True
        if need_invuln:
            itempool.append(self.create_item("Invulnerability", True))
        if need_bio:
            itempool.append(self.create_item("Biosuit", True))
        inventory_items = [
            "Quad Damage",
            "Invulnerability",
            "Biosuit",
            "Invisibility",
            "Backpack",
        ]
        for itemname in inventory_items:
            required, useful = self.generate_inventories(itemname)
            itempool += required
            useful_items += useful

        # Can fail now if we don't even have enough slots for our required items
        if len(itempool) > len(used_locations):
            raise RuntimeError(
                "\nNot enough locations for all mandatory items with these settings!\n"
                "Increase included_locations_preset or episode count."
            )

        # Add one copy of each remaining weapon to the pool
        if progressive_weapons:
            useful_items += self.create_item_list(
                [
                    "Progressive Super Shotgun",
                    "Progressive Nailgun",
                    "Progressive Super Nailgun",
                    "Progressive Thunderbolt",
                ]
            )
        else:
            useful_items += self.create_item_list(
                ["Super Shotgun", "Nailgun", "Super Nailgun", "Thunderbolt"]
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
        self.slot_data.update({"ut_s": str(self.seed)})
        self.slot_data.update({"death_link": self.options.death_link.value})
        return self.slot_data
