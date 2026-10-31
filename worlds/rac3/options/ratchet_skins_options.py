"""This module contains options for customizing ratchet's player skin"""

from Options import Choice
from worlds.rac3.constants.options import RAC3OPTION


class RatchetSkin(Choice):
    """
    Cosmetic:
    What Skin should Ratchet have?
    If the chosen skin is missing, reload your save file without saving or go to the armor vendor.
    """
    display_name = RAC3OPTION.PLAYER_SKIN
    option_default = 0
    option_old_school = 5
    option_snowman = 6
    option_tuxedo = 7
    option_buginoid = 8
    option_brainius = 9
    option_constructo_bot = 10
    option_robo_rooster = 11
    option_trooper = 12
    option_robo = 13
    default = 0
