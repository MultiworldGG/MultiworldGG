from typing import List, Any, Dict

import os
import random
import Utils
from settings import get_settings
from ..common.patching.RomData import *
from .Util import *
from ..common.patching.z80asm.Assembler import Z80Assembler
from ..data.Constants import *
from .Constants import *
from pathlib import Path

from ..data.Locations import LOCATIONS_DATA
from ..data.Entrances import WARPS_DATA, WARP_SOURCE_TABLE, WARP_DEST_TABLE
from ..Options import *

locations = {}

def get_treasure_addr(rom: RomData, item_name: str):
    item_id, item_subid = get_item_id_and_subid(item_name)
    addr = 0x59332 + (item_id * 4)
    if rom.read_byte(addr) & 0x80 != 0:
        addr = 0x54000 + rom.read_word(addr + 1)
    return addr + (item_subid * 4)

def apworld_path(file_path) -> str:
    path = Utils.user_path("lib/" if os.path.exists(Utils.user_path("lib")) else "")
    path += "custom_" if os.path.exists(os.path.join(path, Utils.user_path("custom_worlds"))) else ""
    world_path = "worlds/tloz_ooa"
    world_path_from_source = Utils.user_path(world_path)
    path += world_path
    
    def path_exists(p):
        if not os.path.exists(p):
            raise FileNotFoundError(f"Your apworld could not be found inside {p} for some reason.")
        path = os.path.join(p, file_path)
        if os.path.exists(path):
            return path
        raise FileNotFoundError(f"Your file could not be found inside {path}") 
    
    return path_exists(world_path_from_source if os.path.exists(world_path_from_source) else path)

def list_files(dir_name) -> dict[str, Any]:
    dir_name = apworld_path(dir_name)
    files = {}
    for filename in os.listdir(dir_name):
        fullpath = os.path.join(dir_name, filename)
        files[fullpath] = list_files(fullpath) if os.path.isdir(fullpath) else None
    return files


def set_treasure_data(rom: RomData,
                      item_name: str, text_id: int | None,
                      sprite_id: int | None = None,
                      param_value: int | None = None):
    addr = get_treasure_addr(rom, item_name)
    if text_id is not None:
        rom.write_byte(addr + 0x02, text_id)
    if sprite_id is not None:
        rom.write_byte(addr + 0x03, sprite_id)
    if param_value is not None:
        rom.write_byte(addr + 0x01, param_value)

def alter_treasures(rom: RomData):

    set_treasure_data(rom, "Potion", 0x6d)

    # Set data for remote Archipelago items
    set_treasure_data(rom, "Archipelago Item", 0x57, 0x5a)
    set_treasure_data(rom, "Archipelago Progression Item", 0x57, 0x59)
    set_treasure_data(rom, "King Zora's Potion", 0x45, 0x5e)

    # Make bombs increase max carriable quantity when obtained from treasures,
    # not drops (see asm/seasons/bomb_bag_behavior)
    set_treasure_data(rom, "Bombs (10)", None, None, 0x90)

def define_static_items_table(assembler: Z80Assembler, patch_data: dict[str, Any]):
    # Format is group,room,treasure_id,treasure_subid
    static_item_replacements_table = [
        # ------- Freestanding items -------
        0x01, 0x86, locations["blackTowerHP"]["id"], locations["blackTowerHP"]["subid"],
        0x04, 0x06, locations["makuPathHP"]["id"], locations["makuPathHP"]["subid"],
        0x00, 0x8b, locations["yollGraveyardHP"]["id"], locations["yollGraveyardHP"]["subid"],
        0x05, 0xb1, locations["dekuForestHP"]["id"], locations["dekuForestHP"]["subid"],
        0x03, 0xaf, locations["restorationWallHP"]["id"], locations["restorationWallHP"]["subid"],
        0x00, 0x11, locations["symmetryCityHP"]["id"], locations["symmetryCityHP"]["subid"],
        0x05, 0xc1, locations["ridgeWestHP"]["id"], locations["ridgeWestHP"]["subid"],
        0x00, 0x0d, locations["ridgeUpperHP"]["id"], locations["ridgeUpperHP"]["subid"],
        0x06, 0x05, locations["d0Basement"]["id"], locations["d0Basement"]["subid"],
        0x06, 0x10, locations["d1Basement"]["id"], locations["d1Basement"]["subid"],
        0x06, 0x28, locations["d2ThwompTunnel"]["id"], locations["d2ThwompTunnel"]["subid"],
        0x06, 0x27, locations["d2ThwompShelf"]["id"], locations["d2ThwompShelf"]["subid"],

        # ------- Drops / spawned items -------
        0x04, 0x1e, locations["d1GhiniDrop"]["id"], locations["d1GhiniDrop"]["subid"],
        0x04, 0x39, locations["d2MoblinDrop"]["id"], locations["d2MoblinDrop"]["subid"],
        0x04, 0x42, locations["d2StatuePuzzle"]["id"], locations["d2StatuePuzzle"]["subid"],
        0x04, 0x2e, locations["d2BasementDrop"]["id"], locations["d2BasementDrop"]["subid"],
        0x04, 0x5e, locations["d3ArmosDrop"]["id"], locations["d3ArmosDrop"]["subid"],
        0x04, 0x61, locations["d3StatueDrop"]["id"], locations["d3StatueDrop"]["subid"],
        0x04, 0x64, locations["d3SixBlocDrop"]["id"], locations["d3SixBlocDrop"]["subid"],
        0x04, 0x4b, locations["d3MoldormDrop"]["id"], locations["d3MoldormDrop"]["subid"],
        0x04, 0x7b, locations["d4ColorDrop"]["id"], locations["d4ColorDrop"]["subid"],
        0x05, 0x53, locations["d7CaneDiamondPuzzle"]["id"], locations["d7CaneDiamondPuzzle"]["subid"],
        0x05, 0x4b, locations["d7FlowerRoom"]["id"], locations["d7FlowerRoom"]["subid"],
        0x05, 0x55, locations["d7DiamondPuzzle"]["id"], locations["d7DiamondPuzzle"]["subid"]
    ]
    
    if patch_data["options"]["linked_heros_cave"] > 0:
        static_item_replacements_table.extend([
            0x04, 0xcd, locations["d11Statue3Puzzle"]["id"], locations["d11Statue3Puzzle"]["subid"]
        ])

    if patch_data["options"]["miniboss_locations"]:
        miniboss_room_bytes = [0x18, 0x34, 0x4d, 0x80, 0xb4, 0x12, 0x4a, 0x82]
        for i in range(len(miniboss_room_bytes)):
            group = 0x04 if i <= 4 else 0x07 if i == 6 else 0x05
            location = locations[f"d{i + 1}Miniboss"]
            static_item_replacements_table.extend([group, miniboss_room_bytes[i], location["id"], location["subid"]])

    assembler.add_floating_chunk("staticItemsReplacementsTable", static_item_replacements_table)

