"""EU PS2 SCES-55019 map. See docs/research/eu_address_research.md.

Save data retains the US layout at 0x01F4AB00; resident loader and
per-level addresses differ. Unused/unverified preload and prompt fields
are deliberately left unset. GhostLink on first Outpost Omega is unmapped.
"""

from .us_addresses import PlanetAddresses, GhostRatchetPlanetAddresses

ARMOUR_BASE = 0x1f4b354
ARMOUR_SET_COLLECTED_ADDR = 0x1f4b442
TITANIUM_BOLT_BASE = 0x1f4b444
SKILL_POINTS_BASE = 0x1f4b437
CLANK_CHALLENGE_BASE = 0x1f4b3db
CLANK_CHALLENGE_SIZE = 0x2a
SKYBOARD_BASE = 0x1f4b407
CHEATS = 0x1f4c440
CURRENT_PLANET_ADDRESS = 0x1f4c76c
PLAYER_BOLT_COUNT = 0x1f4c768
BOLT_PICKUP_MASK = 0xffffffffff
PLANET_LOAD_ADDRESS = 0x1f4c770
NEW_PLANET_START_LOAD_ADDR = 0x1f4a744
PLANET_LOAD_IDLE_VALUE = 0xffffffff
QUICK_SELECT_BASE = 0x1f4b364
SKIN_BASE = 0x1f4b45a
CHALLENGE_MODE_BASE = 0x1f4c778
CURRENT_WEAPON_IN_VENDOR = 0x1f4ab8c
WEAPON_VENDOR_SLOTS = 0x1f4abe4
WEAPON_VENDOR_ITEMS = 0x1f4ab80
PLAYER_HEALTH_EXP = 0x1f4c774
PLANET_PROGRESS_BASE = 0x1f4c661
BRIGHTNESS_ADDRESS = 0x1ef1056
DREAMTIME_EFFECT = 0x1ef1058
SHRINK_RAY_GATE_ADDRESS = 0x1f4b40e
STATIC_TEXT_BUFFER = 0x1f649d0
PLANET_STATE_OFFSET = 0x11
TRANSITION_GATE_ADDRESS = 0x01EDD8D4
LOADING_PLANET_ADDRESS = 0x01EDD8E4
PLAYER_STATE = 0x00F80640
PLAYER_HEALTH = 0x00F80EAC
CONTROLLER_PAUSE_SELECT_ADDRESS = 0x00F7ED14
CONTROLLER_BUTTONS_ADDRESS = 0x00F7ED15
POKITARU_RYLLUS_ALT_TRIGGER = 0x002F9CC6

PLANET_UNLOCK_ADDRESSES = {'POKITARU': 32818785, 'RYLLUS': 32818786, 'KALIDON': 32818787, 'METALIS': 32818788, 'DREAMTIME': 32818789, 'OUTPOST_OMEGA': 32818790, 'CHALLAX': 32818791, 'DAYNI_MOON': 32818792, 'INSIDE_CLANK': 32818793, 'QUODRONA': 32818794}
SHRINK_RAY_SKIP_ADDRESSES = {}

