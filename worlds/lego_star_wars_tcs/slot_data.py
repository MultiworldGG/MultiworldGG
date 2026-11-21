import dataclasses
import typing
from abc import ABC, abstractmethod
from collections import Counter
from dataclasses import dataclass, field, Field
from enum import IntFlag, verify, UNIQUE, CONTINUOUS, NAMED_FLAGS
from types import UnionType, NoneType
from typing import Any, TYPE_CHECKING, Iterable, Mapping, Union, Optional, get_origin, Self, TypeVar, cast
from typing_extensions import override

from Options import Option, Range, Toggle, T
from worlds.AutoWorld import World

from . import constants
from .data.areas import Area
from .data.characters import Character
from .options import (
    TCSDirectSlotDataOptions,
    MinikitGoalAmount,
    ChapterUnlockRequirement,
    TextColorChoice,
    EnableBonusLocations,
    EnableStoryCharacterUnlockLocations,
    EnableAllEpisodesCharacterPurchaseLocations,
    EnableMinikitLocations,
    EnableTrueJediLocations,
    Ridesanity,
    EnableNonPowerBrickExtraLocations,
    EasierTrueJedi,
    ScaleTrueJediWithScoreMultipliers,
    LegoStarWarsTCSDeathLink,
    DeathLinkStudLossScaling,
    LogicExpectNonInfiniteTorpedoesPodRacer21,
    UncapOriginalTrilogyHighJump,
    GoalRequiresKyberBricks,
    get_option_name,
)

if TYPE_CHECKING:
    from worlds.lego_star_wars_tcs import LegoStarWarsTCSWorld
else:
    LegoStarWarsTCSWorld = object


@verify(UNIQUE, CONTINUOUS, NAMED_FLAGS)
class EnabledFeature(IntFlag):
    # None is allowed for removed options and allows NONE to be implemented easier.
    option_type: type[Toggle] | None

    def __new__(cls, *args, **kwargs):
        obj = int.__new__(cls, args[0])
        obj._value_ = args[0]
        return obj

    def __init__(self, _id, option_type: type[Toggle]):
        self.option_type = option_type

    NONE = 0x0, None

    # Universal Tracker provides no access to which locations are exist in the connected slot, so we unfortunately have
    # to enabled location types into slot data.
    BONUS_LOCATIONS = 0x1, EnableBonusLocations
    STORY_CHARACTER_UNLOCK_LOCATIONS = 0x2, EnableStoryCharacterUnlockLocations
    ALL_EPISODES_CHARACTER_PURCHASE_LOCATIONS = 0x4, EnableAllEpisodesCharacterPurchaseLocations
    MINIKIT_LOCATIONS = 0x8, EnableMinikitLocations
    TRUE_JEDI_LOCATIONS = 0x10, EnableTrueJediLocations
    RIDESANITY_LOCATIONS = 0x20, Ridesanity
    NON_POWER_BRICK_EXTRA_LOCATIONS = 0x40, EnableNonPowerBrickExtraLocations

    EASIER_TRUE_JEDI = 0x80, EasierTrueJedi
    SCALE_TRUE_JEDI_WITH_SCORE_MULTIPLIERS = 0x100, ScaleTrueJediWithScoreMultipliers

    DEATH_LINK = 0x200, LegoStarWarsTCSDeathLink
    DEATH_LINK_STUD_LOSS_SCALING = 0x400, DeathLinkStudLossScaling

    LOGIC_EXPECT_2_1_TORPEDO_GATHERING = 0x800, LogicExpectNonInfiniteTorpedoesPodRacer21
    LOGIC_UNCAP_OT_HIGH_JUMP = 0x1000, UncapOriginalTrilogyHighJump

    KYBER_BRICK_GOAL = 0x2000, GoalRequiresKyberBricks

    def is_enabled(self, slot_data: "TCSSlotDataOptions") -> bool:
        return self in slot_data.enabled_optional_features.value


# If one of the options changes type in the future, make sure EnabledFeature gets updated too, by raising an
# AssertionError.
assert all(feature.option_type is None or issubclass(feature.option_type, Toggle) for feature in EnabledFeature), \
    "Non-Toggle option types in EnabledFeature are not supported."


class OptionalSlotData(ABC):
    @staticmethod
    @abstractmethod
    def is_present(world: LegoStarWarsTCSWorld) -> bool:
        ...


class CustomJsonSerialize(ABC):
    @abstractmethod
    def to_json_serializable(self) -> Any:
        ...


