import typing
import dataclasses

from Options import Range, Choice, PerGameCommonOptions, Toggle
from dataclasses import dataclass

class Progression(Choice):
    """
    Free Duel mode means progression will be made through the Free Duel menu
    culminating in a fight against Yami Yugi.
    Your game will be longer per duelist you set to play against.
    You do not enter tournaments in this mode.

    Tournament mode means progression will be made in Tournaments with the
    goal being completing The Last Judgement in the Dark Tournament Division.
    24 - 72 duel wins required, depending on checks you receive.
    """
    display_name = "Goal"
    option_free_duel = 0
    option_tournaments = 1
    default = 0

class TournamentRewards(Choice):
    """
    This option only matters when your Progression mode is Tournament.

    Choose whether you will be awarded one, two or three checks every time
    you complete a Tournament.
    """
    display_name = "Tournament Rewards"
    option_one = 0
    option_two = 1
    option_three = 2
    default = 2

class FreeDuelRewards(Choice):
    """
    This option only matters when your Progression mode is Free Duel.

    Choose whether you will be awarded one or two checks every time
    a duelist is defeated in Free Duel.
    """
    display_name = "Free Duel Rewards"
    option_one = 0
    option_two = 1
    default = 1

class StartingDuelists(Range):
    """
    This option only matters when your Progression mode is Free Duel.
     
    The number of Duelists to start with unlocked.
    """
    display_name = "Starting Duelists"
    range_start = 1
    range_end = 91
    default = 10

class FreeDuelGoal(Range):
    """
    This option only matters when your Progression mode is Free Duel.

    The number of duelists defeated required to unlock your goal duel (against Yami Yugi).
    A higher number leads to a longer game.
    """
    display_name = "Free Duel Goal"
    range_start = 1
    range_end = 91
    default = 45

class DiceStats(Choice):
    """
    The double option changes all dice crest faces to have
    double their normal value. This can reduce the amount of time
    spent rolling for necessary crests in battle and can give
    AI opponents a little more bite than normal.
    Normal leaves crest faces as they are in vanilla gameplay.
    """
    display_name = "Dice Stats"
    option_normal = 0
    option_double = 1
    default = 1

class RandomizeStartingDice(Toggle):
    """
    In the base game your starting pool is lightly randomized to begin with,
    but this setting takes off the guardrails and generates you with any
    15 dice from the game (no duplicates).

    It is impossible to generate a starting pool with only items and no creatures to summon.

    With this option active you have to select all of your new dice from your collection
    before the first duel begins.
    """
    display_name = "Randomize Starting Dice"

class BonusItemMode(Choice):
    """
    Decide what you would like to receive from filler checks.

    Random Dice will reward any random die from the game.
    In Tournament Progression mode, Grandpa's Shop can still progress
    although it is quite slow. Approximately 3-6 Tournament wins per shop level.

    Shop Progress makes collecting Dice locations. You may be required
    to buy dice from Grandpa's Shop to progress. This mode will divide the 
    number of filler checks between Shop Levels and Gold items.
    This will halt normal shop progression if you have chosen Tournament mode.
    """
    display_name = "Bonus Item Mode"
    option_random_dice = 0
    option_shop_progress = 1
    default = 0

class GoldRewardAmount(Range):
    """
    This option only matters when your Bonus Item Mode option is Shop Progress.
    
    The amount of gold you will receive from Gold filler checks.
    """
    display_name = "Gold Reward Amount"
    range_start = 50
    range_end = 200
    default = 100

@dataclass
class YGODDMOptions(PerGameCommonOptions):
    progression: Progression
    tournament_rewards: TournamentRewards
    free_duel_rewards: FreeDuelRewards
    starting_duelists: StartingDuelists
    free_duel_goal: FreeDuelGoal
    dice_stats: DiceStats
    randomize_starting_dice: RandomizeStartingDice
    bonus_item_mode: BonusItemMode
    gold_reward_amount: GoldRewardAmount
      
    def serialize(self) -> typing.Dict[str, int]:
        return {field.name: getattr(self, field.name).value for field in dataclasses.fields(self)}