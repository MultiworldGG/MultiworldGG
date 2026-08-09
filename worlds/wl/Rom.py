import hashlib
import os
import math
import Utils
import bsdiff4
from worlds.Files import APDeltaPatch

WORLDHASH = "d9d957771484ef846d4e8d241f6f2815"
ROM_PLAYER_LIMIT = 65535


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(Utils.read_snes_rom(open(file_name, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if WORLDHASH != basemd5.hexdigest():
            raise Exception(
                "Supplied Base Rom does not match known MD5 for WORLD release. "
                "Get the correct game and version, then dump it"
            )
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    if not file_name:
        from settings import get_settings

        file_name = get_settings().wl_options.rom_file
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name


class WLDeltaPatch(APDeltaPatch):
    hash = WORLDHASH
    game = "Wario Land"
    patch_file_ending = ".apwl"
    result_file_ending = ".gb"

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()


class Rom:
    def __init__(self, file, patch=True, vanillaRom=None, name=None, hash=None):
        self.name = name
        self.hash = hash
        self.orig_buffer = None

        with open(file, "rb") as stream:
            self.buffer = Utils.read_snes_rom(stream)

    def read_bit(self, address: int, bit_number: int) -> bool:
        bitflag = 1 << bit_number
        return (self.buffer[address] & bitflag) != 0

    def read_byte(self, address: int) -> int:
        return self.buffer[address]

    def read_bytes(self, startaddress: int, length: int) -> bytes:
        return self.buffer[startaddress : startaddress + length]

    def write_byte(self, address: int, value: int):
        self.buffer[address] = value

    def write_bytes(self, startaddress: int, values):
        self.buffer[startaddress : startaddress + len(values)] = values

    def write_to_file(self, file):
        with open(file, "wb") as outfile:
            outfile.write(self.buffer)

    def read_from_file(self, file):
        with open(file, "rb") as stream:
            self.buffer = bytearray(stream.read())


# Some of the patched instructions are missing their
# first byte because that one overlaps with the vanilla rom


# Block basic movement abilities
def patch_basic_abilities(rom):
    # Climb
    rom.write_byte(0x34A1B, 0xC3)  # d:4a1b    jp 7B00
    rom.write_byte(0x34A1C, 0x00)  # d:4a1c
    rom.write_byte(0x34A1D, 0x7B)  # d:4a1d
    # ---
    rom.write_byte(0x37B00, 0xEA)  # d:7b00    ld (A490),a
    rom.write_byte(0x37B01, 0x90)  # d:7b01
    rom.write_byte(0x37B02, 0xA4)  # d:7b02
    rom.write_byte(0x37B03, 0xFA)  # d:7b03    ld a,(A407)
    rom.write_byte(0x37B04, 0x07)  # d:7b04
    rom.write_byte(0x37B05, 0xA4)  # d:7b05
    rom.write_byte(0x37B06, 0xA7)  # d:7b06    and a
    rom.write_byte(0x37B07, 0x28)  # d:7b07    jr z,06
    rom.write_byte(0x37B08, 0x06)  # d:7b08
    rom.write_byte(0x37B09, 0xFA)  # d:7b09    ld a,(A490)
    rom.write_byte(0x37B0A, 0x90)  # d:7b0a
    rom.write_byte(0x37B0B, 0xA4)  # d:7b0b
    rom.write_byte(0x37B0C, 0xC3)  # d:7b0c    jp 4A1E
    rom.write_byte(0x37B0D, 0x1E)  # d:7b0d
    rom.write_byte(0x37B0E, 0x4A)  # d:7b0e
    rom.write_byte(0x37B0F, 0xC3)  # d:7b0f    jp 4A3D
    rom.write_byte(0x37B10, 0x3D)  # d:7b10
    rom.write_byte(0x37B11, 0x4A)  # d:7b11

    # Duck
    rom.write_byte(0x34C5A, 0xCD)  # d:4c5a    call 7B13
    rom.write_byte(0x34C5B, 0x13)  # d:4c5b
    rom.write_byte(0x34C5C, 0x7B)  # d:4c5c
    rom.write_byte(0x34A7C, 0xCD)  # d:4a7c    call 7B13
    rom.write_byte(0x34A7D, 0x13)  # d:4a7d
    rom.write_byte(0x34A7E, 0x7B)  # d:4a7e
    rom.write_byte(0x3504A, 0xCD)  # d:504a    call 7B13
    rom.write_byte(0x3504B, 0x13)  # d:504b
    rom.write_byte(0x3504C, 0x7B)  # d:504c
    rom.write_byte(0x35FA2, 0xC3)  # d:5fa2    jp 7B8E
    rom.write_byte(0x35FA3, 0x8E)  # d:5fa3
    rom.write_byte(0x35FA4, 0x7B)  # d:5fa4
    # ---quicksand duck hook
    rom.write_byte(0x37B8E, 0xFA)  # d:7b8e    ld a,(A408)
    rom.write_byte(0x37B8F, 0x08)  # d:7b8f
    rom.write_byte(0x37B90, 0xA4)  # d:7b90
    rom.write_byte(0x37B91, 0xA7)  # d:7b91    and a
    rom.write_byte(0x37B92, 0x20)  # d:7b92    jr nz,03
    rom.write_byte(0x37B93, 0x03)  # d:7b93
    rom.write_byte(0x37B94, 0xC3)  # d:7b94    jp 5FB4
    rom.write_byte(0x37B95, 0xB4)  # d:7b95
    rom.write_byte(0x37B96, 0x5F)  # d:7b96
    rom.write_byte(0x37B97, 0x3E)  # d:7b97    ld a,01
    rom.write_byte(0x37B98, 0x01)  # d:7b98
    rom.write_byte(0x37B99, 0xEA)  # d:7b99    ld (A93E),a
    rom.write_byte(0x37B9A, 0x3E)  # d:7b9a
    rom.write_byte(0x37B9B, 0xA9)  # d:7b9b
    rom.write_byte(0x37B9C, 0xC3)  # d:7b9c    jp 5FA5
    rom.write_byte(0x37B9D, 0xA5)  # d:7b9d
    rom.write_byte(0x37B9E, 0x5F)  # d:7b9e
    # ---normal duck hook
    rom.write_byte(0x37B13, 0xFA)  # d:7b13    ld a,(A408)
    rom.write_byte(0x37B14, 0x08)  # d:7b14
    rom.write_byte(0x37B15, 0xA4)  # d:7b15
    rom.write_byte(0x37B16, 0xA7)  # d:7b16    and a
    rom.write_byte(0x37B17, 0x28)  # d:7b17    jr z,04
    rom.write_byte(0x37B18, 0x04)  # d:7b18
    rom.write_byte(0x37B19, 0xFA)  # d:7b19    ld a,(A956)
    rom.write_byte(0x37B1A, 0x56)  # d:7b1a
    rom.write_byte(0x37B1B, 0xA9)  # d:7b1b
    rom.write_byte(0x37B1C, 0xC9)  # d:7b1c    ret
    rom.write_byte(0x37B1D, 0x3E)  # d:7b1d    ld a,01
    rom.write_byte(0x37B1E, 0x01)  # d:7b1e
    rom.write_byte(0x37B1F, 0xC9)  # d:7b1f    ret

    # High jump
    rom.write_byte(0x34E75, 0xCD)  # d:4e75    call 7B22
    rom.write_byte(0x34E76, 0x22)  # d:4e76
    rom.write_byte(0x34E77, 0x7B)  # d:4e77
    # ---
    rom.write_byte(0x37B22, 0xFA)  # d:7b22    ld a,(A405)
    rom.write_byte(0x37B23, 0x05)  # d:7b23
    rom.write_byte(0x37B24, 0xA4)  # d:7b24
    rom.write_byte(0x37B25, 0xEA)  # d:7b25    ld (A92C),a
    rom.write_byte(0x37B26, 0x2C)  # d:7b26
    rom.write_byte(0x37B27, 0xA9)  # d:7b27
    rom.write_byte(0x37B28, 0xC9)  # d:7b28    ret

    # Dash
    rom.write_byte(0x35BD3, 0xCD)  # d:5bd3    call 7B29
    rom.write_byte(0x35BD4, 0x29)  # d:5bd4
    rom.write_byte(0x35BD5, 0x7B)  # d:5bd5
    # ---
    rom.write_byte(0x37B29, 0xFA)  # d:7b29    ld a,(A404)
    rom.write_byte(0x37B2A, 0x04)  # d:7b2a
    rom.write_byte(0x37B2B, 0xA4)  # d:7b2b
    rom.write_byte(0x37B2C, 0xA7)  # d:7b2c    and a
    rom.write_byte(0x37B2D, 0x28)  # d:7b2d    jr z,04
    rom.write_byte(0x37B2E, 0x04)  # d:7b2e
    rom.write_byte(0x37B2F, 0xFA)  # d:7b2f    ld a,(A34D)
    rom.write_byte(0x37B30, 0x4D)  # d:7b30
    rom.write_byte(0x37B31, 0xA3)  # d:7b31
    rom.write_byte(0x37B32, 0xC9)  # d:7b32    ret
    rom.write_byte(0x37B33, 0x3E)  # d:7b33    ld a,01
    rom.write_byte(0x37B34, 0x01)  # d:7b34
    rom.write_byte(0x37B35, 0xC9)  # d:7b35    ret

    # Create coin
    rom.write_byte(0x34B74, 0xCD)  # d:4b74    call 7B36
    rom.write_byte(0x34B75, 0x36)  # d:4b75
    rom.write_byte(0x34B76, 0x7B)  # d:4b76
    # ---
    rom.write_byte(0x37B36, 0xFA)  # d:7b36    ld a,(A406)
    rom.write_byte(0x37B37, 0x06)  # d:7b37
    rom.write_byte(0x37B38, 0xA4)  # d:7b38
    rom.write_byte(0x37B39, 0xA7)  # d:7b39    and a
    rom.write_byte(0x37B3A, 0x28)  # d:7b3a    jr z,04
    rom.write_byte(0x37B3B, 0x04)  # d:7b3b
    rom.write_byte(0x37B3C, 0xFA)  # d:7b3c    ld a,(A9A4)
    rom.write_byte(0x37B3D, 0xA4)  # d:7b3d
    rom.write_byte(0x37B3E, 0xA9)  # d:7b3e
    rom.write_byte(0x37B3F, 0xC9)  # d:7b3f    ret
    rom.write_byte(0x37B40, 0x3E)  # d:7b40    ld a,01
    rom.write_byte(0x37B41, 0x01)  # d:7b41
    rom.write_byte(0x37B42, 0xC9)  # d:7b42    ret

    # Force small wario
    rom.write_byte(0xEC4, 0xCD)  # 0:ec4   call 7F65
    rom.write_byte(0xEC5, 0x65)  # 0:ec5
    rom.write_byte(0xEC6, 0x7F)  # 0:ec6
    # ---
    rom.write_byte(0x33F65, 0xFA)  # c:7f65    ld a,(A410)
    rom.write_byte(0x33F66, 0x10)  # c:7f66
    rom.write_byte(0x33F67, 0xA4)  # c:7f67
    rom.write_byte(0x33F68, 0xA7)  # c:7f68    and a
    rom.write_byte(0x33F69, 0x20)  # c:7f69    jr nz, 3
    rom.write_byte(0x33F6A, 0x03)  # c:7f6a
    rom.write_byte(0x33F6B, 0xEA)  # c:7f6b    ld (A80A),a
    rom.write_byte(0x33F6C, 0x0A)  # c:7f6c
    rom.write_byte(0x33F6D, 0xA8)  # c:7f6d
    rom.write_byte(0x33F6E, 0xFA)  # c:7f6e    ld a, (A80A)
    rom.write_byte(0x33F6F, 0x0A)  # c:7f6f
    rom.write_byte(0x33F70, 0xA8)  # c:7f70
    rom.write_byte(0x33F71, 0xC9)  # c:7f71    ret
    return


# Block powerup usage
def patch_powerups(rom):
    rom.write_byte(0x364B2, 0xC3)  # d:64b2    jp 7B43
    rom.write_byte(0x364B3, 0x43)  # d:64b3
    rom.write_byte(0x364B4, 0x7B)  # d:64b4
    # ---
    rom.write_byte(0x37B43, 0xEA)  # d:7b43    ld (A958),a
    rom.write_byte(0x37B44, 0x58)  # d:7b44
    rom.write_byte(0x37B45, 0xA9)  # d:7b45
    rom.write_byte(0x37B46, 0xFE)  # d:7b46    cp a,04
    rom.write_byte(0x37B47, 0x04)  # d:7b47
    rom.write_byte(0x37B48, 0xD2)  # d:7b48    jp nc, 7B81
    rom.write_byte(0x37B49, 0x81)  # d:7b49
    rom.write_byte(0x37B4A, 0x7B)  # d:7b4a
    rom.write_byte(0x37B4B, 0xFE)  # d:7b4b    cp a,03
    rom.write_byte(0x37B4C, 0x03)  # d:7b4c
    rom.write_byte(0x37B4D, 0xD2)  # d:7b4d    jp nc, 7B75
    rom.write_byte(0x37B4E, 0x75)  # d:7b4e
    rom.write_byte(0x37B4F, 0x7B)  # d:7b4f
    rom.write_byte(0x37B50, 0xFE)  # d:7b50    cp a,02
    rom.write_byte(0x37B51, 0x02)  # d:7b51
    rom.write_byte(0x37B52, 0xD2)  # d:7b52    jp nc, 7B69
    rom.write_byte(0x37B53, 0x69)  # d:7b53
    rom.write_byte(0x37B54, 0x7B)  # d:7b54
    rom.write_byte(0x37B55, 0xFE)  # d:7b55    cp a,01
    rom.write_byte(0x37B56, 0x01)  # d:7b56
    rom.write_byte(0x37B57, 0xD2)  # d:7b57    jp nc, 7B5D
    rom.write_byte(0x37B58, 0x5D)  # d:7b58
    rom.write_byte(0x37B59, 0x7B)  # d:7b59
    rom.write_byte(0x37B5A, 0xC3)  # d:7b5a    jp 64B5
    rom.write_byte(0x37B5B, 0xB5)  # d:7b5b
    rom.write_byte(0x37B5C, 0x64)  # d:7b5c
    # --Check garlic
    rom.write_byte(0x37B5D, 0xFA)  # d:7b5d    ld a,(A400)
    rom.write_byte(0x37B5E, 0x00)  # d:7b5e
    rom.write_byte(0x37B5F, 0xA4)  # d:7b5f
    rom.write_byte(0x37B60, 0xA7)  # d:7b60    and a
    rom.write_byte(0x37B61, 0xCA)  # d:7b61    jp z,6261
    rom.write_byte(0x37B62, 0x61)  # d:7b62
    rom.write_byte(0x37B63, 0x62)  # d:7b63
    rom.write_byte(0x37B64, 0x3E)  # d:7b64    ld a,01
    rom.write_byte(0x37B65, 0x01)  # d:7b65
    rom.write_byte(0x37B66, 0xC3)  # d:7b66    jp 64B5
    rom.write_byte(0x37B67, 0xB5)  # d:7b67
    rom.write_byte(0x37B68, 0x64)  # d:7b68
    # --Check bull
    rom.write_byte(0x37B69, 0xFA)  # d:7b69    ld a,(A401)
    rom.write_byte(0x37B6A, 0x01)  # d:7b6a
    rom.write_byte(0x37B6B, 0xA4)  # d:7b6b
    rom.write_byte(0x37B6C, 0xA7)  # d:7b6c    and a
    rom.write_byte(0x37B6D, 0xCA)  # d:7b6d    jp z,6261
    rom.write_byte(0x37B6E, 0x61)  # d:7b6e
    rom.write_byte(0x37B6F, 0x62)  # d:7b6f
    rom.write_byte(0x37B70, 0x3E)  # d:7b70    ld a,02
    rom.write_byte(0x37B71, 0x02)  # d:7b71
    rom.write_byte(0x37B72, 0xC3)  # d:7b72    jp 64B5
    rom.write_byte(0x37B73, 0xB5)  # d:7b73
    rom.write_byte(0x37B74, 0x64)  # d:7b74
    # --Check jet
    rom.write_byte(0x37B75, 0xFA)  # d:7b75    ld a,(A402)
    rom.write_byte(0x37B76, 0x02)  # d:7b76
    rom.write_byte(0x37B77, 0xA4)  # d:7b77
    rom.write_byte(0x37B78, 0xA7)  # d:7b78    and a
    rom.write_byte(0x37B79, 0xCA)  # d:7b79    jp z,6261
    rom.write_byte(0x37B7A, 0x61)  # d:7b7a
    rom.write_byte(0x37B7B, 0x62)  # d:7b7b
    rom.write_byte(0x37B7C, 0x3E)  # d:7b7c    ld a,03
    rom.write_byte(0x37B7D, 0x03)  # d:7b7d
    rom.write_byte(0x37B7E, 0xC3)  # d:7b7e    jp 64B5
    rom.write_byte(0x37B7F, 0xB5)  # d:7b7f
    rom.write_byte(0x37B80, 0x64)  # d:7b80
    # --Check dragon
    rom.write_byte(0x37B81, 0xFA)  # d:7b81    ld a,(A403)
    rom.write_byte(0x37B82, 0x03)  # d:7b82
    rom.write_byte(0x37B83, 0xA4)  # d:7b83
    rom.write_byte(0x37B84, 0xA7)  # d:7b84    and a
    rom.write_byte(0x37B85, 0xCA)  # d:7b85    jp z,6261
    rom.write_byte(0x37B86, 0x61)  # d:7b86
    rom.write_byte(0x37B87, 0x62)  # d:7b87
    rom.write_byte(0x37B88, 0xFA)  # d:7b88    ld (A958),a
    rom.write_byte(0x37B89, 0x58)  # d:7b89
    rom.write_byte(0x37B8A, 0xA9)  # d:7b8a
    rom.write_byte(0x37B8B, 0xC3)  # d:7b8b    jp 64B5
    rom.write_byte(0x37B8C, 0xB5)  # d:7b8c
    rom.write_byte(0x37B8D, 0x64)  # d:7b8d
    return


# Patch Map Movement
def patch_world_enter(rom):
    # Block world entering
    rom.write_byte(0x20187, 0xC3)  # 8:4187    jp 7EE1
    rom.write_byte(0x20188, 0xE1)  # 8:4188
    rom.write_byte(0x20189, 0x7E)  # 8:4189
    # --
    rom.write_byte(0x23EE1, 0xFA)  # 8:7ee1    ld a,(A79F)
    rom.write_byte(0x23EE2, 0x9F)  # 8:7ee2
    rom.write_byte(0x23EE3, 0xA7)  # 8:7ee3
    rom.write_byte(0x23EE4, 0xFE)  # 8:7ee4    cp a,07
    rom.write_byte(0x23EE5, 0x07)  # 8:7ee5
    rom.write_byte(0x23EE6, 0xD2)  # 8:7ee6    jp nc, 7F60
    rom.write_byte(0x23EE7, 0x60)  # 8:7ee7
    rom.write_byte(0x23EE8, 0x7F)  # 8:7ee8
    rom.write_byte(0x23EE9, 0xFE)  # 8:7ee9    cp a,06
    rom.write_byte(0x23EEA, 0x06)  # 8:7eea
    rom.write_byte(0x23EEB, 0xD2)  # 8:7eeb    jp nc, 7F54
    rom.write_byte(0x23EEC, 0x54)  # 8:7eec
    rom.write_byte(0x23EED, 0x7F)  # 8:7eed
    rom.write_byte(0x23EEE, 0xFE)  # 8:7eee    cp a,05
    rom.write_byte(0x23EEF, 0x05)  # 8:7eef
    rom.write_byte(0x23EF0, 0xD2)  # 8:7ef0    jp nc, 7F48
    rom.write_byte(0x23EF1, 0x48)  # 8:7ef1
    rom.write_byte(0x23EF2, 0x7F)  # 8:7ef2
    rom.write_byte(0x23EF3, 0xFE)  # 8:7ef3    cp a,04
    rom.write_byte(0x23EF4, 0x04)  # 8:7ef4
    rom.write_byte(0x23EF5, 0xD2)  # 8:7ef5    jp nc, 7F3C
    rom.write_byte(0x23EF6, 0x3C)  # 8:7ef6
    rom.write_byte(0x23EF7, 0x7F)  # 8:7ef7
    rom.write_byte(0x23EF8, 0xFE)  # 8:7ef8    cp a,03
    rom.write_byte(0x23EF9, 0x03)  # 8:7ef9
    rom.write_byte(0x23EFA, 0xD2)  # 8:7efa    jp nc, 7F30
    rom.write_byte(0x23EFB, 0x30)  # 8:7efb
    rom.write_byte(0x23EFC, 0x7F)  # 8:7efc
    rom.write_byte(0x23EFD, 0xFE)  # 8:7efd    cp a,02
    rom.write_byte(0x23EFE, 0x02)  # 8:7efe
    rom.write_byte(0x23EFF, 0xD2)  # 8:7eff    jp nc, 7F24
    rom.write_byte(0x23F00, 0x24)  # 8:7f00
    rom.write_byte(0x23F01, 0x7F)  # 8:7f01
    rom.write_byte(0x23F02, 0xFE)  # 8:7f02    cp a,01
    rom.write_byte(0x23F03, 0x01)  # 8:7f03
    rom.write_byte(0x23F04, 0xD2)  # 8:7f04    jp nc, 7F18
    rom.write_byte(0x23F05, 0x18)  # 8:7f05
    rom.write_byte(0x23F06, 0x7F)  # 8:7f06
    rom.write_byte(0x23F07, 0xFE)  # 8:7f07    cp a,00
    rom.write_byte(0x23F08, 0x00)  # 8:7f08
    rom.write_byte(0x23F09, 0xD2)  # 8:7f09    jp nc, 7F0C
    rom.write_byte(0x23F0A, 0x0C)  # 8:7f0a
    rom.write_byte(0x23F0B, 0x7F)  # 8:7f0b
    # --
    rom.write_byte(0x23F0C, 0xFA)  # 8:7f0c    ld a,(A409)
    rom.write_byte(0x23F0D, 0x09)  # 8:7f0d
    rom.write_byte(0x23F0E, 0xA4)  # 8:7f0e
    rom.write_byte(0x23F0F, 0xA7)  # 8:7f0f    and a
    rom.write_byte(0x23F10, 0xCA)  # 8:7f10    jp z,41C4
    rom.write_byte(0x23F11, 0xC4)  # 8:7f11
    rom.write_byte(0x23F12, 0x41)  # 8:7f12
    rom.write_byte(0x23F13, 0x3E)  # 8:7f13    ld a,23
    rom.write_byte(0x23F14, 0x23)  # 8:7f14
    rom.write_byte(0x23F15, 0xC3)  # 8:7f15    jp 418A
    rom.write_byte(0x23F16, 0x8A)  # 8:7f16
    rom.write_byte(0x23F17, 0x41)  # 8:7f17
    # --
    rom.write_byte(0x23F18, 0xFA)  # 8:7f18    ld a,(A40A)
    rom.write_byte(0x23F19, 0x0A)  # 8:7f19
    rom.write_byte(0x23F1A, 0xA4)  # 8:7f1a
    rom.write_byte(0x23F1B, 0xA7)  # 8:7f1b    and a
    rom.write_byte(0x23F1C, 0xCA)  # 8:7f1c    jp z,41C4
    rom.write_byte(0x23F1D, 0xC4)  # 8:7f1d
    rom.write_byte(0x23F1E, 0x41)  # 8:7f1e
    rom.write_byte(0x23F1F, 0x3E)  # 8:7f1f    ld a,23
    rom.write_byte(0x23F20, 0x23)  # 8:7f20
    rom.write_byte(0x23F21, 0xC3)  # 8:7f21    jp 418A
    rom.write_byte(0x23F22, 0x8A)  # 8:7f22
    rom.write_byte(0x23F23, 0x41)  # 8:7f23
    # --
    rom.write_byte(0x23F24, 0xFA)  # 8:7f24    ld a,(A40B)
    rom.write_byte(0x23F25, 0x0B)  # 8:7f25
    rom.write_byte(0x23F26, 0xA4)  # 8:7f26
    rom.write_byte(0x23F27, 0xA7)  # 8:7f27    and a
    rom.write_byte(0x23F28, 0xCA)  # 8:7f28    jp z,41C4
    rom.write_byte(0x23F29, 0xC4)  # 8:7f29
    rom.write_byte(0x23F2A, 0x41)  # 8:7f2a
    rom.write_byte(0x23F2B, 0x3E)  # 8:7f2b    ld a,23
    rom.write_byte(0x23F2C, 0x23)  # 8:7f2c
    rom.write_byte(0x23F2D, 0xC3)  # 8:7f2d    jp 418A
    rom.write_byte(0x23F2E, 0x8A)  # 8:7f2e
    rom.write_byte(0x23F2F, 0x41)  # 8:7f2f
    # --
    rom.write_byte(0x23F30, 0xFA)  # 8:7f30    ld a,(A40C)
    rom.write_byte(0x23F31, 0x0C)  # 8:7f31
    rom.write_byte(0x23F32, 0xA4)  # 8:7f32
    rom.write_byte(0x23F33, 0xA7)  # 8:7f33    and a
    rom.write_byte(0x23F34, 0xCA)  # 8:7f34    jp z,41C4
    rom.write_byte(0x23F35, 0xC4)  # 8:7f35
    rom.write_byte(0x23F36, 0x41)  # 8:7f36
    rom.write_byte(0x23F37, 0x3E)  # 8:7f37    ld a,23
    rom.write_byte(0x23F38, 0x23)  # 8:7f38
    rom.write_byte(0x23F39, 0xC3)  # 8:7f39    jp 418A
    rom.write_byte(0x23F3A, 0x8A)  # 8:7f3a
    rom.write_byte(0x23F3B, 0x41)  # 8:7f3b
    # --
    rom.write_byte(0x23F3C, 0xFA)  # 8:7f3c    ld a,(A40D)
    rom.write_byte(0x23F3D, 0x0D)  # 8:7f3d
    rom.write_byte(0x23F3E, 0xA4)  # 8:7f3e
    rom.write_byte(0x23F3F, 0xA7)  # 8:7f3f    and a
    rom.write_byte(0x23F40, 0xCA)  # 8:7f40    jp z,41C4
    rom.write_byte(0x23F41, 0xC4)  # 8:7f41
    rom.write_byte(0x23F42, 0x41)  # 8:7f42
    rom.write_byte(0x23F43, 0x3E)  # 8:7f43    ld a,23
    rom.write_byte(0x23F44, 0x23)  # 8:7f44
    rom.write_byte(0x23F45, 0xC3)  # 8:7f45    jp 418A
    rom.write_byte(0x23F46, 0x8A)  # 8:7f46
    rom.write_byte(0x23F47, 0x41)  # 8:7f47
    # --
    rom.write_byte(0x23F48, 0xFA)  # 8:7f48    ld a,(A40E)
    rom.write_byte(0x23F49, 0x0E)  # 8:7f49
    rom.write_byte(0x23F4A, 0xA4)  # 8:7f4a
    rom.write_byte(0x23F4B, 0xA7)  # 8:7f4b    and a
    rom.write_byte(0x23F4C, 0xCA)  # 8:7f4c    jp z,41C4
    rom.write_byte(0x23F4D, 0xC4)  # 8:7f4d
    rom.write_byte(0x23F4E, 0x41)  # 8:7f4e
    rom.write_byte(0x23F4F, 0x3E)  # 8:7f4f    ld a,23
    rom.write_byte(0x23F50, 0x23)  # 8:7f50
    rom.write_byte(0x23F51, 0xC3)  # 8:7f51    jp 418A
    rom.write_byte(0x23F52, 0x8A)  # 8:7f52
    rom.write_byte(0x23F53, 0x41)  # 8:7f53
    # --
    rom.write_byte(0x23F54, 0xFA)  # 8:7f54    ld a,(A40F)
    rom.write_byte(0x23F55, 0x0F)  # 8:7f55
    rom.write_byte(0x23F56, 0xA4)  # 8:7f56
    rom.write_byte(0x23F57, 0xA7)  # 8:7f57    and a
    rom.write_byte(0x23F58, 0xCA)  # 8:7f58    jp z,41C4
    rom.write_byte(0x23F59, 0xC4)  # 8:7f59
    rom.write_byte(0x23F5A, 0x41)  # 8:7f5a
    rom.write_byte(0x23F5B, 0x3E)  # 8:7f5b    ld a,23
    rom.write_byte(0x23F5C, 0x23)  # 8:7f5c
    rom.write_byte(0x23F5D, 0xC3)  # 8:7f5d    jp 418A
    rom.write_byte(0x23F5E, 0x8A)  # 8:7f5e
    rom.write_byte(0x23F5F, 0x41)  # 8:7f5f
    # --
    rom.write_byte(0x23F60, 0xC3)  # 8:7f60    jp 41C4
    rom.write_byte(0x23F61, 0xC4)  # 8:7f61
    rom.write_byte(0x23F62, 0x41)  # 8:7f62


def patch_world_movement(rom):
    # Block boss level entry
    rom.write_byte(0x21D76, 0xC3)  # 8:5d76    jp 7f63
    rom.write_byte(0x21D77, 0x63)  # 8:5d77
    rom.write_byte(0x21D78, 0x7F)  # 8:5d78
    # --
    rom.write_byte(0x23F63, 0xFA)  # 8:7f63    ld a,(A79E)
    rom.write_byte(0x23F64, 0x9E)  # 8:7f64
    rom.write_byte(0x23F65, 0xA7)  # 8:7f65
    rom.write_byte(0x23F66, 0xFE)  # 8:7f66    cp a,19
    rom.write_byte(0x23F67, 0x19)  # 8:7f67
    rom.write_byte(0x23F68, 0xFA)  # 8:7f68    ld a,(A421)
    rom.write_byte(0x23F69, 0x21)  # 8:7f69
    rom.write_byte(0x23F6A, 0xA4)  # 8:7f6a
    rom.write_byte(0x23F6B, 0xCA)  # 8:7f6b    jp z, 7FB2
    rom.write_byte(0x23F6C, 0xB2)  # 8:7f6c
    rom.write_byte(0x23F6D, 0x7F)  # 8:7f6d
    rom.write_byte(0x23F6E, 0xFA)  # 8:7f6e    ld a,(A79E)
    rom.write_byte(0x23F6F, 0x9E)  # 8:7f6f
    rom.write_byte(0x23F70, 0xA7)  # 8:7f70
    rom.write_byte(0x23F71, 0xFE)  # 8:7f71    cp a,0A
    rom.write_byte(0x23F72, 0x0A)  # 8:7f72
    rom.write_byte(0x23F73, 0xFA)  # 8:7f73    ld a,(A422)
    rom.write_byte(0x23F74, 0x22)  # 8:7f74
    rom.write_byte(0x23F75, 0xA4)  # 8:7f75
    rom.write_byte(0x23F76, 0xCA)  # 8:7f76    jp z, 7FB2
    rom.write_byte(0x23F77, 0xB2)  # 8:7f77
    rom.write_byte(0x23F78, 0x7F)  # 8:7f78
    rom.write_byte(0x23F79, 0xFA)  # 8:7f79    ld a,(A79E)
    rom.write_byte(0x23F7A, 0x9E)  # 8:7f7a
    rom.write_byte(0x23F7B, 0xA7)  # 8:7f7b
    rom.write_byte(0x23F7C, 0xFE)  # 8:7f7c    cp a,18
    rom.write_byte(0x23F7D, 0x18)  # 8:7f7d
    rom.write_byte(0x23F7E, 0xFA)  # 8:7f7e    ld a,(A426)
    rom.write_byte(0x23F7F, 0x26)  # 8:7f7f
    rom.write_byte(0x23F80, 0xA4)  # 8:7f80
    rom.write_byte(0x23F81, 0xCA)  # 8:7f81    jp z, 7FB2
    rom.write_byte(0x23F82, 0xB2)  # 8:7f82
    rom.write_byte(0x23F83, 0x7F)  # 8:7f83
    rom.write_byte(0x23F84, 0xFA)  # 8:7f84    ld a,(A79E)
    rom.write_byte(0x23F85, 0x9E)  # 8:7f85
    rom.write_byte(0x23F86, 0xA7)  # 8:7f86
    rom.write_byte(0x23F87, 0xFE)  # 8:7f87    cp a,1C
    rom.write_byte(0x23F88, 0x1C)  # 8:7f88
    rom.write_byte(0x23F89, 0xFA)  # 8:7f89    ld a,(A423)
    rom.write_byte(0x23F8A, 0x23)  # 8:7f8a
    rom.write_byte(0x23F8B, 0xA4)  # 8:7f8b
    rom.write_byte(0x23F8C, 0xCA)  # 8:7f8c    jp z, 7FB2
    rom.write_byte(0x23F8D, 0xB2)  # 8:7f8d
    rom.write_byte(0x23F8E, 0x7F)  # 8:7f8e
    rom.write_byte(0x23F8F, 0xFA)  # 8:7f8f    ld a,(A79E)
    rom.write_byte(0x23F90, 0x9E)  # 8:7f90
    rom.write_byte(0x23F91, 0xA7)  # 8:7f91
    rom.write_byte(0x23F92, 0xFE)  # 8:7f92    cp a,14
    rom.write_byte(0x23F93, 0x14)  # 8:7f93
    rom.write_byte(0x23F94, 0xFA)  # 8:7f94    ld a,(A425)
    rom.write_byte(0x23F95, 0x25)  # 8:7f95
    rom.write_byte(0x23F96, 0xA4)  # 8:7f96
    rom.write_byte(0x23F97, 0xCA)  # 8:7f97    jp z, 7FB2
    rom.write_byte(0x23F98, 0xB2)  # 8:7f98
    rom.write_byte(0x23F99, 0x7F)  # 8:7f99
    rom.write_byte(0x23F9A, 0xFA)  # 8:7f9a    ld a,(A79E)
    rom.write_byte(0x23F9B, 0x9E)  # 8:7f9b
    rom.write_byte(0x23F9C, 0xA7)  # 8:7f9c
    rom.write_byte(0x23F9D, 0xFE)  # 8:7f9d    cp a,1A
    rom.write_byte(0x23F9E, 0x1A)  # 8:7f9e
    rom.write_byte(0x23F9F, 0xFA)  # 8:7f9f    ld a,(A424)
    rom.write_byte(0x23FA0, 0x24)  # 8:7fa0
    rom.write_byte(0x23FA1, 0xA4)  # 8:7fa1
    rom.write_byte(0x23FA2, 0xCA)  # 8:7fa2    jp z, 7FB2
    rom.write_byte(0x23FA3, 0xB2)  # 8:7fa3
    rom.write_byte(0x23FA4, 0x7F)  # 8:7fa4
    rom.write_byte(0x23FA5, 0xFA)  # 8:7fa5    ld a,(A79E)
    rom.write_byte(0x23FA6, 0x9E)  # 8:7fa6
    rom.write_byte(0x23FA7, 0xA7)  # 8:7fa7
    rom.write_byte(0x23FA8, 0xFE)  # 8:7fa8    cp a,28
    rom.write_byte(0x23FA9, 0x28)  # 8:7fa9
    rom.write_byte(0x23FAA, 0xFA)  # 8:7faa    ld a,(A427)
    rom.write_byte(0x23FAB, 0x27)  # 8:7fab
    rom.write_byte(0x23FAC, 0xA4)  # 8:7fac
    rom.write_byte(0x23FAD, 0xCA)  # 8:7fad    jp z, 7FB2
    rom.write_byte(0x23FAE, 0xB2)  # 8:7fae
    rom.write_byte(0x23FAF, 0x7F)  # 8:7faf
    rom.write_byte(0x23FB0, 0x3E)  # 8:7fb0    ld a,1
    rom.write_byte(0x23FB1, 0x01)  # 8:7fb1
    rom.write_byte(0x23FB2, 0xA7)  # 8:7fb2    and a
    rom.write_byte(0x23FB3, 0xCA)  # 8:7fb3    jp z, 7FBE
    rom.write_byte(0x23FB4, 0xBE)  # 8:7fb4
    rom.write_byte(0x23FB5, 0x7F)  # 8:7fb5
    rom.write_byte(0x23FB6, 0x3E)  # 8:7fb6    ld a,2b
    rom.write_byte(0x23FB7, 0x2B)  # 8:7fb7
    rom.write_byte(0x23FB8, 0xEA)  # 8:7fb8    ld (A61C),a
    rom.write_byte(0x23FB9, 0x1C)  # 8:7fb9
    rom.write_byte(0x23FBA, 0xA6)  # 8:7fba
    rom.write_byte(0x23FBB, 0xC3)  # 8:7fbb    jp 5D79
    rom.write_byte(0x23FBC, 0x79)  # 8:7fbc
    rom.write_byte(0x23FBD, 0x5D)  # 8:7fbd
    rom.write_byte(0x23FBE, 0xC3)  # 8:7fbe    jp 5D7D
    rom.write_byte(0x23FBF, 0x7D)  # 8:7fbf
    rom.write_byte(0x23FC0, 0x5D)  # 8:7fc0

    # Overworld movement

    # Rice beach
    rom.write_byte(0x22320, 0x1A)  # 8:6320    ld a,(A41A)
    rom.write_byte(0x22321, 0xA4)  # 8:6321
    # Mt teapot
    rom.write_byte(0x22333, 0x1B)  # 8:6333    ld a,(A41B)
    rom.write_byte(0x22334, 0xA4)  # 8:6334
    # Stove canyon
    rom.write_byte(0x22346, 0x1C)  # 8:6346    ld a,(A41C)
    rom.write_byte(0x22347, 0xA4)  # 8:6347
    # Ss teacup
    rom.write_byte(0x22359, 0x1D)  # 8:6359    ld a,(A41D)
    rom.write_byte(0x2235A, 0xA4)  # 8:635a
    # Parsley woods
    rom.write_byte(0x2236C, 0x1E)  # 8:636c    ld a,(A41E)
    rom.write_byte(0x2236D, 0xA4)  # 8:636d
    # Sherbet land
    rom.write_byte(0x2237F, 0x1F)  # 8:637f    ld a,(A41F)
    rom.write_byte(0x22380, 0xA4)  # 8:6380
    # Syrup castle
    rom.write_byte(0x22392, 0x20)  # 8:6392    ld a,(A420)
    rom.write_byte(0x22393, 0xA4)  # 8:6393

    # Subworld movement

    # Rice beach
    rom.write_byte(0x22416, 0x13)  # 8:6416    ld a,(A413)
    rom.write_byte(0x22417, 0xA4)  # 8:6417
    # Mt teapot
    rom.write_byte(0x22407, 0x14)  # 8:6407    ld a,(A414)
    rom.write_byte(0x22408, 0xA4)  # 8:6408
    # Stove canyon
    rom.write_byte(0x223F8, 0x15)  # 8:63f8    ld a,(A415)
    rom.write_byte(0x223F9, 0xA4)  # 8:63f9
    # Ss teacup
    rom.write_byte(0x223E9, 0x16)  # 8:63e9    ld a,(A416)
    rom.write_byte(0x223EA, 0xA4)  # 8:63ea
    # Parsley woods
    rom.write_byte(0x223DA, 0x17)  # 8:63da    ld a,(A417)
    rom.write_byte(0x223DB, 0xA4)  # 8:63db
    # Sherbet land
    rom.write_byte(0x223CB, 0x18)  # 8:63cb    ld a,(A418)
    rom.write_byte(0x223CC, 0xA4)  # 8:63cc
    # Syrup castle
    rom.write_byte(0x223BC, 0x19)  # 8:63bc    ld a,(A419)
    rom.write_byte(0x223BD, 0xA4)  # 8:63bd
    return


# Fix bugs that appear due to changes in game structure
def apply_fixes(rom):
    # Fix syrup castle cutscene
    rom.write_byte(0x23AF3, 0xC1)  # 8:7af3    ld a,(46C1)
    rom.write_byte(0x23AF4, 0x46)  # 8:7af4
    rom.write_byte(0x23B21, 0xC1)  # 8:7b21    ld a,(46C1)
    rom.write_byte(0x23B22, 0x46)  # 8:7b22

    # Fix parsley woods overworld movement
    rom.write_byte(0x20177, 0xFA)  # 8:4177    ld a,(43C9)
    rom.write_byte(0x20178, 0xC9)  # 8:4178
    rom.write_byte(0x20179, 0x43)  # 8:4179
    return


# Turn autoscrollers into normal scrolling screens
def remove_autoscrolling(rom):
    rom.write_byte(0x31D19, 0x1)  # c:5d19
    rom.write_byte(0x31D49, 0x1)  # c:5d49
    rom.write_byte(0x32B89, 0x1)  # c:6b89
    rom.write_byte(0x32BB9, 0x1)  # c:6bb9


# Force max speed value for post-level bonus select
def speedups(rom):
    rom.write_byte(0x465E, 0x3E)  # 1:465e     ld a,ff
    rom.write_byte(0x465F, 0xFF)  # 1:465f
    rom.write_byte(0x4660, 0x00)  # 1:4660     nop


# Block player from using saveslot 3, repurposed for multiworld save data
def remove_saveslot_three(rom):
    rom.write_byte(0x74A5, 0xCD)  # 1:74a5     call 7B82
    rom.write_byte(0x74A6, 0x82)  # 1:74a6
    rom.write_byte(0x74A7, 0x7B)  # 1:74a7
    rom.write_byte(0x7B82, 0xFE)  # 1:7b82     cp a,02
    rom.write_byte(0x7B83, 0x02)  # 1:7b83
    rom.write_byte(0x7B84, 0xC2)  # 1:7b84     jp nz, 7B89
    rom.write_byte(0x7B85, 0x89)  # 1:7b85
    rom.write_byte(0x7B86, 0x7B)  # 1:7b86
    rom.write_byte(0x7B87, 0x3E)  # 1:7b87     ld a,01
    rom.write_byte(0x7B88, 0x01)  # 1:7b88
    rom.write_byte(0x7B89, 0xEA)  # 1:7b89     ld (A0C3),a
    rom.write_byte(0x7B8A, 0xC3)  # 1:7b8a
    rom.write_byte(0x7B8B, 0xA0)  # 1:7b8b
    rom.write_byte(0x7B8C, 0xC9)  # 1:7b8c     ret


# Fix internal checksums
def fix_checksum(rom):
    # Header checksum first
    checksum = 0
    for c in rom.buffer[0x134:0x14D]:
        checksum -= c + 1
    rom.write_byte(0x14D, checksum & 0xFF)

    # Clear ROM checksum bytes before calculation
    rom.buffer[0x14E] = 0
    rom.buffer[0x14F] = 0
    checksum = 0
    for byte in rom.buffer:
        checksum += byte
    checksum_b1 = (checksum >> 8) & 0xFF
    checksum_b2 = (checksum) & 0xFF
    rom.write_byte(0x14E, checksum_b1)
    rom.write_byte(0x14F, checksum_b2)


def custom_level_table(rom):
    # Patch level exit value
    rom.write_byte(0x04A9F, 0x9E)  # 1:4a9f    ld a,(A79E)
    rom.write_byte(0x04AA0, 0xA7)  # 1:4aa0

    # Hook into level loading method
    rom.write_byte(0x21DAC, 0xCD)  # 8:5dac    call 7FC1
    rom.write_byte(0x21DAD, 0xC1)  # 8:5dad
    rom.write_byte(0x21DAE, 0x7F)  # 8:5dae

    rom.write_byte(0x23FC1, 0xFA)  # 8:7fc1    ld	a,(A79E)
    rom.write_byte(0x23FC2, 0x9E)  # 8:7fc2
    rom.write_byte(0x23FC3, 0xA7)  # 8:7fc3
    rom.write_byte(0x23FC4, 0x4F)  # 8:7fc4    ld	c, a
    rom.write_byte(0x23FC5, 0x06)  # 8:7fc5    ld	b, 00
    rom.write_byte(0x23FC6, 0x00)  # 8:7fc6
    rom.write_byte(0x23FC7, 0x21)  # 8:7fc7    ld	hl, 7FCD
    rom.write_byte(0x23FC8, 0xCD)  # 8:7fc8
    rom.write_byte(0x23FC9, 0x7F)  # 8:7fc9
    rom.write_byte(0x23FCA, 0x09)  # 8:7fca    add	hl, bc
    rom.write_byte(0x23FCB, 0x7E)  # 8:7fcb    ld	a, [hl]
    rom.write_byte(0x23FCC, 0xC9)  # 8:7fcc    ret

    # Start of custom level table
    rom.write_byte(0x23FCD, 0x00)  # 8:7fcd
    rom.write_byte(0x23FCE, 0x01)  # 8:7fce
    rom.write_byte(0x23FCF, 0x02)  # 8:7fcf
    rom.write_byte(0x23FD0, 0x03)  # 8:7fd0
    rom.write_byte(0x23FD1, 0x04)  # 8:7fd1
    rom.write_byte(0x23FD2, 0x05)  # 8:7fd2
    rom.write_byte(0x23FD3, 0x06)  # 8:7fd3
    rom.write_byte(0x23FD4, 0x07)  # 8:7fd4
    rom.write_byte(0x23FD5, 0x08)  # 8:7fd5
    rom.write_byte(0x23FD6, 0x09)  # 8:7fd6
    rom.write_byte(0x23FD7, 0x0A)  # 8:7fd7
    rom.write_byte(0x23FD8, 0x0B)  # 8:7fd8
    rom.write_byte(0x23FD9, 0x0C)  # 8:7fd9
    rom.write_byte(0x23FDA, 0x0D)  # 8:7fda
    rom.write_byte(0x23FDB, 0x0E)  # 8:7fdb
    rom.write_byte(0x23FDC, 0x0F)  # 8:7fdc
    rom.write_byte(0x23FDD, 0x10)  # 8:7fdd
    rom.write_byte(0x23FDE, 0x11)  # 8:7fde
    rom.write_byte(0x23FDF, 0x12)  # 8:7fdf
    rom.write_byte(0x23FE0, 0x13)  # 8:7fe0
    rom.write_byte(0x23FE1, 0x14)  # 8:7fe1
    rom.write_byte(0x23FE2, 0x15)  # 8:7fe2
    rom.write_byte(0x23FE3, 0x16)  # 8:7fe3
    rom.write_byte(0x23FE4, 0x17)  # 8:7fe4
    rom.write_byte(0x23FE5, 0x18)  # 8:7fe5
    rom.write_byte(0x23FE6, 0x19)  # 8:7fe6
    rom.write_byte(0x23FE7, 0x1A)  # 8:7fe7
    rom.write_byte(0x23FE8, 0x1B)  # 8:7fe8
    rom.write_byte(0x23FE9, 0x1C)  # 8:7fe9
    rom.write_byte(0x23FEA, 0x1D)  # 8:7fea
    rom.write_byte(0x23FEB, 0x1E)  # 8:7feb
    rom.write_byte(0x23FEC, 0x1F)  # 8:7fec
    rom.write_byte(0x23FED, 0x20)  # 8:7fed
    rom.write_byte(0x23FEE, 0x21)  # 8:7fee
    rom.write_byte(0x23FEF, 0x22)  # 8:7fef
    rom.write_byte(0x23FF0, 0x23)  # 8:7ff0
    rom.write_byte(0x23FF1, 0x24)  # 8:7ff1
    rom.write_byte(0x23FF2, 0x25)  # 8:7ff2
    rom.write_byte(0x23FF3, 0x26)  # 8:7ff3
    rom.write_byte(0x23FF4, 0x27)  # 8:7ff4
    rom.write_byte(0x23FF5, 0x28)  # 8:7ff5
    # End of custom level table


# Shuffles the level music in vanilla limitations
def shuffle_music(rom, level_music):
    level_music_addr = [
        0x33ECD,
        0x33ED9,
        0x33EE5,
        0x33EF1,
        0x33EFD,
        0x33F09,
        0x33F15,
        0x33F21,
        0x33F2D,
        0x33F39,
        0x33F45,
        0x33F51,
        0x33F5D,
    ]
    # Second address always + 0x03 away
    for music_offset in level_music_addr:
        music_pick = level_music.pop()
        rom.write_byte(music_offset, music_pick)
        rom.write_byte(music_offset + 0x03, music_pick)


def blocksanity(rom):
    rom.write_byte(0x153A, 0xC3)  # 0:153a    jp 3C00
    rom.write_byte(0x153B, 0x00)  # 0:153b
    rom.write_byte(0x153C, 0x3C)  # 0:153c
    # ---
    rom.write_byte(0x3C00, 0xFA)  # 0:3c00    ld a,(A42F)
    rom.write_byte(0x3C01, 0x2F)  # 0:3c01
    rom.write_byte(0x3C02, 0xA4)  # 0:3c02
    rom.write_byte(0x3C03, 0xFE)  # 0:3c03    cp a,0
    rom.write_byte(0x3C04, 0x00)  # 0:3c04
    rom.write_byte(0x3C05, 0xC2)  # 0:3c05    jp nz, 3C0E
    rom.write_byte(0x3C06, 0x0E)  # 0:3c06
    rom.write_byte(0x3C07, 0x3C)  # 0:3c07
    rom.write_byte(0x3C08, 0x21)  # 0:3c08    ld hl,A430
    rom.write_byte(0x3C09, 0x30)  # 0:3c09
    rom.write_byte(0x3C0A, 0xA4)  # 0:3c0a
    rom.write_byte(0x3C0B, 0xC3)  # 0:3c0b    jp 3C1B
    rom.write_byte(0x3C0C, 0x1B)  # 0:3c0c
    rom.write_byte(0x3C0D, 0x3C)  # 0:3c0d
    rom.write_byte(0x3C0E, 0xFA)  # 0:3c0e    ld a,(A42E)
    rom.write_byte(0x3C0F, 0x2E)  # 0:3c0f
    rom.write_byte(0x3C10, 0xA4)  # 0:3c10
    rom.write_byte(0x3C11, 0xFE)  # 0:3c11    cp a,6C
    rom.write_byte(0x3C12, 0x6C)  # 0:3c12
    rom.write_byte(0x3C13, 0xD2)  # 0:3c13    jp nc, 3C08
    rom.write_byte(0x3C14, 0x08)  # 0:3c14
    rom.write_byte(0x3C15, 0x3C)  # 0:3c15
    rom.write_byte(0x3C16, 0x6F)  # 0:3c16    ld l, a
    rom.write_byte(0x3C17, 0xFA)  # 0:3c17    ld a,(A42F)
    rom.write_byte(0x3C18, 0x2F)  # 0:3c18
    rom.write_byte(0x3C19, 0xA4)  # 0:3c19
    rom.write_byte(0x3C1A, 0x67)  # 0:3c1a    ld h, a
    rom.write_byte(0x3C1B, 0xFA)  # 0:3c1b    ld a,(A918)
    rom.write_byte(0x3C1C, 0x18)  # 0:3c1c
    rom.write_byte(0x3C1D, 0xA9)  # 0:3c1d
    rom.write_byte(0x3C1E, 0x22)  # 0:3c1e    ldi (hl),a
    rom.write_byte(0x3C1F, 0xFA)  # 0:3c1f    ld a,(A919)
    rom.write_byte(0x3C20, 0x19)  # 0:3c20
    rom.write_byte(0x3C21, 0xA9)  # 0:3c21
    rom.write_byte(0x3C22, 0x22)  # 0:3c22    ldi (hl),a
    rom.write_byte(0x3C23, 0x7C)  # 0:3c23    ld a, h
    rom.write_byte(0x3C24, 0xEA)  # 0:3c24    ld (A42F),a
    rom.write_byte(0x3C25, 0x2F)  # 0:3c25
    rom.write_byte(0x3C26, 0xA4)  # 0:3c26
    rom.write_byte(0x3C27, 0x7D)  # 0:3c27    ld a, l
    rom.write_byte(0x3C28, 0xEA)  # 0:3c28    ld (A42E),a
    rom.write_byte(0x3C29, 0x2E)  # 0:3c29
    rom.write_byte(0x3C2A, 0xA4)  # 0:3c2a
    rom.write_byte(0x3C2B, 0xFA)  # 0:3c2b    ld a,(A918)
    rom.write_byte(0x3C2C, 0x18)  # 0:3c2c
    rom.write_byte(0x3C2D, 0xA9)  # 0:3c2d
    rom.write_byte(0x3C2E, 0x67)  # 0:3c2e    ld h, a
    rom.write_byte(0x3C2F, 0xFA)  # 0:3c2f    ld a,(A919)
    rom.write_byte(0x3C30, 0x19)  # 0:3c30
    rom.write_byte(0x3C31, 0xA9)  # 0:3c31
    rom.write_byte(0x3C32, 0x6F)  # 0:3c32    ld l, a
    rom.write_byte(0x3C33, 0xC3)  # 0:3c33    jp 1542
    rom.write_byte(0x3C34, 0x42)  # 0:3c34
    rom.write_byte(0x3C35, 0x15)  # 0:3c35


def patch_rom(world, rom):
    multiworld = world.multiworld
    options = world.options
    player = world.player

    # Starting Life Count, hex equals displayed value directly
    rom.write_byte(0x7B7D, int(str(options.starting_life_count.value), 16))

    patch_basic_abilities(rom)
    patch_powerups(rom)
    patch_world_movement(rom)
    speedups(rom)
    apply_fixes(rom)
    patch_world_enter(rom)

    if options.blocksanity:
        blocksanity(rom)
    if options.remove_autoscrollers:
        remove_autoscrolling(rom)
    if options.music_shuffle:
        level_music = [
            0x03,
            0x04,
            0x09,
            0x0A,
            0x0B,
            0x0E,
            0x10,
            0x16,
            0x17,
            0x1B,
            0x1E,
            0x22,
            0x27,
        ]
        world.random.shuffle(level_music)
        shuffle_music(rom, level_music)

    # TODO: This patch is not required until level shuffle mode exists
    # custom_level_table(rom)
    # TODO: this is broken on gambatte but works fine on bgb, no idea why :(
    # remove_saveslot_three(rom)

    from Utils import __version__

    rom.name = bytearray(
        f'WL{__version__.replace(".", "")[0:3]}_{player}_{multiworld.seed:11}\0', "utf8"
    )[:21]
    rom.name.extend([0] * (21 - len(rom.name)))

    player_name_length = 0
    # Write slot info to ROM
    for i, byte in enumerate(multiworld.player_name[player].encode("utf-8")):
        rom.write_byte(0x674B1 + i, byte)
        player_name_length += 1
    rom.write_byte(0x674B0, player_name_length)

    # Re-write header title
    new_title = "WARIOLANDAP"
    for i, byte in enumerate(new_title.encode("utf-8")):
        rom.write_byte(0x134 + i, byte)

    for i in range(5):
        rom.write_byte(0x13F + i, 0x00)
    # Fix checksums so emulators don't complain
    fix_checksum(rom)
