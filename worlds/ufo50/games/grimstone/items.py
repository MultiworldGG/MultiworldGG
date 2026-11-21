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
    # Items
    "BANDHALF": ItemInfo(0, IC.filler, 0, "Items"),
    "BANDAGE": ItemInfo(1, IC.filler, 1, "Items"),
    "HERBHALF": ItemInfo(2, IC.filler, 0, "Items"),
    "HERB": ItemInfo(3, IC.filler, 1, "Items"),
    "OINTHALF": ItemInfo(4, IC.filler, 0, "Items"),
    "OINTMENT": ItemInfo(5, IC.filler, 1, "Items"),
    "MEDHALF": ItemInfo(6, IC.filler, 0, "Items"),
    "MEDKIT": ItemInfo(7, IC.filler, 2, "Items"),
    "ANTIHALF": ItemInfo(8, IC.filler, 0, "Items"),
    "ANTIDOTE": ItemInfo(9, IC.filler, 2, "Items"),
    "HOLYWATER": ItemInfo(10, IC.filler, 2, "Items"),
    "ROOTBEER": ItemInfo(11, IC.filler, 1, "Items"),
    "COFFEE": ItemInfo(12, IC.filler, 2, "Items"),
    "MINTLEAF": ItemInfo(13, IC.filler, 1, "Items"),
    "P.PEAR": ItemInfo(14, IC.filler, 1, "Items"),
    "LASSO": ItemInfo(15, IC.filler, 1, "Items"),
    "BEDROLLS": ItemInfo(16, IC.filler, 1, "Items"),
    "FEATHER": ItemInfo(17, IC.filler, 2, "Items"),
    "SALT": ItemInfo(18, IC.filler, 1, "Items"),
    "DOGTREAT A": ItemInfo(19, IC.filler, 1, "Items"),
    "DOGTREAT D": ItemInfo(20, IC.filler, 1, "Items"),
    "DOGTREAT E": ItemInfo(21, IC.filler, 1, "Items"),
    "k MINE": ItemInfo(22, IC.filler, 0, "Items"),
    "k FOCUS": ItemInfo(23, IC.filler, 0, "Items"),
    # Weapons
    "a DERANGER": ItemInfo(30, IC.filler, 1, "Weapons"),
    "a PEPPRBOX": ItemInfo(31, IC.filler, 1, "Weapons"),
    "a SIDEWIND": ItemInfo(32, IC.filler, 2, "Weapons"),
    "a DRAGOON": ItemInfo(33, IC.useful, 1, "Weapons"),
    "a PEACEMKR": ItemInfo(34, IC.useful, 2, "Weapons"),
    "a HELLFANG": ItemInfo(35, IC.useful, 1, "Weapons"),
    "b COACH": ItemInfo(36, IC.filler, 1, "Weapons"),
    "b 4BARREL": ItemInfo(37, IC.filler, 1, "Weapons"),
    "b BUSTER": ItemInfo(38, IC.filler, 1, "Weapons"),
    "b NOCKER": ItemInfo(39, IC.filler, 1, "Weapons"),
    "b PUNTER": ItemInfo(40, IC.useful, 1, "Weapons"),
    "c LONGRIFL": ItemInfo(41, IC.filler, 1, "Weapons"),
    "c SCORPION": ItemInfo(42, IC.filler, 1, "Weapons"),
    "c INFANTRY": ItemInfo(43, IC.filler, 1, "Weapons"),
    "c BUFFALO": ItemInfo(44, IC.useful, 1, "Weapons"),
    "c MUSKET": ItemInfo(45, IC.filler, 1, "Weapons"),
    "c CALAMITY": ItemInfo(46, IC.useful, 1, "Weapons"),
    "d RATLING": ItemInfo(47, IC.filler, 1, "Weapons"),
    "d MITRAIL": ItemInfo(48, IC.filler, 1, "Weapons"),
    "d BLITZER": ItemInfo(49, IC.useful, 1, "Weapons"),
    "d INFERNO": ItemInfo(50, IC.useful, 1, "Weapons"),
    "e KITCHEN": ItemInfo(51, IC.filler, 1, "Weapons"),
    "e DAGGER": ItemInfo(52, IC.filler, 2, "Weapons"),
    "e BOWIE": ItemInfo(53, IC.filler, 1, "Weapons"),
    "e OBSIDIAN": ItemInfo(54, IC.useful, 1, "Weapons"),
    "e TOOTHPIK": ItemInfo(55, IC.useful, 2, "Weapons"),
    "j WOOD": ItemInfo(56, IC.filler, 1, "Weapons"),
    "j RECURVE": ItemInfo(57, IC.filler, 1, "Weapons"),
    "j EAGLE": ItemInfo(58, IC.useful, 1, "Weapons"),
    # Armor
    "f BANDANA": ItemInfo(59, IC.filler, 1, "Armor"),
    "f BOLO": ItemInfo(60, IC.filler, 1, "Armor"),
    "f CHARM": ItemInfo(61, IC.filler, 1, "Armor"),
    "f BONE": ItemInfo(62, IC.filler, 2, "Armor"),
    "f DIAMOND": ItemInfo(63, IC.useful, 2, "Armor"),
    "f RESIST": ItemInfo(64, IC.useful, 1, "Armor"),
    "f SHAMAN": ItemInfo(65, IC.useful, 1, "Armor"),
    "f FOCUS": ItemInfo(66, IC.useful, 1, "Armor"),
    "g LITEVEST": ItemInfo(67, IC.filler, 1, "Armor"),
    "g WOOL": ItemInfo(68, IC.filler, 1, "Armor"),
    "g LEATHER": ItemInfo(69, IC.filler, 1, "Armor"),
    "g PONCHO": ItemInfo(70, IC.useful, 1, "Armor"),
    "g DUSTER": ItemInfo(71, IC.useful, 2, "Armor"),
    "g DEMON": ItemInfo(72, IC.useful, 1, "Armor"),
    "h COTTON": ItemInfo(73, IC.filler, 1, "Armor"),
    "h WOOL": ItemInfo(74, IC.filler, 1, "Armor"),
    "h LEATHER": ItemInfo(75, IC.filler, 1, "Armor"),
    "h SILK": ItemInfo(76, IC.useful, 2, "Armor"),
    "h ROYAL": ItemInfo(77, IC.useful, 1, "Armor"),
    "i WORN": ItemInfo(78, IC.filler, 1, "Armor"),
    "i LEATHER": ItemInfo(79, IC.filler, 1, "Armor"),
    "i SNAKE": ItemInfo(80, IC.filler, 1, "Armor"),
    "i EELSKIN": ItemInfo(81, IC.filler, 1, "Armor"),
    "i GATOR": ItemInfo(82, IC.useful, 1, "Armor"),
    "i MOCASIN": ItemInfo(83, IC.useful, 2, "Armor"),
    # Valuables
    "ABYSSIDIAN": ItemInfo(84, IC.progression, 1, "Key"),
    "DIAMOND": ItemInfo(85, IC.filler, 1, "Valuables"),
    "RUBY": ItemInfo(86, IC.filler, 1, "Valuables"),
    "EMERALD": ItemInfo(87, IC.filler, 1, "Valuables"),
    "TOPAZ": ItemInfo(88, IC.filler, 1, "Valuables"),
    "GOLD": ItemInfo(89, IC.filler, 1, "Valuables"),
    "SILVER": ItemInfo(90, IC.filler, 1, "Valuables"),
    "IRON ORE": ItemInfo(91, IC.filler, 1, "Valuables"),
    # Key Items
    "TOOLBOX": ItemInfo(92, IC.progression, 1, "Key"),
    # "LETTER": ItemInfo(93, IC.filler, 1, "Key"),
    "M. MIRROR": ItemInfo(94, IC.progression, 1, "Key"),
    "RUSTY KEY": ItemInfo(95, IC.progression, 1, "Key"),
    "DETONATOR": ItemInfo(96, IC.progression, 1, "Key"),
    "DEVIL HORN": ItemInfo(97, IC.progression, 1, "Key"),
    "HORSESHOE": ItemInfo(98, IC.progression, 1, "Key"),
    "HAMMER": ItemInfo(99, IC.progression, 1, "Key"),
    "SCALE": ItemInfo(100, IC.progression, 1, "Key"),
    "PASS": ItemInfo(101, IC.progression, 1, "Key"),
    # Bonus
    "Progressive Cash Mult": ItemInfo(200, IC.useful, 0, "Bonus"),
    "Progressive XP Mult": ItemInfo(201, IC.useful, 0, "Bonus"),
}


