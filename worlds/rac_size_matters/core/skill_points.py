from __future__ import annotations

from typing import TYPE_CHECKING

from ..locations import ALL_LOCATIONS
from ..locations.observation import LocationObservation
from . import address_maps
from .address_maps import SKILL_POINTS_BASE as SKILL_POINT_ADDRESS
from .locations.skill_point_locations import (
    CLANK_CHALLENGE_SKILL_POINTS,
    HARD_SKILL_POINTS,
    LOCATION_SKILL_POINTS,
    SKILL_POINT_BY_PLANET_AND_MASK,
    SKILL_POINTS,
    SKYBOARD_CHALLENGE_SKILL_POINTS,
    SkillPoint,
)

if TYPE_CHECKING:
    from ..pypine import Pine

__all__ = [
    "CLANK_CHALLENGE_SKILL_POINTS",
    "HARD_SKILL_POINTS",
    "LOCATION_SKILL_POINTS",
    "SKILL_POINTS",
    "SKILL_POINT_ADDRESS",
    "SKILL_POINT_BY_PLANET_AND_MASK",
    "SKYBOARD_CHALLENGE_SKILL_POINTS",
    "SkillPoint",
    "SkillPointInventory",
]


class SkillPointSlot:
    """Pine-backed accessor for the 5-byte (40-bit) skill-point earned bitmask."""

    address = address_maps.Address("SKILL_POINTS_BASE")

    def __get__(self, instance, owner) -> int | None:
        if instance is None:
            return None
        return int.from_bytes(instance.pine.read_bytes(self.address, 5), "little")

    def __set__(self, instance, value: int) -> None:
        if instance is None:
            return
        instance.pine.write_bytes(self.address, value.to_bytes(5, "little"))

    def __delete__(self, instance) -> None:
        if instance is None:
            return
        instance.pine.write_bytes(self.address, (0).to_bytes(5, "little"))


class SkillPointInventory:
    """Pine-backed live accessor + completion tracking for skill points,
    replacing SkillPointState. Global fixed address — no per-planet base."""

    bits = SkillPointSlot()

    def __init__(self, pine: Pine) -> None:
        self.pine = pine
        self.completed: set[str] = set()
        self._last: int = 0
        self._synced_mask: int = 0

    def get(self, name: str) -> bool:
        return bool(self.bits & SKILL_POINTS[name].mask)

    def set(self, name: str, value: bool) -> None:
        sp = SKILL_POINTS[name]
        current = self.bits
        self.bits = (current | sp.mask) if value else (current & ~sp.mask)

    def delete(self, name: str) -> None:
        self.set(name, False)

    def check(self, current: int | None = None) -> list[str]:
        """Read the earned bitmask and return newly earned AP location names for this call."""
        current = self.bits if current is None else current
        newly_set = current & ~self._last
        self._last = current

        observation = LocationObservation(skill_bits=newly_set)
        newly = [
            name for name in SKILL_POINTS if name not in self.completed and ALL_LOCATIONS[name].completed(observation)
        ]
        self.completed.update(newly)
        return newly

    def sync(self) -> None:
        """Baseline read, applying any AP-synced bits, without reporting anything as newly completed."""
        current = self.bits
        new_val = current | self._synced_mask
        if new_val != current:
            self.bits = new_val
        self._last = new_val

    def sync_from_ap(self, checked_locations: set[str]) -> None:
        mask = 0
        for name, sp in SKILL_POINTS.items():
            if name in checked_locations:
                mask |= sp.mask
                self.completed.add(name)
        self._synced_mask = mask

    def __repr__(self) -> str:
        return f"SkillPointInventory(completed={len(self.completed)}/{len(SKILL_POINTS)})"
