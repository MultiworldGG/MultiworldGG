from typing import Optional

from .RamHandler import GrinchRamData
from BaseClasses import Location, Region


class GrinchLocationData:
    region: str
    location_group: Optional[list[str]]
    id: Optional[int]
    update_ram_addr: list[GrinchRamData]
    reset_addr: Optional[list[GrinchRamData]] = None  # Addresses to update once we find the item
    basic_logic: list[list[str]]
    advanced_logic: Optional[list[list[str]]]

    def __init__(
        self,
        region: str,
        location_group: Optional[list[str]] = None,
        id: Optional[int] = None,
        update_ram_addr: list[GrinchRamData] = [],
        reset_addr: Optional[list[GrinchRamData]] = None,
    ):
        self.region = region

        if location_group:
            self.location_group = location_group

        if id:
            self.id = id
        else:
            raise ValueError(f"id is required on GrinchLocationData")

        if update_ram_addr:
            self.update_ram_addr = update_ram_addr
        else:
            raise ValueError(f"update_ram_addr is required on GrinchLocationData")

        if reset_addr:
            self.reset_addr = reset_addr


class GrinchLocation(Location):
    game: str = "The Grinch"

    @staticmethod
    def get_apid(id: int):
        base_id: int = 42069
        return base_id + id if id is not None else None

    def __init__(
        self,
        player: int,
        name: str,
        parent: Region,
        data: GrinchLocationData,
    ):
        address = None if data.id is None else GrinchLocation.get_apid(data.id)
        super(GrinchLocation, self).__init__(player, name, address=address, parent=parent)

        self.code = data.id
        self.region = data.region
        self.type = data.location_group


def get_location_names_per_category() -> dict[str, set[str]]:
    categories: dict[str, set[str]] = {}

    for name, data in grinch_locations.items():
        if data.location_group is None:
            continue

        for group in data.location_group:  # iterate over each category
            categories.setdefault(group, set()).add(name)

    return categories



