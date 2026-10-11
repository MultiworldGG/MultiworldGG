from __future__ import annotations

import logging
import time
from collections.abc import Callable
from typing import TYPE_CHECKING

from .address_maps import CURRENT_PLANET_ADDRESS
from . import address_maps
from .armour import ArmourInventory
from .armour_spawn_gate import ArmourSpawnGate
from .challenge_mode import ChallengeModeState
from .challenges import ChallengeInventory, SkyboardInventory
from .ghost_ratchet import GhostRatchetInventory
from .inventory_sync import InventorySync
from .location_checks import LocationChecks
from .menu import MenuStateValue
from .missions import MissionInventory
from .native_runtime import NativeRuntime
from .options import ClientOption, ClientOptions
from .planets import PlanetInventory, PlanetUnlockState
from .player_bolts import PlayerBoltInventory
from .player_health_exp import PlayerHealthExpInventory
from .purchase_checks import PurchaseChecks
from .quick_select import QuickSelectState
from .shrink_ray import ShrinkRaySkipInventory
from .skill_points import SkillPointInventory
from .skins import SkinInventory
from .titanium_bolts import TitaniumBoltInventory
from .traps import reconcile_traps, service_traps
from .vendor import WEAPON_VENDOR_IDS, ModVendorMenu, VendorInventory, WeaponVendorMenu

if TYPE_CHECKING:
    from ..pypine import Pine

logger = logging.getLogger("CommonClient")


_PLANET_SETTLE_SECONDS: float = 1.0

_KALIDON_RACE_ID: int = 0x16


_CYCLER_ID_TO_WEAPON_NAME: dict[int, str] = {wid: name for name, wid in WEAPON_VENDOR_IDS.items()}


