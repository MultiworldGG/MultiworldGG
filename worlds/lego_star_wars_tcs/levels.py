import struct
from dataclasses import dataclass, field
from typing import ClassVar, NamedTuple

from .constants import (
    CharacterAbility,
    HIGH_JUMP,
    IMPERIAL,
    SHORTIE,
    SITH,
    HOVER,
    BOUNTY_HUNTER,
    ASTROMECH,
    BLASTER,
    PROTOCOL_DROID,
    JEDI,
    VEHICLE_TIE,
    VEHICLE_TOW,
    CAN_WEAR_HAT,
    CAN_BUILD_BRICKS,
    CAN_PULL_LEVERS,
    CAN_ATTACK_UP_CLOSE,
    CAN_PUSH_OBJECTS,
    CAN_RIDE_VEHICLES,
    IS_A_VEHICLE,
    CHAPTER_SPECIFIC_FLAGS,
)
from .items import SHOP_SLOT_REQUIREMENT_TO_UNLOCKS, CHARACTERS_AND_VEHICLES_BY_NAME


@dataclass(frozen=True)
class ChapterArea:
    """
    Each game level/chapter within an Episode, e.g. 1-4 is represented by an Area, see AREAS.TXT.

    Does not include Character Bonus, Minikit Bonus, or Superstory, though the first two do have their own Areas.
    """
    # Used as a bool or as `value > 0`. The bits other than the first get preserved, so it appears to be safe to store
    # arbitrary data in the remaining 7 bits.
    UNLOCKED_OFFSET: ClassVar[int] = 0

    # Used as a bool or as `value > 0`. The bits other than the first get preserved, so it appears to be safe to store
    # arbitrary data in the remaining 7 bits, which is where the client stores Free Play completion.
    STORY_COMPLETE_OFFSET: ClassVar[int] = 1

    # Used as a bool or as `value > 0`. The bits other than the first get preserved, so it appears to be safe to store
    # arbitrary data in the remaining 7 bits.
    TRUE_JEDI_COMPLETE_OFFSET: ClassVar[int] = 2

    # The 3rd byte also gets set when True Jedi is completed. Having either the second byte or the second byte as
    # nonzero counts for True Jedi being completed.
    # Maybe one of the two bytes is a leftover from having separate True Jedi for Story and Free Play originally, like
    # in some later, non-Star Wars games?
    TRUE_JEDI_COMPLETE_2_OFFSET: ClassVar[int] = 3

    # Used as a bool or as `value > 0`. The bits other than the first get preserved, so it appears to be safe to store
    # arbitrary data in the remaining 7 bits.
    MINIKIT_GOLD_BRICK_OFFSET: ClassVar[int] = 4

    # Setting this to 10 or higher will prevent newly collected minikits from being saved as collected.
    MINIKIT_COUNT_OFFSET: ClassVar[int] = 5

    # Must be exactly `1`
    POWER_BRICK_COLLECTED_OFFSET: ClassVar[int] = 6

    # Used as a bool or as `value > 0`. The bits other than the first get preserved, so it appears to be safe to store
    # arbitrary data in the remaining 7 bits.
    CHALLENGE_COMPLETE_OFFSET: ClassVar[int] = 7

    # Unused, 4-byte float that preserves NaN signal bits and appears to never be written to normally, so can be used to
    # store arbitrary data.
    UNUSED_CHALLENGE_BEST_TIME_OFFSET: ClassVar[int] = 8
    # The default, unused value is 1200 seconds, or 20 minutes, as a single-precision float.
    UNUSED_CHALLENGE_BEST_TIME_VALUE: ClassVar[bytes] = struct.pack("f", 1200.0)

    name: str
    # The episode this Area is in.
    episode: int
    # The number within the episode that this Area is in.
    number_in_episode: int
    # # Level IDs, see the order of the levels defined in LEVELS.TXT.
    # # These are the individual playable 'levels' within a game level, and also include intros, outros and the 'status'
    # # screen at the end of a game level.
    # level_ids: set[int]
    # The address in the in-memory save data that stores most of the Area information.
    address: int
    # The level ID of the 'status' screen used when tallying up collected studs/minikits/etc., either from
    # "Save and Exit to Cantina", or from completing the level.
    status_level_id: int
    area_id: int
    story_true_jedi_requirement: int
    free_play_true_jedi_requirement: int
    # Index of the AreaData* for this area. AreaData is where the level IDs are stored, as well as True Jedi
    # requirements. Generally, the indices are in Episode and Chapter order, except 3-1 has two separate pointers in the
    # array for some reason. The array starts at 0x0087af70 (GOG).
    # Not currently used.
    unused_p_area_data_index: int
    ## The address of each Level in the area with minikits, and the names of the minikits in that Level.
    #minikit_address_to_names: dict[int, set[str]]
    # TODO: Convert this file mostly into a script that writes `print(repr(GAME_LEVEL_AREAS))`
    short_name: str = field(init=False)
    character_requirements: frozenset[str] = field(init=False)
    alt_character_requirements: frozenset[str] = field(init=False)
    character_shop_unlocks: dict[str, int] = field(init=False)
    power_brick_ability_requirements: tuple[CharacterAbility, ...] = field(init=False)
    power_brick_location_name: str = field(init=False)
    power_brick_studs_cost: int = field(init=False)
    all_minikits_ability_requirements: tuple[CharacterAbility, ...] = field(init=False)
    completion_main_ability_requirements: CharacterAbility = field(init=False)
    """
    The combined, main abilities of the Story mode characters for this chapter.
    """
    completion_alt_ability_requirements: CharacterAbility | None = field(init=False)
    """
    Alternative chapter-specific logic that usually replaces a common requirement from the main ability requirements
    with a rarer ability, e.g. replacing "CAN_WEAR_HAT" with "IMPERIAL" if the normal requirement would be to use a Hat
    Machine to use an Imperial panel.
    These requirements should not be used for the starting chapter because it is undesirable to force the player to
    start with a rarer ability.
    """
    boss: str | None = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, "short_name", f"{self.episode}-{self.number_in_episode}")

        character_requirements = CHAPTER_AREA_STORY_CHARACTERS[self.short_name]
        object.__setattr__(self, "character_requirements", character_requirements)

        character_shop_unlock_data = SHOP_SLOT_REQUIREMENT_TO_UNLOCKS.get(self.short_name, {})
        object.__setattr__(self, "alt_character_requirements", frozenset(character_shop_unlock_data.keys()))

        character_shop_unlocks = {f"Purchase {character} ({self.short_name})": price for character, price
                                  in character_shop_unlock_data.items()}
        object.__setattr__(self, "character_shop_unlocks", character_shop_unlocks)

        power_brick = POWER_BRICK_REQUIREMENTS[self.short_name]
        power_brick_location_name = f"Purchase {power_brick.name} ({self.short_name})"
        object.__setattr__(self, "power_brick_location_name", power_brick_location_name)
        power_brick_ability_requirements = power_brick.ability_requirements
        if power_brick_ability_requirements is None:
            power_brick_ability_requirements = (CharacterAbility.NONE,)
        elif isinstance(power_brick_ability_requirements, CharacterAbility):
            power_brick_ability_requirements = (power_brick_ability_requirements,)
        object.__setattr__(self, "power_brick_ability_requirements", power_brick_ability_requirements)
        object.__setattr__(self, "power_brick_studs_cost", power_brick.studs_cost)

        all_minikits_ability_requirements = ALL_MINIKITS_REQUIREMENTS[self.short_name]
        object.__setattr__(self, "all_minikits_ability_requirements", all_minikits_ability_requirements)

        boss = BOSS_CHARACTERS_BY_SHORTNAME.get(self.short_name)
        object.__setattr__(self, "boss", boss)

        base_entrance_abilities = CharacterAbility.NONE
        for character in character_requirements:
            base_entrance_abilities |= CHARACTERS_AND_VEHICLES_BY_NAME[character].abilities
        # Strip all chapter-specific flags. If there are any that are relevant to this chapter, they will be re-added in
        # the next step.
        base_entrance_abilities &= ~CHAPTER_SPECIFIC_FLAGS
        # Add any chapter-specific flags and set possible alternatives
        completion_alt_ability_requirements = None
        if chapter_specific_requirement := CHAPTER_SPECIFIC_REQUIREMENTS.get(self.short_name):
            story_logic, alternative_ability = chapter_specific_requirement
            completion_main_ability_requirements = base_entrance_abilities | story_logic
            if alternative_ability is not None and alternative_ability not in base_entrance_abilities:
                # Define an alternative set of requirements.
                completion_alt_ability_requirements = (base_entrance_abilities & ~story_logic) | alternative_ability
        else:
            completion_main_ability_requirements = base_entrance_abilities
        if completion_main_ability_requirements is CharacterAbility.NONE:
            raise AssertionError("Every chapter should have at least one CharacterAbility requirement.")
        if completion_alt_ability_requirements is CharacterAbility.NONE:
            raise AssertionError("Every chapter's alternate requiremenents should have at least one CharacterAbility"
                                 " requirement.")
        object.__setattr__(self, "completion_main_ability_requirements", completion_main_ability_requirements)
        object.__setattr__(self, "completion_alt_ability_requirements", completion_alt_ability_requirements)

    @property
    def unique_boss_name(self) -> str | None:
        boss = self.boss
        if boss is None:
            return None
        return f"{boss} ({self.short_name})"


