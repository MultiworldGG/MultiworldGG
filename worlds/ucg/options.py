from dataclasses import dataclass

from Options import PerGameCommonOptions, Toggle, DefaultOnToggle, OptionSet, DeathLink, Range, Choice, OptionError

from .locations import EXCLUDABLE_LEVEL_IDS

class GoalLevel(Choice):
    """
    Set what goal level you want to do have as your final level.
    This level is removed from the multiworld, if selected, and will not be an item sent.
    Levels from World 5 or World P will force enable those worlds if selected, and the worlds aren't enabled
    4-18 is a level with no gameplay or uncanny cat, so is provided as an option if you want to just win when you are at go mode.
    """
    display_name = "Goal Level"
    default = 1

    option_3_18 = 0
    option_4_17 = 1
    option_4_18 = 2
    option_5_18 = 3
    option_P_17 = 4

class PrismUnlockAmount(Range):
    """
    How many in game rank prisms are required to be obtained in total before your goal level unlocks.
    Requirement may be forcefully lowered to account for disabled levels or peak checks being disabled.
    You can always view the required amount you need in game to reference it.

    Does nothing if macguffin goal is enabled.
    """
    display_name = "Goal Level Prism Amount"

    default = 200
    range_start = 50
    range_end = 560

class MacguffinGoal(Toggle):
    """
    Sets your goal to require a specified amount of "Cannium Prism" items instead of a specific requirement.
    This is a macguffin item that unlocks the goal level when reaching the specified amount.
    """
    display_name = "Macguffin Goal"

class MacguffinAmount(Range):
    """
    How many macguffin "Cannium Prism" items are added into the multiworld.
    Does nothing if macguffin goal is disabled.
    May be automatically lowered depending on settings and excluded levels.
    """
    display_name = "Goal Level Macguffin Amount"

    default = 40
    range_start = 10
    range_end = 50

class MacguffinPercentRequired(Range):
    """
    What percentage "Cannium Prism" items are required to be obtained in total before your goal level unlocks.
    Does nothing if macguffin goal is disabled.
    """
    display_name = "Macguffin Required Percentage"

    default = 75
    range_start = 25
    range_end = 100

class LevelUnlockStyle(Choice):
    """
    How level unlocks are handled.

    Individual: All level unlocks are individual items you must be sent
    World: Worlds are unlocks that you must be sent, you get access to all levels after being sent that world
    """
    display_name = "Level Unlock Style"

    default = 0
    option_individual = 0
    option_world = 1

class GimmickLocking(DefaultOnToggle):
    """
    Lock level gimmicks such as wormholes, dogs, toggle switches, etc. behind items in the multiworld.
    """
    display_name = "Gimmick Locking"

class Minigames(Toggle):
    """
    Enable minigames as checks, such as Bort Bash, UNCANNY_DASH, Meowls, etc. 
    """
    display_name = "Minigames"

class World5Levels(Toggle):
    """
    Include World 5 (Elysian Fields) levels as checks.
    """
    display_name = "World 5 Levels"

class WorldPLevels(Toggle):
    """
    Include World P (Cosmic Championship) levels as checks. These are a big step up in difficulty, so be warned 
    """
    display_name = "World P Levels"

class WorldELevels(Toggle):
    """
    Include World E levels as checks, which are exclusive levels from the Endless Shuffle.
    """
    display_name = "World E Levels"

class PeakChecks(Toggle):
    """
    Add a check for gaining a "PEAK" rank in a level. These can be really difficult.
    """
    display_name = "Peak Checks"

class Coinsanity(Choice):
    """
    Add checks for every coin found in the levels.

    If you set this to All, it may be beneficial to make Uncanny Cat Spray a local item, to prevent bloating
    the multiworld with a huge amount of filler from your game. Please be cautious when using this setting
    without other people being aware of it, as this adds over 1000 locations into the game.

    Off: Coins are not checks.
    All: Adds checks for every individual coin.
    Full Clear: Adds checks for fully clearing all coins in a level, but leaves out individual coin checks.
    """
    display_name = "Coinsanity"

    default = 0
    option_off = 0
    option_all = 1
    option_full_clear = 2

