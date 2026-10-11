from __future__ import annotations

import struct as _struct
from collections.abc import Callable
from contextlib import contextmanager
from functools import wraps
from typing import TYPE_CHECKING

from ..constants import Rac5GadgetKeys, Rac5WeaponKeys
from ..data.weapons import (
    GADGET_DATA,
    WEAPON_DATA,
    WEAPON_EXP_THRESHOLDS,
    WEAPON_MAX_LEVELS,
    WEAPON_MOD_COUNTS as WEAPON_MOD_COUNTS,
    WEAPON_VENDOR_DISPLAY_AMMO as WEAPON_VENDOR_DISPLAY_AMMO,
    Gadget as Gadget,
    Weapon as Weapon,
)
from .inventory import InventoryEntry, InventoryField
from .locations import weapon_locations as _weapon_locations
from .memory import MemoryWindow

if TYPE_CHECKING:
    from ..pypine import Pine


WEAPON_STRUCT_SIZE = 0x58
WEAPON_MIN_CONSECUTIVE = 4

PROGRESSIVE_OFF = 0
PROGRESSIVE_MANUAL = 1
PROGRESSIVE_AUTOMATIC = 2


TITAN_ELIGIBLE_WEAPONS: frozenset[str] = frozenset(key for key in WEAPON_DATA if key != Rac5WeaponKeys.RYNO)


def exp_threshold_for_level(weapon: str, level: int) -> int | None:
    """Fixed experience value required to reach `level` (1-indexed) for `weapon`,
    or None if there's no threshold for that level."""
    thresholds = WEAPON_EXP_THRESHOLDS.get(weapon, ())
    idx = level - 2
    if idx < 0 or idx >= len(thresholds):
        return None
    return thresholds[idx]


def is_weapon_candidate(data: bytes, i: int) -> bool:
    if i + 0x46 > len(data):
        return False
    if data[i + 0x3D] > 1 or data[i + 0x3E] > 1 or data[i + 0x3F] > 1:
        return False
    if data[i + 0x45] > 1:
        return False
    (level,) = _struct.unpack_from("<I", data, i + 0x2D)
    if level > 7:
        return False
    (ammo,) = _struct.unpack_from("<I", data, i + 0x31)
    if ammo > 9999:
        return False
    (icon,) = _struct.unpack_from("<I", data, i + 0x1D)
    if icon == 0:
        return False
    return True


def is_ps2_weapon_candidate(data: bytes, i: int) -> bool:
    if i + 0x46 > len(data):
        return False
    if data[i + 0x3D] > 1 or data[i + 0x3E] > 1 or data[i + 0x3F] > 1:
        return False
    if data[i + 0x45] > 1:
        return False
    (level,) = _struct.unpack_from("<I", data, i + 0x2D)
    if level > 7:
        return False
    (ammo,) = _struct.unpack_from("<I", data, i + 0x31)
    if ammo > 9999:
        return False
    (icon,) = _struct.unpack_from("<I", data, i + 0x1D)
    if icon == 0:
        return False
    (item,) = _struct.unpack_from("<I", data, i + 0x15)
    if item == 0:
        return False
    return True


class WeaponByteField:
    """Pine-backed accessor for a single-byte weapon struct field
    (unlocked, mod_slot_N, mod_unlock_N)."""

    def __init__(self, field_name: str) -> None:
        self.field_name = field_name

    def _address(self, instance) -> int:
        return instance.base + instance._OFFSETS[self.field_name]

    def __get__(self, instance, owner) -> bool | None:
        if instance is None:
            return None
        return bool(instance.read_field(self.field_name, 1))

    def __set__(self, instance, value: bool) -> None:
        if instance is None:
            return
        instance.write_field(self.field_name, int(value), 1)

    def __delete__(self, instance) -> None:
        if instance is None:
            return
        instance.write_field(self.field_name, 0, 1)


