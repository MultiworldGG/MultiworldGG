from typing import Any

from .Constants import *
from .Util import *
from ..Options import OraclesMasterKeys, OraclesShowDungeonsWithEssence
from .RomData import RomData
from .z80asm.Assembler import Z80Assembler
from ...data.Locations import LOCATIONS_DATA


def write_chest_contents(rom: RomData, patch_data):
    """
    Chest locations are packed inside several big tables in the ROM, unlike other more specific locations.
    This puts the item described in the patch data inside each chest in the game.
    """
    locations_data = patch_data["locations"]
    for location_name, location_data in LOCATIONS_DATA.items():
        if location_data.get("collect", COLLECT_TOUCH) != COLLECT_CHEST and not location_data.get("is_chest", False) or location_name not in locations_data:
            continue
        chest_addr = rom.get_chest_addr(location_data["room"], 0x15, 0x4f6c)
        item = locations_data[location_name]
        item_id, item_subid = get_item_id_and_subid(item)
        rom.write_byte(chest_addr, item_id)
        rom.write_byte(chest_addr + 1, item_subid)


def define_compass_rooms_table(assembler: Z80Assembler, patch_data):
    table = []
    for location_name, item in patch_data["locations"].items():
        item_id, item_subid = get_item_id_and_subid(item)
        dungeon = 0xff
        if item_id == 0x30:  # Small Key or Master Key
            dungeon = item_subid
        elif item_id == 0x31:  # Boss Key
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


def define_location_constants(assembler: Z80Assembler, patch_data):
    # If "Enforce potion in shop" is enabled, put a Potion in a specific location in Horon Shop that was
    # disabled at generation time to prevent trackers from tracking it
    if patch_data["options"]["enforce_potion_in_shop"]:
        patch_data["locations"][patch_data["city_name"] + ": Shop #3"] = {"item": "Potion"}
    # If golden ore spots are not shuffled, they are still reachable nonetheless, so we need to enforce their
    # vanilla item for systems to work
    if patch_data["seasons"]:
        if not patch_data["options"]["shuffle_golden_ore_spots"]:
            from ...data.Constants import SUBROSIA_HIDDEN_DIGGING_SPOTS_LOCATIONS
            for location_name in SUBROSIA_HIDDEN_DIGGING_SPOTS_LOCATIONS:
                patch_data["locations"][location_name] = {"item": "Ore Chunks (50)"}

    # Define shop prices as constants
    for symbolic_name, price in patch_data["shop_prices"].items():
        assembler.define_byte(f"shopPrices.{symbolic_name}", RUPEE_VALUES[price])

    for location_name, location_data in LOCATIONS_DATA.items():
        if "symbolic_name" not in location_data:
            continue

        symbolic_name = location_data["symbolic_name"]
        if location_name in patch_data["locations"]:
            item = patch_data["locations"][location_name]
        else:
            # Put a fake item for disabled locations, since they are unreachable anwyway
            item = {"item": "Friendship Ring"}

        item_id, item_subid = get_item_id_and_subid(item)
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


def define_common_option_constants(assembler: Z80Assembler, patch_data):
    options = patch_data["options"]

    assembler.define_byte("option.animalCompanion", 0x0b + patch_data["options"]["animal_companion"])
    assembler.define_byte("option.defaultSeedType", 0x20 + patch_data["options"]["default_seed"])
    assembler.define_byte("option.receivedDamageModifier", options["combat_difficulty"])
    assembler.define_byte("option.openAdvanceShop", options["advance_shop"])

    assembler.define_byte("option.requiredEssences", options["required_essences"])
    assembler.define_byte("option.deterministicGashaLootCount", options["deterministic_gasha_locations"])

    if patch_data["seasons"]:
        from ...Options import OracleOfSeasonsFoolsOre
        fools_ore_damage = 3 if options["fools_ore"] == OracleOfSeasonsFoolsOre.option_balanced else 12
        assembler.define_byte("option.foolsOreDamage", (-1 * fools_ore_damage + 0x100))

    assembler.define_byte("option.keysanity_small_keys", patch_data["options"]["keysanity_small_keys"])
    keysanity = patch_data["options"]["keysanity_small_keys"] or patch_data["options"]["keysanity_boss_keys"]
    assembler.define_byte("option.customCompassChimes", 1 if keysanity else 0)

    master_keys_as_boss_keys = patch_data["options"]["master_keys"] == OraclesMasterKeys.option_all_dungeon_keys
    assembler.define_byte("option.smallKeySprite", 0x43 if master_keys_as_boss_keys else 0x42)

    if patch_data["options"]["show_dungeons_with_map"]:
        assembler.define_byte("showDungeonWithMap", 0x01)


def define_tree_sprites_common(assembler: Z80Assembler, patch_data, tree_data):
    i = 1
    for tree_name in tree_data:
        seed = patch_data["locations"][tree_name]
        if seed["item"] == "Ember Seeds":
            continue
        seed_id, _ = get_item_id_and_subid(seed)
        assembler.define_byte(f"seedTree{i}.map", tree_data[tree_name][0])
        assembler.define_byte(f"seedTree{i}.position", tree_data[tree_name][1])
        assembler.define_byte(f"seedTree{i}.gfx", seed_id - 26)
        assembler.define(f"seedTree{i}.rectangle", f"treeRect{seed_id}")
        i += 1
    if i == 5:
        # Duplicate ember, we have to blank some data
        assembler.define_byte("seedTree5.enabled", 0x0e)
        assembler.define_byte("seedTree5.map", 0xff)
        assembler.define_byte("seedTree5.position", 0)
        assembler.define_byte("seedTree5.gfx", 0)
        assembler.define_word("seedTree5.rectangle", 0)
    else:
        assembler.define_byte("seedTree5.enabled", 0x0d)


def define_essence_sparkle_constants(assembler: Z80Assembler, patch_data: dict[str, Any], dungeon_entrances: dict[str, Any]):
    from ...data.Constants import ITEM_GROUPS
    byte_array = []
    show_dungeons_with_essence = patch_data["options"]["show_dungeons_with_essence"]

    essence_pedestals = [k for k, v in LOCATIONS_DATA.items() if v.get("essence", False)]
    if show_dungeons_with_essence and not patch_data["options"]["shuffle_essences"]:
        for i, pedestal in enumerate(essence_pedestals):
            if patch_data["locations"][pedestal]["item"] not in ITEM_GROUPS["Essences"]:
                byte_array.extend([0xF0, 0x00])  # Nonexistent room, for padding
                continue

            # Find where dungeon entrance is located, and place the sparkle hint there
            dungeon = f"d{i + 1}"
            dungeon_entrance = [k for k, v in patch_data["dungeon_entrances"].items() if v == dungeon][0]
            entrance_data = dungeon_entrances[dungeon_entrance]
            byte_array.extend([entrance_data["group"], entrance_data["room"]])
    assembler.add_floating_chunk("essenceLocationsTable", byte_array)

    require_compass = show_dungeons_with_essence == OraclesShowDungeonsWithEssence.option_with_compass
    assembler.define_byte("option.essenceSparklesRequireCompass", 1 if require_compass else 0)
