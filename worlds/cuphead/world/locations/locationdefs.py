### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from ..names import locationnames
from .locationbase import LocationData

# Locations
# Next lids: 30003, 10042002
# Level Locations
location_level_tutorial: dict[str, LocationData] = {
    locationnames.loc_level_tutorial: LocationData(1000),
    locationnames.loc_level_tutorial_coin: LocationData(1001),
    #locationnames.loc_level_plane_tutorial: LocationData(1002),
}
location_level_dlc_tutorial: dict[str, LocationData] = {
    locationnames.loc_level_dlc_tutorial: LocationData(10001000),
    locationnames.loc_level_dlc_tutorial_coin: LocationData(10001001),
}

location_level_boss: dict[str, LocationData] = {
    locationnames.loc_level_boss_veggies: LocationData(2000),
    locationnames.loc_level_boss_slime: LocationData(2001),
    locationnames.loc_level_boss_frogs: LocationData(2002),
    locationnames.loc_level_boss_flower: LocationData(2003),
    locationnames.loc_level_boss_baroness: LocationData(2004),
    locationnames.loc_level_boss_clown: LocationData(2005),
    locationnames.loc_level_boss_dragon: LocationData(2006),
    locationnames.loc_level_boss_bee: LocationData(2007),
    locationnames.loc_level_boss_pirate: LocationData(2008),
    locationnames.loc_level_boss_mouse: LocationData(2009),
    locationnames.loc_level_boss_sallystageplay: LocationData(2010),
    locationnames.loc_level_boss_train: LocationData(2011),
    locationnames.loc_level_boss_plane_blimp: LocationData(2013),
    locationnames.loc_level_boss_plane_genie: LocationData(2014),
    locationnames.loc_level_boss_plane_bird: LocationData(2015),
    locationnames.loc_level_boss_plane_mermaid: LocationData(2016),
    locationnames.loc_level_boss_plane_robot: LocationData(2017),
}
location_level_boss_kingdice: dict[str, LocationData] = {
    locationnames.loc_level_boss_kingdice: LocationData(2012),
}
location_level_boss_final: dict[str, LocationData] = {
    locationnames.loc_level_boss_devil: LocationData(4000),
}
location_level_boss_topgrade: dict[str, LocationData] = {
    locationnames.loc_level_boss_veggies_topgrade: LocationData(6000),
    locationnames.loc_level_boss_slime_topgrade: LocationData(6001),
    locationnames.loc_level_boss_frogs_topgrade: LocationData(6002),
    locationnames.loc_level_boss_flower_topgrade: LocationData(6003),
    locationnames.loc_level_boss_baroness_topgrade: LocationData(6004),
    locationnames.loc_level_boss_clown_topgrade: LocationData(6005),
    locationnames.loc_level_boss_dragon_topgrade: LocationData(6006),
    locationnames.loc_level_boss_bee_topgrade: LocationData(6007),
    locationnames.loc_level_boss_pirate_topgrade: LocationData(6008),
    locationnames.loc_level_boss_mouse_topgrade: LocationData(6009),
    locationnames.loc_level_boss_sallystageplay_topgrade: LocationData(6010),
    locationnames.loc_level_boss_train_topgrade: LocationData(6011),
    locationnames.loc_level_boss_plane_blimp_topgrade: LocationData(6013),
    locationnames.loc_level_boss_plane_genie_topgrade: LocationData(6014),
    locationnames.loc_level_boss_plane_bird_topgrade: LocationData(6015),
    locationnames.loc_level_boss_plane_mermaid_topgrade: LocationData(6016),
    locationnames.loc_level_boss_plane_robot_topgrade: LocationData(6017),
}
location_level_boss_kingdice_topgrade: dict[str, LocationData] = {
    locationnames.loc_level_boss_kingdice_topgrade: LocationData(6012),
}
location_level_boss_dlc_chaliced: dict[str, LocationData] = {
    locationnames.loc_level_boss_veggies_dlc_chaliced: LocationData(10002000),
    locationnames.loc_level_boss_slime_dlc_chaliced: LocationData(10002001),
    locationnames.loc_level_boss_frogs_dlc_chaliced: LocationData(10002002),
    locationnames.loc_level_boss_flower_dlc_chaliced: LocationData(10002003),
    locationnames.loc_level_boss_baroness_dlc_chaliced: LocationData(10002004),
    locationnames.loc_level_boss_clown_dlc_chaliced: LocationData(10002005),
    locationnames.loc_level_boss_dragon_dlc_chaliced: LocationData(10002006),
    locationnames.loc_level_boss_bee_dlc_chaliced: LocationData(10002007),
    locationnames.loc_level_boss_pirate_dlc_chaliced: LocationData(10002008),
    locationnames.loc_level_boss_mouse_dlc_chaliced: LocationData(10002009),
    locationnames.loc_level_boss_sallystageplay_dlc_chaliced: LocationData(10002010),
    locationnames.loc_level_boss_train_dlc_chaliced: LocationData(10002011),
    locationnames.loc_level_boss_plane_blimp_dlc_chaliced: LocationData(10002013),
    locationnames.loc_level_boss_plane_genie_dlc_chaliced: LocationData(10002014),
    locationnames.loc_level_boss_plane_bird_dlc_chaliced: LocationData(10002015),
    locationnames.loc_level_boss_plane_mermaid_dlc_chaliced: LocationData(10002016),
    locationnames.loc_level_boss_plane_robot_dlc_chaliced: LocationData(10002017),
}
location_level_boss_kingdice_dlc_chaliced: dict[str, LocationData] = {
    locationnames.loc_level_boss_kingdice_dlc_chaliced: LocationData(10002012),
}
location_level_boss_phases: dict[str, LocationData] = {
    locationnames.loc_level_boss_veggies_phase1: LocationData(8000),
    locationnames.loc_level_boss_veggies_phase2: LocationData(8002),
    locationnames.loc_level_boss_veggies_phase2s: LocationData(8004),
    locationnames.loc_level_boss_veggies_phase3: LocationData(8006),
    locationnames.loc_level_boss_veggies_phase3s: LocationData(8008),

    locationnames.loc_level_boss_slime_phase1: LocationData(8010),
    locationnames.loc_level_boss_slime_phase2: LocationData(8012),
    locationnames.loc_level_boss_slime_phase3: LocationData(8014),

    locationnames.loc_level_boss_frogs_phase1: LocationData(8016),
    locationnames.loc_level_boss_frogs_phase2: LocationData(8018),
    locationnames.loc_level_boss_frogs_phase3: LocationData(8020),

    locationnames.loc_level_boss_flower_phase1: LocationData(8022),
    locationnames.loc_level_boss_flower_phase2: LocationData(8024),
    locationnames.loc_level_boss_flower_phase3: LocationData(8026),
    locationnames.loc_level_boss_flower_phase4: LocationData(8028),

    locationnames.loc_level_boss_baroness_phase1: LocationData(8030),
    locationnames.loc_level_boss_baroness_phase2: LocationData(8032),
    locationnames.loc_level_boss_baroness_phase3: LocationData(8034),
    locationnames.loc_level_boss_baroness_phase4: LocationData(8036),

    locationnames.loc_level_boss_clown_phase1: LocationData(8038),
    locationnames.loc_level_boss_clown_phase2: LocationData(8040),
    locationnames.loc_level_boss_clown_phase3: LocationData(8042),
    locationnames.loc_level_boss_clown_phase4: LocationData(8044),

    locationnames.loc_level_boss_dragon_phase1: LocationData(8046),
    locationnames.loc_level_boss_dragon_phase2: LocationData(8048),
    locationnames.loc_level_boss_dragon_phase3: LocationData(8050),
    locationnames.loc_level_boss_dragon_phase4: LocationData(8052),

    locationnames.loc_level_boss_bee_phase1: LocationData(8054),
    locationnames.loc_level_boss_bee_phase2: LocationData(8056),
    locationnames.loc_level_boss_bee_phase3: LocationData(8058),

    locationnames.loc_level_boss_pirate_phase1: LocationData(8060),
    locationnames.loc_level_boss_pirate_phase2: LocationData(8062),
    locationnames.loc_level_boss_pirate_phase3: LocationData(8064),
    locationnames.loc_level_boss_pirate_phase4: LocationData(8066),

    locationnames.loc_level_boss_mouse_phase1: LocationData(8068),
    locationnames.loc_level_boss_mouse_phase2: LocationData(8070),
    locationnames.loc_level_boss_mouse_phase3: LocationData(8072),

    locationnames.loc_level_boss_sallystageplay_phase1: LocationData(8074),
    locationnames.loc_level_boss_sallystageplay_phase1s: LocationData(8076),
    locationnames.loc_level_boss_sallystageplay_phase2: LocationData(8078),
    locationnames.loc_level_boss_sallystageplay_phase2s: LocationData(8080),
    locationnames.loc_level_boss_sallystageplay_phase3: LocationData(8082),
    locationnames.loc_level_boss_sallystageplay_phase3s: LocationData(8084),
    locationnames.loc_level_boss_sallystageplay_phase4: LocationData(8086),
    locationnames.loc_level_boss_sallystageplay_phase4s: LocationData(8088),

    locationnames.loc_level_boss_train_phase1: LocationData(8090),
    locationnames.loc_level_boss_train_phase2: LocationData(8092),
    locationnames.loc_level_boss_train_phase3: LocationData(8094),
    locationnames.loc_level_boss_train_phase4: LocationData(8096),

    locationnames.loc_level_boss_plane_blimp_phase1: LocationData(8102),
    locationnames.loc_level_boss_plane_blimp_phase2: LocationData(8104),
    locationnames.loc_level_boss_plane_blimp_phase3: LocationData(8106),
    locationnames.loc_level_boss_plane_blimp_phase4: LocationData(8108),
    locationnames.loc_level_boss_plane_blimp_phase5: LocationData(8110),
    locationnames.loc_level_boss_plane_blimp_phase6: LocationData(8112),

    locationnames.loc_level_boss_plane_genie_phase1: LocationData(8114),
    locationnames.loc_level_boss_plane_genie_phase2: LocationData(8116),
    locationnames.loc_level_boss_plane_genie_phase3: LocationData(8118),
    locationnames.loc_level_boss_plane_genie_phase4: LocationData(8120),
    locationnames.loc_level_boss_plane_genie_phase5: LocationData(8122),

    locationnames.loc_level_boss_plane_bird_phase1: LocationData(8124),
    locationnames.loc_level_boss_plane_bird_phase2: LocationData(8126),
    locationnames.loc_level_boss_plane_bird_phase3: LocationData(8128),
    locationnames.loc_level_boss_plane_bird_phase4: LocationData(8130),
    locationnames.loc_level_boss_plane_bird_phase5: LocationData(8132),

    locationnames.loc_level_boss_plane_mermaid_phase1: LocationData(8134),
    locationnames.loc_level_boss_plane_mermaid_phase2: LocationData(8136),
    locationnames.loc_level_boss_plane_mermaid_phase3: LocationData(8138),

    locationnames.loc_level_boss_plane_robot_phase1: LocationData(8140),
    locationnames.loc_level_boss_plane_robot_phase2: LocationData(8142),
    locationnames.loc_level_boss_plane_robot_phase3: LocationData(8144),
}
location_level_boss_kingdice_phases: dict[str, LocationData] = {
    locationnames.loc_level_boss_kingdice_phase1: LocationData(8098),
    locationnames.loc_level_boss_kingdice_phase2: LocationData(8100),
}
location_level_boss_event_agrade: dict[str, LocationData] = {
    locationnames.loc_level_boss_veggies_event_agrade: LocationData(None),
    locationnames.loc_level_boss_slime_event_agrade: LocationData(None),
    locationnames.loc_level_boss_frogs_event_agrade: LocationData(None),
    locationnames.loc_level_boss_flower_event_agrade: LocationData(None),
    locationnames.loc_level_boss_baroness_event_agrade: LocationData(None),
    locationnames.loc_level_boss_clown_event_agrade: LocationData(None),
    locationnames.loc_level_boss_dragon_event_agrade: LocationData(None),
    locationnames.loc_level_boss_bee_event_agrade: LocationData(None),
    locationnames.loc_level_boss_pirate_event_agrade: LocationData(None),
    locationnames.loc_level_boss_mouse_event_agrade: LocationData(None),
    locationnames.loc_level_boss_sallystageplay_event_agrade: LocationData(None),
    locationnames.loc_level_boss_train_event_agrade: LocationData(None),
    locationnames.loc_level_boss_plane_blimp_event_agrade: LocationData(None),
    locationnames.loc_level_boss_plane_genie_event_agrade: LocationData(None),
    locationnames.loc_level_boss_plane_bird_event_agrade: LocationData(None),
    locationnames.loc_level_boss_plane_mermaid_event_agrade: LocationData(None),
    locationnames.loc_level_boss_plane_robot_event_agrade: LocationData(None),
}
location_level_boss_kingdice_event_agrade: dict[str, LocationData] = {
    locationnames.loc_level_boss_kingdice_event_agrade: LocationData(None),
}
location_level_boss_event_dlc_chaliced: dict[str, LocationData] = {
    locationnames.loc_level_boss_veggies_event_dlc_chaliced: LocationData(None),
    locationnames.loc_level_boss_slime_event_dlc_chaliced: LocationData(None),
    locationnames.loc_level_boss_frogs_event_dlc_chaliced: LocationData(None),
    locationnames.loc_level_boss_flower_event_dlc_chaliced: LocationData(None),
    locationnames.loc_level_boss_baroness_event_dlc_chaliced: LocationData(None),
    locationnames.loc_level_boss_clown_event_dlc_chaliced: LocationData(None),
    locationnames.loc_level_boss_dragon_event_dlc_chaliced: LocationData(None),
    locationnames.loc_level_boss_bee_event_dlc_chaliced: LocationData(None),
    locationnames.loc_level_boss_pirate_event_dlc_chaliced: LocationData(None),
    locationnames.loc_level_boss_mouse_event_dlc_chaliced: LocationData(None),
    locationnames.loc_level_boss_sallystageplay_event_dlc_chaliced: LocationData(None),
    locationnames.loc_level_boss_train_event_dlc_chaliced: LocationData(None),
    locationnames.loc_level_boss_plane_blimp_event_dlc_chaliced: LocationData(None),
    locationnames.loc_level_boss_plane_genie_event_dlc_chaliced: LocationData(None),
    locationnames.loc_level_boss_plane_bird_event_dlc_chaliced: LocationData(None),
    locationnames.loc_level_boss_plane_mermaid_event_dlc_chaliced: LocationData(None),
    locationnames.loc_level_boss_plane_robot_event_dlc_chaliced: LocationData(None),
}
location_level_boss_kingdice_event_dlc_chaliced: dict[str, LocationData] = {
    locationnames.loc_level_boss_kingdice_event_dlc_chaliced: LocationData(None),
}
location_level_boss_final_topgrade: dict[str, LocationData] = {
    locationnames.loc_level_boss_devil_topgrade: LocationData(10000)
}
location_level_boss_final_dlc_chaliced: dict[str, LocationData] = {
    locationnames.loc_level_boss_devil_dlc_chaliced: LocationData(10004000)
}
location_level_boss_final_phases: dict[str, LocationData] = {
    locationnames.loc_level_boss_devil_phase1: LocationData(12000),
    locationnames.loc_level_boss_devil_phase2: LocationData(12002),
    locationnames.loc_level_boss_devil_phase3: LocationData(12004),
    locationnames.loc_level_boss_devil_phase4: LocationData(12006),
}
location_level_boss_final_event_agrade: dict[str, LocationData] = {
    locationnames.loc_level_boss_devil_event_agrade: LocationData(None)
}
location_level_boss_final_event_dlc_chaliced: dict[str, LocationData] = {
    locationnames.loc_level_boss_devil_event_dlc_chaliced: LocationData(None)
}
location_level_dlc_boss: dict[str, LocationData] = {
    locationnames.loc_level_dlc_boss_oldman: LocationData(10006000),
    locationnames.loc_level_dlc_boss_rumrunners: LocationData(10006001),
    locationnames.loc_level_dlc_boss_snowcult: LocationData(10006002),
    locationnames.loc_level_dlc_boss_airplane: LocationData(10006003),

    locationnames.loc_level_dlc_boss_plane_cowboy: LocationData(10006004),
}
location_level_dlc_boss_final: dict[str, LocationData] = {
    locationnames.loc_level_dlc_boss_saltbaker: LocationData(10008000),
}
location_level_dlc_boss_topgrade: dict[str, LocationData] = {
    locationnames.loc_level_dlc_boss_oldman_topgrade: LocationData(10010000),
    locationnames.loc_level_dlc_boss_rumrunners_topgrade: LocationData(10010001),
    locationnames.loc_level_dlc_boss_snowcult_topgrade: LocationData(10010002),
    locationnames.loc_level_dlc_boss_airplane_topgrade: LocationData(10010003),

    locationnames.loc_level_dlc_boss_plane_cowboy_topgrade: LocationData(10010004),
}
location_level_dlc_boss_dlc_chaliced: dict[str, LocationData] = {
    locationnames.loc_level_dlc_boss_oldman_dlc_chaliced: LocationData(10012000),
    locationnames.loc_level_dlc_boss_rumrunners_dlc_chaliced: LocationData(10012001),
    locationnames.loc_level_dlc_boss_snowcult_dlc_chaliced: LocationData(10012002),
    locationnames.loc_level_dlc_boss_airplane_dlc_chaliced: LocationData(10012003),

    locationnames.loc_level_dlc_boss_plane_cowboy_dlc_chaliced: LocationData(10012004),
}
location_level_dlc_boss_phases: dict[str, LocationData] = {
    locationnames.loc_level_dlc_boss_oldman_phase1: LocationData(10014000),
    locationnames.loc_level_dlc_boss_oldman_phase2: LocationData(10014002),
    locationnames.loc_level_dlc_boss_oldman_phase3: LocationData(10014004),

    locationnames.loc_level_dlc_boss_rumrunners_phase1: LocationData(10014006),
    locationnames.loc_level_dlc_boss_rumrunners_phase2: LocationData(10014008),
    locationnames.loc_level_dlc_boss_rumrunners_phase3: LocationData(10014010),
    locationnames.loc_level_dlc_boss_rumrunners_phase4: LocationData(10014012),

    locationnames.loc_level_dlc_boss_snowcult_phase1: LocationData(10014014),
    locationnames.loc_level_dlc_boss_snowcult_phase2: LocationData(10014016),
    locationnames.loc_level_dlc_boss_snowcult_phase3: LocationData(10014018),

    locationnames.loc_level_dlc_boss_airplane_phase1: LocationData(10014020),
    locationnames.loc_level_dlc_boss_airplane_phase2: LocationData(10014022),
    locationnames.loc_level_dlc_boss_airplane_phase2s: LocationData(10014024),
    locationnames.loc_level_dlc_boss_airplane_phase3: LocationData(10014026),
    locationnames.loc_level_dlc_boss_airplane_phase3s: LocationData(10014028),

    locationnames.loc_level_dlc_boss_plane_cowboy_phase1: LocationData(10014030),
    locationnames.loc_level_dlc_boss_plane_cowboy_phase2: LocationData(10014032),
    locationnames.loc_level_dlc_boss_plane_cowboy_phase3: LocationData(10014034),
    locationnames.loc_level_dlc_boss_plane_cowboy_phase4: LocationData(10014036),
}
location_level_dlc_boss_event_agrade: dict[str, LocationData] = {
    locationnames.loc_level_dlc_boss_oldman_event_agrade: LocationData(None),
    locationnames.loc_level_dlc_boss_rumrunners_event_agrade: LocationData(None),
    locationnames.loc_level_dlc_boss_snowcult_event_agrade: LocationData(None),
    locationnames.loc_level_dlc_boss_airplane_event_agrade: LocationData(None),
    locationnames.loc_level_dlc_boss_plane_cowboy_event_agrade: LocationData(None),
}
location_level_dlc_boss_event_dlc_chaliced: dict[str, LocationData] = {
    locationnames.loc_level_dlc_boss_oldman_event_dlc_chaliced: LocationData(None),
    locationnames.loc_level_dlc_boss_rumrunners_event_dlc_chaliced: LocationData(None),
    locationnames.loc_level_dlc_boss_snowcult_event_dlc_chaliced: LocationData(None),
    locationnames.loc_level_dlc_boss_airplane_event_dlc_chaliced: LocationData(None),
    locationnames.loc_level_dlc_boss_plane_cowboy_event_dlc_chaliced: LocationData(None),
}
location_level_dlc_boss_final_topgrade: dict[str, LocationData] = {
    locationnames.loc_level_dlc_boss_saltbaker_topgrade: LocationData(10016000),
}
location_level_dlc_boss_final_dlc_chaliced: dict[str, LocationData] = {
    locationnames.loc_level_dlc_boss_saltbaker_dlc_chaliced: LocationData(10018000),
}
location_level_dlc_boss_final_phases: dict[str, LocationData] = {
    locationnames.loc_level_dlc_boss_saltbaker_phase1: LocationData(10020000),
    locationnames.loc_level_dlc_boss_saltbaker_phase2: LocationData(10020002),
    locationnames.loc_level_dlc_boss_saltbaker_phase3: LocationData(10020004),
    locationnames.loc_level_dlc_boss_saltbaker_phase4: LocationData(10020006),
}
location_level_dlc_boss_final_event_agrade: dict[str, LocationData] = {
    locationnames.loc_level_dlc_boss_saltbaker_event_agrade: LocationData(None),
}
location_level_dlc_boss_final_event_dlc_chaliced: dict[str, LocationData] = {
    locationnames.loc_level_dlc_boss_saltbaker_event_dlc_chaliced: LocationData(None),
}

