from __future__ import annotations

import logging
from collections.abc import Callable
from dataclasses import dataclass
from enum import IntEnum
from typing import TYPE_CHECKING, NamedTuple

from ..constants import Rac5CutsceneLocations, Rac5Locations
from ..data.planets import INFOBOT_ITEM_TO_PLANET as INFOBOT_ITEM_TO_PLANET
from . import address_maps
from .address_maps import (
    CURRENT_PLANET_ADDRESS,
    MENU_ADDR_BY_PLANET_ID,
    NEW_PLANET_START_LOAD_ADDR,
    PLANET_LOAD_IDLE_VALUE,
    PLANET_STATE_OFFSET,
    PLANET_UNLOCK_ADDRESSES,
    WEAPON_ARRAY_BASE_BY_PLANET,
)
from .armour import ArmourPiece, ArmourStruct
from .controller import GlobalButtonState
from .display_text import multi_line_text_box_inventory, small_text_box_inventory
from .menu import MenuInventory, MenuStateValue
from .patches.starting_planet import ELIGIBLE
from .player import PlayerInventory, PlayerMovementState
from .states.base_state import BaseState
from .structs.game import (
    TRANSITION_GATE_ARRIVED,
    TRANSITION_GATE_IDLE,
    LoadingPlanetStruct,
    PlanetProgressStruct,
    TransitionGateStruct,
)
from .traps import activate_trap as _activate_trap
from .weapon_cycler import WeaponCyclerInventory
from .weapons import WeaponInventory

if TYPE_CHECKING:
    from ..pypine import Pine
    from .armour import ArmourInventory
    from .quick_select import QuickSelectState


@dataclass(frozen=True)
class Planet:
    name: str
    planet_id: int
    @property
    def menu_addr(self) -> int | None:
        return MENU_ADDR_BY_PLANET_ID.get(self.planet_id)


class Planets:
    POKITARU = Planet("Pokitaru", 0x01)
    RYLLUS = Planet("Ryllus", 0x02)
    KALIDON = Planet("Kalidon", 0x03)
    METALIS = Planet("Metalis", 0x04)
    DREAMTIME = Planet("Dreamtime", 0x05)
    CHALLAX = Planet("Challax", 0x07)
    DAYNI_MOON = Planet("Dayni Moon", 0x08)
    INSIDE_CLANK = Planet("Inside Clank", 0x09)
    QUODRONA = Planet("Quodrona", 0x0A)
    GIANT_CLANK_METALIS = Planet("Giant Clank (Metalis)", 0x0F)
    GIANT_CLANK_CHALLAX = Planet("Giant Clank (Challax)", 0x15)
    KALIDON_RACE = Planet("Kalidon Race Track", 0x16)
    OUTPOST_OMEGA_2 = Planet("Outpost Omega 2", 0x17)


BY_ID: dict[int, Planet] = {p.planet_id: p for p in vars(Planets).values() if isinstance(p, Planet)}


@dataclass(frozen=True)
class PlanetUnlock:
    unlock_addr: int
    state_addr: int
    default_state: int = 0


_DEFAULT_STATES: dict[str, int] = {
    "DREAMTIME": 3,
    "OUTPOST_OMEGA": 3,
}

PLANET_UNLOCKS: dict[str, PlanetUnlock] = {
    name: PlanetUnlock(
        unlock_addr=addr,
        state_addr=addr + address_maps.PLANET_STATE_OFFSET,
        default_state=_DEFAULT_STATES.get(name, 0),
    )
    for name, addr in PLANET_UNLOCK_ADDRESSES.items()
}


INFOBOT_UNLOCK_VALUE = 3


PLANET_STATE_ADDRESSES: dict[str, int] = {
    "pokitaru": PLANET_UNLOCK_ADDRESSES["POKITARU"],
    "ryllus": PLANET_UNLOCK_ADDRESSES["RYLLUS"],
    "kalidon": PLANET_UNLOCK_ADDRESSES["KALIDON"],
    "metalis": PLANET_UNLOCK_ADDRESSES["METALIS"],
    "outpost_omega": PLANET_UNLOCK_ADDRESSES["OUTPOST_OMEGA"],
    "outpost_omega_oo2": 0x1F4C677,
    "challax": PLANET_UNLOCK_ADDRESSES["CHALLAX"],
    "dayni_moon": PLANET_UNLOCK_ADDRESSES["DAYNI_MOON"],
    "inside_clank": PLANET_UNLOCK_ADDRESSES["INSIDE_CLANK"],
    "quodrona": PLANET_UNLOCK_ADDRESSES["QUODRONA"],
}

