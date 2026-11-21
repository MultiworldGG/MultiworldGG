import logging
from typing import Iterable

from ..common import ClientComponent, UCharField, StaticUChar
from ..events import subscribe_event, OnReceiveSlotDataEvent
from ..type_aliases import MemoryAddress, ApLocationId, TCSContext, AreaId

from ...data.areas import Area, BONUS_ROOM_BONUSES
from ...data.locations import LOCATION_NAME_TO_ID


_DEBUG_LOGGER = logging.getLogger("TCS Debug")


_AREA_COMPLETION = UCharField(0x1)
_INDY_TRAILER_WATCHED = StaticUChar(0x86e505)

_FREE_PLAY_BONUSES = (Area.ANAKINSFLIGHT, Area.ANEWHOPE)

_ALL_STORY_COMPLETION_CHECKS: dict[Area, tuple[ApLocationId, MemoryAddress]] = {
    area: (LOCATION_NAME_TO_ID[area.get_completion_name()], area.save_data_address + _AREA_COMPLETION)
    for area in BONUS_ROOM_BONUSES if area not in _FREE_PLAY_BONUSES
}
# The Indiana Jones trailer has its own part of memory that it writes to, to mark that it has been watched, rather than
# marking the Lost Temple Area's save-data as completed.
_ALL_STORY_COMPLETION_CHECKS[Area.LOSTTEMPLE] = (
    LOCATION_NAME_TO_ID[Area.LOSTTEMPLE.get_completion_name()],
    _INDY_TRAILER_WATCHED,
)


class BonusAreaCompletionChecker(ClientComponent):
    """
    Check if the player has completed a bonus Area by reading the completion byte of each bonus Area that has not
    already been completed according to the server.
    """
    # Anakin's Flight and A New Hope support Free Play, but the rest are Story mode only, for now, this class only
    # checks for story completion.
    remaining_story_completion_checks: dict[Area, tuple[ApLocationId, MemoryAddress]]
    remaining_bonus_area_completion_locations: dict[Area, list[ApLocationId]]

    def __init__(self):
        self.remaining_story_completion_checks = _ALL_STORY_COMPLETION_CHECKS.copy()
        self.remaining_bonus_area_completion_locations = {}

    @subscribe_event
    def init_from_slot_data(self, event: OnReceiveSlotDataEvent) -> None:
        bonus_area_completion_locations: dict[Area, list[ApLocationId]] = {}
        for bonus_area in event.slot_data.enabled_bonuses.value:
            if bonus_area not in _ALL_STORY_COMPLETION_CHECKS:
                # Skip Anakin's Flight and A New Hope because they are completed in Free Play, and the
                # free_play_completion.FreePlayAreaCompletionChecker will check those.
                continue
            loc_ids = {LOCATION_NAME_TO_ID[character.get_level_completion_unlock_location_name()]
                        for character in bonus_area.get_story_characters()}
            server_locations = event.context.server_locations
            loc_ids.intersection_update(server_locations)
            bonus_area_completion_locations[bonus_area] = sorted(loc_ids)
        self.remaining_bonus_area_completion_locations = bonus_area_completion_locations

    @staticmethod
    def update_from_datastorage(ctx: TCSContext, area_ids: Iterable[AreaId]):
        _DEBUG_LOGGER.info("Updating Bonus Completion area_ids from datastorage: %s", area_ids)
        for area_id in area_ids:
            _ap_id, address = _ALL_STORY_COMPLETION_CHECKS[Area(area_id)]
            ctx.write_byte(address, 1)

    async def check_completion(self, ctx: TCSContext, new_location_checks: list[int]):
        # As location checks get sent, the remaining bytes check to gets reduced.
        updated_remaining_story_completion_checks: dict[Area, tuple[ApLocationId, MemoryAddress]] = {}
        write_to_datastorage_areas: list[Area] = []
        for area, (ap_id, address) in self.remaining_story_completion_checks.items():
            # Memory reads are assumed to be the slowest part
            if not ctx.is_location_unchecked(ap_id):
                # By skipping the location, it will not be added to the updated dictionary, so will not be checked in
                # the future.
                if ctx.is_location_sendable(ap_id):
                    write_to_datastorage_areas.append(area)
                    # Tell the goal manager it should update for newly completed bonuses.
                    ctx.goal_manager.tag_for_update("area")
                continue
            # It seems that the value is always `1` for a completed bonus and `0` otherwise. The client checks
            # truthiness in case it is possible that other bits could be set.
            if ctx.read_uchar(address):
                # The bonus has been completed, or viewed in the case of the Indiana Jones trailer.
                new_location_checks.append(ap_id)
            # Even if the location is being sent, it is still added to the updated dictionary in case the client loses
            # connection from the server.
            updated_remaining_story_completion_checks[area] = (ap_id, address)

        updated_remaining_bonus_area_completion_locations = {}
        for area, ap_ids in self.remaining_bonus_area_completion_locations.items():
            area_completed_or_disabled = area not in updated_remaining_story_completion_checks
            if area_completed_or_disabled:
                # Send the locations to AP, and skip adding the `area` key into
                # `updated_remaining_bonus_area_completion_locations`.
                # It does not matter if the locations do not exist, they will get filtered out before being sent to the
                # server.
                new_location_checks.extend(ap_ids)
            else:
                updated_remaining_bonus_area_completion_locations[area] = ap_ids

        self.remaining_story_completion_checks = updated_remaining_story_completion_checks
        self.remaining_bonus_area_completion_locations = updated_remaining_bonus_area_completion_locations
        ctx.update_datastorage_bonuses_completion(write_to_datastorage_areas)

