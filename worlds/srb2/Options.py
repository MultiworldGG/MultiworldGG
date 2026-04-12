import typing
from dataclasses import dataclass
from Options import DefaultOnToggle, Range, Toggle, DeathLink, Choice, PerGameCommonOptions, OptionSet, OptionGroup, OptionCounter


class TimeEmblems(DefaultOnToggle):
    """Enable record attack time emblems (27 Locations)"""
    display_name = "Time Emblems"
class RingEmblems(DefaultOnToggle):
    """Enable record attack Ring emblems (20 Locations)"""
    display_name = "Ring Emblems"
class ScoreEmblems(DefaultOnToggle):
    """Enable record attack Score emblems (7 Locations)"""
    display_name = "Score Emblems"

class NightsMaps(DefaultOnToggle):
    """Enable NiGHTS stages as items/locations (36 Locations)"""
    display_name = "NiGHTS Maps"

class RankEmblems(DefaultOnToggle):
    """Enable NiGHTS A Rank emblems (12 Locations)"""
    display_name = "NiGHTS Rank Emblems"
class NTimeEmblems(DefaultOnToggle):
    """Enable NiGHTS Time emblems (12 Locations)"""
    display_name = "NiGHTS Time Emblems"



class StartingCharacter(Choice):
    """Choose Starting character
    Tails/Knuckles are recommended if you don't know where all the emblems are"""
    option_sonic = 0
    option_tails = 1
    option_knuckles = 2
    option_amy = 3
    option_fang = 4
    option_metal_sonic = 5
    option_all = 6
    default = 0


class RadarStart(Toggle):
    """Start with Emblem Hints + Radar, useful if you don't know where all the emblems are"""
    display_name = "Start with Emblem Radar"

class LogicDifficulty(Choice):
    """Difficulty of logic required to get items
    Normal - Tails/Knuckles required for difficult emblems, no badnik bouncing
    Hard - If it's possible, it's in logic
    Custom - Disables in-zone logic for custom character use"""
    option_normal = 0
    option_hard = 1
    option_custom = 2
    default = 0
    display_name = "Logic Difficulty"

class MPMaps(Toggle):
    """Enable Ringslinger Maps as items/locations"""
    display_name = "Multiplayer Maps"

class OneUpSanity(Toggle):
    """Enable 1UP Monitors as checks (247 Locations)"""
    display_name = "1UP-Sanity"

class SuperRingSanity(Toggle):
    """Enable Ring Monitors as checks
    Normal - 598 Locations
    With Ringslinger Maps - 976 Locations"""
    display_name = "Super Ring-Sanity"

class ActSanity(Toggle):
    """Splits zone unlocks into individual acts
    I.E. Greenflower Zone -> Greenflower Zone (Act 1), Greenflower Zone (Act 2), Greenflower Zone (Act 3)"""

class ObjectLocking(Toggle):
    """Shuffles certain objects like springs, slime, zoom tubes etc
    DOES NOT CURRENTLY WORK WITH MATCH MAPS + RING MONITORS"""

class BlackCoreEmblemCost(Range):
    """PERCENTAGE of emblems needed for black core zone to be unlocked
    Putting 0 will make Black Core Zone an item in the multiworld like the rest of the zones"""
    display_name = "Emblems for Black Core"
    range_start = 0
    range_end = 100
    default = 50

class EmblemNumber(Range):
    """Total Number of emblems
    (There are about 250 locations with all emblems turned on)"""
    display_name = "Total Emblems"
    range_start = 10
    range_end = 250
    default = 100

class TrapPercentage(Range):
    """Percentage of filler items to replace with traps"""
    display_name = "Trap Percentage"
    range_start = 0
    range_end = 100
    default = 30

class TrapWeights(OptionCounter):
    """
    Determines the ratio of each trap
    """
    default = {
        "Replay Tutorial": 4,
        "Self-Propelled Bomb": 6,
        "Sonic Forces": 8,
        "Jumpscare": 8,
        "Slippery Floors": 8,
        "Shrink Monitor": 6,
        "Grow Monitor": 6,
        "Forced Gravity Boots": 10,
        "Ring Loss": 10,
        "Dropped Inputs": 10,
        "Forced Pity Shield": 20,
    }
    display_name = "Trap Weights"

class FillerWeights(OptionCounter):
    """
    Determines the ratio of each filler item
    """
    default = {
        "1UP": 4,
        "10 Rings": 25,
        "20 Rings": 10,
        "50 Rings": 5,
        "1000 Points": 8,
        "& Knuckles": 8,
        "Temporary Invincibility": 12,
        "Temporary Super Sneakers": 12,
        "Double Rings": 6,
    }
    display_name = "Filler Weights"



class CompletionType(Choice):
    """Set goal for Victory Condition
    Bad Ending Requires Beating Black Core Zone Act 3
    Good Ending Requires The 7 Chaos Emeralds"""

    display_name = "Completion Goal"
    option_Bad_Ending = 0
    option_Good_Ending = 1

class RingLink(Choice):
    """Enable Ringlink (share rings/currency with other games)
    Easy - Only lose rings through damage
    Normal - Lose rings on death (crushing, drowning, pits)
    Hard - Lose rings on zone exit, zone entry and retry"""
    option_off = 0
    option_easy = 1
    option_normal = 2
    option_hard = 3
    display_name = "Ring Link"

#class LocalRingReset(DefaultOnToggle):
#    """Reset rings locally on zone exit/entry"""
#    display_name = "Reset Rings Locally"

srb2_options_groups = [
    OptionGroup("Emblem Toggles", [
        TimeEmblems,
        RingEmblems,
        ScoreEmblems,
        NightsMaps,
        RankEmblems,
        NTimeEmblems,
        StartingCharacter,
        OneUpSanity,
        SuperRingSanity,
        MPMaps
    ]),
    OptionGroup("Meta Options", [
        ActSanity,
        ObjectLocking,
        LogicDifficulty,
        RadarStart,
        BlackCoreEmblemCost,
        TrapPercentage,
        TrapWeights,
        FillerWeights,
        EmblemNumber,
        RingLink,

    ]),
]

@dataclass
class SRB2Options(PerGameCommonOptions):

    time_emblems: TimeEmblems
    ring_emblems: RingEmblems
    score_emblems: ScoreEmblems
    nights_maps: NightsMaps
    rank_emblems: RankEmblems
    ntime_emblems: NTimeEmblems
    actsanity: ActSanity
    object_locking: ObjectLocking
    starting_character: StartingCharacter
    difficulty: LogicDifficulty
    match_maps: MPMaps
    oneup_sanity: OneUpSanity
    superring_sanity: SuperRingSanity
    radar_start: RadarStart
    num_emblems: EmblemNumber
    trap_weights: TrapWeights
    filler_weights: FillerWeights
    bcz_emblem_percent:BlackCoreEmblemCost
    trap_percentage:TrapPercentage
    ring_link: RingLink
    death_link: DeathLink
    completion_type: CompletionType
