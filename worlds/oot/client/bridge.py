"""
OoT AP bridge: attaches to N64 emulator memory, serves connector protocol on :28921.
"""

import asyncio
import json
from typing import Callable, Dict, List, Optional, Set, Tuple

try:
    from CommonClient import logger
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

from .emu_loader import EmuLoaderClient
from ..LocationList import business_scrubs, location_table
from ..Utils import OOT_PLAYER_NAME_LENGTH, encode_oot_player_name

SCRIPT_VERSION = 8
CONNECT_PORT   = 28921
OUTGOING_KEY_POLL_FRAMES = 6
PROTOCOL_EXCHANGE_FRAMES = 10
FULL_STATE_FRAMES = 30
CACHE_RESYNC_FRAMES = 1800

# COOP_CONTEXT layout at 0x80400020 (RDRAM 0x00400020)
COOP_VERSION_ADDR       = 0x00400020   # u32 = 7
PLAYER_ID_ADDR          = 0x00400024   # u8
INCOMING_PLAYER_ADDR    = 0x00400026   # u16
INCOMING_ITEM_ADDR      = 0x00400028   # u16
DEATH_LINK_ADDR         = 0x0040002B   # u8  (MW_PROGRESSIVE_ITEMS_ENABLE / DEATH_LINK)
PLAYER_NAMES_ADDR       = 0x00400034   # 256 × 8 bytes
FILE_HASH_ADDR          = 0x00400834   # 5 bytes  (CFG_FILE_SELECT_HASH)
OUTGOING_KEY_ADDR       = 0x00400C3C   # 8 bytes  (override_key_t)
DUNGEON_IS_MQ_PTR_ADDR  = 0x00400010   # N64 pointer to MQ dungeon table
BIG_POE_COUNT_ADDR      = 0x0040001E   # u8

# Some generated OoT symbols are stored in the payload using their linked ROM
# address (for example 0x03481E66) rather than an 0x80xxxxxx runtime pointer.
PAYLOAD_SYMBOL_BASE     = 0x03080000
HP_ADDR                 = 0x11A600    # u16  (+0x30)
EQUIPMENT_ADDR          = 0x11A640    # u32  (+0x70)
INTERNAL_COUNT_ADDR     = 0x11A660    # u16  (+0x90)
SCENE_FLAGS_ADDR        = 0x11A6A4    # array (+0xD4, 0x1C per scene)
SHOP_CONTEXT_ADDR       = 0x11AB84    # u32  (+0x5B4)
SKULLTULA_FLAGS_ADDR    = 0x11B46C    # bytes (+0xE9C)
EVENT_CONTEXT_ADDR      = 0x11B4A4    # u16 array (+0xED4)
BIG_POE_POINTS_ADDR     = 0x11B48C    # u32  (+0xEBC)
FISHING_CONTEXT_ADDR    = 0x11B490    # u32  (+0xEC0)
ITEM_GET_INF_ADDR       = 0x11B4C0    # bytes (+0xEF0)
INF_TABLE_ADDR          = 0x11B4C8    # bytes (+0xEF8)

# Global context (base 0x1C84A0)
CUR_SCENE_ADDR          = 0x1C8544    # u16  (+0xA4)

# Game state
LOGO_STATE_ADDR         = 0x11F200    # u32
STATE_MAIN_ADDR         = 0x11B92F    # u8
STATE_SUB_ADDR          = 0x11B933    # u8
STATE_MENU_ADDR         = 0x1D8DD5    # u8
LINK_DYING_ADDR         = 0x1DB09F    # u8, bit 7 = dying flag
SCENE_PTR_ADDR          = 0x1CA208    # u32, current scene pointer

TRIFORCE_HUNT_COMPLETE  = 0x80383C10
GANON_DEFEATED          = 0x80382720

GAME_MODES: Dict[int, tuple] = {
    -1: ("Unknown",          False),
     0: ("N64 Logo",         False),
     1: ("Title Screen",     False),
     2: ("File Select",      False),
     3: ("Normal Gameplay",  True),
     4: ("Cutscene",         True),
     5: ("Paused",           True),
     6: ("Dying",            True),
     7: ("Dying Menu Start", False),
     8: ("Dead",             False),
}

SHOP_SCENES             = {0x2C, 0x2D, 0x2E, 0x2F, 0x30, 0x31, 0x32, 0x33, 0x42, 0x4B}
KILL_LINK_EXCLUDE_SCENES = {27, 28, 29, 35, 36, 37}
PLAYER_NAME_LENGTH      = OOT_PLAYER_NAME_LENGTH


class OoTBridgeState:
    __slots__ = (
        "temp_context_history", "mq_table_address", "collectible_overrides",
        "collectible_offsets", "item_queue", "first_connect",
        "player_names_initialized", "game_complete", "num_big_poes_required",
        "shop_flag_offsets", "location_cache", "location_cache_dirty",
    )

    def __init__(self) -> None:
        self.temp_context_history:    Set[str]         = set()
        self.mq_table_address:        Optional[int]    = None
        self.collectible_overrides:   Optional[int]    = None
        self.collectible_offsets                       = None
        self.item_queue:              List[int]        = []
        self.first_connect:           bool             = True
        self.player_names_initialized: bool            = False
        self.game_complete:           bool             = False
        self.num_big_poes_required:   int              = 10
        self.shop_flag_offsets:       dict             = {}
        self.location_cache:          Optional[dict]   = None
        self.location_cache_dirty:    bool             = True

    def reset_connection(self) -> None:
        self.temp_context_history = set()
        self.first_connect        = True
        self.location_cache       = None
        self.location_cache_dirty = True


def _get_current_game_mode(emu: EmuLoaderClient) -> int:
    logo = emu.read_u32(LOGO_STATE_ADDR)
    if logo in (0x802C5880, 0x00000000):
        return 0
    main = emu.read_u8(STATE_MAIN_ADDR)
    if main == 1:
        return 1
    if main == 2:
        return 2
    menu = emu.read_u8(STATE_MENU_ADDR)
    if menu == 0:
        if bool(emu.read_u8(LINK_DYING_ADDR) & 0x80) or emu.read_u16(HP_ADDR) == 0:
            return 6
        return 4 if emu.read_u8(STATE_SUB_ADDR) == 4 else 3
    if 0 < menu < 9 or menu == 13:
        return 5
    if menu in (9, 0xB):
        return 7
    return 8