PLANET_ADDRESSES = {
    0x01: PlanetAddresses(
        name='Pokitaru',
        player_state=0x00f80640,
        player_health=0x00f80eac,
        menu=0x01073e40,
        weapon_array=0x00f3ea97,
        small_text_box=0x00f47a68,
        multi_line_text_box=0x00f47ba8,
        controller_pause_select=0x00f80614,
        controller_pause_select_v2=0x00f86742,
        weapon_cycler_apply=0x00f80f00,
        weapon_cycler_state=0x00f80f04,
        weapon_cycler_current=0x00f80ee0,
        weapon_cycler_stored=0x00f80eec,
        max_health=0x00f80eb0,
        mission=0x01f4b3c4,
    ),
    0x02: PlanetAddresses(
        name='Ryllus',
        player_state=0x00f7f350,
        player_health=0x00f7fbbc,
        menu=0x01072b40,
        weapon_array=0x00f3af97,
        small_text_box=0x00f442a8,
        multi_line_text_box=0x00f443e8,
        controller_pause_select=0x00f7f324,
        controller_pause_select_v2=0x00f85442,
        weapon_cycler_apply=0x00f7fc10,
        weapon_cycler_state=0x00f7fc14,
        weapon_cycler_current=0x00f7fbf0,
        weapon_cycler_stored=0x00f7fbfc,
        max_health=0x00f7fbc0,
        mission=0x01f4b3c6,
    ),
    0x03: PlanetAddresses(
        name='Kalidon',
        player_state=0x00f7ed40,
        player_health=0x00f7f5ac,
        menu=0x01072540,
        weapon_array=0x00f3aa17,
        small_text_box=0x00f439e8,
        multi_line_text_box=0x00f43b28,
        controller_pause_select=0x00f7ed14,
        controller_pause_select_v2=0x00f84e42,
        weapon_cycler_apply=0x00f7f600,
        weapon_cycler_state=0x00f7f604,
        weapon_cycler_current=0x00f7f5e0,
        weapon_cycler_stored=0x00f7f5ec,
        max_health=0x00f7f5b0,
        mission=0x01f4b3c8,
        skyboard_base=0x01f4b407,
    ),
    0x04: PlanetAddresses(
        name='Metalis',
        player_state=0x00f7e6d0,
        player_health=0x00f7ef3c,
        menu=0x01071ec0,
        weapon_array=0x00f3b497,
        small_text_box=0x00f447a8,
        multi_line_text_box=0x00f448e8,
        controller_pause_select=0x00f7e6a4,
        controller_pause_select_v2=0x00f847c2,
        weapon_cycler_apply=0x00f7ef90,
        weapon_cycler_state=0x00f7ef94,
        weapon_cycler_current=0x00f7ef70,
        weapon_cycler_stored=0x00f7ef7c,
        max_health=0x00f7ef40,
        mission=0x01f4b3ca,
        clank_challenge_base=0x01f4b3db,
    ),
    0x05: PlanetAddresses(
        name='Dreamtime',
        player_state=0x00f75b40,
        player_health=0x00f763ac,
        menu=0x01069500,
        weapon_array=0x00f37697,
        small_text_box=0x00f40668,
        multi_line_text_box=0x00f407a8,
        controller_pause_select=0x00f75b14,
        controller_pause_select_v2=0x00f7be02,
        weapon_cycler_apply=0x00f76400,
        weapon_cycler_state=0x00f76404,
        weapon_cycler_current=0x00f763e0,
        weapon_cycler_stored=0x00f763ec,
        max_health=0x00f763b0,
        mission=0x01f4b3cc,
    ),
    0x06: PlanetAddresses(
        name='Outpost Omega',
        player_state=0x00f81440,
        player_health=0x00f81cac,
        menu=0x01074c40,
        weapon_array=0x00f41a97,
        small_text_box=0x00f4aa68,
        multi_line_text_box=0x00f4aba8,
        controller_pause_select=0x00f81414,
        controller_pause_select_v2=0x00f87542,
        max_health=0x00f81cb0,
        weapon_cycler_current=0x00f81ce0,
        weapon_cycler_stored=0x00f81cec,
        weapon_cycler_apply=0x00f81d00,
        weapon_cycler_state=0x00f81d04,
        mission=0x01f4b3ce,
        skyboard_base=0x01f4b409,
    ),
    0x07: PlanetAddresses(
        name='Challax',
        player_state=0x00f7ffc0,
        player_health=0x00f8082c,
        menu=0x010737c0,
        weapon_array=0x00f3ce97,
        small_text_box=0x00f45e68,
        multi_line_text_box=0x00f45fa8,
        controller_pause_select=0x00f7ff94,
        controller_pause_select_v2=0x00f860c2,
        weapon_cycler_apply=0x00f80880,
        weapon_cycler_state=0x00f80884,
        weapon_cycler_current=0x00f80860,
        weapon_cycler_stored=0x00f8086c,
        max_health=0x00f80830,
        mission=0x01f4b3d0,
    ),
    0x08: PlanetAddresses(
        name='Dayni Moon',
        player_state=0x00f79150,
        player_health=0x00f799bc,
        menu=0x0106c940,
        weapon_array=0x00f30f17,
        small_text_box=0x00f3a228,
        multi_line_text_box=0x00f3a368,
        controller_pause_select=0x00f79124,
        controller_pause_select_v2=0x00f7f242,
        weapon_cycler_apply=0x00f79a10,
        weapon_cycler_state=0x00f79a14,
        weapon_cycler_current=0x00f799f0,
        weapon_cycler_stored=0x00f799fc,
        max_health=0x00f799c0,
        mission=0x01f4b3d2,
        clank_challenge_base=0x01f4b3f3,
    ),
    0x09: PlanetAddresses(
        name='Inside Clank',
        player_state=0x00f81e40,
        player_health=0x00f826ac,
        menu=0x01075640,
        weapon_array=0x00f42917,
        small_text_box=0x00f4b8e8,
        multi_line_text_box=0x00f4ba28,
        controller_pause_select=0x00f81e14,
        controller_pause_select_v2=0x00f87f42,
        weapon_cycler_apply=0x00f82700,
        weapon_cycler_state=0x00f82704,
        weapon_cycler_current=0x00f826e0,
        weapon_cycler_stored=0x00f826ec,
        max_health=0x00f826b0,
        mission=0x01f4b3d4,
    ),
    0x0a: PlanetAddresses(
        name='Quodrona',
        player_state=0x00f802c0,
        player_health=0x00f80b2c,
        menu=0x01073ac0,
        weapon_array=0x00f3e317,
        small_text_box=0x00f472e8,
        multi_line_text_box=0x00f47428,
        controller_pause_select=0x00f80294,
        controller_pause_select_v2=0x00f863c2,
        weapon_cycler_apply=0x00f80b80,
        weapon_cycler_state=0x00f80b84,
        weapon_cycler_current=0x00f80b60,
        weapon_cycler_stored=0x00f80b6c,
        max_health=0x00f80b30,
        mission=0x01f4b3d6,
    ),
    0x17: PlanetAddresses(
        name='Outpost Omega 2',
        player_state=0x00f821c0,
        player_health=0x00f82a2c,
        menu=0x01079980,
        weapon_array=0x00f46617,
        small_text_box=0x00f4f5e8,
        multi_line_text_box=0x00f4f728,
        controller_pause_select=0x00f82194,
        controller_pause_select_v2=0x00f8c2c2,
        max_health=0x00f82a30,
        weapon_cycler_current=0x00f82a60,
        weapon_cycler_stored=0x00f82a6c,
        weapon_cycler_apply=0x00f82a80,
        weapon_cycler_state=0x00f82a84,
    ),
}

