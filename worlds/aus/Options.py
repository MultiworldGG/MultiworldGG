from dataclasses import dataclass
from Options import Choice, Option, Toggle, Range, NamedRange, PerGameCommonOptions, DeathLinkMixin

class ArcadeOptions():
    OFF = 0
    PURCHASE_ONLY = 1
    MUST_WIN = 2

class GoldOrbsRequired(Range):
    """
    How many gold orbs are required for BlackCastle, and thus, to goal
    
    Must be between 0 and 10.
    """
    display_name = "Gold Orb Requirement"
    default = 7
    range_start = 0
    range_end = 10
    
class DifficultySelector(NamedRange):
    """
    The difficulty the game will be set to.
    0 = Simple
    1 = Regular (recommended)
    2 = Difficult
    3 = Masterful
    4 = Insanity (Masterful + one hit kill)
    
    This game can be VERY difficult, only choose a higher difficulty if you know what you're doing!
    """
    display_name = "Difficulty"
    default = 1
    range_start = 0
    range_end = 4
    special_range_names = {
        "simple": 0,
        "regular": 1,
        "difficult": 2,
        "masterful": 3,
        "insanity": 4,
    }
    
class ArcadeMode(Choice):
    """Determines the behaviour of the three arcade machines in SkyTown.
    OFF - The arcade machines are disabled. 3 hearts are removed from the pool
    PURCHASE_ONLY - The arcade machines must be purchased but you don't have to play them to get the check
    MUST_WIN - You must purchase the arcade machine AND get the high score to get the check. (Note the JumpBox minigame is quite difficult)"""
    display_name = "Arcade Behaviour"
    default = ArcadeOptions.PURCHASE_ONLY
    option_off = ArcadeOptions.OFF
    option_purchase_only = ArcadeOptions.PURCHASE_ONLY
    option_must_win = ArcadeOptions.MUST_WIN

class EasyRainbowDive(Toggle):
    """Makes the RainbowDive checks easier by significantly reducing the amount of points required for each prize"""
    display_name = "Easy RainbowDive"

class DisableHeartBarriers(Toggle):
    """Removes all heart barriers from the world, making their checks easier by not requiring you to reach them without taking damage"""
    display_name = "Disable All Heart Barriers"

class ClosedEndLogic(Toggle):
    """Adds into logic locations that require you to return to previous save after getting them, due to them putting you in a dead end without specific items.
    This affects three areas specifically: the two checks after the first Grotto boss (usually requiring 2 jump upgrades to leave), the check after the first boss in StoneCastle (usually requiring DiveBomb to leave), and the second half of FireCage (requiring yellow energy to get to the save)"""
    display_name = "Enable Return to Previous Save Logic"

class HardLogic(Toggle):
    """Adds several difficult jumps into logic.
    This assumes a deep knowledge of the game and ability to perform jumps that are either very precise, unintended, or unintuitive.
    None of these require damage boosting, as logic always assumes maximum difficulty"""
    display_name = "Enable Unintuitive and Unintended Logic"

class GhostSpawnRate(Range):
    """
    Percentage chance of ghosts spawning, per room. 0 is disabled, 100 means they appear every room.
    Note that not all rooms have ghosts enabled in the first place.
    Ghosts won't spawn until you find at least 1 gold orb.
    In vanilla on Regular, this number would be about 5, for reference.
    Must be between 0 and 100.
    """
    display_name = "Ghost Spawn Chance (Percentage)"
    default = 5
    range_start = 0
    range_end = 100

class SpecialBossMusic(Range):
    """
    Percentage chance of using the special insanity boss music when fighting a (non-unique) boss.
    Purely cosmetic and has no gameplay effect.
    Must be between 0 and 100.
    """
    display_name = "Special Boss Music (Percentage)"
    default = 0
    range_start = 0
    range_end = 100
    
    
@dataclass
class AUSOptions(PerGameCommonOptions, DeathLinkMixin):
    gold_orbs_required: GoldOrbsRequired
    difficulty: DifficultySelector
    arcade_mode: ArcadeMode
    easy_rainbowdive: EasyRainbowDive
    disable_heart_barriers: DisableHeartBarriers
    ghost_spawn_rate: GhostSpawnRate
    special_boss_music: SpecialBossMusic
    hard_logic: HardLogic
    closed_end_logic: ClosedEndLogic
    
  
  