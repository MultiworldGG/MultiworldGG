import dataclasses
from typing import TYPE_CHECKING, Any, TypeVar, Generic

from Options import Option, Toggle

from ..data.areas import Area
from ..data.bosses import Boss
from ..data.characters import Character
from ..data.items.generic_items import MINIKITS_BY_BUNDLE_SIZE
from ..data.logic.gold_brick_bonuses import AREA_TO_GOLD_BRICK_BONUS
from ..options import OnlyUniqueBossesCountTowardsGoal, GoalChapterLocationsMode, get_option_name
from ..slot_data import TCSSlotDataOptions, TCSDirectSlotDataOptions, EnabledFeature

if TYPE_CHECKING:
    from .. import LegoStarWarsTCSWorld
else:
    LegoStarWarsTCSWorld = object


T = TypeVar("T")
_MISSING = object()


class UTAttribute(Generic[T]):
    """Descriptor for marking attributes as being specific to generating with Universal Tracker. Primarily used for
    tooling, and marking attributes that belong to Universal Tracker's API so require a specific attribute name.

    Unlike ``property``, also works for ClassVar attributes."""
    _default: T
    _private_name: str
    _is_class_var: bool

    # noinspection PyUnusedLocal
    def __init__(self, default: T = _MISSING, *, class_var: bool = False, ut_api: bool = False):
        """

        :param default: Default value for this attribute, set on the class itself.
        :param ut_api: Set to True to identify that the attribute is part of Universal Tracker's API, meaning that its
        name must match the API in order to function correctly. Has no runtime effect.
        """
        self._default = default
        self._is_class_var = class_var

    def __set_name__(self, owner, name):
        self._private_name = "_ut_attribute_" + name
        if self._default is not _MISSING:
            setattr(owner, self._private_name, self._default)

    def __get__(self, instance, owner=None) -> T:
        if self._is_class_var:
            return getattr(owner, self._private_name)
        else:
            return getattr(instance, self._private_name)

    def __set__(self, instance, value: T):
        setattr(instance, self._private_name, value)

    def __delete__(self, instance):
        delattr(instance, self._private_name)

    def has_default(self) -> bool:
        return self._default is not _MISSING


def _direct_slot_data_options(self: LegoStarWarsTCSWorld, slot_data: TCSSlotDataOptions):
    """Options directly set from slot data."""
    options = self.options

    # Directly exported to slot data and directly imported from slot data.
    for field in dataclasses.fields(TCSDirectSlotDataOptions):
        field_name = field.name
        world_option: Option[Any] = getattr(self.options, field_name)
        slot_data_option: Option[Any] = getattr(slot_data, field_name)
        world_option.value = slot_data_option.value

    # Exported to slot data through other means, but imported directly.
    options.minikit_goal_amount.value = slot_data.minikit_goal_amount.value


def _enabled_feature_slot_data_options(self: LegoStarWarsTCSWorld, slot_data: TCSSlotDataOptions):
    options = self.options
    enabled_features = slot_data.enabled_optional_features.value
    for feature in EnabledFeature:
        option_type = feature.option_type
        if option_type is None:
            continue
        option_attribute_name = get_option_name(option_type)
        option_instance = getattr(options, option_attribute_name)
        assert isinstance(option_instance, Toggle)
        # Strictly speaking, Toggle uses int values 0 and 1, but bool extends int with those values, so this is okay.
        option_instance.value = feature in enabled_features


def _derived_attributes_from_options(self: LegoStarWarsTCSWorld, slot_data: TCSSlotDataOptions):
    """Attributes normally derived from options during generate_early."""
    # Derived Chapter/Episode attributes.
    self.enabled_chapters = slot_data.enabled_chapters.value
    self.enabled_episodes = slot_data.enabled_episodes.value
    # The enabled bonuses are set depending on the number of Gold Bricks available
    self.enabled_bonuses = slot_data.enabled_bonuses.value
    self.starting_chapter = slot_data.starting_chapter.value
    assert self.starting_episode == slot_data.starting_episode.value, ("Starting episode from slot_data did not match "
                                                                      "the starting chapter from slot_data.")

    # Derived Chapter Unlock requirements.
    alt_characters_option = slot_data.chapters_requiring_alt_characters
    if alt_characters_option is None:
        self.chapters_requiring_alt_characters = set()
    else:
        self.chapters_requiring_alt_characters = alt_characters_option.value

    required_counts_option = slot_data.chapter_required_character_counts
    self.chapter_required_character_counts = {} if required_counts_option is None else required_counts_option.value

    random_requirements_option = slot_data.chapter_random_character_requirements
    random_requirements: dict[Area, list[Character]]
    random_requirements = {} if random_requirements_option is None else random_requirements_option.value
    self.chapter_random_character_requirements = random_requirements

    # Derived Goal attributes.
    self.enabled_bosses = slot_data.enabled_bosses.value
    self.goal_area_completion_count = slot_data.goal_area_completion_count.value

    goal_chapter_option = slot_data.goal_chapter
    if goal_chapter_option is not None:
        self.goal_chapter = goal_chapter_option.value
        assert self.goal_chapter in self.enabled_chapters
        self.enabled_non_goal_chapters = self.enabled_chapters - {self.goal_chapter}
        if self.options.goal_chapter_locations_mode == GoalChapterLocationsMode.option_removed:
            self.enabled_chapters_with_locations = self.enabled_chapters
        else:
            self.enabled_chapters_with_locations = self.enabled_non_goal_chapters
    else:
        self.goal_chapter = None
        self.enabled_non_goal_chapters = self.enabled_chapters

    # Derived Minikit attributes.
    if self.options.minikit_goal_amount != 0:
        # 10 Minikits per chapter.
        self.available_minikits = len(self.enabled_non_goal_chapters) * 10
    else:
        # There are no minikits if the goal does not require minikits.
        self.available_minikits = 0
    bundle_size = self.options.minikit_bundle_size.value
    self.minikit_bundle_name = MINIKITS_BY_BUNDLE_SIZE[bundle_size].name
    self.minikit_bundle_count = (self.available_minikits // bundle_size
                                 + (self.available_minikits % bundle_size != 0))


