import logging
from collections import defaultdict
from enum import Enum
from typing import Annotated, Literal, TypedDict

from ..common_types import AreaId, AreaRoomPair
from ..constants.door_types import DoorType
from ..constants.game_data import area_doors_ptrs, minimap_graphics
from ..constants.minimap_tiles import ColoredDoor, Content, Edge
from .auto_generated_types import MarsschemamfDoorLocksItem
from .constants.game_data import hatch_lock_event_count, hatch_lock_events
from .constants.minimap_tiles import (
    ALL_DOOR_TILE_IDS,
    ALL_DOOR_TILES,
    BLANK_TILE_IDS,
    BLANK_TRANSPARENT_TILE_IDS,
)
from ..minimap_tile_creator import create_tile
from ..rom import Rom
from ..room_entry import BlockLayer, RoomEntry
from ..tilemap import Tilemap

class HatchLock(Enum):
    OPEN = 0
    LEVEL_0 = 1
    LEVEL_1 = 2
    LEVEL_2 = 3
    LEVEL_3 = 4
    LEVEL_4 = 5
    LOCKED = 6


BG1_VALUES = {
    HatchLock.OPEN: 0x4,
    HatchLock.LEVEL_0: 0x6,
    HatchLock.LEVEL_1: 0x8,
    HatchLock.LEVEL_2: 0xA,
    HatchLock.LEVEL_3: 0xC,
    HatchLock.LEVEL_4: 0xE,
    HatchLock.LOCKED: 0x819A,
}

