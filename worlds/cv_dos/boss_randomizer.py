from dataclasses import dataclass
import struct

@dataclass
class DoSBoss:
    flag: int # The SLOT's Boss Defeated flag.
    assigned_soul: int # Which Soul is assigned to the SLOT's original boss. Soul randomization reworks how souls are given so this needs to stay the same.
    floor_height: int # The SLOT's room floor height
    room_width: int # The SLOT's room width
    boss_address_pointer: int # Which adress we write to to place the boss
    seal_index: int # Which seal this slot uses
    old_boss: str # Which boss is normally here
    new_boss: str = "None" # Which boss has been randomized to be here

@dataclass
class DoSBossData:
    enemy_id: int # The Enemy's internal ID number
    flag_index: int # Index used for writing boss flags
    seal_index_pointers: list[int] # Addresses for the seal index

base_enemy_address = 0x7CCAC  # I can't import this

def randomize_bosses(world):
    boss_pool = [
        "Puppet Master",
        "Rahab",  # We want to place these bosses first so that they can be fulfilled first
        "Balore",
        "Flying Armor",
        "Dimitrii",
        "Malphas",
        "Dario",
        "Gergoth",
        "Zephyr",
        "Bat Company",
        "Paranoia",
        "Aguni",
        "Death",
        "Abaddon"
    ]

    available_boss_slots = [
        "Lost Village",
        "Wizardry Lab",
        "Dark Chapel",
        "Dark Chapel Inner",
        "Garden of Madness",
        "Demon Guest House",
        "Condemned Tower",
        "Cursed Clock Tower",
        "Subterranean Hell",
        "Silenced Ruins",
        "Demon Guest House Upper",
        "The Pinnacle",
        "Mine of Judgment",
        "The Abyss"
    ]


    world.boss_slots = {
        "Lost Village": DoSBoss(0x02, 0x35, 1, 2, 0xA50B8, 1, "Flying Armor"),  # Flying Armor
        "Wizardry Lab": DoSBoss(0x04, 0x74, 1, 3, 0xAD0B0, 2, "Balore"),  # Balore
        "Dark Chapel": DoSBoss(0x08, 0xFF, 1, 2, 0xB2B58, 3, "Dimitrii"), # Dimitrii
        "Dark Chapel Inner": DoSBoss(0x10, 0x75, 2, 2, 0xB2B04, 4, "Malphas"),  # Malphas
        "Garden of Madness": DoSBoss(0x20, 0xFF, 1, 2, 0xB0500, 5, "Dario"),  # Dario 1 Make sure this is the right address for the flag. Seems low.
        "Demon Guest House": DoSBoss(0x40, 0x00, 1, 2, 0xA96F0, 6, "Puppet Master"),  # Puppet Master
        "Condemned Tower": DoSBoss(0x80, 0x57, 1, 1, 0xB5BE0, 7, "Gergoth"),  # Gergoth
        "Cursed Clock Tower": DoSBoss(0x0200, 0x01, 1, 2, 0xBCDA0, 9, "Zephyr"),  # Zephyr
        "Subterranean Hell": DoSBoss(0x0100, 0x77, 1, 2, 0xB8B1C, 8, "Rahab"),  # Rahab
        "Silenced Ruins": DoSBoss(0x0400, 0x36, 1, 1, 0xBA4B0, 10, "Bat Company"),  # Bat Company
        "Demon Guest House Upper": DoSBoss(0x1000, 0x02, 1, 1, 0xA99A8, 12, "Paranoia"), # Paranoia
        "The Pinnacle": DoSBoss(0x0800, 0x2B, 1, 2, 0x153FA8, 11, "Aguni"), # Aguni, not Dario 2
        "Mine of Judgment": DoSBoss(0x2000, 0x58, 1, 2, 0xB6360, 13, "Death"), # Death
        "The Abyss": DoSBoss(0x8000, 0x2C, 1, 1, 0xC2260, 15, "Abaddon") # Abaddon
    }

    world.boss_data = {
        "Flying Armor": DoSBossData(0x65, 0, [0x3807BC, 0x381764]),
        "Balore": DoSBossData(0x66, 2, [0x363D30, 0x364708]),
        "Malphas": DoSBossData(0x67, 6, [0x37D72C, 0x37E884]),
        "Dimitrii": DoSBossData(0x68, 4, [0]),
        "Dario": DoSBossData(0x69, 8, [0]),
        "Puppet Master": DoSBossData(0x6A, 10, [0x36A860, 0x36A958]),
        "Rahab": DoSBossData(0x6B, 14, [0x370388, 0x3704A0]),
        "Gergoth": DoSBossData(0x6C, 12, [0x39DAF0, 0x39EE40]),
        "Zephyr": DoSBossData(0x6D, 16, [0x38B740, 0x38D108]),
        "Bat Company": DoSBossData(0x6E, 18, [0x3A6AAC, 0x3A7370]),
        "Paranoia": DoSBossData(0x6F, 22, [0x39D630, 0x39A7B8]),
        "Aguni": DoSBossData(0x70, 20, [0x170994, 0x170B04]),
        "Death": DoSBossData(0x71, 24, [0x390100, 0x392920]),
        "Abaddon": DoSBossData(0x72, 26, [0x3B0EB0, 0x3B16FC])
    }

    rahab_pool = [
        "Flying Armor",
        # "Balore",  Removed for having too many graphical glitches
        "Puppet Master",
        "Rahab",
        "Bat Company",
        "Aguni",
        "Death"
    ]

    if not world.options.goal:
        rahab_pool.remove("Aguni")
        boss_pool.remove("Aguni")
        world.boss_slots.pop("The Pinnacle")

    if world.mine_status == "Disabled":
        #  Remove endgame bosses
        rahab_pool.remove("Death")

        boss_pool.remove("Death")
        boss_pool.remove("Abaddon")

        world.boss_slots.pop("Mine of Judgment")
        world.boss_slots.pop("The Abyss")

    rahab_boss = world.random.choice(rahab_pool)

    world.boss_slots["Subterranean Hell"].new_boss = rahab_boss  # Any other boss in Rahab's room will sink below the water level
    boss_pool.remove(rahab_boss)

    for boss in boss_pool:
        if boss == "Balore":
            # Balore needs to have a room with a 1-tile floor height, or there won't be room to dodge his laser attack
            valid_rooms = [room for room in world.boss_slots if world.boss_slots[room].new_boss == "None" and world.boss_slots[room].floor_height == 1]
        elif boss in ["Puppet Master", "Rahab"]:
             # Puppet Master and Rahab need to be in a room that is 2-tiles wide.
             # Puppet Master can teleport the player out of bounds, and Rahab would take an obnoxiously long time to be damagable.
            valid_rooms = [room for room in world.boss_slots if world.boss_slots[room].new_boss == "None" and world.boss_slots[room].room_width == 2]
        else:
            # All other combinations are valid
            valid_rooms = [room for room in world.boss_slots if world.boss_slots[room].new_boss == "None"]
            
        new_room = world.random.choice(valid_rooms)
        world.boss_slots[new_room].new_boss = boss

