import typing
from dataclasses import dataclass
from Options import (
    DefaultOnToggle,
    Toggle,
    Choice,
    PerGameCommonOptions,
    StartInventoryPool,
    NamedRange,
    Range,
    DeathLink,
    OptionSet,
)


class Goal(Choice):
    """Change the desired goal to complete the game
    Dialga - Get X relic fragment shards to unlock hidden land. Find Temporal Tower location
            then go through hidden land via Lapras on the beach to beat dialga
    Darkrai - Beat Dialga (all the same requirements), then get X instruments to unlock Dark Crater"""

    display_name = "Goal"
    option_dialga = 0
    option_darkrai = 1
    default = 0


class FragmentShards(NamedRange):
    """How many Relic Fragment Shards should be required in the game (Macguffins)
    that you must get to unlock Hidden Land"""

    range_start = 4
    range_end = 15
    special_range_names = {"easy": 4, "normal": 6, "hard": 8, "extreme": 10}
    default = 6


class ExtraShards(NamedRange):
    """How many total Fragment Shards should be in the game?
    If the total shards is less than required shards, the total shard amount is equal to the required shard amount"""

    range_start = 0
    range_end = 20
    special_range_names = {"easy": 16, "normal": 12, "hard": 8, "extreme": 0}
    default = 12


class RequiredInstruments(NamedRange):
    """How many Instruments should be required in the game (Macguffins)
    that you must get to unlock Dark Crater if victory condition is Darkrai
    Instruments are not added to the item pool if the goal is Dialga"""

    range_start = 4
    range_end = 15
    special_range_names = {"easy": 4, "normal": 6, "hard": 8, "extreme": 10}
    default = 6


class ExtraInstruments(NamedRange):
    """How many total Instruments should be in the game?
    If the total instruments is less than required instruments,
     the total instrument amount is equal to the required instrument amount"""

    range_start = 0
    range_end = 20
    special_range_names = {"easy": 16, "normal": 12, "hard": 8, "extreme": 0}
    default = 12


class EarlyMissionChecks(NamedRange):
    """How many Missions per dungeon pre dialga should be checks?
    0 equals missions are not checks"""

    range_start = 0
    range_end = 31
    special_range_names = {"off": 0, "some": 4, "lots": 10, "insanity": 31}
    default = 4


class LateMissionChecks(NamedRange):
    """How many Missions per dungeon post-dialga (including Hidden Land
    and Temporal Tower) should be checks? 0 equals missions are not checks"""

    range_start = 0
    range_end = 31
    special_range_names = {"off": 0, "some": 4, "lots": 10, "insanity": 31}
    default = 4


class EarlyOutlawChecks(NamedRange):
    """How many outlaws per dungeon pre dialga should be checks?
    0 equals outlaws are not checks"""

    range_start = 0
    range_end = 31
    special_range_names = {"off": 0, "some": 2, "lots": 10, "insanity": 31}
    default = 2


class LateOutlawChecks(NamedRange):
    """How many Missions per dungeon post-dialga (including Hidden Land
    and Temporal Tower) should be checks? 0 equals outlaws are not checks"""

    range_start = 0
    range_end = 31
    special_range_names = {"off": 0, "some": 2, "lots": 10, "insanity": 31}
    default = 2


class SpindaDrinkEvents(NamedRange):
    """How many drink events should be checks?"""

    default_name = "Spinda Drink Events"
    range_start = 0
    range_end = 20
    special_range_names = {"few": 5, "some": 10, "lots": 15, "all": 20}
    default = 5


class SpindaBasicDrinks(NamedRange):
    """How many Spinda Drinks should be checks?"""

    display_name = "Spinda Drinks"
    range_start = 0
    range_end = 20
    special_range_names = {"few": 5, "some": 10, "lots": 15, "all": 20}
    default = 5


class StartWithBag(DefaultOnToggle):
    """Start with bag? If False all bag upgrades will be randomized in the game.
    If true, you will get one bag upgrade (16 slots) and the rest will be randomized"""

    display_name = "Start with Bag?"


class Recruitment(DefaultOnToggle):
    """Start with recruitment enabled?
    If false, recruitment will be an item available in game"""

    display_name = "Recruitment Enable"


class RecruitmentEvolution(DefaultOnToggle):
    """Start with Recruitment Evolution Enabled?
    If false, evolution will be an item available in game"""

    display_name = "Recruitment Evolution Enable"


class HeroEvolution(DefaultOnToggle):
    """Start with Hero/Partner Evolution Enabled?
    If false, hero evolution will be an item available in game.
    Note: hero evolution does nothing until recruitment
    evolution has been unlocked"""

    display_name = "Partner/Hero Evolution Enable"


