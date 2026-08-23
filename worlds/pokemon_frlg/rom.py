"""
Classes and functions related to creating a ROM patch
"""
import bsdiff4
import struct
from typing import TYPE_CHECKING, Dict, List, Tuple

from worlds.Files import APPatchExtension, APProcedurePatch, APTokenMixin, APTokenTypes
from settings import get_settings
from .data import data, GAME_OPTIONS, EvolutionMethodEnum, TrainerPokemonDataTypeEnum
from .groups import location_groups
from .items import is_single_purchase_item
from .locations import PokemonFRLGLocation
from .options import (CardKey, Dexsanity, FlashRequired, ForceFullyEvolved, IslandPasses, ItemfinderRequired,
                      HmCompatibility, KantoTrainersanity, LevelScaling, RandomizeDamageCategories,
                      RandomizeLegendaryPokemon, RandomizeMiscPokemon, RandomizeMoveTypes, RandomizeStarters,
                      RandomizeTrainerParties, RandomizeWildPokemon, SeviiTrainersanity, ShopPrices, ShuffleFlyUnlocks,
                      ShuffleHiddenItems, TmTutorCompatibility, ViridianCityRoadblock)
from .pokemon import randomize_tutor_moves
from .util import bool_array_to_int, bound, encode_string

if TYPE_CHECKING:
    from .world import PokemonFRLGWorld

FIRERED_REV0_HASH = "e26ee0d44e809351c8ce2d73c7400cdd"
FIRERED_REV1_HASH = "51901a6e40661b3914aa333c802e24e8"
LEAFGREEN_REV0_HASH = "612ca9473451fa42b51d1711031ed5f6"
LEAFGREEN_REV1_HASH = "9d33a02159e018d09073e700e1fd10fd"

_LOOPING_MUSIC = [
    "MUS_RS_VS_GYM_LEADER", "MUS_RS_VS_TRAINER", "MUS_SCHOOL", "MUS_FOLLOW_ME", "MUS_GAME_CORNER", "MUS_ROCKET_HIDEOUT",
    "MUS_GYM", "MUS_CINNABAR", "MUS_LAVENDER", "MUS_CYCLING", "MUS_ENCOUNTER_ROCKET", "MUS_ENCOUNTER_GIRL",
    "MUS_ENCOUNTER_BOY", "MUS_HALL_OF_FAME", "MUS_VIRIDIAN_FOREST", "MUS_MT_MOON", "MUS_POKE_MANSION", "MUS_ROUTE1",
    "MUS_ROUTE24", "MUS_ROUTE3", "MUS_ROUTE11", "MUS_VICTORY_ROAD", "MUS_VS_GYM_LEADER", "MUS_VS_TRAINER",
    "MUS_VS_WILD", "MUS_VS_CHAMPION", "MUS_PALLET", "MUS_OAK_LAB", "MUS_OAK", "MUS_POKE_CENTER", "MUS_SS_ANNE",
    "MUS_SURF", "MUS_POKE_TOWER", "MUS_SILPH", "MUS_FUCHSIA", "MUS_CELADON", "MUS_VICTORY_TRAINER", "MUS_VICTORY_WILD",
    "MUS_VICTORY_GYM_LEADER", "MUS_VERMILLION", "MUS_PEWTER", "MUS_ENCOUNTER_RIVAL", "MUS_RIVAL_EXIT", "MUS_CAUGHT",
    "MUS_POKE_JUMP", "MUS_UNION_ROOM", "MUS_NET_CENTER", "MUS_MYSTERY_GIFT", "MUS_BERRY_PICK", "MUS_SEVII_CAVE",
    "MUS_TEACHY_TV_SHOW", "MUS_SEVII_ROUTE", "MUS_SEVII_DUNGEON", "MUS_SEVII_123", "MUS_SEVII_45", "MUS_SEVII_67",
    "MUS_VS_DEOXYS", "MUS_VS_MEWTWO", "MUS_VS_LEGEND", "MUS_ENCOUNTER_GYM_LEADER", "MUS_ENCOUNTER_DEOXYS",
    "MUS_TRAINER_TOWER", "MUS_SLOW_PALLET", "MUS_TEACHY_TV_MENU"
]

_FANFARES: Dict[str, int] = {
    "MUS_LEVEL_UP": 80,
    "MUS_OBTAIN_ITEM": 160,
    "MUS_EVOLVED": 220,
    "MUS_OBTAIN_TMHM": 220,
    "MUS_HEAL": 160,
    "MUS_OBTAIN_BADGE": 340,
    "MUS_MOVE_DELETED": 180,
    "MUS_OBTAIN_BERRY": 120,
    "MUS_SLOTS_JACKPOT": 250,
    "MUS_SLOTS_WIN": 150,
    "MUS_TOO_BAD": 160,
    "MUS_POKE_FLUTE": 450,
    "MUS_OBTAIN_KEY_ITEM": 170,
    "MUS_DEX_RATING": 196
}


class PokemonFRLGPatchExtension(APPatchExtension):
    game = data.get_game()

    @staticmethod
    def apply_bsdiff4(caller: APProcedurePatch, rom: bytes, patch: str) -> bytes:
        rom_data = bytearray(rom)
        if rom_data[0xBC] == 1:
            return bsdiff4.patch(rom, caller.get_file("base_patch_rev1.bsdiff4"))
        return bsdiff4.patch(rom, caller.get_file(patch))

    @staticmethod
    def apply_tokens(caller: APProcedurePatch, rom: bytes, token_file: str) -> bytes:
        rom_data = bytearray(rom)
        if rom_data[0xBC] == 1:
            token_data = caller.get_file("token_data_rev1.bin")
        else:
            token_data = caller.get_file(token_file)
        token_count = int.from_bytes(token_data[0:4], "little")
        bpr = 4
        for _ in range(token_count):
            token_type = token_data[bpr:bpr + 1][0]
            offset = int.from_bytes(token_data[bpr + 1:bpr + 5], "little")
            size = int.from_bytes(token_data[bpr + 5:bpr + 9], "little")
            data = token_data[bpr + 9:bpr + 9 + size]
            if token_type in [APTokenTypes.AND_8, APTokenTypes.OR_8, APTokenTypes.XOR_8]:
                arg = data[0]
                if token_type == APTokenTypes.AND_8:
                    rom_data[offset] = rom_data[offset] & arg
                elif token_type == APTokenTypes.OR_8:
                    rom_data[offset] = rom_data[offset] | arg
                else:
                    rom_data[offset] = rom_data[offset] ^ arg
            elif token_type in [APTokenTypes.COPY, APTokenTypes.RLE]:
                length = int.from_bytes(data[:4], "little")
                value = int.from_bytes(data[4:], "little")
                if token_type == APTokenTypes.COPY:
                    rom_data[offset: offset + length] = rom_data[value: value + length]
                else:
                    rom_data[offset: offset + length] = bytes([value] * length)
            else:
                rom_data[offset:offset + len(data)] = data
            bpr += 9 + size
        return bytes(rom_data)


