"""The 0x10-byte message text record used by the game."""

from dataclasses import dataclass
from struct import Struct
from typing import ClassVar


# Byte layout of a single string table entry in memory (16 bytes, little-endian).
# UInt32 UInt32 Int32 Int16 UInt16
STRING_ENTRY_FORMAT = Struct("<IIihH")


@dataclass
class StringTableEntry:
    SIZE: ClassVar[int] = STRING_ENTRY_FORMAT.size

    text_pointer: int
    text_id: int
    voice_clip_index: int
    alternate_text_id: int
    portrait_selector: int

    @classmethod
    def from_bytes(cls, data: bytes, offset: int = 0) -> "StringTableEntry":
        return cls(*STRING_ENTRY_FORMAT.unpack_from(data, offset))
