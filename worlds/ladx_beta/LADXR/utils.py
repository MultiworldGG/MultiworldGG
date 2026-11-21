import unicodedata
import re
from typing import Optional

from .locations.items import *

class Error(Exception):
    pass


AP_NAMES = {
    SWORD: "Progressive Sword",
    BOMB: "Bombs",
    POWER_BRACELET: "Progressive Power Bracelet",
    SHIELD: "Progressive Shield",
    BOW: "Bow",
    HOOKSHOT: "Hookshot",
    MAGIC_ROD: "Magic Rod",
    PEGASUS_BOOTS: "Pegasus Boots",
    OCARINA: "Ocarina",
    FEATHER: "Feather",
    SHOVEL: "Shovel",
    MAGIC_POWDER: "Magic Powder",
    BOOMERANG: "Boomerang",
    ROOSTER: "Rooster",

    FLIPPERS: "Flippers",
    SLIME_KEY: "Slime Key",
    TAIL_KEY: "Tail Key",
    ANGLER_KEY: "Angler Key",
    FACE_KEY: "Face Key",
    BIRD_KEY: "Bird Key",
    GOLD_LEAF: "Gold Leaf",

    "RUPEE": "Rupee",
    "RUPEES": "Rupees",
    RUPEES_50: "50 Rupees",
    RUPEES_20: "20 Rupees",
    RUPEES_100: "100 Rupees",
    RUPEES_200: "200 Rupees",
    RUPEES_500: "500 Rupees",
    SEASHELL: "Seashell",

    KEY: "Small Key",
    KEY1: "Small Key (Tail Cave)",
    KEY2: "Small Key (Bottle Grotto)",
    KEY3: "Small Key (Key Cavern)",
    KEY4: "Small Key (Angler's Tunnel)",
    KEY5: "Small Key (Catfish's Maw)",
    KEY6: "Small Key (Face Shrine)",
    KEY7: "Small Key (Eagle's Tower)",
    KEY8: "Small Key (Turtle Rock)",
    KEY9: "Small Key (Color Dungeon)",

    MAP: "Dungeon Map",
    MAP1: "Dungeon Map (Tail Cave)",
    MAP2: "Dungeon Map (Bottle Grotto)",
    MAP3: "Dungeon Map (Key Cavern)",
    MAP4: "Dungeon Map (Angler's Tunnel)",
    MAP5: "Dungeon Map (Catfish's Maw)",
    MAP6: "Dungeon Map (Face Shrine)",
    MAP7: "Dungeon Map (Eagle's Tower)",
    MAP8: "Dungeon Map (Turtle Rock)",
    MAP9: "Dungeon Map (Color Dungeon)",

    COMPASS: "Dungeon Compass",
    COMPASS1: "Compass (Tail Cave)",
    COMPASS2: "Compass (Bottle Grotto)",
    COMPASS3: "Compass (Key Cavern)",
    COMPASS4: "Compass (Angler's Tunnel)",
    COMPASS5: "Compass (Catfish's Maw)",
    COMPASS6: "Compass (Face Shrine)",
    COMPASS7: "Compass (Eagle's Tower)",
    COMPASS8: "Compass (Turtle Rock)",
    COMPASS9: "Compass (Color Dungeon)",

    STONE_BEAK: "Stone Beak",
    STONE_BEAK1: "Stone Beak (Tail Cave)",
    STONE_BEAK2: "Stone Beak (Bottle Grotto)",
    STONE_BEAK3: "Stone Beak (Key Cavern)",
    STONE_BEAK4: "Stone Beak (Angler's Tunnel)",
    STONE_BEAK5: "Stone Beak (Catfish's Maw)",
    STONE_BEAK6: "Stone Beak (Face Shrine)",
    STONE_BEAK7: "Stone Beak (Eagle's Tower)",
    STONE_BEAK8: "Stone Beak (Turtle Rock)",
    STONE_BEAK9: "Stone Beak (Color Dungeon)",

    NIGHTMARE_KEY: "Nightmare Key",
    NIGHTMARE_KEY1: "Nightmare Key (Tail Cave)",
    NIGHTMARE_KEY2: "Nightmare Key (Bottle Grotto)",
    NIGHTMARE_KEY3: "Nightmare Key (Key Cavern)",
    NIGHTMARE_KEY4: "Nightmare Key (Angler's Tunnel)",
    NIGHTMARE_KEY5: "Nightmare Key (Catfish's Maw)",
    NIGHTMARE_KEY6: "Nightmare Key (Face Shrine)",
    NIGHTMARE_KEY7: "Nightmare Key (Eagle's Tower)",
    NIGHTMARE_KEY8: "Nightmare Key (Turtle Rock)",
    NIGHTMARE_KEY9: "Nightmare Key (Color Dungeon)",

    HEART_PIECE: "Piece of Heart",
    BOWWOW: "Bowwow",
    ARROWS_10: "10 Arrows",
    SINGLE_ARROW: "Single Arrow",
    MEDICINE: "Medicine",

    MAX_POWDER_UPGRADE: "Max Powder Upgrade",
    MAX_BOMBS_UPGRADE: "Max Bombs Upgrade",
    MAX_ARROWS_UPGRADE: "Max Arrows Upgrade",

    RED_TUNIC: "Red Tunic",
    BLUE_TUNIC: "Blue Tunic",

    HEART_CONTAINER: "Heart Container",
    BAD_HEART_CONTAINER: "Anti-Heart Container",

    TOADSTOOL: "Toadstool",

    SONG1: "Ballad of the Wind Fish",
    SONG2: "Manbo's Mambo",
    SONG3: "Frog's Song of Soul",

    INSTRUMENT1: "Full Moon Cello",
    INSTRUMENT2: "Conch Horn",
    INSTRUMENT3: "Sea Lily's Bell",
    INSTRUMENT4: "Surf Harp",
    INSTRUMENT5: "Wind Marimba",
    INSTRUMENT6: "Coral Triangle",
    INSTRUMENT7: "Organ of Evening Calm",
    INSTRUMENT8: "Thunder Drum",

    TRADING_ITEM_YOSHI_DOLL: "Yoshi Doll",
    TRADING_ITEM_RIBBON: "Ribbon",
    TRADING_ITEM_DOG_FOOD: "Dog Food",
    TRADING_ITEM_BANANAS: "Bananas",
    TRADING_ITEM_STICK: "Stick",
    TRADING_ITEM_HONEYCOMB: "Honeycomb",
    TRADING_ITEM_PINEAPPLE: "Pineapple",
    TRADING_ITEM_HIBISCUS: "Hibiscus",
    TRADING_ITEM_LETTER: "Letter",
    TRADING_ITEM_BROOM: "Broom",
    TRADING_ITEM_FISHING_HOOK: "Fishing Hook",
    TRADING_ITEM_NECKLACE: "Necklace",
    TRADING_ITEM_SCALE: "Scale",
    TRADING_ITEM_MAGNIFYING_GLASS: "Magnifying Glass",
    
    GUARDIAN_ACORN: "Guardian Acorn",
    PIECE_OF_POWER: "Piece of Power",
    RECOVERY_HEART: "Recovery Heart",
    FAIRY: "Fairy",

    DEATH: "Death",
    GEL: "Zol Attack",
    SLIME_STORM: "Slime Storm",
    BOMB_DROP: "Bomb Drop",
    CUCCO_PARTY: "Cucco Party",

    MESSAGE: "Nothing",
}

