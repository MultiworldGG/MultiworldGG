from collections import Counter
from dataclasses import dataclass
from functools import reduce
from operator import or_
from typing import TYPE_CHECKING, Iterable

from BaseClasses import LocationProgressType, ItemClassification

from .constants import (
    progression_deprioritized_skip_balancing,
    CharacterAbility,
    CHAPTER_SPECIFIC_FLAGS,
    RARE_AND_USEFUL_ABILITIES,
)
from .items import (
    CHARACTERS_AND_VEHICLES_BY_NAME,
    GenericCharacterData,
    LegoStarWarsTCSItem,
    EXTRAS_BY_NAME,
    PURCHASABLE_NON_POWER_BRICK_EXTRAS,
    GENERIC_BY_NAME,
)
from .levels import (
    CHAPTER_AREA_STORY_CHARACTERS,
    VEHICLE_CHAPTER_SHORTNAMES,
    POWER_BRICK_REQUIREMENTS,
    SHORT_NAME_TO_CHAPTER_AREA,
    BONUS_NAME_TO_BONUS_AREA,
    DIFFICULT_OR_IMPOSSIBLE_TRUE_JEDI,
)
from .locations import LegoStarWarsTCSShopLocation
from .options import ChapterUnlockRequirement, GoalChapterLocationsMode


if TYPE_CHECKING:
    from . import LegoStarWarsTCSWorld
else:
    LegoStarWarsTCSWorld = object


progressive_score_multiplier_name = GENERIC_BY_NAME["Progressive Score Multiplier"].name


__all__ = [
    "create_item_pool"
]

# Always pick CAN_ abilities last to avoid picking very boring characters at the start with basically no
# actual abilities.
# Always pick VEHICLE_BLASTER last to avoid picking a VEHICLE_BLASTER, and then picking a VEHICLE_TOW that
# also has VEHICLE_BLASTER.
ABILITY_PICK_ORDER = {
    **dict.fromkeys(~CharacterAbility.NONE, 0),
    CharacterAbility.CAN_ATTACK_UP_CLOSE: 1,
    CharacterAbility.CAN_RIDE_VEHICLES: 1,
    CharacterAbility.CAN_JUMP_NORMALLY: 1,
    CharacterAbility.CAN_PULL_LEVERS: 1,
    CharacterAbility.CAN_PUSH_OBJECTS: 1,
    CharacterAbility.CAN_BUILD_BRICKS: 1,
    CharacterAbility.VEHICLE_BLASTER: 1,
    **dict.fromkeys(CHAPTER_SPECIFIC_FLAGS, 2),
}
BASE_ABILITY_COSTS = {
    CharacterAbility.SITH: 10,
    CharacterAbility.BOUNTY_HUNTER: 10,
    CharacterAbility.ASTROMECH: 8,
    CharacterAbility.SHORTIE: 8,
    CharacterAbility.HIGH_JUMP: 8,
    CharacterAbility.HOVER: 7,
    CharacterAbility.IMPERIAL: 6,
    CharacterAbility.CAN_WEAR_HAT: 0,
    CharacterAbility.JEDI: 2,
    CharacterAbility.BLASTER: 2,
    CharacterAbility.CAN_ATTACK_UP_CLOSE: 1,
    CharacterAbility.CAN_RIDE_VEHICLES: 1,
    CharacterAbility.CAN_JUMP_NORMALLY: 1,
    CharacterAbility.CAN_PULL_LEVERS: 1,
    CharacterAbility.VEHICLE_TOW: 10,
    CharacterAbility.VEHICLE_TIE: 8,
    CharacterAbility.VEHICLE_BLASTER: 2,
    CharacterAbility.IS_A_VEHICLE: 0,
}


@dataclass
class ItemPoolAbilityRequirements:
    required: CharacterAbility
    """Abilities that are logically required to reach every location in the world. In cases where there are multiple
    options, one option will be picked as required and the others as optional."""
    optional: CharacterAbility
    """Abilities that could have logical relevance to the player getting access to locations, but all locations would
    be reachable even if no items with these abilities existed in the item pool."""
    starting: CharacterAbility = CharacterAbility.NONE
    """Abilities that the player will be starting with."""

    _updated_for_chapter_requirements: bool = False

    def get_logically_irrelevant(self) -> CharacterAbility:
        """
        Get abilities that are logically irrelevant for items in the item pool. In slots with few chapters enabled, some
        abilities may not have any logical relevance.
        :return:
        """
        # todo?: Maybe this should return ~(self.required | self.optional | self.starting) instead? With self.required
        #  no longer being mutated once abilities are provided, so that it is easier to see what abilities had to be
        #  provided by the item pool?
        return ~(self.required | self.optional)

    def update_for_starting_abilities(self, starting_abilities: CharacterAbility) -> None:
        """
        Remove abilities present on characters in the player's starting inventory.
        If an ability is provided by starting inventory, then it does not need to be provided by the item pool.
        :param starting_abilities:
        :return:
        """
        assert self._updated_for_chapter_requirements, \
            "Chapter ability requirements should have been processed before starting abilities."
        self.required &= ~starting_abilities
        self.optional &= ~starting_abilities
        self.starting = starting_abilities

    def update_for_chapter_ability_requirements(self, world: LegoStarWarsTCSWorld) -> None:
        """
        Update the ability requirements for the enabled chapters.
        :param world:
        """
        assert not self._updated_for_chapter_requirements, \
            "Already updated for chapter ability requirements, this is a bug."
        for chapter in sorted(world.enabled_chapters):
            chapter_obj = SHORT_NAME_TO_CHAPTER_AREA[chapter]
            # The item pool must provide the abilities required to complete the chapter.
            # While it is possible for characters that satisfy the alt requirements to be picked when picking characters
            # to create that are necessary to unlock a chapter, for simplicity, it is assumed that the main ability
            # requirements for every chapter must be supplied by the item pool.
            self.required |= chapter_obj.completion_main_ability_requirements
            # Alternative requirements that swap out a common ability for a rarer ability are relevant to logic, but
            # are not required to be included in the item pool.
            alt_requirements = chapter_obj.completion_alt_ability_requirements
            if alt_requirements:
                self.optional |= alt_requirements
        self._updated_for_chapter_requirements = True


class ItemCreator:
    _classification_lookup: dict[str, ItemClassification]
    _abilities_lookup: dict[str, CharacterAbility]
    _world: LegoStarWarsTCSWorld

    def __init__(self,
                 world: LegoStarWarsTCSWorld,
                 logically_irrelevant_abilities: CharacterAbility):
        """
        Create a class to help in create items in a performant manner, while stripping starting abilities from the
        created items.
        :param world: The world the created items will belong to.
        :param logically_irrelevant_abilities: Abilities that are not required at all, to be stripped from created
        items for improved generation performance.
        """
        self._world = world
        self._initialize_effective_data_lookups(logically_irrelevant_abilities)

    def _initialize_effective_data_lookups(self, logically_irrelevant_abilities: CharacterAbility) -> None:
        """
        Pre-calculate the effective character abilities and classification of each item, so that the creation of items
        with multiple copies can be sped up.
        :param logically_irrelevant_abilities: These abilities are logically irrelevant to created items, so do not need
         to be provided by created items, potentially changing the effective classifications of the items.
        """
        effective_character_abilities: dict[str, CharacterAbility] = {}

        for name, char in CHARACTERS_AND_VEHICLES_BY_NAME.items():
            # Remove abilities provided by the starting characters from other characters, potentially changing the
            # classification of other characters if all their abilities are covered by the starting characters.
            # This improves generation performance by reducing the number of extra collects when a character item is
            # collected.
            effective_abilities: CharacterAbility = char.abilities & ~logically_irrelevant_abilities
            effective_character_abilities[name] = effective_abilities

        effective_item_classifications: dict[str, ItemClassification] = {}
        effective_item_abilities: dict[str, CharacterAbility] = {}
        for item in self._world.item_name_to_id:
            classification, effective_abilities = self._world.evaluate_effective_item(item, effective_character_abilities)
            effective_item_classifications[item] = classification
            # The returned `effective_abiltiies` should be the same as what was in `effective_character_abilities`.
            # The returned `effective_abiltiies` is not actually needed here, but `effective_character_abilities` is not
            # always available when `self.evaluate_effective_item()` is called.
            assert effective_abilities is effective_character_abilities.get(item, CharacterAbility.NONE)
            effective_item_abilities[item] = effective_abilities

        self._classification_lookup = effective_item_classifications
        self._abilities_lookup = effective_item_abilities

    def create_item(self, name: str) -> LegoStarWarsTCSItem:
        """
        Create an item by name
        :param name: The name of the item. The name must exist in the world's datapackage.
        :return: The created item.
        """
        code = self._world.item_name_to_id[name]
        classification = self._classification_lookup[name]
        abilities = self._abilities_lookup[name]

        return LegoStarWarsTCSItem(name, classification, code, self._world.player, abilities)


