from collections import defaultdict
from typing import Any

from ...common.patching.z80asm.Assembler import Z80Assembler
from ...common.patching.z80asm.Util import parse_hex_string_to_value
from ...data.Constants import (
    SEED_ITEMS,
)
from ...data.items import ITEMS_DATA
from ..Constants import (
    DEFINES,
)


def set_player_start_inventory(assembler: Z80Assembler, patch_data: dict[str, Any]) -> None:
    obtained_treasures_address = parse_hex_string_to_value(DEFINES["wObtainedTreasureFlags"])
    start_inventory_changes = defaultdict(int)

    # ###### Base changes ##############################################
    start_inventory_changes[parse_hex_string_to_value(DEFINES["wIsLinkedGame"])] = 0x00  # No linked gaming
    start_inventory_changes[parse_hex_string_to_value(DEFINES["wAnimalTutorialFlags"])] = 0xFF  # Animal vars
    # Remove the requirement to go in the screen under Sunken City tree to make Dimitri bullies appear
    start_inventory_changes[parse_hex_string_to_value(DEFINES["wDimitriState"])] = 0x20
    # Give L-3 ring box
    start_inventory_changes[0xC697] = 0x10
    start_inventory_changes[parse_hex_string_to_value(DEFINES["wRingBoxLevel"])] = 0x03

    # Starting map/compass
    if patch_data["options"]["starting_maps_compasses"]:
        dungeon_compass = parse_hex_string_to_value(DEFINES["wDungeonCompasses"])
        for i in range(dungeon_compass, dungeon_compass + 4):
            start_inventory_changes[i] = 0xFF

    start_inventory_data: dict[str, int] = patch_data["start_inventory"]
    # Handle leveled items
    if "Progressive Shield" in start_inventory_data:
        start_inventory_changes[parse_hex_string_to_value(DEFINES["wShieldLevel"])] = start_inventory_data[
            "Progressive Shield"
        ]
    bombs = 0
    if "Bombs (10)" in start_inventory_data:
        bombs += start_inventory_data["Bombs (10)"] * 0x10
    if "Bomb Upgrade" in start_inventory_data:
        max_bombchus_level = start_inventory_data["Bomb Upgrade"]
        if max_bombchus_level == 1:
            bombs = max(bombs, 0x20)
        elif max_bombchus_level == 2:
            bombs = max(bombs, 0x50)
        else:
            bombs = max(bombs, 0x99)
        start_inventory_data["Bombs (10)"] = bombs // 0x10
    if bombs > 0:
        start_inventory_changes[parse_hex_string_to_value(DEFINES["wCurrentBombs"])] = start_inventory_changes[
            parse_hex_string_to_value(DEFINES["wMaxBombs"])
        ] = min(bombs, 0x99)
        # The bomb amounts are stored in decimal
    if "Progressive Sword" in start_inventory_data:
        start_inventory_changes[0xC6AC] = start_inventory_data["Progressive Sword"]
    if "Progressive Boomerang" in start_inventory_data:
        start_inventory_changes[0xC6B1] = start_inventory_data["Progressive Boomerang"]  # Boomerang level
    if "Ricky's Flute" in start_inventory_data:
        start_inventory_changes[parse_hex_string_to_value(DEFINES["wFluteIcon"])] = 0x01  # Flute icon
        start_inventory_changes[0xC643] |= 0x80  # Ricky State
    if "Dimitri's Flute" in start_inventory_data:
        start_inventory_changes[parse_hex_string_to_value(DEFINES["wFluteIcon"])] = 0x02  # Flute icon
        start_inventory_changes[0xC644] |= 0x80  # Dimitri State
    if "Moosh's Flute" in start_inventory_data:
        start_inventory_changes[parse_hex_string_to_value(DEFINES["wFluteIcon"])] = 0x03  # Flute icon
        start_inventory_changes[0xC645] |= 0x20  # Moosh State
    if "Progressive Feather" in start_inventory_data:
        start_inventory_changes[parse_hex_string_to_value(DEFINES["wFeatherLevel"])] = start_inventory_data[
            "Progressive Feather"
        ]
    if "Switch Hook" in start_inventory_data:
        start_inventory_changes[parse_hex_string_to_value(DEFINES["wSwitchHookLevel"])] = start_inventory_data[
            "Switch Hook"
        ]
    bombchus = 0
    if "Bombchus (10)" in start_inventory_data:
        bombchus += start_inventory_data["Bombchus (10)"] * 0x10
    if "Bombchu Upgrade" in start_inventory_data:
        max_bombchus_level = start_inventory_data["Bomb Upgrade"]
        if max_bombchus_level == 1:
            bombchus = max(bombchus, 0x20)
        elif max_bombchus_level == 2:
            bombchus = max(bombchus, 0x50)
        else:
            bombchus = max(bombchus, 0x99)
        start_inventory_data["Bombchus (10)"] = bombchus // 0x10
    if bombchus > 0:
        start_inventory_changes[parse_hex_string_to_value(DEFINES["wNumBombchus"])] = start_inventory_changes[
            parse_hex_string_to_value(DEFINES["wMaxBombchus"])
        ] = min(bombchus, 0x99)
        # The bombchus amounts are stored in decimal

    seed_amount = 0
    if "Progressive Slingshot" in start_inventory_data:
        start_inventory_changes[0xC6B3] = start_inventory_data["Progressive Slingshot"]  # Slingshot level
        seed_amount = 0x20
    if "Seed Shooter" in start_inventory_data:
        seed_amount = 0x20
    if "Seed Satchel" in start_inventory_data:
        satchel_level = start_inventory_data["Seed Satchel"]
        start_inventory_changes[parse_hex_string_to_value(DEFINES["wSeedSatchelLevel"])] = satchel_level
        if satchel_level == 1:
            seed_amount = 0x20
        elif satchel_level == 2:
            seed_amount = 0x50
        else:
            seed_amount = 0x99
    if seed_amount:
        start_inventory_data[SEED_ITEMS[patch_data["options"]["default_seed"]]] = 1  # Add seeds to the start inventory

    # Inventory obtained flags
    current_inventory_index = parse_hex_string_to_value(DEFINES["wInventoryB"])
    for item, item_amount in start_inventory_data.items():
        item_id = ITEMS_DATA[item]["id"]
        item_address = obtained_treasures_address + item_id // 8
        item_mask = 0x01 << (item_id % 8)

        start_inventory_changes[item_address] |= item_mask
        if item_id < 0x20:  # items prior to 0x20 are all usable
            if item == "Biggoron's Sword":
                # Biggoron needs special care since it occupies both hands
                if current_inventory_index == parse_hex_string_to_value(DEFINES["wInventoryB"]):
                    start_inventory_changes[current_inventory_index] = start_inventory_changes[
                        current_inventory_index + 1
                    ] = item_id
                    current_inventory_index += 2
                elif current_inventory_index == parse_hex_string_to_value(DEFINES["wInventoryB"]) + 1:
                    current_inventory_index += 1
                    start_inventory_changes[current_inventory_index] = item_id
                    current_inventory_index += 1
            else:
                start_inventory_changes[current_inventory_index] = item_id  # Place the item in the inventory
                current_inventory_index += 1

        if item_id == 0x07:  # Rod of Seasons
            season = ITEMS_DATA[item]["subid"] - 2
            start_inventory_changes[0xC6B0] |= 0x01 << season
        elif item_id == 0x28:  # Rupees
            amount = int(item.split("(")[1][:-1])  # Find the value in the item name
            start_inventory_changes[0xC6A5] += amount * item_amount
        elif item_id == 0x37:  # Ore Chunks
            amount = int(item.split("(")[1][:-1])  # Find the value in the item name
            start_inventory_changes[0xC6A7] += amount * item_amount
        elif item_id == 0x30:  # Small keys
            subid = ITEMS_DATA[item]["subid"] % 0x80
            start_inventory_changes[0xC66E + subid] += item_amount
        elif item_id == 0x31:  # Boss keys
            subid = ITEMS_DATA[item]["subid"]
            start_inventory_changes[0xC67A + subid // 8] |= 0x01 << subid % 8
        elif item_id == 0x32:  # Compasses
            subid = ITEMS_DATA[item]["subid"]
            start_inventory_changes[0xC67C + subid // 8] |= 0x01 << subid % 8
        elif item_id == 0x33:  # Maps
            subid = ITEMS_DATA[item]["subid"]
            start_inventory_changes[0xC67E + subid // 8] |= 0x01 << subid % 8
        elif item_id == 0x2D:  # Rings
            subid = ITEMS_DATA[item]["subid"] - 4
            start_inventory_changes[parse_hex_string_to_value(DEFINES["wRingsObtained"]) + subid // 8] |= (
                0x01 << subid % 8
            )
        elif item_id == 0x40:  # Essences
            subid = ITEMS_DATA[item]["subid"]
            start_inventory_changes[parse_hex_string_to_value(DEFINES["wEssencesObtained"])] |= 0x01 << subid % 8
        elif 0x20 <= item_id <= 0x24:  # Seeds
            seed_address = parse_hex_string_to_value(DEFINES["wNumEmberSeeds"]) + item_id - 0x20
            start_inventory_changes[seed_address] = seed_amount

    if 0xC6A5 in start_inventory_changes:
        hex_rupee_count = parse_hex_string_to_value(f"${start_inventory_changes[0xC6A5]}")
        start_inventory_changes[0xC6A5] = hex_rupee_count % 0x100
        start_inventory_changes[0xC6A6] = hex_rupee_count // 0x100
    if 0xC6A7 in start_inventory_changes:
        hex_ore_count = parse_hex_string_to_value(f"${start_inventory_changes[0xC6A7]}")
        start_inventory_changes[0xC6A7] = hex_ore_count % 0x100
        start_inventory_changes[0xC6A8] = hex_ore_count // 0x100
    if obtained_treasures_address in start_inventory_changes:
        start_inventory_changes[obtained_treasures_address] |= 1 << 2  # Add treasure punch flag

    heart_pieces = start_inventory_data.get("Piece of Heart", 0) + start_inventory_data.get("Rare Peach Stone", 0)
    additional_hearts = start_inventory_data.get("Heart Container", 0) + heart_pieces // 4
    if additional_hearts:
        start_inventory_changes[0xC6A2] = start_inventory_changes[0xC6A3] = 12 + additional_hearts * 4
    if heart_pieces % 4:
        start_inventory_changes[0xC6A4] = heart_pieces % 4
    if "Gasha Seed" in start_inventory_data:
        start_inventory_changes[0xC6BA] = start_inventory_data["Gasha Seed"]

    # Make the list used in asm
    start_inventory = []
    for address in start_inventory_changes:
        start_inventory.append(address // 0x100)
        start_inventory.append(address % 0x100)
        start_inventory.append(start_inventory_changes[address])

    start_inventory.append(0x00)  # End of the list
    assembler.add_floating_chunk("startingInventory", start_inventory)