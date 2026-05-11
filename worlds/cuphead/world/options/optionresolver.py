### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from random import Random
from typing import TYPE_CHECKING

from ..names import itemnames

if TYPE_CHECKING:
    from ... import CupheadWorld
    from . import CupheadOptions

def _set_coin_amounts(options_ref: "CupheadOptions"):
    use_dlc = options_ref.use_dlc.value
    extra_coins = options_ref.extra_coins.value
    total_single_coins = (40 if use_dlc else 37) + extra_coins
    total_double_coins = 5 if use_dlc else 0
    total_triple_coins = 2 if use_dlc else 1

    options_ref.coin_amounts.value = (total_single_coins, total_double_coins, total_triple_coins)


def _set_contract_requirements(options_ref: "CupheadOptions"):
    max_contracts = (5, 10, 17)
    total_req = options_ref.contract_requirements.value
    die1 = min(total_req // 3, max_contracts[0])
    die2 = min((die1 + total_req) // 2, max_contracts[1])

    options_ref.contract_requirements_isle2.value = die1
    options_ref.contract_requirements_isle3.value = die2


def _set_filler_item_weights(options_ref: "CupheadOptions", player: int, player_name: str):
    filler_items: list[str] = [
        itemnames.item_level_extrahealth,
        itemnames.item_level_supercharge,
        #itemnames.item_level_fastfire,
    ]
    filler_item_weights: list[int] = [
        options_ref.filler_weight_extrahealth.value,
        options_ref.filler_weight_supercharge.value,
        #options_ref.filler_weight_fastfire.value,
    ]
    options_ref.filler_item_weights.value = {
        item: weight
        for item, weight in zip(filler_items, filler_item_weights, strict=True)
        if weight > 0
    }
    if len(options_ref.filler_item_weights.value) == 0:
        print(
                f"Warning: For player {player} ({player_name}): Filler item weights cannot be all zero. "
                f"{filler_items} will have a weight of 1"
        )
        options_ref.filler_item_weights.value = dict.fromkeys(filler_items, 1)


def _set_trap_item_weights(options_ref: "CupheadOptions", player: int, player_name: str):
    trap_items: list[str] = [
        #itemnames.item_level_trap_fingerjam,
        #itemnames.item_level_trap_slowfire,
        itemnames.item_level_trap_superdrain,
        #itemnames.item_level_trap_loadout,
        #itemnames.item_level_trap_screen,
    ]
    trap_item_weights: list[int] = [
        #options_ref.trap_weight_fingerjam.value,
        #options_ref.trap_weight_slowfire.value,
        options_ref.trap_weight_superdrain.value,
        #options_ref.trap_weight_loadout.value,
        #0,
    ]
    options_ref.trap_item_weights.value = {
        trap: weight
        for trap, weight in zip(trap_items, trap_item_weights, strict=True)
        if weight > 0
    }
    if options_ref.traps.value > 0 and len(options_ref.trap_item_weights.value) == 0:
        print(
                f"Warning: For player {player} ({player_name}): Trap item weights cannot be all zero. "
                f"{trap_items} will have a weight of 1"
        )
        options_ref.trap_item_weights.value = dict.fromkeys(trap_items, 1)

# Shop Map (shop_index(weapons, charms)) # TODO: Maybe shuffle the amounts later
def _set_shop_map(options_ref: "CupheadOptions"):
    dlc = options_ref.use_dlc.value
    options_ref.shop_map.value = (
        [(2,2), (2,2), (1,2), (3,2)] if not dlc else [(2,2), (2,2), (2,2), (2,2)]
    )

def _get_random_start_weapon_pool(options: "CupheadOptions") -> list[int]:
    start_weapon = options.start_weapon
    max_weapon = start_weapon.option_dlc_twistup if options.use_dlc.value else start_weapon.option_roundabout
    explicit_weapons = list(range(start_weapon.option_peashooter, max_weapon + 1))

    if start_weapon.value == start_weapon.option_random_weapon:
        return explicit_weapons
    if start_weapon.value == start_weapon.random_value:
        return [*explicit_weapons, start_weapon.option_none]
    return []

def resolve_dependent_options(world: "CupheadWorld"):
    options = world.options
    if options.start_maxhealth_p2.value == 0:
        options.start_maxhealth_p2.value = options.start_maxhealth.value
    _set_coin_amounts(options)
    _set_contract_requirements(options)
    _set_filler_item_weights(options, world.player, world.player_name)
    _set_trap_item_weights(options, world.player, world.player_name)
    _set_shop_map(options)

def resolve_random_options(options: "CupheadOptions", rand: Random):
    # Resolve Random
    if options.mode.value == -1:
        # TODO: Once modes can be combined, remove this and use randint
        _mode_choices = [1, 2, 4] + ([8, 9, 16, 18] if options.use_dlc else [])
        options.mode.value = rand.choice(_mode_choices)
    _start_weapon_pool = _get_random_start_weapon_pool(options)
    if _start_weapon_pool:
        options.start_weapon.value = rand.choice(_start_weapon_pool)
    if options.boss_grade_checks.value == -1:
        options.boss_grade_checks.value = rand.randint(0, 4 if options.use_dlc else 3)
    if options.level_shuffle_seed.value == "":
        options.level_shuffle_seed.value = "".join(rand.choices("0123456789", k=16))
