from __future__ import annotations
import typing
from collections.abc import Iterable
from BaseClasses import Location, Region, Entrance
from worlds.generic.Rules import set_rule, add_rule, forbid_item, forbid_items_for_player
from . import rulebase as rb
from .rulebase import Rule
from ..levels import levelrules as lr, levellocrules as llrules, levellocruledefs as llrdefs
from ..items import itemdefs as idef
from ..locations import locationsets, locationdefs as ld
from ..names import ItemNames, LocationNames
from ..enums import GameMode, ItemGroups
if typing.TYPE_CHECKING:
    from .. import CupheadWorld

def get_entrance(world: CupheadWorld, exit: str, entrance: str) -> Entrance:
    return world.multiworld.get_entrance(exit+" -> "+entrance, world.player)
def get_location(world: CupheadWorld, location: str) -> Location:
    return world.multiworld.get_location(location, world.player)
def get_region(world: CupheadWorld, region: str) -> Region:
    return world.multiworld.get_region(region, world.player)
def set_item_rule(world: CupheadWorld, loc: str, item: str, count: int = 1) -> None:
    set_loc_rule(world, loc, rb.rule_has(world, item, count))
def add_item_rule(world: CupheadWorld, loc: str, item: str, count: int = 1, combine_and: bool = True) -> None:
    add_loc_rule(world, loc, rb.rule_has(world, item, count), combine_and)
def set_loc_rule(world: CupheadWorld, loc: str, rule: Rule) -> None:
    set_rule(get_location(world, loc), rule)
def add_loc_rule(world: CupheadWorld, loc: str, rule: Rule, combine_and: bool = True) -> None:
    add_rule(get_location(world, loc), rule, "and" if combine_and else "or")
def set_region_rules(world: CupheadWorld, region_name: str, rule: Rule):
    region = get_region(world, region_name)
    for entrance in region.entrances:
        set_rule(entrance, rule)
def add_region_rules(world: CupheadWorld, region_name: str, rule: Rule, combine_and: bool = True):
    region = get_region(world, region_name)
    for entrance in region.entrances:
        add_rule(entrance, rule, "and" if combine_and else "or")

def set_rules(world: CupheadWorld):
    w = world
    wconfig = w.wconfig
    use_dlc = w.use_dlc
    contract_reqs = wconfig.contract_requirements

    set_region_rules(w, LocationNames.world_inkwell_2, rb.rule_has(w, ItemNames.item_contract, contract_reqs[0]))
    set_region_rules(w, LocationNames.world_inkwell_3, rb.rule_has(w, ItemNames.item_contract, contract_reqs[1]))
    set_region_rules(w, LocationNames.level_boss_kingdice,
                     rb.rule_and(
                         rb.rule_has(w, ItemNames.item_contract, contract_reqs[2]),
                         rb.rrule_to_rule(lr.lrule_kingdice(wconfig), w.player)
                     ))
    set_shop_rules(w)

    set_level_rules(w)

    set_item_rule(w, LocationNames.loc_coin_isle1_secret, ItemNames.item_event_isle1_secret_prereq, 5)

    set_quest_rules(w)

    if use_dlc:
        set_dlc_rules(w)

    set_goal(w)

def add_level_chalice_rule(world: CupheadWorld, loc: str):
    w = world
    if loc in locationsets.s_plane_locations:
        add_loc_rule(
            w,
            loc,
            rb.rrule_to_rule(lr.lrule_dlc_boss_plane_chaliced(w.wconfig), w.player)
        )
    else:
        add_loc_rule(
            w,
            loc,
            rb.rrule_to_rule(lr.lrule_dlc_boss_chaliced(w.wconfig), w.player)
        )

def add_level_chalice_rules(world: CupheadWorld, locs: Iterable[str], exclude: set[str] | None = None):
    if not exclude:
        exclude = set()
    for loc in locs:
        if (loc not in exclude and loc not in llrules.level_loc_rule_locs):
            add_level_chalice_rule(world, loc)

