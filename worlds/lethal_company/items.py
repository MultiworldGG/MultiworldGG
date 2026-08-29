import math

from BaseClasses import Item, ItemClassification
from typing import Dict, Any, TYPE_CHECKING, Tuple, List
from .locations import generate_locations
from .imported import data
from .custom_content import custom_content

if TYPE_CHECKING:
    from . import LethalCompanyWorld


class LethalCompanyItem(Item):
    game: str = f"Lethal Company{custom_content['name']}"


class SlotItemData:
    def __init__(self):
        self.environment_pool: Dict[str, int] = {}
        self.moons: List[str] = []
        self.shop_items: List[str] = []
        self.classification_table: Dict[str, ItemClassification] = {}
        self.filler_items: Dict[str, int] = {}


class LCItem:
    id = 1966720

    def __init__(self, slot_item_data: SlotItemData, name, count_mode=0, count_arg: Any = 1, environment=False,
                 classification=ItemClassification.progression, shop_item=False):
        self.name = name
        if self.name in item_table.keys():
            self.item_id = item_table[self.name]
        else:
            self.item_id = LCItem.id
            LCItem.id += 1
        self.count_mode = count_mode
        self.count_arg = count_arg
        self.slot_item_data = slot_item_data
        item_table.update({self.name: self.item_id})
        if environment:
            slot_item_data.environment_pool[self.name] = self.item_id
            slot_item_data.moons.append(self.name)
        if shop_item:
            slot_item_data.shop_items.append(self.name)
        slot_item_data.classification_table[self.name] = classification

    def create_item(self, lcworld: "LethalCompanyWorld"):
        names = []
        if self.count_mode == 0:
            # arg is # of item
            for i in range(self.count_arg):
                names.append(self.name)
        elif self.count_mode == 1:
            # arg is name of option that contains the count of the item
            for i in range(getattr(lcworld.options, self.count_arg).value):
                names.append(self.name)
        elif self.count_mode == 2:
            # arg is a lambda function that takes in the multiworld and outputs a number
            for i in range(self.count_arg(lcworld)):
                names.append(self.name)
        elif self.count_mode == 3:
            # used for filler items
            self.slot_item_data.filler_items.update({self.name: getattr(lcworld.options, self.count_arg).value})
            return []
        return names


def calculate_credits(world: "LethalCompanyWorld"):
    if not world.options.game_mode.value == 2:
        return 0

    location_count = world.location_count
    location_count -= 7
    location_count -= world.options.randomize_company_building.value
    location_count -= world.options.randomize_scanner.value
    location_count -= world.options.randomize_terminal.value
    location_count -= (4 - world.options.starting_stamina_bars.value)
    location_count -= (4 - world.options.starting_inventory_slots.value)
    location_count -= 16

    credit_count = math.ceil(location_count * (world.options.credit_replacement/100.0))
    world.required_credit_count = round(credit_count * (world.options.required_credits/100.0))
    return credit_count


item_table: Dict[str, int] = {}


def get_default_item_map():
    generate_items(data)
    return item_table


def generate_items(imported_data) -> Tuple[List[LCItem], SlotItemData]:
    slot_item_data = SlotItemData()

    items = [
        LCItem(slot_item_data, "LoudHorn", classification=ItemClassification.useful),
        LCItem(slot_item_data, "SignalTranslator", classification=ItemClassification.useful),
        LCItem(slot_item_data, "Teleporter", classification=ItemClassification.useful),
        LCItem(slot_item_data, "InverseTeleporter", classification=ItemClassification.useful),
        LCItem(slot_item_data, "Company Building", 1, "randomize_company_building",
               classification=ItemClassification.progression),
        LCItem(slot_item_data, "Terminal", 1, "randomize_terminal", classification=ItemClassification.progression),
        LCItem(slot_item_data, "Inventory Slot", 2, lambda w: 4 - w.options.starting_inventory_slots.value,
               classification=ItemClassification.progression),
        LCItem(slot_item_data, "Stamina Bar", 2, lambda w: 4 - w.options.starting_stamina_bars.value,
               classification=ItemClassification.progression),
        LCItem(slot_item_data, "Company Credit", 2, calculate_credits, classification=ItemClassification.progression),
        LCItem(slot_item_data, "Strength Training", 3, "weight_reducers",
               classification=ItemClassification.filler),
        LCItem(slot_item_data, "Scanner", 1, "randomize_scanner", classification=ItemClassification.progression),
        LCItem(slot_item_data, "Money", 3, "money", classification=ItemClassification.filler),
        LCItem(slot_item_data, "More Time", 3, "time_add", classification=ItemClassification.filler),
        LCItem(slot_item_data, "Clone Scrap", 3, "scrap_clone", classification=ItemClassification.filler),
        LCItem(slot_item_data, "Birthday Gift", 3, "birthday", classification=ItemClassification.filler),
        LCItem(slot_item_data, "HauntTrap", 3, "haunt_trap", classification=ItemClassification.trap),
        LCItem(slot_item_data, "BrackenTrap", 3, "bracken_trap", classification=ItemClassification.trap),
        LCItem(slot_item_data, "Less Time", 3, "time_trap", classification=ItemClassification.trap)
    ]

    for item in imported_data.get("store"):
        if "shovel" in item.casefold() or "jetpack" in item.casefold() or "ladder" in item.casefold():
            items.append(LCItem(slot_item_data, item, shop_item=True))
        else:
            items.append(LCItem(slot_item_data, item, classification=ItemClassification.useful, shop_item=True))

    for item in imported_data.get("vehicles"):
        items.append(LCItem(slot_item_data, item, classification=ItemClassification.useful, shop_item=True))

    for moon in imported_data.get("moons"):
        items.append(LCItem(slot_item_data, moon, environment=True))

    return items, slot_item_data
