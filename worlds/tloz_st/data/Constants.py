from dataclasses import dataclass

from .Addresses import STAddr
from .Items import ITEM_GROUPS

VERSION = "0.7.0"
ROM_HASH = "f2dc6c4e093e4f8c6cbea80e8dbd62cb"


STARTING_FLAGS = [
    # Starting flags (these are in the same memory block so can be simplified, but it's called once and this is
    # easier to bugfix)

    [STAddr.adv_flags_0, 0x04],  # restore spirit train cutscene skip
    [STAddr.adv_flags_1, 0x00],  # forest restoration duet done
    [STAddr.adv_flags_2, 0xF0],  # sword tutorial and intro stuff
    [STAddr.adv_flags_3, 0x47],  # split ToS and zelda 1st convo
    [STAddr.adv_flags_4, 0xB4],  # load train to ToS
    [STAddr.adv_flags_5, 0x74],  # train quill tutorial skip
    [STAddr.adv_flags_6, 0xEC],  # Intro stuff
    [STAddr.adv_flags_7, 0x3D],  # postman & get zelda's letter
    [STAddr.adv_flags_8, 0xc0],  # letters
    [STAddr.adv_flags_9, 0x0f],  # letters, marine temple entrance
    [STAddr.adv_flags_a, 0x7B],  # ocean realm
    [STAddr.adv_flags_b, 0x98],  # blizzard stuff
    [STAddr.adv_flags_c, 0xE2],  # convos
    [STAddr.adv_flags_f, 0xF0],  # ToS 4F 1st time entry
    [STAddr.adv_flags_10, 0x50],  # anjean section text
    [STAddr.adv_flags_12, 0x1B],  # zelda 1st phantom possession + mayascore bugs
    [STAddr.adv_flags_13, 0x08],  # whip minigame tutorial
    [STAddr.adv_flags_15, 0x58],  # post fleeing ToS 1F
    [STAddr.adv_flags_16, 0x38],  # ready for FS duet
    [STAddr.adv_flags_17, 0xCA],  # Skip an Anjean dialogue
    [STAddr.adv_flags_18, 0x07],  # HC intro Zelda
    [STAddr.adv_flags_19, 0x63],  # steem
    [STAddr.adv_flags_1a, 0x1C],  # rabbitland rock text
    [STAddr.adv_flags_1b, 0xEE],  # initial train cutscene skip, tos 3 zelda text
    [STAddr.adv_flags_1c, 0x25],  # ToS 3 zelda text
    [STAddr.adv_flags_1d, 0xF4],  # ToS 3 zelda text
    [STAddr.adv_flags_1e, 0x8B],  # Valley sanc
    [STAddr.adv_flags_1f, 0x01],  # Valley sanc
    [STAddr.adv_flags_20, 0x02],  # post valley sanc elder text
    # [STAddr.adv_flags_21, 0x02],  # elder text, despawns kagoron
    [STAddr.adv_flags_22, 0x3C],  # buy cargo first time
    [STAddr.adv_flags_23, 0xc0],  # teao tutorial
    [STAddr.adv_flags_24, 0x08],  # move HC guards
    [STAddr.adv_flags_26, 0x3C],  # end of Tos section zelda texts
    [STAddr.adv_flags_29, 0x80],  # tos 2 zelda text
    [STAddr.adv_flags_2a, 0x23],  # ToS 6 zelda text, gtr
    [STAddr.adv_flags_2b, 0x01],  # ToS 7 zelda text
    [STAddr.adv_flags_2d, 0x20],  # ToS 7 zelda text
    [STAddr.adv_flags_2f, 0x4c],  # linebeck 1st convo
    [STAddr.adv_flags_30, 0x00],  # Prevent GTR death. or not, start with long track?
    [STAddr.adv_flags_31, 0x18],  # Possess Phantom
    [STAddr.adv_flags_33, 0x0E],  # dark ore first conv0
    [STAddr.adv_flags_35, 0x10],  # kagoron text after giving ice
    [STAddr.adv_flags_37, 0x10],  # teacher text skip
    [STAddr.adv_flags_38, 0x08],  # goron text
    [STAddr.adv_flags_3d, 0xE0],  # ToS safe zone tutorial, dos tablet
    [STAddr.adv_flags_3e, 0x09],  # Disorientation station guard
    [STAddr.adv_flags_3f, 0x05],  # Dark ore mine cs
    [STAddr.adv_flags_40, 0x04],  # 1st portal text
    [STAddr.adv_flags_41, 0x03],  # ToS 6 Zelda Text
    [STAddr.adv_flags_42, 0x86],  # board with zelda
    [STAddr.adv_flags_44, 0x02],  # tos 2 zelda text
    [STAddr.adv_flags_46, 0x20],  # 7f zelda collapse
    [STAddr.adv_flags_48, 0x10],  # alfonzo giving cannon
    [STAddr.adv_flags_4e, 0x80],  # blizzard void out
    [STAddr.adv_flags_51, 0x03],  # ToS Staircase cutscene skip
    [STAddr.adv_flags_52, 0x80],  # ToS Staircase cutscene skip
    [STAddr.adv_flags_53, 0x77],  # ToS Staircase 2 zelda text skip
    [STAddr.adv_flags_54, 0xA8],  # first spirit train journey+portal
    [STAddr.adv_flags_55, 0x86],  # trials
    [STAddr.adv_flags_56, 0x1],  # trials
    [STAddr.adv_flags_57, 0xD1],  # first song statue text

    # Set treasures to 0
    [STAddr.all_treasure_count, [0]*32],
    # Center stamp coords
    [STAddr.stamp_coords, [0xB8, 0x48, 0x48, 0x48]*10]
]

