"""This module contains options for if defeating klunk is required to goal"""

from Options import Toggle
from worlds.rac3.constants.options import RAC3OPTION


class GoalBossKlunk(Toggle):
    """Determines if defeating Klunk on Metropolis is required to goal"""
    display_name = RAC3OPTION.GOAL_BOSS_KLUNK