def _in_safe_state(emu: EmuLoaderClient) -> bool:
    return GAME_MODES[_get_current_game_mode(emu)][1]


def _deathlink_enabled(emu: EmuLoaderClient) -> bool:
    return emu.read_u8(DEATH_LINK_ADDR) > 0


def _get_death_state(emu: EmuLoaderClient) -> bool:
    name = GAME_MODES[_get_current_game_mode(emu)][0]
    if name in ("N64 Logo", "File Select"):
        return False
    return emu.read_u16(HP_ADDR) == 0


def _is_game_complete(emu: EmuLoaderClient, state: OoTBridgeState) -> bool:
    if state.game_complete:
        return True
    if emu.read_u32(SCENE_PTR_ADDR) in (TRIFORCE_HUNT_COMPLETE, GANON_DEFEATED):
        state.game_complete = True
        return True
    return False


def _get_player_name(emu: EmuLoaderClient) -> str:
    pid = emu.read_u8(PLAYER_ID_ADDR)
    h   = [emu.read_u8(FILE_HASH_ADDR + i) for i in range(5)]
    return f"OOT{pid:03d}-{h[0]:02x}{h[1]:02x}{h[2]:02x}{h[3]:02x}{h[4]:02x}"


def _item_receivable(emu: EmuLoaderClient) -> bool:
    if GAME_MODES[_get_current_game_mode(emu)][0] != "Normal Gameplay":
        return False
    if emu.read_u16(CUR_SCENE_ADDR) in SHOP_SCENES:
        return False
    return emu.read_u16(INCOMING_PLAYER_ADDR) == 0 and emu.read_u16(INCOMING_ITEM_ADDR) == 0


def _kill_link(emu: EmuLoaderClient) -> None:
    if emu.read_u16(CUR_SCENE_ADDR) not in KILL_LINK_EXCLUDE_SCENES:
        emu.write_u16(HP_ADDR, 0)


def _override_key(scene: int, loc_type: int, flag: int) -> str:
    return f"{scene % 0x100:02X}:{loc_type % 0x100:02X}:{flag % 0x100:02X}"


def _poll_outgoing_key(emu: EmuLoaderClient, state: OoTBridgeState) -> None:
    high = emu.read_u32(OUTGOING_KEY_ADDR)
    low  = emu.read_u32(OUTGOING_KEY_ADDR + 4)
    if high == 0 and low == 0:
        return
    scene    = emu.read_u8(OUTGOING_KEY_ADDR + 0)
    loc_type = emu.read_u8(OUTGOING_KEY_ADDR + 1)
    flag     = emu.read_u8(OUTGOING_KEY_ADDR + 7)  # flag LSB = bit index
    key = _override_key(scene, loc_type, flag)
    state.temp_context_history.add(key)
    _apply_outgoing_key_to_cache(state, key)
    emu.write_u32(OUTGOING_KEY_ADDR,     0)
    emu.write_u32(OUTGOING_KEY_ADDR + 4, 0)


def _check_temp_context(state: OoTBridgeState, scene: int, loc_type: int, flag: int) -> bool:
    return _override_key(scene, loc_type, flag) in state.temp_context_history


def _set_player_name(emu: EmuLoaderClient, player_id: int, name: str) -> None:
    addr    = PLAYER_NAMES_ADDR + player_id * PLAYER_NAME_LENGTH
    data = bytes(encode_oot_player_name(name, PLAYER_NAME_LENGTH))
    # Player name slots are 8-byte/4-byte aligned; write as words to avoid
    # hundreds of synchronous RetroArch UDP writes on first connect.
    emu.write_u32(addr, int.from_bytes(data[:4], "big"))
    emu.write_u32(addr + 4, int.from_bytes(data[4:], "big"))


def _resolve_mq_table(emu: EmuLoaderClient, state: OoTBridgeState) -> None:
    ptr = emu.read_u32(DUNGEON_IS_MQ_PTR_ADDR)
    if 0x80000000 <= ptr < 0x80800000:
        state.mq_table_address = ptr - 0x80000000
    elif PAYLOAD_SYMBOL_BASE <= ptr < PAYLOAD_SYMBOL_BASE + 0x00800000:
        state.mq_table_address = ptr - PAYLOAD_SYMBOL_BASE
    else:
        state.mq_table_address = None


def _is_mq(emu: EmuLoaderClient, state: OoTBridgeState, dungeon_id: int) -> bool:
    if state.mq_table_address is None:
        return False
    return emu.read_u8(state.mq_table_address + dungeon_id) == 1


def _sc(emu: EmuLoaderClient, scene: int, bit: int, off: int) -> bool:
    """scene_check: read scene flag word and test a bit."""
    return bool(emu.read_u32(SCENE_FLAGS_ADDR + 0x1C * scene + off) & (1 << bit))


def _chest(emu: EmuLoaderClient, st: OoTBridgeState, scene: int, bit: int) -> bool:
    return _sc(emu, scene, bit, 0x0) or _check_temp_context(st, scene, 0x01, bit)


def _ground(emu: EmuLoaderClient, st: OoTBridgeState, scene: int, bit: int) -> bool:
    return _sc(emu, scene, bit, 0xC) or _check_temp_context(st, scene, 0x02, bit)


def _boss_item(emu: EmuLoaderClient, st: OoTBridgeState, scene: int) -> bool:
    return _ground(emu, st, scene, 0x1F) or _check_temp_context(st, scene, 0x00, 0x4F)


def _boss_reward(st: OoTBridgeState, flag: int) -> bool:
    return _check_temp_context(st, 0xFF, 0x05, flag)


def _boss_heart(emu: EmuLoaderClient, st: OoTBridgeState, scene: int, flag: int) -> bool:
    return _boss_item(emu, st, scene) or _boss_reward(st, flag)


def _scrub(emu: EmuLoaderClient, scene: int, bit: int) -> bool:
    return _sc(emu, scene, bit, 0x10)


def _bombchu_bowling(emu: EmuLoaderClient, prize_index: int) -> bool:
    return _sc(emu, 0x4B, prize_index, 0x10)


