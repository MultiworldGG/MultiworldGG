"""This module contains options for weapon vendor locations"""

from Options import DefaultOnToggle
from worlds.rac3.constants.options import RAC3OPTION


class WeaponVendors(DefaultOnToggle):
    """
    Determines whether weapon vendors are locations in the world.
    -----------------------------------------------------------------------------------------------
    No:   No weapon vendors are locations.
    Yes:  Weapon vendors are added as locations.
    -----------------------------------------------------------------------------------------------
    Weapons are still randomized regardless of this setting.
    """
    display_name = RAC3OPTION.WEAPON_VENDORS
