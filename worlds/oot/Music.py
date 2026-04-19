# Much of this is heavily inspired from and/or based on az64's / Deathbasket's MM randomizer
from __future__ import annotations
import os
import zipfile
from typing import Optional

from .Sequence import Sequence, SequenceGame
from .Utils import data_path
from .MusicHelpers import process_sequence_ootrs, process_sequence_mmr_zseq, process_sequence_mmrs

# DMA table byte offset for the audioseq file (entry index 4, DMADATA_START 0x7430 + 4*0x10)
AUDIOSEQ_DMADATA_OFFSET = 0x7470

# Format: (Title, Sequence ID)
bgm_sequence_ids: tuple[tuple[str, int], ...] = (
    ("Hyrule Field", 0x02),
    ("Dodongos Cavern", 0x18),
    ("Kakariko Adult", 0x19),
    ("Battle", 0x1A),
    ("Boss Battle", 0x1B),
    ("Inside Deku Tree", 0x1C),
    ("Market", 0x1D),
    ("Title Theme", 0x1E),
    ("House", 0x1F),
    ("Jabu Jabu", 0x26),
    ("Kakariko Child", 0x27),
    ("Fairy Fountain", 0x28),
    ("Zelda Theme", 0x29),
    ("Fire Temple", 0x2A),
    ("Forest Temple", 0x2C),
    ("Castle Courtyard", 0x2D),
    ("Ganondorf Theme", 0x2E),
    ("Lon Lon Ranch", 0x2F),
    ("Goron City", 0x30),
    ("Miniboss Battle", 0x38),
    ("Temple of Time", 0x3A),
    ("Kokiri Forest", 0x3C),
    ("Lost Woods", 0x3E),
    ("Spirit Temple", 0x3F),
    ("Horse Race", 0x40),
    ("Ingo Theme", 0x42),
    ("Fairy Flying", 0x4A),
    ("Deku Tree", 0x4B),
    ("Windmill Hut", 0x4C),
    ("Shooting Gallery", 0x4E),
    ("Sheik Theme", 0x4F),
    ("Zoras Domain", 0x50),
    ("Shop", 0x55),
    ("Chamber of the Sages", 0x56),
    ("Ice Cavern", 0x58),
    ("Kaepora Gaebora", 0x5A),
    ("Shadow Temple", 0x5B),
    ("Water Temple", 0x5C),
    ("Gerudo Valley", 0x5F),
    ("Potion Shop", 0x60),
    ("Kotake and Koume", 0x61),
    ("Castle Escape", 0x62),
    ("Castle Underground", 0x63),
    ("Ganondorf Battle", 0x64),
    ("Ganon Battle", 0x65),
    ("Fire Boss", 0x6B),
    ("Mini-game", 0x6C),
)

fanfare_sequence_ids: tuple[tuple[str, int], ...] = (
    ("Game Over", 0x20),
    ("Boss Defeated", 0x21),
    ("Item Get", 0x22),
    ("Ganondorf Appears", 0x23),
    ("Heart Container Get", 0x24),
    ("Treasure Chest", 0x2B),
    ("Spirit Stone Get", 0x32),
    ("Heart Piece Get", 0x39),
    ("Escape from Ranch", 0x3B),
    ("Learn Song", 0x3D),
    ("Epona Race Goal", 0x41),
    ("Medallion Get", 0x43),
    ("Zelda Turns Around", 0x51),
    ("Master Sword", 0x53),
    ("Door of Time", 0x59),
    ("Ganons Rainbow Bridge", 0x5D),
)

ocarina_sequence_ids: tuple[tuple[str, int], ...] = (
    ("Prelude of Light", 0x25),
    ("Bolero of Fire", 0x33),
    ("Minuet of Forest", 0x34),
    ("Serenade of Water", 0x35),
    ("Requiem of Spirit", 0x36),
    ("Nocturne of Shadow", 0x37),
    ("Saria's Song", 0x44),
    ("Epona's Song", 0x45),
    ("Zelda's Lullaby", 0x46),
    ("Sun's Song", 0x47),
    ("Song of Time", 0x48),
    ("Song of Storms", 0x49),
)

