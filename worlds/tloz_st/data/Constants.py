
from dataclasses import dataclass

from .Addresses import STAddr
from .Items import ITEM_GROUPS

VERSION = "0.7.0"
ROM_HASH = "f2dc6c4e093e4f8c6cbea80e8dbd62cb"


STARTING_FLAGS = [
    # Starting flags (these are in the same memory block so can be simplified, but it's called once and this is
    # easier to bugfix)

    [STAddr.adv_flags_0, 0x04],  # restore spirit train cutscene skip
    # [STAddr.adv_flags_1, 0x00],  # forest restoration duet done
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

# Stage flags for opening blue warps
OPEN_WARPS = [
    [0, 0, 0, 0x40],
    [0, 0, 0, 0x80],
    [0, 0, 0, 0x40],
    [0, 2, 0, 0],
    [0, 0, 0, 0x40],
]

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
    0x43: "Train Carriage Ambush",
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
    "Wooded Temple": "Stagnox Boss Reward",
    "Blizzard Temple": "Fraaz Boss Reward",
    "Marine Temple": "Cactops Boss Reward",
    "Mountain Temple": "Vulcano Boss Reward",
    "Desert Temple": "Capbone Boss Reward",
    "Take 'em All On 3": "Castle Town Take 'em All On Level 3",
    "Lost at Sea": "Lost at Sea Final Chest"
}

BOSS_LOCATION_TO_EVENT_REGION = {
    "Stagnox Boss Reward": "wt stagnox",
    "Fraaz Boss Reward": "bt fraaz",
    "Cactops Boss Reward": "oct phytops",
    "Vulcano Boss Reward": "mtt pre vulcano",
    "Capbone Boss Reward": "dt skeldritch",
    "ToS 3F Forest Rail Glyph": "tos 3f rail map",
    "ToS 7F Snow Rail Glyph": "tos 7f rail map",
    "ToS 12F Ocean Rail Glyph": "tos 11f",
    "ToS 17F Fire Rail Glyph": "tos 16f",
    "ToS 23F Defeat Staven": "tos staven",
    "ToS 24F Final Chest": "tos 24f",
    "Castle Town Take 'em All On Level 3": "teao 3",
    "Lost at Sea Final Chest": "las event shield"
}

BOSS_LOCATION_TO_POST_LOCATIONS = {
    "Stagnox Boss Reward": ["Stagnox Boss Reward", "Stagnox Heart Container"],
    "Fraaz Boss Reward": ["Fraaz Boss Reward", "Fraaz Heart Container"],
    "Cactops Boss Reward": ["Cactops Boss Reward", "Cactops Heart Container"],
    "Vulcano Boss Reward": ["Vulcano Boss Reward", "Vulcano Heart Container"],
    "Capbone Boss Reward": ["Capbone Boss Reward", "Capbone Heart Container", "Desert Temple Bow of Light Chest"]
}

DUNGEON_TO_ENTRANCE = {
    "Wooded Temple": "Wooded Temple Lobby Enter Dungeon",
    "Blizzard Temple": "Blizzard Temple Lobby Enter Dungeon",
    "Marine Temple": "Marine Temple Lobby Enter Dungeon",
    "Mountain Temple": "Mountain Temple Lobby Enter Dungeon",
    "Desert Temple": "Desert Temple Lobby Enter Dungeon",
}

DUNGEON_TO_EXIT = {
    "Wooded Temple": "Wooded Temple 1F Exit",
    "Blizzard Temple": "Blizzard Temple 1F South Exit",
    "Marine Temple": "Marine Temple 1F Exit",
    "Mountain Temple": "Mountain Temple 1F Exit",
    "Desert Temple": "Desert Temple 1F Exit",
}

DUNGEON_TO_WARP_ENTRANCE = {
    "Wooded Temple": "Wooded Temple Lobby Blue Warp",
    "Blizzard Temple": "Blizzard Temple Lobby Blue Warp",
    "Marine Temple": "Marine Temple Lobby Blue Warp",
    "Mountain Temple": "Mountain Temple Lobby Blue Warp",
    "Desert Temple": "Desert Temple Lobby Blue Warp",
}

DUNGEON_TO_WARP_EXIT = {
    "Wooded Temple": "Wooded Temple 4F Blue Warp",
    "Blizzard Temple": "Blizzard Temple 3F Blue Warp",
    "Marine Temple": "Marine Temple 7F Blue Warp",
    "Mountain Temple": "Mountain Temple B4 Blue Warp",
    "Desert Temple": "Desert Temple B2 Blue Warp",
}

DUNGEON_TO_BOSS_STAIRCASE = {
    "Wooded Temple": "Wooded Temple 4F N Staircase",
    "Blizzard Temple": "Blizzard Temple 3F North Staircase",
    "Marine Temple": "Marine Temple 7F North Staircase",
    "Mountain Temple": "Mountain Temple B4 North Staircase",
    "Desert Temple": "Desert Temple B2 North Entrance",
}

BOSS_LOCATION_TO_EXIT = {
    "Stagnox Boss Reward": "Stagnox Exit",
    "Fraaz Boss Reward": "Fraaz Exit",
    "Cactops Boss Reward": "Cactops Exit",
    "Vulcano Boss Reward": "Vulcano Exit",
    "Capbone Boss Reward": "Capbone Exit",
}

DUNGEON_NAME_TO_BOSS_LOCATIONS = {
    "Wooded Temple": ["Stagnox Boss Reward", "Stagnox Heart Container"],
    "Blizzard Temple": ["Fraaz Boss Reward", "Fraaz Heart Container"],
    "Marine Temple": ["Cactops Boss Reward", "Cactops Heart Container"],
    "Mountain Temple": ["Vulcano Boss Reward", "Vulcano Heart Container"],
    "Desert Temple": ["Capbone Boss Reward", "Capbone Heart Container", "Desert Temple Bow of Light Chest"],
}