@dataclass(frozen=True)
class BonusArea:
    name: str
    address: int
    completion_offset: int
    """
    The cheat table listing the addresses listed a base address with unknown purpose for the bonus levels, and then an
    offset from that address for the completion byte, so that is why there is an offset separate from the address.
    """
    status_level_id: int
    area_id: int
    item_requirements: tuple[str, ...] = ()
    completion_ability_requirements: CharacterAbility = CharacterAbility.NONE
    gold_bricks_required: int = 0
    gold_brick: bool = True
    story_characters: frozenset[str] = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, "story_characters", BONUS_AREA_STORY_CHARACTERS.get(self.name, frozenset()))

    @property
    def completion_location_name(self) -> str:
        if self.gold_brick:
            return self.name + " Completion"
        else:
            # The only Bonus Area without a Gold Brick is not a level to complete, but watching the Indy Trailer.
            return self.name


# GameLevelArea short_name to the set of characters needed to unlock that GameLevelArea
# To find characters, grep the LEVELS directory for non-binary files, searching for '" player'. Note that vehicle levels
# typically have an alternate color scheme vehicle for Player 2 which may not be collectable.
CHAPTER_AREA_STORY_CHARACTERS: dict[str, frozenset[str]] = {
    k: frozenset(v) for k, v in {
        "1-1": {
            "Obi-Wan Kenobi",
            "Qui-Gon Jinn",
            "TC-14",
        },
        "1-2": {
            "Obi-Wan Kenobi",
            "Qui-Gon Jinn",
            "Jar Jar Binks",
        },
        "1-3": {
            "Obi-Wan Kenobi",
            "Qui-Gon Jinn",
            "Captain Panaka",
            "Queen Amidala",
        },
        "1-4": {
            "Anakin's Pod",
        },
        "1-5": {
            "Obi-Wan Kenobi",
            "Qui-Gon Jinn",
            "Anakin Skywalker (Boy)",
            "Captain Panaka",
            "Padmé (Battle)",
            "R2-D2",
        },
        "1-6": {
            "Obi-Wan Kenobi",
            "Qui-Gon Jinn",
        },
        "2-1": {
            "Anakin's Speeder",
        },
        "2-2": {
            "Obi-Wan Kenobi (Jedi Master)",
            "R4-P17",
        },
        "2-3": {
            "Anakin Skywalker (Padawan)",
            "C-3PO",
            "Padmé (Geonosis)",
            "R2-D2",
        },
        "2-4": {
            "Anakin Skywalker (Padawan)",
            "Mace Windu",
            "Padmé (Clawed)",
            "Obi-Wan Kenobi (Jedi Master)",
            "R2-D2",
        },
        "2-5": {
            "Republic Gunship",
        },
        "2-6": {
            "Anakin Skywalker (Padawan)",
            "Obi-Wan Kenobi (Jedi Master)",
            "Yoda",
        },
        "3-1": {
            "Anakin's Starfighter",
            "Obi-Wan's Starfighter",
            # These non-vehicle characters are also listed as player characters in the file, but do not get unlocked
            # when completing the chapter in Story mode, so should not be requirements to play the chapter:
            # "Obi-Wan Kenobi (Episode 3)",
            # "Anakin Skywalker (Jedi)",
        },
        "3-2": {
            "Anakin Skywalker (Jedi)",
            "Chancellor Palpatine",
            "Obi-Wan Kenobi (Episode 3)",
            "R2-D2",
        },
        "3-3": {
            "Commander Cody",
            "Obi-Wan Kenobi (Episode 3)",
        },
        "3-4": {
            "Chewbacca",
            "Yoda",
        },
        "3-5": {
            "Obi-Wan Kenobi (Episode 3)",
            "Yoda",
        },
        "3-6": {
            "Anakin Skywalker (Jedi)",
            "Obi-Wan Kenobi (Episode 3)",
        },
        "4-1": {
            "Captain Antilles",
            "C-3PO",
            "Princess Leia",
            "R2-D2",
            "Rebel Friend",
        },
        "4-2": {
            "Ben Kenobi",
            "C-3PO",
            "Luke Skywalker (Tatooine)",
            "R2-D2",
        },
        "4-3": {
            "Ben Kenobi",
            "C-3PO",
            "Chewbacca",
            "Han Solo",
            "Luke Skywalker (Tatooine)",
            "R2-D2",
        },
        "4-4": {
            "Ben Kenobi",
            "C-3PO",
            "Chewbacca",
            "Han Solo (Stormtrooper)",
            "Luke Skywalker (Stormtrooper)",
            "R2-D2",
        },
        "4-5": {
            "C-3PO",
            "Chewbacca",
            "Han Solo",
            "Luke Skywalker (Tatooine)",
            "Princess Leia",
            "R2-D2",
        },
        "4-6": {
            "X-Wing",
            "Y-Wing",
        },
        "5-1": {
            "Snowspeeder",
        },
        "5-2": {
            "C-3PO",
            "Chewbacca",
            "Han Solo (Hoth)",
            "Princess Leia (Hoth)",
        },
        "5-3": {
            "Millennium Falcon",
            "X-Wing",
        },
        "5-4": {
            "Luke Skywalker (Dagobah)",
            "Luke Skywalker (Pilot)",
            "R2-D2",
            "Yoda",
        },
        "5-5": {
            "Luke Skywalker (Bespin)",
            "R2-D2",
        },
        "5-6": {
            "C-3PO",
            "Lando Calrissian",
            "Princess Leia (Bespin)",
            "R2-D2",
            "Chewbacca",
        },
        "6-1": {
            "Chewbacca",
            "C-3PO",
            "Han Solo (Skiff)",
            "Princess Leia (Boushh)",
            "Luke Skywalker (Jedi)",
            "R2-D2",
        },
        "6-2": {
            "Chewbacca",
            "C-3PO",
            "Han Solo (Skiff)",
            "Princess Leia (Slave)",
            "Lando Calrissian (Palace Guard)",
            "Luke Skywalker (Jedi)",
            "R2-D2",
        },
        "6-3": {
            "Luke Skywalker (Endor)",
            "Princess Leia (Endor)",
        },
        "6-4": {
            "Chewbacca",
            "C-3PO",
            "Han Solo (Endor)",
            "Princess Leia (Endor)",
            "R2-D2",
            "Wicket",
        },
        "6-5": {
            "Darth Vader",
            "Luke Skywalker (Jedi)",
        },
        "6-6": {
            "Millennium Falcon",
            "X-Wing",
        }
    }.items()
}


