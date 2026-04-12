from typing import Optional, Callable, TYPE_CHECKING, NamedTuple
from BaseClasses import Region, MultiWorld

from . import Rules

if TYPE_CHECKING:
    from . import LMWorld


class LMRegionInfo(NamedTuple):
    map_id: int
    floor: int
    room_id: int
    in_game_room_id: int
    early_keys: list[str]
    door_keys: list[str] = []
    door_ids: list[int] = []
    allow_random_spawn: bool = False
    pos_x: float = 0.0000000
    pos_y: float = 0.0000000
    pos_z: float = 0.0000000
    element_type: str = None
    allow_element_rando: bool = True

class LMRegion(Region):
    region_data: LMRegionInfo

    def __init__(self, region_name: str, region_data: LMRegionInfo, player: int, multiworld: MultiWorld):
        super().__init__(region_name, player, multiworld)
        self.region_data = region_data


REGION_LIST: dict[str, LMRegionInfo] = {
    "Foyer": LMRegionInfo(2, 1, 2, 2, ["Heart Key", "Family Hallway Key", "Parlor Key"],
        ["Heart Key", "Family Hallway Key", "Parlor Key"], [3, 34, 33], True, -7.640748, 0.000000, 145.174300),
    "Parlor": LMRegionInfo(2, 2, 35, 36, ["Parlor Key", "Heart Key", "Anteroom Key"],
        ["Parlor Key", "Anteroom Key"], [34, 38], False, -43.294357, 550.000000, -1775.288450, "No Element", False),
    "Family Hallway": LMRegionInfo(2, 2, 29, 30, []),
    "1F Hallway": LMRegionInfo(2, 1, 6, 6, []),
    "Anteroom": LMRegionInfo(2, 2, 39, 42, ["Wardrobe Key", "Anteroom Key", "Parlor Key"],
        ["Wardrobe Key", "Anteroom Key"], [43, 38], True, -1.503195, 550.000000, -3087.626950, "No Element"),
    "The Well": LMRegionInfo(2, 0, 69, 72, []),
    "Wardrobe": LMRegionInfo(2, 2, 38, 40, ["Wardrobe Key", "Anteroom Key", "Parlor Key", "Heart Key"],
        ["Wardrobe Key", "Wardrobe Balcony Key"], [43, 41], True, -1789.859250, 550.000000, -3303.123780, "No Element"),
    "Wardrobe Balcony": LMRegionInfo(2, 2, 37, 40, []),
    "Study": LMRegionInfo(2, 2, 34, 35, ["Study Key", "Family Hallway Key"],  ["Study Key"], [32],
        False, -1696.352290, 550.000000, -1605.182980),
    "Master Bedroom": LMRegionInfo(2, 2, 33, 34, ["Master Bedroom Key", "Family Hallway Key"], ["Master Bedroom Key"],
        [31], True, -3365.857670, 550.000000, -1513.529660),
    "Nursery": LMRegionInfo(2, 2, 24, 26, ["Nursery Key", "Family Hallway Key"], ["Nursery Key"], [27], True,
        -3331.658690, 550.000000, -198.970337),
    "Twins' Room": LMRegionInfo(2, 2, 25, 27, ["Twins Bedroom Key", "Family Hallway Key"], ["Twins Bedroom Key"], [28],
        True, -1729.586790, 550.000000, 116.055779),
    "Laundry Room": LMRegionInfo(2, 1, 5, 5, ["Laundry Room Key", "Butler's Room Key", "Heart Key"],
        ["Laundry Room Key", "Butler's Room Key"], [1, 7], False, -3165.112550, 0.000000, -804.770508, "No Element"),
    "Butler's Room": LMRegionInfo(2, 1, 0, 0, ["Butler's Room Key", "Laundry Room Key", "Heart Key"], ["Butler's Room Key"],
        [1], True, -3800.646000, 0.000000, -327.291077),
    "Fortune-Teller's Room": LMRegionInfo(2, 1, 3, 3, ["Fortune Teller Key", "Mirror Room Key"],
        ["Fortune Teller Key", "Mirror Room Key"], [4, 5], True, 2343.24854, 0.000000, -191.177582),
    "Ballroom": LMRegionInfo(2, 1, 10, 9,  ["Ballroom Key", "Storage Room Key"], ["Ballroom Key", "Storage Room Key"],
        [15, 16], True, 2854.236820, 0.000000, -1565.909060, "No Element"),
    "Dining Room": LMRegionInfo(2, 1, 9, 8, ["Dining Room Key", "Kitchen Key"], ["Dining Room Key", "Kitchen Key"],
        [11, 14], True, -393.851349, 0.000000, -1416.557500),
    "1F Washroom": LMRegionInfo(2, 1, 17, 16, []),
    "1F Bathroom": LMRegionInfo(2, 1, 20, 21, ["1F Bathroom Key", "Heart Key"], ["1F Bathroom Key"], [23],
        True, -2160.237550, 0.000000, -4671.114750, "No Element"),
    "Conservatory": LMRegionInfo(2, 1, 21, 22, ["Conservatory Key", "Lower 2F Stairwell Key", "Heart Key"],
        ["Conservatory Key"], [21], True, 1309.44092, 0.000000, -4962.23096),
    "Billiards Room": LMRegionInfo(2, 1, 12, 12, ["Billiards Room Key", "Heart Key"],
        ["Billiards Room Key", "Projection room Key"], [17, 18], True, -963.755737, 0.000000, -3055.808110),
    "Basement Stairwell": LMRegionInfo(2, 0, 65, 67, []),
    "Altar Hallway": LMRegionInfo(2, 0, 68, 71, []),
    "Projection Room": LMRegionInfo(2, 1, 13, 13, ["Projection Room Key", "Billiards Room Key"],
        ["Projection Room Key", "Billiards Room Key"], [18], True, 281.914215, 0.000000, -3137.967530, "No Element"),
    "Kitchen": LMRegionInfo(2, 1, 8, 7, [], element_type="Ice"),
    "Boneyard": LMRegionInfo(2, 1, 11, 11, []),
    "Graveyard": LMRegionInfo(2, 1, 16, 15, [], element_type="No Element"),
    "Hidden Room": LMRegionInfo(2, 1, 1, 1, ["Butler's Room Key", "Laundry Room Key", "Heart Key"],
        allow_random_spawn=True, pos_x=-1998.314700, pos_y=0.000000, pos_z=225.000000, element_type="Ice"),
    "Storage Room": LMRegionInfo(2, 1, 14, 14, ["Storage Room Key", "Ballroom Key"], ["Storage Room Key"], [16],
        True, 3412.177250, 0.000000, -3009.698000, "No Element"),
    "Mirror Room": LMRegionInfo(2, 1, 4, 4, ["Mirror Room Key", "Fortune Teller Key"],  ["Mirror Room Key"], [5],
        True, 3764.000000, 0.000000, 159.723618, "No Element"),
    "Rec Room": LMRegionInfo(2, 1, 22, 23, ["North Rec Room Key", "South Rec Room Key", "Lower 2F Stairwell Key",
        "Upper 2F Stairwell Key"], ["North Rec Room Key", "South Rec Room Key"], [24, 25], True,
        3517.026860, 0.000000, -4646.33203),
    "Courtyard": LMRegionInfo(2, 1, 23, 24, ["Club Key", "North Rec Room Key", "Heart Key"],
        ["Club Key", "North Rec Room Key"], [42, 25], True,  1613.042970, 9.000000, -5663.574710, "No Element"),
    "2F Stairwell": LMRegionInfo(2, 2, 19, 18, []),
    "Cellar": LMRegionInfo(2, 0, 63, 66, [], element_type="No Element"),
    "Breaker Room": LMRegionInfo(2, 0, 67, 69, ["Breaker Room Key", "Basement Stairwell Key"],  ["Breaker Room Key"],
        [71], True, 3127.567140, -550.000000, -1437.766600),
    "Basement Hallway": LMRegionInfo(2, 0, 62, 65, []),
    "Cold Storage": LMRegionInfo(2, 0, 61, 64, ["Cold Storage Key", "Cellar Key"], ["Cold Storage Key"], [65],
        True, 1405.000000, -550.000000, -25.000000),
    "Pipe Room": LMRegionInfo(2, 0, 66, 68, ["Pipe Room Key", "Cellar Key"], ["Pipe Room Key"], [69],
        True, 1235.000000, -480.000000, -1433.000000, "No Element"),
    "Secret Altar": LMRegionInfo(2, 0, 70, 73, ["Spade Key", "Altar Hallway Key"], ["Spade Key"], [72],
        False, 2293.000000, -550.000000, -5805.000000),
    "Tea Room": LMRegionInfo(2, 2, 47, 50, [], element_type="No Element"),
    "Nana's Room": LMRegionInfo(2, 2, 46, 49, ["Nana's Room Key", "Upper 2F Stairwell Key"], ["Nana's Room Key"], [49],
        True, -457.708374, 550.000000, -4535.000000),
    "2F Rear Hallway": LMRegionInfo(2, 2, 26, 32, []),
    "2F Washroom": LMRegionInfo(2, 2, 42, 45, [], element_type="Fire"),
    "2F Bathroom": LMRegionInfo(2, 2, 45, 48, ["2F Bathroom Key", "Upper 2F Stairwell Key"], ["2F Bathroom Key"], [48],
        True, -1902.854130, 550.000000, -4660.501950),
    "Astral Hall": LMRegionInfo(2, 2, 40, 43, ["Astral Hall Key", "Upper 2F Stairwell Key"],
        ["Astral Hall Key", "Observatory Key"], [44, 40], True, 2023.579290, 550.000000, -2915.000000, "No Element", False),
    "Observatory": LMRegionInfo(2, 2, 41, 44, []),
    "Sealed Room": LMRegionInfo(2, 2, 36, 37, [], element_type="No Element"),
    "Sitting Room": LMRegionInfo(2, 2, 27, 28, ["Sitting Room Key", "Guest Room Key"],
        ["Sitting Room Key", "Guest Room Key"], [29, 30], True, 2225.465090, 550.000000, -98.163559, "No Element", False),
    "Guest Room": LMRegionInfo(2, 2, 28, 29, ["Guest Room Key", "Sitting Room Key"], ["Guest Room Key"], [30], True,
        3637.69727, 550.000000, 201.316391),
    "Safari Room": LMRegionInfo(2, 3, 52, 55, ["Safari Room Key", "East Attic Hallway Key", "Balcony Key"],
        ["Safari Room Key", "East Attic Hallway Key"], [55, 56], True, 3317.313480, 1100.000000, 225.000000, "Water"),
    "East Attic Hallway": LMRegionInfo(2, 3, 51, 54, []),
    "West Attic Hallway": LMRegionInfo(2, 3, 49, 57, []),
    "Artist's Studio": LMRegionInfo(2, 3, 57, 60, [], element_type="No Element"),
    "Balcony": LMRegionInfo(2, 3, 59, 62, []),
    "Armory": LMRegionInfo(2, 3, 48, 51, ["Armory Key", "Diamond Key", "Telephone Room Key"],
        ["Armory Key", "Ceramics Studio Key"], [50, 51], True, -2541.662600, 1100.000000, -40.361595, "No Element"),
    "Ceramics Studio": LMRegionInfo(2, 3, 55, 58, ["Ceramics Studio Key", "Armory Key", "Telephone Room Key"],
        ["Ceramics Studio Key", "Armory Key"], [50], True, -2397.3373540, 1100.000000, -1579.717410),
    "Telephone Room": LMRegionInfo(2, 3, 50, 53, ["Telephone Room Key", "Clockwork Key"],
        ["Telephone Room Key", "Clockwork Key"], [52, 53], True, -9.812825, 1100.000000, 118.738243, "No Element"),
    "Clockwork Room": LMRegionInfo(2, 3, 56, 59, ["Clockwork Key", "Telephone Room Key"], ["Clockwork Key"], [53],
        True, 10.759588, 1100.000000, -1649.743900),
    "Roof": LMRegionInfo(2, 4, 60, 63, [], element_type="Ice"),
    "Training Room": LMRegionInfo(3, 1, 0, 0, []),
    "Gallery": LMRegionInfo(6, 1, 0, 0, [])
}

