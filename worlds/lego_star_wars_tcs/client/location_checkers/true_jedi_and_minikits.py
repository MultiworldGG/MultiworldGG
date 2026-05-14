from typing import Iterable

from . import ClientComponent
from ..common_addresses import CURRENT_AREA_ADDRESS
from ..events import subscribe_event, OnReceiveSlotDataEvent
from ..type_aliases import TCSContext
from ...levels import SHORT_NAME_TO_CHAPTER_AREA, AREA_ID_TO_CHAPTER_AREA, ChapterArea
from ...locations import LEVEL_COMMON_LOCATIONS, LOCATION_NAME_TO_ID


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


class TrueJediAndPowerBrickAndMinikitChecker(ClientComponent):
    """
    Check if the player has completed True Jedi for each level, check how many Minikit canisters the player has
    collected in each level, and check if the player has the Power Brick for each level.

    Minikits are checked from both the player's save-file and from the current Area data, allowing for minikit checks to
    be sent as soon as minikits are collected, and to allow progressing while connection to the server has been lost.
    """
    remaining_true_jedi_check_shortnames: set[str]
    remaining_true_jedi_gold_brick_shortnames: set[str]
    remaining_minikit_checks_by_shortname: dict[str, list[tuple[int, str]]]
    remaining_minikit_gold_bricks_by_area_id: set[int]
    remaining_power_bricks_by_area_id: set[int]

    def __init__(self):
        # Set to empty collections for safety.
        self.remaining_true_jedi_check_shortnames = set()
        self.remaining_true_jedi_gold_brick_shortnames = set()
        self.remaining_minikit_checks_by_shortname = {}
        self.remaining_minikit_gold_bricks_by_area_id = set()
        self.remaining_power_bricks_by_area_id = set()

    @subscribe_event
    def init_from_slot_data(self, event: OnReceiveSlotDataEvent) -> None:
        # Determine the enabled locations by comparing against the locations the server says exist.
        # This is more robust than relying on slot data.
        ctx = event.context
        enabled_true_jedi = set()
        remaining_true_jedi = set()
        remaining_minikits = {}
        enabled_minikit_gold_bricks = set()
        enabled_power_bricks_by_area_id = set()

        for shortname, common_locations in LEVEL_COMMON_LOCATIONS.items():
            chapter_area = SHORT_NAME_TO_CHAPTER_AREA[shortname]

            true_jedi_id = LOCATION_NAME_TO_ID[common_locations["True Jedi"]]
            if ctx.is_location_sendable(true_jedi_id):
                enabled_true_jedi.add(shortname)
                if ctx.is_location_unchecked(true_jedi_id):
                    remaining_true_jedi.add(shortname)

            remaining_minikits_in_chapter: list[tuple[int, str]] = []
            for i, minikit_loc_name in enumerate(common_locations["Minikits"], start=1):
                loc_id = LOCATION_NAME_TO_ID[minikit_loc_name]
                if not ctx.is_location_sendable(loc_id):
                    # Minikits are not enabled for this chapter, or for all chapters.
                    break
                if ctx.is_location_checked(loc_id):
                    continue
                remaining_minikits_in_chapter.append((i, minikit_loc_name))
            else:
                # No break, so minikits are enabled.
                remaining_minikits[shortname] = remaining_minikits_in_chapter
                enabled_minikit_gold_bricks.add(chapter_area.area_id)

            if ctx.is_location_sendable(LOCATION_NAME_TO_ID[chapter_area.power_brick_location_name]):
                enabled_power_bricks_by_area_id.add(chapter_area.area_id)

        self.remaining_true_jedi_check_shortnames = remaining_true_jedi
        self.remaining_minikit_checks_by_shortname = remaining_minikits
        self.remaining_power_bricks_by_area_id = enabled_power_bricks_by_area_id

        # Gold Bricks always start with the Gold Bricks for all enabled chapters because the client is unlikely to have
        # received already completed Gold Bricks from the AP server by the time the `OnReceiveSlotDataEvent` is fired.
        self.remaining_true_jedi_gold_brick_shortnames = enabled_true_jedi
        self.remaining_minikit_gold_bricks_by_area_id = enabled_minikit_gold_bricks

    # todo: In the future, this should check for the Power Brick in the current area also.
    async def check_current_area(self, ctx: TCSContext, new_location_checks: list[int]) -> None:
        """Check True Jedi and Minikits from reading the current area."""
        current_area_id = ctx.read_uchar(CURRENT_AREA_ADDRESS)
        true_jedi_datastorage_area_ids_to_update = []
        if current_area_id in AREA_ID_TO_CHAPTER_AREA:
            current_area = AREA_ID_TO_CHAPTER_AREA[current_area_id]
            self._check_minikits_from_current_area(current_area, ctx, new_location_checks)
            if self._check_true_jedi_from_current_area(current_area, ctx, new_location_checks):
                true_jedi_datastorage_area_ids_to_update.append(current_area_id)

        ctx.update_datastorage_true_jedi_completion(true_jedi_datastorage_area_ids_to_update)

    async def check_save_data(self, ctx: TCSContext, new_location_checks: list[int]) -> None:
        """Check True Jedi, Minikits and Power Bricks from reading save data."""
        new_true_jedi_from_sava_data = self._check_true_jedi_power_bricks_and_minikits_from_save_data(
            ctx, new_location_checks)
        ctx.update_datastorage_true_jedi_completion(new_true_jedi_from_sava_data)

    def _check_true_jedi_from_current_area(self,
                                           current_area: ChapterArea,
                                           ctx: TCSContext,
                                           new_location_checks: list[int]
                                           ) -> bool:
        shortname = current_area.short_name

        still_need_gold_brick = shortname in self.remaining_true_jedi_gold_brick_shortnames
        still_need_check = shortname in self.remaining_true_jedi_check_shortnames

        if not still_need_gold_brick and not still_need_check:
            return False

        current_area_true_jedi_complete = ctx.read_uint(
            CURRENT_AREA_TRUE_JEDI_COMPLETE_STORY_OR_FREE_PLAY_ADDRESS)

        if current_area_true_jedi_complete:
            if still_need_check:
                location_name = LEVEL_COMMON_LOCATIONS[shortname]["True Jedi"]
                location_id = LOCATION_NAME_TO_ID[location_name]
                assert ctx.is_location_sendable(location_id), ("init_from_slot_data should have filtered to only"
                                                               " sendable locations in advance")

                self.remaining_true_jedi_check_shortnames.discard(shortname)
                new_location_checks.append(location_id)
            # `shortname` will only be removed from `self.remaining_true_jedi_gold_brick_shortnames` once the server
            # has updated `shortname` in datastorage and the client has acknowledged the datastorage update.
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

    def _check_minikits_from_current_area(self,
                                          current_area: ChapterArea,
                                          ctx: TCSContext,
                                          new_location_checks: list[int]):
        shortname = current_area.short_name
        if shortname not in self.remaining_minikit_checks_by_shortname:
            return

        remaining_minikits = self.remaining_minikit_checks_by_shortname[shortname]

        not_checked_minikit_checks: list[int] = []
        updated_remaining_minikits: list[tuple[int, str]] = []
        for count, location_name in remaining_minikits:
            location_id = LOCATION_NAME_TO_ID[location_name]
            if ctx.is_location_unchecked(location_id):
                not_checked_minikit_checks.append(location_id)
                updated_remaining_minikits.append((count, location_name))
        if updated_remaining_minikits:
            self.remaining_minikit_checks_by_shortname[shortname] = updated_remaining_minikits

            minikit_count = ctx.read_uchar(CURRENT_AREA_MINIKIT_COUNT_ADDRESS)
            zipped = zip(updated_remaining_minikits, not_checked_minikit_checks, strict=True)
            for (count, _name), location_id in zipped:
                if minikit_count >= count:
                    new_location_checks.append(location_id)
        else:
            del self.remaining_minikit_checks_by_shortname[shortname]

    def update_from_datastorage(self,
                                ctx: TCSContext,
                                new_true_jedi_area_ids: Iterable[int] = (),
                                new_minikits_gold_brick_area_ids: Iterable[int] = (),
                                new_power_brick_area_ids: Iterable[int] = ()):
        # todo: Replace the magic numbers used to get addresses, or at least move them to ChapterArea.
        for area_id in new_true_jedi_area_ids:
            area = AREA_ID_TO_CHAPTER_AREA[area_id]
            # There are two bytes for True Jedi, seemingly as a leftover from when there used to be separate True Jedi
            # for Story and Free Play, which got combined into just one True Jedi at some point in development.
            true_jedi_address = area.address + 2
            ctx.write_bytes(true_jedi_address, b"\x01\x01", 2)
            self.remaining_true_jedi_gold_brick_shortnames.discard(area.short_name)
        for area_id in new_minikits_gold_brick_area_ids:
            area = AREA_ID_TO_CHAPTER_AREA[area_id]
            gold_brick_address = area.address + 4
            ctx.write_byte(gold_brick_address, 1)
        for area_id in new_power_brick_area_ids:
            area = AREA_ID_TO_CHAPTER_AREA[area_id]
            power_brick_address = area.address + 6
            ctx.write_byte(power_brick_address, 1)

    def _check_true_jedi_power_bricks_and_minikits_from_save_data(self, ctx: TCSContext, new_location_checks: list[int]
                                                                  ) -> list[int]:
        # todo: More smartly read only as many bytes as necessary. So only 1 byte when either the True Jedi is complete
        #  or all Minikits have been collected.
        # todo: Use a NamedTuple instead of tuple[int, int, int, int]
        cached_bytes: dict[str, tuple[int, int, int, int]] = {}

        def get_bytes_for_short_name(short_name: str):
            if short_name in cached_bytes:
                return cached_bytes[short_name]
            else:
                # True Jedi seems to be at the 4th byte (maybe it is the 3rd because they both get activated?), 10/10
                # Minikits Gold Brick is at the 5th byte, and Minikit count is at the 6th byte. To reduce memory reads,
                # all are retrieved simultaneously.
                #
                read_bytes = ctx.read_bytes(SHORT_NAME_TO_CHAPTER_AREA[short_name].address + 3, 4)
                true_jedi_byte = read_bytes[0]
                minikit_gold_brick = read_bytes[1]
                minikit_count_byte = read_bytes[2]
                power_brick_byte = read_bytes[3]
                new_bytes = (true_jedi_byte, minikit_gold_brick, minikit_count_byte, power_brick_byte)
                cached_bytes[short_name] = new_bytes
                return new_bytes

        # Completed Gold Bricks to sync with Archipelago to support same-slot co-op/resuming an in-progress seed with a
        # new save file.
        completed_true_jedi_gold_brick_area_ids = []
        # Besides !collect and /send_location, both sets should be the same.
        for shortname in (self.remaining_true_jedi_gold_brick_shortnames | self.remaining_true_jedi_check_shortnames):
            location_name = LEVEL_COMMON_LOCATIONS[shortname]["True Jedi"]
            location_id = LOCATION_NAME_TO_ID[location_name]
            assert ctx.is_location_sendable(location_id), ("init_from_slot_data should have filtered to only sendable"
                                                           " locations in advance")

            is_checked = ctx.is_location_checked(location_id)
            if is_checked:
                # The location has been checked, but potentially by !collect instead of by the player.
                # The client no longer needs to send this location ID to the server, but the location being !collect-ed
                # does not give the player the Gold Brick for completing True Jedi, so the player may still need to get
                # the Gold Brick if they have locations locked behind Gold Bricks.
                self.remaining_true_jedi_check_shortnames.discard(shortname)

            if shortname in self.remaining_true_jedi_gold_brick_shortnames:
                # The client does not think the True Jedi Gold Brick has been given/earned yet, so check if that is the
                # case.
                true_jedi = get_bytes_for_short_name(shortname)[0]
                if true_jedi:
                    area_id = SHORT_NAME_TO_CHAPTER_AREA[shortname].area_id
                    # Add the area ID to the area IDs to send to the server.
                    completed_true_jedi_gold_brick_area_ids.append(area_id)
                    if not is_checked:
                        new_location_checks.append(location_id)

        updated_remaining_minikit_checks_by_shortname: dict[str, list[tuple[int, str]]] = {}
        for shortname, remaining_minikits in self.remaining_minikit_checks_by_shortname.items():
            not_checked_minikit_checks: list[int] = []
            updated_remaining_minikits: list[tuple[int, str]] = []
            for count, location_name in remaining_minikits:
                location_id = LOCATION_NAME_TO_ID[location_name]
                if ctx.is_location_unchecked(location_id):
                    not_checked_minikit_checks.append(location_id)
                    updated_remaining_minikits.append((count, location_name))
            if updated_remaining_minikits:
                updated_remaining_minikit_checks_by_shortname[shortname] = updated_remaining_minikits

                minikit_count = get_bytes_for_short_name(shortname)[2]
                zipped = zip(updated_remaining_minikits, not_checked_minikit_checks, strict=True)
                for (count, _name), location_id in zipped:
                    if minikit_count >= count:
                        new_location_checks.append(location_id)
        self.remaining_minikit_checks_by_shortname = updated_remaining_minikit_checks_by_shortname

        # There are no locations tied to getting the Gold Brick for collecting all Minikits in a Chapter, but the Gold
        # Bricks are written to datastorage to sync Gold Bricks in same-slot co-op, and so that the PopTracker pack can
        # determine how many, and which Gold Bricks have been acquired.
        newly_completed_10_minikits_gold_bricks_area_ids: list[int] = []
        updated_remaining_minikit_gold_bricks_by_area_id: set[int] = set()
        for area_id in self.remaining_minikit_gold_bricks_by_area_id:
            shortname = AREA_ID_TO_CHAPTER_AREA[area_id].short_name
            gold_brick = get_bytes_for_short_name(shortname)[1]
            if gold_brick:
                newly_completed_10_minikits_gold_bricks_area_ids.append(area_id)
            else:
                updated_remaining_minikit_gold_bricks_by_area_id.add(area_id)
        ctx.update_datastorage_10_minikits_completion(newly_completed_10_minikits_gold_bricks_area_ids)
        self.remaining_minikit_gold_bricks_by_area_id = updated_remaining_minikit_gold_bricks_by_area_id

        newly_completed_power_brick_area_ids: list[int] = []
        updated_remaining_power_bricks_by_area_id: set[int] = set()
        for area_id in self.remaining_power_bricks_by_area_id:
            shortname = AREA_ID_TO_CHAPTER_AREA[area_id].short_name
            power_brick = get_bytes_for_short_name(shortname)[3]
            if power_brick:
                newly_completed_power_brick_area_ids.append(area_id)
            else:
                updated_remaining_power_bricks_by_area_id.add(area_id)
        ctx.update_datastorage_power_bricks_collected(newly_completed_power_brick_area_ids)
        self.remaining_power_bricks_by_area_id = updated_remaining_power_bricks_by_area_id

        return completed_true_jedi_gold_brick_area_ids
