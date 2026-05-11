from typing import NamedTuple, Optional

from .RamHandler import GrinchRamData, UpdateMethod
from BaseClasses import Item
from BaseClasses import (
    ItemClassification as IC,
)  # IC can be any name, saves having to type the whole word in code


class GrinchItemData(NamedTuple):
    item_group: list[str]  # arbitrary that can be whatever it can be, basically the field/property for item groups
    id: Optional[int]
    classification: IC
    update_ram_addr: Optional[list[GrinchRamData]]


class GrinchItem(Item):
    game: str = "The Grinch"

    # Tells server what item id it is
    @staticmethod
    def get_apid(id: int):
        # If you give me an input id, I will return the Grinch equivalent server/ap id
        base_id: int = 42069
        return base_id + id if id is not None else None

    def __init__(self, name: str, player: int, data: GrinchItemData):
        super(GrinchItem, self).__init__(name, data.classification, GrinchItem.get_apid(data.id), player)

        self.type = data.item_group
        self.item_id = data.id


# allows hinting of items via category
def get_item_names_per_category() -> dict[str, set[str]]:
    categories: dict[str, set[str]] = {}

    for name, data in ALL_ITEMS_TABLE.items():
        for group in data.item_group:  # iterate over each category
            categories.setdefault(group, set()).add(name)

    return categories


class grinch_items:
    class gadgets:
        BINOCULARS: str = "Binoculars"
        ROTTEN_EGG_LAUNCHER: str = "Rotten Egg Launcher"
        ROCKET_SPRING: str = "Rocket Spring"
        SLIME_SHOOTER: str = "Slime Shooter"
        OCTOPUS_CLIMBING_DEVICE: str = "Octopus Climbing Device"
        MARINE_MOBILE: str = "Marine Mobile"
        GRINCH_COPTER: str = "Grinch Copter"

    class keys:
        WHOVILLE: str = "Whoville Vacuum Tube"
        WHO_FOREST: str = "Who Forest Vacuum Tube"
        WHO_DUMP: str = "Who Dump Vacuum Tube"
        WHO_LAKE: str = "Who Lake Vacuum Tube"
        PROGRESSIVE_VACUUM_TUBE: str = "Progressive Vacuum Tube"
        SLEIGH_ROOM_KEY: str = "Sleigh Room Key"

    class sleigh_parts:
        EXHAUST_PIPES: str = "Exhaust Pipes"
        SKIS: str = "Skis"
        TIRES: str = "Tires"
        GPS: str = "GPS"
        TWIN_END_TUBA: str = "Twin-End Tuba"

    class moves:
        PANCAKE: str = "Pancake"
        BAD_BREATH: str = "Bad Breath"
        SEIZE: str = "Seize"
        MAX: str = "Max"
        SNEAK: str = "Sneak"

    class level_items:
        WV_WHO_CLOAK: str = "Who Cloak"
        WV_PAINT_BUCKET: str = "Painting Bucket"
        WV_HAMMER: str = "Hammer"
        WV_SCULPTING_TOOLS: str = "Sculpting Tools"
        WF_GLUE_BUCKET: str = "Glue Bucket"
        WF_CABLE_CAR_ACCESS_CARD: str = "Cable Car Access Card"
        WD_SCISSORS: str = "Scissors"
        WL_ROPE: str = "Rope"
        WL_HOOK: str = "Hook"
        WL_DRILL: str = "Drill"
        WL_SCOUT_CLOTHES: str = "Scout Clothes"

    class useful_items:
        HEART_OF_STONE: str = "Heart of Stone"

    class trap_items:
        DEPLETION_TRAP: str = "Depletion Trap"
        DUMP_IT_TO_CRUMPIT: str = "Dump it to Crumpit"
        WHO_SENT_ME_BACK: str = "Who sent me back?"
        DAMAGE_TRAP: str = "Damage Trap"
        ICE_TRAP: str = "Ice Trap"
        BONK_TRAP: str = "Bonk Trap"
        ELECTROCUTION_TRAP: str = "Electrocution Trap"
        BANANA_TRAP: str = "Banana Trap"
        BEE_TRAP: str = "Bee Trap"
        PUSH_TRAP: str = "Push Trap"

class grinch_categories:
    FILLER: str = "Filler"
    GADGETS: str = "Gadgets"
    HEALING_ITEMS: str = "Healing Items"
    MISSION_SPECIFIC_ITEMS: str = "Mission Specific Items"
    MOVES: str = "Moves"
    REQUIRED_ITEM: str = "Required Items"
    ROTTEN_EGG_BUNDLES: str = "Rotten Egg Bundles"
    SLEIGH_ROOM: str = "Sleigh Room Items"
    TRAPS: str = "Traps"
    USEFUL_ITEMS: str = "Useful Items"
    USEFUL_IC: str = "Useful"
    PROGRESSION_IC: str = "Progression"
    VACUUM_TUBES: str = "Vacuum Tubes"

def get_region_health(region_name: str):
    from .Regions import ALL_REGIONS_INFO
    return ALL_REGIONS_INFO[region_name].map_table_addr + 0x3C

def get_death_offset(region_name: str):
    from .Regions import  ALL_REGIONS_INFO
    return ALL_REGIONS_INFO[region_name].map_table_addr + 0x27

