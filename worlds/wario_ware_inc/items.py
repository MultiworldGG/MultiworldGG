import typing

from BaseClasses import Item, ItemClassification
from .enums import Items
from .constants import *
from .stage_data import microgame_data, game_data

class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    classsification: ItemClassification
    quantity: int = 1

class WarioWareItem(Item):
    game = GAME_NAME

# Item tables
generic_items = {
    Items.flower:                   ItemData(MISC | 0x01, ItemClassification.progression_deprioritized_skip_balancing),
    Items.beep:                     ItemData(MISC | 0x02, ItemClassification.filler),
    Items.introduction_bundle:      ItemData(BUNDLES | 0x000, ItemClassification.progression | ItemClassification.useful),
    Items.jimmy_bundle:             ItemData(BUNDLES | 0x001, ItemClassification.progression | ItemClassification.useful),
    Items.dribble_bundle:           ItemData(BUNDLES | 0x002, ItemClassification.progression | ItemClassification.useful),
    Items.mona_bundle:              ItemData(BUNDLES | 0x003, ItemClassification.progression | ItemClassification.useful),
    Items.nine_volt_bundle:         ItemData(BUNDLES | 0x004, ItemClassification.progression | ItemClassification.useful),
    Items.orbulon_bundle:           ItemData(BUNDLES | 0x005, ItemClassification.progression | ItemClassification.useful),
    Items.crygor_bundle:            ItemData(BUNDLES | 0x006, ItemClassification.progression | ItemClassification.useful),
    Items.kat_bundle:               ItemData(BUNDLES | 0x007, ItemClassification.progression | ItemClassification.useful),
    Items.wario_bundle:             ItemData(BUNDLES | 0x008, ItemClassification.progression | ItemClassification.useful),
    Items.glitched:                 ItemData(None, ItemClassification.progression_deprioritized_skip_balancing),
}

game_items = {}
for game_name, game_id in game_data.items():
    game_items[f"{game_name.value}"] = ItemData(STAGES | game_id, ItemClassification.progression)

microgame_items = {}
for microgame_name, microgame_id in microgame_data.items():
    microgame_items[f"{microgame_name.value} Microgame"] = ItemData(MICROGAME | microgame_id, ItemClassification.progression_deprioritized)

all_items = generic_items | game_items | microgame_items

item_groups = {
    "Microgame Bundle": {
        Items.introduction_bundle.value,
        Items.jimmy_bundle.value,
        Items.dribble_bundle.value,
        Items.mona_bundle.value,
        Items.nine_volt_bundle.value,
        Items.orbulon_bundle.value,
        Items.crygor_bundle.value,
        Items.kat_bundle.value,
        Items.wario_bundle.value,
    },
    "Microgames": {f"{microgame_name.value} Microgame" for microgame_name in list(microgame_data.keys())}
}
