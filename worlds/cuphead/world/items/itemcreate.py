### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

import math
from collections.abc import Iterable
from random import Random
from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification, Location, LocationProgressType

from ..enums import ChaliceMode, CurseMode, ItemGroups, WeaponMode
from ..locations import locationdefs as ldef
from ..names import itemnames, locationnames
from . import itemdefs as idef
from . import weapons
from .filler import get_filler_item_name
from .itembase import CupheadItem, ItemData, weighted_item_choice

if TYPE_CHECKING:
    from ... import CupheadWorld

def create_item(name: str, player: int, force_classification: ItemClassification | None = None) -> Item:
    return create_item_ext(name, player, idef.items_all, force_classification)

def create_active_item(
    world: "CupheadWorld",
    name: str,
    force_classification: ItemClassification | None = None
) -> Item:
    if name not in world.active_items:
        raise KeyError(f"Item {name} is not in active items!")
    return create_item_ext(name, world.player, world.active_items, force_classification)

def create_item_ext(
        name: str,
        player: int,
        item_defs: dict[str, ItemData],
        force_classification: ItemClassification | None = None
    ) -> Item:
    data = item_defs[name]

    if force_classification:
        classification = force_classification
    else:
        classification = data.item_type

    #print("Item: "+name+", "+str(classification))

    return CupheadItem(name, classification, data.id, player)


def create_filler_item(world: "CupheadWorld") -> Item:
    return create_active_item(world, get_filler_item_name(world))

def create_filler_items(world: "CupheadWorld", filler_count: int) -> list[Item]:
    #print(f"Filler count: {filler_count}")
    rand = world.random
    _itempool: list[Item] = []
    if filler_count > 0:
        trap_count = math.ceil(world.options.traps.value / 100 * filler_count)
        #print(f"Trap count: {trap_count}")
        if trap_count>0:
            _itempool += create_traps(world, trap_count, rand)
            filler_count -= trap_count

        #print(f"Total count so far: {len(_itempool)}")
        #print(f"Filler count: {filler_count}")
        #print(len(world.multiworld.precollected_items[world.player]))
        _itempool += [create_filler_item(world) for _ in range(filler_count)]

    #print(f"Total count: {len(_itempool)}")
    return _itempool

def create_traps(world: "CupheadWorld", trap_count: int, rand: Random) -> list[Item]:
    active_trap_weights = world.options.trap_item_weights.value

    if not active_trap_weights:
        return []

    res: list[Item] = [
        create_active_item(world, weighted_item_choice(active_trap_weights, rand))
        for _ in range(trap_count)
    ]

    return res

def create_pool_items(
    world: "CupheadWorld",
    items: list[str],
    precollected_counts: dict[str, int],
    item_qty_overrides: dict[str, int] | None = None
) -> list[Item]:
    if item_qty_overrides is None:
        item_qty_overrides = {}
    _itempool: list[Item] = []
    for itemname in items:
        if itemname in world.active_items:
            item = world.active_items[itemname]
            _item_qty = item_qty_overrides.get(itemname, item.quantity)
            # FIXME: This will break if there are multiple instances of an item.
            qty = _item_qty - precollected_counts.get(itemname, 0)
            #if qty<0:
            #    print(f"WARNING: \"{items}\" has quantity of {str(qty)}!")
            if item.id and qty>0:
                _itempool += [create_active_item(world, itemname, item.item_type) for _ in range(qty)]
    return _itempool

def place_locked_item(world: "CupheadWorld", item: Item, location: str):
    world.multiworld.get_location(location, world.player) \
        .place_locked_item(item)
def create_locked_item(
        world: "CupheadWorld",
        name: str,
        location: str,
        force_classification: ItemClassification | None = None
    ):
    #print(f"Create locked item: '{name}' at '{location}'")
    place_locked_item(world, create_active_item(world, name, force_classification), location)
def create_locked_items_at(
        world: "CupheadWorld",
        name: str,
        locations: Iterable[str],
        force_classification: ItemClassification | None = None
    ):
    for loc in locations:
        if loc in world.active_locations.keys():
            create_locked_item(world, name, loc, force_classification)
        elif world.settings.is_debug_bit_on(1):
            print(f"Skipped {name} for {loc}")

