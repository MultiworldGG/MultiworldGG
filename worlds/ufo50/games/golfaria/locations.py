from enum import IntEnum
from typing import TYPE_CHECKING, NamedTuple

from BaseClasses import Region, Location, Item, ItemClassification
from worlds.generic.Rules import add_rule

from ...constants import get_game_base_id

if TYPE_CHECKING:
    from ... import UFO50World


class LocationInfo(NamedTuple):
    id_offset: int
    region_name: str


location_table: dict[str, LocationInfo] = {
    "Underputt Club 1": LocationInfo(1, "Start"),
    "Underputt Club 2": LocationInfo(2, "Start"),
    "Downswing Dip Club": LocationInfo(3, "Start"),
    "Up N Over Cove Club": LocationInfo(4, "Forest"),
    "Gritty Grip Grotto Club": LocationInfo(5, "Start"),
    "Moebius Hole Club": LocationInfo(6, "Forest"),
    "Rooted Route Dropdown Club": LocationInfo(7, "Forest"),
    "Rooted Route Sand Roll Club": LocationInfo(8, "Forest"),
    "Rooted Route Blocked Club": LocationInfo(9, "Forest"),
    "Rooted Route Water Roll Club": LocationInfo(10, "Forest"),
    "Tee Temple Club 1": LocationInfo(11, "Temple"),
    "Tee Temple Club 2": LocationInfo(12, "Temple"),
    "Gur Grotto Club 1": LocationInfo(13, "Mountain"),
    "Gur Grotto Club 2": LocationInfo(14, "Start"),
    "Mulligan Caverns Club": LocationInfo(15, "Mountain"),
    "Calm Cave Club": LocationInfo(16, "Start"),
    "Driver Depths Club": LocationInfo(17, "Mountain"),
    "Soggy Sand Sump Club": LocationInfo(18, "Desert"),
    "Wormburn Way Club": LocationInfo(19, "Desert"),
    "Winding Wetway Club": LocationInfo(20, "Islands"),
    "South Green Parbot": LocationInfo(21, "Start"),
    "South Rough Parbot": LocationInfo(22, "Start"),
    "West Green Parbot": LocationInfo(23, "Start"),
    "North Green Parbot": LocationInfo(24, "Start"),
    "Mt Driver Parbot": LocationInfo(25, "Temple"),
    "Bunker Dunes Parbot 1": LocationInfo(26, "Desert"),
    "Bunker Dunes Parbot 2": LocationInfo(27, "Desert"),
    "Up And Down Isle Parbot": LocationInfo(28, "Islands"),
    "Arc Archipelago Parbot": LocationInfo(29, "Water"),
    "Underputt Parbot": LocationInfo(30, "Start"),
    "Crumbling Cut Tee": LocationInfo(31, "Mountain"),
    "Water-Wedge Way Tee": LocationInfo(32, "Water"),
    "Sandy Subterra Tee": LocationInfo(33, "Desert"),
    "Tee Temple Tee": LocationInfo(34, "Temple"),
    "South Rough NPC": LocationInfo(41, "Start"),
    "East Green NPC": LocationInfo(42, "Start"),
    "Up N Over Cove NPC": LocationInfo(43, "Start"),
    "Winding Wetway NPC": LocationInfo(44, "Islands"),
    "East Temple NPC": LocationInfo(45, "Temple"),
    "Sandy Subterra NPC": LocationInfo(46, "Desert"),
    "Sandy Sinkhole B NPC": LocationInfo(47, "Desert"),
    "Ocean Pit NPC": LocationInfo(48, "Water"),
    "Brakes Location": LocationInfo(50, "Start"),
    "Block Buster Location": LocationInfo(51, "Temple"),
    "Water Roll Location": LocationInfo(52, "Desert"),
    "Sand Roll Location": LocationInfo(53, "Islands"),
    # "Waking Cave Checkpoint Location": LocationInfo(100, "Islands"),   Starting checkpoint, do not use
    "Wise Ball's Cave Checkpoint Location": LocationInfo(101, "Start"),
    "Calm Cave Checkpoint Location": LocationInfo(102, "Start"),
    "Gur Grotto Checkpoint Location": LocationInfo(103, "Start"),
    "Rooted Route Checkpoint Location": LocationInfo(104, "Forest"),
    "Tee Temple Checkpoint Location": LocationInfo(105, "Temple"),
    "Cave Town Checkpoint Location": LocationInfo(106, "Mountain"),
    "Downswing Dip Checkpoint Location": LocationInfo(107, "Islands"),
    "Winding Wetway Checkpoint Location": LocationInfo(108, "Islands"),
    "Bunker Below Checkpoint Location": LocationInfo(109, "Desert"),
    "Garden": LocationInfo(997, "Temple"),
    "Gold": LocationInfo(998, "Boss"),
    "Cherry": LocationInfo(999, "Boss")
}


# this is for filling out location_name_to_id, it should be static regardless of yaml options
def get_locations() -> dict[str, int]:
    return {f"Golfaria - {name}": data.id_offset + get_game_base_id("Golfaria") for name, data in location_table.items()}


# this should return the location groups for this game, independent of yaml options
# you should include a group that contains all location for this game that is called the same thing as the game
def get_location_groups() -> dict[str, set[str]]:
    location_groups: dict[str, set[str]] = {"Golfaria": {f"Golfaria - {loc_name}" for loc_name in location_table.keys()}}
    return location_groups


# this is not a required function, but a recommended one -- the world class does not call this function
def create_locations(world: "UFO50World", regions: dict[str, Region]) -> None:
    for loc_name, loc_data in location_table.items():
        if loc_name == "Cherry" and "Golfaria" not in world.options.cherry_allowed_games:
            break
        if loc_name in ["Gold", "Cherry"] and "Golfaria" in world.goal_games:
            if (loc_name == "Gold" and "Golfaria" not in world.options.cherry_allowed_games) or loc_name == "Cherry":
                loc = Location(world.player, f"Golfaria - {loc_name}", None, regions[loc_data.region_name])
                loc.place_locked_item(Item("Completed Golfaria", ItemClassification.progression, None, world.player))
                add_rule(world.get_location("Completed All Games"), lambda state: state.has("Completed Golfaria", world.player))
                regions[loc_data.region_name].locations.append(loc)
                break
        loc = Location(world.player, f"Golfaria - {loc_name}", get_game_base_id("Golfaria") + loc_data.id_offset,
                       regions[loc_data.region_name])
        regions[loc_data.region_name].locations.append(loc)
