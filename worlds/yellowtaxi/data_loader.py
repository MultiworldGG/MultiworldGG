from typing import Any, Dict, Set, List

from . import locations
from .names import ItemNames

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
                                      load_json_data("L12.moriosmind.json") |
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

original_portal_costs : List[int] = [
    3,  # "Morio's Home",
    6,  # "Bombeach",
    18, # "Arcade Panik",
    32, # "Pizza Time",
    50, # "Tosla's Offices",
    65, # "Maurizio's City",
    80, # "Crash Test Industries",
    0, # "Morio's Mind",
    0, # "Ruined Observatory",
    130, # "Tosla HQ",
    # 130, # "The Moon",
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

hat_prices : Dict[str, int] = {
    ItemNames.no_hat: 0,
    ItemNames.propeller_cap: 50,
    ItemNames.top_hat: 300,
    ItemNames.morio_hat: 500,
    ItemNames.taxi_stack_hat: 700,
    ItemNames.bomb_hat: 500,
    ItemNames.drink_hat: 500,
    ItemNames.chef_hat: 500,
    ItemNames.spaghetti_hat: 600,
    ItemNames.pot_hat: 300,
    ItemNames.lasagna_hat: 300,
    ItemNames.joystick_hat: 1000,
    ItemNames.slot_machine_hat: 500,
    ItemNames.gelatin_hat: 600,
    ItemNames.mug_hat: 500,
    ItemNames.tosla_employee_hat: 500,
    ItemNames.flexing_hat: 0,
    ItemNames.syringe_hat: 0,
    ItemNames.poop_hat: 600,
    ItemNames.dog_bowl_hat: 500,
    ItemNames.toilet_hat: 700,
    ItemNames.bone_fish_hat: 800,
    ItemNames.spoiler: 600,
    ItemNames.police_lights: 700,
    ItemNames.captain_absurd_hat: 0,
    ItemNames.roidman_hat: 0,
    ItemNames.buzzsaw_hat: 700,
    ItemNames.crusher_hat: 700,
    ItemNames.morios_brain_hat: 500,
    ItemNames.heart_hat: 500,
    ItemNames.moon_globe_hat: 700,
    ItemNames.tower_hat: 500,
    ItemNames.alien_mosk_evil_hat: 700,
    ItemNames.skeleton_taxi_skin: 1000,
    ItemNames.golden_taxi_skin: 5000,
    ItemNames.orbit_hat: 800,
    ItemNames.satellite_dish_hat: 0,
    ItemNames.alien_mosk_good_hat: 0,
    ItemNames.crash_test_dummy_hat: 0,
    ItemNames.dentures_hat: 0,
    ItemNames.mushroom_cloud_hat: 0,
    ItemNames.gym_bros_hat: 0,
    ItemNames.banana_hat: 0,
    ItemNames.bunny_hat: 0,
    ItemNames.inception_top_hat: 0,
    ItemNames.pizza_man_hat: 0,
    ItemNames.toilet_paper_hat: 0,
    ItemNames.pod_hat: 0,
    ItemNames.paper_boat_hat: 0,
    ItemNames.prototype_taxi_skin: 0,
    ItemNames.glitched_taxi_skin: 0,
    ItemNames.tv_hat: 0,
    ItemNames.burger_hat: 0,
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
            reg_locations |= locations.get_hat_locations(None, None, reg["sublevel"], reg["hats"])

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