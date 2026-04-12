import json
import struct
import math
import sys

import logging
from typing import TYPE_CHECKING, List
from Utils import home_path, open_filename, messagebox
from settings import get_settings
from worlds.AutoWorld import World
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes, APPatchExtension
from BaseClasses import Item, ItemClassification
from .ErrorRecalc import ErrorRecalculator
from .Items import tile_id_offset, relic_id_to_name, items, weapon1, shield, armor, helmet, cloak, accessory, id_to_item
from .Locations import locations
from .Enemies import enemy_dict, enemy_stats_list, enemy_atk_type_list, enemy_weak_type_list
from .data.Constants import (RELIC_NAMES, SLOT, slots, equip_id_offset, equip_inv_id_offset, CURRENT_VERSION,
                             faerie_scroll_force_addresses, shop_item_data, start_room_data, music, music_by_area)
from .data.io_items import io_items, tile_filter, io_item_name


from .data.Zones import zones, ZONE
import hashlib
import os
import subprocess

if TYPE_CHECKING:
    from . import SotnWorld

USHASH = "acbb3a2e4a8f865f363dc06df147afa2"
AUDIOHASH = "8f4b1df20c0173f7c2e6a30bd3109ac8"
logger = logging.getLogger("Client")


# Thanks lil David from AP discord for the info on APProcedurePatch
class SotnProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Symphony of the Night"
    hash = USHASH
    patch_file_ending = ".apsotn"
    result_file_ending = ".cue"

    procedure = [
        ("apply_tokens", ["token_data.bin"]),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        with open(get_settings().sotn_settings.rom_file, "rb") as infile:
            return bytes(infile.read())

    def patch(self, target: str) -> None:
        error_message = ""
        try:
            options = json.loads(self.get_file("options.json"))
            gen_version = options["version"]
            if gen_version != CURRENT_VERSION:
                error_message = f"Version mismatch. Gen: {gen_version} - Cur: {CURRENT_VERSION}"
        except KeyError:
            error_message = f"Could not find version on option.json! Generated version too old?"
        except:
            error_message = "Something went really wrong!!!"

        if len(error_message):
            messagebox("Error", error_message, error=True)
            sys.exit()

        file_name = target[:-4]
        if os.path.exists(file_name + ".bin") and os.path.exists(file_name + ".cue"):
            logger.info("Patched ROM + CUE already exist!")
            audio_name = target[0:target.rfind('/') + 1]
            audio_name += "Castlevania - Symphony of the Night (USA) (Track 2).bin"
            if os.path.exists(audio_name):
                logger.info("Track 2 already exist")
            else:
                logger.info("Copying track 2")
                audio_rom = bytearray(get_base_rom_bytes(audio=True))
                with open(audio_name, "wb") as stream:
                    stream.write(audio_rom)
            return

        super().patch(target)

        os.rename(target, file_name + ".bin")

        audio_name = target[0:target.rfind('/') + 1]
        audio_name += "Castlevania - Symphony of the Night (USA) (Track 2).bin"
        if os.path.exists(audio_name):
            logger.info("Track 2 already exist")
        else:
            logger.info("Copying track 2")
            audio_rom = bytearray(get_base_rom_bytes(audio=True))
            with open(audio_name, "wb") as stream:
                stream.write(audio_rom)

        track1_name = target[target.rfind('/') + 1:-4]

        cue_file = f'FILE "{track1_name}.bin" BINARY\n  TRACK 01 MODE2/2352\n\tINDEX 01 00:00:00\n'
        cue_file += f'FILE "Castlevania - Symphony of the Night (USA) (Track 2).bin" BINARY\n  TRACK 02 AUDIO\n'
        cue_file += f'\tINDEX 00 00:00:00\n\tINDEX 01 00:02:00'

        with open(file_name + ".cue", 'wb') as outfile:
            outfile.write(bytes(cue_file, 'utf-8'))

        # Apply Error Recalculation
        error_recalculator = ErrorRecalculator(calculate_form_2_edc=False)
        stats = error_recalculator.recalc(target_file=file_name + ".bin", base_file=get_settings().sotn_settings.rom_file)
        print(f"{stats.identical_sectors} identical sectors out of {stats.total_sectors()}, {stats.recalc_sectors} sectors recalculated")
        print(f"{stats.edc_blocks_computed} EDC blocks computed, {stats.ecc_blocks_generated} ECC blocks generated")


class SotnPatchExtension(APPatchExtension):
    game = "Symphony of the Night"


def apply_acessibility_patches(patch: SotnProcedurePatch):
    # Researched by MottZilla.
    # Patch Clock Room cutscene 0x03ca90
    patch.write_token(APTokenTypes.WRITE, 0x0aea9c, struct.pack("<B", 0x40))
    # Patch Alchemy Laboratory cutscene
    patch.write_token(APTokenTypes.WRITE, 0x054f0f44 + 2, (0x1000).to_bytes(2, "little"))
    # Power of Sire flashing
    patch.write_token(APTokenTypes.WRITE, 0x00136580, (0x03e00008).to_bytes(4, "little"))
    # Clock Tower puzzle gate
    patch.write_token(APTokenTypes.WRITE, 0x05574dee, struct.pack("<B", 0x80))
    patch.write_token(APTokenTypes.WRITE, 0x055a110c, struct.pack("<B", 0xe0))
    # Olrox death
    patch.write_token(APTokenTypes.WRITE, 0x05fe6914, struct.pack("<B", 0x80))
    # Scylla door
    patch.write_token(APTokenTypes.WRITE, 0x061ce8ec, struct.pack("<B", 0xce))
    patch.write_token(APTokenTypes.WRITE, 0x061cb734, (0x304200fe).to_bytes(4, "little"))
    # Minotaur & Werewolf
    offset = 0x0613a640
    patch.write_token(APTokenTypes.WRITE, 0x061294dc, (0x0806d732).to_bytes(4, "little"))
    patch.write_token(APTokenTypes.WRITE, offset, (0x3c028007).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x34423404).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x34030005).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x90420000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x1043000b).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x34030018).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x10430008).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x34030009).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x10430005).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x34030019).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x10430002).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x0806d747).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x34020001).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0xac82002c).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x3c028007).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x944233da).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x08069bc3).to_bytes(4, "little"))
    # Softlock when using gold & silver ring
    offset = 0x492df64
    patch.write_token(APTokenTypes.WRITE, offset, (0xa0202ee8).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x080735cc).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    patch.write_token(APTokenTypes.WRITE, 0x4952454, (0x0806b647).to_bytes(4, "little"))
    patch.write_token(APTokenTypes.WRITE, 0x4952474, (0x0806b647).to_bytes(4, "little"))
    # Always have Clear Game Status. - MottZilla
    patch.write_token(APTokenTypes.WRITE, 0x04397122, struct.pack("<B", 0x22))


def rom_offset(zone: dict, address: int) -> int:
    return zone["pos"] + address + math.floor(address / 0x800) * 0x130


def item_slots(item: dict) -> list:
    if item["type"] in ["WEAPON1", "WEAPON2", "SHIELD", "USABLE"]:
        return [slots[SLOT["LEFT_HAND"]], slots[SLOT["RIGHT_HAND"]]]
    elif item["type"] == "HELMET":
        return [slots[SLOT["HEAD"]]]
    elif item["type"] == "ARMOR":
        return [slots[SLOT["BODY"]]]
    elif item["type"] == "CLOAK":
        return [slots[SLOT["CLOAK"]]]
    elif item["type"] == "ACCESSORY":
        return [slots[SLOT["OTHER"]], slots[SLOT["OTHER2"]]]


def shop_item_type(item: dict) -> int:
    if item["type"] == "HELMET":
        return 0x01
    elif item["type"] == "ARMOR":
        return 0x02
    elif item["type"] == "CLOAK":
        return 0x03
    elif item["type"] == "ACCESSORY":
        return 0x04
    else:
        return 0x00


def tile_value(item: dict, tile: dict) -> int:
    item_id = item["id"]

    if "no_offset" in tile:
        return item_id

    if "shop" in tile:
        if item["type"] in ["HELMET", "ARMOR", "CLOAK", "ACCESSORY"]:
            item_id += equip_id_offset
    else:
        if item["type"] == "RELIC":
            item_id -= 300
        elif item["type"] == "POWERUP":
            item_id -= 400
        elif item["type"] not in ["HEART", "GOLD", "SUBWEAPON"]:
            item_id += tile_id_offset

    return item_id


def write_entity(entity: dict, opts: dict, patch: SotnProcedurePatch) -> None:
    for index, e in enumerate(entity["entities"]):
        zone = zones[entity["zones"][index >> 1]]
        if "x" in opts:
            address = rom_offset(zone, e + 0x00)
            patch.write_token(APTokenTypes.WRITE, address, opts["x"].to_bytes(2, "little"))
        if "y" in opts:
            address = rom_offset(zone, e + 0x02)
            patch.write_token(APTokenTypes.WRITE, address, opts["y"].to_bytes(2, "little"))
        if "id" in opts:
            address = rom_offset(zone, e + 0x04)
            patch.write_token(APTokenTypes.WRITE, address, opts["id"].to_bytes(2, "little"))
        if "slots" in opts:
            address = rom_offset(zone, e + 0x06)
            patch.write_token(APTokenTypes.WRITE, address, opts["slots"][index].to_bytes(2, "little"))
        if "state" in opts:
            address = rom_offset(zone, e + 0x08)
            patch.write_token(APTokenTypes.WRITE, address, opts["state"].to_bytes(2, "little"))


def write_tile_id(zones_list: list, index: int, item_id: int, patch: SotnProcedurePatch) -> None:
    for z in zones_list:
        zone = zones[z]
        addr = rom_offset(zone, zone["items"] + 0x02 * index)
        patch.write_token(APTokenTypes.WRITE, addr, item_id.to_bytes(2, "little"))


def replace_holy_glasses_with_relic(instructions: list, relic: int, patch: SotnProcedurePatch):
    zone = zones[ZONE["CEN"]]
    # Erase Holy glasses
    patch.write_token(APTokenTypes.WRITE,
                      instructions[0]["addresses"][0],
                      instructions[0]["instruction"].to_bytes(4, "little"))
    # Replace entity with relic
    for addr in [0x1328, 0x13be]:
        offset = rom_offset(zone, addr + 0x00)
        patch.write_token(APTokenTypes.WRITE, offset, (0x0180).to_bytes(2, "little"))
        offset = rom_offset(zone, addr + 0x02)
        patch.write_token(APTokenTypes.WRITE, offset, (0x022c).to_bytes(2, "little"))
        offset = rom_offset(zone, addr + 0x04)
        patch.write_token(APTokenTypes.WRITE, offset, (0x000b).to_bytes(2, "little"))
        offset = rom_offset(zone, addr + 0x06)
        patch.write_token(APTokenTypes.WRITE, offset, (0x0000).to_bytes(2, "little"))
        offset = rom_offset(zone, addr + 0x08)
        patch.write_token(APTokenTypes.WRITE, offset, relic.to_bytes(2, "little"))


def replace_shop_relic_with_relic(jewel_address: int, relic_id: int, patch: SotnProcedurePatch):
    relic_name_address = 0x047d5650
    relic_id_address = 0x047dbde0
    relic_id_offset = 0x64
    # Write relic id
    patch.write_token(APTokenTypes.WRITE,
                      jewel_address,
                      struct.pack("<B", relic_id))
    # Fix shop menu check
    patch.write_token(APTokenTypes.WRITE,
                      relic_id_address,
                      struct.pack("<B", (relic_id + relic_id_offset)))
    # Change shop menu name
    relic_name = relic_id_to_name[relic_id + 300]
    ord_string = [0 for _ in range(16)]
    for i in range(16):
        if i < len(relic_name):
            if ord(relic_name[i]) == ' ':
                ord_string[i] = ord(' ')
            else:
                ord_string[i] = ord(relic_name[i]) - 0x20
        elif i == len(relic_name):
            ord_string[i] = 0xff
        else:
            ord_string[i] = 0x00

    ord_string[len(relic_name) + 0] = 0xff
    ord_string[len(relic_name) + 1] = 0x00

    for ch in ord_string:
        patch.write_token(APTokenTypes.WRITE, relic_name_address, struct.pack("<B", ch))
        relic_name_address += 1


def replace_shop_relic_with_item(item: dict, patch: SotnProcedurePatch):
    item_id = item["id"]
    zone = zones[ZONE["LIB"]]
    i_slots = item_slots(item)
    # Write item type
    i_type = shop_item_type(item)
    patch.write_token(APTokenTypes.WRITE, rom_offset(zone, 0x134c), struct.pack("<B", i_type))
    # Write item id
    i_tile = tile_value(item, {"shop": True})
    patch.write_token(APTokenTypes.WRITE, rom_offset(zone, 0x134e), i_tile.to_bytes(2, "little"))
    patch.write_token(APTokenTypes.WRITE, rom_offset(zone, 0x14d4), i_tile.to_bytes(2, "little"))
    # Write short item type
    offset = rom_offset(zone, 0x032b80)
    patch.write_token(APTokenTypes.WRITE, offset, (0x96220000).to_bytes(4, "little"))  # lhu v0, 0x0000 (s1)
    # Load byte item type
    offset = rom_offset(zone, 0x033050)
    patch.write_token(APTokenTypes.WRITE, offset, (0x90a30000).to_bytes(4, "little"))  # lbu v1, 0x0000 (al)
    offset = rom_offset(zone, 0x033638)
    patch.write_token(APTokenTypes.WRITE, offset, (0x90234364).to_bytes(4, "little"))  # lbu v1, 0x4364 (at)
    offset = rom_offset(zone, 0x03369c)
    patch.write_token(APTokenTypes.WRITE, offset, (0x90224364).to_bytes(4, "little"))  # lbu v0, 0x4364 (at)
    offset = rom_offset(zone, 0x033730)
    patch.write_token(APTokenTypes.WRITE, offset, (0x90234364).to_bytes(4, "little"))  # lbu v1, 0x4364 (at)
    offset = rom_offset(zone, 0x03431c)
    patch.write_token(APTokenTypes.WRITE, offset, (0x92620000).to_bytes(4, "little"))  # lbu v0, 0x0000 (s3)
    offset = rom_offset(zone, 0x0343c0)
    patch.write_token(APTokenTypes.WRITE, offset, (0x92630000).to_bytes(4, "little"))  # lbu v1, 0x0000 (s3)
    offset = rom_offset(zone, 0x034f10)
    patch.write_token(APTokenTypes.WRITE, offset, (0x90430000).to_bytes(4, "little"))  # lbu v1, 0x0000 (v0)
    offset = rom_offset(zone, 0x0359f4)
    patch.write_token(APTokenTypes.WRITE, offset, (0x92a30000).to_bytes(4, "little"))  # lbu v1, 0x0000 (s5)
    # Load relic icon
    offset = rom_offset(zone, 0x034fb4)
    patch.write_token(APTokenTypes.WRITE, offset, (0x00801021).to_bytes(4, "little"))  # addu v0, a0, r0
    # Load relic id for purchase
    offset = rom_offset(zone, 0x033750)
    patch.write_token(APTokenTypes.WRITE, offset, (0x00402021).to_bytes(4, "little"))  # addu a0, v0, r0
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    # Entry point
    offset = rom_offset(zone, 0x032b08)
    patch.write_token(APTokenTypes.WRITE, offset, (0x08075180).to_bytes(4, "little"))  # j 0x801d4600
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    # Equipped check
    offset = rom_offset(zone, 0x054600)
    # ori v1, r0, id
    # patch.write_token(APTokenTypes.WRITE, offset, (0x34030000 + item_id + equip_id_offset).to_bytes(4, "little"))
    # Remove so the item is always on shop
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    offset += 4
    for i, slot in enumerate(i_slots):
        # lui v0, 0x8009
        patch.write_token(APTokenTypes.WRITE, offset, (0x3c028000 + (slot >> 16)).to_bytes(4, "little"))
        offset += 4
        # lbu v0, slot (v0)
        patch.write_token(APTokenTypes.WRITE, offset, (0x90420000 + (slot & 0xffff)).to_bytes(4, "little"))
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
        offset += 4
        next_slot = 4 + 5 * (len(i_slots) - i - 1)
        # beq v0, v1, pc + next
        patch.write_token(APTokenTypes.WRITE, offset, (0x10430000 + next_slot).to_bytes(4, "little"))
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
        offset += 4
    # Inventory check
    # patch.write_token(APTokenTypes.WRITE, offset, (0x3c028009).to_bytes(4, "little"))  # lui v0, 0x8009
    # Remove so the item is always on shop
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    offset += 4
    # lbu v0, 0x798a + id (v0)
    patch.write_token(APTokenTypes.WRITE, offset, (0x90420000 + item_id + equip_inv_id_offset).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    offset += 4
    # Return
    patch.write_token(APTokenTypes.WRITE, offset, (0x0806cac7).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    # Entry point
    offset = rom_offset(zone, 0x033050)
    patch.write_token(APTokenTypes.WRITE, offset, (0x08075190).to_bytes(4, "little"))  # j 0x801d4640
    # Load base address
    offset = rom_offset(zone, 0x054640)
    patch.write_token(APTokenTypes.WRITE, offset, (0x90a20001).to_bytes(4, "little"))  # lbu v0, 0x0001 (a1)
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x2c4200ff).to_bytes(4, "little"))  # sltiu v0, v0, 0x00ff
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x14400003).to_bytes(4, "little"))  # bne v0, r0, pc + 0x10
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x90a30000).to_bytes(4, "little"))  # lbu v1, 0x0000 (a1)
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x34030005).to_bytes(4, "little"))  # ori v1, r0, 0x0005
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x0806cc16).to_bytes(4, "little"))  # j 0x801b3058
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    # Patch checker
    offset = rom_offset(zone, 0x03317c)
    patch.write_token(APTokenTypes.WRITE, offset, (0x080751a0).to_bytes(4, "little"))  # j 0x801d4680
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    # Injection
    offset = rom_offset(zone, 0x054680)
    for i, slot in enumerate(i_slots):
        # lui v0, 0x8009
        patch.write_token(APTokenTypes.WRITE, offset, (0x3c028000 + (slot >> 16)).to_bytes(4, "little"))
        offset += 4
        # lbu v0, slot (v0)
        patch.write_token(APTokenTypes.WRITE, offset, (0x90420000 + (slot & 0xffff)).to_bytes(4, "little"))
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
        offset += 4
        next_slot = 5 + 5 * (len(i_slots) - i - 1)
        # beq v0, s3, pc + next
        patch.write_token(APTokenTypes.WRITE, offset, (0x10530000 + next_slot).to_bytes(4, "little"))
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
        offset += 4
    # Inventory check
    patch.write_token(APTokenTypes.WRITE, offset, (0x3c028009).to_bytes(4, "little"))  # lui v0, 0x8009
    offset += 4
    # lbu v0, 0x798a + id (v0)
    patch.write_token(APTokenTypes.WRITE, offset, (0x90420000 + item_id + equip_inv_id_offset).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    offset += 4
    # Return
    patch.write_token(APTokenTypes.WRITE, offset, (0x10400003).to_bytes(4, "little"))  # beq v0, r0, pc + 0x10
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x0806cc1f).to_bytes(4, "little"))  # j 0x801b307c
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x0806cc69).to_bytes(4, "little"))  # j 0x801b31a4
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    # Entry point
    offset = rom_offset(zone, 0x03431c)
    patch.write_token(APTokenTypes.WRITE, offset, (0x080751c0).to_bytes(4, "little"))  # j 0x801d4700
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    # Quantity check
    offset = rom_offset(zone, 0x054700)
    patch.write_token(APTokenTypes.WRITE, offset, (0x92620001).to_bytes(4, "little"))  # lbu v0, 0x0001 (s3)
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x2c4200ff).to_bytes(4, "little"))  # sltiu v0, v0, 0x00ff
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x14400003).to_bytes(4, "little"))  # bne v0, r0, pc + 0x10
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x0806d0d9).to_bytes(4, "little"))  # j 0x801b4364
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x92620000).to_bytes(4, "little"))  # lbu v0, 0x0000 (s3)
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x0806d0c9).to_bytes(4, "little"))  # j 0x801b4324
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop


def replace_boss_relic_with_item(opts: dict, patch: SotnProcedurePatch) -> None:
    relic = opts["relic"]
    boss = zones[relic["reward"]["zones"]]
    index = relic["index"]
    item = opts["item"]
    zone = zones[relic["zones"][0]]
    slots_list = item_slots(item)
    # Patch item table
    offset = rom_offset(zone, zone["items"] + 0x02 * index)
    item_id = tile_value(item, relic)
    patch.write_token(APTokenTypes.WRITE, offset, item_id.to_bytes(2, "little"))
    # Patch entities table
    for entity in relic["entities"]:
        if "as_item" in relic:
            if "x" in relic["as_item"]:
                offset = rom_offset(zone, entity + 0x00)
                patch.write_token(APTokenTypes.WRITE, offset, relic["as_item"]["x"].to_bytes(2, "little"))
            if "y" in relic["as_item"]:
                offset = rom_offset(zone, entity + 0x02)
                patch.write_token(APTokenTypes.WRITE, offset, relic["as_item"]["y"].to_bytes(2, "little"))
        offset = rom_offset(zone, entity + 0x04)
        patch.write_token(APTokenTypes.WRITE, offset, (0x000c).to_bytes(2, "little"))
        offset = rom_offset(zone, entity + 0x08)
        patch.write_token(APTokenTypes.WRITE, offset, index.to_bytes(2, "little"))
    # Patch instructions that load a relic
    patch.write_token(APTokenTypes.WRITE,
                      relic["erase"]["instructions"][0]["addresses"][0],
                      relic["erase"]["instructions"][0]["instruction"].to_bytes(4, "little"))
    # Patch boss rewards
    offset = rom_offset(boss, boss["rewards"])
    item_id = tile_value(item, relic)
    patch.write_token(APTokenTypes.WRITE, offset, item_id.to_bytes(2, "little"))
    # Entry point
    offset = rom_offset(zone, opts["entry"])
    # j inj
    patch.write_token(APTokenTypes.WRITE, offset, (0x08060000 + (opts["inj"] >> 2)).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00041400).to_bytes(4, "little"))  # sll v0, a0, 10
    # Zero tile function if item is equipped
    offset = rom_offset(zone, opts["inj"])
    # ori t1, r0, id
    patch.write_token(APTokenTypes.WRITE, offset, (0x34090000 + item["id"] + equip_id_offset).to_bytes(4, "little"))
    offset += 4
    for i, slot in enumerate(slots_list):
        # lui t0, 0x8009
        patch.write_token(APTokenTypes.WRITE, offset, (0x3c080000 + (slot >> 16)).to_bytes(4, "little"))
        offset += 4
        # lbu t0, slot (t0)
        patch.write_token(APTokenTypes.WRITE, offset, (0x91080000 + (slot & 0xffff)).to_bytes(4, "little"))
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
        offset += 4
        next_slot = 5 + 5 * (len(slots_list) - i - 1)
        # beq t0, t1, pc + next
        patch.write_token(APTokenTypes.WRITE, offset, (0x11090000 + next_slot).to_bytes(4, "little"))
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
        offset += 4
    # Inventory check
    patch.write_token(APTokenTypes.WRITE, offset, (0x3c088009).to_bytes(4, "little"))  # lui t0, 0x8009
    offset += 4
    # lbu t0, 0x798a + id (v0)
    patch.write_token(APTokenTypes.WRITE, offset, (0x91080000 + item["id"] + equip_inv_id_offset).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x11000004).to_bytes(4, "little"))  # beq t0, r0, pc + 0x14
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x3409000f).to_bytes(4, "little"))  # ori t1 ro, 0x000f
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x3c088018).to_bytes(4, "little"))  # lui t0, 0x8018
    offset += 4
    for addr in relic["entities"]:
        # sh t1, entity + 4 (t0)
        patch.write_token(APTokenTypes.WRITE, offset, (0xa5090000 + addr + 0x04).to_bytes(4, "little"))
        offset += 4
    # Return
    patch.write_token(APTokenTypes.WRITE, offset, (0x03e00008).to_bytes(4, "little"))  # jr ra
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    offset += 4


def replace_ring_of_vlad_with_item(opts: dict, patch: SotnProcedurePatch) -> None:
    zone = zones[ZONE["RNZ1"]]
    relic = opts["relic"]
    item = opts["item"]
    item_id = tile_value(item, relic)
    slots_list = item_slots(item)
    # Patch instructions that load a relic
    patch.write_token(APTokenTypes.WRITE,
                      relic["erase"]["instructions"][0]["addresses"][0],
                      relic["erase"]["instructions"][0]["instruction"].to_bytes(4, "little"))
    patch.write_token(APTokenTypes.WRITE, 0x059ee2c8, (0x3402000c).to_bytes(4, "little"))
    patch.write_token(APTokenTypes.WRITE, 0x059ee2d4, (0x24423a54).to_bytes(4, "little"))
    patch.write_token(APTokenTypes.WRITE, 0x059ee2e4, relic["index"].to_bytes(2, "little"))
    offset = rom_offset(zone, 0x2dd6)
    patch.write_token(APTokenTypes.WRITE, offset, relic["index"].to_bytes(2, "little"))
    # Replace item in rewards table
    offset = rom_offset(zone, zone["rewards"])
    patch.write_token(APTokenTypes.WRITE, offset, item_id.to_bytes(2, "little"))
    # Replace item in items table
    offset = rom_offset(zone, zone["items"] + 0x02 * relic["index"])
    patch.write_token(APTokenTypes.WRITE, offset, item_id.to_bytes(2, "little"))
    # Injection point
    offset = rom_offset(zone, 0x02c860)
    patch.write_token(APTokenTypes.WRITE, offset, (0x0806fbb4).to_bytes(4, "little"))  # j 0x801beed0
    offset = rom_offset(zone, 0x02c868)
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    # Get Bat defeat time
    offset = rom_offset(zone, 0x3eed0)
    patch.write_token(APTokenTypes.WRITE, offset, (0x3c020003).to_bytes(4, "little"))  # lui v0, 0x0003
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x3442ca78).to_bytes(4, "little"))  # ori v0, v0, 0xca78
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x8c420000).to_bytes(4, "little"))  # lw v0, 0x0000 (v0)
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    offset += 4
    # Branch if zero
    patch.write_token(APTokenTypes.WRITE, offset, (0x10400005).to_bytes(4, "little"))  # beq v0, r0, pc + 0x18
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    offset += 4
    # Change entity's position and slot
    patch.write_token(APTokenTypes.WRITE, offset, (0x3c088018).to_bytes(4, "little"))  # lui t0, 0x8018
    offset += 4
    # ori t1, r0, y
    patch.write_token(APTokenTypes.WRITE, offset, (0x34090000 + relic["as_item"]["y"]).to_bytes(4, "little"))
    offset += 4
    for addr in relic["entities"]:
        # sh t1, entity + 0x02 (t0)
        patch.write_token(APTokenTypes.WRITE, offset, (0xa5090000 + addr + 0x02).to_bytes(4, "little"))
        offset += 4
    # Zero out tile function pointer if item is in inventory
    # ori v0, r0, id
    patch.write_token(APTokenTypes.WRITE,
                      offset,
                      (0x34020000 + item["id"] + equip_id_offset).to_bytes(4, "little"))
    offset += 4
    for i, slot in enumerate(slots_list):
        # lui s0, 0x8009
        patch.write_token(APTokenTypes.WRITE, offset, (0x3c108000 + (slot >> 16)).to_bytes(4, "little"))
        offset += 4
        # lbu s0, slot (s0)
        patch.write_token(APTokenTypes.WRITE, offset, (0x92100000 + (slot & 0xffff)).to_bytes(4, "little"))
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
        offset += 4
        next_slot = 5 + 5 * (len(slots_list) - i - 1)
        # beq s0, v0, pc + next
        patch.write_token(APTokenTypes.WRITE, offset, (0x12020000 + next_slot).to_bytes(4, "little"))
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
        offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x3c108009).to_bytes(4, "little"))  # lui s0, 0x8009
    offset += 4
    # lbu s0, 0x798a + id (s0)
    patch.write_token(APTokenTypes.WRITE,
                      offset,
                      (0x92100000 + item["id"] + equip_inv_id_offset).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x12000002).to_bytes(4, "little"))  # beq s0, r0, pc + 0x0c
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x3c108007).to_bytes(4, "little"))  # lui s0, 0x8007
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0xae0065f0).to_bytes(4, "little"))  # sw r0, 0x65f0 (s0)
    offset += 4
    # return
    patch.write_token(APTokenTypes.WRITE, offset, (0x0806b21a).to_bytes(4, "little"))  # j 0x801ac868
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop


def replace_gold_ring_with_relic(relic_id: int, patch: SotnProcedurePatch) -> None:
    zone = zones[ZONE["NO4"]]
    # Put relic in entity table
    gold_ring = locations["Underground Caverns Succubus Side - Succubus item"]
    for addr in gold_ring["entities"]:
        offset = rom_offset(zone, addr + 8)
        patch.write_token(APTokenTypes.WRITE, offset, relic_id.to_bytes(2, "little"))
    # injection point
    offset = rom_offset(zone, 0x04c590)
    patch.write_token(APTokenTypes.WRITE, offset, (0x08077aed).to_bytes(4, "little"))  # j 0x801debb4
    # Branch
    offset = rom_offset(zone, 0x05ebb4)
    patch.write_token(APTokenTypes.WRITE, offset, (0x10400003).to_bytes(4, "little"))  # beq v0, r0, pc + 0x10
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    offset += 4
    # Return
    patch.write_token(APTokenTypes.WRITE, offset, (0x08073166).to_bytes(4, "little"))  # j 0x801cc598
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    offset += 4
    # Get Succubus defeat time
    patch.write_token(APTokenTypes.WRITE, offset, (0x3c020003).to_bytes(4, "little"))  # lui v0, 0x0003
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x3442ca4c).to_bytes(4, "little"))  # ori v0, v0, 0xca4c
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x8c420000).to_bytes(4, "little"))  # lw v0, 0x0000 (v0)
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    offset += 4
    # Branch if zero
    patch.write_token(APTokenTypes.WRITE, offset, (0x10400006).to_bytes(4, "little"))  # beq v0, r0, pc + 0x1c
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    offset += 4
    # Patch entity type
    patch.write_token(APTokenTypes.WRITE, offset, (0x3403000b).to_bytes(4, "little"))  # ori v1, r0, 0x000b
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x3c028018).to_bytes(4, "little"))  # lui v0, 0x8018
    offset += 4
    for addr in gold_ring["entities"]:
        # sh v1, addr + 4 (v0)
        patch.write_token(APTokenTypes.WRITE, offset, (0xa4430000 + addr + 4).to_bytes(4, "little"))
        offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x34020000).to_bytes(4, "little"))  # ori v0, r0, 0x0000
    offset += 4
    # Return
    patch.write_token(APTokenTypes.WRITE, offset, (0x0807316f).to_bytes(4, "little"))  # j 0x801cc5bc
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop


def replace_trio_with_relic(relic_id: int, patch: SotnProcedurePatch) -> None:
    trio = locations["Reverse Colosseum - Trio item"]
    # Boss zone patches
    boss = zones[ZONE["RBO0"]]
    # Patch rewards
    offset = rom_offset(boss, boss["rewards"] + 0x02 * trio["reward"]["index"])
    patch.write_token(APTokenTypes.WRITE, offset, relic_id.to_bytes(2, "little"))
    # Remove the condition for writing an item tile
    offset = rom_offset(boss, 0x026088)
    patch.write_token(APTokenTypes.WRITE, offset, (0x34020000).to_bytes(4, "little"))  # ori v0, r0, 0x0000
    # Regular zone patches
    zone = zones[ZONE["RARE"]]
    # Replace entities
    for entity in trio["entities"]:
        addr = rom_offset(zone, entity + 0x04)
        patch.write_token(APTokenTypes.WRITE, addr, (0x000b).to_bytes(2, "little"))
        addr += 2
        patch.write_token(APTokenTypes.WRITE, addr, (0x0010).to_bytes(2, "little"))
        addr += 2
        patch.write_token(APTokenTypes.WRITE, addr, relic_id.to_bytes(2, "little"))


def replace_trio_relic_with_item(opts: dict, patch: SotnProcedurePatch) -> None:
    replace_boss_relic_with_item(opts, patch)

    zone = zones[ZONE["RARE"]]
    trio = opts["relic"]
    for entity in trio["entities"]:
        addr = rom_offset(zone, entity + 0x06)
        patch.write_token(APTokenTypes.WRITE, addr, (0x0010).to_bytes(2, "little"))


