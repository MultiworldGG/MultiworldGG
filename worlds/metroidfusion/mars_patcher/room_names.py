from .common_types import AreaId, RoomNamesItem, TypeU8
from .constants.game_data import room_names_addr
from .rom import Rom
from .text import MAX_LINE_WIDTH, MessageType, encode_text


# ROM has:
# - A list that contains pointers to area room names
# - Area room names are indexed by room ID. This means some entries
#   are never used, but this allows for easy lookup
def write_room_names(rom: Rom, data: list[RoomNamesItem]) -> None:
    if rom.is_zm():
        max_width = 192  # 3 tile margin from edge of screen
    else:
        max_width = MAX_LINE_WIDTH
    room_names_table_addr = room_names_addr(rom)
    seen_rooms: set[tuple[AreaId, TypeU8]] = set()

    for room_name_entry in data:
        area_id = room_name_entry["area"]
        room_id = room_name_entry["room"]
        room_name = room_name_entry["name"]

        # Check that the room wasn't already set
        assert (area_id, room_id) not in seen_rooms, "Duplicate room name provided."
        seen_rooms.add((area_id, room_id))

        # Table is indexed by area ID, then by room ID
        area_room_name_ptrs = rom.read_ptr(room_names_table_addr + (area_id * 4))
        room_name_ptr = area_room_name_ptrs + (room_id * 4)

        encoded_text = encode_text(rom, MessageType.TWO_LINE, room_name, max_width)
        rom.write_data_with_pointers(encoded_text, [room_name_ptr])
