from typing import TYPE_CHECKING

from ..constants.shrink_ray import (
    SHRINK_RAY_PUZZLE_BITS, SHRINK_RAY_LOCATION_PLANETS,
)
from . import address_maps
from .address_maps import SHRINK_RAY_GATE_ADDRESS
from .patches import shrink_ray as native

if TYPE_CHECKING:
    from ..pypine import Pine

SHRINK_RAY_SKIP_LOCATION_NAMES: list[str] = list(SHRINK_RAY_PUZZLE_BITS)


class ShrinkRaySkipInventory:
    """Track real completion flags and optionally release door interlocks."""

    def __init__(self, pine: "Pine") -> None:
        self.pine = pine
        self.completed: set[str] = set()
        self.plan = None
        self.planet = None

    def bind(self, planet, base, code):
        self.plan = None
        self.planet = planet
        self.plan = native.prepare(self.pine, code_start=base, code=code)

    def set_skip(self, planet, enabled):
        if self.plan is None or planet != self.planet:
            return
        if enabled:
            self.plan.install()
        elif not enabled and self.plan.installed:
            self.plan.restore()
        else:
            self.plan._validate(replacement=self.plan.installed)

    def _read(self) -> int:
        return self.pine.read_int16(address_maps.SHRINK_RAY_GATE_ADDRESS) or 0

    def check(self, planet: int) -> list[str]:
        raw = self._read()
        newly = [name for name, bit in SHRINK_RAY_PUZZLE_BITS.items()
                 if SHRINK_RAY_LOCATION_PLANETS[name] == planet
                 and name not in self.completed and raw & bit]
        self.completed.update(newly)
        return newly

    def sync_from_ap(self, checked_locations: set[str]) -> None:
        self.completed.update(name for name in checked_locations if name in SHRINK_RAY_PUZZLE_BITS)

    def __repr__(self) -> str:
        return f"ShrinkRaySkipInventory(completed={len(self.completed)}/{len(SHRINK_RAY_PUZZLE_BITS)})"
