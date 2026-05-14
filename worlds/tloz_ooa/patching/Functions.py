from typing import List, Any

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

from .. import LOCATIONS_DATA
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
            item_name = location_data["vanilla_item"]

        if item_name == "Flute":
            item_name = COMPANIONS[patch_data["options"]["animal_companion"]] + "'s Flute"

        item_id, item_subid = get_item_id_and_subid(item_name)
        locations[symbolic_name] = {}
        locations[symbolic_name]["id"] = item_id
        locations[symbolic_name]["subid"] = item_subid
        locations[symbolic_name]["fullid"] = (item_id << 8) + item_subid
        assembler.define_byte(f"locations.{symbolic_name}.id", locations[symbolic_name]["id"])
        assembler.define_byte(f"locations.{symbolic_name}.subid", locations[symbolic_name]["subid"])
        assembler.define_word(f"locations.{symbolic_name}", locations[symbolic_name]["fullid"])

        
def define_option_constants(assembler: Z80Assembler, patch_data):
    options = patch_data["options"]

    assembler.define_byte("option.startingGroup", 0x00)
    assembler.define_byte("option.startingRoom", 0x39)

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

def text_to_binary(item_name: str) -> List[int]:
    words = item_name.split(" ")
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
        result.extend(line.encode())
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
        ) and location_name != "Rolling Ridge (Present): Bush Cave Chest":
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

def set_dungeon_warps(rom: RomData, patch_data):
    warp_matchings = patch_data["dungeon_entrances"]
    enter_values = {name: rom.read_word(dungeon["addr"]) for name, dungeon in DUNGEON_ENTRANCES.items()}
    exit_values = {name: rom.read_word(addr) for name, addr in DUNGEON_EXITS.items()}

    # Apply warp matchings expressed in the patch
    for from_name, to_name in warp_matchings.items():
        default_entrance_of_to_name = [name for name, dungeon in DUNGEON_ENTRANCES.items() if dungeon["default"] == to_name][0]
        default_exit_of_from_name = DUNGEON_ENTRANCES[from_name]["default"]
        entrance_addr = DUNGEON_ENTRANCES[from_name]["addr"]
        exit_addr = DUNGEON_EXITS[to_name]
        rom.write_word(entrance_addr, enter_values[default_entrance_of_to_name])
        rom.write_word(exit_addr, exit_values[default_exit_of_from_name])

    # Build a map dungeon => entrance (useful for essence warps)
    entrance_map = dict((v, k) for k, v in warp_matchings.items())

    # D1-D8 Essence Warps (hardcoded in one array using a unified format)
    for i in range(0, 9):
        if i == 8:
            if patch_data["options"]["linked_heros_cave"] > 0:
                i = 10
            else:
                continue
        entrance_name = f"d{i + 1}"
        if i == 5:
            entrance_name += " past"
        entrance = DUNGEON_ENTRANCES[entrance_map[entrance_name]]
        if i == 10:
            rom.write_bytes(GameboyAddress(0x0a, 0x7204).address_in_rom(), [
                entrance["group"] | 0x80,
                entrance["room"], 
                0x0e if entrance["shifted"] else 0x01, 
                entrance["position"], 
                (entrance["group"] * 0x10) + 0x03
            ])
        else:
            rom.write_bytes(0x2874f + (i * 4), [
                entrance["group"] | 0x80,
                entrance["room"],
                entrance["position"],
                0x0e if entrance["shifted"] else 0x01
            ])

#    # Change Minimap popups to indicate the randomized dungeon's name
#    for i in range(8):
#        entrance_name = f"d{i}"
#        dungeon_index = int(warp_matchings[entrance_name][1:])
#        map_tile = DUNGEON_ENTRANCES[entrance_name]["map_tile"]
#        rom.write_byte(0x???? + map_tile, 0x81 | (dungeon_index << 3))

def define_tile_replacements_table(assembler: Z80Assembler, patch_data):
    new_tiles_table = [
        0x00, 0x20, 0x00, 0x61, 0xd7, # portal in talus peaks
        0x01, 0x48, 0x00, 0x45, 0xd7, # portal south of past maku tree
        0x00, 0x37, 0x02, 0x43, 0xd7, # portal in southeast ricky/moosh nuun
        0x00, 0x6b, 0x00, 0x42, 0x3a, # removed tree in yoll graveyard
        0x00, 0x6b, 0x02, 0x42, 0xce, # not removed tree in yoll graveyard
        0x00, 0x83, 0x00, 0x43, 0xa4, # rock outside D2
        0x03, 0x0f, 0x00, 0x66, 0xf9, # water in d6 past entrance
        0x01, 0x13, 0x00, 0x61, 0xd7, # portal in symmetry city past
        0x01, 0x13, 0x00, 0x68, 0xd7, # portal in symmetry city past
        0x00, 0x25, 0x00, 0x37, 0xd7, # portal in nuun highlands
        0x05, 0xda, 0x01, 0xa4, 0xb2, # tunnel to moblin keep
        0x05, 0xda, 0x01, 0xa5, 0xb2, # cont.
        0x05, 0xda, 0x01, 0xa6, 0xb2, # cont.
        0x00, 0x24, 0x02, 0x49, 0x63, # other side of symmetry city bridge
        0x00, 0x24, 0x02, 0x59, 0x63, # cont.
        0x00, 0x24, 0x02, 0x69, 0x63, # cont.
        0x00, 0x24, 0x02, 0x79, 0x73, # cont.
        0x01, 0x2c, 0x00, 0x70, 0x69, # ledge in rolling ridge east past
        0x01, 0x2c, 0x00, 0x71, 0x06, # cont.
        0x01, 0x2c, 0x00, 0x72, 0x67, # cont.
        0x00, 0xa9, 0x00, 0x67, 0xf2, # portal sign on crescent island
        0x01, 0xa5, 0x00, 0x35, 0x48, # ledge by library past
        0x01, 0xa5, 0x00, 0x45, 0x0b, # cont.
        0x01, 0xa5, 0x00, 0x55, 0x6c, # cont.
        0x00, 0x83, 0x00, 0x44, 0xd7, # portal outside D2 present
        0x01, 0x48, 0x02, 0x31, 0xcd # past maku road: remove dirt when exiting
    ]

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
