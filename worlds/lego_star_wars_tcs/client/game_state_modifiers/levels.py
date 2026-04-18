import logging
from dataclasses import dataclass, field
from typing import AbstractSet, Callable

from .text_replacer import TextId
from ..events import subscribe_event, OnAreaChangeEvent, OnReceiveSlotDataEvent, OnGameWatcherTickEvent
from ..common import ClientComponent, UintField
from ..common_addresses import (
    OPENED_MENU_DEPTH_ADDRESS,
    CURRENT_P_AREA_DATA_ADDRESS,
    ChapterDoorGameMode,
    IS_CHARACTER_SWAPPING_ENABLED,
    ChallengeMode,
    AREA_DATA_ID,
)
from ..type_aliases import TCSContext, AreaId
from ...items import ITEM_DATA_BY_NAME, ITEM_DATA_BY_ID, GenericItemData
from ...levels import (
    ChapterArea,
    CHAPTER_AREAS,
    SHORT_NAME_TO_CHAPTER_AREA,
    AREA_ID_TO_CHAPTER_AREA,
    DIFFICULT_OR_IMPOSSIBLE_TRUE_JEDI,
)
from ... import options


debug_logger = logging.getLogger("TCS Debug")

ALL_CHAPTER_AREA_IDS_SET = frozenset({area.area_id for area in CHAPTER_AREAS})

# Changes according to what Area door the player is stand in front of. It is 0xFF while in the rest of the Cantina, away
# from an Area door.
CURRENT_AREA_DOOR_ADDRESS = 0x8795A0

AREA_DATA_STORY_TRUE_JEDI_REQUIREMENT = UintField(0x8c)
AREA_DATA_FREE_PLAY_TRUE_JEDI_REQUIREMENT = UintField(0x90)

# For simplicity, the client locks the Goal Chapter by requiring a fake item that does not exist, so that no special
# handling is needed for unlocking the Goal Chapter.
_ITEM_DATA_BY_ID_PLUS_GOAL_SPECIAL = dict(ITEM_DATA_BY_ID)
_SUB_GOAL_SPECIAL_ID = 999_999_999
assert _SUB_GOAL_SPECIAL_ID not in _ITEM_DATA_BY_ID_PLUS_GOAL_SPECIAL, (
    f"The special item ID, {_SUB_GOAL_SPECIAL_ID} for all sub-goal completion already exists as a real item:"
    f" {_ITEM_DATA_BY_ID_PLUS_GOAL_SPECIAL[_SUB_GOAL_SPECIAL_ID]}")
# Note that the fake item name is user-facing.
_ITEM_DATA_BY_ID_PLUS_GOAL_SPECIAL[_SUB_GOAL_SPECIAL_ID] = GenericItemData(_SUB_GOAL_SPECIAL_ID,
                                                                           "all other goals completed")


