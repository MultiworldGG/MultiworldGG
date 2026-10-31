"""This module contains options for how many skillpoints are required to goal"""

from Options import Range
from worlds.rac3.constants.options import RAC3OPTION


class GoalSkillpoints(Range):
    """Determines how many Skillpoints are required to goal."""

    display_name = RAC3OPTION.GOAL_SKILLPOINTS
    range_start = 0
    range_end = 30
    default = 0
