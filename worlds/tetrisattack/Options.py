from Options import PerGameCommonOptions, DeathLink, Choice, Toggle, DefaultOnToggle, Range
from dataclasses import dataclass

class StageClearGoal(DefaultOnToggle):
    """This makes Stage Clear Last Stage Clear one of the goals (you will need to complete all goals for the seed).
    If multiple modes need to be cleared, each will provide a final item and auto-hint the other win conditions.
    Note that if you don't start in round 6, the Last Stage unlock will be in Stage Clear Round 6 Clear."""


class PuzzleGoal(Choice):
    """This makes Puzzle and/or Extra Puzzle Round 6 Clear one of the goals (you will need to complete all goals for the seed).
    If multiple modes need to be cleared, each will provide a final item and auto-hint the other win conditions."""
    option_no_puzzle = 0
    option_puzzle = 1
    option_extra_puzzle = 2
    option_puzzle_and_extra_puzzle = 3
    option_puzzle_or_extra_puzzle = 4
    default = 1


class PuzzleAllClear(Toggle):
    """This makes the Puzzle goal require all 6 or 12 round clears, and thus all puzzles, instead of just the last round clear."""
    # TODO: Use this toggle


class VersusGoal(Choice):
    """This makes Versus one of the goals (you will need to complete all goals for the seed).
    If multiple modes need to be cleared, each will provide a final item and auto-hint the other win conditions.
    Note that harder difficulties will be forced to end at the goal difficulty's final stage.
    If Easy Bowser is enabled for Easy or Normal, the goal becomes Stage 12 at that difficulty.
    Stages that come after the goal stage will be extra unlocks and checks."""
    option_no_vs = 0
    option_easy = 1
    option_normal = 2
    option_hard = 3
    option_very_hard = 4
    # option_very_hard_no_continues = 5
    default = 2


class EasyBowser(Toggle):
    """When enabled, Kamek can be fought on Easy, and Bowser can be fought on Easy and Normal.
    This also changes the goal stage number for Easy and Normal goals."""


class StageClearInclusion(Toggle):
    """This adds Stage Clear to the randomizer, even if they are not part of the goal.
    Note that if the Last Stage is a goal, this won't have any effect."""


class PuzzleInclusion(Choice):
    """This adds Puzzles to the randomizer, even if they are not part of the goal.
    Note that if (Extra) Puzzle Round 6 Clear is a goal, this won't have any effect unless the other set is not a goal."""
    option_no_puzzle = 0
    option_puzzle = 1
    option_extra_puzzle = 2
    option_puzzle_and_extra_puzzle = 3
    default = 0


class VersusInclusion(Toggle):
    """This adds Versus to the randomizer, even if they are not part of the goal.
    Note that if clearing Versus is a goal, this won't have any effect."""


class StarterPack(Choice):
    """This provides a set of stages and puzzles to start with.
    If you're doing Stage Clear only and you don't start in Round 6, the Last Stage will be in Round 6.
    Starting with only one Stage Clear round has all 5 stages in that round unlocked.
    Starting with only one Puzzle level has all 10 puzzles in that level unlocked.
    If there are only extra puzzles and no regular puzzles, the starter level is corrected as such.
    Vs Two Stages gives stages 1 and 2."""
    option_stage_clear_round_1 = 0
    option_stage_clear_round_2 = 1
    option_stage_clear_round_3 = 2
    option_stage_clear_round_4 = 3
    option_stage_clear_round_5 = 4
    option_stage_clear_round_6 = 5
    option_puzzle_level_1 = 6
    option_puzzle_level_2 = 7
    option_puzzle_level_3 = 8
    option_puzzle_level_4 = 9
    option_puzzle_level_5 = 10
    option_vs_two_stages = 11
    # option_first_of_each = 12 # First Of Each option provides the first Stage Clear round, Puzzle (and Extra) level, and the first Vs stage.
    # option_first_stage_of_each = 13 # First Stage Of Each only provides one stage each.
    default = 0


class AutoHints(DefaultOnToggle):
    """If enabled, goal items are auto-hinted after completing a mode"""


