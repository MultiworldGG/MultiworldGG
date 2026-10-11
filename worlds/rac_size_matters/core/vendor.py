from collections.abc import Callable
from typing import TYPE_CHECKING

from ..constants import Rac5GadgetKeys, Rac5ModVendorLocations
from ..locations import (
    GADGET_INTERNAL_TO_LOCATION,
    MOD_INTERNAL_TO_LOCATION,
    TITAN_INTERNAL_TO_LOCATION,
    WEAPON_INTERNAL_TO_LOCATION,
    WEAPON_LEVEL_LOOKUP,
)
from . import address_maps
from .address_maps import PLANET_ADDRESSES, WEAPON_VENDOR_ITEMS, WEAPON_VENDOR_SLOTS
from .controller import GlobalButtonState, PauseSelectButtons
from .menu import MenuStateValue
from .weapons import TITAN_ELIGIBLE_WEAPONS

if TYPE_CHECKING:
    from ..pypine import Pine
    from .planets import PlanetInventory, PlanetUnlockState
    from .weapons import WeaponInventory

MAX_VENDOR_SLOTS = (address_maps.WEAPON_VENDOR_SLOTS - address_maps.WEAPON_VENDOR_ITEMS) // 4

# array slot index + 2 offset. Confirmed in-game.
WEAPON_VENDOR_IDS: dict[str, int] = {
    "lacerator":        0x02,  # confirmed
    "concussion_gun":   0x03,
    "acid_bomb_glove":  0x04,
    "agents_of_doom":   0x05,
    "bee_mine_glove":   0x06,
    "static_barrier":   0x07,
    "shock_rocket":     0x08,
    "sniper_mine":      0x09,
    "scorcher":         0x0A,
    "laser_tracer":     0x0B,
    "suck_cannon":      0x0C,
    "mootator":         0x0D,
    "ryno":             0x0F,
    "hypershot":        0x10,
    "sprout_o_matic":   0x11,
    "polarizer":        0x12,
    "pda":              0x13,
    "shrink_ray":       0x14,
    "bolt_grabber":     0x15,
    "map_o_matic":      0x17,
    "box_breaker":      0x18,
}


_ITEM_IDS: dict[str, int] = WEAPON_VENDOR_IDS

# Legacy reachability tables below are used only when slot data has no vendor_rules.
# New seeds export their location and entrance rules; edit those definitions instead.
_WEAPON_TO_PLANET_KEY: dict[str, str] = {
    "lacerator":       "POKITARU",
    "acid_bomb_glove": "POKITARU",
    "concussion_gun":  "POKITARU",
    "agents_of_doom":  "RYLLUS",
    "scorcher":        "KALIDON",
    "suck_cannon":     "DREAMTIME",
    "bee_mine_glove":  "OUTPOST_OMEGA",
    "sniper_mine":     "CHALLAX",
    "shock_rocket":    "DAYNI_MOON",
    "static_barrier":  "INSIDE_CLANK",
    "laser_tracer":    "QUODRONA",
    "ryno":            "POKITARU",
}

_CHALLENGE_MODE_ONLY_WEAPONS: frozenset[str] = frozenset({"ryno"})

_TITAN_TO_PLANET_KEY: dict[str, str] = {
    **_WEAPON_TO_PLANET_KEY,
    "mootator": "DAYNI_MOON",
}
del _TITAN_TO_PLANET_KEY["ryno"]

_GADGET_TO_PLANET_KEY: dict[str, str] = {
    "hypershot":    "POKITARU",
    "pda":          "CHALLAX",
    "map_o_matic":  "DAYNI_MOON",
    "bolt_grabber": "CHALLAX",
    "box_breaker":  "OUTPOST_OMEGA",
}

