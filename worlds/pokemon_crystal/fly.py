import functools
import logging
from collections import defaultdict
from typing import TYPE_CHECKING

from .data import data, FlyRegion, Landmark, FlypointWarp, OUTDOOR_WARP_MAP_FRIENDLY_NAMES, friendly_entrance_name, \
    internal_entrance_name
from .options import FreeFlyLocation, Route32Condition, JohtoOnly, RandomizeFlyUnlocks, FlyDestinationPlando
from .utils import should_include_region

if TYPE_CHECKING:
    from .world import PokemonCrystalWorld


SILVER_CAVE_FLY_INDEX = next(fr.id for fr in data.fly_regions if fr.name == "Silver Cave")


def get_fly_regions(world: "PokemonCrystalWorld") -> list[FlyRegion]:
    fly_regions = list(data.fly_regions)

    if world.options.johto_only == JohtoOnly.option_on:
        fly_regions = [region for region in fly_regions if region.id != SILVER_CAVE_FLY_INDEX]

    if world.options.johto_only:
        fly_regions = [region for region in fly_regions if region.johto]

    return fly_regions


def fly_flag_index(world: "PokemonCrystalWorld", fly_region: FlyRegion) -> int:
    """0-based flypoint flag: seed order (ROM flypoint table) when destinations are randomized, else vanilla."""
    if world.options.randomize_fly_destinations:
        return get_fly_regions(world).index(fly_region)
    return fly_region.spawn_flag


def get_free_fly_locations(world: "PokemonCrystalWorld"):
    location_pool = list(data.fly_regions)

    if not world.options.randomize_fly_destinations:
        if not world.options.randomize_starting_town:
            location_pool = \
                [region for region in location_pool if not region.exclude_vanilla_start]
            if world.options.route_32_condition.value != Route32Condition.option_any_badge:
                # Azalea, Goldenrod
                location_pool = [region for region in location_pool if region.name not in ("Azalea Town", "Goldenrod City")]
            if not world.options.remove_ilex_cut_tree and world.options.route_32_condition.value != Route32Condition.option_any_badge:
                # Goldenrod
                location_pool = [region for region in location_pool if region.name != "Goldenrod City"]
        else:
            location_pool = [region for region in location_pool if region.name != world.starting_town.name]

    available_regions = set(get_fly_regions(world))
    location_pool = [region for region in location_pool if region in available_regions]

    blocklist = set(world.options.free_fly_blocklist.value)
    if "_Johto" in blocklist:
        blocklist.remove("_Johto")
        blocklist.update(town.name for town in data.fly_regions if town.johto)
    if "_Kanto" in blocklist:
        blocklist.remove("_Kanto")
        blocklist.update(town.name for town in data.fly_regions if not town.johto)

    # only do any of this if there even is a fly location blocklist
    if blocklist:

        # figure out how many fly locations are needed
        locations_required = 1
        if world.options.free_fly_location.value == FreeFlyLocation.option_free_fly_and_map_card:
            locations_required = 2

        # calculate what the list of locations would be after the blocklist
        location_pool_after_blocklist = [item for item in location_pool if
                                         item.name not in blocklist]

        # if the list after the blocked locations are removed is long enough to satisfy all the requested fly locations, set the location pool to it
        if len(location_pool_after_blocklist) >= locations_required:
            location_pool = location_pool_after_blocklist
        else:
            logging.warning("Pokemon Crystal: All valid free fly locations blocked for player %s (%s). "
                            "Using global list instead.", world.player, world.player_name)

    world.random.shuffle(location_pool)
    if world.options.free_fly_location.value in (FreeFlyLocation.option_free_fly,
                                                 FreeFlyLocation.option_free_fly_and_map_card):
        world.free_fly_location = location_pool.pop()
    if world.options.free_fly_location.value in (FreeFlyLocation.option_free_fly_and_map_card,
                                                 FreeFlyLocation.option_map_card):
        world.map_card_fly_location = location_pool.pop()


@functools.cache
def _arrival_index() -> dict[tuple[str, int], list]:
    index = defaultdict(list)
    for conn in data.entrance_connections.values():
        index[(conn.arrival_map, conn.arrival_warp_index)].append(conn)
    return index


def flypoint_arrival_connections(flypoint: FlypointWarp) -> list:
    """Connections whose arrival is this flypoint's warp tile."""
    return _arrival_index().get((flypoint.map_name, flypoint.warp_index), [])


