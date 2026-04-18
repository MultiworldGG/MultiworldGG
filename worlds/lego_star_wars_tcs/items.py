import itertools
import re
from dataclasses import dataclass, field
from typing import Optional, ClassVar, Literal, Mapping, AbstractSet

from BaseClasses import Item, ItemClassification
from .constants import (
    CharacterAbility,
    GAME_NAME,
    ASTROMECH,
    BLASTER,
    BOUNTY_HUNTER,
    HOVER,
    HIGH_JUMP,
    IMPERIAL,
    JEDI,
    PROTOCOL_DROID,
    SHORTIE,
    SITH,
    VEHICLE_TIE,
    VEHICLE_TOW,
    VEHICLE_BLASTER,
    CAN_WEAR_HAT,
    CAN_WEAR_HAT_AND_GRAPPLE,
    CAN_WEAR_HAT_AND_DOUBLE_JUMP,
    CAN_RIDE_VEHICLES,
    CAN_PULL_LEVERS,
    CAN_PUSH_OBJECTS,
    CAN_BUILD_BRICKS,
    CAN_JUMP_NORMALLY,
    CAN_ATTACK_UP_CLOSE,
    CAN_DAGOBAH_SWAMP,
    IS_A_VEHICLE,
)


ItemType = Literal["Character", "Vehicle", "Extra", "Generic", "Minikit"]


class LegoStarWarsTCSItem(Item):
    game = GAME_NAME
    # Most Progression items collect their abilities into the state through a world.collect() override.
    # `collect_abilities_int is not None` is faster than `collect_abilities_int != 0`, so `None` is used instead of `0`.
    collect_abilities_int: int | None
    abilities: CharacterAbility

    def __init__(self, name: str, classification: ItemClassification, code: Optional[int], player: int,
                 abilities: CharacterAbility | None = None):
        super().__init__(name, classification, code, player)
        if abilities is not None and abilities.value != 0:
            self.collect_abilities_int = abilities.value
            self.abilities = abilities
            assert ItemClassification.progression in classification, "All items with abilities should be progression."
        else:
            self.collect_abilities_int = None
            self.abilities = CharacterAbility.NONE


@dataclass(frozen=True)
class GenericItemData:
    code: int
    name: str
    item_type: ClassVar[ItemType] = "Generic"

    @property
    def is_sendable(self):
        return self.code > 0


@dataclass(frozen=True)
class MinikitItemData(GenericItemData):
    bundle_size: int
    item_type: ClassVar[ItemType] = "Minikit"


@dataclass(frozen=True)
class GenericCharacterData(GenericItemData):
    character_index: int
    abilities: CharacterAbility = CharacterAbility.NONE
    shop_slot: int = field(init=False)
    purchase_cost: int = field(init=False)

    def __post_init__(self):
        shop_slot = CHARACTER_TO_SHOP_SLOT.get(self.name, -1)
        object.__setattr__(self, "shop_slot", shop_slot)
        _unlock_method, studs_cost = CHARACTER_SHOP_SLOTS.get(self.name, (..., 0))
        object.__setattr__(self, "purchase_cost", studs_cost)

        # Automatically set some implied abilities as a safeguard.
        abilities = self.abilities
        if SITH in self.abilities:
            abilities |= JEDI

        # Automatically set some implied abilities.
        if JEDI in self.abilities or HIGH_JUMP in self.abilities:
            abilities |= CAN_JUMP_NORMALLY
        if JEDI in self.abilities or BLASTER in self.abilities or BOUNTY_HUNTER in self.abilities:
            abilities |= CAN_ATTACK_UP_CLOSE

        # Automatically set special Hat Machine abilities that are not set explicitly.
        if CAN_WEAR_HAT in self.abilities and BLASTER in self.abilities:
            abilities |= CAN_WEAR_HAT_AND_GRAPPLE
        if CAN_WEAR_HAT in self.abilities and JEDI in self.abilities:
            abilities |= CAN_WEAR_HAT_AND_DOUBLE_JUMP
        if VEHICLE_BLASTER in self.abilities or VEHICLE_TOW in self.abilities or VEHICLE_TIE in self.abilities:
            abilities |= IS_A_VEHICLE

        if abilities is not self.abilities:
            object.__setattr__(self, "abilities", abilities)

    @property
    def purchase_location_name(self) -> str:
        if self.shop_slot == -1:
            raise RuntimeError(f"{self.name} has no shop slot, so cannot be purchased.")
        chapter_short_name, _slot = CHARACTER_SHOP_SLOTS[self.name]
        if chapter_short_name and re.fullmatch(r"\d-\d", chapter_short_name[:3]):
            return f"Purchase {self.name} ({chapter_short_name[:3]})"
        else:
            return f"Purchase {self.name}"


@dataclass(frozen=True)
class CharacterData(GenericCharacterData):
    item_type: ClassVar[ItemType] = "Character"


@dataclass(frozen=True)
class VehicleData(GenericCharacterData):
    item_type: ClassVar[ItemType] = "Vehicle"


