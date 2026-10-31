"""This module contains options for if defeating dr nefarious is required to goal"""

from Options import Toggle
from worlds.rac3.constants.options import RAC3OPTION


class GoalNef(Toggle):
    """
    Determines if defeating Dr Nefarious is required to goal
    --------------------------------------------------------------------------------------
    Off:  Dr Nefarious is not required, Goal is triggered the instant all other conditions are met
    On:   Dr Nefarious is required, it is unlocked after all other conditions have been met
    ---------------------------------------------------------------------------------------
    If the Biobliterator is required, this option does nothing
    """
    display_name = RAC3OPTION.GOAL_NEF
