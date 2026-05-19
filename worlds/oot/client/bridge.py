"""
OoT AP bridge: attaches to N64 emulator memory, serves connector protocol on :28921.
"""

import asyncio
import json
from typing import Dict, List, Optional, Set

try:
    from CommonClient import logger
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

from .emu_loader import EmuLoaderClient
from ..Utils import OOT_PLAYER_NAME_LENGTH, encode_oot_player_name

SCRIPT_VERSION = 7
CONNECT_PORT   = 28921
OUTGOING_KEY_POLL_FRAMES = 6
PROTOCOL_EXCHANGE_FRAMES = 10
FULL_STATE_FRAMES = 30

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

    def reset_connection(self) -> None:
        self.temp_context_history = set()
        self.first_connect        = True


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


def _poll_outgoing_key(emu: EmuLoaderClient, state: OoTBridgeState) -> None:
    high = emu.read_u32(OUTGOING_KEY_ADDR)
    low  = emu.read_u32(OUTGOING_KEY_ADDR + 4)
    if high == 0 and low == 0:
        return
    scene    = emu.read_u8(OUTGOING_KEY_ADDR + 0)
    loc_type = emu.read_u8(OUTGOING_KEY_ADDR + 1)
    flag     = emu.read_u8(OUTGOING_KEY_ADDR + 7)  # flag LSB = bit index
    state.temp_context_history.add(
        f"{scene % 0x100:02X}:{loc_type % 0x100:02X}:{flag % 0x100:02X}"
    )
    emu.write_u32(OUTGOING_KEY_ADDR,     0)
    emu.write_u32(OUTGOING_KEY_ADDR + 4, 0)


def _check_temp_context(state: OoTBridgeState, scene: int, loc_type: int, flag: int) -> bool:
    return (
        f"{scene % 0x100:02X}:{loc_type % 0x100:02X}:{flag % 0x100:02X}"
        in state.temp_context_history
    )


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


def _bgs(emu: EmuLoaderClient) -> bool:
    return bool(emu.read_u32(EQUIPMENT_ADDR) & (1 << 0x8))


def _membership(emu: EmuLoaderClient) -> bool:
    return _event(emu, 0x9, 0) and _event(emu, 0x9, 1) and _event(emu, 0x9, 2) and _event(emu, 0x9, 3)


def _kokiri_forest(emu: EmuLoaderClient, st: OoTBridgeState) -> dict:
    c = _chest; g = _ground; sk = _skulltula; sh = _shop; cw = _cow
    return {
        "KF Midos Top Left Chest":    c(emu, st, 0x28, 0x00),
        "KF Midos Top Right Chest":   c(emu, st, 0x28, 0x01),
        "KF Midos Bottom Left Chest": c(emu, st, 0x28, 0x02),
        "KF Midos Bottom Right Chest":c(emu, st, 0x28, 0x03),
        "KF Kokiri Sword Chest":      c(emu, st, 0x55, 0x00),
        "KF Storms Grotto Chest":     c(emu, st, 0x3E, 0x0C),
        "KF Links House Cow":         cw(emu, st, 0x34, 0x18),
        "KF GS Know It All House":    sk(emu, 0x0C, 0x1),
        "KF GS Bean Patch":           sk(emu, 0x0C, 0x0),
        "KF GS House of Twins":       sk(emu, 0x0C, 0x2),
        "KF Shop Item 5":             sh(emu, 0x6, 0x0),
        "KF Shop Item 6":             sh(emu, 0x6, 0x1),
        "KF Shop Item 7":             sh(emu, 0x6, 0x2),
        "KF Shop Item 8":             sh(emu, 0x6, 0x3),
        "KF Shop Blue Rupee":         g(emu, st, 0x2D, 0x1),
    }


def _lost_woods(emu: EmuLoaderClient, st: OoTBridgeState) -> dict:
    lw_near_bridge = _inf(emu, 0x33, 0x2) or _scrub(emu, 0x5B, 0xA)
    lw_grotto_front = _inf(emu, 0x33, 0x3) or _scrub(emu, 0x1F, 0xB)
    return {
        "LW Gift from Saria":                _event(emu, 0xC, 0x1),
        "LW Ocarina Memory Game":            _igi(emu, 0x3, 0x7),
        "LW Target in Woods":                _igi(emu, 0x2, 0x5),
        "LW Near Shortcuts Grotto Chest":    _chest(emu, st, 0x3E, 0x14),
        "Deku Theater Skull Mask":           _igi(emu, 0x2, 0x6),
        "Deku Theater Mask of Truth":        _igi(emu, 0x2, 0x7),
        "LW Skull Kid":                      _igi(emu, 0x3, 0x6),
        "LW Deku Scrub Near Bridge":         lw_near_bridge,
        "LW Deku Scrub Grotto Front":        lw_grotto_front,
        "LW Deku Scrub Near Deku Theater Left":  _scrub(emu, 0x5B, 0x2),
        "LW Deku Scrub Near Deku Theater Right": _scrub(emu, 0x5B, 0x1),
        "LW Deku Scrub Grotto Rear":         _scrub(emu, 0x1F, 0x4),
        "LW GS Bean Patch Near Bridge":      _skulltula(emu, 0x0D, 0x0),
        "LW GS Bean Patch Near Theater":     _skulltula(emu, 0x0D, 0x1),
        "LW GS Above Theater":               _skulltula(emu, 0x0D, 0x2),
    }


def _sacred_forest_meadow(emu: EmuLoaderClient, st: OoTBridgeState) -> dict:
    return {
        "SFM Wolfos Grotto Chest":    _chest(emu, st, 0x3E, 0x11),
        "SFM Deku Scrub Grotto Front":_scrub(emu, 0x18, 0x9),
        "SFM Deku Scrub Grotto Rear": _scrub(emu, 0x18, 0x8),
        "SFM GS":                     _skulltula(emu, 0x0D, 0x3),
    }


def _deku_tree(emu: EmuLoaderClient, st: OoTBridgeState) -> dict:
    checks = {}
    if not _is_mq(emu, st, 0x0):
        checks.update({
            "Deku Tree Map Chest":               _chest(emu, st, 0x00, 0x3),
            "Deku Tree Slingshot Room Side Chest":_chest(emu, st, 0x00, 0x5),
            "Deku Tree Slingshot Chest":          _chest(emu, st, 0x00, 0x1),
            "Deku Tree Compass Chest":            _chest(emu, st, 0x00, 0x2),
            "Deku Tree Compass Room Side Chest":  _chest(emu, st, 0x00, 0x6),
            "Deku Tree Basement Chest":           _chest(emu, st, 0x00, 0x4),
            "Deku Tree GS Compass Room":          _skulltula(emu, 0x0, 0x3),
            "Deku Tree GS Basement Vines":        _skulltula(emu, 0x0, 0x2),
            "Deku Tree GS Basement Gate":         _skulltula(emu, 0x0, 0x1),
            "Deku Tree GS Basement Back Room":    _skulltula(emu, 0x0, 0x0),
        })
    else:
        checks.update({
            "Deku Tree MQ Map Chest":                    _chest(emu, st, 0x00, 0x3),
            "Deku Tree MQ Slingshot Chest":              _chest(emu, st, 0x00, 0x6),
            "Deku Tree MQ Slingshot Room Back Chest":    _chest(emu, st, 0x00, 0x2),
            "Deku Tree MQ Compass Chest":                _chest(emu, st, 0x00, 0x1),
            "Deku Tree MQ Basement Chest":               _chest(emu, st, 0x00, 0x4),
            "Deku Tree MQ Before Spinning Log Chest":    _chest(emu, st, 0x00, 0x5),
            "Deku Tree MQ After Spinning Log Chest":     _chest(emu, st, 0x00, 0x0),
            "Deku Tree MQ Deku Scrub":                   _scrub(emu, 0x00, 0x5),
            "Deku Tree MQ GS Lobby":                     _skulltula(emu, 0x0, 0x1),
            "Deku Tree MQ GS Compass Room":              _skulltula(emu, 0x0, 0x3),
            "Deku Tree MQ GS Basement Graves Room":      _skulltula(emu, 0x0, 0x2),
            "Deku Tree MQ GS Basement Back Room":        _skulltula(emu, 0x0, 0x0),
        })
    checks["Deku Tree Queen Gohma Heart"] = _boss_heart(emu, st, 0x11, 0x05)
    checks["Queen Gohma"]                 = _boss_reward(st, 0x05)
    return checks