@dataclass(frozen=True)
class ExtraData(GenericItemData):
    extra_number: int
    level_shortname: str | None
    localization_id: int
    item_type: ClassVar[ItemType] = "Extra"
    shop_slot_byte: int = field(init=False)
    shop_slot_bit_mask: int = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, "shop_slot_byte", self.extra_number // 8)
        object.__setattr__(self, "shop_slot_bit_mask", 1 << (self.extra_number % 8))

    @property
    def purchase_location_name(self) -> str:
        if self.level_shortname:
            return f"Purchase {self.name} ({self.level_shortname})"
        else:
            return f"Purchase {self.name}"


@dataclass(frozen=True)
class NonPowerBrickExtraData(ExtraData):
    studs_cost: int

    def __post_init__(self):
        super().__post_init__()
        if self.level_shortname is not None:
            raise ValueError("NonPowerBrickExtraData should not have a level_shortname set.")


# Purchasable characters and how they are unlocked, in the order they appear in the shop.
# See the order of characters in COLLECTION.TXT that use "buy_in_shop", plus Indiana Jones, who is special.
CHARACTER_SHOP_SLOTS: dict[str, tuple[str | None, int]] = {
    "Gonk Droid": (None, 3000),
    "PK Droid": (None, 1500),

    # Episode 1
    "Battle Droid": ("1-1", 6500),
    "Battle Droid (Security)": ("1-1", 8500),
    "Battle Droid (Commander)": ("1-1", 10_000),
    "Droideka": ("1-1", 40_000),

    "Captain Tarpals": ("1-2", 17_500),
    "Boss Nass": ("1-2", 15_000),

    "Royal Guard": ("1-3", 10_000),
    "Padmé": ("1-3", 20_000),

    "Watto": ("1-4", 16_000),
    "Pit Droid": ("1-4", 4000),

    # No non-vehicle characters for 1-5

    "Darth Maul": ("1-6", 60_000),

    # Episode 2
    "Zam Wesell": ("2-1", 27_500),
    "Dexter Jettster": ("2-1", 10_000),

    "Clone": ("2-2", 13_000),
    "Lama Su": ("2-2", 9000),
    "Taun We": ("2-2", 9000),

    "Geonosian": ("2-3", 20_000),
    "Battle Droid (Geonosis)": ("2-3", 8500),

    "Super Battle Droid": ("2-4", 25_000),
    "Jango Fett": ("2-4", 70_000),
    "Boba Fett (Boy)": ("2-4", 5500),
    "Luminara": ("2-4", 28_000),
    "Ki-Adi Mundi": ("2-4", 30_000),
    "Kit Fisto": ("2-4", 35_000),
    "Shaak Ti": ("2-4", 36_000),
    "Aayla Secura": ("2-4", 37_000),
    "Plo Koon": ("2-4", 39_000),

    # No non-vehicle characters for 2-5 or 2-6

    # Episode 3
    # No non-vehicle characters for 3-1

    "Count Dooku": ("3-2", 100_000),
    "Grievous' Bodyguard": ("3-2", 42_000),

    "General Grievous": ("3-3", 70_000),

    "Wookiee": ("3-4", 16_000),
    "Clone (Episode 3)": ("3-4", 10_000),
    "Clone (Episode 3, Pilot)": ("3-4", 11_000),
    "Clone (Episode 3, Swamp)": ("3-4", 12_000),
    "Clone (Episode 3, Walker)": ("3-4", 12_000),

    "Mace Windu (Episode 3)": ("3-5", 38_000),
    "Disguised Clone": ("3-5", 12_000),

    # No non-vehicle characters for 3-6

    # Episode 4
    "Rebel Trooper": ("4-1", 10_000),
    "Stormtrooper": ("4-1", 10_000),
    "Imperial Shuttle Pilot": ("4-1", 25_000),

    "Tusken Raider": ("4-2", 23_000),
    "Jawa": ("4-2", 24_000),

    "Sandtrooper": ("4-3", 14_000),
    "Greedo": ("4-3", 60_000),
    "Imperial Spy": ("4-3", 13_500),

    "Beach Trooper": ("4-4", 20_000),
    "Death Star Trooper": ("4-4", 19_000),
    "TIE Fighter Pilot": ("4-4", 21_000),
    "Imperial Officer": ("4-4", 28_000),
    "Grand Moff Tarkin": ("4-4", 38_000),

    # No non-vehicle characters for 4-5 or 4-6

    # Episode 5
    # No non-vehicle characters for 5-1

    "Han Solo (Hood)": ("5-2", 20_000),
    "Rebel Trooper (Hoth)": ("5-2", 16_000),
    "Rebel Pilot": ("5-2", 15_000),
    "Snowtrooper": ("5-2", 16_000),
    "Luke Skywalker (Hoth)": ("5-2", 14_000),

    # No non-vehicle characters for 5-3, 5-4 or 5-5

    "Lobot": ("5-6", 11_000),
    "Ugnaught": ("5-6", 36_000),
    "Bespin Guard": ("5-6", 15_000),
    "Princess Leia (Prisoner)": ("5-6", 22_000),

    # Episode 6
    "Gamorrean Guard": ("6-1", 40_000),
    "Bib Fortuna": ("6-1", 16_000),
    "Palace Guard": ("6-1", 14_000),
    "Bossk": ("6-1", 75_000),

    "Skiff Guard": ("6-2", 12_000),
    "Boba Fett": ("6-2", 100_000),

    # No non-vehicle characters for 6-3

    "Ewok": ("6-4", 34_000),

    "Imperial Guard": ("6-5", 45_000),
    "The Emperor": ("6-5", 275_000),

    "Admiral Ackbar": ("6-6", 33_000),

    # All Episodes complete
    "IG-88": ("ALL_EPISODES", 100_000),
    "Dengar": ("ALL_EPISODES", 70_000),
    "4-LOM": ("ALL_EPISODES", 45_000),
    "Ben Kenobi (Ghost)": ("ALL_EPISODES", 1_100_000),
    "Anakin Skywalker (Ghost)": ("ALL_EPISODES", 1_000_000),
    "Yoda (Ghost)": ("ALL_EPISODES", 1_200_000),
    "R2-Q5": ("ALL_EPISODES", 100_000),

    # Watch Indiana Jones trailer
    "Indiana Jones": ("INDY_TRAILER", 50_000),

    # Episode 1 Vehicles
    "Sebulba's Pod": ("1-4", 20000),

    # Episode 2 Vehicles
    "Zam's Airspeeder": ("2-1", 24000),

    # Episode 3 Vehicles
    "Droid Trifighter": ("3-1", 28000),
    "Vulture Droid": ("3-1", 30000),
    "Clone Arcfighter": ("3-1", 33000),

    # Episode 4 Vehicles
    "TIE Fighter": ("4-6", 35000),
    "TIE Interceptor": ("4-6", 40000),
    "TIE Fighter (Darth Vader)": ("4-6", 50000),

    # Episode 5 Vehicles
    "TIE Bomber": ("5-3", 60000),
    "Imperial Shuttle": ("5-3", 25000),
}


