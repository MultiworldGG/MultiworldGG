from collections import Counter
from dataclasses import dataclass
from functools import reduce
from operator import or_
from typing import TYPE_CHECKING, Iterable

import Utils
from rule_builder.rules import Rule
from BaseClasses import LocationProgressType, ItemClassification, Entrance, Location, Region, CollectionState
from Fill import sweep_from_pool

from .character_ability import CharacterAbility
from .constants import CHAPTER_SPECIFIC_FLAGS
from .data.areas import PURCHASABLE_NON_POWER_BRICK_EXTRAS, VEHICLE_CHAPTERS, Area
from .data.characters import Character
from .data.extras import Extra
from .data.items import GenericCharacterData
from .data.items.all_character_items import SENDABLE_CHARACTER_TO_ITEM_DATA, CHARACTER_TO_ITEM_DATA
from .data.items.extra_items import EXTRA_DATA, ExtraData
from .data.items.generic_items import NonDataItemName, CHAPTER_TO_CHAPTER_UNLOCK_ITEM
from .data.logic import CHAPTERS_BY_AREA
from .data.logic.extraction import (
    AbilityRequirements as AbilityRequirementsExtractor,
    CNFAbilityRequirementsExtractor,
    DEFAULT_ABILITY_COSTS,
    LogicalRequirementsExtractor,
)
from .data.logic.types import Chapter
from .items import (
    CHARACTERS_AND_VEHICLES_BY_NAME,
    LegoStarWarsTCSItem,
)
from .item_classification import evaluate_effective_item
from .item_groups import ability_to_readable_group
from .legacy_true_jedi import (
    DIFFICULT_OR_IMPOSSIBLE_TRUE_JEDI,
)
from .locations import LegoStarWarsTCSShopLocation
from .options import ChapterUnlockRequirement, GoalChapterLocationsMode, LogicDifficulty

if TYPE_CHECKING:
    from . import LegoStarWarsTCSWorld
else:
    LegoStarWarsTCSWorld = object


_PROGRESSIVE_SCORE_MULTIPLIER_NAME = NonDataItemName.PROGRESSIVE_SCORE_MULTIPLIER.value


__all__ = [
    "create_item_pool"
]

