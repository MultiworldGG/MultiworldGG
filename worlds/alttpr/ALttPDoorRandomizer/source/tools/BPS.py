# Code derived from https://github.com/marcrobledo/RomPatcher.js (MIT License)

import sys

from time import perf_counter

from collections import defaultdict
from binascii import crc32
try:
    from fast_enum import FastEnum
except ImportError:
    from enum import IntFlag as FastEnum


def bps_get_vlv_len(data):
    length = 0
    while True:
        x = data & 0x7f
        data >>= 7
        if data == 0:
            length += 1
            break
        length += 1
        data -= 1
    return length


def bps_read_vlv(stream):
    data, shift = 0, 1
    while True:
        x = stream.read(1)[0]
        data += (x & 0x7f) * shift
        if x & 0x80:
            return data
        shift <<= 7
        data += shift


class Bps:
    def __init__(self):
        self.source_size = 0
        self.target_size = 0
        self.metadata = ''
        self.actions = []
        self.source_checksum = 0
        self.target_checksum = 0
        self.patch_checksum = 0

        self.binary_ba = bytearray()
        self.offset = 0

    def write_to_binary(self):
        patch_size = 4
        patch_size += bps_get_vlv_len(self.source_size)
        patch_size += bps_get_vlv_len(self.target_size)
        patch_size += bps_get_vlv_len(len(self.metadata))
        patch_size += len(self.metadata)

        for action in self.actions:
            mode, length, data = action
            patch_size += bps_get_vlv_len(((length - 1) << 2) + mode)

            if mode == BpsMode.BPS_ACTION_TARGET_READ:
                patch_size += length
            elif mode == BpsMode.BPS_ACTION_SOURCE_COPY or mode == BpsMode.BPS_ACTION_TARGET_COPY:
                patch_size += bps_get_vlv_len((abs(data) << 1) + (1 if data < 0 else 0))
        patch_size += 12

        self.binary_ba = bytearray(patch_size)
        self.write_string('BPS1')
        self.bps_write_vlv(self.source_size)
        self.bps_write_vlv(self.target_size)
        self.bps_write_vlv(len(self.metadata))
        self.write_string(self.metadata)

        for action in self.actions:
            mode, length, data = action
            self.bps_write_vlv(((length - 1) << 2) + mode)
            if mode == BpsMode.BPS_ACTION_TARGET_READ:
                self.write_bytes(data)
            elif mode == BpsMode.BPS_ACTION_SOURCE_COPY or mode == BpsMode.BPS_ACTION_TARGET_COPY:
                self.bps_write_vlv((abs(data) << 1) + (1 if data < 0 else 0))
        self.write_u32(self.source_checksum)
        self.write_u32(self.target_checksum)
        self.write_u32(self.patch_checksum)

    def write_string(self, string):
        for ch in string:
            self.binary_ba[self.offset] = ord(ch)
            self.offset += 1

    def write_byte(self, byte):
        self.binary_ba[self.offset] = byte
        self.offset += 1

    def write_bytes(self, m_bytes):
        for byte in m_bytes:
            self.binary_ba[self.offset] = byte
            self.offset += 1

    def write_u32(self, data):
        self.binary_ba[self.offset] = data & 0x000000ff
        self.binary_ba[self.offset+1] = (data & 0x0000ff00) >> 8
        self.binary_ba[self.offset+2] = (data & 0x00ff0000) >> 16
        self.binary_ba[self.offset+3] = (data & 0xff000000) >> 24
        self.offset += 4

    def bps_write_vlv(self, data):
        while True:
            x = data & 0x7f
            data >>= 7
            if data == 0:
                self.write_byte(0x80 | x)
                break
            self.write_byte(x)
            data -= 1


class BpsMode(FastEnum):
    BPS_ACTION_SOURCE_READ = 0
    BPS_ACTION_TARGET_READ = 1
    BPS_ACTION_SOURCE_COPY = 2
    BPS_ACTION_TARGET_COPY = 3


def create_bps_from_data(original, modified):
    patch = Bps()
    patch.source_size = len(original)
    patch.target_size = len(modified)

    patch.actions = create_bps_linear(original, modified)

    patch.source_checksum = crc32(original)
    patch.target_checksum = crc32(modified)
    patch.write_to_binary()
    patch.patch_checksum = crc32(patch.binary_ba[:-4])
    patch.offset = len(patch.binary_ba) - 4
    patch.write_u32(patch.patch_checksum)
    return patch


