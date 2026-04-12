from typing import List

from dataclasses import dataclass

from Options import (
    Choice,
    OptionDict,
    OptionGroup,
    PerGameCommonOptions,
    Range,
    StartInventoryPool,
    Toggle,
)

from .enums import PeggleDeluxeCharacters, PeggleDeluxeLevels


class Goal(Choice):
    """
    Determines the victory condition.

    Gold Pegs + Final Level: Collect enough Gold Pegs to unlock a Final Level and clear it.
    Gold Peg Hunt: Collect a set number of Gold Pegs spread across the multiworld.
    """
    display_name = "Goal"

    option_gold_pegs_final_level: int = 0
    option_gold_peg_hunt: int = 1

    default = 0


class GoldPegsTotal(Range):
    """
    Determines how many Gold Pegs are in the item pool.

    This number will not be allowed to go over 2 * (number of levels) and will be clamped accordingly if so.
    """

    display_name = "Gold Pegs Total"

    range_start = 1
    range_end = 100

    default = 40


class GoldPegsRequired(Range):
    """
    Determines how many Gold Pegs are required to either win or unlock the final level.

    If this number is higher than the total number of Gold Pegs, it will be set to that number instead.
    """

    display_name = "Gold Pegs Required"

    range_start = 1
    range_end = 100

    default = 30


class MasterSelectionMode(Choice):
    """
    Determines how Masters are selected for the multiworld.

    Single Master: Only one Master will be randomly picked from your selection and usable for the entire game.

    Multiple Masters: Multiple Masters will be randomly picked from your selection.

                      You will be granted a Starting Master. Others will have to be unlocked by receiving their
                      corresponding item before they can be used.
    """

    display_name = "Master Selection Mode"

    option_single_master: int = 0
    option_multiple_masters: int = 1

    default = 1


class MasterSelection(OptionDict):
    """
    Determines which Masters can be considered for inclusion in the multiworld.

    Set any Master you don't want to possibly play as to false.

    At least one Master needs to be selected to play this implementation.
    """

    display_name = "Master Selection"

    valid_keys = {master.value: True for master in PeggleDeluxeCharacters}

    default = valid_keys


class MasterCount(Range):
    """
    Determines how many Masters will be picked from your selection for inclusion in the multiworld.

    If this number is higher than the size of your Master selection, it will be set to that number instead.

    If Master Selection Mode is set to Single Master, this option will be ignored and only 1 Master will be selected.
    """

    display_name = "Master Count"

    range_start = 1
    range_end = 10

    default = 3


class LevelSelection(OptionDict):
    """
    Determines which Levels can be considered for inclusion in the multiworld.

    Set any Level you don't want to possibly play to false.

    A minimum of 5 Levels must be selected to play this implementation.
    """

    display_name = "Level Selection"

    valid_keys = {level.value: True for level in PeggleDeluxeLevels}

    default = valid_keys


class LevelCount(Range):
    """
    Determines how many Levels will be picked from your selection for inclusion in the multiworld.

    If this number is higher than the size of your Level selection, it will be set to that number instead.
    """

    display_name = "Level Count"

    range_start = 5
    range_end = 55

    default = 20


class IncludeFullClears(Toggle):
    """
    If enabled, locations for fully clearing levels will be created when generating the multiworld.

    WARNING: This can be extremely difficult, especially without the proper Masters to tackle each level. Be advised.
    """

    display_name = "Include Full Clears"


class TargetScoreRequirementMode(Choice):
    """
    Determines how Target Score requirements are set.

    Same for All Levels: A single percentage will be applied to the Target Scores of all levels
    Random per Level: Each level will have a random percentage applied to its Target Scores
    """

    display_name = "Target Score Requirement Mode"

    option_same_for_all_levels: int = 0
    option_random_per_level: int = 1

    default = 0


class TargetScoreRequirementPercentage(Range):
    """
    Determines the percentage to apply Target Scores. You will not unlock location checks until
    you reach or exceed the Target Scores on a given level.

    When the requirement mode is set to random per level, the specified percentage will act as the maximum possible.

    The Peggle Deluxe Archipelago client will display the expected scores for each level under the Peggle Deluxe tab.
    """

    display_name = "Target Score Difficulty Percentage"

    range_start = 50
    range_end = 150

    default = 100


class MaximumStartingBallCount(Range):
    """
    Determines the number of balls you will start with after receiving all Progressive Starting Ball Increase items.

    Some of the logic will pivot on this value.
    """

    display_name = "Maximum Starting Ball Count"

    range_start = 8
    range_end = 20

    default = 10


class UsefulItemPercentage(Range):
    """
    Determines what percentage of filler items will get converted to useful items.

    Useful items are: Fever Meter Permanent Bonus, Full Clear Discount, Score Multiplier, Target Score Discount.

    These will make the game slightly easier, but are also level-specific for balance purposes.

    The Peggle Deluxe Archipelago client will display the useful items assigned to each level under the Peggle Deluxe
    tab.
    """

    display_name = "Useful Item Percentage"

    range_start = 0
    range_end = 100

    default = 50


class UsefulItemWeights(OptionDict):
    """
    Determines the relative weights of each useful item type when a useful item replaces a filler item.

    Each weight needs to be at least 1.
    """

    display_name = "Useful Item Weights"

    default = {
        "Fever Meter Permanent Bonus": 1,
        "Full Clear Discount": 1,
        "Score Multiplier": 1,
        "Target Score Discount": 1,
    }


@dataclass
class PeggleDeluxeOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    goal: Goal
    gold_pegs_total: GoldPegsTotal
    gold_pegs_required: GoldPegsRequired
    master_selection_mode: MasterSelectionMode
    master_selection: MasterSelection
    master_count: MasterCount
    level_selection: LevelSelection
    level_count: LevelCount
    include_full_clears: IncludeFullClears
    target_score_requirement_mode: TargetScoreRequirementMode
    target_score_requirement_percentage: TargetScoreRequirementPercentage
    maximum_starting_ball_count: MaximumStartingBallCount
    useful_item_percentage: UsefulItemPercentage
    useful_item_weights: UsefulItemWeights


option_groups: List[OptionGroup] = [
    OptionGroup(
        "Goal Options",
        [
            Goal,
            GoldPegsTotal,
            GoldPegsRequired,
        ],
    ),
    OptionGroup(
        "Master Options",
        [
            MasterSelectionMode,
            MasterSelection,
            MasterCount,
        ],
    ),
    OptionGroup(
        "Level Options",
        [
            LevelSelection,
            LevelCount,
        ],
    ),
    OptionGroup(
        "Location Options",
        [
            IncludeFullClears,
        ],
    ),
    OptionGroup(
        "Target Score Options",
        [
            TargetScoreRequirementMode,
            TargetScoreRequirementPercentage,
        ],
    ),
    OptionGroup(
        "Gameplay Options",
        [
            MaximumStartingBallCount,
        ],
    ),
    OptionGroup(
        "Useful Item Options",
        [
            UsefulItemPercentage,
            UsefulItemWeights,
        ],
    ),
]
