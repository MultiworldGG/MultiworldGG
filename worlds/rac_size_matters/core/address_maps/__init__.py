"""PS2 address maps selected from the detected PINE serial before memory access.

Dictionary identities stay stable for inventories that import lookup tables.
Selection is synchronous and must run under the client's PINE lock.
"""
import os as _os
from . import us_addresses, eu_addresses, jp_addresses

SUPPORTED_GAMES = {"SCUS-97615": "US", "SCES-55019": "EU", "SCPS-15120": "JP"}
_MAPS = {"SCUS-97615": us_addresses, "SCES-55019": eu_addresses, "SCPS-15120": jp_addresses}
GAME_ID = ""


def select_game(game_id: str) -> None:
    """Select a verified map; reject unsupported serials before changing anything."""
    if game_id not in _MAPS:
        raise ValueError(f"Unsupported Size Matters serial: {game_id!r}")
    _load_map(_MAPS[game_id], game_id)


def _publish(name, value):
    previous = globals().get(name)
    if isinstance(value, dict):
        if isinstance(previous, dict):
            previous.clear()
            previous.update(value)
            return
        value = dict(value)
    globals()[name] = value


def _load_map(module, game_id):
    global GAME_ID
    for name, value in vars(module).items():
        if name.isupper():
            _publish(name, value)
    GAME_ID = game_id
    _derive_tables()


def _derive_tables():
    PLAYER_ADDRS: dict[int, tuple[int, int]] = {
        pid: (p.player_state, p.player_health) for pid, p in PLANET_ADDRESSES.items()
    }

    MENU_ADDR_BY_PLANET_ID: dict[int, int] = {
        pid: p.menu for pid, p in PLANET_ADDRESSES.items() if p.menu is not None
    }

    MAX_HEALTH_ADDR_BY_PLANET_ID: dict[int, int] = {
        pid: p.max_health for pid, p in PLANET_ADDRESSES.items() if p.max_health is not None
    }

    WEAPON_ARRAY_BASE_BY_PLANET: dict[int, int] = {
        pid: p.weapon_array for pid, p in PLANET_ADDRESSES.items() if p.weapon_array is not None
    }

    PLANET_MISSION_ADDRESSES: dict[str, int] = {
        p.name: p.mission for p in PLANET_ADDRESSES.values() if p.mission is not None
    }

    SMALL_TEXT_BOX_BY_PLANET: dict[int, int] = {
        pid: p.small_text_box for pid, p in PLANET_ADDRESSES.items() if p.small_text_box is not None
    }

    MULTI_LINE_TEXT_BOX_BY_PLANET: dict[int, int] = {
        pid: p.multi_line_text_box for pid, p in PLANET_ADDRESSES.items() if p.multi_line_text_box is not None
    }

    WEAPON_CYCLER_ADDRS_BY_PLANET: dict[int, tuple[int, int, int, int]] = {
        pid: (p.weapon_cycler_apply, p.weapon_cycler_state, p.weapon_cycler_current, p.weapon_cycler_stored)
        for pid, p in PLANET_ADDRESSES.items()
        if p.weapon_cycler_apply is not None and p.weapon_cycler_state is not None
        and p.weapon_cycler_current is not None and p.weapon_cycler_stored is not None
    }
    for name, value in locals().copy().items():
        _publish(name, value)


def save_address(canonical_address: int) -> int:
    """Resolve a location definition's US save address in the active save block.

    Location IDs and lookup keys remain region-independent; only memory I/O
    uses this translated address. The relative save layout is shared.
    """
    if not 0x1F4AB00 <= canonical_address < 0x1F4C800:
        raise ValueError(f"Not a canonical save address: {canonical_address:#x}")
    return canonical_address + ARMOUR_BASE - 0x1F4B354


class Address:
    """Resolve a class-level MemoryStruct address from the current map."""
    def __init__(self, name, offset=0):
        self.name = name
        self.offset = offset

    def __get__(self, instance, owner):
        return globals()[self.name] + self.offset


_platform = _os.environ.get("RACSM_PLATFORM", "us").lower()
if _platform == "psp":
    from . import psp
    _load_map(psp, "SCUS-97615")
elif _platform in ("us", "eu", "jp"):
    select_game({"us": "SCUS-97615", "eu": "SCES-55019", "jp": "SCPS-15120"}[_platform])
else:
    raise ValueError(f"Unsupported RACSM_PLATFORM: {_platform!r}")
