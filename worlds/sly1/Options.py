from typing import List, Dict, Any
from dataclasses import dataclass
from worlds.AutoWorld import PerGameCommonOptions
from Options import Choice, OptionGroup, Toggle, OptionSet, Range

def create_option_groups() -> List[OptionGroup]:
    option_group_list: List[OptionGroup] = []
    for name, options in sly1_option_groups.items():
        option_group_list.append(OptionGroup(name=name, options=options))

    return option_group_list

class UnlockClockwerk(Choice):
    """
    What you need to do to unlock Cold Heart of Hate to defeat Clockwerk
    """
    display_name = "Unlock Clockwerk"
    option_boss_victories = 1
    option_page_hunt = 2
    default = 1

class FastClockwerk(Toggle):
    """
    If enabled, unlocking Cold Heart of Hate will give you access directly to the Clockwerk boss fight skipping all the previous levels.
    """
    display_name = "Fast Clockwerk"

class RequiredBosses(Range):
    """
    How many members of the Fiendish Five you need to defeat before Cold Heart of Hate is unlocked.
    Only used if boss victories is selected as the Unlock Clockwerk option.
    """
    range_start = 1
    range_end = 4
    default = 4

class MaxPages(Range):
    """
    How many pages are available to collect in the multiworld.
    These pages are NOT the same as the normal pages that give you thief moves.
    Only used if page hunt is selected as the Unlock Clockwerk option.
    Note that this option requires more locations than usual. Cluesanity is recommended.
    """
    range_start = 1
    range_end = 50
    default = 25

class RequiredPages(Range):
    """
    How many pages of the Thievius Raccoonus you need to collect before Cold Heart of Hate is unlocked.
    These pages are NOT the same as the normal pages that give you thief moves.
    Only used if page hunt is selected as the Unlock Clockwerk option.
    """
    range_start = 1
    range_end = 50
    default = 20

class StartingEpisode(Choice):
    """
    Determines which episode you will start in. You will be able to do the initial level for it, but
    will only be able to continue if you receive a key for that episode (or unlock a different episode)
    from a location within it. Avoid Early BK is suggested if you want to avoid early stuck points.
    """
    display_name = "Starting Episode"
    option_tide_of_terror = 1
    option_sunset_snake_eyes = 2
    option_vicious_voodoo = 3
    option_fire_in_the_sky = 4
    option_all = 6
    default = 1

class AvoidEarlyBK(Toggle):
    """
    Determines if you will start with 1 key for your chosen starting episode.
    If all is selected, you are given 1 key for a random episode.
    """
    display_name = "Avoid Early BK"

class IncludeHourglasses(Toggle):
    """
    If enabled, Hourglasses are included in the locations.
    """
    display_name = "Include Hourglasses"

class HourglassesRequireRoll(Toggle):
    """
    Some Hourglasses are tough without the Roll move.
    If enabled, at least one Progressive Roll will logically be required for Hourglasses.
    """
    display_name = "Hourglasses Require Roll"

class ExcludeMinigames(OptionSet):
    """
    Choose which minigames types you want to exclude as locations.
    Crabs: Treasure in the Depths
    Races: At the Dog Track, A Desperate Race
    Turrets: Murray's Big Gamble, The King of the Hill
    Hover Blasters: A Ghastly Voyage, Rapid Fire Assault
    Chicken Killing: Down Home Cooking
    Swamp Skiff: Piranha Lake
    """
    display_name = "Exclude Minigames"
    valid_keys = {
        "Crabs",
        "Races",
        "Turrets",
        "Hover Blasters",
        "Chicken Killing",
        "Swamp Skiff"
    }

class MinigameCaches(Range):
    """
    Determines how many additional "minigame cache" checks that minigame levels send when completed.
    Minigame levels will still have a key location even if this is set to 0.
    This is ignored for any minigame levels excluded above. Allows a range from 0-10.
    """
    display_name = "Minigame Caches"
    range_start = 0
    range_end = 10
    default = 0

class LocationCluesanityBundleSize(Range):
    """
    Determines how many bottles you need to collect for each check.
    Set to 0 to disable. Allows a range between 0 and 5.
    """
    display_name = "Location Cluesanity Bundle Size"
    range_start = 0
    range_end = 5
    default = 0

class ItemCluesanityBundleSize(Range):
    """
    Determines how many bottles you will receive for a given level.
    Set to 0 to disable. Allows a range between 0 and 5.
    """
    display_name = "Item Cluesanity Bundle Size"
    range_start = 0
    range_end = 5
    default = 0

