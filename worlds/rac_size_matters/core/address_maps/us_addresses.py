from __future__ import annotations

from dataclasses import dataclass

ARMOUR_BASE                = 0x1F4B354
ARMOUR_SET_COLLECTED_ADDR  = 0x1F4B442
TITANIUM_BOLT_BASE         = 0x1F4B444
SKILL_POINTS_BASE          = 0x1F4B437
CLANK_CHALLENGE_BASE       = 0x1F4B3DB
CLANK_CHALLENGE_SIZE       = 42
SKYBOARD_BASE              = 0x1F4B407
CHEATS                     = 0x1F4C440
CURRENT_PLANET_ADDRESS     = 0x1F4C76C
PLAYER_BOLT_COUNT          = 0x1F4C768
BOLT_PICKUP_MASK           = 0x000000FFFFFFFFFF
PLANET_LOAD_ADDRESS        = 0x1F4C770
NEW_PLANET_START_LOAD_ADDR = 0x1F4A744
PLANET_LOAD_IDLE_VALUE     = 0xFFFFFFFF
CONTROLLER_PAUSE_SELECT_ADDRESS = 0xF7F414
CONTROLLER_BUTTONS_ADDRESS      = 0xF7F415

QUICK_SELECT_BASE          = 0x1F4B364
SKIN_BASE                  = 0x1F4B45A
CHALLENGE_MODE_BASE        = 0x1F4C778

TRANSITION_GATE_ADDRESS    = 0x1EDDAD4
LOADING_PLANET_ADDRESS     = 0x1EDDAE4

CURRENT_WEAPON_IN_VENDOR   = 0x1F4AB8C
WEAPON_VENDOR_SLOTS        = 0x1F4ABE4
WEAPON_VENDOR_ITEMS        = 0x1F4AB80

POKITARU_RYLLUS_ALT_TRIGGER = 0x2F9CC6

PLAYER_STATE  = 0xF805C0
PLAYER_HEALTH = 0xF80E2C

@dataclass(frozen=True)
class GhostRatchetPlanetAddresses:
    """Per-planet addresses for the Ghost Ratchet feature (see core/ghost_ratchet.py).
    trigger arms the spawn and is a separate address from ghost_base, not an offset within it."""
    player_position: int
    ghost_base: int
    trigger: int


GHOST_RATCHET_ADDRESSES: dict[int, GhostRatchetPlanetAddresses] = {
    0x01: GhostRatchetPlanetAddresses(
        player_position=0x2E62E0,
        ghost_base=0x2F4144,
        trigger=0x2CD554,
    ),
    0x02: GhostRatchetPlanetAddresses(
        player_position=0x5BAB00,
        ghost_base=0x5C6E64,
        trigger=0x5A8D34,
    ),
    0x03: GhostRatchetPlanetAddresses(
        player_position=0x50E8A0,
        ghost_base=0x51EC84,
        trigger=0x4F3934,
    ),
    0x04: GhostRatchetPlanetAddresses(
        player_position=0x1E65B0,
        ghost_base=0x1F3A94,
        trigger=0x1CFB8C,
    ),
    0x05: GhostRatchetPlanetAddresses(
        player_position=0x20BFF0,
        ghost_base=0x2143D4,
        trigger=0x1F77E8,
    ),
    0x06: GhostRatchetPlanetAddresses(
        player_position=0x480E10,
        ghost_base=0x48E0F4,
        trigger=0x46E8EC,
    ),
    0x07: GhostRatchetPlanetAddresses(
        player_position=0x482010,
        ghost_base=0x48D474,
        trigger=0x471B04,
    ),
    0x08: GhostRatchetPlanetAddresses(
        player_position=0x2FFB00,
        ghost_base=0x32EB64,
        trigger=0x2F4964,
    ),
    0x09: GhostRatchetPlanetAddresses(
        player_position=0x3E4F30,
        ghost_base=0x3EF894,
        trigger=0x3CE028,
    ),
    0x0A: GhostRatchetPlanetAddresses(
        player_position=0x3E0990,
        ghost_base=0x404774,
        trigger=0x3D9A58,
    ),
    0x17: GhostRatchetPlanetAddresses(
        player_position=0x45F290,
        ghost_base=0x47CBF4,
        trigger=0x45A454,
    ),
}

PLAYER_HEALTH_EXP = 0x1F4C774

