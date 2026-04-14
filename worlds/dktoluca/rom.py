import typing
import Utils
import hashlib
import os
import json
import settings
import base64

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import DKC3World

from .enums import Regions
from .constants import *

from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes, APPatchExtension

HASH_US = '120abf304f0c40fe059f6a192ed4f947'

valid_letters = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 
    'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 
    'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', 
    '4', '5', '6', '7', '8', '9', " "
]

letters_addr = [
    0xABAD,
    0xABAE,
    0xABB3,
    0xABB4,
    0xABB9,
]

def sanitize_save_name(text: str) -> str:
    result = ""
    for letter in text:
        if letter not in valid_letters:
            result += " "
        else:
            result += letter
    return result

class DKC3PatchExtension(APPatchExtension):
    game = GAME_NAME

    @staticmethod
    def shuffle_levels(caller: APProcedurePatch, rom: bytes) -> bytes:
        unshuffled_rom = bytearray(rom)
        rom = bytearray(rom)
        level_data = base64.b64decode(caller.get_file("levels.bin").decode("UTF-8"))
        rom_connections: dict[str, list[str, int]] = json.loads(level_data)

        from .levels import level_rom_data #, boss_rom_data
        dkc3_level_rom_data = level_rom_data

        for level, selected_level in rom_connections.items():
            if level not in dkc3_level_rom_data.keys():
                continue

            selected_name = selected_level[0]
            selected_addr = dkc3_level_rom_data[selected_name]
            selected_name_id = unshuffled_rom[selected_addr]
            selected_level_id = unshuffled_rom[selected_addr+1]

            dest_addr = dkc3_level_rom_data[level]
            rom[dest_addr] = selected_name_id
            rom[dest_addr+1] = selected_level_id

        return bytes(rom)


