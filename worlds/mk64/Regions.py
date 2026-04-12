from typing import TYPE_CHECKING
from BaseClasses import Region

from . import Courses
from .Locations import (MK64Location, Group, item_cluster_locations, course_locations, shared_hazard_locations,
                        cup_locations)
from .Options import GameMode
from .Rules import course_qualify_rules

if TYPE_CHECKING:
    from . import MK64World


def add_region(world: "MK64World", region_name: str, region_group: list[Region]) -> None:
    region_group.append(Region(region_name, world.player, world.multiworld))


def add_location(player: int, loc_name: str, code: int, region: Region) -> MK64Location:
    location = MK64Location(player, loc_name, code, region)
    region.locations.append(location)
    return location


def create_regions_locations_connections(world: "MK64World"):
    multiworld = world.multiworld
    player = world.player
    opt = world.opt
    shuffle_clusters = world.shuffle_clusters
    filler_spots = world.filler_spots

    location_group_mask = (Group.base
                           | (opt.hazards and Group.hazard)
                           | (opt.secrets and Group.secret)
                           | (opt.special_boxes and Group.blue_shell_item_spot))

    # Prepare Region Handling
    menu_region = Region("Menu", player, multiworld)
    course_regions: list[Region] = []
    shared_hazard_regions: list[Region] = []
    cup_regions: list[Region] = []

    # Construct item_spot_locations for shuffled item clusters and extra locations
    world.random.shuffle(shuffle_clusters)
    world.random.shuffle(filler_spots)
    item_spot_data = []
    c, s, t = 0, 0, -1
    for region in item_cluster_locations:
        item_spot_data.append([])
        for cluster in region:
            if shuffle_clusters[c]:
                t = world.random.randrange(0, len(cluster))
            c += 1
            for i, spot_data in enumerate(cluster):
                if i == t:
                    item_spot_data[-1].append(spot_data)
                    t = -1
                else:
                    if filler_spots[s]:
                        item_spot_data[-1].append(spot_data)
                    s += 1

    # Construct Course Regions and Locations
    for (course_name, locs), spot_data_clusters in zip(course_locations.items(), item_spot_data):
        add_region(world, course_name, course_regions)
        for loc_name, (code, group) in locs.items():
            if group & location_group_mask:
                add_location(player, loc_name, code, course_regions[-1])
        for spot in spot_data_clusters:
            spot_location = add_location(player, spot.name, spot.code, course_regions[-1])
            if opt.fences and spot.access:
                spot_location.access_rule = lambda state, access=spot.access: state.has_any(access, player)

    # Shared Hazard Regions & Locations & Connections
    if opt.hazards:
        for name, (code, courses) in shared_hazard_locations.items():
            add_region(world, name, shared_hazard_regions)
            add_location(player, name, code, shared_hazard_regions[-1])
            for c, region in enumerate(course_regions):
                if c in courses:
                    region.connect(shared_hazard_regions[-1])

    # Cup Regions & Locations
    if opt.mode == GameMode.option_cups:
        for cup, locations in cup_locations.items():
            add_region(world, cup, cup_regions)
            for name, code in locations.items():
                add_location(player, name, code, cup_regions[-1])

    # Determine Course Order
    order = Courses.determine_order(world)
    course_regions = [course_regions[i] for i in order]

    # Create Course & Cup Connections
    if opt.mode == GameMode.option_cups:
        entrance_names = ["Mushroom Cup 1", "Mushroom Cup 2", "Mushroom Cup 3", "Mushroom Cup 4",
                          "Flower Cup 1",   "Flower Cup 2",   "Flower Cup 3",   "Flower Cup 4",
                          "Star Cup 1",     "Star Cup 2",     "Star Cup 3",     "Star Cup 4",
                          "Special Cup 1",  "Special Cup 2",  "Special Cup 3",  "Special Cup 4"]
        for c in range(16):
            if c % 4:
                course_regions[c-1].connect(
                    course_regions[c],
                    entrance_names[c],
                    lambda state, qualify_rule=course_qualify_rules[order[c-1]]:
                        qualify_rule(state, player, opt.logic, opt)
                )
            else:
                menu_region.connect(course_regions[c], entrance_names[c],
                                    lambda state, count=c//4: state.has("Progressive Cup Unlock", player, count))
                course_regions[c+3].connect(cup_regions[c//4], entrance_names[c][:-1] + "Finish")
    else:  # GameMode.option_courses
        for i in range(16):
            locks = max(0, i + opt.locked_courses - 15)
            rule = (lambda state, k=locks: state.has("Progressive Course Unlock", player, k)) if locks > 0 else None
            menu_region.connect(course_regions[i], f"Course {i + 1}", rule)

    # Register regions (and locations)
    multiworld.regions += [menu_region] + course_regions + shared_hazard_regions + cup_regions

    # Write course order to spoiler log
    for i in range(16):
        entrance = course_regions[i].entrances[0]
        multiworld.spoiler.set_entrance(entrance.name, entrance.connected_region.name, "entrance", player)
        # Uncomment to print course order at generation time
        # print(entrance.name + " => " + entrance.connected_region.name)

    # Place Victory Event Location
    if opt.mode == GameMode.option_cups:
        cup_regions[-1].locations[-1].address = None
        cup_regions[-1].locations[-1].event = True
        victory_location = cup_regions[-1].locations[-1]
    else:
        course_regions[15].locations[2].address = None
        course_regions[15].locations[2].event = True
        victory_location = course_regions[15].locations[2]
    world.course_order = order
    world.victory_location = victory_location