from dataclasses import dataclass
from Options import (
    FreeText,
    NumericOption,
    Toggle,
    DefaultOnToggle,
    Choice,
    TextChoice,
    Range,
    NamedRange,
    OptionList,
    PerGameCommonOptions,
    OptionSet,
    OptionCounter,
    StartInventoryPool, OptionGroup, Visibility,
    DeathLinkMixin,
)

class Goal(Choice):
    """
    sleigh_ride: Sleigh parts are placed in their local areas that you must
    physically collect them to goal.
    sleigh_ride_with_parts:  Sleigh parts are randomized in the pool that you
    must find all the required parts and the Sleigh Room Key to goal.
    missions_completed: You must complete a certain number of missions to
    goal.
    squashing_all_gifts: You must squash every gift in the entire game to goal.
    supadows_completed: You are required to win every supadow minigame to
    goal and obtain access to their minigames to do so.
    slaughter: You must kill every Who, every animal, and every robot to goal.
    """

    display_name = "Goal"
    option_sleigh_ride = 0
    option_sleigh_ride_with_parts = 1
    option_missions_completed = 2
    option_squashing_all_gifts = 3
    option_supadows_completed = 4
    option_slaughter = 5
    default = 0
    visibility = Visibility.none


class MissionsCompleted(Range):
    """
    If your goal is missions_completed, set how many missions you want to
    complete to goal. If your goal is missions_completed_with_gifts, this option
    will be ignored.
    """

    display_name = "Mission Goal Count"
    range_start = 3
    range_end = 22
    default = 12
    visibility = Visibility.none

# We will make a list of every mission in the game, excluding squashing gifts.
# Randomly pick whatever range is chosen via missions_completed to include
# in the location pool. If they include squashing all gifts, include those in the
# list.
class MissionCompletedIncludeGiftSquash(Toggle):
    """
    If your goal is missions_completed, include the squashing all gift missions.
    Otherwise, if your goal is not missions_completed, this will do nothing.
    """
    display_name = "Include Gift Squashing in Missions Completed Goal"
    visibility = Visibility.none


class StartingArea(Choice):
    """
    Here, you can select which area you'll start the game with.
    Whichever one you pick is the region you'll have access to at the start of the Multiworld.
    If "progressive_vacuums" is enabled, this is not considered and will always start in Whoville.
    """

    option_whoville = 0
    option_who_forest = 1
    option_who_dump = 2
    option_who_lake = 3
    default = 0
    display_name = "Starting Area"


class ProgressiveVacuums(Toggle):  # DefaultOnToggle
    """
    Determines whether you get access to main areas progressively.
    If enabled, you will receive Whoville, Who Forest, Who Dump, and Who Lake in that order.
    """

    display_name = "Progressive Vacuum Tubes"


class Missionsanity(Choice):
    """
    How mission checks are randomized in the pool.
    - none: Does not add mission checks
    - completion: Only completing the mission gives you a check
    - individual: Individual tasks for one mission, such as individual snowmen
    squashed, are checks.
    - both: Both individual tasks and mission completion are randomized.
    """

    display_name = "Mission Locations"
    option_none = 0
    option_completion = 1
    option_individual = 2
    option_both = 3
    default = 1

class AdvancedLogic(Toggle):

    """
    Enables logic to allow skips, damage boosts, glitches, game restarts,
    excessive egg usage, and various other unintentional ways that beginners
    wouldn't grasp on their first playthrough if this is enabled to be considered
    logical.
    """

    display_name = "Advanced Logic"
    visibility = Visibility.none

class ExcludeEnvironments(OptionSet):
    """
    Allows entire environments to be entirely removed to ensure you are not
    logically required to enter the environment along with any and all checks
    that are in that environment too.

    Valid keys: "Post Office", "Clock Tower", "City Hall", "Ski Resort",
    "Civic Center", "Minefield", "Power Plant", "Generator Building",
    "Scout's Hut", "North Shore", "Mayor's Villa", "Submarine World"
    """

    display_name = "Exclude Environments"
    valid_keys = {
        "Post Office",
        "Clock Tower",
        "City Hall",
        "Ski Resort",
        "Civic Center",
        "Minefield",
        "Power Plant",
        "Generator Building",
        "Scout's Hut",
        "North Shore",
        "Mayor's Villa",
        "Submarine World",
    }


