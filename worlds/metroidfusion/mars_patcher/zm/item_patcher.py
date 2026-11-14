from collections import defaultdict

from ..compress import comp_lz77, decomp_lz77
from ..constants.game_data import (
    anim_graphics_count,
    anim_tileset_count,
    anim_tileset_entries,
    sprite_graphics_ptrs,
    sprite_palette_ptrs,
    tileset_count,
    tileset_entries,
)
from ..convert_array import ptr_to_u8
from ..item_messages import ItemMessages, ItemMessagesKind
from ..palette import PAL_ROW_SIZE
from ..rom import Rom
from ..room_entry import RoomEntry
from ..text import Language, MessageType, encode_text
from ..tilemap import Tilemap, TilemapType
from ..tileset import ANIM_TILESET_SIZE, TILESET_SIZE, Tileset
from .auto_generated_types import MarsschemazmTankIncrements
from .constants.game_data import (
    chozo_statue_targets_addr,
    major_locations_addr,
    minor_locations_addr,
    tank_increase_amounts_addr,
)
from .constants.items import (
    ITEM_TO_SPRITE,
    ItemSprite,
    MajorSource,
    get_sprite_graphics,
    get_sprite_palette,
)
from .constants.reserved_space import ReservedPointersZM
from .constants.sprites import SpriteIdZM
from .locations import HintLocation, LocationSettings, MajorLocation, MinorLocation

MAX_ITEMS_PER_TILEMAP = 4
"""The maximum number of item graphics that can be added to a tilemap."""

NEW_ITEM_BG1_START = 0x4C
"""The first BG1 value to use when adding item graphics to a tileset."""

TANK_SPRITES = {
    ItemSprite.ENERGY_TANK,
    ItemSprite.MISSILE_TANK,
    ItemSprite.SUPER_MISSILE_TANK,
    ItemSprite.POWER_BOMB_TANK,
}

MAJOR_SOURCE_SPRITES = {
    MajorSource.LONG_BEAM: SpriteIdZM.LONG_BEAM_CHOZO_STATUE,
    MajorSource.CHARGE_BEAM: SpriteIdZM.CHARGE_BEAM,
    MajorSource.ICE_BEAM: SpriteIdZM.ICE_BEAM_CHOZO_STATUE,
    MajorSource.WAVE_BEAM: SpriteIdZM.WAVE_BEAM_CHOZO_STATUE,
    MajorSource.PLASMA_BEAM: SpriteIdZM.PLASMA_BEAM_CHOZO_STATUE,
    MajorSource.BOMBS: SpriteIdZM.BOMB_CHOZO_STATUE,
    MajorSource.VARIA_SUIT: SpriteIdZM.VARIA_SUIT_CHOZO_STATUE,
    MajorSource.GRAVITY_SUIT: SpriteIdZM.GRAVITY_SUIT_CHOZO_STATUE,
    MajorSource.MORPH_BALL: SpriteIdZM.MORPH_BALL,
    MajorSource.SPEED_BOOSTER: SpriteIdZM.SPEED_BOOSTER_CHOZO_STATUE,
    MajorSource.HI_JUMP: SpriteIdZM.HI_JUMP_CHOZO_STATUE,
    MajorSource.SCREW_ATTACK: SpriteIdZM.SCREW_ATTACK_CHOZO_STATUE,
    MajorSource.SPACE_JUMP: SpriteIdZM.SPACE_JUMP_CHOZO_STATUE,
    MajorSource.POWER_GRIP: SpriteIdZM.POWER_GRIP,
    MajorSource.ZIPLINES: SpriteIdZM.ZIPLINE_GENERATOR,
}


class ItemPalette:
    def __init__(self, rom: Rom, addr: int, blank_rows: list[int]):
        self.data = rom.read_bytes(addr, PAL_ROW_SIZE * 14)
        self.blank_rows = list(blank_rows)
        self.new_addr: int | None = None

    def add_item_sprite(self, sprite: ItemSprite) -> int:
        row = self.blank_rows.pop(0)
        offset = row * PAL_ROW_SIZE
        self.data[offset : offset + PAL_ROW_SIZE] = get_sprite_palette(sprite)
        return row + 2