def get_asm_files(patch_data):
    asm_files = ASM_FILES.copy()
    if get_settings()["tloz_ooa_options"]["qol_quick_flute"]:
        asm_files.append("asm/conditional/quick_flute.yaml")
    if get_settings()["tloz_ooa_options"]["skip_tokkey_dance"]:
        asm_files.append("asm/conditional/skip_dance.yaml")
    if get_settings()["tloz_ooa_options"]["skip_boi_joke"]:
        asm_files.append("asm/conditional/skip_joke.yaml")
    if get_settings()["tloz_ooa_options"]["qol_mermaid_suit"]:
        asm_files.append("asm/conditional/qol_mermaid_suit.yaml")
    if get_settings()["tloz_ooa_options"]["mute_music"]:
        asm_files.append("asm/conditional/mute_music.yaml")
    if patch_data["options"]["lynna_gardener"]:
        asm_files.append("asm/conditional/lynna_gardener.yaml")
    if patch_data["options"]["miniboss_locations"]:
        asm_files.append("asm/conditional/miniboss_locations.yaml")
    if patch_data["options"]["secret_locations"]:
        asm_files.append("asm/conditional/secret_locations.yaml")
    if patch_data["options"]["goal"] == OracleOfAgesGoal.option_beat_ganon:
        asm_files.append("asm/conditional/ganon_goal.yaml")
    if get_settings()["tloz_ooa_options"]["skip_intro_cinematic"]:
        asm_files.append("asm/conditional/intro_cinematic_skip.yaml")
    if patch_data["options"]["linked_heros_cave"]:
        asm_files.append("asm/conditional/d11.yaml")
        if patch_data["options"]["linked_heros_cave"] == OracleOfAgesLinkedHerosCave.option_maku_tree_entrance_right_side:
            asm_files.append("asm/conditional/d11_in_maku_tree_entrance_right_side.yaml")
    return asm_files

def define_location_constants(assembler: Z80Assembler, patch_data):
    for location_name, location_data in LOCATIONS_DATA.items():
        if "symbolic_name" not in location_data:
            continue
        symbolic_name = location_data["symbolic_name"]

        if location_name in patch_data["locations"]:
            item_name = patch_data["locations"][location_name]
        else:
            # Put a fake item for disabled locations, since they are unreachable anwyway
            item_name =  "Rupees (1)"

        if item_name == "Flute":
            item_name = COMPANIONS[patch_data["options"]["animal_companion"]] + "'s Flute"

        item_id, item_subid = get_item_id_and_subid(item_name)
        locations[symbolic_name] = {
            "fullid": (item_id << 8) + item_subid,
            "id": item_id,
            "subid": item_subid
        }
        assembler.define_byte(f"locations.{symbolic_name}.id", item_id)
        assembler.define_byte(f"locations.{symbolic_name}.subid", item_subid)
        assembler.define_word(f"locations.{symbolic_name}", (item_id << 8) + item_subid)

    # Process deterministic Gasha Nut locations to define a table
    deterministic_gasha_table = []
    for i in range(int(patch_data["options"]["deterministic_gasha_locations"])):
        item = patch_data["locations"][f"Gasha Nut #{i + 1}"]
        item_id, item_subid = get_item_id_and_subid(item)
        deterministic_gasha_table.extend([item_id, item_subid])
    assembler.add_floating_chunk("deterministicGashaLootTable", deterministic_gasha_table)
    
    if patch_data["options"]["linked_heros_cave"]:
        assembler.define_byte("d11", 0x01)

def set_faq_text(assembler: Z80Assembler):
    faq_intro_text = text_to_binary(("Welcome to the "
                        "OoA randomizer "
                        "for Archipelago! "
                        "Did you read "
                        "the FAQ, because there are important randomizer mechanics in it."))
    faq_intro_text.extend([0x00])
    assembler.add_floating_chunk("text.faqIntro", faq_intro_text)
        
