import json
import os
import struct
from collections import Counter, defaultdict

# SNES $18C000 -> PC 0xC4000 (LoROM). Overworld map check graphics live here.
OW_MAP_SNES_ADDR = 0x18C000
OW_MAP_PC_ADDR = ((OW_MAP_SNES_ADDR & 0x7F0000) >> 1) | (OW_MAP_SNES_ADDR & 0x7FFF)
OW_MAP_SIZE = 0x4000  # 128x128 8bpp
OW_MAP_WIDTH = 128
OW_MAP_HEIGHT = 128
OW_TILE_SIZE = 8
# ROM stores the 128x128 map as 8x8 tiles, row-major tiles, row-major pixels in each tile.
SPARSE_SKIP = 0xFF  # matches vanilla color; skipped when writing to ROM
# Sparse whole-tile patch BMP produced by data/overworld/make_ow_map_diff.py
DEFAULT_MAP_BMP = os.path.join('data', 'overworld', 'gridOWmap.bmp')

# LW/DW overworld map tilemaps.
# Tooling (ZScream / Tilemap Studio) exports a linear 64x64 tilemap (0x1000).
# ROM layout:
#   LW $0AC739: 0x1000 bytes as four 32x32 quadrants, row-major TL,TR,BL,BR
#   DW $0AD739: 0x400 bytes = center 32x32 of the 64x64 map (linear).
#               Must not write past $0ADB39 (overworld map palette follows).
OW_TILEMAP_ASSET_SIZE = 0x1000  # exported 64x64 bins
OW_LW_TILEMAP_SIZE = 0x1000
OW_DW_TILEMAP_SIZE = 0x400
OW_TILEMAP_WIDTH = 64
OW_TILEMAP_HEIGHT = 64
OW_TILEMAP_BLOCK = 32
OW_LW_TILEMAP_SNES_ADDR = 0x0AC739
OW_DW_TILEMAP_SNES_ADDR = 0x0AD739
DEFAULT_LW_TILEMAP_BIN = os.path.join('data', 'overworld', 'gridOWmap-LW.bin')
DEFAULT_DW_TILEMAP_BIN = os.path.join('data', 'overworld', 'gridOWmap-DW.bin')


def snes_to_pc(value):
    return ((value & 0x7F0000) >> 1) | (value & 0x7FFF)


def read_rom_bytes(rom_path):
    with open(rom_path, 'rb') as stream:
        buffer = bytearray(stream.read())
    if len(buffer) % 0x400 == 0x200:
        buffer = buffer[0x200:]
    return buffer


def get_rom_path_from_settings(repo_root=None):
    if repo_root is None:
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    user_dir = os.path.join(repo_root, 'resources', 'user')

    def load_json(path):
        if not os.path.isfile(path):
            return {}
        with open(path, 'rt', encoding='utf-8') as fh:
            return json.load(fh)

    settings = load_json(os.path.join(user_dir, 'settings.json'))
    onload = settings.get('settingsonload', 'saved')
    if onload == 'saved':
        settings.update(load_json(os.path.join(user_dir, 'saved.json')))
    elif onload == 'lastused':
        settings.update(load_json(os.path.join(user_dir, 'last.json')))

    rom_path = settings.get('rom')
    if not rom_path:
        raise RuntimeError('No "rom" path found in resources/user settings.')
    if not os.path.isabs(rom_path):
        rom_path = os.path.join(repo_root, rom_path)
    if not os.path.isfile(rom_path):
        raise RuntimeError(f'ROM not found at settings path: {rom_path}')
    return rom_path


def read_vanilla_ow_map(rom_path):
    """Return map bytes in ROM tile order (not linear image order)."""
    buffer = read_rom_bytes(rom_path)
    end = OW_MAP_PC_ADDR + OW_MAP_SIZE
    if len(buffer) < end:
        raise RuntimeError(f'ROM is too small to contain map data at PC {hex(OW_MAP_PC_ADDR)}')
    return bytes(buffer[OW_MAP_PC_ADDR:end])


