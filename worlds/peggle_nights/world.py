import logging

from typing import Any, Dict, List, Optional, TextIO, Tuple

from BaseClasses import Item, ItemClassification, Location, Region, Tutorial

from Options import OptionError

from worlds.AutoWorld import WebWorld, World

from .data.item_data import PeggleNightsItemData, item_data
from .data.location_data import PeggleNightsLocationData, location_data
from .data.mapping_data import base_scores

from .data_funcs import (
    id_to_goals,
    id_to_master_selection_modes,
    id_to_requirement_modes,
    item_names_to_id,
    item_groups,
    location_groups,
    location_names_to_id,
    locations_with_tag,
    location_access_rule_for,
)

from .enums import (
    PeggleNightsAPGoals,
    PeggleNightsAPItems,
    PeggleNightsAPMasterSelectionModes,
    PeggleNightsAPRequirementModes,
    PeggleNightsAPTags,
    PeggleNightsAPUsefulItems,
    PeggleNightsCharacters,
    PeggleNightsLevels,
)

from .options import PeggleNightsOptions, option_groups


class PeggleNightsItem(Item):
    game = "Peggle Nights"


class PeggleNightsLocation(Location):
    game = "Peggle Nights"


class PeggleNightsWebWorld(WebWorld):
    theme: str = "partyTime"

    tutorials: List[Tutorial] = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the Peggle Nights randomizer connected to a MultiworldGG Multiworld",
            "English",
            "setup_en.md",
            "setup/en",
            ["Serpent.AI"],
        )
    ]

    option_groups = option_groups


