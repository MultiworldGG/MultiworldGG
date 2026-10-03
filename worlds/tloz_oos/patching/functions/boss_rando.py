from typing import Any

from ...common.patching.z80asm.Assembler import Z80Assembler


def place_bosses(assembler: Z80Assembler, room_data: list[bytearray], patch_data: Any):
    boss_data = patch_data["boss_mapping"]
    boss_patch = [
        place_aquamentus,
        place_dodongo,
        place_mothula,
        place_gohma,
        place_digdogger,
        place_manhandla,
        place_gleeok,
        place_medusa,
    ]
    for dungeon in range(1, 9):
        target_boss = boss_data[str(dungeon)]
        if target_boss != dungeon:
            boss_patch[target_boss - 1](assembler, room_data, dungeon)


def place_aquamentus(assembler: Z80Assembler, _: list[bytearray], dungeon: int) -> None:
    assembler.define_byte(f"d{dungeon}_boss", 0x78)

    assembler.define_byte(f"d{dungeon}_boss_y", 0x50)
    assembler.define_byte(f"d{dungeon}_boss_x", 0xB0)

    if dungeon == 3:
        assembler.define_byte("d1_boss_in_d3", 1)


def place_dodongo(assembler: Z80Assembler, room_data: list[bytearray], dungeon: int) -> None:
    assembler.define_byte(f"d{dungeon}_boss", 0x79)

    if dungeon == 1:
        spikes = [
            0x11,
            0x12,
            0x13,
            0x14,
            0x15,
            0x21,
            0x22,
            0x23,
            0x24,
            0x31,
            0x32,
            0x41,
            0x61,
            0x71,
            0x72,
            0x81,
            0x82,
            0x83,
            0x84,
            0x91,
            0x92,
            0x93,
            0x94,
            0x95,
        ]
        room = room_data[0x512]
        for spike in spikes:
            room[spike] = 0x60
        assembler.define_byte("d2_boss_in_d1", 1)
    elif dungeon == 3:
        room_changes = {
            # Top
            0x00: 0xB8,
            0x01: 0xB0,
            0x02: 0xB0,
            0x0C: 0xB0,
            0x0D: 0xB0,
            0x0E: 0xB9,
            0x10: 0xB3,
            0x11: 0xA1,
            0x12: 0xA1,
            0x1C: 0xA1,
            0x1D: 0xA1,
            0x1E: 0xB1,
            0x20: 0xB3,
            0x21: 0xA1,
            0x2D: 0xA1,
            0x2E: 0xB1,
            # Bottom
            0x70: 0xB3,
            0x71: 0xA1,
            0x7D: 0xA1,
            0x7E: 0xB1,
            0x80: 0xB3,
            0x81: 0xA1,
            0x82: 0xA1,
            0x8C: 0xA1,
            0x8D: 0xA1,
            0x8E: 0xB1,
            0x90: 0xBA,
            0x91: 0xB2,
            0x92: 0xB2,
            0x9C: 0xB2,
            0x9D: 0xB2,
            0x9E: 0xBB,
            # Spikes
            0x44: 0x60,
            0x45: 0x60,
            0x46: 0x60,
            0x48: 0x60,
            0x49: 0x60,
            0x4A: 0x60,
            0x54: 0x60,
            0x55: 0x60,
            0x56: 0x60,
            0x58: 0x60,
            0x59: 0x60,
            0x5A: 0x60,
        }

        room = room_data[0x553]
        for tile, change in room_changes.items():
            room[tile] = change

        assembler.define_byte("d2_boss_in_d3", 1)
        assembler.define_byte("d2_boss_in_other_dungeons", 1)

        assembler.define_byte(f"d{dungeon}_boss_y", 0x20)
        assembler.define_byte(f"d{dungeon}_boss_x", 0x78)
    elif dungeon == 4:
        room = room_data[0x55F]
        for i in range(0x45, 0x70, 0x10):
            for tile in range(i, i + 5):
                room[tile] = 0x60
        assembler.define_byte("d2_boss_in_other_dungeons", 1)
    elif dungeon == 5:
        room_changes = {
            # Pillars
            0x01: 0xB0,
            0x11: 0xC1,
            0x81: 0xC1,
            0x8D: 0xC1,
            # Spikes
            ## Top
            0x12: 0x60,
            0x13: 0x60,
            0x14: 0x60,
            0x15: 0x60,
            0x16: 0x60,
            0x18: 0x60,
            0x19: 0x60,
            0x1A: 0x60,
            0x1B: 0x60,
            0x1C: 0x60,
            # Sides
            0x31: 0x60,
            0x3D: 0x60,
            0x41: 0x60,
            0x4D: 0x60,
            0x61: 0x60,
            0x6D: 0x60,
            0x71: 0x60,
            0x7D: 0x60,
            # Bottom
            0x92: 0x60,
            0x93: 0x60,
            0x94: 0x60,
            0x95: 0x60,
            0x96: 0x60,
            0x98: 0x60,
            0x99: 0x60,
            0x9A: 0x60,
            0x9B: 0x60,
            0x9C: 0x60,
        }

        room = room_data[0x58C]
        for tile, change in room_changes.items():
            room[tile] = change
        assembler.define_byte("d2_boss_in_other_dungeons", 1)

    elif dungeon == 6:
        room = room_data[0x5D5]
        for tile in range(0x56, 0x59):
            room[tile] = 0x60
        assembler.define_byte("d2_boss_in_d6", 1)

    elif dungeon == 7:
        assembler.define_byte("d2_boss_in_other_dungeons", 1)

    elif dungeon == 8:
        room = room_data[0x664]
        for x in range(0x01, 0x0E):
            if x != 0x07:
                for y in range(0x10, 0x30, 0x10):
                    room[y + x] = 0x60
            if x != 0x03:
                for y in range(0x80, 0xA0, 0x10):
                    room[y + x] = 0x60
        assembler.define_byte("d2_boss_in_other_dungeons", 1)