AUTO_UNLOCK_ADDRESSES: list[int] = [
    0x1F4C665,
]


logger = logging.getLogger("CommonClient")

_METALIS_ID: int = 0x04
_CHALLAX_ID: int = 0x07

_GIANT_CLANK_METALIS_ID: int = 0x0F
_GIANT_CLANK_CHALLAX_ID: int = 0x15


class GiantClankConfig(NamedTuple):
    origin_id: int
    armour_set: str
    piece: ArmourPiece
    pickup_locations: tuple[str, ...]
    redirect_to: int | None = None
    escape_location: str | None = None


GIANT_CLANK_CONFIGS: dict[int, GiantClankConfig] = {
    _GIANT_CLANK_METALIS_ID: GiantClankConfig(
        origin_id=_METALIS_ID,
        armour_set="electroshock",
        piece=ArmourPiece.GLOVES,
        pickup_locations=(Rac5Locations.METALIS_GLOVES,),
        redirect_to=_METALIS_ID,
        escape_location=Rac5CutsceneLocations.METALIS_ESCAPE,
    ),
    _GIANT_CLANK_CHALLAX_ID: GiantClankConfig(
        origin_id=_CHALLAX_ID,
        armour_set="electroshock",
        piece=ArmourPiece.CHESTPLATE,
        pickup_locations=(Rac5Locations.CHALLAX_CHESTPLATE, Rac5CutsceneLocations.CHALLAX_CLANK),
    ),
}


