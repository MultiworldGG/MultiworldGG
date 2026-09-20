from typing import Dict

from .DSZeldaClient.LocationClass import DSLocation
from .data import LOCATIONS_DATA, DYNAMIC_FLAGS
from .data.Items import ITEMS
from .data.Hints import HINT_DATA
from .data.Entrances import ENTRANCES
from .DSZeldaClient.subclasses import compare_slot_data

def build_entrance_id_to_data():
    entrances = {}
    for i in ENTRANCES.values():
        entrances[i.id] = i
    return entrances

def build_hint_scene_to_watches() -> dict[int, list[str]]:
    hint_room_to_watches: dict[int, list[str]] = {}
    for name, data in HINT_DATA.items():
        for scene in data["scenes"]:
            hint_room_to_watches.setdefault(scene, [])
            hint_room_to_watches[scene].append(name)
    return hint_room_to_watches


def build_location_room_to_watches() -> Dict[int, dict[str, DSLocation]]:
    location_room_to_watches: Dict[int, dict[str, DSLocation]] = {}
    for loc_name, location in LOCATIONS_DATA.items():
        if location.scenes:
            for scene in location.scenes:
                location_room_to_watches.setdefault(scene, {})
                location_room_to_watches[scene][loc_name] = location

    return location_room_to_watches


def build_scene_to_dynamic_flag(ctx) -> Dict[int, list[dict]]:
    scene_to_dynamic_flag: Dict[int, list[dict]] = {}

    for flag_name, data in DYNAMIC_FLAGS.items():
        data["name"] = flag_name
        if not compare_slot_data(ctx, data):
            continue

        for scene in data.get("on_scenes", []):
            scene_to_dynamic_flag.setdefault(scene, [])
            scene_to_dynamic_flag[scene].append(data)
    return scene_to_dynamic_flag

def build_scene_to_dynamic_entrance(ctx) -> dict:
    return {}

def build_location_name_to_id_dict() -> Dict[str, int]:
    location_name_to_id: Dict[str, int] = {}
    for loc_name, location in LOCATIONS_DATA.items():
        # ids are for sending flags
        location_name_to_id[loc_name] = location["id"]
    return location_name_to_id


def build_item_name_to_id_dict() -> Dict[str, int]:
    item_name_to_id: Dict[str, int] = {}
    for item_name, item in ITEMS.items():
        item_name_to_id[item_name] = item.id
    return item_name_to_id


def build_item_id_to_name_dict() -> Dict[int, str]:
    item_id_to_name: Dict[int, str] = {}
    for item_name, item in ITEMS.items():
        index = item.id
        item_id_to_name[index] = item_name
    return item_id_to_name

# better title case that .title(), for keeping dungeon names in title case
def title2(s: str):
    res = ""
    words = s.split(' ')
    res += words[0].title()
    for word in words[1:-1]:
        if word.lower() in ['of', "the", "and", "or", "in", "a", "an", "to", "but", "for", "so", "by", "in", "at"]:
            res += " " + word.lower()
        else:
            res += " " + word.title()
    res += " " + words[-1].title()
    return res