"""This module contains options for ship vendor locations"""

from Options import DefaultOnToggle
from worlds.rac3.constants.options import RAC3OPTION


class ShipVendors(DefaultOnToggle):
    """
    Determines whether ship vendor cosmetics are locations in the world.
    -----------------------------------------------------------------------------------------------
    No:   No ship vendor cosmetics are locations.
    Yes:  Ship vendor cosmetics are added as locations.
    -----------------------------------------------------------------------------------------------
    Note: Each planet you have will put the next 2 items in the ship vendor in order of how they would appear in the
    vanilla game.
    You cannot change ship cosmetics with this option enabled.
    """
    display_name = RAC3OPTION.SHIP_VENDOR
