from dataclasses import dataclass
from typing import TYPE_CHECKING, Iterable
from ..data.Entrances import ENTRANCES
from ..data.Locations import LOCATIONS_DATA, LOCATION_GROUPS

if TYPE_CHECKING:
    from .. import SpiritTracksWorld

map_lookup: dict[int, str] = {
    0: "Overview",
    1: "Forest Realm",
    2: "Snow Realm",
    3: "Ocean Realm",
    4: "Fire Realm",
    5: "Ocean Undersea",

    6: "Outset Village",
    7: "Mayscore",
    8: "Mayscore Forest",
    9: "Castle Town",
    10: "Woodland Sanctuary",
    11: "Rabbit Haven",
    12: "Trading Post",

    13: "Anouki Village",
    14: "Snowfall Sanctuary",
    15: "Bridge Worker",
    16: "Icy Spring",
    17: "Slippery Station",
    18: "Snowdrift Station",

    19: "Papuzia Village",
    20: "Papuzia Archipelago",
    21: "Island Sanctuary South",
    22: "Island Sanctuary North",
    23: "Pirate Hideout",
    24: "Lost at Sea Station",

    25: "Goron Village",
    26: "Goron Field",
    27: "Valley Sanctuary",
    28: "Goron Target Range",
    29: "Disorientation Station",
    30: "Dark Ore Mine",
    31: "Ends of the Earth Station",

    32: "Dune Sanctuary",
    33: "Tower of Spirits Lobby",
    34: "Tower of Spirits",

    35: "Wooded Temple Lobby",
    36: "Wooded Temple 1F",
    37: "Wooded Temple 2F",
    38: "Wooded Temple 3F",
    39: "Wooded Temple 4F",
    40: "Stagnox Arena",

    41: "Blizzard Temple Lobby",
    42: "Blizzard Temple 1F",
    43: "Blizzard Temple B1",
    44: "Blizzard Temple 2F",
    45: "Blizzard Temple 3F",
    46: "Fraaz Arena",

    47: "Marine Temple Lobby",
    48: "Marine Temple 1F",
    49: "Marine Temple 2F",
    50: "Marine Temple 3F",
    51: "Marine Temple 4F",
    52: "Marine Temple 5F",
    53: "Marine Temple 6F",
    54: "Marine Temple 7F",
    55: "Marine Temple 2F Secret",
    56: "Cactops Arena",

    57: "Mountain Temple Lobby",
    58: "Mountain Temple 1F",
    59: "Mountain Temple 2F",
    60: "Mountain Temple B1",
    61: "Mountain Temple B2",
    62: "Mountain Temple B3",
    63: "Mountain Temple B4",
    64: "Vulcano Arena",

    65: "Desert Temple Lobby",
    66: "Desert Temple 1F",
    67: "Desert Temple 2F",
    68: "Desert Temple 3F",
    69: "Desert Temple B1",
    70: "Desert Temple B2",
    71: "Capbone Arena",
    72: "Desert Temple B4",

    73: "Tower of Spirits 1F",
    74: "Tower of Spirits 2F",
    75: "Tower of Spirits 2F Secret",
    76: "Tower of Spirits 3F",

    77: "Tower of Spirits 4F",
    78: "Tower of Spirits 5F",
    79: "Tower of Spirits 5F Secret",
    80: "Tower of Spirits 6F",
    81: "Tower of Spirits 7F",

    82: "Tower of Spirits 8F",
    83: "Tower of Spirits 8F North Secret",
    84: "Tower of Spirits 8F South Secret",
    85: "Tower of Spirits 9F",
    86: "Tower of Spirits 9F Secret",
    87: "Tower of Spirits 10F",
    88: "Tower of Spirits 11F",
    89: "Tower of Spirits 12F",

    90: "Tower of Spirits 13F",
    91: "Tower of Spirits 14F",
    92: "Tower of Spirits 15F",
    93: "Tower of Spirits 16F",
    94: "Tower of Spirits 16F Secret",
    95: "Tower of Spirits 17F",

    96: "Tower of Spirits 18F",
    97: "Tower of Spirits 19F",
    98: "Tower of Spirits 20F",
    99: "Tower of Spirits 21F",
    100: "Tower of Spirits 21F Secret",
    101: "Tower of Spirits 22F",
    102: "Tower of Spirits 23F",
    103: "Tower of Spirits Staven Arena",

    104: "Tower of Spirits 31F",
    105: "Tower of Spirits 30F",
    106: "Tower of Spirits 29F",
    107: "Tower of Spirits 29F Secret",
    108: "Tower of Spirits 30F Secret",
    109: "Tower of Spirits 28F",
    110: "Tower of Spirits 27F",
    111: "Tower of Spirits 26F",
    112: "Tower of Spirits 25F",
    113: "Tower of Spirits 24F",

    114: "Lost at Sea Lobby",
    115: "Lost at Sea 1",
    116: "Lost at Sea 2",
    117: "Lost at Sea 3",
    118: "Lost at Sea 4",
    119: "Lost at Sea 5",
    120: "Lost at Sea 6",

    121: "Niko's House",
    122: "Alfonzo's House",
    123: "Mary's House",

    124: "Mayscore Shop",
    125: "Wood's House",
    126: "Morris' House",
    127: "Dovok's House",

    128: "Gage's Sanctuary",

    129: "Castle Town Shop",
    130: "Mona's House",
    131: "Lucia's House",
    132: "Milo's House",
    133: "Take 'em All On Lobby",

    134: "Hyrule Castle Courtyard",
    135: "Hyrule Castle 1F",
    136: "Hyrule Castle 2F",
    137: "Hyrule Castle Barracks",
    138: "Hyrule Castle Infirmary",
    139: "Hyrule Castle Throne",
    140: "Zelda's Room",
    141: "Hyrule Castle Backyard",
    142: "Tunnel to ToS 1F",
    143: "Tunnel to ToS 2F",
    144: "Tunnel to ToS 3F",

    145: "Like-Like Tunnel",
    146: "Linebeck's Shop",
    147: "Linebeck's Treasure Cave",

    148: "Small Ice Puzzle Cave",
    149: "Yefu's House",
    150: "Noko's House",
    151: "Bulu's House",
    152: "Yeko's House",
    153: "Honcho's House",
    154: "Kofu's House",

    155: "Head Statue Cave",
    156: "Steem's Sanctuary",
    157: "Snowfall Supermarket",

    158: "Kenzo's House",
    159: "Ferrus' Trailer",
    160: "Skating Rink",

    161: "Snowdrift Cave",
    162: "Octive Arena",
    163: "Small Skating Cave",
    164: "Frostflame Cave",
    165: "Big Ice Puzzle Cave",

    166: "Treasure Cave",
    167: "Papuzia Shop",
    168: "Orca's House",
    169: "Wise One's House",
    170: "Fuku's House",

    171: "Crab Cave",
    172: "Carben's Sanctuary",

    173: "Disorientation 1",
    174: "Disorientation 2",
    175: "Disorientation 3",
    176: "Disorientation 4",
    177: "Disorientation 5",
    178: "Disorientation 6",
    179: "Disorientation 7",
    180: "Disorientation 8",
    181: "Disorientation 9",

    182: "Dark Ore Tunnels",

    183: "Ends of the Earth 1",
    184: "Ends of the Earth 2",
    185: "Ends of the Earth 3",
    186: "Ends of the Earth 4",
    187: "Ends of the Earth 5",
    188: "Ends of the Earth 6",
    189: "Ends of the Earth 7",
    190: "Ends of the Earth 8",
    191: "Ends of the Earth 9",
    192: "Ends of the Earth A",
    193: "Ends of the Earth B",
    194: "Ends of the Earth C",

    195: "Mountain Altar",
    196: "Goron Shop",
    197: "Kofu's New House",
    198: "Elder Goron House",
    199: "Goron 3 Pots House",
    200: "Mouldy Goron House",
    201: "Goron 2 Pots House",
    202: "Lava Goron House",
    203: "Burning Tunnel",
    204: "Embrose's Sanctuary",

    205: "Sandy Tunnel",
    206: "Rael's Sanctuary",

    207: "Dark Realm",
    208: "Cosmic Ocean",
    209: "Disorientation Dungeon",
    210: "Pirate Hangout",
    211: "Beedle"
}



