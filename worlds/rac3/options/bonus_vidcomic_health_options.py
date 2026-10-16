"""This module contains additional VidComic Health Upgrades options"""

from Options import Range
from worlds.rac3.constants.options import RAC3OPTION


class BonusVidComicHealthUpgrades(Range):
    """
    Determines how many Bonus VidComic Health Upgrades are included in the item pool.
    These are extra upgrades that are not normally available in the vanilla game.
    -------------------------------------------------------------------------------
    Set to 0 for No extra upgrades.
    Set to 3 for all extra upgrades to be available.
    -------------------------------------------------------------------------------
    Note: This option has no effect if VidComics are disabled.
    """
    display_name = RAC3OPTION.BONUS_VIDCOMIC_HEALTH
    range_start = 0
    range_end = 3
    default = 3
