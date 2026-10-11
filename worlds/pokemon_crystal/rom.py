import hashlib
import json
import logging
import os
import pkgutil
import random
from collections import defaultdict, deque
from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING

import bsdiff4

from Generate import roll_settings
from Utils import Version, tuplize_version
from settings import get_settings
from worlds.Files import APProcedurePatch, APTokenMixin, APPatchExtension
from .battle_tower_data import BATTLE_TOWER_TIER_OFFSET, BATTLE_TOWER_NUM_TIERS, BATTLE_TOWER_TRAINER_OFFSET, \
    BATTLE_TOWER_NUM_TRAINERS
from .data import data, MiscOption, EncounterType, EncounterKey, FishingRodType, FishTimeOfDay, TreeRarity, MapPalette, \
    PaletteData, LocationData, EvolutionType, Landmark, MoveCategory, ONE_WAY_TARGET_SUFFIX
from .entrance_rando import REVERSE_CONNECTIONS
from .evolution import get_pokemon_evolutions
from .fly import get_fly_regions, fly_flag_index
from .item_data import POKEDEX_COUNT_OFFSET, POKEDEX_OFFSET, GRASS_OFFSET, CANONICAL_ITEM_ID_MASK
from .items import item_const_name_to_id
from .maps import FLASH_MAP_GROUPS
from .misc import AFRICAN_COUNTRIES
from .options import UndergroundsRequirePower, RequireItemfinder, Goal, VanillaEventChains, Route2Access, Route42Access, \
    BlackthornDarkCaveAccess, NationalParkAccess, Route3Access, EncounterSlotDistribution, Route22AccessRequirement, \
    FreeFlyLocation, HMBadgeRequirements, ShopsanityPrices, WildEncounterMethodsRequired, Shopsanity, \
    RequireFlash, FieldMoveMenuOrder, RedGyaradosAccess, TrainerPalette, PokemonCrystalOptions, RandomizeBadges, \
    RandomizePokegear, BreedingMethodsRequired, RandomizePokedex, Route30Access, SouthKantoCondition, \
    SaffronGatehouseTea, ModifyPalettes, TrainerGender, PhysicalSpecialSplit, ModerniseMovesType, Route12Access
from .phone_data import done_cmd
from .pokemon_data import ALL_UNOWN
from .rematch_trainer_data import REMATCH_TRAINER_LOCATION_BASE, NUM_REMATCH_TRAINER_LOCATIONS
from .rom_patches import ROM_PATCHES
from .utils import convert_to_ingame_text, rom_offset_to_address, write_appp_tokens, write_rom_bytes, \
    replace_map_tiles, parse_time, start_inventory_problems

if TYPE_CHECKING:
    from .world import PokemonCrystalWorld

PAL_OW_PINK_INDEX = 4
PALETTE_SIZE = 8  # 4 colors * 2 bytes each
PALETTES_PER_TIME_OF_DAY = 8
TIME_OF_DAY_BLOCK_SIZE = PALETTES_PER_TIME_OF_DAY * PALETTE_SIZE  # 64 bytes
# Pink palette color 2 offset within each time-of-day block: palette 4, color 2
PINK_COLOR2_OFFSET = PAL_OW_PINK_INDEX * PALETTE_SIZE + 4  # 4 bytes into palette = color 2


BATTLE_TOWER_MONS_PER_TIER = 21
BATTLE_TOWER_TRAINER_ENTRY_LEN = 11
BATTLE_TOWER_MON_STRUCT_LEN = 59


def permute_battle_tower(rom: bytearray, perm: Sequence[int], mon_seed: int) -> None:
    trainers_addr = data.rom_addresses["AP_BattleTowerTrainers"]
    original = [bytes(rom[trainers_addr + i * BATTLE_TOWER_TRAINER_ENTRY_LEN:
                          trainers_addr + (i + 1) * BATTLE_TOWER_TRAINER_ENTRY_LEN])
                for i in range(BATTLE_TOWER_NUM_TRAINERS)]
    for shuffled_pos, canonical_id in enumerate(perm):
        rom[trainers_addr + shuffled_pos * BATTLE_TOWER_TRAINER_ENTRY_LEN:
            trainers_addr + (shuffled_pos + 1) * BATTLE_TOWER_TRAINER_ENTRY_LEN] = original[canonical_id]

    canonical_addr = data.rom_addresses["AP_BattleTowerCanonicalIds"]
    for shuffled_pos, canonical_id in enumerate(perm):
        rom[canonical_addr + shuffled_pos] = canonical_id

    rng = random.Random(mon_seed)
    mons_addr = data.rom_addresses["AP_BattleTowerMons"]
    tier_byte_len = BATTLE_TOWER_MONS_PER_TIER * BATTLE_TOWER_MON_STRUCT_LEN
    for tier in range(BATTLE_TOWER_NUM_TIERS):
        tier_base = mons_addr + tier * tier_byte_len
        mons = [bytes(rom[tier_base + i * BATTLE_TOWER_MON_STRUCT_LEN:
                          tier_base + (i + 1) * BATTLE_TOWER_MON_STRUCT_LEN])
                for i in range(BATTLE_TOWER_MONS_PER_TIER)]
        rng.shuffle(mons)
        for i, mon in enumerate(mons):
            rom[tier_base + i * BATTLE_TOWER_MON_STRUCT_LEN:
                tier_base + (i + 1) * BATTLE_TOWER_MON_STRUCT_LEN] = mon


def write_battle_tower_uber_list(world: "PokemonCrystalWorld",
                                 write_bytes: Callable[[bytes | Sequence[int], int], None]) -> None:
    uber_ids = sorted(pkmn.id for pkmn in world.generated_pokemon.values() if pkmn.bst >= 600)
    payload = uber_ids + [0]
    write_bytes(payload, data.rom_addresses["AP_BattleTowerUberList"])


def hex_to_gbc_color(r8: int, g8: int, b8: int) -> list[int]:
    """Convert 8-bit RGB to 2-byte little-endian GBC color (5-bit per channel, 0bBBBBBGGGGGRRRRR)."""
    r5 = r8 >> 3
    g5 = g8 >> 3
    b5 = b8 >> 3
    gbc = (b5 << 10) | (g5 << 5) | r5
    return [gbc & 0xFF, (gbc >> 8) & 0xFF]


def parse_hex_color(hex_str: str) -> tuple[int, int, int]:
    """Parse a 6-char hex color string (no #) to (r, g, b) 8-bit values."""
    return int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16)



RADIO_TOWER_MUSIC = 0x80
# music loaded with `ld a, LOW(MUSIC_*)`, whose immediate is only 1 byte
SINGLE_BYTE_MUSIC_SCRIPTS = {"credits__MUSIC_POST_CREDITS"}

CRYSTAL_1_0_HASH = "9f2922b235a5eeb78d65594e82ef5dde"
CRYSTAL_1_1_HASH = "301899b8087289a6436b0a241fbbb474"

# ROM revision byte (AP_ROM_Revision) -> base patch shipped in the APWorld package.
BASE_PATCH_FILES = {0: "data/basepatch.bsdiff4", 1: "data/basepatch11.bsdiff4"}


def get_base_patch_hashes() -> dict[str, str]:
    return {str(revision): hashlib.sha256(pkgutil.get_data(__name__, path)).hexdigest()
            for revision, path in BASE_PATCH_FILES.items()}

# Index is offset from AP_Spawns; cities without a pokecenter are omitted. Coords are the tile in
# front of the nurse - the 9x7 Indigo Plateau pokecenter puts its counter three block rows lower
# than the standard 5x4 one, so the usual (3, 3) is solid wall there.
POKECENTER_SPAWN_ENTRIES: list[tuple[int, str, int, int]] = [
    (1, "VIRIDIAN_POKECENTER_1F", 3, 3),
    (2, "PEWTER_POKECENTER_1F", 3, 3),
    (3, "CERULEAN_POKECENTER_1F", 3, 3),
    (4, "ROUTE_10_POKECENTER_1F", 3, 3),
    (5, "VERMILION_POKECENTER_1F", 3, 3),
    (6, "LAVENDER_POKECENTER_1F", 3, 3),
    (7, "SAFFRON_POKECENTER_1F", 3, 3),
    (8, "CELADON_POKECENTER_1F", 3, 3),
    (9, "FUCHSIA_POKECENTER_1F", 3, 3),
    (10, "CINNABAR_POKECENTER_1F", 3, 3),
    (11, "INDIGO_PLATEAU_POKECENTER_1F", 3, 9),
    (13, "CHERRYGROVE_POKECENTER_1F", 3, 3),
    (14, "VIOLET_POKECENTER_1F", 3, 3),
    (15, "ROUTE_32_POKECENTER_1F", 3, 3),
    (16, "AZALEA_POKECENTER_1F", 3, 3),
    (17, "CIANWOOD_POKECENTER_1F", 3, 3),
    (18, "GOLDENROD_POKECENTER_1F", 3, 3),
    (19, "OLIVINE_POKECENTER_1F", 3, 3),
    (20, "ECRUTEAK_POKECENTER_1F", 3, 3),
    (21, "MAHOGANY_POKECENTER_1F", 3, 3),
    (23, "BLACKTHORN_POKECENTER_1F", 3, 3),
    (24, "SILVER_CAVE_POKECENTER_1F", 3, 3),
]


class PokemonCrystalAPPatchExtension(APPatchExtension):
    game = data.manifest.game

    @staticmethod
    def apply_base_patch(caller: "PokemonCrystalProcedurePatch", rom: bytes):
        revision = rom[data.rom_addresses["AP_ROM_Revision"]]
        base_patch_file = BASE_PATCH_FILES.get(revision, BASE_PATCH_FILES[0])
        base_patch = pkgutil.get_data(__name__, base_patch_file)
        expected_hash = (caller.base_patch_hashes or {}).get(str(revision))
        if expected_hash is not None and hashlib.sha256(base_patch).hexdigest() != expected_hash:
            raise AssertionError(f"This {caller.game} patch was generated with a different base patch than the one in "
                                 f"your installed APWorld (version {data.manifest.world_version}). Please regenerate "
                                 "the patch or install the APWorld version it was generated with.")
        return bsdiff4.patch(rom, base_patch)

    @staticmethod
    def apply_overrides(caller: APProcedurePatch, rom: bytes) -> bytes:
        overridden_rom = bytearray(rom)
        write_bytes = lambda data, address: write_rom_bytes(overridden_rom, data, address)

        for patch in ROM_PATCHES:
            if any(entry.expected is not None
                   and list(overridden_rom[entry.rom_offset:entry.rom_offset + len(entry.expected)]) != entry.expected
                   for entry in patch.entries):
                continue
            for entry in patch.entries:
                write_bytes(entry.data, entry.rom_offset)

        if "world_data.json" not in caller.files:
            world_data = {}
        else:
            world_data = json.loads(caller.get_file("world_data.json").decode("utf-8"))

        if "battle_tower_trainer_permutation" in world_data:
            permute_battle_tower(overridden_rom,
                                 world_data["battle_tower_trainer_permutation"],
                                 world_data["battle_tower_mon_seed"])

        option_overrides = get_settings().pokemon_crystal_settings.option_overrides

        if "skip_elite_four" in option_overrides:
            for trainer_name in ("WILL", "KOGA", "BRUNO", "KAREN"):
                if overridden_rom[data.rom_addresses[f"AP_AdhocTrainersanity_ITEM_FROM_ELITE_4_{trainer_name}"]] != 0:
                    logging.warning("Pokemon Crystal: One or more Elite 4 trainers is a trainersanity location. "
                                    "Ignoring skip_elite_four override.")
                    option_overrides.pop("skip_elite_four", None)
                    break

        if ("skip_elite_four" in option_overrides
                and overridden_rom[data.rom_addresses["AP_Setting_LanceKickOut"] + 1] != 0):
            logging.warning("Pokemon Crystal: Lance Requires Elite Four is enabled. "
                            "Ignoring skip_elite_four override.")
            option_overrides.pop("skip_elite_four", None)

        if "skip_elite_four" in option_overrides and not world_data.get("skip_elite_four_overridable", False):
            logging.warning("Pokemon Crystal: Pokemon League entrances are randomized or Skip Elite Four is "
                            "already enabled. Ignoring skip_elite_four override.")
            option_overrides.pop("skip_elite_four", None)

        if not option_overrides:
            return overridden_rom

        wrapped_overrides = {
            "game": data.manifest.game,
            data.manifest.game: option_overrides
        }
        rolled_options = roll_settings(wrapped_overrides)

        must_write_option = lambda option_key: option_key in option_overrides

        if must_write_option("game_options"):
            game_option_overrides = rolled_options.game_options
            game_options_address = data.rom_addresses["AP_Setting_DefaultOptions"]
            num_option_bytes = max([item.option_byte_index for item in data.game_settings.values()]) + 1
            option_bytes = overridden_rom[game_options_address:game_options_address + num_option_bytes]

            for setting_name, setting in data.game_settings.items():
                option_selection = game_option_overrides.get(setting_name, None)
                if option_selection is None:
                    continue
                if setting_name == "text_frame" and option_selection == "random":
                    option_selection = random.randint(1, 8)
                if setting_name == "time_of_day" and option_selection == "random":
                    option_selection = random.choice(("morn", "day", "nite"))
                if setting_name == "_death_link":
                    option_selection = "on" if game_option_overrides.get("death_link", False) else "off"
                elif setting_name == "_trap_link":
                    option_selection = "on" if game_option_overrides.get("trap_link", False) else "off"
                setting.set_option_byte(option_selection, option_bytes)

            write_bytes(option_bytes, game_options_address)

        if must_write_option("trainer_gender"):
            trainer_gender = rolled_options.trainer_gender.value
            if trainer_gender == TrainerGender.option_randomize:
                trainer_gender -= random.randint(1, 2)
            write_bytes([(trainer_gender - 1) % 256], data.rom_addresses["AP_Setting_PlayerGender"] + 1)

        if must_write_option("rival_name"):
            name_set_bool = [1] if rolled_options.rival_name.value != "" else [0]
            rival_name = convert_to_ingame_text(rolled_options.rival_name.value[:7], string_terminator=True)
            write_bytes(name_set_bool, data.rom_addresses["AP_Setting_DoNameRival"] + 1)
            write_bytes(rival_name, data.rom_addresses["AP_Setting_RivalName"])
            write_bytes(name_set_bool, data.rom_addresses["AP_Setting_RivalNameIsSet"] + 1)

        write_customizable_options(rolled_options, write_bytes, must_write_option, world_data)

        return overridden_rom


