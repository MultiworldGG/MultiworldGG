import json
import os
import platform
import struct
import subprocess
import copy
import threading
from .Utils import subprocess_args, data_path, get_version_bytes, __version__
from Utils import user_path
from .ntype import BigStream
from .crc import calculate_crc

DMADATA_START = 0x7430
OVERLAY_TABLE_START = 0xB5E490
OVERLAY_TABLE_OFFSET = 0
OVERLAY_TABLE_ENTRY_SIZE = 0x20
PAUSE_PLAYER_OVERLAY_TABLE_START = 0xB743E0
PAUSE_PLAYER_OVERLAY_TABLE_ENTRY_SIZE = 0x1C
PAUSE_PLAYER_OVERLAY_TABLE_OFFSET = 4

NUM_OVERLAY_ENTRIES = 0x1D7
NUM_PAUSE_PLAYER_OVERLAY_ENTRIES = 2

double_cache_prevention = threading.Lock()

class Rom(BigStream):
    original = None

    def __init__(self, file=None, force_use=False):
        super().__init__([])

        self.changed_address = {}
        self.changed_dma = {}
        self.force_patch = []
        self.dma = DMAIterator(self, DMADATA_START)

        if file is None:
            return

        decomp_file = user_path('ZOOTDEC.z64')

        with open(data_path('generated/symbols.json'), 'r') as stream:
            raw_symbols = json.load(stream)
        self.symbols = {}
        for name, entry in raw_symbols.items():
            if isinstance(entry, dict):
                self.symbols[name] = {'address': int(entry['address'], 16), 'length': entry.get('length', 1)}
            else:
                self.symbols[name] = {'address': int(entry, 16), 'length': 1}

        with open(data_path('generated/patch_symbols.json'), 'r') as stream:
            self.patch_symbols = json.load(stream)

        # If decompressed file already exists, read from it
        if not force_use:
            if os.path.exists(decomp_file):
                file = decomp_file

            if file == '':
                # if not specified, try to read from the previously decompressed rom
                file = decomp_file
                try:
                    self.read_rom(file)
                except FileNotFoundError:
                    # could not find the decompressed rom either
                    raise FileNotFoundError('Must specify path to base ROM')
            else:
                self.read_rom(file)
        else:
            self.read_rom(file)

        # decompress rom, or check if it's already decompressed
        self.decompress_rom_file(file, decomp_file, force_use)

        # Add file to maximum size
        self.buffer.extend(bytearray([0x00] * (0x4000000 - len(self.buffer))))
        with double_cache_prevention:
            if not self.original:
                Rom.original = self.copy()
        self.overlay_table = OverlayTable.read_overlay_table(
            self, OVERLAY_TABLE_START, OVERLAY_TABLE_OFFSET, OVERLAY_TABLE_ENTRY_SIZE, NUM_OVERLAY_ENTRIES
        ) + OverlayTable.read_overlay_table(
            self, PAUSE_PLAYER_OVERLAY_TABLE_START, PAUSE_PLAYER_OVERLAY_TABLE_OFFSET,
            PAUSE_PLAYER_OVERLAY_TABLE_ENTRY_SIZE, NUM_PAUSE_PLAYER_OVERLAY_ENTRIES
        )

        # Add version number to header.
        self.write_bytes(0x35, get_version_bytes(__version__))
        self.force_patch.extend([0x35, 0x36, 0x37])

    def copy(self):
        new_rom = Rom()
        new_rom.buffer = copy.copy(self.buffer)
        new_rom.changed_address = copy.copy(self.changed_address)
        new_rom.changed_dma = copy.copy(self.changed_dma)
        new_rom.force_patch = copy.copy(self.force_patch)
        new_rom.dma = DMAIterator(new_rom, DMADATA_START)
        return new_rom

    def decompress_rom_file(self, file, decomp_file, skip_crc_check):
        validCRC = [
            [0xEC, 0x70, 0x11, 0xB7, 0x76, 0x16, 0xD7, 0x2B],  # Compressed
            [0x70, 0xEC, 0xB7, 0x11, 0x16, 0x76, 0x2B, 0xD7],  # Byteswap compressed
            [0x93, 0x52, 0x2E, 0x7B, 0xE5, 0x06, 0xD4, 0x27],  # Decompressed
        ]

        # Validate ROM file
        file_name = os.path.splitext(file)
        romCRC = list(self.buffer[0x10:0x18])
        if romCRC not in validCRC and not skip_crc_check:
            # Bad CRC validation
            raise RuntimeError('ROM file %s is not a valid OoT 1.0 NTSC-U/J ROM.' % file)
        elif len(self.buffer) < 0x2000000 or len(self.buffer) > (0x4000000) or file_name[1].lower() not in ['.z64',
                                                                                                            '.n64']:
            # ROM is too big, or too small, or not a bad type
            raise RuntimeError('ROM file %s is not a valid OoT 1.0 NTSC-U/J ROM.' % file)
        elif len(self.buffer) == 0x2000000:
            # If Input ROM is compressed, then Decompress it

            sub_dir = data_path("Decompress")

            if platform.system() == 'Windows':
                subcall = [sub_dir + "\\Decompress.exe", file, decomp_file]
            elif platform.system() == 'Linux':
                if platform.uname()[4] == 'aarch64' or platform.uname()[4] == 'arm64':
                    subcall = [sub_dir + "/Decompress_ARM64", file, decomp_file]
                else:
                    subcall = [sub_dir + "/Decompress", file, decomp_file]
            elif platform.system() == 'Darwin':
                subcall = [sub_dir + "/Decompress.out", file, decomp_file]
            else:
                raise RuntimeError(
                    'Unsupported operating system for decompression. Please supply an already decompressed ROM.')

            if not os.path.exists(subcall[0]):
                raise RuntimeError(f'Decompressor does not exist! Please place it at {subcall[0]}.')
            subprocess.check_call(subcall, **subprocess_args())
            self.read_rom(decomp_file)
        else:
            # ROM file is a valid and already uncompressed
            pass

    def write_byte(self, address, value):
        super().write_byte(address, value)
        self.changed_address[self.last_address - 1] = value

    def write_bytes(self, address, values):
        super().write_bytes(address, values)
        self.changed_address.update(zip(range(address, address + len(values)), values))

    def revert_patch(self, patch_name):
        patch_start_symbol = patch_name + "_START"
        patch_end_symbol = patch_name + "_END"
        if patch_start_symbol not in self.patch_symbols or patch_end_symbol not in self.patch_symbols:
            return
        patch_start = OverlayTable.VRAM_2_VROM(self.overlay_table, self.patch_symbols[patch_start_symbol])
        patch_end = OverlayTable.VRAM_2_VROM(self.overlay_table, self.patch_symbols[patch_end_symbol])
        original_bytes = self.original.read_bytes(patch_start, patch_end - patch_start)
        self.write_bytes(patch_start, original_bytes)

    def restore(self):
        self.buffer = copy.copy(self.original.buffer)
        self.changed_address = {}
        self.changed_dma = {}
        self.force_patch = []
        self.last_address = None
        self.write_bytes(0x35, get_version_bytes(__version__))
        self.force_patch.extend([0x35, 0x36, 0x37])

    def sym(self, symbol_name):
        entry = self.symbols.get(symbol_name)
        return entry['address'] if entry else None

    def sym_length(self, symbol_name):
        entry = self.symbols.get(symbol_name)
        return entry['length'] if entry else 0

    def write_to_file(self, file):
        self.verify_dmadata()
        self.update_header()
        with open(file, 'wb') as outfile:
            outfile.write(self.buffer)

    def update_header(self):
        crc = calculate_crc(self)
        self.write_bytes(0x10, crc)

    def read_rom(self, file):
        # "Reads rom into bytearray"
        try:
            with open(file, 'rb') as stream:
                self.buffer = bytearray(stream.read())
        except FileNotFoundError as ex:
            raise FileNotFoundError('Invalid path to Base ROM: "' + file + '"')

    # dmadata/file management helper functions

    def _get_dmadata_record(self, cur):
        start = self.read_int32(cur)
        end = self.read_int32(cur + 0x04)
        size = end - start
        return start, end, size

    def get_dmadata_record_by_key(self, key):
        cur = DMADATA_START
        dma_start, dma_end, dma_size = self._get_dmadata_record(cur)
        while True:
            if dma_start == 0 and dma_end == 0:
                return None
            if dma_start == key:
                return dma_start, dma_end, dma_size
            cur += 0x10
            dma_start, dma_end, dma_size = self._get_dmadata_record(cur)

    def verify_dmadata(self):
        overlapping_records = []
        dma_data = []

        for dma_entry in self.dma:
            this_start, this_end, this_size = dma_entry.as_tuple()

            if this_start == 0 and this_end == 0:
                break

            dma_data.append((this_start, this_end, this_size))

        dma_data.sort(key=lambda v: v[0])

        for i in range(0, len(dma_data) - 1):
            this_start, this_end, this_size = dma_data[i]
            next_start, next_end, next_size = dma_data[i + 1]

            if this_end > next_start:
                overlapping_records.append(
                    '0x%08X - 0x%08X (Size: 0x%04X)\n0x%08X - 0x%08X (Size: 0x%04X)' % \
                    (this_start, this_end, this_size, next_start, next_end, next_size)
                )

        if len(overlapping_records) > 0:
            raise Exception("Overlapping DMA Data Records!\n%s" % \
                            '\n-------------------------------------\n'.join(overlapping_records))

    # update dmadata record with start vrom address "key"
    # if key is not found, then attempt to add a new dmadata entry
    def update_dmadata_record(self, key, start, end, from_file=None):
        dma_entry = self.dma.get_dmadata_record_by_key(key)
        if from_file == None:
            from_file = -1 if key == None else key
        dma_entry.update(start, end, from_file)

    def extend_dmadata(self, extra_entries):
        _, dma_data_end = self.get_dma_table_range()
        self.write_int32(DMADATA_START + 0x04, dma_data_end + extra_entries * 0x10)
        self.dma._dma_entries = 0

    def get_dma_table_range(self):
        cur = DMADATA_START
        dma_start, dma_end, dma_size = self._get_dmadata_record(cur)
        while True:
            if dma_start == 0 and dma_end == 0:
                raise Exception('Bad DMA Table: DMA Table entry missing.')

            if dma_start == DMADATA_START:
                return (DMADATA_START, dma_end)

            cur += 0x10
            dma_start, dma_end, dma_size = self._get_dmadata_record(cur)

    # This will scan for any changes that have been made to the DMA table
    # This assumes any changes here are new files, so this should only be called
    # after patching in the new files, but before vanilla files are repointed
    def scan_dmadata_update(self, preserve_from_file=False, assume_move=False):
        for dma_entry in self.dma:
            dma_start, dma_end, dma_size = dma_entry.as_tuple()
            old_dma_start, old_dma_end, old_dma_size = self.original.dma[dma_entry.index].as_tuple()
            if (dma_start == 0 and dma_end == 0) and \
                    (old_dma_start == 0 and old_dma_end == 0):
                break

            # If the entries do not match, the flag the changed entry
            if not (dma_start == old_dma_start and dma_end == old_dma_end):
                from_file = -1
                if preserve_from_file and dma_entry.index in self.changed_dma:
                    from_file = self.changed_dma[dma_entry.index][0]
                elif assume_move and dma_entry.index < 1496:
                    from_file = old_dma_start
                self.changed_dma[dma_entry.index] = (from_file, dma_start, dma_end - dma_start)

    # gets the last used byte of rom defined in the DMA table
    def free_space(self, size=None):
        return self.dma.free_space(size)


