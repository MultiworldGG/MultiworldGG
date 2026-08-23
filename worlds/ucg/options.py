from dataclasses import dataclass

from Options import PerGameCommonOptions, Toggle, DefaultOnToggle, OptionSet, DeathLink, Range, Choice

class GoalLevel(Choice):
    """
    Set what goal level you want to do have as your final level.
    This level is removed from the multiworld, if selected, and will not be an item sent.
    Levels from World 5 or World P will force enable those worlds if selected, and the worlds aren't enabled
    """
    display_name = "Goal Level"
    default = 1

    option_3_18 = 0
    option_4_17 = 1
    option_5_18 = 2
    option_P_17 = 3

class PrismUnlockAmount(Range):
    """
    How many prisms are required to be obtained in total before your goal level unlocks.
    Requirement may be forcefully lowered to account for disabled levels or peak checks being disabled.
    You can always view the required amount you need in game to reference it.
    """
    display_name = "Goal Level Prism Amount"

    default = 200
    range_start = 50
    range_end = 560

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

    When enabled, these make up all of the filler in your pool. When disabled, that filler is all Uncanny Cat Spray instead.
    Either way you still get one of each of the costumes and other one-off filler items.
    """
    display_name = "Temporary Modifiers"

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

class DeathLinkAmnesty(Range):
    """
    Amount of deaths before sending a Death Link.
    This can be changed in the mod config.
    """
    display_name = "Death Link Amnesty"
    range_start = 1
    range_end = 10
    default = 5

@dataclass
class UncannyCatOptions(PerGameCommonOptions):
    goal_level: GoalLevel
    prism_unlock_amount: PrismUnlockAmount
    gimmick_lock: GimmickLocking
    level_unlock_style: LevelUnlockStyle
    minigames: Minigames
    world_5_levels: World5Levels
    world_p_levels: WorldPLevels
    world_e_levels: WorldELevels
    peak_checks: PeakChecks
    rank_check_difficulty: RankCheckDifficulty
    temp_modifiers: TemporaryModifiers
    chill_mode: ChillMode
    panic_mode: PanicMode
    death_link: DeathLink
    death_link_amnesty: DeathLinkAmnesty