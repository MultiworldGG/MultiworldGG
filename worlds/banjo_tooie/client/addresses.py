"""Per-location flag descriptors.

Author: Umed (UmedMuzl).
"""

from __future__ import annotations

from typing import Dict, NamedTuple, Optional, Tuple

from . import _flag_data

# Category -> flag pointer routing

CATEGORY_FLAG_TYPE: Dict[str, str] = {
    # real_flags
    "JIGGIES": "real",
    "TREBLE": "real",
    "ROYSTEN": "real",
    "PAGES": "real",
    "HONEYCOMB": "real",
    "GLOWBO": "real",
    "DOUBLOON": "real",
    "NOTES": "real",
    "JINJOS": "real",
    "JINJO_FAMILY": "real",
    "JCHUNKS": "real",
    "BOGGY_KIDS": "real",
    "ALIEN_KIDS": "real",
    "MRFIT": "real",
    "BIGTOP_TICKETS": "real",
    "GREEN_RELICS": "real",
    "BEANS": "real",
    "CHUFFY": "real",
    "H1": "real",
    "SCRUT": "real",
    "SCRIT": "real",
    # fake_flags
    "AMAZE": "fake",
    "ROAR": "fake",
    "CHEATO": "fake",
    "STATIONBTN": "fake",
    "SILO": "fake",
    "WARPSILOS": "fake",
    "WARPPADS": "fake",
    # Special-cased
    "STOPNSWAP": "stopnswap_mixed",
    "HONEYB": "honeyb_special",
    "SKIVVIES": "skivvies_special",
    "NESTS": "nest_flags",
    "SIGNPOSTS": "signpost_flags",
    "SCROTTY_KIDS": "scrotty_special",
}


class FlagSpec(NamedTuple):
    category: str
    flag_type: str  # 'real' | 'fake' | 'nest_flags' | 'signpost_flags' | special tags
    addr: int  # byte offset within the flag bitmap
    bit: int  # 0..7 within that byte
    name: str


# Public state
LOCATION_FLAGS: Dict[int, FlagSpec] = {}
BY_CATEGORY: Dict[str, Dict[int, FlagSpec]] = {}

# STOPNSWAP entries that use real_flags instead of fake_flags.
STOPNSWAP_REAL_FLAG_BTIDS: Tuple[int, ...] = (1230953, 1230954, 1230955)


for _cat, _entries in _flag_data.BY_CATEGORY.items():
    bucket: Dict[int, FlagSpec] = {}
    for _btid, _tup in _entries.items():
        spec = FlagSpec(*_tup)
        bucket[_btid] = spec
        LOCATION_FLAGS[_btid] = spec
    BY_CATEGORY[_cat] = bucket


def summary() -> str:
    """One-line per-category count summary for diagnostics."""
    parts = [f"total btids={len(LOCATION_FLAGS)}"]
    for cat in sorted(BY_CATEGORY):
        parts.append(f"{cat}={len(BY_CATEGORY[cat])}")
    return "  ".join(parts)
