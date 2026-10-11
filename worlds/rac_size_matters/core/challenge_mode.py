from __future__ import annotations

from typing import TYPE_CHECKING

from .structs.game import ChallengeModeStruct

if TYPE_CHECKING:
    from ..pypine import Pine


class ChallengeModeSlot:
    """Pine-backed accessor for ChallengeModeStruct's tier byte."""

    def __init__(self, field: str) -> None:
        self.field = field

    @property
    def address(self) -> int:
        # The game region is detected after this descriptor is constructed.
        return ChallengeModeStruct.address_of(self.field)

    def __get__(self, instance, owner) -> int | None:
        if instance is None:
            return None
        return instance.pine.read_int8(self.address)

    def __set__(self, instance, value: int) -> None:
        if instance is None:
            return
        instance.pine.write_int8(self.address, value)


class ChallengeModeState:
    """Pine-backed accessor for the game's own Challenge Mode (New Game
    Plus) tier byte — mirrors options.py's ChallengeMode option value."""

    tier = ChallengeModeSlot("tier")

    def __init__(self, pine: Pine) -> None:
        self.pine = pine
        self._tier: int = 0

    def set_by_option(self, value: int) -> None:
        self._tier = value
        self.tier = value

    def setup(self) -> None:
        """Re-write the current tier on every planet load, in case this byte
        gets reset on a planet transition; harmless if it doesn't."""
        self.tier = self._tier

    def __repr__(self) -> str:
        return f"ChallengeModeState(tier={self._tier})"
