import math
import string

from BaseClasses import MultiWorld, CollectionState, ItemClassification, LocationProgressType
from worlds.generic.Rules import add_rule
from .options import LCOptions
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import LethalCompanyWorld


def has_location_access_rule(multiworld: MultiWorld, moon: str, player: int, item_number: int,
                             options: LCOptions) -> None:
    if item_number == 1:
        multiworld.get_location(f"{moon} check {item_number}", player).access_rule = \
            lambda state: ((state.has("Inventory Slot", player) or options.starting_inventory_slots.value >= 2) and
                           (state.has("Stamina Bar", player) or options.starting_stamina_bars.value >= 1))
    else:
        multiworld.get_location(f"{moon} check {item_number}", player).access_rule = \
            lambda state: check_location(moon=moon, player=player, state=state, item_number=item_number)


def has_quota_access_rule(multiworld: MultiWorld, player: int, item_number: int, options: LCOptions) -> None:
    if item_number == 1:
        return
    checkpoint_every = options.quota_checkpoint_every.value
    num_quotas = options.num_quotas.value
    if item_number % checkpoint_every == 0:

        if item_number < num_quotas:
            multiworld.get_location(f"Quota check {item_number}", player).access_rule = \
                lambda state, ci=item_number // checkpoint_every, n=item_number: check_quota(
                    player=player, state=state, item_number=n
                ) and state.has(f"Completed quota checkpoint {ci}", player)
            return
    multiworld.get_location(f"Quota check {item_number}", player).access_rule = \
        lambda state, n=item_number: check_quota(player=player, state=state, item_number=n)


def check_location(state, moon: str, player: int, item_number: int) -> None:
    return state.can_reach(f"{moon} check {item_number - 1}", "Location", player)


def check_quota(state, player: int, item_number: int) -> None:
    return state.can_reach(f"Quota check {item_number - 1}", "Location", player)


def set_rules(lc_world: 'LethalCompanyWorld') -> None:
    player = lc_world.player
    multiworld = lc_world.multiworld
    options: LCOptions = lc_world.options
    for moon in lc_world.slot_item_data.moons:
        for i in range(options.checks_per_moon.value):
            has_location_access_rule(multiworld, moon, player, i + 1, options)
    
    for i in range(options.num_quotas.value):
        has_quota_access_rule(multiworld, player, i + 1, options)

    checkpoint_every = options.quota_checkpoint_every.value
    num_quotas = options.num_quotas.value
    checkpoint_index = 2
    while checkpoint_index * checkpoint_every < num_quotas:
        ci = checkpoint_index
        multiworld.get_location(f"Quota checkpoint {ci}", player).access_rule = \
            lambda state, prev=ci - 1: state.has(f"Completed quota checkpoint {prev}", player)
        checkpoint_index += 1

    add_rule(multiworld.get_location("Bestiary Entry - Kidnapper fox", player), lambda state: can_buy(state, player, options))
    add_rule(multiworld.get_location("Bestiary Entry - Vain shroud", player), lambda state: can_buy(state, player, options))

    if options.scrapsanity.value == 1:
        for scrap_index in range(len(lc_world.scrap_names)):
            if lc_world.scrap_names[scrap_index] == "Hive" and options.exclude_hive.value == 1:
                multiworld.get_location("Scrap - Hive", player).progress_type = LocationProgressType.EXCLUDED

            if lc_world.scrap_names[scrap_index] == "Sapsucker Egg" and options.exclude_egg.value == 1:
                multiworld.get_location("Scrap - Sapsucker Egg", player).progress_type = LocationProgressType.EXCLUDED

            if lc_world.scrap_names[scrap_index] == "Shotgun" and options.exclude_killing.value == 1:
                multiworld.get_location("Scrap - Shotgun", player).progress_type = LocationProgressType.EXCLUDED

            if lc_world.scrap_names[scrap_index] == "Kitchen knife" and options.exclude_killing.value == 1:
                multiworld.get_location("Scrap - Kitchen knife", player).progress_type = LocationProgressType.EXCLUDED

            if lc_world.scrap_names[scrap_index] == "Gold bar":
                multiworld.get_location("Scrap - Gold bar", player).progress_type = LocationProgressType.EXCLUDED

    multiworld.completion_condition[player] = lambda state: state.has("Victory", player)


def has_multi(state: CollectionState, items, player):
    success = False
    for item in items:
        success = success or state.has(item, player)
    return success


def has_multi_moon(state: CollectionState, items, player, options, world):
    success = False
    for item in items:
        success = success or check_moon_accessible(state, item, player, options, world)
    return success


def has_all(state, items, player):
    success = True
    for item in items:
        success = success and state.has(item, player)
    return success


def check_item_accessible(state: CollectionState, item: string, player: int, options: LCOptions):
    return (state.has(item, player) and (state.has("Terminal", player) or options.randomize_terminal.value == 0)
            and (state.has("Company Building", player) or options.randomize_company_building.value == 0))

def can_buy(state: CollectionState, player: int, options: LCOptions):
    return ((state.has("Terminal", player) or options.randomize_terminal.value == 0) 
            and (state.has("Company Building", player) or options.randomize_company_building.value == 0))

def check_moon_accessible(state: CollectionState, moon: string, player: int,
                          options: LCOptions, world):
    return state.has(moon, player) and (state.has("Terminal", player) or
                                        (options.randomize_terminal.value == 0 or world.initial_world == moon))
