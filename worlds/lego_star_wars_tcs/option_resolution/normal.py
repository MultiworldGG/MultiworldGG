from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Generic, TypeVar, Any, Mapping, Iterable

from Options import Option, OptionError

from ..items import MINIKITS_BY_COUNT
from ..levels import (
    BOSS_UNIQUE_NAME_TO_CHAPTER,
    VEHICLE_CHAPTER_SHORTNAMES,
    SHORT_NAME_TO_CHAPTER_AREA,
    BonusArea,
    BONUS_AREAS,
    BONUS_NAME_TO_BONUS_AREA,
)
from ..options import (
    LegoStarWarsTCSOptions,
    StartingChapter,
    OnlyUniqueBossesCountTowardsGoal,
    AllEpisodesCharacterPurchaseRequirements,
    AllowedChapters,
    AllowedChapterTypes,
    EpisodeUnlockRequirement,
    GoalChapterLocationsMode,
    ChapterUnlockRequirement,
    ChapterUnlockCharactersRequiredCountDistribution,
)


if TYPE_CHECKING:
    from .. import LegoStarWarsTCSWorld
else:
    LegoStarWarsTCSWorld = object


_T = TypeVar("_T")


class _OptionAdjustment(Generic[_T]):
    warning: str
    option: Option[_T]
    value: _T
    warning_args: tuple[Any, ...]

    def __init__(self, option: Option[_T], value: _T, warning: str | None = None, *warning_args):
        self.option = option
        self.value = value
        self.warning = warning
        self.warning_args = warning_args

    def run(self, world: LegoStarWarsTCSWorld):
        if self.warning:
            world.log_warning(self.warning, *self.warning_args)
        self.option.value = self.value


