from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, True_

from .. import constants as C
from ..constants import Rac5Gadgets
from ..options import AllCutscenes, AllMissions, ChallengeMode, ShrinkRayOptions, SkillPoints
from ..rules._helpers import HasChallengeMode
from .model import Completion, LocationOptions, Rac5CompletionSources, Rac5Locations

_S = Rac5CompletionSources

LOCATIONS = (
    Rac5Locations(
        C.Rac5TBolts.INSIDE_CLANK_LADDER,
        C.Rac5Planets.INSIDE_CLANK,
        lambda world: True_(),
        Completion(_S.BOLT_BITS, None, 4294967296),
        categories=frozenset(("titanium_bolt",)),
        native_planets=(9,),
        definition_order=17,
    ),
    Rac5Locations(
        C.Rac5TBolts.INSIDE_CLANK_WALL,
        C.Rac5Planets.INSIDE_CLANK,
        lambda world: True_(),
        Completion(_S.BOLT_BITS, None, 8589934592),
        categories=frozenset(("titanium_bolt",)),
        native_planets=(9,),
        definition_order=18,
    ),
    Rac5Locations(
        C.Rac5Locations.INSIDE_CLANK_CHESTPLATE,
        C.Rac5Planets.INSIDE_CLANK,
        lambda world: HasAll(Rac5Gadgets.HYPERSHOT, Rac5Gadgets.POLARIZER) & Has(Rac5Gadgets.SHRINK_RAY),
        Completion(_S.ARMOUR, "mega_bomb", 1),
        categories=frozenset(("armour_pickup",)),
        definition_order=30,
    ),
    Rac5Locations(
        C.Rac5Locations.INSIDE_CLANK_CHAMELEON_HELMET,
        C.Rac5Planets.INSIDE_CLANK,
        lambda world: HasChallengeMode(world, 2),
        Completion(_S.ARMOUR, "chameleon", 2),
        options=LocationOptions(requirements=(OptionFilter(ChallengeMode, (2,), "in"),)),
        categories=frozenset(("armour_pickup", "challenge_mode_2_armour")),
        definition_order=40,
    ),
    Rac5Locations(
        C.Rac5SkillPoints.INSIDE_CLANK_SHOCK,
        C.Rac5Planets.INSIDE_CLANK,
        lambda world: HasAll(Rac5Gadgets.HYPERSHOT, Rac5Gadgets.POLARIZER) & Has(Rac5Gadgets.SHRINK_RAY),
        Completion(_S.SKILL_BITS, None, 4294967296),
        options=LocationOptions(requirements=(OptionFilter(SkillPoints, (2,), "in"),)),
        categories=frozenset(("skill_point", "hard_skill_point")),
        native_planets=(9,),
        definition_order=62,
    ),
    Rac5Locations(
        C.Rac5SkillPoints.INSIDE_CLANK_RATCHET,
        C.Rac5Planets.INSIDE_CLANK,
        lambda world: HasAll(Rac5Gadgets.HYPERSHOT, Rac5Gadgets.POLARIZER) & Has(Rac5Gadgets.SHRINK_RAY),
        Completion(_S.SKILL_BITS, None, 8589934592),
        options=LocationOptions(requirements=(OptionFilter(SkillPoints, (2,), "in"),)),
        categories=frozenset(("skill_point", "hard_skill_point")),
        native_planets=(9,),
        definition_order=63,
    ),
    Rac5Locations(
        C.Rac5CutsceneLocations.INSIDE_CLANK_ESCAPE,
        C.Rac5Planets.INSIDE_CLANK,
        lambda world: True_(),
        Completion(_S.MISSIONS, 32814034, 32, 8),
        options=LocationOptions(requirements=(OptionFilter(AllMissions, (1,), "in"),)),
        categories=frozenset(("story_mission", "mission")),
        check_order=13,
        definition_order=78,
    ),
    Rac5Locations(
        C.Rac5CutsceneLocations.INSIDE_CLANK_TECHNOMITES,
        C.Rac5Planets.INSIDE_CLANK,
        lambda world: HasAll(Rac5Gadgets.HYPERSHOT, Rac5Gadgets.POLARIZER) & Has(Rac5Gadgets.SHRINK_RAY),
        Completion(_S.MISSIONS, 32814036, 2, 9),
        options=LocationOptions(requirements=(OptionFilter(AllMissions, (1,), "in"),)),
        categories=frozenset(("story_mission", "mission")),
        check_order=14,
        definition_order=79,
    ),
    Rac5Locations(
        C.Rac5CutsceneLocations.INSIDE_CLANK_ENTER,
        C.Rac5Planets.INSIDE_CLANK,
        lambda world: True_(),
        Completion(_S.MISSIONS, 32814036, 1, 9),
        options=LocationOptions(requirements=(OptionFilter(AllCutscenes, (1,), "in"),)),
        categories=frozenset(("cutscene", "mission")),
        check_order=24,
        definition_order=101,
    ),
    Rac5Locations(
        C.Rac5VendorLocations.INSIDE_CLANK_STATIC,
        C.Rac5Planets.INSIDE_CLANK,
        lambda world: HasAll(Rac5Gadgets.HYPERSHOT, Rac5Gadgets.POLARIZER) & Has(Rac5Gadgets.SHRINK_RAY),
        Completion(_S.EVENTS, C.Rac5VendorLocations.INSIDE_CLANK_STATIC),
        options=LocationOptions(weapon=C.Rac5Weapons.STATIC_BARRIER),
        categories=frozenset(("weapon_vendor",)),
        weapon="static_barrier",
        definition_order=113,
    ),
    Rac5Locations(
        C.Rac5TitanVendorLocations.INSIDE_CLANK_STATIC_TITAN,
        C.Rac5Planets.INSIDE_CLANK,
        lambda world: (
            HasAll(Rac5Gadgets.HYPERSHOT, Rac5Gadgets.POLARIZER, Rac5Gadgets.SHRINK_RAY)
            & HasChallengeMode(world, 1)
        ),
        Completion(_S.EVENTS, C.Rac5TitanVendorLocations.INSIDE_CLANK_STATIC_TITAN),
        options=LocationOptions(
            requirements=(OptionFilter(ChallengeMode, (1, 2), "in"),), weapon=C.Rac5Weapons.STATIC_BARRIER
        ),
        categories=frozenset(("weapon_titan_vendor",)),
        weapon="static_barrier",
        definition_order=154,
    ),
    Rac5Locations(
        C.Rac5ShrinkRayGrindrail.INSIDE_CLANK_GRINDRAIL,
        C.Rac5Planets.INSIDE_CLANK,
        lambda world: HasAll(Rac5Gadgets.SHRINK_RAY, Rac5Gadgets.HYPERSHOT),
        Completion(_S.EVENTS, C.Rac5ShrinkRayGrindrail.INSIDE_CLANK_GRINDRAIL),
        options=LocationOptions(requirements=(OptionFilter(ShrinkRayOptions, (1,), "in"),)),
        categories=frozenset(("shrink_ray_skip",)),
        definition_order=368,
    ),
)