PLANET_UNLOCK_ADDRESSES: dict[str, int] = {
    "POKITARU":      0x1F4C661,
    "RYLLUS":        0x1F4C662,
    "KALIDON":       0x1F4C663,
    "METALIS":       0x1F4C664,
    "DREAMTIME":     0x1F4C665,
    "OUTPOST_OMEGA": 0x1F4C666,
    "CHALLAX":       0x1F4C667,
    "DAYNI_MOON":    0x1F4C668,
    "INSIDE_CLANK":  0x1F4C669,
    "QUODRONA":      0x1F4C66A,
}
PLANET_PROGRESS_BASE = PLANET_UNLOCK_ADDRESSES["POKITARU"]
BRIGHTNESS_ADDRESS = 0x1EF1056
DREAMTIME_EFFECT = 0x1EF1058

SHRINK_RAY_GATE_ADDRESS: int = 0x1F4B40E

SHRINK_RAY_SKIP_ADDRESSES: dict[str, int] = {}

STATIC_TEXT_BUFFER: int = 0x1F649D0

PLANET_STATE_OFFSET: int = 0x11


@dataclass(frozen=True)
class PlanetAddresses:
    name:          str
    player_state:  int
    player_health: int
    menu:             int | None = None
    preload_menu:     int | None = None
    weapon_array:     int | None = None
    mission:          int | None = None
    vendor_prompt_id:     int | None = None
    clank_challenge_base: int | None = None
    skyboard_base:        int | None = None
    small_text_box:       int | None = None
    multi_line_text_box:  int | None = None
    controller_pause_select: int | None = None
    controller_pause_select_v2: int | None = None
    weapon_cycler_apply:   int | None = None
    weapon_cycler_state:   int | None = None
    weapon_cycler_current: int | None = None
    weapon_cycler_stored:  int | None = None
    max_health: int | None = None


