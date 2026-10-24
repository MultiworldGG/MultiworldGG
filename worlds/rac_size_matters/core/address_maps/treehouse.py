"""Bind Treehouse to the relocated overlay, rather than an assumed load base."""

import struct
from dataclasses import fields, replace


# Distances from the unique movement-state reference in each LEVEL_24.REL.
# Source excerpts are retained in test/fixtures/treehouse_addresses.json.
_LAYOUT = {
    "SCUS-97615": (-0xDDCC, 0x100F5B),
    "SCES-55019": (-0xDE74, 0x1016B3),
    "SCPS-15120": (-0xDF4C, 0x109003),
}


def resolve(game_id, mapped, code_start, code):
    menu_distance, weapon_distance = _LAYOUT[game_id]
    hits = []
    for offset in range(0, len(code) - 11, 4):
        high, middle, low = struct.unpack_from("<3I", code, offset)
        if high & 0xFFFF0000 == 0x3C020000 and middle == 0x2404000D and low & 0xFFFF0000 == 0x84430000:
            hits.append(offset)
    if len(hits) != 1:
        raise RuntimeError("Expected one Treehouse player-state reference")
    offset = hits[0]

    def target(at, expected):
        if not 0 <= at <= len(code) - 12:
            raise RuntimeError("Truncated Treehouse address reference")
        high, middle, low = struct.unpack_from("<3I", code, at)
        if (high & 0xFFFF0000, middle, low & 0xFFFF0000) != expected:
            raise RuntimeError("Treehouse address reference changed")
        immediate = low & 0xFFFF
        return ((high & 0xFFFF) << 16) + (immediate if immediate < 0x8000 else immediate - 0x10000)

    player = target(offset, (0x3C020000, 0x2404000D, 0x84430000))
    menu = target(offset + menu_distance, (0x3C030000, 0x03E00008, 0x8C620000))
    shift = player - mapped.player_state
    weapon = code_start + offset + weapon_distance
    if menu != mapped.menu + shift or weapon != mapped.weapon_array + shift:
        raise RuntimeError("Treehouse relocated address references disagree")
    # Every populated Treehouse address belongs to this overlay (no save flags).
    updates = {field.name: getattr(mapped, field.name) + shift for field in fields(mapped)
               if field.name != "name" and getattr(mapped, field.name) is not None}
    if any(not 0x100000 <= value < 0x1E00000 for value in updates.values()):
        raise RuntimeError("Treehouse addresses outside level memory")
    return replace(mapped, **updates)