# Small Key (Bottle Grotto) -> Key to Bottle Grotto
# Progressive Sword -> Sword
_NAMES = {k: re.sub(r"(.*)\((.*)\)", r"\1to \2", v).replace("Small ", "").replace("Progressive ", "")
    for k, v in AP_NAMES.items()}

_PREFILTER = {
    'à': '<agrave>',
    'â': '<acirc>',
    'ä': '<auml>',
    'è': '<egrave>',
    'é': '<eacute>',
    'ê': '<ecirc>',
    'ù': '<ugrave>',
    'û': '<ucirc>',
    'ü': '<uuml>',
    'ô': '<ocirc>',
    'ö': '<ouml>',
    'ç': '<ccedil>',
    'î': '<icirc>',
    'ß': '<szlig>',
    'ẞ': '<szlig>',
    'Ä': '<Auml>',
    'Ö': '<Ouml>',
    'Ü': '<Uuml>',
    'Ø': 'O',
    'ø': 'o',
    'Æ': 'AE',
    'æ': 'ae',
    'Œ': 'OE',
    'œ': 'oe',
    'Ł': 'L',
    'ł': 'l',
    'Đ': 'D',
    'đ': 'd',
    '“': '<dquote>',
    '”': '<dquote>',
    '"': '<dquote>',
    '‘': "'",
    '’': "'",
    '–': '-',
    '—': '-',
    '…': '...',
    '©': '(c)',
    '№': 'No.',
    '§': 'S',
    '×': 'x',
    '°': 'deg',
    '{': '(',
    '}': ')',
    '[': '(',
    ']': ')',
    '💀': '<master>',
    '👦': '<link>',
    '👧': '<marin>',
    '👨': '<tarkin>',
    '🎀': '<ribbon>',
    '🥫': '<dogfood>',
    '🍌': '<bananas>',
    '🍍': '<pineapple>',
    '🌺': '<hibiscus>',
    '🧹': '<broom>',
    '🪝': '<hook>',
    '✉️': '<letter>',
    '🔎': '<glass>',
    '⬆️': '<arrowU>',
    '⬇️': '<arrowD>',
    '⬅️': '<arrowL>',
    '➡️': '<arrowR>',
}

