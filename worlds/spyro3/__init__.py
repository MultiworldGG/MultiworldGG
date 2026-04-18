# world/spyro3/__init__.py
from typing import Dict, Set, List, TextIO, Union, ClassVar
import math

from BaseClasses import MultiWorld, Region, Item, Entrance, Tutorial, ItemClassification

from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import set_rule, add_rule, add_item_rule, forbid_item
from Options import Accessibility, Range, Toggle, OptionError
from settings import Group, Bool

from .Items import Spyro3Item, Spyro3ItemCategory, item_dictionary, key_item_names, item_descriptions, BuildItemPool, \
    item_name_groups
from .Locations import Spyro3Location, Spyro3LocationCategory, location_tables, location_dictionary, hint_locations, \
    location_name_groups
from .Options import Spyro3Option, GoalOptions, LifeBottleOptions, MoneybagsOptions, SparxUpgradeOptions, \
    SparxForGemsOptions, GemsanityOptions, LevelLockOptions, spyro_options_groups, PowerupLockOptions
from .Hints import generateHints

class Spyro3Settings(Group):

    class AllowFullGemsanity(Bool):
        """Permits full gemsanity options for multiplayer games.
        Full gemsanity adds almost 4000 locations.  At a later date, it may add an equivalent number of progression
        items. These future items might be local-only or spread across the multiworld."""

    allow_full_gemsanity: Union[AllowFullGemsanity, bool] = False

class Spyro3Web(WebWorld):
    bug_report_page = ""
    theme = "stone"
    option_groups = spyro_options_groups
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Archipelago Spyro 3 randomizer on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["ArsonAssassin", "Uroogla"]
    )
    game_info_languages = ["en"]
    tutorials = [setup_en]
    options_presets = {
        "New Player": {
            "goal": "sorceress_1",
            "egg_count": 100,
            "open_world": False,
            "level_lock_option": "vanilla",
            "moneybags_settings": "vanilla",
            "enable_25_pct_gem_checks": True,
            "enable_gemsanity": "off",
            "enable_filler_extra_lives": True,
            "enable_filler_invincibility": True,
            "enable_filler_color_change": True,
            "enable_filler_big_head_mode": True,
            "enable_filler_heal_sparx": True,
            "zoe_gives_hints": 13,
            "easy_boxing": True,
        },
    }


