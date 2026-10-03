from dataclasses import dataclass


@dataclass
class RomPatchEntry:
    bank: int
    address: int
    data: list[int]
    # only write if the ROM currently holds these bytes (overrides apply after token writes)
    expected: list[int] | None = None

    @property
    def rom_offset(self) -> int:
        if self.bank == 0:
            return self.address
        return (self.bank * 0x4000) + (self.address - 0x4000)


@dataclass
class RomPatch:
    name: str
    entries: list[RomPatchEntry]


ROM_PATCHES: list[RomPatch] = []
