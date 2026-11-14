from ..constants.game_data import area_doors_ptrs, spriteset_ptrs
from ..rom import Rom
from ..room_entry import RoomEntry
from .auto_generated_types import (
    MarsschemazmStartingItems,
    MarsschemazmStartingLocation,
)
from .constants.items import (
    BEAM_BOMB_FLAGS,
    EXTRA_ITEM_FLAGS,
    SUIT_MISC_FLAGS,
    SuitType,
)
from .constants.reserved_space import ReservedPointersZM
from .constants.sprites import SpriteIdZM


def set_starting_location(rom: Rom, data: MarsschemazmStartingLocation) -> None:
    area = data["area"]
    room = data["room"]
    # Don't do anything for area 0 room 0
    if area == 0 and room == 0:
        return
    # Find any door in the provided room
    door = find_door_in_room(rom, area, room)
    # Check if save pad in room
    pos = find_save_pad_position(rom, area, room)
    if pos is not None:
        x_pos, y_pos = pos
    else:
        x_pos = data["block_x"]
        y_pos = data["block_y"]
    # Write to rom (see struct StartingInfo in structs/randomizer.h)
    starting_info_addr = rom.read_ptr(ReservedPointersZM.STARTING_INFO_PTR.value)
    rom.write_8(starting_info_addr, area)
    rom.write_8(starting_info_addr + 1, room)
    rom.write_8(starting_info_addr + 2, door)
    rom.write_8(starting_info_addr + 3, x_pos)
    rom.write_8(starting_info_addr + 4, y_pos)
    # See struct InGameCutsceneData in structs/in_game_cutscene.h
    intro_cutscene_addr = rom.read_ptr(ReservedPointersZM.INTRO_CUTSCENE_DATA_PTR.value)
    rom.write_8(intro_cutscene_addr + 1, area)


def find_door_in_room(rom: Rom, area: int, room: int) -> int:
    door_addr = rom.read_ptr(area_doors_ptrs(rom) + area * 4)
    door = None
    for d in range(256):
        if rom.read_8(door_addr) == 0:
            break
        if rom.read_8(door_addr + 1) == room:
            # Don't use door 0 in Crateria
            if not (area == 5 and d == 0):
                door = d
                break
        door_addr += 0xC
    if door is None:
        raise ValueError(f"No door found for area {area} room {room:X}")
    return door


def find_save_pad_position(rom: Rom, area: int, room: int) -> tuple[int, int] | None:
    # Check if room's spriteset has save pad
    save_platform_ids = {SpriteIdZM.SAVE_PLATFORM.value, SpriteIdZM.SAVE_PLATFORM_CHOZODIA.value}
    room_entry = RoomEntry(rom, area, room)
    spriteset = room_entry.default_spriteset()
    ss_addr = rom.read_ptr(spriteset_ptrs(rom) + spriteset * 4)
    ss_idx = None
    for i in range(15):
        sprite_id = rom.read_8(ss_addr)
        if sprite_id == 0:
            break
        if sprite_id in save_platform_ids:
            ss_idx = i
            break
        ss_addr += 2
    if ss_idx is None:
        return None
    # Find save pad in sprite layout list
    layout_addr = room_entry.default_sprite_layout_addr()
    for i in range(24):
        sp_y = rom.read_8(layout_addr)
        sp_x = rom.read_8(layout_addr + 1)
        prop = rom.read_8(layout_addr + 2)
        if sp_x == 0xFF and sp_y == 0xFF and prop == 0xFF:
            break
        if (prop & 0xF) - 1 == ss_idx:
            return sp_x, sp_y - 1
        layout_addr += 3
    # No save pad found
    return None


def set_starting_items(rom: Rom, data: MarsschemazmStartingItems) -> None:
    def get_ability_flags(ability_flags: dict[str, int]) -> int:
        status = 0
        for ability, flag in ability_flags.items():
            if ability in abilities:
                status |= flag
        return status

    # Get health/ammo amounts
    energy = data.get("energy", 99)
    missiles = data.get("missiles", 0)
    super_missiles = data.get("super_missiles", 0)
    power_bombs = data.get("power_bombs", 0)
    # Get ability status flags
    abilities = data.get("abilities", [])
    beam_bomb_status = get_ability_flags(BEAM_BOMB_FLAGS)
    suit_misc_status = get_ability_flags(SUIT_MISC_FLAGS)
    main_items_status = get_ability_flags(EXTRA_ITEM_FLAGS)
    # Get downloaded map flags
    maps = data.get("downloaded_maps", range(7))
    map_status = 0
    for map in maps:
        map_status |= 1 << map
    # Get suit type
    suit_str = data.get("suit_type")
    suit_type = SuitType[suit_str] if suit_str else SuitType.NORMAL
    # Get ziplines activated
    ziplines = data.get("ziplines_activated", False)

    # Write to rom (see struct StartingInfo in structs/randomizer.h)
    addr = rom.read_ptr(ReservedPointersZM.STARTING_INFO_PTR.value)
    rom.write_16(addr + 6, energy)
    rom.write_16(addr + 8, missiles)
    rom.write_8(addr + 0xA, super_missiles)
    rom.write_8(addr + 0xB, power_bombs)
    rom.write_8(addr + 0xC, beam_bomb_status)
    rom.write_8(addr + 0xD, suit_misc_status)
    rom.write_8(addr + 0xE, main_items_status)
    rom.write_8(addr + 0xF, map_status)
    rom.write_8(addr + 0x10, suit_type.value)
    rom.write_8(addr + 0x11, ziplines)
    # TODO: Disabled hints
    rom.write_8(addr + 0x12, 0)
