from collections.abc import Sequence

from ...patching.RomData import RomData
from ...patching.z80asm.Assembler import GameboyAddress
from ..microbmp import MicroBMP


def draw_tile(image: MicroBMP, sprite_data: Sequence[int], x: int, y: int, address: int) -> None:
    if address >= len(sprite_data):
        return

    for j in range(0, 16):
        b1 = sprite_data[address + j * 2]
        b2 = sprite_data[address + j * 2 + 1]
        for i in range(0, 8):
            c = (b1 & 1) | ((b2 & 1) << 1)
            b1 >>= 1
            b2 >>= 1

            image[x + (7 - i), y + j] = c


def load_link_data(rom_data: RomData) -> Sequence[int]:
    return rom_data.read_bytes(GameboyAddress(0x1a, 0x4000).address_in_rom(), 0x22E0)


def load_link_sprite(sprite_data: Sequence[int], separator: bool = False) -> MicroBMP:
    # Standalone uses 16, 18
    # Vanilla data is 279, or 3 * 3 * 31
    target_width = 16
    target_height = 18
    if separator:
        tile_shift_x = 9
        tile_shift_y = 17
        link_sprite = MicroBMP(target_width * 9 - 1, target_height * 17 - 1, depth=8)
    else:
        tile_shift_x = 8
        tile_shift_y = 16
        link_sprite = MicroBMP(target_width * 8, target_height * 16, depth=8)

    assert isinstance(link_sprite.DIB_w, int)
    assert isinstance(link_sprite.DIB_h, int)
    for i in range(link_sprite.DIB_w):
        for j in range(link_sprite.DIB_h):
            link_sprite[i, j] = 4

    for y in range(target_height):
        for x in range(target_width):
            tile_address = ((y * target_width) + x) * 0x20
            draw_tile(link_sprite, sprite_data, x * tile_shift_x, y * tile_shift_y, tile_address)

    return link_sprite
