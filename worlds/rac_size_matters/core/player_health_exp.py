from __future__ import annotations

from typing import TYPE_CHECKING

from . import address_maps
from .address_maps import PLAYER_HEALTH_EXP

if TYPE_CHECKING:
    from ..pypine import Pine

_MIN_NANOTECH_LEVEL = 1
_MAX_NANOTECH_LEVEL = 75


def _level_from_max_health(max_health: float) -> int | None:
    """max_health read as the Nanotech level directly, or None if the rounded
    reading falls outside the valid 1-75 range (unbound/garbage read)."""
    level = round(max_health)
    if _MIN_NANOTECH_LEVEL <= level <= _MAX_NANOTECH_LEVEL:
        return level
    return None


class PlayerHealthExpInventory:
    """Pine-backed accessor + gain-multiplier tracking for the player's Nanotech
    EXP counter. Nanotech Level checks are driven by PlayerInventory.max_health
    (see check_level()), not by this class's own EXP counter."""

    def __init__(self, pine: Pine) -> None:
        self.pine = pine
        self.multiplier: int = 1
        self._prev: int | None = None
        self._last_level: int = 5

    def get(self) -> int:
        return self.pine.read_int32(address_maps.PLAYER_HEALTH_EXP)

    def set(self, value: int) -> None:
        self.pine.write_int32(address_maps.PLAYER_HEALTH_EXP, value)

    def rebaseline(self, value: int | None = None) -> None:
        """Re-sync the baseline apply_boost() diffs against, without boosting anything.
        Callers writing PLAYER_HEALTH_EXP directly must call this right after."""
        self._prev = value if value is not None else self.get()

    def apply_boost(self) -> None:
        """Inflate ordinary Nanotech EXP gain by multiplier, every tick, by
        diffing against the last raw reading."""
        current = self.get()
        if self._prev is None:
            self._prev = current
            return
        diff = current - self._prev
        if diff <= 0:
            self._prev = current
            return
        if self.multiplier > 1:
            boosted = self._prev + diff * self.multiplier
            self.set(boosted)
            self._prev = boosted
        else:
            self._prev = current

    def check_level(self, max_health: float | None) -> list[str]:
        """Return the Nanotech Level location names newly reached since the last call, in
        ascending order so a multi-level jump doesn't skip any locations. No-op if
        max_health is None or its rounded value falls outside the valid 1-75 range."""
        if max_health is None:
            return []
        current_level = _level_from_max_health(max_health)
        if current_level is None:
            return []
        if current_level <= self._last_level:
            return []
        newly = [
            f"Nanotech Level: {lvl}"
            for lvl in range(self._last_level + 1, current_level + 1)
            if lvl >= 6
        ]
        self._last_level = current_level
        return newly

    def __repr__(self) -> str:
        return f"PlayerHealthExpInventory(prev={self._prev}, multiplier={self.multiplier})"