# Gadgets
# All gadgets require at least 4 different blueprints to be unlocked in the computer in Mount Crumpit.
GADGETS_TABLE: dict[str, GrinchItemData] = {
    grinch_items.gadgets.BINOCULARS: GrinchItemData(
        [
            grinch_categories.GADGETS,
            grinch_categories.USEFUL_IC,
        ],
        100,
        IC.useful,
        [
            GrinchRamData(0x0102B6, value=0x40),
            GrinchRamData(0x0102B7, value=0x41),
            GrinchRamData(0x0102B8, value=0x44),
            GrinchRamData(0x0102B9, value=0x45),
            GrinchRamData(0x0100BC, binary_bit_pos=0),
        ],
    ),
    grinch_items.gadgets.ROTTEN_EGG_LAUNCHER: GrinchItemData(
        [
            grinch_categories.GADGETS,
            grinch_categories.PROGRESSION_IC,
        ],
        101,
        IC.progression,
        [
            GrinchRamData(0x0102BA, value=0x40),
            GrinchRamData(0x0102BB, value=0x41),
            GrinchRamData(0x0102BC, value=0x44),
            GrinchRamData(0x0102BD, value=0x45),
            GrinchRamData(0x0100AC, binary_bit_pos=1),
            GrinchRamData(0x0100BC, binary_bit_pos=1),
        ],
    ),
    grinch_items.gadgets.ROCKET_SPRING: GrinchItemData(
        [
            grinch_categories.GADGETS,
            grinch_categories.PROGRESSION_IC,
        ],
        102,
        IC.progression,
        [
            GrinchRamData(0x0102BE, value=0x40),
            GrinchRamData(0x0102BF, value=0x41),
            GrinchRamData(0x0102C0, value=0x42),
            GrinchRamData(0x0102C1, value=0x44),
            GrinchRamData(0x0102C2, value=0x45),
            GrinchRamData(0x0102C3, value=0x46),
            GrinchRamData(0x0102C4, value=0x48),
            GrinchRamData(0x0102C5, value=0x49),
            GrinchRamData(0x0102C6, value=0x4A),
            GrinchRamData(0x0100AC, binary_bit_pos=2),
            GrinchRamData(0x0100BC, binary_bit_pos=2),
        ],
    ),
    grinch_items.gadgets.SLIME_SHOOTER: GrinchItemData(
        [
            grinch_categories.GADGETS,
            "Slime Gun",  # For canon --MarioSpore
            grinch_categories.PROGRESSION_IC,
        ],
        103,
        IC.progression,
        [
            GrinchRamData(0x0102C7, value=0x40),
            GrinchRamData(0x0102C8, value=0x41),
            GrinchRamData(0x0102C9, value=0x42),
            GrinchRamData(0x0102CA, value=0x44),
            GrinchRamData(0x0102CB, value=0x45),
            GrinchRamData(0x0102CC, value=0x46),
            GrinchRamData(0x0102CD, value=0x48),
            GrinchRamData(0x0102CE, value=0x49),
            GrinchRamData(0x0102CF, value=0x4A),
            GrinchRamData(0x0100AC, binary_bit_pos=0),
            GrinchRamData(0x0100BC, binary_bit_pos=3),
        ],
    ),
    grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE: GrinchItemData(
        [
            grinch_categories.GADGETS,
            grinch_categories.PROGRESSION_IC,
        ],
        104,
        IC.progression,
        [
            GrinchRamData(0x0102D0, value=0x40),
            GrinchRamData(0x0102D1, value=0x41),
            GrinchRamData(0x0102D2, value=0x42),
            GrinchRamData(0x0102D3, value=0x44),
            GrinchRamData(0x0102D4, value=0x45),
            GrinchRamData(0x0102D5, value=0x46),
            GrinchRamData(0x0102D6, value=0x48),
            GrinchRamData(0x0102D7, value=0x49),
            GrinchRamData(0x0102D8, value=0x4A),
            GrinchRamData(0x0100AC, binary_bit_pos=3),
            GrinchRamData(0x0100BC, binary_bit_pos=4),
        ],
    ),
    grinch_items.gadgets.MARINE_MOBILE: GrinchItemData(
        [
            grinch_categories.GADGETS,
            grinch_categories.PROGRESSION_IC,
        ],
        105,
        IC.progression,
        [
            GrinchRamData(0x0102D9, value=0x40),
            GrinchRamData(0x0102DA, value=0x41),
            GrinchRamData(0x0102DB, value=0x42),
            GrinchRamData(0x0102DC, value=0x43),
            GrinchRamData(0x0102DD, value=0x44),
            GrinchRamData(0x0102DE, value=0x45),
            GrinchRamData(0x0102DF, value=0x46),
            GrinchRamData(0x0102E0, value=0x47),
            GrinchRamData(0x0102E1, value=0x48),
            GrinchRamData(0x0102E2, value=0x49),
            GrinchRamData(0x0102E3, value=0x4A),
            GrinchRamData(0x0102E4, value=0x4B),
            GrinchRamData(0x0102E5, value=0x4C),
            GrinchRamData(0x0102E6, value=0x4D),
            GrinchRamData(0x0102E7, value=0x4E),
            GrinchRamData(0x0102E8, value=0x4F),
            GrinchRamData(0x0100BC, binary_bit_pos=5),
        ],
    ),
    grinch_items.gadgets.GRINCH_COPTER: GrinchItemData(
        [
            grinch_categories.GADGETS,
            grinch_categories.PROGRESSION_IC,
        ],
        106,
        IC.progression,
        [
            GrinchRamData(0x0102E9, value=0x40),
            GrinchRamData(0x0102EA, value=0x41),
            GrinchRamData(0x0102EB, value=0x42),
            GrinchRamData(0x0102EC, value=0x43),
            GrinchRamData(0x0102ED, value=0x44),
            GrinchRamData(0x0102EE, value=0x45),
            GrinchRamData(0x0102EF, value=0x46),
            GrinchRamData(0x0102F0, value=0x47),
            GrinchRamData(0x0102F1, value=0x48),
            GrinchRamData(0x0102F2, value=0x49),
            GrinchRamData(0x0102F3, value=0x4A),
            GrinchRamData(0x0102F4, value=0x4B),
            GrinchRamData(0x0102F5, value=0x4C),
            GrinchRamData(0x0102F6, value=0x4D),
            GrinchRamData(0x0102F7, value=0x4E),
            GrinchRamData(0x0102F8, value=0x4F),
            GrinchRamData(0x0100AC, binary_bit_pos=4),
            GrinchRamData(0x0100BC, binary_bit_pos=6),
        ],
    ),
}

