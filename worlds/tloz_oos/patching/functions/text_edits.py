from typing import Any

from ...common.patching.text import normalize_text
from ...common.patching.Util import simple_hex
from ...common.patching.z80asm.Assembler import Z80Assembler
from ...data import LOCATIONS_DATA
from ...data.Constants import SEED_ITEMS
from ...generation.Hints import make_hint_texts


def process_item_name_for_shop_text(item: dict[str, str | bool]) -> str:
    if "player" in item:
        player_name = item["player"]
        if len(player_name) > 14:
            player_name = player_name[:13] + "."
        item_name = f"🟦{player_name}⬜'s 🟥"
    else:
        item_name = "🟥"
    item_name += item["item"]
    item_name = normalize_text(item_name)
    item_name += "⬜\\stop\n"
    return item_name


def make_text_data(assembler: Z80Assembler, text: dict[str, str], patch_data: dict[str, Any]) -> None:
    # Process shops
    OVERWORLD_SHOPS = [
        "Horon Village: Shop",
        "Horon Village: Member's Shop",
        "Sunken City: Syrup Shop",
        "Horon Village: Advance Shop",
    ]
    tx_indices = {
        "horonShop1": "TX_0e04",
        "horonShop2": "TX_0e03",
        "horonShop3": "TX_0e02",
        "memberShop1": "TX_0e1c",
        "memberShop2": "TX_0e1d",
        "memberShop3": "TX_0e1e",
        "syrupShop1": "TX_0d0a",
        "syrupShop2": "TX_0d01",
        "syrupShop3": "TX_0d05",
        "advanceShop1": "TX_0e22",
        "advanceShop2": "TX_0e23",
        "advanceShop3": "TX_0e25",
        "subrosianMarket1": "TX_2b00",
        "subrosianMarket2": "TX_2b01",
        "subrosianMarket3": "TX_2b05",
        "subrosianMarket4": "TX_2b06",
        "subrosianMarket5": "TX_2b10",
        "spoolSwampScrub": "TX_4509",
        "samasaCaveScrub": "TX_450b",
        "d4Scrub": "TX_450c",
        "d2Scrub": "TX_450d",
    }

    for shop_name in OVERWORLD_SHOPS:
        for i in range(1, 4):
            location_name = f"{shop_name} #{i}"
            symbolic_name = LOCATIONS_DATA[location_name]["symbolic_name"]
            if location_name not in patch_data["locations"]:
                continue
            item_text = process_item_name_for_shop_text(patch_data["locations"][location_name])
            item_text += " \\num1 Rupees\n  \\optOK \\optNo thanks\\cmd(0f)"
            text[tx_indices[symbolic_name]] = item_text

    for market_slot in range(1, 6):
        location_name = f"Subrosia: Market #{market_slot}"
        symbolic_name = LOCATIONS_DATA[location_name]["symbolic_name"]
        if location_name not in patch_data["locations"]:
            continue
        item_text = process_item_name_for_shop_text(patch_data["locations"][location_name])
        if market_slot == 1:
            item_text += "I'll trade for\n🟥Star-Shaped Ore⬜.\n\\jump(0b)"
        else:
            item_text += "I'll trade for\n🟥\\num1 Ore Chunks⬜.\n\\jump(0b)"
        text[tx_indices[symbolic_name]] = item_text

    BUSINESS_SCRUBS = [
        "Spool Swamp: Business Scrub",
        "Samasa Desert: Business Scrub",
        "Snake's Remains: Business Scrub",
        "Dancing Dragon Dungeon (1F): Business Scrub",
    ]
    for location_name in BUSINESS_SCRUBS:
        symbolic_name = LOCATIONS_DATA[location_name]["symbolic_name"]
        if location_name not in patch_data["locations"]:
            continue
        # Scrub string asking the player if they want to buy the item
        item_text = (
            "\\sfx(c6)Greetings!\n"
            + process_item_name_for_shop_text(patch_data["locations"][location_name])
            + f"for 🟩{patch_data['shop_prices'][symbolic_name]} Rupees⬜\n"
            "  \\optOK \\optNo thanks"
        )
        text[tx_indices[symbolic_name]] = item_text

    # Cross items
    assembler.define_byte("text.hook1.treasure", 0x3B)
    assembler.define_byte("text.hook2.treasure", 0x51)
    assembler.define_byte("text.cane.treasure", 0x53)
    assembler.define_byte("text.shooter.treasure", 0x54)

    assembler.define_byte("text.hook1.inventory", 0x1E)
    assembler.define_byte("text.hook2.inventory", 0x17)
    assembler.define_byte("text.cane.inventory", 0x1D)
    assembler.define_byte("text.shooter.inventory", 0x2E)

    # Default satchel seed
    seed_name = SEED_ITEMS[patch_data["options"]["default_seed"]].replace(" ", "\n")
    text["TX_002d"] = text["TX_002d"].replace("Ember\nSeeds", seed_name)

    # Misc
    if patch_data["options"]["rosa_quick_unlock"]:
        text["TX_2904"] = "Since you're so\nnice, I unlocked\nall the doors\nhere for you."

    text["TX_3e1b"] = (
        "You've broken\n🟩\\num1 signs⬜!\n"
        "You'd better not\n"
        "break more than\n"
        f"🟩{patch_data['options']['sign_guy_requirement']}⬜"
        ", or else..."
    )

    # Inform the player of how many gashas are good
    wife_text_index = text["TX_3101"].index("The place")
    num_seeds = patch_data["options"]["deterministic_gasha_locations"]
    if num_seeds == 0:
        seed_text = "nuts will not\ncontain anything\nuseful."
    elif num_seeds == 16:
        seed_text = "every nut can\nhold something\nuseful."
    else:
        seed_text = f"only your first\n🟩{num_seeds}⬜ nuts can\ncontain anything\nuseful."
    text["TX_3101"] = text["TX_3101"][:wife_text_index] + "\\stop\nYou should know\n" + seed_text

    # Golden beasts
    golden_beasts_requirement = patch_data["options"]["golden_beasts_requirement"]
    if golden_beasts_requirement == 0:
        # Just a funny text for killing no golden beasts
        golden_beast_reward_text = text["TX_1f05"]
        post_congratulation_index = golden_beast_reward_text.index("Sir")
        text["TX_1f04"] = ""
        text["TX_1f05"] = "You did nothing!\nTruly, " + golden_beast_reward_text[post_congratulation_index:]
    elif golden_beasts_requirement < 4:
        number = ["one", "two", "three"][golden_beasts_requirement - 1]
        text["TX_1f04"] = text["TX_1f04"].replace("the four", number)
        text["TX_1f05"] = text["TX_1f05"].replace("all four", number)
        if golden_beasts_requirement == 1:
            text["TX_1f04"] = text["TX_1f04"].replace("beasts", "beast")
            text["TX_1f05"] = text["TX_1f05"].replace("beasts", "beast")

    # Maku tree sign
    essence_count = patch_data["options"]["required_essences"]
    text["TX_2e00"] = f"Find 🟥{essence_count} essence{'s' if essence_count != 1 else ''}⬜\nto get the seed!"

    # Tarm ruins sign
    jewel_count = patch_data["options"]["tarm_gate_required_jewels"]
    text["TX_2e12"] = f"Bring 🟩{jewel_count}⬜ jewel{'s' if jewel_count != 1 else ''}\nfor the door\nto open."

    # Tree house old man
    essence_count = patch_data["options"]["treehouse_old_man_requirement"]
    text["TX_3601"] = text["TX_3601"].replace(
        "knows many\n🟥essences⬜...", f"has 🟥{essence_count} essence{'s' if essence_count != 1 else ''}⬜!"
    )

    # With quick rosa, the escort code is disabled
    if patch_data["options"]["rosa_quick_unlock"]:
        text["TX_2906"] = normalize_text("Not me. Maybe ask someone else?")

    make_hint_texts(text, patch_data)


