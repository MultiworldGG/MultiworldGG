"""Isolate Treehouse's grind rail completion from Kalidon's shared save bit."""

import struct

from . import asm as m
from .plan import Plan, supported_game_id


def prepare(pine, *, code_start, code, checked=False):
    game_id = supported_game_id(pine)
    signature = m.packed(0x27BDFFC0, 0xFFB20030, 0xFFB00020, 0x0080902D,
                         0xFFB10028, 0xFFBF0038, 0x8E450054, 0x8CA2000C,
                         0x2442FFFF, 0x2C43000B)
    hits = [i for i in range(0, len(code) - len(signature), 4)
            if code[i:i + len(signature)] == signature]
    if len(hits) != 1:
        raise RuntimeError("Expected one Treehouse grind rail lock")
    offset = hits[0]
    start = code_start + offset

    def read(off, size):
        raw = code[offset + off:offset + off + size]
        if len(raw) != size:
            raise RuntimeError("Truncated Treehouse grind rail code")
        return raw

    init = struct.unpack('<4I', read(0x104, 16))
    finish = struct.unpack('<4I', read(0x4C0, 16))
    if (init[0], init[1], init[3]) != (0x2404004E, 0xAE200048, 0x90A5000C) or init[2] >> 26 != 3:
        raise RuntimeError("Treehouse grind rail initialization changed")
    if (finish[0], finish[1], finish[3]) != (0x2404004E, 0x24050001, 0x92A6000C) or finish[2] >> 26 != 3:
        raise RuntimeError("Treehouse grind rail completion changed")
    if read(0x298, 16) != m.packed(0xDFBF0010, 0x03E00008, 0x27BD0020, 0):
        raise RuntimeError("Treehouse grind rail destructor boundary changed")
    journal = start + 0x2A4
    upper, lower = (journal + 0x8000) >> 16, journal & 65535
    plan = Plan(pine, [
        # The native lock uses puzzle ID 0, also used by Kalidon. Keep both
        # its initial lock state and completion separate from that save bit.
        m.Patch(start + 0x104, read(0x104, 16), m.packed(
            m.lui(m.V0, upper), init[1], m.lbu(m.V0, lower, m.V0),
            m.addiu(m.V0, m.V0, -1))),
        m.Patch(start + 0x4C0, read(0x4C0, 12), m.packed(
            m.lui(m.V0, upper), m.addiu(m.V1, m.ZERO, 2), m.sb(m.V1, lower, m.V0))),
        m.Patch(journal, bytes(4), bytes([2 if checked else 1, 0, 0, 0])),
    ], expected_game_id=game_id)
    plan.journals = ((journal, 1),)
    return plan