@dataclass
class ItemLocationCounts:
    world: LegoStarWarsTCSWorld
    non_excluded_chapter_count: int
    goal_chapter_locations_excluded: bool

    free_from_completions: int = 0
    """Free spaces in the item pool from Level completion locations."""
    free_from_true_jedi: int = 0
    """Free spaces in the item pool from True Jedi locations."""
    free_from_ridesanity: int = 0
    """Free spaces in the item pool from ridesanity locations."""

    available_minikit: int = 0
    """Count of enabled locations that give a minikit in vanilla."""
    available_character: int = 0
    """Count of enabled locations that unlock a character in vanilla."""
    available_extra: int = 0
    """Count of enabled locations that unlock an Extra in vanilla."""

    required_minikit: int = 0
    """The number of Minikit bundles that are required to exist in the item pool."""
    required_character: int = 0
    """The number of Characters that are required to exist in the item pool."""
    required_extra: int = 0
    """The number of Extras that are required to exist in the item pool."""
    required_additional: int = 0
    """The number of additional items that don't belong to a particular category, that are required to exist in the 
    pool."""
    required_excludable: int = 0
    """The number of excludable items that are required to exist in the item pool."""

    reserved_non_required_character: int = 0
    """Try to add at least as many non-required characters to the item pool as this."""
    reserved_non_required_extra: int = 0
    """Try to add at least as many non-required Extras to the item pool as this."""

    def set_character_counts(self, pool_required_characters_count: int) -> None:
        self.required_character = pool_required_characters_count

        self.available_character = (
                self.world.character_unlock_location_count - self.world.goal_excluded_character_unlock_location_count
        )
        if self.world.options.filler_reserve_characters:
            characters_remaining_to_fit_in_pool = max(self.available_character, self.required_character)
            # Leftover space for characters is reserved for non-required characters.
            self.reserved_non_required_character = characters_remaining_to_fit_in_pool - self.required_character
        else:
            self.reserved_non_required_character = 0

        # Any goal excluded character unlock locations do not contribute Characters to the item pool (unless those
        # characters happen to be Filler classification). Enough Filler items for Excluded locations is checked and
        # satisfied later, so these locations are effectively free locations.
        self.available_character += self.world.goal_excluded_character_unlock_location_count

    def set_extra_counts(self, pool_required_extras_count: int) -> None:
        self.required_extra = pool_required_extras_count

        self.available_extra = self.non_excluded_chapter_count

        if self.world.options.enable_starting_extras_locations:
            self.available_extra += len(PURCHASABLE_NON_POWER_BRICK_EXTRAS)

        free_extra_location_count: int
        if self.world.options.filler_reserve_extras:
            extras_remaining_to_fit_in_pool = max(self.available_extra, self.required_extra)
            # Leftover space for Extras is reserved for non-required Extras.
            self.reserved_non_required_extra = extras_remaining_to_fit_in_pool - self.required_extra
        else:
            self.reserved_non_required_extra = 0

        if self.goal_chapter_locations_excluded:
            # The Extra location of the Goal Chapter is excluded, and does not contribute an Extra to the item pool.
            self.available_extra += 1

    def set_true_jedi_counts(self) -> None:
        # The vanilla rewards for True Jedi are Gold Bricks, which are events, so these are effectively free locations
        # for any kind of item when enabled.
        if self.world.options.enable_true_jedi_locations:
            self.free_from_true_jedi = self.non_excluded_chapter_count

            if self.goal_chapter_locations_excluded:
                # True Jedi locations are already free locations for any kind of item.
                self.free_from_true_jedi += 1
        else:
            self.free_from_true_jedi = 0

    def set_completion_counts(self) -> None:
        self.free_from_completions = self.non_excluded_chapter_count + len(self.world.enabled_bonuses)
        if self.goal_chapter_locations_excluded:
            # The completion location for the goal chapter is excluded, but is still a free location in the item pool
            # (space for filler needed to be placed at excluded locations is calculated separately from free locations).
            self.free_from_completions += 1

    def set_minikit_counts(self) -> None:
        # As many minikit bundles as this will always be created. This may be fewer than is required to goal, but
        # reducing the total bundle count can make a seed longer, so all minikit bundles should be considered to be
        # required.
        self.required_minikit = self.world.minikit_bundle_count

        if self.world.options.enable_minikit_locations:
            self.available_minikit = self.non_excluded_chapter_count * 10
            if self.goal_chapter_locations_excluded:
                # The locations are excluded, but still count as free locations.
                self.available_minikit += 10
        else:
            if self.world.options.minikit_goal_amount != 0:
                assert self.world.options.minikit_bundle_size == 10
                assert self.world.minikit_bundle_name == "10 Minikits"
                assert self.world.minikit_bundle_count == len(self.world.enabled_non_goal_chapters)
                self.available_minikit = 0
            else:
                assert self.required_minikit == 0
                self.available_minikit = 0

    def set_ridesanity_counts(self) -> None:
        # There are no corresponding items for ridesanity locations, so they are free locations for any item.
        self.free_from_ridesanity = self.world.ridesanity_location_count

    def set_additional_item_counts(self, additional_required_items_count: int) -> None:
        self.required_additional += additional_required_items_count

    def _free_space_from_non_required(self, needed: int) -> tuple[bool, int]:
        """

        :param needed: How many free spaces should be
        :return: True and the total reserved spaces consumed, or False and how many free spaces were missing.
        """
        # Subtract from reserved, but not required, counts.
        ok_to_replace_character_count = self.reserved_non_required_character
        ok_to_replace_extras_count = self.reserved_non_required_extra
        total_replaceable = ok_to_replace_character_count + ok_to_replace_extras_count
        if needed > total_replaceable:
            return False, needed - total_replaceable
        else:
            character_percentage = ok_to_replace_character_count / total_replaceable
            character_subtract = min(needed, round(character_percentage * needed))
            extra_subtract = needed - character_subtract
            self.reserved_non_required_character -= character_subtract
            self.reserved_non_required_extra -= extra_subtract
            assert (character_subtract + extra_subtract) == needed
            return True, character_subtract + extra_subtract

    def free_space_for_required_items(self):
        """
        Replace space in the item pool, reserved by non-required Extras and Characters, until there is enough space in
        the item pool for all required items.
        """
        free_location_count = self.free_location_count
        if free_location_count < 0:
            # There are not enough non-excluded locations for all required progression items.
            # Attempt to reduce reserved items until there is enough space.
            needed = -free_location_count
            ok, count = self._free_space_from_non_required(needed)
            if not ok:
                if self.world.options.goal_requires_kyber_bricks:
                    # The Kyber Bricks goal adds 7 items that have no corresponding vanilla locations.
                    self.world.option_error(
                        "There are not enough locations to fit all required items. Enable additional locations,"
                        " increase the Minikit Bundle Size, or disable the Kyber Bricks goal to free up more locations."
                        " There were %i more required progression items than non-excluded locations.",
                        count)
                else:
                    self.world.option_error(
                        "There are not enough locations to fit all required items. Enable additional locations or"
                        " increase the Minikit Bundle Size to free up more locations. There were %i more required"
                        " progression items than locations.",
                        count)
            self.world.log_warning("There was not enough space in the item pool to fit all required items and"
                                   " all reserved non-required items. %i reserved non-required items had to be"
                                   " un-reserved to fit all the required items.",
                                   count)
        assert self.free_location_count >= 0, "free_location_count must always be >= 0 after freeing required space"

    def free_space_for_excluded_locations(self) -> None:
        """
        Replace space in the item pool, reserved by non-required Extras and Characters, until there is enough free space
        in the item pool for filler to be placed on excluded locations.
        :return: The number of required excludable items.
        """
        # Ensure there is enough space in the item pool for as many filler items as there are unfilled excluded
        # locations.
        required_excludable_count = sum(loc.progress_type == LocationProgressType.EXCLUDED
                                        for loc in self.world.get_locations() if loc.item is None)
        free_location_count = self.free_location_count

        # fixme: Some reserved characters can be Filler classification, which would be fine being placed on excluded
        #  locations, so this check is currently overly strict because it assumes that reserved characters will be
        #  Useful or Progression.
        if free_location_count < required_excludable_count:
            # This shouldn't really happen unless basically the entire world is excluded and/or barely any locations
            # are enabled.
            needed = required_excludable_count - free_location_count
            ok, _count = self._free_space_from_non_required(needed)
            if not ok:
                # There are too many non-excludable items for the number of excluded locations.
                # Give up.
                # If this is too common of an issue, it would be possible to add some of the required characters/extras
                # to start inventory instead of erroring here.
                all_unfilled = self.world.multiworld.get_unfilled_locations(self.world.player)
                non_excluded_count = len(all_unfilled) - required_excludable_count
                num_to_fill = len(all_unfilled)
                required_count = (
                        self.required_extra
                        + self.required_character
                        + self.required_minikit
                        + self.required_additional
                )
                self.world.option_error(
                    "There are too few non-excluded locations to fit all required progression items."
                    " There are %i locations, %i of which are not excluded, but there are %i required"
                    " items that cannot be placed on excluded locations.",
                    num_to_fill, non_excluded_count, required_count)
        self.required_excludable += required_excludable_count
        assert self.free_location_count >= 0, \
            "free_location_count must always be >= 0 after consuming space for excludable items"

    @property
    def explicit_items_to_create(self):
        return self.required_items_to_create + self.reserved_non_required_character + self.reserved_non_required_extra

    @property
    def required_items_to_create(self):
        return (
            self.required_minikit
            + self.required_character
            + self.required_extra
            + self.required_additional
            + self.required_excludable
        )

    @property
    def expected_locations_to_fill(self):
        return (
            self.free_from_completions
            + self.free_from_true_jedi
            + self.available_minikit
            + self.available_character
            + self.available_extra
            + self.free_from_ridesanity
        )

    @property
    def free_location_count(self):
        return self.expected_locations_to_fill - self.explicit_items_to_create