class WeaponInt32Field:
    """Pine-backed accessor for a single int32 weapon struct field."""

    def __init__(self, field_name: str) -> None:
        self.field_name = field_name

    def _address(self, instance) -> int:
        return instance.base + instance._OFFSETS[self.field_name]

    def __get__(self, instance, owner) -> int | None:
        if instance is None:
            return None
        return instance.read_field(self.field_name, 4)

    def __set__(self, instance, value: int) -> None:
        if instance is None:
            return
        instance.write_field(self.field_name, value, 4)

    def __delete__(self, instance) -> None:
        if instance is None:
            return
        instance.write_field(self.field_name, 0, 4)


class InventoryMemory:
    window: MemoryWindow | None = None

    def read_field(self, name, size):
        address = self.base + self._OFFSETS[name]
        if self.window is not None:
            return self.window.read(address, size)
        return int.from_bytes(self.pine.read_bytes(address, size), "little")

    def write_field(self, name, value, size):
        address = self.base + self._OFFSETS[name]
        if self.window is not None:
            self.window.write(address, value, size)
        else:
            self.pine.write_bytes(address, int(value).to_bytes(size, "little"))

    def read_bytes(self):
        return self.pine.read_bytes(self.base, WEAPON_STRUCT_SIZE)


def batched_inventory(method):
    @wraps(method)
    def call(self, *args, **kwargs):
        with self.memory():
            return method(self, *args, **kwargs)

    return call


class WeaponAddresses(InventoryMemory):
    """Pine-backed live accessor for one weapon struct instance — every
    field reads/writes memory directly via its descriptor."""

    _OFFSETS: dict[str, int] = {
        "level": 0x2D,
        "experience": 0x35,
        "mod_slot_one": 0x3D,
        "mod_slot_two": 0x3E,
        "mod_slot_three": 0x3F,
        "mod_unlock_one": 0x40,
        "mod_unlock_two": 0x41,
        "mod_unlock_three": 0x42,
        "unlocked": 0x45,
        "ammo": 0x31,
    }

    level = WeaponInt32Field("level")
    experience = WeaponInt32Field("experience")
    ammo = WeaponInt32Field("ammo")
    mod_slot_one = WeaponByteField("mod_slot_one")
    mod_slot_two = WeaponByteField("mod_slot_two")
    mod_slot_three = WeaponByteField("mod_slot_three")
    mod_unlock_one = WeaponByteField("mod_unlock_one")
    mod_unlock_two = WeaponByteField("mod_unlock_two")
    mod_unlock_three = WeaponByteField("mod_unlock_three")
    unlocked = WeaponByteField("unlocked")

    def __init__(self, base: int, pine: Pine) -> None:
        self.base = base
        self.pine = pine

    def __repr__(self) -> str:
        return f"WeaponAddresses(base=0x{self.base:08X}, unlocked={self.unlocked}, level={self.level})"


class GadgetAddresses(InventoryMemory):
    """Pine-backed live accessor for one gadget struct instance."""

    _OFFSETS: dict[str, int] = {
        "unlocked": 0x45,
    }

    unlocked = WeaponByteField("unlocked")

    def __init__(self, base: int, pine: Pine) -> None:
        self.base = base
        self.pine = pine

    def __repr__(self) -> str:
        return f"GadgetAddresses(base=0x{self.base:08X}, unlocked={self.unlocked})"


WEAPON_ORDER: list[str | None] = [
    Rac5WeaponKeys.LACERATOR,
    Rac5WeaponKeys.CONCUSSION_GUN,
    Rac5WeaponKeys.ACID_BOMB_GLOVE,
    Rac5WeaponKeys.AGENTS_OF_DOOM,
    Rac5WeaponKeys.BEE_MINE_GLOVE,
    Rac5WeaponKeys.STATIC_BARRIER,
    Rac5WeaponKeys.SHOCK_ROCKET,
    Rac5WeaponKeys.SNIPER_MINE,
    Rac5WeaponKeys.SCORCHER,
    Rac5WeaponKeys.LASER_TRACER,
    Rac5WeaponKeys.SUCK_CANNON,
    Rac5WeaponKeys.MOOTATOR,
    None,
    Rac5WeaponKeys.RYNO,
]

