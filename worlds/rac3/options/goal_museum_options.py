"""This module contains options for if unlocking the Insomniac Museum Teleport is required to goal"""

from Options import Toggle
from worlds.rac3.constants.options import RAC3OPTION


class GoalMuseum(Toggle):
    """
    Determines if unlocking the Insomniac Museum Teleporter is required to goal
    --------------------------------------------------------------------------------------
    Off:  Insomniac Museum Teleporter is not required to goal
    On:   Insomniac Museum Teleporter is required to goal
    ---------------------------------------------------------------------------------------
    WARNING: This requires ALL TROPHIES, effectively a 100% completion of the game
    """
    display_name = RAC3OPTION.GOAL_MUSEUM