def _determine_chapters(world: LegoStarWarsTCSWorld) -> tuple[set[str], set[str]]:
    """
    Return the set of chapter short names that have locations, and the set of chapter short names that have non-excluded
    locations.
    """
    if world.goal_chapter:
        if world.options.goal_chapter_locations_mode == GoalChapterLocationsMode.option_removed:
            chapters_with_locations = world.enabled_chapters - {world.goal_chapter}
            chapters_with_non_excluded_locations = world.enabled_non_goal_chapters
        elif world.options.goal_chapter_locations_mode == GoalChapterLocationsMode.option_excluded:
            chapters_with_locations = world.enabled_chapters
            chapters_with_non_excluded_locations = world.enabled_non_goal_chapters
        else:
            assert world.options.goal_chapter_locations_mode == GoalChapterLocationsMode.option_normal
            chapters_with_locations = world.enabled_chapters
            chapters_with_non_excluded_locations = world.enabled_chapters
    else:
        chapters_with_locations = world.enabled_chapters
        chapters_with_non_excluded_locations = world.enabled_chapters

    return chapters_with_locations, chapters_with_non_excluded_locations


def _create_possible_pool(world: LegoStarWarsTCSWorld) -> dict[str, GenericCharacterData]:
    # If Gunship Cavalry (Original), Pod Race (Original) and Anakin's Flight get updated to require Vehicles again,
    # then Republic Gunship, Anakin's Pod and Naboo Starfighter would be required items to included in the pool.
    # if not vehicle_chapters_enabled:
    #     if "Anakin's Flight" in world.enabled_bonuses:
    #         vehicle = CHARACTERS_AND_VEHICLES_BY_NAME["Naboo Starfighter"]
    #         possible_pool_character_items[vehicle.name] = vehicle
    #     if "Gunship Cavalry (Original)" in world.enabled_bonuses:
    #         vehicle = CHARACTERS_AND_VEHICLES_BY_NAME["Republic Gunship"]
    #         possible_pool_character_items[vehicle.name] = vehicle
    #     if "Mos Espa Pod Race (Original)" in world.enabled_bonuses:
    #         vehicle = CHARACTERS_AND_VEHICLES_BY_NAME["Anakin's Pod"]
    #         possible_pool_character_items[vehicle.name] = vehicle
    # todo: Reserve spaces in the item pool for vehicles and non-vehicles separately, based on how many locations
    #  unlock characters of the each type.
    vehicle_chapters_enabled = not VEHICLE_CHAPTER_SHORTNAMES.isdisjoint(world.enabled_chapters)

    possible_pool_character_items = {name: char for name, char in CHARACTERS_AND_VEHICLES_BY_NAME.items()
                                     if char.is_sendable and (vehicle_chapters_enabled
                                                              or char.item_type != "Vehicle")}
    if world.goal_chapter and world.options.goal_chapter_locations_mode == GoalChapterLocationsMode.option_removed:
        # Vehicle chapters could be disabled for normal chapters, but the goal chapter could be a vehicle chapter,
        # so the vehicles required for the goal chapter need to be forced into the item pool.
        for name in CHAPTER_AREA_STORY_CHARACTERS[world.goal_chapter]:
            if name not in possible_pool_character_items:
                possible_pool_character_items[name] = CHARACTERS_AND_VEHICLES_BY_NAME[name]

    return possible_pool_character_items


def determine_random_character_requirements(
        world: LegoStarWarsTCSWorld,
        possible_pool_character_items: dict[str, GenericCharacterData],
) -> None:
    """

    :param world:
    :param possible_pool_character_items:
    :return:
    """
    if world.is_universal_tracker():
        # Should already be loaded from Universal Tracker.
        if not world.chapter_random_character_requirements:
            world.raise_error(Exception, "Random Character requirements for Chapters were not loaded from"
                                         "slot_data")
    else:
        chapters = sorted(world.enabled_chapters)
        world.random.shuffle(chapters)

        pool_size = len(chapters) * world.options.chapter_unlock_random_characters_unique_per_chapter.value
        if pool_size > len(possible_pool_character_items):
            world.log_warning("The size of the requested pool of random Characters to use in Chapter unlock"
                              " requirements was %i, but there were only %i unique Characters available, so the size of"
                              " the pool has been reduced to %i.",
                              pool_size, len(possible_pool_character_items), len(possible_pool_character_items))
            pool_size = len(possible_pool_character_items)

        base_pool = sorted(possible_pool_character_items.keys())
        world.random.shuffle(base_pool)

        extra_counts = world.chapter_extra_random_character_counts
        required_counts = world.chapter_required_character_counts
        # The counts are capped at 9 because displaying the required characters in-game gets squished and difficult to
        # read.
        character_count_per_chapter = {chapter: min(extra_counts[chapter] + required_counts[chapter], 9)
                                       for chapter in chapters}
        min_pool_size = max(character_count_per_chapter.values())
        if pool_size < min_pool_size:
            world.log_warning("Increased the number of unique Characters used in Chapter unlock requirements to %i from"
                              " %i because at least one Chapter needs %i Characters in its unlock requirements.",
                              min_pool_size, pool_size, min_pool_size)
            pool_size = min_pool_size
        pool_size = max(min_pool_size, pool_size)
        pool = base_pool[:pool_size]

        world.log_debug("Random character pool: %s", pool)

        finished_chapter_to_characters: dict[str, set[str]] = {}

        for chapter in chapters:
            count_to_pick = character_count_per_chapter[chapter]
            finished_chapter_to_characters[chapter] = set(world.random.sample(pool, k=count_to_pick))

        if __debug__:
            individual_character_counts = Counter(c for characters in finished_chapter_to_characters.values()
                                                  for c in characters)
            for character in pool:
                if character not in individual_character_counts:
                    individual_character_counts[character] = 0
            count_counts = Counter(individual_character_counts.values())
            world.log_debug("Character count counts: %s", sorted(count_counts.items()))

        world.chapter_random_character_requirements = {k: sorted(v) for k, v in finished_chapter_to_characters.items()}

    for characters_list in world.chapter_random_character_requirements.values():
        for character in characters_list:
            world.character_chapter_access_counts[character] += 1


