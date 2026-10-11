"""Checked, regional port of usernamecipher's Update 1.03.

Install immutable edits while the loader is held. The two conditional sections
run in the native HUD callback, so their timers count game frames, not PINE polls.
"""

from . import asm as m
from .asm import Patch, packed
from .balance_data import BOSS_HEALTH, PATCHES_BY_PLANET
from .balance_types import REGIONS
from .loader_gate import LoaderGate
from .plan import Plan, supported_game_id


def prepare(pine, *, planet, code_start, code):
    game_id = supported_game_id(pine)
    region = REGIONS[game_id]
    edits = []
    boss = []
    for group in PATCHES_BY_PLANET.get(planet, ()):
        for edit in group.edits(region):
            address = code_start + edit.offset
            expected = packed(edit.original)
            if code[edit.offset:edit.offset + 4] != expected:
                raise RuntimeError(f"Balance patch signature changed for {edit.name} at {address:#x}")
            edits.append(Patch(address, expected, packed(edit.replacement)))
            if edit.replacement != edit.boss:
                boss.append((address, edit.replacement, edit.boss))
    if not edits:
        return None
    plan = Plan(pine, edits, expected_game_id=game_id)
    # The callback alternates these words between the normal and boss values.
    plan.mutable_data = tuple((address, 4) for address, _, _ in boss)
    plan.boss = boss
    plan.planet = planet
    plan.code_start = code_start
    if planet == 10:
        health = BOSS_HEALTH.for_region(region)
        if code[health - 4:health + 12] != packed(*([0x42C80000] * 4)):
            raise RuntimeError("Balance patch boss-health layout changed")
        plan.health = code_start + health
    return plan


# Transform of the Ryllus gadgetbot door, verified against the identical US/JP
# scene asset 86880e3e (EU's entire Ryllus WAD is byte-identical to US).
DOOR_POSITION = bytes.fromhex("367f8842c298ce413e82ccc20000803f")


def _door_records(pine):
    start, end = 0x200000, 0xC00000
    data = b"".join(pine.read_bytes(a, 0x10000) for a in range(start, end, 0x10000))
    hits = []
    pos = data.find(DOOR_POSITION)
    while pos >= 0:
        if pos % 16 == 0:
            actor = start + pos - 0x30
            pointer = packed(actor)
            ref = data.find(pointer)
            while ref >= 0:
                if (
                    ref % 4 == 0
                    and data[ref + 16:ref + 20] == pointer
                    and data[ref + 4:ref + 8] == bytes(4)
                    and data[ref + 20:ref + 24] == bytes(4)
                    and int.from_bytes(data[ref + 8:ref + 12], "little") in (0, 3)
                    and int.from_bytes(data[ref + 24:ref + 28], "little") in (0, 3)
                ):
                    hits.append((start + ref, actor))
                ref = data.find(pointer, ref + 1)
        pos = data.find(DOOR_POSITION, pos + 1)
    if len(hits) != 1:
        raise RuntimeError("Expected one Ryllus gadgetbot door event pair")
    return hits[0]


class _Code:
    def __init__(self):
        self.words, self.labels, self.branches = [], {}, []

    def emit(self, *words):
        self.words.extend(words)

    def label(self, name):
        self.labels[name] = len(self.words)

    def branch(self, op, left, right, label):
        self.branches.append((len(self.words), label))
        self.emit(op(left, right, 0), m.NOP)

    def finish(self):
        for index, label in self.branches:
            self.words[index] |= (self.labels[label] - index - 1) & 0xFFFF
        return packed(*self.words)


