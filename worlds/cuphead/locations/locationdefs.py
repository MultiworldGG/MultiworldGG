from __future__ import annotations
from .locationbase import LocationData
from ..names import LocationNames

base_id = 12905168
base_dlc_id = 12909264

def lid(i: int): return base_id+i
def dlc_lid(i: int): return base_dlc_id+i

# Locations
# Next ids: 128, 78
# Level Locations
location_level_tutorial: dict[str, LocationData] = {
    LocationNames.loc_level_tutorial: LocationData(lid(0)),
    LocationNames.loc_level_tutorial_coin: LocationData(lid(1)),
    #LocationNames.loc_level_plane_tutorial: LocationData(lid(2)),
}
location_level_dlc_tutorial: dict[str, LocationData] = {
    LocationNames.loc_level_dlc_tutorial: LocationData(dlc_lid(0)),
    LocationNames.loc_level_dlc_tutorial_coin: LocationData(dlc_lid(1)),
}

location_level_boss: dict[str, LocationData] = {
    LocationNames.loc_level_boss_veggies: LocationData(lid(3)),
    LocationNames.loc_level_boss_slime: LocationData(lid(5)),
    LocationNames.loc_level_boss_frogs: LocationData(lid(7)),
    LocationNames.loc_level_boss_flower: LocationData(lid(9)),
    LocationNames.loc_level_boss_baroness: LocationData(lid(11)),
    LocationNames.loc_level_boss_clown: LocationData(lid(13)),
    LocationNames.loc_level_boss_dragon: LocationData(lid(15)),
    LocationNames.loc_level_boss_bee: LocationData(lid(17)),
    LocationNames.loc_level_boss_pirate: LocationData(lid(19)),
    LocationNames.loc_level_boss_mouse: LocationData(lid(21)),
    LocationNames.loc_level_boss_sallystageplay: LocationData(lid(23)),
    LocationNames.loc_level_boss_train: LocationData(lid(25)),
    LocationNames.loc_level_boss_kingdice: LocationData(lid(27)),

    LocationNames.loc_level_boss_plane_blimp: LocationData(lid(29)),
    LocationNames.loc_level_boss_plane_genie: LocationData(lid(31)),
    LocationNames.loc_level_boss_plane_bird: LocationData(lid(33)),
    LocationNames.loc_level_boss_plane_mermaid: LocationData(lid(35)),
    LocationNames.loc_level_boss_plane_robot: LocationData(lid(37)),
}
location_level_boss_final: dict[str, LocationData] = {
    LocationNames.loc_level_boss_devil: LocationData(lid(39)),
}
location_level_boss_topgrade: dict[str, LocationData] = {
    LocationNames.loc_level_boss_veggies_topgrade: LocationData(lid(4)),
    LocationNames.loc_level_boss_slime_topgrade: LocationData(lid(6)),
    LocationNames.loc_level_boss_frogs_topgrade: LocationData(lid(8)),
    LocationNames.loc_level_boss_flower_topgrade: LocationData(lid(10)),
    LocationNames.loc_level_boss_baroness_topgrade: LocationData(lid(12)),
    LocationNames.loc_level_boss_clown_topgrade: LocationData(lid(14)),
    LocationNames.loc_level_boss_dragon_topgrade: LocationData(lid(16)),
    LocationNames.loc_level_boss_bee_topgrade: LocationData(lid(18)),
    LocationNames.loc_level_boss_pirate_topgrade: LocationData(lid(20)),
    LocationNames.loc_level_boss_mouse_topgrade: LocationData(lid(22)),
    LocationNames.loc_level_boss_sallystageplay_topgrade: LocationData(lid(24)),
    LocationNames.loc_level_boss_train_topgrade: LocationData(lid(26)),
    LocationNames.loc_level_boss_kingdice_topgrade: LocationData(lid(28)),

    LocationNames.loc_level_boss_plane_blimp_topgrade: LocationData(lid(30)),
    LocationNames.loc_level_boss_plane_genie_topgrade: LocationData(lid(32)),
    LocationNames.loc_level_boss_plane_bird_topgrade: LocationData(lid(34)),
    LocationNames.loc_level_boss_plane_mermaid_topgrade: LocationData(lid(36)),
    LocationNames.loc_level_boss_plane_robot_topgrade: LocationData(lid(38)),
}
location_level_boss_dlc_chaliced: dict[str, LocationData] = {
    LocationNames.loc_level_boss_veggies_dlc_chaliced: LocationData(dlc_lid(2)),
    LocationNames.loc_level_boss_slime_dlc_chaliced: LocationData(dlc_lid(3)),
    LocationNames.loc_level_boss_frogs_dlc_chaliced: LocationData(dlc_lid(4)),
    LocationNames.loc_level_boss_flower_dlc_chaliced: LocationData(dlc_lid(5)),
    LocationNames.loc_level_boss_baroness_dlc_chaliced: LocationData(dlc_lid(6)),
    LocationNames.loc_level_boss_clown_dlc_chaliced: LocationData(dlc_lid(7)),
    LocationNames.loc_level_boss_dragon_dlc_chaliced: LocationData(dlc_lid(8)),
    LocationNames.loc_level_boss_bee_dlc_chaliced: LocationData(dlc_lid(9)),
    LocationNames.loc_level_boss_pirate_dlc_chaliced: LocationData(dlc_lid(10)),
    LocationNames.loc_level_boss_mouse_dlc_chaliced: LocationData(dlc_lid(11)),
    LocationNames.loc_level_boss_sallystageplay_dlc_chaliced: LocationData(dlc_lid(12)),
    LocationNames.loc_level_boss_train_dlc_chaliced: LocationData(dlc_lid(13)),
    LocationNames.loc_level_boss_kingdice_dlc_chaliced: LocationData(dlc_lid(14)),
    LocationNames.loc_level_boss_plane_blimp_dlc_chaliced: LocationData(dlc_lid(15)),
    LocationNames.loc_level_boss_plane_genie_dlc_chaliced: LocationData(dlc_lid(16)),
    LocationNames.loc_level_boss_plane_bird_dlc_chaliced: LocationData(dlc_lid(17)),
    LocationNames.loc_level_boss_plane_mermaid_dlc_chaliced: LocationData(dlc_lid(18)),
    LocationNames.loc_level_boss_plane_robot_dlc_chaliced: LocationData(dlc_lid(19)),
}
location_level_boss_event_agrade: dict[str, LocationData] = {
    LocationNames.loc_level_boss_veggies_event_agrade: LocationData(None),
    LocationNames.loc_level_boss_slime_event_agrade: LocationData(None),
    LocationNames.loc_level_boss_frogs_event_agrade: LocationData(None),
    LocationNames.loc_level_boss_flower_event_agrade: LocationData(None),
    LocationNames.loc_level_boss_baroness_event_agrade: LocationData(None),
    LocationNames.loc_level_boss_clown_event_agrade: LocationData(None),
    LocationNames.loc_level_boss_dragon_event_agrade: LocationData(None),
    LocationNames.loc_level_boss_bee_event_agrade: LocationData(None),
    LocationNames.loc_level_boss_pirate_event_agrade: LocationData(None),
    LocationNames.loc_level_boss_mouse_event_agrade: LocationData(None),
    LocationNames.loc_level_boss_sallystageplay_event_agrade: LocationData(None),
    LocationNames.loc_level_boss_train_event_agrade: LocationData(None),
    LocationNames.loc_level_boss_kingdice_event_agrade: LocationData(None),
    LocationNames.loc_level_boss_plane_blimp_event_agrade: LocationData(None),
    LocationNames.loc_level_boss_plane_genie_event_agrade: LocationData(None),
    LocationNames.loc_level_boss_plane_bird_event_agrade: LocationData(None),
    LocationNames.loc_level_boss_plane_mermaid_event_agrade: LocationData(None),
    LocationNames.loc_level_boss_plane_robot_event_agrade: LocationData(None),
}
location_level_boss_event_dlc_chaliced: dict[str, LocationData] = {
    LocationNames.loc_level_boss_veggies_event_dlc_chaliced: LocationData(None),
    LocationNames.loc_level_boss_slime_event_dlc_chaliced: LocationData(None),
    LocationNames.loc_level_boss_frogs_event_dlc_chaliced: LocationData(None),
    LocationNames.loc_level_boss_flower_event_dlc_chaliced: LocationData(None),
    LocationNames.loc_level_boss_baroness_event_dlc_chaliced: LocationData(None),
    LocationNames.loc_level_boss_clown_event_dlc_chaliced: LocationData(None),
    LocationNames.loc_level_boss_dragon_event_dlc_chaliced: LocationData(None),
    LocationNames.loc_level_boss_bee_event_dlc_chaliced: LocationData(None),
    LocationNames.loc_level_boss_pirate_event_dlc_chaliced: LocationData(None),
    LocationNames.loc_level_boss_mouse_event_dlc_chaliced: LocationData(None),
    LocationNames.loc_level_boss_sallystageplay_event_dlc_chaliced: LocationData(None),
    LocationNames.loc_level_boss_train_event_dlc_chaliced: LocationData(None),
    LocationNames.loc_level_boss_kingdice_event_dlc_chaliced: LocationData(None),
    LocationNames.loc_level_boss_plane_blimp_event_dlc_chaliced: LocationData(None),
    LocationNames.loc_level_boss_plane_genie_event_dlc_chaliced: LocationData(None),
    LocationNames.loc_level_boss_plane_bird_event_dlc_chaliced: LocationData(None),
    LocationNames.loc_level_boss_plane_mermaid_event_dlc_chaliced: LocationData(None),
    LocationNames.loc_level_boss_plane_robot_event_dlc_chaliced: LocationData(None),
}
location_level_boss_final_topgrade: dict[str, LocationData] = {
    LocationNames.loc_level_boss_devil_topgrade: LocationData(lid(40))
}
location_level_boss_final_dlc_chaliced: dict[str, LocationData] = {
    LocationNames.loc_level_boss_devil_dlc_chaliced: LocationData(dlc_lid(20))
}
location_level_boss_final_event_agrade: dict[str, LocationData] = {
    LocationNames.loc_level_boss_devil_event_agrade: LocationData(None)
}
location_level_boss_final_event_dlc_chaliced: dict[str, LocationData] = {
    LocationNames.loc_level_boss_devil_event_dlc_chaliced: LocationData(None)
}
location_level_dlc_boss: dict[str, LocationData] = {
    LocationNames.loc_level_dlc_boss_oldman: LocationData(dlc_lid(21)),
    LocationNames.loc_level_dlc_boss_rumrunners: LocationData(dlc_lid(24)),
    LocationNames.loc_level_dlc_boss_snowcult: LocationData(dlc_lid(27)),
    LocationNames.loc_level_dlc_boss_airplane: LocationData(dlc_lid(30)),

    LocationNames.loc_level_dlc_boss_plane_cowboy: LocationData(dlc_lid(33)),
}
location_level_dlc_boss_final: dict[str, LocationData] = {
    LocationNames.loc_level_dlc_boss_saltbaker: LocationData(dlc_lid(36)),
}
location_level_dlc_boss_topgrade: dict[str, LocationData] = {
    LocationNames.loc_level_dlc_boss_oldman_topgrade: LocationData(dlc_lid(22)),
    LocationNames.loc_level_dlc_boss_rumrunners_topgrade: LocationData(dlc_lid(25)),
    LocationNames.loc_level_dlc_boss_snowcult_topgrade: LocationData(dlc_lid(28)),
    LocationNames.loc_level_dlc_boss_airplane_topgrade: LocationData(dlc_lid(31)),

    LocationNames.loc_level_dlc_boss_plane_cowboy_topgrade: LocationData(dlc_lid(34)),
}
location_level_dlc_boss_dlc_chaliced: dict[str, LocationData] = {
    LocationNames.loc_level_dlc_boss_oldman_dlc_chaliced: LocationData(dlc_lid(23)),
    LocationNames.loc_level_dlc_boss_rumrunners_dlc_chaliced: LocationData(dlc_lid(26)),
    LocationNames.loc_level_dlc_boss_snowcult_dlc_chaliced: LocationData(dlc_lid(29)),
    LocationNames.loc_level_dlc_boss_airplane_dlc_chaliced: LocationData(dlc_lid(32)),
    LocationNames.loc_level_dlc_boss_plane_cowboy_dlc_chaliced: LocationData(dlc_lid(35)),
}
location_level_dlc_boss_event_agrade: dict[str, LocationData] = {
    LocationNames.loc_level_dlc_boss_oldman_event_agrade: LocationData(None),
    LocationNames.loc_level_dlc_boss_rumrunners_event_agrade: LocationData(None),
    LocationNames.loc_level_dlc_boss_snowcult_event_agrade: LocationData(None),
    LocationNames.loc_level_dlc_boss_airplane_event_agrade: LocationData(None),
    LocationNames.loc_level_dlc_boss_plane_cowboy_event_agrade: LocationData(None),
}
location_level_dlc_boss_event_dlc_chaliced: dict[str, LocationData] = {
    LocationNames.loc_level_dlc_boss_oldman_event_dlc_chaliced: LocationData(None),
    LocationNames.loc_level_dlc_boss_rumrunners_event_dlc_chaliced: LocationData(None),
    LocationNames.loc_level_dlc_boss_snowcult_event_dlc_chaliced: LocationData(None),
    LocationNames.loc_level_dlc_boss_airplane_event_dlc_chaliced: LocationData(None),
    LocationNames.loc_level_dlc_boss_plane_cowboy_event_dlc_chaliced: LocationData(None),
}
location_level_dlc_boss_final_topgrade: dict[str, LocationData] = {
    LocationNames.loc_level_dlc_boss_saltbaker_topgrade: LocationData(dlc_lid(37)),
}
location_level_dlc_boss_final_dlc_chaliced= {
    LocationNames.loc_level_dlc_boss_saltbaker_dlc_chaliced: LocationData(dlc_lid(38)),
}
location_level_dlc_boss_final_event_agrade: dict[str, LocationData] = {
    LocationNames.loc_level_dlc_boss_saltbaker_event_agrade: LocationData(None),
}
location_level_dlc_boss_final_event_dlc_chaliced: dict[str, LocationData] = {
    LocationNames.loc_level_dlc_boss_saltbaker_event_dlc_chaliced: LocationData(None),
}