# You can find the stage flags for a stage by checking the stage data pointer of 0x265164 and adding an offset of 176 (note decimal) to its value
# then endian is opposite of what it usually is cause i like to use spreadsheets to import it.
# check the stage flag page in the spreadsheet to see what each bit corresponds to.
STAGE_FLAGS = {

    0x04: [0x02, 0x00, 0x00, 0x00], # Forest Realm
    0x2F: [0x9E, 0x00, 0x00, 0x00], # Outset Village
    0x29: [0x10, 0x00, 0x00, 0x00], # Castle Town
    0x28: [0x08, 0x03, 0x00, 0x00],  # Hyrule Castle
    0x13: [0xFE, 0x36, 0x00, 0x00],  # Tower of Spirits (Main)
    0x14: [0x08, 0x00, 0x00, 0x0], # Tower of Spirits (Base)
    # 0x17: [0x00, 0x00, 0x00, 0x17],  # Tower of Spirits (Stairs)
    0x18: [0x04, 0x00, 0x00, 0x00], # Tunnel to ToS
    0x19: [0x00, 0x00, 0x00, 0x0D],  # Wooded Temple
    0x1E: [0x00, 0x00, 0x00, 0x1A], # Stagnox
    0x2A: [0x02, 0x00, 0x00, 0x00],  # Mayscore/Whittleton
    0x30: [0x3C, 0x00, 0x00, 0x20],  # Woodland Sanctuary
    # 0x38: [0x00, 0x00, 0x00, 0x38],  # Mayscore Forest
    0x3E: [0x00, 0x08, 0x00, 0x00],  # Rabbit Haven
    0x37: [0x96, 0x00, 0x00, 0x00],  # Trading Post
    # 0x05: [0x00, 0x00, 0x00, 0x05], # Snow Realm
    0x2B: [0x06, 0x04, 0x00, 0x00], # Anouki Village
    0x31: [0x0A, 0x00, 0x00, 0x00], # Snow Sanctuary
    0x1A: [0x00, 0x40, 0x20, 0x40], # Blizzard Temple
    0x1F: [0x00, 0x00, 0x00, 0xC0], # Fraaz
    0x35: [0x12, 0x00, 0x00, 0x00], # Icy Spring
    # 0x36: [0x00, 0x00, 0x00, 0x36], # Bridge Worker's Home
    0x3F: [0x50, 0xE0, 0x01, 0x00], # Slippery/snowdrift Station
    0x2c: [0x2, 0x0, 0x0, 0x0],  # Papuzia
    0x32: [0x1e, 0x0, 0x0, 0x0],  # Island Sanc
    0x3a: [0x10, 0x40, 0x0, 0x0],  # Pirate Hideout
    0x2e: [0xB4, 0x0, 0x0, 0x0],  # Goron
    0x1c: [0x0, 0x00, 0x1C, 0x0],  # Mountain Temple
    0x21: [0xA, 0x00, 0x0, 0x0],  # Vulcano
    0x3C: [0x2, 0x0, 0x0, 0x0],  # GTR
    0x40: [0xE, 0x0, 0x0, 0x0],  # Disorientation Station
    0x41: [0x0, 0x80, 0x1a, 0x0],  # EotE
    0x34: [0x2, 0x1, 0x0, 0x0],  # Sand Sanc
    0x1d: [0x0, 0x3, 0x9, 0x0], # Desert Temple
    0x3d: [0x2, 0x0, 0x9, 0x0],  # DOM
}

