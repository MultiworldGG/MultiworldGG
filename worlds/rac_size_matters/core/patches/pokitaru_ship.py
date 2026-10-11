"""Remove RatchetShip::Init's Ryllus prerequisite on Pokitaru only."""

from . import asm as m
from .asm import Patch, packed
from .plan import Plan

SITE = 0x00EEAB84
SIGNATURE_START = 0x00EEAB78
SIGNATURE = packed(
    0x24020001,
    0x54620007,
    0x8E320058,
    0x0C35CA9C,
    0x24040002,
    0x54400003,
    0x8E320058,
    0x1000004B,
    0x2402FFFF,
)


def prepare(pine, *, gate=None) -> Plan:
    game_id = pine.get_game_id()
    if game_id in ("SCES-55019", "SCPS-15120"):
        module_base, signature_start, available = {
            "SCES-55019": (0xD49F80, 0xEEAC28, 0xD71768),
            "SCPS-15120": (0xD4A780, 0xEEA490, 0xD71F78),
        }[game_id]
        # EU retail capture: the surrounding instructions are unchanged, but
        # the availability call and its site moved independently of US.
        delta = 0
        if gate is not None:
            held = gate.held_module()
            if gate.pine is not pine or held is None or held[0] != 1:
                raise RuntimeError("Pokitaru must be held before level startup")
            delta = held[1] - module_base
        elif pine.read_int32(0x1F4C5AC if game_id == "SCPS-15120" else 0x1F4C76C) != 1:
            raise RuntimeError("Ship patch requires Pokitaru")
        signature = bytearray(SIGNATURE)
        signature[12:16] = packed(0x0C000000 | ((available + delta) >> 2))
        start = signature_start + delta
        if pine.read_bytes(start, len(signature)) != signature:
            raise RuntimeError("Regional Pokitaru ship initialization signature changed")
        return Plan(
            pine,
            [Patch(start + 12, bytes(signature[12:16]), packed(m.addiu(m.V0, m.ZERO, 1)))],
            expected_game_id=game_id,
        )
    if gate is not None:
        held = gate.held_module()
        if gate.pine is not pine or held is None or held[0] != 1:
            raise RuntimeError("Pokitaru must be held before level startup")
        delta = held[1] - 0xD4B380
    else:
        delta = 0
    if pine.get_game_id() != "SCUS-97615" or (gate is None and pine.read_int32(0x1F4C76C) != 1):
        raise RuntimeError("Ship patch requires US PS2 Pokitaru")
    # The call relocates with the module; the branch and register-relative
    # instructions do not. Derive its expected target from the loaded base.
    signature = bytearray(SIGNATURE)
    signature[12:16] = packed(0x0C000000 | ((0xD72A70 + delta) >> 2))
    if pine.read_bytes(SIGNATURE_START + delta, len(signature)) != signature:
        raise RuntimeError("Pokitaru ship initialization signature changed")
    # Replace only the call testing planet 2's availability. The existing
    # success branch loads s2 and continues normal ship initialization.
    return Plan(
        pine,
        [Patch(SITE + delta, bytes(signature[12:16]), packed(m.addiu(m.V0, m.ZERO, 1)))],  # Set V0 to ZERO + 1.
    )  # Add signed immediate.