def _forest_temple(emu: EmuLoaderClient, st: OoTBridgeState) -> dict:
    checks = {}
    if not _is_mq(emu, st, 0x3):
        checks.update({
            "Forest Temple First Room Chest":              _chest(emu, st, 0x3, 0x3),
            "Forest Temple First Stalfos Chest":           _chest(emu, st, 0x3, 0x0),
            "Forest Temple Raised Island Courtyard Chest": _chest(emu, st, 0x3, 0x5),
            "Forest Temple Map Chest":                     _chest(emu, st, 0x3, 0x1),
            "Forest Temple Well Chest":                    _chest(emu, st, 0x3, 0x9),
            "Forest Temple Eye Switch Chest":              _chest(emu, st, 0x3, 0x4),
            "Forest Temple Boss Key Chest":                _chest(emu, st, 0x3, 0xE),
            "Forest Temple Floormaster Chest":             _chest(emu, st, 0x3, 0x2),
            "Forest Temple Red Poe Chest":                 _chest(emu, st, 0x3, 0xD),
            "Forest Temple Bow Chest":                     _chest(emu, st, 0x3, 0xC),
            "Forest Temple Blue Poe Chest":                _chest(emu, st, 0x3, 0xF),
            "Forest Temple Falling Ceiling Room Chest":    _chest(emu, st, 0x3, 0x7),
            "Forest Temple Basement Chest":                _chest(emu, st, 0x3, 0xB),
            "Forest Temple GS First Room":                 _skulltula(emu, 0x03, 0x1),
            "Forest Temple GS Lobby":                      _skulltula(emu, 0x03, 0x3),
            "Forest Temple GS Raised Island Courtyard":    _skulltula(emu, 0x03, 0x0),
            "Forest Temple GS Level Island Courtyard":     _skulltula(emu, 0x03, 0x2),
            "Forest Temple GS Basement":                   _skulltula(emu, 0x03, 0x4),
        })
    else:
        checks.update({
            "Forest Temple MQ First Room Chest":                      _chest(emu, st, 0x3, 0x3),
            "Forest Temple MQ Wolfos Chest":                          _chest(emu, st, 0x3, 0x0),
            "Forest Temple MQ Well Chest":                            _chest(emu, st, 0x3, 0x9),
            "Forest Temple MQ Raised Island Courtyard Lower Chest":   _chest(emu, st, 0x3, 0x1),
            "Forest Temple MQ Raised Island Courtyard Upper Chest":   _chest(emu, st, 0x3, 0x5),
            "Forest Temple MQ Boss Key Chest":                        _chest(emu, st, 0x3, 0xE),
            "Forest Temple MQ Redead Chest":                          _chest(emu, st, 0x3, 0x2),
            "Forest Temple MQ Map Chest":                             _chest(emu, st, 0x3, 0xD),
            "Forest Temple MQ Bow Chest":                             _chest(emu, st, 0x3, 0xC),
            "Forest Temple MQ Compass Chest":                         _chest(emu, st, 0x3, 0xF),
            "Forest Temple MQ Falling Ceiling Room Chest":            _chest(emu, st, 0x3, 0x6),
            "Forest Temple MQ Basement Chest":                        _chest(emu, st, 0x3, 0xB),
            "Forest Temple MQ GS First Hallway":                      _skulltula(emu, 0x3, 0x1),
            "Forest Temple MQ GS Raised Island Courtyard":            _skulltula(emu, 0x3, 0x0),
            "Forest Temple MQ GS Level Island Courtyard":             _skulltula(emu, 0x3, 0x2),
            "Forest Temple MQ GS Well":                               _skulltula(emu, 0x3, 0x3),
            "Forest Temple MQ GS Block Push Room":                    _skulltula(emu, 0x3, 0x4),
        })
    checks["Forest Temple Phantom Ganon Heart"] = _boss_heart(emu, st, 0x14, 0x08)
    checks["Phantom Ganon"]                     = _boss_reward(st, 0x08)
    return checks


def _hyrule_field(emu: EmuLoaderClient, st: OoTBridgeState) -> dict:
    hf_scrub = _igi(emu, 0x0, 0x3) or _scrub(emu, 0x10, 0x3)
    return {
        "HF Ocarina of Time Item":         _event(emu, 0x4, 0x3),
        "HF Near Market Grotto Chest":     _chest(emu, st, 0x3E, 0x00),
        "HF Tektite Grotto Freestanding PoH": _ground(emu, st, 0x3E, 0x01),
        "HF Southeast Grotto Chest":       _chest(emu, st, 0x3E, 0x02),
        "HF Open Grotto Chest":            _chest(emu, st, 0x3E, 0x03),
        "HF Cow Grotto Cow":               _cow(emu, st, 0x3E, 0x19),
        "HF Deku Scrub Grotto":            hf_scrub,
        "HF GS Cow Grotto":                _skulltula(emu, 0x0A, 0x0),
        "HF GS Near Kak Grotto":           _skulltula(emu, 0x0A, 0x1),
    }


def _lon_lon_ranch(emu: EmuLoaderClient, st: OoTBridgeState) -> dict:
    return {
        "LLR Talons Chickens":       _igi(emu, 0x1, 0x2),
        "LLR Freestanding PoH":      _ground(emu, st, 0x4C, 0x01),
        "LLR Tower Left Cow":        _cow(emu, st, 0x4C, 0x19),
        "LLR Tower Right Cow":       _cow(emu, st, 0x4C, 0x18),
        "LLR Deku Scrub Grotto Left":  _scrub(emu, 0x26, 0x1),
        "LLR Deku Scrub Grotto Center":_scrub(emu, 0x26, 0x4),
        "LLR Deku Scrub Grotto Right": _scrub(emu, 0x26, 0x6),
        "LLR Stables Left Cow":      _cow(emu, st, 0x36, 0x18),
        "LLR Stables Right Cow":     _cow(emu, st, 0x36, 0x19),
        "LLR GS House Window":       _skulltula(emu, 0x0B, 0x2),
        "LLR GS Tree":               _skulltula(emu, 0x0B, 0x3),
        "LLR GS Rain Shed":          _skulltula(emu, 0x0B, 0x1),
        "LLR GS Back Wall":          _skulltula(emu, 0x0B, 0x0),
    }


def _market(emu: EmuLoaderClient, st: OoTBridgeState) -> dict:
    return {
        "Market Shooting Gallery Reward":      _igi(emu, 0x0, 0x5),
        "Market Bombchu Bowling First Prize":  _igi(emu, 0x3, 0x1),
        "Market Bombchu Bowling Second Prize": _igi(emu, 0x3, 0x2),
        "Market Treasure Chest Game Reward":   _igi(emu, 0x2, 0x3),
        "Market Lost Dog":                     _inf(emu, 0x33, 0x1),
        "Market 10 Big Poes":                  _poe_bottle(emu, st),
        "ToT Light Arrows Cutscene":           _event(emu, 0xC, 0x4),
        "ToT Reward from Rauru":               _event(emu, 0x4, 0x5) or _boss_reward(st, 0x04),
        "Market GS Guard House":               _skulltula(emu, 0x0E, 0x3),
        "Market Bazaar Item 5":                _shop(emu, 0x4, 0x0),
        "Market Bazaar Item 6":                _shop(emu, 0x4, 0x1),
        "Market Bazaar Item 7":                _shop(emu, 0x4, 0x2),
        "Market Bazaar Item 8":                _shop(emu, 0x4, 0x3),
        "Market Potion Shop Item 5":           _shop(emu, 0x0, 0x0),
        "Market Potion Shop Item 6":           _shop(emu, 0x0, 0x1),
        "Market Potion Shop Item 7":           _shop(emu, 0x0, 0x2),
        "Market Potion Shop Item 8":           _shop(emu, 0x0, 0x3),
        "Market Bombchu Shop Item 5":          _shop(emu, 0x1, 0x0),
        "Market Bombchu Shop Item 6":          _shop(emu, 0x1, 0x1),
        "Market Bombchu Shop Item 7":          _shop(emu, 0x1, 0x2),
        "Market Bombchu Shop Item 8":          _shop(emu, 0x1, 0x3),
    }


def _hyrule_castle(emu: EmuLoaderClient, st: OoTBridgeState) -> dict:
    return {
        "HC Malon Egg":          _event(emu, 0x1, 0x2),
        "HC Zeldas Letter":      _event(emu, 0x4, 0x0),
        "HC Great Fairy Reward": _igi(emu, 0x2, 0x1),
        "HC GS Tree":            _skulltula(emu, 0xE, 0x2),
        "HC GS Storms Grotto":   _skulltula(emu, 0xE, 0x1),
    }


def _kakariko_village(emu: EmuLoaderClient, st: OoTBridgeState) -> dict:
    return {
        "Kak Anju as Child":                _igi(emu, 0x0, 0x4),
        "Kak Anju as Adult":                _igi(emu, 0x4, 0x4),
        "Kak Impas House Freestanding PoH": _ground(emu, st, 0x37, 0x1),
        "Kak Windmill Freestanding PoH":    _ground(emu, st, 0x48, 0x1),
        "Kak Man on Roof":                  _igi(emu, 0x3, 0x5),
        "Kak Open Grotto Chest":            _chest(emu, st, 0x3E, 0x08),
        "Kak Redead Grotto Chest":          _chest(emu, st, 0x3E, 0x0A),
        "Kak Shooting Gallery Reward":      _igi(emu, 0x0, 0x6),
        "Kak 10 Gold Skulltula Reward":     _event(emu, 0xD, 0xA),
        "Kak 20 Gold Skulltula Reward":     _event(emu, 0xD, 0xB),
        "Kak 30 Gold Skulltula Reward":     _event(emu, 0xD, 0xC),
        "Kak 40 Gold Skulltula Reward":     _event(emu, 0xD, 0xD),
        "Kak 50 Gold Skulltula Reward":     _event(emu, 0xD, 0xE),
        "Kak Impas House Cow":              _cow(emu, st, 0x37, 0x18),
        "Kak GS Tree":                      _skulltula(emu, 0x10, 0x5),
        "Kak GS Near Gate Guard":           _skulltula(emu, 0x10, 0x1),
        "Kak GS Watchtower":                _skulltula(emu, 0x10, 0x2),
        "Kak GS Skulltula House":           _skulltula(emu, 0x10, 0x4),
        "Kak GS House Under Construction":  _skulltula(emu, 0x10, 0x3),
        "Kak GS Above Impas House":         _skulltula(emu, 0x10, 0x6),
        "Kak Bazaar Item 5":                _shop(emu, 0x7, 0x0),
        "Kak Bazaar Item 6":                _shop(emu, 0x7, 0x1),
        "Kak Bazaar Item 7":                _shop(emu, 0x7, 0x2),
        "Kak Bazaar Item 8":                _shop(emu, 0x7, 0x3),
        "Kak Potion Shop Item 5":           _shop(emu, 0x3, 0x0),
        "Kak Potion Shop Item 6":           _shop(emu, 0x3, 0x1),
        "Kak Potion Shop Item 7":           _shop(emu, 0x3, 0x2),
        "Kak Potion Shop Item 8":           _shop(emu, 0x3, 0x3),
    }


