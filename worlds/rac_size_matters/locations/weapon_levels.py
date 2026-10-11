from functools import partial

from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAny

from .. import constants as C
from ..constants import Rac5Weapons
from ..items import PROGRESSIVE_WEAPON_NAME
from ..options import ChallengeMode, NgPlusItems, WeaponLevelChecks
from ..rules._helpers import HasChallengeMode, HasExpAccess, HasGoodExpPlanet
from .model import Completion, LocationOptions, Rac5Categories, Rac5CompletionSources, Rac5Locations

_C = Rac5Categories
_S = Rac5CompletionSources

_NEEDS_GOOD_EXP_PLANET = frozenset((Rac5Weapons.RYNO, Rac5Weapons.LASER_TRACER, Rac5Weapons.STATIC_BARRIER))


def access_rule(world, *, weapon, level):
    rule = (
        Has(PROGRESSIVE_WEAPON_NAME[weapon], level)
        if world.options.progressive_weapons
        else HasAny(weapon, PROGRESSIVE_WEAPON_NAME[weapon])
    ) & HasExpAccess()
    if level >= 5:
        rule = rule & HasChallengeMode(world, 1)
    if weapon in _NEEDS_GOOD_EXP_PLANET:
        rule = rule & HasGoodExpPlanet()
    return rule