def create_bps_delta(original, modified):
    patch_actions = []
    source_data = original
    target_data = modified
    source_size = len(original)
    target_size = len(modified)

    source_relative_offset = 0
    target_relative_offset = 0
    output_offset = 0

    source_tree = defaultdict(list)
    source_tree_2 = defaultdict(list)
    target_tree = defaultdict(list)

    t1_start = perf_counter()
    for offset in range(0, source_size):
        symbol = source_data[offset]
        if offset < source_size - 1:
            symbol |= source_data[offset + 1] << 8
        source_tree[symbol].append(offset)
    print(f'Elasped Time 1: {perf_counter()-t1_start}')

    source_array = list(source_data)

    t2_start = perf_counter()
    for offset in range(0, source_size):
        symbol = source_array[offset]
        if offset < source_size - 1:
            symbol |= source_array[offset + 1] << 8
        source_tree_2[symbol].append(offset)
    print(f'Elasped Time 2: {perf_counter()-t2_start}')

    trl = {'target_read_length': 0}

    def target_read_flush(buffer):
        if buffer['target_read_length']:
            action = (BpsMode.BPS_ACTION_TARGET_READ, buffer['target_read_length'], [])
            patch_actions.append(action)
            offset = output_offset - buffer['target_read_length']
            while buffer['target_read_length']:
                action[2].append(target_data[offset])
                offset += 1
                buffer['target_read_length'] -= 1

    while output_offset < target_size:
        max_length, max_offset, mode = 0, 0, BpsMode.BPS_ACTION_TARGET_READ

        symbol = target_data[output_offset]

        if output_offset < target_size - 1:
            symbol |= target_data[output_offset + 1] << 8

        # source read
        length, offset = 0, output_offset
        while offset < source_size and offset < target_size and source_data[offset] == target_data[offset]:
            length += 1
            offset += 1
        if length > max_length:
            max_length, mode = length, BpsMode.BPS_ACTION_SOURCE_READ

        # source copy
        for node in source_tree[symbol]:
            length, x, y = 0, node, output_offset
            while x < source_size and y < target_size and source_data[x] == target_data[y]:
                length += 1
                x += 1
                y += 1
            if length > max_length:
                max_length, max_offset, mode = length, node, BpsMode.BPS_ACTION_SOURCE_COPY

        # target copy
        for node in target_tree[symbol]:
            length, x, y = 0, node, output_offset
            while y < target_size and target_data[x] == target_data[y]:
                length += 1
                x += 1
                y += 1
            if length > max_length:
                max_length, max_offset, mode = length, node, BpsMode.BPS_ACTION_TARGET_COPY
        target_tree[symbol].append(output_offset)

        # target read
        if max_length < 4:
            max_length = min(1, target_size - output_offset)
            mode = BpsMode.BPS_ACTION_TARGET_READ

        if mode != BpsMode.BPS_ACTION_TARGET_READ:
            target_read_flush(trl)

        if mode == BpsMode.BPS_ACTION_SOURCE_READ:
            patch_actions.append((mode, max_length, None))
        elif mode == BpsMode.BPS_ACTION_TARGET_READ:
            trl['target_read_length'] += max_length
        else:
            if mode == BpsMode.BPS_ACTION_SOURCE_COPY:
                relative_offset = max_offset - source_relative_offset
                source_relative_offset = max_offset + max_length
            else:
                relative_offset = max_offset - target_relative_offset
                target_relative_offset = max_offset + max_length
            patch_actions.append((mode, max_length, relative_offset))

        output_offset += max_length

    target_read_flush(trl)

    return patch_actions


def create_bps_linear(original, modified):
    patch_actions = []
    source_data = original
    target_data = modified
    source_size = len(original)
    target_size = len(modified)

    target_relative_offset = 0
    output_offset = 0
    trl = {'target_read_length': 0}

    def target_read_flush(buffer):
        if buffer['target_read_length']:
            action = (BpsMode.BPS_ACTION_TARGET_READ, buffer['target_read_length'], [])
            patch_actions.append(action)
            offset = output_offset - buffer['target_read_length']
            while buffer['target_read_length']:
                action[2].append(target_data[offset])
                offset += 1
                buffer['target_read_length'] -= 1

    eof = min(source_size, target_size)
    while output_offset < target_size:
        src_length, n = 0, 0

        while output_offset + n < eof:
            if source_data[output_offset + n] != target_data[output_offset + n]:
                break
            src_length += 1
            n += 1

        rle_length, n = 0, 1
        while output_offset + n < target_size:
            if target_data[output_offset] != target_data[output_offset + n]:
                break
            rle_length += 1
            n += 1

        if rle_length >= 4:
            trl['target_read_length'] += 1
            output_offset += 1
            target_read_flush(trl)

            relative_offset = (output_offset - 1) - target_relative_offset
            patch_actions.append((BpsMode.BPS_ACTION_TARGET_COPY, rle_length, relative_offset))
            output_offset += rle_length
            target_relative_offset = output_offset - 1
        elif src_length >= 4:
            target_read_flush(trl)
            patch_actions.append((BpsMode.BPS_ACTION_SOURCE_READ, src_length, None))
            output_offset += src_length
        else:
            trl['target_read_length'] += 1
            output_offset += 1

    target_read_flush(trl)

    return patch_actions


if __name__ == '__main__':
    with open(sys.argv[1], 'rb') as source:
        sourcedata = source.read()

    with open(sys.argv[2], 'rb') as target:
        targetdata = target.read()

    patch = create_bps_from_data(sourcedata, targetdata)
    with open(sys.argv[3], 'wb') as patchfile:
        patchfile.write(patch.binary_ba)



