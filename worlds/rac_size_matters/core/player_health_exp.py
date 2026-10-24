from bisect import bisect_right
from typing import TYPE_CHECKING

from . import address_maps

if TYPE_CHECKING:
    from ..pypine import Pine

NANOTECH_XP_THRESHOLDS = tuple(75 * index * (index + 23) for index in range(71))


class PlayerHealthExpInventory:
    """Pine-backed accessor + gain-multiplier tracking for the player's Nanotech
    EXP counter. Level checks use saved XP, never challenge-overridden HP."""

    def __init__(self, pine: "Pine") -> None:
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

    def check_level(self) -> list[str]:
        """Report earned levels using saved XP and the game's Nanotech table.

        Challenge HP can change before the active player pointer switches.
        It must never advance the persistent level high-water mark.
        """
        experience = self.get()
        if experience < 0:
            return []
        max_level = 75 if self.pine.read_int8(address_maps.CHALLENGE_MODE_BASE) else 50
        current_level = min(4 + bisect_right(NANOTECH_XP_THRESHOLDS, experience), max_level)
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