location_level_dicepalace: dict[str, LocationData] = {
    LocationNames.loc_level_dicepalace_boss1: LocationData(lid(41)),
    LocationNames.loc_level_dicepalace_boss2: LocationData(lid(42)),
    LocationNames.loc_level_dicepalace_boss3: LocationData(lid(43)),
    LocationNames.loc_level_dicepalace_boss4: LocationData(lid(44)),
    LocationNames.loc_level_dicepalace_boss5: LocationData(lid(45)),
    LocationNames.loc_level_dicepalace_boss6: LocationData(lid(46)),
    LocationNames.loc_level_dicepalace_boss7: LocationData(lid(47)),
    LocationNames.loc_level_dicepalace_boss8: LocationData(lid(48)),
    LocationNames.loc_level_dicepalace_boss9: LocationData(lid(49)),
}
location_level_dicepalace_dlc_chaliced: dict[str, LocationData] = {
    LocationNames.loc_level_dicepalace_boss1_dlc_chaliced: LocationData(dlc_lid(39)),
    LocationNames.loc_level_dicepalace_boss2_dlc_chaliced: LocationData(dlc_lid(40)),
    LocationNames.loc_level_dicepalace_boss3_dlc_chaliced: LocationData(dlc_lid(41)),
    LocationNames.loc_level_dicepalace_boss4_dlc_chaliced: LocationData(dlc_lid(42)),
    LocationNames.loc_level_dicepalace_boss5_dlc_chaliced: LocationData(dlc_lid(43)),
    LocationNames.loc_level_dicepalace_boss6_dlc_chaliced: LocationData(dlc_lid(44)),
    LocationNames.loc_level_dicepalace_boss7_dlc_chaliced: LocationData(dlc_lid(45)),
    LocationNames.loc_level_dicepalace_boss8_dlc_chaliced: LocationData(dlc_lid(46)),
    LocationNames.loc_level_dicepalace_boss9_dlc_chaliced: LocationData(dlc_lid(47)),
}