def set_dlc_rules(world: CupheadWorld):
    w = world
    wconfig = w.wconfig
    ingredient_reqs = wconfig.dlc_ingredient_requirements
    set_dlc_boat_rules(w)
    set_region_rules(
        w,
        LocationNames.level_dlc_boss_saltbaker,
        rb.rule_has(w, ItemNames.item_dlc_ingredient, ingredient_reqs)
    )
    if wconfig.dlc_boss_chalice_checks:
        add_level_chalice_rules(w, ld.locations_dlc_boss_chaliced.keys())
    if wconfig.dlc_cactusgirl_quest:
        add_level_chalice_rules(w, ld.locations_dlc_event_boss_chaliced.keys())
        num_chaliced_events = len(ld.locations_dlc_event_boss_chaliced.keys())
        set_loc_rule(
            w,
            LocationNames.loc_dlc_quest_cactusgirl,
            rb.rule_has(w, ItemNames.item_event_dlc_boss_chaliced, num_chaliced_events)
        )

def set_dlc_boat_rules(world: CupheadWorld):
    w = world
    wconfig = w.wconfig
    randomize_boat = wconfig.dlc_randomize_boat
    require_mausoleum = wconfig.dlc_requires_mausoleum
    if require_mausoleum:
        add_region_rules(w, LocationNames.reg_dlc_boat, rb.rule_has(w, ItemNames.item_event_mausoleum))
    if randomize_boat:
        add_region_rules(w, LocationNames.reg_dlc_boat, rb.rule_has(w, ItemNames.item_dlc_boat))

def set_quest_rules(world: CupheadWorld):
    w = world
    wconfig = w.wconfig
    if wconfig.fourmel_quest:
        set_item_rule(w, LocationNames.loc_quest_4mel, ItemNames.item_event_quest_4mel_4th)
    if wconfig.ginger_quest:
        set_item_rule(w, LocationNames.loc_quest_ginger, ItemNames.item_event_isle2_shortcut)
    if wconfig.buster_quest and wconfig.randomize_abilities:
        set_item_rule(w, LocationNames.loc_quest_buster, ItemNames.item_ability_parry)
        if wconfig.is_dlc_chalice_items_separate(ItemGroups.ABILITIES):
            add_loc_rule(w, LocationNames.loc_quest_buster, rb.rule_has_all(w, {
                ItemNames.item_ability_dlc_cdash,
                ItemNames.item_ability_dlc_cparry,
            }), False)
    if wconfig.silverworth_quest:
        set_item_rule(w, LocationNames.loc_quest_silverworth, ItemNames.item_event_agrade, 15)
    if wconfig.pacifist_quest:
        set_item_rule(w, LocationNames.loc_quest_pacifist, ItemNames.item_event_pacifist, 6)
    if wconfig.music_quest:
        set_item_rule(w, LocationNames.loc_quest_music, ItemNames.item_event_ludwig)

def add_level_grade_rule(world: CupheadWorld, loc: str):
    w = world
    if loc in locationsets.s_plane_locations:
        add_loc_rule(
            w,
            loc,
            rb.rrule_to_rule(lr.lrule_plane_topgrade(w.wconfig), w.player)
        )
    else:
        add_loc_rule(
            w,
            loc,
            rb.rrule_to_rule(lr.lrule_topgrade(w.wconfig), w.player)
        )

def add_level_grade_rules(world: CupheadWorld, locs: Iterable[str], exclude: set[str] | None = None):
    if not exclude:
        exclude = set()
    for loc in locs:
        if (loc not in exclude and loc not in llrules.level_loc_rule_locs):
            add_level_grade_rule(world, loc)

def set_level_loc_rules(world: CupheadWorld):
    w = world
    loc_rules = llrdefs.level_loc_rules
    for _loc_rule in loc_rules:
        for loc, rule in _loc_rule.loc_rules.items():
            if loc in w.active_locations:
                set_loc_rule(w, loc, rb.rrule_to_rule(rule(w.wconfig), w.player))
            elif world.settings.is_debug_bit_on(1):
                print(f"[set_level_loc_rules] Skipping {loc}")

