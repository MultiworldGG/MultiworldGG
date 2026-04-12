from dataclasses import dataclass

from .Items import all_categories, get_normal_categories, get_alt_categories
from Options import Choice, DeathLink, OptionGroup, OptionSet, PerGameCommonOptions, Range, Toggle, Visibility


class GameDifficulty(Choice):
    """
    Difficulty. This option determines how difficult the scores are to achieve.
    The difficulties are ordered from easiest to hardest.
    Please try the difficulty to see if it is feasible and fun.
    Best way to test is to see if you can beat the score in logic when all items are unlocked.
    I DO NOT RECOMMEND OUTRAGEOUS AND IMPOSSIBLE FOR MULTIWORLDS
    """

    display_name = "Game difficulty"
    option_easy = 1
    option_medium = 2
    option_hard = 3
    option_extreme = 4
    option_insane = 5
    option_outrageous = 6
    option_impossible = 7
    default = 2


class ScoreForLastCheck(Range):
    """
    The items in the item pool will always allow you to reach a score of 1000.
    By default, the last check is also at a score of 1000.
    However, you can set the score for the last check to be lower. This will make the game shorter and easier.
    """

    display_name = "Score for last check"
    range_start = 500
    range_end = 1000
    default = 1000


class ScoreForGoal(Range):
    """
    This option determines what score you need to reach to finish the game.
    It cannot be higher than the score for the last check (if it is, this option is changed automatically).
    """

    display_name = "Score for goal"
    range_start = 500
    range_end = 1000
    default = 777


class MinimalNumberOfDiceAndRolls(Choice):
    """
    The minimal number of dice and rolls in the pool.
    These are guaranteed, unlike the later items.
    You can never get more than 8 dice and 5 rolls.
    You start with one dice and one roll.
    """

    display_name = "Minimal number of dice and rolls in pool"
    option_5_dice_and_3_rolls = 2
    option_5_dice_and_5_rolls = 3
    option_6_dice_and_4_rolls = 4
    option_7_dice_and_3_rolls = 5
    option_8_dice_and_2_rolls = 6
    default = 2


class NumberDiceFragmentsPerDice(Range):
    """
    Dice can be split into fragments, gathering enough will give you an extra dice.
    You start with one dice, and there will always be one full dice in the pool.
    The other dice are split into fragments, according to this option.
    Setting this to 1 fragment per dice just puts "Dice" objects in the pool.
    """

    display_name = "Number of dice fragments per dice"
    range_start = 1
    range_end = 5
    default = 4


class NumberRollFragmentsPerRoll(Range):
    """
    Rolls can be split into fragments, gathering enough will give you an extra roll.
    You start with one roll, and there will always be one full roll in the pool.
    The other rolls are split into fragments, according to this option.
    Setting this to 1 fragment per roll just puts "Roll" objects in the pool.
    """

    display_name = "Number of roll fragments per roll"
    range_start = 1
    range_end = 5
    default = 4


class TotalNumberOfCategories(Range):
    """
    Number of categories in the game. Note if the list of allowed categories is smaller, there will be fewer categories.
    """

    display_name = "Total number of categories"
    range_start = 1
    range_end = 16
    default = 16


class AllowedNormalCategories(OptionSet):
    """
    Normal categories that are allowed to appear.
    """

    display_name = "Allowed normal categories"
    valid_keys = list(get_normal_categories().keys())
    default = valid_keys


class AllowedAlternativeCategories(OptionSet):
    """
    Alternative categories that are allowed to appear.
    """

    display_name = "Allowed alternative categories"
    valid_keys = list(get_alt_categories().keys())
    default = valid_keys


class PercentageAlternativeCategories(Range):
    """
    How likely alternative categories are to appear. 0 means no chance, 100 means only alternative categories.

    """

    display_name = "Likeliness of alternative categories"
    range_start = 0
    range_end = 100
    default = 0


class AllowedStartingCategories(OptionSet):
    """
    Set of categories that may appear as starting categories.
    Leave this empty to have randomly selected starting categories.
    If this list is smaller than the number of starting categories you want, random categories are added as starting.
    """

    display_name = "Allowed starting categories"
    valid_keys = all_categories
    default = [
        "Category Choice",
        "Category Double Threes and Fours",
        "Category Inverse Choice",
        "Category Quadruple Ones and Twos",
    ]


class NumberOfStartingCategories(Range):
    """
    Number of categories from the list of allowed starting categories that you start your game with.
    Note that you may start with more dice or rolls if the starting categories are really bad or require many dice.
    """

    range_start = 1
    range_end = 16
    default = 2


class FillStartInventoryIfNeeded(Toggle):
    """
    Hidden option.
    If you only pick categories that need many dice or rolls, you might get stuck early on.
    If this option is on, you will start with as many extra dice or rolls needed to get to a score of 5 at the start.
    When this option is off and you have difficult categories, other games in multiworld might save you.
    """

    visibility = Visibility.none
    display_name = "Fill start inventory if needed"
    default = True