def _cow(emu: EmuLoaderClient, st: OoTBridgeState, scene: int, bit: int) -> bool:
    return _sc(emu, scene, bit, 0xC) or _check_temp_context(st, scene, 0x00, bit - 0x03)


def _fairy(emu: EmuLoaderClient, st: OoTBridgeState, scene: int, bit: int) -> bool:
    return _sc(emu, scene, bit, 0x4) or _check_temp_context(st, scene, 0x05, bit)


def _fire_arrows(emu: EmuLoaderClient, st: OoTBridgeState, scene: int, bit: int) -> bool:
    return _sc(emu, scene, bit, 0x0) or _check_temp_context(st, scene, 0x00, 0x58)


def _bean(emu: EmuLoaderClient, st: OoTBridgeState, scene: int, bit: int) -> bool:
    return _sc(emu, scene, bit, 0xC) or _check_temp_context(st, scene, 0x00, 0x16)


def _medigoron(emu: EmuLoaderClient, st: OoTBridgeState, scene: int, bit: int) -> bool:
    return _sc(emu, scene, bit, 0xC) or _check_temp_context(st, scene, 0x00, 0x28)


def _salesman(emu: EmuLoaderClient, st: OoTBridgeState, scene: int, bit: int) -> bool:
    return _sc(emu, scene, bit, 0xC) or _check_temp_context(st, scene, 0x00, 0x03)


def _skulltula(emu: EmuLoaderClient, scene: int, bit: int) -> bool:
    idx = (scene + 3) - 2 * (scene % 4)
    return bool(emu.read_u8(SKULLTULA_FLAGS_ADDR + idx) & (1 << bit))


def _shop(emu: EmuLoaderClient, shop_off: int, item_off: int) -> bool:
    return bool(emu.read_u32(SHOP_CONTEXT_ADDR) & (1 << (shop_off * 4 + item_off)))


def _shop_flag(emu: EmuLoaderClient, flag: int) -> bool:
    return bool(emu.read_u8(SHOP_CONTEXT_ADDR + (flag >> 3)) & (1 << (flag & 7)))


def _shop_location(emu: EmuLoaderClient, st: OoTBridgeState, location_name: str, scene: int, get_item_id: int) -> bool:
    flag = st.shop_flag_offsets.get(location_name)
    if flag is not None:
        return _shop_flag(emu, int(flag)) or _base_item(emu, st, scene, get_item_id)
    return False


def _event(emu: EmuLoaderClient, major: int, bit: int) -> bool:
    return bool(emu.read_u16(EVENT_CONTEXT_ADDR + 2 * major) & (1 << bit))


def _igi(emu: EmuLoaderClient, off: int, bit: int) -> bool:
    return bool(emu.read_u8(ITEM_GET_INF_ADDR + off) & (1 << bit))


def _inf(emu: EmuLoaderClient, off: int, bit: int) -> bool:
    return bool(emu.read_u8(INF_TABLE_ADDR + off) & (1 << bit))


def _poe_bottle(emu: EmuLoaderClient, st: OoTBridgeState) -> bool:
    points = emu.read_u32(BIG_POE_POINTS_ADDR)
    count  = emu.read_u8(BIG_POE_COUNT_ADDR)
    if count:
        st.num_big_poes_required = count
    else:
        count = st.num_big_poes_required
    return count > 0 and points >= 100 * count


def _fishing(emu: EmuLoaderClient, adult: bool) -> bool:
    return bool(emu.read_u32(FISHING_CONTEXT_ADDR) & (1 << (11 if adult else 10)))


def _loach_fishing(emu: EmuLoaderClient) -> bool:
    return bool(emu.read_u32(FISHING_CONTEXT_ADDR) & 0x8000)


def _bgs(emu: EmuLoaderClient) -> bool:
    return bool(emu.read_u32(EQUIPMENT_ADDR) & (1 << 0x8))


def _tcg_salesman(emu: EmuLoaderClient, st: OoTBridgeState) -> bool:
    return _sc(emu, 0x10, 0x01, 0x0C) or _check_temp_context(st, 0x10, 0x00, 0x71)


def _adult_trade(emu: EmuLoaderClient, st: OoTBridgeState, scene: int, get_item_id: int, traded_bit: int) -> bool:
    return _sc(emu, 0x62, traded_bit, 0x10) or _check_temp_context(st, scene, 0x00, get_item_id)


def _base_item(emu: EmuLoaderClient, st: OoTBridgeState, scene: int, get_item_id: int) -> bool:
    return _check_temp_context(st, scene, 0x00, get_item_id)


def _membership(emu: EmuLoaderClient) -> bool:
    return _event(emu, 0x9, 0) and _event(emu, 0x9, 1) and _event(emu, 0x9, 2) and _event(emu, 0x9, 3)


SHOP_CONTEXT_OFFSETS: Dict[int, int] = {
    # ROM shop table index -> save-context shop bitfield group.
    0: 6,  # Kokiri Shop
    1: 3,  # Kak Potion Shop
    2: 1,  # Market Bombchu Shop
    3: 0,  # Market Potion Shop
    4: 4,  # Market Bazaar
    5: 7,  # Kak Bazaar
    7: 2,  # Zora Shop
    8: 5,  # Goron Shop
}

MQ_DUNGEON_TAGS: Dict[str, int] = {
    "Deku Tree": 0x0,
    "Dodongo's Cavern": 0x1,
    "Jabu Jabu's Belly": 0x2,
    "Forest Temple": 0x3,
    "Fire Temple": 0x4,
    "Water Temple": 0x5,
    "Spirit Temple": 0x6,
    "Shadow Temple": 0x7,
    "Bottom of the Well": 0x8,
    "Ice Cavern": 0x9,
    "Gerudo Training Ground": 0xB,
    "Gerudo Training Ground MQ": 0xB,
    "Ganon's Castle": 0xD,
}

BOSS_HEART_REWARD_FLAGS: Dict[int, int] = {
    0x11: 0x05,  # Queen Gohma
    0x12: 0x06,  # King Dodongo
    0x13: 0x07,  # Barinade
    0x14: 0x08,  # Phantom Ganon
    0x15: 0x09,  # Volvagia
    0x16: 0x0A,  # Morpha
    0x17: 0x0B,  # Twinrova
    0x18: 0x0C,  # Bongo Bongo
}

