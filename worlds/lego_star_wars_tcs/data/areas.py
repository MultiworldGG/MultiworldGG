from typing import TypedDict, TYPE_CHECKING, Iterable
from typing_extensions import deprecated
from enum import IntEnum, IntFlag

from .extras import Extra
from .levels import Level


if TYPE_CHECKING:
    from .bosses import Boss
    from .characters import Character


__all__ = [
    "Area",
    "AreaFlag",
    "EPISODE_AREA_LOOKUP",
    "PURCHASABLE_NON_POWER_BRICK_EXTRAS",
    "EXTRA_TO_AREA",
    "POWER_BRICK_EXTRAS",
    "BONUS_ROOM_BONUSES",
    "BONUS_ROOM_VEHICLE_BONUSES",
    "VEHICLE_CHAPTERS",
    "ALL_CHAPTER_AREAS",
]

class AreaFlag(IntFlag):
    VEHICLE_AREA = 0x1
    ENDING_AREA = 0x2
    BONUS_AREA = 0x4
    VEHICLE_BONUS = VEHICLE_AREA | BONUS_AREA
    SINGLE_BUFFER = 0x8
    CHAPTER = 0x10
    TEST_AREA = 0x20
    HUB_AREA = 0x40
    NO_CHARACTER_COLLISION = 0x80
    COLLECT_ALL_STUDS_BONUS = 0x100
    NO_PICKUP_GRAVITY = 0x200
    OVERRIDE_THINGS_SCENE = 0x400
    NO_GOLD_BRICK = 0x800
    NO_FREEPLAY = 0x1000
    NO_COMPLETION_POINTS = 0x2000
    UNKNOWN_0x4000 = 0x4000
    UNKNOWN_0x8000 = 0x8000


class AreaInitializer(TypedDict):
    episode_index: int
    area_index: int
    readable_name: str
    flags: AreaFlag
    story_true_jedi: int
    free_play_true_jedi: int
    extra: Extra | None
    levels: list[Level]


_AREA_SAVE_DATA_START = 0x86e114
_AREA_SAVE_DATA_SIZE = 0xc