class Spyro3World(World):
    """
    Spyro 3 is a game about a purple dragon who likes eggs.
    """

    game: str = "Spyro 3"
    options_dataclass = Spyro3Option
    options: Spyro3Option
    topology_present: bool = False  # Turn on when entrance randomizer is available.
    web = Spyro3Web()
    data_version = 0
    base_id = 1230000
    required_client_version = (0, 5, 0)
    # TODO: Remember to update this!
    ap_world_version = "1.3.5"
    item_name_to_id = Spyro3Item.get_name_to_id()
    location_name_to_id = Spyro3Location.get_name_to_id()
    item_name_groups = item_name_groups
    location_name_groups = location_name_groups
    item_descriptions = item_descriptions
    glitches_item_name: str = "Glitched Item"  # UT Glitched Logic Support
    generation_options = dict()  # UT random option support
    settings: ClassVar[Spyro3Settings]

    level_gems = {
        "Sunrise Spring": 400,
        "Sunny Villa": 400,
        "Cloud Spires": 400,
        "Molten Crater": 400,
        "Seashell Shore": 400,
        "Mushroom Speedway": 400,
        "Sheila's Alp": 400,
        "Buzz": 0,
        "Crawdad Farm": 200,
        "Midday Gardens": 400,
        "Icy Peak": 500,
        "Enchanted Towers": 500,
        "Spooky Swamp": 500,
        "Bamboo Terrace": 500,
        "Country Speedway": 400,
        "Sgt. Byrd's Base": 500,
        "Spike": 0,
        "Spider Town": 200,
        "Evening Lake": 400,
        "Frozen Altars": 600,
        "Lost Fleet": 600,
        "Fireworks Factory": 600,
        "Charmed Ridge": 600,
        "Honey Speedway": 400,
        "Bentley's Outpost": 600,
        "Scorch": 0,
        "Starfish Reef": 200,
        "Midnight Mountain": 400,
        "Crystal Islands": 700,
        "Desert Ruins": 700,
        "Haunted Tomb": 700,
        "Dino Mines": 700,
        "Harbor Speedway": 400,
        "Agent 9's Lab": 700,
        "Sorceress": 0,
        "Bugbot Factory": 200,
        "Super Bonus Round": 5000
    }

    # TODO: Remember to keep this False.
    PRINT_GEM_REQS = False  # Prints out the logic for each gem on generating a seed. Not for production use.


    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.locked_items = []
        self.locked_locations = []
        self.main_path_locations = []
        self.enabled_location_categories = set()
        self.all_levels = [
            "Sunrise Spring","Sunny Villa","Cloud Spires","Molten Crater","Seashell Shore","Mushroom Speedway","Sheila's Alp", "Buzz", "Crawdad Farm",
            "Midday Gardens","Icy Peak","Enchanted Towers","Spooky Swamp","Bamboo Terrace","Country Speedway","Sgt. Byrd's Base","Spike","Spider Town",
            "Evening Lake","Frozen Altars","Lost Fleet","Fireworks Factory","Charmed Ridge","Honey Speedway","Bentley's Outpost","Scorch","Starfish Reef",
            "Midnight Mountain","Crystal Islands","Desert Ruins","Haunted Tomb","Dino Mines","Harbor Speedway","Agent 9's Lab","Sorceress","Bugbot Factory","Super Bonus Round"
        ]
        self.requirement_multiplier = 1.0
        self.enabled_hint_locations = []
        self.enabled_location_categories = set()
        self.chosen_gem_locations = []
        self.key_locked_levels = []
        self.level_egg_requirements = {
            "Sunny Villa": 0,
            "Cloud Spires": 0,
            "Molten Crater": 0,
            "Seashell Shore": 0,
            "Mushroom Speedway": 0,
            "Icy Peak": 0,
            "Enchanted Towers": 0,
            "Spooky Swamp": 0,
            "Bamboo Terrace": 0,
            "Country Speedway": 0,
            "Frozen Altars": 0,
            "Lost Fleet": 0,
            "Fireworks Factory": 0,
            "Charmed Ridge": 0,
            "Honey Speedway": 0,
            "Crystal Islands": 0,
            "Desert Ruins": 0,
            "Haunted Tomb": 0,
            "Dino Mines": 0,
            "Harbor Speedway": 0,
        }
        self.level_gem_requirements = {
            "Sunny Villa": 0,
            "Cloud Spires": 0,
            "Molten Crater": 0,
            "Seashell Shore": 0,
            "Mushroom Speedway": 0,
            "Icy Peak": 0,
            "Enchanted Towers": 0,
            "Spooky Swamp": 0,
            "Bamboo Terrace": 0,
            "Country Speedway": 0,
            "Frozen Altars": 0,
            "Lost Fleet": 0,
            "Fireworks Factory": 0,
            "Charmed Ridge": 0,
            "Honey Speedway": 0,
            "Crystal Islands": 0,
            "Desert Ruins": 0,
            "Haunted Tomb": 0,
            "Dino Mines": 0,
            "Harbor Speedway": 0,
        }
        self.generation_options = dict()

    def generate_entry_requirements(self):
        if self.generation_options["level_lock_option"] in [LevelLockOptions.KEYS]:
            possible_sunrise_unlocked_levels = ["Sunny Villa", "Cloud Spires", "Molten Crater", "Seashell Shore"]
            self.key_locked_levels = [
                "Sunny Villa", "Cloud Spires", "Molten Crater", "Seashell Shore", "Mushroom Speedway",
                "Icy Peak", "Enchanted Towers", "Spooky Swamp", "Bamboo Terrace", "Country Speedway",
                "Frozen Altars", "Lost Fleet", "Fireworks Factory", "Charmed Ridge", "Honey Speedway",
                "Crystal Islands", "Desert Ruins", "Haunted Tomb", "Dino Mines", "Harbor Speedway"
            ]
            starting_level = self.multiworld.random.choice(possible_sunrise_unlocked_levels)
            self.key_locked_levels.remove(starting_level)
            if self.generation_options["starting_levels_count"] != 1:
                other_unlocked_levels = self.multiworld.random.sample(self.key_locked_levels, k=self.generation_options["starting_levels_count"] - 1)
                for level in other_unlocked_levels:
                    self.key_locked_levels.remove(level)
        elif self.generation_options["level_lock_option"] in [LevelLockOptions.VANILLA]:
            self.level_egg_requirements = {
                "Sunny Villa": 0,
                "Cloud Spires": 0,
                "Molten Crater": 10,
                "Seashell Shore": 14,
                "Mushroom Speedway": 20,
                "Icy Peak": 0,
                "Enchanted Towers": 0,
                "Spooky Swamp": 25,
                "Bamboo Terrace": 30,
                "Country Speedway": 36,
                "Frozen Altars": 0,
                "Lost Fleet": 0,
                "Fireworks Factory": 50,
                "Charmed Ridge": 58,
                "Honey Speedway": 65,
                "Crystal Islands": 0,
                "Desert Ruins": 0,
                "Haunted Tomb": 70,
                "Dino Mines": 80,
                "Harbor Speedway": 90,
            }
        elif self.generation_options["level_lock_option"] == LevelLockOptions.KEYS:
            # No egg or gem requirements
            pass
        elif self.generation_options["level_lock_option"] == LevelLockOptions.RANDOM_REQS:
            vanilla_reqs = [10, 14, 20, 25, 30, 36, 50, 58, 65, 70, 80, 90]
            random_reqs = []
            for req in vanilla_reqs:
                # 85% to 110% of vanilla requirements.
                random_reqs.append(math.floor(req * (1 + 0.25 * (-0.6 + self.multiworld.random.random()))))
            if self.generation_options["open_world"]:
                random_levels = [
                    "Molten Crater", "Seashell Shore", "Mushroom Speedway",
                    "Spooky Swamp", "Bamboo Terrace", "Country Speedway",
                    "Fireworks Factory", "Charmed Ridge", "Honey Speedway",
                    "Haunted Tomb", "Dino Mines", "Harbor Speedway"
                ]
                self.multiworld.random.shuffle(random_levels)
                for i in range(12):
                    self.level_egg_requirements[random_levels[i]] = random_reqs[i]
            else:
                random_levels = [
                    ["Molten Crater", "Seashell Shore"],
                    ["Spooky Swamp", "Bamboo Terrace"],
                    ["Fireworks Factory", "Charmed Ridge"],
                    ["Haunted Tomb", "Dino Mines", "Harbor Speedway"]
                ]
                mushroom_index = self.multiworld.random.randint(0, 1)
                random_levels[mushroom_index].append("Mushroom Speedway")
                country_index = self.multiworld.random.randint(1, 2)
                random_levels[country_index].append("Country Speedway")
                honey_index = self.multiworld.random.randint(2, 3)
                random_levels[honey_index].append("Honey Speedway")
                i = 0
                for level_set in random_levels:
                    self.multiworld.random.shuffle(level_set)
                    for level in level_set:
                        self.level_egg_requirements[level] = random_reqs[i]
                        i = i + 1
        elif self.generation_options["level_lock_option"] == LevelLockOptions.ADD_REQS or \
                self.generation_options["level_lock_option"] == LevelLockOptions.ADD_GEM_REQS and \
                (self.generation_options["moneybags_settings"] != MoneybagsOptions.MONEYBAGSSANITY or \
                self.generation_options["enable_gemsanity"] == GemsanityOptions.OFF):
            # Vanilla requirements, plus numbers for levels without vanilla requirements.
            vanilla_reqs = [3, 6, 10, 14, 17, 20, 22, 25, 30, 35, 36, 44, 50, 58, 64, 65, 67, 70, 80, 90]
            random_reqs = []
            open_sunrise_level = self.multiworld.random.randint(0, 3)
            all_levels = list(range(20))
            all_levels.remove(open_sunrise_level)
            unlocked_levels = []
            if self.generation_options["starting_levels_count"] != 1:
                unlocked_levels = self.multiworld.random.sample(all_levels, k=self.generation_options["starting_levels_count"] - 1)
            unlocked_levels.append(open_sunrise_level)
            for req in vanilla_reqs:
                # 80% to 110% of vanilla requirements.
                random_reqs.append(math.floor(req * (1 + 0.25 * (-0.6 + self.multiworld.random.random()))))
            if self.generation_options["open_world"]:
                levels = [
                    "Sunny Villa", "Cloud Spires", "Molten Crater", "Seashell Shore", "Mushroom Speedway",
                    "Icy Peak", "Enchanted Towers", "Spooky Swamp", "Bamboo Terrace", "Country Speedway",
                    "Frozen Altars", "Lost Fleet", "Fireworks Factory", "Charmed Ridge", "Honey Speedway",
                    "Crystal Islands", "Desert Ruins", "Haunted Tomb", "Dino Mines", "Harbor Speedway"
                ]
                self.multiworld.random.shuffle(random_reqs)
                for i in range(20):
                    if i not in unlocked_levels:
                        self.level_egg_requirements[levels[i]] = random_reqs[i]
            else:
                random_levels = [
                    ["Sunny Villa", "Cloud Spires", "Molten Crater", "Seashell Shore"],
                    ["Icy Peak", "Enchanted Towers", "Spooky Swamp", "Bamboo Terrace"],
                    ["Frozen Altars", "Lost Fleet", "Fireworks Factory", "Charmed Ridge"],
                    ["Crystal Islands", "Desert Ruins", "Haunted Tomb", "Dino Mines", "Harbor Speedway"]
                ]
                # Don't group Mushroom with other Sunrise levels to ensure a proper Sunrise level is unlocked.
                mushroom_index = 1
                random_levels[mushroom_index].append("Mushroom Speedway")
                country_index = self.multiworld.random.randint(1, 2)
                random_levels[country_index].append("Country Speedway")
                honey_index = self.multiworld.random.randint(2, 3)
                random_levels[honey_index].append("Honey Speedway")
                i = 0
                for level_set in random_levels:
                    self.multiworld.random.shuffle(level_set)
                    for level in level_set:
                        if i not in unlocked_levels:
                            self.level_egg_requirements[level] = random_reqs[i]
                        i = i + 1
        elif self.generation_options["level_lock_option"] == LevelLockOptions.ADD_GEM_REQS and \
                self.generation_options["moneybags_settings"] == MoneybagsOptions.MONEYBAGSSANITY and \
                self.generation_options["enable_gemsanity"] != GemsanityOptions.OFF:
            # Vanilla requirements, plus numbers for levels without vanilla requirements.
            vanilla_egg_reqs = [3, 6, 10, 14, 17, 20, 22, 25, 30, 35, 36, 44, 50, 58, 64, 65, 67, 70, 80, 90]
            gem_reqs = [200, 400, 600, 800, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2800, 3100, 3400, 3700, 4100, 4500, 4900, 5400, 6000]
            random_reqs = []
            open_sunrise_level = self.multiworld.random.randint(0, 3)
            all_levels = list(range(20))
            all_levels.remove(open_sunrise_level)
            unlocked_levels = []
            if self.generation_options["starting_levels_count"] != 1:
                unlocked_levels = self.multiworld.random.sample(all_levels, k=self.generation_options["starting_levels_count"] - 1)
            unlocked_levels.append(open_sunrise_level)
            for req in vanilla_egg_reqs:
                # 80% to 110% of vanilla requirements.
                random_reqs.append(math.floor(req * (1 + 0.25 * (-0.6 + self.multiworld.random.random()))))
            full_reqs = []
            for i in range(20):
                full_reqs.append((random_reqs[i], gem_reqs[i]))
            if self.generation_options["open_world"]:
                levels = [
                    "Sunny Villa", "Cloud Spires", "Molten Crater", "Seashell Shore", "Mushroom Speedway",
                    "Icy Peak", "Enchanted Towers", "Spooky Swamp", "Bamboo Terrace", "Country Speedway",
                    "Frozen Altars", "Lost Fleet", "Fireworks Factory", "Charmed Ridge", "Honey Speedway",
                    "Crystal Islands", "Desert Ruins", "Haunted Tomb", "Dino Mines", "Harbor Speedway"
                ]
                self.multiworld.random.shuffle(full_reqs)
                for i in range(20):
                    if i not in unlocked_levels:
                        if self.multiworld.random.random() < 0.67:
                            self.level_egg_requirements[levels[i]] = full_reqs[i][0]
                        else:
                            self.level_gem_requirements[levels[i]] = full_reqs[i][1]
            else:
                random_levels = [
                    ["Sunny Villa", "Cloud Spires", "Molten Crater", "Seashell Shore"],
                    ["Icy Peak", "Enchanted Towers", "Spooky Swamp", "Bamboo Terrace"],
                    ["Frozen Altars", "Lost Fleet", "Fireworks Factory", "Charmed Ridge"],
                    ["Crystal Islands", "Desert Ruins", "Haunted Tomb", "Dino Mines", "Harbor Speedway"]
                ]
                # Don't group Mushroom with other Sunrise levels to ensure a proper Sunrise level is unlocked.
                mushroom_index = 1
                random_levels[mushroom_index].append("Mushroom Speedway")
                country_index = self.multiworld.random.randint(1, 2)
                random_levels[country_index].append("Country Speedway")
                honey_index = self.multiworld.random.randint(2, 3)
                random_levels[honey_index].append("Honey Speedway")
                i = 0
                for level_set in random_levels:
                    self.multiworld.random.shuffle(level_set)
                    for level in level_set:
                        if i not in unlocked_levels:
                            if self.multiworld.random.random() < 0.67:
                                self.level_egg_requirements[level] = full_reqs[i][0]
                            else:
                                self.level_gem_requirements[level] = full_reqs[i][1]
                        i = i + 1

    def generate_early(self):
        # Set up generation_options to allow UT when settings are randomized.
        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if re_gen_passthrough and self.game in re_gen_passthrough:
            # Get the passed through slot data from the real generation
            slot_data = re_gen_passthrough[self.game]
            self.generation_options["level_lock_option"] = slot_data["options"]["level_lock_option"]
            self.generation_options["starting_levels_count"] = slot_data["options"]["starting_levels_count"]
            self.generation_options["open_world"] = slot_data["options"]["open_world"]
            self.generation_options["moneybags_settings"] = slot_data["options"]["moneybags_settings"]
            self.generation_options["powerup_lock_settings"] = slot_data["options"]["powerup_lock_settings"]
            self.generation_options["enable_gemsanity"] = slot_data["options"]["enable_gemsanity"]
            self.generation_options["zoe_gives_hints"] = slot_data["options"]["zoe_gives_hints"]
            self.generation_options["goal"] = slot_data["options"]["goal"]
            self.generation_options["sorceress_door_requirement"] = slot_data["options"]["sorceress_door_requirement"]
            self.generation_options["sbr_door_gem_requirement"] = slot_data["options"]["sbr_door_gem_requirement"]
            self.generation_options["sbr_door_egg_requirement"] = slot_data["options"]["sbr_door_egg_requirement"]
            self.generation_options["enable_25_pct_gem_checks"] = slot_data["options"]["enable_25_pct_gem_checks"]
            self.generation_options["enable_50_pct_gem_checks"] = slot_data["options"]["enable_50_pct_gem_checks"]
            self.generation_options["enable_75_pct_gem_checks"] = slot_data["options"]["enable_75_pct_gem_checks"]
            self.generation_options["enable_gem_checks"] = slot_data["options"]["enable_gem_checks"]
            self.generation_options["enable_total_gem_checks"] = slot_data["options"]["enable_total_gem_checks"]
            self.generation_options["enable_skillpoint_checks"] = slot_data["options"]["enable_skillpoint_checks"]
            self.generation_options["enable_life_bottle_checks"] = slot_data["options"]["enable_life_bottle_checks"]
            self.generation_options["egg_count"] = slot_data["options"]["egg_count"]
            self.generation_options["enable_world_keys"] = slot_data["options"]["enable_world_keys"]
            self.generation_options["enable_progressive_sparx_logic"] = slot_data["options"][
                "enable_progressive_sparx_logic"]
            self.generation_options["sparx_power_settings"] = slot_data["options"]["sparx_power_settings"]
            self.generation_options["enable_progressive_sparx_health"] = slot_data["options"][
                "enable_progressive_sparx_health"]
            self.generation_options["require_sparx_for_max_gems"] = slot_data["options"]["require_sparx_for_max_gems"]
            self.generation_options["percent_extra_eggs"] = slot_data["options"]["percent_extra_eggs"]
            self.generation_options["logic_cloud_backwards"] = slot_data["options"]["logic_cloud_backwards"]
            self.generation_options["logic_sheila_early"] = slot_data["options"]["logic_sheila_early"]
            self.generation_options["max_total_gem_checks"] = slot_data["options"]["max_total_gem_checks"]
            self.generation_options["logic_byrd_early"] = slot_data["options"]["logic_byrd_early"]
            self.generation_options["logic_sorceress_early"] = slot_data["options"]["logic_sorceress_early"]
            self.generation_options["logic_bentley_early"] = slot_data["options"]["logic_bentley_early"]
            self.generation_options["logic_spooky_no_moneybags"] = slot_data["options"]["logic_spooky_no_moneybags"]
            self.generation_options["logic_molten_thieves_no_moneybags"] = slot_data["options"][
                "logic_molten_thieves_no_moneybags"]
            self.generation_options["logic_charmed_no_moneybags"] = slot_data["options"]["logic_charmed_no_moneybags"]
            self.generation_options["logic_desert_no_moneybags"] = slot_data["options"]["logic_desert_no_moneybags"]
            self.generation_options["logic_frozen_cat_hockey_no_moneybags"] = slot_data["options"][
                "logic_frozen_cat_hockey_no_moneybags"]
            self.generation_options["logic_crystal_no_moneybags"] = slot_data["options"]["logic_crystal_no_moneybags"]
            self.generation_options["logic_sunny_sheila_early"] = slot_data["options"]["logic_sunny_sheila_early"]
            self.generation_options["logic_molten_early"] = slot_data["options"]["logic_molten_early"]
            self.generation_options["logic_molten_byrd_early"] = slot_data["options"]["logic_molten_byrd_early"]
            self.generation_options["logic_seashell_early"] = slot_data["options"]["logic_seashell_early"]
            self.generation_options["logic_seashell_sheila_early"] = slot_data["options"]["logic_seashell_sheila_early"]
            self.generation_options["logic_mushroom_early"] = slot_data["options"]["logic_mushroom_early"]
            self.generation_options["logic_spooky_early"] = slot_data["options"]["logic_spooky_early"]
            self.generation_options["logic_bamboo_early"] = slot_data["options"]["logic_bamboo_early"]
            self.generation_options["logic_bamboo_bentley_early"] = slot_data["options"]["logic_bamboo_bentley_early"]
            self.generation_options["logic_country_early"] = slot_data["options"]["logic_country_early"]
            self.generation_options["logic_fireworks_early"] = slot_data["options"]["logic_fireworks_early"]
            self.generation_options["logic_fireworks_agent_9_early"] = slot_data["options"][
                "logic_fireworks_agent_9_early"]
            self.generation_options["logic_charmed_early"] = slot_data["options"]["logic_charmed_early"]
            self.generation_options["logic_honey_early"] = slot_data["options"]["logic_honey_early"]
            self.generation_options["logic_dino_agent_9_early"] = slot_data["options"]["logic_dino_agent_9_early"]
            self.generation_options["logic_frozen_bentley_early"] = slot_data["options"]["logic_frozen_bentley_early"]
            self.generation_options["trap_filler_percent"] = 0
        else:
            self.generation_options["level_lock_option"] = self.options.level_lock_option.value
            self.generation_options["starting_levels_count"] = self.options.starting_levels_count.value
            self.generation_options["open_world"] = self.options.open_world.value
            self.generation_options["moneybags_settings"] = self.options.moneybags_settings.value
            self.generation_options["powerup_lock_settings"] = self.options.powerup_lock_settings.value
            self.generation_options["enable_gemsanity"] = self.options.enable_gemsanity.value
            self.generation_options["zoe_gives_hints"] = self.options.zoe_gives_hints.value
            self.generation_options["goal"] = self.options.goal.value
            self.generation_options["sorceress_door_requirement"] = self.options.sorceress_door_requirement.value
            self.generation_options["sbr_door_gem_requirement"] = self.options.sbr_door_gem_requirement.value
            self.generation_options["sbr_door_egg_requirement"] = self.options.sbr_door_egg_requirement.value
            self.generation_options["enable_25_pct_gem_checks"] = self.options.enable_25_pct_gem_checks.value
            self.generation_options["enable_50_pct_gem_checks"] = self.options.enable_50_pct_gem_checks.value
            self.generation_options["enable_75_pct_gem_checks"] = self.options.enable_75_pct_gem_checks.value
            self.generation_options["enable_gem_checks"] = self.options.enable_gem_checks.value
            self.generation_options["enable_total_gem_checks"] = self.options.enable_total_gem_checks.value
            self.generation_options["enable_skillpoint_checks"] = self.options.enable_skillpoint_checks.value
            self.generation_options["enable_life_bottle_checks"] = self.options.enable_life_bottle_checks.value
            self.generation_options["egg_count"] = self.options.egg_count.value
            self.generation_options["enable_world_keys"] = self.options.enable_world_keys.value
            self.generation_options["enable_progressive_sparx_logic"] = self.options.enable_progressive_sparx_logic.value
            self.generation_options["sparx_power_settings"] = self.options.sparx_power_settings.value
            self.generation_options["enable_progressive_sparx_health"] = self.options.enable_progressive_sparx_health.value
            self.generation_options["require_sparx_for_max_gems"] = self.options.require_sparx_for_max_gems.value
            self.generation_options["percent_extra_eggs"] = self.options.percent_extra_eggs.value
            self.generation_options["logic_cloud_backwards"] = self.options.logic_cloud_backwards.value
            self.generation_options["logic_sheila_early"] = self.options.logic_sheila_early.value
            self.generation_options["max_total_gem_checks"] = self.options.max_total_gem_checks.value
            self.generation_options["logic_byrd_early"] = self.options.logic_byrd_early.value
            self.generation_options["logic_sorceress_early"] = self.options.logic_sorceress_early.value
            self.generation_options["logic_bentley_early"] = self.options.logic_bentley_early.value
            self.generation_options["logic_spooky_no_moneybags"] = self.options.logic_spooky_no_moneybags.value
            self.generation_options["logic_molten_thieves_no_moneybags"] = self.options.logic_molten_thieves_no_moneybags.value
            self.generation_options["logic_charmed_no_moneybags"] = self.options.logic_charmed_no_moneybags.value
            self.generation_options["logic_desert_no_moneybags"] = self.options.logic_desert_no_moneybags.value
            self.generation_options["logic_frozen_cat_hockey_no_moneybags"] = self.options.logic_frozen_cat_hockey_no_moneybags.value
            self.generation_options["logic_crystal_no_moneybags"] = self.options.logic_crystal_no_moneybags.value
            self.generation_options["logic_sunny_sheila_early"] = self.options.logic_sunny_sheila_early.value
            self.generation_options["logic_molten_early"] = self.options.logic_molten_early.value
            self.generation_options["logic_molten_byrd_early"] = self.options.logic_molten_byrd_early.value
            self.generation_options["logic_seashell_early"] = self.options.logic_seashell_early.value
            self.generation_options["logic_seashell_sheila_early"] = self.options.logic_seashell_sheila_early.value
            self.generation_options["logic_mushroom_early"] = self.options.logic_mushroom_early.value
            self.generation_options["logic_spooky_early"] = self.options.logic_spooky_early.value
            self.generation_options["logic_bamboo_early"] = self.options.logic_bamboo_early.value
            self.generation_options["logic_bamboo_bentley_early"] = self.options.logic_bamboo_bentley_early.value
            self.generation_options["logic_country_early"] = self.options.logic_country_early.value
            self.generation_options["logic_fireworks_early"] = self.options.logic_fireworks_early.value
            self.generation_options["logic_fireworks_agent_9_early"] = self.options.logic_fireworks_agent_9_early.value
            self.generation_options["logic_charmed_early"] = self.options.logic_charmed_early.value
            self.generation_options["logic_honey_early"] = self.options.logic_honey_early.value
            self.generation_options["logic_dino_agent_9_early"] = self.options.logic_dino_agent_9_early.value
            self.generation_options["logic_frozen_bentley_early"] = self.options.logic_frozen_bentley_early.value
            self.generation_options["trap_filler_percent"] = self.options.trap_filler_percent.value

        is_ut = getattr(self.multiworld, "generation_is_fake", False)

        self.enabled_location_categories.add(Spyro3LocationCategory.EGG_EOL)
        self.enabled_location_categories.add(Spyro3LocationCategory.EGG)
        self.enabled_location_categories.add(Spyro3LocationCategory.EVENT)
        if self.generation_options["zoe_gives_hints"] != 0:
            self.enabled_location_categories.add(Spyro3LocationCategory.HINT)
        if self.generation_options["goal"] in [GoalOptions.ALL_SKILLPOINTS, GoalOptions.EPILOGUE]:
            self.enabled_location_categories.add(Spyro3LocationCategory.SKILLPOINT_GOAL)
        if self.generation_options["enable_25_pct_gem_checks"]:
            self.enabled_location_categories.add(Spyro3LocationCategory.GEM_25)
        if self.generation_options["enable_50_pct_gem_checks"]:
            self.enabled_location_categories.add(Spyro3LocationCategory.GEM_50)
        if self.generation_options["enable_75_pct_gem_checks"]:
            self.enabled_location_categories.add(Spyro3LocationCategory.GEM_75)
        if self.generation_options["enable_gem_checks"]:
            self.enabled_location_categories.add(Spyro3LocationCategory.GEM)
        if self.generation_options["enable_total_gem_checks"]:
            self.enabled_location_categories.add(Spyro3LocationCategory.TOTAL_GEM)
        if self.generation_options["enable_skillpoint_checks"]:
            self.enabled_location_categories.add(Spyro3LocationCategory.SKILLPOINT)
        if self.generation_options["enable_life_bottle_checks"] != LifeBottleOptions.OFF:
            self.enabled_location_categories.add(Spyro3LocationCategory.LIFE_BOTTLE)
        if self.generation_options["enable_life_bottle_checks"] == LifeBottleOptions.HARD:
            self.enabled_location_categories.add(Spyro3LocationCategory.LIFE_BOTTLE_HARD)
        if self.options.enable_gemsanity.value in [GemsanityOptions.FULL, GemsanityOptions.FULL_GLOBAL, GemsanityOptions.FULL_BUNDLES]:
            if not self.settings.allow_full_gemsanity and self.multiworld.players > 1:
                raise OptionError(f"Spyro 3: Player {self.player_name} has gemsanity set to full, which adds nearly 4000 "
                                  f"locations to the world. This may skew item placement, and at a later date this may also "
                                  f"add an equal number of progression items to the pool. "
                                  f"They must either switch to partial gemsanity, or the "
                                  f"host needs to enable allow_full_gemsanity in their host.yaml settings.")
        if self.generation_options["enable_gemsanity"] != GemsanityOptions.OFF:
            self.enabled_location_categories.add(Spyro3LocationCategory.GEMSANITY)
        if self.generation_options["enable_gemsanity"] != GemsanityOptions.OFF:
            all_gem_locations = []
            for location in location_dictionary:
                if location_dictionary[location].category == Spyro3LocationCategory.GEMSANITY:
                    if self.generation_options["goal"] != GoalOptions.EGG_HUNT or self.generation_options["egg_count"] > self.generation_options["sorceress_door_requirement"] or not location.startswith("Bugbot "):
                        all_gem_locations.append(location)
            # Universal Tracker does not know which gems were picked.  Have it assume all gems were picked when it
            # creates its seed.  The location list on the AP server will then remove all non-selected gems.
            if is_ut:
                self.chosen_gem_locations = []
            else:
                if self.generation_options["enable_gemsanity"] == GemsanityOptions.PARTIAL:
                    self.chosen_gem_locations = self.multiworld.random.sample(all_gem_locations, k=200)
                else:
                    self.chosen_gem_locations = []
        if self.generation_options["enable_gemsanity"] == GemsanityOptions.FULL:
            for itemname, item in item_dictionary.items():
                if item.category == Spyro3ItemCategory.GEMSANITY:
                    self.options.local_items.value.add(item)
        # Egg Hunt may not contain enough eggs to reach all areas.
        # If required egg count is generation_options["sorceress_door_requirement"] or fewer, change the access requirements for levels.
        if self.generation_options["goal"] == GoalOptions.EGG_HUNT:
            if self.generation_options["egg_count"] <= self.generation_options["sorceress_door_requirement"]:
                self.all_levels.remove("Sorceress")
                self.all_levels.remove("Bugbot Factory")
            if self.generation_options["egg_count"] <= 100:
                # Use 100 as the weight regardless of the door requirement.
                self.requirement_multiplier = 1.0 * self.generation_options["egg_count"] / 100
            if self.generation_options["egg_count"] <= self.generation_options["sbr_door_egg_requirement"] or \
                    self.generation_options["egg_count"] <= self.generation_options["sorceress_door_requirement"] and self.generation_options["sbr_door_gem_requirement"] > 14800:
                self.all_levels.remove("Super Bonus Round")

        if hasattr(self.multiworld, "re_gen_passthrough"):
            self.key_locked_levels = self.multiworld.re_gen_passthrough["Spyro 3"]["key_locked_levels"]
            self.level_egg_requirements = self.multiworld.re_gen_passthrough["Spyro 3"]["level_egg_requirements"]
            self.level_gem_requirements = self.multiworld.re_gen_passthrough["Spyro 3"]["level_gem_requirements"]
            self.enabled_hint_locations = self.multiworld.re_gen_passthrough["Spyro 3"]["enabled_hint_locations"]
        else:
            self.generate_entry_requirements()
            if self.generation_options["zoe_gives_hints"] != 0:
                # Randomly select which Zoes give hints.
                self.enabled_hint_locations = self.multiworld.random.sample(hint_locations, self.generation_options["zoe_gives_hints"])

        # Prevent restrictive starts.
        if self.generation_options["moneybags_settings"] == MoneybagsOptions.MONEYBAGSSANITY and not self.generation_options["logic_cloud_backwards"]:
            self.multiworld.early_items[self.player]["Moneybags Unlock - Cloud Spires Bellows"] = 1
        if self.generation_options["moneybags_settings"] != MoneybagsOptions.VANILLA and not self.generation_options["logic_sheila_early"]:
            self.multiworld.early_items[self.player]["Moneybags Unlock - Sheila"] = 1
        if self.generation_options["open_world"] and self.generation_options["enable_progressive_sparx_health"] not in [SparxUpgradeOptions.OFF, SparxUpgradeOptions.TRUE_SPARXLESS] and self.generation_options["enable_progressive_sparx_logic"]:
            self.multiworld.early_items[self.player]["Progressive Sparx Health Upgrade"] = 1
        # World keys are not compatible with open world mode.
        if self.generation_options["open_world"]:
            self.options.enable_world_keys = Toggle(0)
            self.generation_options["enable_world_keys"] = self.options.enable_world_keys.value
        # Conceptually, partial accessibility does not make sense in Spyro 3 and just leads to generation failures.
        # Exception: Goal is Spike or Scorch.
        if self.generation_options["goal"] not in [GoalOptions.SCORCH, GoalOptions.SPIKE]:
            self.options.accessibility = Accessibility(0)  # Full
            self.generation_options["accessibility"] = self.options.accessibility.value

    def create_regions(self):
        # Create Regions
        regions: Dict[str, Region] = {}
        regions["Menu"] = self.create_region("Menu", [])
        regions.update({region_name: self.create_region(region_name, location_tables[region_name]) for region_name in (self.all_levels + ["Inventory"])})
        
        # Connect Regions
        def create_connection(from_region: str, to_region: str):
            connection = Entrance(self.player, f"{to_region}", regions[from_region])
            regions[from_region].exits.append(connection)
            connection.connect(regions[to_region])
            
        create_connection("Menu", "Sunrise Spring")
        create_connection("Menu", "Inventory")
                
        create_connection("Sunrise Spring", "Sunny Villa")
        create_connection("Sunrise Spring", "Cloud Spires")
        create_connection("Sunrise Spring", "Molten Crater")
        create_connection("Sunrise Spring", "Seashell Shore")
        create_connection("Sunrise Spring", "Mushroom Speedway")
        create_connection("Sunrise Spring", "Sheila's Alp")
             
        create_connection("Sunrise Spring", "Buzz")
        create_connection("Sunrise Spring", "Crawdad Farm")
        create_connection("Sunrise Spring", "Midday Gardens")
        
        create_connection("Midday Gardens", "Icy Peak")
        create_connection("Midday Gardens", "Enchanted Towers")
        create_connection("Midday Gardens", "Spooky Swamp")
        create_connection("Midday Gardens", "Bamboo Terrace")
        create_connection("Midday Gardens", "Country Speedway")
        create_connection("Midday Gardens", "Sgt. Byrd's Base")

        create_connection("Midday Gardens", "Spike")
        create_connection("Midday Gardens", "Spider Town")
        create_connection("Midday Gardens", "Evening Lake")
        
        create_connection("Evening Lake", "Frozen Altars")
        create_connection("Evening Lake", "Lost Fleet")
        create_connection("Evening Lake", "Fireworks Factory")
        create_connection("Evening Lake", "Charmed Ridge")
        create_connection("Evening Lake", "Honey Speedway")
        create_connection("Evening Lake", "Bentley's Outpost")

        create_connection("Evening Lake", "Scorch")
        create_connection("Evening Lake", "Starfish Reef")        
        create_connection("Evening Lake", "Midnight Mountain")   
        
        create_connection("Midnight Mountain", "Crystal Islands")
        create_connection("Midnight Mountain", "Desert Ruins")
        create_connection("Midnight Mountain", "Haunted Tomb")
        create_connection("Midnight Mountain", "Dino Mines")
        create_connection("Midnight Mountain", "Harbor Speedway")
        create_connection("Midnight Mountain", "Agent 9's Lab")

        if self.generation_options["goal"] != GoalOptions.EGG_HUNT or self.generation_options["egg_count"] > self.generation_options["sorceress_door_requirement"]:
            create_connection("Midnight Mountain", "Sorceress")
            create_connection("Midnight Mountain", "Bugbot Factory")
        if self.generation_options["goal"] != GoalOptions.EGG_HUNT or self.generation_options["egg_count"] > self.generation_options["sbr_door_egg_requirement"] and \
                (self.generation_options["egg_count"] > self.generation_options["sorceress_door_requirement"] or self.generation_options["sbr_door_gem_requirement"] <= 14800):
            create_connection("Midnight Mountain", "Super Bonus Round")

    # For each region, add the associated locations retrieved from the corresponding location_table
    def create_region(self, region_name, location_table) -> Region:
        new_region = Region(region_name, self.player, self.multiworld)
        for location in location_table:
            if self.generation_options["goal"] == GoalOptions.EGG_HUNT and \
                    ((self.generation_options["egg_count"] <= self.generation_options["sorceress_door_requirement"] and (location.name.startswith("Bugbot ") or
                    location.name.startswith == "Sorceress" or
                    location.name == "Midnight Mountain Home: Moneybags Chase Complete" or
                    location.name == "Midnight Mountain Home: Egg for sale. (Al)")) or
                    ((self.generation_options["egg_count"] <= self.generation_options["sbr_door_egg_requirement"] or self.generation_options["egg_count"] <= self.generation_options["sorceress_door_requirement"] and self.generation_options["sbr_door_gem_requirement"] > 14800) and location.name.startswith("Super Bonus Round"))):
                continue
            if location.category in self.enabled_location_categories and location.category == Spyro3LocationCategory.EGG_EOL and self.generation_options["open_world"]:
                filler_item = self.create_item("Filler")
                new_location = Spyro3Location(
                    self.player,
                    location.name,
                    location.category,
                    "Filler",
                    None,
                    new_region
                )
                new_location.place_locked_item(filler_item)
                new_region.locations.append(new_location)
            elif location.category in self.enabled_location_categories and location.category not in [Spyro3LocationCategory.EVENT, Spyro3LocationCategory.GEMSANITY, Spyro3LocationCategory.HINT, Spyro3LocationCategory.TOTAL_GEM]:
                new_location = Spyro3Location(
                    self.player,
                    location.name,
                    location.category,
                    location.default_item,
                    self.location_name_to_id[location.name],
                    new_region
                )
                new_region.locations.append(new_location)
            elif location.category in self.enabled_location_categories and \
                    location.category == Spyro3LocationCategory.GEMSANITY and \
                    (len(self.chosen_gem_locations) == 0 or location.name in self.chosen_gem_locations):
                new_location = Spyro3Location(
                    self.player,
                    location.name,
                    location.category,
                    location.default_item,
                    self.location_name_to_id[location.name],
                    new_region
                )
                new_region.locations.append(new_location)
            elif location.category in self.enabled_location_categories and location.category == Spyro3LocationCategory.TOTAL_GEM:
                gems_needed = int(location.name.split("Total Gems: ")[1])
                if gems_needed <= self.generation_options["max_total_gem_checks"] and not (self.generation_options["goal"] == GoalOptions.EGG_HUNT and gems_needed > 14800):
                    new_location = Spyro3Location(
                        self.player,
                        location.name,
                        location.category,
                        location.default_item,
                        self.location_name_to_id[location.name],
                        new_region
                    )
                    new_region.locations.append(new_location)
            elif location.category in self.enabled_location_categories and location.category == Spyro3LocationCategory.HINT and location.name in self.enabled_hint_locations:
                new_location = Spyro3Location(
                    self.player,
                    location.name,
                    location.category,
                    location.default_item,
                    self.location_name_to_id[location.name],
                    new_region
                )
                new_region.locations.append(new_location)
            elif location.category == Spyro3LocationCategory.EVENT and self.generation_options["open_world"] and \
                    (
                        location.name.endswith(" Complete") and
                        location.name not in ["Crawdad Farm Complete", "Spider Town Complete", "Starfish Reef Complete", "Bugbot Factory Complete", "Midnight Mountain Home: Moneybags Chase Complete", "Super Bonus Round Complete"] or
                        location.name.endswith(" Defeated") and location.name != "Sorceress Defeated"
                    ):
                event_item = self.create_item(location.default_item)
                new_location = Spyro3Location(
                    self.player,
                    location.name,
                    location.category,
                    location.default_item,
                    None,
                    new_region
                )
                event_item.code = None
                new_location.place_locked_item(event_item)
                new_region.locations.append(new_location)
            elif location.category == Spyro3LocationCategory.EVENT:
                event_item = self.create_item(location.default_item)
                new_location = Spyro3Location(
                    self.player,
                    location.name,
                    location.category,
                    location.default_item,
                    self.location_name_to_id[location.name],
                    new_region
                )
                event_item.code = None
                new_location.place_locked_item(event_item)
                new_region.locations.append(new_location)

        self.multiworld.regions.append(new_region)
        return new_region

    def create_items(self):
        itempool: List[Spyro3Item] = []
        itempoolSize = 0
        placedEggs = 0
        remainingHints = []
        for i in range(self.generation_options["zoe_gives_hints"]):
            remainingHints.append(f"Hint {i + 1}")
        for location in self.multiworld.get_locations(self.player):
                item_data = item_dictionary[location.default_item_name]
                # There is a bug with the current client implementation where another player auto-collecting an item on the
                # goal condition results in the client thinking the player has completed the goal.
                # To avoid this, ensure the goal item is always vanilla.  Manually placed items exist outside the item pool.
                # TODO: Remove this restriction after implementing a better client solution.
                if item_data.category == Spyro3ItemCategory.HINT:
                    if len(remainingHints) == 0:
                        raise Exception('Ran out of hints to place.')
                    hint = self.multiworld.random.choice(remainingHints)
                    remainingHints.remove(hint)
                    item = self.create_item(hint)
                    self.multiworld.get_location(location.name, self.player).place_locked_item(item)
                elif item_data.category in [Spyro3ItemCategory.SKIP] or \
                        location.category in [Spyro3LocationCategory.EVENT] or \
                        (self.generation_options["open_world"] and location.category == Spyro3LocationCategory.EGG_EOL) or \
                        (self.generation_options["goal"] in [GoalOptions.ALL_SKILLPOINTS, GoalOptions.EPILOGUE] and location.category == Spyro3LocationCategory.SKILLPOINT_GOAL):
                    item = self.create_item(location.default_item_name)
                    self.multiworld.get_location(location.name, self.player).place_locked_item(item)
                elif location.category in self.enabled_location_categories:
                    itempoolSize += 1

        foo = BuildItemPool(self, itempoolSize, placedEggs, self.options, self.key_locked_levels)

        for item in foo:
            itempool.append(self.create_item(item.name))

        # Add regular items to itempool
        self.multiworld.itempool += itempool

    def create_item(self, name: str) -> Item:
        useful_categories = [Spyro3ItemCategory.SPARX_POWERUP]
        data = self.item_name_to_id[name]

        # Settings info will not be available for or relevant to item link handling - items created by item link cannot
        # rely on methods like generate_early().
        # When required settings data is unavailable for this reason, restrict the item to progression.
        if name in key_item_names or item_dictionary[name].category == Spyro3ItemCategory.EGG \
                or item_dictionary[name].category == Spyro3ItemCategory.EVENT \
                or item_dictionary[name].category == Spyro3ItemCategory.SKILLPOINT_GOAL \
                or item_dictionary[name].category == Spyro3ItemCategory.LEVEL_KEY \
                or item_dictionary[name].category == Spyro3ItemCategory.WORLD_KEY \
                or item_dictionary[name].category == Spyro3ItemCategory.GEMSANITY \
                or (
                    name == 'Progressive Sparx Health Upgrade' and
                    (
                        "enable_progressive_sparx_logic" not in self.generation_options or
                        self.generation_options["enable_progressive_sparx_logic"]
                    )
                ) \
                or name == "Glitched Item" \
                or (
                    name == 'Sparx Gem Finder' and
                    (
                        "require_sparx_for_max_gems" not in self.generation_options or
                        self.generation_options["require_sparx_for_max_gems"] == SparxForGemsOptions.SPARX_FINDER
                    )
                ):
            item_classification = ItemClassification.progression
        elif item_dictionary[name].category == Spyro3ItemCategory.MONEYBAGS:
            item_classification = ItemClassification.progression
            # Moneybags unlocks the player says they don't need are useful, not progression.
            # No way to skip into Agent 9 early, and skipping into Nancy is missable.
            if "logic_sheila_early" in self.generation_options and (
                    name == "Moneybags Unlock - Sheila" and self.generation_options["logic_sheila_early"] or
                    name == "Moneybags Unlock - Sgt. Byrd" and self.generation_options["logic_byrd_early"] or
                    name == "Moneybags Unlock - Bentley" and self.generation_options["logic_bentley_early"] or
                    name == "Moneybags Unlock - Cloud Spires Bellows" and self.generation_options["logic_cloud_backwards"] or
                    name == "Moneybags Unlock - Spooky Swamp Door" and self.generation_options["logic_spooky_no_moneybags"] or
                    name == "Moneybags Unlock - Molten Crater Thieves Door" and self.generation_options["logic_molten_thieves_no_moneybags"] or
                    name == "Moneybags Unlock - Charmed Ridge Stairs" and self.generation_options["logic_charmed_no_moneybags"] or
                    name == "Moneybags Unlock - Desert Ruins Door" and self.generation_options["logic_desert_no_moneybags"] or
                    name == "Moneybags Unlock - Frozen Altars Cat Hockey Door" and self.generation_options["logic_frozen_cat_hockey_no_moneybags"] or
                    name == "Moneybags Unlock - Crystal Islands Bridge" and self.generation_options["logic_crystal_no_moneybags"] or
                    name == "Moneybags Unlock - Spooky Swamp Door" and self.generation_options["open_world"] or
                    name == "Moneybags Unlock - Charmed Ridge Stairs" and self.generation_options["open_world"]
                ):
                item_classification = ItemClassification.useful
            else:
                item_classification = ItemClassification.progression
        elif item_dictionary[name].category in [Spyro3ItemCategory.INDIVIDUAL_POWERUP, Spyro3ItemCategory.TYPE_POWERUP]:
            item_classification = ItemClassification.progression
        elif item_dictionary[name].category in useful_categories \
            or (
                name == 'Progressive Sparx Health Upgrade' and
                "enable_progressive_sparx_logic" in self.generation_options and
                not self.generation_options["enable_progressive_sparx_logic"]
            ):
            item_classification = ItemClassification.useful
        elif item_dictionary[name].category == Spyro3ItemCategory.TRAP:
            item_classification = ItemClassification.trap
        else:
            item_classification = ItemClassification.filler

        return Spyro3Item(name, item_classification, data, self.player)

    def get_filler_item_name(self) -> str:
        return "Extra Life"
    
    def set_rules(self) -> None:          
        def is_level_completed(self, level, state):
            if self.generation_options["open_world"] and level not in [
                "Super Bonus Round", "Crawdad Farm", "Spider Town", "Starfish Reef", "Bugbot Factory",
                "Crystal Islands", "Desert Ruins", "Haunted Tomb", "Dino Mines", "Agent 9's Lab"
            ]:
                return True
            return state.has(level + " Complete", self.player)
        
        def is_boss_defeated(self, boss, state):
            if self.generation_options["open_world"] and boss != "Sorceress":
                return True
            return state.has(boss + " Defeated", self.player)

        def is_companion_unlocked(self, companion, state):
            return state.has(f"Moneybags Unlock - {companion}", self.player) or is_boss_defeated(self, "Sorceress", state)

        def has_world_keys(self, key_count, state):
            return state.count("World Key", self.player) >= key_count

        def can_enter_non_companion_portal(self, level, state, oob_logic):
            if self.generation_options["level_lock_option"] == LevelLockOptions.VANILLA:
                return has_entrance_eggs(self, level, state) or oob_logic
            elif self.generation_options["level_lock_option"] == LevelLockOptions.KEYS:
                return state.has(f"{level} Unlock", self.player)
            elif self.generation_options["level_lock_option"] in [LevelLockOptions.RANDOM_REQS, LevelLockOptions.ADD_REQS] or \
                    self.generation_options["level_lock_option"] == LevelLockOptions.ADD_GEM_REQS and (
                    self.generation_options["moneybags_settings"] != MoneybagsOptions.MONEYBAGSSANITY or
                    self.generation_options["enable_gemsanity"] == GemsanityOptions.OFF
            ):
                return has_entrance_eggs(self, level, state)
            else:
                return has_entrance_eggs(self, level, state) and has_entrance_gems(self, level, state)

        def has_entrance_eggs(self, level, state):
            return state.count("Egg", self.player) >= math.floor(self.requirement_multiplier * self.level_egg_requirements[level])

        def has_entrance_gems(self, level, state):
            return has_total_accessible_gems(self, state, self.level_gem_requirements[level])

        def has_optional_moneybags_unlock(self, unlock, state):
            if self.generation_options["moneybags_settings"] != MoneybagsOptions.MONEYBAGSSANITY:
                return True
            return state.has(f"Moneybags Unlock - {unlock}", self.player) or (self.generation_options["goal"] != GoalOptions.EGG_HUNT or self.generation_options["egg_count"] > self.generation_options["sorceress_door_requirement"]) and is_boss_defeated(self, "Sorceress", state)

        def are_gems_accessible(self, state):
            if self.generation_options["enable_gemsanity"] != GemsanityOptions.OFF:
                return True
            if self.generation_options["enable_progressive_sparx_health"] == SparxUpgradeOptions.TRUE_SPARXLESS:
                return True
            if self.generation_options["require_sparx_for_max_gems"] == SparxForGemsOptions.GREEN_SPARX:
                if self.generation_options["enable_progressive_sparx_logic"] and not has_sparx_health(self, 1, state):
                    return False
            elif self.generation_options["require_sparx_for_max_gems"] == SparxForGemsOptions.SPARX_FINDER:
                if self.generation_options["enable_progressive_sparx_logic"] and not has_sparx_health(self, 1, state):
                    return False
                elif self.generation_options["sparx_power_settings"] and not state.has("Sparx Gem Finder", self.player):
                    return False
                elif not self.generation_options["sparx_power_settings"] and not state.has("Spider Town Complete", self.player):
                    return False
            return True

        def is_glitched_logic(self, state):
            return state.has("Glitched Item", self.player)

        def get_gemsanity_gems(self, level, state):
            return state.count(f"{level} 50 Gems", self.player) * 50 + state.count(f"{level} 100 Gems", self.player) * 100

        def get_gems_accessible_in_level(self, level, state):
            # TODO: It may be worth splitting this into some sort of standardized Logic framework.
            # At present, some logic is duplicated between here
            # and location rules, but a framework to avoid this may be overkill.  Determine if it is
            # desirable to build a framework.
            if self.generation_options["enable_gemsanity"] != GemsanityOptions.OFF and level != "Super Bonus Round":
                return get_gemsanity_gems(self, level, state)

            level_gems = 0
            ignore_sparx_restrictions = False
            # Older versions of Python do not support switch statements, so use if/elif.
            if level == 'Sunrise Spring':
                level_gems = 400
            elif level == 'Sunny Villa':
                if not can_enter_non_companion_portal(self, level, state, True):
                    return 0
                # Sheila's area has 89 gems, skateboarding has 92.  All skateboarding gems are available regardless
                # of Hunter's state.
                level_gems = 311
                if self.generation_options["logic_sunny_sheila_early"] or is_level_completed(self, "Sheila's Alp", state):
                    level_gems += 89
            elif level == 'Cloud Spires':
                if not can_enter_non_companion_portal(self, level, state, True):
                    return 0
                # 171 gems are available logically before the Bellows unlock, with an extra 5 being possible in easy mode,
                # since an enemy's gem falls to the start of the level.
                # All gems are available doing the level backwards.
                level_gems = 171
                if self.generation_options["moneybags_settings"] != MoneybagsOptions.MONEYBAGSSANITY or \
                        self.generation_options["logic_cloud_backwards"] or \
                        state.has("Moneybags Unlock - Cloud Spires Bellows", self.player):
                    level_gems += 229
            elif level == 'Molten Crater':
                if not can_enter_non_companion_portal(self, level, state, self.generation_options["logic_molten_early"]):
                    return 0
                # 109 gems in the Byrd subarea, 106 in thieves.
                level_gems = 185
                if self.generation_options["logic_molten_thieves_no_moneybags"] or \
                        has_optional_moneybags_unlock(self, "Molten Crater Thieves Door", state):
                    level_gems += 106
                if is_level_completed(self, "Sgt. Byrd's Base", state) or self.generation_options["logic_molten_byrd_early"]:
                    level_gems += 109
            elif level == 'Seashell Shore':
                if not can_enter_non_companion_portal(self, level, state, self.generation_options["logic_seashell_early"]):
                    return 0
                # 105 gems in the Sheila sub area.
                level_gems = 295
                if self.generation_options["logic_seashell_sheila_early"] or is_level_completed(self, "Sheila's Alp", state):
                    level_gems += 105
            elif level == 'Mushroom Speedway':
                if not can_enter_non_companion_portal(self, level, state, self.generation_options["logic_mushroom_early"]):
                    return 0
                level_gems = 400
                ignore_sparx_restrictions = True
            elif level == "Sheila's Alp":
                if not self.generation_options["logic_sheila_early"] and \
                        self.generation_options["moneybags_settings"] != MoneybagsOptions.VANILLA and \
                        not (state.has("Moneybags Unlock - Sheila", self.player) or is_boss_defeated(self, "Sorceress", state)):
                    return 0
                level_gems = 400
            elif level == "Crawdad Farm":
                if not is_boss_defeated(self, "Buzz", state) or \
                        (self.generation_options["enable_progressive_sparx_logic"] and not (has_sparx_health(self, 1, state) or is_glitched_logic(self, state))):
                    return 0
                level_gems = 200
                ignore_sparx_restrictions = True
            elif level == 'Midday Gardens':
                if not is_boss_defeated(self, "Buzz", state) or \
                        (self.generation_options["enable_world_keys"] and not has_world_keys(self, 1, state)):
                    return 0
                level_gems = 379
                if self.generation_options["powerup_lock_settings"] == PowerupLockOptions.VANILLA or \
                    self.generation_options["powerup_lock_settings"] == PowerupLockOptions.TYPE and state.has("Fireball Powerup", self.player) or \
                    self.generation_options["powerup_lock_settings"] == PowerupLockOptions.INDIVIDUAL and state.has("Midday Fireball Powerup", self.player):
                    level_gems = level_gems + 21
            elif level == 'Icy Peak':
                if not is_boss_defeated(self, "Buzz", state) or \
                        (self.generation_options["enable_progressive_sparx_logic"] and not (has_sparx_health(self, 1, state) or is_glitched_logic(self, state))) or \
                        (self.generation_options["enable_world_keys"] and not has_world_keys(self, 1, state)):
                    return 0
                if not can_enter_non_companion_portal(self, level, state, True):
                    return 0
                level_gems = 500
            elif level == 'Enchanted Towers':
                if not is_boss_defeated(self, "Buzz", state) or \
                        (self.generation_options["enable_progressive_sparx_logic"] and not (has_sparx_health(self, 1, state) or is_glitched_logic(self, state))) or \
                        (self.generation_options["enable_world_keys"] and not has_world_keys(self, 1, state)):
                    return 0
                if not can_enter_non_companion_portal(self, level, state, True):
                    return 0
                level_gems = 437
                if is_level_completed(self, "Sgt. Byrd's Base", state):
                    level_gems += 63
            elif level == 'Spooky Swamp':
                if not is_boss_defeated(self, "Buzz", state) or \
                        (self.generation_options["enable_progressive_sparx_logic"] and not (has_sparx_health(self, 1, state) or is_glitched_logic(self, state))) or \
                        (self.generation_options["enable_world_keys"] and not has_world_keys(self, 1, state)):
                    return 0
                if not can_enter_non_companion_portal(self, level, state, self.generation_options["logic_spooky_early"]):
                    return 0
                level_gems = 219
                if self.generation_options["open_world"] or self.generation_options["moneybags_settings"] != MoneybagsOptions.MONEYBAGSSANITY or self.generation_options["logic_spooky_no_moneybags"] or state.has("Moneybags Unlock - Spooky Swamp Door", self.player):
                    level_gems += 281
            elif level == 'Bamboo Terrace':
                if not is_boss_defeated(self, "Buzz", state) or \
                        (self.generation_options["enable_progressive_sparx_logic"] and not (has_sparx_health(self, 1, state) or is_glitched_logic(self, state))) or \
                        (self.generation_options["enable_world_keys"] and not has_world_keys(self, 1, state)):
                    return 0
                if not can_enter_non_companion_portal(self, level, state, self.generation_options["logic_bamboo_early"]):
                    return 0
                # Bentley's subarea has 189 gems.
                level_gems = 311
                if is_level_completed(self, "Bentley's Outpost", state) or self.generation_options["logic_bamboo_bentley_early"]:
                    level_gems += 189
            elif level == 'Country Speedway':
                if not is_boss_defeated(self, 'Buzz', state) or \
                        (self.generation_options["enable_world_keys"] and not has_world_keys(self, 1, state)):
                    return 0
                if not can_enter_non_companion_portal(self, level, state, self.generation_options["logic_country_early"]):
                    return 0
                level_gems = 400
                ignore_sparx_restrictions = True
            elif level == "Sgt. Byrd's Base":
                if not is_boss_defeated(self, 'Buzz', state) or \
                        not self.generation_options["logic_byrd_early"] and self.generation_options["moneybags_settings"] != MoneybagsOptions.VANILLA and not (state.has("Moneybags Unlock - Sgt. Byrd", self.player) or is_boss_defeated(self, "Sorceress", state)) or \
                        (self.generation_options["enable_progressive_sparx_logic"] and not (has_sparx_health(self, 1, state) or is_glitched_logic(self, state))) or \
                        (self.generation_options["enable_world_keys"] and not has_world_keys(self, 1, state)):
                    return 0
                level_gems = 500
            elif level == 'Spider Town':
                if not is_boss_defeated(self, 'Spike', state) or not is_level_completed(self, 'Crawdad Farm', state):
                    return 0
                level_gems = 200
                ignore_sparx_restrictions = True
            elif level == 'Evening Lake':
                if not is_boss_defeated(self, 'Spike', state) or (self.generation_options["enable_world_keys"] and not has_world_keys(self, 2, state)):
                    return 0
                level_gems = 352
                if self.generation_options["powerup_lock_settings"] == PowerupLockOptions.VANILLA or \
                    self.generation_options["powerup_lock_settings"] == PowerupLockOptions.TYPE and state.has("Invincibility Powerup", self.player) or \
                    self.generation_options["powerup_lock_settings"] == PowerupLockOptions.INDIVIDUAL and state.has("Evening Invincibility Powerup", self.player):
                    level_gems += 48
            elif level == 'Frozen Altars':
                if not is_boss_defeated(self, "Spike", state) or \
                        (self.generation_options["enable_progressive_sparx_logic"] and not (has_sparx_health(self, 1, state) or is_glitched_logic(self, state))) or \
                        (self.generation_options["enable_world_keys"] and not has_world_keys(self, 2, state)):
                    return 0
                if not can_enter_non_companion_portal(self, level, state, True):
                    return 0
                level_gems = 600
            elif level == 'Lost Fleet':
                if not is_boss_defeated(self, "Spike", state) or \
                        (self.generation_options["enable_progressive_sparx_logic"] and not (has_sparx_health(self, 1, state) or is_glitched_logic(self, state))) or \
                        (self.generation_options["enable_world_keys"] and not has_world_keys(self, 2, state)):
                    return 0
                if not can_enter_non_companion_portal(self, level, state, True):
                    return 0
                # 100 gems in skateboarding area.  Of these, 11 are accessible easily without the skateboard.
                # Roughly 19 require the skateboard, and the rest can be obtained with a medium difficulty jump onto the track, but these are not in logic.
                level_gems = 330
                if self.generation_options["powerup_lock_settings"] == PowerupLockOptions.VANILLA or \
                    self.generation_options["powerup_lock_settings"] == PowerupLockOptions.TYPE and state.has("Invincibility Powerup", self.player) or \
                    self.generation_options["powerup_lock_settings"] == PowerupLockOptions.INDIVIDUAL and state.has("Fleet Invincibility Powerup", self.player):
                    level_gems += 181
                if is_boss_defeated(self, 'Scorch', state) or is_glitched_logic(self, state):
                    level_gems += 89
            elif level == 'Fireworks Factory':
                if not is_boss_defeated(self, "Spike", state) or \
                        (self.generation_options["enable_progressive_sparx_logic"] and not (has_sparx_health(self, 2, state) or is_glitched_logic(self, state))) or \
                        (self.generation_options["enable_world_keys"] and not has_world_keys(self, 2, state)):
                    return 0
                if not can_enter_non_companion_portal(self, level, state, self.generation_options["logic_fireworks_early"]):
                    return 0
                # 175 gems in the Agent 9 subarea.
                level_gems = 414
                if self.generation_options["powerup_lock_settings"] == PowerupLockOptions.VANILLA or \
                    self.generation_options["powerup_lock_settings"] == PowerupLockOptions.TYPE and state.has("Fireball Powerup", self.player) and state.has("Invincibility Powerup", self.player) or \
                    self.generation_options["powerup_lock_settings"] == PowerupLockOptions.INDIVIDUAL and state.has("Fireworks Combo Powerup", self.player):
                    level_gems += 11
                if is_level_completed(self, "Agent 9's Lab", state) or self.generation_options["logic_fireworks_agent_9_early"]:
                    level_gems += 175
            elif level == 'Charmed Ridge':
                if not is_boss_defeated(self, "Spike", state) or \
                        (self.generation_options["enable_progressive_sparx_logic"] and not (has_sparx_health(self, 2, state) or is_glitched_logic(self, state))) or \
                        (self.generation_options["enable_world_keys"] and not has_world_keys(self, 2, state)):
                    return 0
                if not can_enter_non_companion_portal(self, level, state, self.generation_options["logic_charmed_early"]):
                    return 0
                # Moneybags blocks 472 gems.
                level_gems = 128
                if self.generation_options["open_world"] or self.generation_options["moneybags_settings"] != MoneybagsOptions.MONEYBAGSSANITY or self.generation_options["logic_charmed_no_moneybags"] or state.has("Moneybags Unlock - Charmed Ridge Stairs", self.player):
                    level_gems += 470
                    if self.generation_options["powerup_lock_settings"] == PowerupLockOptions.VANILLA or \
                        self.generation_options["powerup_lock_settings"] == PowerupLockOptions.TYPE and state.has("Fireball Powerup", self.player) or \
                        self.generation_options["powerup_lock_settings"] == PowerupLockOptions.INDIVIDUAL and state.has("Charmed Fireball Powerup", self.player):
                        level_gems += 2
            elif level == 'Honey Speedway':
                if not is_boss_defeated(self, "Spike", state) or \
                        (self.generation_options["enable_world_keys"] and not has_world_keys(self, 2, state)):
                    return 0
                if not can_enter_non_companion_portal(self, level, state, self.generation_options["logic_honey_early"]):
                    return 0
                level_gems = 400
                ignore_sparx_restrictions = True
            elif level == "Bentley's Outpost":
                if not is_boss_defeated(self, 'Spike', state) or \
                        not self.generation_options["logic_bentley_early"] and self.generation_options["moneybags_settings"] != MoneybagsOptions.VANILLA and not (state.has("Moneybags Unlock - Bentley", self.player) or is_boss_defeated(self, "Sorceress", state)) or \
                        (self.generation_options["enable_progressive_sparx_logic"] and not (has_sparx_health(self, 1, state) or is_glitched_logic(self, state))) or \
                        (self.generation_options["enable_world_keys"] and not has_world_keys(self, 2, state)):
                    return 0
                level_gems = 600
            elif level == 'Starfish Reef':
                if not is_boss_defeated(self, 'Scorch', state) or not is_level_completed(self, 'Spider Town', state):
                    return 0
                level_gems = 200
                ignore_sparx_restrictions = True
            elif level == 'Midnight Mountain':
                if not is_boss_defeated(self, 'Scorch', state) or (self.generation_options["enable_world_keys"] and not has_world_keys(self, 3, state)):
                    return 0
                level_gems = 400
            elif level == 'Crystal Islands':
                if not is_boss_defeated(self, "Scorch", state) or \
                        (self.generation_options["enable_progressive_sparx_logic"] and not (has_sparx_health(self, 2, state) or is_glitched_logic(self, state))) or \
                        (self.generation_options["enable_world_keys"] and not has_world_keys(self, 3, state)):
                    return 0
                if not can_enter_non_companion_portal(self, level, state, True):
                    return 0
                # Moneybags locks 475 gems.
                level_gems = 225
                if self.generation_options["logic_crystal_no_moneybags"] or has_optional_moneybags_unlock(self, "Crystal Islands Bridge", state):
                    level_gems += 351
                    if self.generation_options["powerup_lock_settings"] == PowerupLockOptions.VANILLA or \
                        self.generation_options["powerup_lock_settings"] == PowerupLockOptions.TYPE and state.has("Superfly Powerup", self.player) or \
                        self.generation_options["powerup_lock_settings"] == PowerupLockOptions.INDIVIDUAL and state.has("Crystal Superfly Powerup", self.player):
                        level_gems += 124
            elif level == 'Desert Ruins':
                if not is_boss_defeated(self, "Scorch", state) or \
                        (self.generation_options["enable_progressive_sparx_logic"] and not (has_sparx_health(self, 2, state) or is_glitched_logic(self, state))) or \
                        (self.generation_options["enable_world_keys"] and not has_world_keys(self, 3, state)):
                    return 0
                if not can_enter_non_companion_portal(self, level, state, True):
                    return 0
                # 252 gems are locked behind Moneybags.
                level_gems = 448
                if self.generation_options["logic_desert_no_moneybags"] or has_optional_moneybags_unlock(self, "Desert Ruins Door", state):
                    level_gems += 252
            elif level == 'Haunted Tomb':
                if not is_boss_defeated(self, "Scorch", state) or \
                        (self.generation_options["enable_progressive_sparx_logic"] and not (has_sparx_health(self, 2, state) or is_glitched_logic(self, state))) or \
                        (self.generation_options["enable_world_keys"] and not has_world_keys(self, 3, state)):
                    return 0
                if not can_enter_non_companion_portal(self, level, state, False):
                    return 0
                level_gems = 700
            elif level == 'Dino Mines':
                if not is_boss_defeated(self, "Scorch", state) or \
                        (self.generation_options["enable_progressive_sparx_logic"] and not (has_sparx_health(self, 3, state) or is_glitched_logic(self, state))) or \
                        (self.generation_options["enable_world_keys"] and not has_world_keys(self, 3, state)):
                    return 0
                if not can_enter_non_companion_portal(self, level, state, False):
                    return 0
                # 108 gems in Agent 9's subarea. This can be entered from out of bounds.
                level_gems = 592
                if self.generation_options["logic_dino_agent_9_early"] or is_level_completed(self, "Agent 9's Lab", state):
                    level_gems += 108
            elif level == 'Harbor Speedway':
                if not is_boss_defeated(self, "Scorch", state) or \
                        (self.generation_options["enable_world_keys"] and not has_world_keys(self, 3, state)):
                    return 0
                if not can_enter_non_companion_portal(self, level, state, False):
                    return 0
                level_gems = 400
                ignore_sparx_restrictions = True
            elif level == "Agent 9's Lab":
                if not is_boss_defeated(self, 'Scorch', state) or \
                        self.generation_options["moneybags_settings"] != MoneybagsOptions.VANILLA and not state.has("Moneybags Unlock - Agent 9", self.player) and not is_boss_defeated(self, 'Sorceress', state) or \
                        (self.generation_options["enable_progressive_sparx_logic"] and not (has_sparx_health(self, 2, state) or is_glitched_logic(self, state))) or \
                        (self.generation_options["enable_world_keys"] and not has_world_keys(self, 3, state)):
                    return 0
                level_gems = 700
            elif level == 'Bugbot Factory':
                if not is_boss_defeated(self, 'Sorceress', state) or not is_level_completed(self, 'Starfish Reef', state):
                    return 0
                level_gems = 200
                ignore_sparx_restrictions = True
            elif level == 'Super Bonus Round':
                if not state.has("Egg", self.player, self.generation_options["sbr_door_egg_requirement"]) or not has_gems_for_sbr(self, state):
                    return 0
                level_gems = 3775
                if self.generation_options["powerup_lock_settings"] == PowerupLockOptions.VANILLA or \
                    self.generation_options["powerup_lock_settings"] == PowerupLockOptions.TYPE and state.has("Fireball Powerup", self.player) and state.has("Superfly Powerup", self.player) or \
                    self.generation_options["powerup_lock_settings"] == PowerupLockOptions.INDIVIDUAL and state.has("Super Bonus Round Combo Powerup", self.player):
                    level_gems += 1225
            if not are_gems_accessible(self, state) and not ignore_sparx_restrictions and not is_glitched_logic(self, state):
                level_gems = int(level_gems * 0.75)
            return level_gems

        def has_total_accessible_gems(self, state, max_gems, include_sbr=True, include_moneybags=True):
            accessible_gems = 0

            for level in self.all_levels:
                if include_sbr or level != 'Super Bonus Round':
                    accessible_gems += get_gems_accessible_in_level(self, level, state)

            if include_moneybags and \
                    self.generation_options["moneybags_settings"] != MoneybagsOptions.MONEYBAGSSANITY and \
                    (self.generation_options["goal"] != GoalOptions.EGG_HUNT or self.generation_options["egg_count"] > self.generation_options["sorceress_door_requirement"]) and \
                    not is_boss_defeated(self, "Sorceress", state) and \
                    self.generation_options["enable_gemsanity"] == GemsanityOptions.OFF:
                # Remove gems for possible Moneybags payments.  To avoid a player locking themselves out of progression,
                # we have to assume every possible payment is made, including anywhere the player can skip into the level
                # out of logic and then pay Moneybags.
                # Further, because total gem checks cannot go out of logic by progressing, group all the payments
                # together at the start.  This means that in logic, total gem checks are unavailable early.
                if self.generation_options["moneybags_settings"] != MoneybagsOptions.COMPANIONSANITY:
                    if not self.generation_options["open_world"]:
                        accessible_gems -= 3300
                # While portal locking prevents some payments,
                # unlocking a later level could take checks out of logic.
                # This breaks AP generation rules.
                accessible_gems -= 4700
            return accessible_gems >= max_gems

        def has_gems_for_sbr(self, state):
            # Don't include SBR in gem calculations to avoid recursion issues.
            return has_total_accessible_gems(self, state, self.generation_options["sbr_door_gem_requirement"], include_sbr=False)

        def has_sparx_health(self, health, state):
            if self.generation_options["enable_progressive_sparx_health"] in [SparxUpgradeOptions.OFF, SparxUpgradeOptions.TRUE_SPARXLESS]:
                return True
            max_health = 0
            if self.generation_options["enable_progressive_sparx_health"] == SparxUpgradeOptions.BLUE:
                max_health = 2
            elif self.generation_options["enable_progressive_sparx_health"] == SparxUpgradeOptions.GREEN:
                max_health = 1
            max_health += state.count("Progressive Sparx Health Upgrade", self.player)
            return max_health >= health
            
        def set_indirect_rule(self, regionName, rule):
            region = self.multiworld.get_region(regionName, self.player)
            entrance = self.multiworld.get_entrance(regionName, self.player)
            set_rule(entrance, rule)
            self.multiworld.register_indirect_condition(region, entrance)

        for region in self.multiworld.get_regions(self.player):
            for location in region.locations:
                    set_rule(location, lambda state: True)
        if self.generation_options["goal"] == GoalOptions.SORCERESS_TWO:
            self.multiworld.completion_condition[self.player] = lambda state: state.has("Super Bonus Round Complete", self.player) and state.has("Egg", self.player, self.generation_options["egg_count"])
        elif self.generation_options["goal"] == GoalOptions.EGG_FOR_SALE:
            self.multiworld.completion_condition[self.player] = lambda state: state.has("Moneybags Chase Complete", self.player)
        elif self.generation_options["goal"] == GoalOptions.ALL_SKILLPOINTS:
            self.multiworld.completion_condition[self.player] = lambda state: state.has("Skill Point", self.player, 20)
        elif self.generation_options["goal"] == GoalOptions.EPILOGUE:
            self.multiworld.completion_condition[self.player] = lambda state: is_boss_defeated(self, "Sorceress", state) and state.has("Skill Point", self.player, 20)
        elif self.generation_options["goal"] == GoalOptions.SPIKE:
            self.multiworld.completion_condition[self.player] = lambda state: is_boss_defeated(self, "Spike", state) and state.has("Egg", self.player, self.generation_options["egg_count"])
        elif self.generation_options["goal"] == GoalOptions.SCORCH:
            self.multiworld.completion_condition[self.player] = lambda state: is_boss_defeated(self, "Scorch", state) and state.has("Egg", self.player, self.generation_options["egg_count"])
        elif self.generation_options["goal"] == GoalOptions.EGG_HUNT:
            self.multiworld.completion_condition[self.player] = lambda state: state.has("Egg", self.player, self.generation_options["egg_count"])
        else:
            self.multiworld.completion_condition[self.player] = lambda state: is_boss_defeated(self, "Sorceress", state) and state.has("Egg", self.player, self.generation_options["egg_count"])

        # After completing 3 levels in Evening Lake, the player is unable to complete any Hunter challenges until defeating Scorch.
        # To prevent the player from locking themselves out of progression, these must be logically locked behind Scorch.
        # Note: The egg "Sunrise Spring Home: Learn Gliding (Coltrane)" is not affected by this - Hunter remains in Sunrise Spring home.
        # Most, if not all gems, in skateboarding areas can be collected without the skateboard, but leave out of base logic.

        # Sunrise Spring Rules
        if self.generation_options["powerup_lock_settings"] == PowerupLockOptions.TYPE:
            set_rule(self.multiworld.get_location("Sunrise Spring Home: Fly through the cave. (Ami)", self.player),
                     lambda state: state.has("Superfly Powerup", self.player))
            if self.generation_options["enable_life_bottle_checks"] != LifeBottleOptions.OFF:
                set_rule(self.multiworld.get_location("Sunrise Spring: Life Bottle By Sheila's Alp", self.player),
                         lambda state: state.has("Superfly Powerup", self.player))
        elif self.generation_options["powerup_lock_settings"] == PowerupLockOptions.INDIVIDUAL:
            set_rule(self.multiworld.get_location("Sunrise Spring Home: Fly through the cave. (Ami)", self.player),
                     lambda state: state.has("Sunrise Superfly Powerup", self.player))
            if self.generation_options["enable_life_bottle_checks"] != LifeBottleOptions.OFF:
                set_rule(self.multiworld.get_location("Sunrise Spring: Life Bottle By Sheila's Alp", self.player),
                         lambda state: state.has("Sunrise Superfly Powerup", self.player))
        if Spyro3LocationCategory.GEMSANITY in self.enabled_location_categories:
            for i in range(142):
                if len(self.chosen_gem_locations) == 0 or f"Sunrise Spring: Gem {i + 1}" in self.chosen_gem_locations:
                    set_rule(
                        self.multiworld.get_location(f"Sunrise Spring: Gem {i + 1}", self.player),
                        lambda state: are_gems_accessible(self, state)
                    )


        # Sunny Villa Rules
        set_indirect_rule(
            self,
            "Sunny Villa",
            lambda state: can_enter_non_companion_portal(self, "Sunny Villa", state, True)
        )
        # Sheila's sub area may be entered early with a spin jump to the peak of the roof of the hut, or from behind.
        if not self.generation_options["logic_sunny_sheila_early"]:
            set_rule(self.multiworld.get_location("Sunny Villa: Hop to Rapunzel. (Lucy)", self.player), lambda state: is_level_completed(self,"Sheila's Alp", state))
        # Skateboarding challenges are not available while Hunter is captured.
        set_rule(self.multiworld.get_location("Sunny Villa: Lizard skating I. (Emily)", self.player), lambda state: is_boss_defeated(self, "Scorch", state) or is_glitched_logic(self, state))
        set_rule(self.multiworld.get_location("Sunny Villa: Lizard skating II. (Daisy)", self.player), lambda state: is_boss_defeated(self, "Scorch", state) or is_glitched_logic(self, state))
        if Spyro3LocationCategory.SKILLPOINT in self.enabled_location_categories:
            set_rule(self.multiworld.get_location("Sunny Villa: Skateboard course record I (Skill Point)", self.player), lambda state: is_boss_defeated(self, "Scorch", state) or is_glitched_logic(self, state))
        if Spyro3LocationCategory.SKILLPOINT_GOAL in self.enabled_location_categories:
            set_rule(self.multiworld.get_location("Sunny Villa: Skateboard course record I (Goal)", self.player), lambda state: is_boss_defeated(self, "Scorch", state) or is_glitched_logic(self, state))
        if Spyro3LocationCategory.GEMSANITY in self.enabled_location_categories:
            for i in range(198):
                if len(self.chosen_gem_locations) == 0 or f"Sunny Villa: Gem {i + 1}" in self.chosen_gem_locations:
                    set_rule(
                        self.multiworld.get_location(f"Sunny Villa: Gem {i + 1}", self.player),
                        lambda state: are_gems_accessible(self, state)
                    )
            # Bits of the gems, not accounting for empty bits
            sheila_gems = [105, 106, 107, 108, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124,
                           125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143,
                           144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 155, 156, 157, 158, 159, 160, 161]
            empty_bits = [13, 33, 34, 58, 109, 154, 172, 173, 174, 175, 193, 194, 195, 196, 197, 203, 205, 206, 213, 214,
                          216]
            if not self.generation_options["logic_sunny_sheila_early"]:
                for gem in sheila_gems:
                    skipped_bits = 0
                    for bit in empty_bits:
                        if bit < gem:
                            skipped_bits += 1
                        else:
                            break
                    if self.PRINT_GEM_REQS:
                        print(f"Sunny Villa: Gem {gem - skipped_bits} requires Sheila.")
                    if len(self.chosen_gem_locations) == 0 or f"Sunny Villa: Gem {gem - skipped_bits}" in self.chosen_gem_locations:
                        add_rule(
                            self.multiworld.get_location(f"Sunny Villa: Gem {gem - skipped_bits}", self.player),
                            lambda state: is_level_completed(self, "Sheila's Alp", state)
                        )

        # Cloud Spires Rules
        set_indirect_rule(
            self,
            "Cloud Spires",
            lambda state: can_enter_non_companion_portal(self, "Cloud Spires", state, True)
        )
        # Cloud Spires can be completed backwards, skipping Moneybags payment.
        # This requires one of two jumps to the end of the level, plus a jump from the egg "Cloud Spires: Glide to the island. (Clare)".
        if self.generation_options["moneybags_settings"] == MoneybagsOptions.MONEYBAGSSANITY and not self.generation_options["logic_cloud_backwards"]:
            if not self.generation_options["open_world"]:
                set_rule(self.multiworld.get_location("Cloud Spires: Turn on the cloud generator. (Henry)", self.player), lambda state: state.has("Moneybags Unlock - Cloud Spires Bellows", self.player))
            set_rule(self.multiworld.get_location("Cloud Spires: Plant the sun seeds. (LuLu)", self.player), lambda state: state.has("Moneybags Unlock - Cloud Spires Bellows", self.player))
            if self.generation_options["powerup_lock_settings"] == PowerupLockOptions.TYPE:
                set_rule(self.multiworld.get_location("Cloud Spires: Bell tower spirits. (Jake)", self.player),
                         lambda state: state.has("Moneybags Unlock - Cloud Spires Bellows", self.player) and state.has("Superfly Powerup", self.player))
            elif self.generation_options["powerup_lock_settings"] == PowerupLockOptions.INDIVIDUAL:
                set_rule(self.multiworld.get_location("Cloud Spires: Bell tower spirits. (Jake)", self.player),
                         lambda state: state.has("Moneybags Unlock - Cloud Spires Bellows", self.player) and state.has("Cloud Superfly Powerup", self.player))
            else:
                set_rule(self.multiworld.get_location("Cloud Spires: Bell tower spirits. (Jake)", self.player), lambda state: state.has("Moneybags Unlock - Cloud Spires Bellows", self.player))
            set_rule(self.multiworld.get_location("Cloud Spires: Bell tower thief. (Bryan)", self.player), lambda state: state.has("Moneybags Unlock - Cloud Spires Bellows", self.player))
            set_rule(self.multiworld.get_location("Cloud Spires: Glide to the island. (Clare)", self.player), lambda state: state.has("Moneybags Unlock - Cloud Spires Bellows", self.player))
            if not self.generation_options["open_world"]:
                set_rule(self.multiworld.get_location("Cloud Spires Complete", self.player), lambda state: state.has("Moneybags Unlock - Cloud Spires Bellows", self.player))
            if Spyro3LocationCategory.LIFE_BOTTLE in self.enabled_location_categories:
                set_rule(self.multiworld.get_location("Cloud Spires: Life Bottle Past Whirlwind", self.player), lambda state: state.has("Moneybags Unlock - Cloud Spires Bellows", self.player))
            if Spyro3LocationCategory.HINT in self.enabled_location_categories and "Cloud Spires: Glide Zoe" in self.enabled_hint_locations:
                set_rule(self.multiworld.get_location("Cloud Spires: Glide Zoe", self.player), lambda state: state.has("Moneybags Unlock - Cloud Spires Bellows", self.player))
        else:
            if self.generation_options["powerup_lock_settings"] == PowerupLockOptions.TYPE:
                set_rule(self.multiworld.get_location("Cloud Spires: Bell tower spirits. (Jake)", self.player),
                         lambda state: state.has("Superfly Powerup", self.player))
            elif self.generation_options["powerup_lock_settings"] == PowerupLockOptions.INDIVIDUAL:
                set_rule(self.multiworld.get_location("Cloud Spires: Bell tower spirits. (Jake)", self.player),
                         lambda state: state.has("Cloud Superfly Powerup", self.player))
        if Spyro3LocationCategory.GEMSANITY in self.enabled_location_categories:
            for i in range(148):
                if len(self.chosen_gem_locations) == 0 or f"Cloud Spires: Gem {i + 1}" in self.chosen_gem_locations:
                    set_rule(
                        self.multiworld.get_location(f"Cloud Spires: Gem {i + 1}", self.player),
                        lambda state: are_gems_accessible(self, state)
                    )
            # Bits of the gems, not accounting for empty bits
            moneybags_gems = [1, 3, 9, 10, 11, 12, 13, 14, 15, 16, 17, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 48, 49,
                              50, 51, 52, 53, 54, 59, 60, 61, 62, 74, 75, 76, 77, 79, 80, 82, 83, 85, 98, 99, 101, 107,
                              112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129,
                              130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 146, 147, 148,
                              149, 150, 151, 152]
            empty_bits = [2, 81, 92, 145]
            if self.generation_options["moneybags_settings"] == MoneybagsOptions.MONEYBAGSSANITY and not self.generation_options["logic_cloud_backwards"]:
                for gem in moneybags_gems:
                    skipped_bits = 0
                    for bit in empty_bits:
                        if bit < gem:
                            skipped_bits += 1
                        else:
                            break
                    if self.PRINT_GEM_REQS:
                        print(f"Cloud Spires: Gem {gem - skipped_bits} requires access beyond Moneybags.")
                    if len(self.chosen_gem_locations) == 0 or f"Cloud Spires: Gem {gem - skipped_bits}" in self.chosen_gem_locations:
                        add_rule(
                            self.multiworld.get_location(f"Cloud Spires: Gem {gem - skipped_bits}", self.player),
                            lambda state: state.has("Moneybags Unlock - Cloud Spires Bellows", self.player)
                        )


        # Molten Crater Rules
        # This requires either a swim in air or getting onto the wall by Molten Crater.
        set_indirect_rule(
            self,
            "Molten Crater",
            lambda state: can_enter_non_companion_portal(self, "Molten Crater", state, self.generation_options["logic_molten_early"])
        )
        # This is possible jumping on the posts of the nearby bridge, then onto the sub-area hut's roof.
        if not self.generation_options["logic_molten_byrd_early"]:
            set_rule(self.multiworld.get_location("Molten Crater: Replace idol heads. (Ryan)", self.player), lambda state: is_level_completed(self,"Sgt. Byrd's Base", state))
            set_rule(self.multiworld.get_location("Molten Crater: Sgt. Byrd blows up a wall. (Luna)", self.player), lambda state: is_level_completed(self,"Sgt. Byrd's Base", state))
            if Spyro3LocationCategory.SKILLPOINT in self.enabled_location_categories:
                set_rule(self.multiworld.get_location("Molten Crater: Assemble tiki heads (Skill Point)", self.player), lambda state: is_level_completed(self, "Sgt. Byrd's Base", state))
            if Spyro3LocationCategory.SKILLPOINT_GOAL in self.enabled_location_categories:
                set_rule(self.multiworld.get_location("Molten Crater: Assemble tiki heads (Goal)", self.player), lambda state: is_level_completed(self, "Sgt. Byrd's Base", state))
        if self.generation_options["moneybags_settings"] == MoneybagsOptions.MONEYBAGSSANITY and not self.generation_options["logic_molten_thieves_no_moneybags"]:
            set_rule(self.multiworld.get_location("Molten Crater: Catch the thief. (Moira)", self.player), lambda state: state.has("Moneybags Unlock - Molten Crater Thieves Door", self.player) or (self.generation_options["goal"] != GoalOptions.EGG_HUNT or self.generation_options["egg_count"] > self.generation_options["sorceress_door_requirement"]) and is_boss_defeated(self, "Sorceress", state))
            set_rule(self.multiworld.get_location("Molten Crater: Supercharge after the thief. (Kermitt)", self.player), lambda state: state.has("Moneybags Unlock - Molten Crater Thieves Door", self.player) or (self.generation_options["goal"] != GoalOptions.EGG_HUNT or self.generation_options["egg_count"] > self.generation_options["sorceress_door_requirement"]) and is_boss_defeated(self, "Sorceress", state))
            if Spyro3LocationCategory.SKILLPOINT in self.enabled_location_categories:
                set_rule(self.multiworld.get_location("Molten Crater: Supercharge the wall (Skill Point)", self.player), lambda state: state.has("Moneybags Unlock - Molten Crater Thieves Door", self.player) or (self.generation_options["goal"] != GoalOptions.EGG_HUNT or self.generation_options["egg_count"] > self.generation_options["sorceress_door_requirement"]) and is_boss_defeated(self, "Sorceress", state))
            if Spyro3LocationCategory.SKILLPOINT_GOAL in self.enabled_location_categories:
                set_rule(self.multiworld.get_location("Molten Crater: Supercharge the wall (Goal)", self.player), lambda state: state.has("Moneybags Unlock - Molten Crater Thieves Door", self.player) or (self.generation_options["goal"] != GoalOptions.EGG_HUNT or self.generation_options["egg_count"] > self.generation_options["sorceress_door_requirement"]) and is_boss_defeated(self, "Sorceress", state))
            if Spyro3LocationCategory.LIFE_BOTTLE in self.enabled_location_categories:
                set_rule(self.multiworld.get_location("Molten Crater: Life Bottle in Breakable Wall in Thief Area", self.player), lambda state: state.has("Moneybags Unlock - Molten Crater Thieves Door", self.player) or (self.generation_options["goal"] != GoalOptions.EGG_HUNT or self.generation_options["egg_count"] > self.generation_options["sorceress_door_requirement"]) and is_boss_defeated(self, "Sorceress", state))
        if Spyro3LocationCategory.GEMSANITY in self.enabled_location_categories:
            for i in range(147):
                if len(self.chosen_gem_locations) == 0 or f"Molten Crater: Gem {i + 1}" in self.chosen_gem_locations:
                    set_rule(
                        self.multiworld.get_location(f"Molten Crater: Gem {i + 1}", self.player),
                        lambda state: are_gems_accessible(self, state)
                    )
            # Bits of the gems, not accounting for empty bits
            moneybags_gems = [112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 125, 126, 127, 128, 129,
                              130, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 146, 147, 148,
                              149, 150, 151, 152, 153, 154, 155, 156, 157]
            byrd_gems = [80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101,
                         102, 103, 104, 106, 107, 108, 109, 110, 111]
            empty_bits = [5, 6, 29, 63, 64, 71, 105, 124, 131, 145]
            if self.generation_options["moneybags_settings"] == MoneybagsOptions.MONEYBAGSSANITY and not self.generation_options["logic_molten_thieves_no_moneybags"]:
                for gem in moneybags_gems:
                    skipped_bits = 0
                    for bit in empty_bits:
                        if bit < gem:
                            skipped_bits += 1
                        else:
                            break
                    if self.PRINT_GEM_REQS:
                        print(f"Molten Crater: Gem {gem - skipped_bits} requires access beyond Moneybags.")
                    if len(self.chosen_gem_locations) == 0 or f"Molten Crater: Gem {gem - skipped_bits}" in self.chosen_gem_locations:
                        add_rule(
                            self.multiworld.get_location(f"Molten Crater: Gem {gem - skipped_bits}", self.player),
                            lambda state: state.has("Moneybags Unlock - Molten Crater Thieves Door", self.player) or (self.generation_options["goal"] != GoalOptions.EGG_HUNT or self.generation_options["egg_count"] > self.generation_options["sorceress_door_requirement"]) and is_boss_defeated(self, "Sorceress", state)
                        )
            if not self.generation_options["logic_molten_byrd_early"]:
                for gem in byrd_gems:
                    skipped_bits = 0
                    for bit in empty_bits:
                        if bit < gem:
                            skipped_bits += 1
                        else:
                            break
                    if self.PRINT_GEM_REQS:
                        print(f"Molten Crater: Gem {gem - skipped_bits} requires Sgt. Byrd.")
                    if len(self.chosen_gem_locations) == 0 or f"Molten Crater: Gem {gem - skipped_bits}" in self.chosen_gem_locations:
                        add_rule(
                            self.multiworld.get_location(f"Molten Crater: Gem {gem - skipped_bits}", self.player),
                            lambda state: is_level_completed(self, "Sgt. Byrd's Base", state)
                        )


        # Seashell Shores Rules
        set_indirect_rule(
            self,
            "Seashell Shore",
            lambda state: can_enter_non_companion_portal(self, "Seashell Shore", state, self.generation_options["logic_seashell_early"])
        )
        if not self.generation_options["logic_seashell_sheila_early"]:
            set_rule(self.multiworld.get_location("Seashell Shore: Destroy the sand castle. (Mollie)", self.player), lambda state: is_level_completed(self, "Sheila's Alp", state))
            set_rule(self.multiworld.get_location("Seashell Shore: Hop to the secret cave. (Jared)", self.player), lambda state: is_level_completed(self, "Sheila's Alp", state))
        if Spyro3LocationCategory.GEMSANITY in self.enabled_location_categories:
            for i in range(169):
                if len(self.chosen_gem_locations) == 0 or f"Seashell Shore: Gem {i + 1}" in self.chosen_gem_locations:
                    set_rule(
                        self.multiworld.get_location(f"Seashell Shore: Gem {i + 1}", self.player),
                        lambda state: are_gems_accessible(self, state)
                    )
            # Bits of the gems, not accounting for empty bits
            sheila_gems = [136, 137, 139, 148, 153, 154, 155, 156, 157, 158, 160, 161, 162, 163, 169, 176, 177,
                           179, 184, 186, 187, 188, 190, 195, 197, 208]
            empty_bits = [33, 60, 97, 99, 100, 101, 102, 116, 121, 122, 134, 135, 138, 140, 141, 142, 143, 144,
                          145, 146, 147, 149, 150, 151, 152, 159, 164, 165, 166, 167, 168, 170, 171, 172, 173,
                          174, 175, 178, 180, 181, 182, 183, 185, 189, 191, 192, 193, 194, 196, 198, 199, 200,
                          201, 202, 203, 204, 205, 206, 207, 209, 210, 227]
            if not self.generation_options["logic_seashell_sheila_early"]:
                for gem in sheila_gems:
                    skipped_bits = 0
                    for bit in empty_bits:
                        if bit < gem:
                            skipped_bits += 1
                        else:
                            break
                    if self.PRINT_GEM_REQS:
                        print(f"Seashell Shore: Gem {gem - skipped_bits} requires Sheila.")
                    if len(self.chosen_gem_locations) == 0 or f"Seashell Shore: Gem {gem - skipped_bits}" in self.chosen_gem_locations:
                        add_rule(
                            self.multiworld.get_location(f"Seashell Shore: Gem {gem - skipped_bits}", self.player),
                            lambda state: is_level_completed(self, "Sheila's Alp", state)
                        )


        # Mushroom Speedway Rules
        set_indirect_rule(
            self,
            "Mushroom Speedway",
            lambda state: can_enter_non_companion_portal(self, "Mushroom Speedway", state, self.generation_options["logic_mushroom_early"])
        )
        # Hunter speedway challenges are not available while Hunter is captured.
        set_rule(self.multiworld.get_location("Mushroom Speedway: Hunter's dogfight. (Tater)", self.player), lambda state: is_boss_defeated(self, "Scorch", state) or is_glitched_logic(self, state))
        # Gemsanity checks in speedways are always accessible.


        # Sheila's Alp Rules
        # This requires a swim in air.
        if self.generation_options["moneybags_settings"] != MoneybagsOptions.VANILLA and not self.generation_options["logic_sheila_early"]:
            set_indirect_rule(self, "Sheila's Alp", lambda state: is_companion_unlocked(self, "Sheila", state))
        if Spyro3LocationCategory.GEMSANITY in self.enabled_location_categories:
            for i in range(117):
                if len(self.chosen_gem_locations) == 0 or f"Sheila's Alp: Gem {i + 1}" in self.chosen_gem_locations:
                    set_rule(
                        self.multiworld.get_location(f"Sheila's Alp: Gem {i + 1}", self.player),
                        lambda state: are_gems_accessible(self, state)
                    )


        # Buzz's Dungeon Rules
        set_indirect_rule(self, "Buzz", lambda state: is_level_completed(self,"Sunny Villa", state) and \
                is_level_completed(self,"Cloud Spires", state) and \
                is_level_completed(self,"Molten Crater", state) and \
                is_level_completed(self,"Seashell Shore", state) and \
                is_level_completed(self,"Sheila's Alp", state))

        # Crawdad Farm Rules
        if self.generation_options["enable_progressive_sparx_logic"]:
            set_indirect_rule(self, "Crawdad Farm", lambda state: is_boss_defeated(self, "Buzz", state) and (has_sparx_health(self, 1, state) or is_glitched_logic(self, state)))
        else:
            set_indirect_rule(self, "Crawdad Farm", lambda state: is_boss_defeated(self, "Buzz", state))
        # Gemsanity checks in Sparx levels are always accessible.


        # Midday Gardens Rules
        if self.generation_options["enable_world_keys"]:
            set_indirect_rule(self, "Midday Gardens", lambda state: is_boss_defeated(self, "Buzz", state) and has_world_keys(self, 1, state))
        else:
            set_indirect_rule(self, "Midday Gardens", lambda state: is_boss_defeated(self, "Buzz", state))
        if self.generation_options["powerup_lock_settings"] == PowerupLockOptions.TYPE:
            set_rule(self.multiworld.get_location("Midday Gardens Home: Superflame the flowerpots. (Matt)", self.player),
                     lambda state: state.has("Fireball Powerup", self.player))
        elif self.generation_options["powerup_lock_settings"] == PowerupLockOptions.INDIVIDUAL:
            set_rule(self.multiworld.get_location("Midday Gardens Home: Superflame the flowerpots. (Matt)", self.player),
                     lambda state: state.has("Midday Fireball Powerup", self.player))
        if Spyro3LocationCategory.GEMSANITY in self.enabled_location_categories:
            for i in range(123):
                if len(self.chosen_gem_locations) == 0 or f"Midday Gardens: Gem {i + 1}" in self.chosen_gem_locations:
                    set_rule(
                        self.multiworld.get_location(f"Midday Gardens: Gem {i + 1}", self.player),
                        lambda state: are_gems_accessible(self, state)
                    )
            # Bits of the gems, not accounting for empty bits
            fireball_gems = [106, 123, 124, 125, 127, 128]
            empty_bits = [72, 89, 90, 109, 126]
            if self.generation_options["powerup_lock_settings"] != PowerupLockOptions.VANILLA:
                for gem in fireball_gems:
                    skipped_bits = 0
                    for bit in empty_bits:
                        if bit < gem:
                            skipped_bits += 1
                        else:
                            break
                    if self.PRINT_GEM_REQS:
                        print(f"Midday Gardens: Gem {gem - skipped_bits} requires the Fireball powerup.")
                    if len(self.chosen_gem_locations) == 0 or f"Midday Gardens: Gem {gem - skipped_bits}" in self.chosen_gem_locations:
                        if self.generation_options["powerup_lock_settings"] == PowerupLockOptions.TYPE:
                            add_rule(
                                self.multiworld.get_location(f"Midday Gardens: Gem {gem - skipped_bits}", self.player),
                                lambda state: state.has("Fireball Powerup", self.player)
                            )
                        elif self.generation_options["powerup_lock_settings"] == PowerupLockOptions.INDIVIDUAL:
                            add_rule(
                                self.multiworld.get_location(f"Midday Gardens: Gem {gem - skipped_bits}", self.player),
                                lambda state: state.has("Midday Fireball Powerup", self.player)
                            )


        # Icy Peak Rules
        if self.generation_options["enable_progressive_sparx_logic"]:
            set_indirect_rule(
                self,
                "Icy Peak",
                lambda state: (has_sparx_health(self, 1, state) or is_glitched_logic(self, state)) and can_enter_non_companion_portal(self, "Icy Peak", state, True)
            )
        else:
            set_indirect_rule(
                self,
                "Icy Peak",
                lambda state: can_enter_non_companion_portal(self, "Icy Peak", state, True)
            )
        # This can be entered without paying Moneybags, but shooting the crystal you need to jump on with the cannon renders the skip impossible.
        if self.generation_options["moneybags_settings"] == MoneybagsOptions.MONEYBAGSSANITY:
            # No gems in Nancy area.
            set_rule(self.multiworld.get_location("Icy Peak: Protect Nancy the skater. (Cerny)", self.player), lambda state: state.has("Moneybags Unlock - Icy Peak Nancy Door", self.player) or (self.generation_options["goal"] != GoalOptions.EGG_HUNT or self.generation_options["egg_count"] > self.generation_options["sorceress_door_requirement"]) and is_boss_defeated(self, "Sorceress", state))
        if Spyro3LocationCategory.GEMSANITY in self.enabled_location_categories:
            for i in range(175):
                if len(self.chosen_gem_locations) == 0 or f"Icy Peak: Gem {i + 1}" in self.chosen_gem_locations:
                    set_rule(
                        self.multiworld.get_location(f"Icy Peak: Gem {i + 1}", self.player),
                        lambda state: are_gems_accessible(self, state)
                    )


        # Enchanted Towers Rules
        if self.generation_options["enable_progressive_sparx_logic"]:
            set_indirect_rule(
                self,
                "Enchanted Towers",
                lambda state: (has_sparx_health(self, 1, state) or is_glitched_logic(self, state)) and can_enter_non_companion_portal(self, "Enchanted Towers", state, True)
            )
        else:
            set_indirect_rule(
                self,
                "Enchanted Towers",
                lambda state: can_enter_non_companion_portal(self, "Enchanted Towers", state, True)
            )
        set_rule(self.multiworld.get_location("Enchanted Towers: Collect the bones. (Ralph)", self.player), lambda state: is_level_completed(self,"Sgt. Byrd's Base", state))
        # Skateboarding challenges are not available while Hunter is captured.
        set_rule(self.multiworld.get_location("Enchanted Towers: Trick skater I. (Caroline)", self.player), lambda state: is_boss_defeated(self, "Scorch", state) or is_glitched_logic(self, state))
        set_rule(self.multiworld.get_location("Enchanted Towers: Trick skater II. (Alex)", self.player), lambda state: is_boss_defeated(self, "Scorch", state) or is_glitched_logic(self, state))
        if Spyro3LocationCategory.SKILLPOINT in self.enabled_location_categories:
            set_rule(self.multiworld.get_location("Enchanted Towers: Skateboard course record II (Skill Point)", self.player), lambda state: is_boss_defeated(self, "Scorch", state) or is_glitched_logic(self, state))
        if Spyro3LocationCategory.SKILLPOINT_GOAL in self.enabled_location_categories:
            set_rule(self.multiworld.get_location("Enchanted Towers: Skateboard course record II (Goal)", self.player), lambda state: is_boss_defeated(self, "Scorch", state) or is_glitched_logic(self, state))
        # Note: The life bottle does not require Sgt. Byrd.
        if Spyro3LocationCategory.GEMSANITY in self.enabled_location_categories:
            for i in range(174):
                if len(self.chosen_gem_locations) == 0 or f"Enchanted Towers: Gem {i + 1}" in self.chosen_gem_locations:
                    set_rule(
                        self.multiworld.get_location(f"Enchanted Towers: Gem {i + 1}", self.player),
                        lambda state: are_gems_accessible(self, state)
                    )
            # Bits of the gems, not accounting for empty bits
            byrd_gems = [40, 41, 42, 43, 45, 46, 47, 73, 75, 77, 109, 110, 111, 112, 113, 116, 117, 118, 119]
            empty_bits = [51, 52, 53, 54, 55, 56, 57, 84, 87, 88, 89, 90, 91, 92, 93, 108, 147, 172]
            for gem in byrd_gems:
                skipped_bits = 0
                for bit in empty_bits:
                    if bit < gem:
                        skipped_bits += 1
                    else:
                        break
                if self.PRINT_GEM_REQS:
                    print(f"Enchanted Towers: Gem {gem - skipped_bits} requires Sgt. Byrd.")
                if len(self.chosen_gem_locations) == 0 or f"Enchanted Towers: Gem {gem - skipped_bits}" in self.chosen_gem_locations:
                    add_rule(
                        self.multiworld.get_location(f"Enchanted Towers: Gem {gem - skipped_bits}", self.player),
                        lambda state: is_level_completed(self, "Sgt. Byrd's Base", state)
                    )


        # Spooky Swamp Rules
        if self.generation_options["enable_progressive_sparx_logic"]:
            set_indirect_rule(
                self,
                "Spooky Swamp",
                lambda state: (has_sparx_health(self, 1, state) or is_glitched_logic(self, state)) and can_enter_non_companion_portal(self, "Spooky Swamp", state, self.generation_options["logic_spooky_early"])
            )
        else:
            set_indirect_rule(
                self,
                "Spooky Swamp",
                lambda state: can_enter_non_companion_portal(self, "Spooky Swamp", state, self.generation_options["logic_spooky_early"])
            )
        # Can skip Moneybags by damage boosting from the island egg to the end of level.
        if self.generation_options["open_world"] or self.generation_options["moneybags_settings"] != MoneybagsOptions.MONEYBAGSSANITY or self.generation_options["logic_spooky_no_moneybags"]:
            # Technically possible without Sheila completion with a glide out of bounds, but there's no reason to add an option for this at this time.
            set_rule(self.multiworld.get_location("Spooky Swamp: Escort the twins I. (Peggy)", self.player), lambda state: is_level_completed(self,"Sheila's Alp", state))
            set_rule(self.multiworld.get_location("Spooky Swamp: Escort the twins II. (Michele)", self.player), lambda state: is_level_completed(self,"Sheila's Alp", state) and state.can_reach_location("Spooky Swamp: Escort the twins I. (Peggy)", self.player))
        else:
            set_rule(self.multiworld.get_location("Spooky Swamp: Escort the twins I. (Peggy)", self.player), lambda state: is_level_completed(self, "Sheila's Alp", state) and state.has("Moneybags Unlock - Spooky Swamp Door", self.player))
            set_rule(self.multiworld.get_location("Spooky Swamp: Escort the twins II. (Michele)", self.player), lambda state: is_level_completed(self, "Sheila's Alp", state) and state.can_reach_location("Spooky Swamp: Escort the twins I. (Peggy)", self.player) and state.has("Moneybags Unlock - Spooky Swamp Door", self.player))
            set_rule(self.multiworld.get_location("Spooky Swamp: Defeat sleepy head. (Herbi)", self.player), lambda state: state.has("Moneybags Unlock - Spooky Swamp Door", self.player))
            # This one is doable with a tricky jump from the tea lamp nearest it, but it's easier to just skip Moneybags.
            set_rule(self.multiworld.get_location("Spooky Swamp: Across the treetops. (Frank)", self.player), lambda state: state.has("Moneybags Unlock - Spooky Swamp Door", self.player))
            if not self.generation_options["open_world"]:
                set_rule(self.multiworld.get_location("Spooky Swamp: Find Shiny the firefly. (Thelonious)", self.player), lambda state: state.has("Moneybags Unlock - Spooky Swamp Door", self.player))
                set_rule(self.multiworld.get_location("Spooky Swamp Complete", self.player), lambda state: state.has("Moneybags Unlock - Spooky Swamp Door", self.player))
            if Spyro3LocationCategory.SKILLPOINT in self.enabled_location_categories:
                set_rule(self.multiworld.get_location("Spooky Swamp: Destroy all piranha signs (Skill Point)", self.player), lambda state: state.has("Moneybags Unlock - Spooky Swamp Door", self.player))
            if Spyro3LocationCategory.SKILLPOINT_GOAL in self.enabled_location_categories:
                set_rule(self.multiworld.get_location("Spooky Swamp: Destroy all piranha signs (Goal)", self.player), lambda state: state.has("Moneybags Unlock - Spooky Swamp Door", self.player))
        if Spyro3LocationCategory.GEMSANITY in self.enabled_location_categories:
            for i in range(151):
                if len(self.chosen_gem_locations) == 0 or f"Spooky Swamp: Gem {i + 1}" in self.chosen_gem_locations:
                    set_rule(
                        self.multiworld.get_location(f"Spooky Swamp: Gem {i + 1}", self.player),
                        lambda state: are_gems_accessible(self, state)
                    )
            # Bits of the gems, not accounting for empty bits
            moneybags_gems = [19, 20, 21, 22, 25, 26, 27, 37, 38, 45, 48, 49, 50, 51, 53, 56, 57, 58, 60, 61, 62, 85,
                              86, 87, 88, 89, 105, 106, 107, 108, 109, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120,
                              121, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139,
                              140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157,
                              158, 159, 160]
            empty_bits = [5, 18, 54, 59, 76, 80, 104, 110, 122]
            if not self.generation_options["open_world"] and self.generation_options["moneybags_settings"] == MoneybagsOptions.MONEYBAGSSANITY and not self.generation_options["logic_spooky_no_moneybags"]:
                for gem in moneybags_gems:
                    skipped_bits = 0
                    for bit in empty_bits:
                        if bit < gem:
                            skipped_bits += 1
                        else:
                            break
                    if self.PRINT_GEM_REQS:
                        print(f"Spooky Swamp: Gem {gem - skipped_bits} requires access past Moneybags.")
                    if len(self.chosen_gem_locations) == 0 or f"Spooky Swamp: Gem {gem - skipped_bits}" in self.chosen_gem_locations:
                        add_rule(
                            self.multiworld.get_location(f"Spooky Swamp: Gem {gem - skipped_bits}", self.player),
                            lambda state: state.has("Moneybags Unlock - Spooky Swamp Door", self.player)
                        )


        # Bamboo Terrace Rules
        if self.generation_options["enable_progressive_sparx_logic"]:
            set_indirect_rule(
                self,
                "Bamboo Terrace",
                lambda state: (has_sparx_health(self, 1, state) or is_glitched_logic(self, state)) and can_enter_non_companion_portal(self, "Bamboo Terrace", state, self.generation_options["logic_bamboo_early"])
            )
        else:
            set_indirect_rule(
                self,
                "Bamboo Terrace",
                lambda state: can_enter_non_companion_portal(self, "Bamboo Terrace", state, self.generation_options["logic_bamboo_early"])
            )
        # This requires a swim in air.
        if not self.generation_options["logic_bamboo_bentley_early"]:
            set_rule(self.multiworld.get_location("Bamboo Terrace: Smash to the mountain top. (Brubeck)", self.player), lambda state: is_level_completed(self,"Bentley's Outpost", state))
            if Spyro3LocationCategory.LIFE_BOTTLE in self.enabled_location_categories:
                set_rule(self.multiworld.get_location("Bamboo Terrace: Life Bottle in Bentley Sub-Area", self.player), lambda state: is_level_completed(self, "Bentley's Outpost", state))
        if self.generation_options["powerup_lock_settings"] == PowerupLockOptions.TYPE:
            set_rule(self.multiworld.get_location("Bamboo Terrace: Shoot from the boat. (Rusty)", self.player),
                     lambda state: state.has("Fireball Powerup", self.player))
        elif self.generation_options["powerup_lock_settings"] == PowerupLockOptions.INDIVIDUAL:
            set_rule(self.multiworld.get_location("Bamboo Terrace: Shoot from the boat. (Rusty)", self.player),
                     lambda state: state.has("Bamboo Fireball Powerup", self.player))
        if Spyro3LocationCategory.GEMSANITY in self.enabled_location_categories:
            for i in range(159):
                if len(self.chosen_gem_locations) == 0 or f"Bamboo Terrace: Gem {i + 1}" in self.chosen_gem_locations:
                    set_rule(
                        self.multiworld.get_location(f"Bamboo Terrace: Gem {i + 1}", self.player),
                        lambda state: are_gems_accessible(self, state)
                    )
            # Bits of the gems, not accounting for empty bits
            bentley_gems = [116, 117, 118, 119, 120, 121, 122, 123, 124, 127, 128, 129, 130, 131, 132, 133, 134, 135,
                            136, 137, 138, 139, 140, 141, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154,
                            155, 156, 157, 158, 162, 164, 165, 166, 169, 170, 173, 174, 177, 184, 189, 191]
            empty_bits = [53, 54, 55, 56, 77, 95, 96, 115, 125, 126, 142, 159, 160, 161, 163, 167, 168, 171, 172, 175,
                          176, 178, 179, 180, 181, 182, 183, 185, 186, 187, 188, 190]
            if not self.generation_options["logic_bamboo_bentley_early"]:
                for gem in bentley_gems:
                    skipped_bits = 0
                    for bit in empty_bits:
                        if bit < gem:
                            skipped_bits += 1
                        else:
                            break
                    if self.PRINT_GEM_REQS:
                        print(f"Bamboo Terrace: Gem {gem - skipped_bits} requires Bentley.")
                    if len(self.chosen_gem_locations) == 0 or f"Bamboo Terrace: Gem {gem - skipped_bits}" in self.chosen_gem_locations:
                        add_rule(
                            self.multiworld.get_location(f"Bamboo Terrace: Gem {gem - skipped_bits}", self.player),
                            lambda state: is_level_completed(self, "Bentley's Outpost", state)
                        )


        # Country Speedway Rules
        set_indirect_rule(
            self,
            "Country Speedway",
            lambda state: can_enter_non_companion_portal(self, "Country Speedway", state, self.generation_options["logic_country_early"])
        )
        # Hunter speedway challenges are not available while Hunter is captured.
        set_rule(self.multiworld.get_location("Country Speedway: Hunter's rescue mission. (Roberto)", self.player), lambda state: is_boss_defeated(self, "Scorch", state) or is_glitched_logic(self, state))
        # Speedway gems are always in logic during gemsanity.


        # Sgt. Byrd's Base Rules
        # This requires a swim in air or a glide out of bounds.
        if self.generation_options["enable_progressive_sparx_logic"] and self.generation_options["moneybags_settings"] != MoneybagsOptions.VANILLA and not self.generation_options["logic_byrd_early"]:
            set_indirect_rule(self, "Sgt. Byrd's Base", lambda state: (has_sparx_health(self, 1, state) or is_glitched_logic(self, state)) and is_companion_unlocked(self, "Sgt. Byrd", state))
        elif self.generation_options["moneybags_settings"] != MoneybagsOptions.VANILLA and not self.generation_options["logic_byrd_early"]:
            set_indirect_rule(self, "Sgt. Byrd's Base", lambda state: is_companion_unlocked(self, "Sgt. Byrd", state))
        elif self.generation_options["enable_progressive_sparx_logic"]:
            set_indirect_rule(self, "Sgt. Byrd's Base", lambda state: (has_sparx_health(self, 1, state) or is_glitched_logic(self, state)))
        if Spyro3LocationCategory.GEMSANITY in self.enabled_location_categories:
            for i in range(117):
                if len(self.chosen_gem_locations) == 0 or f"Sgt. Byrd's Base: Gem {i + 1}" in self.chosen_gem_locations:
                    set_rule(
                        self.multiworld.get_location(f"Sgt. Byrd's Base: Gem {i + 1}", self.player),
                        lambda state: are_gems_accessible(self, state)
                    )


        # Spike's Arena Rules
        if self.generation_options["enable_progressive_sparx_logic"]:
            set_indirect_rule(self, "Spike", lambda state: is_level_completed(self, "Icy Peak", state) and \
                    is_level_completed(self, "Enchanted Towers", state) and \
                    is_level_completed(self, "Spooky Swamp", state) and \
                    is_level_completed(self, "Bamboo Terrace", state) and \
                    is_level_completed(self, "Sgt. Byrd's Base", state) and \
                    (has_sparx_health(self, 1, state) or is_glitched_logic(self, state)))
        else:
            set_indirect_rule(self, "Spike", lambda state: is_level_completed(self,"Icy Peak", state) and \
                    is_level_completed(self,"Enchanted Towers", state) and \
                    is_level_completed(self,"Spooky Swamp", state) and \
                    is_level_completed(self,"Bamboo Terrace", state) and \
                    is_level_completed(self,"Sgt. Byrd's Base", state))


        # Spider Town Rules
        if self.generation_options["enable_progressive_sparx_logic"]:
            set_indirect_rule(self, "Spider Town", lambda state: is_boss_defeated(self, "Spike", state) and \
                    is_level_completed(self, 'Crawdad Farm', state) and \
                    (has_sparx_health(self, 1, state) or is_glitched_logic(self, state))
            )
        else:
            set_indirect_rule(self, "Spider Town", lambda state: is_boss_defeated(self,"Spike", state) and is_level_completed(self, 'Crawdad Farm', state))
        # Sparx level gems are always accessible in gemsanity.


        # Evening Lake Rules
        if self.generation_options["enable_world_keys"]:
            set_indirect_rule(self, "Evening Lake", lambda state: is_boss_defeated(self, "Spike", state) and has_world_keys(self, 2, state))
        else:
            set_indirect_rule(self, "Evening Lake", lambda state: is_boss_defeated(self, "Spike", state))
        if self.generation_options["powerup_lock_settings"] == PowerupLockOptions.TYPE:
            set_rule(self.multiworld.get_location("Evening Lake Home: I'm invincible! (Stuart)", self.player),
                     lambda state: state.has("Invincibility Powerup", self.player))
            set_rule(self.multiworld.get_location("Evening Lake Home: On the bridge (Ted)", self.player),
                lambda state: state.has("Invincibility Powerup", self.player))
            if self.generation_options["enable_life_bottle_checks"] != LifeBottleOptions.OFF:
                set_rule(self.multiworld.get_location("Evening Lake: Life Bottle on Upper Path", self.player),
                         lambda state: state.has("Invincibility Powerup", self.player))
        elif self.generation_options["powerup_lock_settings"] == PowerupLockOptions.INDIVIDUAL:
            set_rule(self.multiworld.get_location("Evening Lake Home: I'm invincible! (Stuart)", self.player),
                     lambda state: state.has("Evening Invincibility Powerup", self.player))
            set_rule(self.multiworld.get_location("Evening Lake Home: On the bridge (Ted)", self.player),
                lambda state: state.has("Evening Invincibility Powerup", self.player))
            if self.generation_options["enable_life_bottle_checks"] != LifeBottleOptions.OFF:
                set_rule(self.multiworld.get_location("Evening Lake: Life Bottle on Upper Path", self.player),
                         lambda state: state.has("Evening Invincibility Powerup", self.player))
        if Spyro3LocationCategory.GEMSANITY in self.enabled_location_categories:
            for i in range(75):
                if len(self.chosen_gem_locations) == 0 or f"Evening Lake: Gem {i + 1}" in self.chosen_gem_locations:
                    set_rule(
                        self.multiworld.get_location(f"Evening Lake: Gem {i + 1}", self.player),
                        lambda state: are_gems_accessible(self, state)
                    )
            # Bits of the gems, not accounting for empty bits
            invincibility_gems = [32, 33, 34, 35, 36, 51, 67, 68, 69, 70, 71, 72, 73, 77, 80]
            empty_bits = [31, 37, 60, 61, 66]
            if self.generation_options["powerup_lock_settings"] != PowerupLockOptions.VANILLA:
                for gem in invincibility_gems:
                    skipped_bits = 0
                    for bit in empty_bits:
                        if bit < gem:
                            skipped_bits += 1
                        else:
                            break
                    if self.PRINT_GEM_REQS:
                        print(f"Evening Lake: Gem {gem - skipped_bits} requires the Invincibility powerup.")
                    if len(self.chosen_gem_locations) == 0 or f"Evening Lake: Gem {gem - skipped_bits}" in self.chosen_gem_locations:
                        if self.generation_options["powerup_lock_settings"] == PowerupLockOptions.TYPE:
                            add_rule(
                                self.multiworld.get_location(f"Evening Lake: Gem {gem - skipped_bits}", self.player),
                                lambda state: state.has("Invincibility Powerup", self.player)
                            )
                        elif self.generation_options["powerup_lock_settings"] == PowerupLockOptions.INDIVIDUAL:
                            add_rule(
                                self.multiworld.get_location(f"Evening Lake: Gem {gem - skipped_bits}", self.player),
                                lambda state: state.has("Evening Invincibility Powerup", self.player)
                            )


        # Frozen Altars Rules
        if self.generation_options["enable_progressive_sparx_logic"]:
            set_indirect_rule(
                self,
                "Frozen Altars",
                lambda state: (has_sparx_health(self, 1, state) or is_glitched_logic(self, state)) and can_enter_non_companion_portal(self, "Frozen Altars", state, True)
            )
        else:
            set_indirect_rule(
                self,
                "Frozen Altars",
                lambda state: can_enter_non_companion_portal(self, "Frozen Altars", state, True)
            )
        # Requires a proxy or getting onto the nearby wall and gliding out of bounds
        if not self.generation_options["logic_frozen_bentley_early"]:
            # 0 gems in Bentley subarea.
            set_rule(self.multiworld.get_location("Frozen Altars: Box the yeti. (Aly)", self.player), lambda state: is_level_completed(self,"Bentley's Outpost", state))
            set_rule(self.multiworld.get_location("Frozen Altars: Box the yeti again! (Ricco)", self.player), lambda state: is_level_completed(self,"Bentley's Outpost", state) and state.can_reach_location("Frozen Altars: Box the yeti. (Aly)", self.player))
            if Spyro3LocationCategory.SKILLPOINT in self.enabled_location_categories:
                set_rule(self.multiworld.get_location("Frozen Altars: Beat yeti in two rounds (Skill Point)", self.player), lambda state: is_level_completed(self, "Bentley's Outpost", state) and state.can_reach_location("Frozen Altars: Box the yeti. (Aly)", self.player))
            if Spyro3LocationCategory.SKILLPOINT_GOAL in self.enabled_location_categories:
                set_rule(self.multiworld.get_location("Frozen Altars: Beat yeti in two rounds (Goal)", self.player), lambda state: is_level_completed(self, "Bentley's Outpost", state) and state.can_reach_location("Frozen Altars: Box the yeti. (Aly)", self.player))
        # Requires a proxy.
        if self.generation_options["moneybags_settings"] == MoneybagsOptions.MONEYBAGSSANITY and not self.generation_options["logic_frozen_cat_hockey_no_moneybags"]:
            # 0 gems in cat hockey subarea.
            set_rule(self.multiworld.get_location("Frozen Altars: Catch the ice cats. (Ba'ah)", self.player), lambda state: state.has("Moneybags Unlock - Frozen Altars Cat Hockey Door", self.player) or (self.generation_options["goal"] != GoalOptions.EGG_HUNT or self.generation_options["egg_count"] > self.generation_options["sorceress_door_requirement"]) and is_boss_defeated(self, "Sorceress", state))
        if Spyro3LocationCategory.GEMSANITY in self.enabled_location_categories:
            for i in range(129):
                if len(self.chosen_gem_locations) == 0 or f"Frozen Altars: Gem {i + 1}" in self.chosen_gem_locations:
                    set_rule(
                        self.multiworld.get_location(f"Frozen Altars: Gem {i + 1}", self.player),
                        lambda state: are_gems_accessible(self, state)
                    )


        # Lost Fleet Rules
        if self.generation_options["enable_progressive_sparx_logic"]:
            set_indirect_rule(
                self,
                "Lost Fleet",
                lambda state: (has_sparx_health(self, 1, state) or is_glitched_logic(self, state)) and can_enter_non_companion_portal(self, "Lost Fleet", state, True)
            )
        else:
            set_indirect_rule(
                self,
                "Lost Fleet",
                lambda state: can_enter_non_companion_portal(self, "Lost Fleet", state, True)
            )
        # Skateboarding challenges are not available while Hunter is captured.
        set_rule(self.multiworld.get_location("Lost Fleet: Skate race the rhynocs. (Oliver)", self.player), lambda state: is_boss_defeated(self, "Scorch", state) or is_glitched_logic(self, state))
        set_rule(self.multiworld.get_location("Lost Fleet: Skate race Hunter. (Aiden)", self.player), lambda state: is_boss_defeated(self, "Scorch", state) or is_glitched_logic(self, state))
        if Spyro3LocationCategory.SKILLPOINT in self.enabled_location_categories:
            set_rule(self.multiworld.get_location("Lost Fleet: Skateboard record time (Skill Point)", self.player), lambda state: is_boss_defeated(self, "Scorch", state) or is_glitched_logic(self, state))
        if Spyro3LocationCategory.SKILLPOINT_GOAL in self.enabled_location_categories:
            set_rule(self.multiworld.get_location("Lost Fleet: Skateboard record time (Goal)", self.player), lambda state: is_boss_defeated(self, "Scorch", state) or is_glitched_logic(self, state))
        if Spyro3LocationCategory.LIFE_BOTTLE in self.enabled_location_categories:
            set_rule(self.multiworld.get_location("Lost Fleet: Life Bottle in Skateboarding Sub-Area", self.player), lambda state: is_boss_defeated(self, "Scorch", state) or is_glitched_logic(self, state))
        if self.generation_options["powerup_lock_settings"] == PowerupLockOptions.TYPE:
            set_rule(self.multiworld.get_location("Lost Fleet: Swim through acid. (Chad)", self.player),
                     lambda state: state.has("Invincibility Powerup", self.player))
            if self.generation_options["enable_life_bottle_checks"] != LifeBottleOptions.OFF:
                set_rule(self.multiworld.get_location("Lost Fleet: Life Bottle in Acid River", self.player),
                         lambda state: state.has("Invincibility Powerup", self.player))
        elif self.generation_options["powerup_lock_settings"] == PowerupLockOptions.INDIVIDUAL:
            set_rule(self.multiworld.get_location("Lost Fleet: Swim through acid. (Chad)", self.player),
                     lambda state: state.has("Fleet Invincibility Powerup", self.player))
            if self.generation_options["enable_life_bottle_checks"] != LifeBottleOptions.OFF:
                set_rule(self.multiworld.get_location("Lost Fleet: Life Bottle in Acid River", self.player),
                         lambda state: state.has("Fleet Invincibility Powerup", self.player))
        if Spyro3LocationCategory.GEMSANITY in self.enabled_location_categories:
            for i in range(151):
                if len(self.chosen_gem_locations) == 0 or f"Lost Fleet: Gem {i + 1}" in self.chosen_gem_locations:
                    set_rule(
                        self.multiworld.get_location(f"Lost Fleet: Gem {i + 1}", self.player),
                        lambda state: are_gems_accessible(self, state)
                    )
            # Bits of the gems, not accounting for empty bits
            hunter_gems = [197, 198, 199, 200, 201, 202, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214,
                           215, 216, 217, 218, 219, 220, 222, 223, 224, 225, 228, 229, 230, 236, 237, 238]
            invincibility_gems = [23, 24, 25, 42, 43, 44, 45, 56, 66, 67, 68, 70, 73, 74, 120, 121, 122, 123, 124,
                                  125, 126, 127, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159,
                                  160, 161, 162, 163, 164, 168, 170, 171, 172, 173, 174, 175, 176, 177, 178,
                                  179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195,
                                  196]
            empty_bits = [41, 50, 52, 69, 78, 93, 165, 166, 167, 169, 221, 227, 231, 232, 233, 235]
            for gem in hunter_gems:
                skipped_bits = 0
                for bit in empty_bits:
                    if bit < gem:
                        skipped_bits += 1
                    else:
                        break
                if self.PRINT_GEM_REQS:
                    print(f"Lost Fleet: Gem {gem - skipped_bits} requires Hunter access (Scorch defeated).")
                if len(self.chosen_gem_locations) == 0 or f"Lost Fleet: Gem {gem - skipped_bits}" in self.chosen_gem_locations:
                    add_rule(
                        self.multiworld.get_location(f"Lost Fleet: Gem {gem - skipped_bits}", self.player),
                        lambda state: is_boss_defeated(self, "Scorch", state) or is_glitched_logic(self, state)
                    )
            for gem in invincibility_gems:
                skipped_bits = 0
                for bit in empty_bits:
                    if bit < gem:
                        skipped_bits += 1
                    else:
                        break
                if self.PRINT_GEM_REQS:
                    print(f"Lost Fleet: Gem {gem - skipped_bits} requires the Invincibility powerup.")
                if len(self.chosen_gem_locations) == 0 or f"Lost Fleet: Gem {gem - skipped_bits}" in self.chosen_gem_locations:
                    if self.generation_options["powerup_lock_settings"] == PowerupLockOptions.TYPE:
                        add_rule(
                            self.multiworld.get_location(f"Lost Fleet: Gem {gem - skipped_bits}", self.player),
                            lambda state: state.has("Invincibility Powerup", self.player)
                        )
                    elif self.generation_options["powerup_lock_settings"] == PowerupLockOptions.INDIVIDUAL:
                        add_rule(
                            self.multiworld.get_location(f"Lost Fleet: Gem {gem - skipped_bits}", self.player),
                            lambda state: state.has("Fleet Invincibility Powerup", self.player)
                        )


        # Fireworks Factory Rules
        if self.generation_options["enable_progressive_sparx_logic"]:
            set_indirect_rule(
                self,
                "Fireworks Factory",
                lambda state: (has_sparx_health(self, 2, state) or is_glitched_logic(self, state)) and can_enter_non_companion_portal(self, "Fireworks Factory", state, self.generation_options["logic_fireworks_early"])
            )
        else:
            set_indirect_rule(
                self,
                "Fireworks Factory",
                lambda state: can_enter_non_companion_portal(self, "Fireworks Factory", state, self.generation_options["logic_fireworks_early"])
            )
        # This requires a careful glide to the right "antenna" of the subarea hut.
        if not self.generation_options["logic_fireworks_agent_9_early"]:
            set_rule(self.multiworld.get_location("Fireworks Factory: You're doomed! (Patty)", self.player), lambda state: is_level_completed(self,"Agent 9's Lab", state))
            set_rule(self.multiworld.get_location("Fireworks Factory: You're still doomed! (Donovan)", self.player), lambda state: is_level_completed(self,"Agent 9's Lab", state) and state.can_reach_location("Fireworks Factory: You're doomed! (Patty)", self.player))
            if Spyro3LocationCategory.SKILLPOINT in self.enabled_location_categories:
                set_rule(self.multiworld.get_location("Fireworks Factory: Find Agent 9's powerup (Skill Point)", self.player), lambda state: is_level_completed(self, "Agent 9's Lab", state))
            if Spyro3LocationCategory.SKILLPOINT_GOAL in self.enabled_location_categories:
                set_rule(self.multiworld.get_location("Fireworks Factory: Find Agent 9's powerup (Goal)", self.player), lambda state: is_level_completed(self, "Agent 9's Lab", state))
            if Spyro3LocationCategory.LIFE_BOTTLE in self.enabled_location_categories:
                set_rule(self.multiworld.get_location("Fireworks Factory: Life Bottle in Agent 9 Sub-Area", self.player), lambda state: is_level_completed(self, "Agent 9's Lab", state))
        if self.generation_options["powerup_lock_settings"] == PowerupLockOptions.TYPE:
            set_rule(self.multiworld.get_location("Fireworks Factory: Bad dragon! (Evan)", self.player),
                     lambda state: state.has("Fireball Powerup", self.player) and state.has("Superfly Powerup", self.player))
        elif self.generation_options["powerup_lock_settings"] == PowerupLockOptions.INDIVIDUAL:
            set_rule(self.multiworld.get_location("Fireworks Factory: Bad dragon! (Evan)", self.player),
                     lambda state: state.has("Fireworks Combo Powerup", self.player))
        if Spyro3LocationCategory.GEMSANITY in self.enabled_location_categories:
            for i in range(233):
                if len(self.chosen_gem_locations) == 0 or f"Fireworks Factory: Gem {i + 1}" in self.chosen_gem_locations:
                    set_rule(
                        self.multiworld.get_location(f"Fireworks Factory: Gem {i + 1}", self.player),
                        lambda state: are_gems_accessible(self, state)
                    )
            # Bits of the gems, not accounting for empty bits
            agent_gems = [161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 178, 179,
                          180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198,
                          199, 200, 201]
            combo_powerup_gems = [111, 112, 114, 115, 116]
            empty_bits = [14, 20, 46, 51, 77, 82, 97, 98, 104, 105, 106, 108, 141, 153, 155, 177]
            if not self.generation_options["logic_fireworks_agent_9_early"]:
                for gem in agent_gems:
                    skipped_bits = 0
                    for bit in empty_bits:
                        if bit < gem:
                            skipped_bits += 1
                        else:
                            break
                    if self.PRINT_GEM_REQS:
                        print(f"Fireworks Factory: Gem {gem - skipped_bits} requires Agent 9.")
                    if len(self.chosen_gem_locations) == 0 or f"Fireworks Factory: Gem {gem - skipped_bits}" in self.chosen_gem_locations:
                        add_rule(
                            self.multiworld.get_location(f"Fireworks Factory: Gem {gem - skipped_bits}", self.player),
                            lambda state: is_level_completed(self, "Agent 9's Lab", state)
                        )
            for gem in combo_powerup_gems:
                skipped_bits = 0
                for bit in empty_bits:
                    if bit < gem:
                        skipped_bits += 1
                    else:
                        break
                if self.PRINT_GEM_REQS:
                    print(f"Fireworks Factory: Gem {gem - skipped_bits} requires combo superfly and fireball powerup access.")
                if len(self.chosen_gem_locations) == 0 or f"Fireworks Factory: Gem {gem - skipped_bits}" in self.chosen_gem_locations:
                    if self.generation_options["powerup_lock_settings"] == PowerupLockOptions.TYPE:
                        add_rule(
                            self.multiworld.get_location(f"Fireworks Factory: Gem {gem - skipped_bits}", self.player),
                            lambda state: state.has("Fireball Powerup", self.player) and state.has("Superfly Powerup", self.player)
                        )
                    elif self.generation_options["powerup_lock_settings"] == PowerupLockOptions.INDIVIDUAL:
                        add_rule(
                            self.multiworld.get_location(f"Fireworks Factory: Gem {gem - skipped_bits}", self.player),
                            lambda state: state.has("Fireworks Combo Powerup", self.player)
                        )


        # Charmed Ridge Rules
        if self.generation_options["enable_progressive_sparx_logic"]:
            set_indirect_rule(
                self,
                "Charmed Ridge",
                lambda state: (has_sparx_health(self, 2, state) or is_glitched_logic(self, state)) and can_enter_non_companion_portal(self, "Charmed Ridge", state, self.generation_options["logic_charmed_early"])
            )
        else:
            set_indirect_rule(
                self,
                "Charmed Ridge",
                lambda state: can_enter_non_companion_portal(self, "Charmed Ridge", state, self.generation_options["logic_charmed_early"])
            )
        # Can glide through a part of the wall with no collision.  A proxy to end of level is possible, but this is harder and grants less access.
        if not self.generation_options["open_world"] and self.generation_options["moneybags_settings"] == MoneybagsOptions.MONEYBAGSSANITY and not self.generation_options["logic_charmed_no_moneybags"]:
            if not self.generation_options["open_world"]:
                set_rule(self.multiworld.get_location("Charmed Ridge: Rescue the Fairy Princess. (Sakura)", self.player), lambda state: state.has("Moneybags Unlock - Charmed Ridge Stairs", self.player))
            set_rule(self.multiworld.get_location("Charmed Ridge: Glide to the tower. (Moe)", self.player), lambda state: state.has("Moneybags Unlock - Charmed Ridge Stairs", self.player))
            set_rule(self.multiworld.get_location("Charmed Ridge: Egg in the cave. (Benjamin)", self.player), lambda state: state.has("Moneybags Unlock - Charmed Ridge Stairs", self.player))
            set_rule(self.multiworld.get_location("Charmed Ridge: Jack and the beanstalk I. (Shelley)", self.player), lambda state: state.has("Moneybags Unlock - Charmed Ridge Stairs", self.player))
            set_rule(self.multiworld.get_location("Charmed Ridge: Jack and the beanstalk II. (Chuck)", self.player), lambda state: state.has("Moneybags Unlock - Charmed Ridge Stairs", self.player))
            if not self.generation_options["open_world"]:
                set_rule(self.multiworld.get_location("Charmed Ridge Complete", self.player), lambda state: state.has("Moneybags Unlock - Charmed Ridge Stairs", self.player))
            set_rule(self.multiworld.get_location("Charmed Ridge: Cat witch chaos. (Abby)", self.player), lambda state: is_level_completed(self, "Sgt. Byrd's Base", state) and state.has("Moneybags Unlock - Charmed Ridge Stairs", self.player))
            if Spyro3LocationCategory.SKILLPOINT in self.enabled_location_categories:
                set_rule(self.multiworld.get_location("Charmed Ridge: Shoot the temple windows (Skill Point)", self.player), lambda state: is_level_completed(self, "Sgt. Byrd's Base", state) and state.has("Moneybags Unlock - Charmed Ridge Stairs", self.player))
                set_rule(self.multiworld.get_location("Charmed Ridge: The Impossible Tower (Skill Point)", self.player), lambda state: state.has("Moneybags Unlock - Charmed Ridge Stairs", self.player))
            if Spyro3LocationCategory.SKILLPOINT_GOAL in self.enabled_location_categories:
                set_rule(self.multiworld.get_location("Charmed Ridge: Shoot the temple windows (Goal)", self.player), lambda state: is_level_completed(self, "Sgt. Byrd's Base", state) and state.has("Moneybags Unlock - Charmed Ridge Stairs", self.player))
                set_rule(self.multiworld.get_location("Charmed Ridge: The Impossible Tower (Goal)", self.player), lambda state: state.has("Moneybags Unlock - Charmed Ridge Stairs", self.player))
        else:
            set_rule(self.multiworld.get_location("Charmed Ridge: Cat witch chaos. (Abby)", self.player), lambda state: is_level_completed(self,"Sgt. Byrd's Base", state))
            if Spyro3LocationCategory.SKILLPOINT in self.enabled_location_categories:
                set_rule(self.multiworld.get_location("Charmed Ridge: Shoot the temple windows (Skill Point)", self.player), lambda state: is_level_completed(self, "Sgt. Byrd's Base", state))
            if Spyro3LocationCategory.SKILLPOINT_GOAL in self.enabled_location_categories:
                set_rule(self.multiworld.get_location("Charmed Ridge: Shoot the temple windows (Goal)", self.player), lambda state: is_level_completed(self, "Sgt. Byrd's Base", state))
        if Spyro3LocationCategory.GEMSANITY in self.enabled_location_categories:
            for i in range(175):
                if len(self.chosen_gem_locations) == 0 or f"Charmed Ridge: Gem {i + 1}" in self.chosen_gem_locations:
                    set_rule(
                        self.multiworld.get_location(f"Charmed Ridge: Gem {i + 1}", self.player),
                        lambda state: are_gems_accessible(self, state)
                    )
            # Bits of the gems, not accounting for empty bits
            moneybags_gems = [12, 13, 14, 15, 16, 17, 18, 19, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 39, 40,
                              41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 54, 55, 56, 57, 62, 63, 64, 65, 67, 68, 69,
                              73, 74, 75, 76, 77, 78, 80, 81, 82, 83, 84, 85, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99,
                              104, 105, 106, 107, 108, 112, 118, 119, 120, 121, 122, 123, 125, 126, 127, 128, 131, 138,
                              139, 140, 141, 142, 143, 148, 153, 154, 155, 156, 157, 158, 159, 160, 161, 163, 164, 165,
                              166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183,
                              184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197]
            fireball_gems = [120, 121]
            empty_bits = [20, 21, 53, 58, 59, 60, 61, 66, 100, 101, 102, 129, 130, 136, 137, 144, 145, 146, 147, 150,
                          152, 162]
            if not self.generation_options["open_world"] and self.generation_options["moneybags_settings"] == MoneybagsOptions.MONEYBAGSSANITY and not self.generation_options["logic_charmed_no_moneybags"]:
                for gem in moneybags_gems:
                    skipped_bits = 0
                    for bit in empty_bits:
                        if bit < gem:
                            skipped_bits += 1
                        else:
                            break
                    if self.PRINT_GEM_REQS:
                        if gem not in fireball_gems:
                            print(f"Charmed Ridge: Gem {gem - skipped_bits} requires access past Moneybags.")
                        else:
                            print(f"Charmed Ridge: Gem {gem - skipped_bits} requires access past Moneybags and the Fireball powerup.")
                    if len(self.chosen_gem_locations) == 0 or f"Charmed Ridge: Gem {gem - skipped_bits}" in self.chosen_gem_locations:
                        if gem not in fireball_gems:
                            add_rule(
                                self.multiworld.get_location(f"Charmed Ridge: Gem {gem - skipped_bits}", self.player),
                                lambda state: state.has("Moneybags Unlock - Charmed Ridge Stairs", self.player)
                            )
                        else:
                            if self.generation_options["powerup_lock_settings"] == PowerupLockOptions.TYPE:
                                add_rule(
                                    self.multiworld.get_location(f"Charmed Ridge: Gem {gem - skipped_bits}", self.player),
                                    lambda state: state.has("Moneybags Unlock - Charmed Ridge Stairs", self.player) and state.has("Fireball Powerup", self.player)
                                )
                            elif self.generation_options["powerup_lock_settings"] == PowerupLockOptions.INDIVIDUAL:
                                add_rule(
                                    self.multiworld.get_location(f"Charmed Ridge: Gem {gem - skipped_bits}", self.player),
                                    lambda state: state.has("Moneybags Unlock - Charmed Ridge Stairs", self.player) and state.has("Charmed Fireball Powerup", self.player)
                                )
            else:
                for gem in fireball_gems:
                    skipped_bits = 0
                    for bit in empty_bits:
                        if bit < gem:
                            skipped_bits += 1
                        else:
                            break
                    if self.PRINT_GEM_REQS:
                        print(f"Charmed Ridge: Gem {gem - skipped_bits} requires the Fireball powerup.")
                    if len(self.chosen_gem_locations) == 0 or f"Charmed Ridge: Gem {gem - skipped_bits}" in self.chosen_gem_locations:
                        if self.generation_options["powerup_lock_settings"] == PowerupLockOptions.TYPE:
                            add_rule(
                                self.multiworld.get_location(f"Charmed Ridge: Gem {gem - skipped_bits}", self.player),
                                lambda state: state.has("Fireball Powerup", self.player)
                            )
                        elif self.generation_options["powerup_lock_settings"] == PowerupLockOptions.INDIVIDUAL:
                            add_rule(
                                self.multiworld.get_location(f"Charmed Ridge: Gem {gem - skipped_bits}", self.player),
                                lambda state: state.has("Charmed Fireball Powerup", self.player)
                            )


        # Honey Speedway Rules
        set_indirect_rule(
            self,
            "Honey Speedway",
            lambda state: can_enter_non_companion_portal(self, "Honey Speedway", state, self.generation_options["logic_honey_early"])
        )
        # Hunter speedway challenges are not available while Hunter is captured.
        set_rule(self.multiworld.get_location("Honey Speedway: Hunter's narrow escape. (Nori)", self.player), lambda state: is_boss_defeated(self, "Scorch", state) or is_glitched_logic(self, state))
        # Speedway gems are always accessible in gemsanity.


        # Bentley's Outpost Rules
        if self.generation_options["enable_progressive_sparx_logic"] and self.generation_options["moneybags_settings"] != MoneybagsOptions.VANILLA and not self.generation_options["logic_bentley_early"]:
            set_indirect_rule(
                self,
                "Bentley's Outpost",
                lambda state: (has_sparx_health(self, 1, state) or is_glitched_logic(self, state)) and is_companion_unlocked(self, "Bentley", state)
            )
        elif self.generation_options["moneybags_settings"] != MoneybagsOptions.VANILLA and not self.generation_options["logic_bentley_early"]:
            set_indirect_rule(self, "Bentley's Outpost", lambda state: is_companion_unlocked(self, "Bentley", state))
        elif self.generation_options["enable_progressive_sparx_logic"]:
            set_indirect_rule(self, "Bentley's Outpost", lambda state: (has_sparx_health(self, 1, state) or is_glitched_logic(self, state)))
        if Spyro3LocationCategory.GEMSANITY in self.enabled_location_categories:
            for i in range(109):
                if len(self.chosen_gem_locations) == 0 or f"Bentley's Outpost: Gem {i + 1}" in self.chosen_gem_locations:
                    set_rule(
                        self.multiworld.get_location(f"Bentley's Outpost: Gem {i + 1}", self.player),
                        lambda state: are_gems_accessible(self, state)
                    )


        # Scorch's Pit Rules
        if self.generation_options["enable_progressive_sparx_logic"]:
            set_indirect_rule(self, "Scorch", lambda state: is_level_completed(self, "Frozen Altars", state) and \
                    is_level_completed(self, "Lost Fleet", state) and \
                    is_level_completed(self, "Fireworks Factory", state) and \
                    is_level_completed(self, "Charmed Ridge", state) and \
                    is_level_completed(self, "Bentley's Outpost", state) and \
                    (has_sparx_health(self, 2, state) or is_glitched_logic(self, state)))
        else:
            set_indirect_rule(self, "Scorch", lambda state: is_level_completed(self,"Frozen Altars", state) and \
                    is_level_completed(self,"Lost Fleet", state) and \
                    is_level_completed(self,"Fireworks Factory", state) and \
                    is_level_completed(self,"Charmed Ridge", state) and \
                    is_level_completed(self,"Bentley's Outpost", state))


        # Starfish Reef Rules
        if self.generation_options["enable_progressive_sparx_logic"]:
            set_indirect_rule(self, "Starfish Reef", lambda state: is_boss_defeated(self, "Scorch", state) and \
                    is_level_completed(self, 'Spider Town', state) and \
                    (has_sparx_health(self, 2, state) or is_glitched_logic(self, state))
            )
        else:
            set_indirect_rule(self, "Starfish Reef", lambda state: is_boss_defeated(self,"Scorch", state) and is_level_completed(self, 'Spider Town', state))
        # Sparx level gems are always accessible in gemsanity.


        # Midnight Mountain Rules
        if self.generation_options["enable_world_keys"]:
            set_indirect_rule(self, "Midnight Mountain", lambda state: is_boss_defeated(self, "Scorch", state) and has_world_keys(self, 3, state))
        else:
            set_indirect_rule(self, "Midnight Mountain", lambda state: is_boss_defeated(self, "Scorch", state))
        if self.generation_options["goal"] != GoalOptions.EGG_HUNT or self.generation_options["egg_count"] > self.generation_options["sorceress_door_requirement"]:
            set_rule(self.multiworld.get_location("Midnight Mountain Home: Egg for sale. (Al)", self.player), lambda state: is_boss_defeated(self,"Sorceress", state))
            set_rule(self.multiworld.get_location("Midnight Mountain Home: Moneybags Chase Complete", self.player), lambda state: is_boss_defeated(self, "Sorceress", state))
        if Spyro3LocationCategory.GEMSANITY in self.enabled_location_categories:
            for i in range(105):
                if len(self.chosen_gem_locations) == 0 or f"Midnight Mountain: Gem {i + 1}" in self.chosen_gem_locations:
                    set_rule(
                        self.multiworld.get_location(f"Midnight Mountain: Gem {i + 1}", self.player),
                        lambda state: are_gems_accessible(self, state)
                    )


        # Crystal Islands Rules
        if self.generation_options["enable_progressive_sparx_logic"]:
            set_indirect_rule(
                self,
                "Crystal Islands",
                lambda state: (has_sparx_health(self, 2, state) or is_glitched_logic(self, state)) and can_enter_non_companion_portal(self, "Crystal Islands", state, True)
            )
        else:
            set_indirect_rule(
                self,
                "Crystal Islands",
                lambda state: can_enter_non_companion_portal(self, "Crystal Islands", state, True)
            )
        # Can defeat the Sorceress or perform a swim in air.
        if self.generation_options["moneybags_settings"] == MoneybagsOptions.MONEYBAGSSANITY and not self.generation_options["logic_crystal_no_moneybags"]:
            # Moneybags locks 475 gems.
            set_rule(self.multiworld.get_location("Crystal Islands: Reach the crystal tower. (Lloyd)", self.player), lambda state: (self.generation_options["goal"] != GoalOptions.EGG_HUNT or self.generation_options["egg_count"] > self.generation_options["sorceress_door_requirement"]) and is_boss_defeated(self, "Sorceress", state) or state.has("Moneybags Unlock - Crystal Islands Bridge", self.player))
            set_rule(self.multiworld.get_location("Crystal Islands: Ride the slide. (Elloise)", self.player), lambda state: (self.generation_options["goal"] != GoalOptions.EGG_HUNT or self.generation_options["egg_count"] > self.generation_options["sorceress_door_requirement"]) and is_boss_defeated(self, "Sorceress", state) or state.has("Moneybags Unlock - Crystal Islands Bridge", self.player))
            if self.generation_options["powerup_lock_settings"] == PowerupLockOptions.TYPE:
                set_rule(self.multiworld.get_location("Crystal Islands: Fly to the hidden egg. (Grace)", self.player),
                         lambda state: ((self.generation_options["goal"] != GoalOptions.EGG_HUNT or
                                        self.generation_options["egg_count"] > self.generation_options["sorceress_door_requirement"]) and
                                        is_boss_defeated(self, "Sorceress", state) or state.has("Moneybags Unlock - Crystal Islands Bridge", self.player)) and
                                        state.has("Superfly Powerup", self.player)
                )
                set_rule(self.multiworld.get_location("Crystal Islands: Catch the flying thief. (Max)", self.player),
                         lambda state: ((self.generation_options["goal"] != GoalOptions.EGG_HUNT or
                                        self.generation_options["egg_count"] > self.generation_options["sorceress_door_requirement"]) and
                                        is_boss_defeated(self, "Sorceress", state) or state.has("Moneybags Unlock - Crystal Islands Bridge", self.player)) and
                                        state.has("Superfly Powerup", self.player)
                )
            elif self.generation_options["powerup_lock_settings"] == PowerupLockOptions.INDIVIDUAL:
                set_rule(self.multiworld.get_location("Crystal Islands: Fly to the hidden egg. (Grace)", self.player),
                         lambda state: ((self.generation_options["goal"] != GoalOptions.EGG_HUNT or
                                        self.generation_options["egg_count"] > self.generation_options[
                                            "sorceress_door_requirement"]) and
                                       is_boss_defeated(self, "Sorceress", state) or state.has(
                                        "Moneybags Unlock - Crystal Islands Bridge", self.player)) and
                                       state.has("Crystal Superfly Powerup", self.player)
                )
                set_rule(self.multiworld.get_location("Crystal Islands: Catch the flying thief. (Max)", self.player),
                         lambda state: ((self.generation_options["goal"] != GoalOptions.EGG_HUNT or
                                        self.generation_options["egg_count"] > self.generation_options[
                                            "sorceress_door_requirement"]) and
                                       is_boss_defeated(self, "Sorceress", state) or state.has(
                                        "Moneybags Unlock - Crystal Islands Bridge", self.player)) and
                                       state.has("Crystal Superfly Powerup", self.player)
                )
            else:
                set_rule(self.multiworld.get_location("Crystal Islands: Fly to the hidden egg. (Grace)", self.player),
                         lambda state: (self.generation_options["goal"] != GoalOptions.EGG_HUNT or
                                        self.generation_options["egg_count"] > self.generation_options["sorceress_door_requirement"]) and
                                       is_boss_defeated(self, "Sorceress", state) or state.has("Moneybags Unlock - Crystal Islands Bridge", self.player))
                set_rule(self.multiworld.get_location("Crystal Islands: Catch the flying thief. (Max)", self.player),
                         lambda state: (self.generation_options["goal"] != GoalOptions.EGG_HUNT or
                                        self.generation_options["egg_count"] > self.generation_options["sorceress_door_requirement"]) and
                                       is_boss_defeated(self, "Sorceress", state) or state.has("Moneybags Unlock - Crystal Islands Bridge", self.player))
            set_rule(self.multiworld.get_location("Crystal Islands Complete", self.player), lambda state: (self.generation_options["goal"] != GoalOptions.EGG_HUNT or self.generation_options["egg_count"] > self.generation_options["sorceress_door_requirement"]) and is_boss_defeated(self, "Sorceress", state) or state.has("Moneybags Unlock - Crystal Islands Bridge", self.player))
            set_rule(self.multiworld.get_location("Crystal Islands: Whack a mole. (Hank)", self.player), lambda state: is_level_completed(self, "Bentley's Outpost", state) and ((self.generation_options["goal"] != GoalOptions.EGG_HUNT or self.generation_options["egg_count"] > self.generation_options["sorceress_door_requirement"]) and is_boss_defeated(self, "Sorceress", state) or state.has("Moneybags Unlock - Crystal Islands Bridge", self.player)))
        else:
            if self.generation_options["powerup_lock_settings"] == PowerupLockOptions.TYPE:
                set_rule(self.multiworld.get_location("Crystal Islands: Fly to the hidden egg. (Grace)", self.player),
                         lambda state: state.has("Superfly Powerup", self.player)
                )
                set_rule(self.multiworld.get_location("Crystal Islands: Catch the flying thief. (Max)", self.player),
                         lambda state: state.has("Superfly Powerup", self.player)
                )
            elif self.generation_options["powerup_lock_settings"] == PowerupLockOptions.INDIVIDUAL:
                set_rule(self.multiworld.get_location("Crystal Islands: Fly to the hidden egg. (Grace)", self.player),
                         lambda state: state.has("Crystal Superfly Powerup", self.player)
                )
                set_rule(self.multiworld.get_location("Crystal Islands: Catch the flying thief. (Max)", self.player),
                         lambda state: state.has("Crystal Superfly Powerup", self.player)
                )
            set_rule(self.multiworld.get_location("Crystal Islands: Whack a mole. (Hank)", self.player), lambda state: is_level_completed(self,"Bentley's Outpost", state))
        if Spyro3LocationCategory.GEMSANITY in self.enabled_location_categories:
            for i in range(205):
                if len(self.chosen_gem_locations) == 0 or f"Crystal Islands: Gem {i + 1}" in self.chosen_gem_locations:
                    set_rule(
                        self.multiworld.get_location(f"Crystal Islands: Gem {i + 1}", self.player),
                        lambda state: are_gems_accessible(self, state)
                    )
            # Bits of the gems, not accounting for empty bits
            moneybags_gems = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 39, 40, 42, 43, 44, 45, 46, 47, 48, 49, 54, 55, 56,
                              58, 59, 64, 65, 66, 67, 70, 71, 72, 73, 74, 75, 76, 77, 78, 85, 86, 90, 91, 92, 93, 94, 111,
                              143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160,
                              161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178,
                              179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196,
                              197, 198, 199, 200, 205, 206, 207, 208, 209, 210, 211, 213, 214, 215, 226, 227, 228, 229,
                              230]
            superfly_gems = [40, 42, 43, 44, 45, 46, 47, 48, 49, 54, 55, 56, 58, 59, 64, 70, 71, 72, 73, 74, 75, 76, 77,
                             78]
            empty_bits = [26, 41, 50, 51, 60, 61, 62, 63, 69, 102, 201, 202, 203, 204, 212, 216, 217, 218, 219, 220,
                          221, 222, 223, 224, 225]
            if self.generation_options["moneybags_settings"] == MoneybagsOptions.MONEYBAGSSANITY and not self.generation_options["logic_crystal_no_moneybags"]:
                for gem in moneybags_gems:
                    skipped_bits = 0
                    for bit in empty_bits:
                        if bit < gem:
                            skipped_bits += 1
                        else:
                            break
                    if self.PRINT_GEM_REQS:
                        if gem not in superfly_gems:
                            print(f"Crystal Islands: Gem {gem - skipped_bits} requires access past Moneybags.")
                        else:
                            print(f"Crystal Islands: Gem {gem - skipped_bits} requires access past Moneybags and the Superfly powerup.")
                    if len(self.chosen_gem_locations) == 0 or f"Crystal Islands: Gem {gem - skipped_bits}" in self.chosen_gem_locations:
                        if gem not in superfly_gems:
                            add_rule(
                                self.multiworld.get_location(f"Crystal Islands: Gem {gem - skipped_bits}", self.player),
                                lambda state: (self.generation_options["goal"] != GoalOptions.EGG_HUNT or
                                               self.generation_options["egg_count"] > self.generation_options["sorceress_door_requirement"]) and
                                               is_boss_defeated(self, "Sorceress", state) or state.has("Moneybags Unlock - Crystal Islands Bridge", self.player)
                            )
                        else:
                            if self.generation_options["powerup_lock_settings"] == PowerupLockOptions.TYPE:
                                add_rule(
                                    self.multiworld.get_location(f"Crystal Islands: Gem {gem - skipped_bits}", self.player),
                                    lambda state: ((self.generation_options["goal"] != GoalOptions.EGG_HUNT or
                                                   self.generation_options["egg_count"] > self.generation_options["sorceress_door_requirement"]) and
                                                   is_boss_defeated(self, "Sorceress", state) or state.has("Moneybags Unlock - Crystal Islands Bridge", self.player))
                                                   and state.has("Superfly Powerup", self.player)
                                )
                            elif self.generation_options["powerup_lock_settings"] == PowerupLockOptions.INDIVIDUAL:
                                add_rule(
                                    self.multiworld.get_location(f"Crystal Islands: Gem {gem - skipped_bits}", self.player),
                                    lambda state: ((self.generation_options["goal"] != GoalOptions.EGG_HUNT or
                                                   self.generation_options["egg_count"] > self.generation_options["sorceress_door_requirement"]) and
                                                   is_boss_defeated(self, "Sorceress", state) or state.has("Moneybags Unlock - Crystal Islands Bridge", self.player))
                                                   and state.has("Crystal Superfly Powerup", self.player)
                                )
            else:
                for gem in superfly_gems:
                    skipped_bits = 0
                    for bit in empty_bits:
                        if bit < gem:
                            skipped_bits += 1
                        else:
                            break
                    if self.PRINT_GEM_REQS:
                        print(f"Crystal Islands: Gem {gem - skipped_bits} requires the Superfly powerup.")
                    if len(self.chosen_gem_locations) == 0 or f"Crystal Islands: Gem {gem - skipped_bits}" in self.chosen_gem_locations:
                        if self.generation_options["powerup_lock_settings"] == PowerupLockOptions.TYPE:
                            add_rule(
                                self.multiworld.get_location(f"Crystal Islands: Gem {gem - skipped_bits}", self.player),
                                lambda state: state.has("Superfly Powerup", self.player)
                            )
                        elif self.generation_options["powerup_lock_settings"] == PowerupLockOptions.INDIVIDUAL:
                            add_rule(
                                self.multiworld.get_location(f"Crystal Islands: Gem {gem - skipped_bits}", self.player),
                                lambda state: state.has("Crystal Superfly Powerup", self.player)
                            )


        # Desert Ruins Rules
        if self.generation_options["enable_progressive_sparx_logic"]:
            set_indirect_rule(
                self,
                "Desert Ruins",
                lambda state: (has_sparx_health(self, 2, state) or is_glitched_logic(self, state)) and can_enter_non_companion_portal(self, "Desert Ruins", state, True)
            )
        else:
            set_indirect_rule(
                self,
                "Desert Ruins",
                lambda state: can_enter_non_companion_portal(self, "Desert Ruins", state, True)
            )
        set_rule(self.multiworld.get_location("Desert Ruins: Krash Kangaroo I. (Lester)", self.player), lambda state: is_level_completed(self,"Sheila's Alp", state))
        set_rule(self.multiworld.get_location("Desert Ruins: Krash Kangaroo II. (Pete)", self.player), lambda state: is_level_completed(self,"Sheila's Alp", state))
        # Can defeat the Sorceress, proxy off a scorpion, or do a terrain jump to end of level.
        if self.generation_options["moneybags_settings"] == MoneybagsOptions.MONEYBAGSSANITY and not self.generation_options["logic_desert_no_moneybags"]:
            # 79 gems in Sheila subarea. 252 are locked behind Moneybags.
            set_rule(self.multiworld.get_location("Desert Ruins: Raid the tomb. (Marty)", self.player), lambda state: (self.generation_options["goal"] != GoalOptions.EGG_HUNT or self.generation_options["egg_count"] > self.generation_options["sorceress_door_requirement"]) and is_boss_defeated(self, "Sorceress", state) or state.has("Moneybags Unlock - Desert Ruins Door", self.player))
            set_rule(self.multiworld.get_location("Desert Ruins: Shark shootin'. (Sadie)", self.player), lambda state: (self.generation_options["goal"] != GoalOptions.EGG_HUNT or self.generation_options["egg_count"] > self.generation_options["sorceress_door_requirement"]) and is_boss_defeated(self, "Sorceress", state) or state.has("Moneybags Unlock - Desert Ruins Door", self.player))
            set_rule(self.multiworld.get_location("Desert Ruins Complete", self.player), lambda state: (self.generation_options["goal"] != GoalOptions.EGG_HUNT or self.generation_options["egg_count"] > self.generation_options["sorceress_door_requirement"]) and is_boss_defeated(self, "Sorceress", state) or state.has("Moneybags Unlock - Desert Ruins Door", self.player))
            if Spyro3LocationCategory.SKILLPOINT in self.enabled_location_categories:
                set_rule(self.multiworld.get_location("Desert Ruins: Destroy all seaweed (Skill Point)", self.player), lambda state: (self.generation_options["goal"] != GoalOptions.EGG_HUNT or self.generation_options["egg_count"] > self.generation_options["sorceress_door_requirement"]) and is_boss_defeated(self, "Sorceress", state) or state.has("Moneybags Unlock - Desert Ruins Door", self.player))
            if Spyro3LocationCategory.SKILLPOINT_GOAL in self.enabled_location_categories:
                set_rule(self.multiworld.get_location("Desert Ruins: Destroy all seaweed (Goal)", self.player), lambda state: (self.generation_options["goal"] != GoalOptions.EGG_HUNT or self.generation_options["egg_count"] > self.generation_options["sorceress_door_requirement"]) and is_boss_defeated(self, "Sorceress", state) or state.has("Moneybags Unlock - Desert Ruins Door", self.player))
            if Spyro3LocationCategory.LIFE_BOTTLE in self.enabled_location_categories:
                set_rule(self.multiworld.get_location("Desert Ruins: Life Bottle near Sharks Sub-Area", self.player), lambda state: (self.generation_options["goal"] != GoalOptions.EGG_HUNT or self.generation_options["egg_count"] > self.generation_options["sorceress_door_requirement"]) and is_boss_defeated(self, "Sorceress", state) or state.has("Moneybags Unlock - Desert Ruins Door", self.player))
        if Spyro3LocationCategory.GEMSANITY in self.enabled_location_categories:
            for i in range(144):
                if len(self.chosen_gem_locations) == 0 or f"Desert Ruins: Gem {i + 1}" in self.chosen_gem_locations:
                    set_rule(
                        self.multiworld.get_location(f"Desert Ruins: Gem {i + 1}", self.player),
                        lambda state: are_gems_accessible(self, state)
                    )
            # Bits of the gems, not accounting for empty bits
            moneybags_gems = [16, 17, 18, 19, 24, 42, 43, 60, 64, 65, 67, 70, 71, 72, 73, 81, 82, 94, 95, 98, 99, 100,
                              101, 102, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148,
                              149, 158, 159, 160, 161, 162, 163, 164, 165, 166, 182, 183, 184, 185, 186, 187, 188, 189]
            empty_bits = [15, 20, 21, 50, 56, 63, 83, 89, 90, 91, 92, 93, 103, 104, 106, 107, 108, 109, 123, 124, 125,
                          126, 150, 151, 152, 153, 154, 155, 156, 157, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176,
                          177, 178, 179, 180, 181]
            if self.generation_options["moneybags_settings"] == MoneybagsOptions.MONEYBAGSSANITY and not self.generation_options["logic_desert_no_moneybags"]:
                for gem in moneybags_gems:
                    skipped_bits = 0
                    for bit in empty_bits:
                        if bit < gem:
                            skipped_bits += 1
                        else:
                            break
                    if self.PRINT_GEM_REQS:
                        print(f"Desert Ruins: Gem {gem - skipped_bits} requires access past Moneybags.")
                    if len(self.chosen_gem_locations) == 0 or f"Desert Ruins: Gem {gem - skipped_bits}" in self.chosen_gem_locations:
                        add_rule(
                            self.multiworld.get_location(f"Desert Ruins: Gem {gem - skipped_bits}", self.player),
                            lambda state: (self.generation_options["goal"] != GoalOptions.EGG_HUNT or self.generation_options["egg_count"] > self.generation_options["sorceress_door_requirement"]) and is_boss_defeated(self, "Sorceress", state) or state.has("Moneybags Unlock - Desert Ruins Door", self.player)
                        )


        # Haunted Tomb Rules
        if self.generation_options["enable_progressive_sparx_logic"]:
            set_indirect_rule(
                self,
                "Haunted Tomb",
                lambda state: (has_sparx_health(self, 2, state) or is_glitched_logic(self, state)) and can_enter_non_companion_portal(self, "Haunted Tomb", state, False)
            )
        else:
            set_indirect_rule(
                self,
                "Haunted Tomb",
                lambda state: can_enter_non_companion_portal(self, "Haunted Tomb", state, False)
            )
        set_rule(self.multiworld.get_location("Haunted Tomb: Clear the caves. (Roxy)", self.player), lambda state: is_level_completed(self, "Agent 9's Lab", state))
        if Spyro3LocationCategory.GEMSANITY in self.enabled_location_categories:
            for i in range(115):
                if len(self.chosen_gem_locations) == 0 or f"Haunted Tomb: Gem {i + 1}" in self.chosen_gem_locations:
                    set_rule(
                        self.multiworld.get_location(f"Haunted Tomb: Gem {i + 1}", self.player),
                        lambda state: are_gems_accessible(self, state)
                    )


        # Dino Mines Rules
        if self.generation_options["enable_progressive_sparx_logic"]:
            set_indirect_rule(
                self,
                "Dino Mines",
                lambda state: (has_sparx_health(self, 3, state) or is_glitched_logic(self, state)) and can_enter_non_companion_portal(self, "Dino Mines", state, False)
            )
        else:
            set_indirect_rule(
                self,
                "Dino Mines",
                lambda state: can_enter_non_companion_portal(self, "Dino Mines", state, False)
            )
        if not self.generation_options["logic_dino_agent_9_early"]:
            set_rule(self.multiworld.get_location("Dino Mines: Gunfight at the Jurassic Corral. (Sharon)", self.player), lambda state: is_level_completed(self, "Agent 9's Lab", state))
            set_rule(self.multiworld.get_location("Dino Mines: Take it to the bank. (Sergio)", self.player), lambda state: is_level_completed(self, "Agent 9's Lab", state) and state.can_reach_location("Dino Mines: Gunfight at the Jurassic Corral. (Sharon)", self.player))
            if Spyro3LocationCategory.SKILLPOINT in self.enabled_location_categories:
                set_rule(self.multiworld.get_location("Dino Mines: Hit the secret dino (Skill Point)", self.player), lambda state: is_level_completed(self, "Agent 9's Lab", state))
            if Spyro3LocationCategory.SKILLPOINT_GOAL in self.enabled_location_categories:
                set_rule(self.multiworld.get_location("Dino Mines: Hit the secret dino (Goal)", self.player), lambda state: is_level_completed(self, "Agent 9's Lab", state))
        if Spyro3LocationCategory.GEMSANITY in self.enabled_location_categories:
            for i in range(143):
                if len(self.chosen_gem_locations) == 0 or f"Dino Mines: Gem {i + 1}" in self.chosen_gem_locations:
                    set_rule(
                        self.multiworld.get_location(f"Dino Mines: Gem {i + 1}", self.player),
                        lambda state: are_gems_accessible(self, state)
                    )
            # Bits of the gems, not accounting for empty bits
            agent_gems = [169, 170, 185, 187, 188, 189, 190, 191, 193, 194, 195, 198, 199, 200, 201, 203, 204, 205,
                          209, 210, 211, 220, 221, 222, 223, 224, 226, 227, 228, 229]
            empty_bits = [24, 41, 61, 77, 79, 82, 83, 88, 90, 98, 104, 111, 117, 127, 128, 129, 130, 131, 132, 133,
                          134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151,
                          152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 171,
                          172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 186, 192, 196, 197, 202,
                          206, 207, 208, 212, 213, 214, 215, 216, 217, 218, 219, 225]
            if not self.generation_options["logic_dino_agent_9_early"]:
                for gem in agent_gems:
                    skipped_bits = 0
                    for bit in empty_bits:
                        if bit < gem:
                            skipped_bits += 1
                        else:
                            break
                    if self.PRINT_GEM_REQS:
                        print(f"Dino Mines: Gem {gem - skipped_bits} requires Agent 9.")
                    if len(self.chosen_gem_locations) == 0 or f"Dino Mines: Gem {gem - skipped_bits}" in self.chosen_gem_locations:
                        add_rule(
                            self.multiworld.get_location(f"Dino Mines: Gem {gem - skipped_bits}", self.player),
                            lambda state: is_level_completed(self, "Agent 9's Lab", state)
                        )


        # Harbor Speedway Rules
        set_indirect_rule(
            self,
            "Harbor Speedway",
            lambda state: can_enter_non_companion_portal(self, "Harbor Speedway", state, False)
        )
        # Speedway gems are always accessible in gemsanity.


        # Agent 9's Lab Rules
        # No known way to skip into Agent 9's Lab, other than beating the Sorceress.
        if self.generation_options["enable_progressive_sparx_logic"] and self.generation_options["moneybags_settings"] != MoneybagsOptions.VANILLA:
            set_indirect_rule(
                self,
                "Agent 9's Lab",
                lambda state: (has_sparx_health(self, 2, state) or is_glitched_logic(self, state)) and (is_companion_unlocked(self, "Agent 9", state) or (self.generation_options["goal"] != GoalOptions.EGG_HUNT or self.generation_options["egg_count"] > self.generation_options["sorceress_door_requirement"]) and is_boss_defeated(self, "Sorceress", state))
            )
        elif self.generation_options["moneybags_settings"] != MoneybagsOptions.VANILLA:
            set_indirect_rule(self, "Agent 9's Lab", lambda state: (is_companion_unlocked(self, "Agent 9", state) or (self.generation_options["goal"] != GoalOptions.EGG_HUNT or self.generation_options["egg_count"] > self.generation_options["sorceress_door_requirement"]) and is_boss_defeated(self, "Sorceress", state)))
        elif self.generation_options["enable_progressive_sparx_logic"]:
            set_indirect_rule(self, "Agent 9's Lab", lambda state: has_sparx_health(self, 2, state))
        if Spyro3LocationCategory.GEMSANITY in self.enabled_location_categories:
            for i in range(106):
                if len(self.chosen_gem_locations) == 0 or f"Agent 9's Lab: Gem {i + 1}" in self.chosen_gem_locations:
                    set_rule(
                        self.multiworld.get_location(f"Agent 9's Lab: Gem {i + 1}", self.player),
                        lambda state: are_gems_accessible(self, state)
                    )

        # Sorceress' Lair Rules
        if self.generation_options["goal"] != GoalOptions.EGG_HUNT or self.generation_options["egg_count"] > self.generation_options["sorceress_door_requirement"]:
            if not self.generation_options["logic_sorceress_early"] and self.generation_options["enable_progressive_sparx_logic"]:
                set_indirect_rule(self, "Sorceress", lambda state: (has_sparx_health(self, 3, state) or is_glitched_logic(self, state)) and state.has("Egg", self.player, self.generation_options["sorceress_door_requirement"]))
            elif not self.generation_options["logic_sorceress_early"]:
                set_indirect_rule(self, "Sorceress", lambda state: state.has("Egg", self.player, self.generation_options["sorceress_door_requirement"]))
            elif self.generation_options["enable_progressive_sparx_logic"]:
                set_indirect_rule(self, "Sorceress", lambda state: (has_sparx_health(self, 3, state) or is_glitched_logic(self, state)))

        # Bugbot Factory Rules
        if self.generation_options["goal"] != GoalOptions.EGG_HUNT or self.generation_options["egg_count"] > self.generation_options["sorceress_door_requirement"]:
            if self.generation_options["enable_progressive_sparx_logic"]:
                set_indirect_rule(self, "Bugbot Factory", lambda state: is_boss_defeated(self, "Sorceress", state) and \
                    is_level_completed(self, 'Starfish Reef', state) and \
                    (has_sparx_health(self, 3, state) or is_glitched_logic(self, state))
                )
            else:
                set_indirect_rule(self, "Bugbot Factory",
                    lambda state: is_boss_defeated(self, "Sorceress", state) and is_level_completed(self, 'Starfish Reef', state))
            # Sparx level gems are always accessible in gemsanity.


        # Super Bonus Round Rules
        if self.generation_options["goal"] != GoalOptions.EGG_HUNT or self.generation_options["egg_count"] > self.generation_options["sbr_door_egg_requirement"] and \
                (self.generation_options["egg_count"] > self.generation_options["sorceress_door_requirement"] or self.generation_options["sbr_door_gem_requirement"] <= 14800):
            # Ensure all gems are in logic.
            if self.generation_options["enable_progressive_sparx_logic"]:
                set_indirect_rule(
                    self,
                    "Super Bonus Round",
                    lambda state: state.has("Egg", self.player, self.generation_options["sbr_door_egg_requirement"]) and has_gems_for_sbr(self, state) and (has_sparx_health(self, 1, state) or is_glitched_logic(self, state))
                )
            else:
                set_indirect_rule(
                    self,
                    "Super Bonus Round",
                    lambda state: state.has("Egg", self.player, self.generation_options["sbr_door_egg_requirement"]) and has_gems_for_sbr(self, state)
                )
            if self.generation_options["powerup_lock_settings"] != PowerupLockOptions.VANILLA:
                set_rule(self.multiworld.get_location("Super Bonus Round: Woo, a secret egg. (Yin Yang)", self.player),
                         lambda state: has_total_accessible_gems(self, state, self.generation_options["sbr_door_gem_requirement"] + 5000))
                set_rule(self.multiworld.get_location("Super Bonus Round Complete", self.player),
                         lambda state: has_total_accessible_gems(self, state, self.generation_options["sbr_door_gem_requirement"] + 5000))

        # Level Gem Count rules
        for level in self.all_levels:
            if level in ["Buzz", "Spike", "Scorch", "Sorceress"]:
                continue
            max_gems = self.level_gems[level]
            if Spyro3LocationCategory.GEM_25 in self.enabled_location_categories:
                set_rule(
                    self.multiworld.get_location(f"{level}: 25% Gems", self.player),
                    lambda state, level=level, max_gems=max_gems: get_gems_accessible_in_level(self, level, state) >= max_gems / 4
                )
            if Spyro3LocationCategory.GEM_50 in self.enabled_location_categories:
                set_rule(
                    self.multiworld.get_location(f"{level}: 50% Gems", self.player),
                    lambda state, level=level, max_gems=max_gems: get_gems_accessible_in_level(self, level, state) >= max_gems / 2
                )
            if Spyro3LocationCategory.GEM_75 in self.enabled_location_categories:
                set_rule(
                    self.multiworld.get_location(f"{level}: 75% Gems", self.player),
                    lambda state, level=level, max_gems=max_gems: get_gems_accessible_in_level(self, level, state) >= 3 * max_gems / 4
                )
            if Spyro3LocationCategory.GEM in self.enabled_location_categories:
                set_rule(
                    self.multiworld.get_location(f"{level}: All Gems", self.player),
                    lambda state, level=level, max_gems=max_gems: get_gems_accessible_in_level(self, level, state) >= max_gems
                )

        # Inventory Rules
        if Spyro3LocationCategory.TOTAL_GEM in self.enabled_location_categories:
            for i in range(40):
                gems = 500 * (i + 1)
                if gems <= self.generation_options["max_total_gem_checks"] and not (self.generation_options["goal"] == GoalOptions.EGG_HUNT and gems > 14800):
                    set_rule(self.multiworld.get_location(f"Total Gems: {gems}", self.player), lambda state, gems=gems: has_total_accessible_gems(self, state, gems) or is_glitched_logic(self, state) and has_total_accessible_gems(self, state, gems, include_moneybags=False))
                else:
                    break

    # Universal Tracker Support
    @staticmethod
    def interpret_slot_data(slot_data):
        return slot_data

    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        if self.generation_options["level_lock_option"] in [LevelLockOptions.RANDOM_REQS, LevelLockOptions.ADD_REQS, LevelLockOptions.ADD_GEM_REQS]:
            spoiler_handle.write(f"\nLevel Unlock Requirements:\n")
            for level in self.level_egg_requirements.keys():
                if self.level_egg_requirements[level] != 0:
                    spoiler_handle.write(f"{level}: {self.level_egg_requirements[level]} eggs\n")
                elif self.level_gem_requirements[level] != 0:
                    spoiler_handle.write(f"{level}: {self.level_egg_requirements[level]} gems\n")

    def fill_slot_data(self) -> Dict[str, object]:
        name_to_s3_code = {item.name: item.s3_code for item in item_dictionary.values()}
        # Create the mandatory lists to generate the player's output file
        items_id = []
        items_address = []
        locations_id = []
        locations_address = []
        locations_target = []
        hints = {}
        
        for location in self.multiworld.get_filled_locations():


            if location.item.player == self.player:
                #we are the receiver of the item
                items_id.append(location.item.code)
                items_address.append(name_to_s3_code[location.item.name])


            if location.player == self.player:
                #we are the sender of the location check
                locations_address.append(item_dictionary[location_dictionary[location.name].default_item].s3_code)
                locations_id.append(location.address)
                if location.item.player == self.player:
                    locations_target.append(name_to_s3_code[location.item.name])
                else:
                    locations_target.append(0)

        if self.generation_options["zoe_gives_hints"] > 0:
            hints = generateHints(self.player, self.generation_options["zoe_gives_hints"], self)

        gemsanity_locations = []
        for loc in self.chosen_gem_locations:
            loc_id = self.location_name_to_id[loc]
            gemsanity_locations.append(loc_id)

        slot_data: Dict[str, object] = {
            "options": {
                "goal": self.options.goal.value,
                "egg_count": self.options.egg_count.value,
                "percent_extra_eggs": self.options.percent_extra_eggs.value,
                "guaranteed_items": self.options.guaranteed_items.value,
                "open_world": self.options.open_world.value,
                "level_lock_option": self.options.level_lock_option.value,
                "starting_levels_count": self.options.starting_levels_count.value,
                "sorceress_door_requirement": self.options.sorceress_door_requirement.value,
                "sbr_door_egg_requirement": self.options.sbr_door_egg_requirement.value,
                "sbr_door_gem_requirement": self.options.sbr_door_gem_requirement.value,
                "enable_25_pct_gem_checks": self.options.enable_25_pct_gem_checks.value,
                "enable_50_pct_gem_checks": self.options.enable_50_pct_gem_checks.value,
                "enable_75_pct_gem_checks": self.options.enable_75_pct_gem_checks.value,
                "enable_gem_checks": self.options.enable_gem_checks.value,
                "enable_total_gem_checks": self.options.enable_total_gem_checks.value,
                "max_total_gem_checks": self.options.max_total_gem_checks.value,
                "enable_gemsanity": self.options.enable_gemsanity.value,
                "enable_skillpoint_checks": self.options.enable_skillpoint_checks.value,
                "enable_life_bottle_checks": self.options.enable_life_bottle_checks.value,
                "sparx_power_settings": self.options.sparx_power_settings.value,
                "death_link": self.options.death_link.value,
                "moneybags_settings": self.options.moneybags_settings.value,
                "powerup_lock_settings": self.options.powerup_lock_settings.value,
                "enable_world_keys": self.options.enable_world_keys.value,
                "enable_filler_extra_lives": self.options.enable_filler_extra_lives.value,
                "enable_filler_invincibility": self.options.enable_filler_invincibility.value,
                "enable_filler_color_change": self.options.enable_filler_color_change.value,
                "enable_filler_big_head_mode": self.options.enable_filler_big_head_mode.value,
                "enable_filler_heal_sparx": self.options.enable_filler_heal_sparx.value,
                "trap_filler_percent": self.options.trap_filler_percent.value,
                "enable_trap_damage_sparx": self.options.enable_trap_damage_sparx.value,
                "enable_trap_sparxless": self.options.enable_trap_sparxless.value,
                "enable_progressive_sparx_health": self.options.enable_progressive_sparx_health.value,
                "enable_progressive_sparx_logic": self.options.enable_progressive_sparx_logic.value,
                "require_sparx_for_max_gems": self.options.require_sparx_for_max_gems.value,
                "zoe_gives_hints": self.options.zoe_gives_hints.value,
                "easy_skateboarding_lizards": self.options.easy_skateboarding_lizards.value,
                "easy_skateboarding_points": self.options.easy_skateboarding_points.value,
                "easy_skateboarding_lost_fleet": self.options.easy_skateboarding_lost_fleet.value,
                "easy_skateboarding_super_bonus_round": self.options.easy_skateboarding_super_bonus_round.value,
                "easy_boxing": self.options.easy_boxing.value,
                "easy_sheila_bombing": self.options.easy_sheila_bombing.value,
                "easy_tanks": self.options.easy_tanks.value,
                "easy_subs": self.options.easy_subs.value,
                "easy_bluto": self.options.easy_bluto.value,
                "easy_sleepyhead": self.options.easy_sleepyhead.value,
                "easy_shark_riders": self.options.easy_shark_riders.value,
                "easy_whackamole": self.options.easy_whackamole.value,
                "easy_tunnels": self.options.easy_tunnels.value,
                "no_green_rockets": self.options.no_green_rockets.value,
                "logic_sunny_sheila_early": self.options.logic_sunny_sheila_early.value,
                "logic_cloud_backwards": self.options.logic_cloud_backwards.value,
                "logic_molten_early": self.options.logic_molten_early.value,
                "logic_molten_byrd_early": self.options.logic_molten_byrd_early.value,
                "logic_molten_thieves_no_moneybags": self.options.logic_molten_thieves_no_moneybags.value,
                "logic_seashell_early": self.options.logic_seashell_early.value,
                "logic_seashell_sheila_early": self.options.logic_seashell_sheila_early.value,
                "logic_mushroom_early": self.options.logic_mushroom_early.value,
                "logic_sheila_early": self.options.logic_sheila_early.value,
                "logic_spooky_early": self.options.logic_spooky_early.value,
                "logic_spooky_no_moneybags": self.options.logic_spooky_no_moneybags.value,
                "logic_bamboo_early": self.options.logic_bamboo_early.value,
                "logic_bamboo_bentley_early": self.options.logic_bamboo_bentley_early.value,
                "logic_country_early": self.options.logic_country_early.value,
                "logic_byrd_early": self.options.logic_byrd_early.value,
                "logic_frozen_bentley_early": self.options.logic_frozen_bentley_early.value,
                "logic_frozen_cat_hockey_no_moneybags": self.options.logic_frozen_cat_hockey_no_moneybags.value,
                "logic_fireworks_early": self.options.logic_fireworks_early.value,
                "logic_fireworks_agent_9_early": self.options.logic_fireworks_agent_9_early.value,
                "logic_charmed_early": self.options.logic_charmed_early.value,
                "logic_charmed_no_moneybags": self.options.logic_charmed_no_moneybags.value,
                "logic_honey_early": self.options.logic_honey_early.value,
                "logic_bentley_early": self.options.logic_bentley_early.value,
                "logic_crystal_no_moneybags": self.options.logic_crystal_no_moneybags.value,
                "logic_desert_no_moneybags": self.options.logic_desert_no_moneybags.value,
                "logic_dino_agent_9_early": self.options.logic_dino_agent_9_early.value,
                "logic_sorceress_early": self.options.logic_sorceress_early.value,
            },
            "gemsanity_ids": gemsanity_locations,
            "hints": hints,
            "key_locked_levels": self.key_locked_levels,
            "level_egg_requirements": self.level_egg_requirements,
            "level_gem_requirements": self.level_gem_requirements,
            "enabled_hint_locations": self.enabled_hint_locations,
            "seed": self.multiworld.seed_name,  # to verify the server's multiworld
            "slot": self.multiworld.player_name[self.player],  # to connect to server
            "base_id": self.base_id,  # to merge location and items lists
            "locationsId": locations_id,
            "locationsAddress": locations_address,
            "locationsTarget": locations_target,
            "itemsId": items_id,
            "itemsAddress": items_address,
            "apworldVersion": self.ap_world_version,
        }

        return slot_data