@dataclass
class _NormalOptionsResolver:
    world: LegoStarWarsTCSWorld

    options: LegoStarWarsTCSOptions = field(init=False)
    option_adjustments: list[_OptionAdjustment] = field(default_factory=list)
    """Adjustments (new values) to apply to self.options once option resolution is completed."""

    # Read once from options in __post_init__().
    # May be `del`-ed if their value is no longer correct, and a return value from the method that `del`-ed the
    # attribute should be used instead.
    # By `del`-ing an attribute once it is no longer correct, this prevents later parts of option resolution from using
    # stale values.
    _bosses_required_for_goal: bool = field(init=False)
    _unique_bosses_only: bool = field(init=False)
    _minikits_required_for_goal: bool = field(init=False)
    _no_vehicle_chapters_allowed: bool = field(init=False)
    _explicitly_allowed_chapters: AllowedChapters = field(init=False)
    _allowed_bosses: set[str] = field(init=False)
    _starting_chapter: StartingChapter = field(init=False)
    _allowed_chapter_types: AllowedChapterTypes = field(init=False)
    _enabled_chapters_count: int = field(init=False)
    _minikit_goal_amount: int = field(init=False)
    _enable_minikit_locations: bool = field(init=False)
    _minikit_bundle_size: int = field(init=False)
    _only_unique_bosses_count: int = field(init=False)
    _defeat_bosses_goal_amount: int = field(init=False)
    _enabled_bosses_count: int = field(init=False)
    _prefer_entire_episodes: bool = field(init=False)
    _preferred_chapters: frozenset[str] = field(init=False)
    _all_episodes_character_purchase_requirements: int = field(init=False)
    _enable_all_episodes_purchases: bool = field(init=False)
    _episode_unlock_requirement: int = field(init=False)
    _summed_filler_weights: int = field(init=False)
    _junk_weights: Mapping[str, int] = field(init=False)
    _enable_bonus_locations: bool = field(init=False)
    _enable_true_jedi_locations: bool = field(init=False)
    _kyber_bricks_required_for_goal: bool = field(init=False)
    _level_completions_required_for_goal: bool = field(init=False)
    _goal_chapter: str | None = field(init=False)
    _goal_chapter_locations_mode: GoalChapterLocationsMode = field(init=False)

    def _deferred_adjust(self, option: Option[_T], value: _T, warning: str | None = None, *warning_args):
        self.option_adjustments.append(_OptionAdjustment(option, value, warning, *warning_args))

    def __post_init__(self):
        """
        All reading from `options` occurs here, to avoid issues where one method could read an option and another method
        could modify that same option. There are no easy protections against the methods being run in the wrong order,
        so, as the number of methods grows large, it becomes unmaintainable to ensure that all modifications and reading
        of options are done in the correct order.
        """
        options = self.world.options
        self.options = options
        self._bosses_required_for_goal = options.defeat_bosses_goal_amount > 0
        self._unique_bosses_only = options.only_unique_bosses_count != OnlyUniqueBossesCountTowardsGoal.option_disabled
        # -1 uses the percentage option, which is always greater than zero.
        self._minikits_required_for_goal = options.minikit_goal_amount != 0
        self._no_vehicle_chapters_allowed = options.allowed_chapter_types == "no_vehicles"
        # "explicitly" prefix added to make it clearer that the allowed chapters for a world may be modified to include
        # allowed bosses.
        self._explicitly_allowed_chapters = AllowedChapters(options.allowed_chapters.value)
        self._allowed_bosses = options.allowed_bosses.value.copy()
        self._starting_chapter = StartingChapter(options.starting_chapter.value)
        self._allowed_chapter_types = AllowedChapterTypes(options.allowed_chapter_types.value)
        self._enabled_chapters_count = options.enabled_chapters_count.value
        self._minikit_goal_amount = options.minikit_goal_amount.value
        self._enable_minikit_locations = bool(options.enable_minikit_locations)
        self._minikit_bundle_size = options.minikit_bundle_size.value
        self._only_unique_bosses_count = options.only_unique_bosses_count.value
        self._defeat_bosses_goal_amount = options.defeat_bosses_goal_amount.value
        self._enabled_bosses_count = options.enabled_bosses_count.value
        self._prefer_entire_episodes = bool(options.prefer_entire_episodes.value)
        self._preferred_chapters = frozenset(options.preferred_chapters.value_ungrouped)
        self._all_episodes_character_purchase_requirements = options.all_episodes_character_purchase_requirements.value
        self._enable_all_episodes_purchases = bool(options.enable_all_episodes_purchases)
        self._episode_unlock_requirement = options.episode_unlock_requirement.value
        self._summed_filler_weights = (
                options.filler_weight_characters + options.filler_weight_extras + options.filler_weight_junk
        )
        self._junk_weights = options.junk_weights.value.copy()
        self._enable_bonus_locations = bool(options.enable_bonus_locations)
        self._enable_true_jedi_locations = bool(options.enable_true_jedi_locations)
        self._kyber_bricks_required_for_goal = bool(options.goal_requires_kyber_bricks)
        self._level_completions_required_for_goal = bool(options.complete_levels_goal_amount_percentage)
        self._goal_chapter = options.goal_chapter.to_short_name()
        self._goal_chapter_locations_mode = GoalChapterLocationsMode(options.goal_chapter_locations_mode.value)

    def _validate_goal_choice(self):
        """Check that at least one goal is enabled."""
        if (not self._bosses_required_for_goal
                and not self._minikits_required_for_goal
                and not self._kyber_bricks_required_for_goal
                and not self._level_completions_required_for_goal
                and not self._goal_chapter
        ):
            self.world.option_error("At least one goal must be enabled.")

    def _resolve_allowed_chapters(self) -> tuple[set[str], set[str]]:

        # Determine all available chapters to pick from.
        allowed_chapters = self._explicitly_allowed_chapters.value_ungrouped
        allowed_boss_chapters: set[str]
        if self._bosses_required_for_goal:
            # Update allowed chapters with allowed bosses.
            allowed_boss_chapters = {BOSS_UNIQUE_NAME_TO_CHAPTER[unique_boss].short_name
                                     for unique_boss in self._allowed_bosses}
            allowed_chapters.update(allowed_boss_chapters)
        else:
            allowed_boss_chapters = set()

        # Remove vehicle chapters if vehicle chapters are not allowed.
        if self._no_vehicle_chapters_allowed:
            allowed_chapters.difference_update(VEHICLE_CHAPTER_SHORTNAMES)
            allowed_boss_chapters.difference_update(VEHICLE_CHAPTER_SHORTNAMES)
        # `allowed_boss_chapters` might no longer refer to the same chapters as self._allowed_bosses.
        del self._allowed_bosses

        if self._goal_chapter:
            # The goal chapter is special and is always picked, when enabled, and does not count towards the enabled
            # chapter count.
            allowed_chapters.discard(self._goal_chapter)
            # The goal chapter can never be a boss chapter because access to the goal chapter requires completing all
            # other goals.
            allowed_boss_chapters.discard(self._goal_chapter)

        return allowed_chapters, allowed_boss_chapters

    def _resolve_allowed_starting_chapters(self,
                                           allowed_chapters: set[str],
                                           allowed_boss_chapters: set[str],
                                           ) -> set[str]:
        world = self.world

        # Determine starting chapters to pick from.
        starting_chapters: set[str]
        starting_chapter_option = self._starting_chapter
        starting_chapters = starting_chapter_option.to_short_name_set()

        # Filter to only the chapters that are allowed to be enabled.
        allowed_starting_chapters = starting_chapters.intersection(allowed_chapters)

        if not allowed_starting_chapters:
            # Figure out what the incompatibility was and see if it can be fixed or if an OptionError needs to be
            # raised.
            if (starting_chapter_option == StartingChapter.option_random_vehicle
                    and self._allowed_chapter_types == "no_vehicles"):
                world.option_error("'random_vehicle' starting Chapter cannot be used when Allowed Chapter Types is"
                                   " set to 'no_vehicles'.")
            elif len(starting_chapters) == 1:
                # If a singular starting chapter was chosen, but not in the allowed chapters set, forcefully add it.
                # This should give a better generation experience to players intending to run fully random yamls.
                assert starting_chapter_option.is_singular_chapter()
                starting_chapter = next(iter(starting_chapters))

                # The starting chapter is not allowed to be the goal chapter.
                if starting_chapter == self._goal_chapter:
                    world.option_error("The individually chosen starting chapter '%s' is not allowed to be the same as"
                                       " the Goal Chapter.", starting_chapter)

                allowed_starting_chapters = starting_chapters.copy()
                allowed_chapters.update(allowed_starting_chapters)

                world.log_warning("The individually chosen starting chapter '%s' was not in the set of allowed"
                                  " chapters %s. '%s' has been forcefully allowed to prevent generation failure.",
                                  starting_chapter,
                                  sorted(allowed_chapters),
                                  starting_chapter)
                # Add the forced starting chapter to allowed_bosses if it was an allowed boss originally.
                if self._bosses_required_for_goal:
                    unique_boss_name = SHORT_NAME_TO_CHAPTER_AREA[starting_chapter].unique_boss_name
                    if unique_boss_name in allowed_boss_chapters:
                        allowed_boss_chapters.add(starting_chapter)
            else:
                world.option_error("None of the chosen possible starting chapters were chosen to be possible to be"
                                   " enabled."
                                   " At least one starting chapter must be allowed to be enabled."
                                   "\nPossible starting chapters:"
                                   "\n\t%s (%s)"
                                   "\nAllowed chapters:"
                                   "\n\t%s (allowed chapters) + %s (allowed boss chapters) (%s)"
                                   "\nGoal chapter (not allowed as the starting chapter):"
                                   "\n\t%s",
                                   starting_chapter_option.current_key,
                                   sorted(starting_chapters),
                                   sorted(self._explicitly_allowed_chapters.value),
                                   sorted(allowed_boss_chapters),
                                   sorted(allowed_chapters),
                                   self._goal_chapter)

        return allowed_starting_chapters

    @staticmethod
    def _assert_allowed_chapters(allowed_chapters: set[str]) -> None:
        assert len(allowed_chapters) >= 1

    def _validate_allowed_boss_chapters(self, allowed_boss_chapters: set[str]) -> None:
        if self._bosses_required_for_goal and not allowed_boss_chapters:
            self.world.option_error("Defeating bosses is required for the goal, but no boss chapters were allowed to"
                                    " be enabled.")

    def _adjust_enabled_non_goal_chapters_count(self, allowed_chapters: set[str]) -> int:
        """
        Adjust the count of non-goal enabled chapters and warn if it was higher than the number of allowed chapters.

        :return: The count of enabled chapters, after adjustments.
        """
        enabled_non_goal_chapters_count = self._enabled_chapters_count
        if enabled_non_goal_chapters_count > len(allowed_chapters):
            self._deferred_adjust(self.options.enabled_chapters_count, len(allowed_chapters),
                                  "Enabled chapter count (%i) was set higher than the number of allowed"
                                  " chapters (%i), it has been reduced to the number of allowed chapters (%i).",
                                  enabled_non_goal_chapters_count,
                                  len(allowed_chapters),
                                  len(allowed_chapters))
            enabled_non_goal_chapters_count = len(allowed_chapters)
        elif enabled_non_goal_chapters_count == 36 and self._goal_chapter:
            # The Goal Chapter is enabled separately. There isn't really a need to warn for this.
            self._deferred_adjust(self.options.enabled_chapters_count, 35)
        del self._enabled_chapters_count

        return enabled_non_goal_chapters_count

    def _adjust_minikit_bundle_size(self) -> int:
        """
        If the Minikits goal is enabled, but Minikit locations are disabled, force Minikit bundle size to 10.

        :return: The adjusted Minikit Bundle Size
        """
        # -1 is the "use_percentage" value, which is always non-zero
        if (self._minikit_goal_amount != 0
                and not self._enable_minikit_locations
                and self._minikit_bundle_size != 10):
            bundle_size = 10
            self._deferred_adjust(self.options.minikit_bundle_size, bundle_size,
                                  f"The Minikits goal is enabled, but Minikit locations are disabled, so the Minikit"
                                  f" Bundle size has been forcefully set to {bundle_size}, otherwise there would not be"
                                  f" enough locations to place all the Minikits")
        else:
            bundle_size = self._minikit_bundle_size
        del self._minikit_bundle_size
        return bundle_size

    def _resolve_unique_allowed_boss_characters(self,
                                                allowed_starting_chapters: set[str],
                                                allowed_boss_chapters: set[str],
                                                enabled_chapters_count: int,
                                                ) -> tuple[int, int, dict[str, str]]:
        """
        Determine unique allowed boss characters.
        """
        maximum_boss_chapters = len(allowed_boss_chapters)
        unique_allowed_boss_characters: set[str] = set()
        unique_bosses_anakin_as_darth_vader = (
                self._only_unique_bosses_count
                == OnlyUniqueBossesCountTowardsGoal.option_enabled_and_count_anakin_as_vader
        )
        if self._unique_bosses_only:
            short_name_to_boss_character: dict[str, str] = {}
            for chapter in allowed_boss_chapters:
                boss_character = SHORT_NAME_TO_CHAPTER_AREA[chapter].boss
                if unique_bosses_anakin_as_darth_vader and boss_character == "Anakin Skywalker":
                    boss_character = "Darth Vader"
                assert boss_character is not None
                unique_allowed_boss_characters.add(boss_character)
                short_name_to_boss_character[chapter] = boss_character
            maximum_unique_boss_characters = len(unique_allowed_boss_characters)
            # The number of unique allowed boss characters is always less than or equal to the number of allowed
            # boss chapters because there can be chapters that have the same boss character.
            assert maximum_unique_boss_characters <= maximum_boss_chapters
        else:
            maximum_unique_boss_characters = -1
            short_name_to_boss_character = {}

        # If the starting chapter cannot be a boss chapter, then the maximum possible number of bosses is 1 fewer.
        starting_chapter_cannot_be_a_boss = allowed_starting_chapters.isdisjoint(allowed_boss_chapters)
        if starting_chapter_cannot_be_a_boss:
            maximum_boss_chapters = min(enabled_chapters_count - 1, maximum_boss_chapters)
        else:
            maximum_boss_chapters = min(enabled_chapters_count, maximum_boss_chapters)

        # Update the maximum unique bosses count.
        maximum_unique_boss_characters = min(maximum_unique_boss_characters, maximum_boss_chapters)

        if self._unique_bosses_only:
            maximum_bosses_for_goal = maximum_unique_boss_characters
        else:
            maximum_bosses_for_goal = maximum_boss_chapters

        return maximum_bosses_for_goal, maximum_boss_chapters, short_name_to_boss_character

    def _adjust_boss_goal_count(self,
                                maximum_bosses_for_goal: int,
                                maximum_boss_chapters: int,
                                enabled_chapters_count: int) -> tuple[int, int]:
        """
        Reduce boss goal count if it is too high. Error in the case of the boss goal not being possible to keep enabled.

        :return: The adjusted boss goal count and the adjusted enabled boss count.
        """
        if self._defeat_bosses_goal_amount > maximum_bosses_for_goal:
            if maximum_boss_chapters == 0:
                assert enabled_chapters_count == 1
                self.world.option_error("Only one Chapter is enabled, but none of the allowed starting chapters were"
                                        " also an allowed boss, and the goal requires defeating bosses.")
            else:
                self._deferred_adjust(self.options.defeat_bosses_goal_amount, maximum_bosses_for_goal,
                                      "The number of bosses to defeat as part of the goal was %i, but the maximum"
                                      " number of bosses that were allowed to be enabled was %i. The number of bosses"
                                      " to defeat as part of the goal has been reduced to %i.",
                                      self._defeat_bosses_goal_amount,
                                      maximum_bosses_for_goal,
                                      maximum_bosses_for_goal)
                goal_boss_count = maximum_bosses_for_goal
        else:
            goal_boss_count = self._defeat_bosses_goal_amount
        del self._defeat_bosses_goal_amount

        # Warn and increase the enabled bosses count if it is lower than the goal amount.
        if self._enabled_bosses_count < goal_boss_count:
            self._deferred_adjust(self.options.enabled_bosses_count, goal_boss_count,
                                  "The number of enabled bosses was %i, but the number of bosses to defeat as part of"
                                  " the goal was %i. The number of enabled bosses has been increased to %i.",
                                  self._enabled_bosses_count,
                                  goal_boss_count,
                                  goal_boss_count)
            enabled_bosses_count = goal_boss_count
        else:
            enabled_bosses_count = self._enabled_bosses_count
        del self._enabled_bosses_count

        # Warn and decrease the enabled bosses count if it is higher than the maximum bosses count.
        if enabled_bosses_count > maximum_boss_chapters:
            self._deferred_adjust(self.options.enabled_bosses_count, maximum_boss_chapters,
                                  "The number of enabled bosses was %i, but the maximum number of bosses that were"
                                  " allowed to be enabled was %i. The number of enabled bosses has been reduced to"
                                  " %i.",
                                  enabled_bosses_count,
                                  maximum_boss_chapters,
                                  maximum_boss_chapters)
            enabled_bosses_count = maximum_boss_chapters

        return goal_boss_count, enabled_bosses_count

    @staticmethod
    def _adjust_starting_chapters_for_boss_chapters(allowed_starting_chapters: set[str],
                                                    allowed_boss_chapters: set[str],
                                                    enabled_chapters_count: int,
                                                    enabled_boss_count: int):
        """In-place adjust `allowed_starting_chapters` when all chapters must be boss chapters. """
        # If every chapter is a boss chapter, then the starting chapter must also be a boss chapter.
        if enabled_boss_count == enabled_chapters_count:
            assert not allowed_starting_chapters.isdisjoint(allowed_boss_chapters)
            allowed_starting_chapters.intersection_update(allowed_boss_chapters)

    def _pick_starting_chapter(self, allowed_starting_chapters: set[str]) -> tuple[str, int]:
        """Pick the starting chapter."""
        starting_chapter = self.world.random.choice(sorted(allowed_starting_chapters))
        starting_episode = SHORT_NAME_TO_CHAPTER_AREA[starting_chapter].episode
        return starting_chapter, starting_episode

    def _generate_early_pick_unique_enabled_bosses(self,
                                                   required_unique_boss_count: int,
                                                   required_boss_chapter_count: int,
                                                   allowed_boss_chapters: set[str],
                                                   tentative_enabled_chapters: list[str],
                                                   short_name_to_boss_character: dict[str, str],
                                                   ) -> set[str]:
        world = self.world

        # Find the currently picked boss chapters and their indices. These will be updated in-place.
        picked_boss_indices: list[int] = [i for i, chapter in enumerate(tentative_enabled_chapters)
                                          if chapter in allowed_boss_chapters]
        picked_boss_chapters: set[str] = {tentative_enabled_chapters[i] for i in picked_boss_indices}
        # Additionally find the indices for each boss character in the currently picked boss chapters.
        picked_boss_characters_to_indices: dict[str, list[int]] = {}
        for i in picked_boss_indices:
            boss_chapter = tentative_enabled_chapters[i]
            boss_character = short_name_to_boss_character[boss_chapter]
            picked_boss_characters_to_indices.setdefault(boss_character, []).append(i)

        def need_more_unique_bosses() -> bool:
            return len(picked_boss_characters_to_indices) < required_unique_boss_count

        def need_more_boss_chapters() -> bool:
            return len(picked_boss_chapters) < required_boss_chapter_count

        if need_more_unique_bosses() or need_more_boss_chapters():
            # There are too few unique bosses or boss chapters present, more need to be enabled.
            # Replace the latest picked chapters.
            # If more unique bosses are needed, replace chapters that are not unique bosses, with chapters that have new
            # unique bosses.
            # If no more unique bosses are needed, but more boss chapters are needed, replace chapters that are not
            # bosses with new unique bosses, or duplicate bosses.
            # Deterministically shuffle for deterministic randomness in pick order.
            unpicked_boss_chapters = sorted(allowed_boss_chapters.difference(tentative_enabled_chapters))
            world.random.shuffle(unpicked_boss_chapters)

            def replace_chapter_at(i: int, boss_chapter_replacement: str):
                # Replace the chapter at index `i`.
                replaced_chapter = tentative_enabled_chapters[i]
                tentative_enabled_chapters[i] = boss_chapter_replacement

                # Add the replacement boss chapter to the set of enabled boss chapters.
                assert boss_chapter_replacement not in picked_boss_chapters
                picked_boss_chapters.add(boss_chapter_replacement)

                # Remove the replacement boss chapter from the chapters that have not been picked.
                unpicked_boss_chapters.remove(replacement_boss_chapter)

                # Add the index to the chapter indices of the boss of the replacement chapter.
                boss_character_replacement = short_name_to_boss_character[boss_chapter_replacement]
                boss_character_indices = picked_boss_characters_to_indices.setdefault(boss_character_replacement, [])
                assert i not in boss_character_indices
                boss_character_indices.append(i)

                if replaced_chapter in short_name_to_boss_character:
                    # The replaced chapter was a boss, so update the sets of enabled boss chapters and unpicked boss
                    # chapters.
                    picked_boss_chapters.remove(replaced_chapter)
                    assert replaced_chapter not in unpicked_boss_chapters
                    unpicked_boss_chapters.append(replaced_chapter)

                    # Remove the index from the chapter indices of the boss of the replaced chapter.
                    replaced_boss_character = short_name_to_boss_character[replaced_chapter]
                    boss_characters_indices = picked_boss_characters_to_indices[replaced_boss_character]
                    boss_characters_indices.remove(i)
                else:
                    # The replaced chapter was not a boss, but has been replaced by a boss, so add the current index to
                    # the picked indices.
                    picked_boss_indices.append(i)

            # Find unique bosses to pick from. The order of this dict is deterministically random because it is created
            # based on the order of `unpicked_boss_chapters`.
            unpicked_boss_characters_to_pick_from: dict[str, list[str]] = {}
            for boss_chapter in unpicked_boss_chapters:
                boss_character = short_name_to_boss_character[boss_chapter]
                assert boss_character is not None
                if boss_character not in picked_boss_characters_to_indices:
                    unpicked_boss_characters_to_pick_from.setdefault(
                        boss_character, []).append(boss_chapter)
            assert ((len(unpicked_boss_characters_to_pick_from) + len(picked_boss_characters_to_indices))
                    >= required_unique_boss_count), (
                "There are fewer unique bosses available than the number of required unique bosses."
                " This should not happen.")
            assert (len(unpicked_boss_chapters) + len(picked_boss_chapters)) >= required_boss_chapter_count, (
                "There are fewer boss chapters available than the number of required boss chapters."
                " This should not happen.")
            # Replace the latest picked chapters that are not unique bosses or not bosses depending on what is needed
            # most.
            reversed_indices = reversed(range(len(tentative_enabled_chapters)))
            for i in reversed_indices:
                chapter_to_replace = tentative_enabled_chapters[i]
                chapter_at_index_is_a_boss = chapter_to_replace in short_name_to_boss_character
                boss_character_to_replace = short_name_to_boss_character.get(chapter_to_replace, None)
                chapter_at_index_is_a_duplicated_boss = (
                        boss_character_to_replace is not None
                        and len(picked_boss_characters_to_indices[boss_character_to_replace]) > 1
                )

                if self._prefer_entire_episodes:
                    # Try to replace chapters with boss chapters from the same episode where possible when the option to
                    # prefer entire episodes is enabled.
                    preferred_episode_number_str = chapter_to_replace[0]
                else:
                    preferred_episode_number_str = None

                # Replace the removed chapter with a unique boss.
                replacement_boss_chapter: str
                replacement_boss_character: str
                if need_more_unique_bosses():
                    if chapter_at_index_is_a_boss and not chapter_at_index_is_a_duplicated_boss:
                        # The chapter at `i` is already a unique boss, so replacing the chapter cannot increase the
                        # number of unique bosses.
                        continue
                    # Iterate through all remaining enabled unique bosses to try to find one in the same episode.
                    for replacement_boss_character, boss_chapters in (
                            unpicked_boss_characters_to_pick_from.items()
                    ):
                        for replacement_boss_chapter in boss_chapters:
                            if (preferred_episode_number_str is None
                                    or replacement_boss_chapter[0] == preferred_episode_number_str):
                                # Suitable replacement found, so break the inner loop.
                                break
                        else:
                            # No break, so no suitable replacement found.
                            continue
                        # Suitable replacement found, so break.
                        break
                    else:
                        # No unique boss in the same episode was found, so pick the first boss in the dict to replace
                        # it.
                        it = iter(unpicked_boss_characters_to_pick_from.items())
                        replacement_boss_character, boss_chapters = next(it)
                        replacement_boss_chapter = boss_chapters[0]
                    # Remove the replacement boss character from the dict of extra, unique boss characters to pick from.
                    # There could be additional chapters that feature this boss, but now that the boss has been picked,
                    # those additional chapters would no longer feature a unique boss.
                    del unpicked_boss_characters_to_pick_from[replacement_boss_character]
                else:
                    if chapter_at_index_is_a_boss:
                        # The chapter at `i` is already a boss chapter, so replacing the chapter cannot increase the
                        # number of bosses.
                        continue
                    for replacement_boss_chapter in unpicked_boss_chapters:
                        if (preferred_episode_number_str is None
                                or replacement_boss_chapter[0] == preferred_episode_number_str):
                            # Suitable replacement found, so break.
                            break
                    else:
                        # No suitable replacement found, so pick the first boss chapter.
                        replacement_boss_chapter = unpicked_boss_chapters[0]

                # Replace the existing chapter with the replacement boss chapter, and update each of the containers for
                # this replacement.
                replace_chapter_at(i, replacement_boss_chapter)

                if not need_more_unique_bosses() and not need_more_boss_chapters():
                    # All needed replacements have been made.
                    break
        assert not need_more_unique_bosses()
        assert not need_more_boss_chapters()

        if len(picked_boss_chapters) > required_boss_chapter_count:
            # There are too many bosses enabled, so disable some bosses while ensuring that we don't go
            # under `required_unique_boss_count`
            remaining_unique_picks = list(picked_boss_characters_to_indices.values())
            # Pick unique bosses in the order they were initially picked.
            enabled_boss_indices = {indices.pop(0) for indices
                                    in remaining_unique_picks[:required_unique_boss_count]}
            extra_boss_chapters_needed = required_boss_chapter_count - len(enabled_boss_indices)
            # Pick extra boss chapters in the order they were initially picked.
            remaining_chapter_picks = [i for i in picked_boss_indices if i not in enabled_boss_indices]
            assert len(remaining_chapter_picks) >= extra_boss_chapters_needed
            enabled_boss_indices.update(remaining_chapter_picks[:extra_boss_chapters_needed])
            picked_boss_chapters = {tentative_enabled_chapters[i] for i in enabled_boss_indices}

        assert len(picked_boss_chapters) == required_boss_chapter_count
        return picked_boss_chapters

    def _generate_early_pick_enabled_bosses(self,
                                            enabled_bosses_count: int,
                                            allowed_boss_chapters: set[str],
                                            tentative_enabled_chapters: list[str],
                                            ) -> set[str]:
        world = self.world

        picked_bosses: set[str]
        picked_boss_indices: list[int] = [i for i, chapter in enumerate(tentative_enabled_chapters)
                                          if chapter in allowed_boss_chapters]

        missing_boss_chapter_count = enabled_bosses_count - len(picked_boss_indices)
        if missing_boss_chapter_count == 0:
            # The exact required number of bosses are present, so no changes are needed.
            picked_bosses = {tentative_enabled_chapters[i] for i in picked_boss_indices}
        elif missing_boss_chapter_count < 0:
            # Too many bosses are present, so pick only as many as needed.
            # If the starting chapter is a boss, always un-pick it first because starting with a boss level
            # is less interesting, especially if there is only one required boss.
            if picked_boss_indices[0] == 0:
                picked_boss_indices = picked_boss_indices[1:]
            chosen_boss_indices = world.random.sample(picked_boss_indices, k=enabled_bosses_count)
            picked_bosses = {tentative_enabled_chapters[i] for i in chosen_boss_indices}
        else:
            # There are too few bosses, so replace the latest picked chapters, that are not bosses, with
            # chapters that have bosses.
            extra_bosses_to_pick_from = sorted(allowed_boss_chapters.difference(tentative_enabled_chapters))
            world.random.shuffle(extra_bosses_to_pick_from)
            picked_bosses = {tentative_enabled_chapters[i] for i in picked_boss_indices}
            # Remove the latest picked chapters that are not bosses.
            picked_boss_indices_set = set(picked_boss_indices)
            reversed_indices = reversed(range(len(tentative_enabled_chapters)))
            replaced_chapters = []

            assert len(extra_bosses_to_pick_from) >= missing_boss_chapter_count, (
                "The number of extra bosses to pick from was less than the missing boss count")
            for i in reversed_indices:
                if i not in picked_boss_indices_set:
                    # The chapter is not a boss, so replace it.
                    chapter_to_replace = tentative_enabled_chapters[i]
                    # Replace the removed chapter with a boss in the same episode if possible.
                    preferred_episode_number_str = chapter_to_replace[0]
                    for j, boss in enumerate(reversed(extra_bosses_to_pick_from), start=1):
                        if boss[0] == preferred_episode_number_str:
                            del extra_bosses_to_pick_from[-j]
                            picked_bosses.add(boss)
                            tentative_enabled_chapters[i] = boss
                            break
                    else:
                        # No suitable boss was found. Pick the last one in the list to replace it.
                        boss = extra_bosses_to_pick_from.pop()
                        tentative_enabled_chapters[i] = boss
                        picked_bosses.add(boss)
                    replaced_chapters.append(chapter_to_replace)
                    if len(replaced_chapters) == missing_boss_chapter_count:
                        # All needed replacements have been made.
                        break
            assert len(replaced_chapters) == missing_boss_chapter_count, (
                "The number of replaced chapters did not match the missing boss count")
        return picked_bosses

    def _pick_enabled_chapters(self,
                               allowed_chapters: set[str],
                               allowed_boss_chapters: set[str],
                               goal_boss_count: int,
                               enabled_boss_count: int,
                               short_name_to_boss_character: dict[str, str],
                               starting_chapter: str,
                               enabled_chapters_count: int,
                               ) -> tuple[set[str], set[str], set[int]]:
        """Pick enabled chapters, and therefore, enabled episodes."""
        # Sort once to ensure deterministic generation.
        non_starting_allowed_chapters = sorted(allowed_chapters - {starting_chapter})
        self.world.random.shuffle(non_starting_allowed_chapters)
        # Determine preferred chapters and then sort again to put any preferred chapters first.
        preferred_chapters = self._preferred_chapters
        if preferred_chapters:
            non_starting_allowed_chapters.sort(key=lambda chapter: -1 if chapter in preferred_chapters else 0)
        # If enabled, sort the allowed chapters into the order of the first occurrence of each episode.
        if self._prefer_entire_episodes:
            # The starting chapter is considered the first picked chapter.
            initial_pick_order = [starting_chapter, *non_starting_allowed_chapters]
            seen_episodes = 0
            episode_pick_order: dict[str, int] = {}
            for chapter in initial_pick_order:
                episode_str = chapter[0]
                if episode_str in episode_pick_order:
                    continue
                episode_pick_order[episode_str] = seen_episodes
                seen_episodes += 1
            non_starting_allowed_chapters.sort(key=lambda s: episode_pick_order[s[0]])
        # Ensure there are enough bosses enabled and randomly disable any extra bosses if there are too many.
        tentative_enabled_chapters = [
            starting_chapter,
            *non_starting_allowed_chapters[:enabled_chapters_count - 1],
        ]
        if self._bosses_required_for_goal:
            if self._unique_bosses_only:
                # The number of bosses is counted by the number of unique boss characters.
                enabled_bosses = self._generate_early_pick_unique_enabled_bosses(
                    goal_boss_count, enabled_boss_count, allowed_boss_chapters, tentative_enabled_chapters,
                    short_name_to_boss_character)
                enabled_unique_bosses = {short_name_to_boss_character[chapter] for chapter in enabled_bosses}
                assert len(enabled_unique_bosses) >= goal_boss_count
            else:
                # Each boss counts separately, even if some bosses use the same boss character.
                enabled_bosses = self._generate_early_pick_enabled_bosses(
                    enabled_boss_count, allowed_boss_chapters, tentative_enabled_chapters)
            assert len(enabled_bosses) == enabled_boss_count
            enabled_bosses = enabled_bosses
        else:
            enabled_bosses = set()

        # Finally set the enabled chapters.
        enabled_chapters_with_locations = set(tentative_enabled_chapters)

        if self._goal_chapter and self._goal_chapter_locations_mode != GoalChapterLocationsMode.option_removed:
            # The goal chapter contains locations in addition to being the goal.
            enabled_chapters_with_locations.add(self._goal_chapter)

        enabled_episodes = {SHORT_NAME_TO_CHAPTER_AREA[s].episode for s in enabled_chapters_with_locations}

        if self._goal_chapter and self._goal_chapter_locations_mode == GoalChapterLocationsMode.option_removed:
            # It is possible that the Goal Chapter could be the only chapter in its episode, so there are no locations
            # in an episode, just the goal. The episode should still be considered enabled in this case.
            enabled_episodes.add(SHORT_NAME_TO_CHAPTER_AREA[self._goal_chapter].episode)

        return enabled_bosses, enabled_chapters_with_locations, enabled_episodes

    def _adjust_all_episodes_unlock_requirement(self, enabled_episodes: set[int]) -> int:
        if (self._all_episodes_character_purchase_requirements
                == AllEpisodesCharacterPurchaseRequirements.option_episodes_unlocked):
            # Only warn if the 'All Episodes' character shop purchases are enabled.
            warn = self._enable_all_episodes_purchases
            if self._episode_unlock_requirement == EpisodeUnlockRequirement.option_open:
                tokens = AllEpisodesCharacterPurchaseRequirements.option_episodes_tokens
                option = self.options.all_episodes_character_purchase_requirements
                if warn:
                    self._deferred_adjust(option, tokens,
                                          "'All Episodes' character shop unlocks were set to require 'Episodes Tokens'"
                                          " instead of 'Episodes Unlocked' because Episode unlock requirements were set"
                                          " to 'Open'")
                else:
                    self._deferred_adjust(option, tokens)
                return tokens
            elif len(enabled_episodes) == 1:
                tokens = AllEpisodesCharacterPurchaseRequirements.option_episodes_tokens
                option = self.options.all_episodes_character_purchase_requirements
                if warn:
                    self._deferred_adjust(option, tokens,
                                          "'All Episodes' character shop unlocks were set to require 'Episodes Tokens'"
                                          " from 'Episodes Unlocked' because there is only 1 Episode enabled.")
                else:
                    self._deferred_adjust(option, tokens)
                return tokens
        return self._all_episodes_character_purchase_requirements

    def _resolve_minikit_options(self, enabled_non_goal_chapter_count: int, bundle_size: int) -> tuple[str, int, int]:
        minikit_bundle_name = MINIKITS_BY_COUNT[bundle_size].name
        # todo?: Set self.available_minikits = 0 when self.options.minikit_goal_amount.value == 0 to remove minikits
        #  from the item pool?
        if self._minikit_goal_amount != 0 or self._enable_minikit_locations:
            available_minikits = enabled_non_goal_chapter_count * 10  # 10 Minikits per chapter.
            minikit_bundle_count = available_minikits // bundle_size + (available_minikits % bundle_size != 0)
        else:
            available_minikits = 0
            minikit_bundle_count = 0

        return minikit_bundle_name, available_minikits, minikit_bundle_count

    def _adjust_minikit_goal_amount(self, available_minikits: int) -> int:
        minikit_goal_amount = self._minikit_goal_amount
        del self._minikit_goal_amount
        if minikit_goal_amount > available_minikits:
            self._deferred_adjust(self.options.minikit_goal_amount, available_minikits,
                                  "The number of minikits required to goal (%i) was higher than the number of"
                                  " available minikits (%i). The number of minikits required to goal has been reduced"
                                  " to the number of available minikits (%i).",
                                  minikit_goal_amount,
                                  available_minikits,
                                  available_minikits)
            return available_minikits
        else:
            return minikit_goal_amount

    def _sanity_check_filler_weights(self):
        """Sanity check Filler Weights options."""
        if self._summed_filler_weights == 0:
            # todo: This should warn and set filler_weight_junk to 1 instead.
            self.world.option_error("At least one Filler Weight option must be set greater than zero")

    def _adjust_junk_weights(self) -> Mapping[str, int]:
        """Sanity check Junk Weights, and force Purple Studs weight to 1 if all are zero."""
        junk_names_and_weights = dict(self._junk_weights)
        del self._junk_weights
        if sum(junk_names_and_weights.values()) == 0:
            junk_names_and_weights["Blue Stud"] = 1
            self._deferred_adjust(self.options.junk_weights, junk_names_and_weights,
                                  "All Junk Weights were zero. The Junk Weight of Blue Stud items has been set to 1.")
        return junk_names_and_weights

    def _resolve_available_bonuses_and_expected_gold_brick_counts(self,
                                                                  enabled_chapter_count: int,
                                                                  ) -> tuple[set[str], int]:
        """Calculate available Bonuses based on logically available Gold Brick counts."""
        enabled_bonuses: set[str] = set()
        expected_gold_brick_event_count: int
        if self._enable_bonus_locations:
            total_chapters_with_gold_bricks = enabled_chapter_count
            if self._goal_chapter and self._goal_chapter_locations_mode == GoalChapterLocationsMode.option_normal:
                # The Goal Chapter contributes Gold Bricks if it has non-excluded locations.
                total_chapters_with_gold_bricks += 1
            # Start with the Gold Bricks available from enabled Chapters.
            gold_bricks_per_chapter = (
                    1
                    + self._enable_minikit_locations
                    + self._enable_true_jedi_locations
            )
            available_gold_bricks_from_chapters = total_chapters_with_gold_bricks * gold_bricks_per_chapter

            # Enable Bonuses that do not require more Gold Bricks than are logically available.
            # Enabled Bonuses can also reward a Gold Brick, so those will also add +1 available Gold Brick.
            available_gold_bricks = available_gold_bricks_from_chapters
            bonuses_by_gold_brick_cost: dict[int, list[BonusArea]] = {}
            for area in BONUS_AREAS:
                bonuses_by_gold_brick_cost.setdefault(area.gold_bricks_required, []).append(area)
            # Sort by lowest cost first, and then iterate.
            for gold_brick_cost, areas in sorted(bonuses_by_gold_brick_cost.items(), key=lambda t: t[0]):
                if gold_brick_cost > available_gold_bricks:
                    # The Bonuses have been sorted by lowest Gold Brick cost first, so all remaining Bonuses will
                    # have even higher requirements that cannot be met.
                    break
                for area in areas:
                    enabled_bonuses.add(area.name)
                    if area.gold_brick:
                        available_gold_bricks += 1
            # An assertion checks that the expected count matches the count created.
            expected_gold_brick_event_count = available_gold_bricks
        else:
            # Gold Brick events are only relevant when bonuses are enabled.
            expected_gold_brick_event_count = 0

        return enabled_bonuses, expected_gold_brick_event_count

    def _resolve_goal_area_completion_count(self,
                                            enabled_non_goal_chapters: set[str],
                                            enabled_bonuses: set[str],
                                            ) -> int:
        # Calculate goal_area_completion_count when set to a non-zero percentage of available areas (chapters +
        # bonuses).
        # The option name uses "levels" as a user-facing term, but has the meaning of "areas" internally.
        complete_areas_goal_amount_percentage = self.options.complete_levels_goal_amount_percentage
        if complete_areas_goal_amount_percentage > 0:
            # The goal chapter is locked behind the area completion count, so cannot contribute itself to the goal
            # requirement.
            chapter_areas_count = len(enabled_non_goal_chapters)
            # Only bonuses that award a Gold Brick on completion count towards the goal count.
            bonus_areas_count = sum(BONUS_NAME_TO_BONUS_AREA[name].gold_brick for name in enabled_bonuses)
            available_areas_count = chapter_areas_count + bonus_areas_count
            goal_area_completion_count = max(1,
                                             round(available_areas_count * complete_areas_goal_amount_percentage / 100))

            # If the Goal Chapter is enabled and has normal locations, so has Gold Bricks, then the Gold Bricks in the
            # Goal Chapter will not be usable to access Bonus Levels that can contribute level completion towards the
            # goal.
            if (self._goal_chapter
                    and self._goal_chapter_locations_mode == GoalChapterLocationsMode.option_normal
                    and enabled_bonuses):
                gold_bricks_per_chapter = (
                        1
                        + bool(self._enable_minikit_locations)
                        + bool(self._enable_true_jedi_locations)
                )
                chapter_gold_bricks = chapter_areas_count * gold_bricks_per_chapter
                gold_brick_bonuses = [BONUS_NAME_TO_BONUS_AREA[name] for name in enabled_bonuses
                                      if BONUS_NAME_TO_BONUS_AREA[name].gold_brick]
                # Sort lower requirement bonuses first.
                gold_brick_bonuses.sort(key=lambda bonus_area: bonus_area.gold_bricks_required)
                pre_goal_gold_bricks = chapter_gold_bricks
                pre_goal_completable_bonuses = 0
                for area in gold_brick_bonuses:
                    if area.gold_bricks_required > pre_goal_gold_bricks:
                        # The bonuses were sorted on order of ascending gold brick requirements, so no other bonuses are
                        # reachable before the goal.
                        break
                    pre_goal_completable_bonuses += 1
                    pre_goal_gold_bricks += 1
                pre_goal_completable_areas = chapter_areas_count + pre_goal_completable_bonuses
                if goal_area_completion_count > pre_goal_completable_areas:
                    # It is rather rare for this to actually happen.
                    self.world.log_warning("Could not satisfy the desired %i%% (%i/%i) level completions for goal"
                                           " because %i bonus levels are only accessible after completing the goal. The"
                                           " number of level completions for the goal has been reduced to the maximum"
                                           " of %.2f%% (%i/%i)",
                                           complete_areas_goal_amount_percentage,
                                           goal_area_completion_count,
                                           available_areas_count,
                                           bonus_areas_count - pre_goal_completable_bonuses,
                                           pre_goal_completable_areas / available_areas_count * 100,
                                           pre_goal_completable_areas,
                                           available_areas_count)
                    goal_area_completion_count = pre_goal_completable_areas
            return goal_area_completion_count
        else:
            return 0

    def _resolve_vanilla_character_unlocked_chapters_requiring_alt_characters(self, enabled_chapters: set[str]):
        if self.options.chapter_unlock_requirement == ChapterUnlockRequirement.option_vanilla_characters:
            alt_character_chapters = set()
            allowed_alt_character_chapters = {chapter for chapter in enabled_chapters
                                              if chapter in self.options.chapters_that_can_require_purchase_characters}
            alt_chance = self.options.require_purchase_characters_chance.value
            if alt_chance == -1:
                alt_chances = self.options.require_purchase_characters_custom_chances.value
            else:
                alt_chances = dict.fromkeys(allowed_alt_character_chapters, alt_chance)
            # Sort before iterating to get deterministic iteration order.
            for chapter in sorted(allowed_alt_character_chapters):
                if self.world.random.randint(0, 99) < alt_chances[chapter]:
                    alt_character_chapters.add(chapter)
            self.world.chapters_requiring_alt_characters = alt_character_chapters

    def _count_based_picks(self, length: int, full_range: range, base_counts: Iterable[int]) -> list[int]:
        """
        Pick as many full sets, of `full_range` values with `base_counts` counts each, as possible, for any remainder,
        randomly sample `full_range` with `base_counts` counts.
        :param length:
        :param full_range:
        :param base_counts:
        :return: Picked values, in descending order.
        """
        total_base_counts = sum(base_counts)
        if length <= total_base_counts:
            return sorted(self.world.random.sample(full_range, k=length, counts=base_counts), reverse=True)
        else:
            # Use counts to ensure there are enough to pick from.
            count_multiplier = length // total_base_counts
            remainder = length % total_base_counts
            if remainder:
                count_multiplier += 1

            initial_picks = []
            for v, base_count in zip(full_range, base_counts):
                initial_picks.extend([v] * base_count)
            initial_picks = initial_picks * (count_multiplier - 1)

            partial_picks = self.world.random.sample(full_range, k=length - len(initial_picks), counts=base_counts)
            return sorted(initial_picks + partial_picks, reverse=True)

    def _resolve_chapter_required_character_counts(self, starting_chapter: str, enabled_chapters: set[str]):
        options = self.options
        min_required_count = options.chapter_unlock_characters_min_count.value
        max_required_count = options.chapter_unlock_characters_max_count.value

        min_extra_random_count = options.chapter_unlock_random_characters_extra_min_count.value
        max_extra_random_count = options.chapter_unlock_random_characters_extra_max_count.value
        chapter_unlock_requirement = options.chapter_unlock_requirement
        is_characters = chapter_unlock_requirement.is_characters()
        if not is_characters:
            if min_required_count > max_required_count:
                # Swap the two options, but don't warn the use because the values are not relevant to their settings.
                self._deferred_adjust(options.chapter_unlock_characters_min_count, max_required_count)
                self._deferred_adjust(options.chapter_unlock_characters_max_count, min_required_count)
            return

        if min_required_count > max_required_count:
            # Swap the min and max.
            min_required_count, max_required_count = max_required_count, min_required_count
            # Swap the options too, so that the spoiler will match.
            self._deferred_adjust(
                options.chapter_unlock_characters_min_count, min_required_count,
                "The minimum chapter_unlock_characters count was greater than the maximum, the minimum and the"
                " maximum have been swapped.")
            self._deferred_adjust(
                options.chapter_unlock_characters_max_count, max_required_count,
                "The maximum chapter_unlock_characters count was less than the minimum, the maximum and the"
                " minimum have been swapped.")

        if min_extra_random_count > max_extra_random_count:
            if chapter_unlock_requirement != ChapterUnlockRequirement.option_random_characters:
                # Swap the two options, but don't warn the use because the values are not relevant to their settings.
                self._deferred_adjust(options.chapter_unlock_random_characters_extra_min_count, max_extra_random_count)
                self._deferred_adjust(options.chapter_unlock_random_characters_extra_max_count, min_extra_random_count)
            else:
                # Swap the min and max.
                min_extra_random_count, max_extra_random_count = max_extra_random_count, min_extra_random_count
                # Swap the options too, so that the spoiler will match.
                self._deferred_adjust(
                    options.chapter_unlock_random_characters_extra_min_count, min_extra_random_count,
                    "The minimum chapter_unlock_random_characters_extra count was greater than the maximum, the"
                    " minimum and the maximum have been swapped.")
                self._deferred_adjust(
                    options.chapter_unlock_random_characters_extra_max_count, max_extra_random_count,
                    "The maximum chapter_unlock_random_characters_extra count was less than the minimum, the"
                    " maximum and the minimum have been swapped.")

        if chapter_unlock_requirement == ChapterUnlockRequirement.option_random_characters:
            # Roll for extra characters that are non-required, but still contribute to unlocking chapters, so that not
            # all chapters require all the relevant characters for that chapter.
            extra_dict = {}
            for chapter in sorted(enabled_chapters):
                extra_dict[chapter] = self.world.random.randint(min_extra_random_count, max_extra_random_count)
            self.world.chapter_extra_random_character_counts = extra_dict

        # Roll for the required count of characters per chapter.
        goal_chapter = self._goal_chapter
        non_special_chapters = sorted(c for c in enabled_chapters
                                      if c != starting_chapter and c != goal_chapter)
        if min_required_count == max_required_count:
            # All requirement counts are the same, so picking is trivial.
            per_chapter_counts = [min_required_count] * len(non_special_chapters)
        else:
            full_range = range(min_required_count, max_required_count + 1)
            distribution = self.options.chapter_unlock_characters_count_distribution.value
            if distribution == ChapterUnlockCharactersRequiredCountDistribution.option_uniform:
                # 1, 1, 1, ... etc. for each value.
                base_counts = [1] * len(full_range)
            elif distribution == ChapterUnlockCharactersRequiredCountDistribution.option_low:
                # ..., 9, 7, 5, 3, 1 etc. for each progressively smaller value.
                base_counts = range(len(full_range) * 2 - 1, 0, -2)
            elif distribution == ChapterUnlockCharactersRequiredCountDistribution.option_middle:
                # Produce [1, 3, 5, 7, 5, 3, 1], [1, 3, 5, 5, 3, 1], or similar depending on len(full_range).
                half_range_len = len(full_range) // 2
                has_middle = len(full_range) % 2 != 0
                left_base_counts = range(1, half_range_len * 2, 2)
                base_counts = list(left_base_counts)
                if has_middle:
                    base_counts.append(left_base_counts[-1] + 2 if left_base_counts else 1)
                right_base_counts = reversed(left_base_counts)
                base_counts.extend(right_base_counts)
            elif distribution == ChapterUnlockCharactersRequiredCountDistribution.option_high:
                # 1, 3, 5, 7, 9, ... etc. for each progressively larger value.
                base_counts = range(1, len(full_range) * 2, 2)
            else:
                raise ValueError(f"Unexpected distribution value {distribution}")
            per_chapter_counts = self._count_based_picks(len(non_special_chapters), full_range, base_counts)

        # Shuffle the order of the chapters, so they match with counts at random.
        self.world.random.shuffle(non_special_chapters)

        if chapter_unlock_requirement == ChapterUnlockRequirement.option_random_characters:
            # Pair each chapter with a count.
            counts_dict = dict(zip(non_special_chapters, per_chapter_counts))

            # The starting chapter always uses the smallest possible required count.
            counts_dict[starting_chapter] = min_required_count
            if goal_chapter:
                # The goal chapter always uses the largest possible required count.
                counts_dict[goal_chapter] = max_required_count

            self.world.chapter_required_character_counts = counts_dict
        elif chapter_unlock_requirement == ChapterUnlockRequirement.option_vanilla_characters:
            not_required = self.world.options.chapter_unlock_story_characters_not_required.value
            max_chapter_required_counts = {}
            for chapter in enabled_chapters:
                chapter_obj = SHORT_NAME_TO_CHAPTER_AREA[chapter]
                if chapter in self.world.chapters_requiring_alt_characters:
                    max_chapter_required_counts[chapter] = len(chapter_obj.alt_character_requirements)
                else:
                    not_required_removed = chapter_obj.character_requirements.difference(not_required)
                    max_chapter_required_counts[chapter] = len(not_required_removed)
            # Some chapters can only have 1 or 2 possible required characters, which could be lower than the lowest
            # picked counts in `per_chapter_counts`.
            # To give a better distribution, if the current lowest available count is the same as, or lower than
            # the maximum possible counts for some chapters, those chapters will get picked in preference to other
            # chapters.
            # Sort lower maximum counts first, so that if a chapter can only be locked by 1 character, it uses up
            # a suitable character count instead of using up one of the larger character counts.
            # To allow for some randomness, this is only done most of the time.
            chapters_by_max_possible_required_counts: dict[int, list[str]] = {}
            for chapter in sorted(non_special_chapters, key=max_chapter_required_counts.__getitem__):
                max_possible = max_chapter_required_counts[chapter]
                chapters_by_max_possible_required_counts.setdefault(max_possible, []).append(chapter)
            counts_dict = {}

            def get_next_lowest() -> tuple[int, list[str]]:
                return next(iter(chapters_by_max_possible_required_counts.items()))

            self.world.log_debug("Rolled chapter requirement counts:\n\t%s", list(reversed(per_chapter_counts)))

            while non_special_chapters:
                assert chapters_by_max_possible_required_counts
                assert per_chapter_counts

                smallest_available_chapter_requirement = per_chapter_counts.pop()
                # 75% chance keeps some randomness without forcing all lower maximum requirement chapters to use up
                # lower requirement count picks.
                if (self.world.random.random() < 0.75
                        and (lowest_max_pair := get_next_lowest())[0] <= smallest_available_chapter_requirement):
                    lowest_max_possible, chapters = lowest_max_pair
                    picked = chapters.pop()
                    non_special_chapters.remove(picked)
                    counts_dict[picked] = lowest_max_possible
                    if not chapters:
                        del chapters_by_max_possible_required_counts[lowest_max_possible]
                    if lowest_max_possible < smallest_available_chapter_requirement:
                        self.world.log_debug("Lowest Picked %s requiring %i/%i, reduced from desired %i/%i",
                                             picked, lowest_max_possible, lowest_max_possible,
                                             smallest_available_chapter_requirement,
                                             smallest_available_chapter_requirement)
                    else:
                        self.world.log_debug("Lowest Picked %s requiring %i/%i", picked, lowest_max_possible,
                                             smallest_available_chapter_requirement)
                else:
                    picked = non_special_chapters.pop()
                    max_possible = max_chapter_required_counts[picked]
                    chapters = chapters_by_max_possible_required_counts[max_possible]
                    chapters.remove(picked)
                    if smallest_available_chapter_requirement > max_possible:
                        self.world.log_debug("Normal Picked %s requiring %i/%i, reduced from desired %i/%i",
                                             picked, max_possible, max_possible,
                                             smallest_available_chapter_requirement,
                                             smallest_available_chapter_requirement)
                        smallest_available_chapter_requirement = max_possible
                    else:
                        self.world.log_debug("Normal Picked %s requiring %i/%i", picked,
                                             smallest_available_chapter_requirement, max_possible)
                    counts_dict[picked] = smallest_available_chapter_requirement
                    if not chapters:
                        del chapters_by_max_possible_required_counts[max_possible]

            # The starting chapter always uses the smallest possible required count.
            counts_dict[starting_chapter] = min(min_required_count, max_chapter_required_counts[starting_chapter])
            if goal_chapter:
                # The goal chapter always uses the largest possible required count.
                counts_dict[goal_chapter] = min(max_required_count, max_chapter_required_counts[goal_chapter])

            # Set the counts per chapter into the dict.
            self.world.chapter_required_character_counts = counts_dict

    def _resolve_normal_options(self):
        self._validate_goal_choice()

        allowed_chapters, allowed_boss_chapters = self._resolve_allowed_chapters()
        allowed_starting_chapters = self._resolve_allowed_starting_chapters(allowed_chapters, allowed_boss_chapters)

        self._assert_allowed_chapters(allowed_chapters)
        self._validate_allowed_boss_chapters(allowed_boss_chapters)

        enabled_non_goal_chapter_count = self._adjust_enabled_non_goal_chapters_count(allowed_chapters)

        minikit_bundle_size = self._adjust_minikit_bundle_size()

        (
            maximum_bosses_for_goal,
            maximum_boss_chapters,
            short_name_to_boss_character,
        ) = self._resolve_unique_allowed_boss_characters(
            allowed_starting_chapters, allowed_boss_chapters, enabled_non_goal_chapter_count)

        goal_boss_count, enabled_boss_count = self._adjust_boss_goal_count(
            maximum_bosses_for_goal, maximum_boss_chapters, enabled_non_goal_chapter_count)
        self._adjust_starting_chapters_for_boss_chapters(
            allowed_starting_chapters, allowed_boss_chapters, enabled_non_goal_chapter_count, enabled_boss_count)

        starting_chapter, _starting_episode = self._pick_starting_chapter(allowed_starting_chapters)
        enabled_bosses, enabled_chapters_with_locations, enabled_episodes = self._pick_enabled_chapters(
            allowed_chapters,
            allowed_boss_chapters,
            goal_boss_count,
            enabled_boss_count,
            short_name_to_boss_character,
            starting_chapter,
            enabled_non_goal_chapter_count,
        )

        enabled_chapters = enabled_chapters_with_locations
        enabled_chapters_with_locations_count = enabled_non_goal_chapter_count
        if self._goal_chapter:
            if self._goal_chapter_locations_mode == GoalChapterLocationsMode.option_removed:
                enabled_chapters = enabled_chapters_with_locations | {self._goal_chapter}
            else:
                enabled_chapters_with_locations_count += 1

        assert enabled_chapters_with_locations_count == len(enabled_chapters_with_locations)

        self._resolve_vanilla_character_unlocked_chapters_requiring_alt_characters(enabled_chapters)

        self._resolve_chapter_required_character_counts(starting_chapter, enabled_chapters)

        _all_episodes_unlock_requirement = self._adjust_all_episodes_unlock_requirement(enabled_episodes)

        minikit_bundle_name, available_minikits, minikit_bundle_count = self._resolve_minikit_options(
            enabled_non_goal_chapter_count, minikit_bundle_size)
        self._adjust_minikit_goal_amount(available_minikits)

        self._sanity_check_filler_weights()
        _junk_weights = self._adjust_junk_weights()

        (
            enabled_bonuses,
            expected_gold_brick_event_count
        ) = self._resolve_available_bonuses_and_expected_gold_brick_counts(enabled_non_goal_chapter_count)

        enabled_non_goal_chapters = enabled_chapters - {self._goal_chapter}
        goal_area_completion_count = self._resolve_goal_area_completion_count(
            enabled_non_goal_chapters, enabled_bonuses)

        world = self.world
        world.short_name_to_boss_character = short_name_to_boss_character
        world.starting_chapter = SHORT_NAME_TO_CHAPTER_AREA[starting_chapter]
        world.enabled_bosses = enabled_bosses
        world.enabled_chapters = enabled_chapters
        world.enabled_episodes = enabled_episodes
        world.enabled_chapters_with_locations = enabled_chapters_with_locations
        world.enabled_non_goal_chapters = enabled_non_goal_chapters
        world.minikit_bundle_name = minikit_bundle_name
        world.available_minikits = available_minikits
        world.minikit_bundle_count = minikit_bundle_count
        world.enabled_bonuses = enabled_bonuses
        world.expected_gold_brick_event_count = expected_gold_brick_event_count
        world.goal_chapter = self._goal_chapter
        world.goal_area_completion_count = goal_area_completion_count

    def resolve_normal_options(self):
        try:
            self._resolve_normal_options()
        except OptionError:
            # Adjust options so that warning are printed, and then re-raise.
            for adjustment in self.option_adjustments:
                adjustment.run(self.world)
            raise
        else:
            # Adjust options that need to have their values changed, logging warnings where appropriate.
            for adjustment in self.option_adjustments:
                adjustment.run(self.world)


def resolve_normal_options(world: LegoStarWarsTCSWorld):
    _NormalOptionsResolver(world).resolve_normal_options()
