"""This module contains options for how many sewer crystals are required to goal"""

from Options import Range
from worlds.rac3.constants.options import RAC3OPTION


class GoalCrystal(Range):
    """Determines how many Sewer Crystals are required to goal, 0 - 101"""

    display_name = RAC3OPTION.GOAL_CRYSTAL
    range_start = 0
    range_end = 101
    default = 0
