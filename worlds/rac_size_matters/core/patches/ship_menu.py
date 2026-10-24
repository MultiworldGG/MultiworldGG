"""Expose the story destinations and HIG Treehouse in the ship menu.

The Treehouse row is gated by a word the client writes (see `plan.treehouse_flag`).
"""

import struct

from . import asm as m
from .asm import Patch, branch, j, jump, packed
from .plan import Plan, supported_game_id


def prepare(pine, *, code_start, code, treehouse_unlocked=True):
    game_id = supported_game_id(pine)
    anchor = packed(0x26310001, 0x2E22000C, 0x1440FFE4, 0x0000802D)
    hits = [i for i in range(0, len(code) - len(anchor) + 1, 4) if code[i : i + len(anchor)] == anchor]
    if len(hits) != 1:
        raise RuntimeError("Expected one native ship menu builder")
    end = code_start + hits[0] + 16
    loop = end - 120

    def read(address, size):
        offset = address - code_start
        if not 0 <= offset <= len(code) - size:
            raise RuntimeError("Ship menu outside loaded module")
        return code[offset : offset + size]

    def require(address, expected):
        if read(address, len(expected)) != expected:
            raise RuntimeError(f"Ship menu signature changed at {address:#x}")

    def call(address):
        (word,) = struct.unpack("<I", read(address, 4))
        if word >> 26 != 3:
            raise RuntimeError("Ship menu call signature changed")
        return (word & 0x3FFFFFF) << 2

    unlock = call(loop + 4)
    tail = call(loop + 20)
    group = call(loop + 44)
    name = call(loop + 56)
    add = call(loop + 96)
    original_loop = packed(
        0x0000802D,
        jump(unlock),  # Call unlock.
        0x0220202D,
        0x10400004,
        0,
        jump(tail),  # Call tail.
        0x0220202D,
        0x0282800B,
        0x12000011,
        0x24060001,
        0x0260202D,
        jump(group),  # Call group.
        0x24050001,
        0x0220202D,
        jump(name),  # Call name.
        0x0000282D,
        0x0040282D,
        0xAFB20000,
        0x0260202D,
        0x0220302D,
        0x0000382D,
        0x0000402D,
        0x0000482D,
        0x240A0001,
        jump(add),  # Call add.
        0x0000582D,
        0x26310001,
        0x2E22000C,
        0x1440FFE4,
        0x0000802D,
    )
    require(loop, original_loop)
    require(tail, packed(0x2483FFFF, 0x2C62000A, 0x10400009, 0x0000282D))
    require(tail + 44, packed(0x24050001, 0x03E00008, 0x00A0102D))
    # Check the switch table as well as its dispatch instructions.
    words = struct.unpack("<7I", read(tail + 16, 28))
    if (
        words[0] >> 16 != 0x3C02
        or words[1] != 0x00031880
        or words[2] >> 16 != 0x2442
        or words[3:] != (0x00621821, 0x8C640000, 0x00800008, 0)
    ):
        raise RuntimeError("Ship visibility switch changed")
    low = words[2] & 0xFFFF
    table = ((words[0] & 0xFFFF) << 16) + (low - 0x10000 if low & 0x8000 else low)
    require(table, packed(*(tail + (48 if p in (5, 9) else 44) for p in range(1, 11))))

    route = end - (0x8D0 if game_id == "SCPS-15120" else 0x8E8)
    setter = call(route + 36)
    visited = call(route + 20)
    require(route - 4, packed(0x1083FFEB))
    require(
        route,
        packed(
            0x24020006,
            0x1482000F,
            0x24020017,
            0x1062FFE7,
            0,
            jump(visited),  # Call visited.
            0x24040017,
            0x10400005,
            0,
            jump(setter),  # Call setter.
            0x24040017,
            0x10000007,
            0,
            jump(setter),  # Call setter.
            0x8E0400D0,
            0x10000003,
            0,
            jump(setter),  # Call setter.
            0,
        ),
    )
    label = route + 52
    # Spare word after the routing strings; nonzero shows the Treehouse row.
    flag = route + 68
    # The first Omega row carries marker 1; the second carries marker 0.
    # Dreamtime (5) uses Outpost's unlock (6), irrespective of its auto-unlock.
    body = [
        m.xori(m.V0, m.S1, 5),  # Set V0 to S1 ^ 5.
        m.sltiu(m.V0, m.V0, 1),  # XOR immediate; Compare unsigned immediate.
        jump(unlock),  # Call unlock.
        m.addu(m.A0, m.S1, m.V0),  # Set A0 to S1 + V0.
        m.beq(m.V0, m.ZERO, (tail - (loop + 20)) // 4),
        m.dmove(m.A0, m.S3),  # Branch if equal; Copy 64-bit register.
        m.addiu(m.A1, m.ZERO, 1),  # Set A1 to ZERO + 1.
        jump(group),  # Call group.
        m.addiu(m.A2, m.ZERO, 1),  # Set A2 to ZERO + 1.
        m.dmove(m.A0, m.S1),  # Copy S1 into A0.
        jump(name),  # Call name.
        m.addiu(m.A1, m.ZERO, 1),  # Resolve special destination 24 as HIG Treehouse.
        m.dmove(m.A1, m.V0),  # Copy V0 into A1.
        m.addiu(m.V0, m.ZERO, 6),  # Copy 64-bit register; Add signed immediate.
        m.bne(m.S1, m.V0, 5),  # Branch 5 words if S1 != V0.
        m.sw(m.S2, 0, m.SP),  # Branch if unequal; Store word.
        *m.li32(m.A1, label),  # Load label into A1.
        m.sll(m.V0, m.S4, 3),  # Set V0 to S4 << 3.
        m.addu(m.A1, m.A1, m.V0),  # Shift left; Add registers.
        m.dmove(m.A0, m.S3),  # Copy S3 into A0.
        m.dmove(m.A2, m.S1),  # Copy S1 into A2.
        m.dmove(m.A3, m.S4),  # Copy S4 into A3.
        m.dmove(m.T0, m.ZERO),  # Copy ZERO into T0.
        m.dmove(m.T1, m.ZERO),  # Copy ZERO into T1.
        m.addiu(m.T2, m.ZERO, 1),  # Copy 64-bit register; Add signed immediate.
        jump(add),
        m.dmove(m.T3, m.ZERO),  # Copy ZERO into T3.
        j(tail),
        m.NOP,
    ]
    continuation = [
        m.addiu(m.V0, m.ZERO, 6),  # No operation; Add signed immediate.
        m.bne(m.S1, m.V0, 3),  # Branch 3 words if S1 != V0.
        m.lui(m.AT, (flag + 0x8000) >> 16),  # Branch delay: prepare the Treehouse flag address.
        m.bne(m.S4, m.ZERO, (loop - (tail + 16)) // 4),
        m.addiu(m.S4, m.ZERO, 0),  # Branch if unequal; Add signed immediate.
        m.addiu(m.S1, m.S1, 1),  # Set S1 to S1 + 1.
        m.sltiu(m.V0, m.S1, 11),  # Add signed immediate; Compare unsigned immediate.
        m.bne(m.V0, m.ZERO, (loop - (tail + 32)) // 4),
        m.addiu(m.S4, m.ZERO, 1),  # Branch if unequal; Add signed immediate.
        m.addiu(m.V0, m.ZERO, 11),
        m.bne(m.S1, m.V0, (end - (tail + 44)) // 4),
        m.addiu(m.S1, m.ZERO, 24),
        # Re-enter at the body's availability branch with the client's flag in
        # place of the story unlock, so a locked Treehouse skips its row.
        j(loop + 16),
        m.lw(m.V0, flag & 65535, m.AT),
    ]
    routing = (
        packed(
            m.addiu(m.V0, m.ZERO, 6),  # Set V0 to ZERO + 6.
            m.bne(m.A0, m.V0, 5),  # Branch 5 words if A0 != V0.
            m.NOP,  # Add signed immediate; Branch if unequal; No operation.
            m.lw(m.V0, 0xD4, m.S0),  # Load V0 from S0 + 212.
            m.bne(m.V0, m.ZERO, 2),  # Branch 2 words if V0 != ZERO.
            m.NOP,  # Load word; Branch if unequal; No operation.
            m.addiu(m.A0, m.ZERO, 23),  # Set A0 to ZERO + 23.
            m.beq(
                m.A0, m.V1, ((route - 0x54) - (route + 32)) // 4
            ),  # Branch (route - 84 - (route + 32)) // 4 words if A0 == V1.
            m.NOP,  # Branch if equal; No operation.
            jump(setter),  # Call setter.
            m.NOP,
            branch(route + 44, route + 76),  # Branch from route + 44 to route + 76.
            m.NOP,  # No operation.
        )
        + b"MOO2\0\0\0\0MOO1\0"
    ).ljust(flag - route, b"\0") + packed(int(treehouse_unlocked))
    edits = [
        Patch(loop, original_loop, packed(*body).ljust(120, b"\0")),
        Patch(tail, read(tail, 56), packed(*continuation).ljust(56, b"\0")),
        Patch(route - 4, packed(0x1083FFEB), packed(m.NOP)),  # No operation.
        Patch(route, read(route, 76), routing.ljust(76, b"\0")),
    ]
    edits.extend(_preview_edits(read, require, call, table, code_start, code))
    plan = Plan(pine, edits, expected_game_id=game_id)
    plan.treehouse_flag = flag
    plan.mutable_data = ((flag, 4),)
    return plan


def _preview_edits(read, require, call, table, code_start, code):
    """Keep special destinations out of the story-only statistics and atlas."""
    def unique(pattern):
        hits = [i for i in range(0, len(code) - len(pattern) + 1, 4)
                if code[i:i + len(pattern)] == pattern]
        if len(hits) != 1:
            raise RuntimeError("Expected one native ship preview block")
        return code_start + hits[0]

    # The first getter returns the total bolt count. The next getter loops
    # that many times; an out-of-range planet can turn it into millions.
    stats = unique(packed(m.lw(m.A0, 0xD0, m.S3), m.dmove(m.S2, m.V0),
                          0x12400024)) - 4
    total = call(stats)
    require(stats + 0xDC, packed(0x12600043, 0x27A50010))
    details_end = stats + 0x1EC
    # The original null-row branch at +0xDC lands at details_end.
    require(details_end - 4, packed(m.dmove(m.A2, m.S1)))
    guard = packed(
        m.sltiu(m.V0, m.A0, 12),
        m.bne(m.V0, m.ZERO, 3),
        m.NOP,
        j(details_end),
        m.NOP,
        j(total),
        m.NOP,
    ).ljust(40, b"\0")

    # Compact the atlas loop by using its full row-array pointer in the
    # final load. This leaves room to reject IDs outside its eleven entries.
    atlas = unique(packed(0, 0x00101080, 0x00441021, 0x8C430000,
                          0x8C6400D0, 0x2484FFFF, 0x000440C0))
    original = read(atlas, 140)
    words = list(struct.unpack('<35I', original))
    require(atlas + 28, packed(0x011E1821, 0x94620000, 0x000210C0,
                               0x02621021, 0x8C460000, 0x10C0000E))
    require(atlas + 124, packed(0x8CA20004, 0x0202102B, 0x5440FFDF))
    if (words[27] >> 16 != 0x3C05 or words[29] >> 16 != 0x24A5
            or words[30] >> 16 != 0x3C04 or words[34] >> 16 != 0x8C84
            or words[27] & 65535 != words[30] & 65535
            or words[29] & 65535 != words[34] & 65535):
        raise RuntimeError("Ship atlas row pointer changed")
    body, positions = [], {}
    for i, word in enumerate(words):
        if i in (0, 30):
            continue
        if i == 5:
            body.extend((m.sltiu(m.V0, m.A0, 12), 0))
        positions[atlas + i * 4] = atlas + len(body) * 4
        body.append(m.lw(m.A0, 0, m.A1) if i == 34 else word)
    for old, new in positions.items():
        idx = (new - atlas) // 4
        word = body[idx]
        if word >> 26 in (4, 5, 20, 21):
            offset = struct.unpack('<h', packed(word)[:2])[0]
            target = old + 4 + offset * 4
            target = positions.get(target, target)
            body[idx] = (word & 0xFFFF0000) | ((target - new - 4) // 4 & 65535)
    body[5] = m.beq(m.V0, m.ZERO, (positions[atlas + 108] - (atlas + 24)) // 4)
    return [
        Patch(table, read(table, 40), guard),
        Patch(stats, read(stats, 4), packed(jump(table))),
        Patch(atlas, original, packed(*body)),
    ]
