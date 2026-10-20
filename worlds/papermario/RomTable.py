# from https://github.com/icebound777/PMR-SeedGenerator/blob/main/table.py

from .data.RomOptionList import rom_option_table, ap_to_rom_option_table
from .data.palettes_meta import MENU_COLORS
from .options import (
    EnemyDamage,
    PaperMarioOptions,
    PartnerUpgradeShuffle,
    ShuffleKootFavors,
    ShuffleLetters,
    BowserCastleMode,
    StatusMenuColorPalette,
    EnemyDifficulty,
    ShuffleSuperMultiBlocks
)
from .data.MysteryOptions import MysteryOptions
from .data.starting_maps import starting_maps
from .data.node import Node
from .items import PMItem
from .data.ItemList import item_groups, item_multiples_ids, item_table


class RomTable:
    instance = None
    default_db = {}
    db = {}
    info = {}

    def __init__(self):
        if RomTable.instance is None:
            RomTable.instance = self
        else:
            self = RomTable.instance

    def __getitem__(self, key):
        return self.db[key]

    def generate_pairs(
        self,
        options: PaperMarioOptions,
        placed_items: list[Node],
        entrances: list,
        actor_attributes: list,
        move_costs: list,
        palettes: list,
        quizzes: list,
        music_list: list,
        mapmirror_list: list,
        puzzle_list: list,
        mystery_opts: MysteryOptions,
        required_spirits: list,
        battle_list: list,
        star_beam_area: int,
        trappable_item_names: list,
        random,
    ):
        table_data = []

        # Options
        option_dbtuples = get_dbtuples(
            options,
            mystery_opts,
            required_spirits,
            star_beam_area
        )

        for option_data in option_dbtuples:
            option_key = option_data[0]
            option_value = option_data[1]
            if isinstance(option_value, int) and option_value < 0:
                option_value = 0x100000000 + option_value
            table_data.append({
                "key": option_key,
                "value": option_value,
            })

        # temp fix for multiworld
        table_data.append({
            "key": 0xAF050000,
            "value": 0x00000000
        })

        # Quizzes
        for key, value in quizzes:
            table_data.append({
                "key": key,
                "value": value
            })

        # Items
        repeat_items = {}
        for node in placed_items:
            if node.key_name_item is not None and node.current_item is not None:
                item_id = node.current_item.id
                # Progressive items default to their highest ids for in-game placement
                # When received, we receive the lowest IDs
                if item_id in item_multiples_ids.keys():
                    if item_id not in repeat_items.keys():
                        repeat_items[item_id] = len(item_multiples_ids[item_id]) - 1

                    item_id = item_multiples_ids[item_id][repeat_items[item_id]]
                    repeat_items[node.current_item.id] -= 1
                elif item_id == item_table["Damage Trap"][2]:
                    # damage traps are fire flowers by default, but if it's local
                    # we can set it to be a different item
                    trap_item = random.choice(trappable_item_names)
                    item_id = get_trapped_item_id(item_table[trap_item][2])

                table_data.append({
                    "key": node.get_item_key(),
                    "value": item_id,
                })

            # Item Prices
            if (node.key_name_price is not None
                and (node.key_name_price.startswith("ShopPrice")
                     or node.key_name_price.startswith("RewardAmount"))):
                table_data.append({
                    "key": node.get_price_key(),
                    "value": node.current_item.base_price
                })

        # Entrances
        for key, value in entrances:
            table_data.append({
                "key": key,
                "value": value
            })

        for key, value in battle_list:
            table_data.append({
                "key": key,
                "value": value
            })

        # Actor Attributes
        for key, value in actor_attributes:
            table_data.append({
                "key": key,
                "value": value
            })

        # Palettes
        for key, value in palettes:
            table_data.append({
                "key": key,
                "value": value
            })

        # Move Costs
        for key, value in move_costs:
            table_data.append({
                "key": key,
                "value": value
            })

        # Audio
        for key, value in music_list:
            table_data.append({
                "key": key,
                "value": value
            })

        # Map mirroring
        for key, value in mapmirror_list:
            table_data.append({
                "key": key,
                "value": value
            })

        # Puzzles & Minigames
        for key, value in puzzle_list:
            table_data.append({
                "key": key,
                "value": value
            })

        table_data.sort(key=lambda pair: pair["key"])
        return table_data

    def create(self):
        self.info = get_table_info()


def get_table_info():
    # Defaults
    table_info = {
        "magic_value": 0x504D4442,
        "header_size": 0x20,
        "db_size": 0,
        "seed": 0xDEADBEEF,
        "address": 0x1D00000,
        "formations_offset": 0,
        "itemhints_offset": 0,
        "auth_address": 0x1cffff0
    }

    return table_info


def generate_table_pairs(value_set):
    table_data = []

    for key, value in value_set:
        table_data.append({
            "key": key,
            "value": value
        })

    table_data.sort(key=lambda pair: pair["key"])
    return table_data