LOCATIONS = (
    Rac5Locations(
        C.Rac5WeaponLevels.LACERATOR_LEVEL_2,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.LACERATOR, level=2),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.LACERATOR, 2)),
        options=LocationOptions(
            requirements=(OptionFilter(WeaponLevelChecks, (4,), "in"),), weapon=C.Rac5Weapons.LACERATOR
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.WEAPON_SUB_MAX_LEVEL)),
        weapon=C.Rac5WeaponKeys.LACERATOR,
        level=2,
        definition_order=156,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.LACERATOR_LEVEL_3,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.LACERATOR, level=3),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.LACERATOR, 3)),
        options=LocationOptions(
            requirements=(OptionFilter(WeaponLevelChecks, (4,), "in"),), weapon=C.Rac5Weapons.LACERATOR
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.WEAPON_SUB_MAX_LEVEL)),
        weapon=C.Rac5WeaponKeys.LACERATOR,
        level=3,
        definition_order=157,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.LACERATOR_LEVEL_4,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.LACERATOR, level=4),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.LACERATOR, 4)),
        options=LocationOptions(
            requirements=(OptionFilter(WeaponLevelChecks, (1, 3, 4), "in"),), weapon=C.Rac5Weapons.LACERATOR
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.WEAPON_MAX_LEVEL)),
        weapon=C.Rac5WeaponKeys.LACERATOR,
        level=4,
        definition_order=158,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.LACERATOR_LEVEL_5,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.LACERATOR, level=5),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.LACERATOR, 5)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (4,), "in"),
            ),
            weapon=C.Rac5Weapons.LACERATOR,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_SUB_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.LACERATOR,
        level=5,
        definition_order=159,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.LACERATOR_LEVEL_6,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.LACERATOR, level=6),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.LACERATOR, 6)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (4,), "in"),
            ),
            weapon=C.Rac5Weapons.LACERATOR,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_SUB_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.LACERATOR,
        level=6,
        definition_order=160,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.LACERATOR_LEVEL_7,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.LACERATOR, level=7),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.LACERATOR, 7)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (4,), "in"),
            ),
            weapon=C.Rac5Weapons.LACERATOR,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_SUB_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.LACERATOR,
        level=7,
        definition_order=161,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.LACERATOR_LEVEL_8,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.LACERATOR, level=8),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.LACERATOR, 8)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (2, 3, 4), "in"),
            ),
            weapon=C.Rac5Weapons.LACERATOR,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.LACERATOR,
        level=8,
        definition_order=162,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.CONCUSSION_GUN_LEVEL_2,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.CONCUSSION_GUN, level=2),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.CONCUSSION_GUN, 2)),
        options=LocationOptions(
            requirements=(OptionFilter(WeaponLevelChecks, (4,), "in"),), weapon=C.Rac5Weapons.CONCUSSION_GUN
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.WEAPON_SUB_MAX_LEVEL)),
        weapon=C.Rac5WeaponKeys.CONCUSSION_GUN,
        level=2,
        definition_order=163,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.CONCUSSION_GUN_LEVEL_3,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.CONCUSSION_GUN, level=3),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.CONCUSSION_GUN, 3)),
        options=LocationOptions(
            requirements=(OptionFilter(WeaponLevelChecks, (4,), "in"),), weapon=C.Rac5Weapons.CONCUSSION_GUN
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.WEAPON_SUB_MAX_LEVEL)),
        weapon=C.Rac5WeaponKeys.CONCUSSION_GUN,
        level=3,
        definition_order=164,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.CONCUSSION_GUN_LEVEL_4,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.CONCUSSION_GUN, level=4),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.CONCUSSION_GUN, 4)),
        options=LocationOptions(
            requirements=(OptionFilter(WeaponLevelChecks, (1, 3, 4), "in"),), weapon=C.Rac5Weapons.CONCUSSION_GUN
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.WEAPON_MAX_LEVEL)),
        weapon=C.Rac5WeaponKeys.CONCUSSION_GUN,
        level=4,
        definition_order=165,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.CONCUSSION_GUN_LEVEL_5,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.CONCUSSION_GUN, level=5),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.CONCUSSION_GUN, 5)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (4,), "in"),
            ),
            weapon=C.Rac5Weapons.CONCUSSION_GUN,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_SUB_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.CONCUSSION_GUN,
        level=5,
        definition_order=166,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.CONCUSSION_GUN_LEVEL_6,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.CONCUSSION_GUN, level=6),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.CONCUSSION_GUN, 6)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (4,), "in"),
            ),
            weapon=C.Rac5Weapons.CONCUSSION_GUN,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_SUB_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.CONCUSSION_GUN,
        level=6,
        definition_order=167,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.CONCUSSION_GUN_LEVEL_7,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.CONCUSSION_GUN, level=7),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.CONCUSSION_GUN, 7)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (4,), "in"),
            ),
            weapon=C.Rac5Weapons.CONCUSSION_GUN,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_SUB_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.CONCUSSION_GUN,
        level=7,
        definition_order=168,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.CONCUSSION_GUN_LEVEL_8,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.CONCUSSION_GUN, level=8),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.CONCUSSION_GUN, 8)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (2, 3, 4), "in"),
            ),
            weapon=C.Rac5Weapons.CONCUSSION_GUN,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.CONCUSSION_GUN,
        level=8,
        definition_order=169,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.ACID_BOMB_GLOVE_LEVEL_2,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.ACID_BOMB_GLOVE, level=2),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.ACID_BOMB_GLOVE, 2)),
        options=LocationOptions(
            requirements=(OptionFilter(WeaponLevelChecks, (4,), "in"),), weapon=C.Rac5Weapons.ACID_BOMB_GLOVE
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.WEAPON_SUB_MAX_LEVEL)),
        weapon=C.Rac5WeaponKeys.ACID_BOMB_GLOVE,
        level=2,
        definition_order=170,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.ACID_BOMB_GLOVE_LEVEL_3,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.ACID_BOMB_GLOVE, level=3),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.ACID_BOMB_GLOVE, 3)),
        options=LocationOptions(
            requirements=(OptionFilter(WeaponLevelChecks, (4,), "in"),), weapon=C.Rac5Weapons.ACID_BOMB_GLOVE
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.WEAPON_SUB_MAX_LEVEL)),
        weapon=C.Rac5WeaponKeys.ACID_BOMB_GLOVE,
        level=3,
        definition_order=171,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.ACID_BOMB_GLOVE_LEVEL_4,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.ACID_BOMB_GLOVE, level=4),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.ACID_BOMB_GLOVE, 4)),
        options=LocationOptions(
            requirements=(OptionFilter(WeaponLevelChecks, (1, 3, 4), "in"),), weapon=C.Rac5Weapons.ACID_BOMB_GLOVE
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.WEAPON_MAX_LEVEL)),
        weapon=C.Rac5WeaponKeys.ACID_BOMB_GLOVE,
        level=4,
        definition_order=172,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.ACID_BOMB_GLOVE_LEVEL_5,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.ACID_BOMB_GLOVE, level=5),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.ACID_BOMB_GLOVE, 5)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (4,), "in"),
            ),
            weapon=C.Rac5Weapons.ACID_BOMB_GLOVE,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_SUB_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.ACID_BOMB_GLOVE,
        level=5,
        definition_order=173,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.ACID_BOMB_GLOVE_LEVEL_6,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.ACID_BOMB_GLOVE, level=6),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.ACID_BOMB_GLOVE, 6)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (4,), "in"),
            ),
            weapon=C.Rac5Weapons.ACID_BOMB_GLOVE,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_SUB_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.ACID_BOMB_GLOVE,
        level=6,
        definition_order=174,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.ACID_BOMB_GLOVE_LEVEL_7,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.ACID_BOMB_GLOVE, level=7),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.ACID_BOMB_GLOVE, 7)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (4,), "in"),
            ),
            weapon=C.Rac5Weapons.ACID_BOMB_GLOVE,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_SUB_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.ACID_BOMB_GLOVE,
        level=7,
        definition_order=175,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.ACID_BOMB_GLOVE_LEVEL_8,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.ACID_BOMB_GLOVE, level=8),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.ACID_BOMB_GLOVE, 8)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (2, 3, 4), "in"),
            ),
            weapon=C.Rac5Weapons.ACID_BOMB_GLOVE,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.ACID_BOMB_GLOVE,
        level=8,
        definition_order=176,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.AGENTS_OF_DOOM_LEVEL_2,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.AGENTS_OF_DOOM, level=2),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.AGENTS_OF_DOOM, 2)),
        options=LocationOptions(
            requirements=(OptionFilter(WeaponLevelChecks, (4,), "in"),), weapon=C.Rac5Weapons.AGENTS_OF_DOOM
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.WEAPON_SUB_MAX_LEVEL)),
        weapon=C.Rac5WeaponKeys.AGENTS_OF_DOOM,
        level=2,
        definition_order=177,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.AGENTS_OF_DOOM_LEVEL_3,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.AGENTS_OF_DOOM, level=3),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.AGENTS_OF_DOOM, 3)),
        options=LocationOptions(
            requirements=(OptionFilter(WeaponLevelChecks, (4,), "in"),), weapon=C.Rac5Weapons.AGENTS_OF_DOOM
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.WEAPON_SUB_MAX_LEVEL)),
        weapon=C.Rac5WeaponKeys.AGENTS_OF_DOOM,
        level=3,
        definition_order=178,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.AGENTS_OF_DOOM_LEVEL_4,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.AGENTS_OF_DOOM, level=4),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.AGENTS_OF_DOOM, 4)),
        options=LocationOptions(
            requirements=(OptionFilter(WeaponLevelChecks, (1, 3, 4), "in"),), weapon=C.Rac5Weapons.AGENTS_OF_DOOM
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.WEAPON_MAX_LEVEL)),
        weapon=C.Rac5WeaponKeys.AGENTS_OF_DOOM,
        level=4,
        definition_order=179,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.AGENTS_OF_DOOM_LEVEL_5,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.AGENTS_OF_DOOM, level=5),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.AGENTS_OF_DOOM, 5)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (4,), "in"),
            ),
            weapon=C.Rac5Weapons.AGENTS_OF_DOOM,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_SUB_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.AGENTS_OF_DOOM,
        level=5,
        definition_order=180,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.AGENTS_OF_DOOM_LEVEL_6,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.AGENTS_OF_DOOM, level=6),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.AGENTS_OF_DOOM, 6)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (4,), "in"),
            ),
            weapon=C.Rac5Weapons.AGENTS_OF_DOOM,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_SUB_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.AGENTS_OF_DOOM,
        level=6,
        definition_order=181,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.AGENTS_OF_DOOM_LEVEL_7,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.AGENTS_OF_DOOM, level=7),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.AGENTS_OF_DOOM, 7)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (4,), "in"),
            ),
            weapon=C.Rac5Weapons.AGENTS_OF_DOOM,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_SUB_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.AGENTS_OF_DOOM,
        level=7,
        definition_order=182,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.AGENTS_OF_DOOM_LEVEL_8,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.AGENTS_OF_DOOM, level=8),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.AGENTS_OF_DOOM, 8)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (2, 3, 4), "in"),
            ),
            weapon=C.Rac5Weapons.AGENTS_OF_DOOM,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.AGENTS_OF_DOOM,
        level=8,
        definition_order=183,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.BEE_MINE_GLOVE_LEVEL_2,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.BEE_MINE_GLOVE, level=2),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.BEE_MINE_GLOVE, 2)),
        options=LocationOptions(
            requirements=(OptionFilter(WeaponLevelChecks, (4,), "in"),), weapon=C.Rac5Weapons.BEE_MINE_GLOVE
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.WEAPON_SUB_MAX_LEVEL)),
        weapon=C.Rac5WeaponKeys.BEE_MINE_GLOVE,
        level=2,
        definition_order=184,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.BEE_MINE_GLOVE_LEVEL_3,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.BEE_MINE_GLOVE, level=3),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.BEE_MINE_GLOVE, 3)),
        options=LocationOptions(
            requirements=(OptionFilter(WeaponLevelChecks, (4,), "in"),), weapon=C.Rac5Weapons.BEE_MINE_GLOVE
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.WEAPON_SUB_MAX_LEVEL)),
        weapon=C.Rac5WeaponKeys.BEE_MINE_GLOVE,
        level=3,
        definition_order=185,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.BEE_MINE_GLOVE_LEVEL_4,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.BEE_MINE_GLOVE, level=4),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.BEE_MINE_GLOVE, 4)),
        options=LocationOptions(
            requirements=(OptionFilter(WeaponLevelChecks, (1, 3, 4), "in"),), weapon=C.Rac5Weapons.BEE_MINE_GLOVE
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.WEAPON_MAX_LEVEL)),
        weapon=C.Rac5WeaponKeys.BEE_MINE_GLOVE,
        level=4,
        definition_order=186,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.BEE_MINE_GLOVE_LEVEL_5,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.BEE_MINE_GLOVE, level=5),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.BEE_MINE_GLOVE, 5)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (4,), "in"),
            ),
            weapon=C.Rac5Weapons.BEE_MINE_GLOVE,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_SUB_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.BEE_MINE_GLOVE,
        level=5,
        definition_order=187,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.BEE_MINE_GLOVE_LEVEL_6,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.BEE_MINE_GLOVE, level=6),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.BEE_MINE_GLOVE, 6)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (4,), "in"),
            ),
            weapon=C.Rac5Weapons.BEE_MINE_GLOVE,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_SUB_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.BEE_MINE_GLOVE,
        level=6,
        definition_order=188,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.BEE_MINE_GLOVE_LEVEL_7,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.BEE_MINE_GLOVE, level=7),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.BEE_MINE_GLOVE, 7)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (4,), "in"),
            ),
            weapon=C.Rac5Weapons.BEE_MINE_GLOVE,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_SUB_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.BEE_MINE_GLOVE,
        level=7,
        definition_order=189,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.BEE_MINE_GLOVE_LEVEL_8,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.BEE_MINE_GLOVE, level=8),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.BEE_MINE_GLOVE, 8)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (2, 3, 4), "in"),
            ),
            weapon=C.Rac5Weapons.BEE_MINE_GLOVE,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.BEE_MINE_GLOVE,
        level=8,
        definition_order=190,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.STATIC_BARRIER_LEVEL_2,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.STATIC_BARRIER, level=2),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.STATIC_BARRIER, 2)),
        options=LocationOptions(
            requirements=(OptionFilter(WeaponLevelChecks, (4,), "in"),), weapon=C.Rac5Weapons.STATIC_BARRIER
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.WEAPON_SUB_MAX_LEVEL)),
        weapon=C.Rac5WeaponKeys.STATIC_BARRIER,
        level=2,
        definition_order=191,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.STATIC_BARRIER_LEVEL_3,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.STATIC_BARRIER, level=3),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.STATIC_BARRIER, 3)),
        options=LocationOptions(
            requirements=(OptionFilter(WeaponLevelChecks, (4,), "in"),), weapon=C.Rac5Weapons.STATIC_BARRIER
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.WEAPON_SUB_MAX_LEVEL)),
        weapon=C.Rac5WeaponKeys.STATIC_BARRIER,
        level=3,
        definition_order=192,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.STATIC_BARRIER_LEVEL_4,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.STATIC_BARRIER, level=4),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.STATIC_BARRIER, 4)),
        options=LocationOptions(
            requirements=(OptionFilter(WeaponLevelChecks, (1, 3, 4), "in"),), weapon=C.Rac5Weapons.STATIC_BARRIER
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.WEAPON_MAX_LEVEL)),
        weapon=C.Rac5WeaponKeys.STATIC_BARRIER,
        level=4,
        definition_order=193,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.STATIC_BARRIER_LEVEL_5,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.STATIC_BARRIER, level=5),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.STATIC_BARRIER, 5)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (4,), "in"),
            ),
            weapon=C.Rac5Weapons.STATIC_BARRIER,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_SUB_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.STATIC_BARRIER,
        level=5,
        definition_order=194,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.STATIC_BARRIER_LEVEL_6,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.STATIC_BARRIER, level=6),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.STATIC_BARRIER, 6)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (4,), "in"),
            ),
            weapon=C.Rac5Weapons.STATIC_BARRIER,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_SUB_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.STATIC_BARRIER,
        level=6,
        definition_order=195,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.STATIC_BARRIER_LEVEL_7,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.STATIC_BARRIER, level=7),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.STATIC_BARRIER, 7)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (4,), "in"),
            ),
            weapon=C.Rac5Weapons.STATIC_BARRIER,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_SUB_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.STATIC_BARRIER,
        level=7,
        definition_order=196,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.STATIC_BARRIER_LEVEL_8,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.STATIC_BARRIER, level=8),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.STATIC_BARRIER, 8)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (2, 3, 4), "in"),
            ),
            weapon=C.Rac5Weapons.STATIC_BARRIER,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.STATIC_BARRIER,
        level=8,
        definition_order=197,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.SHOCK_ROCKET_LEVEL_2,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.SHOCK_ROCKET, level=2),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.SHOCK_ROCKET, 2)),
        options=LocationOptions(
            requirements=(OptionFilter(WeaponLevelChecks, (4,), "in"),), weapon=C.Rac5Weapons.SHOCK_ROCKET
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.WEAPON_SUB_MAX_LEVEL)),
        weapon=C.Rac5WeaponKeys.SHOCK_ROCKET,
        level=2,
        definition_order=198,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.SHOCK_ROCKET_LEVEL_3,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.SHOCK_ROCKET, level=3),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.SHOCK_ROCKET, 3)),
        options=LocationOptions(
            requirements=(OptionFilter(WeaponLevelChecks, (4,), "in"),), weapon=C.Rac5Weapons.SHOCK_ROCKET
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.WEAPON_SUB_MAX_LEVEL)),
        weapon=C.Rac5WeaponKeys.SHOCK_ROCKET,
        level=3,
        definition_order=199,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.SHOCK_ROCKET_LEVEL_4,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.SHOCK_ROCKET, level=4),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.SHOCK_ROCKET, 4)),
        options=LocationOptions(
            requirements=(OptionFilter(WeaponLevelChecks, (1, 3, 4), "in"),), weapon=C.Rac5Weapons.SHOCK_ROCKET
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.WEAPON_MAX_LEVEL)),
        weapon=C.Rac5WeaponKeys.SHOCK_ROCKET,
        level=4,
        definition_order=200,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.SHOCK_ROCKET_LEVEL_5,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.SHOCK_ROCKET, level=5),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.SHOCK_ROCKET, 5)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (4,), "in"),
            ),
            weapon=C.Rac5Weapons.SHOCK_ROCKET,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_SUB_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.SHOCK_ROCKET,
        level=5,
        definition_order=201,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.SHOCK_ROCKET_LEVEL_6,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.SHOCK_ROCKET, level=6),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.SHOCK_ROCKET, 6)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (4,), "in"),
            ),
            weapon=C.Rac5Weapons.SHOCK_ROCKET,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_SUB_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.SHOCK_ROCKET,
        level=6,
        definition_order=202,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.SHOCK_ROCKET_LEVEL_7,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.SHOCK_ROCKET, level=7),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.SHOCK_ROCKET, 7)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (4,), "in"),
            ),
            weapon=C.Rac5Weapons.SHOCK_ROCKET,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_SUB_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.SHOCK_ROCKET,
        level=7,
        definition_order=203,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.SHOCK_ROCKET_LEVEL_8,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.SHOCK_ROCKET, level=8),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.SHOCK_ROCKET, 8)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (2, 3, 4), "in"),
            ),
            weapon=C.Rac5Weapons.SHOCK_ROCKET,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.SHOCK_ROCKET,
        level=8,
        definition_order=204,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.SNIPER_MINE_LEVEL_2,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.SNIPER_MINE, level=2),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.SNIPER_MINE, 2)),
        options=LocationOptions(
            requirements=(OptionFilter(WeaponLevelChecks, (4,), "in"),), weapon=C.Rac5Weapons.SNIPER_MINE
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.WEAPON_SUB_MAX_LEVEL)),
        weapon=C.Rac5WeaponKeys.SNIPER_MINE,
        level=2,
        definition_order=205,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.SNIPER_MINE_LEVEL_3,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.SNIPER_MINE, level=3),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.SNIPER_MINE, 3)),
        options=LocationOptions(
            requirements=(OptionFilter(WeaponLevelChecks, (4,), "in"),), weapon=C.Rac5Weapons.SNIPER_MINE
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.WEAPON_SUB_MAX_LEVEL)),
        weapon=C.Rac5WeaponKeys.SNIPER_MINE,
        level=3,
        definition_order=206,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.SNIPER_MINE_LEVEL_4,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.SNIPER_MINE, level=4),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.SNIPER_MINE, 4)),
        options=LocationOptions(
            requirements=(OptionFilter(WeaponLevelChecks, (1, 3, 4), "in"),), weapon=C.Rac5Weapons.SNIPER_MINE
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.WEAPON_MAX_LEVEL)),
        weapon=C.Rac5WeaponKeys.SNIPER_MINE,
        level=4,
        definition_order=207,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.SNIPER_MINE_LEVEL_5,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.SNIPER_MINE, level=5),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.SNIPER_MINE, 5)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (4,), "in"),
            ),
            weapon=C.Rac5Weapons.SNIPER_MINE,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_SUB_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.SNIPER_MINE,
        level=5,
        definition_order=208,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.SNIPER_MINE_LEVEL_6,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.SNIPER_MINE, level=6),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.SNIPER_MINE, 6)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (4,), "in"),
            ),
            weapon=C.Rac5Weapons.SNIPER_MINE,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_SUB_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.SNIPER_MINE,
        level=6,
        definition_order=209,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.SNIPER_MINE_LEVEL_7,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.SNIPER_MINE, level=7),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.SNIPER_MINE, 7)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (4,), "in"),
            ),
            weapon=C.Rac5Weapons.SNIPER_MINE,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_SUB_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.SNIPER_MINE,
        level=7,
        definition_order=210,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.SNIPER_MINE_LEVEL_8,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.SNIPER_MINE, level=8),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.SNIPER_MINE, 8)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (2, 3, 4), "in"),
            ),
            weapon=C.Rac5Weapons.SNIPER_MINE,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.SNIPER_MINE,
        level=8,
        definition_order=211,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.SCORCHER_LEVEL_2,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.SCORCHER, level=2),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.SCORCHER, 2)),
        options=LocationOptions(
            requirements=(OptionFilter(WeaponLevelChecks, (4,), "in"),), weapon=C.Rac5Weapons.SCORCHER
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.WEAPON_SUB_MAX_LEVEL)),
        weapon=C.Rac5WeaponKeys.SCORCHER,
        level=2,
        definition_order=212,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.SCORCHER_LEVEL_3,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.SCORCHER, level=3),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.SCORCHER, 3)),
        options=LocationOptions(
            requirements=(OptionFilter(WeaponLevelChecks, (4,), "in"),), weapon=C.Rac5Weapons.SCORCHER
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.WEAPON_SUB_MAX_LEVEL)),
        weapon=C.Rac5WeaponKeys.SCORCHER,
        level=3,
        definition_order=213,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.SCORCHER_LEVEL_4,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.SCORCHER, level=4),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.SCORCHER, 4)),
        options=LocationOptions(
            requirements=(OptionFilter(WeaponLevelChecks, (1, 3, 4), "in"),), weapon=C.Rac5Weapons.SCORCHER
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.WEAPON_MAX_LEVEL)),
        weapon=C.Rac5WeaponKeys.SCORCHER,
        level=4,
        definition_order=214,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.SCORCHER_LEVEL_5,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.SCORCHER, level=5),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.SCORCHER, 5)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (4,), "in"),
            ),
            weapon=C.Rac5Weapons.SCORCHER,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_SUB_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.SCORCHER,
        level=5,
        definition_order=215,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.SCORCHER_LEVEL_6,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.SCORCHER, level=6),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.SCORCHER, 6)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (4,), "in"),
            ),
            weapon=C.Rac5Weapons.SCORCHER,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_SUB_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.SCORCHER,
        level=6,
        definition_order=216,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.SCORCHER_LEVEL_7,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.SCORCHER, level=7),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.SCORCHER, 7)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (4,), "in"),
            ),
            weapon=C.Rac5Weapons.SCORCHER,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_SUB_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.SCORCHER,
        level=7,
        definition_order=217,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.SCORCHER_LEVEL_8,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.SCORCHER, level=8),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.SCORCHER, 8)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (2, 3, 4), "in"),
            ),
            weapon=C.Rac5Weapons.SCORCHER,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.SCORCHER,
        level=8,
        definition_order=218,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.LASER_TRACER_LEVEL_2,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.LASER_TRACER, level=2),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.LASER_TRACER, 2)),
        options=LocationOptions(
            requirements=(OptionFilter(WeaponLevelChecks, (4,), "in"),), weapon=C.Rac5Weapons.LASER_TRACER
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.WEAPON_SUB_MAX_LEVEL)),
        weapon=C.Rac5WeaponKeys.LASER_TRACER,
        level=2,
        definition_order=219,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.LASER_TRACER_LEVEL_3,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.LASER_TRACER, level=3),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.LASER_TRACER, 3)),
        options=LocationOptions(
            requirements=(OptionFilter(WeaponLevelChecks, (4,), "in"),), weapon=C.Rac5Weapons.LASER_TRACER
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.WEAPON_SUB_MAX_LEVEL)),
        weapon=C.Rac5WeaponKeys.LASER_TRACER,
        level=3,
        definition_order=220,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.LASER_TRACER_LEVEL_4,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.LASER_TRACER, level=4),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.LASER_TRACER, 4)),
        options=LocationOptions(
            requirements=(OptionFilter(WeaponLevelChecks, (1, 3, 4), "in"),), weapon=C.Rac5Weapons.LASER_TRACER
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.WEAPON_MAX_LEVEL)),
        weapon=C.Rac5WeaponKeys.LASER_TRACER,
        level=4,
        definition_order=221,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.LASER_TRACER_LEVEL_5,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.LASER_TRACER, level=5),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.LASER_TRACER, 5)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (4,), "in"),
            ),
            weapon=C.Rac5Weapons.LASER_TRACER,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_SUB_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.LASER_TRACER,
        level=5,
        definition_order=222,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.LASER_TRACER_LEVEL_6,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.LASER_TRACER, level=6),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.LASER_TRACER, 6)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (4,), "in"),
            ),
            weapon=C.Rac5Weapons.LASER_TRACER,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_SUB_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.LASER_TRACER,
        level=6,
        definition_order=223,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.LASER_TRACER_LEVEL_7,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.LASER_TRACER, level=7),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.LASER_TRACER, 7)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (4,), "in"),
            ),
            weapon=C.Rac5Weapons.LASER_TRACER,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_SUB_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.LASER_TRACER,
        level=7,
        definition_order=224,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.LASER_TRACER_LEVEL_8,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.LASER_TRACER, level=8),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.LASER_TRACER, 8)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (2, 3, 4), "in"),
            ),
            weapon=C.Rac5Weapons.LASER_TRACER,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.LASER_TRACER,
        level=8,
        definition_order=225,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.SUCK_CANNON_LEVEL_2,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.SUCK_CANNON, level=2),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.SUCK_CANNON, 2)),
        options=LocationOptions(
            requirements=(OptionFilter(WeaponLevelChecks, (4,), "in"),), weapon=C.Rac5Weapons.SUCK_CANNON
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.WEAPON_SUB_MAX_LEVEL)),
        weapon=C.Rac5WeaponKeys.SUCK_CANNON,
        level=2,
        definition_order=226,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.SUCK_CANNON_LEVEL_3,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.SUCK_CANNON, level=3),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.SUCK_CANNON, 3)),
        options=LocationOptions(
            requirements=(OptionFilter(WeaponLevelChecks, (4,), "in"),), weapon=C.Rac5Weapons.SUCK_CANNON
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.WEAPON_SUB_MAX_LEVEL)),
        weapon=C.Rac5WeaponKeys.SUCK_CANNON,
        level=3,
        definition_order=227,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.SUCK_CANNON_LEVEL_4,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.SUCK_CANNON, level=4),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.SUCK_CANNON, 4)),
        options=LocationOptions(
            requirements=(OptionFilter(WeaponLevelChecks, (1, 3, 4), "in"),), weapon=C.Rac5Weapons.SUCK_CANNON
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.WEAPON_MAX_LEVEL)),
        weapon=C.Rac5WeaponKeys.SUCK_CANNON,
        level=4,
        definition_order=228,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.SUCK_CANNON_LEVEL_5,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.SUCK_CANNON, level=5),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.SUCK_CANNON, 5)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (4,), "in"),
            ),
            weapon=C.Rac5Weapons.SUCK_CANNON,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_SUB_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.SUCK_CANNON,
        level=5,
        definition_order=229,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.SUCK_CANNON_LEVEL_6,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.SUCK_CANNON, level=6),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.SUCK_CANNON, 6)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (4,), "in"),
            ),
            weapon=C.Rac5Weapons.SUCK_CANNON,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_SUB_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.SUCK_CANNON,
        level=6,
        definition_order=230,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.SUCK_CANNON_LEVEL_7,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.SUCK_CANNON, level=7),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.SUCK_CANNON, 7)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (4,), "in"),
            ),
            weapon=C.Rac5Weapons.SUCK_CANNON,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_SUB_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.SUCK_CANNON,
        level=7,
        definition_order=231,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.SUCK_CANNON_LEVEL_8,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.SUCK_CANNON, level=8),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.SUCK_CANNON, 8)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (2, 3, 4), "in"),
            ),
            weapon=C.Rac5Weapons.SUCK_CANNON,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.SUCK_CANNON,
        level=8,
        definition_order=232,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.MOOTATOR_LEVEL_2,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.MOOTATOR, level=2),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.MOOTATOR, 2)),
        options=LocationOptions(
            requirements=(OptionFilter(WeaponLevelChecks, (4,), "in"),), weapon=C.Rac5Weapons.MOOTATOR
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.WEAPON_SUB_MAX_LEVEL)),
        weapon=C.Rac5WeaponKeys.MOOTATOR,
        level=2,
        definition_order=233,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.MOOTATOR_LEVEL_3,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.MOOTATOR, level=3),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.MOOTATOR, 3)),
        options=LocationOptions(
            requirements=(OptionFilter(WeaponLevelChecks, (4,), "in"),), weapon=C.Rac5Weapons.MOOTATOR
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.WEAPON_SUB_MAX_LEVEL)),
        weapon=C.Rac5WeaponKeys.MOOTATOR,
        level=3,
        definition_order=234,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.MOOTATOR_LEVEL_4,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.MOOTATOR, level=4),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.MOOTATOR, 4)),
        options=LocationOptions(
            requirements=(OptionFilter(WeaponLevelChecks, (1, 3, 4), "in"),), weapon=C.Rac5Weapons.MOOTATOR
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.WEAPON_MAX_LEVEL)),
        weapon=C.Rac5WeaponKeys.MOOTATOR,
        level=4,
        definition_order=235,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.MOOTATOR_LEVEL_5,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.MOOTATOR, level=5),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.MOOTATOR, 5)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (4,), "in"),
            ),
            weapon=C.Rac5Weapons.MOOTATOR,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_SUB_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.MOOTATOR,
        level=5,
        definition_order=236,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.MOOTATOR_LEVEL_6,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.MOOTATOR, level=6),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.MOOTATOR, 6)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (4,), "in"),
            ),
            weapon=C.Rac5Weapons.MOOTATOR,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_SUB_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.MOOTATOR,
        level=6,
        definition_order=237,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.MOOTATOR_LEVEL_7,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.MOOTATOR, level=7),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.MOOTATOR, 7)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (4,), "in"),
            ),
            weapon=C.Rac5Weapons.MOOTATOR,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_SUB_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.MOOTATOR,
        level=7,
        definition_order=238,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.MOOTATOR_LEVEL_8,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.MOOTATOR, level=8),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.MOOTATOR, 8)),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(WeaponLevelChecks, (2, 3, 4), "in"),
            ),
            weapon=C.Rac5Weapons.MOOTATOR,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.CHALLENGE_MODE_MAX_LEVEL, _C.CHALLENGE_MODE_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.MOOTATOR,
        level=8,
        definition_order=239,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.RYNO_LEVEL_2,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.RYNO, level=2),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.RYNO, 2)),
        options=LocationOptions(
            requirements=(
                OptionFilter(NgPlusItems, (1,), "in"),
                OptionFilter(WeaponLevelChecks, (4,), "in"),
            ),
            weapon=C.Rac5Weapons.RYNO,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.WEAPON_SUB_MAX_LEVEL, _C.NG_PLUS_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.RYNO,
        level=2,
        definition_order=240,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.RYNO_LEVEL_3,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.RYNO, level=3),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.RYNO, 3)),
        options=LocationOptions(
            requirements=(
                OptionFilter(NgPlusItems, (1,), "in"),
                OptionFilter(WeaponLevelChecks, (4,), "in"),
            ),
            weapon=C.Rac5Weapons.RYNO,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.WEAPON_SUB_MAX_LEVEL, _C.NG_PLUS_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.RYNO,
        level=3,
        definition_order=241,
    ),
    Rac5Locations(
        C.Rac5WeaponLevels.RYNO_LEVEL_4,
        "Menu",
        partial(access_rule, weapon=C.Rac5Weapons.RYNO, level=4),
        Completion(_S.WEAPON_LEVELS, (C.Rac5WeaponKeys.RYNO, 4)),
        options=LocationOptions(
            requirements=(
                OptionFilter(NgPlusItems, (1,), "in"),
                OptionFilter(WeaponLevelChecks, (1, 3, 4), "in"),
            ),
            weapon=C.Rac5Weapons.RYNO,
        ),
        categories=frozenset((_C.WEAPON_LEVEL, _C.WEAPON_MAX_LEVEL, _C.NG_PLUS_WEAPON_LEVEL)),
        weapon=C.Rac5WeaponKeys.RYNO,
        level=4,
        definition_order=242,
    ),
)
