from dataclasses import dataclass
from Options import Choice, DefaultOnToggle, NamedRange, OptionCounter, OptionGroup, PerGameCommonOptions, Range, StartInventoryPool, Toggle
from schema import Optional, Schema

# Goal
class Goal(Choice):
    """Victory condition for the game.
    All Cup Tour: Collect set amount of gold trophies to unlock All Cup Tour. Get gold in All Cup Tour to win.
    Trophies: Collect set amount of gold trophies to win."""
    display_name = "Goal"
    option_all_cup_tour = 0
    option_trophies = 1

class TrophyRequirementPercent(Range):
    """How many gold trophies are needed for goal completion.
    Percentage of the whole amount of trophies in pool.
    Default is 65 %, which will be 10 trophies out of 16 with other settings left to defaults."""
    display_name = "Trophy Requirement Percent"
    range_start = 0
    range_end = 100
    default = 65

class GrandPrixTrophies(DefaultOnToggle):
    """Does getting gold in cups earn you trophies. Adds 16 trophies."""
    display_name = "Grand Prix Trophies"

class ShuffleExtraTrophies(Range):
    """How many trophies are added in the pool in addition to predetermined trophy locations.
    These trophies can appear in other players' worlds."""
    display_name = "Shuffle Extra Trophies"
    range_start = 0
    range_end = 50
    default = 0

class AllCupTourMinCC(Choice):
    """At what CC you need to play All Cup Tour to win."""
    display_name = "All Cup Tour Min CC"
    option_50cc = 0
    option_100cc = 1
    option_150cc = 2
    option_mirror = 3
    default = 1

class AllCupTourMinRank(Choice):
    """How well you need to do in All Cup Tour to win."""
    display_name = "All Cup Tour Min Rank"
    option_gold = 0
    option_silver = 1
    option_bronze = 2
    option_perfect = 3
    default = 0

# Content
class LogicDifficulty(NamedRange):
    """Balances the difficulty modeling, how many upgrades you are presumed to have to win races.
    Use normal (0) if you can comfortably win 100cc races.
    Unrestricted places locations in logic as soon as they are technically possible."""
    display_name = "Logic Difficulty"  
    range_start = -50
    range_end = 120
    default = 0
    special_range_names = {
        "baby": -50,
        "easy": -25,
        "normal": 0,
        "hard": 50,
        "unrestricted": 120,
    }

class TimeTrials(Choice):
    """Are time trials in logic? If enabled, item pool has course unlocks for time trials.
    Basic adds locations for beating certain times.
    Include Staff Ghosts enables staff ghosts into logic. For experts only!"""
    display_name = "Time Trials"
    option_disable = 0
    option_basic = 1
    option_include_staff_ghosts = 2
    default = 1

class ItemBoxesAsLocations(Choice):
    """Makes some item boxes count as checks.
    Interesting locations adds 1-3 checks per course.
    Box Groups grants you checks by touching any box in a row/group.
    Boxsanity adds checks to every box individually."""
    display_name = "Item Boxes as Locations"
    option_disabled = 0
    option_interesting_locations = 1
    option_box_groups = 2
    option_boxsanity = 3
    default = 1

class AddCustomItemBoxes(DefaultOnToggle):
    """Moves some item boxes to interesting places.
    These boxes might need going off route and hard to reach places.
    Note: Boxes aren't created, just moved to custom positions (so some vanilla boxes are missing)."""
    display_name = "Add Custom Item Boxes"

class ShortcutsAsLocations(DefaultOnToggle):
    """Grants checks from completing shortcuts. Some shortcuts require items like mushrooms."""
    display_name = "Shortcuts as Locations"

class CourseShuffle(Choice):
    """How the courses are shuffled in cups."""
    display_name = "Course Shuffle"
    option_vanilla = 0
    option_shuffle_once = 1
    # TODO: option_shuffle_per_class = 2
    default = 1

# Items
class ItemsForEverybody(Range):
    """How many global item unlocks there are."""
    display_name = "Items for Everybody"
    range_start = 0
    range_end = 19
    default = 4

class ItemsPerCharacter(Range):
    """How many item unlocks there are per character."""
    display_name = "Items per Character"
    range_start = 0
    range_end = 5
    default = 3