DUNGEON_NAME_TO_LOBBY_LOCATION = {
    "Wooded Temple": ["Wooded Temple Lobby Song Statue"],
    "Marine Temple": ["Marine Temple Lobby Song Statue", "Marine Temple Lobby Ferrus Force Gem"],
    "Mountain Temple": ["Mountain Temple Lobby Song Statue"],
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
        "location": "Wooded Temple 3F Boss Key",
        "door_coords": 0x00000FFC00000000FFFFFFFC,
        "dungeon": "Wooded Temple"
    },
    0x1a02: {
        "y": 0,
        "location": "Blizzard Temple 2F Boss Key",
        "door_coords": 0x00002FFC00000000FFFFDFFC,
        "dungeon": "Blizzard Temple"
    },
    0x1b05: {
        "y": 0,
        "location": "Marine Temple 6F Boss Key",
        "door_coords": 0xFFFFAFFC00002666FFFFFFFC,
        "dungeon": "Marine Temple",
        "search_data": [16, 3, 59392, 4],
        # "deletion_data": (8, 0)  # size, offset
    },
    0x1c04: {
        "y": -48000,
        "location": "Mountain Temple B3 Boss Key",
        "door_coords": 0xFFFF0FFC00001333FFFFFFFC,
        "dungeon": "Mountain Temple",
        "search_data": [16, 1, 0xD800, 4],
        "deletion_data": (4, 64)
    },
    0x1d03: {
        "y": -2867,
        "location": "Desert Temple B1 Boss Key",
        "door_coords": 0xFFFFCFFC0000000000003FFC,
        "dungeon": "Desert Temple",
        "search_data": [16, 1, 0xFFFED800, 4],
        "deletion_data": (4, 8)
    },
    0x1309: {
        "y": 0,
        "location": "ToS 10F Boss Key",
        "dungeon": "ToS 3",
        "section": 3,
        "door_coords": 0xffff2ffc00000000fffffffc,
        "deletion_data": (4, 0)
    },
    0x1318: {
        "y": 0,
        "location": "ToS 22F Boss Key",
        "dungeon": "ToS 5",
        "section": 5,
        "door_coords": 0x4ffc000000000000affc,
        "deletion_data": (4, 0)
    },
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
           "entrance": "EVENT: Castle Town Pick Up Alfonzo"},
             {"address": STAddr.cargo_0,
              "value": 4,
              "exact_read": True,
              "entrance": "EVENT: Castle Town Buy Cuccos"}
             ],
    0x3700: [{"address": STAddr.adv_flags_24,
              "value": 0x10,
              "entrance": "EVENT: Trading Post Give Regal Ring to Linebeck"},
             {"address": STAddr.passenger_tag_0,
              "value": 0x43524654,
              "exact_read": True,
              "entrance": "EVENT: Trading Post Pick Up Kenzo"}
             ],
    0x2E00: [{"address": STAddr.adv_flags_1f,
              "value": 0x80,
              "entrance": "EVENT: Goron Village Bring Ice to Kagoron"},
             {"address": STAddr.passenger_tag_0,
              "value": 0x474F5250,
              "exact_read": True,
              "entrance": "EVENT: Goron Village Pick Up Snow Goron"},
             {"address": STAddr.passenger_tag_0,
              "value": 0x474F4350,
              "exact_read": True,
              "entrance": "EVENT: Goron Village Pick Up City Goron"}
             ],
    0x2D02: [{"address": STAddr.adv_flags_18,
              "value": 0x8,
              "entrance": "EVENT: Mountain Altar Visit Kagoron"}],
    0x2F00: [{"address": STAddr.adv_flags_3b,
              "value": 0x2,
              "entrance": "EVENT: Outset Drop Off Ferrus"},
             {"address": STAddr.passenger_tag_0,
              "value": 0x4E434341,
              "exact_read": True,
              "entrance": "EVENT: Outset Pick Up Joe"}
             ],
    0x1b01: [{"address": "stage_flags",
              "value": 0x2,
              "offset": 1,
              "entrance": "EVENT: Marine Temple 2F Boulders"}],
    0x1b05: [{"address": "stage_flags",
              "value": 0x20,
              "offset": 1,
              "entrance": "EVENT: Marine Temple 6F Arena"}],
    0x1b07: [{"address": "stage_flags",
              "value": 0x1,
              "offset": 2,
              "entrance": "EVENT: Marine Temple Stamp Room Switch"}],
    0x3601: [{"address": STAddr.passenger_tag_0,
               "value": 0x43524654,
              "exact_read": True,
               "entrance": "EVENT: Bridge Worker's Home Pick Up Kenzo"}],
    0x2B00: [{"address": STAddr.passenger_tag_0,
              "value": 0x594B4350,
              "exact_read": True,
              "entrance": "EVENT: Anouki Village Pick Up Noko"}],
    0x2B01: [{"address": STAddr.passenger_tag_0,
              "value": 0x594B4150,
              "exact_read": True,
              "entrance": "EVENT: Anouki Village Pick Up Kofu"}],
    0x290C: [{"address": STAddr.passenger_tag_0,
              "value": 0x43415742,
              "exact_read": True,
              "entrance": "EVENT: Castle Town Pick Up Mona"}],
    0x2A04: [{"address": STAddr.passenger_tag_0,
              "value": 0x464F4D52,
              "exact_read": True,
              "entrance": "EVENT: Mayscore Pick Up Dovok"}],
    0x2C00: [{"address": STAddr.passenger_tag_0,
              "value": 0x53595741,
              "exact_read": True,
              "entrance": "EVENT: Papuzia Village Pick Up Carben"},
             {"address": STAddr.cargo_0,
              "value": 3,
              "exact_read": True,
              "entrance": "EVENT: Papuzia Village Buy Fish"}
             ],
    0x3A00: [{"address": STAddr.passenger_tag_0,
              "value": 0x57414D41,
              "exact_read": True,
              "entrance": "EVENT: Pirate Hideout Pick Up Wadatsumi"}],
    # Cargo
    0x3500: [{"address": STAddr.cargo_0,
              "value": 0,
              "exact_read": True,
              "entrance": "EVENT: Icy Spring Buy Mega Ice"}],
    0x2A00: [{"address": STAddr.cargo_0,
              "value": 1,
              "exact_read": True,
              "entrance": "EVENT: Mayscore Buy Lumber"}],
    0x2C04: [{"address": STAddr.cargo_0,
              "value": 5,
              "exact_read": True,
              "entrance": "EVENT: Papuzia Village Buy Vessel"}],
    0x2D03: [{"address": STAddr.cargo_0,
              "value": 2,
              "exact_read": True,
              "entrance": "EVENT: Goron Field Buy Steel"}],
    0x3D01: [{"address": STAddr.cargo_0,
              "value": 6,
              "exact_read": True,
              "entrance": "EVENT: Dark Ore Mine Buy Ore"}],
    # Warps
    0x1903: [{"address": "stage_flags",
              "value": 0x40,
              "offset": 3,
              "entrance": "EVENT: Wooded Temple Open Blue Warp"}],
    0x1a03: [{"address": "stage_flags",
              "value": 0x80,
              "offset": 3,
              "entrance": "EVENT: Blizzard Temple Open Blue Warp"}],
    0x1b06: [{"address": "stage_flags",
              "value": 0x40,
              "offset": 3,
              "entrance": "EVENT: Marine Temple Open Blue Warp"}],
    0x1c05: [{"address": "stage_flags",
              "value": 0x2,
              "offset": 1,
              "entrance": "EVENT: Mountain Temple Open Blue Warp"}],
    0x1d04: [{"address": "stage_flags",
              "value": 0x40,
              "offset": 3,
              "entrance": "EVENT: Desert Temple Open Blue Warp"}],

    # GLP shortcuts
    0x1900: [{
        "entrance": "EVENT: Wooded Temple 1F Shortcut",
        "address": "stage_flags",
        "offset": 0,
        "value": 0x80
    }],
    0x1901: [{
        "entrance": "EVENT: Wooded Temple 2F Windmill",
        "address": "stage_flags",
        "offset": 1,
        "value": 0x4
    }],
    0x1a00: [{
        "entrance": "EVENT: Blizzard Temple 1F Bell Door 1",
        "address": "stage_flags",
        "offset": 0,
        "value": 0x20
    },{
        "entrance": "EVENT: Blizzard Temple 1F Bell Door 2",
        "address": "stage_flags",
        "offset": 1,
        "value": 0x2
    },{
        "entrance": "EVENT: Blizzard Temple 1F NE Door",
        "address": "stage_flags",
        "offset": 0,
        "value": 0x80
    },{
        "entrance": "EVENT: Blizzard Temple 1F NW Door",
        "address": "stage_flags",
        "offset": 1,
        "value": 0x8
    },{
        "entrance": "EVENT: Blizzard Temple 1F Bell Door 3",
        "address": "stage_flags",
        "offset": 1,
        "value": 0x20
    }],
    0x1a01: [{
        "entrance": "EVENT: Blizzard Temple B1 SE Windmill",
        "address": "stage_flags",
        "offset": 1,
        "value": 0x80
    }],
    0x1b02: [{
        "entrance": "EVENT: Marine Temple 3F South Branch",
        "address": "stage_flags",
        "offset": 0,
        "value": 0x4
    }],
    0x1b03: [{
        "entrance": "EVENT: Marine Temple 4F West Door",
        "address": "stage_flags",
        "offset": 0,
        "value": 0x8
    },{
        "entrance": "EVENT: Marine Temple 4F South Bridge",
        "address": "stage_flags",
        "offset": 0,
        "value": 0x40  # with flags, also open 0x20
    }],
    0x1b04: [{
        "entrance": "EVENT: Marine Temple 5F North Branches",
        "address": "stage_flags",
        "offset": 1,
        "value": 0x4
    },{
        "entrance": "EVENT: Marine Temple 5F SE Door",
        "address": "stage_flags",
        "offset": 1,
        "value": 0x8
    }],
    0x1c00: [{
        "entrance": "EVENT: Mountain Temple 1F SW Switch",
        "address": "stage_flags",
        "offset": 1,
        "value": 0x4
    },{
        "entrance": "EVENT: Mountain Temple 1F Main Door",
        "address": "stage_flags",
        "offset": 0,
        "value": 0x4
    }],
    0x1c02: [{
        "entrance": "EVENT: Mountain Temple B1 Arena",
        "address": "stage_flags",
        "offset": 0,
        "value": 0x40
    }],
    0x1c03: [{
        "entrance": "EVENT: Mountain Temple B2 Stalfos Arena",
        "address": "stage_flags",
        "offset": 0,
        "value": 0x20
    },{
        "entrance": "EVENT: Mountain Temple B2 SE Torches",
        "address": "stage_flags",
        "offset": 0,
        "value": 0x80
    },{
        "entrance": "EVENT: Mountain Temple B2 W Branch",
        "address": "stage_flags",
        "offset": 1,
        "value": 0x40
    }],
    0x1d03: [{
        "entrance": "EVENT: Desert Temple B1 Shortcut",
        "address": "stage_flags",
        "offset": 3,
        "value": 0x8
    },
    {
        "entrance": "EVENT: Desert Temple B1 Red Door",
        "address": "stage_flags",
        "offset": 2,
        "value": 0x80
    }
    ],
    0x1801: [{
        "entrance": "EVENT: Tunnel to the Tower 2F Door",
        "address": "stage_flags",
        "offset": 0,
        "value": 0x2
    }],
    0x3200: [{
        "entrance": "EVENT: Island Sanctuary Bridge",
        "address": "stage_flags",
        "offset": 1,
        "value": 0x8
    }],
    0x3300: [{
        "entrance": "EVENT: Valley Sanctuary Door",
        "address": "stage_flags",
        "offset": 1,
        "value": 0x1
    }],
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
    "ToS 31F Exit": 6,
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
    0x1323: "ToS 31F Exit",
}

