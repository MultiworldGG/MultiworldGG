############################################# LOCATION NAMES #############################################
class LocationNames:
    # Prefixes
    _loc_event_ = "Event "
    loc_event_pfx = _loc_event_

    # Postfixes
    _num1_ = " One"
    _num2_ = " Two"
    _num3_ = " Three"
    _num4_ = " Four"
    _nums_ = (_num1_, _num2_, _num3_, _num4_)
    _isle_ = " Isle"
    _isle1_ = _isle_ + _num1_
    _isle2_ = _isle_ + _num2_
    _isle3_ = _isle_ + _num3_
    _isle4_ = _isle_ + _num4_
    _isles_ = (_isle1_, _isle2_, _isle3_, _isle4_)

    # Level Defs
    level_house = "The Elder Kettle"

    level_boss_veggies = "Botanic Panic"
    level_boss_slime = "Ruse of an Ooze"
    level_boss_frogs = "Clip Joint Calamity"
    level_boss_flower = "Floral Fury"
    level_boss_baroness = "Sugarland Shimmy"
    level_boss_clown = "Carnival Kerfuffle"
    level_boss_dragon = "Fiery Frolic"
    level_boss_bee = "Honeycomb Herald"
    level_boss_pirate = "Shootin n' Lootin"
    level_boss_mouse = "Murine Corps"
    level_boss_sallystageplay = "Dramatic Fanatic"
    level_boss_train = "Railroad Wrath"
    level_boss_kingdice = "All Bets Are Off"
    level_boss_devil = "One Hell of a Time"
    level_dlc_boss_oldman = "Gnome Way Out"
    level_dlc_boss_rumrunners = "Bootlegger Boogie"
    level_dlc_boss_snowcult = "Snow Cult Scuffle"
    level_dlc_boss_airplane = "Doggone Dogfight"
    level_dlc_boss_saltbaker = "A Dish to Die For"

    level_boss_plane_blimp = "Threatenin' Zepplin"
    level_boss_plane_genie = "Pyramid Peril"
    level_boss_plane_bird = "Aviary Action"
    level_boss_plane_mermaid = "High Sea Hi-Jinx"
    level_boss_plane_robot = "Junkyard Jive"
    level_dlc_boss_plane_cowboy = "High-Noon Hoopla"

    level_dicepalace = "Kingdice Minibosses"
    level_dicepalace_boss1 = "Kingdice Miniboss 1"
    level_dicepalace_boss2 = "Kingdice Miniboss 2"
    level_dicepalace_boss3 = "Kingdice Miniboss 3"
    level_dicepalace_boss4 = "Kingdice Miniboss 4"
    level_dicepalace_boss5 = "Kingdice Miniboss 5"
    level_dicepalace_boss6 = "Kingdice Miniboss 6"
    level_dicepalace_boss7 = "Kingdice Miniboss 7"
    level_dicepalace_boss8 = "Kingdice Miniboss 8"
    level_dicepalace_boss9 = "Kingdice Miniboss 9"
    level_dicepalace_boss_booze = level_dicepalace_boss1
    level_dicepalace_boss_chips = level_dicepalace_boss2
    level_dicepalace_boss_cigar = level_dicepalace_boss3
    level_dicepalace_boss_domino = level_dicepalace_boss4
    level_dicepalace_boss_rabbit = level_dicepalace_boss5
    level_dicepalace_boss_plane_horse = level_dicepalace_boss6
    level_dicepalace_boss_roulette = level_dicepalace_boss7
    level_dicepalace_boss_eightball = level_dicepalace_boss8
    level_dicepalace_boss_plane_memory = level_dicepalace_boss9

    level_rungun_forest = "Forest Follies"
    level_rungun_tree = "Treetop Trouble"
    level_rungun_circus = "Funfair Fever"
    level_rungun_funhouse = "Funhouse Frazzle"
    level_rungun_harbour = "Perilous Piers"
    level_rungun_mountain = "Rugged Ridge"

    level_mausoleum_i = "Mausoleum I"
    level_mausoleum_ii = "Mausoleum II"
    level_mausoleum_iii = "Mausoleum III"

    level_diehouse1 = "Diehouse 1"
    level_diehouse2 = "Diehouse 2"

    level_dlc_graveyard = "Graveyard Dream"

    level_dlc_chesscastle = "The King's Leap"
    level_dlc_chesscastle_pawn = "The Pawns"
    level_dlc_chesscastle_knight = "The Knight"
    level_dlc_chesscastle_bishop = "The Bishop"
    level_dlc_chesscastle_rook = "The Rook"
    level_dlc_chesscastle_queen = "The Queen"
    level_dlc_chesscastle_run = level_dlc_chesscastle + " Gauntlet"

    level_shop = "Porkrind's Emporium"
    #level_shop1 = level_shop + _isle1_
    #level_shop2 = level_shop + _isle2_
    #level_shop3 = level_shop + _isle3_
    #level_base_shops = (level_shop1, level_shop2, level_shop3)
    #level_dlc_shop4 = level_shop + _isle4_
    #level_dlc_shop = level_dlc_shop4
    #level_dlc_shops = (level_dlc_shop4,)
    #level_shops = level_base_shops + level_dlc_shops

    level_tutorial = "Tutorial"
    level_plane_tutorial = "Plane Tutorial"
    level_dlc_tutorial = "Recipe for Ms. Chalice"

    # Misc Region
    reg_dlc_boat = "Boat"

    # World Defs
    world_inkwell = "Inkwell Isle"
    world_inkwell_1 = world_inkwell + _num1_
    world_inkwell_2 = world_inkwell + _num2_
    world_inkwell_3 = world_inkwell + _num3_
    world_inkwell_hell = "Inkwell Hell"
    world_dlc_inkwell_4 = world_inkwell + _num4_

    # Shop Set Defs
    shop_set = "Shop Set"
    shop_set1 = shop_set + " 1"
    shop_set2 = shop_set + " 2"
    shop_set3 = shop_set + " 3"
    base_shop_sets = (shop_set1, shop_set2, shop_set3)
    shop_set4 = shop_set + " 4"
    dlc_shop_set = shop_set4
    dlc_shop_sets = (shop_set4,)
    shop_sets = base_shop_sets + dlc_shop_sets

    # Location Defs
    loc_level_tutorial = level_tutorial + " Complete"
    loc_level_tutorial_coin = level_tutorial + " Coin"
    loc_level_plane_tutorial = level_plane_tutorial + " Complete"
    loc_level_dlc_tutorial = level_dlc_tutorial + " Complete"
    loc_level_dlc_tutorial_coin = level_dlc_tutorial + " Coin"

    loc_level_boss_veggies = level_boss_veggies + " Complete"
    loc_level_boss_veggies_secret = level_boss_veggies + " Secret Complete"
    loc_level_boss_veggies_topgrade = level_boss_veggies + " Top Grade"
    loc_level_boss_veggies_dlc_chaliced = level_boss_veggies + " Chalice Complete"
    loc_level_boss_veggies_event_defeat = _loc_event_ + level_boss_veggies + " Defeated"
    loc_level_boss_veggies_event_agrade = _loc_event_ + loc_level_boss_veggies_topgrade
    loc_level_boss_veggies_event_dlc_chaliced = _loc_event_ + loc_level_boss_veggies_dlc_chaliced
    loc_level_boss_slime = level_boss_slime + " Complete"
    loc_level_boss_slime_topgrade = level_boss_slime + " Top Grade"
    loc_level_boss_slime_dlc_chaliced = level_boss_slime + " Chalice Complete"
    loc_level_boss_slime_event_defeat = _loc_event_ + level_boss_slime + " Defeated"
    loc_level_boss_slime_event_agrade = _loc_event_ + loc_level_boss_slime_topgrade
    loc_level_boss_slime_event_dlc_chaliced = _loc_event_ + loc_level_boss_slime_dlc_chaliced
    loc_level_boss_frogs = level_boss_frogs + " Complete"
    loc_level_boss_frogs_topgrade = level_boss_frogs + " Top Grade"
    loc_level_boss_frogs_dlc_chaliced = level_boss_frogs + " Chalice Complete"
    loc_level_boss_frogs_event_defeat = _loc_event_ + level_boss_frogs + " Defeated"
    loc_level_boss_frogs_event_agrade = _loc_event_ + loc_level_boss_frogs_topgrade
    loc_level_boss_frogs_event_dlc_chaliced = _loc_event_ + loc_level_boss_frogs_dlc_chaliced
    loc_level_boss_flower = level_boss_flower + " Complete"
    loc_level_boss_flower_topgrade = level_boss_flower + " Top Grade"
    loc_level_boss_flower_dlc_chaliced = level_boss_flower + " Chalice Complete"
    loc_level_boss_flower_event_defeat = _loc_event_ + level_boss_flower + " Defeated"
    loc_level_boss_flower_event_agrade = _loc_event_ + loc_level_boss_flower_topgrade
    loc_level_boss_flower_event_dlc_chaliced = _loc_event_ + loc_level_boss_flower_dlc_chaliced
    loc_level_boss_baroness = level_boss_baroness + " Complete"
    loc_level_boss_baroness_topgrade = level_boss_baroness + " Top Grade"
    loc_level_boss_baroness_dlc_chaliced = level_boss_baroness + " Chalice Complete"
    loc_level_boss_baroness_event_defeat = _loc_event_ + level_boss_baroness + " Defeated"
    loc_level_boss_baroness_event_agrade = _loc_event_ + loc_level_boss_baroness_topgrade
    loc_level_boss_baroness_event_dlc_chaliced = _loc_event_ + loc_level_boss_baroness_dlc_chaliced
    loc_level_boss_clown = level_boss_clown + " Complete"
    loc_level_boss_clown_topgrade = level_boss_clown + " Top Grade"
    loc_level_boss_clown_dlc_chaliced = level_boss_clown + " Chalice Complete"
    loc_level_boss_clown_event_defeat = _loc_event_ + level_boss_clown + " Defeated"
    loc_level_boss_clown_event_agrade = _loc_event_ + loc_level_boss_clown_topgrade
    loc_level_boss_clown_event_dlc_chaliced = _loc_event_ + loc_level_boss_clown_dlc_chaliced
    loc_level_boss_dragon = level_boss_dragon + " Complete"
    loc_level_boss_dragon_topgrade = level_boss_dragon + " Top Grade"
    loc_level_boss_dragon_dlc_chaliced = level_boss_dragon + " Chalice Complete"
    loc_level_boss_dragon_event_defeat = _loc_event_ + level_boss_dragon + " Defeated"
    loc_level_boss_dragon_event_agrade = _loc_event_ + loc_level_boss_dragon_topgrade
    loc_level_boss_dragon_event_dlc_chaliced = _loc_event_ + loc_level_boss_dragon_dlc_chaliced
    loc_level_boss_bee = level_boss_bee + " Complete"
    loc_level_boss_bee_topgrade = level_boss_bee + " Top Grade"
    loc_level_boss_bee_dlc_chaliced = level_boss_bee + " Chalice Complete"
    loc_level_boss_bee_event_defeat = _loc_event_ + level_boss_bee + " Defeated"
    loc_level_boss_bee_event_agrade = _loc_event_ + loc_level_boss_bee_topgrade
    loc_level_boss_bee_event_dlc_chaliced = _loc_event_ + loc_level_boss_bee_dlc_chaliced
    loc_level_boss_pirate = level_boss_pirate + " Complete"
    loc_level_boss_pirate_topgrade = level_boss_pirate + " Top Grade"
    loc_level_boss_pirate_dlc_chaliced = level_boss_pirate + " Chalice Complete"
    loc_level_boss_pirate_event_defeat = _loc_event_ + level_boss_pirate + " Defeated"
    loc_level_boss_pirate_event_agrade = _loc_event_ + loc_level_boss_pirate_topgrade
    loc_level_boss_pirate_event_dlc_chaliced = _loc_event_ + loc_level_boss_pirate_dlc_chaliced
    loc_level_boss_mouse = level_boss_mouse + " Complete"
    loc_level_boss_mouse_topgrade = level_boss_mouse + " Top Grade"
    loc_level_boss_mouse_dlc_chaliced = level_boss_mouse + " Chalice Complete"
    loc_level_boss_mouse_event_defeat = _loc_event_ + level_boss_mouse + " Defeated"
    loc_level_boss_mouse_event_agrade = _loc_event_ + loc_level_boss_mouse_topgrade
    loc_level_boss_mouse_event_dlc_chaliced = _loc_event_ + loc_level_boss_mouse_dlc_chaliced
    loc_level_boss_sallystageplay = level_boss_sallystageplay + " Complete"
    loc_level_boss_sallystageplay_secret = level_boss_sallystageplay + " Secret Complete"
    loc_level_boss_sallystageplay_topgrade = level_boss_sallystageplay + " Top Grade"
    loc_level_boss_sallystageplay_dlc_chaliced = level_boss_sallystageplay + " Chalice Complete"
    loc_level_boss_sallystageplay_event_defeat = _loc_event_ + level_boss_sallystageplay + " Defeated"
    loc_level_boss_sallystageplay_event_agrade = _loc_event_ + loc_level_boss_sallystageplay_topgrade
    loc_level_boss_sallystageplay_event_dlc_chaliced = _loc_event_ + loc_level_boss_sallystageplay_dlc_chaliced
    loc_level_boss_train = level_boss_train + " Complete"
    loc_level_boss_train_topgrade = level_boss_train + " Top Grade"
    loc_level_boss_train_dlc_chaliced = level_boss_train + " Chalice Complete"
    loc_level_boss_train_event_defeat = _loc_event_ + level_boss_train + " Defeated"
    loc_level_boss_train_event_agrade = _loc_event_ + loc_level_boss_train_topgrade
    loc_level_boss_train_event_dlc_chaliced = _loc_event_ + loc_level_boss_train_dlc_chaliced
    loc_level_boss_kingdice = level_boss_kingdice + " Complete"
    loc_level_boss_kingdice_topgrade = level_boss_kingdice + " Top Grade"
    loc_level_boss_kingdice_dlc_chaliced = level_boss_kingdice + " Chalice Complete"
    loc_level_boss_kingdice_event_defeat = _loc_event_ + level_boss_kingdice + " Defeated"
    loc_level_boss_kingdice_event_agrade = _loc_event_ + loc_level_boss_kingdice_topgrade
    loc_level_boss_kingdice_event_dlc_chaliced = _loc_event_ + loc_level_boss_kingdice_dlc_chaliced
    loc_level_boss_devil = level_boss_devil + " Complete"
    loc_level_boss_devil_topgrade = level_boss_devil + " Top Grade"
    loc_level_boss_devil_dlc_chaliced = level_boss_devil + " Chalice Complete"
    loc_level_boss_devil_event_defeated = _loc_event_ + level_boss_devil + " Defeated"
    loc_level_boss_devil_event_agrade = _loc_event_ + loc_level_boss_devil_topgrade
    loc_level_boss_devil_event_dlc_chaliced = _loc_event_ + loc_level_boss_devil_dlc_chaliced
    loc_level_dlc_boss_oldman = level_dlc_boss_oldman + " Complete"
    loc_level_dlc_boss_oldman_topgrade = level_dlc_boss_oldman + " Top Grade"
    loc_level_dlc_boss_oldman_dlc_chaliced = level_dlc_boss_oldman + " Chalice Complete"
    loc_level_dlc_boss_oldman_event_defeat = _loc_event_ + level_dlc_boss_oldman + " Defeated"
    loc_level_dlc_boss_oldman_event_agrade = _loc_event_ + loc_level_dlc_boss_oldman_topgrade
    loc_level_dlc_boss_oldman_event_dlc_chaliced = _loc_event_ + loc_level_dlc_boss_oldman_dlc_chaliced
    loc_level_dlc_boss_rumrunners = level_dlc_boss_rumrunners + " Complete"
    loc_level_dlc_boss_rumrunners_topgrade = level_dlc_boss_rumrunners + " Top Grade"
    loc_level_dlc_boss_rumrunners_dlc_chaliced = level_dlc_boss_rumrunners + " Chalice Complete"
    loc_level_dlc_boss_rumrunners_event_defeat = _loc_event_ + level_dlc_boss_rumrunners + " Defeated"
    loc_level_dlc_boss_rumrunners_event_agrade = _loc_event_ + loc_level_dlc_boss_rumrunners_topgrade
    loc_level_dlc_boss_rumrunners_event_dlc_chaliced = _loc_event_ + loc_level_dlc_boss_rumrunners_dlc_chaliced
    loc_level_dlc_boss_snowcult = level_dlc_boss_snowcult + " Complete"
    loc_level_dlc_boss_snowcult_topgrade = level_dlc_boss_snowcult + " Top Grade"
    loc_level_dlc_boss_snowcult_dlc_chaliced = level_dlc_boss_snowcult + " Chalice Complete"
    loc_level_dlc_boss_snowcult_event_defeat = _loc_event_ + level_dlc_boss_snowcult + " Defeated"
    loc_level_dlc_boss_snowcult_event_agrade = _loc_event_ + loc_level_dlc_boss_snowcult_topgrade
    loc_level_dlc_boss_snowcult_event_dlc_chaliced = _loc_event_ + loc_level_dlc_boss_snowcult_dlc_chaliced
    loc_level_dlc_boss_airplane = level_dlc_boss_airplane + " Complete"
    loc_level_dlc_boss_airplane_secret = level_dlc_boss_airplane + " Secret Complete"
    loc_level_dlc_boss_airplane_topgrade = level_dlc_boss_airplane + " Top Grade"
    loc_level_dlc_boss_airplane_dlc_chaliced = level_dlc_boss_airplane + " Chalice Complete"
    loc_level_dlc_boss_airplane_event_defeat = _loc_event_ + level_dlc_boss_airplane + " Defeated"
    loc_level_dlc_boss_airplane_event_agrade = _loc_event_ + loc_level_dlc_boss_airplane_topgrade
    loc_level_dlc_boss_airplane_event_dlc_chaliced = _loc_event_ + loc_level_dlc_boss_airplane_dlc_chaliced
    loc_level_dlc_boss_saltbaker = level_dlc_boss_saltbaker + " Complete"
    loc_level_dlc_boss_saltbaker_topgrade = level_dlc_boss_saltbaker + " Top Grade"
    loc_level_dlc_boss_saltbaker_dlc_chaliced = level_dlc_boss_saltbaker + " Chalice Complete"
    loc_level_dlc_boss_saltbaker_event_defeated = _loc_event_ + level_dlc_boss_saltbaker + " Defeated"
    loc_level_dlc_boss_saltbaker_event_agrade = _loc_event_ + loc_level_dlc_boss_saltbaker_topgrade
    loc_level_dlc_boss_saltbaker_event_dlc_chaliced = _loc_event_ + loc_level_dlc_boss_saltbaker_dlc_chaliced
    loc_level_boss_plane_blimp = level_boss_plane_blimp + " Complete"
    loc_level_boss_plane_blimp_topgrade = level_boss_plane_blimp + " Top Grade"
    loc_level_boss_plane_blimp_dlc_chaliced = level_boss_plane_blimp + " Chalice Complete"
    loc_level_boss_plane_blimp_event_defeat = _loc_event_ + level_boss_plane_blimp + " Defeated"
    loc_level_boss_plane_blimp_event_agrade = _loc_event_ + loc_level_boss_plane_blimp_topgrade
    loc_level_boss_plane_blimp_event_dlc_chaliced = _loc_event_ + loc_level_boss_plane_blimp_dlc_chaliced
    loc_level_boss_plane_genie = level_boss_plane_genie + " Complete"
    loc_level_boss_plane_genie_secret = level_boss_plane_genie + " Secret Complete"
    loc_level_boss_plane_genie_topgrade = level_boss_plane_genie + " Top Grade"
    loc_level_boss_plane_genie_dlc_chaliced = level_boss_plane_genie + " Chalice Complete"
    loc_level_boss_plane_genie_event_defeat = _loc_event_ + level_boss_plane_genie + " Defeated"
    loc_level_boss_plane_genie_event_agrade = _loc_event_ + loc_level_boss_plane_genie_topgrade
    loc_level_boss_plane_genie_event_dlc_chaliced = _loc_event_ + loc_level_boss_plane_genie_dlc_chaliced
    loc_level_boss_plane_bird = level_boss_plane_bird + " Complete"
    loc_level_boss_plane_bird_topgrade = level_boss_plane_bird + " Top Grade"
    loc_level_boss_plane_bird_dlc_chaliced = level_boss_plane_bird + " Chalice Complete"
    loc_level_boss_plane_bird_event_defeat = _loc_event_ + level_boss_plane_bird + " Defeated"
    loc_level_boss_plane_bird_event_agrade = _loc_event_ + loc_level_boss_plane_bird_topgrade
    loc_level_boss_plane_bird_event_dlc_chaliced = _loc_event_ + loc_level_boss_plane_bird_dlc_chaliced
    loc_level_boss_plane_mermaid = level_boss_plane_mermaid + " Complete"
    loc_level_boss_plane_mermaid_topgrade = level_boss_plane_mermaid + " Top Grade"
    loc_level_boss_plane_mermaid_dlc_chaliced = level_boss_plane_mermaid + " Chalice Complete"
    loc_level_boss_plane_mermaid_event_defeat = _loc_event_ + level_boss_plane_mermaid + " Defeated"
    loc_level_boss_plane_mermaid_event_agrade = _loc_event_ + loc_level_boss_plane_mermaid_topgrade
    loc_level_boss_plane_mermaid_event_dlc_chaliced = _loc_event_ + loc_level_boss_plane_mermaid_dlc_chaliced
    loc_level_boss_plane_robot = level_boss_plane_robot + " Complete"
    loc_level_boss_plane_robot_topgrade = level_boss_plane_robot + " Top Grade"
    loc_level_boss_plane_robot_dlc_chaliced = level_boss_plane_robot + " Chalice Complete"
    loc_level_boss_plane_robot_event_defeat = _loc_event_ + level_boss_plane_robot + " Defeated"
    loc_level_boss_plane_robot_event_agrade = _loc_event_ + loc_level_boss_plane_robot_topgrade
    loc_level_boss_plane_robot_event_dlc_chaliced = _loc_event_ + loc_level_boss_plane_robot_dlc_chaliced
    loc_level_dlc_boss_plane_cowboy = level_dlc_boss_plane_cowboy + " Complete"
    loc_level_dlc_boss_plane_cowboy_topgrade = level_dlc_boss_plane_cowboy + " Top Grade"
    loc_level_dlc_boss_plane_cowboy_dlc_chaliced = level_dlc_boss_plane_cowboy + " Chalice Complete"
    loc_level_dlc_boss_plane_cowboy_event_defeat = _loc_event_ + level_dlc_boss_plane_cowboy + " Defeated"
    loc_level_dlc_boss_plane_cowboy_event_agrade = _loc_event_ + loc_level_dlc_boss_plane_cowboy_topgrade
    loc_level_dlc_boss_plane_cowboy_event_dlc_chaliced = _loc_event_ + loc_level_dlc_boss_plane_cowboy_dlc_chaliced

    loc_level_dicepalace_boss1 = level_dicepalace_boss1 + " Complete"
    loc_level_dicepalace_boss1_dlc_chaliced = level_dicepalace_boss1 + " Chalice Complete"
    loc_level_dicepalace_boss2 = level_dicepalace_boss2 + " Complete"
    loc_level_dicepalace_boss2_dlc_chaliced = level_dicepalace_boss2 + " Chalice Complete"
    loc_level_dicepalace_boss3 = level_dicepalace_boss3 + " Complete"
    loc_level_dicepalace_boss3_dlc_chaliced = level_dicepalace_boss3 + " Chalice Complete"
    loc_level_dicepalace_boss4 = level_dicepalace_boss4 + " Complete"
    loc_level_dicepalace_boss4_dlc_chaliced = level_dicepalace_boss4 + " Chalice Complete"
    loc_level_dicepalace_boss5 = level_dicepalace_boss5 + " Complete"
    loc_level_dicepalace_boss5_dlc_chaliced = level_dicepalace_boss5 + " Chalice Complete"
    loc_level_dicepalace_boss6 = level_dicepalace_boss6 + " Complete"
    loc_level_dicepalace_boss6_dlc_chaliced = level_dicepalace_boss6 + " Chalice Complete"
    loc_level_dicepalace_boss7 = level_dicepalace_boss7 + " Complete"
    loc_level_dicepalace_boss7_dlc_chaliced = level_dicepalace_boss7 + " Chalice Complete"
    loc_level_dicepalace_boss8 = level_dicepalace_boss8 + " Complete"
    loc_level_dicepalace_boss8_dlc_chaliced = level_dicepalace_boss8 + " Chalice Complete"
    loc_level_dicepalace_boss9 = level_dicepalace_boss9 + " Complete"
    loc_level_dicepalace_boss9_dlc_chaliced = level_dicepalace_boss9 + " Chalice Complete"
    loc_level_dicepalace_boss_booze = level_dicepalace_boss_booze + " Complete"
    loc_level_dicepalace_boss_booze_dlc_chaliced = level_dicepalace_boss_booze + " Chalice Complete"
    loc_level_dicepalace_boss_chips = level_dicepalace_boss_chips + " Complete"
    loc_level_dicepalace_boss_chips_dlc_chaliced = level_dicepalace_boss_chips + " Chalice Complete"
    loc_level_dicepalace_boss_cigar = level_dicepalace_boss_cigar + " Complete"
    loc_level_dicepalace_boss_cigar_dlc_chaliced = level_dicepalace_boss_cigar + " Chalice Complete"
    loc_level_dicepalace_boss_domino = level_dicepalace_boss_domino + " Complete"
    loc_level_dicepalace_boss_domino_dlc_chaliced = level_dicepalace_boss_domino + " Chalice Complete"
    loc_level_dicepalace_boss_rabbit = level_dicepalace_boss_rabbit + " Complete"
    loc_level_dicepalace_boss_rabbit_dlc_chaliced = level_dicepalace_boss_rabbit + " Chalice Complete"
    loc_level_dicepalace_boss_plane_horse = level_dicepalace_boss_plane_horse + " Complete"
    loc_level_dicepalace_boss_plane_horse_dlc_chaliced = level_dicepalace_boss_plane_horse + " Chalice Complete"
    loc_level_dicepalace_boss_roulette = level_dicepalace_boss_roulette + " Complete"
    loc_level_dicepalace_boss_roulette_dlc_chaliced = level_dicepalace_boss_roulette + " Chalice Complete"
    loc_level_dicepalace_boss_eightball = level_dicepalace_boss_eightball + " Complete"
    loc_level_dicepalace_boss_eightball_dlc_chaliced = level_dicepalace_boss_eightball + " Chalice Complete"
    loc_level_dicepalace_boss_plane_memory = level_dicepalace_boss_plane_memory + " Complete"
    loc_level_dicepalace_boss_plane_memory_dlc_chaliced = level_dicepalace_boss_plane_memory + " Chalice Complete"

    loc_level_rungun_forest = level_rungun_forest + " Complete"
    loc_level_rungun_forest_agrade = level_rungun_forest + " Top Grade"
    loc_level_rungun_forest_pacifist = level_rungun_forest + " Pacifist"
    loc_level_rungun_forest_coin1 = level_rungun_forest + " Coin 1"
    loc_level_rungun_forest_coin2 = level_rungun_forest + " Coin 2"
    loc_level_rungun_forest_coin3 = level_rungun_forest + " Coin 3"
    loc_level_rungun_forest_coin4 = level_rungun_forest + " Coin 4"
    loc_level_rungun_forest_coin5 = level_rungun_forest + " Coin 5"
    loc_level_rungun_forest_dlc_chaliced = level_rungun_forest + " Chalice Complete"
    loc_level_rungun_forest_event_agrade = _loc_event_ + loc_level_rungun_forest_agrade
    loc_level_rungun_forest_event_pacifist = _loc_event_ + loc_level_rungun_forest_pacifist

    loc_level_rungun_tree = level_rungun_tree + " Complete"
    loc_level_rungun_tree_agrade = level_rungun_tree + " Top Grade"
    loc_level_rungun_tree_pacifist = level_rungun_tree + " Pacifist"
    loc_level_rungun_tree_coin1 = level_rungun_tree + " Coin 1"
    loc_level_rungun_tree_coin2 = level_rungun_tree + " Coin 2"
    loc_level_rungun_tree_coin3 = level_rungun_tree + " Coin 3"
    loc_level_rungun_tree_coin4 = level_rungun_tree + " Coin 4"
    loc_level_rungun_tree_coin5 = level_rungun_tree + " Coin 5"
    loc_level_rungun_tree_dlc_chaliced = level_rungun_tree + " Chalice Complete"
    loc_level_rungun_tree_event_agrade = _loc_event_ + loc_level_rungun_tree_agrade
    loc_level_rungun_tree_event_pacifist = _loc_event_ + loc_level_rungun_tree_pacifist

    loc_level_rungun_circus = level_rungun_circus + " Complete"
    loc_level_rungun_circus_agrade = level_rungun_circus + " Top Grade"
    loc_level_rungun_circus_pacifist = level_rungun_circus + " Pacifist"
    loc_level_rungun_circus_coin1 = level_rungun_circus + " Coin 1"
    loc_level_rungun_circus_coin2 = level_rungun_circus + " Coin 2"
    loc_level_rungun_circus_coin3 = level_rungun_circus + " Coin 3"
    loc_level_rungun_circus_coin4 = level_rungun_circus + " Coin 4"
    loc_level_rungun_circus_coin5 = level_rungun_circus + " Coin 5"
    loc_level_rungun_circus_dlc_chaliced = level_rungun_circus + " Chalice Complete"
    loc_level_rungun_circus_event_agrade = _loc_event_ + loc_level_rungun_circus_agrade
    loc_level_rungun_circus_event_pacifist = _loc_event_ + loc_level_rungun_circus_pacifist

    loc_level_rungun_funhouse = level_rungun_funhouse + " Complete"
    loc_level_rungun_funhouse_agrade = level_rungun_funhouse + " Top Grade"
    loc_level_rungun_funhouse_pacifist = level_rungun_funhouse + " Pacifist"
    loc_level_rungun_funhouse_coin1 = level_rungun_funhouse + " Coin 1"
    loc_level_rungun_funhouse_coin2 = level_rungun_funhouse + " Coin 2"
    loc_level_rungun_funhouse_coin3 = level_rungun_funhouse + " Coin 3"
    loc_level_rungun_funhouse_coin4 = level_rungun_funhouse + " Coin 4"
    loc_level_rungun_funhouse_coin5 = level_rungun_funhouse + " Coin 5"
    loc_level_rungun_funhouse_dlc_chaliced = level_rungun_funhouse + " Chalice Complete"
    loc_level_rungun_funhouse_event_agrade = _loc_event_ + loc_level_rungun_funhouse_agrade
    loc_level_rungun_funhouse_event_pacifist = _loc_event_ + loc_level_rungun_funhouse_pacifist

    loc_level_rungun_harbour = level_rungun_harbour + " Complete"
    loc_level_rungun_harbour_agrade = level_rungun_harbour + " Top Grade"
    loc_level_rungun_harbour_pacifist = level_rungun_harbour + " Pacifist"
    loc_level_rungun_harbour_coin1 = level_rungun_harbour + " Coin 1"
    loc_level_rungun_harbour_coin2 = level_rungun_harbour + " Coin 2"
    loc_level_rungun_harbour_coin3 = level_rungun_harbour + " Coin 3"
    loc_level_rungun_harbour_coin4 = level_rungun_harbour + " Coin 4"
    loc_level_rungun_harbour_coin5 = level_rungun_harbour + " Coin 5"
    loc_level_rungun_harbour_dlc_chaliced = level_rungun_harbour + " Chalice Complete"
    loc_level_rungun_harbour_event_agrade = _loc_event_ + loc_level_rungun_harbour_agrade
    loc_level_rungun_harbour_event_pacifist = _loc_event_ + loc_level_rungun_harbour_pacifist

    loc_level_rungun_mountain = level_rungun_mountain + " Complete"
    loc_level_rungun_mountain_agrade = level_rungun_mountain + " Top Grade"
    loc_level_rungun_mountain_pacifist = level_rungun_mountain + " Pacifist"
    loc_level_rungun_mountain_coin1 = level_rungun_mountain + " Coin 1"
    loc_level_rungun_mountain_coin2 = level_rungun_mountain + " Coin 2"
    loc_level_rungun_mountain_coin3 = level_rungun_mountain + " Coin 3"
    loc_level_rungun_mountain_coin4 = level_rungun_mountain + " Coin 4"
    loc_level_rungun_mountain_coin5 = level_rungun_mountain + " Coin 5"
    loc_level_rungun_mountain_dlc_chaliced = level_rungun_mountain + " Chalice Complete"
    loc_level_rungun_mountain_event_agrade = _loc_event_ + loc_level_rungun_mountain_agrade
    loc_level_rungun_mountain_event_pacifist = _loc_event_ + loc_level_rungun_mountain_pacifist

    loc_level_mausoleum_i = level_mausoleum_i
    loc_level_mausoleum_ii = level_mausoleum_ii
    loc_level_mausoleum_iii = level_mausoleum_iii

    loc_level_dlc_chesscastle_pawn = level_dlc_chesscastle_pawn + " Complete"
    loc_level_dlc_chesscastle_pawn_dlc_chaliced = level_dlc_chesscastle_pawn + " Chalice Complete"
    loc_level_dlc_chesscastle_knight = level_dlc_chesscastle_knight + " Complete"
    loc_level_dlc_chesscastle_knight_dlc_chaliced = level_dlc_chesscastle_knight + " Chalice Complete"
    loc_level_dlc_chesscastle_bishop = level_dlc_chesscastle_bishop + " Complete"
    loc_level_dlc_chesscastle_bishop_dlc_chaliced = level_dlc_chesscastle_bishop + " Chalice Complete"
    loc_level_dlc_chesscastle_rook = level_dlc_chesscastle_rook + " Complete"
    loc_level_dlc_chesscastle_rook_dlc_chaliced = level_dlc_chesscastle_rook + " Chalice Complete"
    loc_level_dlc_chesscastle_queen = level_dlc_chesscastle_queen + " Complete"
    loc_level_dlc_chesscastle_queen_dlc_chaliced = level_dlc_chesscastle_queen + " Chalice Complete"
    loc_level_dlc_chesscastle_run = level_dlc_chesscastle_run + " Complete"
    loc_level_dlc_chesscastle_run_dlc_chaliced = level_dlc_chesscastle_run + " Chalice Complete"

    loc_level_dlc_graveyard = level_dlc_graveyard + " Complete"

    loc_shop_weapon1 = level_shop + " Weapon 1"
    loc_shop_weapon1_bought = loc_shop_weapon1 + " Bought"
    loc_shop_weapon2 = level_shop + " Weapon 2"
    loc_shop_weapon2_bought = loc_shop_weapon2 + " Bought"
    loc_shop_weapon3 = level_shop + " Weapon 3"
    loc_shop_weapon3_bought = loc_shop_weapon3 + " Bought"
    loc_shop_weapon4 = level_shop + " Weapon 4"
    loc_shop_weapon4_bought = loc_shop_weapon4 + " Bought"
    loc_shop_weapon5 = level_shop + " Weapon 5"
    loc_shop_weapon5_bought = loc_shop_weapon5 + " Bought"
    loc_shop_dlc_weapon6 = level_shop + " Weapon 6"
    loc_shop_dlc_weapon6_bought = loc_shop_dlc_weapon6 + " Bought"
    loc_shop_dlc_weapon7 = level_shop + " Weapon 7"
    loc_shop_dlc_weapon7_bought = loc_shop_dlc_weapon7 + " Bought"
    loc_shop_dlc_weapon8 = level_shop + " Weapon 8"
    loc_shop_dlc_weapon8_bought = loc_shop_dlc_weapon8 + " Bought"
    loc_shop_charm1 = level_shop + " Charm 1"
    loc_shop_charm1_bought = loc_shop_charm1 + " Bought"
    loc_shop_charm2 = level_shop + " Charm 2"
    loc_shop_charm2_bought = loc_shop_charm2 + " Bought"
    loc_shop_charm3 = level_shop + " Charm 3"
    loc_shop_charm3_bought = loc_shop_charm3 + " Bought"
    loc_shop_charm4 = level_shop + " Charm 4"
    loc_shop_charm4_bought = loc_shop_charm4 + " Bought"
    loc_shop_charm5 = level_shop + " Charm 5"
    loc_shop_charm5_bought = loc_shop_charm5 + " Bought"
    loc_shop_charm6 = level_shop + " Charm 6"
    loc_shop_charm6_bought = loc_shop_charm6 + " Bought"
    loc_shop_dlc_charm7 = level_shop + " Charm 7"
    loc_shop_dlc_charm7_bought = loc_shop_dlc_charm7 + " Bought"
    loc_shop_dlc_charm8 = level_shop + " Charm 8"
    loc_shop_dlc_charm8_bought = loc_shop_dlc_charm8 + " Bought"
    loc_shop_base_weapons = (loc_shop_weapon1, loc_shop_weapon2, loc_shop_weapon3, loc_shop_weapon4, loc_shop_weapon5)
    loc_shop_dlc_weapons = (loc_shop_dlc_weapon6, loc_shop_dlc_weapon7, loc_shop_dlc_weapon8)
    loc_shop_weapons = loc_shop_base_weapons + loc_shop_dlc_weapons
    loc_shop_base_charms = (
        loc_shop_charm1, loc_shop_charm2, loc_shop_charm3, loc_shop_charm4, loc_shop_charm5, loc_shop_charm6
    )
    loc_shop_dlc_charms = (loc_shop_dlc_charm7, loc_shop_dlc_charm8)
    loc_shop_charms = loc_shop_base_charms + loc_shop_dlc_charms
    loc_shop_items = loc_shop_weapons + loc_shop_charms

    loc_npc_mac = "Mac"
    loc_npc_canteen = "Canteen Hughes"
    loc_quest_buster = "Buster Quest"
    loc_quest_ginger = "Ginger Quest"
    loc_quest_4mel = "Barbershop Quartet Quest"
    loc_quest_lucien = "Lucien Quest"
    loc_quest_pacifist = "Pacifist Quest"
    loc_quest_silverworth = "Silverworth Quest"
    loc_quest_music = "Music Quest"
    loc_quest_ludwig = "Ludwig"
    loc_quest_wolfgang = "Wolfgang"

    loc_coin_isle1_secret = world_inkwell_1 + " Secret Coin"
    loc_coin_isle2_secret = world_inkwell_2 + " Secret Coin"
    loc_coin_isle3_secret = world_inkwell_3 + " Secret Coin"
    loc_coin_isleh_secret = world_inkwell_hell + " Secret Coin"
    loc_dlc_coin_isle4_secret = world_dlc_inkwell_4 + " Secret Coin"

    loc_dlc_cookie = "Astral Cookie"
    loc_dlc_npc_newscat = "Newsy Cat"
    loc_dlc_quest_cactusgirl = "Cactus Girl Quest"

    loc_dlc_curse_complete = "Divine Relic"

    loc_event_start_weapon = _loc_event_ + "Start Weapon"
    loc_event_start_weapon_ex = _loc_event_ + "Start Weapon EX"
    loc_event_isle1_secret_prereq = _loc_event_ + loc_coin_isle1_secret + " Prerequisite"
    loc_event_isle1_secret_prereq1 = loc_event_isle1_secret_prereq + " 1"
    loc_event_isle1_secret_prereq2 = loc_event_isle1_secret_prereq + " 2"
    loc_event_isle1_secret_prereq3 = loc_event_isle1_secret_prereq + " 3"
    loc_event_isle1_secret_prereq4 = loc_event_isle1_secret_prereq + " 4"
    loc_event_isle1_secret_prereq5 = loc_event_isle1_secret_prereq + " 5"
    loc_event_isle2_shortcut = _loc_event_ + world_inkwell_2 + " Shortcut"
    loc_event_quest_4mel_4th = _loc_event_ + "Barbershop Quartet 4th Member"
    loc_event_quest_ludwig = _loc_event_ + "Ludwig Quest"
    loc_event_quest_wolfgang = _loc_event_ + "Wolfgang Quest"
    loc_event_music = _loc_event_ + "Piano Music"
    loc_event_mausoleum = _loc_event_ + "Mausoleum"
    loc_event_dlc_cookie = _loc_event_ + "DLC Cookie"
    loc_event_dlc_curse_complete = _loc_event_ + loc_dlc_curse_complete

    loc_event_firstweapon = _loc_event_ + "First Weapon"
    loc_event_dlc_boatarrival = _loc_event_ + "Boat Arrives"

    loc_event_goal_devil = "Devil Goal"
    loc_event_dlc_goal_saltbaker = "Saltbaker Goal"