def create_dlc_locked_items(world: "CupheadWorld"):
    if world.options.dlc_requires_mausoleum.bvalue:
        create_locked_item(world, itemnames.item_event_mausoleum, locationnames.loc_event_mausoleum)
    if world.options.dlc_chalice.evalue == ChaliceMode.VANILLA:
        create_locked_item(world, itemnames.item_charm_dlc_cookie, locationnames.loc_event_dlc_cookie)
    if locationnames.loc_event_dlc_goal_saltbaker in world.active_locations:
        if not world.options.is_goal_used(locationnames.loc_event_dlc_goal_saltbaker):
            raise ValueError("Saltbaker Goal location created even if it shouldn't")
        create_locked_item(world, itemnames.item_event_goal_dlc_saltbakerko, locationnames.loc_event_dlc_goal_saltbaker)
    create_locked_items_at(world, itemnames.item_event_dlc_boss_chaliced, ldef.locations_dlc_event_boss_chaliced)
    create_locked_items_at(
        world,
        itemnames.item_event_dlc_boss_chaliced,
        ldef.locations_dlc_event_boss_final_chaliced
    )

def create_locked_items(world: "CupheadWorld"):
    # Locked Items
    for i in range(1,6):
        _loc = getattr(locationnames, f"loc_event_isle1_secret_prereq{i}")
        create_locked_item(world, itemnames.item_event_isle1_secret_prereq, _loc)
    if world.options.ginger_quest.bvalue:
        create_locked_item(world, itemnames.item_event_isle2_shortcut, locationnames.loc_event_isle2_shortcut)
    if world.options.fourmel_quest.bvalue:
        create_locked_item(world, itemnames.item_event_quest_4mel_4th, locationnames.loc_event_quest_4mel_4th)
    if world.options.music_quest.bvalue:
        create_locked_item(world, itemnames.item_event_ludwig, locationnames.loc_event_quest_ludwig)
        #create_locked_item(world, itemnames.item_event_wolfgang, locationnames.loc_event_quest_wolfgang)
    if world.options.silverworth_quest.bvalue:
        create_locked_items_at(world, itemnames.item_event_agrade, ldef.locations_event_agrade)
        create_locked_items_at(world, itemnames.item_event_agrade, ldef.location_level_boss_final_event_agrade)
    if world.options.pacifist_quest.bvalue:
        create_locked_items_at(world, itemnames.item_event_pacifist, ldef.location_level_rungun_event_pacifist)
    if locationnames.loc_event_goal_devil in world.active_locations:
        if not world.options.is_goal_used(locationnames.loc_event_goal_devil):
            raise KeyError("Devil Goal location created even if it shouldn't")
        create_locked_item(world, itemnames.item_event_goal_devilko, locationnames.loc_event_goal_devil)

    if world.use_dlc:
        create_dlc_locked_items(world)

def create_special_items(world: "CupheadWorld", precollected_counts: dict[str, int]) -> list[Item]:
    options = world.options
    items: list[Item] = []

    [
        items.append(create_active_item(world, itemnames.item_healthupgrade))
        for _ in range(options.maxhealth_upgrades.value)
    ]
    if world.use_dlc:
        if (
            options.dlc_chalice.evalue == ChaliceMode.RANDOMIZED and
            itemnames.item_charm_dlc_cookie not in precollected_counts
        ):
            items.append(create_active_item(world, itemnames.item_charm_dlc_cookie))
        if ((
                options.dlc_curse_mode.evalue == CurseMode.VANILLA or
                options.dlc_curse_mode.evalue == CurseMode.REVERSE
            ) and itemnames.item_charm_dlc_broken_relic not in precollected_counts
        ):
                items.append(create_active_item(world, itemnames.item_charm_dlc_broken_relic))

    return items

