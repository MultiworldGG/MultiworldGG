import os

from ..Util import simple_hex


def dump_rooms_to_txt(rooms: list[bytearray], path: str) -> None:
    for room in range(len(rooms)):
        file = open(os.path.join(path, simple_hex(room, 4) + ".txt"), "w")
        current_room = rooms[room]
        if len(current_room) == 0x50:
            line_size = 10
        else:
            line_size = 16

        current_line = line_size
        for tile in current_room:
            if current_line == 0:
                file.write("\n")
                current_line = line_size
            if current_line != line_size:
                file.write(" ")
            file.write(simple_hex(tile, 2))
            current_line -= 1