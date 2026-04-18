from . import ClientComponent
from ..common import StaticUint, FloatField
from ..common_addresses import IS_CHARACTER_SWAPPING_ENABLED
from ..events import subscribe_event, OnLevelChangeEvent

from ...items import CHARACTERS_AND_VEHICLES_BY_NAME

LUKE_DAGOBAH_ID = CHARACTERS_AND_VEHICLES_BY_NAME["Luke Skywalker (Dagobah)"].character_index
A_VEHICLE_CHARACTER_ID = CHARACTERS_AND_VEHICLES_BY_NAME["Sebulba's Pod"].character_index
LEVEL_ID_DAGOBAH_H = 240
LUKE_DAGOBAH_ID_ADDR = StaticUint(0x7f198c)

YODA_IDS = [CHARACTERS_AND_VEHICLES_BY_NAME[name].character_index for name in ["Yoda", "Yoda (Ghost)"]]
LEVEL_ID_VADER_A = 136
GCDataList_ADDR = StaticUint(0x93b284)  # CharacterEntry*
SIZE_OF_CHARACTER_ENTRY = 0x120
YODA_RUN_SPEED = 0.8
CHARACTER_ENTRY_RUN_SPEED = FloatField(0x1c)


def fix_luke_skywalker_dagobah(event: OnLevelChangeEvent):
    """
    'Fixes' `Luke Skywalker (Dagobah)` being hardcoded to be unable to lift the X-Wing at the end of Dagobah, which is
    required to complete the chapter.

    The 'fix' is performed by overwriting the character ID that the game checks for when in the final level in Dagobah.
    """
    if event.new_level_id == LEVEL_ID_DAGOBAH_H and IS_CHARACTER_SWAPPING_ENABLED.get(event.context):
        LUKE_DAGOBAH_ID_ADDR.set(event.context, A_VEHICLE_CHARACTER_ID)
    else:
        LUKE_DAGOBAH_ID_ADDR.set(event.context, LUKE_DAGOBAH_ID)


def fix_yodas_3_6_vader_a(event: OnLevelChangeEvent):
    """
    'Fixes' AI `Yoda` and `Yoda (Ghost)` being unable to complete VADER_A because of their lower run speed.

    The 'fix' is performed by overwriting the characters' run speeds to be faster while in VADER_A.
    """
    base_addr = GCDataList_ADDR.get(event.context)
    if event.new_level_id == LEVEL_ID_VADER_A:
        new_run_speed = 1.0
    else:
        new_run_speed = YODA_RUN_SPEED
    for yoda_id in YODA_IDS:
        CHARACTER_ENTRY_RUN_SPEED.set(event.context, base_addr + SIZE_OF_CHARACTER_ENTRY * yoda_id, new_run_speed)


class LevelSpecificFixes(ClientComponent):
    """
    Various level-specific fixes.
    """
    @subscribe_event
    def on_level_change(self, event: OnLevelChangeEvent):
        fix_luke_skywalker_dagobah(event)
        fix_yodas_3_6_vader_a(event)
