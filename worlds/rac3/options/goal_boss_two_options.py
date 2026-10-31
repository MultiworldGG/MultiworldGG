"""This module contains options for if defeating the terrible two is required to goal"""

from Options import Toggle
from worlds.rac3.constants.options import RAC3OPTION


class GoalBossTwo(Toggle):
    """Determines if defeating The Terrible Two on Annihilation Nation is required to goal"""
    display_name = RAC3OPTION.GOAL_BOSS_TWO