credit_sequence_ids: tuple[tuple[str, int], ...] = (
    ("Zeldas Theme Orchestra", 0x52),
    ("Zeldas Ocarina Song", 0x66),
    ("Ending Credits Part 1", 0x67),
    ("Ending Credits Part 2", 0x68),
    ("Ending Credits Part 3", 0x69),
    ("Ending Credits Part 4", 0x6A),
)

fileselect_sequence_id: tuple[tuple[str, int], ...] = (
    ("File Select", 0x57),
)


# Holds raw ROM sequence data (address, size, data bytes) for rebuild_sequences
class SequenceData:
    def __init__(self) -> None:
        self.address: int = -1
        self.size: int = -1
        self.data: bytearray = bytearray()


def process_sequences(rom, ids, seq_type: str = 'bgm',
                      disabled_source_sequences: Optional[list] = None,
                      disabled_target_sequences: Optional[dict] = None,
                      sequences: Optional[dict] = None,
                      target_sequences: Optional[dict] = None,
                      errors: Optional[list] = None,
                      music_dir: Optional[str] = None) -> tuple[dict, dict]:
    disabled_source_sequences = [] if disabled_source_sequences is None else disabled_source_sequences
    disabled_target_sequences = {} if disabled_target_sequences is None else disabled_target_sequences
    sequences = {} if sequences is None else sequences
    target_sequences = {} if target_sequences is None else target_sequences
    if errors is None:
        errors = []

    # Process vanilla music data
    for bgm in ids:
        name = bgm[0]
        cosmetic_name = name
        seq_type_val = rom.read_int16(0xB89AE8 + (bgm[1] * 0x10))
        instrument_set = rom.read_byte(0xB89911 + 0xDD + (bgm[1] * 2))
        id = bgm[1]

        seq = Sequence(name, cosmetic_name, seq_type, seq_type_val, instrument_set, vanilla_id=id)
        target = Sequence(name, cosmetic_name, seq_type, seq_type_val, instrument_set, replaces=id)

        if seq.vanilla_id != 0x57 and cosmetic_name not in disabled_source_sequences:
            sequences[seq.cosmetic_name] = seq
        if cosmetic_name not in disabled_target_sequences:
            target_sequences[target.cosmetic_name] = target

    # If present, load the file containing custom music to exclude
    try:
        with open(os.path.join(data_path(), 'custom_music_exclusion.txt')) as excl_in:
            seq_exclusion_list = excl_in.readlines()
        seq_exclusion_list = [s.rstrip() for s in seq_exclusion_list if s[0] != '#']
        seq_exclusion_list = [s for s in seq_exclusion_list if s.endswith('.ootrs')]
    except FileNotFoundError:
        seq_exclusion_list = []

    # Process custom music files (.ootrs, .zseq, .mmrs) from built-in Music folder
    scan_dirs = [os.path.join(data_path(), 'Music')]
    if music_dir and os.path.isdir(music_dir):
        scan_dirs.append(music_dir)

    for scan_dir in scan_dirs:
        for dirpath, _, filenames in os.walk(scan_dir, followlinks=True):
            for fname in filenames:
                if fname in seq_exclusion_list:
                    continue
                filepath = os.path.join(dirpath, fname)
                seq = None
                try:
                    if fname.lower().endswith('.ootrs'):
                        seq = process_sequence_ootrs(filepath, fname, seq_type, False, {})
                    elif fname.lower().endswith('.zseq'):
                        seq = process_sequence_mmr_zseq(filepath, fname, seq_type, False, {})
                    elif fname.lower().endswith('.mmrs'):
                        seq = process_sequence_mmrs(filepath, fname, seq_type, False, {})
                    if seq and seq.cosmetic_name not in disabled_source_sequences:
                        sequences[seq.cosmetic_name] = seq
                except Exception as e:
                    errors.append(f"Error processing custom sequence {fname} - {e}")

    return sequences, target_sequences


