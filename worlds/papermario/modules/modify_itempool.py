import math
from copy import deepcopy

from ..data.enum_options import IncludeFavorsMode, RandomizeConsumablesMode
from ..data.item_exclusion import exclude_due_to_settings
from ..data.item_scores import item_scores
from ..data.itemlocation_special import (
    kootfavors_reward_locations,
    kootfavors_keyitem_locations,
    limited_by_item_areas,
)

from BaseClasses import Item
from ..data.LocationsList import location_table, location_groups
from ..data.ItemList import item_table, item_groups
from ..options import (
    ItemTraps,
    ShuffleKootFavors,
    ShuffleDojoRewards,
    PartnerUpgradeShuffle,
)


def _get_random_consumables(n: int, available_items: list, random) -> list:
    """
    Returns a list of n items, with categories similar to vanilla distribution
    """
    weights = {
        "battle": 50,
        "heal": 45,
        "taycet": 5,
    }
    item_weights = [
        weights[item["type"]]
        for item in available_items
    ]

    return random.choices(available_items, item_weights, k=n)


def _balance_consumables(
    items: list,
    available_items: list,
    target_score: int,
    random
):
    """
    Modifies a list of consumables until its score is close enough to the target
    score
    """
    new_items = items.copy()
    pool_score = sum([
        item["score"]
        for item in new_items
    ])

    lowest_item = item_scores[0]
    lowest_score = lowest_item["score"]
    highest_item = item_scores[len(item_scores) - 1]
    highest_score = highest_item["score"]
    score_diff = math.ceil((highest_score - lowest_score) / 2)

    # Randomly adjust the items to bring closer to target score
    while (   pool_score < (target_score - score_diff)
           or pool_score > (target_score + score_diff)
    ):
        if pool_score < target_score:
            # Upgrade an item
            item_weights = [
                highest_score - item["score"]
                for item in new_items
            ]
            i = random.choices(
                [
                    i
                    for i in range(len(new_items))
                ],
                item_weights
            ).pop()
            old_item = new_items[i]
            legal_items = [
                item
                for item in available_items
                if      item["score"] > old_item["score"]
                    and item["type"] == old_item["type"]
            ]
        else:
            # Downgrade an item
            item_weights = [
                item["score"] - lowest_score
                for item in new_items
            ]
            i = random.choices(
                [
                    i
                    for i in range(len(new_items))
                ],
                item_weights
            ).pop()
            old_item = new_items[i]
            legal_items = [
                item
                for item in available_items
                if     item["score"] < old_item["score"]
                   and item["type"] == old_item["type"]
            ]

        # If there's no legal items to upgrade/downgrade to, try again
        if len(legal_items) == 0:
            continue

        new_item = random.choice(legal_items)
        pool_score += (new_item["score"] - old_item["score"])
        new_items[i] = new_item

    return new_items


def get_randomized_itempool(
    itempool: list,
    consumable_mode: int,
    quality: int,
    add_unused_items: bool,
    random,
) -> list:
    """
    Returns a randomized general item pool according to consumable mode
    Balanced random mode creates an item pool that has a value equal
    to the input pool's value, multiplied by the quality percentage
    """
    # Consumable mode:
    # 0: vanilla (no quality)
    # 1: full random (no quality)
    # 2: balanced random (quality applies)
    # 3: mystery only (no quality)

    # vanilla
    if consumable_mode == RandomizeConsumablesMode.OFF:
        return itempool

    def is_consumable(item_name):
        item_score_obj = next(
            (x for x in item_scores if x.get("name") == item_name),
            None
        )
        return item_score_obj is not None

    new_items = []
    kept_items = [x for x in itempool if not is_consumable(x)]
    removed_items = [x for x in itempool if is_consumable(x)]
    target_count = len(removed_items)

    # Random or Balanced Random
    if (   consumable_mode == RandomizeConsumablesMode.FULL_RANDOM
        or consumable_mode == RandomizeConsumablesMode.BALANCED_RANDOM
    ):
        if add_unused_items:
            available_items = item_scores
        else:
            available_items = [
                item
                for item in item_scores
                if item["name"] not in ["Hustle Drink", "Insecticide Herb"]
            ]

        # Generate fully random pool
        new_items = _get_random_consumables(target_count, available_items, random)

        # Balance according to quality factor
        if consumable_mode == RandomizeConsumablesMode.BALANCED_RANDOM:
            target_score = 0
            for item_name in removed_items:
                target_score += next(
                    item["score"]
                    for item in item_scores
                    if item["name"] == item_name
                )

            # Multiply score by the quality factor
            target_score = math.floor(target_score * (quality / 100))
            new_items = _balance_consumables(
                new_items,
                available_items,
                target_score,
                random,
            )

        # Convert from scored dict entries to proper item_obj list
        new_items = [item["name"] for item in new_items]

    # Mystery only
    elif consumable_mode == RandomizeConsumablesMode.MYSTERY_ONLY:
        mystery_item = "Mystery"
        for _ in range(target_count):
            new_items.append(deepcopy(mystery_item))

    new_itempool = kept_items + new_items
    assert (len(itempool) == len(new_itempool))
    return new_itempool
