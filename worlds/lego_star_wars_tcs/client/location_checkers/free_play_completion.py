import logging
from enum import IntFlag
from typing import Iterable

from ..events import subscribe_event, OnReceiveSlotDataEvent
from ...levels import CHAPTER_AREAS, ChapterArea
from ...locations import LOCATION_NAME_TO_ID, LEVEL_COMMON_LOCATIONS
from ..type_aliases import ApLocationId, LevelId, TCSContext, AreaId
from ..common import ClientComponent
from ..common_addresses import ChallengeMode

from ...options import GoalChapterLocationsMode


debug_logger = logging.getLogger("TCS Debug")


# Flags set when on the Status screen.
STATUS_LEVEL_FLAGS_ADDRESS = 0x87A6D8


class StatusLevelFlags(IntFlag):
    UNKNOWN_1 = 0x1
    UNKNOWN_2 = 0x2
    # todo: See if completing Story True Jedi vs Free Play True Jedi have different flags.
    TRUE_JEDI_COMPLETED = 0x4  # Upon getting the True Jedi Gold Brick
    STORY_MODE = 0x8
    MINIKITS_COMPLETED = 0x10  # Upon getting the 10/10 Minikits Gold Brick
    UNKNOWN_20 = 0x20
    CHARACTER_SWAP_ENABLED = 0x40  # Free Play/Challenge/Character Bonus/Minikit Bonus
    VEHICLE_LEVEL = 0x80  # Minikit Bonus also counts as a vehicle level
    CHARACTER_OR_MINIKIT_BONUS = 0x100
    UNKNOWN_200 = 0x200  # todo: This appears to be set for 'collect all studs' bonus levels, (LEGO City + New Town)
    SUPERSTORY = 0x400
    SAVE_AND_QUIT = 0x800
    # Story related. This bit gets set when exiting back to the cantina from Story mode, but only after a delay.
    UNKNOWN_1000 = 0x1000


# Free Play level completion therefore requires:
STATUS_LEVEL_FREE_PLAY_COMPLETION_REQUIREMENTS = int(StatusLevelFlags.CHARACTER_SWAP_ENABLED)
# Does not care about:
# STATUS_LEVEL_FREE_PLAY_COMPLETION_IGNORES = int(
#         StatusLevelFlags.TRUE_JEDI_COMPLETED
#         | StatusLevelFlags.MINIKITS_COMPLETED
#         | StatusLevelFlags.VEHICLE_LEVEL
# )
# Must not have:
STATUS_LEVEL_FREE_PLAY_COMPLETION_NEGATIVE_REQUIREMENTS = int(
    StatusLevelFlags.STORY_MODE
    | StatusLevelFlags.CHARACTER_OR_MINIKIT_BONUS
    | StatusLevelFlags.SUPERSTORY
    | StatusLevelFlags.SAVE_AND_QUIT
)
# # Unknown:
# STATUS_LEVEL_FREE_PLAY_COMPLETION_UNKNOWN = int(
#     StatusLevelFlags.UNKNOWN_1
#     | StatusLevelFlags.UNKNOWN_2
#     | StatusLevelFlags.UNKNOWN_20
#     | StatusLevelFlags.UNKNOWN_200
#     | StatusLevelFlags.UNKNOWN_1000
# )
# These status level flags are not enough to tell apart Free Play and Challenge mode, so an additional explicitl check
# for Challenge mode needs to be performed.


STATUS_LEVEL_ID_TO_AP_ID: dict[LevelId, ApLocationId] = {
    area.status_level_id: LOCATION_NAME_TO_ID[LEVEL_COMMON_LOCATIONS[area.short_name]["Completion"]]
    for area in CHAPTER_AREAS
}
STATUS_LEVEL_ID_TO_AREA: dict[LevelId, ChapterArea] = {
    area.status_level_id: area for area in CHAPTER_AREAS
}
AP_ID_TO_AREA: dict[ApLocationId, ChapterArea] = {
    ap_id: STATUS_LEVEL_ID_TO_AREA[level_id] for level_id, ap_id in STATUS_LEVEL_ID_TO_AP_ID.items()
}


def is_status_level_free_play_completion(ctx: TCSContext) -> bool:
    """
    Return whether the current status Level is being shown as part of chapter completion in Free Play.

    The status Level for each chapter Area is used when tallying up Studs/Minikits etc. when returning to the
    Cantina, both for chapter completion and for 'Save and Exit'.

    The result is undefined if the player is not currently in a status Level.
    """
    status_flags = ctx.read_uint(STATUS_LEVEL_FLAGS_ADDRESS)
    return (status_flags & STATUS_LEVEL_FREE_PLAY_COMPLETION_REQUIREMENTS != 0
            and status_flags & STATUS_LEVEL_FREE_PLAY_COMPLETION_NEGATIVE_REQUIREMENTS == 0
            # The status_flags cannot be used to tell apart Free Play and Challenge, so an explicit check for Challenge
            # mode not being enabled is needed.
            and ChallengeMode.NO_CHALLENGE.is_set(ctx))


