from .constants.game_data import anim_tileset_entries, tileset_entries
from .rom import Rom

TILESET_SIZE = 0x14
ANIM_TILESET_SIZE = 0x30


class Tileset:
    def __init__(self, rom: Rom, id: int):
        self.rom = rom
        self.addr = tileset_entries(rom) + id * TILESET_SIZE

    def block_bg_gfx_ptr(self) -> int:
        return self.addr

    def block_bg_gfx_addr(self) -> int:
        return self.rom.read_ptr(self.block_bg_gfx_ptr())

    def palette_ptr(self) -> int:
        return self.addr + 4

    def palette_addr(self) -> int:
        return self.rom.read_ptr(self.palette_ptr())

    def tiled_bg_gfx_ptr(self) -> int:
        return self.addr + 8

    def tiled_bg_gfx_addr(self) -> int:
        return self.rom.read_ptr(self.tiled_bg_gfx_ptr())

    def tilemap_ptr(self) -> int:
        return self.addr + 0xC

    def tilemap_addr(self) -> int:
        return self.rom.read_ptr(self.tilemap_ptr())

    def anim_tileset(self) -> int:
        return self.rom.read_8(self.addr + 0x10)

    def anim_tileset_addr(self) -> int:
        return anim_tileset_entries(self.rom) + self.anim_tileset() * ANIM_TILESET_SIZE

    def anim_palette(self) -> int:
        return self.rom.read_8(self.addr + 0x11)