@dataclass
class ItemModel:
    name: str
    offset: int
    value: int
    crash_in_shops: bool = False

    def __hash__(self):
        return self.offset

ITEM_MODELS = [
    ItemModel("Shield", 0, 0x41646873),
    ItemModel("Sword", 1, 0x41647773),
    ItemModel("Whirlwind", 2, 0x646E7274),
    ItemModel("Bomb Bag", 3, 0x626D6F62),
    ItemModel("Bow", 4, 0x41776F62),
    ItemModel("Boomerang", 5, 0x6E726D62),
    ItemModel("Whip", 6, 0x70696877),
    ItemModel("Sand Wand", 7, 0x646F7273),

    ItemModel("Key", 9, 0x4E79656B),
    ItemModel("Boss Key", 10, 0x4279656B),

    ItemModel("Green Rupee", 11, 0x47707572),
    ItemModel("Blue Rupee", 12, 0x42707572),
    ItemModel("Red Rupee", 13, 0x52707572),
    ItemModel("Big Green Rupee", 14, 0x47707572),
    ItemModel("Big Red Rupee", 15, 0x52707572),
    ItemModel("Gold Rupee", 16, 0x4C707572),

] + [
    ItemModel(f"Force Gem {i}", i, 0x59637266) for i in list(range(17, 20)) + list(range(34, 37)) + list(range(42, 61))
] + [

    ItemModel("Forest Glyph", 20, 0x4174696C),
    ItemModel("Snow Glyph", 21, 0x4274696C),
    ItemModel("Ocean Glyph", 22, 0x4374696C),
    ItemModel("Fire Glyph", 23, 0x4474696C),

    ItemModel("Forest Glyph 2", 24, 0x4174696C),  # Probably restorations?
    ItemModel("Snow Glyph 2", 25, 0x4274696C),
    ItemModel("Ocean Glyph 2", 26, 0x4374696C),
    ItemModel("Fire Glyph 2", 27, 0x4474696C),

    ItemModel("Ocean Glyph 3", 28, 0x4374696C),  # Sand Realm?
    ItemModel("Forest Glyph 3", 29, 0x4474696C), # Compass of light tracks?

    ItemModel("Hero's Clothes Intro", 37, 0x416F6C63),
    ItemModel("Letter Zelda", 38, 0x4C6D7470),
    ItemModel("Heart Container", 39, 0x75747268),
    ItemModel("Medium Quiver", 40, 0x4D647061),
    ItemModel("Medium Bomb Bag", 41, 0x4D626D62),

    ItemModel("Spirit Flute", 61, 0x746C6670),
    ItemModel("Stamp Book", 62, 0x706D7473),
    ItemModel("Bow of Light", 63, 0x42776F62),
    ItemModel("Nothing", 64, 0x42647773),  # Lokomo sword?

    ItemModel("Prize Postcards", 65, 0x437A7270),
    ItemModel("Red Potion", 66, 0x52766572),
    ItemModel("Purple Potion", 67, 0x50766572),
    ItemModel("Yellow Potion", 68, 0x59766572),

    ItemModel("Demon Fossil", 69, 0x736E6F6D),
    ItemModel("Stalfos Skull", 70, 0x626C7473),
    ItemModel("Star Fragment", 71, 0x72617473),
    ItemModel("Bee Larvae", 72, 0x65656562),

    ItemModel("Wood Heart", 73, 0x6E72726D),
    ItemModel("Dark Pearl Loop", 74, 0x426C7270),
    ItemModel("White Pearl Loop", 75, 0x416C7270),
    ItemModel("Ruto Crown", 76, 0x6E777263),

    ItemModel("Dragon Scale", 77, 0x616C6F7A),
    ItemModel("Pirate Necklace", 78, 0x63656E70),
    ItemModel("Palace Dish", 79, 0x6C776F62),
    ItemModel("Goron Amber", 80, 0x6E6F6C67),

    ItemModel("Mystic Jade", 81, 0x6564616A),
    ItemModel("Ancient Coin", 82, 0x6E696F63),
    ItemModel("Alchemy Stone", 83, 0x646C6F67),
    ItemModel("Regal Ring", 84, 0x676E6972),

    ItemModel("Arrow Refill", 85, 0x74737261),
    ItemModel("Bomb Refill", 86, 0x74736D62),
    ItemModel("Sold Out", 87, 0x646C6F73),
    ItemModel("Ancient Shield", 88, 0x42646873),
    ItemModel("Large Quiver", 89, 0x4C647061),
    ItemModel("Large Bomb Bag", 90, 0x4C626D62),

    ItemModel("Tear of Light", 95, 0x756B7A73),
    ItemModel("Compass of Light", 96, 0x706D634C),
    ItemModel("Green Scroll", 97, 0x426B616D),
    ItemModel("Purple Scroll", 98, 0x416B616D),
    ItemModel("Letter", 99, 0x4C6D7470),

    ItemModel("SoA", 100, 0x66706467),  # Songs, all use the same model as spirit flute
    ItemModel("SoH", 101, 0x66706467),  # Songs
    ItemModel("SoB", 102, 0x66706467),  # Songs
    ItemModel("SoL", 103, 0x66706467),  # Songs
    ItemModel("SoD", 104, 0x66706467),  # Songs

    ItemModel("Rabbit Net", 105, 0x746E6272),
    ItemModel("Beedle Bronze", 106, 0x74696F70),
    ItemModel("Beedle Silver", 107, 0x53696F70),
    ItemModel("Beedle Gold", 108, 0x47696F70),
    ItemModel("Beedle Platinum", 109, 0x50696F70),
    ItemModel("Beedle Diamond", 110, 0x44696F70),
    ItemModel("Beedle Freebie", 111, 0x46696F70),
    ItemModel("Beedle Points", 112, 0x35696F70),

    ItemModel("Letter 113", 113, 0x4C6D7470),
    ItemModel("Hero's Clothes", 114, 0x416F6C63),
    ItemModel("Engineer's Clothes", 115, 0x426F6C63),

]
ITEM_MODEL_LOOKUP: dict[str, "ItemModel"] = {i.name: i for i in ITEM_MODELS}
OFFSET_TO_MODEL: dict[int, "ItemModel"] = {i.offset: i for i in ITEM_MODELS}