def define_option_constants(assembler: Z80Assembler, patch_data):
    options = patch_data["options"]

    # if not hasattr(get_settings().tloz_ooa_options, "beat_tutorial"):
        # assembler.define_byte("option.startingGroup", 0x03)
        # assembler.define_byte("option.startingRoom", 0xbf)
        # assembler.define_byte("option.startingXPos", 0x60)
        # assembler.define_byte("option.startingYPos", 0x70)
    # else: # Redirect user to the first item check, saving them some time.
    assembler.define_byte("option.startingGroup", 0x00)
    assembler.define_byte("option.startingRoom", 0x39)
    assembler.define_byte("option.startingXPos", 0x58)
    assembler.define_byte("option.startingYPos", 0x58)

    if options["vasu_ring_checks_requirement"]["disable_entirely"] == False:
        assembler.define_word("option.vasuSlayerRingCheckRequirement", options["vasu_ring_checks_requirement"]["amount_of_enemies_defeated_for_slayer_ring_check"])
        ## Game use hexadecimal as decimal for rupee count, so we translate from decimal to hexadecimal to have the correct value
        ## + we remove one to the count because with current implementation it only work once you go beyond the rupee count given in the option.
        assembler.define_word("option.vasuRupeeRingCheckRequirement", int(str(options["vasu_ring_checks_requirement"]["rupee_requirement_for_rupee_ring_check"]-1),16))
    else:
        assembler.define_word("option.vasuSlayerRingCheckRequirement", 1000)
        assembler.define_word("option.vasuRupeeRingCheckRequirement", int(str(9999),16))


    assembler.define_byte("option.warpingGroup", patch_data["warp_to_start_variables"]["group"] if "group" in patch_data["warp_to_start_variables"] else 0x00)
    assembler.define_byte("option.warpingRoom", patch_data["warp_to_start_variables"]["room"] if "room" in patch_data["warp_to_start_variables"] else 0x59)
    assembler.define_byte("option.warpingPos", patch_data["warp_to_start_variables"]["pos"] if "pos" in patch_data["warp_to_start_variables"] else 0x55)
    assembler.define_byte("option.warpingDestTransittion", patch_data["warp_to_start_variables"]["dest_transittion"] if "dest_transittion" in patch_data["warp_to_start_variables"] else 0x05)
    assembler.define_byte("option.warpingSrcTransittion", patch_data["warp_to_start_variables"]["src_transittion"] if "src_transittion" in patch_data["warp_to_start_variables"] else 0x03)

    assembler.define_byte("option.animalCompanion", 0x0b + patch_data["options"]["animal_companion"])
    assembler.define_byte("option.defaultSeedType", 0x20 + patch_data["options"]["default_seed"])
    assembler.define_byte("option.receivedDamageModifier", options["combat_difficulty"])
    assembler.define_byte("option.openAdvanceShop", options["advance_shop"])

    assembler.define_byte("option.requiredEssences", options["required_essences"])
    assembler.define_byte("option.required_slates", options["required_slates"])
    
    assembler.define_byte("option.keysanity_small_keys", patch_data["options"]["keysanity_small_keys"])
    keysanity = patch_data["options"]["keysanity_small_keys"] or patch_data["options"]["keysanity_boss_keys"]
    assembler.define_byte("option.customCompassChimes", 1 if keysanity else 0)

    master_keys_as_boss_keys = patch_data["options"]["master_keys"] == OraclesMasterKeys.option_all_dungeon_keys
    assembler.define_byte("option.smallKeySprite", 0x43 if master_keys_as_boss_keys else 0x42)
    assembler.define_byte("option.deterministicGashaLootCount", options["deterministic_gasha_locations"])

    always_available_potion_option = patch_data["options"]["enforce_potion_in_shop"]
    assembler.define_byte("option.lynnacityShopSlot3Renewable", 0x00 if always_available_potion_option == OracleOfAgesEnforcePotionInShop.option_lynna_shop else 0x80)
    assembler.define_byte("option.syrupHutSlot3Renewable", 0x00 if always_available_potion_option == OracleOfAgesEnforcePotionInShop.option_syrup_hut else 0x40)

    if options["secret_locations"]:
        assembler.add_floating_chunk("unsetglobalflag_librarySecret", [
            0xb6, (0x4f | 0x80)
        ])

def parse_int(s):
    try:
        return int(s)
    except ValueError:
        return None # Return None if parsing fails

def text_to_binary(text: str) -> List[int]:
    words = text.split(" ")
    current_line = 0
    lines = [""]
    while len(words) > 0:
        line_with_word = lines[current_line]
        if len(line_with_word) > 0:
            line_with_word += " "
        line_with_word += words[0]
        if len(line_with_word) <= 16:
            lines[current_line] = line_with_word
        else:
            current_line += 1
            lines.append(words[0])
        words = words[1:]

    result = []
    for line in lines:
        if len(result) > 0:
            result.append(0x01)  # Newline
        for i in range(len(line)):
            char = line[i:i+1]
            if parse_int(char) is not None:
                result.append(0x30 + int(char))
            else:
                info = next(stuff for stuff in ascii_printable_chars_table if stuff["Character"] == char)
                result.append(info["Hexadecimal"])
    return result