T_ITERABLE = TypeVar("T_ITERABLE", bound=Iterable)
T_MAPPING = TypeVar("T_MAPPING", bound=Mapping)


_MISSING = object()


class NamelessValuesOption(Option[T], ABC):
    """Helper for options that do not use name_lookup so would crash when trying to str/repr them without overriding
    get_option_name."""
    # Core AP does not allow Option subclasses without `default` set, so something needs to be set.
    default = _MISSING
    @classmethod
    def get_option_name(cls, value: T) -> str:
        return str(value)

    def __init_subclass__(cls):
        super().__init_subclass__()
        if cls.default is _MISSING:
            raise Exception(f"Option class {cls.__name__} needs default value")


class AreaOptionSet(NamelessValuesOption[set[Area]]):
    default = set()

    def __init__(self, area_ids: Iterable[int]):
        self.value = set(map(Area, area_ids))

    @classmethod
    def from_any(cls, data: Any) -> Self:
        if isinstance(data, Iterable):
            return cls(data)
        else:
            raise TypeError(f"Cannot create {cls.__name__} from {data} of type {type(data)}")


class AreaOption(NamelessValuesOption[Area]):
    default = Area.NEGOTIATIONS

    def __init__(self, area_id: int):
        self.value = Area(area_id)

    @classmethod
    def from_any(cls, data: Any) -> Self:
        if isinstance(data, int):
            return cls(data)
        else:
            raise TypeError(f"Cannot create {cls.__name__} from {data} of type {type(data)}")


class ApWorldVersion(NamelessValuesOption[tuple[int, int, int]]):
    default = (0, 0, 0)

    def __init__(self, version: tuple[int, int, int]):
        self.value = version

    @classmethod
    def from_any(cls, data: Any) -> Self:
        if isinstance(data, World) and isinstance(data, LegoStarWarsTCSWorld):
            return cls(constants.AP_WORLD_VERSION)
        major, minor, patch = data
        return cls((major, minor, patch))


class LogicVersion(Range):
    range_start = 1
    range_end = 999_999_999

    @classmethod
    def from_any(cls, data: Any) -> Self:
        if isinstance(data, World) and isinstance(data, LegoStarWarsTCSWorld):
            return cls(constants.UT_LOGIC_VERSION)
        return cast(Self, super().from_any(data))


class EnabledChapters(AreaOptionSet):
    @classmethod
    def from_any(cls, data: Any) -> Self:
        if isinstance(data, World) and isinstance(data, LegoStarWarsTCSWorld):
            return cls(data.enabled_chapters)
        return cast(Self, super().from_any(data))


class EnabledEpisodes(NamelessValuesOption[set[int]]):
    default = set()

    def __init__(self, episodes: Iterable[int]):
        self.value = set(episodes)

    @classmethod
    def from_any(cls, data: Any) -> Self:
        if isinstance(data, World) and isinstance(data, LegoStarWarsTCSWorld):
            return cls(data.enabled_episodes)
        elif isinstance(data, Iterable):
            return cls(data)
        else:
            raise TypeError(f"Cannot create EnabledEpisodes from {data} of type {type(data)}")


class EnabledBonuses(AreaOptionSet):
    @classmethod
    def from_any(cls, data: Any) -> Self:
        if isinstance(data, World) and isinstance(data, LegoStarWarsTCSWorld):
            return cls(data.enabled_bonuses)
        return cast(Self, super().from_any(data))


class StartingChapter(AreaOption):
    @classmethod
    def from_any(cls, data: Any) -> Self:
        if isinstance(data, World) and isinstance(data, LegoStarWarsTCSWorld):
            return cls(data.starting_chapter)
        return cast(Self, super().from_any(data))


class StartingEpisode(Range):
    range_start = 1
    range_end = 6

    @classmethod
    def from_any(cls, data: Any) -> Self:
        if isinstance(data, World) and isinstance(data, LegoStarWarsTCSWorld):
            return cls(data.starting_episode)
        return cast(Self, super().from_any(data))


class MinikitGoalAmountDerived(Range):
    range_start = MinikitGoalAmount.range_start
    range_end = MinikitGoalAmount.range_end

    @classmethod
    def from_any(cls, data: Any) -> Self:
        if isinstance(data, World) and isinstance(data, LegoStarWarsTCSWorld):
            return cls(data.goal_minikit_count)
        return cast(Self, super().from_any(data))


