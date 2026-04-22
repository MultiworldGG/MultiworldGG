import typing
import Utils
import hashlib
import os
import json
import base64
import settings
import copy

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from . import DKC2World

from BaseClasses import ItemClassification, LocationProgressType

from .Names import ItemName
from .Items import item_groups
from .Text import string_to_bytes, goal_texts
from .Levels import level_map
from .Options import Goal
from .data import Palettes
from .Aesthetics import get_palette_bytes, palette_set_offsets
from .Names import RegionName
from Options import OptionError
from argparse import Namespace

from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes, APPatchExtension

from .data.Hints import CrankyHint, WrinklyHint, cranky_rarity_text, cranky_location_text, wrinkly_hint_text

HASH_US = '98458530599b9dff8a7414a7f20b777a'
HASH_US_REV_1 = 'd323e6bb4ccc85fd7b416f58350bc1a2'

STARTING_ID = 0xBF0000

rom_start_inventory = {
    ItemName.carry: 0x3DFF83,
    ItemName.climb: 0x3DFF84,
    ItemName.cling: 0x3DFF85,
    ItemName.cartwheel: 0x3DFF86,
    ItemName.swim: 0x3DFF87,
    ItemName.team_attack: 0x3DFF88,
    ItemName.helicopter_spin: 0x3DFF89,
    ItemName.rambi: 0x3DFF8A,
    ItemName.squawks: 0x3DFF8B,
    ItemName.enguarde: 0x3DFF8C,
    ItemName.squitter: 0x3DFF8D,
    ItemName.rattly: 0x3DFF8E,
    ItemName.clapper: 0x3DFF8F,
    ItemName.glimmer: 0x3DFF90,
    ItemName.skull_kart: 0x3DFF91,
    ItemName.barrel_kannons: 0x3DFF92,
    ItemName.barrel_exclamation: 0x3DFF93,
    ItemName.barrel_kong: 0x3DFF94,
    ItemName.barrel_warp: 0x3DFF95,
    ItemName.barrel_control: 0x3DFF96,
}

unlock_data = {
    STARTING_ID + 0x0001: [0x28, 0x56], # Galleon
    STARTING_ID + 0x0002: [0x29, 0x56], # Cauldron
    STARTING_ID + 0x0003: [0x2A, 0x56], # Quay
    STARTING_ID + 0x0004: [0x2B, 0x56], # Kremland
    STARTING_ID + 0x0005: [0x2C, 0x56], # Gulch
    STARTING_ID + 0x0006: [0x2D, 0x56], # Keep
    STARTING_ID + 0x0007: [0x2E, 0x56], # Flying Krock
    STARTING_ID + 0x000B: [0x30, 0x56], # Lost World (Cauldron)
    STARTING_ID + 0x000C: [0x31, 0x56], # Lost World (Quay)
    STARTING_ID + 0x000D: [0x32, 0x56], # Lost World (C)
    STARTING_ID + 0x000E: [0x33, 0x56], # Lost World (Cauldron)
    STARTING_ID + 0x000F: [0x34, 0x56], # Lost World (Cauldron)
    STARTING_ID + 0x0010: [0x0E, 0x05], # Diddy
    STARTING_ID + 0x0011: [0x0E, 0x05], # Dixie
    STARTING_ID + 0x0012: [0x00, 0x36], # Carry
    STARTING_ID + 0x0013: [0x02, 0x36], # Climb
    STARTING_ID + 0x0014: [0x03, 0x36], # Cling
    STARTING_ID + 0x0015: [0x01, 0x36], # Cartwheel
    STARTING_ID + 0x0016: [0x05, 0x36], # Swim
    STARTING_ID + 0x0017: [0x06, 0x05], # Team Attack
    STARTING_ID + 0x0018: [0x04, 0x36], # Helicopter Spin
    STARTING_ID + 0x0019: [0x07, 0x35], # Rambi
    STARTING_ID + 0x001A: [0x08, 0x35], # Squawks
    STARTING_ID + 0x001B: [0x09, 0x35], # Enaguarde
    STARTING_ID + 0x001C: [0x0A, 0x35], # Squitter
    STARTING_ID + 0x001D: [0x0B, 0x35], # Rattly 
    STARTING_ID + 0x001E: [0x0C, 0x35], # Clapper
    STARTING_ID + 0x001F: [0x0D, 0x35], # Glimmer
    STARTING_ID + 0x0020: [0x0F, 0x4B], # Barrel Kannons
    STARTING_ID + 0x0021: [0x12, 0x4B], # Barrel Exclamation
    STARTING_ID + 0x0022: [0x10, 0x4B], # Barrel Kong
    STARTING_ID + 0x0023: [0x13, 0x4B], # Barrel Warp
    STARTING_ID + 0x0024: [0x11, 0x4B], # Barrel Control 
    STARTING_ID + 0x0025: [0x14, 0x35], # Skull Kart
}