def define_text_constants(assembler: Z80Assembler, patch_data):
    overworld_shops = [
        "Lynna City: Shop",
        "Lynna City: Hidden Shop",
        "Yoll Graveyard: Syrup Shop",
        "Lynna Village: Advance Shop",
    ]

    for shop_name in overworld_shops:
        for i in range(1, 4):
            location_name = f"{shop_name} Item #{i}"
            symbolic_name = LOCATIONS_DATA[location_name]["symbolic_name"]
            text_bytes = []
            if location_name in patch_data["locations"]:
                item_name_bytes = text_to_binary(patch_data["locations"][location_name])
                text_bytes = [0x09, 0x01] + item_name_bytes + [0x09, 0x00, 0x0c, 0x18, 0x01]  # Item name
                if shop_name != "Crescent Island (Past): Market":
                    text_bytes.extend([0x20, 0x0c, 0x08, 0x20, 0x03, 0x7b, 0x01])  # Price
                    text_bytes.extend([0x02, 0x00, 0x00])  # OK / No thanks
            assembler.add_floating_chunk(f"text.{symbolic_name}", text_bytes)

    #Tokay Market
    shop_name = "Crescent Island (Past): Market"
    for i in range(1, 3):
        location_name = f"{shop_name} Item #{i}"
        symbolic_name = LOCATIONS_DATA[location_name]["symbolic_name"]
        text_bytes = []
        if location_name in patch_data["locations"]:
            item_name_bytes = text_to_binary(patch_data["locations"][location_name])
            text_bytes = [0x09, 0x01] + item_name_bytes + [0x09, 0x00, 0x0c, 0x18, 0x00]  # Item name
            assembler.add_floating_chunk(f"text.{symbolic_name}", text_bytes)
    text_bytes = [0x31, 0x30, 0x20, 0x02, 0x12, 0x01, 0x02, 0x00, 0x00]
    assembler.add_floating_chunk(f"text.tokayMarket1Validation", text_bytes)


def write_chest_contents(rom: RomData, patch_data):
    """
    Chest locations are packed inside several big tables in the ROM, unlike other more specific locations.
    This puts the item described in the patch data inside each chest in the game.
    """
    locations_data = patch_data["locations"]
    for location_name, location_data in LOCATIONS_DATA.items():
        if (
            'collect' not in location_data 
            or 'room' not in location_data 
            or location_data['collect'] != COLLECT_CHEST
            or location_name not in locations_data
        ) and location_name != "Rolling Ridge (Present): Bush Cave Chest" and location_name != "Crescent Island (Past): Crystal Cave Chest":
            continue
        if location_name == "Nuun Highlands: Southern Cave":
            chest_addr = rom.get_chest_addr(location_data['room'][patch_data["options"]["animal_companion"]], 0x16, 0x5108)
        else:
            chest_addr = rom.get_chest_addr(location_data['room'], 0x16, 0x5108)
        item_name = locations_data[location_name]
        item_id, item_subid = get_item_id_and_subid(item_name)
        rom.write_byte(chest_addr, item_id)
        rom.write_byte(chest_addr + 1, item_subid)


def define_compass_rooms_table(assembler: Z80Assembler, patch_data):
    table = []
    for location_name, item_name in patch_data["locations"].items():
        _, item_subid = get_item_id_and_subid(item_name)
        dungeon = 0xff
        if item_name.startswith("Small Key") or item_name.startswith("Master Key"):
            dungeon = item_subid
        elif item_name.startswith("Boss Key"):
            dungeon = item_subid + 1

        if dungeon != 0xff:
            location_data = LOCATIONS_DATA[location_name]
            rooms = location_data["room"]
            if not isinstance(rooms, list):
                rooms = [rooms]
            for room in rooms:
                room_id = room & 0xff
                group_id = room >> 8
                table.extend([group_id, room_id, dungeon])
    table.append(0xff)  # End of table
    assembler.add_floating_chunk("compassRoomsTable", table)
       

def define_collect_properties_table(assembler: Z80Assembler, patch_data):
    """
    Defines a table of (group, room, collect mode) entries for randomized items
    to determine how they spawn, how they are grabbed and whether they set
    a room flag when obtained.
    """
    table = []
    for location_name, item_name in patch_data["locations"].items():
        location_data = LOCATIONS_DATA[location_name]
        if "collect" not in location_data or "room" not in location_data:
            continue
        mode = location_data["collect"]

        # Use no pickup animation for falling small keys
        if mode == COLLECT_DROP and item_name.startswith("Small Key"):
            mode &= 0xf8  # Set grab mode to TREASURE_GRAB_INSTANT

        rooms = location_data["room"]
        if not isinstance(rooms, list):
            rooms = [rooms]
        for room in rooms:
            room_id = room & 0xff
            group_id = room >> 8
            table.extend([group_id, room_id, mode])

    table.append(0xff)
    assembler.add_floating_chunk("collectPropertiesTable", table)

    
def inject_slot_name(rom: RomData, slot_name: str):
    slot_name_as_bytes = list(str.encode(slot_name))
    slot_name_as_bytes += [0x00] * (0x40 - len(slot_name_as_bytes))
    rom.write_bytes(0xfffc0, slot_name_as_bytes)

    