location_level_dicepalace: dict[str, LocationData] = {
    locationnames.loc_level_dicepalace_boss1: LocationData(14000),
    locationnames.loc_level_dicepalace_boss2: LocationData(14001),
    locationnames.loc_level_dicepalace_boss3: LocationData(14002),
    locationnames.loc_level_dicepalace_boss4: LocationData(14003),
    locationnames.loc_level_dicepalace_boss5: LocationData(14004),
    locationnames.loc_level_dicepalace_boss6: LocationData(14005),
    locationnames.loc_level_dicepalace_boss7: LocationData(14006),
    locationnames.loc_level_dicepalace_boss8: LocationData(14007),
    locationnames.loc_level_dicepalace_boss9: LocationData(14008),
}
location_level_dicepalace_dlc_chaliced: dict[str, LocationData] = {
    locationnames.loc_level_dicepalace_boss1_dlc_chaliced: LocationData(10022000),
    locationnames.loc_level_dicepalace_boss2_dlc_chaliced: LocationData(10022001),
    locationnames.loc_level_dicepalace_boss3_dlc_chaliced: LocationData(10022002),
    locationnames.loc_level_dicepalace_boss4_dlc_chaliced: LocationData(10022003),
    locationnames.loc_level_dicepalace_boss5_dlc_chaliced: LocationData(10022004),
    locationnames.loc_level_dicepalace_boss6_dlc_chaliced: LocationData(10022005),
    locationnames.loc_level_dicepalace_boss7_dlc_chaliced: LocationData(10022006),
    locationnames.loc_level_dicepalace_boss8_dlc_chaliced: LocationData(10022007),
    locationnames.loc_level_dicepalace_boss9_dlc_chaliced: LocationData(10022008),
}

