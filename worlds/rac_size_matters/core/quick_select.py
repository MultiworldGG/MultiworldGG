from __future__ import annotations

import time
from collections.abc import Callable
from typing import TYPE_CHECKING

from .states.base_state import BaseState
from .structs.game import QuickSelectStruct

if TYPE_CHECKING:
    from ..pypine import Pine

_ZERO_BYTES = bytes(4 * len(QuickSelectStruct.SLOT_ORDER))

_WRITE_COOLDOWN_S: float = 0.3


class QuickSelectState(BaseState):

    def __init__(self, pine: Pine) -> None:
        super().__init__()
        self.pine = pine
        self._snapshot: dict[str, int] = dict.fromkeys(QuickSelectStruct.SLOT_ORDER, 0)
        self._polling = False
        self._write_time: float = 0.0
        self.on_save: Callable[[dict[str, int]], None] = lambda _: None
        self.is_ap_owned: Callable[[int], bool] = lambda _weapon_id: True

    def load(self, data: dict[str, int]) -> None:
        """Load a saved quick-select snapshot (e.g. from AP data storage)."""
        for name in QuickSelectStruct.SLOT_ORDER:
            if name in data:
                self._snapshot[name] = int(data[name])

    def push_save(self) -> None:
        """Push the current snapshot to AP data storage. Called explicitly rather than on
        every poll-detected change, since that would echo back and re-trigger restores."""
        self.on_save(dict(self._snapshot))

    def freeze(self) -> None:
        """Stop updating the snapshot (planet transition or vendor open)."""
        self._polling = False

    def unfreeze(self) -> None:
        """Resume snapshot updates."""
        self._polling = True

    def check(self) -> None:
        """Pull-based: call every tick while not frozen — re-reads the wheel and updates
        the snapshot, unless still inside the cooldown window after our own write."""
        if not self._polling:
            return
        if time.monotonic() - self._write_time < _WRITE_COOLDOWN_S:
            return
        self.sync()
        if self._filter_unowned_slots():
            self.apply()

    def sync(self) -> None:
        raw = self.pine.read_bytes(QuickSelectStruct.BASE_ADDRESS, QuickSelectStruct.size())
        instance = QuickSelectStruct.from_bytes(raw)
        for name in QuickSelectStruct.SLOT_ORDER:
            self._snapshot[name] = getattr(instance, name)

    def _filter_unowned_slots(self) -> bool:
        """Zero any snapshot slot referencing a weapon/gadget id the player doesn't
        currently AP-own, since restore() would otherwise keep resurfacing it.
        Returns whether anything changed, so callers only write memory when needed."""
        changed = False
        for name in QuickSelectStruct.SLOT_ORDER:
            weapon_id = self._snapshot[name]
            if weapon_id != 0 and not self.is_ap_owned(weapon_id):
                self._snapshot[name] = 0
                changed = True
        return changed

    def zero(self) -> None:
        """Zero all slots in memory, then start polling. The in-memory snapshot is
        preserved so a previously saved loadout can be written back by restore()."""
        self._write_time = time.monotonic()
        self.pine.write_bytes(QuickSelectStruct.BASE_ADDRESS, _ZERO_BYTES)
        self._polling = True

    def restore(self) -> None:
        """Write the current snapshot to memory without checking polling state. Call
        this BEFORE unfreeze() so the next check() sees our values, not game defaults."""
        self._filter_unowned_slots()
        self._write_time = time.monotonic()
        instance = QuickSelectStruct()
        for name in QuickSelectStruct.SLOT_ORDER:
            setattr(instance, name, self._snapshot[name])
        self.pine.write_bytes(QuickSelectStruct.BASE_ADDRESS, bytes(instance))

    def apply(self) -> None:
        """Write the current snapshot back to memory, zeroing any empty slots."""
        if not self._polling:
            return
        self._write_time = time.monotonic()
        instance = QuickSelectStruct()
        for name in QuickSelectStruct.SLOT_ORDER:
            setattr(instance, name, self._snapshot[name])
        self.pine.write_bytes(QuickSelectStruct.BASE_ADDRESS, bytes(instance))
