from enum import IntEnum, auto
from typing import TypedDict, NotRequired, Collection

from rule_builder.rules import HasAny, Has, True_

from .areas import Area


_EVENT_OFFSET = 1000


__all__ = [
    "Character",
    "UnlockMethod",
    "AREA_TO_STORY_CHARACTERS",
    "AREA_TO_PURCHASE_CHARACTERS",
    "AREA_TO_EXTRA_TOGGLE_CHARACTERS",
    "CHARACTER_TO_STORY_AREA",
    "CHARACTER_TO_PURCHASE_AREA",
    "CHARACTER_TO_EXTRA_TOGGLE_AREA",
    "ALL_LOGIC_RELEVANT_CHARACTERS",
    "NORMAL_LOGIC_RELEVANT_CHARACTERS",
    "EXTRA_TOGGLE_LOGIC_RELEVANT_CHARACTERS",
]


class UnlockMethod(IntEnum):
    START = auto()
    STORY = auto()
    AREA_COMPLETE = auto()
    ALL_EPISODES_COMPLETE = auto()
    INDY_TRAILER = auto()
    ALL_MINIKITS_COMPLETE = auto()
    MINIKIT = auto()
    EXTRA_TOGGLE = auto()

    @property
    def requires_area(self) -> bool:
        return self in (UnlockMethod.STORY,
                        UnlockMethod.AREA_COMPLETE,
                        UnlockMethod.MINIKIT,
                        UnlockMethod.AREA_COMPLETE,
                        UnlockMethod.EXTRA_TOGGLE)

    @property
    def single_area_only(self) -> bool:
        return self in (UnlockMethod.AREA_COMPLETE, UnlockMethod.MINIKIT)


class CharacterInitializer(TypedDict):
    readable_name: NotRequired[str]
    unlock_method: NotRequired[UnlockMethod]
    areas: NotRequired[list[Area]]
    area: NotRequired[Area]
    purchase_cost: NotRequired[int]