def write_tokens(world: "SotnWorld", patch: SotnProcedurePatch):
    option_names: List[str] = [option_name for option_name in world.options_dataclass.type_hints if
                               option_name != "plando_items"]
    options_dict = world.options.as_dict(*option_names)

    if 'W' in world.multiworld.seed_name:
        seed_number = world.multiworld.seed_name[1:]
    else:
        seed_number = world.multiworld.seed_name
    options_dict["seed"] = seed_number
    options_dict["player"] = patch.player
    options_dict["player_name"] = patch.player_name
    randomize_items = options_dict["randomize_items"]

    # Patch Maria dialog to prevent player stuck after Hippogryph
    patch.write_token(APTokenTypes.WRITE, 0x0632f4cc, (0x1000000b).to_bytes(4, "little"))  # je, r0, r0

    relics_vlad = ["Heart of vlad", "Tooth of vlad", "Rib of vlad", "Ring of vlad", "Eye of vlad"]
    local_relics = {}
    copy1_relics = {}
    enemysanity_items = []
    dopp10_item = 0xffff

    for loc in world.multiworld.get_locations(world.player):
        # Save Jewel of open item
        if loc.name == "Long Library - Librarian Shop Item":
            item_data = items["Secret boots"]
            if loc.item.player == world.player:
                item_data = items[loc.item.name]
            jewel_item = item_data["id"]
            patch.write_token(APTokenTypes.WRITE, 0xf4f3a, jewel_item.to_bytes(2))
            patch.write_token(APTokenTypes.WRITE, 0x438d6d2, jewel_item.to_bytes(2, "little"))

        # Save Doppelganger10 item
        if loc.name == "Outer Wall - Doppleganger 10 item":
            if loc.item.player == world.player:
                dopp10_item = items[loc.item.name]
            else:
                dopp10_item = 0xffff

        if loc.item and loc.item.player == world.player:
            if loc.item.name == "Victory":
                continue
            item_data = items[loc.item.name]
            item_id = tile_value(item_data, {})
            loc_data = locations[loc.name]
            # Save relic locations
            if item_data["type"] == "RELIC":
                relic_id = item_id if item_id < 23 else item_id - 2
                if relic_id not in local_relics:
                    local_relics[relic_id] = loc_data["ap_id"]
                else:
                    copy1_relics[relic_id] = loc_data["ap_id"]

            # Save enemysanity locations
            if "Enemysanity" in loc.name:
                enemysanity_items.append(item_data["id"])
                continue

            # Relic locations
            if "vanilla_item" in loc_data and loc_data["vanilla_item"] in RELIC_NAMES:
                # Change relic for a relic
                if item_data["type"] == "RELIC":
                    if loc_data["vanilla_item"] == "Jewel of open":
                        for address in loc_data["addresses"]:
                            replace_shop_relic_with_relic(address, item_id, patch)
                    elif loc_data["vanilla_item"] in ["Bat card", "Skill of wolf"]:
                        for add in loc_data["addresses"]:
                            patch.write_token(APTokenTypes.WRITE, add, item_id.to_bytes(2, "little"))
                    else:
                        write_entity(loc_data, {"state": item_id}, patch)
                        if loc_data["vanilla_item"] in relics_vlad:
                            if loc_data["vanilla_item"] == "Ring of vlad":
                                for address in loc_data["ids"][0]["addresses"]:
                                    patch.write_token(APTokenTypes.WRITE, address, item_id.to_bytes(2, "little"))
                            # Patch Vlad relics boss area
                            else:
                                zone = zones[loc_data["reward"]["zones"]]
                                index = loc_data["reward"]["index"]
                                address = rom_offset(zone, zone["rewards"] + 0x02 * index)
                                patch.write_token(APTokenTypes.WRITE, address, item_id.to_bytes(2, "little"))
                # Change relic for an item
                else:
                    vanilla = loc_data["vanilla_item"]
                    if vanilla == "Jewel of open":
                        replace_shop_relic_with_item(item_data, patch)
                    elif vanilla == "Heart of vlad":
                        opts = {"relic": loc_data, "item": item_data, "entry": 0x034950, "inj": 0x047900}
                        replace_boss_relic_with_item(opts, patch)
                    elif vanilla == "Tooth of vlad":
                        opts = {"relic": loc_data, "item": item_data, "entry": 0x029fc0, "inj": 0x037500}
                        replace_boss_relic_with_item(opts, patch)
                    elif vanilla == "Rib of vlad":
                        opts = {"relic": loc_data, "item": item_data, "entry": 0x037014, "inj": 0x04bf00}
                        replace_boss_relic_with_item(opts, patch)
                    elif vanilla == "Ring of vlad":
                        opts = {"relic": loc_data, "item": item_data}
                        replace_ring_of_vlad_with_item(opts, patch)
                    elif vanilla == "Eye of vlad":
                        opts = {"relic": loc_data, "item": item_data, "entry": 0x01af18, "inj": 0x02a000}
                        replace_boss_relic_with_item(opts, patch)
                    else:
                        as_item = {}
                        if "as_item" in loc_data:
                            as_item = loc_data["as_item"]

                        if "index" in loc_data:
                            write_entity(loc_data, {"id": 0x000c, "state": loc_data["index"]} | as_item, patch)
                            write_tile_id(loc_data["zones"], loc_data["index"], item_id, patch)
                        else:
                            print(f"ERROR on {loc_data}")
            # Item locations
            else:
                if "no_offset" in loc_data:
                    # Relics and vessels are forbid on no offset locations
                    if item_data["type"] == "RELIC":
                        as_relic = {}
                        if "as_relic" in loc_data:
                            as_relic = loc_data["as_relic"]
                        write_entity(loc_data, {"id": 0x000b, "state": item_id} | as_relic, patch)
                    elif item_data["type"] == "POWERUP":
                        for add in loc_data["addresses"]:
                            patch.write_token(APTokenTypes.WRITE, add, (0x0000).to_bytes(2, "little"))
                    else:
                        # TODO In the future add traps and boosts
                        new_value = tile_value(item_data, {"no_offset": True})
                        for add in loc_data["addresses"]:
                            patch.write_token(APTokenTypes.WRITE, add, new_value.to_bytes(2, "little"))
                elif "vanilla_item" in loc_data and loc_data["vanilla_item"] == "Holy glasses":
                    if item_data["type"] == "RELIC":
                        replace_holy_glasses_with_relic(loc_data["erase"]["instructions"], item_id, patch)
                    else:
                        for address in loc_data["addresses"]:
                            # Holy glasses is no-offset item
                            item_id = tile_value(item_data, {"no_offset": True})
                            patch.write_token(APTokenTypes.WRITE, address, item_id.to_bytes(2, "little"))
                elif "trio" in loc_data:
                    opts = {"relic": loc_data, "item": item_data, "entry": 0x026e64, "inj": 0x038a00}
                    if item_data["type"] == "RELIC":
                        replace_trio_with_relic(item_id, patch)
                    else:
                        replace_trio_relic_with_item(opts, patch)
                elif "index" in loc_data:
                    if loc_data["vanilla_item"] == "Gold ring":
                        if item_data["type"] == "RELIC":
                            replace_gold_ring_with_relic(item_id, patch)
                        else:
                            # TODO In the future add traps and boosts
                            for address in loc_data["addresses"]:
                                patch.write_token(APTokenTypes.WRITE, address, item_id.to_bytes(2, "little"))
                    else:
                        # Change item to relic
                        if item_data["type"] == "RELIC":
                            as_relic = {}
                            if "as_relic" in loc_data:
                                as_relic = loc_data["as_relic"]

                            write_entity(loc_data, {"id": 0x000b, "state": item_id} | as_relic, patch)
                        # Change item to item
                        else:
                            write_tile_id(loc_data["zones"], loc_data["index"], item_id, patch)
                else:
                    # Turkey on breakable wall isn't no_offset
                    if loc_data["ap_id"] == 40:
                        for address in loc_data["addresses"]:
                            patch.write_token(APTokenTypes.WRITE, address, item_id.to_bytes(2, "little"))
                    # Bosses drop
                    elif "boss" in loc_data and loc_data["boss"]:
                        address = loc_data["bin_address"]
                        patch.write_token(APTokenTypes.WRITE, address, item_id.to_bytes(2, "little"))
                    else:
                        print(f"ERROR in {loc_data}")
        # Off world items
        elif loc.item and loc.item.player != world.player:
            # Save enemysanity locations
            if "Enemysanity" in loc.name:
                enemysanity_items.append(0xfff)
                continue
            loc_data = locations[loc.name]
            item_data = items["Secret boots"]
            item_id = tile_value(item_data, {})
            gold_value = 0x04  # 04 -> Yellow bag of gold
            if (loc.item.classification == ItemClassification.progression or
                    loc.item.classification == ItemClassification.progression_skip_balancing):
                gold_value = 0x07  # 07 -> Blue bag of gold
            elif loc.item.classification == ItemClassification.useful:
                gold_value = 0x03  # 03 -> Red bag of gold
            # Relic locations
            if "vanilla_item" in loc_data and loc_data["vanilla_item"] in RELIC_NAMES:
                vanilla = loc_data["vanilla_item"]
                if vanilla == "Jewel of open":
                    replace_shop_relic_with_item(items["Secret boots"], patch)
                elif vanilla == "Heart of vlad":
                    opts = {"relic": loc_data, "item": item_data, "entry": 0x034950, "inj": 0x047900}
                    replace_boss_relic_with_item(opts, patch)
                elif vanilla == "Tooth of vlad":
                    opts = {"relic": loc_data, "item": item_data, "entry": 0x029fc0, "inj": 0x037500}
                    replace_boss_relic_with_item(opts, patch)
                elif vanilla == "Rib of vlad":
                    opts = {"relic": loc_data, "item": item_data, "entry": 0x037014, "inj": 0x04bf00}
                    replace_boss_relic_with_item(opts, patch)
                elif vanilla == "Ring of vlad":
                    opts = {"relic": loc_data, "item": item_data}
                    replace_ring_of_vlad_with_item(opts, patch)
                elif vanilla == "Eye of vlad":
                    opts = {"relic": loc_data, "item": item_data, "entry": 0x01af18, "inj": 0x02a000}
                    replace_boss_relic_with_item(opts, patch)
                else:
                    as_item = {}
                    if "as_item" in loc_data:
                        as_item = loc_data["as_item"]

                    if "index" in loc_data:
                        write_entity(loc_data, {"id": 0x000c, "state": loc_data["index"]} | as_item, patch)
                        write_tile_id(loc_data["zones"], loc_data["index"], gold_value, patch)
                    else:
                        print(f"ERROR on {loc_data}")
            # Items locations
            else:
                # 06 -> Green bag of gold
                # 08 -> Purple bag of gold
                # 09 -> Gray bag of gold
                # 0A -> Black bag of gold
                # 0B -> Chest of gold
                if "no_offset" in loc_data:
                    new_value = tile_value(item_data, {"no_offset": True})
                    for add in loc_data["addresses"]:
                        patch.write_token(APTokenTypes.WRITE, add, new_value.to_bytes(2, "little"))
                elif "vanilla_item" in loc_data and loc_data["vanilla_item"] == "Holy glasses":
                    # Holy glasses is no-offset item
                    item_id = tile_value(item_data, {"no_offset": True})
                    for address in loc_data["addresses"]:
                        patch.write_token(APTokenTypes.WRITE, address, item_id.to_bytes(2, "little"))
                elif "trio" in loc_data:
                    opts = {"relic": loc_data, "item": item_data, "entry": 0x026e64, "inj": 0x038a00}
                    replace_trio_relic_with_item(opts, patch)
                elif "index" in loc_data:
                    if loc_data["vanilla_item"] == "Gold ring":
                        for address in loc_data["addresses"]:
                            patch.write_token(APTokenTypes.WRITE, address, gold_value.to_bytes(2, "little"))
                    else:
                        write_tile_id(loc_data["zones"], loc_data["index"], gold_value, patch)
                else:
                    # Turkey on breakable wall isn't no_offset
                    if loc_data["ap_id"] == 40:
                        for address in loc_data["addresses"]:
                            patch.write_token(APTokenTypes.WRITE, address, item_id.to_bytes(2, "little"))
                    elif "boss" in loc_data and loc_data["boss"]:
                        address = loc_data["bin_address"]
                        patch.write_token(APTokenTypes.WRITE, address, item_id.to_bytes(2, "little"))
                    else:
                        print(f"ERROR off world in {loc_data}")

    # Jewel of open price at 0x47a3098 01f4/500 change to 10
    patch.write_token(APTokenTypes.WRITE, 0x47a3098, (10).to_bytes(2, "little"))
    # Write relic location in time-attack menu TOTAL RELICS 28
    # Defeat Minoutaur and Werewolf 30/30 bytes 20 relics(20) @RAM 0x0dfcdc
    start_address = 0x438d66c
    offset = 0x4298798
    for i in range(0, 20, 2):
        try:
            relic1 = local_relics[i]
        except KeyError:
            relic1 = 0xfff
        try:
            relic2 = local_relics[i+1]
        except KeyError:
            relic2 = 0xfff

        transformed = items_as_bytes(relic1, relic2)
        for relic_byte in transformed:
            patch.write_token(APTokenTypes.WRITE, start_address, struct.pack("<B", relic_byte))
            patch.write_token(APTokenTypes.WRITE, start_address - offset, struct.pack("<B", relic_byte))
            start_address += 1
    # Terminate
    patch.write_token(APTokenTypes.WRITE, start_address, (0xff00).to_bytes(2))
    patch.write_token(APTokenTypes.WRITE, start_address - offset, (0xff00).to_bytes(2))

    # Defeat Granfaloon 18/18 bytes 12 relics(8 relics / 4 copy) @RAM 0x0dfcfc
    start_address = 0x438d68c
    for i in range(20, 28, 2):
        try:
            relic1 = local_relics[i]
        except KeyError:
            relic1 = 0xfff
        try:
            relic2 = local_relics[i+1]
        except KeyError:
            relic2 = 0xfff

        transformed = items_as_bytes(relic1, relic2)
        for relic_byte in transformed:
            patch.write_token(APTokenTypes.WRITE, start_address, struct.pack("<B", relic_byte))
            patch.write_token(APTokenTypes.WRITE, start_address - offset, struct.pack("<B", relic_byte))
            start_address += 1

    if len(copy1_relics) != 0:
        for i in range(0, 4, 2):
            try:
                relic1 = copy1_relics[i]
            except KeyError:
                relic1 = 0xfff
            try:
                relic2 = copy1_relics[i+1]
            except KeyError:
                relic2 = 0xfff

            transformed = items_as_bytes(relic1, relic2)
            for relic_byte in transformed:
                patch.write_token(APTokenTypes.WRITE, start_address, struct.pack("<B", relic_byte))
                patch.write_token(APTokenTypes.WRITE, start_address - offset, struct.pack("<B", relic_byte))
                start_address += 1
        # Terminate
        patch.write_token(APTokenTypes.WRITE, start_address, (0xff00).to_bytes(2))
        patch.write_token(APTokenTypes.WRITE, start_address - offset, (0xff00).to_bytes(2))

        # Defeat Dopp?? 21/22 bytes 14 relics (18) @RAM 0dfd10
        start_address = 0x438d6a0
        for i in range(4, 18, 2):
            try:
                relic1 = copy1_relics[i]
            except KeyError:
                relic1 = 0xfff
            try:
                relic2 = copy1_relics[i+1]
            except KeyError:
                relic2 = 0xfff

            transformed = items_as_bytes(relic1, relic2)
            for relic_byte in transformed:
                patch.write_token(APTokenTypes.WRITE, start_address, struct.pack("<B", relic_byte))
                patch.write_token(APTokenTypes.WRITE, start_address - offset, struct.pack("<B", relic_byte))
                start_address += 1
        # Terminate
        patch.write_token(APTokenTypes.WRITE, start_address, (0xff00).to_bytes(2))
        patch.write_token(APTokenTypes.WRITE, start_address - offset, (0xff00).to_bytes(2))

        # Defeat Olrox 12/14 bytes 8 relics (24) @RAM 0x0dfd28
        start_address = 0x438d6b8
        for i in range(18, 26, 2):
            try:
                relic1 = copy1_relics[i]
            except KeyError:
                relic1 = 0xfff
            try:
                relic2 = copy1_relics[i+1]
            except KeyError:
                relic2 = 0xfff

            transformed = items_as_bytes(relic1, relic2)
            for relic_byte in transformed:
                patch.write_token(APTokenTypes.WRITE, start_address, struct.pack("<B", relic_byte))
                patch.write_token(APTokenTypes.WRITE, start_address - offset, struct.pack("<B", relic_byte))
                start_address += 1

        # Terminate
        patch.write_token(APTokenTypes.WRITE, start_address, (0xff00).to_bytes(2))
        patch.write_token(APTokenTypes.WRITE, start_address - offset, (0xff00).to_bytes(2))

        # Richter defeat dracula 3/26 bytes 2 relics (28) @RAM 0x0dfd38
        start_address = 0x438d6c8
        for i in range(26, 28, 2):
            try:
                relic1 = copy1_relics[i]
            except KeyError:
                relic1 = 0xfff
            try:
                relic2 = copy1_relics[i+1]
            except KeyError:
                relic2 = 0xfff

            transformed = items_as_bytes(relic1, relic2)
            for relic_byte in transformed:
                patch.write_token(APTokenTypes.WRITE, start_address, struct.pack("<B", relic_byte))
                patch.write_token(APTokenTypes.WRITE, start_address - offset, struct.pack("<B", relic_byte))
                start_address += 1
        # Terminate
        patch.write_token(APTokenTypes.WRITE, start_address, (0xff00).to_bytes(2))
        patch.write_token(APTokenTypes.WRITE, start_address - offset, (0xff00).to_bytes(2))
        # Richter Defeat Dracula   23 bytes left

    # WRITE DOPP 10 ITEM on the very end of Defeat Olrox and terminate
    if dopp10_item == 0xffff:
        item_id = dopp10_item
    else:
        item_id = dopp10_item["id"]
    patch.write_token(APTokenTypes.WRITE, 0x438d6c4, item_id.to_bytes(2))
    patch.write_token(APTokenTypes.WRITE, 0x438d6c4 - 0x4298798, item_id.to_bytes(2))
    patch.write_token(APTokenTypes.WRITE, 0x438d6c6, (0xff00).to_bytes(2))
    patch.write_token(APTokenTypes.WRITE, 0x438d6c6 - 0x4298798, (0xff00).to_bytes(2))

    # Write enemysanity items in time-attack menu
    if len(enemysanity_items):
        # Final save 18 bytes 12 items (12) @RAM 0x0dfb58
        start_address = 0x438d4e8
        offset = 0x4298798
        for i in range(0, 12, 2):
            transformed = items_as_bytes(enemysanity_items[i], enemysanity_items[i+1])
            for item_byte in transformed:
                patch.write_token(APTokenTypes.WRITE, start_address, struct.pack("<B", item_byte))
                patch.write_token(APTokenTypes.WRITE, start_address - offset, struct.pack("<B", item_byte))
                start_address += 1
        # Terminate Final save
        patch.write_token(APTokenTypes.WRITE, start_address, (0xff00).to_bytes(2))
        patch.write_token(APTokenTypes.WRITE, start_address - offset, (0xff00).to_bytes(2))
        # Defeat Galamoth 18 bytes 12 items (24) @RAM 0x0dfb6c
        start_address = 0x438d4fc
        for i in range(12, 24, 2):
            transformed = items_as_bytes(enemysanity_items[i], enemysanity_items[i+1])
            for item_byte in transformed:
                patch.write_token(APTokenTypes.WRITE, start_address, struct.pack("<B", item_byte))
                patch.write_token(APTokenTypes.WRITE, start_address - offset, struct.pack("<B", item_byte))
                start_address += 1
        # Terminate Defeat Galamoth
        patch.write_token(APTokenTypes.WRITE, start_address, (0xff00).to_bytes(2))
        patch.write_token(APTokenTypes.WRITE, start_address - offset, (0xff00).to_bytes(2))
        # Defeat Darkwing Bat 22 bytes 14 items (38) @RAM 0x0dfb80
        start_address = 0x438d510
        for i in range(24, 38, 2):
            transformed = items_as_bytes(enemysanity_items[i], enemysanity_items[i+1])
            for item_byte in transformed:
                patch.write_token(APTokenTypes.WRITE, start_address, struct.pack("<B", item_byte))
                patch.write_token(APTokenTypes.WRITE, start_address - offset, struct.pack("<B", item_byte))
                start_address += 1
        # Terminate Defeat Darkwing Bat
        patch.write_token(APTokenTypes.WRITE, start_address, (0xff00).to_bytes(2))
        patch.write_token(APTokenTypes.WRITE, start_address - offset, (0xff00).to_bytes(2))
        # Defeat Akmodan II 18 bytes 12 items (50) @RAM 0x0dfb98
        start_address = 0x438d528
        for i in range(38, 50, 2):
            transformed = items_as_bytes(enemysanity_items[i], enemysanity_items[i + 1])
            for item_byte in transformed:
                patch.write_token(APTokenTypes.WRITE, start_address, struct.pack("<B", item_byte))
                patch.write_token(APTokenTypes.WRITE, start_address - offset, struct.pack("<B", item_byte))
                start_address += 1
        # Terminate Defeat Akmodan II
        patch.write_token(APTokenTypes.WRITE, start_address, (0xff00).to_bytes(2))
        patch.write_token(APTokenTypes.WRITE, start_address - offset, (0xff00).to_bytes(2))
        # Defeat Dopp?? 21 bytes 14 items (64) @RAM 0x0dfbac
        start_address = 0x438d53c
        for i in range(50, 64, 2):
            transformed = items_as_bytes(enemysanity_items[i], enemysanity_items[i + 1])
            for item_byte in transformed:
                patch.write_token(APTokenTypes.WRITE, start_address, struct.pack("<B", item_byte))
                patch.write_token(APTokenTypes.WRITE, start_address - offset, struct.pack("<B", item_byte))
                start_address += 1
        # Terminate Defeat Dopp??
        patch.write_token(APTokenTypes.WRITE, start_address, (0xff00).to_bytes(2))
        patch.write_token(APTokenTypes.WRITE, start_address - offset, (0xff00).to_bytes(2))
        # Defeat Lesser Demon 22 bytes 14 items (78) @RAM 0x0dfbc4
        start_address = 0x438d554
        for i in range(64, 78, 2):
            transformed = items_as_bytes(enemysanity_items[i], enemysanity_items[i + 1])
            for item_byte in transformed:
                patch.write_token(APTokenTypes.WRITE, start_address, struct.pack("<B", item_byte))
                patch.write_token(APTokenTypes.WRITE, start_address - offset, struct.pack("<B", item_byte))
                start_address += 1
        # Terminate Defeat Lesser Demon
        patch.write_token(APTokenTypes.WRITE, start_address, (0xff00).to_bytes(2))
        patch.write_token(APTokenTypes.WRITE, start_address - offset, (0xff00).to_bytes(2))
        # Defeat Creature 22 bytes 14 items (92) @RAM 0x0dfbdc
        start_address = 0x438d56c
        for i in range(78, 92, 2):
            transformed = items_as_bytes(enemysanity_items[i], enemysanity_items[i + 1])
            for item_byte in transformed:
                patch.write_token(APTokenTypes.WRITE, start_address, struct.pack("<B", item_byte))
                patch.write_token(APTokenTypes.WRITE, start_address - offset, struct.pack("<B", item_byte))
                start_address += 1
        # Terminate Defeat Creature
        patch.write_token(APTokenTypes.WRITE, start_address, (0xff00).to_bytes(2))
        patch.write_token(APTokenTypes.WRITE, start_address - offset, (0xff00).to_bytes(2))
        # Defeat Medusa 14 bytes 8 items (100) @RAM 0x0dfbf4
        start_address = 0x438d584
        for i in range(92, 100, 2):
            transformed = items_as_bytes(enemysanity_items[i], enemysanity_items[i + 1])
            for item_byte in transformed:
                patch.write_token(APTokenTypes.WRITE, start_address, struct.pack("<B", item_byte))
                patch.write_token(APTokenTypes.WRITE, start_address - offset, struct.pack("<B", item_byte))
                start_address += 1
        # Terminate Defeat Medusa
        patch.write_token(APTokenTypes.WRITE, start_address, (0xff00).to_bytes(2))
        patch.write_token(APTokenTypes.WRITE, start_address - offset, (0xff00).to_bytes(2))
        # Save Richter 22 bytes 14 items (114) @RAM 0x0dfc04
        start_address = 0x438d594
        for i in range(100, 114, 2):
            transformed = items_as_bytes(enemysanity_items[i], enemysanity_items[i + 1])
            for item_byte in transformed:
                patch.write_token(APTokenTypes.WRITE, start_address, struct.pack("<B", item_byte))
                patch.write_token(APTokenTypes.WRITE, start_address - offset, struct.pack("<B", item_byte))
                start_address += 1
        # Terminate Save Richter
        patch.write_token(APTokenTypes.WRITE, start_address, (0xff00).to_bytes(2))
        patch.write_token(APTokenTypes.WRITE, start_address - offset, (0xff00).to_bytes(2))
        # Defeat Cerberus 18 bytes 12 items (126) @RAM 0x0dfc1c
        start_address = 0x438d5ac
        for i in range(114, 126, 2):
            transformed = items_as_bytes(enemysanity_items[i], enemysanity_items[i + 1])
            for item_byte in transformed:
                patch.write_token(APTokenTypes.WRITE, start_address, struct.pack("<B", item_byte))
                patch.write_token(APTokenTypes.WRITE, start_address - offset, struct.pack("<B", item_byte))
                start_address += 1
        # Terminate Defeat Cerberus
        patch.write_token(APTokenTypes.WRITE, start_address, (0xff00).to_bytes(2))
        patch.write_token(APTokenTypes.WRITE, start_address - offset, (0xff00).to_bytes(2))
        # Defeat Death 12 bytes 8 items (134) @RAM 0x0dfc30
        start_address = 0x438d5c0
        for i in range(126, 134, 2):
            transformed = items_as_bytes(enemysanity_items[i], enemysanity_items[i + 1])
            for item_byte in transformed:
                patch.write_token(APTokenTypes.WRITE, start_address, struct.pack("<B", item_byte))
                patch.write_token(APTokenTypes.WRITE, start_address - offset, struct.pack("<B", item_byte))
                start_address += 1
        # Terminate Defeat Death
        patch.write_token(APTokenTypes.WRITE, start_address, (0xff00).to_bytes(2))
        patch.write_token(APTokenTypes.WRITE, start_address - offset, (0xff00).to_bytes(2))
        # Defeat Trevor, Grant 32 bytes total only need 12 bytes 7 items (141) @RAM 0x0dfc40
        start_address = 0x438d5d0
        for i in range(134, 141, 2):
            try:
                transformed = items_as_bytes(enemysanity_items[i], enemysanity_items[i + 1])
            except IndexError:
                transformed = items_as_bytes(enemysanity_items[i], 0x00)
            for item_byte in transformed:
                patch.write_token(APTokenTypes.WRITE, start_address, struct.pack("<B", item_byte))
                patch.write_token(APTokenTypes.WRITE, start_address - offset, struct.pack("<B", item_byte))
                start_address += 1
        # Don't need to terminate. 23 bytes remaining

    # Randomize items
    non_locations = {}
    offset_locations = {}
    vanilla_list = []
    filled_locations = [loc.name for loc in world.multiworld.get_filled_locations(world.player)]

    for k, v in locations.items():
        if "Enemysanity" in k:
            continue
        if k not in filled_locations and randomize_items:
            if "no_offset" in v or v["ap_id"] == 40:
                offset_locations[k] = v
            else:
                non_locations[k] = v
            vanilla_list.append(v["vanilla_item"])

    if world.options.powerful_items.value:
        while len(vanilla_list) and len(world.extra_add):
            vanilla_list.pop(world.random.randrange(len(vanilla_list)))
            vanilla_list.append(world.extra_add.pop(world.random.randrange(len(world.extra_add))))

    # Place no_offset locations first
    while len(offset_locations):
        placed = False
        while not placed:
            item = world.random.choice(vanilla_list)
            if item not in ["Life Vessel", "Heart Vessel"]:
                loc = offset_locations.popitem()
                new_value = tile_value(items[item], {"no_offset": True})
                # Abandoned Mine Demon Side - Item on Breakable Wall is not no_offset
                if loc[1]["ap_id"] == 40:
                    new_value = tile_value(items[item], {})
                for add in loc[1]["addresses"]:
                    patch.write_token(APTokenTypes.WRITE, add, new_value.to_bytes(2, "little"))
                vanilla_list.remove(item)
                placed = True

    # Place non-randomized items
    while len(non_locations):
        loc = non_locations.popitem()
        item = vanilla_list.pop(world.random.randrange(len(vanilla_list)))
        item_id = tile_value(items[item], {})
        if "boss" in loc[1]:
            patch.write_token(APTokenTypes.WRITE, loc[1]["bin_address"], item_id.to_bytes(2, "little"))
        else:
            write_tile_id(loc[1]["zones"], loc[1]["index"], item_id, patch)

    """
    The flag that get set on NO4 switch: 0x03be1c and the instruction is jz, r2, 80181230 on 0x5430404 we patched
    to jne r0, r0 so it never branch.

    The flag that get set on ARE switch: 0x03be9d and the instruction is jz, r2, 801b6f84 on 0x440110c we patched
    to jne r0, r0 so it never branch.

    The flag that get set on NO2 switch: 0x03be4c and the instruction is jz, r2, 801c1028 on 0x46c0968 we patched
    to jne r0, r0 so it never branch.
    """
    if options_dict["open_no4"] != 0:
        if options_dict["open_no4"] == 1:
            patch.write_token(APTokenTypes.WRITE, 0x05430404, (0x14000005).to_bytes(4, "little"))
        if options_dict["open_no4"] == 2:
            patch.write_token(APTokenTypes.WRITE, 0x4ba8798, (0x14000005).to_bytes(4, "little"))
            patch.write_token(APTokenTypes.WRITE, 0x05430404, (0x14000005).to_bytes(4, "little"))

    if options_dict["open_are"]:
        patch.write_token(APTokenTypes.WRITE, 0x0440110c, (0x14000066).to_bytes(4, "little"))

    """
    The instruction that check relics of Vlad is jnz r2, 801c1790 we gonna change to je r0, r0 so it's always 
    branch. ROM is @ 0x4fcf7b4 and RAM is @ 0x801c132c
    """
    #if options_dict["goal"] == 3 or options_dict["goal"] == 5:
    #    patch.write_token(APTokenTypes.WRITE, 0x04fcf7b4, (0x10000118).to_bytes(4, "little"))

    sanity = 0
    if options_dict["enemysanity"]:
        sanity |= (1 << 0)
    if options_dict["enemy_scroll"]:
        sanity |= (1 << 1)
    if options_dict["auto_heal"]:
        sanity |= (1 << 6)
    if options_dict["death_link"]:
        sanity |= (1 << 7)

    enemy_mod = 0
    shop_price_min = -10
    shop_price_max = -10
    drop_mod = 0

    if options_dict["difficult"] != 1:
        if options_dict["difficult"] == 0:
            enemy_mod = 50 / 100
            shop_price_min = 50
            shop_price_max = 75
            drop_mod = 3
        elif options_dict["difficult"] == 2:
            enemy_mod = 150 / 100
            shop_price_min = 100
            shop_price_max = 125
        elif options_dict["difficult"] == 3:
            enemy_mod = 200 / 100
            shop_price_min = 125
            shop_price_max = 150

    if options_dict["enemy_mod"] >= 25:
        enemy_mod = options_dict["enemy_mod"] / 100

    if enemy_mod != 0 or options_dict["enemy_stats"]:
        enemy_stat_rando(enemy_mod, options_dict["enemy_stats"], world, patch)

    if options_dict["drop_mod"] != 0:
        drop_mod = options_dict["drop_mod"]

    if drop_mod != 0:
        modify_drop(options_dict["drop_mod"], patch)

    player_name = world.multiworld.get_player_name(world.player)
    player_num = world.player

    seed_num = options_dict["seed"]

    write_seed(patch, seed_num, player_num, player_name, sanity)

    if options_dict["infinite_wing_smash"]:
        # Wing smash timer
        # Thanks Forat Negre for the info on that
        # @ RAM 1173c8
        patch.write_token(APTokenTypes.WRITE, 0x00134990, (0x00000000).to_bytes(4, "little"))

    if options_dict["rng_start_gear"]:
        randomize_starting_equipment(world, patch)

    if options_dict["remove_prologue"]:
        no_prologue(patch)

    map_colors_value = options_dict["map_color"]
    if map_colors_value != 0:
        map_color(map_colors_value, patch)

    alucard_palette_value = options_dict["alucard_palette"]
    if alucard_palette_value != 0:
        alucard_palette(alucard_palette_value, patch)

    alucard_liner(options_dict["alucard_liner"], patch)

    if options_dict["magic_vessels"]:
        magic_max(patch)

    if options_dict["anti_freeze"]:
        anti_freeze(patch)

    if options_dict["my_purse"]:
        my_purse(patch)

    if options_dict["fast_warp"]:
        fast_warp(patch)

    if options_dict["unlocked_mode"]:
        unlocked_patches(patch)

    if options_dict["relic_suprise"]:
        surprise_patches(patch)

    if options_dict["shop_prices"]:
        shop_price_min = 50
        shop_price_max = 150

    randomize_shop(shop_price_min, shop_price_max, options_dict["random_shop"], world, patch)

    if options_dict["starting_zone"] != 0:
        start_room_rando(options_dict["starting_zone"], world, patch)

    if options_dict["reverse_library"]:
        rlib_card(patch)

    if options_dict["random_music"]:
        randomize_music(world, patch)

    # Thanks DerDrach to point me where to find those on SOTN.IO
    if options_dict["color_randomizer"]:
        randomize_cape_colors(world, patch)
        randomize_grav_boot_colors(world, patch)
        randomize_hydro_storm_color(world, patch)
        randomize_wing_smash_color(world, patch)
        randomize_richter_color(world, patch)
        randomize_dracula_cape(world, patch)
        randomize_maria_color(world, patch)

    if options_dict["skip_nz1"]:
        disable_nz1_puzzle(patch)

    if options_dict["randomize_drop"]:
        randomize_drop(options_dict["randomize_drop"], world, patch)

    apply_acessibility_patches(patch)
    rando_func_master(0, patch)

    options_dict["version"] = CURRENT_VERSION

    patch.write_file("options.json", json.dumps(options_dict).encode("utf-8"))
    patch.write_file("token_data.bin", patch.get_token_binary())


