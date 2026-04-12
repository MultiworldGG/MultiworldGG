from typing import List

from dataclasses import dataclass

from Options import (
    Choice,
    DefaultOnToggle,
    OptionDict,
    OptionGroup,
    PerGameCommonOptions,
    Range,
    StartInventoryPool,
    Toggle,
)

from .data_funcs import generate_dlc_table_strings


class Goal(Choice):
    """
    Determines the victory condition.

    Shiny Quarters + Final Table: Collect enough Shiny Quarters to unlock a Final Table and get a high score on it.
    Shiny Quarter Hunt: Collect a set number of Shiny Quarters spread across the multiworld.
    """
    display_name = "Goal"

    option_shiny_quarters_final_table: int = 0
    option_shiny_quarter_hunt: int = 1

    default = 0


class ShinyQuartersTotal(Range):
    """
    Determines how many Shiny Quarters are in the item pool.

    This number will not be allowed to go over 2 * (number of pinball tables) and will be clamped accordingly if so.
    """

    display_name = "Shiny Quarters Total"

    range_start = 1
    range_end = 100

    default = 20


class ShinyQuartersRequired(Range):
    """
    Determines how many Shiny Quarters are required to either win or unlock the final table.

    If this number is higher than the total number of Shiny Quarters, it will be set to that number instead.
    """

    display_name = "Shiny Quarters Required"

    range_start = 1
    range_end = 100

    default = 15


class PinballTableSelection(OptionDict):
    """
    Determines which Pinball Tables can be considered for inclusion in the multiworld.

    Set any table you don't own (or don't want to play) for Pinball FX3 to false.

    A minimum of 6 Pinball Tables must be selected to play this implementation.
    """

    display_name = "Pinball Table Selection"

    valid_keys = {string: True for string in generate_dlc_table_strings()}

    default = valid_keys


class PinballTableCount(Range):
    """
    Determines how many Pinball Tables will be picked from your table selection for inclusion in the multiworld.

    If this number is higher than the size of your Pinball Table selection, it will be set to that number instead.

    Note: Setting this value below 10 could extremely rarely lead to generation failures when paired with other
          restrictive options.
    """

    display_name = "Pinball Table Count"

    range_start = 6
    range_end = 100

    default = 10


class ExcludeHighTierTargetScores(DefaultOnToggle):
    """
    If enabled, locations for High-Tier Target Scores will not be created when generating the multiworld.
    If your goal includes a final table, the Target Score will shift to the Mid-Tier Target Score instead.

    Disabling this option will add more locations, but will also place additional player skill expectations on you.
    """

    display_name = "Exclude High-Tier Target Scores"


class TargetScoreRequirementMode(Choice):
    """
    Determines how Target Score requirements are set.

    Same for All Tables: A single percentage will be applied to the Target Scores of all tables
    Random per Table: Each table will have a random percentage applied to its Target Scores
    """

    display_name = "Target Score Requirement Mode"

    option_same_for_all_tables: int = 0
    option_random_per_table: int = 1

    default = 0


class TargetScoreRequirementPercentage(Range):
    """
    Determines the percentage to apply Target Scores. You will not unlock location checks until
    you reach or exceed the Target Scores on a given table.

    This only applies to Single-Player mode play.

    When the requirement mode is set to random per table, the specified percentage will act as the maximum possible.

    The Pinball FX3 Archipelago client will display the expected scores for each table under the Pinball FX3 tab.

    WARNING: Values over 100 are intended for players experienced with scoring high on various pinball tables.
             More casual players may never be able to reach the resulting Target Scores. Be advised.
    """

    display_name = "Target Score Difficulty Percentage"

    range_start = 50
    range_end = 300

    default = 100


class ProgressiveChallengeAccess(DefaultOnToggle):
    """
    If enabled, Challenge Access items will unlock Challenge tiers in a progressive manner, meaning you will gain
    access to Low -> Mid -> High-Tier sequentially for each Challenge type. This should smooth the difficulty curve,
    allowing you to collect some useful items by the time you reach High-Tier Challenges.

    For a more challenging / chaotic experience, disable this option. Expect to possibly have to obtain High-Tier
    Challenge stars very early on, before Low or Mid-Tier stars and sometimes without any useful items helping you out.
    """

    display_name = "Progressive Challenge Access"


class ExcludeHighTierChallengeStars(Choice):
    """
    Determines whether High-Tier Challenge Stars are excluded from the multiworld and under what conditions.

    Exclude All: No High-Tier Challenge Star locations will be created.
    Exclude Only 1 Ball: High-Tier Challenge Star locations for 1-Ball challenges will not be created.
    Do Not Exclude: All High-Tier Challenge Star locations will be created.

    Including High-Tier Challenge Stars will add more locations, but will also place additional player skill
    expectations on you.
    """

    display_name = "Exclude High-Tier Challenge Stars"

    option_exclude_all: int = 0
    option_exclude_only_1_ball: int = 1
    option_do_not_exclude: int = 2

    default = 0