@dataclass
class Interior:
    blocking_entrances: Iterable[str]
    locations: Iterable[str]
    maps: Iterable[str]


    def hide_locations(self, active_entr: list[int], hidden_locs: dict) -> dict:
        def check_entrances():
            for e in self.blocking_entrances:
                if ENTRANCES[e].id in active_entr:
                    return True
            return False

        if check_entrances():
            for m in self.maps:
                hidden_locs.setdefault(m, [])
                hidden_locs[m] += [LOCATIONS_DATA[loc]["id"] for loc in self.locations]
        return hidden_locs

@dataclass
class Enterior:
    """Portmanteau of Entrance and Interior"""
    blocking_entrances: Iterable[str]
    entrances: Iterable[str]
    maps: Iterable[str]

    def hide_entrances(self, active_entr: list[int], hidden_entrances: dict) -> dict:
        def check_entrances():
            for e in self.blocking_entrances:
                if ENTRANCES[e].id in active_entr:
                    return True
            return False

        if check_entrances():
            for m in self.maps:
                hidden_entrances.setdefault(m, [])
                hidden_entrances[m] += list(self.entrances)
        return hidden_entrances

interior_data = [
    Interior(["Outset West House"], LOCATION_GROUPS["Niko"], ["Overview", "Forest Realm"]),
    Interior(["Outset Alfonzo's Workshop"], ["Outset Ferrus Force Gem"], ["Overview", "Forest Realm"]),

    Interior(["Mayscore North House"], ["Mayscore Pick Up Dovok"], ["Overview", "Forest Realm"]),
    Interior(["Mayscore NW House"], ["Mayscore Pick Up Morris"], ["Overview", "Forest Realm"]),
    Interior(["Mayscore Shop"], LOCATION_GROUPS["Mayscore Shop"], ["Overview", "Forest Realm"]),
    Interior(["Mayscore North"], LOCATION_GROUPS["Mayscore Forest"], ["Overview", "Forest Realm"]),

    Interior(["Castle Town Take 'em all On"], LOCATION_GROUPS["Take 'em All On"], ["Overview", "Forest Realm"]),
    Interior(["Castle Town West House"], ["Castle Town Pick Up Mona"], ["Overview", "Forest Realm"]),
    Interior(["Castle Town Shop"], LOCATION_GROUPS["Castle Town Shop"], ["Overview", "Forest Realm"]),

    Interior(["Woodland Sanctuary Cave"], ["Woodland Sanctuary Song of Restoration"], ["Overview", "Forest Realm"]),

    Interior(["Anouki Village N House"], ["Anouki Village Pair Villagers", "Anouki Village Pick Up Kofu"], ["Overview", "Snow Realm"]),
    Interior(["Anouki Village Bomb Cave"], ["Anouki Village Bomb Cave Chest"], ["Overview", "Snow Realm"]),

    Interior(["Snowfall Sanctuary Shop"], LOCATION_GROUPS["Snowfall Supermarket"], ["Overview", "Snow Realm"]),
    Interior(["Snowfall Sanctuary Cave", "Head Statue Cave Door"], ["Snowfall Sanctuary Song of Restoration", "Snowfall Sanctuary Steem Gift With Snow Source"], ["Overview", "Snow Realm"]),

    Interior(["Bridge Worker's House"], ["Bridge Worker's Home Pick Up Kenzo"], ["Overview", "Snow Realm"]),
    Interior(["Slippery Station Cave"], LOCATION_GROUPS["Slippery Station"], ["Overview", "Snow Realm"]),
    Interior(["Snowdrift Station Cave"], ["Snowdrift Station Puzzle Reward"], ["Overview", "Snow Realm"]),

    Interior(["Trading Post Shop"], ["Trading Post Buy Shield", "Trading Post Deliver Dark Ore"], ["Overview", "Forest Realm"]),
    Interior(["Trading Post South Cave", "Like-Like Tunnel North"], ["Trading Post Song Statue"], ["Overview", "Forest Realm"]),
    Interior(["Trading Post South Cave", "Like-Like Tunnel North", "Trading Post Island Cave"], ["Trading Post Buried Chest"], ["Overview", "Forest Realm"]),

    Interior(["Papuzia Shop"], LOCATION_GROUPS["Papuzia Shop"], ["Overview", "Ocean Realm"]),
    Interior(["Papuzia Wise One's House"], ["Papuzia Village Buy Vessel"], ["Overview", "Ocean Realm"]),
    Interior(["Papuzia South"], LOCATION_GROUPS["Papuzia Archipelago"], ["Overview", "Ocean Realm"]),

    Interior(["Island Sanctuary South Peninsula"], ["Island Sanctuary NW Chest", "Island Sanctuary Cucco Chest", "Island Sanctuary Stamp Station"], ["Overview", "Ocean Realm"]),
    Interior(["Island Sanctuary South Peninsula", "Island Sanctuary North Cave"], ["Island Sanctuary Song of Restoration"], ["Overview", "Ocean Realm"]),

    Interior(["Lost at Sea Cave", "Lost at Sea Lobby Enter Dungeon"], LOCATION_GROUPS["LAS Dungeon"], ["Overview", "Ocean Realm"]),

    Interior(["Pirate Hideout Bomb Cave"], ["Pirate Hideout Secret Cave Right Treasure", "Pirate Hideout Secret Cave Mid Treasure", "Pirate Hideout Secret Cave Left Treasure"], ["Overview", "Ocean Realm"]),

    Interior(["Dune Sanctuary Secret Staircase", "Sandy Tunnel Left Entrance"], ["Dune Sanctuary Song of Restoration"], ["Overview", "Ocean Realm"]),

    Interior(["Goron Village Shop"], LOCATION_GROUPS["Goron Shop"], ["Overview", "Fire Realm"]),
    Interior(["Disorientation Station Cave"], ["Disorientation Station Maze Chest"], ["Overview", "Fire Realm"]),

    Interior(["Ends of the Earth Master Cave", "EotE 1 Lower Entrance", "EotE 2 Door", "EotE 3 Door"], LOCATION_GROUPS["EotE Master"], ["Overview", "Fire Realm"]),
    Interior(["Ends of the Earth Tempered Cave", "EotE 5 Lower Entrance", "EotE 6 Door", "EotE 7 Door"], LOCATION_GROUPS["EotE Tempered"], ["Overview", "Fire Realm"]),
    Interior(["Ends of the Earth Golden Cave", "EotE 9 Lower Entrance", "EotE A Door", "EotE B Door"], LOCATION_GROUPS["EotE Golden"], ["Overview", "Fire Realm"]),

    Interior(["Dark Ore Mine Left Cave", "Dark Ore Mine Center Cave", "Dark Ore Mine Right Cave"], LOCATION_GROUPS["Dark Ore Mine"], ["Overview", "Fire Realm"]),

]

