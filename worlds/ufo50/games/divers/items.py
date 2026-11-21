from typing import TYPE_CHECKING, NamedTuple

from BaseClasses import ItemClassification as IC, Item

from ...constants import get_game_base_id

if TYPE_CHECKING:
    from ... import UFO50World


class ItemInfo(NamedTuple):
    id_offset: int
    classification: IC
    quantity: int
    group: str


item_table: dict[str, ItemInfo] = {
    # Weapons
    "Slime Stick": ItemInfo(0, IC.filler, 1, "Weapons"),
    "Slime Lance": ItemInfo(1, IC.progression, 1, "Weapons"),
    "Slime Trident": ItemInfo(2, IC.progression, 1, "Weapons"),
    "Shell Stick": ItemInfo(3, IC.filler, 1, "Weapons"),
    "Shell Lance": ItemInfo(4, IC.progression, 1, "Weapons"),
    "Shell Trident": ItemInfo(5, IC.progression, 1, "Weapons"),
    "Elec Stick": ItemInfo(6, IC.filler, 1, "Weapons"),
    "Elec Lance": ItemInfo(7, IC.progression, 1, "Weapons"),
    "Elec Trident": ItemInfo(8, IC.progression, 1, "Weapons"),
    "Holy Rod": ItemInfo(9, IC.progression, 1, "Weapons"),
    "Slime Mallet": ItemInfo(20, IC.filler, 1, "Weapons"),
    "Slime Sledge": ItemInfo(21, IC.progression, 1, "Weapons"),
    "Shell Mallet": ItemInfo(22, IC.filler, 1, "Weapons"),
    "Shell Sledge": ItemInfo(23, IC.progression, 1, "Weapons"),
    "Elec Mallet": ItemInfo(24, IC.filler, 1, "Weapons"),
    "Elec Sledge": ItemInfo(25, IC.progression, 1, "Weapons"),
    "Parasite Hammer": ItemInfo(26, IC.progression, 1, "Weapons"),
    "Slime Lid": ItemInfo(40, IC.filler, 1, "Weapons"),
    "Slime Buckler": ItemInfo(41, IC.progression, 1, "Weapons"),
    "Slime Tower": ItemInfo(42, IC.progression, 1, "Weapons"),
    "Shell Lid": ItemInfo(43, IC.filler, 1, "Weapons"),
    "Shell Buckler": ItemInfo(44, IC.progression, 1, "Weapons"),
    "Shell Tower": ItemInfo(45, IC.progression, 1, "Weapons"),
    "Elec Lid": ItemInfo(46, IC.filler, 1, "Weapons"),
    "Elec Buckler": ItemInfo(47, IC.progression, 1, "Weapons"),
    "Elec Tower": ItemInfo(48, IC.progression, 1, "Weapons"),
    "Thorn Shield": ItemInfo(49, IC.progression, 1, "Weapons"),
    # Potions
    "Small Potion": ItemInfo(60, IC.filler, 1, "Potions"),
    "Medium Potion": ItemInfo(61, IC.filler, 1, "Potions"),
    "Large Potion": ItemInfo(62, IC.progression, 1, "Potions"),
    "Holy Potion": ItemInfo(63, IC.progression, 1, "Potions"),
    "Evil Potion": ItemInfo(64, IC.progression, 1, "Potions"),
    "Egg": ItemInfo(65, IC.filler, 1, "Potions"),
    # Key
    "Bomb": ItemInfo(80, IC.progression, 1, "Key"),
    "Mist Orb": ItemInfo(81, IC.progression, 1, "Key"),
    "Flippers": ItemInfo(82, IC.progression, 1, "Key"),
    "Godblood": ItemInfo(83, IC.filler, 1, "Key"),
    # XP/gold multiplier
    "Progressive Cash Mult": ItemInfo(90, IC.useful, 0, "Bonus"),
    "Progressive XP Mult": ItemInfo(95, IC.useful, 0, "Bonus"),
    # gates
    "Slime Cave Gate": ItemInfo(100, IC.progression, 1, "Key"),
    "Ruins North Gate": ItemInfo(101, IC.progression, 1, "Key"),
    "Boss Gate 1": ItemInfo(102, IC.progression, 1, "Key"),
    "Boss Gate 2": ItemInfo(103, IC.progression, 1, "Key"),
    "Ruins Northeast Gate": ItemInfo(104, IC.progression, 1, "Key"),
    "Ruins Southeast Gate": ItemInfo(105, IC.progression, 1, "Key"),
    "Ruins Southwest Gate": ItemInfo(106, IC.progression, 1, "Key"),
    # relics
    "Fisheye": ItemInfo(110, IC.filler, 1, "Relic"),
    "Residue": ItemInfo(111, IC.filler, 1, "Relic"),
    "Roe": ItemInfo(112, IC.filler, 1, "Relic"),
    "Ingot": ItemInfo(113, IC.filler, 1, "Relic"),
    "Scale": ItemInfo(114, IC.filler, 1, "Relic"),
    "Cross": ItemInfo(115, IC.filler, 1, "Relic"),
    "500 Cash": ItemInfo(118, IC.filler, 1, "Relic"),
    # A relic is given by the ruins boss
    "A relic": ItemInfo(116, IC.filler, 0, "Relic"),
    "B relic": ItemInfo(117, IC.progression, 1, "Relic"),
    # Emblems
    "Barbuta Emblem" : ItemInfo(120, IC.progression, 1, "Key"),
    "Mooncat Emblem": ItemInfo(121, IC.progression, 1, "Key"),
    "Divers Emblem": ItemInfo(122, IC.progression, 1, "Key"),
    # Store Access
    # start with sticks
    "Mallets Store Page": ItemInfo(131, IC.progression, 1, "Key"),
    "Lids Store Page": ItemInfo(132, IC.progression, 1, "Key"),
    "Potions Store Page": ItemInfo(133, IC.progression, 1, "Key"),
    "Bombs Store Page": ItemInfo(134, IC.progression, 1, "Key"),
}