def _graveyard(emu: EmuLoaderClient, st: OoTBridgeState) -> dict:
    return {
        "Graveyard Shield Grave Chest":         _chest(emu, st, 0x40, 0x00),
        "Graveyard Heart Piece Grave Chest":    _chest(emu, st, 0x3F, 0x00),
        "Graveyard Royal Familys Tomb Chest":   _chest(emu, st, 0x41, 0x00),
        "Graveyard Freestanding PoH":           _ground(emu, st, 0x53, 0x4),
        "Graveyard Dampe Gravedigging Tour":    _ground(emu, st, 0x53, 0x8),
        "Graveyard Dampe Race Hookshot Chest":  _chest(emu, st, 0x48, 0x00),
        "Graveyard Dampe Race Freestanding PoH":_ground(emu, st, 0x48, 0x7),
        "Graveyard GS Bean Patch":              _skulltula(emu, 0x10, 0x0),
        "Graveyard GS Wall":                    _skulltula(emu, 0x10, 0x7),
    }


def _bottom_of_well(emu: EmuLoaderClient, st: OoTBridgeState) -> dict:
    checks = {}
    if not _is_mq(emu, st, 0x8):
        checks.update({
            "Bottom of the Well Front Left Fake Wall Chest":   _chest(emu, st, 0x08, 0x08),
            "Bottom of the Well Front Center Bombable Chest":  _chest(emu, st, 0x08, 0x02),
            "Bottom of the Well Back Left Bombable Chest":     _chest(emu, st, 0x08, 0x04),
            "Bottom of the Well Underwater Left Chest":        _chest(emu, st, 0x08, 0x09),
            "Bottom of the Well Freestanding Key":             _ground(emu, st, 0x08, 0x01),
            "Bottom of the Well Compass Chest":                _chest(emu, st, 0x08, 0x01),
            "Bottom of the Well Center Skulltula Chest":       _chest(emu, st, 0x08, 0x0E),
            "Bottom of the Well Right Bottom Fake Wall Chest": _chest(emu, st, 0x08, 0x05),
            "Bottom of the Well Fire Keese Chest":             _chest(emu, st, 0x08, 0x0A),
            "Bottom of the Well Like Like Chest":              _chest(emu, st, 0x08, 0x0C),
            "Bottom of the Well Map Chest":                    _chest(emu, st, 0x08, 0x07),
            "Bottom of the Well Underwater Front Chest":       _chest(emu, st, 0x08, 0x10),
            "Bottom of the Well Invisible Chest":              _chest(emu, st, 0x08, 0x14),
            "Bottom of the Well Lens of Truth Chest":          _chest(emu, st, 0x08, 0x03),
            "Bottom of the Well GS West Inner Room":           _skulltula(emu, 0x08, 0x2),
            "Bottom of the Well GS East Inner Room":           _skulltula(emu, 0x08, 0x1),
            "Bottom of the Well GS Like Like Cage":            _skulltula(emu, 0x08, 0x0),
        })
    else:
        checks.update({
            "Bottom of the Well MQ Map Chest":                    _chest(emu, st, 0x8, 0x3),
            "Bottom of the Well MQ East Inner Room Freestanding Key": _ground(emu, st, 0x8, 0x1),
            "Bottom of the Well MQ Compass Chest":                _chest(emu, st, 0x8, 0x2),
            "Bottom of the Well MQ Dead Hand Freestanding Key":   _ground(emu, st, 0x8, 0x2),
            "Bottom of the Well MQ Lens of Truth Chest":          _chest(emu, st, 0x8, 0x1),
            "Bottom of the Well MQ GS Coffin Room":               _skulltula(emu, 0x08, 0x2),
            "Bottom of the Well MQ GS West Inner Room":           _skulltula(emu, 0x08, 0x1),
            "Bottom of the Well MQ GS Basement":                  _skulltula(emu, 0x08, 0x0),
        })
    return checks


def _shadow_temple(emu: EmuLoaderClient, st: OoTBridgeState) -> dict:
    checks = {}
    if not _is_mq(emu, st, 0x7):
        checks.update({
            "Shadow Temple Map Chest":                    _chest(emu, st, 0x07, 0x01),
            "Shadow Temple Hover Boots Chest":            _chest(emu, st, 0x07, 0x07),
            "Shadow Temple Compass Chest":                _chest(emu, st, 0x07, 0x03),
            "Shadow Temple Early Silver Rupee Chest":     _chest(emu, st, 0x07, 0x02),
            "Shadow Temple Invisible Blades Visible Chest":  _chest(emu, st, 0x07, 0x0C),
            "Shadow Temple Invisible Blades Invisible Chest":_chest(emu, st, 0x07, 0x16),
            "Shadow Temple Falling Spikes Lower Chest":   _chest(emu, st, 0x07, 0x05),
            "Shadow Temple Falling Spikes Upper Chest":   _chest(emu, st, 0x07, 0x06),
            "Shadow Temple Falling Spikes Switch Chest":  _chest(emu, st, 0x07, 0x04),
            "Shadow Temple Invisible Spikes Chest":       _chest(emu, st, 0x07, 0x09),
            "Shadow Temple Freestanding Key":             _ground(emu, st, 0x07, 0x01),
            "Shadow Temple Wind Hint Chest":              _chest(emu, st, 0x07, 0x15),
            "Shadow Temple After Wind Enemy Chest":       _chest(emu, st, 0x07, 0x08),
            "Shadow Temple After Wind Hidden Chest":      _chest(emu, st, 0x07, 0x14),
            "Shadow Temple Spike Walls Left Chest":       _chest(emu, st, 0x07, 0x0A),
            "Shadow Temple Boss Key Chest":               _chest(emu, st, 0x07, 0x0B),
            "Shadow Temple Invisible Floormaster Chest":  _chest(emu, st, 0x07, 0x0D),
            "Shadow Temple GS Invisible Blades Room":     _skulltula(emu, 0x07, 0x3),
            "Shadow Temple GS Falling Spikes Room":       _skulltula(emu, 0x07, 0x1),
            "Shadow Temple GS Single Giant Pot":          _skulltula(emu, 0x07, 0x0),
            "Shadow Temple GS Near Ship":                 _skulltula(emu, 0x07, 0x4),
            "Shadow Temple GS Triple Giant Pot":          _skulltula(emu, 0x07, 0x2),
        })
    else:
        checks.update({
            "Shadow Temple MQ Early Gibdos Chest":              _chest(emu, st, 0x7, 0x3),
            "Shadow Temple MQ Map Chest":                       _chest(emu, st, 0x7, 0x2),
            "Shadow Temple MQ Near Ship Invisible Chest":       _chest(emu, st, 0x7, 0xE),
            "Shadow Temple MQ Compass Chest":                   _chest(emu, st, 0x7, 0x1),
            "Shadow Temple MQ Hover Boots Chest":               _chest(emu, st, 0x7, 0x7),
            "Shadow Temple MQ Invisible Blades Invisible Chest":_chest(emu, st, 0x7, 0x16),
            "Shadow Temple MQ Invisible Blades Visible Chest":  _chest(emu, st, 0x7, 0xC),
            "Shadow Temple MQ Beamos Silver Rupees Chest":      _chest(emu, st, 0x7, 0xF),
            "Shadow Temple MQ Falling Spikes Lower Chest":      _chest(emu, st, 0x7, 0x5),
            "Shadow Temple MQ Falling Spikes Upper Chest":      _chest(emu, st, 0x7, 0x6),
            "Shadow Temple MQ Falling Spikes Switch Chest":     _chest(emu, st, 0x7, 0x4),
            "Shadow Temple MQ Invisible Spikes Chest":          _chest(emu, st, 0x7, 0x9),
            "Shadow Temple MQ Stalfos Room Chest":              _chest(emu, st, 0x7, 0x10),
            "Shadow Temple MQ Wind Hint Chest":                 _chest(emu, st, 0x7, 0x15),
            "Shadow Temple MQ After Wind Hidden Chest":         _chest(emu, st, 0x7, 0x14),
            "Shadow Temple MQ After Wind Enemy Chest":          _chest(emu, st, 0x7, 0x8),
            "Shadow Temple MQ Boss Key Chest":                  _chest(emu, st, 0x7, 0xB),
            "Shadow Temple MQ Spike Walls Left Chest":          _chest(emu, st, 0x7, 0xA),
            "Shadow Temple MQ Freestanding Key":                _ground(emu, st, 0x7, 0x6),
            "Shadow Temple MQ Bomb Flower Chest":               _chest(emu, st, 0x7, 0xD),
            "Shadow Temple MQ GS Falling Spikes Room":          _skulltula(emu, 0x7, 0x1),
            "Shadow Temple MQ GS Wind Hint Room":               _skulltula(emu, 0x7, 0x0),
            "Shadow Temple MQ GS After Wind":                   _skulltula(emu, 0x7, 0x3),
            "Shadow Temple MQ GS After Ship":                   _skulltula(emu, 0x7, 0x4),
            "Shadow Temple MQ GS Near Boss":                    _skulltula(emu, 0x7, 0x2),
        })
    checks["Shadow Temple Bongo Bongo Heart"] = _boss_heart(emu, st, 0x18, 0x0C)
    checks["Bongo Bongo"]                     = _boss_reward(st, 0x0C)
    return checks


