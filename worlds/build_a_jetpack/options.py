from dataclasses import dataclass

from Options import Choice, DeathLink, OptionGroup, PerGameCommonOptions, Range, Toggle

class Fishsanity(Toggle):
    """
    Adds locations for collecting each of the 17 types of fish.
    """

    display_name = "Fishsanity"

class HarshPressure(Toggle):
    """
    Makes high pressure zones drain oxygen far more rapidly, making diving suits more important.
    """

    display_name = "Harsh Pressure"

class ExtraUpgrades(Toggle):
    """
    Adds extra upgrades not present in the original game.
    Rapid Dive: Hold down to dive faster
    Shield: Lose less oxygen when getting hurt by hostile fish
    Insurance: When drowning, fish are sold for a fraction of their normal sell price. Materials are still lost.
    
    Note: This adds 11 items. Fishsanity must be enabled for there to be enough space for these items.
    If Fishsanity is not enabled, this option will be forced off.
    """

    display_name = "Extra Upgrades"

class TrapChance(Range):
    """
    Percentage chance to replace money filler with a Hostile Trap.
    Hostile Traps turn all fish hostile for 10 seconds.
    """

    display_name = "Trap Chance"

    range_start = 0
    range_end = 100
    default = 0

@dataclass
class BuildJetpackOptions(PerGameCommonOptions):
    death_link: DeathLink
    fishsanity: Fishsanity
    harsh_pressure: HarshPressure
    extra_upgrades: ExtraUpgrades
    trap_chance: TrapChance