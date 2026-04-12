from typing import Any


def build_location_name_to_id_dict(data: dict[str, dict[str, Any]]) -> dict[str, int]:
    location_name_to_id: dict[str, int] = {}
    for loc_name, location in data.items():
        if "id" in location:
            index = location["id"]
        elif location["flag_byte"] is not None:
            index = location["flag_byte"] * 0x100 + (location["bit_mask"] if "bit_mask" in location else 0x20)
        else:
            continue
        location_name_to_id[loc_name] = index
    return location_name_to_id


def build_item_name_to_id_dict(data: dict[str, dict[str, Any]]) -> dict[str, int]:
    item_name_to_id: dict[str, int] = {}
    for item_name, item in data.items():
        index = item["id"] * 0x100 + (item["subid"] if "subid" in item else 0)
        item_name_to_id[item_name] = index
    return item_name_to_id


def build_item_id_to_name_dict(data: dict[str, dict[str, Any]]) -> dict[int, str]:
    item_id_to_name: dict[int, str] = {}
    for item_name, item in data.items():
        index = item["id"] * 0x100 + (item["subid"] if "subid" in item else 0)
        item_id_to_name[index] = item_name
    return item_id_to_name