location_level_rungun: dict[str, LocationData] = {
    locationnames.loc_level_rungun_forest: LocationData(16000),
    locationnames.loc_level_rungun_forest_coin1: LocationData(16001),
    locationnames.loc_level_rungun_forest_coin2: LocationData(16002),
    locationnames.loc_level_rungun_forest_coin3: LocationData(16003),
    locationnames.loc_level_rungun_forest_coin4: LocationData(16004),
    locationnames.loc_level_rungun_forest_coin5: LocationData(16005),

    locationnames.loc_level_rungun_tree: LocationData(16006),
    locationnames.loc_level_rungun_tree_coin1: LocationData(16007),
    locationnames.loc_level_rungun_tree_coin2: LocationData(16008),
    locationnames.loc_level_rungun_tree_coin3: LocationData(16009),
    locationnames.loc_level_rungun_tree_coin4: LocationData(16010),
    locationnames.loc_level_rungun_tree_coin5: LocationData(16011),

    locationnames.loc_level_rungun_circus: LocationData(16012),
    locationnames.loc_level_rungun_circus_coin1: LocationData(16013),
    locationnames.loc_level_rungun_circus_coin2: LocationData(16014),
    locationnames.loc_level_rungun_circus_coin3: LocationData(16015),
    locationnames.loc_level_rungun_circus_coin4: LocationData(16016),
    locationnames.loc_level_rungun_circus_coin5: LocationData(16017),

    locationnames.loc_level_rungun_funhouse: LocationData(16018),
    locationnames.loc_level_rungun_funhouse_coin1: LocationData(16019),
    locationnames.loc_level_rungun_funhouse_coin2: LocationData(16020),
    locationnames.loc_level_rungun_funhouse_coin3: LocationData(16021),
    locationnames.loc_level_rungun_funhouse_coin4: LocationData(16022),
    locationnames.loc_level_rungun_funhouse_coin5: LocationData(16023),

    locationnames.loc_level_rungun_harbour: LocationData(16024),
    locationnames.loc_level_rungun_harbour_coin1: LocationData(16025),
    locationnames.loc_level_rungun_harbour_coin2: LocationData(16026),
    locationnames.loc_level_rungun_harbour_coin3: LocationData(16027),
    locationnames.loc_level_rungun_harbour_coin4: LocationData(16028),
    locationnames.loc_level_rungun_harbour_coin5: LocationData(16029),

    locationnames.loc_level_rungun_mountain: LocationData(16030),
    locationnames.loc_level_rungun_mountain_coin1: LocationData(16031),
    locationnames.loc_level_rungun_mountain_coin2: LocationData(16032),
    locationnames.loc_level_rungun_mountain_coin3: LocationData(16033),
    locationnames.loc_level_rungun_mountain_coin4: LocationData(16034),
    locationnames.loc_level_rungun_mountain_coin5: LocationData(16035),
}
location_level_rungun_agrade: dict[str, LocationData] = {
    locationnames.loc_level_rungun_forest_agrade: LocationData(18000),
    locationnames.loc_level_rungun_tree_agrade: LocationData(18001),
    locationnames.loc_level_rungun_circus_agrade: LocationData(18002),
    locationnames.loc_level_rungun_funhouse_agrade: LocationData(18003),
    locationnames.loc_level_rungun_harbour_agrade: LocationData(18004),
    locationnames.loc_level_rungun_mountain_agrade: LocationData(18005),
}
location_level_rungun_pacifist: dict[str, LocationData] = {
    locationnames.loc_level_rungun_forest_pacifist: LocationData(20000),
    locationnames.loc_level_rungun_tree_pacifist: LocationData(20001),
    locationnames.loc_level_rungun_circus_pacifist: LocationData(20002),
    locationnames.loc_level_rungun_funhouse_pacifist: LocationData(20003),
    locationnames.loc_level_rungun_harbour_pacifist: LocationData(20004),
    locationnames.loc_level_rungun_mountain_pacifist: LocationData(20005),
}
location_level_rungun_dlc_chaliced: dict[str, LocationData] = {
    locationnames.loc_level_rungun_forest_dlc_chaliced: LocationData(10024000),
    locationnames.loc_level_rungun_tree_dlc_chaliced: LocationData(10024001),
    locationnames.loc_level_rungun_circus_dlc_chaliced: LocationData(10024002),
    locationnames.loc_level_rungun_funhouse_dlc_chaliced: LocationData(10024003),
    locationnames.loc_level_rungun_harbour_dlc_chaliced: LocationData(10024004),
    locationnames.loc_level_rungun_mountain_dlc_chaliced: LocationData(10024005),
}
location_level_rungun_event_agrade: dict[str, LocationData] = {
    locationnames.loc_level_rungun_forest_event_agrade: LocationData(None),
    locationnames.loc_level_rungun_tree_event_agrade: LocationData(None),
    locationnames.loc_level_rungun_circus_event_agrade: LocationData(None),
    locationnames.loc_level_rungun_funhouse_event_agrade: LocationData(None),
    locationnames.loc_level_rungun_harbour_event_agrade: LocationData(None),
    locationnames.loc_level_rungun_mountain_event_agrade: LocationData(None),
}
location_level_rungun_event_pacifist: dict[str, LocationData] = {
    locationnames.loc_level_rungun_forest_event_pacifist: LocationData(None),
    locationnames.loc_level_rungun_tree_event_pacifist: LocationData(None),
    locationnames.loc_level_rungun_circus_event_pacifist: LocationData(None),
    locationnames.loc_level_rungun_funhouse_event_pacifist: LocationData(None),
    locationnames.loc_level_rungun_harbour_event_pacifist: LocationData(None),
    locationnames.loc_level_rungun_mountain_event_pacifist: LocationData(None),
}

