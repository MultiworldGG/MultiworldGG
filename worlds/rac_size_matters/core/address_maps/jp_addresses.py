"""JP PS2 SCPS-15120 addresses from captured resident and level code.
See docs/research/jp_address_research.md for validation limits.
"""

from .us_addresses import PlanetAddresses, GhostRatchetPlanetAddresses

ARMOUR_BASE = 0x1f4b194
ARMOUR_SET_COLLECTED_ADDR = 0x1f4b282
TITANIUM_BOLT_BASE = 0x1f4b284
SKILL_POINTS_BASE = 0x1f4b277
CLANK_CHALLENGE_BASE = 0x1f4b21b
CLANK_CHALLENGE_SIZE = 0x2a
SKYBOARD_BASE = 0x1f4b247
CHEATS = 0x1f4c280
CURRENT_PLANET_ADDRESS = 0x1f4c5ac
PLAYER_BOLT_COUNT = 0x1f4c5a8
BOLT_PICKUP_MASK = 0xffffffffff
PLANET_LOAD_ADDRESS = 0x1f4c5b0
NEW_PLANET_START_LOAD_ADDR = 0x1f4a584
PLANET_LOAD_IDLE_VALUE = 0xffffffff
CONTROLLER_PAUSE_SELECT_ADDRESS = 0xf7ed14
CONTROLLER_BUTTONS_ADDRESS = 0xf7ed15
QUICK_SELECT_BASE = 0x1f4b1a4
SKIN_BASE = 0x1f4b29a
CHALLENGE_MODE_BASE = 0x1f4c5b8
TRANSITION_GATE_ADDRESS = 0x1edf7f4
LOADING_PLANET_ADDRESS = 0x1edf804
CURRENT_WEAPON_IN_VENDOR = 0x1f4a9cc
WEAPON_VENDOR_SLOTS = 0x1f4aa24
WEAPON_VENDOR_ITEMS = 0x1f4a9c0
POKITARU_RYLLUS_ALT_TRIGGER = 0x2f9cc6
PLAYER_STATE = 0xf800c0
PLAYER_HEALTH = 0xf8092c
PLAYER_HEALTH_EXP = 0x1f4c5b4
PLANET_PROGRESS_BASE = 0x1f4c4a1
BRIGHTNESS_ADDRESS = 0x1ef2d76
DREAMTIME_EFFECT = 0x1ef2d78
SHRINK_RAY_GATE_ADDRESS = 0x1f4b24e
STATIC_TEXT_BUFFER = None
PLANET_STATE_OFFSET = 0x11

PLANET_UNLOCK_ADDRESSES = {
    'POKITARU': 0x1f4c4a1,
    'RYLLUS': 0x1f4c4a2,
    'KALIDON': 0x1f4c4a3,
    'METALIS': 0x1f4c4a4,
    'DREAMTIME': 0x1f4c4a5,
    'OUTPOST_OMEGA': 0x1f4c4a6,
    'CHALLAX': 0x1f4c4a7,
    'DAYNI_MOON': 0x1f4c4a8,
    'INSIDE_CLANK': 0x1f4c4a9,
    'QUODRONA': 0x1f4c4aa,
}
SHRINK_RAY_SKIP_ADDRESSES = {}

