from dataclasses import dataclass
from typing import NamedTuple
import struct


@dataclass
class DoSBoss:
    flag: int  # The SLOT's Boss Defeated flag.
    assigned_soul: int  # Which Soul is assigned to the SLOT's original boss.
    floor_height: int  # The SLOT's room floor height
    room_width: int  # The SLOT's room width
    boss_address_pointer: int  # Which adress we write to to place the boss
    seal_index: int  # Which seal this slot uses
    old_boss: str  # Which boss is normally here
    new_boss: str = "None"  # Which boss has been randomized to be here


@dataclass
class DoSBossData:
    enemy_id: int  # The Enemy's internal ID number
    flag_index: int  # Index used for writing boss flags
    seal_index_pointers: list[int]  # Addresses for the seal index
    file: str  # The file we write to


class DoSBossStats(NamedTuple):
    hp: int  # Enemy's HP
    mp: int  # Enemy's MP
    exp: int  # Enemy's EXP
    atk: int  # Enemy's Attack
    defns: int  # Enemy's Defense
    scaling_factor: int  # Position in boss order ; used to calculate scaling position


base_enemy_address = 0x2078CAC  # I can't import this

boss_stats = {
    "Flying Armor": DoSBossStats(0x00FA, 0x00C8, 0x01F4, 0x18, 0x00, 1),
    "Balore": DoSBossStats(0x0384, 0x01F4, 0x03E8, 0x2D, 0x00, 30),
    "Malphas": DoSBossStats(0x04B0, 0x0320, 0x05DC, 0x34, 0x00, 32),
    "Dmitrii": DoSBossStats(0x03E8, 0x05DC, 0x07D0, 0x30, 0x00, 31),
    "Dario": DoSBossStats(0x05DC, 0x03E8, 0x09C4, 0x3C, 0x00, 33),
    "Puppet Master": DoSBossStats(0x0708, 0x0BB8, 0x0BB8, 0x26, 0x00, 34),
    "Rahab": DoSBossStats(0x04B0, 0x0898, 0x0FA0, 0x39, 0x00, 35),
    "Gergoth": DoSBossStats(0x0ED8, 0x270F, 0x10C2, 0x45, 0x08, 36),
    "Zephyr": DoSBossStats(0x04D2, 0x04D2, 0x162E, 0x50, 0x19, 37),
    "Bat Company": DoSBossStats(0x05DC, 0x05DC, 0x1662, 0x46, 0x00, 38),
    "Paranoia": DoSBossStats(0x06A4, 0x06A4, 0x1F40, 0x48, 0x0A, 39),
    "Aguni": DoSBossStats(0x0FA0, 0x270F, 0x2710, 0x63, 0x0A, 40),
    "Death": DoSBossStats(0x115C, 0x115C, 0x386C, 0x90, 0x1E, 41),
    "Abaddon": DoSBossStats(0x0FA0, 0x270F, 0x2EE0, 0x6E, 0x09, 42),
}

stat_offsets = [
    0x0E,  # HP
    0x10,  # MP
    0x12,  # EXP
    0x15,  # Atk
    0x16,  # Def
]