STAGES = {
    0x4: "Forest Realm",
    0x5: "Snow Realm",
    0x6: "Ocean Realm",
    0x7: "Fire Realm",
    0x8: "Train Tutorial",
    # 0x9: "Lost in the Woods",
    0xA: "Underwater Tracks",
    0xB: "Snow Realm Rocktite Tunnel",
    0xC: "Sand Trial Rocktite Tunnel",
    0xD: "Dark Ore Mine Rocktite Tunnel",
    0xE: "Goron Target Range",
    0xF: "Dark Realm",
    0x10: "Demon Train",
    0x11: "Demon Train P2",
    0x12: "Demon Train P3",
    0x13: "ToS",
    0x14: "ToS Base",
    0x15: "ToS Summit",
    0x17: "ToS Stairs",
    0x18: "Tunnel to ToS",
    0x19: "Wooded Temple",
    0x1A: "Blizzard Temple",
    0x1B: "Marine Temple",
    0x1C: "Mountain Temple",
    0x1D: "Desert Temple",
    0x1E: "Stagnox",
    0x1F: "Fraaz",
    0x20: "Cactops/Phytops",
    0x21: "Cragma/Vulcano",
    0x22: "Skeldritch",
    0x23: "Staven Fight",
    0x24: "Cole Fight",
    0x25: "Malladus 1",
    0x26: "Malladus Spirit Duet",
    0x27: "Malladus P2",
    0x28: "Hyrule Castle",
    0x29: "Castle Town",
    0x2A: "Mayscore",
    0x2B: "Anouki Village",
    0x2C: "Papuzia Village",
    0x2D: "Goron Village West",
    0x2E: "Goron Village",
    0x2F: "Outset Village",
    0x30: "Woodland Sanctuary",
    0x31: "Snowfall Sanctuary",
    0x32: "Island Sanctuary",
    0x33: "Valley Sanctuary",
    0x34: "Dune Sanctuary",
    0x35: "Icy Spring",
    0x36: "Bridge Worker's Home",
    0x37: "Trading Post",
    0x38: "Mayscore Forest",
    0x39: "Papuzia Village South",
    0x3A: "Pirate Hideout",
    0x3B: "Pirate Hideout Minigame",
    0x3C: "Goron Target Range Station",
    0x3D: "Dark Ore Mine",
    0x3E: "Rabbit Haven",
    0x3F: "Snowdrift/Slippery Station",
    0x40: "Disorientation Station",
    0x41: "Ends of the Earth",
    0x42: "Lost at Sea Dungeon",
    0x43: "Train Carridge Ambush",
    # 0x44: "Train Interior CS",
    0x45: "Beedle, Train NPCs",
    0x46: "Take 'em all on Forest theme",
    0x47: "Take 'em all on Snow theme",
    0x48: "Take 'em all on Ocean theme",
    0x49: "Take 'em all on Fire theme",
    0x4A: "Take 'em all on Sand theme",
    0x4B: "TEAO Stagnox",
    0x4C: "TEAO Fraaz",
    0x4D: "TEAO Cactops",
    0x4E: "TEAO Vulcano",
    0x4F: "TEAO Capbone",
    # 0x50: "Train roof CS",
    0x79: "From Menu",
}


