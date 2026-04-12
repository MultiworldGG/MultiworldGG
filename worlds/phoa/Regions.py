from typing import Dict, Callable, Optional, NamedTuple

from BaseClasses import MultiWorld, Region, Location, CollectionState
from Utils import visualize_regions
from worlds.phoa import get_location_data, PhoaOptions
from worlds.phoa.Locations import PhoaLocationData
from worlds.phoa.LogicExtensions import PhoaLogic


class PhoaExit(NamedTuple):
    name: str
    region: str
    connection: str
    rule: Optional[Callable[[CollectionState], bool]] = None
    one_way: bool = False


def get_exit_data(player: int, options: PhoaOptions) -> list[PhoaExit]:
    logic = PhoaLogic(player)

    exits: list[PhoaExit] = [
        # Menu
        PhoaExit(
            name="game_start",
            region="Menu",
            connection="panselo_village",
            one_way=True,
        ),
        # panselo_village
        PhoaExit(
            name="panselo_gate",
            region="panselo_village",
            connection="panselo_region",
            rule=lambda state: logic.can_deal_damage(state, exclude_rocket_boots=True) or options.open_panselo_gates,
        ),
        PhoaExit(
            name="rutea's_lab_gate",
            region="panselo_village",
            connection="panselo_village_rutea's_lab",
            rule=lambda state: logic.can_hit_switch_from_a_distance(state),
        ),
        # panselo_region
        PhoaExit(
            name="anuri_temple_entrance",
            region="panselo_region",
            connection="anuri_temple(main_entrance)",
            rule=lambda state: logic.can_hit_switch_from_a_distance(state),
        ),
        PhoaExit(
            name="anuri_temple_side_entrance",
            region="panselo_region",
            connection="anuri_temple(side_entrance)",
            rule=lambda state: logic.has_explosives(state),
        ),
        PhoaExit(
            name="over_anuri_temple",
            region="panselo_region",
            connection="anuri_temple(slargummy_boss)",
            rule=lambda state: logic.has_sonic_spear(state),
            one_way=True,
        ),
        # anuri_temple(main_entrance)
        PhoaExit(
            name="anuri_temple_main_exit",
            region="anuri_temple(main_entrance)",
            connection="panselo_region",
        ),
        PhoaExit(
            name="anuri_temple_pearl_entrance",
            region="anuri_temple(main_entrance)",
            connection="anuri_temple(main)",
            rule=lambda state: logic.has_anuri_pearlstones(1, state)
        ),
        PhoaExit(
            name="anuri_temple_top_floor_boulder",
            region="anuri_temple(main_entrance)",
            connection="anuri_temple(top_floor)",
            rule=lambda state: logic.has_explosives(state)
                               or (logic.has_sonic_spear(state) and state.has("Rocket Boots", player)),
        ),
        # anuri_temple(top_floor)
        PhoaExit(
            name="anuri_temple_drop_to_throne",
            region="anuri_temple(top_floor)",
            connection="anuri_temple(main)",
            one_way=True,
        ),
        PhoaExit(
            name="anuri_temple_door_to_scaber_maze",
            region="anuri_temple(top_floor)",
            connection="anuri_temple(scaber_switch_maze)",
            rule=lambda state: logic.has_anuri_pearlstones(10, state)
        ),
        # anuri_temple(main)
        PhoaExit(
            name="anuri_temple_to_main_entrance",
            region="anuri_temple(main)",
            connection="anuri_temple(main_entrance)",
        ),
        PhoaExit(
            name="anuri_temple_to_tall_tower_puzzle_room",
            region="anuri_temple(main)",
            connection="anuri_temple(tall_tower_puzzle_room)",
            rule=lambda state: logic.has_anuri_pearlstones(10, state),
        ),
        PhoaExit(
            name="anuri_temple_to_side_entrance",
            region="anuri_temple(main)",
            connection="anuri_temple(side_entrance)",
        ),
        PhoaExit(
            name="anuri_temple_to_basement",
            region="anuri_temple(main)",
            connection="anuri_temple(basement)",
            rule=lambda state: logic.has_explosives(state),
        ),
        PhoaExit(
            name="anuri_temple_bridge_switch",
            region="anuri_temple(main)",
            connection="anuri_temple(moveable_bridge_area)",
            rule=lambda state: logic.can_hit_switch_from_a_distance(state)
                               or state.has("Rocket Boots", player),
        ),
        PhoaExit(
            name="anuri_temple_to_slargummy",
            region="anuri_temple(main)",
            connection="anuri_temple(slargummy_boss)",
            rule=lambda state: logic.has_anuri_pearlstones(6, state),
        ),
        # anuri_temple(side_entrance)
        PhoaExit(
            name="anuri_temple_side_exit",
            region="anuri_temple(side_entrance)",
            connection="panselo_region",
            rule=lambda state: logic.has_explosives(state),
        ),
        PhoaExit(
            name="anuri_temple_side_to_main",
            region="anuri_temple(side_entrance)",
            connection="anuri_temple(main)",
            rule=lambda state: state.has("Anuri Temple - Side entrance gate opened", player),
        ),
        # anuri_temple(slargummy_boss)
        PhoaExit(
            name="anuri_temple_slargummy_to_main",
            region="anuri_temple(slargummy_boss)",
            connection="anuri_temple(main)",
            rule=lambda state: logic.can_reasonably_kill_enemies(state),
        ),
        PhoaExit(
            name="anuri_temple_slargummy_to_pond",
            region="anuri_temple(slargummy_boss)",
            connection="anuri_temple(pond)",
            rule=lambda state: logic.can_reasonably_kill_enemies(state),
        ),
        # anuri_temple(pond)
        PhoaExit(
            name="anuri_temple_to_post_pond",
            region="anuri_temple(pond)",
            connection="anuri_temple(post_pond)",
            rule=lambda state: logic.has_anuri_pearlstones(9, state),
        ),
        # anuri_temple(post_pond)
        PhoaExit(
            name="anuri_temple_to_dive_room",
            region="anuri_temple(post_pond)",
            connection="anuri_temple(dive_room)",
            rule=lambda state: logic.has_anuri_pearlstones(10, state),
        ),
        PhoaExit(
            name="anuri_temple_to_urn_room",
            region="anuri_temple(post_pond)",
            connection="anuri_temple(urn_room)",
            rule=lambda state: logic.has_bombs(state)
                               or state.has("Rocket Boots", player),
        ),
    ]

    return exits


