### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from typing import TYPE_CHECKING

from rule_builder import rules as rule
from worlds.generic.Rules import forbid_item

from ..enums import GameMode, ItemGroups
from ..locations import locationdefs as ld
from ..names import itemnames, locationnames, regionnames
from . import levelrules
from . import rulebase as rb
from .rb import rbrules
from .rulereg import SpotType

if TYPE_CHECKING:
    from ... import CupheadWorld

def register_rules(world: "CupheadWorld"):
    w = world
    rr = w.rulereg
    options = w.options
    use_dlc = w.use_dlc

    rr.add_region_rule(
        regionnames.world_inkwell_2,
        rule.Has(itemnames.item_contract, options.contract_requirements_isle2.value)
    )
    rr.add_region_rule(
        regionnames.world_inkwell_3,
        rule.Has(itemnames.item_contract, options.contract_requirements_isle3.value)
    )

    set_shop_rules(w)

    set_level_rules(w)

    rr.add_item_rule(locationnames.loc_coin_isle1_secret, itemnames.item_event_isle1_secret_prereq, 5)

    set_quest_rules(w)

    if use_dlc:
        set_dlc_rules(w)

def set_rules(world: "CupheadWorld"):
    register_rules(world)

    world.rulereg.apply_rules()

    set_goal(world)

def set_dlc_rules(world: "CupheadWorld"):
    w = world
    rr = w.rulereg
    options = w.options
    ingredient_reqs = options.dlc_ingredient_requirements.value
    set_dlc_boat_rules(w)
    rr.add_region_rule(
        regionnames.level_dlc_boss_saltbaker,
        rule.Has(itemnames.item_dlc_ingredient, ingredient_reqs)
    )

def set_dlc_boat_rules(world: "CupheadWorld"):
    w = world
    rr = w.rulereg
    options = w.options
    randomize_boat = options.dlc_randomize_boat.bvalue
    require_mausoleum = options.dlc_requires_mausoleum.bvalue
    if require_mausoleum:
        rr.add_region_rule(regionnames.reg_dlc_boat, rule.Has(itemnames.item_event_mausoleum))
    if randomize_boat:
        rr.add_region_rule(regionnames.reg_dlc_boat, rule.Has(itemnames.item_dlc_boat))

def set_quest_rules(world: "CupheadWorld"):
    w = world
    rr = w.rulereg
    options = w.options
    if options.fourmel_quest.bvalue:
        rr.add_item_rule(locationnames.loc_quest_4mel, itemnames.item_event_quest_4mel_4th)
    if options.ginger_quest.bvalue:
        rr.add_item_rule(locationnames.loc_quest_ginger, itemnames.item_event_isle2_shortcut)
    if options.buster_quest.bvalue and options.randomize_abilities.bvalue:
        rr.add_item_rule(locationnames.loc_quest_buster, itemnames.item_ability_parry)
        if options.is_dlc_chalice_items_separate(ItemGroups.ABILITIES):
            rr.add_loc_rule(locationnames.loc_quest_buster, rule.HasAll(
                itemnames.item_ability_dlc_cdash,
                itemnames.item_ability_dlc_cparry,
            ), False)
    if options.silverworth_quest.bvalue:
        rr.add_item_rule(locationnames.loc_quest_silverworth, itemnames.item_event_agrade, 15)
    if options.pacifist_quest.bvalue:
        rr.add_item_rule(locationnames.loc_quest_pacifist, itemnames.item_event_pacifist, 6)
    if options.music_quest.bvalue:
        rr.add_item_rule(locationnames.loc_quest_music, itemnames.item_event_ludwig)

