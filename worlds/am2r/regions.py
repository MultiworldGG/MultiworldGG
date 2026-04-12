from typing import List, Set, Dict, Tuple, Optional, Callable, NamedTuple, TYPE_CHECKING
from BaseClasses import CollectionState, Region, Location
from .locations import LocationData, get_location_datas
from .rules import AM2RLogic

if TYPE_CHECKING:
    from . import AM2RWorld
else:
    AM2RWorld = object

EventId: Optional[int] = None


class LocationData(NamedTuple):
    region: str
    name: str
    code: Optional[int]
    rule: Callable[[CollectionState], bool] = lambda state: True


def create_regions_and_locations(world: AM2RWorld, player: int):
    location_datas: Tuple[LocationData] = get_location_datas(world, player)

    locations_per_region: Dict[str, List[LocationData]] = split_location_datas_per_region(location_datas)

    regions = [
        create_region(world, player, locations_per_region, "Menu"),
        create_region(world, player, locations_per_region, "Main Caves"),
        create_region(world, player, locations_per_region, "First Alpha"),
        create_region(world, player, locations_per_region, "Guardian"),
        create_region(world, player, locations_per_region, "Golden Temple"),
        create_region(world, player, locations_per_region, "Golden Temple Nest"),
        create_region(world, player, locations_per_region, "Hydro Station"),
        create_region(world, player, locations_per_region, "Inner Hydro Station"),
        create_region(world, player, locations_per_region, "Hydro Nest"),
        create_region(world, player, locations_per_region, "Arachnus"),
        create_region(world, player, locations_per_region, "Mines"),
        create_region(world, player, locations_per_region, "Industrial Complex Nest"),
        create_region(world, player, locations_per_region, "Pre Industrial Complex"),
        create_region(world, player, locations_per_region, "Industrial Complex"),
        create_region(world, player, locations_per_region, "Torizo Ascended"),
        create_region(world, player, locations_per_region, "The Tower"),
        create_region(world, player, locations_per_region, "Geothermal"),
        create_region(world, player, locations_per_region, "Tester"),
        create_region(world, player, locations_per_region, "Tester Upper"),
        create_region(world, player, locations_per_region, "Tester Lower"),
        create_region(world, player, locations_per_region, "Underwater Distribution Center"),
        create_region(world, player, locations_per_region, "Underwater Distro Connection"),
        create_region(world, player, locations_per_region, "Serris"),
        create_region(world, player, locations_per_region, "Ice Beam"),
        create_region(world, player, locations_per_region, "Pipe Hell BL"),
        create_region(world, player, locations_per_region, "Pipe Hell BR"),
        create_region(world, player, locations_per_region, "Pipe Hell L"),
        create_region(world, player, locations_per_region, "Pipe Hell R"),
        create_region(world, player, locations_per_region, "Pipe Hell Outside"),
        create_region(world, player, locations_per_region, "Fast Travel"),
        create_region(world, player, locations_per_region, "Gravity"),
        create_region(world, player, locations_per_region, "EMP"),
        create_region(world, player, locations_per_region, "Screw Attack"),
        create_region(world, player, locations_per_region, "GFS Thoth"),
        create_region(world, player, locations_per_region, "Genesis"),
        create_region(world, player, locations_per_region, "Deep Caves"),
        create_region(world, player, locations_per_region, "Omega Nest"),
        create_region(world, player, locations_per_region, "The Lab"),
        create_region(world, player, locations_per_region, "Research Station")
    ]

    if __debug__:
        throwIfAnyLocationIsNotAssignedToARegion(regions, locations_per_region.keys())

    world.regions += regions

    logic = AM2RLogic(world, player)

    connect(world, player, "Menu", "Main Caves"),

    connect(world, player, "Main Caves", "Guardian"),
    connect(world, player, "Guardian", "Main Caves"),

    connect(world, player, "Main Caves", "First Alpha"),
    connect(world, player, "First Alpha", "Main Caves"),

    connect(world, player, "Main Caves", "Hydro Station"),
    connect(world, player, "Hydro Station", "Main Caves"),

    connect(world, player, "Main Caves", "Mines", lambda state: state.has("Super Missile", player)),
    connect(world, player, "Mines", "Main Caves"),

    connect(world, player, "Main Caves", "Industrial Complex Nest"),
    connect(world, player, "Industrial Complex Nest", "Main Caves"),

    connect(world, player, "Main Caves", "The Tower"),
    connect(world, player, "The Tower", "Main Caves"),

    connect(world, player, "Main Caves", "Underwater Distribution Center", lambda state: (state.has("Power Bomb", player) or state.has("Super Missile", player)) and state.has("Ice Beam", player)),  # when s&q is fixed, remove ice beam
    connect(world, player, "Underwater Distribution Center", "Main Caves", lambda state: state.has("Ice Beam", player)),

    connect(world, player, "Main Caves", "Deep Caves", logic.AM2R_can_down),
    connect(world, player, "Deep Caves", "Main Caves"),

    connect(world, player, "Main Caves", "GFS Thoth"),
    connect(world, player, "GFS Thoth", "Main Caves"),

    connect(world, player, "GFS Thoth", "Genesis")
    connect(world, player, "Genesis", "GFS Thoth")

    connect(world, player, "Guardian", "Golden Temple"),
    connect(world, player, "Golden Temple", "Guardian"),

    connect(world, player, "Guardian", "Golden Temple Nest"),
    connect(world, player, "Golden Temple Nest", "Guardian"),

    connect(world, player, "Golden Temple", "Fast Travel", lambda state: state.has("Screw Attack", player)),
    connect(world, player, "Fast Travel", "Golden Temple", lambda state: state.has("Screw Attack", player)),

    connect(world, player, "Hydro Station", "Hydro Nest", logic.AM2R_can_jump),
    connect(world, player, "Hydro Nest", "Hydro Station"),

    connect(world, player, "Hydro Station", "The Tower", lambda state: state.has("Screw Attack", player)),
    connect(world, player, "The Tower", "Hydro Station", lambda state: state.has("Screw Attack", player)),

    connect(world, player, "Hydro Station", "The Lab", logic.AM2R_can_lab),
    connect(world, player, "The Lab", "Hydro Station", lambda state: state.has("Screw Attack", player)),

    connect(world, player, "Hydro Station", "Arachnus", lambda state: state.has("Power Bomb", player, 4) or state.has("Bombs", player)),
    connect(world, player, "Arachnus", "Hydro Station"),

    connect(world, player, "Hydro Station", "Inner Hydro Station", lambda state: state.has("Screw Attack", player) or logic.AM2R_can_bomb(state))
    connect(world, player, "Inner Hydro Station", "Hydro Station", lambda state: state.has("Screw Attack", player) or logic.AM2R_can_bomb(state))

    connect(world, player, "Industrial Complex Nest", "Pre Industrial Complex", lambda state: (state.has("Speed Booster", player) and state.has("Hi Jump", player)) or logic.AM2R_can_bomb(state)),
    connect(world, player, "Pre Industrial Complex", "Industrial Complex Nest", lambda state: state.has("Speed Booster", player) or logic.AM2R_can_bomb(state)),

    connect(world, player, "Pre Industrial Complex", "Industrial Complex"),
    connect(world, player, "Industrial Complex", "Pre Industrial Complex", lambda state: state.has("Speed Booster", player)),

    connect(world, player, "Pre Industrial Complex", "Fast Travel", lambda state: state.has("Screw Attack", player)),
    connect(world, player, "Fast Travel", "Pre Industrial Complex", lambda state: state.has("Screw Attack", player)),

    connect(world, player, "Pre Industrial Complex", "Torizo Ascended"),
    connect(world, player, "Torizo Ascended", "Pre Industrial Complex"),
    # A4 to Geothermal
    connect(world, player, "The Tower", "Geothermal", lambda state: state.has("Speed Booster", player) and state.has("Power Bomb", player)),
    connect(world, player, "Geothermal", "The Tower", lambda state: state.has("Speed Booster", player) and state.has("Power Bomb", player)),
    # tower to A5
    connect(world, player, "The Tower", "Fast Travel", lambda state: state.has("Screw Attack", player)),
    connect(world, player, "Fast Travel", "The Tower", lambda state: state.has("Screw Attack", player)),
    # tester
    connect(world, player, "The Tower", "Tester Lower", logic.AM2R_can_bomb),
    connect(world, player, "The Tower", "Tester Upper", logic.AM2R_can_bomb),
    connect(world, player, "Tester Lower", "Tester"),
    connect(world, player, "Tester", "Tester Lower"),
    connect(world, player, "Tester", "Tester Upper"),
    connect(world, player, "Tester Upper", "Tester"),
    connect(world, player, "Tester Lower", "The Tower", logic.AM2R_can_bomb),
    connect(world, player, "Tester Upper", "The Tower", logic.AM2R_can_bomb),
    # A5
    connect(world, player, "Underwater Distribution Center", "EMP", logic.AM2R_can_bomb),
    connect(world, player, "EMP", "Underwater Distribution Center", logic.AM2R_can_bomb),

    connect(world, player, "Underwater Distribution Center", "Serris"),
    connect(world, player, "Serris", "Underwater Distribution Center", lambda state: state.has("Gravity Suit", player)),

    connect(world, player, "Ice Beam", "Serris"),
    connect(world, player, "Serris", "Ice Beam", lambda state: state.has("Gravity Suit", player)),

    # Pipe Hell Fuckery
    connect(world, player, "EMP", "Pipe Hell BL", lambda state: state.has("Speed Booster", player)),
    connect(world, player, "Pipe Hell BL", "EMP", lambda state: state.has("Speed Booster", player)),

    connect(world, player, "Pipe Hell BL", "Pipe Hell BR"),
    connect(world, player, "Pipe Hell BR", "Pipe Hell BL"),

    connect(world, player, "Pipe Hell L", "Pipe Hell BL", lambda state: state.has("Screw Attack", player)),
    connect(world, player, "Pipe Hell BL", "Pipe Hell L", lambda state: state.has("Screw Attack", player)),

    connect(world, player, "Pipe Hell BR", "Pipe Hell L"),
    connect(world, player, "Pipe Hell L", "Pipe Hell BR"),

    connect(world, player, "Pipe Hell BR", "Pipe Hell R", lambda state: state.has("Screw Attack", player)),
    connect(world, player, "Pipe Hell R", "Pipe Hell BR", lambda state: state.has("Screw Attack", player)),

    connect(world, player, "Pipe Hell R", "Pipe Hell L", logic.AM2R_can_bomb),
    connect(world, player, "Pipe Hell L", "Pipe Hell R", logic.AM2R_can_bomb),

    connect(world, player, "Pipe Hell L", "Fast Travel", lambda state: state.has("Screw Attack", player)),
    connect(world, player, "Fast Travel", "Pipe Hell L", lambda state: state.has("Screw Attack", player)),

    connect(world, player, "Fast Travel", "Gravity", lambda state: state.has("Gravity Suit", player) and state.has("Space Jump", player)),  # one way transition due to crumbles

    connect(world, player, "Fast Travel", "Underwater Distribution Center"),
    connect(world, player, "Underwater Distribution Center", "Fast Travel", lambda state: state.can_reach("Fast Travel", "Region", player)),

    connect(world, player, "Gravity", "Pipe Hell Outside", lambda state: state.has("Gravity Suit", player) and state.has("Space Jump", player)),
    connect(world, player, "Pipe Hell Outside", "Gravity"),

    connect(world, player, "Pipe Hell Outside", "Pipe Hell R", logic.AM2R_can_bomb),
    connect(world, player, "Pipe Hell R", "Pipe Hell Outside", lambda state: state.can_reach("Pipe Hell Outside", "Region", player)),

    connect(world, player, "Screw Attack", "Pipe Hell R", lambda state: state.has("Screw Attack", player) and logic.AM2R_can_schmove(state)),
    connect(world, player, "Pipe Hell R", "Screw Attack", lambda state: state.has("Screw Attack", player) and logic.AM2R_can_spider(state)),

    connect(world, player, "Underwater Distribution Center", "Underwater Distro Connection", lambda state: state.has("Ice Beam", player) or (state.has("Gravity Suit", player) and state.has("Speed Booster", player))),
    connect(world, player, "Underwater Distro Connection", "Underwater Distribution Center", lambda state: state.has("Ice Beam", player) or (state.has("Gravity Suit", player) and state.has("Speed Booster", player))),

    connect(world, player, "Underwater Distro Connection", "Pipe Hell R"),
    connect(world, player, "Pipe Hell R", "Underwater Distro Connection", lambda state: state.has("Super Missile", player) or (state.has("Gravity Suit", player) and state.has("Speed Booster", player)))

    connect(world, player, "Deep Caves", "Omega Nest")
    connect(world, player, "Omega Nest", "Deep Caves")

    connect(world, player, "Omega Nest", "The Lab", logic.AM2R_can_lab)  # , logic.AM2R_can_lab
    connect(world, player, "The Lab", "Omega Nest")

    connect(world, player, "The Lab", "Research Station")