def _create_starting_characters_for_character_locked_chapters(
        world: LegoStarWarsTCSWorld,
        possible_pool_character_items: dict[str, GenericCharacterData],
        starting_chapter_characters: list[str],
        starting_chapter_required_count: int,
) -> None:
    starting_chapter = world.starting_chapter
    assert starting_chapter_required_count <= len(starting_chapter_characters)
    if starting_chapter_required_count == len(starting_chapter_characters):
        # All characters are needed.
        picked = starting_chapter_characters
        skipped = []
    else:
        # First reduce the characters to those that provide unique, relevant abilities.
        world.random.shuffle(starting_chapter_characters)
        seen_abilities = CharacterAbility.NONE
        picked = []
        skipped = []
        # Ignore any alternate, or irrelevant, ability requirements by only considering the main requirements.
        main_ability_requirements = starting_chapter.completion_main_ability_requirements
        for char in starting_chapter_characters:
            character_data = CHARACTERS_AND_VEHICLES_BY_NAME[char]
            relevant_character_abilities = character_data.abilities & main_ability_requirements
            if relevant_character_abilities not in seen_abilities:
                seen_abilities |= relevant_character_abilities
                picked.append(char)
            else:
                skipped.append(char)
        if starting_chapter_required_count > len(picked):
            # More characters are needed than those with relevant, unique abilities, so pick additional characters from
            # those that were skipped due to having only duplicated abilities.
            extra_needed = starting_chapter_required_count - len(picked)
            picked.extend(skipped[:extra_needed])
            skipped = skipped[extra_needed:]

        # TODO?: Try the alt ability requirements too?

    # TODO: Do the picked characters need to be set somewhere? Check where else world.starting_chapter is used.
    for name in picked:
        world.push_precollected(world.create_item(name))
        del possible_pool_character_items[name]

    for name in skipped:
        # The skipped characters can be considered to no longer give access to the starting chapter, which could change
        # their classifications if they get created.
        world.character_chapter_access_counts[name] -= 1
        # print(f"Reducing count of chapters locked by {name} because the starting chapter will be unlocked by {picked}"
        #       f" instead")
        assert world.character_chapter_access_counts[name] >= 0


def create_starting_characters_for_random_character_locked_chapters(
        world: LegoStarWarsTCSWorld,
        possible_pool_character_items: dict[str, GenericCharacterData],
) -> None:
    """
    Create and precollect the characters the player should start with when chapters are locked by needing Random
    Characters.

    This tries to pick as few characters as possible, but enough such that the starting chapter can be completed.
    :param world:
    :param possible_pool_character_items:
    :return:
    """
    starting_chapter = world.starting_chapter
    required_count = world.chapter_required_character_counts[starting_chapter.short_name]
    characters = world.chapter_random_character_requirements[starting_chapter.short_name].copy()

    _create_starting_characters_for_character_locked_chapters(
        world, possible_pool_character_items, characters, required_count)


def create_starting_characters_for_vanilla_character_locked_chapters(
        world: LegoStarWarsTCSWorld,
        possible_pool_character_items: dict[str, GenericCharacterData],
) -> None:
    """
    Create and precollect the characters the player should start with when chapters are locked by needing Vanilla
    Characters.

    This tries to pick as few characters as possible, but enough such that the starting chapter can be completed.
    :param world:
    :param possible_pool_character_items:
    :return:
    """
    not_required = world.options.chapter_unlock_story_characters_not_required.value

    starting_chapter = world.starting_chapter
    required_count = world.chapter_required_character_counts[starting_chapter.short_name]

    # Add characters necessary to unlock, *and complete* the starting chapter into starting inventory.
    if starting_chapter.short_name in world.chapters_requiring_alt_characters:
        characters_set = starting_chapter.alt_character_requirements
    else:
        characters_set = starting_chapter.character_requirements
    # The story character names are a `set`, so sort before iterating to get a deterministic iteration order.
    # Also filter out characters that have been excluded from requirements.
    characters = sorted(char for char in characters_set if char not in not_required)

    _create_starting_characters_for_character_locked_chapters(
        world, possible_pool_character_items, characters, required_count)


def pick_characters_to_fulfil_abilities(
        world: LegoStarWarsTCSWorld,
        abilities_to_fulfil: CharacterAbility,
        possible_pool_character_items: dict[str, GenericCharacterData],
        abilities_to_ignore: CharacterAbility = CharacterAbility.NONE,
) -> list[GenericCharacterData]:

    abilities_to_fulfil_list = sorted(abilities_to_fulfil & ~abilities_to_ignore)
    if not abilities_to_fulfil_list:
        return []
    # Shuffle the order the abilities will be fulfilled in.
    fulfilled_abilities: set[CharacterAbility] = set()
    world.random.shuffle(abilities_to_fulfil_list)

    # Always pick CAN_ abilities last to avoid picking very boring characters at the start with basically no
    # actual abilities.
    # Always pick VEHICLE_BLASTER last to avoid picking a VEHICLE_BLASTER, and then picking a VEHICLE_TOW that
    # also has VEHICLE_BLASTER.
    abilities_to_fulfil_list.sort(key=ABILITY_PICK_ORDER.__getitem__)

    # Finally pick characters to fulfil the abilities.
    ability_costs = BASE_ABILITY_COSTS.copy()
    # Clear the cost for abilities that are ignored.
    for ability in abilities_to_ignore:
        ability_costs[ability] = 0

    def sort_func(data: GenericCharacterData):
        value = 0
        for ability in data.abilities:
            value += ability_costs.get(ability, 0)
        return value

    # Pre-calculate the list of characters that provide each individual ability.
    picked_characters: list[GenericCharacterData] = []
    characters_by_ability: dict[CharacterAbility, list[GenericCharacterData]] = {}
    for character_data in possible_pool_character_items.values():
        for ability in character_data.abilities:
            characters_by_ability.setdefault(ability, []).append(character_data)

    for individual_ability in abilities_to_fulfil_list:
        if individual_ability in fulfilled_abilities:
            # A character picked earlier also had this ability, so there does not need to be another character
            # picked.
            continue
        candidates = characters_by_ability[individual_ability]
        # Shuffle first, so that ties on the sort have deterministically random order.
        world.random.shuffle(candidates)
        candidates.sort(key=sort_func)
        # Randomly pick from the first quarter to avoid always picking the character in the list with the lowest
        # ability score.
        picks = candidates[0:max(1, round(len(candidates) * 0.25))]
        picked = world.random.choice(picks)
        picked_characters.append(picked)
        del possible_pool_character_items[picked.name]
        fulfilled_abilities.update(picked.abilities)
        for ability in picked.abilities:
            # The ability is provided by the picked character, so it is no longer relevant for sorting future
            # picks.
            ability_costs[ability] = 0
    return picked_characters


def create_starting_characters_for_needed_starting_chapter_abilities(
        world: LegoStarWarsTCSWorld,
        possible_pool_character_items: dict[str, GenericCharacterData],
) -> None:
    """

    :param world:
    :param possible_pool_character_items:
    :return:
    """
    # Get the abilities the player is currently starting with.
    starting_abilities = world.get_starting_inventory_abilities()

    # Only give enough characters to fulfil the main requirements of the starting chapter, unless all rarer, required
    # alt requirements have already been fulfilled and fewer characters get picked to fulfil the alt requirements.
    starting_chapter_entrance_abilities = world.starting_chapter.completion_main_ability_requirements

    picked_characters = pick_characters_to_fulfil_abilities(
        world,
        starting_chapter_entrance_abilities,
        possible_pool_character_items.copy(),
        starting_abilities,
    )

    # Also try the alt abilities, if they exist, and they don't contain any rare or useful abilities that are not
    # required by the main abilities.
    alt_abilities = world.starting_chapter.completion_alt_ability_requirements
    if alt_abilities:
        alt_abilities &= ~starting_abilities
        unique_alt_abilities = alt_abilities & ~starting_chapter_entrance_abilities
        if not any(ability in RARE_AND_USEFUL_ABILITIES for ability in unique_alt_abilities):
            alt_picked_characters = pick_characters_to_fulfil_abilities(
                world,
                alt_abilities,
                possible_pool_character_items.copy(),
                starting_abilities,
            )
            # Use the alt characters if fewer were picked.
            if len(alt_picked_characters) < len(picked_characters):
                picked_characters = alt_picked_characters

    for character in picked_characters:
        world.push_precollected(world.create_item(character.name))
        del possible_pool_character_items[character.name]