class ExcludedLevels(OptionSet):
    """
    Remove levels from the multiworld completely. This removes all locations related to that level, and the level unlock item.
    Name levels by their id, e.g. "1-4, P-14, 5-3".

    Excluding a level also removes the prisms from that level in logic, so your goal prism amount
    may be forcefully lowered to a still-obtainable number.

    World 0 cannot be excluded at all (why would you want to?)
    """
    display_name = "Excluded Levels"
    valid_keys = EXCLUDABLE_LEVEL_IDS

    def verify_keys(self) -> None:
        # Level ids are case-insensitive, so "p-14" is the same key as "P-14".
        self.value = {key.strip().upper() for key in self.value}
        tutorial = sorted(key for key in self.value if key.startswith("0-"))
        if tutorial:
            raise OptionError(
                f"World 0 cannot be excluded, but {', '.join(tutorial)} was listed in Excluded Levels. "
                f"Its levels need no unlock item, so they are the only checks reachable at the start."
            )
        super().verify_keys()

class ExcludedMinigames(OptionSet):
    """
    Remove specific minigames from the multiworld completely. This removes all locations related to that minigame, and the minigame unlock item.
    Valid options are "Bort Bash", "UNCANNY_DASH", and "Meowls"
    """
    display_name = "Excluded Minigames"
    valid_keys = {"Bort Bash", "UNCANNY_DASH", "Meowls"}

class RankCheckDifficulty(Choice):
    """
    Which in-game rank sends the per-level rank check.

    OK: An "OK" (3 prism) rank or better sends the check.
    Good: A "GOOD" (4 prism) rank or better is required.

    Every level always has a rank check. This only sets how hard it is to send one.
    This also determines how many levels are required to goal your game for logic.
    """
    display_name = "Rank Check Difficulty"

    default = 1
    option_ok = 0
    option_good = 1
    
class TemporaryModifiers(DefaultOnToggle):
    """
    Adds temporary modifier items based on the existing modifiers, some of which are traps and some are useful. These last until you complete a level.
    If you find these too difficult, you can always go back to 0-1 to cycle through them, as that level will always be available.

    When enabled, these make up 50% of the filler in your world, or 30% of it with Coinsanity on (the rest is Uncanny Cat Spray, which prevents you from dying to the Uncanny Cat one time per item).
    When disabled, that filler is all Uncanny Cat Spray instead (besides the costumes and other one off fillers)
    """
    display_name = "Temporary Modifiers"
    
class BuffCatSpray(DefaultOnToggle):
    """
    Buffs the Uncanny Cat Spray item from doing nothing to giving you a one time protection against the Uncanny Cat.
    It is used up the moment you touch the Uncanny Cat, and doesn't come back upon restarting a level.
    """
    display_name = "Buff Uncanny Cat Spray"

class ChillMode(Toggle):
    """
    Enable the "Chill Mode" modifier that removes the Uncanny Cat entirely. This makes the game significantly easier.
    This can be disabled/enabled in the mod config.
    """
    display_name = "Chill Mode"

class PanicMode(Toggle):
    """
    Enable the "Panic Mode" modifier that speeds up the Uncanny Cat quite a bit. This makes the game significantly harder, and may
    result in unbeatable seeds depending on your skill levels. BE WARNED.

    DO NOT ENABLE THIS IF YOU AREN'T PREPARED FOR WHAT IT ENTAILS.

    Automatically disabled if "Chill Mode" is enabled.
    This can be disabled/enabled in the mod config.
    """
    display_name = "Panic Mode"

@dataclass
class UncannyCatOptions(PerGameCommonOptions):
    goal_level: GoalLevel
    prism_unlock_amount: PrismUnlockAmount
    macguffin_goal: MacguffinGoal
    macguffin_amount: MacguffinAmount
    macguffin_percent_required: MacguffinPercentRequired
    gimmick_lock: GimmickLocking
    level_unlock_style: LevelUnlockStyle
    minigames: Minigames
    world_5_levels: World5Levels
    world_p_levels: WorldPLevels
    world_e_levels: WorldELevels
    peak_checks: PeakChecks
    coinsanity: Coinsanity
    excluded_levels: ExcludedLevels
    excluded_minigames: ExcludedMinigames
    rank_check_difficulty: RankCheckDifficulty
    temp_modifiers: TemporaryModifiers
    buff_uncanny_cat_spray: BuffCatSpray
    chill_mode: ChillMode
    panic_mode: PanicMode
    death_link: DeathLink