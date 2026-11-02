from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import BuildJetpackWorld

ITEM_NAME_TO_ID = {
    "Diving Suit": 1,
    "Oxygen Mask": 2,
    "Backpack": 3,
    "Fins": 4,
    "Magnet": 5,
    "Raft Expansion": 6,
    "Jetpack": 7,
    "Radar": 8,
    "Gold Statue": 9,
    "Money": 10,
    "Hostile Trap": 11,
    "Rapid Dive": 12,
    "Shield": 13,
    "Insurance": 14,
}

DEFAULT_ITEM_CLASSIFICATIONS = {
    "Diving Suit": ItemClassification.progression,
    "Oxygen Mask": ItemClassification.progression,
    "Backpack": ItemClassification.useful,
    "Fins": ItemClassification.useful,
    "Magnet": ItemClassification.filler,
    "Raft Expansion": ItemClassification.progression,
    "Jetpack": ItemClassification.progression | ItemClassification.useful,
    "Radar": ItemClassification.useful,
    "Gold Statue": ItemClassification.filler,
    "Money": ItemClassification.filler,
    "Hostile Trap": ItemClassification.trap,
    "Rapid Dive": ItemClassification.useful,
    "Shield": ItemClassification.useful,
    "Insurance": ItemClassification.useful,
}

class BuildJetpackItem(Item):
    game = "Build a Jetpack"

def get_random_filler_item_name(world: BuildJetpackWorld) -> str:
    if world.random.randint(0, 99) < world.options.trap_chance:
        return "Hostile Trap"
    return "Money"

def create_item_with_correct_classification(world: BuildJetpackWorld, name: str) -> BuildJetpackItem:
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]

    return BuildJetpackItem(name, classification, ITEM_NAME_TO_ID[name], world.player)

def create_all_items(world: BuildJetpackWorld) -> None:
    upgrades = {
        "Diving Suit": 8,
        "Oxygen Mask": 8,
        "Backpack": 7,
        "Fins": 7,
        "Magnet": 8,
        "Raft Expansion": 3,
        "Jetpack": 3,
        "Radar": 5,
        "Gold Statue": 1
    }

    if world.options.extra_upgrades:
        upgrades.update({
            "Rapid Dive": 3,
            "Shield": 3,
            "Insurance": 5
        })

    itempool: list[Item] = []

    for k,v in upgrades.items():
        for _ in range(v):
            itempool.append(world.create_item(k))
    
    number_of_items = len(itempool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items
    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    world.multiworld.itempool += itempool