special_respawn_stages = {
    0x15: (0x14, 1, 1),  # Tower
    0x23: (0x13, 0x14, 0)  # Staven
}

unsafe_respawn_stages = [
    0x4, 0x5, 0x8, 0x9, 0xb, 0xc,
    0x19, 0x1E,
    0x1a, 0x1F,
    0x1b, 0x20,
    0x1c, 0x21,
    0x1d, 0x22,
    0x28, 0x18, # HC
    0x40, 0x41,  # DO, EotE
    0x42  # Lost at sea
]

safe_respawn_rooms = [
    0x190A,
    0x1A04,
    0x1B0A,
    0x1C0A,
    0x1D06,
    0x4000,
    0x4100
]

TOS_FLOOR_SECTIONS_CANCEL_TEARS: dict[int, int] = {
    2: 1,
    6: 2,
    0xB: 3,
    0xF: 4,  # 17F
    0x1d: 6,  # 31F, canceled cause removes tears
    0x23: 6,  # 24F
}

TOS_FLOOR_TO_SECTION_SAFE: dict[int, int] = {
    0: 1,
    1: 1,

    3: 2,
    4: 2,
    5: 2,

    7: 3,
    8: 3,
    9: 3,
    0xA: 3,

    0xC: 4,
    0xD: 4,
    0xE: 4,
    0x10: 4, # 16F

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

    0x1e: 6,  # 30F
    0x1f: 6,  # 29F
    0x20: 6,  # 28F
    0x21: 6,  # 27F
    0x22: 6,  # 26F
    0x24: 6,  # 25F
}

