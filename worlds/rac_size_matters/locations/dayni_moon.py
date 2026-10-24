from rule_builder.options import OptionFilter
from rule_builder.rules import And, Has, HasAll, True_

from ..constants import (
    Rac5ClankChallenges,
    Rac5CutsceneLocations,
    Rac5Gadgets,
    Rac5Locations as Rac5LocationNames,
    Rac5Planets,
    Rac5ShrinkRayGrindrail,
    Rac5SkillPoints,
    Rac5TBolts,
    Rac5TitanVendorLocations,
    Rac5VendorLocations,
    Rac5Weapons,
)
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
    HasClankPack,
    HasLongProjectileWeapon,
    HasProjectileWeapon,
    HasWeaponLevel,
)
from .model import Completion, LocationOptions, Rac5CompletionSources, Rac5Locations

_S = Rac5CompletionSources

LOCATIONS = (
    Rac5Locations(
        Rac5TBolts.DAYNI_MOON_BARN,
        Rac5Planets.DAYNI_MOON,
        Has(Rac5Gadgets.SPROUT_O_MATIC) & HasLongProjectileWeapon(),
        Completion(_S.BOLT_BITS, None, 268435456),
        categories=frozenset(("titanium_bolt",)),
        native_planets=(8,),
        definition_order=15,
    ),
    Rac5Locations(
        Rac5TBolts.DAYNI_MOON_MIMIC,
        Rac5Planets.DAYNI_MOON,
        HasAll(Rac5Gadgets.SPROUT_O_MATIC, Rac5Gadgets.SHRINK_RAY) & HasLongProjectileWeapon() & HasClankPack(),
        Completion(_S.BOLT_BITS, None, 536870912),
        categories=frozenset(("titanium_bolt",)),
        native_planets=(8,),
        definition_order=16,
    ),
    Rac5Locations(
        Rac5LocationNames.DAYNI_MOON_HELMET,
        Rac5Planets.DAYNI_MOON,
        Has(Rac5Gadgets.SPROUT_O_MATIC) & HasLongProjectileWeapon() & HasClankPack(),
        Completion(_S.ARMOUR, "mega_bomb", 2),
        categories=frozenset(("armour_pickup",)),
        definition_order=29,
    ),
    Rac5Locations(
        Rac5SkillPoints.DAYNI_MOON_GLADIATOR,
        Rac5Planets.DAYNI_MOON,
        True_(),
        Completion(_S.SKILL_BITS, None, 268435456),
        options=LocationOptions(requirements=(OptionFilter(EnableClankChallengeSkillPoints, (1,), "in"),)),
        categories=frozenset(("skill_point", "clank_challenge_skill_point")),
        native_planets=(8,),
        definition_order=59,
    ),
    Rac5Locations(
        Rac5SkillPoints.DAYNI_MOON_WOOL_PROTEST,
        Rac5Planets.DAYNI_MOON,
        Has(Rac5Gadgets.SPROUT_O_MATIC) & HasLongProjectileWeapon() & HasClankPack(),
        Completion(_S.SKILL_BITS, None, 536870912),
        options=LocationOptions(requirements=(OptionFilter(SkillPoints, (2,), "in"),)),
        categories=frozenset(("skill_point", "hard_skill_point")),
        native_planets=(8,),
        definition_order=60,
    ),
    Rac5Locations(
        Rac5SkillPoints.DAYNI_MOON_BOUNCY,
        Rac5Planets.DAYNI_MOON,
        Has(Rac5Gadgets.SPROUT_O_MATIC),
        Completion(_S.SKILL_BITS, None, 1073741824),
        options=LocationOptions(requirements=(OptionFilter(SkillPoints, (1, 2), "in"),)),
        categories=frozenset(("skill_point", "easy_skill_point")),
        native_planets=(8,),
        definition_order=61,
    ),
    Rac5Locations(
        Rac5CutsceneLocations.DAYNI_MOON,
        Rac5Planets.DAYNI_MOON,
        Has(Rac5Gadgets.SPROUT_O_MATIC) & HasLongProjectileWeapon() & HasClankPack(),
        Completion(_S.MISSIONS, 32814034, 8, 8),
        options=LocationOptions(requirements=(OptionFilter(AllMissions, (1,), "in"),)),
        categories=frozenset(("story_mission", "mission")),
        check_order=11,
        definition_order=76,
    ),
    Rac5Locations(
        Rac5CutsceneLocations.DAYNI_MOON_LUNA,
        Rac5Planets.DAYNI_MOON,
        Has(Rac5Gadgets.SPROUT_O_MATIC) & HasLongProjectileWeapon() & HasClankPack(),
        Completion(_S.MISSIONS, 32814034, 4, 8),
        options=LocationOptions(requirements=(OptionFilter(AllMissions, (1,), "in"),)),
        categories=frozenset(("story_mission", "mission")),
        check_order=12,
        definition_order=77,
    ),
    Rac5Locations(
        Rac5CutsceneLocations.DAYNI_MOON_FIGHT1,
        Rac5Planets.DAYNI_MOON,
        Has(Rac5Gadgets.SPROUT_O_MATIC) & HasLongProjectileWeapon() & HasClankPack(),
        Completion(_S.MISSIONS, 32814034, 16, 8),
        options=LocationOptions(requirements=(OptionFilter(AllCutscenes, (1,), "in"),)),
        categories=frozenset(("cutscene", "mission")),
        check_order=29,
        definition_order=89,
    ),
    Rac5Locations(
        Rac5CutsceneLocations.DAYNI_MOON_FIGHT2,
        Rac5Planets.DAYNI_MOON,
        Has(Rac5Gadgets.SPROUT_O_MATIC) & HasLongProjectileWeapon() & HasClankPack(),
        Completion(_S.MISSIONS, 32814034, 2, 8),
        options=LocationOptions(requirements=(OptionFilter(AllCutscenes, (1,), "in"),)),
        categories=frozenset(("cutscene", "mission")),
        check_order=30,
        definition_order=90,
    ),
    Rac5Locations(
        Rac5VendorLocations.DAYNI_MOON_SHOCK,
        Rac5Planets.DAYNI_MOON,
        True_(),
        Completion(_S.EVENTS, Rac5VendorLocations.DAYNI_MOON_SHOCK),
        options=LocationOptions(weapon=Rac5Weapons.SHOCK_ROCKET),
        categories=frozenset(("weapon_vendor",)),
        weapon=Rac5Weapons.SHOCK_ROCKET,
        definition_order=112,
    ),
    Rac5Locations(
        Rac5VendorLocations.DAYNI_MOON_MAP,
        Rac5Planets.DAYNI_MOON,
        True_(),
        Completion(_S.EVENTS, Rac5VendorLocations.DAYNI_MOON_MAP),
        categories=frozenset(("gadget_vendor",)),
        gadget=Rac5Gadgets.MAP_O_MATIC,
        definition_order=118,
    ),
    Rac5Locations(
        Rac5TitanVendorLocations.DAYNI_MOON_MOOTATOR_TITAN,
        Rac5Planets.DAYNI_MOON,
        # Reaching V4 is what unlocks the Titan purchase in-game; buying it floors the weapon to V5.
        HasWeaponLevel(Rac5Weapons.MOOTATOR, 4) & HasChallengeMode(1),
        Completion(_S.EVENTS, Rac5TitanVendorLocations.DAYNI_MOON_MOOTATOR_TITAN),
        options=LocationOptions(
            requirements=(OptionFilter(ChallengeMode, (1, 2), "in"),), weapon=Rac5Weapons.MOOTATOR
        ),
        categories=frozenset(("weapon_titan_vendor",)),
        weapon=Rac5Weapons.MOOTATOR,
        definition_order=152,
    ),
    Rac5Locations(
        Rac5TitanVendorLocations.DAYNI_MOON_SHOCK_TITAN,
        Rac5Planets.DAYNI_MOON,
        HasChallengeMode(1),
        Completion(_S.EVENTS, Rac5TitanVendorLocations.DAYNI_MOON_SHOCK_TITAN),
        options=LocationOptions(
            requirements=(OptionFilter(ChallengeMode, (1, 2), "in"),), weapon=Rac5Weapons.SHOCK_ROCKET
        ),
        categories=frozenset(("weapon_titan_vendor",)),
        weapon=Rac5Weapons.SHOCK_ROCKET,
        definition_order=153,
    ),
    Rac5Locations(
        Rac5ClankChallenges.DAYNI_MOON_SHOWDOWN,
        Rac5Planets.DAYNI_MOON,
        True_(),
        Completion(_S.CHALLENGES, 32814079, increasing=True),
        options=LocationOptions(
            requirements=(OptionFilter(ClankChallenges, (1, 2), "in"),), challenge_group="Gadgetbot Toss"
        ),
        categories=frozenset(("challenge",)),
        check_order=4,
        definition_order=330,
    ),
    Rac5Locations(
        Rac5ClankChallenges.DAYNI_MOON_INFINITE,
        Rac5Planets.DAYNI_MOON,
        True_(),
        Completion(_S.CHALLENGES, 32814084, increasing=True),
        options=LocationOptions(
            requirements=(OptionFilter(ClankChallenges, (1, 2), "in"),), challenge_group="Gadgetbot"
        ),
        categories=frozenset(("challenge",)),
        check_order=5,
        definition_order=331,
    ),
    Rac5Locations(
        Rac5ClankChallenges.DAYNI_MOON_WELCOME,
        Rac5Planets.DAYNI_MOON,
        True_(),
        Completion(_S.CHALLENGES, 32814070, increasing=True),
        options=LocationOptions(
            requirements=(OptionFilter(ClankChallenges, (2,), "in"),), challenge_group="Demolition Derby"
        ),
        categories=frozenset(("all_clank",)),
        check_order=9,
        definition_order=335,
    ),
    Rac5Locations(
        Rac5ClankChallenges.DAYNI_MOON_ROUND,
        Rac5Planets.DAYNI_MOON,
        True_(),
        Completion(_S.CHALLENGES, 32814071, increasing=True),
        options=LocationOptions(
            requirements=(OptionFilter(ClankChallenges, (2,), "in"),), challenge_group="Demolition Derby"
        ),
        categories=frozenset(("all_clank",)),
        check_order=10,
        definition_order=336,
    ),
    Rac5Locations(
        Rac5ClankChallenges.DAYNI_MOON_VARIETY,
        Rac5Planets.DAYNI_MOON,
        True_(),
        Completion(_S.CHALLENGES, 32814072, increasing=True),
        options=LocationOptions(
            requirements=(OptionFilter(ClankChallenges, (2,), "in"),), challenge_group="Demolition Derby"
        ),
        categories=frozenset(("all_clank",)),
        check_order=11,
        definition_order=337,
    ),
    Rac5Locations(
        Rac5ClankChallenges.DAYNI_MOON_SAWYER,
        Rac5Planets.DAYNI_MOON,
        True_(),
        Completion(_S.CHALLENGES, 32814073, increasing=True),
        options=LocationOptions(
            requirements=(OptionFilter(ClankChallenges, (2,), "in"),), challenge_group="Demolition Derby"
        ),
        categories=frozenset(("all_clank",)),
        check_order=12,
        definition_order=338,
    ),
    Rac5Locations(
        Rac5ClankChallenges.DAYNI_MOON_SMASHER,
        Rac5Planets.DAYNI_MOON,
        True_(),
        Completion(_S.CHALLENGES, 32814074, increasing=True),
        options=LocationOptions(
            requirements=(OptionFilter(ClankChallenges, (2,), "in"),), challenge_group="Demolition Derby"
        ),
        categories=frozenset(("all_clank",)),
        check_order=13,
        definition_order=339,
    ),
    Rac5Locations(
        Rac5ClankChallenges.DAYNI_MOON_HAY,
        Rac5Planets.DAYNI_MOON,
        True_(),
        Completion(_S.CHALLENGES, 32814075, increasing=True),
        options=LocationOptions(
            requirements=(OptionFilter(ClankChallenges, (2,), "in"),), challenge_group="Gadgetbot Toss"
        ),
        categories=frozenset(("all_clank",)),
        check_order=18,
        definition_order=344,
    ),
    Rac5Locations(
        Rac5ClankChallenges.DAYNI_MOON_TOURNAMENT,
        Rac5Planets.DAYNI_MOON,
        True_(),
        Completion(_S.CHALLENGES, 32814076, increasing=True),
        options=LocationOptions(
            requirements=(OptionFilter(ClankChallenges, (2,), "in"),), challenge_group="Gadgetbot Toss"
        ),
        categories=frozenset(("all_clank",)),
        check_order=19,
        definition_order=345,
    ),
    Rac5Locations(
        Rac5ClankChallenges.DAYNI_MOON_AROUND,
        Rac5Planets.DAYNI_MOON,
        True_(),
        Completion(_S.CHALLENGES, 32814077, increasing=True),
        options=LocationOptions(
            requirements=(OptionFilter(ClankChallenges, (2,), "in"),), challenge_group="Gadgetbot Toss"
        ),
        categories=frozenset(("all_clank",)),
        check_order=20,
        definition_order=346,
    ),
    Rac5Locations(
        Rac5ClankChallenges.DAYNI_MOON_LINE,
        Rac5Planets.DAYNI_MOON,
        True_(),
        Completion(_S.CHALLENGES, 32814078, increasing=True),
        options=LocationOptions(
            requirements=(OptionFilter(ClankChallenges, (2,), "in"),), challenge_group="Gadgetbot Toss"
        ),
        categories=frozenset(("all_clank",)),
        check_order=21,
        definition_order=347,
    ),
    Rac5Locations(
        Rac5ClankChallenges.DAYNI_MOON_CROWD,
        Rac5Planets.DAYNI_MOON,
        True_(),
        Completion(_S.CHALLENGES, 32814080, increasing=True),
        options=LocationOptions(requirements=(OptionFilter(ClankChallenges, (2,), "in"),), challenge_group="Gadgetbot"),
        categories=frozenset(("all_clank",)),
        check_order=26,
        definition_order=352,
    ),
    Rac5Locations(
        Rac5ClankChallenges.DAYNI_MOON_REVERSE,
        Rac5Planets.DAYNI_MOON,
        True_(),
        Completion(_S.CHALLENGES, 32814081, increasing=True),
        options=LocationOptions(requirements=(OptionFilter(ClankChallenges, (2,), "in"),), challenge_group="Gadgetbot"),
        categories=frozenset(("all_clank",)),
        check_order=27,
        definition_order=353,
    ),
    Rac5Locations(
        Rac5ClankChallenges.DAYNI_MOON_BRIDGE,
        Rac5Planets.DAYNI_MOON,
        True_(),
        Completion(_S.CHALLENGES, 32814082, increasing=True),
        options=LocationOptions(requirements=(OptionFilter(ClankChallenges, (2,), "in"),), challenge_group="Gadgetbot"),
        categories=frozenset(("all_clank",)),
        check_order=28,
        definition_order=354,
    ),
    Rac5Locations(
        Rac5ClankChallenges.DAYNI_MOON_LEAP,
        Rac5Planets.DAYNI_MOON,
        True_(),
        Completion(_S.CHALLENGES, 32814083, increasing=True),
        options=LocationOptions(requirements=(OptionFilter(ClankChallenges, (2,), "in"),), challenge_group="Gadgetbot"),
        categories=frozenset(("all_clank",)),
        check_order=29,
        definition_order=355,
    ),
    Rac5Locations(
        Rac5ShrinkRayGrindrail.DAYNI_MOON_TITANIUM_BOLT_ENTRANCE,
        Rac5Planets.DAYNI_MOON,
        And(
            HasAll(Rac5Gadgets.SHRINK_RAY, Rac5Gadgets.SPROUT_O_MATIC),
            HasProjectileWeapon(),
            HasClankPack()
        ),
        Completion(_S.EVENTS, Rac5ShrinkRayGrindrail.DAYNI_MOON_TITANIUM_BOLT_ENTRANCE),
        options=LocationOptions(requirements=(OptionFilter(ShrinkRayOptions, (1,), "in"),)),
        categories=frozenset(("shrink_ray_skip",)),
        definition_order=367,
    ),
)