location_level_mausoleum: dict[str, LocationData] = {
    locationnames.loc_level_mausoleum_i: LocationData(22000),
    locationnames.loc_level_mausoleum_ii: LocationData(22001),
    locationnames.loc_level_mausoleum_iii: LocationData(22002),
}

location_level_dlc_chesscastle: dict[str, LocationData] = {
    locationnames.loc_level_dlc_chesscastle_pawn: LocationData(10026000),
    locationnames.loc_level_dlc_chesscastle_knight: LocationData(10026001),
    locationnames.loc_level_dlc_chesscastle_bishop: LocationData(10026002),
    locationnames.loc_level_dlc_chesscastle_rook: LocationData(10026003),
    locationnames.loc_level_dlc_chesscastle_queen: LocationData(10026004),
    locationnames.loc_level_dlc_chesscastle_run: LocationData(10026005),
}
location_level_dlc_chesscastle_dlc_chaliced: dict[str, LocationData] = {
    locationnames.loc_level_dlc_chesscastle_pawn_dlc_chaliced: LocationData(10028000),
    locationnames.loc_level_dlc_chesscastle_knight_dlc_chaliced: LocationData(10028001),
    locationnames.loc_level_dlc_chesscastle_bishop_dlc_chaliced: LocationData(10028002),
    locationnames.loc_level_dlc_chesscastle_rook_dlc_chaliced: LocationData(10028003),
    locationnames.loc_level_dlc_chesscastle_queen_dlc_chaliced: LocationData(10028004),
    locationnames.loc_level_dlc_chesscastle_run_dlc_chaliced: LocationData(10028005),
}
location_level_dlc_chesscastle_phases: dict[str, LocationData] = {
    locationnames.loc_level_dlc_chesscastle_pawn_phase1: LocationData(10030000),

    locationnames.loc_level_dlc_chesscastle_knight_phase1: LocationData(10030002),

    locationnames.loc_level_dlc_chesscastle_bishop_phase1: LocationData(10030004),
    locationnames.loc_level_dlc_chesscastle_bishop_phase2: LocationData(10030006),
    locationnames.loc_level_dlc_chesscastle_bishop_phase3: LocationData(10030008),
    locationnames.loc_level_dlc_chesscastle_bishop_phase4: LocationData(10030010),

    locationnames.loc_level_dlc_chesscastle_rook_phase1: LocationData(10030012),
    locationnames.loc_level_dlc_chesscastle_rook_phase2: LocationData(10030014),
    locationnames.loc_level_dlc_chesscastle_rook_phase3: LocationData(10030016),
    locationnames.loc_level_dlc_chesscastle_rook_phase4: LocationData(10030018),

    locationnames.loc_level_dlc_chesscastle_queen_phase1: LocationData(10030020),
    locationnames.loc_level_dlc_chesscastle_queen_phase2: LocationData(10030022),
    locationnames.loc_level_dlc_chesscastle_queen_phase3: LocationData(10030024),

    locationnames.loc_level_dlc_chesscastle_run_phase1: LocationData(10030026),
    locationnames.loc_level_dlc_chesscastle_run_phase2: LocationData(10030028),
    locationnames.loc_level_dlc_chesscastle_run_phase3: LocationData(10030030),
    locationnames.loc_level_dlc_chesscastle_run_phase4: LocationData(10030032),
    locationnames.loc_level_dlc_chesscastle_run_phase5: LocationData(10030034),
    locationnames.loc_level_dlc_chesscastle_run_phase6: LocationData(10030036),
}

