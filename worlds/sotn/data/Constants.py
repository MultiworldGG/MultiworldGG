CURRENT_VERSION = "0.8.16"
# This is applied to helmet, armor, cloak, and other ids that are sold in
# the librarian's shop menu or are in an equipment slot
equip_id_offset = -0xa9
# This is applied to equipment ids to get the inventory slot it occupies
equip_inv_id_offset = 0x798a

shop_item_data = {
    1: {
        "itemName": "Potion",
        "itemPriceH": 0x00000320,
        "itemPriceD": 800,
        "priceAddress": 0x047a30a0,
    },
    2: {
        "itemName": "High potion",
        "itemPriceH": 0x000007d0,
        "itemPriceD": 2000,
        "priceAddress": 0x047a30a8,
    },
    3: {
        "itemName": "Elixir",
        "itemPriceH": 0x00001f40,
        "itemPriceD": 8000,
        "priceAddress": 0x047a30b0,
    },
    4: {
        "itemName": "Manna prism",
        "itemPriceH": 0x00000fa0,
        "itemPriceD": 4000,
        "priceAddress": 0x047a30b8,
    },
    5: {
        "itemName": "Antivenom",
        "itemPriceH": 0x000000c8,
        "itemPriceD": 200,
        "priceAddress": 0x047a30c0,
    },
    6: {
        "itemName": "Uncurse",
        "itemPriceH": 0x000000c8,
        "itemPriceD": 200,
        "priceAddress": 0x047a30c8,
    },
    7: {
        "itemName": "Hammer",
        "itemPriceH": 0x000000c8,
        "itemPriceD": 200,
        "priceAddress": 0x047a30d0,
    },
    8: {
        "itemName": "Magic Missile",
        "itemPriceH": 0x0000012c,
        "itemPriceD": 300,
        "priceAddress": 0x047a30d8,
    },
    9: {
        "itemName": "Bwaka knife",
        "itemPriceH": 0x00000190,
        "itemPriceD": 400,
        "priceAddress": 0x047a30e0,
    },
    10: {
        "itemName": "Boomerang",
        "itemPriceH": 0x000001f4,
        "itemPriceD": 500,
        "priceAddress": 0x047a30e8,
    },
    11: {
        "itemName": "Javelin",
        "itemPriceH": 0x00000320,
        "itemPriceD": 800,
        "priceAddress": 0x047a30f0,
    },
    12: {
        "itemName": "Fire boomerang",
        "itemPriceH": 0x000003e8,
        "itemPriceD": 1000,
        "priceAddress": 0x047a30f8,
    },
    13: {
        "itemName": "Shuriken",
        "itemPriceH": 0x00000960,
        "itemPriceD": 2400,
        "priceAddress": 0x047a3100,
    },
    14: {
        "itemName": "Cross shuriken",
        "itemPriceH": 0x00001388,
        "itemPriceD": 2400,
        "priceAddress": 0x047a3100,
    },
    15: {
        "itemName": "Buffalo star",
        "itemPriceH": 0x00001388,
        "itemPriceD": 5000,
        "priceAddress": 0x047a3108,
    },
    16: {
        "itemName": "Flame star",
        "itemPriceH": 0x00001f40,
        "itemPriceD": 8000,
        "priceAddress": 0x047a3110,
    },
    17: {
        "itemName": "Library card",
        "itemPriceH": 0x000001f4,
        "itemPriceD": 500,
        "priceAddress": 0x047a3120,
    },
    18: {
        "itemName": "Meal ticket",
        "itemPriceH": 0x000007d0,
        "itemPriceD": 2000,
        "priceAddress": 0x047a3128,
    },
    19: {
        "itemName": "Saber",
        "itemPriceH": 0x000005dc,
        "itemPriceD": 1500,
        "priceAddress": 0x047a3130,
    },
    20: {
        "itemName": "Mace",
        "itemPriceH": 0x000007d0,
        "itemPriceD": 2000,
        "priceAddress": 0x047a3138,
    },
    21: {
        "itemName": "Damascus sword",
        "itemPriceH": 0x00000fa0,
        "itemPriceD": 4000,
        "priceAddress": 0x047a3140,
    },
    22: {
        "itemName": "Firebrand",
        "itemPriceH": 0x00002710,
        "itemPriceD": 10000,
        "priceAddress": 0x047a3148,
    },
    23: {
        "itemName": "Icebrand",
        "itemPriceH": 0x00002710,
        "itemPriceD": 10000,
        "priceAddress": 0x047a3150,
    },
    24: {
        "itemName": "Thunderbrand",
        "itemPriceH": 0x00002710,
        "itemPriceD": 10000,
        "priceAddress": 0x047a3158,
    },
    25: {
        "itemName": "Harper",
        "itemPriceH": 0x00002ee0,
        "itemPriceD": 12000,
        "priceAddress": 0x047a3160,
    },
    26: {
        "itemName": "Leather shield",
        "itemPriceH": 0x00000190,
        "itemPriceD": 400,
        "priceAddress": 0x047a3168,
    },
    27: {
        "itemName": "Iron shield",
        "itemPriceH": 0x00000fbc,
        "itemPriceD": 3980,
        "priceAddress": 0x047a3170,
    },
    28: {
        "itemName": "Velvet hat",
        "itemPriceH": 0x00000190,
        "itemPriceD": 400,
        "priceAddress": 0x047a3178,
    },
    29: {
        "itemName": "Leather hat",
        "itemPriceH": 0x000003e8,
        "itemPriceD": 1000,
        "priceAddress": 0x047a3180,
    },
    30: {
        "itemName": "Circlet",
        "itemPriceH": 0x00000fa0,
        "itemPriceD": 4000,
        "priceAddress": 0x047a3188,
    },
    31: {
        "itemName": "Silver crown",
        "itemPriceH": 0x00002ee0,
        "itemPriceD": 12000,
        "priceAddress": 0x047a3190,
    },
    32: {
        "itemName": "Iron cuirass",
        "itemPriceH": 0x000005dc,
        "itemPriceD": 1500,
        "priceAddress": 0x047a3198,
    },
    33: {
        "itemName": "Steel cuirass",
        "itemPriceH": 0x00000fa0,
        "itemPriceD": 4000,
        "priceAddress": 0x047a31a0,
    },
    34: {
        "itemName": "Diamond plate",
        "itemPriceH": 0x00002ee0,
        "itemPriceD": 12000,
        "priceAddress": 0x047a31a8,
    },
    35: {
        "itemName": "Reverse cloak",
        "itemPriceH": 0x000007d0,
        "itemPriceD": 2000,
        "priceAddress": 0x047a31b0,
    },
    36: {
        "itemName": "Elven cloak",
        "itemPriceH": 0x00000bb8,
        "itemPriceD": 3000,
        "priceAddress": 0x047a31b8,
    },
    37: {
        "itemName": "Joseph's cloak",
        "itemPriceH": 0x00007530,
        "itemPriceD": 30000,
        "priceAddress": 0x047a31c0,
    },
    38: {
        "itemName": "Medal",
        "itemPriceH": 0x00000bb8,
        "itemPriceD": 3000,
        "priceAddress": 0x047a31c8,
    },
    39: {
        "itemName": "Ring of Pales",
        "itemPriceH": 0x00000fa0,
        "itemPriceD": 4000,
        "priceAddress": 0x047a31d0,
    },
    40: {
        "itemName": "Gauntlet",
        "itemPriceH": 0x00001f40,
        "itemPriceD": 8000,
        "priceAddress": 0x047a31d8,
    },
    41: {
        "itemName": "Duplicator",
        "itemPriceH": 0x0007a120,
        "itemPriceD": 500000,
        "priceAddress": 0x047a31e0,
    },
}