PLANET_ADDRESSES: dict[int, PlanetAddresses] = {
    0x01: PlanetAddresses("Pokitaru",        0xF805C0, 0xF80E2C, menu=0x1073DC0, preload_menu=0xF4C8C0, weapon_array=0xF3EA17, mission=0x1F4B3C4, vendor_prompt_id=0xBF48, small_text_box=0xF479E8, multi_line_text_box=0xF47B28, controller_pause_select=0xF80594, controller_pause_select_v2=0xF866C2, weapon_cycler_apply=0xF80E80, weapon_cycler_state=0xF80E84, weapon_cycler_current=0xF80E60, weapon_cycler_stored=0xF80E6C, max_health=0xF80E30),
    0x02: PlanetAddresses("Ryllus",          0xF7F2D0, 0xF7FB3C, menu=0x1072AC0, preload_menu=0xF49080, weapon_array=0xF3AE97, mission=0x1F4B3C6, vendor_prompt_id=0xBF35, small_text_box=0xF441A8, multi_line_text_box=0xF442E8, controller_pause_select=0xF7F2A4, controller_pause_select_v2=0xF853C2, weapon_cycler_apply=0xF7FB90, weapon_cycler_state=0xF7FB94, weapon_cycler_current=0xF7FB70, weapon_cycler_stored=0xF7FB7C, max_health=0xF7FB40),
    0x03: PlanetAddresses("Kalidon",         0xF7F440, 0xF7FCAC, menu=0x1072C40, preload_menu=0xF48F40, weapon_array=0xF3B097, mission=0x1F4B3C8, vendor_prompt_id=0x3F37, skyboard_base=0x1F4B407, small_text_box=0xF44068, multi_line_text_box=0xF441A8, controller_pause_select=0xF7F414, controller_pause_select_v2=0xF85542, weapon_cycler_apply=0xF7FD00, weapon_cycler_state=0xF7FD04, weapon_cycler_current=0xF7FCE0, weapon_cycler_stored=0xF7FCEC, max_health=0xF7FCB0),
    0x04: PlanetAddresses("Metalis",         0xF7EDD0, 0xF7F63C, menu=0x10725C0, preload_menu=0xF49D80, weapon_array=0xF3BB97, mission=0x1F4B3CA, vendor_prompt_id=0x3F30, clank_challenge_base=0x1F4B3DB, small_text_box=0xF44EA8, multi_line_text_box=0xF44FE8, controller_pause_select=0xF7EDA4, controller_pause_select_v2=0xF84EC2, weapon_cycler_apply=0xF7F690, weapon_cycler_state=0xF7F694, weapon_cycler_current=0xF7F670, weapon_cycler_stored=0xF7F67C, max_health=0xF7F640),
    0x05: PlanetAddresses("Dreamtime",       0xF762C0, 0xF76B2C, menu=0x1069C80, preload_menu=0xF45C40, weapon_array=0xF37D97, mission=0x1F4B3CC, vendor_prompt_id=0x7FA7, small_text_box=0xF40D68, multi_line_text_box=0xF40EA8, controller_pause_select=0xF76294, controller_pause_select_v2=0xF7C582, weapon_cycler_apply=0xF76B80, weapon_cycler_state=0xF76B84, weapon_cycler_current=0xF76B60, weapon_cycler_stored=0xF76B6C, max_health=0xF76B30),
    0x06: PlanetAddresses("Outpost Omega",   0xF81B40, 0xF823AC, menu=0x1075340, preload_menu=0xF4D040, weapon_array=0xF42117, mission=0x1F4B3CE, skyboard_base=0x1F4B409, controller_pause_select=0xF7F414, controller_pause_select_v2=0xF87C42, weapon_cycler_apply=0xF82400, weapon_cycler_state=0xF82404, weapon_cycler_current=0xF823E0, weapon_cycler_stored=0xF823EC, max_health=0xF823B0),
    0x07: PlanetAddresses("Challax",         0xF806C0, 0xF80F2C, menu=0x1073EC0, preload_menu=0xF4B3C0, weapon_array=0xF3D517, mission=0x1F4B3D0, vendor_prompt_id=0xBF49, small_text_box=0xF464E8, multi_line_text_box=0xF46628, controller_pause_select=0xF80694, controller_pause_select_v2=0xF867C2, weapon_cycler_apply=0xF80F80, weapon_cycler_state=0xF80F84, weapon_cycler_current=0xF80F60, weapon_cycler_stored=0xF80F6C, max_health=0xF80F30),
    0x08: PlanetAddresses("Dayni Moon",      0xF79850, 0xF7A0BC, menu=0x106D040, preload_menu=0xF3F780, weapon_array=0xF31597, mission=0x1F4B3D2, vendor_prompt_id=0x3FDB, clank_challenge_base=0x1F4B3F3, small_text_box=0xF3A8A8, multi_line_text_box=0xF3A9E8, controller_pause_select=0xF79824, controller_pause_select_v2=0xF7F942, weapon_cycler_apply=0xF7A110, weapon_cycler_state=0xF7A114, weapon_cycler_current=0xF7A0F0, weapon_cycler_stored=0xF7A0FC, max_health=0xF7A0C0),
    0x09: PlanetAddresses("Inside Clank",    0xF82540, 0xF82DAC, menu=0x1075D40, preload_menu=0xF50EC0, weapon_array=0xF43017, mission=0x1F4B3D4, vendor_prompt_id=0x3F68, small_text_box=0xF4BFE8, multi_line_text_box=0xF4C128, controller_pause_select=0xF82514, controller_pause_select_v2=0xF88642, weapon_cycler_apply=0xF82E00, weapon_cycler_state=0xF82E04, weapon_cycler_current=0xF82DE0, weapon_cycler_stored=0xF82DEC, max_health=0xF82DB0),
    0x0A: PlanetAddresses("Quodrona",        0xF809C0, 0xF8122C, menu=0x10741C0, preload_menu=0xF4C8C0, weapon_array=0xF3EA17, mission=0x1F4B3D6, vendor_prompt_id=0xBF4C, small_text_box=0xF479E8, multi_line_text_box=0xF47B28, controller_pause_select=0xF80994, controller_pause_select_v2=0xF86AC2, weapon_cycler_apply=0xF81280, weapon_cycler_state=0xF81284, weapon_cycler_current=0xF81260, weapon_cycler_stored=0xF8126C, max_health=0xF81230),
    0x17: PlanetAddresses("Outpost Omega 2", 0xF82A40, 0xF823AC, menu=0x107A200, preload_menu=0xF54CC0, weapon_array=0xF46E17,                      vendor_prompt_id=0x3F37, small_text_box=0xF4FDE8, multi_line_text_box=0xF4FF28, controller_pause_select=0xF82A14, controller_pause_select_v2=0xF8CB42, max_health=0xF823B0),
}
