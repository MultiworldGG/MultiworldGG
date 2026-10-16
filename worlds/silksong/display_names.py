from __future__ import annotations

from functools import lru_cache
from typing import Mapping


# These category labels add no identifying information to an otherwise unique
# item name. Flea, Bellway, Crest, Map and Relic remain part of the displayed
# identity.
REDUNDANT_ITEM_PREFIXES: tuple[str, ...] = (
    "Ability: ",
    "Ancestral Art: ",
    "Tool: ",
    "Silk Skill: ",
)


FLEA_DISPLAY_NAME_BY_SOURCE_NAME: Mapping[str, str] = {
    "Flea: The Marrow": "Flea: The Marrow",
    "Flea: Deep Docks (Bellway)":
        "Flea: Deep Docks - Bellway",
    "Flea: Deep Docks (Weaver Burial Spire)":
        "Flea: Deep Docks - Weaver Burial Spire",
    "Flea: Far Fields (Captured)":
        "Flea: Far Fields - Captured",
    "Flea: Hunter's March": "Flea: Hunter's March",
    "Flea: Greymoor (Craw Lake)":
        "Flea: Greymoor - Craw Lake",
    "Flea: Greymoor (Tower)":
        "Flea: Greymoor - Tower",
    "Flea: Shellwood": "Flea: Shellwood",
    "Flea: Pilgrim's Rest": "Flea: Pilgrim's Rest",
    "Flea: Blasted Steps": "Flea: Blasted Steps",
    "Flea: Sinner's Road": "Flea: Sinner's Road",
    "Flea: Exhaust Organ": "Flea: Exhaust Organ",
    "Flea: Bellhart": "Flea: Bellhart",
    "Flea: Wormways": "Flea: Wormways",
    "Flea: The Slab (Cell)": "Flea: The Slab - Cell",
    "Flea: Bilewater (Thieves)":
        "Flea: Bilewater - Thieves",
    "Flea: Deep Docks (Mines)":
        "Flea: Deep Docks - Mines",
    "Flea: Wisp Thicket":
        "Flea: Underworks - Wisp Thicket Passage",
    "Flea: Bilehaven": "Flea: Bilehaven",
    "Flea: Choral Chambers (Spa)":
        "Flea: Choral Chambers - Spa",
    "Flea: Sands of Karak": "Flea: Sands of Karak",
    "Flea: Mount Fay": "Flea: Mount Fay",
    "Flea: Songclave": "Flea: Songclave",
    "Flea: Choral Chambers (Walled Room)":
        "Flea: Choral Chambers - Walled Room",
    "Flea: Whispering Vaults":
        "Flea: Whispering Vaults",
    "Flea: Underworks": "Flea: Underworks",
    "Flea: The Slab (Bellway)":
        "Flea: The Slab - Bellway",
    "Flea: Greymoor (Kratt)": "Flea: Greymoor - Kratt",
    "Flea: Putrified Ducts (Vog)": "Flea: Putrified Ducts - Vog",
    "Flea: Memorium (Huge Flea)": "Flea: Memorium - Huge Flea",
}

ORDINARY_FLEA_DISPLAY_NAMES: tuple[str, ...] = tuple(
    FLEA_DISPLAY_NAME_BY_SOURCE_NAME.values()
)[:27]

FLEA_DISPLAY_NAMES: tuple[str, ...] = tuple(
    FLEA_DISPLAY_NAME_BY_SOURCE_NAME.values()
)


@lru_cache(maxsize=8192)
def clean_location_display_name(name: str) -> str:
    flea_name = FLEA_DISPLAY_NAME_BY_SOURCE_NAME.get(name)
    if flea_name is not None:
        return flea_name
    for prefix in REDUNDANT_ITEM_PREFIXES:
        if name.startswith(prefix):
            return name[len(prefix):]
    return name


@lru_cache(maxsize=8192)
def clean_item_display_name(name: str) -> str:
    name = clean_location_display_name(name)
    for prefix in ("Mask Shard", "Spool Fragment"):
        if name.startswith(prefix + " #") and name[len(prefix) + 2:].isdigit():
            return prefix
    if name in FLEA_DISPLAY_NAMES:
        return {
            "Flea: Greymoor - Kratt": "Flea (Kratt)",
            "Flea: Putrified Ducts - Vog": "Flea (Vog)",
            "Flea: Memorium - Huge Flea": "Flea (Huge Flea)",
        }.get(name, "Flea")
    return name


FLEA_ITEM_NAMES: tuple[str, ...] = tuple(dict.fromkeys(
    clean_item_display_name(name) for name in FLEA_DISPLAY_NAMES
))