TREASURE_PRICES = {t: value for treasure_type, value in zip(["Common", "Uncommon", "Rare", "Super Rare"], [50, 150, 500, 2500]) for t in ITEM_GROUPS[treasure_type + " Treasures"]}

LOCATION_GROUPS: dict[str, set[str]] = {}

rabbit_realms = ["Grass", "Snow", "Ocean", "Mountain", "Sand"]

grass_rabbits = [
    "Grass Rabbit",
    "Grass Rabbits (2)",
    "Grass Rabbits (3)",
    "Grass Rabbits (4)",
    "Grass Rabbits (5)",
    "Grass Rabbits (10)"
]
snow_rabbits = [
    "Snow Rabbit",
    "Snow Rabbits (2)",
    "Snow Rabbits (3)",
    "Snow Rabbits (4)",
    "Snow Rabbits (5)",
    "Snow Rabbits (10)"
]
ocean_rabbits = [
    "Ocean Rabbit",
    "Ocean Rabbits (2)",
    "Ocean Rabbits (3)",
    "Ocean Rabbits (4)",
    "Ocean Rabbits (5)",
    "Ocean Rabbits (10)"
]
mountain_rabbits = [
    "Mountain Rabbit",
    "Mountain Rabbits (2)",
    "Mountain Rabbits (3)",
    "Mountain Rabbits (4)",
    "Mountain Rabbits (5)",
    "Mountain Rabbits (10)"
]
sand_rabbits = [
    "Sand Rabbit",
    "Sand Rabbits (2)",
    "Sand Rabbits (3)",
    "Sand Rabbits (4)",
    "Sand Rabbits (5)",
    "Sand Rabbits (10)"
]

DUNGEON_NAMES = [
    "Tunnel to ToS",
    "ToS", #Tower of Spirits
    "Wooded Temple",
    "Blizzard Temple",
    "Marine Temple",
    "Mountain Temple",
    "Desert Temple"
]

DUNGEON_TO_BOSS_ITEM_LOCATION = {
    "ToS 1": "ToS 3F Forest Rail Glyph",
    "ToS 2": "ToS 7F Snow Rail Glyph",
    "ToS 3": "ToS 12F Ocean Rail Glyph",
    "ToS 4": "ToS 17F Fire Rail Glyph",
    "ToS 5": "ToS 23F Defeat Staven",
    "ToS 6": "ToS 24F Final Chest",
    "Wooded Temple": "Wooded Temple Dungeon Reward",
    "Blizzard Temple": "Blizzard Temple Dungeon Reward",
    "Marine Temple": "Marine Temple Dungeon Reward",
    "Mountain Temple": "Mountain Temple Dungeon Reward",
    "Desert Temple": "Desert Temple Dungeon Reward",
    "Take 'em All On 3": "Castle Town Take 'em All On Level 3",
    "Lost at Sea": "Lost at Sea Final Chest"
}