class ChallengeStarRequirementMode(Choice):
    """
    Determines how Challenge Star requirements are set.

    Same for All Tables: A single Star requirement will be applied to all tables for each challenge tier
    Random per Table: Each table will have random Star requirements for each challenge tier
    """

    display_name = "Challenge Star Requirement Mode"

    option_same_for_all_tables: int = 0
    option_random_per_table: int = 1

    default = 0


class ChallengeLowTierStarRequirement(Range):
    """
    Determines how many Stars you need to obtain to check low-tier challenge locations.

    When the requirement mode is set to random per table, the specified number will act as the maximum possible.

    The Pinball FX3 Archipelago client will display the Star requirements for each table under the Pinball FX3 tab.
    """

    display_name = "Challenge Low-Tier Star Requirement"

    range_start = 1
    range_end = 5

    default = 3


class ChallengeMidTierStarRequirement(Range):
    """
    Determines how many Stars you need to obtain to check mid-tier challenge locations.

    When the requirement mode is set to random per table, the specified number will act as the maximum possible.

    The Pinball FX3 Archipelago client will display the Star requirements for each table under the Pinball FX3 tab.
    """

    display_name = "Challenge Mid-Tier Star Requirement"

    range_start = 6
    range_end = 10

    default = 8


class ChallengeHighTierStarRequirement(Range):
    """
    Determines how many Stars you need to obtain to check high-tier challenge locations.

    When the requirement mode is set to random per table, the specified number will act as the maximum possible.

    The Pinball FX3 Archipelago client will display the Star requirements for each table under the Pinball FX3 tab.

    WARNING: Getting more than 11 Stars can be extremely difficult on certain challenges. It is recommended to start
             at 11 and increase only if you are confident you can handle it.
    """

    display_name = "Challenge High-Tier Star Requirement"

    range_start = 11
    range_end = 15

    default = 11


class Starsanity(Toggle):
    """
    If enabled, every Star obtained below the requirement of each tier will also count as a location check.

    Examples: If the Star requirements for a table are 3 / 8 / 11, you will get additonal location checks for
              1 / 2 / 6 / 7 Stars as well.

              If the Star requirements for a table are 4 / 9 / 12, you will get additional location checks for
              1 / 2 / 3 / 6 / 7 / 8 / 11 Stars as well.

    WARNING: This will add a proportionally large amount of filler / useful items to the pool.
    """

    display_name = "Starsanity"


class UsefulItemPercentage(Range):
    """
    Determines what percentage of filler items will get converted to useful items.

    Useful items are: Target Score Discount, Target Score Multiplier, Star Requirement Discount

    These will make the game slightly easier, but are also table-specific for balance purposes.

    The Pinball FX3 Archipelago client will display the useful items assigned to each table under the Pinball FX3 tab.
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
        "Score Multiplier": 1,
        "Star Requirement Discount": 1,
        "Target Score Discount": 1,
    }


@dataclass
class PinballFX3Options(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    goal: Goal
    shiny_quarters_total: ShinyQuartersTotal
    shiny_quarters_required: ShinyQuartersRequired
    pinball_table_selection: PinballTableSelection
    pinball_table_count: PinballTableCount
    exclude_high_tier_target_scores: ExcludeHighTierTargetScores
    target_score_requirement_mode: TargetScoreRequirementMode
    target_score_requirement_percentage: TargetScoreRequirementPercentage
    progressive_challenge_access: ProgressiveChallengeAccess
    exclude_high_tier_challenge_stars: ExcludeHighTierChallengeStars
    challenge_star_requirement_mode: ChallengeStarRequirementMode
    challenge_low_tier_star_requirement: ChallengeLowTierStarRequirement
    challenge_mid_tier_star_requirement: ChallengeMidTierStarRequirement
    challenge_high_tier_star_requirement: ChallengeHighTierStarRequirement
    starsanity: Starsanity
    useful_item_percentage: UsefulItemPercentage
    useful_item_weights: UsefulItemWeights


option_groups: List[OptionGroup] = [
    OptionGroup(
        "Goal Options",
        [
            Goal,
            ShinyQuartersTotal,
            ShinyQuartersRequired,
        ],
    ),
    OptionGroup(
        "Pinball Table Options",
        [
            PinballTableSelection,
            PinballTableCount,
        ],
    ),
    OptionGroup(
        "Target Score Options",
        [
            ExcludeHighTierTargetScores,
            TargetScoreRequirementMode,
            TargetScoreRequirementPercentage,
        ],
    ),
    OptionGroup(
        "Challenge Star Options",
        [
            ProgressiveChallengeAccess,
            ExcludeHighTierChallengeStars,
            ChallengeStarRequirementMode,
            ChallengeLowTierStarRequirement,
            ChallengeMidTierStarRequirement,
            ChallengeHighTierStarRequirement,
        ],
    ),
    OptionGroup(
        "Sanity Options",
        [
            Starsanity,
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
