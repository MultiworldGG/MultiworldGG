from ..constants.game_data import sound_count, sound_data_entries
from ..rom import Rom
from .constants.game_data import (
    default_stereo_addr,
    fast_item_grab_addr,
    remove_cutscenes_addr,
    reveal_hidden_tiles_addr,
    skip_door_transitions_addr,
)

# def _get_patch_path(rom: Rom, subfolder: str, filename: str) -> str:
#     dir = f"{rom.game.name}_{rom.region.name}".lower()
#     return get_data_path("patches", dir, subfolder, filename)


# def apply_base_patch(rom: Rom) -> None:
#     path = _get_patch_path(rom, "asm", "m4rs.bps")
#     with open(path, "rb") as f:
#         patch = f.read()
#     rom.data = BpsDecoder().apply_patch(patch, rom.data)


def skip_door_transitions(rom: Rom) -> None:
    rom.write_8(skip_door_transitions_addr(rom), 1)


def stereo_default(rom: Rom) -> None:
    rom.write_8(default_stereo_addr(rom), 1)


def disable_sounds(rom: Rom, start: int, end: int, exclude: set[int] = set()) -> None:
    sound_data_addr = sound_data_entries(rom)
    for idx in range(start, end):
        if idx not in exclude:
            addr = sound_data_addr + idx * 8
            rom.write_8(rom.read_ptr(addr), 0)


def disable_music(rom: Rom) -> None:
    # Exclude jingles
    exclude = {
        54,  # Loading save
        55,  # Major obtained
        58,  # Minor obtained
        66,  # Unknown item
        74,  # Fully powered suit
    }
    disable_sounds(rom, 0, 100, exclude)


def disable_sound_effects(rom: Rom) -> None:
    disable_sounds(rom, 100, sound_count(rom))


def remove_cutscenes(rom: Rom) -> None:
    rom.write_8(remove_cutscenes_addr(rom), 1)


def fast_item_grab(rom: Rom) -> None:
    rom.write_8(fast_item_grab_addr(rom), 1)


# def apply_unexplored_map(rom: Rom) -> None:
#     pass


def apply_reveal_hidden_tiles(rom: Rom) -> None:
    rom.write_8(reveal_hidden_tiles_addr(rom), 1)


# def apply_reveal_unexplored_doors(rom: Rom) -> None:
#     pass