TOAD_SPAWN_LIST: list[str] = ["Foyer", "Courtyard", "Wardrobe Balcony", "1F Washroom"]

vanilla_door_state = {
        34: 0,
        38: 0,
        43: 1,
        41: 1,
        33: 0,
        32: 1,
        31: 0,
        27: 0,
        28: 0,
        3: 0,
        1: 1,
        4: 0,
        5: 1,
        7: 0,
        11: 1,
        14: 0,
        15: 0,
        10: 1,
        17: 0,
        18: 1,
        20: 0,
        16: 0,
        74: 0,
        75: 1,
        23: 1,
        21: 0,
        25: 0,
        24: 1,
        42: 0,
        29: 0,
        30: 1,
        44: 1,
        40: 1,
        45: 1,
        48: 1,
        49: 1,
        47: 1,
        51: 0,
        63: 0,
        52: 1,
        59: 0,
        62: 1,
        55: 1,
        53: 0,
        56: 0,
        50: 1,
        65: 0,
        9: 1,
        71: 0,
        68: 0,
        67: 1,
        69: 0,
        70: 1,
        72: 0
    }

def set_ghost_type(world: "LMWorld", ghost_list: dict):
    types: list[str] = ["Fire", "Water", "Ice", "No Element"]
    weights: list[int] = [2, 2, 2, 8]

    for region_name in ghost_list.keys():
        if not REGION_LIST[region_name].allow_element_rando:
            ghost_type = "No Element"
        else:
            ghost_type = world.random.choices(sorted(types), weights, k=1)[0]
        ghost_list.update({region_name: ghost_type})