def _death_mountain_trail(emu: EmuLoaderClient, st: OoTBridgeState) -> dict:
    dmt_fairy = _fairy(emu, st, 0x3B, 0x18) or _check_temp_context(st, 0xFF, 0x05, 0x13)
    return {
        "DMT Freestanding PoH":       _ground(emu, st, 0x60, 0x1E),
        "DMT Chest":                  _chest(emu, st, 0x60, 0x01),
        "DMT Storms Grotto Chest":    _chest(emu, st, 0x3E, 0x17),
        "DMT Great Fairy Reward":     dmt_fairy,
        "DMT Biggoron":               _bgs(emu),
        "DMT Cow Grotto Cow":         _cow(emu, st, 0x3E, 0x18),
        "DMT GS Near Kak":            _skulltula(emu, 0x0F, 0x2),
        "DMT GS Bean Patch":          _skulltula(emu, 0x0F, 0x1),
        "DMT GS Above Dodongos Cavern":_skulltula(emu, 0x0F, 0x3),
        "DMT GS Falling Rocks Path":  _skulltula(emu, 0x0F, 0x4),
    }


def _goron_city(emu: EmuLoaderClient, st: OoTBridgeState) -> dict:
    return {
        "GC Darunias Joy":            _event(emu, 0x3, 0x6),
        "GC Pot Freestanding PoH":    _ground(emu, st, 0x62, 0x1F),
        "GC Rolling Goron as Child":  _inf(emu, 0x22, 0x6),
        "GC Rolling Goron as Adult":  _inf(emu, 0x20, 0x1),
        "GC Medigoron":               _medigoron(emu, st, 0x62, 0x1),
        "GC Maze Left Chest":         _chest(emu, st, 0x62, 0x00),
        "GC Maze Right Chest":        _chest(emu, st, 0x62, 0x01),
        "GC Maze Center Chest":       _chest(emu, st, 0x62, 0x02),
        "GC Deku Scrub Grotto Left":  _scrub(emu, 0x25, 0x1),
        "GC Deku Scrub Grotto Center":_scrub(emu, 0x25, 0x4),
        "GC Deku Scrub Grotto Right": _scrub(emu, 0x25, 0x6),
        "GC GS Center Platform":      _skulltula(emu, 0x0F, 0x5),
        "GC GS Boulder Maze":         _skulltula(emu, 0x0F, 0x6),
        "GC Shop Item 5":             _shop(emu, 0x5, 0x0),
        "GC Shop Item 6":             _shop(emu, 0x5, 0x1),
        "GC Shop Item 7":             _shop(emu, 0x5, 0x2),
        "GC Shop Item 8":             _shop(emu, 0x5, 0x3),
    }


def _death_mountain_crater(emu: EmuLoaderClient, st: OoTBridgeState) -> dict:
    dmc_fairy = _fairy(emu, st, 0x3B, 0x10) or _check_temp_context(st, 0xFF, 0x05, 0x14)
    return {
        "DMC Volcano Freestanding PoH":    _ground(emu, st, 0x61, 0x08),
        "DMC Wall Freestanding PoH":       _ground(emu, st, 0x61, 0x02),
        "DMC Upper Grotto Chest":          _chest(emu, st, 0x3E, 0x1A),
        "DMC Great Fairy Reward":          dmc_fairy,
        "DMC Deku Scrub":                  _scrub(emu, 0x61, 0x6),
        "DMC Deku Scrub Grotto Left":      _scrub(emu, 0x23, 0x1),
        "DMC Deku Scrub Grotto Center":    _scrub(emu, 0x23, 0x4),
        "DMC Deku Scrub Grotto Right":     _scrub(emu, 0x23, 0x6),
        "DMC GS Crate":                    _skulltula(emu, 0x0F, 0x7),
        "DMC GS Bean Patch":               _skulltula(emu, 0x0F, 0x0),
    }


def _dodongos_cavern(emu: EmuLoaderClient, st: OoTBridgeState) -> dict:
    checks = {}
    if not _is_mq(emu, st, 0x1):
        checks.update({
            "Dodongos Cavern Map Chest":                        _chest(emu, st, 0x01, 0x8),
            "Dodongos Cavern Compass Chest":                    _chest(emu, st, 0x01, 0x5),
            "Dodongos Cavern Bomb Flower Platform Chest":       _chest(emu, st, 0x01, 0x6),
            "Dodongos Cavern Bomb Bag Chest":                   _chest(emu, st, 0x01, 0x4),
            "Dodongos Cavern End of Bridge Chest":              _chest(emu, st, 0x01, 0xA),
            "Dodongos Cavern Deku Scrub Lobby":                 _scrub(emu, 0x1, 0x5),
            "Dodongos Cavern Deku Scrub Side Room Near Dodongos":_scrub(emu, 0x1, 0x2),
            "Dodongos Cavern Deku Scrub Near Bomb Bag Left":    _scrub(emu, 0x1, 0x1),
            "Dodongos Cavern Deku Scrub Near Bomb Bag Right":   _scrub(emu, 0x1, 0x4),
            "Dodongos Cavern GS Side Room Near Lower Lizalfos": _skulltula(emu, 0x01, 0x4),
            "Dodongos Cavern GS Scarecrow":                     _skulltula(emu, 0x01, 0x1),
            "Dodongos Cavern GS Alcove Above Stairs":           _skulltula(emu, 0x01, 0x2),
            "Dodongos Cavern GS Vines Above Stairs":            _skulltula(emu, 0x01, 0x0),
            "Dodongos Cavern GS Back Room":                     _skulltula(emu, 0x01, 0x3),
        })
    else:
        checks.update({
            "Dodongos Cavern MQ Map Chest":                              _chest(emu, st, 0x1, 0x0),
            "Dodongos Cavern MQ Bomb Bag Chest":                         _chest(emu, st, 0x1, 0x4),
            "Dodongos Cavern MQ Torch Puzzle Room Chest":                _chest(emu, st, 0x1, 0x3),
            "Dodongos Cavern MQ Larvae Room Chest":                      _chest(emu, st, 0x1, 0x2),
            "Dodongos Cavern MQ Compass Chest":                          _chest(emu, st, 0x1, 0x5),
            "Dodongos Cavern MQ Under Grave Chest":                      _chest(emu, st, 0x1, 0x1),
            "Dodongos Cavern MQ Deku Scrub Lobby Front":                 _scrub(emu, 0x1, 0x4),
            "Dodongos Cavern MQ Deku Scrub Lobby Rear":                  _scrub(emu, 0x1, 0x2),
            "Dodongos Cavern MQ Deku Scrub Side Room Near Lower Lizalfos":_scrub(emu, 0x1, 0x8),
            "Dodongos Cavern MQ Deku Scrub Staircase":                   _scrub(emu, 0x1, 0x5),
            "Dodongos Cavern MQ GS Scrub Room":                          _skulltula(emu, 0x1, 0x1),
            "Dodongos Cavern MQ GS Larvae Room":                         _skulltula(emu, 0x1, 0x4),
            "Dodongos Cavern MQ GS Lizalfos Room":                       _skulltula(emu, 0x1, 0x2),
            "Dodongos Cavern MQ GS Song of Time Block Room":             _skulltula(emu, 0x1, 0x3),
            "Dodongos Cavern MQ GS Back Area":                           _skulltula(emu, 0x1, 0x0),
        })
    checks["Dodongos Cavern Boss Room Chest"]       = _chest(emu, st, 0x12, 0x0)
    checks["Dodongos Cavern King Dodongo Heart"]    = _boss_heart(emu, st, 0x12, 0x06)
    checks["King Dodongo"]                          = _boss_reward(st, 0x06)
    return checks


