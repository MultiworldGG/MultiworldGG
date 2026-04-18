from collections import Counter
from typing import TYPE_CHECKING, Any

from Options import OptionSet, OptionCounter

from ..items import MINIKITS_BY_COUNT
from ..levels import SHORT_NAME_TO_CHAPTER_AREA, BONUS_NAME_TO_BONUS_AREA
from ..options import LegoStarWarsTCSOptions, OnlyUniqueBossesCountTowardsGoal, GoalChapterLocationsMode


if TYPE_CHECKING:
    from .. import LegoStarWarsTCSWorld
else:
    LegoStarWarsTCSWorld = object

DIRECT_SLOT_DATA_OPTIONS = (
    "minikit_goal_amount",
    "minikit_bundle_size",
    "episode_unlock_requirement",
    "all_episodes_character_purchase_requirements",
    "most_expensive_purchase_with_no_multiplier",
    "enable_bonus_locations",
    "enable_story_character_unlock_locations",
    "enable_all_episodes_purchases",
    "defeat_bosses_goal_amount",
    "only_unique_bosses_count",
    "enable_minikit_locations",
    "enable_true_jedi_locations",
    "goal_requires_kyber_bricks",
    "goal_chapter_locations_mode",
    "easier_true_jedi",
    "ridesanity",
    "enable_starting_extras_locations",
    "chapter_unlock_requirement",
    "chapter_unlock_story_characters_not_required",
)
assert all(option_name in LegoStarWarsTCSOptions.type_hints for option_name in DIRECT_SLOT_DATA_OPTIONS)


def _direct_slot_data_options(self: LegoStarWarsTCSWorld, passthrough: dict[str, Any]):
    """Options directly set from slot data."""
    options = self.options
    for option_name in DIRECT_SLOT_DATA_OPTIONS:
        # For example:
        # `options.minikit_goal_amount.value = passthrough["minikit_goal_amount"]`
        option = getattr(options, option_name)
        value = passthrough[option_name]
        # Collection values from json are always list/dict
        if isinstance(option, OptionSet):
            value = set(value)
        elif isinstance(option, OptionCounter):
            value = Counter(value)
        option.value = value


def _derived_attributes_from_options(self: LegoStarWarsTCSWorld, passthrough: dict[str, Any]):
    """Attributes normally derived from options during generate_early."""
    # Derived Chapter/Episode attributes.
    self.enabled_chapters = set(passthrough["enabled_chapters"])
    self.enabled_episodes = set(passthrough["enabled_episodes"])
    # The enabled bonuses are set depending on the number of Gold Bricks available
    self.enabled_bonuses = set(passthrough["enabled_bonuses"])
    self.starting_chapter = SHORT_NAME_TO_CHAPTER_AREA[passthrough["starting_chapter"]]
    assert self.starting_episode == passthrough["starting_episode"], ("Starting episode from slot_data did not match "
                                                                      "the starting chapter from slot_data.")

    # Derived Chapter Unlock requirements.
    self.chapters_requiring_alt_characters = set(passthrough.get("chapters_requiring_alt_characters", ()))
    self.chapter_required_character_counts = passthrough.get("chapter_required_character_counts", {})
    self.chapter_random_character_requirements = {
        chapter: [self.item_id_to_name[c] for c in characters]
        for chapter, characters in passthrough.get("chapter_random_character_requirements", {}).items()
    }

    # Derived Goal attributes.
    self.enabled_bosses = set(passthrough["enabled_bosses"])
    self.goal_area_completion_count = passthrough["goal_area_completion_count"]
    if goal_chapter := passthrough["goal_chapter"]:
        self.goal_chapter = goal_chapter
    else:
        self.goal_chapter = None

    if self.goal_chapter:
        assert self.goal_chapter in self.enabled_chapters
        self.enabled_non_goal_chapters = self.enabled_chapters - {self.goal_chapter}
        if self.options.goal_chapter_locations_mode == GoalChapterLocationsMode.option_removed:
            self.enabled_chapters_with_locations = self.enabled_chapters
        else:
            self.enabled_chapters_with_locations = self.enabled_non_goal_chapters
    else:
        self.enabled_non_goal_chapters = self.enabled_chapters

    # Derived Minikit attributes.
    if self.options.minikit_goal_amount != 0 or self.options.enable_minikit_locations:
        # 10 Minikits per chapter.
        self.available_minikits = len(self.enabled_non_goal_chapters) * 10
    else:
        # There are no minikits if the locations are not enabled and the goal does not require minikits.
        self.available_minikits = 0
    bundle_size = self.options.minikit_bundle_size.value
    self.minikit_bundle_name = MINIKITS_BY_COUNT[bundle_size].name
    self.minikit_bundle_count = (self.available_minikits // bundle_size
                                 + (self.available_minikits % bundle_size != 0))


