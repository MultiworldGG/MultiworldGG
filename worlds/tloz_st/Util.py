from typing import Dict
from .data.Locations import LOCATIONS_DATA
from .data.Items import ITEMS, ITEM_GROUPS
from .data.DynamicFlags import DYNAMIC_FLAGS
from .data.Constants import HINTS_ON_SCENE
from .data.Hints import HINT_DATA
from .data.Entrances import ENTRANCES
from .data.DynamicEntrances import DYNAMIC_ENTRANCES

def build_hint_scene_to_watches() -> dict[int, list]:
    res = {}
    for hint_name, hint_data in HINT_DATA.items():
        #loc_names = hint_data.get([hint_name])
        for scene in hint_data.get("scenes", []):
            #for loc in loc_names:
            res.setdefault(scene, []).append(hint_name)
    return res

def build_entrance_id_to_data():
    entrances = {}
    for i in ENTRANCES.values():
        entrances[i.id] = i
    return entrances

def build_location_room_to_watches() -> Dict[int, dict[str, dict]]:
    location_room_to_watches: Dict[int, dict[str, dict]] = {}
    for loc_name, location in LOCATIONS_DATA.items():
        stages, rooms = location.get("stage_id", [0]), location.get("room_id", [0])
        stages = [stages] if isinstance(stages, int) else stages
        rooms = [rooms] if isinstance(rooms, int) else rooms
        room_ids = [stage * 0x100 + room for stage in stages for room in rooms]

        for room_id in room_ids:
            location_room_to_watches.setdefault(room_id, {})
            location_room_to_watches[room_id][loc_name] = location

            # Build Island shops
            if "island_shop" in location:
                for shop_id, shop in HINTS_ON_SCENE.items():
                    if shop_id not in location_room_to_watches:
                        location_room_to_watches[shop_id] = {}
                    if "island_shop" in shop:
                        location_room_to_watches[shop_id][loc_name] = location
            # Add location to multiple rooms
            if "additional_rooms" in location:
                for room in location["additional_rooms"]:
                    if room not in location_room_to_watches:
                        location_room_to_watches[room] = {}
                    location_room_to_watches[room][loc_name] = location
    return location_room_to_watches


def expand_dynamic_groups(data):
    if "has_groups" in data:
        groups = data["has_groups"]
        data["any_has_items"] = data.get("any_has_items", []) + [(i, 1) for i in ITEM_GROUPS[groups[0]]]
        if len(groups) > 1:
            data["any_has_items2"] = [(i, 1) for i in ITEM_GROUPS[groups[1]]]
    if "any_has_groups" in data:
        items = []
        for group in data["any_has_groups"]:
            items.extend(ITEM_GROUPS[group])
        data["any_has_items"] = data.get("any_has_items", []) + [(i, 1) for i in items]
    if "not_has_groups" in data:
        items = []
        for group in data["not_has_groups"]:
            items.extend(ITEM_GROUPS[group])
        data["has_items"] = data.get("has_items", []) + [(i, 0) for i in items]

def _check_slot_data(ctx, data):
    if "has_slot_data" in data:
        for slot, value, *args in data["has_slot_data"]:
            slot_value = ctx.slot_data.get(slot, None)
            # print(f"\t\tTesting slot {slot_value} {type(slot_value)} {value}")
            if type(value) is list:
                if slot_value not in value:
                    return False
            elif type(slot_value) is list:
                if args and args[0] == "not":
                    if value in slot_value:
                        return False
                else:
                    if value not in slot_value:
                        return False
            else:
                if slot_value != value:
                    return False
    return True

def build_scene_to_dynamic_flag(ctx) -> Dict[int, list[dict]]:
    scene_to_dynamic_flag: Dict[int, list[dict]] = {}
    for flag_name, data in DYNAMIC_FLAGS.items():
        data["name"] = flag_name
        if not _check_slot_data(ctx, data):
            continue

        expand_dynamic_groups(data)

        for scene in data.get("on_scenes", []):
            scene_to_dynamic_flag.setdefault(scene, [])
            scene_to_dynamic_flag[scene].append(data)
    return scene_to_dynamic_flag

def build_scene_to_dynamic_entrance(ctx) -> Dict[int, list[dict]]:
    res = {}
    for name, data in DYNAMIC_ENTRANCES.items():
        data["name"] = name
        if not _check_slot_data(ctx, data):
            continue

        entrance_data = ENTRANCES[data["entrance"]]
        expand_dynamic_groups(data)
        if data["destination"] == "_connected_dungeon_entrance":
            destination_data = None
        else:
            destination_data = ENTRANCES[data["destination"]]

        entrance_scene = entrance_data.scene

        # Save er_in_scene values in data
        data["detect_data"] = entrance_data
        data["exit_data"] = destination_data
        res.setdefault(entrance_scene, {})
        res[entrance_scene][name] = data
    return res

def build_location_name_to_id_dict() -> Dict[str, int]:
    location_name_to_id: Dict[str, int] = {}
    for loc_name, location in LOCATIONS_DATA.items():
        # ids are for sending flags
        location_name_to_id[loc_name] = location["id"]
    return location_name_to_id

def build_rabbit_location_id_to_name_dict() -> Dict[int, str]:
    location_id_to_name: Dict[int, str] = {}
    for loc_name, location in LOCATIONS_DATA.items():
        if "rabbit" in location:
            index = location["id"]
            location_id_to_name[index] = loc_name
    return location_id_to_name


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

# Making a dictionary of stamp scenes
def build_scene_to_stamp() -> Dict[int, str]:
    stamp_locations: Dict[int, str] = {}
    for loc_name, location in LOCATIONS_DATA.items():
        if location.get("stamp", None) is not None:
            scene = location.get("stage_id", 0) * 0x100 + location.get("room_id", 0)
            stamp_locations[scene] = loc_name
    return stamp_locations

def build_location_to_goal():
    goal_locations = []
    for loc_name, location in LOCATIONS_DATA.items():
        if location.get("goal"):
            goal_locations.append(loc_name)
    return goal_locations

