from dataclasses import dataclass

from ..constants import Rac5Locations
from ..locations import TITAN_INTERNAL_TO_LOCATION
from .inventory_sync import _SCRIPTED_GADGET_LOCATIONS
from .location_checks import LocationChecks
from .menu import MenuStateValue

_GAME_FORCED_WEAPONS = frozenset(("lacerator", "acid_bomb_glove"))
_GAME_FORCED_GADGETS = frozenset(("hypershot", "sprout_o_matic", "shrink_ray", "map_o_matic", "box_breaker"))
_BONUS_TRIGGER_WEAPONS = frozenset(("concussion_gun",))
_SCRIPTED_PICKUP_GADGETS = frozenset()
_POKITARU_ID = 1


@dataclass
class PurchaseChecks:
    core: object

    def _suppress_forced_starter_items(self, changed: dict[str, list], is_vendor: bool) -> None:
        """Strip game-forced weapons/gadgets out of check_weapons()'s "changed" lists when not AP-owned, and zero them back in memory."""
        core = self.core
        if is_vendor:
            return
        wi = core.planet.weapons
        kept_weapons = []
        forced_this_tick: set[str] = set()
        for name in changed["weapons"]:
            if name in _GAME_FORCED_WEAPONS and (not core._ap_owned_weapons.get(name, False)):
                wi.set(name, False)
                wi.weapons[name] = False
                forced_this_tick.add(name)
                continue
            kept_weapons.append(name)
        changed["weapons"] = kept_weapons
        if forced_this_tick:
            changed["levels"] = [(name, level) for name, level in changed["levels"] if name not in forced_this_tick]
            for name in forced_this_tick:
                wi._raw_level.pop(name, None)
        kept_gadgets = []
        for name in changed["gadgets"]:
            if name in _GAME_FORCED_GADGETS and (not core._ap_owned_gadgets.get(name, False)):
                wi.set(name, False)
                wi.gadgets[name] = False
                continue
            kept_gadgets.append(name)
        changed["gadgets"] = kept_gadgets

    def _check_vendor_purchases(self) -> None:
        """Track vendor visits, including the PDA's separate ammo-only menu."""
        core = self.core
        current = core.planet.menu.get()
        vendor_states = (MenuStateValue.WEAPONS_VENDOR, MenuStateValue.MOD_VENDOR, MenuStateValue.PDA)
        is_vendor = current in vendor_states
        was_vendor = core._prev_vendor in vendor_states
        changed_vendor = current != core._prev_vendor
        core._prev_vendor = current
        if was_vendor and changed_vendor:
            core.weapon_vendor.deactivate()
            core.mod_vendor.deactivate()
            core.vendor.close()
            core.quick_select.restore()
            core.quick_select.unfreeze()
            core.on_vendor_close()
        if is_vendor and changed_vendor:
            core.quick_select.sync()
            core.quick_select.freeze()
            if current in (MenuStateValue.WEAPONS_VENDOR, MenuStateValue.PDA):
                core.weapon_vendor.activate()
            else:
                core.mod_vendor.activate()
            core.on_vendor_open()
        if current == MenuStateValue.PDA:
            core.vendor.pda_vendor()
            return
        if current == MenuStateValue.WEAPONS_VENDOR:
            core.vendor.weapon_vendor()
            return
        if current == MenuStateValue.MOD_VENDOR:
            core.vendor.mod_vendor()
            return
        changed = core.planet.check_weapons()
        if core._planet_settled():
            for name in changed["gadgets"]:
                loc = _SCRIPTED_GADGET_LOCATIONS.get(name)
                if loc and (not (core.native.pickup is not None and loc == Rac5Locations.RYLLUS_SPROUT)):
                    core.send_location(loc)
        core._suppress_forced_starter_items(changed, is_vendor)
        if core.planet.planet_id == _POKITARU_ID:
            for name in changed["weapons"]:
                if name in _BONUS_TRIGGER_WEAPONS:
                    core.on_bonus_weapon_pickup(name)
            for name in changed["gadgets"]:
                if name in _SCRIPTED_PICKUP_GADGETS:
                    core.on_scripted_gadget_pickup(name)
        if changed["levels"]:
            if core.weapon_level_checks_enabled:
                LocationChecks(core).weapon_levels(changed["levels"])
            core.on_weapon_level_up()
        for name in changed["titans"]:
            titan_loc = TITAN_INTERNAL_TO_LOCATION.get(name)
            if titan_loc:
                core.planet.weapons.titan_purchased[name] = True
                core.send_location(titan_loc)