# Mission Specific Items
MISSION_ITEMS_TABLE: dict[str, GrinchItemData] = {
    grinch_items.level_items.WV_WHO_CLOAK: GrinchItemData(
        [
            grinch_categories.MISSION_SPECIFIC_ITEMS,
            grinch_categories.USEFUL_ITEMS,
            grinch_categories.PROGRESSION_IC,
        ],
        200,
        IC.progression,
        [GrinchRamData(0x0101F9, binary_bit_pos=0)],
    ),
    grinch_items.level_items.WV_PAINT_BUCKET: GrinchItemData(
        [
            grinch_categories.MISSION_SPECIFIC_ITEMS,
            grinch_categories.USEFUL_ITEMS,
            grinch_categories.PROGRESSION_IC,
        ],
        201,
        IC.progression,
        [GrinchRamData(0x0101F9, binary_bit_pos=1)],
    ),
    grinch_items.level_items.WD_SCISSORS: GrinchItemData(
        [
            grinch_categories.MISSION_SPECIFIC_ITEMS,
            grinch_categories.USEFUL_ITEMS,
            grinch_categories.PROGRESSION_IC,
        ],
        202,
        IC.progression_deprioritized,
        [
            GrinchRamData(0x0101F9, binary_bit_pos=6),
            GrinchRamData(0x0100C2, binary_bit_pos=1),
        ],
    ),
    grinch_items.level_items.WF_GLUE_BUCKET: GrinchItemData(
        [
            grinch_categories.MISSION_SPECIFIC_ITEMS,
            grinch_categories.USEFUL_ITEMS,
            grinch_categories.PROGRESSION_IC,
        ],
        203,
        IC.progression_deprioritized,
        [GrinchRamData(0x0101F9, binary_bit_pos=4)],
    ),
    grinch_items.level_items.WF_CABLE_CAR_ACCESS_CARD: GrinchItemData(
        [
            grinch_categories.MISSION_SPECIFIC_ITEMS,
            grinch_categories.USEFUL_ITEMS,
            grinch_categories.PROGRESSION_IC,
        ],
        204,
        IC.progression,
        [GrinchRamData(0x0101F9, binary_bit_pos=5)],
    ),
    grinch_items.level_items.WL_DRILL: GrinchItemData(
        [
            grinch_categories.MISSION_SPECIFIC_ITEMS,
            grinch_categories.USEFUL_ITEMS,
            grinch_categories.PROGRESSION_IC,
        ],
        205,
        IC.progression,
        [GrinchRamData(0x0101FA, binary_bit_pos=2)],
    ),
    grinch_items.level_items.WL_ROPE: GrinchItemData(
        [
            grinch_categories.MISSION_SPECIFIC_ITEMS,
            grinch_categories.USEFUL_ITEMS,
            grinch_categories.PROGRESSION_IC,
        ],
        206,
        IC.progression_deprioritized,
        [GrinchRamData(0x0101FA, binary_bit_pos=1)],
    ),
    grinch_items.level_items.WL_HOOK: GrinchItemData(
        [
            grinch_categories.MISSION_SPECIFIC_ITEMS,
            grinch_categories.USEFUL_ITEMS,
            grinch_categories.PROGRESSION_IC,
        ],
        207,
        IC.progression_deprioritized,
        [GrinchRamData(0x0101FA, binary_bit_pos=0)],
    ),
    grinch_items.level_items.WV_SCULPTING_TOOLS: GrinchItemData(
        [
            grinch_categories.MISSION_SPECIFIC_ITEMS,
            grinch_categories.USEFUL_ITEMS,
            grinch_categories.PROGRESSION_IC,
        ],
        208,
        IC.progression_deprioritized,
        [GrinchRamData(0x0101F9, binary_bit_pos=2)],
    ),
    grinch_items.level_items.WV_HAMMER: GrinchItemData(
        [
            grinch_categories.MISSION_SPECIFIC_ITEMS,
            grinch_categories.USEFUL_ITEMS,
            grinch_categories.PROGRESSION_IC,

        ],
        209,
        IC.progression_deprioritized,
        [GrinchRamData(0x0101F9, binary_bit_pos=3)],
    ),
    grinch_items.level_items.WL_SCOUT_CLOTHES: GrinchItemData(
        [
            grinch_categories.MISSION_SPECIFIC_ITEMS,
            grinch_categories.USEFUL_ITEMS,
            grinch_categories.PROGRESSION_IC,
        ],
        210,
        IC.progression,
        [GrinchRamData(0x0101F9, binary_bit_pos=7)],
         # GrinchRamData(0x0100E3, value=5)], # Allows removal of pirate in cave when doing squashing all gifts
    ),
}

