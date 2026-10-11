from __future__ import annotations

import asyncio
import logging
import time
from typing import TYPE_CHECKING

from ..constants import Rac5Traps
from ..data.traps import TRAP_DURATIONS as TRAP_DURATIONS
from . import address_maps
from .no_clank import NoClank
from .address_maps import (
    BRIGHTNESS_ADDRESS,
    CHEATS,
    CURRENT_PLANET_ADDRESS,
    DREAMTIME_EFFECT,
    NEW_PLANET_START_LOAD_ADDR,
)

if TYPE_CHECKING:
    from ..pypine import Pine

_DIRECT_ADDRESSES: dict[str, str] = {
    Rac5Traps.TRAP_FEVERDREAMTIME: "DREAMTIME_EFFECT",
    Rac5Traps.TRAP_BRIGHTNESS: "BRIGHTNESS_ADDRESS",
}

MIRROR_LEVEL_CHEAT_BIT: int = 0x10
REVERSE_CONTROLS_CHEAT_BIT: int = 0x40
WEAPON_SWITCHING_CHEAT_BIT: int = 0x80

_CHEAT_BITS: dict[str, int] = {
    Rac5Traps.TRAP_MIRROR_LEVEL: MIRROR_LEVEL_CHEAT_BIT,
    Rac5Traps.TRAP_REVERSE_CONTROLS: REVERSE_CONTROLS_CHEAT_BIT,
    Rac5Traps.TRAP_WEAPON_SWITCHING: WEAPON_SWITCHING_CHEAT_BIT,
}


ALL_TRAPS: frozenset[str] = frozenset(TRAP_DURATIONS)

_trap_durations: dict[str, float] = dict(TRAP_DURATIONS)


def set_trap_durations(overrides: dict[str, float]) -> None:
    """Apply the TrapDuration option's per-trap seconds, called once on connect.
    Only overwrites known trap names — anything unrecognized keeps its default."""
    for trap_name, seconds in overrides.items():
        if trap_name in _trap_durations:
            _trap_durations[trap_name] = seconds


_active_deadlines: dict[str, float] = {}
_revert_handles: dict[str, asyncio.TimerHandle] = {}
# Expired traps whose game-memory effect hasn't been confirmed cleared yet. Retried every
# tick so a revert that lands during a PINE hiccup or level load can't leave a trap stuck.
_needs_clear: set[str] = set()
_no_clank_effects: dict[object, NoClank] = {}
_missing_clank_pack: set[object] = set()


def set_clank_pack_ownership(pine: Pine, *, enabled: bool, owned: bool) -> None:
    """Combine permanent AP ownership with the temporary trap in one controller."""
    if enabled and not owned:
        _missing_clank_pack.add(pine)
        _no_clank_effects.setdefault(pine, NoClank(pine))
    else:
        _missing_clank_pack.discard(pine)
    service_traps(pine)


def _expire(trap_name: str) -> None:
    _active_deadlines.pop(trap_name, None)
    handle = _revert_handles.pop(trap_name, None)
    if handle is not None:
        handle.cancel()
    if trap_name in _DIRECT_ADDRESSES or trap_name in _CHEAT_BITS:
        _needs_clear.add(trap_name)


def _write_effect(pine: Pine, trap_name: str, on: bool) -> None:
    """Write a memory-flag trap's effect, only touching memory when it differs."""
    field = _DIRECT_ADDRESSES.get(trap_name)
    if field is not None:
        address = getattr(address_maps, field)
        want = 1 if on else 0
        if pine.read_int8(address) != want:
            pine.write_int8(address, want)
        return
    bit = _CHEAT_BITS[trap_name]
    current = pine.read_int8(address_maps.CHEATS)
    wanted = current | bit if on else current & ~bit
    if wanted != current:
        pine.write_int8(address_maps.CHEATS, wanted)


