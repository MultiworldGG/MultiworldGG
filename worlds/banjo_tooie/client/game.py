"""Write-side BTHACK helpers.

Author: Umed (UmedMuzl).
"""

from __future__ import annotations

import random
from collections import Counter
from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Mapping, Optional, Set, Tuple

from . import addresses
from .state import BTHReader

if TYPE_CHECKING:
    from ..BTClient import BTEmuLoaderClient

# Settings struct field offsets
SETTING_SEED = 0x00  # u32
SETTING_VICTORY_CONDITION = 0x04
SETTING_CHUFFY = 0x05
SETTING_NESTS = 0x06
SETTING_WARPPADS = 0x07
SETTING_WARPSILOS = 0x08
SETTING_HONEYB_REWARDS = 0x09
SETTING_CHEATO_REWARDS = 0x0A
SETTING_RANDOMIZE_TICKETS = 0x0B
SETTING_RANDOMIZE_GREEN_RELICS = 0x0C
SETTING_RANDOMIZE_BEANS = 0x0D
SETTING_PUZZLE = 0x0E
SETTING_BACKDOORS = 0x0F
SETTING_GI_OPEN_FRONTDOOR = 0x10
SETTING_KLUNGO = 0x11
SETTING_TOT = 0x12
SETTING_MINIGAMES = 0x13
SETTING_DIALOG_CHARACTER = 0x14
SETTING_MAX_MUMBO_TOKENS = 0x15
SETTING_SIGNPOST_HINTS = 0x16
SETTING_EXTRA_CHEATS = 0x17
SETTING_AUTOMATIC_CHEATS = 0x18
SETTING_EASY_CANARY = 0x19
SETTING_JIGGY_REQUIREMENTS_BASE = 0x1A  # u8 [11]
SETTING_SILO_REQUIREMENTS_BASE = 0x26  # u16 BE [24]


# World-name -> jiggy_requirements[] index. Aliases cover both naming
# variants the seed may emit for the same world.
WORLD_TO_JIGGY_REQ_INDEX: Dict[str, int] = {
    "Mayahem Temple": 0,
    "Glitter Gulch Mine": 1,
    "Witchyworld": 2,
    "Jolly Roger's Lagoon - Town Center": 3,
    "Jolly Roger's Lagoon": 3,
    "Terrydactyland": 4,
    "Outside Grunty Industries": 5,
    "Grunty Industries": 5,
    "Hailfire Peaks": 6,
    "Cloud Cuckooland": 7,
    "Cauldron Keep": 8,
}


# Ordering of Jamjars-silo location IDs in silo_requirements[].
JAMJAR_SILO_LOCATIONS = [
    1230753,
    1230754,
    1230755,
    1230756,
    1230757,
    1230758,
    1230759,
    1230761,
    1230762,
    1230760,
    1230763,
    1230764,
    1230766,
    1230765,
    1230767,
    1230768,
    1230769,
    1230770,
    1230773,
    1230771,
    1230772,
    1230774,
    1230775,
    1230776,
]
JAMJAR_SILO_INDEX: Dict[int, int] = {
    loc: i for i, loc in enumerate(JAMJAR_SILO_LOCATIONS)
}


# ---------------------------------------------------------------------------
# BTHWriter -- write companion to BTHReader
# ---------------------------------------------------------------------------


class BTHWriter:
    """Write helpers for the BTHACK settings struct."""

    def __init__(self, loader: BTEmuLoaderClient, reader: Optional[BTHReader] = None):
        self.loader = loader
        self.reader = reader if reader is not None else BTHReader(loader)

    def settings_ptr(self) -> Optional[int]:
        return self.reader.settings_ptr()

    def write_setting_u8(self, offset: int, value: int) -> bool:
        ptr = self.settings_ptr()
        if ptr is None:
            return False
        self.loader.write_u8(ptr + offset, value & 0xFF)
        return True

    def write_setting_u16(self, offset: int, value: int) -> bool:
        ptr = self.settings_ptr()
        if ptr is None:
            return False
        self.loader.write_u16(ptr + offset, value & 0xFFFF)
        return True

    def write_setting_u32(self, offset: int, value: int) -> bool:
        ptr = self.settings_ptr()
        if ptr is None:
            return False
        self.loader.write_u32(ptr + offset, value & 0xFFFFFFFF)
        return True


# Helpers
def opt(options: Mapping[str, Any], key: str, default: int = 0) -> int:
    """Coerce a slot_data option to int."""
    v = options.get(key, default)
    if isinstance(v, bool):
        return int(v)
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def read_count(loader: BTEmuLoaderClient, reader: BTHReader, item_index: int) -> int:
    """Read the current u8 counter at ``pc.items[item_index]``."""
    ptr = reader.items_ptr()
    if ptr is None:
        return 0
    return loader.read_u8(ptr + item_index)


# Top-level slot-settings write
def write_slot_settings(
    loader: BTEmuLoaderClient, slot_data: Mapping[str, Any]
) -> bool:
    """Push slot_data into BTHACK pc.settings (and related regions)."""
    reader = BTHReader(loader)
    writer = BTHWriter(loader, reader)
    if reader.settings_ptr() is None:
        return False

    bt_data = slot_data.get("custom_bt_data", {}) or {}
    options = slot_data.get("options", {}) or {}

    # ROM toggles "BTCLIENT READY" vs "BTCLIENT DISCONNECTED" on the file
    # select screen based on whether pc.settings.seed is non-zero, so writing
    # a non-zero value here is what makes the ROM acknowledge the client.
    seed = bt_data.get("seed")
    if isinstance(seed, int) and seed:
        writer.write_setting_u32(SETTING_SEED, seed & 0xFFFFFFFF)

    writer.write_setting_u8(
        SETTING_VICTORY_CONDITION, opt(options, "victory_condition")
    )
    writer.write_setting_u8(SETTING_CHUFFY, opt(options, "randomize_chuffy"))
    writer.write_setting_u8(SETTING_NESTS, opt(options, "nestsanity"))
    writer.write_setting_u8(SETTING_WARPPADS, opt(options, "randomize_warp_pads"))
    writer.write_setting_u8(SETTING_WARPSILOS, opt(options, "randomize_silos"))
    writer.write_setting_u8(SETTING_HONEYB_REWARDS, opt(options, "honeyb_rewards"))
    writer.write_setting_u8(SETTING_CHEATO_REWARDS, opt(options, "cheato_rewards"))
    writer.write_setting_u8(
        SETTING_RANDOMIZE_TICKETS, opt(options, "randomize_tickets")
    )
    writer.write_setting_u8(
        SETTING_RANDOMIZE_GREEN_RELICS, opt(options, "randomize_green_relics")
    )
    writer.write_setting_u8(SETTING_RANDOMIZE_BEANS, opt(options, "randomize_beans"))
    writer.write_setting_u8(SETTING_PUZZLE, opt(options, "skip_puzzles"))
    writer.write_setting_u8(SETTING_BACKDOORS, opt(options, "backdoors"))
    writer.write_setting_u8(
        SETTING_GI_OPEN_FRONTDOOR, opt(options, "open_gi_frontdoor")
    )
    writer.write_setting_u8(SETTING_KLUNGO, opt(options, "skip_klungo"))
    writer.write_setting_u8(SETTING_TOT, opt(options, "tower_of_tragedy"))
    writer.write_setting_u8(SETTING_MINIGAMES, opt(options, "speed_up_minigames"))
    writer.write_setting_u8(
        SETTING_DIALOG_CHARACTER, opt(options, "dialog_character", 110)
    )

    # SETTING_SIGNPOST_HINTS doubles as the "hint signposts enabled" toggle:
    # set whenever hints exist AND either signpost_hints or randomize_signposts is on.
    has_hints = bool((bt_data.get("hints") or {}))
    sign_enabled = opt(options, "signpost_hints") or (
        has_hints and opt(options, "randomize_signposts")
    )
    writer.write_setting_u8(SETTING_SIGNPOST_HINTS, 1 if sign_enabled else 0)
    writer.write_setting_u8(SETTING_EXTRA_CHEATS, opt(options, "extra_cheats"))
    writer.write_setting_u8(
        SETTING_AUTOMATIC_CHEATS, opt(options, "auto_enable_cheats")
    )
    writer.write_setting_u8(SETTING_EASY_CANARY, opt(options, "easy_canary"))

    # Per-world jiggy requirements (11 bytes).
    for world, amount in (bt_data.get("world_requirements") or {}).items():
        idx = WORLD_TO_JIGGY_REQ_INDEX.get(world)
        if idx is not None and isinstance(amount, int):
            writer.write_setting_u8(SETTING_JIGGY_REQUIREMENTS_BASE + idx, amount)

    # Silo costs (24 u16 BE values). JSON serialisation may coerce int keys
    # to strings, so accept both shapes for the location id.
    for raw_loc, cost in (bt_data.get("jamjars_silo_costs") or {}).items():
        try:
            loc = int(raw_loc)
        except (TypeError, ValueError):
            continue
        idx = JAMJAR_SILO_INDEX.get(loc)
        if idx is not None and isinstance(cost, int):
            writer.write_setting_u16(SETTING_SILO_REQUIREMENTS_BASE + (idx * 2), cost)

    randomize_bk_moves = opt(options, "randomize_bk_moves", -1)
    if randomize_bk_moves in (0, 1):
        write_default_bk_moves(loader, randomize_bk_moves)

    apply_zone_warps(loader, slot_data)
    apply_preopened_silos(loader, slot_data)
    apply_signpost_hints(loader, slot_data)
    apply_max_mumbo_tokens(loader, slot_data)

    return True


