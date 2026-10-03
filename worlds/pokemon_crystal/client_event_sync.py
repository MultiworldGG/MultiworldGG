"""Co-op event flag syncing between players sharing a slot."""

from .data import data

SYNC_EVENT_FLAGS = [
    "EVENT_BEAT_FALKNER",
    "EVENT_BEAT_BUGSY",
    "EVENT_BEAT_WHITNEY",
    "EVENT_BEAT_MORTY",
    "EVENT_BEAT_JASMINE",
    "EVENT_BEAT_CHUCK",
    "EVENT_BEAT_PRYCE",
    "EVENT_BEAT_CLAIR",
    "EVENT_BEAT_BROCK",
    "EVENT_BEAT_MISTY",
    "EVENT_BEAT_LTSURGE",
    "EVENT_BEAT_ERIKA",
    "EVENT_BEAT_JANINE",
    "EVENT_BEAT_SABRINA",
    "EVENT_BEAT_BLAINE",
    "EVENT_BEAT_BLUE",

    "EVENT_CLEARED_SLOWPOKE_WELL",
    "EVENT_HERDED_FARFETCHD",
    "EVENT_RESTORED_POWER_TO_KANTO",
    "EVENT_JASMINE_RETURNED_TO_GYM",
    "EVENT_CLEARED_ROCKET_HIDEOUT",
    "EVENT_CLEARED_RADIO_TOWER",
    "EVENT_BLUE_GYM_TRACKER",
    "EVENT_SAW_SUICUNE_AT_CIANWOOD_CITY",
    "EVENT_SAW_SUICUNE_ON_ROUTE_42",
    "EVENT_SAW_SUICUNE_ON_ROUTE_36",
    "EVENT_RELEASED_THE_BEASTS",
    "EVENT_GAVE_KENYA",
    "EVENT_BILL_ACTIVATED_TIME_CAPSULE",
    "EVENT_GOT_TOGEPI_EGG_FROM_ELMS_AIDE",
    "EVENT_RETURNED_MACHINE_PART",
    "EVENT_EAST_WEST_UNDERGROUND_OPEN",
    "EVENT_ROUTE_5_6_POKEFAN_M_BLOCKS_UNDERGROUND_PATH",
    "EVENT_HEALED_MOOMOO",

    "EVENT_BEAT_RIVAL_IN_MT_MOON",
    "EVENT_GOT_MYSTERY_EGG_FROM_MR_POKEMON",
    "EVENT_ROUTE_30_BATTLE",
    "EVENT_BEAT_ELITE_FOUR",

    "EVENT_KURT_RETURNED_GS_BALL",
    "EVENT_MISTY_RETURNED_TO_GYM",
    "EVENT_MET_ROCKET_GRUNT_AT_CERULEAN_GYM",
    "EVENT_MET_MANAGER_AT_POWER_PLANT",

    # Visited-region flags used as rematch tier gates.
    "EVENT_VISITED_GOLDENROD",
    "EVENT_VISITED_OLIVINE",
    "EVENT_VISITED_ECRUTEAK",
    "EVENT_VISITED_MAHOGANY",
    "EVENT_VISITED_LAKE_OF_RAGE",
    "EVENT_VISITED_CIANWOOD",
    "EVENT_VISITED_BLACKTHORN",

    "EVENT_CINNABAR_ROCKS_CLEARED",

    "EVENT_MET_KURT",
    "EVENT_AZALEA_TOWN_SLOWPOKETAIL_ROCKET",
    "EVENT_GOT_HM01_CUT",

    "EVENT_LEARNED_HAIL_GIOVANNI",
    "EVENT_FAST_SHIP_FOUND_GIRL",
    "EVENT_BEAT_ROCKET_GRUNTF_5",
    "EVENT_BEAT_ROCKET_GRUNTM_28",

    "EVENT_SHOWED_LICKITUNG_TO_BILLS_GRANDPA",
    "EVENT_SHOWED_ODDISH_TO_BILLS_GRANDPA",
    "EVENT_SHOWED_STARYU_TO_BILLS_GRANDPA",
    "EVENT_SHOWED_GROWLITHE_VULPIX_TO_BILLS_GRANDPA",
    "EVENT_SHOWED_PICHU_TO_BILLS_GRANDPA",

    "EVENT_TALKED_TO_MOM_AFTER_MYSTERY_EGG_QUEST",

    "EVENT_DECIDED_TO_HELP_LANCE",

    "EVENT_USED_THE_CARD_KEY_IN_THE_RADIO_TOWER",

    "EVENT_JASMINE_EXPLAINED_AMPHYS_SICKNESS",
]