BONUS_AREA_STORY_CHARACTERS: dict[str, frozenset[str]] = {
    k: frozenset(v) for k, v in {
        "Mos Espa Pod Race (Original)": {
            "Anakin's Pod",
        },
        "Anakin's Flight": {
            "Naboo Starfighter",
        },
        "Gunship Cavalry (Original)": {
            "Republic Gunship",
        },
        "A New Hope (Bonus Level)": {
            "Darth Vader",
            "C-3PO",
        }
    }.items()
}


class _PowerBrickData(NamedTuple):
    name: str
    ability_requirements: CharacterAbility | tuple[CharacterAbility, ...] | None
    studs_cost: int


POWER_BRICK_REQUIREMENTS: dict[str, _PowerBrickData] = {
    # Currently, these requirements assume access to the chapter requires all the abilities of the Story characters of
    # that chapter.
    "1-1": _PowerBrickData("Super Gonk", ASTROMECH, 100_000),
    "1-2": _PowerBrickData("Poo Money", BOUNTY_HUNTER, 100_000),
    "1-3": _PowerBrickData("Walkie Talkie Disable", BOUNTY_HUNTER | SITH, 5_000),
    "1-4": _PowerBrickData("Power Brick Detector", None, 125_000),
    "1-5": _PowerBrickData("Super Slap", None, 5_000),
    "1-6": _PowerBrickData("Force Grapple Leap", IMPERIAL, 15_000),
    "2-1": _PowerBrickData("Stud Magnet", None, 100_000),
    "2-2": _PowerBrickData("Disarm Troopers", IMPERIAL, 100_000),
    "2-3": _PowerBrickData("Character Studs", None, 100_000),
    "2-4": _PowerBrickData("Perfect Deflect", BOUNTY_HUNTER, 20_000),
    "2-5": _PowerBrickData("Exploding Blaster Bolts", None, 20_000),
    "2-6": _PowerBrickData("Force Pull", BOUNTY_HUNTER | SHORTIE, 12_000),
    "3-1": _PowerBrickData("Vehicle Smart Bomb", None, 15_000),
    "3-2": _PowerBrickData("Super Astromech", BOUNTY_HUNTER, 10_000),
    "3-3": _PowerBrickData("Super Jedi Slam", (HOVER, HIGH_JUMP), 11_000),
    "3-4": _PowerBrickData("Super Thermal Detonator", BOUNTY_HUNTER | SITH, 25_000),
    "3-5": _PowerBrickData("Deflect Bolts", SITH | HIGH_JUMP | PROTOCOL_DROID, 150_000),
    "3-6": _PowerBrickData("Dark Side", ASTROMECH, 25_000),
    "4-1": _PowerBrickData("Super Blasters", (JEDI | BOUNTY_HUNTER, JEDI | IMPERIAL), 15_000),
    "4-2": _PowerBrickData("Fast Force", BOUNTY_HUNTER, 40_000),
    "4-3": _PowerBrickData("Super Lightsabers", None, 40_000),
    "4-4": _PowerBrickData("Tractor Beam", None, 15_000),
    "4-5": _PowerBrickData("Invincibility", JEDI, 1_000_000),
    "4-6": _PowerBrickData("Score x2", None, 1_250_000),
    "5-1": _PowerBrickData("Self Destruct", VEHICLE_TIE, 25_000),
    "5-2": _PowerBrickData("Fast Build", SITH | ASTROMECH, 30_000),
    "5-3": _PowerBrickData("Score x4", None, 2_500_000),
    "5-4": _PowerBrickData("Regenerate Hearts", SITH, 150_000),
    "5-5": _PowerBrickData("Score x6", BOUNTY_HUNTER | HOVER | JEDI, 5_000_000),  # Note: In memory after Minikit Detector
    "5-6": _PowerBrickData("Minikit Detector", None, 250_000),  # Note: In memory before Score x6
    "6-1": _PowerBrickData("Super Zapper", None, 14_000),
    "6-2": _PowerBrickData("Bounty Hunter Rockets", None, 20_000),
    "6-3": _PowerBrickData("Score x8", SHORTIE, 10_000_000),
    "6-4": _PowerBrickData("Super Ewok Catapult", (SHORTIE | SITH | IMPERIAL, SHORTIE | SITH | CAN_WEAR_HAT), 25_000),
    "6-5": _PowerBrickData("Score x10", None, 20_000_000),  # Note: In memory after Infinite Torpedos
    "6-6": _PowerBrickData("Infinite Torpedos", None, 25_000),  # Note: In memory before Score x10
}