start_room_data = {
    1: {
        "comment": "Bottom of Forbidden Route",
        "stage": 0x00,  # Marble Gallery
        "room": 0,
        "xPos": 48,
        "yPos": 644,
        "xyWrite": 0x02840030,
        "roomWrite": 0x00410000,
        "stageWrite": 0x0000
    },
    "2": {
        "comment":  "Top of Spirit Orb room",
        "stage":  0x00,                                                                 # Marble Gallery
        "room":  2,
        "xPos":  332,
        "yPos":  244,
        "xyWrite":  0x00F4014C,
        "roomWrite":  0x00410010,
        "stageWrite":  0x0000
    },
    "3": {
        "comment":  "Middle of the long hallway",
        "stage":  0x00,                                                                 # Marble Gallery
        "room":  8,
        "xPos":  1920,
        "yPos":  164,
        "xyWrite":  0x00a40780,
        "roomWrite":  0x00410040,
        "stageWrite":  0x0000
    },
    "4": {
        "comment":  "Alucart room",
        "stage":  0x00,                                                                 # Marble Gallery
        "room":  14,
        "xPos":  128,
        "yPos":  164,
        "xyWrite":  0x00a40080,
        "roomWrite":  0x00410070,
        "stageWrite":  0x0000
    },
    "5": {
        "comment":  "Gravity Boots items",
        "stage":  0x00,                                                                 # Marble Gallery
        "room":  20,
        "xPos":  192,
        "yPos":  148,
        "xyWrite":  0x009400c0,
        "roomWrite":  0x004100a0,
        "stageWrite":  0x0000
    },
    "6": {
        "comment":  "Same room but across from Telescope",
        "stage":  0x01,                                                                 # Outer Wall
        "room":  3,
        "xPos":  724,
        "yPos":  164,
        "xyWrite":  0x00A402D4,
        "roomWrite":  0x00410018,
        "stageWrite":  0x0001
    },
    "7": {
        "comment":  "Secret elevator room",
        "stage":  0x01,                                                                 # Outer Wall
        "room":  6,
        "xPos":  56,
        "yPos":  164,
        "xyWrite":  0x00a40038,
        "roomWrite":  0x00410030,
        "stageWrite":  0x0001
    },
    "8": {
        "comment":  "Gladius room",
        "stage":  0x01,                                                                 # Outer Wall
        "room":  12,
        "xPos":  128,
        "yPos":  164,
        "xyWrite":  0x00A40080,
        "roomWrite":  0x00410060,
        "stageWrite":  0x0001
    },
    "9": {
        "comment":  "Bookshelf room",
        "stage":  0x02,                                                                 # Long Library
        "room":  1,
        "xPos":  88,
        "yPos":  148,
        "xyWrite":  0x00940058,
        "roomWrite":  0x00410008,
        "stageWrite":  0x0002
    },
    "10": {
        "comment":  "Shop hallway",
        "stage":  0x02,                                                                 # Long Library
        "room":  5,
        "xPos":  16,
        "yPos":  148,
        "xyWrite":  0x00940010,
        "roomWrite":  0x00410028,
        "stageWrite":  0x0002
    },
    "11": {
        "comment":  "Faerie Card room",
        "stage":  0x02,                                                                 # Long Library
        "room":  7,
        "xPos":  208,
        "yPos":  148,
        "xyWrite":  0x009400D0,
        "roomWrite":  0x00410038,
        "stageWrite":  0x0002
    },
    "12": {
        "comment":  "One-dollar room",
        "stage":  0x03,                                                                 # Catacombs
        "room":  5,
        "xPos":  100,
        "yPos":  164,
        "xyWrite":  0x00A40064,
        "roomWrite":  0x00410028,
        "stageWrite":  0x0003
    },
    "13": {
        "comment":  "Icebrand room",
        "stage":  0x03,                                                                 # Catacombs
        "room":  9,
        "xPos":  56,
        "yPos":  164,
        "xyWrite":  0x00a40038,
        "roomWrite":  0x00410048,
        "stageWrite":  0x0003
    },
    "14": {
        "comment":  "Elevator in Slime room",
        "stage":  0x03,                                                                 # Catacombs
        "room":  23,
        "xPos":  352,
        "yPos":  228,
        "xyWrite":  0x00E40160,
        "roomWrite":  0x004100B8,
        "stageWrite":  0x0003
    },
    "15": {
        "comment":  "Top left of Spectral Sword room",
        "stage":  0x04,                                                                 # Olrox's Quarters
        "room":  2,
        "xPos":  48,
        "yPos":  132,
        "xyWrite":  0x00840030,
        "roomWrite":  0x00410010,
        "stageWrite":  0x0004
    },
    "16": {
        "comment":  "Vase shaft",
        "stage":  0x04,                                                                 # Olrox's Quarters
        "room":  6,
        "xPos":  118,
        "yPos":  388,
        "xyWrite":  0x01840076,
        "roomWrite":  0x00410030,
        "stageWrite":  0x0004
    },
    "17": {
        "comment":  "Olrox Garnet room",
        "stage":  0x04,                                                                 # Olrox's Quarters
        "room":  10,
        "xPos":  128,
        "yPos":  164,
        "xyWrite":  0x00A40080,
        "roomWrite":  0x00410050,
        "stageWrite":  0x0004
    },
    "18": {
        "comment":  "Item cubby in boss hallway",
        "stage":  0x04,                                                                 # Olrox's Quarters
        "room":  11,
        "xPos":  468,
        "yPos":  208,
        "xyWrite":  0x00d001d4,
        "roomWrite":  0x00410058,
        "stageWrite":  0x0004
    },
    "19": {
        "comment":  "Room before Cerberus",
        "stage":  0x05,                                                                 # Abandoned Mine
        "room":  1,
        "xPos":  254,
        "yPos":  148,
        "xyWrite":  0x009400FE,
        "roomWrite":  0x00410008,
        "stageWrite":  0x0005
    },
    "20": {
        "comment":  "Combat Knife room",
        "stage":  0x05,                                                                 # Abandoned Mine
        "room":  9,
        "xPos":  208,
        "yPos":  148,
        "xyWrite":  0x009400D0,
        "roomWrite":  0x00410048,
        "stageWrite":  0x0005
    },
    "21": {
        "comment":  "Spike hallway",
        "stage":  0x06,                                                                 # Royal Chapel
        "room":  1,
        "xPos":  1064,
        "yPos":  132,
        "xyWrite":  0x00840428,
        "roomWrite":  0x00410008,
        "stageWrite":  0x0006
    },
    "22": {
        "comment":  "Confessional",
        "stage":  0x06,                                                                 # Royal Chapel
        "room":  7,
        "xPos":  96,
        "yPos":  164,
        "xyWrite":  0x00a40060,
        "roomWrite":  0x00410038,
        "stageWrite":  0x0006
    },
    "23": {
        "comment":  "Goggles location",
        "stage":  0x06,                                                                 # Royal Chapel
        "room":  8,
        "xPos":  196,
        "yPos":  276,
        "xyWrite":  0x011400c4,
        "roomWrite":  0x00410040,
        "stageWrite":  0x0006
    },
    "24": {
        "comment":  "Bottom of the Stairs",
        "stage":  0x06,                                                                 # Royal Chapel
        "room":  11,
        "xPos":  208,
        "yPos":  1700,
        "xyWrite":  0x06A400D0,
        "roomWrite":  0x00410058,
        "stageWrite":  0x0006
    },
    "25": {
        "comment":  "Top of the tower closest to Keep",
        "stage":  0x06,                                                                 # Royal Chapel
        "room":  17,
        "xPos":  510,
        "yPos":  228,
        "xyWrite":  0x00E401FE,
        "roomWrite":  0x00410088,
        "stageWrite":  0x0006
    },
    "26": {
        "comment":  "Power of Wolf",
        "stage":  0x07,                                                                 # Castle Entrance
        "room":  0,
        "xPos":  220,
        "yPos":  132,
        "xyWrite":  0x008400dc,
        "roomWrite":  0x00410000,
        "stageWrite":  0x0007
    },
    "27": {
        "comment":  "Holy Mail ledge",
        "stage":  0x07,                                                                 # Castle Entrance
        "room":  3,
        "xPos":  110,
        "yPos":  72,
        "xyWrite":  0x0048006E,
        "roomWrite":  0x00410018,
        "stageWrite":  0x0007
    },
    "28": {
        "comment":  "On the Teleporter shortcut switch",
        "stage":  0x07,                                                                 # Castle Entrance
        "room":  16,
        "xPos":  104,
        "yPos":  160,
        "xyWrite":  0x00A00068,
        "roomWrite":  0x00410080,
        "stageWrite":  0x0007
    },
    "29": {
        "comment":  "Drawer room",
        "stage":  0x09,                                                                 # Underground Caverns
        "room":  4,
        "xPos":  224,
        "yPos":  148,
        "xyWrite":  0x009400E0,
        "roomWrite":  0x00410020,
        "stageWrite":  0x0009
    },
    "30": {
        "comment":  "Top of Succubus stairs",
        "stage":  0x09,                                                                 # Underground Caverns
        "room":  6,
        "xPos":  172,
        "yPos":  132,
        "xyWrite":  0x008400ac,
        "roomWrite":  0x00410030,
        "stageWrite":  0x0009
    },
    "31": {
        "comment":  "Bottom of waterfall",
        "stage":  0x09,                                                                 # Underground Caverns
        "room":  26,
        "xPos":  316,
        "yPos":  1412,
        "xyWrite":  0x0584013c,
        "roomWrite":  0x004100d0,
        "stageWrite":  0x0009
    },
    "32": {
        "comment":  "Merman Statue room",
        "stage":  0x09,                                                                 # Underground Caverns
        "room":  21,
        "xPos":  208,
        "yPos":  132,
        "xyWrite":  0x008400D0,
        "roomWrite":  0x004100A8,
        "stageWrite":  0x0009
    },
    "33": {
        "comment":  "Opening shortcut",
        "stage":  0x0a,                                                                 # Colosseum
        "room":  4,
        "xPos":  168,
        "yPos":  156,
        "xyWrite":  0x009c00a8,
        "roomWrite":  0x00410020,
        "stageWrite":  0x000a
    },
    "34": {
        "comment":  "Open elevator",
        "stage":  0x0a,                                                                 # Colosseum
        "room":  6,
        "xPos":  72,
        "yPos":  128,
        "xyWrite":  0x00800048,
        "roomWrite":  0x00410030,
        "stageWrite":  0x000a
    },
    "35": {
        "comment":  "Blood cloak room",
        "stage":  0x0a,                                                                 # Colosseum
        "room":  10,
        "xPos":  54,
        "yPos":  164,
        "xyWrite":  0x00A40036,
        "roomWrite":  0x00410050,
        "stageWrite":  0x000A
    },
    "36": {
        "comment":  "Attic",
        "stage":  0x0b,                                                                 # Castle Keep
        "room":  0,
        "xPos":  64,
        "yPos":  164,
        "xyWrite":  0x00a40040,
        "roomWrite":  0x00410000,
        "stageWrite":  0x000b
    },
    "37": {
        "comment":  "Falchion room",
        "stage":  0x0b,                                                                 # Castle Keep
        "room":  5,
        "xPos":  100,
        "yPos":  164,
        "xyWrite":  0x00A40064,
        "roomWrite":  0x00410028,
        "stageWrite":  0x000B
    },
    "38": {
        "comment":  "Tyrfing room",
        "stage":  0x0b,                                                                 # Castle Keep
        "room":  8,
        "xPos":  156,
        "yPos":  164,
        "xyWrite":  0x00A4009C,
        "roomWrite":  0x00410040,
        "stageWrite":  0x000B
    },
    "39": {
        "comment":  "Cloth cape room",
        "stage":  0x0c,                                                                 # Alchemy Laboratory
        "room":  5,
        "xPos":  128,
        "yPos":  164,
        "xyWrite":  0x00A40080,
        "roomWrite":  0x00410028,
        "stageWrite":  0x000C
    },
    "40": {
        "comment":  "Sunglasses room",
        "stage":  0x0c,                                                                 # Alchemy Laboratory
        "room":  6,
        "xPos":  128,
        "yPos":  164,
        "xyWrite":  0x00a40080,
        "roomWrite":  0x00410030,
        "stageWrite":  0x000c
    },
    "41": {
        "comment":  "Skill of Wolf room",
        "stage":  0x0c,                                                                 # Alchemy Laboratory
        "room":  8,
        "xPos":  208,
        "yPos":  132,
        "xyWrite":  0x008400D0,
        "roomWrite":  0x00410040,
        "stageWrite":  0x000C
    },
    "42": {
        "comment":  "Middle of the maze room with pendulums",
        "stage":  0x0d,                                                                 # Clock Tower
        "room":  3,
        "xPos":  1090,
        "yPos":  84,
        "xyWrite":  0x00540442,
        "roomWrite":  0x00410018,
        "stageWrite":  0x000D
    },
    "43": {
        "comment":  "Fire of Bat ledge in large room",
        "stage":  0x0d,                                                                 # Clock Tower
        "room":  10,
        "xPos":  1456,
        "yPos":  132,
        "xyWrite":  0x008405B0,
        "roomWrite":  0x00410050,
        "stageWrite":  0x000D
    },
    "44": {
        "comment":  "Ledge with a column (left side of large room)",
        "stage":  0x0d,                                                                 # Clock Tower
        "room":  10,
        "xPos":  216,
        "yPos":  308,
        "xyWrite":  0x013400d8,
        "roomWrite":  0x00410050,
        "stageWrite":  0x000d
    },
    "45": {  # IMPORTANT CASTLE 2 NOTES: stage number must be correct, but stageWrite should mask off bit 0x20.
        "comment":  "Black Marble Gallery (Reverse Forbidden)",
        "stage":  0x20,
        "room":  0,
        "xPos":  144,
        "yPos":  540,
        "xyWrite":  0x021c0090,
        "roomWrite":  0x00410000,
        "stageWrite":  0x0000  # Castle 2 Stage Numbers should mask off the 0x20 bit.
    },
    "46": {
        "comment":  "Black Marble Gallery (Reverse Alucart)",
        "stage":  0x20,
        "room":  14,
        "xPos":  232,
        "yPos":  128,
        "xyWrite":  0x008000e8,
        "roomWrite":  0x00410070,
        "stageWrite":  0x0000
    },
    "47": {
        "comment":  "Black Marble Gallery (Reverse Library Card)",
        "stage":  0x20,
        "room":  24,
        "xPos":  80,
        "yPos":  128,
        "xyWrite":  0x00800050,
        "roomWrite":  0x004100c0,
        "stageWrite":  0x0000
    },
    "48": {
        "comment":  "Reverse Outer Wall (Save Room)",
        "stage":  0x21,
        "room":  1,
        "xPos":  232,
        "yPos":  128,
        "xyWrite":  0x008000e8,
        "roomWrite":  0x00410008,
        "stageWrite":  0x0001
    },
    "49": {
        "comment":  "Reverse Outer Wall (Telescope)",
        "stage":  0x21,
        "room":  3,
        "xPos":  537,
        "yPos":  128,
        "xyWrite":  0x00800219,
        "roomWrite":  0x00410018,
        "stageWrite":  0x0001
    },
    "50": {
        "comment":  "Forbidden Library (Book Case)",
        "stage":  0x22,
        "room":  1,
        "xPos":  32,
        "yPos":  128,
        "xyWrite":  0x00800020,
        "roomWrite":  0x00410008,
        "stageWrite":  0x0002
    },
    "51": {
        "comment":  "Forbidden Library (Shop)",
        "stage":  0x22,
        "room":  5,
        "xPos":  32,
        "yPos":  128,
        "xyWrite":  0x00800020,
        "roomWrite":  0x00410028,
        "stageWrite":  0x0002
    },
    "52": {
        "comment":  "Floating Catacombs (Galamoth)",
        "stage":  0x23,
        "room":  1,
        "xPos":  24,
        "yPos":  128,
        "xyWrite":  0x00800018,
        "roomWrite":  0x00410008,
        "stageWrite":  0x0003
    },
    "53": {
        "comment":  "Floating Catacombs (Save Room)",
        "stage":  0x23,
        "room":  13,
        "xPos":  246,
        "yPos":  128,
        "xyWrite":  0x008000f6,
        "roomWrite":  0x00410068,
        "stageWrite":  0x0003
    },
    "54": {
        "comment":  "Deathwing's Lair (Entrance)",
        "stage":  0x24,
        "room":  1,
        "xPos":  128,
        "yPos":  128,
        "xyWrite":  0x00800080,
        "roomWrite":  0x00410008,
        "stageWrite":  0x0004
    },
    "55": {
        "comment":  "Deathwing's Lair (Alucard Mail)",
        "stage":  0x24,
        "room":  10,
        "xPos":  32,
        "yPos":  128,
        "xyWrite":  0x00800020,
        "roomWrite":  0x00410050,
        "stageWrite":  0x0004
    },
    "56": {
        "comment":  "Deathwing's Lair (Heart Refresh)",
        "stage":  0x24,
        "room":  14,
        "xPos":  256,
        "yPos":  128,
        "xyWrite":  0x00800100,
        "roomWrite":  0x00410070,
        "stageWrite":  0x0004
    },
    "57": {
        "comment":  "Cave (Alucard Sword)",
        "stage":  0x25,
        "room":  11,
        "xPos":  56,
        "yPos":  128,
        "xyWrite":  0x00800038,
        "roomWrite":  0x00410058,
        "stageWrite":  0x0005
    },
    "58comment": {
        "stage":  0x26,
        "room":  7,
        "xPos":  204,
        "yPos":  128,
        "xyWrite":  0x008000cc,
        "roomWrite":  0x00410038,
        "stageWrite":  0x0006
    },
    "59": {
        "comment":  "Reverse Entrance (Gate)",
        "stage":  0x27,
        "room":  0,
        "xPos":  125,
        "yPos":  512,
        "xyWrite":  0x0100007d,
        "roomWrite":  0x00410000,
        "stageWrite":  0x0007
    },
    "60": {
        "comment":  "Reverse Entrance (Caverns Shortcut)",
        "stage":  0x27,
        "room":  10,
        "xPos":  32,
        "yPos":  128,
        "xyWrite":  0x00800020,
        "roomWrite":  0x00410050,
        "stageWrite":  0x0007
    },
    "61": {
        "comment":  "Reverse Entrance (Talisman)",
        "stage":  0x27,
        "room":  17,
        "xPos":  32,
        "yPos":  128,
        "xyWrite":  0x00800020,
        "roomWrite":  0x00410088,
        "stageWrite":  0x0007
    },
    "62": {
        "comment":  "Reverce Caverns (Peanuts)",
        "stage":  0x29,
        "room":  37,
        "xPos":  18,
        "yPos":  128,
        "xyWrite":  0x00800012,
        "roomWrite":  0x00410128,
        "stageWrite":  0x0009
    },
    "63": {
        "comment":  "Reverce Caverns (Imp Room)",
        "stage":  0x29,
        "room":  4,
        "xPos":  224,
        "yPos":  128,
        "xyWrite":  0x008000e0,
        "roomWrite":  0x00410020,
        "stageWrite":  0x0009
    },
    "64": {
        "comment":  "Reverce Caverns (Garnet)",
        "stage":  0x29,
        "room":  17,
        "xPos":  228,
        "yPos":  128,
        "xyWrite":  0x008000e4,
        "roomWrite":  0x00410088,
        "stageWrite":  0x0009
    },
    "65": {
        "comment":  "Reverse Colosseum (Gram)",
        "stage":  0x2a,
        "room":  10,
        "xPos":  228,
        "yPos":  128,
        "xyWrite":  0x008000e4,
        "roomWrite":  0x00410050,
        "stageWrite":  0x000a
    },
    "66": {
        "comment":  "Reverse Colosseum (Zircon)",
        "stage":  0x2a,
        "room":  12,
        "xPos":  488,
        "yPos":  128,
        "xyWrite":  0x008001e8,
        "roomWrite":  0x00410060,
        "stageWrite":  0x000a
    },
    "67": {
        "comment":  "Reverse Keep (High Potion)",
        "stage":  0x2b,
        "room":  3,
        "xPos":  32,
        "yPos":  256,
        "xyWrite":  0x01000020,
        "roomWrite":  0x00410018,
        "stageWrite":  0x000b
    },
    "68": {
        "comment":  "Reverse Keep (Lightning Mail)",
        "stage":  0x2b,
        "room":  8,
        "xPos":  16,
        "yPos":  128,
        "xyWrite":  0x00800010,
        "roomWrite":  0x00410040,
        "stageWrite":  0x000b
    },
    "69": {
        "comment":  "Necromancy Laboratory (Reverse Skill of Wolf)",
        "stage":  0x2c,
        "room":  8,
        "xPos":  16,
        "yPos":  128,
        "xyWrite":  0x00800010,
        "roomWrite":  0x00410040,
        "stageWrite":  0x000c
    },
    "70": {
        "comment":  "Necromancy Laboratory (Goddess Shield)",
        "stage":  0x2c,
        "room":  6,
        "xPos":  248,
        "yPos":  128,
        "xyWrite":  0x008000f8,
        "roomWrite":  0x00410030,
        "stageWrite":  0x000c
    },
    "71": {
        "comment":  "Necromancy Laboratory (Jewel Door Hall)",
        "stage":  0x2c,
        "room":  2,
        "xPos":  504,
        "yPos":  128,
        "xyWrite":  0x008001f8,
        "roomWrite":  0x00410010,
        "stageWrite":  0x000c
    },
    "72": {
        "comment":  "Reverse Clock Tower (Dragon Helm)",
        "stage":  0x2d,
        "room":  12,
        "xPos":  32,
        "yPos":  128,
        "xyWrite":  0x00800020,
        "roomWrite":  0x00410060,
        "stageWrite":  0x000d
    },
    "73": {
        "comment":  "Reverse Clock Tower (Maze Room)",
        "stage":  0x2d,
        "room":  3,
        "xPos":  1728,
        "yPos":  128,
        "xyWrite":  0x008006c0,
        "roomWrite":  0x00410018,
        "stageWrite":  0x000d
    }
}