location_level_rungun: dict[str, LocationData] = {
    LocationNames.loc_level_rungun_forest: LocationData(lid(50)),
    LocationNames.loc_level_rungun_forest_coin1: LocationData(lid(53)),
    LocationNames.loc_level_rungun_forest_coin2: LocationData(lid(54)),
    LocationNames.loc_level_rungun_forest_coin3: LocationData(lid(55)),
    LocationNames.loc_level_rungun_forest_coin4: LocationData(lid(56)),
    LocationNames.loc_level_rungun_forest_coin5: LocationData(lid(57)),

    LocationNames.loc_level_rungun_tree: LocationData(lid(58)),
    LocationNames.loc_level_rungun_tree_coin1: LocationData(lid(61)),
    LocationNames.loc_level_rungun_tree_coin2: LocationData(lid(62)),
    LocationNames.loc_level_rungun_tree_coin3: LocationData(lid(63)),
    LocationNames.loc_level_rungun_tree_coin4: LocationData(lid(64)),
    LocationNames.loc_level_rungun_tree_coin5: LocationData(lid(65)),

    LocationNames.loc_level_rungun_circus: LocationData(lid(66)),
    LocationNames.loc_level_rungun_circus_coin1: LocationData(lid(69)),
    LocationNames.loc_level_rungun_circus_coin2: LocationData(lid(70)),
    LocationNames.loc_level_rungun_circus_coin3: LocationData(lid(71)),
    LocationNames.loc_level_rungun_circus_coin4: LocationData(lid(72)),
    LocationNames.loc_level_rungun_circus_coin5: LocationData(lid(73)),

    LocationNames.loc_level_rungun_funhouse: LocationData(lid(74)),
    LocationNames.loc_level_rungun_funhouse_coin1: LocationData(lid(77)),
    LocationNames.loc_level_rungun_funhouse_coin2: LocationData(lid(78)),
    LocationNames.loc_level_rungun_funhouse_coin3: LocationData(lid(79)),
    LocationNames.loc_level_rungun_funhouse_coin4: LocationData(lid(80)),
    LocationNames.loc_level_rungun_funhouse_coin5: LocationData(lid(81)),

    LocationNames.loc_level_rungun_harbour: LocationData(lid(82)),
    LocationNames.loc_level_rungun_harbour_coin1: LocationData(lid(85)),
    LocationNames.loc_level_rungun_harbour_coin2: LocationData(lid(86)),
    LocationNames.loc_level_rungun_harbour_coin3: LocationData(lid(87)),
    LocationNames.loc_level_rungun_harbour_coin4: LocationData(lid(88)),
    LocationNames.loc_level_rungun_harbour_coin5: LocationData(lid(89)),

    LocationNames.loc_level_rungun_mountain: LocationData(lid(90)),
    LocationNames.loc_level_rungun_mountain_coin1: LocationData(lid(93)),
    LocationNames.loc_level_rungun_mountain_coin2: LocationData(lid(94)),
    LocationNames.loc_level_rungun_mountain_coin3: LocationData(lid(95)),
    LocationNames.loc_level_rungun_mountain_coin4: LocationData(lid(96)),
    LocationNames.loc_level_rungun_mountain_coin5: LocationData(lid(97)),
}
location_level_rungun_agrade: dict[str, LocationData] = {
    LocationNames.loc_level_rungun_forest_agrade: LocationData(lid(51)),
    LocationNames.loc_level_rungun_tree_agrade: LocationData(lid(59)),
    LocationNames.loc_level_rungun_circus_agrade: LocationData(lid(67)),
    LocationNames.loc_level_rungun_funhouse_agrade: LocationData(lid(75)),
    LocationNames.loc_level_rungun_harbour_agrade: LocationData(lid(83)),
    LocationNames.loc_level_rungun_mountain_agrade: LocationData(lid(91)),
}
location_level_rungun_pacifist: dict[str, LocationData] = {
    LocationNames.loc_level_rungun_forest_pacifist: LocationData(lid(52)),
    LocationNames.loc_level_rungun_tree_pacifist: LocationData(lid(60)),
    LocationNames.loc_level_rungun_circus_pacifist: LocationData(lid(68)),
    LocationNames.loc_level_rungun_funhouse_pacifist: LocationData(lid(76)),
    LocationNames.loc_level_rungun_harbour_pacifist: LocationData(lid(84)),
    LocationNames.loc_level_rungun_mountain_pacifist: LocationData(lid(92)),
}
location_level_rungun_dlc_chaliced: dict[str, LocationData] = {
    LocationNames.loc_level_rungun_forest_dlc_chaliced: LocationData(dlc_lid(48)),
    LocationNames.loc_level_rungun_tree_dlc_chaliced: LocationData(dlc_lid(49)),
    LocationNames.loc_level_rungun_circus_dlc_chaliced: LocationData(dlc_lid(50)),
    LocationNames.loc_level_rungun_funhouse_dlc_chaliced: LocationData(dlc_lid(51)),
    LocationNames.loc_level_rungun_harbour_dlc_chaliced: LocationData(dlc_lid(52)),
    LocationNames.loc_level_rungun_mountain_dlc_chaliced: LocationData(dlc_lid(53)),
}
location_level_rungun_event_agrade: dict[str, LocationData] = {
    LocationNames.loc_level_rungun_forest_event_agrade: LocationData(None),
    LocationNames.loc_level_rungun_tree_event_agrade: LocationData(None),
    LocationNames.loc_level_rungun_circus_event_agrade: LocationData(None),
    LocationNames.loc_level_rungun_funhouse_event_agrade: LocationData(None),
    LocationNames.loc_level_rungun_harbour_event_agrade: LocationData(None),
    LocationNames.loc_level_rungun_mountain_event_agrade: LocationData(None),
}
location_level_rungun_event_pacifist: dict[str, LocationData] = {
    LocationNames.loc_level_rungun_forest_event_pacifist: LocationData(None),
    LocationNames.loc_level_rungun_tree_event_pacifist: LocationData(None),
    LocationNames.loc_level_rungun_circus_event_pacifist: LocationData(None),
    LocationNames.loc_level_rungun_funhouse_event_pacifist: LocationData(None),
    LocationNames.loc_level_rungun_harbour_event_pacifist: LocationData(None),
    LocationNames.loc_level_rungun_mountain_event_pacifist: LocationData(None),
}

