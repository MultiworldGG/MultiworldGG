import hashlib
import json
from pathlib import Path
from random import Random
import tempfile

from worlds.Files import APPatchExtension, APProcedurePatch

from ..Cosmetics import patch_cosmetics
from ..Patches import patch_rom
from ..Rom import Rom, compress_rom_file
from .context import PatchContext


def load_base_rom(file_name=None):
    from .. import OOTSettings, OOTWorld

    path = Path(file_name if file_name is not None else OOTWorld.settings.rom_file)
    source = path.read_bytes()
    if hashlib.md5(source).hexdigest() not in OOTSettings.RomFile.md5s:
        raise ValueError("The base ROM must be Ocarina of Time v1.0 NTSC-U or NTSC-J.")
    with tempfile.TemporaryDirectory(prefix="oot-base-") as directory:
        rom = Rom(file=str(path), force_use=True, decompressed_path=str(Path(directory) / "base.z64"))
        return bytes(rom.original.buffer)


def apply_patch_data(source, data):
    context = PatchContext(data)
    rom = Rom.from_bytes(source)
    patch_rom(context, rom)
    context.random = Random(context.cosmetic_rng_seed)
    patch_cosmetics(context, rom)
    rom.verify_dmadata()
    rom.update_header()
    return rom


def patch_to_rom(patch_file, base_rom=None):
    """Apply a patch without compression for the Adjuster."""
    patch = OoTProcedurePatch(str(patch_file))
    patch.read()
    return apply_patch_data(load_base_rom(base_rom), json.loads(patch.get_file("seed.json")))


class OoTPatchExtension(APPatchExtension):
    game = "Ocarina of Time"

    @staticmethod
    def apply_oot_patch(caller, source, seed_file):
        rom = apply_patch_data(source, json.loads(caller.get_file(seed_file)))
        with tempfile.TemporaryDirectory(prefix="oot-patch-") as directory:
            decompressed = Path(directory) / "decompressed.z64"
            compressed = Path(directory) / "patched.z64"
            rom.write_to_file(decompressed)
            compress_rom_file(str(decompressed), str(compressed))
            return compressed.read_bytes()


class OoTProcedurePatch(APProcedurePatch):
    game = "Ocarina of Time"
    hash = None  # load_base_rom checks the supported ROM hashes.
    patch_file_ending = ".apoot"
    result_file_ending = ".z64"
    procedure = [("apply_oot_patch", ["seed.json"])]

    @classmethod
    def get_source_data(cls):
        return load_base_rom()

    @classmethod
    def get_source_data_with_cache(cls):
        # The user may select a different ROM between patches.
        return cls.get_source_data()
