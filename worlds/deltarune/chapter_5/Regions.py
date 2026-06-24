from typing import TYPE_CHECKING

from worlds.deltarune.Regions import Regions, add_location_to_region
from worlds.deltarune.chapter_5.Locations import chapter5_locations
from worlds.deltarune.Items import items, ItemIDs, glitched_item_name
from worlds.deltarune.Locations import locations, LocationIDs

if TYPE_CHECKING:
    from worlds.deltarune import DeltaruneWorld


def create_regions(world: "DeltaruneWorld"):
    regions = []

    for region in regions:
        if region.name in chapter5_locations:
            add_location_to_region(region, chapter5_locations[region.name], world)
        world.multiworld.regions.append(region)
