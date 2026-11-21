from collections import Counter
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from BaseClasses import Region, LocationProgressType, Location
from rule_builder.rules import Rule, Has, True_, CanReachLocation, And, HasAll, HasFromListUnique

from .character_ability import CharacterAbility
from .constants import GOLD_BRICK_EVENT_NAME

from .data.areas import Area, PURCHASABLE_NON_POWER_BRICK_EXTRAS, VEHICLE_CHAPTERS, EPISODE_AREA_LOOKUP
from .data.bosses import Boss
from .data.characters import UnlockMethod, Character
from .data.items.all_character_items import NORMAL_CHARACTER_TO_ITEM_DATA
from .data.items.character_items import NON_VEHICLE_NORMAL_CHARACTER_TO_ITEM_DATA
from .data.items.generic_items import NonDataItemName, EPISODE_UNLOCKS, CHAPTER_TO_CHAPTER_UNLOCK_ITEM
from .data.items import GenericCharacterData
from .data.logic import CHAPTERS_BY_AREA
from .data.logic.gold_brick_bonuses import GOLD_BRICK_BONUSES
from .data.logic.option_filters import ut_glitched_rule
from .data.logic.types import ExitData, Chapter, GoldBrickBonus, LogicArea
from .data.shop import UNLOCK_REQUIREMENT_TO_CHARACTERS
from .options import (
    GoalChapterLocationsMode,
    ChapterUnlockRequirement,
    EpisodeUnlockRequirement,
    MinikitGoalCompletionMethod,
)
from . import legacy_true_jedi

if TYPE_CHECKING:
    from . import LegoStarWarsTCSWorld as TCSWorld
else:
    TCSWorld = object


@dataclass
class _RidableData:
    area: Area
    region: Region
    entrance_rule: Rule