enterior_data: list["Enterior"] = [
    Enterior(["Forest Realm Outset Station"], [
        "EVENT: Outset Stamp Station", "EVENT: Outset Drop Off Ferrus", "EVENT: Outset Pick Up Joe", "EVENT: Visit Outset"
    ], ["Overview", "Forest Realm"]),

    Enterior(["Forest Realm Mayscore Station", "Mayscore North"], ["EVENT: Mayscore Forest Stamp Station"], ["Overview", "Forest Realm"]),
    Enterior(["Mayscore North"], ["EVENT: Mayscore Forest Stamp Station"], ["Mayscore"]),
    Enterior(["Forest Realm Mayscore Station"], ["EVENT: Mayscore Buy Lumber"], ["Overview", "Forest Realm"]),
    Enterior(["Forest Realm Mayscore Station", "Mayscore North House"], ["EVENT: Mayscore Pick Up Dovok"], ["Overview", "Forest Realm"]),
    Enterior(["Mayscore North House"], ["EVENT: Mayscore Pick Up Dovok"], ["Mayscore"]),

    Enterior(["Forest Realm Castle Town Station"], [
        "EVENT: Castle Town Stamp Station", "EVENT: Castle Town Buy Cuccos",
        "EVENT: Visit Castle Town", "EVENT: Castle Town Pick Up Alfonzo"
    ], ["Overview", "Forest Realm"]),
    Enterior(["Forest Realm Castle Town Station", "Castle Town West House"], ["EVENT: Castle Town Pick Up Mona"], ["Overview", "Forest Realm"]),
    Enterior(["Castle Town West House"], ["EVENT: Castle Town Pick Up Mona"], ["Castle Town"]),
    Enterior(["Castle Town Take 'em all On"], ["EVENT: Complete Take 'em All On 3"], ["Castle Town"]),
    Enterior(["Forest Realm Castle Town Station", "Castle Town Take 'em all On"], ["EVENT: Complete Take 'em All On 3"], ["Overview", "Forest Realm"]),

    Enterior(["Forest Realm Woodland Sanctuary Station"], ["EVENT: Woodland Sanctuary Stamp Station"], ["Overview", "Forest Realm"]),
    Enterior(["Forest Realm Rabbit Haven Station"], ["EVENT: Visit Rabbit Haven"], ["Overview", "Forest Realm"]),

    Enterior(["Forest Realm Trading Post Station", "Trading Post South Cave"], ["EVENT: Trading Post Tunnel Stamp Station"], ["Overview", "Forest Realm"]),
    Enterior(["Trading Post South Cave"], ["EVENT: Trading Post Tunnel Stamp Station"], ["Trading Post"]),
    Enterior(["Forest Realm Trading Post Station"], ["EVENT: Visit Trading Post", "EVENT: Trading Post Drop Off Kenzo", "EVENT: Trading Post Pick Up Kenzo", "EVENT: Trading Post Give Regal Ring to Linebeck"], ["Overview", "Forest Realm"]),

    Enterior(["Forest Realm Wooded Temple Station", "Wooded Temple Lobby Enter Dungeon"], ["EVENT: Wooded Temple Stamp Station"], ["Overview", "Forest Realm"]),

    Enterior(["Snow Realm Anouki Village Station"], ["EVENT: Visit Anouki Village", "EVENT: Anouki Village Stamp Station", "EVENT: Anouki Village Pick Up Noko", "EVENT: Anouki Village Drop Off Goron"], ["Overview", "Snow Realm"]),
    Enterior(["Snow Realm Anouki Village Station", "Anouki Village N House"], ["EVENT: Anouki Village Pick Up Kofu"], ["Overview", "Snow Realm"]),
    Enterior(["Anouki Village N House"], ["EVENT: Anouki Village Pick Up Kofu"], ["Anouki Village"]),

    Enterior(["Snow Realm Snowfall Sanctuary Station"], ["EVENT: Snowfall Sanctuary Stamp Station"], ["Overview", "Snow Realm"]),
    Enterior(["Snow Realm Icy Spring Station"], [
        "EVENT: Icy Spring Stamp Station",
        "EVENT: Icy Spring Drop Off Noko",
        "EVENT: Icy Spring Buy Mega Ice",
"EVENT: Visit Icy Spring"
    ], ["Overview", "Snow Realm"]),

    Enterior(["Bridge Worker's House", "Snow Realm Bridge Worker's Station"], ["EVENT: Bridge Worker's Home Pick Up Kenzo"], ["Overview", "Snow Realm"]),
    Enterior(["Bridge Worker's House"], ["EVENT: Bridge Worker's Home Pick Up Kenzo"], ["Bridge Worker"]),

    Enterior(["Snow Realm Blizzard Temple Station", "Blizzard Temple Lobby Enter Dungeon",
              "Blizzard Temple 1F South Entrance", "Blizzard Temple 1F Main SW", "Blizzard Temple 1F SW Staircase"
              ], ["EVENT: Blizzard Temple Stamp Station"], ["Overview", "Snow Realm"]),

    Enterior(["Ocean Realm Pirate Hideout Station"], ["EVENT: Pirate Hideout Stamp Station", "EVENT: Pirate Hideout Pick Up Wadatsumi"], ["Overview", "Ocean Realm"]),

    Enterior(["Ocean Realm Papuzia Station", "Papuzia South"], ["EVENT: Papuzia Archipelago Stamp Station"], ["Overview", "Ocean Realm"]),
    Enterior(["Ocean Realm Papuzia Station", "Papuzia South"], ["EVENT: Papuzia Archipelago Stamp Station"], ["Papuzia Village"]),
    Enterior(["Ocean Realm Papuzia Station"], ["EVENT: Visit Papuzia Village", "EVENT: Papuzia Village Pick Up Carben", "EVENT: Papuzia Village Buy Fish"], ["Overview", "Ocean Realm"]),
    Enterior(["Ocean Realm Papuzia Station", "Papuzia Wise One's House"], ["EVENT: Papuzia Village Buy Vessel"], ["Overview", "Ocean Realm"]),
    Enterior(["Papuzia Wise One's House"], ["EVENT: Papuzia Village Buy Vessel"], ["Papuzia Village"]),

    Enterior(["Ocean Realm Island Sanctuary Station", "Island Sanctuary South Peninsula"],
             ["EVENT: Island Sanctuary Stamp Station"], ["Overview", "Ocean Realm"]),
    Enterior(["Island Sanctuary South Peninsula"], ["EVENT: Island Sanctuary Stamp Station"], ["Island Sanctuary South"]),
    Enterior(["Ocean Realm Island Sanctuary Station"], ["EVENT: Island Sanctuary Drop Off Carben"], ["Overview", "Ocean Realm"]),

    Enterior(["Undersea Marine Temple Station", "Ocean Realm Dive Underwater",
                "Marine Temple Lobby Enter Dungeon", "Marine Temple 1F North Staircase", "Marine Temple 2F Left Bomb Cave"
              ], ["EVENT: Marine Temple Stamp Station"], ["Overview", "Ocean Realm"]),
    Enterior(["Undersea Marine Temple Station", "Ocean Realm Dive Underwater"], ["EVENT: Marine Temple Lobby Drop Off Ferrus", "EVENT: Visit Marine Temple"], ["Overview", "Ocean Realm"]),
    Enterior(["Ocean Realm Dive Underwater", "Undersea Marine Temple Station",
        "Marine Temple Lobby Enter Dungeon", "Marine Temple 7F North Staircase"
              ], ["GOAL: Defeat Cactops", "EVENT: Defeat Cactops"], ["Overview", "Ocean Realm"]),
Enterior(["Ocean Realm Dive Underwater"], ["Undersea Marine Temple Station"], ["Overview", "Ocean Realm"]),

    Enterior(["Undersea Marine Temple Station", "Marine Temple Lobby Enter Dungeon",
              "Marine Temple 1F North Staircase", "Marine Temple 2F Left Bomb Cave"
              ], ["EVENT: Marine Temple Stamp Station"], ["Ocean Undersea"]),
    Enterior(["Undersea Marine Temple Station"],
             ["EVENT: Marine Temple Lobby Drop Off Ferrus", "EVENT: Visit Marine Temple"], ["Ocean Undersea"]),
    Enterior(["Undersea Marine Temple Station",
              "Marine Temple Lobby Enter Dungeon", "Marine Temple 7F North Staircase"
              ], ["GOAL: Defeat Cactops", "EVENT: Defeat Cactops"], ["Ocean Undersea"]),

    Enterior(["Lost at Sea Cave", "Ocean Realm Lost at Sea Station", "Lost at Sea Lobby Enter Dungeon"], ["EVENT: Complete Lost at Sea Dungeon"], ["Overview", "Ocean Realm"]),
    Enterior(["Lost at Sea Cave", "Lost at Sea Lobby Enter Dungeon"], ["EVENT: Complete Lost at Sea Dungeon"], ["Lost at Sea Station"]),
Enterior(["Lost at Sea Lobby Enter Dungeon"], ["EVENT: Complete Lost at Sea Dungeon"], ["Lost at Sea Lobby"]),

    Enterior(["Fire Realm Goron Village Station", "Goron Village West"], ["EVENT: Goron Field Stamp Station", "EVENT: Goron Field Buy Steel"], ["Overview", "Fire Realm"]),
    Enterior(["Goron Village West"], ["EVENT: Goron Field Stamp Station", "EVENT: Goron Field Buy Steel"], ["Goron Village"]),
    Enterior(["Fire Realm Goron Village Station", "Goron Village Enclave North",
              "Goron Village Elder's House", "Elder Goron House Cave", "Burning Tunnel East Staircase"
              ], ["EVENT: Valley Sanctuary Stamp Station"], ["Overview", "Fire Realm"]),
    Enterior(["Goron Village Enclave North"], ["EVENT: Valley Sanctuary Stamp Station"], ["Goron Village"]),
    Enterior(["Fire Realm Goron Village Station"], [
        "EVENT: Goron Village Pick Up Snow Goron", "EVENT: Goron Village Pick Up City Goron", "EVENT: Goron Village Bring Ice to Kagoron", "EVENT: Visit Goron Village"
    ], ["Overview", "Fire Realm"]),
    Enterior(["Fire Realm Goron Village Station", "Goron Village West", "Goron Field North"], ["EVENT: Mountain Altar Visit Kagoron"], ["Overview", "Fire Realm"]),
    Enterior(["Goron Village West", "Goron Field North"], ["EVENT: Mountain Altar Visit Kagoron"], ["Goron Village"]),
    Enterior(["Goron Field North"], ["EVENT: Mountain Altar Visit Kagoron"], ["Goron Field"]),

    Enterior(["Fire Realm Disorientation Station", "Disorientation Station Cave"], ["EVENT: Disorientation Maze Find Chest"], ["Overview", "Fire Realm"]),
    Enterior(["Disorientation Station Cave"], ["EVENT: Disorientation Maze Find Chest"], ["Disorientation Station"]),

    Enterior(["Fire Realm Dark Ore Mine Station", "Dark Ore Mine Left Cave", "Dark Ore Mine Center Cave", "Dark Ore Mine Right Cave"], ["EVENT: Dark Ore Mine Buy Ore"], ["Overview", "Fire Realm"]),
    Enterior(["Dark Ore Mine Left Cave", "Dark Ore Mine Center Cave", "Dark Ore Mine Right Cave"], ["EVENT: Dark Ore Mine Buy Ore"], ["Dark Ore Mine"]),

    Enterior(["Fire Realm Mountain Temple Station", "Mountain Temple Lobby Enter Dungeon",
                "Mountain Temple 1F Central Staircase", "Mountain Temple 2F NE Staircase", "Mountain Temple 1F North Staircase"
              ], ["EVENT: Mountain Temple Stamp Station"], ["Overview", "Fire Realm"]),

    Enterior(["Ocean Realm Dune Sanctuary Station"], ["EVENT: Dune Sanctuary Stamp Station", "EVENT: Dune Sanctuary Deliver Cuccos"], ["Overview", "Ocean Realm"]),
    Enterior(["Ocean Realm Desert Temple Station", "Desert Temple Lobby Enter Dungeon", "Desert Temple 1F Lower Staircase"],
             ["EVENT: Desert Temple Stamp Station"],["Overview", "Ocean Realm"]),
]