def randomize_bosses(world):
    boss_pool = [
        "Paranoia",
        "Gergoth",
        "Abaddon",
        "Puppet Master",
        "Rahab",  # We want to place these bosses first so that they can be fulfilled first
        "Balore",
        "Flying Armor",
        "Dmitrii",
        "Malphas",
        "Dario",
        "Zephyr",
        "Bat Company",
        "Aguni",
        "Death"
    ]

    world.boss_slots = {
        "Lost Village": DoSBoss(0x02, 0x35, 1, 2, 0x20A10b8, 1, "Flying Armor"),  # Flying Armor
        "Wizardry Lab": DoSBoss(0x04, 0x74, 1, 1, 0x20A90b0, 2, "Balore"),  # Balore
        "Dark Chapel": DoSBoss(0x08, 0xFF, 1, 2, 0x20AEb58, 3, "Dmitrii"),  # Dmitrii
        "Dark Chapel Inner": DoSBoss(0x10, 0x75, 2, 2, 0x20AEB04, 4, "Malphas"),  # Malphas
        "Garden of Madness": DoSBoss(0x20, 0xFF, 1, 2, 0x20AC500, 5, "Dario"),   # Dario 1 Make sure this is the right address for the flag. Seems low.
        "Demon Guest House": DoSBoss(0x40, 0x00, 1, 2, 0x20A56f0, 6, "Puppet Master"),  # Puppet Master
        "Condemned Tower": DoSBoss(0x80, 0x57, 1, 1, 0x20b1Be0, 7, "Gergoth"),  # Gergoth
        "Cursed Clock Tower": DoSBoss(0x0200, 0x01, 1, 2, 0x20B8da0, 9, "Zephyr"),  # Zephyr
        "Subterranean Hell": DoSBoss(0x0100, 0x77, 1, 2, 0x20B4b1c, 8, "Rahab"),  # Rahab
        "Silenced Ruins": DoSBoss(0x0400, 0x36, 1, 1, 0x20B64B0, 10, "Bat Company"),  # Bat Company
        "Demon Guest House Upper": DoSBoss(0x1000, 0x02, 1, 1, 0x20A59a8, 12, "Paranoia"),  # Paranoia
        "The Pinnacle": DoSBoss(0x0800, 0x2B, 1, 2, 0x02225C30, 11, "Aguni"),  # Aguni, not Dario 2
        "Mine of Judgment": DoSBoss(0x2000, 0x58, 1, 2, 0x20B2360, 13, "Death"),  # Death
        "The Abyss": DoSBoss(0x8000, 0x2C, 1, 1, 0x20BE260, 15, "Abaddon")  # Abaddon
    }

    world.boss_data = {
        "Flying Armor": DoSBossData(0x65, 0, [0x022ffb7c, 0x02300b24], "overlay_30"),
        "Balore": DoSBossData(0x66, 2, [0x022ffcf0, 0x23006C8], "overlay_23"),
        "Malphas": DoSBossData(0x67, 6, [0x022ffaec, 0x02300c44], "overlay_29"),
        "Dmitrii": DoSBossData(0x68, 4, [0], "overlay_40"),
        "Dario": DoSBossData(0x69, 8, [0], "overlay_25"),
        "Puppet Master": DoSBossData(0x6A, 10, [0x022ffc20, 0x022ffd18], "overlay_25"),
        "Rahab": DoSBossData(0x6B, 14, [0x022ffb48, 0x022ffc60], "overlay_26"),
        "Gergoth": DoSBossData(0x6C, 12, [0x022ffab0, 0x02300e00], "overlay_36"),
        "Zephyr": DoSBossData(0x6D, 16, [0x022ffb00, 0x023014C8], "overlay_33"),
        "Bat Company": DoSBossData(0x6E, 18, [0x022ffa6c, 0x02300330], "overlay_37"),
        "Paranoia": DoSBossData(0x6F, 22, [0x02305BF0, 0x02302D78], "overlay_35"),
        "Aguni": DoSBossData(0x70, 20, [0x02243D94, 0x02243F04], "overlay_1"),
        "Death": DoSBossData(0x71, 24, [0x022ffac0, 0x023022e0], "overlay_34"),
        "Abaddon": DoSBossData(0x72, 26, [0x22FFA70, 0x23002BC], "overlay_39")
    }

    if not world.options.goal:
        boss_pool.remove("Aguni")
        world.boss_slots.pop("The Pinnacle")

    if world.mine_status == "Disabled":
        #  Remove endgame bosses

        boss_pool.remove("Death")
        boss_pool.remove("Abaddon")

        world.boss_slots.pop("Mine of Judgment")
        world.boss_slots.pop("The Abyss")

    for boss in boss_pool:
        valid_rooms = [room for room in world.boss_slots if world.boss_slots[room].new_boss == "None"]
        if boss in ["Puppet Master", "Rahab"]:
            # Puppet Master and Rahab need to be in a room that is 2-tiles wide.
            # Puppet Master can teleport the player out of bounds, and Rahab would take a long time to be damagable.
            valid_rooms = [room for room in valid_rooms if world.boss_slots[room].room_width == 2]
        elif boss == "Balore":
            # We CANNOT put Balore in Rahab's room because of bugs.
            valid_rooms = [room for room in valid_rooms if world.boss_slots[room].old_boss != "Rahab"]
        elif boss in ["Paranoia", "Gergoth", "Abaddon"]:
            valid_rooms = [room for room in valid_rooms if world.boss_slots[room].room_width == 1]

        new_room = world.random.choice(valid_rooms)
        world.boss_slots[new_room].new_boss = boss