# Always pick CAN_ abilities last to avoid picking very boring characters at the start with basically no
# actual abilities.
# Always pick VEHICLE_BLASTER last to avoid picking a VEHICLE_BLASTER, and then picking a VEHICLE_TOW that
# also has VEHICLE_BLASTER.
ABILITY_PICK_ORDER = {
    **dict.fromkeys(~CharacterAbility.NONE, 0),
    CharacterAbility.CAN_MELEE: 1,
    CharacterAbility.CAN_RIDE_VEHICLES: 1,
    CharacterAbility.CAN_JUMP_HEIGHT_0_37: 1,
    CharacterAbility.CAN_PULL_LEVERS: 1,
    CharacterAbility.CAN_PUSH_OBJECTS: 1,
    CharacterAbility.CAN_BUILD_BRICKS: 1,
    CharacterAbility.VEHICLE_BLASTER: 1,
    **dict.fromkeys(CHAPTER_SPECIFIC_FLAGS, 2),
}
BASE_ABILITY_COSTS = {
    CharacterAbility.SITH: 10,
    CharacterAbility.BOUNTY_HUNTER: 10,
    CharacterAbility.ASTROMECH_PANEL: 8,
    CharacterAbility.SHORTIE: 8,
    CharacterAbility.HIGH_JUMP: 8,
    CharacterAbility.HOVER: 7,
    CharacterAbility.IMPERIAL: 6,
    CharacterAbility.CAN_WEAR_HAT: 0,
    CharacterAbility.JEDI: 2,
    CharacterAbility.BLASTER: 2,
    CharacterAbility.CAN_MELEE: 1,
    CharacterAbility.CAN_RIDE_VEHICLES: 1,
    CharacterAbility.CAN_JUMP_HEIGHT_0_37: 1,
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


class ItemCreator:
    _classification_lookup: dict[str, ItemClassification]
    _abilities_lookup: dict[str, CharacterAbility]
    _world: LegoStarWarsTCSWorld
    logically_relevant_item_counts: Counter[str]
    logically_relevant_abilities: CharacterAbility

    def __init__(self, world: LegoStarWarsTCSWorld):
        """
        Create a class to help in create items in a performant manner, while stripping starting abilities from the
        created items.
        :param world: The world the created items will belong to.
        """
        self._world = world
        self._initialize_effective_data_lookups()

    def _initialize_effective_data_lookups(self) -> None:
        """
        Pre-calculate the effective character abilities and classification of each item, so that the creation of items
        with multiple copies can be sped up.
        """
        world = self._world
        # UT may have disconnected entrances for Deferred Events support.
        starting_state = CollectionState(world.multiworld, allow_partial_entrances=world.is_universal_tracker())
        if world.is_universal_tracker():
            # Remove starting items so that Universal Tracker does not remove abilities or demote the classification of
            # items based on starting inventory that UT is going to discard before re-creating by calling
            # world.create_item() as the starting inventory items are received from the AP server.
            for item in world.multiworld.precollected_items[world.player]:
                starting_state.remove(item)
            # starting_state.prog_items[world.player].clear()
        requirements_extractor = LogicalRequirementsExtractor(starting_state)
        max_requirements = LogicalRequirementsExtractor.Requirements()
        # todo?: Improvements could be made here because not all entrances to access a region need to be used.
        #  Currently, the logic considers all, but some entrances could be accessible with only the starting items.
        for spots in (world.get_locations(), world.get_entrances()):
            for spot in spots:
                if spot.access_rule(starting_state):
                    # The rule can be satisfied with just the starting state.
                    continue
                requirements = requirements_extractor.extract_requirements(spot.access_rule)
                max_requirements |= requirements
        completion_condition = world.multiworld.completion_condition[world.player]
        assert isinstance(completion_condition, Rule.Resolved), "Completion condition should always be a Rule.Resolved"
        completion_requirements = requirements_extractor.extract_requirements(completion_condition)
        max_requirements |= completion_requirements

        missing_abilities = max_requirements.abilities
        missing_item_counts = max_requirements.item_counts

        # Special handling for Super Gonk collect() override.
        super_gonk_droid_collect_name = CHARACTER_TO_ITEM_DATA[Character.EVENT_SUPER_GONK_DROID].name
        if missing_item_counts[super_gonk_droid_collect_name] > 0:
            if world.options.logic_difficulty.normal_plus:
                # Gonk Droid and Super Gonk are unique items where having more than 1 would never be relevant, so there
                # is no need to check the existing counts because they should always be either 0 or 1.
                missing_item_counts[SENDABLE_CHARACTER_TO_ITEM_DATA[Character.GONK_DROID].name] = 1
                missing_item_counts[ExtraData.from_extra(Extra.SUPER_GONK).name] = 1
            else:
                # Extras (besides Score Multipliers) are not considered by logic on the Base logic, so
                # EVENT_SUPER_GONK_DROID will never be collected into a state.
                del missing_item_counts[super_gonk_droid_collect_name]

        # Abilities that are already provided by the starting inventory, or are not relevant to logic with this world's
        # options do not need to be provided by created items, potentially changing the effective classifications of
        # the items.
        logically_irrelevant_abilities = ~missing_abilities

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
            classification, effective_abilities = evaluate_effective_item(
                self._world, item, effective_character_abilities, missing_item_counts)
            effective_item_classifications[item] = classification
            # Unless generating under Universal Tracker, where all abilities are retained, the returned
            # `effective_abiltiies` should be the same as what was in `effective_character_abilities`.
            # The returned `effective_abiltiies` is not actually needed here, but `effective_character_abilities` is not
            # always available when `evaluate_effective_item()` is called.
            assert (self._world.is_universal_tracker()
                    or effective_abilities is effective_character_abilities.get(item, CharacterAbility.NONE))
            effective_item_abilities[item] = effective_abilities

        self._classification_lookup = effective_item_classifications
        self._abilities_lookup = effective_item_abilities
        self.logically_relevant_abilities = missing_abilities
        self.logically_relevant_item_counts = missing_item_counts
        assert world.effective_character_abilities is None, "world.effective_character_abilities is already set"
        world.effective_character_abilities = effective_character_abilities
        assert world.logical_item_counts is None, "world.logical_item_counts is already set"
        world.logical_item_counts = missing_item_counts

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


def _determine_chapters(world: LegoStarWarsTCSWorld) -> tuple[set[Area], set[Area]]:
    """
    Return the set of chapter Areas that have locations, and the set of chapter Areas that have non-excluded locations.
    """
    chapters_with_locations: set[Area]
    chapters_with_non_excluded_locations: set[Area]
    if world.goal_chapter is not None:
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


# todo?: Return a set[GenericCharacterData] instead because each GenericCharacterData has .character?
def _create_possible_pool(world: LegoStarWarsTCSWorld) -> dict[Character, GenericCharacterData]:
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
    vehicle_chapters_enabled = not VEHICLE_CHAPTERS.isdisjoint(world.enabled_chapters)

    possible_pool_character_items = {char: data for char, data in SENDABLE_CHARACTER_TO_ITEM_DATA.items()
                                     if (vehicle_chapters_enabled or data.item_type != "Vehicle")}
    if (world.goal_chapter is not None
            and world.options.goal_chapter_locations_mode == GoalChapterLocationsMode.option_removed):
        # Vehicle chapters could be disabled for normal chapters, but the goal chapter could be a vehicle chapter,
        # so the vehicles required for the goal chapter need to be forced into the item pool.
        for character in sorted(world.goal_chapter.get_story_characters()):
            if character not in possible_pool_character_items:
                possible_pool_character_items[character] = SENDABLE_CHARACTER_TO_ITEM_DATA[character]
    # Anakin's Flight could be enabled, but without any Vehicle chapters enabled. In that case, ensure it is beatable by
    # adding its story characters (Naboo Starfighter) to the possible pool.
    if not vehicle_chapters_enabled and Area.ANAKINSFLIGHT in world.enabled_bonuses:
        for character in sorted(Area.ANAKINSFLIGHT.get_story_characters()):
            if character not in possible_pool_character_items:
                possible_pool_character_items[character] = SENDABLE_CHARACTER_TO_ITEM_DATA[character]

    return possible_pool_character_items


def _get_chapter_completion_ability_requirements(
        world: LegoStarWarsTCSWorld,
        chapter: Chapter
) -> set[CharacterAbility]:
    area = chapter.area

    start_region = world.get_region(area.prefix_name(chapter.start_region))
    completion_region = world.get_region(area.prefix_name("Chapter Completion"))

    path: list[Entrance] = []
    if chapter.intended_completion_path:
        difficulty = world.options.logic_difficulty
        if difficulty == LogicDifficulty.option_hard:
            path_priority = ("hard", "moderate", "normal", "base")
        elif difficulty == LogicDifficulty.option_moderate:
            path_priority = ("moderate", "normal", "base")
        elif difficulty == LogicDifficulty.option_normal:
            path_priority = ("normal", "base")
        elif difficulty == LogicDifficulty.option_none:
            path_priority = ("base",)
        else:
            raise ValueError(f"Unknown logic difficulty: {difficulty}")
        for path_key in path_priority:
            if path_key in chapter.intended_completion_path:
                completion_path = chapter.intended_completion_path[path_key]
                break
        else:
            raise ValueError(f"Could not find any logic difficulty out of {path_priority} in"
                             f" {chapter.intended_completion_path}")
        # Trust that the path visits every logically required region.
        ignore_can_reach_region = True
        current_region = start_region
        already_visited: dict[str, Region] = {area.prefix_name(chapter.start_region): start_region}
        for internal_region_name in completion_path:
            region_name = area.prefix_name(internal_region_name)
            if region_name in already_visited:
                # Jump back to an already visited region.
                current_region = already_visited[region_name]
                continue
            exit_: Entrance
            for exit_ in current_region.exits:
                connected_region = exit_.connected_region
                if connected_region is None:
                    raise Exception(f"Entrance {exit_} has no connected region.")
                if connected_region.name == region_name:
                    current_region = connected_region
                    already_visited[connected_region.name] = connected_region
                    path.append(exit_)
                    break
            else:
                raise Exception(f"Could not find the entrance connecting {current_region.name} to {region_name}")
    else:
        ignore_can_reach_region = False
        reverse_path: list[Entrance] = []
        current_region = completion_region
        while current_region:
            entrances = current_region.entrances
            if len(entrances) != 1:
                raise ValueError(f"Expected 1 entrance connecting to {current_region}, but got {list(entrances)}")
            current_region = entrances[0].parent_region
            if current_region is None:
                raise Exception(f"Entrance {entrances[0]} has no parent region.")
            reverse_path.append(entrances[0])
            if current_region == start_region:
                break
        path = list(reversed(reverse_path))

    extractor = CNFAbilityRequirementsExtractor(ignore_can_reach_region)
    extra_chapter_entrance_rule = chapter.extra_entrance_rules.resolve(world)
    extra_entrance_requirements = extractor.extract_ability_requirements(extra_chapter_entrance_rule)
    if extra_entrance_requirements is None:
        raise Exception(f"No valid extra_entrance_rules ability requirements for {chapter.name}")
    and_has_any_abilities: set[CharacterAbility] = extra_entrance_requirements

    for entrance in path:
        rule = entrance.access_rule
        if not isinstance(rule, Rule.Resolved):
            raise Exception(f"Entrance {entrance} does not have a Rule Builder rule set.")
        entrance_and_has_any_abilities = extractor.extract_ability_requirements(rule)
        if entrance_and_has_any_abilities is None:
            raise Exception(f"Entrance {entrance} does not have any ability-only requirements that satisfy it.")
        and_has_any_abilities.update(entrance_and_has_any_abilities)

    # Get all the abilities provided by starting characters, so that these abilities can be removed from requirements.
    starting_abilities = world.get_starting_inventory_abilities()
    expanded_starting_abilities = starting_abilities.expand_to_implied()

    # If any bits are already provided by starting characters, then the HasAnyAbilities would return True from the
    # start, so only has_any_abilities with no intersection are needed.
    and_has_any_abilities_starting_removed = {c for c in and_has_any_abilities if c & expanded_starting_abilities == 0}

    optimized_and_has_any_abilities = CharacterAbility.optimize_and_has_any_abilities(
        and_has_any_abilities_starting_removed
    )
    return CharacterAbility.convert_and_has_any_to_or_has_all(*optimized_and_has_any_abilities)


def _create_starting_characters_for_character_locked_chapters(
        world: LegoStarWarsTCSWorld,
        possible_pool_character_items: dict[Character, GenericCharacterData],
        starting_chapter_characters: list[GenericCharacterData],
        starting_chapter_required_count: int,
        starting_chapter_ability_requirements: set[CharacterAbility],
) -> set[CharacterAbility]:
    if starting_chapter_required_count > len(starting_chapter_characters):
        raise Exception(f"Too many starting_chapter_characters required for {world.starting_chapter!r}. Required"
                        f" {starting_chapter_required_count}, but only {len(starting_chapter_characters)} exist"
                        f"({starting_chapter_characters}).")
    skipped: list[GenericCharacterData]
    picked: list[GenericCharacterData]
    missing_requirements = starting_chapter_ability_requirements
    if starting_chapter_required_count == len(starting_chapter_characters):
        # All characters are needed.
        picked = starting_chapter_characters
        skipped = []
        # Update missing ability requirements.
        picked_character_abilities = reduce(or_, (character_data.abilities for character_data in picked))
        mask = ~picked_character_abilities
        missing_requirements = {c & mask for c in missing_requirements}
        if CharacterAbility.NONE in missing_requirements:
            # At least one of the HasAllAbilities has been satisfied, so the others can be discarded.
            missing_requirements = set()
        else:
            missing_requirements = CharacterAbility.optimize_or_has_all_abilities(missing_requirements)
    else:
        characters_to_pick_from = starting_chapter_characters.copy()
        world.random.shuffle(characters_to_pick_from)
        # Sort so that characters that potentially lock access to the least chapters are at the end, and are therefore
        # most likely to be picked because iteration
        characters_to_pick_from.sort(key=lambda data: world.character_chapter_access_counts[data.name], reverse=True)

        def sort_func(c: CharacterAbility) -> int:
            return sum(map(DEFAULT_ABILITY_COSTS.__getitem__, c))

        picked = []
        needed_characters = starting_chapter_required_count
        ability_requirements_by_cost = sorted(missing_requirements, key=sort_func)
        while needed_characters > 0:
            # Iteration through `ability_requirements_by_cost` restarts after picking each character with matching
            # abilities because the order of `ability_requirements_by_cost` could change.
            for has_all_abilities in ability_requirements_by_cost:
                # Iterate in reverse because popping from near the end is more efficient that popping from near the
                # start.
                for i, character_data in enumerate(reversed(characters_to_pick_from), start=1):
                    if character_data.abilities & has_all_abilities != 0:
                        # Found a character with matching abilities.
                        picked_index = -i
                        break
                else:
                    # Could not find a character with matching abilities.
                    # Continue to try the next ability requirements.
                    continue
                # Propagate the break from finding a character with matching abilities.
                break
            else:
                # No break, so not a single character was found matching any of the requirements, so just pick
                # characters the number of needed characters.
                picked_characters = characters_to_pick_from[:needed_characters]
                assert len(picked_characters) == needed_characters
                picked.extend(picked_characters)
                skipped = characters_to_pick_from[needed_characters:]
                # del characters_to_pick_from[-needed_characters:]
                # needed_characters = 0
                # Break the while loop now that all characters have been picked.
                break

            # A character with abilities matching one of the requirements was found.
            # This code could be placed within the innermost loop, but it makes the control-flow more difficult to read.
            picked_character = characters_to_pick_from.pop(picked_index)
            picked.append(picked_character)
            needed_characters -= 1

            # Update the missing requirements for the abilities of the picked character.
            abilities_mask = ~picked_character.abilities
            missing_requirements = {c & abilities_mask for c in missing_requirements}
            # Re-optimize to account for abilities that have been removed from individual has_all_abilities.
            missing_requirements = CharacterAbility.optimize_or_has_all_abilities(missing_requirements)
            if CharacterAbility.NONE in missing_requirements:
                # At least one of the HasAllAbilities has been satisfied, so the others can be discarded.
                missing_requirements = set()
                ability_requirements_by_cost = []
            else:
                ability_requirements_by_cost = sorted(missing_requirements, key=sort_func)
        else:
            skipped = characters_to_pick_from

    # TODO: Do the picked characters need to be set somewhere? Check where else world.starting_chapter is used.
    for character_data in picked:
        world.push_precollected(world.create_item(character_data.name))
        del possible_pool_character_items[character_data.character]

    for character_data in skipped:
        # The skipped characters can be considered to no longer give access to the starting chapter, which could change
        # their classifications if they get created.
        world.character_chapter_access_counts[character_data.character] -= 1
        # print(f"Reducing count of chapters locked by {character_data.name} because the starting chapter will be"
        #       f" unlocked by {picked} instead")
        assert world.character_chapter_access_counts[character_data.character] >= 0

    return missing_requirements


def create_starting_characters_for_random_character_locked_chapters(
        world: LegoStarWarsTCSWorld,
        possible_pool_character_items: dict[Character, GenericCharacterData],
        starting_chapter_ability_requirements: set[CharacterAbility],
) -> set[CharacterAbility]:
    """
    Create and precollect the characters the player should start with when chapters are locked by needing Random
    Characters.

    This tries to pick as few characters as possible, but enough such that the starting chapter can be completed.
    :param world:
    :param possible_pool_character_items:
    :param starting_chapter_ability_requirements:
    :return: Still missing starting chapter ability requirements as
    `Or(*(HasAllAbilities(abilities) for abilities in return_value))`
    """
    starting_chapter = world.starting_chapter
    required_count = world.chapter_required_character_counts[starting_chapter]
    starting_chapter_characters_data = [SENDABLE_CHARACTER_TO_ITEM_DATA[c] for c
                                        in world.chapter_random_character_requirements[starting_chapter]]

    return _create_starting_characters_for_character_locked_chapters(
        world, possible_pool_character_items, starting_chapter_characters_data, required_count,
        starting_chapter_ability_requirements)


def create_starting_characters_for_vanilla_character_locked_chapters(
        world: LegoStarWarsTCSWorld,
        possible_pool_character_items: dict[Character, GenericCharacterData],
        starting_chapter_ability_requirements: set[CharacterAbility],
) -> set[CharacterAbility]:
    """
    Create and precollect the characters the player should start with when chapters are locked by needing Vanilla
    Characters.

    This tries to pick as few characters as possible, but enough such that the starting chapter can be completed.
    :param world:
    :param possible_pool_character_items:
    :param starting_chapter_ability_requirements: Ability requirements in
    `Or(*HasAllAbilities(abilities) for abilities in starting_chapter_ability_requirements)` format.
    :return: Still missing starting chapter ability requirements as
    `Or(*(HasAllAbilities(abilities) for abilities in return_value))`.
    """
    not_required = world.options.chapter_unlock_story_characters_not_required.to_character_set()

    starting_chapter_area = world.starting_chapter
    required_count = world.chapter_required_character_counts[starting_chapter_area]

    # Add characters necessary to unlock, *and complete* the starting chapter into starting inventory.
    if starting_chapter_area in world.chapters_requiring_alt_characters:
        characters_set = starting_chapter_area.get_purchase_characters()
    else:
        characters_set = starting_chapter_area.get_story_characters()
    # The story character names are a `set`, so sort before iterating to get a deterministic iteration order.
    # Also filter out characters that have been excluded from requirements.
    characters = sorted(SENDABLE_CHARACTER_TO_ITEM_DATA[char] for char in characters_set.difference(not_required))

    return _create_starting_characters_for_character_locked_chapters(
        world, possible_pool_character_items, characters, required_count, starting_chapter_ability_requirements)


def pick_characters_to_fulfil_abilities(
        world: LegoStarWarsTCSWorld,
        abilities_to_fulfil: CharacterAbility,
        possible_pool_character_items: dict[Character, GenericCharacterData],
        abilities_to_ignore: CharacterAbility = CharacterAbility.NONE,
) -> list[GenericCharacterData]:
    # PyCharm's type checker doesn't like considering the result of the bitwise operation to be sortable.
    # noinspection PyTypeChecker
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

    individual_ability: CharacterAbility
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
        del possible_pool_character_items[picked.character]
        # PyCharm's type checker seems to be unaware that IntFlags are iterable.
        # noinspection PyTypeChecker
        fulfilled_abilities.update(picked.abilities)
        for ability in picked.abilities:
            # The ability is provided by the picked character, so it is no longer relevant for sorting future
            # picks.
            ability_costs[ability] = 0
    return picked_characters


def create_starting_characters_for_needed_starting_chapter_abilities(
        world: LegoStarWarsTCSWorld,
        possible_pool_character_items: dict[Character, GenericCharacterData],
        missing_starting_chapter_ability_requirements: set[CharacterAbility],
) -> None:
    """

    :param world:
    :param possible_pool_character_items:
    :param missing_starting_chapter_ability_requirements: Missing abilities in
    `Or(*HasAllAbilities(abilities) for abilities in missing_starting_chapter_ability_requirements)` format.
    :return:
    """
    if not missing_starting_chapter_ability_requirements:
        # No abilities are missing so there is nothing to do.
        return

    # Get the abilities the player is currently starting with.
    starting_abilities = world.get_starting_inventory_abilities()

    # Find all has_all_abilities without rare/useful abilities and prefer picking from those.
    non_rare_has_all_abilities = {
        has_all_abilities for has_all_abilities in missing_starting_chapter_ability_requirements
        if not has_all_abilities.contains_rare_and_useful_abilities()
    }
    assert all(abilities & starting_abilities == 0 for abilities in missing_starting_chapter_ability_requirements), \
    ("Missing abilities should not have any abilities in common with the starting abilities because then the abilities"
     " are not missing")
    if non_rare_has_all_abilities:
        or_has_all_abilities = non_rare_has_all_abilities
    else:
        or_has_all_abilities = missing_starting_chapter_ability_requirements

    all_abilities_and_costs = {
        has_all_abilities: sum(map(DEFAULT_ABILITY_COSTS.__getitem__, has_all_abilities))
        for has_all_abilities in or_has_all_abilities
    }
    min_cost = min(all_abilities_and_costs.values())
    bounty_hunter_cost = DEFAULT_ABILITY_COSTS[CharacterAbility.BOUNTY_HUNTER]
    # Filter out has_all_abilities much more costly than the others.
    or_has_all_abilities = {has_all_abilities for has_all_abilities, cost in all_abilities_and_costs.items()
                            if cost - min_cost < bounty_hunter_cost}

    # Compute character picks for each has_all_abilities.
    all_picks: dict[CharacterAbility, list[GenericCharacterData]] = {}
    for has_all_abilities in or_has_all_abilities:
        picked_characters = pick_characters_to_fulfil_abilities(
            world,
            has_all_abilities,
            possible_pool_character_items.copy(),
            starting_abilities,
        )
        all_picks[has_all_abilities] = picked_characters

    # Pick randomly from the abilities that produced the fewest characters.
    min_character_count = min(map(len, all_picks.values()))
    final_picks = sorted(
        ((has_all_abilities, characters) for has_all_abilities, characters in all_picks.items()
        if len(characters) == min_character_count), key=lambda t: t[0]
    )
    picked_characters = world.random.choice(final_picks)[1]

    for character_data in picked_characters:
        world.push_precollected(world.create_item(character_data.name))
        del possible_pool_character_items[character_data.character]

    updated_starting_abilities = world.get_starting_inventory_abilities()
    for has_all_abilities in missing_starting_chapter_ability_requirements:
        if has_all_abilities in updated_starting_abilities:
            # Found a has_all_abilities that has been satisfied, so the needed starting chapter abilities have been met.
            break
    else:
        missing = {has_all_abilities & ~updated_starting_abilities
                   for has_all_abilities in missing_starting_chapter_ability_requirements}
        raise Exception(f"Not all required starting chapter abilities were fulfilled. Missing"
                        f" Or(*HasAllAbilities(...) for ... in ...):\n\t{missing!r}")



def determine_item_pool_abilities(
        world: LegoStarWarsTCSWorld,
) -> ItemPoolAbilityRequirements:
    """Determine what abilities must be supplied by the item pool for all locations to be reachable with all items in
    the item pool."""

    spots: list[Location | Entrance] = [
        # Sorting is not required, but is a deterministic generation safeguard if there is a mistake that has caused
        # location/entrance creation order to become nondeterministic.
        *sorted(world.get_locations(), key=lambda loc: loc.name),
        *sorted(world.get_entrances(), key=lambda ent: ent.name),
    ]
    seen_rules: set[Rule.Resolved] = set()
    unique_rules: list[Rule.Resolved] = []
    for spot in spots:
        rule = spot.access_rule
        if rule is Location.access_rule or rule is Entrance.access_rule or rule in seen_rules:
            continue
        assert isinstance(rule, Rule.Resolved), f"{spot} is using a rule that is not using Rule Builder ({rule})"
        seen_rules.add(rule)
        unique_rules.append(rule)
    world.random.shuffle(unique_rules)

    # Get all the abilities provided by starting characters.
    starting_abilities = world.get_starting_inventory_abilities()

    required_character_abilities_including_starting = starting_abilities
    optional_character_abilities = CharacterAbility.NONE
    extractor = AbilityRequirementsExtractor(world.random)
    for rule in unique_rules:
        extracted = extractor.extract_ability_requirements(rule,
                                                           required_character_abilities_including_starting,
                                                           optional_character_abilities)
        # Update the abilities.
        required_character_abilities_including_starting = extracted[0]
        optional_character_abilities = extracted[1]

    # Get the abilities that are required, but are not provided by starting characters.
    required_character_abilities_in_pool = required_character_abilities_including_starting & ~starting_abilities

    return ItemPoolAbilityRequirements(required_character_abilities_in_pool, optional_character_abilities)


def create_item_pool(world: LegoStarWarsTCSWorld):
    # Determine how many chapter worth's of locations are enabled.
    goal_chapter_locations_excluded = (
            world.goal_chapter is not None
            and world.options.goal_chapter_locations_mode == GoalChapterLocationsMode.option_excluded
    )

    # FIXME: chapters_with_locations is unused
    chapters_with_locations, chapters_with_non_excluded_locations = _determine_chapters(world)

    possible_pool_character_items = _create_possible_pool(world)

    starting_chapter = CHAPTERS_BY_AREA[world.starting_chapter]
    starting_chapter_ability_requirements = _get_chapter_completion_ability_requirements(world, starting_chapter)
    if not starting_chapter_ability_requirements:
        raise Exception(f"Did not get any ability-only requirements for completing {starting_chapter.name}.")

    pool_required_chapter_unlock_items: list[str]
    if world.options.chapter_unlock_requirement == ChapterUnlockRequirement.option_vanilla_characters:
        chapters_unlock_with_characters = True
        pool_required_chapter_unlock_items = []

        missing_starting_ability_requirements = create_starting_characters_for_vanilla_character_locked_chapters(
            world,
            possible_pool_character_items,
            starting_chapter_ability_requirements,
        )
        # If the alt characters are created, or not all Story characters are created, there may be abilities that still
        # need to be fulfilled by additional starting characters, so
        # `create_starting_characters_for_needed_starting_chapter_abilities()` will be called even in this case.
    elif world.options.chapter_unlock_requirement == ChapterUnlockRequirement.option_random_characters:
        chapters_unlock_with_characters = True
        pool_required_chapter_unlock_items = []

        missing_starting_ability_requirements = create_starting_characters_for_random_character_locked_chapters(
            world,
            possible_pool_character_items,
            starting_chapter_ability_requirements,
        )
    elif world.options.chapter_unlock_requirement == ChapterUnlockRequirement.option_chapter_item:
        chapters_unlock_with_characters = False
        world.push_precollected(world.create_item(CHAPTER_TO_CHAPTER_UNLOCK_ITEM[world.starting_chapter]))
        pool_required_chapter_unlock_items = [
            CHAPTER_TO_CHAPTER_UNLOCK_ITEM[chapter_area] for chapter_area in sorted(world.enabled_chapters)
            if chapter_area is not world.starting_chapter]
        missing_starting_ability_requirements = starting_chapter_ability_requirements
    else:
        raise Exception(f"Unexpected Chapter Unlock Requirement {world.options.chapter_unlock_requirement}")

    create_starting_characters_for_needed_starting_chapter_abilities(
        world,
        possible_pool_character_items,
        missing_starting_ability_requirements,
    )

    # Create the starting Episode Unlock item if Episode Unlock items are required to access chapters within an Episode.
    if world.options.episode_unlock_requirement == "episode_item":
        world.push_precollected(world.create_item(f"Episode {world.starting_episode} Unlock"))

    # Determine what abilities need to be fulfilled by the item pool for all locations and entrances to be reachable, as
    # well as abilities that are not required, but could still be logically relevant.
    item_pool_ability_requirements = determine_item_pool_abilities(world)

    if chapters_unlock_with_characters:
        # Unary `+` (__pos__) creates a new Counter with counts <= 0 removed.
        level_access_character_counts = +world.character_chapter_access_counts
    else:
        level_access_character_counts = Counter()

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
        level_access_character_counts: Counter[Character],
        possible_pool_character_items: dict[Character, GenericCharacterData],
        item_pool_ability_requirements: ItemPoolAbilityRequirements,
) -> None:
    if not world.options.chapter_unlock_requirement.is_characters():
        # Specific characters are not required to access Chapters.
        return

    is_random_characters = world.options.chapter_unlock_requirement == ChapterUnlockRequirement.option_random_characters

    enabled_chapters = sorted(world.enabled_chapters)
    world.random.shuffle(enabled_chapters)

    if world.options.chapter_unlock_requirement == ChapterUnlockRequirement.option_vanilla_characters:
        excluded_story_characters = world.options.chapter_unlock_story_characters_not_required.to_character_set()
    else:
        excluded_story_characters = ()

    abilities_provided = CharacterAbility.NONE

    for chapter_area in enabled_chapters:
        if chapter_area is world.starting_chapter:
            # Characters for the starting chapter are created separately.
            continue
        if is_random_characters:
            characters = world.chapter_random_character_requirements[chapter_area]
        else:
            # Must be vanilla characters.
            if chapter_area in world.chapters_requiring_alt_characters:
                characters = sorted(chapter_area.get_purchase_characters())
            else:
                characters = sorted(chapter_area.get_story_characters().difference(excluded_story_characters))

        # Skip already created characters and excluded characters.
        for character in characters:
            assert level_access_character_counts[character] > 0
            if character not in possible_pool_character_items:
                # This character has already been created.
                continue
            char_data = SENDABLE_CHARACTER_TO_ITEM_DATA[character]
            abilities_provided |= char_data.abilities
            pool_required_characters.append(char_data)
            del possible_pool_character_items[character]

    item_pool_ability_requirements.required &= ~abilities_provided


