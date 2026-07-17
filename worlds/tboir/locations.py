from typing import Dict, Set

from worlds.tboir.options import AdditionalItemLocationsPerStage
from .game_data import data

def location_list():
    locations = []

    for stage, floor in data["regions"].items():
        if "rooms" in floor:
            for room_condition in floor["rooms"]:
                room, *_ = room_condition.split('&')
                locations.append(f'{stage} - {room}')
    
    for boss, reward in data["boss_rewards"].items():
        for i in range(reward["amount"]):
            locations.append(f'{boss} Reward #{i+1}')

    stages = list(AdditionalItemLocationsPerStage.valid_keys)
    stages.sort()
    for stage in stages:
        for i in range(10):
            locations.append(f'{stage} - Item #{i+1}')

    return locations


def location_group_list():
    location_name_groups: Dict[str, Set[str]] = {}

    for stage, floor in data["regions"].items():
        if "rooms" in floor:
            for room_condition in floor["rooms"]:
                room, *_ = room_condition.split('&')
                add_to_location_group(location_name_groups, "Rooms", f'{stage} - {room}')
                add_to_location_group(location_name_groups, stage, f'{stage} - {room}')
                add_to_location_group(location_name_groups, f'{room}s', f'{stage} - {room}')
    
    for boss, reward in data["boss_rewards"].items():
        for i in range(reward["amount"]):
            add_to_location_group(location_name_groups, "Boss Rewards", f'{boss} Reward #{i+1}')

    stages = list(AdditionalItemLocationsPerStage.valid_keys)
    stages.sort()
    for stage in stages:
        for i in range(10):
            add_to_location_group(location_name_groups, "AP Items", f'{stage} - Item #{i+1}')
            add_to_location_group(location_name_groups, stage, f'{stage} - Item #{i+1}')

    return location_name_groups

def add_to_location_group(location_name_groups, group, location):
    if group not in location_name_groups:
        location_name_groups[group] = set()
    location_name_groups[group].add(location)