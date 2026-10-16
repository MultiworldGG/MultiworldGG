"""This module contains options for VidComic Health Upgrade locations"""

from Options import Choice
from worlds.rac3.constants.options import RAC3OPTION


class VidComicHealthUpgrades(Choice):
    """
    Determines if the VidComic Health Upgrades should be locations or not.
    ------------------------------------------------------------------------------------
    Disabled: The VidComic Health Upgrades are not locations.
    Enabled:  The VidComic Health Upgrades are locations.
    ------------------------------------------------------------------------------------
    Note: This option has no effect if VidComics are disabled.
    """
    display_name = RAC3OPTION.VIDCOMIC_HEALTH_UPGRADES
    option_disabled = 0
    option_enabled = 1
    default = 1
