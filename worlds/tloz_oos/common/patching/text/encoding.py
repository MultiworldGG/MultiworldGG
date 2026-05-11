import logging
import re
from collections import defaultdict
from functools import lru_cache
from typing import Any

from ..RomData import RomData
from ..Util import simple_hex
from ..z80asm.Assembler import GameboyAddress
from . import (
    char_table,
    kanji_table,
    text_addresses_limit_ages,
    text_addresses_limit_seasons,
    text_offset_1_table_address_ages,
    text_offset_1_table_address_seasons,
    text_offset_2_table_address_ages,
    text_offset_2_table_address_seasons,
    text_offset_split_index_ages,
    text_offset_split_index_seasons,
    text_table_eng_address_ages,
    text_table_eng_address_seasons,
)

control_keywords = {
    "link_name",
    "child_name",
    "w7SecretBuffer1",
    "w7SecretBuffer2",
    "num1",
    "opt",
    "stop",
    "heartpiece",
    "num2",
    "slow",
}

control_functions = {"jump", "cmd", "col", "charsfx", "speed", "pos", "wait", "sfx", "call"}

control_sequence_pattern = re.compile(
    r"""
    \\
    (jump|cmd|col|charsfx|speed|pos|wait|sfx|call)
    \(([^)]+)\) |
    \\(link_name|child_name|w7SecretBuffer1|w7SecretBuffer2|
    num1|opt|stop|heartpiece|num2|slow)
""",
    re.VERBOSE,
)
dict_pattern = re.compile(r"DICT(\d+)_([0-9a-f]+)")


def add_to_tree(tree: dict[str, list[int]], char: str, keys: list[int]):
    tree[char] = keys


def build_encoding_dict() -> dict[str, list[int]]:
    tree = {}
    for i in range(len(char_table)):
        char = char_table[i]
        if char != "🚫" and char != "∅":
            add_to_tree(tree, char, [i])

    for i in range(len(kanji_table)):
        char = kanji_table[i]
        if char != "∅":
            add_to_tree(tree, char, [0x06, i])

    add_to_tree(tree, "jump", [0x07, 0x00])
    add_to_tree(tree, "cmd", [0x08, 0x00])

    add_to_tree(tree, "⬜", [0x09, 0x00])
    add_to_tree(tree, "🟥", [0x09, 0x01])
    add_to_tree(tree, "🟧", [0x09, 0x02])
    add_to_tree(tree, "🟦", [0x09, 0x03])
    add_to_tree(tree, "🟩", [0x09, 0x04])
    add_to_tree(tree, "col", [0x09, 0x00])

    add_to_tree(tree, "link_name", [0x0A, 0x00])
    add_to_tree(tree, "child_name", [0x0A, 0x01])
    add_to_tree(tree, "w7SecretBuffer1", [0x0A, 0x02])
    add_to_tree(tree, "w7SecretBuffer2", [0x0A, 0x03])

    add_to_tree(tree, "speed", [0x0C, 0x00])
    add_to_tree(tree, "num1", [0x0C, 0x08])
    add_to_tree(tree, "opt", [0x0C, 0x10])
    add_to_tree(tree, "stop", [0x0C, 0x18])
    add_to_tree(tree, "pos", [0x0C, 0x20])
    add_to_tree(tree, "heartpiece", [0x0C, 0x28])
    add_to_tree(tree, "num2", [0x0C, 0x30])
    add_to_tree(tree, "slow", [0x0C, 0x38])

    add_to_tree(tree, "wait", [0x0D, 0x00])
    add_to_tree(tree, "sfx", [0x0E, 0x00])
    add_to_tree(tree, "call", [0x0F, 0x00])

    add_to_tree(tree, "Ⓐ", [0xB8, 0xB9])
    add_to_tree(tree, "Ⓑ", [0xBA, 0xBB])

    return tree