class EnabledBosses(AreaOptionSet):
    @classmethod
    def from_any(cls, data: Any) -> Self:
        if isinstance(data, World) and isinstance(data, LegoStarWarsTCSWorld):
            return cls(data.enabled_bosses)
        return cast(Self, super().from_any(data))


class EnabledOptionalFeatures(NamelessValuesOption[EnabledFeature]):
    default = EnabledFeature.NONE

    def __init__(self, flag_value: int):
        self.value = EnabledFeature(flag_value)

    @classmethod
    def from_any(cls, data: typing.Any) -> Self:
        if isinstance(data, World) and isinstance(data, LegoStarWarsTCSWorld):
            flag = EnabledFeature.NONE
            for flag_value in EnabledFeature:
                option_type = flag_value.option_type
                if option_type is None:
                    continue
                option_attribute_name = get_option_name(option_type)
                option_instance = getattr(data.options, option_attribute_name)
                assert isinstance(option_instance, Toggle)
                if option_instance:
                    flag |= flag_value
            return cls(flag)
        elif isinstance(data, int):
            return cls(data)
        else:
            raise TypeError(f"Cannot create {cls.__name__} from {data} of type {type(data)}")


class GoalAreaCompletionCount(Range):
    range_start = 0
    range_end = 36 + 6  # Chapters (36) + Bonuses (6, the Indy Trailer does not count).

    @classmethod
    def from_any(cls, data: Any) -> Self:
        if isinstance(data, World) and isinstance(data, LegoStarWarsTCSWorld):
            return cls(data.goal_area_completion_count)
        return cast(Self, super().from_any(data))


class GoalChapterArea(AreaOption, OptionalSlotData):
    default = Area.EMPERORFIGHT

    @classmethod
    def from_any(cls, data: Any) -> Self:
        if isinstance(data, World) and isinstance(data, LegoStarWarsTCSWorld):
            goal_chapter = data.goal_chapter
            assert goal_chapter is not None, "is_present should prevent being called with no goal chapter"
            return cls(goal_chapter)
        else:
            return cast(Self, super().from_any(data))

    @override
    @staticmethod
    def is_present(world: LegoStarWarsTCSWorld) -> bool:
        return world.goal_chapter is not None


class ItemColors(NamelessValuesOption[tuple[int, int, int, int, int, int, int]]):
    default = (TextColorChoice.option_white_ffffff,) * 7

    def __init__(self, colors: tuple[int, int, int, int, int, int, int]):
        self.value = colors

    @classmethod
    def from_any(cls, data: Any) -> Self:
        if isinstance(data, World) and isinstance(data, LegoStarWarsTCSWorld):
            return cls(data.options.item_colors_to_slot_data())
        (
            prog_useful,
            prog,
            useful,
            filler,
            trap,
            player,
            location,
            *_,  # Don't crash if there are extra colors included in a newer patch version.
        ) = data
        return cls((
            prog_useful,
            prog,
            useful,
            filler,
            trap,
            player,
            location,
        ))


class ChaptersRequiringAltCharacters(AreaOptionSet, OptionalSlotData):
    @classmethod
    def from_any(cls, data: Any) -> Self:
        if isinstance(data, World) and isinstance(data, LegoStarWarsTCSWorld):
            return cls(data.chapters_requiring_alt_characters)
        return cast(Self, super().from_any(data))

    @override
    @staticmethod
    def is_present(world: LegoStarWarsTCSWorld) -> bool:
        return world.options.chapter_unlock_requirement == ChapterUnlockRequirement.option_vanilla_characters


class ChapterRequiredCharacterCounts(NamelessValuesOption[Counter[Area]], OptionalSlotData, CustomJsonSerialize):
    default = Counter()

    def __init__(self, chapter_ids: Mapping[int, int]):
        self.value = Counter({Area(k): v for k, v in chapter_ids.items()})

    @classmethod
    def from_any(cls, data: Any) -> Self:
        if isinstance(data, World) and isinstance(data, LegoStarWarsTCSWorld):
            return cls(data.chapter_required_character_counts)
        elif isinstance(data, list):
            # to_json_serializable writes the key-value pairs into a list as [k1, v1, k2, v2, ...].
            it = iter(data)
            return cls(dict(zip(it, it)))
        else:
            raise TypeError(f"Cannot create ChapterRequiredCharacterCounts from {data} of type {type(data)}")

    @override
    @staticmethod
    def is_present(world: LegoStarWarsTCSWorld) -> bool:
        return world.options.chapter_unlock_requirement.is_characters()

    def to_json_serializable(self) -> Any:
        # Because keys in json must be str, and for reduced server memory usage, the pairs are iterated into a list with
        # each key immediately preceding its value.
        return [x for pair in self.value.items() for x in pair]


