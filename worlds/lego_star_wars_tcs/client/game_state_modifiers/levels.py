import logging
from dataclasses import dataclass, field
from typing import AbstractSet, Callable, Iterable

from .text_replacer import TextId
from ..events import subscribe_event, OnAreaChangeEvent, OnReceiveSlotDataEvent, OnGameWatcherTickEvent
from ..common import ClientComponent, UintField, StaticUChar, RawArray, UCharField
from ..common_addresses import (
    OPENED_MENU_DEPTH_ADDRESS,
    CURRENT_P_AREA_DATA_ADDRESS,
    ChapterDoorGameMode,
    IS_CHARACTER_SWAPPING_ENABLED,
    ChallengeMode,
    AREA_DATA_ID,
    CantinaRoom,
    playable_character_entity_iter,
)
from ..type_aliases import TCSContext
from ...items import ITEM_DATA_BY_ID
from ...legacy_true_jedi import DIFFICULT_OR_IMPOSSIBLE_TRUE_JEDI
from ... import options

from ...data.areas import Area, ALL_CHAPTER_AREAS
from ...data.characters import Character
from ...data.items import GenericItemData
from ...data.items.all_character_items import CHARACTER_TO_ITEM_DATA
from ...data.items.generic_items import EPISODE_UNLOCKS, GENERIC_DATA_BY_NAME, CHAPTER_TO_CHAPTER_UNLOCK_ITEM
from ...data.levels import Level
from ...slot_data import EnabledFeature


_DEBUG_LOGGER = logging.getLogger("TCS Debug")

_DEFAULT_PLAYERHITPOINTS = StaticUChar(0x00802bd4)
_PLAYERPROGRESS = 0x0093d530
_PLAYERPROGRESS_ELEMENT_SIZE = 0x10
_PLAYERPROGRESS_INDICES = range(0, 8)
_PLAYERPROGRESS_DEFAULT_PLAYER_HIT_POINTS = UCharField(0x8)
_CHARACTER_MAX_HEALTH = UCharField(0x107e)
_CHARACTER_HEALTH = UCharField(0x107f)

# Changes according to what Area door the player is stand in front of. It is 0xFF while in the rest of the Cantina, away
# from an Area door.
_CURRENT_AREA_DOOR_ADDRESS = 0x8795c0  # _last_hub_area

_AREA_DATA_FREE_PLAY_TRUE_JEDI_REQUIREMENT = UintField(0x90)

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

# The 'super bonus' areas, LEGO City and New Town, don't have Story mode, so are always completed in Free Play, and can
# therefor be ignored.
_FREE_PLAY_BONUSES = (
    Area.ANAKINSFLIGHT,
    Area.ANEWHOPE,
)
_ALL_FREE_PLAY_AREAS = ALL_CHAPTER_AREAS.union(_FREE_PLAY_BONUSES)