GADGET_ORDER: list[str | None] = [
    Rac5GadgetKeys.HYPERSHOT,
    Rac5GadgetKeys.SPROUT_O_MATIC,
    Rac5GadgetKeys.POLARIZER,
    Rac5GadgetKeys.PDA,
    Rac5GadgetKeys.SHRINK_RAY,
    Rac5GadgetKeys.BOLT_GRABBER,
    None,
    Rac5GadgetKeys.MAP_O_MATIC,
    Rac5GadgetKeys.BOX_BREAKER,
]


def build_weapons(array_base: int | None, pine: Pine) -> tuple[dict[str, WeaponAddresses], dict[str, GadgetAddresses]]:
    if array_base is None:
        return {}, {}

    weapons: dict[str, WeaponAddresses] = {}
    for i, name in enumerate(WEAPON_ORDER):
        if name is not None:
            weapons[name] = WeaponAddresses(array_base + i * WEAPON_STRUCT_SIZE, pine)

    gadget_base = array_base + len(WEAPON_ORDER) * WEAPON_STRUCT_SIZE
    gadgets: dict[str, GadgetAddresses] = {}
    for i, name in enumerate(GADGET_ORDER):
        if name is not None:
            gadgets[name] = GadgetAddresses(gadget_base + i * WEAPON_STRUCT_SIZE, pine)

    return weapons, gadgets


_MOD_SLOTS = ("mod_slot_one", "mod_slot_two", "mod_slot_three")


