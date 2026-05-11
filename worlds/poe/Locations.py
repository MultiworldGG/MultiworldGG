import json
import pkgutil
from typing import Dict, TypedDict
from BaseClasses import Location
from worlds.poe.data import LocationTable


class PathOfExileLocation(Location):
    game = "Path of Exile"

def get_base_item_locations ():
    """
    Returns a list of all locations based on base items types in the Path of Exile world.

    """
    return base_item_type_locations


def get_location_id_from_item_name(item_name: str) -> int | None:
    """
    Returns the location ID for a given item name.
    
    Args:
        item_name (str): The name of the item to find the location ID for.
    
    Returns:
        int | None: The location ID if found, otherwise None.
    """
    for loc_id, loc in base_item_type_locations.items():
        if loc.get('baseItem') == item_name:
            return loc_id
    return None

class LocationDict(TypedDict, total=False):
    baseItem: str|None
    placeInAct: str|None
    dropLevel: int|None
    level: int|None
    areaLevel: int|None
    name: str
    act: int
    id: int

#load the json from ./data/bosses.json


acts = [
    {"act": 0.2, "maxMonsterLevel": 2}, # man these roas are tough lol.
    {"act": 1, "maxMonsterLevel": 13},
    {"act": 2, "maxMonsterLevel": 23},
    {"act": 3, "maxMonsterLevel": 33},
    {"act": 4, "maxMonsterLevel": 40},
    {"act": 5, "maxMonsterLevel": 45},
    {"act": 6, "maxMonsterLevel": 50},
    {"act": 7, "maxMonsterLevel": 54},
    {"act": 8, "maxMonsterLevel": 60},
    {"act": 9, "maxMonsterLevel": 64},
    {"act": 10, "maxMonsterLevel": 67},
    {"act": 11, "maxMonsterLevel": 86},
]

def get_lvl_location_name_from_lvl(level: int) -> str: return f"Reach Level {level}"
# based off of baseItemTypes.json
id_by_level_location_name = {i['name']: i['id'] for i in LocationTable.level_location_table.values() if 'name' in i}
base_item_names_set = LocationTable.base_item_set
base_item_type_locations: Dict[int, LocationDict] = LocationTable.base_item_location_table
level_locations: Dict[int, LocationDict] = LocationTable.level_location_table
base_item_locations_by_base_item_name: Dict[str, LocationDict] = {loc['baseItem']: loc for loc in base_item_type_locations.values()}

bosses = LocationTable.bosses_dict
bosses_by_id = {b['id']: b for b in bosses.values()}
area_locations: Dict[int, LocationDict] = LocationTable.area_location_table
full_locations = {**base_item_type_locations, **level_locations, **area_locations}