def write_bosses(world, rom):
    from .rahab_room_extender import expand_rahab_room
    rom.write_to_file(0x20A90C1, "arm9", bytearray([0x00]))  # Delete the Balore pre-boss cutscene, it breaks the game
    rom.write_to_file(0x20AEB69, "arm9", bytearray([0x00]))  # Delete the Malachi in Dmitrii's room used for the pre-boss cutscene
    rom.write_to_file(0x2308B58, "overlay_41", bytearray([0x01]))  # Flag that Boss Shuffle is on, triggers some changes in the ROM
    rom.write_to_file(0x20AEB75, "arm9", bytearray([0x00]))  # Hider for Dmitrii's Quetzalcoatl
    if world.boss_slots["Dark Chapel"].new_boss in ["Dmitrii", "Dario"]:
        rom.write_to_file(0x02308E48, "overlay_41", bytearray([0x01]))

    if world.boss_slots["Garden of Madness"].new_boss in ["Dmitrii", "Dario"]:
        rom.write_to_file(0x02308E49, "overlay_41", bytearray([0x01]))

    if world.boss_slots["Demon Guest House"].new_boss != "Puppet Master":
        # Puppet master's wall is too thick for normal bosses to function, so we move it over
        for i in range(12):
            rom.copy_bytes(0x2A6472 + (0x40 * i), 0x14, 0x2A6460 + (0x40 * i))  # Layer 0

        for i in range(10):
            rom.copy_bytes(0x2A67D2 + (0x40 * i), 0x12, 0x2A67B2 + (0x40 * i))  # layer 1

    if world.boss_slots["Wizardry Lab"].new_boss != "Balore":
        # Conver the room into a one-tile to preserve the fight space
        for i in range(0x158):
            rom.write_to_file(0x022E2A98 + i, "overlay_6", bytearray([0x00]))  # Zero out garbage

        rom.copy_bytes(0x2101AA, 0x20, 0x20FD38)  # Copy over the floor
        rom.write_to_file(0x022E2AB6, "overlay_6", bytearray([0x37]))  # And build a right wall
        rom.write_to_file(0x022E2AD6, "overlay_6", bytearray([0x47]))
        rom.write_to_file(0x022E2AF6, "overlay_6", bytearray([0x57]))
        rom.write_to_file(0x022E2B16, "overlay_6", struct.pack("H", 0x8037))
        rom.write_to_file(0x022E2A68, "overlay_6", bytearray([0x01]))

        rom.write_to_file(0x022E2BB6, "overlay_6", bytearray([0x37]))
        rom.write_to_file(0x022E2BD6, "overlay_6", struct.pack("H", 0x8037))
        for i in range(10):
            rom.write_to_file(0x22E2A98 + (i * 0x20), "overlay_6", struct.pack("H", 0x01FA))
        ########################
        rom.write_to_file(0x020A6C90, "arm9", bytearray([0x01]))  # Move the Door entry to the new pos
        rom.write_to_file(0x020A7B37, "arm9", bytearray([0x00]))  # Move the ENTRANCE position to the left

        rom.write_to_file(0x020A90C8, "arm9", struct.pack("H", 0xF0))  # Move the Boss Door to the new entrance
        rom.write_to_file(0x020A90CA, "arm9", struct.pack("H", 0x90))
        #########################
        # Get rid of the post-boss entities
        rom.write_to_file(0x020A90E5, "arm9", bytearray([0x00]))
        rom.write_to_file(0x020A90F1, "arm9", bytearray([0x00]))
        rom.write_to_file(0x020A90FD, "arm9", bytearray([0x00]))
        #########################

    if world.boss_slots["Dark Chapel Inner"].new_boss == "Balore":
        #  This floor needs to be lowered
        rom.write_to_file(0x022E4A20, "overlay_8", struct.pack("H", 0x026D))
        rom.write_to_file(0x022E4A60, "overlay_8", struct.pack("H", 0x0117))  # Extend the ramp downwards

        rom.copy_bytes(0x255D50, 0x30, 0x255D90)
        rom.copy_bytes(0x255D10, 0x30, 0x255D50)
        rom.copy_bytes(0x255CD0, 0x30, 0x255D10)  # Copy the floor down

        rom.copy_bytes(0x255DE0, 0x30, 0x0255CD0)  # Blank out the top row
        rom.write_to_file(0x022E49EC, "overlay_8", bytearray([0x40, 0x01, 0x41, 0x01]))  # And fix the wall

    if world.boss_slots["Subterranean Hell"].new_boss != "Rahab":
        # Spawn a floor if Rahab isn't in his room
        rom.write_to_file(0x022F27E2, "overlay_17", struct.pack("H", 0x022E))
        rom.write_to_file(0x022F281C, "overlay_17", struct.pack("H", 0x422E))
        for i in range(0x1C):
            rom.write_to_file(0x022F27E4 + 2 * i, "overlay_17", struct.pack("H", 0x022F))

        for i in range(0x20):
            rom.write_to_file(0x022F21D2 + (2 * i), "overlay_17", struct.pack("H", 0x0144))  # Also write collision

    for room in world.boss_slots:
        slot = world.boss_slots[room]
        boss = slot.new_boss
        data = world.boss_data[boss]

        if slot.old_boss == "Aguni":  # Aguni's data is here instead of in the arm9
            boss_file = "overlay_0"
        else:
            boss_file = "arm9"

        rom.write_to_file(slot.boss_address_pointer + 6, boss_file, bytearray([data.enemy_id]))  # Write the new boss into the room
        rom.write_to_file(0x2308B3c + data.flag_index, "overlay_41", struct.pack("H", slot.flag))  # Write the room's flag onto the new boss so the room still works properly
        address = base_enemy_address + (data.enemy_id * 0x24)
        rom.write_to_file(address + 26, "arm9", bytearray([slot.assigned_soul]))  # Give the enemy the boss slot soul so check logic still works
        var_a = 0
        var_b = 0
        x_pos = 0
        y_pos = 0
        if slot.old_boss == "Rahab" and boss != "Rahab":
            y_pos = 0xB0  # Make them not sink, some bosses will overwrite this anyways

        if boss == "Flying Armor":
            var_a = 1
            var_b = 1
            x_pos = (slot.room_width * 0x100) / 2  # Center horizontally
            y_pos = 0x50
        elif boss == "Balore":
            var_a = 1
            x_pos = 0x10
            y_pos = 0xB0
        elif boss == "Malphas":
            x_pos = (slot.room_width * 0x100) / 2  # Center horizontally
        elif boss == "Dario":
            x_pos = (slot.room_width * 0x100) / 2  # Center horizontally
            if slot.room_width == 1:
                rom.write_to_file(0x225BB6C, "overlay_1", struct.pack("I", 0xE1A02800))  # Halve Dario's teleport range so he doesn't go OOB.
        elif boss == "Dmitrii":
            x_pos = (slot.room_width * 0x100) / 2  # Center horizontally
        elif boss == "Puppet Master":
            var_a = 1
            x_pos = 0x100
            y_pos = 0x60
            if room == "Demon Guest House":  # If the room is vanilla, move him over for the shifted wall
                x_pos = 0x148
            elif room == "Subterranean Hell":
                y_pos = 0x70  # Move him down a bit so he's easier to hit in the tall room

            if room != "Demon Guest House":  # Update hardcoded position for some extra entities
                # Arms--------------------------------------------------
                rom.write_to_file(0x23052b0, "overlay_25", struct.pack("H", x_pos))
                rom.write_to_file(0x23052b2, "overlay_25", struct.pack("H", y_pos))
                # Iron maidens------------------------------------------
                rom.write_to_file(0x2305350, "overlay_25", struct.pack("H", x_pos + 0x68))
                rom.write_to_file(0x2305352, "overlay_25", struct.pack("H", y_pos - 0x38))

                rom.write_to_file(0x2305354, "overlay_25", struct.pack("H", x_pos + 0x68))
                rom.write_to_file(0x2305356, "overlay_25", struct.pack("H", y_pos + 0x38))

                rom.write_to_file(0x2305358, "overlay_25", struct.pack("H", x_pos - 0x68))
                rom.write_to_file(0x230535A, "overlay_25", struct.pack("H", y_pos - 0x38))

                rom.write_to_file(0x230535C, "overlay_25", struct.pack("H", x_pos - 0x68))
                rom.write_to_file(0x230535E, "overlay_25", struct.pack("H", y_pos + 0x38))
                # Platforms----------------------------------------------
                rom.write_to_file(0x23052e4, "overlay_25", struct.pack("H", x_pos + 0x68))
                rom.write_to_file(0x23052e6, "overlay_25", struct.pack("H", y_pos - 0x18))

                rom.write_to_file(0x23052e8, "overlay_25", struct.pack("H", x_pos - 0x68))
                rom.write_to_file(0x23052eA, "overlay_25", struct.pack("H", y_pos - 0x18))
                # Player Teleport----------------------------------------
                rom.write_to_file(0x2305370, "overlay_25", struct.pack("H", x_pos + 0x68))
                rom.write_to_file(0x2305372, "overlay_25", struct.pack("H", y_pos - 0x38 + 0x17))

                rom.write_to_file(0x2305374, "overlay_25", struct.pack("H", x_pos + 0x68))
                rom.write_to_file(0x2305376, "overlay_25", struct.pack("H", y_pos + 0x38 + 0x17))

                rom.write_to_file(0x2305378, "overlay_25", struct.pack("H", x_pos - 0x68))
                rom.write_to_file(0x230537A, "overlay_25", struct.pack("H", y_pos - 0x38 + 0x17))

                rom.write_to_file(0x230537C, "overlay_25", struct.pack("H", x_pos - 0x68))
                rom.write_to_file(0x230537E, "overlay_25", struct.pack("H", y_pos + 0x38 + 0x17))
                # Player damage effect------------------------------------
                rom.write_to_file(0x2305390, "overlay_25", struct.pack("H", x_pos + 0x68))
                rom.write_to_file(0x2305392, "overlay_25", struct.pack("H", y_pos - 0x38 + 0x14))

                rom.write_to_file(0x2305394, "overlay_25", struct.pack("H", x_pos + 0x68))
                rom.write_to_file(0x2305396, "overlay_25", struct.pack("H", y_pos + 0x38 + 0x14))

                rom.write_to_file(0x2305398, "overlay_25", struct.pack("H", x_pos - 0x68))
                rom.write_to_file(0x230539A, "overlay_25", struct.pack("H", y_pos - 0x38 + 0x14))

                rom.write_to_file(0x230539c, "overlay_25", struct.pack("H", x_pos - 0x68))
                rom.write_to_file(0x230539E, "overlay_25", struct.pack("H", y_pos + 0x38 + 0x14))

                # NOP out P.M's camera lock in other rooms
                rom.write_to_file(0x22FFC1C, "overlay_25", struct.pack("I", 0xE1A00000))
                rom.write_to_file(0x22ffa40, "overlay_25", struct.pack("I", 0xE1A00000))

        elif boss == "Gergoth":
            if room == "Condemned Tower":
                var_a = 1  # Falling Gergoth, for breaking the tower floors
            elif room == "The Pinnacle":
                x_pos = 0x40  # Outside mirror range
            elif room in ["Wizardry Lab", "Demon Guest House Upper", "Condemned Tower"]:
                x_pos = 0x30
        elif boss == "Zephyr":
            x_pos = (slot.room_width * 0x100) / 2  # Center horizontally
            if slot.room_width > 1:
                var_a = 1  # Normal Zephyr; Boss Rush is used to skip the scene if the room isn't wide enough.
        elif boss == "Bat Company":
            var_a = 1
            var_b = 0
        elif boss == "Rahab":
            if room != "Subterranean Hell":
                expand_rahab_room(rom, room)
        elif boss == "Paranoia":
            var_a = 2
            x_pos = 0x1F
            y_pos = 0x80
        elif boss == "Death":
            var_a = 1
            var_b = 1
            x_pos = (slot.room_width * 0x100) / 2  # Center horizontally
            y_pos = 0x50
        elif boss == "Abaddon":
            var_a = 1
            x_pos = 0x80
            y_pos = 0xB0

        x_pos = int(x_pos)  # Convert if it was centered
        # The X/Y pos here are overrides. If none is specified, use the vanilla value
        if x_pos:
            rom.write_to_file(slot.boss_address_pointer, boss_file, struct.pack("H", x_pos))

        if y_pos:
            rom.write_to_file(slot.boss_address_pointer + 2, boss_file, struct.pack("H", y_pos))

        rom.write_to_file(slot.boss_address_pointer + 8, boss_file, bytearray([var_a]))
        rom.write_to_file(slot.boss_address_pointer + 10, boss_file, bytearray([var_b]))
        stat_table = boss_stats[boss]
        scalar = boss_stats[slot.old_boss].scaling_factor
        stat_list = [
            "hp",
            "mp",
            "exp",
            "atk",
            "defns",
            "scaling_factor"
        ]
        for index, stat in enumerate(stat_table):

            stat_name = stat_list[index]
            new_stat = getattr(boss_stats[slot.old_boss], stat_list[index])  # TODO! Fix/revert

            if index == 5:
                continue  # don't scale the stat factor
            if index >= 3:  # atk, def
                new_stat = min(new_stat, 0xFF)
                rom.write_to_file(address + stat_offsets[index], "arm9", bytearray([new_stat]))
            else:  # HP, MP, EXP
                new_stat = min(new_stat, 0xFFFF)
                rom.write_to_file(address + stat_offsets[index], "arm9", struct.pack("H", new_stat))
            #print(f"! For {boss} at {room}, has {new_stat} {stat_list[index]}, scaled from {stat}")

        for pointer in data.seal_index_pointers:  # We change the Seal index instead of the Seal ID so Boss Doors can exist independently
            if pointer:
                rom.write_to_file(pointer, data.file, bytearray([slot.seal_index]))  # Ignore bosses that don't have a seal, i.e. Dario + Dmitrii
