from rule_builder.rules import HasAny, Has, HasGroupUnique, HasAll

from typing import List, Dict, TYPE_CHECKING
from BaseClasses import Region, Location
from .Locations import LocationData
from .Rules import secret_characters
if TYPE_CHECKING:
    from . import SSBMWorld


class SSBMLocation(Location):
    game: str = "Super Smash Bros. Melee"

    def __init__(self, player: int, name: str = " ", address: int = None, parent=None):
        super().__init__(player, name, address, parent)


def init_areas(world: "SSBMWorld", locations: List[LocationData]) -> None:
    multiworld = world.multiworld
    player = world.player
    locations_per_region = get_locations_per_region(locations)

    regions = [
        create_region(world, player, locations_per_region, "Game Base"),
        create_region(world, player, locations_per_region, "Game Menu"),
        create_region(world, player, locations_per_region, "Any Melee"),
        create_region(world, player, locations_per_region, "Adventure Mode"),
        create_region(world, player, locations_per_region, "Classic Mode"),
        create_region(world, player, locations_per_region, "All-Star Mode"),
        create_region(world, player, locations_per_region, "Event Match Mode"),
        create_region(world, player, locations_per_region, "Target Test"),
        create_region(world, player, locations_per_region, "Home-Run Contest"),
        create_region(world, player, locations_per_region, "Multi-Man Melee"),
        create_region(world, player, locations_per_region, "Any Main 1-P"),
        create_region(world, player, locations_per_region, "Events 1-10"),
        create_region(world, player, locations_per_region, "Events 11-15"),
        create_region(world, player, locations_per_region, "Events 16-20"),
        create_region(world, player, locations_per_region, "Events 21-25"),
        create_region(world, player, locations_per_region, "Events 26-29"),
        create_region(world, player, locations_per_region, "Event 30"),
        create_region(world, player, locations_per_region, "Events 31-39"),
        create_region(world, player, locations_per_region, "Events 40-50"),
        create_region(world, player, locations_per_region, "Event 51"),
        create_region(world, player, locations_per_region, "Lottery Base"),
        create_region(world, player, locations_per_region, "Lottery Adventure/Classic Clear"),
        create_region(world, player, locations_per_region, "Lottery 200 Vs. Matches"),
        create_region(world, player, locations_per_region, "Lottery Secret Characters")
    ]

    if world.use_250_trophy_pool:
        regions.append(create_region(world, player, locations_per_region, "Lottery 250 Trophies"))
    
    multiworld.regions += regions

    multiworld.get_region("Game Base", player).add_exits(["Game Menu"],
                                                    {"Game Menu": HasGroupUnique("Characters", 1)})

    multiworld.get_region("Game Menu", player).add_exits(["Any Melee", "Adventure Mode", "Classic Mode",
                                                    "All-Star Mode", "Event Match Mode", "Target Test",
                                                    "Home-Run Contest", "Multi-Man Melee", "Lottery Base",
                                                    "Any Main 1-P"],
                                                    {"Adventure Mode": Has("Adventure Mode"),
                                                     "Classic Mode": Has("Classic Mode"),
                                                     "All-Star Mode": Has("All-Star Mode"),
                                                     "Home-Run Contest": HasAll("Home-Run Contest", "Home-Run Bat"),
                                                     "Target Test": Has("Target Test"),
                                                     "Multi-Man Melee": Has("Multi-Man Melee"),
                                                     "Any Main 1-P": HasAny("Adventure Mode", "Classic Mode", "All-Star Mode")})

    multiworld.get_region("Event Match Mode", player).add_exits(["Events 1-10", "Events 11-15", "Events 16-20", "Events 21-25", "Events 26-29", "Event 30", "Events 31-39", "Events 40-50", "Event 51"],
                                                    {"Events 11-15": Has("Progressive Event Pack", 1),
                                                    "Events 16-20": Has("Progressive Event Pack", 2),
                                                    "Events 21-25": Has("Progressive Event Pack", 3),
                                                    "Events 26-29": Has("Progressive Event Pack", 4),
                                                    "Event 30": Has("Progressive Event Pack", 5),
                                                    "Events 31-39": Has("Progressive Event Pack", 6),
                                                    "Events 40-50": Has("Progressive Event Pack", 7),
                                                    "Event 51": Has("Progressive Event Pack", 8)})

    if world.options.lottery_pool_mode:
        multiworld.get_region("Lottery Base", player).add_exits(["Lottery Adventure/Classic Clear", "Lottery 200 Vs. Matches", "Lottery Secret Characters", "Lottery 250 Trophies"],
                                                        {"Lottery Adventure/Classic Clear": Has("Progressive Lottery Pool", 1) | Has("Lottery Pool Upgrade (Adventure/Classic Clear)"),
                                                        "Lottery 200 Vs. Matches": Has("Progressive Lottery Pool", 2) | Has("Lottery Pool Upgrade (200 Vs. Matches)"),
                                                        "Lottery Secret Characters": Has("Progressive Lottery Pool", 3) | Has("Lottery Pool Upgrade (Secret Characters)"),
                                                        "Lottery 250 Trophies": Has("Progressive Lottery Pool", 4) | Has("Lottery Pool Upgrade (250 Trophies)")})
    else:
        multiworld.get_region("Lottery Base", player).add_exits(["Lottery Adventure/Classic Clear", "Lottery 200 Vs. Matches", "Lottery Secret Characters"],
                                                        {"Lottery Adventure/Classic Clear": HasAll("Adventure Mode", "Classic Mode"),
                                                        "Lottery Secret Characters": HasAll(*secret_characters)})
        if world.use_250_trophy_pool:
            multiworld.get_region("Lottery Base", player).add_exits(["Lottery 250 Trophies"],
                                                            {"Lottery Adventure/Classic Clear": HasGroupUnique("Trophies", 250)})


def create_location(player: int, location_data: LocationData, region: Region) -> Location:
    location = SSBMLocation(player, location_data.name, location_data.code, region)
    location.region = location_data.region

    return location


def create_region(world: "SSBMWorld", player: int, locations_per_region: Dict[str, List[LocationData]], name: str) -> Region:
    region = Region(name, player, world.multiworld)

    if name in locations_per_region:
        for location_data in locations_per_region[name]:
            location = create_location(player, location_data, region)
            region.locations.append(location)

    return region


def get_locations_per_region(locations: List[LocationData]) -> Dict[str, List[LocationData]]:
    per_region: Dict[str, List[LocationData]] = {}

    for location in locations:
        per_region.setdefault(location.region, []).append(location)

    return per_region
    