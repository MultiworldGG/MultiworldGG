"""CD-ROM XA Mode 2 Form 1 sector checksums (pure Python, no dependencies).

A raw 2352-byte sector is sync (12) + header (4) + subheader (8) + 2048 data + EDC (4) + ECC (276).
Changing data bytes in a raw image means the sector's EDC and ECC must be rewritten, or hardware
and strict emulators see a corrupt sector.  Algorithm as in ECMA-130 / cdrtools edc_ecc.c.

Single source: dw_decomp/tools/cd_sector.py.  tools/build_variants.py copies it next to the
apworld (Apworld/dw1/cd_sector.py), where generate_output() uses it to rebuild the EXTINIT.BIN
sector that holds the custom-digimon enable table.
"""

RAW_SECTOR = 2352
SYNC_SIZE = 12
HEADER_OFF = 12
SUBHEADER_OFF = 16
DATA_OFF = 24
DATA_SIZE = 2048
EDC_OFF = 2072
ECC_P_OFF = 2076
ECC_Q_OFF = 2248

_EDC_TABLE = []
for _i in range(256):
    _e = _i
    for _ in range(8):
        _e = (_e >> 1) ^ (0xD8018001 if _e & 1 else 0)
    _EDC_TABLE.append(_e)

_F_LUT = [0] * 256     # multiply by alpha in GF(2^8), polynomial 0x11D
_B_LUT = [0] * 256     # inverse of (x ^ alpha*x)
for _i in range(256):
    _j = ((_i << 1) ^ (0x11D if _i & 0x80 else 0)) & 0xFF
    _F_LUT[_i] = _j
    _B_LUT[_i ^ _j] = _i


def edc(data) -> int:
    e = 0
    for b in data:
        e = (e >> 8) ^ _EDC_TABLE[(e ^ b) & 0xFF]
    return e


def _ecc_block(src, major_count, minor_count, major_mult, minor_inc):
    size = major_count * minor_count
    out = bytearray(2 * major_count)
    for major in range(major_count):
        index = (major >> 1) * major_mult + (major & 1)
        a = b = 0
        for _ in range(minor_count):
            t = src[index]
            index += minor_inc
            if index >= size:
                index -= size
            a ^= t
            b ^= t
            a = _F_LUT[a]
        a = _B_LUT[_F_LUT[a] ^ b]
        out[major] = a
        out[major + major_count] = a ^ b
    return bytes(out)


def is_form1(sector) -> bool:
    """Mode 2 and subheader submode bit 5 (Form 2) clear."""
    return sector[15] == 2 and not (sector[18] & 0x20)


def fix_sector(sector) -> bytes:
    """Return the sector with EDC and ECC recomputed from its subheader + data (Mode 2 Form 1)."""
    if len(sector) != RAW_SECTOR:
        raise ValueError(f"raw sector must be {RAW_SECTOR} bytes, got {len(sector)}")
    s = bytearray(sector)
    s[EDC_OFF:EDC_OFF + 4] = edc(s[SUBHEADER_OFF:EDC_OFF]).to_bytes(4, 'little')
    # ECC over header (zeroed for Form 1) + subheader + data + EDC (bytes 12..2075); the Q
    # parity also covers the P parity just written (bytes 2076..2247).
    blk = bytearray(s[HEADER_OFF:ECC_Q_OFF])
    blk[0:4] = bytes(4)
    blk[ECC_P_OFF - HEADER_OFF:] = _ecc_block(blk, 86, 24, 2, 86)
    s[ECC_P_OFF:ECC_Q_OFF] = blk[ECC_P_OFF - HEADER_OFF:]
    s[ECC_Q_OFF:RAW_SECTOR] = _ecc_block(blk, 52, 43, 86, 88)
    return bytes(s)


def patch_sector(sector, changes) -> bytes:
    """changes: {offset_in_sector: byte} for data-region bytes; returns the fixed sector."""
    s = bytearray(sector)
    for off, val in changes.items():
        off = int(off)
        if not DATA_OFF <= off < EDC_OFF:
            raise ValueError(f"offset {off} is outside the sector's data region")
        s[off] = val
    return fix_sector(s)