ALL_MINIKITS_REQUIREMENTS: dict[str, tuple[CharacterAbility, ...]] = {
    # Currently, these requirements assume access to the chapter requires all the abilities of the Story characters of
    # that chapter.
    "1-1": (HIGH_JUMP | ASTROMECH | HOVER | SHORTIE,),
    "1-2": (SHORTIE | BLASTER,),
    "1-3": (SITH | HIGH_JUMP | HOVER | BOUNTY_HUNTER | SHORTIE,),
    "1-4": (VEHICLE_TIE,),
    "1-5": (SITH | BOUNTY_HUNTER | HIGH_JUMP,),
    "1-6": (SITH | HIGH_JUMP | BLASTER | BOUNTY_HUNTER | IMPERIAL,),
    "2-1": (VEHICLE_TIE,),
    "2-2": (SITH | HIGH_JUMP | BLASTER | BOUNTY_HUNTER | SHORTIE | PROTOCOL_DROID,),
    "2-3": (HIGH_JUMP | IMPERIAL | SHORTIE,),
    "2-4": (HIGH_JUMP | SHORTIE,),
    "2-5": (VEHICLE_TIE,),
    "2-6": (HIGH_JUMP | BLASTER | ASTROMECH,),
    "3-1": (CharacterAbility.NONE,),
    "3-2": (HIGH_JUMP | BLASTER | SHORTIE | PROTOCOL_DROID,),
    "3-3": (HOVER | BOUNTY_HUNTER | HIGH_JUMP,),
    "3-4": (SITH | HIGH_JUMP | HOVER,),
    # Technically PROTOCOL_DROID is not required, but you must save and exit after getting the kit if you don't have
    # PROTOCOL_DROID, so PROTOCOL_DROID can be expected for the most basic logic difficulty only.
    "3-5": (SITH | HIGH_JUMP | BLASTER | HOVER | BOUNTY_HUNTER | IMPERIAL | PROTOCOL_DROID,),
    "3-6": (HOVER,),
    # At least one kit requires JEDI, but there is a kit that requires SITH, so JEDI does not need to be specified.
    "4-1": (SITH | BOUNTY_HUNTER | IMPERIAL,),
    "4-2": (SITH | BOUNTY_HUNTER | SHORTIE,),
    "4-3": (SITH | BOUNTY_HUNTER | SHORTIE,),
    "4-4": (SITH | BOUNTY_HUNTER | IMPERIAL,),
    # At least one kit requires JEDI, but there is a kit that requires SITH, so JEDI does not need to be specified.
    "4-5": (SITH | BOUNTY_HUNTER | IMPERIAL | SHORTIE,),
    "4-6": (VEHICLE_TOW | VEHICLE_TIE,),
    "5-1": (VEHICLE_TIE,),
    # At least one kit requires JEDI, but there is a kit that requires SITH, so JEDI does not need to be specified.
    "5-2": (SITH | HOVER | ASTROMECH | BOUNTY_HUNTER | SHORTIE,),
    "5-3": (VEHICLE_TOW | VEHICLE_TIE,),
    "5-4": (SITH | BOUNTY_HUNTER | SHORTIE,),
    "5-5": (SITH | BOUNTY_HUNTER | IMPERIAL | SHORTIE,),
    # At least one kit requires JEDI, but there is a kit that requires SITH, so JEDI does not need to be specified.
    "5-6": (SITH | BOUNTY_HUNTER,),
    "6-1": (SITH | SHORTIE | CAN_WEAR_HAT, SITH | SHORTIE | IMPERIAL),
    "6-2": (SITH | HOVER | SHORTIE,),
    "6-3": (SITH | BOUNTY_HUNTER | IMPERIAL | SHORTIE,),
    "6-4": (JEDI | BOUNTY_HUNTER,),
    # IMPERIAL has been considered a chapter-specific ability, so Darth Maul/Count Dooku are considered valid to
    # complete the chapter, and IMPERIAL must be specified for the Minikits.
    "6-5": (BLASTER | BOUNTY_HUNTER | SHORTIE | ASTROMECH | PROTOCOL_DROID | IMPERIAL,),
    "6-6": (VEHICLE_TIE,),
}