class PeggleNightsWorld(World):
    """
    Peggle Nights expands the pachinko-inspired formula with a nocturnal theme, introducing new challenges that take
    place within the dreamscapes of the Peggle Masters. Featuring a new Master, Marina, and her electricity-based
    power-up, the game offers additional levels and trials that demand refined skill and tactical shot-planning.
    """

    options_dataclass = PeggleNightsOptions
    options: PeggleNightsOptions

    game = "Peggle Nights"

    item_name_to_id = item_names_to_id()
    location_name_to_id = location_names_to_id()

    item_name_groups = item_groups()
    location_name_groups = location_groups()

    required_client_version: Tuple[int, int, int] = (0, 6, 5)

    web = PeggleNightsWebWorld()

    filler_item_names: List[str] = item_groups()["Filler Item"]

    # Options
    goal: PeggleNightsAPGoals
    shadow_pegs_required: int
    shadow_pegs_total: int
    include_full_clears: bool
    level_count: int
    level_selection: Dict[PeggleNightsLevels, bool]
    master_count: int
    master_selection: Dict[PeggleNightsCharacters, bool]
    master_selection_mode: PeggleNightsAPMasterSelectionModes
    maximum_starting_ball_count: int
    target_score_requirement_mode: PeggleNightsAPRequirementModes
    target_score_requirement_percentage: int
    useful_item_percentage: int
    useful_item_weights: Dict[PeggleNightsAPUsefulItems, int]

    # Generation
    selected_masters: List[PeggleNightsCharacters]
    selected_starter_master: PeggleNightsCharacters

    selected_levels: List[PeggleNightsLevels]
    selected_starter_level: PeggleNightsLevels
    selected_goal_level: Optional[PeggleNightsLevels] = None

    target_scores: Dict[PeggleNightsLevels, List[int]]

    # Metadata
    target_score_ratios: Dict[PeggleNightsLevels, float]

    # Universal Tracker
    ut_can_gen_without_yaml: bool = True

    @property
    def is_universal_tracker(self) -> bool:
        return hasattr(self.multiworld, "re_gen_passthrough")

    def generate_early(self) -> None:
        self.goal = id_to_goals()[self.options.goal.value]

        self.level_count = self.options.level_count.value

        self.shadow_pegs_required = self.options.shadow_pegs_required.value
        self.shadow_pegs_total = self.options.shadow_pegs_total.value

        if self.shadow_pegs_total > (self.level_count * 2):
            self.shadow_pegs_total = self.level_count * 2

            logging.warning(
                f"Peggle Nights: {self.player_name} has more total shadow pegs than allowable with the selected "
                f"number of levels. Adjusting total shadow pegs to {self.shadow_pegs_total}..."
            )

        if self.shadow_pegs_required > self.shadow_pegs_total:
            self.shadow_pegs_required = self.shadow_pegs_total

            logging.warning(
                f"Peggle Nights: {self.player_name} has more required shadow pegs than total shadow pegs. "
                "Adjusting required shadow pegs to match total shadow pegs..."
            )

        master_pool: List[PeggleNightsCharacters] = list()

        master_name: str
        is_enabled: bool
        for master_name, is_enabled in self.options.master_selection.value.items():
            if is_enabled:
                master_pool.append(PeggleNightsCharacters(master_name))

        master_pool = list(sorted(master_pool, key=lambda m: m.value))

        if not len(master_pool):
            raise OptionError(
                f"Peggle Nights: {self.player_name} must have at least 1 Master selected to play. "
                "All of their Masters are set to False."
            )

        self.master_selection_mode = id_to_master_selection_modes()[self.options.master_selection_mode.value]
        self.master_count = min(self.options.master_count.value, len(master_pool))

        if self.master_selection_mode == PeggleNightsAPMasterSelectionModes.SINGLE_MASTER:
            self.master_count = 1

            master: PeggleNightsCharacters = self.random.choice(master_pool)

            self.selected_masters = [master]
            self.selected_starter_master = master
        else:
            masters: List[PeggleNightsCharacters] = self.random.sample(master_pool, self.master_count)

            self.selected_masters = masters
            self.selected_starter_master = masters[0]

        level_pool: List[PeggleNightsLevels] = list()

        level_name: str
        is_enabled: bool
        for level_name, is_enabled in self.options.level_selection.value.items():
            if is_enabled:
                level_pool.append(PeggleNightsLevels(level_name))

        level_pool = list(sorted(level_pool, key=lambda l: l.value))

        if len(level_pool) < 5:
            raise OptionError(
                f"Peggle Nights: {self.player_name} must have at least 5 levels selected to play. "
                f"They only have {len(level_pool)} selected."
            )

        if self.level_count > len(level_pool):
            self.level_count = len(level_pool)

            logging.warning(
                f"Peggle Nights: {self.player_name} has a level count higher than their selected level pool. "
                "Adjusting level count to match the size of their level pool..."
            )

        self.random.shuffle(level_pool)

        level_pool = level_pool[:self.level_count]

        if self.goal == PeggleNightsAPGoals.SHADOW_PEGS_FINAL_LEVEL:
            self.selected_goal_level = level_pool[-1]
            self.selected_levels = level_pool[:-1]
        else:
            self.selected_levels = level_pool[:]

        self.selected_starter_level = self.selected_levels[0]

        self.include_full_clears = bool(self.options.include_full_clears.value)

        self.target_score_requirement_mode = id_to_requirement_modes()[
            self.options.target_score_requirement_mode.value
        ]

        self.target_score_requirement_percentage = self.options.target_score_requirement_percentage.value

        self.target_scores = dict()
        self.target_score_ratios = dict()

        level: PeggleNightsLevels
        for level in (self.selected_levels + [self.selected_goal_level]):
            if level is None or level == self.selected_goal_level:
                continue

            if self.target_score_requirement_mode == PeggleNightsAPRequirementModes.SAME_FOR_ALL_LEVELS:
                self.target_score_ratios[level] = round(self.target_score_requirement_percentage / 100.0, 2)

                adjusted_scores: List[int] = [
                    round(int(score * (self.target_score_requirement_percentage / 100)), -2) for score in base_scores
                ]
            elif self.target_score_requirement_mode == PeggleNightsAPRequirementModes.RANDOM_PER_LEVEL:
                random_percentage: int = self.random.randint(50, self.target_score_requirement_percentage)

                self.target_score_ratios[level] = round(random_percentage / 100.0, 2)

                adjusted_scores: List[int] = [
                    round(int(score * (random_percentage / 100)), -2) for score in base_scores
                ]
            else:
                adjusted_scores: List[int] = base_scores[:]

            self.target_scores[level] = adjusted_scores

        self.maximum_starting_ball_count = self.options.maximum_starting_ball_count.value

        self.useful_item_percentage = self.options.useful_item_percentage.value

        self.useful_item_weights = {
            PeggleNightsAPUsefulItems.FEVER_METER_BONUS: 1,
            PeggleNightsAPUsefulItems.FULL_CLEAR_DISCOUNT: 1,
            PeggleNightsAPUsefulItems.SCORE_MULTIPLIER: 1,
            PeggleNightsAPUsefulItems.TARGET_SCORE_DISCOUNT: 1,
        }

        item_name: str
        weight: int
        for item_name, weight in self.options.useful_item_weights.value.items():
            try:
                enum_item: PeggleNightsAPUsefulItems = PeggleNightsAPUsefulItems(item_name)
            except ValueError:
                continue

            if isinstance(weight, int) and weight >= 1:
                self.useful_item_weights[enum_item] = weight

        # Universal Tracker Support
        if self.is_universal_tracker:
            self._apply_universal_tracker_passthrough()

    def create_regions(self) -> None:
        # Menu
        region_menu: Region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(region_menu)

        # Endgame
        region_endgame: Region = Region("Endgame", self.player, self.multiworld)

        victory_location: PeggleNightsLocation = PeggleNightsLocation(
            self.player,
            "Victory",
            None,
            region_endgame,
        )

        victory_location.place_locked_item(
            PeggleNightsItem(
                "Victory",
                ItemClassification.progression,
                None,
                self.player,
            )
        )

        region_endgame.locations.append(victory_location)

        if self.goal == PeggleNightsAPGoals.SHADOW_PEGS_FINAL_LEVEL:
            region_menu.connect(
                region_endgame,
                rule=lambda state: (
                    state.has(PeggleNightsAPItems.SHADOW_PEG.value, self.player, self.shadow_pegs_required) and
                    state.has(f"Level Unlock: {self.selected_goal_level.value}", self.player) and
                    state.has(PeggleNightsAPItems.PROGRESSIVE_FEVER_METER.value, self.player, 4)
                )
            )
        elif self.goal == PeggleNightsAPGoals.SHADOW_PEG_HUNT:
            region_menu.connect(
                region_endgame,
                rule=lambda state: state.has(PeggleNightsAPItems.SHADOW_PEG.value, self.player, self.shadow_pegs_required)
            )

        # Levels
        level: PeggleNightsLevels
        for level in (self.selected_levels + [self.selected_goal_level]):
            if level is None:
                continue

            region_level: Region = Region(f"Level: {level.value}", self.player, self.multiworld)

            level_tag: PeggleNightsAPTags = eval(f"PeggleNightsAPTags.{level.name}_LOCATION")
            level_location_names: List[str] = locations_with_tag(level_tag)

            location_name: str
            for location_name in level_location_names:
                data: PeggleNightsLocationData = location_data[location_name]

                if not self.include_full_clears and PeggleNightsAPTags.FULL_CLEAR_LOCATION in data.tags:
                    continue

                if level == self.selected_goal_level and PeggleNightsAPTags.LEVEL_CLEAR_LOCATION not in data.tags:
                    continue

                location: PeggleNightsLocation = PeggleNightsLocation(
                    self.player,
                    location_name,
                    data.archipelago_id,
                    region_level,
                )

                location_access_rule: str = location_access_rule_for(location_name, self.player)

                if "Target Score (Mid)" in location_name:
                    location_access_rule = location_access_rule.replace(
                        "999",
                        str(round((self.maximum_starting_ball_count - 5) / 2))
                    )
                elif "Target Score (High)" in location_name:
                    location_access_rule = location_access_rule.replace(
                        "999",
                        str(self.maximum_starting_ball_count - 5)
                    )
                elif "Full Clear" in location_name:
                    location_access_rule = location_access_rule.replace(
                        "999",
                        str(self.maximum_starting_ball_count - 5)
                    )

                if location_access_rule != "lambda state: True":
                    location.access_rule = eval(location_access_rule)

                region_level.locations.append(location)

            if level == self.selected_goal_level:
                region_menu.connect(
                    region_level,
                    rule=lambda state, l=level: state.has(f"Level Unlock: {l.value}", self.player) and
                    state.has(PeggleNightsAPItems.SHADOW_PEG.value, self.player, self.shadow_pegs_required)
                )
            else:
                region_menu.connect(
                    region_level,
                    rule=lambda state, l=level: state.has(f"Level Unlock: {l.value}", self.player)
                )

            region_level.connect(region_menu)

            self.multiworld.regions.append(region_level)

    def create_items(self) -> None:
        ## Precollect
        items_to_precollect: List[str] = list()

        # Starting Master
        items_to_precollect.append(f"Master Unlock: {self.selected_starter_master.value}")

        # Starting Level
        items_to_precollect.append(f"Level Unlock: {self.selected_starter_level.value}")

        ## Item Pool
        item_pool: List[PeggleNightsItem] = list()

        # Shadow Pegs
        i: int
        for i in range(self.shadow_pegs_total):
            item: PeggleNightsItem = self.create_item(PeggleNightsAPItems.SHADOW_PEG.value)

            if i >= self.shadow_pegs_required:
                item.classification = ItemClassification.useful

            item_pool.append(item)

        # Progressive Items
        for _ in range(4):
            item_pool.append(self.create_item(PeggleNightsAPItems.PROGRESSIVE_FEVER_METER.value))

        for _ in range(self.maximum_starting_ball_count - 5):
            item_pool.append(self.create_item(PeggleNightsAPItems.PROGRESSIVE_STARTING_BALL_INCREASE.value))

        # Character Unlocks
        character: PeggleNightsCharacters
        for character in self.selected_masters:
            if character == self.selected_starter_master:
                continue

            item_pool.append(self.create_item(f"Master Unlock: {character.value}"))

        # Level Unlocks + Prepare Useful Item Pool
        useful_item_pool: List[str] = list()

        level: PeggleNightsLevels
        for level in self.selected_levels:
            if level != self.selected_starter_level:
                item_pool.append(self.create_item(f"Level Unlock: {level.value}"))

            useful_item_pool.append(f"{PeggleNightsAPUsefulItems.FEVER_METER_BONUS.value}: {level.value}")
            useful_item_pool.append(f"{PeggleNightsAPUsefulItems.SCORE_MULTIPLIER.value}: {level.value}")
            useful_item_pool.append(f"{PeggleNightsAPUsefulItems.TARGET_SCORE_DISCOUNT.value}: {level.value}")

            if self.include_full_clears:
                useful_item_pool.append(f"{PeggleNightsAPUsefulItems.FULL_CLEAR_DISCOUNT.value}: {level.value}")

        if self.selected_goal_level is not None:
            item_pool.append(self.create_item(f"Level Unlock: {self.selected_goal_level.value}"))

        # Filler / Useful Replacements
        total_location_count: int = len(self.multiworld.get_unfilled_locations(self.player))
        to_fill_location_count: int = total_location_count - len(item_pool)

        item_name: str
        for item_name in self._generate_filler_useful_item_pool(to_fill_location_count, useful_item_pool):
            item_pool.append(self.create_item(item_name))

        self.multiworld.itempool += item_pool

        item: str
        for item in items_to_precollect:
            self.multiworld.push_precollected(self.create_item(item))

    def create_item(self, name: str) -> PeggleNightsItem:
        data: PeggleNightsItemData = item_data[name]

        return PeggleNightsItem(
            name,
            data.classification,
            data.archipelago_id,
            self.player,
        )

    def generate_basic(self) -> None:
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data: Dict[str, Any] = self.options.as_dict(
            "goal",
            "shadow_pegs_total",
            "shadow_pegs_required",
            "master_selection_mode",
            "master_selection",
            "master_count",
            "level_selection",
            "level_count",
            "include_full_clears",
            "target_score_requirement_mode",
            "target_score_requirement_percentage",
            "maximum_starting_ball_count",
            "useful_item_percentage",
            "useful_item_weights",
        )

        slot_data["selected_masters"] = [master.value for master in self.selected_masters]
        slot_data["selected_starter_master"] = self.selected_starter_master.value

        slot_data["selected_levels"] = [level.value for level in self.selected_levels]
        slot_data["selected_starter_level"] = self.selected_starter_level.value

        if self.selected_goal_level is not None:
            slot_data["selected_goal_level"] = self.selected_goal_level.value

        slot_data["target_scores"] = {
            level.value: self.target_scores[level] for level in self.target_scores
        }

        # Relay generate_early Overrides
        if slot_data["shadow_pegs_total"] != self.shadow_pegs_total:
            slot_data["shadow_pegs_total"] = self.shadow_pegs_total

        if slot_data["shadow_pegs_required"] != self.shadow_pegs_required:
            slot_data["shadow_pegs_required"] = self.shadow_pegs_required

        if slot_data["master_count"] != self.master_count:
            slot_data["master_count"] = self.master_count

        level_count: int = len(self.selected_levels)

        if self.selected_goal_level is not None:
            level_count += 1

        if slot_data["level_count"] != level_count:
            slot_data["level_count"] = level_count

        slot_data["useful_item_weights"] = {
            item.value: weight for item, weight in self.useful_item_weights.items()
        }

        slot_data["target_score_ratios"] = {
            level.value: self.target_score_ratios[level] for level in self.target_score_ratios.keys()
        }

        return slot_data

    def write_spoiler_header(self, spoiler_handle: TextIO) -> None:
        join_string: str = "\n  "

        if len(self.selected_masters) == 1:
            spoiler_handle.write(f"\nSelected Master: {self.selected_starter_master.value}")
        else:
            spoiler_handle.write(f"\nStarting Master: {self.selected_starter_master.value}")
            spoiler_handle.write(f"\n\nUnlockable Masters:\n  {join_string.join(sorted([m.value for m in self.selected_masters[1:]]))}")

        spoiler_handle.write(f"\n\nStarting Level: {self.selected_starter_level.value}")
        spoiler_handle.write(f"\n\nUnlockable Levels:\n  {join_string.join(sorted([l.value for l in self.selected_levels[1:]]))}")

        if self.selected_goal_level is not None:
            spoiler_handle.write(f"\n\nGoal Level: {self.selected_goal_level.value}")

        spoiler_handle.write(f"\n\nTarget Scores:\n  {join_string.join([f'{t.value} ({self.target_score_ratios[t]}x): {self.target_scores[t]}' for t in self.target_scores])}")

    def get_filler_item_name(self) -> str:
        return self.random.choice(self.filler_item_names)

    @staticmethod
    def interpret_slot_data(slot_data: Dict[str, Any]) -> Dict[str, Any]:
        slot_data["goal"] = id_to_goals()[slot_data["goal"]]
        slot_data["master_selection_mode"] = id_to_master_selection_modes()[slot_data["master_selection_mode"]]
        slot_data["target_score_requirement_mode"] = id_to_requirement_modes()[slot_data["target_score_requirement_mode"]]

        slot_data["useful_item_weights"] = {
            PeggleNightsAPUsefulItems(item_name): weight for item_name, weight in slot_data["useful_item_weights"].items()
        }

        slot_data["selected_masters"] = [PeggleNightsCharacters(master_name) for master_name in slot_data["selected_masters"]]
        slot_data["selected_starter_master"] = PeggleNightsCharacters(slot_data["selected_starter_master"])

        slot_data["selected_levels"] = [PeggleNightsLevels(level_name) for level_name in slot_data["selected_levels"]]
        slot_data["selected_starter_level"] = PeggleNightsLevels(slot_data["selected_starter_level"])

        if "selected_goal_level" in slot_data and slot_data["selected_goal_level"] is not None:
            slot_data["selected_goal_level"] = PeggleNightsLevels(slot_data["selected_goal_level"])

        slot_data["target_scores"] = {
            PeggleNightsLevels(level_name): scores for level_name, scores in slot_data["target_scores"].items()
        }

        slot_data["target_score_ratios"] = {
            PeggleNightsLevels(level_name): ratio for level_name, ratio in slot_data["target_score_ratios"].items()
        }

        return slot_data

    def _apply_universal_tracker_passthrough(self) -> None:
        if "Peggle Nights" in self.multiworld.re_gen_passthrough:
            passthrough: Dict[str, Any] = self.multiworld.re_gen_passthrough["Peggle Nights"]

            self.goal = passthrough["goal"]
            self.level = passthrough["level_count"]
            self.shadow_pegs_required = passthrough["shadow_pegs_required"]
            self.shadow_pegs_total = passthrough["shadow_pegs_total"]
            self.master_selection_mode = passthrough["master_selection_mode"]
            self.master_count = passthrough["master_count"]
            self.selected_masters = passthrough["selected_masters"]
            self.selected_starter_master = passthrough["selected_starter_master"]
            self.selected_levels = passthrough["selected_levels"]
            self.selected_goal_level = passthrough.get("selected_goal_level")
            self.selected_starter_level = passthrough["selected_starter_level"]
            self.include_full_clears = passthrough["include_full_clears"]
            self.target_score_requirement_mode = passthrough["target_score_requirement_mode"]
            self.target_score_requirement_percentage = passthrough["target_score_requirement_percentage"]
            self.target_scores = passthrough["target_scores"]
            self.target_score_ratios = passthrough["target_score_ratios"]
            self.maximum_starting_ball_count = passthrough["maximum_starting_ball_count"]
            self.useful_item_percentage = passthrough["useful_item_percentage"]
            self.useful_item_weights = passthrough["useful_item_weights"]

    def _generate_filler_useful_item_pool(self, count: int, useful_item_pool: List[str]) -> List[str]:
        useful_items_needed: int = round(self.useful_item_percentage / 100 * count)
        filler_items_needed: int = count - useful_items_needed

        item_pool: List[str] = list()

        if useful_items_needed > 0:
            useful_item_pool_by_type: Dict[PeggleNightsAPUsefulItems, List[str]] = {
                PeggleNightsAPUsefulItems.FEVER_METER_BONUS: list(),
                PeggleNightsAPUsefulItems.SCORE_MULTIPLIER: list(),
                PeggleNightsAPUsefulItems.TARGET_SCORE_DISCOUNT: list(),
            }

            if self.include_full_clears:
                useful_item_pool_by_type[PeggleNightsAPUsefulItems.FULL_CLEAR_DISCOUNT] = list()

            useful_item_name: str
            for useful_item_name in useful_item_pool:
                if PeggleNightsAPUsefulItems.FEVER_METER_BONUS.value in useful_item_name:
                    useful_item_pool_by_type[PeggleNightsAPUsefulItems.FEVER_METER_BONUS].append(useful_item_name)
                elif PeggleNightsAPUsefulItems.FULL_CLEAR_DISCOUNT.value in useful_item_name and self.include_full_clears:
                    useful_item_pool_by_type[PeggleNightsAPUsefulItems.FULL_CLEAR_DISCOUNT].append(useful_item_name)
                elif PeggleNightsAPUsefulItems.SCORE_MULTIPLIER.value in useful_item_name:
                    useful_item_pool_by_type[PeggleNightsAPUsefulItems.SCORE_MULTIPLIER].append(useful_item_name)
                elif PeggleNightsAPUsefulItems.TARGET_SCORE_DISCOUNT.value in useful_item_name:
                    useful_item_pool_by_type[PeggleNightsAPUsefulItems.TARGET_SCORE_DISCOUNT].append(useful_item_name)

            allowable_useful_item_types: List[PeggleNightsAPUsefulItems] = [
                PeggleNightsAPUsefulItems.FEVER_METER_BONUS,
                PeggleNightsAPUsefulItems.SCORE_MULTIPLIER,
                PeggleNightsAPUsefulItems.TARGET_SCORE_DISCOUNT,
            ]

            if self.include_full_clears:
                allowable_useful_item_types.append(PeggleNightsAPUsefulItems.FULL_CLEAR_DISCOUNT)

            weights: List[int] = [self.useful_item_weights[item_type] for item_type in allowable_useful_item_types]

            useful_item_types: List[PeggleNightsAPUsefulItems] = self.random.choices(
                allowable_useful_item_types,
                weights=weights,
                k=useful_items_needed
            )

            useful_item_type: PeggleNightsAPUsefulItems
            for useful_item_type in useful_item_types:
                item_pool.append(self.random.choice(useful_item_pool_by_type[useful_item_type]))

        for _ in range(filler_items_needed):
            item_pool.append(self.random.choice(self.filler_item_names))

        return item_pool
