from rule_builder.options import OptionFilter
from rule_builder.rules import And, Has, HasAll, True_

from .. import constants as C
from ..constants import Rac5Gadgets, Rac5Weapons
from ..options import (
    AllCutscenes,
    AllMissions,
    ChallengeMode,
    ClankChallenges,
    EnableClankChallengeSkillPoints,
    ShrinkRayOptions,
    SkillPoints,
)
from ..rules._helpers import (
    HasChallengeMode,
    HasLongProjectileWeapon,
    HasProjectileWeapon,
    HasTitanPrereq,
    HasClankPack,
)
from .model import Completion, LocationOptions, Rac5CompletionSources, Rac5Locations

_S = Rac5CompletionSources

LOCATIONS = (
    Rac5Locations(
        C.Rac5TBolts.DAYNI_MOON_BARN,
        C.Rac5Planets.DAYNI_MOON,
        lambda world: Has(Rac5Gadgets.SPROUT_O_MATIC) & HasLongProjectileWeapon(),
        Completion(_S.BOLT_BITS, None, 268435456),
        categories=frozenset(("titanium_bolt",)),
        native_planets=(8,),
        definition_order=15,
    ),
    Rac5Locations(
        C.Rac5TBolts.DAYNI_MOON_MIMIC,
        C.Rac5Planets.DAYNI_MOON,
        lambda world: HasAll(Rac5Gadgets.SPROUT_O_MATIC, Rac5Gadgets.SHRINK_RAY) & HasLongProjectileWeapon() & HasClankPack(world),
        Completion(_S.BOLT_BITS, None, 536870912),
        categories=frozenset(("titanium_bolt",)),
        native_planets=(8,),
        definition_order=16,
    ),
    Rac5Locations(
        C.Rac5Locations.DAYNI_MOON_HELMET,
        C.Rac5Planets.DAYNI_MOON,
        lambda world: Has(Rac5Gadgets.SPROUT_O_MATIC) & HasLongProjectileWeapon() & HasClankPack(world),
        Completion(_S.ARMOUR, "mega_bomb", 2),
        categories=frozenset(("armour_pickup",)),
        definition_order=29,
    ),
    Rac5Locations(
        C.Rac5SkillPoints.DAYNI_MOON_GLADIATOR,
        C.Rac5Planets.DAYNI_MOON,
        lambda world: True_(),
        Completion(_S.SKILL_BITS, None, 268435456),
        options=LocationOptions(requirements=(OptionFilter(EnableClankChallengeSkillPoints, (1,), "in"),)),
        categories=frozenset(("skill_point", "clank_challenge_skill_point")),
        native_planets=(8,),
        definition_order=59,
    ),
    Rac5Locations(
        C.Rac5SkillPoints.DAYNI_MOON_WOOL_PROTEST,
        C.Rac5Planets.DAYNI_MOON,
        lambda world: Has(Rac5Gadgets.SPROUT_O_MATIC) & HasLongProjectileWeapon() & HasClankPack(world),
        Completion(_S.SKILL_BITS, None, 536870912),
        options=LocationOptions(requirements=(OptionFilter(SkillPoints, (2,), "in"),)),
        categories=frozenset(("skill_point", "hard_skill_point")),
        native_planets=(8,),
        definition_order=60,
    ),
    Rac5Locations(
        C.Rac5SkillPoints.DAYNI_MOON_BOUNCY,
        C.Rac5Planets.DAYNI_MOON,
        lambda world: Has(Rac5Gadgets.SPROUT_O_MATIC),
        Completion(_S.SKILL_BITS, None, 1073741824),
        options=LocationOptions(requirements=(OptionFilter(SkillPoints, (1, 2), "in"),)),
        categories=frozenset(("skill_point", "easy_skill_point")),
        native_planets=(8,),
        definition_order=61,
    ),
    Rac5Locations(
        C.Rac5CutsceneLocations.DAYNI_MOON,
        C.Rac5Planets.DAYNI_MOON,
        lambda world: Has(Rac5Gadgets.SPROUT_O_MATIC) & HasLongProjectileWeapon() & HasClankPack(world),
        Completion(_S.MISSIONS, 32814034, 8, 8),
        options=LocationOptions(requirements=(OptionFilter(AllMissions, (1,), "in"),)),
        categories=frozenset(("story_mission", "mission")),
        check_order=11,
        definition_order=76,
    ),
    Rac5Locations(
        C.Rac5CutsceneLocations.DAYNI_MOON_LUNA,
        C.Rac5Planets.DAYNI_MOON,
        lambda world: Has(Rac5Gadgets.SPROUT_O_MATIC) & HasLongProjectileWeapon() & HasClankPack(world),
        Completion(_S.MISSIONS, 32814034, 4, 8),
        options=LocationOptions(requirements=(OptionFilter(AllMissions, (1,), "in"),)),
        categories=frozenset(("story_mission", "mission")),
        check_order=12,
        definition_order=77,
    ),
    Rac5Locations(
        C.Rac5CutsceneLocations.DAYNI_MOON_FIGHT1,
        C.Rac5Planets.DAYNI_MOON,
        lambda world: Has(Rac5Gadgets.SPROUT_O_MATIC) & HasLongProjectileWeapon() & HasClankPack(world),
        Completion(_S.MISSIONS, 32814034, 16, 8),
        options=LocationOptions(requirements=(OptionFilter(AllCutscenes, (1,), "in"),)),
        categories=frozenset(("cutscene", "mission")),
        check_order=29,
        definition_order=89,
    ),
    Rac5Locations(
        C.Rac5CutsceneLocations.DAYNI_MOON_FIGHT2,
        C.Rac5Planets.DAYNI_MOON,
        lambda world: Has(Rac5Gadgets.SPROUT_O_MATIC) & HasLongProjectileWeapon() & HasClankPack(world),
        Completion(_S.MISSIONS, 32814034, 2, 8),
        options=LocationOptions(requirements=(OptionFilter(AllCutscenes, (1,), "in"),)),
        categories=frozenset(("cutscene", "mission")),
        check_order=30,
        definition_order=90,
    ),
    Rac5Locations(
        C.Rac5VendorLocations.DAYNI_MOON_SHOCK,
        C.Rac5Planets.DAYNI_MOON,
        lambda world: True_(),
        Completion(_S.EVENTS, C.Rac5VendorLocations.DAYNI_MOON_SHOCK),
        options=LocationOptions(weapon=C.Rac5Weapons.SHOCK_ROCKET),
        categories=frozenset(("weapon_vendor",)),
        weapon="shock_rocket",
        definition_order=112,
    ),
    Rac5Locations(
        C.Rac5VendorLocations.DAYNI_MOON_MAP,
        C.Rac5Planets.DAYNI_MOON,
        lambda world: True_(),
        Completion(_S.EVENTS, C.Rac5VendorLocations.DAYNI_MOON_MAP),
        categories=frozenset(("gadget_vendor",)),
        gadget="map_o_matic",
        definition_order=118,
    ),
    Rac5Locations(
        C.Rac5TitanVendorLocations.DAYNI_MOON_MOOTATOR_TITAN,
        C.Rac5Planets.DAYNI_MOON,
        lambda world: HasTitanPrereq(world, Rac5Weapons.MOOTATOR) & HasChallengeMode(world, 1),
        Completion(_S.EVENTS, C.Rac5TitanVendorLocations.DAYNI_MOON_MOOTATOR_TITAN),
        options=LocationOptions(
            requirements=(OptionFilter(ChallengeMode, (1, 2), "in"),), weapon=C.Rac5Weapons.MOOTATOR
        ),
        categories=frozenset(("weapon_titan_vendor",)),
        weapon="mootator",
        definition_order=152,
    ),
    Rac5Locations(
        C.Rac5TitanVendorLocations.DAYNI_MOON_SHOCK_TITAN,
        C.Rac5Planets.DAYNI_MOON,
        lambda world: HasChallengeMode(world, 1),
        Completion(_S.EVENTS, C.Rac5TitanVendorLocations.DAYNI_MOON_SHOCK_TITAN),
        options=LocationOptions(
            requirements=(OptionFilter(ChallengeMode, (1, 2), "in"),), weapon=C.Rac5Weapons.SHOCK_ROCKET
        ),
        categories=frozenset(("weapon_titan_vendor",)),
        weapon="shock_rocket",
        definition_order=153,
    ),
    Rac5Locations(
        C.Rac5ClankChallenges.DAYNI_MOON_SHOWDOWN,
        C.Rac5Planets.DAYNI_MOON,
        lambda world: True_(),
        Completion(_S.CHALLENGES, 32814079, increasing=True),
        options=LocationOptions(
            requirements=(OptionFilter(ClankChallenges, (1, 2), "in"),), challenge_group="Gadgetbot Toss"
        ),
        categories=frozenset(("challenge",)),
        check_order=4,
        definition_order=330,
    ),
    Rac5Locations(
        C.Rac5ClankChallenges.DAYNI_MOON_INFINITE,
        C.Rac5Planets.DAYNI_MOON,
        lambda world: True_(),
        Completion(_S.CHALLENGES, 32814084, increasing=True),
        options=LocationOptions(
            requirements=(OptionFilter(ClankChallenges, (1, 2), "in"),), challenge_group="Gadgetbot"
        ),
        categories=frozenset(("challenge",)),
        check_order=5,
        definition_order=331,
    ),
    Rac5Locations(
        C.Rac5ClankChallenges.DAYNI_MOON_WELCOME,
        C.Rac5Planets.DAYNI_MOON,
        lambda world: True_(),
        Completion(_S.CHALLENGES, 32814070, increasing=True),
        options=LocationOptions(
            requirements=(OptionFilter(ClankChallenges, (2,), "in"),), challenge_group="Demolition Derby"
        ),
        categories=frozenset(("all_clank",)),
        check_order=9,
        definition_order=335,
    ),
    Rac5Locations(
        C.Rac5ClankChallenges.DAYNI_MOON_ROUND,
        C.Rac5Planets.DAYNI_MOON,
        lambda world: True_(),
        Completion(_S.CHALLENGES, 32814071, increasing=True),
        options=LocationOptions(
            requirements=(OptionFilter(ClankChallenges, (2,), "in"),), challenge_group="Demolition Derby"
        ),
        categories=frozenset(("all_clank",)),
        check_order=10,
        definition_order=336,
    ),
    Rac5Locations(
        C.Rac5ClankChallenges.DAYNI_MOON_VARIETY,
        C.Rac5Planets.DAYNI_MOON,
        lambda world: True_(),
        Completion(_S.CHALLENGES, 32814072, increasing=True),
        options=LocationOptions(
            requirements=(OptionFilter(ClankChallenges, (2,), "in"),), challenge_group="Demolition Derby"
        ),
        categories=frozenset(("all_clank",)),
        check_order=11,
        definition_order=337,
    ),
    Rac5Locations(
        C.Rac5ClankChallenges.DAYNI_MOON_SAWYER,
        C.Rac5Planets.DAYNI_MOON,
        lambda world: True_(),
        Completion(_S.CHALLENGES, 32814073, increasing=True),
        options=LocationOptions(
            requirements=(OptionFilter(ClankChallenges, (2,), "in"),), challenge_group="Demolition Derby"
        ),
        categories=frozenset(("all_clank",)),
        check_order=12,
        definition_order=338,
    ),
    Rac5Locations(
        C.Rac5ClankChallenges.DAYNI_MOON_SMASHER,
        C.Rac5Planets.DAYNI_MOON,
        lambda world: True_(),
        Completion(_S.CHALLENGES, 32814074, increasing=True),
        options=LocationOptions(
            requirements=(OptionFilter(ClankChallenges, (2,), "in"),), challenge_group="Demolition Derby"
        ),
        categories=frozenset(("all_clank",)),
        check_order=13,
        definition_order=339,
    ),
    Rac5Locations(
        C.Rac5ClankChallenges.DAYNI_MOON_HAY,
        C.Rac5Planets.DAYNI_MOON,
        lambda world: True_(),
        Completion(_S.CHALLENGES, 32814075, increasing=True),
        options=LocationOptions(
            requirements=(OptionFilter(ClankChallenges, (2,), "in"),), challenge_group="Gadgetbot Toss"
        ),
        categories=frozenset(("all_clank",)),
        check_order=18,
        definition_order=344,
    ),
    Rac5Locations(
        C.Rac5ClankChallenges.DAYNI_MOON_TOURNAMENT,
        C.Rac5Planets.DAYNI_MOON,
        lambda world: True_(),
        Completion(_S.CHALLENGES, 32814076, increasing=True),
        options=LocationOptions(
            requirements=(OptionFilter(ClankChallenges, (2,), "in"),), challenge_group="Gadgetbot Toss"
        ),
        categories=frozenset(("all_clank",)),
        check_order=19,
        definition_order=345,
    ),
    Rac5Locations(
        C.Rac5ClankChallenges.DAYNI_MOON_AROUND,
        C.Rac5Planets.DAYNI_MOON,
        lambda world: True_(),
        Completion(_S.CHALLENGES, 32814077, increasing=True),
        options=LocationOptions(
            requirements=(OptionFilter(ClankChallenges, (2,), "in"),), challenge_group="Gadgetbot Toss"
        ),
        categories=frozenset(("all_clank",)),
        check_order=20,
        definition_order=346,
    ),
    Rac5Locations(
        C.Rac5ClankChallenges.DAYNI_MOON_LINE,
        C.Rac5Planets.DAYNI_MOON,
        lambda world: True_(),
        Completion(_S.CHALLENGES, 32814078, increasing=True),
        options=LocationOptions(
            requirements=(OptionFilter(ClankChallenges, (2,), "in"),), challenge_group="Gadgetbot Toss"
        ),
        categories=frozenset(("all_clank",)),
        check_order=21,
        definition_order=347,
    ),
    Rac5Locations(
        C.Rac5ClankChallenges.DAYNI_MOON_CROWD,
        C.Rac5Planets.DAYNI_MOON,
        lambda world: True_(),
        Completion(_S.CHALLENGES, 32814080, increasing=True),
        options=LocationOptions(requirements=(OptionFilter(ClankChallenges, (2,), "in"),), challenge_group="Gadgetbot"),
        categories=frozenset(("all_clank",)),
        check_order=26,
        definition_order=352,
    ),
    Rac5Locations(
        C.Rac5ClankChallenges.DAYNI_MOON_REVERSE,
        C.Rac5Planets.DAYNI_MOON,
        lambda world: True_(),
        Completion(_S.CHALLENGES, 32814081, increasing=True),
        options=LocationOptions(requirements=(OptionFilter(ClankChallenges, (2,), "in"),), challenge_group="Gadgetbot"),
        categories=frozenset(("all_clank",)),
        check_order=27,
        definition_order=353,
    ),
    Rac5Locations(
        C.Rac5ClankChallenges.DAYNI_MOON_BRIDGE,
        C.Rac5Planets.DAYNI_MOON,
        lambda world: True_(),
        Completion(_S.CHALLENGES, 32814082, increasing=True),
        options=LocationOptions(requirements=(OptionFilter(ClankChallenges, (2,), "in"),), challenge_group="Gadgetbot"),
        categories=frozenset(("all_clank",)),
        check_order=28,
        definition_order=354,
    ),
    Rac5Locations(
        C.Rac5ClankChallenges.DAYNI_MOON_LEAP,
        C.Rac5Planets.DAYNI_MOON,
        lambda world: True_(),
        Completion(_S.CHALLENGES, 32814083, increasing=True),
        options=LocationOptions(requirements=(OptionFilter(ClankChallenges, (2,), "in"),), challenge_group="Gadgetbot"),
        categories=frozenset(("all_clank",)),
        check_order=29,
        definition_order=355,
    ),
    Rac5Locations(
        C.Rac5ShrinkRayGrindrail.DAYNI_MOON_TITANIUM_BOLT_ENTRANCE,
        C.Rac5Planets.DAYNI_MOON,
        lambda world: And(
            HasAll(Rac5Gadgets.SHRINK_RAY, Rac5Gadgets.SPROUT_O_MATIC),
            HasProjectileWeapon(),
            HasClankPack(world)
        ),
        Completion(_S.EVENTS, C.Rac5ShrinkRayGrindrail.DAYNI_MOON_TITANIUM_BOLT_ENTRANCE),
        options=LocationOptions(requirements=(OptionFilter(ShrinkRayOptions, (1,), "in"),)),
        categories=frozenset(("shrink_ray_skip",)),
        definition_order=367,
    ),
)
