"""This module contains options for how much nanotech is required to goal"""

from Options import Range
from worlds.rac3.constants.options import RAC3OPTION


class GoalNano(Range):
    """
    Determines what nanotech level is required to goal.
    -----------------------------------------------------------------------------------------------
    Nanotech starts at level 10 and can go up to nanotech level 200.
    This option is capped at 100 if ngplus_start is disabled.
    -----------------------------------------------------------------------------------------------
    """

    display_name = RAC3OPTION.GOAL_NANO
    range_start = 10
    range_end = 200
    default = 10
