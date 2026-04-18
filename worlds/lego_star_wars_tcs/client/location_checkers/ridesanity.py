from . import ClientComponent
from ..common import AREA_ID_CANTINA
from ..common_addresses import CURRENT_AREA_ADDRESS
from ..events import subscribe_event, OnReceiveSlotDataEvent, OnAreaChangeEvent, OnPlayerCharacterIdChangeEvent
from ..type_aliases import AreaId, ApLocationId, CharacterId, TCSContext
from ...levels import SHORT_NAME_TO_CHAPTER_AREA, BONUS_NAME_TO_BONUS_AREA
from ...locations import LOCATION_NAME_TO_ID
from ...ridables import CHAPTER_TO_RIDABLES, BONUS_TO_RIDABLES, RIDABLES_BY_NAME

from ...options import GoalChapterLocationsMode


class RidesanityChecker(ClientComponent):
    ridables_by_area: dict[AreaId, dict[CharacterId, ApLocationId]]
    current_area_id: AreaId = -1
    locations_to_send: set[ApLocationId]

    def __init__(self):
        self.ridables_by_area = {}
        self.locations_to_send = set()

    @subscribe_event
    def init_from_slot_data(self, event: OnReceiveSlotDataEvent):
        # Initialise
        if event.generator_version < (1, 2, 0):
            # Ridesanity did not exist on older versions.
            ridesanity_enabled = False
        else:
            ridesanity_enabled = bool(event.slot_data["ridesanity"])

        self.ridables_by_area = {}

        if not ridesanity_enabled:
            return

        goal_chapter_locations_mode = event.slot_data.get("goal_chapter_locations_mode",
                                                          GoalChapterLocationsMode.option_normal)
        goal_locations_removed = goal_chapter_locations_mode == GoalChapterLocationsMode.option_removed
        goal_chapter = event.slot_data.get("goal_chapter")

        for bonus_name in event.slot_data["enabled_bonuses"]:
            if bonus_name not in BONUS_TO_RIDABLES:
                # No ridables in this bonus.
                continue
            area_id = BONUS_NAME_TO_BONUS_AREA[bonus_name].area_id
            self.ridables_by_area[area_id] = {
                ridable.character_id: LOCATION_NAME_TO_ID[ridable.location_name]
                for ridable in BONUS_TO_RIDABLES[bonus_name]
            }
        for short_name in event.slot_data["enabled_chapters"]:
            if short_name not in CHAPTER_TO_RIDABLES:
                # No ridables in this chapter.
                continue
            if short_name == goal_chapter and goal_locations_removed:
                # The Goal Chapter, with locations removed, should not send Ridesanity checks.
                continue
            area_id = SHORT_NAME_TO_CHAPTER_AREA[short_name].area_id
            self.ridables_by_area[area_id] = {
                ridable.character_id: LOCATION_NAME_TO_ID[ridable.location_name]
                for ridable in CHAPTER_TO_RIDABLES[short_name]
            }

        cantina_car = RIDABLES_BY_NAME["Cantina Car"]
        self.ridables_by_area[AREA_ID_CANTINA] = {
            cantina_car.character_id: LOCATION_NAME_TO_ID[cantina_car.location_name],
        }

        self.current_area_id = CURRENT_AREA_ADDRESS.get(event.context)

        # If the player is currently riding a character that should send a check, they can just stop riding and then
        # start riding again for the check to send, so don't bother checking the current character IDs of the players.

    @subscribe_event
    async def on_area_change(self, event: OnAreaChangeEvent):
        # Update which ids we are currently checking for. (or just update a `self` attribute that stores the area ID.
        self.current_area_id = event.new_area_data_id

    @subscribe_event
    async def on_player_character_id_change(self, event: OnPlayerCharacterIdChangeEvent):
        # Check for the player being one of the ridable characters that should send a check and update a `self`
        # attribute of locations to send.
        ridables = self.ridables_by_area.get(self.current_area_id, {})

        if not ridables:
            return

        for character_id in (event.new_p1_character_id, event.new_p2_character_id):
            if character_id in ridables:
                ap_location_id = ridables[character_id]
                if event.context.is_location_unchecked(ap_location_id):
                    self.locations_to_send.add(ap_location_id)
                else:
                    del ridables[character_id]

    async def check_ridesanity(self, ctx: TCSContext, new_location_checks: list[int]):
        if self.locations_to_send:
            # Remove any completed location checks.
            self.locations_to_send.difference_update(ctx.checked_locations)
            # Add in new location checks.
            new_location_checks.extend(self.locations_to_send)