class PokemonFireRedProcedurePatch(APProcedurePatch, APTokenMixin):
    game = data.get_game()
    hash = [FIRERED_REV0_HASH, FIRERED_REV1_HASH]
    patch_file_ending = data.get_firered_extension()
    result_file_ending = ".gba"

    procedure = [
        ("apply_bsdiff4", ["base_patch_rev0.bsdiff4"]),
        ("apply_tokens", ["token_data_rev0.bin"])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        with open(get_settings().pokemon_frlg_settings.firered_rom_file, "rb") as infile:
            base_rom_bytes = bytes(infile.read())
        return base_rom_bytes


class PokemonLeafGreenProcedurePatch(APProcedurePatch, APTokenMixin):
    game = data.get_game()
    hash = [LEAFGREEN_REV0_HASH, LEAFGREEN_REV1_HASH]
    patch_file_ending = data.get_leafgreen_extension()
    result_file_ending = ".gba"

    procedure = [
        ("apply_bsdiff4", ["base_patch_rev0.bsdiff4"]),
        ("apply_tokens", ["token_data_rev0.bin"])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        with open(get_settings().pokemon_frlg_settings.leafgreen_rom_file, "rb") as infile:
            base_rom_bytes = bytes(infile.read())
        return base_rom_bytes


class PokemonFRLGPatchData:
    tokens: Dict[str, APTokenMixin]
    game_version: str
    revision_keys: List[str]

    def __init__(self) -> None:
        self.tokens = {}
        self.game_version = ""
        self.revision_keys = []
        self.token_data = []

    def set_game_version(self, game_version: str) -> None:
        self.game_version = game_version
        self.revision_keys.append(game_version)
        self.revision_keys.append(f"{game_version}_rev1")
        for key in self.revision_keys:
            self.tokens[key] = APTokenMixin()

    def write_token(self,
                    addresses: Dict[str, int | List[int]],
                    offset: int,
                    data: bytes | Tuple[int, int] | int) -> None:
        for key in self.revision_keys:
            address = addresses[key]
            if type(address) is int:
                self.tokens[key].write_token(APTokenTypes.WRITE, address + offset, data)
            elif type(address) is list:
                for addr in address:
                    self.tokens[key].write_token(APTokenTypes.WRITE, addr + offset, data)

    def get_rev_token_bytes(self, key: str) -> bytes:
        return self.tokens[key].get_token_binary()


def write_tokens(world: "PokemonFRLGWorld") -> None:
    patch = world.patch_data

    # Set item values
    location_info: List[Tuple[int, int, str]] = []
    for location in world.get_locations():
        assert isinstance(location, PokemonFRLGLocation)
        if location.address is None or location.item is None:
            continue

        item_address = location.item_address

        if not world.options.remote_items and location.item.player == world.player:
            item_id = location.item.code
        else:
            item_id = data.constants["ITEM_ARCHIPELAGO_PROGRESSION"]

        patch.write_token(item_address, 0, struct.pack("<H", item_id))

        if world.options.item_appearance_matches_contents:
            graphic_address = location.graphic_address
            if all(v != 0 for v in graphic_address.values()):
                if location.item.advancement:
                    graphic_id = data.constants["OBJ_EVENT_GFX_PROG_ITEM_BALL"]
                elif location.item.useful:
                    graphic_id = data.constants["OBJ_EVENT_GFX_USEFUL_ITEM_BALL"]
                elif location.item.trap:
                    graphic_id = world.random.choice([data.constants["OBJ_EVENT_GFX_PROG_ITEM_BALL"],
                                                      data.constants["OBJ_EVENT_GFX_USEFUL_ITEM_BALL"],
                                                      data.constants["OBJ_EVENT_GFX_ITEM_BALL"]])
                else:
                    graphic_id = data.constants["OBJ_EVENT_GFX_ITEM_BALL"]
                patch.write_token(graphic_address, 0, struct.pack("<B", graphic_id))

        # Creates a list of item information to store in tables later. Those tables are used to display the item and
        # player name in a text box. In the case of not enough space, the game will default to "found an ARCHIPELAGO
        # ITEM"
        location_info.append((location.address, location.item.player, location.item.name))

    if world.options.kanto_trainersanity:
        rival_rewards = ["RIVAL_OAKS_LAB", "RIVAL_ROUTE22_EARLY", "RIVAL_CERULEAN", "RIVAL_SS_ANNE",
                         "RIVAL_POKEMON_TOWER", "RIVAL_SILPH", "RIVAL_ROUTE22_LATE", "CHAMPION_FIRST"]
        if not world.options.kanto_only:
            rival_rewards.append("CHAMPION_REMATCH")
        for trainer in rival_rewards:
            try:
                location = world.get_location(data.locations[f"TRAINER_{trainer}_BULBASAUR_REWARD"].name)
                alternates = [f"TRAINER_{trainer}_CHARMANDER", f"TRAINER_{trainer}_SQUIRTLE"]
                location_info.extend(
                    (
                        data.constants["TRAINER_FLAGS_START"] + data.constants[alternate],
                        location.item.player,
                        location.item.name
                    ) for alternate in alternates)
            except KeyError:
                continue

    player_name_ids: Dict[str, int] = {world.player_name: 0}
    player_name_address = data.rom_addresses["gArchipelagoPlayerNames"]
    for j, b in enumerate(encode_string(world.player_name, 17)):
        patch.write_token(player_name_address,
                          j,
                          struct.pack("<B", b))
    item_name_offsets: Dict[str, int] = {}
    item_name_address = data.rom_addresses["gArchipelagoItemNames"]
    next_item_name_offset = 0
    name_table_address = data.rom_addresses["gArchipelagoNameTable"]
    for i, (flag, item_player, item_name) in enumerate(sorted(location_info, key=lambda t: t[0])):
        player_name = world.multiworld.get_player_name(item_player)

        if player_name not in player_name_ids:
            # Only space for 1000 player names
            if len(player_name_ids) >= 1000:
                continue

            player_name_ids[player_name] = len(player_name_ids)
            for j, b in enumerate(encode_string(player_name, 17)):
                patch.write_token(player_name_address,
                                  (player_name_ids[player_name] * 17) + j,
                                  struct.pack("<B", b))

        if item_name not in item_name_offsets:
            if len(item_name) > 35:
                item_name = item_name[:34] + "…"

            # Only 36 * 2000 bytes for item names
            if next_item_name_offset + len(item_name) + 1 > 36 * 2000:
                continue

            item_name_offsets[item_name] = next_item_name_offset
            next_item_name_offset += len(item_name) + 1
            patch.write_token(item_name_address, item_name_offsets[item_name], encode_string(item_name) + b"\xFF")

        # There should always be enough space for one entry per location
        patch.write_token(name_table_address, (i * 6) + 0, struct.pack("<H", flag))
        patch.write_token(name_table_address, (i * 6) + 2, struct.pack("<H", item_name_offsets[item_name]))
        patch.write_token(name_table_address, (i * 6) + 4, struct.pack("<H", player_name_ids[player_name]))

    # Set starting items
    start_inventory = world.options.start_inventory.value.copy()

    starting_items: List[Tuple[str, int]] = []
    for item, quantity in start_inventory.items():
        if "Unique" in data.items[world.item_name_to_id[item]].tags:
            quantity = 1
        if quantity > 999:
            quantity = 999
        starting_items.append((item, quantity))

    for i, starting_item in enumerate(starting_items, 1):
        item_address = data.rom_addresses["gArchipelagoStartingItems"]
        count_address = data.rom_addresses["gArchipelagoStartingItemsCount"]
        item = world.item_name_to_id[starting_item[0]]
        patch.write_token(item_address, (i * 2), struct.pack("<H", item))
        patch.write_token(count_address, (i * 2), struct.pack("<H", starting_item[1]))

    # Set shuffled entrances
    _set_shuffled_entrances(world)

    # Set randomized fly destinations
    _set_randomized_fly_destinations(world)

    # Set shop data
    _set_shop_data(world)

    # Set species data
    _set_species_info(world)

    # Set wild encounters
    _set_wild_encounters(world)

    # Set starters
    _set_starters(world)

    # Set legendaries
    _set_legendaries(world)

    # Set misc Pokémon
    _set_misc_pokemon(world)

    # Set trade Pokémon
    _set_trade_pokemon(world)

    # Set trainer parties
    _set_trainer_parties(world)

    # Set TM/HM compatibility
    _set_tmhm_compatibility(world)

    # Set TM Moves
    _set_tm_moves(world)

    # Randomize move tutors
    _randomize_move_tutors(world)

    # Set types damage catagories
    _set_types_damage_categories(world)

    # Set moves
    _set_moves(world)

    # Set AP Options
    address = data.rom_addresses["gArchipelagoOptions"]
    offsets = data.ap_offsets

    # Set game options
    game_options_1 = 0
    game_options_2 = 0
    for option_name, option in GAME_OPTIONS.items():
        if option_name in world.options.game_options.value.keys():
            value = option.options[world.options.game_options.value[option_name]]
        else:
            value = option.default
        if option.option_group == -1:
            patch.write_token(address, offsets["windowFrameType"], struct.pack("<B", value))
        elif option.option_group == -2:
            patch.write_token(address, offsets["expMultiplier"], struct.pack("<H", value))
        elif option.option_group == 1:
            game_options_1 |= (value << option.option_number)
        elif option.option_group == 2:
            game_options_2 |= (value << option.option_number)
    patch.write_token(address, offsets["gameOptions1"], struct.pack("<H", game_options_1))
    patch.write_token(address, offsets["gameOptions2"], struct.pack("<H", game_options_2))

    # Set better shops
    better_shops = 1 if world.options.better_shops else 0
    patch.write_token(address, offsets["betterShops"], struct.pack("<B", better_shops))

    # Set cheaper coins
    cheaper_coins = 1 if world.options.cheaper_coins else 0
    patch.write_token(address, offsets["cheaperCoins"], struct.pack("<B", cheaper_coins))

    # Set reusable TMs and Move Tutors
    reusable_tm_tutors = 1 if world.options.reusable_tm_tutors else 0
    patch.write_token(address, offsets["reusableTms"], struct.pack("<B", reusable_tm_tutors))

    # Set unlock seen dex info
    all_pokemon_seen = 1 if world.options.all_pokemon_seen else 0
    patch.write_token(address, offsets["unlockSeenDexInfo"], struct.pack("<B", all_pokemon_seen))

    # Set physical/special split
    physical_special_split = 1 if world.options.physical_special_split else 0
    patch.write_token(address, offsets["physicalSpecialSplit"], struct.pack("<B", physical_special_split))

    # Set Viridian City roadblock
    open_viridian = 1 if world.options.viridian_city_roadblock.value == ViridianCityRoadblock.option_open else 0
    patch.write_token(address, offsets["openViridianCity"], struct.pack("<B", open_viridian))

    # Set Pewter City roadblock
    route_3_condition = world.options.pewter_city_roadblock.value
    patch.write_token(address, offsets["route3Requirement"], struct.pack("<B", route_3_condition))

    # Set Cerulean City roadblocks
    open_cerulean = world.options.remove_cerulean_city_roadblocks.value
    patch.write_token(address, offsets["openCeruleanCity"], struct.pack("<B", open_cerulean))

    # Set Diglett's Cave access
    digletts_cave_access = world.options.digletts_cave_roadblock.value
    patch.write_token(address, offsets["diglettsCaveRoadblock"], struct.pack("<B", digletts_cave_access))

    # Set Route 9 access
    route_9_access = world.options.route_9_roadblock.value
    patch.write_token(address, offsets["route9Roadblock"], struct.pack("<B", route_9_access))

    # Set Underground Paths blocked
    block_paths = world.options.block_underground_paths.value
    patch.write_token(address, offsets["blockUndergroundPaths"], struct.pack("<B", block_paths))

    # Set Route 12 boulders
    route_12_boulders = world.options.route_12_boulders.value
    patch.write_token(address, offsets["route12Boulders"], struct.pack("<B", route_12_boulders))

    # Set Route 10 waterfall
    route_10_waterfall = world.options.route_10_waterfall.value
    patch.write_token(address, data.ap_offsets["route10Waterfall"], struct.pack("<B", route_10_waterfall))

    # Set Route 12 rocks
    route_12_rocks = world.options.route_12_rocks.value
    patch.write_token(address, offsets["route12Rocks"], struct.pack("<B", route_12_rocks))

    # Set Route 16 rock
    route_16_rock = world.options.route_16_rock.value
    patch.write_token(address, offsets["route16Rock"], struct.pack("<B", route_16_rock))

    # Set open Silph Co.
    open_silph = world.options.open_silph_co.value
    patch.write_token(address, offsets["openSilphCo"], struct.pack("<B", open_silph))

    # Set remove Saffron Rockets
    remove_saffron_rockets = world.options.remove_saffron_rockets.value
    patch.write_token(address, offsets["removeSaffronRockets"], struct.pack("<B", remove_saffron_rockets))

    # Set Route 23 waterfall
    route_23_waterfall = world.options.route_23_waterfall.value
    patch.write_token(address, offsets["route23Waterfall"], struct.pack("<B", route_23_waterfall))

    # Set Route 23 trees
    route_23_trees = world.options.route_23_trees.value
    patch.write_token(address, offsets["route23Trees"], struct.pack("<B", route_23_trees))

    # Set Pokémon Tower blocked
    block_tower = world.options.block_pokemon_tower.value
    patch.write_token(address, offsets["blockPokemonTower"], struct.pack("<B", block_tower))

    # Set Victory Road rocks
    victory_road_rocks = world.options.victory_road_rocks.value
    patch.write_token(address, offsets["victoryRoadRocks"], struct.pack("<B", victory_road_rocks))

    # Set early gossipers
    early_gossipers = world.options.early_gossipers.value
    patch.write_token(address, offsets["earlyFameGossip"], struct.pack("<B", early_gossipers))

    # Set block Vermilion sailing
    block_vermilion_sailing = world.options.block_vermilion_sailing.value
    patch.write_token(address, offsets["blockSailing"], struct.pack("<B", block_vermilion_sailing))

    # Set all elevators locked
    elevators_condition = world.options.elevators_condition
    patch.write_token(address, offsets["elevatorsState"], struct.pack("<B", elevators_condition))

    # Set Viridian Gym Rrquirement
    viridian_gym_requirement = world.options.viridian_gym_requirement.value
    patch.write_token(address, offsets["giovanniRequiresGyms"], struct.pack("<B", viridian_gym_requirement))

    # Set Viridian Gym count
    viridian_gym_count = world.options.viridian_gym_count.value
    patch.write_token(address, offsets["giovanniRequiredCount"], struct.pack("<B", viridian_gym_count))

    # Set Route 22 requirement
    route_22_requirement = world.options.route22_gate_requirement.value
    patch.write_token(address, offsets["route22GateRequiresGyms"], struct.pack("<B", route_22_requirement))

    # Set Route 22 count
    route_22_count = world.options.route22_gate_count.value
    patch.write_token(address, offsets["route22GateRequiredCount"], struct.pack("<B", route_22_count))

    # Set Route 23 requirement
    route_23_requirement = world.options.route23_guard_requirement.value
    patch.write_token(address, offsets["route23GuardRequiresGyms"], struct.pack("<B", route_23_requirement))

    # Set Route 23 count
    route_23_count = world.options.route23_guard_count.value
    patch.write_token(address, offsets["route23GuardRequiredCount"], struct.pack("<B", route_23_count))

    # Set Elite Four requirement
    elite_four_requirement = world.options.elite_four_requirement.value
    patch.write_token(address, offsets["eliteFourRequiresGyms"], struct.pack("<B", elite_four_requirement))

    # Set Elite Four count
    elite_four_count = world.options.elite_four_count.value
    patch.write_token(address, offsets["eliteFourRequiredCount"], struct.pack("<B", elite_four_count))

    # Set Elite Four Rematch requirement
    elite_four_rematch_requirement = world.options.elite_four_rematch_requirement.value
    patch.write_token(address, offsets["eliteFourRematchRequiresGyms"], struct.pack("<B", elite_four_rematch_requirement))

    # Set Elite Four Rematch count
    elite_four_rematch_count = world.options.elite_four_rematch_count.value
    patch.write_token(address, offsets["eliteFourRematchRequiredCount"], struct.pack("<B", elite_four_rematch_count))

    # Set Cerulean Cave requirement
    cerulean_cave_requirement = world.options.cerulean_cave_requirement.value
    patch.write_token(address, offsets["ceruleanCaveRequirement"], struct.pack("<B", cerulean_cave_requirement))

    # Set Cerulean Cave count
    cerulean_cave_count = world.options.cerulean_cave_count.value
    patch.write_token(address, offsets["ceruleanCaveRequiredCount"], struct.pack("<B", cerulean_cave_count))

    # Set Fossil count
    fossil_count = world.options.fossil_count.value
    patch.write_token(address, offsets["cinnabarFossilCount"], struct.pack("<B", fossil_count))

    # Set rematch requirements
    rematch_requirements = world.options.rematch_requirements.value
    patch.write_token(address, offsets["rematchRequiresGyms"], struct.pack("<B", rematch_requirements))

    # Set starting money
    patch.write_token(address, offsets["startingMoney"], struct.pack("<I", world.options.starting_money.value))

    # Set itemfinder required
    itemfinder_required = 1 if world.options.itemfinder_required.value == ItemfinderRequired.option_required else 0
    patch.write_token(address, offsets["itemfinderRequired"], struct.pack("<B", itemfinder_required))

    # Set flash required
    flash_required = 1 if world.options.flash_required.value == FlashRequired.option_required else 0
    patch.write_token(address, offsets["flashRequired"], struct.pack("<B", flash_required))

    # Set fame checker required
    fame_checker_required = 1 if world.options.fame_checker_required else 0
    patch.write_token(address, offsets["fameCheckerRequired"], struct.pack("<B", fame_checker_required))

    # Set bicycle requires jumping shoes
    bicycle_requires_jumping_shoes = 1 if world.options.bicycle_requires_jumping_shoes else 0
    patch.write_token(address, offsets["bikeRequiresJumpingShoes"], struct.pack("<B", bicycle_requires_jumping_shoes))

    # Set acrobatic bicycle
    acrobatic_bicycle = 1 if world.options.acrobatic_bicycle else 0
    patch.write_token(address, offsets["acrobaticBike"], struct.pack("<B", acrobatic_bicycle))

    # Set Oak's Aides counts
    oaks_aide_route_2 = world.options.oaks_aide_route_2.value
    patch.write_token(address, offsets["oaksAideRequiredCounts"], struct.pack("<B", oaks_aide_route_2))
    oaks_aide_route_10 = world.options.oaks_aide_route_10.value
    patch.write_token(address, offsets["oaksAideRequiredCounts"] + 1, struct.pack("<B", oaks_aide_route_10))
    oaks_aide_route_11 = world.options.oaks_aide_route_11.value
    patch.write_token(address, offsets["oaksAideRequiredCounts"] + 2, struct.pack("<B", oaks_aide_route_11))
    oaks_aide_route_16 = world.options.oaks_aide_route_16.value
    patch.write_token(address, offsets["oaksAideRequiredCounts"] + 3, struct.pack("<B", oaks_aide_route_16))
    oaks_aide_route_15 = world.options.oaks_aide_route_15.value
    patch.write_token(address, offsets["oaksAideRequiredCounts"] + 4, struct.pack("<B", oaks_aide_route_15))

    # Set recurring hidden items shuffled
    recurring_hidden_items = 1 if world.options.shuffle_hidden.value == ShuffleHiddenItems.option_all else 0
    patch.write_token(address, offsets["reccuringHiddenItems"], struct.pack("<B", recurring_hidden_items))

    # Set trainersanity
    trainersanity = 1 if (world.options.kanto_trainersanity.value
                          != KantoTrainersanity.special_range_names["none"]
                          or world.options.sevii_trainersanity.value
                          != SeviiTrainersanity.special_range_names["none"]) else 0
    patch.write_token(address, offsets["isTrainersanity"], struct.pack("<B", trainersanity))

    # Set dexsanity
    dexsanity = 1 if world.options.dexsanity.value != Dexsanity.special_range_names["none"] else 0
    patch.write_token(address, offsets["isDexsanity"], struct.pack("<B", dexsanity))

    # Set extra key items
    extra_key_items = 1 if world.options.extra_key_items else 0
    patch.write_token(address, offsets["extraKeyItems"], struct.pack("<B", extra_key_items))

    # Set kanto only
    kanto_only = 1 if world.options.kanto_only else 0
    patch.write_token(address, offsets["kantoOnly"], struct.pack("<B", kanto_only))

    # Set fly unlocks
    fly_unlocks = 1 if (world.options.shuffle_fly_unlocks.value != ShuffleFlyUnlocks.option_off or
                        world.options.randomize_fly_destinations) else 0
    patch.write_token(address, offsets["flyUnlocks"], struct.pack("<B", fly_unlocks))

    # Set famesanity
    famesanity = 1 if world.options.famesanity else 0
    patch.write_token(address, offsets["isFamesanity"], struct.pack("<B", famesanity))

    # Set gym keys
    gym_keys = 1 if world.options.gym_keys else 0
    patch.write_token(address, offsets["gymKeys"], struct.pack("<B", gym_keys))

    # Set shopsanity
    shopsanity = 1 if world.options.shopsanity else 0
    patch.write_token(address, offsets["isShopsanity"], struct.pack("<B", shopsanity))

    # Set remove badge requirements
    hms = ["Flash", "Cut", "Fly", "Strength", "Surf", "Rock Smash", "Waterfall"]
    remove_badge_requirements = 0
    for i, hm in enumerate(hms):
        if hm in world.options.remove_badge_requirement.value:
            remove_badge_requirements |= (1 << i)
    patch.write_token(address, offsets["removeBadgeRequirement"], struct.pack("<B", remove_badge_requirements))

    # Set additional dark caves
    dark_caves = ["Mt. Moon", "Diglett's Cave", "Victory Road"]
    map_ids = [["MAP_MT_MOON_1F", "MAP_MT_MOON_B1F", "MAP_MT_MOON_B2F"],
               ["MAP_DIGLETTS_CAVE_B1F"],
               ["MAP_VICTORY_ROAD_1F", "MAP_VICTORY_ROAD_2F", "MAP_VICTORY_ROAD_3F"]]
    additional_dark_caves = 0
    for i, dark_cave in enumerate(dark_caves):
        if dark_cave in world.options.additional_dark_caves.value:
            additional_dark_caves |= (1 << i)
            for map_id in map_ids[i]:
                map_data = world.modified_maps[map_id]
                header_address = map_data.header_address
                patch.write_token(header_address, 21, struct.pack("<B", 1))
    patch.write_token(address, offsets["additionalDarkCaves"], struct.pack("<B", additional_dark_caves))

    # Set passes split
    passes_split = 1 if world.options.island_passes.value in {IslandPasses.option_split,
                                                              IslandPasses.option_progressive_split} else 0
    patch.write_token(address, offsets["passesSplit"], struct.pack("<B", passes_split))

    # Set card keys split
    card_keys_split = 1 if world.options.card_key.value in {CardKey.option_split, CardKey.option_progressive} else 0
    patch.write_token(address, offsets["cardKeysSplit"], struct.pack("<B", card_keys_split))

    # Set teas split
    teas_split = 1 if world.options.split_teas else 0
    patch.write_token(address, offsets["teasSplit"], struct.pack("<B", teas_split))

    # Set starting town
    starting_town = data.constants[world.starting_town]
    patch.write_token(address, offsets["startingLocation"], struct.pack("<B", starting_town))

    # Set starting respawn
    starting_respawn = data.constants[world.starting_respawn]
    patch.write_token(address, offsets["startingRespawn"], struct.pack("<B", starting_respawn))

    # Set free fly location
    patch.write_token(address, offsets["freeFlyId"], struct.pack("<B", world.free_fly_location_id))

    # Set town map fly location
    patch.write_token(address, offsets["townFreeFlyId"], struct.pack("<B", world.town_map_fly_location_id))

    # Set resort gorgeous mon
    patch.write_token(address, offsets["resortGorgeousMon"], struct.pack("<H", world.logic.resort_gorgeous_pokemon))

    # Set intro species
    species_id = world.random.choice(list(data.species.keys()))
    patch.write_token(address, offsets["introSpecies"], struct.pack("<H", species_id))

    # Set PC item ID
    pc_item_location = world.get_location("Player's PC - Item")
    if not world.options.remote_items and pc_item_location.item.player == world.player:
        item_id = pc_item_location.item.code
    else:
        item_id = data.constants["ITEM_ARCHIPELAGO_PROGRESSION"]
    patch.write_token(address, offsets["pcItemId"], struct.pack("<H", item_id))

    # Set remote items
    remote_items = 1 if world.options.remote_items else 0
    patch.write_token(address, offsets["remoteItems"], struct.pack("<B", remote_items))

    # Set interior ER
    shuffle_interiors = 1 if world.options.shuffle_interiors else 0
    patch.write_token(address, offsets["internalEntrancesRandomized"], struct.pack("<B", shuffle_interiors))

    # Set Pokémon Center ER
    shuffle_pokemon_centers = 1 if world.options.shuffle_pokemon_centers else 0
    patch.write_token(address, offsets["pokemonCenterEntrancesRandomized"], struct.pack("<B", shuffle_pokemon_centers))

    # Set skip intro
    skip_intro = 1 if world.options.skip_intro else 0
    patch.write_token(address, offsets["skipIntro"], struct.pack("<B", skip_intro))

    # Set that the game has been randomized
    patch.write_token(address, offsets["randomized"], struct.pack("<B", 1))

    # Set apworld version
    apworld_version = f"AP v{data.get_version_string()}"
    for j, b in enumerate(encode_string(apworld_version, 16)):
        patch.write_token(address, offsets["version"] + j, struct.pack("<B", b))

    # Set total darkness
    if world.options.total_darkness:
        flash_level_address = data.rom_addresses["sFlashLevelToRadius"]
        patch.write_token(flash_level_address, 8, struct.pack("<H", 0))

    # Set skip elite four
    if world.options.skip_elite_four:
        indigo_address = data.maps["MAP_INDIGO_PLATEAU_POKEMON_CENTER_1F"].warp_table_address
        champion_address = data.maps["MAP_POKEMON_LEAGUE_CHAMPIONS_ROOM"].warp_table_address
        patch.write_token(indigo_address,
                          14,
                          struct.pack("<H", data.constants["MAP_POKEMON_LEAGUE_CHAMPIONS_ROOM"]))
        patch.write_token(champion_address,
                          6,
                          struct.pack("<H", data.constants["MAP_INDIGO_PLATEAU_POKEMON_CENTER_1F"]))

    # Randomize music
    if world.options.randomize_music:
        # The "randomized sound table" is a patchboard that redirects sounds just before they get played
        randomized_looping_music = _LOOPING_MUSIC.copy()
        world.random.shuffle(randomized_looping_music)
        sound_table_address = data.rom_addresses["gRandomizedSoundTable"]
        for original_music, randomized_music in zip(_LOOPING_MUSIC, randomized_looping_music):
            patch.write_token(sound_table_address,
                              data.constants[original_music] * 2,
                              struct.pack("<H", data.constants[randomized_music]))

    # Randomize fanfares
    if world.options.randomize_fanfares:
        # Shuffle the lists, pair new tracks with original tracks, set the new track ids, and set new fanfare durations
        randomized_fanfares = [fanfare_name for fanfare_name in _FANFARES]
        world.random.shuffle(randomized_fanfares)
        sound_table_address = data.rom_addresses["gRandomizedSoundTable"]
        fanfares_address = data.rom_addresses["sFanfares"]
        for i, fanfare_data in enumerate(zip(_FANFARES.keys(), randomized_fanfares)):
            patch.write_token(sound_table_address,
                              data.constants[fanfare_data[0]] * 2,
                              struct.pack("<H", data.constants[fanfare_data[1]]))
            patch.write_token(fanfares_address,
                              (i * 4) + 2,
                              struct.pack("<H", data.constants[fanfare_data[1]]))

    # Set slot auth
    patch.write_token(data.rom_addresses["gArchipelagoInfo"], 0, world.auth)

    # Set apworld version in ROM header
    apworld_version_address = {}
    for key in patch.revision_keys:
        apworld_version_address[key] = 0x178
    patch.write_token(apworld_version_address, 0, data.get_version_string().encode("ascii"))


def _set_shuffled_entrances(world: "PokemonFRLGWorld") -> None:
    if world.er_pairings is None:
        return

    patch = world.patch_data
    for source_name, dest_name in world.er_pairings:
        source_id = data.warp_name_map[source_name]
        dest_id = data.warp_name_map[dest_name]
        source_warp_data = data.warps[source_id]
        dest_warp_data = data.warps[dest_id]
        source_warp_table_address = data.maps[source_warp_data.source_map].warp_table_address
        dest_map_id = data.constants[dest_warp_data.source_map]
        if len(source_warp_data.source_ids) <= len(dest_warp_data.source_ids):
            for i, source_warp_id in enumerate(source_warp_data.source_ids):
                dest_warp_id = dest_warp_data.source_ids[i]
                patch.write_token(source_warp_table_address,
                                  (source_warp_id * 8) + 5,
                                  struct.pack("<B", dest_warp_id))
                patch.write_token(source_warp_table_address,
                                  (source_warp_id * 8) + 6,
                                  struct.pack("<H", dest_map_id))
        elif len(dest_warp_data.source_ids) == 1:
            dest_warp_id = dest_warp_data.source_ids[0]
            for source_warp_id in source_warp_data.source_ids:
                patch.write_token(source_warp_table_address,
                                  (source_warp_id * 8) + 5,
                                  struct.pack("<B", dest_warp_id))
                patch.write_token(source_warp_table_address,
                                  (source_warp_id * 8) + 6,
                                  struct.pack("<H", dest_map_id))
        elif len(source_warp_data.source_ids) > len(dest_warp_data.source_ids):
            for i, source_warp_id in enumerate(source_warp_data.source_ids):
                if i <= 1:
                    dest_warp_id = dest_warp_data.source_ids[0]
                else:
                    dest_warp_id = dest_warp_data.source_ids[1]
                patch.write_token(source_warp_table_address,
                                  (source_warp_id * 8) + 5,
                                  struct.pack("<B", dest_warp_id))
                patch.write_token(source_warp_table_address,
                                  (source_warp_id * 8) + 6,
                                  struct.pack("<H", dest_map_id))


def _set_randomized_fly_destinations(world: "PokemonFRLGWorld") -> None:
    if not world.options.randomize_fly_destinations:
        return

    patch = world.patch_data
    fly_id_map = {
        "SPAWN_PALLET_TOWN": "MAPSEC_PALLET_TOWN",
        "SPAWN_VIRIDIAN_CITY": "MAPSEC_VIRIDIAN_CITY",
        "SPAWN_PEWTER_CITY": "MAPSEC_PEWTER_CITY",
        "SPAWN_CERULEAN_CITY": "MAPSEC_CERULEAN_CITY",
        "SPAWN_LAVENDER_TOWN": "MAPSEC_LAVENDER_TOWN",
        "SPAWN_VERMILION_CITY": "MAPSEC_VERMILION_CITY",
        "SPAWN_CELADON_CITY": "MAPSEC_CELADON_CITY",
        "SPAWN_FUCHSIA_CITY": "MAPSEC_FUCHSIA_CITY",
        "SPAWN_CINNABAR_ISLAND": "MAPSEC_CINNABAR_ISLAND",
        "SPAWN_INDIGO_PLATEAU": "MAPSEC_INDIGO_PLATEAU",
        "SPAWN_SAFFRON_CITY": "MAPSEC_SAFFRON_CITY",
        "SPAWN_ROUTE4": "MAPSEC_ROUTE_4_POKECENTER",
        "SPAWN_ROUTE10": "MAPSEC_ROUTE_10_POKECENTER",
        "SPAWN_ONE_ISLAND": "MAPSEC_ONE_ISLAND",
        "SPAWN_TWO_ISLAND": "MAPSEC_TWO_ISLAND",
        "SPAWN_THREE_ISLAND": "MAPSEC_THREE_ISLAND",
        "SPAWN_FOUR_ISLAND": "MAPSEC_FOUR_ISLAND",
        "SPAWN_FIVE_ISLAND": "MAPSEC_FIVE_ISLAND",
        "SPAWN_SEVEN_ISLAND": "MAPSEC_SEVEN_ISLAND",
        "SPAWN_SIX_ISLAND": "MAPSEC_SIX_ISLAND"
    }

    fly_layer_offset = 0x294
    fly_point_table_address = data.rom_addresses["sFlyPoints"]
    fly_map_kanto_address = data.rom_addresses["sRegionMapSections_Kanto"]
    fly_map_sevii_123_address = data.rom_addresses["sRegionMapSections_Sevii123"]
    fly_map_sevii_45_address = data.rom_addresses["sRegionMapSections_Sevii45"]
    fly_map_sevii_67_address = data.rom_addresses["sRegionMapSections_Sevii67"]
    fly_map_address = [fly_map_kanto_address, fly_map_sevii_123_address,
                       fly_map_sevii_45_address, fly_map_sevii_67_address]
    fly_name_array_address = data.rom_addresses["gFlyUnlockNames"]
    for i in range(fly_layer_offset, fly_layer_offset + 0x14A):
        value = data.constants["MAPSEC_NONE"]
        patch.write_token(fly_map_kanto_address, i, struct.pack("<B", value))
        patch.write_token(fly_map_sevii_123_address, i, struct.pack("<B", value))
        patch.write_token(fly_map_sevii_45_address, i, struct.pack("<B", value))
        patch.write_token(fly_map_sevii_67_address, i, struct.pack("<B", value))
    for fly_id, fly_data in world.fly_destination_data.items():
        fly_id_offset = (data.constants[fly_id] - 1) * 8
        fly_map_offset = fly_layer_offset + fly_data.region_map_index
        fly_name_offset = (data.constants[fly_id] - 1) * 17
        fly_map_value = data.constants[fly_id_map[fly_id]]
        patch.write_token(fly_point_table_address, fly_id_offset, struct.pack("<B", fly_data.map_group))
        patch.write_token(fly_point_table_address, fly_id_offset + 1, struct.pack("<B", fly_data.map_num))
        patch.write_token(fly_point_table_address, fly_id_offset + 2, struct.pack("<H", fly_data.x_pos))
        patch.write_token(fly_point_table_address, fly_id_offset + 4, struct.pack("<H", fly_data.y_pos))
        patch.write_token(fly_map_address[fly_data.region_map_id - 1],
                          fly_map_offset,
                          struct.pack("<B", fly_map_value))
        for j, b in enumerate(encode_string(fly_data.display_name, 17)):
            patch.write_token(fly_name_array_address, fly_name_offset + j, struct.pack("<B", b))


def _set_shop_data(world: "PokemonFRLGWorld") -> None:
    patch = world.patch_data
    shop_locations = [loc for loc in world.get_locations()
                      if loc.name in location_groups["Shops"]
                      or loc.name in location_groups["Vending Machines"]
                      or loc.name in location_groups["Prizes"]]
    already_set_prices: Dict[str, int] = {}

    for location in shop_locations:
        if location.item is None:
            continue

        already_set = False
        item_address = location.item_address

        if location.item.player != world.player:
            price = 2000
            if location.item.useful:
                price = round(price * 0.5)
            elif location.item.filler:
                price = round(price * 0.1)
            patch.write_token(item_address, 2, struct.pack("<H", data.constants["ITEM_ARCHIPELAGO_PROGRESSION"]))
        else:
            if location.item.name in already_set_prices and world.options.consistent_shop_prices:
                price = already_set_prices[location.item.name]
                already_set = True
            else:
                price = data.items[world.item_name_to_id[location.item.name]].price
            if location.item.code is not None:
                patch.write_token(item_address, 2, struct.pack("<H", location.item.code))

        if location.name in location_groups["Prizes"]:
            price = round(price * 0.5)
        if not already_set:
            if world.options.shop_prices == ShopPrices.option_cheap:
                price = round(price * 0.5)
            elif world.options.shop_prices == ShopPrices.option_affordable:
                price = world.random.randint(round(price * 0.5), price)
            elif world.options.shop_prices == ShopPrices.option_standard:
                price = world.random.randint(round(price * 0.5), round(price * 1.5))
            elif world.options.shop_prices == ShopPrices.option_expensive:
                price = world.random.randint(price, round(price * 1.5))

        patch.write_token(item_address, 4, struct.pack("<H", price))

        if location.item.player == world.player and location.item.name not in already_set_prices:
            if location.name in location_groups["Prizes"]:
                already_set_prices[location.item.name] = round(price * 2)
            else:
                already_set_prices[location.item.name] = price

        if ((location.item.player and is_single_purchase_item(location.item) or location.item.player != world.player)
                and location.address is not None):
            patch.write_token(item_address, 6, struct.pack("<B", 0))
        else:
            patch.write_token(item_address, 6, struct.pack("<B", 1))


def _set_species_info(world: "PokemonFRLGWorld") -> None:
    patch = world.patch_data
    for species in world.modified_species.values():
        address = species.address
        patch.write_token(address, 0x00, struct.pack("<B", species.base_stats[0]))
        patch.write_token(address, 0x01, struct.pack("<B", species.base_stats[1]))
        patch.write_token(address, 0x02, struct.pack("<B", species.base_stats[2]))
        patch.write_token(address, 0x03, struct.pack("<B", species.base_stats[3]))
        patch.write_token(address, 0x04, struct.pack("<B", species.base_stats[4]))
        patch.write_token(address, 0x05, struct.pack("<B", species.base_stats[5]))
        patch.write_token(address, 0x06, struct.pack("<B", species.types[0]))
        patch.write_token(address, 0x07, struct.pack("<B", species.types[1]))
        patch.write_token(address, 0x08, struct.pack("<B", species.catch_rate))
        patch.write_token(address, 0x16, struct.pack("<B", species.abilities[0]))
        patch.write_token(address, 0x17, struct.pack("<B", species.abilities[1]))

        for i, learnset_move in enumerate(species.learnset):
            learnset_address = species.learnset_address
            level_move = learnset_move.level << 9 | learnset_move.move_id
            patch.write_token(learnset_address, i * 2, struct.pack("<H", level_move))


def _set_wild_encounters(world: "PokemonFRLGWorld") -> None:
    if (world.options.level_scaling == LevelScaling.option_off and
            world.options.wild_pokemon == RandomizeWildPokemon.option_vanilla):
        return

    patch = world.patch_data
    for map_data in world.modified_maps.values():
        for table in map_data.encounters.values():
            if table is not None:
                for i, species_data in enumerate(table.slots[patch.game_version]):
                    address = table.address
                    patch.write_token(address, (i * 4) + 0x00, struct.pack("<B", species_data.min_level))
                    patch.write_token(address, (i * 4) + 0x01, struct.pack("<B", species_data.max_level))
                    patch.write_token(address, (i * 4) + 0x02, struct.pack("<H", species_data.species_id))


def _set_starters(world: "PokemonFRLGWorld") -> None:
    if world.options.starters == RandomizeStarters.option_vanilla:
        return

    patch = world.patch_data
    for name, starter in world.modified_starters.items():
        patch.write_token(starter.address, 0, struct.pack("<H", starter.species_id))


def _set_legendaries(world: "PokemonFRLGWorld") -> None:
    if (world.options.level_scaling == LevelScaling.option_off and
            world.options.legendary_pokemon == RandomizeLegendaryPokemon.option_vanilla):
        return

    patch = world.patch_data
    for name, legendary in world.modified_legendary_pokemon.items():
        patch.write_token(legendary.address, 0, struct.pack("<H", legendary.species_id[patch.game_version]))
        patch.write_token(legendary.level_address, 0, struct.pack("<B", legendary.level[patch.game_version]))


def _set_misc_pokemon(world: "PokemonFRLGWorld") -> None:
    if (world.options.level_scaling == LevelScaling.option_off and
            world.options.misc_pokemon == RandomizeMiscPokemon.option_vanilla):
        return

    patch = world.patch_data
    for name, misc_pokemon in world.modified_misc_pokemon.items():
        patch.write_token(misc_pokemon.address,
                          0,
                          struct.pack("<H", misc_pokemon.species_id[patch.game_version]))
        if misc_pokemon.level[patch.game_version] != 0:
            patch.write_token(misc_pokemon.level_address,
                              0,
                              struct.pack("<B", misc_pokemon.level[patch.game_version]))


def _set_trade_pokemon(world: "PokemonFRLGWorld") -> None:
    patch = world.patch_data
    for name, trade_pokemon in world.modified_trade_pokemon.items():
        patch.write_token(trade_pokemon.species_address,
                          0,
                          struct.pack("<H", trade_pokemon.species_id[patch.game_version]))
        patch.write_token(trade_pokemon.requested_species_address,
                          0,
                          struct.pack("<H", trade_pokemon.requested_species_id[patch.game_version]))


def _set_trainer_parties(world: "PokemonFRLGWorld") -> None:
    if (world.options.level_scaling == LevelScaling.option_off and
            world.options.trainers == RandomizeTrainerParties.option_vanilla and
            world.options.starters == RandomizeStarters.option_vanilla and
            world.options.modify_trainer_levels.value == 100):
        return

    patch = world.patch_data
    for trainer in world.modified_trainers.values():
        party_address = trainer.party.address

        if trainer.party.pokemon_data_type in {TrainerPokemonDataTypeEnum.NO_ITEM_DEFAULT_MOVES,
                                               TrainerPokemonDataTypeEnum.ITEM_DEFAULT_MOVES}:
            pokemon_data_size = 8
        else:
            pokemon_data_size = 16

        for i, pokemon in enumerate(trainer.party.pokemon):
            pokemon_offset = (i * pokemon_data_size)
            level = round(pokemon.level * (world.options.modify_trainer_levels.value / 100))
            level = bound(level, 1, 100)
            species_id = pokemon.species_id

            if world.options.force_fully_evolved != ForceFullyEvolved.special_range_names["never"]:
                evolve = True
                if world.options.force_fully_evolved == ForceFullyEvolved.special_range_names["species"]:
                    while evolve:
                        evolve = False
                        species_data = world.modified_species[species_id]
                        evolutions = species_data.evolutions.copy()
                        world.random.shuffle(evolutions)
                        for evolution in evolutions:
                            if evolution.method in range(EvolutionMethodEnum.LEVEL, EvolutionMethodEnum.ITEM):
                                if level >= evolution.param:
                                    species_id = evolution.species_id
                                    evolve = True
                                    break
                            else:
                                evolution_data = world.modified_species[evolution.species_id]
                                evolution_level = sum(evolution_data.base_stats) / 15
                                if level > evolution_level:
                                    species_id = evolution.species_id
                                    evolve = True
                                    break
                elif level >= world.options.force_fully_evolved.value:
                    while evolve:
                        species_data = world.modified_species[species_id]
                        if len(species_data.evolutions) > 0:
                            evolution = world.random.choice(species_data.evolutions)
                            species_id = evolution.species_id
                        else:
                            evolve = False

            patch.write_token(party_address, pokemon_offset + 0x02, struct.pack("<B", level))
            patch.write_token(party_address, pokemon_offset + 0x04, struct.pack("<H", species_id))
            if trainer.party.pokemon_data_type in {TrainerPokemonDataTypeEnum.NO_ITEM_CUSTOM_MOVES,
                                                   TrainerPokemonDataTypeEnum.ITEM_CUSTOM_MOVES}:
                offset = 2 if trainer.party.pokemon_data_type == TrainerPokemonDataTypeEnum.ITEM_CUSTOM_MOVES else 0
                patch.write_token(party_address,
                                  pokemon_offset + offset + 0x06,
                                  struct.pack("<H", pokemon.moves[0]))
                patch.write_token(party_address,
                                  pokemon_offset + offset + 0x08,
                                  struct.pack("<H", pokemon.moves[1]))
                patch.write_token(party_address,
                                  pokemon_offset + offset + 0x0A,
                                  struct.pack("<H", pokemon.moves[2]))
                patch.write_token(party_address,
                                  pokemon_offset + offset + 0x0C,
                                  struct.pack("<H", pokemon.moves[3]))


def _set_tmhm_compatibility(world: "PokemonFRLGWorld") -> None:
    if (world.options.hm_compatibility == HmCompatibility.special_range_names["vanilla"] and
            world.options.tm_tutor_compatibility == TmTutorCompatibility.special_range_names["vanilla"]):
        return

    patch = world.patch_data
    learnsets_address = data.rom_addresses["sTMHMLearnsets"]
    for species in world.modified_species.values():
        patch.write_token(learnsets_address,
                          species.species_id * 8,
                          struct.pack("<Q", species.tm_hm_compatibility))


def _set_tm_moves(world: "PokemonFRLGWorld") -> None:
    if not world.options.tm_tutor_moves:
        return

    patch = world.patch_data
    address = data.rom_addresses["sTMHMMoves"]
    for i, move in enumerate(world.modified_tmhm_moves):
        # Don't modify HMs
        if i >= 50:
            break
        patch.write_token(address, i * 2, struct.pack("<H", move))


def _randomize_move_tutors(world: "PokemonFRLGWorld") -> None:
    patch = world.patch_data

    if world.options.tm_tutor_moves:
        new_tutor_moves = randomize_tutor_moves(world)
        address = data.rom_addresses["gTutorMoves"]

        for i, move in enumerate(new_tutor_moves):
            patch.write_token(address, i * 2, struct.pack("<H", move))

    if world.options.tm_tutor_compatibility != TmTutorCompatibility.special_range_names["vanilla"]:
        learnsets_address = data.rom_addresses["sTutorLearnsets"]

        for species in world.modified_species.values():
            patch.write_token(
                learnsets_address,
                species.species_id * 2,
                struct.pack("<H", bool_array_to_int([
                    world.random.randrange(0, 100) < world.options.tm_tutor_compatibility.value
                    for _ in range(16)
                ]))
            )


def _set_types_damage_categories(world: "PokemonFRLGWorld") -> None:
    if world.options.damage_categories == RandomizeDamageCategories.option_vanilla:
        return

    patch = world.patch_data
    address = data.rom_addresses["sDamageTypeTable"]
    for i, damage_category in enumerate(world.modified_type_damage_categories):
        patch.write_token(address, i, struct.pack("<B", damage_category))


def _set_moves(world: "PokemonFRLGWorld") -> None:
    if (world.options.move_types == RandomizeMoveTypes.option_vanilla and
            world.options.damage_categories == RandomizeDamageCategories.option_vanilla):
        return

    patch = world.patch_data
    for move in world.modified_moves.values():
        address = move.address
        patch.write_token(address, 2, struct.pack("<B", move.type))
        patch.write_token(address, 9, struct.pack("<B", move.category))
