"""This module contains options for titanium bolt locations"""

from Options import DefaultOnToggle
from worlds.rac3.constants.options import RAC3OPTION


class TitaniumBolts(DefaultOnToggle):
    """
    Determines whether Titanium Bolts are locations in the world.
    -----------------------------------------------------------------------------------------------
    No:   No Titanium Bolts are locations.
    Yes:  Titanium Bolts are added as locations.
    -----------------------------------------------------------------------------------------------
    Any Titanium bolts locked behind other locations such as Ranger Missions require those options to be enabled
    """
    display_name = RAC3OPTION.TITANIUM_BOLTS
