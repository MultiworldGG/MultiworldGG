from .common_types import MusicMapping
from .constants.game_data import sound_data_entries
from .mf.constants.music_library import MusicLibrary as MusicLibraryMF
from .rom import Rom
from .zm.constants.music_library import MusicLibrary as MusicLibraryZM

SOUND_SIZE = 8


def set_sounds(rom: Rom, data: MusicMapping) -> None:
    read_data_entries = []

    MusicLibrary: type[MusicLibraryMF] | type[MusicLibraryZM]
    if rom.is_mf():
        MusicLibrary = MusicLibraryMF
    elif rom.is_zm():
        MusicLibrary = MusicLibraryZM

    # Read new data
    for new in data.values():
        read_location = sound_data_entries(rom) + SOUND_SIZE * MusicLibrary[new].value
        read_data_entries.append(rom.read_bytes(read_location, SOUND_SIZE))

    # Write to rom
    for original, sound_data in zip(data.keys(), read_data_entries):
        write_location = sound_data_entries(rom) + SOUND_SIZE * MusicLibrary[original].value
        rom.write_bytes(write_location, sound_data)