class ItemAnimatedTileset:
    def __init__(self, rom: Rom, addr: int, blank_slots: list[int]):
        self.data = rom.read_bytes(addr, ANIM_TILESET_SIZE)
        self.blank_slots = list(blank_slots)
        self.new_id: int | None = None

    def add_item_sprite(self, id: int) -> int:
        slot = self.blank_slots.pop(0)
        self.data[slot * 3] = id
        return slot


class ItemTilemap:
    def __init__(self, rom: Rom, ptr: int):
        self.tilemap = Tilemap(rom, ptr, TilemapType.TILESET)
        self.items_added = 0
        self.new_addr: int | None = None

    def add_item_sprite(self, pal_row: int, anim_gfx_slot: int) -> int:
        bg1 = NEW_ITEM_BG1_START + self.items_added
        self.items_added += 1
        offset = bg1 * 4
        tile_val = (pal_row << 12) | (anim_gfx_slot * 4)
        for t in range(4):
            self.tilemap.data[offset + t] = tile_val + t
        return bg1


class ItemPatcher:
    """Class for writing item assignments to a ROM."""

    def __init__(self, rom: Rom, settings: LocationSettings):
        self.rom = rom
        self.settings = settings

    def write_items(self) -> None:
        rom = self.rom
        hint_targets_addr = chozo_statue_targets_addr(rom)
        seen_messages: dict[str, int] = {}

        # Handle minor locations
        # Locations need to be written in order so that binary search works
        minor_locs = sorted(self.settings.minor_locs, key=lambda x: x.key)
        loc_bg1_values = self.create_graphics_for_minor_locations(minor_locs)
        minor_loc_addr = minor_locations_addr(rom)

        for min_loc in minor_locs:
            # Get BG1 block value
            sprite = min_loc.actual_item_sprite
            match sprite:
                case ItemSprite.ENERGY_TANK:
                    bg1_val = 0x49
                case ItemSprite.MISSILE_TANK:
                    bg1_val = 0x48
                case ItemSprite.SUPER_MISSILE_TANK:
                    bg1_val = 0x4B
                case ItemSprite.POWER_BOMB_TANK:
                    bg1_val = 0x4A
                case _:
                    bg1_val = loc_bg1_values[min_loc]

            # Overwrite BG1 if not hidden
            if not min_loc.hidden:
                room = RoomEntry(rom, min_loc.area, min_loc.room)
                with room.load_bg1() as bg1:
                    bg1.set_block_value(min_loc.block_x, min_loc.block_y, bg1_val)

            # See struct MinorLocation in include/structs/randomizer.h
            rom.write_32(minor_loc_addr, min_loc.key)
            rom.write_16(minor_loc_addr + 4, bg1_val)
            rom.write_8(minor_loc_addr + 6, min_loc.new_item.value)
            rom.write_8(minor_loc_addr + 7, min_loc.item_jingle.value)
            rom.write_8(minor_loc_addr + 8, min_loc.hint_value)
            self.write_item_messages(seen_messages, min_loc.item_messages, minor_loc_addr, False)
            minor_loc_addr += 0x10

            if min_loc.hinted_by != HintLocation.NONE:
                room = RoomEntry(rom, min_loc.area, min_loc.room)
                map_x, map_y = room.map_coords_at_block(min_loc.block_x, min_loc.block_y)
                target_addr = hint_targets_addr + (min_loc.hinted_by.value * 0xC)
                rom.write_8(target_addr + 6, min_loc.area)
                rom.write_8(target_addr + 7, map_x)
                rom.write_8(target_addr + 8, map_y)

        self.fix_caterpillar_room()
        # Replace the graphics of the item the space pirate carries
        pirate_loc = next((x for x in minor_locs if x.area == 6 and x.room == 0x2F), None)
        if pirate_loc is not None:
            self.replace_space_pirate_item(pirate_loc.actual_item_sprite)

        # Handle major locations
        major_locs_addr = major_locations_addr(rom)
        for maj_loc in self.settings.major_locs:
            self.write_major_location_graphics(maj_loc)

            # See struct MajorLocation in include/structs/randomizer.h
            addr = major_locs_addr + (maj_loc.major_src.value * 8)
            rom.write_8(addr, maj_loc.new_item.value)
            rom.write_8(addr + 1, maj_loc.item_jingle.value)
            rom.write_8(addr + 2, maj_loc.hint_value)
            self.write_item_messages(seen_messages, maj_loc.item_messages, addr, True)

            if maj_loc.hinted_by != HintLocation.NONE:
                target_addr = hint_targets_addr + (maj_loc.hinted_by.value * 0xC)
                rom.write_8(target_addr + 6, maj_loc.area)
                rom.write_8(target_addr + 7, maj_loc.map_x)
                rom.write_8(target_addr + 8, maj_loc.map_y)

    def create_graphics_for_minor_locations(
        self, minor_locs: list[MinorLocation]
    ) -> dict[MinorLocation, int]:
        """
        Creates new palettes, animated tilesets, and tilemaps to contain non-tank minor location
        graphics. Data is reused where possible to save space. Each room is given a new tileset
        entry based on the items in the room.
        """
        rom = self.rom

        # Find minor locations with non-tank sprites and group them by room.
        # Also find empty slots in palettes and animated tilesets used in those rooms.
        room_locs: defaultdict[tuple[int, int], list[MinorLocation]] = defaultdict(list)
        empty_pal_rows: dict[int, list[int]] = {}
        empty_anim_set_slots: dict[int, list[int]] = {}
        for minor_loc in minor_locs:
            if minor_loc.actual_item_sprite in TANK_SPRITES:
                continue

            key = (minor_loc.area, minor_loc.room)
            room_locs[key].append(minor_loc)

            entry = RoomEntry(rom, minor_loc.area, minor_loc.room)
            tileset = Tileset(rom, entry.tileset())

            pal_addr = tileset.palette_addr()
            if pal_addr not in empty_pal_rows:
                empty_pal_rows[pal_addr] = self.get_blank_rows_in_palette(pal_addr)

            anim_set_id = tileset.anim_tileset()
            if anim_set_id not in empty_anim_set_slots:
                empty_anim_set_slots[anim_set_id] = self.get_blank_slots_in_animated_tileset(
                    tileset.anim_tileset_addr()
                )

        # Create new palettes, animated tilesets, and tilemaps to store new item graphics
        all_item_palettes: defaultdict[int, list[ItemPalette]] = defaultdict(list)
        all_item_anim_sets: defaultdict[int, list[ItemAnimatedTileset]] = defaultdict(list)
        all_item_tilemaps: defaultdict[int, list[ItemTilemap]] = defaultdict(list)
        anim_gfx_count = anim_graphics_count(self.rom)
        loc_bg1_values: dict[MinorLocation, int] = {}
        room_data: list[tuple[int, int, ItemPalette, ItemAnimatedTileset, ItemTilemap]] = []
        for (area, room), group in room_locs.items():
            entry = RoomEntry(rom, area, room)
            tileset = Tileset(rom, entry.tileset())

            # Add items to existing palette or add a new one
            pal_addr = tileset.palette_addr()
            item_palettes = all_item_palettes[pal_addr]
            for pal in item_palettes:
                if len(pal.blank_rows) >= len(group):
                    item_pal = pal
                    break
            else:
                item_pal = ItemPalette(rom, pal_addr, empty_pal_rows[pal_addr])
                item_palettes.append(item_pal)
            rows = [item_pal.add_item_sprite(loc.actual_item_sprite) for loc in group]

            # Add items to existing animated tileset or add a new one
            anim_set_id = tileset.anim_tileset()
            item_anim_sets = all_item_anim_sets[anim_set_id]
            for anim_set in item_anim_sets:
                if len(anim_set.blank_slots) >= len(group):
                    item_anim_set = anim_set
                    break
            else:
                item_anim_set = ItemAnimatedTileset(
                    rom, tileset.anim_tileset_addr(), empty_anim_set_slots[anim_set_id]
                )
                item_anim_sets.append(item_anim_set)
            slots = [
                item_anim_set.add_item_sprite(
                    anim_gfx_count + (loc.actual_item_sprite.value - ItemSprite.EMPTY.value)
                )
                for loc in group
            ]

            # Add items to existing tilemaps or add a new one
            tm_addr = tileset.tilemap_addr()
            item_tilemaps = all_item_tilemaps[tm_addr]
            for tm in item_tilemaps:
                if tm.items_added + len(group) <= MAX_ITEMS_PER_TILEMAP:
                    item_tm = tm
                    break
            else:
                item_tm = ItemTilemap(rom, tileset.tilemap_ptr())
                item_tilemaps.append(item_tm)
            bg1_vals = [item_tm.add_item_sprite(row, slot) for row, slot in zip(rows, slots)]

            for loc, bg1 in zip(group, bg1_vals):
                loc_bg1_values[loc] = bg1

            room_data.append((area, room, item_pal, item_anim_set, item_tm))

        # Write palette data
        for addr, item_palettes in all_item_palettes.items():
            # Overwrite the first entry
            rom.write_bytes(addr, item_palettes[0].data)
            item_palettes[0].new_addr = addr
            # Create new data for remaining entries
            for item_pal in item_palettes[1:]:
                new_addr = rom.reserve_free_space(len(item_pal.data))
                rom.write_bytes(new_addr, item_pal.data)
                item_pal.new_addr = new_addr

        # Write animated tileset data
        new_anim_set_entries: list[bytes] = []
        anim_set_count = anim_tileset_count(rom)
        for id, item_anim_sets in all_item_anim_sets.items():
            # Overwrite the first entry
            addr = anim_tileset_entries(rom) + id * ANIM_TILESET_SIZE
            rom.write_bytes(addr, item_anim_sets[0].data)
            item_anim_sets[0].new_id = id
            # Create new data for remaining entries
            for item_anim_set in item_anim_sets[1:]:
                new_anim_set_entries.append(bytes(item_anim_set.data))
                item_anim_set.new_id = anim_set_count
                anim_set_count += 1

        # Write tilemap data
        for addr, item_tilemaps in all_item_tilemaps.items():
            # Overwrite the first entry
            rom.write_bytes(addr, item_tilemaps[0].tilemap.byte_data())
            item_tilemaps[0].new_addr = addr
            # Create new data for remaining entries
            for item_tm in item_tilemaps[1:]:
                data = item_tm.tilemap.byte_data()
                new_addr = rom.reserve_free_space(len(data))
                rom.write_bytes(new_addr, data)
                item_tm.new_addr = new_addr

        # Create new tileset entries and update tileset ID in each room
        ts_count = tileset_count(rom)
        new_tileset_entries: list[bytes] = []
        for area, room, item_pal, item_anim_set, item_tm in room_data:
            entry = RoomEntry(rom, area, room)
            # Create new tileset entry
            assert item_pal.new_addr is not None
            assert item_tm.new_addr is not None
            assert item_anim_set.new_id is not None
            ts_entry = self.create_tileset(
                entry.tileset(), item_pal.new_addr, item_tm.new_addr, item_anim_set.new_id
            )
            new_tileset_entries.append(ts_entry)
            # Write tileset ID in room entry
            rom.write_8(entry.addr, ts_count)
            ts_count += 1

        # Write new tileset entries and animated tileset entries
        self.write_new_tilesets(new_tileset_entries, new_anim_set_entries)

        return loc_bg1_values

    def get_blank_rows_in_palette(self, addr: int) -> list[int]:
        blank_rows: list[int] = []
        # Start at row 1 because row 0 is unused
        for row in range(1, 14):
            src = addr + row * PAL_ROW_SIZE
            color = self.rom.read_16(src + 2)
            if all(self.rom.read_16(src + i) == color for i in range(4, PAL_ROW_SIZE, 2)):
                blank_rows.append(row)
        return blank_rows

    def get_blank_slots_in_animated_tileset(self, addr: int) -> list[int]:
        return [i for i in range(16) if self.rom.read_8(addr + i * 3) == 0]

    def create_tileset(
        self, id: int, pal_addr: int, tilemap_addr: int, anim_tileset_id: int
    ) -> bytes:
        """Creates a copy of a tileset entry using the provided palette address, tilemap address,
        and animated tileset ID."""
        tileset = Tileset(self.rom, id)
        data = bytearray()
        data += self.rom.read_bytes(tileset.block_bg_gfx_ptr(), 4)
        data += ptr_to_u8(pal_addr)
        data += self.rom.read_bytes(tileset.tiled_bg_gfx_ptr(), 4)
        data += ptr_to_u8(tilemap_addr)
        data.append(anim_tileset_id)
        data.append(tileset.anim_palette())
        # Padding
        data.append(0)
        data.append(0)
        return bytes(data)

    def write_new_tilesets(
        self, new_tileset_entries: list[bytes], new_anim_tileset_entries: list[bytes]
    ) -> None:
        rom = self.rom

        # Get existing tileset data
        tileset_addr = tileset_entries(rom)
        orig_tileset_size = tileset_count(rom) * TILESET_SIZE
        tileset_data = rom.read_bytes(tileset_addr, orig_tileset_size)

        # Append data for each new tileset entry
        for entry in new_tileset_entries:
            tileset_data += entry

        # Get existing animated tileset data
        anim_tileset_addr = anim_tileset_entries(rom)
        orig_anim_tileset_count = anim_tileset_count(rom)
        orig_anim_tileset_size = orig_anim_tileset_count * ANIM_TILESET_SIZE
        anim_tileset_data = rom.read_bytes(anim_tileset_addr, orig_anim_tileset_size)

        # Append data for each new animated tileset
        for entry in new_anim_tileset_entries:
            anim_tileset_data += entry

        # Write data to ROM and repoint
        rom.write_repointable_data(
            tileset_addr,
            orig_tileset_size,
            tileset_data,
            [ReservedPointersZM.TILESET_ENTRIES_PTR.value],
        )
        rom.write_repointable_data(
            anim_tileset_addr,
            orig_anim_tileset_size,
            anim_tileset_data,
            [ReservedPointersZM.ANIM_TILESET_ENTRIES_PTR.value],
        )

    def fix_caterpillar_room(self) -> None:
        """Set both versions of the Norfair caterpillar room to use the same tileset"""
        room = RoomEntry(self.rom, 2, 0x2A)
        tileset = room.tileset()
        room = RoomEntry(self.rom, 2, 0x2E)
        self.rom.write_8(room.addr, tileset)

    def write_major_location_graphics(self, major_loc: MajorLocation) -> None:
        # Fully powered and ziplines don't have any item graphics
        if major_loc.major_src in {MajorSource.FULLY_POWERED, MajorSource.ZIPLINES}:
            return

        # Get graphics for item sprite
        sprite = major_loc.item_sprite
        if sprite == ItemSprite.DEFAULT:
            sprite = ITEM_TO_SPRITE[major_loc.new_item]
        item_gfx = get_sprite_graphics(sprite)
        item_pal = get_sprite_palette(sprite)

        # Overwrite graphics of source sprite
        gfx_sprite_id = MAJOR_SOURCE_SPRITES[major_loc.major_src] - 0x10
        gfx_ptr = sprite_graphics_ptrs(self.rom) + gfx_sprite_id * 4
        pal_ptr = sprite_palette_ptrs(self.rom) + gfx_sprite_id * 4
        pal_addr = self.rom.read_ptr(pal_ptr)
        match major_loc.major_src:
            case (
                MajorSource.LONG_BEAM
                | MajorSource.ICE_BEAM
                | MajorSource.WAVE_BEAM
                | MajorSource.PLASMA_BEAM
                | MajorSource.BOMBS
                | MajorSource.VARIA_SUIT
                | MajorSource.GRAVITY_SUIT
                | MajorSource.SPEED_BOOSTER
                | MajorSource.HI_JUMP
                | MajorSource.SCREW_ATTACK
                | MajorSource.SPACE_JUMP
            ):
                gfx_ptrs = [gfx_ptr]
                # Hint statues use the same graphics
                if major_loc.major_src in {
                    MajorSource.LONG_BEAM,
                    MajorSource.ICE_BEAM,
                    MajorSource.WAVE_BEAM,
                    MajorSource.BOMBS,
                    MajorSource.SPEED_BOOSTER,
                    MajorSource.HI_JUMP,
                    MajorSource.SCREW_ATTACK,
                    MajorSource.VARIA_SUIT,
                }:
                    # Hint statues appear 1 entry before
                    gfx_ptrs.append(gfx_ptr - 4)
                self.replace_sprite_graphics(gfx_ptrs, item_gfx, 4, 4)
                self.replace_sprite_palette(pal_addr, item_pal, 0)
            case MajorSource.CHARGE_BEAM | MajorSource.MORPH_BALL | MajorSource.POWER_GRIP:
                self.replace_sprite_graphics([gfx_ptr], item_gfx, 0, 0)
                self.replace_sprite_palette(pal_addr, item_pal, 0)
            case _:
                raise ValueError(major_loc.major_src)

    def replace_sprite_graphics(
        self, gfx_ptrs: list[int], item_gfx: bytes, tile_x: int, tile_y: int
    ) -> None:
        assert len(item_gfx) == 12 * 32, "Item graphics should be 12 tiles"
        gfx_addr = self.rom.read_ptr(gfx_ptrs[0])
        gfx_data, orig_size = decomp_lz77(self.rom.data, gfx_addr)

        offset = (tile_y * 32 + tile_x) * 32
        src = 0
        for x in range(0, 6, 2):
            for y in range(2):
                dst = offset + (y * 32 + x) * 32
                gfx_data[dst : dst + 64] = item_gfx[src : src + 64]
                src += 64

        comp_data = comp_lz77(gfx_data)
        self.rom.write_repointable_data(gfx_addr, orig_size, comp_data, gfx_ptrs)

    def replace_sprite_palette(self, pal_addr: int, item_pal: bytes, row: int) -> None:
        assert len(item_pal) == PAL_ROW_SIZE, "Item palette should be one row"
        addr = pal_addr + row * PAL_ROW_SIZE
        self.rom.write_bytes(addr, item_pal)

    def replace_space_pirate_item(self, item_sprite: ItemSprite) -> None:
        """Replaces the graphics of the power bomb sprite that the space pirate
        carries in Chozodia."""
        gfx_sprite_id = SpriteIdZM.FAKE_POWER_BOMB - 0x10
        gfx_ptr = sprite_graphics_ptrs(self.rom) + gfx_sprite_id * 4
        pal_ptr = sprite_palette_ptrs(self.rom) + gfx_sprite_id * 4
        pal_addr = self.rom.read_ptr(pal_ptr)

        item_gfx = get_sprite_graphics(item_sprite)
        item_pal = get_sprite_palette(item_sprite)
        self.replace_sprite_graphics([gfx_ptr], item_gfx, 0, 0)
        self.replace_sprite_palette(pal_addr, item_pal, 0)

    def write_item_messages(
        self,
        seen_messages: dict[str, int],
        messages: ItemMessages | None,
        loc_addr: int,
        is_major: bool,
    ) -> None:
        rom = self.rom
        id_offset = 3 if is_major else 9
        custom_offset = 4 if is_major else 0xC

        if messages is None:
            rom.write_8(loc_addr + id_offset, 0xFF)
            rom.write_32(loc_addr + custom_offset, 0)  # NULL
        elif messages.kind == ItemMessagesKind.MESSAGE_ID:
            rom.write_8(loc_addr + id_offset, messages.message_id)
            rom.write_32(loc_addr + custom_offset, 0)  # NULL
        elif messages.kind == ItemMessagesKind.CUSTOM_MESSAGE:
            # Reserve space for pointers for each language
            table_addr = rom.reserve_free_space(len(Language) * 4)
            for lang in Language:
                # English is required to be set - use English as the fallback value
                msg_text = (
                    messages.item_messages[lang]
                    if lang in messages.item_messages
                    else messages.item_messages[Language.ENGLISH]
                )
                text_ptr = table_addr + (lang.value * 4)
                # Check if text has been seen before
                text_addr = seen_messages.get(msg_text)
                if text_addr is None:
                    encoded_text = encode_text(
                        rom, MessageType.TWO_LINE, msg_text, centered=messages.centered
                    )
                    text_addr = rom.write_data_with_pointers(encoded_text, [text_ptr])
                    seen_messages[msg_text] = text_addr
                rom.write_ptr(text_ptr, text_addr)
            rom.write_8(loc_addr + id_offset, 0xFF)
            rom.write_ptr(loc_addr + custom_offset, table_addr)


def set_tank_increments(rom: Rom, data: MarsschemazmTankIncrements) -> None:
    addr = tank_increase_amounts_addr(rom)
    rom.write_16(addr, data["energy_tank"])
    rom.write_16(addr + 2, data["missile_tank"])
    rom.write_8(addr + 4, data["super_missile_tank"])
    rom.write_8(addr + 5, data["power_bomb_tank"])
    rom.write_16(addr + 6, data["main_missiles"])
    rom.write_8(addr + 8, data["main_super_missiles"])
    rom.write_8(addr + 9, data["main_power_bombs"])
