"""This module contains options for if defeating the terror of talos is required to goal"""

from Options import Toggle
from worlds.rac3.constants.options import RAC3OPTION


class GoalBossTalos(Toggle):
    """Determines if defeating The Terror of Talos on Holostar Studios is required to goal"""
    display_name = RAC3OPTION.GOAL_BOSS_TALOS
