from typing import TYPE_CHECKING

from BaseClasses import Region

from .locations import create_locations

if TYPE_CHECKING:
    from ... import UFO50World

# adapted from Porgy

regions: list[str] = [
    "Menu",
    "The Party House",
]


# this function is required, and its only argument can be the world class
# it must return the regions that it created
# it is recommended that you prepend each region name with the game it is from to avoid overlap
def create_regions_and_rules(world: "UFO50World") -> dict[str, Region]:
    party_house_regions: dict[str, Region] = {}
    for region_name in regions:
        party_house_regions[region_name] = Region(f"Party House - {region_name}", world.player, world.multiworld)

    create_locations(world, party_house_regions)
    party_house_regions["Menu"].connect(party_house_regions["The Party House"])

    return party_house_regions