# Sleigh Parts
SLEIGH_TABLE: dict[str, GrinchItemData] = {
    grinch_items.keys.SLEIGH_ROOM_KEY: GrinchItemData(
        [
            grinch_categories.SLEIGH_ROOM,
            grinch_categories.REQUIRED_ITEM,
            grinch_categories.PROGRESSION_IC,
        ],
        410,
        IC.progression_skip_balancing,
        [
            GrinchRamData(0x010200, binary_bit_pos=6),
            GrinchRamData(0x0100AA, binary_bit_pos=5),
        ],
    ),
    grinch_items.sleigh_parts.EXHAUST_PIPES: GrinchItemData(
        [
            grinch_categories.SLEIGH_ROOM,
            grinch_categories.REQUIRED_ITEM,
            grinch_categories.PROGRESSION_IC,
        ],
        411,
        IC.progression_skip_balancing,
        [
            GrinchRamData(0x0101FB, binary_bit_pos=2)],
    ),
    grinch_items.sleigh_parts.GPS: GrinchItemData(
        [
            grinch_categories.SLEIGH_ROOM,
            grinch_categories.FILLER,
        ],
        412,
        IC.filler,
        [
            GrinchRamData(0x0101FB, binary_bit_pos=5)],
    ),
    grinch_items.sleigh_parts.TIRES: GrinchItemData(
        [
            grinch_categories.SLEIGH_ROOM,
            grinch_categories.REQUIRED_ITEM,
            grinch_categories.PROGRESSION_IC,
        ],
        413,
        IC.progression_skip_balancing,
        [
            GrinchRamData(0x0101FB, binary_bit_pos=4)],
    ),
    grinch_items.sleigh_parts.SKIS: GrinchItemData(
        [
            grinch_categories.SLEIGH_ROOM,
            grinch_categories.REQUIRED_ITEM,
            grinch_categories.PROGRESSION_IC,
        ],
        414,
        IC.progression_skip_balancing,
        [
            GrinchRamData(0x0101FB, binary_bit_pos=3)],
    ),
    grinch_items.sleigh_parts.TWIN_END_TUBA: GrinchItemData(
        [
            grinch_categories.SLEIGH_ROOM,
            grinch_categories.REQUIRED_ITEM,
            grinch_categories.PROGRESSION_IC,
        ],
        415,
        IC.progression_skip_balancing,
        [
            GrinchRamData(0x0101FB, binary_bit_pos=6)],
    ),
}

# Access Keys
KEYS_TABLE: dict[str, GrinchItemData] = {
    grinch_items.keys.WHOVILLE: GrinchItemData(
        [
            grinch_categories.VACUUM_TUBES,
            grinch_categories.PROGRESSION_IC,
        ],
        400,
        IC.progression,
        [GrinchRamData(0x010200, binary_bit_pos=1)],
    ),
    grinch_items.keys.WHO_FOREST: GrinchItemData(
        [
            grinch_categories.VACUUM_TUBES,
            grinch_categories.PROGRESSION_IC,
        ],
        401,
        IC.progression,
        [GrinchRamData(0x0100AA, binary_bit_pos=2)],
    ),
    grinch_items.keys.WHO_DUMP: GrinchItemData(
        [
            grinch_categories.VACUUM_TUBES,
            grinch_categories.PROGRESSION_IC,
        ],
        402,
        IC.progression,
        [GrinchRamData(0x0100AA, binary_bit_pos=3)],
    ),
    grinch_items.keys.WHO_LAKE: GrinchItemData(
        [
            grinch_categories.VACUUM_TUBES,
            grinch_categories.PROGRESSION_IC,
        ],
        403,
        IC.progression,
        [GrinchRamData(0x0100AA, binary_bit_pos=4)],
    ),
    grinch_items.keys.PROGRESSIVE_VACUUM_TUBE: GrinchItemData(
        [
            grinch_categories.VACUUM_TUBES,
            grinch_categories.PROGRESSION_IC,
        ],
        404,
        IC.progression,
        [GrinchRamData(0x010200, binary_bit_pos=1),
        GrinchRamData(0x0100AA, binary_bit_pos=2),
        GrinchRamData(0x0100AA, binary_bit_pos=3),
        GrinchRamData(0x0100AA, binary_bit_pos=4)],
    ),
}