def prepare_callback(pine, *, balance, arena, max_health, toast):
    """Use vendor-reserved storage, disjoint from skins and connection warnings."""
    if balance.planet not in (2, 10):
        return None
    game_id = balance.expected_game_id
    entry, counter, message = arena + 0x500, arena + 0x200, arena + 0x204
    reminder = b"Otto: Your ammo has been refilled!\0"
    code = _Code()
    code.emit(*m.li32(m.T0, LoaderGate(pine, game_id=game_id).STATE), m.lw(m.T1, 0, m.T0),
              m.addiu(m.T2, m.ZERO, 6))
    code.branch(m.bne, m.T1, m.T2, "return")
    if balance.planet == 2:
        # Scene runtime records do not exist until object initialization. The
        # client publishes these two pointers after gameplay becomes ready.
        code.emit(*m.li32(m.T0, counter + 0x40), m.lw(m.T5, 0, m.T0), m.lw(m.T6, 4, m.T0))
        code.branch(m.beq, m.T5, m.ZERO, "return")
        code.emit(*m.li32(m.T0, max_health), m.lw(m.T1, 0, m.T0), m.srl(m.T1, m.T1, 16),
                  m.addiu(m.T2, m.ZERO, 0x4080))
        code.branch(m.bne, m.T1, m.T2, "return")
        code.emit(*m.li32(m.T0, counter), m.lw(m.T1, 0, m.T0), m.sltiu(m.T2, m.T1, 70))
        code.branch(m.beq, m.T2, m.ZERO, "return")
        code.emit(m.addiu(m.T1, m.T1, 1), m.sw(m.T1, 0, m.T0), m.addiu(m.T2, m.ZERO, 60))
        code.branch(m.bne, m.T1, m.T2, "return")
        code.emit(m.lw(m.T1, 0, m.T5))
        code.branch(m.bne, m.T1, m.T6, "return")
        code.emit(m.lw(m.T1, 16, m.T5))
        code.branch(m.bne, m.T1, m.T6, "return")
        code.emit(m.sw(m.ZERO, 8, m.T5), m.sw(m.ZERO, 24, m.T5))
    else:
        # Compare the upper halfword exactly as the original extended codes do.
        code.emit(*m.li32(m.T0, balance.health), m.lw(m.T1, 0, m.T0), m.srl(m.T1, m.T1, 16),
                  m.addiu(m.T4, m.ZERO, 4), m.sltiu(m.T2, m.T1, 0x45BC))
        code.branch(m.beq, m.T2, m.ZERO, "apply")
        code.emit(m.sltiu(m.T2, m.T1, 0x43FA))
        code.branch(m.bne, m.T2, m.ZERO, "apply")
        code.emit(m.addiu(m.T4, m.ZERO, 8))
        code.label("apply")
        table_load = len(code.words)
        code.emit(0, 0, m.addiu(m.T3, m.ZERO, len(balance.boss)))
        code.label("loop")
        code.emit(m.lw(m.T1, 0, m.T0), m.addu(m.T2, m.T0, m.T4), m.lw(m.T2, 0, m.T2),
                  m.sw(m.T2, 0, m.T1), m.addiu(m.T0, m.T0, 12), m.addiu(m.T3, m.T3, -1))
        code.branch(m.bne, m.T3, m.ZERO, "loop")
        code.emit(m.addiu(m.T2, m.ZERO, 8))
        code.branch(m.bne, m.T4, m.T2, "return")
        code.emit(*m.li32(m.T0, counter), m.lw(m.T1, 0, m.T0), m.sltiu(m.T2, m.T1, 45))
        code.branch(m.beq, m.T2, m.ZERO, "notify")
        code.emit(m.addiu(m.T1, m.T1, 1), m.sw(m.T1, 0, m.T0))
        code.label("notify")
        code.emit(m.addiu(m.T2, m.ZERO, 45))
        code.branch(m.bne, m.T1, m.T2, "return")
        code.emit(*m.li32(m.T2, toast.timer), m.lw(m.T3, 0, m.T2))
        code.branch(m.bne, m.T3, m.ZERO, "return")
        code.emit(m.addiu(m.T1, m.ZERO, 46), m.sw(m.T1, 0, m.T0),
                  *m.li32(m.T0, message), *m.li32(m.T1, toast.message),
                  m.addiu(m.T3, m.ZERO, len(reminder)))
        code.label("copy")
        code.emit(m.lbu(m.T4, 0, m.T0), m.sb(m.T4, 0, m.T1), m.addiu(m.T0, m.T0, 1),
                  m.addiu(m.T1, m.T1, 1), m.addiu(m.T3, m.T3, -1))
        code.branch(m.bne, m.T3, m.ZERO, "copy")
        code.emit(m.addiu(m.T1, m.ZERO, 180), m.sw(m.T1, 0, m.T2))
    code.label("return")
    code.emit(m.jr(m.RA), m.NOP)
    if balance.planet == 10:
        table = entry + len(code.words) * 4
        code.words[table_load:table_load + 2] = m.li32(m.T0, table)
    payload = code.finish() + b"".join(packed(*row) for row in balance.boss)
    if len(payload) > 0x300:
        raise RuntimeError("Balance callback exceeds reserved storage")
    scratch = (bytes(4) + reminder).ljust(0x48, b"\0")
    plan = Plan(pine, [
        Patch(entry, pine.read_bytes(entry, len(payload)), payload),
        Patch(counter, pine.read_bytes(counter, len(scratch)), scratch),
    ], expected_game_id=game_id)
    plan.mutable_data = ((counter, 4), (counter + 0x40, 8))
    plan.entry, plan.counter = entry, counter
    plan.needs_doors = balance.planet == 2
    return plan


def bind_doors(plan):
    """Resolve the scene by its transform and event records, never a region delta."""
    plan._validate(replacement=True)
    record, actor = _door_records(plan.pine)
    plan.pine.write_int32(plan.counter + 0x44, actor)
    # Publish last so the native callback cannot observe a partial pair.
    plan.pine.write_int32(plan.counter + 0x40, record)
    plan.needs_doors = False
