from typing import TYPE_CHECKING

from BaseClasses import Region
from rule_builder.rules import Has
from worlds.deltarune.Regions import Regions, add_location_to_region
from worlds.deltarune.chapter_5.Locations import chapter5_locations
from worlds.deltarune.Items import items, ItemIDs, glitched_item_name
from worlds.deltarune.Locations import locations, LocationIDs

if TYPE_CHECKING:
    from worlds.deltarune import DeltaruneWorld


def create_regions(world: "DeltaruneWorld"):
    pink_room = Region(Regions.ch5_pink_room, world.player, world.multiworld)
    flower_rewards = Region(Regions.ch5_flower_rewards, world.player, world.multiworld)
    regions = [pink_room, flower_rewards]

    for region in regions:
        if region.name in chapter5_locations:
            add_location_to_region(region, chapter5_locations[region.name], world)
        world.multiworld.regions.append(region)

    # world.get_region(Regions.chapter_5).connect(castle_town)

    pink_room.connect(
        flower_rewards,
        rule=Has(items[ItemIDs.pinkcoin], 16) | Has(items[ItemIDs.pinkcoin]) & Has(glitched_item_name),
    )
