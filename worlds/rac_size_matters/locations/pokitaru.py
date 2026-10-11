from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAny, True_

from .. import constants as C
from ..constants import Rac5Weapons
from ..items import GLITCHES_ITEM_NAME, PROGRESSIVE_WEAPON_NAME
from ..options import AllCutscenes, AllMissions, ChallengeMode, SkillPoints
from ..rules._helpers import HasChallengeMode, HasProjectileWeapon, HasClankPack
from .model import Completion, LocationOptions, Rac5CompletionSources, Rac5Locations

_S = Rac5CompletionSources


def _glitch(world):
    return Has(GLITCHES_ITEM_NAME) & HasClankPack(world)


LOCATIONS = (
    Rac5Locations(
        C.Rac5TBolts.POKITARU_ZIPLINE,
        C.Rac5Planets.POKITARU,
        lambda world: HasProjectileWeapon() & HasClankPack(world) | _glitch(world),
        Completion(_S.BOLT_BITS, None, 1),
        categories=frozenset(("titanium_bolt",)),
        native_planets=(1,),
        definition_order=0,
    ),
    Rac5Locations(
        C.Rac5TBolts.POKITARU_HUT,
        C.Rac5Planets.POKITARU,
        lambda world: HasProjectileWeapon() | _glitch(world),
        Completion(_S.BOLT_BITS, None, 2),
        categories=frozenset(("titanium_bolt",)),
        native_planets=(1,),
        definition_order=1,
    ),
    Rac5Locations(
        C.Rac5Locations.POKITARU_CHESTPLATE,
        C.Rac5Planets.POKITARU,
        lambda world: HasProjectileWeapon() | _glitch(world),
        Completion(_S.ARMOUR, "wildfire", 1),
        categories=frozenset(("armour_pickup",)),
        definition_order=20,
    ),
    Rac5Locations(
        C.Rac5Locations.POKITARU_GLOVES,
        C.Rac5Planets.POKITARU,
        lambda world: HasProjectileWeapon() | _glitch(world),
        Completion(_S.ARMOUR, "wildfire", 4),
        categories=frozenset(("armour_pickup",)),
        definition_order=21,
    ),
    Rac5Locations(
        C.Rac5Locations.POKITARU_HYPERBOREAN_GLOVES,
        C.Rac5Planets.POKITARU,
        lambda world: (HasProjectileWeapon() | _glitch(world)) & HasChallengeMode(world, 1),
        Completion(_S.ARMOUR, "hyperborean", 4),
        options=LocationOptions(requirements=(OptionFilter(ChallengeMode, (1, 2), "in"),)),
        categories=frozenset(("armour_pickup", "challenge_mode_1_armour")),
        definition_order=33,
    ),
    Rac5Locations(
        C.Rac5Locations.POKITARU_CHAMELEON_BOOTS,
        C.Rac5Planets.POKITARU,
        lambda world: HasChallengeMode(world, 2),
        Completion(_S.ARMOUR, "chameleon", 16),
        options=LocationOptions(requirements=(OptionFilter(ChallengeMode, (2,), "in"),)),
        categories=frozenset(("armour_pickup", "challenge_mode_2_armour")),
        definition_order=37,
    ),
    Rac5Locations(
        C.Rac5SkillPoints.POKITARU_TRAIN,
        C.Rac5Planets.POKITARU,
        lambda world: HasProjectileWeapon() | _glitch(world),
        Completion(_S.SKILL_BITS, None, 1),
        options=LocationOptions(requirements=(OptionFilter(SkillPoints, (1, 2), "in"),)),
        categories=frozenset(("skill_point", "easy_skill_point")),
        native_planets=(1,),
        definition_order=44,
    ),
    Rac5Locations(
        C.Rac5SkillPoints.POKITARU_BOAT,
        C.Rac5Planets.POKITARU,
        lambda world: HasProjectileWeapon() | _glitch(world),
        Completion(_S.SKILL_BITS, None, 2),
        options=LocationOptions(requirements=(OptionFilter(SkillPoints, (1, 2), "in"),)),
        categories=frozenset(("skill_point", "easy_skill_point")),
        native_planets=(1,),
        definition_order=45,
    ),
    Rac5Locations(
        C.Rac5SkillPoints.POKITARU_COWS,
        C.Rac5Planets.POKITARU,
        lambda world: HasAny(Rac5Weapons.MOOTATOR, PROGRESSIVE_WEAPON_NAME[Rac5Weapons.MOOTATOR]) & (HasProjectileWeapon() | _glitch(world)),
        Completion(_S.SKILL_BITS, None, 4),
        options=LocationOptions(requirements=(OptionFilter(SkillPoints, (1, 2), "in"),), weapon=C.Rac5Weapons.MOOTATOR),
        categories=frozenset(("skill_point", "easy_skill_point")),
        weapon="mootator",
        native_planets=(1,),
        definition_order=46,
    ),
    Rac5Locations(
        C.Rac5CutsceneLocations.POKITARU_FIGHT,
        C.Rac5Planets.POKITARU,
        lambda world: HasProjectileWeapon() | _glitch(world),
        Completion(_S.MISSIONS, 32814020, 2, 1),
        options=LocationOptions(requirements=(OptionFilter(AllMissions, (1,), "in"),)),
        categories=frozenset(("story_mission", "mission")),
        check_order=3,
        definition_order=68,
    ),
    Rac5Locations(
        C.Rac5CutsceneLocations.POKITARU_RESCUE,
        C.Rac5Planets.POKITARU,
        lambda world: HasProjectileWeapon() | _glitch(world),
        Completion(_S.MISSIONS, 32814020, 4, 1),
        options=LocationOptions(requirements=(OptionFilter(AllMissions, (1,), "in"),)),
        categories=frozenset(("story_mission", "mission")),
        reload_planet=1,
        check_order=0,
        definition_order=83,
    ),
    Rac5Locations(
        C.Rac5CutsceneLocations.POKITARU_ENTER,
        C.Rac5Planets.POKITARU,
        lambda world: True_(),
        Completion(_S.MISSIONS, 32814020, 1, 1),
        options=LocationOptions(requirements=(OptionFilter(AllCutscenes, (1,), "in"),)),
        categories=frozenset(("cutscene", "mission")),
        check_order=17,
        definition_order=94,
    ),
    Rac5Locations(
        C.Rac5VendorLocations.POKITARU_LACERATOR,
        C.Rac5Planets.POKITARU,
        lambda world: True_(),
        Completion(_S.EVENTS, C.Rac5VendorLocations.POKITARU_LACERATOR),
        options=LocationOptions(weapon=C.Rac5Weapons.LACERATOR),
        categories=frozenset(("weapon_vendor",)),
        weapon="lacerator",
        definition_order=104,
    ),
    Rac5Locations(
        C.Rac5VendorLocations.POKITARU_ACID,
        C.Rac5Planets.POKITARU,
        lambda world: True_(),
        Completion(_S.EVENTS, C.Rac5VendorLocations.POKITARU_ACID),
        options=LocationOptions(weapon=C.Rac5Weapons.ACID_BOMB_GLOVE),
        categories=frozenset(("weapon_vendor",)),
        weapon="acid_bomb_glove",
        definition_order=105,
    ),
    Rac5Locations(
        C.Rac5VendorLocations.POKITARU_CONCUSSION,
        C.Rac5Planets.POKITARU,
        lambda world: True_(),
        Completion(_S.EVENTS, C.Rac5VendorLocations.POKITARU_CONCUSSION),
        options=LocationOptions(weapon=C.Rac5Weapons.CONCUSSION_GUN),
        categories=frozenset(("weapon_vendor",)),
        weapon="concussion_gun",
        definition_order=106,
    ),
    Rac5Locations(
        C.Rac5VendorLocations.POKITARU_RYNO,
        C.Rac5Planets.POKITARU,
        lambda world: HasChallengeMode(world, 1),
        Completion(_S.EVENTS, C.Rac5VendorLocations.POKITARU_RYNO),
        options=LocationOptions(requirements=(OptionFilter(ChallengeMode, (1, 2), "in"),), weapon=C.Rac5Weapons.RYNO),
        categories=frozenset(("weapon_vendor", "challenge_mode_ryno")),
        weapon="ryno",
        definition_order=115,
    ),
    Rac5Locations(
        C.Rac5VendorLocations.POKITARU_HYPERSHOT,
        C.Rac5Planets.POKITARU,
        lambda world: True_(),
        Completion(_S.EVENTS, C.Rac5VendorLocations.POKITARU_HYPERSHOT),
        categories=frozenset(("gadget_vendor",)),
        gadget="hypershot",
        definition_order=116,
    ),
    Rac5Locations(
        C.Rac5TitanVendorLocations.POKITARU_LACERATOR_TITAN,
        C.Rac5Planets.POKITARU,
        lambda world: HasChallengeMode(world, 1),
        Completion(_S.EVENTS, C.Rac5TitanVendorLocations.POKITARU_LACERATOR_TITAN),
        options=LocationOptions(
            requirements=(OptionFilter(ChallengeMode, (1, 2), "in"),), weapon=C.Rac5Weapons.LACERATOR
        ),
        categories=frozenset(("weapon_titan_vendor",)),
        weapon="lacerator",
        definition_order=144,
    ),
    Rac5Locations(
        C.Rac5TitanVendorLocations.POKITARU_ACID_TITAN,
        C.Rac5Planets.POKITARU,
        lambda world: HasChallengeMode(world, 1),
        Completion(_S.EVENTS, C.Rac5TitanVendorLocations.POKITARU_ACID_TITAN),
        options=LocationOptions(
            requirements=(OptionFilter(ChallengeMode, (1, 2), "in"),), weapon=C.Rac5Weapons.ACID_BOMB_GLOVE
        ),
        categories=frozenset(("weapon_titan_vendor",)),
        weapon="acid_bomb_glove",
        definition_order=145,
    ),
    Rac5Locations(
        C.Rac5TitanVendorLocations.POKITARU_CONCUSSION_TITAN,
        C.Rac5Planets.POKITARU,
        lambda world: HasChallengeMode(world, 1),
        Completion(_S.EVENTS, C.Rac5TitanVendorLocations.POKITARU_CONCUSSION_TITAN),
        options=LocationOptions(
            requirements=(OptionFilter(ChallengeMode, (1, 2), "in"),), weapon=C.Rac5Weapons.CONCUSSION_GUN
        ),
        categories=frozenset(("weapon_titan_vendor",)),
        weapon="concussion_gun",
        definition_order=146,
    ),
)