def _fire_temple(emu: EmuLoaderClient, st: OoTBridgeState) -> dict:
    checks = {}
    if not _is_mq(emu, st, 0x4):
        checks.update({
            "Fire Temple Near Boss Chest":                 _chest(emu, st, 0x04, 0x01),
            "Fire Temple Flare Dancer Chest":              _chest(emu, st, 0x04, 0x00),
            "Fire Temple Boss Key Chest":                  _chest(emu, st, 0x04, 0x0C),
            "Fire Temple Big Lava Room Lower Open Door Chest": _chest(emu, st, 0x04, 0x04),
            "Fire Temple Big Lava Room Blocked Door Chest":_chest(emu, st, 0x04, 0x02),
            "Fire Temple Boulder Maze Lower Chest":        _chest(emu, st, 0x04, 0x03),
            "Fire Temple Boulder Maze Side Room Chest":    _chest(emu, st, 0x04, 0x08),
            "Fire Temple Map Chest":                       _chest(emu, st, 0x04, 0x0A),
            "Fire Temple Boulder Maze Shortcut Chest":     _chest(emu, st, 0x04, 0x0B),
            "Fire Temple Boulder Maze Upper Chest":        _chest(emu, st, 0x04, 0x06),
            "Fire Temple Scarecrow Chest":                 _chest(emu, st, 0x04, 0x0D),
            "Fire Temple Compass Chest":                   _chest(emu, st, 0x04, 0x07),
            "Fire Temple Megaton Hammer Chest":            _chest(emu, st, 0x04, 0x05),
            "Fire Temple Highest Goron Chest":             _chest(emu, st, 0x04, 0x09),
            "Fire Temple GS Boss Key Loop":                _skulltula(emu, 0x04, 0x1),
            "Fire Temple GS Song of Time Room":            _skulltula(emu, 0x04, 0x0),
            "Fire Temple GS Boulder Maze":                 _skulltula(emu, 0x04, 0x2),
            "Fire Temple GS Scarecrow Climb":              _skulltula(emu, 0x04, 0x4),
            "Fire Temple GS Scarecrow Top":                _skulltula(emu, 0x04, 0x3),
        })
    else:
        checks.update({
            "Fire Temple MQ Map Room Side Chest":                _chest(emu, st, 0x4, 0x2),
            "Fire Temple MQ Megaton Hammer Chest":               _chest(emu, st, 0x4, 0x0),
            "Fire Temple MQ Map Chest":                          _chest(emu, st, 0x4, 0xC),
            "Fire Temple MQ Near Boss Chest":                    _chest(emu, st, 0x4, 0x7),
            "Fire Temple MQ Big Lava Room Blocked Door Chest":   _chest(emu, st, 0x4, 0x1),
            "Fire Temple MQ Boss Key Chest":                     _chest(emu, st, 0x4, 0x4),
            "Fire Temple MQ Lizalfos Maze Side Room Chest":      _chest(emu, st, 0x4, 0x8),
            "Fire Temple MQ Compass Chest":                      _chest(emu, st, 0x4, 0xB),
            "Fire Temple MQ Lizalfos Maze Upper Chest":          _chest(emu, st, 0x4, 0x6),
            "Fire Temple MQ Lizalfos Maze Lower Chest":          _chest(emu, st, 0x4, 0x3),
            "Fire Temple MQ Freestanding Key":                   _ground(emu, st, 0x4, 0x1C),
            "Fire Temple MQ Chest On Fire":                      _chest(emu, st, 0x4, 0x5),
            "Fire Temple MQ GS Big Lava Room Open Door":         _skulltula(emu, 0x4, 0x0),
            "Fire Temple MQ GS Skull On Fire":                   _skulltula(emu, 0x4, 0x2),
            "Fire Temple MQ GS Flame Maze Center":               _skulltula(emu, 0x4, 0x3),
            "Fire Temple MQ GS Flame Maze Side Room":            _skulltula(emu, 0x4, 0x4),
            "Fire Temple MQ GS Above Flame Maze":                _skulltula(emu, 0x4, 0x1),
        })
    checks["Fire Temple Volvagia Heart"] = _boss_heart(emu, st, 0x15, 0x09)
    checks["Volvagia"]                   = _boss_reward(st, 0x09)
    return checks


def _zoras_river(emu: EmuLoaderClient, st: OoTBridgeState) -> dict:
    return {
        "ZR Magic Bean Salesman":          _bean(emu, st, 0x54, 0x1),
        "ZR Open Grotto Chest":            _chest(emu, st, 0x3E, 0x09),
        "ZR Frogs in the Rain":            _event(emu, 0xD, 0x6),
        "ZR Frogs Ocarina Game":           _event(emu, 0xD, 0x0),
        "ZR Near Open Grotto Freestanding PoH": _ground(emu, st, 0x54, 0x04),
        "ZR Near Domain Freestanding PoH": _ground(emu, st, 0x54, 0x0B),
        "ZR Deku Scrub Grotto Front":      _scrub(emu, 0x15, 0x9),
        "ZR Deku Scrub Grotto Rear":       _scrub(emu, 0x15, 0x8),
        "ZR Frogs Zeldas Lullaby":         _event(emu, 0xD, 0x1),
        "ZR Frogs Eponas Song":            _event(emu, 0xD, 0x2),
        "ZR Frogs Suns Song":              _event(emu, 0xD, 0x3),
        "ZR Frogs Sarias Song":            _event(emu, 0xD, 0x4),
        "ZR Frogs Song of Time":           _event(emu, 0xD, 0x5),
        "ZR GS Tree":                      _skulltula(emu, 0x11, 0x1),
        "ZR GS Ladder":                    _skulltula(emu, 0x11, 0x0),
        "ZR GS Near Raised Grottos":       _skulltula(emu, 0x11, 0x4),
        "ZR GS Above Bridge":              _skulltula(emu, 0x11, 0x3),
    }


def _zoras_domain(emu: EmuLoaderClient, st: OoTBridgeState) -> dict:
    return {
        "ZD Diving Minigame": _event(emu, 0x3, 0x8),
        "ZD Chest":           _chest(emu, st, 0x58, 0x00),
        "ZD King Zora Thawed":_inf(emu, 0x26, 0x1),
        "ZD GS Frozen Waterfall":_skulltula(emu, 0x11, 0x6),
        "ZD Shop Item 5":     _shop(emu, 0x2, 0x0),
        "ZD Shop Item 6":     _shop(emu, 0x2, 0x1),
        "ZD Shop Item 7":     _shop(emu, 0x2, 0x2),
        "ZD Shop Item 8":     _shop(emu, 0x2, 0x3),
    }


def _zoras_fountain(emu: EmuLoaderClient, st: OoTBridgeState) -> dict:
    return {
        "ZF Great Fairy Reward":         _igi(emu, 0x2, 0x0),
        "ZF Iceberg Freestanding PoH":   _ground(emu, st, 0x59, 0x01),
        "ZF Bottom Freestanding PoH":    _ground(emu, st, 0x59, 0x14),
        "ZF GS Above the Log":           _skulltula(emu, 0x11, 0x2),
        "ZF GS Tree":                    _skulltula(emu, 0x11, 0x7),
        "ZF GS Hidden Cave":             _skulltula(emu, 0x11, 0x5),
    }


def _jabu(emu: EmuLoaderClient, st: OoTBridgeState) -> dict:
    checks = {}
    if not _is_mq(emu, st, 0x2):
        checks.update({
            "Jabu Jabus Belly Boomerang Chest":        _chest(emu, st, 0x02, 0x01),
            "Jabu Jabus Belly Map Chest":              _chest(emu, st, 0x02, 0x02),
            "Jabu Jabus Belly Compass Chest":          _chest(emu, st, 0x02, 0x04),
            "Jabu Jabus Belly Deku Scrub":             _scrub(emu, 0x02, 0x1),
            "Jabu Jabus Belly GS Water Switch Room":   _skulltula(emu, 0x02, 0x3),
            "Jabu Jabus Belly GS Lobby Basement Lower":_skulltula(emu, 0x02, 0x0),
            "Jabu Jabus Belly GS Lobby Basement Upper":_skulltula(emu, 0x02, 0x1),
            "Jabu Jabus Belly GS Near Boss":           _skulltula(emu, 0x02, 0x2),
        })
    else:
        checks.update({
            "Jabu Jabus Belly MQ Map Chest":                _chest(emu, st, 0x2, 0x3),
            "Jabu Jabus Belly MQ First Room Side Chest":    _chest(emu, st, 0x2, 0x5),
            "Jabu Jabus Belly MQ Second Room Lower Chest":  _chest(emu, st, 0x2, 0x2),
            "Jabu Jabus Belly MQ Compass Chest":            _chest(emu, st, 0x2, 0x0),
            "Jabu Jabus Belly MQ Basement Near Switches Chest": _chest(emu, st, 0x2, 0x8),
            "Jabu Jabus Belly MQ Basement Near Vines Chest":    _chest(emu, st, 0x2, 0x4),
            "Jabu Jabus Belly MQ Boomerang Room Small Chest":   _chest(emu, st, 0x2, 0x1),
            "Jabu Jabus Belly MQ Boomerang Chest":          _chest(emu, st, 0x2, 0x6),
            "Jabu Jabus Belly MQ Falling Like Like Room Chest": _chest(emu, st, 0x2, 0x9),
            "Jabu Jabus Belly MQ Second Room Upper Chest":  _chest(emu, st, 0x2, 0x7),
            "Jabu Jabus Belly MQ Near Boss Chest":          _chest(emu, st, 0x2, 0xA),
            "Jabu Jabus Belly MQ Cow":                      _cow(emu, st, 0x2, 0x18),
            "Jabu Jabus Belly MQ GS Boomerang Chest Room":  _skulltula(emu, 0x2, 0x0),
            "Jabu Jabus Belly MQ GS Tailpasaran Room":      _skulltula(emu, 0x2, 0x2),
            "Jabu Jabus Belly MQ GS Invisible Enemies Room":_skulltula(emu, 0x2, 0x3),
            "Jabu Jabus Belly MQ GS Near Boss":             _skulltula(emu, 0x2, 0x1),
        })
    checks["Jabu Jabus Belly Barinade Heart"] = _boss_heart(emu, st, 0x13, 0x07)
    checks["Barinade"]                        = _boss_reward(st, 0x07)
    return checks