location_level_dlc_special: dict[str, LocationData] = {
    #locationnames.loc_level_dlc_graveyard: LocationData(10032000),
}

# Shop Locations
location_shop: dict[str, LocationData] = {
    locationnames.loc_shop_weapon1: LocationData(24000),
    locationnames.loc_shop_weapon2: LocationData(24001),
    locationnames.loc_shop_weapon3: LocationData(24002),
    locationnames.loc_shop_weapon4: LocationData(24003),
    locationnames.loc_shop_weapon5: LocationData(24004),
    locationnames.loc_shop_charm1: LocationData(24005),
    locationnames.loc_shop_charm2: LocationData(24006),
    locationnames.loc_shop_charm3: LocationData(24007),
    locationnames.loc_shop_charm4: LocationData(24008),
    locationnames.loc_shop_charm5: LocationData(24009),
    locationnames.loc_shop_charm6: LocationData(24010),
}
location_shop_dlc: dict[str, LocationData] = {
    locationnames.loc_shop_dlc_weapon6: LocationData(10034000),
    locationnames.loc_shop_dlc_weapon7: LocationData(10034001),
    locationnames.loc_shop_dlc_weapon8: LocationData(10034002),
    locationnames.loc_shop_dlc_charm7: LocationData(10034003),
    locationnames.loc_shop_dlc_charm8: LocationData(10034004),
}

