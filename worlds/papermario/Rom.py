# from https://github.com/icebound777/PMR-SeedGenerator/blob/main/randomizer.py, pulled functions for rom-related stuff
import pkgutil

import bsdiff4

from . import PMItem
from .RomTable import RomTable
import os

from .data.itemlocation_replenish import replenishing_itemlocations
from .itemhints import get_itemhints
from .modules.random_actor_stats import get_shuffled_chapter_difficulty
from .modules.random_audio import get_randomized_audio
from .modules.random_formations import get_random_formations
from .modules.random_map_mirroring import get_mirrored_map_list
from .modules.random_movecosts import get_randomized_moves
from .modules.random_mystery import get_random_mystery
from .modules.random_palettes import get_randomized_palettes, get_randomized_coinpalette
from .data.MysteryOptions import MysteryOptions
from .modules.random_puzzles_minigames import get_puzzles_minigames
from .modules.random_quizzes import get_randomized_quizzes
from .options import EnemyDifficulty
from .data.ItemList import item_table, item_groups
from .data.node import Node
from .Locations import PMLocation
from .modules.random_shop_prices import get_shop_price
from .modules.random_stat_distribution import generate_random_stats
from .modules.modify_game_strings import multiworld_item_info_to_pmString
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes, APPatchExtension
from settings import get_settings

FILENAME_PMR_TOKEN_BINARY: str = "pmr_token_data.bin"

