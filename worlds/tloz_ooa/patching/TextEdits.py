from typing import Any, cast

from settings import get_settings
from ..common.patching.text import normalize_text
from ..common.patching.Util import simple_hex
from ..common.patching.z80asm.Assembler import Z80Assembler
from ..data.Constants import DUNGEON_NAMES_FOR_TXT
from ..data.Locations import LOCATIONS_DATA
from ..data.Hints import *
import random

# -----------------------------------------------------------------------------------------------------
def process_item_name_for_shop_text(item: str) -> str:
    item_name = "🟥"
    item_name += item
    item_name = normalize_text(item_name)
    item_name += "⬜\\stop\n"
    return item_name

# -----------------------------------------------------------------------------------------------------
def mahe_shop_text(text: dict[str, str], patch_data: dict[str, Any]):
    overworld_shops = [
        "Lynna City: Shop",
        "Lynna City: Hidden Shop",
        "Yoll Graveyard: Syrup Shop",
        "Lynna Village: Advance Shop",
    ]
    
    shop_tx_indices = {
        "lynnaShop1":"TX_0101",
        "lynnaShop2":"TX_0102",
        "lynnaShop3":"TX_0103",
        "advanceShop1":"TX_0113",
        "advanceShop2":"TX_0118",
        "advanceShop3":"TX_0e24",
        "syrupShop1":"TX_0114",
        "syrupShop2":"TX_0117",
        "syrupShop3":"TX_0125",
        "hiddenShop1":"TX_0e09",
        "hiddenShop2":"TX_012a",
        "hiddenShop3":"TX_0131",

        "tokayMarket1":"TX_0a2a",
        "tokayMarket2":"TX_0a31",
    }

    #General Shops
    for shop_name in overworld_shops:
        for i in range(1, 4):
            location_name = f"{shop_name} Item #{i}"
            symbolic_name = LOCATIONS_DATA[location_name]["symbolic_name"]
            if location_name not in patch_data["locations"]:
                continue
            item_text = process_item_name_for_shop_text(patch_data["locations"][location_name])
            item_text += " \\num1 Rupees\n  \\optOK \\optNo thanks\\cmd(0f)"
            text[shop_tx_indices[symbolic_name]] = item_text

    #Tokay Market
    shop_name = "Crescent Island (Past): Market"
    for i in range(1, 3):
        location_name = f"{shop_name} Item #{i}"
        symbolic_name = LOCATIONS_DATA[location_name]["symbolic_name"]
        text_bytes = []
        if location_name not in patch_data["locations"]:
            continue
        item_text = process_item_name_for_shop_text(patch_data["locations"][location_name])
        if i == 1:
            item_text += " 10 Mystery Seed\n  \\optOK \\optNo thanks\\cmd(0f)"
        else:
            item_text += " 10 Scent Seed\n  \\optOK \\optNo thanks\\cmd(0f)"
        text[shop_tx_indices[symbolic_name]] = item_text

# ====================================================================================================
def get_region_hint_text(region_name: str, region_category: str) -> str:
    region_name = f"🟦{region_name}⬜"
    hint_text = "Did you know? "
    if region_category == "Foolish":
        hint_text += f"It is foolish to search {region_name}."
    elif region_category == "Golden":
        hint_text += f"Everything in {region_name} is precious!"
    else:
        hint_text += f"There are 🟩{region_category}⬜ precious treasures in {region_name}."
    return normalize_text(hint_text)

# -----------------------------------------------------------------------------------------------------
def get_random_joke_text(owl_id: int) -> tuple[str, str]:
    match random.randrange(6):
        case 0:
            location = [
                "Crown Dungeon",
                "Wing Dungeon",
                "Ancient Tomb",
                "Wing Dungeon",
                "Talus Peak",
                "Deku Forest",
                "Wing Dungeon",
                "Mermaid's Cave",
                "Mermaid's Cave",
                "Ancient Tomb",
                "Mermaid's Cave",
                "Moonlit Grotto",
                "Moonlit Grotto",
                #"Black Tower"
                "Western Rolling Ridge",
                "Jabu-Jabu's Belly",
                "Jabu-Jabu's Belly",
                "Jabu-Jabu's Belly",
            ][owl_id]
            return "\\link_name", location
        case 1:
            return "Ganon", "The Island of Koridai"
        case 2:
            return "Princess Zelda", "Another Castle"
        case 3:
            return "Maku Tree", "Lynna City"
        case 4:
            return "Ralph", "a hurry"
        case _:
            return "Maple", "the airs"

# -----------------------------------------------------------------------------------------------------
def make_hint_texts(texts: dict[str, str], patch_data) -> None:
    region_hints = patch_data["region_hints"]
    if len(region_hints):
        i = 0
        for region, category in region_hints:
            texts[KNOW_IT_ALL_BIRDS_TX[i]] = get_region_hint_text(region, category)
            i += 1

    item_hints = patch_data["item_hints"]
    if len(item_hints):
        for i in range(0x00, 0x1c):
            texts[f"TX_39{simple_hex(i)}"] = ""

        i = 0
        for hint in item_hints:
            if hint is None:
                item, location = get_random_joke_text(i)
            else:
                item, location, player = hint
                if player:
                    location = f"{player}'s {location}"
            text = f"They say that 🟥{item}⬜ can be found in 🟦{location}"
            text = normalize_text(text)

            texts[OWL_STATUE_TX[i]] = text
            i += 1

