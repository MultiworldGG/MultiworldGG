from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, True_

from .. import constants as C
from ..constants import Rac5Gadgets, Rac5Infobots
from ..constants.options import Rac5Options
from ..options import AllCutscenes, AllMissions, ChallengeMode, GiantClank, ShrinkRayOptions, SkillPoints
from ..rules._helpers import HasChallengeMode
from .model import BASE_ID, Completion, LocationOptions, Rac5CompletionSources, Rac5Locations

_S = Rac5CompletionSources

LOCATIONS = (
    Rac5Locations(
        C.Rac5TBolts.CHALLAX_MECH_PAD,
        C.Rac5Planets.CHALLAX,
        lambda world: True_(),
        Completion(_S.BOLT_BITS, None, 16777216),
        categories=frozenset(("titanium_bolt",)),
        native_planets=(7,),
        definition_order=12,
    ),
    Rac5Locations(
        C.Rac5TBolts.CHALLAX_ROOM,
        C.Rac5Planets.CHALLAX,
        lambda world: Has(Rac5Gadgets.SHRINK_RAY) & Has(Rac5Gadgets.POLARIZER),
        Completion(_S.BOLT_BITS, None, 33554432),
        categories=frozenset(("titanium_bolt",)),
        native_planets=(7,),
        definition_order=13,
    ),
    Rac5Locations(
        C.Rac5TBolts.CHALLAX_PLANT,
        C.Rac5Planets.CHALLAX,
        lambda world: Has(Rac5Gadgets.SHRINK_RAY) & Has(Rac5Gadgets.POLARIZER) & Has(Rac5Gadgets.SPROUT_O_MATIC),
        Completion(_S.BOLT_BITS, None, 67108864),
        categories=frozenset(("titanium_bolt",)),
        native_planets=(7,),
        definition_order=14,
    ),
    Rac5Locations(
        C.Rac5Locations.CHALLAX_HELMET,
        C.Rac5Planets.CHALLAX,
        lambda world: (
            Has(Rac5Gadgets.SHRINK_RAY) & Has(Rac5Gadgets.POLARIZER) & Has(Rac5Gadgets.SPROUT_O_MATIC)
            | Has(Rac5Infobots.DAYNI_MOON)
        ),
        Completion(_S.ARMOUR, "electroshock", 2),
        categories=frozenset(("armour_pickup",)),
        definition_order=28,
    ),
    Rac5Locations(
        C.Rac5Locations.CHALLAX_CHESTPLATE,
        C.Rac5Planets.CHALLAX,
        lambda world: True_(),
        Completion(_S.ARMOUR, "electroshock", 1),
        options=LocationOptions(requirements=(OptionFilter(GiantClank, (1,), "in"),)),
        categories=frozenset(("armour_pickup", Rac5Options.GIANT_CLANK)),
        definition_order=32,
    ),
    Rac5Locations(
        C.Rac5Locations.CHALLAX_HYPERBOREAN_HELMET,
        C.Rac5Planets.CHALLAX,
        lambda world: (
            Has(Rac5Gadgets.SHRINK_RAY)
            & Has(Rac5Gadgets.POLARIZER)
            & Has(Rac5Gadgets.SPROUT_O_MATIC)
            & HasChallengeMode(world, 1)
        ),
        Completion(_S.ARMOUR, "hyperborean", 2),
        options=LocationOptions(requirements=(OptionFilter(ChallengeMode, (1, 2), "in"),)),
        categories=frozenset(("armour_pickup", "challenge_mode_1_armour")),
        definition_order=36,
    ),
    Rac5Locations(
        C.Rac5SkillPoints.CHALLAX_MASTER,
        C.Rac5Planets.CHALLAX,
        lambda world: Has(Rac5Gadgets.SHRINK_RAY) & Has(Rac5Gadgets.POLARIZER) & Has(Rac5Gadgets.SPROUT_O_MATIC),
        Completion(_S.SKILL_BITS, None, 33554432),
        options=LocationOptions(requirements=(OptionFilter(SkillPoints, (2,), "in"),)),
        categories=frozenset(("skill_point", "hard_skill_point")),
        native_planets=(7,),
        definition_order=58,
    ),
    Rac5Locations(
        C.Rac5SkillPoints.CHALLAX_VARMINTS,
        C.Rac5Planets.CHALLAX,
        lambda world: True_(),
        Completion(_S.SKILL_BITS, None, 67108864),
        options=LocationOptions(
            requirements=(
                OptionFilter(GiantClank, (1,), "in"),
                OptionFilter(SkillPoints, (1, 2), "in"),
            )
        ),
        categories=frozenset((Rac5Options.GIANT_CLANK, "skill_point", "easy_skill_point")),
        native_planets=(7,),
        definition_order=67,
    ),
    Rac5Locations(
        C.Rac5CutsceneLocations.CHALLAX_CLANK,
        C.Rac5Planets.CHALLAX,
        lambda world: True_(),
        Completion(_S.EVENTS, C.Rac5CutsceneLocations.CHALLAX_CLANK),
        options=LocationOptions(
            requirements=(
                OptionFilter(GiantClank, (1,), "in"),
                OptionFilter(AllMissions, (1,), "in"),
            )
        ),
        categories=frozenset((Rac5Options.GIANT_CLANK, "story_mission", "mission")),
        definition_order=82,
    ),
    Rac5Locations(
        C.Rac5CutsceneLocations.CHALLAX_EXPLORE,
        C.Rac5Planets.CHALLAX,
        lambda world: Has(Rac5Gadgets.SHRINK_RAY) & Has(Rac5Gadgets.POLARIZER) & Has(Rac5Gadgets.SPROUT_O_MATIC),
        Completion(_S.MISSIONS, 32814032, 4, 7),
        options=LocationOptions(requirements=(OptionFilter(AllMissions, (1,), "in"),)),
        categories=frozenset(("story_mission", "mission")),
        reload_planet=7,
        check_order=2,
        definition_order=85,
    ),
    Rac5Locations(
        C.Rac5CutsceneLocations.CHALLAX_ENTER,
        C.Rac5Planets.CHALLAX,
        lambda world: True_(),
        Completion(_S.MISSIONS, 32814032, 1, 7),
        options=LocationOptions(requirements=(OptionFilter(AllCutscenes, (1,), "in"),)),
        categories=frozenset(("cutscene", "mission")),
        check_order=23,
        definition_order=100,
    ),
    Rac5Locations(
        C.Rac5VendorLocations.CHALLAX_SNIPER,
        C.Rac5Planets.CHALLAX,
        lambda world: Has(Rac5Gadgets.SHRINK_RAY),
        Completion(_S.EVENTS, C.Rac5VendorLocations.CHALLAX_SNIPER),
        options=LocationOptions(weapon=C.Rac5Weapons.SNIPER_MINE),
        categories=frozenset(("weapon_vendor",)),
        weapon="sniper_mine",
        definition_order=111,
    ),
    Rac5Locations(
        C.Rac5VendorLocations.CHALLAX_PDA,
        C.Rac5Planets.CHALLAX,
        lambda world: Has(Rac5Gadgets.SHRINK_RAY),
        Completion(_S.EVENTS, C.Rac5VendorLocations.CHALLAX_PDA),
        categories=frozenset(("gadget_vendor",)),
        gadget="pda",
        definition_order=117,
    ),
    Rac5Locations(
        C.Rac5VendorLocations.CHALLAX_BOLT_GRABBER,
        C.Rac5Planets.CHALLAX,
        lambda world: True_(),
        Completion(_S.EVENTS, C.Rac5VendorLocations.CHALLAX_BOLT_GRABBER),
        categories=frozenset(("gadget_vendor",)),
        gadget="bolt_grabber",
        definition_order=119,
    ),
    Rac5Locations(
        C.Rac5ModVendorLocations.CHALLAX_LACERATOR_DOUBLE,
        C.Rac5Planets.CHALLAX,
        lambda world: Has(Rac5Gadgets.SHRINK_RAY) & Has(Rac5Gadgets.POLARIZER),
        Completion(_S.EVENTS, C.Rac5ModVendorLocations.CHALLAX_LACERATOR_DOUBLE),
        options=LocationOptions(weapon=C.Rac5Weapons.LACERATOR),
        categories=frozenset(("weapon_mod_vendor",)),
        weapon="lacerator",
        mod_slot="mod_slot_one",
        definition_order=123,
    ),
    Rac5Locations(
        C.Rac5ModVendorLocations.CHALLAX_ACID_BURN,
        C.Rac5Planets.CHALLAX,
        lambda world: Has(Rac5Gadgets.SHRINK_RAY) & Has(Rac5Gadgets.POLARIZER),
        Completion(_S.EVENTS, C.Rac5ModVendorLocations.CHALLAX_ACID_BURN),
        options=LocationOptions(weapon=C.Rac5Weapons.ACID_BOMB_GLOVE),
        categories=frozenset(("weapon_mod_vendor",)),
        weapon="acid_bomb_glove",
        mod_slot="mod_slot_one",
        definition_order=124,
    ),
    Rac5Locations(
        C.Rac5ModVendorLocations.CHALLAX_ACID_EPOXY,
        C.Rac5Planets.CHALLAX,
        lambda world: Has(Rac5Gadgets.SHRINK_RAY) & Has(Rac5Gadgets.POLARIZER),
        Completion(_S.EVENTS, C.Rac5ModVendorLocations.CHALLAX_ACID_EPOXY),
        options=LocationOptions(weapon=C.Rac5Weapons.ACID_BOMB_GLOVE),
        categories=frozenset(("weapon_mod_vendor",)),
        weapon="acid_bomb_glove",
        mod_slot="mod_slot_two",
        definition_order=125,
    ),
    Rac5Locations(
        C.Rac5ModVendorLocations.CHALLAX_CONCUSSION_LOCK,
        C.Rac5Planets.CHALLAX,
        lambda world: Has(Rac5Gadgets.SHRINK_RAY) & Has(Rac5Gadgets.POLARIZER),
        Completion(_S.EVENTS, C.Rac5ModVendorLocations.CHALLAX_CONCUSSION_LOCK),
        options=LocationOptions(weapon=C.Rac5Weapons.CONCUSSION_GUN),
        categories=frozenset(("weapon_mod_vendor",)),
        weapon="concussion_gun",
        mod_slot="mod_slot_three",
        definition_order=126,
    ),
    Rac5Locations(
        C.Rac5ModVendorLocations.CHALLAX_CONCUSSION_CHARGE,
        C.Rac5Planets.CHALLAX,
        lambda world: Has(Rac5Gadgets.SHRINK_RAY) & Has(Rac5Gadgets.POLARIZER),
        Completion(_S.EVENTS, C.Rac5ModVendorLocations.CHALLAX_CONCUSSION_CHARGE),
        options=LocationOptions(weapon=C.Rac5Weapons.CONCUSSION_GUN),
        categories=frozenset(("weapon_mod_vendor",)),
        weapon="concussion_gun",
        mod_slot="mod_slot_two",
        definition_order=127,
    ),
    Rac5Locations(
        C.Rac5ModVendorLocations.CHALLAX_BEE_WORKER,
        C.Rac5Planets.CHALLAX,
        lambda world: Has(Rac5Gadgets.SHRINK_RAY) & Has(Rac5Gadgets.POLARIZER),
        Completion(_S.EVENTS, C.Rac5ModVendorLocations.CHALLAX_BEE_WORKER),
        options=LocationOptions(weapon=C.Rac5Weapons.BEE_MINE_GLOVE),
        categories=frozenset(("weapon_mod_vendor",)),
        weapon="bee_mine_glove",
        mod_slot="mod_slot_one",
        definition_order=128,
    ),
    Rac5Locations(
        C.Rac5ModVendorLocations.CHALLAX_SNIPER_SMART_REFLECTOR,
        C.Rac5Planets.CHALLAX,
        lambda world: Has(Rac5Gadgets.SHRINK_RAY) & Has(Rac5Gadgets.POLARIZER) & HasChallengeMode(world, 1),
        Completion(_S.EVENTS, C.Rac5ModVendorLocations.CHALLAX_SNIPER_SMART_REFLECTOR),
        options=LocationOptions(
            requirements=(OptionFilter(ChallengeMode, (1, 2), "in"),), weapon=C.Rac5Weapons.SNIPER_MINE
        ),
        categories=frozenset(("weapon_mod_vendor", "challenge_mode_mod")),
        weapon="sniper_mine",
        mod_slot="mod_slot_two",
        definition_order=138,
    ),
    Rac5Locations(
        C.Rac5ModVendorLocations.CHALLAX_SHOCK_MULTI_LAUNCHER,
        C.Rac5Planets.CHALLAX,
        lambda world: Has(Rac5Gadgets.SHRINK_RAY) & Has(Rac5Gadgets.POLARIZER) & HasChallengeMode(world, 1),
        Completion(_S.EVENTS, C.Rac5ModVendorLocations.CHALLAX_SHOCK_MULTI_LAUNCHER),
        options=LocationOptions(
            requirements=(OptionFilter(ChallengeMode, (1, 2), "in"),), weapon=C.Rac5Weapons.SHOCK_ROCKET
        ),
        categories=frozenset(("weapon_mod_vendor", "challenge_mode_mod")),
        weapon="shock_rocket",
        mod_slot="mod_slot_two",
        definition_order=139,
    ),
    Rac5Locations(
        C.Rac5ModVendorLocations.CHALLAX_LASER_PIERCE,
        C.Rac5Planets.CHALLAX,
        lambda world: Has(Rac5Gadgets.SHRINK_RAY) & Has(Rac5Gadgets.POLARIZER) & HasChallengeMode(world, 1),
        Completion(_S.EVENTS, C.Rac5ModVendorLocations.CHALLAX_LASER_PIERCE),
        options=LocationOptions(
            requirements=(OptionFilter(ChallengeMode, (1, 2), "in"),), weapon=C.Rac5Weapons.LASER_TRACER
        ),
        categories=frozenset(("weapon_mod_vendor", "challenge_mode_mod")),
        weapon="laser_tracer",
        mod_slot="mod_slot_one",
        definition_order=142,
    ),
    Rac5Locations(
        C.Rac5TitanVendorLocations.CHALLAX_SNIPER_TITAN,
        C.Rac5Planets.CHALLAX,
        lambda world: Has(Rac5Gadgets.SHRINK_RAY) & HasChallengeMode(world, 1),
        Completion(_S.EVENTS, C.Rac5TitanVendorLocations.CHALLAX_SNIPER_TITAN),
        options=LocationOptions(
            requirements=(OptionFilter(ChallengeMode, (1, 2), "in"),), weapon=C.Rac5Weapons.SNIPER_MINE
        ),
        categories=frozenset(("weapon_titan_vendor",)),
        weapon="sniper_mine",
        definition_order=151,
    ),
    Rac5Locations(
        C.Rac5ShrinkRayGrindrail.CHALLAX_GRINDRAIL,
        C.Rac5Planets.CHALLAX,
        lambda world: Has(Rac5Gadgets.SHRINK_RAY),
        Completion(_S.EVENTS, C.Rac5ShrinkRayGrindrail.CHALLAX_GRINDRAIL),
        options=LocationOptions(requirements=(OptionFilter(ShrinkRayOptions, (1,), "in"),)),
        categories=frozenset(("shrink_ray_skip",)),
        definition_order=366,
    ),
    Rac5Locations(
        C.Rac5ShrinkRayGrindrail.CHALLAX_SECOND_PUZZLE,
        C.Rac5Planets.CHALLAX,
        lambda world: HasAll(Rac5Gadgets.SHRINK_RAY, Rac5Gadgets.POLARIZER, Rac5Gadgets.SPROUT_O_MATIC),
        Completion(_S.EVENTS, C.Rac5ShrinkRayGrindrail.CHALLAX_SECOND_PUZZLE),
        code=BASE_ID + 373,
        options=LocationOptions(requirements=(OptionFilter(ShrinkRayOptions, (1,), "in"),)),
        categories=frozenset(("shrink_ray_skip",)),
        definition_order=372,
    ),
)