def _ice_cavern(emu: EmuLoaderClient, st: OoTBridgeState) -> dict:
    checks = {}
    if not _is_mq(emu, st, 0x9):
        checks.update({
            "Ice Cavern Map Chest":              _chest(emu, st, 0x09, 0x00),
            "Ice Cavern Compass Chest":          _chest(emu, st, 0x09, 0x01),
            "Ice Cavern Freestanding PoH":       _ground(emu, st, 0x09, 0x01),
            "Ice Cavern Iron Boots Chest":       _chest(emu, st, 0x09, 0x02),
            "Ice Cavern GS Spinning Scythe Room":_skulltula(emu, 0x09, 0x1),
            "Ice Cavern GS Heart Piece Room":    _skulltula(emu, 0x09, 0x2),
            "Ice Cavern GS Push Block Room":     _skulltula(emu, 0x09, 0x0),
        })
    else:
        checks.update({
            "Ice Cavern MQ Map Chest":       _chest(emu, st, 0x09, 0x01),
            "Ice Cavern MQ Compass Chest":   _chest(emu, st, 0x09, 0x00),
            "Ice Cavern MQ Freestanding PoH":_ground(emu, st, 0x09, 0x01),
            "Ice Cavern MQ Iron Boots Chest":_chest(emu, st, 0x09, 0x02),
            "Ice Cavern MQ GS Red Ice":      _skulltula(emu, 0x09, 0x1),
            "Ice Cavern MQ GS Ice Block":    _skulltula(emu, 0x09, 0x2),
            "Ice Cavern MQ GS Scarecrow":    _skulltula(emu, 0x09, 0x0),
        })
    return checks


def _lake_hylia(emu: EmuLoaderClient, st: OoTBridgeState) -> dict:
    return {
        "LH Underwater Item":           _event(emu, 0x3, 0x1),
        "LH Child Fishing":             _fishing(emu, False),
        "LH Adult Fishing":             _fishing(emu, True),
        "LH Lab Dive":                  _igi(emu, 0x3, 0x0),
        "LH Freestanding PoH":          _ground(emu, st, 0x57, 0x1E),
        "LH Sun":                       _fire_arrows(emu, st, 0x57, 0x0),
        "LH Deku Scrub Grotto Left":    _scrub(emu, 0x19, 0x1),
        "LH Deku Scrub Grotto Center":  _scrub(emu, 0x19, 0x4),
        "LH Deku Scrub Grotto Right":   _scrub(emu, 0x19, 0x6),
        "LH GS Lab Wall":               _skulltula(emu, 0x12, 0x2),
        "LH GS Bean Patch":             _skulltula(emu, 0x12, 0x0),
        "LH GS Small Island":           _skulltula(emu, 0x12, 0x1),
        "LH GS Lab Crate":              _skulltula(emu, 0x12, 0x3),
        "LH GS Tree":                   _skulltula(emu, 0x12, 0x4),
    }


def _water_temple(emu: EmuLoaderClient, st: OoTBridgeState) -> dict:
    checks = {}
    if not _is_mq(emu, st, 0x5):
        checks.update({
            "Water Temple Compass Chest":              _chest(emu, st, 0x05, 0x09),
            "Water Temple Map Chest":                  _chest(emu, st, 0x05, 0x02),
            "Water Temple Cracked Wall Chest":         _chest(emu, st, 0x05, 0x00),
            "Water Temple Torches Chest":              _chest(emu, st, 0x05, 0x01),
            "Water Temple Boss Key Chest":             _chest(emu, st, 0x05, 0x05),
            "Water Temple Central Pillar Chest":       _chest(emu, st, 0x05, 0x06),
            "Water Temple Central Bow Target Chest":   _chest(emu, st, 0x05, 0x08),
            "Water Temple Longshot Chest":             _chest(emu, st, 0x05, 0x07),
            "Water Temple River Chest":                _chest(emu, st, 0x05, 0x03),
            "Water Temple Dragon Chest":               _chest(emu, st, 0x05, 0x0A),
            "Water Temple GS Behind Gate":             _skulltula(emu, 0x05, 0x0),
            "Water Temple GS Near Boss Key Chest":     _skulltula(emu, 0x05, 0x3),
            "Water Temple GS Central Pillar":          _skulltula(emu, 0x05, 0x2),
            "Water Temple GS Falling Platform Room":   _skulltula(emu, 0x05, 0x1),
            "Water Temple GS River":                   _skulltula(emu, 0x05, 0x4),
        })
    else:
        checks.update({
            "Water Temple MQ Longshot Chest":              _chest(emu, st, 0x5, 0x0),
            "Water Temple MQ Map Chest":                   _chest(emu, st, 0x5, 0x2),
            "Water Temple MQ Compass Chest":               _chest(emu, st, 0x5, 0x1),
            "Water Temple MQ Central Pillar Chest":        _chest(emu, st, 0x5, 0x6),
            "Water Temple MQ Boss Key Chest":              _chest(emu, st, 0x5, 0x5),
            "Water Temple MQ Freestanding Key":            _ground(emu, st, 0x5, 0x1),
            "Water Temple MQ GS Lizalfos Hallway":         _skulltula(emu, 0x5, 0x0),
            "Water Temple MQ GS Before Upper Water Switch":_skulltula(emu, 0x5, 0x2),
            "Water Temple MQ GS River":                    _skulltula(emu, 0x5, 0x1),
            "Water Temple MQ GS Freestanding Key Area":    _skulltula(emu, 0x5, 0x3),
            "Water Temple MQ GS Triple Wall Torch":        _skulltula(emu, 0x5, 0x4),
        })
    checks["Water Temple Morpha Heart"] = _boss_heart(emu, st, 0x16, 0x0A)
    checks["Morpha"]                    = _boss_reward(st, 0x0A)
    return checks


def _gerudo_valley(emu: EmuLoaderClient, st: OoTBridgeState) -> dict:
    return {
        "GV Crate Freestanding PoH":     _ground(emu, st, 0x5A, 0x2),
        "GV Waterfall Freestanding PoH": _ground(emu, st, 0x5A, 0x1),
        "GV Chest":                      _chest(emu, st, 0x5A, 0x00),
        "GV Deku Scrub Grotto Front":    _scrub(emu, 0x1A, 0x9),
        "GV Deku Scrub Grotto Rear":     _scrub(emu, 0x1A, 0x8),
        "GV Cow":                        _cow(emu, st, 0x5A, 0x18),
        "GV GS Small Bridge":            _skulltula(emu, 0x13, 0x1),
        "GV GS Bean Patch":              _skulltula(emu, 0x13, 0x0),
        "GV GS Behind Tent":             _skulltula(emu, 0x13, 0x3),
        "GV GS Pillar":                  _skulltula(emu, 0x13, 0x2),
    }


def _gerudo_fortress(emu: EmuLoaderClient, st: OoTBridgeState) -> dict:
    return {
        "Hideout 1 Torch Jail Gerudo Key": _ground(emu, st, 0xC, 0xC),
        "Hideout 2 Torches Jail Gerudo Key":_ground(emu, st, 0xC, 0xF),
        "Hideout 3 Torches Jail Gerudo Key":_ground(emu, st, 0xC, 0xA),
        "Hideout 4 Torches Jail Gerudo Key":_ground(emu, st, 0xC, 0xE),
        "Hideout Gerudo Membership Card":  _membership(emu),
        "GF Chest":                        _chest(emu, st, 0x5D, 0x0),
        "GF HBA 1000 Points":              _inf(emu, 0x33, 0x0),
        "GF HBA 1500 Points":              _igi(emu, 0x0, 0x7),
        "GF GS Top Floor":                 _skulltula(emu, 0x14, 0x1),
        "GF GS Archery Range":             _skulltula(emu, 0x14, 0x0),
    }


