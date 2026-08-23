from ..Subclasses import STTransition, EntranceGroups

def event(reg1:str, reg2: str="") -> dict:
    return {
        "two_way": False,
        "entrance_region": reg1,
        "exit_region": reg2 if reg2 else reg1 + " event",
        "entrance": (0x0, 0x0, 0xF),
        "type": EntranceGroups.EVENT,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE
    }

def silent_event(reg1: str, reg2: str, reverse_entrance=""):
    return {
        "return_name": reverse_entrance if reverse_entrance else f"{reg2} -> {reg1}",
        "two_way": False,
        "entrance_region": reg1,
        "exit_region": reg2,
        "extra_data": {"silent_event": True},
        "entrance": (0x0, 0x0, 0xF),
        "type": EntranceGroups.EVENT,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE
    }

# For adding entrance data. Generates an object for both directions from each entry
ENTRANCE_DATA = {
    # "Name": {
    #   "return_name": str. what to call the vanilla connecting entrance that generates automatically
    #   "entrance": tuple[int, int, int], stage room entrance. If you come from entrance
    #   "exit": tuple[int, int, int], stage room entrance. What the vanilla game sends you on entering
    #   "entrance_region": str. logic region that the entrance is in (only used for ER)
    #   "exit_region": str. logic region it leads to in (only used for ER)
    #   "coords": tuple[int, int, int]. x, y, z. Where to place link on a continuous transition. y value is also used
    #       to differentiate transitions at different heights
    #   "extra_data": dict[str: int]. additional coordinate data for continuous boundaries, like "x_max" etc.
    #  There are hooks for doing special things with extra data.
    #   "type": EntranceGroup. Entrance group entrance type (house, cave, station etc)
    #   "direction": EntranceGroup. Entrance group direction
    #   "two_way": bool=True. generates a reciprocal entrance, also used for ER generation
    # }

    # Outset
    "Outset West House": {
        "return_name": "Niko's House Exit",
        "exit": (0x2F, 0xA, 1),
        "entrance": (0x2F, 0x0, 1),
        "exit_region": "niko's house",
        "entrance_region": "outset village",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Outset East House": {
        "return_name": "Mary's House Exit",
        "exit": (0x2F, 0xC, 0),
        "entrance": (0x2F, 0x0, 3),
        "exit_region": "mary's house",
        "entrance_region": "outset village",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Outset Alfonzo's Workshop": {
        "return_name": "Alfonzo's Workshop Exit",
        "exit": (0x2F, 0xB, 0),
        "entrance": (0x2F, 0x0, 2),
        "exit_region": "train workshop",
        "entrance_region": "outset village",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },

    # Mayscore
    "Mayscore North House": {
        "return_name": "Dovok's House Exit",
        "exit": (0x2A, 0x4, 0),
        "entrance": (0x2A, 0x0, 4),
        "exit_region": "dovok's house",
        "entrance_region": "mayscore",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Mayscore NW House": {
        "return_name": "Morris' House Exit",
        "exit": (0x2A, 0x3, 0),
        "entrance": (0x2A, 0x0, 3),
        "exit_region": "morris' house",
        "entrance_region": "mayscore",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Mayscore NE House": {
        "return_name": "Wood's House Exit",
        "exit": (0x2A, 0x2, 0),
        "entrance": (0x2A, 0x0, 2),
        "exit_region": "wood's house",
        "entrance_region": "mayscore",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Mayscore Shop": {
        "return_name": "Uriko's Shop Exit",
        "exit": (0x2A, 0x5, 0),
        "entrance": (0x2A, 0x0, 1),
        "exit_region": "uriko's shop",
        "entrance_region": "mayscore",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Mayscore North": {
        "return_name": "Mayscore Forest South",
        "exit": (0x38, 0x0, 0),
        "entrance": (0x2A, 0x0, 5),
        "exit_region": "mayscore north",
        "entrance_region": "mayscore",
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },

    # Castle Town
    "Castle Town North": {
        "return_name": "Hyrule Castle Courtyard South",
        "exit": (0x28, 0x0, 0),
        "entrance": (0x29, 0x0, 1),
        "exit_region": "hyrule castle courtyard",
        "entrance_region": "castle town",
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Castle Town West House": {
        "return_name": "Mona's House Exit",
        "exit": (0x29, 0xc, 0),
        "entrance": (0x29, 0x0, 5),
        "exit_region": "mona's house",
        "entrance_region": "castle town",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Castle Town NW House": {
        "return_name": "Lucia's House Exit",
        "exit": (0x29, 0xE, 0),
        "entrance": (0x29, 0x0, 7),
        "exit_region": "lucia's house",
        "entrance_region": "castle town",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Castle Town Shop": {
        "return_name": "Shitate's Shop Exit",
        "exit": (0x29, 0xA, 0),
        "entrance": (0x29, 0x0, 3),
        "exit_region": "shitate's shop",
        "entrance_region": "castle town",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Castle Town NE House": {
        "return_name": "Milo's House Exit",
        "exit": (0x29, 0xD, 0),
        "entrance": (0x29, 0x0, 6),
        "exit_region": "milo's house",
        "entrance_region": "castle town",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Castle Town Take 'em all On": {
        "return_name": "Take 'em all On Lobby Exit",
        "exit": (0x29, 0xB, 0),
        "entrance": (0x29, 0x0, 4),
        "exit_region": "teao",
        "entrance_region": "castle town",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },

    # Hyrule Castle
    "Hyrule Castle Courtyard Entrance": {
        "return_name": "Hyrule Castle 1F Exit",
        "exit": (0x28, 0x1, 0),
        "entrance": (0x28, 0x0, 1),
        "exit_region": "hyrule castle 1f",
        "entrance_region": "hyrule castle courtyard",
        "type": EntranceGroups.CASTLE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Hyrule Castle 1F NW": {
        "return_name": "Hyrule Castle Infirmary Exit",
        "exit": (0x28, 0x3, 1),
        "entrance": (0x28, 0x1, 3),
        "exit_region": "hyrule castle infirmary",
        "entrance_region": "hyrule castle 1f",
        "type": EntranceGroups.CASTLE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Hyrule Castle 1F NE": {
        "return_name": "Hyrule Castle Barracks Exit",
        "exit": (0x28, 0x7, 0),
        "entrance": (0x28, 0x1, 2),
        "exit_region": "hyrule castle barracks",
        "entrance_region": "hyrule castle 1f",
        "type": EntranceGroups.CASTLE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Hyrule Castle 1F SE": {
        "return_name": "Hyrule Castle Roof SE",
        "exit": (0x28, 0x0, 2),
        "entrance": (0x28, 0x1, 4),
        "exit_region": "hyrule castle roof right",
        "entrance_region": "hyrule castle 1f",
        "type": EntranceGroups.CASTLE,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE
    },
    "Hyrule Castle 1F SW": {
        "return_name": "Hyrule Castle Roof SW",
        "exit": (0x28, 0x0, 3),
        "entrance": (0x28, 0x1, 5),
        "exit_region": "hyrule castle roof left",
        "entrance_region": "hyrule castle 1f",
        "type": EntranceGroups.CASTLE,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE
    },
    "Hyrule Castle 1F Main Staircase": {
        "return_name": "Hyrule Castle Throne Room Exit",
        "exit": (0x28, 0x6, 0),
        "entrance": (0x28, 0x1, 1),
        "exit_region": "hyrule castle throne room",
        "entrance_region": "hyrule castle 1f",
        "type": EntranceGroups.CASTLE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Hyrule Castle Roof Central Door": {
        "return_name": "Hyrule Castle 2F Central Exit",
        "exit": (0x28, 0x2, 1),
        "entrance": (0x28, 0x0, 4),
        "exit_region": "hyrule castle 2f",
        "entrance_region": "hyrule castle roof right",
        "type": EntranceGroups.CASTLE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Hyrule Castle Roof NE": {
        "return_name": "Hyrule Castle 2F NE Exit",
        "exit": (0x28, 0x2, 4),
        "entrance": (0x28, 0x0, 5),
        "exit_region": "hyrule castle 2f",
        "entrance_region": "hyrule castle ne ledge",
        "type": EntranceGroups.CASTLE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Hyrule Castle Zelda's Room Exit": {
        "return_name": "Hyrule Castle 2F NE Staircase",
        "exit": (0x28, 0x2, 3),
        "entrance": (0x28, 0x5, 0),
        "exit_region": "hyrule castle 2f",
        "entrance_region": "zelda's room",
        "type": EntranceGroups.CASTLE,
        "direction": EntranceGroups.DOWN,
        "island": EntranceGroups.NONE
    },
    "Hyrule Castle Throne Room NE": {
        "return_name": "Hyrule Castle 2F NE Door",
        "exit": (0x28, 0x2, 7),
        "entrance": (0x28, 0x6, 2),
        "exit_region": "hyrule castle 2f",
        "entrance_region": "hyrule castle throne room",
        "type": EntranceGroups.CASTLE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Hyrule Castle Roof NW": {
        "return_name": "Hyrule Castle 2F NW Exit",
        "exit": (0x28, 0x2, 5),
        "entrance": (0x28, 0x0, 6),
        "exit_region": "hyrule castle 2f",
        "entrance_region": "hyrule castle nw ledge",
        "type": EntranceGroups.CASTLE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Hyrule Castle Throne Room NW": {
        "return_name": "Hyrule Castle 2F NW Door",
        "exit": (0x28, 0x2, 6),
        "entrance": (0x28, 0x6, 1),
        "exit_region": "hyrule castle 2f left",
        "entrance_region": "hyrule castle throne room",
        "type": EntranceGroups.CASTLE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Hyrule Castle 1F Back Staircase": {
        "return_name": "Hyrule Castle 2F NW Staircase",
        "exit": (0x28, 0x2, 2),
        "entrance": (0x28, 0x1, 7),
        "exit_region": "hyrule castle 2f",
        "entrance_region": "hyrule castle backdoor",
        "type": EntranceGroups.CASTLE,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE
    },
    "Hyrule Castle 1F Back Exit": {
        "return_name": "Hyrule Castle Backyard Castle",
        "exit": (0x28, 0x4, 0),
        "entrance": (0x28, 0x1, 6),
        "exit_region": "hyrule castle backyard",
        "entrance_region": "hyrule castle backdoor",
        "type": EntranceGroups.CASTLE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },

    "Hyrule Castle Backyard Cave": {
        "return_name": "Tunnel to the Tower 1F Exit",
        "exit": (0x18, 0x0, 0),
        "entrance": (0x28, 0x4, 1),
        "exit_region": "tower tunnel 1f",
        "entrance_region": "hyrule castle backyard",
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Tunnel to the Tower 1F Staircase": {
        "return_name": "Tunnel to the Tower 2F Exit",
        "exit": (0x18, 0x1, 0),
        "entrance": (0x18, 0x0, 1),
        "entrance_region": "tower tunnel key door",
        "exit_region": "tower tunnel 2f",
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Tunnel to the Tower 2F Staircase": {
        "return_name": "Tunnel to the Tower 3F Exit",
        "exit": (0x18, 0x2, 0),
        "entrance": (0x18, 0x1, 1),
        "exit_region": "tower tunnel 3f",
        "entrance_region": "tower tunnel 2f door",
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },

    # FOS
    "Woodland Sanctuary Cave": {
        "return_name": "Gage's Sanctuary Exit",
        "entrance": (0x30, 0, 1),
        "exit": (0x30, 0x1, 0),
        "entrance_region": "woodland sanc door",
        "exit_region": "woodland sanc sanc",
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    # Snow realm
    "Anouki Village SW House": {
        "return_name": "Yefu's House Exit",
        "entrance": (0x2B, 0, 5),
        "exit": (0x2B, 0x5, 0),
        "entrance_region": "anouki village",
        "exit_region": "yefu's house",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Anouki Village S House": {
        "return_name": "Noko's House Exit",
        "entrance": (0x2B, 0, 4),
        "exit": (0x2B, 0x4, 0),
        "entrance_region": "anouki village",
        "exit_region": "noko's house",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Anouki Village SE House": {
        "return_name": "Bulu's House Exit",
        "entrance": (0x2B, 0, 3),
        "exit": (0x2B, 0x3, 0),
        "entrance_region": "anouki village",
        "exit_region": "bulu's house",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Anouki Village NE House": {
        "return_name": "Kofu's House Exit",
        "entrance": (0x2B, 0, 2),
        "exit": (0x2B, 0x2, 0),
        "entrance_region": "anouki village",
        "exit_region": "kofu's house",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Anouki Village NW House": {
        "return_name": "Yeko's House Exit",
        "entrance": (0x2B, 0, 6),
        "exit": (0x2B, 0x6, 0),
        "entrance_region": "anouki village",
        "exit_region": "yeko's house",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Anouki Village N House": {
        "return_name": "Honcho's House Exit",
        "entrance": (0x2B, 0, 1),
        "exit": (0x2B, 0x1, 0),
        "entrance_region": "anouki village",
        "exit_region": "honcho's house",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Anouki Village Bomb Cave": {
        "return_name": "Small Ice Puzzle Cave Exit",
        "entrance": (0x2B, 0, 7),
        "exit": (0x2B, 0x7, 0),
        "entrance_region": "anouki village",
        "exit_region": "ice block cave",
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },

    # Snowfall sanc
    "Snowfall Sanctuary Cave": {
        "return_name": "Head Statue Cave Exit",
        "entrance": (0x31, 0, 1),
        "exit": (0x31, 0x1, 0),
        "entrance_region": "snow sanc",
        "exit_region": "snow sanc cave",
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Head Statue Cave Door": {
        "return_name": "Steem's Sanctuary Exit",
        "entrance": (0x31, 1, 1),
        "exit": (0x31, 0x2, 0),
        "entrance_region": "snow sanc cave",
        "exit_region": "snow sanc sanc",
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Snowfall Sanctuary Shop": {
        "return_name": "Snowfall Supermarket Exit",
        "entrance": (0x31, 0, 2),
        "exit": (0x31, 0x3, 0),
        "entrance_region": "snow sanc",
        "exit_region": "snowfall supermarket",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    # Small Stations
    "Icy Spring Trailer": {
        "return_name": "Ferrus' Trailer Exit",
        "entrance": (0x35, 0, 1),
        "exit": (0x35, 0x1, 0),
        "entrance_region": "icyspring",
        "exit_region": "ferrus' trailer",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Bridge Worker's House": {
        "return_name": "Kenzo's House Exit",
        "entrance": (0x36, 0, 1),
        "exit": (0x36, 0x1, 0),
        "entrance_region": "bridge workers",
        "exit_region": "kenzo's house",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Slippery Station Cave": {
        "return_name": "Skating Rink Exit",
        "entrance": (0x3F, 0xA, 1),
        "exit": (0x3F, 0x6, 0),
        "entrance_region": "slippery",
        "exit_region": "skating rink",
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    # Snowdrift
    "Snowdrift Station Cave": {
        "return_name": "Snowdrift Cave Exit",
        "entrance": (0x3F, 0x0, 1),
        "exit": (0x3F, 0x1, 0),
        "entrance_region": "snowdrift",
        "exit_region": "snowdrift cave",
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Snowdrift Cave SE": {
        "return_name": "Octive Arena Exit",
        "entrance": (0x3F, 0x1, 1),
        "exit": (0x3F, 0x2, 0),
        "entrance_region": "snowdrift cave",
        "exit_region": "octive arena",
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE
    },
    "Snowdrift Cave NE": {
        "return_name": "Frostflame Cave Exit",
        "entrance": (0x3F, 0x1, 3),
        "exit": (0x3F, 0x3, 0),
        "entrance_region": "snowdrift cave",
        "exit_region": "frostflame cave",
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE
    },
    "Snowdrift Cave SW": {
        "return_name": "Small Skating Cave Exit",
        "entrance": (0x3F, 0x1, 2),
        "exit": (0x3F, 0x4, 0),
        "entrance_region": "snowdrift cave",
        "exit_region": "small skating",
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE
    },
    "Snowdrift Cave NW": {
        "return_name": "Big Ice Puzzle Cave Exit",
        "entrance": (0x3F, 0x1, 4),
        "exit": (0x3F, 0x5, 0),
        "entrance_region": "snowdrift cave",
        "exit_region": "big ice puzzle",
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE
    },

    # Trading post
    "Trading Post Shop": {
        "return_name": "Linebeck III's Shop Exit",
        "entrance": (0x37, 0x0, 1),
        "exit": (0x37, 0xA, 0),
        "entrance_region": "trading post",
        "exit_region": "linebeck's shop",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Trading Post South Cave": {
        "return_name": "Like-Like Tunnel South",
        "entrance": (0x37, 0x0, 2),
        "exit": (0x37, 0x1, 0),
        "entrance_region": "trading post",
        "exit_region": "trading post tunnel",
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Trading Post North Staircase": {
        "return_name": "Like-Like Tunnel North",
        "entrance": (0x37, 0x0, 3),
        "exit": (0x37, 0x1, 1),
        "entrance_region": "trading post north",
        "exit_region": "trading post tunnel",
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE
    },
    "Trading Post Island Cave": {
        "return_name": "Linebeck's Treasure's Cave Exit",
        "entrance": (0x37, 0x0, 4),
        "exit": (0x37, 0x2, 0),
        "entrance_region": "trading post island",
        "exit_region": "trading post cave",
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },

    # Papuzia
    "Papuzia NW House": {
        "return_name": "Fuku's House Exit",
        "entrance_region": "papuzia village",
        "exit_region": "fuku's house",
        "entrance": (0x2c, 0x0, 0x1),
        "exit": (0x2c, 0x1, 0x0),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Papuzia Wise One's House": {
        "return_name": "Wise One's House Exit",
        "entrance_region": "papuzia village",
        "exit_region": "wise one's house",
        "entrance": (0x2c, 0x0, 0x4),
        "exit": (0x2c, 0x4, 0x0),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Papuzia South House": {
        "return_name": "Orca's House Exit",
        "entrance_region": "papuzia village",
        "exit_region": "orca's house",
        "entrance": (0x2c, 0x0, 0x3),
        "exit": (0x2c, 0x3, 0x0),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Papuzia Shop": {
        "return_name": "Kogane's Shop Exit",
        "entrance_region": "papuzia village",
        "exit_region": "kogane's shop",
        "entrance": (0x2c, 0x0, 0x2),
        "exit": (0x2c, 0x2, 0x0),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Papuzia South": {
        "return_name": "Papuzia Archipelago North",
        "entrance_region": "papuzia village south",
        "exit_region": "papuzia archipelago north",
        "entrance": (0x2c, 0x0, 0x5),
        "exit": (0x39, 0x0, 0x0),
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.DOWN,
        "island": EntranceGroups.NONE
    },

    # Island Sanctuary
    "Island Sanctuary South Cave": {
        "return_name": "Crab Cave Exit",
        "entrance_region": "island sanc",
        "exit_region": "island sanc cave west",
        "entrance": (0x32, 0x0, 0x1),
        "exit": (0x32, 0x1, 0x0),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Island Sanctuary North Staircase": {
        "return_name": "Crab Cave Staircase",
        "entrance_region": "island sanc north",
        "exit_region": "island sanc cave east",
        "entrance": (0x32, 0x2, 0x0),
        "exit": (0x32, 0x1, 0x1),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE
    },
    "Island Sanctuary North Cave": {
        "return_name": "Carben's Sanctuary Exit",
        "entrance_region": "island sanc north",
        "exit_region": "island sanc sanc",
        "entrance": (0x32, 0x2, 0x2),
        "exit": (0x32, 0x4, 0x0),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Island Sanctuary South Peninsula": {
        "return_name": "Island Sanctuary North Peninsula",
        "entrance_region": "island sanc peninsula",
        "exit_region": "island sanc north",
        "entrance": (0x32, 0x0, 0x2),
        "exit": (0x32, 0x2, 0x1),
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },

    # Ocean Islands
    "Pirate Hideout Bomb Cave": {
        "return_name": "Treasure Cave Exit",
        "entrance_region": "pirate hideout",
        "exit_region": "pirate hideout secret cave",
        "entrance": (0x3A, 0x0, 0x3),
        "exit": (0x3A, 0x1, 0x0),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Pirate Hideout Game Cave": {
        "return_name": "Pirate Hangout Exit",
        "entrance_region": "pirate hideout",
        "exit_region": "pirate hangout",
        "entrance": (0x3A, 0x0, 0x1),
        "exit": (0x3B, 0x0, 0x0),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Lost at Sea Cave": {
        "return_name": "Lost at Sea Lobby Exit",
        "entrance_region": "las cliff",
        "exit_region": "las lobby",
        "entrance": (0x39, 0xA, 0x1),
        "exit": (0x39, 0xB, 0x0),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Dune Sanctuary Secret Staircase": {
        "return_name": "Sandy Tunnel Right Staircase",
        "entrance_region": "sand sanc",
        "exit_region": "sand sanc tunnel",
        "entrance": (0x34, 0x0, 0x1),
        "exit": (0x34, 0x1, 0x0),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE
    },
    "Rael's Sanctuary Exit": {
        "return_name": "Sandy Tunnel Left Entrance",
        "entrance_region": "sand sanc sanc",
        "exit_region": "sand sanc tunnel",
        "entrance": (0x34, 0x2, 0x0),
        "exit": (0x34, 0x1, 0x1),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },

    # Fire realm

    # Goron village
    "Goron Village West": {
        "return_name": "Goron Field East",
        "entrance_region": "goron village",
        "exit_region": "goron field",
        "entrance": (0x2e, 0x0, 0x3),
        "exit": (0x2d, 0x3, 0x1),
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.LEFT,
        "island": EntranceGroups.NONE
    },
    "Goron Field North": {
        "return_name": "Mountain Altar South",
        "entrance_region": "goron field north",
        "exit_region": "mountain altar",
        "entrance": (0x2d, 0x3, 0x2),
        "exit": (0x2d, 0x2, 0x1),
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },

    "Goron Village Shop": {
        "return_name": "Goron Shop Exit",
        "entrance_region": "goron village",
        "exit_region": "goron village shop",
        "entrance": (0x2e, 0x0, 0x2),
        "exit": (0x2e, 0x6, 0x1),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Goron Village SW House": {
        "return_name": "Goron 3 Pots House Exit",
        "entrance_region": "goron plaza",
        "exit_region": "goron house 3 pots",
        "entrance": (0x2e, 0x0, 0xc),
        "exit": (0x2e, 0xc, 0x1),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Goron Village Center House": {
        "return_name": "Kofu's New House Exit",
        "entrance_region": "goron plaza",
        "exit_region": "kofu's new house",
        "entrance": (0x2e, 0x0, 0xD),
        "exit": (0x2e, 0xD, 0x1),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Goron Village SE House": {
        "return_name": "Goron 2 Pots House Exit",
        "entrance_region": "goron plaza",
        "exit_region": "goron neighbour's house",
        "entrance": (0x2e, 0x0, 0xE),
        "exit": (0x2e, 0xE, 0x1),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Goron Village Elder's House": {
        "return_name": "Elder Goron House Exit",
        "entrance_region": "goron plaza",
        "exit_region": "goron elder's house",
        "entrance": (0x2e, 0x0, 0xA),
        "exit": (0x2e, 0xA, 0x1),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Goron Village NW House": {
        "return_name": "Mouldy Goron House Exit",
        "entrance_region": "goron plaza",
        "exit_region": "mouldy goron house",
        "entrance": (0x2e, 0x0, 0xB),
        "exit": (0x2e, 0xB, 0x1),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Goron Village East Lava House": {
        "return_name": "Lava Goron House Exit",
        "entrance_region": "comfy goron's doorstep",
        "exit_region": "comfy goron's house",
        "entrance": (0x2e, 0x0, 0xF),
        "exit": (0x2e, 0xF, 0x1),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },

    "Elder Goron House Cave": {
        "return_name": "Burning Tunnel West Exit",
        "entrance_region": "goron elder's house",
        "exit_region": "valley sanc tunnel west",
        "entrance": (0x2e, 0xA, 0x2),
        "exit": (0x2e, 0x1, 0x1),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Goron Village Enclave Staircase": {
        "return_name": "Burning Tunnel East Staircase",
        "entrance_region": "goron village north",
        "exit_region": "valley sanc tunnel east",
        "entrance": (0x2e, 0x0, 0x5),
        "exit": (0x2e, 0x1, 0x2),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE
    },
    "Goron Village Enclave North": {
        "return_name": "Valley Sanctuary South",
        "entrance_region": "goron village north",
        "exit_region": "valley sanc",
        "entrance": (0x2e, 0x0, 0x4),
        "exit": (0x33, 0x0, 0x1),
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Valley Sanctuary Cave": {
        "return_name": "Embrose's Sanctuary Exit",
        "entrance_region": "valley sanc door",
        "exit_region": "valley sanc sanc",
        "entrance": (0x33, 0x0, 0x2),
        "exit": (0x33, 0x3, 0x1),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },

    # Dark Ore Mine
    "Dark Ore Mine Left Cave": {
        "return_name": "Dark Ore Tunnels Left Exit",
        "entrance_region": "dark ore mine",
        "exit_region": "dark ore tunnels left",
        "entrance": (0x3D, 0x0, 0x3),
        "exit": (0x3D, 0x1, 0x2),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Dark Ore Mine Center Cave": {
        "return_name": "Dark Ore Tunnels Center Exit",
        "entrance_region": "dark ore mine",
        "exit_region": "dark ore tunnels mid",
        "entrance": (0x3D, 0x0, 0x2),
        "exit": (0x3D, 0x1, 0x1),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Dark Ore Mine Right Cave": {
        "return_name": "Dark Ore Tunnels Right Exit",
        "entrance_region": "dark ore mine",
        "exit_region": "dark ore tunnels right",
        "entrance": (0x3D, 0x0, 0x4),
        "exit": (0x3D, 0x1, 0x3),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },

    # Disorientation Station
    "Disorientation Station Cave": {
        "return_name": "Disorientation 5 Staircase",
        "entrance_region": "disorientation top",
        "exit_region": "d5",
        "entrance": (0x40, 0x0, 0x1),
        "exit": (0x40, 0x5, 0x5),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE
    },
    "D8 Up": {
        "return_name": "D2 Down",
        "entrance_region": "d8",
        "exit_region": "d2",
        "entrance": (0x40, 0x8, 0x3),
        "exit": (0x40, 0x2, 0x1),
        "type": EntranceGroups.DISORIENTATION,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    }
}

ENTRANCE_DATA |= {  # Horizontal
    f"D{i+3*j} Right": {
        "return_name": f"D{i+3*j+1} Left",
        "entrance_region": f"d{i+3*j}",
        "exit_region": f"d{i+3*j+1}",
        "entrance": (0x40, i+3*j, 0x4),
        "exit": (0x40, i+3*j+1, 0x2),
        "type": EntranceGroups.DISORIENTATION,
        "direction": EntranceGroups.RIGHT,
        "island": EntranceGroups.NONE
    } for i in range(1, 4) for j in range(3)
}

ENTRANCE_DATA |= { # Horizontal looping
    f"D{3+3*j} Right": {
        "return_name": f"D{1+3*j} Left",
        "entrance_region": f"d{3+3*j}",
        "exit_region": f"d{1+3*j}",
        "entrance": (0x40, 3+3*j, 0x4),
        "exit": (0x40, 3*j+1, 0x2),
        "type": EntranceGroups.DISORIENTATION,
        "direction": EntranceGroups.RIGHT,
        "island": EntranceGroups.NONE
    } for j in range(3)
}
ENTRANCE_DATA |= { # Vertical
    f"D{i+3*j} Up": {
        "return_name": f"D{i+3*j+3} Down",
        "entrance_region": f"d{i+3*j}",
        "exit_region": f"d{i+3*j+3}",
        "entrance": (0x40, i+3*j, 0x3),
        "exit": (0x40, i+3*j+3, 0x1),
        "type": EntranceGroups.DISORIENTATION,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    } for i in range(1, 4) for j in range(2)
}

ENTRANCE_DATA |= {
    # Ends of the Earth
    "Ends of the Earth Master Cave": {
        "return_name": "EotE 1 Exit",
        "entrance_region": "ends of the earth",
        "exit_region": "eote 1",
        "entrance": (0x41, 0x0, 0x2),
        "exit": (0x41, 0x1, 0x0),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Ends of the Earth Tempered Cave": {
        "return_name": "EotE 5 Exit",
        "entrance_region": "ends of the earth",
        "exit_region": "eote 5",
        "entrance": (0x41, 0x0, 0x1),
        "exit": (0x41, 0x5, 0x0),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Ends of the Earth Golden Cave": {
        "return_name": "EotE 9 Exit",
        "entrance_region": "ends of the earth",
        "exit_region": "eote 9",
        "entrance": (0x41, 0x0, 0x3),
        "exit": (0x41, 0x9, 0x0),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },

    "EotE 1 Lower Entrance": {
        "return_name": "EotE 2 Exit",
        "entrance_region": "eote 1",
        "exit_region": "eote 2",
        "entrance": (0x41, 0x1, 0x1),
        "exit": (0x41, 0x2, 0x0),
        "type": EntranceGroups.EOTE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "EotE 2 Door": {
        "return_name": "EotE 3 Exit",
        "entrance_region": "eote 2",
        "exit_region": "eote 3",
        "entrance": (0x41, 0x2, 0x1),
        "exit": (0x41, 0x3, 0x0),
        "type": EntranceGroups.EOTE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "EotE 3 Door": {
        "return_name": "EotE 4 Exit",
        "entrance_region": "eote 3",
        "exit_region": "eote 4",
        "entrance": (0x41, 0x3, 0x1),
        "exit": (0x41, 0x4, 0x0),
        "type": EntranceGroups.EOTE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "EotE 1 Upper Entrance": {
        "return_name": "EotE 4 Chest Exit",
        "entrance_region": "eote 1 chest",
        "exit_region": "eote 4 chest",
        "entrance": (0x41, 0x1, 0x2),
        "exit": (0x41, 0x4, 0x1),
        "type": EntranceGroups.EOTE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },

    "EotE 5 Lower Entrance": {
        "return_name": "EotE 6 Exit",
        "entrance_region": "eote 5",
        "exit_region": "eote 6",
        "entrance": (0x41, 0x5, 0x1),
        "exit": (0x41, 0x6, 0x0),
        "type": EntranceGroups.EOTE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "EotE 6 Door": {
        "return_name": "EotE 7 Exit",
        "entrance_region": "eote 6",
        "exit_region": "eote 7",
        "entrance": (0x41, 0x6, 0x1),
        "exit": (0x41, 0x7, 0x0),
        "type": EntranceGroups.EOTE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "EotE 7 Door": {
        "return_name": "EotE 8 Exit",
        "entrance_region": "eote 7",
        "exit_region": "eote 8",
        "entrance": (0x41, 0x7, 0x1),
        "exit": (0x41, 0x8, 0x0),
        "type": EntranceGroups.EOTE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "EotE 5 Upper Entrance": {
        "return_name": "EotE 8 Chest Exit",
        "entrance_region": "eote 5 chest",
        "exit_region": "eote 8 chest",
        "entrance": (0x41, 0x5, 0x2),
        "exit": (0x41, 0x8, 0x1),
        "type": EntranceGroups.EOTE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },

    "EotE 9 Lower Entrance": {
        "return_name": "EotE A Exit",
        "entrance_region": "eote 9",
        "exit_region": "eote a",
        "entrance": (0x41, 0x9, 0x1),
        "exit": (0x41, 0xa, 0x0),
        "type": EntranceGroups.EOTE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "EotE A Door": {
        "return_name": "EotE B Exit",
        "entrance_region": "eote a",
        "exit_region": "eote b",
        "entrance": (0x41, 0xa, 0x1),
        "exit": (0x41, 0xb, 0x0),
        "type": EntranceGroups.EOTE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "EotE B Door": {
        "return_name": "EotE C Exit",
        "entrance_region": "eote b",
        "exit_region": "eote c",
        "entrance": (0x41, 0xb, 0x1),
        "exit": (0x41, 0xc, 0x0),
        "type": EntranceGroups.EOTE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "EotE 9 Upper Entrance": {
        "return_name": "EotE C Chest Exit",
        "entrance_region": "eote 9 chest",
        "exit_region": "eote c chest",
        "entrance": (0x41, 0x9, 0x2),
        "exit": (0x41, 0xc, 0x1),
        "type": EntranceGroups.EOTE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },


    # ==== Overworld ====
    "Outset to Tutorial": {
        "return_name": "Tutorial to Outset",
        "exit": (0x8, 0x0, 0),
        "entrance": (0x2F, 0x0, 0),
        "exit_region": "forest realm",
        "entrance_region": "outset village",
        "type": EntranceGroups.STATION,
        "direction": EntranceGroups.DOWN,
        "island": EntranceGroups.NONE
    },
    "Outset Board Train": {
        "return_name": "Forest Realm Outset Station",
        "exit": (0x4, 0x0, 1),
        "entrance": (0x2F, 0x0, 0),
        "exit_region": "outset station",
        "entrance_region": "outset village",
        "reverse_required_groups": ["Tracks: Forest Glyph"],
        "type": EntranceGroups.STATION,
        "direction": EntranceGroups.DOWN,
        "island": EntranceGroups.NONE
    },
    "Mayscore Board Train": {
        "return_name": "Forest Realm Mayscore Station",
        "exit": (0x4, 0x0, 2),
        "entrance": (0x2A, 0x0, 0),
        "exit_region": "mayscore station",
        "entrance_region": "mayscore",
        "reverse_required_groups": ["Tracks: Forest Glyph"],
        "type": EntranceGroups.STATION,
        "direction": EntranceGroups.DOWN,
        "island": EntranceGroups.NONE
    },
    "Castle Town Board Train": {
        "return_name": "Forest Realm Castle Town Station",
        "exit": (0x4, 0x0, 0),
        "entrance": (0x29, 0x0, 0),
        "exit_region": "forest realm (ct)",
        "entrance_region": "castle town",
        "reverse_required_groups": ["Tracks: Forest Glyph"],
        "type": EntranceGroups.STATION,
        "direction": EntranceGroups.DOWN,
        "island": EntranceGroups.NONE
    },
    "Woodland Sanctuary Board Train": {
        "return_name": "Forest Realm Woodland Sanctuary Station",
        "exit": (0x4, 0x0, 3),
        "entrance": (0x30, 0x0, 0),
        "exit_region": "woodland sanc station",
        "entrance_region": "woodland sanc",
        "reverse_required_groups": ["Tracks: Forest Glyph"],
        "type": EntranceGroups.STATION,
        "direction": EntranceGroups.DOWN,
        "island": EntranceGroups.NONE
    },
    "Wooded Temple Lobby Board Train": {
        "return_name": "Forest Realm Wooded Temple Station",
        "exit": (0x4, 0x0, 4),
        "entrance": (0x19, 0xA, 0),
        "exit_region": "wt station",
        "entrance_region": "wooded temple lobby",
        "reverse_required_groups": [("Tracks: Wooded Temple Tracks", "Tracks: Forest Source")],
        "type": EntranceGroups.STATION,
        "direction": EntranceGroups.DOWN,
        "island": EntranceGroups.NONE
    },
    "Rabbit Haven Board Train": {
        "return_name": "Forest Realm Rabbit Haven Station",
        "exit": (0x4, 0x0, 8),
        "entrance": (0x3E, 0x0, 0),
        "exit_region": "rabbit haven station",
        "entrance_region": "rabbit haven",
        "reverse_required_groups": ["Tracks: Snow Glyph"],
        "type": EntranceGroups.STATION,
        "direction": EntranceGroups.DOWN,
        "island": EntranceGroups.NONE
    },
    "Anouki Village Board Train": {
        "return_name": "Snow Realm Anouki Village Station",
        "exit": (0x5, 0x0, 0),
        "entrance": (0x2B, 0x0, 0),
        "exit_region": "snow realm (av)",
        "entrance_region": "anouki village",
        "reverse_required_groups": ["Tracks: Snow Glyph"],
        "type": EntranceGroups.STATION,
        "direction": EntranceGroups.DOWN,
        "island": EntranceGroups.NONE
    },
    "Snowfall Sanctuary Board Train": {
        "return_name": "Snow Realm Snowfall Sanctuary Station",
        "exit": (0x5, 0x0, 2),
        "entrance": (0x31, 0x0, 0),
        "exit_region": "snow sanc station",
        "entrance_region": "snow sanc",
        "reverse_required_groups": ["Tracks: Snow Glyph"],
        "type": EntranceGroups.STATION,
        "direction": EntranceGroups.DOWN,
        "island": EntranceGroups.NONE
    },
    "Snow Realm Icy Spring Station": {
        "return_name": "Icy Spring Board Train",
        "entrance_region": "icyspring station",
        "exit_region": "icyspring",
        "required_groups": ["Tracks: Blizzard Temple Tracks"],
        "entrance": (0x5, 0x0, 0x3),
        "exit": (0x35, 0x0, 0x0),
        "type": EntranceGroups.STATION,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Bridge Worker's Board Train": {
        "return_name": "Snow Realm Bridge Worker's Station",
        "exit": (0x5, 0x0, 5),
        "entrance": (0x36, 0x0, 0),
        "exit_region": "bridge workers station",
        "entrance_region": "bridge workers",
        "reverse_required_groups": ["Tracks: Snow Source"],
        "type": EntranceGroups.STATION,
        "direction": EntranceGroups.DOWN,
        "island": EntranceGroups.NONE
    },
    "Blizzard Temple Lobby Board Train": {
        "return_name": "Snow Realm Blizzard Temple Station",
        "exit": (0x5, 0x0, 1),
        "entrance": (0x1A, 0x4, 0),
        "exit_region": "bt station",
        "entrance_region": "blizzard temple lobby",
        "reverse_required_groups": [("Tracks: Blizzard Temple Tracks", "Tracks: Snow Source")],
        "type": EntranceGroups.STATION,
        "direction": EntranceGroups.DOWN,
        "island": EntranceGroups.NONE
    },
    "Slippery Station Board Train": {
        "return_name": "Snow Realm Slippery Station",
        "exit": (0x5, 0x0, 0xF),
        "entrance": (0x3f, 0xA, 0),
        "exit_region": "slippery station",
        "entrance_region": "slippery",
        "reverse_required_groups": ["Tracks: Slippery Station"],
        "type": EntranceGroups.STATION,
        "direction": EntranceGroups.DOWN,
        "island": EntranceGroups.NONE
    },
    "Snowdrift Board Train": {
        "return_name": "Snow Realm Snowdrift Station",
        "exit": (0x5, 0x0, 0xE),
        "entrance": (0x3F, 0x0, 0),
        "exit_region": "snowdrift station",
        "entrance_region": "snowdrift",
        "reverse_required_groups": ["Tracks: Snowdrift Station"],
        "type": EntranceGroups.STATION,
        "direction": EntranceGroups.DOWN,
        "island": EntranceGroups.NONE
    },

    "Trading Post Board Train": {
        "return_name": "Forest Realm Trading Post Station",
        "exit": (0x4, 0x0, 7),
        "entrance": (0x37, 0x0, 0),
        "exit_region": "trading post station",
        "entrance_region": "trading post",
        "reverse_required_groups": ["Tracks: Ocean Glyph"],
        "type": EntranceGroups.STATION,
        "direction": EntranceGroups.DOWN,
        "island": EntranceGroups.NONE
    },
    "Papuzia Board Train": {
        "return_name": "Ocean Realm Papuzia Station",
        "exit": (0x6, 0x0, 0),
        "entrance": (0x2C, 0x0, 0),
        "exit_region": "ocean realm (pv)",
        "entrance_region": "papuzia village",
        "reverse_required_groups": ["Tracks: Ocean Glyph"],
        "type": EntranceGroups.STATION,
        "direction": EntranceGroups.DOWN,
        "island": EntranceGroups.NONE
    },
    "Island Sanctuary Board Train": {
        "return_name": "Ocean Realm Island Sanctuary Station",
        "exit": (0x6, 0x0, 2),
        "entrance": (0x32, 0x0, 0),
        "exit_region": "island sanc station",
        "entrance_region": "island sanc",
        "reverse_required_groups": ["Tracks: Ocean Glyph"],
        "type": EntranceGroups.STATION,
        "direction": EntranceGroups.DOWN,
        "island": EntranceGroups.NONE
    },
    "Marine Temple Lobby Board Train": {
        "return_name": "Undersea Marine Temple Station",
        "exit": (0xA, 0x0, 1),
        "entrance": (0x1B, 0xA, 0),
        "exit_region": "oct station",
        "entrance_region": "marine temple lobby",
        "reverse_required_groups": [("Tracks: Ocean Source", "Tracks: Marine Temple Tracks")],
        "type": EntranceGroups.STATION,
        "direction": EntranceGroups.DOWN,
        "island": EntranceGroups.NONE
    },
    "Marine Temple Train Exit Water Warp": {
        "exit": (0x6, 0x0, 3),
        "entrance": (0x1B, 0xA, 0),
        "exit_region": "ocean temple tracks",
        "entrance_region": "marine temple lobby",
        "reverse_required_groups": [("Tracks: Ocean Source", "Tracks: Marine Temple Tracks")],
        "type": EntranceGroups.NONE,
        "direction": EntranceGroups.DOWN,
        "island": EntranceGroups.NONE,
        "two_way": False
    },
    "Pirate Hideout Board Train": {
        "return_name": "Ocean Realm Pirate Hideout Station",
        "exit": (0x6, 0x0, 5),
        "entrance": (0x3a, 0x0, 0),
        "exit_region": "pirate hideout station",
        "entrance_region": "pirate hideout",
        "reverse_required_groups": ["Tracks: Pirate Hideout"],
        "type": EntranceGroups.STATION,
        "direction": EntranceGroups.DOWN,
        "island": EntranceGroups.NONE
    },
    "Lost at Sea Board Train": {
        "return_name": "Ocean Realm Lost at Sea Station",
        "exit": (0x6, 0x0, 0xE),
        "entrance": (0x39, 0xA, 0),
        "exit_region": "lost at sea station",
        "entrance_region": "lost at sea",
        "reverse_required_groups": ["Tracks: Lost at Sea Station"],
        "type": EntranceGroups.STATION,
        "direction": EntranceGroups.DOWN,
        "island": EntranceGroups.NONE
    },
    "Dune Sanctuary Board Train": {
        "return_name": "Ocean Realm Dune Sanctuary Station",
        "exit": (0x6, 0x0, 6),
        "entrance": (0x34, 0x0, 0),
        "exit_region": "sand sanc station",
        "entrance_region": "sand sanc",
        "reverse_required_groups": ["Tracks: Sand Realm"],
        "type": EntranceGroups.STATION,
        "direction": EntranceGroups.DOWN,
        "island": EntranceGroups.NONE
    },
    "Desert Temple Lobby Board Train": {
        "return_name": "Ocean Realm Desert Temple Station",
        "exit": (0x6, 0x0, 7),
        "entrance": (0x1D, 0x6, 0),
        "exit_region": "desert temple station",
        "entrance_region": "desert temple lobby",
        "reverse_required_groups": ["Tracks: Desert Temple Tracks"],
        "type": EntranceGroups.STATION,
        "direction": EntranceGroups.DOWN,
        "island": EntranceGroups.NONE
    },

    "Fire Realm Goron Village Station": {
        "return_name": "Goron Village Board Train",
        "entrance_region": "fire realm (gv)",
        "exit_region": "goron village",
        "entrance": (0x7, 0x0, 0x0),
        "exit": (0x2E, 0x0, 0x0),
        "required_groups": [("Tracks: Fire Glyph", "Tracks: Fire Source")],
        "type": EntranceGroups.STATION,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Goron Target Range Board Train": {
        "return_name": "Fire Realm Goron Target Range Station",
        "exit": (0x7, 0x0, 4),
        "entrance": (0x3c, 0x0, 1),
        "exit_region": "goron target station",
        "entrance_region": "goron target lobby",
        "reverse_required_groups": ["Tracks: Fire Glyph"],
        "type": EntranceGroups.STATION,
        "direction": EntranceGroups.DOWN,
        "island": EntranceGroups.NONE
    },
    "Goron Target Range Exit": {
        "exit": (0x7, 0x0, 4),
        "entrance": (0x3c, 0x1, 1),
        "exit_region": "goron target station",
        "entrance_region": "gtr",
        "reverse_required_groups": ["Tracks: Fire Glyph"],
        "type": EntranceGroups.STATION,
        "direction": EntranceGroups.DOWN,
        "island": EntranceGroups.NONE,
        "two_way": False
    },
    "Mountain Temple Lobby Board Train": {
        "return_name": "Fire Realm Mountain Temple Station",
        "exit": (0x7, 0x0, 1),
        "entrance": (0x1c, 0xA, 0),
        "exit_region": "mtt station",
        "entrance_region": "mountain temple lobby",
        "reverse_required_groups": [("Tracks: Mountain Temple Tracks", "Tracks: Fire Source")],
        "type": EntranceGroups.STATION,
        "direction": EntranceGroups.DOWN,
        "island": EntranceGroups.NONE
    },
    "Disorientation Station Board Train": {
        "return_name": "Fire Realm Disorientation Station",
        "exit": (0x7, 0x0, 0x16),
        "entrance": (0x40, 0x0, 0),
        "exit_region": "disorientation station station",
        "entrance_region": "disorientation station",
        "reverse_required_groups": ["Tracks: Disorientation Station"],
        "type": EntranceGroups.STATION,
        "direction": EntranceGroups.DOWN,
        "island": EntranceGroups.NONE
    },
    "Ends of the Earth Board Train": {
        "return_name": "Fire Realm Ends of the Earth Station",
        "exit": (0x7, 0x0, 0x17),
        "entrance": (0x41, 0x0, 0),
        "exit_region": "ends of the earth station",
        "entrance_region": "ends of the earth",
        "reverse_required_groups": ["Tracks: Ends of the Earth"],
        "type": EntranceGroups.STATION,
        "direction": EntranceGroups.DOWN,
        "island": EntranceGroups.NONE
    },
    "Dark Ore Mine Board Train": {
        "return_name": "Fire Realm Dark Ore Mine Station",
        "exit": (0x7, 0x0, 5),
        "entrance": (0x3D, 0x0, 0),
        "exit_region": "dark ore mine station",
        "entrance_region": "dark ore mine",
        "reverse_required_groups": ["Tracks: Dark Ore Mine"],
        "type": EntranceGroups.STATION,
        "direction": EntranceGroups.DOWN,
        "island": EntranceGroups.NONE
    },

    # Train Transitions
    "Ocean Realm Dive Underwater": {
        "return_name": "Undersea Tracks Surface",
        "exit": (0xA, 0x0, 0),
        "entrance": (0x6, 0x0, 3),
        "exit_region": "undersea tracks",
        "entrance_region": "undersea entrance",
        "reverse_required_groups": [("Tracks: Ocean Source", "Tracks: Marine Temple Tracks")],
        "required_groups": [("Tracks: Ocean Source", "Tracks: Marine Temple Tracks")],
        "type": EntranceGroups.OVERWORLD_TRAIN,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE
    },
    "Forest Realm North Snow Glyph": {
        "return_name": "Snow Realm South Snow Glyph",
        "entrance_region": "snow realm fr",
        "exit_region": "snow realm s entr",
        "extra_data": {"x_max": -240000},
        "coords": (-368640, 983, -342045),
        "reverse_coords": "flip_v",
        "entrance": (0x4, 0x0, 0xFB),
        "exit": (0x5, 0x0, 0xFC),
        "required_groups": ["Tracks: Snow Glyph"],
        "reverse_required_groups": ["Tracks: Snow Glyph"],
        "type": EntranceGroups.OVERWORLD_TRAIN,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Forest Realm North W Wooded Temple": {
        "return_name": "Snow Realm South W Wooded Temple",
        "entrance_region": "w wooded temple tracks",
        "exit_region": "w wooded temple tracks north",
        "extra_data": {"x_max": -200000, "x_min": -240000},
        "coords": (-221184, 1393, -341845),
        "reverse_coords": "flip_v",
        "entrance": (0x4, 0x0, 0xFB),
        "exit": (0x5, 0x0, 0xFC),
        "required_groups": ["Tracks: W Wooded Temple"],
        "reverse_required_groups": ["Tracks: W Wooded Temple", "Tracks: Snow Glyph"],
        "type": EntranceGroups.OVERWORLD_TRAIN,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Forest Realm North Bridge Tracks": {
        "return_name": "Snow Realm South Bridge Tracks",
        "entrance_region": "snow bridge south",
        "exit_region": "snow bridge mid",
        "extra_data": {"x_min": 70000, "x_max": 80000},
        "coords": (73728, 1393, -334700),
        "reverse_coords": "flip_v",
        "entrance": (0x4, 0x0, 0xFB),
        "exit": (0x5, 0x0, 0xFC),
        "required_groups": ["Tracks: Snow Realm Bridge"],
        "reverse_required_groups": ["Tracks: Snow Realm Bridge"],
        "type": EntranceGroups.OVERWORLD_TRAIN,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Forest Realm North Castle Tracks": {
        "return_name": "Snow Realm South Castle Tracks",
        "entrance_region": "n castle town tracks",
        "exit_region": "n castle town tracks north",
        "extra_data": {"x_min": 260000},
        "coords": (270336, 983, -342045),
        "reverse_coords": "flip_v",
        "entrance": (0x4, 0x0, 0xFB),
        "exit": (0x5, 0x0, 0xFC),
        "required_groups": ["Tracks: N Castle Town"],
        "reverse_required_groups": ["Tracks: N Castle Town"],
        "type": EntranceGroups.OVERWORLD_TRAIN,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Fire Realm West Fire Glyph": {
        "return_name": "Snow Realm East Fire Glyph",
        "entrance_region": "fire realm west entr",
        "exit_region": "fire realm west",
        "extra_data": {"z_min": 0},
        "coords": (463671, 0, 147456),
        "reverse_coords": (-464853, 0, 147456),
        "entrance": (0x7, 0x0, 0xFD),
        "exit": (0x5, 0x0, 0xFE),
        "required_groups": ["Tracks: Fire Glyph"],
        "reverse_required_groups": ["Tracks: Fire Glyph"],
        "type": EntranceGroups.OVERWORLD_TRAIN,
        "direction": EntranceGroups.LEFT,
        "island": EntranceGroups.NONE
    },
    "Fire Realm West Gorge Tracks": {
        "return_name": "Snow Realm East Gorge Tracks",
        "entrance_region": "gorge tracks east",
        "exit_region": "gorge tracks west",
        "extra_data": {"z_max": 0},
        "coords": (-464925, 901, -147456),
        "reverse_coords": "flip_h",
        "entrance": (0x7, 0x0, 0xFD),
        "exit": (0x5, 0x0, 0xFE),
        "required_groups": ["Tracks: Snow Realm Gorge"],
        "reverse_required_groups": ["Tracks: Snow Realm Gorge"],
        "type": EntranceGroups.OVERWORLD_TRAIN,
        "direction": EntranceGroups.LEFT,
        "island": EntranceGroups.NONE
    },
    "Ocean Realm West Ocean Shortcut": {
        "return_name": "Forest Realm East Ocean Shortcut",
        "entrance_region": "ocean shortcut east",
        "exit_region": "ocean shortcut",
        "extra_data": {"z_max": 10000},
        "coords": (487572, 0, 0),
        "reverse_coords": "flip_h",
        "entrance": (0x6, 0x0, 0xFD),
        "exit": (0x4, 0x0, 0xFE),
        "required_groups": ["Tracks: Forest Realm Ocean Shortcut"],
        "reverse_required_groups": ["Tracks: Forest Realm Ocean Shortcut"],
        "type": EntranceGroups.OVERWORLD_TRAIN,
        "direction": EntranceGroups.LEFT,
        "island": EntranceGroups.NONE
    },
    "Ocean Realm West Ocean Glyph": {
        "return_name": "Forest Realm East Ocean Glyph",
        "reverse_one_way_data": {"animation_override": 0x30},
        "entrance_region": "ocean realm",
        "exit_region": "ocean realm mid",
        "extra_data": {"z_min": 10000},  # This turns train invis but better than crashing
        "coords": (-453624, 9585, 245760),
        "reverse_coords": "flip_h",
        "entrance": (0x6, 0x0, 0xFD),
        "exit": (0x4, 0x0, 0xFE),
        "required_groups": ["Tracks: Ocean Glyph"],
        "reverse_required_groups": ["Tracks: Ocean Glyph"],
        "type": EntranceGroups.OVERWORLD_TRAIN,
        "direction": EntranceGroups.LEFT,
        "island": EntranceGroups.NONE
    },
    "Ocean Realm North Sand Connection": {
        "return_name": "Fire Realm South Sand Connection",
        "entrance_region": "sand connection south",
        "exit_region": "sand connection mid",
        "extra_data": {"x_max": -300000},
        "coords": (-319488, 1393, -342045),
        "reverse_coords": "flip_v",
        "entrance": (0x6, 0x0, 0xFB),
        "exit": (0x7, 0x0, 0xFC),
        "required_groups": ["Tracks: Sand Realm", "Tracks: Fire Realm Sand Portal"],
        "reverse_required_groups": ["Tracks: Sand Realm", "Tracks: Fire Realm Sand Portal"],
        "type": EntranceGroups.OVERWORLD_TRAIN,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Ocean Realm North Rocktite Cave": {
        "return_name": "Fire Realm South Rocktite Cave",
        "entrance_region": "sand realm exit",
        "exit_region": "sand restoration rocktite",
        "extra_data": {"x_min": 20000, "x_max": 30000},
        "coords": (24576, 983, 342045),
        "reverse_coords": "flip_v",
        "entrance": (0x6, 0x0, 0xFB),
        "exit": (0x7, 0x0, 0x11),
        "required_groups": ["Tracks: Desert Temple Tracks"],
        "reverse_required_groups": ["Tracks: Desert Temple Tracks"],
        "type": EntranceGroups.OVERWORLD_TRAIN,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Ocean Realm North Rocktite Cave Fight": {
        "return_name": "Desert Rocktite Fight Entrance",
        "entrance_region": "sand realm exit",
        "exit_region": "sand restoration",
        "extra_data": {"x_min": -200000},
        "coords": (24576, 983, 342045),
        "entrance": (0x6, 0x0, 0xFB),
        "exit": (0xC, 0x0, 0x0),
        "required_groups": ["Tracks: Sand Realm", "Tracks: Desert Temple Tracks"],
        "reverse_required_groups": ["Tracks: Sand Realm", "Tracks: Desert Temple Tracks"],
        "type": EntranceGroups.NONE,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE,
        "two_way": False
    },
    "Desert Rocktite Fight Exit": {
        "return_name": "Fire Realm Exit Rocktite Fight",
        "entrance_region": "sand restoration rocktite",
        "exit_region": "sand restoration mid",
        "entrance": (0xC, 0x0, 0x0),
        "exit": (0x7, 0x0, 0x6),
        "required_groups": ["Tracks: Desert Temple Tracks"],
        "reverse_required_groups": ["Tracks: Desert Temple Tracks"],
        "type": EntranceGroups.NONE,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE,
        "two_way": False
    },
    "Ocean Realm North Desert Temple": {
        "return_name": "Fire Realm South Desert Temple",
        "entrance_region": "sand restoration south exit",
        "exit_region": "sand restoration mid",
        "extra_data": {"x_min": 400000},
        "coords": (417792, 0, -334526),
        "reverse_coords": (417792, 983, 342045),
        "entrance": (0x6, 0x0, 0xFB),
        "exit": (0x7, 0x0, 0xFC),
        "required_groups": ["Tracks: Desert Temple Tracks"],
        "reverse_required_groups": ["Tracks: Desert Temple Tracks"],
        "type": EntranceGroups.OVERWORLD_TRAIN,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },

    # ===== Tower of Spirits =====
    "Tower of Spirits to Forest Realm": {
        "return_name": "Forest Realm to Tower of Spirits",
        "entrance": (0x14, 1, 0),
        "exit": (0x4, 0x0, 6),
        "entrance_region": "tos lobby",
        "exit_region": "tos forest station",
        "reverse_required_groups": [("Tracks: Forest Glyph", "Tracks: Forest Source")],
        "type": EntranceGroups.STATION,
        "direction": EntranceGroups.DOWN,
        "island": EntranceGroups.NONE
    },
    "Tower of Spirits to Snow Realm": {
        "return_name": "Snow Realm to Tower of Spirits",
        "entrance": (0x14, 1, 0),
        "exit": (0x5, 0x0, 6),
        "entrance_region": "tos lobby",
        "exit_region": "tos snow station",
        "reverse_required_groups": ["Tracks: Snow Source"],
        "type": EntranceGroups.STATION,
        "direction": EntranceGroups.DOWN,
        "island": EntranceGroups.NONE
    },
    "Tower of Spirits to Ocean Realm": {
        "return_name": "Ocean Realm to Tower of Spirits",
        "entrance": (0x14, 1, 0),
        "exit": (0x6, 0x0, 4),
        "entrance_region": "tos lobby",
        "exit_region": "tos ocean station",
        "reverse_required_groups": ["Tracks: Ocean Source"],
        "type": EntranceGroups.STATION,
        "direction": EntranceGroups.DOWN,
        "island": EntranceGroups.NONE
    },
    "Tower of Spirits to Fire Realm": {
        "return_name": "Fire Realm to Tower of Spirits",
        "entrance": (0x14, 1, 0),
        "exit": (0x7, 0x0, 2),
        "entrance_region": "tos lobby",
        "exit_region": "tos fire station",
        "reverse_required_groups": ["Tracks: Fire Source"],
        "type": EntranceGroups.STATION,
        "direction": EntranceGroups.DOWN,
        "island": EntranceGroups.NONE
    },

    # ===== Warp Portals =====
    "Forest Realm North Portal": {
        "return_name": "Snow Realm West Portal",
        "entrance": (0x4, 0, 0xA),
        "exit": (0x5, 0x0, 0xA),
        "entrance_region": "forest realm n portal",
        "exit_region": "snow realm south portal",
        "required_groups": ["Tracks: Forest Glyph"],
        "reverse_required_groups": ["Tracks: Snow Glyph"],
        "type": EntranceGroups.TRAIN_PORTAL,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE
    },
    "Forest Realm South Portal": {
        "return_name": "Snow Realm East Portal",
        "entrance": (0x4, 0, 0xB),
        "exit": (0x5, 0x0, 0xC),
        "entrance_region": "forest realm se portal",
        "exit_region": "btt e portal",
        "required_groups": ["Tracks: Forest Realm SE Portal"],
        "reverse_required_groups": ["Tracks: Blizzard Temple Tracks"],
        "type": EntranceGroups.TRAIN_PORTAL,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE
    },
    "Snow Realm North Portal": {
        "return_name": "Fire Realm Mountain Portal",
        "entrance": (0x5, 0, 0xD),  # Random value, probably not correct
        "exit": (0x7, 0x0, 0x14),
        "entrance_region": "icyspring portal",
        "exit_region": "mountain temple portal",
        "required_groups": ["Tracks: N Icy Spring"],
        "reverse_required_groups": ["Tracks: Mountain Temple Tracks"],
        "type": EntranceGroups.TRAIN_PORTAL,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE
    },
    "Snow Realm Bridge Portal": {
        "return_name": "Ocean Realm South Portal",
        "entrance": (0x5, 0, 0xB),
        "exit": (0x6, 0x0, 0x9),
        "entrance_region": "snow bridge portal",
        "exit_region": "island sanc portal",
        "required_groups": ["Tracks: Snow Realm Bridge"],
        "reverse_required_groups": ["Tracks: Marine Temple Tracks"],
        "type": EntranceGroups.TRAIN_PORTAL,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE
    },
    "Forest Realm Cave Portal": {
        "return_name": "Fire Realm Portal",
        "entrance": (0x4, 0, 0xC),
        "exit": (0x7, 0x0, 0x12),
        "entrance_region": "forest cave portal",
        "exit_region": "fire realm portal",
        "required_groups": ["Tracks: Forest Realm SW Cave"],
        "reverse_required_groups": ["Tracks: Fire Glyph"],
        "type": EntranceGroups.TRAIN_PORTAL,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE
    },
    "Ocean Realm West Portal": {
        "return_name": "Forest Realm Mayscore Portal",
        "entrance": (0x6, 0, 0xd),
        "exit": (0x4, 0, 0xd),
        "entrance_region": "ocean portal",
        "exit_region": "s mayscore portal",
        "required_groups": ["Tracks: Ocean Portal"],
        "reverse_required_groups": ["Tracks: Ocean Glyph"],
        "type": EntranceGroups.TRAIN_PORTAL,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE
    },
    "Sand Realm Temple Portal": {
        "return_name": "Sand Realm Sanctuary Portal",
        "entrance": (0x6, 0, 0xB),
        "exit": (0x6, 0x0, 0xC),
        "entrance_region": "desert temple portal",
        "exit_region": "sand realm portal",
        "required_groups": ["Tracks: Desert Temple Tracks"],
        "reverse_required_groups": ["Tracks: Sand Realm"],
        "type": EntranceGroups.TRAIN_PORTAL,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE
    },
    "Fire Realm Sand Portal": {
        "return_name": "Ocean Realm Temple Portal",
        "entrance": (0x7, 0, 0x13),
        "exit": (0x6, 0x0, 0xA),
        "entrance_region": "sand connection portal",
        "exit_region": "ocean temple portal",
        "required_groups": ["Tracks: Fire Realm Sand Portal"],
        "reverse_required_groups": ["Tracks: Marine Temple Tracks"],
        "type": EntranceGroups.TRAIN_PORTAL,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE
    },

    # Dark Realm
    "Enter Dark Realm Portal": {
        "return_name": "Enter Dark Trains",
        "entrance": (0x4, 0, 0x9),
        "exit": (0xF, 0x0, 0x0),
        "entrance_region": "dark realm portal",
        "exit_region": "dark realm trains",
        "type": EntranceGroups.NONE,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE
    },
    "Defeat Dark Trains": {
        "return_name": "Enter Demon Train",
        "entrance": (0xF, 0, 0x0),
        "exit": (0x10, 0xFF, 0x0),
        "two_way": False,
        "entrance_region": "dark realm trains",
        "exit_region": "demon train",
        "type": EntranceGroups.NONE,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE
    },
    "Defeat Demon Train": {
        "return_name": "Enter Cole Fight",
        "entrance": (0x12, 0xFF, 0x0),
        "exit": (0x24, 0x00, 0x0),
        "two_way": False,
        "entrance_region": "demon train",
        "exit_region": "cole fight",
        "type": EntranceGroups.NONE,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE
    },
    "Defeat Cole": {
        "return_name": "Enter Malladus 1",
        "entrance": (0x10, 0x0, 0x0),
        "exit": (0x25, 0x0, 0x0),
        "two_way": False,
        "entrance_region": "cole fight",
        "exit_region": "malladus 1",
        "type": EntranceGroups.NONE,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE
    },
    "Defeat Malladus 1": {
        "return_name": "Enter Malladus 2",
        "entrance": (0x26, 0x0, 0x0),
        "exit": (0x27, 0x0, 0x0),
        "two_way": False,
        "entrance_region": "malladus 1",
        "exit_region": "malladus 2",
        "type": EntranceGroups.NONE,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE
    },

    # ToS Entrances
    "Tower of Spirits Enter Section 1": {
        "return_name": "ToS 1F Exit",
        "entrance": (0x17, 0, 1),
        "exit": (0x13, 0x0, 0),
        "entrance_region": "tos 1",
        "exit_region": "tos 1f",
        "one_way_data": {"tower": 1},
        "type": EntranceGroups.TOS_SECTION,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Tower of Spirits Enter Section 2": {
        "return_name": "ToS 4F Exit",
        "entrance": (0x17, 0, 2),
        "exit": (0x13, 0x3, 0),
        "entrance_region": "tos 2",
        "exit_region": "tos 4f",
        "one_way_data": {"tower": 2},
        "type": EntranceGroups.TOS_SECTION,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Tower of Spirits Enter Section 3": {
        "return_name": "ToS 8F Exit",
        "entrance": (0x17, 0, 3),
        "exit": (0x13, 0x7, 0),
        "entrance_region": "tos 3",
        "exit_region": "tos 8f",
        "one_way_data": {"tower": 3},
        "type": EntranceGroups.TOS_SECTION,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Tower of Spirits Enter Section 4": {
        "return_name": "ToS 13F Exit",
        "entrance": (0x17, 0, 4),
        "exit": (0x13, 0xC, 0),
        "entrance_region": "tos 4",
        "exit_region": "tos 13f",
        "one_way_data": {"tower": 4},
        "type": EntranceGroups.TOS_SECTION,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Tower of Spirits Enter Section 5": {
        "return_name": "ToS 18F Exit",
        "entrance": (0x17, 0, 5),
        "exit": (0x13, 0x11, 0),
        "entrance_region": "tos 5",
        "exit_region": "tos 18f",
        "one_way_data": {"tower": 5},
        "type": EntranceGroups.TOS_SECTION,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Tower of Spirits Exit Staven": {
        "return_name": "ToS Summit Lower Exit",
        "entrance": (0x23, 0, 1),
        "exit": (0x15, 0x0, 0),
        "entrance_region": "tos post staven",
        "exit_region": "tos summit lower",
        "type": EntranceGroups.TOS_SECTION,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Tower of Spirits Summit Enter Altar": {
        "return_name": "ToS 31F Exit",
        "entrance": (0x15, 0, 2),
        "exit": (0x13, 0x1d, 0),
        "entrance_region": "tos 6",
        "exit_region": "tos 30f",
        "type": EntranceGroups.TOS_SECTION,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },

    "Tower of Spirits Lobby Staircase": {
        "return_name": "Tower of Spirits Staircase Exit",
        "entrance_region": "tos lobby",
        "exit_region": "tos",
        "entrance": (0x14, 0x1, 0x1),  # Needs extra data for staircase side
        "exit": (0x17, 0x0, 0x0),
        "reverse_one_way_data": {"y": 0},
        "type": EntranceGroups.TOS_LOBBY,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Tower of Spirits Staircase Elevators": {
        "two_way": False,
        "entrance_region": "tos lobby",
        "exit_region": "tos 1",
        "exit": (0x14, 0x1, 0x1),
        "entrance": (0x17, 0x0, 0x0),
        # "reverse_one_way_data": {"y": 0},
        "type": EntranceGroups.NONE,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE
    },
    "ToS 3F Blue Portal": {
        "two_way": False,
        "entrance": (0x13, 2, 1),
        "exit": (0x14, 0x1, 3),
        "entrance_region": "tos 3f rail map",
        "exit_region": "tos",
        "type": EntranceGroups.NONE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "ToS 7F Blue Portal": {
        "two_way": False,
        "entrance": (0x13, 6, 1),
        "exit": (0x14, 0x1, 3),
        "entrance_region": "tos 7f rail map",
        "exit_region": "tos",
        "type": EntranceGroups.NONE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "ToS 12F Blue Portal": {
        "two_way": False,
        "entrance": (0x13, 0xB, 1),
        "exit": (0x14, 0x1, 3),
        "entrance_region": "tos 11f",
        "exit_region": "tos",
        "type": EntranceGroups.NONE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "ToS 17F Blue Portal": {
        "two_way": False,
        "entrance": (0x13, 0xF, 1),
        "exit": (0x14, 0x1, 3),
        "entrance_region": "tos 16f",
        "exit_region": "tos",
        "type": EntranceGroups.NONE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "ToS 24F Blue Portal": {
        "two_way": False,
        "entrance": (0x13, 0x23, 1),
        "exit": (0x14, 0x1, 1),
        "entrance_region": "tos 24f",
        "exit_region": "tos",
        "type": EntranceGroups.NONE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "ToS 23F Blue Warp Before Staven": {
        "return_name": "ToS Top of Staircase Blue Warp",
        "entrance": (0x13, 0x14, 2),
        "exit": (0x17, 0x0, 6),
        "entrance_region": "tos 22f",
        "exit_region": "tos 5",
        "type": EntranceGroups.NONE,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE
    },


    # ===== Dungeons =====

    # wooded temple
    "Wooded Temple Lobby Enter Dungeon": {
        "return_name": "Wooded Temple 1F Exit",
        "entrance_region": "wooded temple lobby",
        "exit_region": "wt 1f",
        "entrance": (0x19, 0xA, 1),
        "exit": (0x19, 0x0, 0),
        "direction": EntranceGroups.UP,
        "type": EntranceGroups.DUNGEON_ENTRANCE,
        "island": EntranceGroups.WOODED
    },
    "Wooded Temple 1F SE Staircase": {
        "return_name": "Wooded Temple 2F SE Staircase",
        "entrance_region": "wt 1f se door",
        "exit_region": "wt 2f",
        "entrance": (0x19, 0x0, 1),
        "exit": (0x19, 0x1, 0),
        "direction": EntranceGroups.NONE,
        "type": EntranceGroups.DUNGEON_ROOM,
        "island": EntranceGroups.WOODED
    },
    "Wooded Temple 1F NW Staircase": {
        "return_name": "Wooded Temple 2F NW Staircase",
        "entrance_region": "wt 1f north",
        "exit_region": "wt 2f north",
        "entrance": (0x19, 0x0, 2),
        "exit": (0x19, 0x1, 1),
        "direction": EntranceGroups.NONE,
        "type": EntranceGroups.DUNGEON_ROOM,
        "island": EntranceGroups.WOODED
    },
    "Wooded Temple 1F SW Staircase": {
        "return_name": "Wooded Temple 2F SW Staircase",
        "entrance_region": "wt 1f left arena",
        "exit_region": "wt 2f left",
        "entrance": (0x19, 0x0, 3),
        "exit": (0x19, 0x1, 3),
        "direction": EntranceGroups.NONE,
        "type": EntranceGroups.DUNGEON_ROOM,
        "island": EntranceGroups.WOODED
    },
    "Wooded Temple 2F W Staircase": {
        "return_name": "Wooded Temple 3F W Staircase",
        "entrance_region": "wt 2f left",
        "exit_region": "wt 3f left",
        "entrance": (0x19, 0x1, 4),
        "exit": (0x19, 0x2, 2),
        "direction": EntranceGroups.NONE,
        "type": EntranceGroups.DUNGEON_ROOM,
        "island": EntranceGroups.WOODED
    },
    "Wooded Temple 2F Central Staircase": {
        "return_name": "Wooded Temple 3F N Staircase",
        "entrance_region": "wt 2f moth door",
        "exit_region": "wt 3f",
        "entrance": (0x19, 0x1, 2),
        "exit": (0x19, 0x2, 0),
        "direction": EntranceGroups.NONE,
        "type": EntranceGroups.DUNGEON_ROOM,
        "island": EntranceGroups.WOODED
    },
    "Wooded Temple 3F S Staircase": {
        "return_name": "Wooded Temple 4F S Staircase",
        "entrance_region": "wt 3f boss door",
        "exit_region": "wt 4f",
        "entrance": (0x19, 0x2, 1),
        "exit": (0x19, 0x3, 0),
        "direction": EntranceGroups.NONE,
        "type": EntranceGroups.DUNGEON_ROOM,
        "island": EntranceGroups.WOODED
    },
    "Wooded Temple 4F N Staircase": {
        "return_name": "Stagnox Exit",
        "entrance_region": "wt 4f",
        "exit_region": "wt pre stagnox",
        "entrance": (0x19, 0x3, 1),
        "exit": (0x1E, 0x0, 0),
        "direction": EntranceGroups.UP,
        "type": EntranceGroups.BOSS,
        "island": EntranceGroups.WOODED
    },
    "Wooded Temple 4F Blue Warp": {
        "return_name": "Wooded Temple Lobby Blue Warp",
        "entrance_region": "wt blue warp",
        "exit_region": "wooded temple lobby",
        "entrance": (0x19, 0x3, 2),
        "exit": (0x19, 0xA, 2),
        "direction": EntranceGroups.DOWN,
        "type": EntranceGroups.WARP_PORTAL,
        "island": EntranceGroups.WOODED
    },

    # Blizzard Temple
    "Blizzard Temple Lobby Enter Dungeon": {
        "return_name": "Blizzard Temple 1F South Exit",
        "entrance_region": "blizzard temple lobby",
        "exit_region": "bt 1f exit",
        "entrance": (0x1a, 0x4, 1),
        "exit": (0x1a, 0x5, 0),
        "direction": EntranceGroups.UP,
        "type": EntranceGroups.DUNGEON_ENTRANCE,
        "island": EntranceGroups.BLIZZARD
    },
    "Blizzard Temple 1F South Entrance": {
        "return_name": "Blizzard Temple 1F Main South",
        "entrance_region": "bt 1f s",
        "exit_region": "bt 1f",
        "entrance": (0x1a, 0x5, 5),
        "exit": (0x1a, 0x0, 7),
        "direction": EntranceGroups.UP,
        "type": EntranceGroups.DUNGEON_ROOM,
        "island": EntranceGroups.BLIZZARD
    },
    "Blizzard Temple 1F Main East": {
        "return_name": "Blizzard Temple 1F SE Entrance",
        "entrance_region": "bt 1f e",
        "exit_region": "bt 1f se",
        "entrance": (0x1a, 0x0, 8),
        "exit": (0x1a, 0x5, 6),
        "direction": EntranceGroups.DOWN,
        "type": EntranceGroups.DUNGEON_ROOM,
        "island": EntranceGroups.BLIZZARD
    },
    "Blizzard Temple 1F SE Staircase": {
        "return_name": "Blizzard Temple B1 SE Staircase",
        "entrance_region": "bt 1f se door",
        "exit_region": "bt b1 se",
        "entrance": (0x1a, 0x5, 1),
        "exit": (0x1a, 0x1, 1),
        "direction": EntranceGroups.NONE,
        "type": EntranceGroups.DUNGEON_ROOM,
        "island": EntranceGroups.BLIZZARD
    },
    "Blizzard Temple 1F NE Staircase": {
        "return_name": "Blizzard Temple B1 NE Staircase",
        "entrance_region": "bt 1f ne",
        "exit_region": "bt b1 ne door",
        "entrance": (0x1a, 0x0, 2),
        "exit": (0x1a, 0x1, 2),
        "direction": EntranceGroups.NONE,
        "type": EntranceGroups.DUNGEON_ROOM,
        "island": EntranceGroups.BLIZZARD
    },
    "Blizzard Temple 1F Main SW": {
        "return_name": "Blizzard Temple 1F SW Entrance",
        "entrance_region": "bt 1f",
        "exit_region": "bt 1f sw",
        "entrance": (0x1a, 0x0, 6),
        "exit": (0x1a, 0x5, 4),
        "direction": EntranceGroups.DOWN,
        "type": EntranceGroups.DUNGEON_ROOM,
        "island": EntranceGroups.BLIZZARD
    },
    "Blizzard Temple 1F SW Staircase": {
        "return_name": "Blizzard Temple B1 SW Staircase",
        "entrance_region": "bt 1f sw door",
        "exit_region": "bt b1 sw",
        "entrance": (0x1a, 0x5, 3),
        "exit": (0x1a, 0x1, 3),
        "direction": EntranceGroups.NONE,
        "type": EntranceGroups.DUNGEON_ROOM,
        "island": EntranceGroups.BLIZZARD
    },
    "Blizzard Temple 1F NW Staircase": {
        "return_name": "Blizzard Temple B1 NW Staircase",
        "entrance_region": "bt 1f nw",
        "exit_region": "bt b1 nw",
        "entrance": (0x1a, 0x0, 4),
        "exit": (0x1a, 0x1, 4),
        "direction": EntranceGroups.NONE,
        "type": EntranceGroups.DUNGEON_ROOM,
        "island": EntranceGroups.BLIZZARD
    },
    "Blizzard Temple 1F NW Entrance": {
        "return_name": "Blizzard Temple 1F West Entrance",
        "entrance_region": "bt 1f nw",
        "exit_region": "bt 1f w",
        "entrance": (0x1a, 0x0, 9),
        "exit": (0x1a, 0x5, 7),
        "direction": EntranceGroups.DOWN,
        "type": EntranceGroups.DUNGEON_ROOM,
        "island": EntranceGroups.BLIZZARD
    },
    "Blizzard Temple 1F North Staircase": {
        "return_name": "Blizzard Temple 2F North Staircase",
        "entrance_region": "bt 1f n",
        "exit_region": "bt 2f",
        "entrance": (0x1a, 0x0, 5),
        "exit": (0x1a, 0x2, 0),
        "direction": EntranceGroups.NONE,
        "type": EntranceGroups.DUNGEON_ROOM,
        "island": EntranceGroups.BLIZZARD
    },
    "Blizzard Temple 2F South Staircase": {
        "return_name": "Blizzard Temple 3F South Staircase",
        "entrance_region": "bt 2f boss door",
        "exit_region": "bt 3f",
        "entrance": (0x1a, 0x2, 1),
        "exit": (0x1a, 0x3, 0),
        "direction": EntranceGroups.NONE,
        "type": EntranceGroups.DUNGEON_ROOM,
        "island": EntranceGroups.BLIZZARD
    },
    "Blizzard Temple 3F North Staircase": {
        "return_name": "Fraaz Exit",
        "entrance_region": "bt 3f",
        "exit_region": "bt pre fraaz",
        "entrance": (0x1a, 0x3, 1),
        "exit": (0x1F, 0x0, 0),
        "direction": EntranceGroups.UP,
        "type": EntranceGroups.BOSS,
        "island": EntranceGroups.BLIZZARD
    },
    "Blizzard Temple 3F Blue Warp": {
        "return_name": "Blizzard Temple Lobby Blue Warp",
        "entrance_region": "bt blue warp",
        "exit_region": "blizzard temple lobby",
        "entrance": (0x1a, 0x3, 2),
        "exit": (0x1a, 0x4, 3),
        "direction": EntranceGroups.DOWN,
        "type": EntranceGroups.WARP_PORTAL,
        "island": EntranceGroups.BLIZZARD
    },

    # Marine Temple
    "Marine Temple Lobby Enter Dungeon": {
        "return_name": "Marine Temple 1F Exit",
        "entrance_region": "marine temple lobby",
        "exit_region": "oct 1f",
        "entrance": (0x1b, 0xA, 1),
        "exit": (0x1b, 0x0, 0),
        "direction": EntranceGroups.UP,
        "type": EntranceGroups.DUNGEON_ENTRANCE,
        "island": EntranceGroups.MARINE
    },
    "Marine Temple 1F North Staircase": {
        "return_name": "Marine Temple 2F North Staircase",
        "entrance_region": "oct 1f",
        "exit_region": "oct 2f",
        "entrance": (0x1b, 0x0, 1),
        "exit": (0x1b, 0x1, 0),
        "direction": EntranceGroups.NONE,
        "type": EntranceGroups.DUNGEON_ROOM,
        "island": EntranceGroups.MARINE
    },
    "Marine Temple 2F Left Bomb Cave": {
        "return_name": "Marine Temple Stamp Room Exit",
        "entrance_region": "oct 2f",
        "exit_region": "oct stamp room",
        "entrance": (0x1b, 0x1, 3),
        "exit": (0x1b, 0x7, 0),
        "direction": EntranceGroups.UP,
        "type": EntranceGroups.DUNGEON_ROOM,
        "island": EntranceGroups.MARINE
    },
    "Marine Temple 2F Right Bomb Cave": {
        "return_name": "Marine Temple Switch Room Exit",
        "entrance_region": "oct 2f",
        "exit_region": "oct boomerang room",
        "entrance": (0x1b, 0x1, 4),
        "exit": (0x1b, 0x7, 1),
        "direction": EntranceGroups.UP,
        "type": EntranceGroups.DUNGEON_ROOM,
        "island": EntranceGroups.MARINE
    },
    "Marine Temple 1F East Staircase": {
        "return_name": "Marine Temple 2F NE Staircase",
        "entrance_region": "oct 1f right",
        "exit_region": "oct 2f right",
        "entrance": (0x1b, 0x0, 2),
        "exit": (0x1b, 0x1, 2),
        "direction": EntranceGroups.NONE,
        "type": EntranceGroups.DUNGEON_ROOM,
        "island": EntranceGroups.MARINE
    },
    "Marine Temple 2F East Staircase": {
        "return_name": "Marine Temple 3F East Staircase",
        "entrance_region": "oct 2f right",
        "exit_region": "oct 3f east",
        "entrance": (0x1b, 0x1, 1),
        "exit": (0x1b, 0x2, 0),
        "direction": EntranceGroups.NONE,
        "type": EntranceGroups.DUNGEON_ROOM,
        "island": EntranceGroups.MARINE
    },
    "Marine Temple 3F North Staircase": {
        "return_name": "Marine Temple 4F North Staircase",
        "entrance_region": "oct 3f ne",
        "exit_region": "oct 4f north",
        "entrance": (0x1b, 0x2, 3),
        "exit": (0x1b, 0x3, 2),
        "direction": EntranceGroups.NONE,
        "type": EntranceGroups.DUNGEON_ROOM,
        "island": EntranceGroups.MARINE
    },
    "Marine Temple 3F West Staircase": {
        "return_name": "Marine Temple 4F West Staircase",
        "entrance_region": "oct 3f west",
        "exit_region": "oct 4f west",
        "entrance": (0x1b, 0x2, 1),
        "exit": (0x1b, 0x3, 0),
        "direction": EntranceGroups.NONE,
        "type": EntranceGroups.DUNGEON_ROOM,
        "island": EntranceGroups.MARINE
    },
    "Marine Temple 3F South Staircase": {
        "return_name": "Marine Temple 4F South Staircase",
        "entrance_region": "oct 3f south",
        "exit_region": "oct 4f south",
        "entrance": (0x1b, 0x2, 2),
        "exit": (0x1b, 0x3, 3),
        "direction": EntranceGroups.NONE,
        "type": EntranceGroups.DUNGEON_ROOM,
        "island": EntranceGroups.MARINE
    },
    "Marine Temple 4F East Staircase": {
        "return_name": "Marine Temple 5F East Staircase",
        "entrance_region": "oct 4f east",
        "exit_region": "oct 5f",
        "entrance": (0x1b, 0x3, 1),
        "exit": (0x1b, 0x4, 0),
        "direction": EntranceGroups.NONE,
        "type": EntranceGroups.DUNGEON_ROOM,
        "island": EntranceGroups.MARINE
    },
    "Marine Temple 5F NW Staircase": {
        "return_name": "Marine Temple 6F NW Staircase",
        "entrance_region": "oct 5f nw",
        "exit_region": "oct 6f nw",
        "entrance": (0x1b, 0x4, 2),
        "exit": (0x1b, 0x5, 0),
        "direction": EntranceGroups.NONE,
        "type": EntranceGroups.DUNGEON_ROOM,
        "island": EntranceGroups.MARINE
    },
    "Marine Temple 5F SW Staircase": {
        "return_name": "Marine Temple 6F SW Staircase",
        "entrance_region": "oct 5f sw",
        "exit_region": "oct 6f sw",
        "entrance": (0x1b, 0x4, 1),
        "exit": (0x1b, 0x5, 1),
        "direction": EntranceGroups.NONE,
        "type": EntranceGroups.DUNGEON_ROOM,
        "island": EntranceGroups.MARINE
    },
    "Marine Temple 5F SE Staircase": {
        "return_name": "Marine Temple 6F SE Staircase",
        "entrance_region": "oct 5f se",
        "exit_region": "oct 6f se",
        "entrance": (0x1b, 0x4, 4),
        "exit": (0x1b, 0x5, 2),
        "direction": EntranceGroups.NONE,
        "type": EntranceGroups.DUNGEON_ROOM,
        "island": EntranceGroups.MARINE
    },
    "Marine Temple 6F Central Staircase": {
        "return_name": "Marine Temple 7F South Staircase",
        "entrance_region": "oct 6f boss door",
        "exit_region": "oct 7f south",
        "entrance": (0x1b, 0x5, 3),
        "exit": (0x1b, 0x6, 0),
        "direction": EntranceGroups.NONE,
        "type": EntranceGroups.DUNGEON_ROOM,
        "island": EntranceGroups.MARINE
    },
    "Marine Temple 7F North Staircase": {
        "return_name": "Cactops Exit",
        "entrance_region": "oct 7f thorns",
        "exit_region": "oct pre phytops",
        "entrance": (0x1b, 0x6, 1),
        "exit": (0x20, 0x0, 0),
        "direction": EntranceGroups.UP,
        "type": EntranceGroups.BOSS,
        "island": EntranceGroups.MARINE
    },
    "Marine Temple 7F Blue Warp": {
        "return_name": "Marine Temple Lobby Blue Warp",
        "entrance_region": "oct blue warp",
        "exit_region": "marine temple lobby",
        "entrance": (0x1b, 0x6, 2),
        "exit": (0x1b, 0xA, 2),
        "direction": EntranceGroups.DOWN,
        "type": EntranceGroups.WARP_PORTAL,
        "island": EntranceGroups.MARINE
    },

    # Mountain Temple
    "Mountain Temple Lobby Enter Dungeon": {
        "return_name": "Mountain Temple 1F Exit",
        "entrance_region": "mountain temple lobby",
        "exit_region": "mtt 1f",
        "entrance": (0x1c, 0xA, 1),
        "exit": (0x1c, 0x0, 0),
        "direction": EntranceGroups.UP,
        "type": EntranceGroups.DUNGEON_ENTRANCE,
        "island": EntranceGroups.MOUNTAIN
    },
    "Mountain Temple 1F SW Staircase": {
        "return_name": "Mountain Temple 2F SW Staircase",
        "entrance_region": "mtt 1f left",
        "exit_region": "mtt 2f left",
        "entrance": (0x1c, 0x0, 5),
        "exit": (0x1c, 0x6, 3),
        "direction": EntranceGroups.NONE,
        "type": EntranceGroups.DUNGEON_ROOM,
        "island": EntranceGroups.MOUNTAIN
    },
    "Mountain Temple 1F SE Staircase": {
        "return_name": "Mountain Temple 2F SE Staircase",
        "entrance_region": "mtt 1f right",
        "exit_region": "mtt 2f right",
        "entrance": (0x1c, 0x0, 4),
        "exit": (0x1c, 0x6, 2),
        "direction": EntranceGroups.NONE,
        "type": EntranceGroups.DUNGEON_ROOM,
        "island": EntranceGroups.MOUNTAIN
    },
    "Mountain Temple 1F Central Staircase": {
        "return_name": "Mountain Temple 2F Central Staircase",
        "entrance_region": "mtt 1f door",
        "exit_region": "mtt 2f arena",
        "entrance": (0x1c, 0x0, 1),
        "exit": (0x1c, 0x6, 0),
        "direction": EntranceGroups.NONE,
        "type": EntranceGroups.DUNGEON_ROOM,
        "island": EntranceGroups.MOUNTAIN
    },
    "Mountain Temple 1F NE Staircase": {
        "return_name": "Mountain Temple 2F NE Staircase",
        "entrance_region": "mtt 1f ne",
        "exit_region": "mtt 2f ne door",
        "entrance": (0x1c, 0x0, 3),
        "exit": (0x1c, 0x6, 1),
        "direction": EntranceGroups.NONE,
        "type": EntranceGroups.DUNGEON_ROOM,
        "island": EntranceGroups.MOUNTAIN
    },
    "Mountain Temple 1F North Staircase": {
        "return_name": "Mountain Temple B1 NE Staircase",
        "entrance_region": "mtt 1f n",
        "exit_region": "mtt b1 n",
        "entrance": (0x1c, 0x0, 2),
        "exit": (0x1c, 0x2, 0),
        "direction": EntranceGroups.NONE,
        "type": EntranceGroups.DUNGEON_ROOM,
        "island": EntranceGroups.MOUNTAIN
    },
    "Mountain Temple B1 North Staircase": {
        "return_name": "Mountain Temple B2 North Staircase",
        "entrance_region": "mtt b1 n",
        "exit_region": "mtt b2 n",
        "entrance": (0x1c, 0x2, 1),
        "exit": (0x1c, 0x3, 0),
        "direction": EntranceGroups.NONE,
        "type": EntranceGroups.DUNGEON_ROOM,
        "island": EntranceGroups.MOUNTAIN
    },
    "Mountain Temple B1 East Staircase": {
        "return_name": "Mountain Temple B2 East Staircase",
        "entrance_region": "mtt b1 arena",
        "exit_region": "mtt b2 se",
        "entrance": (0x1c, 0x2, 3),
        "exit": (0x1c, 0x3, 4),
        "direction": EntranceGroups.NONE,
        "type": EntranceGroups.DUNGEON_ROOM,
        "island": EntranceGroups.MOUNTAIN
    },
    "Mountain Temple B1 West Staircase": {
        "return_name": "Mountain Temple B2 West Staircase",
        "entrance_region": "mtt b1 arena exit",
        "exit_region": "mtt b2 sw",
        "entrance": (0x1c, 0x2, 4),
        "exit": (0x1c, 0x3, 5),
        "direction": EntranceGroups.NONE,
        "type": EntranceGroups.DUNGEON_ROOM,
        "island": EntranceGroups.MOUNTAIN
    },
    "Mountain Temple B1 Central Staircase": {
        "return_name": "Mountain Temple B2 Central Staircase",
        "entrance_region": "mtt b1 cart exit",
        "exit_region": "mtt b2 s",
        "entrance": (0x1c, 0x2, 2),
        "exit": (0x1c, 0x3, 2),
        "direction": EntranceGroups.NONE,
        "type": EntranceGroups.DUNGEON_ROOM,
        "island": EntranceGroups.MOUNTAIN
    },
    "Mountain Temple B2 South Staircase": {
        "return_name": "Mountain Temple B3 South Staircase",
        "entrance_region": "mtt b2 s",
        "exit_region": "mtt b3",
        "entrance": (0x1c, 0x3, 3),
        "exit": (0x1c, 0x4, 0),
        "direction": EntranceGroups.NONE,
        "type": EntranceGroups.DUNGEON_ROOM,
        "island": EntranceGroups.MOUNTAIN
    },
    "Mountain Temple B3 North Staircase": {
        "return_name": "Mountain Temple B4 South Staircase",
        "entrance_region": "mtt b3 boss door",
        "exit_region": "mtt b4",
        "entrance": (0x1c, 0x4, 2),
        "exit": (0x1c, 0x5, 0),
        "direction": EntranceGroups.NONE,
        "type": EntranceGroups.DUNGEON_ROOM,
        "island": EntranceGroups.MOUNTAIN
    },
    "Mountain Temple B4 North Staircase": {
        "return_name": "Vulcano Exit",
        "entrance_region": "mtt b4",
        "exit_region": "mtt pre vulcano",
        "entrance": (0x1c, 0x5, 2),
        "exit": (0x21, 0x0, 0),
        "direction": EntranceGroups.UP,
        "type": EntranceGroups.BOSS,
        "island": EntranceGroups.MOUNTAIN
    },
    "Mountain Temple Lobby Blue Warp": {
        "return_name": "Mountain Temple B4 Blue Warp",
        "entrance_region": "mountain temple lobby",
        "exit_region": "mtt blue warp",
        "entrance": (0x1c, 0xa, 2),
        "exit": (0x1c, 0x5, 1),
        "direction": EntranceGroups.UP,
        "type": EntranceGroups.WARP_PORTAL,
        "island": EntranceGroups.MOUNTAIN
    },

    # Desert Temple
    "Desert Temple Lobby Enter Dungeon": {
        "return_name": "Desert Temple 1F Exit",
        "entrance_region": "desert temple lobby",
        "exit_region": "dt",
        "entrance": (0x1d, 0x6, 1),
        "exit": (0x1d, 0x0, 0),
        "direction": EntranceGroups.UP,
        "type": EntranceGroups.DUNGEON_ENTRANCE,
        "island": EntranceGroups.DESERT
    },
    "Desert Temple 1F Lower Staircase": {
        "return_name": "Desert Temple B1 Left Staircase",
        "entrance_region": "dt",
        "exit_region": "dt b1 stairs",
        "entrance": (0x1d, 0x0, 2),
        "exit": (0x1d, 0x3, 0),
        "direction": EntranceGroups.NONE,
        "type": EntranceGroups.DUNGEON_ROOM,
        "island": EntranceGroups.DESERT
    },
    "Desert Temple 1F Upper Staircase": {
        "return_name": "Desert Temple 2F Left Staircase",
        "entrance_region": "dt",
        "exit_region": "dt 2f west",
        "entrance": (0x1d, 0x0, 1),
        "exit": (0x1d, 0x1, 0),
        "direction": EntranceGroups.NONE,
        "type": EntranceGroups.DUNGEON_ROOM,
        "island": EntranceGroups.DESERT
    },
    "Desert Temple 3F Staircase": {
        "return_name": "Desert Temple 2F Right Staircase",
        "entrance_region": "dt 3f",
        "exit_region": "dt 2f",
        "entrance": (0x1d, 0x2, 0),
        "exit": (0x1d, 0x1, 1),
        "direction": EntranceGroups.NONE,
        "type": EntranceGroups.DUNGEON_ROOM,
        "island": EntranceGroups.DESERT
    },
    "Desert Temple B1 Boss Door Staircase": {
        "return_name": "Desert Temple B2 South Staircase",
        "entrance_region": "dt b1 boss door",
        "exit_region": "dt b2 s",
        "entrance": (0x1d, 0x3, 1),
        "exit": (0x1d, 0x4, 0),
        "direction": EntranceGroups.NONE,
        "type": EntranceGroups.DUNGEON_ROOM,
        "island": EntranceGroups.DESERT
    },
    "Desert Temple B2 North Entrance": {
        "return_name": "Capbone Exit",
        "entrance_region": "dt b2 n",
        "exit_region": "dt pre skeldritch",
        "entrance": (0x1d, 0x4, 1),
        "exit": (0x22, 0x0, 0),
        "direction": EntranceGroups.UP,
        "type": EntranceGroups.BOSS,
        "island": EntranceGroups.DESERT
    },
    "Desert Temple Lobby Blue Warp": {
        "return_name": "Desert Temple B2 Blue Warp",
        "entrance_region": "desert temple lobby",
        "exit_region": "dt blue warp",
        "entrance": (0x1d, 0x6, 3),
        "exit": (0x1d, 0x4, 2),
        "direction": EntranceGroups.UP,
        "type": EntranceGroups.WARP_PORTAL,
        "island": EntranceGroups.DESERT
    },

    # Lost at Sea Dungeon
    "Lost at Sea Lobby Enter Dungeon One-Way": {
        "return_name": "Lost at Sea Dungeon Plain Phantom Spawn",
        "entrance_region": "las loop",
        "two_way": False,
        "exit_region": "las 1",
        "exit": (0x42, 0x2, 0x0),
        "entrance": (0x39, 0xB, 0x1),
        "type": EntranceGroups.NONE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Lost at Sea Dungeon Plain Phantom Staircase": {
        "return_name": "Lost at Sea Dungeon Torch Phantom North",
        "entrance_region": "las 1",
        "exit_region": "las 2",
        "exit": (0x42, 0x3, 0x0),
        "entrance": (0x42, 0x2, 0x1),
        "type": EntranceGroups.LAS,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE
    },
    "Lost at Sea Dungeon Warp Phantom South": {
        "return_name": "Lost at Sea Dungeon Torch Phantom South",
        "entrance_region": "las 3",
        "exit_region": "las 2",
        "entrance": (0x42, 0x4, 0x0),
        "exit": (0x42, 0x3, 0x1),
        "type": EntranceGroups.LAS,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE
    },
    "Lost at Sea Dungeon Warp Phantom North": {
        "return_name": "Lost at Sea Dungeon Wrecker Phantom West",
        "entrance_region": "las 3",
        "exit_region": "las 4",
        "entrance": (0x42, 0x4, 0x1),
        "exit": (0x42, 0x5, 0x0),
        "type": EntranceGroups.LAS,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE
    },
    "Lost at Sea Dungeon Wrecker Phantom East": {
        "return_name": "Lost at Sea Dungeon Quad Room South",
        "entrance_region": "las 4 door",
        "exit_region": "las 5",
        "entrance": (0x42, 0x5, 0x1),
        "exit": (0x42, 0x6, 0x0),
        "type": EntranceGroups.LAS,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE
    },
    "Lost at Sea Dungeon Quad Room North": {
        "return_name": "Lost at Sea Dungeon Reward Room South",
        "entrance_region": "las 5 door",
        "exit_region": "las 6",
        "entrance": (0x42, 0x6, 0x1),
        "exit": (0x42, 0x7, 0x0),
        "type": EntranceGroups.LAS,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Lost at Sea Dungeon Reward Room Warp One-Way": {
        "return_name": "Lost at Sea Dungeon Return Warp",
        "entrance_region": "las 6",
        "exit_region": "las lobby",
        "entrance": (0x42, 0x7, 0x1),
        "exit": (0x39, 0xB, 0x1),
        "type": EntranceGroups.NONE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    "Lost at Sea Lobby Enter Dungeon": {
        "return_name": "Lost at Sea Dungeon Reward Room Warp",
        "entrance_region": "las lobby",
        "exit_region": "las loop",
        "exit": (0x42, 0x7, 0x1),
        "entrance": (0x39, 0xB, 0x1),
        "type": EntranceGroups.LAS,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.NONE
    },
    # Misc entrances
    "Desert Temple B2 North Post-Fight": {
        "return_name": "Skeldritch Post-Fight Exit",
        "entrance_region": "dt b2 n",
        "exit_region": "dt skeldritch",
        "entrance": (0x1D, 0x4, 0x1),
        "exit": (0x22, 0x1, 0),
        "type": EntranceGroups.NONE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.DESERT
    },
    "Stagnox Blue Warp": {
        "return_name": "Wooded Temple Lobby Boss Warp",
        "entrance_region": "wt stagnox",
        "exit_region": "wooded temple lobby",
        "entrance": (0x1E, 0x0, 5),
        "exit": (0x19, 0xA, 1),
        "extra_data": {"animation_override": 0x19},
        "type": EntranceGroups.NONE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.WOODED,
        "two_way": False
    },
    "Fraaz Blue Warp": {
        "return_name": "Blizzard Temple Lobby Boss Warp",
        "entrance_region": "bt fraaz",
        "exit_region": "blizzard temple lobby",
        "entrance": (0x1F, 0x0, 5),
        "exit": (0x1A, 0x4, 2),
        "extra_data": {"animation_override": 0x19},
        "type": EntranceGroups.NONE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.BLIZZARD,
        "two_way": False
    },
    "Cactops Blue Warp": {
        "return_name": "Marine Temple Lobby Boss Warp",
        "entrance_region": "oct phytops",
        "exit_region": "marine temple lobby",
        "entrance": (0x20, 0x0, 5),
        "exit": (0x1B, 0xA, 2),
        "extra_data": {"animation_override": 0x19},
        "type": EntranceGroups.NONE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.MARINE,
        "two_way": False
    },
    "Vulcano Blue Warp": {
        "return_name": "Mountain Temple Lobby Boss Warp",
        "entrance_region": "mtt vulcano",
        "exit_region": "mountain temple lobby",
        "entrance": (0x21, 0x0, 5),
        "exit": (0x1C, 0xA, 2),
        "extra_data": {"animation_override": 0x19},
        "type": EntranceGroups.NONE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.MOUNTAIN,
        "two_way": False
    },
    "Desert Temple Bow of Light Room Blue Warp": {
        "return_name": "Desert Temple Lobby Boss Warp",
        "entrance_region": "dt skeldritch",
        "exit_region": "desert temple lobby",
        "entrance": (0x1d, 0x5, 1),
        "exit": (0x1D, 0x6, 2),
        "extra_data": {"animation_override": 0x19},
        "type": EntranceGroups.NONE,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.DESERT,
        "two_way": False
    },
    "Menu Enter Game": {
        "entrance_region": "menu",
        "exit_region": "niko's house",
        "entrance": (0x79, 0xFF, 0),
        "exit": (0x2F, 0xA, 0),
        "type": EntranceGroups.NONE,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE,
        "two_way": False
    },
    # Events

    # Boss Events
    "EVENT: Defeat Stagnox": event("wt stagnox", "event_stagnox"),
    "EVENT: Defeat Fraaz": event("bt fraaz", "event_fraaz"),
    "EVENT: Defeat Cactops": event("oct phytops", "event_phytops"),
    "EVENT: Defeat Vulcano": event("mtt vulcano", "event_vulcano"),
    "EVENT: Defeat Capbone": event("dt skeldritch", "skeldritch event"),
    "EVENT: Reach ToS 3F": event("tos 3f rail map", "event_3f"),
    "EVENT: Reach ToS 7F": event("tos 7f rail map", "event_7f"),
    "EVENT: Reach ToS 12F": event("tos 11f", "event_12f"),
    "EVENT: Reach ToS 17F": event("tos 16f", "event_17f"),
    "EVENT: Defeat Staven": event("tos staven", "event_staven"),
    "EVENT: Reach ToS 24F": event("tos 24f", "event_24f"),
    "EVENT: Complete Lost at Sea Dungeon": event("las event shield", "las_event"),
    "EVENT: Complete Take 'em All On 3": event("teao 3", "teao_event"),

    # Goal Events
    "GOAL: Defeat Stagnox": event("wt stagnox", "goal_stagnox"),
    "GOAL: Defeat Fraaz": event("bt fraaz", "goal_fraaz"),
    "GOAL: Defeat Cactops": event("oct phytops", "goal_phytops"),
    "GOAL: Defeat Vulcano": event("mtt pre vulcano", "goal_vulcano"),
    "GOAL: Defeat Skeldritch": event("dt skeldritch", "skeldritch goal"),
    "GOAL: Reach ToS 3F": event("tos 3f rail map", "goal_forest_glyph"),
    "GOAL: Reach ToS 7F": event("tos 7f rail map", "goal_forest_glyph"),
    "GOAL: Reach ToS 12F": event("tos 11f", "goal_ocean_glyph"),
    "GOAL: Reach ToS 17F": event("tos 16f", "goal_fire_glyph"),
    "GOAL: Defeat Staven": event("tos staven", "goal_staven"),
    "GOAL: Reach ToS 24F": event("tos 24f", "goal_compass"),
    "GOAL: Defeat Malladus": event("malladus 2", "malladus event"),
    "GOAL: Enter Dark Realm": event("dark realm trains", "dark realm event"),

    # NPC Events
    "EVENT: Castle Town Pick Up Alfonzo": event("pick up alfonzo", "alfonzo event"),
    "EVENT: Trading Post Give Regal Ring to Linebeck": event("linebeck trading", "linebeck event"),
    "EVENT: Goron Village Bring Ice to Kagoron": event("goron ice", "goron ice event"),
    "EVENT: Mountain Altar Visit Kagoron": event("mountain altar", "kagoron event"),
    "EVENT: Outset Drop Off Ferrus": event("delivered ferrus", "outset delivered ferrus event"),
    "EVENT: Anouki Village Drop Off Goron": event("av goron", "av goron event"),
    "EVENT: Island Sanctuary Drop Off Carben": event("island sanc carben", "carben event"),
    "EVENT: Disorientation Maze Find Chest": event("disorientation sod", "disorientation event"),

    # Blue Warp Events
    "EVENT: Wooded Temple Open Blue Warp": event("wt blue warp", "wt warp event"),
    "EVENT: Blizzard Temple Open Blue Warp": event("bt blue warp", "bt warp event"),
    "EVENT: Marine Temple Open Blue Warp": event("oct blue warp", "oct warp event"),
    "EVENT: Mountain Temple Open Blue Warp": event("mtt blue warp", "mtt warp event"),
    "EVENT: Desert Temple Open Blue Warp": event("dt blue warp", "dt warp event"),

    # Train Portal Events
    "EVENT: Unlock Forest Realm Cave Portal": event("forest cave portal loc", "cave portal event"),
    "EVENT: Unlock Snow Bridge Portal": event("snow bridge portal loc", "snow bridge portal event"),
    "EVENT: Unlock Anouki Village Portal": event("anouki portal", "anouki portal event"),
    "EVENT: Unlock Icy Spring Portal": event("icyspring portal loc", "icyspring portal event"),
    "EVENT: Unlock Forest Realm SE Portal": event("trading post portal", "trading post portal event"),
    "EVENT: Unlock Ocean Portal": event("ocean portal loc", "ocean portal event"),
    "EVENT: Unlock Desert Temple Portal": event("sand restoration portal", "sand restoration portal event"),
    "EVENT: Unlock Sand Connection Portal": event("sand connection portal loc", "sand connection portal event"),

    # Dungeon Events
    "EVENT: Marine Temple 6F Arena": event("oct 6f sw arena", "oct 6f sw arena event"),
    "EVENT: Marine Temple 2F Boulders": event("oct 2f boulders", "oct 2f boulders event"),
    "EVENT: Marine Temple Stamp Room Switch": event("oct boomerang switch", "oct boomerang switch event"),

    # Visit Station Events
    "EVENT: Visit Outset": event("outset village", "visit outset"),
    "EVENT: Visit Castle Town": event("castle town", "visit castle town"),
    "EVENT: Visit Rabbit Haven": event("rabbit haven", "visit rabbit haven"),
    "EVENT: Visit Anouki Village": event("anouki village", "visit anouki village"),
    "EVENT: Visit Icy Spring": event("icyspring", "visit icyspring"),
    "EVENT: Visit Trading Post": event("trading post", "visit trading post"),
    "EVENT: Visit Papuzia Village": event("papuzia village", "visit papuzia"),
    "EVENT: Visit Marine Temple": event("marine temple lobby", "visit marine temple"),
    "EVENT: Visit Goron Village": event("goron village", "visit goron village"),

    # Stamp Station Events
    "EVENT: Outset Stamp Station": event("outset stamp station", "outset stamp event"),
    "EVENT: Mayscore Forest Stamp Station": event("mayscore stamp station", "mayscore stamp event"),
    "EVENT: Castle Town Stamp Station": event("castle town stamp station", "castle town stamp event"),
    "EVENT: Woodland Sanctuary Stamp Station": event("woodland sanc stamp station", "woodland sanc stamp event"),
    "EVENT: Anouki Village Stamp Station": event("anouki village stamp station", "anouki village stamp event"),
    "EVENT: Snowfall Sanctuary Stamp Station": event("snow sanc stamp station", "snow sanc stamp event"),
    "EVENT: Icy Spring Stamp Station": event("icyspring stamp station", "icyspring stamp event"),
    "EVENT: Trading Post Tunnel Stamp Station": event("trading post stamp station", "trading post stamp event"),
    "EVENT: Papuzia Archipelago Stamp Station": event("papuzia village stamp station", "papuzia village stamp event"),
    "EVENT: Island Sanctuary Stamp Station": event("island sanc stamp station", "island sanc stamp event"),
    "EVENT: Pirate Hideout Stamp Station": event("pirate hideout stamp station", "pirate hideout stamp event"),
    "EVENT: Goron Field Stamp Station": event("goron field stamp station", "goron field stamp event"),
    "EVENT: Valley Sanctuary Stamp Station": event("valley sanc stamp station", "valley sanc stamp event"),
    "EVENT: Dune Sanctuary Stamp Station": event("sand sanc stamp station", "sand sanc stamp event"),
    "EVENT: Wooded Temple Stamp Station": event("wt stamp station", "wt stamp event"),
    "EVENT: Blizzard Temple Stamp Station": event("bt b1 stamp station", "bt b1 stamp event"),
    "EVENT: Marine Temple Stamp Station": event("oct stamp station", "oct stamp event"),
    "EVENT: Mountain Temple Stamp Station": event("mtt b1 stamp station", "mtt b1 stamp event"),
    "EVENT: Desert Temple Stamp Station": event("dt stamp station", "dt stamp event"),
    "EVENT: Tower of Spirits Summit Stamp Station": event("tos stamp station", "tos stamp event"),

    # Rabbit Events
    "EVENT: Rabbit Near Castle Town": event("forest realm rabbits", "forest realm rabbits event"),
    "EVENT: Rabbit Near Ocean Shortcut": event("forest ocean shortcut rabbit", "forest ocean shortcut rabbit event"),
    "EVENT: Rabbit E Mayscore": event("e mayscore rabbits", "e mayscore rabbits event"),
    "EVENT: Rabbit SW Trading Post": event("sw trading post rabbit", "sw trading post rabbit event"),
    "EVENT: Rabbit E Outset": event("forest realm rabbits", "forest realm rabbits event 2"),
    "EVENT: Rabbit SW Rabbit Haven": event("s rabbit haven rabbits", "s rabbit haven rabbits event"),
    "EVENT: Rabbit Near Wooded Temple": event("wt rabbit", "wt rabbit event"),
    "EVENT: Rabbit Near Rabbit Haven": event("nr rabbit haven rabbit", "nr rabbit haven rabbit event"),
    "EVENT: Rabbit Past Wooden Bridge": event("e mayscore rabbits", "e mayscore rabbits event 2"),
    "EVENT: Rabbit S Rabbit Haven": event("s rabbit haven rabbits", "s rabbit haven rabbits event 2"),

    "EVENT: Rabbit Near ToS Fire Realm": event("fire source rabbits", "fire source rabbits event"),
    "EVENT: Rabbit Near Disorientation Station": event("disorientation rabbits", "disorientation rabbits event"),
    "EVENT: Rabbit Near Ends of the Earth": event("eote rabbits", "eote rabbits event"),
    "EVENT: Rabbit NW Mountain": event("mountain rabbits", "mountain rabbits event"),
    "EVENT: Rabbit NE Mountain": event("mountain rabbits", "mountain rabbits event 2"),
    "EVENT: Rabbit N Mountain": event("mountain rabbits", "mountain rabbits event 3"),
    "EVENT: Rabbit S Mountain": event("s mountain temple rabbit", "s mountain temple rabbit event"),
    "EVENT: Rabbit SE Mountain": event("mountain rabbits", "mountain rabbits event 4"),
    "EVENT: Rabbit N Fire Glyph": event("fire realm rabbits", "fire realm rabbits event"),
    "EVENT: Rabbit Near Goron Target Range": event("fire realm rabbits", "fire realm rabbits event 2"),
    "EVENT: Rabbit E Sand Maze": event("sand restoration rabbits", "sand restoration rabbits event"),
    "EVENT: Rabbit Mid Sand Maze": event("sand restoration rabbits", "sand restoration rabbits event 2"),
    "EVENT: Rabbit W Sand Maze": event("sand restoration rabbits", "sand restoration rabbits event 3"),
    "EVENT: Rabbit Sand Valley": event("sand connection rabbit", "sand connection rabbit event"),

    "EVENT: Rabbit W Lost at Sea": event("las rabbit", "las rabbit event"),
    "EVENT: Rabbit Near Island Sanctuary": event("ocean rabbits", "ocean rabbits event"),
    "EVENT: Rabbit E Pirate Hideout": event("ocean source rabbits", "ocean source rabbits event"),
    "EVENT: Rabbit W Pirate Hideout": event("pirate rabbit", "pirate rabbit event"),
    "EVENT: Rabbit W Marine Temple": event("ocean rabbits", "ocean rabbits event 2"),
    "EVENT: Rabbit N Undersea Entrance": event("ocean rabbits", "ocean rabbits event 3"),
    "EVENT: Rabbit Near Ocean Portal": event("ocean portal rabbits", "ocean portal rabbits event"),
    "EVENT: Rabbit S Undersea Entrance": event("ocean rabbits", "ocean rabbits event 4"),
    "EVENT: Rabbit E Ocean": event("ocean rabbits", "ocean rabbits event 5"),
    "EVENT: Rabbit N Lost at Sea": event("ocean rabbits", "ocean rabbits event 6"),
    "EVENT: Rabbit E Sand Realm": event("sand realm rabbits", "sand realm rabbits event"),
    "EVENT: Rabbit N Sand Realm": event("sand realm rabbits", "sand realm rabbits event 2"),
    "EVENT: Rabbit S Sand Realm": event("sand realm rabbits", "sand realm rabbits event 3"),
    "EVENT: Rabbit W Sand Realm": event("sand realm rabbits", "sand realm rabbits event 4"),
    "EVENT: Rabbit W Desert Temple": event("sand restoration south rabbits", "sand restoration south rabbits event"),
    "EVENT: Rabbit E Desert Temple": event("sand restoration south rabbits", "sand restoration south rabbits event 2"),

    "EVENT: Rabbit NE Blizzard": event("snow realm early blizzard rabbits", "snow realm early blizzard rabbits event"),
    "EVENT: Rabbit SE Blizzard": event("snow realm blizzard rabbits", "snow realm blizzard rabbits event"),
    "EVENT: Rabbit W Anouki Village": event("snow realm rabbits", "snow realm rabbits event"),
    "EVENT: Rabbit SW Blizzard": event("snow realm blizzard rabbits", "snow realm blizzard rabbits event 2"),
    "EVENT: Rabbit E Anouki Village": event("blizzard temple tracks rabbits", "blizzard temple tracks rabbits event"),
    "EVENT: Rabbit Near Snowdrift Station": event("snowdrift station rabbit", "snowdrift station rabbit event"),
    "EVENT: Rabbit W Icy Spring Station": event("icyspring rabbits", "icyspring rabbits event"),
    "EVENT: Rabbit N Icy Spring Station": event("icyspring rabbits", "icyspring rabbits event 2"),
    "EVENT: Rabbit NW Blizzard": event("snow realm early blizzard rabbits", "snow realm early blizzard rabbits event 2"),
    "EVENT: Rabbit Central Blizzard": event("snow realm early blizzard rabbits", "snow realm early blizzard rabbits event 3"),

    # Vanilla Passenger Events
    "EVENT: Bridge Worker's Home Pick Up Kenzo": event("pick up bridge worker"),
    "EVENT: Trading Post Drop Off Kenzo": event("trading post bridge worker"),  # no event item, just connects regions
    "EVENT: Trading Post Pick Up Kenzo": event("trading post pick up kenzo"),

    "EVENT: Anouki Village Pick Up Kofu": event("av kofu"),
    "EVENT: Anouki Village Pick Up Noko": event("av noko"),
    "EVENT: Icy Spring Drop Off Noko": event("icyspring noko"),  # no event item

    "EVENT: Castle Town Pick Up Mona": event("castle town mona"),
    "EVENT: Outset Pick Up Joe": event("outset joe"),
    "EVENT: Mayscore Pick Up Dovok": event("mayscore dovok"),

    "EVENT: Papuzia Village Pick Up Carben": event("pv carben"),
    "EVENT: Pirate Hideout Pick Up Wadatsumi": event("pirate wadatsumi"),

    "EVENT: Goron Village Pick Up Snow Goron": event("pick up snow goron"),
    "EVENT: Goron Village Pick Up City Goron": event("pick up city goron"),

    "EVENT: Snow Realm Pick Up Ferrus": event("snow realm ferrus"),
    "EVENT: Fire Realm Pick Up Ferrus": event("fire realm ferrus"),
    "EVENT: Marine Temple Lobby Drop Off Ferrus": event("oct ferrus"),

    "EVENT: Dune Sanctuary Deliver Cuccos": event("sand sanc cuccos"),

    # Vanilla buy cargo
    "EVENT: Icy Spring Buy Mega Ice": event("icyspring ice"),
    "EVENT: Mayscore Buy Lumber": event("mayscore lumber"),
    "EVENT: Castle Town Buy Cuccos": event("castle town buy cuccos"),
    "EVENT: Papuzia Village Buy Fish": event("papuzia buy fish"),
    "EVENT: Papuzia Village Buy Vessel": event("wise one buy vessel"),
    "EVENT: Goron Field Buy Steel": event("goron steel"),
    "EVENT: Dark Ore Mine Buy Ore": event("dark ore mine ore"),

    "Mountain Temple 2F Central Staircase Alt": {
        "return_name": "MTT Fake",
        "entrance_region": "mtt 2f arena",
        "exit_region": "mtt 1f",
        "exit": (0x1c, 0x0, 1),
        "entrance": (0x1c, 0x1, 0),
        "direction": EntranceGroups.NONE,
        "type": EntranceGroups.NONE,
        "island": EntranceGroups.NONE
    },
    "MTT Fake 2": {
        "return_name": "Mountain Temple 2F NE Staircase Alt",
        "entrance_region": "mtt 1f n",
        "exit_region": "mtt 2f ne",
        "entrance": (0x1c, 0x0, 3),
        "exit": (0x1c, 0x1, 1),
        "direction": EntranceGroups.NONE,
        "type": EntranceGroups.NONE,
        "island": EntranceGroups.NONE
    },

    "EVENT: Wooded Temple 1F Shortcut": silent_event("wt 1f","wt 1f north"),
    "EVENT: Wooded Temple 2F Windmill": silent_event("wt 2f north","wt 2f ne arena"),

    "EVENT: Blizzard Temple 1F Bell Door 1": silent_event("bt 1f e shortcut","bt 1f"),
    "EVENT: Blizzard Temple B1 SE Windmill": silent_event("bt b1 e","bt b1 se"),
    "EVENT: Blizzard Temple 1F NE Door": silent_event("bt 1f","bt 1f ne"),
    "EVENT: Blizzard Temple 1F NW Door": silent_event("bt 1f","bt 1f nw"),
    "EVENT: Blizzard Temple 1F Bell Door 3": event("bt 1f nw bell"),

    "EVENT: Marine Temple 3F South Branch": silent_event("oct 3f arena","oct 3f south"),
    "EVENT: Marine Temple 4F West Door": silent_event("oct 4f west","oct 4f north"),
    "EVENT: Marine Temple 4F South Bridge": silent_event("oct 4f south","oct 4f west"),
    "EVENT: Marine Temple 5F North Branches": silent_event("oct 5f nw","oct 5f"),
    "EVENT: Marine Temple 5F SE Door": silent_event("oct 5f se","oct 5f s"),

    "EVENT: Mountain Temple 1F SW Switch": silent_event("mtt 1f right","mtt 1f"),
    "EVENT: Mountain Temple 1F Main Door": silent_event("mtt 1f door","mtt 1f"),
    "EVENT: Mountain Temple 2F Heatoise Arena": silent_event("mtt 2f ne","mtt 2f arena"),
    "EVENT: Mountain Temple B2 Stalfos Arena": silent_event("mtt b2","mtt b2 n"),
    "EVENT: Mountain Temple B2 SE Torches": silent_event("mtt b2 se","mtt b2 e"),
    "EVENT: Mountain Temple B2 W Branch": silent_event("mtt b2","mtt b2 sw shortcut"),  # Requires whip
    "EVENT: Mountain Temple B1 Arena": silent_event("mtt b1 arena exit", "mtt b1 arena"),

    "EVENT: Desert Temple B1 Shortcut": silent_event("dt b1 stairs", "dt b1 s"),

    "EVENT: Island Sanctuary Bridge": silent_event("island sanc", "island sanc shortcut"),  # ow logic
    "EVENT: Tunnel to the Tower 2F Door": silent_event("tower tunnel 2f door", "tower tunnel 2f north"),
    "EVENT: Valley Sanctuary Door": silent_event("valley sanc door", "valley sanc east"),

    "EVENT: Blizzard Temple 1F Bell Door 2": event("bt 1f ne bell"),
    "EVENT: Desert Temple B1 Red Door": silent_event("dt b1 mid", "dt b1 s"),

}


ENTRANCES: dict[str, STTransition] = STTransition.from_data(ENTRANCE_DATA)
entrance_id_to_entrance = {e.id: e for e in ENTRANCES.values()}
entrance_id_to_region = {e.id: e.entrance_region for e in ENTRANCES.values()}
entrance_tuple_to_entrance: dict[tuple, STTransition] = {e.entrance: e for e in ENTRANCES.values()}
entrances_per_scene: dict[int, list[STTransition]] = {}
for e in ENTRANCES.values():
    entrances_per_scene.setdefault(e.scene, []).append(e)

location_event_lookup = {"Stagnox Boss Reward": "EVENT: Defeat Stagnox",
                         "Fraaz Boss Reward": "EVENT: Defeat Fraaz",
                         "ToS 3F Forest Rail Glyph": "EVENT: Reach ToS 3F",
                         "ToS 7F Snow Rail Glyph": "EVENT: Reach ToS 7F",
                         "ToS 12F Ocean Rail Glyph": "EVENT: Reach ToS 12F",
                         "ToS 17F Fire Rail Glyph": "EVENT: Reach ToS 17F",
                         "ToS 23F Defeat Staven": "EVENT: Defeat Staven",
                         "ToS 24F Final Chest": "EVENT: Reach ToS 24F",
                         "Cactops Boss Reward": "EVENT: Defeat Cactops",
                         "Vulcano Boss Reward": "EVENT: Defeat Vulcano",
                         "Capbone Boss Reward": "EVENT: Defeat Capbone",
                         "Castle Town Take 'em All On Level 3": "EVENT: Complete Take 'em All On 3",
                         "Lost at Sea Final Chest": "EVENT: Complete Lost at Sea Dungeon"}
boss_events = set(location_event_lookup.values())
cargo_events = {
    "EVENT: Icy Spring Buy Mega Ice",
    "EVENT: Mayscore Buy Lumber",
    "EVENT: Castle Town Buy Cuccos",
    "EVENT: Papuzia Village Buy Fish",
    "EVENT: Papuzia Village Buy Vessel",
    "EVENT: Goron Field Buy Steel",
    "EVENT: Dark Ore Mine Buy Ore",
}

goal_event_lookup =     {0: "GOAL: Defeat Stagnox",
                         1: "GOAL: Defeat Fraaz",
                         2: "GOAL: Defeat Cactops",
                         3: "GOAL: Defeat Vulcano",
                         4: "GOAL: Defeat Skeldritch",
                         5: "GOAL: Reach ToS 3F",
                         6: "GOAL: Reach ToS 7F",
                         7: "GOAL: Reach ToS 12F",
                         8: "GOAL: Reach ToS 17F",
                         9: "GOAL: Defeat Staven",
                         10: "GOAL: Reach ToS 24F",
                         -1: "GOAL: Defeat Malladus"}

valid_starts: set[str] = {
    n for n, d in ENTRANCES.items() if
    not n.startswith("Unnamed")
    and d.category_group not in [EntranceGroups.TRAIN_PORTAL, EntranceGroups.OVERWORLD_TRAIN, EntranceGroups.EVENT, EntranceGroups.NONE]
    and not (d.category_group == EntranceGroups.STATION and d.direction == EntranceGroups.UP)
}
