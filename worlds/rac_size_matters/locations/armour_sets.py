from functools import partial

from rule_builder.options import OptionFilter
from rule_builder.rules import And

from .. import constants as C
from ..items import ARMOUR_SETS
from ..options import ArmourSetChecks, ChallengeMode, NgPlusItems
from ..rules._helpers import HasArmourPiece, HasChallengeMode
from .model import ArmourSetCompletion, LocationOptions, Rac5Locations


def access_rule(world, *, combo, categories):
    rule = And(
        *(
            HasArmourPiece(ARMOUR_SETS[getattr(combo, field) - 1][0], field.title())
            for field in ("chestplate", "helmet", "gloves", "boots")
            if getattr(combo, field) is not None
        )
    )
    if "challenge_mode_1_armour_set" in categories:
        rule = rule & HasChallengeMode(world, 1)
    if "challenge_mode_2_armour_set" in categories:
        rule = rule & HasChallengeMode(world, 2)
    return rule


LOCATIONS = (
    Rac5Locations(
        C.Rac5ArmourSet.WILDFIRE,
        C.Rac5Planets.POKITARU,
        partial(
            access_rule,
            combo=ArmourSetCompletion(chestplate=1, helmet=1, gloves=1, boots=1),
            categories=frozenset(("armour_set_check",)),
        ),
        ArmourSetCompletion(chestplate=1, helmet=1, gloves=1, boots=1),
        options=LocationOptions(requirements=(OptionFilter(ArmourSetChecks, (1,), "in"),)),
        categories=frozenset(("armour_set_check",)),
        definition_order=313,
    ),
    Rac5Locations(
        C.Rac5ArmourSet.WILDBURST,
        C.Rac5Planets.POKITARU,
        partial(
            access_rule,
            combo=ArmourSetCompletion(chestplate=1, helmet=2, gloves=1, boots=1),
            categories=frozenset(("armour_set_check",)),
        ),
        ArmourSetCompletion(chestplate=1, helmet=2, gloves=1, boots=1),
        options=LocationOptions(requirements=(OptionFilter(ArmourSetChecks, (1,), "in"),)),
        categories=frozenset(("armour_set_check",)),
        definition_order=314,
    ),
    Rac5Locations(
        C.Rac5ArmourSet.SLUDGE_MK9,
        C.Rac5Planets.POKITARU,
        partial(
            access_rule,
            combo=ArmourSetCompletion(chestplate=2, helmet=2, gloves=2, boots=2),
            categories=frozenset(("armour_set_check",)),
        ),
        ArmourSetCompletion(chestplate=2, helmet=2, gloves=2, boots=2),
        options=LocationOptions(requirements=(OptionFilter(ArmourSetChecks, (1,), "in"),)),
        categories=frozenset(("armour_set_check",)),
        definition_order=315,
    ),
    Rac5Locations(
        C.Rac5ArmourSet.CRYSTALLIX,
        C.Rac5Planets.POKITARU,
        partial(
            access_rule,
            combo=ArmourSetCompletion(chestplate=3, helmet=3, gloves=3, boots=3),
            categories=frozenset(("armour_set_check",)),
        ),
        ArmourSetCompletion(chestplate=3, helmet=3, gloves=3, boots=3),
        options=LocationOptions(requirements=(OptionFilter(ArmourSetChecks, (1,), "in"),)),
        categories=frozenset(("armour_set_check",)),
        definition_order=316,
    ),
    Rac5Locations(
        C.Rac5ArmourSet.TRIPLE_WAVE,
        C.Rac5Planets.POKITARU,
        partial(
            access_rule,
            combo=ArmourSetCompletion(chestplate=4, helmet=1, gloves=2, boots=4),
            categories=frozenset(("armour_set_check",)),
        ),
        ArmourSetCompletion(chestplate=4, helmet=1, gloves=2, boots=4),
        options=LocationOptions(requirements=(OptionFilter(ArmourSetChecks, (1,), "in"),)),
        categories=frozenset(("armour_set_check",)),
        definition_order=317,
    ),
    Rac5Locations(
        C.Rac5ArmourSet.SHOCK_CRYSTAL,
        C.Rac5Planets.POKITARU,
        partial(
            access_rule,
            combo=ArmourSetCompletion(chestplate=3, helmet=4, gloves=3, boots=4),
            categories=frozenset(("armour_set_check",)),
        ),
        ArmourSetCompletion(chestplate=3, helmet=4, gloves=3, boots=4),
        options=LocationOptions(requirements=(OptionFilter(ArmourSetChecks, (1,), "in"),)),
        categories=frozenset(("armour_set_check",)),
        definition_order=318,
    ),
    Rac5Locations(
        C.Rac5ArmourSet.ELECTROSHOCK,
        C.Rac5Planets.POKITARU,
        partial(
            access_rule,
            combo=ArmourSetCompletion(chestplate=4, helmet=4, gloves=4, boots=4),
            categories=frozenset(("armour_set_check",)),
        ),
        ArmourSetCompletion(chestplate=4, helmet=4, gloves=4, boots=4),
        options=LocationOptions(requirements=(OptionFilter(ArmourSetChecks, (1,), "in"),)),
        categories=frozenset(("armour_set_check",)),
        definition_order=319,
    ),
    Rac5Locations(
        C.Rac5ArmourSet.MEGA_BOMB,
        C.Rac5Planets.POKITARU,
        partial(
            access_rule,
            combo=ArmourSetCompletion(chestplate=5, helmet=5, gloves=5, boots=5),
            categories=frozenset(("armour_set_check",)),
        ),
        ArmourSetCompletion(chestplate=5, helmet=5, gloves=5, boots=5),
        options=LocationOptions(requirements=(OptionFilter(ArmourSetChecks, (1,), "in"),)),
        categories=frozenset(("armour_set_check",)),
        definition_order=320,
    ),
    Rac5Locations(
        C.Rac5ArmourSet.FIRE_BOMB,
        C.Rac5Planets.POKITARU,
        partial(
            access_rule,
            combo=ArmourSetCompletion(chestplate=5, helmet=5, gloves=1, boots=5),
            categories=frozenset(("armour_set_check",)),
        ),
        ArmourSetCompletion(chestplate=5, helmet=5, gloves=1, boots=5),
        options=LocationOptions(requirements=(OptionFilter(ArmourSetChecks, (1,), "in"),)),
        categories=frozenset(("armour_set_check",)),
        definition_order=321,
    ),
    Rac5Locations(
        C.Rac5ArmourSet.HYPERBOREAN,
        C.Rac5Planets.POKITARU,
        partial(
            access_rule,
            combo=ArmourSetCompletion(chestplate=6, helmet=6, gloves=6, boots=6),
            categories=frozenset(("armour_set_check", "ng_plus_armour_set", "challenge_mode_1_armour_set")),
        ),
        ArmourSetCompletion(chestplate=6, helmet=6, gloves=6, boots=6),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(NgPlusItems, (1,), "in"),
                OptionFilter(ArmourSetChecks, (1,), "in"),
            )
        ),
        categories=frozenset(("armour_set_check", "ng_plus_armour_set", "challenge_mode_1_armour_set")),
        definition_order=322,
    ),
    Rac5Locations(
        C.Rac5ArmourSet.ICE_II,
        C.Rac5Planets.POKITARU,
        partial(
            access_rule,
            combo=ArmourSetCompletion(chestplate=6, helmet=3, gloves=6, boots=6),
            categories=frozenset(("armour_set_check", "ng_plus_armour_set", "challenge_mode_1_armour_set")),
        ),
        ArmourSetCompletion(chestplate=6, helmet=3, gloves=6, boots=6),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (1, 2), "in"),
                OptionFilter(NgPlusItems, (1,), "in"),
                OptionFilter(ArmourSetChecks, (1,), "in"),
            )
        ),
        categories=frozenset(("armour_set_check", "ng_plus_armour_set", "challenge_mode_1_armour_set")),
        definition_order=323,
    ),
    Rac5Locations(
        C.Rac5ArmourSet.CHAMELEON,
        C.Rac5Planets.POKITARU,
        partial(
            access_rule,
            combo=ArmourSetCompletion(chestplate=7, helmet=7, gloves=7, boots=7),
            categories=frozenset(("armour_set_check", "ng_plus_armour_set", "challenge_mode_2_armour_set")),
        ),
        ArmourSetCompletion(chestplate=7, helmet=7, gloves=7, boots=7),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (2,), "in"),
                OptionFilter(NgPlusItems, (1,), "in"),
                OptionFilter(ArmourSetChecks, (1,), "in"),
            )
        ),
        categories=frozenset(("armour_set_check", "ng_plus_armour_set", "challenge_mode_2_armour_set")),
        definition_order=324,
    ),
    Rac5Locations(
        C.Rac5ArmourSet.STALKER,
        C.Rac5Planets.POKITARU,
        partial(
            access_rule,
            combo=ArmourSetCompletion(chestplate=7, helmet=1, gloves=2, boots=7),
            categories=frozenset(("armour_set_check", "ng_plus_armour_set", "challenge_mode_2_armour_set")),
        ),
        ArmourSetCompletion(chestplate=7, helmet=1, gloves=2, boots=7),
        options=LocationOptions(
            requirements=(
                OptionFilter(ChallengeMode, (2,), "in"),
                OptionFilter(NgPlusItems, (1,), "in"),
                OptionFilter(ArmourSetChecks, (1,), "in"),
            )
        ),
        categories=frozenset(("armour_set_check", "ng_plus_armour_set", "challenge_mode_2_armour_set")),
        definition_order=325,
    ),
)
