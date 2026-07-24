from typing import TYPE_CHECKING
from BaseClasses import Region, Location

if TYPE_CHECKING:
    from . import XenobladeXWorld


def init_region(world: "XenobladeXWorld", region_name: str) -> None:
    """Initialize the new region if it was not done before and establish the connection rules,
        based on its predecessors, if applicable"""
    if region_name not in [reg.name for reg in world.get_regions()]:
        world.multiworld.regions += [Region(region_name, world.player, world.multiworld)]


def add_region_location(world: "XenobladeXWorld", region_name: str, location: Location) -> Location:
    init_region(world, region_name)
    region = world.get_region(region_name)
    location.parent_region = region
    region.locations += [location]
    return location
