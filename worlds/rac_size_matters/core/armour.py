from __future__ import annotations

from dataclasses import dataclass, replace
from enum import IntEnum, IntFlag

from ..constants import (
    Rac5ClankChallenges,
    Rac5SkyboardChallenges,
)
from ..locations.model import LocationView
from ..locations.shared import LOCATIONS
from ..pypine import Pine
from . import address_maps
from .address_maps import ARMOUR_BASE
from .states.base_state import BaseState

_BOOTS_MASK = 0xF0


class ArmourSet(IntEnum):
    """Value set in armour slots to represent what armour is currently equiped."""

    Wildfire = 1
    Sludge = 2
    Crystallix = 3
    Electroshock = 4
    MegaBomb = 5
    Hyperborean = 6
    Chameleon = 7


class ArmourPiece(IntFlag):
    """Armour pieces are bits in a byte: chestplate 0x01, helmet 0x02, gloves 0x04,
    boots 0x10 (any value with bit 4 set counts as boots equipped)."""

    NONE = 0
    CHESTPLATE = 0x01
    HELMET = 0x02
    GLOVES = 0x04
    BOOTS = 0x10
    ALL = 0x17

    @classmethod
    def from_raw(cls, value: int) -> ArmourPiece:
        """Normalize raw value of armour piece because boots are represented by any value with bit 4 set"""
        normalized = value & 0x0F
        if value & _BOOTS_MASK:
            normalized |= cls.BOOTS
        return cls(normalized)


@dataclass
class ArmourSnapshot:
    """Snapshot of the player's armour state at a given point in time. Any field left as
    None is treated as unset — ArmourStruct.write() skips it and leaves memory untouched."""

    chestplate: ArmourSet | None = None
    helmet: ArmourSet | None = None
    gloves_left: ArmourSet | None = None
    gloves_right: ArmourSet | None = None
    boots_left: ArmourSet | None = None
    boots_right: ArmourSet | None = None
    wildfire: ArmourPiece | None = None
    sludge: ArmourPiece | None = None
    crystallix: ArmourPiece | None = None
    electroshock: ArmourPiece | None = None
    mega_bomb: ArmourPiece | None = None
    hyperborean: ArmourPiece | None = None
    chameleon: ArmourPiece | None = None

    @classmethod
    def read_bytes(cls, raw: bytes) -> ArmourSnapshot:
        if len(raw) != 13:
            raise ValueError("Incomplete armour snapshot")
        slots = [ArmourSet(value) if value else None for value in raw[:6]]
        pieces = [ArmourPiece.from_raw(value) for value in raw[6:]]
        return cls(*slots, *pieces)

    def owned_mask(self) -> int:
        """Bitmask with one bit per armour set (bit i = ArmourStruct.SET_FIELDS order)
        that has any piece owned. None/NONE fields count as not-owned."""
        return sum(1 << i for i, name in enumerate(ArmourStruct.SET_FIELDS) if getattr(self, name))


class ArmourStruct:
    """Batched pine read/write over the full armour block."""

    BASE_ADDRESS = address_maps.Address("ARMOUR_BASE")
    pine: Pine | None = None
    GameState: ArmourSnapshot | None = None

    _fields_ = [
        ("chestplate", Pine.DataSize.INT8),
        ("helmet", Pine.DataSize.INT8),
        ("gloves_left", Pine.DataSize.INT8),
        ("gloves_right", Pine.DataSize.INT8),
        ("boots_left", Pine.DataSize.INT8),
        ("boots_right", Pine.DataSize.INT8),
        ("wildfire", Pine.DataSize.INT8),
        ("sludge", Pine.DataSize.INT8),
        ("crystallix", Pine.DataSize.INT8),
        ("electroshock", Pine.DataSize.INT8),
        ("mega_bomb", Pine.DataSize.INT8),
        ("hyperborean", Pine.DataSize.INT8),
        ("chameleon", Pine.DataSize.INT8),
    ]

    SLOT_FIELDS: tuple[str, ...] = (
        "chestplate",
        "helmet",
        "gloves_left",
        "gloves_right",
        "boots_left",
        "boots_right",
    )
    SET_FIELDS: tuple[str, ...] = (
        "wildfire",
        "sludge",
        "crystallix",
        "electroshock",
        "mega_bomb",
        "hyperborean",
        "chameleon",
    )

    @classmethod
    def _iter_fields(cls):
        """Yield (name, size, address) for each field, laid out back-to-back from BASE_ADDRESS."""
        offset = 0
        for name, size in cls._fields_:
            yield name, size, cls.BASE_ADDRESS + offset
            offset += size

    def read(self) -> None:
        """Batched read of every field, decoded the same way the old per-field descriptors did: a slot is None when unequipped (raw 0) or the matching ArmourSet otherwise; a set is always an ArmourPiece, boots-bit normalized."""
        self.GameState = ArmourSnapshot.read_bytes(self.pine.read_bytes(self.BASE_ADDRESS, 13))

    def write(self, snapshot: ArmourSnapshot) -> None:
        """Write only the fields set on `snapshot` — unset (None) fields are left untouched in memory."""
        writes = [
            (size, address, self.pine.to_bytes(int(value), size))
            for name, size, address in self._iter_fields()
            if (value := getattr(snapshot, name)) is not None
        ]
        self.pine.batch_write(writes)


@dataclass(frozen=True, slots=True)
class ArmourPickup:
    set_key: str
    piece: ArmourPiece
    name: str
    planet: str