currency_data = {
    STARTING_ID + 0x002F: [0x8024, 0x56],
    STARTING_ID + 0x0008: [0x802F, 0x36], # Lost World Rock
    STARTING_ID + 0x0009: [0x80A2, 0x00], # DK Coin
    STARTING_ID + 0x000A: [0x80A4, 0x00], # Kremkoin
    STARTING_ID + 0x0030: [0x80A6, 0x00], # Banana Coin
    STARTING_ID + 0x0031: [0x80A0, 0x00], # 1-Up
}

trap_data = {
    STARTING_ID + 0x0040: [0x40, 0x00], # Freeze Trap
    STARTING_ID + 0x0041: [0x42, 0x00], # Reverse Trap
    STARTING_ID + 0x0042: [0x54, 0x00], # Honey Trap
    STARTING_ID + 0x0043: [0x4A, 0x00], # Ice Trap
    STARTING_ID + 0x0044: [0x50, 0x00], # TNT Barrel Trap
    STARTING_ID + 0x0045: [0x44, 0x00], # Damage Trap
    STARTING_ID + 0x0046: [0x46, 0x00], # Instant Death Trap
    STARTING_ID + 0x0032: [0x48, 0x1B], # Instant DK Barrel (not a trap, but this system works better lol)
    STARTING_ID + 0x0033: [0x4C, 0x2D], # Banana Extractinator (not a trap, but this system works better lol)
}

reward_list = [
    0x00,   # Banana bunch
    0x05,   # DK Barrel
    0x06,   # TNT Barrel
    0x07,   # Invincibility barrel
    0x08,   # Red balloon
    0x09,   # Green balloon
    0x0A,   # Blue balloon
    0x0C,   # Banana coin
    0x12,   # Cannonball
    0x19,   # Single banana
]

reward_list_weights = [
    20,  # Banana bunch
    5,   # DK Barrel
    5,   # TNT Barrel
    5,   # Invincibility barrel
    10,  # Red balloon
    10,  # Green balloon
    10,  # Blue balloon
    25,  # Banana coin
    5,   # Cannonball
    5,   # Single banana
]

trivia_addrs = {
    "easy": [
        0x34F800,
        0x34F900,
        0x34FA00,
        0x34FB00,
        0x34FC00,
        0x34FD00,
    ],
    "medium": [
        0x34F850,
        0x34F950,
        0x34FA50,
        0x34FB50,
        0x34FC50,
        0x34FD50,
    ],
    "hard": [
        0x34F8A0,
        0x34F9A0,
        0x34FAA0,
        0x34FBA0,
        0x34FCA0,
        0x34FDA0,
    ],
}

excluded_questions = [
    2*8, 
    7*8,
    9*8,
    10*8,
    12*8,
    16*8,
    24*8,
    27*8,
    30*8,
    35*8,
    36*8,
    41*8,
    45*8,
]

original_correct_answers = {
    # Galleon
    0: 0,
    1: 0,
    2: 2,
    3: 1,
    4: 1,
    5: 2,
    6: 1,
    7: 0,
    8: 2,
    # Cauldron
    9: 1,
    10: 0,
    11: 0,
    12: 2,
    13: 1,
    14: 0,
    15: 1,
    16: 2,
    17: 2,
    # Quay
    18: 0,
    19: 1,
    20: 2,
    21: 1,
    22: 2,
    23: 1,
    24: 1,
    25: 0,
    26: 2,
    # Kremland
    27: 2,
    28: 0,
    29: 2,
    30: 1,
    31: 1,
    32: 0,
    33: 2,
    34: 1,
    35: 2,
    # Gulch
    36: 0,
    37: 1,
    38: 2,
    39: 2,
    40: 1,
    41: 1,
    42: 2,
    43: 0,
    44: 0,
    # Keep
    45: 1,
    46: 2,
    47: 1,
    48: 0,
    49: 2,
    50: 1,
    51: 1,
    52: 0,
    53: 2,
}

