"""Install native checks before level startup and consume their journals."""

import logging
from collections import deque

from ..constants import Rac5Locations
from ..locations import GADGET_INTERNAL_TO_LOCATION, TITAN_INTERNAL_TO_LOCATION, WEAPON_INTERNAL_TO_LOCATION
from . import vendor_presentation
from . import address_maps
from .address_maps import CURRENT_PLANET_ADDRESS, NEW_PLANET_START_LOAD_ADDR, PLANET_ADDRESSES
from .armour import ARMOUR_PICKUPS, ArmourPiece, ArmourStruct
from .menu import MenuStateValue
from .patches import (
    PatchOptions,
    armour_pickup,
    balance_patch,
    connection_warning,
    inside_clank_exit,
    item_toast,
    multiplayer_skins,
    pokitaru_ship,
    ship_menu,
    skins,
    sprout_pickup,
    vendor as vendor_patch,
)
from .patches.loader_gate import LoaderGate
from .patches.starting_planet import StartingPlanet
from .vendor import WEAPON_VENDOR_IDS
from .traps import close_no_clank_trap

logger = logging.getLogger("CommonClient")


class NativeRuntime:
    def __init__(self, pine, vendor, send_location, log, shrink_ray=None, patch_options=None):
        self.patch_options = patch_options or PatchOptions()
        self.pine, self.vendor = pine, vendor
        self.send_location, self.log = send_location, log
        self.gate = LoaderGate(pine, game_id=address_maps.GAME_ID)
        self.starting_planet = StartingPlanet(pine, log, game_id=address_maps.GAME_ID)
        self.shrink_ray = shrink_ray
        self.vendor_scouts = None
        self.presentation = None
        self._presentation_pending = None
        self.enabled = False
        self.checked = set()
        self.allowed_locations = None
        self.progressive_challenge_mode_enabled = False
        self.notifications = deque()
        self.plans = []
        self.module = None
        self.pickup = None
        self.toast = None
        self.connection_warning = None
        self.ap_connected = False
        self.skin = None
        self.armour = None
        self._released = False
        self._attach_reload_requested = False
        self.waiting = False
        self.balance = None
        self.balance_callback = None
        self._installed_balance_option = self.patch_options.balance_patch

    def close(self):
        if self.pine.get_game_id() != self.gate.game_id:
            return
        try:
            close_no_clank_trap(self.pine)
            self.starting_planet.close()
            if (
                self.connection_warning is not None
                and self.connection_warning.installed
                and self.pine.get_game_id() == self.gate.game_id
                and self.pine.read_int32(self.gate.STATE) == 6
                and self.pine.read_int32(address_maps.CURRENT_PLANET_ADDRESS) == self.module
            ):
                connection_warning.refresh(self.connection_warning, False)
            if self.presentation is not None:
                self.presentation.close()
            if (
                self.shrink_ray is not None
                and self.shrink_ray.plan is not None
                and self.shrink_ray.plan.installed
                and self.pine.get_game_id() == self.gate.game_id
                and self.pine.read_int32(address_maps.CURRENT_PLANET_ADDRESS) == self.shrink_ray.planet
            ):
                self.shrink_ray.plan.restore()
        finally:
            if self.gate.armed and self.pine.get_game_id() == self.gate.game_id:
                self.gate.release()

    def _prepare(self, target, base):
        planet = self.vendor.planet
        planet.is_ready = False
        planet._pending_planet_id = target
        planet._prev_gate = -1
        self.presentation = None
        self._presentation_pending = None
        self.plans = []
        self.pickup = None
        self.toast = None
        self.connection_warning = None
        self.skin = None
        self.armour = None
        self.vendor.native_plan = None
        self.balance = None
        self.balance_callback = None
        self._installed_balance_option = self.patch_options.balance_patch
        if target not in PLANET_ADDRESSES and not (target == 15 and self.patch_options.balance_patch):
            if target == 15:
                self.module = target
                self._attach_reload_requested = False
            return
        p = self.pine
        options = self.patch_options
        # Include relocated switch tables too (Dayni Moon's ship-menu table
        # lies beyond the old 0x240000-byte executable-only window).
        code = b"".join(p.read_bytes(base + offset, 0x10000) for offset in range(0, 0x280000, 0x10000))
        if options.balance_patch:
            self.balance = balance_patch.prepare(p, planet=target, code_start=base, code=code)
        if target not in PLANET_ADDRESSES:
            if self.balance is not None:
                self.plans.append(self.balance)
            for patch in self.plans:
                patch.install()
            self.module = target
            self._attach_reload_requested = False
            return
        pieces = [ArmourPiece.CHESTPLATE, ArmourPiece.HELMET, ArmourPiece.GLOVES, ArmourPiece.BOOTS]
        armour_locations = {
            ArmourStruct.SET_FIELDS.index(pickup.set_key) * 4 + pieces.index(pickup.piece): pickup.name
            for pickup in ARMOUR_PICKUPS
            if self.allowed_locations is None or pickup.name in self.allowed_locations
        }
        self.armour = (
            armour_pickup.prepare(
                p,
                code_start=base,
                code=code,
                locations=armour_locations,
                checked=self.checked,
                bypass_tier_gate=not self.progressive_challenge_mode_enabled,
            )
            if options.armour_pickup
            else None
        )
        # Shrink Ray only binds here: its door locks are live objects, so Core
        # installs it via set_skip() once the planet has initialised them.
        if self.shrink_ray is not None and options.shrink_ray:
            self.shrink_ray.bind(target, base, code)
        presentation = (
            vendor_presentation.prepare(p, base, code)
            if self.vendor_scouts is not None and options.vendor_presentation
            else None
        )
        base_locations = {
            WEAPON_VENDOR_IDS[name]: loc
            for name, loc in (WEAPON_INTERNAL_TO_LOCATION | GADGET_INTERNAL_TO_LOCATION).items()
            if self.allowed_locations is None or loc in self.allowed_locations
        }
        titans = {
            WEAPON_VENDOR_IDS[name]: loc
            for name, loc in TITAN_INTERNAL_TO_LOCATION.items()
            if self.allowed_locations is None or loc in self.allowed_locations
        }
        plan = (
            vendor_patch.prepare(
                p,
                code_start=base,
                code=code,
                base_locations=base_locations,
                titan_locations=titans,
                checked=self.checked,
            )
            if options.vendor
            else None
        )
        skin_plans = []
        hud_plans = []
        box = PLANET_ADDRESSES[target].small_text_box
        if box is not None and plan is not None and options.skins:
            has_hero_buffer = p.read_int32(multiplayer_skins.mcp_address(self.gate.game_id) + 0x2DC) != 0
            extended = has_hero_buffer and options.multiplayer_skins
            self.skin = skins.prepare(
                p,
                code_start=base,
                code=code,
                arena=plan.arena,
                menu=PLANET_ADDRESSES[target].menu,
                model_count=multiplayer_skins.COUNT if extended else 7,
            )
            skin_plans.append(self.skin)
            if extended:
                skin_plans.append(multiplayer_skins.prepare(p, code_start=base, code=code, skin=self.skin))
            if options.item_toast:
                self.toast = item_toast.prepare(
                    p, code_start=base, code=code, small_box=box, starter=plan.starter, frame_hook=self.skin.entry
                )
                if options.connection_warning:
                    self.connection_warning = connection_warning.prepare(
                        p, arena=plan.arena, font=self.toast.font, colour=self.toast.colour, text=self.toast.text
                    )
                    hud_plans.append(self.connection_warning)
                    self.toast = item_toast.prepare(
                        p,
                        code_start=base,
                        code=code,
                        small_box=box,
                        starter=plan.starter,
                        frame_hook=self.skin.entry,
                        status_hook=self.connection_warning.entry,
                    )
        if self.balance is not None and target in (2, 10):
            if plan is None:
                raise RuntimeError("Balance patch conditional effects require the native vendor storage")
            if self.toast is None:
                self.toast = item_toast.prepare(
                    p, code_start=base, code=code, small_box=box, starter=plan.starter,
                    frame_hook=self.skin.entry if self.skin is not None else None,
                )
            callback = balance_patch.prepare_callback(
                p, balance=self.balance, arena=plan.arena,
                max_health=PLANET_ADDRESSES[target].max_health, toast=self.toast,
            )
            self.balance_callback = callback
            hud_plans.append(callback)
            self.toast = item_toast.prepare(
                p, code_start=base, code=code, small_box=box, starter=plan.starter,
                frame_hook=self.skin.entry if self.skin is not None else None,
                status_hook=self.connection_warning.entry if self.connection_warning is not None else None,
                balance_hook=callback.entry,
            )
        if self.toast is not None:
            hud_plans.append(self.toast)
        planet_plans = []
        if target == 1 and options.pokitaru_ship:
            planet_plans.append(pokitaru_ship.prepare(p, gate=self.gate))
        elif target == 2 and options.sprout_pickup:
            self.pickup = sprout_pickup.prepare(p, gate=self.gate, checked=Rac5Locations.RYLLUS_SPROUT in self.checked)
            planet_plans.append(self.pickup)
        if target == 9 and plan is not None and options.inside_clank_exit:
            planet_plans.append(
                inside_clank_exit.prepare(p, code_start=base, code=code, arena=plan.arena, gate=self.gate)
            )
        # Install order: armour pickup, skins, balance, ship menu, vendor, HUD
        # (connection warning, balance callback, item toast), then planet-specific.
        self.plans = [
            patch
            for patch in (
                self.armour,
                *skin_plans,
                self.balance,
                ship_menu.prepare(p, code_start=base, code=code) if options.ship_menu else None,
                plan,
                *hud_plans,
                *planet_plans,
            )
            if patch is not None
        ]
        installed = []
        try:
            for patch in self.plans:
                patch.install()
                installed.append(patch)
        except Exception:
            for patch in reversed(installed):
                patch.restore()
            self.plans = []
            self.pickup = None
            self.skin = None
            raise
        self.vendor.native_plan = plan
        # Stage 5 follows the held relocation stage. Keep the new display
        # pending until gameplay is ready so loading cleanup cannot discard it.
        self._presentation_pending = presentation
        self.module = target
        self._attach_reload_requested = False
        self.log(f"[RAC] Native vendor checks active for planet {target}.")

    def _eligible_titans(self):
        if not self.vendor.planet.is_ready or self.vendor.planet.planet_id != self.module:
            return set()
        return {WEAPON_VENDOR_IDS[name] for name in TITAN_INTERNAL_TO_LOCATION if self.vendor._is_titan_pending(name)}

    def notify(self, text):
        self.notifications.append(text)

    def _report(self, name):
        if name not in self.checked and (self.allowed_locations is None or name in self.allowed_locations):
            self.send_location(name)
            self.checked.add(name)

    def _poll(self):
        if (self.balance_callback is not None and self.balance_callback.needs_doors
                and self.vendor.planet.is_ready):
            balance_patch.bind_doors(self.balance_callback)
        if self.connection_warning is not None:
            connection_warning.refresh(self.connection_warning, self.ap_connected)
        if self.vendor.planet.is_ready and self._presentation_pending is not None:
            self.presentation = self._presentation_pending
            self._presentation_pending = None
        if self.presentation is not None and self.vendor.planet.is_ready:
            try:
                self.presentation.tick(
                    self.vendor.planet.menu.get() == MenuStateValue.WEAPONS_VENDOR, self.vendor_scouts
                )
            except RuntimeError as exc:
                logger.warning("[RAC] Vendor display disabled for this level: %s", exc)
                try:
                    self.presentation.close()
                except RuntimeError as cleanup:
                    logger.warning("[RAC] Vendor display cleanup needs a level reload: %s", cleanup)
                self.presentation = None
        plan = self.vendor.native_plan
        if plan is not None:
            plan._validate(replacement=True)
            for kind, table in plan.tables.items():
                flags = self.pine.read_bytes(table, 32 if kind == "base" else 16)
                for slot, name in plan.locations[kind].items():
                    if flags[slot] == 2 and name not in self.checked:
                        self.vendor.record_native_purchase(kind, name)
                        self._report(name)
                    elif name in self.checked and flags[slot] != 2:
                        self.pine.write_int8(table + slot, 2)
            table = plan.tables["titan"]
            for slot in self._eligible_titans():
                if self.pine.read_int8(table + slot) == 3:
                    self.pine.write_int8(table + slot, 1)
        if self.pickup is not None:
            self.pickup._validate(replacement=True)
            journal = self.pickup.journals[0][0]
            if self.pine.read_int8(journal) == 2:
                self._report(Rac5Locations.RYLLUS_SPROUT)
            elif Rac5Locations.RYLLUS_SPROUT in self.checked:
                self.pine.write_int8(journal, 2)
        if self.armour is not None:
            self.armour._validate(replacement=True)
            flags = self.pine.read_bytes(self.armour.table, 32)
            for slot, name in self.armour.locations.items():
                if flags[slot] == 2:
                    self._report(name)
                elif name in self.checked:
                    self.pine.write_int8(self.armour.table + slot, 2)
        if (
            self.toast is not None
            and self.notifications
            and self.vendor.planet.is_ready
            and self.vendor.planet.menu.get() == MenuStateValue.CLOSED
            and self.pine.read_int32(self.toast.timer) == 0
        ):
            item_toast.show(self.toast, self.notifications[0])
            self.notifications.popleft()

    def tick(self):
        """Return True while normal Core polling must wait for the loader."""
        self.waiting = self._tick()
        return self.waiting

    def _tick(self):
        if not self.enabled:
            return False
        self.starting_planet.service(self.vendor.planet.starting_planet_id)
        p = self.pine
        state = p.read_int32(self.gate.STATE)
        if self._released:
            if state == 4:
                return True
            self._released = False
        if self.gate.armed and p.read_int32(self.gate.SITE) == self.gate.ORIGINAL:
            self.gate.armed = False
        self.gate.arm()
        held = self.gate.held_module()
        if held is not None:
            try:
                self._prepare(*held)
            finally:
                self.gate.release()
                self._released = True
            return True
        if state != 6:
            if self.presentation is not None:
                try:
                    self.presentation.close()
                except RuntimeError:
                    pass
                self.presentation = None
            return state in (4, 5)
        target = p.read_int32(address_maps.CURRENT_PLANET_ADDRESS)
        if self._installed_balance_option != self.patch_options.balance_patch:
            self.module = None
        if self.module == target and (
            self.vendor.native_plan is not None or not self.patch_options.vendor or target == 15
        ):
            try:
                if self.vendor.native_plan is not None:
                    self.vendor.native_plan._validate(replacement=True)
                if self.shrink_ray is not None and self.shrink_ray.plan is not None:
                    self.shrink_ray.plan._validate(replacement=self.shrink_ray.plan.installed)
                if self.balance is not None:
                    self.balance._validate(replacement=True)
            except RuntimeError:
                self.module = None
            else:
                self._poll()
                return False
        balance_flying_level = target == 15 and (self.patch_options.balance_patch or self.balance is not None)
        if (target in PLANET_ADDRESSES or balance_flying_level) and self.module != target and not self._attach_reload_requested:
            if p.read_int32(address_maps.NEW_PLANET_START_LOAD_ADDR) == 0xFFFFFFFF:
                self._attach_reload_requested = True
                self.vendor.planet.is_ready = False
                p.write_int32(address_maps.NEW_PLANET_START_LOAD_ADDR, target)
                self.log("[RAC] Reloading this planet once to install native checks before object initialization.")
                return True
        return False
