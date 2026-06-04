import typing
from dataclasses import dataclass
from Options import DefaultOnToggle, Range, Toggle, DeathLink, Choice, PerGameCommonOptions, OptionSet, OptionGroup, OptionCounter, OptionList


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


class CharacterList(OptionList):
    """Choose Included characters
    MODDED CHARACTERS MUST BE DOWNLOADED SEPERATELY
    Removing vanilla character may cause logic issues
    Vanilla characters: 'Sonic', 'Tails', 'Knuckles', 'Amy', 'Fang', 'Metal Sonic'
    Chaotix: 'Espio', 'Mighty', 'Charmy Bee', 'Vector', 'Heavy', 'Bomb'
    Mario Bros: 'Mario', 'Luigi'
    RChars: 'Metal Knuckles', 'Tails Doll'
    Misc characters: 'Yoshi', 'Ray', 'Silver', 'Shadow', 'Modern Sonic', 'Werehog'"""

    display_name = "Character List"
    valid_keys = {"Sonic","Tails","Knuckles","Amy","Fang","Metal Sonic","Mario","Luigi","Yoshi","Ray","Silver","Shadow","Modern Sonic","Werehog","Metal Knuckles","Tails Doll","Espio","Mighty","Charmy Bee","Vector","Heavy","Bomb"}
    default = ["Sonic","Tails","Knuckles","Amy","Fang","Metal Sonic"]

class StartingCharacter(OptionList):
    """Choose Starting characters
    Tails/Knuckles are recommended if you don't know where all the emblems are
    You may also select any valid custom character"""
    display_name = "Starting Character"
    valid_keys = {"Sonic","Tails","Knuckles","Amy","Fang","Metal Sonic","Mario","Luigi","Yoshi","Ray","Silver","Shadow","Modern Sonic","Werehog","Metal Knuckles","Tails Doll","Espio","Mighty","Charmy Bee","Vector","Heavy","Bomb"}
    default = ["Sonic"]

class RandomStartChar(Toggle):
    """Randomly pick a character from the Starting Character list as your starting character instead of all of them"""
    display_name = "Randomize Starting Character"
#randomize starting character
#randomly pick from startingcharacter as your starting character


class RadarStart(Toggle):
    """Start with Emblem Hints + Radar, useful if you don't know where all the emblems are"""
    display_name = "Start with Emblem Radar"

class LogicDifficulty(Choice):
    """Difficulty of logic required to get items
    Normal - Tails/Knuckles required for difficult emblems, no badnik bouncing
    Hard - If it's possible, it's in logic"""
    option_normal = 0
    option_hard = 1
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
    display_name = "Actsanity"

class ObjectLocking(Toggle):
    """Shuffles objects such as springs, slime, zoom tubes etc"""
    display_name = "Object Locking"

class BlackCoreEmblemCost(Range):
    """PERCENTAGE of emblems needed for your goal stage to be unlocked
    When playing with the challenge level goal:
        1/3 of this percentage unlocks Haunted Heights, 2/3 unlocks Aerial Garden and 3/3 unlocks Azure Temple
    Putting 0 will make your goal stages items in the multiworld like the rest of the zones
    """
    display_name = "Emblems for Goal"
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
    Bad Ending - Beat Black Core Zone Act 3
    Good Ending - Beat Black Core Act 3 with all 7 Chaos Emeralds
    Challenge Levels - Beat Haunted Heights, Aerial Garden and Azure Temple
    All Bosses - Beat every Act 3 and every act of Black Core Zone"""


    display_name = "Completion Goal"
    option_Bad_Ending = 0
    option_Good_Ending = 1
    option_Challenge_Levels = 2
    option_All_Bosses = 3

class RingResetZoneExit(DefaultOnToggle):
    """Rings reset locally on zone entry/exit (takes priority over hard ringlink)"""
    display_name = "Local Ring Reset"


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



srb2_options_groups = [
    OptionGroup("Emblem Toggles", [
        TimeEmblems,
        RingEmblems,
        ScoreEmblems,
        NightsMaps,
        RankEmblems,
        NTimeEmblems,
        OneUpSanity,
        SuperRingSanity,
        MPMaps
    ]),
    OptionGroup("Meta Options", [
        ActSanity,
        ObjectLocking,
        LogicDifficulty,
        RadarStart,
        CompletionType,
        BlackCoreEmblemCost,
        CharacterList,
        StartingCharacter,
        RandomStartChar,
        TrapPercentage,
        TrapWeights,
        FillerWeights,
        EmblemNumber,
        RingResetZoneExit,
        RingLink


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
    character_list: CharacterList
    random_start_char: RandomStartChar
    difficulty: LogicDifficulty
    match_maps: MPMaps
    oneup_sanity: OneUpSanity
    superring_sanity: SuperRingSanity
    radar_start: RadarStart
    num_emblems: EmblemNumber
    trap_weights: TrapWeights
    filler_weights: FillerWeights
    completion_type: CompletionType
    bcz_emblem_percent:BlackCoreEmblemCost
    trap_percentage:TrapPercentage
    ring_link: RingLink
    ring_reset_zone_exit: RingResetZoneExit
    death_link: DeathLink