class StageClearFiller(DefaultOnToggle):
    """If enabled, the game will maximize the number of locations (aside from additional Special Stages) and add more filler items to the pool.
    Note that there are situations where filler is forced, otherwise the logic would be too tight and lead to unbeatable seeds."""


class PuzzleFiller(DefaultOnToggle):
    """If enabled, the game will maximize the number of locations and add more filler items to the pool.
    Note that there are situations where filler is forced, otherwise the logic would be too tight and lead to unbeatable seeds."""


class VersusFiller(DefaultOnToggle):
    """If enabled, the game will maximize the number of locations (aside from higher difficulty levels) and add more filler items to the pool.
    Note that there are situations where filler is forced, otherwise the logic would be too tight and lead to unbeatable seeds."""


class StageClearMode(Choice):
    """Determines how progression works in Stage Clear.
    Whole Rounds puts each round as one item.
    Individual Stages puts each round as 5 progressive items. All 5 are needed to start a round.
    Incremental puts each round as 5 progressive items with optional gate.
    Skippable puts each round as 5 or 6 items. You can start a round with some stages locked, but all 5 stages are needed for the Round Clear."""
    option_whole_rounds = 0
    option_individual_stages = 1
    option_incremental = 2
    option_incremental_with_round_gate = 3
    option_skippable = 4
    option_skippable_with_round_gate = 5
    default = 3


class StageClearSaves(DefaultOnToggle):
    """If enabled, Stage Clear will let you resume rounds at the first unchecked stage or the stage after the last cleared one, whichever is earlier"""


class SpecialStageTraps(Range):
    """Adds extra locations to certain Stage Clear stages such as Round 3 Clear, but as a consequence adds the Special Stage trap.
    When tripped, you must either win or lose the Special Stage before you can continue.
    Requires Stage Clear to be included or as a goal."""
    # TODO_AFTER: Enable Special Stage traps when Stage Clear is not included after making a new main menu
    range_start = 0
    range_end = 30
    default = 1


class SpecialStageHPMultiplier(Range):
    """Changes Bowser's HP to this times 100 in the Special Stage traps. Default (vanilla) is 6 (x100)."""
    range_start = 1
    range_end = 100
    default = 6


class LastStageHPMultiplier(Range):
    """Changes Bowser's HP to this times 100 at the Last Stage. Default (vanilla) is 6 (x100).
    For reference, a x2 Chain does 50 damage while a x6 Chain does a total of 980 damage."""
    range_start = 1
    range_end = 100
    default = 6


class ShockPanelChecks(Range):
    """Number of items to add to the item pool locked behind clearing shock panels (gray ! panels) in Stage Clear.
    Multiply by the panels per check for the total panel count in your slot.
    For reference, one panel will spawn per row but will step up to two panels per row if you fall behind."""
    range_start = 0
    range_end = 100
    default = 0


class ShockPanelsPerCheck(Range):
    """Number of shock panels required to unlock each check.
    This also determines the number of panels you get each time you receive the item."""
    range_start = 1
    range_end = 20
    default = 4


class ShockPanelBias(Choice):
    """Determines the pattern of items that shock panels unlock.
    The randomizer will try to fill these locations first with what the item pool has.
    Selecting traps will cause shock panels themselves to be labeled as traps."""
    option_no_bias = 0
    option_progression_and_useful = 1
    option_useful_and_filler = 2
    option_traps = 3
    option_progression_and_traps = 4
    option_traps_and_filler = 5
    default = 0


class PuzzleMode(Choice):
    """Determines how progression works in Puzzle.
    Whole Levels puts each level as one item.
    Individual Stages puts each level as 10 progressive items. All 10 are needed to start a level.
    Incremental puts each level as 10 progressive items with optional gate.
    Skippable puts each level as 10 or 11 items. You can start a level with some puzzles locked, but all 10 puzzles are needed for the Round Clear."""
    option_whole_levels = 0
    option_individual_stages = 1
    option_incremental = 2
    option_incremental_with_level_gate = 3
    option_skippable = 4
    option_skippable_with_level_gate = 5
    default = 3


