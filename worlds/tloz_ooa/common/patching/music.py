import random
from enum import Enum
from typing import List, Tuple, Dict, Set, Any

class Game(Enum):
    Seasons = 1
    Ages = 2

# Constants
SOUND_POINTER_TABLE_OFFSETS = {
    Game.Seasons: (0x39 - 1) * 0x4000 + 0x57cf,
    Game.Ages: (0x39 - 1) * 0x4000 + 0x5748,
}
SOUND_PTR_SIZE = 3
SOUND_PTR_ADDR_IS_LITTLE_ENDIAN = True

UNUSED_INDICES = {0x00, 0x37, 0x3a, 0x3b, 0x41, 0x42, 0x43, 0x44, 0x45,
                  0x47, 0x48, 0x49, 0x4b, 0x97}

JINGLE_INDICES = {0x06, 0x10, 0x40}

GAME_SPECIFIC_MUSIC_INDICES = {
    Game.Seasons: {0x3d},
    Game.Ages: {0x24, 0x30},
}

BASE_MUSIC_INDICES = set(range(0x4c)) - UNUSED_INDICES - JINGLE_INDICES - \
                     GAME_SPECIFIC_MUSIC_INDICES[Game.Seasons] - GAME_SPECIFIC_MUSIC_INDICES[Game.Ages]

GAME_SPECIFIC_SFX_INDICES = {
    Game.Seasons: set(),
    Game.Ages: {0xa1, 0xad, 0xb6, 0xd4},
}

LOOPING_SFX_INDICES = {0xb9, 0xc2}

BASE_SFX_INDICES = set(range(0x4c, 0xd5)) - UNUSED_INDICES - LOOPING_SFX_INDICES - \
                   GAME_SPECIFIC_SFX_INDICES[Game.Seasons] - GAME_SPECIFIC_SFX_INDICES[Game.Ages]

def format_offset(offset: int) -> str:
    return f"0x{offset:04x}"

def read_sound_ptr(view: memoryview, offset: int) -> Tuple[int, int]:
    bank_offset = view[offset]
    addr = int.from_bytes(view[offset+1:offset+3], byteorder='little' if SOUND_PTR_ADDR_IS_LITTLE_ENDIAN else 'big')
    if bank_offset > 0x3f or addr < 0x4000 or addr > 0x7fff:
        msg = 'Read invalid sound pointer at ' + format_offset(offset)
        raise ValueError(msg)
    return (bank_offset, addr)

def write_sound_ptr(view: memoryview, offset: int, ptr: Tuple[int, int]) -> None:
    view[offset] = ptr[0]
    view[offset+1:offset+3] = ptr[1].to_bytes(2, byteorder='little' if SOUND_PTR_ADDR_IS_LITTLE_ENDIAN else 'big')

def shuffle(array: List[Any]) -> List[Any]:
    """Fisher-Yates shuffle algorithm"""
    copy = array.copy()
    for i in range(len(copy)-1, 0, -1):
        j = random.randint(0, i)
        copy[i], copy[j] = copy[j], copy[i]
    return copy

def shuffle_audio(rom: bytearray, indices: Set[int], game: Game) -> None:
    view = memoryview(rom)
    offset = SOUND_POINTER_TABLE_OFFSETS[game]
    ptrs = [read_sound_ptr(view, offset + i * SOUND_PTR_SIZE) for i in indices]
    shuffled_ptrs = shuffle(ptrs)
    for i, ptr in zip(indices, shuffled_ptrs):
        write_sound_ptr(view, offset + i * SOUND_PTR_SIZE, ptr)

def shuffle_music(rom: bytearray, game: Game) -> bytes:
    indices = BASE_MUSIC_INDICES.union(GAME_SPECIFIC_MUSIC_INDICES[game])
    shuffle_audio(rom, indices, game)
    return bytes(rom)

def shuffle_sfx(rom: bytearray, game: Game) -> bytes:
    indices = BASE_SFX_INDICES.union(GAME_SPECIFIC_SFX_INDICES[game])
    shuffle_audio(rom, indices, game)
    return bytes(rom)