def define_dungeon_items_text_constants(texts: dict[str, str], patch_data: dict[str, Any]) -> None:
    base_id = 0x73
    for i in range(10):
        if i == 0:
            dungeon_precision = " for\nHero's Cave"
        elif i == 9:
            dungeon_precision = " for\nLinked Hero's\nCave"
        else:
            dungeon_precision = f" for\nDungeon {i}"

        # ###### Small keys ##############################################
        small_key_text = "You found a\n🟥"
        if patch_data["options"]["master_keys"]:
            small_key_text += "Master Key"
        else:
            small_key_text += "Small Key"
        if patch_data["options"]["keysanity_small_keys"]:
            small_key_text += dungeon_precision
        small_key_text += "⬜!"
        texts[f"TX_00{simple_hex(base_id + i)}"] = small_key_text

        # Hero's Cave only has Small Keys, so skip other texts
        if i == 0 or i == 9:
            continue

        # ###### Boss keys ##############################################
        boss_key_text = "You found the\n🟥Boss Key"
        if patch_data["options"]["keysanity_boss_keys"]:
            boss_key_text += dungeon_precision
        boss_key_text += "⬜!"
        texts[f"TX_00{simple_hex(base_id + i + 9)}"] = boss_key_text

        # ###### Dungeon maps ##############################################
        dungeon_map_text = "You found the\n🟥"
        if patch_data["options"]["keysanity_maps_compasses"]:
            dungeon_map_text += "Map"
            dungeon_map_text += dungeon_precision
        else:
            dungeon_map_text += "Dungeon Map"
        dungeon_map_text += "⬜!"
        texts[f"TX_00{simple_hex(base_id + i + 17)}"] = dungeon_map_text

        # ###### Compasses ##############################################
        compasses_text = "You found the\n🟥Compass"
        if patch_data["options"]["keysanity_maps_compasses"]:
            compasses_text += dungeon_precision
        compasses_text += "⬜!"
        texts[f"TX_00{simple_hex(base_id + i + 25)}"] = compasses_text

    if patch_data["options"]["master_keys"]:
        texts["TX_001a"] = texts["TX_001a"].replace("Small", "Master")