def random_color(world: "SotnWorld") -> int:
    return 0x8000 | math.floor(world.random.random() * 0x10000)


def cape_color(world: "SotnWorld", lining_address: int, outer_address: int, opts: dict, patch: SotnProcedurePatch):
    if "liningColor1" in opts:
        lining_color_1 = opts["liningColor1"]
    else:
        lining_color_1 = random_color(world)

    if "liningColor2" in opts:
        lining_color_2 = opts["liningColor2"]
    else:
        lining_color_2 = random_color(world)

    if "outerColor1" in opts:
        outer_color_1 = opts["outerColor1"]
    else:
        outer_color_1 = random_color(world)

    if "outerColor2" in opts:
        outer_color_2 = opts["outerColor2"]
    else:
        outer_color_2 = random_color(world)

    patch.write_token(APTokenTypes.WRITE, lining_address + 0x00, lining_color_1.to_bytes(2, "little"))
    patch.write_token(APTokenTypes.WRITE, lining_address + 0x02, lining_color_2.to_bytes(2, "little"))
    patch.write_token(APTokenTypes.WRITE, outer_address + 0x00, outer_color_1.to_bytes(2, "little"))
    patch.write_token(APTokenTypes.WRITE, outer_address + 0x02, outer_color_2.to_bytes(2, "little"))


def randomize_josephs_cloak(world: "SotnWorld", patch: SotnProcedurePatch):
    colors = [
        math.floor(world.random.random() * 32),
        math.floor(world.random.random() * 32),
        math.floor(world.random.random() * 32),
        math.floor(world.random.random() * 32),
        math.floor(world.random.random() * 32),
        math.floor(world.random.random() * 32)
    ]
    # Write the jump to injected code
    rom_address = 0x158c98
    ram_address = 0x136c00
    patch.write_token(APTokenTypes.WRITE, 0x0fa97c, (0x0c000000 + (ram_address >> 2)).to_bytes(4, "little"))
    # Write the color setting instructions
    address = rom_address
    for i in range(len(colors)):
        patch.write_token(APTokenTypes.WRITE, address, (0x3c020003).to_bytes(4, "little"))
        address += 4
        patch.write_token(APTokenTypes.WRITE, address, (0x3442caa8 + 4 * i).to_bytes(4, "little"))
        address += 4
        patch.write_token(APTokenTypes.WRITE, address, (0x24030000 + colors[i]).to_bytes(4, "little"))
        address += 4
        patch.write_token(APTokenTypes.WRITE, address, (0xa0430000).to_bytes(4, "little"))
        address += 4

    # Write the jump from injected code
    patch.write_token(APTokenTypes.WRITE, address, (0x0803924f).to_bytes(4, "little"))


def randomize_cape_colors(world: "SotnWorld", patch: SotnProcedurePatch):
    # Cloth Cape
    cape_color(world, 0x0afb84, 0x0afb88, {}, patch)
    # Reverse Cloak & Inverted Cloak
    lining_1 = random_color(world)
    lining_2 = random_color(world)
    outer_1 = random_color(world)
    outer_2 = random_color(world)
    cape_color(world, 0x0afb7c, 0x0afb80,
               {"liningColor1": lining_1, "liningColor2": lining_2, "outerColor1": outer_1, "outerColor2": outer_2},
               patch)
    cape_color(world, 0x0afbb8, 0x0afbbc,
               {"liningColor1": lining_1, "liningColor2": lining_2, "outerColor1": outer_1, "outerColor2": outer_2},
               patch)
    # Elven Cloak
    cape_color(world, 0x0afb94, 0x0afb98, {}, patch)
    # Crystal Cloak
    cape_color(world, 0x0afba4, 0x0afba8, {"outerColor1": 0x0000}, patch)
    # Royal Cloak
    cape_color(world, 0x0afb8c, 0x0afb90, {}, patch)
    # Blood Cloak
    cape_color(world, 0x0afb9c, 0x0afba0, {}, patch)
    # Joseph's Cloak is disabled on SOTN.IO conflits with preset preloaders
    randomize_josephs_cloak(world, patch)
    # Twilight Cloak
    cape_color(world, 0x0afa44, 0x0afbac, {}, patch)
    # DOP10 Cloak. - MottZilla
    cape_color(world, 0x627984c, 0x6279850, {}, patch)
    # DOP40 Cloak. - MottZilla
    cape_color(world, 0x6894054, 0x6894058, {}, patch)