class ExtraPuzzleBehindRegular(Choice):
    """Determines the relationship between regular puzzles and extra puzzles when both are included.
    Think of it as deciding on either 12 levels containing 10 puzzles or 6 levels containing 20 puzzles.
    Separate treats each regular and extra level as independent regions.
    Passive still keeps them separate but tells Archipelago that the regular puzzles are logically required first.
    Doing extra puzzles before their respective regular counterparts is considered out of logic.
    Strict makes each extra level require clearing their respective regular level.
    Followup halves the number of unlocks in the item pool, and clearing in the regular level automatically unlocks their extra counterpart.
    Followup can generate a lot of filler items.
    NOTE: Extra Puzzles are not integrated yet."""
    option_separate = 0
    option_passive = 1
    option_strict = 2
    option_followup = 3
    default = 1


class VersusMode(Choice):
    """Determines how difficulty levels are handled and which ones have locations.
    Minimum puts locations on the minimum difficulty level required for each stage except for the last stage.
    For example, if the goal is to beat Vs on Hard, stages 1 to 10 will still give checks on Easy.
    If filler is included, higher difficulties for early stages are considered non-priority.
    Minimum progressive is the same as above, but adds one set of unlocks as progressive from 1 to 10/11/12.
    Goal puts locations on the goal difficulty level only, and also forces the game to that difficulty.
    Goal progressive is the same as above, but adds one set of unlocks as progressive from 1 to 10/11/12."""
    option_minimum_difficulty = 0
    option_minimum_progressive = 1
    option_goal_difficulty = 2
    option_goal_progressive = 3
    # option_progressive_per_stage = 4
    # Progressive per stage puts each stage as their own set of progressive unlocks from Easy to the goal difficulty.
    # Using this option with V. Hard will put 45 or 48 unlocks in the pool.
    # option_marathon = 5 # Marathon puts one large set of progressive unlocks in the pool for all stages and difficulties.
    default = 3


class VersusAutoCompleteEasierLevels(DefaultOnToggle):
    """When enabled, clearing a stage on a higher difficulty is the same as clearing a stage on easier difficulties."""


class FriendshipGate(DefaultOnToggle):
    """When enabled, Versus stages 9 to 12 require all 8 recruitable characters (for all difficulty levels simultaneously).
    Otherwise, the Mt. Wickedness Gate is added to the item pool (for each difficulty level if applicable)."""


class OverworldShuffle(DefaultOnToggle):
    """When enabled, Versus stages 1 to 8 are shuffled."""


class ChainsCheckLimit(Range):
    """Adds a number of locations that are checked when you perform a chain level, starting from x2. Set to 1 to not include.
    The highest level chain will always have a non-progression item. 14 corresponds to the "x?" chain."""
    range_start = 1
    range_end = 14
    default = 6


class CombosCheckLimit(Range):
    """Adds a number of locations that are checked for each combo, starting from 4 combos. Set to 3 to not include."""
    range_start = 3
    range_end = 12
    default = 10


class MusicFilter(Choice):
    """Pick the categories of music you want to disable. Menu music also includes the title screen."""
    option_disable_no_music = 0
    option_disable_menu_music = 1
    option_disable_all_music = 3
    default = 0


@dataclass
class TetrisAttackOptions(PerGameCommonOptions):
    starter_pack: StarterPack
    stage_clear_goal: StageClearGoal
    puzzle_goal: PuzzleGoal
    versus_goal: VersusGoal
    stage_clear_inclusion: StageClearInclusion
    puzzle_inclusion: PuzzleInclusion
    versus_inclusion: VersusInclusion
    # autohints: AutoHints
    death_link: DeathLink
    stage_clear_mode: StageClearMode
    stage_clear_filler: StageClearFiller
    stage_clear_saves: StageClearSaves
    special_stage_trap_count: SpecialStageTraps
    special_stage_hp_multiplier: SpecialStageHPMultiplier
    last_stage_hp_multiplier: LastStageHPMultiplier
    shock_panel_checks: ShockPanelChecks
    shock_panels_per_check: ShockPanelsPerCheck
    # shock_panel_bias: ShockPanelBias
    puzzle_mode: PuzzleMode
    puzzle_filler: PuzzleFiller
    # extra_puzzle_behind_regular: ExtraPuzzleBehindRegular
    versus_mode: VersusMode
    versus_easy_bowser: EasyBowser
    music_filter: MusicFilter