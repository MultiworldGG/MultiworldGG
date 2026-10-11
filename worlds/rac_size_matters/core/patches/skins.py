"""Expose Trash Ratchet and apply queued skins using the native menu routines."""

import struct

from . import asm as m
from .asm import Patch, jump, packed
from .loader_gate import LoaderGate
from .plan import Plan, supported_game_id

MODEL_IDS = (0, 5, 4, 6, 3, 1, 2) + tuple(range(7, 20))


def prepare(pine, *, code_start, code, arena, menu, model_count=7):
    if model_count not in (7, len(MODEL_IDS)):
        raise ValueError("Unsupported skin model count")
    game_id = supported_game_id(pine)
    loader_state = LoaderGate(pine, game_id=game_id).STATE

    def read(address, size):
        offset = address - code_start
        if not 0 <= offset <= len(code) - size:
            raise RuntimeError("Skin code outside loaded module")
        return code[offset : offset + size]

    def unique(signature):
        hits = [i for i in range(0, len(code) - len(signature) + 1, 4) if code[i : i + len(signature)] == signature]
        if len(hits) != 1:
            raise RuntimeError("Expected one native skin menu signature")
        return code_start + hits[0]

    def call(address):
        (word,) = struct.unpack("<I", read(address, 4))
        if word >> 26 != 3:
            raise RuntimeError("Native skin call changed")
        return (word & 0x3FFFFFF) << 2

    jp = game_id == "SCPS-15120"
    gate = unique(
        packed(0x8E050000, 0x0220302D, 0xAFB30000, 0x0240202D, 0x0000382D)
        if jp else packed(0x8E030000, 0x1074000A, 0x0240202D, 0x8E050008)
    )
    close = unique(packed(0x806402E0, 0x10A40007))
    if read(close + 12, 4) != packed(0x00A0202D) or read(close + 20, 4) != packed(0x24050001):
        raise RuntimeError("Native skin application sequence changed")
    begin, finish = call(close + 16), call(close + 24)
    if (
        read(begin, 4) != packed(0x27BDFFB0)
        or read(begin + 12, 4) != packed(0x2407FFFF)
        or read(finish, 4) != packed(0x27BDFFB0)
        or read(finish + 12, 4) != packed(0x2402FFFF)
    ):
        raise RuntimeError("Native skin loader changed")
    # Reuse the menu's save-pointer load and model-id store after a successful
    # load. This is distinct from the saved menu selection byte at SKIN_BASE+1.
    upper = read(close + 32, 4)
    load = read(close + 40, 4)
    if (
        int.from_bytes(upper, "little") & 0xFFFF0000 != 0x3C020000
        or int.from_bytes(load, "little") & 0xFFFF0000 != 0x8C430000
        or read(close + 44, 4) != packed(0xA0641C7E)
    ):
        raise RuntimeError("Native skin save sequence changed")

    entry, request = arena + 0x100, arena + 0x1F0
    words = []
    exits = []

    def guard(register):
        exits.append(len(words))
        words.extend([m.bne(register, m.ZERO, 0), m.NOP])  # Branch if unequal; No operation.

    words += [m.lui(m.T0, (menu + 0x8000) >> 16), m.lw(m.T1, menu & 65535, m.T0)]  # Load upper immediate; Load word.
    guard(m.T1)
    words += [m.lw(m.T1, (menu + 4) & 65535, m.T0)]  # Load T1 from T0 + menu + 4 & 65535.
    guard(m.T1)
    words += [
        *m.li32(m.T0, loader_state),
        m.lw(m.T1, 0, m.T0),  # Load T1 from T0 + 0.
        m.xori(m.T1, m.T1, 6),  # Set T1 to T1 ^ 6.
    ]  # Load word; XOR immediate; Load 32-bit constant.
    guard(m.T1)
    words += [
        *m.li32(m.T0, request),  # Load request into T0.
        m.lbu(m.A0, 0, m.T0),  # Load A0 from T0 + 0.
        m.sltiu(m.T1, m.A0, model_count),  # Set T1 to A0 < model_count.
    ]  # Load byte; Compare unsigned immediate; Load 32-bit constant.
    exits.append(len(words))
    words += [
        m.beq(m.T1, m.ZERO, 0),  # Branch 0 words if T1 == ZERO.
        m.NOP,  # Branch if equal; No operation.
        m.addiu(m.SP, m.SP, -16),  # Set SP to SP + -16.
        m.sd(m.RA, 0, m.SP),  # Store RA at SP + 0.
        m.sw(m.A0, 8, m.SP),  # Add signed immediate; Save 64-bit register; Store word.
        m.addiu(m.T1, m.ZERO, 255),  # Set T1 to ZERO + 255.
        m.sb(m.T1, 0, m.T0),  # Add signed immediate; Store byte.
        jump(begin),  # Call begin.
        m.addiu(m.A1, m.ZERO, 1),  # Set A1 to ZERO + 1.
    ]  # Add signed immediate.
    failed = len(words)
    words += [m.beq(m.V0, m.ZERO, 0), m.NOP, jump(finish), m.NOP]  # Branch if equal; No operation.
    failed_finish = len(words)
    words += [
        m.beq(m.V0, m.ZERO, 0),  # Branch 0 words if V0 == ZERO.
        m.NOP,  # Branch if equal; No operation.
        int.from_bytes(upper, "little"),
        int.from_bytes(load, "little"),
        m.lw(m.A0, 8, m.SP),  # Load A0 from SP + 8.
        m.sb(m.A0, 0x1C7E, m.V1),  # Store A0 at V1 + 7294.
    ]  # Load word; Store byte.
    epilogue = len(words)
    words += [m.ld(m.RA, 0, m.SP), m.addiu(m.SP, m.SP, 16)]  # Load 64-bit register; Add signed immediate.
    end = len(words)
    words += [m.jr(m.RA), m.NOP]  # Jump to register; No operation.
    for index in exits:
        words[index] |= end - index - 1
    for index in (failed, failed_finish):
        words[index] |= epilogue - index - 1
    payload = packed(*words)
    if len(payload) > request - entry:
        raise RuntimeError("Skin callback exceeds reserved storage")
    payload = payload.ljust(request - entry, b"\0") + b"\xff"
    plan = Plan(
        pine,
        [
            *([] if jp else [Patch(gate + 4, packed(0x1074000A), packed(m.NOP))]),
            Patch(entry, pine.read_bytes(entry, len(payload)), payload),
        ],
        expected_game_id=game_id,
    )
    plan.mutable_data = ((request, 1),)
    plan.entry, plan.request = entry, request
    plan.begin, plan.finish = begin, finish
    plan.model_count = model_count
    plan.menu_anchor = gate
    return plan
