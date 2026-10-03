import json
import os
from typing import List, TYPE_CHECKING

import settings
import Utils
from BaseClasses import ItemClassification
from settings import get_settings
from worlds.Files import APPatchExtension, APProcedurePatch, APTokenMixin, APTokenTypes

from . import Data
from . import Palettes
from .Locations import shop_location_names

if TYPE_CHECKING:
    from . import MMZero3World


# Bit positions in ZeroStatus.unlockedWeapon.
WEAPON_BITS = {"Buster": 0, "Z-Saber": 1, "Recoil Rod": 2, "Shield Boomerang": 3}


def get_base_rom_bytes() -> bytes:
    file_name = get_settings().MMZero3_settings["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    with open(file_name, "rb") as infile:
        return infile.read()


class MMZero3ProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Mega Man Zero 3"
    hash = "aa1d5eeffcd5e4577db9ee6d9b1100f9"
    patch_file_ending = ".apmmzero3"
    result_file_ending = ".gba"

    procedure = [
        ("apply_bsdiff4", ["basepatch.bsdiff4"]),
        ("apply_tokens", ["token_data.bin"]),
        ("recolor_palettes", ["palettes.json"]),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()


def encode_text(text: str, cols: int) -> bytes:
    """
    String into a series of bytes the ROM can print using the charmap.
    
    For shop's text. Anything not in Data's charmap becomes a ?.
    """
    out = bytearray()
    for letter in text[:cols]:
        if letter in Data.CHARMAP:
            out.append(Data.CHARMAP[letter])
        else:
            out.append(Data.CHARMAP["?"])

    out.append(Data.AP_SHOP_TEXT_END)
    while len(out) < cols + 1:
        out.append(0)
    return bytes(out)


def wrap_text(text: str, cols: int, lines: int) -> List[str]:
    words = []
    for word in text.split():
        while len(word) > cols:
            words.append(word[:cols])
            word = word[cols:]
        words.append(word)

    out = []
    line = ""
    for word in words:
        longer = word if line == "" else line + " " + word
        if len(longer) <= cols:
            line = longer
        else:
            out.append(line)
            line = word
    if line != "":
        out.append(line)

    if len(out) > lines:
        out = out[:lines]
        last = out[-1]
        if len(last) + 3 > cols:
            last = last[:cols - 3].rstrip()
        out[-1] = last + "..."
    return out


class MMZero3PatchExtensions(APPatchExtension):
    game = "Mega Man Zero 3"

    @staticmethod
    def recolor_palettes(caller: APProcedurePatch, rom: bytes, rolls_file: str) -> bytes:
        """Randomized level palettes"""
        rolls = json.loads(caller.get_file(rolls_file).decode("utf-8"))
        by_offset = {}
        for stage_id, preset in rolls.items():
            for offset, size in Data.STAGE_PALETTES[int(stage_id)]:
                by_offset[offset] = (size, preset)

        rom = bytearray(rom)
        for offset, (size, preset) in by_offset.items():
            rom[offset:offset + size] = Palettes.recolor(rom[offset:offset + size],
                                                          Palettes.PRESETS[preset])
        return bytes(rom)


def shop_record(name_lines: List[str], player_lines: List[str], kind: int, code: int) -> bytes:
    """
    Get data for one shop item. 68 Bytes total: 
    The name lines, the player lines, the kind byte, then padding.
    """
    cols = Data.AP_SHOP_TEXT_COLS
    out = bytearray()

    for i in range(Data.AP_SHOP_NAME_LINES):
        if i < len(name_lines):
            out += encode_text(name_lines[i], cols)
        else:
            out += encode_text("", cols)

    for i in range(Data.AP_SHOP_PLAYER_LINES):
        if i < len(player_lines):
            out += encode_text(player_lines[i], cols)
        else:
            out += encode_text("", cols)

    out.append(kind)
    while len(out) % 2 != 0:          # the item code is a u16, so it needs to start on an even byte
        out.append(0)
    out += code.to_bytes(2, "little")
    while len(out) < Data.SHOP_ITEMS_SIZE:
        out.append(0)
    return bytes(out)


def shop_item_records(world: "MMZero3World") -> bytes:
    """
    Gets all shop item information from world to place into ROM, formatting when needed.
    """
    cols = Data.AP_SHOP_TEXT_COLS
    out = bytearray()

    for slot in range(Data.SHOP_ITEMS_COUNT):
        if slot >= world.options.shop_slots.value:
            out += shop_record([], [], 0, 0)
            continue

        item = world.multiworld.get_location(shop_location_names[slot], world.player).item

        if item.advancement:
            kind = Data.AP_SHOP_KIND_PROGRESSION
        elif item.classification == ItemClassification.trap:
            kind = Data.AP_SHOP_KIND_TRAP
        else:
            kind = Data.AP_SHOP_KIND_PLAIN

        if item.player == world.player:
            kind |= Data.AP_SHOP_OWN_WORLD
            code = item.code
            player = ""
        else:
            code = 0
            player = world.multiworld.get_player_name(item.player)

        name_lines = wrap_text(item.name, cols, Data.AP_SHOP_NAME_LINES)
        player_lines = wrap_text(player, cols, Data.AP_SHOP_PLAYER_LINES)
        out += shop_record(name_lines, player_lines, kind, code)

    return bytes(out)


def write_tokens(world: "MMZero3World", patch: MMZero3ProcedurePatch) -> None:
    """Write this seed's settings over ApSeedConfig in the ROM.

    struct ApSeedConfig {
        u16 requiredDisks;
        u8  startingWeapons;
        u8  exSkillRank;
        u8  itemsanity;
        u8  exLifeSanity;
        u8  selectButton;
        u8  damageUpgrades;
        u8  cyberElves;
        u8  diskNamePopup;
        u8  infiniteLives;
        u8  finalStageRank;
    };

    Theres also gApShopPrices, one u16 per shop slot: 
    what that slot costs, or 0 for a slot this seed does not stock

    And gApShopItems, one record a slot saying what is in it.
    """
    starting_weapons = 0
    for name in world.starting_weapons:
        starting_weapons |= 1 << WEAPON_BITS[name]

    values = {
        "requiredDisks": world.options.required_secret_disks.value,
        "startingWeapons": starting_weapons,
        "exSkillRank": world.options.ex_skill_rank.value,
        "itemsanity": 1 if world.options.itemsanity.value else 0,
        "exLifeSanity": 1 if world.options.extra_life_sanity.value else 0,
        "selectButton": world.options.select_button.value,
        "damageUpgrades": 1 if world.options.weapon_damage_upgrades.value else 0,
        "cyberElves": world.options.cyber_elves.value,
        "diskNamePopup": 1 if world.options.disk_name_popup.value else 0,
        "infiniteLives": 1 if world.options.infinite_lives.value else 0,
        "finalStageRank": world.options.final_stage_rank.value,
    }

    seed_config = bytearray(Data.SEED_CONFIG_SIZE)
    for name, (offset, size) in Data.SEED_CONFIG_FIELDS.items():
        seed_config[offset:offset + size] = values[name].to_bytes(size, "little")

    patch.write_token(APTokenTypes.WRITE, Data.SEED_CONFIG_ROM_OFFSET, bytes(seed_config))

    prices = bytearray()
    for slot in range(Data.SHOP_PRICES_COUNT):
        if slot < len(world.shop_prices):
            price = world.shop_prices[slot]
        else:
            price = 0
        prices += price.to_bytes(Data.SHOP_PRICES_ELEMENT_SIZE, "little")
    patch.write_token(APTokenTypes.WRITE, Data.SHOP_PRICES_ROM_OFFSET, bytes(prices))

    patch.write_token(APTokenTypes.WRITE, Data.SHOP_ITEMS_ROM_OFFSET, shop_item_records(world))

    patch.write_file("token_data.bin", patch.get_token_binary())

    patch.write_file("palettes.json", json.dumps(world.stage_palettes).encode("utf-8"))


class MMZero3Settings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of your Mega Man Zero 3 (USA) ROM"""
        required = True
        description = "Mega Man Zero 3 (USA) ROM File"
        copy_to = "Mega Man Zero 3 (USA).gba"
        md5s = [MMZero3ProcedurePatch.hash]

    rom_file: RomFile = RomFile(RomFile.copy_to)
