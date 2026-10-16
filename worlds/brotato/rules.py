from collections.abc import Iterable

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


def create_player_can_reach_wave_rule(player: int, character: str, num_wave_cap_items_needed: int) -> CollectionRule:
    """Checks if the player can reach the given wave with the given character."""
    item_name = PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char=character)

    def can_reach_wave(state: CollectionState) -> bool:
        return state.has(item_name, player, num_wave_cap_items_needed)

    return can_reach_wave


def create_any_player_can_reach_wave_rule(
    player: int, chatacters: Iterable[str], num_wave_cap_items_needed: int
) -> CollectionRule:
    """Checks if the player can reach the given wave with any character."""
    item_counts = {PROGRESSIVE_WAVE_CAP_ITEM_TEMPLATE.format(char=c): num_wave_cap_items_needed for c in chatacters}

    def can_reach_wave(state: CollectionState) -> bool:
        return state.has_any_count(item_counts, player)

    return can_reach_wave
