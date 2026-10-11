"""Compatibility fallback for clients without the native armour journal."""

from __future__ import annotations

from ..pypine import Pine
from . import address_maps
from .patches import asm as m

_GATE_ANCHOR = bytes.fromhex("781c628c2b1045002f004014")


def _scan(pine: Pine, pattern: bytes, start: int = 0, end: int = 0x02000000, chunk: int = 0x10000) -> int | None:
    if not pattern or chunk < len(pattern):
        raise ValueError("Scan chunk must contain the whole pattern")
    overlap = len(pattern) - 1
    addr = start
    while addr < end:
        length = min(chunk, end - addr)
        data = pine.read_bytes(addr, length)
        idx = data.find(pattern)
        if idx != -1:
            return addr + idx
        if addr + length == end:
            break
        addr += length - overlap
    return None


class ArmourSpawnGate:
    """Bypass only ArmorPickup::Init's story-tier branch.

    The previous scratch-pointer approach overwrote the pickup's required-tier
    load, whose location had been mistaken for a LUI instruction. A NOP of the
    conditional branch leaves both data loads and the collected-piece gate intact.
    NativeRuntime installs this bypass before object initialization as part of
    the independent armour pickup journal; this is the legacy late-attach fallback.
    """

    def __init__(self, pine: Pine):
        self.pine = pine
        self.last_applied_planet_id = None

    def apply(self, planet_id: int | None) -> bool:
        if self.pine.get_game_id() != address_maps.GAME_ID:
            return False
        anchor = _scan(self.pine, _GATE_ANCHOR)
        if anchor is None:
            self.last_applied_planet_id = None
            return False
        self.pine.write_int32(anchor + 8, m.NOP)
        if self.pine.read_int32(anchor + 8) != m.NOP:
            raise RuntimeError("Armour spawn gate readback failed")
        self.last_applied_planet_id = planet_id
        return True
