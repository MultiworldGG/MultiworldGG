from typing import NamedTuple, TYPE_CHECKING

from BaseClasses import ItemClassification as IC, Item

from ...constants import get_game_base_id

if TYPE_CHECKING:
    from ... import UFO50World


class ItemInfo(NamedTuple):
    id_offset: int
    classification: IC
    quantity: int = 1


item_table: dict[str, ItemInfo] = {
    "+1 Starting Cash": ItemInfo(0, IC.filler, 3),
    "+1 Starting Popularity": ItemInfo(1, IC.filler, 2)
}


def get_items() -> dict[str, int]:
    return {f"Party House - {name}": data.id_offset + get_game_base_id("Party House") for name, data in item_table.items()}


def get_item_groups() -> dict[str, set[str]]:
    item_groups: dict[str, set[str]] = {"Party House": {
        f"Party House - {item_name}" for item_name in item_table.keys()}}
    return item_groups


def create_item(item_name: str, world: "UFO50World", item_class: IC = None) -> Item:
    base_id = get_game_base_id("Party House")
    if item_name.startswith("Party House - "):
        item_name = item_name.split(" - ", 1)[1]
    item_data = item_table[item_name]
    return Item(f"Party House - {item_name}", item_class or item_data.classification,
                base_id + item_data.id_offset, world.player)


def create_items(world: "UFO50World") -> list[Item]:
    items_to_create: dict[str, int] = {item_name: data.quantity for item_name, data in item_table.items()}
    party_house_items: list[Item] = []

    for item_name, quantity in items_to_create.items():
        for _ in range(quantity):
            party_house_items.append(create_item(item_name, world))
    return party_house_items


def get_filler_item_name(world: "UFO50World") -> str:
    return world.random.choice(["Party House - +1 Starting Cash", "Party House - +1 Starting Popularity"])
