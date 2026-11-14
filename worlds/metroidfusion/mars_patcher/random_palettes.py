import random
from enum import Enum, auto
from typing import TypeAlias

from typing_extensions import Self

from .constants import game_data as gd
from .mf.auto_generated_types import (
    MarsschemamfPalettes,
    MarsschemamfPalettesColorSpace,
    MarsschemamfPalettesRandomize,
)
from .mf.constants.game_data import sax_palettes, sprite_vram_sizes
from .mf.constants.palettes import (
    ENEMY_GROUPS_MF,
    EXCLUDED_ENEMIES_MF,
    MF_TILESET_ALT_PAL_ROWS,
    NETTORI_EXTRA_PALS,
    TILESET_ANIM_PALS,
)
from .mf.constants.sprites import SpriteIdMF
from .palette import PAL_ROW_SIZE, ColorChange, Palette, SineWave
from .rom import Rom
from .tileset import Tileset
from .zm.auto_generated_types import (
    MarsschemazmPalettes,
    MarsschemazmPalettesColorSpace,
    MarsschemazmPalettesRandomize,
)
from .zm.constants.game_data import (
    gunship_flashing_palette_addr,
    statues_cutscene_palette_addr,
)
from .zm.constants.palettes import ENEMY_GROUPS_ZM, EXCLUDED_ENEMIES_ZM
from .zm.constants.sprites import SpriteIdZM

SchemaPalettes = MarsschemamfPalettes | MarsschemazmPalettes
SchemaPalettesColorSpace = MarsschemamfPalettesColorSpace | MarsschemazmPalettesColorSpace
SchemaPalettesRandomize = MarsschemamfPalettesRandomize | MarsschemazmPalettesRandomize

HueRange: TypeAlias = tuple[int, int]


class PaletteType(Enum):
    TILESETS = auto()
    ENEMIES = auto()
    SAMUS = auto()
    BEAMS = auto()


class PaletteSettings:
    def __init__(
        self,
        seed: int,
        pal_types: dict[PaletteType, HueRange],
        color_space: SchemaPalettesColorSpace,
        symmetric: bool,
        extra_variation: bool,
    ):
        self.seed = seed
        self.pal_types = pal_types
        self.color_space: SchemaPalettesColorSpace = color_space
        self.symmetric = symmetric
        self.extra_variation = extra_variation

    @classmethod
    def from_json(cls, data: SchemaPalettes) -> Self:
        seed = data.get("seed", random.randint(0, 2**31 - 1))
        random.seed(seed)
        pal_types = {}
        for type_name, hue_data in data["randomize"].items():
            pal_type = PaletteType[type_name]
            hue_range = cls.get_hue_range(hue_data)
            pal_types[pal_type] = hue_range
        color_space = data.get("color_space", "OKLAB")
        symmetric = data.get("symmetric", True)
        # Extra variation is always enabled. This could be passed via JSON instead.
        return cls(seed, pal_types, color_space, symmetric, True)

    @classmethod
    def get_hue_range(cls, data: SchemaPalettesRandomize) -> HueRange:
        hue_min = data.get("hue_min")
        hue_max = data.get("hue_max")
        if hue_min is None or hue_max is None:
            if hue_max is not None:
                hue_min = random.randint(0, hue_max)
            elif hue_min is not None:
                hue_max = random.randint(hue_min, 360)
            else:
                hue_min = random.randint(0, 360)
                hue_max = random.randint(hue_min, 360)
        if hue_min > hue_max:
            raise ValueError("HueMin cannot be greater than HueMax")
        return hue_min, hue_max