def service_traps(pine: Pine) -> None:
    """Called every tick: expire overdue traps and re-assert every trap's effect, so
    effects the game resets (level loads, save loads) are re-applied while active and
    reverts that failed to write are retried until they stick. Write errors propagate."""
    # Deadlines come from loop.time(), which is time.monotonic() on the default loop.
    now = time.monotonic()
    for trap_name, deadline in list(_active_deadlines.items()):
        if deadline <= now:
            _expire(trap_name)

    effect = _no_clank_effects.get(pine)
    if effect is not None:
        active = pine in _missing_clank_pack or Rac5Traps.TRAP_NO_CLANK in _active_deadlines
        effect.update(active)
        if not active and not effect.backpacks:
            _no_clank_effects.pop(pine, None)

    for trap_name in _active_deadlines:
        if trap_name in _DIRECT_ADDRESSES or trap_name in _CHEAT_BITS:
            _write_effect(pine, trap_name, True)
    for trap_name in list(_needs_clear):
        _write_effect(pine, trap_name, False)
        _needs_clear.discard(trap_name)


def close_no_clank_trap(pine: Pine) -> None:
    """Restore backpack objects before closing the emulator connection."""
    _missing_clank_pack.discard(pine)
    if pine not in _no_clank_effects:
        return
    _expire(Rac5Traps.TRAP_NO_CLANK)
    service_traps(pine)


def activate_trap(pine: Pine, trap_name: str) -> None:
    """Activate a trap by name and schedule it to automatically revert. Re-activating
    a still-active trap extends (stacks) its deadline rather than reverting at the first."""
    if trap_name == Rac5Traps.TRAP_RESET_LEVEL:
        planet_id = pine.read_int8(address_maps.CURRENT_PLANET_ADDRESS)
        pine.write_int32(address_maps.NEW_PLANET_START_LOAD_ADDR, planet_id)
        return

    duration = _trap_durations.get(trap_name)
    if duration is None:
        return
    if trap_name != Rac5Traps.TRAP_NO_CLANK and trap_name not in _DIRECT_ADDRESSES and trap_name not in _CHEAT_BITS:
        return

    loop = asyncio.get_event_loop()
    now = loop.time()
    new_deadline = max(_active_deadlines.get(trap_name, now), now) + duration
    # Bookkeeping before any memory write, so a failed write is still enforced/reverted by ticks.
    _active_deadlines[trap_name] = new_deadline
    _needs_clear.discard(trap_name)

    existing_handle = _revert_handles.pop(trap_name, None)
    if existing_handle is not None:
        existing_handle.cancel()

    if trap_name == Rac5Traps.TRAP_NO_CLANK:
        _no_clank_effects.setdefault(pine, NoClank(pine))

    def _revert() -> None:
        _expire(trap_name)
        try:
            service_traps(pine)
        except Exception:
            # _needs_clear / the NoClank snapshot keep the revert pending; the next tick retries it.
            logging.getLogger("CommonClient").warning(f"[RAC] {trap_name} revert pending retry.", exc_info=True)

    _revert_handles[trap_name] = loop.call_at(new_deadline, _revert)
    service_traps(pine)


def reconcile_traps(pine: Pine) -> None:
    """Clear any trap effect in game memory with no bookkeeping in _active_deadlines,
    called on PINE (re)connect and on each save load — catches a bit left stuck by a client
    restart, a dropped revert, or a save written while a trap was active."""
    service_traps(pine)
    for trap_name, field in _DIRECT_ADDRESSES.items():
        address = getattr(address_maps, field)
        if trap_name in _active_deadlines:
            continue
        if pine.read_int8(address):
            pine.write_int8(address, 0)

    clear_mask = 0
    for trap_name, bit in _CHEAT_BITS.items():
        if trap_name not in _active_deadlines:
            clear_mask |= bit
    if clear_mask:
        current = pine.read_int8(address_maps.CHEATS)
        cleared = current & ~clear_mask
        if cleared != current:
            pine.write_int8(address_maps.CHEATS, cleared)