def write_seed_tree_content(rom: RomData, patch_data):
    for _, tree_data in SEED_TREE_DATA.items():
        original_data = rom.read_byte(tree_data["codeAdress"])
        item_name = patch_data["locations"][tree_data["location"]]
        item_id, _ = get_item_id_and_subid(item_name)
        newdata = (original_data & 0x0f) | (item_id - 0x20) << 4
        rom.write_bytes(tree_data["codeAdress"], [newdata])

def define_underwater_warp_arraywarps(assembler: Z80Assembler, rom: RomData, patch_data):
    warp_matchings = patch_data["randomized_entrances"]
    # +2 because we only use the 2 last byte of the 4 warp bytes
    outside_values = {name: rom.read_word(GameboyAddress(0x04, warp["outside_warp"]).address_in_rom()) for name, warp in WARPS_DATA.items()}
    inside_values = {name: rom.read_word(GameboyAddress(0x04, warp["inside_warp"]).address_in_rom()) for name, warp in WARPS_DATA.items()}
    
    underwater_warp_table = []

    for outside_name, inside_name in warp_matchings.items():
        if "is_underwater" in WARPS_DATA[outside_name] and WARPS_DATA[outside_name]["is_underwater"]:
            intoout_warp_group = (inside_values[outside_name] & 0xf000) >> 12
            intoout_warp_index = inside_values[outside_name] & 0x00ff
            underwater_warp_table.append(intoout_warp_group)
            underwater_warp_table.append(intoout_warp_index)
            
            outtoin_warp_group = (outside_values[outside_name] & 0xf000) >> 12
            outtoin_warp_index = outside_values[outside_name] & 0x00ff
            underwater_warp_table.append(outtoin_warp_group)
            underwater_warp_table.append(outtoin_warp_index)
    underwater_warp_table.append(0xff)

    assembler.add_floating_chunk("underwaterWarpTable", underwater_warp_table)

def set_dungeon_warps(rom: RomData, patch_data):
    warp_matchings = patch_data["randomized_entrances"]
    # +2 because we only use the 2 last byte of the 4 warp bytes
    outside_values = {name: rom.read_word(GameboyAddress(0x04, warp["outside_warp"]).address_in_rom()) for name, warp in WARPS_DATA.items()}
    inside_values = {name: rom.read_word(GameboyAddress(0x04, warp["inside_warp"]).address_in_rom()) for name, warp in WARPS_DATA.items()}

    # Reading the warp desting table group addresses. Useful for essence warp back.
    warp_dest_table = []
    for i in range(0, 8):
        warp_dest_table.append(rom.read_word(WARP_DEST_TABLE + 2 * i))
    
    # Apply warp matchings expressed in the patch 
    for outside_name, inside_name in warp_matchings.items():
        outside_warp_addr: int = WARPS_DATA[outside_name]["outside_warp"]
        inside_warp_addr: int = WARPS_DATA[inside_name]["inside_warp"]
        rom.write_word(GameboyAddress(0x04, outside_warp_addr).address_in_rom(), outside_values[inside_name])
        rom.write_word(GameboyAddress(0x04, inside_warp_addr).address_in_rom(), inside_values[outside_name])
        
        if ("dungeon" in WARPS_DATA[inside_name]):
            dungeon_number = WARPS_DATA[inside_name]["dungeon"]
                        
            intoout_warp_group = (inside_values[outside_name] & 0xf000) >> 12
            intoout_warp_index = inside_values[outside_name] & 0x00ff
            intoout_warp_dest_address = warp_dest_table[intoout_warp_group] + intoout_warp_index * 3
            intoout_warp_room = rom.read_byte(GameboyAddress(0x04, intoout_warp_dest_address).address_in_rom())
            intoout_warp_position = rom.read_byte(GameboyAddress(0x04, intoout_warp_dest_address + 1).address_in_rom())
            intoout_warp_flag = rom.read_byte(GameboyAddress(0x04, intoout_warp_dest_address + 2).address_in_rom())
            
            # Change Minimap popups to indicate the randomized dungeon's name
            dungeon_txt_id =  0x81 | (dungeon_number << 3)
            if "custom_txt_id" in WARPS_DATA[inside_name]:
                dungeon_txt_id = WARPS_DATA[inside_name]["custom_txt_id"]
            
            tile_group = intoout_warp_group
            basetile_room = intoout_warp_room
            if "custom_map_tile" in WARPS_DATA[outside_name]:
                tile_group = WARPS_DATA[outside_name]["custom_map_tile"] >> 8
                basetile_room = WARPS_DATA[outside_name]["custom_map_tile"] & 0xff
            tile_room = (basetile_room & 0x0f) + (((basetile_room & 0xf0) >> 4) * 14)
            if (tile_group == 0):
                rom.write_byte(0xAAAF + tile_room, dungeon_txt_id)
            if (tile_group == 1):
                rom.write_byte(0xAB73 + tile_room, dungeon_txt_id)

            # ESSENCE WARP
            if dungeon_number == 6 or dungeon_number == 0: # No essence warp for D6 present or maku path
                continue
            if dungeon_number == 9:
                dungeon_number = 6

            if (intoout_warp_flag == 0x4):
                intoout_warp_flag = 0x1 # Force set respawn

            if dungeon_number == 11: # NOTE : No need to check for the option. If it's not set, it shouldn't be in the array in the first place
                rom.write_bytes(GameboyAddress(0x0a, 0x7204).address_in_rom(), [
                    intoout_warp_group | 0x80,
                    intoout_warp_room,
                    intoout_warp_flag, 
                    intoout_warp_position, 
                    (intoout_warp_group * 0x10) + 0x03
                ])
            else:
                rom.write_bytes(0x2874f + ((dungeon_number - 1) * 4), [
                    intoout_warp_group | 0x80,
                    intoout_warp_room,
                    intoout_warp_position,
                    intoout_warp_flag
                ])