location_level_mausoleum: dict[str, LocationData] = {
    LocationNames.loc_level_mausoleum_i: LocationData(lid(98)),
    LocationNames.loc_level_mausoleum_ii: LocationData(lid(99)),
    LocationNames.loc_level_mausoleum_iii: LocationData(lid(100)),
}

location_level_dlc_chesscastle: dict[str, LocationData] = {
    LocationNames.loc_level_dlc_chesscastle_pawn: LocationData(dlc_lid(54)),
    LocationNames.loc_level_dlc_chesscastle_knight: LocationData(dlc_lid(55)),
    LocationNames.loc_level_dlc_chesscastle_bishop: LocationData(dlc_lid(56)),
    LocationNames.loc_level_dlc_chesscastle_rook: LocationData(dlc_lid(57)),
    LocationNames.loc_level_dlc_chesscastle_queen: LocationData(dlc_lid(58)),
    LocationNames.loc_level_dlc_chesscastle_run: LocationData(dlc_lid(59)),
}
location_level_dlc_chesscastle_dlc_chaliced: dict[str, LocationData] = {
    LocationNames.loc_level_dlc_chesscastle_pawn_dlc_chaliced: LocationData(dlc_lid(60)),
    LocationNames.loc_level_dlc_chesscastle_knight_dlc_chaliced: LocationData(dlc_lid(61)),
    LocationNames.loc_level_dlc_chesscastle_bishop_dlc_chaliced: LocationData(dlc_lid(62)),
    LocationNames.loc_level_dlc_chesscastle_rook_dlc_chaliced: LocationData(dlc_lid(63)),
    LocationNames.loc_level_dlc_chesscastle_queen_dlc_chaliced: LocationData(dlc_lid(64)),
    LocationNames.loc_level_dlc_chesscastle_run_dlc_chaliced: LocationData(dlc_lid(65)),
}

