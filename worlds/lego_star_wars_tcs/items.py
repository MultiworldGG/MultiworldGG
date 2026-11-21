from typing import Optional, Mapping, cast

from BaseClasses import Item, ItemClassification
from .constants import GAME_NAME
from .character_ability import CharacterAbility
from .data.characters import Character
from .data.extras import Extra
from .data.items import GenericItemData, GenericCharacterData
from .data.items.all_character_items import CHARACTER_TO_ITEM_DATA
from .data.items.character_items import NORMAL_CHARACTER_DATA
from .data.items.extra_items import EXTRA_DATA, ExtraData
from .data.items.generic_items import GENERIC_DATA
from .data.items.vehicle_items import VEHICLE_DATA


__all__ = [
    "LegoStarWarsTCSItem",
    "ITEM_DATA",
    "ITEM_DATA_BY_NAME",
    "ITEM_DATA_BY_ID",
    "CHARACTERS_AND_VEHICLES_BY_NAME",
    "ITEM_NAME_TO_ID",
    "SUPER_GONK_ITEMS",
    "SUPER_GONK_DROID_ABILITIES_VALUE",
]


class LegoStarWarsTCSItem(Item):
    game = GAME_NAME
    # Most Progression items collect their abilities into the state through a world.collect() override.
    # `collect_abilities_int is not None` is faster than `collect_abilities_int != 0`, so `None` is used instead of `0`.
    collect_abilities_int: int | None
    abilities: CharacterAbility

    def __init__(self, name: str, classification: ItemClassification, code: Optional[int], player: int,
                 abilities: CharacterAbility | None = None):
        super().__init__(name, classification, code, player)
        if abilities is not None and abilities.value != 0:
            self.collect_abilities_int = abilities.value
            self.abilities = abilities
            assert ItemClassification.progression in classification, "All items with abilities should be progression."
        else:
            self.collect_abilities_int = None
            self.abilities = CharacterAbility.NONE


ITEM_DATA: list[GenericItemData] = [
    *NORMAL_CHARACTER_DATA,
    *VEHICLE_DATA,
    *GENERIC_DATA,
    *EXTRA_DATA,
]
ITEM_DATA_BY_NAME: Mapping[str, GenericItemData] = {data.name: data for data in ITEM_DATA}
ITEM_DATA_BY_ID: Mapping[int, GenericItemData] = cast(dict[int, GenericItemData],
                                                      {data.code: data for data in ITEM_DATA if data.is_sendable})
CHARACTERS_AND_VEHICLES_BY_NAME: Mapping[str, GenericCharacterData] = {
    data.name: data for data in ITEM_DATA if isinstance(data, GenericCharacterData)}

ITEM_NAME_TO_ID: dict[str, int] = cast(
    dict[str, int],
    {name: item.code for name, item in ITEM_DATA_BY_NAME.items() if item.is_sendable}
)

SUPER_GONK_ITEMS: tuple[str, str] = (
    CHARACTER_TO_ITEM_DATA[Character.GONK_DROID].name,
    ExtraData.from_extra(Extra.SUPER_GONK).name,
)
SUPER_GONK_DROID_ABILITIES_VALUE: int = (
    CHARACTER_TO_ITEM_DATA[Character.EVENT_SUPER_GONK_DROID].abilities
    # Abilities provided by non-super Gonk Droid can be skipped.
    & ~CHARACTER_TO_ITEM_DATA[Character.GONK_DROID].abilities
).value
