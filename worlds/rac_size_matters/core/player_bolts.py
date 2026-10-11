from __future__ import annotations

from typing import TYPE_CHECKING

from . import address_maps
from .address_maps import PLAYER_BOLT_COUNT

if TYPE_CHECKING:
    from ..pypine import Pine

MAX_PLAYER_BOLTS = 20_000_000


class PlayerBoltInventory:
    """Pine-backed accessor + gain-multiplier tracking for the player's
    spendable bolt count (global fixed address, no per-planet base)."""

    def __init__(self, pine: Pine) -> None:
        self.pine = pine
        self.multiplier: int = 1
        self._prev: int | None = None

    def get(self) -> int:
        return self.pine.read_int32(address_maps.PLAYER_BOLT_COUNT)

    def set(self, value: int) -> None:
        self.pine.write_int32(address_maps.PLAYER_BOLT_COUNT, min(value, MAX_PLAYER_BOLTS))

    def rebaseline(self, value: int | None = None) -> None:
        """Re-sync the baseline apply_boost() diffs against, without boosting anything.
        Callers writing PLAYER_BOLT_COUNT directly must call this right after."""
        self._prev = value if value is not None else self.get()

    def apply_boost(self) -> None:
        """Inflate ordinary bolt gain (crates, enemies, etc.) by multiplier,
        every tick, by diffing against the last raw reading."""
        current = self.get()
        if self._prev is None:
            self._prev = current
            return
        diff = current - self._prev
        if diff <= 0:
            self._prev = current
            return
        if self.multiplier > 1:
            boosted = min(self._prev + diff * self.multiplier, MAX_PLAYER_BOLTS)
            self.set(boosted)
            self._prev = boosted
        else:
            self._prev = current

    def __repr__(self) -> str:
        return f"PlayerBoltInventory(prev={self._prev}, multiplier={self.multiplier})"