# noinspection LongLine
class Character(IntEnum):
    readable_name: str
    unlock_method: UnlockMethod | None
    """How this character is unlocked. If absent, the character is not unlockable."""
    areas: frozenset[Area] | None
    """Any areas that must be completed to unlock this character (either immediately, or in the shop), or the area 
    whose minikit must be completed to unlock this character."""
    purchase_cost: int | None
    """When specified, this character must be purchased from the shop once unlocked."""

    def __new__(cls, *args, **kwargs):
        obj = int.__new__(cls, args[0])
        obj._value_ = args[0]
        return obj

    def __init__(self, _id, character_initializer: CharacterInitializer | None = None):
        if character_initializer is None:
            self.readable_name = "?"
            self.purchase_cost = None
            self.areas = None
            self.unlock_method = None
            return 

        self.readable_name = character_initializer["readable_name"]
        self.purchase_cost = character_initializer.get("purchase_cost")
        self.unlock_method = character_initializer.get("unlock_method")
        if self.unlock_method is not None and self.unlock_method.requires_area:
            if self.unlock_method.single_area_only:
                if "areas" in character_initializer or "area" not in character_initializer:
                    raise ValueError(f"The unlock method for {self.name} is {self.unlock_method!r}, which should"
                                     f" include a single Area")
                self.areas = frozenset((character_initializer["area"],))
            else:
                if "area" in character_initializer or "areas" not in character_initializer:
                    raise ValueError(f"The unlock method for {self.name} is {self.unlock_method!r}, which should"
                                     f" include one or many Areas")
                self.areas = frozenset(character_initializer["areas"],)
        else:
            if "areas" in character_initializer or "area" in character_initializer:
                raise ValueError(f"The unlock method for {self.name} is {self.unlock_method!r}, which should not"
                                 f" include any Areas")
            self.areas = frozenset()

    def is_event(self):
        return self.value >= _EVENT_OFFSET

    def is_unlockable(self) -> bool:
        """Is this Character unlockable in-game?"""
        return self.unlock_method is not None

    def is_logic_relevant(self) -> bool:
        """Can this character be collected into a Collection state (by .readable_name)?"""
        return (self.is_unlockable() and self.unlock_method is not UnlockMethod.MINIKIT) or self.is_event()

    def is_sendable(self) -> bool:
        """Can this Character be shuffled into the multiworld and sent to players as an item?"""
        return self.is_logic_relevant() and not self.is_event()

    def get_purchase_location_name(self):
        base_name = f"Purchase {self.readable_name}"
        area = CHARACTER_TO_PURCHASE_AREA[self]
        if area.is_chapter() or area.is_bonus_room_bonus():
            return area.prefix_name(base_name)
        else:
            # Cantina purchases.
            return base_name

    def get_level_completion_unlock_location_name(self):
        return f"Level Completion - Unlock {self.readable_name}"

    def get_ridesanity_location_name(self):
        return f"Ride {self.readable_name}"

    def has(self) -> Has:
        if self not in NORMAL_LOGIC_RELEVANT_CHARACTERS:
            raise ValueError(f"{self!r} cannot be used in rules.")
        return Has(self.readable_name)

    @staticmethod
    def _validate_characters_for_logic(characters: "Collection[Character]"):
        if not all(map(NORMAL_LOGIC_RELEVANT_CHARACTERS.__contains__, characters)):
            if any(map(EXTRA_TOGGLE_LOGIC_RELEVANT_CHARACTERS.__contains__, characters)):
                raise ValueError("Cannot create rules that check for Extra Toggle characters because these never get"
                                " collected into a CollectionState. Logic should check for"
                                " Extra.EXTRA_TOGGLE.readable_name being in the state instead, if an Extra Toggle character"
                                f" can satisfy a rule. Got {characters}.")
            else:
                raise ValueError(f"Cannot create rules that check for characters that cannot be used in rules. Got"
                                 f" {characters}")

    @staticmethod
    def has_any(*characters: "Character") -> HasAny | Has | True_:
        character_names = Character.to_logic_names(characters)
        if not characters:
            return True_()
        if len(character_names) == 1:
            return Has(character_names[0])
        else:
            return HasAny(*character_names)

    @staticmethod
    def to_logic_names(characters: "Collection[Character]"):
        Character._validate_characters_for_logic(characters)
        return [c.readable_name for c in characters]

    @staticmethod
    def from_sendable_name(sendable_name: str) -> "Character":
        return _NAME_TO_SENDABLE_CHARACTER[sendable_name]


    # There is no extractor for this data because of a significant number of edits needing to be made due to duplicates
    # and invalid identifiers. Most of the extractable data from characters is not really usable individually and needs
    # parsing manually to extract what's useful from it.
    # The data that is useful to extract is also spread across multiple data structures.
    SLAVE1_LSW1 =                         0
    OBI_WAN_KENOBI =                      1, dict(readable_name="Obi-Wan Kenobi", unlock_method=UnlockMethod.STORY, areas=[Area.NEGOTIATIONS, Area.GUNGAN, Area.PALACERESCUE, Area.RETAKEPALACE, Area.MAUL])
    ZAM_WESELL =                          2, dict(readable_name="Zam Wesell", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.PURSUIT, purchase_cost=27_500)
    ANAKINS_SPEEDER =                     3, dict(readable_name="Anakin's Speeder", unlock_method=UnlockMethod.STORY, areas=[Area.PURSUIT])
    ANAKINS_SPEEDER_GREEN =               4, dict(readable_name="Anakin's Speeder (Green)")
    ASSASSINDROID =                       5
    THE_EMPEROR =                         6, dict(readable_name="The Emperor", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.EMPERORFIGHT, purchase_cost=275_000)
    BOBA_FETT =                           7, dict(readable_name="Boba Fett", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.SARLACCPIT, purchase_cost=100_000)
    R2_D2 =                               8, dict(readable_name="R2-D2", unlock_method=UnlockMethod.STORY, areas=[Area.RETAKEPALACE, Area.FACTORY, Area.JEDI, Area.CRUISER, Area.BLOCKADERUNNER, Area.TATOOINE, Area.MOSEISLEY, Area.DEATHSTARRESCUE, Area.DEATHSTARESCAPE, Area.DAGOBAH, Area.CLOUDCITYTRAP, Area.CLOUDCITYESCAPE, Area.JABBASPALACE, Area.SARLACCPIT, Area.ENDORBATTLE])
    TUSKEN_RAIDER =                       9, dict(readable_name="Tusken Raider", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.TATOOINE, purchase_cost=23_000)
    YODA =                               10, dict(readable_name="Yoda", unlock_method=UnlockMethod.STORY, areas=[Area.DOOKU, Area.KASHYYYK, Area.TEMPLE, Area.DAGOBAH])
    SLAVE_1 =                            11, dict(readable_name="Slave 1", unlock_method=UnlockMethod.ALL_MINIKITS_COMPLETE)
    C_3PO =                              12, dict(readable_name="C-3PO", unlock_method=UnlockMethod.STORY, areas=[Area.FACTORY, Area.BLOCKADERUNNER, Area.TATOOINE, Area.MOSEISLEY, Area.DEATHSTARRESCUE, Area.DEATHSTARESCAPE, Area.HOTHESCAPE, Area.CLOUDCITYESCAPE, Area.JABBASPALACE, Area.SARLACCPIT, Area.ENDORBATTLE, Area.ANEWHOPE])
    REBEL_TROOPER =                      13, dict(readable_name="Rebel Trooper", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.BLOCKADERUNNER, purchase_cost=10_000)
    IMPERIAL_OFFICER =                   14, dict(readable_name="Imperial Officer", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.DEATHSTARRESCUE, purchase_cost=28_000)
    SPEEDER_LAND =                       15, dict(readable_name="Landspeeder")
    CHEWBACCA =                          16, dict(readable_name="Chewbacca", unlock_method=UnlockMethod.STORY, areas=[Area.KASHYYYK, Area.MOSEISLEY, Area.DEATHSTARRESCUE, Area.DEATHSTARESCAPE, Area.HOTHESCAPE, Area.CLOUDCITYESCAPE, Area.JABBASPALACE, Area.SARLACCPIT, Area.ENDORBATTLE])
    GONK_DROID =                         17, dict(readable_name="Gonk Droid", unlock_method=UnlockMethod.START, purchase_cost=3000)
    CLONEWALKER =                        18, dict(readable_name="Clone Walker")
    TRAINING_REMOTE =                    19, dict(readable_name="Training Remote", unlock_method=UnlockMethod.EXTRA_TOGGLE, areas=[Area.TEMPLE])
    STORMTROOPER =                       20, dict(readable_name="Stormtrooper", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.BLOCKADERUNNER, purchase_cost=10_000)
    BARMAN =                             21
    JAWA =                               22, dict(readable_name="Jawa", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.TATOOINE, purchase_cost=24_000)
    PRINCESS_LEIA =                      23, dict(readable_name="Princess Leia", unlock_method=UnlockMethod.STORY, areas=[Area.BLOCKADERUNNER, Area.DEATHSTARESCAPE])
    PRINCESS_LEIA_HOTH =                 24, dict(readable_name="Princess Leia (Hoth)", unlock_method=UnlockMethod.STORY, areas=[Area.HOTHESCAPE])
    LUKE_SKYWALKER_BESPIN =              25, dict(readable_name="Luke Skywalker (Bespin)", unlock_method=UnlockMethod.STORY, areas=[Area.CLOUDCITYTRAP])
    LUKE_SKYWALKER_ENDOR =               26, dict(readable_name="Luke Skywalker (Endor)", unlock_method=UnlockMethod.STORY, areas=[Area.SPEEDERCHASE])
    LUKE_SKYWALKER_JEDI =                27, dict(readable_name="Luke Skywalker (Jedi)", unlock_method=UnlockMethod.STORY, areas=[Area.JABBASPALACE, Area.SARLACCPIT, Area.EMPERORFIGHT])
    LUKE_SKYWALKER_TATOOINE =            28, dict(readable_name="Luke Skywalker (Tatooine)", unlock_method=UnlockMethod.STORY, areas=[Area.TATOOINE, Area.MOSEISLEY, Area.DEATHSTARESCAPE])
    LUKE_SKYWALKER_STORMTROOPER =        29, dict(readable_name="Luke Skywalker (Stormtrooper)", unlock_method=UnlockMethod.STORY, areas=[Area.DEATHSTARRESCUE])
    SPEEDERBIKE =                        30, dict(readable_name="Speeder Bike")
    SPEEDERBIKE_SNOW =                   31
    SNOWSPEEDER =                        32, dict(readable_name="Snowspeeder", unlock_method=UnlockMethod.STORY, areas=[Area.HOTHBATTLE])
    HAN_SOLO =                           33, dict(readable_name="Han Solo", unlock_method=UnlockMethod.STORY, areas=[Area.MOSEISLEY, Area.DEATHSTARESCAPE])
    HAN_SOLO_STORMTROOPER =              34, dict(readable_name="Han Solo (Stormtrooper)", unlock_method=UnlockMethod.STORY, areas=[Area.DEATHSTARRESCUE])
    LANDO_CALRISSIAN =                   35, dict(readable_name="Lando Calrissian", unlock_method=UnlockMethod.STORY, areas=[Area.CLOUDCITYESCAPE])
    X_WING =                             36, dict(readable_name="X-wing", unlock_method=UnlockMethod.STORY, areas=[Area.DEATHSTARBATTLE, Area.ASTEROIDCHASE, Area.DEATHSTAR2BATTLE])
    TIE_FIGHTER =                        37, dict(readable_name="TIE Fighter", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.DEATHSTARBATTLE, purchase_cost=35_000)
    MILLENNIUM_FALCON =                  38, dict(readable_name="Millennium Falcon", unlock_method=UnlockMethod.STORY, areas=[Area.ASTEROIDCHASE, Area.DEATHSTAR2BATTLE])
    Y_WING =                             39, dict(readable_name="Y-wing", unlock_method=UnlockMethod.STORY, areas=[Area.DEATHSTARBATTLE])
    DARTH_VADER =                        40, dict(readable_name="Darth Vader", unlock_method=UnlockMethod.STORY, areas=[Area.EMPERORFIGHT, Area.ANEWHOPE])
    MINI_MILLENNIUM_FALCON =             41, dict(readable_name="Millennium Falcon", unlock_method=UnlockMethod.MINIKIT, area=Area.DEATHSTARRESCUE)
    MINI_X_WING =                        42, dict(readable_name="X-wing", unlock_method=UnlockMethod.MINIKIT, area=Area.DAGOBAH)
    MINI_TIE_INTERCEPTOR =               43, dict(readable_name="TIE Interceptor", unlock_method=UnlockMethod.MINIKIT, area=Area.DEATHSTAR2BATTLE)
    MOUSE_DROID =                        44, dict(readable_name="Mouse Droid", unlock_method=UnlockMethod.EXTRA_TOGGLE, areas=[Area.DEATHSTARRESCUE, Area.DEATHSTARESCAPE, Area.EMPERORFIGHT])
    SNOWTROOPER =                        45, dict(readable_name="Snowtrooper", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.HOTHESCAPE, purchase_cost=16_000)
    PROBEDROID =                         46
    ATAT =                               47, dict(readable_name="AT-AT")
    BEACH_TROOPER =                      48, dict(readable_name="Beach Trooper", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.DEATHSTARRESCUE, purchase_cost=20_000)
    DEATH_STAR_TROOPER =                 49, dict(readable_name="Death Star Trooper", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.DEATHSTARRESCUE, purchase_cost=19_000)
    TIE_FIGHTER_PILOT =                  50, dict(readable_name="TIE Fighter Pilot", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.DEATHSTARRESCUE, purchase_cost=21_000)
    SANDTROOPER =                        51, dict(readable_name="Sandtrooper", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.MOSEISLEY, purchase_cost=14_000)
    SCOUT_TROOPER =                      52, dict(readable_name="Scout Trooper", unlock_method=UnlockMethod.EXTRA_TOGGLE, areas=[Area.SPEEDERCHASE, Area.ENDORBATTLE])
    IMPERIAL_SHUTTLE_PILOT =             53, dict(readable_name="Imperial Shuttle Pilot", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.BLOCKADERUNNER, purchase_cost=25_000)
    DRAGBOMB =                           54
    GRABBER =                            55
    BEN_KENOBI =                         56, dict(readable_name="Ben Kenobi", unlock_method=UnlockMethod.STORY, areas=[Area.TATOOINE, Area.MOSEISLEY, Area.DEATHSTARRESCUE])
    PRINCESS_LEIA_BESPIN =               57, dict(readable_name="Princess Leia (Bespin)", unlock_method=UnlockMethod.STORY, areas=[Area.CLOUDCITYESCAPE])
    REBEL_PILOT =                        58, dict(readable_name="Rebel Pilot", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.HOTHESCAPE, purchase_cost=15_000)
    JANGO_FETT =                         59, dict(readable_name="Jango Fett", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.JEDI, purchase_cost=70_000)
    GENERAL_GRIEVOUS =                   60, dict(readable_name="General Grievous", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.GRIEVOUS, purchase_cost=70_000)
    DARTH_MAUL =                         61, dict(readable_name="Darth Maul", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.MAUL, purchase_cost=60_000)
    MACE_WINDU =                         62, dict(readable_name="Mace Windu", unlock_method=UnlockMethod.STORY, areas=[Area.JEDI])
    MACE_WINDU_EPISODE_III =             63, dict(readable_name="Mace Windu (Episode III)", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.TEMPLE, purchase_cost=38_000)
    GRIEVOUS_BODYGUARD =                 64, dict(readable_name="Grievous' Bodyguard", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.CRUISER, purchase_cost=42_000)
    DROIDEKA =                           65, dict(readable_name="Droideka", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.NEGOTIATIONS, purchase_cost=40_000)
    R4_P17 =                             66, dict(readable_name="R4-P17", unlock_method=UnlockMethod.STORY, areas=[Area.KAMINO])
    BATTLE_DROID =                       67, dict(readable_name="Battle Droid", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.NEGOTIATIONS, purchase_cost=6500)
    BATTLE_DROID_COMMANDER =             68, dict(readable_name="Battle Droid (Commander)", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.NEGOTIATIONS, purchase_cost=10_000)
    BATTLE_DROID_GEONOSIS =              69, dict(readable_name="Battle Droid (Geonosis)", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.FACTORY, purchase_cost=8500)
    BATTLE_DROID_SECURITY =              70, dict(readable_name="Battle Droid (Security)", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.NEGOTIATIONS, purchase_cost=8500)
    TC_14 =                              71, dict(readable_name="TC-14", unlock_method=UnlockMethod.STORY, areas=[Area.NEGOTIATIONS])
    WOOKIEE =                            72, dict(readable_name="Wookiee", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.KASHYYYK, purchase_cost=16_000)
    CHANCELLOR_PALPATINE =               73, dict(readable_name="Chancellor Palpatine", unlock_method=UnlockMethod.STORY, areas=[Area.CRUISER])
    OBI_WAN_KENOBI_EPISODE_III =         74, dict(readable_name="Obi-Wan Kenobi (Episode III)", unlock_method=UnlockMethod.STORY, areas=[Area.CRUISER, Area.GRIEVOUS, Area.TEMPLE, Area.VADER])
    OBI_WAN_KENOBI_JEDI_MASTER =         75, dict(readable_name="Obi-Wan Kenobi (Jedi Master)", unlock_method=UnlockMethod.STORY, areas=[Area.KAMINO, Area.JEDI, Area.DOOKU])
    PADME =                              76, dict(readable_name="Padmé", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.PALACERESCUE, purchase_cost=20_000)
    PADME_BATTLE =                       77, dict(readable_name="Padmé (Battle)", unlock_method=UnlockMethod.STORY, areas=[Area.RETAKEPALACE])
    PADME_CLAWED =                       78, dict(readable_name="Padmé (Clawed)", unlock_method=UnlockMethod.STORY, areas=[Area.JEDI])
    PADME_GEONOSIS =                     79, dict(readable_name="Padmé (Geonosis)", unlock_method=UnlockMethod.STORY, areas=[Area.FACTORY])
    QUEEN_AMIDALA =                      80, dict(readable_name="Queen Amidala", unlock_method=UnlockMethod.STORY, areas=[Area.PALACERESCUE])
    SUPER_BATTLE_DROID =                 81, dict(readable_name="Super Battle Droid", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.JEDI, purchase_cost=25_000)
    KI_ADI_MUNDI =                       82, dict(readable_name="Ki-Adi Mundi", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.JEDI, purchase_cost=30_000)
    KIT_FISTO =                          83, dict(readable_name="Kit Fisto", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.JEDI, purchase_cost=35_000)
    LUMINARA =                           84, dict(readable_name="Luminara", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.JEDI, purchase_cost=28_000)
    SHAAK_TI =                           85, dict(readable_name="Shaak Ti", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.JEDI, purchase_cost=36_000)
    CLONE =                              86, dict(readable_name="Clone", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.KAMINO, purchase_cost=13_000)
    CLONE_EPISODE_III =                  87, dict(readable_name="Clone (Episode III)", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.KASHYYYK, purchase_cost=10_000)
    CLONE_EPISODE_III_PILOT =            88, dict(readable_name="Clone (Episode III, Pilot)", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.KASHYYYK, purchase_cost=11_000)
    COMMANDER_CODY =                     89, dict(readable_name="Commander Cody", unlock_method=UnlockMethod.STORY, areas=[Area.GRIEVOUS])
    CLONE_EPISODE_III_SWAMP =            90, dict(readable_name="Clone (Episode III, Swamp)", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.KASHYYYK, purchase_cost=12_000)
    CLONE_EPISODE_III_WALKER =           91, dict(readable_name="Clone (Episode III, Walker)", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.KASHYYYK, purchase_cost=12_000)
    DISGUISED_CLONE =                    92, dict(readable_name="Disguised Clone", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.TEMPLE, purchase_cost=12_000)
    ANAKIN_SKYWALKER_BOY =               93, dict(readable_name="Anakin Skywalker (Boy)", unlock_method=UnlockMethod.STORY, areas=[Area.RETAKEPALACE])
    BOBA_FETT_BOY =                      94, dict(readable_name="Boba Fett (Boy)", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.JEDI, purchase_cost=5500)
    GEONOSIAN =                          95, dict(readable_name="Geonosian", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.FACTORY, purchase_cost=20_000)
    ANAKIN_SKYWALKER_JEDI =              96, dict(readable_name="Anakin Skywalker (Jedi)", unlock_method=UnlockMethod.STORY, areas=[Area.CRUISER, Area.VADER])
    ANAKIN_SKYWALKER_PADAWAN =           97, dict(readable_name="Anakin Skywalker (Padawan)", unlock_method=UnlockMethod.STORY, areas=[Area.FACTORY, Area.JEDI, Area.DOOKU])
    CAPTAIN_PANAKA =                     98, dict(readable_name="Captain Panaka", unlock_method=UnlockMethod.STORY, areas=[Area.PALACERESCUE, Area.RETAKEPALACE])
    JAR_JAR_BINKS =                      99, dict(readable_name="Jar Jar Binks", unlock_method=UnlockMethod.STORY, areas=[Area.GUNGAN])
    PK_DROID =                          100, dict(readable_name="PK Droid", unlock_method=UnlockMethod.START, purchase_cost=1500)
    ROYAL_GUARD =                       101, dict(readable_name="Royal Guard", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.PALACERESCUE, purchase_cost=10_000)
    GAMORREAN_GUARD =                   102, dict(readable_name="Gamorrean Guard", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.JABBASPALACE, purchase_cost=40_000)
    COUNT_DOOKU =                       103, dict(readable_name="Count Dooku", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.CRUISER, purchase_cost=100_000)
    QUI_GON_JINN =                      104, dict(readable_name="Qui-Gon Jinn", unlock_method=UnlockMethod.STORY, areas=[Area.NEGOTIATIONS, Area.GUNGAN, Area.PALACERESCUE, Area.RETAKEPALACE, Area.MAUL])
    HAN_SOLO_FROZEN_IN_CARBONITE =      105, dict(readable_name="Han Solo (frozen in carbonite)", unlock_method=UnlockMethod.EXTRA_TOGGLE, areas=[Area.CLOUDCITYTRAP, Area.CLOUDCITYESCAPE, Area.JABBASPALACE, Area.E5CHARACTERBONUS])
    BANTHA =                            106, dict(readable_name="Bantha")
    REBEL_TROOPER_HOTH =                107, dict(readable_name="Rebel Trooper (Hoth)", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.HOTHESCAPE, purchase_cost=16_000)
    TAUNTAUN =                          108, dict(readable_name="Tauntaun")
    WAMPA =                             109, dict(readable_name="Wampa", unlock_method=UnlockMethod.EXTRA_TOGGLE, areas=[Area.E5VEHICLEBONUS])
    MINI_REPUBLIC_CRUISER =             110, dict(readable_name="Republic Cruiser", unlock_method=UnlockMethod.MINIKIT, area=Area.NEGOTIATIONS)
    MINI_GUNGAN_BONGO =                 111, dict(readable_name="Gungan Bongo", unlock_method=UnlockMethod.MINIKIT, area=Area.GUNGAN)
    MINI_ROYAL_STARSHIP =               112, dict(readable_name="Royal Starship", unlock_method=UnlockMethod.MINIKIT, area=Area.PALACERESCUE)
    MINI_SEBULBAS_POD =                 113, dict(readable_name="Sebulba's Pod", unlock_method=UnlockMethod.MINIKIT, area=Area.PODSPRINT)
    MINI_NABOO_STARFIGHTER =            114, dict(readable_name="Naboo Starfighter", unlock_method=UnlockMethod.MINIKIT, area=Area.RETAKEPALACE)
    MINI_SITH_INFILTRATOR =             115, dict(readable_name="Sith Infiltrator", unlock_method=UnlockMethod.MINIKIT, area=Area.MAUL)
    MINI_JEDI_STARFIGHTER =             116, dict(readable_name="Jedi Starfighter", unlock_method=UnlockMethod.MINIKIT, area=Area.KAMINO)
    MINI_DROIDEKA =                     117, dict(readable_name="Droideka", unlock_method=UnlockMethod.MINIKIT, area=Area.FACTORY)
    MINI_REPUBLIC_GUNSHIP =             118, dict(readable_name="Republic Gunship", unlock_method=UnlockMethod.MINIKIT, area=Area.JEDI)
    MINI_AT_TE =                        119, dict(readable_name="AT-TE", unlock_method=UnlockMethod.MINIKIT, area=Area.GUNSHIP)
    MINI_SOLAR_SAILOR =                 120, dict(readable_name="Solar Sailor", unlock_method=UnlockMethod.MINIKIT, area=Area.DOOKU)
    MINI_DROP_SHIP =                    121, dict(readable_name="Drop Ship", unlock_method=UnlockMethod.MINIKIT, area=Area.DOGFIGHT)
    MINI_EMERGENCY_SHIP =               122, dict(readable_name="Emergency Ship", unlock_method=UnlockMethod.MINIKIT, area=Area.CRUISER)
    MINI_JEDI_STARFIGHTER_EPISODE_III = 123, dict(readable_name="Jedi Starfighter (Episode III)", unlock_method=UnlockMethod.MINIKIT, area=Area.GRIEVOUS)
    MINI_WOOKIEE_CAT =                  124, dict(readable_name="Wookiee Cat", unlock_method=UnlockMethod.MINIKIT, area=Area.KASHYYYK)
    MINI_ARC_FIGHTER =                  125, dict(readable_name="ARC Fighter", unlock_method=UnlockMethod.MINIKIT, area=Area.TEMPLE)
    MINI_V_WING =                       126, dict(readable_name="V wing", unlock_method=UnlockMethod.MINIKIT, area=Area.VADER)
    RANCOR =                            127, dict(readable_name="Rancor", unlock_method=UnlockMethod.EXTRA_TOGGLE, areas=[Area.E1VEHICLEBONUS])
    TIE_INTERCEPTOR =                   128, dict(readable_name="TIE Interceptor", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.DEATHSTARBATTLE, purchase_cost=40_000)
    PRINCESS_LEIA_BOUSHH =              129, dict(readable_name="Princess Leia (Boushh)", unlock_method=UnlockMethod.STORY, areas=[Area.JABBASPALACE])
    ROBOT_BASE =                        130
    GRAND_MOFF_TARKIN =                 131, dict(readable_name="Grand Moff Tarkin", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.DEATHSTARRESCUE, purchase_cost=38_000)
    BAT =                               132
    SNAKE =                             133
    CANNON =                            134, dict(readable_name="Skiff Cannon")
    GRABBERCONTROL =                    135, dict(readable_name="Crane Control")
    MAGNET =                            136
    DEWBACK =                           137, dict(readable_name="Dewback")
    HEAVYREPEATINGCANNON =              138
    MINI_IMPERIAL_SHUTTLE =             139, dict(readable_name="Imperial Shuttle", unlock_method=UnlockMethod.MINIKIT, area=Area.EMPERORFIGHT)
    MINI_SLAVE_1 =                      140, dict(readable_name="Slave 1", unlock_method=UnlockMethod.MINIKIT, area=Area.CLOUDCITYESCAPE)
    HAN_SOLO_SKIFF =                    141, dict(readable_name="Han Solo (Skiff)", unlock_method=UnlockMethod.STORY, areas=[Area.JABBASPALACE, Area.SARLACCPIT])
    HAN_SOLO_HOOD =                     142, dict(readable_name="Han Solo (Hood)", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.HOTHESCAPE, purchase_cost=20_000)
    HAN_SOLO_HOTH =                     143, dict(readable_name="Han Solo (Hoth)", unlock_method=UnlockMethod.STORY, areas=[Area.HOTHESCAPE])
    MINI_TIE_ADVANCED =                 144, dict(readable_name="TIE Advanced", unlock_method=UnlockMethod.MINIKIT, area=Area.DEATHSTARBATTLE)
    MINI_TIE_FIGHTER =                  145, dict(readable_name="TIE Fighter", unlock_method=UnlockMethod.MINIKIT, area=Area.ASTEROIDCHASE)
    MINI_SANDCRAWLER =                  146, dict(readable_name="Sandcrawler", unlock_method=UnlockMethod.MINIKIT, area=Area.TATOOINE)
    MINI_AT_ST =                        147, dict(readable_name="AT-ST", unlock_method=UnlockMethod.MINIKIT, area=Area.ENDORBATTLE)
    MINI_AT_AT =                        148, dict(readable_name="AT-AT", unlock_method=UnlockMethod.MINIKIT, area=Area.HOTHBATTLE)
    MINI_STAR_DESTROYER =               149, dict(readable_name="Star Destroyer", unlock_method=UnlockMethod.MINIKIT, area=Area.BLOCKADERUNNER)
    MINI_Y_WING =                       150, dict(readable_name="Y-wing", unlock_method=UnlockMethod.MINIKIT, area=Area.DEATHSTARESCAPE)
    MINI_SNOWSPEEDER =                  151, dict(readable_name="Snowspeeder", unlock_method=UnlockMethod.MINIKIT, area=Area.HOTHESCAPE)
    MINI_SAIL_BARGE =                   152, dict(readable_name="Sail Barge", unlock_method=UnlockMethod.MINIKIT, area=Area.SARLACCPIT)
    MINI_DESERT_SKIFF =                 153, dict(readable_name="Desert Skiff", unlock_method=UnlockMethod.MINIKIT, area=Area.JABBASPALACE)
    MINI_CLOUD_CAR =                    154, dict(readable_name="Cloud Car", unlock_method=UnlockMethod.MINIKIT, area=Area.CLOUDCITYTRAP)
    MINI_TIE_BOMBER =                   155, dict(readable_name="TIE Bomber", unlock_method=UnlockMethod.MINIKIT, area=Area.SPEEDERCHASE)
    LUKE_SKYWALKER_PILOT =              156, dict(readable_name="Luke Skywalker (Pilot)", unlock_method=UnlockMethod.STORY, areas=[Area.DAGOBAH])
    LUKE_SKYWALKER_DAGOBAH =            157, dict(readable_name="Luke Skywalker (Dagobah)", unlock_method=UnlockMethod.STORY, areas=[Area.DAGOBAH])
    UGNAUGHT =                          158, dict(readable_name="Ugnaught", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.CLOUDCITYESCAPE, purchase_cost=36_000)
    CATAPULT =                          159, dict(readable_name="Ewok Catapult")
    SERVICE_CAR =                       160, dict(readable_name="Service Car")
    PRINCESS_LEIA_SLAVE =               161, dict(readable_name="Princess Leia (Slave)", unlock_method=UnlockMethod.STORY, areas=[Area.SARLACCPIT])
    PRINCESS_LEIA_ENDOR =               162, dict(readable_name="Princess Leia (Endor)", unlock_method=UnlockMethod.STORY, areas=[Area.SPEEDERCHASE, Area.ENDORBATTLE])
    GRABBERR2CONTROL =                  163
    ATST =                              164, dict(readable_name="AT-ST")
    WOMP_RAT =                          165, dict(readable_name="Womp Rat", unlock_method=UnlockMethod.EXTRA_TOGGLE, areas=[Area.TATOOINE, Area.MOSEISLEY, Area.JABBASPALACE, Area.ENDORBATTLE, Area.BONUS, Area.BONUS2, Area.E4CHARACTERBONUS])
    WORM =                              166
    DUVET =                             167
    STRANGER_1 =                        168, dict(readable_name="Stranger 1", unlock_method=UnlockMethod.START)
    STRANGER_2 =                        169, dict(readable_name="Stranger 2", unlock_method=UnlockMethod.START)
    MOSEISLEYCITIZEN =                  170
    GREEDO =                            171, dict(readable_name="Greedo", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.MOSEISLEY, purchase_cost=60_000)
    IMPERIAL_SPY =                      172, dict(readable_name="Imperial Spy", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.MOSEISLEY, purchase_cost=13_500)
    CANTINABAND =                       173
    DROID_1 =                           174, dict(readable_name="Droid 1", unlock_method=UnlockMethod.EXTRA_TOGGLE, areas=[Area.TATOOINE, Area.MOSEISLEY, Area.E4CHARACTERBONUS])
    DROID_2 =                           175, dict(readable_name="Droid 2", unlock_method=UnlockMethod.EXTRA_TOGGLE, areas=[Area.TATOOINE, Area.MOSEISLEY, Area.E4CHARACTERBONUS])
    DROID_3 =                           176, dict(readable_name="Droid 3", unlock_method=UnlockMethod.EXTRA_TOGGLE, areas=[Area.TATOOINE, Area.MOSEISLEY, Area.E4CHARACTERBONUS])
    DROID_4 =                           177, dict(readable_name="Droid 4", unlock_method=UnlockMethod.EXTRA_TOGGLE, areas=[Area.TATOOINE, Area.MOSEISLEY, Area.E4CHARACTERBONUS])
    DREVAZAN =                          178
    SENTRYDROID =                       179
    MOSCANNON =                         180, dict(readable_name="Mos Eisley Cannon")
    PONDABABA =                         181
    TIE_FIGHTER_DARTH_VADER =           182, dict(readable_name="TIE Fighter (Darth Vader)", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.DEATHSTARBATTLE, purchase_cost=50_000)
    JABBA =                             183
    BOMARRMONK =                        184, dict(readable_name="B'omarr Monk")
    BIB_FORTUNA =                       185, dict(readable_name="Bib Fortuna", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.JABBASPALACE, purchase_cost=16_000)
    SKIFF_GUARD =                       186, dict(readable_name="Skiff Guard", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.SARLACCPIT, purchase_cost=12_000)
    MOONCAR =                           187, dict(readable_name="Moon Car")
    TRACTOR =                           188, dict(readable_name="Tractor")
    TOWNCAR =                           189, dict(readable_name="Town Car")
    REBEL_FRIEND =                      190, dict(readable_name="Rebel Friend", unlock_method=UnlockMethod.STORY, areas=[Area.BLOCKADERUNNER])
    CLOUDCAR =                          191, dict(readable_name="Cloud Car")
    LOBOT =                             192, dict(readable_name="Lobot", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.CLOUDCITYESCAPE, purchase_cost=11_000)
    BESPIN_GUARD =                      193, dict(readable_name="Bespin Guard", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.CLOUDCITYESCAPE, purchase_cost=15_000)
    IMPERIAL_GUARD =                    194, dict(readable_name="Imperial Guard", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.EMPERORFIGHT, purchase_cost=45_000)
    BEN_KENOBI_GHOST =                  195, dict(readable_name="Ben Kenobi (Ghost)", unlock_method=UnlockMethod.ALL_EPISODES_COMPLETE, purchase_cost=1_100_000)
    PALACE_GUARD =                      196, dict(readable_name="Palace Guard", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.JABBASPALACE, purchase_cost=14_000)
    IG_88 =                             197, dict(readable_name="IG-88", unlock_method=UnlockMethod.ALL_EPISODES_COMPLETE, purchase_cost=100_000)
    IMPERIAL_SHUTTLE =                  198, dict(readable_name="Imperial Shuttle", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.ASTEROIDCHASE, purchase_cost=25_000)
    EWOK =                              199, dict(readable_name="Ewok", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.ENDORBATTLE, purchase_cost=34_000)
    TROOPERCANNON =                     200, dict(readable_name="Stormtrooper Cannon")
    LANDO_PALACE_GUARD =                201, dict(readable_name="Lando (Palace Guard)", unlock_method=UnlockMethod.STORY, areas=[Area.SARLACCPIT])
    CANTINAALIENS =                     202
    SNOWMOB =                           203, dict(readable_name="Snowmobile")
    LUKE_SKYWALKER_HOTH =               204, dict(readable_name="Luke Skywalker (Hoth)", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.HOTHESCAPE, purchase_cost=14_000)
    PRINCESS_LEIA_PRISONER =            205, dict(readable_name="Princess Leia (Prisoner)", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.CLOUDCITYESCAPE, purchase_cost=22_000)
    HAN_SOLO_ENDOR =                    206, dict(readable_name="Han Solo (Endor)", unlock_method=UnlockMethod.STORY, areas=[Area.ENDORBATTLE])
    CAPTAIN_ANTILLES =                  207, dict(readable_name="Captain Antilles", unlock_method=UnlockMethod.STORY, areas=[Area.BLOCKADERUNNER])
    CURTAINS =                          208
    TIE_BOMBER =                        209, dict(readable_name="TIE Bomber", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.ASTEROIDCHASE, purchase_cost=60_000)
    BIGGUN =                            210, dict(readable_name="Sail Barge Cannon")
    ADMIRAL_ACKBAR =                    211, dict(readable_name="Admiral Ackbar", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.DEATHSTAR2BATTLE, purchase_cost=33_000)
    BOSSK =                             212, dict(readable_name="Bossk", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.JABBASPALACE, purchase_cost=75_000)
    DENGAR =                            213, dict(readable_name="Dengar", unlock_method=UnlockMethod.ALL_EPISODES_COMPLETE, purchase_cost=70_000)
    REPUBLIC_GUNSHIP_ORIGNAL =          214, dict(readable_name="Republic Gunship")  # Presumed to be the bonus level version.
    GEONOSIANFIGHTER =                  215
    DOOKUSSPEEDER =                     216
    UNPLAYABLE_DARTH_VADER =            217, dict(readable_name="Darth Vader")
    ANAKIN_JEDI_SCARRED =               218
    PADMEUPTHEDUFF_MUSTAFAR =           219, dict(readable_name="Padmé")
    ROYALNABOOSTARSHIP =                220
    JEDI_STARFIGHTER_YELLOW =           221, dict(readable_name="Jedi Starfighter (Yellow)", unlock_method=UnlockMethod.STORY, areas=[Area.DOGFIGHT])
    WOOKIEFLYER =                       222, dict(readable_name="Wookie Flyer")
    WICKET =                            223, dict(readable_name="Wicket", unlock_method=UnlockMethod.STORY, areas=[Area.ENDORBATTLE])
    REBEL_ENGINEER =                    224, dict(readable_name="Rebel Engineer", unlock_method=UnlockMethod.EXTRA_TOGGLE, areas=[Area.BLOCKADERUNNER, Area.HOTHESCAPE])
    FOUR_LOM =                          225, dict(readable_name="4-LOM", unlock_method=UnlockMethod.ALL_EPISODES_COMPLETE, purchase_cost=45_000)
    ANAKIN_SKYWALKER_GHOST =            226, dict(readable_name="Anakin Skywalker (Ghost)", unlock_method=UnlockMethod.ALL_EPISODES_COMPLETE, purchase_cost=1_000_000)
    YODA_GHOST =                        227, dict(readable_name="Yoda (Ghost)", unlock_method=UnlockMethod.ALL_EPISODES_COMPLETE, purchase_cost=1_200_000)
    AT_AT_DRIVER =                      228, dict(readable_name="AT-AT Driver", unlock_method=UnlockMethod.EXTRA_TOGGLE, areas=[Area.HOTHESCAPE, Area.SPEEDERCHASE])
    TENNUMB =                           229
    ATST_LOWRES =                       230
    SKELETON =                          231, dict(readable_name="Skeleton", unlock_method=UnlockMethod.EXTRA_TOGGLE, areas=[Area.JEDI, Area.TEMPLE, Area.TATOOINE, Area.DEATHSTARRESCUE, Area.HOTHESCAPE, Area.DAGOBAH, Area.CLOUDCITYTRAP, Area.E3CHARACTERBONUS])
    TWO_ONEB =                          232
    IMPERIAL_ENGINEER =                 233, dict(readable_name="Imperial Engineer", unlock_method=UnlockMethod.EXTRA_TOGGLE, areas=[Area.DEATHSTARRESCUE, Area.DEATHSTARESCAPE, Area.ENDORBATTLE, Area.EMPERORFIGHT, Area.E6CHARACTERBONUS])
    UNPLAYABLE_ADMIRAL_ACKBAR =         234, dict(readable_name="Admiral Ackbar")
    GENERALVEERS =                      235, dict(readable_name="Grand Moff Tarkin")
    SARLACC =                           236
    CLOUDCITYCITIZEN =                  237
    UNPLAYABLE_REBEL_GENERAL =          238, dict(readable_name="Rebel Trooper")
    LANDO_CALRISSIAN_GENERAL =          239, dict(readable_name="Lando Calrissian")
    LANDO_CALRISSIAN_WAISTCOAT =        240, dict(readable_name="Lando Calrissian")
    NIENNUMB =                          241
    LUKE_SKYWALKER_JEDI_PYJAMAS =       242, dict(readable_name="Luke Skywalker (Jedi)")
    LUKE_SKYWALKER_JEDI_CEREMONY =      243, dict(readable_name="Luke Skywalker (Jedi)")
    SKIFFSHADOW =                       244
    BASKETCANNON =                      245, dict(readable_name="Basketball Cannon")
    DROIDSTARFIGHTER =                  246
    TRADEFEDERATIONLANDINGSHIP =        247
    MTT =                               248
    KAADU =                             249
    STAP =                              250
    FALUMPASET =                        251
    GUNGANBONGO =                       252
    REPTEER =                           253
    BOSS_NASS =                         254, dict(readable_name="Boss Nass", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.GUNGAN, purchase_cost=15_000)
    AAT =                               255
    ATT =                               256
    # This is presumed to be the old one used in the bonus level.
    ANAKINS_POD_ORIGINAL =              257, dict(readable_name="Anakin's Pod")
    ANAKINS_POD_GREEN_ORIGINAL =        258, dict(readable_name="Anakin's Pod (Green)")  # P2 story version
    ANAKINS_POD =                       259, dict(readable_name="Anakin's Pod", unlock_method=UnlockMethod.STORY, areas=[Area.PODSPRINT, Area.PODRACE])  # This is the unlockable one.
    ANAKINS_POD_GREEN =                 260, dict(readable_name="Anakin's Pod (Green)")  # P2 story version
    SEBULBAS_POD =                      261, dict(readable_name="Sebulba's Pod", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.PODSPRINT, purchase_cost=20_000)
    GASGANOSPOD =                       262
    MISCPOD =                           263
    ANOTHERMISCPOD =                    264
    MISCPOD2 =                          265
    ANOTHERMISCPOD2 =                   266
    SEBULBA =                           267
    PIT_DROID =                         268, dict(readable_name="Pit Droid", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.PODSPRINT, purchase_cost=4000)
    WATTO =                             269, dict(readable_name="Watto", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.PODSPRINT, purchase_cost=16_000)
    MAWHONIC =                          270
    FLASHSPEEDER =                      271, dict(readable_name="Flash Speeder")
    NABOO_STARFIGHTER =                 272, dict(readable_name="Naboo Starfighter", unlock_method=UnlockMethod.STORY, areas=[Area.ANAKINSFLIGHT])
    NABOO_STARFIGHTER_BLUE =            273, dict(readable_name="Naboo Starfighter (Blue)")
    NABOO_STARFIGHTER_GREEN =           274, dict(readable_name="Naboo Starfighter (Green)")
    GUNGAN =                            275, dict(readable_name="Gungan")
    CAPTAIN_TARPALS =                   276, dict(readable_name="Captain Tarpals", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.GUNGAN, purchase_cost=17_500)
    ZAMS_AIRSPEEDER =                   277, dict(readable_name="Zam's Airspeeder", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.PURSUIT, purchase_cost=24_000)
    BOMBTOW =                           278
    KAMINO =                            279
    LAMA_SU =                           280, dict(readable_name="Lama Su", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.KAMINO, purchase_cost=9000)
    TAUN_WE =                           281, dict(readable_name="Taun We", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.KAMINO, purchase_cost=9000)
    KAMINOANDROID =                     282
    JEDI_BATTLE_GENERIC_JEDI_BOB =      283, dict(readable_name="Ki-Adi Mundi")
    # Presumed to be the P2 version of the bonus level story version.
    REPUBLIC_GUNSHIP_GREEN_ORIGINAL =   284, dict(readable_name="Republic Gunship (Green)")
    REPUBLIC_GUNSHIP =                  285, dict(readable_name="Republic Gunship", unlock_method=UnlockMethod.STORY, areas=[Area.GUNSHIP, Area.BONUS_GUNSHIP])  # This is the unlockable one.
    REPUBLIC_GUNSHIP_GREEN =            286, dict(readable_name="Republic Gunship (Green)")  # P2 story version
    HAILFIREDROID =                     287
    REPUBLICATTE =                      288
    JUMBOHOMINGDROID =                  289
    SPEEDER_DOOKU =                     290
    JEDI_STARFIGHTER_RED =              291, dict(readable_name="Jedi Starfighter (Red)", unlock_method=UnlockMethod.STORY, areas=[Area.DOGFIGHT])
    DROID_TRIFIGHTER =                  292, dict(readable_name="Droid Trifighter", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.DOGFIGHT, purchase_cost=28_000)
    VULTURE_DROID =                     293, dict(readable_name="Vulture Droid", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.DOGFIGHT, purchase_cost=30_000)
    BUZZ_DROID =                        294, dict(readable_name="Buzz Droid", unlock_method=UnlockMethod.EXTRA_TOGGLE, areas=[Area.DOGFIGHT, Area.CRUISER, Area.GRIEVOUS, Area.E2CHARACTERBONUS])
    CLONE_ARCFIGHTER =                  295, dict(readable_name="Clone Arcfighter", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.DOGFIGHT, purchase_cost=33_000)
    BABYLEIA =                          296
    BABYLUKE =                          297
    MEDIC =                             298
    PADMEUPTHEDUFF =                    299, dict(readable_name="Padmé")
    JEDISTARFIGHTER =                   300
    DARTHSIDIOUS =                      301
    STAP2 =                             302, dict(readable_name="STAP")
    MAPCAR =                            303, dict(readable_name="Cantina Car")
    DEXTER_JETTSTER =                   304, dict(readable_name="Dexter Jettster", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.PURSUIT, purchase_cost=10_000)
    UNPLAYABLE_ZAM_WESELL =             305, dict(readable_name="Zam Wesell")
    SANSWEET =                          306
    WHIP =                              307
    ZAMDROID =                          308
    FIRETRUCK =                         309, dict(readable_name="Firetruck")
    LIFEBOAT =                          310, dict(readable_name="Lifeboat")
    UNPLAYABLE_BASKETCANNON =           311  # I don't know what this BASKETCANNON is used for.
    MINI_ZAMS_AIRSPEEDER =              312, dict(readable_name="Zam's Airspeeder", unlock_method=UnlockMethod.MINIKIT, area=Area.PURSUIT)
    MINI_LAND_SPEEDER =                 313, dict(readable_name="Land Speeder", unlock_method=UnlockMethod.MINIKIT, area=Area.MOSEISLEY)
    R2_Q5 =                             314, dict(readable_name="R2-Q5", unlock_method=UnlockMethod.ALL_EPISODES_COMPLETE, purchase_cost=100_000)
    AAYLA_SECURA =                      315, dict(readable_name="Aayla Secura", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.JEDI, purchase_cost=37_000)
    PLO_KOON =                          316, dict(readable_name="Plo Koon", unlock_method=UnlockMethod.AREA_COMPLETE, area=Area.JEDI, purchase_cost=39_000)
    INDIANA_JONES =                     317, dict(readable_name="Indiana Jones", unlock_method=UnlockMethod.INDY_TRAILER, purchase_cost=50_000)
    RAFT =                              318
    # Events
    EVENT_SUPER_GONK_DROID = 1 + _EVENT_OFFSET, dict(readable_name="Super Gonk Droid")