GenericLocationRule = Tuple[str, str, Tuple[int, ...], Tuple[str, ...]]
SCRUB_ITEM_BITS: Dict[int, int] = {
    scrub_item: index
    for index, (scrub_item, _default_price, _text_id, _text_replacement) in enumerate(business_scrubs, start=1)
}
GROTTO_SCRUB_SCENE_BASE = 0xD6

SCRUB_FALLBACK_CHECKS: Dict[str, Callable[[EmuLoaderClient, OoTBridgeState], bool]] = {
    "LW Deku Scrub Near Bridge": lambda emu, st: _inf(emu, 0x33, 0x2),
    "LW Deku Scrub Grotto Front": lambda emu, st: _inf(emu, 0x33, 0x3),
    "HF Deku Scrub Grotto": lambda emu, st: _igi(emu, 0x0, 0x3),
}


def _as_tags(tags) -> Tuple[str, ...]:
    if tags is None:
        return ()
    if isinstance(tags, str):
        return (tags,)
    return tuple(tags)


def _mask_to_bit(mask: int) -> int:
    return mask.bit_length() - 1


def _active_location_variant(emu: EmuLoaderClient, st: OoTBridgeState, tags: Tuple[str, ...]) -> bool:
    has_vanilla = "Vanilla" in tags
    has_mq = "Master Quest" in tags
    if has_vanilla == has_mq:
        return True

    for tag, dungeon_id in MQ_DUNGEON_TAGS.items():
        if tag in tags:
            is_mq = _is_mq(emu, st, dungeon_id)
            return is_mq if has_mq else not is_mq
    return True


def _is_shop_slot_5_to_8(name: str) -> bool:
    return name.endswith(("Item 5", "Item 6", "Item 7", "Item 8"))


def _shop_context_rule(name: str, addresses) -> Optional[Tuple[int, int]]:
    if not _is_shop_slot_5_to_8(name) or addresses is None:
        return None
    address = addresses[0]
    if address is None:
        return None

    offset = address - 0xC71ED0
    if offset < 0:
        return None
    rom_shop_id = offset // 0x40
    shelf_id = (offset % 0x40) // 0x08
    shop_context = SHOP_CONTEXT_OFFSETS.get(rom_shop_id)
    if shop_context is None or not 4 <= shelf_id <= 7:
        return None
    return shop_context, shelf_id - 4


def _scrub_rule(loc_type: str, scene: int, default: int) -> Optional[Tuple[int, int]]:
    bit = SCRUB_ITEM_BITS.get(default)
    if bit is None:
        return None
    if loc_type == "GrottoScrub":
        return scene - GROTTO_SCRUB_SCENE_BASE, bit
    return scene, bit


def _build_generic_location_rules() -> List[GenericLocationRule]:
    rules: List[GenericLocationRule] = []
    for name, data in location_table.items():
        loc_type, scene, default, addresses, _vanilla_item, tags = data
        tag_tuple = _as_tags(tags)

        if loc_type == "Chest" and scene is not None and default is not None:
            rules.append((name, "chest", (int(scene), int(default)), tag_tuple))
        elif loc_type == "Collectable" and scene is not None and default is not None:
            rules.append((name, "ground", (int(scene), int(default)), tag_tuple))
        elif loc_type == "GS Token" and scene is not None and default is not None:
            rules.append((name, "skulltula", (int(scene), _mask_to_bit(int(default))), tag_tuple))
        elif loc_type == "Shop":
            shop_rule = _shop_context_rule(name, addresses)
            if shop_rule is not None:
                rules.append((name, "shop", shop_rule, tag_tuple))
        elif loc_type == "MaskShop" and scene is not None and default is not None:
            rules.append((name, "mask_shop", (int(scene), int(default)), tag_tuple))
        elif loc_type == "Boss" and default is not None:
            rules.append((name, "boss", (int(default),), tag_tuple))
        elif loc_type == "BossHeart" and scene in BOSS_HEART_REWARD_FLAGS:
            rules.append((name, "boss_heart", (int(scene), BOSS_HEART_REWARD_FLAGS[int(scene)]), tag_tuple))
        elif loc_type in {"Scrub", "GrottoScrub"} and scene is not None and default is not None:
            scrub_rule = _scrub_rule(loc_type, int(scene), int(default))
            if scrub_rule is not None:
                rules.append((name, "scrub", scrub_rule, tag_tuple))

    return rules


GENERIC_LOCATION_RULES = _build_generic_location_rules()

