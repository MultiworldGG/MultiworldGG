from enum import Enum, auto
from types import TracebackType

from .common_types import MinimapId
from .compress import comp_lz77, decomp_lz77
from .constants.game_data import minimap_ptrs
from .convert_array import u8_to_u16, u16_to_u8
from .rom import Rom


class TilemapType(Enum):
    TILESET = auto()
    """Uncompressed, prefixed with 02 00"""
    BACKGROUND = auto()
    """Compressed, prefixed with background size"""
    MISC = auto()
    """Compressed, used for minimaps and cutscene graphics"""


class Tilemap:
    def __init__(self, rom: Rom, ptr: int, type: TilemapType):
        self.rom = rom
        self.pointer = ptr
        self.type = type
        # Get data
        addr = rom.read_ptr(ptr)
        self.data: list[int] = []
        if type == TilemapType.TILESET:
            addr += 2
            while True:
                val = rom.read_16(addr)
                if val == 0:
                    if len(self.data) % 4 != 0:
                        raise ValueError("Tilemap length should be a multiple of 4")
                    break
                if len(self.data) >= 1024 * 4:
                    raise ValueError("Tilemap is too long")
                self.data.append(val)
                addr += 2
            self.data_size = len(self.data) * 2 + 4
        elif type == TilemapType.BACKGROUND:
            raise NotImplementedError()
        elif type == TilemapType.MISC:
            data, self.data_size = decomp_lz77(rom.data, addr)
            self.data = u8_to_u16(data)

    def __enter__(self) -> "Tilemap":
        # We don't need to do anything
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.write(copy=False)

    @classmethod
    def from_minimap(cls, rom: Rom, id: MinimapId) -> "Tilemap":
        ptr = minimap_ptrs(rom) + (id * 4)
        return Tilemap(rom, ptr, TilemapType.MISC)

    def get_tile_index(self, x: int, y: int) -> int:
        if self.type == TilemapType.TILESET:
            idx = (y // 2 * 64) + (y % 2 * 2) + (x // 2 * 4) + (x % 2)
        else:
            idx = y * 32 + x
        if idx >= len(self.data):
            raise IndexError(f"Tile coordinate ({x}, {y}) is not within tilemap")
        return idx

    def get_tile_value(self, x: int, y: int) -> tuple[int, int, bool, bool]:
        idx = self.get_tile_index(x, y)
        value = self.data[idx]
        tile = value & 0x3FF
        palette = value >> 12
        h_flip = value & 0x400 != 0
        v_flip = value & 0x800 != 0
        return tile, palette, h_flip, v_flip

    def set_tile_value(
        self, x: int, y: int, tile: int, palette: int, h_flip: bool = False, v_flip: bool = False
    ) -> None:
        idx = self.get_tile_index(x, y)
        value = tile | (palette << 12)
        if h_flip:
            value |= 0x400
        if v_flip:
            value |= 0x800
        self.data[idx] = value

    def byte_data(self) -> bytes:
        if self.type == TilemapType.TILESET:
            return bytes([2, 0]) + u16_to_u8(self.data) + bytes([0, 0])
        elif self.type == TilemapType.BACKGROUND:
            raise NotImplementedError()
        elif self.type == TilemapType.MISC:
            data = comp_lz77(u16_to_u8(self.data))
            return bytes(data)

    def write(self, copy: bool) -> None:
        data = self.byte_data()
        if copy:
            self.rom.write_data_with_pointers(data, [self.pointer])
        else:
            addr = self.rom.read_ptr(self.pointer)
            self.rom.write_repointable_data(addr, self.data_size, data, [self.pointer])


def apply_minimap_edits(rom: Rom, edit_dict: dict) -> None:
    # Go through every minimap
    for map_id, changes in edit_dict.items():
        with Tilemap.from_minimap(rom, int(map_id)) as minimap:
            for change in changes:
                minimap.set_tile_value(
                    change["x"],
                    change["y"],
                    change["tile"],
                    change["palette"],
                    change.get("h_flip", False),
                    change.get("v_flip", False),
                )