station_section_link: dict[str, str] = {  # Location section: blocking entrances
    "Overview Castle Town": "Forest Realm Castle Town Station",
    "Overview Hyrule Castle": ["Forest Realm Castle Town Station", "Castle Town North", "Hyrule Castle Courtyard Entrance"],
    "Overview Outset": "Forest Realm Outset Station",
    "Overview Mayscore": "Forest Realm Mayscore Station",
    "Overview Woodland": "Forest Realm Woodland Sanctuary Station",
    "Overview Rabbit Haven": "Forest Realm Rabbit Haven Station",
    "Overview Trading Post": "Forest Realm Trading Post Station",
    "Overview WT": ["Forest Realm Wooded Temple Station", "Wooded Temple Lobby Enter Dungeon"],

    "Overview Anouki": "Snow Realm Anouki Village Station",
    "Overview Snowfall": "Snow Realm Snowfall Sanctuary Station",
    "Overview BT": ["Snow Realm Blizzard Temple Station", "Blizzard Temple Lobby Enter Dungeon"],
    "Overview Icyspring": "Snow Realm Icy Spring Station",
    "Overview Snowdrift": "Snow Realm Snowdrift Station",
    "Overview Slippery": "Snow Realm Slippery Station",
    "Overview Kenzo": "Snow Realm Bridge Worker's Station",

    "Overview Papuzia": "Ocean Realm Papuzia Station",
    "Overview Island": "Ocean Realm Island Sanctuary Station",
    "Overview OCT": ["Undersea Marine Temple Station", "Marine Temple Lobby Enter Dungeon"],
    "Overview Pirate": "Ocean Realm Pirate Hideout Station",
    "Overview LAS": "Ocean Realm Lost at Sea Station",
    "Overview Dune": "Ocean Realm Dune Sanctuary Station",
    "Overview DT": ["Ocean Realm Desert Temple Station", "Desert Temple Lobby Enter Dungeon"],

    "Overview Disorientation": "Fire Realm Disorientation Station",
    "Overview EotE": "Fire Realm Ends of the Earth Station",
    "Overview DOM": "Fire Realm Dark Ore Mine Station",
    "Overview Goron": "Fire Realm Goron Village Station",
    "Overview Goron Field": ["Goron Village West", "Fire Realm Goron Village Station"],
    "Overview Valley": ["Fire Realm Goron Village Station", "Goron Village Enclave North", "Elder Goron House Cave", "Goron Village Elder's House"],
    "Overview GTR": "Fire Realm Goron Target Range Station",
    "Overview MTT": ["Fire Realm Mountain Temple Station", "Mountain Temple Lobby Enter Dungeon"],

    "Lost at Sea Station Cave": ["Lost at Sea Lobby Enter Dungeon"],
}