class ProgressiveGadgets(Toggle):  # DefaultOnToggle
    """
    Determines whether you get access to a gadget as the individual blueprint count.
    """

    display_name = "Progressive Gadgets"
    visibility = Visibility.none


class Supadow(Toggle):
    """
    Enables completing minigames through the Supadows in Mount Crumpit as checks.
    """

    display_name = "Supadow Minigames"
    visibility = Visibility.none


class Gifts(Toggle):
    """
    Determines if individual gifts are checks
    NOTE: This currently only disables the missions relating to squashing all
    gifts for an entire region.
    """

    display_name = "Giftsanity"


class Killsanity(OptionSet):
    """
    Determines whether you consider killing/destroying certain enemies
    throughout the games are checks.

    "Whos" are considereed as people such as guards, children, and other
    humanoid related figures.
    "Animals" are considered as non-human species such as Summer beasts,
    porcupines, moose, and mosquitoes.
    "Robots" are considered mechanical beings that electrocute the player,
    specifically the robots you find in Who Dump.
    """

    display_name = "Killsanity"
    valid_keys = {"Whos", "Animals", "Robots"}
    visibility = Visibility.none


class Gadgetrando(DefaultOnToggle):
    """
    Determines whether the Grinch's gadgets will be randomized or not.
    """

    display_name = "Randomize Gadgets"


class Gadgetrandolist(OptionSet):
    """
    If "gadget_rando" is enabled, gadgets that you add to the dictionary will
    be randomized.
    """

    display_name = "Gadgets Randomized"
    default = [
        "Binoculars",
        "Rotten Egg Launcher",
        "Rocket Spring",
        "Slime Shooter",
        "Octopus Climbing Device",
        "Marine Mobile",
        "Grinch Copter",
    ]


class ExcludeGC(Toggle):
    """
    Tired of getting Grinch Copter? This option ensures Grinch Copter is
    entirely taken out from the multiworld.
    Note that locations that hard require Grinch Copter will also be removed.
    """

    display_name = "Remove Grinch Copter"


class Moverando(Toggle):
    """
    Determines whether the Grinch's moves will be randomized or not.
    NOTE: Tutorial section would be logical linearly and vacuum tubes would still
    be logical. To access them, you can use certain controller combinations to
    warp to their respective areas in Mount Crumpit at any time.
    To warp to the computer room, press and hold start, L1, and R1 at the same time.
    To warp to the top, press and hold start, L2, and R2 at the same time.
    """

    display_name = "Randomize Moves"


class Moverandolist(OptionSet):
    """
    If "move_rando" is enabled, the Grinch's moves that you add to the dictionary will be randomized.
    """

    display_name = "Moves Randomized"
    default = [
        "Pancake",
        "Bad Breath",
        "Seize",
        "Max",
        "Sneak",
    ]


class UnlimitedEggs(Toggle):
    """
    Determine if you run out of rotten eggs when you utilize your gadgets.
    NOTE: Attempting to enable this with ringlink will force generation to stop
    until either option is disabled.
    """

    display_name = "Unlimited Rotten Eggs"


class RingLinkOption(Toggle):
    """
    Whenever this is toggled, your ammo is linked with other ringlink-compatible
    games that also have this enabled.
    NOTE: Attempting to enable this with unlimited_eggs will force generation
    to stop until either option is enabled.
    """

    display_name = "Ring Link"


class TrapLinkOption(Toggle):
    """
    If a trap is sent from Grinch, traps that are compatible with other games
    are triggered as well.
    """

    display_name = "Trap Link"
    visibility = Visibility.none


class FillerWeight(OptionCounter):
    """
    Determines which filler is added to the pool.
    """

    display_name = "Filler Weights"
    # min = 0
    # max = 100
    default = {
        "5 Rotten Eggs": 50,
        "10 Rotten Eggs": 25,
        "20 Rotten Eggs": 25,
    }


class TrapPercentage(Range):
    """
    Determines how much filler is replaced with traps.
    """

    display_name = "Trap Percentage"
    range_start = 0
    range_end = 100
    default = 0


class TrapWeight(OptionCounter):
    """
    Determines which traps are replaced with filler in the pool.
    """

    display_name = "Trap Weights"
    # min = 0
    # max = 100
    default = {
        "Dump it to Crumpit": 33,
        "Who sent me back?": 33,
        "Depletion Trap": 34,
        # "Bonk Trap": 25,
        # "Push Trap": 25,
        # "Damage Trap": 25,
        # "Electrocution Trap": 25,
        # "Ice Trap": 25,
        # "Bee Trap": 25,
        # "Banana Trap": 25,
    }

