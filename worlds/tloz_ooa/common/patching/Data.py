from typing import Any


def get_item_id_and_subid(item_data: dict[str, dict[str, Any]], item: dict[str, str | bool]) -> tuple[int, int]:
    item_name = item["item"]
    if "player" in item:
        item_name += f"|{item["player"]}"
    item_data = item_data[item_name]
    item_id = item_data["id"]
    item_subid = item_data["subid"] if "subid" in item_data else 0x00
    if item_id == 0x30:
        item_subid = item_subid & 0x7F  # TODO : Remove when/if master key becomes available on non-master key worlds
    return item_id, item_subid