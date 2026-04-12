import json
import logging
import pkgutil
import random

import yaml

import Utils
from settings import get_settings
from worlds.Files import APPatchExtension, APProcedurePatch, APTokenMixin

from ..common.patching.RomData import RomData
from ..common.patching.rooms.encoding import write_room_data
from ..common.patching.text.encoding import write_text_data
from ..common.patching.z80asm.Assembler import GameboyAddress, Z80Assembler, Z80Block
from ..data.Constants import ROM_HASH
from ..Options import OracleOfSeasonsLinkedHerosCave
from .Constants import CAVE_DATA, DEFINES, DUNGEON_ENTRANCES, DUNGEON_EXITS
from .data_manager.text import apply_ages_edits, get_modded_seasons_text_data
from .functions import (
    alter_treasure_types,
    apply_miscellaneous_options,
    define_additional_tile_replacements,
    define_collect_properties_table,
    define_compass_rooms_table,
    define_essence_sparkle_constants,
    define_foreign_item_data,
    define_location_constants,
    define_lost_woods_sequences,
    define_option_constants,
    define_samasa_combination,
    define_season_constants,
    define_tree_sprites,
    get_asm_files,
    inject_slot_name,
    randomize_ai_for_april_fools,
    set_character_sprite_from_settings,
    set_dungeon_warps,
    set_faq_trap,
    set_file_select_text,
    set_fixed_subrosia_seaside_location,
    set_heart_beep_interval_from_settings,
    set_old_men_rupee_values,
    set_player_start_inventory,
    set_portal_warps,
    write_chest_contents,
)
from .functions.room_edits import apply_room_edits
from .functions.text_edits import define_dungeon_items_text_constants, make_text_data
from .puzzle_rando import randomize_puzzles


