"""This module contains options for Qwark VidComic locations"""

from Options import DefaultOnToggle
from worlds.rac3.constants.options import RAC3OPTION


class VidComics(DefaultOnToggle):
    """
    Determines whether VidComics and anything that is located in or behind them is a location.
    -----------------------------------------------------------------------------------------------
    No:   Removes anything that is located in or behind a VidComic from being a location.
    Yes:  VidComics, and anything directly locked behind them, are added as locations.
    -----------------------------------------------------------------------------------------------
    Any Skill Points or Titanium Bolts are added if their respective setting is enabled.
    """
    display_name = RAC3OPTION.VIDCOMICS
