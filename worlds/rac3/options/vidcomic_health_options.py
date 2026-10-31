"""This module contains options for VidComic Health Upgrade locations"""

from Options import DefaultOnToggle
from worlds.rac3.constants.options import RAC3OPTION


class VidComicHealthUpgrades(DefaultOnToggle):
    """
    Determines if the VidComic Health Upgrades should be locations or not.
    ------------------------------------------------------------------------------------
    No:   The VidComic Health Upgrades are not locations.
    Yes:  The VidComic Health Upgrades are locations.
    ------------------------------------------------------------------------------------
    Note: This option has no effect if VidComics are disabled.
    """
    display_name = RAC3OPTION.VIDCOMIC_HEALTH_UPGRADES
