from .data.ItemList import item_table
import typing

from BaseClasses import Item, ItemClassification

"""Paper Mario came out August 11th, 2000 (in Japan)"""
item_id_prefix = 8112000000


def pm_data_to_ap_id(data, event):
    # if
    if event or data[6]:
        return None
    if data[0] in [
        "KEYITEM",
        "ITEM",
        "BADGE",
        "STARPIECE",
        "POWERSTAR",
        "COIN",
        "GEAR",
        "PARTNER",
        "OTHER",
        "PARTNERUPGRADE",
        "NOTHING",
        "STARPOWER"
    ]:
        return item_id_prefix + data[2]
    else:
        raise Exception(f"Unexpected PM item type found: {data[0]}")


def ap_id_to_pm_data(ap_id):
    val = ap_id - item_id_prefix
    try:
        return list(filter(lambda d: d[1][2] == val, item_table.items()))[0]
    except IndexError:
        raise Exception(f"Could not find desired item ID: {ap_id}")


def item_id_to_item_name(item_id):
    try:
        return list(filter(
            lambda d: d[1][0] == 'Item' and d[1][2] == item_id,
            item_table.items()
        ))[0][0]
    except IndexError:
        raise Exception(f"Could not find desired item ID: {item_id}")


def pm_is_item_of_type(item, item_type):
    if isinstance(item, PMItem):
        return item.type == item_type
    if isinstance(item, str):
        return item in item_table and item_table[item][0] == item_type
    return False


class PMItem(Item):
    game: str = "Paper Mario"
    type: str

    def __init__(self, name, player, data, event):
        (type, progression, id, base_price, unused, unused_dupe, unplaceable) = data

        if name == "Trap":
            classification = ItemClassification.trap
        else:
            classification = progression
        super(PMItem, self).__init__(name, classification, pm_data_to_ap_id(data, event), player)
        self.type = type
        self.id = id
        self.base_price = base_price
        self.unused = unused
        self.unused_dupe = unused_dupe
        self.unplaceable = unplaceable
        self.internal = False