# noinspection LongLine
class Area(IntEnum):
    episode_index: int
    area_index: int
    readable_name: str
    flags: AreaFlag
    story_true_jedi: int
    free_play_true_jedi: int
    extra: Extra | None
    levels: tuple[Level, ...]
    save_data_address: int

    def __new__(cls, *args, **kwargs):
        obj = int.__new__(cls, args[0])
        obj._value_ = args[0]
        return obj

    def __init__(self,
                 _id,
                 area_initializer: AreaInitializer,
                 ):
        self.episode_index = area_initializer["episode_index"]
        self.area_index = area_initializer["area_index"]
        self.readable_name = area_initializer["readable_name"]
        self.flags = area_initializer["flags"]
        self.story_true_jedi = area_initializer["story_true_jedi"]
        self.free_play_true_jedi = area_initializer["free_play_true_jedi"]
        self.extra = area_initializer["extra"]
        self.levels = tuple(area_initializer["levels"])
        self.save_data_address = _AREA_SAVE_DATA_START + self * _AREA_SAVE_DATA_SIZE

    def get_first_playable_level(self) -> Level | None:
        return next(filter(Level.is_playable, self.levels), None)

    def get_status_level(self) -> Level:
        # Status levels are last when present.
        status_level = self.levels[-1]
        if status_level.is_status():
            return status_level
        # Workaround for the Area not being fully implemented in the game.
        if self is Area.LOSTTEMPLE:
            # Just pretend the Area's only level is also the status level for the Area.
            assert status_level is Level.LOSTTEMPLE_A
            return status_level
        else:
            raise Exception(f"{self!r} does not have a status level")

    def get_playable_levels(self) -> list[Level]:
        return list(filter(Level.is_playable, self.levels))

    def get_story_characters(self) -> "frozenset[Character]":
        # Lazy import to prevent circular import.
        global _AREA_TO_STORY_CHARACTERS
        if not _AREA_TO_STORY_CHARACTERS:
            from .characters import AREA_TO_STORY_CHARACTERS as _AREA_TO_STORY_CHARACTERS
            assert _AREA_TO_STORY_CHARACTERS, "_AREA_TO_STORY_CHARACTERS must not be empty"
        return _AREA_TO_STORY_CHARACTERS.get(self, frozenset())

    def get_purchase_characters(self) -> "frozenset[Character]":
        # Lazy import to prevent circular import.
        global _AREA_TO_PURCHASE_CHARACTERS
        if not _AREA_TO_PURCHASE_CHARACTERS:
            from .characters import AREA_TO_PURCHASE_CHARACTERS as _AREA_TO_PURCHASE_CHARACTERS
            assert _AREA_TO_PURCHASE_CHARACTERS, "_AREA_TO_PURCHASE_CHARACTERS must not be empty"
        return _AREA_TO_PURCHASE_CHARACTERS.get(self, frozenset())

    def get_extra_toggle_characters(self) -> "frozenset[Character]":
        # Lazy import to prevent circular import.
        global _AREA_TO_EXTRA_TOGGLE_CHARACTERS
        if not _AREA_TO_EXTRA_TOGGLE_CHARACTERS:
            from .characters import AREA_TO_EXTRA_TOGGLE_CHARACTERS as _AREA_TO_EXTRA_TOGGLE_CHARACTERS
            assert _AREA_TO_EXTRA_TOGGLE_CHARACTERS, "_AREA_TO_EXTRA_TOGGLE_CHARACTERS must not be empty"
        return _AREA_TO_EXTRA_TOGGLE_CHARACTERS.get(self, frozenset())

    def is_chapter(self):
        return 0 <= self.area_index <= 5

    def get_chapter_episode(self) -> int:
        if not self.is_chapter():
            raise Exception(f"{self!r} is not a chapter.")
        return self.episode_index + 1

    def get_chapter_number_in_episode(self) -> int:
        if not self.is_chapter():
            raise Exception(f"{self!r} is not a chapter.")
        return self.area_index + 1

    def is_character_bonus(self):
        return self.area_index == 7

    def is_minikit_bonus(self):
        return self.area_index == 8

    def is_bonus_room_bonus(self):
        return self in BONUS_ROOM_BONUSES

    def is_vehicle_area(self):
        return AreaFlag.VEHICLE_AREA in self.flags

    def has_gold_brick(self):
        return AreaFlag.NO_GOLD_BRICK not in self.flags

    def prefix_name(self, name: str) -> str:
        return f"{self.readable_name} - {name}"

    def get_true_jedi_name(self) -> str:
        return self.prefix_name("True Jedi")

    def get_completion_name(self) -> str:
        return self.prefix_name("Completion")

    def get_completion_event_name(self) -> str:
        return self.get_completion_name() + " (Event)"

    def get_completion_goal_progress_event_name(self) -> str:
        return self.get_completion_name() + " (Event - Goal Progress)"

    def get_completion_gold_brick_event_name(self) -> str:
        return self.get_completion_name() + " - Gold Brick"

    def get_boss_defeat_event_name(self, boss: "Boss") -> str:
        return f"{self.get_long_name()} Defeat {boss.unique_name}"

    def get_true_jedi_gold_brick_event_name(self) -> str:
        return f"{self.get_true_jedi_name()} - Gold Brick"

    def get_all_minikits_gold_brick_event_name(self) -> str:
        return f"{self.get_long_name()} - Collect All Minikits Gold Brick"

    def get_power_brick_event_name(self) -> str:
        return f"{self.get_long_name()} - Power Brick (Event)"

    def get_short_name(self) -> str:
        """This is a legacy method, and should be considered deprecated."""
        if not self.is_chapter():
            raise Exception(f"{self!r} is not a chapter.")
        return f"{self.episode_index + 1}-{self.area_index + 1}"

    def get_long_name(self) -> str:
        if self.is_chapter():
            return f"{self.readable_name} ({self.get_short_name()})"
        # LOSTTEMPLE is not locked behind a gold brick door.
        # ANEWHOPE already has (Bonus Level) in its .readable_name to help tell it apart from Episode IV - A New Hope.
        elif self.is_bonus_room_bonus() and self is not Area.LOSTTEMPLE and self is not Area.ANEWHOPE:
            return f"{self.readable_name} (Gold Brick Bonus)"
        else:
            return self.readable_name

    def __bool__(self):
        # NEGOTIATIONS being falsey is confusing, but making it truthy would also be confusing because its value is
        # falsey. So prevent use of Area instances in boolean operations.
        raise Exception("Truthiness of Area objects is confusing. Use `area is not None` to check for absence instead.")

    @staticmethod
    def from_episode_chapter(episode: int, chapter: int) -> "Area":
        return EPISODE_AREA_LOOKUP[episode][chapter]

    @staticmethod
    @deprecated("Use Area IDs instead", category=None)  # category=None -> No runtime warning
    def from_short_name(short_name: str) -> "Area":
        """This method is deprecated as code should move to using Area objects directly, instead of using short names"""
        return _LEGACY_CHAPTER_SHORT_NAME_TO_AREA[short_name]

    @staticmethod
    def to_human_readable_list(areas: "Iterable[Area]") -> list[str]:
        """Small helper mostly intended for formatting areas to a human readable error message."""
        return [a.get_long_name() for a in sorted(areas, key=int)]

    NEGOTIATIONS =      0, dict(episode_index= 0, area_index= 0, readable_name=               "Negotiations", flags=AreaFlag(0x0010), story_true_jedi=31000, free_play_true_jedi= 64000, extra=             Extra.SUPER_GONK, levels=[Level.EP1_FAILEDNEG_INTRO1, Level.EP1_FAILEDNEG_INTRO2, Level.NEGOTIATIONS_A, Level.NEGOTIATIONS_B, Level.NEGOTIATIONS_C, Level.FAILEDNEG_OUTRO, Level.NEGOTIATIONS_STATUS])
    GUNGAN =            1, dict(episode_index= 0, area_index= 1, readable_name=          "Invasion Of Naboo", flags=AreaFlag(0x0010), story_true_jedi=44000, free_play_true_jedi= 52000, extra=              Extra.POO_MONEY, levels=[Level.GUNGAN_INTRO1, Level.GUNGAN_INTRO2, Level.GUNGAN_A, Level.GUNGAN_B, Level.GUNGAN_C, Level.GUNGAN_E, Level.GUNGAN_OUTRO2, Level.GUNGAN_STATUS])
    PALACERESCUE =      2, dict(episode_index= 0, area_index= 2, readable_name=          "Escape From Naboo", flags=AreaFlag(0x0010), story_true_jedi=48000, free_play_true_jedi= 60000, extra=  Extra.WALKIE_TALKIE_DISABLE, levels=[Level.RESCUE_INTRO1, Level.RESCUE_INTRO2, Level.RESCUE_INTRO4, Level.RESCUE_A, Level.RESCUE_B, Level.RESCUE_C, Level.RESCUE_E, Level.RESCUE_OUTRO, Level.RESCUE_STATUS])
    PODSPRINT =         3, dict(episode_index= 0, area_index= 3, readable_name=          "Mos Espa Pod Race", flags=AreaFlag(0x0019), story_true_jedi=45000, free_play_true_jedi= 45000, extra=   Extra.POWER_BRICK_DETECTOR, levels=[Level.PODSPRINT_A, Level.PODSPRINT_STATUS])
    PODRACE =           4, dict(episode_index=-1, area_index=-1, readable_name=        "Pod Race (Original)", flags=AreaFlag(0x1001), story_true_jedi=45000, free_play_true_jedi= 45000, extra=                         None, levels=[Level.PODRACE_ARRIVAL1, Level.PODRACE_ARRIVAL2, Level.PODRACE_ARRIVAL3, Level.PODRACE_ARRIVAL4, Level.PODRACE_INTRO, Level.PODRACE_B, Level.PODRACE_C, Level.PODRACE_A, Level.PODRACE_OUTRO1, Level.PODRACE_OUTRO2, Level.PODRACE_STATUS])
    RETAKEPALACE =      5, dict(episode_index= 0, area_index= 4, readable_name=        "Retake Theed Palace", flags=AreaFlag(0x0010), story_true_jedi=60000, free_play_true_jedi=100000, extra=             Extra.SUPER_SLAP, levels=[Level.RETAKE_INTRO1, Level.RETAKE_INTRO2, Level.RETAKE_INTRO3, Level.RETAKE_A, Level.RETAKE_B, Level.RETAKE_D, Level.RETAKE_E, Level.RETAKE_F, Level.RETAKE_G, Level.RETAKE_OUTRO, Level.RETAKE_STATUS])
    MAUL =              6, dict(episode_index= 0, area_index= 5, readable_name=                 "Darth Maul", flags=AreaFlag(0x0010), story_true_jedi=31000, free_play_true_jedi= 64000, extra=     Extra.FORCE_GRAPPLE_LEAP, levels=[Level.DARTHMAUL_INTRO, Level.MAUL_A, Level.MAUL_B, Level.MAUL_D, Level.MAUL_E, Level.MAUL_F, Level.MAUL_STATUS])
    E1ENDING =          7, dict(episode_index= 0, area_index= 6, readable_name=           "Episode 1 Ending", flags=AreaFlag(0x0002), story_true_jedi=    0, free_play_true_jedi=     0, extra=                         None, levels=[Level.EPISODE1ENDING_A])
    E1CHARACTERBONUS =  8, dict(episode_index= 0, area_index= 7, readable_name=  "Episode 1 Character Bonus", flags=AreaFlag(0x0004), story_true_jedi=    0, free_play_true_jedi=     0, extra=                         None, levels=[Level.E1CHARACTERBONUS_A, Level.E1CHARACTERBONUS_STATUS])
    E1VEHICLEBONUS =    9, dict(episode_index= 0, area_index= 8, readable_name=    "Episode 1 Minikit Bonus", flags=AreaFlag(0x0005), story_true_jedi=    0, free_play_true_jedi=     0, extra=                         None, levels=[Level.E1VEHICLEBONUS_A, Level.E1VEHICLEBONUS_STATUS])
    PURSUIT =          10, dict(episode_index= 1, area_index= 0, readable_name=      "Bounty Hunter Pursuit", flags=AreaFlag(0x0211), story_true_jedi=35000, free_play_true_jedi= 45000, extra=            Extra.STUD_MAGNET, levels=[Level.PURSUIT_INTRO, Level.PURSUIT_A, Level.PURSUIT_B, Level.PURSUIT_C, Level.PURSUIT_D, Level.PURSUIT_E, Level.PURSUIT_OUTRO, Level.PURSUIT_STATUS])
    KAMINO =           11, dict(episode_index= 1, area_index= 1, readable_name=        "Discovery On Kamino", flags=AreaFlag(0x0010), story_true_jedi=50000, free_play_true_jedi= 65000, extra=        Extra.DISARM_TROOPERS, levels=[Level.KAMINO_INTRO1, Level.KAMINO_INTRO2, Level.KAMINO_A, Level.KAMINO_C, Level.KAMINO_D, Level.KAMINO_E, Level.KAMINO_F, Level.KAMINO_OUTRO1, Level.KAMINO_OUTRO2, Level.KAMINO_STATUS])
    FACTORY =          12, dict(episode_index= 1, area_index= 2, readable_name=              "Droid Factory", flags=AreaFlag(0x0010), story_true_jedi=40000, free_play_true_jedi= 55000, extra=        Extra.CHARACTER_STUDS, levels=[Level.FACTORY_INTRO1, Level.FACTORY_INTRO2, Level.FACTORY_INTRO3, Level.FACTORY_A, Level.FACTORY_B, Level.FACTORY_D, Level.FACTORY_E, Level.FACTORY_F, Level.FACTORY_G, Level.FACTORY_STATUS])
    JEDI =             13, dict(episode_index= 1, area_index= 3, readable_name=                "Jedi Battle", flags=AreaFlag(0x0010), story_true_jedi= 8000, free_play_true_jedi= 16000, extra=        Extra.PERFECT_DEFLECT, levels=[Level.JEDI_INTRO, Level.JEDI_B, Level.JEDI_OUTRO, Level.JEDI_STATUS])
    GUNSHIP =          14, dict(episode_index= 1, area_index= 4, readable_name=            "Gunship Cavalry", flags=AreaFlag(0x0011), story_true_jedi=30000, free_play_true_jedi= 40000, extra=Extra.EXPLODING_BLASTER_BOLTS, levels=[Level.GUNSHIP_A, Level.GUNSHIP_B, Level.GUNSHIP_STATUS])
    BONUS_GUNSHIP =    15, dict(episode_index=-1, area_index=-1, readable_name= "Gunship Cavalry (Original)", flags=AreaFlag(0x1081), story_true_jedi=50000, free_play_true_jedi=100000, extra=                         None, levels=[Level.BONUS_GUNSHIP_A, Level.BONUS_GUNSHIP_B, Level.BONUS_GUNSHIP_STATUS])
    DOOKU =            16, dict(episode_index= 1, area_index= 5, readable_name=                "Count Dooku", flags=AreaFlag(0x0010), story_true_jedi=10000, free_play_true_jedi= 22000, extra=             Extra.FORCE_PULL, levels=[Level.DOOKU_INTRO, Level.DOOKU_B, Level.DOOKU_C, Level.DOOKU_OUTRO, Level.DOOKU_STATUS])
    E2ENDING =         17, dict(episode_index= 1, area_index= 6, readable_name=           "Episode 2 Ending", flags=AreaFlag(0x0002), story_true_jedi=    0, free_play_true_jedi=     0, extra=                         None, levels=[Level.EP2_ENDING1, Level.EP2_ENDING2])
    E2CHARACTERBONUS = 18, dict(episode_index= 1, area_index= 7, readable_name=  "Episode 2 Character Bonus", flags=AreaFlag(0x0004), story_true_jedi=    0, free_play_true_jedi=     0, extra=                         None, levels=[Level.E2CHARACTERBONUS_A, Level.E2CHARACTERBONUS_STATUS])
    E2VEHICLEBONUS =   19, dict(episode_index= 1, area_index= 8, readable_name=    "Episode 2 Minikit Bonus", flags=AreaFlag(0x0205), story_true_jedi=    0, free_play_true_jedi=     0, extra=                         None, levels=[Level.E2VEHICLEBONUS_A, Level.E2VEHICLEBONUS_STATUS])
    DOGFIGHT =         20, dict(episode_index= 2, area_index= 0, readable_name=      "Battle Over Coruscant", flags=AreaFlag(0x0019), story_true_jedi=75000, free_play_true_jedi= 75000, extra=     Extra.VEHICLE_SMART_BOMB, levels=[Level.DOGFIGHT_A, Level.DOGFIGHT_STATUS])
    CRUISER =          21, dict(episode_index= 2, area_index= 1, readable_name=        "Chancellor In Peril", flags=AreaFlag(0x0010), story_true_jedi=60000, free_play_true_jedi= 80000, extra=        Extra.SUPER_ASTROMECH, levels=[Level.CRUISER_A, Level.CRUISER_B, Level.CRUISER_C, Level.CRUISER_D, Level.CRUISER_E, Level.CRUISER_F, Level.CRUISER_G, Level.CRUISER_OUTRO1, Level.CRUISER_OUTRO2, Level.CRUISER_STATUS])
    GRIEVOUS =         22, dict(episode_index= 2, area_index= 2, readable_name=           "General Grievous", flags=AreaFlag(0x0018), story_true_jedi= 3300, free_play_true_jedi=  5000, extra=        Extra.SUPER_JEDI_SLAM, levels=[Level.GRIEVOUS_A, Level.GRIEVOUS_STATUS])
    KASHYYYK =         23, dict(episode_index= 2, area_index= 3, readable_name=        "Defense Of Kashyyyk", flags=AreaFlag(0x0010), story_true_jedi=65000, free_play_true_jedi= 90000, extra=Extra.SUPER_THERMAL_DETONATOR, levels=[Level.KASHYYYK_A, Level.KASHYYYK_B, Level.KASHYYYK_C, Level.KASHYYYK_D, Level.KASHYYYK_STATUS])
    TEMPLE =           24, dict(episode_index= 2, area_index= 4, readable_name=           "Ruin Of The Jedi", flags=AreaFlag(0x0010), story_true_jedi=35000, free_play_true_jedi= 75000, extra=          Extra.DEFLECT_BOLTS, levels=[Level.TEMPLE_INTRO, Level.TEMPLE_INTRO2, Level.TEMPLE_A, Level.TEMPLE_B, Level.TEMPLE_C, Level.TEMPLE_STATUS])
    VADER =            25, dict(episode_index= 2, area_index= 5, readable_name=                "Darth Vader", flags=AreaFlag(0x0010), story_true_jedi=25000, free_play_true_jedi= 45000, extra=              Extra.DARK_SIDE, levels=[Level.VADER_INTRO, Level.VADER_A, Level.VADER_B, Level.VADER_C, Level.VADER_STATUS])
    E3ENDING =         26, dict(episode_index= 2, area_index= 6, readable_name=           "Episode 3 Ending", flags=AreaFlag(0x0002), story_true_jedi=    0, free_play_true_jedi=     0, extra=                         None, levels=[Level.EP3_ENDING_MEDICROOM, Level.EP3_ENDING_MUSTAFAR, Level.EP3_ENDING_VADER])
    E3CHARACTERBONUS = 27, dict(episode_index= 2, area_index= 7, readable_name=  "Episode 3 Character Bonus", flags=AreaFlag(0x0004), story_true_jedi=    0, free_play_true_jedi=     0, extra=                         None, levels=[Level.E3CHARACTERBONUS_A, Level.E3CHARACTERBONUS_STATUS])
    E3VEHICLEBONUS =   28, dict(episode_index= 2, area_index= 8, readable_name=    "Episode 3 Minikit Bonus", flags=AreaFlag(0x0005), story_true_jedi=    0, free_play_true_jedi=     0, extra=                         None, levels=[Level.E3VEHICLEBONUS_A, Level.E3VEHICLEBONUS_STATUS])
    ANEWHOPE =         29, dict(episode_index=-1, area_index=-1, readable_name=   "A New Hope (Bonus Level)", flags=AreaFlag(0x0000), story_true_jedi=40000, free_play_true_jedi= 70000, extra=                         None, levels=[Level.ANEWHOPE_INTRO, Level.ANEWHOPE_A, Level.ANEWHOPE_B, Level.ANEWHOPE_STATUS])
    BLOCKADERUNNER =   30, dict(episode_index= 3, area_index= 0, readable_name=               "Secret Plans", flags=AreaFlag(0x0010), story_true_jedi=28000, free_play_true_jedi= 40000, extra=         Extra.SUPER_BLASTERS, levels=[Level.BLOCKADERUNNER_INTRO1, Level.BLOCKADERUNNER_INTRO2, Level.BLOCKADERUNNER_A, Level.BLOCKADERUNNER_B, Level.BLOCKADERUNNER_C, Level.BLOCKADERUNNER_D, Level.BLOCKADERUNNER_OUTRO1, Level.BLOCKADERUNNER_OUTRO2, Level.BLOCKADERUNNER_STATUS])
    TATOOINE =         31, dict(episode_index= 3, area_index= 1, readable_name="Through The Jundland Wastes", flags=AreaFlag(0x0010), story_true_jedi=60000, free_play_true_jedi= 90000, extra=             Extra.FAST_FORCE, levels=[Level.TATOOINE_INTRO, Level.TATOOINE_A, Level.TATOOINE_B, Level.TATOOINE_C, Level.TATOOINE_D, Level.TATOOINE_E, Level.TATOOINE_OUTRO, Level.TATOOINE_STATUS])
    MOSEISLEY =        32, dict(episode_index= 3, area_index= 2, readable_name=       "Mos Eisley Spaceport", flags=AreaFlag(0x0010), story_true_jedi=60000, free_play_true_jedi=100000, extra=      Extra.SUPER_LIGHTSABERS, levels=[Level.MOSEISLEY_INTRO, Level.MOSEISLEY_A, Level.MOSEISLEY_B, Level.MOSEISLEY_C, Level.MOSEISLEY_D, Level.MOSEISLEY_E, Level.MOSEISLEY_OUTRO1, Level.MOSEISLEY_OUTRO2, Level.MOSEISLEY_OUTRO3, Level.MOSEISLEY_STATUS])
    DEATHSTARRESCUE =  33, dict(episode_index= 3, area_index= 3, readable_name=        "Rescue The Princess", flags=AreaFlag(0x0010), story_true_jedi=60000, free_play_true_jedi= 80000, extra=           Extra.TRACTOR_BEAM, levels=[Level.DEATHSTARRESCUE_INTRO1, Level.DEATHSTARRESCUE_INTRO2, Level.DEATHSTARRESCUE_A, Level.DEATHSTARRESCUE_B, Level.DEATHSTARRESCUE_C, Level.DEATHSTARRESCUE_D, Level.DEATHSTARRESCUE_E, Level.DEATHSTARRESCUE_STATUS])
    DEATHSTARESCAPE =  34, dict(episode_index= 3, area_index= 4, readable_name=          "Death Star Escape", flags=AreaFlag(0x0010), story_true_jedi=45000, free_play_true_jedi= 65000, extra=          Extra.INVINCIBILITY, levels=[Level.DEATHSTARESCAPE_INTRO, Level.DEATHSTARESCAPE_A, Level.DEATHSTARESCAPE_B, Level.DEATHSTARESCAPE_C, Level.DEATHSTARESCAPE_D, Level.DEATHSTARESCAPE_OUTRO, Level.DEATHSTARESCAPE_STATUS])
    DEATHSTARBATTLE =  35, dict(episode_index= 3, area_index= 5, readable_name=               "Rebel Attack", flags=AreaFlag(0x0091), story_true_jedi=30000, free_play_true_jedi= 45000, extra=               Extra.SCORE_X2, levels=[Level.DEATHSTARBATTLE_INTRO1, Level.DEATHSTARBATTLE_INTRO2, Level.DEATHSTARBATTLE_INTRO3, Level.DEATHSTARBATTLE_INTRO4, Level.DEATHSTARBATTLE_A, Level.DEATHSTARBATTLE_B, Level.DEATHSTARBATTLE_C, Level.DEATHSTARBATTLE_D, Level.DEATHSTARBATTLE_MIDTRO, Level.DEATHSTARBATTLE_OUTRO, Level.DEATHSTARBATTLE_STATUS])
    E4ENDING =         36, dict(episode_index= 3, area_index= 6, readable_name=           "Episode 4 Ending", flags=AreaFlag(0x0002), story_true_jedi=    0, free_play_true_jedi=     0, extra=                         None, levels=[Level.EPISODE4ENDING_A])
    E4CHARACTERBONUS = 37, dict(episode_index= 3, area_index= 7, readable_name=  "Episode 4 Character Bonus", flags=AreaFlag(0x0004), story_true_jedi=    0, free_play_true_jedi=     0, extra=                         None, levels=[Level.E4CHARACTERBONUS_A, Level.E4CHARACTERBONUS_STATUS])
    E4VEHICLEBONUS =   38, dict(episode_index= 3, area_index= 8, readable_name=    "Episode 4 Minikit Bonus", flags=AreaFlag(0x000d), story_true_jedi=    0, free_play_true_jedi=     0, extra=                         None, levels=[Level.E4VEHICLEBONUS_A, Level.E4VEHICLEBONUS_STATUS])
    HOTHBATTLE =       39, dict(episode_index= 4, area_index= 0, readable_name=                "Hoth Battle", flags=AreaFlag(0x0011), story_true_jedi=25000, free_play_true_jedi= 35000, extra=          Extra.SELF_DESTRUCT, levels=[Level.HOTHBATTLE_INTRO1, Level.HOTHBATTLE_INTRO2, Level.HOTHBATTLE_INTRO3, Level.HOTHBATTLE_INTRO4, Level.HOTHBATTLE_A, Level.HOTHBATTLE_B, Level.HOTHBATTLE_C, Level.HOTHBATTLE_D, Level.HOTHBATTLE_E, Level.HOTHBATTLE_OUTRO, Level.HOTHBATTLE_STATUS])
    HOTHESCAPE =       40, dict(episode_index= 4, area_index= 1, readable_name=      "Escape From Echo Base", flags=AreaFlag(0x0010), story_true_jedi=40000, free_play_true_jedi= 80000, extra=             Extra.FAST_BUILD, levels=[Level.HOTHESCAPE_INTRO, Level.HOTHESCAPE_A, Level.HOTHESCAPE_B, Level.HOTHESCAPE_C, Level.HOTHESCAPE_D, Level.HOTHESCAPE_OUTRO1, Level.HOTHESCAPE_OUTRO2, Level.HOTHESCAPE_STATUS])
    ASTEROIDCHASE =    41, dict(episode_index= 4, area_index= 2, readable_name=              "Falcon Flight", flags=AreaFlag(0x0291), story_true_jedi=30000, free_play_true_jedi= 48000, extra=               Extra.SCORE_X4, levels=[Level.ASTEROIDCHASE_INTRO, Level.ASTEROIDCHASE_D, Level.ASTEROIDCHASE_A, Level.ASTEROIDCHASE_B, Level.ASTEROIDCHASE_C, Level.ASTEROIDCHASE_MIDTRO, Level.ASTEROIDCHASE_OUTRO, Level.ASTEROIDCHASE_STATUS])
    DAGOBAH =          42, dict(episode_index= 4, area_index= 3, readable_name=                    "Dagobah", flags=AreaFlag(0x0010), story_true_jedi=52000, free_play_true_jedi= 72000, extra=      Extra.REGENERATE_HEARTS, levels=[Level.DAGOBAH_INTRO, Level.DAGOBAH_A, Level.DAGOBAH_B, Level.DAGOBAH_C, Level.DAGOBAH_D, Level.DAGOBAH_E, Level.DAGOBAH_OUTRO2, Level.DAGOBAH_STATUS])
    CLOUDCITYTRAP =    43, dict(episode_index= 4, area_index= 4, readable_name=            "Cloud City Trap", flags=AreaFlag(0x0010), story_true_jedi=14000, free_play_true_jedi= 22000, extra=               Extra.SCORE_X6, levels=[Level.CLOUDCITYTRAP_INTRO, Level.CLOUDCITYTRAP_A, Level.CLOUDCITYTRAP_B, Level.CLOUDCITYTRAP_C, Level.CLOUDCITYTRAP_OUTRO, Level.CLOUDCITYTRAP_STATUS])
    CLOUDCITYESCAPE =  44, dict(episode_index= 4, area_index= 5, readable_name=       "Betrayal Over Bespin", flags=AreaFlag(0x0010), story_true_jedi=34000, free_play_true_jedi= 60000, extra=       Extra.MINIKIT_DETECTOR, levels=[Level.CLOUDCITYESCAPE_INTRO1, Level.CLOUDCITYESCAPE_INTRO2, Level.CLOUDCITYESCAPE_A, Level.CLOUDCITYESCAPE_B, Level.CLOUDCITYESCAPE_C, Level.CLOUDCITYESCAPE_OUTRO, Level.CLOUDCITYESCAPE_STATUS])
    E5ENDING =         45, dict(episode_index= 4, area_index= 6, readable_name=           "Episode 5 Ending", flags=AreaFlag(0x0002), story_true_jedi=    0, free_play_true_jedi=     0, extra=                         None, levels=[Level.EPISODE5ENDING_A])
    E5CHARACTERBONUS = 46, dict(episode_index= 4, area_index= 7, readable_name=  "Episode 5 Character Bonus", flags=AreaFlag(0x0004), story_true_jedi=    0, free_play_true_jedi=     0, extra=                         None, levels=[Level.E5CHARACTERBONUS_A, Level.E5CHARACTERBONUS_STATUS])
    E5VEHICLEBONUS =   47, dict(episode_index= 4, area_index= 8, readable_name=    "Episode 5 Minikit Bonus", flags=AreaFlag(0x000d), story_true_jedi=    0, free_play_true_jedi=     0, extra=                         None, levels=[Level.E5VEHICLEBONUS_A, Level.E5VEHICLEBONUS_STATUS])
    JABBASPALACE =     48, dict(episode_index= 5, area_index= 0, readable_name=             "Jabba's Palace", flags=AreaFlag(0x0010), story_true_jedi=43000, free_play_true_jedi= 60000, extra=           Extra.SUPER_ZAPPER, levels=[Level.JABBASPALACE_INTRO1, Level.JABBASPALACE_INTRO2, Level.JABBASPALACE_A, Level.JABBASPALACE_B, Level.JABBASPALACE_D, Level.JABBASPALACE_E, Level.JABBASPALACE_MIDTRO2, Level.JABBASPALACE_OUTRO, Level.JABBASPALACE_STATUS])
    SARLACCPIT =       49, dict(episode_index= 5, area_index= 1, readable_name=   "The Great Pit Of Carkoon", flags=AreaFlag(0x0010), story_true_jedi=50000, free_play_true_jedi= 65000, extra=  Extra.BOUNTY_HUNTER_ROCKETS, levels=[Level.SARLACCPIT_INTRO, Level.SARLACCPIT_A, Level.SARLACCPIT_B, Level.SARLACCPIT_C, Level.SARLACCPIT_OUTRO, Level.SARLACCPIT_STATUS])
    SPEEDERCHASE =     50, dict(episode_index= 5, area_index= 2, readable_name=           "Speeder Showdown", flags=AreaFlag(0x0018), story_true_jedi=55000, free_play_true_jedi= 70000, extra=               Extra.SCORE_X8, levels=[Level.SPEEDERCHASE_A, Level.SPEEDERCHASE_STATUS])
    ENDORBATTLE =      51, dict(episode_index= 5, area_index= 3, readable_name=        "The Battle Of Endor", flags=AreaFlag(0x0010), story_true_jedi=90000, free_play_true_jedi=110000, extra=    Extra.SUPER_EWOK_CATAPULT, levels=[Level.ENDORBATTLE_INTRO, Level.ENDORBATTLE_A, Level.ENDORBATTLE_B, Level.ENDORBATTLE_C, Level.ENDORBATTLE_D, Level.ENDORBATTLE_OUTRO, Level.ENDORBATTLE_STATUS])
    EMPERORFIGHT =     52, dict(episode_index= 5, area_index= 4, readable_name=               "Jedi Destiny", flags=AreaFlag(0x0010), story_true_jedi=35000, free_play_true_jedi= 80000, extra=              Extra.SCORE_X10, levels=[Level.EMPERORFIGHT_INTRO, Level.EMPERORFIGHT_A, Level.EMPERORFIGHT_B, Level.EMPERORFIGHT_STATUS])
    DEATHSTAR2BATTLE = 53, dict(episode_index= 5, area_index= 5, readable_name=        "Into The Death Star", flags=AreaFlag(0x0291), story_true_jedi=35000, free_play_true_jedi= 40000, extra=      Extra.INFINITE_TORPEDOS, levels=[Level.DEATHSTAR2BATTLE_INTRO, Level.DEATHSTAR2BATTLE_A, Level.DEATHSTAR2BATTLE_B, Level.DEATHSTAR2BATTLE_C, Level.DEATHSTAR2BATTLE_D, Level.DEATHSTAR2BATTLE_E, Level.DEATHSTAR2BATTLE_F, Level.DEATHSTAR2BATTLE_G, Level.DEATHSTAR2BATTLE_MIDTRO, Level.DEATHSTAR2BATTLE_OUTRO, Level.DEATHSTAR2BATTLE_STATUS])
    E6ENDING =         54, dict(episode_index= 5, area_index= 6, readable_name=           "Episode 6 Ending", flags=AreaFlag(0x0002), story_true_jedi=    0, free_play_true_jedi=     0, extra=                         None, levels=[Level.EPISODE6ENDING_A, Level.EPISODE6ENDING_B])
    E6CHARACTERBONUS = 55, dict(episode_index= 5, area_index= 7, readable_name=  "Episode 6 Character Bonus", flags=AreaFlag(0x0004), story_true_jedi=    0, free_play_true_jedi=     0, extra=                         None, levels=[Level.E6CHARACTERBONUS_A, Level.E6CHARACTERBONUS_STATUS])
    E6VEHICLEBONUS =   56, dict(episode_index= 5, area_index= 8, readable_name=    "Episode 6 Minikit Bonus", flags=AreaFlag(0x000d), story_true_jedi=    0, free_play_true_jedi=     0, extra=                         None, levels=[Level.E6VEHICLEBONUS_A, Level.E6VEHICLEBONUS_STATUS])
    BONUS =            57, dict(episode_index=-1, area_index=-1, readable_name=                   "New Town", flags=AreaFlag(0x010c), story_true_jedi=    0, free_play_true_jedi=     0, extra=                         None, levels=[Level.NEW_TOWN, Level.NEW_TOWN_STATUS])
    ANAKINSFLIGHT =    58, dict(episode_index=-1, area_index=-1, readable_name=            "Anakin's Flight", flags=AreaFlag(0x0281), story_true_jedi=20000, free_play_true_jedi= 30000, extra=                         None, levels=[Level.ANAKINSFLIGHT_INTRO, Level.ANAKINSFLIGHT_A, Level.ANAKINSFLIGHT_B, Level.ANAKINSFLIGHT_C, Level.ANAKINSFLIGHT_OUTRO1, Level.ANAKINSFLIGHT_OUTRO2, Level.ANAKINSFLIGHT_STATUS])
    BONUS2 =           59, dict(episode_index=-1, area_index=-1, readable_name=                  "LEGO City", flags=AreaFlag(0x010c), story_true_jedi=    0, free_play_true_jedi=     0, extra=                         None, levels=[Level.LEGO_CITY, Level.LEGO_CITY_STATUS])
    SENATE =           60, dict(episode_index=-1, area_index=-1, readable_name=                     "Senate", flags=AreaFlag(0x2804), story_true_jedi=    0, free_play_true_jedi=     0, extra=                         None, levels=[Level.SENATE_A, Level.SENATE_STATUS])
    UTAPAU =           61, dict(episode_index=-1, area_index=-1, readable_name=                     "Utapau", flags=AreaFlag(0x2804), story_true_jedi=    0, free_play_true_jedi=     0, extra=                         None, levels=[Level.UTAPAU_A, Level.UTAPAU_STATUS])
    HOTH =             62, dict(episode_index=-1, area_index=-1, readable_name=                       "Hoth", flags=AreaFlag(0x2804), story_true_jedi=    0, free_play_true_jedi=     0, extra=                         None, levels=[Level.HOTH_A, Level.HOTH_STATUS])
    NB_KAMINO =        63, dict(episode_index=-1, area_index=-1, readable_name=                     "Kamino", flags=AreaFlag(0x2804), story_true_jedi=    0, free_play_true_jedi=     0, extra=                         None, levels=[Level.NB_KAMINO_A, Level.NB_KAMINO_STATUS])
    NB_KASHYYYK =      64, dict(episode_index=-1, area_index=-1, readable_name=                   "Kashyyyk", flags=AreaFlag(0x2804), story_true_jedi=    0, free_play_true_jedi=     0, extra=                         None, levels=[Level.NB_KASHYYYK_A, Level.NB_KASHYYYK_STATUS])
    NB_DAGOBAH =       65, dict(episode_index=-1, area_index=-1, readable_name=                    "Dagobah", flags=AreaFlag(0x2804), story_true_jedi=    0, free_play_true_jedi=     0, extra=                         None, levels=[Level.NB_DAGOBAH_A, Level.NB_DAGOBAH_STATUS])
    MAP =              66, dict(episode_index=-1, area_index=-1, readable_name=                          "?", flags=AreaFlag(0x0048), story_true_jedi=    0, free_play_true_jedi=     0, extra=                         None, levels=[Level.MAP])
    LOSTTEMPLE =       67, dict(episode_index=-1, area_index=-1, readable_name=      "Indiana Jones Trailer", flags=AreaFlag(0x2c00), story_true_jedi=    0, free_play_true_jedi=     0, extra=                         None, levels=[Level.LOSTTEMPLE_A])