BOSS_CHARACTERS_BY_SHORTNAME: dict[str, str] = {
    "1-6": "Darth Maul",
    "2-1": "Zam Wesell",
    "2-2": "Jango Fett",
    "2-4": "Jango Fett",
    "2-6": "Count Dooku",
    "3-2": "Count Dooku",
    "3-3": "General Grievous",
    "3-6": "Anakin Skywalker",
    "4-3": "Imperial Spy",
    "4-6": "Death Star",
    "5-4": "Darth Vader",
    "5-5": "Darth Vader",
    "5-6": "Boba Fett",
    "6-1": "Rancor",
    "6-2": "Boba Fett",
    "6-5": "Darth Sidious",
    "6-6": "Death Star II",
}

# True Jedi that is difficult if not impossible in Free Play with just the Story characters for a level.
DIFFICULT_OR_IMPOSSIBLE_TRUE_JEDI: set[str] = {
    # I don't think this is possible, I tried before, even with maximum usage of Power Ups. Higher logic could probably
    # get this because they can jump to the top of the cylindrical area with all the Battle Droids, which has a bunch of
    # Blue Studs.
    "1-6",
    "2-6",  # I only managed 14180/22000
    "3-3",  # Barely possible by re-entering and getting studs that replace minikits
    "3-5",  # I managed only 40700/45000, even with 3 double jump slams to get 3 Blue Studs that were just too high.
    # Dying is easy in multiple areas, where even without deaths, it is barely possible.
    "3-6",
    # It's pretty slow, but possible to overshoot by 20K studs while mostly wasting the two Power Ups. If it is possible
    # to get 9/10 TIE Fighters in the Turbolaser control area towards the very end, then return to the previous room via
    # the elevator, go back to the Turbolasers and destroy the last TIE Fighter before the Power Up runs out, then
    # doubling the studs that spawn (around 20K) would be a huge benefit.
    # "4-4",
    # Possible to overshoot by 95K Studs, even without taking advantage of Power Ups, though it is slow, and a vehicle,
    # level, so dying a lot is expected. Vehicle chapters also just kind of suck for picking up studs. 4-6 could be
    # included in the difficult True Jedi if there are complaints.
    # "4-6",
    # Apparently barely possible by re-entering and getting studs that replace minikits. I find this vehicle chapter
    # especially difficult to actually pick studs up off the ground, and dying is also easy in this chapter.
    "5-1",
    # I only managed 53K/80K without deaths, but while wasting Power Ups. Even with Power Ups, 5-2 is looking clearly
    # impossible.
    "5-2",
    # If no studs are lost from dying and Power Ups are used to their fullest, then 5-6 is just barely possible
    # without getting Minikit Blue Studs, but by only around 100-200 Studs.
    "5-6",
    # I am assuming that the extra room where the door needs to be blown up is required to get True Jedi in 6-5.
    "6-5",
}


