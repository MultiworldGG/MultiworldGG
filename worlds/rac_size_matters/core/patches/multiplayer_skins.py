"""US multiplayer skins in the single-player menu."""

import struct

from . import asm as m
from .asm import Patch, j, jump, packed
from .plan import Plan, supported_game_id

NAMES = (
    "Ratchet",
    "Snowman",
    "HotBot",
    "Qwark",
    "Ninja",
    "Training Bot",
    "Nurse",
    "Technomite",
    "Dan",
    "Low Rider Ratchet",
    "Samurai Ratchet",
    "Kangaroo Ratchet",
    "Tuxedo Ratchet",
)
COUNT = 7 + len(NAMES)
MCP = 0x1F4A740
SP_TABLE = 0x1EDCC10
MP_TABLE = 0x1EDCCB8
PRIMARY_LIMIT = 0x70000


class _Code:
    def __init__(self):
        self.words, self.labels, self.branches = [], {}, []

    def emit(self, *words):
        self.words.extend(words)

    def label(self, name):
        self.labels[name] = len(self.words)

    def branch(self, opcode, name, delay=0):
        self.branches.append((len(self.words), name))
        self.emit(opcode, delay)

    def pack(self):
        words = self.words.copy()
        for index, name in self.branches:
            words[index] |= (self.labels[name] - index - 1) & 0xFFFF
        return packed(*words)