music = {
    "LOST_PAINTING": 0x01,  # Lost Painting
    "CURSE_ZONE": 0x03,  # Curse Zone
    "REQUIEM_FOR_THE_GODS": 0x05,  # Requiem for the Gods
    "RAINBOW_CEMETARY": 0x07,  # Rainbow Cemetary
    "WOOD_CARVING_PARTITA": 0x09,  # Wood Carving Partita
    "CRYSTAL_TEARDROPS": 0x0b,  # Crystal Teardrops
    "MARBLE_GALLERY": 0x0d,  # Marble Gallery
    "DRACULAS_CASTLE": 0x0f,  # Dracula's Castle
    "THE_TRAGIC_PRINCE": 0x11,  # The Tragic Prince
    "TOWER_OF_MIST": 0x13,  # Tower of Mist
    "DOOR_OF_HOLY_SPIRITS": 0x15,  # Door of Holy Spirits
    "DANCE_OF_PALES": 0x17,  # Dance of Pales
    "ABANDONED_PIT": 0x19,  # Abandoned Pit
    "HEAVENLY_DOORWAY": 0x1b,  # Heavenly Doorway
    "FESTIVAL_OF_SERVANTS": 0x1d,  # Festival of Servants
    "WANDERING_GHOSTS": 0x23,  # Wandering Ghosts
    "THE_DOOR_TO_THE_ABYSS": 0x25,  # The Door to the Abyss
    "DANCE_OF_GOLD": 0x2e,  # Dance of Gold
    "ENCHANTED_BANQUET": 0x30,  # Enchanted Banquet
    "DEATH_BALLAD": 0x34,  # Death Ballad
    "FINAL_TOCCATA": 0x38,  # Final Tocatta
    "NOCTURNE": 0x3f  # Nocturne
}

