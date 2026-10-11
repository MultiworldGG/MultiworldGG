"""Render-only item message, with no prompt state or controller writes."""

import re
import struct

from . import asm as m
from .asm import Patch, jump, packed
from .plan import Plan, supported_game_id


def prepare(pine, *, code_start, code, small_box, starter, frame_hook=None, status_hook=None, balance_hook=None):
    game_id = supported_game_id(pine)
    def read(address, count):
        offset = address - code_start
        if not 0 <= offset <= len(code) - count:
            raise RuntimeError("Item message code outside loaded module")
        return code[offset : offset + count]

    def target(address):
        (word,) = struct.unpack("<I", read(address, 4))
        if word >> 26 != 3:
            raise RuntimeError("Item message renderer call changed")
        return (word & 0x3FFFFFF) << 2

    signature = packed(
        0x27BDFFD0,
        0x3C020000 | ((small_box + 0x8000) >> 16),
        0xFFB00010,
        0x24420000 | (small_box & 0xFFFF),
        0xFFBF0018,
        0x00048080,
        0xE7B40020,
    )
    hits = [i for i in range(0, len(code) - len(signature), 4) if code[i : i + len(signature)] == signature]
    if len(hits) != 1:
        raise RuntimeError("Expected one small-prompt renderer")
    draw = code_start + hits[0]
    wrapper = draw + 0x190
    expected = packed(0x27BDFFF0, 0xFFBF0000, jump(draw), 0x0000202D, 0xDFBF0000, 0x03E00008, 0x27BD0010)  # Call draw.
    if read(wrapper, len(expected)) != expected:
        raise RuntimeError("Small-prompt renderer wrapper changed")
    font, colour, text = (target(draw + offset) for offset in (0x30, 0xCC, 0x100))
    if read(starter + 0xF8, 12) != packed(0xDFBF0000, 0x03E00008, 0x27BD0010):
        raise RuntimeError("Starter storage boundary changed")
    entry = starter + 32
    timer = entry + 128
    message = timer + 4
    words = [
        m.addiu(m.SP, m.SP, -16),  # Set SP to SP + -16.
        m.sd(m.RA, 8, m.SP),  # Store RA at SP + 8.
        jump(draw),  # Call draw.
        m.daddu(m.A0, m.ZERO, m.ZERO),  # Add signed immediate; Save 64-bit register; Add 64-bit registers.
        m.lui(m.T0, (timer + 0x8000) >> 16),  # Load upper half of T0 with timer + 32768 >> 16.
        m.lw(m.T1, timer & 0xFFFF, m.T0),  # Load T1 from T0 + timer & 65535.
        m.beq(m.T1, m.ZERO, 27 - 6 - 1),  # empty -> epilogue (word 27)
        m.addiu(m.T1, m.T1, -1),  # Set T1 to T1 + -1.
        m.sw(m.T1, timer & 0xFFFF, m.T0),  # Store T1 at T0 + timer & 65535.
        m.daddu(m.A0, m.ZERO, m.ZERO),  # Set A0 to ZERO + ZERO.
        jump(font),  # Call font.
        m.daddu(m.A1, m.ZERO, m.ZERO),  # Add 64-bit registers.
        m.lui(m.A0, 0xFFFF),  # Load upper half of A0 with 65535.
        jump(colour),  # Call colour.
        m.ori(m.A0, m.A0, 0xFFFF),  # Load upper immediate; OR immediate.
        m.lui(m.A2, (message + 0x8000) >> 16),  # Load upper half of A2 with message + 32768 >> 16.
        m.addiu(m.A2, m.A2, message & 0xFFFF),  # Set A2 to A2 + message & 65535.
        m.addiu(m.A0, m.ZERO, 0xEF),  # Set A0 to ZERO + 239.
        jump(text),  # Call text.
        m.addiu(m.A1, m.ZERO, 0xCD),  # Set A1 to ZERO + 205.
    ]
    if frame_hook is not None:
        # Run with no notification too; preserve the fixed data offsets.
        words[2:2] = [jump(frame_hook), m.NOP]  # Call frame_hook.
        words[8] = m.beq(m.T1, m.ZERO, 27 - 8 - 1)  # Branch 27 - 8 - 1 words if T1 == ZERO.
    if status_hook is not None:
        # Draw after the native prompt, even when no item message is queued.
        insert = 6 if frame_hook is not None else 4
        words[insert:insert] = [jump(status_hook), m.NOP]  # Call status_hook.
        empty_branch = 10 if frame_hook is not None else 8
        words[empty_branch] = m.beq(
            m.T1, m.ZERO, 27 - empty_branch - 1
        )  # Branch 27 - empty_branch - 1 words if T1 == ZERO.
    if balance_hook is not None:
        # A third callback still fits before the fixed epilogue/data offsets.
        words[2:2] = [jump(balance_hook), m.NOP]
        empty_branch = 8 + (2 if frame_hook is not None else 0) + (2 if status_hook is not None else 0)
        words[empty_branch] = m.beq(m.T1, m.ZERO, 27 - empty_branch - 1)
    if len(words) > 27:
        raise RuntimeError("Item message callbacks exceed reserved storage")
    words += [0] * (27 - len(words))
    words += [
        m.ld(m.RA, 8, m.SP),  # Load RA from SP + 8.
        m.jr(m.RA),  # Jump to RA.
        m.addiu(m.SP, m.SP, 16),  # Set SP to SP + 16.
        m.NOP,
        m.NOP,
    ]  # Load 64-bit register; Jump to register; Add signed immediate; No operation.
    replacement = packed(*words) + bytes(100)
    plan = Plan(
        pine,
        [
            Patch(entry, read(entry, len(replacement)), replacement),
            Patch(wrapper + 8, packed(jump(draw)), packed(jump(entry))),  # Call draw. Call entry.
        ],
        expected_game_id=game_id,
    )
    plan.mutable_data = ((timer, 100),)
    plan.timer, plan.message = timer, message
    plan.font, plan.colour, plan.text = font, colour, text
    return plan