def get_dbtuples(
    options: PaperMarioOptions,
    mystery_opts: MysteryOptions,
    required_spirits: list,
    star_beam_area: int,
) -> list:
    dbtuples = []

    # map tracker check and shop bits
    map_tracker_bits = 0x1 + 0x2
    if options.shuffle_hidden_panels.value:
        map_tracker_bits += 0x4
    if options.partner_upgrades.value >= PartnerUpgradeShuffle.option_Super_Block_Locations:
        map_tracker_bits += 0x8
    if options.overworld_coins.value:
        map_tracker_bits += 0x10
    if options.coin_blocks.value:
        map_tracker_bits += 0x20
    if options.koot_coins.value:
        map_tracker_bits += 0x40
    if options.foliage_coins.value:
        map_tracker_bits += 0x80
    if options.dojo.value:
        map_tracker_bits += 0x100
    if options.koot_favors.value != ShuffleKootFavors.option_Vanilla:
        map_tracker_bits += 0x200
    if options.trading_events.value:
        map_tracker_bits += 0x400
    if options.letter_rewards.value != ShuffleLetters.option_Vanilla:
        map_tracker_bits += 0x800
    if not options.open_forest.value:
        map_tracker_bits += 0x1000
    if options.bowser_castle_mode.value == BowserCastleMode.option_Vanilla:
        map_tracker_bits += 0x2000
    if options.bowser_castle_mode.value <= BowserCastleMode.option_Shortened:
        map_tracker_bits += 0x4000
    if options.super_multi_blocks.value == ShuffleSuperMultiBlocks.option_Anywhere:
        map_tracker_bits += 0x8000

    map_tracker_check_bits = map_tracker_bits
    map_tracker_shop_bits = 0x7
    if options.bowser_castle_mode.value <= BowserCastleMode.option_Shortened:
        map_tracker_shop_bits += 0x8

    # status menu palette comes from multiple settings
    color_mode, menu_color_a, menu_color_b = MENU_COLORS[options.status_menu_palette.value]

    # if specific star spirits are required they need to be encoded
    encoded_spirits = 0
    for spirit in required_spirits:
        encoded_spirits = encoded_spirits | (1 << (spirit - 1))

    for rom_option, ap_option in ap_to_rom_option_table.items():
        option_key = get_db_key(rom_option)
        option_value = -1
        if ap_option == "":
            #  handle options that are calculated, not yet implemented, or
            # otherwise not changeable by the player
            match rom_option:
                # Always turned on
                case "BlocksMatchContent" | "FastTextSkip" | "ShuffleItems" | "RandomQuiz" \
                     | "PeachCastleReturnPipe" | "MultiworldEnabled":
                    option_value = 1
                # Always turned off
                case "ChallengeMode" | "ShuffleDungeonRooms" | "ShuffleEntrancesByAll" | "MatchEntranceTypes" \
                     | "Widescreen" | "PawnsEnabled" | "StartingItem0" | "StartingItem1" | "StartingItem2" \
                     | "StartingItem3" | "StartingItem4" | "StartingItem5" | "StartingItem6" | "StartingItem7" \
                     | "StartingItem8" | "StartingItem9" | "StartingItemA" | "StartingItemB" | "StartingItemC" \
                     | "StartingItemD" | "StartingItemE" | "StartingItemF" | "PlandomizerActive":
                    option_value = 0
                # Hammer and boots get received by the server, so we set the rom to jumpless/hammerless to start
                case "StartingBoots" | "StartingHammer":
                    option_value = -1
                # One setting on the front end, but two separate flags for the mod
                case "DoubleDamage":
                    option_value = options.enemy_damage.value == EnemyDamage.option_Double_Pain
                case "QuadrupleDamage":
                    option_value = options.enemy_damage.value == EnemyDamage.option_Quadruple_Pain
                case "ProgressiveScaling":
                    option_value = options.enemy_difficulty.value == EnemyDifficulty.option_Progressive_Scaling
                case "EnabledCheckBits":
                    option_value = map_tracker_check_bits
                case "EnabledShopBits":
                    option_value = map_tracker_shop_bits
                case "ColorMode":
                    option_value = color_mode
                case "Box5ColorA":
                    option_value = menu_color_a
                case "Box5ColorB":
                    option_value = menu_color_b
                case "ItemChoiceA":
                    option_value = mystery_opts.mystery_itemA
                case "ItemChoiceB":
                    option_value = mystery_opts.mystery_itemB
                case "ItemChoiceC":
                    option_value = mystery_opts.mystery_itemC
                case "ItemChoiceD":
                    option_value = mystery_opts.mystery_itemD
                case "ItemChoiceE":
                    option_value = mystery_opts.mystery_itemE
                case "ItemChoiceF":
                    option_value = mystery_opts.mystery_itemF
                case "ItemChoiceG":
                    option_value = mystery_opts.mystery_itemG
                # Calculated based on starting stats
                case "StartingLevel":
                    option_value = int(options.starting_hp.value / 5 +
                                       options.starting_fp.value / 5 +
                                       options.starting_bp.value / 3) - 3
                case "StartingMap":
                    option_value = starting_maps[options.starting_map.value][0]
                case "StarWaySpiritsNeededEnc":
                    option_value = encoded_spirits
                case "AllowPhysicsGlitches":
                    option_value = not options.prevent_ooblzs.value
                case "StarBeamArea":
                    option_value = star_beam_area

        else:
            option_value = getattr(options, ap_option).value

        dbtuples.append((option_key, option_value))
        # print(f"{rom_option}, {option_value}")
    return dbtuples


def get_db_key(rom_option):
    data = rom_option_table[rom_option]
    return (0xAF << 24) | (data[1] << 16) | (data[2] << 8) | data[3]


def get_trapped_item_id(item_id) -> int:
    return item_id | 0x2000