class PlanetInventory:
    """Single home for planet-specific runtime logic. Owns every planet-dependent
    Inventory and rebinds them via set_planet(); never pokes memory directly itself."""

    def __init__(
        self,
        pine: Pine,
        armour: ArmourInventory,
        quick_select: QuickSelectState,
    ) -> None:
        self.pine = pine
        self.armour = armour
        self.quick_select = quick_select

        self.player = PlayerInventory(pine)
        self.menu = MenuInventory(pine)
        self.weapons = WeaponInventory(pine)
        self.weapon_cycler = WeaponCyclerInventory(pine)
        self.small_text = small_text_box_inventory(pine)
        self.multi_line_text = multi_line_text_box_inventory(pine)

        self.planet_id: int | None = None
        self.is_ready: bool = False
        self._pending_planet_id: int | None = None
        self._prev_gate: int = TRANSITION_GATE_IDLE

        self.starting_planet_id: int | None = None
        self._quick_select_primed: bool = False

        self.giant_clank_allowed: bool = True
        self.giant_clank_active: bool = False
        self._giant_clank_config: GiantClankConfig | None = None
        self._giant_clank_had_piece: bool = False
        self._giant_clank_escape_sent: bool = False

        self.equipped_armour: dict[str, int] = dict.fromkeys(ArmourStruct.SLOT_FIELDS, 0)
        self._was_picking_up: bool = False
        self._equipped_pickup_baseline: dict[str, int] | None = None

        self.on_death: Callable[[], None] = lambda: None
        self.on_respawn: Callable[[], None] = lambda: None
        self.on_equipped_armour_saved: Callable[[dict[str, int]], None] = lambda _: None
        self.on_pause_close: Callable[[], None] = lambda: None

        self._prev_dead: bool = False
        self._prev_menu: MenuStateValue | None = None
        self._cached_movement: PlayerMovementState | None = None

    @property
    def weapons_available(self) -> bool:
        """Only access weapons on a ready, current level with a weapon array.

        Read the live id too: client restore can run before check_transition().
        Skyboard and Clank sub-levels must not use the previous planet's array.
        """
        return (
            self.is_ready
            and not self.giant_clank_active
            and WEAPON_ARRAY_BASE_BY_PLANET.get(self.planet_id) is not None
            and self.pine.read_int8(address_maps.CURRENT_PLANET_ADDRESS) == self.planet_id
        )

    def set_starting_planet(self, planet_id: int | None) -> None:
        """Configure the frontend New Game patch; never redirect loaded saves."""
        if planet_id is not None and planet_id not in ELIGIBLE:
            raise ValueError(f"Invalid starting planet: {planet_id!r}")
        self.starting_planet_id = planet_id

    def set_planet(self, planet_id: int) -> None:
        """Rebind every planet-dependent Inventory to the newly loaded planet, including
        unbinding for an unrecognized planet_id — otherwise it'd keep stale addresses."""
        self.planet_id = planet_id
        self.player.set_base(planet_id)
        self.menu.set_base(planet_id)
        self.small_text.set_base(planet_id)
        self.multi_line_text.set_base(planet_id)
        self.weapons.set_base(WEAPON_ARRAY_BASE_BY_PLANET.get(planet_id))
        self.weapon_cycler.set_base(planet_id)

    def check_transition(self) -> bool:
        """Pull-based transition detector — call every tick. Primary signal is the
        transition gate; falls back to a raw CURRENT_PLANET_ADDRESS comparison for a
        planet swap that never touches the gate. Returns True once, when ready."""
        gate = self.pine.read_int32(TransitionGateStruct.BASE_ADDRESS)
        if gate != self._prev_gate:
            prev = self._prev_gate
            self._prev_gate = gate
            left_idle = prev == TRANSITION_GATE_IDLE and gate != TRANSITION_GATE_IDLE
            back_to_idle = prev != TRANSITION_GATE_IDLE and gate == TRANSITION_GATE_IDLE

            if left_idle:
                self.is_ready = False
                self.quick_select.freeze()

            if gate == TRANSITION_GATE_ARRIVED:
                planet_id = self.pine.read_int8(LoadingPlanetStruct.BASE_ADDRESS)
                if planet_id != 0:
                    self._pending_planet_id = planet_id

            if back_to_idle and self._pending_planet_id:
                self._ready_on_planet(self._pending_planet_id)
                self._pending_planet_id = None
                return True

            return False

        current_id = self.pine.read_int8(address_maps.CURRENT_PLANET_ADDRESS)
        if current_id != 0 and current_id != self.planet_id and self._pending_planet_id is None:
            self._ready_on_planet(current_id)
            return True

        return False

    def _ready_on_planet(self, planet_id: int) -> None:
        config = GIANT_CLANK_CONFIGS.get(planet_id)
        if config is not None and not self.giant_clank_allowed:
            self.pine.write_int32(address_maps.NEW_PLANET_START_LOAD_ADDR, config.origin_id)
            return

        self.set_planet(planet_id)
        self.is_ready = True
        if not self._quick_select_primed:
            self._quick_select_primed = True
            self.quick_select.zero()
        else:
            self.quick_select.unfreeze()
        self.quick_select.restore()

        if config is not None:
            self._enter_giant_clank(config)
        elif self.giant_clank_active:
            self._exit_giant_clank()

    def _enter_giant_clank(self, config: GiantClankConfig) -> None:
        """Strip armour on entry so nothing AP-granted shows during the
        sequence, and so the completion pickup (checked live via
        check_giant_clank()) is a clean 0->1 transition."""
        self.giant_clank_active = True
        self._giant_clank_config = config
        self._giant_clank_had_piece = False
        self._giant_clank_escape_sent = False
        self.armour.clear_unlocked()

    def _exit_giant_clank(self) -> None:
        """Restore true AP armour ownership once back on a regular planet."""
        self.giant_clank_active = False
        self._giant_clank_config = None
        self.armour.apply_full()

    def check_giant_clank(self) -> list[str]:
        """Poll-based: call every tick regardless of is_ready/transition state so a
        redirect lands ASAP. No-ops unless giant_clank_active. Returns
        pickup_locations on a genuine armour pickup, and escape_location once
        when redirecting the game's own scripted exit back to origin_id."""
        config = self._giant_clank_config
        if not self.giant_clank_active or config is None:
            return []

        to_send: list[str] = []

        unlocked = self.armour.read()
        has_piece = bool(getattr(unlocked, config.armour_set) & config.piece)
        if has_piece and not self._giant_clank_had_piece:
            to_send.extend(config.pickup_locations)
        self._giant_clank_had_piece = has_piece

        if config.redirect_to is not None:
            load_value = self.pine.read_int32(address_maps.NEW_PLANET_START_LOAD_ADDR)
            if load_value != address_maps.PLANET_LOAD_IDLE_VALUE:
                self.pine.write_int32(address_maps.NEW_PLANET_START_LOAD_ADDR, config.redirect_to)
                if not self._giant_clank_escape_sent:
                    self._giant_clank_escape_sent = True
                    if config.escape_location:
                        to_send.append(config.escape_location)

        return to_send

    def show_text(self, text: bytes | str, *, multi_line: bool = False) -> None:
        if not self.is_ready:
            return
        box = self.multi_line_text if multi_line else self.small_text
        box.set(text)

    def check_death(self) -> bool:
        """Also refreshes self._cached_movement, the single PlayerInventory read this
        and check_collected_armour() both need this tick, avoiding a second read."""
        if not self.is_ready:
            return False
        movement = self.player.movement_state
        self._cached_movement = movement
        is_dead = movement is not None and PlayerMovementState.is_dead(int(movement))
        newly_dead = is_dead and not self._prev_dead
        newly_revived = self._prev_dead and not is_dead
        self._prev_dead = is_dead
        if newly_dead:
            self.on_death()
        elif newly_revived:
            self.on_respawn()
        return newly_dead

    def check_controller(self) -> None:
        if not self.is_ready or self.planet_id is None:
            return
        buttons = GlobalButtonState.read(self.pine, self.planet_id)
        if buttons is not None and buttons.opens_planet_menu:
            self.menu.set(MenuStateValue.PLANET_MENU)

    def activate_trap(self, trap_name: str) -> None:
        if not self.is_ready:
            return
        _activate_trap(self.pine, trap_name)

    def check_collected_armour(self) -> None:
        """Snapshot equipped slots at pickup-animation start and restore them at
        pickup-animation end, since the game can auto-equip whatever was just
        picked up and this must not silently change the player's loadout.
        Detecting *which* piece was collected no longer happens here -- that's
        ArmourInventory.check(), called every tick like TitaniumBoltInventory.check()
        (see its docstring for why the old pickup-animation-window + clear_unlocked()
        dance is no longer needed)."""
        if not self.is_ready:
            return
        is_picking_up = self._cached_movement == PlayerMovementState.Pickup
        if is_picking_up and not self._was_picking_up:
            equipped = self.armour.read()
            self._equipped_pickup_baseline = {
                name: int(getattr(equipped, name) or 0) for name in ArmourStruct.SLOT_FIELDS
            }
        elif not is_picking_up and self._was_picking_up:
            if self._equipped_pickup_baseline is not None:
                self.armour.sync_equipped(self._equipped_pickup_baseline)
                self._equipped_pickup_baseline = None
        self._was_picking_up = is_picking_up

    def check_equipped_armour(self) -> bool:
        """Pull-based: call whenever you want to check for a pause-menu-close
        transition. Only then does it snapshot + save EquipedArmour."""
        if not self.is_ready:
            return False
        current = self.menu.get()
        left_pause_menu = self._prev_menu == MenuStateValue.PAUSE_MENU and current != MenuStateValue.PAUSE_MENU
        self._prev_menu = current
        if left_pause_menu:
            equipped = self.armour.read()
            for name in ArmourStruct.SLOT_FIELDS:
                self.equipped_armour[name] = int(getattr(equipped, name) or 0)
            self.on_equipped_armour_saved(dict(self.equipped_armour))
            self.on_pause_close()
        return left_pause_menu

    def check_weapons(self) -> dict[str, list]:
        if not self.is_ready:
            return {"weapons": [], "gadgets": [], "mods": [], "levels": []}
        return self.weapons.check()

    def check_weapon_cycler(
        self,
        *,
        is_ap_owned: Callable[[int], bool],
        vendor_active: bool,
        fallback_weapon_id: Callable[[], int | None],
    ) -> None:
        if not self.is_ready:
            return
        self.weapon_cycler.check(
            is_ap_owned=is_ap_owned,
            vendor_active=vendor_active,
            fallback_weapon_id=fallback_weapon_id,
        )

    def __repr__(self) -> str:
        return f"PlanetInventory(planet_id={self.planet_id})"