def shuffle_music(source_sequences: dict, target_sequences: dict, music_mapping: dict,
                  log: dict, rand, errors: list) -> list:
    sequences = []
    sequence_ids = [name for name in source_sequences if name not in music_mapping.values()]
    rand.shuffle(sequence_ids)

    refill_needed = False
    for name, target in target_sequences.items():
        if target.cosmetic_name not in music_mapping:
            if not sequence_ids:
                refill_needed = True
                sequence_ids = list(source_sequences.keys())
                rand.shuffle(sequence_ids)
            sequence = source_sequences[sequence_ids.pop()].copy()
        elif music_mapping[target.cosmetic_name] in source_sequences:
            sequence = source_sequences[music_mapping[target.cosmetic_name]].copy()
        else:
            errors.append(f"Sequence '{music_mapping[target.cosmetic_name]}' mapped to '{target.cosmetic_name}' was not found.")
            if sequence_ids:
                sequence = source_sequences[sequence_ids.pop()].copy()
            else:
                continue
        sequences.append(sequence)
        sequence.replaces = target.replaces
        log[target.cosmetic_name] = sequence.cosmetic_name

    if refill_needed:
        errors.append("Not enough music available to avoid repeats. Some tracks may be duplicated.")
    return sequences


def rebuild_sequences(rom, sequences: list) -> None:
    audioseq_start, audioseq_end, audioseq_size = rom._get_dmadata_record(AUDIOSEQ_DMADATA_OFFSET)

    replacement_dict = {seq.replaces: seq for seq in sequences}

    bgmlist = [seq_id for _, seq_id in bgm_sequence_ids]
    fanfarelist = [seq_id for _, seq_id in fanfare_sequence_ids]
    ocarinalist = [seq_id for _, seq_id in ocarina_sequence_ids]
    creditlist = [seq_id for _, seq_id in credit_sequence_ids]
    fileselectlist = [seq_id for _, seq_id in fileselect_sequence_id]

    # Read all vanilla sequence data from ROM
    old_sequences: list[SequenceData] = []
    for i in range(0x6E):
        entry = SequenceData()
        entry_address = 0xB89AE0 + (i * 0x10)
        entry.address = rom.read_int32(entry_address)
        entry.size = rom.read_int32(entry_address + 0x04)

        if entry.size > 0:
            entry.data = rom.read_bytes(entry.address + audioseq_start, entry.size)
        else:
            seq = replacement_dict.get(i, None)
            if seq and 0 < entry.address < 128:
                if seq.replaces != 0x28:
                    seq.replaces = entry.address
                else:
                    entry.data = old_sequences[0x57].data
                    entry.size = old_sequences[0x57].size

        old_sequences.append(entry)

    # Build new sequence data
    new_sequences: list[SequenceData] = []
    address = 0
    new_audio_sequence: list = []

    for i in range(0x6E):
        new_entry = SequenceData()
        if old_sequences[i].size == 0:
            new_entry.address = old_sequences[i].address
        else:
            new_entry.address = address

        seq = replacement_dict.get(i, None)
        if seq:
            if seq.vanilla_id != -1:
                new_entry.size = old_sequences[seq.vanilla_id].size
                new_entry.data = bytearray(old_sequences[seq.vanilla_id].data)
            else:
                try:
                    if seq.name.endswith('.zseq'):
                        with open(seq.name, 'rb') as stream:
                            new_entry.data = bytearray(stream.read())
                            new_entry.size = len(new_entry.data)
                    else:
                        with zipfile.ZipFile(seq.name) as zip:
                            with zip.open(seq.seq_file, 'r') as stream:
                                new_entry.data = bytearray(stream.read())
                                new_entry.size = len(new_entry.data)
                    if new_entry.size % 0x10 != 0:
                        new_entry.data.extend(bytearray(0x10 - (new_entry.size % 0x10)))
                        new_entry.size += 0x10 - (new_entry.size % 0x10)
                    if new_entry.size <= 0x10:
                        raise Exception(f'Invalid sequence file "{seq.name}"')
                    new_entry.data[1] = 0x20
                except FileNotFoundError:
                    raise FileNotFoundError(f'No sequence file for: "{seq.name}"')
        else:
            new_entry.size = old_sequences[i].size
            new_entry.data = bytearray(old_sequences[i].data)

        # Deduplication: if this data was already added, reuse that address
        for existing in new_sequences:
            if new_entry.size == existing.size and new_entry.data == existing.data and new_entry.size > 0:
                new_entry.address = existing.address
                new_entry.data = bytearray()
                break

        new_sequences.append(new_entry)

        if new_entry.data and new_entry.size > 0:
            if new_entry.size % 0x10 != 0:
                new_entry.data.extend(bytearray(0x10 - (new_entry.size % 0x10)))
                new_entry.size += 0x10 - (new_entry.size % 0x10)
            new_audio_sequence.extend(new_entry.data)
            address += new_entry.size

    if address > audioseq_size:
        rom.buffer[audioseq_start:audioseq_end] = [0] * audioseq_size
        new_address = rom.free_space()
        rom.write_bytes(new_address, new_audio_sequence)
        rom.update_dmadata_record(audioseq_start, new_address, new_address + address)
    else:
        rom.write_bytes(audioseq_start, new_audio_sequence)

    # Update pointer table
    for i in range(0x6E):
        rom.write_int32(0xB89AE0 + (i * 0x10), new_sequences[i].address)
        rom.write_int32(0xB89AE0 + (i * 0x10) + 0x04, new_sequences[i].size)

    # Update instrument sets by category
    for i in bgmlist:
        base = 0xB89911 + 0xDD + (i * 2)
        j = replacement_dict.get(i if new_sequences[i].size else new_sequences[i].address, None)
        if j:
            rom.write_byte(base, j.instrument_set)
    for i in fanfarelist:
        base = 0xB89911 + 0xDD + (i * 2)
        j = replacement_dict.get(i if new_sequences[i].size else new_sequences[i].address, None)
        if j:
            rom.write_byte(base, j.instrument_set)
    for i in ocarinalist:
        base = 0xB89911 + 0xDD + (i * 2)
        j = replacement_dict.get(i if new_sequences[i].size else new_sequences[i].address, None)
        if j:
            rom.write_byte(base, j.instrument_set)
    for i in creditlist:
        base = 0xB89911 + 0xDD + (i * 2)
        j = replacement_dict.get(i if new_sequences[i].size else new_sequences[i].address, None)
        if j:
            rom.write_byte(base, j.instrument_set)
    for i in fileselectlist:
        base = 0xB89911 + 0xDD + (i * 2)
        j = replacement_dict.get(i if new_sequences[i].size else new_sequences[i].address, None)
        if j:
            rom.write_byte(base, j.instrument_set)