E4_DOOR_SYNC_EVENT_FLAGS = [
    "EVENT_BEAT_ELITE_4_WILL",
    "EVENT_BEAT_ELITE_4_KOGA",
    "EVENT_BEAT_ELITE_4_BRUNO",
    "EVENT_BEAT_ELITE_4_KAREN",
    "EVENT_WILLS_ROOM_EXIT_OPEN",
    "EVENT_KOGAS_ROOM_EXIT_OPEN",
    "EVENT_BRUNOS_ROOM_EXIT_OPEN",
    "EVENT_KARENS_ROOM_EXIT_OPEN",
]

def build_sync_layout(flags: list[str]) -> dict[str, int]:
    """Map each sync flag name to its bitfield position."""
    return {flag_name: bit for bit, flag_name in enumerate(flags)}


SYNC_LAYOUT = build_sync_layout(SYNC_EVENT_FLAGS)
SYNC_EVENTS_FLAG_MAP = {data.event_flags[event]: event for event in SYNC_LAYOUT}

E4_DOOR_SYNC_LAYOUT = build_sync_layout(E4_DOOR_SYNC_EVENT_FLAGS)
E4_DOOR_SYNC_FLAG_MAP = {data.event_flags[event]: event for event in E4_DOOR_SYNC_LAYOUT}

SYNC_GOAL_FLAGS = [
    "EVENT_BEAT_ELITE_FOUR",
    "EVENT_BEAT_RED",
    "EVENT_OBTAINED_DIPLOMA",
    "EVENT_BEAT_CHERRYGROVE_RIVAL",
    "EVENT_BEAT_AZALEA_RIVAL",
    "EVENT_RIVAL_BURNED_TOWER",
    "EVENT_BEAT_GOLDENROD_UNDERGROUND_RIVAL",
    "EVENT_BEAT_VICTORY_ROAD_RIVAL",
    "EVENT_BEAT_RIVAL_IN_MT_MOON",
    "EVENT_BEAT_RIVAL_IN_INDIGO_PLATEAU",
    "EVENT_CLEARED_SLOWPOKE_WELL",
    "EVENT_CLEARED_ROCKET_HIDEOUT",
    "EVENT_BEAT_ROCKET_EXECUTIVEM_3",
    "EVENT_CLEARED_RADIO_TOWER",
    "EVENT_DEFEATED_ROUTE_24_ROCKET",
    "EVENT_GOT_ALL_UNOWN",
]

SYNC_GOAL_FLAG_MAP = {data.event_flags[event]: event for event in SYNC_GOAL_FLAGS}
SYNC_GOAL_LAYOUT = build_sync_layout(SYNC_GOAL_FLAGS)


def detect_sync_events(flag_bytes: bytes, flag_map: dict[int, str] = SYNC_EVENTS_FLAG_MAP) -> dict[str, bool]:
    """Parse event flag bytes from game RAM into a sync events dict."""
    local_sync_events = {flag_name: False for flag_name in flag_map.values()}
    for byte_i, byte in enumerate(flag_bytes):
        for i in range(8):
            location_id = byte_i * 8 + i
            if byte & (1 << i):
                if location_id in flag_map:
                    local_sync_events[flag_map[location_id]] = True
    return local_sync_events


def encode_sync_bitfield(local_sync_events: dict[str, bool], layout: dict[str, int] = SYNC_LAYOUT) -> int:
    """Convert a sync events dict to a bitfield for server upload."""
    bitfield = 0
    for flag_name, bit in layout.items():
        if local_sync_events[flag_name]:
            bitfield |= 1 << bit
    return bitfield


def apply_remote_sync_events(flag_bytes: bytes, remote_sync_events: int,
                             layout: dict[str, int] = SYNC_LAYOUT) -> bytearray:
    """Apply a remote sync events bitfield onto a copy of the event flag bytes."""
    synced = bytearray(flag_bytes)
    for event, bit in layout.items():
        if remote_sync_events & (1 << bit):
            event_id = data.event_flags[event]
            synced[event_id // 8] |= 1 << (event_id % 8)
    return synced


def detect_sync_goal_events(flag_bytes: bytes) -> dict[str, bool]:
    """Parse event flag bytes from game RAM into a sync goal events dict."""
    return detect_sync_events(flag_bytes, SYNC_GOAL_FLAG_MAP)


def encode_sync_goal_bitfield(events: dict[str, bool]) -> int:
    """Convert a sync goal events dict to a bitfield for server upload."""
    return encode_sync_bitfield(events, SYNC_GOAL_LAYOUT)
