"""Native watchdog: a missed client heartbeat leaves a persistent HUD warning."""

from . import asm as m
from .asm import Patch, jump, packed
from .plan import Plan, supported_game_id

HEARTBEAT_FRAMES = 180
MESSAGE = b"\x90\x03DISCONNECTED FROM ARCHIPELAGO\0"


def prepare(pine, *, arena, font, colour, text):
    game_id = supported_game_id(pine)
    # Vendor reserves [arena, arena + 0x800). Skins occupy +0x100..+0x1f1
    # and Inside Clank's exit occupies +0x300..+0x364.
    entry, heartbeat, message = arena + 0x400, arena + 0x4C0, arena + 0x4C4
    words = [
        *m.li32(m.T0, heartbeat),  # Load heartbeat into T0.
        m.lw(m.T1, 0, m.T0),  # Load word; Load 32-bit constant.
        m.beq(m.T1, m.ZERO, 5),  # Branch 5 words if T1 == ZERO.
        m.NOP,  # Branch if equal; No operation.
        m.addiu(m.T1, m.T1, -1),  # Set T1 to T1 + -1.
        m.sw(m.T1, 0, m.T0),  # Store T1 at T0 + 0.
        m.jr(m.RA),  # Jump to RA.
        m.NOP,  # Add signed immediate; Store word; Jump to register; No operation.
        m.addiu(m.SP, m.SP, -16),  # Set SP to SP + -16.
        m.sd(m.RA, 0, m.SP),  # Add signed immediate; Save 64-bit register.
        m.daddu(m.A0, m.ZERO, m.ZERO),  # Set A0 to ZERO + ZERO.
        jump(font),  # Call font.
        m.daddu(m.A1, m.ZERO, m.ZERO),  # Add 64-bit registers.
        m.lui(m.A0, 0xFFFF),  # Load upper half of A0 with 65535.
        jump(colour),  # Call colour.
        m.ori(m.A0, m.A0, 0xFFFF),  # Load upper immediate; OR immediate.
        *m.li32(m.A2, message),  # Load message into A2.
        m.addiu(m.A0, m.ZERO, 0xEF),  # Add signed immediate; Load 32-bit constant.
        jump(text),  # Call text.
        m.addiu(m.A1, m.ZERO, 0x30),  # Set A1 to ZERO + 48.
        m.ld(m.RA, 0, m.SP),  # Load RA from SP + 0.
        m.jr(m.RA),  # Jump to RA.
        m.addiu(m.SP, m.SP, 16),  # Load 64-bit register; Jump to register; Add signed immediate.
    ]
    payload = packed(*words).ljust(heartbeat - entry, b"\0") + packed(0) + MESSAGE
    plan = Plan(pine, [Patch(entry, pine.read_bytes(entry, len(payload)), payload)], expected_game_id=game_id)
    plan.mutable_data = ((heartbeat, 4),)
    plan.entry, plan.heartbeat, plan.message = entry, heartbeat, message
    return plan


def refresh(plan, connected):
    plan._validate(replacement=True)
    plan.pine.write_int32(plan.heartbeat, HEARTBEAT_FRAMES if connected else 0)