@dataclass
class RemainingChapterItemRequirements:
    """
    Represents the remaining requirements to unlock a chapter.
    """
    count_remaining: int = 0
    item_ids_count_remaining: set[int] = field(default_factory=set)
    item_ids_hard_remaining: set[int] = field(default_factory=set)

    @staticmethod
    def ids_to_names(ids: set[int]) -> list[str]:
        return sorted(_ITEM_DATA_BY_ID_PLUS_GOAL_SPECIAL[ap_item_id].name for ap_item_id in ids)

    def __bool__(self) -> bool:
        """
        :return: Whether requirements still need to be met.
        """
        return (len(self.item_ids_hard_remaining) > 0
                or (len(self.item_ids_count_remaining) > 0 and self.count_remaining > 0))

    def __contains__(self, item) -> bool:
        """
        :param item: Item to test.
        :return: Whether the item is a remaining requirement.
        """
        return (item in self.item_ids_hard_remaining
                or (self.count_remaining > 0 and item in self.item_ids_count_remaining))

    def remove(self, ap_item_id: int) -> None:
        """
        Remove an item ID as a remaining requirement.
        :param ap_item_id:
        :return:
        """
        self.item_ids_hard_remaining.discard(ap_item_id)

        if self.count_remaining > 0 and ap_item_id in self.item_ids_count_remaining:
            self.item_ids_count_remaining.remove(ap_item_id)
            self.count_remaining -= 1

    @staticmethod
    def _format_items_names(names: list[str]):
        assert len(names) > 0
        if len(names) > 1:
            # A and B
            # A, B and C
            return f"{', '.join(names[:-1])} and {names[-1]}"
        else:
            # A
            return names[0]

    def format_remaining_chapter_requirements(self, chapter_name: str) -> str:
        count_items = self.ids_to_names(self.item_ids_count_remaining)
        hard_items = self.ids_to_names(self.item_ids_hard_remaining)
        # Move "Episode # Unlock" items to the front.
        hard_items.sort(key=lambda s: 0 if s.startswith("Episode") else 1)
        if count_items:
            if hard_items:
                return (f"{chapter_name} - Missing {self._format_items_names(hard_items)}"
                        f" and any {self.count_remaining} of {self._format_items_names(count_items)}")
            else:
                return f"{chapter_name} - Missing any {self.count_remaining} of {self._format_items_names(count_items)}"
        else:
            if hard_items:
                return f"{chapter_name} - Missing {self._format_items_names(hard_items)}"
            else:
                return ""

    def __str__(self) -> str:
        if self.count_remaining > 0:
            return (f"Requires all of {self.ids_to_names(self.item_ids_hard_remaining)},"
                    f" and {self.count_remaining} of {self.ids_to_names(self.item_ids_count_remaining)}")
        else:
            return f"Requires all of {self.ids_to_names(self.item_ids_hard_remaining)}"