def _override_options_with_derived_rolled_values(self: LegoStarWarsTCSWorld):
    """Override options with their derived/rolled values."""
    # Override the enable_chapter count to match the number that are enabled.
    self.options.enabled_chapters_count.value = len(self.enabled_chapters)
    # Unrandomize the starting chapter choice with the starting chapter that was actually picked.
    self.options.starting_chapter.value = self.starting_chapter.value
    # Override the allowed chapters with all the chapters that rolled as enabled.
    self.options.allowed_chapters.value = set(map(int, self.enabled_chapters))
    # Act as if there was no filtering of allowed chapter types.
    self.options.allowed_chapter_types.set_from_string("all")


def _compute_unique_bosses(self: LegoStarWarsTCSWorld, slot_data: TCSSlotDataOptions):
    """Compute bosses when unique bosses are enabled."""
    unique_bosses_only = (
            self.options.only_unique_bosses_count != OnlyUniqueBossesCountTowardsGoal.option_disabled)
    unique_bosses_anakin_as_darth_vader = (
            self.options.only_unique_bosses_count
            == OnlyUniqueBossesCountTowardsGoal.option_enabled_and_count_anakin_as_vader
    )
    if unique_bosses_only:
        boss_area_to_boss: dict[Area, Boss] = {}
        for chapter in slot_data.enabled_bosses.value:
            boss = Boss.from_area(chapter)
            if unique_bosses_anakin_as_darth_vader and boss is Boss.ANAKIN:
                boss = Boss.VADER_VADER
            boss_area_to_boss[chapter] = boss
    else:
        boss_area_to_boss = {}
    self.boss_area_to_boss = boss_area_to_boss


def _compute_expected_gold_brick_event_count(self: LegoStarWarsTCSWorld):
    """Compute expected Gold Brick event count."""
    if self.options.enable_bonus_locations:
        gold_bricks_per_chapter = (
                1
                + bool(self.options.enable_minikit_locations)
                + bool(self.options.enable_true_jedi_locations)
        )
        if (
                self.goal_chapter is not None
                and self.options.goal_chapter_locations_mode == GoalChapterLocationsMode.option_normal
        ):
            chapters_with_gold_bricks = len(self.enabled_chapters)
        else:
            chapters_with_gold_bricks = len(self.enabled_non_goal_chapters)
        gold_bricks_from_chapters = chapters_with_gold_bricks * gold_bricks_per_chapter
        bonus_areas_gen = (AREA_TO_GOLD_BRICK_BONUS[area] for area in self.enabled_bonuses)
        gold_bricks_from_bonuses = sum(bonus_area.rewards_gold_brick for bonus_area in bonus_areas_gen)
        self.expected_gold_brick_event_count = gold_bricks_from_chapters + gold_bricks_from_bonuses
    else:
        # Gold Brick events are only relevant when bonuses are enabled.
        self.expected_gold_brick_event_count = 0


def resolve_universal_tracker_options(self: LegoStarWarsTCSWorld, passthrough: dict[str, Any]):
    slot_data_options = TCSSlotDataOptions.from_slot_data(passthrough)
    _direct_slot_data_options(self, slot_data_options)
    _enabled_feature_slot_data_options(self, slot_data_options)
    _derived_attributes_from_options(self, slot_data_options)
    _override_options_with_derived_rolled_values(self)
    _compute_unique_bosses(self, slot_data_options)
    _compute_expected_gold_brick_event_count(self)
