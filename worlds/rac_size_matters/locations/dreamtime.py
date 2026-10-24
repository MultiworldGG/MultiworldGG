from rule_builder.options import OptionFilter
from rule_builder.rules import HasAll, True_

from ..constants import (
    Rac5CutsceneLocations,
    Rac5Gadgets,
    Rac5Locations as Rac5LocationNames,
    Rac5Planets,
    Rac5SkillPoints,
    Rac5TBolts,
    Rac5TitanVendorLocations,
    Rac5VendorLocations,
    Rac5Weapons,
)
from ..options import AllCutscenes, AllMissions, ChallengeMode, SkillPoints
from ..rules._helpers import HasChallengeMode, HasProjectileWeapon
from .model import Completion, LocationOptions, Rac5CompletionSources, Rac5Locations

_S = Rac5CompletionSources

LOCATIONS = (
    Rac5Locations(
        Rac5TBolts.DREAMTIME_HAT,
        Rac5Planets.DREAMTIME,
        HasAll(Rac5Gadgets.HYPERSHOT, Rac5Gadgets.SPROUT_O_MATIC),
        Completion(_S.BOLT_BITS, None, 65536),
        categories=frozenset(("titanium_bolt",)),
        native_planets=(5,),
        definition_order=8,
    ),
    Rac5Locations(
        Rac5TBolts.DREAMTIME_GARAGE,
        Rac5Planets.DREAMTIME,
        HasAll(Rac5Gadgets.HYPERSHOT, Rac5Gadgets.SPROUT_O_MATIC),
        Completion(_S.BOLT_BITS, None, 131072),
        categories=frozenset(("titanium_bolt",)),
        native_planets=(5,),
        definition_order=9,
    ),
    Rac5Locations(
        Rac5TBolts.DREAMTIME_CRAB,
        Rac5Planets.DREAMTIME,
        HasAll(Rac5Gadgets.HYPERSHOT, Rac5Gadgets.SPROUT_O_MATIC) & HasProjectileWeapon(),
        Completion(_S.BOLT_BITS, None, 262144),
        categories=frozenset(("titanium_bolt",)),
        native_planets=(5,),
        definition_order=10,
    ),
    Rac5Locations(
        Rac5LocationNames.DREAMTIME_CHESTPLATE,
        Rac5Planets.DREAMTIME,
        HasAll(Rac5Gadgets.HYPERSHOT, Rac5Gadgets.SPROUT_O_MATIC),
        Completion(_S.ARMOUR, "crystallix", 1),
        categories=frozenset(("armour_pickup",)),
        definition_order=26,
    ),
    Rac5Locations(
        Rac5LocationNames.DREAMTIME_HYPERBOREAN_CHESTPLATE,
        Rac5Planets.DREAMTIME,
        HasAll(Rac5Gadgets.HYPERSHOT, Rac5Gadgets.SPROUT_O_MATIC) & HasChallengeMode(1),
        Completion(_S.ARMOUR, "hyperborean", 1),
        options=LocationOptions(requirements=(OptionFilter(ChallengeMode, (1, 2), "in"),)),
        categories=frozenset(("armour_pickup", "challenge_mode_1_armour")),
        definition_order=35,
    ),
    Rac5Locations(
        Rac5SkillPoints.DREAMTIME_FRIENDS,
        Rac5Planets.DREAMTIME,
        HasAll(Rac5Gadgets.HYPERSHOT, Rac5Gadgets.SPROUT_O_MATIC),
        Completion(_S.SKILL_BITS, None, 65536),
        options=LocationOptions(requirements=(OptionFilter(SkillPoints, (2,), "in"),)),
        categories=frozenset(("skill_point", "hard_skill_point")),
        native_planets=(5,),
        definition_order=55,
    ),
    Rac5Locations(
        Rac5SkillPoints.DREAMTIME_NIGHT_TERRORS,
        Rac5Planets.DREAMTIME,
        HasAll(Rac5Gadgets.HYPERSHOT, Rac5Gadgets.SPROUT_O_MATIC),
        Completion(_S.SKILL_BITS, None, 131072),
        options=LocationOptions(requirements=(OptionFilter(SkillPoints, (2,), "in"),)),
        categories=frozenset(("skill_point", "hard_skill_point")),
        native_planets=(5,),
        definition_order=56,
    ),
    Rac5Locations(
        Rac5CutsceneLocations.DREAMTIME_COMPLETE,
        Rac5Planets.DREAMTIME,
        HasAll(Rac5Gadgets.HYPERSHOT, Rac5Gadgets.SPROUT_O_MATIC),
        Completion(_S.MISSIONS, 32814028, 4, 5),
        options=LocationOptions(requirements=(OptionFilter(AllMissions, (1,), "in"),)),
        categories=frozenset(("story_mission", "mission")),
        check_order=8,
        definition_order=73,
    ),
    Rac5Locations(
        Rac5CutsceneLocations.DREAMTIME_ENTER,
        Rac5Planets.DREAMTIME,
        True_(),
        Completion(_S.MISSIONS, 32814028, 1, 5),
        options=LocationOptions(requirements=(OptionFilter(AllCutscenes, (1,), "in"),)),
        categories=frozenset(("cutscene", "mission")),
        check_order=21,
        definition_order=98,
    ),
    Rac5Locations(
        Rac5CutsceneLocations.DREAMTIME_SLEEPING_RATCHET,
        Rac5Planets.DREAMTIME,
        HasAll(Rac5Gadgets.HYPERSHOT, Rac5Gadgets.SPROUT_O_MATIC),
        Completion(_S.MISSIONS, 32814028, 2, 5),
        options=LocationOptions(requirements=(OptionFilter(AllCutscenes, (1,), "in"),)),
        categories=frozenset(("cutscene", "mission")),
        check_order=31,
        definition_order=103,
    ),
    Rac5Locations(
        Rac5VendorLocations.DREAMTIME_SUCK,
        Rac5Planets.DREAMTIME,
        True_(),
        Completion(_S.EVENTS, Rac5VendorLocations.DREAMTIME_SUCK),
        options=LocationOptions(weapon=Rac5Weapons.SUCK_CANNON),
        categories=frozenset(("weapon_vendor",)),
        weapon=Rac5Weapons.SUCK_CANNON,
        definition_order=109,
    ),
    Rac5Locations(
        Rac5TitanVendorLocations.DREAMTIME_SUCK_TITAN,
        Rac5Planets.DREAMTIME,
        HasChallengeMode(1),
        Completion(_S.EVENTS, Rac5TitanVendorLocations.DREAMTIME_SUCK_TITAN),
        options=LocationOptions(
            requirements=(OptionFilter(ChallengeMode, (1, 2), "in"),), weapon=Rac5Weapons.SUCK_CANNON
        ),
        categories=frozenset(("weapon_titan_vendor",)),
        weapon=Rac5Weapons.SUCK_CANNON,
        definition_order=149,
    ),
)
