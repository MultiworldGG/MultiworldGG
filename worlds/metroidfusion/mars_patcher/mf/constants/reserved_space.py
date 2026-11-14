from enum import IntEnum, auto

from typing_extensions import Self


class ReservedConstantsMF:
    """
    These are constants that are in the ROM's 'Reserved Space';
    things that are intended to be modified by this patcher.
    """

    # These need to be kept in sync with the base patch
    # found somewhere around https://github.com/MetroidAdvRandomizerSystem/MARS-Fusion/blob/main/src/main.s#L48

    RANDO_POINTERS_ADDR = 0x7FF000

    # Pointers, offset by language value, that store the message table location
    MESSAGE_TABLE_LOOKUP_ADDR = 0x79CDF4
    FIRST_CUSTOM_MESSAGE_ID = 0x39  # The first 0x38 messages are reserved for standard messages

    PATCHER_FREE_SPACE_ADDR = 0x7D0000
    PATCHER_FREE_SPACE_END = PATCHER_FREE_SPACE_ADDR + 0x20000


class ReservedPointersMF(IntEnum):
    """
    These are pointers that are in the ROM's 'Reserved Space';
    things that are intended to be modified by this patcher.
    """

    MINOR_LOCS_TABLE_ADDR = 0
    MINOR_LOCS_ARRAY_ADDR = auto()
    MAJOR_LOCS_POINTER_ADDR = auto()
    TANK_INC_ADDR = auto()
    METROID_PARAMETERS_ADDR = auto()
    STARTING_LOCATION_ADDR = auto()
    CREDITS_PARAMETERS_ADDR = auto()  # Unused. Remnant of when we didn't have looping credits music
    HINT_SECURITY_LEVELS_ADDR = auto()
    ENVIRONMENTAL_HAZARD_DAMAGE_ADDR = auto()
    MISSILE_LIMIT_ADDR = auto()
    ROOM_NAMES_TABLE_ADDR = auto()
    REVEAL_HIDDEN_TILES_ADDR = auto()
    TITLE_SCREEN_TEXT_POINTERS_POINTER_ADDR = auto()
    DEFAULT_STEREO_FLAG_POINTER_ADDR = auto()
    INSTANT_MORPH_FLAG_POINTER_ADDR = auto()
    USE_ALTERNATIVE_HUD_DISPLAY = auto()
    GADORA_BEAMS_TABLE_POINTER = auto()
    ZAZABI_ADDITIONAL_DELAY_POINTER = auto()
    YAKUZA_ROUNDS_POINTER = auto()
    USE_TOGGLE_FOR_SECONDARY_WEAPON_SELECTION = auto()

    def __new__(cls, offset: int) -> Self:
        obj = int.__new__(cls)
        obj._value_ = ReservedConstantsMF.RANDO_POINTERS_ADDR + (offset * 4)
        return obj