class StartItemsPerCharacter(Range):
    """Unlocks some items for the characters straight away."""
    display_name = "Start Items per Character"
    range_start = 0
    range_end = 5
    default = 1

class FranticItems(NamedRange):
    """Changes the item distribution to give all items evenly regardless of current position.
    0 = vanilla, 100 = every item has equal chance, values in between are possible."""
    display_name = "Frantic Items"
    range_start = 0
    range_end = 100
    default = 0
    special_range_names = {
        "vanilla": 0,
        "medium": 50,
        "frantic": 100,
    }

class GuaranteedItems(DefaultOnToggle):
    """Guarantees getting unlocked items if they are appropriate for your position.
    For example, if your character has mushroom unlocked, you cannot get blank item at 4th or worse place."""
    display_name = "Guaranteed Items"

# Karts
class KartUpgrades(Range):
    """How many random kart stat upgrades there are total.
    Unlike progressive speed upgrades, these upgrades are tied to certain vehicles."""
    display_name = "Kart Upgrades"
    range_start = 0
    range_end = 100
    default = 20

class SpeedUpgrades(DefaultOnToggle):
    """Adds 3 Progressive Speed Upgrades to the pool.
    You start at a slight disadvantage (90 % speed) and collecting all the speed upgrades gets you to 110 % speed.
    Disabling this sets logic difficulty on hard if it's lower."""
    display_name = "Speed Upgrades"

# Traps
class TrapChance(Range):
    """Percentage of how many filler items are converted into traps.
    If this is 0, no traps will be in the pool. 100 means all filler items are traps.
    Use weight options below to choose which traps will be more likely."""
    display_name = "Trap Chance"
    range_start = 0
    range_end = 100
    default = 5

class BananaRainTrapWeight(Range):
    """Bananas will spawn in front of you!
    Bigger number = bigger chance of occurring."""
    display_name = "Banana Rain Trap Weight"
    range_start = 0
    range_end = 100
    default = 30

class ShellRainTrapWeight(Range):
    """Shells will spawn in front of you!
    Bigger number = bigger chance of occurring."""
    display_name = "Shell Rain Trap Weight"
    range_start = 0
    range_end = 100
    default = 30

class BombRainTrapWeight(Range):
    """Bob-ombs will spawn in front of you!
    Bigger number = bigger chance of occurring."""
    display_name = "Bomb Rain Trap Weight"
    range_start = 0
    range_end = 100
    default = 10

class OverlappingStartTrapWeight(Range):
    """All karts will start at the same position on next race.
    Loud sound warning!"""
    display_name = "Overlapping Start Trap Weight"
    range_start = 0
    range_end = 100
    default = 5

# Quality of Life
class Mirror200cc(Toggle):
    """Mirror mode is 200cc if enabled."""
    display_name = "Mirror is 200cc"

class Faster50cc100cc(Toggle):
    """Makes 50cc as fast as 100cc and 100cc closer to 150cc."""
    display_name = "Faster 50cc and 100cc"

class AllCupTourLength(Range):
    """How many races are in the All Cup Tour? 16 = vanilla. Default 8."""
    display_name = "All Cup Tour Length"
    range_start = 2
    range_end = 16
    default = 8

class ShorterCourses(Toggle):
    """Makes most courses 2 laps long. Might make the flow of the game better."""
    display_name = "Shorter Courses"

class CustomLapCounts(OptionCounter):
    """Set custom amount of laps on each course.
    Write each course on its own line, followed by : and number of laps(max 9)."""
    display_name = "Custom Lap Counts"
    default = {"Wario Colosseum": 2}
    schema = Schema({
        Optional("Luigi Circuit"): lambda n: 1 <= n <= 9,
        Optional("Peach Beach"): lambda n: 1 <= n <= 9,
        Optional("Baby Park"): lambda n: 1 <= n <= 9,
        Optional("Dry Dry Desert"): lambda n: 1 <= n <= 9,
        Optional("Mushroom Bridge"): lambda n: 1 <= n <= 9,
        Optional("Mario Circuit"): lambda n: 1 <= n <= 9,
        Optional("Daisy Cruiser"): lambda n: 1 <= n <= 9,
        Optional("Waluigi Stadium"): lambda n: 1 <= n <= 9,
        Optional("Sherbet Land"): lambda n: 1 <= n <= 9,
        Optional("Mushroom City"): lambda n: 1 <= n <= 9,
        Optional("Yoshi Circuit"): lambda n: 1 <= n <= 9,
        Optional("DK Mountain"): lambda n: 1 <= n <= 9,
        Optional("Wario Colosseum"): lambda n: 1 <= n <= 9,
        Optional("Dino Dino Jungle"): lambda n: 1 <= n <= 9,
        Optional("Bowser's Castle"): lambda n: 1 <= n <= 9,
        Optional("Rainbow Road"): lambda n: 1 <= n <= 9,
    })