# Special locations that need extra bridge information not derivable from the location list (like scene-specific permanent bits)
SPECIAL_LOCATION_CHECKS: Dict[str, Callable[[EmuLoaderClient, OoTBridgeState], bool]] = {
    "KF Links House Cow": lambda emu, st: _cow(emu, st, 0x34, 0x18),
    "LW Gift from Saria": lambda emu, st: _event(emu, 0xC, 0x1),
    "LW Ocarina Memory Game": lambda emu, st: _igi(emu, 0x3, 0x7),
    "LW Target in Woods": lambda emu, st: _igi(emu, 0x2, 0x5),
    "Deku Theater Skull Mask": lambda emu, st: _igi(emu, 0x2, 0x6),
    "Deku Theater Mask of Truth": lambda emu, st: _igi(emu, 0x2, 0x7),
    "LW Skull Kid": lambda emu, st: _igi(emu, 0x3, 0x6),
    "LW Trade Cojiro": lambda emu, st: _adult_trade(emu, st, 0x5B, 0x1F, 13),
    "LW Trade Odd Potion": lambda emu, st: _adult_trade(emu, st, 0x5B, 0x21, 15),
    "HF Ocarina of Time Item": lambda emu, st: _event(emu, 0x4, 0x3),
    "HF Cow Grotto Cow": lambda emu, st: _cow(emu, st, 0x3E, 0x19),
    "LLR Talons Chickens": lambda emu, st: _igi(emu, 0x1, 0x2),
    "LLR Tower Left Cow": lambda emu, st: _cow(emu, st, 0x4C, 0x19),
    "LLR Tower Right Cow": lambda emu, st: _cow(emu, st, 0x4C, 0x18),
    "LLR Stables Left Cow": lambda emu, st: _cow(emu, st, 0x36, 0x18),
    "LLR Stables Right Cow": lambda emu, st: _cow(emu, st, 0x36, 0x19),
    "Gift from Sages": lambda emu, st: _check_temp_context(st, 0xFF, 0x05, 0x03),
    "Market Shooting Gallery Reward": lambda emu, st: _igi(emu, 0x0, 0x5),
    "Market Bombchu Bowling First Prize": lambda emu, st: _bombchu_bowling(emu, 0),
    "Market Bombchu Bowling Second Prize": lambda emu, st: _bombchu_bowling(emu, 1),
    "Market Treasure Chest Game Salesman": lambda emu, st: _tcg_salesman(emu, st),
    "Market Treasure Chest Game Reward": lambda emu, st: _igi(emu, 0x2, 0x3) or _chest(emu, st, 0x10, 0x0A),
    "Market Lost Dog": lambda emu, st: _inf(emu, 0x33, 0x1),
    "Market 10 Big Poes": lambda emu, st: _poe_bottle(emu, st),
    "ToT Light Arrows Cutscene": lambda emu, st: _event(emu, 0xC, 0x4),
    "ToT Reward from Rauru": lambda emu, st: _event(emu, 0x4, 0x5) or _boss_reward(st, 0x04),
    "HC Malon Egg": lambda emu, st: _event(emu, 0x1, 0x2),
    "HC Zeldas Letter": lambda emu, st: _event(emu, 0x4, 0x0),
    "HC Great Fairy Reward": lambda emu, st: _igi(emu, 0x2, 0x1),
    "Kak Anju as Child": lambda emu, st: _igi(emu, 0x0, 0x4),
    "Kak Anju as Adult": lambda emu, st: _igi(emu, 0x4, 0x4),
    "Kak Anju Trade Pocket Cucco": lambda emu, st: _adult_trade(emu, st, 0x52, 0x0E, 12),
    "Kak Granny Trade Odd Mushroom": lambda emu, st: _adult_trade(emu, st, 0x4E, 0x20, 14),
    "Kak Granny Buy Blue Potion": lambda emu, st: _sc(emu, 0x4E, 0x00, 0x10) or _base_item(emu, st, 0x4E, 0x12),
    "Kak Man on Roof": lambda emu, st: _igi(emu, 0x3, 0x5),
    "Kak Shooting Gallery Reward": lambda emu, st: _igi(emu, 0x0, 0x6),
    "Kak 10 Gold Skulltula Reward": lambda emu, st: _event(emu, 0xD, 0xA),
    "Kak 20 Gold Skulltula Reward": lambda emu, st: _event(emu, 0xD, 0xB),
    "Kak 30 Gold Skulltula Reward": lambda emu, st: _event(emu, 0xD, 0xC),
    "Kak 40 Gold Skulltula Reward": lambda emu, st: _event(emu, 0xD, 0xD),
    "Kak 50 Gold Skulltula Reward": lambda emu, st: _event(emu, 0xD, 0xE),
    "Kak 100 Gold Skulltula Reward": lambda emu, st: _base_item(emu, st, 0x50, 0x56),
    "Kak Impas House Cow": lambda emu, st: _cow(emu, st, 0x37, 0x18),
    "DMT Great Fairy Reward": lambda emu, st: _fairy(emu, st, 0x3B, 0x18) or _check_temp_context(st, 0xFF, 0x05, 0x13),
    "DMT Biggoron": lambda emu, st: _bgs(emu) or _adult_trade(emu, st, 0x60, 0x57, 21),
    "DMT Trade Broken Sword": lambda emu, st: _adult_trade(emu, st, 0x60, 0x23, 17),
    "DMT Trade Eyedrops": lambda emu, st: _adult_trade(emu, st, 0x60, 0x26, 20),
    "DMT Cow Grotto Cow": lambda emu, st: _cow(emu, st, 0x3E, 0x18),
    "GC Darunias Joy": lambda emu, st: _event(emu, 0x3, 0x6),
    "GC Rolling Goron as Child": lambda emu, st: _inf(emu, 0x22, 0x6),
    "GC Rolling Goron as Adult": lambda emu, st: _inf(emu, 0x20, 0x1),
    "GC Medigoron": lambda emu, st: _medigoron(emu, st, 0x62, 0x1),
    "DMC Great Fairy Reward": lambda emu, st: _fairy(emu, st, 0x3B, 0x10) or _check_temp_context(st, 0xFF, 0x05, 0x14),
    "ZR Magic Bean Salesman": lambda emu, st: _bean(emu, st, 0x54, 0x1),
    "ZR Frogs in the Rain": lambda emu, st: _event(emu, 0xD, 0x6),
    "ZR Frogs Ocarina Game": lambda emu, st: _event(emu, 0xD, 0x0),
    "ZR Frogs Zeldas Lullaby": lambda emu, st: _event(emu, 0xD, 0x1),
    "ZR Frogs Eponas Song": lambda emu, st: _event(emu, 0xD, 0x2),
    "ZR Frogs Suns Song": lambda emu, st: _event(emu, 0xD, 0x3),
    "ZR Frogs Sarias Song": lambda emu, st: _event(emu, 0xD, 0x4),
    "ZR Frogs Song of Time": lambda emu, st: _event(emu, 0xD, 0x5),
    "ZD Diving Minigame": lambda emu, st: _event(emu, 0x3, 0x8),
    "ZD King Zora Thawed": lambda emu, st: _inf(emu, 0x26, 0x1),
    "ZD Trade Prescription": lambda emu, st: _adult_trade(emu, st, 0x58, 0x24, 18),
    "ZF Great Fairy Reward": lambda emu, st: _igi(emu, 0x2, 0x0),
    "Jabu Jabus Belly MQ Cow": lambda emu, st: _cow(emu, st, 0x02, 0x18),
    "LH Underwater Item": lambda emu, st: _event(emu, 0x3, 0x1),
    "LH Child Fishing": lambda emu, st: _fishing(emu, False),
    "LH Adult Fishing": lambda emu, st: _fishing(emu, True),
    "LH Loach Fishing": lambda emu, st: _loach_fishing(emu),
    "LH Lab Dive": lambda emu, st: _igi(emu, 0x3, 0x0),
    "LH Trade Eyeball Frog": lambda emu, st: _adult_trade(emu, st, 0x38, 0x25, 19),
    "LH Sun": lambda emu, st: _fire_arrows(emu, st, 0x57, 0x0),
    "GV Trade Poachers Saw": lambda emu, st: _adult_trade(emu, st, 0x5A, 0x22, 16),
    "GV Cow": lambda emu, st: _cow(emu, st, 0x5A, 0x18),
    "Hideout Gerudo Membership Card": lambda emu, st: _membership(emu),
    "GF HBA 1000 Points": lambda emu, st: _inf(emu, 0x33, 0x0),
    "GF HBA 1500 Points": lambda emu, st: _igi(emu, 0x0, 0x7),
    "Wasteland Bombchu Salesman": lambda emu, st: _salesman(emu, st, 0x5E, 0x1),
    "Colossus Great Fairy Reward": lambda emu, st: _igi(emu, 0x2, 0x2),
    "OGC Great Fairy Reward": lambda emu, st: _fairy(emu, st, 0x3B, 0x8),
    "Song from Impa": lambda emu, st: _event(emu, 0x5, 0x9),
    "Song from Malon": lambda emu, st: _event(emu, 0x5, 0x8),
    "Song from Saria": lambda emu, st: _event(emu, 0x5, 0x7),
    "Song from Royal Familys Tomb": lambda emu, st: _event(emu, 0x5, 0xA),
    "Song from Ocarina of Time": lambda emu, st: _event(emu, 0xA, 0x9),
    "Song from Windmill": lambda emu, st: _event(emu, 0x5, 0xB),
    "Sheik in Forest": lambda emu, st: _event(emu, 0x5, 0x0),
    "Sheik in Crater": lambda emu, st: _event(emu, 0x5, 0x1),
    "Sheik in Ice Cavern": lambda emu, st: _event(emu, 0x5, 0x2),
    "Sheik at Colossus": lambda emu, st: _event(emu, 0xA, 0xC),
    "Sheik in Kakariko": lambda emu, st: _event(emu, 0x5, 0x4),
    "Sheik at Temple": lambda emu, st: _event(emu, 0x5, 0x5),
}