directionality_etype_lookup: dict[int, str] = {
    0: "plando",
    1: "houses",
    2: "caves",
    3: "stations",
    4: "overworld",
    5: "dungeon_entrances",
    6: "bosses",
    7: "dungeon_rooms",
    8: "blue_warps",
    9: "portals",
    11: "tos_sections",
    12: "train",
    13: "tos_staircase",
    15: "castle",
    16: "disorientation",
    17: "eote",
    18: "las",
}

pool_name_lookup = {
    0: "pool_a",
    1: "pool_b",
    2: "pool_c",
    3: "in_own_dungeon"
}

@dataclass
class WarpStorageData:
    scene: int
    region: str
    valid_entrances: set = None
    invalid_entrances: set = None
    special_options: bool = False
    event: str = ""

    def __eq__(self, other):
        return self.scene == other

    def __ne__(self, other):
        return self.scene != other

    def __hash__(self):
        return self.scene

    def is_valid(self, entr, slot_data):
        if self.special_options:
            return self.process_special(entr, slot_data)
        res = True if not self.valid_entrances else entr in self.valid_entrances
        res = res if not self.invalid_entrances else entr not in self.invalid_entrances
        return  res

    def process_special(self, entr, slot_data):
        if self.scene == 0x2e00:
            res = {4, 5, 6}
            if slot_data["randomize_cargo"]:
                res.add(0xF)
            return entr not in res

        return False

_warp_data = [
    WarpStorageData(0x2f00, "outset village", event="EVENT: Visit Outset"),
    WarpStorageData(0x2a00, "mayscore"),
    WarpStorageData(0x2900, "castle town", event="EVENT: Visit Castle Town"),
    WarpStorageData(0x3000, "woodland sanc", {0}),
    WarpStorageData(0x190a, "wooded temple lobby"),
    WarpStorageData(0x3e00, "rabbit haven", event="EVENT: Visit Rabbit Haven"),
    WarpStorageData(0x2b00, "anouki village", event="EVENT: Visit Anouki Village"),
    WarpStorageData(0x3100, "snow sanc"),
    WarpStorageData(0x3500, "icyspring", event="EVENT: Visit Icy Spring"),
    WarpStorageData(0x3600, "bridge workers"),
    WarpStorageData(0x1a04, "blizzard temple lobby"),
    WarpStorageData(0x3f0a, "slippery"),
    WarpStorageData(0x3f00, "snowdrift"),
    WarpStorageData(0x3700, "trading post", {0, 1, 2}, event="EVENT: Visit Trading Post"),
    WarpStorageData(0x2c00, "papuzia village", invalid_entrances={5}, event="EVENT: Visit Papuzia Village"),
    WarpStorageData(0x3200, "island sanc"),
    WarpStorageData(0x1b0a, "marine temple lobby", event="EVENT: Visit Marine Temple"),
    WarpStorageData(0x3a00, "pirate hideout"),
    WarpStorageData(0x390a, "lost at sea"),
    WarpStorageData(0x3400, "sand sanc"),
    WarpStorageData(0x1d06, "desert temple lobby"),
    WarpStorageData(0x2e00, "goron village", special_options=True, event="EVENT: Visit Goron Village"),
    WarpStorageData(0x3c00, "goron target lobby"),
    WarpStorageData(0x1c0a, "mountain temple lobby"),
    WarpStorageData(0x4000, "disorientation station"),
    WarpStorageData(0x4100, "ends of the earth"),
    WarpStorageData(0x3d00, "dark ore mine"),
    WarpStorageData(0x400, "forest realm (ct)", {0, 1, 2, 3, 6, 0xa}),
    WarpStorageData(0x500, "snow realm (av)", {0, 0xA}),
    WarpStorageData(0x600, "ocean realm (pv)", {0, 2}),
    WarpStorageData(0x700, "fire realm (gv)", {0, 2, 4, 0x12}),
    WarpStorageData(0x1401, "tos lobby")
]
WARP_SCENES: dict[int, "WarpStorageData"] = {data.scene: data for data in _warp_data}

BOSS_LOCATION_TO_ENTRANCE: dict[str, str] = {
    "Stagnox Boss Reward": "Stagnox Exit",
    "Fraaz Boss Reward": "Fraaz Exit",
    "Cactops Boss Reward": "Cactops Exit",
    "Vulcano Boss Reward": "Vulcano Exit",
    "Capbone Boss Reward": "Capbone Exit"
}
DUNGEON_LOBBY_ENTRANCES: dict[str, tuple[str, str]] = {
    "Wooded Temple": ("Wooded Temple Lobby Enter Dungeon","Wooded Temple Lobby Blue Warp"),
    "Blizzard Temple": ("Blizzard Temple Lobby Enter Dungeon","Blizzard Temple Lobby Blue Warp"),
    "Marine Temple": ("Marine Temple Lobby Enter Dungeon", "Marine Temple Lobby Blue Warp"),
    "Mountain Temple": ("Mountain Temple Lobby Enter Dungeon", "Mountain Temple Lobby Blue Warp"),
    "Desert Temple": ("Desert Temple Lobby Enter Dungeon", "Desert Temple Lobby Blue Warp"),
}

