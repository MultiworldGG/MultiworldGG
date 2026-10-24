from rule_builder.options import OptionFilter
from rule_builder.rules import HasAll, True_

from ..constants import (
    Rac5ClankChallenges,
    Rac5CutsceneLocations,
    Rac5Gadgets,
    Rac5Locations as Rac5LocationNames,
    Rac5Planets,
    Rac5SkillPoints,
    Rac5TBolts,
)
from ..constants.options import Rac5Options
from ..options import (
    AllCutscenes,
    AllMissions,
    ClankChallenges,
    EnableClankChallengeSkillPoints,
    GiantClank,
    SkillPoints,
)
from ..rules._helpers import HasClankPack
from .model import Completion, LocationOptions, Rac5CompletionSources, Rac5Locations

_S = Rac5CompletionSources

LOCATIONS = (
    Rac5Locations(
        Rac5TBolts.METALIS_DOOR,
        Rac5Planets.METALIS,
        HasAll(Rac5Gadgets.POLARIZER, Rac5Gadgets.HYPERSHOT) & HasClankPack(),
        Completion(_S.BOLT_BITS, None, 4096),
        categories=frozenset(("titanium_bolt",)),
        native_planets=(4,),
        definition_order=7,
    ),
    Rac5Locations(
        Rac5LocationNames.METALIS_GLOVES,
        Rac5Planets.METALIS,
        True_(),
        Completion(_S.ARMOUR, "electroshock", 4),
        options=LocationOptions(requirements=(OptionFilter(GiantClank, (1,), "in"),)),
        categories=frozenset(("armour_pickup", Rac5Options.GIANT_CLANK)),
        definition_order=31,
    ),
    Rac5Locations(
        Rac5SkillPoints.METALIS_SHUTOUT,
        Rac5Planets.METALIS,
        True_(),
        Completion(_S.SKILL_BITS, None, 4096),
        options=LocationOptions(requirements=(OptionFilter(EnableClankChallengeSkillPoints, (1,), "in"),)),
        categories=frozenset(("skill_point", "clank_challenge_skill_point")),
        native_planets=(4,),
        definition_order=53,
    ),
    Rac5Locations(
        Rac5SkillPoints.METALIS_GLADIATOR,
        Rac5Planets.METALIS,
        True_(),
        Completion(_S.SKILL_BITS, None, 16384),
        options=LocationOptions(requirements=(OptionFilter(EnableClankChallengeSkillPoints, (1,), "in"),)),
        categories=frozenset(("skill_point", "clank_challenge_skill_point")),
        native_planets=(4,),
        definition_order=54,
    ),
    Rac5Locations(
        Rac5SkillPoints.METALIS_TERROR,
        Rac5Planets.METALIS,
        True_(),
        Completion(_S.SKILL_BITS, None, 8192),
        options=LocationOptions(
            requirements=(
                OptionFilter(GiantClank, (1,), "in"),
                OptionFilter(SkillPoints, (2,), "in"),
            )
        ),
        categories=frozenset((Rac5Options.GIANT_CLANK, "skill_point", "hard_skill_point")),
        native_planets=(4,),
        definition_order=66,
    ),
    Rac5Locations(
        Rac5CutsceneLocations.METALIS_WAR,
        Rac5Planets.METALIS,
        True_(),
        Completion(_S.MISSIONS, 32814026, 2, 4),
        options=LocationOptions(
            requirements=(
                OptionFilter(AllMissions, (1,), "in"),
                OptionFilter(ClankChallenges, (1, 2), "in"),
            )
        ),
        categories=frozenset(("story_mission", "mission")),
        check_order=7,
        definition_order=72,
    ),
    Rac5Locations(
        Rac5CutsceneLocations.METALIS_ESCAPE,
        Rac5Planets.METALIS,
        True_(),
        Completion(_S.EVENTS, Rac5CutsceneLocations.METALIS_ESCAPE),
        options=LocationOptions(
            requirements=(
                OptionFilter(GiantClank, (1,), "in"),
                OptionFilter(AllMissions, (1,), "in"),
            )
        ),
        categories=frozenset((Rac5Options.GIANT_CLANK, "story_mission", "mission")),
        definition_order=81,
    ),
    Rac5Locations(
        Rac5CutsceneLocations.METALIS_ENTER,
        Rac5Planets.METALIS,
        True_(),
        Completion(_S.MISSIONS, 32814026, 1, 4),
        options=LocationOptions(requirements=(OptionFilter(AllCutscenes, (1,), "in"),)),
        categories=frozenset(("cutscene", "mission")),
        check_order=20,
        definition_order=97,
    ),
    Rac5Locations(
        Rac5ClankChallenges.METALIS_BUZZSAW,
        Rac5Planets.METALIS,
        True_(),
        Completion(_S.CHALLENGES, 32814046, increasing=True),
        options=LocationOptions(
            requirements=(OptionFilter(ClankChallenges, (1, 2), "in"),), challenge_group="Demolition Derby"
        ),
        categories=frozenset(("challenge",)),
        check_order=0,
        definition_order=326,
    ),
    Rac5Locations(
        Rac5ClankChallenges.METALIS_REVENGE,
        Rac5Planets.METALIS,
        True_(),
        Completion(_S.CHALLENGES, 32814050, increasing=True),
        options=LocationOptions(
            requirements=(OptionFilter(ClankChallenges, (1, 2), "in"),), challenge_group="Demolition Derby"
        ),
        categories=frozenset(("challenge",)),
        check_order=1,
        definition_order=327,
    ),
    Rac5Locations(
        Rac5ClankChallenges.METALIS_UBER,
        Rac5Planets.METALIS,
        True_(),
        Completion(_S.CHALLENGES, 32814055, increasing=True),
        options=LocationOptions(
            requirements=(OptionFilter(ClankChallenges, (1, 2), "in"),), challenge_group="Gadgetbot Toss"
        ),
        categories=frozenset(("challenge",)),
        check_order=2,
        definition_order=328,
    ),
    Rac5Locations(
        Rac5ClankChallenges.METALIS_NIGHT,
        Rac5Planets.METALIS,
        True_(),
        Completion(_S.CHALLENGES, 32814060, increasing=True),
        options=LocationOptions(
            requirements=(OptionFilter(ClankChallenges, (1, 2), "in"),), challenge_group="Gadgetbot"
        ),
        categories=frozenset(("challenge",)),
        check_order=3,
        definition_order=329,
    ),
    Rac5Locations(
        Rac5ClankChallenges.METALIS_CHARGE,
        Rac5Planets.METALIS,
        True_(),
        Completion(_S.CHALLENGES, 32814047, increasing=True),
        options=LocationOptions(
            requirements=(OptionFilter(ClankChallenges, (2,), "in"),), challenge_group="Demolition Derby"
        ),
        categories=frozenset(("all_clank",)),
        check_order=6,
        definition_order=332,
    ),
    Rac5Locations(
        Rac5ClankChallenges.METALIS_BOOGALOO,
        Rac5Planets.METALIS,
        True_(),
        Completion(_S.CHALLENGES, 32814048, increasing=True),
        options=LocationOptions(
            requirements=(OptionFilter(ClankChallenges, (2,), "in"),), challenge_group="Demolition Derby"
        ),
        categories=frozenset(("all_clank",)),
        check_order=7,
        definition_order=333,
    ),
    Rac5Locations(
        Rac5ClankChallenges.METALIS_SHOWDOWN,
        Rac5Planets.METALIS,
        True_(),
        Completion(_S.CHALLENGES, 32814049, increasing=True),
        options=LocationOptions(
            requirements=(OptionFilter(ClankChallenges, (2,), "in"),), challenge_group="Demolition Derby"
        ),
        categories=frozenset(("all_clank",)),
        check_order=8,
        definition_order=334,
    ),
    Rac5Locations(
        Rac5ClankChallenges.METALIS_LEAGUE,
        Rac5Planets.METALIS,
        True_(),
        Completion(_S.CHALLENGES, 32814051, increasing=True),
        options=LocationOptions(
            requirements=(OptionFilter(ClankChallenges, (2,), "in"),), challenge_group="Gadgetbot Toss"
        ),
        categories=frozenset(("all_clank",)),
        check_order=14,
        definition_order=340,
    ),
    Rac5Locations(
        Rac5ClankChallenges.METALIS_BRACKET,
        Rac5Planets.METALIS,
        True_(),
        Completion(_S.CHALLENGES, 32814052, increasing=True),
        options=LocationOptions(
            requirements=(OptionFilter(ClankChallenges, (2,), "in"),), challenge_group="Gadgetbot Toss"
        ),
        categories=frozenset(("all_clank",)),
        check_order=15,
        definition_order=341,
    ),
    Rac5Locations(
        Rac5ClankChallenges.METALIS_DIVISION,
        Rac5Planets.METALIS,
        True_(),
        Completion(_S.CHALLENGES, 32814053, increasing=True),
        options=LocationOptions(
            requirements=(OptionFilter(ClankChallenges, (2,), "in"),), challenge_group="Gadgetbot Toss"
        ),
        categories=frozenset(("all_clank",)),
        check_order=16,
        definition_order=342,
    ),
    Rac5Locations(
        Rac5ClankChallenges.METALIS_PROFESSIONAL,
        Rac5Planets.METALIS,
        True_(),
        Completion(_S.CHALLENGES, 32814054, increasing=True),
        options=LocationOptions(
            requirements=(OptionFilter(ClankChallenges, (2,), "in"),), challenge_group="Gadgetbot Toss"
        ),
        categories=frozenset(("all_clank",)),
        check_order=17,
        definition_order=343,
    ),
    Rac5Locations(
        Rac5ClankChallenges.METALLIS_TEAM,
        Rac5Planets.METALIS,
        True_(),
        Completion(_S.CHALLENGES, 32814056, increasing=True),
        options=LocationOptions(requirements=(OptionFilter(ClankChallenges, (2,), "in"),), challenge_group="Gadgetbot"),
        categories=frozenset(("all_clank",)),
        check_order=22,
        definition_order=348,
    ),
    Rac5Locations(
        Rac5ClankChallenges.METALIS_GAP,
        Rac5Planets.METALIS,
        True_(),
        Completion(_S.CHALLENGES, 32814057, increasing=True),
        options=LocationOptions(requirements=(OptionFilter(ClankChallenges, (2,), "in"),), challenge_group="Gadgetbot"),
        categories=frozenset(("all_clank",)),
        check_order=23,
        definition_order=349,
    ),
    Rac5Locations(
        Rac5ClankChallenges.METALIS_TELEPORTERS,
        Rac5Planets.METALIS,
        True_(),
        Completion(_S.CHALLENGES, 32814058, increasing=True),
        options=LocationOptions(requirements=(OptionFilter(ClankChallenges, (2,), "in"),), challenge_group="Gadgetbot"),
        categories=frozenset(("all_clank",)),
        check_order=24,
        definition_order=350,
    ),
    Rac5Locations(
        Rac5ClankChallenges.METALIS_BRAIN,
        Rac5Planets.METALIS,
        True_(),
        Completion(_S.CHALLENGES, 32814059, increasing=True),
        options=LocationOptions(requirements=(OptionFilter(ClankChallenges, (2,), "in"),), challenge_group="Gadgetbot"),
        categories=frozenset(("all_clank",)),
        check_order=25,
        definition_order=351,
    ),
)