SPECIAL_LOCATION_TAGS: Dict[str, Tuple[str, ...]] = {
    name: _as_tags(location_table[name][5])
    for name in SPECIAL_LOCATION_CHECKS
    if name in location_table
}


SPECIAL_LOCATION_OVERRIDE_KEYS: Dict[str, Tuple[str, ...]] = {
    "LW Trade Cojiro": (_override_key(0x5B, 0x00, 0x1F),),
    "LW Trade Odd Potion": (_override_key(0x5B, 0x00, 0x21),),
    "Gift from Sages": (_override_key(0xFF, 0x05, 0x03),),
    "Market Treasure Chest Game Salesman": (_override_key(0x10, 0x00, 0x71),),
    "Market Treasure Chest Game Reward": (_override_key(0x10, 0x01, 0x0A),),
    "ToT Reward from Rauru": (_override_key(0xFF, 0x05, 0x04),),
    "Kak Anju Trade Pocket Cucco": (_override_key(0x52, 0x00, 0x0E),),
    "Kak Granny Trade Odd Mushroom": (_override_key(0x4E, 0x00, 0x20),),
    "Kak Granny Buy Blue Potion": (_override_key(0x4E, 0x00, 0x12),),
    "Kak 100 Gold Skulltula Reward": (_override_key(0x50, 0x00, 0x56),),
    "DMT Great Fairy Reward": (
        _override_key(0x3B, 0x05, 0x18),
        _override_key(0xFF, 0x05, 0x13),
    ),
    "DMT Biggoron": (_override_key(0x60, 0x00, 0x57),),
    "DMT Trade Broken Sword": (_override_key(0x60, 0x00, 0x23),),
    "DMT Trade Eyedrops": (_override_key(0x60, 0x00, 0x26),),
    "DMC Great Fairy Reward": (
        _override_key(0x3B, 0x05, 0x10),
        _override_key(0xFF, 0x05, 0x14),
    ),
    "ZR Magic Bean Salesman": (_override_key(0x54, 0x00, 0x16),),
    "ZD Trade Prescription": (_override_key(0x58, 0x00, 0x24),),
    "LH Sun": (_override_key(0x57, 0x00, 0x58),),
    "LH Trade Eyeball Frog": (_override_key(0x38, 0x00, 0x25),),
    "GV Trade Poachers Saw": (_override_key(0x5A, 0x00, 0x22),),
    "Wasteland Bombchu Salesman": (_override_key(0x5E, 0x00, 0x03),),
}


def _generic_override_keys(kind: str, args: Tuple[int, ...]) -> Tuple[str, ...]:
    if kind == "chest":
        return (_override_key(args[0], 0x01, args[1]),)
    if kind == "ground":
        return (_override_key(args[0], 0x02, args[1]),)
    if kind == "mask_shop":
        return (_override_key(args[0], 0x00, args[1]),)
    if kind == "boss":
        return (_override_key(0xFF, 0x05, args[0]),)
    if kind == "boss_heart":
        return (
            _override_key(args[0], 0x02, 0x1F),
            _override_key(args[0], 0x00, 0x4F),
            _override_key(0xFF, 0x05, args[1]),
        )
    return ()


def _build_override_key_location_index() -> Dict[str, Tuple[str, ...]]:
    index: Dict[str, List[str]] = {}

    for name, kind, args, _tags in GENERIC_LOCATION_RULES:
        for key in _generic_override_keys(kind, args):
            index.setdefault(key, []).append(name)

    for name, keys in SPECIAL_LOCATION_OVERRIDE_KEYS.items():
        for key in keys:
            index.setdefault(key, []).append(name)

    return {key: tuple(names) for key, names in index.items()}


OVERRIDE_KEY_LOCATION_INDEX = _build_override_key_location_index()
CACHED_LOCATION_NAMES = {
    name
    for names in OVERRIDE_KEY_LOCATION_INDEX.values()
    for name in names
}


def _apply_outgoing_key_to_cache(st: OoTBridgeState, key: str) -> None:
    if st.location_cache is None:
        st.location_cache_dirty = True
        return

    names = OVERRIDE_KEY_LOCATION_INDEX.get(key)
    if not names:
        st.location_cache_dirty = True
        return

    updated = False
    for name in names:
        if name in st.location_cache:
            st.location_cache[name] = True
            updated = True

    if not updated:
        st.location_cache_dirty = True