def lmconnect(world: "LMWorld", source: str, target: str, key: Optional[str] = None,
            doorid: Optional[int] = None, rule: Optional[Callable] = None, one_way: bool = False, required_element: Optional[str] = ""):
    player = world.player

    if world.open_doors.get(doorid) == 0:
        extra_rule = lambda state: state.has(key, player)
        if rule is not None:
            rule = lambda state, orig_rule=rule: orig_rule(state) and extra_rule(state)
        else:
            rule = extra_rule

    source_region = world.get_region(source)
    target_region = world.get_region(target)
    source_region.connect(target_region, rule=rule)
    if not one_way:
        target_region.connect(source_region, rule=rule)

    if required_element == "Fire":
        for fregion in Rules.FIRE_SPIRIT_SPOT:
            world.multiworld.register_indirect_condition(world.get_region(fregion),
                                                         world.multiworld.get_entrance(f"{source_region.name} -> {target_region.name}", world.player))
            if not one_way:
                world.multiworld.register_indirect_condition(world.get_region(fregion),
                                                             world.multiworld.get_entrance(
                                                                 f"{target_region.name} -> {source_region.name}", world.player))
    elif required_element == "Ice":
        for iregion in Rules.ICE_SPIRIT_SPOT:
            world.multiworld.register_indirect_condition(world.get_region(iregion),
                                                         world.multiworld.get_entrance(f"{source_region.name} -> {target_region.name}", world.player))
            if not one_way:
                world.multiworld.register_indirect_condition(world.get_region(iregion),
                                                             world.multiworld.get_entrance(
                                                                 f"{target_region.name} -> {source_region.name}", world.player))
    elif required_element == "Water":
        for wregion in Rules.WATER_SPIRIT_SPOT:
            world.multiworld.register_indirect_condition(world.get_region(wregion),
                                                         world.multiworld.get_entrance(f"{source_region.name} -> {target_region.name}", world.player))
            if not one_way:
                world.multiworld.register_indirect_condition(world.get_region(wregion),
                                                             world.multiworld.get_entrance(
                                                                 f"{target_region.name} -> {source_region.name}", world.player))