def next_character(text: str, index: int) -> tuple[str | tuple[str, int], int]:
    # EoL
    if index >= len(text):
        return "\0", 1

    # Normal character
    if text[index] != "\\":
        return text[index], 1

    # Command with argument
    for name in control_functions:
        if text.startswith(f"\\{name}(", index):
            start = index + len(name) + 2  # skip past '\name('
            end = start + 2
            value = text[start:end]
            return (name, int(value, 16)), end + 1 - index

    # Command without argument
    for name in control_keywords:
        if text.startswith(f"\\{name}", index):
            return name, 1 + len(name)

    raise Exception

class TrieNode:
    def __init__(self) -> None:
        self.children = defaultdict(TrieNode)
        self.code: None | tuple[int, int] = None


def build_dict_trie(dictionary: dict[str, str]) -> TrieNode:
    root = TrieNode()
    for key, value in dictionary.items():
        node = root
        i = 0
        while i < len(value):
            token, length = next_character(value, i)
            node = node.children[token]
            i += length
        node.code = (2 + int(key[4]), int(key[6:8], 16))
    return root


def encode_text_data(text_data: dict[str, str], dictionary: dict[str, str] | None = None) -> dict[str, list[int]]:
    encoding_dict: dict[str, list[int]] = build_encoding_dict()
    encoding_trie: TrieNode = build_dict_trie(dictionary or {})
    encoded_dict: dict[str, list[int]] = {}

    @lru_cache
    def recursive_encode(text_to_encode: str, index: int) -> list[int]:
        if index >= len(text_to_encode):
            return [0]

        token, length = next_character(text_to_encode, index)
        if isinstance(token, tuple):
            encoded = list(encoding_dict[token[0]])
            encoded[-1] += token[1]
            if token[0] == "jump":
                return encoded
        else:
            if token not in encoding_dict:
                token = "口"  # Use a white square to denote unknown characters
            encoded = encoding_dict[token]

        best = encoded + recursive_encode(text_to_encode, index + length)

        if token not in encoding_trie.children:
            # No dict entry
            return best

        node = encoding_trie.children[token]
        i = index + length
        depth = 1

        while i < len(text_to_encode):
            token2, token_length = next_character(text_to_encode, i)
            if token2 not in node.children:
                break
            node = node.children[token2]
            i += token_length
            depth += 1
            if node.code:
                candidate = list(node.code) + recursive_encode(text_to_encode, i)
                if len(candidate) < len(best):
                    best = candidate

        return best

    for key, text in text_data.items():
        encoded_text = recursive_encode(text, 0)
        encoded_dict[key] = encoded_text

    return encoded_dict


def build_compact_table(data: dict[str, list[int]]) -> tuple[list[int], dict[str, int]]:
    sorted_items = sorted(data.items(), key=lambda kv: -len(kv[1]))
    compact = []
    offsets = {}

    for key, seq in sorted_items:
        for key2, string_start in offsets.items():
            string_end = string_start + len(data[key2])
            if compact[string_end - len(seq) : string_end] == seq:
                offset = string_end - len(seq)
                break
        else:
            offset = len(compact)
            compact.extend(seq)
        offsets[key] = offset
    assert len(compact) <= 0xFFFF

    return compact, offsets