class ChapterRandomCharacterRequirements(NamelessValuesOption[dict[Area, list[Character]]],
                                         OptionalSlotData,
                                         CustomJsonSerialize):
    default = {}

    def __init__(self, value: dict[int, list[int]]):
        self.value = {Area(k): [Character(c) for c in v] for k, v in value.items()}

    @classmethod
    def from_any(cls, data: typing.Any) -> Self:
        if isinstance(data, World) and isinstance(data, LegoStarWarsTCSWorld):
            return cls({
                chapter: characters
                for chapter, characters in data.chapter_random_character_requirements.items()
            })
        if isinstance(data, list):
            from_list = {}
            it = iter(data)
            current_characters_value = None
            for x in it:
                # Keys are identified by being negative from inversion (^ -1).
                if x < 0:
                    # x is a key in the dict, so create a new list of values and put it into the dict.
                    current_characters_value = []
                    from_list[x ^ -1] = current_characters_value
                else:
                    # x is an element within a value in the dict, so append it to the current value.
                    assert current_characters_value is not None, \
                        "A key should always be found before the first value-element"
                    current_characters_value.append(x)
            return cls(from_list)
        raise TypeError(f"Cannot create ChapterRandomCharacterRequirements from {data} of type {type(data)}")

    @override
    @staticmethod
    def is_present(world: LegoStarWarsTCSWorld) -> bool:
        return world.options.chapter_unlock_requirement == ChapterUnlockRequirement.option_random_characters

    def to_json_serializable(self) -> list[int]:
        # Put the key-value pairs into a single list where each key is inverted to identify it. This decreases pickled
        # size, compared to a list[list[int]], but the pickled bytes tend to be less compressible, so the multidata can
        # end up slightly larger.
        # However, a single list has smaller memory requirements, so that is what is being preferred because slot data
        # is kept in memory by the AP server.
        return [x for k, v in self.value.items() for x in (k.value ^ -1, *v)]



_DIRECT_FIELD_NAMES: frozenset[str] = frozenset({field.name for field in dataclasses.fields(TCSDirectSlotDataOptions)})