############################################# ITEM NAMES #############################################
class ItemNames:
    # Prefixes
    _item_event_ = "Event "
    _item_progressive = "Progressive "

    # Junk
    item_level_generic = "Present"
    item_level_extrahealth = "+1 Health"
    item_level_supercharge = "Super Charge"
    item_level_fastfire = "Fast Fire"
    item_level_4 = "Item Id 4"

    # Weapons
    item_weapon = "Weapon"
    item_weapon_peashooter = "Peashooter"
    item_weapon_spread = "Spread"
    item_weapon_chaser = "Chaser"
    item_weapon_lobber = "Lobber"
    item_weapon_charge = "Charge"
    item_weapon_roundabout = "Roundabout"
    item_dlc_weapon = "DLC Weapon"
    item_weapon_dlc_crackshot = "Crackshot"
    item_weapon_dlc_converge = "Converge"
    item_weapon_dlc_twistup = "Twist-Up"

    # Weapon EX
    _weapon_ex = " EX"
    item_weapon_ex = item_weapon + _weapon_ex
    item_weapon_peashooter_ex = item_weapon_peashooter + _weapon_ex
    item_weapon_spread_ex = item_weapon_spread + _weapon_ex
    item_weapon_chaser_ex = item_weapon_chaser + _weapon_ex
    item_weapon_lobber_ex = item_weapon_lobber + _weapon_ex
    item_weapon_charge_ex = item_weapon_charge + _weapon_ex
    item_weapon_roundabout_ex = item_weapon_roundabout + _weapon_ex
    item_dlc_weapon_ex = item_dlc_weapon + _weapon_ex
    item_weapon_dlc_crackshot_ex = item_weapon_dlc_crackshot + _weapon_ex
    item_weapon_dlc_converge_ex = item_weapon_dlc_converge + _weapon_ex
    item_weapon_dlc_twistup_ex = item_weapon_dlc_twistup + _weapon_ex

    # Progressive Weapon
    item_p_weapon = _item_progressive + "Weapon"
    item_p_weapon_peashooter = _item_progressive + "Peashooter"
    item_p_weapon_spread = _item_progressive + "Spread"
    item_p_weapon_chaser = _item_progressive + "Chaser"
    item_p_weapon_lobber = _item_progressive + "Lobber"
    item_p_weapon_charge = _item_progressive + "Charge"
    item_p_weapon_roundabout = _item_progressive + "Roundabout"
    item_p_dlc_weapon = _item_progressive + "DLC Weapon"
    item_p_weapon_dlc_crackshot = _item_progressive + "Crackshot"
    item_p_weapon_dlc_converge = _item_progressive + "Converge"
    item_p_weapon_dlc_twistup = _item_progressive + "Twist-Up"

    # Charms
    item_charm = "Charm"
    item_charm_heart = "Heart"
    item_charm_smokebomb = "Smoke Bomb"
    item_charm_psugar = "P. Sugar"
    item_charm_coffee = "Coffee"
    item_charm_twinheart = "Twin Heart"
    item_charm_whetstone = "Whetstone"
    item_dlc_charm = "DLC Charm"
    item_charm_dlc_heartring = "Heart Ring"
    item_charm_dlc_broken_relic = "Broken Relic"
    item_charm_dlc_cookie = "Astral Cookie"

    # Super
    item_super_i = "Super Art I"
    item_super_ii = "Super Art II"
    item_super_iii = "Super Art III"

    item_super_dlc_c_i = "Chalice Super Art I"
    item_super_dlc_c_ii = "Chalice Super Art II"
    item_super_dlc_c_iii = "Chalice Super Art III"

    # Abilities
    item_ability_parry = "Parry"
    item_ability_dash = "Dash"
    item_ability_duck = "Duck"
    item_ability_plane_shrink = "Plane Shrink"
    item_ability_plane_parry = "Plane Parry"

    item_ability_dlc_cparry = "Chalice Parry"
    item_ability_dlc_cdash = "Chalice Dash"
    item_ability_dlc_p_cdash = _item_progressive + "Chalice Dash"
    item_ability_dlc_cdoublejump = "Chalice Double Jump"
    item_ability_dlc_cduck = "Chalice Duck"
    item_ability_dlc_cplane_shrink = "Chalice Plane Shrink"
    item_ability_dlc_cplane_parry = "Chalice Plane Parry"

    item_ability_aim_left = "Aim Left"
    item_ability_aim_right = "Aim Right"
    item_ability_aim_up = "Aim Up"
    item_ability_aim_down = "Aim Down"
    item_ability_aim_upleft = "Aim Up-Left"
    item_ability_aim_upright = "Aim Up-Right"
    item_ability_aim_downleft = "Aim Down-Left"
    item_ability_aim_downright = "Aim Down-Right"

    item_ability_dlc_c_aim_left = "Chalice Aim Left"
    item_ability_dlc_c_aim_right = "Chalice Aim Right"
    item_ability_dlc_c_aim_up = "Chalice Aim Up"
    item_ability_dlc_c_aim_down = "Chalice Aim Down"
    item_ability_dlc_c_aim_upleft = "Chalice Aim Up-Left"
    item_ability_dlc_c_aim_upright = "Chalice Aim Up-Right"
    item_ability_dlc_c_aim_downleft = "Chalice Aim Down-Left"
    item_ability_dlc_c_aim_downright = "Chalice Aim Down-Right"

    # Essential
    item_coin = "Coin"
    item_coin2 = "2 Coins"
    item_coin3 = "3 Coins"
    item_progressive_plane = _item_progressive + "Plane"
    item_plane = "Plane"
    item_plane_gun = "Plane Peashooter"
    item_plane_gun_a = "Plane Gun"
    item_plane_ex = "Plane EX"
    item_plane_bombs = "Plane Bombs"
    item_plane_super = "Plane Super"
    item_contract = "Contract"
    item_healthupgrade = "+1 Max Health"
    item_dlc_boat = "Boat"
    item_dlc_ingredient = "Ingredient"
    item_dlc_cplane_gun = "Chalice Plane Peashooter"
    item_dlc_cplane_gun_a = "Chalice Plane Gun"
    item_dlc_cplane_ex = "Chalice Plane EX"
    item_dlc_cplane_bombs = "Chalice Plane Bombs"
    item_dlc_cplane_super = "Chalice Plane Super"

    # Traps
    item_level_trap_fingerjam = "Finger Jam"
    item_level_trap_slowfire = "Slow Fire"
    item_level_trap_superdrain = "Super Drain"
    item_level_trap_loadout = "Loadout Mixup"
    item_level_trap_screen = "Screen Trap"

    # Events
    item_event_null = "null"
    item_event_boss_defeated = _item_event_ + "Boss Defeated"
    item_event_mausoleum = _item_event_ + "Mausoleum"
    item_event_isle1_secret_prereq = _item_event_ + LocationNames.world_inkwell_1 + " Secret Coin Prerequisite"
    item_event_isle2_shortcut = _item_event_ + LocationNames.loc_event_isle2_shortcut + " Accessed"
    item_event_quest_4mel_4th = _item_event_ + LocationNames.loc_event_quest_4mel_4th
    item_event_agrade = _item_event_ + "A Grade"
    item_event_pacifist = _item_event_ + "P Grade"
    item_event_ludwig = _item_event_ + "Lugwig"
    item_event_wolfgang = _item_event_ + "Wolfgang"
    item_event_music = _item_event_ + "Music Changed"
    item_event_dlc_start = _item_event_ + "DLC Start"
    item_event_charm_dlc_cookie = _item_event_ + item_charm_dlc_cookie
    item_event_dlc_boataccess = _item_event_ + "Boat Access"
    item_event_dlc_boss_chaliced = _item_event_ + "Boss Chalice Defeated"

    # Goals
    item_event_goal_devilko = "The Devil's Surrender"
    item_event_goal_dlc_saltbakerko = "Chef Saltbaker's Surrender"