music_by_area = {
    "ARE": [0x00b0188, 0x6126570],
    "CAT": [0x00b0054, 0x609505c],
    "CEN": [0x00b0130],
    "CHI": [0x00b00ac, 0x66cc898],
    "DAI": [0x00b00d8],
    "DRE": [0x5b074f4],
    "LIB": [0x00b0028, 0x00b036c, 0x47e5ec4, 0x47e6060],
    "LIB_BOSS": [0x47e5e08],
    "NO0": [0x00affd0],
    "NO1": [0x00afffc],
    "NO2": [0x00b0080, 0x5fea9dc],
    "NO3": [0x00b0104, 0x00b0c2c, 0x4ba6cb0, 0x4bb0064],
    "NO4": [0x00b015c, 0x61d1fa8, 0x61d1fec, 0x61d2188],
    "NZ0": [0x00b01e0, 0x54ecb58, 0x54ecbd4],
    "NZ0_BOSS": [0x54eca88],
    "NZ1": [0x00b020c, 0x55a2f90, 0x55a3008],
    "NZ1_BOSS": [0x55a2ed0],
    "TOP": [0x00b01b4],
    "RARE": [0x00b0838, 0x6487b44, 0x6487bec],
    "RCAT": [0x00b0704, 0x6a7c4f0, 0x6a7c58c],
    "RCEN": [0x00b07e0],
    "RCEN_BOSS": [0x56dc624],
    "RCHI": [0x00b075c, 0x6644d10],
    "RDAI": [0x00b0788, 0x6757ad8, 0x6757b74],
    "RLIB": [0x00b06d8],
    "RNO0": [0x00b0680],
    "RNO1": [0x00b06ac, 0x67ec31c, 0x67ec3b8],
    "RNO2": [0x00b0730],
    "RNO3": [0x00b07b4],
    "RNO4": [0x00b080c],
    "RNZ0": [0x00b0890, 0x65a8960, 0x65a89f0],
    "RNZ1": [0x00b08bc, 0x59ee534, 0x59ee5ac],
    "RNZ1_BOSS": [0x59ee490],
    "RTOP": [0x00b0864],
    "BO0": [0x5fddd24, 0x5fddd80, 0x5fddda0, 0x5fdde14],
    "BO1": [0x6094500, 0x6094534],
    "BO2": [0x6129480],
    "BO3": [0x61d20f4],
    "BO5": [0x632e8c8],
    "RBO1": [0x65a88e8, 0x65a8908],
    "RBO2": [0x6644bc4],
    "RBO3": [0x6757a78],
    "RBO4": [0x67ec2bc],
    "RBO5": [0x689e4f0],
    "RBO7": [0x69e8318],
    "RBO8": [0x6a7c490],
}

