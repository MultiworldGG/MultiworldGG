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
    # Shallows
    "Shallows Piranha Chest": LocationInfo(10, "Shallows"),
    "Shallows Hidden Chest Near Gate": LocationInfo(11, "Shallows"),
    "Shallows Ruins Entrance Chest": LocationInfo(12, "Shallows"),
    "Shallows Bomb Blocked Chest 1": LocationInfo(13, "Shallows"),
    "Shallows Bomb Blocked Chest 2": LocationInfo(14, "Shallows"),
    "Ruins Left of Entrance Chest": LocationInfo(20, "Shallows"),
    "Ruins Center Chest": LocationInfo(21, "Ruins"),
    "Southwest of Ruins Chest": LocationInfo(22, "Ruins"),
    "Piranha Cave Bomb Blocked Chest": LocationInfo(23, "Depths"),
    "Piranha Cave Bottom Right Chest": LocationInfo(24, "Depths"),
    "Boss Area Chest": LocationInfo(30, "Depths"),
    "Slime Cave Upper Chest": LocationInfo(40, "Shallows"),
    "Slime Cave Lower Chest": LocationInfo(41, "Ruins"),
    "Eastern Cave Gift Chest": LocationInfo(50, "Shallows"),
    "Upper Spider Cave Chest": LocationInfo(60, "Depths"),
    "Lower Spider Cave Chest": LocationInfo(61, "Depths"),
    "Jelly Cave Chest": LocationInfo(70, "Depths"),
    "Shallows Lever": LocationInfo(90, "Shallows"),
    "Ruins Lever": LocationInfo(91, "Ruins"),
    "Boss Lever 1": LocationInfo(92, "Depths"),
    "Boss Lever 2": LocationInfo(93, "Depths"),
    "Gift Area Emblem": LocationInfo(100, "Shallows"),
    "Slime Cave Emblem": LocationInfo(101, "Shallows"),
    "Piranha Cave Emblem": LocationInfo(102, "Depths"),
    "Slime Stick Store": LocationInfo(110, "Shallows"),
    "Slime Lance Store": LocationInfo(111, "Ruins"),
    "Slime Trident Store": LocationInfo(112, "Depths"),
    "Shell Stick Store": LocationInfo(113, "Shallows"),
    "Shell Lance Store": LocationInfo(114, "Ruins"),
    "Shell Trident Store": LocationInfo(115, "Depths"),
    "Elec Stick Store": LocationInfo(116, "Shallows"),
    "Elec Lance Store": LocationInfo(117, "Ruins"),
    "Elec Trident Store": LocationInfo(118, "Depths"),
    "Slime Mallet Store": LocationInfo(120, "Shallows"),
    "Slime Sledge Store": LocationInfo(121, "Ruins"),
    "Shell Mallet Store": LocationInfo(122, "Shallows"),
    "Shell Sledge Store": LocationInfo(123, "Ruins"),
    "Elec Mallet Store": LocationInfo(124, "Shallows"),
    "Elec Sledge Store": LocationInfo(125, "Depths"),
    "Slime Lid Store": LocationInfo(130, "Shallows"),
    "Slime Buckler Store": LocationInfo(131, "Ruins"),
    "Slime Tower Store": LocationInfo(132, "Depths"),
    "Shell Lid Store": LocationInfo(133, "Shallows"),
    "Shell Buckler Store": LocationInfo(134, "Ruins"),
    "Shell Tower Store": LocationInfo(135, "Depths"),
    "Elec Lid Store": LocationInfo(136, "Shallows"),
    "Elec Buckler Store": LocationInfo(137, "Ruins"),
    "Elec Tower Store": LocationInfo(138, "Depths"),
    "Small Potion Store": LocationInfo(140, "Shallows"),
    "Medium Potion Store": LocationInfo(141, "Ruins"),
    "Holy Potion Store": LocationInfo(142, "Boss"),
    "Evil Potion Store": LocationInfo(143, "Shallows"),
    "Bomb Store": LocationInfo(150, "Shallows"),
    "Mist Orb Store": LocationInfo(151, "Ruins"),
    "Godblood Store": LocationInfo(152, "Shallows"),
    "Egg Store": LocationInfo(144, "Ruins"),
    "Garden": LocationInfo(997, "Shallows"),
    "Gold": LocationInfo(998, "Boss"),
    "Cherry": LocationInfo(999, "Boss")
}


# this is for filling out location_name_to_id, it should be static regardless of yaml options
def get_locations() -> dict[str, int]:
    return {f"Divers - {name}": data.id_offset + get_game_base_id("Divers") for name, data in location_table.items()}


# this should return the location groups for this game, independent of yaml options
# you should include a group that contains all location for this game that is called the same thing as the game
def get_location_groups() -> dict[str, set[str]]:
    location_groups: dict[str, set[str]] = {"Divers": {f"Divers - {loc_name}" for loc_name in location_table.keys()}}
    return location_groups


# this is not a required function, but a recommended one -- the world class does not call this function
def create_locations(world: "UFO50World", regions: dict[str, Region]) -> None:
    for loc_name, loc_data in location_table.items():
        if loc_name == "Shallows Lever" or loc_name == "Ruins Lever" or loc_name == "Boss Lever 1" or loc_name == "Boss Lever 2":
            if not world.options.divers_lever_check:
                continue
        if loc_name == "Cherry" and "Divers" not in world.options.cherry_allowed_games:
            break
        if loc_name in ["Gold", "Cherry"] and "Divers" in world.goal_games:
            if (loc_name == "Gold" and "Divers" not in world.options.cherry_allowed_games) or loc_name == "Cherry":
                loc = Location(world.player, f"Divers - {loc_name}", None, regions[loc_data.region_name])
                loc.place_locked_item(Item("Completed Divers", ItemClassification.progression, None, world.player))
                add_rule(world.get_location("Completed All Games"), lambda state: state.has("Completed Divers", world.player))
                regions[loc_data.region_name].locations.append(loc)
                break
        loc = Location(world.player, f"Divers - {loc_name}", get_game_base_id("Divers") + loc_data.id_offset,
                       regions[loc_data.region_name])
        regions[loc_data.region_name].locations.append(loc)