location_level_dlc_special: dict[str, LocationData] = {
    #LocationNames.loc_level_dlc_graveyard: LocationData(dlc_lid(66)),
}

# Shop Locations
location_shop: dict[str, LocationData] = {
    LocationNames.loc_shop_weapon1: LocationData(lid(101)),
    LocationNames.loc_shop_weapon2: LocationData(lid(102)),
    LocationNames.loc_shop_weapon3: LocationData(lid(103)),
    LocationNames.loc_shop_weapon4: LocationData(lid(104)),
    LocationNames.loc_shop_weapon5: LocationData(lid(105)),
    LocationNames.loc_shop_charm1: LocationData(lid(106)),
    LocationNames.loc_shop_charm2: LocationData(lid(107)),
    LocationNames.loc_shop_charm3: LocationData(lid(108)),
    LocationNames.loc_shop_charm4: LocationData(lid(109)),
    LocationNames.loc_shop_charm5: LocationData(lid(110)),
    LocationNames.loc_shop_charm6: LocationData(lid(111)),
}
location_shop_dlc: dict[str, LocationData] = {
    LocationNames.loc_shop_dlc_weapon6: LocationData(dlc_lid(67)),
    LocationNames.loc_shop_dlc_weapon7: LocationData(dlc_lid(68)),
    LocationNames.loc_shop_dlc_weapon8: LocationData(dlc_lid(69)),
    LocationNames.loc_shop_dlc_charm7: LocationData(dlc_lid(70)),
    LocationNames.loc_shop_dlc_charm8: LocationData(dlc_lid(71)),
}

