from enum import Enum
from typing import TYPE_CHECKING, NotRequired, TypedDict

from typing_extensions import Unpack

import worlds.gstla.gen.internal_item_data as ItemLists  # noqa: N812
from BaseClasses import ItemClassification
from worlds.gstla.game_data import ElementType, ItemType
from .internal_item_data import InternalDjinnItemData, InternalEventItemData, InternalItemData
from .item_names import ItemName

if TYPE_CHECKING:
    # TODO: Swap name
    base_item = InternalItemData
    base_djinn = InternalDjinnItemData
    base_event = InternalEventItemData
else:
    base_item = object
    base_djinn = object
    base_event = object


class TrapType(str, Enum):
    Mimic = 'Mimic'


class FillerType(str, Enum):
    ForgeMaterials = 'Forge Materials'
    RustyMaterials = 'Rusty Materials'
    StatBoosts = 'Stat Boosts'
    UsefulConsumables = 'Useful Consumables'
    ForgedEquipment = 'Forged Equipment'
    LuckyEquipment = 'Lucky Equipment'
    ShopEquipment = 'Shop Equipment'
    Coins = 'Coins'
    CommonConsumables = 'Common Consumables'


class ItemDataDict(TypedDict):
    id: NotRequired[int]
    name: NotRequired[str]
    progression: NotRequired[ItemClassification]
    addr: NotRequired[int]
    type: NotRequired[ItemType]
    is_mimic: NotRequired[bool]
    is_rare: NotRequired[bool]


class DjinnDataDict(ItemDataDict):
    element: NotRequired[ElementType]
    vanilla_id: NotRequired[int]
    stats_addr: NotRequired[int]
    stats: NotRequired[list[int]]


class EventDataDict(ItemDataDict):
    flag: NotRequired[int]
    location: NotRequired[str]


class ItemData(base_item):
    def __init__(self, item: InternalItemData, **kwargs: Unpack[ItemDataDict]):
        self._item = item
        self._kwargs = kwargs

    def __getattr__(self, name):
        if name in self._kwargs:
            return self._kwargs[name]  # type: ignore
        return getattr(self._item, name)


class DjinnItemData(ItemData, base_djinn):
    def __init__(self, item: InternalDjinnItemData, **kwargs: Unpack[DjinnDataDict]):
        super().__init__(item, **kwargs)


class EventItemData(ItemData, base_event):
    def __init__(self, item: InternalItemData, **kwargs: Unpack[EventDataDict]):
        super().__init__(item, **kwargs)


_overrides: dict[str, ItemDataDict] = {
    ItemName.Catch_Beads: {'progression': ItemClassification.filler},
    ItemName.Right_Prong: {'progression': ItemClassification.progression_deprioritized_skip_balancing},
    ItemName.Left_Prong: {'progression': ItemClassification.progression_deprioritized_skip_balancing},
    ItemName.Center_Prong: {'progression': ItemClassification.progression_deprioritized_skip_balancing},
    ItemName.Healing_Fungus: {'progression': ItemClassification.progression_deprioritized_skip_balancing},
    ItemName.Red_Cloth: {'progression': ItemClassification.progression_deprioritized_skip_balancing},
    ItemName.Milk: {'progression': ItemClassification.progression_deprioritized_skip_balancing},
}


def _wrap_datum(item: InternalItemData) -> ItemData:
    if item.name in _overrides:
        return ItemData(item, **_overrides[item.name])
    return ItemData(item)


def _wrap_djinn(djinn: InternalDjinnItemData) -> DjinnItemData:
    if djinn.name in _overrides:
        return DjinnItemData(djinn, **_overrides[djinn.name])
    return DjinnItemData(djinn)


def _wrap_event(event: InternalEventItemData) -> EventItemData:
    if event.name in _overrides:
        return EventItemData(event, **_overrides[event.name])
    return EventItemData(event)


def _convert_data(data: list[InternalItemData]) -> list[ItemData]:
    return [_wrap_datum(x) for x in data]


def _convert_djinn(data: list[InternalDjinnItemData]) -> list[DjinnItemData]:
    return [_wrap_djinn(x) for x in data]


def _convert_events(data: list[InternalEventItemData]) -> list[EventItemData]:
    return [_wrap_event(x) for x in data]


summon_list: list[ItemData] = _convert_data(ItemLists.summon_list)

psyenergy_list: list[ItemData] = _convert_data(ItemLists.psyenergy_list)
psyenergy_as_item_list: list[ItemData] = _convert_data(ItemLists.psyenergy_as_item_list)

djinn_items: list[DjinnItemData] = _convert_djinn(ItemLists.djinn_items)
events: list[EventItemData] = _convert_events(ItemLists.events)

characters: list[ItemData] = _convert_data(ItemLists.characters)

mimics: list[ItemData] = _convert_data(ItemLists.mimics)

other_progression: list[ItemData] = _convert_data(ItemLists.other_progression)

useful_consumables: list[ItemData] = _convert_data(ItemLists.useful_consumables)
forge_materials: list[ItemData] = _convert_data(ItemLists.forge_materials)
class_change_items: list[ItemData] = _convert_data(ItemLists.class_change_items)
rusty_items: list[ItemData] = _convert_data(ItemLists.rusty_items)
stat_boosters: list[ItemData] = _convert_data(ItemLists.stat_boosters)
useful_remainder = _convert_data(ItemLists.useful_remainder)

other_useful: list[ItemData] = useful_remainder + useful_consumables + forge_materials + class_change_items

shop_only: list[ItemData] = _convert_data(ItemLists.shop_only)
forge_only: list[ItemData] = _convert_data(ItemLists.forge_only)
lucky_only: list[ItemData] = _convert_data(ItemLists.lucky_only)

non_vanilla: list[ItemData] = _convert_data(ItemLists.non_vanilla)

vanilla_coins: list[ItemData] = _convert_data(ItemLists.vanilla_coins)
misc: list[ItemData] = _convert_data(ItemLists.misc)
remainder: list[ItemData] = _convert_data(ItemLists.remainder)

all_items: list[ItemData] = (
    djinn_items
    + psyenergy_as_item_list
    + psyenergy_list
    + summon_list
    + events
    + characters
    + mimics
    + other_progression
    + other_useful
    + shop_only
    + forge_only
    + lucky_only
    + non_vanilla
    + vanilla_coins
    + misc
    + rusty_items
    + stat_boosters
    + remainder
)
assert len(all_items) == len({x.id for x in all_items})
item_table: dict[str, ItemData] = {item.name: item for item in all_items}
items_by_id: dict[int, ItemData] = {item.id: item for item in all_items}