# Supadow
# SUPADOW_TABLE: dict[str. GrinchItemData] = {
# "Progressive Vacuum Tube": GrinchItemData(["Vacuum Tubes"], 404, IC.progression,
#     [GrinchRamData()]),
# "Spin N' Win Door Unlock": GrinchItemData(["Supadow Door Unlocks"], 405, IC.progression,
#     [GrinchRamData()]),
# "Dankamania Door Unlock": GrinchItemData(["Supadow Door Unlocks"], 406, IC.progression,
#     [GrinchRamData()]),
# "The Copter Race Contest Door Unlock": GrinchItemData("Supadow Door Unlocks", 407, IC.progression,
#     [GrinchRamData()]),
# "Progressive Supadow Door Unlock": GrinchItemData("Supadow Door Unlocks", 408, IC.progression,
#     [GrinchRamData()]),
# "Bike Race Access": GrinchItemData(["Supadow Door Unlocks", 409, IC.progression,
#     [GrinchRamData()])
# }

# Misc Items
MISC_ITEMS_TABLE: dict[str, GrinchItemData] = {
    # This item may not function properly if you receive it during a loading screen or in Mount Crumpit
    # "Fully Healed Grinch": GrinchItemData(["Health Items", "Filler"], 500, IC.filler,
    #     [GrinchRamData(0x0E8FDC, value=120)]),
    "5 Rotten Eggs": GrinchItemData(
        [
            grinch_categories.ROTTEN_EGG_BUNDLES,
            grinch_categories.FILLER,
        ],
        502,
        IC.filler,
        [
            GrinchRamData(
                0x010058,
                value=5,
                update_method=UpdateMethod.ADD,
                max_count=200,
                byte_size=2,
            )
        ],
    ),
    "10 Rotten Eggs": GrinchItemData(
        [
            grinch_categories.ROTTEN_EGG_BUNDLES,
            grinch_categories.FILLER,
        ],
        503,
        IC.filler,
        [
            GrinchRamData(
                0x010058,
                value=10,
                update_method=UpdateMethod.ADD,
                max_count=200,
                byte_size=2,
            )
        ],
    ),
    "20 Rotten Eggs": GrinchItemData(
        [
            grinch_categories.ROTTEN_EGG_BUNDLES,
            grinch_categories.FILLER,
        ],
        504,
        IC.filler,
        [
            GrinchRamData(
                0x010058,
                value=20,
                update_method=UpdateMethod.ADD,
                max_count=200,
                byte_size=2,
            )
        ],
    ),
    "Present": GrinchItemData(
        [
            grinch_categories.FILLER,
        ],
        505,
        IC.filler,
        [
            # GrinchRamData(get_region_health("Mount Crumpit"),value=10,update_method=UpdateMethod.ADD,max_count=255,
            #               byte_size=1,),
            # GrinchRamData(get_region_health("Whoville"),value=10,update_method=UpdateMethod.ADD,max_count=255,
            #               byte_size=1,),
            # GrinchRamData(get_region_health("Post Office"),value=10,update_method=UpdateMethod.ADD,max_count=255,
            #               byte_size=1,),
            # GrinchRamData(get_region_health("City Hall"), value=10, update_method=UpdateMethod.ADD, max_count=255,
            #               byte_size=1, ),
            # GrinchRamData(get_region_health("Clock Tower"), value=10, update_method=UpdateMethod.ADD, max_count=255,
            #               byte_size=1, ),
            # GrinchRamData(get_region_health("Who Forest"), value=10, update_method=UpdateMethod.ADD, max_count=255,
            #               byte_size=1, ),
            # GrinchRamData(get_region_health("Ski Resort"), value=10, update_method=UpdateMethod.ADD, max_count=255,
            #               byte_size=1, ),
            # GrinchRamData(get_region_health("Civic Center"), value=10, update_method=UpdateMethod.ADD, max_count=255,
            #               byte_size=1, ),
            # GrinchRamData(get_region_health("Who Dump"), value=10, update_method=UpdateMethod.ADD, max_count=255,
            #               byte_size=1, ),
            # GrinchRamData(get_region_health("Minefield"), value=10, update_method=UpdateMethod.ADD, max_count=255,
            #               byte_size=1, ),
            # GrinchRamData(get_region_health("Power Plant"), value=10, update_method=UpdateMethod.ADD, max_count=255,
            #               byte_size=1, ),
            # GrinchRamData(get_region_health("Generator Building"), value=10, update_method=UpdateMethod.ADD, max_count=255,
            #               byte_size=1, ),
            # GrinchRamData(get_region_health("Who Lake"), value=10, update_method=UpdateMethod.ADD, max_count=255,
            #               byte_size=1, ),
            # GrinchRamData(get_region_health("Scout's Hut"), value=10, update_method=UpdateMethod.ADD, max_count=255,
            #               byte_size=1, ),
            # GrinchRamData(get_region_health("North Shore"), value=10, update_method=UpdateMethod.ADD, max_count=255,
            #               byte_size=1, ),
            # GrinchRamData(get_region_health("Mayor's Villa"), value=10, update_method=UpdateMethod.ADD, max_count=255,
            #               byte_size=1, ),
            # GrinchRamData(get_region_health("Submarine World"), value=10, update_method=UpdateMethod.ADD, max_count=255,
            #               byte_size=1, ),
        ],
    ),
}

USEFUL_ITEMS_TABLE: dict[str, GrinchItemData] = {
    grinch_items.useful_items.HEART_OF_STONE: GrinchItemData(
        [
            grinch_categories.USEFUL_IC,
            grinch_categories.HEALING_ITEMS,
        ],
        501,
        IC.useful,
        [
            GrinchRamData(
                0x0100ED,
                value=1,
                update_method=UpdateMethod.ADD,
                max_count=4,
            )
        ],
    )
}

