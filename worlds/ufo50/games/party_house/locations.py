from typing import TYPE_CHECKING, NamedTuple

from BaseClasses import Region, Location, Item, ItemClassification
from worlds.generic.Rules import add_rule

from ...constants import get_game_base_id

if TYPE_CHECKING:
    from ... import UFO50World


class LocationInfo(NamedTuple):
    id_offset: int
    region_name: str = "The Party House"


location_table: dict[str, LocationInfo] = {
    "Alien Invitation": LocationInfo(0),
    "High or Low": LocationInfo(1),
    "Best Wishes": LocationInfo(2),
    "Money Management": LocationInfo(3),
    "A Magical Night": LocationInfo(4),

    "Garden": LocationInfo(997),
    "Gold": LocationInfo(998),
    "Cherry": LocationInfo(999)
}


def get_locations() -> dict[str, int]:
    return {f"Party House - {name}": data.id_offset + get_game_base_id("Party House") for name, data in location_table.items()}


def get_location_groups() -> dict[str, set[str]]:
    location_groups: dict[str, set[str]] = {"Party House": {f"Party House - {loc_name}"
                                                            for loc_name in location_table.keys()}}
    return location_groups


def create_locations(world: "UFO50World", regions: dict[str, Region]) -> None:
    for loc_name, loc_data in location_table.items():
        if loc_name == "Cherry" and "Party House" not in world.options.cherry_allowed_games:
            break
        if loc_name in ["Gold", "Cherry"] and "Party House" in world.goal_games:
            if (loc_name == "Gold" and "Party House" not in world.options.cherry_allowed_games) or loc_name == "Cherry":
                loc = Location(world.player, f"Party House - {loc_name}", None, regions[loc_data.region_name])
                loc.place_locked_item(Item("Completed Party House", ItemClassification.progression, None, world.player))
                add_rule(world.get_location("Completed All Games"),
                         lambda state: state.has("Completed Party House", world.player))
                regions[loc_data.region_name].locations.append(loc)
                break

        loc = Location(world.player, f"Party House - {loc_name}", get_game_base_id("Party House") + loc_data.id_offset,
                       regions[loc_data.region_name])
        regions[loc_data.region_name].locations.append(loc)