def define_tile_replacements_table(assembler: Z80Assembler, patch_data):
    # NOTE ; The fifth bit (which normally determine if a map has been visited) is used to know if the test is negative
    # For instance 0x12 test if the second bit is 0
    # and 0x02 test if the second bit 1
    new_tiles_table = [
        0x00, 0x20, 0x00, 0x61, 0xd7, # portal in talus peaks
        0x01, 0x48, 0x00, 0x45, 0xd7, # portal south of past maku tree
        0x00, 0x37, 0x12, 0x43, 0xd7, # portal in southeast ricky/moosh nuun
        0x00, 0x6b, 0x00, 0x42, 0x3a, # removed tree in yoll graveyard
        0x00, 0x6b, 0x12, 0x42, 0xce, # not removed tree in yoll graveyard
        0x00, 0x83, 0x00, 0x43, 0xa4, # rock outside D2
        0x03, 0x0f, 0x00, 0x66, 0xf9, # water in d6 past entrance
        0x01, 0x13, 0x00, 0x61, 0xd7, # portal in symmetry city past
        0x01, 0x13, 0x00, 0x68, 0xd7, # portal in symmetry city past
        0x00, 0x25, 0x00, 0x37, 0xd7, # portal in nuun highlands
        0x05, 0xda, 0x11, 0xa4, 0xb2, # tunnel to moblin keep
        0x05, 0xda, 0x11, 0xa5, 0xb2, # cont.
        0x05, 0xda, 0x11, 0xa6, 0xb2, # cont.
        0x00, 0x24, 0x12, 0x49, 0x63, # other side of symmetry city bridge
        0x00, 0x24, 0x12, 0x59, 0x63, # cont.
        0x00, 0x24, 0x12, 0x69, 0x63, # cont.
        0x00, 0x24, 0x12, 0x79, 0x73, # cont.
        0x01, 0x2c, 0x00, 0x70, 0x69, # ledge in rolling ridge east past
        0x01, 0x2c, 0x00, 0x71, 0x06, # cont.
        0x01, 0x2c, 0x00, 0x72, 0x67, # cont.
        0x01, 0xa5, 0x00, 0x35, 0x48, # ledge by library past
        0x01, 0xa5, 0x00, 0x45, 0x0b, # cont.
        0x01, 0xa5, 0x00, 0x55, 0x6c, # cont.
        0x00, 0x83, 0x00, 0x44, 0xd7, # portal outside D2 present
        0x01, 0x48, 0x12, 0x31, 0xcd, # past maku road: remove dirt when exiting
        # 0x00, 0x5d, 0x00, 0x66, 0x0b, # ledge by the linked ghini ghost (traps link in ghini's interaction space until warp to start is initialized (used for faq room space))
        # 0x00, 0x5d, 0x00, 0x57, 0xf4, # waterblock for preventing the trapped player from escaping into the graveyard
    ]

    if patch_data["options"]["secret_locations"]: # Format is group, room, room flag, position in YX format, and replacement tile byte.
        new_tiles_table.extend([
            0x01, 0xc6, 0x00, 0x47, 0x30, # add a small sand bank in the sea of storms past to allow players to time travel to the present sea of storms.
            0x01, 0xc6, 0x00, 0x48, 0x32, # ^
            0x01, 0xc6, 0x00, 0x57, 0x33, # ^
            0x01, 0xc6, 0x00, 0x58, 0x35, # ^
            0x03, 0xc6, 0x00, 0x47, 0x80, # add a tree underwater to avoid surfacing where there is the sand bank
            0x03, 0xc6, 0x00, 0x48, 0x81, # ^
            0x03, 0xc6, 0x00, 0x57, 0x90, # ^
            0x03, 0xc6, 0x00, 0x58, 0x91, # ^
            0x00, 0x76, 0x00, 0x55, 0xa7, # add walkable tiles to black tower present entrance
            0x00, 0x76, 0x00, 0x54, 0xa7, # ^
        ])

    
    """
    Define a list of entries following the format of `tileReplacementsTable` (see ASM for more info) which end up
    being tile replacements on various rooms in the game.
    """
    # Remove Gasha spots when harvested once if deterministic Gasha locations are enabled
    if patch_data["options"]["deterministic_gasha_locations"] > 0:
        new_tiles_table.extend([

            0x00, 0xd7, 0x20, 0x25, 0x1c,    # Sea of Storms (Present) Gasha Spot
            0x00, 0xcb, 0x20, 0x62, 0x1c,    # Crescent Island West (Present) Gasha Spot
            0x00, 0xad, 0x20, 0x36, 0x1c,    # Crescent Island East (Present) Gasha Spot
            0x00, 0x90, 0x20, 0x61, 0x1c,    # Fairies' Woods Gasha Spot
            0x00, 0x7b, 0x20, 0x26, 0x1c,    # Yoll Graveyard Gasha Spot
            0x00, 0x30, 0x20, 0x52, 0x1c,    # Talus Peeks (Present) Gasha Spot
            0x00, 0x2c, 0x20, 0x34, 0x1c,    # Rolling Ridge (Present, East) Gasha Spot
            0x00, 0x05, 0x20, 0x26, 0x1c,    # Nuun Highlands Gasha Spot
            0x01, 0xd0, 0x20, 0x31, 0x1c,    # Zora Vilage Gasha Spot
            0x01, 0xca, 0x20, 0x43, 0x1c,    # Crescent Island West (Past) Gasha Spot
            0x01, 0x95, 0x20, 0x31, 0x1c,    # Southern Shore Gasha Spot
            0x01, 0x55, 0x20, 0x21, 0x1c,    # Lynna Village Gasha Spot
            0x01, 0x34, 0x20, 0x45, 0x1c,    # Deku Forest Gasha Spot
            0x01, 0x0a, 0x20, 0x66, 0x1c,    # Rolling Ridge (Past, Upper) Gasha Spot
            0x01, 0x01, 0x20, 0x23, 0x1c,    # Talus Peeks (Past) Gasha Spot
            0x01, 0x28, 0x20, 0x63, 0x1c,    # Rolling Ridge (Past, West) Gasha Spot
        ])

    assembler.add_floating_chunk("tileReplacementsTable", new_tiles_table)