def compress_coins(coin_amounts: tuple[int, int, int], location_count: int) -> tuple[int, int, int]:
    total_single_coins, total_double_coins, total_triple_coins = coin_amounts
    def _total_coins():
        return total_single_coins + total_double_coins + total_triple_coins
    while _total_coins() >= location_count:
        if total_single_coins >= 2 and _total_coins():
            total_single_coins -= 2
            total_double_coins += 1
        elif total_single_coins >= 3:
            total_single_coins -= 3
            total_triple_coins += 1
        elif total_double_coins >= 1 and total_single_coins >= 1:
            total_single_coins -= 1
            total_double_coins -= 1
            total_triple_coins += 1
        elif total_double_coins >= 3:
            total_double_coins -= 3
            total_triple_coins += 2
        elif total_single_coins >= 2:
            total_single_coins -= 2
            total_double_coins += 1
        else:
            print("Error: Cannot resolve coins!")
            break
    return (total_single_coins, total_double_coins, total_triple_coins)

def create_start_weapons(world: "CupheadWorld", weapon: str) -> list[str]:
    options = world.options
    res: list[str] = []

    create_locked_item(world, weapon, locationnames.loc_event_start_weapon, ItemClassification.progression)
    res.append(weapon)
    if locationnames.loc_event_start_weapon_ex in world.active_locations:
        if options.weapon_mode.evalue == WeaponMode.PROGRESSIVE_EXCEPT_START:
            weapon_ex = weapons.weapon_p_dict[options.start_weapon.value]
        elif options.weapon_mode.evalue == WeaponMode.EX_SEPARATE_EXCEPT_START:
            weapon_ex = weapons.weapon_ex_dict[options.start_weapon.value]
        else:
            weapon_ex = ""
        create_locked_item(world, weapon_ex, locationnames.loc_event_start_weapon_ex, ItemClassification.progression)
        res.append(weapon_ex)
    return res

## Returns a tuple with the list of weapon items and a dict representing their counts
def setup_weapon_pool(world: "CupheadWorld") -> tuple[list[str], dict[str, int]]:
    _weapons: list[str] = []
    _weapon_dict = weapons.get_weapon_dict(world.options)

    _weapon_counts: dict[str, int] = {}

    def _push_weapon_counts(w: str, v: int = 1):
        _weapon_counts[w] = _weapon_counts.get(w, 0) + v

    _start_weapon_index = world.options.start_weapon.value
    if _start_weapon_index in _weapon_dict:
        _weapon = _weapon_dict[world.options.start_weapon.value]
        _start_weapons = create_start_weapons(world, _weapon)
        for w in _start_weapons:
            _push_weapon_counts(w, -1)
    elif not world.options.start_weapon.is_none():
        raise ValueError(f"weapon {_start_weapon_index} is invalid")

    _weapons = list(_weapon_dict.values())

    _weapon_qty = 2 if (world.options.weapon_mode.evalue & WeaponMode.PROGRESSIVE) > 0 else 1

    if (world.options.weapon_mode.evalue & WeaponMode.EX_SEPARATE) > 0:
        _weapons.extend(idef.item_weapon_ex.keys())
        if world.use_dlc:
            _weapons.extend(idef.item_dlc_weapon_ex.keys())

    for w in _weapons:
        _push_weapon_counts(w, _weapon_qty if weapons.all_weapon_to_index[w] in _weapon_dict else 1)

    return (_weapons, _weapon_counts)

def setup_ability_pool(world: "CupheadWorld", precollected_counts: dict[str, int]) -> list[str]:
    abilities = list(idef.item_abilities.keys())
    # FIXME: Is this needed? If they are not active, they won't be added anyways
    if world.options.dlc_chalice_items_separate.fvalue & ItemGroups.ABILITIES:
        abilities.extend(idef.item_dlc_chalice_abilities.keys())
    else:
        abilities.append(itemnames.item_ability_dlc_cdoublejump)
    return [a for a in abilities if a not in precollected_counts]