# World Locations
location_world: dict[str, LocationData] = {
    locationnames.loc_npc_mac: LocationData(26000),
    locationnames.loc_npc_canteen: LocationData(26001),
    locationnames.loc_coin_isle1_secret: LocationData(26002),
    locationnames.loc_coin_isle2_secret: LocationData(26003),
    locationnames.loc_coin_isle3_secret: LocationData(26004),
    locationnames.loc_coin_isleh_secret: LocationData(26005),
}
location_world_event: dict[str, LocationData] = {
    locationnames.loc_event_isle1_secret_prereq1: LocationData(None),
    locationnames.loc_event_isle1_secret_prereq2: LocationData(None),
    locationnames.loc_event_isle1_secret_prereq3: LocationData(None),
    locationnames.loc_event_isle1_secret_prereq4: LocationData(None),
    locationnames.loc_event_isle1_secret_prereq5: LocationData(None),
}
location_world_quest: dict[str, LocationData] = {
    locationnames.loc_quest_buster: LocationData(28000),
    locationnames.loc_quest_ginger: LocationData(28001),
    locationnames.loc_quest_4mel: LocationData(28002),
    locationnames.loc_quest_lucien: LocationData(28003),
    locationnames.loc_quest_pacifist: LocationData(28004),
    locationnames.loc_quest_silverworth: LocationData(28005),
    locationnames.loc_quest_music: LocationData(28006),
}
location_level_boss_secret: dict[str, LocationData] = {
    locationnames.loc_level_boss_veggies_secret: LocationData(30000),
    locationnames.loc_level_boss_plane_genie_secret: LocationData(30001),
    locationnames.loc_level_boss_sallystageplay_secret: LocationData(30002),
}
location_level_dlc_boss_secret: dict[str, LocationData] = {
    locationnames.loc_level_dlc_boss_airplane_secret: LocationData(10036000),
}
location_dlc_world: dict[str, LocationData] = {
    locationnames.loc_dlc_npc_newscat: LocationData(10038000),
    locationnames.loc_dlc_coin_isle4_secret: LocationData(10038001),
}
location_dlc_world_quest: dict[str, LocationData] = {
    locationnames.loc_dlc_quest_cactusgirl: LocationData(10040000),
}