def connect_regions(world: "LMWorld"):
    lmconnect(world, "Foyer", "Parlor", "Parlor Key", 34)
    lmconnect(world, "Parlor", "Anteroom", "Anteroom Key", 38)
    lmconnect(world, "Anteroom", "Wardrobe", "Wardrobe Key", 43)
    lmconnect(world, "Wardrobe", "Wardrobe Balcony", "Wardrobe Balcony Key", 41)
    lmconnect(world, "Foyer", "Family Hallway", "Family Hallway Key", 33)
    lmconnect(world, "Foyer", "1F Hallway", "Heart Key", 3)
    lmconnect(world, "Family Hallway", "Study", "Study Key", 32)
    lmconnect(world, "Family Hallway", "Master Bedroom", "Master Bedroom Key", 31)
    lmconnect(world, "Family Hallway", "Nursery", "Nursery Key", 27)
    lmconnect(world, "Family Hallway", "Twins' Room", "Twins Bedroom Key", 28)
    lmconnect(world, "1F Hallway", "Basement Stairwell", "Basement Stairwell Key", 9)
    lmconnect(world, "1F Hallway", "2F Stairwell", "Lower 2F Stairwell Key", 74)
    lmconnect(world, "1F Hallway", "Courtyard", "Club Key", 42)
    lmconnect(world, "1F Hallway", "1F Bathroom", "1F Bathroom Key", 23)
    lmconnect(world, "1F Hallway", "Conservatory", "Conservatory Key", 21)
    lmconnect(world, "1F Hallway", "Billiards Room", "Billiards Room Key", 17)
    lmconnect(world, "1F Hallway", "1F Washroom", "1F Washroom Key", 20)
            # lambda state, wash_boo_count=world.options.washroom_boo_count.value: state.has_group("Boo", world.player, wash_boo_count)
            #               or state.has("Boo", world.player, wash_boo_count))
    lmconnect(world, "1F Hallway", "Ballroom", "Ballroom Key", 15)
    lmconnect(world, "1F Hallway", "Dining Room", "Dining Room Key", 14)
    lmconnect(world, "1F Hallway", "Laundry Room", "Laundry Room Key", 7)
    lmconnect(world, "1F Hallway", "Fortune-Teller's Room", "Fortune Teller Key", 4)
    lmconnect(world, "Courtyard", "Rec Room", "North Rec Room Key", 25)
    lmconnect(world, "Ballroom", "Storage Room", "Storage Room Key", 16)
    lmconnect(world, "Dining Room", "Kitchen", "Kitchen Key", 11)
    lmconnect(world, "Kitchen", "Boneyard", "Boneyard Key", 10,
            lambda state: Rules.can_fst_water(state, world.player), required_element="Water")
    lmconnect(world, "Boneyard", "Graveyard",
            rule=lambda state: Rules.can_fst_water(state, world.player), required_element="Water")
    lmconnect(world, "Billiards Room", "Projection Room", "Projection Room Key", 18)
    lmconnect(world, "Fortune-Teller's Room", "Mirror Room", "Mirror Room Key", 5)
    lmconnect(world, "Laundry Room", "Butler's Room", "Butler's Room Key", 1)
    lmconnect(world, "Butler's Room", "Hidden Room", rule=lambda state: state.has("Poltergust 3000", world.player))
    lmconnect(world, "Courtyard", "The Well")
    lmconnect(world, "Rec Room", "2F Stairwell", "South Rec Room Key", 24)
    lmconnect(world, "2F Stairwell", "Tea Room", "Tea Room Key", 47,
            lambda state: Rules.can_fst_water(state, world.player), required_element="Water")
    lmconnect(world, "2F Stairwell", "2F Rear Hallway", "Upper 2F Stairwell Key", 75)
    lmconnect(world, "2F Rear Hallway", "2F Bathroom", "2F Bathroom Key", 48)
    lmconnect(world, "2F Rear Hallway", "2F Washroom", "2F Washroom Key", 45)
    lmconnect(world, "2F Rear Hallway", "Nana's Room", "Nana's Room Key", 49)
    lmconnect(world, "2F Rear Hallway", "Astral Hall", "Astral Hall Key", 44)
    lmconnect(world, "2F Rear Hallway", "Sitting Room", "Sitting Room Key", 29)
    lmconnect(world, "2F Rear Hallway", "Safari Room", "Safari Room Key", 56)
    lmconnect(world, "Astral Hall", "Observatory", "Observatory Key", 40,
            lambda state: Rules.can_fst_fire(state, world.player), required_element="Fire")
    lmconnect(world, "Sitting Room", "Guest Room", "Guest Room Key", 30)
    lmconnect(world, "Safari Room", "East Attic Hallway", "East Attic Hallway Key", 55)
    lmconnect(world, "East Attic Hallway", "Artist's Studio", "Artist's Studio Key", 63)
    lmconnect(world, "East Attic Hallway", "Balcony", "Balcony Key", 62,
            lambda state, balc_boo_count=world.options.balcony_boo_count.value: state.has_group_unique("Boo", world.player, balc_boo_count)
                          or state.has("Boo", world.player, balc_boo_count))
    lmconnect(world, "Balcony", "West Attic Hallway", "Diamond Key", 59)
    lmconnect(world, "West Attic Hallway", "Armory", "Armory Key", 51)
    lmconnect(world, "West Attic Hallway", "Telephone Room", "Telephone Room Key", 52)
    lmconnect(world, "Telephone Room", "Clockwork Room", "Clockwork Key", 53)
    lmconnect(world, "Armory", "Ceramics Studio", "Ceramics Studio Key", 50)
    lmconnect(world, "Clockwork Room", "Roof", rule=lambda state: state.has("Defeat Clockwork", world.player))
    lmconnect(world, "Roof", "Sealed Room", one_way=True),
    lmconnect(world, "Basement Stairwell", "Breaker Room", "Breaker Room Key", 71)
    lmconnect(world, "Basement Stairwell", "Cellar", "Cellar Key", 68,
              rule=lambda state: state.has("Poltergust 3000", world.player))
    lmconnect(world, "Cellar", "Basement Hallway", "Basement Hallway Key", 67,
              rule=lambda state: state.has("Poltergust 3000", world.player))
    lmconnect(world, "Basement Hallway", "Cold Storage", "Cold Storage Key", 65)
    lmconnect(world, "Basement Hallway", "Pipe Room", "Pipe Room Key", 69)
    lmconnect(world, "Basement Hallway", "Altar Hallway", "Altar Hallway Key", 70)
    lmconnect(world, "Altar Hallway", "Secret Altar", "Spade Key", 72,
            lambda state, final_boo_count=world.options.final_boo_count.value: state.has_group_unique("Boo", world.player, final_boo_count)
                          or state.has("Boo", world.player, final_boo_count))
    lmconnect(world, world.origin_region_name, "Gallery")
    lmconnect(world, world.origin_region_name, "Training Room")

# ROOM_EXITS = []

# THis dict maps exits to entrances located in that exit
# ENTRANCE_ACCESSIBILITY: dict[str, list[str]] = {
#    "Foyer": [
#        "Dungeon Entrance on Dragon Roost Island",
#        ],