# this is for filling out item_name_to_id, it should be static regardless of yaml options
def get_items() -> dict[str, int]:
    return {f"Divers - {name}": data.id_offset + get_game_base_id("Divers") for name, data in item_table.items()}


# this should return the item groups for this game, independent of yaml options
def get_item_groups() -> dict[str, set[str]]:
    item_groups: dict[str, set[str]] = {"Divers": {
        f"Divers - {item_name}" for item_name in item_table.keys()}}
    item_groups.update({
        "Divers - Weapons": {
            "Divers - Slime Stick",
            "Divers - Slime Lance",
            "Divers - Slime Trident",
            "Divers - Shell Stick",
            "Divers - Shell Lance",
            "Divers - Shell Trident",
            "Divers - Elec Stick",
            "Divers - Elec Lance",
            "Divers - Elec Trident",
            "Divers - Holy Rod",
            "Divers - Slime Mallet",
            "Divers - Slime Sledge",
            "Divers - Shell Mallet",
            "Divers - Shell Sledge",
            "Divers - Elec Mallet",
            "Divers - Elec Sledge",
            "Divers - Parasite Hammer",
            "Divers - Slime Lid",
            "Divers - Slime Buckler",
            "Divers - Slime Tower",
            "Divers - Shell Lid",
            "Divers - Shell Buckler",
            "Divers - Shell Tower",
            "Divers - Elec Lid",
            "Divers - Elec Buckler",
            "Divers - Elec Tower",
            "Divers - Thorn Shield"},
        "Divers - Potions": {
            "Divers - Small Potion",
            "Divers - Medium Potion",
            "Divers - Large Potion",
            "Divers - Holy Potion",
            "Divers - Evil Potion",
            "Divers - Egg"},
        "Divers - Key": {
            "Divers - Bomb",
            "Divers - Mist Orb",
            "Divers - Flippers",
            "Divers - Godblood",
            "Divers - Shallows Gate",
            "Divers - Ruins Gate",
            "Divers - Boss Gate 1",
            "Divers - Boss Gate 2"},
        "Divers - Bonus": {
            "Divers - Progressive Cash Mult",
            "Divers - Progressive XP Mult"},
        "Divers - Relic": {
            "Divers - Fisheye",
            "Divers - Residue",
            "Divers - Roe",
            "Divers - Ingot",
            "Divers - Scale",
            "Divers - Cross",
            "Divers - 500 Cash",
            "Divers - A Relic",
            "Divers - B Relic"},
    })
    return item_groups


# for when the world needs to create an item at random (like with random filler items)
def create_item(item_name: str, world: "UFO50World", item_class: IC = None) -> Item:
    base_id = get_game_base_id("Divers")
    if item_name.startswith("Divers - "):
        item_name = item_name.split(" - ", 1)[1]
    item_data = item_table[item_name]
    return Item(f"Divers - {item_name}", item_class or item_data.classification,
                base_id + item_data.id_offset, world.player)


# for when the world is getting the items to place into the multiworld's item pool
def create_items(world: "UFO50World") -> list[Item]:
    cash_item = 0
    xp_item = 0

    while world.options.divers_cash_item > cash_item:
        cash_item = cash_item + 1

    while world.options.divers_xp_item > xp_item:
        xp_item = xp_item + 1

    items_to_create: dict[str, int] = {item_name: data.quantity for item_name, data in item_table.items()}
    items_to_create["Progressive Cash Mult"] = cash_item
    items_to_create["Progressive XP Mult"] = xp_item
    if world.options.divers_start_flippers:
        items_to_create["Flippers"] = 0
    divers_items: list[Item] = []
    for item_name, quantity in items_to_create.items():
        for _ in range(quantity):
            divers_items.append(create_item(item_name, world))
    return divers_items


def get_filler_item_name(world: "UFO50World") -> str:
    return world.random.choice(["Divers - Fisheye", "Divers - Residue", "Divers - Roe", "Divers - Ingot",
                                "Divers - Scale", "Divers - Cross", "Divers - 500 Cash"])
