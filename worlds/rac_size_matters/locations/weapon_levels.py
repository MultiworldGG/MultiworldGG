from rule_builder.options import OptionFilter
from rule_builder.rules import Rule

from ..constants import Rac5Weapons
from ..data.weapons import WEAPONS
from ..items import NG_PLUS_WEAPONS
from ..options import ChallengeMode, NgPlusItems, WeaponLevelChecks
from ..rules._helpers import HasChallengeMode, HasExpAccess, HasGoodExpPlanet, HasWeaponLevel
from .model import Completion, LocationOptions, Rac5Categories, Rac5CompletionSources, Rac5Locations

_C = Rac5Categories

FIRST_DEFINITION_ORDER = 156
# Level 4 is the max outside Challenge Mode; levels 5-8 need Challenge Mode (Titan variants).
NORMAL_MAX_LEVEL = 4

_NEEDS_GOOD_EXP_PLANET = frozenset((Rac5Weapons.RYNO, Rac5Weapons.LASER_TRACER, Rac5Weapons.STATIC_BARRIER))


def access_rule(weapon: str, level: int) -> Rule:
    rule = HasWeaponLevel(weapon, level) & HasExpAccess()
    if level >= 5:
        rule &= HasChallengeMode(1)
    if weapon in _NEEDS_GOOD_EXP_PLANET:
        rule &= HasGoodExpPlanet()
    return rule


def _weapon_level_checks_values(level: int) -> tuple[int, ...]:
    """WeaponLevelChecks values that include this level: max levels (4 and 8) have their own choices,
    every level in between only appears with `all`."""
    if level == NORMAL_MAX_LEVEL:
        return 1, 3, 4
    if level == 8:
        return 2, 3, 4
    return (4,)


def _categories(weapon: str, level: int) -> frozenset[str]:
    categories = {_C.WEAPON_LEVEL}
    if level <= NORMAL_MAX_LEVEL:
        categories.add(_C.WEAPON_MAX_LEVEL if level == NORMAL_MAX_LEVEL else _C.WEAPON_SUB_MAX_LEVEL)
    else:
        categories.add(_C.CHALLENGE_MODE_WEAPON_LEVEL)
        categories.add(_C.CHALLENGE_MODE_MAX_LEVEL if level == 8 else _C.CHALLENGE_MODE_SUB_MAX_LEVEL)
    if weapon in NG_PLUS_WEAPONS:
        categories.add(_C.NG_PLUS_WEAPON_LEVEL)
    return frozenset(categories)


def _requirements(weapon: str, level: int) -> tuple[OptionFilter, ...]:
    requirements = []
    if weapon in NG_PLUS_WEAPONS:
        requirements.append(OptionFilter(NgPlusItems, (1,), "in"))
    if level > NORMAL_MAX_LEVEL:
        requirements.append(OptionFilter(ChallengeMode, (1, 2), "in"))
    requirements.append(OptionFilter(WeaponLevelChecks, _weapon_level_checks_values(level), "in"))
    return tuple(requirements)


def _location(weapon: str, level: int, definition_order: int) -> Rac5Locations:
    return Rac5Locations(
        f"Weapon Level: {weapon} V{level}",
        "Menu",
        access_rule(weapon, level),
        Completion(Rac5CompletionSources.WEAPON_LEVELS, (weapon, level)),
        options=LocationOptions(requirements=_requirements(weapon, level), weapon=weapon),
        categories=_categories(weapon, level),
        weapon=weapon,
        level=level,
        definition_order=definition_order,
    )


LOCATIONS = tuple(
    _location(weapon, level, FIRST_DEFINITION_ORDER + index)
    for index, (weapon, level) in enumerate(
        (weapon.name, level) for weapon in WEAPONS for level in range(2, weapon.max_level + 1)
    )
)