GHOST_RATCHET_ADDRESSES = {
    0x01: GhostRatchetPlanetAddresses(0x2e62e0, 0x2f4144, 0x2cd554),
    0x02: GhostRatchetPlanetAddresses(0x5bab00, 0x5c6e64, 0x5a8d34),
    0x03: GhostRatchetPlanetAddresses(0x50e8a0, 0x51ec84, 0x4f3934),
    0x04: GhostRatchetPlanetAddresses(0x1e65b0, 0x1f3a94, 0x1cfb8c),
    0x05: GhostRatchetPlanetAddresses(0x20bff0, 0x2143d4, 0x1f77e8),
    0x06: GhostRatchetPlanetAddresses(0x480e10, 0x48e0f4, 0x46e8ec),
    0x07: GhostRatchetPlanetAddresses(0x482010, 0x48d474, 0x471b04),
    0x08: GhostRatchetPlanetAddresses(0x2ffb00, 0x32eb64, 0x2f4964),
    0x09: GhostRatchetPlanetAddresses(0x3e4f30, 0x3ef894, 0x3ce028),
    0x0a: GhostRatchetPlanetAddresses(0x3e0990, 0x404774, 0x3d9a58),
    0x17: GhostRatchetPlanetAddresses(0x45f290, 0x47cbf4, 0x45a454),
}