boss_event_link: dict[str, list[str]] = {  # entrance section: blocking entrances
    "Overview WT Events": [
        "Forest Realm Wooded Temple Station",
        "Wooded Temple Lobby Enter Dungeon",
        "Wooded Temple 4F N Staircase"],
    "Overview BT Events": [
        "Snow Realm Blizzard Temple Station",
        "Blizzard Temple Lobby Enter Dungeon",
        "Blizzard Temple 3F North Staircase"],
    "Overview MTT Events": [
        "Fire Realm Mountain Temple Station",
        "Mountain Temple Lobby Enter Dungeon",
        "Mountain Temple B4 North Staircase"],
    "Overview DT Events": [
        "Ocean Realm Desert Temple Station",
        "Desert Temple Lobby Enter Dungeon",
        "Desert Temple B2 North Entrance"],
}

def get_hidden_map_icons(world: "SpiritTracksWorld"):
    import json
    import pkgutil
    pack_name = world.__class__.__module__

    def get_json(files):
        res = []
        for f in files:
            res += json.loads(
                pkgutil.get_data(
                    pack_name,
                    f"/tracker/{f}").decode('utf-8-sig'))
        return res

    entr_data = get_json(["entrances/entrances.json"])
    loc_data = get_json(["locations/overworld.json"])
    active_entrances = [int(i) for i in world.ut_pairings]
    entr_hidden: dict[str, list[str]] = {}
    locs_hidden: dict[str, list[int]] = {}  # map_name: [loc_ids]
    events_hidden = {}
    map_coord_checks: dict[str, list[tuple[int, int]]] = {}

    # Handle entrances
    for entrance in entr_data:
        entr_section = entrance.get("name")
        entr_names = [s.get("name") for s in entrance.get("sections", [])]
        map_locs = [m for m in entrance.get("map_locations", [])]
        map_loc_names = [m["map"] for m in map_locs]

        for entr_name in entr_names:
            if entr_name not in ENTRANCES:
                print(f"Wrong Entrance in tracker data: {entr_name}")
            elif ENTRANCES[entr_name].id not in active_entrances:
                for map_loc in map_loc_names:
                    entr_hidden.setdefault(map_loc, []).append(entr_name)
            else:
                for map_loc in map_locs:
                    if world.options.randomize_stamps.value == 1 and entr_name.endswith("Stamp Station"):
                        entr_hidden.setdefault(map_loc["map"], []).append(entr_name)
                    elif world.options.rabbitsanity.value in [3, 4] and entr_name.startswith("EVENT: Rabbit"):
                        continue
                    else:
                        coords = (map_loc["x"], map_loc["y"])
                        map_coord_checks.setdefault(map_loc["map"], []).append(coords)



        # Filter out stations using station_section_link
        if entr_section in boss_event_link:
            blocking_entrances = [ENTRANCES[e].id for e in boss_event_link[entr_section]]
            for blocking_entrance in blocking_entrances:
                if blocking_entrance in active_entrances:
                    for loc_map in map_loc_names:
                        entr_hidden.setdefault(loc_map, [])
                        entr_hidden[loc_map] += entr_names

    # print(f"map_coord_checks: {map_coord_checks}")

    # Handle locations and coord check entrances
    for loc in loc_data:
        loc_section = loc["name"]
        loc_names = [s.get("name") for s in loc.get("sections", [])]
        loc_map_locations = loc.get("map_locations")
        loc_maps = [l["map"] for l in loc_map_locations]
        loc_coords = [(l["x"], l["y"]) for l in loc_map_locations]

        # Filter out stations using station_section_link
        if loc_section in station_section_link:
            _e = station_section_link[loc_section]
            _e = _e if isinstance(_e, list) else [_e]
            blocking_entrances = [ENTRANCES[i].id for i in _e]
            for blocking_entrance in blocking_entrances:
                if blocking_entrance in active_entrances:
                    for loc_map in loc_maps:
                        locs_hidden.setdefault(loc_map, [])
                        locs_hidden[loc_map] += [world.location_name_to_id[n] for n in loc_names]

        for loc_map in loc_maps:
            if loc_map in map_coord_checks:
                # print(f"Testing {loc_map} coords {loc_coords} in {[i for i in map_coord_checks[loc_map]]}")
                coords_in_map = [i for i in map_coord_checks[loc_map]]
                for c in loc_coords:
                    if c in coords_in_map:
                        loc_ids = []
                        for loc2 in loc_names:
                            if "EVENT" in loc2 or "GOAL" in loc2:
                                entr_hidden.setdefault(loc_map, []).append(loc2)
                            else:
                                loc_ids.append(world.location_name_to_id[loc2])
                        locs_hidden.setdefault(loc_map, [])
                        locs_hidden[loc_map] += loc_ids


    # Hard coded examples
    if world.options.rabbitsanity.value == 4 and "rabbits" in world.options.extra_events.value:
        realm_lookup = {
            4: "Forest Realm",
            5: "Snow Realm",
            6: "Ocean Realm",
            7: "Fire Realm"
        }
        for rabbit_loc in LOCATION_GROUPS["Unique Rabbits"]:
            if rabbit_loc in world.active_rabbit_locations:
                entr_hidden.setdefault("Overview", []).append(f"EVENT: {rabbit_loc}")
                entr_hidden.setdefault(realm_lookup[LOCATIONS_DATA[rabbit_loc]["stage_id"]], []).append(f"EVENT: {rabbit_loc}")

    # Hide interiors from overview
    for data in interior_data:
        locs_hidden = data.hide_locations(active_entrances, locs_hidden)

    for data in enterior_data:
        entr_hidden = data.hide_entrances(active_entrances, entr_hidden)

    # print(f"hidden entrances: {entr_hidden}")
    return locs_hidden, entr_hidden