class PaletteRandomizer:
    """Class for randomly shifting the hues of color palettes."""

    def __init__(self, rom: Rom, settings: PaletteSettings):
        self.rom = rom
        self.settings = settings
        if settings.color_space == "HSV":
            self.change_func = self.change_palette_hsv
        elif settings.color_space == "OKLAB":
            self.change_func = self.change_palette_oklab
        else:
            raise ValueError(f"Invalid color space '{settings.color_space}' for color space!")

    @staticmethod
    def change_palette_hsv(
        pal: Palette, change: ColorChange, excluded_rows: set[int] = set()
    ) -> None:
        pal.change_colors_hsv(change, excluded_rows)

    @staticmethod
    def change_palette_oklab(
        pal: Palette, change: ColorChange, excluded_rows: set[int] = set()
    ) -> None:
        pal.change_colors_oklab(change, excluded_rows)

    def generate_palette_change(self, hue_range: HueRange) -> ColorChange:
        """Generates a random color change. hue_range determines how far each color's hue will be
        initially rotated. Individual colors can be additionally rotated using the values of a
        random sine wave."""
        hue_min, hue_max = hue_range
        hue_shift = random.randint(hue_min, hue_max)
        if self.settings.symmetric and random.choice([True, False]):
            hue_shift = 360 - hue_shift
        if self.settings.extra_variation:
            hue_var_range = min(1.0, (hue_max - hue_min) / 180)
            hue_var = SineWave.generate(hue_var_range)
        else:
            hue_var = None
        return ColorChange(hue_shift, hue_var)

    def randomize(self) -> None:
        random.seed(self.settings.seed)
        self.randomized_pals: set[int] = set()
        pal_types = self.settings.pal_types
        if PaletteType.TILESETS in pal_types:
            self.randomize_tilesets(pal_types[PaletteType.TILESETS])
        if PaletteType.ENEMIES in pal_types:
            self.randomize_enemies(pal_types[PaletteType.ENEMIES])
        if PaletteType.SAMUS in pal_types:
            self.randomize_samus(pal_types[PaletteType.SAMUS])
        if PaletteType.BEAMS in pal_types:
            self.randomize_beams(pal_types[PaletteType.BEAMS])
        # Fix any sprite/tileset palettes that should be the same
        if self.rom.is_zm():
            self.fix_zm_palettes()

    def change_palettes(self, pals: list[tuple[int, int]], change: ColorChange) -> None:
        for addr, rows in pals:
            if addr in self.randomized_pals:
                continue
            pal = Palette(rows, self.rom, addr)
            self.change_func(pal, change)
            pal.write(self.rom, addr)
            self.randomized_pals.add(addr)

    def randomize_samus(self, hue_range: HueRange) -> None:
        change = self.generate_palette_change(hue_range)
        self.change_palettes(gd.samus_palettes(self.rom), change)
        self.change_palettes(gd.helmet_cursor_palettes(self.rom), change)
        if self.rom.is_mf():
            self.change_palettes(sax_palettes(self.rom), change)

    def randomize_beams(self, hue_range: HueRange) -> None:
        change = self.generate_palette_change(hue_range)
        self.change_palettes(gd.beam_palettes(self.rom), change)

    def randomize_tilesets(self, hue_range: HueRange) -> None:
        rom = self.rom
        ts_addr = gd.tileset_entries(rom)
        ts_count = gd.tileset_count(rom)
        anim_pal_count = gd.anim_palette_count(rom)
        anim_pal_to_randomize = set(range(anim_pal_count))

        for _ in range(ts_count):
            # Get tileset palette address
            pal_ptr = ts_addr + 4
            pal_addr = rom.read_ptr(pal_ptr)
            ts_addr += 0x14
            if pal_addr in self.randomized_pals:
                continue
            # Get excluded palette rows
            excluded_rows = set()
            if rom.is_mf():
                row = MF_TILESET_ALT_PAL_ROWS.get(pal_addr)
                if row is not None:
                    excluded_rows = {row}
            # Load palette and shift hue
            pal = Palette(13, rom, pal_addr)
            change = self.generate_palette_change(hue_range)
            self.change_func(pal, change, excluded_rows)
            pal.write(rom, pal_addr)
            self.randomized_pals.add(pal_addr)
            # Check animated palette
            anim_pal_id = TILESET_ANIM_PALS.get(pal_addr)
            if anim_pal_id is not None:
                self.randomize_anim_palette(anim_pal_id, change)
                anim_pal_to_randomize.remove(anim_pal_id)

        # Go through remaining animated palettes
        for anim_pal_id in anim_pal_to_randomize:
            change = self.generate_palette_change(hue_range)
            self.randomize_anim_palette(anim_pal_id, change)

    def randomize_anim_palette(self, anim_pal_id: int, change: ColorChange) -> None:
        rom = self.rom
        addr = gd.anim_palette_entries(rom) + anim_pal_id * 8
        pal_addr = rom.read_ptr(addr + 4)
        if pal_addr in self.randomized_pals:
            return
        rows = rom.read_8(addr + 2)
        pal = Palette(rows, rom, pal_addr)
        self.change_func(pal, change)
        pal.write(rom, pal_addr)
        self.randomized_pals.add(pal_addr)

    def randomize_enemies(self, hue_range: HueRange) -> None:
        rom = self.rom
        _excluded: set[SpriteIdMF] | set[SpriteIdZM]
        if rom.is_mf():
            _excluded = EXCLUDED_ENEMIES_MF
        elif rom.is_zm():
            _excluded = EXCLUDED_ENEMIES_ZM
        else:
            raise ValueError(rom.game)
        excluded = {en_id.value for en_id in _excluded}
        sp_count = gd.sprite_count(rom)
        # The first 0x10 sprites have no graphics
        to_randomize = set(range(0x10, sp_count))
        to_randomize -= excluded

        # Go through sprites in groups
        groups: dict[str, list[SpriteIdMF]] | dict[str, list[SpriteIdZM]]
        if rom.is_mf():
            groups = ENEMY_GROUPS_MF
        elif rom.is_zm():
            groups = ENEMY_GROUPS_ZM
        else:
            raise ValueError(rom.game)
        for _, sprite_ids in groups.items():
            change = self.generate_palette_change(hue_range)
            for sprite_id in sprite_ids:
                assert sprite_id in to_randomize, f"{sprite_id:X} should be excluded"
                self.randomize_enemy(sprite_id, change)
                to_randomize.remove(sprite_id)

        # Go through remaining sprites
        for sp_id in to_randomize:
            change = self.generate_palette_change(hue_range)
            self.randomize_enemy(sp_id, change)

    def randomize_enemy(self, sprite_id: int, change: ColorChange) -> None:
        # Get palette address and row count
        rom = self.rom
        sprite_gfx_id = sprite_id - 0x10
        pal_ptr = gd.sprite_palette_ptrs(rom)
        pal_addr = rom.read_ptr(pal_ptr + sprite_gfx_id * 4)

        # Skip palettes that have already been randomized
        if pal_addr in self.randomized_pals:
            return
        if rom.is_mf():
            if sprite_id == SpriteIdMF.ICE_BEAM_ABILITY or sprite_id == SpriteIdMF.ZOZORO:
                # Ice beam ability and zozoros only have 1 row, not 2
                rows = 1
            else:
                vram_size_addr = sprite_vram_sizes(rom)
                vram_size = rom.read_32(vram_size_addr + sprite_gfx_id * 4)
                rows = vram_size // 0x800
        elif rom.is_zm():
            gfx_ptr = gd.sprite_graphics_ptrs(rom)
            gfx_addr = rom.read_ptr(gfx_ptr + sprite_gfx_id * 4)
            rows = (rom.read_32(gfx_addr) >> 8) // 0x800
        else:
            raise ValueError("Unknown game!")

        # Load palette, change colors, and write to ROM
        pal = Palette(rows, rom, pal_addr)
        self.change_func(pal, change)
        pal.write(rom, pal_addr)
        self.randomized_pals.add(pal_addr)
        # Handle sprites with extra palettes
        if rom.is_mf():
            if sprite_id in {
                SpriteIdMF.SAMUS_EATER_BUD,
                SpriteIdMF.SAMUS_EATER,
                SpriteIdMF.NETTORI,
            }:
                self.fix_nettori(change)
        elif rom.is_zm():
            if sprite_id == SpriteIdZM.GUNSHIP:
                self.fix_zm_gunship(change)

    def get_sprite_addr(self, sprite_id: int) -> int:
        addr = gd.sprite_palette_ptrs(self.rom) + (sprite_id - 0x10) * 4
        return self.rom.read_ptr(addr)

    def get_tileset_addr(self, tileset_id: int) -> int:
        tileset = Tileset(self.rom, tileset_id)
        return tileset.palette_addr()

    def fix_nettori(self, change: ColorChange) -> None:
        """Nettori has extra palettes stored separately, so they require the same color change."""
        for addr, rows in NETTORI_EXTRA_PALS:
            pal = Palette(rows, self.rom, addr)
            self.change_func(pal, change)
            pal.write(self.rom, addr)

    def fix_zm_gunship(self, change: ColorChange) -> None:
        """The gunship has an extra palette stored separately, so it requires
        the same color change."""
        addr = gunship_flashing_palette_addr(self.rom)
        pal = Palette(8, self.rom, addr)
        self.change_func(pal, change)
        pal.write(self.rom, addr)

    def fix_zm_palettes(self) -> None:
        if (
            PaletteType.ENEMIES in self.settings.pal_types
            or PaletteType.TILESETS in self.settings.pal_types
        ):
            # Fix kraid's body (copy row from sprite to tileset)
            sp_addr = self.get_sprite_addr(SpriteIdZM.KRAID)
            ts_addr = self.get_tileset_addr(9)
            self.rom.copy_bytes(sp_addr, ts_addr + (8 * PAL_ROW_SIZE), PAL_ROW_SIZE)

        if PaletteType.TILESETS in self.settings.pal_types:
            # Fix kraid elevator statue
            sp_addr = self.get_sprite_addr(SpriteIdZM.KRAID_ELEVATOR_STATUE)
            ts_addr = self.get_tileset_addr(0x35)
            self.rom.copy_bytes(ts_addr + PAL_ROW_SIZE, sp_addr, PAL_ROW_SIZE)

            # Fix ridley elevator statue
            ts_addr = self.get_tileset_addr(7)
            self.rom.copy_bytes(ts_addr + PAL_ROW_SIZE, sp_addr + PAL_ROW_SIZE, PAL_ROW_SIZE)

            # Fix tourian statues
            sp_addr = self.get_sprite_addr(SpriteIdZM.KRAID_STATUE)
            ts_addr = self.get_tileset_addr(0x41)
            self.rom.copy_bytes(ts_addr + (3 * PAL_ROW_SIZE), sp_addr, PAL_ROW_SIZE)
            # Fix cutscene
            sp_addr = statues_cutscene_palette_addr(self.rom)
            self.rom.copy_bytes(ts_addr, sp_addr, 6 * PAL_ROW_SIZE)
