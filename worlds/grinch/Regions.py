from typing import TYPE_CHECKING, NamedTuple, Optional

from BaseClasses import Region, MultiWorld, Entrance
from .Rules import interpret_rule
from .Items import grinch_items

from ..generic.Rules import add_rule

if TYPE_CHECKING:
    from . import GrinchWorld

mainareas_list = [
    "Mount Crumpit"
    "Whoville",
    "Who Forest",
    "Who Dump",
    "Who Lake",
]

subareas_list = [
    "Post Office",
    "City Hall",
    "Clock Tower",
    "Ski Resort",
    "Civic Center",
    "Minefield",
    "Power Plant",
    "Generator Building",
    "Submarine World",
    "Scout's Hut",
    "North Shore",
    "Mayor's Villa",
    "Sleigh Room",
    "Sleigh Ride",
]

supadow_list = [
    "Spin N' Win",
    "Pankamania",
    "The Copter Race Contest",
    "Bike Race",
]

class GrinchRegionInfo(NamedTuple):
    map_id: int
    parent_region: str
    allow_deathlink: bool = False
    map_table_addr: Optional[int] = None
    allow_music_rando: Optional[bool] = None
    region_access: list[list[str]] = None
    advanced_region_access: Optional[list[list[str]]] = None

class GrinchRegion(Region):
    region_data: GrinchRegionInfo

    def __init__(self, region_name: str, region_data: GrinchRegionInfo, player: int, multiworld: MultiWorld):
        super().__init__(region_name, player, multiworld)
        self.region_data = region_data

ALL_REGIONS_INFO: dict[str, GrinchRegionInfo] = {
    "Mount Crumpit": GrinchRegionInfo(0x05, "", False, 0x0FAAB4, True),

    "Whoville": GrinchRegionInfo(0x07, "Mount Crumpit", True, 0x0E8FA0, True,
        region_access=[
            [grinch_items.keys.WHOVILLE],
            ["1:" + grinch_items.keys.PROGRESSIVE_VACUUM_TUBE],
        ],),

    "Who Forest": GrinchRegionInfo(0x0B, "Mount Crumpit", True, 0x0E1C54, True,
        region_access=[
            [grinch_items.keys.WHO_FOREST],
            ["2:" + grinch_items.keys.PROGRESSIVE_VACUUM_TUBE],
        ],),

    "Who Dump": GrinchRegionInfo(0x0E, "Mount Crumpit", True, 0x0DFF24, True,
        region_access=[
            [grinch_items.keys.WHO_DUMP],
            ["3:" + grinch_items.keys.PROGRESSIVE_VACUUM_TUBE],
        ],),

    "Who Lake": GrinchRegionInfo(0x12, "Mount Crumpit", True, 0x0DD16C, True,
        region_access=[
            [grinch_items.keys.WHO_LAKE],
            ["4:" + grinch_items.keys.PROGRESSIVE_VACUUM_TUBE],
        ],),

    "Sleigh Room": GrinchRegionInfo(0x05, "Mount Crumpit", False, 0x0FAAB4, True,
        region_access=[
            [grinch_items.keys.SLEIGH_ROOM_KEY],
        ],),

    "Spin N' Win": GrinchRegionInfo(0x1A, "Mount Crumpit", False, allow_music_rando=True,
        region_access = [
            [grinch_items.supadow.SPIN_N_WIN],
        ],),

    "Pankamania": GrinchRegionInfo(0x1B, "Mount Crumpit", False, allow_music_rando=True,
       region_access=[
           [grinch_items.supadow.PANKAMANIA],
       ],),

    "The Copter Race Contest": GrinchRegionInfo(0X1C, "Mount Crumpit", False, allow_music_rando=True,
        region_access=[
            [grinch_items.supadow.COPTER_RACE],
        ],),
    "Post Office": GrinchRegionInfo(0x0A, "Whoville", False, 0x0DFB64, True,
        region_access=[
            [grinch_items.level_items.WV_WHO_CLOAK],
        ],
        advanced_region_access=[
            []
        ],),

    "City Hall": GrinchRegionInfo(0x08, "Whoville", False, 0x0E7090, True,
        region_access=[
            [grinch_items.gadgets.ROTTEN_EGG_LAUNCHER],
        ],),

    "Clock Tower": GrinchRegionInfo(0x09, "Whoville", False, 0x0E70E8, True,
        region_access=[
            [grinch_items.moves.SNEAK],
            [grinch_items.gadgets.SLIME_SHOOTER],
            [grinch_items.level_items.WV_WHO_CLOAK],
        ],
        advanced_region_access=[
            []
        ],),

    "Ski Resort": GrinchRegionInfo(0x0C, "Who Forest", True, 0x0E98C0, True,
        region_access=[
            [grinch_items.level_items.WF_CABLE_CAR_ACCESS_CARD],
        ],),

    "Civic Center": GrinchRegionInfo(0x0D, "Who Forest", True, 0x0DDEA0, True,
        region_access=[
            [grinch_items.gadgets.GRINCH_COPTER],
            [grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE],
        ],),

    "Minefield": GrinchRegionInfo(0x11, "Who Dump", True, 0x0E87C4, True,
        region_access=[
            [grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE],
            [grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE],
        ],
        advanced_region_access=[
            [grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE],
            [grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE],
        ],),

    "Power Plant": GrinchRegionInfo(0x10, "Who Dump", True, 0x0E885C, True,
        region_access=[
            [grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE],
            [grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE],
            [grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE],
        ],),

    "Generator Building": GrinchRegionInfo(0x0F, "Power Plant", True, 0x0E0ED4, True,
        region_access=[
            [grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER],
            [grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
             grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
             grinch_items.gadgets.ROCKET_SPRING,
             grinch_items.moves.MAX,
             grinch_items.moves.BAD_BREATH],
        ],),

    "Submarine World": GrinchRegionInfo(0x17, "Who Lake", True, 0x0E0368, True,
        region_access=[
            [grinch_items.gadgets.MARINE_MOBILE],
        ],),

    "Scout's Hut": GrinchRegionInfo(0x13, "Who Lake", True, 0x0D5DFC, True,
        region_access=[
            [grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.SNEAK],
            [grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.SNEAK],
        ],
        advanced_region_access=[
            [grinch_items.gadgets.GRINCH_COPTER],
            [grinch_items.gadgets.ROCKET_SPRING],
        ],),

    "North Shore": GrinchRegionInfo(0x14, "Who Lake", True, 0x0DD43C, True,
        region_access=[
            [grinch_items.level_items.WL_SCOUT_CLOTHES,
            grinch_items.moves.SNEAK],
        ],
        advanced_region_access=[
            [grinch_items.level_items.WL_SCOUT_CLOTHES],
        ],),
    "Mayor's Villa": GrinchRegionInfo(0x16, "North Shore", True, 0x0FA7C8, True,
        region_access=[
            [grinch_items.level_items.WL_SCOUT_CLOTHES],
        ],),
    "Bike Race": GrinchRegionInfo(0x18, "Sleigh Room", False, allow_music_rando=True,
        region_access=[
            [grinch_items.supadow.BIKE_RACE,
             grinch_items.keys.SLEIGH_ROOM_KEY],
        ],),
    "Sleigh Ride": GrinchRegionInfo(0x19, "Sleigh Room", False, allow_music_rando=True,
        region_access=[
            [grinch_items.sleigh_parts.EXHAUST_PIPES,
            grinch_items.sleigh_parts.TWIN_END_TUBA,
            grinch_items.sleigh_parts.SKIS,
            grinch_items.sleigh_parts.TIRES],
        ],),
}