@dataclass
class _RegionBuilder:
    """Small helper to store some data while creating regions."""

    world: TCSWorld
    """The world to create regions for."""

    available_minikits_check: int = 0
    """Double check that the minikit counts is as expected."""

    cantina: Region = field(init=False)
    """The origin region of the world, the Cantina."""

    story_character_unlock_regions: dict[Character, list[Region]] = field(default_factory=dict)
    """A dict mapping story characters by the regions that would unlock that character in vanilla."""

    ridable_character_regions: dict[Character, list[_RidableData]] = field(default_factory=dict)
    """A dict mapping ridable character names by the regions that feature that character."""

    goal_requires_area_completion: bool = field(init=False)
    """Whether the goal requires completing areas."""

    ut_deferred_events: bool = field(init=False)
    """Whether UT Deferred Events are enabled."""

    def __post_init__(self) -> None:
        # Create the origin region.
        self.cantina = self.world.create_region(self.world.origin_region_name)

        self.goal_requires_area_completion = self.world.goal_area_completion_count > 0

        self.ut_deferred_events = self.world.is_universal_tracker_deferred_entrances()

    def _get_score_multiplier_rule(self, studs_cost: int) -> Rule:
        count = self.world.get_score_multiplier_requirement(studs_cost)
        if count == 0:
            return True_()
        # All purchases can be made with enough grinding for studs, it just might take a long time.
        return ut_glitched_rule(
            normal_rule=Has(NonDataItemName.PROGRESSIVE_SCORE_MULTIPLIER.value, count),
            glitched_rule=True_(),
        )

    def _add_score_multiplier_rule(self, base_rule: Rule, studs_cost: int) -> Rule:
        to_add = self._get_score_multiplier_rule(studs_cost)
        if isinstance(to_add, True_):
            return base_rule
        return to_add & base_rule

    def _add_10_minikits_gold_brick_event(self, area: Area, minikit_locations: list[Location]) -> None:
        # Minikits are generally in order of appearance within a level, so put the event in the same region as
        # the last minikit.
        event_region = minikit_locations[-1].parent_region
        assert event_region is not None
        all_minikits_loc = self.world.add_gold_brick_event(area.get_all_minikits_gold_brick_event_name(),
                                                           event_region)
        # The last minikit location is generally the furthest into the level, so construct the rule such that it checks
        # the locations in reverse.
        all_minikits_rule = And(*(CanReachLocation(loc.name) for loc in reversed(minikit_locations)))
        self.world.set_rule(all_minikits_loc, all_minikits_rule)

    def _add_ut_deferred_10_minikits_gold_brick_event(self, area: Area, minikit_locations: list[Location]) -> None:
        # Create an event in the same region, with the same rule, as each Minikit location.
        # This is a workaround for https://github.com/ArchipelagoMW/Archipelago/issues/6391.
        # The 10 minikit Gold Brick event checks CanReachLocation for all 10 minikit locations. Normally, this is
        # no problem because the rule is specified on a location, however, with Universal Tracker Deferred Events
        # enabled, the rule is moved to an Entrance, meaning that Indirect Conditions would need to be registered
        # for any regions the locations could check for access to. Rule Builder is supposed to handle this
        # automatically, but does not.
        ut_event_item_name = area.get_long_name() + " Minikit (UT Event)"
        for minikit_location in minikit_locations:
            ut_event_location_name = minikit_location.name + "(UT Event)"
            parent_region = minikit_location.parent_region
            assert parent_region is not None
            event_loc = self.world.add_event_pair(ut_event_location_name, parent_region, ut_event_item_name)
            if minikit_location.access_rule is not Location.access_rule:
                self.world.set_rule(event_loc, minikit_location.access_rule)
        # Logic performance in Universal Tracker is nowhere near as important, so the parent region of any minikit
        # location would suffice, rather than preferring a specific parent region.
        entrance_parent_region = minikit_locations[-1].parent_region
        assert entrance_parent_region is not None
        event_name = area.get_all_minikits_gold_brick_event_name()
        event_region = self.world.create_region(event_name + " (Region)")
        self.world.add_gold_brick_event(area.get_all_minikits_gold_brick_event_name(), event_region)
        # In UT deferred events, the rule is on the entrance instead of on the location.
        entrance_rule = Has(ut_event_item_name, len(minikit_locations))
        entrance = entrance_parent_region.create_exit(name=event_name)
        self.world.set_rule(entrance, entrance_rule)
        # Add the entrance and event region to the dict on the world.
        self.world.ut_disconnected_10_minikits_gold_brick_events[area] = (entrance, event_region)

    @staticmethod
    def _exclude_location(location: Location) -> None:
        location.progress_type = LocationProgressType.EXCLUDED

    def make_victory_rule(self) -> Rule:
        world = self.world
        rule = True_()

        # Minikits goal.
        if world.goal_minikit_count > 0:
            if (self.ut_deferred_events
                    and self.world.options.minikit_goal_completion_method ==
                    MinikitGoalCompletionMethod.option_junkyard_minikit_display):
                # Create a deferred event for submitting the minikits goal.
                submit_minikit_goal_event_name = "Submit Minikits at the Cantina Junkyard Minikit Display"
                minikit_goal_submitted_region = world.create_region(submit_minikit_goal_event_name + " (Region)")
                world.add_event_pair(submit_minikit_goal_event_name + " (Event Item)", minikit_goal_submitted_region)

                # Put the normal rule on the entrance to the region the deferred event is in.
                entrance = world.get_region(world.origin_region_name).create_exit(submit_minikit_goal_event_name)
                world.set_rule(entrance, Has(world.minikit_bundle_name, count=world.goal_minikit_bundle_count))

                # Make the goal rule require the deferred event.
                rule &= Has(submit_minikit_goal_event_name + " (Event Item)")

                # Set the disconnected entrance on the world.
                world.ut_minikit_goal_disconnected_entrance = (entrance, minikit_goal_submitted_region)
            else:
                rule &= Has(world.minikit_bundle_name, count=world.goal_minikit_bundle_count)

        # Bosses goal
        goal_boss_count = world.options.defeat_bosses_goal_amount.value
        if goal_boss_count > 0:
            if world.options.only_unique_bosses_count:
                bosses = {world.boss_area_to_boss[chapter] for chapter in world.enabled_bosses}
                boss_item_names = [boss.unique_event_name for boss in bosses]
                assert goal_boss_count <= len(boss_item_names)
                rule &= HasFromListUnique(*boss_item_names, count=goal_boss_count)
            else:
                rule &= Has("Boss Defeated", count=goal_boss_count)

        # Area completion goal.
        goal_area_completions = world.goal_area_completion_count
        if goal_area_completions > 0:
            # "Level" here is as a user-facing term, with the meaning of "Area" internally.
            rule &= Has("Level Completion", count=goal_area_completions)

        # Kyber Bricks Goal
        if world.options.goal_requires_kyber_bricks:
            rule &= Has("Kyber Brick", count=7)

        return rule

    def _create_chapter_entrance_rule(self, chapter: Chapter) -> tuple[Rule, set[Character], int]:
        world = self.world
        area = chapter.area
        rule = chapter.extra_entrance_rules
        characters: set[Character]
        if world.options.chapter_unlock_requirement.is_characters():
            character_count = world.chapter_required_character_counts[chapter.area]
            if world.options.chapter_unlock_requirement == ChapterUnlockRequirement.option_vanilla_characters:
                if area in world.chapters_requiring_alt_characters:
                    characters = set(area.get_purchase_characters())
                else:
                    characters = set(area.get_story_characters())
                    # Remove characters excluded from being included in requirements.
                    characters.difference_update(
                        world.options.chapter_unlock_story_characters_not_required.to_character_set())
            elif world.options.chapter_unlock_requirement == ChapterUnlockRequirement.option_random_characters:
                characters = set(world.chapter_random_character_requirements[chapter.area])
            else:
                world.raise_error(AssertionError,
                                  "Unexpected chapter unlock requirement %s",
                                  world.options.chapter_unlock_requirement)

            if len(characters) < 1:
                world.raise_error(AssertionError,
                                  "At least one character should always be required, but %s is requiring %i",
                                  area.get_long_name(), character_count)
            if len(characters) < character_count:
                world.raise_error(AssertionError,
                                  "The number of required characters should always be less than or equal to the"
                                  " available count, but %s is requiring %i characters and only has a max of %i"
                                  " available",
                                  area.get_long_name(), character_count, len(characters))

            character_names = Character.to_logic_names(characters)
            if len(characters) == character_count:
                # HasFromListUnique does not perform this optimisation automatically.
                rule &= HasAll(*character_names)
            else:
                rule &= HasFromListUnique(*character_names, count=character_count)
        else:
            rule &= Has(CHAPTER_TO_CHAPTER_UNLOCK_ITEM[area])
            characters = set()
            character_count = 0

        if world.options.episode_unlock_requirement == EpisodeUnlockRequirement.option_episode_item:
            rule &= Has(EPISODE_UNLOCKS[area.get_chapter_episode()].value)

        return rule, characters, character_count

    def _create_logic_area_regions(self, logic_area: LogicArea) -> tuple[Region, dict[str, Region]]:
        """

        :param logic_area:
        :return: The start region and dict of regions by name
        """
        area = logic_area.area

        # Regions (and finding Entrances).
        start_region_internal_name = logic_area.start_region
        start_region_exits = logic_area.regions[start_region_internal_name]
        region_data_stack: list[tuple[str, tuple[ExitData, ...]]] = [(start_region_internal_name, start_region_exits)]
        create_region = self.world.create_region
        prefix_name = area.prefix_name
        regions: dict[str, Region] = {}
        resolved_rule: Rule.Resolved
        entrances_to_create: list[tuple[Region, str, str | None, Rule | Rule.Resolved]] = []
        while region_data_stack:
            internal_region_name, exits = region_data_stack.pop()
            if internal_region_name not in regions:
                r = create_region(prefix_name(internal_region_name))
                regions[internal_region_name] = r
            else:
                # Already processed.
                continue
            for exit_ in exits:
                try:
                    resolved_rule = exit_.rule.resolve(self.world)
                    if resolved_rule.always_false:
                        continue
                    entrances_to_create.append((r, exit_.to_region, exit_.name, resolved_rule))
                except KeyError:
                    # CanReachRegion rules cannot be resolved yet if the region they reference does not exist.
                    entrances_to_create.append((r, exit_.to_region, exit_.name, exit_.rule))
                region_data_stack.append((exit_.to_region, logic_area.regions[exit_.to_region]))
        start_region = regions[start_region_internal_name]

        # Entrances.
        for r, to_region_name, entrance_name, rule in entrances_to_create:
            to_r = regions[to_region_name]
            r.connect(to_r, entrance_name, rule)

        return start_region, regions

    def _prepare_rideables_in_logic_area(self, logic_area: LogicArea, regions: dict[str, Region]) -> None:
        """Prepare rideable locations within this logic area for later creation of all rideable locations.

        Each rideable location exists only once, so everywhere that rideable character exists needs to connect to a
        region containing that singular rideable location."""
        # Locations for riding unique characters.
        if self.world.options.ridesanity:
            for rideable_character, rideable_location_data in logic_area.ridables.items():
                if isinstance(rideable_location_data, tuple):
                    rideable_location_data_tuple = rideable_location_data
                else:
                    rideable_location_data_tuple = (rideable_location_data,)
                for rideable_location_datum in rideable_location_data_tuple:
                    rideable_region = regions[rideable_location_datum.region]
                    rideable_data = _RidableData(logic_area.area, rideable_region, rideable_location_datum.rule)
                    self.ridable_character_regions.setdefault(rideable_character, []).append(rideable_data)

    def _create_chapter(self, chapter: Chapter) -> Region:
        start_region, regions = self._create_logic_area_regions(chapter)

        area = chapter.area
        world = self.world
        create_region = world.create_region

        completion_region = regions["Chapter Completion"]
        create_gold_bricks = bool(self.world.options.enable_bonus_locations)

        # Goal event.
        exclude_locations = False
        is_goal_chapter = chapter.area is world.goal_chapter
        if is_goal_chapter:
            world.add_event_pair(
                f"Complete Goal Chapter {world.goal_chapter.get_long_name()}", completion_region, "Victory")

            goal_chapter_locations_mode = world.options.goal_chapter_locations_mode.value
            if goal_chapter_locations_mode == GoalChapterLocationsMode.option_removed:
                # The only location that will be placed in the chapter's Region is the Victory event used by the
                # completion_condition.
                return start_region
            if goal_chapter_locations_mode == GoalChapterLocationsMode.option_excluded:
                # When the locations are excluded, Gold Bricks from the Goal Chapter are removed from logic.
                create_gold_bricks = False
                exclude_locations = True

        # Completion Location + Events.
        completion_name = area.get_completion_name()
        completion_location = self.world.add_location(completion_name, completion_region)

        # With Universal Tracker deferred events enabled, completion events and purchase characters are moved to a
        # region locked behind a deferred entrance.
        if self.ut_deferred_events:
            post_completion_region = create_region(completion_region.name + " (UT Deferred)")
            entrance_to_post_completion = completion_region.create_exit(completion_name + " (Event)")
            self.world.ut_disconnected_free_play_completion_events[area] = (entrance_to_post_completion,
                                                                            post_completion_region)
        else:
            post_completion_region = completion_region

        if exclude_locations:
            self._exclude_location(completion_location)
        if create_gold_bricks:
            # Completion Gold Brick event.
            world.add_gold_brick_event(area.get_completion_gold_brick_event_name(), post_completion_region)
        # Area completion.
        # The goal chapter does not contribute to Area Completion because the Goal Chapter requires completing
        # all other goals before it will unlock.
        if self.goal_requires_area_completion and not is_goal_chapter:
            # "Level" here is as a user-facing term, with the meaning of "Area" internally.
            world.add_event_pair(area.get_completion_event_name(), post_completion_region, "Level Completion")

        # True Jedi (legacy logic).
        if world.options.enable_true_jedi_locations:
            true_jedi_name = area.get_true_jedi_name()
            # With full True Jedi logic, the True Jedi location would likely end up in the start region because of score
            # multipliers when True Jedi is not set to scale with score multipliers.
            true_jedi_location = world.add_location(true_jedi_name, completion_region)
            legacy_rule = legacy_true_jedi.get_legacy_true_jedi_rule(area)
            world.set_rule(true_jedi_location, legacy_rule)
            if exclude_locations:
                self._exclude_location(true_jedi_location)
            if create_gold_bricks:
                # True Jedi Gold Brick event.
                true_jedi_event_name = area.get_true_jedi_gold_brick_event_name()
                if self.ut_deferred_events:
                    true_jedi_event_region = create_region(true_jedi_event_name + " (Region)")
                    true_jedi_event_entrance = completion_region.create_exit(true_jedi_event_name)
                    self.world.ut_disconnected_true_jedi_gold_brick_events[area] = (true_jedi_event_entrance,
                                                                                    true_jedi_event_region)
                    world.add_gold_brick_event(true_jedi_event_name, true_jedi_event_region)
                    # The rule gets placed on the entrance rather, than the location, in the case of deferred events.
                    world.set_rule(true_jedi_event_entrance, legacy_rule)
                else:
                    true_jedi_event = world.add_gold_brick_event(true_jedi_event_name, completion_region)
                    world.set_rule(true_jedi_event, legacy_rule)

        # Power Brick Location.
        extra = chapter.area.extra
        assert extra is not None
        power_brick_location_name = extra.get_purchase_location_name()
        power_brick_region = regions[chapter.power_brick.region]
        studs_cost = extra.purchase_cost
        assert studs_cost is not None
        if self.ut_deferred_events:
            extra_purchase_region = create_region(area.prefix_name("Power Brick (UT Deferred Event Region)"))
            entrance_to_extra_purchase = power_brick_region.create_exit(area.prefix_name("Power Brick (Event)"))
            # Set the Power Brick's rule on the entrance.
            world.set_rule(entrance_to_extra_purchase, chapter.power_brick.rule)
            power_brick_loc = world.add_shop_location(power_brick_location_name, extra_purchase_region, studs_cost)
            # Set the Purchase cost rule on the location.
            world.set_rule(power_brick_loc, self._get_score_multiplier_rule(studs_cost))
            self.world.ut_disconnected_power_brick_events[area] = (entrance_to_extra_purchase, extra_purchase_region)
        else:
            power_brick_loc = world.add_shop_location(power_brick_location_name, power_brick_region, studs_cost)
            world.set_rule(power_brick_loc, self._add_score_multiplier_rule(chapter.power_brick.rule, studs_cost))
        if exclude_locations:
            self._exclude_location(power_brick_loc)

        # Character Purchases in the shop.
        # Character purchases unlocked upon completing the chapter (normally in Story mode).
        purchase_characters = area.get_purchase_characters()
        for character in purchase_characters:
            location_name = character.get_purchase_location_name()
            studs_cost = character.purchase_cost
            assert studs_cost is not None
            purchase_location = world.add_shop_location(location_name, post_completion_region, studs_cost)
            world.set_rule(purchase_location, self._get_score_multiplier_rule(studs_cost))
            if exclude_locations:
                self._exclude_location(purchase_location)
        world.character_unlock_location_count += len(purchase_characters)

        # Minikits.
        minikits_from_chapter = 0
        if world.options.enable_minikit_locations:
            minikit_locations: list[Location] = []
            for minikit_name, location_data in chapter.minikits.items():
                r = regions[location_data.region]
                loc = self.world.add_location(area.prefix_name(minikit_name), r)
                self.world.set_rule(loc, location_data.rule)
                minikit_locations.append(loc)
                minikits_from_chapter += 1
            if exclude_locations:
                for loc in minikit_locations:
                    self._exclude_location(loc)
            if create_gold_bricks:
                if self.ut_deferred_events:
                    self._add_ut_deferred_10_minikits_gold_brick_event(area, minikit_locations)
                else:
                    self._add_10_minikits_gold_brick_event(area, minikit_locations)
        else:
            # If Minikit locations are disabled, but the goal requires Minikits, the Chapter Completion location
            # is instead treated as if it was the vanilla location for a 10 Minikits bundle.
            minikits_from_chapter += 10

        # The goal chapter does not contribute Minikits because it is only accessible once the Minikits goal is
        # complete.
        if not is_goal_chapter and world.options.minikit_goal_amount != 0:
            self.available_minikits_check += minikits_from_chapter

        # Story Character unlocks.
        if world.options.enable_story_character_unlock_locations:
            for character in chapter.area.get_story_characters():
                # These unlock as soon as the chapter is completed, so should not be locked behind a deferred chapter
                # completion event.
                self.story_character_unlock_regions.setdefault(character, []).append(completion_region)

        # Locations for riding unique characters (if enabled).
        self._prepare_rideables_in_logic_area(chapter, regions)

        # Boss.
        if chapter.area in world.enabled_bosses:
            assert chapter.area is not world.goal_chapter, ("The Goal Chapter should never be selected as an "
                                                              "enabled boss")
            if world.options.only_unique_bosses_count:
                boss = world.boss_area_to_boss[chapter.area]
                boss_event_item_name = boss.unique_event_name
            else:
                boss = Boss.from_area(chapter.area)
                # todo: Replace the literal with a shared global str.
                boss_event_item_name = "Boss Defeated"
            # Bosses are currently implemented in the client by requiring the chapter to be completed, so the boss event
            # can just go in `post_completion_region`.
            world.add_event_pair(
                chapter.area.get_boss_defeat_event_name(boss),
                post_completion_region,
                boss_event_item_name,
            )

        return start_region

    def _create_episode(self, episode_number: int) -> None:
        world = self.world
        episode_room = world.create_region(f"Episode {episode_number} Room")
        self.cantina.connect(episode_room, f"Episode {episode_number} Door")
        for chapter_area in EPISODE_AREA_LOOKUP[episode_number].values():
            if chapter_area not in world.enabled_chapters:
                continue
            chapter_number = chapter_area.get_chapter_number_in_episode()
            chapter = CHAPTERS_BY_AREA[chapter_area]
            chapter_start_region = self._create_chapter(chapter)

            t = self._create_chapter_entrance_rule(chapter)
            chapter_entrance_rule, characters_locking_access, character_count = t
            # Add Goal Chapter rules if this is the Goal Chapter.
            if world.goal_chapter is chapter.area:
                chapter_entrance_rule &= self.make_victory_rule()

            # Create the entrance.
            main_entrance_name = f"Episode {episode_number} Room, Chapter {chapter_number} Door"
            episode_room.connect(chapter_start_region, main_entrance_name, chapter_entrance_rule)

            # Update the counts of chapters locked by each character.
            world.character_chapter_access_counts.update(characters_locking_access)
            # Prepare the requirements for writing to the spoiler.
            sorted_character_names = sorted(c.readable_name for c in characters_locking_access)
            world.spoiler_chapter_character_requirements[chapter.short_name] = (character_count, sorted_character_names)

    def create_episodes(self) -> None:
        for episode_number in range(1, 7):
            if episode_number not in self.world.enabled_episodes:
                continue
            self._create_episode(episode_number)

    def create_story_character_unlock_locations(self) -> None:
        world = self.world

        excluded_character_locations: frozenset[Character]
        if (world.goal_chapter is not None
                and world.options.goal_chapter_locations_mode.value == GoalChapterLocationsMode.option_excluded):
            excluded_character_locations = world.goal_chapter.get_story_characters()
        else:
            excluded_character_locations = frozenset()

        for character, parent_regions in self.story_character_unlock_regions.items():
            loc_name = character.get_level_completion_unlock_location_name()
            if len(parent_regions) == 1:
                parent_region = parent_regions[0]
                # The location is only accessed from 1 region, so put the location in that region. This slightly
                # improves logic performance.
                character_location = world.add_location(loc_name, parent_region)
            else:
                # The location is accessed from multiple regions, so put the location in its own region that those
                # regions can be connected to.
                character_region = world.create_region(character.get_level_completion_unlock_location_name())
                character_location = world.add_location(loc_name, character_region)
                for parent_region in parent_regions:
                    parent_region.connect(character_region)
                # There are multiple ways this location could be reached, so enable path display in the Spoiler (when
                # Playthrough Paths are enabled in the generator's host.yaml), so that the route the Playthrough used to
                # reach the location is clear.
                world.topology_present = True
            if character in excluded_character_locations:
                # If the location can be accessed through the Goal Chapter that has excluded locations, exclude the
                # location, even if it could be accessed from elsewhere. This prevents the possibility of the Goal
                # Chapter from locking access to locations.
                character_location.progress_type = LocationProgressType.EXCLUDED
                world.goal_excluded_character_unlock_location_count += 1

        world.character_unlock_location_count += len(self.story_character_unlock_regions)

    def create_bonus_locations(self) -> None:
        world = self.world
        # Bonuses.
        bonuses = world.create_region("Bonuses")
        self.cantina.connect(bonuses, "Bonuses Door")

        # Group Bonuses by gold brick costs so that the regions requiring progressively more Gold Bricks can be
        # chained together more easily.
        gold_brick_costs: dict[int, list[GoldBrickBonus]] = {}
        for gold_brick_bonus in GOLD_BRICK_BONUSES:
            area = gold_brick_bonus.area
            if area not in world.enabled_bonuses:
                continue
            gold_bricks_required = gold_brick_bonus.gold_brick_requirement
            if gold_bricks_required == 0:
                # No Gold Bricks are required to watch the Indy Trailer, so put it in the Bonuses region directly.
                assert area is Area.LOSTTEMPLE
                world.add_location(area.get_completion_name(), bonuses)
            else:
                gold_brick_costs.setdefault(gold_bricks_required, []).append(gold_brick_bonus)

        previous_gold_brick_region = bonuses
        for gold_brick_cost, gold_brick_bonuses in sorted(gold_brick_costs.items(), key=lambda t: t[0]):
            region = world.create_region(f"{gold_brick_cost} Gold Bricks Collected")
            previous_gold_brick_region.connect(
                region, f"Collect {gold_brick_cost} Gold Bricks",
                Has(GOLD_BRICK_EVENT_NAME, gold_brick_cost),
            )
            previous_gold_brick_region = region

            for gold_brick_bonus in gold_brick_bonuses:
                start_region, regions = self._create_logic_area_regions(gold_brick_bonus)

                area = gold_brick_bonus.area
                region.connect(start_region, f"{gold_brick_cost} Gold Brick Door -> {start_region.name}")

                # Completion location.
                completion_region = regions[gold_brick_bonus.COMPLETION_REGION_NAME]
                world.add_location(area.get_completion_name(), completion_region)

                if world.options.enable_story_character_unlock_locations:
                    for character in sorted(area.get_story_characters()):
                        self.story_character_unlock_regions.setdefault(character, []).append(completion_region)
                # Note: There are currently no item requirements, e.g. Story characters, to gain access to bonus levels
                #  because it is not currently possible to lock access to the bonus levels.
                assert gold_brick_bonus.rewards_gold_brick, ("Every bonus that requires Gold Bricks to access should "
                                                             "award a Gold Brick on completion")

                if self.ut_deferred_events:
                    post_completion_region = world.create_region(area.get_completion_name() + " (UT Deferred)")
                    to_post_completion = completion_region.create_exit(area.get_completion_name() + " (Event)")
                    world.ut_disconnected_bonus_completion_events[area] = (to_post_completion, post_completion_region)
                else:
                    post_completion_region = completion_region

                # Completion Gold Brick
                world.add_gold_brick_event(area.get_completion_gold_brick_event_name(), post_completion_region)

                if self.goal_requires_area_completion:
                    # "Level" here is as a user-facing term, with the meaning of "Area" internally.
                    world.add_event_pair(area.get_completion_goal_progress_event_name(), post_completion_region,
                                         "Level Completion")

                # Locations for riding unique characters (if enabled).
                self._prepare_rideables_in_logic_area(gold_brick_bonus, regions)

        # Indiana Jones shop purchase. Unlocks in the shop after watching the Lego Indiana Jones trailer.
        if self.ut_deferred_events:
            entrance_name = Area.LOSTTEMPLE.get_completion_event_name()
            post_trailer_watch_region = world.create_region(entrance_name + " (Region)")
            entrance_to_post_watch = bonuses.create_exit(entrance_name)
            self.world.ut_disconnected_bonus_completion_events[Area.LOSTTEMPLE] = (entrance_to_post_watch,
                                                                                   post_trailer_watch_region)
        else:
            post_trailer_watch_region = bonuses
        indiana_jones_purchase = world.add_location(
            Character.INDIANA_JONES.get_purchase_location_name(), post_trailer_watch_region)
        purchase_cost = Character.INDIANA_JONES.purchase_cost
        assert purchase_cost is not None
        world.set_rule(indiana_jones_purchase, self._get_score_multiplier_rule(purchase_cost))
        world.character_unlock_location_count += 1

    def create_ridesanity_locations(self) -> None:
        world = self.world

        excluded_goal_area: Area | None
        if (world.goal_chapter is not None
                and world.options.goal_chapter_locations_mode.value == GoalChapterLocationsMode.option_excluded):
            excluded_goal_area = world.goal_chapter
        else:
            excluded_goal_area = None

        # Add the Cantina Car ridable found in the Cantina itself, it cannot be found anywhere else.
        cantina_car = Character.MAPCAR
        # todo: lazy imports for now because this rule should be defined somewhere else and then imported, instead of
        #  being defined here and cluttering up the imports in this module.
        from rule_builder.rules import Or
        from .data.logic.rules import HasAbility
        from .data.logic.macros import CAN_DAMAGE_AT_CLOSE_RANGE
        cantina_car_rule = Or(
            HasAbility(CharacterAbility.CAN_PULL_LEVERS),
            CAN_DAMAGE_AT_CLOSE_RANGE & HasAbility(CharacterAbility.CAN_BUILD_BRICKS),
        )
        del Or, HasAbility, CAN_DAMAGE_AT_CLOSE_RANGE
        # Add it to the dict of regions.
        cantina_car_data = _RidableData(Area.MAP, self.cantina, cantina_car_rule)
        self.ridable_character_regions[cantina_car] = [cantina_car_data]

        for ridable, ridable_data_list in self.ridable_character_regions.items():
            world.ridesanity_location_count += 1
            ridable_location_name = ridable.get_ridesanity_location_name()
            is_excluded_goal_chapter_location = False
            if len(ridable_data_list) == 0:
                # There is only one region where this ridable can be found, so the ridable location can go directly in
                # that region.
                ridable_data = ridable_data_list[0]

                area = ridable_data.area
                area_region = ridable_data.region
                ridable_rule = ridable_data.entrance_rule

                ridable_location = world.add_location(ridable_location_name, area_region)
                world.set_rule(ridable_location, ridable_rule)
                is_excluded_goal_chapter_location = area == excluded_goal_area
            else:
                # There are multiple regions this ridable can be found in, so create a new region just for this
                # location and connect each region this ridable is found in, to this new region.
                ridable_region = world.create_region(ridable_location_name)
                for ridable_data in ridable_data_list:
                    area = ridable_data.area
                    area_region = ridable_data.region
                    ridable_rule = ridable_data.entrance_rule

                    if area == excluded_goal_area:
                        is_excluded_goal_chapter_location = True
                    area_region.connect(ridable_region, rule=ridable_rule)
                ridable_location = world.add_location(ridable_location_name, ridable_region)

            if is_excluded_goal_chapter_location:
                # If the location can be accessed through the Goal Chapter that has excluded locations, exclude the
                # location, even if it could be accessed from elsewhere. This prevents the possibility of the Goal
                # Chapter from locking access to locations.
                ridable_location.progress_type = LocationProgressType.EXCLUDED

    def create_all_episodes_character_purchases(self) -> None:
        world = self.world
        all_episodes = world.create_region("All Episodes Unlocked")

        if world.options.all_episodes_character_purchase_requirements == "episodes_unlocked":
            entrance_rule = HasAll(*(EPISODE_UNLOCKS[i] for i in range(1, 7) if i in self.world.enabled_episodes))
            self.cantina.connect(all_episodes, "Unlock All Episodes Containing Enabled Chapters", entrance_rule)
        elif world.options.all_episodes_character_purchase_requirements == "episodes_tokens":
            entrance_rule = Has(NonDataItemName.EPISODE_COMPLETION_TOKEN, count=6)
            self.cantina.connect(all_episodes, "Collect 6 Episode Completion Tokens", entrance_rule)

        all_episodes_purchases = UNLOCK_REQUIREMENT_TO_CHARACTERS[UnlockMethod.ALL_EPISODES_COMPLETE]
        for character in all_episodes_purchases:
            purchase_cost = character.purchase_cost
            assert purchase_cost is not None
            loc = world.add_shop_location(character.get_purchase_location_name(), all_episodes, character.purchase_cost)
            world.set_rule(loc, self._get_score_multiplier_rule(purchase_cost))
        world.character_unlock_location_count += len(all_episodes_purchases)

    def create_starting_purchases(self) -> None:
        world = self.world
        starting_purchases = (Character.GONK_DROID, Character.PK_DROID)
        for character in starting_purchases:
            purchase_cost = character.purchase_cost
            assert purchase_cost is not None
            loc = world.add_shop_location(character.get_purchase_location_name(), self.cantina, character.purchase_cost)
            world.set_rule(loc, self._get_score_multiplier_rule(purchase_cost))
        world.character_unlock_location_count += len(starting_purchases)

        for extra in sorted(PURCHASABLE_NON_POWER_BRICK_EXTRAS):
            purchase_cost = extra.purchase_cost
            assert purchase_cost is not None
            loc = world.add_shop_location(extra.get_purchase_location_name(), self.cantina, purchase_cost)
            world.set_rule(loc, self._get_score_multiplier_rule(purchase_cost))
            if not world.options.enable_starting_extras_locations:
                item = world.create_item(extra.readable_name)
                loc.place_locked_item(item)
                # Marking the locations as excluded allows Universal Tracker to show the locations as unimportant.
                if item.excludable:
                    loc.progress_type = LocationProgressType.EXCLUDED

    def create_non_goal_chapter_victory(self) -> None:
        """Create the Victory event for the goal when the goal does not require completing a Goal Chapter."""
        victory = self.world.add_event_pair("Goal", self.cantina, "Victory")
        self.world.set_rule(victory, self.make_victory_rule())