def _make_shop_slot_requirement_to_unlocks() -> Mapping[str | None, Mapping[str, int]]:
    d: dict[str | None, dict[str, int]] = {}
    for character_name, (unlock_requirement, studs_cost) in CHARACTER_SHOP_SLOTS.items():
        if unlock_requirement not in d:
            names: dict[str, int] = {}
            d[unlock_requirement] = names
        else:
            names = d[unlock_requirement]
        names[character_name] = studs_cost

    return d


SHOP_SLOT_REQUIREMENT_TO_UNLOCKS: Mapping[str | None, Mapping[str, int]] = (
    _make_shop_slot_requirement_to_unlocks()
)
del _make_shop_slot_requirement_to_unlocks

CHARACTER_TO_SHOP_SLOT = {name: i for i, name in enumerate(CHARACTER_SHOP_SLOTS.keys())}


_generic = GenericItemData
_char = CharacterData
_vehicle = VehicleData
_extra = ExtraData


COMMON_PACIFIST_NON_DROID = (
        CAN_BUILD_BRICKS
        | CAN_PULL_LEVERS
        | CAN_PUSH_OBJECTS
        | CAN_JUMP_NORMALLY
        | CAN_RIDE_VEHICLES
)
COMMON_NON_DROID = COMMON_PACIFIST_NON_DROID | CAN_ATTACK_UP_CLOSE
HATLESS_COMMON_NON_DROID = COMMON_NON_DROID | CAN_WEAR_HAT
HATLESS_PACIFIST_COMMON_NON_DROID = COMMON_PACIFIST_NON_DROID | CAN_WEAR_HAT
ASTROMECH_DROID = ASTROMECH | HOVER | CAN_DAGOBAH_SWAMP
COMMON_JEDI = JEDI | COMMON_NON_DROID
HATLESS_COMMON_JEDI = JEDI | HATLESS_COMMON_NON_DROID
COMMON_SITH = COMMON_JEDI | SITH
HATLESS_COMMON_SITH = HATLESS_COMMON_JEDI | SITH