@dataclass
class _RemainingChapterItemRequirements:
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
        hard_items = self.ids_to_names(self.item_ids_hard_remaining)
        # Move "Episode # Unlock" items to the front.
        hard_items.sort(key=lambda s: 0 if s.startswith("Episode") else 1)
        if self.count_remaining:
            count_items = self.ids_to_names(self.item_ids_count_remaining)
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
    ap_item_id_to_dependent_game_chapters: dict[int, list[Area]]
    remaining_chapter_item_requirements: dict[Area, _RemainingChapterItemRequirements]

    unlocked_chapters_per_episode: dict[int, set[Area]]
    should_unlock_all_episodes_shop_slots: Callable[[TCSContext], bool] = staticmethod(lambda _ctx: False)

    enabled_chapter_areas: set[Area]
    enabled_free_play_bonuses: set[Area]  # Anakin's Flight and A New Hope
    enabled_episodes: set[int]
    chapters_using_alt_characters: set[Area]
    characters_excluded_from_unlocking_chapters: set[Character]
    per_chapter_required_character_count: dict[Area, int]
    random_character_chapter_requirements: dict[Area, list[Character]]

    easy_true_jedi: bool = False
    scale_true_jedi_with_score_multipliers: bool = False
    goal_chapter_area: Area | None = None

    last_area_door: Area | None = None
    current_area: Area | None = None
    most_recent_real_area: Area | None = None

    character_max_health: int = 4
    vehicle_max_health: int = 4

    def __init__(self) -> None:
        self.ap_item_id_to_dependent_game_chapters = {}
        self.remaining_chapter_item_requirements = {}
        self.unlocked_chapters_per_episode = {}
        self.enabled_chapter_areas = set()
        self.enabled_free_play_bonuses = set()
        self.chapters_using_alt_characters = set()
        self.characters_excluded_from_unlocking_chapters = set()
        self.per_chapter_required_character_count = {}

    @subscribe_event
    def init_from_slot_data(self, event: OnReceiveSlotDataEvent) -> None:
        slot_data = event.slot_data
        ctx = event.context

        self.character_max_health = slot_data.character_max_health.value
        self.vehicle_max_health = slot_data.vehicle_max_health.value


        enabled_chapters: list[Area] = sorted(slot_data.enabled_chapters.value)
        enabled_episodes: list[int] = sorted(slot_data.enabled_episodes.value)
        episode_unlock_requirement = slot_data.episode_unlock_requirement
        all_episodes_character_purchase_requirements = slot_data.all_episodes_character_purchase_requirements
        all_episodes_purchases_enabled = EnabledFeature.ALL_EPISODES_CHARACTER_PURCHASE_LOCATIONS.is_enabled(slot_data)

        self.easy_true_jedi = EnabledFeature.EASIER_TRUE_JEDI.is_enabled(slot_data)
        self._set_current_area_true_jedi_requirement(ctx)

        self.scale_true_jedi_with_score_multipliers = \
            EnabledFeature.SCALE_TRUE_JEDI_WITH_SCORE_MULTIPLIERS.is_enabled(slot_data)

        chapter_unlock_requirement = slot_data.chapter_unlock_requirement

        if chapter_unlock_requirement == options.ChapterUnlockRequirement.option_random_characters:
            character_requirements_option = slot_data.chapter_random_character_requirements
            if character_requirements_option is None:
                raise Exception("Random character requirements option is missing from slot data, but is required, "
                                "please report this as a bug.")
            self.random_character_chapter_requirements = character_requirements_option.value.copy()
        else:
            self.random_character_chapter_requirements = {}

        num_enabled_episodes = len(enabled_episodes)

        self.enabled_chapter_areas = slot_data.enabled_chapters.value.copy()
        self.enabled_free_play_bonuses = {area for area in slot_data.enabled_bonuses.value
                                          if area in _FREE_PLAY_BONUSES}

        required_counts_option = slot_data.chapter_required_character_counts
        required_counts: dict[Area, int]
        if required_counts_option is None:
            required_counts = {}
        else:
            required_counts = required_counts_option.value
        self.per_chapter_required_character_count = required_counts
        alt_character_chapters_option = slot_data.chapters_requiring_alt_characters
        chapters_requiring_alt_characters: Iterable[Area]
        if alt_character_chapters_option is None:
            chapters_requiring_alt_characters = ()
        else:
            chapters_requiring_alt_characters = alt_character_chapters_option.value
        self.chapters_using_alt_characters = set(chapters_requiring_alt_characters)
        self.characters_excluded_from_unlocking_chapters = (
            slot_data.chapter_unlock_story_characters_not_required.to_character_set())

        if len(enabled_chapters) == 1:
            chapters_text = enabled_chapters[0].get_short_name()
        else:
            sorted_chapters = sorted(enabled_chapters)
            chapters_text = ", ".join(map(Area.get_short_name, sorted_chapters[:-1]))
            chapters_text += f" and {sorted_chapters[-1].get_short_name()}"
        chapters_info_text = f"Enabled Chapters for this slot: {chapters_text}"
        ctx.text_replacer.write_custom_string(TextId.SHOP_UNLOCKED_HINT_1, chapters_info_text)

        # Set 'All Episodes' unlock requirement.
        if not all_episodes_purchases_enabled:
            self.should_unlock_all_episodes_shop_slots = UnlockedChapterManager.should_unlock_all_episodes_shop_slots
        else:
            tokens = options.AllEpisodesCharacterPurchaseRequirements.option_episodes_tokens
            unlocks = options.AllEpisodesCharacterPurchaseRequirements.option_episodes_unlocked
            if all_episodes_character_purchase_requirements == tokens:
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
        item_id_to_chapter_area: dict[int, list[Area]] = {}
        remaining_chapter_item_requirements: dict[Area, _RemainingChapterItemRequirements] = {}

        if (goal_chapter := slot_data.goal_chapter) is not None:
            goal_area = goal_chapter.value
            # Add the requirement for the fake sub-goals item to the Goal Chapter so that it will only unlock once all
            # sub-goals have been completed.
            item_id_to_chapter_area[_SUB_GOAL_SPECIAL_ID] = [goal_area]
            remaining_requirements = _RemainingChapterItemRequirements(item_ids_hard_remaining={_SUB_GOAL_SPECIAL_ID})
            remaining_chapter_item_requirements[goal_area] = remaining_requirements
            self.goal_chapter_area = goal_area
            self.enabled_chapter_areas.add(goal_area)

        for chapter_area in ALL_CHAPTER_AREAS:
            if chapter_area not in self.enabled_chapter_areas:
                continue

            unique_count_required_items: list[int] = []
            unique_count_required: int = 0
            always_required_items: list[int]
            if chapter_unlock_requirement.is_characters():
                character_requirements: list[Character]
                if chapter_unlock_requirement == options.ChapterUnlockRequirement.option_vanilla_characters:
                    if chapter_area in self.chapters_using_alt_characters:
                        character_requirements_set = chapter_area.get_purchase_characters()
                    else:
                        character_requirements_set = chapter_area.get_story_characters()
                    # Filter out excluded characters.
                    character_requirements = sorted(
                        character_requirements_set.difference(self.characters_excluded_from_unlocking_chapters),
                        key=lambda c: c.readable_name,
                    )
                    count_required = self.per_chapter_required_character_count[chapter_area]
                else:
                    assert chapter_unlock_requirement == options.ChapterUnlockRequirement.option_random_characters
                    count_required = self.per_chapter_required_character_count[chapter_area]
                    character_requirements = self.random_character_chapter_requirements[chapter_area]

                # Convert characters to item codes.
                character_code_requirements: list[int] = []
                for character in character_requirements:
                    code = CHARACTER_TO_ITEM_DATA[character].code
                    assert code is not None
                    character_code_requirements.append(code)

                assert count_required <= len(character_code_requirements), \
                    "Required counts should never be larger than the maximum possible"
                if count_required < len(character_code_requirements):
                    # Not all are required.
                    unique_count_required_items.extend(character_code_requirements)
                    unique_count_required = count_required
                    always_required_items = []
                else:
                    # All are required.
                    always_required_items = list(character_code_requirements)
            elif chapter_unlock_requirement == options.ChapterUnlockRequirement.option_chapter_item:
                unlock_item_name = CHAPTER_TO_CHAPTER_UNLOCK_ITEM[chapter_area]
                unlock_item_data = GENERIC_DATA_BY_NAME[unlock_item_name]
                unlock_item_code = unlock_item_data.code
                assert unlock_item_code is not None
                always_required_items = [unlock_item_code]
            else:
                raise ValueError(f"Unexpected ChapterUnlockRequirement with value {chapter_unlock_requirement}")

            episode = chapter_area.get_chapter_episode()
            if episode_unlock_requirement == options.EpisodeUnlockRequirement.option_episode_item:
                unlock_item_name = EPISODE_UNLOCKS[episode]
                unlock_item_data = GENERIC_DATA_BY_NAME[unlock_item_name]
                unlock_item_code = unlock_item_data.code
                assert unlock_item_code is not None
                always_required_items.append(unlock_item_code)
            elif episode_unlock_requirement == options.EpisodeUnlockRequirement.option_open:
                pass
            else:
                raise RuntimeError(f"Unexpected EpisodeUnlockRequirement: {episode_unlock_requirement}")

            # Convert item names into item IDs, and register the chapter area as depending on
            # these item IDs.
            unique_count_required_codes: set[int] = set(unique_count_required_items)
            assert len(unique_count_required_items) == len(unique_count_required_codes)
            for item_code in unique_count_required_items:
                item_id_to_chapter_area.setdefault(item_code, []).append(chapter_area)

            always_required_codes: set[int] = set(always_required_items)
            assert len(always_required_items) == len(always_required_codes)
            for item_code in always_required_items:
                item_id_to_chapter_area.setdefault(item_code, []).append(chapter_area)

            assert unique_count_required_codes.isdisjoint(always_required_codes), \
                "Items should not be both always, and sometimes, required"

            if chapter_area in remaining_chapter_item_requirements:
                remaining_requirements = remaining_chapter_item_requirements[chapter_area]
            else:
                remaining_requirements = _RemainingChapterItemRequirements()
                remaining_chapter_item_requirements[chapter_area] = remaining_requirements
            assert remaining_requirements.count_remaining == 0, "Count should not be set"
            assert len(remaining_requirements.item_ids_count_remaining) == 0, "Count item IDs set should be empty"
            remaining_requirements.count_remaining += unique_count_required
            remaining_requirements.item_ids_count_remaining.update(unique_count_required_codes)
            remaining_requirements.item_ids_hard_remaining.update(always_required_codes)
            assert remaining_requirements, f"There should be some requirements for {chapter_area!r}"

        self.ap_item_id_to_dependent_game_chapters = item_id_to_chapter_area
        self.remaining_chapter_item_requirements = remaining_chapter_item_requirements
        self.enabled_episodes = {area.get_chapter_episode() for area in self.enabled_chapter_areas}

    def on_sub_goal_completion(self, ctx: TCSContext):
        self.on_character_or_chapter_or_episode_unlocked(ctx, _SUB_GOAL_SPECIAL_ID)

    def on_character_or_chapter_or_episode_unlocked(self, ctx: TCSContext, ap_item_id: int):
        dependent_chapters = self.ap_item_id_to_dependent_game_chapters.get(ap_item_id)
        if dependent_chapters is None:
            return

        for dependent_area in dependent_chapters:
            if dependent_area not in self.remaining_chapter_item_requirements:
                _DEBUG_LOGGER.info("Would have removed %s from %s requirements, but it has already been unlocked.",
                                   _ITEM_DATA_BY_ID_PLUS_GOAL_SPECIAL[ap_item_id].name, dependent_area)
                continue
            remaining_requirements = self.remaining_chapter_item_requirements[dependent_area]
            assert remaining_requirements
            if ap_item_id not in remaining_requirements:
                # Consider a Chapter that requires an Episode Unlock and any 1 of 4 different Characters, once the first
                # Character of that 4 has been received, that part of the unlock requirements is completed, but the
                # Episode Unlock is still missing, so the chapter is not unlocked yet.
                _DEBUG_LOGGER.info("Would have removed %s from %s requirements, but the relevant part of the"
                                   " requirements has already been completed.",
                                   _ITEM_DATA_BY_ID_PLUS_GOAL_SPECIAL[ap_item_id].name, dependent_area)
                continue
            remaining_requirements.remove(ap_item_id)
            _DEBUG_LOGGER.info("Removed %s from %s requirements",
                               _ITEM_DATA_BY_ID_PLUS_GOAL_SPECIAL[ap_item_id].name, dependent_area)
            if not remaining_requirements:
                self._unlock_chapter(dependent_area)
                # Display a message when the goal chapter is unlocked, but try to avoid telling the user if they are
                # connecting to a slot where the goal chapter is already completed.
                if (dependent_area == self.goal_chapter_area
                        and not ctx.finished_game
                        and self.goal_chapter_area not in ctx.free_play_completion_checker.completed_free_play):
                    msg = f"> Goal Chapter {self.goal_chapter_area.get_short_name()} Unlocked! <"
                    # todo: This is something that would benefit from being able to control how long a message is
                    #  displayed for.
                    # Display the message twice because of its importance.
                    ctx.text_display.priority_messages(msg, msg)
                del self.remaining_chapter_item_requirements[dependent_area]

        del self.ap_item_id_to_dependent_game_chapters[ap_item_id]

    def _unlock_chapter(self, chapter_area: Area):
        self.unlocked_chapters_per_episode[chapter_area.get_chapter_episode()].add(chapter_area)
        _DEBUG_LOGGER.info("Unlocked chapter %s (%s)", chapter_area.name, chapter_area.get_short_name())

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
            temporary_story_completion = ALL_CHAPTER_AREAS
        else:
            temporary_story_completion = set()
            # If the player is in an Episode's room, and inside a Chapter door with the Chapter door's menu open, grant
            # them temporary Story mode completion so that they can select Free Play.
            cantina_room = ctx.read_current_cantina_room().value
            if cantina_room in self.unlocked_chapters_per_episode:
                # The player is in an Episode room in the cantina.
                unlocked_areas_in_room = self.unlocked_chapters_per_episode[cantina_room]
                if unlocked_areas_in_room:
                    # There are unlocked chapters in this room.
                    area_id_of_door_the_player_is_in_front_of = ctx.read_uchar(_CURRENT_AREA_DOOR_ADDRESS)
                    if area_id_of_door_the_player_is_in_front_of in Area:
                        area = Area(area_id_of_door_the_player_is_in_front_of)
                        if not area.is_chapter():
                            area = None
                    else:
                        area = None
                    if area is not None and area in unlocked_areas_in_room:
                        # The player is standing in front of, or within a chapter door that is unlocked.
                        if ctx.read_uchar(OPENED_MENU_DEPTH_ADDRESS) > 0:
                            # The player has a menu open (hopefully the menu within the chapter door).
                            temporary_story_completion = {area}
                            if self.last_area_door != area:
                                # Force the selection in the menu to "Free Play" instead of "Story" or "Challenge".
                                # This is only done when the Area changes, so that users can still choose "Story"
                                # or "Challenge" if they really want to (not currently useful).
                                ChapterDoorGameMode.FREE_PLAY.set(ctx)
                                self.last_area_door = area
                        else:
                            self.last_area_door = None
            elif cantina_room == CantinaRoom.BONUSES.value:
                area_id_of_door_the_player_is_in_front_of = ctx.read_uchar(_CURRENT_AREA_DOOR_ADDRESS)
                if area_id_of_door_the_player_is_in_front_of in _FREE_PLAY_BONUSES:
                    area = Area(area_id_of_door_the_player_is_in_front_of)
                    # The player is standing in front of, or within a bonus door.
                    if ctx.read_uchar(OPENED_MENU_DEPTH_ADDRESS) > 0:
                        # The player has a menu open (hopefully the menu within the bonus door).
                        temporary_story_completion = {area}
                        if self.last_area_door != area:
                            # Force the selection in the menu to "Free Play" instead of "Story".
                            # This is only done when the Area changes, so that users can still choose "Story" if they
                            # really want to (not currently useful).
                            ChapterDoorGameMode.FREE_PLAY.set(ctx)
                            self.last_area_door = area
                    else:
                        self.last_area_door = None

            # If the player is in a chapter, grant temporary Story mode completion so that they can Save and Exit to the
            # Cantina.
            current_area = self.current_area
            if current_area is not None and current_area in _ALL_FREE_PLAY_AREAS:
                temporary_story_completion |= {current_area}

        completed_free_play = ctx.free_play_completion_checker.completed_free_play

        # 38 writes on each game state update is undesirable, but necessary to easily allow for temporarily completing
        # Story modes.
        for area in _ALL_FREE_PLAY_AREAS:
            enabled = area in self.enabled_chapter_areas or area in self.enabled_free_play_bonuses
            if enabled and area in completed_free_play:
                # Set the chapter as unlocked and Story mode completed because Free Play has been completed.
                # The second bit in the third byte is custom to the AP client and signifies that Free Play has been
                # completed.
                ctx.write_bytes(area.save_data_address, b"\x03\x01", 2)
            elif area in temporary_story_completion:
                # Set the chapter as unlocked and Story mode completed because Story mode for this chapter needs to be
                # temporarily set as completed for some purpose.
                ctx.write_bytes(area.save_data_address, b"\x01\x01", 2)
            elif area not in self.enabled_chapter_areas and area not in self.enabled_free_play_bonuses:
                # Set the chapter as locked, with Story mode incomplete.
                ctx.write_bytes(area.save_data_address, b"\x00\x00", 2)
            else:
                # Even if a Gold Brick Bonus is unlocked, it cannot be accessed without building the door, so it does
                # not matter that Gold Brick Bonuses are technically considered 'unlocked' early.
                if (enabled and (area in _FREE_PLAY_BONUSES
                                or area in self.unlocked_chapters_per_episode[area.get_chapter_episode()])):
                    # Set the chapter as unlocked, but with Story mode incomplete because Free Play has not been
                    # completed. This prevents characters being for sale in the shop without completing Free Play for
                    # the chapter that unlocks those shop slots.
                    ctx.write_bytes(area.save_data_address, b"\x01\x00", 2)
                else:
                    # Set the chapter as locked, with Story mode incomplete.
                    ctx.write_bytes(area.save_data_address, b"\x00\x00", 2)

    def _set_current_area_true_jedi_requirement(self, ctx: TCSContext, current_p_area_data: int | None = None,
                                                chapter_area: Area | None = None):
        if current_p_area_data is None or chapter_area is None:
            current_p_area_data = CURRENT_P_AREA_DATA_ADDRESS.get(ctx)

            if current_p_area_data == 0:
                # _DEBUG_LOGGER.info("Current AreaData pointer is NULL. Nothing to do.")
                return

            current_area_id = AREA_DATA_ID.get(ctx, current_p_area_data)
            current_area = Area(current_area_id) if current_area_id in Area else None

            if current_area is None or not current_area.is_chapter():
                # The current area is not a chapter area, so there is nothing to do.
                _DEBUG_LOGGER.info("The current area has ID %i, which is not a chapter Area", current_area_id)
                return
            chapter_area = current_area

        if self.easy_true_jedi:
            true_jedi_requirement = chapter_area.story_true_jedi
        else:
            true_jedi_requirement = chapter_area.free_play_true_jedi

        if self.scale_true_jedi_with_score_multipliers:
            multiplier = ctx.acquired_generic.current_score_multiplier
            if (not self.easy_true_jedi
                    and multiplier >= 2
                    and chapter_area in DIFFICULT_OR_IMPOSSIBLE_TRUE_JEDI):
                # The chapter has a difficult or impossible True Jedi without the use of Score x2, so remove Score x2
                # from the multiplier.
                multiplier //= 2
            true_jedi_requirement *= multiplier

        _AREA_DATA_FREE_PLAY_TRUE_JEDI_REQUIREMENT.set(ctx, current_p_area_data, true_jedi_requirement)
        _DEBUG_LOGGER.info("Set the True Jedi requirement for %s to %i", chapter_area.name, true_jedi_requirement)

    @subscribe_event
    def on_area_change(self, event: OnAreaChangeEvent):
        ctx = event.context

        previous_real_area = self.most_recent_real_area
        current_area_id = event.new_area_data_id
        if current_area_id in Area:
            current_area = Area(current_area_id)
            self.most_recent_real_area = current_area
        else:
            current_area = None
        self.current_area = current_area
        if current_area is None:
            # _DEBUG_LOGGER.info("Current AreaData pointer is NULL. Nothing to do.")
            return

        # Adjust player character max health depending on whether they're going to a vehicle/non-vehicle Area.
        set_player_health_to_max = False
        if current_area.is_vehicle_area():
            max_health_to_set = self.vehicle_max_health
            if previous_real_area is Area.MAP and self.character_max_health < self.vehicle_max_health:
                # The player has gone from a non-vehicle Area (the Cantina) to a vehicle Area, but vehicles have more
                # max health than non-vehicle characters, so, if needed, set the playable character health in addition
                # to max health.
                set_player_health_to_max = True
        else:
            max_health_to_set = self.character_max_health
            if (
                    previous_real_area is not None
                    and previous_real_area.is_vehicle_area()
                    and self.vehicle_max_health < self.character_max_health
            ):
                # The player has gone from a vehicle Area to a non-vehicle Area (the Cantina), but non-vehicle
                # characters have more max health than vehicles, so, if needed, set the playable character health in
                # addition to max health.
                set_player_health_to_max = True
        _DEFAULT_PLAYERHITPOINTS.set(ctx, max_health_to_set)
        _DEBUG_LOGGER.info("Set player max health to %i", max_health_to_set)
        # These _PLAYERPROGRESS element fields also get set when initializing players. I don't know what _PLAYERPROGRESS
        # is actually used for.
        arr = RawArray(ctx.adjust_gog_address(_PLAYERPROGRESS), _PLAYERPROGRESS_ELEMENT_SIZE)
        for index in _PLAYERPROGRESS_INDICES:
            _PLAYERPROGRESS_DEFAULT_PLAYER_HIT_POINTS.set(ctx, arr[index], max_health_to_set)
        # Depending on when the client detects the area change, the characters may already have been created using the
        # old _DEFAULT_PLAYERHITPOINTS value, so iterate the playable characters that exist, and adjust their max
        # health, and health if necessary.
        for character_index, character_addr in playable_character_entity_iter(ctx):
            _CHARACTER_MAX_HEALTH.set(ctx, character_addr, max_health_to_set)
            _DEBUG_LOGGER.info("Set character _Player[%i] max health to %i", character_index, max_health_to_set)
            if set_player_health_to_max:
                _CHARACTER_HEALTH.set(ctx, character_addr, max_health_to_set)
                _DEBUG_LOGGER.info("Set character _Player[%i] health to %i", character_index, max_health_to_set)

        if current_area not in _ALL_FREE_PLAY_AREAS:
            # The current area is not a free play area, so there is nothing to do.
            _DEBUG_LOGGER.info("The current area is %s, which is not a chapter Area of free play bonus area",
                               repr(current_area))
            return

        is_chapter = current_area.is_chapter()
        if is_chapter:
            self._set_current_area_true_jedi_requirement(event.context, event.new_p_area_data, current_area)
        # Check that the chapter is being played in Free Play.
        if not IS_CHARACTER_SWAPPING_ENABLED.get(ctx):
            # todo: Can we block entry to Story in another way?
            # The player must be in Story, Superstory or a Bounty Hunter Mission.
            # todo: Find a way to tell apart Story, Superstory and Bounty Hunter Missions while in the level itself.
            #  Currently, the client can only tell them apart on the 'status' screen.
            ctx.load_level(Level.MAP, hard_reset=True)
            if is_chapter:
                ctx.text_display.priority_messages("Chapters should only be played in Free Play",
                                                   "Other modes are not currently part of the randomizer.")
            else:
                ctx.text_display.priority_messages("Bonuses with Free Play should only be played in Free Play",
                                                   "Story mode is not currently part of the randomizer.")
        else:
            if not ChallengeMode.NO_CHALLENGE.is_set(ctx):
                # The player is in Challenge mode.
                # Challenge mode uses the Free Play roster, so does not grant access to anything the player should not
                # already have access to, so there is no need to kick the player back to the Cantina.
                ctx.text_display.priority_messages("Challenge mode is not currently part of the randomizer.")

    def is_chapter_enabled(self, chapter: Area):
        return chapter in self.enabled_chapter_areas

    def is_chapter_unlocked(self, chapter: Area):
        return chapter in self.unlocked_chapters_per_episode[chapter.get_chapter_episode()]

    def format_locked_chapter_requirements(self, chapter: Area) -> str:
        remaining = self.remaining_chapter_item_requirements.get(chapter)
        if remaining:
            return remaining.format_remaining_chapter_requirements(chapter.readable_name)
        else:
            return ""

    def is_episode_enabled(self, episode: int):
        return episode in self.enabled_episodes

    def is_episode_unlocked(self, episode: int):
        # Unlocking any chapter in the episode unlocks the Episode door.
        return bool(self.unlocked_chapters_per_episode.get(episode))