EQUIPPED_SLOT_TO_PIECE: dict[str, ArmourPiece] = {
    "chestplate": ArmourPiece.CHESTPLATE,
    "helmet": ArmourPiece.HELMET,
    "gloves_left": ArmourPiece.GLOVES,
    "gloves_right": ArmourPiece.GLOVES,
    "boots_left": ArmourPiece.BOOTS,
    "boots_right": ArmourPiece.BOOTS,
}

ARMOUR_PICKUPS = tuple(
    ArmourPickup(location.completed.key, ArmourPiece(location.completed.mask), location.name, location.planet)
    for location in LOCATIONS
    if location.completed.source == "armour"
)
ARMOUR_FLAG_TO_LOCATION = LocationView(
    LOCATIONS,
    lambda location: location.completed.source == "armour",
    key=lambda location: (location.completed.key, ArmourPiece(location.completed.mask)),
    value=lambda location: location.name,
)

CHALLENGE_LOCATION_TO_ARMOUR_FLAG: dict[str, tuple[str, ArmourPiece]] = {
    Rac5ClankChallenges.METALIS_REVENGE: ("crystallix", ArmourPiece.HELMET),
    Rac5ClankChallenges.METALIS_UBER: ("crystallix", ArmourPiece.GLOVES),
    Rac5ClankChallenges.METALIS_NIGHT: ("sludge", ArmourPiece.GLOVES),
    Rac5ClankChallenges.DAYNI_MOON_SHOWDOWN: ("mega_bomb", ArmourPiece.GLOVES),
    Rac5ClankChallenges.DAYNI_MOON_INFINITE: ("mega_bomb", ArmourPiece.BOOTS),
    Rac5SkyboardChallenges.OUTPOST_OMEGA_VERTIGO: ("electroshock", ArmourPiece.BOOTS),
}


class ArmourInventory(BaseState):
    """Owns a single ArmourStruct plus two logical states: ap_armour (what AP has granted -- the only thing that actually counts as "owned") and game_armour (what's been physically picked up in this playthrough, regardless of AP ownership)."""

    def __init__(self, pine: Pine) -> None:
        super().__init__()
        self.pine = pine
        self.struct = ArmourStruct()
        self.struct.pine = pine
        self.ap_armour: ArmourSnapshot = ArmourSnapshot()
        self.game_armour: ArmourSnapshot = ArmourSnapshot()

    def read(self) -> ArmourSnapshot:
        """Batched read of the full armour block."""
        self.struct.read()
        return self.struct.GameState

    def sync_equipped(self, data: dict[str, int]) -> None:
        """Write an Archipelago data-storage dict into the equipped slots."""
        fields = {name: int(value) for name, value in data.items() if name in ArmourStruct.SLOT_FIELDS}
        self.struct.write(ArmourSnapshot(**fields))

    def set_ap_armour(self, data: dict[str, int]) -> None:
        """Replace ap_armour wholesale (not a merge) from an AP data-storage dict.
        Pure bookkeeping; call apply_full()/apply_collected_only() to write."""
        fields = {
            name: ArmourPiece.from_raw(int(value)) for name, value in data.items() if name in ArmourStruct.SET_FIELDS
        }
        self.ap_armour = ArmourSnapshot(**fields)

    def record_pickup(self, pieces: dict[str, ArmourPiece]) -> None:
        """OR-merge newly detected in-game pickups into game_armour -- purely so check() doesn't re-report the same not-(yet)-AP-owned pickup forever."""
        merged = {name: (getattr(self.game_armour, name) or ArmourPiece.NONE) | piece for name, piece in pieces.items()}
        self.game_armour = replace(self.game_armour, **merged)

    def check(self) -> dict[str, ArmourPiece]:
        """Every-tick diff, titanium-bolt style: read raw memory and return whatever bits aren't already accounted for by ap_armour or game_armour, per set -- i.e."""
        current = self.read()
        new_pieces: dict[str, ArmourPiece] = {}
        for name in ArmourStruct.SET_FIELDS:
            raw = int(getattr(current, name) or 0)
            known = int(getattr(self.ap_armour, name) or 0) | int(getattr(self.game_armour, name) or 0)
            new_bits = raw & ~known
            if new_bits:
                new_pieces[name] = ArmourPiece(new_bits)
        if new_pieces:
            self.record_pickup(new_pieces)
        return new_pieces

    def apply_full(self) -> None:
        """Write ap_armour to memory — only what AP has actually granted."""
        fields = {name: (getattr(self.ap_armour, name) or ArmourPiece.NONE) for name in ArmourStruct.SET_FIELDS}
        self.struct.write(ArmourSnapshot(**fields))

    def apply_collected_only(self) -> None:
        """Write only game_armour — death-sequence state: shows exactly what's been physically found in this playthrough, regardless of AP ownership (deliberately NOT filtered by ap_armour, unlike apply_full() — this is a transient display during the death sequence, not persistent ownership; _handle_respawn()'s apply_full() call corrects everything back to AP truth immediately after)."""
        fields = {name: (getattr(self.game_armour, name) or ArmourPiece.NONE) for name in ArmourStruct.SET_FIELDS}
        self.struct.write(ArmourSnapshot(**fields))

    def clear_unlocked(self) -> None:
        """Zero every unlocked-set byte in memory to open a clean 0->1 pickup-detection
        window; never touches ap_armour/game_armour."""
        self.struct.write(ArmourSnapshot(**dict.fromkeys(ArmourStruct.SET_FIELDS, ArmourPiece.NONE)))

    def __repr__(self) -> str:
        return f"ArmourInventory(ap={self.ap_armour!r}, game={self.game_armour!r})"
