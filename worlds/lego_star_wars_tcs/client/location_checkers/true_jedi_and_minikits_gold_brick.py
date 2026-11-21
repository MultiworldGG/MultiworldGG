import logging
from typing import Iterable, NamedTuple

from . import ClientComponent
from ..common_addresses import CURRENT_AREA_ADDRESS
from ..common import UCharField
from ..events import subscribe_event, OnReceiveSlotDataEvent
from ..type_aliases import TCSContext

from ...data.areas import Area
from ...data.locations import LOCATION_NAME_TO_ID
from ...data.logic import ALL_CHAPTERS

_LOGGER = logging.getLogger("Client")

_TRUE_JEDI_FIELD_1 = UCharField(2)
#_TRUE_JEDI_FIELD_2 = UCharField(3)
_MINIKITS_GOLD_BRICK_FIELD = UCharField(4)
#_MINIKITS_COUNT_FIELD = UCharField(5)
_POWER_BRICK_FIELD = UCharField(6)


CURRENT_AREA_MINIKIT_COUNT_ADDRESS = 0x951258
# There is a second address, but I don't know what the difference is. This address remains non-zero for longer when
# exiting a level.
# CURRENT_AREA_MINIKIT_COUNT_ADDRESS2 = 0x951250
# The number of minikits found in this current session is also found in this same memory area.
# CURRENT_AREA_CURRENT_SESSION_MINIKIT_COUNT_ADDRESS = 0x951254
# There is an array of found Minikits in the current session. Each element of the array includes the Minikit's internal
# name and the Level ID the Minikit was found in. Minikit names can be shared by multiple Levels within an Area, so the
# Level ID is necessary to differentiate them.
# Each Minikit name is an 8-character null-terminated string.
# Each Level ID is a 2-byte integer (probably)
# There are then 2 unknown bytes
# CURRENT_AREA_CURRENT_SESSION_MINIKIT_ARRAY = 0x955ff0

# Set to 1 when True Jedi is completed, in either Story mode or Free Play, 0 otherwise.
# This is used by the game when deciding whether it needs to write True Jedi completion to the save data.
CURRENT_AREA_TRUE_JEDI_COMPLETE_STORY_OR_FREE_PLAY_ADDRESS = 0x87b9a0
# There is a second byte that only gets set from Free Play.
# Completing True Jedi in either Story or Free Play sets both True Jedi bytes in the save data, so there is not much
# point in only sending in-level True Jedi from Free Play mode, when the player could 'cheat' and do it in Story mode
# instead.
# CURRENT_AREA_TRUE_JEDI_COMPLETE_FREE_PLAY_ONLY_ADDRESS = 0x87b9b6


class AreaSaveData(NamedTuple):
    true_jedi_complete: bool
    minikits_gold_brick: bool
    power_brick: bool