def determine_item_pool_abilities(
        world: LegoStarWarsTCSWorld,
        chapters_with_locations: set[str]
) -> ItemPoolAbilityRequirements:
    # Determine what abilities must be supplied by the item pool for all locations to be reachable with all items in
    # the item pool.
    required_character_abilities_in_pool = CharacterAbility.NONE
    optional_character_abilities = CharacterAbility.NONE
    # `chapters_with_locations` is a `set`, so sort for deterministic results from the `world.random` usage.
    for shortname in sorted(chapters_with_locations):
        power_brick_abilities = POWER_BRICK_REQUIREMENTS[shortname][1]
        if power_brick_abilities is not None:
            if isinstance(power_brick_abilities, tuple):
                at_least_one_already_required = False
                for abilities in power_brick_abilities:
                    if abilities in required_character_abilities_in_pool:
                        at_least_one_already_required = True
                    # Mark the abilities as optional. They will be included in logic, but won't necessarily be
                    # guaranteed to be provided by the item pool.
                    optional_character_abilities |= abilities

                if not at_least_one_already_required:
                    # Pick any one of the abilities to be required to be provided by the item pool.
                    picked = world.random.choice(power_brick_abilities)
                    required_character_abilities_in_pool |= picked
            else:
                required_character_abilities_in_pool |= power_brick_abilities
        if world.options.enable_minikit_locations.value:
            for requirements in SHORT_NAME_TO_CHAPTER_AREA[shortname].all_minikits_ability_requirements:
                required_character_abilities_in_pool |= requirements
    for bonus_name in world.enabled_bonuses:
        area = BONUS_NAME_TO_BONUS_AREA[bonus_name]
        required_character_abilities_in_pool |= area.completion_ability_requirements
    for _area_name, ridable_spots in world.ridesanity_spots.items():
        for _spot, any_ridable_ability_requirements in ridable_spots:
            if any_ridable_ability_requirements:
                if len(any_ridable_ability_requirements) == 1:
                    required_character_abilities_in_pool |= any_ridable_ability_requirements[0]
                else:
                    at_least_one_already_required = False
                    for ridable_ability_requirements in any_ridable_ability_requirements:
                        if ridable_ability_requirements in required_character_abilities_in_pool:
                            at_least_one_already_required = True
                        # Mark the abilities as optional. They will be included in logic, but won't necessarily be
                        # guaranteed to be provided by the item pool.
                        optional_character_abilities |= ridable_ability_requirements

                    if not at_least_one_already_required:
                        # Pick any one of the abilities to be required to be provided by the item pool.
                        picked = world.random.choice(any_ridable_ability_requirements)
                        required_character_abilities_in_pool |= picked
    return ItemPoolAbilityRequirements(required_character_abilities_in_pool, optional_character_abilities)


def create_item_pool(world: LegoStarWarsTCSWorld):
    # Determine how many chapter worth's of locations are enabled.
    goal_chapter_locations_excluded = (
            world.goal_chapter
            and world.options.goal_chapter_locations_mode == GoalChapterLocationsMode.option_excluded
    )

    chapters_with_locations, chapters_with_non_excluded_locations = _determine_chapters(world)

    possible_pool_character_items = _create_possible_pool(world)

    pool_required_chapter_unlock_items: list[str]
    if world.options.chapter_unlock_requirement == ChapterUnlockRequirement.option_vanilla_characters:
        chapters_unlock_with_characters = True
        pool_required_chapter_unlock_items = []

        create_starting_characters_for_vanilla_character_locked_chapters(world, possible_pool_character_items)
        # If the alt characters are created, or not all Story characters are created, there may be abilities that still
        # need to be fulfilled by additional starting characters, so
        # `create_starting_characters_for_needed_starting_chapter_abilities()` will be called even in this case.
    elif world.options.chapter_unlock_requirement == ChapterUnlockRequirement.option_random_characters:
        chapters_unlock_with_characters = True
        pool_required_chapter_unlock_items = []

        determine_random_character_requirements(world, possible_pool_character_items)
        create_starting_characters_for_random_character_locked_chapters(world, possible_pool_character_items)
    elif world.options.chapter_unlock_requirement == ChapterUnlockRequirement.option_chapter_item:
        chapters_unlock_with_characters = False
        starting_chapter_short_name = world.starting_chapter.short_name
        world.push_precollected(world.create_item(f"{starting_chapter_short_name} Unlock"))
        pool_required_chapter_unlock_items = [f"{short_name} Unlock" for short_name in sorted(world.enabled_chapters)
                                              if short_name != starting_chapter_short_name]
        del starting_chapter_short_name
    else:
        raise Exception(f"Unexpected Chapter Unlock Requirement {world.options.chapter_unlock_requirement}")

    create_starting_characters_for_needed_starting_chapter_abilities(world, possible_pool_character_items)

    # Create the starting Episode Unlock item if Episode Unlock items are required to access chapters within an Episode.
    if world.options.episode_unlock_requirement == "episode_item":
        world.push_precollected(world.create_item(f"Episode {world.starting_episode} Unlock"))

    item_pool_ability_requirements = determine_item_pool_abilities(world, chapters_with_locations)

    item_pool_ability_requirements.update_for_chapter_ability_requirements(world)

    if chapters_unlock_with_characters:
        # Unary `+` (__pos__) creates a new Counter with counts <= 0 removed.
        level_access_character_counts = +world.character_chapter_access_counts
    else:
        level_access_character_counts = Counter()

    # Gather the abilities of all items in starting inventory, so that they can be removed from other created items,
    # improving generation performance.
    starting_abilities = world.get_starting_inventory_abilities()

    item_pool_ability_requirements.update_for_starting_abilities(starting_abilities)

    return _create_items(
        world,
        level_access_character_counts,
        possible_pool_character_items,
        len(chapters_with_non_excluded_locations),
        goal_chapter_locations_excluded,
        pool_required_chapter_unlock_items,
        chapters_unlock_with_characters,
        item_pool_ability_requirements,
    )


def _append_level_access_required_characters(
        world: LegoStarWarsTCSWorld,
        pool_required_characters: list[GenericCharacterData],
        level_access_character_counts: Counter[str],
        possible_pool_character_items: dict[str, GenericCharacterData],
        item_pool_ability_requirements: ItemPoolAbilityRequirements,
) -> None:
    if not world.options.chapter_unlock_requirement.is_characters():
        # Specific characters are not required to access Chapters.
        return

    is_random_characters = world.options.chapter_unlock_requirement == ChapterUnlockRequirement.option_random_characters

    enabled_chapters = sorted(world.enabled_chapters)
    world.random.shuffle(enabled_chapters)

    if world.options.chapter_unlock_requirement == ChapterUnlockRequirement.option_vanilla_characters:
        excluded_story_characters = world.options.chapter_unlock_story_characters_not_required.value
    else:
        excluded_story_characters = ()

    abilities_provided = CharacterAbility.NONE

    for shortname in enabled_chapters:
        chapter = SHORT_NAME_TO_CHAPTER_AREA[shortname]
        if chapter == world.starting_chapter:
            # Characters for the starting chapter are created separately.
            continue
        if is_random_characters:
            characters = world.chapter_random_character_requirements[shortname]
        else:
            # Must be vanilla characters.
            if shortname in world.chapters_requiring_alt_characters:
                characters = sorted(chapter.alt_character_requirements)
            else:
                characters = sorted(c for c in chapter.character_requirements if c not in excluded_story_characters)

        # Skip already created characters and excluded characters.
        for character in characters:
            assert level_access_character_counts[character] > 0
            if character not in possible_pool_character_items:
                # This character has already been created.
                continue
            char = CHARACTERS_AND_VEHICLES_BY_NAME[character]
            abilities_provided |= char.abilities
            pool_required_characters.append(char)
            del possible_pool_character_items[character]

    item_pool_ability_requirements.required &= ~abilities_provided


def _append_remaining_required_characters(
        pool_required_characters: list[GenericCharacterData],
        world: LegoStarWarsTCSWorld,
        possible_pool_character_items: dict[str, GenericCharacterData],
        item_pool_ability_requirements: ItemPoolAbilityRequirements,
) -> None:
    possible_pool_character_names = list(possible_pool_character_items.values())
    world.random.shuffle(possible_pool_character_names)
    # Sort preferred characters first so that they are picked in preference.
    preferred_characters = world.options.preferred_characters.value
    if preferred_characters:
        possible_pool_character_names.sort(key=lambda char: -1 if char.name in preferred_characters else 0)

    for character in possible_pool_character_names:
        if item_pool_ability_requirements.required & character.abilities:
            # This character satisfied at least one of the remaining required abilities.
            pool_required_characters.append(character)
            item_pool_ability_requirements.required &= ~character.abilities
            del possible_pool_character_items[character.name]


