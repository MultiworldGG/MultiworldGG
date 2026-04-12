import hashlib
import os
import Utils
import typing
import struct
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes, APPatchExtension
from typing import Sequence
from .in_game_data import (global_weapon_table, base_weapons, valid_random_starting_weapons, global_soul_table,
                           base_check_address_table, easter_egg_table, warp_room_bits, world_version, global_item_table, common_filler_pool,
                           boss_list, enemy_table, button_item_table)
from .music_randomizer import area_music_randomizer, boss_music_randomizer
from .boss_randomizer import write_bosses
from .synthesis_randomizer import write_synthesis
from .bullet_wall_randomizer import apply_souls_and_gfx
from Options import OptionError
from .Options import StartingWeapon, SoulRandomizer, SoulsanityLevel, GateItems
from .Items import soul_filler_table
from .seal_shuffle import write_seals, randomize_seal_patterns
from .set_goals import write_goal_triggers
from BaseClasses import ItemClassification

hash_us = "cc0f25b8783fb83cb4588d1c111bdc18"

base_enemy_address = 0x7CCAC
soul_check_table = 0x2F6DC50
button_check_table = 0x2F6DE0C


class LocalRom(object):

    def __init__(self, file: bytes, name: str | None = None) -> None:
        self.file = bytearray(file)
        self.name = name

    def read_byte(self, offset: int) -> int:
        return self.file[offset]

    def read_bytes(self, offset: int, length: int) -> bytes:
        return self.file[offset:offset + length]

    def write_bytes(self, offset: int, values: Sequence[int]) -> None:
        self.file[offset:offset + len(values)] = values

    def get_bytes(self) -> bytes:
        return bytes(self.file)