def _append_remaining_required_characters(
        pool_required_characters: list[GenericCharacterData],
        world: LegoStarWarsTCSWorld,
        possible_pool_character_items: dict[Character, GenericCharacterData],
        item_pool_ability_requirements: ItemPoolAbilityRequirements,
) -> None:
    possible_pool_characters_data = list(possible_pool_character_items.values())
    world.random.shuffle(possible_pool_characters_data)
    # Sort preferred characters first so that they are picked in preference.
    preferred_characters = world.options.preferred_characters.value
    if preferred_characters:
        possible_pool_characters_data.sort(key=lambda char: -1 if char.name in preferred_characters else 0)

    for character_data in possible_pool_characters_data:
        if item_pool_ability_requirements.required & character_data.abilities:
            # This character satisfied at least one of the remaining required abilities.
            pool_required_characters.append(character_data)
            item_pool_ability_requirements.required &= ~character_data.abilities
            del possible_pool_character_items[character_data.character]


def prepare_extras(world: LegoStarWarsTCSWorld) -> tuple[list[str], list[str]]:
    """
    Pre-collect starting Extras and get lists of the required and non-required Extras to be included in the item pool.
    :param world: The world that is creating items.
    :return: A list of item names required to be included in the item pool and a list of item names not required to be
     included in the item pool.
    """
    # Start with all sendable Extras as possible to add to the item pool.
    possible_pool_extras = {extra.name: extra for extra in EXTRA_DATA}

    if not world.options.enable_starting_extras_locations:
        # The starting Extra purchases are vanilla, so don't include their Extras in the pool.
        for extra in PURCHASABLE_NON_POWER_BRICK_EXTRAS:
            del possible_pool_extras[extra.readable_name]

    if world.options.start_with_detectors:
        detectors = {"Minikit Detector", "Power Brick Detector"}
        assert detectors.issubset(possible_pool_extras.keys())
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
    pool_required_extras: list[str] = [_PROGRESSIVE_SCORE_MULTIPLIER_NAME] * required_score_multipliers
    non_required_extras.extend([_PROGRESSIVE_SCORE_MULTIPLIER_NAME] * non_required_score_multipliers)
    return pool_required_extras, non_required_extras


