from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TitaniumBolt:
    planet_id: int | tuple[int, ...]
    bit: int
    region: str

    @property
    def delta(self) -> int:
        return 1 << self.bit

    @property
    def planet_ids(self) -> tuple[int, ...]:
        return self.planet_id if isinstance(self.planet_id, tuple) else (self.planet_id,)


from ...locations.model import FlatLocationView, LocationView
from ...locations.shared import LOCATIONS

TITANIUM_BOLTS = LocationView(
    LOCATIONS,
    lambda location: location.completed.source == "bolt_bits",
    value=lambda location: TitaniumBolt(
        location.native_planets, location.completed.mask.bit_length() - 1, location.planet
    ),
)
BOLT_BY_PLANET_AND_DELTA = FlatLocationView(
    LOCATIONS,
    lambda location: location.completed.source == "bolt_bits",
    key=lambda location: ((planet, location.completed.mask) for planet in location.native_planets),
    value=lambda location: location.name,
)