# Special Locations
location_special: dict[str, LocationData] = {
    locationnames.loc_event_start_weapon: LocationData(None),
    locationnames.loc_event_start_weapon_ex: LocationData(None),
    locationnames.loc_event_isle2_shortcut: LocationData(None),
    locationnames.loc_event_quest_4mel_4th: LocationData(None),
    locationnames.loc_event_quest_ludwig: LocationData(None),
    #locationnames.loc_event_quest_wolfgang: LocationData(None),
    #locationnames.loc_event_music: LocationData(None),
}
location_dlc_special: dict[str, LocationData] = {
    locationnames.loc_dlc_cookie: LocationData(10042000),
    locationnames.loc_event_mausoleum: LocationData(None),
    locationnames.loc_event_dlc_cookie: LocationData(None),
    #locationnames.loc_dlc_curse_complete: LocationData(10042001),
}

# Goal Locations
location_goal: dict[str, LocationData] = {
    locationnames.loc_event_goal_devil: LocationData(None),
}
location_dlc_goal: dict[str, LocationData] = {
    locationnames.loc_event_dlc_goal_saltbaker: LocationData(None),
}

# Kingdice locations
locations_kingdice_all: dict[str, LocationData] = {
    **location_level_boss_kingdice,
    **location_level_boss_kingdice_topgrade,
    **location_level_boss_kingdice_phases,
    **location_level_boss_kingdice_dlc_chaliced,
    **location_level_boss_kingdice_event_agrade,
    **location_level_boss_kingdice_event_dlc_chaliced,
}