def throwIfAnyLocationIsNotAssignedToARegion(regions: List[Region], regionNames: Set[str]):
    existingRegions: Set[str] = set()

    for region in regions:
        existingRegions.add(region.name)

    if regionNames - existingRegions:
        raise Exception(
            "AM2R: the following regions are used in locations: {}, but no such region exists".format(
                regionNames - existingRegions))


def create_location(player: int, location_data: LocationData, region: Region) -> Location:
    location = Location(player, location_data.name, location_data.code, region)
    location.access_rule = location_data.rule

    if id is None:
        location.event = True
        location.locked = True

    return location


def create_region(world: AM2RWorld, player: int, locations_per_region: Dict[str, List[LocationData]],name: str) -> Region:
    region = Region(name, player, world)

    if name in locations_per_region:
        for location_data in locations_per_region[name]:
            location = create_location(player, location_data, region)
            region.locations.append(location)

    return region


def connect(world: AM2RWorld, player: int, source: str, target: str,
            rule: Optional[Callable[[CollectionState], bool]] = None):
    sourceRegion = world.get_region(source, player)
    targetRegion = world.get_region(target, player)
    sourceRegion.connect(targetRegion, rule=rule)


def split_location_datas_per_region(locations: Tuple[LocationData, ...]) -> Dict[str, List[LocationData]]:
    per_region: Dict[str, List[LocationData]] = {}

    for location in locations:
        per_region.setdefault(location.region, []).append(location)

    return per_region