def randomize_dracula_cape(world: "SotnWorld", patch: SotnProcedurePatch):
    dracula_cape_pallete_count = 8
    color_dc = math.floor(world.random.random() * dracula_cape_pallete_count)
    offset = 0x535d4ea
    palettes_dracula_cape = [
        [0x9c21, 0xbc42, 0xd0a1],  # Blue
        [0x8d03, 0x8a23, 0x82e7],  # Green
        [0x8008, 0x8011, 0x801C],  # Default red
        [0x9448, 0xd492, 0xd93b],  # Pink
        [0x8d2d, 0x9a36, 0x9bbd],  # Yellow
        [0xa129, 0xb231, 0xdb39],  # Gray
        [0x9422, 0xa826, 0xb867],  # Purple
        [0x8000, 0x8821, 0x8c63]   # Black
    ]
    if color_dc >= dracula_cape_pallete_count:
        color_dc = 0
    for i in range(3):
        patch.write_token(APTokenTypes.WRITE, offset, palettes_dracula_cape[color_dc][i].to_bytes(2, "little"))
        offset += 2


def randomize_hydro_storm_color(world: "SotnWorld", patch: SotnProcedurePatch):
    color_1 = math.floor(world.random.random() * 0x100)
    color_2 = math.floor(world.random.random() * 0x100)
    color_3 = math.floor(world.random.random() * 0x100)
    color_4 = math.floor(world.random.random() * 0x100)
    color_5 = math.floor(world.random.random() * 0x100)
    patch.write_token(APTokenTypes.WRITE, 0x3A19544, struct.pack("<B", color_1))
    patch.write_token(APTokenTypes.WRITE, 0x3A19550, struct.pack("<B", color_2))
    patch.write_token(APTokenTypes.WRITE, 0x3A19558, struct.pack("<B", color_3))
    patch.write_token(APTokenTypes.WRITE, 0x3A19560, struct.pack("<B", color_4))
    patch.write_token(APTokenTypes.WRITE, 0x3A19568, struct.pack("<B", color_5))


def randomize_grav_boot_colors(world: "SotnWorld", patch: SotnProcedurePatch):
    # Base game has 2 bytes that it can set for a0 and a1
    # set at 0x8011e1ac and 0x8011e1b0
    color_1 = math.floor(world.random.random() * 0x100)
    patch.write_token(APTokenTypes.WRITE, 0x13C814, struct.pack("<B", color_1))
    color_2 = math.floor(world.random.random() * 0x100)
    patch.write_token(APTokenTypes.WRITE, 0x13C818, struct.pack("<B", color_2))
    prim_write_address_start = 0x13C82A
    # Iterate through 12 values (r,g,and b for 4 prim corners)
    for i in range(12):
        # Select one color. 0x60 means 0, 0x64 is color1, 0x65 is color2
        selection_index = math.floor(world.random.random() * 3)
        selection_bytes = [0x60, 0x64, 0x65][selection_index]
        # Go to the proper byte within the sb instruction and change which register writes
        target_address = prim_write_address_start + i * 4
        patch.write_token(APTokenTypes.WRITE, target_address, struct.pack("<B", selection_bytes))


# Wing smash uses a palette pulled from the GPU
# By default, this is palette #0x8102 (see EntityWingSmashTrail in decomp)
# Keep the 0x8100, but change the lower byte to pick a random palette
# This write is to 8011e438 at runtime
def randomize_wing_smash_color(world: "SotnWorld", patch: SotnProcedurePatch):
    # Index 0 in most cluts is transparent. In some it is not. In these non-transparent cluts, we won't
    # get a recolored wing smash outline and will instead get an ugly rectangle, since all the pixels
    # that are supposed to be transparent won't be. These CLUTS were identified by python script as having
    # a non-transparent index 0. If we get one of them, we will re-roll the palette

    # Dev note: The bad palettes were not "removed" by that Python script. This has been revised to use a
    # combination of the two methods. -eldri7ch
    good_cluts = [
        0, 1, 3, 4, 5, 6, 7, 9, 13, 28, 40, 80, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104,
        105, 106, 107, 108, 109, 110, 111, 112, 118, 129, 130, 131, 132, 133, 134, 135, 136, 151, 152, 154, 156, 160,
        163, 168, 174, 241, 242, 243, 245, 249, 254
    ]

    new_palette = math.floor(world.random.random() * 0x100)
    new_outline = math.floor(world.random.random() * 0x10000)

    if new_palette in good_cluts:
        # define new palette if it's a good palette
        patch.write_token(APTokenTypes.WRITE, 0x13caa0, struct.pack("<B", new_palette))
    else:
        # otherwise use a new color for the outline
        patch.write_token(APTokenTypes.WRITE, 0xef990, new_outline.to_bytes(2, "little"))


def randomize_richter_color(world: "SotnWorld", patch: SotnProcedurePatch):
    richter_palette_count = 5
    color_r = math.floor(world.random.random() * richter_palette_count)
    richter_offset = [  # Offsets for the pause UI during Prologue
        0x38BE9EA, 0x38BEA0A, 0x38BEA2A, 0x38BEA4A, 0x38BEA6A, 0x38BEAAA, 0x38BEACA, 0x38BEAEA, 0x38BEB0A, 0x38BEB2A,
        0x38BEB4A, 0x38BEB6A
    ]
    palettes_richter = [
        [0x0000, 0x8000, 0xb185, 0xc210, 0xd294, 0xf39c, 0xfd80, 0xb000, 0x80ac, 0x9556, 0xb21c, 0xc29c, 0xd33c, 0x8194,
         0xfc00, 0x801f],  # Blue
        [0x0000, 0x8000, 0xb185, 0xc210, 0xd294, 0xf39c, 0xaa80, 0x8080, 0x80ac, 0x9556, 0xb21c, 0xc29c, 0xd33c, 0x8194,
         0x8180, 0xfc1f],  # Green
        [0x0000, 0x8000, 0xa906, 0xbd8d, 0xdab6, 0xffff, 0x801e, 0x8009, 0x80cd, 0x9956, 0xbe7f, 0xcedf, 0xdb7f, 0x81f2,
         0x8013, 0x83e0],  # Red
        [0x0000, 0x8000, 0xa906, 0xbd8d, 0xdab6, 0xffff, 0xa4e9, 0x9402, 0x80cd, 0x9956, 0xbe7f, 0xcedf, 0xdb7f, 0x81f2,
         0x94a2, 0xff80],  # Black
        [0x0000, 0x8000, 0xB185, 0xC210, 0xD294, 0xF39C, 0xFD97, 0xB007, 0xB04C, 0x9556, 0xB21C, 0xC29C, 0xD33C, 0x8194,
         0xFC10, 0x801F]  # Purple (MottZilla)
    ]
    if color_r >= richter_palette_count:
        color_r = 0
    offset = 0x38BED78  # Richter's main palette
    for i in range(16):
        patch.write_token(APTokenTypes.WRITE, offset, palettes_richter[color_r][i].to_bytes(2, "little"))
        offset += 2
    offset = 0x38BEED8  # Richter's alternate palettes when using item crash
    for i in range(16):
        patch.write_token(APTokenTypes.WRITE, offset, palettes_richter[color_r][i].to_bytes(2, "little"))
        offset += 2
    for i in range(16):
        patch.write_token(APTokenTypes.WRITE, offset, palettes_richter[color_r][i].to_bytes(2, "little"))
        offset += 2
    for i in range(16):
        patch.write_token(APTokenTypes.WRITE, offset, palettes_richter[color_r][i].to_bytes(2, "little"))
        offset += 2
    for i in range(16):
        patch.write_token(APTokenTypes.WRITE, offset, palettes_richter[color_r][i].to_bytes(2, "little"))
        offset += 2
    offset = 0x436BA9C  # Richter's palette for ending cutscene
    for i in range(16):
        patch.write_token(APTokenTypes.WRITE, offset, palettes_richter[color_r][i].to_bytes(2, "little"))
        offset += 2
    offset = 0x562266C  # Richter's palette for saving Richter cutscene
    for i in range(16):
        patch.write_token(APTokenTypes.WRITE, offset, palettes_richter[color_r][i].to_bytes(2, "little"))
        offset += 2
    offset = 0x63CD658  # Richter's palette for his Boss Fight
    for i in range(16):
        patch.write_token(APTokenTypes.WRITE, offset, palettes_richter[color_r][i].to_bytes(2, "little"))
        offset += 2
    offset = 0x63CD7B8  # Richter's alternate paletts when using item crashes during Boss Fight
    for i in range(16):
        patch.write_token(APTokenTypes.WRITE, offset, palettes_richter[color_r][i].to_bytes(2, "little"))
        offset += 2
    for i in range(16):
        patch.write_token(APTokenTypes.WRITE, offset, palettes_richter[color_r][i].to_bytes(2, "little"))
        offset += 2
    for i in range(16):
        patch.write_token(APTokenTypes.WRITE, offset, palettes_richter[color_r][i].to_bytes(2, "little"))
        offset += 2
    for i in range(16):
        patch.write_token(APTokenTypes.WRITE, offset, palettes_richter[color_r][i].to_bytes(2, "little"))
        offset += 2
    offset = 0x6113772  # Richter's Colosseum cutscene
    patch.write_token(APTokenTypes.WRITE, offset, palettes_richter[color_r][14].to_bytes(2, "little"))
    offset += 2
    patch.write_token(APTokenTypes.WRITE, offset, palettes_richter[color_r][7].to_bytes(2, "little"))
    offset += 2
    patch.write_token(APTokenTypes.WRITE, offset, palettes_richter[color_r][6].to_bytes(2, "little"))
    offset = 0x38BE9EA  # Richter's pause UI
    for i in range(12):
        patch.write_token(APTokenTypes.WRITE, richter_offset[i], palettes_richter[color_r][14].to_bytes(2, "little"))
    offset = 0x38BEA1A  # Richter's Health Bar
    patch.write_token(APTokenTypes.WRITE, offset, palettes_richter[color_r][6].to_bytes(2, "little"))
    offset += 2
    patch.write_token(APTokenTypes.WRITE, offset, palettes_richter[color_r][14].to_bytes(2, "little"))
    offset += 2
    patch.write_token(APTokenTypes.WRITE, offset, palettes_richter[color_r][7].to_bytes(2, "little"))


def randomize_maria_color(world: "SotnWorld", patch: SotnProcedurePatch):
    maria_palette_count = 6
    color_m = math.floor(world.random.random() * maria_palette_count)
    palettes_maria = [
        [0x0000, 0x84c9, 0x8d53, 0xa1f9, 0xb6fc, 0x8180, 0x8280, 0xab2a, 0x9218, 0x931f, 0x9463, 0x9ce7, 0xb148, 0xca2e,
         0xe2f6, 0xef7b],  # Default
        [0x0000, 0x84c9, 0x8d53, 0xa1f9, 0xb6fc, 0xb0a0, 0xd120, 0xe62a, 0x9218, 0x931f, 0x9463, 0x9ce7, 0xb148, 0xca2e,
         0xe2f6, 0xef7b],  # Blue
        [0x0000, 0xb04c, 0x8d53, 0xb1f9, 0xcafd, 0xb4f3, 0xbd9a, 0xd1de, 0x9218, 0x931f, 0xa488, 0x9ce7, 0xb1a7, 0xca2e,
         0xe2f6, 0xef7b],  # Pink
        [0x0000, 0xb50a, 0x8d53, 0xa1f9, 0xb6fc, 0xde04, 0xd6e3, 0xeb49, 0x9218, 0x931f, 0xb486, 0xb50a, 0xbd69, 0xd26d,
         0xe2f6, 0xef7b],  # Light blue
        [0x0000, 0x84c9, 0x950f, 0xa1f9, 0xb6fc, 0x9c64, 0x98c8, 0xa906, 0x9218, 0x931f, 0x9463, 0x9ce7, 0xa906, 0xb9ac,
         0xd6b2, 0xef7b],  # Black
        [0x0000, 0xb04c, 0x8d53, 0xa9b8, 0xc29c, 0xbc49, 0xd06f, 0xf8b1, 0x9218, 0x931f, 0x9463, 0x9ce7, 0xb1a7, 0xca2e,
         0xe2f6, 0xef7b]   # Purple
    ]
    if color_m >= maria_palette_count:
        color_m = 0
    offset = 0x436BA7C  # Ending Cutscene
    for i in range(16):
        patch.write_token(APTokenTypes.WRITE, offset, palettes_maria[color_m][i].to_bytes(2, "little"))
        offset += 2
    offset = 0x45638F4  # Holy Glasses Cutscene
    for i in range(16):
        patch.write_token(APTokenTypes.WRITE, offset, palettes_maria[color_m][i].to_bytes(2, "little"))
        offset += 2
    offset = 0x4690EE4  # Silver Ring Cutscene
    for i in range(16):
        patch.write_token(APTokenTypes.WRITE, offset, palettes_maria[color_m][i].to_bytes(2, "little"))
        offset += 2
    offset = 0x54CA704
    for i in range(16):
        patch.write_token(APTokenTypes.WRITE, offset, palettes_maria[color_m][i].to_bytes(2, "little"))
        offset += 2
    offset = 0x562220C  # Save Richter Cutscene
    for i in range(16):
        patch.write_token(APTokenTypes.WRITE, offset, palettes_maria[color_m][i].to_bytes(2, "little"))
        offset += 2
    offset = 0x631620C  # Hippogriff Cutscene
    for i in range(16):
        patch.write_token(APTokenTypes.WRITE, offset, palettes_maria[color_m][i].to_bytes(2, "little"))
        offset += 2
    offset = 0x650E768  # Clock Room Cutscene
    for i in range(16):
        patch.write_token(APTokenTypes.WRITE, offset, palettes_maria[color_m][i].to_bytes(2, "little"))
        offset += 2


def disable_nz1_puzzle(patch: SotnProcedurePatch):
    # Clock tower puzzle 180fd0 = 0f Change 1a8a64: and r3, r5 to 3403000f mov r3, 0x0f @ROM 0x055a0f4c
    # Reverse clock tower puzzle 180f6c = 0f Change 1a8350: and r2, r3 to 3402000f mov r2, 0x0f @ ROM 0x059e928
    patch.write_token(APTokenTypes.WRITE, 0x055a0f4c, (0x3403000f).to_bytes(4, "little"))
    patch.write_token(APTokenTypes.WRITE, 0x059e9328, (0x3402000f).to_bytes(4, "little"))


def randomize_music(world: "SotnWorld", patch: SotnProcedurePatch):
    music_list = list(music_by_area.values())
    song_src = list(music.values())

    song_pool = song_src.copy()
    while len(song_pool) < len(music_list):
        song_pool.append(world.random.choice(song_src))

    world.random.shuffle(song_pool)

    for zone in music_list:
        rand_song = song_pool.pop()
        for addr in zone:
            patch.write_token(APTokenTypes.WRITE, addr, struct.pack("<B", rand_song))


def rlib_card(patch: SotnProcedurePatch):
    # Patch the reverse library card function
    offset = 0x12b534  # Hook to our new LBC function
    patch.write_token(APTokenTypes.WRITE, offset, (0x0c02622f).to_bytes(4, "little"))
    # No "nop" instr needed as it's already a call

    # Function to call when using library card. Thanks eldrich for some direction
    offset = 0x3711a74
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x08026243).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    offset = 0x3711ac4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x3c028004).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x9045925d).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x38a500ff).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x30a50040).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x10a00008).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x3c028007).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x9042bbfb).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x10400004).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x34180022).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x341988be).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x18000003).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x34180002).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x34197c0e).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x3c02800f).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0xa0581724).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x3b180020).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0xa05832a4).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x3c02800a).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0xa4593c98).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x34040000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x0804390b).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x03e00008).to_bytes(4, "little"))
    offset += 4


def rando_func_master(opt_write: int, patch: SotnProcedurePatch) -> None:
    offset = 0xF96D8
    patch.write_token(APTokenTypes.WRITE, offset, (0x0c038ba6).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    offset += 4

    offset = 0xF87B0
    patch.write_token(APTokenTypes.WRITE, offset, (0x3C01800A).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0xAC208850).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x27BDFFE0).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x3C020026).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x34422905).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x34040002).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x27A50010).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x34060000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0xAFBF0018).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x0C006578).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0xAFA20010).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x3404000E).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x3C058009).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x34A588B0).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x0C007020).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x34060080).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x34040000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x0C007062).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x34050000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x34020000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x8FBF0018).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x27BD0020).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x03E00008).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))

    offset = 0x3711A68

    patch.write_token(APTokenTypes.WRITE, offset, opt_write.to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x08026231).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x08026243).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x27BDFFE0).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0xAFBF0010).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x0C03C182).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x3C048009).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x348488B0).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x8C860000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x3C058000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x34A50000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00C53024).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x10C00003).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x0C02625D).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x8FBF000A).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x27BD0020).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x03E00008).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x3C028004).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x9045925D).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x38A500FF).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x30A50040).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x10A00008).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x3C028007).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x9042BBFB).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x10400004).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x34180022).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x341988BE).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x18000003).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x34180002).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x34197C0E).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x3C02800F).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0xA0581724).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x3B180020).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0xA05832A4).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x3C02800A).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0xA4593C98).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x34040000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x0804390B).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x03E00008).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    offset += 4


