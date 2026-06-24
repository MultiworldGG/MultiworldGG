class MkddMemAddresses():
    """
    Collection of memory addresses of relevant data.
    Inherit this class to specify addresses for different versions.

    Property suffixes tell the data type (b = byte, h = half word, w = word, s = string, f = float, x = table).
    Pointers are always words.
    """
    # Vanilla addresses:
    mode_w: int
    """Current game mode. Updated after select character screen. See game_data.Modes for values."""
    cup_w: int
    """Cup selection. 0 Mushroom Cup - 4 All Cup Tour."""
    menu_course_w: int
    """Currently selected course inside a cup. Doesn't update in midst of a gp. 0-3."""
    human_players_b: int
    """Amount of human players. Used to check if actually playing or in attraction mode."""
    vehicle_class_w: int
    """Currently selected class. Updated after select character screen. 0 = 50cc, 3 = Mirror."""
    current_course_w: int
    """Currently loaded course. For values see game_data.COURSES"""
    race_timer_pointer: int
    """Increased each frame during the race (inc. countdown of 185 frames)."""
    current_lap_wx: int
    """Table of players' current lap from 1st player to 4th. 0 = 1st lap."""
    in_race_placement_wx: int
    """Table of player placements from 1st player to 4th. 1 = 1st place. -1 for unused player slots."""
    starting_positions_wx: int
    """Table of player placements in last race. 0 = 1st place. Used for starting positions in the next race. Length 8."""
    total_ranking_w: int
    """Player's placement in the current cup. 0 = 1st place."""
    total_points_wx: int
    """Players' and cpus' points in a table."""
    game_ticks_w: int
    """Frames since game startup. 60 per second."""
    pause_state_w: int
    """1 if game is paused. Can be 0 or 2 otherwise."""
    kart_control_pointer: int
    """Pointer to kart manager."""
    kart_stats_pointer: int
    """Pointer to kart stat table."""
    gp_race_no_w: int
    """Current race # inside a cup. 0 = first race, 16 = all cup tour awards."""
    class_speed_multipliers_fx: int
    """Speed multipliers when playing on 50cc, 100cc or 150cc/Mirror. Defaults are 0.9, 1.0 and 1.15 respectively."""
    max_speed_f: int
    """Max kart speed which cannot be exceeded even with mushrooms. Default 200."""
    all_cup_tour_contents_wx: int
    """All cup tour course ids - uses ids 0 (Luigi Circuit) - 16 (Rainbow Road). Length 16, first value is unused."""
    cup_contents_wx: int
    """Table of cup course ids, name and preview images in cup order (ie. from Luigi Circuit to Rainbow Road).
    Example: Mushroom cup course 3: course id = 2*12, name = 2*12+4, preview = 2*12+8."""
    course_names_s: list[int]
    """List of course name image files for the menu."""
    course_previews_s: list[int]
    """List of course preview image files for the menu."""

    # Vanilla offsets:
    menu_character_w_offset: int
    """Offset from menu_pointer, cursor position."""
    menu_kart_w_offset: int
    """Offset from menu_pointer, selected kart."""
    menu_driver_w_offset: int
    """Offset from menu_pointer, confirmed driver."""
    menu_rider_w_offset: int
    """Offset from menu_pointer, confirmed rider."""
    menu_player_struct_size: int
    """Size of player menu struct. Add this to menu offsets to get different players' selections."""
    kart_control_kart_pointers_offset: int
    """Pointers for karts are found here from kart_control (size 8)."""
    kart_position_fx_offset: int
    """Kart's position is here from kart pointer (x, y, z)."""
    kart_velocity_fx_offset: int
    """Kart's velocity is here from kart pointer (x, y, z)."""
    kart_struct_size: int
    """Use this in combination with kart_stats_pointer and stat offsets to modify karts."""
    kart_speed_on_road_f_offset: int
    kart_speed_off_road_sand_f_offset: int
    kart_speed_off_road_grass_f_offset: int
    kart_speed_off_road_mud_f_offset: int
    kart_acceleration_1_f_offset: int
    kart_acceleration_2_f_offset: int
    kart_mini_turbo_f_offset: int
    kart_mass_f_offset: int
    kart_roll_f_offset: int
    kart_steer_f_offset: int

    # Custom addresses:
    menu_pointer: int
    """Pointer to menu object. Use with character/kart offsets."""
    available_characters_bx: int
    """Table of available characters from Mario to King Boo (size 20). 1 = unlocked."""
    available_karts_bx: int
    """Table of available karts from Goo-Goo Buggy to Parade Kart (size 21). 1 = unlocked."""
    lap_count_bx: int
    """Lap count for each course. Offsets from course ids."""
    max_vehicle_class_w: int
    """0 = 50cc, 3 = Mirror"""
    available_cups_bx: int
    """Table of available cups (size 5). 1 = unlocked."""
    tt_items_bx: int
    """Items for driver and rider in time trials (size 2)."""
    gp_next_items_bx: int
    """Item for player in grand prix. Offset by character's special item id (size 22)."""
    item_box_p: int
    """Pointer for last gotten item box data."""
    shuffle_queue_w: int
    """Counter for how many items should be given to player."""
    spawn_item_id_w: int
    """Item id for item to spawn. 20 == None."""
    spawn_item_pos_fx: int
    """Position for item to spawn."""
    spawn_item_vel_fx: int
    """Velocity for item to spawn."""
    text_sx: int
    """Text to print."""
    text_size: int
    """Max length of the text."""
    text_x_offset_h: int
    """Offset from text, x coordinate for the text."""
    text_y_offset_h: int
    """Offset from text, y coordinate for the text."""
    text_amount: int
    """Size of the text table."""
    menu_pointer_to_char_icons: dict[int, list[int]]
    """Pointers of the menu character icons"""
    item_box_data_x: dict[str, list[list[int]]]
    """The pointers of reference of some boxes"""