def place_mothula(assembler: Z80Assembler, _: list[bytearray], dungeon: int):
    assembler.define_byte(f"d{dungeon}_boss", 0x7A)
    assembler.define_byte("d3_boss_not_in_d3", 1)


def place_gohma(assembler: Z80Assembler, _: list[bytearray], dungeon: int):
    if dungeon == 3:
        raise NotImplementedError
    assembler.define_byte(f"d{dungeon}_boss", 0x7B)


def place_digdogger(assembler: Z80Assembler, room_data: list[bytearray], dungeon: int):
    assembler.define_byte(f"d{dungeon}_boss", 0x7C)
    if dungeon == 1:
        # To avoid the ball to get stuck
        room = room_data[0x512]
        removed_blocks = [0x19, 0x99, 0x2A, 0x8A, 0x2B, 0x8B, 0x3C, 0x7C, 0x4D, 0x6D]
        for tile in removed_blocks:
            room[tile] = 0x3E
    elif dungeon == 2:
        # Too many bushes makes the game lag when the small ones spawn
        room = room_data[0x529]
        removed_bushes = [0x12, 0x1C, 0x21, 0x2D, 0x81, 0x8D, 0x92, 0x9C]
        for tile in removed_bushes:
            room[tile] = 0x4A
    elif dungeon == 3:
        raise NotImplementedError


def place_manhandla(assembler: Z80Assembler, _: list[bytearray], dungeon: int):
    assembler.define_byte(f"d{dungeon}_boss", 0x7D)
    if dungeon == 3:
        assembler.define_byte("d6_boss_in_d3", 1)


def place_gleeok(assembler: Z80Assembler, _: list[bytearray], dungeon: int):
    assembler.define_byte(f"d{dungeon}_boss", 0x06)
    if dungeon == 3:
        assembler.define_byte("d7_boss_in_d3", 1)


def place_medusa(assembler: Z80Assembler, _: list[bytearray], dungeon: int):
    assembler.define_byte(f"d{dungeon}_boss", 0x7F)
    if dungeon == 3:
        assembler.define_byte("d8_boss_in_d3", 1)
