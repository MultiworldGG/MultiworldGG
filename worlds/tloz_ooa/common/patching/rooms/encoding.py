import heapq
import logging
import os
from collections import Counter, defaultdict
from importlib.resources import files

from .. import rooms
from ..RomData import RomData
from ..Util import simple_hex
from ..z80asm.Assembler import GameboyAddress


def compress_small_room(room: bytearray, mode: int) -> bytearray:
    room_data = bytearray()
    for slice_start in range(0x00, 0x50, mode * 0x08):
        room_slice = room[slice_start:slice_start + mode * 0x08]
        common_item = Counter(room_slice).most_common(1)[0][0]
        mask = 0
        purified_slice = bytearray()
        for i in range(len(room_slice)):
            if room_slice[i] == common_item:
                mask |= 1 << i
            else:
                purified_slice.append(room_slice[i])
        room_data.extend(mask.to_bytes(mode, "little"))
        room_data.append(common_item)
        room_data.extend(purified_slice)

    return room_data


def encode_group_data_small(room_data: list[bytearray], first_room: int) -> tuple[int, bytearray, bytearray]:
    room_infos = bytearray()
    group_data = bytearray()

    for room_id in range(first_room, first_room + 0x100):
        best_encoding = (0, room_data[room_id])
        for mode in [1, 2]:
            new_encoding = compress_small_room(room_data[room_id], mode)
            if len(new_encoding) < len(best_encoding[1]):
                best_encoding = (mode, new_encoding)
        room_info = len(group_data) + (best_encoding[0] << 14)
        room_infos.extend(room_info.to_bytes(2, "little"))
        group_data.extend(best_encoding[1])
    return 1, room_infos, group_data


def compress_big_room(room: bytearray, compression_dict: bytes) -> bytearray:
    room_data = bytearray()
    mask_data = bytearray()
    slice_start = 0
    mask = 0
    mask_length = 0
    while slice_start < 0xb0:
        if mask_length == 8:
            room_data.append(mask)
            room_data.extend(mask_data)
            mask_length = 0
            mask = 0
            mask_data.clear()
        for slice_size in range(min(0xb0 - slice_start, 18), 2, -1):
            pos = compression_dict.find(room[slice_start:slice_start + slice_size])
            if pos != -1:
                mask |= 1 << mask_length
                slice_start += slice_size
                mask_length += 1
                assert pos < 0x1000
                data = pos + ((slice_size - 3) << 12)
                mask_data.extend(data.to_bytes(2, "little"))
                break
        else:
            mask_data.append(room[slice_start])
            slice_start += 1
            mask_length += 1

    room_data.append(mask)
    room_data.extend(mask_data)
    # Rest is garbage, but shouldn't be read anyway

    return room_data


def compute_score(parent_slice: bytes, all_slices: dict[bytes, int]) -> int:
    score = (1.125 * len(parent_slice) - 2.125) * all_slices[parent_slice]
    # Using is costs 2 bytes and 1 bit, compared to 1 byte and 1 bit per character

    for slice_length in range(3, len(parent_slice)):
        seen_slices = set()
        for dict_slice_start in range(0, len(parent_slice) - slice_length):
            sub_slice = bytes(parent_slice[dict_slice_start:dict_slice_start + slice_length])
            if sub_slice not in seen_slices:
                score += (1.125 * slice_length - 2.125) * (
                        all_slices[sub_slice] - all_slices[parent_slice])  # Adds the extra ones
    return score / len(parent_slice)


def make_compression_dict(room_data: list[bytearray], first_room: int) -> bytes:
    all_slices = defaultdict(lambda: 0)
    last_appearance = defaultdict(lambda: -0x100)
    for slice_size in range(3, 19):
        for room_id in range(first_room, first_room + 0x100):
            last_appearance.clear()
            for slice_start in range(0x00, 0xb0 - slice_size):
                current_slice = bytes(room_data[room_id][slice_start:slice_start + slice_size])
                if slice_start - last_appearance[current_slice] >= slice_size:
                    last_appearance[current_slice] = slice_start
                    all_slices[current_slice] += 1
    heap = []
    for dict_slice in all_slices:
        score = compute_score(dict_slice, all_slices)
        if score > 15:
            heapq.heappush(heap, (-score, dict_slice))
    compression_dict = bytearray()
    while len(compression_dict) < 0xffe:  # Can't do anything if the dict is lacking 2 bytes
        old_score, current_slice = heap[0]
        if len(current_slice) > 0x1000 - len(compression_dict) or all_slices[current_slice] == 0:
            heapq.heappop(heap)
            continue
        score = compute_score(current_slice, all_slices)
        if -old_score != score:
            heapq.heapreplace(heap, (-score, current_slice))
        else:
            cursor = len(compression_dict)
            compression_dict.extend(current_slice)
            heapq.heappop(heap)

            # Clear all of the matches to clear their score
            for slice_length in range(3, 19):
                for slice_start in range(cursor - slice_length + 1, cursor + len(current_slice) - slice_length):
                    sub_slice = bytes(compression_dict[slice_start:slice_start + slice_length])
                    all_slices[sub_slice] = 0

    compression_dict = compression_dict.rjust(0x1000, b'\x00')
    return bytes(compression_dict)