class Core:
    """Initial setup + per-tick orchestration for the whole client."""

    clank_enabled = ClientOption()
    clank_all_challenges = ClientOption()
    skyboard_enabled = ClientOption()
    shrink_ray_skips_enabled = ClientOption()
    shrink_ray_locations_enabled = ClientOption()
    skill_points_enabled = ClientOption()
    weapon_level_checks_enabled = ClientOption()
    nanotech_level_checks_enabled = ClientOption()
    progressive_challenge_mode_enabled = ClientOption()
    all_missions_enabled = ClientOption()
    all_cutscenes_enabled = ClientOption()

    def __init__(self, pine: Pine, log: Callable[[str], None] | None = None, *, patch_options=None) -> None:
        self.pine = pine
        self._log = log or logger.info

        self.armour = ArmourInventory(pine)
        self.armour_spawn_gate = ArmourSpawnGate(pine)
        self.quick_select = QuickSelectState(pine)
        self.quick_select.is_ap_owned = self._is_weapon_id_ap_owned
        self.planet_unlock = PlanetUnlockState(pine)

        self.clank = ChallengeInventory(pine)
        self.skyboard = SkyboardInventory(pine)
        self.bolts = TitaniumBoltInventory(pine)
        self.player_bolts = PlayerBoltInventory(pine)
        self.player_health_exp = PlayerHealthExpInventory(pine)
        self.skill_points = SkillPointInventory(pine)
        self.missions = MissionInventory(pine)
        self.skin = SkinInventory(pine)
        self.challenge_mode = ChallengeModeState(pine)
        self.shrink_ray = ShrinkRaySkipInventory(pine)
        self.ghost_ratchet = GhostRatchetInventory(pine)

        self.planet = PlanetInventory(pine, self.armour, self.quick_select)
        self.planet.on_death = self._handle_death
        self.planet.on_respawn = self._handle_respawn
        self.planet.on_equipped_armour_saved = lambda data: self.on_equipped_armour_saved(data)
        self.planet.on_pause_close = self.quick_select.push_save

        self.options = ClientOptions()

        self.vendor = VendorInventory(
            pine,
            self.planet,
            self.planet_unlock,
            lambda loc: self.send_location(loc),
            log=self._log,
            is_weapon_ap_owned=lambda name: self._ap_owned_weapons.get(name, False),
            is_gadget_ap_owned=lambda name: self._ap_owned_gadgets.get(name, False),
            is_weapon_level_checks_enabled=lambda: self.weapon_level_checks_enabled,
        )
        self.weapon_vendor = WeaponVendorMenu()
        self.mod_vendor = ModVendorMenu()
        self.native = NativeRuntime(
            pine,
            self.vendor,
            lambda loc: self.send_location(loc),
            self._log,
            self.shrink_ray,
            patch_options=patch_options,
        )
        self._prev_vendor: MenuStateValue | None = None

        self._ap_owned_weapons: dict[str, bool] = {}
        self._ap_owned_gadgets: dict[str, bool] = {}
        self._ap_inventory_ready: bool = False

        self.send_location: Callable[[str], None] = lambda _: None
        self.send_deathlink: Callable[[int], None] = lambda _: None
        self.death_amnesty: Callable[[], int] = lambda: 1
        self.death_link_enabled: Callable[[], bool] = lambda: False
        self.on_goal: Callable[[], None] = lambda: None
        self._death_count: int = 0

        self.on_planet_ready: Callable[[], None] = lambda: None
        self.on_initial_load: Callable[[], None] = lambda: None
        self._initial_load_done: bool = False

        self.on_vendor_open: Callable[[], None] = lambda: None
        self.on_vendor_close: Callable[[], None] = lambda: None

        self.on_equipped_armour_saved: Callable[[dict[str, int]], None] = lambda _: None

        self.on_bonus_weapon_pickup: Callable[[str], None] = lambda _: None
        self.on_scripted_gadget_pickup: Callable[[str], None] = lambda _: None
        self.on_weapon_level_up: Callable[[], None] = lambda: None

        self.at_main_menu: bool = True
        self._planet_settle_until: float = float("inf")
        self._main_menu_state_known: bool = False

    def select_game(self, game_id: str) -> bool:
        """Bind a detected region before ticking; retain AP state and callbacks.

        The caller holds the PINE lock. Old native objects keep their original
        serial guards, so cleanup cannot write US patches into an EU game.
        """
        if game_id not in address_maps.SUPPORTED_GAMES:
            raise ValueError(f"Unsupported Size Matters serial: {game_id!r}")
        if self.native.gate.game_id == game_id and address_maps.GAME_ID == game_id:
            return False
        previous_native = self.native
        previous_native.close()
        address_maps.select_game(game_id)

        # Recreate live planet caches, preserving the AP-owned weapon inventory
        # (also referenced by the vendor) and seed configuration.
        planet = self.planet
        retained = {name: getattr(planet, name) for name in (
            "weapons", "starting_planet_id", "giant_clank_allowed",
            "on_death", "on_respawn", "on_equipped_armour_saved", "on_pause_close",
        )}
        planet.__init__(self.pine, self.armour, self.quick_select)
        for name, value in retained.items():
            setattr(planet, name, value)
        planet.set_planet(0)
        planet.weapons._prev_experience.clear()
        planet.weapons._pinned_experience.clear()
        self.player_bolts._prev = None
        self.player_health_exp._prev = None
        self.quick_select.freeze()
        self.ghost_ratchet = GhostRatchetInventory(self.pine)
        self.shrink_ray.plan = None
        self.shrink_ray.planet = None
        self.armour_spawn_gate.last_applied_planet_id = None
        self.vendor.native_plan = None
        self.vendor._native_purchase_pending = False
        self.vendor._weapon_vendor_open = False
        self.vendor._mod_vendor_open = False
        self.weapon_vendor.deactivate()
        self.mod_vendor.deactivate()
        self._prev_vendor = None
        self.native = NativeRuntime(
            self.pine, self.vendor, previous_native.send_location, self._log,
            self.shrink_ray, patch_options=previous_native.patch_options,
        )
        for name in ("vendor_scouts", "enabled", "checked", "allowed_locations",
                     "progressive_challenge_mode_enabled", "ap_connected"):
            setattr(self.native, name, getattr(previous_native, name))
        self._ap_inventory_ready = False
        self.at_main_menu = True
        self._main_menu_state_known = False
        self._initial_load_done = False
        self._planet_settle_until = float("inf")
        return True

    @property
    def _ap_owned_weapons(self):
        return self.planet.weapons.ap_weapons

    @_ap_owned_weapons.setter
    def _ap_owned_weapons(self, values):
        self.planet.weapons.ap_weapons = values

    @property
    def _ap_owned_gadgets(self):
        return self.planet.weapons.ap_gadgets

    @_ap_owned_gadgets.setter
    def _ap_owned_gadgets(self, values):
        self.planet.weapons.ap_gadgets = values

    def _refresh_main_menu_state(self) -> bool:
        """Fresh, unconditional read of the raw in-game planet id — independent of PlanetInventory.planet_id, which only ever holds the LAST real planet seen and never regresses to 0 on its own."""
        raw_planet_id = self.pine.read_int8(address_maps.CURRENT_PLANET_ADDRESS)
        now_at_main_menu = not raw_planet_id
        if now_at_main_menu != self.at_main_menu or not self._main_menu_state_known:
            self.at_main_menu = now_at_main_menu
            self._main_menu_state_known = True
            if now_at_main_menu:
                self._log("[RAC] Player at main menu — waiting for a save to load before applying AP state.")
            else:
                self._log("[RAC] Save loaded — resuming normal play.")
                # A save written mid-trap carries the trap's flags; clear any we aren't tracking.
                reconcile_traps(self.pine)
        return self.at_main_menu

    def wire(
        self,
        send_location: Callable[[str], None],
        send_deathlink: Callable[[int], None] | None = None,
        death_amnesty: Callable[[], int] | None = None,
        death_link_enabled: Callable[[], bool] | None = None,
        on_goal: Callable[[], None] | None = None,
        on_planet_ready: Callable[[], None] | None = None,
        on_initial_load: Callable[[], None] | None = None,
        on_vendor_open: Callable[[], None] | None = None,
        on_vendor_close: Callable[[], None] | None = None,
        on_equipped_armour_saved: Callable[[dict[str, int]], None] | None = None,
        on_bonus_weapon_pickup: Callable[[str], None] | None = None,
        on_scripted_gadget_pickup: Callable[[str], None] | None = None,
        on_weapon_level_up: Callable[[], None] | None = None,
    ) -> None:
        self.send_location = send_location
        if send_deathlink is not None:
            self.send_deathlink = send_deathlink
        if death_amnesty is not None:
            self.death_amnesty = death_amnesty
        if death_link_enabled is not None:
            self.death_link_enabled = death_link_enabled
        if on_goal is not None:
            self.on_goal = on_goal
        if on_planet_ready is not None:
            self.on_planet_ready = on_planet_ready
        if on_initial_load is not None:
            self.on_initial_load = on_initial_load
        if on_vendor_open is not None:
            self.on_vendor_open = on_vendor_open
        if on_vendor_close is not None:
            self.on_vendor_close = on_vendor_close
        if on_equipped_armour_saved is not None:
            self.on_equipped_armour_saved = on_equipped_armour_saved
        if on_bonus_weapon_pickup is not None:
            self.on_bonus_weapon_pickup = on_bonus_weapon_pickup
        if on_scripted_gadget_pickup is not None:
            self.on_scripted_gadget_pickup = on_scripted_gadget_pickup
        if on_weapon_level_up is not None:
            self.on_weapon_level_up = on_weapon_level_up

    @property
    def vendor_active(self) -> bool:
        return self.weapon_vendor.active or self.mod_vendor.active

    def _planet_settled(self) -> bool:
        """False for _PLANET_SETTLE_SECONDS after a planet becomes ready — see that constant's comment."""
        return time.monotonic() >= self._planet_settle_until

    def apply_inventory(
        self,
        *,
        weapons: dict[str, bool],
        gadgets: dict[str, bool],
        weapon_levels: dict[str, int],
        weapon_mods: dict[str, set[str]],
        armour_unlocked: dict[str, int],
        infobot_planets: set[str],
        challenge_mode: int = 0,
        clank_pack: bool = False,
    ) -> None:
        return InventorySync(self).apply_inventory(
            weapons=weapons,
            gadgets=gadgets,
            weapon_levels=weapon_levels,
            weapon_mods=weapon_mods,
            armour_unlocked=armour_unlocked,
            infobot_planets=infobot_planets,
            challenge_mode=challenge_mode,
            clank_pack=clank_pack,
        )

    def _sync_weapon_gadget_ownership(self) -> None:
        return InventorySync(self)._sync_weapon_gadget_ownership()

    def restore_world_states(self, checked_locations: set[str]) -> None:
        return InventorySync(self).restore_world_states(checked_locations)

    def restore_armour_from_locations(self, checked_locations: set[str]) -> None:
        return InventorySync(self).restore_armour_from_locations(checked_locations)

    def sync_from_ap(self, checked_locations: set[str]) -> None:
        return InventorySync(self).sync_from_ap(checked_locations)

    def spawn_ghost_ratchet(self) -> bool:
        """Manually triggered via /spawn_ghost. Only works on planets present
        in GHOST_RATCHET_ADDRESSES — returns False on any other planet."""
        if self.at_main_menu:
            return False
        planet_id = self.planet.planet_id
        if planet_id is None:
            return False
        return self.ghost_ratchet.spawn(planet_id)

    def notify(self, text: bytes | str) -> None:
        """Draw a timed item message without activating a Triangle prompt."""
        self.native.notify(text)

    def tick(self) -> None:
        """One poll cycle, called once per tick by the client's poll loop. Doesn't
        manage its own timing or swallow errors, so connection problems surface to the caller."""
        service_traps(self.pine)
        if self.native.tick():
            return
        if self._refresh_main_menu_state():
            return
        previous_planet_id = self.planet.planet_id
        became_ready = self.planet.check_transition()
        self.planet_unlock.check()

        for name in self.planet.check_giant_clank():
            self.send_location(name)

        if self.planet.giant_clank_active:
            return

        if self.planet.planet_id == _KALIDON_RACE_ID:
            if self.planet.is_ready and self.skyboard_enabled:
                for name in self.skyboard.check():
                    self.send_location(name)
            return

        self.planet.check_controller()
        self.planet.check_death()
        self.planet.check_equipped_armour()

        if not self.planet.is_ready:
            return

        if became_ready:
            self._planet_settle_until = time.monotonic() + _PLANET_SETTLE_SECONDS
            self.planet.weapons.wipe(preserve_levels=previous_planet_id == _KALIDON_RACE_ID)
            if not self._initial_load_done:
                self.planet.weapon_cycler.initialize(self._first_owned_weapon_id)
            if self._ap_inventory_ready:
                # Skip until apply_inventory() has run this session, or ap_armour/_ap_owned_*
                # are still empty defaults and stale save memory reads as a brand-new pickup.
                self._sync_weapon_gadget_ownership()
                if (
                    not self.vendor_active
                    and not self.planet.player.is_dead
                    and not self.planet.player.is_picking_up
                    and not self.planet.giant_clank_active
                ):
                    self._report_new_armour_pickups()
                    self.armour.apply_full()
            if self.native.armour is None:
                self.armour_spawn_gate.apply(self.planet.planet_id)
            self.skin.setup()
            self.challenge_mode.setup()
            if self.clank_enabled:
                self.clank.setup(self.clank_all_challenges)
            self.on_planet_ready()
            if not self._initial_load_done:
                self._initial_load_done = True
                self.on_initial_load()

        if not self._ap_inventory_ready:
            return

        self.skin.apply_pending(
            self.native.skin,
            allowed=(
                self._planet_settled()
                and self.planet.menu.get() == MenuStateValue.CLOSED
                and not self.planet.player.is_dead
                and not self.planet.player.is_picking_up
                and not self.planet.giant_clank_active
            ),
        )
        self.quick_select.check()

        if self._planet_settled():
            LocationChecks(self).world()
        self.shrink_ray.set_skip(
            self.planet.planet_id,
            self.shrink_ray_skips_enabled
            and not self.shrink_ray_locations_enabled
            and self._ap_owned_gadgets.get("shrink_ray", False),
        )

        if self.planet.planet_id is not None:
            self.ghost_ratchet.keep_alive(self.planet.planet_id)

        self.planet.weapons.update_progression(self.weapon_vendor.active)
        self.player_bolts.apply_boost()
        self.player_health_exp.apply_boost()
        if self.nanotech_level_checks_enabled:
            LocationChecks(self).nanotech()
        self._check_armour_pickups()
        self._check_vendor_purchases()
        self.planet.check_weapon_cycler(
            is_ap_owned=self._is_weapon_id_ap_owned,
            vendor_active=self.vendor_active,
            fallback_weapon_id=self._first_owned_weapon_id,
        )

    def _is_weapon_id_ap_owned(self, weapon_id: int) -> bool:
        """WEAPON_VENDOR_IDS-scheme id -> AP ownership, shared by
        WeaponCyclerInventory and QuickSelectState."""
        name = _CYCLER_ID_TO_WEAPON_NAME.get(weapon_id)
        if name is None:
            return False
        return self._ap_owned_weapons.get(name, False) or self._ap_owned_gadgets.get(name, False)

    def _first_owned_weapon_id(self) -> int | None:
        """Lowest WEAPON_VENDOR_IDS id among AP-owned weapons (gadgets excluded),
        or None if AP hasn't granted any weapon yet; fills an empty current_weapon."""
        owned_ids = [
            WEAPON_VENDOR_IDS[name]
            for name, owned in self._ap_owned_weapons.items()
            if owned and name in WEAPON_VENDOR_IDS
        ]
        return min(owned_ids) if owned_ids else None

    def _check_armour_pickups(self) -> None:
        """Every-tick diff (titanium-bolt style, see ArmourInventory.check()) -- also runs planet.check_collected_armour() first, which now only preserves the equipped loadout across the pickup animation and no longer does any pickup detection itself."""
        self.planet.check_collected_armour()
        self._report_new_armour_pickups()

    def _report_new_armour_pickups(self) -> None:
        LocationChecks(self).armour()

    def _suppress_forced_starter_items(self, changed: dict[str, list], is_vendor: bool) -> None:
        return PurchaseChecks(self)._suppress_forced_starter_items(changed, is_vendor)

    def _check_vendor_purchases(self) -> None:
        return PurchaseChecks(self)._check_vendor_purchases()

    def _handle_death(self) -> None:
        self.armour.apply_collected_only()

        if not self.death_link_enabled():
            return
        self._death_count += 1
        if self._death_count > self.death_amnesty():
            cause = int(self.planet.player.movement_state)
            self.send_deathlink(cause)

    def _handle_respawn(self) -> None:
        self._death_count = 0
        self._report_new_armour_pickups()
        self.armour.apply_full()
        self._sync_weapon_gadget_ownership()

    def __repr__(self) -> str:
        return f"Core(planet_id={self.planet.planet_id}, is_ready={self.planet.is_ready})"