class ChanceOfDice(Range):
    """
    The item pool is always filled in such a way that you can reach a score of 1000.
    Extra progression items are added that will help you on your quest.
    You can set the weight for each extra progressive item in the following options.

    Of course, more dice = more points!
    """

    display_name = "Weight of adding Dice"
    range_start = 0
    range_end = 100
    default = 5


class ChanceOfRoll(Range):
    """
    With more rolls, you will be able to reach higher scores.
    """

    display_name = "Weight of adding Roll"
    range_start = 0
    range_end = 100
    default = 20


class ChanceOfFixedScoreMultiplier(Range):
    """
    Getting a Fixed Score Multiplier will boost all future scores by 10%.
    """

    display_name = "Weight of adding Fixed Score Multiplier"
    range_start = 0
    range_end = 100
    default = 30


class ChanceOfStepScoreMultiplier(Range):
    """
    The Step Score Multiplier boosts your multiplier after every roll by 1%, and resets on sheet reset.
    So, keep high scoring categories for later to get the most out of them.
    By default, this item is not included. It is fun however, you just need to know the above strategy.
    """

    display_name = "Weight of adding Step Score Multiplier"
    range_start = 0
    range_end = 100
    default = 0


class ChanceOfDoubleCategory(Range):
    """
    This option allows categories to appear multiple times.
    Each time you get a category after the first, its score value gets doubled.
    """

    display_name = "Weight of adding Category copy"
    range_start = 0
    range_end = 100
    default = 50


class DoubleCategoryCalculation(Choice):
    """
    This option determines how the score of a category is calculated when it appears multiple times.
    double: the multiplier is doubled each time the category is obtained.
    increment: the multiplier is increased by 1 each time the category is obtained.
    """

    display_name = "Double category calculation"
    option_double = 1
    option_increment = 2
    default = 1


class ChanceOfPoints(Range):
    """
    Are you tired of rolling dice countless times and tallying up points one by one, all by yourself?
    Worry not, as this option will simply add some points items to the item pool!
    And getting one of these points items gives you... points!
    Imagine how nice it would be to find tons of them. Or even better, having others find them FOR you!
    """

    display_name = "Weight of adding Points"
    range_start = 0
    range_end = 100
    default = 20


class PointsSize(Choice):
    """
    If you choose to add points to the item pool, you can choose to have many small points,
    medium-size points, a few larger points, or a mix of them.
    """

    display_name = "Size of points"
    option_small = 1
    option_medium = 2
    option_large = 3
    option_mix = 4
    default = 2


class MinimizeExtraItems(Choice):
    """
    Besides necessary items, Yacht Dice has extra useful/filler items in the item pool.
    It is possible however to decrease the number of locations and extra items.
    This option will:
    - decrease the number of locations at the start (you'll start with 2 dice and 2 rolls).
    - will limit the number of dice/roll fragments per dice/roll to 2.
    - in multiplayer games, it will reduce the number of filler items.
    """

    display_name = "Minimize extra items"
    option_no_dont = 1
    option_yes_please = 2
    default = 1


class AddExtraPoints(Choice):
    """
    Yacht Dice typically has space for extra items.
    This option determines if bonus points are put into the item pool.
    They make the game a little bit easier, as they are not considered in the logic.

    All Of It: fill all locations with extra points
    Sure: put some bonus points in
    Never: do not put any bonus points
    """

    display_name = "Extra bonus in the pool"
    option_all_of_it = 1
    option_sure = 2
    option_never = 3
    default = 2


class AddStoryChapters(Choice):
    """
    Yacht Dice typically has space for more items.
    This option determines if extra story chapters are put into the item pool.
    Note: if you have extra points on "all_of_it", there will not be story chapters.

    All Of It: fill all locations with story chapters
    Sure: if there is space left, put in 10 story chapters.
    Never: do not put any story chapters in, I do not like reading (but I am glad you are reading THIS!)
    """

    display_name = "Extra story chapters in the pool"
    option_all_of_it = 1
    option_sure = 2
    option_never = 3
    default = 3


class WhichStory(Choice):
    """
    The most important part of Yacht Dice is the narrative.
    Of course you will need to add story chapters to the item pool.
    You can read story chapters in the feed on the website and there are several stories to choose from.
    """

    display_name = "Story"
    option_the_quest_of_the_dice_warrior = 1
    option_the_tragedy_of_fortunas_gambit = 2
    option_the_dicey_animal_dice_game = 3
    option_whispers_of_fate = 4
    option_a_yacht_dice_odyssey = 5
    option_a_rollin_rhyme_adventure = 6
    option_random_story = -1
    default = -1