# Loading-zone shuffle (writes redirect entries into pc.exit_map[])
EXIT_MAP_STRUCT_SIZE = 0x0E
EXIT_MAP_ON_MAP = 0x00  # u16 BE -- the map you're currently on
EXIT_MAP_OG_MAP = 0x02  # u16 BE -- original "from" world id
EXIT_MAP_TO_MAP = 0x04  # u16 BE -- new "to" world id
EXIT_MAP_OG_EXIT = 0x06  # u8 -- original exit id
EXIT_MAP_TO_EXIT = 0x07  # u8 -- new exit id
EXIT_MAP_ACCESS_RULES = 0x08  # 6 bytes -- bitmap of required pc.items[] indices

# Per-world descriptors
WORLD_MAP_ENTRANCES: Dict[int, Dict[str, Any]] = {
    0xB8: {
        "name": "Mayahem Temple",
        "entrance_id": 10,
        "exit_id": 2,
        "exit_map": 0x14F,
        "access": [],
        "reverse_access": [],
    },
    0xC7: {
        "name": "Glitter Gulch Mine",
        "entrance_id": 17,
        "exit_id": 2,
        "exit_map": 0x152,
        "access": [],
        "reverse_access": [],
    },
    0xD6: {
        "name": "Witchyworld",
        "entrance_id": 18,
        "exit_id": 2,
        "exit_map": 0x154,
        "access": [],
        "reverse_access": [],
    },
    0x1A7: {
        "name": "Jolly Roger's Lagoon - Town Center",
        "entrance_id": 3,
        "exit_id": 5,
        "exit_map": 0x155,
        "access": [],
        "reverse_access": [],
    },
    0x112: {
        "name": "Terrydactyland",
        "entrance_id": 23,
        "exit_id": 2,
        "exit_map": 0x15A,
        "access": [],
        "reverse_access": [],
    },
    0x100: {
        "name": "Outside Grunty Industries",
        "entrance_id": 9,
        "exit_id": 2,
        "exit_map": 0x15C,
        "access": [],
        "reverse_access": [],
    },
    0x127: {
        "name": "Hailfire Peaks",
        "entrance_id": 21,
        "exit_id": 6,
        "exit_map": 0x155,
        "access": [],
        "reverse_access": [],
    },
    0x136: {
        "name": "Cloud Cuckooland",
        "entrance_id": 20,
        "exit_id": 5,
        "exit_map": 0x15A,
        "access": [],
        "reverse_access": [],
    },
    0x15D: {
        "name": "Cauldron Keep",
        "entrance_id": 1,
        "exit_id": 3,
        "exit_map": 0x15C,
        "access": [],
        "reverse_access": [],
    },
    # Secondary entrances (inner-world doors that can be shuffled too).
    0x17A: {
        "name": "Targitzan's Really Sacred Chamber",
        "entrance_id": 1,
        "exit_id": 2,
        "exit_map": 0x178,
        "access": [1],
        "reverse_access": [1],
    },  # BBLASTER
    0x0D1: {
        "name": "Inside Chuffy's Boiler",
        "entrance_id": 1,
        "exit_id": 2,
        "exit_map": 0x0D0,
        "access": [],
        "reverse_access": [],
    },
    0x0F9: {
        "name": "Big Top Interior",
        "entrance_id": 1,
        "exit_id": 3,
        "exit_map": 0x0D6,
        "access": [],
        "reverse_access": [],
    },
    0x0FC: {
        "name": "Davy Jones' Locker",
        "entrance_id": 1,
        "exit_id": 0x28,
        "exit_map": 0x1A9,
        "access": [21, 9],
        "reverse_access": [],
    },  # GEGGS, AUQAIM
    0x113: {
        "name": "Terry's Nest",
        "entrance_id": 0x05,
        "exit_id": 0x14,
        "exit_map": 0x112,
        "access": [],
        "reverse_access": [],
    },
    0x110: {
        "name": "Repair Depot",
        "entrance_id": 1,
        "exit_id": 3,
        "exit_map": 0x10F,
        "access": [21],
        "reverse_access": [],
    },  # GEGGS
    0x12B: {
        "name": "Chilli Billi Crater",
        "entrance_id": 1,
        "exit_id": 0x16,
        "exit_map": 0x127,
        "access": [23],
        "reverse_access": [],
    },  # IEGGS
    0x12C: {
        "name": "Chilly Willy Crater",
        "entrance_id": 1,
        "exit_id": 0x0C,
        "exit_map": 0x128,
        "access": [],
        "reverse_access": [],
    },
    0x13F: {
        "name": "Mingy Jongo Skull",
        "entrance_id": 1,
        "exit_id": 0x09,
        "exit_map": 0x136,
        "access": [],
        "reverse_access": [],
    },
}

WORLD_NAME_TO_MAP_ID: Dict[str, int] = {
    v["name"]: k for k, v in WORLD_MAP_ENTRANCES.items()
}