BOSS_EXIT_TO_BOSS_WARP = {
    "Stagnox Exit": "Stagnox Blue Warp",
    "Fraaz Exit": "Fraaz Blue Warp",
    "Cactops Exit": "Cactops Blue Warp",
    "Vulcano Exit": "Vulcano Blue Warp",
    "Capbone Exit": "Desert Temple Bow of Light Room Blue Warp",
}

map_warp_redirects: dict[int, tuple[int, int, int]] = {
    0x3C: (0x3c, 1, 1),

}

@dataclass
class SceneData:
    scene: int
    name: str
    room_type: str
    map_id: int = 0

    def __bool__(self):
        return True

    def __str__(self):
        return f"{self.name} ({hex(self.scene)}, {self.map_id})"

SCENES: list[SceneData] = [
    SceneData(0x400, "Forest Realm", "train", 1),
    SceneData(0x500, "Snow Realm", "train", 2),
    SceneData(0x600, "Ocean Realm", "train", 3),
    SceneData(0x700, "Fire Realm", "train", 4),
    SceneData(0xA00, "Undersea Tracks", "train", 5),
    SceneData(0x4503, "Beedle", "train", 211),

    SceneData(0xB00, "Rocktite Tunnel", "train", 2),
    SceneData(0xC00, "Rocktite Tunnel", "train", 4),
    SceneData(0xD00, "Rocktite Tunnel", "train", 4),

    SceneData(0x2f00, "Outset", "overworld", 6),
    SceneData(0x2F0A, "Niko's House", "house", 121),
    SceneData(0x2F0C, "Mary's House", "house", 123),
    SceneData(0x2F0B, "Alfonzo's Workshop", "house", 122),

    SceneData(0x2A00, "Mayscore", "overworld", 7),
    SceneData(0x2A04, "Dovok's House", "house", 127),
    SceneData(0x2A03, "Morris' House", "house", 126),
    SceneData(0x2A02, "Wood's House", "house", 125),
    SceneData(0x2A05, "Uriko's Shop", "useful house", 124),
    SceneData(0x3800, "Mayscore Forest", "overworld", 8),

    SceneData(0x2900, "Castle Town", "overworld", 9),
    SceneData(0x290C, "Mona's House", "house", 130),
    SceneData(0x290E, "Lucia's House", "house", 131),
    SceneData(0x290A, "Shitate's Shop", "useful house", 129),
    SceneData(0x290D, "Milo's House", "house", 132),
    SceneData(0x290B, "Take 'em All On Lobby", "house", 133),

    SceneData(0x2800, "Hyrule Castle Courtyard", "Castle", 134),
    SceneData(0x2801, "Hyrule Castle 1F", "Castle", 135),
    SceneData(0x2803, "Hyrule Castle Infirmary", "Castle", 138),
    SceneData(0x2807, "Hyrule Castle Barracks", "Castle", 137),
    SceneData(0x2806, "Hyrule Castle Throne Room", "Castle", 139),
    SceneData(0x2802, "Hyrule Castle 2F", "Castle", 136),
    SceneData(0x2805, "Zelda's Room", "Castle", 140),
    SceneData(0x2804, "Hyrule Castle Backyard", "Castle", 141),
    SceneData(0x1800, "Tunnel to the Tower 1F", "useful cave", 142),
    SceneData(0x1801, "Tunnel to the Tower 2F", "useful cave", 143),
    SceneData(0x1802, "Tunnel to the Tower 3F", "useful cave", 144),

    SceneData(0x3000, "Woodland Sanctuary", "overworld", 10),
    SceneData(0x3001, "Gage's Sanctuary", "cave", 128),

    SceneData(0x3E00, "Rabbit Haven", "overworld", 11),

    SceneData(0x2B00, "Anouki Village", "overworld", 13),
    SceneData(0x2B05, "Yefu's House", "house", 149),
    SceneData(0x2B04, "Noko's House", "house", 150),
    SceneData(0x2B03, "Bulu's House", "house", 151),
    SceneData(0x2B02, "Kofu's House", "house", 154),
    SceneData(0x2B06, "Yeko's House", "house", 152),
    SceneData(0x2B01, "Honcho's House", "house", 153),
    SceneData(0x2B07, "Small Ice Puzzle Cave", "cave", 148),

    SceneData(0x3100, "Snowfall Sanctuary", "overworld", 14),
    SceneData(0x3101, "Head Statue Cave", "cave", 155),
    SceneData(0x3102, "Steem's Sanctuary", "cave", 156),
    SceneData(0x3103, "Snowfall Supermarket", "useful house", 157),

    SceneData(0x3500, "Icy Spring", "overworld", 16),
    SceneData(0x3501, "Ferrus' Trailer", "house", 159),

    SceneData(0x3600, "Bridge Worker's", "overworld", 15),
    SceneData(0x3601, "Kenzo's House", "house", 158),

    SceneData(0x3F0A, "Slippery Station", "overworld", 17),
    SceneData(0x3F06, "Skating Rink", "useful cave", 160),

    SceneData(0x3F00, "Snowdrift Station", "overworld", 18),
    SceneData(0x3F01, "Snowdrift Cave", "useful cave", 161),
    SceneData(0x3F02, "Octive Arena", "cave", 162),
    SceneData(0x3F03, "Frostflame Cave", "cave", 164),
    SceneData(0x3F04, "Small Skating Cave", "cave", 163),
    SceneData(0x3F05, "Big Ice Puzzle Cave", "cave", 165),

    SceneData(0x3700, "Trading Post", "overworld", 12),
    SceneData(0x370A, "Linebeck's Shop", "house", 146),
    SceneData(0x3701, "Like-Like Tunnel", "useful cave", 145),
    SceneData(0x3702, "Linebeck's Treasure Cave", "useful cave", 147),

    SceneData(0x2C00, "Papuzia Village", "overworld", 19),
    SceneData(0x2C01, "Fuku's House", "house", 170),
    SceneData(0x2C04, "Wise One's House", "house", 169),
    SceneData(0x2C03, "Orca's House", "house", 168),
    SceneData(0x2C02, "Kogane's Shop", "useful house", 167),
    SceneData(0x3900, "Papuzia Archipelago", "overworld", 20),

    SceneData(0x3200, "Island Sanctuary South", "overworld", 21),
    SceneData(0x3202, "Island Sanctuary North", "overworld", 22),
    SceneData(0x3201, "Crab Cave", "cave", 171),
    SceneData(0x3204, "Carben's Sanctuary", "cave", 172),

    SceneData(0x3A00, "Pirate Hideout", "overworld", 23),
    SceneData(0x3A01, "Treasure Cave", "cave", 166),
    SceneData(0x3B00, "Pirate Hangout", "cave", 210),

    SceneData(0x390A, "Lost at Sea Stations", "overworld", 24),
    SceneData(0x390B, "Lost at Sea Lobby", "useful cave", 114),
    SceneData(0x4202, "Lost at Sea 1", "useful cave", 115),
    SceneData(0x4203, "Lost at Sea 2", "useful cave", 116),
    SceneData(0x4204, "Lost at Sea 3", "useful cave", 117),
    SceneData(0x4205, "Lost at Sea 4", "useful cave", 118),
    SceneData(0x4206, "Lost at Sea 5", "useful cave", 119),
    SceneData(0x4207, "Lost at Sea 6", "useful cave", 120),

    SceneData(0x3400, "Dune Sanctuary", "overworld", 32),
    SceneData(0x3401, "Sandy Tunnel", "cave", 205),
    SceneData(0x3402, "Rael's Sanctuary", "cave", 206),

    SceneData(0x2E00, "Goron Village", "overworld", 25),
    SceneData(0x2D03, "Goron Field", "overworld", 26),
    SceneData(0x2D02, "Mountain Altar", "overworld", 195),
    SceneData(0x2E06, "Goron Shop", "useful house", 196),
    SceneData(0x2E0C, "Goron 3 Pots House", "house", 199),
    SceneData(0x2E0D, "Kofu's New House", "house", 197),
    SceneData(0x2E0E, "Goron 2 Pots House", "house", 201),
    SceneData(0x2E0A, "Goron Elder's House", "useful house", 198),
    SceneData(0x2E0B, "Mouldy Goron's House", "house", 200),
    SceneData(0x2E0F, "Lava Goron's House", "house", 202),
    SceneData(0x2E01, "Burning Tunnel", "useful cave", 203),
    SceneData(0x3300, "Valley Sanctuary", "overworld", 27),
    SceneData(0x3303, "Embrose's Sanctuary", "cave", 204),

    SceneData(0x3D00, "Dark Ore Mine", "overworld", 30),
    SceneData(0x3D01, "Dark Ore Mine Tunnels", "useful cave", 182),

    SceneData(0x4000, "Disorientation Station", "overworld", 29),
    SceneData(0x4001, "D1", "disorientation", 173),
    SceneData(0x4002, "D2", "disorientation", 174),
    SceneData(0x4003, "D3", "disorientation", 175),
    SceneData(0x4004, "D4", "disorientation", 176),
    SceneData(0x4005, "D5", "disorientation", 177),
    SceneData(0x4006, "D6", "disorientation", 178),
    SceneData(0x4007, "D7", "disorientation", 179),
    SceneData(0x4008, "D8", "disorientation", 180),
    SceneData(0x4009, "D9", "disorientation", 181),

    SceneData(0x4100, "Ends of the Earth", "overworld", 31),
    SceneData(0x4101, "EotE 1", "eote", 183),
    SceneData(0x4102, "EotE 2", "eote", 184),
    SceneData(0x4103, "EotE 3", "eote", 185),
    SceneData(0x4104, "EotE 4", "eote", 186),
    SceneData(0x4105, "EotE 5", "eote", 187),
    SceneData(0x4106, "EotE 6", "eote", 188),
    SceneData(0x4107, "EotE 7", "eote", 189),
    SceneData(0x4108, "EotE 8", "eote", 190),
    SceneData(0x4109, "EotE 9", "eote", 191),
    SceneData(0x410A, "EotE A", "eote", 192),
    SceneData(0x410B, "EotE B", "eote", 193),
    SceneData(0x410C, "EotE C", "eote", 194),

    SceneData(0x3c00, "Goron Target Range", "overworld", 28),
    SceneData(0x3c01, "Goron Target Range", "overworld", 28),
    SceneData(0xE00, "Goron Target Range", "train", 28),

    SceneData(0xF00, "Dark Realm", "train", 207),
    SceneData(0x1000, "Demon Train Fight", "train", 208),
    SceneData(0x10FF, "Demon Train Fight", "train", 208),
    SceneData(0x1100, "Demon Train Fight", "train", 208),
    SceneData(0x1200, "Demon Train Fight", "train", 208),
    SceneData(0x12FF, "Demon Train Fight", "train", 208),
    SceneData(0x2400, "Cole Fight", "train", 208),
    SceneData(0x2500, "Malladus Fight", "train", 208),
    SceneData(0x2600, "Malladus Fight", "train", 208),
    SceneData(0x2700, "Malladus Fight", "train", 208),

    SceneData(0x1400, "ToS Lobby", "tos", 33),
    SceneData(0x1401, "ToS Lobby", "tos", 33),
    SceneData(0x1700, "ToS Staircase", "tos", 34),
    SceneData(0x1500, "ToS Summit", "tos", 34),

    SceneData(0x1300, "ToS 1F", "tos", 73),
    SceneData(0x1301, "ToS 2F", "tos", 74),
    SceneData(0x1302, "ToS 3F", "tos", 76),
    SceneData(0x1328, "ToS 2F Secret", "tos", 75),

    SceneData(0x1303, "ToS 4F", "tos", 77),
    SceneData(0x1304, "ToS 5F", "tos", 78),
    SceneData(0x1305, "ToS 6F", "tos", 80),
    SceneData(0x1306, "ToS 7F", "tos", 81),
    SceneData(0x1329, "ToS 5F Secret", "tos", 79),

    SceneData(0x1307, "ToS 8F", "tos", 82),
    SceneData(0x1308, "ToS 9F", "tos", 85),
    SceneData(0x1309, "ToS 10F", "tos", 87),
    SceneData(0x130a, "ToS 11F", "tos", 88),
    SceneData(0x130b, "ToS 12F", "tos", 89),
    SceneData(0x132A, "ToS 8F S Secret", "tos", 84),
    SceneData(0x1315, "ToS 8F N Secret", "tos", 83),
    SceneData(0x1316, "ToS 9F Secret", "tos", 86),

    SceneData(0x130c, "ToS 13F", "tos", 90),
    SceneData(0x130d, "ToS 14F", "tos", 91),
    SceneData(0x130e, "ToS 15F", "tos", 92),
    SceneData(0x1310, "ToS 16F", "tos", 93),
    SceneData(0x130f, "ToS 17F", "tos", 95),
    SceneData(0x132B, "ToS 6F Secret", "tos", 94),

    SceneData(0x1311, "ToS 18F", "tos", 96),
    SceneData(0x1312, "ToS 19F", "tos", 97),
    SceneData(0x1313, "ToS 20F", "tos", 98),
    SceneData(0x1317, "ToS 21F", "tos", 99),
    SceneData(0x1318, "ToS 22F", "tos", 101),
    SceneData(0x1314, "ToS 23F", "tos", 102),
    SceneData(0x132E, "ToS 21F Secret", "tos", 100),
    SceneData(0x2300, "ToS Staven", "tos", 103),

    SceneData(0x131d, "ToS 31F", "tos", 104),
    SceneData(0x131e, "ToS 30F", "tos", 105),
    SceneData(0x131f, "ToS 29F", "tos", 106),
    SceneData(0x1320, "ToS 28F", "tos", 109),
    SceneData(0x1321, "ToS 27F", "tos", 110),
    SceneData(0x1322, "ToS 26F", "tos", 111),
    SceneData(0x1324, "ToS 25F", "tos", 112),
    SceneData(0x1323, "ToS 24F", "tos", 113),
    SceneData(0x132C, "ToS 29F Passage", "tos", 107),
    SceneData(0x132D, "ToS 30F Passage", "tos", 108),

    SceneData(0x190A, "Wooded Temple Lobby", "dungeon", 35),
    SceneData(0x1900, "Wooded Temple 1F", "dungeon", 36),
    SceneData(0x1901, "Wooded Temple 2F", "dungeon", 37),
    SceneData(0x1902, "Wooded Temple 3F", "dungeon", 38),
    SceneData(0x1903, "Wooded Temple 4F", "dungeon", 39),
    SceneData(0x1E00, "Stagnox", "boss", 40),

    SceneData(0x1A04, "Blizzard Temple Lobby", "dungeon", 41),
    SceneData(0x1A05, "Blizzard Temple 1F", "dungeon", 42),
    SceneData(0x1A00, "Blizzard Temple 1F", "dungeon", 42),
    SceneData(0x1A01, "Blizzard Temple B1", "dungeon", 43),
    SceneData(0x1A02, "Blizzard Temple 2F", "dungeon", 44),
    SceneData(0x1A03, "Blizzard Temple 3F", "dungeon", 45),
    SceneData(0x1F00, "Fraaz", "boss", 46),

    SceneData(0x1B0A, "Marine Temple Lobby", "dungeon", 47),
    SceneData(0x1B00, "Marine Temple 1F", "dungeon", 48),
    SceneData(0x1B01, "Marine Temple 2F", "dungeon", 49),
    SceneData(0x1B02, "Marine Temple 3F", "dungeon", 50),
    SceneData(0x1B03, "Marine Temple 4F", "dungeon", 51),
    SceneData(0x1B04, "Marine Temple 5F", "dungeon", 52),
    SceneData(0x1B05, "Marine Temple 6F", "dungeon", 53),
    SceneData(0x1B06, "Marine Temple 7F", "dungeon", 54),
    SceneData(0x1B07, "Marine Temple Stamp Room", "dungeon", 55),
    SceneData(0x2000, "Cactops", "boss", 56),

    SceneData(0x1C0A, "Mountain Temple Lobby", "dungeon", 57),
    SceneData(0x1C00, "Mountain Temple 1F", "dungeon", 58),
    SceneData(0x1C06, "Mountain Temple 2F", "dungeon", 59),
    SceneData(0x1C01, "Mountain Temple 2F", "dungeon", 59),
    SceneData(0x1C02, "Mountain Temple B1", "dungeon", 60),
    SceneData(0x1C03, "Mountain Temple B2", "dungeon", 61),
    SceneData(0x1C04, "Mountain Temple B3", "dungeon", 62),
    SceneData(0x1C05, "Mountain Temple B4", "dungeon", 63),
    SceneData(0x2100, "Vulcano", "boss", 64),

    SceneData(0x1D06, "Desert Temple Lobby", "dungeon", 65),
    SceneData(0x1D00, "Desert Temple 1F", "dungeon", 66),
    SceneData(0x1D01, "Desert Temple 2F", "dungeon", 67),
    SceneData(0x1D02, "Desert Temple 3F", "dungeon", 68),
    SceneData(0x1D03, "Desert Temple B1", "dungeon", 69),
    SceneData(0x1D04, "Desert Temple B2", "dungeon", 70),
    SceneData(0x2200, "Capbone", "boss", 71),
    SceneData(0x2201, "Capbone", "boss", 71),
    SceneData(0x1D05, "Desert Temple B4", "boss", 72),
]

