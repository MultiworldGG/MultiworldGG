from rule_builder.options import OptionFilter
from rule_builder.rules import And, Rule

from ..constants import Rac5ArmourSet, Rac5Planets
from ..items import ARMOUR_SETS
from ..options import ArmourSetChecks, ChallengeMode, NgPlusItems
from ..rules._helpers import HasArmourPiece, HasChallengeMode
from .model import ArmourSetCompletion, LocationOptions, Rac5Locations


def access_rule(combo: ArmourSetCompletion, categories: frozenset[str]) -> Rule:
    rule = And(
        *(
            HasArmourPiece(ARMOUR_SETS[getattr(combo, field) - 1][0], field.title())
            for field in ("chestplate", "helmet", "gloves", "boots")
            if getattr(combo, field) is not None
        )
    )
    if "challenge_mode_1_armour_set" in categories:
        rule = rule & HasChallengeMode(1)
    if "challenge_mode_2_armour_set" in categories:
        rule = rule & HasChallengeMode(2)
    return rule


LOCATIONS = (
    Rac5Locations(
        Rac5ArmourSet.WILDFIRE,
        Rac5Planets.POKITARU,
        access_rule(
            combo=ArmourSetCompletion(chestplate=1, helmet=1, gloves=1, boots=1),
            categories=frozenset(("armour_set_check",)),
        ),
        ArmourSetCompletion(chestplate=1, helmet=1, gloves=1, boots=1),
        options=LocationOptions(requirements=(OptionFilter(ArmourSetChecks, (1,), "in"),)),
        categories=frozenset(("armour_set_check",)),
        definition_order=313,
    ),
    Rac5Locations(
        Rac5ArmourSet.WILDBURST,
        Rac5Planets.POKITARU,
        access_rule(
            combo=ArmourSetCompletion(chestplate=1, helmet=2, gloves=1, boots=1),
            categories=frozenset(("armour_set_check",)),
        ),
        ArmourSetCompletion(chestplate=1, helmet=2, gloves=1, boots=1),
        options=LocationOptions(requirements=(OptionFilter(ArmourSetChecks, (1,), "in"),)),
        categories=frozenset(("armour_set_check",)),
        definition_order=314,
    ),
    Rac5Locations(
        Rac5ArmourSet.SLUDGE_MK9,
        Rac5Planets.POKITARU,
        access_rule(
            combo=ArmourSetCompletion(chestplate=2, helmet=2, gloves=2, boots=2),
            categories=frozenset(("armour_set_check",)),
        ),
        ArmourSetCompletion(chestplate=2, helmet=2, gloves=2, boots=2),
        options=LocationOptions(requirements=(OptionFilter(ArmourSetChecks, (1,), "in"),)),
        categories=frozenset(("armour_set_check",)),
        definition_order=315,
    ),
    Rac5Locations(
        Rac5ArmourSet.CRYSTALLIX,
        Rac5Planets.POKITARU,
        access_rule(
            combo=ArmourSetCompletion(chestplate=3, helmet=3, gloves=3, boots=3),
            categories=frozenset(("armour_set_check",)),
        ),
        ArmourSetCompletion(chestplate=3, helmet=3, gloves=3, boots=3),
        options=LocationOptions(requirements=(OptionFilter(ArmourSetChecks, (1,), "in"),)),
        categories=frozenset(("armour_set_check",)),
        definition_order=316,
    ),
    Rac5Locations(
        Rac5ArmourSet.TRIPLE_WAVE,
        Rac5Planets.POKITARU,
        access_rule(
            combo=ArmourSetCompletion(chestplate=4, helmet=1, gloves=2, boots=4),
            categories=frozenset(("armour_set_check",)),
        ),
        ArmourSetCompletion(chestplate=4, helmet=1, gloves=2, boots=4),
        options=LocationOptions(requirements=(OptionFilter(ArmourSetChecks, (1,), "in"),)),
        categories=frozenset(("armour_set_check",)),
        definition_order=317,
    ),
    Rac5Locations(
        Rac5ArmourSet.SHOCK_CRYSTAL,
        Rac5Planets.POKITARU,
        access_rule(
            combo=ArmourSetCompletion(chestplate=3, helmet=4, gloves=3, boots=4),
            categories=frozenset(("armour_set_check",)),
        ),
        ArmourSetCompletion(chestplate=3, helmet=4, gloves=3, boots=4),
        options=LocationOptions(requirements=(OptionFilter(ArmourSetChecks, (1,), "in"),)),
        categories=frozenset(("armour_set_check",)),
        definition_order=318,
    ),
    Rac5Locations(
        Rac5ArmourSet.ELECTROSHOCK,
        Rac5Planets.POKITARU,
        access_rule(
            combo=ArmourSetCompletion(chestplate=4, helmet=4, gloves=4, boots=4),
            categories=frozenset(("armour_set_check",)),
        ),
        ArmourSetCompletion(chestplate=4, helmet=4, gloves=4, boots=4),
        options=LocationOptions(requirements=(OptionFilter(ArmourSetChecks, (1,), "in"),)),
        categories=frozenset(("armour_set_check",)),
        definition_order=319,
    ),
    Rac5Locations(
        Rac5ArmourSet.MEGA_BOMB,
        Rac5Planets.POKITARU,
        access_rule(
            combo=ArmourSetCompletion(chestplate=5, helmet=5, gloves=5, boots=5),
            categories=frozenset(("armour_set_check",)),
        ),
        ArmourSetCompletion(chestplate=5, helmet=5, gloves=5, boots=5),
        options=LocationOptions(requirements=(OptionFilter(ArmourSetChecks, (1,), "in"),)),
        categories=frozenset(("armour_set_check",)),
        definition_order=320,
    ),
    Rac5Locations(
        Rac5ArmourSet.FIRE_BOMB,
        Rac5Planets.POKITARU,
        access_rule(
            combo=ArmourSetCompletion(chestplate=5, helmet=5, gloves=1, boots=5),
            categories=frozenset(("armour_set_check",)),
        ),
        ArmourSetCompletion(chestplate=5, helmet=5, gloves=1, boots=5),
        options=LocationOptions(requirements=(OptionFilter(ArmourSetChecks, (1,), "in"),)),
        categories=frozenset(("armour_set_check",)),
        definition_order=321,
    ),
    Rac5Locations(
        Rac5ArmourSet.HYPERBOREAN,
        Rac5Planets.POKITARU,
        access_rule(
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
        Rac5ArmourSet.ICE_II,
        Rac5Planets.POKITARU,
        access_rule(
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
        Rac5ArmourSet.CHAMELEON,
        Rac5Planets.POKITARU,
        access_rule(
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
        Rac5ArmourSet.STALKER,
        Rac5Planets.POKITARU,
        access_rule(
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