def write_exit_map_entry(
    loader: BTEmuLoaderClient,
    exit_maps_ptr: int,
    world_index: int,
    *,
    on_map: int,
    og_map: int,
    to_map: int,
    og_exit: int,
    to_exit: int,
    access: List[int],
) -> None:
    base = exit_maps_ptr + world_index * EXIT_MAP_STRUCT_SIZE
    loader.write_u16(base + EXIT_MAP_ON_MAP, on_map & 0xFFFF)
    loader.write_u16(base + EXIT_MAP_OG_MAP, og_map & 0xFFFF)
    loader.write_u16(base + EXIT_MAP_TO_MAP, to_map & 0xFFFF)
    loader.write_u8(base + EXIT_MAP_OG_EXIT, og_exit & 0xFF)
    loader.write_u8(base + EXIT_MAP_TO_EXIT, to_exit & 0xFF)
    bitmap = [0, 0, 0, 0, 0, 0]
    for move_id in access:
        if 0 <= move_id < 48:
            bitmap[move_id // 8] |= 1 << (move_id % 8)
    for i, b in enumerate(bitmap):
        loader.write_u8(base + EXIT_MAP_ACCESS_RULES + i, b)


def apply_zone_warps(loader: BTEmuLoaderClient, slot_data: Mapping[str, Any]) -> int:
    """Push the loading-zone shuffle into pc.exit_map[]."""
    reader = BTHReader(loader)
    exit_maps_ptr = reader.exit_map_ptr()
    if exit_maps_ptr is None:
        return 0

    bt_data = slot_data.get("custom_bt_data", {}) or {}
    zones = bt_data.get("loading_zones") or {}
    if not zones:
        return 0

    world_index = 0
    for orig_name, new_name in zones.items():
        orig_id = WORLD_NAME_TO_MAP_ID.get(orig_name)
        new_id = WORLD_NAME_TO_MAP_ID.get(new_name)
        if orig_id is None or new_id is None:
            continue
        orig = WORLD_MAP_ENTRANCES[orig_id]
        new = WORLD_MAP_ENTRANCES[new_id]

        write_exit_map_entry(
            loader,
            exit_maps_ptr,
            world_index,
            on_map=orig["exit_map"],
            og_map=orig_id,
            to_map=new_id,
            og_exit=orig["entrance_id"],
            to_exit=new["entrance_id"],
            access=new["access"],
        )
        world_index += 1

        write_exit_map_entry(
            loader,
            exit_maps_ptr,
            world_index,
            on_map=new_id,
            og_map=new["exit_map"],
            to_map=orig["exit_map"],
            og_exit=new["exit_id"],
            to_exit=orig["exit_id"],
            access=orig["reverse_access"],
        )
        world_index += 1

        if orig_id == 0xC7:
            write_exit_map_entry(
                loader,
                exit_maps_ptr,
                world_index,
                on_map=orig["exit_map"],
                og_map=orig_id,
                to_map=new_id,
                og_exit=16,
                to_exit=new["entrance_id"],
                access=new["access"],
            )
            world_index += 1

    return world_index


# Received-items write
AP_ITEM_INDEX: Dict[int, int] = {
    # Jamjars moves
    1230753: 0,  # GGRAB
    1230754: 1,  # BBLASTER
    1230755: 2,  # EGGAIM
    1230757: 3,  # BDRILL
    1230758: 4,  # BBAYONET
    1230760: 5,  # AIREAIM
    1230761: 6,  # SPLITUP
    1230764: 7,  # WWHACK
    1230765: 8,  # TTORP
    1230766: 9,  # AUQAIM
    1230774: 10,  # SHPACK
    1230775: 11,  # GLIDE
    1230771: 12,  # SNPACK
    1230772: 13,  # LSPRING
    1230773: 14,  # CLAWBTS
    1230768: 15,  # SPRINGB
    1230769: 16,  # TAXPACK
    1230770: 17,  # HATCH
    1230762: 18,  # PACKWH
    1230776: 19,  # SAPACK
    1230756: 20,  # FEGGS
    1230759: 21,  # GEGGS
    1230767: 22,  # CEGGS
    1230763: 23,  # IEGGS
    # Roysten moves
    1230777: 24,  # FSWIM
    1230778: 25,  # DAIR
    # Stop'n'Swap special: BBASH
    1230800: 26,  # BBASH
    # Dino moves
    1230779: 27,  # AMAZEOGAZE
    1230780: 28,  # ROAR
    # BK moves
    1230810: 29,  # DIVE
    1230811: 30,  # FPAD
    1230824: 31,  # GRAT
    1230814: 32,  # ROLL
    1230822: 33,  # ARAT
    1230825: 34,  # BBARGE
    1230816: 35,  # TJUMP
    1230818: 36,  # FLUTTER
    1230812: 37,  # FFLIP
    1230817: 38,  # CLIMB
    1230823: 39,  # BEGGS
    1230815: 40,  # TTROT
    1230820: 41,  # BBUST
    1230819: 42,  # WWING
    1230826: 43,  # SSTRIDE
    1230821: 44,  # TTRAIN
    1230827: 45,  # BBOMB
    1230813: 46,  # EGGSHOOT
    # Counters
    1230513: 47,  # PAGES
    1230512: 48,  # HONEY
    # Jinjos (one of each colour)
    1230501: 49,  # WJINJO
    1230502: 50,  # OJINJO
    1230503: 51,  # YJINJO
    1230504: 52,  # BRJINJO
    1230505: 53,  # GJINJO
    1230506: 54,  # RJINJO
    1230507: 55,  # BLJINJO
    1230508: 56,  # PJINJO
    1230509: 57,  # BKJINJO
    1230514: 58,  # DOUBLOON
    1230515: 59,  # JIGGY
    1230516: 60,  # TREBLE
    1230797: 61,  # NOTE
    1230798: 62,  # MUMBOTOKEN
    # Stop'n'Swap items
    1230799: 63,  # IKEY
    1230804: 64,  # PMEGG (hatched)
    1230803: 65,  # BMEGG (hatched)
    1230916: 66,  # HEALTHUP
    1230802: 67,  # HOMINGEGGS
    # Cheats
    1230917: 68,  # CHEATFEATHER
    1230918: 69,  # CHEATEGG
    1230919: 70,  # CHEATFALL
    1230920: 71,  # CHEATHONEY
    1230921: 72,  # CHEATJUKE
    # Mumbo Magic per world
    1230855: 73,  # MUMBOMT
    1230856: 74,  # MUMBOGM
    1230857: 75,  # MUMBOWW
    1230858: 76,  # MUMBOJR
    1230859: 77,  # MUMBOTD
    1230860: 78,  # MUMBOGI
    1230861: 79,  # MUMBOHP
    1230862: 80,  # MUMBOCC
    1230863: 81,  # MUMBOIH
    # Humba Magic per world
    1230174: 82,  # HUMBAMT
    1230175: 83,  # HUMBAGM
    1230176: 84,  # HUMBAWW
    1230177: 85,  # HUMBAJR
    1230178: 86,  # HUMBATD
    1230179: 87,  # HUMBAGI
    1230180: 88,  # HUMBAHP
    1230181: 89,  # HUMBACC
    1230182: 90,  # HUMBAIH
    # Train switches
    1230794: 91,  # TRAINSWIH
    1230791: 92,  # TRAINSWTD
    1230790: 93,  # TRAINSWGI
    1230792: 94,  # TRAINSWHP1
    1230793: 95,  # TRAINSWHP2
    1230795: 96,  # TRAINSWWW
    1230796: 97,  # CHUFFY
    # Nest item drops (counters)
    1230805: 98,  # GNEST
    1230806: 99,  # ENEST
    1230807: 100,  # FNEST
    # World access keys
    1230944: 101,  # MTA
    1230945: 102,  # GGA
    1230946: 103,  # WWA
    1230947: 104,  # JRA
    1230948: 105,  # TDA
    1230949: 106,  # GIA
    1230950: 107,  # HFA
    1230951: 108,  # CCA
    1230952: 109,  # CKA
    # 110 = H1A -- event-only, no AP item ID.
    # Warp pads
    1230880: 111,  # WARPMT_HUMBA
    1230879: 112,  # WARPMT_PRISON
    1230878: 113,  # WARPMT_MUMBO
    1230877: 114,  # WARPMT_ENTRANCE
    1230881: 115,  # WARPMT_KICKBALL
    1230886: 116,  # WARPGG_TRAIN
    1230885: 117,  # WARPGG_CRUSHING
    1230884: 118,  # WARPGG_HUMBA
    1230883: 119,  # WARPGG_MUMBO
    1230882: 120,  # WARPGG_ENTRANCE
    1230888: 121,  # WARPWW_BIGTOP
    1230887: 122,  # WARPWW_ENTRANCE
    1230891: 123,  # WARPWW_MUMBO
    1230890: 124,  # WARPWW_HUMBA
    1230889: 125,  # WARPWW_SPACE
    1230896: 126,  # WARPJR_LOCKERS
    1230895: 127,  # WARPJR_BIGFISH
    1230894: 128,  # WARPJR_SHIP
    1230893: 129,  # WARPJR_ATLANTIS
    1230892: 130,  # WARPJR_ENTRANCE
    1230904: 131,  # WARPGI_MUMBO
    1230903: 132,  # WARPGI_HUMBA
    1230902: 133,  # WARPGI_ENTRANCE
    1230906: 134,  # WARPGI_ROOF
    1230905: 135,  # WARPGI_CRUSHER
    1230901: 136,  # WARPTD_TOP
    1230900: 137,  # WARPTD_HUMBA
    1230899: 138,  # WARPTD_MUMBO
    1230898: 139,  # WARPTD_STOMPING
    1230897: 140,  # WARPTD_ENTRANCE
    1230912: 141,  # WARPCC_ENTRANCE
    1230913: 142,  # WARPCC_CENTER
    1230911: 143,  # WARPHF_ICICLE
    1230910: 144,  # WARPHF_HUMBA
    1230909: 145,  # WARPHF_ICYUPPER
    1230908: 146,  # WARPHF_LAVAUPPER
    1230907: 147,  # WARPHF_ENTRANCE
    1230915: 148,  # WARPCK_HAG1
    1230914: 149,  # WARPCK_ENTRANCE
    # Silos
    1230870: 150,  # SILO_JINJO_VILLAGE
    1230871: 151,  # SILO_WOODED_HOLLOW
    1230872: 152,  # SILO_PLATEAU
    1230873: 153,  # SILO_PINE_GROVE
    1230874: 154,  # SILO_CLIFF_TOP
    1230875: 155,  # SILO_WASTELAND
    1230876: 156,  # SILO_QUAGMIRE
    # Misc collectibles
    1230922: 157,  # BTTICKET
    1230923: 158,  # GRRELIC
    1230924: 159,  # BEAN
}


# Traps go to pc.traps[]
AP_TRAP_INDEX: Dict[int, int] = {
    1230786: 0,  # TTRAP  ("Trip Trap")      -> AP_TRAP_TRIP
    1230787: 1,  # STRAP  ("Slip Trap")      -> AP_TRAP_SLIP
    1230788: 2,  # TRTRAP ("Transform Trap") -> AP_TRAP_TRANSFORM
    1230789: 3,  # SQTRAP ("Squish Trap")    -> AP_TRAP_SQUISH
    1230833: 4,  # TIPTRAP ("Tip Trap")      -> AP_TRAP_TIP
}


# Progressive items unlock a fixed sequence of plain items. When the player
# has received the progressive N times, the first N entries get set to 1.
AP_PROGRESSIVE_SEQUENCE: Dict[int, List[int]] = {
    1230828: [41, 3],  # PBBUST  -> BBUST, BDRILL
    1230829: [20, 21, 23, 22],  # PEGGS   -> FEGGS, GEGGS, IEGGS, CEGGS
    1230830: [43, 44, 15, 14],  # PSHOES  -> SSTRIDE, TTRAIN, SPRINGB, CLAWBTS
    1230831: [29, 25, 24],  # PSWIM   -> DIVE, DAIR, FSWIM
    1230832: [31, 26],  # PBASH   -> GRAT, BBASH
    1230782: [30, 45, 5],  # PFLIGHT -> FPAD, BBOMB, AIREAIM
    1230783: [46, 2],  # PEGGAIM -> EGGSHOOT, EGGAIM
    1230784: [29, 9, 8, 25, 24],  # PASWIM  -> DIVE, AUQAIM, TTORP, DAIR, FSWIM
    1230785: [46, 27, 2, 1],  # PAEGGAIM-> EGGSHOOT, AMAZEOGAZE, EGGAIM, BBLASTER
}


# AP item IDs we recognise but don't act on.
AP_DEFERRED_ITEMS: Set[int] = {
    1230834,  # NONE / filler
}

NOTE_BTID = 1230797
BASS_BTID = 1230781

def write_received_items(
    loader: BTEmuLoaderClient, items_received: Iterable[Any]
) -> Dict[str, int]:
    """Write the player's current items_received state into pc.items[] and pc.traps[]"""
    reader = BTHReader(loader)
    items_ptr = reader.items_ptr()
    traps_ptr = reader.traps_ptr()
    if items_ptr is None or traps_ptr is None:
        return {"error": -1}

    counts: Counter[int] = Counter()
    for it in items_received:
        ap_id = getattr(it, "item", None)
        if ap_id is None:
            continue
        counts[int(ap_id)] += 1

    written_items = 0
    written_traps = 0
    written_progressive = 0
    unknown: List[int] = []

    bass_cnt = counts.pop(BASS_BTID, 0)
    if bass_cnt:
        counts[NOTE_BTID] = counts.get(NOTE_BTID, 0) + 2 * bass_cnt

    for ap_id, cnt in counts.items():
        if ap_id in AP_ITEM_INDEX:
            loader.write_u8(items_ptr + AP_ITEM_INDEX[ap_id], cnt & 0xFF)
            written_items += 1
        elif ap_id in AP_TRAP_INDEX:
            loader.write_u8(traps_ptr + AP_TRAP_INDEX[ap_id], cnt & 0xFF)
            written_traps += 1
        elif ap_id in AP_PROGRESSIVE_SEQUENCE:
            seq = AP_PROGRESSIVE_SEQUENCE[ap_id]
            unlocks = min(cnt, len(seq))
            for i in range(unlocks):
                loader.write_u8(items_ptr + seq[i], 1)
            written_progressive += 1
        elif ap_id in AP_DEFERRED_ITEMS:
            continue
        else:
            unknown.append(ap_id)

    return {
        "items_written": written_items,
        "traps_written": written_traps,
        "progressives_written": written_progressive,
        "unknown_ids": unknown,
        "total_received": sum(counts.values()),
    }


# ---------------------------------------------------------------------------
# Pre-opened silos
# ---------------------------------------------------------------------------

PREOPENED_SILO_IDS: Tuple[int, ...] = (
    1230870,
    1230871,
    1230872,
    1230873,
    1230874,
    1230875,
    1230876,
)


def apply_preopened_silos(
    loader: BTEmuLoaderClient, slot_data: Mapping[str, Any]
) -> int:
    """Grant the silo items the seed flagged as starting open. Returns the
    number of silos written."""
    bt_data = slot_data.get("custom_bt_data", {}) or {}
    preopened = bt_data.get("preopened_silos_ids") or []
    if not preopened:
        return 0
    reader = BTHReader(loader)
    items_ptr = reader.items_ptr()
    if items_ptr is None:
        return 0
    n = 0
    for silo_id in preopened:
        if (
            isinstance(silo_id, int)
            and silo_id in PREOPENED_SILO_IDS
            and silo_id in AP_ITEM_INDEX
        ):
            loader.write_u8(items_ptr + AP_ITEM_INDEX[silo_id], 1)
            n += 1
    return n


# Hint signposts
SIGNPOST_TEXT_SLOT_SIZE = 150
SKIP_HINT_SUFFIX = b"\nPRESS \x86 TO SKIP"


def apply_signpost_hints(
    loader: BTEmuLoaderClient, slot_data: Mapping[str, Any]
) -> int:
    """Write hint text into pc.signposts. Text is uppercased ASCII plus the
    B-button skip footer, truncated to 149 chars + null terminator."""
    bt_data = slot_data.get("custom_bt_data", {}) or {}
    hints = bt_data.get("hints") or {}
    if not hints:
        return 0
    reader = BTHReader(loader)
    hint_ptr = reader.signpost_messages_ptr()
    if hint_ptr is None:
        return 0
    signpost_map = addresses.BY_CATEGORY.get("SIGNPOSTS", {})
    if not signpost_map:
        return 0

    n = 0
    for raw_loc, hint_payload in hints.items():
        try:
            loc_id = int(raw_loc)
        except (TypeError, ValueError):
            continue
        spec = signpost_map.get(loc_id)
        if spec is None:
            continue
        sign_id = spec.addr  # bytebit form: addr holds the signpost index
        if isinstance(hint_payload, dict):
            text = hint_payload.get("text", "")
        else:
            text = str(hint_payload)
        body = str(text).upper().encode("ascii", errors="ignore")
        max_body = SIGNPOST_TEXT_SLOT_SIZE - 1 - len(SKIP_HINT_SUFFIX)
        if max_body < 0:
            max_body = 0
        encoded = body[:max_body] + SKIP_HINT_SUFFIX
        encoded = encoded[: SIGNPOST_TEXT_SLOT_SIZE - 1]
        base = hint_ptr + sign_id * SIGNPOST_TEXT_SLOT_SIZE
        for i, b in enumerate(encoded):
            loader.write_u8(base + i, b)
        loader.write_u8(base + len(encoded), 0)
        n += 1
    return n


# Goal info: mumbo-token cap + in-game goal-info dialog

# Offset within the pc struct for the message-queue counter the PC bumps
# to ask N64 to display a queued dialog.
PC_SHOW_TXT_OFFSET = 0x4
N64_SHOW_TEXT_OFFSET = 0x0
PC_MESSAGE_BUFFER_SIZE = 508

ENCOURAGEMENT: Tuple[str, ...] = (
    " GUH-HUH!",
    " BREEE!",
    " EEKUM BOKUM!",
    " YEEHAW!",
    " JINJOO!!",
    " WAHEY!!!",
    " ROOOOO!!!",
    " OOMANAKA!!!",
)


def goal_max_mumbo_tokens(slot_data: Mapping[str, Any]) -> Optional[int]:
    """The mumbo-token cap the HUD should track for the active goal type.
    None means the goal doesn't apply a token cap."""
    options = slot_data.get("options", {}) or {}
    goal = opt(options, "victory_condition", 0)
    if goal == 0:
        return 0
    if goal == 1:
        return opt(options, "minigame_hunt_length", 0)
    if goal == 2:
        return opt(options, "boss_hunt_length", 0)
    if goal == 3:
        return opt(options, "jinjo_family_rescue_length", 0)
    if goal == 4:
        return 32
    if goal == 5:
        return opt(options, "token_hunt_length", 0)
    if goal == 6:
        return opt(options, "boss_hunt_length", 0)
    return None


def apply_max_mumbo_tokens(
    loader: BTEmuLoaderClient, slot_data: Mapping[str, Any]
) -> bool:
    """Write the per-goal mumbo-token cap into settings.max_mumbo_tokens."""
    writer = BTHWriter(loader)
    cap = goal_max_mumbo_tokens(slot_data)
    if cap is None:
        return False
    return writer.write_setting_u8(SETTING_MAX_MUMBO_TOKENS, cap & 0xFF)


def build_goal_info_message(
    slot_data: Mapping[str, Any], encouragement: Optional[str] = None
) -> Optional[Tuple[str, int]]:
    """Build the in-game (message, icon_id) tuple for the active goal type.
    Returns None if the goal type isn't recognised or required lengths are
    missing."""
    options = slot_data.get("options", {}) or {}
    goal = opt(options, "victory_condition", -1)
    if goal < 0:
        return None

    if encouragement is None:
        encouragement = random.choice(ENCOURAGEMENT)
    enc = encouragement

    msg: Optional[str] = None
    if goal == 0:
        msg = f"You need to hunt down Grunty in her HAG1 and put her back in the ground!\nGood Luck and{enc}"
    elif goal == 1:
        n = opt(options, "minigame_hunt_length", 0)
        if n == 15:
            msg = f"You are hunting down all 15 of the Mumbo Tokens found in Grunty's dastardly minigames!\nGood luck and{enc}"
        elif n > 0:
            msg = f"You are hunting for {n} Mumbo Tokens from Grunty's dastardly minigames!\nGood Luck and{enc}"
    elif goal == 2:
        n = opt(options, "boss_hunt_length", 0)
        if n == 8:
            msg = f"You are hunting down all 8 Mumbo Tokens from each world boss!\nGood Luck and{enc}"
        elif n > 0:
            msg = f"You are hunting for {n} Mumbo Tokens from the 8 world bosses!\nGood Luck and{enc}"
    elif goal == 3:
        n = opt(options, "jinjo_family_rescue_length", 0)
        if n == 9:
            msg = f"You are trying to rescue all 9 Jinjo families and retrieve their Mumbo Tokens!\nGood Luck and{enc}"
        elif n > 0:
            msg = f"You are trying to rescue {n} of the 9 Jinjo families and retrieve their Mumbo Tokens!\nGood Luck and{enc}"
    elif goal == 4:
        msg = f"You absolute mad lad! You're doing the Wonder Wing Challenge!\nGood Luck and{enc}"
    elif goal == 5:
        n = opt(options, "token_hunt_length", 0)
        if n > 0:
            msg = f"You are trying to find {n} Mumbo Tokens scattered throughout the Isle O' Hags!\nGood Luck and{enc}"
    elif goal == 6:
        n = opt(options, "boss_hunt_length", 0)
        if n > 0:
            msg = f"You need to defeat {n} Bosses in order to defeat HAG-1!\nGood Luck and{enc}"

    if msg is None:
        return None

    # If dialog_character is the default (110, the icon-less value), goal
    # messages use icon 5; otherwise use the configured icon.
    dialog_char = opt(options, "dialog_character", 110)
    icon_id = 5 if dialog_char == 110 else dialog_char
    return (msg, icon_id)


def read_n64_text_queue(loader: BTEmuLoaderClient) -> int:
    """Current value of n64.show_text -- the queue counter the N64 has
    caught up to. We must not bump pc.show_text past this until the N64
    advances."""
    reader = BTHReader(loader)
    n64_ptr = reader.n64_ptr()
    if n64_ptr is None:
        return 0
    return loader.read_u8(n64_ptr + N64_SHOW_TEXT_OFFSET)


def read_pc_text_queue(loader: BTEmuLoaderClient) -> int:
    reader = BTHReader(loader)
    pc_ptr = reader.pc_ptr()
    if pc_ptr is None:
        return 0
    return loader.read_u8(pc_ptr + PC_SHOW_TXT_OFFSET)


def send_pc_dialog(loader: BTEmuLoaderClient, text: str, icon_id: int) -> bool:
    """Push a message into the PC dialog queue.

    Writes uppercase ASCII text into pc.messages, sets the dialog
    character icon, then bumps pc.show_txt by 1 so the ROM picks it up on
    the next frame.
    """
    reader = BTHReader(loader)
    msg_ptr = reader.pc_messages_ptr()
    pc_ptr = reader.pc_ptr()
    settings_ptr = reader.settings_ptr()
    if msg_ptr is None or pc_ptr is None or settings_ptr is None:
        return False

    encoded = str(text).upper().encode("ascii", errors="ignore")
    encoded = encoded[: PC_MESSAGE_BUFFER_SIZE - 1]
    for i, b in enumerate(encoded):
        loader.write_u8(msg_ptr + i, b)
    loader.write_u8(msg_ptr + len(encoded), 0)

    loader.write_u8(settings_ptr + SETTING_DIALOG_CHARACTER, icon_id & 0xFF)

    current_pc_q = loader.read_u8(pc_ptr + PC_SHOW_TXT_OFFSET)
    loader.write_u8(pc_ptr + PC_SHOW_TXT_OFFSET, (current_pc_q + 1) & 0xFF)
    return True


# ///////////////// Dialogs \\\\\\\\\\\\\\\\\\\

STATION_NAMES: Dict[int, str] = {
    1230794: "Train Station in Isle O' Hags",
    1230791: "Train Station in Terrydactyland",
    1230790: "Train Station in Grunty Industries",
    1230792: "Train Station on the Lava Side of Hailfire Peaks",
    1230793: "Train Station on the Icy Side of Hailfire Peaks",
    1230795: "Train Station in Witchyworld",
}

MAGIC_NAMES: Dict[int, str] = {
    1230855: "Golden Goliath",
    1230856: "Levitate",
    1230857: "Power",
    1230858: "Oxygenate",
    1230859: "Enlarge",
    1230860: "EMP",
    1230861: "Life Force",
    1230862: "Rain Dance",
    1230863: "Heal",
}

TRANSFORMATION_NAMES: Dict[int, Tuple[str, str]] = {
    1230174: ("Stony", "strong"),
    1230175: ("Detonator", "explosive"),
    1230176: ("Money Van", "fast"),
    1230177: ("Submarine", "high-tech"),
    1230178: ("T-Rex", "scary"),
    1230179: ("Washing Machine", "useful"),
    1230180: ("Snowball", "cool"),
    1230181: ("Bee", "cute"),
    1230182: ("Dragon", "dangerous"),
}

CHEAT_NAMES: Dict[int, str] = {
    1230917: "Feathers Cheat",
    1230918: "Egg Cheat",
    1230919: "Fallproof Cheat",
    1230920: "Honeyback Cheat. Press D-Pad Down to Toggle this Cheat",
    1230921: "Jukebox Cheat",
}


def format_item_message(
    item_id: int, item_name: str, sender_name: str, own: bool, dialog_character: int
) -> Optional[str]:
    """Return the dialog text for a single received item, or None if the item
    has no dedicated message (jiggies, notes, traps, etc.)."""
    if (
        1230753 <= item_id <= 1230780  # BT moves
        or 1230810 <= item_id <= 1230827  # BK moves
        or 1230782 <= item_id <= 1230785  # Progressive moves I
        or 1230828 <= item_id <= 1230832  # Progressive moves II
        or item_id in (1230800, 1230802)  # Stop'n'Swap moves
    ):
        return (
            f"You can now use {item_name}."
            if own
            else f"{sender_name} taught you how to use {item_name}."
        )

    if 1230944 <= item_id <= 1230952:  # World keys
        return (
            f"{item_name} is now open!"
            if own
            else f"{sender_name} has just opened {item_name}!"
        )

    if item_id == 1230796:  # Chuffy
        extra = "\nDon't forget that you can call Chuffy at any unlocked station."
        return (
            f"You can now use {item_name}.{extra}"
            if own
            else f"{sender_name} has just repaired {item_name}.{extra}"
        )

    if 1230790 <= item_id <= 1230795:  # Stations
        sname = STATION_NAMES.get(item_id, item_name)
        return (
            f"You can now use the {sname}."
            if own
            else f"{sender_name} has just opened the {sname}."
        )

    if 1230855 <= item_id <= 1230863:  # Mumbo magic
        mname = MAGIC_NAMES.get(item_id, item_name)
        if dialog_character in (110, 8):  # Mumbo flavor
            return (
                f"Mumbo now use mighty {mname} spell. Bear go visit Mumbo to try."
                if own
                else f"{sender_name} told Mumbo mighty {mname} spell. Bear go visit Mumbo to try."
            )
        return (
            f"Mumbo can now use the {mname} spell."
            if own
            else f"{sender_name} has just unlocked Mumbo's {mname} spell."
        )

    if 1230174 <= item_id <= 1230182:  # Humba transformations
        tname, attribute = TRANSFORMATION_NAMES.get(item_id, (item_name, ""))
        is_bird = item_id == 1230182
        who = "bird" if is_bird else "bear"
        target = "Kazooie" if is_bird else "Banjo"
        if dialog_character in (110, 37):  # Wumba flavor
            return (
                f"Wumba now make {who} {tname}. Very {attribute}!"
                if own
                else f"{sender_name} told Wumba how to make {who} {tname}. Very {attribute}!"
            )
        return (
            f"{target} can now be transformed into a {tname}."
            if own
            else f"{sender_name} has just unlocked the {tname} transformation."
        )

    if 1230870 <= item_id <= 1230876:  # Silos
        return (
            f"{item_name} is now open!"
            if own
            else f"{sender_name} has just opened the {item_name}!"
        )

    if 1230877 <= item_id <= 1230915:  # Warp pads
        return (
            f"You can now use the {item_name}."
            if own
            else f"{sender_name} has just unlocked the {item_name}."
        )

    if 1230917 <= item_id <= 1230921:  # Cheats
        cname = CHEAT_NAMES.get(item_id, item_name)
        return (
            f"You can now use the {cname}."
            if own
            else f"{sender_name} has just sent you the {cname}."
        )

    return None


def pick_message_icon(item_id: int, dialog_character: int) -> int:
    """Pick the dialog-character icon for an item message.

    Mirrors the lua's get_item_message_char: when dialog_character is 110
    (auto), pick a thematically appropriate face per item range; if 255,
    random; otherwise the user-configured icon."""
    if dialog_character == 255:
        return random.randint(0, 109)
    if dialog_character != 110:
        return dialog_character

    # Auto-pick by item category.
    if 1230753 <= item_id <= 1230776:
        return 17  # Jamjars (BT moves)
    if item_id == 1230779:
        return 99  # Goggles (Amaze-O-Gaze)
    if item_id == 1230780:
        return 50  # Bargasaurus (Roar)
    if item_id in (1230800, 1230802):
        return 109  # Heggy (Stop'n'Swap moves)
    if 1230810 <= item_id <= 1230827:
        return 7  # Bottles (BK moves)
    if (1230777 <= item_id <= 1230778) or item_id == 1230831:
        return 56  # Roysten (water moves)
    if (
        1230828 <= item_id <= 1230830
        or item_id == 1230832
        or 1230782 <= item_id <= 1230785
    ):
        return 7  # Bottles (progressive moves)
    if item_id == 1230944:
        return 100  # Targitzan -> MT
    if item_id == 1230945:
        return 39  # Old King Coal -> GGM
    if item_id in (1230946, 1230795):
        return 31  # Mr Patch -> WW
    if item_id == 1230947:
        return 102  # Lord Woo Fak Fak -> JRL
    if item_id in (1230948, 1230791):
        return 49  # Terry -> TDL
    if item_id in (1230949, 1230790):
        return 103  # Weldar -> GI
    if item_id in (1230950, 1230793):
        return 65  # Chilly Willy -> HFP icy
    if item_id == 1230792:
        return 66  # HFP lava
    if item_id == 1230951:
        return 27  # Canary Mary -> CCL
    if item_id == 1230952:
        return 71  # Klungo -> CK
    if item_id == 1230794:
        return 8  # Mumbo (IoH station)
    if item_id == 1230796:
        return 39  # Old King Coal (Chuffy)
    if 1230855 <= item_id <= 1230863:
        return 8  # Mumbo (magic)
    if 1230174 <= item_id <= 1230182:
        return 37  # Wumba (transformations)
    if 1230870 <= item_id <= 1230876:
        return 17  # Jamjars (silos)
    if 1230877 <= item_id <= 1230881:
        return 100  # Targitzan (MT warps)
    if 1230882 <= item_id <= 1230886:
        return 39  # Old King Coal (GGM warps)
    if 1230887 <= item_id <= 1230891:
        return 31  # Mr Patch (WW warps)
    if 1230892 <= item_id <= 1230896:
        return 102  # Lord Woo Fak Fak (JRL warps)
    if 1230897 <= item_id <= 1230901:
        return 49  # Terry (TDL warps)
    if 1230902 <= item_id <= 1230906:
        return 103  # Weldar (GI warps)
    if 1230907 <= item_id <= 1230911:
        return 65  # Chilly Willy (HFP warps)
    if 1230912 <= item_id <= 1230915:
        return 27  # Canary Mary (CCL warps)
    if 1230917 <= item_id <= 1230921:
        return 28  # Cheato (cheats)
    return 7  # Default: Bottles


def drain_item_messages(
    loader: BTEmuLoaderClient,
    pending: Dict[int, Any],
    local_player_name: str,
    dialog_character: int,
) -> int:
    """Pop up to one queued item message off `pending` and push it to the ROM
    dialog buffer if the queue is free. Returns the dict key that was consumed
    (so the caller can `del pending[key]`), or 0 if nothing was sent."""
    if not pending:
        return 0

    # Don't stomp the previous message; wait for the ROM to read it.
    if read_pc_text_queue(loader) != read_n64_text_queue(loader):
        return 0

    for key in sorted(pending.keys()):
        msg = pending[key]
        if not isinstance(msg, dict):
            return key  # Drop unstructured entries
        if msg.get("to_player") != local_player_name:
            return key  # Item we sent to someone else

        item_id = int(msg.get("item_id", 0))
        item_name = str(msg.get("item", ""))
        sender = str(msg.get("player", ""))
        text = format_item_message(
            item_id, item_name, sender, sender == local_player_name, dialog_character
        )
        if text is None:
            return key  # No dedicated text for this item

        icon = pick_message_icon(item_id, dialog_character)
        if send_pc_dialog(loader, text, icon):
            return key
        return 0  # Couldn't write (ptrs unresolved); try again next tick.

    return 0


# Victory detection and HAG-1 access
AP_ITEM_H1A_INDEX = 110
END_GAME_MAP = 0x191


def check_victory(loader: BTEmuLoaderClient, slot_data: Mapping[str, Any]) -> bool:
    """Return True if the active win condition has been met.

    Goal types:
      0 - Defeat HAG-1                          -> HAG-1 defeated flag set
      1 - Minigame Hunt (token count)           -> tokens >= minigame_hunt_length
      2 - Boss Hunt (token count)               -> tokens >= boss_hunt_length
      3 - Jinjo Family Rescue                   -> tokens >= jinjo_family_rescue_length AND on END_GAME_MAP
      4 - Wonder Wing (HAG-1 after 32 tokens)   -> HAG-1 defeated flag set
      5 - Token Hunt                            -> tokens >= token_hunt_length AND on END_GAME_MAP
      6 - Boss Hunt + HAG-1                     -> HAG-1 defeated flag set

    Token-based goals return False when their length option is missing so
    the seed never auto-finishes on partial data.
    """
    reader = BTHReader(loader)
    items_ptr = reader.items_ptr()
    if items_ptr is None:
        return False

    options = slot_data.get("options", {}) or {}
    goal_type = opt(options, "victory_condition", 0)

    if goal_type in (0, 4, 6):
        # H1 category from the address registry: real_flags(0x03, 3).
        return bool(reader.check_real_flag(0x03, 3))

    if goal_type == 1:
        length = opt(options, "minigame_hunt_length", -1)
        if length <= 0:
            return False
        tokens = loader.read_u8(items_ptr + AP_ITEM_INDEX[1230798])
        return tokens >= length

    if goal_type == 2:
        length = opt(options, "boss_hunt_length", -1)
        if length <= 0:
            return False
        tokens = loader.read_u8(items_ptr + AP_ITEM_INDEX[1230798])
        return tokens >= length

    if goal_type == 3:
        length = opt(options, "jinjo_family_rescue_length", -1)
        if length <= 0 or reader.current_map() != END_GAME_MAP:
            return False
        tokens = loader.read_u8(items_ptr + AP_ITEM_INDEX[1230798])
        return tokens >= length

    if goal_type == 5:
        length = opt(options, "token_hunt_length", -1)
        if length <= 0 or reader.current_map() != END_GAME_MAP:
            return False
        tokens = loader.read_u8(items_ptr + AP_ITEM_INDEX[1230798])
        return tokens >= length

    return False


def apply_hag1_open(loader: BTEmuLoaderClient, slot_data: Mapping[str, Any]) -> bool:
    """Set the HAG-1 access flag if the goal-type threshold is met.

    Returns True iff this call flipped the flag from 0 to 1.
    """
    reader = BTHReader(loader)
    items_ptr = reader.items_ptr()
    if items_ptr is None:
        return False

    if loader.read_u8(items_ptr + AP_ITEM_H1A_INDEX) == 1:
        return False

    options = slot_data.get("options", {}) or {}
    goal_type = opt(options, "victory_condition", 0)
    if goal_type in (1, 2, 5):
        # Pure token-count goals don't use HAG-1 access at all.
        return False

    total_jiggy = read_count(loader, reader, AP_ITEM_INDEX[1230515])
    total_tokens = read_count(loader, reader, AP_ITEM_INDEX[1230798])
    open_hag1 = opt(options, "open_hag1", 0) != 0

    should_open = False
    if goal_type == 0:
        if open_hag1 or total_jiggy >= 70:
            should_open = True
    elif goal_type == 4:
        if total_tokens >= 32:
            should_open = True
    elif goal_type == 6:
        bh_length = opt(options, "boss_hunt_length", 999)
        if total_tokens >= bh_length:
            should_open = True

    if should_open:
        loader.write_u8(items_ptr + AP_ITEM_H1A_INDEX, 1)
        return True
    return False


# World entrance checks
WORLD_ENTRANCE_DEFAULT_COSTS: Dict[str, int] = {
    "Mayahem Temple": 1,
    "Glitter Gulch Mine": 4,
    "Witchyworld": 8,
    "Jolly Roger's Lagoon": 14,
    "Jolly Roger's Lagoon - Town Center": 14,
    "Terrydactyland": 20,
    "Grunty Industries": 28,
    "Outside Grunty Industries": 28,
    "Hailfire Peaks": 36,
    "Cloud Cuckooland": 45,
    "Cauldron Keep": 55,
}


def check_world_entrances_open(
    loader: BTEmuLoaderClient, slot_data: Mapping[str, Any]
) -> List[int]:
    """World-entrance location IDs the player is now eligible to check based
    on current jiggy count. The caller is responsible for diffing against
    what they've already sent."""
    reader = BTHReader(loader)
    if reader.items_ptr() is None:
        return []

    bt_data = slot_data.get("custom_bt_data", {}) or {}
    world_order: Mapping[str, Any] = bt_data.get("world_order") or {}
    world_reqs: Mapping[str, Any] = bt_data.get("world_requirements") or {}
    if not world_order:
        return []

    total_jiggy = read_count(loader, reader, AP_ITEM_INDEX[1230515])

    eligible: List[int] = []
    for world_name, loc_id in world_order.items():
        if not isinstance(loc_id, int):
            continue
        cost = world_reqs.get(
            world_name, WORLD_ENTRANCE_DEFAULT_COSTS.get(world_name, 999)
        )
        if isinstance(cost, int) and total_jiggy >= cost:
            eligible.append(loc_id)
    return eligible


# BK-moves giveaway
# Indices match the BK-moves block in AP_ITEM_INDEX above.
BK_MOVE_INDICES: Tuple[int, ...] = (
    29,
    30,
    37,
    46,
    32,
    40,
    35,
    38,
    36,
    42,
    41,
    44,
    33,
    39,
    31,
    34,
    43,
    45,
)


def write_default_bk_moves(loader: BTEmuLoaderClient, randomize_bk_moves: int) -> int:
    """Grant default BK moves at slot-setup time when they aren't randomized.

      - ``randomize_bk_moves == 0``: grant all 18 default BK moves.
      - ``randomize_bk_moves == 1``: grant only TJUMP + TTROT.

    Returns the number of move slots written.
    """
    reader = BTHReader(loader)
    items_ptr = reader.items_ptr()
    if items_ptr is None:
        return 0
    if randomize_bk_moves == 0:
        for idx in BK_MOVE_INDICES:
            loader.write_u8(items_ptr + idx, 1)
        return len(BK_MOVE_INDICES)
    if randomize_bk_moves == 1:
        loader.write_u8(items_ptr + 35, 1)  # TJUMP
        loader.write_u8(items_ptr + 40, 1)  # TTROT
        return 2
    return 0


# Diagnostic helper
def dump_current_settings(loader: BTEmuLoaderClient) -> Dict[str, Any]:
    """Read back the settings struct as it currently sits in RAM. Useful for
    confirming a write took effect."""
    reader = BTHReader(loader)
    ptr = reader.settings_ptr()
    if ptr is None:
        return {"error": "no settings pointer"}
    return {
        "seed": loader.read_u32(ptr + SETTING_SEED),
        "victory_condition": loader.read_u8(ptr + SETTING_VICTORY_CONDITION),
        "chuffy": loader.read_u8(ptr + SETTING_CHUFFY),
        "nestsanity": loader.read_u8(ptr + SETTING_NESTS),
        "randomize_warp_pads": loader.read_u8(ptr + SETTING_WARPPADS),
        "randomize_silos": loader.read_u8(ptr + SETTING_WARPSILOS),
        "honeyb_rewards": loader.read_u8(ptr + SETTING_HONEYB_REWARDS),
        "cheato_rewards": loader.read_u8(ptr + SETTING_CHEATO_REWARDS),
        "randomize_tickets": loader.read_u8(ptr + SETTING_RANDOMIZE_TICKETS),
        "randomize_green_relics": loader.read_u8(ptr + SETTING_RANDOMIZE_GREEN_RELICS),
        "randomize_beans": loader.read_u8(ptr + SETTING_RANDOMIZE_BEANS),
        "skip_puzzles": loader.read_u8(ptr + SETTING_PUZZLE),
        "backdoors": loader.read_u8(ptr + SETTING_BACKDOORS),
        "open_gi_frontdoor": loader.read_u8(ptr + SETTING_GI_OPEN_FRONTDOOR),
        "skip_klungo": loader.read_u8(ptr + SETTING_KLUNGO),
        "tower_of_tragedy": loader.read_u8(ptr + SETTING_TOT),
        "speed_up_minigames": loader.read_u8(ptr + SETTING_MINIGAMES),
        "dialog_character": loader.read_u8(ptr + SETTING_DIALOG_CHARACTER),
        "signpost_hints": loader.read_u8(ptr + SETTING_SIGNPOST_HINTS),
        "extra_cheats": loader.read_u8(ptr + SETTING_EXTRA_CHEATS),
        "auto_enable_cheats": loader.read_u8(ptr + SETTING_AUTOMATIC_CHEATS),
        "easy_canary": loader.read_u8(ptr + SETTING_EASY_CANARY),
        "jiggy_requirements": [
            loader.read_u8(ptr + SETTING_JIGGY_REQUIREMENTS_BASE + i) for i in range(11)
        ],
        "silo_requirements": [
            loader.read_u16(ptr + SETTING_SILO_REQUIREMENTS_BASE + i * 2)
            for i in range(24)
        ],
    }
