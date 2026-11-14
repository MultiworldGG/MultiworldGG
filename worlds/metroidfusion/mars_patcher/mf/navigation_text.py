from __future__ import annotations

from enum import IntEnum, auto
from typing import TYPE_CHECKING

from .constants.game_data import navigation_text_ptrs
from .constants.reserved_space import ReservedPointersMF
from ..rom import Rom
from ..text import Language, MessageType, encode_text

if TYPE_CHECKING:
    from .auto_generated_types import HintLocks, MarsschemamfNavStationLocksKey
    from ..rom import Rom


class NavRoom(IntEnum):
    MAIN_DECK_WEST = 1
    MAIN_DECK_EAST = auto()
    OPERATIONS_DECK = auto()
    SECTOR_1_ENTRANCE = auto()
    SECTOR_5_ENTRANCE = auto()
    SECTOR_2_ENTRANCE = auto()
    SECTOR_4_ENTRANCE = auto()
    SECTOR_3_ENTRANCE = auto()
    SECTOR_6_ENTRANCE = auto()
    AUXILIARY_POWER = auto()
    RESTRICTED_LABS = auto()


# Later down the line, when/if Nav terminals don't have their
# confirm text patched out, combine these two.
class ShipText(IntEnum):
    INITIAL_TEXT = 0
    CONFIRM_TEXT = auto()


class NavStationLockType(IntEnum):
    OPEN = 0xFF
    LOCKED = 0x05
    GREY = 0x00
    BLUE = 0x01
    GREEN = 0x02
    YELLOW = 0x03
    RED = 0x04


class NavigationText:
    GAME_START_CHAR = "[GAME_START]"
    NAV_TERMINALS_KEY = "navigation_terminals"
    SHIP_TEXT_KEY = "ship_text"

    def __init__(self, navigation_text: dict[Language, dict[str, dict[IntEnum, str]]]):
        self.navigation_text = navigation_text

    @classmethod
    def from_json(cls, data: dict) -> NavigationText:
        navigation_text: dict[Language, dict[str, dict[IntEnum, str]]] = {}
        for lang, lang_text in data.items():
            lang = Language[lang]
            navigation_text[lang] = {
                cls.NAV_TERMINALS_KEY: {
                    NavRoom[k]: v for k, v in lang_text[cls.NAV_TERMINALS_KEY].items()
                },
                cls.SHIP_TEXT_KEY: {
                    # Make sure initial text string starts with [GAME_START]
                    ShipText[k]: cls.GAME_START_CHAR + v
                    if k == ShipText.INITIAL_TEXT.name and not v.startswith(cls.GAME_START_CHAR)
                    else v
                    for k, v in lang_text[cls.SHIP_TEXT_KEY].items()
                },
            }
        return cls(navigation_text)

    def write(self, rom: Rom) -> None:
        for lang, lang_texts in self.navigation_text.items():
            base_text_address = rom.read_ptr(navigation_text_ptrs(rom) + lang.value * 4)

            # Info Text
            for info_place, text in lang_texts["ship_text"].items():
                encoded_text = encode_text(rom, MessageType.CONTINUOUS, text)
                text_ptr = base_text_address + info_place.value * 4
                rom.write_data_with_pointers(encoded_text, [text_ptr, text_ptr + 4])

            # Navigation Text
            for nav_room, text in lang_texts["navigation_terminals"].items():
                encoded_text = encode_text(rom, MessageType.CONTINUOUS, text)
                text_ptr = base_text_address + nav_room.value * 8
                rom.write_data_with_pointers(encoded_text, [text_ptr, text_ptr + 4])

    @classmethod
    def apply_hint_security(
        cls, rom: Rom, locks: dict[MarsschemamfNavStationLocksKey, HintLocks]
    ) -> None:
        """
        Applies an optional security level requirement to use Navigation Stations
        Defaults to OPEN if not provided in patch data JSON
        """
        locks_values = {NavRoom[k]: NavStationLockType[v] for k, v in locks.items()}
        default_lock = NavStationLockType.OPEN
        for location in NavRoom:
            rom.write_8(
                rom.read_ptr(ReservedPointersMF.HINT_SECURITY_LEVELS_ADDR.value) + location.value,
                locks_values.get(location, default_lock).value,
            )