def prepare_extras(world: LegoStarWarsTCSWorld) -> tuple[list[str], list[str]]:
    """
    Pre-collect starting Extras and get lists of the required and non-required Extras to be included in the item pool.
    :param world: The world that is creating items.
    :return: A list of item names required to be included in the item pool and a list of item names not required to be
     included in the item pool.
    """
    # Start with all sendable Extras as possible to add to the item pool.
    possible_pool_extras = {name: extra for name, extra in EXTRAS_BY_NAME.items() if extra.is_sendable}

    if not world.options.enable_starting_extras_locations:
        # The starting Extra purchases are vanilla, so don't include their Extras in the pool.
        for extra in PURCHASABLE_NON_POWER_BRICK_EXTRAS:
            del possible_pool_extras[extra.name]

    if world.options.start_with_detectors:
        detectors = {"Minikit Detector", "Power Brick Detector"}
        assert detectors <= set(possible_pool_extras.keys())
        # The detector Extras are being given to the player at the start, so don't include their Extras in the pool.
        for extra_name in detectors:
            del possible_pool_extras[extra_name]
        for detector in sorted(detectors):
            world.push_precollected(world.create_item(detector))

    non_required_extras: list[str] = list(possible_pool_extras.keys())

    max_studs_purchase = max(loc.studs_cost for loc in world.get_locations()
                             if isinstance(loc, LegoStarWarsTCSShopLocation))

    required_score_multipliers = world.get_score_multiplier_requirement(max_studs_purchase)
    # Increase required_score_multipliers to at least 1 if there are any enabled chapters with difficult or
    # potentially impossible True Jedi.
    if (required_score_multipliers < 1
            and world.options.enable_true_jedi_locations
            and not world.options.easier_true_jedi
            and not DIFFICULT_OR_IMPOSSIBLE_TRUE_JEDI.isdisjoint(world.enabled_chapters_with_locations)):
        required_score_multipliers = 1

    non_required_score_multipliers = 5 - required_score_multipliers
    assert 0 <= required_score_multipliers <= 5
    pool_required_extras: list[str] = [progressive_score_multiplier_name] * required_score_multipliers
    non_required_extras.extend([progressive_score_multiplier_name] * non_required_score_multipliers)
    return pool_required_extras, non_required_extras


def _sort_for_preferred_extras(non_required_extras: list[str], world: LegoStarWarsTCSWorld) -> list[str]:
    """
    Sort preferred Extras to the front of `non_required_extras`. May run in-place on non_required_extras.

    This is more complicated than it sounds because score multipliers are currently always progressive, and the player
    can specify how many score multipliers they prefer by using the non-progressive names of the score multipliers.
    :param non_required_extras: The names of all Extras items that are not required to be included in the item pool.
    :param world: The world that is creating its item pool.
    :return: A list of Extras item names, with preferred Extras sorted to the front.
    """
    preferred_extras = world.options.preferred_extras.value
    if not preferred_extras:
        return non_required_extras
    # The score multipliers are in descending order because Score x10 means the player prefers all score multipliers
    # to be in the item pool
    individual_score_multipliers = [
        "Score x10",
        "Score x8",
        "Score x6",
        "Score x4",
        "Score x2",
    ]
    non_required_score_multiplier_indices = [i for i, extra in enumerate(non_required_extras)
                                             if extra == progressive_score_multiplier_name]
    if not non_required_score_multiplier_indices or preferred_extras.isdisjoint(individual_score_multipliers):
        num_preferred_non_required_score_multipliers = 0
    else:
        # Find the highest preferred Score multiplier and ensure the lower multipliers are also preferred.
        num_preferred_non_required_score_multipliers = len(non_required_score_multiplier_indices)
        # Score x10 -> All non-required are preferred.
        # Score x8 -> (All - 1) non-required are preferred.
        # ...
        # Score x2 -> (All - 4) non-required are preferred.
        for count_not_preferred, multiplier in enumerate(individual_score_multipliers):
            if multiplier in preferred_extras:
                num_preferred_non_required_score_multipliers -= count_not_preferred
                break
        else:
            raise Exception("Unreachable. At least one score multiplier in `individual_score_multipliers` must be"
                            " present in `preferred_extras` because of the `not a.isdisjoint(b)` check, so the loop"
                            " should always break.")

    if num_preferred_non_required_score_multipliers <= 0:
        # Simply sort preferred extras to the front so that they get picked first.
        non_required_extras.sort(key=lambda extra: -1 if extra in preferred_extras else 0)
        return non_required_extras
    else:
        # Pick the Progressive Score Multipliers randomly for fairness.
        picked_preferred_score_multiplier_indices = world.random.sample(non_required_score_multiplier_indices,
                                                                        num_preferred_non_required_score_multipliers)
        # Sort preferred extras to the front by splitting the extras into two lists of preferred and non-preferred.
        preferred_extras_list = []
        non_preferred_extras_list = []
        for i, item in enumerate(non_required_extras):
            if item in preferred_extras:
                preferred_extras_list.append(item)
            elif item == progressive_score_multiplier_name and i in picked_preferred_score_multiplier_indices:
                preferred_extras_list.append(item)
            else:
                non_preferred_extras_list.append(item)
        return preferred_extras_list + non_preferred_extras_list


def _get_additional_required_items(
        world: LegoStarWarsTCSWorld,
        pool_required_chapter_unlock_items: list[str],
) -> tuple[list[str], list[str]]:
    """
    Get the names of additional required items that don't fall into any specific category.
    :param world: The world that is creating its item pool.
    :param pool_required_chapter_unlock_items: The Chapter Unlock items that this world requires to be in the item pool.
    :return: A tuple containing a list of items required to be in the pool, and a list of items required to be added to
    the player's starting inventory.
    """
    other_required_items: list[str] = []
    starting_other_required_items: list[str] = []
    # A few free locations may need to be used for episode unlock items and/or episode tokens.
    if world.options.episode_unlock_requirement == "episode_item":
        for i in world.enabled_episodes:
            if i != world.starting_episode:
                other_required_items.append(f"Episode {i} Unlock")
    if world.options.all_episodes_character_purchase_requirements == "episodes_tokens":
        # One token is added to the item pool for every episode's worth of (6) chapters that are enabled.
        tokens_in_pool = max(1, round(len(world.enabled_chapters) / 6))
        start_inventory_tokens = 6 - tokens_in_pool
        assert 5 >= start_inventory_tokens >= 0
        for _ in range(tokens_in_pool):
            other_required_items.append("Episode Completion Token")
        for _ in range(start_inventory_tokens):
            starting_other_required_items.append("Episode Completion Token")
    # 7 free locations may need to be used for Kyber Bricks.
    if world.options.goal_requires_kyber_bricks:
        other_required_items.extend(("Kyber Brick",) * 7)

    # As many Chapter Unlock items as there are enabled Chapters, excluding the starting chapter.
    other_required_items.extend(pool_required_chapter_unlock_items)
    return other_required_items, starting_other_required_items


