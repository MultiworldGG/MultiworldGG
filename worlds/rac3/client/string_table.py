"""Location of the active string table in memory."""

from dataclasses import dataclass
from typing import ClassVar


@dataclass
class StringTable:
    MAX_ENTRIES: ClassVar[int] = 0x4000

    game_id: str
    planet: str
    base_address: int
    first_text_address: int