_MOD_LOCATION_TO_PLANET_KEY: dict[str, str] = {
    Rac5ModVendorLocations.KALIDON_LACERATOR_LOCK:     "KALIDON",
    Rac5ModVendorLocations.KALIDON_CONCUSSION_SPLIT:   "KALIDON",
    Rac5ModVendorLocations.CHALLAX_LACERATOR_DOUBLE:   "CHALLAX",
    Rac5ModVendorLocations.CHALLAX_ACID_BURN:          "CHALLAX",
    Rac5ModVendorLocations.CHALLAX_ACID_EPOXY:         "CHALLAX",
    Rac5ModVendorLocations.CHALLAX_CONCUSSION_LOCK:    "CHALLAX",
    Rac5ModVendorLocations.CHALLAX_CONCUSSION_CHARGE:  "CHALLAX",
    Rac5ModVendorLocations.CHALLAX_BEE_WORKER:         "CHALLAX",
    Rac5ModVendorLocations.QUODRONA_AGENTS_LAUNCHER:   "QUODRONA",
    Rac5ModVendorLocations.QUODRONA_SCORCHER_SPITFIRE: "QUODRONA",
    Rac5ModVendorLocations.QUODRONA_SNIPER_SPLIT:      "QUODRONA",
    Rac5ModVendorLocations.QUODRONA_SHOCK_LOCK:        "QUODRONA",
    Rac5ModVendorLocations.QUODRONA_SHOCK_AFTER:       "QUODRONA",
    Rac5ModVendorLocations.KALIDON_AGENTS_EXPLOSIVE:       "KALIDON",
    Rac5ModVendorLocations.KALIDON_SCORCHER_SUNFLARE:      "KALIDON",
    Rac5ModVendorLocations.KALIDON_SUCK_CANNON_BOUNCE:     "KALIDON",
    Rac5ModVendorLocations.KALIDON_BEE_HIVE_BOMB:          "KALIDON",
    Rac5ModVendorLocations.CHALLAX_SNIPER_SMART_REFLECTOR: "CHALLAX",
    Rac5ModVendorLocations.CHALLAX_SHOCK_MULTI_LAUNCHER:   "CHALLAX",
    Rac5ModVendorLocations.KALIDON_STATIC_REFLECTION:      "KALIDON",
    Rac5ModVendorLocations.QUODRONA_STATIC_MIRAGE:         "QUODRONA",
    Rac5ModVendorLocations.CHALLAX_LASER_PIERCE:           "CHALLAX",
    Rac5ModVendorLocations.QUODRONA_LASER_RICOCHET:        "QUODRONA",
}

_CHALLENGE_MODE_MOD_LOCATIONS: frozenset[str] = frozenset({
    Rac5ModVendorLocations.KALIDON_AGENTS_EXPLOSIVE,
    Rac5ModVendorLocations.KALIDON_SCORCHER_SUNFLARE,
    Rac5ModVendorLocations.KALIDON_SUCK_CANNON_BOUNCE,
    Rac5ModVendorLocations.KALIDON_BEE_HIVE_BOMB,
    Rac5ModVendorLocations.CHALLAX_SNIPER_SMART_REFLECTOR,
    Rac5ModVendorLocations.CHALLAX_SHOCK_MULTI_LAUNCHER,
    Rac5ModVendorLocations.KALIDON_STATIC_REFLECTION,
    Rac5ModVendorLocations.QUODRONA_STATIC_MIRAGE,
    Rac5ModVendorLocations.CHALLAX_LASER_PIERCE,
    Rac5ModVendorLocations.QUODRONA_LASER_RICOCHET,
})

_MOD_VENDOR_EXTRA_GADGETS: dict[str, tuple[str, ...]] = {
    "CHALLAX": (Rac5GadgetKeys.SHRINK_RAY, Rac5GadgetKeys.POLARIZER),
}

_WEAPON_VENDOR_EXTRA_GADGETS: dict[str, tuple[str, ...]] = {
    "INSIDE_CLANK": (
        Rac5GadgetKeys.HYPERSHOT, Rac5GadgetKeys.SPROUT_O_MATIC,
        Rac5GadgetKeys.SHRINK_RAY, Rac5GadgetKeys.POLARIZER,
    ),
}

_SLOT_TO_UNLOCK_ATTR: dict[str, str] = {
    "mod_slot_one":   "mod_unlock_one",
    "mod_slot_two":   "mod_unlock_two",
    "mod_slot_three": "mod_unlock_three",
}


class WeaponVendorMenu:
    """Weapons vendor menu (sells weapons/gadgets) open/close toggle."""

    def __init__(self) -> None:
        self.active = False

    def activate(self) -> None:
        self.active = True

    def deactivate(self) -> None:
        self.active = False

    def __repr__(self) -> str:
        return f"WeaponVendorMenu(active={self.active})"


