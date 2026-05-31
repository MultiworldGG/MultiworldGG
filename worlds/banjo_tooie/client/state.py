"""Read-only N64 RAM state pollers.

Author: Umed (UmedMuzl).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Optional

from . import addresses

if TYPE_CHECKING:
    from ..BTClient import BTEmuLoaderClient

ANCHOR_VERSION = 0x00
ANCHOR_PC = 0x04
ANCHOR_PC_MESSAGES = 0x08
ANCHOR_SIGNPOST_MESSAGES = 0x0C
ANCHOR_PC_SETTINGS = 0x10
ANCHOR_PC_ITEMS = 0x14
ANCHOR_PC_TRAPS = 0x18
ANCHOR_PC_EXIT_MAP = 0x1C
ANCHOR_N64 = 0x20
ANCHOR_REAL_FLAGS = 0x24
ANCHOR_FAKE_FLAGS = 0x28
ANCHOR_NEST_FLAGS = 0x2C
ANCHOR_SIGNPOST_FLAGS = 0x30

PC_DEATH_US = 0x0
PC_DEATH_AP = 0x1
PC_TAG_US = 0x2
PC_TAG_AP = 0x3

N64_SHOW_TEXT = 0x0
N64_DEATH_US = 0x1
N64_DEATH_AP = 0x2
N64_TAG_US = 0x3
N64_TAG_AP = 0x4
N64_CURRENT_MAP = 0x6  # u16 BE


class BTHReader:
    """Pointer-chase + flag-check helpers for the BTHACK injected struct."""

    def __init__(self, loader: BTEmuLoaderClient):
        self.loader = loader

    # ----- anchor + per-field deref -----

    def anchor(self) -> Optional[int]:
        return self.loader.get_anchor()

    def sub_ptr(self, field_offset: int) -> Optional[int]:
        a = self.anchor()
        if a is None:
            return None
        return self.loader.deref(a + field_offset)

    def pc_ptr(self) -> Optional[int]:
        return self.sub_ptr(ANCHOR_PC)

    def n64_ptr(self) -> Optional[int]:
        return self.sub_ptr(ANCHOR_N64)

    def settings_ptr(self) -> Optional[int]:
        return self.sub_ptr(ANCHOR_PC_SETTINGS)

    def items_ptr(self) -> Optional[int]:
        return self.sub_ptr(ANCHOR_PC_ITEMS)

    def traps_ptr(self) -> Optional[int]:
        return self.sub_ptr(ANCHOR_PC_TRAPS)

    def exit_map_ptr(self) -> Optional[int]:
        return self.sub_ptr(ANCHOR_PC_EXIT_MAP)

    def pc_messages_ptr(self) -> Optional[int]:
        return self.sub_ptr(ANCHOR_PC_MESSAGES)

    def signpost_messages_ptr(self) -> Optional[int]:
        return self.sub_ptr(ANCHOR_SIGNPOST_MESSAGES)

    def real_flags_ptr(self) -> Optional[int]:
        return self.sub_ptr(ANCHOR_REAL_FLAGS)

    def fake_flags_ptr(self) -> Optional[int]:
        return self.sub_ptr(ANCHOR_FAKE_FLAGS)

    def nest_flags_ptr(self) -> Optional[int]:
        return self.sub_ptr(ANCHOR_NEST_FLAGS)

    def signpost_flags_ptr(self) -> Optional[int]:
        return self.sub_ptr(ANCHOR_SIGNPOST_FLAGS)

    # ----- flag checks -----

    def bit_at(self, ptr: Optional[int], addr: int, bit: int) -> bool:
        if ptr is None:
            return False
        byte = self.loader.read_u8(ptr + addr)
        return ((byte >> bit) & 1) == 1

    def check_real_flag(self, addr: int, bit: int) -> bool:
        return self.bit_at(self.real_flags_ptr(), addr, bit)

    def check_fake_flag(self, addr: int, bit: int) -> bool:
        return self.bit_at(self.fake_flags_ptr(), addr, bit)

    def check_nest_flag(self, bytebit: int) -> bool:
        return self.bit_at(self.nest_flags_ptr(), bytebit // 8, bytebit % 8)

    def check_signpost_flag(self, bytebit: int) -> bool:
        return self.bit_at(self.signpost_flags_ptr(), bytebit // 8, bytebit % 8)

    # ----- game state -----

    def current_map(self) -> int:
        n64 = self.n64_ptr()
        if n64 is None:
            return 0
        return self.loader.read_u16(n64 + N64_CURRENT_MAP)

    def pc_death(self) -> int:
        pc = self.pc_ptr()
        return self.loader.read_u8(pc + PC_DEATH_US) if pc is not None else 0

    def pc_tag(self) -> int:
        pc = self.pc_ptr()
        return self.loader.read_u8(pc + PC_TAG_US) if pc is not None else 0

    def n64_death(self) -> int:
        n64 = self.n64_ptr()
        return self.loader.read_u8(n64 + N64_DEATH_US) if n64 is not None else 0

    def n64_tag(self) -> int:
        n64 = self.n64_ptr()
        return self.loader.read_u8(n64 + N64_TAG_US) if n64 is not None else 0


# Comprehensive polling
def poll_all_locations(bth: BTHReader) -> Dict[int, bool]:
    """Read every known location flag.

      - NESTS / SIGNPOSTS use bytebit indices into the nest/signpost bitmaps.
      - STOPNSWAP is mixed: three btids use real_flags, the rest use fake_flags.
      - HONEYB rewards are a 3-bit *cumulative count*: fake_flags(0x98) bits
        2|3|4 carry weights 1|2|4, summed to give "rewards collected so far"
        (1..5). The first N HONEYB btids are then marked collected together.
      - SKIVVIES use real_flags per location plus a completion override at
        real_flags(0x81, 3) which marks all of them collected at once.
    """
    out: Dict[int, bool] = {}

    for btid, spec in addresses.LOCATION_FLAGS.items():
        ft = spec.flag_type
        if ft == "real":
            out[btid] = bth.check_real_flag(spec.addr, spec.bit)
        elif ft == "fake":
            out[btid] = bth.check_fake_flag(spec.addr, spec.bit)
        elif ft == "nest_flags":
            out[btid] = bth.check_nest_flag(spec.addr)
        elif ft == "signpost_flags":
            out[btid] = bth.check_signpost_flag(spec.addr)
        # special tags handled below

    for btid, spec in addresses.BY_CATEGORY.get("STOPNSWAP", {}).items():
        if btid in addresses.STOPNSWAP_REAL_FLAG_BTIDS:
            out[btid] = bth.check_real_flag(spec.addr, spec.bit)
        else:
            out[btid] = bth.check_fake_flag(spec.addr, spec.bit)

    honeyb_count = (
        (1 if bth.check_fake_flag(0x98, 2) else 0)
        + (2 if bth.check_fake_flag(0x98, 3) else 0)
        + (4 if bth.check_fake_flag(0x98, 4) else 0)
    )
    honeyb_btids = (1230997, 1230998, 1230999, 1231000, 1231001)
    for i, btid in enumerate(honeyb_btids):
        out[btid] = i < honeyb_count

    skiv_complete = bth.check_real_flag(0x81, 3)
    for btid, spec in addresses.BY_CATEGORY.get("SKIVVIES", {}).items():
        per_loc = bth.check_real_flag(spec.addr, spec.bit)
        out[btid] = bool(per_loc or skiv_complete)

    #SCRAT
    scrat_healed = bth.check_real_flag(0x26, 6)
    scrat_train = bth.check_real_flag(0x2C, 1)
    if scrat_healed and scrat_train == False:
        out[1231007] = True

    return out