# TODO: How quickly can a player reasonably skip through the chapter completion screen? Do we need to check for chapter
#  completion with a higher frequency than how often the game watcher is checking?
class FreePlayChapterCompletionChecker(ClientComponent):
    """
    Check if the player has completed a free play chapter by looking for the ending screen that tallies up new
    studs/minikits.

    There appears to be no persistent storage in the game's memory or save data for whether a chapter has been completed
    in Free Play, so the client must poll the game state and track completions itself in the case of disconnecting from
    the server.
    """

    sent_locations: set[ApLocationId]
    completed_free_play: set[AreaId]
    enabled_chapter_areas: set[AreaId] | None
    chapter_completion_locations: dict[AreaId, list[ApLocationId]]

    def __init__(self):
        self.sent_locations = set()
        self.completed_free_play = set()
        self.enabled_chapter_areas = set()
        self.chapter_completion_locations = {}

    @subscribe_event
    def init_from_slot_data(self, event: OnReceiveSlotDataEvent) -> None:
        ctx = event.context

        goal_chapter_locations_mode = event.slot_data.get("goal_chapter_locations_mode",
                                                          GoalChapterLocationsMode.option_normal)
        goal_locations_removed = goal_chapter_locations_mode == GoalChapterLocationsMode.option_removed
        goal_chapter = event.slot_data.get("goal_chapter")
        enabled_chapter_areas: set[AreaId] = set()
        for area in CHAPTER_AREAS:
            chapter_locations = [STATUS_LEVEL_ID_TO_AP_ID[area.status_level_id]]
            # If the Goal Chapter had its locations removed, it should not send Level Completion Character Unlock
            # checks when completing the chapter.
            if not (area.short_name == goal_chapter and goal_locations_removed):
                for story_character in area.character_requirements:
                    loc_name = f"Level Completion - Unlock {story_character}"
                    chapter_locations.append(LOCATION_NAME_TO_ID[loc_name])
            enabled_chapter_locations = [loc_id for loc_id in chapter_locations if loc_id in ctx.server_locations]
            # Determine if a chapter is enabled by whether any of the chapter locations exist.
            # This is more robust against world bugs than relying on slot data.
            if enabled_chapter_locations:
                enabled_chapter_areas.add(area.area_id)
                self.chapter_completion_locations[area.area_id] = enabled_chapter_locations
            else:
                # There shouldn't be any present, but ensure that no data from disable chapters is present.
                self.completed_free_play.discard(area.area_id)
                self.sent_locations.difference_update(chapter_locations)
        self.enabled_chapter_areas = enabled_chapter_areas

        # Read any completions from save data. This should catch cases where the player has temporarily lost connection
        # to the server, completed a chapter, and then automatically reconnected to the server. The save data will be
        # read and should update datastorage.
        self.read_completed_free_play_from_save_data(ctx)

    def read_completed_free_play_from_save_data(self, ctx: TCSContext):
        enabled_chapter_areas = self.enabled_chapter_areas
        completed_area_ids: list[int] = []
        for area in CHAPTER_AREAS:
            area_id = area.area_id
            if enabled_chapter_areas is not None and area_id not in enabled_chapter_areas:
                continue
            # Either the chapter is enabled, or the player has not connected yet, so it is not known if the chapter is
            # enabled.
            unlocked_byte = ctx.read_uchar(area.address + area.UNLOCKED_OFFSET)
            if unlocked_byte == 0b11:
                self.completed_free_play.add(area_id)
                debug_logger.info("Read from save file that %s has been completed in Free Play", area.short_name)
                self.sent_locations.add(STATUS_LEVEL_ID_TO_AP_ID[area.status_level_id])
                completed_area_ids.append(area_id)
                # Tell the goal manager it should update for newly completed chapters.
                ctx.goal_manager.tag_for_update("area")
        ctx.update_datastorage_free_play_completion(completed_area_ids)
        ctx.goal_manager.tag_for_update("boss")

    def update_from_datastorage(self, ctx: TCSContext, area_ids: Iterable[int]):
        debug_logger.info("Updating Free Play Completion area_ids from datastorage: %s", area_ids)
        for area_id in area_ids:
            self.completed_free_play.add(area_id)
            ctx.goal_manager.tag_for_update("boss")
            # The locations should have been sent already, but try sending again just in-case.
            self.sent_locations.update(self.chapter_completion_locations.get(area_id, ()))
            # Tell the goal manager it should update for newly completed chapters.
            ctx.goal_manager.tag_for_update("area")

    async def check_completion(self, ctx: TCSContext, new_location_checks: list[ApLocationId]):

        # Level ID should be checked first because STATUS_LEVEL_FLAGS_ADDRESS only gets set when entering a Status
        # level, and its value will persist in memory until it is set again.
        current_level_id = ctx.read_current_level_id()
        completion_location_id = STATUS_LEVEL_ID_TO_AP_ID.get(current_level_id)
        if completion_location_id is not None:
            area = STATUS_LEVEL_ID_TO_AREA[current_level_id]
            area_id = area.area_id
            if area_id not in self.completed_free_play and is_status_level_free_play_completion(ctx):
                completion_locations = self.chapter_completion_locations.get(area.area_id, ())
                self.sent_locations.update(completion_locations)
                ctx.update_datastorage_free_play_completion([area_id])
                self.completed_free_play.add(area.area_id)
                ctx.write_byte(area.address + area.UNLOCKED_OFFSET, 0b11)
                ctx.goal_manager.tag_for_update("boss")

        # Not required because only the intersection of ctx.missing_locations will be sent to the server, but removing
        # checked locations (server state) here helps with debugging by reducing self.sent_locations to only new checks.
        self.sent_locations.difference_update(ctx.checked_locations)

        # Locations to send to the server will be filtered to only those in ctx.missing_locations, so include everything
        # up to this point in-case one was missed in a disconnect.
        new_location_checks.extend(self.sent_locations)
