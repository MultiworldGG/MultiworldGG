import Utils
import hashlib
import os
from typing import TYPE_CHECKING, Iterable
from BaseClasses import Location, ItemClassification
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes, APPatchExtension

if TYPE_CHECKING:
    from . import WarioWareWorld

from .items import item_groups
from .constants import *

HASH_US = 'a2d26dc774cec9a0b47388a5dd727b03'

class WarioWarePatchExtension(APPatchExtension):
    game = GAME_NAME
    
    @staticmethod
    def apply_selected_patches(caller: APProcedurePatch, rom: bytes):
        import bsdiff4
        import pkgutil
        
        basemd5 = hashlib.md5()
        basemd5.update(rom)
        patch_file = pkgutil.get_data(__name__, f"data/wario.bsdiff4")
        rom = bsdiff4.patch(rom, patch_file)

        return rom
        

class WarioWareProcedurePatch(APProcedurePatch, APTokenMixin):
    hash = [HASH_US]
    game = GAME_NAME
    patch_file_ending = ".apwariowareinc"
    result_file_ending = ".gba"
    name: bytearray
    procedure = [
        ("apply_selected_patches", []),
        ("apply_tokens", ["token_patch.bin"]),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

    def write_byte(self, offset: int, value: int):
        self.write_token(APTokenTypes.WRITE, offset, value.to_bytes(1, "little"))

    def write_bytes(self, offset: int, value: Iterable[int]):
        self.write_token(APTokenTypes.WRITE, offset, bytes(value))


def patch_rom(world: "WarioWareWorld", patch: WarioWareProcedurePatch):
    patch.name = world.auth
    patch.write_bytes(AUTH_NUMBER_START, patch.name)
    patch.write_byte(SETTING_UNLOCKS, world.options.microgame_unlock.value)
    patch.write_byte(SETTING_GOAL, world.required_flowers)
    patch.write_byte(SETTING_FLOWERS, world.options.flowers_required.value)

    microgames_list = world.microgames.copy()
    microgames_list.extend([0xFF] * (0x100 - len(microgames_list)))
    patch.write_bytes(MICROGAMES_LIST, bytearray(microgames_list))

    write_location_data(world, patch)
    
    patch.write_file("token_patch.bin", patch.get_token_binary())

classification_text = {
    ItemClassification.progression | ItemClassification.useful:
        "☀LOCATION⛉",
    ItemClassification.progression:
        "⛊LOCATION⛉",
}

def write_location_data(world: "WarioWareWorld", patch: WarioWareProcedurePatch):
    from .stage_data import microgame_data, microgame_flower_data
    from .text_dict import supported_characters

    filled_locations = world.multiworld.get_filled_locations(world.player)
    location_data_by_name = {location.name: location for location in filled_locations}
    for microgame_name in microgame_data.keys():
        if f"{microgame_name} - Clear" not in location_data_by_name.keys():
            continue

        item_name, classification, player_name = get_location_info(world, location_data_by_name[f"{microgame_name} - Clear"])
    
        clear_text = "Clear — "
        if classification in classification_text:
            clear_text += f"{classification_text[classification].replace("LOCATION", item_name)} "
        else:
            clear_text += f"{item_name} "
        clear_text += f"(⛊{player_name}⛉)"

        flower_text = ""
        if world.options.microgame_flowers:
            flower_text = f"Flower: ⛊{microgame_flower_data[microgame_name]}⛉ Pts. — "
            item_name, classification, player_name = get_location_info(world, location_data_by_name[f"{microgame_name} - Flower"])
            if classification in classification_text:
                flower_text += f"{classification_text[classification].replace("LOCATION", item_name)} "
            else:
                flower_text += f"{item_name} "
            flower_text += f"(⛊{player_name}⛉) ★"

        hint_text = f"【{microgame_name}】 {flower_text} {clear_text}©©©©©©©©"

        microgame_id = microgame_data[microgame_name]
        current_offset = NEW_MICROGAME_LOCATION + (microgame_id << 9)
        patch.write_bytes(MICROGAME_PTRS + (microgame_id * 4), (current_offset | 0x08000000).to_bytes(4, "little"))
        for character in hint_text: 
            if character not in supported_characters:
                character = "★"
            data = supported_characters[character]
            for current_byte in data:
                patch.write_byte(current_offset, current_byte)
                current_offset += 1


def get_location_info(world: "WarioWareWorld", location: Location):
    return (
        location.item.name[:32],
        location.item.classification & (ItemClassification.progression | ItemClassification.useful),
        world.multiworld.get_player_name(location.item.player)[:16]
    )

    
def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(open(file_name, "rb").read())

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if basemd5.hexdigest() not in [HASH_US]:
            raise Exception(f"Supplied Base ROM does not match known MD5s for {GAME_NAME}."
                            "Get the correct game and version, then dump it.")
        setattr(get_base_rom_bytes, "base_rom_bytes", base_rom_bytes)
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    if not file_name:
        from settings import get_settings
        file_name = get_settings()["wario_ware_inc_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name