def _check_generic_location(emu: EmuLoaderClient, st: OoTBridgeState, name: str, kind: str, args: Tuple[int, ...]) -> bool:
    if kind == "chest":
        return _chest(emu, st, args[0], args[1])
    if kind == "ground":
        return _ground(emu, st, args[0], args[1])
    if kind == "skulltula":
        return _skulltula(emu, args[0], args[1])
    if kind == "shop":
        return _shop(emu, args[0], args[1])
    if kind == "mask_shop":
        return _shop_location(emu, st, name, args[0], args[1])
    if kind == "boss":
        return _boss_reward(st, args[0])
    if kind == "boss_heart":
        return _boss_heart(emu, st, args[0], args[1])
    if kind == "scrub":
        return SCRUB_FALLBACK_CHECKS.get(name, lambda _emu, _st: False)(emu, st) or _scrub(emu, args[0], args[1])
    raise NotImplementedError(f"Unhandled generic location rule: {kind}")


def _check_generic_locations(emu: EmuLoaderClient, st: OoTBridgeState, cached: Optional[bool] = None) -> dict:
    active_cache: Dict[Tuple[str, ...], bool] = {}
    out: dict = {}
    for name, kind, args, tags in GENERIC_LOCATION_RULES:
        is_cached = name in CACHED_LOCATION_NAMES
        if cached is not None and cached != is_cached:
            continue
        if tags not in active_cache:
            active_cache[tags] = _active_location_variant(emu, st, tags)
        if active_cache[tags]:
            out[name] = _check_generic_location(emu, st, name, kind, args)
    return out


def _check_special_locations(emu: EmuLoaderClient, st: OoTBridgeState, cached: Optional[bool] = None) -> dict:
    active_cache: Dict[Tuple[str, ...], bool] = {}
    out: dict = {}
    for name, check in SPECIAL_LOCATION_CHECKS.items():
        is_cached = name in CACHED_LOCATION_NAMES
        if cached is not None and cached != is_cached:
            continue
        tags = SPECIAL_LOCATION_TAGS.get(name, ())
        if tags not in active_cache:
            active_cache[tags] = _active_location_variant(emu, st, tags)
        if active_cache[tags]:
            out[name] = check(emu, st)
    return out


def _check_all_locations(emu: EmuLoaderClient, st: OoTBridgeState) -> dict:
    out: dict = _check_generic_locations(emu, st)
    out.update(_check_special_locations(emu, st))
    return out


def _cached_location_is_checked(st: OoTBridgeState, name: str, force_resync: bool) -> bool:
    return not force_resync and st.location_cache is not None and st.location_cache.get(name) is True


def _check_cached_generic_locations(emu: EmuLoaderClient, st: OoTBridgeState, force_resync: bool) -> dict:
    active_cache: Dict[Tuple[str, ...], bool] = {}
    out: dict = {}
    for name, kind, args, tags in GENERIC_LOCATION_RULES:
        if name not in CACHED_LOCATION_NAMES:
            continue
        if tags not in active_cache:
            active_cache[tags] = _active_location_variant(emu, st, tags)
        if not active_cache[tags]:
            continue
        if _cached_location_is_checked(st, name, force_resync):
            out[name] = True
        else:
            out[name] = _check_generic_location(emu, st, name, kind, args)
    return out


def _check_cached_special_locations(emu: EmuLoaderClient, st: OoTBridgeState, force_resync: bool) -> dict:
    active_cache: Dict[Tuple[str, ...], bool] = {}
    out: dict = {}
    for name, check in SPECIAL_LOCATION_CHECKS.items():
        if name not in CACHED_LOCATION_NAMES:
            continue
        tags = SPECIAL_LOCATION_TAGS.get(name, ())
        if tags not in active_cache:
            active_cache[tags] = _active_location_variant(emu, st, tags)
        if not active_cache[tags]:
            continue
        if _cached_location_is_checked(st, name, force_resync):
            out[name] = True
        else:
            out[name] = check(emu, st)
    return out


def _check_cached_locations(emu: EmuLoaderClient, st: OoTBridgeState, force_resync: bool) -> dict:
    out: dict = _check_cached_generic_locations(emu, st, force_resync)
    out.update(_check_cached_special_locations(emu, st, force_resync))
    return out


def _check_uncached_locations(emu: EmuLoaderClient, st: OoTBridgeState) -> dict:
    out: dict = _check_generic_locations(emu, st, cached=False)
    out.update(_check_special_locations(emu, st, cached=False))
    return out


def _check_collectibles(emu: EmuLoaderClient, st: OoTBridgeState) -> dict:
    result: dict = {}
    if st.collectible_overrides is None or not st.collectible_offsets:
        return result
    byte_cache: Dict[int, int] = {}
    for id_str, data in st.collectible_offsets.items():
        byte_addr = st.collectible_overrides + data[0] + (data[1] >> 3)
        if byte_addr not in byte_cache:
            byte_cache[byte_addr] = emu.read_u8(byte_addr)
        mem = byte_cache[byte_addr]
        result[id_str] = bool(mem & (1 << (7 - (data[1] % 8))))
    return result


def _build_state(
    emu: EmuLoaderClient,
    st: OoTBridgeState,
    include_full_state: bool,
    force_resync: bool,
) -> dict:
    batch_owner = getattr(emu.emulator_info, "begin_batch", None)
    batch_done = getattr(emu.emulator_info, "end_batch", None)
    if batch_owner and batch_done:
        batch_owner()
    try:
        return _build_state_uncached(emu, st, include_full_state, force_resync)
    finally:
        if batch_done:
            batch_done()


def _check_locations_with_cache(emu: EmuLoaderClient, st: OoTBridgeState, force_resync: bool) -> dict:
    resync_cached = st.location_cache_dirty or force_resync
    if st.location_cache is None:
        st.location_cache = {}
        resync_cached = True

    checked_cacheable = _check_cached_locations(emu, st, resync_cached)
    st.location_cache.update(checked_cacheable)
    st.location_cache_dirty = False

    locations = dict(checked_cacheable)
    locations.update(_check_uncached_locations(emu, st))
    return locations


