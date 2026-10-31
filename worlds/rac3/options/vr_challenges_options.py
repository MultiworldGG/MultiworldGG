"""This module contains options for Phoenix VR mission locations"""

from Options import DefaultOnToggle
from worlds.rac3.constants.options import RAC3OPTION


class VRChallenges(DefaultOnToggle):
    """
    Determines whether VR Challenges and anything that is located in or behind them is a location.
    -----------------------------------------------------------------------------------------------
    No:   Removes anything that is located in or behind a VR Challenge from being a location.
    Yes:  VR Challenges, and anything directly locked behind them, are added as locations.
    -----------------------------------------------------------------------------------------------
    Any Skill Points or Titanium Bolts are added if their respective setting is enabled.
    This option also includes the VR Gadget Training Challenge before Daxx and all of its checks
    """
    display_name = RAC3OPTION.VR_CHALLENGES