def linear_to_rom_tiles(pixels, width=OW_MAP_WIDTH, height=OW_MAP_HEIGHT, tile=OW_TILE_SIZE):
    if len(pixels) != width * height:
        raise ValueError('Pixel buffer size does not match width*height')
    if width % tile or height % tile:
        raise ValueError('Width/height must be divisible by tile size')
    out = bytearray(width * height)
    i = 0
    for ty in range(height // tile):
        for tx in range(width // tile):
            for y in range(tile):
                for x in range(tile):
                    out[i] = pixels[(ty * tile + y) * width + tx * tile + x]
                    i += 1
    return bytes(out)


def rom_tiles_to_linear(pixels, width=OW_MAP_WIDTH, height=OW_MAP_HEIGHT, tile=OW_TILE_SIZE):
    if len(pixels) != width * height:
        raise ValueError('Pixel buffer size does not match width*height')
    if width % tile or height % tile:
        raise ValueError('Width/height must be divisible by tile size')
    out = bytearray(width * height)
    i = 0
    for ty in range(height // tile):
        for tx in range(width // tile):
            for y in range(tile):
                for x in range(tile):
                    out[(ty * tile + y) * width + tx * tile + x] = pixels[i]
                    i += 1
    return bytes(out)


def read_8bpp_bmp(path):
    with open(path, 'rb') as fh:
        data = fh.read()
    if data[:2] != b'BM':
        raise ValueError(f'Not a BMP file: {path}')

    bf_off_bits = struct.unpack_from('<I', data, 10)[0]
    bi_size = struct.unpack_from('<I', data, 14)[0]
    width = struct.unpack_from('<i', data, 18)[0]
    height = struct.unpack_from('<i', data, 22)[0]
    planes = struct.unpack_from('<H', data, 26)[0]
    bit_count = struct.unpack_from('<H', data, 28)[0]
    compression = struct.unpack_from('<I', data, 30)[0]
    clr_used = struct.unpack_from('<I', data, 46)[0] if bi_size >= 40 else 0

    if planes != 1 or bit_count != 8 or compression != 0:
        raise ValueError(f'Expected uncompressed 8bpp BMP, got planes={planes} bpp={bit_count} compression={compression}')
    if width != OW_MAP_WIDTH or abs(height) != OW_MAP_HEIGHT:
        raise ValueError(f'Expected {OW_MAP_WIDTH}x{OW_MAP_HEIGHT}, got {width}x{abs(height)}')

    palette_entries = clr_used if clr_used else 256
    palette_offset = 14 + bi_size
    palette = bytearray(data[palette_offset:palette_offset + palette_entries * 4])
    if len(palette) < 256 * 4:
        palette.extend(b'\x00' * (256 * 4 - len(palette)))

    row_size = (width + 3) // 4 * 4
    raw = data[bf_off_bits:bf_off_bits + row_size * abs(height)]
    rows = [raw[y * row_size:y * row_size + width] for y in range(abs(height))]
    # BMP stores bottom-up when height > 0; keep a top-down linear buffer.
    if height > 0:
        rows = list(reversed(rows))
    pixels = bytearray(b''.join(rows))
    if len(pixels) != OW_MAP_SIZE:
        raise ValueError(f'Unexpected pixel buffer size {len(pixels)}')
    return width, abs(height), bytes(palette[:256 * 4]), bytes(pixels)


def write_8bpp_bmp(path, width, height, palette, pixels, bottom_up=True):
    if len(pixels) != width * height:
        raise ValueError('Pixel buffer size does not match width*height')
    palette = bytearray(palette)
    if len(palette) < 256 * 4:
        palette.extend(b'\x00' * (256 * 4 - len(palette)))
    palette = palette[:256 * 4]

    row_size = (width + 3) // 4 * 4
    padding = b'\x00' * (row_size - width)
    rows = [pixels[y * width:(y + 1) * width] + padding for y in range(height)]
    if bottom_up:
        rows = list(reversed(rows))
    pixel_data = b''.join(rows)

    pixel_offset = 14 + 40 + 256 * 4
    file_size = pixel_offset + len(pixel_data)
    header = struct.pack('<2sIHHI', b'BM', file_size, 0, 0, pixel_offset)
    dib = struct.pack('<IiiHHIIiiII',
                      40, width, height if bottom_up else -height, 1, 8, 0,
                      len(pixel_data), 0x0EC3, 0x0EC3, 256, 0)
    with open(path, 'wb') as fh:
        fh.write(header)
        fh.write(dib)
        fh.write(palette)
        fh.write(pixel_data)


def palette_bgr(palette, index):
    offset = index * 4
    return palette[offset:offset + 3]


def build_color_to_index(palette, pixels=None):
    """
    Map BGR color -> palette index.
    If pixels are given, prefer the index used most often for that color.
    Otherwise use the lowest index that has the color.
    """
    if pixels is None:
        color_to_idx = {}
        for idx in range(256):
            color = bytes(palette_bgr(palette, idx))
            color_to_idx.setdefault(color, idx)
        return color_to_idx

    usage = defaultdict(Counter)
    for idx in pixels:
        usage[bytes(palette_bgr(palette, idx))][idx] += 1
    return {color: counts.most_common(1)[0][0] for color, counts in usage.items()}


def make_sparse_diff_pixels(modded_pixels, modded_palette, vanilla_linear_pixels, vanilla_palette, skip=SPARSE_SKIP):
    """
    Build a linear sparse image in 8x8 tile units:
      - unchanged tiles are filled with 0xFF (leave ROM alone)
      - if any pixel in a tile differs by color, the entire 8x8 tile is emitted
        as vanilla-palette indices for the modded colors
    Comparing by color avoids false diffs from duplicate palette indices /
    BMP reserved-byte differences.
    """
    if len(modded_pixels) != len(vanilla_linear_pixels):
        raise ValueError('Modded and vanilla buffers must be the same length')

    color_to_idx = build_color_to_index(vanilla_palette, vanilla_linear_pixels)
    # Ensure every vanilla palette color is representable, even if unused in pixels.
    for idx in range(256):
        color_to_idx.setdefault(bytes(palette_bgr(vanilla_palette, idx)), idx)

    width = OW_MAP_WIDTH
    height = OW_MAP_HEIGHT
    tile = OW_TILE_SIZE
    out = bytearray([skip]) * len(modded_pixels)
    changed_tiles = []
    changed_pixels = 0

    for ty in range(height // tile):
        for tx in range(width // tile):
            tile_differs = False
            for y in range(tile):
                row = (ty * tile + y) * width + tx * tile
                for x in range(tile):
                    i = row + x
                    mod_color = bytes(palette_bgr(modded_palette, modded_pixels[i]))
                    van_color = bytes(palette_bgr(vanilla_palette, vanilla_linear_pixels[i]))
                    if mod_color != van_color:
                        tile_differs = True
                        break
                if tile_differs:
                    break

            if not tile_differs:
                continue

            changed_tiles.append((tx, ty))
            for y in range(tile):
                row = (ty * tile + y) * width + tx * tile
                for x in range(tile):
                    i = row + x
                    mod_color = bytes(palette_bgr(modded_palette, modded_pixels[i]))
                    if mod_color not in color_to_idx:
                        raise ValueError(
                            f'Modded pixel uses color {mod_color.hex()} not present in vanilla palette')
                    encoded = color_to_idx[mod_color]
                    if encoded == skip:
                        raise ValueError(f'Refused to encode tile pixel as skip sentinel {skip:#x}')
                    out[i] = encoded
                    changed_pixels += 1

    return bytes(out), changed_pixels, changed_tiles


def mark_skip_palette_entry(palette, skip=SPARSE_SKIP, color_bgrx=(0xFF, 0x00, 0xFF, 0x00)):
    """Make the skip index a visible magenta so sparse BMPs are easy to inspect."""
    palette = bytearray(palette)
    offset = skip * 4
    palette[offset:offset + 4] = bytes(color_bgrx)
    return bytes(palette)


def apply_sparse_map_to_rom(rom, sparse_linear_pixels, pc_addr=OW_MAP_PC_ADDR, skip=SPARSE_SKIP):
    """Convert linear sparse BMP pixels to ROM 8x8 tile order and write non-skip bytes."""
    if len(sparse_linear_pixels) != OW_MAP_SIZE:
        raise ValueError(f'Sparse map must be {OW_MAP_SIZE:#x} bytes')
    sparse_rom = linear_to_rom_tiles(sparse_linear_pixels)
    written = 0
    for offset, value in enumerate(sparse_rom):
        if value != skip:
            rom.write_byte(pc_addr + offset, value)
            written += 1
    return written


def load_sparse_bmp_pixels(path):
    _, _, _, pixels = read_8bpp_bmp(path)
    return pixels


def vanilla_rom_to_linear_pixels(rom_path):
    return rom_tiles_to_linear(read_vanilla_ow_map(rom_path))


def _data_path(relative_path):
    """Resolve a repo-relative data path without importing Utils."""
    if os.path.isabs(relative_path) or os.path.isfile(relative_path):
        return relative_path
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    candidate = os.path.join(repo_root, relative_path)
    if os.path.isfile(candidate):
        return candidate
    return os.path.join('.', relative_path)


def apply_ow_map_diff(rom, path=None):
    if path is None:
        path = _data_path(DEFAULT_MAP_BMP)
    if not os.path.isfile(path):
        return 0
    pixels = load_sparse_bmp_pixels(path)
    # The ROM asset must be the script output (whole unchanged tiles = 0xFF).
    # A full source BMP has no skip bytes and must not be written raw.
    if SPARSE_SKIP not in pixels:
        raise RuntimeError(
            f'{path} does not look like a sparse OW map asset (no 0xFF tiles). '
            f'Drag the full source BMP onto data/overworld/make_ow_map_diff.py '
            f'to generate {DEFAULT_MAP_BMP}.')
    return apply_sparse_map_to_rom(rom, pixels)


def linear_tilemap_to_rom_blocks(
        data,
        width=OW_TILEMAP_WIDTH,
        height=OW_TILEMAP_HEIGHT,
        block=OW_TILEMAP_BLOCK):
    """Convert a tool-linear 64x64 tilemap into ROM 32x32 quadrant order."""
    if len(data) != width * height:
        raise ValueError('Tilemap size does not match width*height')
    if width % block or height % block:
        raise ValueError('Tilemap width/height must be divisible by block size')
    out = bytearray(width * height)
    i = 0
    for by in range(height // block):
        for bx in range(width // block):
            for y in range(block):
                for x in range(block):
                    out[i] = data[(by * block + y) * width + bx * block + x]
                    i += 1
    return bytes(out)


def extract_dw_tilemap_overlay(linear_64, width=OW_TILEMAP_WIDTH, block=OW_TILEMAP_BLOCK):
    """
    Dark World ROM tilemap is the center 32x32 of the tool's linear 64x64 map.
    Game uploads that block at Mode 7 position (16,16) over the LW map.
    """
    if len(linear_64) != width * width:
        raise ValueError('Expected a linear 64x64 tilemap')
    origin = (width - block) // 2  # 16
    out = bytearray(block * block)
    i = 0
    for y in range(origin, origin + block):
        row = y * width + origin
        out[i:i + block] = linear_64[row:row + block]
        i += block
    return bytes(out)


def _load_tool_tilemap_bin(path):
    if not os.path.isfile(path):
        raise FileNotFoundError(f'OW tilemap not found: {path}')
    with open(path, 'rb') as fh:
        data = fh.read()
    if len(data) != OW_TILEMAP_ASSET_SIZE:
        raise ValueError(
            f'OW tilemap {path} must be {OW_TILEMAP_ASSET_SIZE:#x} bytes '
            f'(linear 64x64 export), got {len(data):#x}')
    return data


def apply_ow_lw_tilemap(rom, path=None):
    if path is None:
        path = _data_path(DEFAULT_LW_TILEMAP_BIN)
    data = _load_tool_tilemap_bin(path)
    # Linear 64x64 -> four 32x32 ROM quadrants.
    rom.write_bytes(snes_to_pc(OW_LW_TILEMAP_SNES_ADDR), linear_tilemap_to_rom_blocks(data))
    return OW_LW_TILEMAP_SIZE


def apply_ow_dw_tilemap(rom, path=None):
    if path is None:
        path = _data_path(DEFAULT_DW_TILEMAP_BIN)
    data = _load_tool_tilemap_bin(path)
    # Only the center 32x32 is stored; do not write into palette at $0ADB39.
    overlay = extract_dw_tilemap_overlay(data)
    if len(overlay) != OW_DW_TILEMAP_SIZE:
        raise ValueError(f'DW overlay must be {OW_DW_TILEMAP_SIZE:#x} bytes')
    rom.write_bytes(snes_to_pc(OW_DW_TILEMAP_SNES_ADDR), overlay)
    return OW_DW_TILEMAP_SIZE


def apply_ow_tilemaps(rom, lw_path=None, dw_path=None):
    written = 0
    written += apply_ow_lw_tilemap(rom, lw_path)
    written += apply_ow_dw_tilemap(rom, dw_path)
    return written


def apply_ow_map_assets(rom):
    """Apply OW map graphics diff (if present) and LW/DW tilemap bins."""
    gfx_written = apply_ow_map_diff(rom)
    tilemap_written = apply_ow_tilemaps(rom)
    return gfx_written, tilemap_written