class DMAEntry:
    def __init__(self, rom, index):
        self.rom = rom
        self.index = index
        if self.index < 0 or self.index > self.rom.dma.dma_entries:
            raise ValueError(f"DMAEntry: Index out of range: {self.index}")

    @property
    def start(self):
        return self.rom.read_int32(self.rom.dma.dma_start + (self.index * 0x10))

    @property
    def end(self):
        return self.rom.read_int32(self.rom.dma.dma_start + (self.index * 0x10) + 0x04)

    @property
    def size(self):
        return self.end - self.start

    def as_tuple(self):
        start, end = self.start, self.end
        return start, end, end - start

    def file_bytes(self):
        start, end, size = self.as_tuple()
        return self.rom.read_bytes(start, size)

    def update(self, start, end, from_file=None):
        if from_file is None:
            if self.index in self.rom.changed_dma:
                from_file = self.rom.changed_dma[self.index][0]
            elif self.start and self.end:
                from_file = self.start
            else:
                from_file = -1
        self.rom.write_int32s(self.rom.dma.dma_start + (self.index * 0x10), [start, end, start, 0])
        self.rom.changed_dma[self.index] = (from_file, start, end - start)


class DMAIterator:
    def __init__(self, rom, dma_start):
        self.rom = rom
        self.dma_start = dma_start
        self.dma_index = 0
        self.dma_end = 0
        self._dma_entries = 0

    @property
    def dma_entries(self):
        if not self._dma_entries:
            self._calculate_dma_entries()
        return self._dma_entries

    def _calculate_dma_entries(self):
        i = start = -1
        while start != self.dma_start:
            i += 1
            if i > 2000:
                dma_bytes = self.rom.read_bytes(self.rom.dma.dma_start, 160).hex(' ', 4)
                raise Exception(f"DMA entry for DMA table not found. Attempted to find DMA entry starting at {self.dma_start}. First 160 bytes of DMA table: {dma_bytes}")
            start = self.rom.read_int32(self.rom.dma.dma_start + (i * 0x10))
        self.dma_index = i
        self.dma_end = self.rom.read_int32(self.dma_start + (self.dma_index * 0x10) + 0x04)
        self._dma_entries = (self.dma_end - self.dma_start) >> 4

    def __getitem__(self, item):
        if not isinstance(item, int):
            raise ValueError("DMAIterator only supports integer keys.")
        if item < 0:
            item = self.dma_entries + item
        if item > self.dma_entries:
            raise ValueError(f"Attempted to get DMA entry exceeding the table size: {item}")

        return DMAEntry(self.rom, item)

    def __iter__(self):
        for item in range(0, self.dma_entries):
            yield self[item]

    def get_dmadata_record_by_key(self, key):
        for dma_entry in self:
            if key is None and dma_entry.end == 0 and dma_entry.start == 0:
                return dma_entry
            elif dma_entry.start == key:
                return dma_entry
        raise Exception(f"`get_dmadata_record_by_key`: DMA Start '{key}' not found in the DMA Table.")

    # Gets the last used byte of rom defined in the DMA table.
    def end_of_data(self):
        max_end = 0
        for dma_entry in self:
            max_end = max(max_end, dma_entry.end)

        max_end = ((max_end + 0x0F) >> 4) << 4
        return max_end

    # Finds the smallest suitable place between current files. If size is None, find the largest span of free space.
    def free_space(self, size=None):
        free_space = []

        files = sorted([dma_entry.as_tuple() for dma_entry in self])
        for i in range(len(files)):
            end_current = ((files[i][1] + 0x0F) >> 4) << 4
            start_next = ((files[i + 1][0] + 0x0F) >> 4) << 4 if i + 1 < len(files) else len(self.rom.buffer)
            if end_current < start_next:
                free_space.append((start_next - end_current, end_current))

        free_space.sort()
        if not free_space:
            raise Exception(f"No free space in ROM. This should never happen. DMA entries: {self.dma_entries}")

        if size is None:
            return free_space[-1][1]

        try:
            return next(filter(lambda f: f[0] >= size, free_space))[1]
        except StopIteration:
            raise Exception(f"Not enough free space in ROM to fit a file of size {size}. Largest region of free space available: {free_space[-1][0]}.")


