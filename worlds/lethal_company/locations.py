import math
from typing import Dict, List, TYPE_CHECKING
from BaseClasses import Location
from .imported import data
from .options import ChecksPerMoon, NumQuotas
from .custom_content import custom_content

if TYPE_CHECKING:
    from . import LethalCompanyWorld


class LethalCompanyLocation(Location):
    game: str = f"Lethal Company{custom_content['name']}"


lc_locations_start_id = 1966720
max_id = lc_locations_start_id


def get_default_location_map():
    log_names = [
        "Mummy",
        "Swing of Things",
        "Autopilot",
        "Golden Planet",
        "Sound Behind the Wall",
        "Goodbye",
        "Screams",
        "Idea",
        "Nonsense",
        "Hiding",
        "Real Job",
        "Desmond",
        "Team Synergy",
        "Letter of Resignation"
    ]

    bestiary_names = [[key for key in monster.keys()][0] for monster in data["bestiary"]]

    moons = [moon for moon in data.get("moons")]

    scrap_names = []

    for item in data["scrap"]:
        key = [key for key in item.keys()][0]
        scrap_names.append(key)

    for moon in moons:
        if not f"AP Apparatus - {moon}" in scrap_names:
            scrap_names.append(f"AP Apparatus - {moon}")

    location_result = {}

    for i in range(len(moons)):
        for j in range(ChecksPerMoon.range_end):
            location_result.update(check_location(f"{moons[i]} check {j + 1}")) # maybe change this to Offense Grade check 1...The current name seems to confuse people
    for i in range(NumQuotas.range_end):
        location_result.update(check_location(f"Quota check {i + 1}"))
    for i in range(len(log_names)):
        location_result.update(check_location(f"Log - {log_names[i]}"))
    for i in range(len(bestiary_names)):
        location_result.update(check_location(f"Bestiary Entry - {bestiary_names[i]}"))
    for i in range(len(scrap_names)):
        location_result.update(check_location(f"Scrap - {scrap_names[i]}"))
    return location_result


def generate_locations(world: "LethalCompanyWorld"):
    world.log_names = [
        "Mummy",
        "Swing of Things",
        "Autopilot",
        "Golden Planet",
        "Sound Behind the Wall",
        "Goodbye",
        "Screams",
        "Idea",
        "Nonsense",
        "Hiding",
        "Real Job",
        "Desmond",
        "Team Synergy",
        "Letter of Resignation"
    ]

    #world.bestiary_names = [[key for key in monster.keys() if any(moon["chance"] > 0 for moon in monster[key])][0] for monster in world.imported_data["bestiary"]]
    world.bestiary_names = []
    for monster in world.imported_data["bestiary"]:
        key = [key for key in monster.keys()][0]
        if any(moon["chance"] > 0 for moon in monster[key]):
            world.bestiary_names.append(key)

    moons = [moon for moon in world.imported_data.get("moons")]

    world.scrap_names = []
    removed_scrap = []

    for item in world.imported_data["scrap"]:
        key = [key for key in item.keys()][0]
        # check if the scrap can be found on at least one moon, and add it if so
        if any(moon["chance"] > 0 for moon in item[key]):
            world.scrap_names.append(key)
        else: 
            removed_scrap.append(key)

    if len(removed_scrap) > 0:
        import logging
        logging.warning(f"Warning - The following scrap do not appear to spawn on any moons and have been removed from logic:\n{removed_scrap}")

    # the mod now handles this part before generating the logic string, so we don't need it here
    #for moon in moons:
    #    if not f"AP Apparatus - {moon}" in world.scrap_names:
    #        world.scrap_names.append(f"AP Apparatus - {moon}")
    #        print(f"AP Apparatus - {moon}")

    #if "AP Apparatus - Custom" in world.scrap_names:
    #    world.scrap_names.remove("AP Apparatus - Custom")

    location_result = {}

    for i in range(len(moons)):
        for j in range(world.options.checks_per_moon.value):
            location_result.update(check_location(f"{moons[i]} check {j + 1}")) # maybe change this to Offense Grade check 1...The current name seems to confuse people
    for i in range(world.options.num_quotas.value):
        location_result.update(check_location(f"Quota check {i + 1}"))
    for i in range(len(world.log_names)):
        location_result.update(check_location(f"Log - {world.log_names[i]}"))
    for i in range(len(world.bestiary_names)):
        location_result.update(check_location(f"Bestiary Entry - {world.bestiary_names[i]}"))
    if world.options.scrapsanity.value == 1:
        for i in range(len(world.scrap_names)):
            location_result.update(check_location(f"Scrap - {world.scrap_names[i]}"))
    return location_result