def patch_rom(world, rom, player: int, code_patch):
    # This is the entirety of the patched code
    rom.write_bytes(0x2F6DC50, code_patch)

    write_goal_triggers(world, rom)

    weapon = world.options.starting_weapon.value


    if isinstance(weapon, str):
        if weapon not in global_weapon_table:
            raise OptionError(f"Error generating for player {world.player_name}. Attempted to set an invalid starting weapon: {weapon}.")
    else:
        if weapon == StartingWeapon.option_random_base:
            weapon = world.random.choice(base_weapons)
        else:
            weapon = world.random.choice(valid_random_starting_weapons)

    starting_weapon = global_weapon_table.index(weapon)

    # Options handling
    rom.write_bytes(0x122E88, bytearray([starting_weapon]))

    warp_room = warp_room_bits[world.starting_warp_room]
    rom.write_bytes(0x2F6DD4E, struct.pack("H", warp_room))  # The initial warp room bit

    if world.options.replace_menace_with_soma:
        rom.copy_bytes(0x158C3C, 8, 0x158C34)  # Replace the menace warp coords with soma's

    if world.options.remove_money_gates:
        rom.write_bytes(0xAD661, bytearray([0x00]))
        rom.write_bytes(0xB0A2D, bytearray([0x00]))
        rom.write_bytes(0xBD135, bytearray([0x00]))

    if world.options.disable_boss_seals:
        rom.write_bytes(0x11EA18, bytearray([0x00]))
        rom.write_bytes(0x140A24, bytearray([0x01, 0x00, 0xA0, 0xE3]))

    if world.options.reveal_map:
        rom.write_bytes(0x260C7, bytearray([0xE1, 0x00, 0x00, 0xA0, 0xE1]))
        rom.write_bytes(0x28BE8, bytearray([0x00, 0x00, 0xE0, 0xE3, 0x1E, 0xFF, 0x2F]))

    if world.options.open_drawbridge:
        rom.write_bytes(0x0CF046, bytearray([0xA0, 0xE1]))  # Make the drawbridge always be down

    if world.options.fix_luck:
        rom.write_bytes(0xF087D, bytearray([0x22]))
        rom.write_bytes(0xF0888, bytearray([0x02, 0x70]))
        rom.write_bytes(0xF088D, bytearray([0x71]))
        rom.write_bytes(0xF0890, bytearray([0x00, 0x00]))
        rom.write_bytes(0xF0893, bytearray([0xE1]))
        rom.write_bytes(0xF089A, bytearray([0xA0, 0xE3]))
        rom.write_bytes(0xF08BE, bytearray([0x87, 0xE0]))
        rom.write_bytes(0xF09A0, bytearray([0x00, 0x00, 0xA0, 0xE1]))
        rom.write_bytes(0xF09C8, bytearray([0x02, 0x0A]))
        rom.write_bytes(0xF09CB, bytearray([0xE3]))
        rom.write_bytes(0xF09F0, bytearray([0x47, 0x91, 0x80, 0xE0]))
        rom.write_bytes(0xF0A00, bytearray([0x89]))
        rom.write_bytes(0xF0A04, bytearray([0x02, 0x0A]))
        rom.write_bytes(0xF0A07, bytearray([0xE3]))

    if world.options.reveal_hidden_walls:
        rom.write_bytes(0xA5231, bytearray([0x00]))
        rom.write_bytes(0xA57AD, bytearray([0x00]))
        rom.write_bytes(0xAA45D, bytearray([0x00]))
        rom.write_bytes(0xAD3E5, bytearray([0x00]))
        rom.write_bytes(0xB0199, bytearray([0x00]))
        rom.write_bytes(0xBEE21, bytearray([0x00]))
        rom.write_bytes(0xBEE8D, bytearray([0x00]))
        rom.write_bytes(0xBEFC5, bytearray([0x00]))
        rom.write_bytes(0xB84A9, bytearray([0x00]))

    if not world.options.goal:  # Remove the better ending trigger and replace Dario with Menace
        rom.write_bytes(0xBD508, bytearray([0x60, 0xDC])) #  ???
        rom.write_bytes(0xBD50E, bytearray([0xFF, 0xFE, 0xD0, 0xFF]))
        rom.write_bytes(0xC1C30, bytearray([0xD4, 0x94]))
        rom.write_bytes(0xC1C38, bytearray([0xD0]))
        #rom.write_bytes(0xB05A1, bytearray([0x00]))

        ####  Wall off the final boss door in the Abyss
        rom.write_bytes(0x2DE0DC, bytearray([0x2F]))
        rom.write_bytes(0x2DE11C, bytearray([0x3F]))
        rom.write_bytes(0x2DE15C, bytearray([0x4F]))
        rom.write_bytes(0x2DE19C, bytearray([0x5F]))
        rom.write_bytes(0x2DE1DC, bytearray([0x5F]))
        rom.write_bytes(0x2DE21C, bytearray([0x41]))
        ######

        rom.write_bytes(0x2F6DDFD, bytearray([0xFF])) # Remove Death, Abaddon, and Aguni from the Soulstiary
        rom.write_bytes(0x2F6DDFE, bytearray([0xFF])) # IF MINE IS REMOVED!!!!
        rom.write_bytes(0x2F6DE02, bytearray([0xFF]))

    #if world.options.goal == 2:
        #rom.write_bytes(0x2F6DD48, bytearray([0x01]))  # Abyss plus mode, flags the Garden event as requiring Aguni to be defeated

    if world.options.one_screen_mode:
        rom.write_bytes(0x2F6DD4C, bytearray([0x01]))

    if world.options.boost_speed:
        rom.write_bytes(0x15B2A9, bytearray([0x20]))

    if world.options.death_link:
        rom.write_bytes(0x2F6DD8D, bytearray([0x01]))

    if world.options.no_mp_bat:
        rom.write_bytes(0xA1782, bytearray([0x00])) # Zero the Bat's MP cost
        
    if world.options.randomize_seal_patterns:
        randomize_seal_patterns(world, rom)

    rom.write_bytes(0x2F6DD8E, struct.pack("H", world.options.experience_percentage))

    rom.write_bytes(0x2F6DD90, struct.pack("H", world.options.soul_drop_percentage))
    soul_total = set(world.common_souls)
    if world.options.soulsanity_level:
        soul_total |= world.uncommon_souls

    if world.options.soulsanity_level == SoulsanityLevel.option_rare:
        soul_total |= world.rare_souls
    soul_total = list(soul_total)

    for i, soul in enumerate(soul_total):  # Fill IDs of souls in the loc pool
        rom.write_bytes(0x2F6DD94 + i, bytearray([global_soul_table.index(soul)]))

    if world.options.soul_randomizer == SoulRandomizer.option_shuffled:
        vanilla_souls = [soul for soul in world.important_souls if soul not in world.excluded_static_souls]

        shuffled_keys = [item for item in soul_filler_table.copy() if item not in vanilla_souls]  # Will this break with Aguni/Abaddon since they're not filler?
        souls_output = {key: key for key in soul_filler_table.copy()}  # this is assuming all vanilla souls are in soul_filler_table
        shuffled_vals = world.random.sample(shuffled_keys, k=len(shuffled_keys))
        for key, val in zip(shuffled_keys, shuffled_vals):
            souls_output[key] = val

        for soul in souls_output:
            soul_data = bytearray([global_soul_table.index(souls_output[soul]), 0x05])
            rom.write_bytes(soul_check_table + (global_soul_table.index(soul) * 2), soul_data)

    elif world.options.soul_randomizer == SoulRandomizer.option_soulsanity:
        rom.write_bytes(0x2F6DD49, bytearray([0x01]))

    if world.options.shop_randomizer:
        shop_pool = common_filler_pool.copy()
        shop_pool = [item for item in shop_pool if item not in ["Potion", "Mind Up", "Claymore"]]
        for i in range(10):
            # Shop pool 2
            item = world.random.choice(shop_pool)
            rom.write_bytes(0xA1F14 + i, bytearray([global_item_table.index(item) + 1]))
            shop_pool.remove(item)

        for i in range(18):
            # Shop pool 1
            item = world.random.choice(shop_pool)
            rom.write_bytes(0xA1F38 + i, bytearray([global_item_table.index(item) + 1]))
            shop_pool.remove(item)

        for i in range(19):
            # Starting shop
            item = world.random.choice(shop_pool)
            rom.write_bytes(0xA1F4F + i, bytearray([global_item_table.index(item) + 1]))
            shop_pool.remove(item)

        # Claymore should always be available for breakable walls
        rom.write_bytes(0xA1F4E, bytearray([global_item_table.index("Claymore") + 1]))

    if world.options.shuffle_enemy_drops:
        drop_pool = common_filler_pool.copy()
        for enemy in enemy_table:
            if enemy in boss_list:  # We don't want to shuffle drops for bosses
                continue

            index = (base_enemy_address + (enemy_table.index(enemy) * 0x24))
            common_drop_address = index + 8
            rare_drop_address = index + 10
            if world.random.randint(0, 99) < 45:
                # Common drop
                item = world.random.choice(drop_pool)
                common_item = global_item_table.index(item) + 1
            else:
                common_item = 0

            if world.random.randint(0, 99) < 29:
                # Rare drop
                item = world.random.choice(drop_pool)
                rare_item = global_item_table.index(item) + 1
            else:
                rare_item = 0

            rom.write_bytes(common_drop_address, bytearray([common_item]))
            rom.write_bytes(rare_drop_address, bytearray([rare_item]))

    write_synthesis(world, rom)
    write_seals(world, rom)

    if world.options.boss_shuffle:
        write_bosses(world, rom)

    if world.options.area_music_randomizer:
        area_music_randomizer(world, rom)

    if world.options.boss_music_randomizer:
        boss_music_randomizer(world, rom)

    if world.options.randomize_red_soul_walls:
        rom.write_bytes(0x2F6DE08, bytearray([0x01])) # Tell the rom we have this on

        rom.write_bytes(0x158BC0, bytearray([global_soul_table.index(world.red_soul_walls[0])]))
        rom.write_bytes(0x158BBA, bytearray([global_soul_table.index(world.red_soul_walls[1])]))
        rom.write_bytes(0x158BB4, bytearray([global_soul_table.index(world.red_soul_walls[2])]))
        rom.write_bytes(0x158BC6, bytearray([global_soul_table.index(world.red_soul_walls[3])]))

    if world.options.gate_items == GateItems.option_buttonsanity:
        rom.write_bytes(0x2F6DE09, bytearray([0x01])) # Enables Button Check Mode

    if world.options.hard_mode:
        rom.write_bytes(0x2F6DE0A, bytearray([0x01])) # Hard mode set

    if world.options.passive_soul_eater_ring:
        rom.write_bytes(0x2F6DE0B, bytearray([0x01])) # Passive souls

    for location in world.multiworld.get_locations(player):
        item_type = 0
        item_id = 0
        
        if location.address:
            if location.item.player == world.player:   # If this is an item for the player, we need to extract it's Type and ID
                item_type = (location.item.code & 0xFF00) >> 8
                item_id = location.item.code & 0x00FF
            else:  # AP items are item type 2 and then use ID for progression.
                item_type = 2
                if ItemClassification.progression in location.item.classification:
                    item_id = 0x0C3B
                elif ItemClassification.useful in location.item.classification:
                    item_id = 0x073A
                elif ItemClassification.trap in location.item.classification:
                    item_id = 0x063A
                else:
                    item_id = 0x093A

        if location.address:  # Filter out events
            if location.name in global_soul_table:
                if location.item.player != world.player:
                    # AP items on souls can use the Type as the color
                    item_type = (item_id & 0xFF00) >> 8
                    item_id = item_id & 0xFF
                item_struct = (item_type << 8) | item_id
                index = (global_soul_table.index(location.name) * 2)
                rom.write_bytes(soul_check_table + index, struct.pack("H", item_struct))
            elif location.name in easter_egg_table:
                if item_id > 0xFF: # If this has a color
                    item_type = (item_id & 0xFF00) >> 8 # Replace the type with the color if it has one
                    item_id = item_id & 0xFF
                rom.write_bytes(easter_egg_table[location.name][0], bytearray([item_type]))
                rom.write_bytes(easter_egg_table[location.name][1], bytearray([item_id]))
            elif location.name in button_item_table:
                address = button_check_table + (button_item_table.index(location.name) * 4) # Set the address
                item_color = item_id >> 8
                item_id = item_id & 0xFF
                rom.write_bytes(address, bytearray([item_type, item_id, item_color]))

            else:
                # Regular item checks
                address = base_check_address_table[location.name]
                if location.item.name in global_soul_table and location.item.player == world.player:
                    rom.write_bytes(address + 9, bytearray([item_id]))  # High byte of the flag is used as Soul /Color ID
                    rom.write_bytes(address + 10, bytearray([0x3C]))
                    item_type = 2
                else:
                    rom.write_bytes(address + 9, struct.pack(">H", item_id))
                rom.write_bytes(address + 6, bytearray([item_type]))

    rom.name = f"{world.player}_{world.auth_id}"
    patch_name = rom.name + "\0"
    patch_name = bytearray(rom.name, "utf8")[:0x14]
    rom.write_bytes(0x2F6DD50, patch_name)
    rom.write_bytes(0x2F6DD7C, world_version.encode("ascii"))

    rom.write_file("token_patch.bin", rom.get_token_binary())


