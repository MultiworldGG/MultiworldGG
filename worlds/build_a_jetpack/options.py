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

@dataclass
class BuildJetpackOptions(PerGameCommonOptions):
    death_link: DeathLink
    fishsanity: Fishsanity
    harsh_pressure: HarshPressure