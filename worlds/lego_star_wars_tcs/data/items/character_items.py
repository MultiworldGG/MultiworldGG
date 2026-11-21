from dataclasses import dataclass
from enum import IntEnum, auto
from typing import ClassVar

from . import CHARACTER_ITEMS_BASE, GenericCharacterData, ItemType
from ..characters import Character, EXTRA_TOGGLE_LOGIC_RELEVANT_CHARACTERS
from ...character_ability import *


__all__ = [
    "Alignment",
    "CharacterData",
    "NORMAL_CHARACTER_DATA",
    "NON_VEHICLE_CHARACTER_TO_ITEM_DATA",
    "NON_VEHICLE_NORMAL_CHARACTER_TO_ITEM_DATA",
    "NON_VEHICLE_EXTRA_CHARACTER_TO_ITEM_DATA",
    "EXTRA_CHARACTER_DATA",
    "CANTINA_CAR",
    "SORTED_SINGLE_JUMP_DISTANCE_TO_CHARACTERS",
]


class Alignment(IntEnum):
    GOOD = auto()  # Enemies will attack on sight.
    NEUTRAL = auto()  # Enemies will only attack if attacked first (or attacks are used nearby).
    PASSIVE = auto()  # Enemies will not attack. Switching to a passive character will lose aggro.
    # Enemies will only attack if attacked first (or attacks are used nearby). These characters have the "baddie" tag.
    EVIL = auto()


@dataclass(frozen=True)
class CharacterData(GenericCharacterData):
    run_speed: float  # The majority of characters have 1.2.
    # Jump height is calculated through jump_speed**2/(2*air_gravity) (v0**2/2g: v0 = jump_speed, g=-air_gravity
    single_jump_height: float  # The majority of characters have 0.44 (Jedi and many other decent jumpers).
    # Jump distance is calculated through air_time = 2*jump_speed/abs(air_gravity); jump_distance = air_time * run_speed
    single_jump_distance: float
    alignment: Alignment = Alignment.GOOD
    item_type: ClassVar[ItemType] = "Character"

    @classmethod
    def ap_item(
            cls,
            character: Character,
            abilities: CharacterAbility,
            run_speed: float,
            single_jump_height: float,
            single_jump_distance: float,
            alignment: Alignment = Alignment.GOOD,
    ):
        return cls(
            code=character + CHARACTER_ITEMS_BASE,
            name=character.readable_name,
            character=character,
            abilities=abilities,
            run_speed=run_speed,
            single_jump_height=single_jump_height,
            single_jump_distance=single_jump_distance,
            alignment=alignment,
        )

    @classmethod
    def event(
            cls,
            name: str,
            character: Character,
            abilities: CharacterAbility,
            run_speed: float,
            single_jump_height: float,
            single_jump_distance: float,
            alignment: Alignment = Alignment.GOOD,
    ):
        return cls(
            code=None,
            name=name,
            character=character,
            abilities=abilities,
            run_speed=run_speed,
            single_jump_height=single_jump_height,
            single_jump_distance=single_jump_distance,
            alignment=alignment,
        )

    def __post_init__(self):
        # Automatically set some implied abilities as a safeguard.
        abilities = self.abilities

        # todo: Higher jump heights should include CAN_FLOP_JUMP (Gamorrean Guard and Super Gonk Droid)
        if self.single_jump_height >= 0.44:
            abilities |= CAN_JUMP_0_44
        if self.single_jump_height >= 0.37:
            abilities |= CAN_JUMP_HEIGHT_0_37
        if self.single_jump_distance > 0:
            abilities |= CAN_BARELY_JUMP

        if self.single_jump_distance >= 0.69:
            abilities |= CAN_JUMP_DISTANCE_0_69
        if self.single_jump_distance >= 0.84:
            abilities |= CAN_JUMP_DISTANCE_0_84
        if self.single_jump_distance >= 0.92:
            abilities |= CAN_JUMP_DISTANCE_0_92

        # All Sith are Jedi.
        if SITH in abilities:
            abilities |= JEDI
            assert self.alignment is Alignment.EVIL, f"{self.name} is a Sith, but is not EVIL alignment."

        # All Jedi/Sith, except Luke Skywalker (Dagobah) are trained Jedi that can lift the X-Wing at the end of
        # 5-4 (Dagobah).
        if JEDI in abilities and self.character is not Character.LUKE_SKYWALKER_DAGOBAH:
            abilities |= TRAINED_JEDI

        # All characters that can Grapple happen to have Blasters.
        if GRAPPLE in abilities:
            abilities |= BLASTER

        # These can all melee.
        if JEDI in abilities or BOUNTY_HUNTER in abilities or CAN_HIGH_JUMP_SLAM in abilities:
            abilities |= CAN_MELEE

        # All Bounty Hunters can use blasters.
        if BOUNTY_HUNTER in abilities:
            abilities |= BLASTER

        assert CAN_BUILD_BRICKS not in abilities or CAN_JUMP_HEIGHT_0_37 in abilities, \
            f"All characters that can build should be able to jump 0.37 or higher, but {self.name} cannot."

        assert BOUNTY_HUNTER not in abilities or self.alignment is Alignment.EVIL, \
            f"{self.name} is a Bounty Hunter, but is not EVIL alignment."

        # Double jump implies all the jump height and jump distance abilities.
        if (HIGH_JUMP | JEDI) & abilities != 0:
            abilities |= CAN_DOUBLE_JUMP
        if CAN_DOUBLE_JUMP in abilities:
            abilities |= CAN_JUMP_DISTANCE_0_92
            abilities |= CAN_JUMP_DISTANCE_0_84
            abilities |= CAN_JUMP_DISTANCE_0_69
            abilities |= CAN_FLOP_JUMP
        if CAN_FLOP_JUMP in abilities:
            abilities |= CAN_JUMP_0_44
        if CAN_JUMP_0_44 in abilities:
            abilities |= CAN_JUMP_HEIGHT_0_37
        if CAN_JUMP_HEIGHT_0_37 in abilities:
            # Normal jump distance is not guaranteed.
            abilities |= CAN_BARELY_JUMP

        # Jetpacks are a superior version of Astromech hovering.
        if JETPACK in abilities:
            abilities |= HOVER
        # Hovering is the superior version of jump distance.
        if HOVER in abilities:
            abilities |= CAN_JUMP_DISTANCE_0_92
            abilities |= CAN_JUMP_DISTANCE_0_84
            abilities |= CAN_JUMP_DISTANCE_0_69

        # Automatically set special Hat Machine abilities that are not set explicitly.
        if CAN_WEAR_HAT in abilities and GRAPPLE in abilities:
            abilities |= CAN_WEAR_HAT_AND_GRAPPLE
        if CAN_WEAR_HAT in abilities and CAN_DOUBLE_JUMP in abilities:
            abilities |= CAN_WEAR_HAT_AND_DOUBLE_JUMP

        if self.alignment is Alignment.PASSIVE:
            # Note that Force Ghosts are considered passive.
            abilities &= ~CAN_AGGRAVATE_ENEMIES
            abilities |= IS_PASSIVE
        else:
            # Enemies are aggressive against GOOD characters and will fight back against that damage or attack near
            # them, except Force Ghosts who are untargetable.
            if CAN_MELEE in abilities or BLASTER in abilities or self.alignment is Alignment.GOOD:
                abilities |= CAN_AGGRAVATE_ENEMIES
            # All non-passive (non-ghost) Jedi can deflect (and reflect) blaster bolts.
            if JEDI in abilities:
                abilities |= CAN_DEFLECT_BOLTS

        if self.run_speed >= 0.9:
            abilities |= RUN_SPEED_0_9_OR_HIGHER
        if self.run_speed >= 1.18:
            abilities |= RUN_SPEED_1_18_OR_HIGHER

        if abilities & CharacterAbility.ALL_VEHICLE_ABILITIES != 0:
            raise Exception("Regular characters must not have vehicle abilities.")

        if abilities is not self.abilities:
            # print(f"Updated abilities for {self.name}. Added:\n\t{abilities & ~self.abilities!r}")
            object.__setattr__(self, "abilities", abilities)