def _split_for_preferred_extras(
        non_required_extras: list[str],
        world: LegoStarWarsTCSWorld
) -> tuple[list[str], list[str]]:
    """
    Split preferred Extras into a separate list from `non_required_extras`. May return `non_required_extras` as the
    second return value if there are no preferred Extras.

    This is more complicated than it sounds because score multipliers are currently always progressive, and the player
    can specify how many score multipliers they prefer by using the non-progressive names of the score multipliers.
    :param non_required_extras: The names of all Extras items that are not required to be included in the item pool.
    :param world: The world that is creating its item pool.
    :return: A list of Extras item names, with preferred Extras sorted to the front.
    """
    preferred_extras = world.options.preferred_extras.value
    if not preferred_extras:
        return [], non_required_extras
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
                                             if extra == _PROGRESSIVE_SCORE_MULTIPLIER_NAME]
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

    # Sort preferred extras to the front by splitting the extras into two lists of preferred and non-preferred.
    preferred_extras_list = []
    non_preferred_extras_list = []
    if num_preferred_non_required_score_multipliers <= 0:
        # Simply split.
        for item in non_required_extras:
            if item in preferred_extras:
                preferred_extras_list.append(item)
            else:
                non_preferred_extras_list.append(item)
    else:
        # Pick the Progressive Score Multipliers randomly for fairness.
        picked_preferred_score_multiplier_indices = world.random.sample(non_required_score_multiplier_indices,
                                                                        num_preferred_non_required_score_multipliers)
        for i, item in enumerate(non_required_extras):
            if item in preferred_extras:
                preferred_extras_list.append(item)
            elif item == _PROGRESSIVE_SCORE_MULTIPLIER_NAME and i in picked_preferred_score_multiplier_indices:
                preferred_extras_list.append(item)
            else:
                non_preferred_extras_list.append(item)
    return preferred_extras_list, non_preferred_extras_list