# Lazy imports set these when they are empty.
_AREA_TO_STORY_CHARACTERS: "dict[Area, frozenset[Character]]" = {}
_AREA_TO_PURCHASE_CHARACTERS: "dict[Area, frozenset[Character]]" = {}
_AREA_TO_EXTRA_TOGGLE_CHARACTERS: "dict[Area, frozenset[Character]]" = {}


# Explicit frozenset[Area] type hints are provided, otherwise PyCharm tries to type the sets as containing literals, and
# which messes with PyCharm's type inference when using the set for other purposes, e.g. iterating it.
BONUS_ROOM_VEHICLE_BONUSES: frozenset[Area] = frozenset({
    Area.PODRACE,
    Area.BONUS_GUNSHIP,
    Area.ANAKINSFLIGHT,
})

BONUS_ROOM_BONUSES: frozenset[Area] = BONUS_ROOM_VEHICLE_BONUSES | frozenset({
    Area.ANEWHOPE,
    Area.BONUS,
    Area.BONUS2,
    Area.LOSTTEMPLE,
})

_TWO_PLAYER_ARCADE_ARES: frozenset[Area] = frozenset({
    Area.SENATE,
    Area.UTAPAU,
    Area.HOTH,
    Area.NB_KAMINO,
    Area.NB_KASHYYYK,
    Area.NB_DAGOBAH,
})