scene_lookup: dict[int, SceneData] = {s.scene: s for s in SCENES}

DEAD_END_ENTRANCES: list[str] = [  # Used for extra entrance hints
    "Niko's House Exit",
    "Mary's House Exit",
    "Alfonzo's Workshop Exit",
    "Dovok's House Exit",
    "Morris' House Exit",
    "Wood's House Exit",
    "Uriko's Shop Exit",
    "Mayscore Forest South",
    "Mona's House Exit",
    "Lucia's House Exit",
    "Shitate's Shop Exit",
    "Milo's House Exit",
    "Take 'em all On Lobby Exit",
    "Hyrule Castle Infirmary Exit",
    "Hyrule Castle Barracks Exit",
    "Hyrule Castle Zelda's Room Exit",
    "Hyrule Castle Roof NW",
    "Tunnel to the Tower 3F Exit",
    "Gage's Sanctuary Exit",
    "Yefu's House Exit",
    "Noko's House Exit",
    "Bulu's House Exit",
    "Kofu's House Exit",
    "Yeko's House Exit",
    "Honcho's House Exit",
    "Small Ice Puzzle Cave Exit",
    "Steem's Sanctuary Exit",
    "Snowfall Supermarket Exit",
    "Ferrus' Trailer Exit",
    "Kenzo's House Exit",
    "Skating Rink Exit",
    "Octive Arena Exit",
    "Frostflame Cave Exit",
    "Small Skating Cave Exit",
    "Big Ice Puzzle Cave Exit",
    "Linebeck III's Shop Exit",
    "Linebeck's Treasure's Cave Exit",
    "Fuku's House Exit",
    "Wise One's House Exit",
    "Orca's House Exit",
    "Kogane's Shop Exit",
    "Papuzia Archipelago North",
    "Carben's Sanctuary Exit",
    "Treasure Cave Exit",
    "Lost at Sea Lobby Exit",
    "Rael's Sanctuary Exit",
    "Mountain Altar South",
    "Goron Shop Exit",
    "Goron 3 Pots House Exit",
    "Kofu's New House Exit",
    "Goron 2 Pots House Exit",
    "Mouldy Goron House Exit",
    "Lava Goron House Exit",
    "Embrose's Sanctuary Exit",
    "EotE 1 Upper Entrance",
    "EotE 4 Exit",
    "EotE 5 Upper Entrance",
    "EotE 8 Exit",
    "EotE 9 Upper Entrance",
    "EotE C Exit",
    "Rabbit Haven Board Train",
    "Goron Target Range Board Train",
    "ToS 31F Exit",
    "ToS 13F Exit",
    "ToS 8F Exit",
    "ToS 4F Exit",
    "Wooded Temple 2F SE Staircase",
    "Wooded Temple 1F NW Staircase",
    "Wooded Temple 3F W Staircase",
    "Stagnox Exit",
    "Blizzard Temple B1 SE Staircase",
    "Blizzard Temple 1F NE Staircase",
    "Blizzard Temple B1 SW Staircase",
    "Fraaz Exit",
    "Marine Temple Stamp Room Exit",
    "Marine Temple Switch Room Exit",
    "Marine Temple 3F South Staircase",
    "Marine Temple 6F SW Staircase",
    "Marine Temple 6F SE Staircase",
    "Cactops Exit",
    "Mountain Temple 2F SW Staircase",
    "Mountain Temple 2F Central Staircase",
    "Mountain Temple B2 North Staircase",
    "Mountain Temple B1 East Staircase",
    "Mountain Temple B2 West Staircase",
    "Mountain Temple B3 South Staircase",
    "Vulcano Exit",
    "Desert Temple 3F Staircase",
    "Capbone Exit",
]