def _sort_for_preferred_extras(non_required_extras: list[str], world: LegoStarWarsTCSWorld) -> list[str]:
    """
    Sort preferred Extras to the front of `non_required_extras`. May run in-place on non_required_extras.

    This is more complicated than it sounds because score multipliers are currently always progressive, and the player
    can specify how many score multipliers they prefer by using the non-progressive names of the score multipliers.
    :param non_required_extras: The names of all Extras items that are not required to be included in the item pool.
    :param world: The world that is creating its item pool.
    :return: A list of Extras item names, with preferred Extras sorted to the front.
    """
    preferred, non_preferred = _split_for_preferred_extras(non_required_extras, world)
    return preferred + non_preferred


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

def _find_required_items_for_full_access(
        world: LegoStarWarsTCSWorld,
        item_creator: ItemCreator,
        current_item_pool: list[LegoStarWarsTCSItem],
        non_required_characters: list[GenericCharacterData],
        non_required_extras: list[str],
) -> list[LegoStarWarsTCSItem]:
    """
    Return a near-minimal list of items that need to be added to the multiworld item pool to ensure that all locations
    are reachable.
    :param world:
    :param item_creator:
    :param current_item_pool:
    :param non_required_characters:
    :param non_required_extras:
    :return:
    """
    return _find_required_items_for_access(
        world, item_creator, current_item_pool, non_required_characters, non_required_extras, world.get_locations()
    )