def _gerudo_training_ground(emu: EmuLoaderClient, st: OoTBridgeState) -> dict:
    checks = {}
    if not _is_mq(emu, st, 0xB):
        checks.update({
            "Gerudo Training Ground Lobby Left Chest":          _chest(emu, st, 0x0B, 0x13),
            "Gerudo Training Ground Lobby Right Chest":         _chest(emu, st, 0x0B, 0x07),
            "Gerudo Training Ground Stalfos Chest":             _chest(emu, st, 0x0B, 0x00),
            "Gerudo Training Ground Before Heavy Block Chest":  _chest(emu, st, 0x0B, 0x11),
            "Gerudo Training Ground Heavy Block First Chest":   _chest(emu, st, 0x0B, 0x0F),
            "Gerudo Training Ground Heavy Block Second Chest":  _chest(emu, st, 0x0B, 0x0E),
            "Gerudo Training Ground Heavy Block Third Chest":   _chest(emu, st, 0x0B, 0x14),
            "Gerudo Training Ground Heavy Block Fourth Chest":  _chest(emu, st, 0x0B, 0x02),
            "Gerudo Training Ground Eye Statue Chest":          _chest(emu, st, 0x0B, 0x03),
            "Gerudo Training Ground Near Scarecrow Chest":      _chest(emu, st, 0x0B, 0x04),
            "Gerudo Training Ground Hammer Room Clear Chest":   _chest(emu, st, 0x0B, 0x12),
            "Gerudo Training Ground Hammer Room Switch Chest":  _chest(emu, st, 0x0B, 0x10),
            "Gerudo Training Ground Freestanding Key":          _ground(emu, st, 0x0B, 0x1),
            "Gerudo Training Ground Maze Right Central Chest":  _chest(emu, st, 0x0B, 0x05),
            "Gerudo Training Ground Maze Right Side Chest":     _chest(emu, st, 0x0B, 0x08),
            "Gerudo Training Ground Underwater Silver Rupee Chest": _chest(emu, st, 0x0B, 0x0D),
            "Gerudo Training Ground Beamos Chest":              _chest(emu, st, 0x0B, 0x01),
            "Gerudo Training Ground Hidden Ceiling Chest":      _chest(emu, st, 0x0B, 0x0B),
            "Gerudo Training Ground Maze Path First Chest":     _chest(emu, st, 0x0B, 0x06),
            "Gerudo Training Ground Maze Path Second Chest":    _chest(emu, st, 0x0B, 0x0A),
            "Gerudo Training Ground Maze Path Third Chest":     _chest(emu, st, 0x0B, 0x09),
            "Gerudo Training Ground Maze Path Final Chest":     _chest(emu, st, 0x0B, 0x0C),
        })
    else:
        checks.update({
            "Gerudo Training Ground MQ Lobby Left Chest":            _chest(emu, st, 0xB, 0x13),
            "Gerudo Training Ground MQ Lobby Right Chest":           _chest(emu, st, 0xB, 0x7),
            "Gerudo Training Ground MQ First Iron Knuckle Chest":    _chest(emu, st, 0xB, 0x0),
            "Gerudo Training Ground MQ Before Heavy Block Chest":    _chest(emu, st, 0xB, 0x11),
            "Gerudo Training Ground MQ Heavy Block Chest":           _chest(emu, st, 0xB, 0x2),
            "Gerudo Training Ground MQ Eye Statue Chest":            _chest(emu, st, 0xB, 0x3),
            "Gerudo Training Ground MQ Ice Arrows Chest":            _chest(emu, st, 0xB, 0x4),
            "Gerudo Training Ground MQ Second Iron Knuckle Chest":   _chest(emu, st, 0xB, 0x12),
            "Gerudo Training Ground MQ Flame Circle Chest":          _chest(emu, st, 0xB, 0xE),
            "Gerudo Training Ground MQ Maze Right Central Chest":    _chest(emu, st, 0xB, 0x5),
            "Gerudo Training Ground MQ Maze Right Side Chest":       _chest(emu, st, 0xB, 0x8),
            "Gerudo Training Ground MQ Underwater Silver Rupee Chest":_chest(emu, st, 0xB, 0xD),
            "Gerudo Training Ground MQ Dinolfos Chest":              _chest(emu, st, 0xB, 0x1),
            "Gerudo Training Ground MQ Hidden Ceiling Chest":        _chest(emu, st, 0xB, 0xB),
            "Gerudo Training Ground MQ Maze Path First Chest":       _chest(emu, st, 0xB, 0x6),
            "Gerudo Training Ground MQ Maze Path Third Chest":       _chest(emu, st, 0xB, 0x9),
            "Gerudo Training Ground MQ Maze Path Second Chest":      _chest(emu, st, 0xB, 0xA),
        })
    return checks


def _haunted_wasteland(emu: EmuLoaderClient, st: OoTBridgeState) -> dict:
    return {
        "Wasteland Bombchu Salesman": _salesman(emu, st, 0x5E, 0x01),
        "Wasteland Chest":           _chest(emu, st, 0x5E, 0x00),
        "Wasteland GS":              _skulltula(emu, 0x15, 0x1),
    }


def _desert_colossus(emu: EmuLoaderClient, st: OoTBridgeState) -> dict:
    return {
        "Colossus Great Fairy Reward":       _igi(emu, 0x2, 0x2),
        "Colossus Freestanding PoH":         _ground(emu, st, 0x5C, 0xD),
        "Colossus Deku Scrub Grotto Front":  _scrub(emu, 0x27, 0x9),
        "Colossus Deku Scrub Grotto Rear":   _scrub(emu, 0x27, 0x8),
        "Colossus GS Bean Patch":            _skulltula(emu, 0x15, 0x0),
        "Colossus GS Tree":                  _skulltula(emu, 0x15, 0x3),
        "Colossus GS Hill":                  _skulltula(emu, 0x15, 0x2),
    }


def _spirit_temple(emu: EmuLoaderClient, st: OoTBridgeState) -> dict:
    checks = {}
    if not _is_mq(emu, st, 0x6):
        checks.update({
            "Spirit Temple Child Bridge Chest":           _chest(emu, st, 0x06, 0x08),
            "Spirit Temple Child Early Torches Chest":    _chest(emu, st, 0x06, 0x00),
            "Spirit Temple Child Climb North Chest":      _chest(emu, st, 0x06, 0x06),
            "Spirit Temple Child Climb East Chest":       _chest(emu, st, 0x06, 0x0C),
            "Spirit Temple Map Chest":                    _chest(emu, st, 0x06, 0x03),
            "Spirit Temple Sun Block Room Chest":         _chest(emu, st, 0x06, 0x01),
            "Spirit Temple Silver Gauntlets Chest":       _chest(emu, st, 0x5C, 0x0B),
            "Spirit Temple Compass Chest":                _chest(emu, st, 0x06, 0x04),
            "Spirit Temple Early Adult Right Chest":      _chest(emu, st, 0x06, 0x07),
            "Spirit Temple First Mirror Left Chest":      _chest(emu, st, 0x06, 0x0D),
            "Spirit Temple First Mirror Right Chest":     _chest(emu, st, 0x06, 0x0E),
            "Spirit Temple Statue Room Northeast Chest":  _chest(emu, st, 0x06, 0x0F),
            "Spirit Temple Statue Room Hand Chest":       _chest(emu, st, 0x06, 0x02),
            "Spirit Temple Near Four Armos Chest":        _chest(emu, st, 0x06, 0x05),
            "Spirit Temple Hallway Right Invisible Chest":_chest(emu, st, 0x06, 0x14),
            "Spirit Temple Hallway Left Invisible Chest": _chest(emu, st, 0x06, 0x15),
            "Spirit Temple Mirror Shield Chest":          _chest(emu, st, 0x5C, 0x09),
            "Spirit Temple Boss Key Chest":               _chest(emu, st, 0x06, 0x0A),
            "Spirit Temple Topmost Chest":                _chest(emu, st, 0x06, 0x12),
            "Spirit Temple GS Metal Fence":               _skulltula(emu, 0x06, 0x4),
            "Spirit Temple GS Sun on Floor Room":         _skulltula(emu, 0x06, 0x3),
            "Spirit Temple GS Hall After Sun Block Room": _skulltula(emu, 0x06, 0x0),
            "Spirit Temple GS Lobby":                     _skulltula(emu, 0x06, 0x2),
            "Spirit Temple GS Boulder Room":              _skulltula(emu, 0x06, 0x1),
        })
    else:
        checks.update({
            "Spirit Temple MQ Entrance Front Left Chest":   _chest(emu, st, 0x6, 0x1A),
            "Spirit Temple MQ Entrance Back Right Chest":   _chest(emu, st, 0x6, 0x1F),
            "Spirit Temple MQ Entrance Front Right Chest":  _chest(emu, st, 0x6, 0x1B),
            "Spirit Temple MQ Entrance Back Left Chest":    _chest(emu, st, 0x6, 0x1E),
            "Spirit Temple MQ Map Chest":                   _chest(emu, st, 0x6, 0x0),
            "Spirit Temple MQ Map Room Enemy Chest":        _chest(emu, st, 0x6, 0x8),
            "Spirit Temple MQ Child Climb North Chest":     _chest(emu, st, 0x6, 0x6),
            "Spirit Temple MQ Child Climb South Chest":     _chest(emu, st, 0x6, 0xC),
            "Spirit Temple MQ Compass Chest":               _chest(emu, st, 0x6, 0x3),
            "Spirit Temple MQ Silver Block Hallway Chest":  _chest(emu, st, 0x6, 0x1C),
            "Spirit Temple MQ Sun Block Room Chest":        _chest(emu, st, 0x6, 0x1),
            "Spirit Temple Silver Gauntlets Chest":         _chest(emu, st, 0x5C, 0xB),
            "Spirit Temple MQ Child Hammer Switch Chest":   _chest(emu, st, 0x6, 0x1D),
            "Spirit Temple MQ Statue Room Lullaby Chest":   _chest(emu, st, 0x6, 0xF),
            "Spirit Temple MQ Statue Room Invisible Chest": _chest(emu, st, 0x6, 0x2),
            "Spirit Temple MQ Leever Room Chest":           _chest(emu, st, 0x6, 0x4),
            "Spirit Temple MQ Symphony Room Chest":         _chest(emu, st, 0x6, 0x7),
            "Spirit Temple MQ Beamos Room Chest":           _chest(emu, st, 0x6, 0x19),
            "Spirit Temple MQ Chest Switch Chest":          _chest(emu, st, 0x6, 0x18),
            "Spirit Temple MQ Boss Key Chest":              _chest(emu, st, 0x6, 0x5),
            "Spirit Temple Mirror Shield Chest":            _chest(emu, st, 0x5C, 0x9),
            "Spirit Temple MQ Mirror Puzzle Invisible Chest":_chest(emu, st, 0x6, 0x12),
            "Spirit Temple MQ GS Sun Block Room":           _skulltula(emu, 0x6, 0x0),
            "Spirit Temple MQ GS Leever Room":              _skulltula(emu, 0x6, 0x1),
            "Spirit Temple MQ GS Symphony Room":            _skulltula(emu, 0x6, 0x3),
            "Spirit Temple MQ GS Nine Thrones Room West":   _skulltula(emu, 0x6, 0x2),
            "Spirit Temple MQ GS Nine Thrones Room North":  _skulltula(emu, 0x6, 0x4),
        })
    checks["Spirit Temple Twinrova Heart"] = _boss_heart(emu, st, 0x17, 0x0B)
    checks["Twinrova"]                     = _boss_reward(st, 0x0B)
    return checks


