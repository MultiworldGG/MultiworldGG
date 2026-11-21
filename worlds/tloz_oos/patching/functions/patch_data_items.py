import random
from typing import Any

from ...data.items import RING_LIST
from ...data.locations import LOCATIONS_DATA
from ...world import OracleOfSeasonsWorld


def interpret_location_data(patch_data: dict[str, Any]) -> None:
    patch_locations_data = patch_data["locations"]
    new_patch_locations_data = {}
    for location_name, location_data in LOCATIONS_DATA.items():
        if "owl_id" in location_data:
            continue
        location_id = str(OracleOfSeasonsWorld.location_name_to_id[location_name])
        if location_id in patch_locations_data:
            patch_location_data = patch_locations_data[location_id]
            if "player" not in patch_location_data:
                # If it is local, do not rely on a name in the patch data, but its ID
                item_name = OracleOfSeasonsWorld.item_id_to_name[patch_location_data["item_code"]]
                patch_location_data["item"] = item_name
            new_patch_locations_data[location_name] = patch_location_data
            continue
        # Set item to vanilla
        vanilla_item = location_data["vanilla_item"]
        if vanilla_item == "Filler Item":
            vanilla_item = "Friendship Ring"
        elif vanilla_item == vanilla_item == "Random Ring":
            vanilla_item = random.choice(RING_LIST)
        new_patch_locations_data[location_name] = {"item": vanilla_item}
    patch_data["locations"] = new_patch_locations_data