def determine_random_character_requirements(
        world: TCSWorld,
) -> None:
    """
    Determine the characters that lock access to chapters when chapters are set to unlock with random characters.
    :param world:
    :return:
    """
    if world.is_universal_tracker():
        # Should already be loaded from Universal Tracker.
        if not world.chapter_random_character_requirements:
            world.raise_error(Exception, "Random Character requirements for Chapters were not loaded from "
                                         "slot_data")
    else:
        # If Bonus levels become locked by items again, then whether vehicle characters are added to the item pool
        # would also have to consider the enabled bonus levels.
        vehicle_chapters_enabled = not VEHICLE_CHAPTERS.isdisjoint(
            world.enabled_chapters | {world.goal_chapter}
        )

        if vehicle_chapters_enabled:
            characters_dict = NORMAL_CHARACTER_TO_ITEM_DATA
        else:
            characters_dict = NON_VEHICLE_NORMAL_CHARACTER_TO_ITEM_DATA

        allowed_characters = [data for data in characters_dict.values() if data.is_sendable]


        chapters = sorted(world.enabled_chapters)
        world.random.shuffle(chapters)

        pool_size = len(chapters) * world.options.chapter_unlock_random_characters_unique_per_chapter.value
        if pool_size > len(allowed_characters):
            world.log_warning("The size of the requested pool of random Characters to use in Chapter unlock"
                              " requirements was %i, but there were only %i unique Characters available, so the size of"
                              " the pool has been reduced to %i.",
                              pool_size, len(allowed_characters), len(allowed_characters))
            pool_size = len(allowed_characters)

        base_pool = allowed_characters
        world.random.shuffle(base_pool)

        extra_counts = world.chapter_extra_random_character_counts
        required_counts = world.chapter_required_character_counts
        # The counts are capped at 9 because displaying the required characters in-game gets squished and difficult to
        # read.
        character_count_per_chapter = {chapter: min(extra_counts[chapter] + required_counts[chapter], 9)
                                       for chapter in chapters}
        min_pool_size = max(character_count_per_chapter.values())
        if pool_size < min_pool_size:
            world.log_warning(
                "Increased the number of unique Characters used in Chapter unlock requirements to %i from"
                " %i because at least one Chapter needs %i Characters in its unlock requirements.",
                min_pool_size, pool_size, min_pool_size)
            pool_size = min_pool_size
        pool_size = max(min_pool_size, pool_size)
        pool = base_pool[:pool_size]

        world.log_debug("Random character pool: %s", pool)

        finished_chapter_to_characters: dict[Area, set[GenericCharacterData]] = {}

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

        world.chapter_random_character_requirements = {k: sorted(c.character for c in v) for k, v in
                                                       finished_chapter_to_characters.items()}

    for characters_list in world.chapter_random_character_requirements.values():
       for character in characters_list:
           world.character_chapter_access_counts[character] += 1



