"""This module handles creation of item hints for Merluvlee to offer Mario."""
from .options import ShuffleKootFavors, ShuffleLetters, PaperMarioOptions

from .data.itemlocation_special import (
    kootfavors_reward_locations,
    kootfavors_keyitem_locations,
    chainletter_giver_locations,
    chainletter_final_reward_location,
    simpleletter_locations,
    limited_by_item_areas
)
from .data.partners_meta import all_partners


def get_itemhints(
    allow_itemhints: bool,
    placed_items: list,
    options: PaperMarioOptions,
):
    """
    Returns a list of item hint lists for a given list of item nodes.
    Each item hint list contains the item id and a reference word describing
    the area, map and item source type.
    """
    return [[0x00000000, 0xFFFFFFFF]]