def _build_state_uncached(
    emu: EmuLoaderClient,
    st: OoTBridgeState,
    include_full_state: bool,
    force_resync: bool,
) -> dict:
    payload: dict = {
        "playerName":    _get_player_name(emu),
        "scriptVersion": SCRIPT_VERSION,
        "deathlinkActive": _deathlink_enabled(emu),
    }
    if include_full_state and _in_safe_state(emu) and st.mq_table_address is not None:
        payload["locations"]   = _check_locations_with_cache(emu, st, force_resync)
        payload["collectibles"]= _check_collectibles(emu, st)
        payload["isDead"]      = _get_death_state(emu)
        payload["gameComplete"]= _is_game_complete(emu, st)
    return payload


def _process_block(emu: EmuLoaderClient, st: OoTBridgeState, block: dict) -> None:
    if not block:
        return

    # Write player names on first connect or while in menu/logo/file-select modes.
    cur_mode = _get_current_game_mode(emu)
    if (st.first_connect or cur_mode in (0, 1, 2)) and block.get("playerNames"):
        st.first_connect = False
        st.player_names_initialized = True
        _resolve_mq_table(emu, st)
        for idx, name in enumerate(block["playerNames"][:254], start=1):
            _set_player_name(emu, idx, name)
        _set_player_name(emu, 255, "a player")

    if block.get("triggerDeath"):
        _kill_link(emu)

    # Item queue: write the next undelivered item if the game is ready.
    st.item_queue = block.get("items", [])
    received = emu.read_u16(INTERNAL_COUNT_ADDR)
    if received < len(st.item_queue) and _item_receivable(emu):
        pid = emu.read_u8(PLAYER_ID_ADDR)
        emu.write_u16(INCOMING_PLAYER_ADDR, pid)
        emu.write_u16(INCOMING_ITEM_ADDR, st.item_queue[received])
        
    # Collectible override pointer (resolved once from a rando-context pointer).
    co = block.get("collectibleOverrides", 0)
    if st.collectible_overrides is None and co:
        ptr = emu.read_u32(0x400000 + co)
        if 0x80000000 <= ptr < 0x80800000:
            st.collectible_overrides = ptr - 0x80000000

    new_offsets = block.get("collectibleOffsets")
    if new_offsets != st.collectible_offsets:
        st.collectible_offsets = new_offsets

    new_shop_offsets = block.get("shopFlagOffsets", {})
    if new_shop_offsets != st.shop_flag_offsets:
        st.shop_flag_offsets = new_shop_offsets
        st.location_cache_dirty = True


async def _protocol_cycle(
    reader: asyncio.StreamReader,
    writer: asyncio.StreamWriter,
    emu: EmuLoaderClient,
    st: OoTBridgeState,
    include_full_state: bool,
    force_resync: bool,
) -> None:
    """One receive-then-send exchange with the AP client."""
    try:
        raw = await asyncio.wait_for(reader.readline(), timeout=0.1)
    except asyncio.TimeoutError:
        return
    if not raw:
        raise ConnectionError("client disconnected")
    try:
        block = json.loads(raw.decode().strip())
        _process_block(emu, st, block)
    except json.JSONDecodeError:
        logger.warning("OoT Bridge: could not decode client message")

    payload = _build_state(emu, st, include_full_state, force_resync)
    line    = json.dumps(payload) + "\n"
    writer.write(line.encode())
    await writer.drain()


async def _client_session(
    reader: asyncio.StreamReader,
    writer: asyncio.StreamWriter,
    emu: EmuLoaderClient,
    st: OoTBridgeState,
    ctx,
) -> None:
    st.reset_connection()
    loop  = asyncio.get_event_loop()
    frame = 0

    try:
        while not ctx.exit_event.is_set() and not reader.at_eof():
            frame += 1

            # Ensure emulator is attached.
            if not emu.is_connected():
                try:
                    ok = await loop.run_in_executor(None, emu.connect)
                    if ok:
                        logger.info(
                            f"OoT Bridge: attached to "
                            f"{emu.emulator_info.readable_emulator_name}"  # type: ignore[union-attr]
                        )
                    else:
                        break
                except Exception as exc:
                    logger.warning(f"OoT Bridge: emulator attach failed: {exc}")
                    break

            # The ROM keeps OUTGOING_KEY set until the bridge clears it, so
            # polling at ~10 Hz is enough and avoids saturating RetroArch UDP.
            if frame % OUTGOING_KEY_POLL_FRAMES == 0:
                try:
                    _poll_outgoing_key(emu, st)
                except Exception as exc:
                    logger.debug(f"OoT Bridge: outgoing-key read failed: {exc}")
                    emu.disconnect()
                    break

            # Exchange often enough for incoming items to feel responsive, but
            # only include the expensive full location state on the old cadence.
            if frame % PROTOCOL_EXCHANGE_FRAMES == 0:
                try:
                    await _protocol_cycle(
                        reader, writer, emu, st,
                        include_full_state=(frame % FULL_STATE_FRAMES == 0),
                        force_resync=(frame % CACHE_RESYNC_FRAMES == 0),
                    )
                except ConnectionError as exc:
                    logger.info(f"OoT Bridge: client disconnected ({exc})")
                    break
                except Exception as exc:
                    logger.warning(f"OoT Bridge: cycle error: {exc}")
                    emu.disconnect()
                    break

            await asyncio.sleep(1 / 60)
    finally:
        try:
            writer.close()
            await writer.wait_closed()
        except Exception:
            pass


async def n64_bridge_task(ctx) -> None:
    """Launch the TCP bridge server and serve one AP client at a time."""
    emu   = EmuLoaderClient()
    st    = OoTBridgeState()
    lock  = asyncio.Lock()

    async def _on_connect(
        reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        if lock.locked():
            logger.warning("OoT Bridge: rejecting second client (already connected)")
            writer.close()
            return
        async with lock:
            await _client_session(reader, writer, emu, st, ctx)

    try:
        server = await asyncio.start_server(_on_connect, "127.0.0.1", CONNECT_PORT)
    except OSError as exc:
        logger.error(f"OoT Bridge: cannot bind :28921 – {exc}")
        return

    logger.info(f"OoT Bridge: listening on 127.0.0.1:{CONNECT_PORT}")
    async with server:
        while not ctx.exit_event.is_set():
            await asyncio.sleep(1)

    emu.disconnect()