ITEM_DATA: list[GenericItemData] = [
    MinikitItemData(1, "5 Minikits", 5),
    # Jar Jar has a vanilla bug where there is a typo in the lever pulling animation, which prevents Jar Jar, and
    # Gungans based on him, from being able to pull levers.
    _char(2, "Jar Jar Binks", 99, abilities=HIGH_JUMP | CAN_BUILD_BRICKS | CAN_PUSH_OBJECTS | CAN_RIDE_VEHICLES),
    _char(3, "Queen Amidala", 80, abilities=BLASTER | COMMON_NON_DROID),
    _char(4, "Captain Panaka", 98, abilities=BLASTER | COMMON_NON_DROID),
    _char(5, "Padmé (Battle)", 77, abilities=BLASTER | HATLESS_COMMON_NON_DROID),
    _char(6, "R2-D2", 8, abilities=ASTROMECH_DROID),
    _char(7, "Anakin Skywalker (Boy)", 93, abilities=SHORTIE | HATLESS_PACIFIST_COMMON_NON_DROID),
    _char(8, "Obi-Wan Kenobi (Jedi Master)", 75, abilities=HATLESS_COMMON_JEDI),
    _char(9, "R4-P17", 66, abilities=ASTROMECH_DROID),
    _char(10, "Anakin Skywalker (Padawan)", 97, abilities=HATLESS_COMMON_JEDI),
    _char(11, "Padmé (Geonosis)", 79, abilities=BLASTER | HATLESS_COMMON_NON_DROID),
    _char(12, "C-3PO", 12, abilities=PROTOCOL_DROID),
    _char(13, "Mace Windu", 62, abilities=HATLESS_COMMON_JEDI),
    _char(14, "Padmé (Clawed)", 78, abilities=BLASTER | HATLESS_COMMON_NON_DROID),
    _char(15, "Yoda", 10, abilities=HATLESS_COMMON_JEDI),
    _char(16, "Obi-Wan Kenobi (Episode 3)", 74, abilities=HATLESS_COMMON_JEDI),
    _char(17, "Anakin Skywalker (Jedi)", 96, abilities=HATLESS_COMMON_JEDI),
    _char(18, "Chancellor Palpatine", 73, abilities=HATLESS_PACIFIST_COMMON_NON_DROID),
    _char(19, "Commander Cody", 89, abilities=BLASTER | IMPERIAL | COMMON_NON_DROID),
    _char(20, "Chewbacca", 16, abilities=BLASTER | HATLESS_COMMON_NON_DROID),
    _char(21, "Princess Leia", 23, abilities=BLASTER | HATLESS_COMMON_NON_DROID),
    _char(22, "Captain Antilles", 207, abilities=BLASTER | COMMON_NON_DROID),
    _char(23, "Rebel Friend", 190, abilities=BLASTER | COMMON_NON_DROID),
    _char(24, "Luke Skywalker (Tatooine)", 28, abilities=BLASTER | HATLESS_COMMON_NON_DROID),
    _char(25, "Ben Kenobi", 56, abilities=HATLESS_COMMON_JEDI),
    _char(26, "Han Solo", 33, abilities=BLASTER | HATLESS_COMMON_NON_DROID),
    _char(27, "Luke Skywalker (Stormtrooper)", 29, abilities=BLASTER | HATLESS_COMMON_NON_DROID),
    _char(28, "Han Solo (Stormtrooper)", 34, abilities=BLASTER | HATLESS_COMMON_NON_DROID),
    _char(29, "Han Solo (Hoth)", 143, abilities=BLASTER | HATLESS_COMMON_NON_DROID),
    _char(30, "Princess Leia (Hoth)", 24, abilities=BLASTER | HATLESS_COMMON_NON_DROID),
    _char(31, "Luke Skywalker (Pilot)", 156, abilities=BLASTER | COMMON_NON_DROID),
    _char(32, "Luke Skywalker (Dagobah)", 157, abilities=HATLESS_COMMON_JEDI),
    _char(33, "Luke Skywalker (Bespin)", 25, abilities=HATLESS_COMMON_JEDI),
    _char(34, "Princess Leia (Boushh)", 129, abilities=BLASTER | HATLESS_COMMON_NON_DROID),
    _char(35, "Luke Skywalker (Jedi)", 27, abilities=HATLESS_COMMON_JEDI),
    _char(36, "Han Solo (Skiff)", 141, abilities=BLASTER | HATLESS_COMMON_NON_DROID),
    _char(37, "Lando Calrissian (Palace Guard)", 201, abilities=BLASTER | COMMON_NON_DROID),
    _char(38, "Princess Leia (Slave)", 161, abilities=BLASTER | HATLESS_COMMON_NON_DROID),
    _char(39, "Luke Skywalker (Endor)", 26, abilities=COMMON_JEDI),
    _char(40, "Princess Leia (Endor)", 162, abilities=BLASTER | COMMON_NON_DROID),
    _char(41, "Han Solo (Endor)", 206, abilities=BLASTER | HATLESS_COMMON_NON_DROID),
    _char(42, "Wicket", 223, abilities=SHORTIE | COMMON_NON_DROID),
    _char(43, "Darth Vader", 40, abilities=IMPERIAL | COMMON_SITH),
    _char(44, "Lando Calrissian", 35, abilities=BLASTER | HATLESS_COMMON_NON_DROID),
    # Has special hair that apparently counts as a hat.
    _char(45, "Princess Leia (Bespin)", 57, abilities=BLASTER | COMMON_NON_DROID),
    _char(46, "Gonk Droid", 17),
    _char(47, "PK Droid", 100),
    _char(48, "Battle Droid", 67, abilities=CAN_ATTACK_UP_CLOSE),
    _char(49, "Battle Droid (Security)", 70, abilities=CAN_ATTACK_UP_CLOSE),
    _char(50, "Battle Droid (Commander)", 68, abilities=CAN_ATTACK_UP_CLOSE),
    _char(51, "Droideka", 65, abilities=CAN_ATTACK_UP_CLOSE),
    # Due to being based on Jar Jar, he cannot pull levers.
    _char(52, "Captain Tarpals", 276,
          abilities=HIGH_JUMP | CAN_BUILD_BRICKS | CAN_PUSH_OBJECTS | CAN_RIDE_VEHICLES | CAN_ATTACK_UP_CLOSE),
    _char(53, "Boss Nass", 254, abilities=COMMON_PACIFIST_NON_DROID),
    _char(54, "Royal Guard", 101, abilities=BLASTER | COMMON_NON_DROID),
    # Cannot build.
    # I am unsure if he should be considered able to jump normally because he flies around instead, but does not hover
    # over gaps.
    _char(55, "Watto", 269, abilities=CAN_PULL_LEVERS | CAN_PUSH_OBJECTS | CAN_RIDE_VEHICLES),
    _char(56, "Pit Droid", 268),
    _char(57, "Darth Maul", 61, abilities=COMMON_SITH),
    _char(58, "Zam Wesell", 2, abilities=BOUNTY_HUNTER | BLASTER | COMMON_NON_DROID),  # There is a second, incorrect Zam Wesell at 305
    _char(59, "Dexter Jettster", 304, abilities=COMMON_PACIFIST_NON_DROID),
    _char(60, "Clone", 86, abilities=IMPERIAL | BLASTER | COMMON_NON_DROID),
    _char(61, "Lama Su", 280, abilities=COMMON_NON_DROID),
    _char(62, "Taun We", 281, abilities=COMMON_NON_DROID),
    # Cannot build.
    # Like Watto, they cannot jump normally, but fly instead.
    _char(63, "Geonosian", 95, abilities=CAN_PULL_LEVERS | CAN_PUSH_OBJECTS | CAN_RIDE_VEHICLES | CAN_ATTACK_UP_CLOSE),
    _char(64, "Battle Droid (Geonosis)", 69, abilities=CAN_ATTACK_UP_CLOSE),
    _char(65, "Super Battle Droid", 81, abilities=CAN_ATTACK_UP_CLOSE),
    _char(66, "Jango Fett", 59, abilities=BOUNTY_HUNTER | BLASTER | HOVER | COMMON_NON_DROID),
    _char(67, "Boba Fett (Boy)", 94, abilities=SHORTIE | COMMON_PACIFIST_NON_DROID),
    _char(68, "Luminara", 84, abilities=COMMON_JEDI),
    _char(69, "Ki-Adi Mundi", 82, abilities=COMMON_JEDI),
    _char(70, "Kit Fisto", 83, abilities=COMMON_JEDI),
    _char(71, "Shaak Ti", 85, abilities=COMMON_JEDI),
    _char(72, "Aayla Secura", 315, abilities=COMMON_JEDI),
    _char(73, "Plo Koon", 316, abilities=COMMON_JEDI),
    _char(74, "Count Dooku", 103, abilities=HATLESS_COMMON_SITH),
    _char(75, "Grievous' Bodyguard", 64, abilities=HIGH_JUMP | CAN_ATTACK_UP_CLOSE),
    # Can build for some reason???
    _char(76, "General Grievous", 60, abilities=HIGH_JUMP | CAN_ATTACK_UP_CLOSE | CAN_BUILD_BRICKS),
    # An extension of Chewbacca, who is specially allowed to wear hats.
    _char(77, "Wookiee", 72, abilities=BLASTER | HATLESS_COMMON_NON_DROID),
    _char(78, "Clone (Episode 3)", 87, abilities=IMPERIAL | BLASTER | COMMON_NON_DROID),
    _char(79, "Clone (Episode 3, Pilot)", 88, abilities=IMPERIAL | BLASTER | COMMON_NON_DROID),
    _char(80, "Clone (Episode 3, Swamp)", 90, abilities=IMPERIAL | BLASTER | COMMON_NON_DROID),
    _char(81, "Clone (Episode 3, Walker)", 91, abilities=IMPERIAL | BLASTER | COMMON_NON_DROID),
    _char(82, "Mace Windu (Episode 3)", 63, abilities=HATLESS_COMMON_JEDI),
    _char(83, "Disguised Clone", 92, abilities=IMPERIAL | BLASTER | COMMON_NON_DROID),
    _char(84, "Rebel Trooper", 13, abilities=BLASTER | COMMON_NON_DROID),
    _char(85, "Stormtrooper", 20, abilities=IMPERIAL | BLASTER | COMMON_NON_DROID),
    _char(86, "Imperial Shuttle Pilot", 53, abilities=IMPERIAL | BLASTER | COMMON_NON_DROID),
    _char(87, "Tusken Raider", 9, abilities=BLASTER | HATLESS_COMMON_NON_DROID),
    _char(88, "Jawa", 22, abilities=SHORTIE | COMMON_PACIFIST_NON_DROID),  # Note: Cannot grapple
    _char(89, "Sandtrooper", 51, abilities=IMPERIAL | BLASTER | COMMON_NON_DROID),
    _char(90, "Greedo", 171, abilities=BOUNTY_HUNTER | BLASTER | COMMON_NON_DROID),
    _char(91, "Imperial Spy", 172, abilities=COMMON_PACIFIST_NON_DROID),
    _char(92, "Beach Trooper", 48, abilities=IMPERIAL | BLASTER | COMMON_NON_DROID),
    _char(93, "Death Star Trooper", 49, abilities=IMPERIAL | BLASTER | COMMON_NON_DROID),
    _char(94, "TIE Fighter Pilot", 50, abilities=IMPERIAL | BLASTER | COMMON_NON_DROID),
    _char(95, "Imperial Officer", 14, abilities=IMPERIAL | BLASTER | COMMON_NON_DROID),
    _char(96, "Grand Moff Tarkin", 131, abilities=IMPERIAL | BLASTER | HATLESS_COMMON_NON_DROID),
    # Can wear hats despite the hood.
    _char(97, "Han Solo (Hood)", 142, abilities=BLASTER | HATLESS_COMMON_NON_DROID),
    _char(98, "Rebel Trooper (Hoth)", 107, abilities=BLASTER | COMMON_NON_DROID),
    _char(99, "Rebel Pilot", 58, abilities=BLASTER | COMMON_NON_DROID),
    _char(100, "Snowtrooper", 45, abilities=IMPERIAL | BLASTER | COMMON_NON_DROID),
    _char(101, "Lobot", 192, abilities=HATLESS_COMMON_NON_DROID),
    _char(102, "Ugnaught", 158, abilities=SHORTIE | COMMON_PACIFIST_NON_DROID),
    _char(103, "Bespin Guard", 193, abilities=BLASTER | COMMON_NON_DROID),
    _char(104, "Gamorrean Guard", 102, abilities=COMMON_NON_DROID),
    _char(105, "Bib Fortuna", 185, abilities=COMMON_NON_DROID),
    _char(106, "Palace Guard", 196, abilities=BLASTER | COMMON_NON_DROID),
    _char(107, "Bossk", 212, abilities=BOUNTY_HUNTER | BLASTER | COMMON_NON_DROID),
    _char(108, "Skiff Guard", 186, abilities=BLASTER | HATLESS_COMMON_NON_DROID),
    _char(109, "Boba Fett", 7, abilities=BOUNTY_HUNTER | BLASTER | HOVER | COMMON_NON_DROID),
    _char(110, "Ewok", 199, abilities=SHORTIE | COMMON_NON_DROID),
    _char(111, "Imperial Guard", 194, abilities=IMPERIAL | COMMON_NON_DROID),
    _char(112, "The Emperor", 6, abilities=IMPERIAL | COMMON_SITH),
    _char(113, "Admiral Ackbar", 211, abilities=BLASTER | COMMON_NON_DROID),
    _char(114, "IG-88", 197,
          abilities=
          BOUNTY_HUNTER
          | BLASTER
          | ASTROMECH
          | PROTOCOL_DROID
          | CAN_PUSH_OBJECTS
          | CAN_JUMP_NORMALLY
          | CAN_RIDE_VEHICLES),
    _char(115, "Dengar", 213, abilities=BOUNTY_HUNTER | BLASTER | COMMON_NON_DROID),
    _char(116, "4-LOM", 225,
          abilities=
          BOUNTY_HUNTER
          | BLASTER
          | ASTROMECH
          | PROTOCOL_DROID
          | CAN_PUSH_OBJECTS
          | CAN_JUMP_NORMALLY
          | CAN_RIDE_VEHICLES),
    _char(117, "Ben Kenobi (Ghost)", 195, abilities=HATLESS_COMMON_JEDI),
    _char(118, "Yoda (Ghost)", 227, abilities=COMMON_JEDI),
    _char(119, "R2-Q5", 314, abilities=ASTROMECH_DROID),
    _char(120, "Padmé", 76, abilities=BLASTER | HATLESS_COMMON_NON_DROID),
    _char(121, "Luke Skywalker (Hoth)", 204, abilities=BLASTER | COMMON_NON_DROID),  # Ability missing from manual
    _extra(122, "Super Gonk", 0x8, "1-1", 699),
    _extra(123, "Poo Money", 0x9, "1-2", 296),  # "Fertilizer" in manual
    _extra(124, "Walkie Talkie Disable", 0xA, "1-3", 1665),
    _extra(125, "Power Brick Detector", 0xB, "1-4", 1657),
    _extra(126, "Super Slap", 0xC, "1-5", 1658),
    _extra(127, "Force Grapple Leap", 0xD, "1-6", 1660),
    _extra(128, "Stud Magnet", 0xE, "2-1", 297),
    _extra(129, "Disarm Troopers", 0xF, "2-2", 1662),
    _extra(130, "Character Studs", 0x10, "2-3", 1671),
    _extra(131, "Perfect Deflect", 0x11, "2-4", 1666),
    _extra(132, "Exploding Blaster Bolts", 0x12, "2-5", 1663),
    _extra(133, "Force Pull", 0x13, "2-6", 1667),
    _extra(134, "Vehicle Smart Bomb", 0x14, "3-1", 1664),
    _extra(135, "Super Astromech", 0x15, "3-2", 1668),
    _extra(136, "Super Jedi Slam", 0x16, "3-3", 1670),
    _extra(137, "Super Thermal Detonator", 0x17, "3-4", 1661),
    _extra(138, "Deflect Bolts", 0x18, "3-5", 1659),
    _extra(139, "Dark Side", 0x19, "3-6", 1669),
    _extra(140, "Super Blasters", 0x1A, "4-1", 682),
    _extra(141, "Fast Force", 0x1B, "4-2", 685),
    _extra(142, "Super Lightsabers", 0x1C, "4-3", 667),
    _extra(143, "Tractor Beam", 0x1D, "4-4", 687),
    _extra(144, "Invincibility", 0x1E, "4-5", 664),
    _generic(145, "Progressive Score Multiplier"),
    _extra(-1, "Score x2", 0x1F, "4-6", 666),
    _extra(146, "Self Destruct", 0x20, "5-1", 681),
    _extra(147, "Fast Build", 0x21, "5-2", 684),
    _extra(-1, "Score x4", 0x22, "5-3" ,670),
    _extra(148, "Regenerate Hearts", 0x23, "5-4", 683),
    _extra(149, "Minikit Detector", 0x24, "5-6", 665),
    _extra(-1, "Score x6", 0x25, "5-5", 676),
    _extra(150, "Super Zapper", 0x26, "6-1", 688),
    _extra(151, "Bounty Hunter Rockets", 0x27, "6-2", 673),
    _extra(-1, "Score x8", 0x28, "6-3", 679),
    _extra(152, "Super Ewok Catapult", 0x29, "6-4", 689),
    _extra(153, "Infinite Torpedos", 0x2A, "6-6", 686),
    _extra(-1, "Score x10", 0x2B, "6-5", 680),
    _generic(154, "Episode Completion Token"),
    _generic(155, "Episode 1 Unlock"),
    _generic(156, "Episode 2 Unlock"),
    _generic(157, "Episode 3 Unlock"),
    _generic(158, "Episode 4 Unlock"),
    _generic(159, "Episode 5 Unlock"),
    _generic(160, "Episode 6 Unlock"),
    _char(161, "Anakin Skywalker (Ghost)", 226, abilities=HATLESS_COMMON_JEDI),
    _char(162, "Indiana Jones", 317, abilities=BLASTER | HATLESS_COMMON_NON_DROID),
    _char(163, "Princess Leia (Prisoner)", 205, abilities=BLASTER | HATLESS_COMMON_NON_DROID),
    _vehicle(164, "Anakin's Pod", 259, abilities=IS_A_VEHICLE),
    _vehicle(165, "Naboo Starfighter", 272, abilities=VEHICLE_TOW | VEHICLE_BLASTER),
    _vehicle(166, "Republic Gunship", 285, abilities=VEHICLE_TOW | VEHICLE_BLASTER),
    _vehicle(167, "Anakin's Starfighter", 221, abilities=VEHICLE_BLASTER),
    _vehicle(168, "Obi-Wan's Starfighter", 291, abilities=VEHICLE_BLASTER),
    _vehicle(169, "X-Wing", 36, abilities=VEHICLE_BLASTER),
    _vehicle(170, "Y-Wing", 39, abilities=VEHICLE_BLASTER),
    _vehicle(171, "Millennium Falcon", 38, abilities=VEHICLE_BLASTER),
    _vehicle(172, "TIE Interceptor", 128, abilities=VEHICLE_TIE | VEHICLE_BLASTER),
    _vehicle(173, "Snowspeeder", 32, abilities=VEHICLE_TOW | VEHICLE_BLASTER),
    _vehicle(174, "Anakin's Speeder", 3, abilities=VEHICLE_BLASTER),
    _generic(175, "Purple Stud"),
    # NEW. Items below here did not exist in the manual.
    # TODO: Redo all the item IDs to make more sense. Either internal order in chars.txt, or in character grid order.
    _char(176, "Qui-Gon Jinn", 104, abilities=HATLESS_COMMON_JEDI),
    _char(177, "Obi-Wan Kenobi", 1, abilities=HATLESS_COMMON_JEDI),
    _char(178, "TC-14", 71, abilities=PROTOCOL_DROID),
    NonPowerBrickExtraData(179, "Extra Toggle", 0x0, None, 672, 30000),
    NonPowerBrickExtraData(180, "Fertilizer", 0x1, None, 671, 8000),
    NonPowerBrickExtraData(181, "Disguise", 0x2, None, 668, 10000),
    NonPowerBrickExtraData(182, "Daisy Chains", 0x3, None, 677, 5000),
    NonPowerBrickExtraData(183, "Chewbacca Carrying C-3PO", 0x4, None, 669, 10000),
    NonPowerBrickExtraData(184, "Tow Death Star", 0x5, None, 678, 5000),
    NonPowerBrickExtraData(185, "Silhouettes", 0x6, None, 698, 10000),
    NonPowerBrickExtraData(186, "Beep Beep", 0x7, None, 298, 7500),
    _extra(-1, "Adaptive Difficulty", 0x2C, None, 690),  # Effectively a difficulty setting, so not randomized.
    # Custom characters can only use unlocked character equipment, besides some blasters. They do not get access to
    # lightsabers/force unless Jedi are unlocked.
    _char(188, "STRANGER 1", 168, abilities=BLASTER | HATLESS_COMMON_NON_DROID),
    _char(189, "STRANGER 2", 169, abilities=BLASTER | HATLESS_COMMON_NON_DROID),
    _vehicle(190, "Sebulba's Pod", 261, abilities=IS_A_VEHICLE),
    _vehicle(191, "Zam's Airspeeder", 277, abilities=VEHICLE_BLASTER),
    _vehicle(192, "Droid Trifighter", 292, abilities=VEHICLE_BLASTER),
    _vehicle(193, "Vulture Droid", 293, abilities=VEHICLE_BLASTER),
    _vehicle(194, "Clone Arcfighter", 295, abilities=VEHICLE_BLASTER),
    _vehicle(195, "TIE Fighter", 37, abilities=VEHICLE_BLASTER | VEHICLE_TIE),
    _vehicle(196, "TIE Fighter (Darth Vader)", 182, abilities=VEHICLE_BLASTER | VEHICLE_TIE),
    _vehicle(197, "TIE Bomber", 209, abilities=VEHICLE_BLASTER | VEHICLE_TIE),
    _vehicle(198, "Imperial Shuttle", 198, abilities=VEHICLE_BLASTER),
    MinikitItemData(199, "Minikit", 1),
    MinikitItemData(200, "2 Minikits", 2),
    MinikitItemData(201, "10 Minikits", 10),
    _generic(202, "Power Up"),
    _generic(203, "Kyber Brick"),
    _generic(204, "Silver Stud"),
    _generic(205, "Gold Stud"),
    _generic(206, "Blue Stud"),
    _vehicle(207, "Slave 1", 11, abilities=VEHICLE_BLASTER),

    # "Extra Toggle" characters.
    _char(-1, "Womp Rat", 165),
    _char(-1, "Skeleton", 231),

    # Miscellaneous vehicles.
    # This is the vehicle present in the outside area of the Cantina. 'map' is the internal name for the Cantina.
    _char(-1, "mapcar", 303),
]