# This is not currently used because characters are currently always picked until all logically relevant abilities are
# supplied by the pool, and almost all locations are always accessible with just the logically relevant abilities.
def _find_required_items_for_minimal_access(
        world: LegoStarWarsTCSWorld,
        item_creator: ItemCreator,
        current_item_pool: list[LegoStarWarsTCSItem],
        non_required_characters: list[GenericCharacterData],
        non_required_extras: list[str],
) -> list[LegoStarWarsTCSItem]:
    """
    Return a near-minimal list of items that need to be added to the multiworld item pool to ensure that the goal is
    reachable.
    :param world:
    :param item_creator:
    :param current_item_pool:
    :param non_required_characters:
    :param non_required_extras:
    :return:
    """
    # Goal location changes name depending on goal chapter if a goal chapter is set. For ease of compatibility, just
    # iterate through the locations to find the "Victory" event.
    # todo: Store the name of the victory location as an instance attribute on the world, or store the Victory event
    #  item, whose `.location` can be used to get the victory location.
    victory = [loc for loc in world.get_locations()
               if (item := loc.item) is not None and item.name == "Victory" and item.is_event]
    if len(victory) != 1:
        raise Exception(f"Expected 1 Victory location, but got {victory}")
    return _find_required_items_for_access(
        world, item_creator, current_item_pool, non_required_characters, non_required_extras, victory
    )