def create_regions(world: TCSWorld) -> None:
    # Chapter entrance rules need to know what characters to require, so the characters need to be determined before the
    # chapter entrances can be set along with their rules.
    if world.options.chapter_unlock_requirement == ChapterUnlockRequirement.option_random_characters:
        determine_random_character_requirements(world)

    builder = _RegionBuilder(world)

    builder.create_episodes()

    # Available minikit count is calculated in generate_early.
    if world.available_minikits != builder.available_minikits_check:
        world.raise_error(AssertionError,
                          "Available minikits in create_regions did not match. %i from generate_early and %i"
                          " from create_regions. Please report this as a bug in the apworld.",
                          world.available_minikits,
                          builder.available_minikits_check)

    if world.options.enable_bonus_locations:
        builder.create_bonus_locations()

    if world.options.enable_story_character_unlock_locations:
        if builder.story_character_unlock_regions:
            builder.create_story_character_unlock_locations()
        else:
            # Every Chapter has at least 1 Story Character, so if none exist in a generation, the locations should be
            # disabled.
            assert not builder.world.options.enable_story_character_unlock_locations

    if world.options.ridesanity:
        builder.create_ridesanity_locations()

    # 'All Episodes' character purchases.
    if world.options.enable_all_episodes_purchases:
        builder.create_all_episodes_character_purchases()

    builder.create_starting_purchases()

    # General Victory event.
    if not world.goal_chapter is not None:
        builder.create_non_goal_chapter_victory()

    # For debugging.
    # from Utils import visualize_regions
    # visualize_regions(cantina, "LegoStarWarsTheCompleteSaga_Regions.puml", show_entrance_names=True)