AreaToCharacter = dict[Area, frozenset[Character]]
def _make_area_lookups() -> tuple[AreaToCharacter, AreaToCharacter, AreaToCharacter]:
    area_to_story_characters: AreaToCharacter = {}
    area_to_purchase_characters: AreaToCharacter = {}
    area_to_extra_toggle_characters: AreaToCharacter = {}
    empty = frozenset()
    for c in Character:
        if c.unlock_method is UnlockMethod.START or c.unlock_method is UnlockMethod.ALL_EPISODES_COMPLETE:
            if c.purchase_cost is None:
                # Character is unlocked from the start (STRANGER 1 and STRANGER 2).
                continue
            else:
                assert c.purchase_cost is not None
                d = area_to_purchase_characters
            d[Area.MAP] = d.get(Area.MAP, empty) | {c}
        elif c.unlock_method is UnlockMethod.INDY_TRAILER:
            # The LOSTTEMPLE Area does not get completed when watching the trailer, but rather a different byte,
            # dedicated to recording whether the trailer has been watched, gets set. For purposes of assigning the
            # character purchase to an Area however, Indiana Jones is assigned to LOSTTEMPLE, so that the purchase
            # location gets given the expected name.
            d = area_to_purchase_characters
            d[Area.LOSTTEMPLE] = d.get(Area.LOSTTEMPLE, empty) | {c}
        else:
            if c.unlock_method is UnlockMethod.STORY:
                d = area_to_story_characters
            elif c.unlock_method is UnlockMethod.AREA_COMPLETE:
                assert c.purchase_cost is not None
                d = area_to_purchase_characters
            elif c.unlock_method is UnlockMethod.EXTRA_TOGGLE:
                d = area_to_extra_toggle_characters
            else:
                continue
            assert c.areas is not None
            for area in c.areas:
                d[area] = d.get(area, empty) | {c}
    return area_to_story_characters, area_to_purchase_characters, area_to_extra_toggle_characters


