from BaseClasses import Item, ItemClassification
from . import Common
from collections.abc import Callable
from typing import NamedTuple
from .LADXR.locations.items import *
from .LADXR.locations.constants import CHEST_ITEMS
from .LADXR.utils import AP_NAMES


dungeon_item_types = ('INSTRUMENT', 'NIGHTMARE_KEY', 'KEY', 'STONE_BEAK', 'MAP', 'COMPASS')


class ItemData():
    item_name: str
    ladxr_id: str
    classification: ItemClassification
    item_id: int
    dungeon_item_type: str | None
    dungeon_index: int | None

    def __init__(self, ladxr_id, classification):
        self.item_name = AP_NAMES[ladxr_id]
        self.ladxr_id = ladxr_id
        self.classification = classification
        self.item_id = CHEST_ITEMS[ladxr_id]
        self.dungeon_item_type = next((t for t in dungeon_item_types if ladxr_id.startswith(t)), None)
        if self.dungeon_item_type:
            self.dungeon_index = int(self.ladxr_id[-1])


class LinksAwakeningItem(Item):
    game: str = Common.LINKS_AWAKENING

    def __init__(self, item_data, world, player):
        classification = item_data.classification
        if callable(classification):
            classification = classification(world, player)

        super().__init__(item_data.item_name, classification, Common.BASE_ID + item_data.item_id, player)
        self.item_data = item_data


class ItemGroup(NamedTuple):
    classification: ItemClassification | Callable
    items: list[str]
    in_game_hintable: bool = True
    goes_in_datapackage: bool = True

def stone_beak_classification(world, player):
    if world.options.owlsanity == "none":
        return ItemClassification.useful
    else:
        return ItemClassification.progression

def seashell_classification(world, player):
    if world.options.goal == "seashells":
        return ItemClassification.progression_skip_balancing
    else:
        return ItemClassification.progression_deprioritized_skip_balancing

# group items for classification, but also for data package item groups
item_groups: dict[str, ItemGroup] = {
    "Instruments": ItemGroup(ItemClassification.progression, [f'INSTRUMENT{i}' for i in range(1, 9)]),
    "Small Keys": ItemGroup(ItemClassification.progression, [f'KEY{i}' for i in range(1, 10)]),
    "Nightmare Keys": ItemGroup(ItemClassification.progression, [f'NIGHTMARE_KEY{i}' for i in range(1, 10)]),
    "Maps": ItemGroup(ItemClassification.filler, [f'MAP{i}' for i in range(1, 10)], False),
    "Compasses": ItemGroup(ItemClassification.filler, [f'COMPASS{i}' for i in range(1, 10)], False),
    "Stone Beaks": ItemGroup(stone_beak_classification, [f'STONE_BEAK{i}' for i in range(1, 10)]),
    "Equipment": ItemGroup(ItemClassification.progression, [
        SWORD,
        BOMB,
        POWER_BRACELET,
        SHIELD,
        BOW,
        HOOKSHOT,
        MAGIC_ROD,
        PEGASUS_BOOTS,
        OCARINA,
        FEATHER,
        SHOVEL,
        MAGIC_POWDER,
        BOOMERANG,
        ROOSTER,
        FLIPPERS,
        TOADSTOOL,
        BOWWOW,
    ]),
    "Songs": ItemGroup(ItemClassification.progression, [f'SONG{i}' for i in range(1, 4)]),
    "Entrance Keys": ItemGroup(ItemClassification.progression, [
        SLIME_KEY,
        TAIL_KEY,
        ANGLER_KEY,
        FACE_KEY,
        BIRD_KEY,
    ]),
    "Rupees": ItemGroup(ItemClassification.progression_deprioritized_skip_balancing, [
        RUPEES_20,
        RUPEES_50,
        RUPEES_100,
        RUPEES_200,
        RUPEES_500,
    ], False),
    "Trading Items": ItemGroup(ItemClassification.progression, [
        TRADING_ITEM_YOSHI_DOLL,
        TRADING_ITEM_RIBBON,
        TRADING_ITEM_DOG_FOOD,
        TRADING_ITEM_BANANAS,
        TRADING_ITEM_STICK,
        TRADING_ITEM_HONEYCOMB,
        TRADING_ITEM_PINEAPPLE,
        TRADING_ITEM_HIBISCUS,
        TRADING_ITEM_LETTER,
        TRADING_ITEM_BROOM,
        TRADING_ITEM_FISHING_HOOK,
        TRADING_ITEM_NECKLACE,
        TRADING_ITEM_SCALE,
        TRADING_ITEM_MAGNIFYING_GLASS,
    ]),
    "Gold Leaf": ItemGroup(ItemClassification.progression_deprioritized_skip_balancing, [
        GOLD_LEAF,
    ], False, False),
    "Seashells": ItemGroup(seashell_classification, [
        SEASHELL
    ], True, False),
    "Traps": ItemGroup(ItemClassification.trap, [
        BAD_HEART_CONTAINER,
        GEL,
        DEATH,
        SLIME_STORM,
        BOMB_DROP,
        CUCCO_PARTY,
    ], False, False),
    "Misc Useful": ItemGroup(ItemClassification.useful, [
        HEART_PIECE,
        HEART_CONTAINER,
        RED_TUNIC,
        BLUE_TUNIC,
        MAX_POWDER_UPGRADE,
        MAX_BOMBS_UPGRADE,
        MAX_ARROWS_UPGRADE,
    ], False, False),
    "Misc Filler": ItemGroup(ItemClassification.filler, [
        ARROWS_10,
        SINGLE_ARROW,
        MEDICINE,
        GUARDIAN_ACORN,
        PIECE_OF_POWER,
        RECOVERY_HEART,
        FAIRY,
        MESSAGE,
    ], False, False),
}

