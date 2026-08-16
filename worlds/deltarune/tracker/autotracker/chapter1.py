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
forest_rooms = {
    "room_forest_savepoint1": {"x": 36, "y": 237},
    "room_forest_area0": {"x": 66, "y": 237},
    "room_forest_area1": {"x": 132, "y": 237},
    "room_forest_area2": {"x": 210, "y": 270},
    "room_forest_area2A": {"x": 183, "y": 212},
    "room_forest_puzzle1": {"x": 266, "y": 248},
    "room_forest_beforeclover": {"x": 329, "y": 248},
    "room_forest_area3A": {"x": 308, "y": 218},
    "room_forest_area3": {"x": 394, "y": 258},
    "room_forest_savepoint2": {"x": 33, "y": 86},
    "room_forest_smith": {"x": 25, "y": 60},
    "room_forest_area4": {"x": 108, "y": 68},
    "room_forest_dancers1": {"x": 187, "y": 104},
    "room_forest_secret1": {"x": 187, "y": 177},
    "room_forest_trashmaker": {"x": 248, "y": 106},
    "room_forest_starwalker": {"x": 336, "y": 100},
    "room_forest_area5": {"x": 460, "y": 90},
    "room_man": {"x": 397, "y": 72},
    "room_forest_savepoint_relax": {"x": 520, "y": 106},
    "room_forest_maze1": {"x": 518, "y": 84},
    "room_forest_maze_deadend": {"x": 518, "y": 84},
    "room_forest_maze_susie": {"x": 518, "y": 84},
    "room_forest_maze2": {"x": 518, "y": 84},
    "room_forest_maze_deadend2": {"x": 518, "y": 84},
    "room_forest_savepoint3": {"x": 518, "y": 63},
}
card_castle_rooms = {}


def handle_auto_tracking(data: dict[str, any]):
    if data["current_room"] in unknown_rooms:
        return MapIndex.overview
    if data["current_room"] in fields_rooms:
        return MapIndex.ch1_fields
    if data["current_room"] in great_board_rooms:
        return MapIndex.overview
    if data["current_room"] in forest_rooms:
        return MapIndex.ch1_forest
    if data["current_room"] in card_castle_rooms:
        return MapIndex.overview
    return MapIndex.overview


def handle_player_icon_position(map_index: int, data: dict[str, any]):
    room_info = None

    match map_index:
        case MapIndex.ch1_fields:
            room_info = fields_rooms.get(data["current_room"], None)
        case MapIndex.ch1_forest:
            room_info = forest_rooms.get(data["current_room"], None)

    if room_info == None:
        return None

    return (room_info["x"], room_info["y"], "images/icon/heart.png")
