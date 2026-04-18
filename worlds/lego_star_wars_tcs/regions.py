from collections import defaultdict
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from BaseClasses import Region, LocationProgressType, Location, Entrance

from .constants import GOLD_BRICK_EVENT_NAME, CharacterAbility
from .items import CHARACTERS_AND_VEHICLES_BY_NAME, SHOP_SLOT_REQUIREMENT_TO_UNLOCKS, PURCHASABLE_NON_POWER_BRICK_EXTRAS
from .levels import (
    EPISODE_TO_CHAPTER_AREAS,
    CHAPTER_AREA_STORY_CHARACTERS,
    BonusArea,
    BONUS_AREAS,
    SHORT_NAME_TO_CHAPTER_AREA,
)
from .options import GoalChapterLocationsMode, ChapterUnlockRequirement
from .ridables import CHAPTER_TO_RIDABLES, BONUS_TO_RIDABLES, get_ridable_requirements, Ridable, RIDABLES_BY_NAME

if TYPE_CHECKING:
    from . import LegoStarWarsTCSWorld as TCSWorld
else:
    TCSWorld = object


@dataclass
class _RegionBuilder:
    """Small helper to store some data while creating regions."""

    world: TCSWorld
    """The world to create regions for."""

    available_minikits_check: int = 0
    """Double check that the minikit counts is as expected."""

    cantina: Region = field(init=False)
    """The origin region of the world, the Cantina."""

    story_character_unlock_regions: dict[str, list[Region]] = field(default_factory=dict)
    """A dict mapping story character names by the regions that would unlock that character in vanilla."""

    ridable_character_regions: dict[Ridable, list[tuple[str, Region]]] = field(default_factory=dict)
    """A dict mapping ridable character names by the regions that feature that character."""

    goal_requires_area_completion: bool = field(init=False)
    """Whether the goal requires completing areas."""

    def __post_init__(self) -> None:
        # Create the origin region.
        self.cantina = self.world.create_region(self.world.origin_region_name)

        self.goal_requires_area_completion = self.world.goal_area_completion_count > 0

    def _create_episode(self, episode_number: int) -> None:
        world = self.world
        episode_room = world.create_region(f"Episode {episode_number} Room")
        self.cantina.connect(episode_room, f"Episode {episode_number} Door")

        episode_chapters = EPISODE_TO_CHAPTER_AREAS[episode_number]
        for chapter_number, chapter in enumerate(episode_chapters, start=1):
            assert chapter.episode == episode_number
            assert chapter.number_in_episode == chapter_number
            if chapter.short_name not in world.enabled_chapters:
                continue
            if world.options.chapter_unlock_requirement == ChapterUnlockRequirement.option_vanilla_characters:
                # Update the count of how many chapters this character blocks access to.
                # Sort to ensure that `world.character_chapter_access_counts` maintains a deterministic order.
                if chapter.short_name in world.chapters_requiring_alt_characters:
                    world.character_chapter_access_counts.update(sorted(chapter.alt_character_requirements))
                else:
                    world.character_chapter_access_counts.update(sorted(chapter.character_requirements))
            chapter_region = world.create_region(chapter.name)

            entrance_name = f"Episode {episode_number} Room, Chapter {chapter_number} Door"
            episode_room.connect(chapter_region, entrance_name)

            create_gold_bricks = bool(world.options.enable_bonus_locations)
            exclude_locations = False
            is_goal_chapter = chapter.short_name == world.goal_chapter
            if is_goal_chapter:
                world.add_event_pair(f"Complete Goal Chapter {world.goal_chapter}", chapter_region, "Victory")

                goal_chapter_locations_mode = world.options.goal_chapter_locations_mode.value
                if goal_chapter_locations_mode == GoalChapterLocationsMode.option_removed:
                    # The only location that will be placed in the chapter's Region is the Victory event used by the
                    # completion_condition.
                    continue
                if goal_chapter_locations_mode == GoalChapterLocationsMode.option_excluded:
                    # When the locations are excluded, Gold Bricks from the Goal Chapter are removed from logic.
                    create_gold_bricks = False
                    exclude_locations = True

            # Completion.
            completion_name = f"{chapter.short_name} Completion"
            world.add_location(completion_name, chapter_region)
            if create_gold_bricks:
                # Completion Gold Brick event.
                world.add_gold_brick_event(f"{completion_name} - Gold Brick", chapter_region)

            # True Jedi.
            if world.options.enable_true_jedi_locations:
                true_jedi_name = f"{chapter.short_name} True Jedi"
                world.add_location(true_jedi_name, chapter_region)
                if create_gold_bricks:
                    # True Jedi Gold Brick event.
                    world.add_gold_brick_event(f"{true_jedi_name} - Gold Brick", chapter_region)

            # Power Brick.
            world.add_shop_location(chapter.power_brick_location_name, chapter_region, chapter.power_brick_studs_cost)

            # Character Purchases in the shop.
            # Character purchases unlocked upon completing the chapter (normally in Story mode).
            for shop_unlock, studs_cost in chapter.character_shop_unlocks.items():
                world.add_shop_location(shop_unlock, chapter_region, studs_cost)
            world.character_unlock_location_count += len(chapter.character_shop_unlocks)

            # Minikits.
            minikits_from_chapter = 0
            if world.options.enable_minikit_locations:
                chapter_minikits = world.create_region(f"{chapter.name} Minikits")
                chapter_region.connect(chapter_minikits, f"{chapter.name} - Collect All Minikits")
                for i in range(1, 11):
                    world.add_location(f"{chapter.short_name} Minikit {i}", chapter_minikits)
                    minikits_from_chapter += 1
                if exclude_locations:
                    # Exclude the minikit locations.
                    for loc in chapter_minikits.locations:
                        assert not loc.is_event  # At this point, only non-event locations should be created.
                        loc.progress_type = LocationProgressType.EXCLUDED
                if create_gold_bricks:
                    # All Minikits Gold Brick.
                    world.add_gold_brick_event(f"{chapter_minikits.name} - Gold Brick", chapter_minikits)
            elif world.options.minikit_goal_amount != 0:
                # If Minikit locations are disabled, but the goal requires Minikits, the Chapter Completion location
                # is instead treated as if it was the vanilla location for a 10 Minikits bundle.
                minikits_from_chapter += 10

            # The goal chapter does not contribute Minikits because it is only accessible once the Minikits goal is
            # complete.
            if not is_goal_chapter:
                self.available_minikits_check += minikits_from_chapter

            if world.options.enable_story_character_unlock_locations:
                # Story Character unlocks.
                for character in sorted(CHAPTER_AREA_STORY_CHARACTERS[chapter.short_name]):
                    self.story_character_unlock_regions.setdefault(character, []).append(chapter_region)

            if world.options.ridesanity:
                # Checks for riding unique characters.
                for ridable in CHAPTER_TO_RIDABLES.get(chapter.short_name, ()):
                    t = (chapter.short_name, chapter_region)
                    self.ridable_character_regions.setdefault(ridable, []).append(t)

            # Boss.
            if chapter.short_name in world.enabled_bosses:
                assert chapter.short_name != world.goal_chapter, ("The Goal Chapter should never be selected as an "
                                                                  "enabled boss")
                if world.options.only_unique_bosses_count:
                    boss_event_item_name = f"{world.short_name_to_boss_character[chapter.short_name]} Defeated"
                else:
                    boss_event_item_name = "Boss Defeated"
                world.add_event_pair(
                    f"{chapter.short_name} Defeat {chapter.boss}", chapter_region, boss_event_item_name)

            # Area completion.
            # The goal chapter does not contribute to Area Completion because the Goal Chapter requires completing
            # all other goals before it will unlock.
            if self.goal_requires_area_completion and not is_goal_chapter:
                # "Level" here is as a user-facing term, with the meaning of "Area" internally.
                world.add_event_pair(f"{chapter.short_name} Completion (Event)", chapter_region, "Level Completion")

            if exclude_locations:
                # Exclude the non-event locations in the chapter's region.
                loc: Location
                for loc in chapter_region.locations:
                    if not loc.is_event:
                        loc.progress_type = LocationProgressType.EXCLUDED

    def create_episodes(self) -> None:
        for episode_number in range(1, 7):
            if episode_number not in self.world.enabled_episodes:
                continue
            self._create_episode(episode_number)

    def create_story_character_unlock_locations(self) -> None:
        world = self.world

        excluded_goal_region: Region | None
        if (world.goal_chapter
                and world.options.goal_chapter_locations_mode.value == GoalChapterLocationsMode.option_excluded):
            excluded_goal_region = world.get_region(SHORT_NAME_TO_CHAPTER_AREA[world.goal_chapter].name)
        else:
            excluded_goal_region = None

        for character, parent_regions in self.story_character_unlock_regions.items():
            loc_name = f"Level Completion - Unlock {character}"
            if len(parent_regions) == 1:
                parent_region = parent_regions[0]
                # The location is only accessed from 1 region, so put the location in that region. This slightly
                # improves logic performance.
                character_location = world.add_location(loc_name, parent_region)
                if parent_region == excluded_goal_region:
                    # The location is only accessed through the Goal Chapter which has its locations excluded, so this
                    # chapter completion character unlock location should also be excluded.
                    character_location.progress_type = LocationProgressType.EXCLUDED
                    world.goal_excluded_character_unlock_location_count += 1
            else:
                # The location is accessed from multiple regions, so put the location in its own region that those
                # regions can be connected to.
                character_region = world.create_region(f"Unlock {character}")
                character_location = world.add_location(loc_name, character_region)
                for parent_region in parent_regions:
                    parent_region.connect(character_region)
                # There are multiple ways this location could be reached, so enable path display in the Spoiler (when
                # Playthrough Paths are enabled in the generator's host.yaml), so that the route the Playthrough used to
                # reach the location is clear.
                world.topology_present = True
            if excluded_goal_region is not None and excluded_goal_region in parent_regions:
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
        gold_brick_costs: dict[int, list[BonusArea]] = {}
        for area in BONUS_AREAS:
            if area.name not in world.enabled_bonuses:
                continue
            gold_bricks_required = area.gold_bricks_required
            if gold_bricks_required == 0:
                # No Gold Bricks are required to watch the Indy Trailer, so put it in the Bonuses region directly.
                assert area.name == "Indiana Jones: Trailer"
                world.add_location(area.completion_location_name, bonuses)
            else:
                gold_brick_costs.setdefault(gold_bricks_required, []).append(area)

        previous_gold_brick_region = bonuses
        for gold_brick_cost, areas in sorted(gold_brick_costs.items(), key=lambda t: t[0]):
            region = world.create_region(f"{gold_brick_cost} Gold Bricks Collected")
            player = world.player
            previous_gold_brick_region.connect(
                region, f"Collect {gold_brick_cost} Gold Bricks",
                lambda state, cost_=gold_brick_cost, item_=GOLD_BRICK_EVENT_NAME: (
                    state.has(item_, player, cost_)))
            previous_gold_brick_region = region

            for area in areas:
                area_region = world.create_region(area.name)
                region.connect(area_region)
                world.add_location(area.completion_location_name, area_region)

                if world.options.enable_story_character_unlock_locations:
                    for character in sorted(area.story_characters):
                        self.story_character_unlock_regions.setdefault(character, []).append(area_region)
                # todo: Item requirements have been removed for now because it is not currently possible to lock
                #  access to the bonus levels.
                if self.world.options.chapter_unlock_requirement == ChapterUnlockRequirement.option_vanilla_characters:
                    for item in area.item_requirements:
                        if item in CHARACTERS_AND_VEHICLES_BY_NAME:
                            world.character_chapter_access_counts[item] += 1
                assert area.gold_brick, "Every bonus that requires Gold Bricks to access should award a Gold Brick"

                world.add_gold_brick_event(f"{area.name} - Gold Brick", area_region)

                if self.goal_requires_area_completion:
                    # "Level" here is as a user-facing term, with the meaning of "Area" internally.
                    world.add_event_pair(f"{area.name} Completion (Event)", area_region, "Level Completion")

                if world.options.ridesanity:
                    # Checks for riding unique characters
                    for ridable in BONUS_TO_RIDABLES.get(area.name, ()):
                        t = (area.name, area_region)
                        self.ridable_character_regions.setdefault(ridable, []).append(t)

        # Indiana Jones shop purchase. Unlocks in the shop after watching the Lego Indiana Jones trailer.
        world.add_location("Purchase Indiana Jones", bonuses)
        world.character_unlock_location_count += 1

    def create_ridesanity_locations(self) -> None:
        world = self.world

        excluded_goal_region: Region | None
        if (world.goal_chapter
                and world.options.goal_chapter_locations_mode.value == GoalChapterLocationsMode.option_excluded):
            excluded_goal_region = world.get_region(SHORT_NAME_TO_CHAPTER_AREA[world.goal_chapter].name)
        else:
            excluded_goal_region = None

        # Add the Cantina Car ridable found in the Cantina itself, it cannot be found anywhere else.
        cantina_car = RIDABLES_BY_NAME["Cantina Car"]
        # Assert that it cannot be found anywhere else.
        assert cantina_car.is_in_cantina
        assert not cantina_car.bonus_area_names
        assert not cantina_car.chapter_shortnames
        # Add it to the dict of regions.
        self.ridable_character_regions[cantina_car] = [("cantina", self.cantina)]

        ridesanity_spots: defaultdict[str, list[tuple[Location | Entrance, tuple[CharacterAbility, ...] | None]]]
        ridesanity_spots = defaultdict(list)
        for ridable, areas_list in self.ridable_character_regions.items():
            world.ridesanity_location_count += 1
            ridable_location_name = ridable.location_name
            is_excluded_goal_chapter_location = False
            if len(areas_list) == 0:
                # There is only one region where this ridable can be found, so the ridable location can go directly in
                # that region.
                area_short_name, area_region = areas_list[0]
                ridable_location = world.add_location(ridable_location_name, area_region)
                # If there are any rules, they will be set on the location.
                requirements = get_ridable_requirements(area_short_name, ridable.user_facing_name)
                ridesanity_spots[area_short_name].append((ridable_location, requirements))
                is_excluded_goal_chapter_location = area_region == excluded_goal_region
            else:
                # There are multiple regions this ridable can be found in, so create a new region just for this location
                # and
                ridable_region = world.create_region(ridable_location_name)
                for area_short_name, area_region in areas_list:
                    entrance = area_region.connect(ridable_region)
                    # If there are any rules, they will be set on the entrance.
                    requirements = get_ridable_requirements(area_short_name, ridable.user_facing_name)
                    ridesanity_spots[area_short_name].append((entrance, requirements))
                    if area_region == excluded_goal_region:
                        is_excluded_goal_chapter_location = True
                ridable_location = world.add_location(ridable_location_name, ridable_region)
            if is_excluded_goal_chapter_location:
                # If the location can be accessed through the Goal Chapter that has excluded locations, exclude the
                # location, even if it could be accessed from elsewhere. This prevents the possibility of the Goal
                # Chapter from locking access to locations.
                ridable_location.progress_type = LocationProgressType.EXCLUDED
        world.ridesanity_spots.update(ridesanity_spots)

    def create_all_episodes_character_purchases(self) -> None:
        world = self.world
        all_episodes = world.create_region("All Episodes Unlocked")
        self.cantina.connect(all_episodes, "Unlock All Episodes")
        all_episodes_purchases = SHOP_SLOT_REQUIREMENT_TO_UNLOCKS["ALL_EPISODES"]
        for character_name in all_episodes_purchases.keys():
            character = CHARACTERS_AND_VEHICLES_BY_NAME[character_name]
            world.add_shop_location(character.purchase_location_name, all_episodes, character.purchase_cost)
        world.character_unlock_location_count += len(all_episodes_purchases)

    def create_starting_purchases(self) -> None:
        world = self.world
        starting_purchases = ("Gonk Droid", "PK Droid")
        for purchase in starting_purchases:
            character = CHARACTERS_AND_VEHICLES_BY_NAME[purchase]
            world.add_shop_location(character.purchase_location_name, self.cantina, character.purchase_cost)
        world.character_unlock_location_count += len(starting_purchases)

        for extra in PURCHASABLE_NON_POWER_BRICK_EXTRAS:
            loc = world.add_shop_location(extra.purchase_location_name, self.cantina, extra.studs_cost)
            if not world.options.enable_starting_extras_locations:
                loc.place_locked_item(world.create_item(extra.name))

    def create_non_goal_chapter_victory(self) -> None:
        """Create the Victory event for the goal when the goal does not require completing a Goal Chapter."""
        self.world.add_event_pair("Goal", self.cantina, "Victory")


def create_regions(world: TCSWorld) -> None:
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
    if not world.goal_chapter:
        builder.create_non_goal_chapter_victory()

    # For debugging.
    # from Utils import visualize_regions
    # visualize_regions(cantina, "LegoStarWarsTheCompleteSaga_Regions.puml", show_entrance_names=True)
