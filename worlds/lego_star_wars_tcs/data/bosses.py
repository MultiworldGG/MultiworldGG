from enum import IntEnum, auto
from typing import TypedDict, NotRequired

from .areas import Area
from .characters import Character
from .levels import Level

class DefeatMethod(IntEnum):
    KILL = auto()
    """The character is defeated by killing them, spawning parts etc."""
    COMPLETE_CHAPTER = auto()
    """No character exists, or the chapter ends as soon as the boss is defeated"""
    DESPAWN = auto()
    """The character despawns when defeated, rather than dying"""


class _BossInitializer(TypedDict):
    area: Area
    character: NotRequired[Character]
    unique_name: NotRequired[str]
    defeat_method: DefeatMethod
    level: NotRequired[Level]
    alt_boss: NotRequired[bool]
    """The level in which a boss character is killed, or despawns, upon being defeated"""


class Boss(IntEnum):
    area: Area
    character: Character | None
    unique_name: str
    defeat_method: DefeatMethod
    level: Level | None
    is_alt_boss: bool

    def __new__(cls, *args, **kwargs):
        obj = int.__new__(cls, args[0])
        obj._value_ = args[0]
        return obj

    def __init__(self, _id, boss_initializer: _BossInitializer):
        self.area = boss_initializer["area"]
        self.character = boss_initializer.get("character")
        self.defeat_method = boss_initializer["defeat_method"]
        if "unique_name" in boss_initializer:
            self.unique_name = boss_initializer["unique_name"]
        else:
            character = self.character
            if character is None:
                raise ValueError("No name or character specified.")
            self.unique_name = character.readable_name
        self.level = boss_initializer.get("level")
        if self.level is not None and self.level not in self.area.levels:
            raise ValueError(f"Level {self.level!r} is not found in area {self.area!r}")
        if self.defeat_method in (DefeatMethod.KILL, DefeatMethod.DESPAWN) and self.level is None:
            raise ValueError("A Level must be specified when the DefeatMethod is KILL or DESPAWN")
        self.is_alt_boss = boss_initializer.get("alt_boss", False)
    
    @staticmethod
    def from_area(area: Area) -> "Boss":
        return _AREA_TO_BOSS[area]

    @property
    def unique_event_name(self) -> str:
        return f"{self.unique_name} Defeated"

    DARTH_MAUL = auto(), dict(area=Area.MAUL,
                              character=Character.DARTH_MAUL,
                              defeat_method=DefeatMethod.COMPLETE_CHAPTER)
    ZAM_WESELL = auto(), dict(area=Area.PURSUIT,
                              unique_name=Character.ZAM_WESELL.readable_name,
                              character=Character.ZAMS_AIRSPEEDER,
                              defeat_method=DefeatMethod.COMPLETE_CHAPTER)
    JANGO_FETT_KAMINO = auto(), dict(area=Area.KAMINO,
                                     character=Character.JANGO_FETT,
                                     defeat_method=DefeatMethod.COMPLETE_CHAPTER)
    JANGO_FETT_JEDI = auto(), dict(area=Area.JEDI,
                                   character=Character.JANGO_FETT,
                                   defeat_method=DefeatMethod.COMPLETE_CHAPTER)
    DOOKU_DOOKU = auto(), dict(area=Area.DOOKU,
                               character=Character.COUNT_DOOKU,
                               defeat_method=DefeatMethod.COMPLETE_CHAPTER)
    DOOKU_CRUISER = auto(), dict(area=Area.CRUISER,
                                 character=Character.COUNT_DOOKU,
                                 defeat_method=DefeatMethod.KILL,
                                 level=Level.CRUISER_C)
    GRIEVOUS = auto(), dict(area=Area.GRIEVOUS,
                            character=Character.GENERAL_GRIEVOUS,
                            defeat_method=DefeatMethod.COMPLETE_CHAPTER)
    ANAKIN = auto(), dict(area=Area.VADER,
                          unique_name="Anakin Skywalker",
                          character=Character.ANAKIN_SKYWALKER_JEDI,
                          defeat_method=DefeatMethod.COMPLETE_CHAPTER)
    # Alternative version of Area.VADER where Anakin Skywalker is considered the same character as Darth Vader.
    VADER_VADER = auto(), dict(area=Area.VADER,
                               character=Character.DARTH_VADER,
                               defeat_method=DefeatMethod.COMPLETE_CHAPTER,
                               alt_boss=True)
    SPY = auto(), dict(area=Area.MOSEISLEY,
                       character=Character.IMPERIAL_SPY,
                       defeat_method=DefeatMethod.KILL,
                       level=Level.MOSEISLEY_D)
    DEATH_STAR = auto(), dict(area=Area.DEATHSTARBATTLE,
                              unique_name="Death Star",
                              defeat_method=DefeatMethod.COMPLETE_CHAPTER)
    VADER_DAGOBAH = auto(), dict(area=Area.DAGOBAH,
                                 character=Character.DARTH_VADER,
                                 defeat_method=DefeatMethod.DESPAWN,
                                 level=Level.DAGOBAH_D)
    VADER_TRAP = auto(), dict(area=Area.CLOUDCITYTRAP,
                              character=Character.DARTH_VADER,
                              defeat_method=DefeatMethod.COMPLETE_CHAPTER)
    BOBA_FETT_ESCAPE = auto(), dict(area=Area.CLOUDCITYESCAPE,
                                    character=Character.BOBA_FETT,
                                    defeat_method=DefeatMethod.DESPAWN,
                                    level=Level.CLOUDCITYESCAPE_A)
    RANCOR = auto(), dict(area=Area.JABBASPALACE,
                          character=Character.RANCOR,
                          defeat_method=DefeatMethod.COMPLETE_CHAPTER)
    BOBA_FETT_SARLACC = auto(), dict(area=Area.SARLACCPIT,
                                     character=Character.BOBA_FETT,
                                     defeat_method=DefeatMethod.KILL,
                                     level=Level.SARLACCPIT_A)
    EMPEROR = auto(), dict(area=Area.EMPERORFIGHT,
                           character=Character.THE_EMPEROR,
                           defeat_method=DefeatMethod.COMPLETE_CHAPTER)
    DEATH_STAR_2 = auto(), dict(area=Area.DEATHSTAR2BATTLE,
                                unique_name="Death Star II",
                                defeat_method=DefeatMethod.COMPLETE_CHAPTER)


assert len([boss.area for boss in Boss]) == len({boss.area for boss in Boss}) + 1,\
    "Each area can only have one boss, except Area.VADER with its Darth Vader alternative."

_AREA_TO_BOSS = {
    # VADER_VADER is an alternative to ANAKIN, so is only ever accessed manually.
    boss.area: boss for boss in Boss if boss is not boss.is_alt_boss
}