def generate_bestiary_moons(world: "LethalCompanyWorld", chance: float) -> Dict[str, List[str]]:
    bestiary_moons = {

    }

    bestiary_data = world.imported_data["bestiary"]
    for entry in bestiary_data:
        key = [key for key in entry.keys()][0]
        b_moons = []
        for moon in entry[key]:
            if moon["chance"] >= chance:
                b_moons.append(moon["moon_name"])
        if b_moons == []:
                best_moon = max(entry[key], key=lambda moon_spawns: moon_spawns["chance"])
                if best_moon["chance"] > 0:
                    b_moons.append(best_moon["moon_name"])    # ensures that the location is still 'accessible' as long as it can be found SOMEWHERE
                    b_moons.append("excluded")     # special indicator that this location should be excluded
                else:
                    continue            # if the item isn't found ANYWHERE, don't add it
        bestiary_moons[key] = b_moons

    return bestiary_moons


def check_location(location_name: "str") -> Dict[str, int]:
    global max_id
    global locations

    if location_name in locations.keys():
        location_id = locations[location_name]
    else:
        location_id = max_id
        max_id += 1
    locations.update({location_name: location_id})
    return {location_name: location_id}


def generate_scrap_moons(world: "LethalCompanyWorld", chance: float) -> Dict[str, List[str]]:
    scrap_moons = {

    }

    scrap_data = world.imported_data["scrap"]
    for entry in scrap_data:
        key = [key for key in entry.keys()][0]
        s_moons = []
        for moon in entry[key]:
            if moon["chance"] >= chance:
                s_moons.append(moon["moon_name"])
        if s_moons == []:
            best_moon = max(entry[key], key=lambda moon_spawns: moon_spawns["chance"])
            if best_moon["chance"] > 0:
                s_moons.append(best_moon["moon_name"])    # ensures that the location is still 'accessible' as long as it can be found SOMEWHERE
                s_moons.append("excluded")     # special indicator that this location should be excluded
            else:
                continue            # if the item isn't found ANYWHERE, don't add it
        scrap_moons[key] = s_moons

    return scrap_moons


def generate_scrap_moons_alt(world: 'LethalCompanyWorld') -> Dict[str, List[str]]:
    scrap_moons = {

    }

    normal = generate_scrap_moons(world=world, chance=world.options.min_scrap_chance.value/100)

    scrap = [name for name in world.scrap_names]

    for name in scrap:
        if "AP Apparatus" in name:
            scrap.remove(name)
        elif "Archipelago Chest" in name:
            scrap.remove(name)
        elif "Apparatus" in name or "Shotgun" in name or "Kitchen knife" in name or "Hive" in name or "Sapsucker Egg" in name:
            scrap.remove(name)

    items_per_bin = math.floor(len(scrap) / len(world.moons))
    world.multiworld.random.shuffle(scrap)

    for i in range(len(scrap)):
        bin_num = math.floor(i/items_per_bin)
        if bin_num < len(world.moons):
            scrap_moons[scrap[i]] = [world.moons[bin_num]]
        else:
            scrap_moons[scrap[i]] = ["Common"]

    scrap_moons["Archipelago Chest"] = []
    scrap_moons["Apparatus"] = normal["Apparatus"]
    scrap_moons["Shotgun"] = normal["Shotgun"]
    scrap_moons["Kitchen knife"] = normal["Kitchen knife"]
    scrap_moons["Hive"] = normal["Hive"]
    scrap_moons["Sapsucker Egg"] = normal["Sapsucker Egg"]

    for moon in world.moons:
        scrap_moons[f"AP Apparatus - {moon}"] = [moon]
        scrap_moons["Archipelago Chest"].append(moon)

    world.scrap_map = scrap_moons

    inverse_scrap_map = {
        "Common": [],
        "Experimentation": [],
        "Assurance": [],
        "Vow": [],
        "Offense": [],
        "March": [],
        "Adamance": [],
        "Embrion": [],
        "Rend": [],
        "Dine": [],
        "Titan": [],
        "Artifice": []
    }

    for scrap, moons in world.scrap_map.items():
        for moon in moons:
            if not (moon in inverse_scrap_map):
                inverse_scrap_map[moon] = []
            inverse_scrap_map[moon].append(scrap)

    spoiler_string = f"\n{world.player_name}'s Randomized scrap placements:"

    for moon, scrap in inverse_scrap_map.items():
        spoiler_string += f"{moon}: {', '.join(scrap)}\n"

    world.spoiler_text = spoiler_string

    return scrap_moons


locations : Dict[str, int] = {}
