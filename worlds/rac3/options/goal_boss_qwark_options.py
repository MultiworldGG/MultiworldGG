"""This module contains options for if defeating captain qwark is required to goal"""

from Options import Toggle
from worlds.rac3.constants.options import RAC3OPTION


class GoalBossQwark(Toggle):
    """Determines if defeating Captain Qwark on Florana is required to goal"""
    display_name = RAC3OPTION.GOAL_BOSS_QWARK