class UnlockedChapterManager(ClientComponent):
    ap_item_id_to_dependent_game_chapters: dict[int, list[str]]
    remaining_chapter_item_requirements: dict[str, RemainingChapterItemRequirements]

    unlocked_chapters_per_episode: dict[int, set[AreaId]]
    should_unlock_all_episodes_shop_slots: Callable[[TCSContext], bool] = staticmethod(lambda _ctx: False)

    enabled_chapter_area_ids: set[int]
    enabled_episodes: set[int]
    chapters_using_alt_characters: set[str]
    characters_excluded_from_unlocking_chapters: set[str]
    per_chapter_required_character_count: dict[str, int]
    random_character_chapter_requirements: dict[str, list[str]]

    easy_true_jedi: bool = False
    scale_true_jedi_with_score_multipliers: bool = False
    goal_chapter: str = ""
    goal_chapter_area_id: int = -1

    last_area_door: ChapterArea | None = None
    current_area_id: int = -1

    def __init__(self) -> None:
        self.ap_item_id_to_dependent_game_chapters = {}
        self.remaining_chapter_item_requirements = {}
        self.unlocked_chapters_per_episode = {}
        self.enabled_chapter_area_ids = set()
        self.chapters_using_alt_characters = set()
        self.characters_excluded_from_unlocking_chapters = set()
        self.per_chapter_required_character_count = {}

    @subscribe_event
    def init_from_slot_data(self, event: OnReceiveSlotDataEvent) -> None:
        slot_data = event.slot_data
        ctx = event.context

        enabled_chapters = slot_data["enabled_chapters"]
        enabled_episodes = slot_data["enabled_episodes"]
        episode_unlock_requirement = slot_data["episode_unlock_requirement"]
        all_episodes_character_purchase_requirements = slot_data["all_episodes_character_purchase_requirements"]
        all_episodes_purchases_enabled = bool(slot_data["enable_all_episodes_purchases"])

        # In older multiworlds, easier true jedi is never enabled because the option did not exist.
        if event.generator_version < (1, 2, 0):
            self.easy_true_jedi = False
        else:
            self.easy_true_jedi = slot_data["easier_true_jedi"]
        self._set_current_area_true_jedi_requirement(ctx)

        # In older multiworlds, there is no option to scale True Jedi with score multipliers, so it is always disabled
        # in those versions.
        if event.generator_version < (1, 2, 0):
            self.scale_true_jedi_with_score_multipliers = False
        else:
            self.scale_true_jedi_with_score_multipliers = bool(slot_data["scale_true_jedi_with_score_multipliers"])

        # In older multiworlds, chapters were always unlocked through Story Characters.
        if event.generator_version < (1, 3, 0):
            chapter_unlock_requirement = options.ChapterUnlockRequirement.option_vanilla_characters
        else:
            chapter_unlock_requirement = slot_data["chapter_unlock_requirement"]

        chapter_unlock_requirement_is_characters = chapter_unlock_requirement in (
            options.ChapterUnlockRequirement.option_vanilla_characters,
            options.ChapterUnlockRequirement.option_random_characters,
        )

        if chapter_unlock_requirement == options.ChapterUnlockRequirement.option_random_characters:
            self.random_character_chapter_requirements = {
                chapter: [ITEM_DATA_BY_ID[c].name for c in characters]
                for chapter, characters in slot_data["chapter_random_character_requirements"].items()
            }
        else:
            self.random_character_chapter_requirements = {}

        num_enabled_episodes = len(enabled_episodes)

        self.enabled_chapter_area_ids = {SHORT_NAME_TO_CHAPTER_AREA[chapter_shortname].area_id
                                         for chapter_shortname in enabled_chapters}

        # In older multiworlds, all characters were required, alt characters could not be chosen, and characters could
        # not be excluded from requirements.
        if event.generator_version < (1, 4, 0):
            self.per_chapter_required_character_count = dict.fromkeys(enabled_chapters, 999_999_999)
            self.chapters_using_alt_characters = set()
            self.characters_excluded_from_unlocking_chapters = set()
        else:
            self.per_chapter_required_character_count = slot_data.get("chapter_required_character_counts", {})
            self.chapters_using_alt_characters = set(slot_data.get("chapters_requiring_alt_characters", ()))
            self.characters_excluded_from_unlocking_chapters = set(
                slot_data.get("chapter_unlock_characters_not_required", ())
            )

        if len(enabled_chapters) == 1:
            chapters_text = enabled_chapters[0]
        else:
            sorted_chapters = sorted(enabled_chapters)
            chapters_text = ", ".join(sorted_chapters[:-1])
            chapters_text += f" and {sorted_chapters[-1]}"
        chapters_info_text = f"Enabled Chapters for this slot: {chapters_text}"
        ctx.text_replacer.write_custom_string(TextId.SHOP_UNLOCKED_HINT_1, chapters_info_text)

        # Set 'All Episodes' unlock requirement.
        if not all_episodes_purchases_enabled:
            self.should_unlock_all_episodes_shop_slots = UnlockedChapterManager.should_unlock_all_episodes_shop_slots
        else:
            tokens = options.AllEpisodesCharacterPurchaseRequirements.option_episodes_tokens
            unlocks = options.AllEpisodesCharacterPurchaseRequirements.option_episodes_unlocked
            if all_episodes_character_purchase_requirements == tokens:
                if event.generator_version < (1, 2, 0):
                    # Old versions unlock by having as many tokens as the number of enabled episodes.
                    # The tokens were previously called "All Episodes Token".
                    self.should_unlock_all_episodes_shop_slots = (
                        lambda ctx: ctx.acquired_generic.episode_completion_token_count == num_enabled_episodes)
                else:
                    self.should_unlock_all_episodes_shop_slots = (
                        lambda ctx: ctx.acquired_generic.episode_completion_token_count >= 6)
            elif all_episodes_character_purchase_requirements == unlocks:
                self.should_unlock_all_episodes_shop_slots = (
                    lambda ctx: len(ctx.acquired_generic.received_episode_unlocks) == num_enabled_episodes)
            else:
                self.should_unlock_all_episodes_shop_slots = (
                    UnlockedChapterManager.should_unlock_all_episodes_shop_slots)
                raise RuntimeError(f"Unexpected 'All Episodes' character purchase requirement:"
                                   f" {all_episodes_character_purchase_requirements}")

        self.unlocked_chapters_per_episode = {i: set() for i in enabled_episodes}
        item_id_to_chapter_area_short_name: dict[int, list[str]] = {}
        remaining_chapter_item_requirements: dict[str, RemainingChapterItemRequirements] = {}

        if goal_chapter := slot_data.get("goal_chapter"):
            # Add the requirement for the fake sub-goals item to the Goal Chapter so that it will only unlock once all
            # sub-goals have been completed.
            item_id_to_chapter_area_short_name[_SUB_GOAL_SPECIAL_ID] = [goal_chapter]
            remaining_requirements = RemainingChapterItemRequirements(item_ids_hard_remaining={_SUB_GOAL_SPECIAL_ID})
            remaining_chapter_item_requirements[goal_chapter] = remaining_requirements
            self.goal_chapter = goal_chapter
            self.goal_chapter_area_id = SHORT_NAME_TO_CHAPTER_AREA[goal_chapter].area_id
            self.enabled_chapter_area_ids.add(self.goal_chapter_area_id)

        for chapter_area in CHAPTER_AREAS:
            if chapter_area.area_id not in self.enabled_chapter_area_ids:
                continue
            short_name = chapter_area.short_name

            unique_count_required_items: list[str] = []
            unique_count_required: int = 0
            always_required_items: list[str]
            if chapter_unlock_requirement_is_characters:
                if chapter_unlock_requirement == options.ChapterUnlockRequirement.option_vanilla_characters:
                    if short_name in self.chapters_using_alt_characters:
                        character_requirements = list(chapter_area.alt_character_requirements)
                    else:
                        character_requirements = list(chapter_area.character_requirements)
                    # Filter out excluded characters.
                    character_requirements = [c for c in character_requirements
                                              if c not in self.characters_excluded_from_unlocking_chapters]
                    count_required = self.per_chapter_required_character_count[short_name]
                else:
                    assert chapter_unlock_requirement == options.ChapterUnlockRequirement.option_random_characters
                    count_required = self.per_chapter_required_character_count[short_name]
                    character_requirements = self.random_character_chapter_requirements[short_name]
                assert count_required <= len(character_requirements), \
                    "Required counts should never be larger than the maximum possible"
                if count_required < len(character_requirements):
                    # Not all are required.
                    unique_count_required_items.extend(character_requirements)
                    unique_count_required = count_required
                    always_required_items = []
                else:
                    # All are required.
                    always_required_items = list(character_requirements)
            elif chapter_unlock_requirement == options.ChapterUnlockRequirement.option_chapter_item:
                always_required_items = [f"{short_name} Unlock"]
            else:
                raise ValueError(f"Unexpected ChapterUnlockRequirement with value {chapter_unlock_requirement}")

            episode = chapter_area.episode
            if episode_unlock_requirement == options.EpisodeUnlockRequirement.option_episode_item:
                always_required_items.append(f"Episode {episode} Unlock")
            elif episode_unlock_requirement == options.EpisodeUnlockRequirement.option_open:
                pass
            else:
                raise RuntimeError(f"Unexpected EpisodeUnlockRequirement: {episode_unlock_requirement}")

            # Convert item names into item IDs, and register the chapter shortname as depending on
            # these item IDs.
            unique_count_required_codes: set[int] = set()
            for item_name in unique_count_required_items:
                item_code = ITEM_DATA_BY_NAME[item_name].code
                assert item_code != -1
                item_id_to_chapter_area_short_name.setdefault(item_code, []).append(short_name)
                assert item_code not in unique_count_required_items
                unique_count_required_codes.add(item_code)

            always_required_codes: set[int] = set()
            for item_name in always_required_items:
                item_code = ITEM_DATA_BY_NAME[item_name].code
                assert item_code != -1
                item_id_to_chapter_area_short_name.setdefault(item_code, []).append(short_name)
                assert item_code not in always_required_codes
                always_required_codes.add(item_code)

            assert unique_count_required_codes.isdisjoint(always_required_codes), \
                "Items should not be both always, and sometimes, required"

            if short_name in remaining_chapter_item_requirements:
                remaining_requirements = remaining_chapter_item_requirements[short_name]
            else:
                remaining_requirements = RemainingChapterItemRequirements()
                remaining_chapter_item_requirements[short_name] = remaining_requirements
            assert remaining_requirements.count_remaining == 0, "Count should not be set"
            assert len(remaining_requirements.item_ids_count_remaining) == 0, "Count item IDs set should be empty"
            remaining_requirements.count_remaining += unique_count_required
            remaining_requirements.item_ids_count_remaining.update(unique_count_required_codes)
            remaining_requirements.item_ids_hard_remaining.update(always_required_codes)
            assert remaining_requirements, f"There should be some requirements for {short_name}"

        self.ap_item_id_to_dependent_game_chapters = item_id_to_chapter_area_short_name
        self.remaining_chapter_item_requirements = remaining_chapter_item_requirements
        self.enabled_episodes = {AREA_ID_TO_CHAPTER_AREA[area_id].episode for area_id in self.enabled_chapter_area_ids}

    def on_sub_goal_completion(self, ctx: TCSContext):
        self.on_character_or_chapter_or_episode_unlocked(ctx, _SUB_GOAL_SPECIAL_ID)

    def on_character_or_chapter_or_episode_unlocked(self, ctx: TCSContext, ap_item_id: int):
        dependent_chapters = self.ap_item_id_to_dependent_game_chapters.get(ap_item_id)
        if dependent_chapters is None:
            return

        for dependent_area_short_name in dependent_chapters:
            if dependent_area_short_name not in self.remaining_chapter_item_requirements:
                debug_logger.info("Would have removed %s from %s requirements, but it has already been unlocked.",
                                  _ITEM_DATA_BY_ID_PLUS_GOAL_SPECIAL[ap_item_id].name, dependent_area_short_name)
                continue
            remaining_requirements = self.remaining_chapter_item_requirements[dependent_area_short_name]
            assert remaining_requirements
            if ap_item_id not in remaining_requirements:
                # Consider a Chapter that requires an Episode Unlock and any 1 of 4 different Characters, once the first
                # Character of that 4 has been received, that part of the unlock requirements is completed, but the
                # Episode Unlock is still missing, so the chapter is not unlocked yet.
                debug_logger.info("Would have removed %s from %s requirements, but the relevant part of the"
                                  " requirements has already been completed.",
                                  _ITEM_DATA_BY_ID_PLUS_GOAL_SPECIAL[ap_item_id].name, dependent_area_short_name)
                continue
            remaining_requirements.remove(ap_item_id)
            debug_logger.info("Removed %s from %s requirements",
                              _ITEM_DATA_BY_ID_PLUS_GOAL_SPECIAL[ap_item_id].name, dependent_area_short_name)
            if not remaining_requirements:
                self.unlock_chapter(SHORT_NAME_TO_CHAPTER_AREA[dependent_area_short_name])
                # Display a message when the goal chapter is unlocked, but try to avoid telling the user if they are
                # connecting to a slot where the goal chapter is already completed.
                if (dependent_area_short_name == self.goal_chapter
                        and not ctx.finished_game
                        and self.goal_chapter_area_id not in ctx.free_play_completion_checker.completed_free_play):
                    msg = f"> Goal Chapter {self.goal_chapter} Unlocked! <"
                    # todo: This is something that would benefit from being able to control how long a message is
                    #  displayed for.
                    # Display the message twice because of its importance.
                    ctx.text_display.priority_messages(msg, msg)
                del self.remaining_chapter_item_requirements[dependent_area_short_name]

        del self.ap_item_id_to_dependent_game_chapters[ap_item_id]

    def unlock_chapter(self, chapter_area: ChapterArea):
        self.unlocked_chapters_per_episode[chapter_area.episode].add(chapter_area.area_id)
        debug_logger.info("Unlocked chapter %s (%s)", chapter_area.name, chapter_area.short_name)

    @subscribe_event
    async def update_game_state(self, event: OnGameWatcherTickEvent) -> None:
        ctx = event.context
        temporary_story_completion: AbstractSet[int]
        if (self.should_unlock_all_episodes_shop_slots(ctx)
                and ctx.acquired_characters.is_all_episodes_character_selected_in_shop(ctx)):
            # TODO: Instead of this, temporarily change the unlock conditions for these characters to 0 Gold Bricks.
            #  This will require finding the Collection data structs in memory at runtime.
            # In vanilla, the 'all episodes' characters unlock for purchase in the shop when the player has completed
            # every chapter in Story mode. In the AP randomizer, they need to be unlocked once all Episode Unlocks have
            # been acquired instead because completing all chapters in Story mode would basically never happen in a
            # playthrough of the randomized world.
            # Unfortunately, chapters being completed in Story mode is also what unlocks most other Character
            # purchases in the shop.
            # To work around this, all Story mode completions are temporarily set when all Episode Unlocks have been
            # acquired and the player has selected one of the 'all episodes' characters for purchase in the shop.
            temporary_story_completion = ALL_CHAPTER_AREA_IDS_SET
        else:
            temporary_story_completion = set()
            # TODO: Temporarily set the player's current chapter as completed so that they can save and exit from the
            #  chapter instead of having to exit without saving. This should happen once individual minikit logic is
            #  added because it can then be expected for a player to collect Minikits before a chapter is possible to
            #  complete.
            # If the player is in an Episode's room, and inside a Chapter door with the Chapter door's menu open, grant
            # them temporary Story mode completion so that they can select Free Play.
            cantina_room = ctx.read_current_cantina_room().value
            if cantina_room in self.unlocked_chapters_per_episode:
                # The player is in an Episode room in the cantina.
                unlocked_areas_in_room = self.unlocked_chapters_per_episode[cantina_room]
                if unlocked_areas_in_room:
                    # There are unlocked chapters in this room (the player shouldn't be able to access an Episode room
                    # unless it contains unlocked chapters...).
                    area_id_of_door_the_player_is_in_front_of = ctx.read_uchar(CURRENT_AREA_DOOR_ADDRESS)
                    area = AREA_ID_TO_CHAPTER_AREA.get(area_id_of_door_the_player_is_in_front_of)
                    if area is not None and area.area_id in unlocked_areas_in_room:
                        # The player is standing in front of, or within a chapter door that is unlocked.
                        if ctx.read_uchar(OPENED_MENU_DEPTH_ADDRESS) > 0:
                            # The player has a menu open (hopefully the menu within the chapter door.
                            temporary_story_completion = {area.area_id}
                            if self.last_area_door is not area:
                                # Force the selection in the menu to "Free Play" instead of "Story" or "Challenge".
                                # This is only done when the ChapterArea changes, so that users can still choose "Story"
                                # or "Challenge" if they really want to (not currently useful).
                                ChapterDoorGameMode.FREE_PLAY.set(ctx)
                                self.last_area_door = area

            # If the player is in a chapter, grant temporary Story mode completion so that they can Save and Exit to the
            # Cantina.
            current_area_id = self.current_area_id
            if current_area_id in AREA_ID_TO_CHAPTER_AREA:
                temporary_story_completion |= {current_area_id}

        completed_free_play = ctx.free_play_completion_checker.completed_free_play

        # 36 writes on each game state update is undesirable, but necessary to easily allow for temporarily completing
        # Story modes.
        for area in CHAPTER_AREAS:
            area_id = area.area_id
            enabled = area_id in self.enabled_chapter_area_ids
            if enabled and area_id in completed_free_play:
                # Set the chapter as unlocked and Story mode completed because Free Play has been completed.
                # The second bit in the third byte is custom to the AP client and signifies that Free Play has been
                # completed.
                ctx.write_bytes(area.address, b"\x03\x01", 2)
            elif area_id in temporary_story_completion:
                # Set the chapter as unlocked and Story mode completed because Story mode for this chapter needs to be
                # temporarily set as completed for some purpose.
                ctx.write_bytes(area.address, b"\x01\x01", 2)
            elif area_id not in self.enabled_chapter_area_ids:
                # Set the chapter as locked, with Story mode incomplete.
                ctx.write_bytes(area.address, b"\x00\x00", 2)
            else:
                if enabled and area_id in self.unlocked_chapters_per_episode[area.episode]:
                    # Set the chapter as unlocked, but with Story mode incomplete because Free Play has not been
                    # completed. This prevents characters being for sale in the shop without completing Free Play for
                    # the chapter that unlocks those shop slots.
                    ctx.write_bytes(area.address, b"\x01\x00", 2)
                else:
                    # Set the chapter as locked, with Story mode incomplete.
                    ctx.write_bytes(area.address, b"\x00\x00", 2)

    def _set_current_area_true_jedi_requirement(self, ctx: TCSContext, current_p_area_data: int | None = None,
                                                chapter_area: ChapterArea | None = None):
        if current_p_area_data is None or chapter_area is None:
            current_p_area_data = CURRENT_P_AREA_DATA_ADDRESS.get(ctx)

            if current_p_area_data == 0:
                # debug_logger.info("Current AreaData pointer is NULL. Nothing to do.")
                return

            current_area_id = AREA_DATA_ID.get(ctx, current_p_area_data)
            chapter_area = AREA_ID_TO_CHAPTER_AREA.get(current_area_id)

            if chapter_area is None:
                # The current area is not a chapter area, so there is nothing to do.
                debug_logger.info("The current area has ID %i, which is not a chapter Area", current_area_id)
                return

        if self.easy_true_jedi:
            true_jedi_requirement = chapter_area.story_true_jedi_requirement
        else:
            true_jedi_requirement = chapter_area.free_play_true_jedi_requirement

        if self.scale_true_jedi_with_score_multipliers:
            multiplier = ctx.acquired_generic.current_score_multiplier
            if (not self.easy_true_jedi
                    and multiplier >= 2
                    and chapter_area.short_name in DIFFICULT_OR_IMPOSSIBLE_TRUE_JEDI):
                # The chapter has a difficult or impossible True Jedi without the use of Score x2, so remove Score x2
                # from the multiplier.
                multiplier //= 2
            true_jedi_requirement *= multiplier

        AREA_DATA_FREE_PLAY_TRUE_JEDI_REQUIREMENT.set(ctx, current_p_area_data, true_jedi_requirement)
        debug_logger.info("Set the True Jedi requirement for %s to %i", chapter_area.name, true_jedi_requirement)

    @subscribe_event
    def on_area_change(self, event: OnAreaChangeEvent):
        ctx = event.context

        current_area_id = event.new_area_data_id
        self.current_area_id = current_area_id
        if current_area_id == -1:
            # debug_logger.info("Current AreaData pointer is NULL. Nothing to do.")
            return
        chapter_area = AREA_ID_TO_CHAPTER_AREA.get(current_area_id)

        if chapter_area is None:
            # The current area is not a chapter area, so there is nothing to do.
            debug_logger.info("The current area has ID %i, which is not a chapter Area", current_area_id)
            return

        self._set_current_area_true_jedi_requirement(event.context, event.new_p_area_data, chapter_area)
        # Check if the player is in a chapter.
        if current_area_id in AREA_ID_TO_CHAPTER_AREA:
            if not IS_CHARACTER_SWAPPING_ENABLED.get(ctx):
                # The player must be in Story, Superstory or a Bounty Hunter Mission.
                # todo: Find a way to tell apart Story, Superstory and Bounty Hunter Missions while in the level itself.
                #  Currently, the client can only tell them apart on the 'status' screen.
                ctx.text_display.priority_messages("Chapters should only be played in Free Play",
                                                   "Other modes are not currently part of the randomizer.")
            else:
                if not ChallengeMode.NO_CHALLENGE.is_set(ctx):
                    # The player is in Challenge mode.
                    ctx.text_display.priority_messages("Chapters should only be played in Free Play",
                                                       "Challenge mode is not currently part of the randomizer")

    def is_chapter_enabled(self, chapter: ChapterArea):
        return chapter.area_id in self.enabled_chapter_area_ids

    def is_chapter_unlocked(self, chapter: ChapterArea):
        return chapter.area_id in self.unlocked_chapters_per_episode[chapter.episode]

    def format_locked_chapter_requirements(self, chapter: ChapterArea) -> str:
        remaining = self.remaining_chapter_item_requirements.get(chapter.short_name)
        if remaining:
            return remaining.format_remaining_chapter_requirements(chapter.name)
        else:
            return ""

    def is_episode_enabled(self, episode: int):
        return episode in self.enabled_episodes

    def is_episode_unlocked(self, episode: int):
        # Unlocking any chapter in the episode unlocks the Episode door.
        return bool(self.unlocked_chapters_per_episode.get(episode))
