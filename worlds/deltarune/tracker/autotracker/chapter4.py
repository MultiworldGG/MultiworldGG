from worlds.deltarune.tracker import MapIndex

first_sanctuary = {
    "room_dw_church_intro1": {"x": 45, "y": 293},
    "room_dw_church_intropiano": {"x": 121, "y": 293},
    "room_dw_church_staircase": {"x": 178, "y": 293},
    "room_dw_church_glass": {"x": 217, "y": 606},
    "room_dw_church_savepoint": {"x": 251, "y": 606},
    "room_dw_church_intro_guei": {"x": 251, "y": 606},
    "room_dw_church_intro_gerson": {"x": 326, "y": 588},
    "room_dw_church_minorlegend": {"x": 422, "y": 591},
    "room_dw_church_shadowgerson": {"x": 424, "y": 545},
    "room_dw_church_bookcase": {"x": 505, "y": 536},
    "room_dw_church_turtles": {"x": 561, "y": 535},
    "room_dw_church_ripplepuzzle": {"x": 642, "y": 535},
    "room_dw_church_ripseq1": {"x": 642, "y": 535},
    "room_dw_church_ripseq2": {"x": 642, "y": 535},
    "room_dw_church_ripplepuzzle_postgers": {"x": 746, "y": 531},
    "room_dw_church_lantern_hallway": {"x": 454, "y": 479},
    "room_dw_church_darkmaze": {"x": 454, "y": 420},
    "room_dw_church_gersonstudy": {"x": 525, "y": 417},
    "room_dw_church_nwconnect": {"x": 514, "y": 331},
    "room_dw_church_biblioxencounter": {"x": 504, "y": 264},
    "room_dw_church_bookshelfpuzzle_rev": {"x": 502, "y": 204},
    "room_dw_church_worshiproom": {"x": 448, "y": 174},
    "room_dw_church_tallbookcases": {"x": 480, "y": 144},
    "room_dw_church_pianopuzzle": {"x": 481, "y": 71},
    "room_dw_church_pianopiece_left": {"x": 368, "y": 106},
    "room_dw_church_pianopiece_right": {"x": 565, "y": 130},
    "room_dw_church_pianopiece_rightprophecy": {"x": 600, "y": 90},
    "room_dw_church_jackenstein": {"x": 737, "y": 157},
    "room_dw_church_secretpiano": {"x": 512, "y": 116},
    "room_dw_church_arena": {"x": 553, "y": 456},
    "room_dw_church_rippleworship": {"x": 724, "y": 460},
    "room_dw_church_holywatercooler": {"x": 305, "y": 520},
    "room_dw_church_rightconnect": {"x": 600, "y": 403},
    "room_dw_church_stairspreview": {"x": 736, "y": 406},
    "room_dw_church_trueclimbadventure": {"x": 605, "y": 347},
    "room_dw_church_sideclimb": {"x": 730, "y": 323},
    "room_dw_church_organpuzzle": {"x": 665, "y": 196},
    "room_dw_church_mizzleencounter": {"x": 765, "y": 202},
    "room_dw_church_bellhall_bookroom": {"x": 860, "y": 195},
    "room_dw_church_bellhall_curtain": {"x": 860, "y": 158},
    "room_dw_church_northprophecies": {"x": 270, "y": 328},
    "room_dw_church_knightclimb": {"x": 143, "y": 259},
    "room_dw_church_knightclimb_post": {"x": 143, "y": 228},
    "room_dw_church_fountain": {"x": 206, "y": 199},
}


def handle_auto_tracking(data: dict[str, any]):
    if data["current_room"] in first_sanctuary:
        return MapIndex.ch4_first_sanctuary
    return MapIndex.overview


def handle_player_icon_position(map_index: int, data: dict[str, any]):
    room_info = None

    match map_index:
        case MapIndex.ch4_first_sanctuary:
            room_info = first_sanctuary.get(data["current_room"], None)

    if room_info == None:
        return None

    return (room_info["x"], room_info["y"], "images/icon/heart.png")
