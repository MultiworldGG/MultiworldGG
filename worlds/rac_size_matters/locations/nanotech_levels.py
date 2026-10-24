from rule_builder.options import OptionFilter
from rule_builder.rules import Rule

from ..options import ChallengeMode, NanotechExperienceMultiplier
from ..rules._helpers import HasChallengeMode, HasExpAccess, HasGoodExpPlanet
from .model import Completion, LocationOptions, Rac5Categories, Rac5CompletionSources, Rac5Locations

# The player starts at Nanotech Level 5; levels above 50 only exist in Challenge Mode.
FIRST_LEVEL = 6
LAST_NORMAL_LEVEL = 50
LAST_LEVEL = 75
FIRST_DEFINITION_ORDER = 243


def access_rule(level: int) -> Rule:
    rule = HasExpAccess()
    if level > 20:
        # Higher multipliers level fast enough anywhere.
        rule &= HasGoodExpPlanet(options=[OptionFilter(NanotechExperienceMultiplier, 8, "le")], filtered_resolution=True)
    if level > LAST_NORMAL_LEVEL:
        rule &= HasChallengeMode(1)
    return rule


def _location(level: int) -> Rac5Locations:
    challenge_mode = level > LAST_NORMAL_LEVEL
    return Rac5Locations(
        f"Nanotech Level: {level}",
        "Menu",
        access_rule(level),
        Completion(Rac5CompletionSources.NANOTECH_LEVELS, level),
        options=LocationOptions(
            requirements=(OptionFilter(ChallengeMode, (1, 2), "in"),) if challenge_mode else (),
            nanotech_level=level,
        ),
        categories=frozenset(
            (Rac5Categories.NANOTECH_LEVEL, Rac5Categories.CHALLENGE_MODE_NANOTECH_LEVEL)
            if challenge_mode
            else (Rac5Categories.NANOTECH_LEVEL,)
        ),
        level=level,
        definition_order=FIRST_DEFINITION_ORDER + level - FIRST_LEVEL,
    )


LOCATIONS = tuple(_location(level) for level in range(FIRST_LEVEL, LAST_LEVEL + 1))
