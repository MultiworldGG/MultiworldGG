from typing import Any, Dict, Set, List

from . import locations

import orjson
import pkgutil

# Load regions from JSON
def load_json_data(data_name: str) -> Dict[str, Any]:
    return orjson.loads(pkgutil.get_data(__name__, "json/" + data_name).decode("utf-8-sig"))

regions_json_data : Dict[str, Any] = (load_json_data("LXX.special.json") |
                                      load_json_data("L00.hub.json") |
                                      load_json_data("L03.morioshome.json") |
                                      load_json_data("L01.bombeach.json") |
                                      load_json_data("L04.arcadepanik.json") |
                                      load_json_data("L02.pizzatime.json") |
                                      load_json_data("L05.toslaoffices.json") |
                                      load_json_data("L06.gymgears.json") |
                                      load_json_data("L07.fecalmatters.json") |
                                      load_json_data("L08.flushedaway.json") |
                                      load_json_data("L09.maurizioscity.json") |
                                      load_json_data("L10.crashtestindustries.json") |
                                      load_json_data("L16.rocket.json") |
                                      load_json_data("L17.babysteps.json") |
                                      load_json_data("L18.gettinggud.json") |
                                      load_json_data("L19.protricks.json")
                                      )

original_portal_level_order : List[str] = [
    "Morio's Home",
    "Bombeach",
    "Arcade Panik",
    "Pizza Time",
    "Tosla's Offices",
    "Maurizio's City",
    "Crash Test Industries",
    "Morio's Mind",
    "Ruined Observatory",
    "Tosla HQ",
    "The Moon",
]

alternative_portal_level_order : List[str] = [
    "Bombeach",
    "Pizza Time",
    "Morio's Home",
    "Arcade Panik",
    "Tosla's Offices",
    "Maurizio's City",
    "Crash Test Industries",
    "Morio's Mind",
    "Ruined Observatory",
    "Tosla HQ",
    "The Moon",
]

grannys_island_level_order : List[str] = [
    "Gym Gears",
    "Fecal Matters",
    "Flushed Away",
]

miscellaneous_level_order : List[str] = [
    "Mosk's Rocket",
    "Baby Steps!",
    "Getting Gud!",
    "Pro Tricks!",
    "Psycho Taxi"
]

original_level_order : List[str] = original_portal_level_order + grannys_island_level_order + miscellaneous_level_order

# TODO: Remove levels as they are finished. Remove this list entirely for v1.0.0
unfinished_levels : List[str] = [
    "Morio's Mind",
    "Ruined Observatory",
    "Tosla HQ",
    "The Moon"
]

level_ids : Dict[str, int] = {
    "Excluded": 11, # HubDemo in vanilla. Fully unused so repurposing

    "Hub": 0,
    "Bombeach": 1,
    "Pizza Time": 2,
    "Morio's Home": 3,
    "Arcade Panik": 4,
    "Tosla's Offices": 5,
    "Gym Gears": 6,
    "Fecal Matters": 7,
    "Flushed Away": 8,
    "Maurizio's City": 9,
    "Crash Test Industries": 10,
    "Morio's Mind": 12,
    "Ruined Observatory": 13,
    "Tosla HQ": 14,
    "The Moon": 15,
    "Mosk's Rocket": 16,
    "Baby Steps!": 17,
    "Getting Gud!": 18,
    "Pro Tricks!": 19,
    "Psycho Taxi": 20,
}

special_starting_areas : Dict[str, str] = {
    "Morio's Home": "Morio's Island",
    "Arcade Panik": "Arcade Plaza",
    "Tosla's Offices": "Tosla Square",
    "Psycho Taxi": "",
}

# Load static locations list
def get_all_locations(json_data: Dict[str, Any]) -> Dict[str, int | None]:
    # Get all location ids from JSON
    game_locations: Dict[str, int | None] = {}
    location_keys : List[str] = [
        "gears",
        "bunnies",
        "safes",
        "chests",
        "coinbags",
        "coins",
        "checkpoints",
        "cheeses",
        # Hats are handled specially
    ]
    for reg_name in json_data.keys():
        reg = json_data[reg_name]
        reg_locations : Dict[str, int | None] = {}
        for key in location_keys:
            if key in reg.keys():
                reg_locations |= reg[key]

        if "hats" in reg.keys():
            reg_locations |= locations.get_hat_locations(None, reg["sublevel"], reg["hats"])

        reg_locations |= locations.get_special_locations(None, reg_name)
        game_locations.update(reg_locations)
        for location in reg_locations:
            if reg["sublevel"] in all_location_groups:
                all_location_groups[reg["sublevel"]].add(location)
            else:
                all_location_groups[reg["sublevel"]] = {location}


    return game_locations

all_location_groups : Dict[str, Set[str]] = {}
all_locations: Dict[str, int | None] = get_all_locations(regions_json_data)