class MiscLocations(Toggle):
    """
    Adds locations that aren't specifically categorized and are either random
    events or just unnecessarily added locations that don't mean anything.
    """

    display_name =  "Miscellaneous Locations"


class DamageRate(Range):
    """
    How much damage can the Grinch tolerate before death
    0 = Invincible
    1 = Base game damage rate
    78 = Instant death without any Hearts of Stone
    88 = Instant death with one Heart of Stone
    99 = Instant death with two Hearts of Stone
    110 = Instant death with three Hearts of Stone
    120 = Instant death
    """

    display_name = "Damage Rate"
    range_start = 0
    range_end = 120
    default = 1
    visibility = Visibility.none


class MusicRando(Toggle):
    """
    Randomizes all music in the game
    """
    display_name = "Music Rando"


class ReducedCutscenes(Toggle):
    """
    Certain cutscenes no longer trigger if enabled for a faster experience
    """
    display_name = "Reduced Cutscenes"


class RandomizeMissionItems(DefaultOnToggle):
    """
    Allows mission specific items to be randomized in the itempool.
    NOTE: Disabling this adds the locations and will still keep the items. But will be
    forced to their vanilla locations. Enabling this removes these locations.
    """
    display_name = "Randomize Mission Specific Items"
    visibility = Visibility.none

class RandomizeSleighParts(DefaultOnToggle):
    """
    Allows the sleigh parts to be randomized in the itempool.
    NOTE: Disabling this adds the locations and will still keep the items. But will be
    forced to their vanilla locations. Enabling this removes these locations.
    """
    display_name = "Randomize Sleigh Parts"
    visibility = Visibility.none


@dataclass
class GrinchOptions(DeathLinkMixin, PerGameCommonOptions):
    progressive_vacuums: ProgressiveVacuums
    starting_area: StartingArea
    missionsanity: Missionsanity
    exclude_environments: ExcludeEnvironments
    giftsanity: Gifts
    supadow_minigames: Supadow
    killsanity: Killsanity
    progressive_gadgets: ProgressiveGadgets
    gadget_rando: Gadgetrando
    gadgets_to_randomize: Gadgetrandolist
    exclude_gc: ExcludeGC
    move_rando: Moverando
    moves_to_randomize: Moverandolist
    unlimited_eggs: UnlimitedEggs
    filler_weight: FillerWeight
    trap_percentage: TrapPercentage
    trap_weight: TrapWeight
    ring_link: RingLinkOption
    trap_link: TrapLinkOption
    advanced_logic: AdvancedLogic
    start_inventory_from_pool: StartInventoryPool
    misc_checks: MiscLocations
    damage_rate: DamageRate
    goal: Goal
    missions_completed: MissionsCompleted
    include_gift_squash: MissionCompletedIncludeGiftSquash
    music_rando: MusicRando
    reduced_cutscenes: ReducedCutscenes
    randomize_mission_items: RandomizeMissionItems
    randomize_sleigh_parts: RandomizeSleighParts


grinch_option_groups: list[OptionGroup] = [
    # OptionGroup("Goal", [
    #     Goal,
    #     MissionsCompleted,
    #     MissionCompletedIncludeGiftSquash,
    # ]),
    OptionGroup("Item Pool", [
        ProgressiveVacuums,
        StartingArea,
        ProgressiveGadgets,
        Gadgetrando,
        Gadgetrandolist,
        ExcludeGC,
        Moverando,
        Moverandolist,
        RandomizeMissionItems,
        RandomizeSleighParts,
    ]),
    OptionGroup("Location Settings", [
        Missionsanity,
        ExcludeEnvironments,
        Gifts,
        Supadow,
        Killsanity,
        MiscLocations,
    ]),
    # OptionGroup("Logic Settings", [
    #     AdvancedLogic,
    # ]),
    OptionGroup("In-Game Tweaks", [
        UnlimitedEggs,
        DamageRate,
        MusicRando,
        ReducedCutscenes,
    ]),
    OptionGroup("Filler/Trap Settings", [
        FillerWeight,
        TrapPercentage,
        TrapWeight,
        RingLinkOption,
        TrapLinkOption,
    ]),
]