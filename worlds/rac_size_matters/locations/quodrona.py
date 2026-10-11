from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, True_

from .. import constants as C
from ..constants import Rac5Gadgets, Rac5Infobots
from ..options import AllCutscenes, AllMissions, ChallengeMode, ShrinkRayOptions, SkillPoints
from ..rules._helpers import HasChallengeMode, HasClankPack
from .model import Completion, LocationOptions, Rac5CompletionSources, Rac5Locations
from ..items import GLITCHES_ITEM_NAME
_S = Rac5CompletionSources


def victory_rule(world):
    return HasAll(Rac5Gadgets.SHRINK_RAY, Rac5Gadgets.HYPERSHOT, Rac5Infobots.QUODRONA)

def _glitch(world):
    return HasAll(Rac5Gadgets.SHRINK_RAY, Rac5Gadgets.HYPERSHOT, GLITCHES_ITEM_NAME)

LOCATIONS = (
    Rac5Locations(
        C.Rac5TBolts.QUODRONA_DUMMIES,
        C.Rac5Planets.QUODRONA,
        lambda world: HasAll(Rac5Gadgets.SHRINK_RAY, Rac5Gadgets.HYPERSHOT) & HasClankPack(world) | _glitch(world),
        Completion(_S.BOLT_BITS, None, 68719476736),
        categories=frozenset(("titanium_bolt",)),
        native_planets=(10,),
        definition_order=19,
    ),
    Rac5Locations(
        C.Rac5CutsceneLocations.QUODRONA_GOAL,
        C.Rac5Planets.QUODRONA,
        lambda world: HasAll(Rac5Gadgets.SHRINK_RAY, Rac5Gadgets.HYPERSHOT) & HasClankPack(world) | _glitch(world),
        Completion(_S.MISSIONS, 32814038, 320, 10),
        categories=frozenset(("boss",)),
        check_order=16,
        definition_order=41,
    ),
    Rac5Locations(
        C.Rac5SkillPoints.QUODRONA_ELITE,
        C.Rac5Planets.QUODRONA,
        lambda world: HasAll(Rac5Gadgets.SHRINK_RAY, Rac5Gadgets.HYPERSHOT) & HasClankPack(world) | _glitch(world),
        Completion(_S.SKILL_BITS, None, 68719476736),
        options=LocationOptions(requirements=(OptionFilter(SkillPoints, (2,), "in"),)),
        categories=frozenset(("skill_point", "hard_skill_point")),
        native_planets=(10,),
        definition_order=64,
    ),
    Rac5Locations(
        C.Rac5SkillPoints.QUODRONA_STORM,
        C.Rac5Planets.QUODRONA,
        lambda world: HasAll(Rac5Gadgets.SHRINK_RAY, Rac5Gadgets.HYPERSHOT) & HasClankPack(world) | _glitch(world),
        Completion(_S.SKILL_BITS, None, 137438953472),
        options=LocationOptions(requirements=(OptionFilter(SkillPoints, (2,), "in"),)),
        categories=frozenset(("skill_point", "hard_skill_point")),
        native_planets=(10,),
        definition_order=65,
    ),
    Rac5Locations(
        C.Rac5CutsceneLocations.QUODRONA_FIND,
        C.Rac5Planets.QUODRONA,
        lambda world: HasAll(Rac5Gadgets.SHRINK_RAY, Rac5Gadgets.HYPERSHOT) & HasClankPack(world) | _glitch(world),
        Completion(_S.MISSIONS, 32814038, 4, 10),
        options=LocationOptions(requirements=(OptionFilter(AllMissions, (1,), "in"),)),
        categories=frozenset(("story_mission", "mission")),
        check_order=15,
        definition_order=80,
    ),
    Rac5Locations(
        C.Rac5CutsceneLocations.QUODRONA_CLONE,
        C.Rac5Planets.QUODRONA,
        lambda world: HasAll(Rac5Gadgets.SHRINK_RAY, Rac5Gadgets.HYPERSHOT) & HasClankPack(world) | _glitch(world),
        Completion(_S.MISSIONS, 32814038, 8, 10),
        options=LocationOptions(requirements=(OptionFilter(AllCutscenes, (1,), "in"),)),
        categories=frozenset(("cutscene", "mission")),
        check_order=32,
        definition_order=91,
    ),
    Rac5Locations(
        C.Rac5CutsceneLocations.QUODRONA_CHASE,
        C.Rac5Planets.QUODRONA,
        lambda world: HasAll(Rac5Gadgets.SHRINK_RAY, Rac5Gadgets.HYPERSHOT) & HasClankPack(world) | _glitch(world),
        Completion(_S.MISSIONS, 32814038, 16, 10),
        options=LocationOptions(requirements=(OptionFilter(AllCutscenes, (1,), "in"),)),
        categories=frozenset(("cutscene", "mission")),
        check_order=33,
        definition_order=92,
    ),
    Rac5Locations(
        C.Rac5CutsceneLocations.QUODRONA_MECHA,
        C.Rac5Planets.QUODRONA,
        lambda world: HasAll(Rac5Gadgets.SHRINK_RAY, Rac5Gadgets.HYPERSHOT) & HasClankPack(world) | _glitch(world),
        Completion(_S.MISSIONS, 32814038, 32, 10),
        options=LocationOptions(requirements=(OptionFilter(AllCutscenes, (1,), "in"),)),
        categories=frozenset(("cutscene", "mission")),
        check_order=34,
        definition_order=93,
    ),
    Rac5Locations(
        C.Rac5CutsceneLocations.QUODRONA_ENTER,
        C.Rac5Planets.QUODRONA,
        lambda world: True_(),
        Completion(_S.MISSIONS, 32814038, 1, 10),
        options=LocationOptions(requirements=(OptionFilter(AllCutscenes, (1,), "in"),)),
        categories=frozenset(("cutscene", "mission")),
        check_order=25,
        definition_order=102,
    ),
    Rac5Locations(
        C.Rac5VendorLocations.QUODRONA_LASER,
        C.Rac5Planets.QUODRONA,
        lambda world: True_(),
        Completion(_S.EVENTS, C.Rac5VendorLocations.QUODRONA_LASER),
        options=LocationOptions(weapon=C.Rac5Weapons.LASER_TRACER),
        categories=frozenset(("weapon_vendor",)),
        weapon="laser_tracer",
        definition_order=114,
    ),
    Rac5Locations(
        C.Rac5ModVendorLocations.QUODRONA_AGENTS_LAUNCHER,
        C.Rac5Planets.QUODRONA,
        lambda world: True_(),
        Completion(_S.EVENTS, C.Rac5ModVendorLocations.QUODRONA_AGENTS_LAUNCHER),
        options=LocationOptions(weapon=C.Rac5Weapons.AGENTS_OF_DOOM),
        categories=frozenset(("weapon_mod_vendor",)),
        weapon="agents_of_doom",
        mod_slot="mod_slot_two",
        definition_order=129,
    ),
    Rac5Locations(
        C.Rac5ModVendorLocations.QUODRONA_SCORCHER_SPITFIRE,
        C.Rac5Planets.QUODRONA,
        lambda world: True_(),
        Completion(_S.EVENTS, C.Rac5ModVendorLocations.QUODRONA_SCORCHER_SPITFIRE),
        options=LocationOptions(weapon=C.Rac5Weapons.SCORCHER),
        categories=frozenset(("weapon_mod_vendor",)),
        weapon="scorcher",
        mod_slot="mod_slot_two",
        definition_order=130,
    ),
    Rac5Locations(
        C.Rac5ModVendorLocations.QUODRONA_SNIPER_SPLIT,
        C.Rac5Planets.QUODRONA,
        lambda world: True_(),
        Completion(_S.EVENTS, C.Rac5ModVendorLocations.QUODRONA_SNIPER_SPLIT),
        options=LocationOptions(weapon=C.Rac5Weapons.SNIPER_MINE),
        categories=frozenset(("weapon_mod_vendor",)),
        weapon="sniper_mine",
        mod_slot="mod_slot_one",
        definition_order=131,
    ),
    Rac5Locations(
        C.Rac5ModVendorLocations.QUODRONA_SHOCK_LOCK,
        C.Rac5Planets.QUODRONA,
        lambda world: True_(),
        Completion(_S.EVENTS, C.Rac5ModVendorLocations.QUODRONA_SHOCK_LOCK),
        options=LocationOptions(weapon=C.Rac5Weapons.SHOCK_ROCKET),
        categories=frozenset(("weapon_mod_vendor",)),
        weapon="shock_rocket",
        mod_slot="mod_slot_three",
        definition_order=132,
    ),
    Rac5Locations(
        C.Rac5ModVendorLocations.QUODRONA_SHOCK_AFTER,
        C.Rac5Planets.QUODRONA,
        lambda world: True_(),
        Completion(_S.EVENTS, C.Rac5ModVendorLocations.QUODRONA_SHOCK_AFTER),
        options=LocationOptions(weapon=C.Rac5Weapons.SHOCK_ROCKET),
        categories=frozenset(("weapon_mod_vendor",)),
        weapon="shock_rocket",
        mod_slot="mod_slot_one",
        definition_order=133,
    ),
    Rac5Locations(
        C.Rac5ModVendorLocations.QUODRONA_STATIC_MIRAGE,
        C.Rac5Planets.QUODRONA,
        lambda world: HasChallengeMode(world, 1),
        Completion(_S.EVENTS, C.Rac5ModVendorLocations.QUODRONA_STATIC_MIRAGE),
        options=LocationOptions(
            requirements=(OptionFilter(ChallengeMode, (1, 2), "in"),), weapon=C.Rac5Weapons.STATIC_BARRIER
        ),
        categories=frozenset(("weapon_mod_vendor", "challenge_mode_mod")),
        weapon="static_barrier",
        mod_slot="mod_slot_two",
        definition_order=141,
    ),
    Rac5Locations(
        C.Rac5ModVendorLocations.QUODRONA_LASER_RICOCHET,
        C.Rac5Planets.QUODRONA,
        lambda world: HasChallengeMode(world, 1),
        Completion(_S.EVENTS, C.Rac5ModVendorLocations.QUODRONA_LASER_RICOCHET),
        options=LocationOptions(
            requirements=(OptionFilter(ChallengeMode, (1, 2), "in"),), weapon=C.Rac5Weapons.LASER_TRACER
        ),
        categories=frozenset(("weapon_mod_vendor", "challenge_mode_mod")),
        weapon="laser_tracer",
        mod_slot="mod_slot_two",
        definition_order=143,
    ),
    Rac5Locations(
        C.Rac5TitanVendorLocations.QUODRONA_LASER_TITAN,
        C.Rac5Planets.QUODRONA,
        lambda world: HasChallengeMode(world, 1),
        Completion(_S.EVENTS, C.Rac5TitanVendorLocations.QUODRONA_LASER_TITAN),
        options=LocationOptions(
            requirements=(OptionFilter(ChallengeMode, (1, 2), "in"),), weapon=C.Rac5Weapons.LASER_TRACER
        ),
        categories=frozenset(("weapon_titan_vendor",)),
        weapon="laser_tracer",
        definition_order=155,
    ),
    Rac5Locations(
        C.Rac5ShrinkRayGrindrail.QUODRONA_ENTRANCE,
        C.Rac5Planets.QUODRONA,
        lambda world: Has(Rac5Gadgets.SHRINK_RAY),
        Completion(_S.EVENTS, C.Rac5ShrinkRayGrindrail.QUODRONA_ENTRANCE),
        options=LocationOptions(requirements=(OptionFilter(ShrinkRayOptions, (1,), "in"),)),
        categories=frozenset(("shrink_ray_skip",)),
        definition_order=369,
    ),
    Rac5Locations(
        C.Rac5ShrinkRayGrindrail.QUODRONA_CLONE_TRAINING_ROOM,
        C.Rac5Planets.QUODRONA,
        lambda world: HasAll(Rac5Gadgets.SHRINK_RAY, Rac5Gadgets.HYPERSHOT) & HasClankPack(world) | _glitch(world),
        Completion(_S.EVENTS, C.Rac5ShrinkRayGrindrail.QUODRONA_CLONE_TRAINING_ROOM),
        options=LocationOptions(requirements=(OptionFilter(ShrinkRayOptions, (1,), "in"),)),
        categories=frozenset(("shrink_ray_skip",)),
        definition_order=370,
    ),
)
