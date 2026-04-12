from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from BaseClasses import Region

if TYPE_CHECKING:
    from .world import Schedule1World as Schedule1World

# A region is a container for locations ("checks"), which connects to other regions via "Entrance" objects.
# Many games will model their Regions after physical in-game places, but you can also have more abstract regions.
# For a location to be in logic, its containing region must be reachable.
# The Entrances connecting regions can have rules - more on that in rules.py.
# This makes regions especially useful for traversal logic ("Can the player reach this part of the map?")

# Every location must be inside a region, and you must have at least one region.
# This is why we create regions first, and then later we create the locations (in locations.py).


def create_and_connect_regions(world: Schedule1World, region_data) -> None:
    create_all_regions(world, region_data)
    connect_regions(world, region_data)


def create_all_regions(world: Schedule1World, region_data) -> None:
    # Create all regions from regions.json
    regions = []
    
    for region_name in region_data.regions.keys():
        region = Region(region_name, world.player, world.multiworld)
        regions.append(region)
    
    # Add all regions to multiworld.regions so that AP knows about their existence
    world.multiworld.regions += regions


def connect_regions(world: Schedule1World, region_data) -> None:
    # Load all regions into a dictionary once to avoid repeated get_region calls
    regions_dict: Dict[str, Region] = {
        region_name: world.get_region(region_name)
        for region_name in region_data.regions.keys()
    }
    
    # Connect all regions based on the connections defined in regions.json
    for region_name, region_info in region_data.regions.items():
        source_region = regions_dict[region_name]
        
        # Iterate through all connections for this region
        for connected_region_name in region_info.connections.keys():
            target_region = regions_dict[connected_region_name]
            entrance_name = f"{region_name} to {connected_region_name}"
            source_region.connect(target_region, entrance_name)