locations_base: dict[str, LocationData] = {
    **location_level_tutorial,
    **location_level_boss,
    **location_level_boss_kingdice,
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
    **location_level_boss_kingdice_topgrade,
    #**location_level_boss_final_topgrade,
    **location_level_rungun_agrade,
    **location_level_rungun_pacifist,
}
locations_event_agrade: dict[str, LocationData] = {
    **location_level_boss_event_agrade,
    **location_level_boss_kingdice_event_agrade,
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
}
locations_dlc_boss_chaliced: dict[str, LocationData] = {
    **location_level_boss_dlc_chaliced,
    **location_level_boss_kingdice_dlc_chaliced,
    #**location_level_boss_final_dlc_chaliced,
    **location_level_dlc_boss_dlc_chaliced,
    #**location_level_dlc_boss_final_dlc_chaliced,
}
locations_boss_phases: dict[str, LocationData] = {
    **location_level_boss_phases,
    **location_level_boss_kingdice_phases,
    #**location_level_boss_final_phases,
    **location_level_dlc_boss_phases,
    #**location_level_dlc_boss_final_phases,
}
locations_dlc_topgrade: dict[str, LocationData] = {
    **location_level_dlc_boss_topgrade,
    #**location_level_dlc_boss_final_topgrade,
}
locations_dlc_event_boss_chaliced: dict[str, LocationData] = {
    **location_level_boss_event_dlc_chaliced,
    **location_level_boss_kingdice_event_dlc_chaliced,
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
    **locations_boss_phases,
    **location_level_boss_final_topgrade,  # Final
    **location_level_boss_final_phases, # Final
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
    **location_level_dlc_boss_final_phases, # Final
    **locations_dlc_boss_chaliced,
    **location_level_rungun_dlc_chaliced,
    **location_level_boss_final_dlc_chaliced, # Final
    **location_level_dlc_boss_final_dlc_chaliced, # Final
    **location_level_dicepalace_dlc_chaliced,
    **location_level_dlc_chesscastle_dlc_chaliced,
    **location_level_dlc_chesscastle_phases,
    **locations_dlc_event_boss_chaliced,
    **location_dlc_world_quest,
    **location_dlc_special,
    **location_dlc_goal,
    **location_level_dicepalace,
}

name_to_id = {name: data.id for name, data in locations_all.items() if data.id}
