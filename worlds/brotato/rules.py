from BaseClasses import CollectionState
from worlds.generic.Rules import CollectionRule

from .constants import PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE
from .items import ItemName


def create_has_run_wins_rule(player: int, count: int) -> CollectionRule:
    def has_wins(state: CollectionState) -> bool:
        return state.has(ItemName.RUN_COMPLETE.value, player, count)

    return has_wins


def create_has_character_rule(player: int, character: str) -> CollectionRule:
    def char_region_access_rule(state: CollectionState) -> bool:
        return state.has(character, player)

    return char_region_access_rule


def create_can_reach_wave_rule(player: int, character: str, num_wave_cap_items_needed: int) -> CollectionRule:
    item_name = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char=character)

    def can_reach_wave(state: CollectionState) -> bool:
        return state.has(item_name, player, num_wave_cap_items_needed)

    return can_reach_wave
