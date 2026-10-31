"""This module contains options for if defeating the biobliterator is required to goal"""

from Options import DefaultOnToggle
from worlds.rac3.constants.options import RAC3OPTION


class GoalBio(DefaultOnToggle):
    """
    Determines if defeating the Biobliterator is required to goal
    --------------------------------------------------------------------------------------
    Off:  Biobliterator is not required, Goal is triggered the instant all other conditions are met
    On:   Biobliterator is required, it is the final goal that is unlocked after all other conditions have been met
    ---------------------------------------------------------------------------------------
    """
    display_name = RAC3OPTION.GOAL_BIO