_CHARACTERS = {
    b"'":  b"^",
    b'<agrave>': b'\x80',
    b'<acirc>' : b'\x81',
    b'<auml>'  : b'\x82',
    b'<egrave>': b'\x83',
    b'<eacute>': b'\x84',
    b'<ecirc>' : b'\x85',
    b'<ugrave>': b'\x86',
    b'<ucirc>' : b'\x87',
    b'<uuml>'  : b'\x88',
    b'<ocirc>' : b'\x89',
    b'<ouml>'  : b'\x8A',
    b'<ccedil>': b'\x8B',
    b'<icirc>' : b'\x8C',
    b'<szlig>' : b'\x8D',
    b'<Auml>'  : b'\x8E',
    b'<Ouml>'  : b'\x8F',
    b'<Uuml>'  : b'\x90',
    b'<dquote>': b'\x91',
    b'<bigA>'  : b'\xD0',
    b'<bigB>'  : b'\xD1',
    b'<bigC>'  : b'\xD2',
    b'<bigD>'  : b'\xD3',
    b'<bigE>'  : b'\xD4',
    b'<bigF>'  : b'\xD5',
    b'<foot>'  : b'\xDA',
    b'<master>': b'\xDC',
    b'<link>'  : b'\xDD',
    b'<marin>' : b'\xDE',
    b'<tarkin>': b'\xDF',
    b'<yoshi>' : b'\xE0',
    b'<ribbon>': b'\xE1',
    b'<dogfood>':b'\xE2',
    b'<bananas>': b'\xE3',
    b'<stick>' : b'\xE4',
    b'<honeycomb>': b'\xE5',
    b'<pineapple>': b'\xE6',
    b'<hibiscus>': b'\xE7',
    b'<broom>' : b'\xE8',
    b'<hook>'  : b'\xE9',
    b'<necklace>':b'\xEA',
    b'<scale>' : b'\xEB',
    b'<glass>' : b'\xEC',
    b'<letter>': b'\xED',
    b'<dpad>'  : b'\xEE',
    b'<arrowU>': b'\xF0',
    b'<arrowD>': b'\xF1',
    b'<arrowL>': b'\xF2',
    b'<arrowR>': b'\xF3',
}

def setReplacementName(key: str, value: str) -> None:
    _NAMES[key] = value

def preformatText(instr: str, skip_names: bool = False) -> bytes:
    if not skip_names:
        instr = instr.format(**_NAMES)
    for character, replacement in _PREFILTER.items():
        instr = instr.replace(character, replacement)
    s = unicodedata.normalize("NFKD", instr).encode("ascii", "ignore")
    for character, encodedCharacter in _CHARACTERS.items():
        s = s.replace(character, encodedCharacter)
    return s

def formatText(instr: str, *, center: bool = False, ask: Optional[str] = None, skip_names: bool = False) -> bytes:
    s = preformatText(instr, skip_names)

    def padLine(line: bytes) -> bytes:
        return line + b' ' * (16 - len(line))
    if center:
        def padLine(line: bytes) -> bytes:
            padding = (16 - len(line))
            return b' ' * (padding // 2) + line + b' ' * (padding - padding // 2)

    result = b''
    for line in s.split(b'\n'):
        result_line = b''
        for word in line.split(b' '):
            if len(result_line) + 1 + len(word) > 16:
                result += padLine(result_line)
                result_line = b''
            elif result_line:
                result_line += b' '
            result_line += word
        if result_line:
            result += padLine(result_line)
    if ask is not None:
        askbytes = ask.encode("ascii")
        result = result.rstrip()
        while len(result) % 16 != 0:
            result += b' '
        return result + b'    ' + askbytes + b'\xfe'
    return result.replace(b'_', b' ').rstrip() + b'\xff'


def tileDataToString(data: bytes, key: str = " 123") -> str:
    result = ""
    for n in range(0, len(data), 2):
        a = data[n]
        b = data[n+1]
        for m in range(8):
            bit = 0x80 >> m
            if (a & bit) and (b & bit):
                result += key[3]
            elif (b & bit):
                result += key[2]
            elif (a & bit):
                result += key[1]
            else:
                result += key[0]
        result += "\n"
    return result.rstrip("\n")


def createTileData(data: str, key: str = " 123") -> bytes:
    result = []
    for line in data.split("\n"):
        line = line + "        "
        a = 0
        b = 0
        for n in range(8):
            if line[n] == key[3]:
                a |= 0x80 >> n
                b |= 0x80 >> n
            elif line[n] == key[2]:
                b |= 0x80 >> n
            elif line[n] == key[1]:
                a |= 0x80 >> n
        result.append(a)
        result.append(b)
    assert (len(result) % 16) == 0, len(result)
    return bytes(result)


if __name__ == "__main__":
    data = formatText("It is dangurous to go alone.\nTake\nthis\na\nline.")
    for i in range(0, len(data), 16):
        print(data[i:i+16])
