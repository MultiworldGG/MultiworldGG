"""This module contains options for if defeating the daxx warship is required to goal"""

from Options import Toggle
from worlds.rac3.constants.options import RAC3OPTION


class GoalBossWarship(Toggle):
    """Determines if defeating the Warship on Daxx is required to goal"""
    display_name = RAC3OPTION.GOAL_BOSS_WARSHIP