COMMON_PACIFIST_NON_DROID = (
        CAN_BUILD_BRICKS
        | CAN_PULL_LEVERS
        | CAN_PUSH_OBJECTS
        | CAN_RIDE_VEHICLES
)
COMMON_SHORT_SLOW = (
    CAN_BUILD_BRICKS
    | CAN_PULL_LEVERS
    | CAN_PUSH_OBJECTS
    | CAN_RIDE_VEHICLES
    | SHORTIE
)

COMMON_NORMAL_SPEED_PACIFIST_NON_DROID = COMMON_PACIFIST_NON_DROID
COMMON_HIGH_JUMP = CAN_DOUBLE_JUMP | HIGH_JUMP
COMMON_HIGH_JUMP_SLAM = COMMON_HIGH_JUMP | CAN_HIGH_JUMP_SLAM | CAN_MELEE | CAN_DEFLECT_BOLTS

COMMON_MELEE_NON_DROID = COMMON_PACIFIST_NON_DROID | CAN_MELEE
COMMON_MELEE_NON_DROID_HIGHER_JUMP = COMMON_MELEE_NON_DROID
COMMON_BLASTER_NON_DROID = COMMON_PACIFIST_NON_DROID | BLASTER
COMMON_HATLESS_NON_DROID = COMMON_PACIFIST_NON_DROID | CAN_WEAR_HAT
COMMON_HATLESS_MELEE_NON_DROID = COMMON_MELEE_NON_DROID | CAN_WEAR_HAT
COMMON_HATLESS_MELEE_NON_DROID_HIGHER_JUMP = COMMON_HATLESS_MELEE_NON_DROID
COMMON_HATLES_PACIFIST_NON_DROID = COMMON_PACIFIST_NON_DROID | CAN_WEAR_HAT
COMMON_JEDI = JEDI | COMMON_PACIFIST_NON_DROID | CAN_DOUBLE_JUMP | CAN_TRIPLE_JUMP_GREAT_DISTANCE | IS_NON_GHOST_JEDI
COMMON_SITH = COMMON_JEDI | SITH