grinch_locations = {
    # Going to use current map id as indicator whether or not you visited a location
    # Visitsanity
    "WV - First Visit": GrinchLocationData(
        "Whoville",
        ["Visitsanity", "Whoville"],
        100,
        [
            GrinchRamData(0x010000, value=0x07),
            # GrinchRamData(0x010212, binary_bit_pos=0),
        ],

    ),
    "WV - Post Office - First Visit": GrinchLocationData(
        "Post Office",
        ["Visitsanity", "Whoville", "Post Office"],
        101,
        [GrinchRamData(0x010000, value=0x0A)],
    ),
    "WV - City Hall - First Visit": GrinchLocationData(
        "City Hall",
        ["Visitsanity", "Whoville", "City Hall"],
        102,
        [GrinchRamData(0x010000, value=0x08)],
    ),
    "WV - Clock Tower - First Visit": GrinchLocationData(
        "Clock Tower",
        ["Visitsanity", "Whoville", "Clock Tower"],
        103,
        [GrinchRamData(0x010000, value=0x09)],
    ),
    "WF - First Visit": GrinchLocationData(
        "Who Forest",
        ["Visitsanity", "Who Forest"],
        104,
        [
            GrinchRamData(0x010000, value=0x0B),
            # GrinchRamData(0x01024A, binary_bit_pos=1),
         ],
    ),
    "WF - Ski Resort - First Visit": GrinchLocationData(
        "Ski Resort",
        ["Visitsanity", "Who Forest", "Ski Resort"],
        105,
        [GrinchRamData(0x010000, value=0x0C)],
    ),
    "WF - Civic Center - First Visit": GrinchLocationData(
        "Civic Center",
        ["Visitsanity", "Who Forest", "Civic Center"],
        106,
        [GrinchRamData(0x010000, value=0x0D)],
    ),
    "WD - First Visit": GrinchLocationData(
        "Who Dump",
        ["Visitsanity", "Who Dump"],
        107,
        [
            GrinchRamData(0x010000, value=0x0E),
            # GrinchRamData(0x01025C, binary_bit_pos=1),
        ],
    ),
    "WD - Minefield - First Visit": GrinchLocationData(
        "Minefield",
        ["Visitsanity", "Who Dump", "Minefield"],
        108,
        [GrinchRamData(0x010000, value=0x11)],
    ),
    "WD - Power Plant - First Visit": GrinchLocationData(
        "Power Plant",
        ["Visitsanity", "Who Dump", "Power Plant"],
        109,
        [GrinchRamData(0x010000, value=0x10)],
    ),
    "WD - Generator Building - First Visit": GrinchLocationData(
        "Generator Building",
        ["Visitsanity", "Who Dump", "Generator Building"],
        110,
        [GrinchRamData(0x010000, value=0x0F)],
    ),
    "WL - South Shore - First Visit": GrinchLocationData(
        "Who Lake",
        ["Visitsanity", "Who Lake", "South Shore"],
        111,
        [
            GrinchRamData(0x010000, value=0x12),
            # GrinchRamData(0x010282, binary_bit_pos=4),
        ],
    ),
    "WL - Submarine World - First Visit": GrinchLocationData(
        "Submarine World",
        ["Visitsanity", "Who Lake", "Submarine World"],
        112,
        [GrinchRamData(0x010000, value=0x17)],
    ),
    "WL - Scout's Hut - First Visit": GrinchLocationData(
        "Scout's Hut",
        ["Visitsanity", "Who Lake", "Scout's Hut"],
        113,
        [GrinchRamData(0x010000, value=0x13)],
    ),
    "WL - North Shore - First Visit": GrinchLocationData(
        "North Shore",
        ["Visitsanity", "Who Lake", "North Shore"],
        114,
        [GrinchRamData(0x010000, value=0x14)],
    ),
    "WL - Mayor's Villa - First Visit": GrinchLocationData(
        "Mayor's Villa",
        ["Visitsanity", "Who Lake", "Mayor's Villa"],
        115,
        [GrinchRamData(0x010000, value=0x16)],
    ),
    # Need to find mission completion address for handful of locations that are not documented.
    # Missions that have value are the ones we need to find the check for
    # Whoville Missions
    "WV - Post Office - Shuffling The Mail": GrinchLocationData(
        "Post Office",
        ["Whoville Missions", "Missions", "Whoville", "Post Office"],
        201,
        [GrinchRamData(0x0100BE, binary_bit_pos=0)],
    ),
    "WV - Smashing Snowmen": GrinchLocationData(
        "Whoville",
        ["Whoville Missions", "Missions", "Whoville"],
        200,
        [GrinchRamData(0x0100C5, value=10)],
    ),
    "WV - Painting The Mayor's Posters": GrinchLocationData(
        "Whoville",
        ["Whoville Missions", "Missions", "Whoville"],
        202,
        [GrinchRamData(0x0100C6, value=10)],
    ),
    "WV - Launching Eggs Into Houses": GrinchLocationData(
        "Whoville",
        ["Whoville Missions", "Missions", "Whoville"],
        203,
        [GrinchRamData(0x0100C7, value=10)],
    ),
    "WV - City Hall - Modifying The Mayor's Statue": GrinchLocationData(
        "City Hall",
        ["Whoville Missions", "Missions", "Whoville", "City Hall"],
        204,
        [GrinchRamData(0x0100BE, binary_bit_pos=1)],
    ),
    "WV - Clock Tower - Advancing The Countdown-To-Xmas Clock": GrinchLocationData(
        "Clock Tower",
        ["Whoville Missions", "Missions", "Whoville", "Clock Tower"],
        205,
        [GrinchRamData(0x0100BE, binary_bit_pos=2)],
    ),
    "WV - Squashing All Gifts": GrinchLocationData(
        "Whoville",
        ["Whoville Missions", "Missions", "Giftsanity", "Whoville"],
        206,
        [GrinchRamData(0x01005C, value=500, byte_size=2)],
    ),
    # Who Forest Missions
    "WF - Making Xmas Trees Droop": GrinchLocationData(
        "Who Forest",
        ["Who Forest Missions", "Missions", "Who Forest"],
        300,
        [GrinchRamData(0x0100C8, value=10)],
    ),
    "WF - Sabotaging Snow Cannon With Glue": GrinchLocationData(
        "Who Forest",
        ["Who Forest Missions", "Missions", "Who Forest"],
        301,
        [GrinchRamData(0x0100BE, binary_bit_pos=3)],
    ),
    "WF - Putting Beehives In Cabins": GrinchLocationData(
        "Who Forest",
        ["Who Forest Missions", "Missions", "Who Forest"],
        302,
        [GrinchRamData(0x0100CA, value=10)],
    ),
    "WF - Ski Resort - Sliming The Mayor's Skis": GrinchLocationData(
        "Ski Resort",
        ["Who Forest Missions", "Missions", "Who Forest", "Ski Resort"],
        303,
        [GrinchRamData(0x0100BE, binary_bit_pos=4)],
    ),
    "WF - Civic Center - Replacing The Candles On The Cake With Fireworks": GrinchLocationData(
        "Civic Center",
        ["Who Forest Missions", "Missions", "Who Forest", "Civic Center"],
        304,
        [GrinchRamData(0x0100BE, binary_bit_pos=5)],
    ),
    "WF - Squashing All Gifts": GrinchLocationData(
        "Who Forest",
        ["Who Forest Missions", "Missions", "Giftsanity", "Who Forest"],
        305,
        [GrinchRamData(0x01005E, value=750, byte_size=2)],
    ),
    # Who Dump Missions
    "WD - Stealing Food From Birds": GrinchLocationData(
        "Who Dump",
        ["Who Dump Missions", "Missions", "Who Dump"],
        400,
        [GrinchRamData(0x0100CB, value=10)],
    ),
    "WD - Feeding The Computer With Robot Parts": GrinchLocationData(
        "Who Dump",
        ["Who Dump Missions", "Missions", "Who Dump"],
        401,
        [GrinchRamData(0x0100BF, binary_bit_pos=2)],
    ),
    "WD - Infesting The Mayor's House With Rats": GrinchLocationData(
        "Who Dump",
        ["Who Dump Missions", "Missions", "Who Dump"],
        402,
        [GrinchRamData(0x0100BE, binary_bit_pos=6)],
    ),
    "WD - Conducting The Stinky Gas To Who-Bris' Shack": GrinchLocationData(
        "Who Dump",
        ["Who Dump Missions", "Missions", "Who Dump"],
        403,
        [GrinchRamData(0x0100BE, binary_bit_pos=7)],
    ),
    "WD - Minefield - Shaving Who Dump Guardian": GrinchLocationData(
        "Minefield",
        ["Who Dump Missions", "Missions", "Who Dump", "Minefield"],
        404,
        [GrinchRamData(0x0100BF, binary_bit_pos=0)],
    ),
    "WD - Generator Building - Short-Circuiting Power-Plant": GrinchLocationData(
        "Generator Building",
        ["Who Dump Missions", "Missions", "Who Dump", "Generator Building"],
        405,
        [GrinchRamData(0x0100BF, binary_bit_pos=1)],
    ),
    "WD - Squashing All Gifts": GrinchLocationData(
        "Who Dump",
        ["Who Dump Missions", "Missions", "Who Dump", "Giftsanity"],
        406,
        [GrinchRamData(0x010060, value=750, byte_size=2)],
    ),
    # Who Lake Missions
    "WL - South Shore - Putting Thistles In Shorts": GrinchLocationData(
        "Who Lake",
        [
            "Who Lake Missions",
            "Missions",
            "Who Lake",
            "South Shore",
            "South Shore Missions",
        ],
        500,
        [GrinchRamData(0x0100E5, value=10)],
    ),
    "WL - South Shore - Sabotaging The Tents": GrinchLocationData(
        "Who Lake",
        [
            "Who Lake Missions",
            "Missions",
            "Who Lake",
            "South Shore",
            "South Shore Missions",
        ],
        501,
        [GrinchRamData(0x0100E6, value=10)],
    ),
    "WL - North Shore - Drilling Holes In Canoes": GrinchLocationData(
        "North Shore",
        ["Who Lake Missions", "Missions", "Who Lake", "North Shore"],
        502,
        [GrinchRamData(0x0100EE, value=10)],
    ),
    "WL - Submarine World - Modifying The Marine Mobile": GrinchLocationData(
        "Submarine World",
        ["Who Lake Missions", "Missions", "Who Lake", "Submarine World"],
        503,
        [GrinchRamData(0x0100BF, binary_bit_pos=4)],
    ),
    "WL - Mayor's Villa - Hooking The Mayor's Bed To The Motorboat": GrinchLocationData(
        "Mayor's Villa",
        ["Who Lake Missions", "Missions", "Who Lake", "Mayor's Villa"],
        504,
        [GrinchRamData(0x0100BF, binary_bit_pos=3)],
    ),
    "WL - Squashing All Gifts": GrinchLocationData(
        "Who Lake",
        ["Who Lake Missions", "Missions", "Who Lake", "Giftsanity"],
        505,
        [GrinchRamData(0x010062, value=1000, byte_size=2)],
    ),
    # Need to find binary values for individual blueprints, but all ram addresses are found
    # Blueprints
    # Binoculars Blueprints
    "WV - Binoculars BP on Post Office Roof": GrinchLocationData(
        "Whoville",
        ["Binocular Blueprints", "Blueprints", "Whoville", "Whoville Blueprints"],
        600,
        [GrinchRamData(0x01020B, binary_bit_pos=2)],
    ),
    "WV - City Hall - Binoculars BP left side of Library": GrinchLocationData(
        "City Hall",
        [
            "Binocular Blueprints",
            "Blueprints",
            "Whoville",
            "Whoville Blueprints",
            "City Hall",
            "City Hall Blueprints",
        ],
        601,
        [GrinchRamData(0x01021F, binary_bit_pos=6)],
    ),
    "WV - City Hall - Binoculars BP front side of Library": GrinchLocationData(
        "City Hall",
        [
            "Binocular Blueprints",
            "Blueprints",
            "Whoville",
            "Whoville Blueprints",
            "City Hall",
            "City Hall Blueprints",
        ],
        602,
        [GrinchRamData(0x01021F, binary_bit_pos=5)],
    ),
    "WV - City Hall - Binoculars BP right side of Library": GrinchLocationData(
        "City Hall",
        [
            "Binocular Blueprints",
            "Blueprints",
            "Whoville",
            "Whoville Blueprints",
            "City Hall",
            "City Hall Blueprints",
        ],
        603,
        [GrinchRamData(0x01021F, binary_bit_pos=4)],
    ),
    # Rotten Egg Launcher Blueprints
    "WV - REL BP left of City Hall": GrinchLocationData(
        "Whoville",
        [
            "Rotten Egg Launcher Blueprints",
            "Blueprints",
            "Whoville",
            "Whoville Blueprints",
        ],
        700,
        [GrinchRamData(0x01020B, binary_bit_pos=0)],
    ),
    "WV - REL BP left of Clock Tower": GrinchLocationData(
        "Whoville",
        [
            "Rotten Egg Launcher Blueprints",
            "Blueprints",
            "Whoville",
            "Whoville Blueprints",
        ],
        701,
        [GrinchRamData(0x01020B, binary_bit_pos=1)],
    ),
    "WV - Post Office - REL BP inside Gray Room": GrinchLocationData(
        "Post Office",
        [
            "Rotten Egg Launcher Blueprints",
            "Blueprints",
            "Whoville",
            "Whoville Blueprints",
            "Post Office",
            "Post Office Blueprints",
        ],
        702,
        [GrinchRamData(0x01021C, binary_bit_pos=1)],
    ),
    "WV - Post Office - REL BP at Entrance Door after Mission Completion": GrinchLocationData(
        "Post Office",
        [
            "Rotten Egg Launcher Blueprints",
            "Blueprints",
            "Whoville",
            "Whoville Blueprints",
            "Post Office",
            "Post Office Blueprints",
        ],
        703,
        [GrinchRamData(0x01021C, binary_bit_pos=2)],
    ),
    # Rocket Spring Blueprints
    "WF - RS BP behind Vacuum Tube": GrinchLocationData(
        "Who Forest",
        [
            "Rocket Spring Blueprints",
            "Blueprints",
            "Who Forest",
            "Who Forest Blueprints",
        ],
        800,
        [GrinchRamData(0x010243, binary_bit_pos=3)],
    ),
    "WF - RS BP in front of 2nd House near Vacuum Tube": GrinchLocationData(
        "Who Forest",
        [
            "Rocket Spring Blueprints",
            "Blueprints",
            "Who Forest",
            "Who Forest Blueprints",
        ],
        801,
        [GrinchRamData(0x010243, binary_bit_pos=1)],
    ),
    "WF - RS BP near Tree House on Ground": GrinchLocationData(
        "Who Forest",
        [
            "Rocket Spring Blueprints",
            "Blueprints",
            "Who Forest",
            "Who Forest Blueprints",
        ],
        802,
        [GrinchRamData(0x010243, binary_bit_pos=4)],
    ),
    "WF - RS BP behind Cable Car House": GrinchLocationData(
        "Who Forest",
        [
            "Rocket Spring Blueprints",
            "Blueprints",
            "Who Forest",
            "Who Forest Blueprints",
        ],
        804,
        [GrinchRamData(0x010242, binary_bit_pos=7)],
    ),
    "WF - RS BP near Who Snowball in Cave": GrinchLocationData(
        "Who Forest",
        [
            "Rocket Spring Blueprints",
            "Blueprints",
            "Who Forest",
            "Who Forest Blueprints",
        ],
        805,
        [GrinchRamData(0x010242, binary_bit_pos=6)],
    ),
    "WF - RS BP on Branch Platform closest to Glue Cannon": GrinchLocationData(
        "Who Forest",
        [
            "Rocket Spring Blueprints",
            "Blueprints",
            "Who Forest",
            "Who Forest Blueprints",
        ],
        806,
        [GrinchRamData(0x010243, binary_bit_pos=2)],
    ),
    "WF - RS BP on Branch Platform Near Beast": GrinchLocationData(
        "Who Forest",
        [
            "Rocket Spring Blueprints",
            "Blueprints",
            "Who Forest",
            "Who Forest Blueprints",
        ],
        807,
        [GrinchRamData(0x010243, binary_bit_pos=0)],
    ),
    "WF - RS BP on Branch Platform Elevated next to House": GrinchLocationData(
        "Who Forest",
        [
            "Rocket Spring Blueprints",
            "Blueprints",
            "Who Forest",
            "Who Forest Blueprints",
        ],
        808,
        [GrinchRamData(0x010243, binary_bit_pos=6)],
    ),
    "WF - RS BP on Tree House": GrinchLocationData(
        "Who Forest",
        [
            "Rocket Spring Blueprints",
            "Blueprints",
            "Who Forest",
            "Who Forest Blueprints",
        ],
        809,
        [GrinchRamData(0x010243, binary_bit_pos=5)],
    ),
    # Slime Shooter Blueprints
    "WF - SS BP in Branch Platform Elevated House": GrinchLocationData(
        "Who Forest",
        [
            "Slime Shooter Blueprints",
            "Blueprints",
            "Who Forest",
            "Who Forest Blueprints",
        ],
        900,
        [GrinchRamData(0x010244, binary_bit_pos=3)],
    ),
    "WF - SS BP in Branch Platform House next to Beast": GrinchLocationData(
        "Who Forest",
        [
            "Slime Shooter Blueprints",
            "Blueprints",
            "Who Forest",
            "Who Forest Blueprints",
        ],
        901,
        [GrinchRamData(0x010243, binary_bit_pos=7)],
    ),
    "WF - SS BP in House in front of Civic Center Cave": GrinchLocationData(
        "Who Forest",
        [
            "Slime Shooter Blueprints",
            "Blueprints",
            "Who Forest",
            "Who Forest Blueprints",
        ],
        902,
        [GrinchRamData(0x010244, binary_bit_pos=2)],
    ),
    "WF - SS BP in House next to Tree House": GrinchLocationData(
        "Who Forest",
        [
            "Slime Shooter Blueprints",
            "Blueprints",
            "Who Forest",
            "Who Forest Blueprints",
        ],
        903,
        [GrinchRamData(0x010244, binary_bit_pos=1)],
    ),
    "WF - SS BP in House across from Tree House": GrinchLocationData(
        "Who Forest",
        [
            "Slime Shooter Blueprints",
            "Blueprints",
            "Who Forest",
            "Who Forest Blueprints",
        ],
        904,
        [GrinchRamData(0x010244, binary_bit_pos=5)],
    ),
    "WF - SS BP in 2nd House near Vacuum Tube Right Side": GrinchLocationData(
        "Who Forest",
        [
            "Slime Shooter Blueprints",
            "Blueprints",
            "Who Forest",
            "Who Forest Blueprints",
        ],
        905,
        [GrinchRamData(0x010244, binary_bit_pos=4)],
    ),
    "WF - SS BP in 2nd House near Vacuum Tube Left Side": GrinchLocationData(
        "Who Forest",
        [
            "Slime Shooter Blueprints",
            "Blueprints",
            "Who Forest",
            "Who Forest Blueprints",
        ],
        906,
        [GrinchRamData(0x010244, binary_bit_pos=7)],
    ),
    "WF - SS BP in 2nd House near Vacuum Tube inbetween Blueprints": GrinchLocationData(
        "Who Forest",
        [
            "Slime Shooter Blueprints",
            "Blueprints",
            "Who Forest",
            "Who Forest Blueprints",
        ],
        907,
        [GrinchRamData(0x010244, binary_bit_pos=6)],
    ),
    "WF - SS BP in House near Vacuum Tube": GrinchLocationData(
        "Who Forest",
        [
            "Slime Shooter Blueprints",
            "Blueprints",
            "Who Forest",
            "Who Forest Blueprints",
        ],
        908,
        [GrinchRamData(0x010244, binary_bit_pos=0)],
    ),
    # Octopus Climbing Device
    "WD - OCD BP inside Pipe near Vacuum Tube": GrinchLocationData(
        "Who Dump",
        [
            "Octopus Climbing Device Blueprints",
            "Blueprints",
            "Who Dump",
            "Who Dump Blueprints",
        ],
        1001,
        [GrinchRamData(0x010252, binary_bit_pos=3)],
    ),
    "WD - OCD BP inside Pipe on Minefield side": GrinchLocationData(
        "Who Dump",
        [
            "Octopus Climbing Device Blueprints",
            "Blueprints",
            "Who Dump",
            "Who Dump Blueprints",
        ],
        1002,
        [GrinchRamData(0x010252, binary_bit_pos=5)],
    ),
    "WD - OCD BP in Vent to Mayor's House": GrinchLocationData(
        "Who Dump",
        [
            "Octopus Climbing Device Blueprints",
            "Blueprints",
            "Who Dump",
            "Who Dump Blueprints",
        ],
        1003,
        [GrinchRamData(0x010252, binary_bit_pos=1)],
    ),
    "WD - OCD BP inside Pipe on Power Plant side": GrinchLocationData(
        "Who Dump",
        [
            "Octopus Climbing Device Blueprints",
            "Blueprints",
            "Who Dump",
            "Who Dump Blueprints",
        ],
        1004,
        [GrinchRamData(0x010252, binary_bit_pos=4)],
    ),
    "WD - OCD BP near Right Side of Power Plant Wall": GrinchLocationData(
        "Who Dump",
        [
            "Octopus Climbing Device Blueprints",
            "Blueprints",
            "Who Dump",
            "Who Dump Blueprints",
        ],
        1005,
        [GrinchRamData(0x010252, binary_bit_pos=0)],
    ),
    "WD - OCD BP near Who-Bris' Shack": GrinchLocationData(
        "Who Dump",
        [
            "Octopus Climbing Device Blueprints",
            "Blueprints",
            "Who Dump",
            "Who Dump Blueprints",
        ],
        1006,
        [GrinchRamData(0x010252, binary_bit_pos=2)],
    ),
    "WD - Minefield - OCD BP on Left Side of House": GrinchLocationData(
        "Minefield",
        [
            "Octopus Climbing Device Blueprints",
            "Blueprints",
            "Who Dump",
            "Who Dump Blueprints",
            "Minefield",
            "Minefield Blueprints",
        ],
        1007,
        [GrinchRamData(0x01026E, binary_bit_pos=2)],
    ),
    "WD - Minefield - OCD BP on Right Side of Shack": GrinchLocationData(
        "Minefield",
        [
            "Octopus Climbing Device Blueprints",
            "Blueprints",
            "Who Dump",
            "Who Dump Blueprints",
            "Minefield",
            "Minefield Blueprints",
        ],
        1008,
        [GrinchRamData(0x01026E, binary_bit_pos=4)],
    ),
    "WD - Minefield - OCD BP inside Guardian's House": GrinchLocationData(
        "Minefield",
        [
            "Octopus Climbing Device Blueprints",
            "Blueprints",
            "Who Dump",
            "Who Dump Blueprints",
            "Minefield",
            "Minefield Blueprints",
        ],
        1009,
        [GrinchRamData(0x01026E, binary_bit_pos=3)],
    ),
    # Marine Mobile Blueprints
    "WL - South Shore - MM BP on Bridge to Scout's Hut": GrinchLocationData(
        "Who Lake",
        [
            "Marine Mobile Blueprints",
            "Blueprints",
            "Who Lake",
            "Who Lake Blueprints",
            "South Shore",
            "South Shore Blueprints",
        ],
        1100,
        [GrinchRamData(0x010281, binary_bit_pos=5)],
    ),
    "WL - South Shore - MM BP across from Tent near Porcupine": GrinchLocationData(
        "Who Lake",
        [
            "Marine Mobile Blueprints",
            "Blueprints",
            "Who Lake",
            "Who Lake Blueprints",
            "South Shore",
            "South Shore Blueprints",
        ],
        1101,
        [GrinchRamData(0x010281, binary_bit_pos=6)],
    ),
    "WL - South Shore - MM BP near Outhouse": GrinchLocationData(
        "Who Lake",
        [
            "Marine Mobile Blueprints",
            "Blueprints",
            "Who Lake",
            "Who Lake Blueprints",
            "South Shore",
            "South Shore Blueprints",
        ],
        1102,
        [GrinchRamData(0x010281, binary_bit_pos=7)],
    ),
    "WL - South Shore - MM BP near Hill Bridge": GrinchLocationData(
        "Who Lake",
        [
            "Marine Mobile Blueprints",
            "Blueprints",
            "Who Lake",
            "Who Lake Blueprints",
            "South Shore",
            "South Shore Blueprints",
        ],
        1103,
        [GrinchRamData(0x010282, binary_bit_pos=0)],
    ),
    "WL - South Shore - MM BP on Scout's Hut Roof": GrinchLocationData(
        "Who Lake",
        [
            "Marine Mobile Blueprints",
            "Blueprints",
            "Who Lake",
            "Who Lake Blueprints",
            "South Shore",
            "South Shore Blueprints",
        ],
        1104,
        [GrinchRamData(0x010281, binary_bit_pos=4)],
    ),
    "WL - South Shore - MM BP on Grass Platform": GrinchLocationData(
        "Who Lake",
        [
            "Marine Mobile Blueprints",
            "Blueprints",
            "Who Lake",
            "Who Lake Blueprints",
            "South Shore",
            "South Shore Blueprints",
        ],
        1105,
        [GrinchRamData(0x010281, binary_bit_pos=2)],
    ),
    "WL - South Shore - MM BP across Zipline Platform": GrinchLocationData(
        "Who Lake",
        [
            "Marine Mobile Blueprints",
            "Blueprints",
            "Who Lake",
            "Who Lake Blueprints",
            "South Shore",
            "South Shore Blueprints",
        ],
        1106,
        [GrinchRamData(0x010281, binary_bit_pos=3)],
    ),
    "WL - South Shore - MM BP behind Summer Beast": GrinchLocationData(
        "Who Lake",
        [
            "Marine Mobile Blueprints",
            "Blueprints",
            "Who Lake",
            "Who Lake Blueprints",
            "South Shore",
            "South Shore Blueprints",
        ],
        1107,
        [GrinchRamData(0x010282, binary_bit_pos=1)],
    ),
    "WL - North Shore - MM BP below Bridge": GrinchLocationData(
        "North Shore",
        [
            "Marine Mobile Blueprints",
            "Blueprints",
            "Who Lake",
            "Who Lake Blueprints",
            "North Shore",
            "North Shore Blueprints",
        ],
        1108,
        [GrinchRamData(0x010293, binary_bit_pos=0)],
    ),
    "WL - North Shore - MM BP behind Skunk Hut": GrinchLocationData(
        "North Shore",
        [
            "Marine Mobile Blueprints",
            "Blueprints",
            "Who Lake",
            "Who Lake Blueprints",
            "North Shore",
            "North Shore Blueprints",
        ],
        1109,
        [GrinchRamData(0x010293, binary_bit_pos=2)],
    ),
    "WL - North Shore - MM BP inside Skunk Hut": GrinchLocationData(
        "North Shore",
        [
            "Marine Mobile Blueprints",
            "Blueprints",
            "Who Lake",
            "Who Lake Blueprints",
            "North Shore",
            "North Shore Blueprints",
        ],
        1110,
        [GrinchRamData(0x010292, binary_bit_pos=6)],
    ),
    "WL - North Shore - MM BP inside House's Fence": GrinchLocationData(
        "North Shore",
        [
            "Marine Mobile Blueprints",
            "Blueprints",
            "Who Lake",
            "Who Lake Blueprints",
            "North Shore",
            "North Shore Blueprints",
        ],
        1111,
        [GrinchRamData(0x010292, binary_bit_pos=7)],
    ),
    "WL - North Shore - MM BP inside Boulder Box near Bridge": GrinchLocationData(
        "North Shore",
        [
            "Marine Mobile Blueprints",
            "Blueprints",
            "Who Lake",
            "Who Lake Blueprints",
            "North Shore",
            "North Shore Blueprints",
        ],
        1112,
        [GrinchRamData(0x010293, binary_bit_pos=3)],
    ),
    "WL - North Shore - MM BP inside Boulder Box behind Skunk Hut": GrinchLocationData(
        "North Shore",
        [
            "Marine Mobile Blueprints",
            "Blueprints",
            "Who Lake",
            "Who Lake Blueprints",
            "North Shore",
            "North Shore Blueprints",
        ],
        1113,
        [GrinchRamData(0x010293, binary_bit_pos=4)],
    ),
    "WL - North Shore - MM BP inside Drill House": GrinchLocationData(
        "North Shore",
        [
            "Marine Mobile Blueprints",
            "Blueprints",
            "Who Lake",
            "Who Lake Blueprints",
            "North Shore",
            "North Shore Blueprints",
        ],
        1114,
        [GrinchRamData(0x010292, binary_bit_pos=5)],
    ),
    "WL - North Shore - MM BP on Crow Platform near Drill House": GrinchLocationData(
        "North Shore",
        [
            "Marine Mobile Blueprints",
            "Blueprints",
            "Who Lake",
            "Who Lake Blueprints",
            "North Shore",
            "North Shore Blueprints",
        ],
        1115,
        [GrinchRamData(0x010293, binary_bit_pos=1)],
    ),
    # Grinch Copter Blueprints
    "WV - City Hall - GC BP in Safe Room": GrinchLocationData(
        "City Hall",
        [
            "Grinch Copter Blueprints",
            "Blueprints",
            "Whoville",
            "Whoville Blueprints",
            "City Hall",
            "City Hall Blueprints",
        ],
        1200,
        [GrinchRamData(0x01021F, binary_bit_pos=7)],
    ),
    "WV - City Hall - GC BP in Statue Room": GrinchLocationData(
        "City Hall",
        [
            "Grinch Copter Blueprints",
            "Blueprints",
            "Whoville",
            "Whoville Blueprints",
            "City Hall",
            "City Hall Blueprints",
        ],
        1201,
        [GrinchRamData(0x010220, binary_bit_pos=0)],
    ),
    "WV - Clock Tower - GC BP in Bedroom": GrinchLocationData(
        "Clock Tower",
        [
            "Grinch Copter Blueprints",
            "Blueprints",
            "Whoville",
            "Whoville Blueprints",
            "Clock Tower",
            "Clock Tower Blueprints",
        ],
        1202,
        [GrinchRamData(0x010216, binary_bit_pos=3)],
    ),
    "WV - Clock Tower - GC BP in Bell Room": GrinchLocationData(
        "Clock Tower",
        [
            "Grinch Copter Blueprints",
            "Blueprints",
            "Whoville",
            "Whoville Blueprints",
            "Clock Tower",
            "Clock Tower Blueprints",
        ],
        1203,
        [GrinchRamData(0x010216, binary_bit_pos=2)],
    ),
    "WF - Ski Resort - GC BP inside Dog's Fence": GrinchLocationData(
        "Ski Resort",
        [
            "Grinch Copter Blueprints",
            "Blueprints",
            "Who Forest",
            "Who Forest Blueprints",
            "Ski Resort",
            "Ski Resort Blueprints",
        ],
        1204,
        [GrinchRamData(0x010234, binary_bit_pos=7)],
    ),
    "WF - Ski Resort - GC BP in Max Cave": GrinchLocationData(
        "Ski Resort",
        [
            "Grinch Copter Blueprints",
            "Blueprints",
            "Who Forest",
            "Who Forest Blueprints",
            "Ski Resort",
            "Ski Resort Blueprints",
        ],
        1205,
        [GrinchRamData(0x010234, binary_bit_pos=6)],
    ),
    "WF - Civic Center - GC BP on Left Side in Bat Cave Wall": GrinchLocationData(
        "Civic Center",
        [
            "Grinch Copter Blueprints",
            "Blueprints",
            "Who Forest",
            "Who Forest Blueprints",
            "Civic Center",
            "Civic Center Blueprints",
        ],
        1206,
        [GrinchRamData(0x01022A, binary_bit_pos=7)],
    ),
    "WF - Civic Center - GC BP in Frozen Ice": GrinchLocationData(
        "Civic Center",
        [
            "Grinch Copter Blueprints",
            "Blueprints",
            "Who Forest",
            "Who Forest Blueprints",
            "Civic Center",
            "Civic Center Blueprints",
        ],
        1207,
        [GrinchRamData(0x01022B, binary_bit_pos=0)],
    ),
    "WD - Power Plant - GC BP in Max Cave": GrinchLocationData(
        "Power Plant",
        [
            "Grinch Copter Blueprints",
            "Blueprints",
            "Who Dump",
            "Who Dump Blueprints",
            "Power Plant",
            "Power Plant Blueprints",
        ],
        1208,
        [GrinchRamData(0x010265, binary_bit_pos=1)],
    ),
    "WD - Power Plant - GC BP After First Gate": GrinchLocationData(
        "Power Plant",
        [
            "Grinch Copter Blueprints",
            "Blueprints",
            "Who Dump",
            "Who Dump Blueprints",
            "Power Plant",
            "Power Plant Blueprints",
        ],
        1209,
        [GrinchRamData(0x010265, binary_bit_pos=2)],
    ),
    "WD - Generator Building - GC BP on the Highest Platform": GrinchLocationData(
        "Generator Building",
        [
            "Grinch Copter Blueprints",
            "Blueprints",
            "Who Dump",
            "Who Dump Blueprints",
            "Generator Building",
            "Generator Building Blueprints",
        ],
        1210,
        [GrinchRamData(0x01026B, binary_bit_pos=0)],
    ),
    "WD - Generator Building - GC BP at the Entrance after Mission Completion": GrinchLocationData(
        "Generator Building",
        [
            "Grinch Copter Blueprints",
            "Blueprints",
            "Who Dump",
            "Who Dump Blueprints",
            "Generator Building",
            "Generator Building Blueprints",
        ],
        1211,
        [GrinchRamData(0x01026B, binary_bit_pos=1)],
    ),
    "WL - Submarine World - GC BP Just Below Water Surface": GrinchLocationData(
        "Submarine World",
        [
            "Grinch Copter Blueprints",
            "Blueprints",
            "Who Lake",
            "Who Lake Blueprints",
            "Submarine World",
            "Submarine World Blueprints",
        ],
        1212,
        [GrinchRamData(0x010289, binary_bit_pos=3)],
    ),
    "WL - Submarine World - GC BP Underwater": GrinchLocationData(
        "Submarine World",
        [
            "Grinch Copter Blueprints",
            "Blueprints",
            "Who Lake",
            "Who Lake Blueprints",
            "Submarine World",
            "Submarine World Blueprints",
        ],
        1213,
        [GrinchRamData(0x010289, binary_bit_pos=4)],
    ),
    "WL - Mayor's Villa - GC BP on Tree Branch": GrinchLocationData(
        "Mayor's Villa",
        [
            "Grinch Copter Blueprints",
            "Blueprints",
            "Who Lake",
            "Who Lake Blueprints",
            "Mayor's Villa",
            "Mayor's Villa Blueprints",
        ],
        1214,
        [GrinchRamData(0x010275, binary_bit_pos=7)],
    ),
    "WL - Mayor's Villa - GC BP in Pirate's Cave": GrinchLocationData(
        "Mayor's Villa",
        [
            "Grinch Copter Blueprints",
            "Blueprints",
            "Who Lake",
            "Who Lake Blueprints",
            "Mayor's Villa",
            "Mayor's Villa Blueprints",
        ],
        1215,
        [GrinchRamData(0x010275, binary_bit_pos=6)],
    ),
    # Sleigh Room Locations
    "MC - Sleigh Ride - Stealing All Gifts": GrinchLocationData(
        "Sleigh Ride",
        ["Sleigh Ride"],
        1300,
        [GrinchRamData(0x0100BF, binary_bit_pos=6)],
    ),
    "MC - Sleigh Ride - Neutralizing Santa": GrinchLocationData(
        "Sleigh Ride",
        ["Sleigh Ride"],
        1301,
        [GrinchRamData(0x0100BF, binary_bit_pos=7)],
    ),
    "MC - Sleigh Ride - Save Christmas": GrinchLocationData(
        "Sleigh Ride",
        ["Sleigh Ride"],
        1302,
        [GrinchRamData(0x010000, value=0x3E)],
    ),
    # Heart of Stones
    "WV - Post Office - Heart of Stone": GrinchLocationData(
        "Post Office",
        ["Heart of Stones", "Whoville", "Post Office"],
        1400,
        [
            # GrinchRamData(0x0101FA, binary_bit_pos=6),
            GrinchRamData(0x010000, value=0x0A),
            GrinchRamData(0x0E303A, binary_bit_pos=5),
        ],
    ),
    "WF - Ski Resort - Heart of Stone": GrinchLocationData(
        "Ski Resort",
        ["Heart of Stones", "Who Forest", "Ski Resort"],
        1401,
        [
            # GrinchRamData(0x0101FA, binary_bit_pos=7),
            GrinchRamData(0x010000, value=0x0C),
            GrinchRamData(0x0100C1, binary_bit_pos=6),
         ],
    ),
    "WD - Minefield - Heart of Stone": GrinchLocationData(
        "Minefield",
        ["Heart of Stones", "Who Dump", "Minefield"],
        1402,
        [
            # GrinchRamData(0x0101FB, binary_bit_pos=0),
            GrinchRamData(0x010000, value=0x11),
            # GrinchRamData(0x0EE054, value=188),
            GrinchRamData(0x095306, value=27),
        ],
    ),
    "WL - North Shore - Heart of Stone": GrinchLocationData(
        "North Shore",
        ["Heart of Stones", "Who Lake", "North Shore"],
        1403,
        [
            # GrinchRamData(0x0101FB, binary_bit_pos=1),
            GrinchRamData(0x010000, value=0x14),
            GrinchRamData(0x0100C3, binary_bit_pos=6),
        ],
    ),
    # Supadow Minigames
    # "Spin N' Win - Easy": GrinchLocationData(
    #     "Spin N' Win",
    #     ["Supadow Minigames", "Spin N' Win"],
    #     1500,
    #     [GrinchRamData(0x0100FD, min_count=1, max_count=59)]),
    # "Spin N' Win - Hard": GrinchLocationData(
    #     "Spin N' Win",
    #     ["Supadow Minigames", "Spin N' Win"],
    #     1501,
    #     [GrinchRamData(0x0100FD, min_count=1, max_count=44)]),
    # "Spin N' Win - Real Tough": GrinchLocationData(
    #     "Spin N' Win",
    #     ["Supadow Minigames", "Spin N' Win"],
    #     1502,
    #     [GrinchRamData(0x0100FD, min_count=1, max_count=29)]),
    # "Dankamania - 12 Points": GrinchLocationData(
    #     "Dankamania",
    #     ["Supadow Minigames", "Dankamania"],
    #     1503,
    #     [GrinchRamData(0x0100FB, min_count=12)]),
    # "The Copter Race Contest - Easy": GrinchLocationData(
    #     "The Copter Race Contest",
    #     ["Supadow Minigames", "The Copter Race Contest"],
    #     1504,
    #     [GrinchRamData(0x0100FC, min_count=1, max_count=44)]),
    # "The Copter Race Contest - Hard": GrinchLocationData(
    #     "The Copter Race Contest",
    #     ["Supadow Minigames", "The Copter Race Contest"],
    #     1505,
    #     [GrinchRamData(0x0100FC, min_count=1, max_count=34)]),
    # "The Copter Race Contest - Real Tough": GrinchLocationData(
    #     "The Copter Race Contest",
    #     ["Supadow Minigames", "The Copter Race Contest"],
    #     1506,
    #     [GrinchRamData(0x0100FC, min_count=1, max_count=29)]),
    # "Bike Race - 1st Place":  GrinchLocationData(
    #     "Bike Race",
    #     ["Supadow Minigames", "Bike Race"],
    #     1509,
    #     [
    #         GrinchRamData(0x010000, value=0x18),
    #         GrinchRamData(0x134CA5, value=1)]),
    # "Bike Race - Top 2": GrinchLocationData(
    #     "Bike Race",
    #     ["Supadow Minigames", "Bike Race"],
    #     1510,
    #     [
    #         GrinchRamData(0x010000, value=0x18),
    #         GrinchRamData(0x134CA5, min_count=1, max_count=2)]),
    # "Bike Race - Top 3": GrinchLocationData(
    #     "Bike Race",
    #     ["Supadow Minigames", "Bike Race"],
    #     1511,
    #     [
    #         GrinchRamData(0x010000, value=0x18),
    #         GrinchRamData(0x134CA5, min_count=1, max_count=3)]),
    # "Bike Race - Top 4": GrinchLocationData(
    #     "Bike Race",
    #     ["Supadow Minigames", "Bike Race"],
    #     1512,
    #     [
    #         GrinchRamData(0x010000, value=0x18),
    #         GrinchRamData(0x134CA5, min_count=1, max_count=4)]),
    # Sleigh Part Locations
    "WV - Exhaust Pipes": GrinchLocationData(
        "Whoville",
        ["Sleigh Ride", "Whoville", "Sleigh Parts"],
        1600,
        [
            GrinchRamData(0x0101FB, binary_bit_pos=2)],
    ),
    "WF - Skis": GrinchLocationData(
        "Who Forest",
        ["Sleigh Ride", "Who Forest", "Sleigh Parts"],
        1601,
        [GrinchRamData(0x0101FB, binary_bit_pos=3)],
    ),
    "WD - Tires": GrinchLocationData(
        "Who Dump",
        ["Sleigh Ride", "Who Dump", "Sleigh Parts"],
        1602,
        [GrinchRamData(0x0101FB, binary_bit_pos=4)],
    ),
    "WL - Submarine World - Twin-End Tuba": GrinchLocationData(
        "Submarine World",
        ["Sleigh Ride", "Who Lake", "South Shore", "Sleigh Parts"],
        1603,
        [GrinchRamData(0x0101FB, binary_bit_pos=6)],
    ),
    "WL - South Shore - GPS": GrinchLocationData(
        "Who Lake",
        ["Sleigh Ride", "Who Lake", "Submarine World", "Sleigh Parts"],
        1604,
        [GrinchRamData(0x0101FB, binary_bit_pos=5)],
    ),
    # Mount Crumpit Locations
    "MC - 1st Crate Squashed": GrinchLocationData(
        "Mount Crumpit",
        ["Mount Crumpit"],
        1700,
        [
            GrinchRamData(0x095343, value=1),
            GrinchRamData(0x010000, value=0x05),
        ],
    ),
    "MC - 2nd Crate Squashed": GrinchLocationData(
        "Mount Crumpit",
        ["Mount Crumpit"],
        1701,
        [
            GrinchRamData(0x095343, value=2),
            GrinchRamData(0x010000, value=0x05),
        ],
    ),
    "MC - 3rd Crate Squashed": GrinchLocationData(
        "Mount Crumpit",
        ["Mount Crumpit"],
        1702,
        [
            GrinchRamData(0x095343, value=3),
            GrinchRamData(0x010000, value=0x05),
        ],
    ),
    "MC - 4th Crate Squashed": GrinchLocationData(
        "Mount Crumpit",
        ["Mount Crumpit"],
        1703,
        [
            GrinchRamData(0x095343, value=4),
            GrinchRamData(0x010000, value=0x05),
        ],
    ),
    "MC - 5th Crate Squashed": GrinchLocationData(
        "Mount Crumpit",
        ["Mount Crumpit"],
        1704,
        [
            GrinchRamData(0x095343, value=5),
            GrinchRamData(0x010000, value=0x05),
        ],
    ),
    "MC - Interact with the Telescope": GrinchLocationData(
        "Mount Crumpit",
        ["Mount Crumpit"],
        1705,
        [
            GrinchRamData(0x010111, value=1),
        ],
    ),
    "MC - I hate Whos!": GrinchLocationData(
        "Mount Crumpit",
        ["Mount Crumpit"],
        1706,
        [
            GrinchRamData(0x010111, value=1),
            GrinchRamData(0x0F84E4, value=0x48),
        ],
    ),
    "MC - I hate Christmas!": GrinchLocationData(
        "Mount Crumpit",
        ["Mount Crumpit"],
        1707,
        [
            GrinchRamData(0x010111, value=1),
            GrinchRamData(0x0F84E4, value=0x38),
        ],
    ),
    "MC - My heart is like a pea!": GrinchLocationData(
        "Mount Crumpit",
        ["Mount Crumpit"],
        1708,
        [
            GrinchRamData(0x010111, value=1),
            GrinchRamData(0x0F84E4, value=0x58),
        ],
    ),
    "MC - Move Boulder": GrinchLocationData(
        "Mount Crumpit",
        ["Mount Crumpit"],
        1709,
        [
            GrinchRamData(0x0101FE, binary_bit_pos=1),
        ],
    ),
    "MC - Collect Max Door Key": GrinchLocationData(
        "Mount Crumpit",
        ["Mount Crumpit"],
        1710,
        [
            GrinchRamData(0x0101FE, binary_bit_pos=4),
        ],
    ),
    "MC - Open Door with Breath Analyzer": GrinchLocationData(
        "Mount Crumpit",
        ["Mount Crumpit"],
        1711,
        [
            GrinchRamData(0x0101FE, binary_bit_pos=5),
        ],
    ),
    "MC - Collect Key in Boxes": GrinchLocationData(
        "Mount Crumpit",
        ["Mount Crumpit"],
        1712,
        [
            GrinchRamData(0x0101FE, binary_bit_pos=0),
        ],
    ),
    "WL - Scout's Hut - Steal Scout's Hat": GrinchLocationData(
        "Scout's Hut",
        ["Scout's Hut", "Who Lake", "Miscellaneous"],
        1800,
        [
            GrinchRamData(0x010000, value=0x13),
            # GrinchRamData(0x095349, binary_bit_pos=0),
            GrinchRamData(0x0100BB, binary_bit_pos=0),
        ],
    ),
    "WL - Scout's Hut - Steal Scout's Shirt": GrinchLocationData(
        "Scout's Hut",
        ["Scout's Hut", "Who Lake", "Miscellaneous"],
        1801,
        [
            GrinchRamData(0x010000, value=0x13),
            # GrinchRamData(0x095349, binary_bit_pos=1),
            GrinchRamData(0x0100BB, binary_bit_pos=0),
            GrinchRamData(0x0100BB, binary_bit_pos=1),
        ],
    ),
    "WL - Scout's Hut - Steal Scout's Shorts": GrinchLocationData(
        "Scout's Hut",
        ["Scout's Hut", "Who Lake", "Miscellaneous"],
        1802,
        [
            GrinchRamData(0x010000, value=0x13),
            # GrinchRamData(0x095349, binary_bit_pos=2),
            GrinchRamData(0x0100BB, binary_bit_pos=0),
            GrinchRamData(0x0100BB, binary_bit_pos=1),
        ],
    ),
    "WV - Smashing Snowmen - Next to Vacuum Tube": GrinchLocationData(
        "Whoville",
        ["Whoville's Missions", "Missionsanity", "Whoville"],
        1900,
        [
            GrinchRamData(0x01020C, binary_bit_pos=0),
        ],
    ),
    "WV - Smashing Snowmen - Left Side of Post Office": GrinchLocationData(
        "Whoville",
        ["Whoville's Missions", "Missionsanity", "Whoville"],
        1901,
        [
            GrinchRamData(0x01020C, binary_bit_pos=1),
        ],
    ),
    "WV - Smashing Snowmen - Right Side of Clock Tower": GrinchLocationData(
        "Whoville",
        ["Whoville's Missions", "Missionsanity", "Whoville"],
        1902,
        [
            GrinchRamData(0x01020C, binary_bit_pos=2),
        ],
    ),
    "WV - Smashing Snowmen - Left Side of Clock Tower": GrinchLocationData(
        "Whoville",
        ["Whoville's Missions", "Missionsanity", "Whoville"],
        1903,
        [
            GrinchRamData(0x01020C, binary_bit_pos=3),
        ],
    ),
    "WV - Smashing Snowmen - Between Christmas Tree and Orange Round Building": GrinchLocationData(
        "Whoville",
        ["Whoville's Missions", "Missionsanity", "Whoville"],
        1904,
        [
            GrinchRamData(0x01020C, binary_bit_pos=4),
        ],
    ),
    "WV - Smashing Snowmen - East of Christmas Tree on Platform": GrinchLocationData(
        "Whoville",
        ["Whoville's Missions", "Missionsanity", "Whoville"],
        1905,
        [
            GrinchRamData(0x01020C, binary_bit_pos=5),
        ],
    ),
    "WV - Smashing Snowmen - Near Vacuum Tube on Blue Platform near Orange Bridge": GrinchLocationData(
        "Whoville",
        ["Whoville's Missions", "Missionsanity", "Whoville"],
        1906,
        [
            GrinchRamData(0x01020C, binary_bit_pos=6),
        ],
    ),
    "WV - Smashing Snowmen - Left side of City Hall": GrinchLocationData(
        "Whoville",
        ["Whoville's Missions", "Missionsanity", "Whoville"],
        1907,
        [
            GrinchRamData(0x01020C, binary_bit_pos=7),
        ],
    ),
    "WV - Smashing Snowmen - South of Christmas Tree": GrinchLocationData(
        "Whoville",
        ["Whoville's Missions", "Missionsanity", "Whoville"],
        1908,
        [
            GrinchRamData(0x01020B, binary_bit_pos=6),
        ],
    ),
    "WV - Smashing Snowmen - Right side of City Hall around the back": GrinchLocationData(
        "Whoville",
        ["Whoville's Missions", "Missionsanity", "Whoville"],
        1910,
        [
            GrinchRamData(0x01020B, binary_bit_pos=7),
        ],
    ),
    "WV - Launching Eggs Into Houses - On Gray Building right side of City Hall": GrinchLocationData(
        "Whoville",
        ["Whoville's Missions", "Missionsanity", "Whoville"],
        1911,
        [
            GrinchRamData(0x01020E, binary_bit_pos=2),
        ],
    ),
    "WV - Launching Eggs Into Houses - On Orange Round Building facing Christmas Tree": GrinchLocationData(
        "Whoville",
        ["Whoville's Missions", "Missionsanity", "Whoville"],
        1912,
        [
            GrinchRamData(0x01020E, binary_bit_pos=3),
        ],
    ),
    "WV - Launching Eggs Into Houses - Left side of Snow Wall on Gray Building": GrinchLocationData(
        "Whoville",
        ["Whoville's Missions", "Missionsanity", "Whoville"],
        1913,
        [
            GrinchRamData(0x01020E, binary_bit_pos=4),
        ],
    ),
    "WV - Launching Eggs Into Houses - Above Vacuum Tube": GrinchLocationData(
        "Whoville",
        ["Whoville's Missions", "Missionsanity", "Whoville"],
        1914,
        [
            GrinchRamData(0x01020E, binary_bit_pos=5),
        ],
    ),
    "WV - Launching Eggs Into Houses - Above Child near right side of Post Office": GrinchLocationData(
        "Whoville",
        ["Whoville's Missions", "Missionsanity", "Whoville"],
        1915,
        [
            GrinchRamData(0x01020E, binary_bit_pos=6),
        ],
    ),
    "WV - Launching Eggs Into Houses - On Orange Building right side of City Hall": GrinchLocationData(
        "Whoville",
        ["Whoville's Missions", "Missionsanity", "Whoville"],
        1916,
        [
            GrinchRamData(0x01020E, binary_bit_pos=7),
        ],
    ),
    "WV - Launching Eggs Into Houses - Greenish Building facing Christmas Tree above Child": GrinchLocationData(
        "Whoville",
        ["Whoville's Missions", "Missionsanity", "Whoville"],
        1917,
        [
            GrinchRamData(0x01020F, binary_bit_pos=0),
        ],
    ),
    "WV - Launching Eggs Into Houses - Above Post Office": GrinchLocationData(
        "Whoville",
        ["Whoville's Missions", "Missionsanity", "Whoville"],
        1918,
        [
            GrinchRamData(0x01020F, binary_bit_pos=1),
        ],
    ),
    "WV - Launching Eggs Into Houses - On Skinny Building right side of Clock Tower": GrinchLocationData(
        "Whoville",
        ["Whoville's Missions", "Missionsanity", "Whoville"],
        1919,
        [
            GrinchRamData(0x01020F, binary_bit_pos=2),
        ],
    ),
    "WV - Launching Eggs Into Houses - Orange Building facing away from Vacuum Tube": GrinchLocationData(
        "Whoville",
        ["Whoville's Missions", "Missionsanity", "Whoville"],
        1920,
        [
            GrinchRamData(0x01020F, binary_bit_pos=3),
        ],
    ),
    "WV - Painting The Mayor's Posters - Near Vacuum Tube on right side on Platform": GrinchLocationData(
        "Whoville",
        ["Whoville's Missions", "Missionsanity", "Whoville"],
        1921,
        [
            GrinchRamData(0x01020D, binary_bit_pos=0),
        ],
    ),
    "WV - Painting The Mayor's Posters - Left side of City Hall on Red Building": GrinchLocationData(
        "Whoville",
        ["Whoville's Missions", "Missionsanity", "Whoville"],
        1922,
        [
            GrinchRamData(0x01020D, binary_bit_pos=1),
        ],
    ),
    "WV - Painting The Mayor's Posters - Orange Building in front of Post Office upper level": GrinchLocationData(
        "Whoville",
        ["Whoville's Missions", "Missionsanity", "Whoville"],
        1923,
        [
            GrinchRamData(0x01020D, binary_bit_pos=2),
        ],
    ),
    "WV - Painting The Mayor's Posters - Left side of Post Office on Orange Building left side wall": GrinchLocationData(
        "Whoville",
        ["Whoville's Missions", "Missionsanity", "Whoville"],
        1924,
        [
            GrinchRamData(0x01020D, binary_bit_pos=3),
        ],
    ),
    "WV - Painting The Mayor's Posters - Right side of City Hall on Gray Building Platform": GrinchLocationData(
        "Whoville",
        ["Whoville's Missions", "Missionsanity", "Whoville"],
        1925,
        [
            GrinchRamData(0x01020D, binary_bit_pos=4),
        ],
    ),
    "WV - Painting The Mayor's Posters - Next to Vacuum Tube on left side": GrinchLocationData(
        "Whoville",
        ["Whoville's Missions", "Missionsanity", "Whoville"],
        1926,
        [
            GrinchRamData(0x01020D, binary_bit_pos=5),
        ],
    ),
    "WV - Painting The Mayor's Posters - Right side of Clock Tower on Swinging Platform": GrinchLocationData(
        "Whoville",
        ["Whoville's Missions", "Missionsanity", "Whoville"],
        1927,
        [
            GrinchRamData(0x01020D, binary_bit_pos=6),
        ],
    ),
    "WV - Painting The Mayor's Posters - Orange Building in front of Post Office lower level": GrinchLocationData(
        "Whoville",
        ["Whoville's Missions", "Missionsanity", "Whoville"],
        1928,
        [
            GrinchRamData(0x01020D, binary_bit_pos=7),
        ],
    ),
    "WV - Painting The Mayor's Posters - Left Side of City Hall on Gray Building Platform": GrinchLocationData(
        "Whoville",
        ["Whoville's Missions", "Missionsanity", "Whoville"],
        1929,
        [
            GrinchRamData(0x01020E, binary_bit_pos=0),
        ],
    ),
    "WV - Painting The Mayor's Posters - Right Side of City Hall on Orange Building": GrinchLocationData(
        "Whoville",
        ["Whoville's Missions", "Missionsanity", "Whoville"],
        1930,
        [
            GrinchRamData(0x01020E, binary_bit_pos=1),
        ],
    ),
    "WV - Post Office - Shuffling The Mail - Pink Room (Room 1)": GrinchLocationData(
        "Post Office",
        ["Whoville's Missions", "Missionsanity", "Whoville", "Post Office"],
        1931,
        [
            GrinchRamData(0x010219, binary_bit_pos=0),
            GrinchRamData(0x010219, binary_bit_pos=5),
        ],
    ),
    "WV - Post Office - Shuffling The Mail - Orange Room (Room 2)": GrinchLocationData(
        "Post Office",
        ["Whoville's Missions", "Missionsanity", "Whoville", "Post Office"],
        1932,
        [
            GrinchRamData(0x010219, binary_bit_pos=1),
            GrinchRamData(0x010219, binary_bit_pos=6),
        ],
    ),
    "WV - Post Office - Shuffling The Mail - Blue Room (Room 3)": GrinchLocationData(
        "Post Office",
        ["Whoville's Missions", "Missionsanity", "Whoville", "Post Office"],
        1933,
        [
            GrinchRamData(0x010219, binary_bit_pos=7),
        ],
    ),
    "WV - Post Office - Shuffling The Mail - Yellow Room (Room 4)": GrinchLocationData(
        "Post Office",
        ["Whoville's Missions", "Missionsanity", "Whoville", "Post Office"],
        1934,
        [
            GrinchRamData(0x010219, binary_bit_pos=3),
        ],
    ),
    "WV - Post Office - Shuffling The Mail - Gray Room (Room 5)": GrinchLocationData(
        "Post Office",
        ["Whoville's Missions", "Missionsanity", "Whoville", "Post Office"],
        1935,
        [
            GrinchRamData(0x01021A, binary_bit_pos=1),
        ],
    ),
    "WV - Clock Tower - Open Hatch to Floor 2": GrinchLocationData(
        "Clock Tower",
        ["Whoville", "Clock Tower", "Doorsanity", "Miscellaneous"],
        1936,
        [
            GrinchRamData(0x0100D9, binary_bit_pos=1),
            GrinchRamData(0x0100DA, binary_bit_pos=1),
        ],
    ),
    "WV - Clock Tower - Open Hatch to Floor 3": GrinchLocationData(
        "Clock Tower",
        ["Whoville", "Clock Tower", "Doorsanity", "Miscellaneous"],
        1937,
        [
            GrinchRamData(0x0100D9, binary_bit_pos=2),
            GrinchRamData(0x0100DA, binary_bit_pos=2),
        ],
    ),
    "WV - Clock Tower - Open Hatch to Floor 4": GrinchLocationData(
        "Clock Tower",
        ["Whoville", "Clock Tower", "Doorsanity", "Miscellaneous"],
        1938,
        [
            GrinchRamData(0x0100D9, binary_bit_pos=3),
            GrinchRamData(0x0100DA, binary_bit_pos=3),
        ],
    ),
    "WV - Clock Tower - Open Hatch to Floor 5": GrinchLocationData(
        "Clock Tower",
        ["Whoville", "Clock Tower", "Doorsanity", "Miscellaneous"],
        1939,
        [
            GrinchRamData(0x0100D9, binary_bit_pos=4),
            GrinchRamData(0x0100DA, binary_bit_pos=4),
        ],
    ),
    "WV - Clock Tower - Ring 1st Bell": GrinchLocationData(
        "Clock Tower",
        ["Whoville", "Clock Tower", "Bellsanity", "Miscellaneous"],
        1940,
        [
            GrinchRamData(0x010000, value=0x09),
            GrinchRamData(0x09534A, value=2),
        ],
    ),
    "WV - Clock Tower - Ring 2nd Bell": GrinchLocationData(
        "Clock Tower",
        ["Whoville", "Clock Tower", "Bellsanity", "Miscellaneous"],
        1941,
        [
            GrinchRamData(0x010000, value=0x09),
            GrinchRamData(0x09534A, value=3),
        ],
    ),
    "WV - Clock Tower - Ring 3rd Bell": GrinchLocationData(
        "Clock Tower",
        ["Whoville", "Clock Tower", "Bellsanity", "Miscellaneous"],
        1942,
        [
            GrinchRamData(0x010000, value=0x09),
            GrinchRamData(0x09534A, value=4),
        ],
    ),
    "WV - Clock Tower - Ring 4th Bell": GrinchLocationData(
        "Clock Tower",
        ["Whoville", "Clock Tower", "Bellsanity", "Miscellaneous"],
        1943,
        [
            GrinchRamData(0x010000, value=0x09),
            GrinchRamData(0x09534A, value=5),
        ],
    ),
    "WV - Clock Tower - Ring 5th Bell": GrinchLocationData(
        "Clock Tower",
        ["Whoville", "Clock Tower", "Bellsanity", "Miscellaneous"],
        1944,
        [
            GrinchRamData(0x010000, value=0x09),
            GrinchRamData(0x09534A, value=7),
        ],
    ),
    "WF - Making Xmas Trees Droop - Swinging platform farthest to Glue Cannon": GrinchLocationData(
        "Who Forest",
        ["Who Forest's Missions", "Missionsanity", "Who Forest"],
        2000,
        [
            GrinchRamData(0x010240, binary_bit_pos=7),
        ],
    ),
    "WF - Making Xmas Trees Droop - 2nd closest to Civic Center cave": GrinchLocationData(
        "Who Forest",
        ["Who Forest's Missions", "Missionsanity", "Who Forest"],
        2001,
        [
            GrinchRamData(0x010242, binary_bit_pos=0),
        ],
    ),
    "WF - Making Xmas Trees Droop - Swinging platform closest to Glue Cannon": GrinchLocationData(
        "Who Forest",
        ["Who Forest's Missions", "Missionsanity", "Who Forest"],
        2002,
        [
            GrinchRamData(0x010241, binary_bit_pos=0),
        ],
    ),
    "WF - Making Xmas Trees Droop - Next to Tree house": GrinchLocationData(
        "Who Forest",
        ["Who Forest's Missions", "Missionsanity", "Who Forest"],
        2003,
        [
            GrinchRamData(0x010241, binary_bit_pos=1),
        ],
    ),
    "WF - Making Xmas Trees Droop - Closest to Civic Center cave": GrinchLocationData(
        "Who Forest",
        ["Who Forest's Missions", "Missionsanity", "Who Forest"],
        2004,
        [
            GrinchRamData(0x010241, binary_bit_pos=2),
        ],
    ),
    "WF - Making Xmas Trees Droop - Tree 3rd closest to vacuum tube": GrinchLocationData(
        "Who Forest",
        ["Who Forest's Missions", "Missionsanity", "Who Forest"],
        2005,
        [
            GrinchRamData(0x010241, binary_bit_pos=3),
        ],
    ),
    "WF - Making Xmas Trees Droop - Tree 2nd closest to vacuum tube": GrinchLocationData(
        "Who Forest",
        ["Who Forest's Missions", "Missionsanity", "Who Forest"],
        2006,
        [
            GrinchRamData(0x010241, binary_bit_pos=4),
        ],
    ),
    "WF - Making Xmas Trees Droop - Tree closest to vacuum tube": GrinchLocationData(
        "Who Forest",
        ["Who Forest's Missions", "Missionsanity", "Who Forest"],
        2007,
        [
            GrinchRamData(0x010241, binary_bit_pos=5),
        ],
    ),
    "WF - Making Xmas Trees Droop - Tree 4th closest to vacuum tube": GrinchLocationData(
        "Who Forest",
        ["Who Forest's Missions", "Missionsanity", "Who Forest"],
        2008,
        [
            GrinchRamData(0x010241, binary_bit_pos=6),
        ],
    ),
    "WF - Making Xmas Trees Droop - Left of cable car": GrinchLocationData(
        "Who Forest",
        ["Who Forest's Missions", "Missionsanity", "Who Forest"],
        2009,
        [
            GrinchRamData(0x010241, binary_bit_pos=7),
        ],
    ),
    "WF - Putting Beehives In Cabins - Closest to Vacuum Tube": GrinchLocationData(
        "Who Forest",
        ["Who Forest's Missions", "Missionsanity", "Who Forest"],
        2010,
        [
            GrinchRamData(0x010245, binary_bit_pos=1),
        ],
    ),
    "WF - Putting Beehives In Cabins - Red house on glue cannon platform": GrinchLocationData(
        "Who Forest",
        ["Who Forest's Missions", "Missionsanity", "Who Forest"],
        2011,
        [
            GrinchRamData(0x010245, binary_bit_pos=2),
        ],
    ),
    "WF - Putting Beehives In Cabins - Green house on glue cannon platform": GrinchLocationData(
        "Who Forest",
        ["Who Forest's Missions", "Missionsanity", "Who Forest"],
        2012,
        [
            GrinchRamData(0x010245, binary_bit_pos=3),
        ],
    ),
    "WF - Putting Beehives In Cabins - 2nd closest to vacuum tube": GrinchLocationData(
        "Who Forest",
        ["Who Forest's Missions", "Missionsanity", "Who Forest"],
        2013,
        [
            GrinchRamData(0x010245, binary_bit_pos=4),
        ],
    ),
    "WF - Putting Beehives In Cabins - Yellow house across from Tree House": GrinchLocationData(
        "Who Forest",
        ["Who Forest's Missions", "Missionsanity", "Who Forest"],
        2014,
        [
            GrinchRamData(0x010245, binary_bit_pos=5),
        ],
    ),
    "WF - Putting Beehives In Cabins - Red house next to Tree House": GrinchLocationData(
        "Who Forest",
        ["Who Forest's Missions", "Missionsanity", "Who Forest"],
        2015,
        [
            GrinchRamData(0x010245, binary_bit_pos=6),
        ],
    ),
    "WF - Putting Beehives In Cabins - Tree house": GrinchLocationData(
        "Who Forest",
        ["Who Forest's Missions", "Missionsanity", "Who Forest"],
        2016,
        [
            GrinchRamData(0x010245, binary_bit_pos=7),
        ],
    ),
    "WF - Putting Beehives In Cabins - Red house near Cable car": GrinchLocationData(
        "Who Forest",
        ["Who Forest's Missions", "Missionsanity", "Who Forest"],
        2017,
        [
            GrinchRamData(0x010246, binary_bit_pos=0),
        ],
    ),
    "WF - Putting Beehives In Cabins - Blue house in front of civic center cave": GrinchLocationData(
        "Who Forest",
        ["Who Forest's Missions", "Missionsanity", "Who Forest"],
        2018,
        [
            GrinchRamData(0x010246, binary_bit_pos=1),
        ],
    ),
    "WF - Putting Beehives In Cabins - Green house left side of Cable car": GrinchLocationData(
        "Who Forest",
        ["Who Forest's Missions", "Missionsanity", "Who Forest"],
        2019,
        [
            GrinchRamData(0x010246, binary_bit_pos=2),
        ],
    ),
    "WF - Civic Center - Replacing The Candles On The Cake With Fireworks - Front side of Civic Center building": GrinchLocationData(
        "Civic Center",
        ["Who Forest's Missions", "Missionsanity", "Who Forest", "Civic Center"],
        2020,
        [
            GrinchRamData(0x01022C, binary_bit_pos=6),
        ],
    ),
    "WF - Civic Center - Replacing The Candles On The Cake With Fireworks - Left side of Civic Center building": GrinchLocationData(
        "Civic Center",
        ["Who Forest's Missions", "Missionsanity", "Who Forest", "Civic Center"],
        2021,
        [
            GrinchRamData(0x01022C, binary_bit_pos=7),
        ],
    ),
    "WF - Civic Center - Replacing The Candles On The Cake With Fireworks - Across tree branch swinging platform": GrinchLocationData(
        "Civic Center",
        ["Who Forest's Missions", "Missionsanity", "Who Forest", "Civic Center"],
        2022,
        [
            GrinchRamData(0x01022D, binary_bit_pos=0),
        ],
    ),
    "WF - Civic Center - Replacing The Candles On The Cake With Fireworks - Middle platform of super toy parkour": GrinchLocationData(
        "Civic Center",
        ["Who Forest's Missions", "Missionsanity", "Who Forest", "Civic Center"],
        2023,
        [
            GrinchRamData(0x01022D, binary_bit_pos=1),
        ],
    ),
    "WF - Civic Center - Replacing The Candles On The Cake With Fireworks - Front of Bat Cave entrance": GrinchLocationData(
        "Civic Center",
        ["Who Forest's Missions", "Missionsanity", "Who Forest", "Civic Center"],
        2024,
        [
            GrinchRamData(0x01022D, binary_bit_pos=2),
        ],
    ),
    "WF - Civic Center - Replacing The Candles On The Cake With Fireworks - Guarded by who below super toy platforms": GrinchLocationData(
        "Civic Center",
        ["Who Forest's Missions", "Missionsanity", "Who Forest", "Civic Center"],
        2025,
        [
            GrinchRamData(0x01022D, binary_bit_pos=3),
        ],
    ),
    "WF - Civic Center - Replacing The Candles On The Cake With Fireworks - Furthest platform of super toy parkour": GrinchLocationData(
        "Civic Center",
        ["Who Forest's Missions", "Missionsanity", "Who Forest", "Civic Center"],
        2026,
        [
            GrinchRamData(0x01022D, binary_bit_pos=4),
        ],
    ),
    "WF - Civic Center - Replacing The Candles On The Cake With Fireworks - Across snow boulders": GrinchLocationData(
        "Civic Center",
        ["Who Forest's Missions", "Missionsanity", "Who Forest", "Civic Center"],
        2027,
        [
            GrinchRamData(0x01022D, binary_bit_pos=5),
        ],
    ),
    "WF - Civic Center - Replacing The Candles On The Cake With Fireworks - After ice wall near entrance left side": GrinchLocationData(
        "Civic Center",
        ["Who Forest's Missions", "Missionsanity", "Who Forest", "Civic Center"],
        2028,
        [
            GrinchRamData(0x01022D, binary_bit_pos=6),
        ],
    ),
    "WF - Civic Center - Replacing The Candles On The Cake With Fireworks - Across bridge near entrance": GrinchLocationData(
        "Civic Center",
        ["Who Forest's Missions", "Missionsanity", "Who Forest", "Civic Center"],
        2029,
        [
            GrinchRamData(0x01022D, binary_bit_pos=7),
        ],
    ),
    "WD - Feeding The Computer With Robot Parts - Left side of center area": GrinchLocationData(
        "Who Dump",
        ["Who Dump's Missions", "Missionsanity", "Who Dump"],
        2101,
        [
            GrinchRamData(0x010255, binary_bit_pos=2),
        ],
    ),
    "WD - Feeding The Computer With Robot Parts - Center area between pipes": GrinchLocationData(
        "Who Dump",
        ["Who Dump's Missions", "Missionsanity", "Who Dump"],
        2102,
        [
            GrinchRamData(0x010255, binary_bit_pos=3),
        ],
    ),
    "WD - Feeding The Computer With Robot Parts - Right side of center area": GrinchLocationData(
        "Who Dump",
        ["Who Dump's Missions", "Missionsanity", "Who Dump"],
        2103,
        [
            GrinchRamData(0x010255, binary_bit_pos=4),
        ],
    ),
    "WD - Feeding The Computer With Robot Parts - Who Bris Shack Area": GrinchLocationData(
        "Who Dump",
        ["Who Dump's Missions", "Missionsanity", "Who Dump"],
        2104,
        [
            GrinchRamData(0x010255, binary_bit_pos=5),
        ],
    ),
    "WD - Feeding The Computer With Robot Parts - Right area near robot parts vacuum": GrinchLocationData(
        "Who Dump",
        ["Who Dump's Missions", "Missionsanity", "Who Dump"],
        2105,
        [
            GrinchRamData(0x010255, binary_bit_pos=6),
        ],
    ),
    "WD - Feeding The Computer With Robot Parts - Right area near entrance to center area": GrinchLocationData(
        "Who Dump",
        ["Who Dump's Missions", "Missionsanity", "Who Dump"],
        2106,
        [
            GrinchRamData(0x010255, binary_bit_pos=7),
        ],
    ),
    "WD - Feeding The Computer With Robot Parts - Right area near shooting pipe": GrinchLocationData(
        "Who Dump",
        ["Who Dump's Missions", "Missionsanity", "Who Dump"],
        2107,
        [
            GrinchRamData(0x010256, binary_bit_pos=0),
        ],
    ),
    "WD - Feeding The Computer With Robot Parts - Near inward pipe in left area": GrinchLocationData(
        "Who Dump",
        ["Who Dump's Missions", "Missionsanity", "Who Dump"],
        2108,
        [
            GrinchRamData(0x010256, binary_bit_pos=1),
        ],
    ),
    "WD - Feeding The Computer With Robot Parts - Left area on right electric fence": GrinchLocationData(
        "Who Dump",
        ["Who Dump's Missions", "Missionsanity", "Who Dump"],
        2109,
        [
            GrinchRamData(0x010256, binary_bit_pos=2),
        ],
    ),
    "WD - Feeding The Computer With Robot Parts - Left area on left electric fence": GrinchLocationData(
        "Who Dump",
        ["Who Dump's Missions", "Missionsanity", "Who Dump"],
        2110,
        [
            GrinchRamData(0x010256, binary_bit_pos=3),
        ],
    ),
    "WD - Conducting The Stinky Gas To Who-Bris' Shack - Swinging pipe in right side of center area": GrinchLocationData(
        "Who Dump",
        ["Who Dump's Missions", "Missionsanity", "Who Dump"],
        2111,
        [
            GrinchRamData(0x010257, binary_bit_pos=4),
        ],
    ),
    "WD - Conducting The Stinky Gas To Who-Bris' Shack - Swinging pipe in left side of center area": GrinchLocationData(
        "Who Dump",
        ["Who Dump's Missions", "Missionsanity", "Who Dump"],
        2112,
        [
            GrinchRamData(0x010257, binary_bit_pos=5),
        ],
    ),
    "WD - Conducting The Stinky Gas To Who-Bris' Shack - Shooting pipe in left area": GrinchLocationData(
        "Who Dump",
        ["Who Dump's Missions", "Missionsanity", "Who Dump"],
        2113,
        [
            GrinchRamData(0x010257, binary_bit_pos=6),
        ],
    ),
    "WD - Conducting The Stinky Gas To Who-Bris' Shack - Swinging pipe in left area": GrinchLocationData(
        "Who Dump",
        ["Who Dump's Missions", "Missionsanity", "Who Dump"],
        2114,
        [
            GrinchRamData(0x010257, binary_bit_pos=7),
        ],
    ),
    "WD - Conducting The Stinky Gas To Who-Bris' Shack - Shooting pipe in right side": GrinchLocationData(
        "Who Dump",
        ["Who Dump's Missions", "Missionsanity", "Who Dump"],
        2115,
        [
            GrinchRamData(0x010258, binary_bit_pos=1),
        ],
    ),
    "WD - Conducting The Stinky Gas To Who-Bris' Shack - Seizing pipe in rat area": GrinchLocationData(
        "Who Dump",
        ["Who Dump's Missions", "Missionsanity", "Who Dump"],
        2116,
        [
            GrinchRamData(0x010258, binary_bit_pos=2),
        ],
    ),
    "WD - Conducting The Stinky Gas To Who-Bris' Shack - Shooting pipe in right side inside pipe": GrinchLocationData(
        "Who Dump",
        ["Who Dump's Missions", "Missionsanity", "Who Dump"],
        2117,
        [
            GrinchRamData(0x010258, binary_bit_pos=3),
        ],
    ),
    "WD - Conducting The Stinky Gas To Who-Bris' Shack - Swinging pipe in center area pipe": GrinchLocationData(
        "Who Dump",
        ["Who Dump's Missions", "Missionsanity", "Who Dump"],
        2118,
        [
            GrinchRamData(0x010258, binary_bit_pos=4),
        ],
    ),
    "WD - Conducting The Stinky Gas To Who-Bris' Shack - Swinging pipe in left area pipe": GrinchLocationData(
        "Who Dump",
        ["Who Dump's Missions", "Missionsanity", "Who Dump"],
        2119,
        [
            GrinchRamData(0x010258, binary_bit_pos=5),
        ],
    ),
    "WD - Conducting The Stinky Gas To Who-Bris' Shack - Final pipe screw in Who Bris' Shack area": GrinchLocationData(
        "Who Dump",
        ["Who Dump's Missions", "Missionsanity", "Who Dump"],
        2120,
        [
            GrinchRamData(0x010258, binary_bit_pos=0),
            GrinchRamData(0x010258, binary_bit_pos=6),
        ],
    ),
    "WD - Infesting The Mayor's House With Rats - Rat 1": GrinchLocationData(
        "Who Dump",
        ["Who Dump's Missions", "Missionsanity", "Who Dump"],
        2121,
        [
            # GrinchRamData(0x0100FE, value=1),
            GrinchRamData(0x010258, binary_bit_pos=7),
        ],
    ),
    "WD - Infesting The Mayor's House With Rats - Rat 2": GrinchLocationData(
        "Who Dump",
        ["Who Dump's Missions", "Missionsanity", "Who Dump"],
        2122,
        [
            # GrinchRamData(0x0100FE, value=2),
            GrinchRamData(0x010259, binary_bit_pos=0),
        ],
    ),
    "WD - Infesting The Mayor's House With Rats - Rat 3": GrinchLocationData(
        "Who Dump",
        ["Who Dump's Missions", "Missionsanity", "Who Dump"],
        2123,
        [
            # GrinchRamData(0x0100FE, value=3),
            GrinchRamData(0x010259, binary_bit_pos=1),
        ],
    ),
    "WD - Infesting The Mayor's House With Rats - Rat 4": GrinchLocationData(
        "Who Dump",
        ["Who Dump's Missions", "Missionsanity", "Who Dump"],
        2124,
        [
            # GrinchRamData(0x0100FE, value=4),
            GrinchRamData(0x010259, binary_bit_pos=2),
        ],
    ),
    "WD - Infesting The Mayor's House With Rats - Rat 5": GrinchLocationData(
        "Who Dump",
        ["Who Dump's Missions", "Missionsanity", "Who Dump"],
        2125,
        [
            # GrinchRamData(0x0100FE, value=5),
            GrinchRamData(0x010259, binary_bit_pos=3),
        ],
    ),
    "WD - Infesting The Mayor's House With Rats - Rat 6": GrinchLocationData(
        "Who Dump",
        ["Who Dump's Missions", "Missionsanity", "Who Dump"],
        2126,
        [
            # GrinchRamData(0x0100FE, value=6),
            GrinchRamData(0x010259, binary_bit_pos=4),
        ],
    ),
    "WD - Infesting The Mayor's House With Rats - Rat 7": GrinchLocationData(
        "Who Dump",
        ["Who Dump's Missions", "Missionsanity", "Who Dump"],
        2127,
        [
            # GrinchRamData(0x0100FE, value=7),
            GrinchRamData(0x010259, binary_bit_pos=5),
        ],
    ),
    "WD - Infesting The Mayor's House With Rats - Rat 8": GrinchLocationData(
        "Who Dump",
        ["Who Dump's Missions", "Missionsanity", "Who Dump"],
        2128,
        [
            # GrinchRamData(0x0100FE, value=8),
            GrinchRamData(0x010259, binary_bit_pos=6),
        ],
    ),
    "WD - Infesting The Mayor's House With Rats - Rat 9": GrinchLocationData(
        "Who Dump",
        ["Who Dump's Missions", "Missionsanity", "Who Dump"],
        2129,
        [
            # GrinchRamData(0x0100FE, value=9),
            GrinchRamData(0x010259, binary_bit_pos=7),
        ],
    ),
    "WD - Infesting The Mayor's House With Rats - Rat 10": GrinchLocationData(
        "Who Dump",
        ["Who Dump's Missions", "Missionsanity", "Who Dump"],
        2130,
        [
            # GrinchRamData(0x0100FE, value=10),
            GrinchRamData(0x01025A, binary_bit_pos=0),
        ],
    ),
    "WD - Stealing Food From Birds - Left area on right electric fence": GrinchLocationData(
        "Who Dump",
        ["Who Dump's Missions", "Missionsanity", "Who Dump"],
        2131,
        [
            GrinchRamData(0x010253, binary_bit_pos=0),
        ],
    ),
    "WD - Stealing Food From Birds - Right area near Minefield entrance": GrinchLocationData(
        "Who Dump",
        ["Who Dump's Missions", "Missionsanity", "Who Dump"],
        2132,
        [
            GrinchRamData(0x010253, binary_bit_pos=1),
        ],
    ),
    "WD - Stealing Food From Birds - Who Bris Shack Area": GrinchLocationData(
        "Who Dump",
        ["Who Dump's Missions", "Missionsanity", "Who Dump"],
        2133,
        [
            GrinchRamData(0x010253, binary_bit_pos=2),
        ],
    ),
    "WD - Stealing Food From Birds - Shooting pipe near right area": GrinchLocationData(
        "Who Dump",
        ["Who Dump's Missions", "Missionsanity", "Who Dump"],
        2134,
        [
            GrinchRamData(0x010253, binary_bit_pos=3),
        ],
    ),
    "WD - Stealing Food From Birds - Right area in rat section": GrinchLocationData(
        "Who Dump",
        ["Who Dump's Missions", "Missionsanity", "Who Dump"],
        2135,
        [
            GrinchRamData(0x010253, binary_bit_pos=4),
        ],
    ),
    "WD - Stealing Food From Birds - Left area near inward pipe": GrinchLocationData(
        "Who Dump",
        ["Who Dump's Missions", "Missionsanity", "Who Dump"],
        2136,
        [
            GrinchRamData(0x010253, binary_bit_pos=5),
        ],
    ),
    "WD - Stealing Food From Birds - Left area on left electric fence": GrinchLocationData(
        "Who Dump",
        ["Who Dump's Missions", "Missionsanity", "Who Dump"],
        2137,
        [
            GrinchRamData(0x010253, binary_bit_pos=6),
        ],
    ),
    "WD - Stealing Food From Birds - Left area below spinning pipe near blue tube": GrinchLocationData(
        "Who Dump",
        ["Who Dump's Missions", "Missionsanity", "Who Dump"],
        2138,
        [
            GrinchRamData(0x010253, binary_bit_pos=7),
        ],
    ),
    "WD - Stealing Food From Birds - Near blue tube in center area": GrinchLocationData(
        "Who Dump",
        ["Who Dump's Missions", "Missionsanity", "Who Dump"],
        2139,
        [
            GrinchRamData(0x010252, binary_bit_pos=6),
        ],
    ),
    "WD - Stealing Food From Birds - TV Platform": GrinchLocationData(
        "Who Dump",
        ["Who Dump's Missions", "Missionsanity", "Who Dump"],
        2140,
        [
            GrinchRamData(0x010252, binary_bit_pos=7),
        ],
    ),
    "WD - Generator Building - Short-Circuiting Power-Plant - Yellow Generator (4th)": GrinchLocationData(
        "Generator Building",
        ["Who Dump's Missions", "Missionsanity", "Who Dump"],
        2141,
        [
            GrinchRamData(0x0100DF, binary_bit_pos=3),
        ],
    ),
    "WD - Generator Building - Short-Circuiting Power-Plant - Orange Generator (3rd)": GrinchLocationData(
        "Generator Building",
        ["Who Dump's Missions", "Missionsanity", "Who Dump"],
        2142,
        [
            GrinchRamData(0x0100DF, binary_bit_pos=2),
        ],
    ),
    "WD - Generator Building - Short-Circuiting Power-Plant - Pink Generator (2nd)": GrinchLocationData(
        "Generator Building",
        ["Who Dump's Missions", "Missionsanity", "Who Dump"],
        2143,
        [
            GrinchRamData(0x0100DF, binary_bit_pos=1),
        ],
    ),
    "WD - Generator Building - Short-Circuiting Power-Plant - Blue Generator (1st)": GrinchLocationData(
        "Generator Building",
        ["Who Dump's Missions", "Missionsanity", "Who Dump"],
        2144,
        [
            GrinchRamData(0x0100DF, binary_bit_pos=0),
        ],
    ),
    "WL - South Shore - Sabotaging The Tents - Right side of bridge to Scout Hut": GrinchLocationData(
        "Who Lake",
        [
        "Who Lake Missions",
        "Missionsanity",
        "Who Lake",
        "South Shore",
        "South Shore Missions",
        ],
        2200,
        [
            GrinchRamData(0x010280, binary_bit_pos=0),
        ],
    ),
    "WL - South Shore - Sabotaging The Tents - Left side of summer beast": GrinchLocationData(
        "Who Lake",
        [
            "Who Lake Missions",
            "Missionsanity",
            "Who Lake",
            "South Shore",
            "South Shore Missions",
        ],
        2201,
        [
            GrinchRamData(0x010280, binary_bit_pos=1),
        ],
    ),
    "WL - South Shore - Sabotaging The Tents - Across from boulder": GrinchLocationData(
        "Who Lake",
        [
            "Who Lake Missions",
            "Missionsanity",
            "Who Lake",
            "South Shore",
            "South Shore Missions",
        ],
        2202,
        [
            GrinchRamData(0x010280, binary_bit_pos=2),
        ],
    ),
    "WL - South Shore - Sabotaging The Tents - Grass platform": GrinchLocationData(
        "Who Lake",
        [
            "Who Lake Missions",
            "Missionsanity",
            "Who Lake",
            "South Shore",
            "South Shore Missions",
        ],
        2203,
        [
            GrinchRamData(0x010280, binary_bit_pos=3),
        ],
    ),
    "WL - South Shore - Sabotaging The Tents - Left side of bridge right of rope wall": GrinchLocationData(
        "Who Lake",
        [
            "Who Lake Missions",
            "Missionsanity",
            "Who Lake",
            "South Shore",
            "South Shore Missionsanity",
        ],
        2204,
        [
            GrinchRamData(0x010280, binary_bit_pos=4),
        ],
    ),
    "WL - South Shore - Sabotaging The Tents - Right side of summer beast": GrinchLocationData(
        "Who Lake",
        [
            "Who Lake Missions",
            "Missionsanity",
            "Who Lake",
            "South Shore",
            "South Shore Missions",
        ],
        2205,
        [
            GrinchRamData(0x010280, binary_bit_pos=5),
        ],
    ),
    "WL - South Shore - Sabotaging The Tents - Across from clothes line": GrinchLocationData(
        "Who Lake",
        [
            "Who Lake Missions",
            "Missionsanity",
            "Who Lake",
            "South Shore",
            "South Shore Missions",
        ],
        2206,
        [
            GrinchRamData(0x010280, binary_bit_pos=6),
        ],
    ),
    "WL - South Shore - Sabotaging The Tents - Across swinging line": GrinchLocationData(
        "Who Lake",
        [
            "Who Lake Missions",
            "Missionsanity",
            "Who Lake",
            "South Shore",
            "South Shore Missions",
        ],
        2207,
        [
            GrinchRamData(0x010280, binary_bit_pos=7),
        ],
    ),
    "WL - South Shore - Sabotaging The Tents - Across from clothes line near North Shore bridge": GrinchLocationData(
        "Who Lake",
        [
            "Who Lake Missions",
            "Missionsanity",
            "Who Lake",
            "South Shore",
            "South Shore Missions",
        ],
        2208,
        [
            GrinchRamData(0x010281, binary_bit_pos=0),
        ],
    ),
    "WL - South Shore - Sabotaging The Tents - Left of North Shore bridge": GrinchLocationData(
        "Who Lake",
        [
            "Who Lake Missions",
            "Missionsanity",
            "Who Lake",
            "South Shore",
            "South Shore Missions",
        ],
        2209,
        [
            GrinchRamData(0x010281, binary_bit_pos=1),
        ],
    ),
    "WL - South Shore - Putting Thistles In Shorts - Left of rack guarded by child": GrinchLocationData(
        "Who Lake",
        [
            "Who Lake Missions",
            "Missionsanity",
            "Who Lake",
            "South Shore",
            "South Shore Missions",
        ],
        2210,
        [
            GrinchRamData(0x01027F, binary_bit_pos=0),
        ],
    ),
    "WL - South Shore - Putting Thistles In Shorts - Left of rack near entrance": GrinchLocationData(
        "Who Lake",
        [
            "Who Lake Missions",
            "Missionsanity",
            "Who Lake",
            "South Shore",
            "South Shore Missions",
        ],
        2211,
        [
            GrinchRamData(0x01027F, binary_bit_pos=1),
        ],
    ),
    "WL - South Shore - Putting Thistles In Shorts - Middle of rack near entrance": GrinchLocationData(
        "Who Lake",
        [
            "Who Lake Missions",
            "Missionsanity",
            "Who Lake",
            "South Shore",
            "South Shore Missions",
        ],
        2212,
        [
            GrinchRamData(0x01027F, binary_bit_pos=2),
        ],
    ),
    "WL - South Shore - Putting Thistles In Shorts - Right of rack near entrance": GrinchLocationData(
        "Who Lake",
        [
            "Who Lake Missions",
            "Missionsanity",
            "Who Lake",
            "South Shore",
            "South Shore Missions",
        ],
        2213,
        [
            GrinchRamData(0x01027F, binary_bit_pos=3),
        ],
    ),
    "WL - South Shore - Putting Thistles In Shorts - Left of rack on wall platform": GrinchLocationData(
        "Who Lake",
        [
            "Who Lake Missions",
            "Missionsanity",
            "Who Lake",
            "South Shore",
            "South Shore Missions",
        ],
        2214,
        [
            GrinchRamData(0x01027F, binary_bit_pos=4),
        ],
    ),
    "WL - South Shore - Putting Thistles In Shorts - Right of rack on wall platform": GrinchLocationData(
        "Who Lake",
        [
            "Who Lake Missions",
            "Missionsanity",
            "Who Lake",
            "South Shore",
            "South Shore Missions",
        ],
        2215,
        [
            GrinchRamData(0x01027F, binary_bit_pos=5),
        ],
    ),
    "WL - South Shore - Putting Thistles In Shorts - Right of rack near North Shore Bridge": GrinchLocationData(
        "Who Lake",
        [
            "Who Lake Missions",
            "Missionsanity",
            "Who Lake",
            "South Shore",
            "South Shore Missions",
        ],
        2216,
        [
            GrinchRamData(0x01027F, binary_bit_pos=6),
        ],
    ),
    "WL - South Shore - Putting Thistles In Shorts - Left of rack near North Shore Bridge": GrinchLocationData(
        "Who Lake",
        [
            "Who Lake Missions",
            "Missionsanity",
            "Who Lake",
            "South Shore",
            "South Shore Missions",
        ],
        2217,
        [
            GrinchRamData(0x01027F, binary_bit_pos=7),
        ],
    ),
    "WL - South Shore - Putting Thistles In Shorts - Right of rack guarded by child": GrinchLocationData(
        "Who Lake",
        [
            "Who Lake Missions",
            "Missionsanity",
            "Who Lake",
            "South Shore",
            "South Shore Missions",
        ],
        2218,
        [
            GrinchRamData(0x01027E, binary_bit_pos=6),
        ],
    ),
    "WL - South Shore - Putting Thistles In Shorts - Middle of rack guarded by child": GrinchLocationData(
        "Who Lake",
        [
            "Who Lake Missions",
            "Missionsanity",
            "Who Lake",
            "South Shore",
            "South Shore Missions",
        ],
        2219,
        [
            GrinchRamData(0x01027E, binary_bit_pos=7),
        ],
    ),
    "WL - North Shore - Drilling Holes In Canoes - Right side adjacent to fence area": GrinchLocationData(
        "North Shore",
        [
            "Who Lake Missions",
            "Missionsanity",
            "Who Lake",
            "North Shore",
            "North Shore Missions",
        ],
        2220,
        [
            GrinchRamData(0x010294, binary_bit_pos=0),
        ],
    ),
    "WL - North Shore - Drilling Holes In Canoes - Left side adjacent to fence area": GrinchLocationData(
        "North Shore",
        [
            "Who Lake Missions",
            "Missionsanity",
            "Who Lake",
            "North Shore",
            "North Shore Missions",
        ],
        2221,
        [
            GrinchRamData(0x010294, binary_bit_pos=1),
        ],
    ),
    "WL - North Shore - Drilling Holes In Canoes - Left side in fence area": GrinchLocationData(
        "North Shore",
        [
            "Who Lake Missions",
            "Missionsanity",
            "Who Lake",
            "North Shore",
            "North Shore Missions",
        ],
        2222,
        [
            GrinchRamData(0x010294, binary_bit_pos=2),
        ],
    ),
    "WL - North Shore - Drilling Holes In Canoes - Right side in fence area": GrinchLocationData(
        "North Shore",
        [
            "Who Lake Missions",
            "Missionsanity",
            "Who Lake",
            "North Shore",
            "North Shore Missions",
        ],
        2223,
        [
            GrinchRamData(0x010294, binary_bit_pos=3),
        ],
    ),
    "WL - North Shore - Drilling Holes In Canoes - On beach left side below max house": GrinchLocationData(
        "North Shore",
        [
            "Who Lake Missions",
            "Missionsanity",
            "Who Lake",
            "North Shore",
            "North Shore Missions",
        ],
        2224,
        [
            GrinchRamData(0x010294, binary_bit_pos=4),
        ],
    ),
    "WL - North Shore - Drilling Holes In Canoes - On beach right side below max house": GrinchLocationData(
        "North Shore",
        [
            "Who Lake Missions",
            "Missionsanity",
            "Who Lake",
            "North Shore",
            "North Shore Missions",
        ],
        2225,
        [
            GrinchRamData(0x010294, binary_bit_pos=5),
        ],
    ),
    "WL - North Shore - Drilling Holes In Canoes - Middle side in fence area": GrinchLocationData(
        "North Shore",
        [
            "Who Lake Missions",
            "Missionsanity",
            "Who Lake",
            "North Shore",
            "North Shore Missions",
        ],
        2226,
        [
            GrinchRamData(0x010294, binary_bit_pos=6),
        ],
    ),
    "WL - North Shore - Drilling Holes In Canoes - Behind max house": GrinchLocationData(
        "North Shore",
        [
            "Who Lake Missions",
            "Missionsanity",
            "Who Lake",
            "North Shore",
            "North Shore Missions",
        ],
        2227,
        [
            GrinchRamData(0x010293, binary_bit_pos=5),
        ],
    ),
    "WL - North Shore - Drilling Holes In Canoes - Right side on top of car": GrinchLocationData(
        "North Shore",
        [
            "Who Lake Missions",
            "Missionsanity",
            "Who Lake",
            "North Shore",
            "North Shore Missions",
        ],
        2228,
        [
            GrinchRamData(0x010293, binary_bit_pos=6),
        ],
    ),
    "WL - North Shore - Drilling Holes In Canoes - Left side on top of car": GrinchLocationData(
        "North Shore",
        [
            "Who Lake Missions",
            "Missionsanity",
            "Who Lake",
            "North Shore",
            "North Shore Missions",
        ],
        2229,
        [
            GrinchRamData(0x010293, binary_bit_pos=7),
        ],
    ),
    "WL - Submarine World - Modifying The Marine Mobile - Outer Fast-moving Fish": GrinchLocationData(
        "Submarine World",
        [
            "Who Lake Missions",
            "Missionsanity",
            "Who Lake",
            "Submarine World",
            "Submarine World Missions",
        ],
        2230,
        [
            GrinchRamData(0x010289, binary_bit_pos=6),
        ],
    ),
    "WL - Submarine World - Modifying The Marine Mobile - Inner Slow-moving Fish": GrinchLocationData(
        "Submarine World",
        [
            "Who Lake Missions",
            "Missionsanity",
            "Who Lake",
            "Submarine World",
            "Submarine World Missions",
        ],
        2231,
        [
            GrinchRamData(0x010289, binary_bit_pos=5),
        ],
    ),
    "WL - Submarine World - Modifying The Marine Mobile - Pirate Ship in Cave": GrinchLocationData(
        "Submarine World",
        [
            "Who Lake Missions",
            "Missionsanity",
            "Who Lake",
            "Submarine World",
            "Submarine World Missions",
        ],
        2232,
        [
            GrinchRamData(0x010289, binary_bit_pos=7),
        ],
    ),
    "WL - Submarine World - Modifying The Marine Mobile - Sea Cow Leaves": GrinchLocationData(
        "Submarine World",
        [
            "Who Lake Missions",
            "Missionsanity",
            "Who Lake",
            "Submarine World",
            "Submarine World Missions",
        ],
        2233,
        [
            GrinchRamData(0x01028A, binary_bit_pos=0),
        ],
    ),
    "WL - Submarine World - Modifying The Marine Mobile - Timed Cage": GrinchLocationData(
        "Submarine World",
        [
            "Who Lake Missions",
            "Missionsanity",
            "Who Lake",
            "Submarine World",
            "Submarine World Missions",
        ],
        2234,
        [
            GrinchRamData(0x01028A, binary_bit_pos=1),
        ],
    ),
    "WD - Power Plant - Touch Grass": GrinchLocationData(
        "Power Plant",
        ["Who Dump", "Power Plant", "Grasssanity", "Miscellaneous"],
        2300,
        [GrinchRamData(0x010000, value=0x10)],
    ),
    "WL - South Shore - Touch Grass": GrinchLocationData(
        "Who Lake",
        ["Who Lake", "South Shore", "Grasssanity", "Miscellaneous"],
        2301,
        [
            GrinchRamData(0x010000, value=0x12),
            GrinchRamData(0x010282, binary_bit_pos=4),
        ],
    ),
    "WL - North Shore - Touch Grass": GrinchLocationData(
        "North Shore",
        ["Who Lake", "North Shore", "Grasssanity", "Miscellaneous"],
        2302,
        [GrinchRamData(0x010000, value=0x14)],
    ),
    "WL - Mayor's Villa - Touch Grass": GrinchLocationData(
        "Mayor's Villa",
        ["Who Lake", "Mayor's Villa", "Grasssanity", "Miscellaneous"],
        2303,
        [GrinchRamData(0x010000, value=0x16)],
    ),
    "WV - Collect all Rotten Egg Launcher Blueprints": GrinchLocationData(
        "Whoville",
        ["Rotten Egg Launcher Blueprints", "Blueprints", "Whoville", "Whoville Blueprints", "Miscellaneous"],
        2400,
        [
            GrinchRamData(0x01020B, binary_bit_pos=0),
            GrinchRamData(0x01020B, binary_bit_pos=1),
            GrinchRamData(0x01021C, binary_bit_pos=1),
            GrinchRamData(0x01021C, binary_bit_pos=2),
        ],
    ),
    "WF - Collect all Rocket Spring Blueprints": GrinchLocationData(
        "Who Forest",
        ["Rocket Spring Blueprints", "Blueprints", "Who Forest", "Who Forest Blueprints", "Miscellaneous"],
        2401,
        [
            GrinchRamData(0x010243, binary_bit_pos=3),
            GrinchRamData(0x010243, binary_bit_pos=1),
            GrinchRamData(0x010243, binary_bit_pos=4),
            GrinchRamData(0x010242, binary_bit_pos=7),
            GrinchRamData(0x010242, binary_bit_pos=6),
            GrinchRamData(0x010243, binary_bit_pos=2),
            GrinchRamData(0x010243, binary_bit_pos=0),
            GrinchRamData(0x010243, binary_bit_pos=6),
            GrinchRamData(0x010243, binary_bit_pos=5),
        ],
    ),
    "WF - Collect all Slime Shooter Blueprints": GrinchLocationData(
        "Who Forest",
        ["Slime Shooter Blueprints", "Blueprints", "Who Forest", "Who Forest Blueprints", "Miscellaneous"],
        2402,
        [
            GrinchRamData(0x010244, binary_bit_pos=3),
            GrinchRamData(0x010243, binary_bit_pos=7),
            GrinchRamData(0x010244, binary_bit_pos=2),
            GrinchRamData(0x010244, binary_bit_pos=1),
            GrinchRamData(0x010244, binary_bit_pos=5),
            GrinchRamData(0x010244, binary_bit_pos=4),
            GrinchRamData(0x010244, binary_bit_pos=7),
            GrinchRamData(0x010244, binary_bit_pos=6),
            GrinchRamData(0x010244, binary_bit_pos=0),
        ],
    ),
    "WD - Collect all Octopus Climbing Device Blueprints": GrinchLocationData(
        "Who Dump",
        ["Octopus Climbing Device Blueprints", "Blueprints", "Who Dump", "Who Dump Blueprints", "Miscellaneous"],
        2403,
        [
            GrinchRamData(0x010252, binary_bit_pos=3),
            GrinchRamData(0x010252, binary_bit_pos=5),
            GrinchRamData(0x010252, binary_bit_pos=1),
            GrinchRamData(0x010252, binary_bit_pos=4),
            GrinchRamData(0x010252, binary_bit_pos=0),
            GrinchRamData(0x010252, binary_bit_pos=2),
            GrinchRamData(0x01026E, binary_bit_pos=2),
            GrinchRamData(0x01026E, binary_bit_pos=4),
            GrinchRamData(0x01026E, binary_bit_pos=3),
        ],
    ),
    "WL - Collect all Marine Mobile Blueprints": GrinchLocationData(
        "Who Lake",
        ["Marine Mobile Blueprints", "Blueprints", "Who Lake", "Who Lake Blueprints", "Miscellaneous"],
        2404,
        [
            GrinchRamData(0x010281, binary_bit_pos=5),
            GrinchRamData(0x010281, binary_bit_pos=6),
            GrinchRamData(0x010281, binary_bit_pos=7),
            GrinchRamData(0x010282, binary_bit_pos=0),
            GrinchRamData(0x010281, binary_bit_pos=4),
            GrinchRamData(0x010281, binary_bit_pos=2),
            GrinchRamData(0x010281, binary_bit_pos=3),
            GrinchRamData(0x010282, binary_bit_pos=1),
            GrinchRamData(0x010293, binary_bit_pos=0),
            GrinchRamData(0x010293, binary_bit_pos=2),
            GrinchRamData(0x010292, binary_bit_pos=6),
            GrinchRamData(0x010292, binary_bit_pos=7),
            GrinchRamData(0x010293, binary_bit_pos=3),
            GrinchRamData(0x010293, binary_bit_pos=4),
            GrinchRamData(0x010292, binary_bit_pos=5),
            GrinchRamData(0x010293, binary_bit_pos=1),
        ],
    ),
    "MC - Collect all Grinch Copter Blueprints": GrinchLocationData(
        "Mount Crumpit",
        ["Grinch Copter Blueprints", "Blueprints", "Whoville", "Whoville Blueprints",
         "Who Forest", "Who Forest Blueprints", "Who Dump", "Who Dump Blueprints", "Who Lake", "Who Lake Blueprints", "Miscellaneous"],
        2405,
        [
            GrinchRamData(0x01021F, binary_bit_pos=7),
            GrinchRamData(0x010220, binary_bit_pos=0),
            GrinchRamData(0x010216, binary_bit_pos=3),
            GrinchRamData(0x010216, binary_bit_pos=2),
            GrinchRamData(0x010234, binary_bit_pos=7),
            GrinchRamData(0x010234, binary_bit_pos=6),
            GrinchRamData(0x01022A, binary_bit_pos=7),
            GrinchRamData(0x01022B, binary_bit_pos=0),
            GrinchRamData(0x010265, binary_bit_pos=1),
            GrinchRamData(0x010265, binary_bit_pos=2),
            GrinchRamData(0x01026B, binary_bit_pos=0),
            GrinchRamData(0x01026B, binary_bit_pos=1),
            GrinchRamData(0x010289, binary_bit_pos=3),
            GrinchRamData(0x010289, binary_bit_pos=4),
            GrinchRamData(0x010275, binary_bit_pos=7),
            GrinchRamData(0x010275, binary_bit_pos=6),
        ],
    ),
        "WV - Collect all Binoculars Blueprints": GrinchLocationData(
        "Whoville",
        ["Binocular Blueprints", "Blueprints", "Whoville", "Whoville Blueprints", "Miscellaneous"],
        2406,
        [
            GrinchRamData(0x01020B, binary_bit_pos=2),
            GrinchRamData(0x01021F, binary_bit_pos=6),
            GrinchRamData(0x01021F, binary_bit_pos=5),
            GrinchRamData(0x01021F, binary_bit_pos=4),
        ],
    ),
    "WL - North Shore - Squash the Groundhog 1 time": GrinchLocationData(
        "North Shore",
        ["Who Lake", "North Shore", "Killsanity", "Miscellaneous"],
        2500,
        [
            GrinchRamData(0x095347, binary_bit_pos=0),
            GrinchRamData(0x010000, value=0x14),
         ],
    ),
    "WL - North Shore - Squash the Groundhog 2 times": GrinchLocationData(
        "North Shore",
        ["Who Lake", "North Shore", "Killsanity", "Miscellaneous"],
        2501,
        [
            GrinchRamData(0x095347, binary_bit_pos=1),
            GrinchRamData(0x010000, value=0x14),
        ],
    ),
    "WL - North Shore - Squash the Groundhog 3 times": GrinchLocationData(
        "North Shore",
        ["Who Lake", "North Shore", "Killsanity", "Miscellaneous"],
        2502,
        [
            GrinchRamData(0x095347, binary_bit_pos=2),
            GrinchRamData(0x010000, value=0x14),
            ],
    ),
    "WL - North Shore - Squash the Groundhog 4 times": GrinchLocationData(
        "North Shore",
        ["Who Lake", "North Shore", "Killsanity", "Miscellaneous"],
        2503,
        [
            GrinchRamData(0x095347, binary_bit_pos=3),
            GrinchRamData(0x010000, value=0x14),
        ],
    ),
    "WL - North Shore - Squash the Groundhog 5 times": GrinchLocationData(
        "North Shore",
        ["Who Lake", "North Shore", "Killsanity", "Miscellaneous"],
        2504,
        [
            GrinchRamData(0x095347, binary_bit_pos=4),
            GrinchRamData(0x010000, value=0x14),
        ],
    ),
    "WL - North Shore - Squash the Groundhog 6 times": GrinchLocationData(
        "North Shore",
        ["Who Lake", "North Shore", "Killsanity", "Miscellaneous"],
        2505,
        [
            GrinchRamData(0x095347, binary_bit_pos=5),
            GrinchRamData(0x010000, value=0x14),
        ],
    ),
    "WL - North Shore - Squash the Groundhog 7 times": GrinchLocationData(
        "North Shore",
        ["Who Lake", "North Shore", "Killsanity", "Miscellaneous"],
        2506,
        [
            GrinchRamData(0x095347, binary_bit_pos=6),
            GrinchRamData(0x010000, value=0x14),
        ],
    ),
    "WL - North Shore - Squash the Groundhog 8 times": GrinchLocationData(
        "North Shore",
        ["Who Lake", "North Shore", "Killsanity", "Miscellaneous"],
        2507,
        [
            GrinchRamData(0x095347, binary_bit_pos=7),
            GrinchRamData(0x010000, value=0x14),
        ],
    ),
    "WL - North Shore - Squash the Groundhog 9 times": GrinchLocationData(
        "North Shore",
        ["Who Lake", "North Shore", "Killsanity", "Miscellaneous"],
        2508,
        [
            GrinchRamData(0x095348, binary_bit_pos=0),
            GrinchRamData(0x010000, value=0x14),
        ],
    ),
    "WL - North Shore - Squash the Groundhog 10 times": GrinchLocationData(
        "North Shore",
        ["Who Lake", "North Shore", "Killsanity", "Miscellaneous"],
        2509,
        [
            GrinchRamData(0x095348, binary_bit_pos=1),
            GrinchRamData(0x010000, value=0x14),
        ],
    ),
    "WD - Shoot Down North West Platform": GrinchLocationData(
        "Who Dump",
        ["Who Dump", "Miscellaneous"],
        2600,
        [GrinchRamData(0x01025B, binary_bit_pos=0)],
    ),
    "WD - Shoot Down South West Platform": GrinchLocationData(
        "Who Dump",
        ["Who Dump", "Miscellaneous"],
        2601,
        [GrinchRamData(0x01025B, binary_bit_pos=1)],
    ),
    "WD - Shoot Down South Platform": GrinchLocationData(
        "Who Dump",
        ["Who Dump", "Miscellaneous"],
        2602,
        [GrinchRamData(0x01025B, binary_bit_pos=2)],
    ),
    "WD - Shoot Down South East Platform": GrinchLocationData(
        "Who Dump",
        ["Who Dump", "Miscellaneous"],
        2603,
        [GrinchRamData(0x01025B, binary_bit_pos=3)],
    ),
    "WD - Shoot Down North East Platform": GrinchLocationData(
        "Who Dump",
        ["Who Dump", "Miscellaneous"],
        2604,
        [GrinchRamData(0x01025B, binary_bit_pos=4)],
    ),
    "WV - Painting Bucket": GrinchLocationData(
        "Whoville",
        ["Whoville", "Mission Specific Item Locations"],
        2700,
        [GrinchRamData(0x0101F9, binary_bit_pos=1)],
    ),
    "WV - Clock Tower - Who Cloak": GrinchLocationData(
        "Clock Tower",
        ["Whoville", "Clock Tower", "Mission Specific Item Locations"],
        2701,
        [GrinchRamData(0x0101F9, binary_bit_pos=0)],
    ),
    "WV - Clock Tower - Hammer": GrinchLocationData(
        "Clock Tower",
        ["Whoville", "Clock Tower", "Mission Specific Item Locations"],
        2702,
        [GrinchRamData(0x0101F9, binary_bit_pos=3)],
    ),
    "WV - City Hall - Sculpting Tools": GrinchLocationData(
        "City Hall",
        ["Whoville", "City Hall", "Mission Specific Item Locations"],
        2703,
        [GrinchRamData(0x0101F9, binary_bit_pos=2)],
    ),
    "WF - Glue Bucket": GrinchLocationData(
        "Who Forest",
        ["Who Forest", "Mission Specific Item Locations"],
        2704,
        [GrinchRamData(0x0101F9, binary_bit_pos=4)],
    ),
    "WF - Cable Car Access Card": GrinchLocationData(
        "Who Forest",
        ["Who Forest", "Mission Specific Item Locations"],
        2705,
        [GrinchRamData(0x0101F9, binary_bit_pos=5)],
    ),
    "WD - Minefield - Scissors": GrinchLocationData(
        "Minefield",
        ["Who Dump", "Minefield", "Mission Specific Item Locations"],
         2706,
         [GrinchRamData(0x0101F9, binary_bit_pos=6)],
    ),
    "WL - Scout's Hut - Scout Clothes": GrinchLocationData(
        "Scout's Hut",
        ["Who Lake", "Scout's Hut", "Mission Specific Item Locations"],
        2707,
        [GrinchRamData(0x0101F9, binary_bit_pos=7),],
    ),
    "WL - North Shore - Drill": GrinchLocationData(
        "North Shore",
        ["Who Lake", "North Shore", "Mission Specific Item Locations"],
        2708,
        [GrinchRamData(0x0101FA, binary_bit_pos=2)],
    ),
        "WL - Mayor's Villa - Rope": GrinchLocationData(
        "Mayor's Villa",
        ["Who Lake", "Mayor's Villa", "Mission Specific Item Locations"],
        2709,
        [GrinchRamData(0x0101FA, binary_bit_pos=1)],
    ),
    "WL - Mayor's Villa - Hook": GrinchLocationData(
        "Mayor's Villa",
        ["Who Lake", "Mayor's Villa", "Mission Specific Item Locations"],
        2710,
        [GrinchRamData(0x0101FA, binary_bit_pos=0)],
    ),
}
def grinch_locations_to_id() -> dict[str, int]:
    location_mappings: dict[str, int] = {}
    for LocationName, LocationData in grinch_locations.items():
        location_mappings.update({LocationName: GrinchLocation.get_apid(LocationData.id)})
    return location_mappings
