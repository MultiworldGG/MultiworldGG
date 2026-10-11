"""Open Shrink Ray door interlocks without changing puzzle completion flags."""
import struct

from .asm import packed
from .plan import supported_game_id

SIGNATURE = packed(0x8C830058, 0x90620050, 0x03E00008, 0x0002102B,
                   0x27BDFFC0, 0xFFB20030, 0xFFB00020, 0x0080902D,
                   0xFFB10028, 0xFFBF0038)


def _hits(data, needle):
    pos = data.find(needle)
    while pos >= 0:
        if pos % 4 == 0:
            yield pos
        pos = data.find(needle, pos + 1)


def prepare(pine, *, code_start, code):
    hits = list(_hits(code, SIGNATURE))
    if not hits:
        return None
    if len(hits) != 1:
        raise RuntimeError("Ambiguous Shrink Ray lock class")
    return DoorLocks(pine, code_start + hits[0])


class DoorLocks:
    def __init__(self, pine, getter):
        self.pine, self.getter = pine, getter
        self.game_id = supported_game_id(pine)
        self.installed = False
        self.locks = None
        self.changed = set()

    def _validate(self, replacement=False):
        if self.pine.get_game_id() != self.game_id:
            raise RuntimeError(f"Shrink Ray bypass requires {self.game_id}")
        if self.pine.read_bytes(self.getter, len(SIGNATURE)) != SIGNATURE:
            raise RuntimeError("Shrink Ray module changed")

    def _discover(self):
        # Once per loaded module, after object initialization. Validate class,
        # puzzle id, runtime backlink, and pointers before accepting a lock.
        p = self.pine
        start, end = 0x200000, min(self.getter, 0x1E00000)
        data = b"".join(p.read_bytes(a, min(0x10000, end - a))
                        for a in range(start, end, 0x10000))
        result = []
        for ref in _hits(data, packed(self.getter + 16)):
            cls = start + ref - 0x14
            for ref in _hits(data, packed(cls)):
                moby = start + ref - 0x40
                if not start <= moby <= end - 0x80:
                    continue
                pv, rt = struct.unpack_from('<II', data, moby - start + 0x54)
                if not (start <= pv <= end - 0x20 and start <= rt <= end - 0x58):
                    continue
                puzzle = struct.unpack_from('<I', data, pv - start + 12)[0]
                backlink = struct.unpack_from('<I', data, rt - start + 4)[0]
                if puzzle <= 10 and backlink == moby:
                    result.append((moby, cls, pv, rt, puzzle))
        self.locks = result

    def _valid_lock(self, lock):
        moby, cls, pv, rt, puzzle = lock
        p = self.pine
        return (p.read_int32(moby + 0x40) == cls
                and p.read_int32(cls + 0x14) == self.getter + 16
                and p.read_int32(moby + 0x54) == pv
                and p.read_int32(moby + 0x58) == rt
                and p.read_int32(pv + 12) == puzzle
                and p.read_int32(rt + 4) == moby)

    def install(self):
        self._validate()
        if self.locks is None:
            self._discover()
        for lock in self.locks:
            if not self._valid_lock(lock):
                raise RuntimeError("Shrink Ray object changed; reload the planet")
        for lock in self.locks:
            rt = lock[3]
            # Never interfere with an in-progress puzzle or player restoration.
            if self.pine.read_int32(rt + 0x4C) == 0 and self.pine.read_int8(rt + 0x50):
                self.changed.add(lock)
                self.pine.write_int8(rt + 0x50, 0)
        self.installed = True

    def restore(self):
        self._validate()
        # Restore interlocks only. Native completion still takes precedence;
        # a door already opened may require a level reload to close again.
        flags = self.pine.read_int16(0x1F4B24E if self.game_id == "SCPS-15120" else 0x1F4B40E)
        for lock in self.changed:
            if self._valid_lock(lock) and self.pine.read_int32(lock[3] + 0x4C) == 0:
                self.pine.write_int8(lock[3] + 0x50, int(not flags & (1 << lock[4])))
        self.changed.clear()
        self.installed = False
