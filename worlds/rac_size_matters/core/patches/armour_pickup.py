"""Separate physical armour pickups from AP-granted/equipped armour."""

import struct

from . import asm as m
from .asm import Patch, branch, jump, packed
from .plan import Plan, supported_game_id


def prepare(pine, *, code_start, code, locations, checked=(), bypass_tier_gate=True):
    game_id = supported_game_id(pine)
    anchor = packed(0x8C621C78, 0x0045102B, 0x1440002F)
    hits = [i for i in range(0, len(code) - len(anchor), 4) if code[i : i + len(anchor)] == anchor]
    if not hits:
        return None
    if len(hits) != 1:
        raise RuntimeError("Ambiguous armour pickup class")
    gate = code_start + hits[0]

    def read(address, count):
        offset = address - code_start
        if not 0 <= offset <= len(code) - count:
            raise RuntimeError("Armour code outside loaded module")
        return code[offset : offset + count]

    def require(address, data):
        if read(address, len(data)) != data:
            raise RuntimeError(f"Armour pickup signature changed at {address:#x}")

    def target(address):
        (word,) = struct.unpack("<I", read(address, 4))
        if word >> 26 != 3:
            raise RuntimeError("Armour pickup call changed")
        return (word & 0x3FFFFFF) << 2

    getter_site = gate - 28
    target(getter_site)
    require(getter_site + 4, packed(0x92240046, 0x14400036, 0x2402FFFF))
    # Init -> Update -> Give, all validated independently before using offsets.
    give = gate + 0x6B4
    require(give, packed(0x27BDFF90))
    require(give + 0x38, packed(0x92440046, 0x3A260001, 0x24050001))
    target(give + 0x44)
    require(give + 0x48, packed(0x30C600FF))
    target(give + 0xA4)
    require(give + 0xA8, packed(0x0200202D))
    target(give + 0xB0)
    require(
        give + 0x130,
        packed(0xDFB00040, 0xDFB10048, 0xDFB20050, 0xDFB30058, 0xDFB40060, 0xDFBF0068, 0x03E00008, 0x27BD0070),
    )
    table = give + 0x54
    get = table + 32
    record = get + 20
    flags = bytearray([2] * 32)
    for slot, name in locations.items():
        if type(slot) is not int or not 0 <= slot < 28:
            raise ValueError("Invalid native armour id")
        flags[slot] = 2 if name in checked else 1
    # v0 = hi(table) + a0 (item id), via the classic lui/addu-then-offset split
    # (+0x8000 compensates for the offset's sign-extension when its top bit is set).
    prefix = [m.lui(m.V0, (table + 0x8000) >> 16), m.addu(m.V0, m.V0, m.A0)]  # Load upper immediate; Add registers.
    arena = bytes(flags) + packed(
        *prefix,
        m.lbu(m.V0, table & 0xFFFF, m.V0),  # Load V0 from V0 + table & 65535.
        m.jr(m.RA),  # Jump to RA.
        m.addiu(m.V0, m.V0, -1),  # Set V0 to V0 + -1.
    )  # Jump to register; Add signed immediate.
    arena += packed(
        *prefix,
        m.addiu(m.V1, m.ZERO, 2),  # Set V1 to ZERO + 2.
        m.jr(m.RA),  # Add signed immediate; Jump to register.
        m.sb(m.V1, table & 0xFFFF, m.V0),  # Store V1 at V0 + table & 65535.
    )  # Store byte.
    arena += b"SMARMOURCHECKS!!"
    assert len(arena) <= 0x58
    arena = arena.ljust(0x58, b"\0")
    edits = [
        (getter_site, packed(jump(get))),  # Call get.
        (give + 0x44, packed(jump(record))),  # Call record.
        (give + 0x4C, packed(branch(give + 0x4C, give + 0xAC), 0)),  # Branch from give + 76 to give + 172.
        (table, arena),
    ]
    if bypass_tier_gate:
        # Fixed Challenge Mode tier never advances the vanilla NG+ progress byte,
        # so the story-tier check must be skipped or tier-locked pickups never spawn.
        edits.append((gate + 8, packed(0)))
    plan = Plan(pine, [Patch(a, read(a, len(b)), b) for a, b in edits], expected_game_id=game_id)
    plan.journals = ((table, 32),)
    plan.table, plan.locations = table, dict(locations)
    return plan