# Programmatically add Chapter Unlock items, starting from ID 1000 so that they avoid clashing with manually defined
# items.
CHAPTER_UNLOCKS: list[GenericItemData] = [
    _generic(i, f"{episode}-{chapter} Unlock") for i, (episode, chapter)
    in enumerate(itertools.product(range(1, 7), range(1, 7)), start=1000)
]
ITEM_DATA.extend(CHAPTER_UNLOCKS)


USEFUL_NON_PROGRESSION_CHARACTERS: set[str] = {
    # There is currently no Ghost logic for bypassing gas and other hazards, so give the Ghosts at least Useful
    # classification.
    "Ben Kenobi (Ghost)",
    "Anakin Skywalker (Ghost)",
    "Yoda (Ghost)",
    # There is currently no glitch logic for the glitchy mess that is Yoda, so ensure Yoda is never excluded by making
    # him Useful.
    "Yoda",
    # The fastest character (1.8).
    "Droideka",
    # The second-fastest character (1.5).
    "Watto",
    # The third-fastest character when Super Gonk is active (1.44).
    "Gonk Droid",
    # Fastest vehicles.
    "Anakin's Pod",
    "Sebulba's Pod",
}


ITEM_DATA_BY_NAME: Mapping[str, GenericItemData] = {data.name: data for data in ITEM_DATA}
ITEM_DATA_BY_ID: Mapping[int, GenericItemData] = {data.code: data for data in ITEM_DATA if data.is_sendable}
EXTRAS_BY_NAME: Mapping[str, ExtraData] = {data.name: data for data in ITEM_DATA if isinstance(data, ExtraData)}
PURCHASABLE_NON_POWER_BRICK_EXTRAS: tuple[NonPowerBrickExtraData, ...] = tuple(
    [extra for extra in EXTRAS_BY_NAME.values() if isinstance(extra, NonPowerBrickExtraData)]
)
CHARACTERS_AND_VEHICLES_BY_NAME: Mapping[str, GenericCharacterData] = {data.name: data for data in ITEM_DATA
                                                                       if isinstance(data, GenericCharacterData)}
GENERIC_BY_NAME: Mapping[str, GenericItemData] = {data.name: data for data in ITEM_DATA if data.item_type == "Generic"}
MINIKITS_BY_NAME: Mapping[str, MinikitItemData] = {data.name: data for data in ITEM_DATA
                                                   if isinstance(data, MinikitItemData)}
NON_VEHICLE_CHARACTER_BY_INDEX: Mapping[int, CharacterData] = {char.character_index: char
                                                               for char in CHARACTERS_AND_VEHICLES_BY_NAME.values()
                                                               if isinstance(char, CharacterData)}
AP_NON_VEHICLE_CHARACTER_INDICES: AbstractSet[int] = {char.character_index
                                                      for char in NON_VEHICLE_CHARACTER_BY_INDEX.values()
                                                      if char.is_sendable}

ITEM_NAME_TO_ID: dict[str, int] = {name: item.code for name, item in ITEM_DATA_BY_NAME.items() if item.is_sendable}

MINIKITS_BY_COUNT: Mapping[int, GenericItemData] = {bundle.bundle_size: bundle for bundle in MINIKITS_BY_NAME.values()}
