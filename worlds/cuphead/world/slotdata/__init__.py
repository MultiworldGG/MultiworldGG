### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
     from ... import CupheadWorld
     from ..options import CupheadOptions

def _get_feature_bits(options: "CupheadOptions") -> int:
    return 0

_slot_data_options: list[str] = [
    "boss_grade_checks",
    "boss_phase_checks",
    "contract_goal_requirements",
    "dlc_boss_chalice_checks",
    "dlc_chalice",
    "dlc_curse_mode",
    "dlc_ingredient_goal_requirements",
    "dlc_kingsleap",
    "dlc_rungun_chalice_checks",
    "ducklock_platdrop",
    "expert_mode",
    "freemove_isles",
    "logic_mode",
    "mode",
    "music_shuffle",
    "randomize_abilities",
    "rungun_grade_checks",
    "start_maxhealth",
    "start_maxhealth_p2",
    "start_weapon",
    "trap_loadout_anyweapon",
    "use_dlc",
    "weapon_mode",
]

def get_slot_data_options() -> frozenset[str]:
    return frozenset(_slot_data_options)

def fill_slot_data(world: "CupheadWorld") -> dict[str, Any]:
    slot_data: dict[str, Any] = {
        "version": world.SLOT_DATA_VERSION,
        "world_version": world.APWORLD_VERSION,
        "feature_bit_reqs": _get_feature_bits(world.options),
        "gen_bits": world.gen_bits,
        "resolved_start_weapon": world.resolved_start_weapon_index,
        "level_map": world.level_map,
        "shop_mode": world.options.shop_mode.value,
        "shop_map": world.shop.shop_map,
        "contract_requirements": world.options.get_contract_requirements_tuple(),
        "dlc_ingredient_requirements": world.options.dlc_ingredient_requirements.value,
        "deathlink": world.options.deathlink_mode.value if world.options.deathlink.bvalue else 0,
        "deathlink_grace_count": world.options.deathlink_grace_count.value,
    }
    for option in _slot_data_options:
        slot_data.update(world.options.as_dict(option))
    if world.settings.is_debug_bit_on(64):
        print(f"slot_data: {slot_data}")
    return slot_data