BOSS_LOCATION_TO_EVENT_REGION = {
    "Wooded Temple Dungeon Reward": "wt stagnox",
    "Blizzard Temple Dungeon Reward": "bt fraaz",
    "Marine Temple Dungeon Reward": "oct phytops",
    "Mountain Temple Dungeon Reward": "mtt boss",
    "Desert Temple Dungeon Reward": "skeldritch",
    "ToS 3F Forest Rail Glyph": "tos 3f rail map",
    "ToS 7F Snow Rail Glyph": "tos 7f rail map",
    "ToS 12F Ocean Rail Glyph": "tos 11f",
    "ToS 17F Fire Rail Glyph": "tos 16f",
    "ToS 23F Defeat Staven": "tos staven",
    "ToS 24F Final Chest": "tos 24f",
    "Castle Town Take 'em All On Level 3": "teao 3",
    "Lost at Sea Final Chest": "las 5th room"
}

BOSS_LOCATION_TO_POST_LOCATIONS = {
    "Wooded Temple Dungeon Reward": ["Wooded Temple Boss Heart Container"],
    "Blizzard Temple Dungeon Reward": ["Blizzard Temple Boss Heart Container"],
    "Marine Temple Dungeon Reward": ["Marine Temple Heart Container"],
    "Mountain Temple Dungeon Reward": ["Mountain Temple Boss Heart Container"],
    "Desert Temple Dungeon Reward": ["Desert Temple Boss Heart Container", "Desert Temple Bow of Light Chest"]
}

DUNGEON_KEY_DATA = {
    0x13: {
        "name": "ToS",
        "address": STAddr.key_storage_tos,
        "filter": 0xFF,
        "value": 1,
        "size": 8,
    },
    0x132: {
        "name": "ToS 2",
        "address": STAddr.key_storage_tos,
        "filter": 0x3,
        "value": 1,
        "size": 2,
    },
    0x134: {
        "name": "ToS 4",
        "address": STAddr.key_storage_tos,
        "filter": 0xC,
        "value": 4,
        "size": 2,
    },
    0x135: {
        "name": "ToS 5",
        "address": STAddr.key_storage_tos,
        "filter": 0x30,
        "value": 0x10,
        "size": 2,
    },
    0x136: {
        "name": "ToS 6",
        "address": STAddr.key_storage_tos,
        "filter": 0xC0,
        "value": 0x40,
        "size": 2,
    },
    0x18: {
        "name": "Tunnel to ToS",
        "address": STAddr.key_storage_0,
        "filter": 0x01,
        "value": 1,
        "size": 1,
    },
    0x19: {
        "name": "Wooded Temple",
        "address": STAddr.key_storage_0,
        "filter": 0x06,
        "value": 0x02,
        "size": 2,
    },
    0x1A: {
        "name": "Blizzard Temple",
        "address": STAddr.key_storage_0,
        "filter": 0x08,
        "value": 0x08,
        "size": 1,
    },
    0x1B: {
        "name": "Marine Temple",
        "address": STAddr.key_storage_0,
        "filter": 0x30,
        "value": 0x10,
        "size": 2,
    },
    0x1C: {
        "name": "Mountain Temple",
        "address": STAddr.key_storage_2,
        "filter": 0x3,
        "value": 0x1,
        "size": 2,
    },
    0x1D: {
        "name": "Desert Temple",
        "address": STAddr.key_storage_0,
        "filter": 0xC0,
        "value": 0x40,
        "size": 2,
    }
}


BOSS_KEY_DATA = {
    0x1902: {
        "y": 4915,
        "pointer": STAddr.wt_bk_pointer,
        "location": "Wooded Temple 3F Boss Key",
        "door": STAddr.wt_boss_door,
        "dungeon": "Wooded Temple"
    },
    0x1a02: {
        "y": 0,
        "pointer": STAddr.bt_bk_pointer,
        "location": "Blizzard Temple 2F Boss Key",
        "door": STAddr.bt_boss_door,
        "dungeon": "Blizzard Temple"
    },
    0x1b05: {
        "y": 0,
        # "pointer": STAddr.oct_bk_pointer,
        "location": "Marine Temple 6F Boss Key",
        "door": STAddr.oct_boss_door,
        "dungeon": "Marine Temple",
        "search_data": (16, 3, 59392, 4, STAddr.oct_actor_table_start),
        "deletion_data": (8, 0)  # size, offset
    },
    0x1c04: {
        "y": -48000,
        "pointer": STAddr.mtt_bk_pointer,
        "location": "Mountain Temple B3 Boss Key",
        "door": STAddr.mtt_boss_door,
        "dungeon": "Mountain Temple",
        "deletion_data": (4, 64)
    },
    0x1d03: {
        "y": -2867,
        "pointer": STAddr.dt_bk_pointer,
        "location": "Desert Temple B1 Boss Key",
        "door": STAddr.dt_boss_door,
        "dungeon": "Desert Temple",
        "deletion_data": (4, 8)
    },
    0x1309: {
        "y": 0,
        # "pointer": STAddr.tos_actor_table_pointer_0,
        "location": "ToS 10F Boss Key",
        "door": STAddr.tos3_boss_door,
        "dungeon": "ToS 3",
        "door_coords": 0xffff2ffc00000000fffffffc,
        "deletion_data": (4, 0)
    },
    0x1318: {
        "y": 0,
        # "pointer": STAddr.tos_actor_table_pointer_0,
        "location": "ToS 22F Boss Key",
        "door": STAddr.tos5_boss_door,
        "dungeon": "ToS 5",
        "door_coords": 0x4ffc000000000000affc,
        "deletion_data": (4, 0)
    },
}