def format_text(value):
    data = _wrap_text(value)
    if len(data) <= 96:
        return data
    result = bytearray()
    for token in re.findall(rb"\x90[\s\S]|[^\x90]", data[:-1]):
        if len(result) + len(token) > 92:
            break
        result.extend(token)
    return bytes(result) + b"...\0"


def _wrap_text(value):
    """Wrap visible characters while retaining complete native colour pairs."""
    raw = (
        bytes(value) if isinstance(value, (bytes, bytearray)) else str(value).encode("ascii", errors="replace")
    ).split(b"\0", 1)[0]
    result = bytearray()
    line, width = 0, 0
    words = raw.replace(b"\n", b" \n ").split(b" ")
    for word_index, word in enumerate(words):
        if word == b"\n":
            if line:
                result.extend(b"...")
                break
            result.extend(b"\n")
            line, width = 1, 0
            continue
        tokens = re.findall(rb"\x90[\s\S]|[^\x90]", word)
        visible = sum(len(t) == 1 for t in tokens)
        if width and width + 1 + visible > 42:
            if line:
                result.extend(b"...")
                break
            result.extend(b"\n")
            line, width = 1, 0
        elif width and word:
            result.extend(b" ")
            width += 1
        for token in tokens:
            if len(result) + len(token) > 92 or (len(token) == 1 and width == 42 and line):
                return bytes(result) + b"...\0"
            if len(token) == 1 and width == 42:
                result.extend(b"\n")
                line, width = 1, 0
            result.extend(token)
            width += len(token) == 1
    return bytes(result) + b"\0"


def show(plan, value):
    """Publish text first, then activate it; never touch native prompt flags."""
    data = format_text(value)
    plan._validate(replacement=True)
    plan.pine.write_int32(plan.timer, 0)
    plan.pine.write_bytes(plan.message, data.ljust(96, b"\0"))
    plan.pine.write_int32(plan.timer, 180)