# World Locations
location_world: dict[str, LocationData] = {
    LocationNames.loc_npc_mac: LocationData(lid(112)),
    LocationNames.loc_npc_canteen: LocationData(lid(113)),
    LocationNames.loc_coin_isle1_secret: LocationData(lid(114)),
    LocationNames.loc_coin_isle2_secret: LocationData(lid(115)),
    LocationNames.loc_coin_isle3_secret: LocationData(lid(116)),
    LocationNames.loc_coin_isleh_secret: LocationData(lid(117)),
}
location_world_event: dict[str, LocationData] = {
    LocationNames.loc_event_isle1_secret_prereq1: LocationData(None),
    LocationNames.loc_event_isle1_secret_prereq2: LocationData(None),
    LocationNames.loc_event_isle1_secret_prereq3: LocationData(None),
    LocationNames.loc_event_isle1_secret_prereq4: LocationData(None),
    LocationNames.loc_event_isle1_secret_prereq5: LocationData(None),
}
location_world_quest: dict[str, LocationData] = {
    LocationNames.loc_quest_buster: LocationData(lid(118)),
    LocationNames.loc_quest_ginger: LocationData(lid(119)),
    LocationNames.loc_quest_4mel: LocationData(lid(120)),
    LocationNames.loc_quest_lucien: LocationData(lid(121)),
    LocationNames.loc_quest_pacifist: LocationData(lid(122)),
    LocationNames.loc_quest_silverworth: LocationData(lid(123)),
    LocationNames.loc_quest_music: LocationData(lid(124)),
}
location_level_boss_secret: dict[str, LocationData] = {
    LocationNames.loc_level_boss_veggies_secret: LocationData(lid(125)),
    LocationNames.loc_level_boss_plane_genie_secret: LocationData(lid(126)),
    LocationNames.loc_level_boss_sallystageplay_secret: LocationData(lid(127)),
}
location_level_dlc_boss_secret: dict[str, LocationData] = {
    LocationNames.loc_level_dlc_boss_airplane_secret: LocationData(dlc_lid(77)),
}
location_dlc_world: dict[str, LocationData] = {
    LocationNames.loc_dlc_npc_newscat: LocationData(dlc_lid(72)),
    LocationNames.loc_dlc_coin_isle4_secret: LocationData(dlc_lid(73)),
}
location_dlc_world_event: dict[str, LocationData] = {
    LocationNames.loc_event_dlc_boatarrival: LocationData(None),
}
location_dlc_world_quest: dict[str, LocationData] = {
    LocationNames.loc_dlc_quest_cactusgirl: LocationData(dlc_lid(74)),
}