def compress_rom_file(input_file, output_file):
    input_file = os.path.abspath(input_file)
    output_file = os.path.abspath(output_file)
    compressor_dir = data_path("Compress")

    def _read_dmadata_entries(path):
        entries = []
        with open(path, 'rb') as stream:
            index = 0
            cur = DMADATA_START
            while True:
                stream.seek(cur)
                data = stream.read(0x10)
                if len(data) < 0x10:
                    break
                start, end, pstart, pend = struct.unpack('>IIII', data)
                if start == 0 and end == 0:
                    break
                entries.append((index, start, end, pstart, pend))
                cur += 0x10
                index += 1
        return entries

    def _read_extended_object_indices(path):
        with open(data_path('generated/symbols.json'), 'r') as stream:
            symbols = json.load(stream)
        ext_symbol = symbols.get('EXTENDED_OBJECT_TABLE')
        if ext_symbol is None:
            return []
        if isinstance(ext_symbol, dict):
            ext_addr = int(ext_symbol['address'], 16)
            ext_len = ext_symbol.get('length', 0)
        else:
            ext_addr = int(ext_symbol, 16)
            ext_len = 0
        if ext_len <= 0 or ext_len % 8 != 0:
            return []

        dmadata = _read_dmadata_entries(path)
        if not dmadata:
            return []

        indices = set()
        with open(path, 'rb') as stream:
            stream.seek(ext_addr)
            table = stream.read(ext_len)
        if len(table) < ext_len:
            return []

        for off in range(0, ext_len, 8):
            obj_start, obj_end = struct.unpack_from('>II', table, off)
            if obj_start == 0 and obj_end == 0:
                continue
            for dma_index, dma_start, dma_end, _pstart, _pend in dmadata:
                if dma_start <= obj_start < dma_end:
                    indices.add(dma_index)
                    break
        return sorted(indices)

    dma_table_backup = None
    dma_table_path = os.path.join(compressor_dir, 'dmaTable.dat')
    try:
        extended_dma_indices = _read_extended_object_indices(input_file)
    except Exception:
        extended_dma_indices = []

    if extended_dma_indices and os.path.exists(dma_table_path):
        with open(dma_table_path, 'r', encoding='utf-8') as stream:
            dma_table_backup = stream.read()

        try:
            current_values = [int(tok) for tok in dma_table_backup.split()]
        except ValueError:
            current_values = []

        changed = False
        for dma_index in extended_dma_indices:
            # Positive entries in dmaTable.dat are left uncompressed by Compress.
            if dma_index not in current_values and -dma_index not in current_values:
                current_values.append(dma_index)
                changed = True

        if changed:
            with open(dma_table_path, 'w', encoding='utf-8') as stream:
                stream.write(' '.join(str(v) for v in current_values) + '\n')

    if platform.system() == 'Windows':
        executable_path = "Compress.exe"
    elif platform.system() == 'Linux':
        if platform.uname()[4] == 'aarch64' or platform.uname()[4] == 'arm64':
            executable_path = "Compress_ARM64"
        else:
            executable_path = "Compress"
    elif platform.system() == 'Darwin':
        executable_path = "Compress.out"
    else:
        raise RuntimeError('Unsupported operating system for compression.')
    compressor_path = os.path.join(compressor_dir, executable_path)
    if not os.path.exists(compressor_path):
        raise RuntimeError(f'Compressor does not exist! Please place it at {compressor_path}.')
    import logging
    try:
        logging.info(subprocess.check_output([compressor_path, input_file, output_file],
                                             cwd=compressor_dir,
                                             **subprocess_args(include_stdout=False)))
    finally:
        if dma_table_backup is not None:
            with open(dma_table_path, 'w', encoding='utf-8') as stream:
                stream.write(dma_table_backup)


