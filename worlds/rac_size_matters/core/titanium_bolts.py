from __future__ import annotations

from typing import TYPE_CHECKING

from ..locations import ALL_LOCATIONS
from ..locations.observation import LocationObservation
from . import address_maps
from .address_maps import TITANIUM_BOLT_BASE
from .locations.titanium_bolt_locations import BOLT_BY_PLANET_AND_DELTA, TITANIUM_BOLTS, TitaniumBolt

if TYPE_CHECKING:
    from ..pypine import Pine

__all__ = [
    "BOLT_BY_PLANET_AND_DELTA",
    "TITANIUM_BOLTS",
    "TitaniumBolt",
    "TitaniumBoltInventory",
]

_PICKUP_ADDR = address_maps.TITANIUM_BOLT_BASE + 0x00
_TOTAL_ADDR = address_maps.TITANIUM_BOLT_BASE + 0x05


class TitaniumBoltSlot:
    """Pine-backed accessor for the 5-byte cumulative bolt-pickup bitmask."""

    address = address_maps.Address("TITANIUM_BOLT_BASE")

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


class TitaniumBoltTotalSlot:
    """Pine-backed accessor for the single-byte cumulative bolt count."""

    address = address_maps.Address("TITANIUM_BOLT_BASE", 5)

    def __get__(self, instance, owner) -> int | None:
        if instance is None:
            return None
        return instance.pine.read_int8(self.address)

    def __set__(self, instance, value: int) -> None:
        if instance is None:
            return
        instance.pine.write_int8(self.address, value)

    def __delete__(self, instance) -> None:
        if instance is None:
            return
        instance.pine.write_int8(self.address, 0)


class TitaniumBoltInventory:
    """Pine-backed live accessor + completion tracking for titanium bolts,
    replacing TitaniumBoltState. Global fixed address — no per-planet base."""

    pickup = TitaniumBoltSlot()
    total = TitaniumBoltTotalSlot()

    def __init__(self, pine: Pine) -> None:
        self.pine = pine
        self.completed: set[str] = set()
        self._last: int = 0
        self._synced_mask: int = 0

    def get(self, name: str) -> bool:
        return bool(self.pickup & TITANIUM_BOLTS[name].delta)

    def set(self, name: str, value: bool) -> None:
        bolt = TITANIUM_BOLTS[name]
        current = self.pickup
        self.pickup = (current | bolt.delta) if value else (current & ~bolt.delta)

    def delete(self, name: str) -> None:
        self.set(name, False)

    def check(self, current: int | None = None) -> list[str]:
        """Read the cumulative bitmask and return newly completed AP location names for this call."""
        current = self.pickup if current is None else current
        delta = current & ~self._last
        self._last = current

        observation = LocationObservation(bolt_bits=delta)
        newly = [
            name for name in TITANIUM_BOLTS if name not in self.completed and ALL_LOCATIONS[name].completed(observation)
        ]
        self.completed.update(newly)
        return newly

    def sync(self) -> None:
        """Baseline read, applying any AP-synced bits, without reporting anything as newly completed."""
        current = self.pickup
        new_val = current | self._synced_mask
        if new_val != current:
            self.pickup = new_val
        self._last = new_val

    def sync_from_ap(self, checked_location_names: set[str]) -> None:
        mask = 0
        for name, bolt in TITANIUM_BOLTS.items():
            if name in checked_location_names:
                mask |= bolt.delta
                self.completed.add(name)
        self._synced_mask = mask

    def __repr__(self) -> str:
        return f"TitaniumBoltInventory(completed={len(self.completed)}/{len(TITANIUM_BOLTS)})"