def set_level_rules(world: "CupheadWorld"):
    w = world
    rr = w.rulereg
    levelrules.set_levelrules(w)
    level_loc_rule_map: dict[str, str] = {
        locationnames.loc_event_isle1_secret_prereq1: regionnames.level_boss_veggies,
        locationnames.loc_event_isle1_secret_prereq2: regionnames.level_boss_slime,
        locationnames.loc_event_isle1_secret_prereq3: regionnames.level_boss_plane_blimp,
        locationnames.loc_event_isle1_secret_prereq4: regionnames.level_boss_frogs,
        locationnames.loc_event_isle1_secret_prereq5: regionnames.level_boss_flower
    }
    for llrl, llrr in level_loc_rule_map.items():
        locs = rb.get_region(world, llrr).get_locations()
        loc = locs[0].name
        if not loc.endswith("Complete"):
            raise ValueError(f"{loc} is not the correct 'Complete' location for region {llrr}")
        if rr.contains(loc, SpotType.LOCATION):
            rr.copy_rule(loc, SpotType.LOCATION, llrl, SpotType.LOCATION)

def set_shop_rules(world: "CupheadWorld"):
    w = world
    player = w.player
    use_dlc = w.use_dlc
    total_coins = w.total_coins
    shop_map = w.shop.shop_map

    shop_items = {**ld.location_shop, **(ld.location_shop_dlc if use_dlc else {})}
    coins = (itemnames.item_coin, itemnames.item_coin2, itemnames.item_coin3)

    # Prevent certain items from appearing in the shop
    for shop_item in shop_items.keys():
        _loc = rb.get_location(w, shop_item)
        # Prevent putting money in the shop
        [forbid_item(_loc, x, player) for x in coins]

    # Set coin requirements for the shops
    shop_costs: list[int] = [0, 0, 0, 0]

    for i in range(len(shop_map)):
        shop_costs[i] = (shop_map[i][0]*4) + (shop_map[i][1]*3)

    total_cost = shop_costs[0] + shop_costs[1] + shop_costs[2] + (shop_costs[3] if use_dlc else 0)

    if total_cost > total_coins:
        raise Exception(f"Error: Total cost is {total_cost}, but there are {total_coins} coins!")

    for i in range(4 if use_dlc else 3):
        set_shop_cost_rule(w, i, shop_costs)

def set_shop_cost_rule(world: "CupheadWorld", shop_index: int, shop_costs: list[int]):
    rr = world.rulereg
    cost = 0
    for i in range(shop_index+1):
        cost += shop_costs[i]
    region = rb.get_region(world, regionnames.shop_sets[shop_index])
    rr.add_region_rule(region.name, rule.Has(itemnames.item_coin, cost))

def set_goal(world: "CupheadWorld"):
    w = world
    options = w.options
    w.set_completion_rule(
        (
            rule.Has(itemnames.item_contract, options.contract_goal_requirements.value)
        ) if options.mode.evalue == GameMode.COLLECT_CONTRACTS else (
            rbrules.CanBuyOutShop()
        ) if options.mode.evalue == GameMode.BUY_OUT_SHOP else (
            rule.Has(itemnames.item_event_goal_dlc_saltbakerko)
        ) if (
            options.mode.evalue == GameMode.DLC_BEAT_SALTBAKER or
            options.mode.evalue == GameMode.DLC_BEAT_SALTBAKER_ISLE4_ONLY
        ) else (
            rule.HasAll(itemnames.item_event_goal_devilko, itemnames.item_event_goal_dlc_saltbakerko)
        ) if options.mode.evalue == GameMode.DLC_BEAT_BOTH else (
            rule.Has(itemnames.item_dlc_ingredient, options.dlc_ingredient_goal_requirements.value)
        ) if options.mode.evalue == GameMode.DLC_COLLECT_INGREDIENTS else (
            rule.HasAllCounts({
                itemnames.item_contract: options.contract_goal_requirements.value,
                itemnames.item_dlc_ingredient: options.dlc_ingredient_goal_requirements.value
            })
        ) if options.mode.evalue == GameMode.DLC_COLLECT_BOTH else (
            rule.Has(itemnames.item_event_goal_devilko)
        )
    )