@dataclass
class TCSSlotDataOptions(TCSDirectSlotDataOptions):
    apworld_version: ApWorldVersion
    enabled_chapters: EnabledChapters  # todo: make optional and deduce from chapter_required_character_counts when present
    enabled_episodes: EnabledEpisodes
    enabled_bonuses: EnabledBonuses
    starting_chapter: StartingChapter
    starting_episode: StartingEpisode
    minikit_goal_amount: MinikitGoalAmountDerived
    enabled_bosses: EnabledBosses
    goal_area_completion_count: GoalAreaCompletionCount
    item_colors: ItemColors
    enabled_optional_features: EnabledOptionalFeatures
    logic_version: LogicVersion  # = field(default_factory=lambda: LogicVersion(1), metadata=_since(1, 4, 0)) # Example
    goal_chapter: GoalChapterArea | None = field(default=None)
    chapters_requiring_alt_characters: ChaptersRequiringAltCharacters | None = field(default=None)
    # todo?: combine counts and requirements into a single option
    chapter_required_character_counts: ChapterRequiredCharacterCounts | None = field(default=None)
    chapter_random_character_requirements: ChapterRandomCharacterRequirements | None = field(default=None)

    @staticmethod
    def _get_option_type_from_hint(field_obj: Field) -> type[Option[Any]]:
        field_type = field_obj.type
        origin = get_origin(field_type)
        # At the time of writing, on Python 3.13, "X | None" produces a UnionType, but check for each origin for
        # compatibility purposes.
        if origin is UnionType or origin is Union or origin is Optional:
            non_optional_types: list[type] = []
            for arg in typing.get_args(field_type):
                if arg is NoneType:
                    continue
                non_optional_types.append(arg)
            if len(non_optional_types) != 1:
                raise Exception(f"Expected exactly one non-optional type for '{field_obj.name}', but got"
                                f" {len(non_optional_types)} ({non_optional_types}).")
            option_type = non_optional_types[0]
            if not issubclass(option_type, OptionalSlotData):
                raise Exception(f"All optional slot data options should extend OptionalSlotData, but {option_type}"
                                f" does not.")
            return option_type
        # Options use a metaclass, so the type of their type won't be `type`, but rather that metaclass.
        elif not isinstance(field_type, type) or not issubclass(field_type, Option):
            raise Exception(f"Expected an Option type for '{field_obj.name}', but got '{field_type}', a"
                            f" '{type(field_type)}'.")
        else:
            assert not issubclass(field_type, OptionalSlotData), "Required slot data should not be OptionalSlotData"
            return field_type

    def fill_slot_data(self, slot_data: dict[str, Any]) -> None:
        for field_obj in dataclasses.fields(self):
            field_name = field_obj.name
            field_option: Option[Any] | None = getattr(self, field_name)
            if field_option is None:
                # There is no option instance, so do not include anything in slot data.
                continue
            field_option: Option[Any] = getattr(self, field_name)
            if isinstance(field_option, CustomJsonSerialize):
                field_value = field_option.to_json_serializable()
            else:
                field_value = field_option.value
                if isinstance(field_value, set):
                    field_value = sorted(field_value)
            slot_data[field_name] = field_value

    @classmethod
    def from_world(cls, world: LegoStarWarsTCSWorld) -> "TCSSlotDataOptions":
        options = world.options
        constructor_kwargs: dict[str, Any] = {}
        for field_obj in dataclasses.fields(TCSSlotDataOptions):
            field_name = field_obj.name
            if field_name in _DIRECT_FIELD_NAMES:
                constructor_kwargs[field_name] = getattr(options, field_name)
            else:
                option_type: type[Option[Any]] = cls._get_option_type_from_hint(field_obj)
                if issubclass(option_type, OptionalSlotData) and not option_type.is_present(world):
                    constructor_kwargs[field_name] = None
                else:
                    option_instance = option_type.from_any(world)
                    constructor_kwargs[field_name] = option_instance
        return cls(**constructor_kwargs)

    @classmethod
    def from_slot_data(cls, slot_data: Mapping[str, Any]) -> "TCSSlotDataOptions":
        constructor_kwargs: dict[str, Any] = {}
        missing_required_fields: dict[type[Option[Any]], Field[Any]] = {}
        for field_obj in dataclasses.fields(TCSSlotDataOptions):
            field_name = field_obj.name
            if field_name in _DIRECT_FIELD_NAMES:
                option_type = field_obj.type
                assert isinstance(option_type, type)
                assert issubclass(option_type, Option), \
                    "All direct slot data fields should have a type hint that is an Option subclass"
                if field_name not in slot_data:
                    missing_required_fields[option_type] = field_obj
                    continue
                option_value = slot_data[field_name]
                assert issubclass(option_type, Option)
                option = option_type.from_any(option_value)
                constructor_kwargs[field_name] = option
            else:
                option_type: type[Option[Any]] = cls._get_option_type_from_hint(field_obj)
                if field_name not in slot_data:
                    if not issubclass(option_type, OptionalSlotData):
                        missing_required_fields[option_type] = field_obj
                    else:
                        # Use the default/default_factory.
                        pass
                    continue
                option_value = slot_data[field_name]
                option = option_type.from_any(option_value)
                constructor_kwargs[field_name] = option
        if missing_required_fields:
            if ApWorldVersion in missing_required_fields:
                raise Exception("The version of the AP World that generated this multiworld is missing from slot data.")
            ap_world_version = next(v for v in constructor_kwargs.values() if isinstance(v, ApWorldVersion))
            ap_world_version_value = ap_world_version.value
            for field_obj in missing_required_fields.values():
                metadata = field_obj.metadata
                if metadata is None or "since" not in metadata or metadata["since"] <= ap_world_version_value:
                    raise Exception(f"Missing required slot data for {field_obj.name}")
                if field_obj.default is dataclasses.MISSING and field_obj.default_factory is dataclasses.MISSING:
                    raise AssertionError(f"Missing default for {field_obj.name}")
                # The default value/default_factory will be used.
        return cls(**constructor_kwargs)

_OPTION_TYPE_TO_ATTRIBUTE: Mapping[type[Option[Any]], str] = {
    TCSSlotDataOptions._get_option_type_from_hint(f): f.name for f in dataclasses.fields(TCSSlotDataOptions)
}

def get_slot_data_name(o: type[Option[Any]]) -> str:
    return _OPTION_TYPE_TO_ATTRIBUTE[o]