class TrueJediAndPowerBrickAndMinikitBrickChecker(ClientComponent):
    """
    Check if the player has completed True Jedi for each level, check how many Minikit canisters the player has
    collected in each level, and check if the player has the Power Brick for each level.

    The Minikits Gold Brick is checked from the player's save-file. Individual minikit locations are checked by a
    different ClientComponent.
    """
    remaining_true_jedi_checks: set[Area]
    remaining_true_jedi_gold_bricks: set[Area]
    remaining_minikit_gold_bricks: set[Area]
    remaining_power_bricks_by_area: set[Area]

    def __init__(self):
        # Set to empty collections for safety.
        self.remaining_true_jedi_checks = set()
        self.remaining_true_jedi_gold_bricks = set()
        self.remaining_minikit_gold_bricks = set()
        self.remaining_power_bricks_by_area = set()

    @subscribe_event
    def init_from_slot_data(self, event: OnReceiveSlotDataEvent) -> None:
        # Determine the enabled locations by comparing against the locations the server says exist.
        # This is more robust than relying on slot data.
        ctx = event.context
        enabled_true_jedi: set[Area] = set()
        remaining_true_jedi: set[Area] = set()
        enabled_minikit_gold_bricks: set[Area] = set()
        enabled_power_bricks_by_area: set[Area] = set()

        for chapter in ALL_CHAPTERS:
            area = chapter.area

            # True Jedi
            true_jedi_id = LOCATION_NAME_TO_ID[area.get_true_jedi_name()]
            if ctx.is_location_sendable(true_jedi_id):
                enabled_true_jedi.add(area)
                if ctx.is_location_unchecked(true_jedi_id):
                    remaining_true_jedi.add(area)

            # Minikit Gold Brick
            for internal_name in chapter.minikits.keys():
                loc_id = LOCATION_NAME_TO_ID[area.prefix_name(internal_name)]
                if not ctx.is_location_sendable(loc_id):
                    # Minikit locations are not enabled, or this chapter is not enabled.
                    break
            else:
                # No break, so minikits are enabled (at least for this chapter)
                enabled_minikit_gold_bricks.add(area)
            
            # Power Brick
            extra = chapter.area.extra
            assert extra is not None, f"All chapters should have an Extra, but {chapter} is missing one"
            loc_id = LOCATION_NAME_TO_ID[extra.get_purchase_location_name()]
            if ctx.is_location_sendable(loc_id):
                enabled_power_bricks_by_area.add(area)

        self.remaining_true_jedi_checks = remaining_true_jedi
        self.remaining_power_bricks_by_area = enabled_power_bricks_by_area

        # Gold Bricks always start with the Gold Bricks for all enabled chapters because the client is unlikely to have
        # received already completed Gold Bricks from the AP server by the time the `OnReceiveSlotDataEvent` is fired.
        self.remaining_true_jedi_gold_bricks = enabled_true_jedi
        self.remaining_minikit_gold_bricks = enabled_minikit_gold_bricks

    # todo: In the future, this should check for the Power Brick in the current area also.
    async def check_current_area(self, ctx: TCSContext, new_location_checks: list[int]) -> None:
        """Check True Jedi and Minikits from reading the current area."""
        current_area_id = CURRENT_AREA_ADDRESS.get(ctx)
        if current_area_id not in Area:
            return

        current_area = Area(current_area_id)
        true_jedi_datastorage_area_ids_to_update = []
        if current_area.is_chapter():
            if self._check_true_jedi_from_current_area(current_area, ctx, new_location_checks):
                true_jedi_datastorage_area_ids_to_update.append(current_area_id)

        ctx.update_datastorage_true_jedi_completion(true_jedi_datastorage_area_ids_to_update)

    async def check_save_data(self, ctx: TCSContext, new_location_checks: list[int]) -> None:
        """Check True Jedi, Minikits and Power Bricks from reading save data."""
        new_true_jedi_from_sava_data = self._check_true_jedi_power_bricks_and_minikits_brick_from_save_data(
            ctx, new_location_checks)
        ctx.update_datastorage_true_jedi_completion(new_true_jedi_from_sava_data)

    def _check_true_jedi_from_current_area(self,
                                           current_area: Area,
                                           ctx: TCSContext,
                                           new_location_checks: list[int]
                                           ) -> bool:

        still_need_gold_brick = current_area in self.remaining_true_jedi_gold_bricks
        still_need_check = current_area in self.remaining_true_jedi_checks

        if not still_need_gold_brick and not still_need_check:
            return False

        current_area_true_jedi_complete = ctx.read_uint(
            CURRENT_AREA_TRUE_JEDI_COMPLETE_STORY_OR_FREE_PLAY_ADDRESS)

        if current_area_true_jedi_complete:
            if still_need_check:
                location_name = current_area.get_true_jedi_name()
                location_id = LOCATION_NAME_TO_ID[location_name]
                assert ctx.is_location_sendable(location_id), ("init_from_slot_data should have filtered to only"
                                                               " sendable locations in advance")

                self.remaining_true_jedi_checks.discard(current_area)
                new_location_checks.append(location_id)
            # `current_area` will only be removed from `self.remaining_true_jedi_gold_bricks` once the server
            # has updated `current_area` in datastorage and the client has acknowledged the datastorage update.
            return still_need_gold_brick
        else:
            # The True Jedi is still incomplete, so the client will need to continue polling until the True Jedi is
            # completed in-game. It is important to keep polling even when the location has been checked due to a
            # !collect because completing True Jedi gives a Gold Brick, which should only be given to the player when
            # True Jedi has actually been completed.
            # When True Jedi has actually been completed, it will update datastorage, telling other TCS clients
            # connected to the same slot that they should award the True Jedi Gold Brick. This is important for
            # supporting same-slot co-op.
            return False

    def update_from_datastorage(self,
                                ctx: TCSContext,
                                new_true_jedi_area_ids: Iterable[int] = (),
                                new_minikits_gold_brick_area_ids: Iterable[int] = (),
                                new_power_brick_area_ids: Iterable[int] = ()):
        for area_id in new_true_jedi_area_ids:
            if area_id not in Area:
                _LOGGER.error(f"Received true jedi completion from the server for Area ID %i, but no such area exists.",
                              area_id)
                continue
            area = Area(area_id)
            # There are two one-byte fields for True Jedi, seemingly as a leftover from when there used to be separate
            # True Jedi for Story and Free Play, which presumably got combined into just one True Jedi at some point in
            # development. The game writes to both fields, so we will too.
            true_jedi_address = area.save_data_address + _TRUE_JEDI_FIELD_1
            ctx.write_bytes(true_jedi_address, b"\x01\x01", 2)
            self.remaining_true_jedi_gold_bricks.discard(area)
        for area_id in new_minikits_gold_brick_area_ids:
            if area_id not in Area:
                _LOGGER.error(f"Received 10/10 minikits completion from the server for Area ID %i, but no such area"
                              f" exists.", area_id)
                continue
            area = Area(area_id)
            gold_brick_address = area.save_data_address + _MINIKITS_GOLD_BRICK_FIELD
            ctx.write_byte(gold_brick_address, 1)
        for area_id in new_power_brick_area_ids:
            if area_id not in Area:
                _LOGGER.error(f"Received power brick completion from the server for Area ID %i, but no such area"
                              f" exists.", area_id)
                continue
            area = Area(area_id)
            power_brick_address = area.save_data_address + _POWER_BRICK_FIELD
            ctx.write_byte(power_brick_address, 1)

    def _check_true_jedi_power_bricks_and_minikits_brick_from_save_data(
            self, ctx: TCSContext, new_location_checks: list[int]) -> list[int]:
        # todo: More smartly read only as many bytes as necessary. So only 1 byte when either the True Jedi is complete
        #  or all Minikits have been collected.
        cached_bytes: dict[Area, AreaSaveData] = {}

        def get_save_data_for_area(area: Area) -> AreaSaveData:
            if area in cached_bytes:
                return cached_bytes[area]
            else:
                # True Jedi seems to be at the 4th byte (maybe it is the 3rd because they both get activated?), 10/10
                # Minikits Gold Brick is at the 5th byte, and Minikit count is at the 6th byte. To reduce memory reads,
                # all are retrieved simultaneously.
                #
                read_bytes = ctx.read_bytes(area.save_data_address + 3, 4)
                true_jedi_byte = read_bytes[0]
                minikit_gold_brick = read_bytes[1]
                # The minikit count is in the middle, but is not used by the client because minikits are tracked
                # individually.
                # minikit_count_byte = read_bytes[2]
                power_brick_byte = read_bytes[3]
                area_save_data = AreaSaveData(bool(true_jedi_byte), bool(minikit_gold_brick), bool(power_brick_byte))
                cached_bytes[area] = area_save_data
                return area_save_data

        # Completed Gold Bricks to sync with Archipelago to support same-slot co-op/resuming an in-progress seed with a
        # new save file.
        completed_true_jedi_gold_brick_areas: list[Area] = []
        # Besides !collect and /send_location, both sets should be the same.
        for area in (self.remaining_true_jedi_gold_bricks | self.remaining_true_jedi_checks):
            location_name = area.get_true_jedi_name()
            location_id = LOCATION_NAME_TO_ID[location_name]
            assert ctx.is_location_sendable(location_id), ("init_from_slot_data should have filtered to only sendable"
                                                           " locations in advance")

            is_checked = ctx.is_location_checked(location_id)
            if is_checked:
                # The location has been checked, but potentially by !collect instead of by the player.
                # The client no longer needs to send this location ID to the server, but the location being !collect-ed
                # does not give the player the Gold Brick for completing True Jedi, so the player may still need to get
                # the Gold Brick if they have locations locked behind Gold Bricks.
                self.remaining_true_jedi_checks.discard(area)

            if area in self.remaining_true_jedi_gold_bricks:
                # The client does not think the True Jedi Gold Brick has been given/earned yet, so check if that is the
                # case.
                if get_save_data_for_area(area).true_jedi_complete:
                    # Add the area ID to the area IDs to send to the server.
                    completed_true_jedi_gold_brick_areas.append(area)
                    if not is_checked:
                        new_location_checks.append(location_id)

        # There are no locations tied to getting the Gold Brick for collecting all Minikits in a Chapter, but the Gold
        # Bricks are written to datastorage to sync Gold Bricks in same-slot co-op, and so that the PopTracker pack can
        # determine how many, and which Gold Bricks have been acquired.
        newly_completed_10_minikits_gold_bricks_areas: list[Area] = []
        updated_remaining_minikit_gold_bricks_by_area: set[Area] = set()
        for area in self.remaining_minikit_gold_bricks:
            if get_save_data_for_area(area).minikits_gold_brick:
                newly_completed_10_minikits_gold_bricks_areas.append(area)
            else:
                updated_remaining_minikit_gold_bricks_by_area.add(area)
        ctx.update_datastorage_10_minikits_completion(newly_completed_10_minikits_gold_bricks_areas)
        self.remaining_minikit_gold_bricks = updated_remaining_minikit_gold_bricks_by_area

        newly_completed_power_brick_areas: list[Area] = []
        updated_remaining_power_bricks_by_area: set[Area] = set()
        for area in self.remaining_power_bricks_by_area:
            if get_save_data_for_area(area).power_brick:
                newly_completed_power_brick_areas.append(area)
            else:
                updated_remaining_power_bricks_by_area.add(area)
        ctx.update_datastorage_power_bricks_collected(newly_completed_power_brick_areas)
        self.remaining_power_bricks_by_area = updated_remaining_power_bricks_by_area

        return completed_true_jedi_gold_brick_areas