def create_coins(
        world: "CupheadWorld",
        location_count: int,
        precollected_counts: dict[str, int],
        coin_items: tuple[str, str, str]
    ) -> list[Item]:
    res: list[Item] = []
    # Coins
    # TODO: Start inventory from pool vs start inventory. Allow for extra coins depending on shop.
    coin_amounts = world.options.coin_amounts.value
    total_single_coins = coin_amounts[0]
    total_double_coins = coin_amounts[1]
    total_triple_coins = coin_amounts[2]
    total_coins = world.total_coins

    # Starter Coins
    start_coins = precollected_counts.get(coin_items[0], 0)
    start_coins += precollected_counts.get(coin_items[1], 0) * 2
    start_coins += precollected_counts.get(coin_items[2], 0) * 3

    total_coins -= start_coins

    start_3coins = min(start_coins // 3, total_triple_coins)
    start_coins -= start_3coins * 3
    start_2coins = min(start_coins // 2, total_double_coins)
    start_coins -= start_2coins * 2

    total_triple_coins = max(total_triple_coins - start_3coins, 0)
    total_double_coins = max(total_double_coins - start_2coins, 0)
    total_single_coins = max(total_single_coins - start_coins, 0)

    total_coins = compress_coins((total_single_coins, total_double_coins, total_triple_coins), location_count)

    res += [create_active_item(world, coin_items[0]) for _ in range(total_coins[0])]
    res += [create_active_item(world, coin_items[1]) for _ in range(total_coins[1])]
    res += [create_active_item(world, coin_items[2]) for _ in range(total_coins[2])]

    return res

def create_items(world: "CupheadWorld"):
    itempool: list[Item] = []

    create_locked_items(world)

    # Setup Weapons including start weapons
    weapons, weapon_counts = setup_weapon_pool(world)

    #total_locations = len([x.name for x in world.multiworld.get_locations(world.player) if not x.is_event])
    #unfilled_locations = list(world.multiworld.get_unfilled_locations(world.player))
    #unfilled_location_count = len(unfilled_locations)
    #print(total_locations)
    #print(unfilled_locations)
    # This can fail if someone uses plando
    # if total_locations != unfilled_locations:
    #     print("ERROR: unfilled locations mismatch total non-event locations")

    #print(weapons)

    # Item names for coins
    coin_items = (itemnames.item_coin, itemnames.item_coin2, itemnames.item_coin3)

    essential_items = (
        [y for y in idef.item_essential.keys() if y not in coin_items] + \
            (list(idef.item_dlc_essential.keys()) if world.use_dlc else [])
    )
    charms = list(idef.item_charms.keys()) + (list(idef.item_dlc_charms.keys()) if world.use_dlc else [])
    supers = list(idef.item_super.keys())

    if world.use_dlc and world.options.dlc_chalice_items_separate.value:
        essential_items += list(idef.item_dlc_chalice_essential.keys())
        #supers += list(items.item_dlc_chalice_super) # TODO: Investigate adding this later

    # Add the grouped fill items
    itempool += create_pool_items(world, essential_items, world.precollected_counts)
    itempool += create_pool_items(world, weapons, world.precollected_counts, weapon_counts)
    itempool += create_pool_items(world, charms, world.precollected_counts)
    itempool += create_pool_items(world, supers, world.precollected_counts)
    if world.options.randomize_abilities.bvalue:
        abilities = setup_ability_pool(world, world.precollected_counts)
        itempool += create_pool_items(world, abilities, world.precollected_counts)

    # Add special Items
    itempool += create_special_items(world, world.precollected_counts)

    minimum_filler = world.options.minimum_filler.value

    def _exclude_location(loc: Location) -> bool:
        if loc.progress_type == LocationProgressType.EXCLUDED:
            place_locked_item(world, create_filler_item(world), loc.name)
            return False
        return True
    unfilled_locations = [
        x for x in world.multiworld.get_unfilled_locations(world.player)
        if _exclude_location(x)
    ]

    unfilled_location_count = len(unfilled_locations)

    # Add Coins
    leftover_locations = unfilled_location_count - len(itempool) - minimum_filler

    itempool += create_coins(world, leftover_locations, world.precollected_counts, coin_items)

    leftover_locations = unfilled_location_count - len(itempool)
    if (leftover_locations<0):
        print("Error: There are more items than locations!")

    # Filler Items and Traps
    filler_count = leftover_locations
    if filler_count>0:
        itempool += create_filler_items(world, filler_count)

    #print("itempool size: "+str(len(itempool)))
    world.multiworld.itempool += itempool
