"""This module contains options for weapon mods items"""

from Options import Choice
from worlds.rac3.constants.options import RAC3OPTION


class WeaponMods(Choice):
    """
    Determines whether weapon mods are items in the multiworld.
    -----------------------------------------------------------------------------------------------
    Vanilla:         Weapon mods are not added as items. Mods are unlocked like they are in the base game,
                     but can only appear on weapons that have them in the base game.
    Modpack:         Weapon modpacks are added as items. Receiving a modpack unlocks all 3 mods for that weapon.
    Individual Mods: Shock, Acid, and Lock-on mods are all added as separate items for each weapon in the item pool.
    -----------------------------------------------------------------------------------------------
    If this option is not set to Vanilla, any weapon can get any weapon mod.
    Even those that are not normally compatible in the base game.
    Some mods might not behave as expected on weapons that they are not normally compatible with.
    """
    display_name = RAC3OPTION.WEAPON_MODS
    option_vanilla = 0
    option_modpack = 1
    option_individual_mods = 2
    default = 0