COMMON_GRAPPLE = GRAPPLE | BLASTER
COMMON_BOUNTY_HUNTER = BOUNTY_HUNTER | COMMON_GRAPPLE | CAN_MELEE
COMMON_JETPACK = HOVER | JETPACK
COMMON_NON_DROID_BOUNTY_HUNTER = COMMON_BOUNTY_HUNTER | COMMON_PACIFIST_NON_DROID
COMMON_JETPACK_BOUNTY_HUNTER = COMMON_NON_DROID_BOUNTY_HUNTER | COMMON_JETPACK

MIXIN_FORCE_GHOST = ~(CAN_AGGRAVATE_ENEMIES | IS_NON_GHOST_JEDI | CAN_DEFLECT_BOLTS)


def generic_jedi(character: Character, already_got_hat: bool = False, is_ghost: bool = False):
    abilities = COMMON_JEDI
    if not already_got_hat:
        abilities |= CAN_WEAR_HAT
    if is_ghost:
        abilities &= MIXIN_FORCE_GHOST
        alignment = Alignment.PASSIVE
    else:
        alignment = Alignment.GOOD
    return CharacterData.ap_item(character, abilities, 1.2, 0.44, 0.92, alignment)


def generic_sith(character: Character, already_got_hat: bool = False, imperial: bool = False):
    abilities = COMMON_SITH
    if imperial:
        abilities |= IMPERIAL
    if not already_got_hat:
        abilities |= CAN_WEAR_HAT
    return CharacterData.ap_item(character, abilities, 1.2, 0.44, 0.92, Alignment.EVIL)


def generic_astromech(character: Character):
    abilities = ASTROMECH_PANEL | HOVER | ASTROMECH_DROID | CAN_BARELY_JUMP | CAN_SELF_DESTRUCT | WEAPON_ZAPPER
    # todo?: Use hover time to determine jump distance instead of using the calculated value for their barely jump?
    return CharacterData.ap_item(character, abilities, 1.0, 0.11, 0.41, Alignment.PASSIVE)


def generic_clone(character: Character):
    abilities = IMPERIAL | COMMON_GRAPPLE | COMMON_PACIFIST_NON_DROID
    return CharacterData.ap_item(character, abilities, 1.0, 0.37, 0.7, Alignment.EVIL)


def generic_officer(character: Character, already_got_hat: bool = False):
    abilities = IMPERIAL | COMMON_GRAPPLE | COMMON_HATLESS_MELEE_NON_DROID
    if not already_got_hat:
        abilities |= CAN_WEAR_HAT
    return CharacterData.ap_item(character, abilities, 1.2, 0.44, 0.92, Alignment.EVIL)


def generic_lando(character: Character, already_got_hat: bool = False):
    abilities = COMMON_GRAPPLE | COMMON_MELEE_NON_DROID | CAN_REGULAR_DIVE_ROLL
    if not already_got_hat:
        abilities |= CAN_WEAR_HAT
    return CharacterData.ap_item(character, abilities, 1.18, 0.44, 0.90413, Alignment.GOOD)


def generic_padme(character: Character, can_melee: bool = True):
    if can_melee:
        abilities = COMMON_GRAPPLE | COMMON_HATLESS_MELEE_NON_DROID
    else:
        abilities = COMMON_GRAPPLE | COMMON_HATLESS_NON_DROID
    return CharacterData.ap_item(character, abilities, 1.2, 0.37, 0.84, Alignment.GOOD)


def generic_solo(character: Character):
    # todo: ViolaGuy's standalone TCS randomizer I think has some logic involving the roll that Han Solo can do.
    abilities = COMMON_GRAPPLE | COMMON_HATLESS_MELEE_NON_DROID | CAN_REGULAR_DIVE_ROLL
    return CharacterData.ap_item(character, abilities, 1.2, 0.37, 0.84, Alignment.GOOD)


def generic_leia(character: Character, already_got_hat: bool = False):
    abilities = COMMON_GRAPPLE | COMMON_MELEE_NON_DROID
    if not already_got_hat:
        abilities |= CAN_WEAR_HAT
    return CharacterData.ap_item(character, abilities, 1.2, 0.44, 0.92, Alignment.GOOD)


def generic_stormtrooper(character: Character):
    abilities = IMPERIAL | COMMON_GRAPPLE | COMMON_PACIFIST_NON_DROID | CAN_FLOP_JUMP
    return CharacterData.ap_item(character, abilities, 1.2, 0.44, 0.92, Alignment.EVIL)


def generic_rebel(character: Character):
    abilities = COMMON_GRAPPLE | COMMON_MELEE_NON_DROID
    return CharacterData.ap_item(character, abilities, 1.2, 0.44, 0.92, Alignment.GOOD)