HINTS_ON_SCENE = {
    # 0xB11: {  # Mercay Shop
    #     "island_shop": True
    # },
    # 0xC0E: {  # Molida Shop
    #     "island_shop": True
    # },
    # 0x1014: {  # Goron Shop
    #     "island_shop": True
    # },
    # 0x130B: {  # Eddo Cannon Island
    #     "unique": ["Cannon Island Cannon", "Cannon Island Salvage Arm"]
    # },
    # 0x500: {  # Beedle Shop
    #     "unique": ["Beedle Shop Wisdom Gem"],
    #     "beedle": True  # TODO: make this modular, instead of hard coding item requirements
    # },
    # 0xb0A: {  # Oshus Dungeon hints
    #     "dungeon_hints": 1
    # },
    # 0x2600: {  # TotOK Dungeon hints
    #     "dungeon_hints": 2
    # },
    # 0x1701: {
    #     "spirit_island_hints": True
    # },
}


SHOP_TREASURE_DATA = {
    0x290a: [{
        "locations": ["Castle Town Shop Treasure 1", "Castle Town Shop Treasure 2"],
        "group": "Uncommon"
    }],
    0x2a05: [{
        "locations": ["Mayscore Shop Treasure 1", "Mayscore Shop Treasure 2"],
        "group": "Common"
    }],
    0x4503: [{
        "locations": ["Beedle Shop Uncommon Treasure"],
        "group": "Uncommon"
    }, {
        "locations": ["Beedle Shop Rare Treasure"],
        "group": "Rare"
    }],
    0x3103: [{
        "locations": ["Snowfall Supermarket Treasure"],
        "group": "Uncommon"
    }],
}

potion_location_lookup = {
    0x4503: {1: "Beedle Shop Red Potion",
             2: "Beedle Shop Purple Potion"},
    0x2a05: {1: "Mayscore Shop Red Potion"},
    0x290a: {1: "Castle Town Shop Red Potion"},
    0x3103: {1: "Snowfall Supermarket Red Potion",
             2: "Snowfall Supermarket Purple Potion"},
    0x2c02: {3: "Papuzia Shop Yellow Potion",
             2: "Papuzia Shop Purple Potion"},
    0x2e06: {3: "Goron Shop Yellow Potion",
             2: "Goron Shop Purple Potion"}
}

ammo_shop_lookup = {
    0x2c02: {STAddr.bomb_count: "Papuzia Shop Bombs",
             STAddr.arrow_count: "Papuzia Shop Arrows"},
    0x4503: {STAddr.bomb_count: "Beedle Shop Bomb Refill"},
    0x2e06: {STAddr.bomb_count: "Goron Shop Bomb Refill"}
}

tear_lookup = {1: 3, 4: 6, 9: 9, 13: 12, 18: 15, 30: 16}
big_tear_lookup = {1:1, 4:2, 9: 3, 13: 4, 18: 5, 30: 6}

DUNGEON_STAGES_TO_ENTRANCE_SCENE = {
    0x13: 0x1401,
    0x15: 0x1401,
    0x17: 0x1401,
    0x23: 0x1401,
    0x1A: 0x1A00,
    0x19: 0x1900,
    0x1E: 0x1900,
    0x1F: 0x1A00
}

# Used by rule builder
ITEM_MAPPING = {
        i: "Rupees" for i in ITEM_GROUPS["Rupee Items"]
    } | {
        f"Grass Rabbits ({i})": "Grass Rabbit" for i in list(range(2, 6)) + [10]
    } | {
        f"Snow Rabbits ({i})": "Snow Rabbit" for i in list(range(2, 6)) + [10]
    } | {
        t : "Treasure" for t in ITEM_GROUPS["All Treasures"]
    }

