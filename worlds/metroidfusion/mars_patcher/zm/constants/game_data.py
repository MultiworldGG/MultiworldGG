from ...rom import Rom
from .reserved_space import ReservedPointersZM


def chozo_statue_targets_addr(rom: Rom) -> int:
    return rom.read_ptr(ReservedPointersZM.CHOZO_STATUE_TARGETS_PTR.value)


def intro_cutscene_data_addr(rom: Rom) -> int:
    return rom.read_ptr(ReservedPointersZM.INTRO_CUTSCENE_DATA_PTR.value)


def starting_info_addr(rom: Rom) -> int:
    return rom.read_ptr(ReservedPointersZM.STARTING_INFO_PTR.value)


def major_locations_addr(rom: Rom) -> int:
    return rom.read_ptr(ReservedPointersZM.MAJOR_LOCATIONS_PTR.value)


def minor_locations_addr(rom: Rom) -> int:
    return rom.read_ptr(ReservedPointersZM.MINOR_LOCATIONS_PTR.value)


def message_text_addr(rom: Rom) -> int:
    return rom.read_ptr(ReservedPointersZM.MESSAGE_TEXT_PTR.value)


def story_text_addr(rom: Rom) -> int:
    return rom.read_ptr(ReservedPointersZM.STORY_TEXT_PTR.value)


def difficulty_options_addr(rom: Rom) -> int:
    return rom.read_ptr(ReservedPointersZM.DIFFICULTY_OPTIONS_PTR.value)


def default_stereo_addr(rom: Rom) -> int:
    return rom.read_ptr(ReservedPointersZM.DEFAULT_STEREO_PTR.value)


def metroid_sprite_stats_addr(rom: Rom) -> int:
    return rom.read_ptr(ReservedPointersZM.METROID_SPRITE_STATS_PTR.value)


def black_pirates_require_plasma_addr(rom: Rom) -> int:
    return rom.read_ptr(ReservedPointersZM.BLACK_PIRATES_REQUIRE_PLASMA_PTR.value)


def skip_door_transitions_addr(rom: Rom) -> int:
    return rom.read_ptr(ReservedPointersZM.SKIP_DOOR_TRANSITIONS_PTR.value)


def ball_launcher_without_bombs_addr(rom: Rom) -> int:
    return rom.read_ptr(ReservedPointersZM.BALL_LAUNCHER_WITHOUT_BOMBS_PTR.value)


def remove_cutscenes_addr(rom: Rom) -> int:
    return rom.read_ptr(ReservedPointersZM.REMOVE_CUTSCENES_PTR.value)


def fast_item_grab_addr(rom: Rom) -> int:
    return rom.read_ptr(ReservedPointersZM.FAST_ITEM_GRAB_PTR.value)


def reveal_hidden_tiles_addr(rom: Rom) -> int:
    return rom.read_ptr(ReservedPointersZM.REVEAL_HIDDEN_TILES.value)


def skip_suitless_sequence_addr(rom: Rom) -> int:
    return rom.read_ptr(ReservedPointersZM.SKIP_SUITLESS_SEQUENCE_PTR.value)


def tank_increase_amounts_addr(rom: Rom) -> int:
    return rom.read_ptr(ReservedPointersZM.TANK_INCREASE_AMOUNTS_PTR.value)


def title_text_lines_addr(rom: Rom) -> int:
    return rom.read_ptr(ReservedPointersZM.TITLE_TEXT_LINES_PTR.value)


def seed_hash_addr(rom: Rom) -> int:
    return rom.read_ptr(ReservedPointersZM.SEED_HASH_PTR.value)


def gunship_flashing_palette_addr(rom: Rom) -> int:
    return rom.read_ptr(ReservedPointersZM.GUNSHIP_FLASHING_PALETTE_PTR.value)


def statues_cutscene_palette_addr(rom: Rom) -> int:
    return rom.read_ptr(ReservedPointersZM.STATUES_CUTSCENE_PALETTE_PTR.value)
