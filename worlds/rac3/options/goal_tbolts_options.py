"""This module contains options for how many titanium bolts are required to goal"""

from Options import Range
from worlds.rac3.constants.options import RAC3OPTION


class GoalTbolts(Range):
    """Determines how many Titanium Bolts are required to goal, 0 - 40"""

    display_name = RAC3OPTION.GOAL_TBOLTS
    range_start = 0
    range_end = 40
    default = 0