CLIP_VALUES = {
    HatchLock.OPEN: [0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    HatchLock.LEVEL_0: [0x30, 0x31, 0x32, 0x33, 0x34, 0x35],
    HatchLock.LEVEL_1: [0x36, 0x37, 0x38, 0x39, 0x3A, 0x3B],
    HatchLock.LEVEL_2: [0x40, 0x41, 0x42, 0x43, 0x44, 0x45],
    HatchLock.LEVEL_3: [0x46, 0x47, 0x48, 0x49, 0x4A, 0x4B],
    HatchLock.LEVEL_4: [0x3C, 0x3D, 0x3E, 0x4C, 0x4D, 0x4E],
    HatchLock.LOCKED: [0x10, 0x10, 0x10, 0x10, 0x10, 0x10],
}

CLIP_TO_HATCH_LOCK: dict[int, HatchLock] = {}
for lock, vals in CLIP_VALUES.items():
    for val in vals:
        CLIP_TO_HATCH_LOCK[val] = lock


EXCLUDED_DOORS = {
    (0, 0xB4),  # Restricted lab escape
    (2, 0x71),  # Cathedral -> Ripper Tower. Excluded to prevent more than 6 hatches in that room.
    (
        5,
        0x38,
    ),  # Arctic Containment -> Ripper Road. Excluded to prevent more than 6 hatches in that room.
    (
        2,
        0x1D,
    ),  # Cathedral (Before Destruction) -> C. Save Access. Excluded to prevent more than 6 hatches.
    (
        2,
        0x69,
    ),  # Cathedral (After Destruction) -> C. Save Access. Excluded to prevent more than 6 hatches.
}

HatchSlot = Annotated[int, "0 <= value <= 5"]

MinimapLocation = tuple[int, int]
"""`(X, Y)`"""


class MinimapLockChanges(TypedDict, total=False):
    left: HatchLock
    right: HatchLock


# TODO:
# - Optimize by only loading rooms that contain doors to modify
# - Split into more than one function for readability
def set_door_locks(rom: Rom, data: list[MarsschemamfDoorLocksItem]) -> None:
    door_locks = parse_door_lock_data(data)

    # Go through all doors in game in order
    doors_ptrs = area_doors_ptrs(rom)
    loaded_rooms: dict[AreaRoomPair, RoomEntry] = {}

    # (AreaID, RoomID): (BG1, Clipdata)
    loaded_bg1_and_clip: dict[AreaRoomPair, tuple[BlockLayer, BlockLayer]] = {}

    # (AreaID, RoomID): (CappedSlot, CaplessSlot)
    orig_room_hatch_slots: dict[AreaRoomPair, tuple[HatchSlot, HatchSlot]] = {}
    new_room_hatch_slots: dict[AreaRoomPair, tuple[HatchSlot, HatchSlot]] = {}

    hatch_slot_changes: dict[AreaRoomPair, dict[HatchSlot, HatchSlot]] = {}

    def factory() -> dict:
        return defaultdict(dict)

    # AreaID: {(MinimapX, MinimapY): {"left" | "right": HatchLock}}
    minimap_changes: dict[AreaId, dict[MinimapLocation, MinimapLockChanges]] = defaultdict(factory)

    for area in range(7):
        area_addr = rom.read_ptr(doors_ptrs + area * 4)
        for door in range(256):
            door_addr = area_addr + door * 0xC
            door_properties = rom.read_8(door_addr)

            # Check if at end of list
            if door_properties == 0:
                break

            # Skip doors that mage or asm marks as deleted
            room = rom.read_8(door_addr + 1)
            if room == 0xFF:
                continue

            door_type = DoorType(door_properties & 0xF)

            # Skip excluded doors and doors that aren't lockable/open hatches
            lock = door_locks.get((area, door))
            if (area, door) in EXCLUDED_DOORS or door_type not in [
                DoorType.OPEN_HATCH,
                DoorType.LOCKABLE_HATCH,
            ]:
                # Don't log the error if door is open and JSON says to change to open.
                if lock is not None and not (
                    lock is HatchLock.OPEN and door_type == DoorType.OPEN_HATCH
                ):
                    logging.error(
                        f"Area {area} door {door} type {door_type} cannot have its lock changed"
                    )
                continue

            # If the door type is an "Open Hatch" door, modify it to a lockable one
            if door_type == DoorType.OPEN_HATCH:
                upper_bits = door_properties & 0xF0
                door_properties = upper_bits | DoorType.LOCKABLE_HATCH
                rom.write_8(door_addr, door_properties)
                door_type = DoorType.LOCKABLE_HATCH

            # Load room's BG1 and clipdata if not already loaded
            area_room = (area, room)
            room_entry = loaded_rooms.get(area_room)
            if room_entry is None:
                room_entry = RoomEntry(rom, area, room)
                bg1 = room_entry.load_bg1()
                clip = room_entry.load_clip()
                loaded_rooms[area_room] = room_entry
                loaded_bg1_and_clip[area_room] = (bg1, clip)
                orig_room_hatch_slots[area_room] = (0, 5)
                new_room_hatch_slots[area_room] = (0, 5)
                hatch_slot_changes[area_room] = {}
            else:
                _tuple = loaded_bg1_and_clip.get(area_room)
                if _tuple is not None:
                    bg1, clip = _tuple

            # Check x exit distance to get facing direction
            x_exit = rom.read_8(door_addr + 7)
            facing_right = x_exit < 0x80
            dx = 1 if facing_right else -1

            # Get hatch position
            hatch_x = rom.read_8(door_addr + 2) + dx
            hatch_y = rom.read_8(door_addr + 4)

            # Get original hatch slot number
            capped_slot, capless_slot = orig_room_hatch_slots[area_room]
            clip_val = clip.get_block_value(hatch_x, hatch_y)
            orig_has_cap = clip_val != 0
            if orig_has_cap:
                # Has cap
                orig_hatch_slot = capped_slot
                capped_slot += 1
            else:
                # Capless
                orig_hatch_slot = capless_slot
                capless_slot -= 1
            orig_room_hatch_slots[area_room] = (capped_slot, capless_slot)

            # Get new hatch slot number
            capped_slot, capless_slot = new_room_hatch_slots[area_room]
            if lock == HatchLock.LOCKED:
                new_hatch_slot = orig_hatch_slot
            elif (lock is None and orig_has_cap) or (lock is not None and lock != HatchLock.OPEN):
                # Has cap
                new_hatch_slot = capped_slot
                capped_slot += 1
            else:
                # Capless
                new_hatch_slot = capless_slot
                capless_slot -= 1
            new_room_hatch_slots[area_room] = (capped_slot, capless_slot)

            if new_hatch_slot != orig_hatch_slot:
                hatch_slot_changes[area_room][orig_hatch_slot] = new_hatch_slot

            # Map tiles
            if lock is not None:
                minimap_x, minimap_y = room_entry.map_coords_at_block(hatch_x, hatch_y)

                minimap_areas = [area]
                if area == 0:
                    minimap_areas = [0, 9]  # Main Deck has two maps
                for minimap_area in minimap_areas:
                    map_tile = minimap_changes[minimap_area][minimap_x, minimap_y]
                    side: Literal["left", "right"] = "left" if facing_right else "right"
                    if side in map_tile and map_tile[side] != lock:
                        raise ValueError(
                            f"Minimap tile in area {area} at 0x{minimap_x:X}, 0x{minimap_y} "
                            f"has already changed {side} hatch to {map_tile[side].name} but is "
                            f"being set to {lock.name}"
                        )
                    map_tile[side] = lock

            # Overwrite BG1 and clipdata
            if lock is None:
                # Even if a hatch's lock hasn't changed, its slot may have changed
                lock = CLIP_TO_HATCH_LOCK.get(clip_val)
                if lock is None:
                    continue

            bg1_val = BG1_VALUES[lock]
            if facing_right:
                bg1_val += 1

            clip_val = CLIP_VALUES[lock][new_hatch_slot]

            for y in range(4):
                bg1.set_block_value(hatch_x, hatch_y + y, bg1_val)
                clip.set_block_value(hatch_x, hatch_y + y, clip_val)
                bg1_val += 0x10

    # Write BG1 and clipdata for each room
    for bg1, clip in loaded_bg1_and_clip.values():
        bg1.write()
        clip.write()

    fix_hatch_lock_events(rom, hatch_slot_changes)

    change_minimap_tiles(rom, minimap_changes)


def parse_door_lock_data(data: list[MarsschemamfDoorLocksItem]) -> dict[AreaRoomPair, HatchLock]:
    """Returns a dictionary of `(AreaID, RoomID): HatchLock` from the input data."""
    door_locks: dict[AreaRoomPair, HatchLock] = {}
    for entry in data:
        area_door = (entry["area"], entry["door"])
        lock = HatchLock[entry["lock_type"]]
        door_locks[area_door] = lock
    return door_locks


def fix_hatch_lock_events(
    rom: Rom, hatch_slot_changes: dict[AreaRoomPair, dict[HatchSlot, HatchSlot]]
) -> None:
    hatch_locks_addr = hatch_lock_events(rom)
    count = hatch_lock_event_count(rom)
    for i in range(count):
        addr = hatch_locks_addr + i * 5
        area = rom.read_8(addr + 1)
        room = rom.read_8(addr + 2) - 1
        changes = hatch_slot_changes.get((area, room))
        # Some rooms no longer have doors in rando
        if changes is None:
            continue
        hatch_flags = rom.read_8(addr + 3)
        new_flags = 0
        remain = (1 << 6) - 1
        for prev_slot, new_slot in changes.items():
            if (1 << prev_slot) & hatch_flags != 0:
                new_flags |= 1 << new_slot
            remain &= ~(1 << new_slot)
        new_flags |= hatch_flags & remain
        rom.write_8(addr + 3, new_flags)


def change_minimap_tiles(
    rom: Rom, minimap_changes: dict[AreaId, dict[MinimapLocation, MinimapLockChanges]]
) -> None:
    MAP_EDGES: dict[HatchLock, Edge | ColoredDoor] = {
        HatchLock.OPEN: Edge.DOOR,
        HatchLock.LEVEL_0: Edge.DOOR,
        HatchLock.LEVEL_1: ColoredDoor.BLUE,
        HatchLock.LEVEL_2: ColoredDoor.GREEN,
        HatchLock.LEVEL_3: ColoredDoor.YELLOW,
        HatchLock.LEVEL_4: ColoredDoor.RED,
        HatchLock.LOCKED: Edge.DOOR,
        # HatchLock.LOCKED: Edge.WALL,
    }

    all_door_tile_ids = dict(ALL_DOOR_TILE_IDS)
    remaining_blank_tile_ids = list(BLANK_TILE_IDS)
    remaining_blank_transparent_tile_ids = list(BLANK_TRANSPARENT_TILE_IDS)

    for area, area_map in minimap_changes.items():
        with Tilemap.from_minimap(rom, area) as minimap:
            for (x, y), tile_changes in area_map.items():
                tile_id, palette, h_flip, v_flip = minimap.get_tile_value(x, y)

                try:
                    tile_data = ALL_DOOR_TILES[tile_id]
                except KeyError:
                    logging.warning(
                        f"Minimap tile 0x{tile_id:X} in area {area} "
                        + f"at 0x{x:X}, 0x{y:X} was expected to have a door"
                    )
                    continue

                # Account for h_flip before changing edges
                left = tile_changes.get("left")
                right = tile_changes.get("right")
                if h_flip:
                    left, right = right, left

                # Replace edges
                edges = tile_data.edges
                if left is not None:
                    edges = edges._replace(left=MAP_EDGES[left])
                if right is not None:
                    edges = edges._replace(right=MAP_EDGES[right])
                orig_new_tile_data = tile_data._replace(edges=edges)
                new_tile_data = orig_new_tile_data

                def tile_exists() -> bool:
                    return new_tile_data in all_door_tile_ids

                if new_tile_data.content.can_h_flip and not tile_exists():
                    # Try flipping horizontally
                    new_tile_data = orig_new_tile_data.h_flip()
                    if tile_exists():
                        h_flip = not h_flip

                if new_tile_data.content.can_v_flip and not tile_exists():
                    # Try flipping vertically
                    new_tile_data = orig_new_tile_data.v_flip()
                    if tile_exists():
                        v_flip = not v_flip

                if (
                    new_tile_data.content.can_h_flip
                    and new_tile_data.content.can_v_flip
                    and not tile_exists()
                ):
                    # Try flipping it both ways
                    new_tile_data = orig_new_tile_data.v_flip()
                    new_tile_data = new_tile_data.h_flip()
                    if tile_exists():
                        v_flip = not v_flip
                        h_flip = not h_flip

                if not tile_exists():
                    logging.debug(
                        f"Could not reuse existing map tile for area {area} at {x:X}, {y:X}."
                    )
                    logging.debug(f"  Desired tile: {orig_new_tile_data.as_str}")

                    # Try getting a blank tile ID
                    requires_transparent_tile = orig_new_tile_data.content == Content.TUNNEL or any(
                        isinstance(e, Edge) and e == Edge.SHORTCUT for e in orig_new_tile_data.edges
                    )
                    blank_tile_ids = (
                        remaining_blank_transparent_tile_ids
                        if requires_transparent_tile
                        else remaining_blank_tile_ids
                    )
                    is_item = orig_new_tile_data.content == Content.ITEM
                    new_tile_id = get_blank_minimap_tile_id(blank_tile_ids, is_item)

                    if new_tile_id is not None:
                        # Create new graphics for the tile
                        gfx = create_tile(orig_new_tile_data)
                        new_tiles = [(new_tile_id, gfx, orig_new_tile_data)]

                        # If the tile has an item, add another tile for the obtained item
                        if is_item:
                            data = orig_new_tile_data._replace(content=Content.OBTAINED_ITEM)
                            gfx = create_tile(data)
                            new_tiles.append((new_tile_id + 1, gfx, data))

                        # If the tile doesn't fill the whole square, add another tile with
                        # transparency
                        if requires_transparent_tile:
                            for tile_id, gfx, data in list(new_tiles):
                                data = data._replace(transparent=True)
                                gfx = create_tile(data)
                                new_tiles.append((tile_id + 0x20, gfx, data))

                        for tile_id, gfx, data in new_tiles:
                            addr = minimap_graphics(rom) + tile_id * 32
                            rom.write_bytes(addr, gfx)

                            all_door_tile_ids[data] = tile_id
                            logging.debug(f"  Created new tile: 0x{tile_id:X}.")

                        new_tile_data = orig_new_tile_data
                    else:
                        # No blank tiles remaining, try replacing with open doors
                        logging.warning("  No blank tiles available, trying open doors.")
                        if (left is not None) and tile_data.edges.left.is_door:
                            edges = edges._replace(left=Edge.DOOR)
                        if (right is not None) and tile_data.edges.right.is_door:
                            edges = edges._replace(right=Edge.DOOR)
                        new_tile_data = orig_new_tile_data._replace(edges=edges)

                        if not tile_exists():
                            logging.warning("  Still no luck. Using vanilla tile.")

                        logging.warning("")

                if tile_exists():
                    minimap.set_tile_value(
                        x,
                        y,
                        all_door_tile_ids[new_tile_data],
                        palette,
                        h_flip,
                        v_flip,
                    )


def get_blank_minimap_tile_id(blank_tile_ids: list[int], is_item: bool) -> int | None:
    """Finds a usable tile from the provided list of blank tile IDs. Item tiles require a blank
    tile next to them. Non-item tiles can use any blank tile, but solitary tiles are preferred
    to save more tiles for item tiles."""
    valid_tile_id: int | None = None
    for tile_id in blank_tile_ids:
        if is_item:
            # Item tiles require a blank tile next to them for the obtained item tile
            if tile_id + 1 in blank_tile_ids:
                valid_tile_id = tile_id
                break
        else:
            # Prefer solitary blank tiles for non-item tiles
            if tile_id + 1 not in blank_tile_ids:
                valid_tile_id = tile_id
                break
            elif valid_tile_id is None:
                valid_tile_id = tile_id
    if valid_tile_id is not None:
        blank_tile_ids.remove(valid_tile_id)
        if is_item:
            blank_tile_ids.remove(valid_tile_id + 1)
    return valid_tile_id