def _get_flyable_warps() -> dict[Landmark, list[FlypointWarp]]:
    """
    Filters the global list of flypoint warps by their presence in data.entrance_connections,
    with which we later retreive flypoint's destination region.
    """
    flypoints = {
        l: [flypoint for flypoint in flypoints if flypoint_arrival_connections(flypoint)]
        for l, flypoints in data.flypoints.items()
    }

    # N.B. this does nothing as of 6.0.0 since National Park is excluded from ER entirely,
    # none of its warps are in entrance_connections anyways
    flypoints[Landmark.NationalPark] = [
        flypoint for flypoint in flypoints[Landmark.NationalPark]
        if flypoint.map_name != "NationalParkBugContest"
    ]
    return flypoints


def _resolve_plando_destination(destination: str, outmaps_set: set[str]) -> tuple[Landmark, str, FlypointWarp | None]:
    """
    Resolves a Fly Destination Plando entry, returning the following:
    - Landmark
    - Map name
    - Specific Flypoint (if the entry targets a flypoint, None if it's a map)
    """
    if destination in outmaps_set:
        map_name = "".join(part.title() for part in destination.split(" "))
        landmark = data.maps[map_name].landmark
        return landmark, map_name, None
    else:
        target_entrance_warps = data.entrance_connections[internal_entrance_name(destination)].exit_warps
        map_name = target_entrance_warps[0].map_name
        landmark = data.maps[map_name].landmark
        target_flypoint = next(flypoint for flypoint in data.flypoints[landmark]
                               if flypoint.warp_index in (warp.warp_index for warp in target_entrance_warps)
                               and flypoint.map_name == map_name)
        return landmark, map_name, target_flypoint


def _apply_fly_destination_plando(world: "PokemonCrystalWorld",
                                  flyable_flypoints: dict[Landmark, list[FlypointWarp]],
                                  limit: int
                                  ) -> dict[int, FlypointWarp]:
    """
    Returns the plandoed fly destinations and their 0-based fly unlock index

    Pops the flypoints' landmarks from flyable_flypoints to immediately filter them for regular randomization later.
    """
    plando = {}

    if world.options.randomize_fly_unlocks.value == RandomizeFlyUnlocks.option_exclude_silver_cave \
            and world.options.johto_only.value != JohtoOnly.option_on:
        silver_key = f"{FlyDestinationPlando.KEY_PREFIX}{SILVER_CAVE_FLY_INDEX}"
        if silver_key in world.options.fly_destination_plando.value:
            logging.warning(f"Pokemon Crystal: Cannot plando {silver_key} as that slot is reserved for Silver Cave "
                            f"when Exclude Silver Cave is on. Removing key from Fly Destination Plando.")
            world.options.fly_destination_plando.value.pop(silver_key)
        silver_flypoint = data.flypoints[Landmark.SilverCave][0]
        plando[SILVER_CAVE_FLY_INDEX - 1] = silver_flypoint
        flyable_flypoints.pop(Landmark.Route28, None)
        flyable_flypoints.pop(Landmark.SilverCave, None)

    if not world.options.fly_destination_plando.value:
        return plando

    plandoed_landmarks = set()
    outmaps_set = frozenset(OUTDOOR_WARP_MAP_FRIENDLY_NAMES)
    for key, destination in world.options.fly_destination_plando.value.items():
        index = int(key.removeprefix(FlyDestinationPlando.KEY_PREFIX)) - 1
        if index >= limit:
            logging.warning(f"Pokemon Crystal: Cannot fulfill {key}: {destination} as only {limit} flypoints exist "
                            f"with these settings. "
                            f"Ignoring key {key} in Fly Destination Plando for player {world.player_name}.")
            continue

        landmark, map_name, target_flypoint = _resolve_plando_destination(destination, outmaps_set)

        if landmark in plandoed_landmarks:
            logging.warning(f"Pokemon Crystal: Cannot fulfill {key}: {destination} as its landmark is already taken. "
                            f"Ignoring key {key} in Fly Destination Plando for player {world.player_name}.")
            continue

        if target_flypoint is not None and target_flypoint not in flyable_flypoints.get(landmark, []):
            logging.warning(f"Pokemon Crystal: Cannot fulfill {key}: {destination} as the destination is unavailable "
                            f"under these settings. Ignoring key {key} in Fly Destination Plando for player "
                            f"{world.player_name}.")
            continue

        if target_flypoint is None:
            potential_dests = {flypoint for flypoint in flyable_flypoints[landmark] if flypoint.map_name == map_name}
            if len(potential_dests) == 0:
                logging.warning(f"Pokemon Crystal: cannot fulfill {key}: {destination} as no flypoints in that map "
                                f"are available under these settings. Ignoring key {key} in Fly Destination Plando "
                                f"for player {world.player_name}.")
                continue

            # Prefer non-blocklisted warps if one is available
            blocklisted_conns = {conn for name, conn in data.entrance_connections.items()
                                 if conn.exit_warps[0].map_name == map_name
                                 and friendly_entrance_name(name) in world.options.fly_destination_blocklist.value}
            blocklisted_dests = {flypoint for flypoint in potential_dests
                                 if any(conn for conn in blocklisted_conns
                                        if flypoint.warp_index in (warp.warp_index for warp in conn.exit_warps)
                                        )
                                 }
            non_blocklisted = potential_dests - blocklisted_dests
            if non_blocklisted:
                potential_dests = non_blocklisted
            target_flypoint = world.random.choice(sorted(potential_dests, key=lambda fw: fw.warp_index))

        plandoed_landmarks.add(landmark)
        flyable_flypoints.pop(landmark)
        plando[index] = target_flypoint

    return plando


