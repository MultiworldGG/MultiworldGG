"""Intercept Ryllus' scripted Sprout-o-Matic handoff."""

from . import asm as m
from .asm import Patch, branch, packed
from .plan import Plan

START = 0x00F06610
JOURNAL = START + 0x50
SIGNATURE = packed(
    0x27BDFFF0,
    0x0080402D,
    0xFFBF0000,
    0x240A0002,
    0x24040011,
    0x2406FFFF,
    0x8D020064,
    0x24070001,
    0x8D090058,
    0x24050001,
    0x34420020,
    0xAD020064,
    0x8D230000,
    0x8C620064,
    0x34420020,
    0xAC620064,
    0x0C356180,
    0xA10A0045,
    0x3C0400F8,
    0x24050011,
    0x0C355C1C,
    0x2484F1D0,
    0x3C0200F6,
    0x0C39B074,
    0x8C4422F0,
    0xDFBF0000,
    0x03E00008,
    0x27BD0010,
)


def prepare(pine, *, checked=False, gate=None):
    game_id = pine.get_game_id()
    start, signature = START, SIGNATURE
    gate_original = packed(0x24040011, 0x0C3560EA, 0x2405FFFF)
    if game_id == "SCES-55019":
        start = 0x00F06708
        signature = bytearray(SIGNATURE)
        for offset, word in ((0x40, 0x0C355CB0), (0x50, 0x0C355732),
                             (0x54, 0x2484F250), (0x5C, 0x0C39B026),
                             (0x60, 0x8C442390)):
            signature[offset:offset + 4] = packed(word)
        signature = bytes(signature)
        gate_original = packed(0x24040011, 0x0C355C1A, 0x2405FFFF)
    elif game_id == "SCPS-15120":
        start = 0x00F060D8
        signature = bytearray(SIGNATURE)
        for offset, word in ((0x40, 0x0C355EC0), (0x50, 0x0C35595C),
                             (0x54, 0x2484ED50), (0x5C, 0x0C39AE9E),
                             (0x60, 0x8C441E10)):
            signature[offset:offset + 4] = packed(word)
        signature = bytes(signature)
        gate_original = packed(0x24040011, 0x0C355E2A, 0x2405FFFF)
    journal = start + 0x50
    held = gate.held_module() if gate is not None else None
    correct_level = (
        held is not None and held[0] == 2 and gate.pine is pine if gate is not None else pine.read_int32(0x1F4C5AC if game_id == "SCPS-15120" else 0x1F4C76C) == 2
    )
    if game_id not in ("SCUS-97615", "SCES-55019", "SCPS-15120") or not correct_level:
        raise RuntimeError("Sprout pickup patch requires US, EU or JP PS2 Ryllus")
    if pine.read_bytes(start, len(signature)) != signature:
        raise RuntimeError("Sprout pickup signature changed")
    replacement = (
        packed(
            m.lui(m.V0, (journal + 0x8000) >> 16),
            0xA10A0045,  # retain object state change (original instruction)
            branch(start + 0x48, start + 0x58),
            m.sb(m.T2, journal & 0xFFFF, m.V0),  # t2 is still 2 (no setter call)
        )
        + bytes([2 if checked else 1])
        + b"SMPICK!"
    )
    gate_address = start - 0xC4
    if pine.read_bytes(gate_address, 12) != gate_original:
        raise RuntimeError("Sprout pickup ownership gate changed")
    gate_code = packed(
        m.lui(m.V0, (journal + 0x8000) >> 16),
        m.lbu(m.V0, journal & 0xFFFF, m.V0),
        m.addiu(m.V0, m.V0, -1),  # Set V0 to V0 + -1.
    )  # Load byte; Add signed immediate.
    plan = Plan(
        pine, [Patch(start + 0x40, signature[0x40:0x58], replacement), Patch(gate_address, gate_original, gate_code)],
        expected_game_id=game_id,
    )
    plan.journals = ((journal, 1),)
    return plan
