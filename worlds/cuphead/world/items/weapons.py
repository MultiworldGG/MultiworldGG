### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from ..enums import WeaponMode
from ..names import itemnames
from ..options import CupheadOptions

weapon_dict: dict[int,str] = {
    0: itemnames.item_weapon_peashooter,
    1: itemnames.item_weapon_spread,
    2: itemnames.item_weapon_chaser,
    3: itemnames.item_weapon_lobber,
    4: itemnames.item_weapon_charge,
    5: itemnames.item_weapon_roundabout,
    6: itemnames.item_weapon_dlc_crackshot,
    7: itemnames.item_weapon_dlc_converge,
    8: itemnames.item_weapon_dlc_twistup,
}
weapon_ex_dict: dict[int,str] = {
    0: itemnames.item_weapon_peashooter_ex,
    1: itemnames.item_weapon_spread_ex,
    2: itemnames.item_weapon_chaser_ex,
    3: itemnames.item_weapon_lobber_ex,
    4: itemnames.item_weapon_charge_ex,
    5: itemnames.item_weapon_roundabout_ex,
    6: itemnames.item_weapon_dlc_crackshot_ex,
    7: itemnames.item_weapon_dlc_converge_ex,
    8: itemnames.item_weapon_dlc_twistup_ex,
}
weapon_p_dict: dict[int,str] = {
    0: itemnames.item_p_weapon_peashooter,
    1: itemnames.item_p_weapon_spread,
    2: itemnames.item_p_weapon_chaser,
    3: itemnames.item_p_weapon_lobber,
    4: itemnames.item_p_weapon_charge,
    5: itemnames.item_p_weapon_roundabout,
    6: itemnames.item_p_weapon_dlc_crackshot,
    7: itemnames.item_p_weapon_dlc_converge,
    8: itemnames.item_p_weapon_dlc_twistup,
}
weapon_to_index: dict[str, int] = {y:x for x,y in weapon_dict.items()}
weapon_p_to_index: dict[str, int] = {y:x for x,y in weapon_p_dict.items()}
weapon_ex_to_index: dict[str, int] = {y:x for x,y in weapon_ex_dict.items()}
all_weapon_to_index: dict[str, int] = {**weapon_to_index, **weapon_p_to_index, **weapon_ex_to_index}

def _get_weapon_dict(options: CupheadOptions, ex: bool = False, force_dlc_weapons: bool = False) -> dict[int, str]:
    dlc_weapons = options.use_dlc.bvalue or force_dlc_weapons
    orig_weapon_dict: dict[int,str] = (
        (weapon_ex_dict if ex else weapon_dict)
        if (options.weapon_mode.evalue & WeaponMode.EX_SEPARATE) > 0 else
        weapon_p_dict if (options.weapon_mode.evalue & WeaponMode.PROGRESSIVE) > 0 else
        weapon_dict
    )
    return {k: v for k, v in orig_weapon_dict.items() if k < 6 or dlc_weapons}

def get_weapon_dict(options: CupheadOptions, force_dlc_weapons: bool = False) -> dict[int, str]:
    return _get_weapon_dict(options, False, force_dlc_weapons)

def get_weapon_ex_dict(options: CupheadOptions, force_dlc_weapons: bool = False) -> dict[int, str]:
    return _get_weapon_dict(options, True, force_dlc_weapons)