# Stamp stuff
STAMPS = []

# Decode classification for humans
CLASSIFICATION = {
    1: "Progression",
    2: "Useful",
    4: "Trap",
    9: "Prog Skip Balancing",
    0: "Filler"
                  }

UT_EVENT_DATA = {
    0x2900: [{"address": STAddr.adv_flags_11,
           "value": 0x40,
           "entrance": "EVENT: Pick up Alfonzo"}],
    0x3700: [{"address": STAddr.adv_flags_24,
              "value": 0x10,
              "entrance": "EVENT: Give Regal Ring to Linebeck"}],
    0x2E00: [{"address": STAddr.adv_flags_1f,
              "value": 0x80,
              "entrance": "EVENT: Bring Ice to Kagoron"}]
}



ENTRANCE_TO_TOS_ORDER = {
    "Tower of Spirits Exit Staven": 6,
    "Tower of Spirits Summit Enter Altar": 7,
    "Tower of Spirits Enter Section 1": 1,
    "Tower of Spirits Enter Section 2": 2,
    "Tower of Spirits Enter Section 3": 3,
    "Tower of Spirits Enter Section 4": 4,
    "Tower of Spirits Enter Section 5": 5,
}

EXIT_TO_TOS_SECTION = {
    "ToS 30F Exit": 6,
    "ToS 18F Exit": 5,
    "ToS 13F Exit": 4,
    "ToS 8F Exit": 3,
    "ToS 4F Exit": 2,
    "ToS 1F Exit": 1,
}

KEY_COUNTS = {
    "Small Key (Wooded Temple)": 2,
    "Small Key (Blizzard Temple)": 1,
    "Small Key (Marine Temple)": 2,
    "Small Key (Mountain Temple)": 3,
    "Small Key (Desert Temple)": 2,
    "Mountain Temple Snurglar Key": 3,
    "Small Key (ToS 2)": 2,
    "Small Key (ToS 4)": 3,
    "Small Key (ToS 5)": 2,
    "Small Key (ToS 6)": 3,
    "Small Key (Tunnel to ToS)": 1,
}

BOSS_ROOM_TO_BLOCKED_ITEM_GROUP: dict[int, str] = {
    0x1e00: "Tracks: Forest Source",
    0x1f00: "Tracks: Snow Source",
    0x2000: "Tracks: Ocean Source",
    0x2100: "Tracks: Fire Source",
}

TOS_SECTION_TO_EXIT = {section: e for e, section in EXIT_TO_TOS_SECTION.items()}

BOSS_WARP_SCENE_LOOKUP = {
    0x1302: "ToS 1F Exit",
    0x1306: "ToS 4F Exit",
    0x130b: "ToS 8F Exit",
    0x130f: "ToS 13F Exit",
    0x1314: "ToS 18F Exit",
    0x1323: "ToS 30F Exit",
}

special_respawn_stages = {
    0x15: (0x14, 1, 1),
    0x23: (0x14, 1, 1)
}

TOS_FLOOR_TO_SECTION = {
    0: 1,
    1: 1,
    2: 1,
    3: 2,
    4: 2,
    5: 2,
    6: 2,
    7: 3,
    8: 3,
    9: 3,
    0xA: 3,
    0xB: 3,
    0xC: 4,
    0xD: 4,
    0xE: 4,
    0xF: 4,
    0x10: 4,
    0x11: 5,
    0x12: 5,
    0x13: 5,
    0x14: 5,  # 23F
    0x17: 5,  # 21F
    0x18: 5,  # 22F

    0x15: 3,
    0x16: 3,

    0x28: 1,
    0x29: 2,
    0x2A: 3,
    0x2B: 4,
    0x2C: 6,
    0x2D: 6,
    0x2E: 5,

    0x1d: 6,  # 31F
    0x1e: 6,  # 30F
    0x1f: 6,  # 29F
    0x20: 6,  # 28F
    0x21: 6,  # 27F
    0x22: 6,  # 26F
    0x23: 6,  # 24F
    0x24: 6,  # 25F
}

#TREASURE_READ_LIST = {i: (0x1BA5AC + i * 4, 4, "Main RAM") for i in range(8)}