class DKC2PatchExtension(APPatchExtension):
    game = "Donkey Kong Country 2"

    @staticmethod
    def shuffle_levels(caller: APProcedurePatch, rom: bytes) -> bytes:
        unshuffled_rom = bytearray(rom)
        rom = bytearray(rom)
        level_data = base64.b64decode(caller.get_file("levels.bin").decode("UTF-8"))
        rom_connections = json.loads(level_data)
        
        from .Levels import level_rom_data, boss_rom_data
        dkc2_level_rom_data = dict(level_rom_data, **boss_rom_data)

        for level, selected_level in rom_connections.items():
            addr = dkc2_level_rom_data[level][0]
            rom[addr] = selected_level[1]

            source_ptr = dkc2_level_rom_data[selected_level[0]][1]
            name_size = unshuffled_rom[source_ptr]
            name = unshuffled_rom[source_ptr + 1:source_ptr + name_size + 2]

            destination_ptr = dkc2_level_rom_data[level][1]
            rom[destination_ptr] = name_size
            rom[destination_ptr + 1:destination_ptr + name_size + 2] = bytearray(name)

        return bytes(rom)

    @staticmethod
    def generate_trivia(caller: APProcedurePatch, rom: bytes) -> bytes:
        rom = bytearray(rom)

        import random
        from worlds.dkc2_trivia.trivia import retrieve_topics
        from worlds.dkc2_trivia.types import TriviaQuestion, Topic

        json_data = json.loads(caller.get_file("data.json").decode("UTF-8"))
        random.seed(json_data["seed"])
        games_in_session: set = set(json_data["games_in_session"])

        if vars(Utils.persistent_load().get("trivia_settings", {}).get("Donkey Kong Country 2", Namespace())):
            persistent_settings = Utils.persistent_load().get("trivia_settings", {}).get("Donkey Kong Country 2", Namespace())
            # Fetch question count
            if hasattr(persistent_settings, "question_count"):
                question_count = persistent_settings.question_count
                if question_count == 0:
                    question_count = 1
            else:
                question_count = 1
            # Fetch topic statuses
            if hasattr(persistent_settings, "valid_topics"):
                for topic_name, topic_status in persistent_settings.valid_topics.items():
                    if topic_status == "Forced":
                        games_in_session.add(topic_name)
                    elif topic_status == "Excluded" and topic_name in games_in_session:
                        games_in_session.remove(topic_name)
        else:
            question_count = 1

        # Build database from original question
        start_addr = 0x34C591
        local_trivia_data: dict[str, Topic] = retrieve_topics(games_in_session, is_dkc2=True)

        for idx in range(0, 0x1B0, 8):
            if idx in excluded_questions:
                continue
            offset = int.from_bytes(rom[start_addr+idx:start_addr+idx+2], "little")
            offset |= 0x370000
            text_data = rom[offset:offset+0xD0]     # The max amount should be around 0xC6
            text_data = text_data.split(b'\x00')
            question = []
            for _ in range(6):
                question.append(text_data.pop(0).decode() + "°")

            offset = int.from_bytes(rom[start_addr+idx+4:start_addr+idx+6], "little")
            offset |= 0x370000
            text_data = rom[offset:offset+0x70]     # The max amount should be around 0x66
            text_data = text_data.split(b'\x00')
            answers = []
            for _ in range(3):
                text = text_data.pop(0).decode() + "°" + text_data.pop(0).decode() + "°"
                text = text[8:]
                answers.append(text)

            idy = original_correct_answers[idx >> 3]
            correct_answer = answers.pop(idy)
            data = TriviaQuestion(question, "RARE", "Donkey Kong Country 2", correct_answer, answers.pop(0), answers.pop(0))
            if idx % 0x48 < 0x10:
                local_trivia_data["Donkey Kong Country 2"].easy_questions.append(data)
            elif idx % 0x48 < 0x28:
                local_trivia_data["Donkey Kong Country 2"].medium_questions.append(data)
            else:
                local_trivia_data["Donkey Kong Country 2"].hard_questions.append(data)

        # Build valid library
        selected_trivia: dict[str, list[TriviaQuestion]] = {
            "easy": [],
            "medium": [],
            "hard": [],
        }
        
        for game, trivia in local_trivia_data.items():
            selected_trivia["easy"].extend(trivia.easy_questions)
            selected_trivia["medium"].extend(trivia.medium_questions)
            selected_trivia["hard"].extend(trivia.hard_questions)

        question_count = min(question_count, 
                             len(selected_trivia["easy"]) // 6, 
                             len(selected_trivia["medium"]) // 6, 
                             len(selected_trivia["hard"]) // 6)

        answer_a = "     A. "
        answer_b = "     B. "
        answer_c = "     C. "

        # Choose questions and write them to ROM
        write_addr = 0x378466
        for difficulty, questions in selected_trivia.items():
            random.shuffle(questions)
            for idx in range(6):
                pointer_addr = trivia_addrs[difficulty][idx]
                for idy in range(0, question_count*8, 8):
                    # Write a question
                    addr = write_addr & 0xFFFF
                    rom[pointer_addr+idy:pointer_addr+idy+2] = addr.to_bytes(2, "little")
                    rom[pointer_addr+idy+2:pointer_addr+idy+4] = bytearray([0x58, 0x02])
                    trivia = questions.pop(0)
                    for line in trivia.question:
                        write_addr = write_text_to_rom(rom, write_addr, line)

                    # Write answers
                    choice = random.randrange(1, 4)
                    addr = write_addr & 0xFFFF
                    rom[pointer_addr+idy+4:pointer_addr+idy+6] = addr.to_bytes(2, "little")
                    rom[pointer_addr+idy+6:pointer_addr+idy+8] = choice.to_bytes(2, "little")
                    if choice == 1:
                        write_addr = write_text_to_rom(rom, write_addr, answer_a + trivia.correct_answer)
                        write_addr = write_text_to_rom(rom, write_addr, answer_b + trivia.incorrect_answer_1)
                        write_addr = write_text_to_rom(rom, write_addr, answer_c + trivia.incorrect_answer_2)
                    elif choice == 2:
                        write_addr = write_text_to_rom(rom, write_addr, answer_a + trivia.incorrect_answer_1)
                        write_addr = write_text_to_rom(rom, write_addr, answer_b + trivia.correct_answer)
                        write_addr = write_text_to_rom(rom, write_addr, answer_c + trivia.incorrect_answer_2)
                    else:
                        write_addr = write_text_to_rom(rom, write_addr, answer_a + trivia.incorrect_answer_1)
                        write_addr = write_text_to_rom(rom, write_addr, answer_b + trivia.incorrect_answer_2)
                        write_addr = write_text_to_rom(rom, write_addr, answer_c + trivia.correct_answer)

        rom[0x34A3CC] = question_count

        # Save last written addr for later
        rom[0x400000:0x400003] = write_addr.to_bytes(3, "little")

        return bytes(rom)


    @staticmethod
    def write_cranky_hints(caller: APProcedurePatch, rom: bytes) -> bytes:
        rom = bytearray(rom)
        hint_data = bytearray(caller.get_file("cranky_hints.bin"))
        hint_offsets = bytearray(caller.get_file("cranky_hint_offsets.bin"))

        write_addr = int.from_bytes(rom[0x400000:0x400003], "little")

        size = len(hint_data)
        rom[write_addr:write_addr+size] = hint_data
        addr = 0x34C7B1
        
        for idx in range(0, 82, 2):
            offset = int.from_bytes(hint_offsets[idx:idx+2], "little")
            pointer = offset + write_addr & 0xFFFF
            rom[addr+idx:addr+idx+2] = bytearray(pointer.to_bytes(2, "little"))

        write_addr = write_addr + size
        rom[0x400000:0x400003] = write_addr.to_bytes(3, "little")

        return bytes(rom)
    

    @staticmethod
    def write_wrinkly_hints(caller: APProcedurePatch, rom: bytes) -> bytes:
        rom = bytearray(rom)
        hint_data = bytearray(caller.get_file("wrinkly_hints.bin"))
        hint_offsets = bytearray(caller.get_file("wrinkly_hint_offsets.bin"))

        write_addr = int.from_bytes(rom[0x400000:0x400003], "little")

        size = len(hint_data)
        rom[write_addr:write_addr+size] = hint_data
        addr = 0x34C74F

        invalid_options = [
            7*2,
            14*2,
            21*2,
            25*2,
            29*2,
            32*2,
        ]
        idy = 0
        for idx in range(2, 70, 2):
            if idx in invalid_options:
                continue
            offset = int.from_bytes(hint_offsets[idy:idy+2], "little")
            idy += 2
            pointer = offset + (write_addr & 0xFFFF)
            rom[addr+idx:addr+idx+2] = bytearray(pointer.to_bytes(2, "little"))

        return bytes(rom[:-3])


    @staticmethod
    def write_settings(caller: APProcedurePatch, rom: bytes) -> bytes:
        rom = bytearray(rom)

        import random

        reward_addrs: list[int] = [
            0x3FC49C,
            0x3FC4A5,
            0x3FC4AE,
            0x3FC4C9,
            0x3FC4D2,
            0x3FC4DB,
            0x3FC4ED,
            0x3FC4FF,
            0x3FC508,
            0x3FC511,
            0x3FC51A,
            0x3FC523,
            0x3FC52C,
            0x3FC53E,
            0x3FC550,
            0x3FC559,
        ]

        special_reward_addrs: dict[int, list[int,int]] = {
            0x3FC4B7: [0x04, 0x03],  # G letter
            0x3FC4C0: [0x04, 0x03],  # G letter
            0x3FC4E4: [0x04, 0x03],  # G letter
            0x3FC535: [0x04, 0x03],  # G letter
            0x3FC4F6: [0x11, 0x00],  # DK Coin
            0x3FC547: [0x11, 0x01],  # DK Coin
        }

        if vars(Utils.persistent_load().get("global_settings", {}).get("Donkey Kong Country 2", Namespace())):
            persistent_settings = Utils.persistent_load().get("global_settings", {}).get("Donkey Kong Country 2", Namespace())
            if hasattr(persistent_settings, "guaranteed_rewards"):
                guaranteed_rewards = persistent_settings.guaranteed_rewards
            else:
                guaranteed_rewards = False
            if hasattr(persistent_settings, "random_rewards"):
                random_rewards = persistent_settings.random_rewards
            else:
                random_rewards = False
        else:
            guaranteed_rewards = False
            random_rewards = False

        print (guaranteed_rewards, random_rewards)

        if guaranteed_rewards:
            for addr, value in special_reward_addrs.items():
                rom[addr+0x00] = 0x40
                rom[addr+0x01] = value[0x00]
                rom[addr+0x02] = 0x00

        if random_rewards:
            for addr in reward_addrs:
                rewards = random.choices(reward_list, reward_list_weights, k=4)
                rom[addr+0x01] = rewards[0]
                rom[addr+0x03] = rewards[1]
                rom[addr+0x05] = rewards[2]
                rom[addr+0x07] = rewards[3]

            if not guaranteed_rewards:
                for addr, value in special_reward_addrs.items():
                    rewards = random.choices(reward_list, reward_list_weights, k=4)
                    rom[addr+0x01] = rewards[0]
                    rom[addr+0x03] = rewards[1]
                    rom[addr+0x05] = rewards[2]
                    rom[addr+0x07] = rewards[3]
                    offset = value[1] * 2
                    rom[addr+0x01+offset] = value[0]

        return bytes(rom)


def write_text_to_rom(rom: bytearray, write_addr: int, input_string: str):
    data = string_to_bytes(input_string)
    size = len(data)
    rom[write_addr:write_addr+size] = data
    write_addr += size
    return write_addr


class DKC2ProcedurePatch(APProcedurePatch, APTokenMixin):
    hash = [HASH_US_REV_1]
    game = "Donkey Kong Country 2"
    patch_file_ending = ".apdkc2"
    result_file_ending = ".sfc"
    name: bytearray
    procedure = [
        ("apply_tokens", ["token_patch.bin"]),
        ("apply_bsdiff4", ["dkc2_basepatch.bsdiff4"]),
        ("shuffle_levels", []),
        ("generate_trivia", []),
        ("write_cranky_hints", []),
        ("write_wrinkly_hints", []),
        ("write_settings", []),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

    def write_byte(self, offset: int, value: int):
        self.write_token(APTokenTypes.WRITE, offset, value.to_bytes(1, "little"))

    def write_bytes(self, offset: int, value: typing.Iterable[int]):
        self.write_token(APTokenTypes.WRITE, offset, bytes(value))

def patch_rom(world: "DKC2World", patch: DKC2ProcedurePatch):
    # Edit the ROM header
    from Utils import __version__
    patch.name = bytearray(f'DKC2{__version__.replace(".", "")[0:3]}_{world.player}_{world.multiworld.seed:11}\0', 'utf8')[:21]
    patch.name.extend([0] * (21 - len(patch.name)))
    patch.write_bytes(0xFFC0, patch.name)

    # Set goal
    patch.write_byte(0x3DFF81, world.options.goal.value)
    patch.write_byte(0x3DFF82, world.options.lost_world_rocks.value)
    patch.write_byte(0x3DFF97, world.options.krock_boss_tokens.value)

    # Set starting lives
    patch.write_byte(0x008FA1, world.options.starting_life_count.value)

    # Link-features
    patch.write_byte(0x3DFF98, world.options.death_link.value)
    patch.write_byte(0x3DFF99, world.options.energy_link.value)
    patch.write_byte(0x3DFF9A, world.options.trap_link.value)

    # Options write
    patch.write_byte(0x3DFFA0, world.options.dk_coin_checks.value)
    patch.write_byte(0x3DFFA1, world.options.kong_checks.value)
    patch.write_byte(0x3DFFA2, world.options.balloonsanity.value)
    patch.write_byte(0x3DFFA3, world.options.coinsanity.value)
    patch.write_byte(0x3DFFA4, world.options.bananasanity.value)
    patch.write_byte(0x3DFFA5, world.options.swanky_checks.value)

    # Set level restrictions
    patch.write_bytes(0x3DFF00, world.options.required_galleon_levels.value.to_bytes(2, "little"))
    patch.write_bytes(0x3DFF02, world.options.required_cauldron_levels.value.to_bytes(2, "little"))
    patch.write_bytes(0x3DFF04, world.options.required_quay_levels.value.to_bytes(2, "little"))
    patch.write_bytes(0x3DFF06, world.options.required_kremland_levels.value.to_bytes(2, "little"))
    patch.write_bytes(0x3DFF08, world.options.required_gulch_levels.value.to_bytes(2, "little"))
    patch.write_bytes(0x3DFF0A, world.options.required_keep_levels.value.to_bytes(2, "little"))
    patch.write_bytes(0x3DFF0C, world.options.required_krock_levels.value.to_bytes(2, "little"))

    order = [
        RegionName.krows_nest_level,
        RegionName.pirate_panic_level,
        RegionName.mainbrace_mayhem_level,
        RegionName.gangplank_galley_level,
        RegionName.lockjaws_locker_level,
        RegionName.topsail_trouble_level,
        RegionName.kleevers_kiln_level,
        RegionName.hot_head_hop_level,
        RegionName.kannons_klaim_level,
        RegionName.lava_lagoon_level,
        RegionName.red_hot_ride_level,
        RegionName.squawks_shaft_level,
        RegionName.kudgels_kontest_level,
        RegionName.barrel_bayou_level,
        RegionName.glimmers_galleon_level,
        RegionName.krockhead_klamber_level,
        RegionName.rattle_battle_level,
        RegionName.slime_climb_level,
        RegionName.bramble_blast_level,
        RegionName.king_zing_sting_level,
        RegionName.hornet_hole_level,
        RegionName.target_terror_level,
        RegionName.bramble_scramble_level,
        RegionName.rickety_race_level,
        RegionName.mudhole_marsh_level,
        RegionName.rambi_rumble_level,
        RegionName.kreepy_krow_level,
        RegionName.ghostly_grove_level,
        RegionName.haunted_hall_level,
        RegionName.gusty_glade_level,
        RegionName.parrot_chute_panic_level,
        RegionName.web_woods_level,
        RegionName.stronghold_showdown_level,
        RegionName.arctic_abyss_level,
        RegionName.windy_well_level,
        RegionName.castle_crush_level,
        RegionName.clappers_cavern_level,
        RegionName.chain_link_chamber_level,
        RegionName.toxic_tower_level,
        RegionName.k_rool_duel_level,
        RegionName.screechs_sprint_level,
    ]
    for idx, map_level in enumerate(order):
        if map_level == RegionName.k_rool_duel_level:
            patch.write_bytes(0x3DFF5C, (0x61).to_bytes(2, "little"))
        elif map_level ==  RegionName.pirate_panic_level:
            patch.write_bytes(0x3DFF10, (0x03).to_bytes(2, "little"))
        else:
            shuffled_level: int = world.rom_connections[map_level][1]
            patch.write_bytes(0x3DFF0E+(idx*2), shuffled_level.to_bytes(2, "little"))

    # Enabled traps
    patch.write_byte(0x3DFFA8, world.options.freeze_trap_weight.value)
    patch.write_byte(0x3DFFA9, world.options.reverse_trap_weight.value)
    patch.write_byte(0x3DFFAA, world.options.honey_trap_weight.value)
    patch.write_byte(0x3DFFAB, world.options.ice_trap_weight.value)
    patch.write_byte(0x3DFFAC, world.options.tnt_barrel_trap_weight.value)
    patch.write_byte(0x3DFFAD, world.options.damage_trap_weight.value)
    patch.write_byte(0x3DFFAE, world.options.insta_death_trap_weight.value)

    # Write starting inventory
    patch.write_byte(0x3DFF80, world.options.starting_kong.value)

    for item in item_groups["Abilities"]:
        addr = rom_start_inventory[item]
        if item in world.options.shuffle_abilities.value:
            patch.write_byte(addr, 0x00)
        else:
            patch.write_byte(addr, 0x01)
    for item in item_groups["Animals"]:
        addr = rom_start_inventory[item]
        if item in world.options.shuffle_animals.value:
            patch.write_byte(addr, 0x00)
        else:
            patch.write_byte(addr, 0x01)
    for item in item_groups["Barrels"]:
        addr = rom_start_inventory[item]
        if item in world.options.shuffle_barrels.value:
            patch.write_byte(addr, 0x00)
        else:
            patch.write_byte(addr, 0x01)

    # Write amount of questions per quiz (for the menus)
    #patch.write_byte(0x34A3CC, world.options.swanky_questions_per_quiz.value)

    # Write flavor text for the goal
    if world.options.goal == Goal.option_kompletionist:
        if world.options.krock_boss_tokens.value != 0:
            text = goal_texts["kompletionist_tokens"].copy()
        else:
            text = goal_texts["kompletionist_item"].copy()
    elif world.options.goal == Goal.option_flying_krock:
        if world.options.krock_boss_tokens.value != 0:
            text = goal_texts["flying_krock_tokens"].copy()
        else:
            text = goal_texts["flying_krock_items"].copy()
    else:
        text = goal_texts["lost_world"].copy()
    
    data = bytearray()
    for line in text:
        line = line.replace("TOKENS", str(world.options.krock_boss_tokens.value))
        line = line.replace("ROCKS", str(world.options.lost_world_rocks.value))
        line = line.center(32, " ").rstrip() + "°"
        line = string_to_bytes(line)
        data += line

    patch.write_bytes(0x34AC84, data)

    # Write additional data for generation
    games_in_session = set()
    for _, game_world in world.multiworld.worlds.items():
        games_in_session.add(game_world.game)

    data_dict = {
        "seed": world.random.getrandbits(64),
        "games_in_session": list(games_in_session),
        "energy_link": world.options.energy_link.value,
        "trap_link": world.options.trap_link.value,
        "death_link": world.options.death_link.value,
    }
    patch.write_file("data.json", json.dumps(data_dict).encode("UTF-8"))

    # Write hints to an external file
    compute_cranky_hints(world, patch)
    compute_wrinkly_hints(world, patch)

    adjust_palettes(world, patch)

    # Save shuffled levels data
    json_levels = json.dumps(world.rom_connections).encode("UTF-8")
    patch.write_file("levels.bin", base64.b64encode(json_levels))

    patch.write_file("token_patch.bin", patch.get_token_binary())

 
def compute_cranky_hints(world: "DKC2World", patch: DKC2ProcedurePatch):
    # Prepare hints
    reverse_connections = {y: x for x, y in world.level_connections.items()}
    valid_hints: List[CrankyHint] = []
    for location in world.multiworld.get_filled_locations(world.player):
        if location.progress_type is LocationProgressType.EXCLUDED or \
            location.is_event or \
            "(Map Event)" in location.name or \
            "Defeated" in location.name or \
            "K. Rool Duel" in location.name or  \
            "Krocodile Kore" in location.name:
            continue
        level_name = location.name.split(" - ")[0]
        location_type = location.name.split(" - ")[1].split(" #")[0].split("(")[0].strip()
        bonus_num = 0
        if "Swanky" in location.name:
            level_name = "Swanky Trivia"
            location_type = "Swanky"
            world_name = location.name.split(" at ")[1].split(" - ")[0]
        elif "Bonus" in location.name:
            bonus_num = location.name.split("#")[1]
        else:
            level_map_name = reverse_connections[level_name + ": Level"]
            world_name = level_map[level_map_name]
        world_name = world_name.split(" (")[0]

        # Let's ignore tags that we don't care about
        classification = location.item.classification
        classification &= ItemClassification.skip_balancing^0xFFFF
        classification &= ItemClassification.deprioritized^0xFFFF

        data = CrankyHint(
            location_type,
            level_name, 
            world_name, 
            bonus_num,
            location.item.name, 
            int(classification),
            world.multiworld.get_player_name(location.item.player),
        )
        valid_hints.append(data)

    # Select hints
    hint_data = bytearray()
    hint_offsets = bytearray()
    world.random.shuffle(valid_hints)
    count = 0
    addr = 0
    for hint in valid_hints:
        hint_text: List[str] = []
        selection = world.random.choice(cranky_location_text[hint.type])
        hint_text.extend(selection)
        if hint.classification not in cranky_rarity_text.keys():
            hint.classification = 0xFF
        selection = world.random.choice(cranky_rarity_text[hint.classification])
        hint_text.extend(selection)

        hint_offsets += addr.to_bytes(2, "little")

        for line in hint_text:
            line = line.replace("LEVEL", hint.level)
            line = line.replace("WORLD", hint.world)
            line = line.replace("NUM", hint.bonus)
            line = line.replace("PLAYER", hint.player)
            line = line.replace("ITEM", hint.item)
            line = line.center(32, " ").rstrip() + "°"
            line = string_to_bytes(line)
            hint_data += line
            addr += len(line)

        count += 1
        if count == 41:
            break

    patch.write_file("cranky_hints.bin", hint_data)
    patch.write_file("cranky_hint_offsets.bin", hint_offsets)


def compute_wrinkly_hints(world: "DKC2World", patch: DKC2ProcedurePatch):
    hint_data = bytearray()
    hint_offsets = bytearray()
    hints = []

    hintable_items = [
        ItemName.diddy,
        ItemName.dixie,
        ItemName.crocodile_cauldron,
        ItemName.krem_quay,
        ItemName.krazy_kremland,
        ItemName.gloomy_gulch,
        ItemName.krools_keep,
        ItemName.the_flying_krock,
        ItemName.lost_world_cauldron,
        ItemName.lost_world_quay,
        ItemName.lost_world_kremland,
        ItemName.lost_world_gulch,
        ItemName.lost_world_keep,
        ItemName.carry,
        ItemName.climb,
        ItemName.cling,
        ItemName.cartwheel,
        ItemName.swim,
        ItemName.team_attack,
        ItemName.helicopter_spin,
        ItemName.rambi,
        ItemName.squawks,
        ItemName.enguarde,
        ItemName.squitter,
        ItemName.rattly,
        ItemName.clapper,
        ItemName.glimmer,
        ItemName.barrel_kannons,
        ItemName.barrel_exclamation,
        ItemName.barrel_kong,
        ItemName.barrel_warp,
        ItemName.barrel_control,
        ItemName.skull_kart,
        ItemName.lost_world_rock,
        ItemName.dk_coin,
        ItemName.kremkoins,
        ItemName.banana_coin,
        ItemName.red_balloon,
    ]
    unskippable_items = [
        ItemName.lost_world_rock,
        ItemName.dk_coin,
        ItemName.kremkoins,
        ItemName.banana_coin,
        ItemName.red_balloon,
    ]

    abort = False
    count = 0
    for item in hintable_items:
        if item in world.options.start_inventory.value and item not in unskippable_items:
            continue
        locations = world.multiworld.find_item_locations(item, world.player)
        if len(locations) == 0:
            continue
        
        for location in locations:
            hint = WrinklyHint(
                location.item.name,
                location.name,
                world.multiworld.get_player_name(location.player),
                location.game,
            )
            hints.append(hint)
            count += 1
            if count == 28:
                abort = True
                break

        if abort:
            break

    world.random.shuffle(hints)
    # B4AC84
    addr = 0
    hint: WrinklyHint
    for hint in hints:
        hint_text: List[str] = []
        selection = world.random.choice(wrinkly_hint_text)
        hint_text.extend(selection)

        hint_offsets += addr.to_bytes(2, "little")

        if "LOCATION" in hint_text[-1]:
            hint_text.pop()
            hint_text.extend(hint.location)

        for line in hint_text:
            line = line.replace("PLAYER", hint.player)
            line = line.replace("ITEM", hint.item)
            line = line.replace("GAME", hint.game)
            line = line.center(32, " ").rstrip() + "°"
            line = string_to_bytes(line)
            hint_data += line
            addr += len(line)
            
    patch.write_file("wrinkly_hints.bin", hint_data)
    patch.write_file("wrinkly_hint_offsets.bin", hint_offsets)


def adjust_palettes(world: "DKC2World", patch: DKC2ProcedurePatch):
    palette_options = {
        "Diddy": world.options.palette_diddy_active.current_key,
        "Diddy Inactive": world.options.palette_diddy_inactive.current_key,
        "Diddy Invincible": world.options.palette_diddy_invincible.current_key,
        "Diddy Frozen": world.options.palette_diddy_frozen.current_key,
        "Diddy Reversed": world.options.palette_diddy_reversed.current_key,
        "Diddy Slow": world.options.palette_diddy_slow.current_key,
        "Dixie": world.options.palette_dixie_active.current_key,
        "Dixie Inactive":  world.options.palette_dixie_inactive.current_key,
        "Dixie Invincible": world.options.palette_dixie_invincible.current_key,
        "Dixie Frozen": world.options.palette_dixie_frozen.current_key,
        "Dixie Reversed": world.options.palette_dixie_reversed.current_key,
        "Dixie Slow": world.options.palette_dixie_slow.current_key,
        "Rambi": world.options.palette_rambi.current_key,
        "Enguarde": world.options.palette_enguarde.current_key,
        "Squitter": world.options.palette_squitter.current_key,
        "Rattly": world.options.palette_rattly.current_key,
        "Squawks": world.options.palette_squawks.current_key,
        "Quawks": world.options.palette_quawks.current_key,
    }
    custom_palettes = world.options.palettes
    palette_filters = world.options.palette_filters
    for palette_set, offset in palette_set_offsets.items():
        palette_option = palette_options[palette_set]
        if "Diddy" in palette_set:
            palette = Palettes.palettes["Diddy"][palette_option]
        elif "Dixie" in palette_set:
            palette = Palettes.palettes["Dixie"][palette_option]
        else:
            palette = Palettes.palettes[palette_set][palette_option]
        
        if palette_set in custom_palettes.keys():
            if len(custom_palettes[palette_set]) == 0x0F:
                palette = custom_palettes[palette_set]
            else:
                print (f"[{world.multiworld.player_name[world.player]}] Custom palette set for {palette_set} doesn't have exactly 15 colors. Falling back to the selected preset ({palette_option})")
        
        if palette_set in palette_filters:
            filter_option = palette_filters[palette_set]
        else:
            filter_option = 0
        data = get_palette_bytes(palette, filter_option)
        patch.write_bytes(offset, data)


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(Utils.read_snes_rom(open(file_name, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if basemd5.hexdigest() not in {HASH_US_REV_1}:
            raise Exception('Supplied Base Rom does not match known MD5 for US 1.1 release. '
                            'Get the correct game and version, then dump it')
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    options: settings.Settings = settings.get_settings()
    if not file_name:
        file_name = options["dkc2_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
