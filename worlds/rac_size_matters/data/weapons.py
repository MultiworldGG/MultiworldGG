from collections.abc import Mapping
from dataclasses import dataclass

from BaseClasses import ItemClassification

from ..constants import Rac5GadgetKeys, Rac5WeaponKeys


@dataclass(frozen=True, slots=True)
class VendorDisplayAmmo:
    base: int
    titan: int | None = None


@dataclass(frozen=True, slots=True)
class Weapon:
    name: str
    is_projectile: bool
    classification: ItemClassification
    max_level: int
    mod_count: int
    exp_thresholds: tuple[int | None, ...]
    vendor_ammo: VendorDisplayAmmo
    is_long_projectile: bool = False


@dataclass(frozen=True, slots=True)
class Gadget:
    name: str
    classification: ItemClassification


class AttributeView(Mapping):
    def __init__(self, records, attribute=None):
        self.records, self.attribute = records, attribute

    def __iter__(self):
        return (record.name for record in self.records)

    def __len__(self):
        return len(self.records)

    def __getitem__(self, name):
        for record in self.records:
            if record.name == name:
                return record if self.attribute is None else getattr(record, self.attribute)
        raise KeyError(name)


WEAPONS = (
    Weapon(
        Rac5WeaponKeys.LACERATOR,
        is_projectile=True,
        is_long_projectile=True,
        classification=ItemClassification.progression,
        max_level=8,
        mod_count=2,
        exp_thresholds=(3000, 9000, 15000, None, 27000, 55000, 205000, None),
        vendor_ammo=VendorDisplayAmmo(base=60, titan=120),
    ),
    Weapon(
        Rac5WeaponKeys.CONCUSSION_GUN,
        is_projectile=True,
        classification=ItemClassification.progression,
        max_level=8,
        mod_count=3,
        exp_thresholds=(6000, 9000, 12000, None, 50000, 78000, 158000, None),
        vendor_ammo=VendorDisplayAmmo(base=25, titan=30),
    ),
    Weapon(
        Rac5WeaponKeys.ACID_BOMB_GLOVE,
        is_projectile=False,
        classification=ItemClassification.progression,
        max_level=8,
        mod_count=2,
        exp_thresholds=(3000, 6000, 9000, None, 27000, 55000, 55000, None),
        vendor_ammo=VendorDisplayAmmo(base=5, titan=10),
    ),
    Weapon(
        Rac5WeaponKeys.AGENTS_OF_DOOM,
        is_projectile=False,
        classification=ItemClassification.progression,
        max_level=8,
        mod_count=2,
        exp_thresholds=(6000, 9000, 12000, None, 27000, 100000, 250000, None),
        vendor_ammo=VendorDisplayAmmo(base=6, titan=10),
    ),
    Weapon(
        Rac5WeaponKeys.BEE_MINE_GLOVE,
        is_projectile=False,
        classification=ItemClassification.progression,
        max_level=8,
        mod_count=2,
        exp_thresholds=(6000, 7500, 9000, None, 50000, 142000, 225000, None),
        vendor_ammo=VendorDisplayAmmo(base=8, titan=8),
    ),
    Weapon(
        Rac5WeaponKeys.STATIC_BARRIER,
        is_projectile=False,
        classification=ItemClassification.useful,
        max_level=8,
        mod_count=2,
        exp_thresholds=(15000, 18000, 21000, None, 24000, 27000, 30000, None),
        vendor_ammo=VendorDisplayAmmo(base=5, titan=5),
    ),
    Weapon(
        Rac5WeaponKeys.SHOCK_ROCKET,
        is_projectile=True,
        is_long_projectile=True,
        classification=ItemClassification.progression,
        max_level=8,
        mod_count=3,
        exp_thresholds=(15000, 19000, 42000, None, 60000, 145000, 250000, None),
        vendor_ammo=VendorDisplayAmmo(base=20, titan=22),
    ),
    Weapon(
        Rac5WeaponKeys.SNIPER_MINE,
        is_projectile=True,
        is_long_projectile=True,
        classification=ItemClassification.progression,
        max_level=8,
        mod_count=2,
        exp_thresholds=(4000, 5500, 7000, None, 50000, 142000, 225000, None),
        vendor_ammo=VendorDisplayAmmo(base=8, titan=10),
    ),
    Weapon(
        Rac5WeaponKeys.SCORCHER,
        is_projectile=True,
        classification=ItemClassification.progression,
        max_level=8,
        mod_count=2,
        exp_thresholds=(7000, 8500, 10000, None, 27000, 55000, 205000, None),
        vendor_ammo=VendorDisplayAmmo(base=60, titan=90),
    ),
    Weapon(
        Rac5WeaponKeys.LASER_TRACER,
        is_projectile=True,
        is_long_projectile=True,
        classification=ItemClassification.progression,
        max_level=8,
        mod_count=2,
        exp_thresholds=(15000, 27000, 45000, None, 65000, 225000, 350000, None),
        vendor_ammo=VendorDisplayAmmo(base=200, titan=300),
    ),
    Weapon(
        Rac5WeaponKeys.SUCK_CANNON,
        is_projectile=False,
        classification=ItemClassification.useful,
        max_level=8,
        mod_count=1,
        exp_thresholds=(3500, 5000, 7000, None, 12500, 43000, 67500, None),
        vendor_ammo=VendorDisplayAmmo(base=8, titan=16),
    ),
    Weapon(
        Rac5WeaponKeys.MOOTATOR,
        is_projectile=False,
        classification=ItemClassification.progression,
        max_level=8,
        mod_count=0,
        exp_thresholds=(12000, 12000, 16000, None, 50000, 142000, 225000, None),
        vendor_ammo=VendorDisplayAmmo(base=0, titan=0),
    ),
    Weapon(
        Rac5WeaponKeys.RYNO,
        is_projectile=True,
        is_long_projectile=True,
        classification=ItemClassification.progression,
        max_level=4,
        mod_count=0,
        exp_thresholds=(85000, 350000, 999000, None),
        vendor_ammo=VendorDisplayAmmo(base=30),
    ),
)

GADGETS = (
    Gadget(Rac5GadgetKeys.HYPERSHOT, ItemClassification.progression),
    Gadget(Rac5GadgetKeys.SPROUT_O_MATIC, ItemClassification.progression),
    Gadget(Rac5GadgetKeys.POLARIZER, ItemClassification.progression),
    Gadget(Rac5GadgetKeys.PDA, ItemClassification.useful),
    Gadget(Rac5GadgetKeys.SHRINK_RAY, ItemClassification.progression),
    Gadget(Rac5GadgetKeys.BOLT_GRABBER, ItemClassification.useful),
    Gadget(Rac5GadgetKeys.MAP_O_MATIC, ItemClassification.useful),
    Gadget(Rac5GadgetKeys.BOX_BREAKER, ItemClassification.useful),
)

WEAPON_DATA = AttributeView(WEAPONS)
GADGET_DATA = AttributeView(GADGETS)
WEAPON_MAX_LEVELS = AttributeView(WEAPONS, "max_level")
WEAPON_MOD_COUNTS = AttributeView(WEAPONS, "mod_count")
WEAPON_EXP_THRESHOLDS = AttributeView(WEAPONS, "exp_thresholds")
WEAPON_VENDOR_DISPLAY_AMMO = AttributeView(WEAPONS, "vendor_ammo")
WeaponData = Weapon
GadgetData = Gadget