class MkddMemAddressesUsa(MkddMemAddresses):
    # Vanilla addresses:
    mode_w = 0x803b1464
    cup_w = 0x803cb7a8
    menu_course_w = 0x803cb7ac
    human_players_b = 0x803b147b
    vehicle_class_w = 0x803b146c
    current_course_w = 0x803cbd44
    race_timer_pointer = 0x803cbe5c
    current_lap_wx = 0x8037ff60
    in_race_placement_wx = 0x8037ffa0
    starting_positions_wx = 0x803b0f38
    total_ranking_w = 0x803b1260
    total_points_wx = 0x803b11cc
    game_ticks_w = 0x803b0754 # Currently unused.
    pause_state_w = 0x803b0720
    kart_control_pointer = 0x803CC588
    kart_stats_pointer = 0x80bd5000
    gp_race_no_w = 0x803b0fc8
    class_speed_multipliers_fx = 0x80361d44
    max_speed_f = 0x803d1894
    all_cup_tour_contents_wx = 0x803b1300
    cup_contents_wx = 0x803322e8
    course_names_s = [
        0x80331fd0, # Luigi Circuit
        0x80332004, # Peach Beach
        0x80332030, # Baby Park
        0x8033205c, # Dry Dry Desert
        0x80332094, # Mushroom Bridge
        0x803320c8, # Mario Circuit
        0x803320fc, # Daisy Cruiser
        0x80332128, # Waluigi Stadium
        0x8033215c, # Sherbet Land
        0x8033218c, # Mushroom City
        0x803321b8, # Yoshi Circuit
        0x803321ec, # DK Mountain
        0x80332218, # Wario Colosseum
        0x8033224c, # Dino Dino Jungle
        0x80332284, # Bowser's Castle
        0x803322b8, # Rainbow Road
    ]
    course_previews_s = [
        0x80331fec, # Luigi Circuit
        0x8033201c, # Peach Beach
        0x80332048, # Baby Park
        0x80332078, # Dry Dry Desert
        0x803320b0, # Mushroom Bridge
        0x803320e4, # Mario Circuit
        0x80332114, # Daisy Cruiser
        0x80332144, # Waluigi Stadium
        0x80332174, # Sherbet Land
        0x803321a4, # Mushroom City
        0x803321d4, # Yoshi Circuit
        0x80332204, # DK Mountain
        0x80332234, # Wario Colosseum
        0x80332268, # Dino Dino Jungle
        0x803322a0, # Bowser's Castle
        0x803322d0, # Rainbow Road
    ]

    # Vanilla offsets:
    menu_character_w_offset = 0x212c
    menu_kart_w_offset = 0x2140
    menu_driver_w_offset = 0x2138
    menu_rider_w_offset = 0x213c
    menu_player_struct_size = 28

    kart_control_kart_pointers_offset = 0xA0
    kart_position_fx_offset = 0x23c
    kart_velocity_fx_offset = 0x26c

    kart_struct_size = 0x100
    kart_speed_on_road_f_offset = 0x50
    kart_speed_off_road_sand_f_offset = 0x54
    kart_speed_off_road_grass_f_offset = 0x58
    kart_speed_off_road_mud_f_offset = 0x5c
    kart_acceleration_1_f_offset = 0x64
    kart_acceleration_2_f_offset = 0x74
    kart_mini_turbo_f_offset = 0x80
    kart_mass_f_offset = 0x84
    kart_roll_f_offset = 0xa0
    kart_steer_f_offset = 0xb4

    # Custom addresses:
    available_characters_bx = 0x80001000
    available_karts_bx = 0x80001014
    menu_pointer = 0x80001030
    max_vehicle_class_w = 0x80001038
    available_cups_bx = 0x8000103c
    tt_items_bx = 0x80001041
    gp_next_items_bx = 0x80001043
    item_box_p = 0x80001060
    shuffle_queue_w = 0x80001064
    spawn_item_id_w = 0x8000106c
    spawn_item_pos_fx = spawn_item_id_w + 4
    spawn_item_vel_fx = spawn_item_id_w + 16

    text_sx = 0x80000da4
    text_size = 0x30
    text_x_offset_h = -4
    text_y_offset_h = -2
    text_amount = 5
    
    lap_count_bx = 0x80005460 - 0x21 # First course has id of 0x21

    menu_pointer_to_char_icons = {
        0x812BFACC: [
            0x813FE760,  # Mario
            0x813FDDE0,  # Luigi
            0x81401DDC,  # Peach
            0x8140145C,  # Daisy
            0x81405458,  # Yoshi
            0x81404AD8,  # Birdo
            0x81408AD4,  # Baby Mario
            0x81408154,  # Baby Luigi
            0x8140C150,  # Toad
            0x8140B7D0,  # Toadette
            0x8140F7CC,  # Koopa
            0x8140EE4C,  # Red Koopa
            0x81412E48,  # Donkey Kong
            0x814124C8,  # Diddy Kong
            0x814164C4,  # Bowser
            0x81415B44,  # Bowser Jr.
            0x81419B40,  # Wario
            0x814191C0,  # Waluigi
            0x8141D1BC,  # Petey Piranha
            0x8141C83C  # King Boo
        ],
        0x811D9BCC: [
            0x81318880,  # Mario
            0x81317F00,  # Luigi
            0x8131BEFC,  # Peach
            0x8131B57C,  # Daisy
            0x8131F578,  # Yoshi
            0x8131EBF8,  # Birdo
            0x81322BF4,  # Baby Mario
            0x81322274,  # Baby Luigi
            0x81326270,  # Toad
            0x813258F0,  # Toadette
            0x813298EC,  # Koopa
            0x81328F6C,  # Red Koopa
            0x8132CF68,  # Donkey Kong
            0x8132C5E8,  # Diddy Kong
            0x813305E4,  # Bowser
            0x8132FC64,  # Bowser Jr.
            0x81333C60,  # Wario
            0x813332E0,  # Waluigi
            0x813372DC,  # Petey Piranha
            0x8133695C  # King Boo
        ],
        0x8132380C: [
            0x8145D6D8,  # Mario
            0x8145CD58,  # Luigi
            0x81460D54,  # Peach
            0x814603D4,  # Daisy
            0x814643D0,  # Yoshi
            0x81463A50,  # Birdo
            0x81467A4C,  # Baby Mario
            0x814670CC,  # Baby Luigi
            0x8146B0C8,  # Toad
            0x8146A748,  # Toadette
            0x8146E744,  # Koopa
            0x8146DDC4,  # Red Koopa
            0x81471DC0,  # Donkey Kong
            0x81471440,  # Diddy Kong
            0x8147543C,  # Bowser
            0x81474ABC,  # Bowser Jr.
            0x81478AB8,  # Wario
            0x81478138,  # Waluigi
            0x8147C134,  # Petey Piranha
            0x8147B7B4  # King Boo
        ],
        0x812BFAEC: [
            0x813FE780,  # Mario
            0x813FDE00,  # Luigi
            0x81401DFC,  # Peach
            0x8140147C,  # Daisy
            0x81405478,  # Yoshi
            0x81404AF8,  # Birdo
            0x81408AF4,  # Baby Mario
            0x81408174,  # Baby Luigi
            0x8140C170,  # Toad
            0x8140B7F0,  # Toadette
            0x8140F7EC,  # Koopa
            0x8140EE6C,  # Red Koopa
            0x81412E68,  # Donkey Kong
            0x814124E8,  # Diddy Kong
            0x814164E4,  # Bowser
            0x81415B64,  # Bowser Jr.
            0x81419B60,  # Wario
            0x814191E0,  # Waluigi
            0x8141D1DC,  # Petey Piranha
            0x8141C85C  # King Boo
        ]
    }

    item_box_data_x = {
        "Luigi Circuit 50cc": [
            [0x80d6e300, 0x80d6e380, 0x80d6e540, 0x80d6e4c0, 0x80d6e240, 0x80d6e480, 0x80d6e600],   # First U-turn
            [0x80d6e880, 0x80d6e8c0, 0x80d6ea40, 0x80d6ea00, 0x80d6ea80],                           # Last Turn
            [0x80d6e980, 0x80d6eb40, 0x80d6e940, 0x80d6e900],                                       # 50cc First Straight
            [0x80d6e9c0, 0x80d6eac0, 0x80d6eb00, 0x80d6eb80],                                       # 50cc Second Straight
            [],
            [],
            [],
        ],
        "Luigi Circuit 100cc": [
            [0x80d67f68, 0x80d68028, 0x80d686e8, 0x80d685e8, 0x80d67ea8, 0x80d685a8, 0x80d687a8],   # First U-turn
            [0x80d67e68, 0x80d68528, 0x80d67fe8, 0x80d68568, 0x80d68828],                           # Last Turn
            [],
            [],
            [0x80d68228, 0x80d681e8, 0x80d681a8, 0x80d68168],                                       # 100cc Center
            [0x80D683E8, 0x80D684E8],                                                               # 100cc Chomp Shortcut
            [0x80D68668, 0x80D686A8],                                                               # 100cc Last Turn Shortcut
        ],
        "Peach Beach": [
            [0x80D8B390],                                                                           # Hidden pipe
            [0x80d8a3d0, 0x80d8a410, 0x80d8a390, 0x80d8a450, 0x80d8a350],                           # First Turn
            [0x80D8A2D0, 0x80D8A850],                                                               # Beach jump boxes
            [0x80d8a610, 0x80d8b610, 0x80d8a650, 0x80d8a5d0, 0x80d8b5d0, 0x80d8a690],               # Under Arc
            [0x80d8a290, 0x80d8a250, 0x80d8a210, 0x80d8a190, 0x80d8a1d0, 0x80d8a310],               # Ramp
            [0x80D8A790, 0x80D8A750],                                                               # Fountain
        ],
        "Baby Park": [
            [0x80e3b160, 0x80e3b260, 0x80e3b220, 0x80e3b120, 0x80e3b0e0, 0x80e3b0a0, 0x80e3b1e0],   # First Turn
            [0x80e3b3a0, 0x80e3b2a0, 0x80e3b2e0, 0x80e3b320, 0x80e3b3e0, 0x80e3b420, 0x80e3b360],   # Second Turn
        ],
        "Dry Dry Desert": [
            [0x80da52c4, 0x80da5284, 0x80da5304, 0x80da5344],                                       # Start
            [0x80da5d44, 0x80da5e04, 0x80da5d04, 0x80da5d84, 0x80da5dc4],                           # First Turn
            [0x80da5444, 0x80da5404, 0x80da53c4, 0x80da5384],                                       # Before Sand Pit
            [0x80da5484, 0x80da5504, 0x80da5a84, 0x80da5604],                                       # After Sand Pit
            [0x80da54c4],                                                                           # Between Pokeys
            [0x80da5584, 0x80da5ac4, 0x80da5644, 0x80da5684, 0x80da5544],                           # Sand Hills
            [0x80da5b04, 0x80da55c4, 0x80da5b44, 0x80da5b84],                                       # Last Pokeys
        ],
        "Mushroom Bridge": [
            [0x80d85ef8, 0x80d860f8],                                                               # Left Lane
            [0x80d85eb8, 0x80d85db8],                                                               # Right Lane
            [0x80D86338],                                                                           # Pipe
            [0x80d85e38, 0x80d85df8, 0x80d85e78],                                                   # First Tunnel
            [0x80D863B8],                                                                           # Sidewalk
            [0x80d85af8, 0x80d859b8, 0x80d85ab8],                                                   # Second Tunnel
            [0x80d85a78, 0x80d85a38, 0x80d859f8],                                                   # Bridge
            [0x80D85F38, 0x80D85F78],                                                               # Bridge Top
        ],
        "Mario Circuit": [
            [0x80d85cac, 0x80d85eac, 0x80d85c2c, 0x80d85bec, 0x80d862ac],                           # Start
            [0x80d85c6c, 0x80d85cec, 0x80d85eec, 0x80d85d2c],                                       # Before Tunnel
            [0x80d85d6c, 0x80d85e6c, 0x80d85e2c, 0x80d85dec, 0x80d8626c, 0x80d85dac],               # Near Goombas
        ],
        "Daisy Cruiser": [
            [0x80d4e6a4, 0x80d4e6e4, 0x80d4e724, 0x80d4e424, 0x80d4e3e4],                           # First
            [0x80d4e3a4, 0x80d4e764, 0x80d4e2a4, 0x80d4e624, 0x80d4e7e4, 0x80d4e7a4, 0x80d4e664, 0x80d4e324], # Dining Hall
            [0x80d4f124, 0x80d4f164],                                                               # Cargo Hatch
            [0x80D4F064],                                                                           # Cargo Area
            [0x80d4e564, 0x80d4e524, 0x80d4e4e4, 0x80d4e4a4, 0x80d4e824],                           # Deck
        ],
        "Waluigi Stadium": [
            [0x80d76130, 0x80d760f0, 0x80d760b0, 0x80d76170],                                       # Start
            [0x80d76070],                                                                           # First Jump
            [0x80d765b0],                                                                           # Second Jump
            [0x80d76570, 0x80d76530, 0x80d75ff0, 0x80d76030],                                       # Near Big Puddle
            [0x80d75fb0, 0x80d76270, 0x80d762b0, 0x80d764f0],                                       # First Piranha
            [0x80d764b0, 0x80d76370, 0x80d76330, 0x80d762f0],                                       # Second Piranha
            [0x80d769b0, 0x80d768f0, 0x80d76970, 0x80d76930],                                       # After Piranhas
            [0x80d768b0],                                                                           # Last Jump
        ],
        "Sherbet Land": [
            [0x80d50980, 0x80d509c0, 0x80d50a00, 0x80d50a40],                                       # Start
            [0x80d51040, 0x80d51080, 0x80d51000],                                                   # Tunnel Beginning
            [0x80d50c40, 0x80d50c00, 0x80d50bc0],                                                   # Tunnel End
            [0x80d510c0, 0x80d51100, 0x80d51140],                                                   # After Tunnel
            [0x80d50c80, 0x80d50cc0, 0x80d50d00, 0x80d50d40, 0x80d50fc0],                           # Before Ice
            [0x80d50d80, 0x80d50dc0, 0x80d50e40, 0x80d50e00],                                       # On Ice
        ],
        "Mushroom City": [
            [0x80d667a8, 0x80d66a28],                                                               # Outer Route
            [0x80d66ba8],                                                                           # First Block
            [0x80d664a8, 0x80d66928],                                                               # Last Straight Left Lane
            [0x80d663a8, 0x80d66428, 0x80d66a68],                                                   # Last Straight Right Lane
            [0x80d66c68, 0x80d66c28, 0x80d66be8, 0x80d66ca8],                                       # Start
            [0x80d66b68],                                                                           # Alley
            [0x80d66ce8],                                                                           # Crossroad
            [0x80d66268, 0x80d662a8, 0x80d66228, 0x80d662e8],                                       # After City
            [0x80d66d68, 0x80d66d28, 0x80d66da8],                                                   # Ramp
        ],
        "Yoshi Circuit": [
            [0x80d7d034, 0x80d7d0b4, 0x80d7d0f4, 0x80d7d074],                                       # First Turn
            [0x80d7d474, 0x80d7d3b4, 0x80d7d3f4, 0x80d7d434],                                       # Before Tunnel
            [0x80d7cfb4, 0x80d7cf74, 0x80d7cf34, 0x80d7cff4],                                       # After Tunnel
            [0x80d7d1f4, 0x80d7d134, 0x80d7d174, 0x80d7d1b4],                                       # Before U-turn
            [0x80d7d934, 0x80d7d8f4],                                                               # Tunnel Shortcut
            [0x80d7d374, 0x80d7d2b4, 0x80d7d4b4, 0x80d7d2f4, 0x80d7d334],                           # Last Straight
        ],
        "DK Mountain": [
            [0x80d7ca4c, 0x80d7c9cc, 0x80d7ca0c, 0x80d7ce4c],                                       # Start
            [0x80d7ca8c, 0x80d7cb0c, 0x80d7cacc, 0x80d7cb4c],                                       # Mountain Top
            [0x80d7cc0c, 0x80d7cbcc, 0x80d7cb8c, 0x80d7d10c],                                       # Cliff U-turn
            [0x80d7cfcc, 0x80d7cd4c, 0x80d7cd0c, 0x80d7cccc, 0x80d7cc8c],                           # Last Turn
        ],
        "Wario Colosseum": [
            [0x80d99f64],                                                                           # First Jump
            [0x80d99fa4],                                                                           # Second Jump
            [0x80d9a164, 0x80d9a0e4, 0x80d9a124, 0x80d9a1a4, 0x80d9a524],                           # Before Big Jump
            [0x80d99ca4, 0x80d99c64, 0x80d99ce4, 0x80d99c24],                                       # After Spiral
            [0x80d9a3e4, 0x80d9a4a4, 0x80d9a464, 0x80d9a4e4, 0x80d9a424],                           # Wide Curve
            [0x80d99de4, 0x80d99d24, 0x80d99da4, 0x80d99d64],                                       # Before Pit
            [0x80d9a364, 0x80d9a3a4],                                                               # Pit Left
            [0x80D9A1E4],                                                                           # Pit Jump
            [0x80d9a324, 0x80d9a2e4],                                                               # Pit Right
            [0x80d99ee4, 0x80d99e24, 0x80d99ea4, 0x80d9a624, 0x80d9a5e4, 0x80d99e64],               # After Pit
            [0x80d9a264, 0x80d99f24, 0x80d9a2a4, 0x80d9a224],                                       # Last Jump
        ],
        "Dino Dino Jungle": [
            [0x80d6e738, 0x80d6e6f8, 0x80d6e778, 0x80d6ecb8],                                       # First Turn
            [0x80d6e8b8, 0x80d6e7b8],                                                               # Over Logs
            [0x80d6eef8, 0x80d6e9f8, 0x80d6ea38, 0x80d6ef38],                                       # Under Dino
            [0x80D6E878, 0x80D6E7f8],                                                               # Bridge
            [0x80d6efb8, 0x80d6ecf8, 0x80d6ef78],                                                   # Cave
            [0x80d6e838],                                                                           # Cave Shortcut
            [0x80d6e978, 0x80d6e938, 0x80d6e8f8, 0x80d6e9b8],                                       # After Cave
            [0x80d6eaf8, 0x80d6eab8, 0x80d6eb78, 0x80d6eb38],                                       # Last Straight
        ],
        "Bowser's Castle": [
            [0x80d5e700, 0x80d5e780, 0x80d5eac0, 0x80d5e580],                                       # Entrance
            [0x80d5eb80, 0x80d5ebc0],                                                               # Lava Room Left
            [0x80d5eb00, 0x80d5eb40],                                                               # Lava Room Right
            [0x80d5e800, 0x80d5e840, 0x80d5e740, 0x80d5e7c0],                                       # Spinning Fire
            [0x80d5ef80, 0x80d5e600, 0x80d5e5c0, 0x80d5efc0],                                       # Balcon
            [0x80d5e6c0, 0x80d5e640, 0x80d5e680],                                                   # Cannon Room First
            [0x80d5ec40, 0x80d5ec00, 0x80d5ec80],                                                   # Cannon Room Second
        ],
        "Rainbow Road": [
            [0x80db1548, 0x80db1508, 0x80db14c8, 0x80db1488],                                       # Downhill
            [0x80db1648, 0x80db1608, 0x80db1a88, 0x80db15c8, 0x80db1588],                           # U-turn
            [0x80db1748, 0x80db1708, 0x80db16c8, 0x80db1688],                                       # Spiral
            [0x80db1848, 0x80db1808, 0x80db17c8, 0x80db1788],                                       # After Spiral
            [0x80db1888, 0x80db18c8, 0x80db1ac8, 0x80db1908, 0x80db1948],                           # Big Pipe
            [0x80db1988, 0x80db19c8, 0x80db1a08, 0x80db1a48],                                       # Last Jump
        ],
    }