def create_regions_and_locations(world: MultiWorld, player: int, options: PhoaOptions):
    locations_per_region: Dict[str, Dict[str, PhoaLocationData]] = split_locations_per_region(
        get_location_data(player, options))

    regions = [
        create_region(world, player, locations_per_region, "Menu"),
        create_region(world, player, locations_per_region, "panselo_village"),
        create_region(world, player, locations_per_region, "panselo_village_rutea's_lab"),
        create_region(world, player, locations_per_region, "panselo_region"),
        create_region(world, player, locations_per_region, "anuri_temple(main_entrance)"),
        create_region(world, player, locations_per_region, "anuri_temple(top_floor)"),
        create_region(world, player, locations_per_region, "anuri_temple(scaber_switch_maze)"),
        create_region(world, player, locations_per_region, "anuri_temple(main)"),
        create_region(world, player, locations_per_region, "anuri_temple(tall_tower_puzzle_room)"),
        create_region(world, player, locations_per_region, "anuri_temple(side_entrance)"),
        create_region(world, player, locations_per_region, "anuri_temple(basement)"),
        create_region(world, player, locations_per_region, "anuri_temple(moveable_bridge_area)"),
        create_region(world, player, locations_per_region, "anuri_temple(slargummy_boss)"),
        create_region(world, player, locations_per_region, "anuri_temple(pond)"),
        create_region(world, player, locations_per_region, "anuri_temple(post_pond)"),
        create_region(world, player, locations_per_region, "anuri_temple(dive_room)"),
        create_region(world, player, locations_per_region, "anuri_temple(urn_room)"),
    ]

    world.regions += regions

    connect_regions(world, player, get_exit_data(player, options))


def create_region(world: MultiWorld, player: int, locations_per_region: Dict[str, Dict[str, PhoaLocationData]],
                  name: str) -> Region:
    region = Region(name, player, world)

    if name in locations_per_region:
        for location_name, location_data in locations_per_region[name].items():
            location = create_location(player, location_name, location_data, region)
            region.locations.append(location)

    return region


def create_location(player: int, location_name: str, location_data: PhoaLocationData, region: Region):
    location = Location(player, location_name, location_data.address, region)

    if location_data.rule:
        location.access_rule = location_data.rule

    return location


def connect_regions(world: MultiWorld, player: int, exits: list[PhoaExit]):
    for regionExit in exits:
        connect(world, player, regionExit.region, regionExit.connection, regionExit.rule, regionExit.name)


def connect(world: MultiWorld, player: int, source: str, target: str,
            rule: Optional[Callable[[CollectionState], bool]] = None, name: str = None):
    source_region = world.get_region(source, player)
    target_region = world.get_region(target, player)
    entrance = source_region.create_exit(name)

    if rule is not None:
        entrance.access_rule = rule

    entrance.connect(target_region)


def split_locations_per_region(locations: Dict[str, PhoaLocationData]):
    locations_per_region: Dict[str, Dict[str, PhoaLocationData]] = {}

    for location_name, location_data in locations.items():
        if location_data.region not in locations_per_region:
            locations_per_region[location_data.region] = {}

        locations_per_region[location_data.region][location_name] = location_data

    return locations_per_region
