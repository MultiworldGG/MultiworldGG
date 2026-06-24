from worlds.deltarune.tracker import MapIndex

unknown_rooms = {}
fields_rooms = {
    "room_field_start": {"x": 20, "y": 80},
    "room_field_forest": {"x": 28, "y": 115},
    "room_field1": {"x": 85, "y": 116},
    "room_field2": {"x": 39, "y": 164},
    "room_field2A": {"x": 32, "y": 202},
    "room_field_topchef": {"x": 114, "y": 165},
    "room_field_puzzle1": {"x": 196, "y": 161},
    "room_field_maze": {"x": 272, "y": 188},
    "room_field_puzzle2": {"x": 346, "y": 207},
    "room_field_getsusie": {"x": 380, "y": 209},
    "room_field_shop1": {"x": 389, "y": 181},
    "room_field_puzzletutorial": {"x": 354, "y": 177},
    "room_field3": {"x": 428, "y": 177},
    "room_field_boxpuzzle": {"x": 490, "y": 179},
    "room_field4": {"x": 368, "y": 137},
    "room_field_secret1": {"x": 380, "y": 108},
}
great_board_rooms = {}
forest_rooms = {}
card_castle_rooms = {}


def handle_auto_tracking(data: dict[str, any]):
    if data["current_room"] in unknown_rooms:
        return MapIndex.overview
    if data["current_room"] in fields_rooms:
        return MapIndex.ch1_fields
    if data["current_room"] in great_board_rooms:
        return MapIndex.overview
    if data["current_room"] in forest_rooms:
        return MapIndex.overview
    if data["current_room"] in card_castle_rooms:
        return MapIndex.overview
    return MapIndex.ch1_fields


def handle_player_icon_position(map_index: int, data: dict[str, any]):
    match map_index:
        case MapIndex.ch1_fields:
            room_info = fields_rooms.get(data["current_room"], None)

    if room_info == None:
        return None

    return (room_info["x"], room_info["y"], "images/icon/heart.png")