class DKC3ProcedurePatch(APProcedurePatch, APTokenMixin):
    hash = [HASH_US]
    game = GAME_NAME
    patch_file_ending = ".aptoluca"
    result_file_ending = ".sfc"
    name: bytearray
    procedure = [
        ("apply_tokens", ["token_patch.bin"]),
        ("apply_bsdiff4", ["dkc3_basepatch.bsdiff4"]),
        ("shuffle_levels", []),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

    def write_byte(self, offset: int, value: int):
        self.write_token(APTokenTypes.WRITE, offset, value.to_bytes(1, "little"))

    def write_bytes(self, offset: int, value: typing.Iterable[int]):
        self.write_token(APTokenTypes.WRITE, offset, bytes(value))

def patch_rom(world: "DKC3World", patch: DKC3ProcedurePatch):
    # Write additional data for generation
    data_dict = {
        "seed": world.random.getrandbits(64),
    }
    patch.write_file("data.json", json.dumps(data_dict).encode("UTF-8"))

    # Edit the ROM header
    from Utils import __version__
    patch.name = bytearray(f'DKCT{__version__.replace(".", "")[0:3]}_{world.player}_{world.multiworld.seed:11}\0', 'utf8')[:21]
    patch.name.extend([0] * (21 - len(patch.name)))
    patch.write_bytes(0xFFC0, patch.name)

    patch.write_byte(0x3AFF00, world.options.starting_kong.value)
    patch.write_byte(0x3AFF01, world.options.energy_link.value)
    #patch.write_byte(0x3AFF02, world.options.trap_link.value)
    #patch.write_byte(0x3AFF03, world.options.death_link.value)
    patch.write_byte(0x3AFF04, world.options.goal.value)
    patch.write_byte(0x3AFF05, world.options.required_birds.value)
    patch.write_byte(0x3AFF06, world.options.required_lake_levels.value)
    patch.write_byte(0x3AFF07, world.options.required_forest_levels.value)
    patch.write_byte(0x3AFF08, world.options.required_cove_levels.value)
    patch.write_byte(0x3AFF09, world.options.required_mekanos_levels.value)
    patch.write_byte(0x3AFF0A, world.options.required_k3_levels.value)
    patch.write_byte(0x3AFF0B, world.options.required_ridge_levels.value)
    patch.write_byte(0x3AFF0C, world.options.required_kore_levels.value)
    patch.write_byte(0x3AFF0D, world.options.required_krematoa_levels.value)
    patch.write_byte(0x3AFF0E, world.options.dk_coin_checks.value)
    patch.write_byte(0x3AFF0F, world.options.kong_checks.value)
    patch.write_byte(0x3AFF10, world.options.balloon_checks.value)
    patch.write_byte(0x3AFF11, world.options.banana_checks.value)
    patch.write_byte(0x3AFF12, world.options.coin_checks.value)
    patch.write_byte(0x3AFF13, world.options.bird_checks.value)
    patch.write_byte(0x3AFF14, world.options.starting_life_count.value)

    order = [
        Regions.belchas_barn_level,
        Regions.lakeside_limbo_level,
        Regions.doorstop_dash_level,
        Regions.tidal_trouble_level,
        Regions.skiddas_row_level,
        Regions.murky_mill_level,
        Regions.arichs_ambush_level,
        Regions.barrel_shield_bust_up_level,
        Regions.riverside_race_level,
        Regions.squeals_on_wheels_level,
        Regions.springing_spiders_level,
        Regions.bobbing_barrel_brawl_level,
        Regions.squirt_showdown_level,
        Regions.bazzas_blockade_level,
        Regions.rocket_barrel_ride_level,
        Regions.kreeping_klasps_level,
        Regions.tracker_barrel_trek_level,
        Regions.fish_food_frenzy_level,
        Regions.kaos_karnage_level,
        Regions.fireball_frenzy_level,
        Regions.demolition_drain_pipe_level,
        Regions.ripsaw_rage_level,
        Regions.blazing_bazukas_level,
        Regions.low_g_labyrinth_level,
        Regions.bleaks_house_level,
        Regions.krevice_kreepers_level,
        Regions.tearaway_toboggan_level,
        Regions.barrel_drop_bounce_level,
        Regions.krackshot_krock_level,
        Regions.lemguin_lunge_level,
        Regions.barbos_barrier_level,
        Regions.buzzer_barrage_level,
        Regions.kongfused_cliffs_level,
        Regions.floodlit_fish_level,
        Regions.pot_hole_panic_level,
        Regions.ropey_rumpus_level,
        Regions.kastle_kaos_level,
        Regions.konveyor_rope_klash_level,
        Regions.creepy_caverns_level,
        Regions.lightning_look_out_level,
        Regions.koindozer_klamber_level,
        Regions.poisonous_pipeline_level,
        Regions.knautilus_level,
        Regions.stampede_sprint_level,
        Regions.criss_kross_cliffs_level,
        Regions.tyrant_twin_tussle_level,
        Regions.swoopy_salvo_level,
        Regions.rocket_rush_level,
    ]

    for idx, map_level in enumerate(order):
        if map_level == Regions.skiddas_row_level:
            patch.write_bytes(0x3AFF40+(idx*2), (0x2B).to_bytes(2, "little"))
        elif map_level == Regions.knautilus_level:
            patch.write_bytes(0x3AFF40+(idx*2), (0x24).to_bytes(2, "little"))
        elif map_level == Regions.kastle_kaos_level:
            patch.write_bytes(0x3AFF40+(idx*2), (0x23).to_bytes(2, "little"))
        else:
            shuffled_level: int = world.rom_connections[map_level][1]
            patch.write_bytes(0x3AFF40+(idx*2), shuffled_level.to_bytes(2, "little"))

    # Initialize save name
    save_name = world.options.default_save_name.value[:5].upper()
    if len(save_name) == 0:
        save_name = "DIXIE"
    save_name = sanitize_save_name(save_name)

    patch.write_byte(letters_addr[0], 0x20)
    patch.write_byte(letters_addr[1], 0x20)
    patch.write_byte(letters_addr[2], 0x20)
    patch.write_byte(letters_addr[3], 0x20)
    patch.write_byte(letters_addr[4], 0x20)

    for idx, letter in enumerate(save_name):
        patch.write_byte(letters_addr[idx], ord(letter))
    else:
        patch.write_byte(letters_addr[idx], ord(letter) | 0x80)

    # Save shuffled levels data
    json_levels = json.dumps(world.rom_connections).encode("UTF-8")
    patch.write_file("levels.bin", base64.b64encode(json_levels))
    
    patch.write_file("token_patch.bin", patch.get_token_binary())

def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(Utils.read_snes_rom(open(file_name, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if basemd5.hexdigest() not in {HASH_US}:
            raise Exception('Supplied Base Rom does not match known MD5 for US 1.0 release. '
                            'Get the correct game and version, then dump it')
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    options: settings.Settings = settings.get_settings()
    if not file_name:
        file_name = options["dkc3_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
