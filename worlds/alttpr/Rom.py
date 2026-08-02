import hashlib
import io
import logging
import pkgutil
from typing import Callable, Sequence

from worlds.Files import APPatchExtension, APProcedurePatch, APTokenMixin, APTokenTypes
from .ALttPDoorRandomizer.InitialSram import InitialSram
from .ALttPDoorRandomizer.Rom import JAP10HASH, RANDOMIZERBASEHASH
from .python_bps_continued.bps.apply import apply_to_bytearrays
from .python_bps_continued.bps.io import read_bps


logger = logging.Logger("alttpr")

class ALttPRProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "The Legend of Zelda: A Link to the Past"
    hash = JAP10HASH
    patch_file_ending = ".apalttpr"
    result_file_ending = ".sfc"
    procedure = [
        ("apply_randomizer_rom", []),
        ("apply_tokens", ["token_data.bin"]),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        from .World import ALttPRWorld
        with open(ALttPRWorld.settings.rom_file, "rb") as base_rom:
            base_rom_bytes = bytes(base_rom.read())

        return base_rom_bytes


# We need to patch the original ROM to create the generic randomizer ROM,
# then we can edit that with the randomized items, settings, etc.
class ALttPRBaseRandomizerPatch(APPatchExtension):
    game = "The Legend of Zelda: A Link to the Past"

    @staticmethod
    def apply_randomizer_rom(caller: ALttPRProcedurePatch, rom: bytes):
        rom_writable = bytearray(rom)
        has_smc_header = False
        if len(rom)%0x400 == 0x200:
            rom_writable = rom_writable[0x200:]
            has_smc_header = True
        return bytes(patch_base_rom(rom_writable))


def patch_base_rom(buffer):
    # verify correct checksum of baserom
    basemd5 = hashlib.md5()
    basemd5.update(buffer)
    if JAP10HASH != basemd5.hexdigest():
        logger.warning('Supplied Base Rom does not match known MD5 for JAP(1.0) release. Will try to patch anyway.')

    orig_buffer = buffer.copy()

    # extend to 2MB
    buffer.extend(bytearray([0x00] * (0x200000 - len(buffer))))

    # load randomizer patches
    data = pkgutil.get_data(__name__, "ALttPDoorRandomizer/data/base2current.bps")
    apply_to_bytearrays(read_bps(io.BytesIO(data)), orig_buffer, buffer)

    # verify md5
    patchedmd5 = hashlib.md5()
    patchedmd5.update(buffer)
    if RANDOMIZERBASEHASH != patchedmd5.hexdigest():
        raise RuntimeError('Provided Base Rom unsuitable for patching. Please provide a JAP(1.0) "Zelda no Densetsu - Kamigami no Triforce (Japan).sfc" rom to use as a base.')

    return buffer


# This class is an adapter for the door randomizer LocalRom, so we can reuse its patch_rom()
# logic and make it AP-compatible, by passing in an ALttPRRom instead of LocalRom.
# TODO: "Adapter" is the wrong word, since this is really replacing LocalRom. Maybe this should
# be a child of LocalRom to reuse some its logic, and only overwrite the methods we need to?
# Was focused on getting it working rather than correct architecture while writing this code.
class ALttPRRom:
    def __init__(self, player: int, player_name: str, seed_hash: bytes):
        self.initial_sram = InitialSram()
        self.name = None
        self.orig_buffer = None
        self.patch = ALttPRProcedurePatch(player=player, player_name=player_name)
        self.hash = JAP10HASH
        self.player = player
        self.player_name = player_name
        self.seed_hash = seed_hash  # This is the 5-item hash that appears on the file select screen.


    def get_hash(self):
        # This is a random code. An accurate hash would require the ROM file, and we
        # don't want the ROM to be required for generating the seed.
        return self.seed_hash.hex()


    def write_initial_sram(self):
        self.write_bytes(0x183000, self.initial_sram.get_initial_sram())


    def write(self, output_path: str):
        self.patch.write_file("token_data.bin", self.patch.get_token_binary())
        self.patch.write(output_path)


    def write_byte(self, address: int, value: int):
        self.write_bytes(address, value)


    def write_bytes(self, address: int, data: Sequence[int] | int):
        if isinstance(data, int):
            data = bytes([data])
        else:
            data = bytes(data)

        self.patch.write_token(APTokenTypes.WRITE, address, data)


    def write_crc(self):
        crc = (sum(self.buffer[:0x7FDC] + self.buffer[0x7FE0:]) + 0x01FE) & 0xFFFF
        inv = crc ^ 0xFFFF
        self.write_bytes(0x7FDC, [inv & 0xFF, (inv >> 8) & 0xFF, crc & 0xFF, (crc >> 8) & 0xFF])