faerie_scroll_force_addresses = [
    0x04403938,
    0x044d4948,
    0x045702c0,
    0x0460bcb8,
    0x046c70ec,
    0x047eadd4,
    0x04947e2c,
    0x04a1da54,
    0x04ae1d98,
    0x04bb25e0,
    0x04c86ae4,
    0x04d367a4,
    0x04dc4068,
    0x04e6e350,
    0x04f0ab84,
    0x04fc4c08,
    0x050800a0,
    0x051373c4,
    0x051e8da4,
    0x052c0628,
    0x0537889c,
    0x05436b40,
    0x054f34d8,
    0x055a6164,
    0x05643614,
    0x056e3670,
    0x0577dcb4,
    0x05807b68,
    0x0588d50c,
    0x05936448,
    0x059ef674,
    0x05a7a89c,
    0x05b0d6c4,
    0x05fef940,
    0x06099584,
    0x0612aac4,
    0x061d2f48,
    0x06286480,
    0x06332188,
    0x063dae48,
    0x0648f038,
    0x06518314,
    0x065a9958,
    0x06648254,
    0x066cdacc,
    0x06758d7c,
    0x067ed580,
    0x0689f884,
    0x06956f20,
    0x069eb4c8,
    0x06a7da5c,
    ]

RELIC_NAMES = ["Soul of bat", "Fire of bat", "Echo of bat", "Force of echo", "Soul of wolf", "Power of wolf",
               "Skill of wolf", "Form of mist", "Power of mist", "Gas cloud", "Cube of zoe", "Spirit orb",
               "Gravity boots", "Leap stone", "Holy symbol", "Faerie scroll", "Jewel of open", "Merman statue",
               "Bat card", "Ghost card", "Faerie card", "Demon card", "Sword card", "Heart of vlad", "Tooth of vlad",
               "Rib of vlad", "Ring of vlad", "Eye of vlad"]
