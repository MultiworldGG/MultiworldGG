import math
from typing import cast

from worlds.tloz_oos.common.spriter.microbmp import MicroBMP

from . import blue_palette, bw_palette, green_palette, orange_palette, red_palette


def has_separator(image: MicroBMP) -> bool:
    if cast(int, image.DIB_w) > 8:
        return image[8, 0] == 4

    # Just to cover the case where it's a single column
    return image[0, 8] == 4


def encode_tile(image: MicroBMP, x: int, y: int) -> bytearray:
    data = bytearray(32)

    for j in range(16):
        b1 = 0
        b2 = 0
        for i in range(8):
            c = cast(int, image[x + (7 - i), y + j])
            assert c < 4

            b1 |= (c & 1) << i
            b2 |= ((c >> 1) & 1) << i

        data[j * 2] = b1
        data[j * 2 + 1] = b2

    return data


def encode_sprite(image: MicroBMP) -> bytearray:
    x = y = 0
    sprite_data = bytearray()
    if has_separator(image):
        x_step = 9
        y_step = 17
    else:
        x_step = 8
        y_step = 16

    for _sprite_id in range(279):
        sprite_data.extend(encode_tile(image, x, y))
        x += x_step
        if x >= cast(int, image.DIB_w):
            x = 0
            y += y_step
    return sprite_data


def remap_sprite(image: MicroBMP) -> None:
    image_palette = cast(list[bytearray], image.palette)
    candidate_palettes = [bw_palette, green_palette, blue_palette, red_palette, orange_palette]
    mapping_attempt: dict[int, tuple[int, list[int]]] = {key: (0, []) for key in range(len(candidate_palettes))}
    for palette_color in image_palette:
        for palette_id in range(len(candidate_palettes)):
            palette = candidate_palettes[palette_id]
            error = 0x1000
            match = -1
            for color_id in range(5):
                color = palette[color_id]
                current_error = 0
                for component in range(3):
                    current_error += abs(color[component] - palette_color[component])
                if current_error < error:
                    error = current_error
                    match = color_id

            previous_error, palette_mapping = mapping_attempt[palette_id]
            palette_mapping.append(match)
            mapping_attempt[palette_id] = (previous_error + error, palette_mapping)

    chosen_palette = []
    best_error = math.inf
    best_mapping: list[int] = []
    for palette_id in range(len(candidate_palettes)):
        error, mapping = mapping_attempt[palette_id]
        if error < best_error:
            best_error = error
            best_mapping = mapping
            chosen_palette = candidate_palettes[palette_id]

    image.palette = chosen_palette
    for x in range(cast(int, image.DIB_w)):
        for y in range(cast(int, image.DIB_h)):
            image[x, y] = best_mapping[cast(int, image[x, y])]
