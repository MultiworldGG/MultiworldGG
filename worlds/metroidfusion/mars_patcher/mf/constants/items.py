from enum import IntEnum, auto
from typing import Any, Final


class MajorSource(IntEnum):
    MAIN_DECK_DATA = 0
    ARACHNUS = auto()
    CHARGE_CORE_X = auto()
    LEVEL_1 = auto()
    TRO_DATA = auto()
    ZAZABI = auto()
    SERRIS = auto()
    LEVEL_2 = auto()
    PYR_DATA = auto()
    MEGA_X = auto()
    LEVEL_3 = auto()
    ARC_DATA_1 = auto()
    WIDE_CORE_X = auto()
    ARC_DATA_2 = auto()
    YAKUZA = auto()
    NETTORI = auto()
    NIGHTMARE = auto()
    LEVEL_4 = auto()
    AQA_DATA = auto()
    WAVE_CORE_X = auto()
    RIDLEY = auto()
    BOILER = auto()
    ANIMALS = auto()
    AUXILIARY_POWER = auto()


class ItemType(IntEnum):
    UNDEFINED = -1
    NONE = 0
    LEVEL_0 = auto()
    MISSILES = auto()
    MORPH_BALL = auto()
    CHARGE_BEAM = auto()
    LEVEL_1 = auto()
    BOMBS = auto()
    HI_JUMP = auto()
    SPEED_BOOSTER = auto()
    LEVEL_2 = auto()
    SUPER_MISSILES = auto()
    VARIA_SUIT = auto()
    LEVEL_3 = auto()
    ICE_MISSILES = auto()
    WIDE_BEAM = auto()
    POWER_BOMBS = auto()
    SPACE_JUMP = auto()
    PLASMA_BEAM = auto()
    GRAVITY_SUIT = auto()
    LEVEL_4 = auto()
    DIFFUSION_MISSILES = auto()
    WAVE_BEAM = auto()
    SCREW_ATTACK = auto()
    ICE_BEAM = auto()
    MISSILE_TANK = auto()
    ENERGY_TANK = auto()
    POWER_BOMB_TANK = auto()
    ICE_TRAP = auto()
    INFANT_METROID = auto()

    def __le__(self, other: Any) -> bool:
        if isinstance(other, ItemType):
            return self.value <= other.value
        return NotImplemented


class ItemSprite(IntEnum):
    UNCHANGED = -1
    EMPTY = 0
    LEVEL_0 = auto()
    MISSILES = auto()
    MORPH_BALL = auto()
    CHARGE_BEAM = auto()
    LEVEL_1 = auto()
    BOMBS = auto()
    HI_JUMP = auto()
    SPEED_BOOSTER = auto()
    LEVEL_2 = auto()
    SUPER_MISSILES = auto()
    VARIA_SUIT = auto()
    LEVEL_3 = auto()
    ICE_MISSILES = auto()
    WIDE_BEAM = auto()
    POWER_BOMBS = auto()
    SPACE_JUMP = auto()
    PLASMA_BEAM = auto()
    GRAVITY_SUIT = auto()
    LEVEL_4 = auto()
    DIFFUSION_MISSILES = auto()
    WAVE_BEAM = auto()
    SCREW_ATTACK = auto()
    ICE_BEAM = auto()
    MISSILE_TANK = auto()
    ENERGY_TANK = auto()
    POWER_BOMB_TANK = auto()
    ANONYMOUS = auto()
    SHINY_MISSILE_TANK = auto()
    SHINY_POWER_BOMB_TANK = auto()
    INFANT_METROID = auto()
    SAMUS_HEAD = auto()
    WALLJUMP_BOOTS = auto()
    RANDOVANIA = auto()
    ARCHIPELAGO_COLOR = auto()
    ARCHIPELAGO_MONOCHROME = auto()


KEY_MAJOR_LOCS: Final = "major_locations"
KEY_MINOR_LOCS: Final = "minor_locations"
KEY_AREA: Final = "area"
KEY_ROOM: Final = "room"
KEY_SOURCE: Final = "source"
KEY_BLOCK_X: Final = "block_x"
KEY_BLOCK_Y: Final = "block_y"
KEY_HIDDEN: Final = "hidden"
KEY_ORIGINAL: Final = "original"
KEY_ITEM: Final = "item"
KEY_ITEM_SPRITE: Final = "item_sprite"
KEY_ITEM_MESSAGES: Final = "item_messages"
KEY_ITEM_JINGLE: Final = "jingle"


class ItemJingle(IntEnum):
    MINOR = 0
    MAJOR = auto()


BEAM_FLAGS = {"CHARGE_BEAM": 1, "WIDE_BEAM": 2, "PLASMA_BEAM": 4, "WAVE_BEAM": 8, "ICE_BEAM": 0x10}
MISSILE_BOMB_FLAGS = {
    "MISSILES": 1,
    "SUPER_MISSILES": 2,
    "ICE_MISSILES": 4,
    "DIFFUSION_MISSILES": 8,
    "BOMBS": 0x10,
    "POWER_BOMBS": 0x20,
}
SUIT_MISC_FLAGS = {
    "HI_JUMP": 1,
    "SPEED_BOOSTER": 2,
    "SPACE_JUMP": 4,
    "SCREW_ATTACK": 8,
    "VARIA_SUIT": 0x10,
    "GRAVITY_SUIT": 0x20,
    "MORPH_BALL": 0x40,
    "SA_X_SUIT": 0x80,
}