SLOT = {"RIGHT_HAND": 'r',
        "LEFT_HAND": 'l',
        "HEAD": 'h',
        "BODY": 'b',
        "CLOAK": 'c',
        "OTHER": 'o',
        "OTHER2": 'o2',
        "AXEARMOR": 'a',
        "LUCK_MODE": 'x'}
slots = {'r':  0x097c00,
         'l':  0x097c04,
         'h':  0x097c08,
         'b':  0x097c0c,
         'c':  0x097c10,
         'o':  0x097c14,
         'o2': 0x097c18}
EXTENSIONS = {
    # RELICS+PROG
    0: RELIC_NAMES + ['CAT_Spike breaker_16', 'CEN_Holy glasses_72803176', 'NO4_Gold ring_10', 'DAI_Silver ring_2',
                      'RARE_Life Vessel_8'],
    # GUARDED
    1: RELIC_NAMES + ['CAT_Spike breaker_16', 'CEN_Holy glasses_72803176', 'NO4_Gold ring_10', 'DAI_Silver ring_2',
                      'NO4_Crystal cloak_2', 'CAT_Mormegil_3', 'RNO4_Dark blade_23', 'RNZ0_Ring of arcana_8',
                      'RARE_Life Vessel_8'],
    # EQUIPMENT
    2: RELIC_NAMES + ['CAT_Spike breaker_16', 'CEN_Holy glasses_72803176', 'NO4_Gold ring_10', 'DAI_Silver ring_2',
                      'NO4_Crystal cloak_2', 'CAT_Mormegil_3', 'RNO4_Dark blade_23', 'RNZ0_Ring of arcana_8',
                      'RARE_Life Vessel_8', 'NP3_Jewel sword_9', 'NZ0_Basilard_9', 'NZ0_Sunglasses_6',
                      'NZ0_Cloth cape_2', 'DAI_Mystic pendant_4', 'DAI_Ankh of life_0', 'DAI_Morningstar_1',
                      'DAI_Goggles_9', 'DAI_Silver plate_10', 'DAI_Cutlass_14', 'TOP_Platinum mail_11',
                      'TOP_Falchion_12', 'NZ1_Gold plate_4', 'NZ1_Bekatowa_7', 'NO1_Gladius_4', 'NO1_Jewel knuckles_0',
                      'LIB_Holy rod_2', 'LIB_Onyx_6', 'LIB_Bronze cuirass_4', 'NO0_Alucart sword_7', 'NO2_Broadsword_4',
                      'NO2_Estoc_10', 'NO2_Garnet_12', 'ARE_Blood cloak_3', 'ARE_Shield rod_1', 'ARE_Knight shield_4',
                      'NO4_Bandanna_11', 'NO4_Nunchaku_36', 'NO4_Knuckle duster_23', 'NO4_Onyx_22',
                      'NO4_Secret boots_31', 'CHI_Combat knife_5', 'CHI_Ring of ares_4', 'CAT_Bloodstone_8',
                      'CAT_Icebrand_1', 'CAT_Walk armor_2', 'RNO3_Beryl circlet_6', 'RNO3_Talisman_9', 'RNZ0_Katana_5',
                      'RNZ0_Goddess shield_3', 'RDAI_Twilight cloak_16', 'RDAI_Talwar_13', 'RTOP_Garnet_22',
                      'RTOP_Bastard sword_4', 'RTOP_Royal cloak_11', 'RTOP_Lightning mail_23', 'RNZ1_Moon rod_11',
                      'RNZ1_Sunstone_8', 'RNZ1_Luminus_3', 'RNZ1_Dragon helm_5', 'RNO1_Hammer_2', 'RLIB_Staurolite_8',
                      'RLIB_Badelaire_7', 'RNO4_Diamond_13', 'RNO4_Opal_11', 'RNO4_Garnet_4', 'RNO4_Osafune katana_26',
                      'RNO4_Alucard shield_0', 'RCHI_Alucard sword_2', 'RCAT_Necklace of j_13', 'RCAT_Diamond_14',
                      'RNO2_Opal_0', 'RNO2_Alucard mail_7', 'RARE_Gram_3', 'RARE_Fury plate_0'],
    # FULL
    3: ['ARE_Heart Vessel_0', 'ARE_Shield rod_1', 'ARE_Blood cloak_3', 'ARE_Knight shield_4', 'ARE_Library card_5',
        'ARE_Green tea_6', 'ARE_Holy sword_7', 'Form of mist', 'CAT_Cat-eye circl._0', 'CAT_Icebrand_1',
        'CAT_Walk armor_2', 'CAT_Mormegil_3', 'CAT_Library card_4', 'CAT_Heart Vessel_6', 'CAT_Ballroom mask_7',
        'CAT_Bloodstone_8', 'CAT_Life Vessel_9', 'CAT_Heart Vessel_10', 'CAT_Cross shuriken_11',
        'CAT_Cross shuriken_12', 'CAT_Karma coin_13', 'CAT_Karma coin_14', 'CAT_Pork bun_15',
        'CAT_Spike breaker_16', 'CAT_Monster vial 3_17', 'CAT_Monster vial 3_18', 'CAT_Monster vial 3_19',
        'CAT_Monster vial 3_20', 'CHI_Power of sire_0', 'CHI_Karma coin_1', 'CHI_Ring of ares_4',
        'CHI_Combat knife_5', 'CHI_Shiitake_6', 'CHI_Shiitake_7', 'CHI_Barley tea_8', 'CHI_Peanuts_9',
        'CHI_Peanuts_10', 'CHI_Peanuts_11', 'CHI_Peanuts_12', 'CHI_Turkey_73307650', 'Demon card',
        'DAI_Ankh of life_0', 'DAI_Morningstar_1', 'DAI_Silver ring_2', 'DAI_Aquamarine_3', 'DAI_Mystic pendant_4',
        'DAI_Magic missile_5', 'DAI_Shuriken_6', 'DAI_TNT_7', 'DAI_Boomerang_8', 'DAI_Goggles_9',
        'DAI_Silver plate_10', 'DAI_Str. potion_11', 'DAI_Life Vessel_12', 'DAI_Zircon_13', 'DAI_Cutlass_14',
        'DAI_Potion_15', 'LIB_Stone mask_1', 'LIB_Holy rod_2', 'LIB_Bronze cuirass_4', 'LIB_Takemitsu_5',
        'LIB_Onyx_6', 'LIB_Frankfurter_7', 'LIB_Potion_8', 'LIB_Antivenom_9', 'LIB_Topaz circlet_10',
        'Soul of bat', 'Faerie scroll', 'Faerie card', 'Jewel of open', 'NO0_Life Vessel_0',
        'NO0_Alucart shield_1', 'NO0_Heart Vessel_2', 'NO0_Life apple_3', 'NO0_Hammer_4', 'NO0_Potion_5',
        'NO0_Alucart mail_6', 'NO0_Alucart sword_7', 'NO0_Life Vessel_8', 'NO0_Heart Vessel_9',
        'NO0_Library card_10', 'NO0_Attack potion_11', 'NO0_Hammer_12', 'NO0_Str. potion_13',
        'CEN_Holy glasses_72803176', 'Spirit orb', 'Gravity boots', 'NO1_Jewel knuckles_0', 'NO1_Mirror cuirass_1',
        'NO1_Heart Vessel_2', 'NO1_Garnet_3', 'NO1_Gladius_4', 'NO1_Life Vessel_5', 'NO1_Zircon_6',
        'NO1_Pot roast_77699032', 'Soul of wolf', 'NO2_Heart Vessel_1', 'NO2_Broadsword_4', 'NO2_Onyx_5',
        'NO2_Cheese_6', 'NO2_Manna prism_7', 'NO2_Resist fire_8', 'NO2_Luck potion_9', 'NO2_Estoc_10',
        'NO2_Iron ball_11', 'NO2_Garnet_12', 'Echo of bat', 'Sword card', 'NO3_Heart Vessel_0',
        'NO3_Life Vessel_1', 'NO3_Life apple_2', 'NO3_Shield potion_4', 'NO3_Holy mail_5', 'NO3_Life Vessel_6',
        'NO3_Heart Vessel_7', 'NO3_Life Vessel_8', 'NP3_Jewel sword_9', 'NO3_Pot roast_79337332',
        'NO3_Turkey_79340208', 'Cube of zoe', 'Power of wolf', 'NO4_Heart Vessel_0', 'NO4_Life Vessel_1',
        'NO4_Crystal cloak_2', 'NO4_Antivenom_4', 'NO4_Life Vessel_5', 'NO4_Life Vessel_6', 'NO4_Herald shield_7',
        'NO4_Zircon_9', 'NO4_Gold ring_10', 'NO4_Bandanna_11', 'NO4_Shiitake_12', 'NO4_Claymore_13',
        'NO4_Meal ticket_14', 'NO4_Meal ticket_15', 'NO4_Meal ticket_16', 'NO4_Meal ticket_17', 'NO4_Moonstone_18',
        'NO4_Scimitar_19', 'NO4_Resist ice_20', 'NO4_Pot roast_21', 'NO4_Onyx_22', 'NO4_Knuckle duster_23',
        'NO4_Life Vessel_24', 'NO4_Elixir_25', 'NO4_Toadstool_26', 'NO4_Shiitake_27', 'NO4_Life Vessel_28',
        'NO4_Heart Vessel_29', 'NO4_Pentagram_30', 'NO4_Secret boots_31', 'NO4_Shiitake_32', 'NO4_Toadstool_33',
        'NO4_Shiitake_35', 'NO4_Nunchaku_36', 'Holy symbol', 'Merman statue', 'NZ0_Hide cuirass_0',
        'NZ0_Heart Vessel_1', 'NZ0_Cloth cape_2', 'NZ0_Life Vessel_3', 'NZ0_Sunglasses_6', 'NZ0_Resist thunder_7',
        'NZ0_Leather shield_8', 'NZ0_Basilard_9', 'NZ0_Potion_10', 'Skill of wolf', 'Bat card',
        'NZ1_Magic missile_0', 'NZ1_Pentagram_1', 'NZ1_Star flail_3', 'NZ1_Gold plate_4', 'NZ1_Steel helm_5',
        'NZ1_Healing mail_6', 'NZ1_Bekatowa_7', 'NZ1_Shaman shield_8', 'NZ1_Ice mail_9', 'NZ1_Life Vessel_10',
        'NZ1_Heart Vessel_11', 'NZ1_Bwaka knife_89601956', 'NZ1_Pot roast_89601948', 'NZ1_Shuriken_89601952',
        'NZ1_TNT_89601960', 'Fire of bat', 'TOP_Turquoise_0', 'TOP_Turkey_1', 'TOP_Fire mail_2', 'TOP_Tyrfing_3',
        'TOP_Sirloin_4', 'TOP_Turkey_5', 'TOP_Pot roast_6', 'TOP_Frankfurter_7', 'TOP_Resist stone_8',
        'TOP_Resist dark_9', 'TOP_Resist holy_10', 'TOP_Platinum mail_11', 'TOP_Falchion_12', 'TOP_Life Vessel_13',
        'TOP_Life Vessel_14', 'TOP_Heart Vessel_15', 'TOP_Heart Vessel_16', 'TOP_Heart Vessel_18', 'Leap stone',
        'Power of mist', 'Ghost card', 'RARE_Fury plate_0', 'RARE_Zircon_1', 'RARE_Buffalo star_2', 'RARE_Gram_3',
        'RARE_Aquamarine_4', 'RARE_Heart Vessel_5', 'RARE_Life Vessel_6', 'RARE_Heart Vessel_7',
        'RCAT_Magic missile_0', 'RCAT_Buffalo star_1', 'RCAT_Resist thunder_2', 'RCAT_Resist fire_3',
        'RCAT_Karma coin_4', 'RCAT_Karma coin_5', 'RCAT_Red bean bun_6', 'RCAT_Elixir_7', 'RCAT_Library card_8',
        'RCAT_Life Vessel_9', 'RCAT_Heart Vessel_10', 'RCAT_Shield potion_11', 'RCAT_Attack potion_12',
        'RCAT_Necklace of j_13', 'RCAT_Diamond_14', 'RCAT_Heart Vessel_15', 'RCAT_Life Vessel_16',
        'RCAT_Ruby circlet_17', 'Gas cloud', 'RCHI_Power of sire_0', 'RCHI_Life apple_1', 'RCHI_Alucard sword_2',
        'RCHI_Green tea_3', 'RCHI_Power of sire_4', 'RCHI_Shiitake_6', 'RCHI_Shiitake_7', 'Eye of vlad',
        'RDAI_Fire boomerang_2', 'RDAI_Diamond_3', 'RDAI_Zircon_4', 'RDAI_Heart Vessel_5', 'RDAI_Shuriken_6',
        'RDAI_TNT_7', 'RDAI_Boomerang_8', 'RDAI_Javelin_9', 'RDAI_Manna prism_10', 'RDAI_Smart potion_11',
        'RDAI_Life Vessel_12', 'RDAI_Talwar_13', 'RDAI_Bwaka knife_14', 'RDAI_Magic missile_15',
        'RDAI_Twilight cloak_16', 'RDAI_Heart Vessel_17', 'Heart of vlad', 'RLIB_Turquoise_0', 'RLIB_Opal_1',
        'RLIB_Library card_2', 'RLIB_Resist fire_3', 'RLIB_Resist ice_4', 'RLIB_Resist stone_5',
        'RLIB_Neutron bomb_6', 'RLIB_Badelaire_7', 'RLIB_Staurolite_8', 'RNO0_Library card_0', 'RNO0_Potion_1',
        'RNO0_Antivenom_2', 'RNO0_Life Vessel_3', 'RNO0_Heart Vessel_4', 'RNO0_Resist dark_5',
        'RNO0_Resist holy_6', 'RNO0_Resist thunder_7', 'RNO0_Resist fire_8', 'RNO0_Meal ticket_9',
        'RNO0_Iron ball_10', 'RNO0_Heart refresh_11', 'RNO1_Heart Vessel_0', 'RNO1_Shotel_1', 'RNO1_Hammer_2',
        'RNO1_Life Vessel_3', 'RNO1_Luck potion_4', 'RNO1_Shield potion_5', 'RNO1_High potion_6', 'RNO1_Garnet_7',
        'RNO1_Dim sum set_84398220', 'Tooth of vlad', 'RNO2_Opal_0', 'RNO2_Sword of hador_1', 'RNO2_High potion_2',
        'RNO2_Shield potion_3', 'RNO2_Luck potion_4', 'RNO2_Manna prism_5', 'RNO2_Aquamarine_6',
        'RNO2_Alucard mail_7', 'RNO2_Life Vessel_8', 'RNO2_Heart refresh_9', 'RNO2_Shuriken_10',
        'RNO2_Heart Vessel_11', 'Rib of vlad', 'RNO3_Hammer_0', 'RNO3_Antivenom_1', 'RNO3_High potion_2',
        'RNO3_Heart Vessel_3', 'RNO3_Zircon_4', 'RNO3_Opal_5', 'RNO3_Beryl circlet_6', 'RNO3_Fire boomerang_7',
        'RNO3_Life Vessel_8', 'RNO3_Talisman_9', 'RNO3_Pot roast_85880396', 'RNO4_Alucard shield_0',
        'RNO4_Shiitake_1', 'RNO4_Toadstool_2', 'RNO4_Shiitake_3', 'RNO4_Garnet_4', 'RNO4_Bat pentagram_5',
        'RNO4_Life Vessel_6', 'RNO4_Heart Vessel_7', 'RNO4_Potion_8', 'RNO4_Shiitake_9', 'RNO4_Shiitake_10',
        'RNO4_Opal_11', 'RNO4_Life Vessel_12', 'RNO4_Diamond_13', 'RNO4_Zircon_14', 'RNO4_Heart Vessel_15',
        'RNO4_Meal ticket_16', 'RNO4_Meal ticket_17', 'RNO4_Meal ticket_18', 'RNO4_Meal ticket_19',
        'RNO4_Meal ticket_20', 'RNO4_Zircon_21', 'RNO4_Pot roast_22', 'RNO4_Dark blade_23', 'RNO4_Manna prism_24',
        'RNO4_Elixir_25', 'RNO4_Osafune katana_26', 'Force of echo', 'RNZ0_Heart Vessel_1', 'RNZ0_Life Vessel_2',
        'RNZ0_Goddess shield_3', 'RNZ0_Manna prism_4', 'RNZ0_Katana_5', 'RNZ0_High potion_6', 'RNZ0_Turquoise_7',
        'RNZ0_Ring of arcana_8', 'RNZ0_Resist dark_9', 'RNZ1_Magic missile_0', 'RNZ1_Karma coin_1',
        'RNZ1_Str. potion_2', 'RNZ1_Luminus_3', 'RNZ1_Smart potion_4', 'RNZ1_Dragon helm_5', 'RNZ1_Diamond_6',
        'RNZ1_Life apple_7', 'RNZ1_Sunstone_8', 'RNZ1_Life Vessel_9', 'RNZ1_Heart Vessel_10', 'RNZ1_Moon rod_11',
        'RNZ1_Bwaka knife_94094164', 'RNZ1_Pot roast_94094156', 'RNZ1_Shuriken_94094160', 'RNZ1_TNT_94094168',
        'Ring of vlad', 'RTOP_Sword of dawn_0', 'RTOP_Iron ball_1', 'RTOP_Zircon_2', 'RTOP_Bastard sword_4',
        'RTOP_Life Vessel_5', 'RTOP_Heart Vessel_6', 'RTOP_Life Vessel_7', 'RTOP_Heart Vessel_8',
        'RTOP_Life Vessel_9', 'RTOP_Heart Vessel_10', 'RTOP_Royal cloak_11', 'RTOP_Resist fire_17',
        'RTOP_Resist ice_18', 'RTOP_Resist thunder_19', 'RTOP_Resist stone_20', 'RTOP_High potion_21',
        'RTOP_Garnet_22', 'RTOP_Lightning mail_23', 'RTOP_Library card_24', 'RARE_Life Vessel_8']
}
