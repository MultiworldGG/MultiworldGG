import struct
import logging

from . import ClientComponent
from ..events import (
    subscribe_event,
    OnReceiveSlotDataEvent,
    OnAreaChangeEvent,
    OnGameWatcherTickEvent,
    OnLevelChangeEvent,
)
from ..type_aliases import TCSContext, ApLocationId

from ...data.areas import Area
from ...data.levels import Level
from ...data.locations import LOCATION_NAME_TO_ID
from ...data.logic import ALL_CHAPTERS

_MINIKIT_EMPTY_NAME = b"\x00" * 8

_CURRENT_AREA_NEW_MINIKITS_ARRAY = 0x955ff0
_CURRENT_AREA_NEW_MINIKITS_ELEMENT_SIZE = 0xc
_CURRENT_AREA_NEW_MINIKITS_RELEVANT_ELEMENT_SIZE = 0xa  # The last two bytes are unknown and appear to always be zero.
_CURRENT_AREA_NEW_MINIKITS_ELEMENT_COUNT = 10
_CURRENT_AREA_NEW_MINIKITS_ARRAY_SIZE = (_CURRENT_AREA_NEW_MINIKITS_ELEMENT_SIZE
                                         * _CURRENT_AREA_NEW_MINIKITS_ELEMENT_COUNT)
_CURRENT_AREA_NEW_MINIKITS_EMPTY_ELEMENT = b"\x00" * _CURRENT_AREA_NEW_MINIKITS_RELEVANT_ELEMENT_SIZE


_SAVE_DATA_MINIKITS_ARRAY = Level(0).minikits_save_data_addr
# 10 * 8 bytes of null terminated strings, plus one byte
_SAVE_DATA_MINIKITS_ELEMENT_SIZE = 0x8 * 10 + 1
_SAVE_DATA_MINIKITS_RELEVANT_ELEMENT_SIZE = _SAVE_DATA_MINIKITS_ELEMENT_SIZE - 1
_SAVE_DATA_MINIKITS_EMPTY_ELEMENT = b"\x00" * _SAVE_DATA_MINIKITS_RELEVANT_ELEMENT_SIZE


_LOGGER = logging.getLogger("Client")


def _make_level_to_minikits_data() -> dict[bytes, ApLocationId]:
    level_minikits_bytes_to_ap_id: dict[bytes, ApLocationId] = {}
    for chapter in ALL_CHAPTERS:
        area = chapter.area
        for level, minikits_data in chapter.level_minikits.items():
            assert level not in level_minikits_bytes_to_ap_id
            for minikit_name in minikits_data.keys():
                # 8 byte string, followed by a short.
                minikit_bytes = struct.pack(b"<8sh", minikit_name.encode("utf-8"), level)
                location_id = LOCATION_NAME_TO_ID[area.prefix_name(minikit_name)]
                level_minikits_bytes_to_ap_id[minikit_bytes] = location_id
    return level_minikits_bytes_to_ap_id


def _make_per_level_minikits_to_ap_id() -> dict[Level, dict[bytes, ApLocationId]]:
    per_level_minikits_to_ap_ids: dict[Level, dict[bytes, ApLocationId]] = {}
    for chapter in ALL_CHAPTERS:
        area = chapter.area
        for level, minikits_data in chapter.level_minikits.items():
            level_minikits_to_ap_ids: dict[bytes, ApLocationId] = {}
            assert level not in level_minikits_to_ap_ids
            per_level_minikits_to_ap_ids[level] = level_minikits_to_ap_ids
            for minikit_name, minikit_data in minikits_data.items():
                location_id = LOCATION_NAME_TO_ID[area.prefix_name(minikit_name)]
                pickup_names = minikit_data.pickup_names
                for pickup_name in pickup_names:
                    # Right pad to the full 8 bytes with b"\x00".
                    minikit_bytes = struct.pack(b"<8s", pickup_name.encode("utf-8"))
                    level_minikits_to_ap_ids[minikit_bytes] = location_id
    return per_level_minikits_to_ap_ids


_PER_LEVEL_MINIKITS_TO_AP_IDS: dict[Level, dict[bytes, ApLocationId]] = _make_per_level_minikits_to_ap_id()
_LEVEL_MINIKITS_BYTES_TO_AP_IDS: dict[tuple[bytes, int], ApLocationId] = {
    # 8 byte, null-terminated string, followed by a short.
    (minikit_bytes.rstrip(b"\x00"), level.value): ap_location_id
    for level, per_level_minikits in _PER_LEVEL_MINIKITS_TO_AP_IDS.items()
    for minikit_bytes, ap_location_id in per_level_minikits.items()
}