def define_dungeon_items_text_constants(assembler: Z80Assembler, patch_data):

    for i in range(0, 11): # Maku Path and Hero's Cave has no map, no compass, no boss key, and the unique small key use the default text. 
        # " for\nDungeon X"
        trueI = i if i != 9 else 6
        if trueI == 10:
            trueI = 11
        dungeon_precision = [0x03, 0x39]
        dungeon_tag = f"D{trueI}"
        dungeon_precision.extend(text_to_binary((f"{DUNGEON_NAMES[trueI]} ({dungeon_tag})") if get_settings().tloz_ooa_options["simplify_dungeon_precision_text"] else (
            f"Dungeon {dungeon_tag[1:]}"
        )))
        dungeon_precisionForBossKey = dungeon_precision.copy()

        if i == 6:
            #\n(present)
            dungeon_precision.extend([0x01, 0x28, 0x03, 0x2e, 0x29])
            dungeon_tag += "Present"
        if i == 9:
            #\n(past)
            dungeon_precision.extend([0x01, 0x28, 0x70, 0x61, 0x73, 0x74, 0x29])
            dungeon_tag += "Past"

        # ###### Small keys ##############################################
        # "You found a\n\color(RED)"
        small_key_text = [0x02, 0x7c, 0x20, 0x61, 0x01, 0x09, 0x01]
        if patch_data["options"]["master_keys"]:
            # "Master Key"
            small_key_text.extend([0x4d, 0x61, 0x73, 0x74, 0x65, 0x72, 0x20, 0x03, 0x37])
        else:
            # "Small Key"
            small_key_text.extend([0x53, 0x6d, 0x04, 0xd2, 0x4b, 0x65, 0x79])
        if patch_data["options"]["keysanity_small_keys"]:
            small_key_text.extend(dungeon_precision)
        small_key_text.extend([0x09, 0x00, 0x21, 0x00])  # "\color(WHITE)!(end)"
        assembler.add_floating_chunk(f"text.smallKey{dungeon_tag}", small_key_text)

        # Maku Path & Hero Cave only has Small Keys, so skip other texts
        if i == 0 or i == 10:
            continue

        # ###### Boss keys ##############################################
        # "You found the\n\color(RED)Boss Key"
        if i < 9:
            boss_key_text = [
                0x02, 0x7c, 0x20, 0x05, 0xb4,
                0x09, 0x01, 0x42, 0x6f, 0x73, 0x73, 0x20, 0x4b, 0x65, 0x79
            ]
            if patch_data["options"]["keysanity_boss_keys"]:
                boss_key_text.extend(dungeon_precisionForBossKey)
            boss_key_text.extend([0x09, 0x00, 0x21, 0x00])  # "\color(WHITE)!(end)"
            assembler.add_floating_chunk(f"text.bossKeyD{trueI}", boss_key_text)

        # ###### Dungeon maps ##############################################
        # "You found the\n\color(RED)"
        dungeon_map_text = [0x02, 0x7c, 0x20, 0x05, 0xb4, 0x09, 0x01]
        dungeon_map_text.extend(text_to_binary("Dungeon Map"))
        if patch_data["options"]["keysanity_maps_compasses"]:
            dungeon_map_text.extend(dungeon_precision)
        dungeon_map_text.extend([0x09, 0x00, 0x21, 0x00])  # "\color(WHITE)!(end)"
        assembler.add_floating_chunk(f"text.dungeonMap{dungeon_tag}", dungeon_map_text)

        # ###### Compasses ##############################################
        # "You found the\n\color(RED)Compass"
        compasses_text = [
            0x02, 0x7c, 0x20, 0x05, 0xb4, 0x09, 0x01,
            0x09, 0x01, 0x43, 0x6f, 0x6d, 0x05, 0xfe
        ]
        if patch_data["options"]["keysanity_maps_compasses"]:
            compasses_text.extend(dungeon_precision)
        compasses_text.extend([0x09, 0x00, 0x21, 0x00])  # "\color(WHITE)!(end)"
        assembler.add_floating_chunk(f"text.compass{dungeon_tag}", compasses_text)