PLANET_ADDRESSES = {
    0x01: PlanetAddresses(
        name='Pokitaru',
        player_state=0xf800c0,
        player_health=0xf8092c,
        menu=0x10738c0,
        weapon_array=0xf3e497,
        mission=0x1f4b204,
        small_text_box=0xf47468,
        multi_line_text_box=0xf475a8,
        controller_pause_select=0xf80094,
        controller_pause_select_v2=0xf861c2,
        weapon_cycler_apply=0xf80980,
        weapon_cycler_state=0xf80984,
        weapon_cycler_current=0xf80960,
        weapon_cycler_stored=0xf8096c,
        max_health=0xf80930,
    ),
    0x02: PlanetAddresses(
        name='Ryllus',
        player_state=0xf7ee50,
        player_health=0xf7f6bc,
        menu=0x1072640,
        weapon_array=0xf3a997,
        mission=0x1f4b206,
        small_text_box=0xf43ca8,
        multi_line_text_box=0xf43de8,
        controller_pause_select=0xf7ee24,
        controller_pause_select_v2=0xf84f42,
        weapon_cycler_apply=0xf7f710,
        weapon_cycler_state=0xf7f714,
        weapon_cycler_current=0xf7f6f0,
        weapon_cycler_stored=0xf7f6fc,
        max_health=0xf7f6c0,
    ),
    0x03: PlanetAddresses(
        name='Kalidon',
        player_state=0xf7ed40,
        player_health=0xf7f5ac,
        menu=0x1072540,
        weapon_array=0xf3a997,
        mission=0x1f4b208,
        skyboard_base=0x1f4b247,
        small_text_box=0xf43968,
        multi_line_text_box=0xf43aa8,
        controller_pause_select=0xf7ed14,
        controller_pause_select_v2=0xf84e42,
        weapon_cycler_apply=0xf7f600,
        weapon_cycler_state=0xf7f604,
        weapon_cycler_current=0xf7f5e0,
        weapon_cycler_stored=0xf7f5ec,
        max_health=0xf7f5b0,
    ),
    0x04: PlanetAddresses(
        name='Metalis',
        player_state=0xf7e950,
        player_health=0xf7f1bc,
        menu=0x1072140,
        weapon_array=0xf3b697,
        mission=0x1f4b20a,
        clank_challenge_base=0x1f4b21b,
        small_text_box=0xf449a8,
        multi_line_text_box=0xf44ae8,
        controller_pause_select=0xf7e924,
        controller_pause_select_v2=0xf84a42,
        weapon_cycler_apply=0xf7f210,
        weapon_cycler_state=0xf7f214,
        weapon_cycler_current=0xf7f1f0,
        weapon_cycler_stored=0xf7f1fc,
        max_health=0xf7f1c0,
    ),
    0x05: PlanetAddresses(
        name='Dreamtime',
        player_state=0xf75d40,
        player_health=0xf765ac,
        menu=0x1069700,
        weapon_array=0xf37817,
        mission=0x1f4b20c,
        small_text_box=0xf407e8,
        multi_line_text_box=0xf40928,
        controller_pause_select=0xf75d14,
        controller_pause_select_v2=0xf7c002,
        weapon_cycler_apply=0xf76600,
        weapon_cycler_state=0xf76604,
        weapon_cycler_current=0xf765e0,
        weapon_cycler_stored=0xf765ec,
        max_health=0xf765b0,
    ),
    0x06: PlanetAddresses(
        name='Outpost Omega',
        player_state=0xf81c40,
        player_health=0xf824ac,
        menu=0x1075440,
        weapon_array=0xf42217,
        mission=0x1f4b20e,
        skyboard_base=0x1f4b249,
        small_text_box=0xf4b1e8,
        multi_line_text_box=0xf4b328,
        controller_pause_select=0xf81c14,
        controller_pause_select_v2=0xf87d42,
        weapon_cycler_apply=0xf82500,
        weapon_cycler_state=0xf82504,
        weapon_cycler_current=0xf824e0,
        weapon_cycler_stored=0xf824ec,
        max_health=0xf824b0,
    ),
    0x07: PlanetAddresses(
        name='Challax',
        player_state=0xf801c0,
        player_health=0xf80a2c,
        menu=0x10739c0,
        weapon_array=0xf3d017,
        mission=0x1f4b210,
        small_text_box=0xf45fe8,
        multi_line_text_box=0xf46128,
        controller_pause_select=0xf80194,
        controller_pause_select_v2=0xf862c2,
        weapon_cycler_apply=0xf80a80,
        weapon_cycler_state=0xf80a84,
        weapon_cycler_current=0xf80a60,
        weapon_cycler_stored=0xf80a6c,
        max_health=0xf80a30,
    ),
    0x08: PlanetAddresses(
        name='Dayni Moon',
        player_state=0xf793d0,
        player_health=0xf79c3c,
        menu=0x106cbc0,
        weapon_array=0xf31097,
        mission=0x1f4b212,
        clank_challenge_base=0x1f4b233,
        small_text_box=0xf3a3a8,
        multi_line_text_box=0xf3a4e8,
        controller_pause_select=0xf793a4,
        controller_pause_select_v2=0xf7f4c2,
        weapon_cycler_apply=0xf79c90,
        weapon_cycler_state=0xf79c94,
        weapon_cycler_current=0xf79c70,
        weapon_cycler_stored=0xf79c7c,
        max_health=0xf79c40,
    ),
    0x09: PlanetAddresses(
        name='Inside Clank',
        player_state=0xf81bc0,
        player_health=0xf8242c,
        menu=0x10753c0,
        weapon_array=0xf42697,
        mission=0x1f4b214,
        small_text_box=0xf4b668,
        multi_line_text_box=0xf4b7a8,
        controller_pause_select=0xf81b94,
        controller_pause_select_v2=0xf87cc2,
        weapon_cycler_apply=0xf82480,
        weapon_cycler_state=0xf82484,
        weapon_cycler_current=0xf82460,
        weapon_cycler_stored=0xf8246c,
        max_health=0xf82430,
    ),
    0x0A: PlanetAddresses(
        name='Quodrona',
        player_state=0xf804c0,
        player_health=0xf80d2c,
        menu=0x1073cc0,
        weapon_array=0xf3e517,
        mission=0x1f4b216,
        small_text_box=0xf474e8,
        multi_line_text_box=0xf47628,
        controller_pause_select=0xf80494,
        controller_pause_select_v2=0xf865c2,
        weapon_cycler_apply=0xf80d80,
        weapon_cycler_state=0xf80d84,
        weapon_cycler_current=0xf80d60,
        weapon_cycler_stored=0xf80d6c,
        max_health=0xf80d30,
    ),
    0x17: PlanetAddresses(
        name='Outpost Omega 2',
        player_state=0xf7fac0,
        player_health=0xf8032c,
        menu=0x10772c0,
        weapon_array=0xf43497,
        small_text_box=0xf4c468,
        multi_line_text_box=0xf4c5a8,
        controller_pause_select=0xf7fa94,
        controller_pause_select_v2=0xf89bc2,
        weapon_cycler_apply=0xf80380,
        weapon_cycler_state=0xf80384,
        weapon_cycler_current=0xf80360,
        weapon_cycler_stored=0xf8036c,
        max_health=0xf80330,
    ),
}

