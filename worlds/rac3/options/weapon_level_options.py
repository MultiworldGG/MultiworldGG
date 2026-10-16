"""This module contains options for Weapon Level locations"""

from Options import OptionSet
from worlds.rac3.constants.options import RAC3OPTION


class WeaponLevels(OptionSet):
    """
    Determines whether weapon levels should be locations or not.
    -----------------------------------------------------------------------------------------------
    All weapon levels can be locations (including V6, V7, V8 if ngplus_items are enabled).
    Only locations for the selected levels will be added. To disable weapon level locations, leave the brackets empty.
    The valid keys are the following: V2, V3, V4, V5, V6, V7, V8
    -----------------------------------------------------------------------------------------------
    Note: If progressive weapons are enabled, leveling will be forced to manual leveling instead of automatic leveling.
    """
    display_name = RAC3OPTION.WEAPON_LEVEL_LOCATIONS
    valid_keys = frozenset({
        "V2", "V3", "V4", "V5", "V6", "V7", "V8"
    })
    default = frozenset({"V2", "V3", "V4", "V5", "V6", "V7", "V8"})