class AllowManual(Choice):
    """
    If allowed, players can roll IRL dice and input them manually into the game.
    By sending "manual" in the chat, an input field appears where you can type your dice rolls.
    Of course, we cannot check anymore if the player is playing fair.
    """

    display_name = "Allow manual inputs"
    option_yes_allow = 1
    option_no_dont_allow = 2
    default = 1


class IncludeScores(OptionSet):
    """
    Scores in this set will always be included.
    Note that if you put many scores here, there will be many filler items too.
    You can put numbers 1 up to (including) 1000. Note that scores above last check don't count.
    You can also set this option to just ['Everything'], this adds all possible scores to the pool (up to last check).
    Note: only the 10 lowest entries in your list are considered ('Everything' adds all scores anyway though).
    """

    display_name = "Guaranteed included scores as locations"
    valid_keys = [str(i) for i in range(1, 1001)] + ["Everything"]
    default = ["1"]


class MaximumRNGInItempool(Range):
    """
    When you add many or all scores in the above option, the item pool will be filled with many filler "RNG" items.
    This option determines the maximum number of filler items in the item pool and possibly put in other worlds.
    """

    display_name = "Maximum RNG In Itempool"
    range_start = 0
    range_end = 1000
    default = 50


class ReceiveDeathLink(Toggle):
    """
    With this option on, your current game will be reset when someone else in the multiworld dies.
    """

    display_name = "Receive death link"
    default = False


class SendDeathLink(Toggle):
    """
    With this option on, other players with deathlink will die when you put a "0" in one of the categories.
    Instead of putting a 0, you can just reset your game and the other players will be fine.
    So, this deathlink is very much preventable if you pay attention not to put a 0.
    When you put a 0, your own game will be reset as well.
    """

    display_name = "Send death link"
    default = False


class NumberOfKeys(Range):
    """
    Add this many keys to the itempool. You need *all* keys to be able to do anything in the game.
    """

    visibility = Visibility.none
    display_name = "Number of keys"
    range_start = 0
    range_end = 100
    default = 0


@dataclass
class YachtDiceOptions(PerGameCommonOptions):
    game_difficulty: GameDifficulty
    score_for_last_check: ScoreForLastCheck
    score_for_goal: ScoreForGoal

    minimal_number_of_dice_and_rolls: MinimalNumberOfDiceAndRolls
    number_of_dice_fragments_per_dice: NumberDiceFragmentsPerDice
    number_of_roll_fragments_per_roll: NumberRollFragmentsPerRoll

    total_number_of_categories: TotalNumberOfCategories
    allowed_normal_categories: AllowedNormalCategories
    allowed_alternative_categories: AllowedAlternativeCategories
    percentage_alternative_categories: PercentageAlternativeCategories
    number_of_starting_categories: NumberOfStartingCategories
    allowed_starting_categories: AllowedStartingCategories
    fill_start_inventory_if_needed: FillStartInventoryIfNeeded

    allow_manual_input: AllowManual

    # the following options determine what extra items are shuffled into the pool:
    weight_of_dice: ChanceOfDice
    weight_of_roll: ChanceOfRoll
    weight_of_fixed_score_multiplier: ChanceOfFixedScoreMultiplier
    weight_of_step_score_multiplier: ChanceOfStepScoreMultiplier
    weight_of_double_category: ChanceOfDoubleCategory
    double_category_calculation: DoubleCategoryCalculation
    weight_of_points: ChanceOfPoints
    points_size: PointsSize

    minimize_extra_items: MinimizeExtraItems
    add_bonus_points: AddExtraPoints
    add_story_chapters: AddStoryChapters
    which_story: WhichStory

    include_scores: IncludeScores
    maximum_rng_in_itempool: MaximumRNGInItempool

    receive_death_link_toggle: ReceiveDeathLink
    send_death_link_toggle: SendDeathLink

    number_of_keys: NumberOfKeys


yd_option_groups = [
    OptionGroup(
        "Categories",
        [
            TotalNumberOfCategories,
            AllowedNormalCategories,
            AllowedAlternativeCategories,
            PercentageAlternativeCategories,
            AllowedStartingCategories,
            NumberOfStartingCategories,
            FillStartInventoryIfNeeded,
        ],
    ),
    OptionGroup(
        "Extra progression items",
        [
            ChanceOfDice,
            ChanceOfRoll,
            ChanceOfFixedScoreMultiplier,
            ChanceOfStepScoreMultiplier,
            ChanceOfDoubleCategory,
            DoubleCategoryCalculation,
            ChanceOfPoints,
            PointsSize,
        ],
    ),
    OptionGroup(
        "Other items",
        [
            MinimizeExtraItems,
            AddExtraPoints,
            AddStoryChapters,
            WhichStory,
        ],
    ),
    OptionGroup(
        "Misc",
        [
            IncludeScores,
            MaximumRNGInItempool,
            AllowManual,
            ReceiveDeathLink,
            SendDeathLink,
            NumberOfKeys,
        ],
    ),
]