def set_level_boss_grade_rules(world: CupheadWorld):
    wconfig = world.wconfig
    boss_grade_checks = wconfig.boss_grade_checks
    if boss_grade_checks > 0:
        add_level_grade_rules(
            world,
            ld.location_level_boss_topgrade
        )
        if wconfig.mode != GameMode.BEAT_DEVIL:
            add_level_grade_rules(
                world,
                ld.location_level_boss_final_topgrade
            )
        if wconfig.silverworth_quest:
            add_level_grade_rules(
                world,
                ld.location_level_boss_event_agrade
            )
            if wconfig.mode != GameMode.BEAT_DEVIL:
                add_level_grade_rules(
                    world,
                    ld.location_level_boss_final_event_agrade
                )
        if wconfig.use_dlc:
            add_level_grade_rules(
                world,
                ld.location_level_dlc_boss_topgrade
            )
            if wconfig.mode != GameMode.DLC_BEAT_SALTBAKER:
                add_level_grade_rules(
                    world,
                    ld.location_level_dlc_boss_final_topgrade
                )

def set_level_rules(world: CupheadWorld):
    w = world
    set_level_loc_rules(w)
    if w.wconfig.randomize_abilities:
        set_level_boss_grade_rules(w)

def set_shop_rules(world: CupheadWorld):
    w = world
    player = w.player
    use_dlc = w.use_dlc
    total_coins = w.total_coins
    shop_map = w.shop.shop_map

    shop_items = {**ld.location_shop, **(ld.location_shop_dlc if use_dlc else {})}
    coins = (ItemNames.item_coin, ItemNames.item_coin2, ItemNames.item_coin3)

    # Prevent certain items from appearing in the shop
    for shop_item in shop_items.keys():
        _loc = get_location(w, shop_item)
        # Prevent putting money in the shop
        [forbid_item(_loc, x, player) for x in coins]
        # Prevent putting local filler items in the shop
        forbid_items_for_player(_loc, {x for x in idef.item_filler.keys()}, player)

    # Set coin requirements for the shops
    shop_costs: list[int] = [0, 0, 0, 0]

    for i in range(len(shop_map)):
        shop_costs[i] = (shop_map[i][0]*4) + (shop_map[i][1]*3)

    total_cost = shop_costs[0] + shop_costs[1] + shop_costs[2] + (shop_costs[3] if use_dlc else 0)

    if total_cost > total_coins:
        raise Exception(f"Error: Total cost is {total_cost}, but there are {total_coins} coins!")

    for i in range(4 if use_dlc else 3):
        set_shop_cost_rule(w, i, shop_costs)

def set_shop_cost_rule(world: CupheadWorld, shop_index: int, shop_costs: list[int]):
    player = world.player
    cost = 0
    for i in range(shop_index+1):
        cost += shop_costs[i]
    region = get_region(world, LocationNames.shop_sets[shop_index])
    for entrance in region.entrances:
        set_rule(entrance, lambda state: state.has(ItemNames.item_coin, player, cost))

def set_goal(world: CupheadWorld):
    w = world
    wconfig = w.wconfig
    w.multiworld.completion_condition[w.player] = (
        rb.rule_has(w, ItemNames.item_contract, wconfig.contract_goal_requirements)
    ) if wconfig.mode == GameMode.COLLECT_CONTRACTS else (
        rb.rule_can_reach_all_regions(
            w, LocationNames.shop_sets if wconfig.use_dlc else LocationNames.base_shop_sets
        )
    ) if wconfig.mode == GameMode.BUY_OUT_SHOP else (
        rb.rule_has(w, ItemNames.item_event_goal_dlc_saltbakerko)
    ) if wconfig.mode == GameMode.DLC_BEAT_SALTBAKER or wconfig.mode == GameMode.DLC_BEAT_SALTBAKER_ISLE4_ONLY else (
        rb.rule_has_all(w, {ItemNames.item_event_goal_devilko, ItemNames.item_event_goal_dlc_saltbakerko})
    ) if wconfig.mode == GameMode.DLC_BEAT_BOTH else (
        rb.rule_has(w, ItemNames.item_dlc_ingredient, wconfig.dlc_ingredient_goal_requirements)
    ) if wconfig.mode == GameMode.DLC_COLLECT_INGREDIENTS else (
        rb.rule_and(
            rb.rule_has(w, ItemNames.item_contract, wconfig.contract_goal_requirements),
            rb.rule_has(w, ItemNames.item_dlc_ingredient, wconfig.dlc_ingredient_goal_requirements)
        )
    ) if wconfig.mode == GameMode.DLC_COLLECT_BOTH else (
        rb.rule_has(w, ItemNames.item_event_goal_devilko)
    )