def generic_greedo(character: Character):
    abilities = COMMON_BOUNTY_HUNTER | COMMON_MELEE_NON_DROID | CAN_REGULAR_DIVE_ROLL
    return CharacterData.ap_item(character, abilities, 1.2, 0.44, 0.92, Alignment.EVIL)


def generic_kaminoan(character: Character):
    abilities = COMMON_PACIFIST_NON_DROID
    return CharacterData.ap_item(character, abilities, 1.2, 0.37, 0.84, Alignment.NEUTRAL)


def generic_skiff_guard(character: Character, already_got_hat: bool = False):
    abilities = COMMON_GRAPPLE | COMMON_PACIFIST_NON_DROID
    if not already_got_hat:
        abilities |= CAN_WEAR_HAT
    return CharacterData.ap_item(character, abilities, 1.2, 0.44, 0.92, Alignment.EVIL)


def generic_battle_droid(character: Character):
    abilities = BLASTER | CAN_SELF_DESTRUCT
    return CharacterData.ap_item(character, abilities, 1.2, 0.0, 0.0, Alignment.EVIL)


def generic_yoda(character: Character, is_ghost: bool = False):
    # Yoda's low base movement speed greatly reduces his triple jump horizontal distance, so he cannot
    # CAN_TRIPLE_JUMP_GREAT_DISTANCE.
    abilities = JEDI | COMMON_MELEE_NON_DROID | CAN_DOUBLE_JUMP | CAN_DEFLECT_BOLTS | IS_NON_GHOST_JEDI
    if is_ghost:
        abilities &= MIXIN_FORCE_GHOST
        alignment = Alignment.PASSIVE
    else:
        alignment = Alignment.GOOD
    # todo: what is the effective run_speed with the lightsaber out and jumping?
    return CharacterData.ap_item(character, abilities, 0.8, 0.44, 0.6133333, alignment)


def generic_ewok(character: Character):
    abilities = WEAPON_EWOK | COMMON_SHORT_SLOW | CAN_JUMP_0_44
    return CharacterData.ap_item(character, abilities, 0.9, 0.44, 0.69, Alignment.GOOD)


def generic_protocol_droid(character: Character):
    abilities = PROTOCOL_PANEL | CAN_SELF_DESTRUCT
    return CharacterData.ap_item(character, abilities, 0.75, 0.0, 0.0, Alignment.PASSIVE)


def generic_wookie(character: Character):
    # Wookies can specially wear hats.
    abilities = COMMON_GRAPPLE | COMMON_HATLESS_MELEE_NON_DROID
    return CharacterData.ap_item(character, abilities, 1.2, 0.37, 0.84, Alignment.GOOD)


def generic_luke(character: Character, already_got_hat: bool = False):
    """Non-Jedi Luke specifically."""
    abilities = COMMON_GRAPPLE | COMMON_MELEE_NON_DROID | CAN_REGULAR_DIVE_ROLL
    if not already_got_hat:
        abilities |= CAN_WEAR_HAT
    return CharacterData.ap_item(character, abilities, 1.2, 0.44, 0.92, Alignment.GOOD)


def generic_geonosian(character: Character, abilities: CharacterAbility, alignment: Alignment):
    # Calculated jump distance is 1.2, but it's more like 0.75 or so.
    # Geonosian gets a jump, and then hovers slightly above the ground, which grants extra height.
    # Jump Distance:
    #  I could get across larger gaps, without elevation changes, than
    #  - run_speed=1.0, jump_speed=2.1, air_gravity=-6.0 -> jump_distance=0.7 (Clone).
    #  I could not get across as large gaps, without elevation changes, as
    #  - run_speed=1.32, jump_speed=2.4, air_gravity=-7.0 -> jump_distance=0.9 (Captain Tarpals)
    #  - run_speed=1.2, jump_speed=2.1, air_gravity=-6.0 -> jump_distance=0.84 (Padmé)
    #  - run_speed=1.0, jump_speed=2.3, air_gravity=-6.0 -> jump_distance=0.77777 (Dexter Jettster)
    #  Without elevation changes, I'm guessing the Geonosian jump_distance is around 0.75.
    #  There is an issue with gaps that have elevation changes however, since the flutter effect can quickly fall
    #  downwards. For example, on 3-6, in the lava platforming section, there is a jump from rib-like platforms to
    #  individual sinking platforms, and while Ewok (jump_distance=0.69) can barely make it to the first platform,
    #  Geonosian cannot. Geonosian does not seem far off from being able to make this jump, however, so I have given
    #  Geonosian a jump_distance of 0.65.
    # Jump Height:
    #  I could not jump as high as 4-LOM (0.37 jump height) and the only other characters that can jump worse are
    #  Astromech Droids.
    #  Geonosian can make it up the first two force steps in 3-3 (spawned by destroying the second explosives),
    #  Astromech Droids are not even close. These steps have about 0.3 y distance between them.
    return CharacterData.ap_item(character, abilities, 1.5, 0.3, 0.65)


_char = CharacterData.ap_item