class PaperMarioPatchExtensions(APPatchExtension):
    game = "Paper Mario"

    @staticmethod
    def calculate_pm_crc(caller: APProcedurePatch, rom: bytes) -> bytes:
        rom_data = bytearray(rom)

        t1 = 0xA3886759  # 6103 only
        t2 = 0xA3886759  # 6103 only
        t3 = 0xA3886759  # 6103 only
        t4 = 0xA3886759  # 6103 only
        t5 = 0xA3886759  # 6103 only
        t6 = 0xA3886759  # 6103 only

        # Read contents to generate crc over
        read_pos = 0x1000
        for _ in range(0x100000//4):
            d = int.from_bytes(rom_data[read_pos:read_pos + 4], "big") & 0xFFFFFFFF

            if ((t6 + d) & 0xFFFFFFFF) < (t6 & 0xFFFFFFFF):
                t4 += 1
            t6 += d
            t3 ^= d
            r = (d << (d & 0x1F)) | (d >> (32 - (d & 0x1F))) & 0xFFFFFFFF
            t5 += r
            if (t2 & 0xFFFFFFFF) > (d & 0xFFFFFFFF):
                t2 ^= r
            else:
                t2 ^= (t6 ^ d)
            t1 += t5 ^ d

            read_pos += 4

        # Write new crc
        crc1 = ((t6 ^ t4) + t3) & 0xFFFFFFFF
        crc2 = ((t5 ^ t2) + t1) & 0xFFFFFFFF

        rom_data[0x10:0x14] = crc1.to_bytes(4, byteorder="big")
        rom_data[0x14:0x18] = crc2.to_bytes(4, byteorder="big")

        return rom_data


class PaperMarioProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Paper Mario"
    hash = "a722f8161ff489943191330bf8416496"
    patch_file_ending = ".appm64"
    result_file_ending = ".z64"

    procedure = [
        ("apply_bsdiff4", ["base_pmr_patch.bsdiff4"]),
        ("apply_tokens", [FILENAME_PMR_TOKEN_BINARY]),
        ("calculate_pm_crc", [])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_as_bytes()


def get_base_rom_as_bytes() -> bytes:
    with open(get_settings().paper_mario_settings.rom_file, "rb") as infile:
        base_rom_bytes = bytes(infile.read())

    return base_rom_bytes


def write_bytes(byte_array: bytearray, address: int, value: bytes) -> int:
    byte_array[address: address + len(value) - 1] = value
    return address + len(value)


def write_patch(
    output_directory: str,
    world,
    placed_items: list,
    entrance_list: list,
    enemy_stats: list,
    battle_formations: list,
    move_costs: list,
    itemhints: list,
    coin_palette_data: list,
    coin_palette_targets: list,
    coin_palette_crcs: list,
    palette_data: list,
    quiz_data: list,
    music_list: list,
    mapmirror_list: list,
    puzzle_list: list,
    mystery_opts: MysteryOptions,
    star_beam_area: int
):
    patch: PaperMarioProcedurePatch = PaperMarioProcedurePatch(
        player=world.player,
        player_name=world.player_name,
    )
    def write_single_token(
        cur_pos: int,
        bytes_to_write: bytes | bytearray
    ) -> int:
        if isinstance(bytes_to_write, bytearray):
            immutable_bytes = bytes(bytes_to_write)
        else:
            immutable_bytes = bytes_to_write
        patch.write_token(
            APTokenTypes.WRITE,
            cur_pos,
            immutable_bytes
        )
        return cur_pos + len(immutable_bytes)

    patch.write_file("base_pmr_patch.bsdiff4", pkgutil.get_data(__name__, "data/base_pmr_patch.bsdiff4"))

    seed_id = world.random.randint(0, 0xFFFFFFFF)

    # Create the ROM table
    rom_table = RomTable()
    rom_table.create()
    # Create a sorted list of key:value pairs to be written into the ROM
    table_data = rom_table.generate_pairs(
        options=world.options,
        placed_items=placed_items,
        entrances=entrance_list,
        actor_attributes=enemy_stats,
        move_costs=move_costs,
        palettes=palette_data,
        quizzes=quiz_data,
        music_list=music_list,
        mapmirror_list=mapmirror_list,
        puzzle_list=puzzle_list,
        mystery_opts=mystery_opts,
        required_spirits=world.required_spirits,
        battle_list=world.battle_list,
        star_beam_area=star_beam_area,
        trappable_item_names=world.trappable_item_names,
        random=world.random
    )

    # Update table info with variable data
    end_of_content_marker = 0x4  # end of table FFFFFFFF
    end_padding = 0x10  # 4x FFFFFFFF
    len_battle_formations = sum([len(formation) for formation in battle_formations])
    len_itemhints = sum([len(itemhint_word) for itemhint_word in itemhints])

    rom_table.info["db_size"] = (rom_table.info["header_size"]
                                 + (len(table_data) * 8)
                                 + (len_battle_formations * 4)
                                 + end_of_content_marker
                                 + (len_itemhints * 4)
                                 + end_of_content_marker
                                 + end_padding)
    rom_table.info["seed"] = seed_id
    rom_table.info["formations_offset"] = len(table_data) * 8
    rom_table.info["itemhints_offset"] = (rom_table.info["formations_offset"]
                                          + end_of_content_marker
                                          + (len_battle_formations * 4))

    # Modify the table data in the ROM

    # Set slot auth
    cur_pos: int = rom_table.info["auth_address"]
    cur_pos = write_single_token(
        cur_pos,
        world.auth
    )

    # Write the db header
    cur_pos = write_single_token(
        cur_pos,
        rom_table.info["magic_value"].to_bytes(4, byteorder="big")
    )
    cur_pos = write_single_token(
        cur_pos,
        rom_table.info["header_size"].to_bytes(4, byteorder="big")
    )
    cur_pos = write_single_token(
        cur_pos,
        rom_table.info["db_size"].to_bytes(4, byteorder="big")
    )
    cur_pos = write_single_token(
        cur_pos,
        rom_table.info["seed"].to_bytes(4, byteorder="big")
    )
    cur_pos = write_single_token(
        cur_pos,
        rom_table.info["formations_offset"].to_bytes(4, byteorder="big")
    )
    _ = write_single_token(
        cur_pos,
        rom_table.info["itemhints_offset"].to_bytes(4, byteorder="big")
    )

    # Write table data and generate log file
    cur_pos = rom_table.info["address"] + rom_table.info["header_size"]

    for _, pair in enumerate(table_data):
        key_int = pair["key"].to_bytes(4, byteorder="big")
        value_int = pair["value"].to_bytes(4, byteorder="big")
        cur_pos = write_single_token(
            cur_pos,
            key_int
        )
        cur_pos = write_single_token(
            cur_pos,
            value_int
        )

    for formation in battle_formations:
        for formation_hex_word in formation:
            cur_pos = write_single_token(
                cur_pos,
                formation_hex_word.to_bytes(4, byteorder="big")
            )

    # Write end of formations table
    cur_pos = write_single_token(
        cur_pos,
        0xFFFFFFFF.to_bytes(4, byteorder="big")
    )

    # Write itemhint table
    for itemhint in itemhints:
        for itemhint_hex in itemhint:
            cur_pos = write_single_token(
                cur_pos,
                itemhint_hex.to_bytes(4, byteorder="big")
            )

    # Write end of item hints table
    cur_pos = write_single_token(
        cur_pos,
        0xFFFFFFFF.to_bytes(4, byteorder="big")
    )

    # Write end of db padding
    for _ in range(1, 5):
        cur_pos = write_single_token(
            cur_pos,
            0xFFFFFFFF.to_bytes(4, byteorder="big")
        )

    # Write shop descriptions
    for node in placed_items:
        if node.shop_string_location != -1:
            _ = write_single_token(
                node.shop_string_location,
                bytes(node.shop_string)
            )

    # Special solution for random coin palettes
    if coin_palette_data and coin_palette_targets:
        for target_rom_location in coin_palette_targets:
            cur_pos = target_rom_location
            for palette_byte in coin_palette_data:
                cur_pos = write_single_token(
                    cur_pos,
                    palette_byte.to_bytes(4, byteorder="big")
                )

    # Write output
    patch.write_file(FILENAME_PMR_TOKEN_BINARY, patch.get_token_binary())

    out_file_name = world.multiworld.get_out_file_name_base(world.player)
    patch.write(os.path.join(output_directory, f"{out_file_name}{patch.patch_file_ending}"))


def generate_output(world, output_dir: str) -> None:

    # mario stats
    if world.options.random_start_stats.value:
        world.options.starting_hp.value, world.options.starting_fp.value, world.options.starting_bp.value = (
            generate_random_stats(world.options.random_start_stats_level.value, world.random))

    # enemy stats
    enemy_stats, chapter_changes = get_shuffled_chapter_difficulty(
        world.options.enemy_difficulty.value, world.options.starting_map.value, world.random)

    battle_formations = []

    if (world.options.formation_shuffle.value
            or world.options.enemy_difficulty.value == EnemyDifficulty.option_Progressive_Scaling):
        battle_formations = get_random_formations(chapter_changes,
                                                  world.options.enemy_difficulty.value ==
                                                  EnemyDifficulty.option_Progressive_Scaling,
                                                  world.random)

    # Coin palette values
    coin_palette_data, coin_palette_targets, coin_palette_crcs = (
        get_randomized_coinpalette(world.options.coin_palette.value))

    # Quizzes are always randomized
    quiz_data = get_randomized_quizzes(world.random)

    # randomized puzzles
    puzzle_list, world.spoilerlog_puzzles = get_puzzles_minigames(world.options.random_puzzles.value, world)

    # Default mystery options for now
    mystery_opts = get_random_mystery(world.options.mystery_shuffle.value, world.random)

    # Non-coin palettes
    palette_data = get_randomized_palettes(world)

    # Move costs
    move_costs = get_randomized_moves(world.options.badge_bp_shuffle.value,
                                      world.options.badge_fp_shuffle.value,
                                      world.options.partner_fp_shuffle.value,
                                      world.options.sp_shuffle.value,
                                      world.random)

    # Randomized music
    music_list = get_randomized_audio(world.options.shuffle_music.value,
                                      world.options.shuffle_jingles.value,
                                      world.random)

    # mirror mode is always off at the moment
    static_map_mirroring = get_mirrored_map_list()

    placed_items = get_filled_node_list(world)
    item_hints = get_itemhints(False, placed_items, world.options)

    star_beam_area = get_star_beam_area(world)

    write_patch(output_directory=output_dir,
                world=world,
                placed_items=placed_items,
                entrance_list=world.entrance_list,
                enemy_stats=enemy_stats,
                battle_formations=battle_formations,
                move_costs=move_costs,
                itemhints=item_hints,
                coin_palette_data=coin_palette_data,
                coin_palette_targets=coin_palette_targets,
                coin_palette_crcs=coin_palette_crcs,
                palette_data=palette_data,
                quiz_data=quiz_data,
                music_list=music_list,
                mapmirror_list=static_map_mirroring,
                puzzle_list=puzzle_list,
                mystery_opts=mystery_opts,
                star_beam_area=star_beam_area)


# Paper Mario Rando operates off of a node list with item IDs and prices
def get_filled_node_list(world):
    placed_items = []
    mw_keys = 0

    all_locations = [location for location in world.multiworld.get_locations(world.player)]
    all_locations.extend(world.ch_excluded_locations)

    for location in all_locations:

        if location.keyname is None:
            continue

        if location.item is None:
            continue

        pm_loc: PMLocation = location
        cur_node = Node()
        cur_node.map_id = pm_loc.map_id
        cur_node.area_id = pm_loc.area_id
        cur_node.key_name_item = pm_loc.keyname
        cur_node.item_source_type = pm_loc.source_type
        cur_node.vanilla_price = pm_loc.vanilla_price
        cur_node.item_index = pm_loc.index
        cur_node.price_index = pm_loc.price_index
        cur_node.identifier = pm_loc.identifier
        cur_node.item_classification = pm_loc.item.classification
        cur_node.item_player_name = world.multiworld.get_player_name(pm_loc.item.player)
        cur_node.item_name = pm_loc.item.name

        if pm_loc.price_keyname != "None":
            cur_node.key_name_price = pm_loc.price_keyname

        if pm_loc.item.player == world.player:
            cur_node.current_item = pm_loc.item
        else:
            # Multiworld items in replenishable locations get IDs that cause them to stop spawning after being obtained
            if cur_node.identifier in replenishing_itemlocations:
                mw_key_name = "MultiWorldKey" + f"{mw_keys:02x}".upper()
                cur_node.current_item = PMItem("MultiWorldItem", world.player, item_table[mw_key_name], False)
                mw_keys += 1

            # The rest can get the generic id
            else:
                cur_node.current_item = PMItem("MultiWorldItem", world.player, item_table["MultiWorldGeneric"], False)

        # set prices, descriptions for items in shops
        if "Shop" in cur_node.identifier:
            if pm_loc.item.player != world.player:
                cur_node.shop_string_location, cur_node.shop_string = (multiworld_item_info_to_pmString(
                                                     world.multiworld.get_player_name(pm_loc.item.player),
                                                     pm_loc.item.name,
                                                     pm_loc.item.classification,
                                                     cur_node.identifier))
            cur_node.current_item.base_price = get_shop_price(pm_loc,
                                                              cur_node.current_item,
                                                              world.options.include_shops.value,
                                                              world.options.merlow_rewards_pricing.value,
                                                              world.options.total_power_stars.value,
                                                              world.random)

        placed_items.append(cur_node)

    return placed_items


def get_star_beam_area(world):
    if world.options.shuffle_star_beam.value:
        item_locations = world.multiworld.find_item_locations("Star Beam", world.player)
        if item_locations:
            location = item_locations[0]
            # if the location is not in the player's game, the area must be an invalid one so fallback text is used
            if location.player != world.player:
                return 28
            # local star beam gets its area hinted
            else:
                loc: PMLocation = location
                return loc.area_id

    return 28
