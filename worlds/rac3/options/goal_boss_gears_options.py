"""This module contains options for if defeating courtney gears is required to goal"""

from Options import Toggle
from worlds.rac3.constants.options import RAC3OPTION


class GoalBossGears(Toggle):
    """Determines if defeating Courtney Gears on Obani Draco is required to goal"""
    display_name = RAC3OPTION.GOAL_BOSS_GEARS