def _apply_fly_destination_blocklist(world: "PokemonCrstalWorld",
                                     flyable_flypoints: dict[Landmark, list[FlypointWarp]],
                                     num_flypoints: int):
    """
    Removes blocklisted flypoints from flyable_flypoints while ensuring len(flyable_flypoints) >= num_flypoints
    """
    if not world.options.fly_destination_blocklist.value: return

    outmaps_set = frozenset(OUTDOOR_WARP_MAP_FRIENDLY_NAMES)
    blocklist = {_resolve_plando_destination(dest, outmaps_set)
                 for dest in world.options.fly_destination_blocklist.value}
    blocklisted_per_landmark = defaultdict(set)
    for dest in blocklist:
        if len(flyable_flypoints.get(dest[0], [])) == 0: continue
        if dest[2] is not None:
            blocklisted_per_landmark[dest[0]].add(dest[2])
        else:
            blocklisted_per_landmark[dest[0]] |= {flypoint for flypoint in flyable_flypoints[dest[0]]
                                                  if flypoint.map_name == dest[1]}

    blocklisted_landmarks = set()
    for landmark, blocked in blocklisted_per_landmark.items():
        blocked &= set(flyable_flypoints[landmark])
        if len(blocked) == len(flyable_flypoints[landmark]):
            blocklisted_landmarks.add(landmark)

    remaining = len(flyable_flypoints) - len(blocklisted_landmarks)
    if remaining < num_flypoints:
        loosen = world.random.sample(sorted(blocklisted_landmarks), num_flypoints - remaining)
        for landmark in loosen:
            blocklisted_per_landmark.pop(landmark)

    for landmark, blocked in blocklisted_per_landmark.items():
        for flypoint in blocked:
            flyable_flypoints[landmark].remove(flypoint)


def randomize_fly_destinations(world: "PokemonCrystalWorld"):
    if world.is_universal_tracker or not world.options.randomize_fly_destinations: return

    def flyable_filter(flypoint):
        if not world.options.route_23_restored and flypoint.map_name == "Route23Restored":
            return False
        # A flypoint targets a specific warp tile on an outdoor map; that tile
        # may sit in a sub-region gated by another option (e.g. the Flooded
        # Mine entrance tile lives in REGION_CHERRYGROVE_CITY:FLOODED_MINE_
        # ENTRANCE, which only exists when flooded_mine is on). Drop those.
        for conn in flypoint_arrival_connections(flypoint):
            if not should_include_region(data.regions[conn.entrance_region], world):
                return False
        return True

    flyable_flypoints = {
        l: [flypoint for flypoint in flypoints if flyable_filter(flypoint)]
        for l, flypoints in _get_flyable_warps().items()
    }
    flyable_flypoints = {l: flypoints for l, flypoints in flyable_flypoints.items() if len(flypoints) > 0}

    num_flypoints = len(get_fly_regions(world))
    plando = _apply_fly_destination_plando(world, flyable_flypoints, num_flypoints)

    num_flypoints -= len(plando)

    _apply_fly_destination_blocklist(world, flyable_flypoints, num_flypoints)

    eligible_landmarks = [l for l, flypoints in flyable_flypoints.items() if len(flypoints) > 0]
    selected_landmarks = world.random.sample(eligible_landmarks, num_flypoints)
    fly_destinations = [world.random.choice(flyable_flypoints[l]) for l in selected_landmarks]

    for index, flypoint in sorted(plando.items()):
        fly_destinations.insert(index, flypoint)

    world.fly_destinations = fly_destinations
