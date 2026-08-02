from collections import deque

from ...BaseClasses import CollectionState, RegionType
from ...Dungeons import dungeon_table
from ...OWEdges import OWTileRegions, OWTileDistricts

class District(object):

    def __init__(self, name, dungeon=None):
        self.name = name
        self.dungeon = dungeon
        self.regions = list()
        self.locations = set()
        self.entrances = list()
        self.sphere_one = False

        self.dungeons = set()
        self.access_points = set()


def create_districts(world):
    world.districts = {}
    for p in range(1, world.players + 1):
        create_district_helper(world, p)


def create_district_helper(world, player):
    districts = {}
    districts['Kakariko'] = District('Kakariko')
    districts['Northwest Hyrule'] = District('Northwest Hyrule')
    districts['Central Hyrule'] = District('Central Hyrule')
    districts['The Desert Area'] = District('Desert')
    districts['Lake Hylia'] = District('Lake Hylia')
    districts['Eastern Hyrule'] = District('Eastern Hyrule')
    districts['Death Mountain'] = District('Death Mountain')
    districts['East Dark World'] = District('East Dark World')
    districts['South Dark World'] = District('South Dark World')
    districts['Northwest Dark World'] = District('Northwest Dark World')
    districts['The Mire Area'] = District('The Mire')
    districts['Dark Death Mountain'] = District('Dark Death Mountain')
    districts.update({x: District(x, dungeon=x) for x in dungeon_table.keys()})

    world.districts[player] = districts


def init_districts(world):
    def exclude_area(world, owid, area, player):
        # area can be a region or entrancecurrently, could potentially be a problem later if name collision
        std_regions = ['Pyramid Ledge', 'Pyramid Hole', 'Pyramid Entrance']
        inv_regions = ['Spiral Mimic Ledge Extend', 'Inverted Pyramid Hole', 'Inverted Pyramid Entrance']
        if (area in inv_regions and not world.is_tile_swapped(owid, player)) \
            or (area in std_regions and world.is_tile_swapped(owid, player)):
            return True
        return False

    create_districts(world)
    for player in range(1, world.players + 1):
        # adding regions to districts
        for owid, (alt_regions, alt_districts, default_districts) in OWTileDistricts.items():
            idx = 0 if (world.mode[player] == 'inverted') == world.is_tile_swapped(owid, player) else 1
            if owid in OWTileRegions.inverse.keys():
                for region in OWTileRegions.inverse[owid]:
                    if exclude_area(world, owid, region, player):
                        continue
                    if alt_regions and region in alt_regions:
                        world.districts[player][alt_districts[idx]].regions.append(region)
                    else:
                        world.districts[player][default_districts[idx]].regions.append(region)
            if owid + 0x40 in OWTileRegions.inverse.keys():
                for region in OWTileRegions.inverse[owid + 0x40]:
                    if exclude_area(world, owid, region, player):
                        continue
                    if alt_regions and region in alt_regions:
                        world.districts[player][alt_districts[(idx + 1) % 2]].regions.append(region)
                    else:
                        world.districts[player][default_districts[(idx + 1) % 2]].regions.append(region)

        # adding entrances to districts
        for name, district in world.districts[player].items():
            if not district.dungeon:
                for region_name in district.regions:
                    region = world.get_region(region_name, player)
                    for exit in region.exits:
                        if exit.spot_type == 'Entrance' and not exclude_area(world, OWTileRegions[region.name], exit.name, player):
                            district.entrances.append(exit.name)


def resolve_districts(world):
    state = CollectionState(world)
    state.sweep_for_events()
    for player in range(1, world.players + 1):
        # these are not static for OWR - but still important
        inaccessible = [r for r in inaccessible_regions_std if not world.is_tile_swapped(OWTileRegions[r], player)]
        inaccessible = inaccessible + [r for r in inaccessible_regions_inv if world.is_tile_swapped(OWTileRegions[r], player)]
        check_set = find_reachable_locations(state, player)
        
        for name, district in world.districts[player].items():
            if district.dungeon:
                dungeon = world.get_dungeon(district.dungeon, player)
                dungeon.districts = [district] + dungeon.districts
                layout = world.dungeon_layouts[player][district.dungeon]
                district.locations.update([l.name for r in layout.master_sector.regions
                                           for l in r.locations if not l.item and l.real])
            else:
                for region_name in district.regions:
                    region = world.get_region(region_name, player)
                    region.districts.append(district)
                    for location in region.locations:
                        if not location.item and location.real:
                            district.locations.add(location.name)
                for entrance in district.entrances:
                    ent = world.get_entrance(entrance, player)
                    queue = deque([ent.connected_region])
                    visited = set()
                    while len(queue) > 0:
                        region = queue.pop()
                        if region is None:
                            RuntimeError(f'No region connected to entrance: {ent.name} Likely a missing entry in OWExitTypes')
                        visited.add(region)
                        if region.type == RegionType.Cave:
                            region.districts.append(district)
                            for location in region.locations:
                                if not location.item and location.real:
                                    district.locations.add(location.name)
                            for ext in region.exits:
                                if ext.connected_region and ext.connected_region not in visited:
                                    queue.appendleft(ext.connected_region)
                        elif region.type == RegionType.Dungeon and region.dungeon:
                            district.dungeons.add(region.dungeon.name)
                            if district not in region.dungeon.districts:
                                region.dungeon.districts.append(district)
                        elif region.name in inaccessible:
                            district.access_points.add(region)

            district.sphere_one = len(check_set.intersection(district.locations)) > 0


def find_reachable_locations(state, player):
    check_set = set()
    for region in state.reachable_regions[player]:
        for location in region.locations:
            if location.can_reach(state) and not location.forced_item and location.real:
                check_set.add(location.name)
    return check_set


inaccessible_regions_std = {'Desert Mouth', 'Bumper Cave Ledge', 'Skull Woods Forest (West)',
                            'Dark Death Mountain Ledge', 'Dark Death Mountain Isolated Ledge',
                            'Death Mountain Floating Island'}


inaccessible_regions_inv = {'Desert Mouth', 'Maze Race Ledge', 'Desert Ledge',
                            'Desert Ledge Keep', 'Hyrule Castle Ledge', 'Mountain Pass Ledge'}