def create_regions(world: "GrinchWorld"):
    for area in [*mainareas_list, *subareas_list, *supadow_list]:
        # Each area in mainarea, subarea, and supadow create a region for the given player
        world.multiworld.regions.append(Region(area, world.player, world.multiworld))


# TODO Optimize this function
def grinchconnect(
    world: "GrinchWorld",
    current_region_name: str,
    connected_region_name: str,
    access_rules: list[list[str]],
):
    current_region = world.get_region(current_region_name)
    connected_region = world.get_region(connected_region_name)
    rule_list = interpret_rule(access_rules, world.player)

    curr_entr: Entrance = current_region.connect(connected_region)
    connect_entr: Entrance = connected_region.connect(current_region)

    if rule_list:
        rule = lambda state, rules=tuple(rule_list): any(rule(state) for rule in rules)
        add_rule(curr_entr, rule)
        add_rule(connect_entr, rule)


def connect_regions(world: "GrinchWorld", multiworld: MultiWorld):
    for grinch_region, grinch_data in ALL_REGIONS_INFO.items():

        if world.options.supadow_minigames == 0 and grinch_region in supadow_list:
            #Prevent supadow region being created if supadows are off
            continue
        multiworld.regions.append(GrinchRegion(grinch_region, grinch_data, world.player, multiworld))

        access_list = [] if grinch_data.region_access is None else [item_set.copy() for item_set in grinch_data.region_access]

        if world.options.advanced_logic or world.using_ut:
            if grinch_data.advanced_region_access is not None:
                for advanced_rule in grinch_data.advanced_region_access:
                    advanced_rule = advanced_rule.copy()
                    if world.using_ut and not world.options.advanced_logic:
                        advanced_rule.append(world.glitches_item_name)
                    access_list.append(advanced_rule)

        if grinch_region == "Mount Crumpit":
            continue

        grinchconnect(world, grinch_region, grinch_data.parent_region, access_list)