def write_bosses(world, rom):
    rom.write_bytes(0xAD0C1, bytearray([0x00]))  # Delete the Balore pre-boss cutscene, it breaks the game
    rom.write_bytes(0xB2B69, bytearray([0x00]))  # Delete the Malachi in Dimitrii's room used for the pre-boss cutscene
    rom.write_bytes(0x2F6DE38, bytearray([0x01]))  # Flag that Boss Shuffle is on, triggers some changes in the ROM
    rom.write_bytes(0xB2B75, bytearray([0x00]))  # Hider for Dimitrii's Quetzalcoatl
    copy_boss_stats(world, rom)

    if world.boss_slots["Demon Guest House"].new_boss != "Puppet Master":
        # Puppet master's wall is too thick for normal bosses to function, so we move it over
        for i in range(12):
            rom.copy_bytes(0x2A6472 + (0x40 * i), 0x14, 0x2A6460 + (0x40 * i)) # Layer 0

        for i in range(10):
            rom.copy_bytes(0x2A67D2 + (0x40 * i), 0x12, 0x2A67B2 + (0x40 * i)) # layer 1

    for room in world.boss_slots:
        slot = world.boss_slots[room]
        boss = slot.new_boss
        data = world.boss_data[boss]
        rom.write_bytes(slot.boss_address_pointer + 6, bytearray([data.enemy_id])) # Write the new boss into the room
        rom.write_bytes(0x2F6DE1C + data.flag_index, struct.pack("H", slot.flag)) # Write the room's flag onto the new boss so the room still works properly
        address = base_enemy_address + (data.enemy_id * 0x24)
        rom.write_bytes(address + 26, bytearray([slot.assigned_soul])) # Give the enemy the boss slot soul so check logic still works
        var_a = 0
        var_b = 0
        x_pos = 0
        y_pos = 0

        if boss == "Flying Armor":
            var_a = 1
            var_b = 1
            x_pos = (slot.room_width * 0x100) / 2 # Center horizontally
            y_pos = 0x50
        elif boss == "Balore":
            var_a = 1
            x_pos = 0x10
            y_pos = 0xB0
        elif boss == "Malphas":
            x_pos = (slot.room_width * 0x100) / 2 # Center horizontally
        elif boss == "Dario":
            x_pos = (slot.room_width * 0x100) / 2 # Center horizontally
            if slot.room_width == 1:
                rom.write_bytes(0x18876C, struct.pack("I", 0xE1A02800)) # Halve Dario's teleport range so he doesn't go OOB.
        elif boss == "Dimitrii":
            x_pos = (slot.room_width * 0x100) / 2 # Center horizontally
        elif boss == "Puppet Master":
            var_a = 1
            x_pos = 0x100
            y_pos = 0x60
            if room == "Demon Guest House": # If the room is vanilla, move him over for the shifted wall
                x_pos = 0x148
            elif room == "Subterranean Hell":
                y_pos = 0x70 # Move him down a bit so he's easier to hit in the tall room

            if room != "Demon Guest House": # Update hardcoded position for some extra entities
                # Arms--------------------------------------------------
                rom.write_bytes(0x36FEF0, struct.pack("H", x_pos))
                rom.write_bytes(0x36FEF2, struct.pack("H", y_pos))
                # Iron maidens------------------------------------------
                rom.write_bytes(0x36FF90, struct.pack("H", x_pos + 0x68))
                rom.write_bytes(0x36FF92, struct.pack("H", y_pos - 0x38))

                rom.write_bytes(0x36FF94, struct.pack("H", x_pos + 0x68))
                rom.write_bytes(0x36FF96, struct.pack("H", y_pos + 0x38))

                rom.write_bytes(0x36FF98, struct.pack("H", x_pos - 0x68))
                rom.write_bytes(0x36FF9A, struct.pack("H", y_pos - 0x38))

                rom.write_bytes(0x36FF9C, struct.pack("H", x_pos - 0x68))
                rom.write_bytes(0x36FF9E, struct.pack("H", y_pos + 0x38))
                # Platforms----------------------------------------------
                rom.write_bytes(0x36FF24, struct.pack("H", x_pos + 0x68))
                rom.write_bytes(0x36FF26, struct.pack("H", y_pos - 0x18))

                rom.write_bytes(0x36FF28, struct.pack("H", x_pos - 0x68))
                rom.write_bytes(0x36FF2A, struct.pack("H", y_pos - 0x18))
                # Player Teleport----------------------------------------
                rom.write_bytes(0x36FFB0, struct.pack("H", x_pos + 0x68))
                rom.write_bytes(0x36FFB2, struct.pack("H", y_pos - 0x38 + 0x17))

                rom.write_bytes(0x36FFB4, struct.pack("H", x_pos + 0x68))
                rom.write_bytes(0x36FFB6, struct.pack("H", y_pos + 0x38 + 0x17))

                rom.write_bytes(0x36FFB8, struct.pack("H", x_pos - 0x68))
                rom.write_bytes(0x36FFBA, struct.pack("H", y_pos - 0x38 + 0x17))

                rom.write_bytes(0x36FFBC, struct.pack("H", x_pos - 0x68))
                rom.write_bytes(0x36FFBE, struct.pack("H", y_pos + 0x38 + 0x17))
                # Player damage effect------------------------------------
                rom.write_bytes(0x36FFD0, struct.pack("H", x_pos + 0x68))
                rom.write_bytes(0x36FFD2, struct.pack("H", y_pos - 0x38 + 0x14))

                rom.write_bytes(0x36FFD4, struct.pack("H", x_pos + 0x68))
                rom.write_bytes(0x36FFD6, struct.pack("H", y_pos + 0x38 + 0x14))

                rom.write_bytes(0x36FFD8, struct.pack("H", x_pos - 0x68))
                rom.write_bytes(0x36FFDA, struct.pack("H", y_pos - 0x38 + 0x14))

                rom.write_bytes(0x36FFDC, struct.pack("H", x_pos - 0x68))
                rom.write_bytes(0x36FFDE, struct.pack("H", y_pos + 0x38 + 0x14))

                # NOP out P.M's camera lock in other rooms
                rom.write_bytes(0x36A85C, struct.pack("I", 0xE1A00000))
                rom.write_bytes(0x36A680, struct.pack("I", 0xE1A00000))

        elif boss == "Gergoth":
            if room == "Condemned Tower":
                var_a = 1 # Falling Gergoth, for breaking the tower floors
            elif room == "The Pinnacle":
                x_pos = 0x40 # Outside mirror range
        elif boss == "Zephyr":
            x_pos = (slot.room_width * 0x100) / 2 # Center horizontally
            if slot.room_width > 1:
                var_a = 1 # Normal Zephyr; Boss Rush is used to skip the scene if the room isn't wide enough.
        elif boss == "Bat Company":
            var_a = 1
            var_b = 0
        elif boss == "Paranoia":
            var_a = 2
            x_pos = 0x1F
            y_pox = 0x80
        elif boss == "Death":
            var_a = 1
            var_b = 1
            x_pos = (slot.room_width * 0x100) / 2 # Center horizontally
            y_pos = 0x50
        elif boss == "Abaddon":
            var_a = 1
            x_pos = 0x80
            y_pos = 0xB0

        x_pos = int(x_pos) # Convert if it was centered
        # The X/Y pos here are overrides. If none is specified, use the vanilla value
        if x_pos:
            rom.write_bytes(slot.boss_address_pointer, struct.pack("H", x_pos))

        if y_pos:
            rom.write_bytes(slot.boss_address_pointer + 2, struct.pack("H", y_pos))

        rom.write_bytes(slot.boss_address_pointer + 8, bytearray([var_a]))
        rom.write_bytes(slot.boss_address_pointer + 10, bytearray([var_b]))
        for pointer in data.seal_index_pointers:  # We change the Seal index instead of the Seal ID so Boss Doors can exist independently
            if pointer:
                rom.write_bytes(pointer, bytearray([slot.seal_index])) # Ignore bosses that don't have a seal, i.e. Dario + Dimitrii


        index = int(world.boss_data[slot.old_boss].flag_index / 2)
        rom.copy_bytes(0x3FFFCC0 + (index * 9), 9, address + 0x0E)  # Copy the SLOT'S original stats onto the new boss for balance
    
    for i in range(126):
        rom.write_bytes(0x3FFFCC0 + i, bytearray([0x00]))  # Clean up the copied data afterwards

def copy_boss_stats(world, rom):
    # Copy all boss stats into unused ROM so we can copy them back
    for boss in world.boss_data:
        data = world.boss_data[boss]
        index = int(data.flag_index / 2)
        address = base_enemy_address + (data.enemy_id * 0x24)
        rom.copy_bytes(address + 0x0E, 9, 0x3FFFCC0 + (9 * index))


# Test all bosses on all slots