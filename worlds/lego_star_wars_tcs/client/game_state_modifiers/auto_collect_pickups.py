from enum import IntFlag

from ..common import ClientComponent, StaticPointer, UintField
from ..custom_save_data import CustomSaveFlags1
from ..events import subscribe_event, OnReceiveSlotDataEvent
from ..type_aliases import TCSContext
from ...options import AutoCollectSpawnedPickups

from ...data.areas import Area, BONUS_ROOM_BONUSES
from ...data.levels import Level


# Levels within these areas already auto-collect spawned pickups, though through a different means than setting the flag
# that this component sets on level data.
_EXCLUDED_CHAPTER_AREAS = {
    Area.PODSPRINT,
    Area.DOGFIGHT,
}
_EXCLUDED_BONUS_AREAS = {
    Area.PODRACE,
    Area.BONUS_GUNSHIP,
    Area.BONUS,
    Area.BONUS2,
}

_MAIN_AREAS: set[Area] = {
    Area.MAP,
    *[area for area in Area if area not in _EXCLUDED_CHAPTER_AREAS and area.is_chapter()],
    *[area for area in BONUS_ROOM_BONUSES if area not in _EXCLUDED_BONUS_AREAS],
}

_MAIN_LEVELS: set[Level] = set().union(
    *[area.get_playable_levels() for area in _MAIN_AREAS],
)
_VEHICLE_LEVELS: set[Level] = set().union(
    *[area.get_playable_levels() for area in _MAIN_AREAS if area.is_vehicle_area()],
)


P_L_DATA_LIST = StaticPointer(0x00951b98)
L_DATA_SIZE = 0x130
L_DATA_FLAG = UintField(0x64)


# Missing flag values are unknown.
class LevelDataFlag(IntFlag):
    FLAT_TERRAIN = 0x10
    INTRO_LEVEL = 0x20
    CUTSCENE_LEVEL = 0x40  # midtro level
    OUTRO_LEVEL = 0x80
    FIX_STROBING_ANIMS = 0x100
    TEST_LEVEL = 0x200
    STATUS_LEVEL = 0x400
    DOUBLE_SCORE = 0x800
    METAL = 0x1000
    CAMERA_RAIN = 0x4000
    TERRAIN_RAIN = 0x8000
    NEWGAME_LEVEL = 0x10000
    LOADGAME_LEVEL = 0x20000
    IN_SPACE = 0x40000
    PICKUPS_TO_PANEL = 0x80000
    FORGET_TAKEOVERS = 0x100000
    NARROW_SOCKS = 0x200000
    OVERRIDE_NOPICKUPGRAVITY = 0x400000
    HIDDEN_ICONS = 0x800000  # on = unset, off = set


class AutoCollectPickups(ClientComponent):
    enabled: bool = False
    vehicles_only: bool = False

    @subscribe_event
    def init_from_slot_data(self, event: OnReceiveSlotDataEvent):
        ctx = event.context
        if event.first_time_setup:
            # Read the value from slot data and write it into the save data.
            option = event.slot_data.auto_collect_spawned_pickups
            enabled = bool(option)
            vehicles_only = option == AutoCollectSpawnedPickups.option_vehicle_levels_only
            CustomSaveFlags1.AUTO_COLLECT_PICKUPS_ENABLED.set_bool(ctx, enabled)
            CustomSaveFlags1.AUTO_COLLECT_PICKUPS_VEHICLES_ONLY.set_bool(ctx, vehicles_only)
        else:
            # Read the value from the save data.
            enabled = CustomSaveFlags1.AUTO_COLLECT_PICKUPS_ENABLED.is_set(event.context)
            if enabled:
                vehicles_only = CustomSaveFlags1.AUTO_COLLECT_PICKUPS_VEHICLES_ONLY.is_set(ctx)
            else:
                vehicles_only = False

        self.update(ctx, enabled, vehicles_only, False)

    def update(self, ctx: TCSContext, enabled: bool, vehicles_only: bool, update_save_data: bool = True):
        if enabled:
            if vehicles_only:
                to_set = _VEHICLE_LEVELS
                to_unset = _MAIN_LEVELS - _VEHICLE_LEVELS
            else:
                to_set = _MAIN_LEVELS
                to_unset = ()
        else:
            to_set = ()
            to_unset = _MAIN_LEVELS

        bit_value: int = LevelDataFlag.PICKUPS_TO_PANEL.value
        l_data = P_L_DATA_LIST.to_array(ctx, L_DATA_SIZE)

        for level in to_set:
            flag_address = l_data[level]
            flag = L_DATA_FLAG.get(ctx, flag_address)
            updated_flag = flag | bit_value
            L_DATA_FLAG.set(ctx, flag_address, updated_flag)

        for level in to_unset:
            flag_address = l_data[level]
            flag = L_DATA_FLAG.get(ctx, flag_address)
            updated_flag = flag & ~bit_value
            L_DATA_FLAG.set(ctx, flag_address, updated_flag)

        if update_save_data:
            if enabled != self.enabled:
                CustomSaveFlags1.AUTO_COLLECT_PICKUPS_ENABLED.set_bool(ctx, enabled)
            if vehicles_only != self.vehicles_only:
                CustomSaveFlags1.AUTO_COLLECT_PICKUPS_VEHICLES_ONLY.set_bool(ctx, vehicles_only)
        self.enabled = enabled
        self.vehicles_only = vehicles_only