def modify_drop(drop_mod: int, patch: SotnProcedurePatch):
    if drop_mod == 3:
        nop_line = 0x00000000
        always_drop = 0x1800000D

        # Patch drops to always be items
        offset = 0x440413c  # Colosseum
        patch.write_token(APTokenTypes.WRITE, offset, nop_line.to_bytes(4, "little"))  # Removes failures
        offset += 0x1c
        patch.write_token(APTokenTypes.WRITE, offset, nop_line.to_bytes(4, "little"))  # Removes second roll failures
        offset += 0x10
        patch.write_token(APTokenTypes.WRITE, offset, always_drop.to_bytes(4, "little"))  # Forces an item drop

        offset = 0x44d514c  # Catacombs
        patch.write_token(APTokenTypes.WRITE, offset, nop_line.to_bytes(4, "little"))
        offset += 0x2c
        patch.write_token(APTokenTypes.WRITE, offset, always_drop.to_bytes(4, "little"))

        offset = 0x460c4bc  # Abandoned Mine
        patch.write_token(APTokenTypes.WRITE, offset, nop_line.to_bytes(4, "little"))
        offset += 0x2c
        patch.write_token(APTokenTypes.WRITE, offset, always_drop.to_bytes(4, "little"))

        offset = 0x46c78f0  # Royal Chapel
        patch.write_token(APTokenTypes.WRITE, offset, nop_line.to_bytes(4, "little"))
        offset += 0x2c
        patch.write_token(APTokenTypes.WRITE, offset, always_drop.to_bytes(4, "little"))

        offset = 0x47eb5d8  # Long Library
        patch.write_token(APTokenTypes.WRITE, offset, nop_line.to_bytes(4, "little"))
        offset += 0x2c
        patch.write_token(APTokenTypes.WRITE, offset, always_drop.to_bytes(4, "little"))

        offset = 0x4948630  # Marble Gallery
        patch.write_token(APTokenTypes.WRITE, offset, nop_line.to_bytes(4, "little"))
        offset += 0x2c
        patch.write_token(APTokenTypes.WRITE, offset, always_drop.to_bytes(4, "little"))

        offset = 0x4a1e258  # Outer Wall
        patch.write_token(APTokenTypes.WRITE, offset, nop_line.to_bytes(4, "little"))
        offset += 0x2c
        patch.write_token(APTokenTypes.WRITE, offset, always_drop.to_bytes(4, "little"))

        offset = 0x4ae259c  # Olrox's Quarters
        patch.write_token(APTokenTypes.WRITE, offset, nop_line.to_bytes(4, "little"))
        offset += 0x2c
        patch.write_token(APTokenTypes.WRITE, offset, always_drop.to_bytes(4, "little"))

        offset = 0x4bb2de4  # Entrance(2nd)
        patch.write_token(APTokenTypes.WRITE, offset, nop_line.to_bytes(4, "little"))
        offset += 0x2c
        patch.write_token(APTokenTypes.WRITE, offset, always_drop.to_bytes(4, "little"))

        offset = 0x4c871b8  # Underground Caverns
        patch.write_token(APTokenTypes.WRITE, offset, nop_line.to_bytes(4, "little"))
        offset += 0x2c
        patch.write_token(APTokenTypes.WRITE, offset, always_drop.to_bytes(4, "little"))

        offset = 0x4d36fa8  # Floating Catacombs
        patch.write_token(APTokenTypes.WRITE, offset, nop_line.to_bytes(4, "little"))
        offset += 0x2c
        patch.write_token(APTokenTypes.WRITE, offset, always_drop.to_bytes(4, "little"))

        offset = 0x4dc486c  # Cave
        patch.write_token(APTokenTypes.WRITE, offset, nop_line.to_bytes(4, "little"))
        offset += 0x2c
        patch.write_token(APTokenTypes.WRITE, offset, always_drop.to_bytes(4, "little"))

        offset = 0x4e6ea24  # Anti-Chapel
        patch.write_token(APTokenTypes.WRITE, offset, nop_line.to_bytes(4, "little"))
        offset += 0x2c
        patch.write_token(APTokenTypes.WRITE, offset, always_drop.to_bytes(4, "little"))

        offset = 0x4f0b388  # Forbidden Library
        patch.write_token(APTokenTypes.WRITE, offset, nop_line.to_bytes(4, "little"))
        offset += 0x2c
        patch.write_token(APTokenTypes.WRITE, offset, always_drop.to_bytes(4, "little"))

        offset = 0x4fc540c  # Black Marble Gallery
        patch.write_token(APTokenTypes.WRITE, offset, nop_line.to_bytes(4, "little"))
        offset += 0x2c
        patch.write_token(APTokenTypes.WRITE, offset, always_drop.to_bytes(4, "little"))

        offset = 0x50808a4  # Reverse Outer Wall
        patch.write_token(APTokenTypes.WRITE, offset, nop_line.to_bytes(4, "little"))
        offset += 0x2c
        patch.write_token(APTokenTypes.WRITE, offset, always_drop.to_bytes(4, "little"))

        offset = 0x5137bc8  # Death Wing's Lair
        patch.write_token(APTokenTypes.WRITE, offset, nop_line.to_bytes(4, "little"))
        offset += 0x2c
        patch.write_token(APTokenTypes.WRITE, offset, always_drop.to_bytes(4, "little"))

        offset = 0x51e95a8  # Reverse Entrance
        patch.write_token(APTokenTypes.WRITE, offset, nop_line.to_bytes(4, "little"))
        offset += 0x2c
        patch.write_token(APTokenTypes.WRITE, offset, always_drop.to_bytes(4, "little"))

        offset = 0x52c0e2c  # Reverse Caverns
        patch.write_token(APTokenTypes.WRITE, offset, nop_line.to_bytes(4, "little"))
        offset += 0x2c
        patch.write_token(APTokenTypes.WRITE, offset, always_drop.to_bytes(4, "little"))

        offset = 0x5437344  # Entrance(1st)
        patch.write_token(APTokenTypes.WRITE, offset, nop_line.to_bytes(4, "little"))
        offset += 0x2c
        patch.write_token(APTokenTypes.WRITE, offset, always_drop.to_bytes(4, "little"))

        offset = 0x54f3cdc  # Alchemy Laboratory
        patch.write_token(APTokenTypes.WRITE, offset, nop_line.to_bytes(4, "little"))
        offset += 0x2c
        patch.write_token(APTokenTypes.WRITE, offset, always_drop.to_bytes(4, "little"))

        offset = 0x55a6968  # Clock Tower
        patch.write_token(APTokenTypes.WRITE, offset, nop_line.to_bytes(4, "little"))
        offset += 0x2c
        patch.write_token(APTokenTypes.WRITE, offset, always_drop.to_bytes(4, "little"))

        offset = 0x5643ce8  # Castle Keep
        patch.write_token(APTokenTypes.WRITE, offset, nop_line.to_bytes(4, "little"))
        offset += 0x2c
        patch.write_token(APTokenTypes.WRITE, offset, always_drop.to_bytes(4, "little"))

        offset = 0x577e4b8  # Reverse Colosseum
        patch.write_token(APTokenTypes.WRITE, offset, nop_line.to_bytes(4, "little"))
        offset += 0x2c
        patch.write_token(APTokenTypes.WRITE, offset, always_drop.to_bytes(4, "little"))

        offset = 0x580836c  # Reverse Keep
        patch.write_token(APTokenTypes.WRITE, offset, nop_line.to_bytes(4, "little"))
        offset += 0x2c
        patch.write_token(APTokenTypes.WRITE, offset, always_drop.to_bytes(4, "little"))

        offset = 0x5936c4c  # Necromancy Laboratory
        patch.write_token(APTokenTypes.WRITE, offset, nop_line.to_bytes(4, "little"))
        offset += 0x2c
        patch.write_token(APTokenTypes.WRITE, offset, always_drop.to_bytes(4, "little"))

        offset = 0x59efe78  # Reverse Clock Tower
        patch.write_token(APTokenTypes.WRITE, offset, nop_line.to_bytes(4, "little"))
        offset += 0x2c
        patch.write_token(APTokenTypes.WRITE, offset, always_drop.to_bytes(4, "little"))

        # Alternate between Rare and Uncommon Drops based on Kill Count - MottZilla
        offset = 0x119188  # PSX MainRam 800FF4C0h
        patch.write_token(APTokenTypes.WRITE, offset, (0x3c068009).to_bytes(4, "little"))  # mov r6,80090000h
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x34c67bf4).to_bytes(4, "little"))  # or r6,7BF4h
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x8cc20000).to_bytes(4, "little"))  # mov r2,[r6]
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x30420001).to_bytes(4, "little"))  # and r2,1h
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x14400004).to_bytes(4, "little"))  # jnz r2,800FF4E8h
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x34020020).to_bytes(4, "little"))  # mov r2,20h
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x0803fd7a).to_bytes(4, "little"))  # jmp 800FF5E8h
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x34020040).to_bytes(4, "little"))  # mov r2,40h
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x0803fd7a).to_bytes(4, "little"))  # jmp 800FF5E8h
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
    else:
        for k, enemy in enemy_dict.items():
            if enemy in ["Stone skull", "Slime", "Large slime", "Poltergeist", "Puppet sword", "Shield", "Spear", "Ball"]:
                continue

            if "drop_rate" in enemy:
                try:
                    address = enemy["drop_addresses"][0] + 4
                    drop_rare_new = 64 * drop_mod
                    patch.write_token(APTokenTypes.WRITE, address, drop_rare_new.to_bytes(2, "little"))
                except IndexError:
                    pass
                try:
                    address = enemy["drop_addresses"][1] + 4
                    drop_common_new = 32 * drop_mod
                    patch.write_token(APTokenTypes.WRITE, address, drop_common_new.to_bytes(2, "little"))
                except IndexError:
                    pass


def start_room_rando(castle_flag: int, world: "SotnWorld", patch: SotnProcedurePatch):
    room_keys = list(start_room_data.keys())
    rand_room_key = world.random.choice(room_keys)
    rand_room = start_room_data[rand_room_key]

    if castle_flag == 1:  # 1st castle only
        while rand_room["stage"] >= 20:
            rand_room_key = world.random.choice(room_keys)
            rand_room = start_room_data[rand_room_key]
    elif castle_flag == 2:  # 2nd castle only
        while rand_room["stage"] <= 20:
            rand_room_key = world.random.choice(room_keys)
            rand_room = start_room_data[rand_room_key]

    # Not sure if this prevents logic breaking for SOTN.IO
    if rand_room["stage"] >= 0x20:
        offset = 0xf0230
        patch.write_token(APTokenTypes.WRITE, offset, (0x3C028009).to_bytes(4, "little"))
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x8C4274A0).to_bytes(4, "little"))
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x30420020).to_bytes(4, "little"))
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x1040000E).to_bytes(4, "little"))
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x3C028007).to_bytes(4, "little"))
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x9042BBFB).to_bytes(4, "little"))
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x14400009).to_bytes(4, "little"))
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x3C028007).to_bytes(4, "little"))
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x9042BCC0).to_bytes(4, "little"))
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x14400004).to_bytes(4, "little"))
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x34020001).to_bytes(4, "little"))
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x03E00008).to_bytes(4, "little"))
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x0803F8EA).to_bytes(4, "little"))
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))

        # Hooks
        offset = 0x12C7B0
        patch.write_token(APTokenTypes.WRITE, offset, (0x6E6E).to_bytes(2, "little"))
        offset = 0x12CB00
        patch.write_token(APTokenTypes.WRITE, offset, (0x6E6E).to_bytes(2, "little"))
        # Disable Richter Cutscene
        offset = 0x5641220
        patch.write_token(APTokenTypes.WRITE, offset, (0x34020001).to_bytes(4, "little"))
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))

        # Patch Zone with Hatch Entity (required for 2nd to work)
        offset = 0x4BA934C
        patch.write_token(APTokenTypes.WRITE, offset, (0x34040020).to_bytes(4, "little"))  # mov r4,20h
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x3C058009).to_bytes(4, "little"))  # mov r5,80090000h
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0xACA474A0).to_bytes(4, "little"))  # mov [r5+74a0h],r4
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x0806E92B).to_bytes(4, "little"))  # jmp 801BA4ACh
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))  # nop
        offset += 4

    offset = 0x4b6ab0c
    patch.write_token(APTokenTypes.WRITE, offset, (0x28042804).to_bytes(4, "little"))  # Setting up the CD room
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x34000015).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x28052805).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x0000ff64).to_bytes(4, "little"))

    offset = 0x4b66a44
    patch.write_token(APTokenTypes.WRITE, offset, struct.pack("<B", 0x04))
    offset += 1
    patch.write_token(APTokenTypes.WRITE, offset, struct.pack("<B", 0x4a))
    offset += 1
    patch.write_token(APTokenTypes.WRITE, offset, struct.pack("<B", 0x00))
    offset += 1
    patch.write_token(APTokenTypes.WRITE, offset, struct.pack("<B", 0x41))
    offset += 1
    patch.write_token(APTokenTypes.WRITE, offset, struct.pack("<B", 0x64))

    offset = 0xae95c  # change the destination
    new_write = rand_room["xyWrite"]  # Write X,Y Position
    patch.write_token(APTokenTypes.WRITE, offset, new_write.to_bytes(4, "little"))
    offset += 4

    new_write = rand_room["roomWrite"]  # Write Rooms Used
    patch.write_token(APTokenTypes.WRITE, offset, new_write.to_bytes(4, "little"))
    offset += 4

    new_write = rand_room["stageWrite"]  # Write destination stage Used
    patch.write_token(APTokenTypes.WRITE, offset, new_write.to_bytes(4, "little"))
    offset += 4

    if new_write == 0x03 or new_write == 0x05:
        offset = 0x45f55a2  # Solve soft lock if player starts near Room 0 in Abandoned Mines
        patch.write_token(APTokenTypes.WRITE, offset, struct.pack("<B", 0x42))
        offset += 1
        patch.write_token(APTokenTypes.WRITE, offset, struct.pack("<B", 0x03))

        offset = 0x45f52a2  # Solve soft lock if player starts near Room 0 in Abandoned Mines
        patch.write_token(APTokenTypes.WRITE, offset, struct.pack("<B", 0x42))
        offset += 1
        patch.write_token(APTokenTypes.WRITE, offset, struct.pack("<B", 0x03))

        offset = 0x45f5142  # Solve soft lock if player starts near Room 0 in Abandoned Mines
        patch.write_token(APTokenTypes.WRITE, offset, struct.pack("<B", 0x42))
        offset += 1
        patch.write_token(APTokenTypes.WRITE, offset, struct.pack("<B", 0x03))

        offset = 0x45f4eec  # Solve soft lock if player starts near Room 0 in Abandoned Mines
        patch.write_token(APTokenTypes.WRITE, offset, struct.pack("<B", 0x42))
        offset += 1
        patch.write_token(APTokenTypes.WRITE, offset, struct.pack("<B", 0x03))

        offset = 0x45f67bc  # Solve soft lock if player starts near Room 3 in Abandoned Mines
        patch.write_token(APTokenTypes.WRITE, offset, struct.pack("<B", 0x67))
        offset += 1
        patch.write_token(APTokenTypes.WRITE, offset, struct.pack("<B", 0x00))
        offset += 1
        patch.write_token(APTokenTypes.WRITE, offset, struct.pack("<B", 0x68))
        offset += 1
        patch.write_token(APTokenTypes.WRITE, offset, struct.pack("<B", 0x00))

        offset = 0x45f65dc  # Solve soft lock if player starts near Room 3 in Abandoned Mines
        patch.write_token(APTokenTypes.WRITE, offset, struct.pack("<B", 0x23))

        offset = 0x45f655a  # Solve soft lock if player starts near Room 3 in Abandoned Mines
        patch.write_token(APTokenTypes.WRITE, offset, struct.pack("<B", 0x68))
        offset += 1
        patch.write_token(APTokenTypes.WRITE, offset, struct.pack("<B", 0x00))

        offset = 0x45f64dc  # Solve soft lock if player starts near Room 3 in Abandoned Mines
        patch.write_token(APTokenTypes.WRITE, offset, struct.pack("<B", 0x42))
        offset += 1
        patch.write_token(APTokenTypes.WRITE, offset, struct.pack("<B", 0x03))

        offset = 0x45f644e  # Solve soft lock if player starts near Room 3 in Abandoned Mines
        patch.write_token(APTokenTypes.WRITE, offset, struct.pack("<B", 0x67))
        offset += 1
        patch.write_token(APTokenTypes.WRITE, offset, struct.pack("<B", 0x00))
        offset += 1
        patch.write_token(APTokenTypes.WRITE, offset, struct.pack("<B", 0x68))
        offset += 1
        patch.write_token(APTokenTypes.WRITE, offset, struct.pack("<B", 0x00))

        offset = 0x45f6168  # Solve soft lock if player starts near Room 3 in Abandoned Mines
        patch.write_token(APTokenTypes.WRITE, offset, struct.pack("<B", 0xda))
        offset += 1
        patch.write_token(APTokenTypes.WRITE, offset, struct.pack("<B", 0x01))

        # Solve soft lock if player starts near Room 8 in Abandoned Mines
        patch.write_token(APTokenTypes.WRITE, 0x45f8de2, (0x03430342).to_bytes(4, "little"))
        patch.write_token(APTokenTypes.WRITE, 0x45f8a92, (0x0342).to_bytes(2, "little"))
        patch.write_token(APTokenTypes.WRITE, 0x45f897c, (0x0343).to_bytes(2, "little"))
        patch.write_token(APTokenTypes.WRITE, 0x45f879a, (0x03430342).to_bytes(4, "little"))