def _balance_item_location_counts(
        world: LegoStarWarsTCSWorld,
        num_to_fill: int,
        non_excluded_chapter_count: int,
        goal_chapter_locations_excluded: bool,
        pool_required_characters_count: int,
        pool_required_extras_count: int,
        pool_required_additional_items_count: int,
) -> ItemLocationCounts:
    """
    Balance out the item counts to add to the item pool, ensuring that, if there is not enough space in the pool for all
    required items, that an OptionError is raised, and that no more items are added to the item pool than the number of
    unfilled locations to fill.
    :param world: The world that is creating its item pool.
    :param num_to_fill: The number of unfilled locations to fill, and therefore items to create.
    :param non_excluded_chapter_count: The number of non-excluded chapters present for this world.
    :param goal_chapter_locations_excluded: Whether the goal chapter's locations are excluded for this world.
    :param pool_required_characters_count: The number of characters required to be present in the item pool.
    :param pool_required_extras_count: The number of Extras required to be present in the item pool.
    :param pool_required_additional_items_count: The number of additional items required to be present in the item pool.
    :return: An ItemLocationCounts instance with counts of items to create, balanced against the number of locations to
    fill with items.
    """
    item_location_counts = ItemLocationCounts(world, non_excluded_chapter_count, goal_chapter_locations_excluded)
    item_location_counts.set_true_jedi_counts()
    item_location_counts.set_completion_counts()
    item_location_counts.set_ridesanity_counts()

    free_location_count = item_location_counts.free_location_count

    assert free_location_count >= 0, "initial free_location_count should always be >= 0"

    # There may be more minikits/characters/extras required/desired than enabled locations that provide those items in
    # vanilla, so `item_location_counts.free_location_count` could now be negative.
    item_location_counts.set_minikit_counts()
    item_location_counts.set_character_counts(pool_required_characters_count)
    item_location_counts.set_extra_counts(pool_required_extras_count)

    # These items don't have associated vanilla locations at all, so will have to consume free locations to fit into the
    # item pool.
    item_location_counts.set_additional_item_counts(pool_required_additional_items_count)

    # If there was not enough space for all required items, replace reserved space, intended for non-required items,
    # until there is enough space, or raise an OptionError if there is still not enough space, even with all reserved
    # space replaced.
    item_location_counts.free_space_for_required_items()

    # Check that the number of locations that are expected to be filled matches the number of locations that are
    # unfilled.
    expected_num_to_fill = item_location_counts.expected_locations_to_fill
    assert num_to_fill == expected_num_to_fill, \
        f"Expected {expected_num_to_fill} locations to fill, but got {num_to_fill}"

    # Ensure there is enough space in the item pool for as many filler items as there are excluded locations.
    item_location_counts.free_space_for_excluded_locations()

    expected_num_to_fill = item_location_counts.expected_locations_to_fill
    assert num_to_fill == expected_num_to_fill, \
        (f"Expected {expected_num_to_fill} locations to fill, but got {num_to_fill} after"
         f" freeing space for excludable items.")

    assert num_to_fill >= item_location_counts.explicit_items_to_create
    assert item_location_counts.required_minikit >= 0
    assert item_location_counts.required_character >= 0
    assert item_location_counts.required_extra >= 0
    assert item_location_counts.required_additional >= 0
    assert item_location_counts.required_excludable >= 0
    assert item_location_counts.free_from_completions >= 0
    assert item_location_counts.free_from_true_jedi >= 0
    assert item_location_counts.available_minikit >= 0
    assert item_location_counts.available_character >= 0
    assert item_location_counts.available_extra >= 0
    assert item_location_counts.free_from_ridesanity >= 0

    return item_location_counts


def _create_pool(
        world: LegoStarWarsTCSWorld,
        remaining_to_create: int,
        item_creator: ItemCreator,
        item_location_counts: ItemLocationCounts,
        other_required_items: list[str],
        pool_required_characters: list[GenericCharacterData],
        pool_required_extras: list[str],
        non_required_characters: list[GenericCharacterData],
        non_required_extras: list[str],
) -> list[LegoStarWarsTCSItem]:
    """
    Create each of the items to add into the multiworld item pool.
    :param world: The world that is creating its item pool.
    :param remaining_to_create: The remaining count of items to create
    :param item_creator: An ItemCreator instance, already set up to handling stripping starting abilities from created
    items.
    :param item_location_counts: Predetermined, item counts to add into the item pool.
    :param other_required_items: A list of required item names that don't belong to any particular item type.
    :param pool_required_characters: A list of character data of all characters that are required to be present in the
    item pool.
    :param pool_required_extras: A list of Extra names, of Extra items that are required to be present in the item pool.
    :param non_required_characters: A list of character data of all characters that are available to include in the item
    pool, but are not required.
    :param non_required_extras: A list of Extra names, of Extra items that are available to include in the item pool, but
    are not required.
    :return: The full item pool for the given world.
    """
    item_pool: list[LegoStarWarsTCSItem] = []

    created_item_names: set[str] = set()

    def add_to_pool(item: LegoStarWarsTCSItem):
        nonlocal remaining_to_create
        remaining_to_create -= 1
        if remaining_to_create < 0:
            raise RuntimeError("Ran out of unfilled locations...")
        item_pool.append(item)
        created_item_names.add(item.name)

    # Create required generic items that don't fall into any particular category.
    for name in other_required_items:
        add_to_pool(item_creator.create_item(name))

    # Create required characters.
    assert len(pool_required_characters) == item_location_counts.required_character
    for character in pool_required_characters:
        add_to_pool(item_creator.create_item(character.name))

    # Create required extras.
    assert len(pool_required_extras) == item_location_counts.required_extra
    for extra_name in pool_required_extras:
        add_to_pool(item_creator.create_item(extra_name))

    # Create required minikits.
    for _ in range(world.minikit_bundle_count):
        add_to_pool(item_creator.create_item(world.minikit_bundle_name))

    # Create as many non-required characters as there are reserved character locations.
    required_excludable_count = item_location_counts.required_excludable
    world.random.shuffle(non_required_characters)
    # Sort preferred characters first so that they are picked in preference.
    preferred_characters = world.options.preferred_characters.value
    if preferred_characters:
        non_required_characters.sort(key=lambda char: -1 if char.name in preferred_characters else 0)
    picked_chars = non_required_characters[:item_location_counts.reserved_non_required_character]
    leftover_chars = non_required_characters[item_location_counts.reserved_non_required_character:]
    for char in picked_chars:
        item = item_creator.create_item(char.name)
        add_to_pool(item)
        if required_excludable_count > 0 and item.excludable:
            required_excludable_count -= 1

    # Create as many non-required extras as there are reserved power brick locations.
    world.random.shuffle(non_required_extras)
    # Sort preferred Extras first so that they are picked in preference.
    non_required_extras = _sort_for_preferred_extras(non_required_extras, world)

    picked_extras = non_required_extras[:item_location_counts.reserved_non_required_extra]
    leftover_extras = non_required_extras[item_location_counts.reserved_non_required_extra:]
    for extra in picked_extras:
        item = item_creator.create_item(extra)
        add_to_pool(item)
        if required_excludable_count > 0 and item.excludable:
            required_excludable_count -= 1

    # Determine items to fill out the rest of the item pool according to the weights in the options.
    leftover_choices: list[list[LegoStarWarsTCSItem]] = []
    leftover_weights: list[int] = []

    leftover_character_items = list(map(item_creator.create_item, (char.name for char in leftover_chars)))
    character_weight = world.options.filler_weight_characters.value
    if character_weight and leftover_character_items:
        leftover_choices.append(leftover_character_items)
        leftover_weights.append(character_weight)

    leftover_extra_items = list(map(item_creator.create_item, leftover_extras))
    extras_weight = world.options.filler_weight_extras.value
    if extras_weight and leftover_extra_items:
        leftover_choices.append(leftover_extra_items)
        leftover_weights.append(extras_weight)

    junk_names_and_weights = world.options.junk_weights.value
    junk_names = tuple(junk_names_and_weights.keys())
    junk_weights = tuple(junk_names_and_weights.values())

    def create_excludable_junk_items(count: int) -> list[LegoStarWarsTCSItem]:
        names = world.random.choices(junk_names, junk_weights, k=count)
        return list(map(item_creator.create_item, names))

    junk_weight = world.options.filler_weight_junk.value
    if junk_weight:
        leftover_junk = create_excludable_junk_items(max(remaining_to_create, required_excludable_count))
        leftover_choices.append(leftover_junk)
        leftover_weights.append(junk_weight)

    all_leftover_items: Iterable[LegoStarWarsTCSItem]
    if not leftover_choices:
        # While there is always at least one nonzero weight, it's possible to have run out of Extras or Characters.
        all_leftover_items = []
    elif len(leftover_choices) == 1:
        all_leftover_items = leftover_choices[0]
    else:
        weighted_leftover_items: list[LegoStarWarsTCSItem] = []
        needed_excludable = required_excludable_count
        # Items will be popped from the ends rather than taken from the start, so reverse the lists.
        for item_list in leftover_choices:
            item_list.reverse()
        while (len(weighted_leftover_items) < remaining_to_create or needed_excludable > 0) and leftover_choices:
            picked_list = world.random.choices(leftover_choices, leftover_weights, k=1)[0]
            item = picked_list.pop()
            if needed_excludable > 0 and item.excludable:
                needed_excludable -= 1
            weighted_leftover_items.append(item)
            if not picked_list:
                # The picked list is now empty, so update leftover_choices
                next_leftover_choices: list[list[LegoStarWarsTCSItem]] = []
                next_leftover_weights: list[int] = []
                for item_list, weight in zip(leftover_choices, leftover_weights):
                    if item_list:
                        next_leftover_choices.append(item_list)
                        next_leftover_weights.append(weight)

                leftover_choices = next_leftover_choices
                leftover_weights = next_leftover_weights

                if len(leftover_choices) == 1:
                    # There is only one list left, so append all elements from it.
                    remaining_list = next_leftover_choices[0]
                    weighted_leftover_items.extend(reversed(remaining_list))
                    remaining_list.clear()
                    break

        all_leftover_items = weighted_leftover_items

    # Split the all_leftover_items into separate lists for required excludable items and other leftover items.
    excludable_leftover_items = []
    leftover_items = []
    for item in all_leftover_items:
        if required_excludable_count > 0 and item.excludable:
            excludable_leftover_items.append(item)
            required_excludable_count -= 1
        else:
            leftover_items.append(item)
    if required_excludable_count > 0:
        excludable_leftover_items.extend(create_excludable_junk_items(required_excludable_count))

    for item in excludable_leftover_items:
        add_to_pool(item)

    if len(leftover_items) < remaining_to_create:
        leftover_items.extend(create_excludable_junk_items(remaining_to_create - len(leftover_items)))
    else:
        leftover_items = leftover_items[:remaining_to_create]
    assert len(leftover_items) == remaining_to_create

    for item in leftover_items:
        add_to_pool(item)

    return item_pool