# JP ghost entity locations have not yet been validated.
GHOST_RATCHET_ADDRESSES = {
    0x01: GhostRatchetPlanetAddresses(0x2e62e0, 0x2f4144, 0x2cd554),
    0x02: GhostRatchetPlanetAddresses(0x5bab10, 0x5c6e74, 0x5a8d34),
    0x03: GhostRatchetPlanetAddresses(0x50e9a0, 0x51ed84, 0x4f3a34),
    0x04: GhostRatchetPlanetAddresses(0x1e65b0, 0x1f3a94, 0x1cfb8c),
    0x05: GhostRatchetPlanetAddresses(0x20bff0, 0x2143d4, 0x1f77e8),
    0x06: GhostRatchetPlanetAddresses(0x480e10, 0x48e0f4, 0x46e8ec),
    0x07: GhostRatchetPlanetAddresses(0x482010, 0x48d474, 0x471b04),
    0x08: GhostRatchetPlanetAddresses(0x2ffb00, 0x32eb64, 0x2f4964),
    0x09: GhostRatchetPlanetAddresses(0x3e4f30, 0x3ef894, 0x3ce028),
    0x0a: GhostRatchetPlanetAddresses(0x3e0990, 0x404774, 0x3d9a58),
    0x17: GhostRatchetPlanetAddresses(0x45f8c0, 0x47d224, 0x45a764),
}