NORMAL_CHARACTER_DATA: list[CharacterData] = [
    generic_jedi(Character.OBI_WAN_KENOBI),
    # There is a second, incorrect Zam Wesell at 305
    _char(Character.ZAM_WESELL, COMMON_BOUNTY_HUNTER | COMMON_MELEE_NON_DROID, 1.4, 0.4, 1.112, Alignment.EVIL),
    generic_sith(Character.THE_EMPEROR, True, True),
    _char(Character.BOBA_FETT, COMMON_JETPACK_BOUNTY_HUNTER, 1.2, 0.44, 0.92, Alignment.EVIL),
    generic_astromech(Character.R2_D2),
    _char(Character.TUSKEN_RAIDER, COMMON_GRAPPLE | COMMON_HATLESS_MELEE_NON_DROID, 1.2, 0.44, 0.92, Alignment.EVIL),
    generic_yoda(Character.YODA),
    generic_protocol_droid(Character.C_3PO),
    generic_rebel(Character.REBEL_TROOPER),
    generic_officer(Character.IMPERIAL_OFFICER, True),
    generic_wookie(Character.CHEWBACCA),
    _char(Character.GONK_DROID, CAN_SELF_DESTRUCT, 0.12, 0.0, 0.0, Alignment.PASSIVE),
    generic_stormtrooper(Character.STORMTROOPER),
    _char(Character.JAWA, SHORTIE | COMMON_PACIFIST_NON_DROID | WEAPON_ZAPPER, 0.9, 0.44, 0.69, Alignment.EVIL),
    generic_leia(Character.PRINCESS_LEIA),
    generic_leia(Character.PRINCESS_LEIA_HOTH),
    generic_jedi(Character.LUKE_SKYWALKER_BESPIN),
    generic_jedi(Character.LUKE_SKYWALKER_ENDOR, True),
    generic_jedi(Character.LUKE_SKYWALKER_JEDI),
    generic_luke(Character.LUKE_SKYWALKER_TATOOINE),
    generic_luke(Character.LUKE_SKYWALKER_STORMTROOPER),
    generic_solo(Character.HAN_SOLO),
    generic_solo(Character.HAN_SOLO_STORMTROOPER),
    generic_lando(Character.LANDO_CALRISSIAN),
    generic_sith(Character.DARTH_VADER, True, True),
    generic_stormtrooper(Character.BEACH_TROOPER),
    generic_stormtrooper(Character.SNOWTROOPER),
    generic_stormtrooper(Character.DEATH_STAR_TROOPER),
    generic_stormtrooper(Character.TIE_FIGHTER_PILOT),
    generic_stormtrooper(Character.SANDTROOPER),
    generic_officer(Character.IMPERIAL_SHUTTLE_PILOT, True),
    generic_jedi(Character.BEN_KENOBI),
    # Has special hair that apparently counts as a hat.
    generic_leia(Character.PRINCESS_LEIA_BESPIN, True),
    generic_rebel(Character.REBEL_PILOT),
    _char(Character.JANGO_FETT, COMMON_JETPACK_BOUNTY_HUNTER, 1.2, 0.44, 0.92, Alignment.EVIL),
    # Can build for some reason???
    _char(Character.GENERAL_GRIEVOUS,
          COMMON_HIGH_JUMP_SLAM | CAN_BUILD_BRICKS | CAN_TRIPLE_JUMP_GREAT_DISTANCE,
          1.2, 0.65, 1.12, Alignment.EVIL),
    generic_sith(Character.DARTH_MAUL, True),
    generic_jedi(Character.MACE_WINDU),
    generic_jedi(Character.MACE_WINDU_EPISODE_III),
    _char(Character.GRIEVOUS_BODYGUARD, COMMON_HIGH_JUMP_SLAM, 1.4, 1.44, 1.6, Alignment.EVIL),
    _char(Character.DROIDEKA, BLASTER | CAN_SELF_DESTRUCT, 1.8, 0.0, 0.0, Alignment.EVIL),
    generic_astromech(Character.R4_P17),
    generic_battle_droid(Character.BATTLE_DROID),
    generic_battle_droid(Character.BATTLE_DROID_COMMANDER),
    generic_battle_droid(Character.BATTLE_DROID_GEONOSIS),
    generic_battle_droid(Character.BATTLE_DROID_SECURITY),
    generic_protocol_droid(Character.TC_14),
    generic_wookie(Character.WOOKIEE),
    _char(Character.CHANCELLOR_PALPATINE, COMMON_HATLES_PACIFIST_NON_DROID, 1.2, 0.37, 0.84, Alignment.GOOD),
    generic_jedi(Character.OBI_WAN_KENOBI_EPISODE_III),
    generic_jedi(Character.OBI_WAN_KENOBI_JEDI_MASTER),
    generic_padme(Character.PADME),
    generic_padme(Character.PADME_BATTLE),
    generic_padme(Character.PADME_CLAWED),
    generic_padme(Character.PADME_GEONOSIS, can_melee=False),
    _char(Character.QUEEN_AMIDALA, COMMON_GRAPPLE | COMMON_MELEE_NON_DROID, 1.2, 0.37, 0.84, Alignment.GOOD),
    _char(Character.SUPER_BATTLE_DROID, BLASTER | CAN_SELF_DESTRUCT, 1.07, 0.0, 0.0, Alignment.EVIL),
    generic_jedi(Character.KI_ADI_MUNDI, True),
    generic_jedi(Character.KIT_FISTO, True),
    generic_jedi(Character.LUMINARA, True),
    generic_jedi(Character.SHAAK_TI, True),
    generic_clone(Character.CLONE),
    generic_clone(Character.CLONE_EPISODE_III),
    generic_clone(Character.CLONE_EPISODE_III_PILOT),
    generic_clone(Character.COMMANDER_CODY),
    generic_clone(Character.CLONE_EPISODE_III_SWAMP),
    generic_clone(Character.CLONE_EPISODE_III_WALKER),
    generic_clone(Character.DISGUISED_CLONE),
    _char(Character.ANAKIN_SKYWALKER_BOY, SHORTIE | COMMON_PACIFIST_NON_DROID, 1.2, 0.37, 0.84, Alignment.GOOD),
    _char(Character.BOBA_FETT_BOY, COMMON_SHORT_SLOW, 0.8, 0.37, 0.56, Alignment.EVIL),
    # Cannot build.
    # Like Watto, they cannot jump normally, but fly instead, with similar jump distance to Ewok.
    # TODO: Find something that another 0.4 height user can just barely get onto, or otherwise figure out the effective
    #  jump height for Geonosian.
    generic_geonosian(Character.GEONOSIAN,
                      CAN_PULL_LEVERS | CAN_PUSH_OBJECTS | CAN_RIDE_VEHICLES | BLASTER | CAN_JUMP_HEIGHT_0_37,
                      Alignment.EVIL),
    generic_jedi(Character.ANAKIN_SKYWALKER_JEDI),
    generic_jedi(Character.ANAKIN_SKYWALKER_PADAWAN),
    _char(Character.CAPTAIN_PANAKA, COMMON_GRAPPLE | COMMON_MELEE_NON_DROID, 1.2, 0.37, 0.84, Alignment.GOOD),
    # Jar Jar has a vanilla bug where there is a typo in the lever pulling animation, which prevents Jar Jar, and
    # Gungans based on him, from being able to pull levers.
    _char(Character.JAR_JAR_BINKS,
          COMMON_HIGH_JUMP
          | CAN_BUILD_BRICKS
          | CAN_PUSH_OBJECTS
          | CAN_RIDE_VEHICLES
          | CAN_AGGRAVATE_ENEMIES,
          1.32, 0.41, 0.905, Alignment.GOOD),
    _char(Character.PK_DROID, CAN_SELF_DESTRUCT, 0.8285375, 0.0, 0.0, Alignment.PASSIVE),
    _char(Character.ROYAL_GUARD, COMMON_GRAPPLE | COMMON_PACIFIST_NON_DROID, 1.2, 0.37, 0.84, Alignment.GOOD),
    # Crazy jump height on such an unassuming character!
    _char(Character.GAMORREAN_GUARD, COMMON_MELEE_NON_DROID | CAN_DEFLECT_BOLTS, 0.75, 0.53, 0.69, Alignment.EVIL),
    generic_sith(Character.COUNT_DOOKU, False, False),
    generic_jedi(Character.QUI_GON_JINN),
    generic_rebel(Character.REBEL_TROOPER_HOTH),
    generic_leia(Character.PRINCESS_LEIA_BOUSHH),
    generic_officer(Character.GRAND_MOFF_TARKIN),
    generic_solo(Character.HAN_SOLO_SKIFF),
    # Can wear hats despite the hood.
    generic_solo(Character.HAN_SOLO_HOOD),
    generic_solo(Character.HAN_SOLO_HOTH),
    generic_luke(Character.LUKE_SKYWALKER_PILOT),
    generic_jedi(Character.LUKE_SKYWALKER_DAGOBAH),
    _char(Character.UGNAUGHT, COMMON_SHORT_SLOW | WEAPON_ZAPPER, 0.9, 0.44, 0.69, Alignment.EVIL),
    generic_leia(Character.PRINCESS_LEIA_SLAVE),
    generic_leia(Character.PRINCESS_LEIA_ENDOR, True),
    # Custom characters can only use unlocked character equipment, besides some blasters. They do not get access to
    # lightsabers/force unless Jedi are unlocked.
    _char(Character.STRANGER_1, COMMON_GRAPPLE | COMMON_HATLESS_MELEE_NON_DROID, 1.2, 0.44, 0.92, Alignment.GOOD),
    _char(Character.STRANGER_2, COMMON_GRAPPLE | COMMON_HATLESS_MELEE_NON_DROID, 1.2, 0.44, 0.92, Alignment.GOOD),
    generic_greedo(Character.GREEDO),
    # GOOD alignment for some reason.
    _char(Character.IMPERIAL_SPY, COMMON_PACIFIST_NON_DROID, 1.2, 0.44, 0.92, Alignment.GOOD),
    # GOOD alignment for some reason.
    _char(Character.BIB_FORTUNA, COMMON_MELEE_NON_DROID, 1.2, 0.44, 0.92, Alignment.GOOD),
    generic_skiff_guard(Character.SKIFF_GUARD),
    generic_rebel(Character.REBEL_FRIEND),
    _char(Character.LOBOT, COMMON_HATLESS_MELEE_NON_DROID, 1.2, 0.44, 0.92, Alignment.GOOD),
    _char(Character.BESPIN_GUARD,
          COMMON_GRAPPLE
          | COMMON_MELEE_NON_DROID
          | CAN_REGULAR_DIVE_ROLL,
          1.2, 0.44, 0.92, Alignment.GOOD),
    _char(Character.IMPERIAL_GUARD,
          IMPERIAL | COMMON_MELEE_NON_DROID | CAN_DEFLECT_BOLTS,
          1.2, 0.44, 0.92, Alignment.EVIL),
    generic_jedi(Character.BEN_KENOBI_GHOST, False, True),
    generic_skiff_guard(Character.PALACE_GUARD, True),
    _char(Character.IG_88,
          COMMON_BOUNTY_HUNTER
          | ASTROMECH_PANEL
          | PROTOCOL_PANEL
          | CAN_PUSH_OBJECTS
          | CAN_JUMP_HEIGHT_0_37
          | CAN_RIDE_VEHICLES
          | CAN_MELEE,
          1.2, 0.44, 0.92, Alignment.EVIL),
    generic_ewok(Character.EWOK),
    generic_lando(Character.LANDO_PALACE_GUARD, True),
    generic_luke(Character.LUKE_SKYWALKER_HOTH, True),
    generic_leia(Character.PRINCESS_LEIA_PRISONER),
    generic_solo(Character.HAN_SOLO_ENDOR),
    generic_rebel(Character.CAPTAIN_ANTILLES),
    _char(Character.ADMIRAL_ACKBAR,
          COMMON_GRAPPLE
          | COMMON_PACIFIST_NON_DROID
          | CAN_DOUBLE_JUMP,
          1.2, 0.44, 0.92, Alignment.GOOD),
    generic_greedo(Character.BOSSK),
    generic_greedo(Character.DENGAR),
    generic_ewok(Character.WICKET),
    # Lower jump height than IG-88.
    _char(Character.FOUR_LOM,
          COMMON_BOUNTY_HUNTER
          | ASTROMECH_PANEL
          | PROTOCOL_PANEL
          | CAN_PUSH_OBJECTS
          | CAN_JUMP_HEIGHT_0_37
          | CAN_RIDE_VEHICLES
          | CAN_MELEE,
          1.2, 0.37, 0.84, Alignment.EVIL),
    generic_jedi(Character.ANAKIN_SKYWALKER_GHOST, False, True),
    generic_yoda(Character.YODA_GHOST, True),
    _char(Character.BOSS_NASS, COMMON_PACIFIST_NON_DROID, 1.0, 0.37, 0.7, Alignment.GOOD),
    _char(Character.PIT_DROID, CAN_SELF_DESTRUCT, 0.8, 0.0, 0.0, Alignment.PASSIVE),
    # Cannot build.
    generic_geonosian(Character.WATTO,
                      CAN_PULL_LEVERS | CAN_PUSH_OBJECTS | CAN_RIDE_VEHICLES | WEAPON_ZAPPER | CAN_JUMP_HEIGHT_0_37,
                      Alignment.GOOD),
    # Due to being based on Jar Jar, he cannot pull levers.
    _char(Character.CAPTAIN_TARPALS,
          COMMON_HIGH_JUMP
          | CAN_BUILD_BRICKS
          | CAN_PUSH_OBJECTS
          | CAN_RIDE_VEHICLES
          | CAN_MELEE
          | CAN_DEFLECT_BOLTS,
          1.32, 0.41, 0.905, Alignment.GOOD),
    generic_kaminoan(Character.LAMA_SU),
    generic_kaminoan(Character.TAUN_WE),
    # Unusual jump distance.
    _char(Character.DEXTER_JETTSTER, COMMON_PACIFIST_NON_DROID, 1.0, 0.44, 0.76666, Alignment.GOOD),
    generic_astromech(Character.R2_Q5),
    generic_jedi(Character.AAYLA_SECURA, True),
    generic_jedi(Character.PLO_KOON, True),
    # TODO: Check he can wear hats.
    generic_solo(Character.INDIANA_JONES),

    # This is an additional character to define the abilities of Gonk Droid when the Super Gonk Extra is active.
    CharacterData.event("Super Gonk Droid", Character.EVENT_SUPER_GONK_DROID, CAN_SELF_DESTRUCT,
                        1.44, 0.53, 1.325, Alignment.PASSIVE),
]