class OverlayEntry:
    def __init__(self, vrom_start, vrom_end, vram_start, vram_end):
        self.vrom_start = vrom_start
        self.vrom_end = vrom_end
        self.vram_start = vram_start
        self.vram_end = vram_end


class OverlayTable:
    @staticmethod
    def read_overlay_table(rom, ovl_table_start, offset, entry_size, num_entries):
        overlay_entries = []
        for i in range(0, num_entries):
            entry_bytes = rom.read_bytes(ovl_table_start + i * entry_size, entry_size)
            vrom_start = int.from_bytes(entry_bytes[offset + 0:offset + 4], 'big')
            vrom_end = int.from_bytes(entry_bytes[offset + 4:offset + 8], 'big')
            vram_start = int.from_bytes(entry_bytes[offset + 8:offset + 12], 'big')
            vram_end = int.from_bytes(entry_bytes[offset + 12:offset + 16], 'big')
            overlay_entries.append(OverlayEntry(vrom_start, vrom_end, vram_start, vram_end))
        return overlay_entries

    @staticmethod
    def VRAM_2_VROM(overlay_entries, vram_address):
        for overlay_entry in overlay_entries:
            if overlay_entry.vram_start <= vram_address < overlay_entry.vram_end:
                return vram_address - overlay_entry.vram_start + overlay_entry.vrom_start
        raise Exception("Overlay address not found in table")
