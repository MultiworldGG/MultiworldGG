"""This module contains options for if defeating the momma tyhrranoid is required to goal"""

from Options import Toggle
from worlds.rac3.constants.options import RAC3OPTION


class GoalBossNoid(Toggle):
    """
    Determines if defeating the Momma Tyhrranoid on Tyhrranosis is required to goal
    IRON HARD ABS
    """
    display_name = RAC3OPTION.GOAL_BOSS_NOID