EXTRA_CHARACTER_DATA: list[CharacterData] = [
    # "Extra Toggle" characters.
    # Floats above the ground, with hover_height=0.25, which prevents the last safe position from updating.
    # Shoots short range blaster bolts that deal no damage to enemies, but can destroy objects and are affected by
    # Exploding Blaster Bolts (allowing dealing damage to enemies). The 0-damage blaster bolts will also aggro enemies.
    # todo: Find out what height of obstacle it can float over, guessing at least 0.15 for now.
    # TODO: Find out what distance it can 'jump'. Since it cannot actually jump, and instead floats
    _char(Character.TRAINING_REMOTE, CAN_SELF_DESTRUCT | CAN_AGGRAVATE_ENEMIES, 1.05, 0.25, 0.0, Alignment.NEUTRAL),
    generic_stormtrooper(Character.SCOUT_TROOPER),
    _char(Character.HAN_SOLO_FROZEN_IN_CARBONITE, CharacterAbility.NONE, 0.75, 0.0, 0.0, Alignment.GOOD),
    _char(Character.WOMP_RAT, CharacterAbility.NONE, 1.8, 0.0, 0.0, Alignment.PASSIVE),
    _char(Character.DROID_1, BLASTER | CAN_SELF_DESTRUCT, 0.6, 0.0, 0.0, Alignment.PASSIVE),
    _char(Character.DROID_2, BLASTER | CAN_SELF_DESTRUCT, 0.6, 0.0, 0.0, Alignment.PASSIVE),
    _char(Character.DROID_3, BLASTER | CAN_SELF_DESTRUCT, 0.4, 0.0, 0.0, Alignment.PASSIVE),
    _char(Character.DROID_4, BLASTER | CAN_SELF_DESTRUCT, 0.6, 0.0, 0.0, Alignment.PASSIVE),
    _char(Character.MOUSE_DROID, CAN_SELF_DESTRUCT, 2.4, 0.0, 0.0, Alignment.PASSIVE),
    generic_rebel(Character.REBEL_ENGINEER),
    generic_stormtrooper(Character.AT_AT_DRIVER),
    # Explicitly marked as being able to jump with 0.44 height, but cannot actually jump in-game.
    _char(Character.SKELETON, CAN_MELEE, 1.2, 0.0, 0.0, Alignment.GOOD),
    generic_stormtrooper(Character.IMPERIAL_ENGINEER),
    # Note: It's melee attack is a regular melee attack, not a combo melee attack.
    _char(Character.BUZZ_DROID, CAN_SELF_DESTRUCT | CAN_MELEE, 1.2, 0.0, 0.0, Alignment.EVIL),
]