data_package_only_item_groups: dict[str, list[str]] = {
    "Bush Breakers": [
        POWER_BRACELET,
        MAGIC_ROD,
        MAGIC_POWDER,
        BOMB,
        SWORD,
        BOOMERANG,
    ],
    "Sword": [SWORD],
    "Shield": [SHIELD],
    "Power Bracelet": [POWER_BRACELET],
    "Bracelet": [POWER_BRACELET],
}

links_awakening_items: list[ItemData] = [
    ItemData(item, group.classification)
    for group in item_groups.values()
    for item in group.items
]

ladxr_to_ap_item_name: dict[str, str] = {
    item.ladxr_id: item.item_name for item in links_awakening_items
}

ap_to_ladxr_item_name: dict[str, str] = {v: k for k, v in ladxr_to_ap_item_name.items()}

links_awakening_items_by_name: dict[str, ItemData] = {
    item.item_name: item for item in links_awakening_items
}

links_awakening_item_name_groups: dict[str, set[str]] = {
    group_name: [AP_NAMES[item] for item in group.items]
    for group_name, group in item_groups.items()
    if group.goes_in_datapackage
}
links_awakening_item_name_groups.update({
    group_name: [AP_NAMES[item] for item in items]
    for group_name, items in data_package_only_item_groups.items()
})

item_prefixes_to_skip_text_in_prefill = [
    'HEART',
    'BAD_HEART',
    'RUPEE',
    'BLUE_TUNIC',
    'RED_TUNIC'
    'GEL',
    'KEY',
    'NIGHTMARE_KEY',
    'STONE_BEAK',
    'MAP',
    'COMPASS',
]

start_items_to_block_by_prefix = [
    'GOLD_LEAF',
    'RUPEE',
    'SEASHELL',
    'KEY',
]

rupees = {
    RUPEES_20: 20,
    RUPEES_50: 50,
    RUPEES_100: 100,
    RUPEES_200: 200,
    RUPEES_500: 500,
}

possible_filler = [
    ladxr_to_ap_item_name[item]
    for name, group in item_groups.items()
    for item in group.items
    if name in ['Seashells', 'Traps', 'Misc Filler']
]
possible_filler.extend([ladxr_to_ap_item_name[i] for i in (BOMB, MAGIC_POWDER, RUPEES_20)])
possible_filler.sort()

hint_groups = [name for name, group in item_groups.items() if group.in_game_hintable]
hint_groups.sort()