# Special Locations
location_special: dict[str, LocationData] = {
    LocationNames.loc_event_start_weapon: LocationData(None),
    LocationNames.loc_event_start_weapon_ex: LocationData(None),
    LocationNames.loc_event_isle2_shortcut: LocationData(None),
    LocationNames.loc_event_quest_4mel_4th: LocationData(None),
    LocationNames.loc_event_quest_ludwig: LocationData(None),
    #LocationNames.loc_event_quest_wolfgang: LocationData(None),
    #LocationNames.loc_event_music: LocationData(None),
}
location_dlc_special: dict[str, LocationData] = {
    LocationNames.loc_dlc_cookie: LocationData(dlc_lid(75)),
    LocationNames.loc_event_mausoleum: LocationData(None),
    LocationNames.loc_event_dlc_cookie: LocationData(None),
    #LocationNames.loc_dlc_curse_complete: LocationData(dlc_lid(76)),
}

# Goal Locations
location_goal: dict[str, LocationData] = {
    LocationNames.loc_event_goal_devil: LocationData(None),
}
location_dlc_goal: dict[str, LocationData] = {
    LocationNames.loc_event_dlc_goal_saltbaker: LocationData(None),
}

locations_base: dict[str, LocationData] = {
    **location_level_tutorial,
    **location_level_boss,
    #**location_level_boss_final,
    **location_level_rungun,
    **location_level_mausoleum,
    **location_shop,
    #**location_shop_event,
    **location_world,
    **location_world_event,
}
locations_topgrade: dict[str, LocationData] = {
    **location_level_boss_topgrade,
    #**location_level_boss_final_topgrade,
    **location_level_rungun_agrade,
    **location_level_rungun_pacifist,
}
locations_event_agrade: dict[str, LocationData] = {
    **location_level_boss_event_agrade,
    #**location_level_boss_final_event_agrade,
    **location_level_rungun_event_agrade,
}
locations_dlc: dict[str, LocationData] = {
    **location_level_dlc_boss,
    #**location_level_dlc_boss_final,
    **location_level_dlc_chesscastle,
    **location_level_dlc_special,
    **location_shop_dlc,
    #**location_shop_dlc_event,
    **location_dlc_world,
    **location_dlc_world_event,
}
locations_dlc_boss_chaliced: dict[str, LocationData] = {
    **location_level_boss_dlc_chaliced,
    #**location_level_boss_final_dlc_chaliced,
    **location_level_dlc_boss_dlc_chaliced,
    #**location_level_dlc_boss_final_dlc_chaliced,
}
locations_dlc_topgrade: dict[str, LocationData] = {
    **location_level_dlc_boss_topgrade,
    #**location_level_dlc_boss_final_topgrade,
}
locations_dlc_event_boss_chaliced: dict[str, LocationData] = {
    **location_level_boss_event_dlc_chaliced,
    **location_level_dlc_boss_event_dlc_chaliced,
}
locations_dlc_event_boss_final_chaliced: dict[str, LocationData] = {
    **location_level_boss_final_event_dlc_chaliced,
    **location_level_dlc_boss_final_event_dlc_chaliced,
}

locations_all: dict[str, LocationData] = {
    **locations_base,
    **location_level_boss_final, # Final
    **location_level_boss_secret,
    **locations_topgrade,
    **location_level_boss_final_topgrade,  # Final
    **locations_event_agrade,
    **location_level_rungun_event_pacifist,
    **location_world_quest,
    **location_special,
    **location_goal,
    **locations_dlc,
    **location_level_dlc_tutorial,
    **location_level_dlc_boss_final, # Final
    **location_level_dlc_boss_secret,
    **locations_dlc_topgrade,
    **location_level_dlc_boss_final_topgrade, # Final
    **locations_dlc_boss_chaliced,
    **location_level_rungun_dlc_chaliced,
    **location_level_boss_final_dlc_chaliced, # Final
    **location_level_dlc_boss_final_dlc_chaliced, # Final
    **location_level_dicepalace_dlc_chaliced,
    **location_level_dlc_chesscastle_dlc_chaliced,
    **locations_dlc_event_boss_chaliced,
    **location_dlc_world_quest,
    **location_dlc_special,
    **location_dlc_goal,
    **location_level_dicepalace,
}

name_to_id = {name: data.id for name, data in locations_all.items() if data.id}