def write_text_data(rom: RomData, dictionary: dict[str, str], texts: dict[str, str], seasons: bool):
    if seasons:
        text_offset_split_index = text_offset_split_index_seasons
        text_offset_1 = GameboyAddress(
            rom.read_byte(text_offset_1_table_address_seasons), rom.read_word(text_offset_1_table_address_seasons + 1)
        )
        text_offset_2 = GameboyAddress(
            rom.read_byte(text_offset_2_table_address_seasons), rom.read_word(text_offset_2_table_address_seasons + 1)
        )
        text_table_eng_address = text_table_eng_address_seasons
        text_addresses_limit = text_addresses_limit_seasons
    else:
        text_offset_split_index = text_offset_split_index_ages
        text_offset_1 = GameboyAddress(
            rom.read_byte(text_offset_1_table_address_ages), rom.read_word(text_offset_1_table_address_ages + 1)
        )
        text_offset_2 = GameboyAddress(
            rom.read_byte(text_offset_2_table_address_ages), rom.read_word(text_offset_2_table_address_ages + 1)
        )
        text_table_eng_address = text_table_eng_address_ages
        text_addresses_limit = text_addresses_limit_ages

    dict1 = {}
    dict2 = {}
    for key, text in texts.items():
        if int(key[3:5], 16) < text_offset_split_index - 4:
            dict1[key] = text
        else:
            dict2[key] = text

    encoded_dict1 = encode_text_data(dict1, dictionary)
    encoded_dict1.update(encode_text_data(dictionary))
    encoded_dict2 = encode_text_data(dict2, dictionary)

    offset_table_length = (len(encoded_dict1) + len(encoded_dict2)) * 2
    text_offset_1_address = text_offset_1.address_in_rom()
    text_offset_2_address = text_offset_2.address_in_rom()
    text_table_current_address = text_table_eng_address
    tx_table_current_address = text_table_eng_address + 0x64 * 2
    text_offset_1_offset = text_table_eng_address + 0x64 * 2 + offset_table_length - text_offset_1_address
    assert text_offset_1_offset >= 0

    compact_table1, compact_offsets1 = build_compact_table(encoded_dict1)
    rom.write_bytes(text_offset_1_address + text_offset_1_offset, compact_table1)

    for i in range(4):
        rom.write_word(text_table_current_address, tx_table_current_address - text_table_eng_address)
        text_table_current_address += 2
        for j in range(0, 0x100):
            entry_name = f"DICT{i}_{simple_hex(j)}"
            rom.write_word(tx_table_current_address, compact_offsets1[entry_name] + text_offset_1_offset)
            tx_table_current_address += 2

    for i in range(text_offset_split_index - 4):
        start_address = tx_table_current_address
        subid = 0
        while True:
            tx = f"TX_{simple_hex(i)}{simple_hex(subid)}"
            if tx not in dict1:
                break
            subid += 1

            rom.write_word(tx_table_current_address, compact_offsets1[tx] + text_offset_1_offset)
            tx_table_current_address += 2
        if subid > 0:
            rom.write_word(text_table_current_address, start_address - text_table_eng_address)
        else:
            rom.write_word(text_table_current_address, 0)
        text_table_current_address += 2

    if __debug__ and False:
        sorted_dict = sorted(list(encoded_dict1.items()) + list(encoded_dict2.items()), key=lambda kv: -len(kv[1]))
        for entry in sorted_dict:
            if entry[0] in dict1:
                print(entry[0], dict1[entry[0]], len(entry[1]))
            elif entry[0] in dict2:
                print(entry[0], dict2[entry[0]], len(entry[1]))
    text_offset_2_offset = max(
        0, text_offset_1_address + text_offset_1_offset + len(compact_table1) - text_offset_2_address
    )
    compact_table2, compact_offsets2 = build_compact_table(encoded_dict2)
    assert text_offset_2_address + text_offset_2_offset + len(compact_table2) < text_addresses_limit, (
        "Text is too long ("
        f"{text_offset_2_address + text_offset_2_offset + len(compact_table2) - text_addresses_limit}"
        " too many bytes)"
    )
    logging.info(
        f"Free text bytes: {text_addresses_limit - text_offset_2_address - text_offset_2_offset - len(compact_table2)}"
    )
    rom.write_bytes(text_offset_2_address + text_offset_2_offset, compact_table2)

    for i in range(text_offset_split_index - 4, 0x60):
        start_address = tx_table_current_address
        subid = 0
        while True:
            tx = f"TX_{simple_hex(i)}{simple_hex(subid)}"
            if tx not in dict2:
                break
            subid += 1

            rom.write_word(tx_table_current_address, compact_offsets2[tx] + text_offset_2_offset)
            tx_table_current_address += 2
        if subid > 0:
            rom.write_word(text_table_current_address, start_address - text_table_eng_address)
        else:
            rom.write_word(text_table_current_address, 0)
        text_table_current_address += 2