# Movesets
MOVES_TABLE: dict[str, GrinchItemData] = {
    grinch_items.moves.BAD_BREATH: GrinchItemData(
        [
            grinch_categories.MOVES,
            grinch_categories.PROGRESSION_IC,
        ],
        700,
        IC.progression,
        [
            GrinchRamData(0x0100BB, binary_bit_pos=0),
        ],
    ),
    grinch_items.moves.PANCAKE: GrinchItemData(
        [
            grinch_categories.MOVES,
            grinch_categories.PROGRESSION_IC,
        ],
        701,
        IC.progression,
        [
            GrinchRamData(0x0100BB, binary_bit_pos=1),
        ],
    ),
    grinch_items.moves.SEIZE: GrinchItemData(
        [
            grinch_categories.MOVES,
            grinch_categories.PROGRESSION_IC,
        ],
        702,
        IC.progression,
        [
            GrinchRamData(0x0100BB, binary_bit_pos=2),
        ],
    ),
    grinch_items.moves.MAX: GrinchItemData(
        [
            grinch_categories.MOVES,
            grinch_categories.PROGRESSION_IC,
        ],
        703,
        IC.progression,
        [
            GrinchRamData(0x0100BB, binary_bit_pos=3),
            GrinchRamData(0x0100BB, binary_bit_pos=5),
        ],
    ),
    grinch_items.moves.SNEAK: GrinchItemData(
        [
            grinch_categories.MOVES,
            grinch_categories.PROGRESSION_IC,
        ],
        704,
        IC.progression,
        [
            GrinchRamData(0x0100BB, binary_bit_pos=4),
        ],
    ),
}