def _find_required_items_for_access(
        world: LegoStarWarsTCSWorld,
        item_creator: ItemCreator,
        current_item_pool: list[LegoStarWarsTCSItem],
        available_characters: list[GenericCharacterData],
        available_extras: list[str],
        access_locations: Iterable[Location],
) -> list[LegoStarWarsTCSItem]:
    # - first produce a state with all the currently required items.
    starting_pool_state = CollectionState(world.multiworld)
    for item in current_item_pool:
        if item.advancement:
            starting_pool_state.collect(item, prevent_sweep=True)
    # fixme: Score multipliers should already be determined as required?
    # # - create and collect score multipliers as specified in item_creator.logically_relevant_item_counts because there
    # # are no alternatives for rules that require score multipliers.
    # new_pool_items = []
    # score_multiplier_name = NonDataItemName.PROGRESSIVE_SCORE_MULTIPLIER.value
    # relevant_multipliers = item_creator.logically_relevant_item_counts[score_multiplier_name]
    # multipliers_to_create = starting_pool_state.count(score_multiplier_name, world.player) - relevant_multipliers
    # for _ in range(multipliers_to_create):
    #     score_multiplier_item = item_creator.create_item(score_multiplier_name)
    #     new_pool_items.append(score_multiplier_item)
    #     starting_pool_state.collect(score_multiplier_item, prevent_sweep=True)
    # - sweep the state to use it as a base state
    locations_to_sweep = {loc for loc in world.get_locations() if loc.advancement}
    starting_pool_state.sweep_for_advancements(locations_to_sweep)
    locations_to_sweep.difference_update(starting_pool_state.advancements)
    # - find all unreachable locations, these will need to become reachable by items that will be added to the item
    # pool, either directly, or indirectly by being able to pick up events
    unreachable_with_starting_pool = [
        loc for loc in access_locations
        if (loc.advancement and loc not in starting_pool_state.advancements) or not loc.can_reach(starting_pool_state)
    ]
    if not unreachable_with_starting_pool:
        # Every location is reachable already, so no additional items need to be created.
        return []

    required_locations_to_sweep = locations_to_sweep.intersection(access_locations)

    # - filter out non-required extras/characters that are not in item_creator.logically_relevant_item_counts
    # - extract preferred non-required extras and preferred non-required characters into their own list and shuffle
    logically_relevant_counts = +item_creator.logically_relevant_item_counts
    preferred_characters = world.options.preferred_characters.value
    filtered_non_required_characters: list[str] = []
    preferred_filtered_non_required_characters: list[str] = []
    for character in available_characters:
        character_name = character.name
        if character_name in logically_relevant_counts and not starting_pool_state.has(character_name, world.player):
            if character_name in preferred_characters:
                preferred_filtered_non_required_characters.append(character_name)
            else:
                filtered_non_required_characters.append(character_name)
    # Logically relevant Score Multipliers should always be required, so filter them out for simplicity.
    filtered_available_extras = [
        extra for extra in available_extras if extra != NonDataItemName.PROGRESSIVE_SCORE_MULTIPLIER.value
    ]
    preferred_non_required_extras, non_preferred_non_required_extras = _split_for_preferred_extras(
        filtered_available_extras, world)
    non_preferred_filtered_non_required_extras: list[str] = []
    preferred_filtered_non_required_extras: list[str] = []
    for extras, filtered_output in (
            (preferred_non_required_extras, preferred_filtered_non_required_extras),
            (non_preferred_non_required_extras, non_preferred_filtered_non_required_extras)
    ):
        for extra in extras:
            if extra in logically_relevant_counts and not starting_pool_state.has(extra, world.player):
                filtered_output.append(extra)
    # - put the remaining non-required, logically relevant extras/characters into lists and shuffle
    preferred_items = list(
        map(item_creator.create_item,
            preferred_filtered_non_required_characters + preferred_filtered_non_required_extras)
    )
    non_preferred_items = list(
        map(item_creator.create_item, filtered_non_required_characters + non_preferred_filtered_non_required_extras)
    )
    world.random.shuffle(preferred_items)
    world.random.shuffle(non_preferred_items)
    # - combine both lists, putting the list of preferred items at the start, making the potential pool
    potential_pool = preferred_items + non_preferred_items

    # - assert that with all potential pool items, all locations are reachable
    # Debug check to run on dev branch only.
    if __debug__ and not Utils.is_frozen():
        all_state = sweep_from_pool(starting_pool_state, potential_pool, locations_to_sweep)
        still_unreachable = [loc for loc in unreachable_with_starting_pool if not loc.can_reach(all_state)]
        if still_unreachable:
            raise Exception(f"Item pool all-state could not reach locations: {sorted(still_unreachable)}")


    # - collect one item at a time (and sweep uncollected pre-placed) until all locations are reached
    #   (can see when to `locations_to_sweep_copy -= state.advancements` when state.advancements changes in length)
    locations_maybe_still_unreachable = unreachable_with_starting_pool.copy()
    sweep_locations_maybe_still_unreachable = locations_to_sweep.copy()
    available_items = list(reversed(potential_pool))
    current_pool_picks = []
    collecting_state = starting_pool_state.copy()
    while locations_maybe_still_unreachable and available_items:
        loc = locations_maybe_still_unreachable.pop()
        if not loc.can_reach(collecting_state):
            item_to_collect = available_items.pop()
            current_pool_picks.append(item_to_collect)
            collecting_state.collect(item_to_collect, prevent_sweep=True)
            # If there are still locations to sweep, sweep them.
            if sweep_locations_maybe_still_unreachable:
                advancements_before = len(collecting_state.advancements)
                collecting_state.sweep_for_advancements(sweep_locations_maybe_still_unreachable)
                # If the number of advancements changed by the sweep, then update the locations to sweep.
                if len(collecting_state.advancements) != advancements_before:
                    sweep_locations_maybe_still_unreachable.difference_update(collecting_state.advancements)
            # Append the unreachable location back onto the end to try again next.
            locations_maybe_still_unreachable.append(loc)
        else:
            # The location is reachable, so collect the item if there is one and it is advancement.
            placed_item = loc.item
            if placed_item is not None and placed_item.advancement:
                collecting_state.collect(placed_item, prevent_sweep=True, location=loc)
    # The state has reached all pre-placed advancements, so the expected count of advancements can be compared when
    # all advancements are required to be reached.
    all_advancements_required = required_locations_to_sweep == locations_to_sweep
    expected_all_advancements_count = len(collecting_state.advancements)

    # - with only the items that were collected in order to reach all locations, begin a binary search for items that
    # are required, 'peeling off' items towards the end of the list first so that items towards the front (those which
    # are preferred by the player) are most likely to be picked as required.
    # todo: Can we create spheres, then copy the code from my playthrough calculation update that allows carried over
    #  locations? The big difference is that most of the locations won't have items placed at them.
    # todo: Binary search to eliminate items from being required might be faster.
    required_pool_picks = []
    non_advancements_to_check_reachable = [loc for loc in unreachable_with_starting_pool if not loc.advancement]
    while current_pool_picks:
        test_skip = current_pool_picks.pop()
        test_state = sweep_from_pool(starting_pool_state, current_pool_picks + required_pool_picks, locations_to_sweep)
        if all_advancements_required and len(test_state.advancements) != expected_all_advancements_count:
            # One of the pre-placed advancements was not reachable, so the item is required to be in the item pool.
            required_pool_picks.append(test_skip)
        for loc in non_advancements_to_check_reachable:
            if not loc.can_reach(test_state):
                # One of the non-advancement locations was not reachable
                required_pool_picks.append(test_skip)
                break

    # - assert that with all the items to add to the pool, all locations are reachable
    # Debug check to run on dev branch only.
    if __debug__ and not Utils.is_frozen():
        all_state = sweep_from_pool(starting_pool_state, required_pool_picks, locations_to_sweep)
        still_unreachable = [loc for loc in unreachable_with_starting_pool if not loc.can_reach(all_state)]
        if still_unreachable:
            raise Exception(f"Item pool full-accessibility-satisfied-state could not reach locations:"
                            f" {sorted(still_unreachable)}")

    return required_pool_picks



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

    # Shuffle to ensure there is randomness when picking characters/extras.
    world.random.shuffle(non_required_characters)
    world.random.shuffle(non_required_extras)

    # The abilities to reach every location are determined earlier, and required Score Multipliers and characters
    # required to unlock chapters are also determined earlier. However, it is possible that a location is not accessible
    # with just abilities (and characters to unlock chapters), so any additional characters/extras necessary to reach
    # these locations need to be added to the item pool.
    # todo: Try finding all item pool required items this way; it might be too slow.
    required_for_full_access = _find_required_items_for_full_access(
        world, item_creator, item_pool, non_required_characters, non_required_extras)
    if remaining_to_create < len(required_for_full_access):
        world.option_error("There was not enough space in the item pool to ensure that all locations are reachable."
                           " Enable more locations or reduce the requirements needed to access levels.")
    for item in required_for_full_access:
        add_to_pool(item)

    required_for_full_access_item_names = {item.name for item in required_for_full_access}
    # Characters and Extras (aside from Progressive Score Multipliers) are unique items.
    assert len(required_for_full_access_item_names) == len(required_for_full_access), \
        "No duplicates should be in the required items for full accessibility"

    # todo: There might be a need to subtract from Extra reserved counts if too many characters are needed, or vice
    #  versa.
    # item_deficit = 0
    reserved_non_required_character_count = item_location_counts.reserved_non_required_character
    before_length = len(non_required_characters)
    non_required_characters = [
        data for data in non_required_characters if data.name not in required_for_full_access_item_names
    ]
    reserved_non_required_character_count -= (before_length - len(non_required_characters))
    if reserved_non_required_character_count < 0:
        # item_deficit += -reserved_non_required_character_count
        reserved_non_required_character_count = 0

    reserved_non_required_extras_count = item_location_counts.reserved_non_required_extra
    before_length = len(non_required_extras)
    non_required_extras = [extra for extra in non_required_extras if extra not in required_for_full_access_item_names]
    reserved_non_required_extras_count -= (before_length - len(non_required_extras))
    if reserved_non_required_extras_count < 0:
        # item_deficit += -reserved_non_required_extras_count
        reserved_non_required_extras_count = 0


    # Sort preferred characters first so that they are picked in preference.
    preferred_characters = world.options.preferred_characters.value
    if preferred_characters:
        non_required_characters.sort(key=lambda char: -1 if char.name in preferred_characters else 0)

    # Create as many non-required characters as there are reserved character locations.
    required_excludable_count = item_location_counts.required_excludable
    picked_chars = non_required_characters[:reserved_non_required_character_count]
    leftover_chars = non_required_characters[reserved_non_required_character_count:]
    for char in picked_chars:
        item = item_creator.create_item(char.name)
        add_to_pool(item)
        if required_excludable_count > 0 and item.excludable:
            required_excludable_count -= 1

    # Create as many non-required extras as there are reserved power brick locations.
    # Sort preferred Extras first so that they are picked in preference.
    non_required_extras = _sort_for_preferred_extras(non_required_extras, world)

    picked_extras = non_required_extras[:reserved_non_required_extras_count]
    leftover_extras = non_required_extras[reserved_non_required_extras_count:]
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
        level_access_character_counts: Counter[Character],
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
    #  For this, it will probably be necessary to count how many times each character is relevant to a rule (both
    #  directly and also indirectly through its abilities), with some scaling based on how many characters satisfy that
    #  rule. Alternatively, hardcoding for some more obvious cases, e.g. Droideka, General Grievous and
    #  Yoda/Yoda (Ghost).
    # Give deprioritized + skip_balancing to characters with only common abilities, and that do not give access to
    # levels.
    non_level_access_character_items: list[LegoStarWarsTCSItem] = []
    non_deprioritize_ability_counts: Counter[CharacterAbility] = Counter()
    level_access_character_item_name_counts: Counter[str] = Counter(
        {
            SENDABLE_CHARACTER_TO_ITEM_DATA[k].name: v for k, v in level_access_character_counts.items()
        }
    )
    for item in item_pool:
        if item.advancement and item.name in CHARACTERS_AND_VEHICLES_BY_NAME:
            if ItemClassification.progression_deprioritized_skip_balancing in item.classification:
                # Don't count abilities from characters that are already deprioritized + skip_balancing.
                continue
            abilities = item.abilities
            if abilities:
                # PyCharm's type checker misses that CharacterAbility is Iterable[CharacterAbility].
                # noinspection PyTypeChecker
                non_deprioritize_ability_counts.update(abilities)
            if chapters_unlock_with_characters:
                # FIXME: Remove the level_access_character_item_name_counts check now that precise logical amounts are
                #  determined.
                if level_access_character_item_name_counts[item.name] == 0 and world.logical_item_counts[item.name] < 1:
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
            item.classification |= ItemClassification.progression_deprioritized_skip_balancing
            if abilities:
                # Reduce the remaining ability counts from non-deprioritized characters
                # PyCharm's type checker misses that CharacterAbility is Iterable[CharacterAbility].
                # noinspection PyTypeChecker
                non_deprioritize_ability_counts.subtract(abilities)
    assert all(ability.bit_count() == 1 for ability in non_deprioritize_ability_counts)