def set_file_select_text(assembler: Z80Assembler, slot_name: str):
    def char_to_tile(c: str) -> int:
        if '0' <= c <= '9':
            return ord(c) - 0x20
        if 'A' <= c <= 'Z':
            return ord(c) + 0xa1
        if c == '+':
            return 0xfd
        if c == '-':
            return 0xfe
        if c == '.':
            return 0xff
        else:
            return 0xfc  # All other chars are blank spaces
    from .. import OracleOfAgesWorld
    row_1 = [char_to_tile(c) for c in f"ARCHIP. {OracleOfAgesWorld.version()}"]
    row_1_left_padding = int((16 - len(row_1)) / 2)
    row_1_right_padding = int(16 - row_1_left_padding - len(row_1))
    row_1 = ([0x00] * row_1_left_padding) + row_1 + ([0x00] * row_1_right_padding)
    row_2 = [char_to_tile(c) for c in slot_name.replace("-", " ").upper()]
    row_2_left_padding = int((16 - len(row_2)) / 2)
    row_2_right_padding = int(16 - row_2_left_padding - len(row_2))
    row_2 = ([0x00] * row_2_left_padding) + row_2 + ([0x00] * row_2_right_padding)

    text_tiles = [0x74, 0x31]
    text_tiles.extend(row_1)
    text_tiles.extend([0x41, 0x40])
    text_tiles.extend([0x02] * 12)  # Offscreen tiles

    text_tiles.extend([0x40, 0x41])
    text_tiles.extend(row_2)
    text_tiles.extend([0x51, 0x50])
    text_tiles.extend([0x02] * 12)  # Offscreen tiles

    assembler.add_floating_chunk("dma_FileSelectStringTiles", text_tiles)

    
def set_heart_beep_interval_from_settings(rom: RomData):
    heart_beep_interval = get_settings()["tloz_ooa_options"]["heart_beep_interval"]
    if heart_beep_interval == "half":
        rom.write_byte(0x914B, 0x3f * 2)
    elif heart_beep_interval == "quarter":
        rom.write_byte(0x914B, 0x3f * 4)
    elif heart_beep_interval == "disabled":
        rom.write_bytes(0x914B, [0x00, 0xc9])  # Put a return to avoid beeping entirely

def set_character_sprite_from_settings(rom: RomData):
    sprite = get_settings()["tloz_ooa_options"]["character_sprite"]
    sprite_dir = Path(Utils.local_path(os.path.join('data', 'sprites', 'oos_ooa')))
    if sprite == "random":
        sprite_filenames = [f for f in os.listdir(sprite_dir) if sprite_dir.joinpath(f).is_file() and f.endswith(".bin")]
        sprite = sprite_filenames[random.randint(0, len(sprite_filenames) - 1)]
    elif not sprite.endswith(".bin"):
        sprite += ".bin"
    if sprite != "link.bin":
        sprite_path = sprite_dir.joinpath(sprite)
        if not (sprite_path.exists() and sprite_path.is_file()):
            raise ValueError(f"Path '{sprite_path}' doesn't exist")
        sprite_bytes = list(Path(sprite_path).read_bytes())
        rom.write_bytes(0x68000, sprite_bytes)

    palette = get_settings()["tloz_ooa_options"]["character_palette"]
    if palette == "random":
        palette = random.choice(get_available_random_colors_from_sprite_name(sprite))

    if palette == "green":
        return  # Nothing to change
    if palette not in PALETTE_BYTES:
        raise ValueError(f"Palette color '{palette}' doesn't exist (must be 'green', 'blue', 'red' or 'orange')")
    palette_byte = PALETTE_BYTES[palette]

    # Link in-game
    for addr in range(0x1420e, 0x14221, 2):
        rom.write_byte(addr, 0x08 | palette_byte)
    # Link palette restored after Medusa Head / Ganon stun attacks
    rom.write_byte(0x15271, 0x08 | palette_byte)
    # Link standing still in file select (fileSelectDrawLink:@sprites0)
    rom.write_byte(0x8d86, palette_byte)
    rom.write_byte(0x8d8a, palette_byte)
    # Link animated in file select (@sprites1 & @sprites2)
    rom.write_byte(0x8d8f, palette_byte)
    rom.write_byte(0x8d93, palette_byte)
    rom.write_byte(0x8d98, 0x20 | palette_byte)
    rom.write_byte(0x8d9c, 0x20 | palette_byte)

def apply_misc_option(rom: RomData, patch_data):
    if patch_data["options"]["master_keys"] != OraclesMasterKeys.option_disabled:
        # Remove small key consumption on keydoor opened
        rom.write_byte(0x18366, 0x00)
        # Change obtention text
        rom.write_bytes(0x78247, [0x4d, 0x61, 0x73, 0x74, 0x65, 0x72, 0x20, 0x4b, 0x65, 0x79, 0x09, 0x01, 0x21, 0x00]) # I really wish that the dictionnay of ages would be more useful...
    if patch_data["options"]["master_keys"] == OraclesMasterKeys.option_all_dungeon_keys:
        # Remove boss key consumption on boss keydoor opened (boss door behave like normal locked door)
        rom.write_word(0x1835e, 0x0000)
    
    rom.write_byte(GameboyAddress(0x0B, 0x4445).address_in_rom(), patch_data["options"]["gasha_nut_kill_requirement"])
    rom.write_byte(GameboyAddress(0x02, 0x7d03).address_in_rom(), patch_data["options"]["gasha_nut_kill_requirement"] // 2)
