from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import SkulWorld

ITEM_NAME_TO_ID = {
    
    # Progression
    "Progressive Stage": 20,
    "Progressive Skull Tree": 21,
    "Progressive Bone Tree": 22,
    "Progressive Spirit Tree": 23,
    
    # Useful
    "Marrow Transplant": 1,
    "Thick Bone": 2,
    "Fatal Mind": 3,
    "Quick Dislocation": 4,
    "Fracture Prevention": 5,
    "Ancestral Fortitude": 6,
    "Nutrition Supply": 7,
    "Heavy Frame": 8,
    "Spirit Acceleration": 9,
    "Exoskeleton Reinforcement": 10,
    "Reassemble": 11,
    "Ancient Alchemy": 12,
    "Fox NPC": 13,
    "Ogre NPC": 14,
    "Druid NPC": 15,
    "Death Knight NPC": 16,

    # Filler
    "Bone x10": 30,
    "Dark Quartz x100": 31,
    "Gold x200": 32,

    # Trap
    "De-Skull Trap": 40,
}

DEFAULT_ITEM_CLASSIFICATIONS = {
    "Progressive Stage": ItemClassification.progression,
    "Progressive Skull Tree": ItemClassification.progression,
    "Progressive Bone Tree": ItemClassification.progression,
    "Progressive Spirit Tree": ItemClassification.progression,
    
    "Marrow Transplant": ItemClassification.useful,
    "Thick Bone": ItemClassification.useful,
    "Fatal Mind": ItemClassification.useful,
    "Quick Dislocation": ItemClassification.useful,
    "Fracture Prevention": ItemClassification.useful,
    "Ancestral Fortitude": ItemClassification.useful,
    "Nutrition Supply": ItemClassification.useful,
    "Heavy Frame": ItemClassification.useful,
    "Spirit Acceleration": ItemClassification.useful,
    "Exoskeleton Reinforcement": ItemClassification.useful,
    "Reassemble": ItemClassification.useful,
    "Ancient Alchemy": ItemClassification.useful,
    "Fox NPC": ItemClassification.useful,
    "Ogre NPC": ItemClassification.useful,
    "Druid NPC": ItemClassification.useful,
    "Death Knight NPC": ItemClassification.progression,

    "Bone x10": ItemClassification.filler,
    "Dark Quartz x100": ItemClassification.filler,
    "Gold x200": ItemClassification.filler,

    "De-Skull Trap": ItemClassification.trap,
}


class SkulItem(Item):
    game = "Skul: The Hero Slayer"


def get_random_filler_item_name(world: SkulWorld) -> str:
    trap_chance = world.options.de_skull_trap_weight.value
    if trap_chance and world.random.randint(0, 99) < trap_chance:
        return "De-Skull Trap"
    return world.random.choice(["Bone x10", "Dark Quartz x100", "Gold x200"])


def create_item_with_correct_classification(world: SkulWorld, name: str) -> SkulItem:
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]

    return SkulItem(name, classification, ITEM_NAME_TO_ID[name], world.player)


def create_all_items(world: SkulWorld) -> None:

    itempool: list[Item] = []

    # Progressive Stage (one per area: Forest, Grand Hall, Black Lab, Fortress of Fate, Sacred Grounds)
    itempool += [world.create_item("Progressive Stage") for _ in range(5)]

    # Progressive tree upgrades (3 per tree — gates tiers 1, 2, 3 of each witch tree)
    for name in ["Progressive Skull Tree", "Progressive Bone Tree", "Progressive Spirit Tree"]:
        itempool += [world.create_item(name) for _ in range(3)]

    # Bone upgrades (x10 each)
    for name in [
        "Marrow Transplant", "Thick Bone", "Fatal Mind",
        "Quick Dislocation", "Fracture Prevention", "Ancestral Fortitude",
    ]:
        itempool += [world.create_item(name) for _ in range(10)]

    # Dark Quartz upgrades (x2 each)
    for name in [
        "Nutrition Supply", "Heavy Frame", "Spirit Acceleration",
        "Exoskeleton Reinforcement", "Reassemble", "Ancient Alchemy",
    ]:
        itempool += [world.create_item(name) for _ in range(2)]

    # NPCs
    itempool += [world.create_item("Fox NPC"), world.create_item("Ogre NPC"),
                 world.create_item("Druid NPC"), world.create_item("Death Knight NPC")]

    number_of_items = len(itempool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items
    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]
    world.multiworld.itempool += itempool