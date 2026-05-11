### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from collections.abc import Mapping
from random import Random
from typing import NamedTuple

from BaseClasses import Item, ItemClassification


class CupheadItem(Item):
    game: str = "Cuphead"

class ItemData(NamedTuple):
    id: int | None
    item_type: ItemClassification = ItemClassification.filler
    quantity: int = 1 # Set to 0 to skip automatic placement (Useful if placing manually)
    event: bool = False
    category: str | None = None

    def with_item_type(self, type: ItemClassification) -> "ItemData":
        return ItemData(self.id, type, self.quantity, self.event, self.category)
    def with_quantity(self, quantity: int) -> "ItemData":
        return ItemData(self.id, self.item_type, quantity, self.event, self.category)

def weighted_item_choice(item_weights: Mapping[str, int], rand: Random) -> str:
    if len(item_weights)<1:
        raise ValueError("item_weights must not be empty!")

    active_items = list(item_weights.keys())
    active_weights = list(item_weights.values())

    total_weight = sum(active_weights)

    if total_weight <= 0:
        raise ValueError("Total weight must be greater than 0!")

    choice = rand.randint(1, total_weight)

    culum_sum = 0
    for i, weight in enumerate(active_weights):
        culum_sum += weight
        if choice <= culum_sum:
            return active_items[i]
    raise ValueError("Failed to choose an item from weighted_item_choice!")