def randomize_shop(min_value: int, max_value: int, randomize_items: int, world: "SotnWorld",
                   patch: SotnProcedurePatch) -> None:
    new_min = 50
    new_max = 150
    new_shop_prices = []
    new_shop_stock = []
    new_shop_value = []
    forbid_items = [169, 195, 217, 226]

    if randomize_items >= 3:
        forbid_items = [169, 183, 195, 203, 217, 226, 241, 242]

    if min_value > 0:
        new_min = min_value
    if max_value > 0:
        new_max = max_value

    for item_id, item in shop_item_data.items():
        if min_value > 0 or max_value > 0:
            new_price = world.random.randint(new_min, new_max)
            new_shop_prices.append(new_price)

        if item_id == 1 and (randomize_items == 2 or randomize_items == 4):
            new_shop_stock.append(166)
            new_shop_value.append(0x00)
        elif randomize_items != 0:
            new_item = 0
            type_value = 0x00
            while new_item == 0 or new_item in new_shop_stock:
                new_item = world.random.choice([i for i in range(1, 259) if i not in forbid_items])
            item = id_to_item[new_item]
            if item["type"] == "HELMET":
                type_value = 0x01
            elif item["type"] == "ARMOR":
                type_value = 0x02
            elif item["type"] == "CLOAK":
                type_value = 0x03
            elif item["type"] == "ACCESSORY":
                type_value = 0x04
            new_shop_stock.append(new_item)
            new_shop_value.append(type_value)

    world.random.shuffle(new_shop_prices)

    for item_id, item in shop_item_data.items():
        item_price = item["itemPriceD"]
        item_address = item["priceAddress"]
        if min_value > 0 or max_value > 0:
            new_price = new_shop_prices.pop()
            rng_price = int(item_price * (new_price / 100))
            patch.write_token(APTokenTypes.WRITE, item_address, rng_price.to_bytes(4, "little"))

        if randomize_items != 0:
            new_item = new_shop_stock.pop(0)
            type_value = new_shop_value.pop(0)
            offset = -0xa9
            if type_value == 0x00:
                offset = 0x00
            patch.write_token(APTokenTypes.WRITE, item_address - 4, struct.pack("<B", type_value))
            patch.write_token(APTokenTypes.WRITE, item_address - 2, (new_item + offset).to_bytes(2, "little"))


def enemy_stat_rando(new_mod: float, enemy_stat: bool, world: "SotnWorld", patch: SotnProcedurePatch):
    for enemy in enemy_stats_list:
        stat_hp = enemy["hpValue"]
        stat_atk = enemy["atkValue"]
        stat_def = enemy["defValue"]

        if new_mod != 0:
            new_hp = int(round(new_mod * stat_hp))
            new_atk = int(round(new_mod * stat_atk))
            new_def = int(round(new_mod * stat_def))
        else:
            new_hp = enemy_num_stat_rand(world, stat_hp)
            new_atk = enemy_num_stat_rand(world, stat_atk)
            new_def = enemy_num_stat_rand(world, stat_def)

        patch.write_token(APTokenTypes.WRITE, enemy["hpOffset"], new_hp.to_bytes(2, "little"))
        patch.write_token(APTokenTypes.WRITE, enemy["atkOffset"], new_atk.to_bytes(2, "little"))
        patch.write_token(APTokenTypes.WRITE, enemy["defOffset"], new_def.to_bytes(2, "little"))

        if enemy["id"] == 379:
            stat_atk = 70
            new_atk = enemy_num_stat_rand(world, stat_atk)
            patch.write_token(APTokenTypes.WRITE, 0x0b9c0e, new_atk.to_bytes(2, "little"))
            stat_def = 20
            new_def = enemy_num_stat_rand(world, stat_def)
            patch.write_token(APTokenTypes.WRITE, 0x0b9c12, new_def.to_bytes(2, "little"))

        if not enemy_stat:
            continue

        new_atk_type = world.random.choice(enemy_atk_type_list)
        patch.write_token(APTokenTypes.WRITE, enemy["atkTypeOffset"], new_atk_type.to_bytes(2, "little"))
        new_weak_type = world.random.choice(enemy_weak_type_list)
        patch.write_token(APTokenTypes.WRITE, enemy["weakOffset"], new_weak_type.to_bytes(2, "little"))
        new_resist_type = enemy_resist_type_stat_rand(world)
        patch.write_token(APTokenTypes.WRITE, enemy["resistOffset"], new_resist_type.to_bytes(2, "little"))

        if enemy["id"] == 379:
            patch.write_token(APTokenTypes.WRITE, 0x0b9c10, new_atk_type.to_bytes(2, "little"))
            patch.write_token(APTokenTypes.WRITE, 0x0b9c16, new_weak_type.to_bytes(2, "little"))
            patch.write_token(APTokenTypes.WRITE, 0x0b9c18, new_resist_type.to_bytes(2, "little"))

        res_index = (world.random.uniform(0, 1) * 10) % 2 == 0
        if res_index:
            offset = enemy["guardOffset"]
            new_immune_type = enemy_resist_type_stat_rand(world)
            patch.write_token(APTokenTypes.WRITE, offset, new_immune_type.to_bytes(2, "little"))
            if enemy["id"] == 379:
                patch.write_token(APTokenTypes.WRITE, 0x0b9c1a, new_immune_type.to_bytes(2, "little"))
        else:
            offset = enemy["absorbOffset"]
            new_immune_type = enemy_resist_type_stat_rand(world)
            patch.write_token(APTokenTypes.WRITE, offset, new_immune_type.to_bytes(2, "little"))
            if enemy["id"] == 379:
                patch.write_token(APTokenTypes.WRITE, 0x0b9c1c, new_immune_type.to_bytes(2, "little"))

        disclosure_card = 'f0'
        new_disclosure = hex_value_to_damage_string(new_atk_type)
        if new_disclosure.startswith('05'):
            new_disclosure = replace_text_at_index(new_disclosure, '00', 0)
            disclosure_card += '05'
        elif new_disclosure.startswith('3f'):
            new_disclosure = replace_text_at_index(new_disclosure, '00', 0)
            disclosure_card += '3f'
        elif new_atk > stat_atk:
            disclosure_card += 'e2'
        else:
            disclosure_card += 'e6'
        disclosure_card += new_disclosure + 'f1'
        if new_def > stat_def:
            disclosure_card += 'e2'
        else:
            disclosure_card += 'e6'

        new_disclosure = hex_value_to_defence_string(new_weak_type)[-2:]
        disclosure_card += new_disclosure
        new_disclosure = hex_value_to_defence_string(new_resist_type)[-2:]
        disclosure_card += new_disclosure
        if res_index:
            disclosure_card += 'f7'
            new_disclosure = hex_value_to_defence_string(new_immune_type)[-2:]
            disclosure_card += new_disclosure
        else:
            disclosure_card += 'f6'
            new_disclosure = hex_value_to_defence_string(new_immune_type)[-2:]
            disclosure_card += new_disclosure
        disclosure_card += 'ff'
        len_disclosure = len(disclosure_card)
        for _ in range(len_disclosure, 24):
            disclosure_card += '00'
        offset = enemy["newNameText"]
        for i in range(0, len(disclosure_card), 2):
            two_chars_str = '0x' + disclosure_card[i:i+2]
            two_chars = int(two_chars_str, 16)
            patch.write_token(APTokenTypes.WRITE, offset, struct.pack("<B", two_chars))
            offset += 1
        patch.write_token(APTokenTypes.WRITE, enemy["nameOffset"], enemy["newNameReference"].to_bytes(4, "little"))

    if enemy_stat:
        offset = 0x0f6138
        normal_names = "0024524143554C41FF0027414C414D4F5448FF00F700214C4CFF00274F4F44002C55434BFF00"

        for i in range(0, len(normal_names), 2):
            two_chars_str = '0x' + normal_names[i:i+2]
            two_chars = int(two_chars_str, 16)
            patch.write_token(APTokenTypes.WRITE, offset, struct.pack("<B", two_chars))
            offset += 1

        offset = 0x0b9ca8
        patch.write_token(APTokenTypes.WRITE, offset, (0x800e0cf4).to_bytes(4, "little"))

        offset = 0x0b6220
        patch.write_token(APTokenTypes.WRITE, offset, (0x800e0cfb).to_bytes(4, "little"))

        for address in faerie_scroll_force_addresses:
            force_on = 0x34020003
            force_nop = 0x00000000
            offset = address

            patch.write_token(APTokenTypes.WRITE, offset, force_on.to_bytes(4, "little"))
            offset += 4
            patch.write_token(APTokenTypes.WRITE, offset, force_nop.to_bytes(4, "little"))


def replace_text_at_index(old_str: str, new_str: str, index: int) -> str:
    return old_str[0:index] + new_str + old_str[index + len(new_str):]


def find_required_numbers(total: int, numbers: list) -> list:
    # This returns the numbers that compose a value. For example, if the total is 12 and the possible
    # numbers are 1, 2, 4 and 8, it will return [8, 4]
    # Sort the numbers in descending order
    numbers.sort(reverse=True)

    # Initialize an array to store the result
    result = []

    # Iterate through the sorted numbers
    for number in numbers:
        if total >= number:
            # If the current number can be subtracted from the total, add it to the result
            result.append(number)
            total -= number

    # Return the list of required numbers
    return result


def get_stat_type(type_obj: dict, value: int) -> str:
    values_for_damage = find_required_numbers(value, list(type_obj.keys()))
    values_for_damage.sort()  # Sort them ascending
    value_type = ""
    for value in values_for_damage:
        value_type += type_obj[value]

    return value_type


def hex_value_to_damage_string(hex_value: int) -> str:
    # Hit types can't be combined
    hit_types = {
        0: "",  # No hit box
        1: "",  # Hit 16%
        2: "",  # Hit
        4: "",  # Cut
        5: "",  # Cut 16%
        6: "",  # Cut weak
        8: "30"  # Poison
    }

    # Hit effects can't be combined
    hit_effects = {
        0: "",  # No hit box
        1: "",  # Ignore normal attack styles
        2: "",  # Hit weak
        4: "",  # Big toss
        6: "",  # Guard
        7: "23",  # Cat
    }

    # Damage Types CAN be combined
    damage_types = {
        0: "",  # None
        1: "28",  # Holy
        2: "29",  # Ice
        4: "2c",  # Lightning
        8: "26",  # Fire
    }

    # Special Types CAN be combined
    special_types = {
        0: "",  # None
        1: "35",  # Curse
        2: "33",  # Stone
        4: "37",  # Water
        8: "24",  # Dark
    }

    hit_type_value = (hex_value >> 4) & 0xf
    hit_type = hit_types[hit_type_value]

    hit_effect_value = hex_value & 0xf
    hit_effect = hit_effects[hit_effect_value]

    damage_type_value = (hex_value >> 12) & 0xf
    damage_type = get_stat_type(damage_types, damage_type_value)

    special_type_value = (hex_value >> 8) & 0xf
    special_type = get_stat_type(special_types, special_type_value)

    return f"{hit_type}{hit_effect}{damage_type}{special_type}"


def hex_value_to_defence_string(hex_value: int) -> str:
    # Hit types can't be combined
    hit_types = {
        0: "3f",  # No resistence
        1: "",  # Hit 16%
        2: "03",  # Hit
        4: "0f",  # Cut
        5: "",  # Cut 16%
        6: "",  # Cut weak
        8: "30",  # Poison
    }

    # Hit effects can't be combined
    hit_effects = {
        0: "",  # No hit box
        1: "",  # Ignore normal attack styles
        2: "",  # Hit weak
        4: "",  # Big toss
        6: "",  # Guard
        7: "23",  # Cat
    }

    # Damage Types CAN be combined
    damage_types = {
        0: "",  # None
        1: "28",  # Holy
        2: "29",  # Ice
        4: "2c",  # Lightning
        8: "26",  # Fire
    }

    # Special Types CAN be combined
    special_types = {
        0: "",  # None
        1: "35",  # Curse
        2: "33",  # Stone
        4: "37",  # Water
        8: "24",  # Dark
    }

    hit_type_value = (hex_value >> 4) & 0xf
    hit_type = hit_types[hit_type_value]

    hit_effect_value = hex_value & 0xf
    hit_effect = hit_effects[hit_effect_value]

    damage_type_value = (hex_value >> 12) & 0xf
    damage_type = damage_types[damage_type_value]

    special_type_value = (hex_value >> 8) & 0xf
    special_type = special_types[special_type_value]

    return f"{hit_type}{hit_effect}{damage_type}{special_type}"


def enemy_resist_type_stat_rand(world: "SotnWorld") -> int:
    # We want nothing 50% of the time, and a random type all other times
    if world.random.uniform(0, 1) >= 0.5:
        return 0x0000

    type_list = [
        0x0020,  # hit
        0x0040,  # cut
        0x0080,  # poison
        0x8000,  # Fire
        0x2000,  # Ice
        0x1000,  # Holy
        0x4000,  # Lightning
        0x0100,  # Curse
        0x0200,  # Stone
        0x0800,   # Dark
    ]

    return world.random.choice(type_list)


def enemy_num_stat_rand(world: "SotnWorld", original_stat: int) -> int:
    random_number = world.random.uniform(0.25, 2.00)

    new_value = int(round(random_number * original_stat))
    return new_value


# Thanks eldri7ch
def no_prologue(patch: SotnProcedurePatch):
    # Patch from Chaos-Lite / MottZilla
    patch.write_token(APTokenTypes.WRITE, 0x04392b1c, struct.pack("<B", 0x41))

    # hook address to reset time attack
    offset = 0x00119b98
    # place hook in relic reset
    patch.write_token(APTokenTypes.WRITE, offset, (0x0803fef0).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))

    offset = 0x001199b8  # start code in richter (no use in no-prologue)
    # reset the time attack to allow bosses to spawn
    patch.write_token(APTokenTypes.WRITE, offset, (0xa0600000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x2610ffff).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x0601fffd).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x2463ffff).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x3c038003).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x3463ca28).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x3410001b).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0xac600000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x2610ffff).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x0601fffd).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x24630004).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x0803ff6c).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    offset += 4


# Researched by MottZilla & eldri7ch. Function by eldri7ch
def map_color(map_col: int, patch: SotnProcedurePatch):
    address_al = 0x03874848  # define address for Alucard maps
    address_ri = 0x038C0508  # define address for Richter maps
    address_al_bord = 0x03874864  # define address for Alucard maps borders
    address_ri_bord = 0x038C0524  # define address for Richter maps borders

    # Patch map colors - eldri7ch. WHY PYTHON DOES NOT HAVE A SWITCH/CASE??? I MISS C
    if map_col == 1:  # Dark Blue
        color_write = 0xb0000000
        patch.write_token(APTokenTypes.WRITE, address_al, color_write.to_bytes(4, "little"))
        patch.write_token(APTokenTypes.WRITE, address_ri, color_write.to_bytes(4, "little"))
    elif map_col == 2:  # Crimson
        color_write = 0x00500000
    elif map_col == 3:  # Brown
        color_write = 0x80ca0000
    elif map_col == 4:  # Dark Green
        color_write = 0x09000000
    elif map_col == 5:  # Gray
        color_write = 0xE3180000
        bord_write = 0xffff
    elif map_col == 6:  # Purple
        color_write = 0xB0080000
    elif map_col == 7:  # Pink
        color_write = 0xff1f0000
        bord_write = 0xfd0f
    elif map_col == 8:  # Black
        color_write = 0x10000000
    elif map_col == 9:  # Invisible
        color_write = 0x00000000

    try:
        patch.write_token(APTokenTypes.WRITE, address_al, color_write.to_bytes(4, "little"))
        patch.write_token(APTokenTypes.WRITE, address_ri, color_write.to_bytes(4, "little"))
    except NameError:
        pass

    try:
        patch.write_token(APTokenTypes.WRITE, address_al_bord, bord_write.to_bytes(2, "little"))
        patch.write_token(APTokenTypes.WRITE, address_ri_bord, bord_write.to_bytes(2, "little"))
    except NameError:
        pass


# Alucard Palette Randomizer - CRAZY4BLADES, palettes by eldri7ch
def alucard_palette(al_col_p: int, patch: SotnProcedurePatch):
    color_alucard_bright = 1
    palettes_alucard =\
        [
            [],                                                        # Default
            [0x8404, 0x8c28, 0x8c4c, 0xa552, 0xb9f3, 0xcad8, 0xf39c],  # Bloody Tears
            [0x9021, 0xa043, 0xb8a6, 0xc529, 0xcded, 0xcef5, 0xf39c],  # Blue Danube
            [0x8042, 0x8082, 0x80c6, 0x8d2f, 0xa9d1, 0xc6d5, 0xe39b],  # Swamp Thing
            [0x9063, 0x94a5, 0xa12a, 0xb9f0, 0xd674, 0xeb5b, 0xf39c],  # White Knight
            [0x8c02, 0x9c04, 0xac88, 0xbd0a, 0xcdad, 0xc655, 0xcf18],  # Royal Purple
            [0x9024, 0x9867, 0xa8ac, 0xbd31, 0xcdf5, 0xeabb, 0xfb1d],  # Pink Passion
            [0x8000, 0x8c42, 0x98a5, 0xa0e9, 0xa96d, 0xb9f1, 0xc655],  # Shadow Prince
        ]

    # Cloth
    offset = 0xef952
    for i in range(5):
        index = i + color_alucard_bright + 1
        patch.write_token(APTokenTypes.WRITE, offset, palettes_alucard[al_col_p][index].to_bytes(2, "little"))
        offset += 2

    # Darkest color
    offset = 0xef93e
    index = color_alucard_bright
    patch.write_token(APTokenTypes.WRITE, offset, palettes_alucard[al_col_p][index].to_bytes(2, "little"))


def alucard_liner(al_col_l: int, patch: SotnProcedurePatch):
    palettes_alucard_liner = [
        [0x84ab, 0x8d2f, 0x91d6, 0x929b],  # Gold Trim (Default)
        [0x8465, 0x88a8, 0x88ec, 0x9151],  # Bronze Trim
        [0x94a6, 0xa54a, 0xb9ef, 0xc693],  # Silver Trim
        [0x8c43, 0x98a5, 0x9cc8, 0xa54c],  # Onyx Trim
        [0xa8ac, 0xad0f, 0xadb3, 0xbe16],  # Coral Trim
    ]

    offset = 0xef940
    for i in range(4):
        patch.write_token(APTokenTypes.WRITE, offset, palettes_alucard_liner[al_col_l][i].to_bytes(2, "little"))
        offset += 2