CHAPTER_SPECIFIC_REQUIREMENTS: dict[str, tuple[CharacterAbility, CharacterAbility | None]] = {
    # Mos Espa Pod Race does not require any Vehicle abilities, but does require having at least one vehicle character
    # unlocked, so extra logic is needed to ensure the player actually has a vehicle character.
    "1-4": (IS_A_VEHICLE, None),
    # There is a Hat Machine in Level D, which you can take all the way back to behind spawn to the Imperial Panel with
    # a Minikit behind.
    # All the characters that can wear hats can jump and can make it back to the panel.
    # todo: Maybe the most basic logic level should use (CAN_WEAR_HAT_AND_GRAPPLE or CAN_WEAR_HAT_AND_DOUBLE_JUMP)
    #  because CAN_WEAR_HAT on its own requires either a tight jump, or jumping off a small garbage bin than can be
    #  destroyed by accident.
    "4-3": (CAN_WEAR_HAT, CharacterAbility.IMPERIAL),
    # There is a section where a Stormtrooper helmet needs to be taken across a gap that requires grappling if you want
    # to keep the hat.
    "4-4": (CharacterAbility.CAN_WEAR_HAT_AND_GRAPPLE, CharacterAbility.IMPERIAL),
    # In 4-5, there is an Imperial Hat Machine with an Imperial panel that requires grappling across a gap to reach
    # (Level A), so, if the player has no Imperial character, they need a BLASTER character that can wear hats.
    # This additionally covers a later use of an Imperial Hat Machine where the panel is at the top of an elevator
    # (level B), and another later use of an Imperial Hat Machine where the panel is at the end of a Zipup, across a gap
    # (level C).
    "4-5": (CharacterAbility.CAN_WEAR_HAT_AND_GRAPPLE, CharacterAbility.IMPERIAL),
    "5-4": (CharacterAbility.CAN_DAGOBAH_SWAMP, None),
    # In 5-5, there is an Imperial Hat Machine with an Imperial panel that requires double-jumping across a gap to
    # reach, so, if the player has no Imperial character, they need a Jedi/Sith that can wear hats.
    # This gets its own flag, instead of being JEDI | CAN_WEAR_HAT, for logic performance reasons. The complexity comes
    # from the fact that characters may have additional flags, but the logic system prefers to store only the combined
    # flag of all currently usable abilities.
    "5-5": (CharacterAbility.CAN_WEAR_HAT_AND_DOUBLE_JUMP, CharacterAbility.IMPERIAL),
    # Level A has a Hat Machine where you need to walk to an elevator with the hat.
    "5-6": (CAN_WEAR_HAT, CharacterAbility.IMPERIAL),
    # The level is played in Story with a character than can wear hats instead of needing a bounty hunter.
    "6-1": (CAN_WEAR_HAT, CharacterAbility.BOUNTY_HUNTER),
}
"""
Chapter completions that require logic that is specific to that chapter.

The first element of each value are the abilities that would normally be used in Story mode.

The second element of each value is an optional alternative ability that can be used instead, but often requires a rarer
ability. 
"""


