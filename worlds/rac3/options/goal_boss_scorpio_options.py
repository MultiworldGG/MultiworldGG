"""This module contains options for if defeating scorpio is required to goal"""

from Options import Toggle
from worlds.rac3.constants.options import RAC3OPTION


class GoalBossScorpio(Toggle):
    """Determines if defeating Scorpio on Annihilation Nation is required to goal"""
    display_name = RAC3OPTION.GOAL_BOSS_SCORPIO
