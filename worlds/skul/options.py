from dataclasses import dataclass

from Options import Toggle, DeathLink, OptionGroup, PerGameCommonOptions, Range

class QuartzMult(Range):
    """
    Multiplier increase to the amount of dark quartz you get from all sources.
    """

    display_name = "Dark Quartz Multiplier"

    range_start = 1
    range_end = 8
    default = 3

class ReqRoomCount(Range):
    """
    How many rooms must be cleared per area.
    """

    display_name = "Required Room Count"

    range_start = 8
    range_end = 16
    default = 10

class ShrineChecks(Range):
    """
    Total number of shrine checks to generate across the game.
    """

    display_name = "Shrine Check Count"

    range_start = 10
    range_end = 50
    default = 25

class DeSkullTrapWeight(Range):
    """
    Percentage chance for a filler item to be a De-Skull Trap. Set to 0 to disable traps entirely.
    """

    display_name = "De-Skull Trap Weight"
    range_start = 0
    range_end = 100
    default = 20


@dataclass
class SkulOptions(PerGameCommonOptions):
    quartz_mult: QuartzMult
    req_room_count: ReqRoomCount
    shrine_checks_count: ShrineChecks
    de_skull_trap_weight: DeSkullTrapWeight
    death_link: DeathLink

option_groups = [
    OptionGroup(
        "Location Options",
        [ReqRoomCount, ShrineChecks],
    ),
    OptionGroup(
        "Quality of Life Options",
        [QuartzMult, DeSkullTrapWeight],
    ),
]

option_presets: dict = {}
