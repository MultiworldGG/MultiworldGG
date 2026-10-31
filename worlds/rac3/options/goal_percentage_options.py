"""This module contains options for how many location collections are required to goal"""

from Options import Range
from worlds.rac3.constants.options import RAC3OPTION


class GoalCompletion(Range):
    """Determines what location collection percentage is required to goal."""

    display_name = RAC3OPTION.GOAL_COMPLETION
    range_start = 0
    range_end = 100
    default = 0
