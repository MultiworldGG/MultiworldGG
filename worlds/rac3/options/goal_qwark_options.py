"""This module contains options for if completing the qwarktastic battle is required to goal"""

from Options import Toggle
from worlds.rac3.constants.options import RAC3OPTION


class GoalQwark(Toggle):
    """
    Determines if completing the Qwarktastic Battle is required to goal
    --------------------------------------------------------------------------------------
    Off:  Qwarktastic Battle is not required to goal
    On:   Qwarktastic Battle is required to goal
    ---------------------------------------------------------------------------------------
    Completing this mission will give you an item
    """
    display_name = RAC3OPTION.GOAL_QWARK