class DoSProcPatch(APProcedurePatch, APTokenMixin):
    hash = hash_us
    game = "Castlevania: Dawn of Sorrow"
    patch_file_ending = ".apcvdos"
    result_file_ending = ".nds"
    name: bytearray
    procedure = [
        ("apply_bsdiff4", ["dos_base.bsdiff4"]),
        ("apply_tokens", ["token_patch.bin"]),
        ("adjust_item_positions", []),
        ("apply_modifiers", []),
        ("modify_soulwall_gfx", [])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

    def write_bytes(self, offset: int, value: typing.Iterable[int]) -> None:
        self.write_token(APTokenTypes.WRITE, offset, bytes(value))
    
    def copy_bytes(self, source: int, amount: int, destination: int) -> None:
        self.write_token(APTokenTypes.COPY, destination, (amount, source))


class DoSPatchExtensions(APPatchExtension):
    game = "Castlevania: Dawn of Sorrow"

    @staticmethod
    def adjust_item_positions(caller: APProcedurePatch, rom: bytes) -> bytes:
        rom = LocalRom(rom)
        version_check = rom.read_bytes(0x2F6DD7C, 15)
        version = version_check.rstrip(b"\x69")
        version = version.decode("ascii")
        if version != world_version:  # Installed world is different from generated world
            raise Exception(f"Error! this patch was generated on Dawn of Sorrow APworld version: {version}, but installed APworld is version: {world_version}. " +
                            f"Please use APWorld version {version} to patch your game.")

        for check in base_check_address_table:
            address = base_check_address_table[check]
            item_type = int.from_bytes(rom.read_bytes(address + 6, 1))
            item_id = int.from_bytes(rom.read_bytes(address + 10, 1))
            if (item_type == 0x01 and item_id < 4) or (item_type == 0x02 and item_id >= 0x3D):
                # Coins and Magic Seals spawn slightly in the ground, so we need to raise them up a little bit
                y_pos = int.from_bytes(rom.read_bytes(address + 2, 2), byteorder="little")
                y_pos -= 10
                rom.write_bytes(address + 2, struct.pack("H", y_pos))

        return rom.get_bytes()

    @staticmethod
    def apply_modifiers(caller: APProcedurePatch, rom: bytes) -> bytes:
        rom = LocalRom(rom)
        exp_multiplier = struct.unpack("H", rom.read_bytes(0x2F6DD8E, 2))[0]  # Read the multiplier
        exp_multiplier = exp_multiplier / 100

        soul_chance_multiplier = struct.unpack("H", rom.read_bytes(0x2F6DD90, 2))[0]
        soul_chance_multiplier = soul_chance_multiplier / 100

        for enemy in enemy_table:
            address = (base_enemy_address + (enemy_table.index(enemy) * 0x24))
            exp_address = address + 18  # Offset where EXP is stored
            exp = rom.read_bytes(exp_address, 2)
            exp = struct.unpack("H", exp)[0]
            exp = int(min(0xFFFF, (exp * exp_multiplier)))
            rom.write_bytes(exp_address, struct.pack("H", exp))

            soul_chance_address = address + 20
            soul_chance = int.from_bytes(rom.read_bytes(soul_chance_address, 1))
            if soul_chance:  # Only modify non-guaranteed Souls
                soul_chance = int(min(0xFF, (soul_chance * soul_chance_multiplier)))
                rom.write_bytes(soul_chance_address, bytearray([soul_chance]))

        return rom.get_bytes()

    @staticmethod
    def modify_soulwall_gfx(caller: APProcedurePatch, rom: bytes) -> bytes:
        rom = LocalRom(rom)
        soul_wall_randomizer = int.from_bytes(rom.read_bytes(0x2F6DE08, 1))
        if soul_wall_randomizer:
            apply_souls_and_gfx(rom)
        return rom.get_bytes()



def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(Utils.read_snes_rom(open(file_name, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if hash_us != basemd5.hexdigest():
            raise Exception('Supplied Base Rom does not match known MD5 for US release. '
                            'Get the correct game and version, then dump it')
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    from worlds.cv_dos import DoSWorld
    if not file_name:
        file_name = DoSWorld.settings.rom_file
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