@dataclass
class MkddOptions(PerGameCommonOptions):
    goal: Goal
    trophy_requirement_percent: TrophyRequirementPercent
    grand_prix_trophies: GrandPrixTrophies
    shuffle_extra_trophies: ShuffleExtraTrophies
    all_cup_tour_min_cc: AllCupTourMinCC
    all_cup_tour_min_rank: AllCupTourMinRank

    logic_difficulty: LogicDifficulty
    time_trials: TimeTrials
    item_boxes_as_locations: ItemBoxesAsLocations
    add_custom_item_boxes: AddCustomItemBoxes
    shortcuts_as_locations: ShortcutsAsLocations
    course_shuffle: CourseShuffle

    items_for_everybody: ItemsForEverybody
    items_per_character: ItemsPerCharacter
    start_items_per_character: StartItemsPerCharacter
    frantic_items: FranticItems
    guaranteed_items: GuaranteedItems

    kart_upgrades: KartUpgrades
    speed_upgrades: SpeedUpgrades
    
    trap_chance: TrapChance
    banana_rain_trap_weight: BananaRainTrapWeight
    shell_rain_trap_weight: ShellRainTrapWeight
    bomb_rain_trap_weight: BombRainTrapWeight
    overlapping_start_trap_weight: OverlappingStartTrapWeight

    mirror_200cc: Mirror200cc
    faster_50cc_100cc: Faster50cc100cc
    all_cup_tour_length: AllCupTourLength
    shorter_courses: ShorterCourses
    custom_lap_counts: CustomLapCounts

    start_inventory_from_pool: StartInventoryPool

    def to_slot_data(self) -> dict[str, any]:
        """Returns dict of relevant options for UT or the client."""
        return self.as_dict(
            "all_cup_tour_min_cc",
            "all_cup_tour_min_rank",
            "logic_difficulty",
            "time_trials",
            "item_boxes_as_locations",
            "add_custom_item_boxes",
            "shortcuts_as_locations",
            "frantic_items",
            "guaranteed_items",
            "all_cup_tour_length",
            "mirror_200cc",
            "faster_50cc_100cc",
            "custom_lap_counts",
        )

    def update_from_slot_data(self, slot_data: dict[str, any]) -> None:
        """Sets options that are relayed in slot data."""
        for key, val in slot_data.items():
            if key in MkddOptions.type_hints: # Filter non-option data.
                setattr(self, key, val)

def init_options() -> MkddOptions:
    """Initializes options object with default values."""
    return MkddOptions(**{key: val.default for key, val in MkddOptions.type_hints.items()})


option_groups: list[OptionGroup] = [
    OptionGroup("Goal", [
        Goal,
        TrophyRequirementPercent,
        GrandPrixTrophies,
        ShuffleExtraTrophies,
        AllCupTourMinCC,
        AllCupTourMinRank,
    ]),
    OptionGroup("Content", [
        LogicDifficulty,
        TimeTrials,
        ItemBoxesAsLocations,
        AddCustomItemBoxes,
        ShortcutsAsLocations,
        CourseShuffle,
    ]),
    OptionGroup("Items", [
        ItemsForEverybody,
        ItemsPerCharacter,
        StartItemsPerCharacter,
        FranticItems,
        GuaranteedItems,
    ]),
    OptionGroup("Karts", [
        KartUpgrades,
        SpeedUpgrades,
    ]),
    OptionGroup("Traps", [
        TrapChance,
        BananaRainTrapWeight,
        ShellRainTrapWeight,
        BombRainTrapWeight,
        OverlappingStartTrapWeight,
    ]),
    OptionGroup("Quality of Life", [
        Mirror200cc,
        Faster50cc100cc,
        AllCupTourLength,
        ShorterCourses,
        CustomLapCounts,
    ]),
]
