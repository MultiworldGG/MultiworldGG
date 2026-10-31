"""This module contains options for New Game Plus purchase locations"""

from Options import Toggle
from worlds.rac3.constants.options import RAC3OPTION


class NGPlusVendor(Toggle):
    """
    Determines if the RY3N0 Purchase should be a location in the vendor or not.
    ------------------------------------------------------------------------------------
    No:   The RY3N0 is not a purchasable location.
    Yes:  The RY3N0 is a purchasable location.
    ------------------------------------------------------------------------------------
    """
    display_name = RAC3OPTION.NGPLUS_VENDOR