def _apply_deprioritized_and_skip_balancing_to_characters(
        world: LegoStarWarsTCSWorld,
        item_pool: list[LegoStarWarsTCSItem],
        chapters_unlock_with_characters: bool,
        level_access_character_counts: Counter[str],
) -> None:
    """
    Apply deprioritized and skip_balancing classifications to characters whose only abilities are commonly found within
    the item pool.
    :param world: The world that is creating its item pool.
    :param item_pool: The full created item pool.
    :param chapters_unlock_with_characters: Whether chapters are set to unlock with characters.
    :param level_access_character_counts: The counts of how many levels each character locks access to.
    """
    # todo: In the future, individual characters may be relevant to logic, e.g. Droideka, which should never be
    #  given deprioritized + skip_balancing.
    # Give deprioritized + skip_balancing to characters with only common abilities, and that do not give access to
    # levels.
    non_level_access_character_items: list[LegoStarWarsTCSItem] = []
    non_deprioritize_ability_counts: Counter[CharacterAbility] = Counter()
    for item in item_pool:
        if item.advancement and item.name in CHARACTERS_AND_VEHICLES_BY_NAME:
            if progression_deprioritized_skip_balancing in item.classification:
                # Don't count abilities from characters that are already deprioritized + skip_balancing.
                continue
            abilities = item.abilities
            if abilities:
                non_deprioritize_ability_counts.update(abilities)
            if chapters_unlock_with_characters:
                if level_access_character_counts[item.name] == 0:
                    assert abilities, (f"No abilities should mean the character item is not progression currently if"
                                       f" the character does not unlock levels, but {item.name} has no abilities and"
                                       f" does not unlock levels.")
                    non_level_access_character_items.append(item)
            else:
                non_level_access_character_items.append(item)
    world.random.shuffle(non_level_access_character_items)
    for item in non_level_access_character_items:
        abilities = item.abilities
        for ability in abilities:
            # 3 is a magic number and could be changed if other values produce nicer results.
            if non_deprioritize_ability_counts[ability] <= 3:
                # One of the abilities is uncommon.
                break
        else:
            # None of the abilities were uncommon, so add the deprioritize and skip balancing classifications.
            item.classification |= progression_deprioritized_skip_balancing
            if abilities:
                # Reduce the remaining ability counts from non-deprioritized characters
                non_deprioritize_ability_counts.subtract(abilities)
    assert all(ability.bit_count() == 1 for ability in non_deprioritize_ability_counts)


def _create_items(
        world: LegoStarWarsTCSWorld,
        level_access_character_counts: Counter[str],
        possible_pool_character_items: dict[str, GenericCharacterData],
        non_excluded_chapter_count: int,
        goal_chapter_locations_excluded: bool,
        pool_required_chapter_unlock_items: list[str],
        chapters_unlock_with_characters: bool,
        item_pool_ability_requirements: ItemPoolAbilityRequirements,
) -> list[LegoStarWarsTCSItem]:
    """
    Main item pool creation function.
    :param world: The world that is creating its item pool.
    :param level_access_character_counts: The names of characters that lock access to levels, and the count of levels
    that character locks access to for the current player.
    :param possible_pool_character_items: Character item names and their data that are possible to include in the item
    pool.
    :param non_excluded_chapter_count: The number of enabled chapters that do not have their locations automatically
    excluded.
    :param goal_chapter_locations_excluded: Whether the goal chapter's locations are automatically excluded.
    :param pool_required_chapter_unlock_items: Chapter Unlock item names that must be provided by the item pool.
    :param chapters_unlock_with_characters: Whether chapters are locked by characters, rather than by unlock items.
    :param item_pool_ability_requirements: CharacterAbility requirements for the item pool.
    :return: The created item pool.
    """
    if world.is_universal_tracker():
        # Universal Tracker discards the item pool, so don't bother creating it in the first place.
        # In rare cases, due to Universal Tracker integration assuming there are no starting abilities, some characters
        # who would normally have all their abilities removed, and become non-progression, could become progression when
        # generating with Universal Tracker, and it might not be possible to fit all the progression items into the pool
        # if there are more than expected.
        return []

    item_creator = ItemCreator(world, item_pool_ability_requirements.get_logically_irrelevant())

    # These abilities are provided by the starting characters, so these abilities can be stripped from other
    # characters, improving logic performance.
    world.starting_character_abilities = item_pool_ability_requirements.starting

    pool_required_characters: list[GenericCharacterData] = []
    # Append characters that are required to access levels, updating `item_pool_ability_requirements` as characters are
    # appended.
    _append_level_access_required_characters(
        world,
        pool_required_characters,
        level_access_character_counts,
        possible_pool_character_items,
        item_pool_ability_requirements,
    )
    # Append additional characters to satisfy the remaining required abilities in `item_pool_ability_requirements`.
    _append_remaining_required_characters(pool_required_characters,
                                          world,
                                          possible_pool_character_items,
                                          item_pool_ability_requirements)

    non_required_characters = list(possible_pool_character_items.values())

    # The abilities that need to be fulfilled by the item pool, retrieved, before modification, to double-check that all
    # required abilities are accounted for.
    required_abilities_to_fulfil = item_pool_ability_requirements.required
    assert item_pool_ability_requirements.required is CharacterAbility.NONE, \
           "There are required abilities remaining that have not been fulfilled."
    assert required_abilities_to_fulfil in reduce(
        or_, (data.abilities for data in pool_required_characters), CharacterAbility.NONE), \
        "The abilities of the required characters are not a subset of the required abilities."

    # Get the required, and non-required extras.
    pool_required_extras, non_required_extras = prepare_extras(world)

    # Get other required items that don't belong to any particular category, and don't have associated vanilla
    # locations.
    other_required_items, starting_required_other_items = _get_additional_required_items(
        world, pool_required_chapter_unlock_items)

    # Pre-collect the items (Episode Completion Tokens) that won't be in the pool, but the player will start with.
    for item_name in starting_required_other_items:
        world.push_precollected(item_creator.create_item(item_name))

    unfilled_locations = world.multiworld.get_unfilled_locations(world.player)
    num_to_fill = len(unfilled_locations)

    # Balance out the number of items to create, against the number of locations to fill.
    item_location_counts = _balance_item_location_counts(
        world,
        num_to_fill,
        non_excluded_chapter_count,
        goal_chapter_locations_excluded,
        len(pool_required_characters),
        len(pool_required_extras),
        len(other_required_items),
    )

    # Create the full item pool.
    item_pool = _create_pool(
        world,
        num_to_fill,
        item_creator,
        item_location_counts,
        other_required_items,
        pool_required_characters,
        pool_required_extras,
        non_required_characters,
        non_required_extras,
    )

    assert len(item_pool) == len(unfilled_locations), \
        f"Created {len(item_pool)} items, but there were {len(unfilled_locations)} unfilled locations"

    # Apply deprioritized and skip_balancing classifications to characters with abilities that are commonly found in the
    # item pool.
    _apply_deprioritized_and_skip_balancing_to_characters(
        world,
        item_pool,
        chapters_unlock_with_characters,
        level_access_character_counts,
    )

    return item_pool
