from typing import TYPE_CHECKING

from BaseClasses import Region

from .locations import create_locations
from .rules import create_rules

if TYPE_CHECKING:
    from ... import UFO50World


regions: list[str] = [
    "Menu",
    "Start",
    "Temple",
    "Mountain",
    "Forest",
    "Desert",
    "Islands",
    "Water",
    "Boss"
]


# this function is required, and its only argument can be the world class
# it must return the regions that it created
# it is recommended that you prepend each region name with the game it is from to avoid overlap
def create_regions_and_rules(world: "UFO50World") -> dict[str, Region]:
    golfaria_regions: dict[str, Region] = {}
    for region_name in regions:
        golfaria_regions[region_name] = Region(f"Golfaria - {region_name}", world.player, world.multiworld)

    create_locations(world, golfaria_regions)
    create_rules(world, golfaria_regions)

    return golfaria_regions