VEHICLE_CHAPTERS: frozenset[Area] = frozenset({
    Area.PODSPRINT,
    Area.PURSUIT,
    Area.GUNSHIP,
    Area.DOGFIGHT,
    Area.DEATHSTARBATTLE,
    Area.HOTHBATTLE,
    Area.ASTEROIDCHASE,
    Area.DEATHSTAR2BATTLE,
})

ALL_CHAPTER_AREAS: frozenset[Area] = frozenset({area for area in Area if area.is_chapter()})
assert VEHICLE_CHAPTERS < ALL_CHAPTER_AREAS


POWER_BRICK_EXTRAS: frozenset[Extra] = frozenset({
    area.extra for area in Area if area.extra is not None
})
NON_POWER_BRICK_EXTRAS: frozenset[Extra] = frozenset({
    extra for extra in Extra if extra not in POWER_BRICK_EXTRAS
})
PURCHASABLE_NON_POWER_BRICK_EXTRAS: frozenset[Extra] = frozenset({
    extra for extra in NON_POWER_BRICK_EXTRAS if extra.purchase_cost is not None
})
EXTRA_TO_AREA: dict[Extra, Area] = {
    **{a.extra: a for a in Area if a.extra is not None},
    **{extra: Area.MAP for extra in PURCHASABLE_NON_POWER_BRICK_EXTRAS},
}


def make_episode_area_lookup() -> dict[int, dict[int, Area]]:
    lookup: dict[int, dict[int, Area]] = {}
    for area in Area:
        if area.episode_index == -1:
            continue
        lookup.setdefault(area.episode_index + 1, {})[area.area_index + 1] = area
    return lookup

EPISODE_AREA_LOOKUP: dict[int, dict[int, Area]] = make_episode_area_lookup()
del make_episode_area_lookup
_LEGACY_CHAPTER_SHORT_NAME_TO_AREA: dict[str, Area] = {area.get_short_name(): area for area in ALL_CHAPTER_AREAS}
