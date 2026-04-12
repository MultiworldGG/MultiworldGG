import math
import threading
import typing
import os
import pkgutil
import settings
import random
from typing import List, Dict, Set, Any

from .Items import (
    EOSItem,
    item_table,
    item_frequencies,
    item_table_by_id,
    item_table_by_groups,
    filler_item_table,
    filler_item_weights,
    trap_item_table,
    trap_item_weights,
    exclusive_filler_item_table,
    exclusive_filler_item_weights,
    legendary_pool_dict,
    filler_items,
    exclusive_filler_items,
    conditional_filler_useful_items,
)
from .Locations import EOS_location_table, EOSLocation, location_Dict_by_id, expanded_EOS_location_table
from .Options import EOSOptions
from .Rules import set_rules, ready_for_late_game, has_relic_shards
from BaseClasses import Tutorial, ItemClassification, Region, Location, LocationProgressType, Item
from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import set_rule
from .Client import EoSClient, game_version
from .Rom import EOSProcedurePatch, write_tokens


class EOSWeb(WebWorld):
    theme = "ocean"
    game = "Pokemon Mystery Dungeon Explorers of Sky"

    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A Guide to setting up Explorers of Sky for MultiWorld.",
            "English",
            "setup_en.md",
            "setup/en",
            ["CrypticMonkey33", "Chesyon"],
        )
    ]


class EOSSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the EoS EU rom"""

        copy_to = "POKEDUN_SORA_C2SP01_00.nds"
        description = "Explorers of Sky (EU) ROM File"
        md5s = ["6735749e060e002efd88e61560e45567"]

    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: bool = True


class EOSWorld(World):
    """
    This is for Pokemon Mystery Dungeon Explorers of Sky, a game where you inhabit a pokemon and explore
    through dungeons, solve quests, and help out other Pokemon in the colony
    """

    game = "Pokemon Mystery Dungeon Explorers of Sky"
    options: EOSOptions
    options_dataclass = EOSOptions
    web = EOSWeb()
    settings: typing.ClassVar[EOSSettings]

    item_name_to_id = {item.name: item.id for item in item_table.values()}
    location_name_to_id = {location.name: location.id for location in expanded_EOS_location_table}

    required_client_version = (0, 6, 1)
    required_server_version = (0, 6, 1)

    item_name_groups = item_table_by_groups
    disabled_locations: Set[str] = []
    extra_locations_added = 0
    mission_start_id = 1000
    excluded_locations = 0
    dimensional_scream_list = []
    dimensional_scream_list_ints: list[int] = []
    starting_se: int = 0
    slot_data_ready = threading.Event
    excluded_tag_amount: int = 0

    def get_filler_item_name(self) -> str:
        """Called when the item pool needs to be filled with additional items to match location count."""
        # logging.warning(f"World {self} is generating a filler item without custom filler pool.")
        return self.multiworld.random.choice(tuple(filler_item_table.keys()))

    def generate_early(self) -> None:
        self.slot_data_ready = threading.Event()
        if self.options.bag_on_start.value:
            item_name = "Bag Upgrade"
            self.multiworld.push_precollected(self.create_item(item_name))
        if self.options.hero_evolution.value:
            item_name = "Hero Evolution"
            self.multiworld.push_precollected(self.create_item(item_name))
        if self.options.recruit_evo.value:
            item_name = "Recruit Evolution"
            self.multiworld.push_precollected(self.create_item(item_name))
        if self.options.dojo_dungeons.value > 0:
            dojo_amount = self.options.dojo_dungeons.value
            dojo_table = item_table_by_groups["Dojo Dungeons"]
            random_open_dungeons = self.random.sample(sorted(dojo_table), k=dojo_amount)
            for item_name in random_open_dungeons:
                self.multiworld.push_precollected(self.create_item(item_name))
        if self.options.recruit.value:
            item_name = "Recruitment"
            self.multiworld.push_precollected(self.create_item(item_name))
        if self.options.team_form.value:
            item_name = "Formation Control"
            self.multiworld.push_precollected(self.create_item(item_name))
        if self.options.special_episode_sanity.value and not self.options.exclude_special.value:
            possible_se = [
                "Bidoof's Wish",
                "Igglybuff the Prodigy",
                'Today\'s "Oh My Gosh"',
                "Here Comes Team Charm!",
                "In the Future of Darkness",
            ]
            se_num = self.random.randint(0, 4)
            self.starting_se = se_num
            item_name = possible_se[se_num]
            self.multiworld.push_precollected(self.create_item(item_name))
        else:
            self.multiworld.push_precollected(self.create_item("Main Game Unlock"))

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)

        early_dungeons_region = Region("Early Dungeons", self.player, self.multiworld)
        self.multiworld.regions.append(early_dungeons_region)

        # early_dungeons_region2 = Region("Early Dungeons2", self.player, self.multiworld)
        # self.multiworld.regions.append(early_dungeons_region2)

        late_dungeons_region = Region("Late Dungeons", self.player, self.multiworld)
        self.multiworld.regions.append(late_dungeons_region)

        end_game_region = Region("Boss Dungeons", self.player, self.multiworld)
        self.multiworld.regions.append(end_game_region)

        extra_items_region = Region("Extra Items", self.player, self.multiworld)
        self.multiworld.regions.append(extra_items_region)

        rule_dungeons_region = Region("Rule Dungeons", self.player, self.multiworld)
        self.multiworld.regions.append(rule_dungeons_region)

        for location in EOS_location_table:
            if location.name == "Beach Cave":
                menu_region.locations.append(EOSLocation(self.player, location.name, location.id, menu_region))
                if "Mission" in location.group:
                    for j in range(self.options.early_mission_checks.value):
                        location_name: str = f"{location.name} Mission {j + 1}"
                        location_id = location.id + self.mission_start_id + (100 * location.id) + j
                        menu_region.locations.append(EOSLocation(self.player, location_name, location_id, menu_region))

                        self.extra_locations_added += 1
                    for j in range(self.options.early_outlaw_checks.value):
                        location_name = f"{location.name} Outlaw {j + 1}"
                        location_id = location.id + self.mission_start_id + (100 * location.id) + j + 50
                        menu_region.locations.append(EOSLocation(self.player, location_name, location_id, menu_region))

                        self.extra_locations_added += 1
            elif location.classification == "Free":
                menu_region.locations.append(EOSLocation(self.player, location.name, location.id, menu_region))
            elif location.name == "Team Name Location":
                menu_region.locations.append(EOSLocation(self.player, location.name, location.id, menu_region))
            elif location.classification == "Rank":
                rank_toid_dict = {
                    "Bronze Rank": 1,
                    "Silver Rank": 2,
                    "Gold Rank": 3,
                    "Diamond Rank": 4,
                    "Super Rank": 5,
                    "Ultra Rank": 6,
                    "Hyper Rank": 7,
                    "Master Rank": 8,
                    "Master ★ Rank": 9,
                    "Master ★★ Rank": 10,
                    "Master ★★★ Rank": 11,
                    "Guildmaster Rank": 12,
                }
                if rank_toid_dict[location.name] > self.options.max_rank:
                    # self.excluded_locations += 1
                    # continue
                    early_dungeon = EOSLocation(self.player, location.name, location.id, early_dungeons_region)
                    early_dungeon.progress_type = LocationProgressType.EXCLUDED
                    self.excluded_tag_amount += 1
                    early_dungeons_region.locations.append(early_dungeon)

                # if dialga is the goal, we can't add master star rank+
                elif self.options.goal.value == 0 and rank_toid_dict[location.name] > 8:
                    # self.excluded_locations += 1
                    # continue

                    late_dungeon = EOSLocation(self.player, location.name, location.id, late_dungeons_region)
                    late_dungeon.progress_type = LocationProgressType.EXCLUDED
                    self.excluded_tag_amount += 1
                    late_dungeons_region.locations.append(late_dungeon)

                elif rank_toid_dict[location.name] <= 8:
                    early_dungeons_region.locations.append(
                        EOSLocation(self.player, location.name, location.id, early_dungeons_region)
                    )
                else:
                    late_dungeon = EOSLocation(self.player, location.name, location.id, late_dungeons_region)
                    late_dungeons_region.locations.append(late_dungeon)

            elif location.classification in ["EarlyDungeonComplete", "EarlySubX"]:
                early_dungeons_region.locations.append(
                    EOSLocation(self.player, location.name, location.id, early_dungeons_region)
                )
                if "Mission" in location.group:
                    for j in range(self.options.early_mission_checks.value):
                        location_name = f"{location.name} Mission {j + 1}"
                        location_id = location.id + self.mission_start_id + (100 * location.id) + j
                        early_dungeons_region.locations.append(
                            EOSLocation(self.player, location_name, location_id, early_dungeons_region)
                        )

                        set_rule(
                            self.multiworld.get_location(location_name, self.player),
                            lambda state, ln=location.name, p=self.player: state.has(ln, p),
                        )
                        self.extra_locations_added += 1

                    for j in range(self.options.early_outlaw_checks.value):
                        location_name = f"{location.name} Outlaw {j + 1}"
                        location_id = location.id + self.mission_start_id + (100 * location.id) + j + 50
                        early_dungeons_region.locations.append(
                            EOSLocation(self.player, location_name, location_id, early_dungeons_region)
                        )

                        set_rule(
                            self.multiworld.get_location(location_name, self.player),
                            lambda state, ln=location.name, p=self.player: state.has(ln, p),
                        )
                        self.extra_locations_added += 1

            elif location.classification == "SpecialDungeonComplete":
                if not self.options.exclude_special.value:
                    early_dungeons_region.locations.append(
                        EOSLocation(self.player, location.name, location.id, early_dungeons_region)
                    )
                else:
                    self.excluded_locations += 1
                    continue

            elif location.classification in ["LateDungeonComplete", "LateSubX"]:
                late_dungeon = EOSLocation(self.player, location.name, location.id, late_dungeons_region)
                if self.options.goal.value == 0:  # if dialga is the goal, make the location excluded
                    self.excluded_locations += 1
                    continue

                late_dungeons_region.locations.append(late_dungeon)
                if self.options.goal.value == 1 and ("Mission" in location.group):
                    for j in range(self.options.late_mission_checks.value):
                        location_name = f"{location.name} Mission {j + 1}"
                        location_id = location.id + self.mission_start_id + (100 * location.id) + j
                        late_dungeons_region.locations.append(
                            EOSLocation(self.player, location_name, location_id, late_dungeons_region)
                        )

                        set_rule(
                            self.multiworld.get_location(f"{location.name} Mission {j + 1}", self.player),
                            lambda state, ln=location.name, p=self.player: state.has(ln, p),
                        )
                        self.extra_locations_added += 1

                    for j in range(self.options.late_outlaw_checks.value):
                        location_name = f"{location.name} Outlaw {j + 1}"
                        location_id = location.id + self.mission_start_id + (100 * location.id) + j + 50
                        late_dungeons_region.locations.append(
                            EOSLocation(self.player, location_name, location_id, late_dungeons_region)
                        )

                        set_rule(
                            self.multiworld.get_location(f"{location.name} Outlaw {j + 1}", self.player),
                            lambda state, ln=location.name, p=self.player: state.has(ln, p),
                        )

                        self.extra_locations_added += 1
            elif location.classification in ["Manaphy", "SecretRank", "Legendary", "Instrument"] or location.name in [
                "Bag Upgrade 5",
                "Recycle Shop Dungeon #4",
                "Recycle Shop Dungeon #5",
            ]:
                late_dungeon = EOSLocation(self.player, location.name, location.id, late_dungeons_region)
                if self.options.goal.value == 0:  # if dialga is the goal, make the location excluded
                    self.excluded_locations += 1
                    continue
                    # late_dungeon.progress_type = LocationProgressType.EXCLUDED
                    # Manaphy's discovery can only be collected if manaphy is in the game
                    # if location.name == "Manaphy's Discovery":
                    #    continue
                late_dungeons_region.locations.append(late_dungeon)
            elif location.classification == "SpindaDrinkEvent":
                if int(location.name[-2:]) <= self.options.drink_events:
                    menu_region.locations.append(EOSLocation(self.player, location.name, location.id, menu_region))
                else:
                    self.excluded_locations += 1
            elif location.classification == "SpindaDrink":
                if int(location.name[-2:]) <= self.options.spinda_drinks:
                    menu_region.locations.append(EOSLocation(self.player, location.name, location.id, menu_region))
                else:
                    self.excluded_locations += 1

            elif location.classification == "BossDungeonComplete":
                location_data = EOSLocation(self.player, location.name, location.id, end_game_region)
                if location.name == "Dark Crater" and self.options.goal.value == 0:
                    location_data.progress_type = LocationProgressType.EXCLUDED

                end_game_region.locations.append(location_data)
                if (self.options.goal.value == 1) and ("Mission" in location.group):
                    for j in range(self.options.late_mission_checks.value):
                        location_name = f"{location.name} Mission {j + 1}"
                        location_id = location.id + self.mission_start_id + (100 * location.id) + j
                        late_dungeons_region.locations.append(
                            EOSLocation(self.player, location_name, location_id, late_dungeons_region)
                        )

                        set_rule(
                            self.multiworld.get_location(f"{location.name} Mission {j + 1}", self.player),
                            lambda state, ln=location.name, p=self.player: state.has(ln, p),
                        )
                        self.extra_locations_added += 1

                    for j in range(self.options.late_outlaw_checks.value):
                        location_name = f"{location.name} Outlaw {j + 1}"
                        location_id = location.id + self.mission_start_id + (100 * location.id) + j + 50
                        late_dungeons_region.locations.append(
                            EOSLocation(self.player, location_name, location_id, late_dungeons_region)
                        )

                        set_rule(
                            self.multiworld.get_location(f"{location.name} Outlaw {j + 1}", self.player),
                            lambda state, ln=location.name, p=self.player: state.has(ln, p),
                        )

                        self.extra_locations_added += 1
            elif (
                (location.classification == "ProgressiveBagUpgrade")
                or (location.classification == "ShopItem")
                or (location.classification == "DojoDungeonComplete")
                or (location.classification == "SEDungeonUnlock")
            ):
                extra_items_region.locations.append(
                    EOSLocation(self.player, location.name, location.id, extra_items_region)
                )
            elif location.classification in ["RuleDungeonComplete"]:
                if self.options.long_location.value == 0:
                    self.excluded_locations += 1
                    continue
                    # location = EOSLocation(self.player, location.name, location.id, rule_dungeons_region)
                    # location.progress_type = LocationProgressType.EXCLUDED
                    # rule_dungeons_region.locations.append(location)
                else:
                    location = EOSLocation(self.player, location.name, location.id, rule_dungeons_region)
                    rule_dungeons_region.locations.append(location)

            elif location.classification in "OptionalSubX":
                if self.options.long_location.value == 0:
                    location = EOSLocation(self.player, location.name, location.id, rule_dungeons_region)
                    location.progress_type = LocationProgressType.EXCLUDED
                    self.excluded_tag_amount += 1
                    rule_dungeons_region.locations.append(location)
                else:
                    location = EOSLocation(self.player, location.name, location.id, rule_dungeons_region)
                    rule_dungeons_region.locations.append(location)

        menu_region.connect(extra_items_region)

        menu_region.connect(early_dungeons_region)

        early_dungeons_region.connect(late_dungeons_region, "Late Game Door")

        # early_dungeons_region.connect(early_dungeons_region2)

        late_dungeons_region.connect(end_game_region, "Boss Door")
        # lambda state: ready_for_final_boss(state, self.player))

        boss_region = Region("Boss Room", self.player, self.multiworld)

        boss_region.locations.append(EOSLocation(self.player, "Final Boss", None, boss_region))

        end_game_region.connect(boss_region, "End Game")
        # lambda state: state.has("Temporal Tower", self.player))
        late_dungeons_region.connect(rule_dungeons_region, "Rule Dungeons")

        self.get_location("Final Boss").place_locked_item(self.create_item("Victory"))

    def create_item(self, name: str, classification: ItemClassification = None) -> EOSItem:
        item_data = item_table[name]
        if classification is not None:
            return EOSItem(item_data.name, classification, item_data.id, self.player)
        else:
            return EOSItem(item_data.name, item_data.classification, item_data.id, self.player)

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "Goal": self.options.goal.value,
            "ServerVersion": game_version,
            "BagOnStart": self.options.bag_on_start.value,
            "Recruitment": self.options.recruit.value,
            "TeamFormation": self.options.team_form.value,
            "LevelScaling": self.options.level_scale.value,
            "RecruitmentEvolution": self.options.recruit_evo.value,
            "DojoDungeonsRandomization": self.options.dojo_dungeons.value,
            "ShardFragmentAmount": self.options.required_fragments.value,
            "ExtraShardsAmount": self.options.total_shards.value,
            "EarlyMissionsAmount": self.options.early_mission_checks.value,
            "EarlyOutlawsAmount": self.options.early_outlaw_checks.value,
            "LateMissionsAmount": self.options.late_mission_checks.value,
            "LateOutlawsAmount": self.options.late_outlaw_checks.value,
            "TypeSanity": self.options.type_sanity.value,
            "StarterOption": self.options.starter_option.value,
            "IQScaling": self.options.iq_scaling.value,
            "XPScaling": self.options.xp_scaling.value,
            "RequiredInstruments": self.options.req_instruments.value,
            "ExtraInstruments": self.options.total_instruments.value,
            "HeroEvolution": self.options.hero_evolution.value,
            "Deathlink": self.options.deathlink.value,
            "DeathlinkType": self.options.deathlink_type.value,
            "LegendaryAmount": self.options.legendaries.value,
            "AllowedLegendaries": self.options.allowed_legendaries.value,
            "SkyPeakType": self.options.sky_peak_type.value,
            "SpecialEpisodeSanity": self.options.special_episode_sanity.value,
            "HintLocationList": self.dimensional_scream_list_ints,
            "TrapsAllowed": self.options.allow_traps.value,
            "InvisibleTraps": self.options.invisible_traps.value,
            "TrapPercentage": self.options.trap_percent.value,
            "LongLocations": self.options.long_location.value,
            "CursedAegisCave": self.options.cursed_aegis_cave.value,
            "DrinkEvents": self.options.drink_events.value,
            "SpindaDrinks": self.options.spinda_drinks.value,
            "ExcludeSpecial": self.options.exclude_special.value,
            "AllowMissionsEarly": self.options.early_mission_floors.value,
            "MaxRank": self.options.max_rank.value,
            "GuestScaling": self.options.guest_scaling.value,
            "MoveShortcuts": self.options.move_shortcuts.value,
            "StartInventoryFromPool": self.options.start_inventory_from_pool.value,
        }

    def create_items(self) -> None:
        required_items = []
        filler_items_pool = []
        exclusive_filler_pool = []
        non_unique_trap_items = []
        non_unique_trap_weights = []
        unique_trap_items = []
        unique_trap_weights = []
        instruments = []
        item_weights = []
        conditional_count = 0
        # conditional_item_table = []
        if self.options.goal.value == 1:
            instruments_to_add = 0
            if self.options.total_instruments.value < self.options.req_instruments.value:
                instruments_to_add = self.options.req_instruments.value
            else:
                instruments_to_add = self.options.total_instruments.value

            instrument_table = item_table_by_groups["Instrument"]
            instruments = self.random.sample(sorted(instrument_table), instruments_to_add)
            for item in instruments:
                required_items.append(self.create_item(item, ItemClassification.progression_skip_balancing))

        precollected = [item.name for item in self.multiworld.precollected_items[self.player]]

        precollected_from_pool = []
        for item, value in self.options.start_inventory_from_pool.value.items():
            for _ in range(value):
                precollected_from_pool += [item]

        precollected_added = []
        for item, value in self.options.start_inventory.value.items():
            for _ in range(value):
                precollected_added += [item]
        # precollected_from_pool = [item for item, value in self.multiworld.start_inventory_from_pool[self.player].value.items()]
        # precollected_added = [item for item, value in self.multiworld.start_inventory[self.player].value.items()]
        relics_to_add = 0
        if self.options.required_fragments.value > self.options.total_shards.value:
            relics_to_add = self.options.required_fragments.value
        else:
            relics_to_add = self.options.total_shards.value

        for i in range(relics_to_add):
            required_items.append(
                self.create_item("Relic Fragment Shard", ItemClassification.progression_skip_balancing)
            )

        if self.options.goal == 1:
            required_items.append(self.create_item("Manaphy", ItemClassification.progression))
            required_items.append(self.create_item("Secret Rank", ItemClassification.progression))
        else:
            # self.excluded_locations += 1
            test = 0
        if self.options.goal.value == 1 and (
            self.options.legendaries.value > len(self.options.allowed_legendaries.value)
        ):
            for item in self.options.allowed_legendaries.value:
                required_items.append(self.create_item(item, ItemClassification.filler))
        elif self.options.goal.value == 1:
            new_list = self.random.sample(
                sorted(self.options.allowed_legendaries.value), self.options.legendaries.value
            )
            for item in new_list:
                required_items.append(self.create_item(item, ItemClassification.filler))

        for item_name in item_table:
            # if (item_name == "Dark Crater") and (self.options.goal.value == 1):
            # continue
            if item_name in item_frequencies:
                freq = 0

                freq = item_frequencies.get(item_name, 1)

                freq = max(
                    freq
                    - precollected.count(item_name)
                    + precollected_added.count(item_name)
                    + precollected_from_pool.count(item_name),
                    0,
                )
                required_items += [self.create_item(item_name) for _ in range(freq)]
            elif "Special Dungeons" in item_table[item_name].group:
                if self.options.exclude_special.value:
                    continue
                else:
                    classification = ItemClassification.progression
                    required_items.append(self.create_item(item_name, classification))
            elif item_table[item_name].name == "Main Game Unlock":
                if not self.options.special_episode_sanity.value or self.options.exclude_special.value:
                    continue
                else:
                    required_items.append(self.create_item(item_name, ItemClassification.progression))
            elif item_table[item_name].name in ["Victory", "Relic Fragment Shard"]:
                continue
            elif "Legendary" in item_table[item_name].group:
                continue
            elif "Instrument" in item_table[item_name].group:
                continue
            elif "Rank" in item_table[item_name].group:
                continue
            elif item_table[item_name].name in conditional_filler_useful_items:
                conditional_count += 1
                # conditional_item_table.append(item_name)
                continue
            elif item_table[item_name].classification == ItemClassification.filler:
                if item_name in ["Gold Ribbon"]:
                    continue
                if "Exclusive" in item_table[item_name].group:
                    exclusive_filler_pool.append(self.create_item(item_name, ItemClassification.filler))
                else:
                    filler_items_pool.append(self.create_item(item_name, ItemClassification.filler))

            elif item_table[item_name].classification == ItemClassification.trap:
                if "Late" in item_table[item_name].group and self.options.goal.value == 0:
                    continue
                elif "Unique" in item_table[item_name].group:
                    unique_trap_items.append(self.create_item(item_name, ItemClassification.trap))
                    unique_trap_weights.append(item_table[item_name].start_number)
                else:
                    non_unique_trap_items.append(self.create_item(item_name, ItemClassification.trap))
                    non_unique_trap_weights.append(item_table[item_name].start_number)

            elif item_table[item_name].classification == ItemClassification.progression:
                classification = ItemClassification.progression
                if (self.options.goal.value == 0) and "LateDungeons" in item_table[item_name].group:
                    continue
                    # classification = ItemClassification.useful

                if (self.options.long_location.value == 0) and "RuleDungeons" in item_table[item_name].group:
                    continue

                if "Aegis" in item_table[item_name].group:
                    if self.options.goal.value == 0:
                        # classification = ItemClassification.useful
                        continue
                    else:
                        classification = ItemClassification.progression
                    if self.options.cursed_aegis_cave.value == 0:
                        if item_name == "Progressive Seal":
                            for i in range(3):
                                required_items.append(self.create_item(item_name, classification))
                                continue
                        else:
                            continue
                    else:
                        if item_name == "Progressive Seal":
                            continue
                        else:
                            required_items.append(self.create_item(item_name, classification))
                            continue

                if "SkyPeak" in item_table[item_name].group:
                    if self.options.sky_peak_type.value == 1:
                        if item_name == "Progressive Sky Peak":
                            if self.options.goal.value == 0:
                                continue
                                # classification = ItemClassification.useful
                            else:
                                classification = ItemClassification.progression
                            for i in range(10):
                                required_items.append(self.create_item(item_name, classification))
                            continue
                        else:
                            continue
                    elif self.options.sky_peak_type.value == 2:
                        if item_name == "Progressive Sky Peak":
                            continue
                        else:
                            if self.options.goal.value == 0:
                                # classification = ItemClassification.useful
                                continue
                            else:
                                classification = ItemClassification.progression
                    elif self.options.sky_peak_type.value == 3:
                        if item_name == "1st Station Pass":
                            if self.options.goal.value == 0:
                                continue
                                # classification = ItemClassification.useful
                            else:
                                classification = ItemClassification.progression

                        else:
                            continue

                required_items.append(self.create_item(item_name, classification))

            else:
                required_items.append(self.create_item(item_name, ItemClassification.useful))

        remaining = (
            len(EOS_location_table)
            + self.extra_locations_added
            - len(required_items)
            - conditional_count
            - 1
            - self.excluded_locations
        )  # subtracting 1 for the event check
        for i in range(len(conditional_filler_useful_items)):
            if (i <= (self.excluded_tag_amount - remaining)) and (remaining < self.excluded_tag_amount):
                required_items.append(self.create_item(conditional_filler_useful_items[i], ItemClassification.filler))
            else:
                required_items.append(self.create_item(conditional_filler_useful_items[i], ItemClassification.useful))

        self.multiworld.itempool += required_items

        item_weights += filler_item_weights
        for i in range(4):
            filler_items_pool += filler_items_pool
            non_unique_trap_items += non_unique_trap_items
            item_weights += item_weights
            non_unique_trap_weights += non_unique_trap_weights
        filler_items_pool += exclusive_filler_pool
        item_weights += exclusive_filler_item_weights
        all_traps = []
        all_traps += non_unique_trap_items
        all_traps += unique_trap_items
        all_trap_weights = []
        all_trap_weights += non_unique_trap_weights
        all_trap_weights += unique_trap_weights

        if self.options.allow_traps.value in [1, 2]:
            filler_items_toadd = math.ceil(remaining * (100 - self.options.trap_percent) / 100)
            traps_toadd = math.floor(remaining * self.options.trap_percent / 100)
            self.multiworld.itempool += [
                self.create_item(filler_item.name)
                for filler_item in self.random.sample(filler_items_pool, filler_items_toadd, counts=item_weights)
            ]
            self.multiworld.itempool += [
                self.create_item(trap.name)
                for trap in self.random.sample(all_traps, traps_toadd, counts=all_trap_weights)
            ]

        else:
            self.multiworld.itempool += [
                self.create_item(filler_item.name)
                for filler_item in self.random.sample(filler_items_pool, remaining, counts=item_weights)
            ]

        idek_var = self.excluded_tag_amount
        wtf_items_list = [item.name for item in self.multiworld.itempool]
        excluded_location_list = [
            location.name
            for location in self.multiworld.get_locations(self.player)
            if location.progress_type is LocationProgressType.EXCLUDED
        ]
        test = 0

    def set_rules(self) -> None:
        set_rules(self, self.disabled_locations)
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def generate_output(self, output_directory: str) -> None:
        try:
            patch = EOSProcedurePatch(player=self.player, player_name=self.multiworld.player_name[self.player])
            patch.write_file("base_patch.bsdiff4", pkgutil.get_data(__name__, "data/archipelago-base.bsdiff"))
            hint_item_list: list[Location] = []
            self.dimensional_scream_list = self.hint_locations()
            self.dimensional_scream_list_ints = [k.address for k in self.dimensional_scream_list]
        except Exception:
            raise
        finally:
            self.slot_data_ready.set()

        for i in range(10):
            hint_item_list += [self.multiworld.get_location(f"Shop Item {1 + i}", self.player)]
        write_tokens(self, patch, hint_item_list, self.dimensional_scream_list, self.starting_se + 1)
        rom_path = os.path.join(
            output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}{patch.patch_file_ending}"
        )
        patch.write(rom_path)

    def hint_locations(self) -> list[Location]:
        hint_loc = []
        filler = 5
        useful = 6
        progressive = 9
        min_internal_progressive = 4
        max_external_progressive = progressive - min_internal_progressive
        sky_dungeons = []
        external_items = []
        extra_useful_items = []
        extra_filler_items = []
        important_sky_items = [
            "Icy Flute",
            "Fiery Drum",
            "Terra Cymbal",
            "Aqua-Monica",
            "Rock Horn",
            "Grass Cornet",
            "Sky Melodica",
            "Stellar Symphony",
            "Null Bagpipes",
            "Glimmer Harp",
            "Toxic Sax",
            "Biting Bass",
            "Knockout Bell",
            "Spectral Chimes",
            "Liar's Lyre",
            "Charge Synth",
            "Norma-ccordion",
            "Psychic Cello",
            "Dragu-teki",
            "Steel Guitar",
            "Relic Fragment Shard",
        ]
        location_list = list(self.multiworld.get_locations(self.player))
        random.shuffle(location_list)
        for location in location_list:
            if location.address is not None and location.item:
                if filler <= 0 and useful <= 0 and progressive <= 0:
                    break
                elif progressive > 0 and location.item.advancement:
                    if location.item.player == self.player and location.item.name not in important_sky_items:
                        sky_dungeons.append(location)
                        continue
                    if location.item.player != self.player:
                        if max_external_progressive > 0:
                            hint_loc.append(location)
                            max_external_progressive -= 1
                            progressive -= 1
                        else:
                            external_items.append(location)
                            continue
                    if location.item.player == self.player and location.item.name in important_sky_items:
                        hint_loc.append(location)
                        progressive -= 1
                elif filler > 0 and not (location.item.advancement or location.item.useful):
                    hint_loc.append(location)
                    filler -= 1
                elif not (location.item.advancement or location.item.useful):
                    extra_filler_items.append(location)
                elif useful > 0 and location.item.useful:
                    hint_loc.append(location)
                    useful -= 1
                elif location.item.useful:
                    extra_useful_items.append(location)
        if progressive > 0:
            for i in range(progressive):
                if i < len(sky_dungeons):
                    hint_loc.append(sky_dungeons[i])
                else:
                    if i - len(sky_dungeons) < len(external_items):
                        hint_loc.append(external_items[i - len(sky_dungeons)])
                    else:
                        if i - len(sky_dungeons) - len(external_items) < len(extra_useful_items):
                            hint_loc.append(extra_useful_items[i - len(sky_dungeons) - len(external_items)])
                        else:
                            if i - len(sky_dungeons) - len(external_items) - len(extra_useful_items) < len(
                                extra_filler_items
                            ):
                                hint_loc.append(
                                    extra_filler_items[
                                        i - len(sky_dungeons) - len(external_items) - len(extra_useful_items)
                                    ]
                                )
                            else:
                                break

        return hint_loc

    def modify_multidata(self, multidata: Dict[str, Any]) -> None:
        self.slot_data_ready.wait()
        slot = self.player
        if self.dimensional_scream_list_ints:
            multidata["slot_data"][slot]["HintLocationList"] = self.dimensional_scream_list_ints
