import logging

from typing import Any, Dict, List, Optional, TextIO, Tuple

from BaseClasses import Item, ItemClassification, Location, Region, Tutorial

from Options import OptionError

from rule_builder.rules import Rule, And, Has

from worlds.AutoWorld import WebWorld, World

from .data.item_data import PinballFX3ItemData, item_data
from .data.location_data import PinballFX3LocationData, location_data
from .data.score_data import base_target_scores

from .data_funcs import (
    id_to_exclude_high_tier_challenge_stars,
    id_to_goals,
    id_to_requirement_modes,
    item_names_to_id,
    item_groups,
    items_with_tag,
    location_groups,
    location_names_to_id,
    locations_with_tag,
)

from .enums import (
    PinballFX3APExcludeHighTierChallengeStars,
    PinballFX3APRequirementModes,
    PinballFX3APGoals,
    PinballFX3APItems,
    PinballFX3APTags,
    PinballFX3APUsefulItems,
    PinballFX3Tables,
)

from .options import PinballFX3Options, option_groups


class PinballFX3Item(Item):
    game = "Pinball FX3"


class PinballFX3Location(Location):
    game = "Pinball FX3"


class PinballFX3WebWorld(WebWorld):
    theme: str = "partyTime"

    tutorials: List[Tutorial] = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the Pinball FX3 randomizer connected to a MultiworldGG Multiworld",
            "English",
            "setup_en.md",
            "setup/en",
            ["Serpent.AI"],
        )
    ]

    option_groups = option_groups