map_object_identifiers = {
    0x1151AC: "Key Door",
    0x11527c: "Blue Door",
    0x1150d8: "Arena Door",
    0x1217b4: "Red Pattern Door",
    0x11535c: "Big Red Door",
    0x1379a8: "Big Door",
    0x157c14: "Bell Door",
    0x16019c: "Gem Door",
    0x12e060: "Boss Door",  # Bliz
    0x12e0d0: "Boss Door",  # ToS 3

    0x115ed0: "Staircase",
    0x162eac: "Entrance",
    0x1155e4: "Stairs",
    0x115dac: "Cracked Wall",
    0x115520: "Exit",

    0x1157dc: "Chest",
    0x115970: "Chest Spawner",
    0x14f62c: "Big Chest",
    0x14f6ac: "Big Chest Spawner",
    0x14f5ac: "Big Chest",
    0x155c70: "Sign",
    0x115bc4: "Tablet",
    0x178128: "Map Board",
    0x116084: "Stamp Stand",
    0x178260: "Song Statue",
    0x116134: "Gossip Stone",

    0x115b08: "Pot",
    0x155938: "Rock",
    0x115c20: "Chestnut",
    0x115728: "Bomb Flower",
    0x115f2c: "Cracked Brick",
    0x1650a8: "Tall Cracked Brick",

    0x115c9c: "Torch",
    0x115e08: "Bridge",
    0x341aec: "Sand Bridge",
    0x14ef4c: "Spikes",
    0x14f480: "Flames",
    0x14efb0: "Permanent Spikes",

    0x33ed6c: "Switch",
    0x1156cc: "Switch",  # Are all switches unique?
    0x122d30: "Rail Switch",
    0xb370c: "Pressure Pad",
    0x1211f4: "Sand Block Switch",

    0x14f234: "Eye",
    0x14f150: "Arrow Trap",
    0x116214: "Tongue Statue",
    0x1227d8: "Sword Statue",
    0x115e74: "Whip Log",
    0x14f1d8: "Windmill",

    0xb3774: "Divider",
    0x121198: "Sand Divider",
    0x177fb4: "Fence",
    0x162dac: "Pillar",
    0x163888: "Head Statue",
    0x155860: "Tree",
    0x1781e0: "Pillar", # MTT
0x14ee84: "Block", # MTT

    0x11565c: "Grass",
    0x155d50: "Long Grass",
    0x12f358: "Rails",
    0x178344: "Frozen Grass",
    0x178474: "Snow",
    0x1558d8: "Leaves",
    0x164f10: "Swap Pad",
    0x12f2f0: "Train Platform"
}

TOS_FLOOR_TO_SECTION: dict[int, int] = TOS_FLOOR_TO_SECTION_SAFE | TOS_FLOOR_SECTIONS_CANCEL_TEARS

#TREASURE_READ_LIST = {i: (0x1BA5AC + i * 4, 4, "Main RAM") for i in range(8)}
