from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import PikunikuWorld

BASE_ITEM_ID = 100

# Default classification for every item.
# Items that only exist on certain options must still be present here and in ITEM_NAME_TO_ID.
DEFAULT_ITEM_CLASSIFICATIONS = {
    # Hats
    "Pencil Hat": ItemClassification.progression,
    "Water Hat": ItemClassification.progression,
    "Sunglasses": ItemClassification.progression,
    "X-Ray Glasses": ItemClassification.progression,
    "Flower Hat": ItemClassification.filler,
    "Beast Mask": ItemClassification.filler,
    "Some Arms": ItemClassification.filler,
    # Key Items
    "Magnetic Card": ItemClassification.progression,
    "The Cabin Key": ItemClassification.progression,
    "A Detonator": ItemClassification.progression,
    "Apple": ItemClassification.progression,
    "The Golden Tooth from the Silver Frog": ItemClassification.progression,
    "Co-op Level Access": ItemClassification.progression,
    "A Video Game": ItemClassification.filler,
    # Trophies
    "Sam the Slime Trophy": ItemClassification.filler,
    "The Resistance Trophy": ItemClassification.filler,
    "A Giant Robot Trophy": ItemClassification.filler,
    "The Demonic Toast Trophy": ItemClassification.filler,
    "PikDug Trophy": ItemClassification.filler,
    "Piku at the Beach Trophy": ItemClassification.filler,
    "The Worms Trophy": ItemClassification.filler,
    "Ernie the Worm Trophy": ItemClassification.filler,
    "Sunshine Inc. Robot Trophy": ItemClassification.filler,
    "Mr. Sunshine Trophy": ItemClassification.filler,
    "Baskick Champion Trophy": ItemClassification.filler,
    "Walking Piku Trophy": ItemClassification.filler,
    "The Hidden Rock Trophy": ItemClassification.filler,
    "Piku & Niku I Trophy": ItemClassification.filler,
    "Piku & Niku II Trophy": ItemClassification.filler,
    "Piku & Niku III Trophy": ItemClassification.filler,
    "Piku & Niku IV Trophy": ItemClassification.filler,
    "Piku & Niku V Trophy": ItemClassification.filler,
    # Junk
    "A Scary Plush": ItemClassification.filler,
    "Forest Postcard": ItemClassification.filler,
    # Each "5 Coins" item gives 5 coins. With coinsanity on, some of them are progression
    # (enough to afford every shop purchase), see create_all_items.
    "5 Coins": ItemClassification.filler,
    "Joyful Whimsy": ItemClassification.filler,
}

ITEM_NAME_TO_ID = {name: BASE_ITEM_ID + index for index, name in enumerate(DEFAULT_ITEM_CLASSIFICATIONS)}

# Progression items that are always created exactly once.
UNIQUE_PROGRESSION_ITEMS = [
    "Pencil Hat",
    "Water Hat",
    "Sunglasses",
    "X-Ray Glasses",
    "Magnetic Card",
    "The Cabin Key",
    "A Detonator",
    "The Golden Tooth from the Silver Frog",
]

# Non-progression items that are always created exactly once.
UNIQUE_OTHER_ITEMS = [
    "Flower Hat",
    "Beast Mask",
    "Some Arms",
    "A Video Game",
    "A Scary Plush",
    "Forest Postcard",
    "Sam the Slime Trophy",
    "The Resistance Trophy",
    "A Giant Robot Trophy",
    "The Demonic Toast Trophy",
    "PikDug Trophy",
    "Piku at the Beach Trophy",
    "The Worms Trophy",
    "Ernie the Worm Trophy",
    "Sunshine Inc. Robot Trophy",
    "Mr. Sunshine Trophy",
    "Baskick Champion Trophy",
    "Walking Piku Trophy",
    "The Hidden Rock Trophy",
]

COOP_ITEMS = [
    "Co-op Level Access",
    "Piku & Niku I Trophy",
    "Piku & Niku II Trophy",
    "Piku & Niku III Trophy",
    "Piku & Niku IV Trophy",
    "Piku & Niku V Trophy",
]

ITEM_NAME_GROUPS = {
    "Hats": {"Pencil Hat", "Water Hat", "Sunglasses", "X-Ray Glasses", "Flower Hat", "Beast Mask", "Some Arms"},
    "Trophies": {
        "Sam the Slime Trophy",
        "The Resistance Trophy",
        "A Giant Robot Trophy",
        "The Demonic Toast Trophy",
        "PikDug Trophy",
        "Piku at the Beach Trophy",
        "The Worms Trophy",
        "Ernie the Worm Trophy",
        "Sunshine Inc. Robot Trophy",
        "Mr. Sunshine Trophy",
        "Baskick Champion Trophy",
        "Walking Piku Trophy",
        "The Hidden Rock Trophy",
        "Piku & Niku I Trophy",
        "Piku & Niku II Trophy",
        "Piku & Niku III Trophy",
        "Piku & Niku IV Trophy",
        "Piku & Niku V Trophy",
    },
    "Key Items": {
        "Magnetic Card",
        "The Cabin Key",
        "A Detonator",
        "Apple",
        "The Golden Tooth from the Silver Frog",
        "Co-op Level Access",
    },
}


class PikunikuItem(Item):
    game = "Pikuniku"


def get_filler_item_name(world: PikunikuWorld) -> str:
    # With coinsanity on, the coin economy is exact (one "5 Coins" per coin location),
    # so additionally requested filler is Joyful Whimsy instead.
    if world.options.coinsanity:
        return "Joyful Whimsy"
    return "5 Coins"


def create_item_with_correct_classification(world: PikunikuWorld, name: str) -> PikunikuItem:
    return PikunikuItem(name, DEFAULT_ITEM_CLASSIFICATIONS[name], ITEM_NAME_TO_ID[name], world.player)


def create_all_items(world: PikunikuWorld) -> None:
    from . import locations

    itempool: list[Item] = [world.create_item(name) for name in UNIQUE_PROGRESSION_ITEMS]

    # Three apples are needed to open the Apple Temple.
    itempool += [world.create_item("Apple") for _ in range(3)]

    itempool += [world.create_item(name) for name in UNIQUE_OTHER_ITEMS]

    if world.options.coop_levels:
        itempool += [world.create_item(name) for name in COOP_ITEMS]

    if world.options.coinsanity:
        # One "5 Coins" item per freestanding coin location.
        # Only enough of them to afford every shop purchase are progression, the rest are filler.
        for index in range(len(locations.COIN_LOCATIONS)):
            classification = (
                ItemClassification.progression_skip_balancing
                if index < locations.PROGRESSION_FIVE_COINS_COUNT
                else ItemClassification.filler
            )
            itempool.append(PikunikuItem("5 Coins", classification, ITEM_NAME_TO_ID["5 Coins"], world.player))

    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - len(itempool)
    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    world.multiworld.itempool += itempool