# Double star combines all dictionaries from each individual list together
TRAPS_TABLE: dict[str, GrinchItemData] = {
    # alias to Slowness Trap for traplink
    # "Tip Toe Trap": GrinchItemData(["Traps"], 603, IC.trap, [GrinchRamData()]),
    # This item may not function properly if you receive it during a loading screen or in Mount Crumpit
    grinch_items.trap_items.BANANA_TRAP: GrinchItemData(
        [grinch_categories.TRAPS],
        600,
        IC.trap,
        [
            GrinchRamData(get_death_offset("Whoville"), value=40, byte_size=1, ),
            GrinchRamData(get_death_offset("City Hall"), value=40, byte_size=1, ),
            GrinchRamData(get_death_offset("Who Forest"), value=40, byte_size=1, ),
            GrinchRamData(get_death_offset("Ski Resort"), value=40, byte_size=1, ),
            GrinchRamData(get_death_offset("Civic Center"), value=40, byte_size=1, ),
            GrinchRamData(get_death_offset("Who Dump"), value=40, byte_size=1, ),
            GrinchRamData(get_death_offset("Minefield"), value=40, byte_size=1, ),
            GrinchRamData(get_death_offset("Power Plant"), value=40, byte_size=1, ),
            GrinchRamData(get_death_offset("Generator Building"), value=40,  byte_size=1, ),
            GrinchRamData(get_death_offset("Who Lake"), value=40, byte_size=1, ),
            GrinchRamData(get_death_offset("Scout's Hut"), value=40, byte_size=1, ),
            GrinchRamData(get_death_offset("North Shore"), value=40, byte_size=1, ),
            GrinchRamData(get_death_offset("Mayor's Villa"), value=40, byte_size=1, ),
        ],
    ),
    # alias to Ice Trap for traplink
    grinch_items.trap_items.PUSH_TRAP: GrinchItemData(
        [grinch_categories.TRAPS],
        601,
        IC.trap,
        [
            GrinchRamData(get_death_offset("Who Forest"), value=40, byte_size=1, ),
            GrinchRamData(get_death_offset("Ski Resort"), value=40, byte_size=1, ),
            GrinchRamData(get_death_offset("Civic Center"), value=40, byte_size=1, ),
            GrinchRamData(get_death_offset("Who Dump"), value=40, byte_size=1, ),
            GrinchRamData(get_death_offset("Submarine World"), value=40, byte_size=1, ),
            GrinchRamData(get_region_health("Who Forest"), value=10, update_method=UpdateMethod.SUBTRACT, max_count=255,
                          byte_size=1, ),
            GrinchRamData(get_region_health("Ski Resort"), value=10, update_method=UpdateMethod.SUBTRACT, max_count=255,
                          byte_size=1, ),
            GrinchRamData(get_region_health("Civic Center"), value=10, update_method=UpdateMethod.SUBTRACT, max_count=255,
                          byte_size=1, ),
            GrinchRamData(get_region_health("Who Dump"), value=10, update_method=UpdateMethod.SUBTRACT, max_count=255,
                          byte_size=1, ),
            GrinchRamData(get_region_health("Submarine World"), value=5, update_method=UpdateMethod.SUBTRACT,max_count=255,
                          byte_size=1, ),
        ],
    ),
    grinch_items.trap_items.ICE_TRAP: GrinchItemData(
        [grinch_categories.TRAPS],
        602,
        IC.trap,
        [
            GrinchRamData(get_death_offset("Whoville"), value=40, byte_size=1, ),
            GrinchRamData(get_death_offset("Ski Resort"), value=40, byte_size=1, ),
            GrinchRamData(get_death_offset("Civic Center"), value=40, byte_size=1, ),
        ],
    ),
    grinch_items.trap_items.BEE_TRAP: GrinchItemData(
        [grinch_categories.TRAPS],
        603,
        IC.trap,
        [
            GrinchRamData(get_death_offset("Who Lake"), value=40, byte_size=1, ),
        ],
    ),
    grinch_items.trap_items.ELECTROCUTION_TRAP: GrinchItemData(
        [grinch_categories.TRAPS],
        604,
        IC.trap,
        [
            GrinchRamData(get_death_offset("Who Dump"), value=40, byte_size=1, ),
            GrinchRamData(get_death_offset("Minefield"), value=40, byte_size=1, ),
            GrinchRamData(get_death_offset("Power Plant"), value=40, byte_size=1, ),
            GrinchRamData(get_death_offset("Generator Building"), value=40, byte_size=1, ),
            GrinchRamData(get_region_health("Who Dump"), value=10, update_method=UpdateMethod.SUBTRACT, max_count=255,
                          byte_size=1, ),
            GrinchRamData(get_region_health("Minefield"), value=10, update_method=UpdateMethod.SUBTRACT, max_count=255,
                          byte_size=1, ),
            GrinchRamData(get_region_health("Power Plant"), value=10, update_method=UpdateMethod.SUBTRACT, max_count=255,
                          byte_size=1, ),
            GrinchRamData(get_region_health("Generator Building"), value=10, update_method=UpdateMethod.SUBTRACT,max_count=255,
                          byte_size=1, ),
        ],
    ),
    # alias to Exhaustion Trap
    grinch_items.trap_items.DAMAGE_TRAP: GrinchItemData(
        [grinch_categories.TRAPS],
        605,
        IC.trap,
        [
            GrinchRamData(get_death_offset("Whoville"), value=40, byte_size=1, ),
            GrinchRamData(get_death_offset("City Hall"), value=40, byte_size=1, ),
            GrinchRamData(get_death_offset("Who Forest"), value=40, byte_size=1, ),
            GrinchRamData(get_death_offset("Ski Resort"), value=40, byte_size=1, ),
            GrinchRamData(get_death_offset("Civic Center"), value=40, byte_size=1, ),
            GrinchRamData(get_death_offset("Who Dump"), value=40, byte_size=1, ),
            GrinchRamData(get_death_offset("Minefield"), value=40, byte_size=1, ),
            GrinchRamData(get_death_offset("Power Plant"), value=40, byte_size=1, ),
            GrinchRamData(get_death_offset("Generator Building"), value=40, byte_size=1, ),
            GrinchRamData(get_death_offset("Who Lake"), value=40, byte_size=1, ),
            GrinchRamData(get_death_offset("Scout's Hut"), value=40, byte_size=1, ),
            GrinchRamData(get_death_offset("North Shore"), value=40, byte_size=1, ),
            GrinchRamData(get_death_offset("Mayor's Villa"), value=40, byte_size=1, ),
            GrinchRamData(get_death_offset("Submarine World"), value=40, byte_size=1, ),
            GrinchRamData(get_region_health("Whoville"), value=8, update_method=UpdateMethod.SUBTRACT, max_count=255,
                          byte_size=1, ),
            GrinchRamData(get_region_health("City Hall"), value=5, update_method=UpdateMethod.SUBTRACT, max_count=255,
                          byte_size=1, ),
            GrinchRamData(get_region_health("Who Forest"), value=10, update_method=UpdateMethod.SUBTRACT, max_count=255,
                          byte_size=1, ),
            GrinchRamData(get_region_health("Ski Resort"), value=8, update_method=UpdateMethod.SUBTRACT, max_count=255,
                          byte_size=1, ),
            GrinchRamData(get_region_health("Civic Center"), value=8, update_method=UpdateMethod.SUBTRACT, max_count=255,
                          byte_size=1, ),
            GrinchRamData(get_region_health("Who Dump"), value=8, update_method=UpdateMethod.SUBTRACT, max_count=255,
                          byte_size=1, ),
            GrinchRamData(get_region_health("Minefield"), value=8, update_method=UpdateMethod.SUBTRACT, max_count=255,
                          byte_size=1, ),
            GrinchRamData(get_region_health("Power Plant"), value=8, update_method=UpdateMethod.SUBTRACT, max_count=255,
                          byte_size=1, ),
            GrinchRamData(get_region_health("Generator Building"), value=8, update_method=UpdateMethod.SUBTRACT,max_count=255,
                          byte_size=1, ),
            GrinchRamData(get_region_health("Who Lake"), value=8, update_method=UpdateMethod.SUBTRACT, max_count=255,
                          byte_size=1, ),
            GrinchRamData(get_region_health("Scout's Hut"), value=10, update_method=UpdateMethod.SUBTRACT, max_count=255,
                          byte_size=1, ),
            GrinchRamData(get_region_health("North Shore"), value=8, update_method=UpdateMethod.SUBTRACT, max_count=255,
                          byte_size=1, ),
            GrinchRamData(get_region_health("Mayor's Villa"), value=8, update_method=UpdateMethod.SUBTRACT, max_count=255,
                          byte_size=1, ),
            GrinchRamData(get_region_health("Submarine World"), value=5, update_method=UpdateMethod.SUBTRACT,max_count=255,
                          byte_size=1, ),
        ],
    ),
    grinch_items.trap_items.DEPLETION_TRAP: GrinchItemData(
        [grinch_categories.TRAPS],
        606,
        IC.trap,
        [GrinchRamData(0x010058, value=1, byte_size=2)],
    ),
    grinch_items.trap_items.DUMP_IT_TO_CRUMPIT: GrinchItemData(
        [grinch_categories.TRAPS],
        607,
        IC.trap,  # Alias to Home Trap for traplink
        [
            GrinchRamData(0x010000, value=0x05),
            GrinchRamData(0x0101FF, binary_bit_pos=0),
            GrinchRamData(0x0100B4, value=0),
            GrinchRamData(0x08FB94, value=1),
            GrinchRamData(0x010111, value=0),
            GrinchRamData(0x01010D, value=1),
            GrinchRamData(0x0100B3, value=0),
        ],
    ),
    # alias to Spring Trap for traplink
    # "Rocket Spring Trap": GrinchItemData(["Traps"], 607, IC.trap, [GrinchRamData()]),
    # alias to Home Trap for traplink
    grinch_items.trap_items.WHO_SENT_ME_BACK: GrinchItemData(
        [grinch_categories.TRAPS],
        608,
        IC.trap,
        [
            GrinchRamData(0x08FB94, value=1),
            GrinchRamData(0x010111, value=0),
            GrinchRamData(0x0100B3, value=0),
        ],
    ),
    grinch_items.trap_items.BONK_TRAP: GrinchItemData(
        [grinch_categories.TRAPS],
        609,
        IC.trap,
        [
            GrinchRamData(get_region_health("Whoville"), value=5, update_method=UpdateMethod.SUBTRACT, max_count=255,
                          byte_size=1, ),
            GrinchRamData(get_region_health("City Hall"), value=5, update_method=UpdateMethod.SUBTRACT, max_count=255,
                          byte_size=1, ),
            GrinchRamData(get_region_health("Who Forest"), value=5, update_method=UpdateMethod.SUBTRACT, max_count=255,
                          byte_size=1, ),
            GrinchRamData(get_region_health("Ski Resort"), value=5, update_method=UpdateMethod.SUBTRACT, max_count=255,
                          byte_size=1, ),
            GrinchRamData(get_region_health("Civic Center"), value=5, update_method=UpdateMethod.SUBTRACT,
                          max_count=255,
                          byte_size=1, ),
            GrinchRamData(get_region_health("Who Dump"), value=5, update_method=UpdateMethod.SUBTRACT, max_count=255,
                          byte_size=1, ),
            GrinchRamData(get_region_health("Minefield"), value=5, update_method=UpdateMethod.SUBTRACT, max_count=255,
                          byte_size=1, ),
            GrinchRamData(get_region_health("Power Plant"), value=5, update_method=UpdateMethod.SUBTRACT, max_count=255,
                          byte_size=1, ),
            GrinchRamData(get_region_health("Generator Building"), value=5, update_method=UpdateMethod.SUBTRACT,
                          max_count=255,
                          byte_size=1, ),
            GrinchRamData(get_region_health("Who Lake"), value=5, update_method=UpdateMethod.SUBTRACT, max_count=255,
                          byte_size=1, ),
            GrinchRamData(get_region_health("Scout's Hut"), value=5, update_method=UpdateMethod.SUBTRACT,
                          max_count=255,
                          byte_size=1, ),
            GrinchRamData(get_region_health("North Shore"), value=5, update_method=UpdateMethod.SUBTRACT, max_count=255,
                          byte_size=1, ),
            GrinchRamData(get_region_health("Mayor's Villa"), value=5, update_method=UpdateMethod.SUBTRACT,
                          max_count=255,
                          byte_size=1, ),
            GrinchRamData(get_region_health("Submarine World"), value=5, update_method=UpdateMethod.SUBTRACT,
                          max_count=255,
                          byte_size=1, ),
        ],
    ),
    # "Cutscene Trap": GrinchItemData(["Traps"], 609, IC.trap, [GrinchRamData()]),
    # "No Vac Trap": GrinchItemData(["Traps"], 610, IC.trap, [GrinchRamData(0x0102DA, value=0]),
    # "Invisible Trap": GrinchItemData(["Traps"], 611, IC.trap, [GrinchRamData(0x0102DA, value=0, byte_size=4)])
    # "Child Trap": GrinchItemData(["Traps"], 612, IC.trap,[GrinchRamData()])
    # "Disable Jump Trap": GrinchItemData(["Traps"], 613, IC.trap,[GrinchRamData(0x010026, binary_bit_pos=6)])
}
ALL_ITEMS_TABLE: dict[str, GrinchItemData] = {
    **GADGETS_TABLE,
    **MISSION_ITEMS_TABLE,
    **KEYS_TABLE,
    **MISC_ITEMS_TABLE,
    **TRAPS_TABLE,
    **USEFUL_ITEMS_TABLE,
    **SLEIGH_TABLE,
    **MOVES_TABLE,
    # **SUPADOW_TABLE,
}

def grinch_items_to_id() -> dict[str, int]:
    item_mappings: dict[str, int] = {}
    for ItemName, ItemData in ALL_ITEMS_TABLE.items():
        item_mappings.update({ItemName: GrinchItem.get_apid(ItemData.id)})
    return item_mappings
