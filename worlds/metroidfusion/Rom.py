import json
import logging
import os
import tempfile
import typing
from settings import get_settings
from Utils import read_snes_rom, Version, tuplize_version
from worlds.Files import APProcedurePatch, APTokenMixin, APPatchExtension
from .data import memory

def get_base_rom_as_bytes() -> bytes:
    with open(get_settings().metroidfusion_options.rom_file, "rb") as infile:
        base_rom_bytes = bytes(read_snes_rom(infile))
    return base_rom_bytes


class IncompatiblePatchError(Exception):
    generator_version: Version
    patch_version: Version

    def __init__(self, gen_version: Version, patch_version: Version):
        self.generator_version = gen_version
        self.patch_version = patch_version
        direction = "up" if gen_version >= patch_version else "down"
        super().__init__(f"This patch was generated with APWorld version {gen_version.as_simple_string()}, "
                         f"which is incompatible with currently installed version {patch_version.as_simple_string()}."
                         f"\nPlease {direction}grade your APWorld.")


class MetroidFusionPatchExtension(APPatchExtension):
    game = "Metroid Fusion"

    @staticmethod
    def call_mars(caller, rom, placement_file):
        from . import MetroidFusionWorld
        patch_dict = json.loads(caller.get_file(placement_file))
        gen_version_str = patch_dict.get("generation_version", None)
        patch_min_version_str = patch_dict.get("minimum_compatible_version", None)
        if patch_min_version_str is None:
            raise ValueError(f"This {caller.game} patch is too old for this APWorld. "
                              "Please double-check the version used for generating.")
        logging.info(f"Metroid Fusion APWorld v{gen_version_str} was used for generation.")
        logging.info(f"Metroid Fusion APWorld v{MetroidFusionWorld.version} used for patching.")
        gen_version = tuplize_version(gen_version_str)
        patch_min_version = tuplize_version(patch_min_version_str)
        patch_version = tuplize_version(MetroidFusionWorld.version)
        if patch_min_version > patch_version or MetroidFusionProcedurePatch.minimum_patch_version > gen_version:
            raise IncompatiblePatchError(gen_version, patch_version)
        from .mars_patcher import patcher
        patcher.validate_patch_data_mf(patch_dict)
        output_file = patch_dict["output_file"]
        directory = tempfile.gettempdir()
        with open(os.path.join(directory, "temp.gba"), "wb") as file:
            file.write(rom)
        patcher.patch(
            os.fspath(os.path.join(directory, "temp.gba")),
            os.fspath(os.path.join(directory, output_file)),
            typing.cast("patcher.MarsSchema", patch_dict),
            lambda message, progress: print(f"{message} -- {progress}"),
        )
        with open(os.path.join(directory, output_file), "rb") as file:
            rom_data = bytearray(file.read())
            rom_name_text = patch_dict["rom_name"]
            rom_name = bytearray(rom_name_text, 'utf-8')
            rom_name.extend([0] * (20 - len(rom_name)))
            rom_data[memory.rom_name_location:memory.rom_name_location + 20] = bytes(rom_name)
            rom_data[memory.generation_version_location:memory.generation_version_location + 2] = bytes(gen_version)
            rom_data[memory.patching_version_location:memory.patching_version_location + 2] = bytes(patch_version)
        return rom_data


class MetroidFusionProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Metroid Fusion"
    hash = "27D02A4F03E172E029C9B82AC3DB79F7"
    patch_file_ending = ".apmetfus"
    result_file_ending = ".gba"
    minimum_patch_version = Version(1, 23, 0)

    procedure = [
        ("call_mars", ["patch_file.json"])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_as_bytes()