class WeaponInventory:
    """Pine-backed live accessor + ownership/vendor tracking for weapons, gadgets and
    mods. Planet-dependent: call set_base(array_base) whenever the loaded planet changes."""

    weapons = InventoryField("owned", gadget=False)
    ap_weapons = InventoryField("ap_owned", gadget=False)
    ap_gadgets = InventoryField("ap_owned", gadget=True)
    gadgets = InventoryField("owned", gadget=True)
    mods = InventoryField("mods", gadget=False)
    _raw_weapons = InventoryField("raw_owned", gadget=False)
    _raw_gadgets = InventoryField("raw_owned", gadget=True)
    _raw_mods = InventoryField("raw_mods", gadget=False)
    _raw_level = InventoryField("raw_level", gadget=False)
    _prev_experience = InventoryField("previous_experience", gadget=False)
    _pinned_experience = InventoryField("pinned_experience", gadget=False)
    level_caps = InventoryField("level_cap", gadget=False)
    titan_purchased = InventoryField("titan_purchased", gadget=False)
    _weapon_addrs = InventoryField("address", gadget=False)
    _gadget_addrs = InventoryField("address", gadget=True)

    def __init__(self, pine: Pine) -> None:
        self.entries = {
            name: InventoryEntry(name, name in GADGET_DATA)
            for name in (*WEAPON_ORDER, *GADGET_ORDER)
            if name is not None
        }
        self.pine = pine
        self.weapons: dict[str, bool] = {}
        self.gadgets: dict[str, bool] = {}
        self.mods: dict[str, dict[str, bool]] = {}
        self._raw_weapons: dict[str, bool] = {}
        self._raw_gadgets: dict[str, bool] = {}
        self._raw_mods: dict[str, dict[str, bool]] = {}
        self._raw_level: dict[str, int] = {}
        self.vendor_locations: dict[str, bool] = dict.fromkeys(
            (
                *_weapon_locations.VENDOR_WEAPON_LOC,
                *_weapon_locations.VENDOR_GADGET_LOC,
                *_weapon_locations._MOD_LOC,
            ),
            False,
        )
        self._weapon_addrs: dict[str, WeaponAddresses] = {}
        self._gadget_addrs: dict[str, GadgetAddresses] = {}

        self.experience_multiplier: int = 1
        self._prev_experience: dict[str, int] = {}

        self.progressive_mode: int = PROGRESSIVE_OFF
        self.level_caps: dict[str, int] = {}
        self._pinned_experience: dict[str, int] = {}

        self.challenge_mode: int = 0
        self.titan_purchased: dict[str, bool] = dict.fromkeys(TITAN_ELIGIBLE_WEAPONS, False)

    @contextmanager
    def memory(self):
        addresses = (*self._weapon_addrs.values(), *self._gadget_addrs.values())
        if not addresses or not all(isinstance(address, InventoryMemory) for address in addresses):
            yield
            return
        if addresses[0].window is not None:
            yield
            return
        base = min(address.base for address in addresses)
        end = max(address.base for address in addresses) + WEAPON_STRUCT_SIZE
        window = MemoryWindow.read_bytes(self.pine, base, end - base)
        for address in addresses:
            address.window = window
        try:
            yield
            window.flush(self.pine)
        finally:
            for address in addresses:
                address.window = None

    @batched_inventory
    def update_progression(self, vendor_active=False):
        self.apply_experience_boost()
        if not vendor_active:
            self.apply_progressive_leveling()
            if self.progressive_mode == PROGRESSIVE_MANUAL:
                for name, addr in self._weapon_addrs.items():
                    # Consume a full XP bar here before exposing boosted XP to
                    # the game. Otherwise it can process several level-ups
                    # between polls, bypassing the received-item cap.
                    threshold = exp_threshold_for_level(name, addr.level + 2)
                    if (self._level_cap(name) > addr.level and threshold is not None
                            and addr.experience >= threshold):
                        addr.level += 1
                        addr.experience = 0
                    # Baseline the XP actually written, not the pre-cap boost.
                    self._prev_experience[name] = addr.experience

    def set_base(self, array_base: int | None) -> None:
        """Rebind every weapon/gadget address to the planet's array base, or unbind
        entirely (check()/sync() become no-ops) when array_base is None."""
        self._weapon_addrs, self._gadget_addrs = build_weapons(array_base, self.pine)

    def get(self, name: str) -> bool:
        addr = self._weapon_addrs.get(name) or self._gadget_addrs.get(name)
        if addr is None:
            return False
        return bool(addr.unlocked)

    def set(self, name: str, value: bool) -> None:
        addr = self._weapon_addrs.get(name) or self._gadget_addrs.get(name)
        if addr is not None:
            addr.unlocked = value

    def delete(self, name: str) -> None:
        self.set(name, False)

    def get_mod(self, weapon: str, slot: str) -> bool:
        addr = self._weapon_addrs.get(weapon)
        if addr is None:
            return False
        return bool(getattr(addr, slot))

    def set_mod(self, weapon: str, slot: str, value: bool) -> None:
        addr = self._weapon_addrs.get(weapon)
        if addr is not None:
            setattr(addr, slot, value)

    def delete_mod(self, weapon: str, slot: str) -> None:
        self.set_mod(weapon, slot, False)

    def get_experience(self, weapon: str) -> int:
        addr = self._weapon_addrs.get(weapon)
        if addr is None:
            return 0
        return addr.experience

    def set_experience(self, weapon: str, value: int) -> None:
        addr = self._weapon_addrs.get(weapon)
        if addr is not None:
            addr.experience = value

    def get_ammo(self, weapon: str) -> int:
        addr = self._weapon_addrs.get(weapon)
        if addr is None:
            return 0
        return addr.ammo

    def set_ammo(self, weapon: str, value: int) -> None:
        """Write a weapon's ammo directly, for AmmoLink to mirror a shared value in;
        doesn't distinguish that from organic gain/spend, unlike set_level()/experience."""
        addr = self._weapon_addrs.get(weapon)
        if addr is not None:
            addr.ammo = value

    def get_level(self, weapon: str) -> int:
        addr = self._weapon_addrs.get(weapon)
        if addr is None:
            return 0
        return addr.level

    def set_level(self, weapon: str, level: int) -> None:
        """Write a weapon's level directly (a synthetic write, not an organic level-up).
        Also rebaselines _raw_level so check() doesn't fire spurious level checks."""
        addr = self._weapon_addrs.get(weapon)
        if addr is not None:
            addr.level = level
        self._raw_level[weapon] = level

    @batched_inventory
    def zero_levels_for_vendor(self, purchasable: frozenset[str] | None = None) -> dict[str, int]:
        """Snapshot every weapon's level, then zero out the ones in `purchasable` so the vendor's level-derived price doesn't leak a leveled-but-unowned weapon's real price; caller must pass the snapshot to restore_levels() once the vendor closes."""
        snapshot = {name: addr.level for name, addr in self._weapon_addrs.items()}
        for name, addr in self._weapon_addrs.items():
            if purchasable is None or name in purchasable:
                addr.level = 0
                self._raw_level[name] = 0
        return snapshot

    @batched_inventory
    def restore_levels(self, snapshot: dict[str, int]) -> None:
        """Write back a snapshot taken by zero_levels_for_vendor(), also rebaselining
        _raw_level so check() doesn't misread the restore as a fresh level-up."""
        for name, level in snapshot.items():
            addr = self._weapon_addrs.get(name)
            if addr is not None:
                addr.level = level
            self._raw_level[name] = level

    def snapshot_ammo(self, names: frozenset[str] | None = None) -> dict[str, int]:
        """Read live ammo for `names` (or every weapon) — the counterpart to
        restore_ammo(), for VendorInventory's display override."""
        if names is None:
            return {name: addr.ammo for name, addr in self._weapon_addrs.items()}
        return {name: addr.ammo for name, addr in self._weapon_addrs.items() if name in names}

    def restore_ammo(self, snapshot: dict[str, int]) -> None:
        """Write back a snapshot taken by snapshot_ammo()."""
        for name, ammo in snapshot.items():
            addr = self._weapon_addrs.get(name)
            if addr is not None:
                addr.ammo = ammo

    def get_mod_unlock(self, weapon: str, attr: str) -> bool:
        addr = self._weapon_addrs.get(weapon)
        if addr is None:
            return False
        return bool(getattr(addr, attr))

    def set_mod_unlock(self, weapon: str, attr: str, value: bool) -> None:
        """Write the mod_unlock_N "purchasable" byte — separate from set_mod (ownership),
        this just controls whether the mod vendor shows that slot as buyable."""
        addr = self._weapon_addrs.get(weapon)
        if addr is not None:
            setattr(addr, attr, value)

    @batched_inventory
    def check(self) -> dict[str, list]:
        """Batch-read every weapon/gadget/mod byte, update ownership state, and return what newly changed since the raw memory's last reading (not weapons/gadgets/mods, which never regress, so a repurchase of an already-owned item wouldn't show)."""
        newly_weapons: list[str] = []
        newly_gadgets: list[str] = []
        newly_mods: list[tuple[str, str]] = []
        newly_levels: list[tuple[str, int]] = []
        newly_titans: list[str] = []

        weapon_names = list(self._weapon_addrs)
        gadget_names = list(self._gadget_addrs)

        for name in weapon_names:
            was_unlocked = self._raw_weapons.get(name, False)
            is_unlocked = bool(self._weapon_addrs[name].unlocked)
            self._raw_weapons[name] = is_unlocked
            if is_unlocked:
                self.weapons[name] = True
            if is_unlocked and not was_unlocked:
                newly_weapons.append(name)

            prev_mods = dict(self._raw_mods.get(name, dict.fromkeys(_MOD_SLOTS, False)))
            raw_mods = self._raw_mods.setdefault(name, dict.fromkeys(_MOD_SLOTS, False))
            mods = self.mods.setdefault(name, dict.fromkeys(_MOD_SLOTS, False))
            for slot in _MOD_SLOTS:
                slot_unlocked = bool(getattr(self._weapon_addrs[name], slot))
                raw_mods[slot] = slot_unlocked
                if slot_unlocked:
                    mods[slot] = True
                if slot_unlocked and not prev_mods.get(slot, False):
                    newly_mods.append((name, slot))

            if is_unlocked:
                prev_level = self._raw_level.get(name, -1)
                current_level = self._weapon_addrs[name].level
                if current_level > prev_level:
                    for idx in range(prev_level + 1, current_level + 1):
                        level = idx + 1
                        if level >= 2:
                            newly_levels.append((name, level))
                        if level == 5 and name in TITAN_ELIGIBLE_WEAPONS:
                            newly_titans.append(name)
                self._raw_level[name] = current_level

        for name in gadget_names:
            was_unlocked = self._raw_gadgets.get(name, False)
            is_unlocked = bool(self._gadget_addrs[name].unlocked)
            self._raw_gadgets[name] = is_unlocked
            if is_unlocked:
                self.gadgets[name] = True
            if is_unlocked and not was_unlocked:
                newly_gadgets.append(name)

        return {
            "weapons": newly_weapons,
            "gadgets": newly_gadgets,
            "mods": newly_mods,
            "levels": newly_levels,
            "titans": newly_titans,
        }

    @batched_inventory
    def apply_experience_boost(self) -> None:
        """Inflate each weapon's experience gain by experience_multiplier every tick."""
        multiplier = self.experience_multiplier
        for name, addr in self._weapon_addrs.items():
            current = addr.experience
            previous = self._prev_experience.get(name)
            if previous is None:
                self._prev_experience[name] = current
                continue
            diff = current - previous
            if diff <= 0:
                self._prev_experience[name] = current
                continue
            max_level_idx = WEAPON_MAX_LEVELS.get(name, 4) - 1
            if multiplier > 1 and addr.level < max_level_idx:
                boosted = previous + diff * multiplier
                addr.experience = boosted
                self._prev_experience[name] = boosted
            else:
                self._prev_experience[name] = current

    def _level_cap(self, name: str) -> int:
        """Progressive Weapon level cap for `name`, held at V4 for a Titan-eligible weapon until
        Challenge Mode 1 is reached, since V5+ is Challenge Mode content even with enough copies."""
        cap = self.level_caps.get(name, -1)
        if self.challenge_mode < 1 and name in TITAN_ELIGIBLE_WEAPONS:
            return min(cap, 3)
        return cap

    def level_ceiling(self, name: str) -> int | None:
        """Highest level apply_progressive_leveling() currently lets `name` keep, or None if it never lowers it."""
        if self.progressive_mode == PROGRESSIVE_OFF:
            return None
        cap = self._level_cap(name)
        if self.progressive_mode == PROGRESSIVE_AUTOMATIC:
            return max(cap, 0)
        return None if cap < 0 else cap

    def within_level_ceilings(self, levels: dict[str, int]) -> dict[str, int]:
        """`levels` with each weapon lowered to its level_ceiling(), so a guarded save/restore
        never fights the Progressive Weapon cap."""
        capped = {}
        for name, level in levels.items():
            ceiling = self.level_ceiling(name)
            capped[name] = level if ceiling is None else min(level, ceiling)
        return capped

    @batched_inventory
    def apply_progressive_leveling(self) -> None:
        """Gate weapon leveling behind Progressive Weapon items, and step V4 weapons up to V5
        once Challenge Mode allows it, every tick. Buying a Titan never changes a level itself."""
        mode = self.progressive_mode
        if mode == PROGRESSIVE_OFF and self.challenge_mode < 1:
            return

        for name, addr in self._weapon_addrs.items():
            if mode == PROGRESSIVE_OFF:
                # V5 has no experience threshold, so an owned V4 weapon steps straight up once
                # Challenge Mode is reached, even if it hit V4 before Progressive Challenge Mode
                # raised the tier.
                if name in TITAN_ELIGIBLE_WEAPONS and addr.level == 3 and addr.unlocked:
                    addr.level = 4
                    addr.experience = 0
                continue

            cap = self._level_cap(name)

            if mode == PROGRESSIVE_AUTOMATIC:
                addr.level = max(cap, 0)
                addr.experience = 0
                continue

            if cap < 0:
                pinned = self._pinned_experience.get(name)
                if pinned is None:
                    self._pinned_experience[name] = addr.experience
                else:
                    addr.experience = pinned
                continue
            self._pinned_experience.pop(name, None)

            if addr.level > cap:
                addr.level = cap

            max_level_idx = WEAPON_MAX_LEVELS.get(name, cap + 1) - 1
            if cap >= max_level_idx:
                continue

            if addr.level == cap:
                if addr.experience != 0:
                    addr.experience = 0
                continue

            next_threshold = exp_threshold_for_level(name, addr.level + 2)
            if next_threshold is None:
                addr.level += 1
                addr.experience = 0
            else:
                ceiling = exp_threshold_for_level(name, cap + 1)
                if ceiling is not None and addr.experience > ceiling:
                    addr.experience = ceiling

    @batched_inventory
    def wipe(self, *, preserve_levels: bool = False) -> None:
        """Reset ownership, retaining game-restored levels when returning from a race."""
        for addr in self._weapon_addrs.values():
            addr.unlocked = False
            for slot in _MOD_SLOTS:
                setattr(addr, slot, False)
            if not preserve_levels:
                addr.level = 0
        for addr in self._gadget_addrs.values():
            addr.unlocked = False

        self.weapons = dict.fromkeys(self._weapon_addrs, False)
        self.gadgets = dict.fromkeys(self._gadget_addrs, False)
        self.mods = {name: dict.fromkeys(_MOD_SLOTS, False) for name in self._weapon_addrs}
        self._raw_weapons = dict(self.weapons)
        self._raw_gadgets = dict(self.gadgets)
        self._raw_mods = {name: dict(mods) for name, mods in self.mods.items()}
        self._raw_level = {name: addr.level for name, addr in self._weapon_addrs.items()}
        self._prev_experience = {name: addr.experience for name, addr in self._weapon_addrs.items()}

    @batched_inventory
    def sync(self) -> None:
        """Write the current ownership dicts into game memory for the current planet's array."""
        for name, addr in self._weapon_addrs.items():
            addr.unlocked = self.weapons.get(name, False)
            mods = self.mods.get(name, {})
            for slot in _MOD_SLOTS:
                setattr(addr, slot, mods.get(slot, False))
        for name, addr in self._gadget_addrs.items():
            addr.unlocked = self.gadgets.get(name, False)

    @batched_inventory
    def sync_slots(self) -> None:
        """Read the current planet's array into the ownership dicts (no change report).
        Also re-baselines check()'s raw-memory dicts so it doesn't see this resync as a change."""
        for name, addr in self._weapon_addrs.items():
            unlocked = bool(addr.unlocked)
            self.weapons[name] = unlocked
            self._raw_weapons[name] = unlocked
            mods = self.mods.setdefault(name, dict.fromkeys(_MOD_SLOTS, False))
            raw_mods = self._raw_mods.setdefault(name, dict.fromkeys(_MOD_SLOTS, False))
            for slot in _MOD_SLOTS:
                slot_unlocked = bool(getattr(addr, slot))
                mods[slot] = slot_unlocked
                raw_mods[slot] = slot_unlocked
            self._prev_experience[name] = addr.experience
        for name, addr in self._gadget_addrs.items():
            unlocked = bool(addr.unlocked)
            self.gadgets[name] = unlocked
            self._raw_gadgets[name] = unlocked

    @batched_inventory
    def apply_vendor_locations(self, allowed_extra: frozenset[str] = frozenset()) -> None:
        """Zero all weapon/gadget/mod memory then restore what the player may keep:
        purchased-and-owned or in allowed_extra for weapons/gadgets; purchased-only for mods."""
        weapon_unlocked = dict.fromkeys(self._weapon_addrs, False)
        weapon_mods: dict[str, dict[str, bool]] = {
            name: dict.fromkeys(_MOD_SLOTS, False) for name in self._weapon_addrs
        }
        gadget_unlocked = dict.fromkeys(self._gadget_addrs, False)

        for loc_name, purchased in self.vendor_locations.items():
            if not purchased:
                continue
            if loc_name in _weapon_locations.VENDOR_WEAPON_LOC:
                name = _weapon_locations.VENDOR_WEAPON_LOC[loc_name]
                if self.weapons.get(name, False) and name in weapon_unlocked:
                    weapon_unlocked[name] = True
            elif loc_name in _weapon_locations.VENDOR_GADGET_LOC:
                name = _weapon_locations.VENDOR_GADGET_LOC[loc_name]
                if self.gadgets.get(name, False) and name in gadget_unlocked:
                    gadget_unlocked[name] = True
            elif loc_name in _weapon_locations._MOD_LOC:
                weapon, slot = _weapon_locations._MOD_LOC[loc_name]
                if weapon in weapon_mods:
                    weapon_mods[weapon][slot] = True

        for name in allowed_extra:
            if name in weapon_unlocked:
                weapon_unlocked[name] = True
            if name in gadget_unlocked:
                gadget_unlocked[name] = True

        for name, addr in self._weapon_addrs.items():
            addr.unlocked = weapon_unlocked[name]
            for slot in _MOD_SLOTS:
                setattr(addr, slot, weapon_mods[name][slot])
        for name, addr in self._gadget_addrs.items():
            addr.unlocked = gadget_unlocked[name]

    @batched_inventory
    def zero_unpurchased_mod_slots(self, names: frozenset[str]) -> None:
        """Re-zero mod_slot_N unless bought from this vendor, since a Progressive-item
        grant can race back in after apply_vendor_locations()'s own zero/restore pass."""
        purchased_slots = {
            _weapon_locations._MOD_LOC[loc]
            for loc, bought in self.vendor_locations.items()
            if bought and loc in _weapon_locations._MOD_LOC
        }
        for name in names:
            addr = self._weapon_addrs.get(name)
            if addr is None:
                continue
            for slot in _MOD_SLOTS:
                if (name, slot) in purchased_slots:
                    continue
                if getattr(addr, slot):
                    setattr(addr, slot, False)

    def sync_from_ap(self, checked_locations: set[str]) -> None:
        for loc in checked_locations:
            if loc in self.vendor_locations:
                self.vendor_locations[loc] = True
            if loc in _weapon_locations.VENDOR_WEAPON_LOC:
                self.weapons[_weapon_locations.VENDOR_WEAPON_LOC[loc]] = True
            elif loc in _weapon_locations.VENDOR_GADGET_LOC:
                self.gadgets[_weapon_locations.VENDOR_GADGET_LOC[loc]] = True
            elif loc in _weapon_locations._MOD_LOC:
                weapon, slot = _weapon_locations._MOD_LOC[loc]
                self.mods.setdefault(weapon, dict.fromkeys(_MOD_SLOTS, False))
                self.mods[weapon][slot] = True
            elif loc in _weapon_locations._TITAN_LOC:
                self.titan_purchased[_weapon_locations._TITAN_LOC[loc]] = True

    @batched_inventory
    def level_snapshot(self) -> dict[str, int]:
        """Levels only; experience remains managed by the game."""
        return {name: addr.level for name, addr in self._weapon_addrs.items()}

    @batched_inventory
    def revert_unowned(self, is_ap_owned: Callable[[str], bool]) -> None:
        """Zero unlocked + every mod slot for every weapon is_ap_owned says no to."""
        for weapon, addr in self._weapon_addrs.items():
            if is_ap_owned(weapon):
                continue
            addr.unlocked = False
            self.weapons[weapon] = False
            mods = self.mods.setdefault(weapon, dict.fromkeys(_MOD_SLOTS, False))
            for slot in _MOD_SLOTS:
                setattr(addr, slot, False)
                mods[slot] = False

    def has_weapon(self, name: str) -> bool:
        return self.weapons.get(name, False)

    def has_gadget(self, name: str) -> bool:
        return self.gadgets.get(name, False)

    def has_mod(self, weapon: str, slot: str) -> bool:
        return self.mods.get(weapon, {}).get(slot, False)

    def __repr__(self) -> str:
        unlocked_w = [n for n, v in self.weapons.items() if v]
        unlocked_g = [n for n, v in self.gadgets.items() if v]
        return f"WeaponInventory(weapons={unlocked_w}, gadgets={unlocked_g})"
