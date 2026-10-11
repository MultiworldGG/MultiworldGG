from __future__ import annotations

from collections.abc import Callable
from enum import IntEnum
from typing import TYPE_CHECKING

from .address_maps import WEAPON_CYCLER_ADDRS_BY_PLANET

if TYPE_CHECKING:
    from ..pypine import Pine


class WeaponCycleState(IntEnum):
    IDLE   = 0x00
    PICKUP = 0x0C

EMPTY_WEAPON_ID = 1


class WeaponCyclerField:
    """Pine-backed accessor for one 4-byte weapon-cycler field. `attr` names the
    instance attribute holding its address (None -> every read/write is a no-op)."""

    def __init__(self, attr: str) -> None:
        self.attr = attr

    def __get__(self, instance, owner) -> int | None:
        if instance is None:
            return None
        address = getattr(instance, self.attr)
        if address is None:
            return None
        return instance.pine.read_int32(address)

    def __set__(self, instance, value: int) -> None:
        address = getattr(instance, self.attr)
        if address is not None:
            instance.pine.write_int32(address, value)


class WeaponCyclerInventory:
    """Pine-backed live accessor + write gate for the per-planet weapon cycler. With no
    "we're in a cutscene" signal to gate writes on, a cutscene-forced weapon is let through
    then immediately clamped back to EMPTY_WEAPON_ID if AP hasn't granted it (see check())."""

    applied_weapon = WeaponCyclerField("apply_addr")
    cycle_state    = WeaponCyclerField("state_addr")
    current_weapon = WeaponCyclerField("current_addr")
    stored_weapon  = WeaponCyclerField("stored_addr")

    def __init__(self, pine: Pine) -> None:
        self.pine = pine
        self.apply_addr:   int | None = None
        self.state_addr:   int | None = None
        self.current_addr: int | None = None
        self.stored_addr:  int | None = None
        self._prev_vendor_active: bool = False

    def set_base(self, planet_id: int) -> None:
        addrs = WEAPON_CYCLER_ADDRS_BY_PLANET.get(planet_id)
        if addrs is None:
            self.apply_addr = self.state_addr = self.current_addr = self.stored_addr = None
        else:
            self.apply_addr, self.state_addr, self.current_addr, self.stored_addr = addrs

    def initialize(self, fallback_weapon_id: Callable[[], int | None]) -> None:
        """Force cycle_state to 1 and set current/stored weapon to what AP already
        owns, called once on the first planet-ready since the wheel otherwise starts
        in a state that blocks weapon application."""
        if not self.is_ready:
            return
        self.cycle_state = 1
        weapon_id = fallback_weapon_id() or EMPTY_WEAPON_ID
        self.applied_weapon = weapon_id
        self.stored_weapon  = weapon_id

    @property
    def is_ready(self) -> bool:
        return self.apply_addr is not None

    @property
    def is_picking_up(self) -> bool:
        state = self.cycle_state
        return state is not None and state == WeaponCycleState.PICKUP

    def can_write(self, *, vendor_active: bool) -> bool:
        """Whether it's currently safe to write applied/current/stored weapon — false
        during a pickup animation or while a vendor menu owns this same memory."""
        return self.is_ready and not self.is_picking_up and not vendor_active

    def apply(self, weapon_id: int, *, vendor_active: bool) -> bool:
        """Hand `weapon_id` to the player via the apply-weapon trigger address.
        No-ops (returns False) during a pickup animation or an open vendor menu."""
        if not self.can_write(vendor_active=vendor_active):
            return False
        self.applied_weapon = weapon_id
        return True

    def check(
        self, *, is_ap_owned: Callable[[int], bool], vendor_active: bool,
        fallback_weapon_id: Callable[[], int | None],
    ) -> None:
        """Pull-based: call every tick. Clamps current/stored weapon back to
        EMPTY_WEAPON_ID if the game itself forced an unowned one on (e.g. a cutscene).
        EMPTY_WEAPON_ID is also what the always-available wrench reads as, so only a
        raw 0 (never set) gets filled from fallback_weapon_id() -- the wrench itself
        must never be treated as "empty," which used to yank the wheel back to the
        player's lowest-id weapon the instant they pulled it out."""
        just_closed_vendor = self._prev_vendor_active and not vendor_active
        self._prev_vendor_active = vendor_active

        if not self.is_ready or self.is_picking_up or vendor_active or just_closed_vendor:
            return

        current = self.current_weapon
        if current is not None and current not in (0, EMPTY_WEAPON_ID) and not is_ap_owned(current):
            fallback = fallback_weapon_id()
            self.applied_weapon = fallback if fallback else EMPTY_WEAPON_ID
            current = self.applied_weapon
        elif current == 0:
            fallback = fallback_weapon_id()
            self.applied_weapon = fallback if fallback else EMPTY_WEAPON_ID

        stored = self.stored_weapon
        if stored is not None and stored not in (0, EMPTY_WEAPON_ID) and not is_ap_owned(stored):
            self.stored_weapon = EMPTY_WEAPON_ID

    def __repr__(self) -> str:
        return (
            f"WeaponCyclerInventory(current={self.current_weapon!r}, "
            f"stored={self.stored_weapon!r}, state={self.cycle_state!r})"
        )
