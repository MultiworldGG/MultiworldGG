from typing import Dict, List, Optional, Set, Tuple, Union

import collections
import logging

from .data.mapping_data import level_to_peg_count

from .enums import (
    PeggleNightsAPGoals,
    PeggleNightsAPItems,
    PeggleNightsAPMasterSelectionModes,
    PeggleNightsAPRequirementModes,
    PeggleNightsAPUsefulItems,
    PeggleNightsCharacters,
    PeggleNightsContexts,
    PeggleNightsGameModes,
    PeggleNightsLevels,
    PeggleNightsLevelStates,
)

from .game_state_manager import GameStateManager, GameState


class GameController:
    logger: Optional[logging.Logger]

    received_items: Dict[str, int]
    completed_locations: Set[str]

    completed_locations_queue: collections.deque
    received_items_queue: collections.deque

    goal_completed: bool

    # Game State
    game_state_context: Optional[PeggleNightsContexts]
    game_state_current_game_mode: Optional[PeggleNightsGameModes]
    game_state_current_level: Optional[PeggleNightsLevels]
    game_state_level_state: Optional[PeggleNightsLevelStates]
    game_state_current_character: Optional[PeggleNightsCharacters]
    game_state_current_ball_count: Optional[int]
    game_state_current_score: Optional[int]
    game_state_current_shot_score: Optional[int]
    game_state_current_orange_peg_combo: Optional[int]
    game_state_current_peg_combo: Optional[int]
    game_state_current_fever_meter_multiplier: Optional[int]
    game_state_orange_pegs_remaining: Optional[int]
    game_state_pegs_cleared: Optional[int]
    game_state_has_achieved_fever_meter_multiplier_2x: Optional[bool]
    game_state_has_achieved_fever_meter_multiplier_3x: Optional[bool]
    game_state_has_achieved_fever_meter_multiplier_5x: Optional[bool]
    game_state_has_achieved_fever_meter_multiplier_10x: Optional[bool]
    game_state_has_cleared_level: Optional[bool]
    game_state_has_achieved_style_shot: Optional[bool]
    game_state_has_achieved_3_orange_peg_combo: Optional[bool]
    game_state_has_achieved_5_orange_peg_combo: Optional[bool]
    game_state_has_achieved_7_peg_combo: Optional[bool]
    game_state_has_achieved_15_peg_combo: Optional[bool]
    game_state_has_achieved_full_clear: Optional[bool]

    # Generation Options
    option_goal: Optional[PeggleNightsAPGoals]
    option_shadow_pegs_total: Optional[int]
    option_shadow_pegs_required: Optional[int]
    option_master_selection_mode: Optional[PeggleNightsAPMasterSelectionModes]
    option_master_selection: Optional[Dict[str, bool]]
    option_master_count: Optional[int]
    option_level_selection: Optional[Dict[str, bool]]
    option_level_count: Optional[int]
    option_include_full_clears: Optional[bool]
    option_target_score_requirement_mode: Optional[PeggleNightsAPRequirementModes]
    option_target_score_requirement_percentage: Optional[int]
    option_maximum_starting_ball_count: Optional[int]
    option_useful_item_percentage: Optional[int]
    option_useful_item_weights: Optional[Dict[PeggleNightsAPUsefulItems, int]]

    # Generation Data
    selected_masters: Optional[List[PeggleNightsCharacters]]
    selected_starter_master: Optional[PeggleNightsCharacters]
    selected_levels: Optional[List[PeggleNightsLevels]]
    selected_starter_level: Optional[PeggleNightsLevels]
    selected_goal_level: Optional[PeggleNightsLevels]
    target_scores: Optional[Dict[PeggleNightsLevels, List[int]]]
    target_score_ratios: Optional[Dict[PeggleNightsLevels, List[float]]]

    # Data
    target_score_locations_by_level: Optional[Dict[PeggleNightsLevels, Dict[int, str]]]
    useful_items: Optional[Dict[PeggleNightsLevels, Dict[PeggleNightsAPUsefulItems, int]]]
    can_modify_ball_count: bool
    can_modify_fever_meter: bool

    def __init__(self, logger: logging.Logger = None) -> None:
        self.logger = logger

        self.game_state_manager = GameStateManager()

        self.received_items = dict()
        self.completed_locations = set()

        self.completed_locations_queue = collections.deque()
        self.received_items_queue = collections.deque()

        self.goal_completed = False

        self.game_state_context = None
        self.game_state_current_game_mode = None
        self.game_state_current_level = None
        self.game_state_level_state = None
        self.game_state_current_character = None
        self.game_state_current_ball_count = None
        self.game_state_current_score = None
        self.game_state_current_shot_score = None
        self.game_state_current_orange_peg_combo = None
        self.game_state_current_peg_combo = None
        self.game_state_current_fever_meter_multiplier = None
        self.game_state_orange_pegs_remaining = None
        self.game_state_pegs_cleared = None
        self.game_state_has_achieved_fever_meter_multiplier_2x = None
        self.game_state_has_achieved_fever_meter_multiplier_3x = None
        self.game_state_has_achieved_fever_meter_multiplier_5x = None
        self.game_state_has_achieved_fever_meter_multiplier_10x = None
        self.game_state_has_cleared_level = None
        self.game_state_has_achieved_style_shot = None
        self.game_state_has_achieved_3_orange_peg_combo = None
        self.game_state_has_achieved_5_orange_peg_combo = None
        self.game_state_has_achieved_7_peg_combo = None
        self.game_state_has_achieved_15_peg_combo = None
        self.game_state_has_achieved_full_clear = None

        self.option_goal = None
        self.option_shadow_pegs_total = None
        self.option_shadow_pegs_required = None
        self.option_master_selection_mode = None
        self.option_master_selection = None
        self.option_master_count = None
        self.option_level_selection = None
        self.option_level_count = None
        self.option_include_full_clears = None
        self.option_target_score_requirement_mode = None
        self.option_target_score_requirement_percentage = None
        self.option_maximum_starting_ball_count = None
        self.option_useful_item_percentage = None
        self.option_useful_item_weights = None

        self.selected_masters = None
        self.selected_starter_master = None
        self.selected_levels = None
        self.selected_starter_level = None
        self.selected_goal_level = None
        self.target_scores = None
        self.target_score_ratios = None

        self.target_score_locations_by_level = None
        self.useful_items = None
        self.can_modify_ball_count = True
        self.can_modify_fever_meter = True

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

    def assemble_target_score_locations(self) -> None:
        if self.target_scores is None:
            return

        locations: Dict[PeggleNightsLevels, Dict[int, str]] = dict()

        level: PeggleNightsLevels
        for level in self.selected_levels:
            level_prefix: str = f"{level.value} -"

            locations[level] = dict()

            locations[level][self.target_scores[level][0]] = f"{level_prefix} Target Score (Low)"
            locations[level][self.target_scores[level][1]] = f"{level_prefix} Target Score (Mid)"
            locations[level][self.target_scores[level][2]] = f"{level_prefix} Target Score (High)"

        self.target_score_locations_by_level = locations

    def initialize_useful_items(self) -> None:
        useful_items: Dict[PeggleNightsLevels, Dict[PeggleNightsAPUsefulItems, int]] = dict()

        if self.selected_levels is None:
            return

        level: PeggleNightsLevels
        for level in self.selected_levels:
            useful_items[level] = dict()

            item: PeggleNightsAPUsefulItems
            for item in PeggleNightsAPUsefulItems:
                useful_items[level][item] = 0

        if self.selected_goal_level is not None:
            useful_items[self.selected_goal_level] = dict()

            item: PeggleNightsAPUsefulItems
            for item in PeggleNightsAPUsefulItems:
                useful_items[self.selected_goal_level][item] = 0

        self.useful_items = useful_items

    def update(self) -> None:
        if self.game_state_manager.is_process_still_running():
            try:
                self._refresh_game_state()

                self._apply_conditional_game_state()

                self._check_for_completed_locations()
                self._process_received_items()

                self._check_for_victory()
            except Exception:
                import traceback

                with open("peggle_nights_errors.log", "a") as f:
                    f.write(traceback.format_exc() + "\n\n")

    def reset(self) -> None:
        self.received_items = dict()
        self.completed_locations = set()

        self.completed_locations_queue = collections.deque()
        self.received_items_queue = collections.deque()

        self.goal_completed = False

        self.game_state_context = None
        self.game_state_current_game_mode = None
        self.game_state_current_level = None
        self.game_state_level_state = None
        self.game_state_current_character = None
        self.game_state_current_ball_count = None
        self.game_state_current_score = None
        self.game_state_current_shot_score = None
        self.game_state_current_orange_peg_combo = None
        self.game_state_current_peg_combo = None
        self.game_state_current_fever_meter_multiplier = None
        self.game_state_orange_pegs_remaining = None
        self.game_state_pegs_cleared = None
        self.game_state_has_achieved_fever_meter_multiplier_2x = None
        self.game_state_has_achieved_fever_meter_multiplier_3x = None
        self.game_state_has_achieved_fever_meter_multiplier_5x = None
        self.game_state_has_achieved_fever_meter_multiplier_10x = None
        self.game_state_has_cleared_level = None
        self.game_state_has_achieved_style_shot = None
        self.game_state_has_achieved_3_orange_peg_combo = None
        self.game_state_has_achieved_5_orange_peg_combo = None
        self.game_state_has_achieved_7_peg_combo = None
        self.game_state_has_achieved_15_peg_combo = None
        self.game_state_has_achieved_full_clear = None

        self.option_goal = None
        self.option_shadow_pegs_total = None
        self.option_shadow_pegs_required = None
        self.option_master_selection_mode = None
        self.option_master_selection = None
        self.option_master_count = None
        self.option_level_selection = None
        self.option_level_count = None
        self.option_include_full_clears = None
        self.option_target_score_requirement_mode = None
        self.option_target_score_requirement_percentage = None
        self.option_maximum_starting_ball_count = None
        self.option_useful_item_percentage = None
        self.option_useful_item_weights = None

        self.selected_masters = None
        self.selected_starter_master = None
        self.selected_levels = None
        self.selected_starter_level = None
        self.selected_goal_level = None
        self.target_scores = None
        self.target_score_ratios = None

        self.target_score_locations_by_level = None
        self.useful_items = None
        self.can_modify_ball_count = True
        self.can_modify_fever_meter = True

    def _refresh_game_state(self) -> None:
        game_state: GameState = self.game_state_manager.determine_game_state()

        self.game_state_context = game_state.context
        self.game_state_current_game_mode = game_state.current_game_mode
        self.game_state_current_level = game_state.current_level
        self.game_state_level_state = game_state.level_state
        self.game_state_current_character = game_state.current_character
        self.game_state_current_ball_count = game_state.current_ball_count
        self.game_state_current_score = game_state.current_score
        self.game_state_current_shot_score = game_state.current_shot_score
        self.game_state_current_orange_peg_combo = game_state.current_orange_peg_combo
        self.game_state_current_peg_combo = game_state.current_peg_combo
        self.game_state_current_fever_meter_multiplier = game_state.current_fever_meter_multiplier
        self.game_state_orange_pegs_remaining = game_state.orange_pegs_remaining
        self.game_state_pegs_cleared = game_state.pegs_cleared
        self.game_state_has_achieved_fever_meter_multiplier_2x = game_state.has_achieved_fever_meter_multiplier_2x
        self.game_state_has_achieved_fever_meter_multiplier_3x = game_state.has_achieved_fever_meter_multiplier_3x
        self.game_state_has_achieved_fever_meter_multiplier_5x = game_state.has_achieved_fever_meter_multiplier_5x
        self.game_state_has_achieved_fever_meter_multiplier_10x = game_state.has_achieved_fever_meter_multiplier_10x
        self.game_state_has_cleared_level = game_state.has_cleared_level
        self.game_state_has_achieved_style_shot = game_state.has_achieved_style_shot
        self.game_state_has_achieved_3_orange_peg_combo = game_state.has_achieved_3_orange_peg_combo
        self.game_state_has_achieved_5_orange_peg_combo = game_state.has_achieved_5_orange_peg_combo
        self.game_state_has_achieved_7_peg_combo = game_state.has_achieved_7_peg_combo
        self.game_state_has_achieved_15_peg_combo = game_state.has_achieved_15_peg_combo
        self.game_state_has_achieved_full_clear = game_state.has_achieved_full_clear

    def _apply_conditional_game_state(self) -> None:
        if not self.game_state_manager.are_quick_play_levels_unlocked():
            self.game_state_manager.unlock_quick_play_levels()

        return_contexts: List[Union[PeggleNightsContexts, None]] = [
            PeggleNightsContexts.INVALID,
            None,
        ]

        if self.game_state_context in return_contexts:
            self.can_modify_ball_count = True
            self.can_modify_fever_meter = True

            return

        if self.game_state_current_level in self.selected_levels or self.game_state_current_level == self.selected_goal_level:
            # Starting Ball Count
            if self.game_state_current_score > 0:
                self.can_modify_ball_count = True

            if self.can_modify_ball_count and self.game_state_current_score == 0:
                self.can_modify_ball_count = False

                ball_count: int = 5
                ball_count += self.received_items.get(PeggleNightsAPItems.PROGRESSIVE_STARTING_BALL_INCREASE.value, 0)

                self.game_state_manager.set_current_ball_count(ball_count)
                self.game_state_current_ball_count = ball_count

            # Fever Meter Bonus
            if self.game_state_orange_pegs_remaining < 25:
                self.can_modify_fever_meter = True

            if self.can_modify_fever_meter and self.game_state_orange_pegs_remaining == 25:
                self.can_modify_ball_count = False

                if self.game_state_current_level != self.selected_goal_level:
                    useful_item_count: int = self.useful_items[self.game_state_current_level][
                        PeggleNightsAPUsefulItems.FEVER_METER_BONUS
                    ]

                    self.game_state_manager.set_orange_pegs_remaining(25 - useful_item_count)
                    self.game_state_orange_pegs_remaining = 25 - useful_item_count

            # Fever Meter Caps
            fever_meter_caps: Dict[int, Tuple[int, int]] = {
                0: (2, 15),
                1: (3, 10),
                2: (5, 6),
                3: (10, 3),
                4: (10, 0),
            }

            progressive_item_count: int = self.received_items.get(PeggleNightsAPItems.PROGRESSIVE_FEVER_METER.value, 0)

            maximum_multiplier, minimum_orange_pegs_remaining = fever_meter_caps.get(progressive_item_count, (10, 0))

            if self.game_state_manager.get_orange_pegs_remaining() == 0:
                maximum_multiplier *= 10

            if (self.game_state_current_fever_meter_multiplier or 0) > maximum_multiplier:
                self.game_state_manager.set_current_fever_meter_multiplier(maximum_multiplier)
                self.game_state_fever_meter_multiplier = maximum_multiplier

            if (self.game_state_orange_pegs_remaining or 25) < minimum_orange_pegs_remaining:
                self.game_state_manager.set_orange_pegs_remaining(minimum_orange_pegs_remaining)
                self.game_state_orange_pegs_remaining = minimum_orange_pegs_remaining

    def _check_for_completed_locations(self) -> None:
        return_contexts: List[Union[PeggleNightsContexts, None]] = [
            PeggleNightsContexts.INVALID,
            None,
        ]

        if self.game_state_context in return_contexts:
            return

        if self.game_state_current_level is None:
            return
        elif self.game_state_current_level not in self.selected_levels and self.game_state_current_level != self.selected_goal_level:
            return

        level_unlock_item: str = f"Level Unlock: {self.game_state_current_level.value}"

        if level_unlock_item not in self.received_items:
            return
        elif self.received_items[level_unlock_item] < 1:
            return

        if self.selected_goal_level is not None and self.game_state_current_level == self.selected_goal_level:
            if PeggleNightsAPItems.SHADOW_PEG.value not in self.received_items:
                return
            elif self.received_items[PeggleNightsAPItems.SHADOW_PEG.value] < self.option_shadow_pegs_required:
                return

        character_unlock_item: str = f"Master Unlock: {self.game_state_current_character.value}"

        if character_unlock_item not in self.received_items:
            return
        elif self.received_items[character_unlock_item] < 1:
            return

        checked_locations: List[str] = list()

        level_prefix: str = f"{self.game_state_current_level.value} -"

        progressive_fever_meter_count: int = self.received_items.get(PeggleNightsAPItems.PROGRESSIVE_FEVER_METER.value, 0)

        if self.game_state_current_level != self.selected_goal_level:
            if self.game_state_has_achieved_fever_meter_multiplier_2x:
                location: str = f"{level_prefix} Fever Meter X2"
                checked_locations.append(location)

            if self.game_state_has_achieved_fever_meter_multiplier_3x and progressive_fever_meter_count >= 1:
                location: str = f"{level_prefix} Fever Meter X3"
                checked_locations.append(location)

            if self.game_state_has_achieved_fever_meter_multiplier_5x and progressive_fever_meter_count >= 2:
                location: str = f"{level_prefix} Fever Meter X5"
                checked_locations.append(location)

            if self.game_state_has_achieved_fever_meter_multiplier_10x and progressive_fever_meter_count >= 3:
                location: str = f"{level_prefix} Fever Meter X10"
                checked_locations.append(location)

            if self.game_state_current_level in self.target_score_locations_by_level:
                multiplier_item_count: int = self.useful_items[self.game_state_current_level][PeggleNightsAPUsefulItems.SCORE_MULTIPLIER]
                discount_item_count: int = self.useful_items[self.game_state_current_level][PeggleNightsAPUsefulItems.TARGET_SCORE_DISCOUNT]

                current_score: int = round(self.game_state_current_score * (1.0 + (0.05 * multiplier_item_count)), -2)
                discount_ratio: float = 1.0 - (0.05 * discount_item_count)

                target_score_low: int = round(self.target_scores[self.game_state_current_level][0] * discount_ratio, -2)
                target_score_mid: int = round(self.target_scores[self.game_state_current_level][1] * discount_ratio, -2)
                target_score_high: int = round(self.target_scores[self.game_state_current_level][2] * discount_ratio, -2)

                if current_score >= target_score_low:
                    location: str = f"{level_prefix} Target Score (Low)"
                    checked_locations.append(location)

                if current_score >= target_score_mid:
                    location: str = f"{level_prefix} Target Score (Mid)"
                    checked_locations.append(location)

                if current_score >= target_score_high:
                    location: str = f"{level_prefix} Target Score (High)"
                    checked_locations.append(location)

            if self.game_state_has_achieved_style_shot:
                location: str = f"{level_prefix} Style Shot (25,000+)"
                checked_locations.append(location)

            if self.game_state_has_achieved_3_orange_peg_combo:
                location: str = f"{level_prefix} 3 Orange Peg Combo"
                checked_locations.append(location)

            if self.game_state_has_achieved_5_orange_peg_combo:
                location: str = f"{level_prefix} 5 Orange Peg Combo"
                checked_locations.append(location)

            if self.game_state_has_achieved_7_peg_combo:
                location: str = f"{level_prefix} 7 Peg Combo"
                checked_locations.append(location)

            if self.game_state_has_achieved_15_peg_combo:
                location: str = f"{level_prefix} 15 Peg Combo"
                checked_locations.append(location)

            if self.option_include_full_clears:
                required_peg_clears: int = level_to_peg_count[self.game_state_current_level]

                discount_item_count: int = self.useful_items[self.game_state_current_level][
                    PeggleNightsAPUsefulItems.FULL_CLEAR_DISCOUNT
                ]

                required_peg_clears -= discount_item_count

                if (self.game_state_pegs_cleared or 0) >= required_peg_clears:
                    location: str = f"{level_prefix} Full Clear"
                    checked_locations.append(location)

        if self.game_state_has_cleared_level:
            if progressive_fever_meter_count >= 4:
                location: str = f"{level_prefix} Level Clear"
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

            is_fever_meter_bonus: bool = PeggleNightsAPUsefulItems.FEVER_METER_BONUS.value in item
            is_full_clear_discount: bool = PeggleNightsAPUsefulItems.FULL_CLEAR_DISCOUNT.value in item
            is_score_multiplier: bool = PeggleNightsAPUsefulItems.SCORE_MULTIPLIER.value in item
            is_target_score_discount: bool = PeggleNightsAPUsefulItems.TARGET_SCORE_DISCOUNT.value in item

            if (
                is_fever_meter_bonus
                or is_full_clear_discount
                or is_score_multiplier
                or is_target_score_discount
            ):
                split_item: List[str] = item.split(": ")

                useful_item_string: str = split_item[0]
                level_string: str = ": ".join(split_item[1:])

                level: PeggleNightsLevels = PeggleNightsLevels(level_string)
                useful_item: PeggleNightsAPUsefulItems = PeggleNightsAPUsefulItems(useful_item_string)

                self.useful_items[level][useful_item] += 1

    def _check_for_victory(self) -> None:
        if self.option_goal == PeggleNightsAPGoals.SHADOW_PEGS_FINAL_LEVEL:
            if f"{self.selected_goal_level.value} - Level Clear" in self.completed_locations:
                self.goal_completed = True
        elif self.option_goal == PeggleNightsAPGoals.SHADOW_PEG_HUNT:
            if PeggleNightsAPItems.SHADOW_PEG.value in self.received_items:
                if self.received_items[PeggleNightsAPItems.SHADOW_PEG.value] >= self.option_shadow_pegs_required:
                    self.goal_completed = True