def magic_max(patch: SotnProcedurePatch):
    offset = 0x00117b50	 # Set Starting Offset
    # Patch MP Vessels function Heart Vessels - code by MottZilla & graphics drawn by eldri7ch
    patch.write_token(APTokenTypes.WRITE, offset, (0x3c028004).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x8c42c9a0).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x10400003).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x0803f8e7).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x34020001).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x3c058009).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x8ca47bac).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x8ca67ba8).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x24840005).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0xaca47bac).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x24c60005).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0xaca67ba8).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x8ca47bb4).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x24840003).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0xaca47bb0).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0xaca47bb4).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x3c058013).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x34a57964).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x8ca40000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x00000000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x24840001).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0xaca40000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x0803f8e7).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x34020000).to_bytes(4, "little"))
    # Patch GFX - MottZilla
    offset = 0x3868268
    patch.write_token(APTokenTypes.WRITE, offset, (0x40000000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x3).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x40000000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x3).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x40000000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x3).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x40000000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x3).to_bytes(4, "little"))
    offset += 0x24
    patch.write_token(APTokenTypes.WRITE, offset, (0xf7200000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x277).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0xf7200000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x277).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0xf7200000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x277).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0xf7200000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x277).to_bytes(4, "little"))
    offset += 0x24
    patch.write_token(APTokenTypes.WRITE, offset, (0x97122000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x22169).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x97122000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x22169).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x97122000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x22169).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x97122000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x22169).to_bytes(4, "little"))
    offset += 0x24
    patch.write_token(APTokenTypes.WRITE, offset, (0x1f944300).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x344971).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x1f944300).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x344971).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x1f944300).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x344971).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x1f944300).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x344971).to_bytes(4, "little"))
    offset += 0x24
    patch.write_token(APTokenTypes.WRITE, offset, (0xa9432130).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x321449a).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0xa9432130).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x321449a).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0xa9432130).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x321449a).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0xa9432130).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x321449a).to_bytes(4, "little"))
    offset += 0x24
    patch.write_token(APTokenTypes.WRITE, offset, (0x93319920).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x2992349).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x93319920).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x2992349).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x93319920).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x2992349).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x93319920).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x2992349).to_bytes(4, "little"))
    offset += 0x24
    patch.write_token(APTokenTypes.WRITE, offset, (0x3f2c7690).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x9679233).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x3f2c7690).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x9679233).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x3f2c7690).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x9679233).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x3f2c7690).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x9679233).to_bytes(4, "little"))
    offset += 0x24
    patch.write_token(APTokenTypes.WRITE, offset, (0xf29ccf60).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x6fab913).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0xf29ccf60).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x6fab913).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0xf293cf60).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x6fab913).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0xf23c3f60).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x6fab913).to_bytes(4, "little"))
    offset += 0x24
    patch.write_token(APTokenTypes.WRITE, offset, (0x19accbf0).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0xf9aaa91).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x19cfcbf0).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0xf9aaa91).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x193f3bf0).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0xf9aaa91).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x19cfcbf0).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0xf9aaa91).to_bytes(4, "little"))
    offset += 0x24
    patch.write_token(APTokenTypes.WRITE, offset, (0x9accba70).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x79baaa9).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x9accba70).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x79baaa9).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x9ac3ba70).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x79baaa9).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x9ac3ba70).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x79baaa9).to_bytes(4, "little"))
    offset += 0x24
    patch.write_token(APTokenTypes.WRITE, offset, (0xabccaf00).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x79baaa).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0xabccaf00).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x79baaa).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0xabccaf00).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x79baaa).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0xabccaf00).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x79baaa).to_bytes(4, "little"))
    offset += 0x24
    patch.write_token(APTokenTypes.WRITE, offset, (0xbbbaf000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x79bab).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0xbbbaf000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x79bab).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0xbbbaf000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x79bab).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0xbbbaf000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x79bab).to_bytes(4, "little"))
    offset += 0x24
    patch.write_token(APTokenTypes.WRITE, offset, (0xaaa70000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x79aa).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0xaaa70000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x79aa).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0xaaa70000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x79aa).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0xaaa70000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x79aa).to_bytes(4, "little"))
    offset += 0x24
    patch.write_token(APTokenTypes.WRITE, offset, (0xf7600000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x67f).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0xf7600000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x67f).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0xf7600000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x67f).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0xf7600000).to_bytes(4, "little"))
    offset += 4
    patch.write_token(APTokenTypes.WRITE, offset, (0x67f).to_bytes(4, "little"))
    offset += 4


def anti_freeze(patch: SotnProcedurePatch):
    # Patch screen freeze value - eldri7ch
    patch.write_token(APTokenTypes.WRITE, 0x00140a2c, struct.pack("<B", 0x00))


def my_purse(patch: SotnProcedurePatch):
    # Patch Death goes home - eldri7ch
    patch.write_token(APTokenTypes.WRITE, 0x04baea08, (0x18000006).to_bytes(4, "little"))


def fast_warp(patch: SotnProcedurePatch):
    # Patch warp animation speed - eldri7ch
    patch.write_token(APTokenTypes.WRITE, 0x0588be90, struct.pack("<B", 0x02))  # Patch from Aperture / MottZilla
    patch.write_token(APTokenTypes.WRITE, 0x05a78fe4, struct.pack("<B", 0x02))


def unlocked_patches(patch: SotnProcedurePatch):
    tile_remove = 0x00000000  # set tile overwrites to remove them
    memory_skip = 0x34020001  # set register 2 to 01 instead of whatever RAM said
    nop_value = 0x00000000  # nop instruction follow-up

    # Patch the reverse entrance shortcut - eldri7ch
    offset = 0x051caaee  # remove the blocking tiles - eldri7ch
    for _ in range(8):
        patch.write_token(APTokenTypes.WRITE, offset, tile_remove.to_bytes(4, "little"))
        offset += 0x40

    offset_list = [
        0x05430050, 0x05430518, 0x04ba840c, 0x04ba88ac,  # Underground Caverns - Entrance shortcut - eldri7ch
        0x04ba8bc4, 0x04ba8dd4, 0x04ba8e00, 0x04ba918c, 0x04ba91b4, 0x05430844, 0x05430a80, 0x05430bd0, 0x05430e3c,
        0x05430e64,  # Marble Gallery - Entrance shortcut - eldri7ch
        0x04bab2d4, 0x04bab534, 0x04bab674, 0x054325dc, 0x0543283c, 0x0543297c,  # Warp Room - Entrance shortcut - eldri7ch
        0x046c082c,  # Olrox's Quarters - Royal Chapel shortcut - eldri7ch
        0x0440100c, 0x04401100,  # Colosseum - Royal Chapel shortcut - eldri7ch
    ]

    patch.write_token(APTokenTypes.WRITE, 0x051b03c2, (0x030e).to_bytes(2, "little"))  # move the entity down - eldri7ch
    patch.write_token(APTokenTypes.WRITE, 0x051afb80, (0x030e).to_bytes(2, "little"))
    for o in offset_list:
        offset = o
        patch.write_token(APTokenTypes.WRITE, offset, memory_skip.to_bytes(4, "little"))
        offset += 4
        patch.write_token(APTokenTypes.WRITE, offset, nop_value.to_bytes(4, "little"))


def surprise_patches(patch: SotnProcedurePatch):
    surprise_pal = 0x01020111  # set tile overwrites to remove them
    # Patch the sprites for each relic - eldri7ch; code by MottZilla
    offset = 0x000b5550  # start with Soul of Bat - eldri7ch
    for i in range(30):
        patch.write_token(APTokenTypes.WRITE, offset, surprise_pal.to_bytes(4, "little"))
        if i == 13:
            offset += 0x140
        else:
            offset += 0x10


def randomize_drop(option: int, world: "SotnWorld", patch: SotnProcedurePatch):
    if option == 1 or option == 2:
        items = tile_filter(io_items, ["enemy"])
        dropped_items = []
        # Collect every drop
        for item in items:
            for tile in item["tiles"]:
                if option == 1 and tile["enemy"] == "GLOBAL_DROP":
                    continue

                total = len(tile["addresses"])
                for _ in range(total):
                    dropped_items.append(item["name"])
        # Randomize the drops
        world.random.shuffle(dropped_items)
        # Write on the ROM
        for item in items:
            for tile in item["tiles"]:
                if option == 1 and tile["enemy"] == "GLOBAL_DROP":
                    continue

                for address in tile["addresses"]:
                    tile_options = {}
                    if "noOffset" in tile:
                        tile_options = {"no_offset": True}
                    new_drop = io_item_name[dropped_items.pop()]
                    new_tile = tile_value(new_drop, tile_options)
                    patch.write_token(APTokenTypes.WRITE, address, new_tile.to_bytes(2, "little"))


def get_base_rom_bytes(audio: bool = False) -> bytes:
    if not audio:
        file_name = get_settings().sotn_settings.rom_file
        with open(file_name, "rb") as infile:
            base_rom_bytes = bytes(infile.read())

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if USHASH != basemd5.hexdigest():
            raise Exception('Supplied Track 1 Base Rom does not match known MD5 for SLU067 release. '
                            'Get the correct game and version, then dump it')
    else:
        file_name = get_settings().sotn_settings.audio_file
        with open(file_name, "rb") as infile:
            base_rom_bytes = bytes(infile.read())

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if AUDIOHASH != basemd5.hexdigest():
            raise Exception('Supplied Track 2 Audio Rom does not match known MD5 for SLU067 release. '
                            'Get the correct game and version, then dump it')

    return base_rom_bytes


def write_seed(patch: SotnProcedurePatch, seed, player_number, player_name, sanity_options) -> None:
    byte = 0
    start_address = 0x0438d47c
    duplicate_offset = 0x4298798
    seed_text = []

    # Seed number occupies 10 bytes total line have 22 + 0xFF 0x00 at end
    # There are 2 unused bytes from bonus luck
    for i, num in enumerate(seed):
        if i % 2 != 0:
            byte = (byte | int(num))
            seed_text.append(byte)
            byte = 0
        else:
            byte = (int(num) << 4)

    if player_number < 255:
        seed_text.append(0)
        seed_text.append(player_number)
    else:
        b_array = bytearray(player_number.to_bytes(2, "big"))
        seed_text.append(b_array[0])
        seed_text.append(b_array[1])

    seed_text.append(sanity_options)

    # Still space on 1st maria meeting text

    options_len = len(seed_text)
    for _ in range(options_len, 22):
        seed_text.append(0x00)

    seed_text.append(0xFF)
    seed_text.append(0x00)

    for b in seed_text:
        patch.write_token(APTokenTypes.WRITE, start_address, struct.pack("<B", b))
        patch.write_token(APTokenTypes.WRITE, start_address - duplicate_offset, struct.pack("<B", b))
        start_address += 1

    utf_name = player_name.encode("utf8")
    sizes = [30, 30, 20]
    first_line = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0x00]
    second_line = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0x00]
    third_line = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                  0x00, 0x00, 0xFF, 0x00]
    # Name MAX SIZE is 16 chars = 64 bytes
    char_count = 0
    line_count = 0
    for c in utf_name:
        if char_count == sizes[line_count]:
            line_count += 1
            char_count = 0

        if line_count == 0:
            first_line[char_count] = c
        elif line_count == 1:
            second_line[char_count] = c
        elif line_count == 2:
            third_line[char_count] = c

        char_count += 1

    # Write a CR+LF 0d 0a
    if char_count == sizes[line_count]:
        line_count += 1
        char_count = 0

    if line_count == 0:
        first_line[char_count] = 0x0d
        first_line[char_count + 1] = 0x0a
    elif line_count == 1:
        second_line[char_count] = 0x0d
        second_line[char_count + 1] = 0x0a
    elif line_count == 2:
        third_line[char_count] = 0x0d
        third_line[char_count + 1] = 0x0a

    # Write to file
    # Player name on meeting with librarian, get holy glasses, meeting with death
    start_address = 0x438d494
    for b in first_line:
        patch.write_token(APTokenTypes.WRITE, start_address, struct.pack("<B", b))
        patch.write_token(APTokenTypes.WRITE, start_address - duplicate_offset, struct.pack("<B", b))
        start_address += 1

    start_address = 0x438d4b4
    for b in second_line:
        patch.write_token(APTokenTypes.WRITE, start_address, struct.pack("<B", b))
        patch.write_token(APTokenTypes.WRITE, start_address - duplicate_offset, struct.pack("<B", b))
        start_address += 1

    start_address = 0x438d4d4
    for b in third_line:
        patch.write_token(APTokenTypes.WRITE, start_address, struct.pack("<B", b))
        patch.write_token(APTokenTypes.WRITE, start_address - duplicate_offset, struct.pack("<B", b))
        start_address += 1


def items_as_bytes(item1: int, item2: int) -> tuple:
    value1 = item1 >> 4
    value2 = (item1 & 0x0f) << 4
    if item2 < 255:
        value3 = item2
    else:
        value2 = value2 | (item2 >> 8)
        value3 = item2 & 0x0ff

    return value1, value2, value3


def bytes_as_items(byte1: int, byte2: int, byte3: int) -> tuple:
    item1 = (byte1 << 4) | ((byte2 & 0xf0) >> 4)
    item2 = ((byte2 & 0x0f) << 8) | byte3

    return item1, item2


def randomize_starting_equipment(world: "SotnWorld", patch: SotnProcedurePatch):
    rng_weapon = world.random.choice(list(weapon1.items()))
    rng_shield = world.random.choice(list(shield.items()))
    rng_armor = world.random.choice(list(armor.items()))
    rng_cloak = world.random.choice(list(cloak.items()))
    rng_helmet = world.random.choice(list(helmet.items()))
    rng_other = world.random.choice(list(accessory.items()))

    # Their values when equipped
    weapon_equip_val = rng_weapon[1]["id"]
    shield_equip_val = rng_shield[1]["id"]
    helmet_equip_val = rng_helmet[1]["id"] + equip_id_offset
    armor_equip_val = rng_armor[1]["id"] + equip_id_offset
    cloak_equip_val = rng_cloak[1]["id"] + equip_id_offset
    other_equip_val = rng_other[1]["id"] + equip_id_offset

    # Their inventory locations
    weapon_inv_offset = rng_weapon[1]["id"] + equip_inv_id_offset
    shield_inv_offset = rng_shield[1]["id"] + equip_inv_id_offset
    helmet_inv_offset = rng_helmet[1]["id"] + equip_inv_id_offset
    armor_inv_offset = rng_armor[1]["id"] + equip_inv_id_offset
    cloak_inv_offset = rng_cloak[1]["id"] + equip_inv_id_offset
    other_inv_offset = rng_other[1]["id"] + equip_inv_id_offset

    equip_base_address = 0x11a0d0
    # Equip the items
    patch.write_token(APTokenTypes.WRITE, equip_base_address, weapon_equip_val.to_bytes(2, "little"))
    patch.write_token(APTokenTypes.WRITE, equip_base_address + 12, shield_equip_val.to_bytes(2, "little"))
    patch.write_token(APTokenTypes.WRITE, equip_base_address + 24, helmet_equip_val.to_bytes(2, "little"))
    patch.write_token(APTokenTypes.WRITE, equip_base_address + 36, armor_equip_val.to_bytes(2, "little"))
    patch.write_token(APTokenTypes.WRITE, equip_base_address + 48, cloak_equip_val.to_bytes(2, "little"))
    patch.write_token(APTokenTypes.WRITE, equip_base_address + 60, other_equip_val.to_bytes(2, "little"))

    # Death removes these values if equipped
    patch.write_token(APTokenTypes.WRITE, 0x1195f8, weapon_equip_val.to_bytes(2, "little"))
    patch.write_token(APTokenTypes.WRITE, 0x119658, shield_equip_val.to_bytes(2, "little"))
    patch.write_token(APTokenTypes.WRITE, 0x1196b8, helmet_equip_val.to_bytes(2, "little"))
    patch.write_token(APTokenTypes.WRITE, 0x1196f4, armor_equip_val.to_bytes(2, "little"))
    patch.write_token(APTokenTypes.WRITE, 0x119730, cloak_equip_val.to_bytes(2, "little"))
    patch.write_token(APTokenTypes.WRITE, 0x119774, other_equip_val.to_bytes(2, "little"))

    # Death decrements these inventory values if not equipped
    patch.write_token(APTokenTypes.WRITE, 0x119634, weapon_inv_offset.to_bytes(2, "little"))
    patch.write_token(APTokenTypes.WRITE, 0x119648, weapon_inv_offset.to_bytes(2, "little"))
    patch.write_token(APTokenTypes.WRITE, 0x119694, shield_inv_offset.to_bytes(2, "little"))
    patch.write_token(APTokenTypes.WRITE, 0x1196a8, shield_inv_offset.to_bytes(2, "little"))
    patch.write_token(APTokenTypes.WRITE, 0x1196d0, helmet_inv_offset.to_bytes(2, "little"))
    patch.write_token(APTokenTypes.WRITE, 0x1196e4, helmet_inv_offset.to_bytes(2, "little"))
    patch.write_token(APTokenTypes.WRITE, 0x11970c, armor_inv_offset.to_bytes(2, "little"))
    patch.write_token(APTokenTypes.WRITE, 0x119720, armor_inv_offset.to_bytes(2, "little"))
    patch.write_token(APTokenTypes.WRITE, 0x119750, cloak_inv_offset.to_bytes(2, "little"))
    patch.write_token(APTokenTypes.WRITE, 0x119764, cloak_inv_offset.to_bytes(2, "little"))
    patch.write_token(APTokenTypes.WRITE, 0x1197b0, other_inv_offset.to_bytes(2, "little"))
    patch.write_token(APTokenTypes.WRITE, 0x1197c4, other_inv_offset.to_bytes(2, "little"))

    # Death cutscene draws these items
    patch.write_token(APTokenTypes.WRITE, 0x04b6844c, rng_weapon[1]["id"].to_bytes(2, "little"))
    patch.write_token(APTokenTypes.WRITE, 0x04b6844e, rng_shield[1]["id"].to_bytes(2, "little"))
    patch.write_token(APTokenTypes.WRITE, 0x04b68452, rng_helmet[1]["id"].to_bytes(2, "little"))
    patch.write_token(APTokenTypes.WRITE, 0x04b68450, rng_armor[1]["id"].to_bytes(2, "little"))
    patch.write_token(APTokenTypes.WRITE, 0x04b68454, rng_cloak[1]["id"].to_bytes(2, "little"))
    patch.write_token(APTokenTypes.WRITE, 0x04b68456, rng_other[1]["id"].to_bytes(2, "little"))
