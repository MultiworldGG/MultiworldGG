### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from ..names import itemnames
from . import itemdefs as idefs

item_groups: dict[str, set[str]] = {
    ## Main Groups
    itemnames.item_group_weapon: {
        *idefs.item_weapons.keys(),
        *idefs.item_p_weapons.keys(),
        *idefs.item_dlc_weapons.keys(),
        *idefs.item_dlc_p_weapons.keys()
    },
    itemnames.item_group_weapon_ex: {
        *idefs.item_weapon_ex.keys(),
        *idefs.item_dlc_weapon_ex.keys()
    },
    itemnames.item_group_charm: {
        *idefs.item_charms.keys(),
        *idefs.item_dlc_charms.keys(),
        itemnames.item_charm_dlc_cookie
    },
    itemnames.item_group_super: {
        *idefs.item_super.keys(),
        *idefs.item_dlc_chalice_super.keys()
    },
    itemnames.item_group_ability: {
        *idefs.item_abilities.keys(),
        *idefs.item_dlc_chalice_abilities.keys(),
    },
    #itemnames.item_group_aim_ability: {
    #    *idefs.item_abilities_aim.keys(),
    #    *idefs.item_dlc_chalice_abilities_aim.keys()
    #},

    ## Aliases
    itemnames.item_contract_a: {itemnames.item_contract},
    itemnames.item_plane_gun_a: {itemnames.item_plane_gun},
    itemnames.item_ability_crouch_a: {itemnames.item_ability_crouch},
    itemnames.item_dlc_cplane_gun_a: {itemnames.item_dlc_cplane_gun},
    itemnames.item_ability_dlc_ccrouch_a: {itemnames.item_ability_dlc_ccrouch}
}
