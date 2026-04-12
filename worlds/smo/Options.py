from dataclasses import dataclass

from Options import Toggle, Choice, FreeText, PerGameCommonOptions, DeathLink


class Goal(Choice):
    """Sets the completion goal. This is the kingdom you must get the last story multi moon in to win the game.
    Valid options: Metro (A Traditional Festival), Luncheon (Cookatiel Showdown), Moon (Beat the game), Dark (Arrival at Rabbit Ridge), Darker (A Long Journey's End)"""
    display_name = "Goal"
    option_sand = 2
    option_lake = 4
    option_metro = 7
    option_luncheon = 10
    option_moon = 13
    option_dark = 15
    option_darker = 16
    default = 13  # default to moon

class StorySanity(Choice):
    """Adds story progression moons to the pool."""
    display_name = "Randomize Story Moons"
    option_single_moons = 1
    option_multi_moons = 2
    option_all = 3
    option_off = 0
    default = 0 # default to off

class ShopSanity(Choice):
    """Adds various shop items to the pool.
    shuffle: shuffles outfits amongst themselves keeping them in your game."""
    display_name = "Randomize Shops"
    option_shuffle = 1
    option_outfits  = 2
    option_non_outfits = 3
    option_all = 4
    option_off = 0
    default = 0  # default to off

class RandomizeMoonColors(Choice):
    """Changes the color of moons.
    kingdom : shuffles color dependent on kingdom (all moons in one kingdom will be the same color similar to the original implementation)
    item : color is dependent on the item at the location (SMO items only)
    classification : color is dependent on the item classification of the item at the location
    random : randomizes the colors instead of using the default set.
    chaos : colors are completely random for each moon individually."""
    display_name = "Randomize Moon Colors"
    option_off = 0
    option_kingdom_random = 1
    option_item = 2
    option_classification = 3
    option_item_random = 4
    option_classification_random = 5
    option_chaos = 6
    default = 0
    #visibility = 0b1101

class RandomizeMoonCount(Choice):
    """Randomizes each kingdom's moon count.
    same total: Moon counts still add up to 124 like in the base game.
    lock ruined: Moon counts still add up to 124, but ruined kingdom is always a 3 moon requirement.
    moderate: Up to +25% and down to -20% of normal per kingdom counts.
    extreme: Up to 200% of normal count.
    """
    display_name = "Randomize Moon Requirements"
    #visibility = 0b1101
    option_same_total = 1
    option_same_total_lock_ruined = 2
    option_moderate = 3
    option_extreme = 4
    option_off = 0
    default = 0

class CaptureSanity(Toggle):
    """Randomizes Captures.
    Warning this is an experimental feature!
    NOT ALL Captures have logic, use at YOU OWN RISK!
    Logic for post game is still missing.
    """
    display_name = "Randomize Captures"
    #visibility = 0b1101

class ExtraMoons(Choice):
    """
    Sets the multiplier for the number of extra moons available in the pool for each kingdom.
    Default: some = 1.2x moons
    """
    display_name = "Extra Moons"
    option_none = 1.0
    option_some = 1.2
    option_more = 1.5
    option_many = 1.75
    option_double = 2.0

    default = 1.2  # default to some

class TrickJumpLogic(Choice):
    """
        Difficulty of trick jumps considered as in logic.
    """
    option_off = 0
    option_easy = 1
    option_intermediate = 2
    option_hard = 3

    default = 0  # default to off

class MiscTrickLogic(Choice):
    """
        Difficulty of clips and glitches considered as in logic.
    """
    option_off = 0
    option_easy = 1
    option_intermediate = 2
    option_hard = 3

    default = 0  # default to off

class SMODeathLink(DeathLink):
    __doc__ = DeathLink.__doc__ + "\n    In Super Mario Odyssey, Mario dying in any way sends a death and receiving a death causes Mario to die where he stands."

@dataclass
class SMOOptions(PerGameCommonOptions):
    goal: Goal
    story : StorySanity
    extra_moons : ExtraMoons
    shop_sanity : ShopSanity
    # replace: ReplaceUnneededMoons
    colors : RandomizeMoonColors
    counts : RandomizeMoonCount
    capture_sanity : CaptureSanity
    death_link : SMODeathLink