class PinballFX3World(World):
    """
    Pinball FX3 delivers fast, physics-driven pinball action with meticulously crafted tables inspired by iconic
    franchises and original designs. With competitive modes, online tournaments, and razor-sharp controls, it turns
    classic pinball into a modern skill-based challenge.
    """

    options_dataclass = PinballFX3Options
    options: PinballFX3Options

    game = "Pinball FX3"

    item_name_to_id = item_names_to_id()
    location_name_to_id = location_names_to_id()

    item_name_groups = item_groups()
    location_name_groups = location_groups()

    required_client_version: Tuple[int, int, int] = (0, 6, 7)

    web = PinballFX3WebWorld()

    filler_item_names: List[str] = item_groups()["Filler Item"]

    # Options
    challenge_high_tier_star_requirement: int
    challenge_low_tier_star_requirement: int
    challenge_mid_tier_star_requirement: int
    challenge_star_requirement_mode: PinballFX3APRequirementModes
    exclude_high_tier_challenge_stars: PinballFX3APExcludeHighTierChallengeStars
    exclude_high_tier_target_scores: bool
    goal: PinballFX3APGoals
    pinball_table_count: int
    pinball_table_selection: List[PinballFX3Tables]
    progressive_challenge_access: bool
    shiny_quarters_required: int
    shiny_quarters_total: int
    starsanity: bool
    target_score_requirement_mode: PinballFX3APRequirementModes
    target_score_requirement_percentage: int
    useful_item_percentage: int
    useful_item_weights: Dict[PinballFX3APUsefulItems, int]

    # Generation
    challenge_stars: Dict[PinballFX3Tables, List[int]]
    selected_goal_table: Optional[PinballFX3Tables] = None
    selected_starter_table: PinballFX3Tables
    selected_tables: List[PinballFX3Tables]
    target_scores: Dict[PinballFX3Tables, List[int]]

    # Metadata
    target_score_ratios: Dict[PinballFX3Tables, float]

    # Universal Tracker
    ut_can_gen_without_yaml: bool = True

    @property
    def is_universal_tracker(self) -> bool:
        return hasattr(self.multiworld, "re_gen_passthrough")

    def generate_early(self) -> None:
        self.goal = id_to_goals()[self.options.goal.value]

        self.pinball_table_count = self.options.pinball_table_count.value

        self.shiny_quarters_required = self.options.shiny_quarters_required.value
        self.shiny_quarters_total = self.options.shiny_quarters_total.value

        if self.shiny_quarters_total > (self.pinball_table_count * 2):
            self.shiny_quarters_total = self.pinball_table_count * 2

            logging.warning(
                f"Pinball FX3: {self.player_name} has more total shiny quarters than allowable with the selected "
                f"number of pinball tables. Adjusting total shiny quarters to {self.shiny_quarters_total}..."
            )

        if self.shiny_quarters_required > self.shiny_quarters_total:
            self.shiny_quarters_required = self.shiny_quarters_total

            logging.warning(
                f"Pinball FX3: {self.player_name} has more required shiny quarters than total shiny quarters. "
                "Adjusting required shiny quarters to match total shiny quarters..."
            )

        pinball_table_pool: List[PinballFX3Tables] = list()

        table_name: str
        is_enabled: bool
        for table_name, is_enabled in self.options.pinball_table_selection.value.items():
            if is_enabled:
                if table_name.startswith("[Free"):
                    table_name = table_name.split("Tables] ")[1]
                else:
                    table_name = table_name.split("DLC] ")[1]

                pinball_table_pool.append(PinballFX3Tables(table_name))

        pinball_table_pool = list(sorted(pinball_table_pool, key=lambda t: t.value))

        if len(pinball_table_pool) < 6:
            raise OptionError(
                f"Pinball FX3: {self.player_name} must have at least 6 pinball tables selected to play. "
                f"They only have {len(pinball_table_pool)} selected."
            )

        if self.pinball_table_count > len(pinball_table_pool):
            self.pinball_table_count = len(pinball_table_pool)

            logging.warning(
                f"Pinball FX3: {self.player_name} has a pinball table count higher than their selected pinball "
                "table pool. Adjusting pinball table count to match the size of their pinball table pool..."
            )

        self.random.shuffle(pinball_table_pool)

        pinball_table_pool = pinball_table_pool[:self.pinball_table_count]

        if self.goal == PinballFX3APGoals.SHINY_QUARTERS_FINAL_TABLE:
            self.selected_goal_table = pinball_table_pool[-1]
            self.selected_tables = pinball_table_pool[:-1]
        else:
            self.selected_tables = pinball_table_pool[:]

        self.selected_starter_table = self.selected_tables[0]

        self.exclude_high_tier_target_scores = bool(self.options.exclude_high_tier_target_scores.value)

        self.target_score_requirement_mode = id_to_requirement_modes()[
            self.options.target_score_requirement_mode.value
        ]

        self.target_score_requirement_percentage = self.options.target_score_requirement_percentage.value

        self.target_scores = dict()
        self.target_score_ratios = dict()

        table: PinballFX3Tables
        for table in (self.selected_tables + [self.selected_goal_table]):
            if table is None:
                continue

            base_scores: List[int] = base_target_scores[table]

            if self.target_score_requirement_mode == PinballFX3APRequirementModes.SAME_FOR_ALL_TABLES:
                self.target_score_ratios[table] = round(self.target_score_requirement_percentage / 100.0, 2)

                adjusted_scores: List[int] = [
                    round(int(score * (self.target_score_requirement_percentage / 100)), -4) for score in base_scores
                ]
            elif self.target_score_requirement_mode == PinballFX3APRequirementModes.RANDOM_PER_TABLE:
                random_percentage: int = self.random.randint(50, self.target_score_requirement_percentage)

                self.target_score_ratios[table] = round(random_percentage / 100.0, 2)

                adjusted_scores: List[int] = [
                    round(int(score * (random_percentage / 100)), -4) for score in base_scores
                ]
            else:
                adjusted_scores: List[int] = base_scores[:]

            if table == self.selected_goal_table:
                if self.exclude_high_tier_target_scores:
                    adjusted_scores[2] = adjusted_scores[1]

                adjusted_scores[0] = None
                adjusted_scores[1] = None
            elif self.exclude_high_tier_target_scores:
                adjusted_scores[2] = None

            self.target_scores[table] = adjusted_scores

        self.progressive_challenge_access = bool(self.options.progressive_challenge_access.value)

        self.exclude_high_tier_challenge_stars = id_to_exclude_high_tier_challenge_stars()[
            self.options.exclude_high_tier_challenge_stars.value
        ]

        self.challenge_star_requirement_mode = id_to_requirement_modes()[
            self.options.challenge_star_requirement_mode.value
        ]

        self.challenge_low_tier_star_requirement = self.options.challenge_low_tier_star_requirement.value
        self.challenge_mid_tier_star_requirement = self.options.challenge_mid_tier_star_requirement.value
        self.challenge_high_tier_star_requirement = self.options.challenge_high_tier_star_requirement.value

        self.challenge_stars = dict()

        table: PinballFX3Tables
        for table in self.selected_tables:
            if self.challenge_star_requirement_mode == PinballFX3APRequirementModes.SAME_FOR_ALL_TABLES:
                stars: List[int] = [
                    self.challenge_low_tier_star_requirement,
                    self.challenge_mid_tier_star_requirement,
                    self.challenge_high_tier_star_requirement,
                ]
            elif self.challenge_star_requirement_mode == PinballFX3APRequirementModes.RANDOM_PER_TABLE:
                stars: List[int] = [
                    self.random.randint(1, self.challenge_low_tier_star_requirement),
                    self.random.randint(6, self.challenge_mid_tier_star_requirement),
                    self.random.randint(11, self.challenge_high_tier_star_requirement),
                ]
            else:
                stars: List[int] = [
                    self.challenge_low_tier_star_requirement,
                    self.challenge_mid_tier_star_requirement,
                    self.challenge_high_tier_star_requirement,
                ]

            self.challenge_stars[table] = stars

            if self.exclude_high_tier_challenge_stars == PinballFX3APExcludeHighTierChallengeStars.EXCLUDE_ALL:
                self.challenge_stars[table][2] = None

        self.starsanity = bool(self.options.starsanity.value)

        self.useful_item_percentage = self.options.useful_item_percentage.value

        self.useful_item_weights = {
            PinballFX3APUsefulItems.SCORE_MULTIPLIER: 1,
            PinballFX3APUsefulItems.STAR_REQUIREMENT_DISCOUNT: 1,
            PinballFX3APUsefulItems.TARGET_SCORE_DISCOUNT: 1,
        }

        item_name: str
        weight: int
        for item_name, weight in self.options.useful_item_weights.value.items():
            try:
                enum_item: PinballFX3APUsefulItems = PinballFX3APUsefulItems(item_name)
            except ValueError:
                continue

            if isinstance(weight, int) and weight >= 1:
                self.useful_item_weights[enum_item] = weight

        # Universal Tracker Support
        if self.is_universal_tracker:
            self._apply_universal_tracker_passthrough()

    def create_regions(self) -> None:
        region_menu: Region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(region_menu)

        # Tables
        table: PinballFX3Tables
        for table in (self.selected_tables + [self.selected_goal_table]):
            if table is None:
                continue

            if table in self.challenge_stars:
                stars_low, stars_mid, stars_high = self.challenge_stars[table]
            else:
                stars_low, stars_mid, stars_high = 0, 0, 0

            region_table: Region = Region(f"Table: {table.value}", self.player, self.multiworld)

            table_tag: PinballFX3APTags = getattr(PinballFX3APTags, f"{table.name}_LOCATION")
            table_location_names: List[str] = locations_with_tag(table_tag)

            location_string: str
            for location_name in table_location_names:
                data: PinballFX3LocationData = location_data[location_name]

                is_target_score: bool = PinballFX3APTags.TARGET_SCORE_LOCATION in data.tags
                is_high_tier: bool = PinballFX3APTags.HIGH_TIER_LOCATION in data.tags

                # Only add the High Tier Target Score location for the goal table
                # If High Tier Target Scores are excluded, we will provide the Mid Tier Target Score value in slot data instead
                if table == self.selected_goal_table:
                    if not is_target_score or not is_high_tier:
                        continue
                else:
                    is_challenge_star: bool = PinballFX3APTags.CHALLENGE_STAR_LOCATION in data.tags
                    is_starsanity: bool = PinballFX3APTags.STARSANITY_LOCATION in data.tags
                    is_1_ball: bool = PinballFX3APTags.CHALLENGE_1_BALL_LOCATION in data.tags

                    exclude_all: bool = self.exclude_high_tier_challenge_stars == (
                        PinballFX3APExcludeHighTierChallengeStars.EXCLUDE_ALL
                    )

                    exclude_only_1_ball: bool = self.exclude_high_tier_challenge_stars == (
                        PinballFX3APExcludeHighTierChallengeStars.EXCLUDE_ONLY_1_BALL
                    )

                    if self.exclude_high_tier_target_scores and is_target_score:
                        if is_high_tier:
                            continue
                    elif exclude_all and (is_challenge_star or is_starsanity):
                        if is_high_tier:
                            continue
                    elif exclude_only_1_ball and (is_challenge_star or is_1_ball):
                        if is_high_tier and is_1_ball:
                            continue

                if not self.starsanity and PinballFX3APTags.STARSANITY_LOCATION in data.tags:
                    continue

                if self.starsanity and PinballFX3APTags.STARSANITY_LOCATION in data.tags:
                    if PinballFX3APTags.LOW_TIER_LOCATION in data.tags:
                        if PinballFX3APTags.STARSANITY_1_LOCATION in data.tags and stars_low <= 1:
                            continue
                        elif PinballFX3APTags.STARSANITY_2_LOCATION in data.tags and stars_low <= 2:
                            continue
                        elif PinballFX3APTags.STARSANITY_3_LOCATION in data.tags and stars_low <= 3:
                            continue
                        elif PinballFX3APTags.STARSANITY_4_LOCATION in data.tags and stars_low <= 4:
                            continue
                    elif PinballFX3APTags.MID_TIER_LOCATION in data.tags:
                        if PinballFX3APTags.STARSANITY_1_LOCATION in data.tags and stars_mid <= 6:
                            continue
                        elif PinballFX3APTags.STARSANITY_2_LOCATION in data.tags and stars_mid <= 7:
                            continue
                        elif PinballFX3APTags.STARSANITY_3_LOCATION in data.tags and stars_mid <= 8:
                            continue
                        elif PinballFX3APTags.STARSANITY_4_LOCATION in data.tags and stars_mid <= 9:
                            continue
                    elif PinballFX3APTags.HIGH_TIER_LOCATION in data.tags:
                        if PinballFX3APTags.STARSANITY_1_LOCATION in data.tags and stars_high <= 11:
                            continue
                        elif PinballFX3APTags.STARSANITY_2_LOCATION in data.tags and stars_high <= 12:
                            continue
                        elif PinballFX3APTags.STARSANITY_3_LOCATION in data.tags and stars_high <= 13:
                            continue
                        elif PinballFX3APTags.STARSANITY_4_LOCATION in data.tags and stars_high <= 14:
                            continue

                location: PinballFX3Location = PinballFX3Location(
                    self.player,
                    location_name,
                    data.archipelago_id,
                    region_table,
                )

                if table == self.selected_goal_table:
                    location.place_locked_item(self.create_item(PinballFX3APItems.VICTORY.value))

                if table != self.selected_starter_table:
                    location_access_rule: Optional[Rule] = data.requirements

                    if location_access_rule is not None:
                        self.set_rule(location, location_access_rule)

                region_table.locations.append(location)

            if table == self.selected_goal_table:
                region_menu.connect(
                    region_table,
                    rule=And(
                        Has(f"Table Unlock: {table.value}"),
                        Has(PinballFX3APItems.SHINY_QUARTER.value, self.shiny_quarters_required),
                    )
                )
            else:
                region_menu.connect(region_table, rule=Has(f"Table Unlock: {table.value}"))

            region_table.connect(region_menu)

            self.multiworld.regions.append(region_table)

    def create_items(self) -> None:
        ## Precollect
        items_to_precollect: List[str] = list()

        # Starting Table
        items_to_precollect.append(f"Table Unlock: {self.selected_starter_table.value}")

        ## Item Pool
        item_pool: List[PinballFX3Item] = list()

        # Shiny Quarters
        i: int
        for i in range(self.shiny_quarters_total):
            item: PinballFX3Item = self.create_item(PinballFX3APItems.SHINY_QUARTER.value)

            if i >= self.shiny_quarters_required:
                item.classification = ItemClassification.useful

            item_pool.append(item)

        # Challenge Access
        exclude_all: bool = self.exclude_high_tier_challenge_stars == (
            PinballFX3APExcludeHighTierChallengeStars.EXCLUDE_ALL
        )

        exclude_only_1_ball: bool = self.exclude_high_tier_challenge_stars == (
            PinballFX3APExcludeHighTierChallengeStars.EXCLUDE_ONLY_1_BALL
        )

        if self.progressive_challenge_access:
            item_name: str
            for item_name in items_with_tag(PinballFX3APTags.PROGRESSIVE_CHALLENGE_ACCESS_ITEM):
                is_1_ball: bool = item_name == PinballFX3APItems.PROGRESSIVE_1_BALL_CHALLENGE_TIER.value

                item_copies: int = 3

                if exclude_all:
                    item_copies = 2
                elif exclude_only_1_ball and is_1_ball:
                    item_copies = 2

                for _ in range(item_copies):
                    item_pool.append(self.create_item(item_name))
        else:
            item_name: str
            for item_name in items_with_tag(PinballFX3APTags.CHALLENGE_ACCESS_ITEM):
                is_high_tier: bool = item_name in (
                    PinballFX3APItems.CHALLENGES_1_BALL_HIGH_TIER.value,
                    PinballFX3APItems.CHALLENGES_5_MINUTE_HIGH_TIER.value,
                    PinballFX3APItems.CHALLENGES_SURVIVAL_HIGH_TIER.value,
                )

                is_1_ball: bool = item_name == PinballFX3APItems.CHALLENGES_1_BALL_HIGH_TIER.value

                if exclude_all:
                    if is_high_tier:
                        continue
                elif exclude_only_1_ball:
                    if is_high_tier and is_1_ball:
                        continue

                item_pool.append(self.create_item(item_name))

        # Table Unlocks + Prepare Useful Item Pool
        useful_item_pool: List[str] = list()

        i: int
        table: PinballFX3Tables
        for i, table in enumerate(self.selected_tables):
            table_tag: PinballFX3APTags = getattr(PinballFX3APTags, f"{table.name}_ITEM")
            table_items: List[str] = items_with_tag(table_tag)

            item_name: str
            for item_name in table_items:
                data: PinballFX3ItemData = item_data[item_name]

                if PinballFX3APTags.TABLE_UNLOCK_ITEM in data.tags:
                    if i > 0:
                        item_pool.append(self.create_item(item_name))
                else:
                    useful_item_pool.append(item_name)

        if self.selected_goal_table is not None:
            table_tag: PinballFX3APTags = getattr(PinballFX3APTags, f"{self.selected_goal_table.name}_ITEM")
            table_items: List[str] = items_with_tag(table_tag)

            item_name: str
            for item_name in table_items:
                data: PinballFX3ItemData = item_data[item_name]

                if PinballFX3APTags.TABLE_UNLOCK_ITEM in data.tags:
                    item_pool.append(self.create_item(item_name))
                else:
                    if PinballFX3APUsefulItems.STAR_REQUIREMENT_DISCOUNT.value not in item_name:
                        useful_item_pool.append(item_name)

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

    def create_item(self, name: str) -> PinballFX3Item:
        data: PinballFX3ItemData = item_data[name]

        return PinballFX3Item(
            name,
            data.classification,
            data.archipelago_id,
            self.player,
        )

    def generate_basic(self) -> None:
        if self.goal == PinballFX3APGoals.SHINY_QUARTERS_FINAL_TABLE:
            self.multiworld.completion_condition[self.player] = lambda state: state.has(
                PinballFX3APItems.VICTORY.value, self.player
            )
        elif self.goal == PinballFX3APGoals.SHINY_QUARTERS_HUNT:
            self.multiworld.completion_condition[self.player] = lambda state: state.has(
                PinballFX3APItems.SHINY_QUARTER.value, self.player, self.shiny_quarters_required
            )

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data: Dict[str, Any] = self.options.as_dict(
            "goal",
            "shiny_quarters_total",
            "shiny_quarters_required",
            "pinball_table_selection",
            "pinball_table_count",
            "exclude_high_tier_target_scores",
            "target_score_requirement_mode",
            "target_score_requirement_percentage",
            "progressive_challenge_access",
            "exclude_high_tier_challenge_stars",
            "challenge_star_requirement_mode",
            "challenge_low_tier_star_requirement",
            "challenge_mid_tier_star_requirement",
            "challenge_high_tier_star_requirement",
            "starsanity",
            "useful_item_percentage",
            "useful_item_weights",
        )

        slot_data["challenge_stars"] = {
            table.value: self.challenge_stars[table] for table in self.challenge_stars
        }

        slot_data["selected_goal_table"] = None

        if self.selected_goal_table is not None:
            slot_data["selected_goal_table"] = self.selected_goal_table.value

        slot_data["selected_starter_table"] = self.selected_starter_table.value
        slot_data["selected_tables"] = [table.value for table in self.selected_tables]

        slot_data["target_scores"] = {
            table.value: self.target_scores[table] for table in self.target_scores
        }

        # Relay generate_early Overrides
        if slot_data["shiny_quarters_total"] != self.shiny_quarters_total:
            slot_data["shiny_quarters_total"] = self.shiny_quarters_total

        if slot_data["shiny_quarters_required"] != self.shiny_quarters_required:
            slot_data["shiny_quarters_required"] = self.shiny_quarters_required

        pinball_table_count: int = len(self.selected_tables)

        if self.selected_goal_table is not None:
            pinball_table_count += 1

        if slot_data["pinball_table_count"] != pinball_table_count:
            slot_data["pinball_table_count"] = pinball_table_count

        slot_data["useful_item_weights"] = {
            item.value: weight for item, weight in self.useful_item_weights.items()
        }

        slot_data["target_score_ratios"] = {
            table.value: self.target_score_ratios[table] for table in self.target_score_ratios.keys()
        }

        return slot_data

    def write_spoiler_header(self, spoiler_handle: TextIO) -> None:
        join_string: str = "\n  "

        spoiler_handle.write(f"\nStarting Table: {self.selected_starter_table.value}")
        spoiler_handle.write(f"\n\nSelected Tables:\n  {join_string.join(sorted([t.value for t in self.selected_tables[1:]]))}")

        if self.selected_goal_table is not None:
            spoiler_handle.write(f"\n\nGoal Table: {self.selected_goal_table.value}")

        spoiler_handle.write(f"\n\nTarget Scores:\n  {join_string.join([f'{t.value} ({self.target_score_ratios[t]}x): {self.target_scores[t]}' for t in self.target_scores])}")
        spoiler_handle.write(f"\n\nChallenge Stars:\n  {join_string.join([f'{t.value}: {self.challenge_stars[t]}' for t in self.challenge_stars])}")

    def get_filler_item_name(self) -> str:
        return self.random.choice(self.filler_item_names)

    @staticmethod
    def interpret_slot_data(slot_data: Dict[str, Any]) -> Dict[str, Any]:
        slot_data["goal"] = id_to_goals()[slot_data["goal"]]
        slot_data["target_score_requirement_mode"] = id_to_requirement_modes()[slot_data["target_score_requirement_mode"]]

        slot_data["exclude_high_tier_challenge_stars"] = id_to_exclude_high_tier_challenge_stars()[
            slot_data["exclude_high_tier_challenge_stars"]
        ]

        slot_data["challenge_star_requirement_mode"] = id_to_requirement_modes()[slot_data["challenge_star_requirement_mode"]]

        slot_data["useful_item_weights"] = {
            PinballFX3APUsefulItems(item_name): weight for item_name, weight in slot_data["useful_item_weights"].items()
        }

        slot_data["selected_starter_table"] = PinballFX3Tables(slot_data["selected_starter_table"])
        slot_data["selected_tables"] = [PinballFX3Tables(table_name) for table_name in slot_data["selected_tables"]]

        if slot_data["selected_goal_table"] is not None:
            slot_data["selected_goal_table"] = PinballFX3Tables(slot_data["selected_goal_table"])

        slot_data["target_scores"] = {
            PinballFX3Tables(table_name): scores for table_name, scores in slot_data["target_scores"].items()
        }

        slot_data["challenge_stars"] = {
            PinballFX3Tables(table_name): stars for table_name, stars in slot_data["challenge_stars"].items()
        }

        slot_data["target_score_ratios"] = {
            PinballFX3Tables(table_name): ratio for table_name, ratio in slot_data["target_score_ratios"].items()
        }

        return slot_data

    def _apply_universal_tracker_passthrough(self) -> None:
        if "Pinball FX3" in self.multiworld.re_gen_passthrough:
            passthrough: Dict[str, Any] = self.multiworld.re_gen_passthrough["Pinball FX3"]

            self.goal = passthrough["goal"]
            self.pinball_table_count = passthrough["pinball_table_count"]
            self.shiny_quarters_required = passthrough["shiny_quarters_required"]
            self.shiny_quarters_total = passthrough["shiny_quarters_total"]
            self.selected_starter_table = passthrough["selected_starter_table"]
            self.selected_tables = passthrough["selected_tables"]
            self.selected_goal_table = passthrough["selected_goal_table"]
            self.exclude_high_tier_target_scores = passthrough["exclude_high_tier_target_scores"]
            self.target_score_requirement_mode = passthrough["target_score_requirement_mode"]
            self.target_score_requirement_percentage = passthrough["target_score_requirement_percentage"]
            self.target_scores = passthrough["target_scores"]
            self.progressive_challenge_access = passthrough["progressive_challenge_access"]
            self.exclude_high_tier_challenge_stars = passthrough["exclude_high_tier_challenge_stars"]
            self.challenge_star_requirement_mode = passthrough["challenge_star_requirement_mode"]
            self.challenge_low_tier_star_requirement = passthrough["challenge_low_tier_star_requirement"]
            self.challenge_mid_tier_star_requirement = passthrough["challenge_mid_tier_star_requirement"]
            self.challenge_high_tier_star_requirement = passthrough["challenge_high_tier_star_requirement"]
            self.challenge_stars = passthrough["challenge_stars"]
            self.starsanity = passthrough["starsanity"]
            self.useful_item_percentage = passthrough["useful_item_percentage"]
            self.useful_item_weights = passthrough["useful_item_weights"]
            self.target_score_ratios = passthrough["target_score_ratios"]

    def _generate_filler_useful_item_pool(self, count: int, useful_item_pool: List[str]) -> List[str]:
        useful_items_needed: int = round(self.useful_item_percentage / 100 * count)
        filler_items_needed: int = count - useful_items_needed

        item_pool: List[str] = list()

        if useful_items_needed > 0:
            useful_item_pool_by_type: Dict[PinballFX3APUsefulItems, List[str]] = {
                PinballFX3APUsefulItems.SCORE_MULTIPLIER: list(),
                PinballFX3APUsefulItems.STAR_REQUIREMENT_DISCOUNT: list(),
                PinballFX3APUsefulItems.TARGET_SCORE_DISCOUNT: list(),
            }

            useful_item_name: str
            for useful_item_name in useful_item_pool:
                if PinballFX3APUsefulItems.SCORE_MULTIPLIER.value in useful_item_name:
                    useful_item_pool_by_type[PinballFX3APUsefulItems.SCORE_MULTIPLIER].append(useful_item_name)
                elif PinballFX3APUsefulItems.STAR_REQUIREMENT_DISCOUNT.value in useful_item_name:
                    useful_item_pool_by_type[PinballFX3APUsefulItems.STAR_REQUIREMENT_DISCOUNT].append(useful_item_name)
                elif PinballFX3APUsefulItems.TARGET_SCORE_DISCOUNT.value in useful_item_name:
                    useful_item_pool_by_type[PinballFX3APUsefulItems.TARGET_SCORE_DISCOUNT].append(useful_item_name)

            useful_item_types: List[PinballFX3APUsefulItems] = self.random.choices(
                (
                    PinballFX3APUsefulItems.SCORE_MULTIPLIER,
                    PinballFX3APUsefulItems.STAR_REQUIREMENT_DISCOUNT,
                    PinballFX3APUsefulItems.TARGET_SCORE_DISCOUNT,
                ),
                weights=(
                    self.useful_item_weights[PinballFX3APUsefulItems.SCORE_MULTIPLIER],
                    self.useful_item_weights[PinballFX3APUsefulItems.STAR_REQUIREMENT_DISCOUNT],
                    self.useful_item_weights[PinballFX3APUsefulItems.TARGET_SCORE_DISCOUNT],
                ),
                k=useful_items_needed
            )

            useful_item_type: PinballFX3APUsefulItems
            for useful_item_type in useful_item_types:
                item_pool.append(self.random.choice(useful_item_pool_by_type[useful_item_type]))

        for _ in range(filler_items_needed):
            item_pool.append(self.random.choice(self.filler_item_names))

        return item_pool