def _override_options_with_derived_rolled_values(self: LegoStarWarsTCSWorld):
    """Override options with their derived/rolled values."""
    # Override the enable_chapter count to match the number that are enabled.
    self.options.enabled_chapters_count.value = len(self.enabled_chapters)
    # Unrandomize the starting chapter choice with the starting chapter that was actually picked.
    self.options.starting_chapter.set_from_string(self.starting_chapter.short_name)
    # Override the allowed chapters with all the chapters that rolled as enabled.
    self.options.allowed_chapters.value = set(self.enabled_chapters)
    # Act as if there was no filtering of allowed chapter types.
    self.options.allowed_chapter_types.set_from_string("all")


def _compute_boss_names(self: LegoStarWarsTCSWorld):
    """Compute boss names when unique bosses are enabled."""
    unique_bosses_only = (
            self.options.only_unique_bosses_count != OnlyUniqueBossesCountTowardsGoal.option_disabled)
    unique_bosses_anakin_as_darth_vader = (
            self.options.only_unique_bosses_count
            == OnlyUniqueBossesCountTowardsGoal.option_enabled_and_count_anakin_as_vader
    )
    if unique_bosses_only:
        short_name_to_boss_character: dict[str, str] = {}
        for chapter in self.enabled_bosses:
            boss_character = SHORT_NAME_TO_CHAPTER_AREA[chapter].boss
            if unique_bosses_anakin_as_darth_vader and boss_character == "Anakin Skywalker":
                boss_character = "Darth Vader"
            assert boss_character is not None
            short_name_to_boss_character[chapter] = boss_character
    else:
        short_name_to_boss_character = {}
    self.short_name_to_boss_character = short_name_to_boss_character


def _compute_expected_gold_brick_event_count(self: LegoStarWarsTCSWorld):
    """Compute expected Gold Brick event count."""
    if self.options.enable_bonus_locations:
        gold_bricks_per_chapter = (
                1
                + bool(self.options.enable_minikit_locations)
                + bool(self.options.enable_true_jedi_locations)
        )
        if self.goal_chapter and self.options.goal_chapter_locations_mode == GoalChapterLocationsMode.option_normal:
            chapters_with_gold_bricks = len(self.enabled_chapters)
        else:
            chapters_with_gold_bricks = len(self.enabled_non_goal_chapters)
        gold_bricks_from_chapters = chapters_with_gold_bricks * gold_bricks_per_chapter
        areas_gen = (BONUS_NAME_TO_BONUS_AREA[area_name] for area_name in self.enabled_bonuses)
        gold_bricks_from_bonuses = sum(area.gold_brick for area in areas_gen)
        self.expected_gold_brick_event_count = gold_bricks_from_chapters + gold_bricks_from_bonuses
    else:
        # Gold Brick events are only relevant when bonuses are enabled.
        self.expected_gold_brick_event_count = 0


def resolve_universal_tracker_options(self: LegoStarWarsTCSWorld, passthrough: dict[str, Any]):
    _direct_slot_data_options(self, passthrough)
    _derived_attributes_from_options(self, passthrough)
    _override_options_with_derived_rolled_values(self)
    _compute_boss_names(self)
    _compute_expected_gold_brick_event_count(self)