class ModVendorMenu:
    """Weapon mod vendor menu (sells mod slots) open/close toggle."""

    def __init__(self) -> None:
        self.active = False

    def activate(self) -> None:
        self.active = True

    def deactivate(self) -> None:
        self.active = False

    def __repr__(self) -> str:
        return f"ModVendorMenu(active={self.active})"


class VendorInventory:
    """Pine-backed accessor for the vendor item list/size array. add_weapon() tracks
    which names belong in the vendor's item list; refresh() writes that list to memory."""

    def __init__(
        self,
        pine: "Pine",
        planet: "PlanetInventory",
        planet_unlock: "PlanetUnlockState",
        send_location: Callable[[str], None],
        log: Callable[[str], None] | None = None,
        is_weapon_ap_owned: Callable[[str], bool] | None = None,
        is_gadget_ap_owned: Callable[[str], bool] | None = None,
        is_weapon_level_checks_enabled: Callable[[], bool] | None = None,
    ) -> None:
        self.pine = pine
        self.planet = planet
        self.planet_unlock = planet_unlock
        self.send_location = send_location
        self._log = log or (lambda msg: None)
        self._is_weapon_ap_owned = is_weapon_ap_owned or (lambda name: False)
        self._is_gadget_ap_owned = is_gadget_ap_owned or (lambda name: False)
        self._is_weapon_level_checks_enabled = is_weapon_level_checks_enabled or (lambda: False)
        self.weapons: WeaponInventory = planet.weapons
        self._items: list[str] = []

        self.challenge_mode: int = 0

        self._weapon_vendor_open:      bool = False
        self._mod_vendor_open:         bool = False
        self._pda_open:                bool = False
        self.show_purchasable_weapons: bool = True
        self.native_plan = None
        self._native_purchase_pending = False
        # None selects the legacy gates for seeds generated before rule export.
        self.location_rules = None
        self.rule_items: dict[str, int] = {}
        self._reached_cache: tuple[dict[str, int], set[str]] | None = None

    def configure_rules(self, data) -> None:
        from ..vendor_rules import VERSION

        if data is not None and data.get("version") != VERSION:
            raise ValueError("Unsupported vendor rules version")
        self.location_rules = data
        self.rule_items = {}
        self._reached_cache = None

    def _location_accessible(self, location: str | None) -> bool:
        from ..vendor_rules import location_accessible, reachable_regions

        if self.location_rules is None:
            raise RuntimeError("No exported vendor rules configured")
        # rule_items may be replaced or mutated in place, so key the cache on a snapshot.
        if self._reached_cache is None or self._reached_cache[0] != self.rule_items:
            self._reached_cache = (dict(self.rule_items),
                                   reachable_regions(self.location_rules["regions"], self.rule_items))
        return location_accessible(self.location_rules, location, self.rule_items, self._reached_cache[1])

    def record_native_purchase(self, kind: str, location: str) -> None:
        """Adopt a native journal event without inferring gameplay ownership."""
        self._native_purchase_pending = True
        if kind == "base":
            self.weapons.vendor_locations[location] = True
        else:
            name = next(name for name, loc in TITAN_INTERNAL_TO_LOCATION.items() if loc == location)
            self.weapons.titan_purchased[name] = True

    def controller(self) -> GlobalButtonState | None:
        """Current controller/pause-select button state, or None if no planet is loaded
        or its address isn't mapped (checked first since read() raises otherwise)."""
        planet_id = self.planet.planet_id
        if planet_id is None:
            return None
        planet = PLANET_ADDRESSES.get(planet_id)
        if planet is None or planet.controller_pause_select_v2 is None:
            return None
        return GlobalButtonState.read(self.pine, planet_id)

    def _owned_names(self) -> frozenset[str]:
        owned = {name for name, unlocked in self.weapons.weapons.items() if unlocked}
        owned |= {name for name, unlocked in self.weapons.gadgets.items() if unlocked}
        return frozenset(owned)

    def _is_purchased(self, name: str) -> bool:
        loc = WEAPON_INTERNAL_TO_LOCATION.get(name) or GADGET_INTERNAL_TO_LOCATION.get(name)
        return bool(loc and self.weapons.vendor_locations.get(loc, False))

    def _is_weapon_vendor_accessible(self, planet_key: str) -> bool:
        if not self.planet_unlock.is_vendor_accessible(planet_key):
            return False
        return all(
            self.weapons.gadgets.get(gadget, False)
            for gadget in _WEAPON_VENDOR_EXTRA_GADGETS.get(planet_key, ())
        )

    def _is_titan_eligible(self, name: str) -> bool:
        """Whether `name` still has an unbought Titan variant to offer:
        Challenge Mode 1+, one of TITAN_ELIGIBLE_WEAPONS, not yet bought."""
        if self.location_rules is not None:
            return (not self.weapons.titan_purchased.get(name, False)
                    and self._location_accessible(TITAN_INTERNAL_TO_LOCATION.get(name)))
        return (self.challenge_mode >= 1 and name in TITAN_ELIGIBLE_WEAPONS
                and not self.weapons.titan_purchased.get(name, False))

    def _is_titan_pending(self, name: str) -> bool:
        """True once `name`'s vendor slot should show the level-4 floor for its Titan
        purchase; requires the base location to be bought AT THIS VENDOR (not just AP
        ownership), so its own base location can still be sent. Mootator goes by real level."""
        if not self._is_titan_eligible(name):
            return False
        base_loc = WEAPON_INTERNAL_TO_LOCATION.get(name)
        if base_loc is None:
            return self.weapons.get_level(name) >= 3
        return self._is_purchased(name)

    @property
    def ammo_link_paused(self) -> bool:
        # The vendor no longer substitutes fake ammo values.
        return False

    def _purchasable_names(self) -> list[str]:
        """Weapons/gadgets shown on the vendor's default (left, buy-new) view. A
        Titan-eligible weapon stays listed (reusing the same slot) until its Titan
        variant is bought; Mootator has no base listing, so it only appears Titan-pending."""
        if self.location_rules is not None:
            names = []
            for name, location in WEAPON_INTERNAL_TO_LOCATION.items():
                target = TITAN_INTERNAL_TO_LOCATION.get(name) if self._is_purchased(name) else location
                if self._is_purchased(name) and self.weapons.titan_purchased.get(name, False):
                    continue
                if self._location_accessible(target):
                    names.append(name)
            # Mootator has no base purchase location.
            for name, location in TITAN_INTERNAL_TO_LOCATION.items():
                if name not in WEAPON_INTERNAL_TO_LOCATION and not self.weapons.titan_purchased.get(name, False):
                    if self.weapons.get_level(name) >= 3 and self._location_accessible(location):
                        names.append(name)
            for name, location in GADGET_INTERNAL_TO_LOCATION.items():
                if not self._is_purchased(name) and self._location_accessible(location):
                    names.append(name)
            return names
        names: list[str] = []
        for name, planet_key in _WEAPON_TO_PLANET_KEY.items():
            if name in _CHALLENGE_MODE_ONLY_WEAPONS and self.challenge_mode < 1:
                continue
            if not self._is_weapon_vendor_accessible(planet_key):
                continue
            if self._is_titan_eligible(name) or not self._is_purchased(name):
                names.append(name)
        if self._is_titan_eligible("mootator") and self.weapons.get_level("mootator") >= 3:
            mootator_planet_key = _TITAN_TO_PLANET_KEY["mootator"]
            if self._is_weapon_vendor_accessible(mootator_planet_key):
                names.append("mootator")
        for name, planet_key in _GADGET_TO_PLANET_KEY.items():
            if self._is_weapon_vendor_accessible(planet_key) and not self._is_purchased(name):
                names.append(name)
        return names

    def purchasable_locations(self) -> list[str]:
        """AP location names for every weapon/gadget/Titan variant currently purchasable
        at the vendor's default view, used to hint before the player has to browse."""
        locations: list[str] = []
        for name in self._purchasable_names():
            if self._is_titan_pending(name):
                loc = TITAN_INTERNAL_TO_LOCATION.get(name)
            else:
                loc = WEAPON_INTERNAL_TO_LOCATION.get(name) or GADGET_INTERNAL_TO_LOCATION.get(name)
            if loc:
                locations.append(loc)
        return locations

    def mod_locations(self) -> list[str]:
        """AP location names for every mod slot currently reachable, same hinting
        purpose as purchasable_locations() but for the mod vendor."""
        return [
            loc for (_weapon, _slot), loc in MOD_INTERNAL_TO_LOCATION.items()
            if self._is_mod_location_accessible(loc)
        ]

    def _is_mod_location_accessible(self, loc: str) -> bool:
        """Whether this location's mod vendor is actually reachable — planet
        accessibility alone isn't enough where an extra gadget or Challenge Mode gates it."""
        if self.location_rules is not None:
            return self._location_accessible(loc)
        if loc in _CHALLENGE_MODE_MOD_LOCATIONS and self.challenge_mode < 1:
            return False
        planet_key = _MOD_LOCATION_TO_PLANET_KEY.get(loc)
        if not planet_key or not self.planet_unlock.is_vendor_accessible(planet_key):
            return False
        return all(
            self.weapons.gadgets.get(gadget, False)
            for gadget in _MOD_VENDOR_EXTRA_GADGETS.get(planet_key, ())
        )

    def _mod_vendor_weapons(self) -> list[str]:
        """Weapons that should appear in the mod vendor's selection list: at least one of
        their mod locations is reachable, regardless of ownership (which only gates purchasability)."""
        weapons: list[str] = []
        for (weapon, _slot), loc in MOD_INTERNAL_TO_LOCATION.items():
            if self._is_mod_location_accessible(loc) and weapon not in weapons:
                weapons.append(weapon)
        return weapons

    def _apply_mod_unlock_flags(self) -> None:
        """Write mod_unlock_N — gated purely on reachability, not ownership, since AP's
        accessibility sweep assumes these locations are reachable regardless. Also forces
        the weapon's `unlocked` byte to match; temporary, undone by close()'s revert_unowned()."""
        reachable_weapons = set(self._mod_vendor_weapons())
        for (weapon, slot), loc in MOD_INTERNAL_TO_LOCATION.items():
            reachable = self._is_mod_location_accessible(loc)
            unlock_attr = _SLOT_TO_UNLOCK_ATTR[slot]
            self.weapons.set_mod_unlock(weapon, unlock_attr, reachable)
            self.weapons.set(weapon, weapon in reachable_weapons)

    def _set_items(self, names: list[str]) -> None:
        self._items = []
        for name in names:
            self.add_weapon(name)

    def _set_weapon_view(self, purchases: bool) -> None:
        if self.native_plan is None:
            raise RuntimeError("Native vendor patch must be installed before opening the vendor")
        self.native_plan._validate(replacement=True)
        if self._pda_open:
            purchases = False
        self.show_purchasable_weapons = purchases
        self.pine.write_int32(self.native_plan.view_mode, 0 if purchases else 1)
        names = self._purchasable_names() if purchases else [
            name for name in self.weapons.weapons if self._is_weapon_ap_owned(name)]
        self._set_items(names)
        self.refresh(MenuStateValue.PDA if self._pda_open else MenuStateValue.WEAPONS_VENDOR)

    def pda_vendor(self) -> None:
        """Use native PDA ammo prices and restrictions, without purchase views or controls."""
        if not self._pda_open:
            self._pda_open = True
            self._weapon_vendor_open = True
            self._set_weapon_view(False)

    def weapon_vendor(self) -> None:
        """D-pad left: native AP checks; D-pad right: real owned-weapon ammo.

        Only menu eligibility and the native view flag change. Purchases are
        consumed from journals by NativeRuntime, never inferred from inventory.
        """
        if not self._weapon_vendor_open:
            self._weapon_vendor_open = True
            self._set_weapon_view(bool(self._purchasable_names()))
        controller = self.controller()
        if controller is not None:
            if controller.pressed(PauseSelectButtons.D_PAD_RIGHT) and self.show_purchasable_weapons:
                self._set_weapon_view(False)
            elif controller.pressed(PauseSelectButtons.D_PAD_LEFT) and not self.show_purchasable_weapons:
                self._set_weapon_view(True)
        if self._native_purchase_pending:
            self._native_purchase_pending = False
            if self.show_purchasable_weapons:
                self._set_weapon_view(bool(self._purchasable_names()))

    def close(self) -> None:
        """Reset the view. Weapon visits require no inventory restoration."""
        if self._mod_vendor_open:
            self.weapons.revert_unowned(self._is_weapon_ap_owned)
        self._weapon_vendor_open = False
        self._mod_vendor_open = False
        self._pda_open = False
        self.show_purchasable_weapons = True
        self._native_purchase_pending = False

    def _refresh_mod_vendor(self) -> None:
        """(Re)build the mod vendor's weapon list and unlock flags, shared by the open
        edge, D_PAD_UP refresh, and post-purchase refresh. Passes the entire weapons_sold
        list as allowed_extra since a weapon must show unlocked to render as a selection."""
        weapons_sold = self._mod_vendor_weapons()
        self.weapons.apply_vendor_locations(frozenset(weapons_sold))
        self._apply_mod_unlock_flags()
        self._set_items(weapons_sold)
        self.refresh(MenuStateValue.MOD_VENDOR)

    def mod_vendor(self) -> None:
        """Called every tick while the mod vendor menu is open."""
        if not self._mod_vendor_open:
            self._mod_vendor_open = True
            self._refresh_mod_vendor()

        controller = self.controller()
        if controller is not None and controller.pressed(PauseSelectButtons.D_PAD_UP):
            self._refresh_mod_vendor()

        changed = self.weapons.check()

        for name in changed["weapons"]:
            if not self._is_weapon_ap_owned(name):
                self.weapons.weapons[name] = False

        newly_purchased = False
        for weapon, slot in changed["mods"]:
            loc = MOD_INTERNAL_TO_LOCATION.get((weapon, slot))
            if loc:
                self.weapons.vendor_locations[loc] = True
                self.send_location(loc)
                newly_purchased = True

        if self._is_weapon_level_checks_enabled():
            for name, level in changed["levels"]:
                loc = WEAPON_LEVEL_LOOKUP.get((name, level))
                if loc:
                    self.send_location(loc)

        if newly_purchased:
            self._refresh_mod_vendor()

    def add_weapon(self, weapon: str) -> None:
        """Add a rac5 weapon/gadget/Titan-variant pseudo name to the vendor's
        unlocked-item list."""
        if weapon in _ITEM_IDS and weapon not in self._items:
            self._items.append(weapon)

    def force_refresh(self) -> None:
        """Debug/manual command hook: rebuild and rewrite the open vendor's item list
        immediately, for verifying the write directly against a memory viewer."""
        if self._weapon_vendor_open:
            self._set_weapon_view(self.show_purchasable_weapons)
        elif self._mod_vendor_open:
            self._refresh_mod_vendor()

    def refresh(self, menu_value: MenuStateValue) -> None:
        """Write the current item list into game memory, then poke the menu update
        field so the game redraws the vendor instead of showing stale contents.
        Item ids (and the zeroed tail) are written BEFORE the count, not after —
        the game can render mid-write since these are independent PINE writes, not
        a single atomic transaction, so a count written first could be read against
        a still-stale item array and show leftover/duplicate entries (or let a
        purchase resolve against the wrong slot's id). Writing the count last means
        any torn read only ever sees a count the (already fully current) array
        satisfies."""
        item_ids = [_ITEM_IDS[name] for name in self._items]
        for i, item_id in enumerate(item_ids):
            self.pine.write_bytes(address_maps.WEAPON_VENDOR_ITEMS + i * 4, item_id.to_bytes(4, "little"))
        for i in range(len(item_ids), MAX_VENDOR_SLOTS):
            self.pine.write_bytes(address_maps.WEAPON_VENDOR_ITEMS + i * 4, (0).to_bytes(4, "little"))
        self.pine.write_bytes(address_maps.WEAPON_VENDOR_SLOTS, len(item_ids).to_bytes(4, "little"))
        self.planet.menu.set(menu_value)

    def __repr__(self) -> str:
        return (
            f"VendorInventory(items={list(self._items)}, "
            f"weapon_open={self._weapon_vendor_open}, mod_open={self._mod_vendor_open}, "
            f"show_purchasable={self.show_purchasable_weapons}, "
            f"planet_id={self.planet.planet_id!r}, controller={self.controller()!r})"
        )
