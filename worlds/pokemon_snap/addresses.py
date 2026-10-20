"""Game memory addresses for the client, loaded from the ROM build's export.

`pokemonsnap.symbols.json` is emitted by the decomp build (tools/export_symbols.py)
and copied here, so the addresses stay in sync with the ROM.
"""
import json
from importlib.resources import files
from .constants import *

_data = json.loads(
    files(__package__).joinpath("data/pokemonsnap.symbols.json").read_text(encoding="utf-8")
)


def _addr(section: str, name: str) -> int:
    return int(_data[section][name]["addr"], 16)


def _ident(name: str):
    e = _data["idents"][name]
    return int(e["addr"], 16), int(e["rom_offset"], 16), e["len"]


# Expansion interface (volatile, written by the client to drive unlocks)
EXPANSION_MAGIC = _addr("symbols", "gExpansionMagic")
MAX_FILM = _addr("symbols", "gMaxFilm")
CAN_USE_OVERRIDE = _addr("symbols", "gCanUseOverride")
CAN_USE_MASK = _addr("symbols", "gCanUseMask")
CAN_USE_PER_COURSE_MASK = _addr("symbols", "gCanUsePerLevelMask")
COURSE_OVERRIDE = _addr("symbols", "gCourseOverride")
COURSE_UNLOCK_MASK = _addr("symbols", "gCourseUnlockMask")
DIALOG_REQUEST_FLAGS = _addr("symbols", "gDialogRequestFlags")
DIALOG_PLAYED_FLAGS = _addr("symbols", "gDialogPlayedFlags")
CAMERA_INVERSION = _addr("symbols", "gCameraInversionYAMLOption")
LEVEL_ID = _addr("symbols", "gLevelID")

# Camera inversion constants from the ROM
CAMERA_INVERSION_OPTION_INVERTED = 0
CAMERA_INVERSION_OPTION_NORMAL   = 1

# Vanilla save block (read-only)
SAVE_BASE = _addr("save", "saveBase")
RANK = _addr("save", "rank")
REPORT_SCORES = _addr("save", "reportScores")
SPECIES_SCORES = _addr("symbols", "speciesScores")
SIGN_FLAGS = _addr("symbols", "signsFound")
SECRET_EXIT_FLAGS = _addr("symbols", "secretExits")

# Per-seed auth token: RAM addr (read), ROM offset (write), length.
AUTH_ADDR, AUTH_ROM, AUTH_LEN = _ident("auth")
UNPATCHED_AUTH = b"PSAP-UNPATCHED!!"

# gExpansionMagic reads as 'OKAY' once the expansion segment has booted.
EXPANSION_LOADED = 0x4F4B4159

# 63 snappable Pokemon + 10 extra for pokemon that appear in multiple levels
NUM_SPECIES_SCORES = 73
NUM_SIGNS = 6

# Photographing Mew (the last species) is the goal.
MEW_LOCATION = 63

# Item name -> bit in gCanUseMask.
CAN_USE_BITS = {
    POKEMON_FOOD:  0,
    APPLE:         0,
    PESTER_BALL:   1,
    POKEFLUTE:     2,
    DASH_ENGINE:   3,
    SIGN_DETECTOR: 4,
    L_TO_STOP:     5,
    WDFL_SCORING:  6,
    MULT_SCORING:  7,
    MULT_WO_WDFL:  8,
}

CAN_USE_FLAGS = {name: (1 << CAN_USE_BITS[name]) for name in CAN_USE_BITS}
CAN_USE_PER_COURSE_FLAGS = {course(name, level): (i, 1 << CAN_USE_BITS[name]) for name in CAN_USE_BITS for i, level in enumerate(ALL_LEVELS)}

# Item name -> bit in gCourseUnlockMask.
COURSE_IDS = {
    LVL_BEACH:   0,
    LVL_TUNNEL:  1,
    LVL_VOLCANO: 2,
    LVL_RIVER:   3,
    LVL_CAVE:    4,
    LVL_VALLEY:  5,
    LVL_CLOUD:   6,
}