AREA_TO_STORY_CHARACTERS, AREA_TO_PURCHASE_CHARACTERS, AREA_TO_EXTRA_TOGGLE_CHARACTERS = _make_area_lookups()
del _make_area_lookups

CHARACTER_TO_STORY_AREA = {
    character: area for area, characters in AREA_TO_STORY_CHARACTERS.items() for character in characters
}
CHARACTER_TO_PURCHASE_AREA = {
    character: area for area, characters in AREA_TO_PURCHASE_CHARACTERS.items() for character in characters
}
CHARACTER_TO_EXTRA_TOGGLE_AREA = {
    character: area for area, characters in AREA_TO_EXTRA_TOGGLE_CHARACTERS.items() for character in characters
}

ALL_LOGIC_RELEVANT_CHARACTERS = {c for c in Character if c.is_logic_relevant()}
NORMAL_LOGIC_RELEVANT_CHARACTERS = {
    c for c in ALL_LOGIC_RELEVANT_CHARACTERS if c.unlock_method is not UnlockMethod.EXTRA_TOGGLE
}
_MINIKIT_BONUS_EXTRA_TOGGLE_CHARACTERS = {Character.WAMPA, Character.RANCOR}
EXTRA_TOGGLE_LOGIC_RELEVANT_CHARACTERS = {
    c for c in ALL_LOGIC_RELEVANT_CHARACTERS
    if c.unlock_method is UnlockMethod.EXTRA_TOGGLE
    and c not in _MINIKIT_BONUS_EXTRA_TOGGLE_CHARACTERS
}
ALL_SENDABLE_CHARACTERS = {c for c in ALL_LOGIC_RELEVANT_CHARACTERS if c.is_sendable()}
_NAME_TO_SENDABLE_CHARACTER = {c.readable_name: c for c in ALL_SENDABLE_CHARACTERS}