PLANET_UNLOCK_BASE: int = PlanetProgressStruct.BASE_ADDRESS


class PlanetLockValue(IntEnum):
    LOCKED = 0x00
    UNLOCKED = 0x03


PLANET_UNLOCK_ORDER: list[str] = list(PlanetProgressStruct.PLANET_NAME_ORDER)

_AUTO_UNLOCK_NAMES: frozenset[str] = frozenset(
    {
        "DREAMTIME",
    }
)

_NATURAL_UNLOCK_NAMES: frozenset[str] = frozenset({"INSIDE_CLANK"})

_VENDOR_PLANET_GATE: dict[str, str] = {
    "DREAMTIME": "OUTPOST_OMEGA",
    "INSIDE_CLANK": "DAYNI_MOON",
}

_COUNT = len(PLANET_UNLOCK_ORDER)


class PlanetUnlockState(BaseState):
    def __init__(self, pine: Pine) -> None:
        super().__init__()
        self.pine = pine
        self.unlocked: dict[str, bool] = dict.fromkeys(PLANET_UNLOCK_ORDER, False)
        self._desired: dict[str, bool] = {p: p in _AUTO_UNLOCK_NAMES for p in PLANET_UNLOCK_ORDER}
        self._desired["RYLLUS"] = True
        self._enforce_active: bool = True
        self._ryllus_released: bool = False
        self._infobot_planets: set[str] = set()
        self._random_start: bool = False
        self.split_infobots: bool = False

    def _read_struct(self) -> PlanetProgressStruct:
        raw = self.pine.read_bytes(PlanetProgressStruct.BASE_ADDRESS, PlanetProgressStruct.size())
        return PlanetProgressStruct.from_bytes(raw)

    def check(self) -> None:
        """Pull-based: re-check + enforce planet unlock state, firing
        on_planet_unlocked/on_planet_locked for whatever changed."""
        instance = self._read_struct()
        prev = dict(self.unlocked)
        for field, name in zip(PlanetProgressStruct.PLANET_ORDER, PLANET_UNLOCK_ORDER, strict=False):
            self.unlocked[name] = getattr(instance, field) == PlanetLockValue.UNLOCKED

        self._enforce_desired()

        for name in PLANET_UNLOCK_ORDER:
            if self.unlocked[name] and not prev[name]:
                self.on_planet_unlocked(name)
            elif not self.unlocked[name] and prev[name]:
                self.on_planet_locked(name)

    def sync(self) -> None:
        instance = self._read_struct()
        for field, name in zip(PlanetProgressStruct.PLANET_ORDER, PLANET_UNLOCK_ORDER, strict=False):
            self.unlocked[name] = getattr(instance, field) == PlanetLockValue.UNLOCKED
        self._enforce_desired()

    def _enforce_desired(self) -> None:
        """Unconditionally re-assert every non-natural planet's lock state every call,
        since _write_desired()'s second state_addr byte can silently drift out of sync."""
        if not self._enforce_active:
            return
        names = [n for n in PLANET_UNLOCK_ORDER if n not in _NATURAL_UNLOCK_NAMES]
        self._write_desired(names)
        for name in names:
            self.unlocked[name] = self._desired[name]

    def _write_desired(self, names: list[str]) -> None:
        for field, name in zip(PlanetProgressStruct.PLANET_ORDER, PLANET_UNLOCK_ORDER, strict=False):
            if name not in names:
                continue
            unlock_val = PlanetLockValue.UNLOCKED if self._desired[name] else PlanetLockValue.LOCKED
            self.pine.write_int8(PlanetProgressStruct.address_of(field), int(unlock_val))
            pu = PLANET_UNLOCKS.get(name)
            if pu is not None:
                state_val = max(int(unlock_val), pu.default_state)
                state_addr = PLANET_UNLOCK_ADDRESSES[name] + address_maps.PLANET_STATE_OFFSET
                self.pine.write_int8(state_addr, state_val)

    def set_random_start(self, enabled: bool) -> None:
        self._random_start = enabled

    def set_unlocked_planets(self, planets: set[str]) -> None:
        self._infobot_planets = set(planets)
        for name in PLANET_UNLOCK_ORDER:
            self._desired[name] = name in planets or name in _AUTO_UNLOCK_NAMES
        if not self.split_infobots and not self._random_start and not self._ryllus_released:
            self._desired["RYLLUS"] = True

    def on_ryllus_cutscene_ended(self) -> None:
        if self.split_infobots or self._random_start or self._ryllus_released:
            return
        self._ryllus_released = True
        self._desired["RYLLUS"] = "RYLLUS" in self._infobot_planets

    def reset_session(self) -> None:
        self._ryllus_released = False
        if not self.split_infobots and not self._random_start:
            self._desired["RYLLUS"] = True

    def unlock(self, planet: str) -> None:
        self._desired[planet] = True

    def lock(self, planet: str) -> None:
        if planet not in _AUTO_UNLOCK_NAMES:
            self._desired[planet] = False

    def is_unlocked(self, planet: str) -> bool:
        return self._desired.get(planet, False)

    def is_vendor_accessible(self, planet: str) -> bool:
        gate = _VENDOR_PLANET_GATE.get(planet, planet)
        return self._desired.get(gate, False)

    def on_planet_unlocked(self, _planet: str) -> None:
        del _planet

    def on_planet_locked(self, _planet: str) -> None:
        del _planet

    def __repr__(self) -> str:
        count = sum(self.unlocked.values())
        return f"PlanetUnlockState(unlocked={count}/{_COUNT})"
