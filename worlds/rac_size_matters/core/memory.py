from dataclasses import dataclass, field


@dataclass(slots=True)
class MemoryWindow:
    """An operation-scoped read with writes restricted to explicitly changed bytes."""

    base: int
    data: bytearray
    dirty: set[int] = field(default_factory=set)

    @classmethod
    def read_bytes(cls, pine, base: int, size: int):
        data = pine.read_bytes(base, size)
        if len(data) != size:
            raise ValueError("Incomplete memory snapshot")
        return cls(base, bytearray(data))

    def read(self, address: int, size: int) -> int:
        offset = address - self.base
        return int.from_bytes(self.data[offset : offset + size], "little")

    def write(self, address: int, value: int, size: int) -> None:
        offset = address - self.base
        raw = int(value).to_bytes(size, "little")
        if self.data[offset : offset + size] != raw:
            self.data[offset : offset + size] = raw
            self.dirty.update(range(offset, offset + size))

    def flush(self, pine) -> None:
        writes = []
        remaining = set(self.dirty)
        for offset in sorted(self.dirty):
            if offset not in remaining:
                continue
            size = next(
                size for size in (8, 4, 2, 1) if all(index in remaining for index in range(offset, offset + size))
            )
            writes.append((size, self.base + offset, bytes(self.data[offset : offset + size])))
            remaining.difference_update(range(offset, offset + size))
        if writes:
            pine.batch_write(writes)
        self.dirty.clear()
