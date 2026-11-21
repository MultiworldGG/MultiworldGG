from typing import cast

from .character_items import NON_VEHICLE_CHARACTER_TO_ITEM_DATA, NON_VEHICLE_NORMAL_CHARACTER_TO_ITEM_DATA
from .vehicle_items import ALL_VEHICLE_CHARACTER_TO_ITEM_DATA, VEHICLE_NORMAL_CHARACTER_TO_ITEM_DATA
from . import GenericCharacterData

from ..characters import Character

__all__ = [
    "CHARACTER_TO_ITEM_DATA",
    "NORMAL_CHARACTER_TO_ITEM_DATA",
    "EXTRA_TOGGLE_CHARACTER_TO_ITEM_DATA",
    "SENDABLE_CHARACTER_TO_ITEM_DATA",
    "CODE_TO_ITEM_DATA",
]

CHARACTER_TO_ITEM_DATA: dict[Character, GenericCharacterData] = {
    **NON_VEHICLE_CHARACTER_TO_ITEM_DATA,
    **ALL_VEHICLE_CHARACTER_TO_ITEM_DATA,
}
"""All characters, both normal and those that are specific to the "Extra Toggle" Extra."""

NORMAL_CHARACTER_TO_ITEM_DATA: dict[Character, GenericCharacterData] = {
    **NON_VEHICLE_NORMAL_CHARACTER_TO_ITEM_DATA,
    **VEHICLE_NORMAL_CHARACTER_TO_ITEM_DATA,
}
"""All non-Extra Toggle characters. These characters can be collected into a CollectionState."""

EXTRA_TOGGLE_CHARACTER_TO_ITEM_DATA: dict[Character, GenericCharacterData] = {
    k: v for k, v in CHARACTER_TO_ITEM_DATA.items() if k not in NORMAL_CHARACTER_TO_ITEM_DATA
}
"""
Extra Toggle characters. These characters are never collected into a CollectionState, instead, rules are modified to
check for the Extra Toggle item being collected into a CollectionState if Extra Toggle could satisfy those rules in the
current Area.
"""

SENDABLE_CHARACTER_TO_ITEM_DATA: dict[Character, GenericCharacterData] = {
    k: v for k, v in NORMAL_CHARACTER_TO_ITEM_DATA.items() if v.is_sendable
}
"""All characters that can be created and sent as AP items. This excludes Extra Toggle characters, and event-only
characters e.g Super Gonk Droid."""

CODE_TO_ITEM_DATA: dict[int, GenericCharacterData] = cast(dict[int, GenericCharacterData], {
    v.code: v for v in SENDABLE_CHARACTER_TO_ITEM_DATA.values()
})
