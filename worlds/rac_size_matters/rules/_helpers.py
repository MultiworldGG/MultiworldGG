from dataclasses import dataclass

from rule_builder.rules import (
    And,
    CanReachLocation,
    Has,
    HasAll,
    HasAny,
    HasAnyCount,
    HasGroup,
    Or,
    Rule,
    True_,
    TWorld,
)
from typing_extensions import override

from ..constants import Rac5Gadgets, Rac5Infobots
from ..items import (
    ARMOUR_SETS,
    CLANK_PACK_NAME,
    LONG_PROJECTILE_WEAPONS_GROUP,
    PROGRESSIVE_ARMOUR_NAME,
    PROGRESSIVE_ARMOUR_UNIFIED_NAME,
    PROGRESSIVE_CHALLENGE_MODE_NAME,
    PROGRESSIVE_WEAPON_NAME,
    PROJECTILE_WEAPONS_GROUP,
)

_ARMOUR_PIECE_INDEX: dict[str, int] = {"Chestplate": 1, "Helmet": 2, "Gloves": 3, "Boots": 4}
_ARMOUR_SET_ORDER_INDEX: dict[str, int] = {display: i for i, (display, _internal) in enumerate(ARMOUR_SETS)}


def _unified_armour_count(set_display: str, piece_name: str) -> int:
    """Copies of PROGRESSIVE_ARMOUR_UNIFIED_NAME needed to have granted `piece_name` of `set_display`: every piece of every earlier set in ARMOUR_SETS order, plus this piece's own 1-indexed position within its set."""
    return _ARMOUR_SET_ORDER_INDEX[set_display] * 4 + _ARMOUR_PIECE_INDEX[piece_name]


@dataclass
class HasProjectileWeapon(Rule[TWorld], game="Ratchet & Clank: Size Matters"):
    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        return HasGroup(PROJECTILE_WEAPONS_GROUP).resolve(world)


@dataclass
class HasLongProjectileWeapon(Rule[TWorld], game="Ratchet & Clank: Size Matters"):
    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        return HasGroup(LONG_PROJECTILE_WEAPONS_GROUP).resolve(world)


@dataclass
class HasArmourPiece(Rule[TWorld], game="Ratchet & Clank: Size Matters"):
    set_display: str
    piece_name: str

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        return HasAnyCount(
            {
                f"{self.set_display} {self.piece_name}": 1,
                PROGRESSIVE_ARMOUR_NAME[self.set_display]: _ARMOUR_PIECE_INDEX[self.piece_name],
                PROGRESSIVE_ARMOUR_UNIFIED_NAME: _unified_armour_count(self.set_display, self.piece_name),
            }
        ).resolve(world)


@dataclass
class HasWeaponLevel(Rule[TWorld], game="Ratchet & Clank: Size Matters"):
    """Weapon at `level` or higher. Without progressive weapons, levelling isn't an item, so owning it is enough."""

    weapon: str
    level: int

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        rule = HasAny(self.weapon, PROGRESSIVE_WEAPON_NAME[self.weapon])
        if world.options.progressive_weapons:
            rule = Has(PROGRESSIVE_WEAPON_NAME[self.weapon], self.level)
        return rule.resolve(world)


@dataclass
class HasChallengeMode(Rule[TWorld], game="Ratchet & Clank: Size Matters"):
    """Challenge Mode tier gate for content options.py's ChallengeMode option makes exist at all (RYNO, Titan variants, Challenge-Mode-only mods, Hyperborean/Chameleon pickups)."""

    tier: int

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        rule = True_()
        if world.options.progressive_challenge_mode:
            rule = Has(PROGRESSIVE_CHALLENGE_MODE_NAME, self.tier)
        return rule.resolve(world)


@dataclass
class HasClankPack(Rule[TWorld], game="Ratchet & Clank: Size Matters"):
    """Clank Pack gate for checks that need the backpack; free when the ClankPack option leaves it vanilla."""

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        rule = True_()
        if world.options.clank_pack:
            rule = Has(CLANK_PACK_NAME)
        return rule.resolve(world)


@dataclass
class HasGoodExpPlanet(Rule[TWorld], game="Ratchet & Clank: Size Matters"):
    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        return Or(
            HasAll(Rac5Infobots.QUODRONA, Rac5Gadgets.SHRINK_RAY),
            HasAll(Rac5Infobots.DAYNI_MOON, Rac5Gadgets.SPROUT_O_MATIC),
            HasAll(Rac5Infobots.CHALLAX, Rac5Gadgets.POLARIZER, Rac5Gadgets.SHRINK_RAY),
            HasAll(Rac5Infobots.OUTPOST_OMEGA, Rac5Gadgets.HYPERSHOT, Rac5Gadgets.SPROUT_O_MATIC),
        ).resolve(world)


@dataclass
class HasExpAccess(Rule[TWorld], game="Ratchet & Clank: Size Matters"):
    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        return Or(
            HasAll(Rac5Infobots.QUODRONA, Rac5Gadgets.SHRINK_RAY),
            Has(Rac5Infobots.DAYNI_MOON),
            HasAll(Rac5Infobots.CHALLAX, Rac5Gadgets.POLARIZER, Rac5Gadgets.SHRINK_RAY),
            HasAll(Rac5Infobots.METALIS, Rac5Gadgets.POLARIZER),
            HasAll(Rac5Infobots.KALIDON, Rac5Gadgets.HYPERSHOT),
            HasAny(Rac5Infobots.POKITARU, Rac5Infobots.RYLLUS, Rac5Infobots.OUTPOST_OMEGA),
        ).resolve(world)


@dataclass
class CanReachAllSkillPoints(Rule[TWorld], game="Ratchet & Clank: Size Matters"):
    """Every skill point location the SkillPoints/Clank/Skyboard Challenge options put in this seed."""

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        from ..locations.shared import required_skill_points

        return And(*(CanReachLocation(name) for name in required_skill_points(world.options))).resolve(world)


@dataclass
class CanReachAllClankChallenges(Rule[TWorld], game="Ratchet & Clank: Size Matters"):
    """Every Clank Challenge location the ClankChallenges/ClankChallengeGroups options put in this seed."""

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        from ..locations.shared import required_clank_challenges

        return And(*(CanReachLocation(name) for name in required_clank_challenges(world.options))).resolve(world)