# this is for filling out item_name_to_id, it should be static regardless of yaml options
def get_items() -> dict[str, int]:
    return {f"Grimstone - {name}": data.id_offset + get_game_base_id("Grimstone") for name, data in item_table.items()}


# this should return the item groups for this game, independent of yaml options
def get_item_groups() -> dict[str, set[str]]:
    item_groups: dict[str, set[str]] = {"Grimstone": {
        f"Grimstone - {item_name}" for item_name in item_table.keys()}}
    return item_groups


# for when the world needs to create an item at random (like with random filler items)
def create_item(item_name: str, world: "UFO50World", item_class: IC = None) -> Item:
    base_id = get_game_base_id("Grimstone")
    if item_name.startswith("Grimstone - "):
        item_name = item_name.split(" - ", 1)[1]
    item_data = item_table[item_name]
    return Item(f"Grimstone - {item_name}", item_class or item_data.classification,
                base_id + item_data.id_offset, world.player)


# for when the world is getting the items to place into the multiworld's item pool
def create_items(world: "UFO50World") -> list[Item]:
    cash_item = 0
    xp_item = 0

    while world.options.grimstone_cash_item > cash_item:
       cash_item += 1

    while world.options.grimstone_xp_item > xp_item:
        xp_item += 1

    items_to_create: dict[str, int] = {item_name: data.quantity for item_name, data in item_table.items()}
    items_to_create["Progressive Cash Mult"] = cash_item
    items_to_create["Progressive XP Mult"] = xp_item
    grimstone_items: list[Item] = []
    for item_name, quantity in items_to_create.items():
        for _ in range(quantity):
            grimstone_items.append(create_item(item_name, world))
    return grimstone_items


def get_filler_item_name(world: "UFO50World") -> str:
    return world.random.choice(["Grimstone - DOGTREAT A", "Grimstone - DOGTREAT D", "Grimstone - DOGTREAT E",
                                "Grimstone - BANDAGE", "Grimstone - HERB", "Grimstone - OINTMENT", "Grimstone - MEDKIT",
                                "Grimstone - ROOTBEER", "Grimstone - FEATHER", "Grimstone - SALT",
                                "Grimstone - ANTIDOTE", "Grimstone - BEDROLLS", "Grimstone - HOLYWATER",
                                "Grimstone - MINTLEAF"])
