from ..DSZeldaClient.subclasses import Address, Pointer

addr_null = Address(0)

class STAddr:
    
    null = addr_null
    
    # Fundamentals
    game_identifier = Address(0, 0, 16, "ROM")
    
    game_state = Address(0x060C48)
    loading_room = Address(0x0c2FF0)
    mid_load = Address(0x265190)
    
    received_item_index = Address(0x265780, size=2)
    slot_id = Address(0x265782, size=2)
    
    stage = Address(0x2690E0)
    floor = Address(0x1B2E98)
    room = Address(0x2690EA)
    entrance = Address(0x2690EB)

    respawn_stage = Address(0x262074)
    respawn_room = Address(0x26207e)
    respawn_entrance = Address(0x26207f)

    getting_location = Address(0x04B114)
    saving = Address(0x049BD8)
    getting_tear_safety = Address(0x327B8C)
    getting_item_safety = Address(0x264648)
    entering_shop = Address(0x260A44)

    # drinking_potion = Address(0x317ED0)  # 39 normal, 3b drinking
    drinking_potion_pointer = Address(0x265338, size=4)
    
    link_x = Address.pointer(0x05CC)  # Not actually pointers, but the object does all the settings right
    link_y = Address.pointer(0x05D0)
    link_z = Address.pointer(0x05D4)
    
    menu = Address(0x260958)
    equipped_item = Address(0x265318, size=4)
    
    health = Address(0x2651BC)
    heart_count = Address(0x2651BD)
    rabbits = Address(0x262030, size=7)
    rabbits_0 = Address(0x262030)
    rabbits_1 = Address(0x262031)
    rabbits_2 = Address(0x262032)
    rabbits_3 = Address(0x262033)
    rabbits_4 = Address(0x262034)
    rabbits_5 = Address(0x262035)
    rabbits_6 = Address(0x262036)
    
    gItemManager = Address.pointer(0x0fb4)
    gPlayerManager = Address.pointer(0x0fbc)
    gAdventureFlags = Address.pointer(0x0f74)
    gPlayer = Address.pointer(0x0fec)
    gMapManager = Address.pointer(0x0e60)
    stage_flag_pointer = Address(0x265164, size=4)
    
    watched_intro = Address(0x265726)

    train_speed_fast = Address(0x136004, size=4)  # 0xc1 193
    train_speed_med = Address(0x135FFC, size=4)   # 0x73 115
    train_speed_stop = Address(0x135FF4, size=4)  # 0
    train_speed_reverse = Address(0x135FEC, size=4) # -143
    train_speed_pointer = Address(0x13F578, size=4)  # + 0x94 to get actual train speed

    train_action = Address(0x2CA23C) # forest, but near train speed pointer
    train_gear = Address(0x2CA438)  # forest, find pointer
    train_health = Address(0x2653a0)

    train_trans_x = Address(0x262090, size=4)
    train_trans_y = Address(0x262094, size=4)
    train_trans_z = Address(0x262098, size=4)

    train_x = Address(0x264628, size=4)
    train_y = Address(0x26462C, size=4)
    train_z = Address(0x264630, size=4)
    train_coords = (train_x, train_y,train_z)

    # Inventory
    items_0 = Address(0x265320)
    items_2 = Address(0x265322)
    songs = Address(0x268FB0)
    arrow_capacity = Address(0x265330)
    bomb_capacity = Address(0x265331)
    arrow_count = Address(0x265332)
    bomb_count = Address(0x265333)
    postcard_count = Address(0x268FA2)

    item_restrictions = Address(0x26532C, size=2)
    
    rupees = Address(0x265328, size=2)
    tears_of_light = Address(0x26532E)
    small_keys = Address(0x26532F)
    
    potion_0 = Address(0x265334)
    potion_1 = Address(0x265335)
    all_potions = Address(0x265334, size=2)
    
    rail_restorations = Address(0x2653B0)
    tracks_0 = Address(0x2653B4)
    tracks_1 = Address(0x2653B5)
    tracks_2 = Address(0x2653B6)
    source_rails = Address(0x2653B8)
    key_storage_0 = Address(0x265784)
    key_storage_tos = Address(0x265785)
    key_storage_2 = set_starting_train = Address(0x265786)

    train_parts = Address(0x2653A8, size=4)
    equipped_engine = Address(0x265388, size=4)
    equipped_cannon = Address(0x26538C, size=4)
    equipped_car = Address(0x265390, size=4)
    equipped_cart = Address(0x265394, size=4)

    # Passenger data
    has_passenger_0 = Address(0x265598, size=4)
    has_passenger_1 = Address(0x2655AC, size=4)
    passenger_tag_0 = Address(0x265594, size=4)
    passenger_tag_1 = Address(0x2655A8, size=4)
    passenger_goal = Address(0x26559C, size=4)

    # Cargo Data
    cargo_0 = Address(0x2655d8, size=4)
    cargo_1 = Address(0x2655e4, size=4)
    cargo_count_0 = Address(0x2655dc)
    cargo_count_1 = Address(0x2655e8)

    # Boss key pointers
    boss_key_deletion_pointer = Address(0x265620, size=3)  # points to 3 references, and deleting then deletes the key.
    boss_key_deletion = Address(0x3251C0, size=12)
    wt_bk_pointer = Address(0x3251C0, size=3)
    bt_bk_pointer = Address(0x326C20, size=3)
    oct_bk_pointer = Address(0x32520C, size=3)
    mtt_bk_pointer = Address(0x32963C, size=3)
    dt_bk_pointer = Address(0x3251C8, size=3)
    tos3_bk_pointer = Address(0x332858, size=3)
    tos5_bk_pointer = Address(0x332818, size=3)
    tos_actor_table = Address(0x332810, size=3)
    tos_bk_pointer = Address(0x332818, size=3)

    tos_actor_table_pointer_0 = Address(0x3329C0, size=3)
    tos_actor_table_pointer_1 = Address(0x329C3C, size=3)
    tos_actor_table_pointer_safe = Address(0x25FA48, size=3)  # offset 1032 (header)/1040 (start of pointers)

    oct_actor_table_start = Address(0x3251D8, size=3)

    # Candidates for ToS 3 bk pointers
    # 332858
    # 332A20
    # 332BB4
    # 332BD4
    # 332D1C
    # 33DBFC

    # Boss door openers
    wt_boss_door = Address(0x3368FE)
    bt_boss_door = Address(0x33099E)
    oct_boss_door = Address(0x32F6EE)
    mtt_boss_door = Address(0x33497E)
    dt_boss_door = Address(0x332C5E)
    tos3_boss_door = Address(0x33E482)
    # tos5_boss_door = Address(0x33E182)
    tos5_boss_door = Address(0x33E1Ce)

    mtt_b1_heatoise_trigger_pointer = Address(0x1231B4, size=3)

    # Object pointer table
    tos_boss_door_pointer = Address(0x265668, size=4)

    snurglin_keys = Address(0x2e986c)
    snurglar_pointer = Address(0x0499F4, size=4)
    mountain_gate = Address(0x2e3640)

    # Stamps
    stamp_ids = Address(0x268f8c, size=20)
    stamp_coords = Address(0x268F50, size=40)

    # Adventure Flags
    adv_flags_0 = sources = Address(0x265714)
    adv_flags_1 = restorations = Address(0x265715)
    adv_flags_2 = glyphs = Address(0x265716)
    adv_flags_3 = Address(0x265717)
    adv_flags_4 = Address(0x265718)
    adv_flags_5 = Address(0x265719)
    adv_flags_6 = Address(0x26571a)
    adv_flags_7 = Address(0x26571b)
    adv_flags_8 = Address(0x26571c)
    adv_flags_9 = Address(0x26571d)
    adv_flags_a = Address(0x26571e)
    adv_flags_b = Address(0x26571f)
    adv_flags_c = Address(0x265720)
    adv_flags_d = Address(0x265721)
    adv_flags_e = Address(0x265722)
    adv_flags_f = Address(0x265723)
    adv_flags_10 = Address(0x265724)
    adv_flags_11 = Address(0x265725)
    adv_flags_12 = Address(0x265726)
    adv_flags_13 = Address(0x265727)
    adv_flags_14 = Address(0x265728)
    adv_flags_15 = Address(0x265729)
    adv_flags_16 = Address(0x26572a)
    adv_flags_17 = Address(0x26572b)
    adv_flags_18 = Address(0x26572c)
    adv_flags_19 = Address(0x26572d)
    adv_flags_1a = Address(0x26572e)
    adv_flags_1b = Address(0x26572f)
    adv_flags_1c = Address(0x265730)
    adv_flags_1d = Address(0x265731)
    adv_flags_1e = Address(0x265732)
    adv_flags_1f = Address(0x265733)
    adv_flags_20 = Address(0x265734)
    adv_flags_21 = Address(0x265735)
    adv_flags_22 = Address(0x265736)
    adv_flags_23 = Address(0x265737)
    adv_flags_24 = Address(0x265738)
    adv_flags_25 = Address(0x265739)
    adv_flags_26 = Address(0x26573a)
    adv_flags_27 = Address(0x26573b)
    adv_flags_28 = Address(0x26573c)
    adv_flags_29 = Address(0x26573d)
    adv_flags_2a = Address(0x26573e)
    adv_flags_2b = Address(0x26573f)
    adv_flags_2c = Address(0x265740)
    adv_flags_2d = Address(0x265741)
    adv_flags_2e = Address(0x265742)
    adv_flags_2f = Address(0x265743)
    adv_flags_30 = activate_portals = Address(0x265744)
    adv_flags_31 = Address(0x265745)
    adv_flags_32 = Address(0x265746)
    adv_flags_33 = Address(0x265747)
    adv_flags_34 = Address(0x265748)
    adv_flags_35 = Address(0x265749)
    adv_flags_36 = Address(0x26574a)
    adv_flags_37 = Address(0x26574b)
    adv_flags_38 = Address(0x26574c)
    adv_flags_39 = Address(0x26574d)
    adv_flags_3a = Address(0x26574e)
    adv_flags_3b = Address(0x26574f)
    adv_flags_3c = Address(0x265750)
    adv_flags_3d = Address(0x265751)
    adv_flags_3e = Address(0x265752)
    adv_flags_3f = Address(0x265753)
    adv_flags_40 = Address(0x265754)
    adv_flags_41 = Address(0x265755)
    adv_flags_42 = Address(0x265756)
    adv_flags_43 = Address(0x265757)
    adv_flags_44 = Address(0x265758)
    adv_flags_45 = Address(0x265759)
    adv_flags_46 = Address(0x26575a)
    adv_flags_47 = Address(0x26575b)
    adv_flags_48 = Address(0x26575c)
    adv_flags_49 = Address(0x26575d)
    adv_flags_4a = Address(0x26575e)
    adv_flags_4b = Address(0x26575f)
    adv_flags_4c = Address(0x265760)
    adv_flags_4d = Address(0x265761)
    adv_flags_4e = Address(0x265762)
    adv_flags_4f = Address(0x265763)
    adv_flags_50 = Address(0x265764)
    adv_flags_51 = Address(0x265765)
    adv_flags_52 = Address(0x265766)
    adv_flags_53 = Address(0x265767)
    adv_flags_54 = Address(0x265768)
    adv_flags_55 = Address(0x265769)
    adv_flags_56 = Address(0x26576a)
    adv_flags_57 = Address(0x26576b)
    adv_flags_58 = Address(0x26576c)
    adv_flags_59 = Address(0x26576d)
    adv_flags_5a = Address(0x26576e)
    adv_flags_5b = Address(0x26576f)
    
    # Treasure
    all_treasure_count = Address(0x269000, size=32)
    demon_fossil_count = Address(0x269000, size=2)
    stalfos_skull_count = Address(0x269002, size=2)
    star_fragment_count = Address(0x269004, size=2)
    bee_larvae_count = Address(0x269006, size=2)
    wood_heart_count = Address(0x269008, size=2)
    dark_pearl_loop_count = Address(0x26900a, size=2)
    white_pearl_loop_count = Address(0x26900c, size=2)
    ruto_crown_count = Address(0x26900e, size=2)
    dragon_scale_count = Address(0x269010, size=2)
    pirates_necklace_count = Address(0x269012, size=2)
    palace_dish_count = Address(0x269014, size=2)
    goron_amber_count = Address(0x269016, size=2)
    mystic_jade_count = Address(0x269018, size=2)
    ancient_coin_count = Address(0x26901a, size=2)
    priceless_stone_count = Address(0x26901c, size=2)
    regal_ring_count = Address(0x26901e, size=2)

    item_model_table = Address(0x0af590)  # size=big

#  = Address()
#  = Address()
#  = Address()
#  = Address()
#  = Address()
#  = Address()
#  = Address()
#  = Address()
#  = Address()
#  = Address()