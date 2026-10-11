"""Named records for the regional balance tables; all stored values are words."""

import struct
from dataclasses import dataclass
from enum import IntEnum


class Region(IntEnum):
    US = 0
    EU = 1
    JP = 2


REGIONS = {"SCUS-97615": Region.US, "SCES-55019": Region.EU, "SCPS-15120": Region.JP}


def f32(value: float) -> int:
    """Encode a readable gameplay value as its exact little-endian float32 word."""
    return struct.unpack("<I", struct.pack("<f", value))[0]


@dataclass(frozen=True)
class RegionalOffsets:
    """Offsets from the loaded SNR2 module, never absolute EE addresses."""

    us: int
    eu: int
    jp: int

    def for_region(self, region: Region) -> int:
        return {Region.US: self.us, Region.EU: self.eu, Region.JP: self.jp}[region]


@dataclass(frozen=True)
class RegionalWords:
    """Shared US values with explicit EU/JP overrides only when they differ."""

    us: tuple[int, ...]
    eu: tuple[int, ...] | None = None
    jp: tuple[int, ...] | None = None

    def for_region(self, region: Region) -> tuple[int, ...]:
        override = {Region.US: self.us, Region.EU: self.eu, Region.JP: self.jp}[region]
        return self.us if override is None else override


@dataclass(frozen=True)
class BalanceEdit:
    name: str
    offset: int
    original: int
    replacement: int
    boss: int


@dataclass(frozen=True)
class PatchGroup:
    """One named effect: level-ordered damage rows or consecutive instructions.

    Damage tables use stride 0x10, with values ordered level 1 through level 4.
    Instruction sequences use stride 4 and retain literal MIPS words.
    An omitted boss override uses the normal replacement in every region.
    """

    name: str
    offsets: RegionalOffsets
    original: RegionalWords
    replacement: RegionalWords
    stride: int = 4
    boss: RegionalWords | None = None

    def __post_init__(self):
        count = len(self.original.us)
        if not count or self.stride <= 0 or self.stride % 4:
            raise ValueError(f"Invalid balance patch layout: {self.name}")
        for region in Region:
            if self.offsets.for_region(region) % 4:
                raise ValueError(f"Unaligned balance patch offset: {self.name}")
            for values in (self.original, self.replacement, self.boss):
                if values is not None and len(values.for_region(region)) != count:
                    raise ValueError(f"Mismatched regional word counts: {self.name}")

    def edits(self, region: Region):
        offset = self.offsets.for_region(region)
        original = self.original.for_region(region)
        replacement = self.replacement.for_region(region)
        boss = (self.boss or self.replacement).for_region(region)
        for index, (before, after, conditional) in enumerate(zip(original, replacement, boss, strict=True)):
            yield BalanceEdit(self.name, offset + index * self.stride, before, after, conditional)
