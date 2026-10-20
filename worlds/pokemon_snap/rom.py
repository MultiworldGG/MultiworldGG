import hashlib
import os
from typing import Optional

import settings
import Utils
from worlds.Files import APProcedurePatch, APTokenMixin

# MD5 of the North American Pokemon Snap ROM (.z64, big-endian) the basepatch
# is built against.
PSNAP_NA_HASH = "fc3c9329b7cdd67cf7650abf63b9a580"


class PokemonSnapProcedurePatch(APProcedurePatch, APTokenMixin):
    hash = PSNAP_NA_HASH
    game = "Pokemon Snap"
    patch_file_ending = ".apsnap"
    result_file_ending = ".z64"

    procedure = [
        ("apply_bsdiff4", ["basepatch.bsdiff4"]),
        ("apply_tokens", ["token_patch.bin"]),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()


def get_base_rom_path(file_name: str = "") -> str:
    options: settings.Settings = settings.get_settings()
    if not file_name:
        file_name = options["pokemon_snap_options"]["rom_path"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes: Optional[bytes] = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        base_rom_bytes = bytes(open(get_base_rom_path(file_name), "rb").read())

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if basemd5.hexdigest() != PSNAP_NA_HASH:
            raise Exception("Supplied base ROM does not match the known MD5 for the North American "
                            "Pokemon Snap release (.z64). Get the correct game and version, then dump it.")

        setattr(get_base_rom_bytes, "base_rom_bytes", base_rom_bytes)
    return base_rom_bytes