class MinikitChecker(ClientComponent):
    _on_tick_active: bool = False
    _checked_locations: set[int]
    _enabled_chapter_levels_with_minikits: set[Level]
    _initial_save_data_check_done: bool = False

    def __init__(self):
        self._checked_locations = set()
        self._enabled_chapter_levels_with_minikits = set()

    @subscribe_event
    def on_receive_slot_data(self, event: OnReceiveSlotDataEvent) -> None:
        for area in event.slot_data.enabled_chapters.value:
            self._enabled_chapter_levels_with_minikits.update(area.get_playable_levels())
        # Not all levels contain minikits.
        self._enabled_chapter_levels_with_minikits.intersection_update(_PER_LEVEL_MINIKITS_TO_AP_IDS)

    @subscribe_event
    async def on_area_change(self, event: OnAreaChangeEvent) -> None:
        # Always check the save data the first time, then only check the save data when returning to the Cantina.
        if event.new_area_data_id == Area.MAP or not self._initial_save_data_check_done:
            self._check_save_data_minikits(event.context)
            self._initial_save_data_check_done = True

    @subscribe_event
    def on_level_change(self, event: OnLevelChangeEvent) -> None:
        self._on_tick_active = event.new_level_id in _PER_LEVEL_MINIKITS_TO_AP_IDS

    @subscribe_event
    async def on_tick(self, event: OnGameWatcherTickEvent) -> None:
        if not self._on_tick_active:
            return

        self._check_current_area_new_minikits(event.context)

    def _check_save_data_minikits(self, ctx: TCSContext) -> None:
        for level in self._enabled_chapter_levels_with_minikits:
            minikit_to_ap_id = _PER_LEVEL_MINIKITS_TO_AP_IDS[level]
            sub_array_addr = level.minikits_save_data_addr
            minikits_bytes_array = ctx.read_bytes(sub_array_addr, _SAVE_DATA_MINIKITS_RELEVANT_ELEMENT_SIZE)
            minikit_bytes: bytes
            if minikits_bytes_array == _SAVE_DATA_MINIKITS_EMPTY_ELEMENT:
                # The entire array is empty, so skip and check the next Level.
                continue
            for i in range(0, _SAVE_DATA_MINIKITS_RELEVANT_ELEMENT_SIZE, 8):
                minikit_bytes = minikits_bytes_array[i:i + 8]
                if minikit_bytes == _MINIKIT_EMPTY_NAME:
                    # There is no need to iterate any further because minikit names are inserted into the earliest free
                    # space in the array.
                    break
                if minikit_bytes not in minikit_to_ap_id:
                    _LOGGER.error("Could not find AP location id for minikit %r in level %r. Report this as a bug.",
                                  minikit_bytes, level)
                    continue
                self._checked_locations.add(minikit_to_ap_id[minikit_bytes])


    def _check_current_area_new_minikits(self, ctx: TCSContext) -> None:
        current_area_minikits = ctx.read_bytes(_CURRENT_AREA_NEW_MINIKITS_ARRAY, _CURRENT_AREA_NEW_MINIKITS_ARRAY_SIZE)
        for i in range(0, _CURRENT_AREA_NEW_MINIKITS_ARRAY_SIZE, _CURRENT_AREA_NEW_MINIKITS_ELEMENT_SIZE):
            # Truncate to only the relevant bytes.
            element = current_area_minikits[i:i+_CURRENT_AREA_NEW_MINIKITS_RELEVANT_ELEMENT_SIZE]
            if element == _CURRENT_AREA_NEW_MINIKITS_EMPTY_ELEMENT:
                # There is no need to iterate any further.
                # Note that 0x951254 says how many elements are in the array, so the client could read that instead.
                break
            minikit_name_bytes: bytes
            level_id: int
            minikit_name_bytes, level_id = struct.unpack("<8sh", element)
            minikit_name_bytes = minikit_name_bytes.partition(b"\x00")[0]
            key = (minikit_name_bytes, level_id)
            if key not in _LEVEL_MINIKITS_BYTES_TO_AP_IDS:
                _LOGGER.error("Could not find AP location id for minikit %r. Report this as a bug.", key)
                continue
            self._checked_locations.add(_LEVEL_MINIKITS_BYTES_TO_AP_IDS[key])


    async def check_minikits(self, ctx: TCSContext, new_location_checks: list[int]) -> None:
        self._checked_locations.difference_update(ctx.checked_locations)
        new_location_checks.extend(self._checked_locations)
