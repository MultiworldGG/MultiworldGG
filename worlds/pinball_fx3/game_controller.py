from typing import Dict, List, Optional, Set, Union

import collections
import logging

from .data.mapping_data import table_to_table_groups

from .enums import (
    PinballFX3APExcludeHighTierChallengeStars,
    PinballFX3APGoals,
    PinballFX3APItems,
    PinballFX3APRequirementModes,
    PinballFX3APUsefulItems,
    PinballFX3ChallengeTypes,
    PinballFX3Contexts,
    PinballFX3Tables,
)

from .game_state_manager import GameStateManager, GameState


class GameController:
    logger: Optional[logging.Logger]

    game_state_manager: GameStateManager

    received_items: Dict[str, int]
    completed_locations: Set[str]

    completed_locations_queue: collections.deque
    received_items_queue: collections.deque

    goal_item_count: int
    goal_completed: bool

    game_state_context: Optional[PinballFX3Contexts]
    game_state_table: Optional[PinballFX3Tables]
    game_state_current_score: Optional[int]
    game_state_challenge_type: Optional[PinballFX3ChallengeTypes]
    game_state_stars_obtained: Optional[int]
    game_state_target_score: Optional[int]
    game_state_previous_target_score: Optional[int]

    option_goal: Optional[PinballFX3APGoals]
    option_shiny_quarters_total: Optional[int]
    option_shiny_quarters_required: Optional[int]
    option_pinball_table_selection: Optional[Dict[str, bool]]
    option_pinball_table_count: Optional[int]
    option_exclude_high_tier_target_scores: Optional[bool]
    option_target_score_requirement_mode: Optional[PinballFX3APRequirementModes]
    option_target_score_requirement_percentage: Optional[int]
    option_progressive_challenge_access: Optional[bool]
    option_exclude_high_tier_challenge_stars: Optional[PinballFX3APExcludeHighTierChallengeStars]
    option_challenge_star_requirement_mode: Optional[PinballFX3APRequirementModes]
    option_challenge_low_tier_star_requirement: Optional[int]
    option_challenge_mid_tier_star_requirement: Optional[int]
    option_challenge_high_tier_star_requirement: Optional[int]
    option_starsanity: Optional[bool]
    option_useful_item_percentage: Optional[int]
    option_useful_item_weights: Optional[Dict[PinballFX3APUsefulItems, int]]

    selected_starting_table: Optional[PinballFX3Tables]
    selected_tables: Optional[List[PinballFX3Tables]]
    selected_goal_table: Optional[PinballFX3Tables]

    target_scores: Optional[Dict[PinballFX3Tables, List[int]]]
    challenge_stars: Optional[Dict[PinballFX3Tables, List[int]]]

    single_player_locations_by_table: Optional[Dict[PinballFX3Tables, Dict[int, str]]]

    challenge_1_ball_locations_by_table: Optional[Dict[PinballFX3Tables, Dict[int, str]]]
    challenge_5_minute_locations_by_table = Optional[Dict[PinballFX3Tables, Dict[int, str]]]
    challenge_survival_locations_by_table = Optional[Dict[PinballFX3Tables, Dict[int, str]]]

    useful_items: Optional[Dict[PinballFX3Tables, Dict[PinballFX3APUsefulItems, int]]]

    def __init__(self, logger: logging.Logger = None) -> None:
        self.logger = logger

        self.game_state_manager = GameStateManager()

        self.received_items = dict()
        self.completed_locations = set()

        self.completed_locations_queue = collections.deque()
        self.received_items_queue = collections.deque()

        self.goal_item_count = 0
        self.goal_completed = False

        self.game_state_context = None
        self.game_state_table = None
        self.game_state_current_score = None
        self.game_state_challenge_type = None
        self.game_state_stars_obtained = None
        self.game_state_target_score = None
        self.game_state_previous_target_score = None

        self.option_goal = None
        self.option_shiny_quarters_total = None
        self.option_shiny_quarters_required = None
        self.option_pinball_table_selection = None
        self.option_pinball_table_count = None
        self.option_exclude_high_tier_target_scores = None
        self.option_target_score_requirement_mode = None
        self.option_target_score_requirement_percentage = None
        self.option_progressive_challenge_access = None
        self.option_exclude_high_tier_target_scores = None
        self.option_challenge_star_requirement_mode = None
        self.option_challenge_low_tier_star_requirement = None
        self.option_challenge_mid_tier_star_requirement = None
        self.option_challenge_high_tier_star_requirement = None
        self.option_starsanity = None
        self.option_useful_item_percentage = None
        self.option_useful_item_weights = None

        self.selected_starting_table = None
        self.selected_tables = None
        self.selected_goal_table = None

        self.target_scores = None
        self.challenge_stars = None

        self.single_player_locations_by_table = None

        self.challenge_1_ball_locations_by_table = None
        self.challenge_5_minute_locations_by_table = None
        self.challenge_survival_locations_by_table = None

        self.useful_items = None

    def log(self, message) -> None:
        if self.logger:
            self.logger.info(message)

    def log_debug(self, message) -> None:
        if self.logger:
            self.logger.debug(message)

    def open_process_handle(self) -> bool:
        return self.game_state_manager.open_process_handle()

    def close_process_handle(self) -> bool:
        return self.game_state_manager.close_process_handle()

    def is_process_running(self) -> bool:
        return self.game_state_manager.is_process_still_running()

    def assemble_single_player_locations(self) -> None:
        if self.target_scores is None:
            return

        locations: Dict[PinballFX3Tables, Dict[int, str]] = dict()

        table: PinballFX3Tables
        for table in self.selected_tables:
            table_prefix: str = f"{table.value} [{table_to_table_groups[table].value}] -"

            locations[table] = dict()

            locations[table][self.target_scores[table][0]] = f"{table_prefix} Target Score (Low)"
            locations[table][self.target_scores[table][1]] = f"{table_prefix} Target Score (Mid)"

            if not self.option_exclude_high_tier_target_scores:
                locations[table][self.target_scores[table][2]] = f"{table_prefix} Target Score (High)"

        if self.selected_goal_table is not None:
            table_prefix: str = f"{self.selected_goal_table.value} [{table_to_table_groups[self.selected_goal_table].value}] -"

            locations[self.selected_goal_table] = dict()

            locations[self.selected_goal_table][self.target_scores[self.selected_goal_table][2]] = f"{table_prefix} Target Score (High)"

        self.single_player_locations_by_table = locations

    def assemble_challenge_locations(self) -> None:
        if self.challenge_stars is None:
            return

        exclude_all: bool = self.option_exclude_high_tier_challenge_stars == (
            PinballFX3APExcludeHighTierChallengeStars.EXCLUDE_ALL
        )

        exclude_1_ball: bool = self.option_exclude_high_tier_challenge_stars == (
            PinballFX3APExcludeHighTierChallengeStars.EXCLUDE_ONLY_1_BALL
        )

        locations_1_ball: Dict[PinballFX3Tables, Dict[int, str]] = dict()
        locations_5_minute: Dict[PinballFX3Tables, Dict[int, str]] = dict()
        locations_survival: Dict[PinballFX3Tables, Dict[int, str]] = dict()

        table: PinballFX3Tables
        for table in self.selected_tables:
            table_prefix: str = f"{table.value} [{table_to_table_groups[table].value}] -"

            locations_1_ball[table] = dict()

            locations_1_ball[table][self.challenge_stars[table][0]] = f"{table_prefix} 1 Ball Challenge - Target Star (Low)"
            locations_1_ball[table][self.challenge_stars[table][1]] = f"{table_prefix} 1 Ball Challenge - Target Star (Mid)"

            if not exclude_all and not exclude_1_ball:
                locations_1_ball[table][self.challenge_stars[table][2]] = f"{table_prefix} 1 Ball Challenge - Target Star (High)"

            locations_5_minute[table] = dict()

            locations_5_minute[table][self.challenge_stars[table][0]] = f"{table_prefix} 5 Minute Challenge - Target Star (Low)"
            locations_5_minute[table][self.challenge_stars[table][1]] = f"{table_prefix} 5 Minute Challenge - Target Star (Mid)"

            if not exclude_all:
                locations_5_minute[table][self.challenge_stars[table][2]] = f"{table_prefix} 5 Minute Challenge - Target Star (High)"

            locations_survival[table] = dict()

            locations_survival[table][self.challenge_stars[table][0]] = f"{table_prefix} Survival Challenge - Target Star (Low)"
            locations_survival[table][self.challenge_stars[table][1]] = f"{table_prefix} Survival Challenge - Target Star (Mid)"

            if not exclude_all:
                locations_survival[table][self.challenge_stars[table][2]] = f"{table_prefix} Survival Challenge - Target Star (High)"

            if self.option_starsanity:
                if self.challenge_stars[table][0] > 1:
                    locations_1_ball[table][1] = f"{table_prefix} 1 Ball Challenge - Starsanity 1 (Low)"
                    locations_5_minute[table][1] = f"{table_prefix} 5 Minute Challenge - Starsanity 1 (Low)"
                    locations_survival[table][1] = f"{table_prefix} Survival Challenge - Starsanity 1 (Low)"

                if self.challenge_stars[table][0] > 2:
                    locations_1_ball[table][2] = f"{table_prefix} 1 Ball Challenge - Starsanity 2 (Low)"
                    locations_5_minute[table][2] = f"{table_prefix} 5 Minute Challenge - Starsanity 2 (Low)"
                    locations_survival[table][2] = f"{table_prefix} Survival Challenge - Starsanity 2 (Low)"

                if self.challenge_stars[table][0] > 3:
                    locations_1_ball[table][3] = f"{table_prefix} 1 Ball Challenge - Starsanity 3 (Low)"
                    locations_5_minute[table][3] = f"{table_prefix} 5 Minute Challenge - Starsanity 3 (Low)"
                    locations_survival[table][3] = f"{table_prefix} Survival Challenge - Starsanity 3 (Low)"

                if self.challenge_stars[table][0] > 4:
                    locations_1_ball[table][4] = f"{table_prefix} 1 Ball Challenge - Starsanity 4 (Low)"
                    locations_5_minute[table][4] = f"{table_prefix} 5 Minute Challenge - Starsanity 4 (Low)"
                    locations_survival[table][4] = f"{table_prefix} Survival Challenge - Starsanity 4 (Low)"

                if self.challenge_stars[table][1] > 6:
                    locations_1_ball[table][6] = f"{table_prefix} 1 Ball Challenge - Starsanity 1 (Mid)"
                    locations_5_minute[table][6] = f"{table_prefix} 5 Minute Challenge - Starsanity 1 (Mid)"
                    locations_survival[table][6] = f"{table_prefix} Survival Challenge - Starsanity 1 (Mid)"

                if self.challenge_stars[table][1] > 7:
                    locations_1_ball[table][7] = f"{table_prefix} 1 Ball Challenge - Starsanity 2 (Mid)"
                    locations_5_minute[table][7] = f"{table_prefix} 5 Minute Challenge - Starsanity 2 (Mid)"
                    locations_survival[table][7] = f"{table_prefix} Survival Challenge - Starsanity 2 (Mid)"

                if self.challenge_stars[table][1] > 8:
                    locations_1_ball[table][8] = f"{table_prefix} 1 Ball Challenge - Starsanity 3 (Mid)"
                    locations_5_minute[table][8] = f"{table_prefix} 5 Minute Challenge - Starsanity 3 (Mid)"
                    locations_survival[table][8] = f"{table_prefix} Survival Challenge - Starsanity 3 (Mid)"

                if self.challenge_stars[table][1] > 9:
                    locations_1_ball[table][9] = f"{table_prefix} 1 Ball Challenge - Starsanity 4 (Mid)"
                    locations_5_minute[table][9] = f"{table_prefix} 5 Minute Challenge - Starsanity 4 (Mid)"
                    locations_survival[table][9] = f"{table_prefix} Survival Challenge - Starsanity 4 (Mid)"

                if not exclude_all:
                    if self.challenge_stars[table][2] > 11:
                        if not exclude_1_ball:
                            locations_1_ball[table][11] = f"{table_prefix} 1 Ball Challenge - Starsanity 1 (High)"

                        locations_5_minute[table][11] = f"{table_prefix} 5 Minute Challenge - Starsanity 1 (High)"
                        locations_survival[table][11] = f"{table_prefix} Survival Challenge - Starsanity 1 (High)"

                    if self.challenge_stars[table][2] > 12:
                        if not exclude_1_ball:
                            locations_1_ball[table][12] = f"{table_prefix} 1 Ball Challenge - Starsanity 2 (High)"

                        locations_5_minute[table][12] = f"{table_prefix} 5 Minute Challenge - Starsanity 2 (High)"
                        locations_survival[table][12] = f"{table_prefix} Survival Challenge - Starsanity 2 (High)"

                    if self.challenge_stars[table][2] > 13:
                        if not exclude_1_ball:
                            locations_1_ball[table][13] = f"{table_prefix} 1 Ball Challenge - Starsanity 3 (High)"

                        locations_5_minute[table][13] = f"{table_prefix} 5 Minute Challenge - Starsanity 3 (High)"
                        locations_survival[table][13] = f"{table_prefix} Survival Challenge - Starsanity 3 (High)"

                    if self.challenge_stars[table][2] > 14:
                        if not exclude_1_ball:
                            locations_1_ball[table][14] = f"{table_prefix} 1 Ball Challenge - Starsanity 4 (High)"

                        locations_5_minute[table][14] = f"{table_prefix} 5 Minute Challenge - Starsanity 4 (High)"
                        locations_survival[table][14] = f"{table_prefix} Survival Challenge - Starsanity 4 (High)"

        self.challenge_1_ball_locations_by_table = locations_1_ball
        self.challenge_5_minute_locations_by_table = locations_5_minute
        self.challenge_survival_locations_by_table = locations_survival

    def initialize_useful_items(self) -> None:
        useful_items: Dict[PinballFX3Tables, Dict[PinballFX3APUsefulItems, int]] = dict()

        if self.selected_tables is None:
            return

        table: PinballFX3Tables
        for table in self.selected_tables:
            useful_items[table] = dict()

            item: PinballFX3APUsefulItems
            for item in PinballFX3APUsefulItems:
                useful_items[table][item] = 0

        if self.selected_goal_table is not None:
            useful_items[self.selected_goal_table] = dict()

            item: PinballFX3APUsefulItems
            for item in PinballFX3APUsefulItems:
                useful_items[self.selected_goal_table][item] = 0

        self.useful_items = useful_items

    def update(self) -> None:
        if self.game_state_manager.is_process_still_running():
            try:
                self._refresh_game_state()
                self._check_for_completed_locations()
                self._process_received_items()
                self._check_for_victory()
            except Exception:
                import traceback

                with open("pinball_fx3_errors.log", "a") as f:
                    f.write(traceback.format_exc() + "\n\n")

    def reset(self) -> None:
        self.received_items = dict()
        self.completed_locations = set()

        self.completed_locations_queue = collections.deque()
        self.received_items_queue = collections.deque()

        self.goal_item_count = 0
        self.goal_completed = False

        self.game_state_context = None
        self.game_state_table = None
        self.game_state_current_score = None
        self.game_state_challenge_type = None
        self.game_state_stars_obtained = None
        self.game_state_target_score = None
        self.game_state_previous_target_score = None

        self.option_goal = None
        self.option_shiny_quarters_total = None
        self.option_shiny_quarters_required = None
        self.option_pinball_table_selection = None
        self.option_pinball_table_count = None
        self.option_exclude_high_tier_target_scores = None
        self.option_target_score_requirement_mode = None
        self.option_target_score_requirement_percentage = None
        self.option_progressive_challenge_access = None
        self.option_exclude_high_tier_target_scores = None
        self.option_challenge_star_requirement_mode = None
        self.option_challenge_low_tier_star_requirement = None
        self.option_challenge_mid_tier_star_requirement = None
        self.option_challenge_high_tier_star_requirement = None
        self.option_starsanity = None
        self.option_useful_item_percentage = None
        self.option_useful_item_weights = None

        self.selected_starting_table = None
        self.selected_tables = None
        self.selected_goal_table = None

        self.target_scores = None
        self.challenge_stars = None

        self.single_player_locations_by_table = None

        self.challenge_1_ball_locations_by_table = None
        self.challenge_5_minute_locations_by_table = None
        self.challenge_survival_locations_by_table = None

        self.useful_items = None

    def _refresh_game_state(self) -> None:
        game_state: GameState = self.game_state_manager.determine_game_state()

        self.game_state_context = game_state.context
        self.game_state_table = game_state.table
        self.game_state_current_score = game_state.current_score
        self.game_state_challenge_type = game_state.challenge_type
        self.game_state_stars_obtained = game_state.stars_obtained
        self.game_state_target_score = game_state.target_score
        self.game_state_previous_target_score = game_state.previous_target_score

    def _check_for_completed_locations(self) -> None:
        return_contexts: List[Union[PinballFX3Contexts, None]] = [
            PinballFX3Contexts.INVALID,
            None,
        ]

        if self.game_state_context in return_contexts:
            return

        if self.game_state_table is None:
            return
        elif self.game_state_table not in self.selected_tables and self.game_state_table != self.selected_goal_table:
            return

        table_unlock_item: str = f"Table Unlock: {self.game_state_table.value}"

        if table_unlock_item not in self.received_items:
            return

        if self.received_items[table_unlock_item] < 1:
            return

        if self.selected_goal_table is not None and self.game_state_table == self.selected_goal_table:
            if PinballFX3APItems.SHINY_QUARTER.value not in self.received_items:
                return
            elif self.received_items[PinballFX3APItems.SHINY_QUARTER.value] < self.option_shiny_quarters_required:
                return

        checked_locations: List[str] = list()

        if self.game_state_context == PinballFX3Contexts.SINGLE_PLAYER:
            if self.game_state_table not in self.target_scores:
                return

            multiplier: float = 1.0 + (
                self.useful_items[self.game_state_table][PinballFX3APUsefulItems.SCORE_MULTIPLIER] * 0.05
            )

            multiplied_score: int = round(self.game_state_current_score * multiplier)

            score: int
            location: str
            for score, location in self.single_player_locations_by_table[self.game_state_table].items():
                if score is None:
                    continue

                discount_ratio: float = 1.0 - (
                    self.useful_items[self.game_state_table][PinballFX3APUsefulItems.TARGET_SCORE_DISCOUNT] * 0.05
                )

                discounted_score: int = round(score * discount_ratio)

                if multiplied_score >= discounted_score:
                    checked_locations.append(location)
        elif self.game_state_context == PinballFX3Contexts.CHALLENGE:
            if self.game_state_table not in self.challenge_stars:
                return

            possible_locations: Dict[int, str] = dict()

            has_low_access: bool = False
            has_mid_access: bool = False
            has_high_access: bool = False

            if self.game_state_challenge_type == PinballFX3ChallengeTypes.ONE_BALL:
                possible_locations = self.challenge_1_ball_locations_by_table[self.game_state_table]

                if PinballFX3APItems.CHALLENGES_1_BALL_LOW_TIER.value in self.received_items and \
                        self.received_items[PinballFX3APItems.CHALLENGES_1_BALL_LOW_TIER.value] >= 1:
                    has_low_access = True
                elif PinballFX3APItems.PROGRESSIVE_1_BALL_CHALLENGE_TIER.value in self.received_items and \
                        self.received_items[PinballFX3APItems.PROGRESSIVE_1_BALL_CHALLENGE_TIER.value] >= 1:
                    has_low_access = True

                if PinballFX3APItems.CHALLENGES_1_BALL_MID_TIER.value in self.received_items and \
                        self.received_items[PinballFX3APItems.CHALLENGES_1_BALL_MID_TIER.value] >= 1:
                    has_mid_access = True
                elif PinballFX3APItems.PROGRESSIVE_1_BALL_CHALLENGE_TIER.value in self.received_items and \
                        self.received_items[PinballFX3APItems.PROGRESSIVE_1_BALL_CHALLENGE_TIER.value] >= 2:
                    has_mid_access = True

                if PinballFX3APItems.CHALLENGES_1_BALL_HIGH_TIER.value in self.received_items and \
                        self.received_items[PinballFX3APItems.CHALLENGES_1_BALL_HIGH_TIER.value] >= 1:
                    has_high_access = True
                elif PinballFX3APItems.PROGRESSIVE_1_BALL_CHALLENGE_TIER.value in self.received_items and \
                        self.received_items[PinballFX3APItems.PROGRESSIVE_1_BALL_CHALLENGE_TIER.value] >= 3:
                    has_high_access = True
            elif self.game_state_challenge_type == PinballFX3ChallengeTypes.FIVE_MINUTE:
                possible_locations = self.challenge_5_minute_locations_by_table[self.game_state_table]

                if PinballFX3APItems.CHALLENGES_5_MINUTE_LOW_TIER.value in self.received_items and \
                        self.received_items[PinballFX3APItems.CHALLENGES_5_MINUTE_LOW_TIER.value] >= 1:
                    has_low_access = True
                elif PinballFX3APItems.PROGRESSIVE_5_MINUTE_CHALLENGE_TIER.value in self.received_items and \
                        self.received_items[PinballFX3APItems.PROGRESSIVE_5_MINUTE_CHALLENGE_TIER.value] >= 1:
                    has_low_access = True

                if PinballFX3APItems.CHALLENGES_5_MINUTE_MID_TIER.value in self.received_items and \
                        self.received_items[PinballFX3APItems.CHALLENGES_5_MINUTE_MID_TIER.value] >= 1:
                    has_mid_access = True
                elif PinballFX3APItems.PROGRESSIVE_5_MINUTE_CHALLENGE_TIER.value in self.received_items and \
                        self.received_items[PinballFX3APItems.PROGRESSIVE_5_MINUTE_CHALLENGE_TIER.value] >= 2:
                    has_mid_access = True

                if PinballFX3APItems.CHALLENGES_5_MINUTE_HIGH_TIER.value in self.received_items and \
                        self.received_items[PinballFX3APItems.CHALLENGES_5_MINUTE_HIGH_TIER.value] >= 1:
                    has_high_access = True
                elif PinballFX3APItems.PROGRESSIVE_5_MINUTE_CHALLENGE_TIER.value in self.received_items and \
                        self.received_items[PinballFX3APItems.PROGRESSIVE_5_MINUTE_CHALLENGE_TIER.value] >= 3:
                    has_high_access = True
            elif self.game_state_challenge_type == PinballFX3ChallengeTypes.SURVIVAL:
                possible_locations = self.challenge_survival_locations_by_table[self.game_state_table]

                if PinballFX3APItems.CHALLENGES_SURVIVAL_LOW_TIER.value in self.received_items and \
                        self.received_items[PinballFX3APItems.CHALLENGES_SURVIVAL_LOW_TIER.value] >= 1:
                    has_low_access = True
                elif PinballFX3APItems.PROGRESSIVE_SURVIVAL_CHALLENGE_TIER.value in self.received_items and \
                        self.received_items[PinballFX3APItems.PROGRESSIVE_SURVIVAL_CHALLENGE_TIER.value] >= 1:
                    has_low_access = True

                if PinballFX3APItems.CHALLENGES_SURVIVAL_MID_TIER.value in self.received_items and \
                        self.received_items[PinballFX3APItems.CHALLENGES_SURVIVAL_MID_TIER.value] >= 1:
                    has_mid_access = True
                elif PinballFX3APItems.PROGRESSIVE_SURVIVAL_CHALLENGE_TIER.value in self.received_items and \
                        self.received_items[PinballFX3APItems.PROGRESSIVE_SURVIVAL_CHALLENGE_TIER.value] >= 2:
                    has_mid_access = True

                if PinballFX3APItems.CHALLENGES_SURVIVAL_HIGH_TIER.value in self.received_items and \
                        self.received_items[PinballFX3APItems.CHALLENGES_SURVIVAL_HIGH_TIER.value] >= 1:
                    has_high_access = True
                elif PinballFX3APItems.PROGRESSIVE_SURVIVAL_CHALLENGE_TIER.value in self.received_items and \
                        self.received_items[PinballFX3APItems.PROGRESSIVE_SURVIVAL_CHALLENGE_TIER.value] >= 3:
                    has_high_access = True

            bonus_stars: int = self.useful_items[self.game_state_table][PinballFX3APUsefulItems.STAR_REQUIREMENT_DISCOUNT]
            stars_obtained: int = self.game_state_stars_obtained + bonus_stars

            if stars_obtained is None or stars_obtained < 1:
                return

            i: int
            for i in range(1, stars_obtained + 1):
                if i in possible_locations:
                    location: str = possible_locations[i]

                    if self.game_state_table != self.selected_starting_table:
                        if i <= 5 and not has_low_access:
                            continue

                        if 5 < i <= 10 and not has_mid_access:
                            continue

                        if i > 10 and not has_high_access:
                            continue

                    checked_locations.append(location)

        location: str
        for location in checked_locations:
            if location not in self.completed_locations and location not in self.completed_locations_queue:
                self.completed_locations.add(location)
                self.completed_locations_queue.append(location)

    def _process_received_items(self) -> None:
        while len(self.received_items_queue) > 0:
            item: str = self.received_items_queue.popleft()

            if item not in self.received_items:
                self.received_items[item] = 0

            self.received_items[item] += 1

            is_score_multiplier: bool = PinballFX3APUsefulItems.SCORE_MULTIPLIER.value in item
            is_star_requirement_discount: bool = PinballFX3APUsefulItems.STAR_REQUIREMENT_DISCOUNT.value in item
            is_target_score_discount: bool = PinballFX3APUsefulItems.TARGET_SCORE_DISCOUNT.value in item

            if is_score_multiplier or is_star_requirement_discount or is_target_score_discount:
                split_item: List[str] = item.split(": ")

                useful_item_string: str = split_item[0]
                table_string: str = ": ".join(split_item[1:])

                table: PinballFX3Tables = PinballFX3Tables(table_string)
                useful_item: PinballFX3APUsefulItems = PinballFX3APUsefulItems(useful_item_string)

                self.useful_items[table][useful_item] += 1

    def _check_for_victory(self) -> None:
        if self.option_goal == PinballFX3APGoals.SHINY_QUARTERS_FINAL_TABLE:
            if PinballFX3APItems.VICTORY.value in self.received_items:
                self.goal_completed = True
        elif self.option_goal == PinballFX3APGoals.SHINY_QUARTERS_HUNT:
            if PinballFX3APItems.SHINY_QUARTER.value in self.received_items:
                if self.received_items[PinballFX3APItems.SHINY_QUARTER.value] >= self.option_shiny_quarters_required:
                    self.goal_completed = True