class CutsceneSkip(Toggle):
    """
    Automatically skips dialogue and FMV cutscenes if enabled.
    Dialogue can be skipped with the R2 button whether this option is on or off.
    """
    display_name = "Cutscene Skip"
    default = 1

class TrapChance(Range):
    """
    Determines the chance for a filler item to become a trap.
    Set it to 0 for no traps.
    """
    display_name = "Include Traps"
    range_start = 0
    range_end = 100
    default = 0

class IcePhysicsTrapWeight(Range):
    """
    The weight of ice physics traps in the trap pool.
    Ice physics traps turn on the low friction cheat code for 10 seconds.
    """
    display_name = "Ice Physics Trap Weight"
    range_start = 0
    range_end = 100
    default = 25

class SpeedChangeTrapWeight(Range):
    """
    The weight of speed change traps in the trap pool.
    Speed change traps change the game speed for 10 seconds.
    """
    display_name = "Speed Change Trap Weight"
    range_start = 0
    range_end = 100
    default = 25

class InvisibilityTrapWeight(Range):
    """
    The weight of invisibility traps in the trap pool.
    Invisibility traps turn Sly completely invisible for 10 seconds.
    """
    display_name = "Invisibility Trap Weight"
    range_start = 0
    range_end = 100
    default = 25

class BallTrapWeight(Range):
    """
    The weight of ball traps in the trap pool.
    Ball traps force Sly to stay in the roll form for 10 seconds.
    """
    display_name = "Ball Trap Weight"
    range_start = 0
    range_end = 100
    default = 25

class EnableTricks(OptionSet):
    """
    This option allows you to enable alternative forms of logic to access parts of the game via tricks.
    Intended for use by people who know speedrun tricks already, but if you would like to learn, watch an
    Any% run of the game for reference on how to do the below tricks.

    Tide of Terror supports tot_second_half_early and tot_raleigh_early.
    Sunset Snake Eyes supports sse_second_half_early and sse_muggshot_early.
    Vicious Voodoo only supports vv_second_half early as Mz. Ruby does not have known methods of early access.
    Fire in the Sky supports fits_second_half_early and fits_panda_early.
    Additionally, an 8th trick unseen_foe_invis_skip is supported which puts all Unseen Foe locations into logic
    without requiring any progressive invisibility items.

    Including any of the tricks below will potentially require you to do those tricks to progress, depending
    on the randomization.
    """
    display_name = "Enable Tricks"
    default = []
    valid_keys = ["tot_second_half_early", "tot_raleigh_early", "sse_second_half_early", "sse_muggshot_early",
                  "vv_second_half_early", "fits_second_half_early", "fits_panda_early", "unseen_foe_invis_skip"]

@dataclass
class Sly1Options(PerGameCommonOptions):
    UnlockClockwerk:                UnlockClockwerk
    FastClockwerk:                  FastClockwerk
    RequiredBosses:                 RequiredBosses
    MaxPages:                       MaxPages
    RequiredPages:                  RequiredPages
    StartingEpisode:                StartingEpisode
    IncludeHourglasses:             IncludeHourglasses
    HourglassesRequireRoll:         HourglassesRequireRoll
    AvoidEarlyBK:                   AvoidEarlyBK
    ExcludeMinigames:               ExcludeMinigames
    MinigameCaches:                 MinigameCaches
    LocationCluesanityBundleSize:   LocationCluesanityBundleSize
    ItemCluesanityBundleSize:       ItemCluesanityBundleSize
    EnableTricks:                   EnableTricks
    CutsceneSkip:                   CutsceneSkip
    TrapChance:                     TrapChance
    IcePhysicsTrapWeight:           IcePhysicsTrapWeight
    SpeedChangeTrapWeight:          SpeedChangeTrapWeight
    InvisibilityTrapWeight:         InvisibilityTrapWeight
    BallTrapWeight:                 BallTrapWeight

sly1_option_groups: Dict[str, List[Any]] = {
    "General Options": [UnlockClockwerk, FastClockwerk,
                         RequiredBosses, MaxPages,
                         RequiredPages, StartingEpisode,
                         IncludeHourglasses, HourglassesRequireRoll,
                         EnableTricks, CutsceneSkip],
    "Minigame Options": [ExcludeMinigames, MinigameCaches],
    "Cluesanity Options": [LocationCluesanityBundleSize, ItemCluesanityBundleSize],
    "Trap Options": [TrapChance, IcePhysicsTrapWeight,
                     SpeedChangeTrapWeight, InvisibilityTrapWeight,
                     BallTrapWeight]
}