def _create_universal_tracker_item_pool(world: LegoStarWarsTCSWorld) -> list[LegoStarWarsTCSItem]:
    """
    Universal Tracker discards the item pool for the most part, it needs it to know what item names to try in
    the `/next_progression` client command.

    We don't create the full item pool when generating under Universal Tracker because of a couple of issues:
    1. Non-required, but logically relevant, characters are randomly chosen, so each Universal Tracker generation
       could create different non-required characters, some of which may not even exist in the multiworld that UT
       is connected to. Similarly, some characters may exist in the multiworld, but not be created during UT's
       generation, so `/next_progression` would miss these items.
    2. In rare cases, due to Universal Tracker integration assuming there are no starting abilities, some
       characters who would normally have all their abilities removed, and become non-progression, could become
       progression when generating with Universal Tracker, and it might not be possible to fit all the progression
       items into the pool if there are more than expected.

    Instead of creating non-required, but logically relevant characters, events are created for each logically
    relevant CharacterAbility, whose names match the Item Group names for characters with those abilities.
    :return: The created item pool for Universal Tracker.
    """
    item_creator = ItemCreator(world)

    item_pool: list[LegoStarWarsTCSItem] = []

    # Append an event for each logically relevant ability. These events are created instead of creating one of every
    # possibly logically relevant character. The event names match the Item Groups.
    for ability in item_creator.logically_relevant_abilities:
        item = world.create_item(ability_to_readable_group(ability))
        assert item.advancement
        item_pool.append(item)

    # Append each logically relevant non-event item.
    non_event_items = world.item_name_to_id
    for item_name, count in item_creator.logically_relevant_item_counts.items():
        if count < 1 or item_name not in non_event_items:
            continue
        item = item_creator.create_item(item_name)
        assert item.advancement
        item_pool.append(item)

    return item_pool


def _create_items(
        world: LegoStarWarsTCSWorld,
        level_access_character_counts: Counter[Character],
        possible_pool_character_items: dict[Character, GenericCharacterData],
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
        return _create_universal_tracker_item_pool(world)

    item_creator = ItemCreator(world)

    # These abilities are provided by the starting characters, so these abilities can be stripped from other
    # characters, improving logic performance.
    world.starting_character_abilities = item_pool_ability_requirements.starting

    # The abilities that need to be fulfilled by the item pool, retrieved, before modification, to double-check that all
    # required abilities are accounted for.
    required_abilities_to_fulfil = item_pool_ability_requirements.required

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

    assert item_pool_ability_requirements.required is CharacterAbility.NONE, \
           "There are required abilities remaining that have not been fulfilled."
    assert required_abilities_to_fulfil in reduce(
        or_, (data.abilities for data in pool_required_characters), CharacterAbility.NONE), \
        "The required abilities are not a subset of the abilities of the required characters."

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