# TODO: Record Level IDs, these would mostly be there to help make map switching in the tracker easier, and would
#  serve as a record of data that might be useful for others.
CHAPTER_AREAS = [
    # area -1/255 = Cantina, AreaData* index ??
    ChapterArea("Negotiations", 1, 1, 0x86E0F4, 7, 0, 31000, 64000, 0),
    ChapterArea("Invasion of Naboo", 1, 2, 0x86E100, 15, 1, 44000, 52000, 1),
    ChapterArea("Escape From Naboo", 1, 3, 0x86E10C, 24, 2, 48000, 60000, 2),
    ChapterArea("Mos Espa Pod Race", 1, 4, 0x86E118, 37, 3, 45000, 45000, 3),
    # area 4 = Bonus: Pod Race (Original), AreaData* index 49
    ChapterArea("Retake Theed Palace", 1, 5, 0x86E130, 48, 5, 60000, 100000, 4),
    ChapterArea("Darth Maul", 1, 6, 0x86E13C, 55, 6, 31000, 64000, 5),
    # area 7 = EP1 Ending
    # area 8 = EP1 Character Bonus, AreaData* index 37
    # area 9 = EP1 Minikit Bonus. Episode Bonus doors show the Minikit Bonus Area ID rather than Character Bonus Area ID
    # AreaData* index 43
    ChapterArea("Bounty Hunter Pursuit", 2, 1, 0x86E16C, 68, 10, 35000, 45000, 6),
    ChapterArea("Discovery On Kamino", 2, 2, 0x86E178, 78, 11, 50000, 65000, 7),
    ChapterArea("Droid Factory", 2, 3, 0x86E184, 88, 12, 40000, 55000, 8),
    ChapterArea("Jedi Battle", 2, 4, 0x86E190, 92, 13, 8000, 16000, 9),
    ChapterArea("Gunship Cavalry", 2, 5, 0x86E19C, 95, 14, 30000, 40000, 10),
    # area 15 = Bonus: Gunship Cavalry (Original), AreaData* index 51
    ChapterArea("Count Dooku", 2, 6, 0x86E1B4, 103, 16, 10000, 22000, 11),
    # area 17 = EP2 Ending
    # area 18 = EP2 Character Bonus, AreaData* index 38
    # area 19 = EP2 Minikit Bonus, AreaData* index 44
    ChapterArea("Battle Over Coruscant", 3, 1, 0x86E1E4, 111, 20, 75000, 75000, 12),
    ChapterArea("Chancellor In Peril", 3, 2, 0x86E1F0, 121, 21, 60000, 80000, 14),
    ChapterArea("General Grievous", 3, 3, 0x86E1FC, 123, 22, 3300, 5000, 15),
    ChapterArea("Defense Of Kashyyyk", 3, 4, 0x86E208, 128, 23, 65000, 90000, 16),
    ChapterArea("Ruin Of The Jedi", 3, 5, 0x86E214, 134, 24, 35000, 75000, 17),
    ChapterArea("Darth Vader", 3, 6, 0x86E220, 139, 25, 25000, 45000, 18),
    # area 26 = EP3 Ending
    # area 27 = EP3 Character Bonus, AreaData* index 39
    # area 28 = EP3 Minikit Bonus, AreaData* index 45
    # area 29 = Bonus: A New Hope, AreaData* index 52
    ChapterArea("Secret Plans", 4, 1, 0x86E25C, 159, 30, 28000, 40000, 19),
    ChapterArea("Through The Jundland Wastes", 4, 2, 0x86E268, 167, 31, 60000, 90000, 20),
    ChapterArea("Mos Eisley Spaceport", 4, 3, 0x86E274, 177, 32, 60000, 100000, 21),
    ChapterArea("Rescue The Princess", 4, 4, 0x86E280, 185, 33, 60000, 80000, 22),
    ChapterArea("Death Star Escape", 4, 5, 0x86E28C, 192, 34, 45000, 65000, 23),
    ChapterArea("Rebel Attack", 4, 6, 0x86E298, 203, 35, 30000, 45000, 24),
    # area 36 = EP4 Ending
    # area 37 = EP4 Character Bonus, AreaData* index 40
    # area 38 = EP4 Minikit Bonus, AreaData* index 46
    ChapterArea("Hoth Battle", 5, 1, 0x86E2C8, 219, 39, 25000, 35000, 25),
    ChapterArea("Escape From Echo Base", 5, 2, 0x86E2D4, 228, 40, 40000, 80000, 26),
    ChapterArea("Falcon Flight", 5, 3, 0x86E2E0, 236, 41, 30000, 48000, 27),
    ChapterArea("Dagobah", 5, 4, 0x86E2EC, 244, 42, 52000, 72000, 28),
    # 5-5 levels are after 5-6 levels for some reason.
    ChapterArea("Cloud City Trap", 5, 5, 0x86E2F8, 257, 43, 14000, 22000, 29),
    ChapterArea("Betrayal Over Bespin", 5, 6, 0x86E304, 251, 44, 34000, 60000, 30),
    # area 45 = EP5 Ending
    # area 46 = EP5 Character Bonus, AreaData* index 41
    # area 47 = EP5 Minikit Bonus, AreaData* index 47
    ChapterArea("Jabba's Palace", 6, 1, 0x86E334, 271, 48, 43000, 60000, 31),
    ChapterArea("The Great Pit Of Carkoon", 6, 2, 0x86E340, 277, 49, 50000, 65000, 32),
    ChapterArea("Speeder Showdown", 6, 3, 0x86E34C, 279, 50, 55000, 70000, 33),
    ChapterArea("The Battle Of Endor", 6, 4, 0x86E358, 286, 51, 90000, 110000, 34),
    ChapterArea("Jedi Destiny", 6, 5, 0x86E364, 301, 52, 35000, 80000, 35),
    ChapterArea("Into The Death Star", 6, 6, 0x86E370, 297, 53, 35000, 40000, 36),
    # area 54 = EP6 Ending
    # area 55 = EP6 Character Bonus, AreaData* index 42
    # area 56 = EP6 Minikit Bonus, AreaData* index 48
    # area 57 = Bonus: New Town
    # area 58 = Bonus: Anakin's Flight, AreaData* index 50
    # area 59 = Bonus: Lego City
    # area 60 = Two Player Arcade
    # area 66 = Cantina
    # area 67 = Bonus: Trailers door
]