def rebuild_pointers_table(rom, sequences: list) -> None:
    for sequence in [s for s in sequences if s.vanilla_id != -1 and s.replaces != -1]:
        bgm_sequence = rom.original.read_bytes(0xB89AE0 + (sequence.vanilla_id * 0x10), 0x10)
        bgm_instrument = rom.original.read_int16(0xB89910 + 0xDD + (sequence.vanilla_id * 2))
        rom.write_bytes(0xB89AE0 + (sequence.replaces * 0x10), bgm_sequence)
        rom.write_int16(0xB89910 + 0xDD + (sequence.replaces * 2), bgm_instrument)

    # Write Fairy Fountain instrument to File Select
    rom.write_int16(0xB89910 + 0xDD + (0x57 * 2), rom.read_int16(0xB89910 + 0xDD + (0x28 * 2)))


def randomize_music(rom, ootworld, music_mapping: dict, symbols: Optional[dict] = None, music_dir: Optional[str] = None) -> tuple[dict, list]:
    log: dict = {}
    errors: list = []
    sequences: dict = {}
    target_sequences: dict = {}
    fanfare_sequences: dict = {}
    target_fanfare_sequences: dict = {}
    disabled_source_sequences: list = []
    disabled_target_sequences: dict = {}

    music_mapping = music_mapping.copy()
    bgm_ids = {bgm[0]: bgm for bgm in bgm_sequence_ids}
    ff_ids = {ff[0]: ff for ff in fanfare_sequence_ids}
    ocarina_ids = {bgm[0]: bgm for bgm in ocarina_sequence_ids}

    if getattr(ootworld, 'credits_music', False) and ootworld.background_music == 'randomized':
        bgm_ids.update({bgm[0]: bgm for bgm in credit_sequence_ids})

    # Check if we have mapped music for BGM or Fanfares
    bgm_mapped = any(name in music_mapping for name in bgm_ids)
    ff_mapped = any(name in music_mapping for name in ff_ids)
    ocarina_mapped = any(name in music_mapping for name in ocarina_ids)

    # Flag sequence locations that are set to off for disabling
    disabled_ids = []
    if ootworld.background_music == 'off':
        disabled_ids += list(bgm_ids.values())
    if ootworld.fanfares == 'off':
        disabled_ids += list(ff_ids.values())
        if ootworld.ocarina_fanfares:
            disabled_ids += list(ocarina_ids.values())
    for bgm in list(bgm_ids.values()) + list(ff_ids.values()) + list(ocarina_ids.values()):
        if music_mapping.get(bgm[0], '') == "None":
            disabled_target_sequences[bgm[0]] = bgm
            music_mapping.pop(bgm[0], None)
    for bgm in disabled_ids:
        if bgm[0] not in music_mapping:
            disabled_target_sequences[bgm[0]] = bgm

    # Map music to itself if music is set to normal
    normal_ids = []
    if ootworld.background_music == 'normal' and bgm_mapped:
        normal_ids += list(bgm_ids.values())
    if ootworld.fanfares == 'normal' and (ff_mapped or ocarina_mapped):
        normal_ids += list(ff_ids.values())
    if ootworld.fanfares == 'normal' and ocarina_mapped:
        normal_ids += list(ocarina_ids.values())
    for bgm in normal_ids:
        if bgm[0] not in music_mapping:
            music_mapping[bgm[0]] = bgm[0]

    # Include ocarina songs in fanfare pool if checked
    if ootworld.ocarina_fanfares or ocarina_mapped:
        ff_ids.update(ocarina_ids)

    # Process and shuffle BGM
    if ootworld.background_music == 'randomized' or bgm_mapped:
        sequences, target_sequences = process_sequences(
            rom, bgm_ids.values(), 'bgm', disabled_source_sequences, disabled_target_sequences, errors=errors,
            music_dir=music_dir)

    # Process and shuffle fanfares
    if ootworld.fanfares == 'randomized' or ff_mapped or ocarina_mapped:
        fanfare_sequences, target_fanfare_sequences = process_sequences(
            rom, ff_ids.values(), 'fanfare', disabled_source_sequences, disabled_target_sequences, errors=errors,
            music_dir=music_dir)

    shuffled_sequences = []
    shuffled_fanfare_sequences = []

    if sequences and target_sequences:
        shuffled_sequences = shuffle_music(sequences, target_sequences, music_mapping, log, ootworld.random, errors)
    if fanfare_sequences and target_fanfare_sequences:
        shuffled_fanfare_sequences = shuffle_music(fanfare_sequences, target_fanfare_sequences, music_mapping, log, ootworld.random, errors)

    # Mark disabled sequences in log
    for name in disabled_target_sequences:
        log[name] = "None"

    # Patch the ROM
    all_sequences = shuffled_sequences + shuffled_fanfare_sequences
    if all_sequences:
        rebuild_sequences(rom, all_sequences)

    if disabled_target_sequences:
        disable_music(rom, disabled_target_sequences.values(), log)

    return log, errors


