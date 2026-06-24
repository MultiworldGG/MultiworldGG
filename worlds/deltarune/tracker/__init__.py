from worlds.deltarune.tracker.MapIndex import MapIndex

from worlds.deltarune.tracker.autotracker.chapter1 import (
    handle_auto_tracking as chapter1_handle_auto_tracking,
    handle_player_icon_position as chapter1_handle_player_icon_position,
)

map_without_position_icon = [MapIndex.overview]


def handle_auto_tracking(data: dict[str, any]):
    if type(data) != dict:
        return MapIndex.overview

    match data.get("current_chapter", -1):
        case 1:
            return chapter1_handle_auto_tracking(data)
        case _:
            return MapIndex.overview


def handle_player_icon_position(map_index: int, data: dict[str, any]):
    if map_index in map_without_position_icon:
        return None

    if type(data) != dict:
        return MapIndex.overview

    match data.get("current_chapter", -1):
        case 1:
            return chapter1_handle_player_icon_position(map_index, data)
        case _:
            return None
