from .constants import *
from .enums import Locations, Regions, Items
from .stage_data import microgame_data, game_data, game_scores, score_only_games, game_groups, microgame_flower_data

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import WarioWareWorld

all_locations = {}

for region_name, stage_id in game_data.items():
    if region_name not in score_only_games:
        all_locations[f"{region_name.value} - Clear"] = STAGES | (stage_id << 16)
    for score in game_scores[region_name]:
        all_locations[f"{region_name.value} - {score} Points"] = SCORE | (stage_id << 16) | score & 0xFFFF

for region_name, game_id in microgame_data.items():
    all_locations[f"{region_name.value} - Clear"] = MICROGAME | game_id
    all_locations[f"{region_name.value} - Flower"] = FLOWER | game_id

def count_locations_active(world: "WarioWareWorld"):
    total_count = 0
    for loc in world.get_locations():
        if loc.is_event is None:
            continue
        if loc.item is None:
            total_count += 1
    return total_count

flower_groups = {
    "Flowers": [
        name for name in all_locations.keys() if f" - Flower" in name
    ],
}

location_groups = {
    "Introduction": [name for name in all_locations.keys() if "Introduction -" in name],
    "Jimmy": [name for name in all_locations.keys() if "Jimmy -" in name],
    "Dribble": [name for name in all_locations.keys() if "Dribble -" in name],
    "Mona": [name for name in all_locations.keys() if "Mona -" in name],
    "9-Volt": [name for name in all_locations.keys() if "9-Volt -" in name],
    "9 Volt": [name for name in all_locations.keys() if "9-Volt -" in name],
    "Remix 1": [name for name in all_locations.keys() if "Remix 1 -" in name],
    "Orbulon": [name for name in all_locations.keys() if "Orbulon -" in name],
    "Dr. Crygor": [name for name in all_locations.keys() if "Dr. Crygor -" in name],
    "Crygor": [name for name in all_locations.keys() if "Dr. Crygor -" in name],
    "Kat": [name for name in all_locations.keys() if "Kat -" in name],
    "Remix 2": [name for name in all_locations.keys() if "Remix 2 -" in name],
    "Wario": [name for name in all_locations.keys() if "Wario -" in name],
    "Flowers": [name for name in all_locations.keys() if f" - Flower" in name],
    "Introduction Microgames": [entry for name in game_groups[Items.introduction_bundle] for entry in [f"{name} - Clear", f"{name} - Flower"]],
    "Jimmy Microgames": [entry for name in game_groups[Items.jimmy_bundle] for entry in [f"{name} - Clear", f"{name} - Flower"]],
    "Dribble Microgames": [entry for name in game_groups[Items.dribble_bundle] for entry in [f"{name} - Clear", f"{name} - Flower"]],
    "Mona Microgames": [entry for name in game_groups[Items.mona_bundle] for entry in [f"{name} - Clear", f"{name} - Flower"]],
    "9-Volt Microgames": [entry for name in game_groups[Items.nine_volt_bundle] for entry in [f"{name} - Clear", f"{name} - Flower"]],
    "9 Volt Microgames": [entry for name in game_groups[Items.nine_volt_bundle] for entry in [f"{name} - Clear", f"{name} - Flower"]],
    "Orbulon Microgames": [entry for name in game_groups[Items.orbulon_bundle] for entry in [f"{name} - Clear", f"{name} - Flower"]],
    "Dr. Crygor Microgames": [entry for name in game_groups[Items.crygor_bundle] for entry in [f"{name} - Clear", f"{name} - Flower"]],
    "Crygor Microgames": [entry for name in game_groups[Items.crygor_bundle] for entry in [f"{name} - Clear", f"{name} - Flower"]],
    "Kat Microgames": [entry for name in game_groups[Items.kat_bundle] for entry in [f"{name} - Clear", f"{name} - Flower"]],
    "Wario Microgames": [entry for name in game_groups[Items.wario_bundle] for entry in [f"{name} - Clear", f"{name} - Flower"]],
}

ut_location_id_to_alias: dict[int, str] = {}

for group_name, microgames in game_groups.items():
    current_group = group_name.replace(" Microgame Bundle", "")
    for microgame_name in microgames:
        clear_id = all_locations[f"{microgame_name} - Clear"]
        flower_id = all_locations[f"{microgame_name} - Flower"]
        ut_location_id_to_alias[clear_id] = current_group
        ut_location_id_to_alias[flower_id] = f"{current_group}, {microgame_flower_data[microgame_name]} Points"