def _ganons_castle(emu: EmuLoaderClient, st: OoTBridgeState) -> dict:
    checks = {}
    if not _is_mq(emu, st, 0xD):
        checks.update({
            "Ganons Castle Forest Trial Chest":                   _chest(emu, st, 0x0D, 0x09),
            "Ganons Castle Water Trial Left Chest":               _chest(emu, st, 0x0D, 0x07),
            "Ganons Castle Water Trial Right Chest":              _chest(emu, st, 0x0D, 0x06),
            "Ganons Castle Shadow Trial Front Chest":             _chest(emu, st, 0x0D, 0x08),
            "Ganons Castle Shadow Trial Golden Gauntlets Chest":  _chest(emu, st, 0x0D, 0x05),
            "Ganons Castle Light Trial First Left Chest":         _chest(emu, st, 0x0D, 0x0C),
            "Ganons Castle Light Trial Second Left Chest":        _chest(emu, st, 0x0D, 0x0B),
            "Ganons Castle Light Trial Third Left Chest":         _chest(emu, st, 0x0D, 0x0D),
            "Ganons Castle Light Trial First Right Chest":        _chest(emu, st, 0x0D, 0x0E),
            "Ganons Castle Light Trial Second Right Chest":       _chest(emu, st, 0x0D, 0x0A),
            "Ganons Castle Light Trial Third Right Chest":        _chest(emu, st, 0x0D, 0x0F),
            "Ganons Castle Light Trial Invisible Enemies Chest":  _chest(emu, st, 0x0D, 0x10),
            "Ganons Castle Light Trial Lullaby Chest":            _chest(emu, st, 0x0D, 0x11),
            "Ganons Castle Spirit Trial Crystal Switch Chest":    _chest(emu, st, 0x0D, 0x12),
            "Ganons Castle Spirit Trial Invisible Chest":         _chest(emu, st, 0x0D, 0x14),
            "Ganons Castle Deku Scrub Left":                      _scrub(emu, 0xD, 0x9),
            "Ganons Castle Deku Scrub Center-Left":               _scrub(emu, 0xD, 0x6),
            "Ganons Castle Deku Scrub Center-Right":              _scrub(emu, 0xD, 0x4),
            "Ganons Castle Deku Scrub Right":                     _scrub(emu, 0xD, 0x8),
        })
    else:
        checks.update({
            "Ganons Castle MQ Forest Trial Freestanding Key":       _ground(emu, st, 0xD, 0x1),
            "Ganons Castle MQ Forest Trial Eye Switch Chest":        _chest(emu, st, 0xD, 0x2),
            "Ganons Castle MQ Forest Trial Frozen Eye Switch Chest": _chest(emu, st, 0xD, 0x3),
            "Ganons Castle MQ Water Trial Chest":                    _chest(emu, st, 0xD, 0x1),
            "Ganons Castle MQ Shadow Trial Bomb Flower Chest":       _chest(emu, st, 0xD, 0x0),
            "Ganons Castle MQ Shadow Trial Eye Switch Chest":        _chest(emu, st, 0xD, 0x5),
            "Ganons Castle MQ Light Trial Lullaby Chest":            _chest(emu, st, 0xD, 0x4),
            "Ganons Castle MQ Spirit Trial First Chest":             _chest(emu, st, 0xD, 0xA),
            "Ganons Castle MQ Spirit Trial Invisible Chest":         _chest(emu, st, 0xD, 0x14),
            "Ganons Castle MQ Spirit Trial Sun Front Left Chest":    _chest(emu, st, 0xD, 0x9),
            "Ganons Castle MQ Spirit Trial Sun Back Left Chest":     _chest(emu, st, 0xD, 0x8),
            "Ganons Castle MQ Spirit Trial Sun Back Right Chest":    _chest(emu, st, 0xD, 0x7),
            "Ganons Castle MQ Spirit Trial Golden Gauntlets Chest":  _chest(emu, st, 0xD, 0x6),
            "Ganons Castle MQ Deku Scrub Left":                      _scrub(emu, 0xD, 0x9),
            "Ganons Castle MQ Deku Scrub Center-Left":               _scrub(emu, 0xD, 0x6),
            "Ganons Castle MQ Deku Scrub Center":                    _scrub(emu, 0xD, 0x4),
            "Ganons Castle MQ Deku Scrub Center-Right":              _scrub(emu, 0xD, 0x8),
            "Ganons Castle MQ Deku Scrub Right":                     _scrub(emu, 0xD, 0x1),
        })
    checks["Ganons Tower Boss Key Chest"] = _chest(emu, st, 0x0A, 0x0B)
    return checks


def _outside_ganons_castle(emu: EmuLoaderClient, st: OoTBridgeState) -> dict:
    return {
        "OGC Great Fairy Reward": _fairy(emu, st, 0x3B, 0x8),
        "OGC GS":                 _skulltula(emu, 0x0E, 0x0),
    }


def _songs(emu: EmuLoaderClient, st: OoTBridgeState) -> dict:
    return {
        "Song from Impa":               _event(emu, 0x5, 0x9),
        "Song from Malon":              _event(emu, 0x5, 0x8),
        "Song from Saria":              _event(emu, 0x5, 0x7),
        "Song from Royal Familys Tomb": _event(emu, 0x5, 0xA),
        "Song from Ocarina of Time":    _event(emu, 0xA, 0x9),
        "Song from Windmill":           _event(emu, 0x5, 0xB),
        "Sheik in Forest":              _event(emu, 0x5, 0x0),
        "Sheik in Crater":              _event(emu, 0x5, 0x1),
        "Sheik in Ice Cavern":          _event(emu, 0x5, 0x2),
        "Sheik at Colossus":            _event(emu, 0xA, 0xC),
        "Sheik in Kakariko":            _event(emu, 0x5, 0x4),
        "Sheik at Temple":              _event(emu, 0x5, 0x5),
    }


def _check_all_locations(emu: EmuLoaderClient, st: OoTBridgeState) -> dict:
    out: dict = {}
    for fn in (
        _kokiri_forest, _lost_woods, _sacred_forest_meadow,
        _deku_tree, _forest_temple,
        _hyrule_field, _lon_lon_ranch, _market, _hyrule_castle,
        _kakariko_village, _graveyard,
        _bottom_of_well, _shadow_temple,
        _death_mountain_trail, _goron_city, _death_mountain_crater,
        _dodongos_cavern, _fire_temple,
        _zoras_river, _zoras_domain, _zoras_fountain,
        _jabu, _ice_cavern,
        _lake_hylia, _water_temple,
        _gerudo_valley, _gerudo_fortress, _gerudo_training_ground,
        _haunted_wasteland, _desert_colossus, _spirit_temple,
        _ganons_castle, _outside_ganons_castle,
        _songs,
    ):
        out.update(fn(emu, st))
    return out


def _check_collectibles(emu: EmuLoaderClient, st: OoTBridgeState) -> dict:
    result: dict = {}
    if st.collectible_overrides is None or not st.collectible_offsets:
        return result
    for id_str, data in st.collectible_offsets.items():
        byte_addr = st.collectible_overrides + data[0] + (data[1] >> 3)
        mem = emu.read_u8(byte_addr)
        result[id_str] = bool(mem & (1 << (7 - (data[1] % 8))))
    return result


def _build_state(emu: EmuLoaderClient, st: OoTBridgeState, include_full_state: bool) -> dict:
    batch_owner = getattr(emu.emulator_info, "begin_batch", None)
    batch_done = getattr(emu.emulator_info, "end_batch", None)
    if batch_owner and batch_done:
        batch_owner()
    try:
        return _build_state_uncached(emu, st, include_full_state)
    finally:
        if batch_done:
            batch_done()


def _build_state_uncached(emu: EmuLoaderClient, st: OoTBridgeState, include_full_state: bool) -> dict:
    payload: dict = {
        "playerName":    _get_player_name(emu),
        "scriptVersion": SCRIPT_VERSION,
        "deathlinkActive": _deathlink_enabled(emu),
    }
    if include_full_state and _in_safe_state(emu) and st.mq_table_address is not None:
        payload["locations"]   = _check_all_locations(emu, st)
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


async def _protocol_cycle(
    reader: asyncio.StreamReader,
    writer: asyncio.StreamWriter,
    emu: EmuLoaderClient,
    st: OoTBridgeState,
    include_full_state: bool,
) -> None:
    """One send-then-receive exchange with the AP client."""
    payload = _build_state(emu, st, include_full_state)
    line    = json.dumps(payload) + "\n"
    writer.write(line.encode())
    await writer.drain()

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
