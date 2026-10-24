from rule_builder.options import OptionFilter
from rule_builder.rules import Has, True_

from ..constants import (
    Rac5ClankChallenges,
    Rac5Gadgets,
    Rac5Locations as Rac5LocationNames,
    Rac5Planets,
    Rac5ShrinkRayGrindrail,
)
from ..data.challenges import CHALLENGE_GROUP_GADGETBOT
from ..options import ClankChallenges, EnableHIGTreehouse, ShrinkRayOptions, SkillPoints
from ..rules._helpers import CanReachAllSkillPoints
from .model import BASE_ID, Completion, LocationOptions, Rac5Categories, Rac5Locations

CHALLENGE_NAMES = (
    Rac5ClankChallenges.HIG_TREEHOUSE_1,
    Rac5ClankChallenges.HIG_TREEHOUSE_2,
    Rac5ClankChallenges.HIG_TREEHOUSE_3,
    Rac5ClankChallenges.HIG_TREEHOUSE_4,
)


# The arena table selects save-byte IDs 148 onward for Treehouse's Gadgetbot
# section. Save byte IDs are relative to the canonical save block + 0x8C0.
LOCATIONS = tuple(
    Rac5Locations(
        name, Rac5Planets.HIG_TREEHOUSE, True_(),
        Completion("challenges", 0x1F4B454 + index, increasing=True),
        code=BASE_ID + 375 + index,
        options=LocationOptions(
            requirements=(OptionFilter(EnableHIGTreehouse, 1), OptionFilter(ClankChallenges, (1, 2), "in")),
            challenge_group=CHALLENGE_GROUP_GADGETBOT,
        ),
        categories=frozenset(("challenge",)),
        check_order=30 + index, definition_order=375 + index,
    )
    for index, name in enumerate(CHALLENGE_NAMES)
) + (
    Rac5Locations(
        Rac5ShrinkRayGrindrail.HIG_TREEHOUSE_GRINDRAIL, Rac5Planets.HIG_TREEHOUSE,
        Has(Rac5Gadgets.SHRINK_RAY),
        Completion("events", Rac5ShrinkRayGrindrail.HIG_TREEHOUSE_GRINDRAIL),
        code=BASE_ID + 380,
        options=LocationOptions(requirements=(OptionFilter(EnableHIGTreehouse, 1),
                                             OptionFilter(ShrinkRayOptions, 1))),
        categories=frozenset(("shrink_ray_skip",)),
        native_planets=(24,), definition_order=380,
    ),
    Rac5Locations(
        Rac5LocationNames.HIG_TREEHOUSE_ALL_SKILL_POINTS, Rac5Planets.HIG_TREEHOUSE,
        CanReachAllSkillPoints(),
        Completion("events", Rac5LocationNames.HIG_TREEHOUSE_ALL_SKILL_POINTS),
        code=BASE_ID + 381,
        options=LocationOptions(requirements=(OptionFilter(EnableHIGTreehouse, 1),
                                             OptionFilter(SkillPoints, (1, 2), "in"))),
        categories=frozenset((Rac5Categories.ALL_SKILL_POINTS,)),
        definition_order=381,
    ),
)

