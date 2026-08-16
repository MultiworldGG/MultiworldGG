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

from .enums import Regions, Events
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

trade_items_data = {
    Events.item_shell.value:    (0x04, 0x02),
    Events.item_mirror.value:   (0x08, 0x03),
    Events.item_present.value:  (0x10, 0x04),
    Events.item_ball.value:     (0x20, 0x05),
    Events.item_flower.value:   (0x40, 0x06),
    Events.item_wrench.value:   (0x80, 0x07),
}

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

    @staticmethod
    def handle_trading(caller: APProcedurePatch, rom: bytes) -> bytes:
        rom = bytearray(rom)
        trade_data = base64.b64decode(caller.get_file("trade.bin").decode("UTF-8"))
        trade_items: dict[str, str] = json.loads(trade_data)

        # Handle Bazaar #1
        item_name = trade_items[Events.bazaar_1.value]
        item_value, item_bit = trade_items_data[item_name]
        bazaar_value_1 = item_value
        rom[0x349190] = item_value

        # Handle Bazaar #2
        item_name = trade_items[Events.bazaar_2.value]
        item_value, item_bit = trade_items_data[item_name]
        rom[0x3491AA] = item_value
        rom[0x32D84C] = item_bit

        # Handle showing Bazaar items
        rom[0x32E1BD] = bazaar_value_1 | item_value

        # Handle Blizzard
        item_name = trade_items[Events.blizzard.value]
        item_value, item_bit = trade_items_data[item_name]
        rom[0x349527] = item_value
        rom[0x32E1BD+0x10] = item_value

        # Handle Blue
        item_name = trade_items[Events.blue.value]
        item_value, item_bit = trade_items_data[item_name]
        rom[0x3494A5] = item_value
        rom[0x32E1BD+0x0C] = item_value

        # Handle Flower
        item_name = trade_items[Events.flower.value]
        item_value, item_bit = trade_items_data[item_name]
        rom[0x32E501] = item_value

        # Handle Barter
        item_name = trade_items[Events.barter.value]
        item_value, item_bit = trade_items_data[item_name]
        rom[0x349366] = item_value
        rom[0x32E1BD+0x06] = item_value

        return bytes(rom)


    @staticmethod
    def write_palettes(caller: APProcedurePatch, rom: bytes) -> bytes:
        data = json.loads(caller.get_file("data.json").decode("UTF-8"))
        rom = bytearray(rom)

        selected_palettes = data["palettes"]
        selected_palette_filters = data["palette_filters"]

        from .aesthetics import palette_set_offsets, get_palette_bytes
        from .data.palettes import palettes

        for palette_set, offset in palette_set_offsets.items():
            palette_option = selected_palettes[palette_set]
            if "Dixie" in palette_set:
                palette = palettes["Dixie"][palette_option]
            elif "Kiddy" in palette_set:
                palette = palettes["Kiddy"][palette_option]
            else:
                palette = palettes[palette_set][palette_option]
            
            # TODO: Handle custom palettes

            if palette_set in selected_palette_filters:
                filter_option = selected_palette_filters[palette_set]
            else:
                filter_option = 0
            data = get_palette_bytes(palette, filter_option)
            rom[offset:offset+0x1E] = data

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
        ("handle_trading", []),
        ("write_palettes", []),
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
        "palettes": world.options.palettes.value,
        "palette_filters": world.options.palette_filters.value,
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
    patch.write_byte(0x3AFF0E, world.options.dk_coin_locations.value)
    patch.write_byte(0x3AFF0F, world.options.kong_locations.value)
    patch.write_byte(0x3AFF10, world.options.balloon_locations.value)
    patch.write_byte(0x3AFF11, world.options.banana_locations.value)
    patch.write_byte(0x3AFF12, world.options.coin_locations.value)
    patch.write_byte(0x3AFF13, world.options.bird_locations.value)
    patch.write_byte(0x3AFF14, world.options.starting_life_count.value)
    patch.write_byte(0x3AFF15, world.options.vehicle_unlock.value)
    patch.write_byte(0x3AFF16, world.options.swanky_locations.value)
    patch.write_byte(0x3AFF17, world.options.swap_krool.value)

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

    # Move Knautilus RAM if swapped
    if world.options.swap_krool:
        patch.write_byte(0x32F339, 0x55)

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

    # Save shuffled levels data and trade items
    json_trade = json.dumps(world.trade_items).encode("UTF-8")
    patch.write_file("trade.bin", base64.b64encode(json_trade))

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
        file_name = options["dktoluca_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