# todo: Need to consider the Gold Brick shop eventually. Also Bounty Hunter missions. Also Challenges. Also
#  Character/Minikit bonuses.
BONUS_AREAS = [
    # Could require: "Anakin's Pod"
    BonusArea("Mos Espa Pod Race (Original)", 0x86E124, 0x1, 35, 4, gold_bricks_required=10),
    # There are a number of test levels in LEVELS.TXT that seem to not be counted, so the level IDs for Anakin's Flight
    # do not match what is expected:
    # Intro = 327
    # A = 328
    # B = 329
    # C = 330
    # Outro1 = 331
    # Outro2 = 332
    # Status = 333
    # Could require: "Naboo Starfighter"
    BonusArea("Anakin's Flight", 0x86E3AC, 0x1, 333, 58, gold_bricks_required=30),
    # Could require: "Republic Gunship"
    BonusArea("Gunship Cavalry (Original)", 0x86E1A8, 0x1, 98, 15, gold_bricks_required=10),
    # Note: The base address may be incorrect/I do not know what the base address is supposed to be.
    # Could require: "Darth Vader" + "Stormtrooper" + "C-3PO"
    BonusArea("A New Hope (Bonus Level)", 0x86E249, 0x8, 150, 29, gold_bricks_required=20),
    BonusArea("LEGO City", 0x86E3B8, 0x1, 311, 59,
              gold_bricks_required=10,
              completion_ability_requirements=(
                      JEDI
                      | BLASTER
                      | BOUNTY_HUNTER
                      | CAN_BUILD_BRICKS
                      | CAN_PULL_LEVERS
                      | CAN_ATTACK_UP_CLOSE
                      | CAN_RIDE_VEHICLES
              )),
    BonusArea("New Town", 0x86E3A0, 0x1, 309, 57,
              gold_bricks_required=50,
              completion_ability_requirements=(
                      JEDI
                      | SITH
                      | BLASTER
                      | BOUNTY_HUNTER
                      | CAN_BUILD_BRICKS
                      | CAN_PULL_LEVERS
                      | CAN_ATTACK_UP_CLOSE
                      | CAN_PUSH_OBJECTS
                      | CAN_RIDE_VEHICLES
              )),
    # The bonus level was never completed, so there is just the trailer to watch (which can be skipped immediately).
    # No gold brick for watching the trailer, but it does unlock the shop slot for purchasing Indiana Jones in vanilla
    # todo: Add the Purchase Indiana Jones location.
    # It looks like the unfinished Indiana Jones level would have been Area 67, though this is inaccessible.
    BonusArea("Indiana Jones: Trailer", 0x86E4E5, 0x0, -1, 67, gold_brick=False)
]
BONUS_NAME_TO_BONUS_AREA = {bonus.name: bonus for bonus in BONUS_AREAS}

# todo: Rewrite this to be cleaner, probably by splitting the BonusGameLevelArea requirements into characters and other
#  items.
BONUS_AREA_REQUIREMENT_CHARACTERS = [
    [item for item in area.item_requirements if item not in ("Progressive Bonus Level", "Gold Brick")]
    for area in BONUS_AREAS
]

ALL_AREA_REQUIREMENT_CHARACTERS: frozenset[str] = frozenset().union(
    *CHAPTER_AREA_STORY_CHARACTERS.values(),
    *BONUS_AREA_REQUIREMENT_CHARACTERS
)

SHORT_NAME_TO_CHAPTER_AREA = {area.short_name: area for area in CHAPTER_AREAS}
EPISODE_TO_CHAPTER_AREAS = {i + 1: CHAPTER_AREAS[i * 6:(i + 1) * 6] for i in range(6)}
AREA_ID_TO_CHAPTER_AREA = {area.area_id: area for area in CHAPTER_AREAS}
STATUS_LEVEL_IDS = (
        {area.status_level_id for area in CHAPTER_AREAS} | {area.status_level_id for area in BONUS_AREAS
                                                            if area.status_level_id != -1}
)
AREA_ID_TO_BONUS_AREA = {area.area_id: area for area in BONUS_AREAS}

VEHICLE_BONUS_AREA_NAMES: frozenset[str] = frozenset({
    "Mos Espa Pod Race (Original)",
    "Anakin's Flight",
    "Gunship Cavalry (Original)",
})

assert all(name in BONUS_NAME_TO_BONUS_AREA for name in VEHICLE_BONUS_AREA_NAMES)

VEHICLE_CHAPTER_SHORTNAMES: frozenset[str] = frozenset({
    "1-4",
    "2-1",
    "2-5",
    "3-1",
    "4-6",
    "5-1",
    "5-3",
    "6-6",
})

BOSS_UNIQUE_NAME_TO_CHAPTER: dict[str, ChapterArea] = {
    chapter.unique_boss_name: chapter for chapter in CHAPTER_AREAS if chapter.boss
}