# todo: This should not be needed at all, all that is needed is the Character.MAPCAR.
# Miscellaneous.
# This is the vehicle present in the outside area of the Cantina. 'map' is the internal name for the Cantina.
CANTINA_CAR = _char(Character.MAPCAR, CharacterAbility.NONE, 2.0, 0.0, 0.0, Alignment.GOOD),

assert len(EXTRA_TOGGLE_LOGIC_RELEVANT_CHARACTERS) == len(EXTRA_CHARACTER_DATA)

NON_VEHICLE_NORMAL_CHARACTER_TO_ITEM_DATA: dict[Character, CharacterData] = {
    data.character: data for data in NORMAL_CHARACTER_DATA
}
NON_VEHICLE_EXTRA_CHARACTER_TO_ITEM_DATA: dict[Character, CharacterData] = {
    data.character: data for data in EXTRA_CHARACTER_DATA
}

NON_VEHICLE_CHARACTER_TO_ITEM_DATA: dict[Character, CharacterData] = {
    **NON_VEHICLE_NORMAL_CHARACTER_TO_ITEM_DATA,
    **NON_VEHICLE_EXTRA_CHARACTER_TO_ITEM_DATA,
}
assert len(NON_VEHICLE_CHARACTER_TO_ITEM_DATA) == (
        len(NON_VEHICLE_NORMAL_CHARACTER_TO_ITEM_DATA) + len(NON_VEHICLE_EXTRA_CHARACTER_TO_ITEM_DATA)
)

def _make_single_jump_distance_relevant_characters_by_jump_distance() -> dict[float, list[Character]]:
    jump_distance_to_characters: dict[float, list[Character]] = {}
    for c in NON_VEHICLE_NORMAL_CHARACTER_TO_ITEM_DATA.values():
        if (HOVER | CAN_DOUBLE_JUMP) & c.abilities != 0:
            # Double jump and hover characters are always considered to have max jump distance.
            # Any need for logic beyond how far non-double-jump and non-hover characters can jump is handled separately.
            continue
        distance = c.single_jump_distance
        if distance in jump_distance_to_characters:
            jump_distance_to_characters[distance].append(c.character)
        else:
            jump_distance_to_characters[distance] = [c.character]

    # Sort by jump distance and then return.
    return dict(sorted(jump_distance_to_characters.items(), key=lambda t: t[0]))


SORTED_SINGLE_JUMP_DISTANCE_TO_CHARACTERS = _make_single_jump_distance_relevant_characters_by_jump_distance()
del _make_single_jump_distance_relevant_characters_by_jump_distance