class PokemonCrystalProcedurePatch(APProcedurePatch, APTokenMixin):
    game = data.manifest.game
    hash = [CRYSTAL_1_0_HASH, CRYSTAL_1_1_HASH]
    patch_file_ending = ".apcrystal"
    result_file_ending = ".gbc"
    world_version: Version | None = None
    minimum_world_version: Version | None = None
    base_patch_hashes: dict[str, str] | None = None

    procedure = [
        ("apply_base_patch", []),
        ("apply_tokens", ["token_data.bin"]),
        ("apply_overrides", [])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_as_bytes()

    def get_manifest(self):
        manifest = super().get_manifest()
        manifest["world_version"] = data.manifest.world_version
        manifest["minimum_patch_version"] = data.manifest.minimum_patch_version
        manifest["base_patch_hashes"] = get_base_patch_hashes()
        return manifest

    def read_contents(self, opened_zipfile):
        manifest = super().read_contents(opened_zipfile)
        world_version = manifest.get("world_version", None)
        min_version = manifest.get("minimum_patch_version", None)
        if world_version is not None:
            self.world_version = tuplize_version(world_version)
        if min_version is not None:
            self.minimum_world_version = tuplize_version(min_version)
        self.base_patch_hashes = manifest.get("base_patch_hashes", None)
        self.assert_version_compat()

    def assert_version_compat(self):
        if self.world_version is None:
            raise AssertionError(f"This {self.game} patch is too old for this APWorld. "
                                  "Please double-check the version used for generating.")

        installed_world_version = tuplize_version(data.manifest.world_version)
        installed_min_version = tuplize_version(data.manifest.minimum_patch_version)
        direction = False
        if installed_world_version < self.minimum_world_version:
            direction = "up"
        elif self.world_version < installed_min_version:
            direction = "down"
        if direction:
            raise AssertionError(f"This {self.game} patch used version {self.world_version.as_simple_string()}, "
                                  "which is incompatible with currently installed version "
                                 f"{data.manifest.world_version}. Please {direction}grade your APWorld.")


def write_customizable_options(options: PokemonCrystalOptions,
                               write_bytes: Callable[[bytes | Sequence[int], int], None],
                               must_write_option: Callable[[str], bool],
                               world_data: dict
                               ) -> None:
    if must_write_option("field_move_menu_order"):
        write_bytes([FieldMoveMenuOrder.default.index(val) for val in options.field_move_menu_order.value],
                    data.rom_addresses["AP_Setting_Field_Move_Order"])

    if must_write_option("trainer_name"):
        name_bytes = convert_to_ingame_text(options.trainer_name.value[:7], string_terminator=True)
        write_bytes(name_bytes, data.rom_addresses["AP_Setting_DefaultTrainerName"])

    if must_write_option("start_time"):
        time = parse_time(options.start_time.value)
        if time is not None:
            write_bytes([time[0]], data.rom_addresses["AP_Setting_DefaultHour"] + 1)
            write_bytes([time[1]], data.rom_addresses["AP_Setting_DefaultMinutes"] + 1)
        else:
            logging.warning(f"Pokemon Crystal: {options.start_time.value} is not a valid time string. Ignoring.")

    if must_write_option("default_pokedex_mode"):
        write_bytes([options.default_pokedex_mode.value], data.rom_addresses["AP_Setting_DefaultDexMode"] + 1)

    if must_write_option("encounter_slot_distribution"):
        write_encounter_rates(options.encounter_slot_distribution.value, data.wild, write_bytes)

    if must_write_option("trainer_palette"):
        is_custom = isinstance(options.trainer_palette.value, str)

        if is_custom:
            r8, g8, b8 = parse_hex_color(options.trainer_palette.value)
            custom_color_bytes = hex_to_gbc_color(r8, g8, b8)
            chris_palette_index = PAL_OW_PINK_INDEX
            kris_palette_index = PAL_OW_PINK_INDEX

            # Patch the pink palette's clothing color (color 2) in all 4 time-of-day slots
            map_object_pals_base = data.rom_addresses["AP_Setting_MapObjectPals"]
            for tod in range(4):  # morn, day, nite, dark
                offset = map_object_pals_base + tod * TIME_OF_DAY_BLOCK_SIZE + PINK_COLOR2_OFFSET
                write_bytes(custom_color_bytes, offset)

            # Patch the pink palette's clothing color in the party menu OBJ palettes (used by naming screen)
            party_menu_ob_pals_base = data.rom_addresses["AP_Setting_PartyMenuOBPals"]
            write_bytes(custom_color_bytes, party_menu_ob_pals_base + PINK_COLOR2_OFFSET)
        elif options.trainer_palette.value == TrainerPalette.option_vanilla:
            chris_palette_data = next(
                palette for palette in data.palettes if palette.index == TrainerPalette.option_red - 1)
            kris_palette_data = next(
                palette for palette in data.palettes if palette.index == TrainerPalette.option_blue - 1)
            chris_palette_index = chris_palette_data.index
            kris_palette_index = kris_palette_data.index
            chris_battle_palette = chris_palette_data.battle_palette
            kris_battle_palette = kris_palette_data.battle_palette
        else:
            palette_data = next(
                palette for palette in data.palettes if palette.index == options.trainer_palette - 1)
            chris_palette_index = palette_data.index
            kris_palette_index = palette_data.index
            chris_battle_palette = palette_data.battle_palette
            kris_battle_palette = palette_data.battle_palette

        chris_addresses = ("AP_Setting_ChrisWalkSpriteData", "AP_Setting_ChrisBikeSpriteData",
                           "AP_Setting_ChrisRunSpriteData")
        kris_addresses = ("AP_Setting_KrisWalkSpriteData", "AP_Setting_KrisBikeSpriteData",
                          "AP_Setting_KrisRunSpriteData")

        for address_ref in chris_addresses:
            write_bytes([chris_palette_index], data.rom_addresses[address_ref] + 5)
        for address_ref in kris_addresses:
            write_bytes([kris_palette_index], data.rom_addresses[address_ref] + 5)

        for i in range(1, 5):
            chris_byte = (chris_palette_index + PaletteData.NPC_PAL_OFFSET) << 4
            kris_byte = (kris_palette_index + PaletteData.NPC_PAL_OFFSET) << 4
            write_bytes([chris_byte], data.rom_addresses[f"AP_Setting_ChrisSpritePalette_{i}"] + 1)
            write_bytes([kris_byte], data.rom_addresses[f"AP_Setting_KrisSpritePalette_{i}"] + 1)

        write_bytes([chris_palette_index], data.rom_addresses["AP_Setting_ChrisIntroPal"] + 1)
        write_bytes([kris_palette_index], data.rom_addresses["AP_Setting_KrisIntroPal"] + 1)

        if is_custom:
            # Only patch color 2 (clothing), leave color 1 (skin tone) from basepatch
            write_bytes(custom_color_bytes, data.rom_addresses["AP_Setting_ChrisBattlePalette"] + 2)
            write_bytes(custom_color_bytes, data.rom_addresses["AP_Setting_KrisBattlePalette"] + 2)
        else:
            write_bytes(chris_battle_palette, data.rom_addresses["AP_Setting_ChrisBattlePalette"])
            write_bytes(kris_battle_palette, data.rom_addresses["AP_Setting_KrisBattlePalette"])

        address = data.rom_addresses["AP_Setting_OAMBlueWalk"] + 4
        for i in range(4):
            write_bytes([kris_palette_index], address)
            address += 4

        address = data.rom_addresses["AP_Setting_OAMRedWalk"] + 4
        for i in range(4):
            write_bytes([chris_palette_index], address)
            address += 4

        address = data.rom_addresses["AP_Setting_OAMMagnetTrainBlue"] + 4
        for i in range(4):
            write_bytes([kris_palette_index | PaletteData.PRIORITY], address)
            address += 4

        address = data.rom_addresses["AP_Setting_OAMMagnetTrainRed"] + 4
        for i in range(4):
            write_bytes([chris_palette_index | PaletteData.PRIORITY], address)
            address += 4

    if must_write_option("reusable_tms"):
        patched_value = 1 if options.reusable_tms.value else 0
        address = data.rom_addresses["AP_Setting_ReusableTMs"] + 1
        write_bytes([patched_value], address)


    if must_write_option("minimum_catch_rate"):
        address = data.rom_addresses["AP_Setting_MinCatchrate"] + 1
        write_bytes([options.minimum_catch_rate.value], address)

    if must_write_option("experience_modifier"):
        exp_modifier_address = data.rom_addresses["AP_Setting_ExpModifier"]
        write_bytes([options.experience_modifier.value], exp_modifier_address)

    if must_write_option("skip_elite_four"):
        # Set warp to Lance's room or set it back to Will's
        e4_warp = 0x07 if options.skip_elite_four.value else 0x03
        write_bytes([e4_warp], data.rom_addresses["AP_Setting_IndigoPlateauPokecenter1F_E4Warp"] + 4)

    if must_write_option("shopsanity_restrict_rare_candies"):
        patched_value = 1 if options.shopsanity_restrict_rare_candies.value else 0
        address = data.rom_addresses["AP_Setting_ShopsanityRestrictRareCandies"] + 1
        write_bytes([patched_value], address)

    if must_write_option("all_pokemon_seen"):
        patched_value = 1 if options.all_pokemon_seen.value else 0
        write_bytes([patched_value], data.rom_addresses["AP_Setting_AllPokemonSeen_1"] + 1)
        write_bytes([patched_value], data.rom_addresses["AP_Setting_AllPokemonSeen_2"] + 1)

    if must_write_option("starting_money"):
        start_money = options.starting_money.value.to_bytes(3, "big")
        for i, byte in enumerate(start_money):
            write_bytes([byte], data.rom_addresses[f"AP_Setting_StartMoney_{i + 1}"] + 1)

    if must_write_option("better_marts"):
        patched_value = 1 if options.better_marts.value else 0
        write_bytes([patched_value], data.rom_addresses["AP_Setting_BetterMarts"] + 1)

    if must_write_option("build_a_mart"):
        custom_mart_base = data.rom_addresses["AP_Setting_CustomBetterMart"]

        available_items = {item.label: item.item_const for item in data.items.values()
                           if "CustomShop" in item.tags}

        selected_items = []
        for item_name in options.build_a_mart.value:
            if item_name in available_items:
                selected_items.append(available_items[item_name])

        if len(selected_items) > 14:
            selected_items = selected_items[:14]

        total_items = len(selected_items) + 2
        write_bytes([total_items], custom_mart_base)

        get_item_price = lambda item_data: (world_data.get("item_prices", {})
                                            .get(str(item_data.item_id), item_data.price))

        current_address = custom_mart_base + 11
        for item_const in selected_items:
            item_id = item_const_name_to_id(item_const)
            item_data = data.items[item_id]
            price_bytes = get_item_price(item_data).to_bytes(2, "little")
            write_bytes([item_id, *price_bytes, 0xFF, 0xFF], current_address)
            current_address += 5

        write_bytes([0xFF], current_address)

    if must_write_option("game_options"):
        if "tracker_slot" in options.game_options:
            try:
                tracker_slot = int(options.game_options["tracker_slot"]) & 0xFF
                write_bytes([tracker_slot], data.rom_addresses["AP_Setting_DefaultTrackerSlot"])
            except ValueError:
                pass


def _resolve_arrival(conns, map_consts, reverse_lookup, target_name):
    """Resolve a pairing target to (warp, group, map) arrival data."""
    if target_name.endswith(ONE_WAY_TARGET_SUFFIX):
        conn = conns.get(target_name.removesuffix(ONE_WAY_TARGET_SUFFIX))
    else:
        rev = reverse_lookup.get(target_name)
        conn = conns.get(rev) if rev else None
    if conn and conn.arrival_map_const in map_consts:
        group, map_id = map_consts[conn.arrival_map_const]
        return conn.arrival_warp_index, group, map_id
    return None


def write_route_23_restored_warps(write_bytes) -> None:
    """Redirect Victory Road's south warp and Victory Road Gate's north warps
    through Route 23 Restored. The ROM ships with vanilla destinations; this
    rewrites the destination bytes (warp_id, group, map_id) when the option
    is on.

    These three labels must NOT be in any ER pool, or the subsequent
    write_entrance_pairings pass would clobber the redirect. The
    bypassed_vanilla_edges filter in regions.py:create_regions excludes the
    corresponding connections from world.er_entrances, which preserves this
    invariant.
    """
    group, map_id = data.map_constants["ROUTE_23_RESTORED"]
    redirects = [
        ("AP_Warp_VictoryRoad_1", 1),
        ("AP_Warp_VictoryRoadGate_5", 2),
        ("AP_Warp_VictoryRoadGate_6", 3),
    ]
    for label, warp_index in redirects:
        addr = data.rom_addresses.get(label)
        if addr is None:
            continue
        write_bytes([warp_index, group, map_id], addr + 2)


def write_skip_elite_four_lance_exit(write_bytes) -> None:
    """Point Lance's south door at the E4 gate; ER keeps it unlocked and Karen's room is gone."""
    group, map_id = data.map_constants["INDIGO_PLATEAU_POKECENTER_1F"]
    for label in ("AP_Warp_LancesRoom_1", "AP_Warp_LancesRoom_2"):
        write_bytes([4, group, map_id], data.rom_addresses[label] + 2)


def show_flooded_mine_entrances(patch, write_bytes) -> None:
    """When the Flooded Mine is enabled, paint the entrance blocks back onto
    Cherrygrove City and Route 32 and re-enable the town-map cursor stop. The
    basepatch ships vanilla blks and the cursor-skip default-on, so the area
    is invisible until this runs."""
    replace_map_tiles(patch, "CherrygroveCity", 1, 1, [0x6a, 0x70, 0x6b])
    replace_map_tiles(patch, "CherrygroveCity", 0, 2, [0x55, 0x6c, 0x73, 0x6d])
    replace_map_tiles(patch, "CherrygroveCity", 0, 3, [0x59, 0x0a, 0x71, 0x58])
    replace_map_tiles(patch, "CherrygroveCity", 1, 4, [0x76, 0x76, 0x79])
    replace_map_tiles(patch, "Route32", 5, 19, [0x73])
    for label in ("AP_Setting_FloodedMine_Up", "AP_Setting_FloodedMine_Down"):
        addr = data.rom_addresses.get(label)
        if addr is None:
            continue
        write_bytes([1], addr + 1)


def suppress_flooded_mine_wilds(write_bytes) -> None:
    """When Flooded Mine is disabled, the area is unreachable but its wild
    encounter tables still ship in the ROM. FLOODED_MINE is the last entry in
    both johto_grass and johto_water; overwriting the byte before its header
    with 0xff terminates the table scan before reaching its slots, so the
    Pokedex Area screen doesn't pin species to an unreachable cave."""
    for label in ("AP_WildGrass_FLOODED_MINE", "AP_WildWater_FLOODED_MINE"):
        addr = data.rom_addresses.get(label)
        if addr is None:
            continue
        write_bytes([0xff], addr - 2)


def hide_flooded_mine_landmark(write_bytes) -> None:
    """When Flooded Mine is disabled, move its landmark off the town map so
    the dot/cursor never highlights it. The landmark macro stores (x+8, y+16)
    as bytes 0-1 of the entry; matching the SpecialMapName sentinel (-8, -16)
    puts the dot at (0, 0), off the visible map."""
    addr = data.rom_addresses.get("AP_Landmark_FLOODED_MINE")
    if addr is None:
        return
    write_bytes([0, 0], addr)


def suppress_route_23_restored_wilds(write_bytes) -> None:
    """When Route 23 Restored is disabled, the area is unreachable but its
    wild encounter tables still ship in the ROM. Truncate them so the Pokédex
    Area screen doesn't pin species to an unreachable Route 23. Route 23
    Restored is the last entry in both kanto_grass and kanto_water; wild-table
    consumers terminate on a 0xff first byte, so overwriting the map-group
    byte of its header ends the scan before reaching its slots."""
    for label in ("AP_WildGrass_ROUTE_23_RESTORED", "AP_WildWater_ROUTE_23_RESTORED"):
        addr = data.rom_addresses.get(label)
        if addr is None:
            continue
        write_bytes([0xff], addr - 2)


def write_entrance_pairings(world: "PokemonCrystalWorld", write_bytes) -> None:
    conns = data.entrance_connections
    map_consts = data.map_constants
    reverse_lookup = REVERSE_CONNECTIONS

    resolve = lambda tgt: _resolve_arrival(conns, map_consts, reverse_lookup, tgt)

    floor_entry_origin: dict[str, tuple[int, int, int]] = {}
    for source_name, target_name in world.er_pairings:
        source_origin = resolve(source_name)
        if source_origin:
            floor_entry_origin[target_name] = source_origin

    for source_name, target_name in world.er_pairings:
        source_conn = conns.get(source_name)
        if source_conn is None:
            continue

        arrival = resolve(target_name)
        if arrival is None:
            continue

        for exit_warp in source_conn.exit_warps:
            label = exit_warp.label or f"AP_Warp_{exit_warp.map_name}_{exit_warp.warp_index}"
            addr = data.rom_addresses.get(label)
            if addr is None:
                continue
            if exit_warp.addr_offset == 4:
                warp_data = floor_entry_origin.get(reverse_lookup.get(source_name), arrival)
            else:
                warp_data = arrival
            write_bytes(list(warp_data), addr + exit_warp.addr_offset)


# Encounter slot rate/probability tables per EncounterSlotDistribution.
# Each distribution leaves "unchanged" methods at their vanilla values, so the
# tables are complete and overwriting them is idempotent for the vanilla case.
_ESD = EncounterSlotDistribution
_GRASS_PROBS = {  # cumulative thresholds, 7 slots
    _ESD.option_vanilla: [30, 60, 80, 90, 95, 99, 100],
    _ESD.option_remove_one_percents: [30, 55, 75, 85, 90, 95, 100],
    _ESD.option_balanced: [20, 40, 55, 70, 80, 90, 100],
    _ESD.option_equal: [14, 28, 42, 57, 71, 85, 100],
}
_WATER_PROBS = {  # cumulative thresholds, 3 slots
    _ESD.option_vanilla: [60, 90, 100],
    _ESD.option_remove_one_percents: [60, 90, 100],
    _ESD.option_balanced: [60, 90, 100],
    _ESD.option_equal: [33, 66, 100],
}
_TREE_RATES = {  # per-slot rates, 6 slots
    _ESD.option_vanilla: [50, 15, 15, 10, 5, 5],
    _ESD.option_remove_one_percents: [50, 15, 15, 10, 5, 5],
    _ESD.option_balanced: [20, 20, 20, 15, 15, 10],
    _ESD.option_equal: [16, 16, 17, 17, 17, 17],
}
_ROCK_RATES = {  # per-slot rates, 2 slots
    _ESD.option_vanilla: [90, 10],
    _ESD.option_remove_one_percents: [90, 10],
    _ESD.option_balanced: [70, 30],
    _ESD.option_equal: [50, 50],
}


def write_encounter_rates(distribution: int, wild, write_bytes) -> None:
    """Write every encounter slot rate/probability byte for the given distribution.
    Writes only rate bytes (not species/levels), so it is safe to call both during
    generation and as a patch-time override."""
    prob_table = lambda probs: [b for i, p in enumerate(probs) for b in (p, i * 2)]
    write_bytes(prob_table(_GRASS_PROBS[distribution]), data.rom_addresses["AP_Prob_GrassMon"])
    write_bytes(prob_table(_WATER_PROBS[distribution]), data.rom_addresses["AP_Prob_WaterMon"])
    tree_rates = _TREE_RATES[distribution]
    rock_rates = _ROCK_RATES[distribution]
    is_equal = distribution == _ESD.option_equal

    for region_key, encounters in wild.items():
        if region_key.encounter_type is EncounterType.Tree:
            base = data.rom_addresses[f"TreeMonSet_{region_key.region_id}"]
            if region_key.rarity is TreeRarity.Rare:
                base += 19  # skip the 6 common encounters + terminator byte
            for i in range(len(encounters)):
                write_bytes([tree_rates[i]], base + i * 3)
        elif region_key.encounter_type is EncounterType.RockSmash:
            base = data.rom_addresses["TreeMonSet_Rock"]
            for i in range(len(encounters)):
                write_bytes([rock_rates[i]], base + i * 3)
        elif region_key.encounter_type is EncounterType.Fish:
            if region_key.time_of_day is FishTimeOfDay.Nite:
                continue  # rates live in the shared per-slot bytes, covered by the Day key
            base = data.rom_addresses[f"AP_FishMons_{region_key.region_id}"]
            if region_key.fishing_rod is FishingRodType.Good:
                base += 9  # skip the 3 old-rod encounters, each 3 bytes
            elif region_key.fishing_rod is FishingRodType.Super:
                base += 21  # skip the 7 old + good encounters
            n = len(encounters)
            if is_equal:
                # fishing rates are stored as an increasing fraction of 255
                rates = [int(((i + 1) / n) * 255) for i in range(n)]
            else:
                rates = data.fish_rates[(region_key.region_id, region_key.fishing_rod)]
            for i in range(n):
                write_bytes([rates[i]], base + i * 3)


def generate_output(world: "PokemonCrystalWorld", output_directory: str, patch: PokemonCrystalProcedurePatch) -> None:
    write_bytes = lambda data, address: write_appp_tokens(patch, data, address)
    # The vanilla value of an option evaluates to False
    must_write_option = lambda option_key: bool(getattr(world.options, option_key))

    option_bytes = bytearray(max([item.option_byte_index for item in data.game_settings.values()]) + 1)

    for setting_name, setting in data.game_settings.items():
        option_selection = world.options.game_options.get(setting_name, None)
        if setting_name == "text_frame" and option_selection == "random":
            option_selection = world.random.randint(1, 8)
        if setting_name == "time_of_day" and option_selection == "random":
            option_selection = world.random.choice(("morn", "day", "nite"))
        if setting_name == "time_of_day" and world.options.unlockable_time_of_day and world.options.time_of_day_encounters:
            option_selection = world.precollected_tod.lower()
        if setting_name == "_death_link":
            option_selection = "on" if world.options.death_link else "off"
        if setting_name == "_trap_link":
            option_selection = "on" if world.options.trap_link else "off"
        setting.set_option_byte(option_selection, option_bytes)

    write_bytes(option_bytes, data.rom_addresses["AP_Setting_DefaultOptions"])

    # Patch unlockable time of day starting bitmask
    if world.options.unlockable_time_of_day and world.options.time_of_day_encounters:
        tod_bitmask = {"Morn": 1, "Day": 2, "Nite": 4}[world.precollected_tod]
        write_bytes([tod_bitmask], data.rom_addresses["AP_Setting_UnlockableTimeOfDay"] + 1)
    else:
        write_bytes([0x07], data.rom_addresses["AP_Setting_UnlockableTimeOfDay"] + 1)

    def write_item(item: int, addresses: list[int]) -> None:
        for address in addresses:
            write_bytes([item], address)
            if address in data.adhoc_trainersanity:
                write_bytes([1], data.adhoc_trainersanity[address])

    item_texts = []
    for location in world.multiworld.get_locations(world.player):
        if location.address is None:
            continue

        if location.address >= GRASS_OFFSET:
            location_addresses = location.rom_addresses
        elif location.address > POKEDEX_COUNT_OFFSET:
            location_addresses = [data.rom_addresses["AP_DexcountsanityItems"] + address - 1 for address in
                                  location.rom_addresses]
        elif location.address > POKEDEX_OFFSET:
            location_addresses = [data.rom_addresses["AP_DexsanityItems"] + address - 1 for address in
                                  location.rom_addresses]
        else:
            location_addresses = location.rom_addresses

        if not world.options.remote_items and location.item and location.item.player == world.player:
            item_id = location.item.code & CANONICAL_ITEM_ID_MASK
            if location.item.flag_index is not None:
                write_item(item_const_name_to_id("FLAG_ITEM"), location_addresses)

                if location.address >= GRASS_OFFSET:
                    if hasattr(location, "original_grass_flag"):
                        grass_address = location.original_grass_flag
                    else:
                        grass_address = location.address
                    address = (data.rom_addresses["AP_Setting_FlagItems_Table_Grass"]
                               + (grass_address - GRASS_OFFSET))
                elif location.address > POKEDEX_COUNT_OFFSET:
                    address = (data.rom_addresses["AP_Setting_FlagItems_Table_Dexcountsanity"]
                               + (location.address - POKEDEX_COUNT_OFFSET) - 1)
                elif location.address > POKEDEX_OFFSET:
                    address = (data.rom_addresses["AP_Setting_FlagItems_Table_Dexsanity"]
                               + (location.address - POKEDEX_OFFSET) - 1)
                elif BATTLE_TOWER_TIER_OFFSET <= location.address < BATTLE_TOWER_TIER_OFFSET + BATTLE_TOWER_NUM_TIERS:
                    address = (data.rom_addresses["AP_Setting_FlagItems_Table_BattleTower"]
                               + (location.address - BATTLE_TOWER_TIER_OFFSET))
                elif BATTLE_TOWER_TRAINER_OFFSET <= location.address < BATTLE_TOWER_TRAINER_OFFSET + BATTLE_TOWER_NUM_TRAINERS:
                    address = (data.rom_addresses["AP_Setting_FlagItems_Table_BattleTowerTrainers"]
                               + (location.address - BATTLE_TOWER_TRAINER_OFFSET))
                elif REMATCH_TRAINER_LOCATION_BASE <= location.address < REMATCH_TRAINER_LOCATION_BASE + NUM_REMATCH_TRAINER_LOCATIONS:
                    address = (data.rom_addresses["AP_Setting_FlagItems_Table_RematchTrainers"]
                               + (location.address - REMATCH_TRAINER_LOCATION_BASE))
                else:
                    address = data.rom_addresses["AP_Setting_FlagItems_Table_Events"] + location.address

                write_bytes([location.item.flag_index], address)
            else:
                write_item(item_id, location_addresses)
        else:
            # for in game text
            if location.address < POKEDEX_OFFSET:
                from BaseClasses import ItemClassification
                item_flag = location.address
                player_name = world.multiworld.player_name[location.item.player].upper()
                item_name = location.item.name.upper()
                cls = location.item.classification
                if cls & ItemClassification.trap:
                    display_class = world.random.randint(0, 3)
                elif (cls & ItemClassification.progression) and (cls & ItemClassification.useful):
                    display_class = 0
                elif cls & ItemClassification.progression:
                    display_class = 1
                elif cls & ItemClassification.useful:
                    display_class = 2
                else:
                    display_class = 3
                item_texts.append((player_name, item_name, item_flag, "shopsanity" in location.tags, display_class))

            write_item(item_const_name_to_id("AP_ITEM"), location_addresses)

    # table has format: location id (2 bytes), string address (2 bytes), string bank (1 byte),
    # and is terminated by 0xFF
    item_name_table_length = len([entry for entry in item_texts if not entry[3]]) * 5 + 1
    item_name_table_adr = data.rom_addresses["AP_ItemText_Table"]
    shopsanity_name_table_length = len([entry for entry in item_texts if entry[3]]) * 5 + 1
    shopsanity_name_table_adr = data.rom_addresses["AP_MartItemTable"]

    # strings are 16 chars each, plus a terminator byte,
    # this gives every pair of item + player names a size of 34 bytes
    item_name_bank1 = item_name_table_adr + item_name_table_length
    item_name_bank1_length = data.rom_addresses["AP_ItemText_Bank1_End"] - item_name_bank1
    item_name_bank1_capacity = int(item_name_bank1_length / 34)

    item_name_bank2 = data.rom_addresses["AP_ItemText_Bank2"]
    item_name_bank2_length = data.rom_addresses["AP_ItemText_Bank2_End"] - item_name_bank2
    item_name_bank2_capacity = int(item_name_bank2_length / 34)

    item_name_bank3 = data.rom_addresses["AP_ItemText_Bank3"]
    item_name_bank3_length = data.rom_addresses["AP_ItemText_Bank3_End"] - item_name_bank3
    item_name_bank3_capacity = int(item_name_bank3_length / 34)

    table_offset_adr = item_name_table_adr
    shopsanity_table_offset_adr = shopsanity_name_table_adr

    for i, text in enumerate(item_texts):
        shopsanity_entry = text[3]
        # truncate if too long
        player_text = convert_to_ingame_text(text[0])[:16]
        # pad with terminator byte to keep alignment
        player_text.extend([0x50] * (17 - len(player_text)))
        item_text = convert_to_ingame_text(text[1])[:14 if shopsanity_entry else 16]
        item_text.append(0x50)
        # bank 1
        bank = 0x75

        if i >= item_name_bank1_capacity + item_name_bank2_capacity + item_name_bank3_capacity:
            # if we somehow run out of capacity in all banks, just finish the table and break,
            # there is a fallback string in the ROM, so it should handle this gracefully.
            write_bytes([0xFF], item_name_table_adr + table_offset_adr)
            write_bytes([0xFF], shopsanity_name_table_adr + shopsanity_table_offset_adr)
            print("oopsie")
            break
        if i + 1 < item_name_bank1_capacity:
            text_offset = i * 34
            text_adr = item_name_bank1 + text_offset
        elif i + 1 < (item_name_bank1_capacity + item_name_bank2_capacity):
            # bank 2
            bank = 0x76
            text_offset = (i + 1 - item_name_bank1_capacity) * 34
            text_adr = item_name_bank2 + text_offset
        else:
            # bank 3
            bank = 0x7c
            text_offset = (i + 1 - (item_name_bank1_capacity + item_name_bank2_capacity)) * 34
            text_adr = item_name_bank3 + text_offset
        write_bytes(player_text + item_text, text_adr)
        # get the address within the rom bank (0x4000 - 0x7FFF)
        text_bank_adr = (text_adr % 0x4000) + 0x4000
        offset_adr = shopsanity_table_offset_adr if shopsanity_entry else table_offset_adr
        write_bytes(((text[2] - data.mart_flag_offset) if shopsanity_entry else text[2]).to_bytes(2, "big"),
                    offset_adr)
        write_bytes(text_bank_adr.to_bytes(2, "little"), offset_adr + 2)
        if shopsanity_entry:
            bank_selector = {0x75: 0, 0x76: 1, 0x7c: 2}[bank]
            write_bytes([(bank_selector << 6) | (text[4] << 4)], offset_adr + 4)
        else:
            write_bytes([bank], offset_adr + 4)

        if shopsanity_entry:
            shopsanity_table_offset_adr += 5
        else:
            table_offset_adr += 5

    write_bytes([0xFF], item_name_table_adr + item_name_table_length - 1)
    write_bytes([0xFF], shopsanity_name_table_adr + shopsanity_name_table_length - 1)

    if Shopsanity.JOHTO_MARTS in world.options.shopsanity.value:
        write_bytes([1], data.rom_addresses["AP_Setting_JohtoShopsanityEnabled"] + 2)
        # the dw at +11 is the event flag.
        write_bytes([0xFF, 0xFF], data.rom_addresses["AP_Setting_Shopsanity_MahoganyMart_1"] + 11)
        write_bytes([0xFF, 0xFF], data.rom_addresses["AP_Setting_Shopsanity_MahoganyMart_2"] + 11)

    if Shopsanity.KANTO_MARTS in world.options.shopsanity.value:
        write_bytes([1], data.rom_addresses["AP_Setting_KantoShopsanityEnabled"] + 2)

    if Shopsanity.BLUE_CARD in world.options.shopsanity.value:
        write_bytes([1], data.rom_addresses["AP_Setting_BlueCardShopsanityEnabled"] + 2)

    if Shopsanity.GAME_CORNERS in world.options.shopsanity.value:
        write_bytes([1], data.rom_addresses["AP_Setting_GameCornerShopsanityEnabled"] + 2)

    if Shopsanity.APRICORNS in world.options.shopsanity.value:
        write_bytes([1], data.rom_addresses["AP_Setting_ApricornShopsanityEnabled"] + 2)

    for mart, mart_data in data.marts.items():
        if mart_data.category in (Shopsanity.JOHTO_MARTS, Shopsanity.KANTO_MARTS):
            for item in mart_data.items:
                item_id = item_const_name_to_id(item.item)
                price = world.generated_item_values.get(item_id, item.price)
                write_bytes(price.to_bytes(2, "little"), item.address + 1)

    if world.options.shopsanity:

        min_shop_price = world.options.shopsanity_minimum_price.value
        max_shop_price = world.options.shopsanity_maximum_price.value
        total_shop_spheres = len(world.shop_locations_by_spheres)

        remote_items = world.options.remote_items.value

        by_item_price = world.options.shopsanity_prices == ShopsanityPrices.option_item_price

        by_spheres = world.options.shopsanity_prices in (
            ShopsanityPrices.option_spheres,
            ShopsanityPrices.option_spheres_and_classification
        )
        by_classification = world.options.shopsanity_prices in (
            ShopsanityPrices.option_classification,
            ShopsanityPrices.option_spheres_and_classification
        )
        by_location = world.options.shopsanity_prices == ShopsanityPrices.option_vanilla

        if world.options.shopsanity_minimum_price > world.options.shopsanity_maximum_price:
            logging.info("Pokemon Crystal: Minimum Shopsanity Price for player %s (%s)"
                         " is greater than Maximum Shopsanity Price.",
                         world.player, world.player_name)
            min_shop_price = world.options.shopsanity_maximum_price.value
            max_shop_price = world.options.shopsanity_minimum_price.value

        for i, locations in enumerate(world.shop_locations_by_spheres):
            sphere_min_shop_price = min_shop_price
            sphere_max_shop_price = max_shop_price
            if by_spheres:
                base_price = sphere_min_shop_price
                price_difference = max_shop_price - min_shop_price
                sphere_min_shop_price = int(round(base_price + ((price_difference / total_shop_spheres) * i)))
                sphere_max_shop_price = int(round(base_price + ((price_difference / total_shop_spheres) * (i + 1))))

            for location in locations:
                item_min_shop_price = sphere_min_shop_price
                item_max_shop_price = sphere_max_shop_price

                is_local_item = location.item.player == world.player
                item_price = world.generated_item_values.get(location.item.code, 0) if is_local_item else 0
                item_intrinsic_value = item_price
                location_price = location.price

                if by_item_price:
                    if item_price < item_min_shop_price:
                        item_price = item_min_shop_price
                    elif item_price > item_max_shop_price:
                        item_price = item_max_shop_price
                    item_min_shop_price = item_price
                    item_max_shop_price = item_price
                elif by_classification:
                    base_price = item_min_shop_price
                    price_difference = item_max_shop_price - item_min_shop_price
                    if location.item.advancement:
                        item_min_shop_price = base_price + int(round(price_difference * 0.6))
                    elif location.item.useful:
                        item_min_shop_price = base_price + int(round(price_difference * 0.2))
                        item_max_shop_price = base_price + int(round(price_difference * 0.6))
                    else:
                        item_max_shop_price = base_price + int(round(price_difference * 0.2))
                elif by_location:
                    item_min_shop_price = location_price
                    item_max_shop_price = location_price

                if not remote_items and item_min_shop_price < item_intrinsic_value // 2:
                    item_min_shop_price = item_intrinsic_value // 2

                address = location.rom_addresses[0] + 1
                shop_price = world.random.randint(item_min_shop_price, item_max_shop_price) \
                    if item_max_shop_price > item_min_shop_price else item_min_shop_price
                logging.debug(f"Setting ¥{shop_price} for {location.name}")
                shop_price_bytes = shop_price.to_bytes(2, "little")
                write_bytes(shop_price_bytes, address)

    world.finished_level_scaling.wait()

    for _, pkmn_data in world.generated_static.items():
        pokemon_id = data.pokemon[pkmn_data.pokemon].id
        if pkmn_data.level_type == "gamecorner":
            addresses = pkmn_data.addresses[:-1]
        else:
            addresses = pkmn_data.addresses

        for address in addresses:
            cur_address = data.rom_addresses[address] + 1
            write_bytes([pokemon_id], cur_address)

        if pkmn_data.level_type == "gamecorner":
            static_name = world.generated_pokemon[pkmn_data.pokemon].friendly_name.upper()
            static_name = "NIDORAN♀" if static_name == "NIDORAN F" else static_name
            static_name = "NIDORAN♂" if static_name == "NIDORAN M" else static_name
            static_text = convert_to_ingame_text(static_name)

            write_bytes(static_text, data.rom_addresses[pkmn_data.addresses[-1]])

        if pkmn_data.level_address is not None:
            if pkmn_data.level_type in ("givepoke", "loadwildmon", "gamecorner"):
                write_bytes([pkmn_data.level], data.rom_addresses[pkmn_data.level_address] + 2)
            elif pkmn_data.level_type == "custom":
                write_bytes([pkmn_data.level], data.rom_addresses[pkmn_data.level_address] + 1)

    if world.options.randomize_trades:
        trade_table_address = data.rom_addresses["AP_Setting_TradeTable"]
        for trade in world.generated_trades.values():
            trade_address = trade_table_address + (trade.index * 32)  # each trade record is 32 bytes
            requested = data.pokemon[trade.requested_pokemon].id
            write_bytes([requested], trade_address + 1)

            received = data.pokemon[trade.received_pokemon].id
            write_bytes([received], trade_address + 2)

            write_bytes([trade.requested_gender], trade_address + 30)

            item_id = item_const_name_to_id(trade.held_item)
            write_bytes([item_id], trade_address + 16)

    # Always set the three lucky number targets. When the option is on they are the chosen trades'
    # OT IDs; when off they are random IDs so the (unconfigured) show can't match a zero-ID mon.
    targets_address = data.rom_addresses["AP_Setting_LuckyNumberTargets"]
    if world.options.randomize_lucky_number_show:
        target_ids = [world.generated_trades[trade_id].ot_id for trade_id in world.generated_lucky_number_trades]
    else:
        target_ids = [world.random.randint(1, 0xFFFF) for _ in range(3)]
    for i, ot_id in enumerate(target_ids):
        write_bytes([ot_id >> 8, ot_id & 0xFF], targets_address + i * 2)  # big-endian, matches MON_ID

    if world.options.randomize_starters:
        for j, pokemon in enumerate(["CYNDAQUIL_", "TOTODILE_", "CHIKORITA_"]):
            pokemon_id = data.pokemon[world.generated_starters[j][0]].id
            starter_name = world.generated_pokemon[world.generated_starters[j][0]].friendly_name.upper()
            starter_name = "NIDORAN♀" if starter_name == "NIDORAN F" else starter_name
            starter_name = "NIDORAN♂" if starter_name == "NIDORAN M" else starter_name
            starter_text = convert_to_ingame_text(starter_name)
            for i in range(1, 9):
                cur_address = data.rom_addresses["AP_Starter_" + pokemon + str(i)] + 1
                write_bytes([pokemon_id], cur_address)
                if i == 4:
                    helditem = item_const_name_to_id(world.generated_starter_helditems[j])
                    write_bytes([helditem], cur_address + 2)
                if i == 8:
                    helditem = item_const_name_to_id(world.generated_starter_helditems[j])
                    write_bytes([helditem], cur_address + 10)
            for i in range(9, 10):
                cur_address = data.rom_addresses["AP_Starter_" + pokemon + str(i)]
                write_bytes(starter_text + [0x7f] * (10 - len(starter_text)), cur_address)

    for region_key, encounters in world.generated_wild.items():
        if region_key.encounter_type is EncounterType.Grass:
            base_address = data.rom_addresses[f"AP_WildGrass_{region_key.region_id}"] + 3
            slot_size = len(encounters) * 2

            if region_key.time_of_day is not None:
                # ToD mode: write to the specific time slot
                cur_address = base_address + (region_key.time_of_day.ordinal * slot_size)
                for encounter in encounters:
                    pokemon_id = data.pokemon[encounter.pokemon].id
                    write_bytes([encounter.level, pokemon_id], cur_address)
                    cur_address += 2
            else:
                # Legacy mode: write same data to all 3 time slots
                cur_address = base_address
                for _ in range(3):  # morn, day, nite
                    for encounter in encounters:
                        pokemon_id = data.pokemon[encounter.pokemon].id
                        write_bytes([encounter.level, pokemon_id], cur_address)
                        cur_address += 2

        elif region_key.encounter_type is EncounterType.Water:
            cur_address = data.rom_addresses[f"AP_WildWater_{region_key.region_id}"] + 1
            for encounter in encounters:
                pokemon_id = data.pokemon[encounter.pokemon].id
                write_bytes([encounter.level, pokemon_id], cur_address)
                cur_address += 2

        elif region_key.encounter_type is EncounterType.Fish:
            fish_base = data.rom_addresses[f"AP_FishMons_{region_key.region_id}"]
            if region_key.fishing_rod is FishingRodType.Good:
                fish_base += 9  # skip the first 3 encounters, each encounter is 3 bytes
            elif region_key.fishing_rod is FishingRodType.Super:
                fish_base += 21  # skip the first 7 encounters
            time_fish_base = data.rom_addresses["AP_FishMons_TimeFish"]
            time_slot_list = data.fish_time_slots.get((region_key.region_id, region_key.fishing_rod), ())

            if region_key.time_of_day is FishTimeOfDay.Nite:
                # Nite keys hold only the time-varying slots, in slot-index order
                for (_, time_group_index), encounter in zip(time_slot_list, encounters, strict=True):
                    pokemon_id = data.pokemon[encounter.pokemon].id
                    write_bytes([pokemon_id, encounter.level], time_fish_base + time_group_index * 4 + 2)
            else:
                time_slots = dict(time_slot_list)
                write_nite = region_key.time_of_day is None
                for i, encounter in enumerate(encounters):
                    pokemon_id = data.pokemon[encounter.pokemon].id
                    if i in time_slots:
                        tg_addr = time_fish_base + time_slots[i] * 4
                        write_bytes([pokemon_id, encounter.level], tg_addr)
                        if write_nite:
                            write_bytes([pokemon_id, encounter.level], tg_addr + 2)
                    else:
                        write_bytes([pokemon_id, encounter.level], fish_base + i * 3 + 1)

        elif region_key.encounter_type is EncounterType.Tree:
            cur_address = data.rom_addresses[f"TreeMonSet_{region_key.region_id}"]
            if region_key.rarity is TreeRarity.Rare:
                cur_address += 19  # skip the first 6 encounters + terminator byte, each encounter is 3 bytes
            for encounter in encounters:
                cur_address += 1
                pokemon_id = data.pokemon[encounter.pokemon].id
                write_bytes([pokemon_id, encounter.level], cur_address)
                cur_address += 2

        elif region_key.encounter_type is EncounterType.RockSmash:
            cur_address = data.rom_addresses["TreeMonSet_Rock"]
            for encounter in encounters:
                cur_address += 1
                pokemon_id = data.pokemon[encounter.pokemon].id
                write_bytes([pokemon_id, encounter.level], cur_address)
                cur_address += 2

    wooper_sprite_address = data.rom_addresses["AP_Setting_Intro_Wooper_1"] + 1
    wooper_cry_address = data.rom_addresses["AP_Setting_Intro_Wooper_2"] + 1
    wooper_id = data.pokemon[world.generated_wooper].id
    write_bytes([wooper_id], wooper_sprite_address)
    write_bytes([wooper_id], wooper_cry_address)


    if world.options.randomize_berry_trees:
        write_bytes([1], data.rom_addresses["AP_Setting_BerryTrees"] + 1)
        # 0xC9 = ret
        write_bytes([0xC9], data.rom_addresses["AP_Setting_FruitTreesReset"])

    if world.options.modify_palettes == ModifyPalettes.option_swap_shiny:
        write_bytes([1], data.rom_addresses["AP_Setting_SwapShinyPalettes"] + 1)

    for move_name, move in world.generated_moves.items():  # effect modification is also possible but not included
        if move_name in ("NO_MOVE", "CURSE"):
            continue

        address = data.rom_addresses["AP_MoveData_Type_" + move_name]
        move_category_type = [world.generated_types[move.type].rom_id | move.category]
        write_bytes(move_category_type, address)

        address = data.rom_addresses["AP_MoveData_Power_" + move_name]
        write_bytes([move.power], address)  # power 20-150

        address = data.rom_addresses["AP_MoveData_PP_" + move_name]
        write_bytes([move.pp], address)  # 5-40 PP

        address = data.rom_addresses["AP_MoveData_Accuracy_" + move_name]
        acc = int(move.accuracy * 255 / 100)
        write_bytes([acc], address)  # accuracy 30-100

    # Hidden Power: select runtime category dispatch in engine/battle/hidden_power.asm.
    # The default (0) keeps vanilla Gen 2 behavior (always Special).
    split = world.options.physical_special_split
    if split == PhysicalSpecialSplit.option_random_by_move:
        # Use the stored category byte already written above.
        write_bytes([0x01], data.rom_addresses["AP_Setting_HiddenPowerCategoryMode"] + 1)
    elif split == PhysicalSpecialSplit.option_random_by_type:
        write_bytes([0x02], data.rom_addresses["AP_Setting_HiddenPowerCategoryMode"] + 1)
        # Per-type category lookup table indexed by rolled type id.
        table = bytearray([MoveCategory.Special] * 32)
        for type_name in world.generated_physical_types:
            rom_id = world.generated_types[type_name].rom_id
            assert rom_id < len(table), \
                f"type {type_name} rom_id {rom_id} exceeds HiddenPowerCategoryTable size"
            table[rom_id] = MoveCategory.Physical
        write_bytes(bytes(table), data.rom_addresses["AP_Setting_HiddenPowerCategoryTable"])

    # Hidden Power: in Gen 6+ buff modernization, use the move's stored power
    # (60) instead of the DV-based power formula.
    modernise_gen = world.options.modernise_moves_generation.value
    apply_buffs = world.options.modernise_moves_type != ModerniseMovesType.option_nerfs_only
    if modernise_gen >= 6 and apply_buffs:
        write_bytes([0x01], data.rom_addresses["AP_Setting_HiddenPowerPowerMode"] + 1)

    if world.options.modify_palettes in (ModifyPalettes.option_randomize, ModifyPalettes.option_match_types):
        write_palettes = write_bytes
    elif world.options.modify_palettes == ModifyPalettes.option_gold_and_silver:
        def write_palettes(pal, addr):
            for i, color in enumerate(pal):
                if color is None: continue
                write_bytes(color, addr + 2*i)

    for pkmn_name, pkmn_data in world.generated_pokemon.items():
        address = data.rom_addresses["AP_Stats_Types_" + pkmn_name]
        if world.options.randomize_types.value:
            pkmn_types = [pkmn_data.types[0], pkmn_data.types[-1]]
            type_ids = [world.generated_types[pkmn_types[0]].rom_id, world.generated_types[pkmn_types[1]].rom_id]
            write_bytes(type_ids, address)

        address += 15  # growth rate lives 15 bytes after type1
        write_bytes([pkmn_data.growth_rate], address)

        if world.options.randomize_base_stats.value:
            address = data.rom_addresses["AP_Stats_Base_" + pkmn_name]
            write_bytes(pkmn_data.base_stats, address)

        if world.options.randomize_evolution:
            address = data.rom_addresses["AP_Evos_" + pkmn_name]
            for evo in pkmn_data.evolutions:
                evo_pkmn_id = data.pokemon[evo.pokemon].id
                if evo_pkmn_id == pkmn_name:
                    if len(evo.evo_type) < 4:
                        # Edge case: no valid evolution found, is not Tyrogue
                        write_bytes([evo.evo_type.value, evo.condition, evo_pkmn_id], address)
                        address += len(evo.evo_type)
                    else:
                        # Edge case: no valid evolution found, is Tyrogue
                        write_bytes([evo.evo_type.value, evo.level], address)
                        write_bytes([evo_pkmn_id], address + 3)
                        address += len(evo.evo_type)
                else:
                    # Normal case
                    address += len(evo.evo_type) - 1
                    # Enums over evolution conditions would be needed to write the whole evolution data for all cases
                    write_bytes([evo_pkmn_id], address)
                    address += 1

        if world.options.maximum_evolution_level.value < 100:
            address = data.rom_addresses["AP_Evos_" + pkmn_name]
            for evo in pkmn_data.evolutions:
                if evo.evo_type in (EvolutionType.Level, EvolutionType.Stats):
                    write_bytes([evo.level], address + 1)  # level is always byte 1 for Level and Stats evolutions
                address += len(evo.evo_type)

        if world.options.randomize_learnsets.value:
            address = data.rom_addresses["AP_Attacks_" + pkmn_name]
            for move in pkmn_data.learnset:
                move_id = data.moves[move.move].rom_id
                write_bytes([move.level, move_id], address)
                address += 2

        if pkmn_name in world.generated_palettes:
            palettes = world.generated_palettes[pkmn_name]
            address = data.rom_addresses["AP_Stats_Palette_" + pkmn_name]
            write_palettes(palettes, address)

        tm_bytes = [0, 0, 0, 0, 0, 0, 0, 0]
        for tm in pkmn_data.tm_hm:
            tm_num = data.tmhm[tm].tm_num
            tm_bytes[int((tm_num - 1) / 8)] |= 1 << (tm_num - 1) % 8
        tm_address = data.rom_addresses["AP_Stats_TMHM_" + pkmn_name]
        write_bytes(tm_bytes, tm_address)

    if world.options.randomize_type_chart:
        for type_id, type_data in world.generated_types.items():
            address = data.rom_addresses["AP_Setting_TypeMatchups_" + type_id] - 1
            for _, matchup in sorted(
                    type_data.matchups.items(), key=lambda matchup: world.generated_types[matchup[0]].rom_id):
                address += 3
                write_bytes([matchup], address)

    if world.options.randomize_breeding:
        base_address = data.rom_addresses["AP_Setting_EggMons"]

        for pokemon_data in world.generated_pokemon.values():
            index = pokemon_data.id - 1
            produces_egg_id = world.generated_pokemon[pokemon_data.produces_egg].id
            write_bytes([produces_egg_id], base_address + index)

    for trainer_name, trainer_data in world.generated_trainers.items():
        address = data.rom_addresses["AP_TrainerParty_" + trainer_name]
        address += trainer_data.name_length + 1  # skip name and type
        for pokemon in trainer_data.pokemon:
            pokemon_data = [pokemon.level, data.pokemon[pokemon.pokemon].id]
            if pokemon.item is not None:
                item_id = item_const_name_to_id(pokemon.item)
                pokemon_data.append(item_id)
            for move in pokemon.moves:
                move_id = data.moves[move].rom_id
                pokemon_data.append(move_id)
            write_bytes(pokemon_data, address)
            address += len(pokemon_data)

    if world.options.randomize_tm_moves.value or world.options.metronome_only.value or world.options.tm_plando.value:
        tm_moves = [tm_data.move_id for _name, tm_data in world.generated_tms.items()]
        address = data.rom_addresses["AP_Setting_TMMoves"]
        write_bytes(tm_moves, address)

        address = data.rom_addresses["AP_Setting_GoldenrodMoveTutorMoveNames"]
        for tm in ("FLAMETHROWER", "THUNDERBOLT", "ICE_BEAM"):
            move_data = world.generated_moves[world.generated_tms[tm].id]
            move_name = convert_to_ingame_text(move_data.name + " " * (12 - len(move_data.name)),
                                               string_terminator=True)
            write_bytes(move_name, address)
            address += 13

        for tm in ("FLAMETHROWER", "THUNDERBOLT", "ICE_BEAM"):
            move_id = world.generated_tms[tm].move_id
            address = data.rom_addresses["AP_Setting_MoveTutor_" + tm] + 1
            write_bytes([move_id], address)

    if world.options.enable_mischief:
        if MiscOption.FuchsiaGym.value in world.generated_misc.selected:
            address = data.rom_addresses["AP_Misc_FuchsiaTrainers"] + 1
            write_bytes([0x0a], address + 2)  # spin speed
            for c in world.generated_misc.fuchsia_gym_trainers:
                write_coords = [c[1] + 4, c[0] + 4]
                write_bytes(write_coords, address)
                address += 13

        if MiscOption.SaffronGym.value in world.generated_misc.selected:
            for pair in world.generated_misc.saffron_gym_warps.pairs:
                addresses = [data.rom_addresses["AP_Misc_SaffronGymWarp_" + warp] + 2 for warp in pair]
                ids = [world.generated_misc.saffron_gym_warps.warps[warp].id for warp in pair]
                write_bytes([ids[1]], addresses[0])  # reverse ids
                write_bytes([ids[0]], addresses[1])

        if MiscOption.EcruteakGym.value in world.generated_misc.selected:
            address = data.rom_addresses["AP_Misc_Ecruteak_Gym_Warp"]
            write_bytes([2, 5], address)

        if MiscOption.OhkoMoves.value in world.generated_misc.selected:
            for move in ("GUILLOTINE", "HORN_DRILL", "FISSURE"):
                address = data.rom_addresses["AP_MoveData_Effect_" + move]
                write_bytes([0x65], address)  # false swipe effect
                address = data.rom_addresses["AP_MoveData_Power_" + move]
                write_bytes([0xFF], address)  # power 255
                address = data.rom_addresses["AP_MoveData_Accuracy_" + move]
                write_bytes([0xFF], address)  # accuracy 100%
                address = data.rom_addresses["AP_MoveData_PP_" + move]
                write_bytes([0x14], address)  # 20 PP

        if MiscOption.RadioTowerQuestions.value in world.generated_misc.selected:
            address = data.rom_addresses["AP_Misc_RadioTower_Sfx_N"] + 1
            # bad pokedex rating jingle
            write_bytes([0x9F], address)
            address = data.rom_addresses["AP_Misc_RadioTower_Sfx_Y2"] + 1
            # increasing pokedex rating jingles
            write_bytes([0xA0], address)
            address = data.rom_addresses["AP_Misc_RadioTower_Sfx_Y3"] + 1
            write_bytes([0xA1], address)
            address = data.rom_addresses["AP_Misc_RadioTower_Sfx_Y4"] + 1
            write_bytes([0xA2], address)
            address = data.rom_addresses["AP_Misc_RadioTower_Sfx_Y5"] + 1
            write_bytes([0xA3], address)
            for i in range(0, 5):
                answer = world.generated_misc.radio_tower_questions[i]
                # # 0x08 is iffalse (.WrongAnswer), 0x09 is iftrue (.WrongAnswer)
                byte = 0x08 if answer == "Y" else 0x09
                address = data.rom_addresses["AP_Misc_RadioTower_Q" + str(i + 1)]
                write_bytes([byte], address)

        if MiscOption.FanClubChairman.value in world.generated_misc.selected:
            # gives the chairman a 15/16 chance of repeating the rapidash rant each time
            address = data.rom_addresses["AP_Misc_Rapidash_Loop"] + 1
            write_bytes([1], address)

        if MiscOption.Amphy.value in world.generated_misc.selected:
            address = data.rom_addresses["AP_Misc_Amphy"] + 1
            write_bytes([1], address)

        if MiscOption.SecretSwitch.value in world.generated_misc.selected:
            address = data.rom_addresses["AP_Misc_SecretSwitch"] + 1
            write_bytes([1], address)

        if MiscOption.RedGyarados.value in world.generated_misc.selected:
            address = data.rom_addresses["AP_Misc_RedGyarados"] + 1
            write_bytes([1], address)

        if MiscOption.RadioChannels.value in world.generated_misc.selected:
            address = data.rom_addresses["AP_Misc_RadioChannels"]
            for channel_addr in world.generated_misc.radio_channel_addresses:
                write_bytes(channel_addr.to_bytes(2, "little"), address + 1)
                address += 3

        if MiscOption.MomItems.value in world.generated_misc.selected:
            address = data.rom_addresses["AP_Misc_MomItems"]
            for mom_item in world.generated_misc.mom_items:
                write_bytes([item_const_name_to_id(mom_item.item)], address + (8 * mom_item.index) + 7)

        if world.options.momsanity:
            # AP drives these slots via the patched item byte (+7), so force the kind
            # byte (+6) to MOM_ITEM (1). Otherwise a real item shuffled onto one of the
            # MOM_DOLL milestones would hit Mom_GiveItemOrDoll's vanilla doll fallback
            # and be misread as a decoration id.
            for i in range(10):
                write_bytes([1], data.rom_addresses[f"AP_MomMilestone_{i}"] - 1)

            # Let Mom call after battles even where there's no phone service (caves,
            # dungeons), so milestone checks aren't gated on the player's location.
            write_bytes([1], data.rom_addresses["AP_Momsanity"] + 1)

        if MiscOption.IcePath.value in world.generated_misc.selected:
            write_bytes([13, 3], data.rom_addresses["AP_Misc_IcePathWarp_1"])
            write_bytes([13, 13], data.rom_addresses["AP_Misc_IcePathWarp_2"])

        if MiscOption.TooManyDogs.value in world.generated_misc.selected:
            write_bytes([1], data.rom_addresses["AP_Misc_TooManyDogs"] + 1)

        if MiscOption.Farfetchd.value in world.generated_misc.selected:
            write_bytes([1], data.rom_addresses["AP_Misc_Farfetchd"] + 1)

        if MiscOption.Ledge.value in world.generated_misc.selected:
            write_bytes([1], data.rom_addresses["AP_Misc_Ledge"] + 1)

        if MiscOption.BlackthornGym.value in world.generated_misc.selected:
            write_bytes([1], data.rom_addresses["AP_Misc_BlackthornGym"] + 1)

        if MiscOption.TeleportingAbra.value in world.generated_misc.selected:
            write_bytes([1], data.rom_addresses["AP_Misc_TeleportingAbra"] + 1)

        if MiscOption.DB.value in world.generated_misc.selected:
            address = data.rom_addresses["AP_Misc_DB"] + 1
            write_bytes([1], address)

        if MiscOption.Chad.value in world.generated_misc.selected:
            write_bytes(convert_to_ingame_text(world.random.choice(AFRICAN_COUNTRIES).upper(), True),
                        data.rom_addresses["AP_Misc_KenyaName"])

        if MiscOption.Chuckster.value in world.generated_misc.selected:
            write_bytes([1], data.rom_addresses["AP_Misc_Chuckster"] + 1)

        if MiscOption.MahoganyGym.value in world.generated_misc.selected:
            replace_map_tiles(patch, "MahoganyGym", 2, 1, [0x32, 0x39])
            replace_map_tiles(patch, "MahoganyGym", 1, 2, [0x39, 0x39, 0x39])
            replace_map_tiles(patch, "MahoganyGym", 0, 4, [0x39])

        if MiscOption.DarkAreas.value in world.generated_misc.selected:
            write_bytes([1], data.rom_addresses["AP_Misc_DarkAreas"] + 1)

        if MiscOption.StatusMoves.value in world.generated_misc.selected:
            for label in ("AP_Misc_StatusMoves_Sleep", "AP_Misc_StatusMoves_Poison",
                          "AP_Misc_StatusMoves_StatDown", "AP_Misc_StatusMoves_Paralyze"):
                write_bytes([0], data.rom_addresses[label] + 1)

        if MiscOption.VermilionGym.value in world.generated_misc.selected:
            write_bytes([0], data.rom_addresses["AP_Misc_VermilionGymSwitch1"] + 2)
            write_bytes([0], data.rom_addresses["AP_Misc_VermilionGymSwitch2"] + 2)
            write_bytes([1], data.rom_addresses["AP_Misc_VermilionGymTraps_1"] + 1)
            write_bytes([1], data.rom_addresses["AP_Misc_VermilionGymTraps_2"] + 1)
            write_bytes([1], data.rom_addresses["AP_Misc_VermilionGymEventReset"] + 1)

        if MiscOption.UnLuckyEgg.value in world.generated_misc.selected:
            write_bytes([1], data.rom_addresses["AP_Misc_UnLuckyEgg"] + 1)
            write_bytes(convert_to_ingame_text("?"), data.rom_addresses["AP_Misc_LuckyEggDesc"] + 7)

        if MiscOption.Fuschia.value in world.generated_misc.selected:
            replace_map_tiles(patch, "FuchsiaCity", 2, 15, [0x07])
            replace_map_tiles(patch, "FuchsiaCity", 10, 15, [0x5C])

        if MiscOption.BlueBlue.value in world.generated_misc.selected:
            write_bytes([TrainerPalette.option_blue - 1], data.rom_addresses["AP_Misc_BlueBlue_SpriteColor"] + 5)
            text = convert_to_ingame_text("I'm blue", False)
            text.append(done_cmd)
            write_bytes(text, data.rom_addresses["AP_Misc_BlueBlue_Text"] + 1)

        if MiscOption.MountMoon.value in world.generated_misc.selected:
            SPRITE_SURFING_PIKACHU = 0x34

            # Patch the outdoor sprite group so the GFX are loaded into VRAM
            write_bytes([SPRITE_SURFING_PIKACHU], data.rom_addresses["AP_Misc_MountMoonFairy_GroupSprite"])

            # Write sprite bytes (1st byte of object_event data)
            write_bytes([SPRITE_SURFING_PIKACHU], data.rom_addresses["AP_Misc_MountMoonFairy1_Sprite"])
            write_bytes([SPRITE_SURFING_PIKACHU], data.rom_addresses["AP_Misc_MountMoonFairy2_Sprite"])

            # Write cry to Pikachu
            species_id = data.pokemon["PIKACHU"].id
            for i in range(1, 8):
                addr = data.rom_addresses[f"AP_Misc_MountMoonCry{i}"]
                write_bytes(species_id.to_bytes(2, "little"), addr + 1)

    if world.options.colored_item_balls:
        from BaseClasses import ItemClassification
        PAL_NPC_RED, PAL_NPC_BLUE, PAL_NPC_GREEN = 0x8, 0x9, 0xA
        TRAP_PALETTES = (PAL_NPC_RED, PAL_NPC_BLUE, PAL_NPC_GREEN)
        OBJECTTYPE_ITEMBALL = 0x1

        def palette_for_item(item) -> int:
            cls = item.classification
            if cls & ItemClassification.trap:
                return world.random.choice(TRAP_PALETTES)
            if cls & ItemClassification.progression:
                return PAL_NPC_GREEN
            if cls & ItemClassification.useful:
                return PAL_NPC_BLUE
            return PAL_NPC_RED

        itemball_locations = {
            loc_data.label: loc_data
            for loc_data in data.locations.values()
            if "Item Balls" in loc_data.tags
        }
        for location in world.multiworld.get_filled_locations(world.player):
            loc_data = itemball_locations.get(location.name)
            if loc_data is None:
                continue
            addr = data.rom_addresses.get(f"AP_ItemBall_{loc_data.scripts[0]}")
            if addr is None:
                continue
            palette = palette_for_item(location.item)
            write_bytes([(palette << 4) | OBJECTTYPE_ITEMBALL], addr)

    if world.options.randomize_music:
        for map_name, map_music in world.generated_music.maps.items():
            music_address = data.rom_addresses["AP_Music_" + map_name]
            # map music uses a single byte
            music_id = world.generated_music.consts[map_music].id
            if map_name.startswith("MAP_RadioTower"):
                music_id |= RADIO_TOWER_MUSIC
            write_bytes([music_id], music_address)
        for i, music_name in enumerate(world.generated_music.encounters):
            music_address = data.rom_addresses["AP_EncounterMusic"] + i
            write_bytes([world.generated_music.consts[music_name].id], music_address)
        for script_name, script_music in world.generated_music.scripts.items():
            music_address = data.rom_addresses["AP_Music_" + script_name] + 1
            music_id = world.generated_music.consts[script_music].id
            if script_name in SINGLE_BYTE_MUSIC_SCRIPTS:
                write_bytes([music_id], music_address)
            else:
                # script music is 2 bytes LE
                write_bytes(music_id.to_bytes(2, "little"), music_address)

    # Each HM badge entry is `dw mask` + `db regional`: the mask's low byte holds wJohtoBadges
    # bits, the high byte wKantoBadges bits; the regional flag gates the HM by region. Badge bit
    # positions follow badge_items order (first 8 Johto, next 8 Kanto), matching the ROM consts.
    badge_bits = {badge: bit for bit, badge in enumerate(world.logic.badge_items)}
    for hm in [hm for hm in world.options.remove_badge_requirement.valid_keys if not hm.startswith("_")]:
        hm_address = data.rom_addresses[f"AP_Setting_HMBadges_{hm}"]
        johto = world.logic.hm_badge_requirements_johto.get(hm.upper(), ())
        kanto = world.logic.hm_badge_requirements_kanto.get(hm.upper(), ())
        mask = 0
        for badge in set(johto) | set(kanto):
            mask |= 1 << badge_bits[badge]
        regional = 1 if set(johto) != set(kanto) else 0
        write_bytes(mask.to_bytes(2, "little") + bytes([regional]), hm_address)

    if world.options.hm_badge_requirements.value == HMBadgeRequirements.option_regional:
        write_bytes([1], data.rom_addresses["AP_Setting_RegionalHMBadges_1"] + 1)
        write_bytes([1], data.rom_addresses["AP_Setting_RegionalHMBadges_2"] + 1)

    write_bytes([world.options.victory_road_requirement.value],
                data.rom_addresses["AP_Setting_VictoryRoadRequirement"] + 1)
    write_bytes([world.options.victory_road_count.value], data.rom_addresses["AP_Setting_VictoryRoadCount_1"] + 1)
    write_bytes([world.options.victory_road_count.value], data.rom_addresses["AP_Setting_VictoryRoadCount_2"] + 1)
    write_bytes([world.options.victory_road_count.value], data.rom_addresses["AP_Setting_VictoryRoadCount_3"] + 1)
    write_bytes([world.options.victory_road_count.value], data.rom_addresses["AP_Setting_VictoryRoadCount_Text"] + 1)

    write_bytes([world.options.elite_four_requirement.value],
                data.rom_addresses["AP_Setting_EliteFourRequirement"] + 1)
    write_bytes([world.options.elite_four_count.value], data.rom_addresses["AP_Setting_EliteFourCount_1"] + 1)
    write_bytes([world.options.elite_four_count.value], data.rom_addresses["AP_Setting_EliteFourCount_2"] + 1)
    write_bytes([world.options.elite_four_count.value], data.rom_addresses["AP_Setting_EliteFourCount_3"] + 1)
    write_bytes([world.options.elite_four_count.value], data.rom_addresses["AP_Setting_EliteFourCount_Text"] + 1)
    write_bytes([world.options.elite_four_count.value], data.rom_addresses["AP_Setting_EliteFourCount_Callback"] + 1)
    write_bytes([1 if world.options.lance_requires_elite_four else 0],
                data.rom_addresses["AP_Setting_LanceKickOut"] + 1)

    write_bytes([world.options.radio_tower_requirement.value],
                data.rom_addresses["AP_Setting_RocketsRequirement"] + 1)
    write_bytes([world.options.radio_tower_count.value], data.rom_addresses["AP_Setting_RocketsCount"] + 1)

    for i in range(2):
        write_bytes([world.options.route_44_access_requirement.value],
                    data.rom_addresses[f"AP_Setting_Route44Requirement_{i + 1}"] + 1)
    for i in range(4):
        write_bytes([world.options.route_44_access_count.value],
                    data.rom_addresses[f"AP_Setting_Route44Count_{i + 1}"] + 1)

    write_bytes([world.options.mt_silver_requirement.value],
                data.rom_addresses["AP_Setting_MtSilverRequirement_Gate"] + 1)
    write_bytes([world.options.mt_silver_requirement.value],
                data.rom_addresses["AP_Setting_MtSilverRequirement_Oak"] + 1)
    write_bytes([world.options.mt_silver_count.value], data.rom_addresses["AP_Setting_MtSilverCount_Oak_1"] + 1)
    write_bytes([world.options.mt_silver_count.value], data.rom_addresses["AP_Setting_MtSilverCount_Oak_2"] + 1)
    write_bytes([world.options.mt_silver_count.value], data.rom_addresses["AP_Setting_MtSilverCount_Oak_Text"] + 1)
    write_bytes([world.options.mt_silver_count.value], data.rom_addresses["AP_Setting_MtSilverCount_Gate_1"] + 1)
    write_bytes([world.options.mt_silver_count.value], data.rom_addresses["AP_Setting_MtSilverCount_Gate_2"] + 1)
    write_bytes([world.options.mt_silver_count.value], data.rom_addresses["AP_Setting_MtSilverCount_Gate_Text"] + 1)

    write_bytes([world.options.red_requirement.value], data.rom_addresses["AP_Setting_RedRequirement"] + 1)
    write_bytes([world.options.red_count], data.rom_addresses["AP_Setting_RedCount_1"] + 1)
    write_bytes([world.options.red_count], data.rom_addresses["AP_Setting_RedCount_2"] + 1)

    if not world.options.johto_only:
        kanto_access_become_champion = [1] if (world.options.route_22_access_requirement.value
                                               == Route22AccessRequirement.option_become_champion) else [0]
        write_bytes(kanto_access_become_champion, data.rom_addresses["AP_Setting_KantoAccess_Champion"] + 1)

        kanto_access_wake_snorlax = [1] if (world.options.route_22_access_requirement.value
                                            == Route22AccessRequirement.option_wake_snorlax) else [0]
        write_bytes(kanto_access_wake_snorlax, data.rom_addresses["AP_Setting_KantoAccess_Snorlax"] + 1)

        write_bytes([world.options.route_22_access_requirement.value],
                    data.rom_addresses["AP_SettingKantoAccess_Requirement"] + 1)
        write_bytes([world.options.route_22_access_count.value],
                    data.rom_addresses["AP_Setting_KantoAccess_Count_1"] + 1)
        write_bytes([world.options.route_22_access_count.value],
                    data.rom_addresses["AP_Setting_KantoAccess_Count_2"] + 1)
        write_bytes([world.options.route_22_access_count.value],
                    data.rom_addresses["AP_Setting_KantoAccess_Count_Text"] + 1)

    if world.options.johto_trainersanity or world.options.kanto_trainersanity:
        # prevents disabling gym trainers, among a few others
        write_bytes([1], data.rom_addresses["AP_Setting_Trainersanity"] + 2)
        # removes events from certain trainers, to prevent disabling them.
        missable_trainers = ("GruntM29", "GruntM2", "GruntF1", "GruntM16", "ScientistJed", "GruntM17", "GruntM18",
                             "GruntM19", "RocketMurkrow", "SlowpokeGrunt", "RaticateGrunt", "ScientistRoss",
                             "ScientistMitch", "RocketBaseB3FRocket")

        for trainer in missable_trainers:
            # the dw at +11 is the event flag.
            write_bytes([0xFF, 0xFF], data.rom_addresses[f"AP_Setting_Trainersanity_{trainer}"] + 11)

    if world.options.rematchsanity:
        write_bytes([1], data.rom_addresses["AP_Setting_Rematchsanity"] + 2)

    for i, script in enumerate(world.generated_phone_traps):
        address = data.rom_addresses["AP_Setting_PhoneCallTrapTexts"] + (i * 0x400)
        s_bytes = script.get_script_bytes()
        # write script text
        write_bytes(s_bytes, address)
        # write script caller id
        address = data.rom_addresses["AP_Setting_SpecialCalls"] + (6 * i) + 2
        write_bytes([script.caller_id], address)

    phone_location_bytes = []
    for loc in world.generated_phone_indices:
        phone_location_bytes += list(loc.to_bytes(2, "little"))
    phone_location_address = data.rom_addresses["AP_Setting_Phone_Trap_Locations"]
    write_bytes(phone_location_bytes, phone_location_address)

    start_inventory_address = data.rom_addresses["AP_Start_Inventory"]
    start_inventory = defaultdict[str, int](int)
    for item in world.multiworld.precollected_items[world.player]:
        start_inventory[item.name] += 1

    # generate_early checks the options, but the generator panic method can also add items here
    problems = start_inventory_problems(world, start_inventory)
    if problems:
        raise AssertionError(f"{world.player_name}'s start inventory does not fit in the game: "
                             f"{'. '.join(problems)}")

    for item_name, quantity in start_inventory.items():
        item = world.create_item(item_name)
        if item.flag_index is not None:
            item_code = item_const_name_to_id("FLAG_ITEM")
            flag_index = item.flag_index
        else:
            item_code = item.code & CANONICAL_ITEM_ID_MASK
            flag_index = 0

        while quantity:
            stack = min(quantity, data.max_item_stack)
            write_bytes([item_code, stack, flag_index], start_inventory_address)
            quantity -= stack

            start_inventory_address += 3

    if world.options.free_fly_location.value in (FreeFlyLocation.option_free_fly,
                                                 FreeFlyLocation.option_free_fly_and_map_card):
        flypoint_bytes = max(fly_region.spawn_flag for fly_region in data.fly_regions) // 8 + 1
        free_fly_write = [0] * flypoint_bytes
        free_fly_flag = fly_flag_index(world, world.free_fly_location)
        free_fly_write[free_fly_flag // 8] |= (1 << (free_fly_flag % 8))
        write_bytes(free_fly_write, data.rom_addresses["AP_Setting_FreeFly"])

    if world.options.free_fly_location.value in (FreeFlyLocation.option_free_fly_and_map_card,
                                                 FreeFlyLocation.option_map_card):
        map_fly_flag = fly_flag_index(world, world.map_card_fly_location)
        map_fly_offset = (map_fly_flag // 8).to_bytes(2, "little")
        map_fly_byte = 1 << (map_fly_flag % 8)
        write_bytes([map_fly_byte], data.rom_addresses["AP_Setting_MapCardFreeFly_Byte"] + 1)
        write_bytes(map_fly_offset, data.rom_addresses["AP_Setting_MapCardFreeFly_Offset"] + 1)

    if world.options.remove_ilex_cut_tree:
        # Set cut tree tile to floor
        replace_map_tiles(patch, "IlexForest", 0, 11, [0x1])

    route_32_flag = world.options.route_32_condition.value
    write_bytes([route_32_flag], data.rom_addresses["AP_Setting_Route32_Condition_1"] + 1)
    write_bytes([route_32_flag], data.rom_addresses["AP_Setting_Route32_Condition_2"] + 1)
    write_bytes([route_32_flag], data.rom_addresses["AP_Setting_Route32_Condition_3"] + 1)

    if SaffronGatehouseTea.NORTH in world.options.saffron_gatehouse_tea.value:
        write_bytes([1], data.rom_addresses["AP_Setting_SaffronRoute5Blocked"] + 2)
    if SaffronGatehouseTea.EAST in world.options.saffron_gatehouse_tea.value:
        write_bytes([1], data.rom_addresses["AP_Setting_SaffronRoute8Blocked"] + 2)
    if SaffronGatehouseTea.SOUTH in world.options.saffron_gatehouse_tea.value:
        write_bytes([1], data.rom_addresses["AP_Setting_SaffronRoute6Blocked"] + 2)
    if SaffronGatehouseTea.WEST in world.options.saffron_gatehouse_tea.value:
        write_bytes([1], data.rom_addresses["AP_Setting_SaffronRoute7Blocked"] + 2)

    if world.options.saffron_gatehouse_tea.value:
        write_bytes([1], data.rom_addresses["AP_Setting_TeaEnabled"] + 1)

    if world.options.east_west_underground.value:
        write_bytes([1], data.rom_addresses["AP_Setting_EastWestUndergroundEnabled"] + 1)

    if world.options.undergrounds_require_power.value in (UndergroundsRequirePower.option_neither,
                                                          UndergroundsRequirePower.option_east_west):
        write_bytes([1], data.rom_addresses["AP_Setting_NorthSouthUndergroundOpen"] + 2)

    if (world.options.east_west_underground.value and
            world.options.undergrounds_require_power.value in (UndergroundsRequirePower.option_neither,
                                                               UndergroundsRequirePower.option_north_south)):
        write_bytes([1], data.rom_addresses["AP_Setting_EastWestUndergroundOpen"] + 2)

    if world.options.remote_items:
        write_bytes([1], data.rom_addresses["AP_Setting_RemoteItems"])

    progressive_tier_unlocks_active = world.options.battle_tower_progressive_tier_unlocks and (
        world.options.battle_tower_sanity or Goal.BATTLE_TOWER in world.options.goal)
    if not progressive_tier_unlocks_active:
        # Feature off: patch the tier-gate functions to early-return so they
        # behave as no-ops. Without the patch they'd treat the never-incremented
        # counter as the unlock count, locking every tier and shrinking the menu.
        write_bytes([0xc9], data.rom_addresses["AP_Setting_TierGate"])
        write_bytes([0xc9], data.rom_addresses["AP_Setting_AnyTierGate"])
        write_bytes([0xc9], data.rom_addresses["AP_Setting_TierMenuGate"])

    if not world.options.wonder_trading:
        write_bytes([0], data.rom_addresses["AP_Setting_WonderTrading"])

    if world.options.require_itemfinder.value == RequireItemfinder.option_hard_required:
        write_bytes([1], data.rom_addresses["AP_Setting_ItemfinderRequired"] + 1)

    if world.options.goal.value != {Goal.ELITE_FOUR}:
        write_bytes([1], data.rom_addresses["AP_Setting_SkipE4Credits"] + 1)

    if VanillaEventChains.CLAIR in world.options.vanilla_event_chains.value:
        write_bytes([1], data.rom_addresses["AP_Setting_VanillaClair"] + 2)

    if VanillaEventChains.JASMINE in world.options.vanilla_event_chains.value:
        write_bytes([1], data.rom_addresses["AP_Setting_VanillaJasmine"] + 1)

    if VanillaEventChains.COPYCAT in world.options.vanilla_event_chains.value:
        write_bytes([1], data.rom_addresses["AP_Setting_VanillaCopycat"] + 1)

    if VanillaEventChains.MISTY in world.options.vanilla_event_chains.value:
        write_bytes([1], data.rom_addresses["AP_Setting_VanillaMisty"] + 2)
        write_bytes([1], data.rom_addresses["AP_Setting_VanillaMistyGymRocket"] + 2)
        write_bytes([1], data.rom_addresses["AP_Setting_VanillaMistyMachinePartHidden"] + 2)
        write_bytes([1], data.rom_addresses["AP_Setting_VanillaMistyTrainers"] + 2)
        write_bytes([1], data.rom_addresses["AP_Setting_VanillaMistyRoute24Rocket"] + 2)
        write_bytes([0], data.rom_addresses["AP_Setting_VanillaMistyGymScene"] + 2)

    if world.options.victory_road_strength:
        write_bytes([0], data.rom_addresses["AP_Setting_VictoryRoadBoulder"] + 2)

    if world.options.route_2_access.value == Route2Access.option_open:
        tiles = [0x01]  # ground
    elif world.options.route_2_access.value == Route2Access.option_ledge:
        tiles = [0x58, 0x0A]  # grass with left ledge, grass
    else:
        tiles = None

    if tiles:
        replace_map_tiles(patch, "Route2", 5, 1, tiles)

    if world.options.route_42_access.opens_mortar_connection:
        map_name = "MountMortar1FOutside"
        replace_map_tiles(patch, map_name, 9, 8, [0x1D])  # rocks above waterfall
        replace_map_tiles(patch, map_name, 9, 11, [0x37])  # cave entrance
        replace_map_tiles(patch, map_name, 8, 12, [0x25, 0x02, 0x26])  # shore
        replace_map_tiles(patch, map_name, 8, 13, [0x32, 0x27, 0x33])  # shore edge

        map_name = "MountMortar1FInside"
        replace_map_tiles(patch, map_name, 9, 23, [0x02])  # remove rocks
        replace_map_tiles(patch, map_name, 8, 24, [0x06, 0x24, 0x04])  # entrance corridor + warp tile
        replace_map_tiles(patch, map_name, 9, 25, [0x23])  # exit

    if world.options.route_42_access.value != Route42Access.option_vanilla:
        map_name = "Route42"
        replace_map_tiles(patch, map_name, 7, 3, [0x0A])  # west rock
        replace_map_tiles(patch, map_name, 8, 6, [0x3A])  # west buoys
        replace_map_tiles(patch, map_name, 8, 7, [0x34])  # west buoys
        replace_map_tiles(patch, map_name, 16, 3, [0x0A, 0x0A])  # east rocks
        if world.options.route_42_access.value == Route42Access.option_blocked:
            replace_map_tiles(patch, map_name, 8, 3, [0x38])  # west buoys
            replace_map_tiles(patch, map_name, 8, 4, [0x36])  # west buoys
            replace_map_tiles(patch, map_name, 18, 4, [0x0A])  # east rock
            replace_map_tiles(patch, map_name, 18, 3, [0x54])  # prettier shore edge
            replace_map_tiles(patch, map_name, 17, 4, [0x54])  # prettier shore edge
        else:
            replace_map_tiles(patch, map_name, 8, 4, [0x07])  # west whirlpool
            replace_map_tiles(patch, map_name, 18, 4, [0x07])  # east whirlpool

    if world.options.red_gyarados_access == RedGyaradosAccess.option_whirlpool:
        whirlpool_tile = 0x07
        rock_tile = 0x0A
        water_tile = 0x35
        map_name = "LakeOfRage"
        replace_map_tiles(patch, map_name, 8, 10, [rock_tile, whirlpool_tile, 0x39])
        replace_map_tiles(patch, map_name, 7, 11, [0x30, water_tile, water_tile, rock_tile])
        replace_map_tiles(patch, map_name, 7, 12, [0x31, whirlpool_tile, 0x3A, 0x31])
    elif world.options.red_gyarados_access == RedGyaradosAccess.option_shore:
        write_bytes([31], data.rom_addresses["AP_Setting_LakeOfRage_RED_GYARADOS"] + 1)

    if world.options.blackthorn_dark_cave_access.value == BlackthornDarkCaveAccess.option_waterfall:
        map_name = "DarkCaveVioletEntrance"
        replace_map_tiles(patch, map_name, 6, 0, [0x11, 0x10])
        replace_map_tiles(patch, map_name, 6, 1, [0x08, 0x0A])
        replace_map_tiles(patch, map_name, 6, 2, [0x0C, 0x0E, 0x27, 0x0C, 0x0D, 0x0E])
        replace_map_tiles(patch, map_name, 6, 3, [0x2D, 0x2F, 0x2C, 0x2D, 0x2E, 0x2F])
        replace_map_tiles(patch, map_name, 9, 4, [0x04, 0x06])

        map_name = "DarkCaveBlackthornEntrance"
        replace_map_tiles(patch, map_name, 2, 7, [0x02])
        replace_map_tiles(patch, map_name, 2, 8, [0x02])

    if world.options.national_park_access.value == NationalParkAccess.option_bicycle:
        write_bytes([1], data.rom_addresses["AP_Setting_NationalParkBicycle"] + 2)

    if world.options.route_3_access.value == Route3Access.option_boulder_badge:
        # This is a sprite event, so 0 shows the sprite
        write_bytes([0], data.rom_addresses["AP_Setting_PewterCityBadgeRequired_1"] + 2)
        # Don't set the scene to the noop scene
        write_bytes([0], data.rom_addresses["AP_Setting_PewterCityBadgeRequired_2"] + 2)

    if world.options.mount_mortar_access:
        # This is a sprite event, so 0 shows the sprite
        write_bytes([0], data.rom_addresses["AP_Setting_MountMortarRocks"] + 2)

    headbutt_seed = (world.multiworld.seed & 0xFFFF).to_bytes(2, "big")
    write_bytes(headbutt_seed[:1], data.rom_addresses["AP_Setting_TreeMonSeed_1"] + 1)
    write_bytes(headbutt_seed[1:], data.rom_addresses["AP_Setting_TreeMonSeed_2"] + 1)

    if world.options.randomize_starting_town or world.options.randomize_entrances:
        if world.options.randomize_starting_town:
            town_id = world.starting_town.id
        else:
            town_id = next(t for t in data.starting_towns if t.region_id == "REGION_NEW_BARK_TOWN").id
        # Point SPAWN_HOME at the starting town's outside pokecenter tile.
        outside = data.spawnpoints[town_id - 23]
        write_bytes(outside.to_bytes(), data.rom_addresses["AP_Spawn_Home"])

    if world.options.metronome_only:
        for i in range(4):
            write_bytes([1], data.rom_addresses[f"AP_Setting_MetronomeOnly_{i + 1}"] + 1)

    if world.options.randomize_entrances:
        post_flypoint_base = data.rom_addresses["AP_Spawns"]
        for index, map_const, x, y in POKECENTER_SPAWN_ENTRIES:
            group, map_id = data.map_constants[map_const]
            write_bytes([group, map_id, x, y], post_flypoint_base + index * 4)
        # sight range 0: spotting the player from behind the boulder softlocks the Kurt scene
        write_bytes([0], data.rom_addresses["AP_Setting_SlowpokeWell_GruntM1"] + 8)

    if world.options.randomize_fly_unlocks or world.options.randomize_fly_destinations:
        write_bytes([1], data.rom_addresses["AP_Setting_FlyUnlocksShuffled"] + 2)
        # Regions outside the fly pool are still visitable; queue NO_ITEM instead of the spawn id
        for fly_region in set(data.fly_regions) - set(get_fly_regions(world)):
            write_bytes([0], data.rom_addresses[f"AP_FlyUnlock_{fly_region.base_identifier}"])

    if world.options.enforce_wild_encounter_methods_logic:
        excluded = {WildEncounterMethodsRequired.BUG_CATCHING_CONTEST, WildEncounterMethodsRequired.SWARM}
        valid_methods = [key for key in WildEncounterMethodsRequired.valid_keys
                         if key not in excluded and not key.startswith("_")]
        assert len(valid_methods) == 5, valid_methods
        methods = [method in world.options.wild_encounter_methods_required.value for method in valid_methods]

        write_bytes(methods, data.rom_addresses["AP_Setting_AllowedCatchTypes"])

        if WildEncounterMethodsRequired.SWARM in world.options.wild_encounter_methods_required.value:
            write_bytes([1], data.rom_addresses["AP_Setting_AllowSwarmCatches"] + 1)

    swarm_species_region = {
        "Qwilfish":  "Qwilfish_Swarm",
        "Dunsparce": "Dunsparce_Swarm",
        "Yanma":     "Yanma_Swarm",
    }
    for trainer_mon, swarm_region_id in swarm_species_region.items():
        slot = next(
            (encounters[0]
             for key, encounters in world.generated_wild.items()
             if key.is_swarm and key.region_id == swarm_region_id and encounters),
            None,
        )
        if slot is None:
            continue
        species_id = world.generated_pokemon[slot.pokemon].id
        level = int(slot.level)
        encounter_species = data.rom_addresses.get(f"AP_SwarmEncounter_{trainer_mon}_Species")
        encounter_level = data.rom_addresses.get(f"AP_SwarmEncounter_{trainer_mon}_Level")
        if encounter_species is not None:
            write_bytes([species_id], encounter_species + 1)
        if encounter_level is not None:
            write_bytes([level], encounter_level + 1)
        for variant in ("Activate", "Deactivate"):
            addr = data.rom_addresses.get(f"AP_SwarmSpecies_{trainer_mon}_{variant}")
            if addr is not None:
                write_bytes([species_id], addr + 1)

    if world.options.randomize_pokemon_requests:
        for pokemon_index, pokemon in enumerate(world.generated_request_pokemon[:5]):
            pokemon_id = world.generated_pokemon[pokemon].id
            for i in range(3):
                write_bytes([pokemon_id],
                            data.rom_addresses[f"AP_Setting_BillsGrandpaRequested{pokemon_index + 1}_{i + 1}"] + 1)

        requesters = ["Beverly", "Derek", "Tiffany"]
        for pokemon_index, pokemon in enumerate(world.generated_request_pokemon[5:]):
            pokemon_id = world.generated_pokemon[pokemon].id
            requester = requesters[pokemon_index]
            for i in range(3):
                write_bytes([pokemon_id], data.rom_addresses[f"AP_Setting_{requester}Requested_{i + 1}"] + 1)

    if world.options.randomize_static_pokemon or world.options.randomize_evolution:
        mystery_egg_pokemon = world.generated_static[EncounterKey.static("EggTogepi")].pokemon
        togepi_evo_tree = sorted(get_pokemon_evolutions(world, mystery_egg_pokemon))
        for i, pokemon in enumerate(togepi_evo_tree):
            write_bytes([world.generated_pokemon[pokemon].id], data.rom_addresses["AP_TogepiEvoTree"] + i)
        write_bytes([0xff], data.rom_addresses["AP_TogepiEvoTree"] + len(togepi_evo_tree))

    if world.options.always_unlock_fly_destinations:
        write_bytes([1], data.rom_addresses["AP_Setting_FlyUnlocksQoLEnabled"] + 2)

    for map_group in [key for key in world.options.dark_areas.valid_keys if not key.startswith("_")]:
        maps = FLASH_MAP_GROUPS[map_group]
        for map in maps:
            map_data = data.maps[map]
            default_palette = map_data.palette if map_data.palette is not MapPalette.Dark else MapPalette.Nite
            resolved_palette = MapPalette.Dark if map_group in world.options.dark_areas else default_palette
            palette_byte = (map_data.phone_service << 4) | resolved_palette
            write_bytes([palette_byte], data.rom_addresses[f"AP_MapPalette_{map}"])

    if world.options.require_flash == RequireFlash.option_hard_required:
        write_bytes([1], data.rom_addresses["AP_Setting_FlashHardRequired"] + 1)

    if world.options.require_flash and ("Ilex Forest" in world.options.dark_areas):
        write_bytes([1], data.rom_addresses["AP_Setting_IlexRequiresFlash"] + 1)

    if "Dark Cave" not in world.options.dark_areas:
        _, address = rom_offset_to_address(data.rom_addresses["AP_Address_DarkCaveName"])
        # "DARK CAVE"[5:] == "CAVE"
        address_bytes = (address + 5).to_bytes(2, "little")
        write_bytes(address_bytes, data.rom_addresses["AP_Setting_DarkCaveName"] + 2)

    if world.options.field_moves_always_usable:
        write_bytes([1], data.rom_addresses["AP_Setting_FieldMovesAlwaysUsable_SetUp"] + 1)
        write_bytes([1], data.rom_addresses["AP_Setting_FieldMovesAlwaysUsable_CallMove"] + 1)
        write_bytes([1], data.rom_addresses["AP_Setting_FieldMovesAlwaysUsable_CheckTMHM"] + 1)
        write_bytes([1], data.rom_addresses["AP_Setting_FieldMovesAlwaysUsable_MustKnowFieldMove"] + 1)

    if world.options.route_12_access:
        write_bytes([0], data.rom_addresses["AP_Setting_Route12Sudowoodo"] + 2)
        if world.options.route_12_access.value == Route12Access.option_weird_tree_surf_block:
            # Due to limitations with map tiles, move Fisher Stephen's pier one block up to make things fit
            replace_map_tiles(patch, "Route12", 6, 10, [0x05, 0x05]) # pier
            replace_map_tiles(patch, "Route12", 6, 11, [0x78, 0x78]) # pier bottom
            replace_map_tiles(patch, "Route12", 6, 12, [0x6b, 0x6b, 0x6b, 0x15]) # rocks
            write_bytes([25], data.rom_addresses["AP_Setting_Route12SurfBlock_StephenPos"] + 1)
            _, text_address = rom_offset_to_address(data.rom_addresses["AP_Address_StephenMovedText"])
            text_address = text_address.to_bytes(2, "little")
            write_bytes(text_address, data.rom_addresses["AP_Setting_Route12SurfBlock_StephenText"] + 1)

    if world.options.magnet_train_access:
        write_bytes([1], data.rom_addresses["AP_Setting_VanillaMagnetTrain_1"] + 1)
        write_bytes([1], data.rom_addresses["AP_Setting_VanillaMagnetTrain_2"] + 1)

    dexcount = len(world.pokemon_pool.all_available)
    write_bytes([dexcount - 1], data.rom_addresses["AP_Setting_DiplomaCount"] + 1)
    write_bytes([dexcount], data.rom_addresses["AP_Setting_DiplomaCount_2"] + 1)

    for i, slot in enumerate(world.generated_contest):
        address = data.rom_addresses["AP_Setting_BugContestMons"] + (i * 4)  # contest entries are 4 bytes
        write_bytes([slot.percentage, world.generated_pokemon[slot.pokemon].id, slot.min_level, slot.max_level],
                    address)
    if world.options.randomize_bug_catching_contest:
        write_bytes([world.options.randomize_bug_catching_contest.value - 1],
                    data.rom_addresses["AP_Setting_BugContestMode"] + 1)

    for i in range(1, 5):
        write_bytes([world.options.ss_aqua_access.value],
                    data.rom_addresses[f"AP_Setting_ShipRequiresLighthouse_{i}"] + 1)

    write_bytes([world.options.phone_call_mode.value],
                data.rom_addresses["AP_Setting_PhoneCallMode"] + 1)

    write_bytes([world.options.require_pokegear_for_phone_numbers.value],
                data.rom_addresses["AP_Setting_PhoneRequiresGear_1"] + 1)
    write_bytes([world.options.require_pokegear_for_phone_numbers.value],
                data.rom_addresses["AP_Setting_PhoneRequiresGear_2"] + 1)

    for sign, unown in world.generated_unown_signs.items():
        write_bytes([ALL_UNOWN.index(unown) + 1], data.rom_addresses[f"AP_Sign_{sign}"] + 1)

    if Goal.UNOWN_HUNT in world.options.goal:
        write_bytes([1], data.rom_addresses["AP_Setting_AlphPuzzlesLocked"] + 1)

    if world.options.route_30_battle:
        standing_left = 8
        standing_right = 9

        write_bytes([27, 6, standing_right], data.rom_addresses["AP_Setting_Route30Battle_Joey"] + 1)
        write_bytes([standing_left], data.rom_addresses["AP_Setting_Route30Battle_Mikey"] + 3)
        write_bytes([27, 8, standing_left], data.rom_addresses["AP_Setting_Route30Battle_MikeysMon"] + 1)
        write_bytes([27, 7, standing_right], data.rom_addresses["AP_Setting_Route30Battle_JoeysMon"] + 1)

        left = 2
        move_left = 16 | left
        right = 3
        move_right = 16 | right
        write_bytes([move_right], data.rom_addresses["AP_Setting_Route30Battle_JoeysMonAttacks1"])
        write_bytes([move_left], data.rom_addresses["AP_Setting_Route30Battle_JoeysMonAttacks2"])
        write_bytes([move_left], data.rom_addresses["AP_Setting_Route30Battle_MikeysMonAttacks1"])
        write_bytes([move_right], data.rom_addresses["AP_Setting_Route30Battle_MikeysMonAttacks2"])

        write_bytes([right], data.rom_addresses["AP_Setting_Route30Battle_JoeyTurn"] + 2)
        write_bytes([left], data.rom_addresses["AP_Setting_Route30Battle_MikeyTurn"] + 2)

    all_pokemon_seen = 1 if world.options.all_pokemon_seen else 0
    write_bytes([all_pokemon_seen], data.rom_addresses["AP_Setting_AllPokemonSeen_1"] + 1)
    write_bytes([all_pokemon_seen], data.rom_addresses["AP_Setting_AllPokemonSeen_2"] + 1)

    def write_item_flag(location: LocationData):
        event = location.flag
        item_flag = data.items[location.default_item].flag_index
        write_bytes([item_flag], data.rom_addresses["AP_Setting_FlagItems_Table_Events"] + event)

    if world.options.randomize_badges == RandomizeBadges.option_vanilla:
        for location in [loc for loc in data.locations.values() if "Badge" in loc.tags]:
            write_item_flag(location)

    if world.options.randomize_pokegear == RandomizePokegear.option_false:
        for location in [loc for loc in data.locations.values() if "Pokegear" in loc.tags]:
            write_item_flag(location)

    if world.options.randomize_pokedex == RandomizePokedex.option_vanilla:
        for location in [loc for loc in data.locations.values() if "Pokedex" in loc.tags]:
            write_item_flag(location)

    if world.options.randomize_item_values or world.options.item_value_plando:
        for item_id, value in world.generated_item_values.items():
            item_const = data.items[item_id].item_const
            address = data.rom_addresses.get(f"AP_Item_Price_{item_const}", None)
            if address:
                write_bytes(value.to_bytes(2, "little"), address)

    write_battle_tower_uber_list(world, write_bytes)

    world_data = {
        "item_prices": world.generated_item_values,
        "battle_tower_trainer_permutation": world.battle_tower_trainer_permutation,
        "battle_tower_mon_seed": world.battle_tower_mon_seed,
        "skip_elite_four_overridable": ("Pokemon League" not in world.options.randomize_entrances.value
                                        and not world.options.skip_elite_four),
    }
    patch.write_file("world_data.json", json.dumps(world_data).encode("utf-8"))

    goal_name_map = {
        Goal.ELITE_FOUR: "Champion",
        Goal.RED: "Red",
        Goal.DIPLOMA: "Diploma",
        Goal.RIVAL: "Rival",
        Goal.DEFEAT_TEAM_ROCKET: "Rocket",
        Goal.UNOWN_HUNT: "Unown",
        Goal.BATTLE_TOWER: "BattleTower",
    }
    goal_queue = deque(sorted(world.options.goal, key=Goal.valid_keys.index))
    while len(goal_queue) > 0:
        goal_key = goal_queue.popleft()
        rom_name = goal_name_map[goal_key]
        write_bytes([1], data.rom_addresses[f"AP_Setting_Elm{rom_name}Goal"] + 1)
        if len(goal_queue) > 0:
            write_bytes([1], data.rom_addresses[f"AP_Setting_SegueAfter{rom_name}"] + 1)

    if world.options.enforce_breeding_methods_logic:
        if world.options.breeding_methods_required == BreedingMethodsRequired.option_none:
            write_bytes([0], data.rom_addresses["AP_Setting_DittoBreedingAllowed"] + 1)
            write_bytes([0], data.rom_addresses["AP_Setting_BreedingAllowed"] + 1)
        elif world.options.breeding_methods_required == BreedingMethodsRequired.option_with_ditto:
            write_bytes([0], data.rom_addresses["AP_Setting_BreedingAllowed"] + 1)

    write_bytes([world.options.route_30_access == Route30Access.option_mr_pokemon],
                data.rom_addresses["AP_Setting_Route30Access_MrPokemon"] + 1)
    write_bytes([world.options.route_30_access == Route30Access.option_mystery_egg],
                data.rom_addresses["AP_Setting_Route30Access_ElmsLab"] + 1)

    route_19_rocks = 2  # LANDSLIDE_CLEAR_ALWAYS
    route_21_rocks = 2  # LANDSLIDE_CLEAR_ALWAYS
    clear_requirement = 0 if world.options.south_kanto_condition == SouthKantoCondition.option_enter_south_kanto else 1
    if world.options.south_kanto_access.blocks_route_19:
        route_19_rocks = clear_requirement
    if world.options.south_kanto_access.blocks_route_21:
        route_21_rocks = clear_requirement

    write_bytes([route_19_rocks], data.rom_addresses["AP_Setting_Route19LandslideRemoval"] + 1)
    write_bytes([route_21_rocks], data.rom_addresses["AP_Setting_Route21LandslideRemoval"] + 1)

    if world.options.trainer_gender != TrainerGender.option_vanilla:
        trainer_gender = world.options.trainer_gender
        if trainer_gender == TrainerGender.option_randomize:
            trainer_gender -= world.random.randint(1, 2)
        write_bytes([trainer_gender - 1], data.rom_addresses["AP_Setting_PlayerGender"] + 1)

    if world.options.rival_name.value.strip() != "":
        rival_name = world.multiworld.player_name[world.generated_rival] if world.generated_rival != 0 \
                else world.options.rival_name.value
        rival_name_bytes = convert_to_ingame_text(rival_name[:7], string_terminator=True)
        write_bytes([1], data.rom_addresses["AP_Setting_DoNameRival"] + 1)
        write_bytes(rival_name_bytes, data.rom_addresses["AP_Setting_RivalName"])
        write_bytes([1], data.rom_addresses["AP_Setting_RivalNameIsSet"] + 1)

    write_customizable_options(world.options, write_bytes, must_write_option, world_data)

    # Set slot auth
    ap_version_text = convert_to_ingame_text(data.manifest.pokemon_crystal_version)[:19]
    ap_version_text.append(0x50)
    # truncated to 19 to preserve the "v" at the beginning
    write_bytes(world.auth, data.rom_addresses["AP_Seed_Auth"])
    write_bytes(data.manifest.world_version.encode("ascii")[:32], data.rom_addresses["AP_Version"])
    write_bytes(ap_version_text, data.rom_addresses["AP_Version_Text"] + 1)

    if world.options.route_23_restored:
        write_route_23_restored_warps(write_bytes)
    else:
        suppress_route_23_restored_wilds(write_bytes)

    if world.options.flooded_mine:
        show_flooded_mine_entrances(patch, write_bytes)
    else:
        suppress_flooded_mine_wilds(write_bytes)
        hide_flooded_mine_landmark(write_bytes)

    if world.er_pairings:
        write_bytes([1], data.rom_addresses["AP_Setting_EROn"] + 2)
        write_entrance_pairings(world, write_bytes)
        if world.options.skip_elite_four and "Pokemon League" not in world.options.randomize_entrances.value:
            write_skip_elite_four_lance_exit(write_bytes)

    if world.options.randomize_fly_destinations:
        sorted_flypoints = sorted(world.fly_destinations, key=lambda warp: data.maps[warp.map_name].landmark)
        if any(flypoint for flypoint in world.fly_destinations
               if data.maps[flypoint.map_name].landmark >= Landmark.PalletTown):
            kanto_start_index = next(i for i, flypoint in enumerate(sorted_flypoints)
                                     if data.maps[flypoint.map_name].landmark >= Landmark.PalletTown)
        else:
            kanto_start_index = len(world.fly_destinations)

        write_bytes([kanto_start_index], data.rom_addresses["AP_Setting_Last_Johto_Flypoint_1"] + 1)
        write_bytes([kanto_start_index - 1], data.rom_addresses["AP_Setting_Last_Johto_Flypoint_2"] + 1)
        _, flypoints_address = rom_offset_to_address(data.rom_addresses["AP_Address_Flypoints"])
        kanto_flypoints_address = (flypoints_address + 2 * kanto_start_index).to_bytes(2, "little")
        write_bytes(kanto_flypoints_address, data.rom_addresses["AP_Setting_First_Kanto_Flypoint_1"] + 1)
        write_bytes([kanto_start_index - 1], data.rom_addresses["AP_Setting_First_Kanto_Flypoint_2"] + 1)
        write_bytes([kanto_start_index], data.rom_addresses["AP_Setting_First_Kanto_Flypoint_3"] + 1)

        for i, flypoint in enumerate(world.fly_destinations, start=1):
            write_bytes(flypoint.spawn_data(), data.rom_addresses[f"AP_Flypoint_{i}_Spawn"])

            landmark = data.maps[flypoint.map_name].landmark
            flytable_index = sorted_flypoints.index(flypoint) + 1
            write_bytes([landmark, i - 1], data.rom_addresses[f"AP_Flypoint_{flytable_index}"])

            write_bytes(convert_to_ingame_text(f"FLY UNLOCK {i}", True), data.rom_addresses[f"AP_Flypoint_{i}_Name"])

        if not world.options.randomize_fly_unlocks:
            flag_item_byte = [item_const_name_to_id("FLAG_ITEM")]
            for i, fly_region in enumerate(get_fly_regions(world), start=1):
                write_bytes(flag_item_byte, data.rom_addresses[f"AP_FlyUnlock_{fly_region.base_identifier}"])
                event_flag = data.event_flags[f"EVENT_VISITED_{fly_region.base_identifier}"]
                write_bytes([i], data.rom_addresses["AP_Setting_FlagItems_Table_Events"] + event_flag)


    patch.write_file("token_data.bin", patch.get_token_binary())

    out_file_name = world.multiworld.get_out_file_name_base(world.player)
    patch.write(os.path.join(output_directory, f"{out_file_name}{patch.patch_file_ending}"))


def get_base_rom_as_bytes() -> bytes:
    with open(get_settings().pokemon_crystal_settings.rom_file, "rb") as infile:
        base_rom_bytes = bytes(infile.read())

    return base_rom_bytes
