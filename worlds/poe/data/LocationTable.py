import json
import pkgutil
# two-toned boots and fleshripper were duplicates.

base_item_location_array = json.loads(pkgutil.get_data("worlds.poe.data", "BaseItems.json").decode("utf-8"))
base_item_location_table = {}
level_location_array = json.loads(pkgutil.get_data("worlds.poe.data", "LevelLocations.json").decode("utf-8"))
level_location_table = {}
bosses_dict = json.loads(pkgutil.get_data("worlds.poe.data", "Bosses.json").decode("utf-8"))
area_location_array = json.loads(pkgutil.get_data("worlds.poe.data", "AreaLocations.json").decode("utf-8"))
area_location_table = {}

existing_ids = {item['id'] for item in base_item_location_array if item.get('id')} | {item['id'] for item in level_location_array if item.get('id')}  | {item['id'] for item in bosses_dict.values() if item.get('id')}
next_available_default_id = 1
for i, item in enumerate(base_item_location_array, start=1):
    item_id: int
    if item.get('id'):
        item_id = item['id']
    else:
        item_id = next_available_default_id
        item['id'] = item_id
        next_available_default_id += 1
        while next_available_default_id in existing_ids:
            next_available_default_id += 1

    base_item_location_table[item_id] = item

base_item_set = set(item["baseItem"] for item in base_item_location_array)

for i, item in enumerate(level_location_array, start=next_available_default_id):
    item_id: int
    if item.get('id'):
        item_id = item['id']
    else:
        item_id = next_available_default_id
        item['id'] = item_id
        next_available_default_id += 1
        while next_available_default_id in existing_ids:
            next_available_default_id += 1

    level_location_table[item_id] = item

# Area location IDs start at 42000 to avoid conflicts with sequential base/level IDs and boss IDs
AREA_LOCATION_ID_START = 42000
next_area_id = AREA_LOCATION_ID_START
for item in area_location_array:
    if item.get("areaLevel", 0) == 0:
        continue  # skip encampments / towns
    entry = {
        "name": f"Reach {item['areaName']}",
        "act": item["act"],
        "areaLevel": item["areaLevel"],
        "level": item["areaLevel"],  # used by Regions.py for placement
        "id": next_area_id,
    }
    area_location_table[next_area_id] = entry
    next_area_id += 1


if __name__ == "__main__":
    full_location_table = base_item_location_table | level_location_table | area_location_table
    import json
    #print(json.dumps(full_location_table, indent=4))
    print(json.dumps(bosses_dict, indent=4, ensure_ascii=False))