class FullTeamFormationControl(DefaultOnToggle):
    """Start with full team formation control?
    If false, full team formation control will be an item
    available in game"""

    display_name = "Formation Control Enable"


class LevelScaling(Choice):
    """Allow for dungeons to scale to the highest level of your party members?
    This will not scale bosses at the end of dungeons, also will not scale Outlaws
    Adjust enemies levels to match the highest party level so you won't have to grind as much.
    Off: Enemy levels are vanilla.
    Easy: Enemies will be bumped down to the highest party level if they're above it.
    Difficult: Enemies will be bumped either down or up to match the party level regardless of their vanilla level
    Regardless of your choice, bosses at the end of dungeons will NOT scale."""

    display_name = "Level Scaling"
    option_off = 0
    option_easy = 1
    option_difficult = 2
    default = 1


class GuestScaling(DefaultOnToggle):
    """Makes the dungeon guests (Bidoof in Cragy Coast, Grovyle in Hidden Land, etc.) scale to your party level
    Does nothing if Level scaling is off"""

    display_name = "Guest Scaling"


class StarterOption(Choice):
    """How would you like your starter and partner to be chosen?
    Vanilla: You do the quiz and are stuck with what the quiz gives you. Choose your partner as normal
    Random: Both your MC and partner will be completely random. This means they can be the same type
            WARNING: game is not balanced for same type team, use at your own risk (until we fix typesanity)
    Override: Do the quiz, but you can override the hero it gives you. Choose your partner as normal
    Choose: Skip the quiz and go straight to choosing your starter and partner
    For both Choose and Override you will be able to pick partner exclusive pokemon for your starter as well as gender
    exclusive pokemon regardless of gender"""

    display_name = "Starter Choice Option"
    option_vanilla = 0
    option_random_starter = 1
    option_override = 2
    option_choose = 3
    default = 2


class TypeSanity(Toggle):
    """Allow for your partner to share a type with your main character
    WARNING: The game is not balanced around this, and we have not done anything to change that.
    Use at your own risk
    """

    display_name = "Type Sanity"


class SpecialEpisodeSanity(Toggle):
    """Start the game with one of the special episodes and NOT the main game.
    Unlock the main game through an item
    Overridden by Excluding Special Episodes"""

    display_name = "Special Episode Sanity"


class ExcludeSpecialEpisodes(Toggle):
    """No special episode items will be added to the game
    Overrides Special Episode Sanity"""

    display_name = "Exclude Special Episodes"


class IqScaling(Range):
    """Do you want to scale IQ to gain IQ faster? What rate? (1x, 2x, 3x, etc.)
    WARNING: 0x WILL NOT GIVE YOU ANY IQ. USE AT YOUR OWN RISK
    """

    display_name = "IQ Scaling"
    range_start = 0
    range_end = 15
    default = 2


class XpScaling(Range):
    """Do you want to scale XP to gain XP faster? What rate? (1x, 2x, 3x, etc.)
    WARNING: 0x WILL NOT GIVE YOU ANY XP. USE AT YOUR OWN RISK
    """

    display_name = "XP Scaling"
    range_start = 0
    range_end = 15
    default = 2


class SkyPeakType(Choice):
    """How do you want sky peak to work?
    1: Progressive (unlock dungeons sequentially when you pick up a sky peak item)
    2. All Random (unlock sky peak dungeons completely at random based on which sky peak item you pick up)
    3: All unlocked from one item (there will be one sky peak item that unlocks all sky peak checks)"""

    display_name = "Sky Peak Type"
    option_progressive = 1
    option_all_random = 2
    option_unlock_all = 3
    default = 1


class DojoDungeons(NamedRange):
    """How many dojo dungeons should be accessible at start?"""

    display_name = "Dojo Dungeons Randomized"
    range_start = 0
    range_end = 10
    special_range_names = {
        "all_open": 10,
        "all_random": 0,
        "start_with_three": 3,
        "start_with_one": 1,
    }
    default = 3


class LegendariesInPool(Range):
    """How many Legendary Pokemon should be in the item pool for you to recruit?
    The Legendary will only come post-dialga if you get it early
    Legendaries are disabled if you are going for a dialga goal
    """

    display_name = "Legendaries in Item Pool"
    range_start = 0
    range_end = 21
    default = 3


