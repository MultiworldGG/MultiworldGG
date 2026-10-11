from typing import TYPE_CHECKING

from rule_builder.rules import And, Has, HasAll, HasAny, HasAnyCount, Or, True_

from ..constants import Rac5Gadgets, Rac5Infobots
from ..data.weapons import WEAPON_DATA
from ..items import (
    ARMOUR_SETS,
    CLANK_PACK_NAME,
    PROGRESSIVE_ARMOUR_NAME,
    PROGRESSIVE_ARMOUR_UNIFIED_NAME,
    PROGRESSIVE_CHALLENGE_MODE_NAME,
    PROGRESSIVE_WEAPON_NAME,
    WEAPON_DISPLAY_TO_INTERNAL,
)
if TYPE_CHECKING:
    from ..world import RACSizeMatterWorld
_PROJECTILE_WEAPONS = [
    display for display, internal in WEAPON_DISPLAY_TO_INTERNAL.items() if WEAPON_DATA[internal].is_projectile
]
_LONG_PROJECTILE_WEAPONS = [
    display for display, internal in WEAPON_DISPLAY_TO_INTERNAL.items() if WEAPON_DATA[internal].is_long_projectile
]
_PROJECTILE_WEAPONS_ALL_NAMES = [*_PROJECTILE_WEAPONS, *(PROGRESSIVE_WEAPON_NAME[name] for name in _PROJECTILE_WEAPONS)]
_LONG_PROJECTILE_WEAPONS_ALL_NAMES = [*_LONG_PROJECTILE_WEAPONS, *(PROGRESSIVE_WEAPON_NAME[name] for name in _LONG_PROJECTILE_WEAPONS)]
PROJECTILE_WEAPON_ITEM_NAMES = frozenset(_PROJECTILE_WEAPONS_ALL_NAMES)
_ARMOUR_PIECE_INDEX: dict[str, int] = {"Chestplate": 1, "Helmet": 2, "Gloves": 3, "Boots": 4}
_ARMOUR_SET_ORDER_INDEX: dict[str, int] = {display: i for i, (display, _internal) in enumerate(ARMOUR_SETS)}


def _unified_armour_count(set_display: str, piece_name: str) -> int:
    """Copies of PROGRESSIVE_ARMOUR_UNIFIED_NAME needed to have granted `piece_name` of `set_display`: every piece of every earlier set in ARMOUR_SETS order, plus this piece's own 1-indexed position within its set."""
    return _ARMOUR_SET_ORDER_INDEX[set_display] * 4 + _ARMOUR_PIECE_INDEX[piece_name]


def HasProjectileWeapon() -> HasAny:
    return HasAny(*_PROJECTILE_WEAPONS_ALL_NAMES)

def HasLongProjectileWeapon() -> HasAny:
    return HasAny(*_LONG_PROJECTILE_WEAPONS_ALL_NAMES)


def HasArmourPiece(set_display: str, piece_name: str) -> HasAnyCount:
    return HasAnyCount(
        {
            f"{set_display} {piece_name}": 1,
            PROGRESSIVE_ARMOUR_NAME[set_display]: _ARMOUR_PIECE_INDEX[piece_name],
            PROGRESSIVE_ARMOUR_UNIFIED_NAME: _unified_armour_count(set_display, piece_name),
        }
    )


def HasTitanPrereq(world: "RACSizeMatterWorld", weapon: str) -> HasAny | Has:
    """Weapon Titan variant purchase prerequisite: reaching level 4 is what unlocks the purchase in-game (see core/vendor.py's Titan-purchase handling, which floors the weapon to level 5 the moment it's bought)."""
    if world.options.progressive_weapons:
        return Has(PROGRESSIVE_WEAPON_NAME[weapon], 4)
    return HasAny(weapon, PROGRESSIVE_WEAPON_NAME[weapon])


def HasArmourSet(set_display: str) -> And:
    return And(*(HasArmourPiece(set_display, piece) for piece in _ARMOUR_PIECE_INDEX))


def weapon_enabled(world: "RACSizeMatterWorld", weapon: str) -> bool:
    """EnabledWeapons option (options.py): whether `weapon` (display name) is still in the pool at all."""
    return weapon in world.options.enabled_weapons.value


def HasChallengeMode(world: "RACSizeMatterWorld", tier: int) -> Has | True_:
    """Challenge Mode tier gate for content options.py's ChallengeMode option makes exist at all (RYNO, Titan variants, Challenge-Mode-only mods, Hyperborean/Chameleon pickups)."""
    if not world.options.progressive_challenge_mode:
        return True_()
    return Has(PROGRESSIVE_CHALLENGE_MODE_NAME, tier)


def HasClankPack(world: "RACSizeMatterWorld") -> Has | True_:
    """Clank Pack gate for checks that need the backpack; free when the ClankPack option leaves it vanilla."""
    if not world.options.clank_pack:
        return True_()
    return Has(CLANK_PACK_NAME)


def HasGoodExpPlanet() -> Or:
    return Or(
        HasAll(Rac5Infobots.QUODRONA, Rac5Gadgets.SHRINK_RAY),
        HasAll(Rac5Infobots.DAYNI_MOON, Rac5Gadgets.SPROUT_O_MATIC),
        HasAll(Rac5Infobots.CHALLAX, Rac5Gadgets.POLARIZER, Rac5Gadgets.SHRINK_RAY),
        HasAll(Rac5Infobots.OUTPOST_OMEGA, Rac5Gadgets.HYPERSHOT, Rac5Gadgets.SPROUT_O_MATIC),
    )

def HasExpAccess() -> Or:
    return Or(
        HasAll(Rac5Infobots.QUODRONA, Rac5Gadgets.SHRINK_RAY),
        HasAll(Rac5Infobots.DAYNI_MOON),
        HasAll(Rac5Infobots.CHALLAX, Rac5Gadgets.POLARIZER, Rac5Gadgets.SHRINK_RAY),
        HasAll(Rac5Infobots.METALIS, Rac5Gadgets.POLARIZER),
        HasAll(Rac5Infobots.KALIDON, Rac5Gadgets.HYPERSHOT),
        HasAny(Rac5Infobots.POKITARU,Rac5Infobots.RYLLUS, Rac5Infobots.OUTPOST_OMEGA),
    )
