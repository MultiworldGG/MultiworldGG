from dataclasses import dataclass
from typing import Literal, ClassVar

from ..characters import Character
from ...character_ability import CharacterAbility

CHARACTER_ITEMS_BASE = 1_000
# Vehicles are actually just huge characters that get used in huge levels.
VEHICLE_ITEMS_BASE = CHARACTER_ITEMS_BASE
EXTRA_ITEMS_BASE = 2_000
GENERIC_ITEMS_BASE = 3_000


ItemType = Literal["Character", "Vehicle", "Extra", "Generic", "Minikit"]


@dataclass(frozen=True)
class GenericItemData:
    code: int | None
    name: str
    item_type: ClassVar[ItemType] = "Generic"

    @property
    def is_sendable(self):
        return self.code is not None


@dataclass(frozen=True)
class GenericCharacterData(GenericItemData):
    character: Character
    abilities: CharacterAbility

    def __lt__(self, other: "GenericCharacterData") -> bool:
        return self.character < other.character


@dataclass(frozen=True)
class MinikitItemData(GenericItemData):
    bundle_size: int
    item_type: ClassVar[ItemType] = "Minikit"