class AllowedLegendaries(OptionSet):
    """Set which Legendaries will be available for the item pool as recruits.
    NOTE: legendaries normally found in dungeons are not yet randomized. This only includes legendary recruits at the ends of dungeons
    """

    display_name = "Allowed Legendary Recruits"
    valid_keys = [
        "Regirock",
        "Regice",
        "Registeel",
        "Groudon",
        "Uxie",
        "Mesprit",
        "Azelf",
        "Dialga",
        "Palkia",
        "Regigigas",
        "Giratina",
        "Celebi",
        "Articuno",
        "Heatran",
        "Primal Dialga",
        "Mew",
        "Phione",
        "Cresselia",
        "Rayquaza",
        "Kyogre",
        "Shaymin",
    ]
    default = valid_keys.copy()


class DeathlinkType(Toggle):
    """What type of deathlink do you want?
    Currently False is death even if you have revival seeds
    True will die and recover from revival seeds"""

    display_name = "Deathlink Type"


class AllowTraps(Choice):
    """Would you like to allow traps in the filler items of the game?
    0: No traps allowed
    1: regular traps allowed, nothing too crazy
    2: mean traps allowed (possibility of getting two traps at the same time *unown sentry duty*)
    MEAN TRAPS NOT CURRENTLY IMPLEMENTED CURRENTLY 1 AND 2 DO THE SAME THING WHICH IS JUST ENABLE TRAPS"""

    display_name = "Allow Traps"
    option_disabled = 0
    option_regular = 1
    option_mean = 2


class InvisibleTraps(Toggle):
    """Make all traps invisible so when they come in from the client you don't know what happens until you get the trap
    activated
    NOT YET IMPLEMENTED"""

    display_name = "Invisible Traps"


class TrapPercentage(Range):
    """What percentage of filler items should be traps? Range from 0 to 100 (affected by allowed traps)"""

    display_name = "Trap Percentage"
    range_start = 0
    range_end = 100
    default = 20


class CursedAegisCave(Toggle):
    """Do you want Aegis cave to logically require you to beat a regi you don't have a seal for?"""

    display_name = "Cursed Aegis Cave"


class LongLocationsInclusion(Toggle):
    """Include Rule dungeons, clearing all dojos, final dojo, ludicolo dance,
    and duskull bank checks over 20k in logic"""

    display_name = "Long Locations"


class EarlyMissionFloors(DefaultOnToggle):
    """Allow missions to start on floor 2 of dungeons instead on (floors/2)"""

    display_name = "Mission on Early Floors"


class MoveShortcutMenu(DefaultOnToggle):
    """Enable the Move Shortcut Menu by holding (default L button)
    Disabling this current is not implemented ROMSide"""

    display_name = "Move Shortcut Menu"


class MaxRequiredRank(Choice):
    """What is the maximum required rank you want to be logically necessary
    If your goal is dialga and your max rank is above master rank, your max will be set to master rank"""

    display_name = "Max Required Rank"
    option_disabled = 0
    option_bronze = 1
    option_silver = 2
    option_gold = 3
    option_diamond = 4
    option_super = 5
    option_ultra = 6
    option_hyper = 7
    option_master = 8
    option_master_1star = 9
    option_master_2star = 10
    option_master_3star = 11
    option_guildmaster = 12


@dataclass
class EOSOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    goal: Goal
    required_fragments: FragmentShards
    total_shards: ExtraShards
    req_instruments: RequiredInstruments
    total_instruments: ExtraInstruments
    recruit: Recruitment
    recruit_evo: RecruitmentEvolution
    team_form: FullTeamFormationControl
    hero_evolution: HeroEvolution
    bag_on_start: StartWithBag
    dojo_dungeons: DojoDungeons
    early_mission_checks: EarlyMissionChecks
    late_mission_checks: LateMissionChecks
    early_outlaw_checks: EarlyOutlawChecks
    late_outlaw_checks: LateOutlawChecks
    type_sanity: TypeSanity
    starter_option: StarterOption
    iq_scaling: IqScaling
    xp_scaling: XpScaling
    level_scale: LevelScaling
    guest_scaling: GuestScaling
    deathlink: DeathLink
    deathlink_type: DeathlinkType
    legendaries: LegendariesInPool
    allowed_legendaries: AllowedLegendaries
    special_episode_sanity: SpecialEpisodeSanity
    exclude_special: ExcludeSpecialEpisodes
    sky_peak_type: SkyPeakType
    allow_traps: AllowTraps
    invisible_traps: InvisibleTraps
    trap_percent: TrapPercentage
    long_location: LongLocationsInclusion
    cursed_aegis_cave: CursedAegisCave
    early_mission_floors: EarlyMissionFloors
    move_shortcuts: MoveShortcutMenu
    spinda_drinks: SpindaBasicDrinks
    drink_events: SpindaDrinkEvents
    max_rank: MaxRequiredRank