class OoSPatchExtensions(APPatchExtension):
    game = "The Legend of Zelda - Oracle of Seasons"

    @staticmethod
    def apply_patches(caller: APProcedurePatch, rom: bytes, patch_file: str) -> bytes:
        from .. import OracleOfSeasonsWorld
        rom_data = RomData(rom)
        patch_data = json.loads(caller.get_file(patch_file).decode("utf-8"))

        version = patch_data["version"].split(".")
        world_version = OracleOfSeasonsWorld.world_version
        if int(version[0]) != world_version.major or int(version[1]) > world_version.minor:
            raise Exception(f"Invalid version: this patch was generated on v{patch_data['version']}, "
                            f"you are currently using v{world_version.as_simple_string()}")

        if patch_data["options"]["cross_items"]:
            file_name = get_settings().tloz_oos_options.ages_rom_file
            file_path = Utils.user_path(file_name)
            rom_file = open(file_path, "rb")
            ages_rom = bytes(rom_file.read())
            rom_file.close()

            for bank in range(0x40, 0x80):
                rom_data.add_bank(bank)
            rom_data.update_rom_size()
        else:
            ages_rom = b""

        # Initialize random seed with the one used for generation + the player ID, so that cosmetic stuff set
        # to "random" always generate the same for successive patchings for a given slot
        seed: int = patch_data["seed"]
        random.seed(seed + caller.player)

        assembler = Z80Assembler(CAVE_DATA, DEFINES, rom, ages_rom)
        dictionary, texts = get_modded_seasons_text_data(rom_data)
        if patch_data["options"]["cross_items"]:
            if texts["TX_0053"] == "":  # Check if cane text exists
                # If not, add the Ages texts
                apply_ages_edits(texts, RomData(ages_rom))

        # Generate dungeon entrance/exit data
        dungeon_entrances = dict(DUNGEON_ENTRANCES)
        dungeon_exits = dict(DUNGEON_EXITS)
        if patch_data["options"]["linked_heros_cave"] & OracleOfSeasonsLinkedHerosCave.samasa:
            dungeon_entrances["d11"] = {
                "map_tile": 0xcf,
                "room": 0xcf,
                "group": 0x00,
                "position": 0x55
            }
        if patch_data["options"]["linked_heros_cave"]:
            dungeon_exits["d11"] = GameboyAddress(0x04, 0x7b35).address_in_rom()
        room_data = apply_room_edits(rom_data, patch_data)

        # Define assembly constants & floating chunks
        item_data = define_foreign_item_data(assembler, texts, patch_data)
        define_location_constants(assembler, patch_data, item_data)
        define_option_constants(assembler, patch_data)
        define_season_constants(assembler, patch_data)
        make_text_data(assembler, texts, patch_data)
        define_compass_rooms_table(assembler, patch_data, item_data)
        define_collect_properties_table(assembler, patch_data, item_data)
        define_additional_tile_replacements(assembler, patch_data)
        define_samasa_combination(assembler, patch_data)
        define_dungeon_items_text_constants(texts, patch_data)
        define_essence_sparkle_constants(assembler, patch_data, dungeon_entrances)
        define_lost_woods_sequences(assembler, texts, patch_data)
        define_tree_sprites(assembler, patch_data, item_data)
        set_file_select_text(assembler, caller.player_name)
        set_player_start_inventory(assembler, patch_data)
        randomize_puzzles(rom_data, assembler, room_data, patch_data)
        if not hasattr(get_settings().tloz_oos_options, "beat_tutorial"):
            set_faq_trap(assembler)

        # Parse assembler files, compile them and write the result in the ROM
        logging.info("Compiling ASM files...")
        write_text_data(rom_data, dictionary, texts, True)
        write_room_data(rom_data, room_data, True)
        for file_path in get_asm_files(patch_data):
            yaml_data = pkgutil.get_data(__name__, file_path)
            if yaml_data is None:
                raise OSError(f"Could not load asm file: {file_path}")
            data_loaded = yaml.safe_load(yaml_data)
            for metalabel, contents in data_loaded.items():
                assembler.add_block(Z80Block(metalabel, contents))
        assembler.compile_all()
        for block in assembler.blocks:
            rom_data.write_bytes(block.addr.address_in_rom(), block.byte_array)

        if patch_data["options"]["linked_heros_cave"] & OracleOfSeasonsLinkedHerosCave.samasa:
            dungeon_entrances["d11"]["addr"] = assembler.global_labels["warpSourceDesert"].address_in_rom() + 2

        # Perform direct edits on the ROM
        alter_treasure_types(rom_data, item_data)
        write_chest_contents(rom_data, patch_data, item_data)
        set_old_men_rupee_values(rom_data, patch_data)
        set_dungeon_warps(rom_data, patch_data, dungeon_entrances, dungeon_exits)
        set_portal_warps(rom_data, patch_data)
        apply_miscellaneous_options(rom_data, patch_data)
        set_fixed_subrosia_seaside_location(rom_data, patch_data)
        if patch_data["options"]["randomize_ai"]:
            randomize_ai_for_april_fools(rom_data)

        # Apply cosmetic settings
        set_heart_beep_interval_from_settings(rom_data)
        set_character_sprite_from_settings(rom_data)
        inject_slot_name(rom_data, caller.player_name)

        rom_data.update_header_checksum()
        rom_data.update_checksum(0x14e)
        return rom_data.output()


class OoSProcedurePatch(APProcedurePatch, APTokenMixin):
    hash = (ROM_HASH,)
    patch_file_ending: str = ".apoos"
    result_file_ending: str = ".gbc"

    game = "The Legend of Zelda - Oracle of Seasons"
    procedure = (
        ("apply_patches", ["patch.json"]),
    )

    @classmethod
    def get_source_data(cls) -> bytes:
        base_rom_bytes = getattr(cls, "base_rom_bytes", None)
        if not base_rom_bytes:
            file_name = get_settings().tloz_oos_options.rom_file
            file_name = Utils.user_path(file_name)

            rom_file = open(file_name, "rb")
            base_rom_bytes = bytes(rom_file.read())
            rom_file.close()

            cls.base_rom_bytes = base_rom_bytes
        return base_rom_bytes