def disable_music(rom, ids, log: dict) -> None:
    blank_track = rom.read_bytes(0xB89AE0 + (0 * 0x10), 0x10)
    for bgm in ids:
        rom.write_bytes(0xB89AE0 + (bgm[1] * 0x10), blank_track)
        log[bgm[0]] = "None"


def restore_music(rom) -> None:
    for bgm in bgm_sequence_ids + fanfare_sequence_ids + ocarina_sequence_ids:
        bgm_sequence = rom.original.read_bytes(0xB89AE0 + (bgm[1] * 0x10), 0x10)
        rom.write_bytes(0xB89AE0 + (bgm[1] * 0x10), bgm_sequence)
        bgm_instrument = rom.original.read_int16(0xB89910 + 0xDD + (bgm[1] * 2))
        rom.write_int16(0xB89910 + 0xDD + (bgm[1] * 2), bgm_instrument)

    # Restore file select instrument
    bgm_instrument = rom.original.read_int16(0xB89910 + 0xDD + (0x57 * 2))
    rom.write_int16(0xB89910 + 0xDD + (0x57 * 2), bgm_instrument)

    # Restore audioseq DMA entry and data
    orig_start, orig_end, orig_size = rom.original._get_dmadata_record(AUDIOSEQ_DMADATA_OFFSET)
    rom.write_bytes(orig_start, rom.original.read_bytes(orig_start, orig_size))

    start, end, size = rom._get_dmadata_record(AUDIOSEQ_DMADATA_OFFSET)
    if start != orig_start:
        rom.write_bytes(start, [0] * size)
        rom.update_dmadata_record(start, orig_start, orig_end)