def promoted_commands(commands, mapping):
    """Reference implementation used to validate the game-thread converter."""
    if len(commands) % 4 or not commands or len(commands) > 0x1000:
        raise ValueError("Invalid LOD command length")
    inverse = {}
    for full, reduced in enumerate(mapping):
        inverse.setdefault(reduced, full)
    words = list(struct.unpack("<%dI" % (len(commands) // 4), commands))
    if words[-1] != 0xFE000000:
        raise ValueError("Missing LOD terminator")
    for index, word in enumerate(words):
        if word >> 24 in (0xFA, 0xFB):
            if word & 0xFFFF not in inverse:
                raise ValueError("LOD bone has no full-skeleton mapping")
            words[index] = (word & 0xFFFF0000) | inverse[word & 0xFFFF]
    return packed(*words)


def mcp_address(game_id):
    return {"SCUS-97615": MCP, "SCES-55019": MCP, "SCPS-15120": 0x1F4A580}[game_id]


def prepare(pine, *, code_start, code, skin):
    """Prepare only while the level loader is held, or skin functions are idle."""
    game_id = supported_game_id(pine)
    sp_table, mp_table, load_model = {
        "SCUS-97615": (SP_TABLE, MP_TABLE, 0x1E92A20),
        "SCES-55019": (0x1EDCA10, 0x1EDCAB8, 0x1E927C8),
        "SCPS-15120": (0x1EDE938, 0x1EDE9E0, 0x1E946D0),
    }[game_id]
    mcp = mcp_address(game_id)
    buffer = pine.read_int32(mcp + 0x2DC)
    if not 0x100000 <= buffer <= 0x1E00000 - 0x89000 or buffer & 15:
        raise RuntimeError("Single-player hero buffer is not allocated")
    edits = []

    def read(address, size):
        offset = address - code_start
        if not 0 <= offset <= len(code) - size:
            raise RuntimeError("Skin function outside loaded module")
        return code[offset : offset + size]

    def word(address):
        return struct.unpack("<I", read(address, 4))[0]

    def require(address, expected):
        if read(address, len(expected)) != expected:
            raise RuntimeError(f"Multiplayer skin signature changed at {address:#x}")

    def patch(address, expected, replacement):
        require(address, expected)
        edits.append(Patch(address, expected, replacement))

    def call(address):
        value = word(address)
        if value >> 26 != 3:
            raise RuntimeError("Skin loader call changed")
        return (value & 0x3FFFFFF) << 2

    def ptr(upper, lower):
        return ((word(upper) & 65535) << 16) + struct.unpack("<h", read(lower, 2))[0]

    def redirect_ptr(upper, lower, old, new):
        if word(upper) >> 26 != 15 or word(lower) >> 26 != 9 or ptr(upper, lower) != old:
            raise RuntimeError("Skin table reference changed")
        patch(upper, packed(word(upper)), packed((word(upper) & 0xFFFF0000) | ((new + 0x8000) >> 16)))
        patch(lower, packed(word(lower)), packed((word(lower) & 0xFFFF0000) | (new & 65535)))

    # These allocations are disjoint from the model, promoted geometry,
    # two texture buffers, and one another.
    rows, menu_table, descriptors = buffer + 0x72000, buffer + 0x74000, buffer + 0x74800
    finish, stock_finish, owned, label, add_row = (buffer + x for x in (0x75000, 0x75700, 0x75800, 0x75840, 0x75880))
    strings = buffer + 0x75A00
    begin, end = skin.begin, skin.finish
    gate = getattr(skin, "menu_anchor", skin.edits[0].address - 4)
    # JP builds every stock menu row; US/EU skip Trash. That changes the
    # surrounding function offsets, while row and descriptor layouts agree.
    jp_offsets = {
        -0x93C: -0x934, -0x934: -0x92C, -0x814: -0x80C, -0x810: -0x808,
        -0x738: -0x730, -0x730: -0x728, -0x34C: -0x344, -0x348: -0x340,
        -0x1C0: -0x1B8, -0x1B8: -0x1B0, 0x84: 0x74, 0x9C: 0x8C,
        0xBD4: 0xBC4, 0xBD8: 0xBC8, -0x378: -0x370, -0x1C8: -0x1C0,
        0x34: 0x2C, 0x144: 0x134, 0x170: 0x160, -0xB4: -0xAC,
        -0xBC: -0xB4, -0x91C: -0x914, -0x728: -0x720,
        0x108: 0xF8, -0x8A8: -0x8A0, 0x28: 0x24,
    }
    def site(offset):
        return gate + (jp_offsets.get(offset, offset) if game_id == "SCPS-15120" else offset)

    old_menu = ptr(site(-0x1C), site(-0x18))
    original_rows = read(old_menu, 7 * 16)
    if [struct.unpack_from("<I", original_rows, i * 16)[0] for i in range(7)] != [0, 1, 2, 6, 3, 5, 4]:
        raise RuntimeError("Unexpected single-player skin table")
    sp = pine.read_bytes(sp_table, 7 * 24)
    mp = pine.read_bytes(mp_table, 13 * 64)
    if [struct.unpack_from("<I", mp, i * 64)[0] for i in range(13)] != [
        26,
        50,
        8,
        16,
        9,
        56,
        12,
        53,
        3,
        25,
        28,
        19,
        31,
    ]:
        raise RuntimeError("Unexpected multiplayer asset table")
    menu_data, descriptor_data, text = bytearray(original_rows), bytearray(sp), bytearray()
    for index, name in enumerate(NAMES):
        source = struct.unpack_from("<16I", mp, index * 64)
        model = 7 + index
        menu_data += packed(model, 0, strings + len(text), model)
        text += ("Multiplayer Ratchet" if index == 0 else name).encode("ascii") + b"\0"
        descriptor_data += packed(source[0], source[1], source[5], source[9], 0, 0)
    if len(text) > 0x400 or COUNT * 0xE4 > 0x2000:
        raise RuntimeError("Multiplayer skin storage overflow")
    for hi, lo in [
        (-0x93C, -0x934),
        (-0x814, -0x810),
        (-0x738, -0x730),
        (-0x34C, -0x348),
        (-0x1C0, -0x1B8),
        (-0x1C, -0x18),
        (0x84, 0x9C),
        (0xBD4, 0xBD8),
    ]:
        redirect_ptr(site(hi), site(lo), old_menu, menu_table)
    for offset, expected, replacement in [
        (-0x378, 0x2E620FB9, 0x2E620000 | (0xFB2 + COUNT)),
        (-0x1C8, 0x2CA20007, 0x2CA20000 | COUNT),
        (0x34, 0x2E220007, 0x2E220000 | COUNT),
        (0x144, 0x2E220007, 0x2E220000 | COUNT),
        (0x170, 0x2E220007, 0x2E220000 | COUNT),
        (-0xB4, 0x24061000, 0x24062000),
    ]:
        patch(site(offset), packed(expected), packed(replacement))
    old_rows = ptr(site(-0xBC), site(-0x88))
    redirect_ptr(site(-0xBC), site(-0x88), old_rows, rows)
    # The normal loader also handles the extended descriptor table. Never
    # allow a primary PAK read to overwrite the storage reserved above.
    for offset, expected, replacement in [
        (0x3C, 0x3C120008, 0x3C120007),
        (0x4C, 0x36524000, 0x36520000),
        (0xD8, 0x3C070008, 0x3C070007),
        (0xE8, 0x34E74000, 0x34E70000),
    ]:
        patch(begin + offset, packed(expected), packed(replacement))
    # Preserve the texture offset: native begin uses S2 for both its limit
    # and the secondary texture address. Supply the original 0x84000 offset.
    require(begin + 0x78, packed(0x0292B021))
    # At this point S6=buffer+0x70000. Redirect the cache-flush call through
    # a trampoline that corrects S6 while preserving the native delay slot.
    begin_fix = buffer + 0x75900
    patch(begin + 0x7C, packed(jump(load_model)), packed(jump(begin_fix)))  # Call 32057888. Call begin_fix.

    size, load, asset = call(begin + 0xAC), call(begin + 0xE4), call(end + 0xB4)
    pak = ptr(begin + 0xA4, begin + 0xB0)
    pending = ptr(end + 4, end + 16)
    changed = ptr(end + 0x98, end + 0xA4)
    apply = ptr(end + 0x9C, end + 0xA8)
    is_owned = call(site(-0x91C))
    for offset in (-0x91C, -0x728, 0x108):
        patch(site(offset), packed(jump(is_owned)), packed(jump(owned)))  # Call is_owned. Call owned.
    gettext = call(site(-0x8A8))
    patch(site(-0x8A8), packed(jump(gettext)), packed(jump(label)))  # Call gettext. Call label.
    native_add = call(site(0x28))
    patch(site(0x28), packed(jump(native_add)), packed(jump(add_row)))  # Call native_add. Call add_row.

    c = _Code()
    c.emit(
        *m.li32(m.T0, pending),
        m.lw(m.T1, 0, m.T0),
        m.sltiu(m.T2, m.T1, 7),  # Load T1 from T0 + 0. Set T2 to T1 < 7. Load pending into T0.
    )  # Load word; Compare unsigned immediate; Load 32-bit constant.
    c.branch(m.beq(m.T2, m.ZERO, 0), "mp")  # Branch 0 words if T2 == ZERO.
    c.emit(j(stock_finish), 0)  # Jump to stock_finish.
    c.label("mp")
    c.emit(m.sltiu(m.T2, m.T1, COUNT))  # Set T2 to T1 < COUNT.
    c.branch(m.beq(m.T2, m.ZERO, 0), "invalid")  # Branch 0 words if T2 == ZERO.
    c.emit(m.addiu(m.SP, m.SP, -0x90), m.sd(m.RA, 0x80, m.SP))  # Add signed immediate; Save 64-bit register.
    for index, reg in enumerate((m.S0, m.S1, m.S2, m.S3, m.S4)):
        c.emit(m.sd(reg, 0x50 + index * 8, m.SP))  # Store reg at SP + 80 + index * 8.
    c.emit(
        m.move(m.S4, m.T1),  # Copy T1 into S4.
        *m.li32(m.S0, buffer),  # Copy register; Load 32-bit constant.
        m.addiu(m.T0, m.T1, -7),  # Set T0 to T1 + -7.
        m.sll(m.T0, m.T0, 6),  # Add signed immediate; Shift left.
        *m.li32(m.S1, mp_table),  # Use the detected region's multiplayer descriptors.
        m.addu(m.S1, m.S1, m.T0),  # Add registers; Load 32-bit constant.
        *m.li32(m.T0, changed),  # Load changed into T0.
        m.lbu(m.S2, 0, m.T0),  # Load byte; Load 32-bit constant.
        *m.li32(m.T0, apply),  # Load apply into T0.
        m.lbu(m.S3, 0, m.T0),  # Load byte; Load 32-bit constant.
        m.lw(m.A1, 12, m.S1),  # Load A1 from S1 + 12.
    )  # Load word.
    c.branch(m.beq(m.A1, m.ZERO, 0), "textures")  # Branch 0 words if A1 == ZERO.
    c.branch(m.beq(m.S2, m.ZERO, 0), "textures")  # Branch 0 words if S2 == ZERO.
    c.emit(
        *m.li32(m.A0, pak),
        jump(size),
        0,
        m.sltiu(m.T0, m.V0, 0x5001),  # Call size. Set T0 to V0 < 20481. Load pak into A0.
    )  # Compare unsigned immediate; Load 32-bit constant.
    c.branch(m.beq(m.T0, m.ZERO, 0), "failed")  # Branch 0 words if T0 == ZERO.
    c.emit(
        m.sw(m.V0, 0x3C, m.S1),  # Store V0 at S1 + 60.
        *m.li32(m.A0, pak),  # Load pak into A0.
        m.lw(m.A1, 12, m.S1),  # Store word; Load word; Load 32-bit constant.
        *m.li32(m.A2, buffer + 0x7F000),  # Load buffer + 520192 into A2.
        jump(load),  # Call load.
        m.addiu(m.A3, m.ZERO, 0x5000),  # Set A3 to ZERO + 20480.
    )  # Add signed immediate; Load 32-bit constant.
    c.label("textures")
    c.emit(
        m.sw(m.ZERO, 0, m.SP),  # Store ZERO at SP + 0.
        m.sw(m.ZERO, 4, m.SP),  # Store ZERO at SP + 4.
        *m.li32(m.T0, 0xB9C25B73),  # Load 3116522355 into T0.
        m.sw(m.T0, 8, m.SP),  # Store word; Load 32-bit constant.
        m.sw(m.ZERO, 12, m.SP),  # Store ZERO at SP + 12.
        m.sw(m.ZERO, 16, m.SP),  # Store ZERO at SP + 16.
        *m.li32(m.T0, 0xB51670D1),  # Load 3038146769 into T0.
        m.sw(m.T0, 20, m.SP),  # Store word; Load 32-bit constant.
        m.sll(m.T0, m.S4, 1),  # Set T0 to S4 << 1.
        m.addu(m.T0, m.T0, m.S4),  # Set T0 to T0 + S4.
        m.sll(m.T0, m.T0, 3),  # Shift left; Add registers.
        *m.li32(m.T1, descriptors),  # Load descriptors into T1.
        m.addu(m.T0, m.T0, m.T1),  # Add registers; Load 32-bit constant.
        *m.li32(m.T1, buffer + 0x84000),  # Load buffer + 540672 into T1.
        m.sw(m.T1, 24, m.SP),  # Store word; Load 32-bit constant.
        m.lw(m.T1, 20, m.T0),  # Load T1 from T0 + 20.
        m.sw(m.T1, 28, m.SP),  # Load word; Store word.
        m.lw(m.T1, 12, m.T0),  # Load T1 from T0 + 12.
        m.sw(m.T1, 32, m.SP),  # Load word; Store word.
        m.lw(m.T0, 12, m.S1),  # Load T0 from S1 + 12.
        m.addiu(m.A2, m.ZERO, 3),  # Set A2 to ZERO + 3.
    )  # Load word; Add signed immediate.
    c.branch(m.beq(m.T0, m.ZERO, 0), "load")  # Branch 0 words if T0 == ZERO.
    c.emit(
        *m.li32(m.T0, buffer + 0x7F000),  # Load buffer + 520192 into T0.
        m.sw(m.T0, 36, m.SP),  # Store word; Load 32-bit constant.
        m.lw(m.T0, 0x3C, m.S1),  # Load T0 from S1 + 60.
        m.sw(m.T0, 40, m.SP),  # Load word; Store word.
        m.lw(m.T0, 0x2C, m.S1),  # Load T0 from S1 + 44.
        m.sw(m.T0, 44, m.SP),  # Store T0 at SP + 44.
        m.addiu(m.A2, m.ZERO, 4),  # Set A2 to ZERO + 4.
    )  # Load word; Store word; Add signed immediate.
    c.label("load")
    c.emit(
        m.move(m.A0, m.ZERO),  # Copy ZERO into A0.
        m.move(m.A1, m.S0),  # Copy S0 into A1.
        m.move(m.A3, m.SP),  # Copy SP into A3.
        m.move(m.T0, m.S2),  # Copy S2 into T0.
        m.move(m.T1, m.S3),  # Copy S3 into T1.
        jump(asset),  # Call asset.
        m.move(m.T2, m.ZERO),  # Copy ZERO into T2.
    )  # Copy register.
    c.branch(m.beq(m.V0, m.ZERO, 0), "failed")  # Branch 0 words if V0 == ZERO.
    c.branch(m.beq(m.S2, m.ZERO, 0), "done")  # Branch 0 words if S2 == ZERO.
    # Promote a copy; altering LOD1 itself would break distant rendering.
    c.emit(
        m.lw(m.T0, 0x1C, m.S0),  # Load T0 from S0 + 28.
        m.lw(m.T1, 0x1C, m.T0),  # Load T1 from T0 + 28.
        m.lw(m.T2, 0x20, m.T0),  # Load T2 from T0 + 32.
        m.lw(m.T3, 0x24, m.S0),  # Load T3 from S0 + 36.
        m.lw(m.T3, 0x14, m.T3),  # Load T3 from T3 + 20.
        m.lw(m.T4, 0x20, m.S0),  # Load T4 from S0 + 32.
        m.lw(m.T4, 4, m.T4),  # Load T4 from T4 + 4.
        *m.li32(m.T5, buffer + PRIMARY_LIMIT),  # Load buffer + PRIMARY_LIMIT into T5.
        *m.li32(m.T6, buffer + PRIMARY_LIMIT + 0x1000),  # Load buffer + PRIMARY_LIMIT + 4096 into T6.
    )  # Load 32-bit constant.
    c.label("copy")
    c.emit(m.sltu(m.V0, m.T1, m.T2))  # Set V0 to T1 < T2.
    c.branch(m.beq(m.V0, m.ZERO, 0), "failed")  # Branch 0 words if V0 == ZERO.
    c.emit(m.sltu(m.V0, m.T5, m.T6))  # Set V0 to T5 < T6.
    c.branch(m.beq(m.V0, m.ZERO, 0), "failed")  # Branch 0 words if V0 == ZERO.
    c.emit(
        m.lw(m.T7, 0, m.T1),
        m.srl(m.T8, m.T7, 24),
        m.addiu(m.T9, m.ZERO, 0xFA),  # Load T7 from T1 + 0. Set T8 to T7 >> 24. Set T9 to ZERO + 250.
    )  # Load word; Shift right; Add signed immediate.
    c.branch(m.beq(m.T8, m.T9, 0), "bone")  # Branch 0 words if T8 == T9.
    c.emit(m.addiu(m.T9, m.ZERO, 0xFB))  # Set T9 to ZERO + 251.
    c.branch(m.bne(m.T8, m.T9, 0), "write")  # Branch 0 words if T8 != T9.
    c.label("bone")
    c.emit(m.andi(m.A0, m.T7, 0xFFFF), m.move(m.A1, m.ZERO))  # AND immediate; Copy register.
    c.label("search")
    c.emit(m.sltu(m.V0, m.A1, m.T4))  # Set V0 to A1 < T4.
    c.branch(m.beq(m.V0, m.ZERO, 0), "failed")  # Branch 0 words if V0 == ZERO.
    c.emit(m.addu(m.A2, m.T3, m.A1), m.lbu(m.A2, 0, m.A2))  # Add registers; Load byte.
    c.branch(m.beq(m.A2, m.A0, 0), "found")  # Branch 0 words if A2 == A0.
    c.branch(m.beq(m.ZERO, m.ZERO, 0), "search", m.addiu(m.A1, m.A1, 1))  # Branch if equal; Add signed immediate.
    c.label("found")
    c.emit(
        m.srl(m.T7, m.T7, 16),
        m.sll(m.T7, m.T7, 16),
        m.or_(m.T7, m.T7, m.A1),  # Set T7 to T7 >> 16. Set T7 to T7 << 16. Set T7 to T7 | A1.
    )  # Shift right; Shift left; OR registers.
    c.label("write")
    c.emit(
        m.sw(m.T7, 0, m.T5),  # Store T7 at T5 + 0.
        m.addiu(m.T1, m.T1, 4),  # Set T1 to T1 + 4.
        m.addiu(m.T5, m.T5, 4),  # Store word; Add signed immediate.
        m.addiu(m.T9, m.ZERO, 0xFE),  # Set T9 to ZERO + 254.
    )  # Add signed immediate.
    c.branch(m.bne(m.T8, m.T9, 0), "copy")  # Branch 0 words if T8 != T9.
    c.emit(*m.li32(m.T1, buffer + PRIMARY_LIMIT), m.sw(m.T1, 0x18, m.T0))  # Store word; Load 32-bit constant.
    c.label("done")
    c.emit(
        *m.li32(m.T0, mcp),  # Publish the loaded model to this region's MCP.
        m.sb(m.S4, 0x2E0, m.T0),  # Store byte; Load 32-bit constant.
        *m.li32(m.T0, pending),  # Load pending into T0.
        m.addiu(m.T1, m.ZERO, -1),  # Set T1 to ZERO + -1.
        m.sw(m.T1, 0, m.T0),  # Add signed immediate; Store word; Load 32-bit constant.
        m.addiu(m.V0, m.ZERO, 1),  # Set V0 to ZERO + 1.
    )  # Add signed immediate.
    c.branch(m.beq(m.ZERO, m.ZERO, 0), "return")  # Branch 0 words if ZERO == ZERO.
    c.label("failed")
    c.emit(m.move(m.V0, m.ZERO))  # Copy ZERO into V0.
    c.label("return")
    for index, reg in enumerate((m.S0, m.S1, m.S2, m.S3, m.S4)):
        c.emit(m.ld(reg, 0x50 + index * 8, m.SP))  # Load reg from SP + 80 + index * 8.
    c.emit(
        m.ld(m.RA, 0x80, m.SP),
        m.jr(m.RA),
        m.addiu(m.SP, m.SP, 0x90),  # Load RA from SP + 128. Jump to RA. Set SP to SP + 144.
    )  # Load 64-bit register; Jump to register; Add signed immediate.
    c.label("invalid")
    c.emit(m.jr(m.RA), m.move(m.V0, m.ZERO))  # Jump to register; Copy register.
    finish_code = c.pack()
    if len(finish_code) > stock_finish - finish:
        raise RuntimeError("Multiplayer loader exceeds reserved code storage")
    owned_code = packed(
        m.sltiu(m.T0, m.A1, 7),  # Set T0 to A1 < 7.
        m.bne(m.T0, m.ZERO, 3),  # Branch 3 words if T0 != ZERO.
        0,  # Compare unsigned immediate; Branch if unequal.
        m.jr(m.RA),  # Jump to RA.
        m.sltiu(m.V0, m.A1, COUNT),  # Set V0 to A1 < COUNT.
        j(is_owned),  # Jump to is_owned.
        0,
    )  # Jump to register; Compare unsigned immediate.
    label_code = packed(
        m.sltiu(m.T0, m.A0, 0x1000),  # Set T0 to A0 < 4096.
        m.bne(m.T0, m.ZERO, 3),  # Branch 3 words if T0 != ZERO.
        0,  # Compare unsigned immediate; Branch if unequal.
        m.jr(m.RA),  # Jump to RA.
        m.move(m.V0, m.A0),  # Copy A0 into V0.
        j(gettext),  # Jump to gettext.
        0,
    )  # Jump to register; Copy register.
    add_code = packed(
        m.sltiu(m.T2, m.A2, 7),
        m.xori(m.T2, m.T2, 1),
        j(native_add),
        0,  # Set T2 to A2 < 7. Set T2 to T2 ^ 1. Jump to native_add.
    )  # Compare unsigned immediate; XOR immediate.
    fix_code = packed(
        m.addiu(m.SP, m.SP, -16),  # Set SP to SP + -16.
        m.sd(m.RA, 0, m.SP),  # Add signed immediate; Save 64-bit register.
        *m.li32(m.T0, 0x84000),  # Load 540672 into T0.
        m.addu(m.S6, m.S4, m.T0),  # Add registers; Load 32-bit constant.
        # The resident loaded id can survive a planet transition even though
        # the hero/texture buffers are reused. Stock skins (including Pirate)
        # must reload too: matching ids do not prove those assets are intact.
        # Invalidate only begin's cached id, preserving the requested id in S3.
        m.addiu(m.S0, m.ZERO, -1),  # Set S0 to ZERO + -1.
        jump(load_model),  # Call 32057888.
        0,
        m.ld(m.RA, 0, m.SP),  # Load RA from SP + 0.
        m.jr(m.RA),  # Jump to RA.
        m.addiu(m.SP, m.SP, 16),  # Set SP to SP + 16.
    )  # Load 64-bit register; Jump to register; Add signed immediate.
    data_edits = []
    for address, payload in [
        (rows, bytes(0x2000)),
        (menu_table, bytes(menu_data)),
        (descriptors, bytes(descriptor_data)),
        (finish, finish_code),
        (stock_finish, read(end, 0xE8)),
        (owned, owned_code),
        (label, label_code),
        (add_row, add_code),
        (begin_fix, fix_code),
        (strings, bytes(text)),
    ]:
        data_edits.append(Patch(address, pine.read_bytes(address, len(payload)), payload))
    table_pointer = mcp + 0x2D4
    previous_table = pine.read_int32(table_pointer)
    if previous_table not in (sp_table, descriptors):
        raise RuntimeError("Hero descriptor pointer already modified")
    data_edits.append(Patch(table_pointer, packed(previous_table), packed(descriptors)))
    # Install the initialized storage before publishing any entry points.
    patch(end, read(end, 8), packed(j(finish), 0))  # Jump to finish.
    plan = Plan(pine, data_edits + edits, expected_game_id=game_id)
    plan.mutable_data = ((rows, 0x2000), (descriptors, len(descriptor_data)))
    plan.buffer, plan.count, plan.finish = buffer, COUNT, finish
    plan.rows, plan.table, plan.descriptors = rows, menu_table, descriptors
    plan.promoted = buffer + PRIMARY_LIMIT
    return plan