def load_compression_dict(first_room: int, seasons: bool) -> bytes | None:
    resource = files(rooms).joinpath("compression_dict", "seasons" if seasons else "ages", f"dict_{simple_hex(first_room, 3)}.bin")

    if resource.is_file():
        return resource.read_bytes()

    return None


def encode_group_data_big(room_data: list[bytearray], first_room: int, seasons: bool) -> tuple[int, bytearray, bytearray]:
    compression_dict = load_compression_dict(first_room, seasons)
    if not compression_dict:
        logging.warning("No compression dict found in the apworld, generating one, it will take some time...")
        compression_dict = make_compression_dict(room_data, first_room)
        if __debug__:
            path = os.path.join(
                os.path.dirname(rooms.__file__),
                "compression_dict",
                ("seasons" if seasons else "ages"),
                f"dict_{simple_hex(first_room, 3)}.bin"
            )
            with open(path, "wb") as f:
                f.write(compression_dict)
            logging.info(f"Saved a compression dict to {path} for future use.")
    room_infos = bytearray()
    room_infos.extend(compression_dict)
    group_data = bytearray()

    for room_id in range(first_room, first_room + 0x100):
        room_info = len(group_data) + 0x200
        room_infos.extend(room_info.to_bytes(2, "little"))
        compressed_room = compress_big_room(room_data[room_id], compression_dict)
        group_data.extend(compressed_room)
    return 0, room_infos, group_data


def encode_group_data(room_data: list[bytearray], group: int, seasons: bool) -> tuple[int, bytearray, bytearray]:
    first_room = group * 0x100
    if len(room_data[first_room]) == 0x50:
        return encode_group_data_small(room_data, first_room)
    else:
        return encode_group_data_big(room_data, first_room, seasons)


def write_room_data(rom: RomData, room_data: list[bytearray], seasons: bool):
    if seasons:
        room_layout_group_table = GameboyAddress(0x04, 0x4c4c).address_in_rom()
        small_group_layout_table = GameboyAddress(0x16, 0x7006)
        big_group_layout_table = GameboyAddress(0x18, 0x4000)
        room_data_current = GameboyAddress(0x21, 0x4e04)
        room_data_end = GameboyAddress(0x27, 0x790c).address_in_rom()  # As often, included
        num_groups = 7
    else:
        room_layout_group_table = GameboyAddress(0x04, 0x4f6c).address_in_rom()
        small_group_layout_table = GameboyAddress(0x17, 0x66e3)
        big_group_layout_table = GameboyAddress(0x1c, 0x59c0)
        room_data_current = GameboyAddress(0x23, 0x67e3)
        room_data_end = GameboyAddress(0x28, 0x7f3b).address_in_rom()  # As often, included
        num_groups = 6

    group_layout_table = small_group_layout_table
    for group in range(num_groups):
        current_address = room_layout_group_table + group * 8
        room_type, room_infos, group_data = encode_group_data(room_data, group, seasons)
        if room_type == 0 and group_layout_table < big_group_layout_table:
            group_layout_table = big_group_layout_table

        # Room type
        rom.write_byte(current_address, room_type)

        # Room infos address
        rom.write_byte(current_address + 1, group_layout_table.bank)
        rom.write_word(current_address + 2, group_layout_table.to_word_int())

        # Room infos content
        rom.write_bytes(group_layout_table.address_in_rom(), room_infos)
        group_layout_table += len(room_infos)

        # Group's data address
        rom.write_byte(current_address + 4, room_data_current.bank)
        rom.write_word(current_address + 5, room_data_current.to_word_int())

        # Group's data content
        rom.write_bytes(room_data_current.address_in_rom(), group_data)
        room_data_current += len(group_data)
        assert room_data_current.address_in_rom() <= room_data_end, f"Room data is {hex(room_data_current.address_in_rom() - room_data_end)} bytes too long"
    print(f"Room data ends at {room_data_current}, {hex(room_data_end - room_data_current.address_in_rom())} bytes left")
