from ..RomData import RomData
from ..z80asm.Assembler import GameboyAddress

def decompress_room(rom: RomData, base_address: int, room_type: int, room_info: int, group_dict: None | bytearray) -> bytearray:
    if room_type == 1:  # Small room
        compression_mode = room_info >> 14
        room_pointer = base_address + room_info % 0x4000

        if compression_mode == 0:
            # That's just not compressed
            return rom.read_bytes(room_pointer, 0x50)
        room_data = bytearray()

        while len(room_data) < 0x50:
            # The way data is compressed is:
            # 1- write a bit mask of len compression_mode * 8
            # 2- write which is the most common tile in the range (skipped if mask is 0)
            # 3- write the actual value for every 0 in the mask, 1 being the step 2 tile instead

            if compression_mode == 1:
                mask = rom.read_byte(room_pointer)
                room_pointer += 1
            else:
                mask = rom.read_word(room_pointer)
                room_pointer += 2

            common_byte = -1
            if mask != 0:
                common_byte = rom.read_byte(room_pointer)
                room_pointer += 1

            # mask:
            # 0 = literal byte
            # 1 = common byte
            for i in range(8 * compression_mode):
                if mask & (1 << i):
                    # Apply the common byte
                    room_data.append(common_byte)
                else:
                    room_data.append(rom.read_byte(room_pointer))
                    room_pointer += 1
        return room_data
    else:  # Large room, with dict compression
        room_pointer = base_address + room_info - 0x200  # I would like to know why that -200 exists
        room_data = bytearray()
        while len(room_data) < 0xb0:
            # Using a mask again:
            # 0 = literal byte
            # 1 = 2 bytes dict access
            mask = rom.read_byte(room_pointer)
            room_pointer += 1

            for i in range(8):
                if mask & (1 << i):
                    data = rom.read_word(room_pointer)
                    room_pointer += 2
                    data_pointer = data % 0x1000
                    data_length = (data >> 12) + 3 # Max is 18, used in vanilla
                    room_data.extend(group_dict[data_pointer:data_pointer + data_length])
                else:
                    room_data.append(rom.read_byte(room_pointer))
                    room_pointer += 1
        room_data = room_data[:0xb0]
        return room_data


def decompress_rooms(rom: RomData, seasons: bool = True) -> list[bytearray]:
    if seasons:
        room_layout_group_table = GameboyAddress(0x04, 0x4c4c).address_in_rom()
        num_groups = 7
    else:
        room_layout_group_table = GameboyAddress(0x04, 0x4f6c).address_in_rom()
        num_groups = 6

    room_data = []
    for group in range(num_groups):
        current_address = room_layout_group_table + group * 8
        room_type = rom.read_byte(current_address)
        table_address = GameboyAddress(
            rom.read_byte(current_address + 1),
            rom.read_word(current_address + 2)
        ).address_in_rom()
        base_address = GameboyAddress(
            rom.read_byte(current_address + 4),
            rom.read_word(current_address + 5)
        ).address_in_rom()

        group_dict = None
        if room_type != 1:
            group_dict = rom.read_bytes(table_address, 0x1000)
            table_address += 0x1000
            if __debug__ and False:
                # Output the dict to see how it looks like
                import os
                from ..Util import simple_hex
                file = open(os.path.join("output", simple_hex(group, 2) + ".bin"), "wb")
                file.write(group_dict)

        for room in range(0x100):
            room_info = rom.read_word(table_address + room * 2)

            room_data.append(decompress_room(rom, base_address, room_type, room_info, group_dict))
    return room_data