# ====================================================================================================
def make_dungeon_item_texts(texts: dict[str, str], patch_data) -> None:
    
    dungeon_obj_tx_indices = {
        "smallKeyD0":"TX_5a00",
        "smallKeyD1":"TX_5a01",
        "smallKeyD2":"TX_5a02",
        "smallKeyD3":"TX_5a03",
        "smallKeyD4":"TX_5a04",
        "smallKeyD5":"TX_5a05",
        "smallKeyD6Present":"TX_5a06",
        "smallKeyD7":"TX_5a07",
        "smallKeyD8":"TX_5a08",
        "smallKeyD11":"TX_5a09",
        "smallKeyD6Past":"TX_5a0a",
        "bossKeyD1":"TX_5a0b",
        "bossKeyD2":"TX_5a0c",
        "bossKeyD3":"TX_5a0d",
        "bossKeyD4":"TX_5a0e",
        "bossKeyD5":"TX_5a0f",
        "bossKeyD6":"TX_5a10",
        "bossKeyD7":"TX_5a11",
        "bossKeyD8":"TX_5a12",
        "dungeonMapD1":"TX_5a13",
        "dungeonMapD2":"TX_5a14",
        "dungeonMapD3":"TX_5a15",
        "dungeonMapD4":"TX_5a16",
        "dungeonMapD5":"TX_5a17",
        "dungeonMapD6Present":"TX_5a18",
        "dungeonMapD7":"TX_5a19",
        "dungeonMapD8":"TX_5a1a",
        "dungeonMapD6Past":"TX_5a1b",
        "compassD1":"TX_5a1c",
        "compassD2":"TX_5a1d",
        "compassD3":"TX_5a1e",
        "compassD4":"TX_5a1f",
        "compassD5":"TX_5a20",
        "compassD6Present":"TX_5a21",
        "compassD7":"TX_5a22",
        "compassD8":"TX_5a23",
        "compassD6Past":"TX_5a24",
    }

    for i in range(0, 11): # Maku Path and Hero's Cave has no map, no compass, no boss key, and the unique small key use the default text. 
        # " for\nDungeon X"
        trueI = i if i != 9 else 6
        if trueI == 10:
            trueI = 11
        dungeon_precision = " for\n"
        dungeon_tag = f"D{trueI}"
        dungeon_precision += (f"{DUNGEON_NAMES_FOR_TXT[trueI]}({dungeon_tag})" if get_settings().tloz_ooa_options["simplify_dungeon_precision_text"] else (
            f"Dungeon {dungeon_tag[1:]}"
        ))
        dungeon_precisionForBossKey = f"{dungeon_precision}"

        if i == 6:
            #\n(present)
            dungeon_precision += " (present)"
            dungeon_tag += "Present"
        elif i == 9:
            #\n(past)
            dungeon_precision += " (past)"
            dungeon_tag += "Past"


        # ###### Small keys ##############################################
        # "You found a\n\color(RED)"
        small_key_text = "You found a\n🟥"
        if patch_data["options"]["master_keys"]:
            # "Master Key"
            small_key_text += "Master Key"
        else:
            # "Small Key"
            small_key_text += "Small Key"
        if patch_data["options"]["keysanity_small_keys"]:
            small_key_text += dungeon_precision
        small_key_text += "⬜!" 
        texts[dungeon_obj_tx_indices[f"smallKey{dungeon_tag}"]] = small_key_text

        # Maku Path & Hero Cave only has Small Keys, so skip other texts
        if i == 0 or i == 10:
            continue

        # ###### Boss keys ##############################################
        # "You found the\n\color(RED)Boss Key"
        if i < 9:
            boss_key_text = "You found the\n🟥Boss Key"
            if patch_data["options"]["keysanity_boss_keys"]:
                boss_key_text += dungeon_precisionForBossKey
            texts[dungeon_obj_tx_indices[f"bossKeyD{trueI}"]] = boss_key_text

        # ###### Dungeon maps ##############################################
        # "You found the\n\color(RED)"
        dungeon_map_text = "You found the\n🟥Dungeon Map"
        if patch_data["options"]["keysanity_maps_compasses"]:
            dungeon_map_text += dungeon_precision
        dungeon_map_text += "⬜!" 
        texts[dungeon_obj_tx_indices[f"dungeonMap{dungeon_tag}"]] = dungeon_map_text

        # ###### Compasses ##############################################
        # "You found the\n\color(RED)Compass"
        compasses_text = "You found the\n🟥Compass"
        if patch_data["options"]["keysanity_maps_compasses"]:
            compasses_text += dungeon_precision
        compasses_text += "⬜!" 
        texts[dungeon_obj_tx_indices[f"compass{dungeon_tag}"]] = compasses_text
    return

# ====================================================================================================
def make_text_data(assembler: Z80Assembler, text: dict[str, str], patch_data: dict[str, Any]) -> None:
    mahe_shop_text(text, patch_data)
    make_hint_texts(text, patch_data)
    make_dungeon_item_texts(text, patch_data)

    # Maku road Sign Replacement
    options = patch_data["options"]
    requiredEssences = options["required_essences"]
    requiredSlates = options["required_slates"]

    item_text = f"You need 🟩{requiredEssences}⬜\nessences to get\nthe Maku Seed\\stop\n"
    item_text += f"You need 🟩{requiredSlates}⬜\nslates to open\nD8 basement"
    text["TX_2e0d"] = item_text

    text["TX_05b1"] = "Come back when\nyou beat that\nminigame, kid!"

    
