### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from ..names import locationnames, regionnames
from .levelbase import LevelData

# Levels
level_boss_regular: dict[str, LevelData] = {
    regionnames.level_boss_veggies: LevelData(regionnames.world_inkwell_1, [
        locationnames.loc_level_boss_veggies,
        locationnames.loc_level_boss_veggies_topgrade,
        locationnames.loc_level_boss_veggies_secret,
        locationnames.loc_level_boss_veggies_event_agrade,
        locationnames.loc_level_boss_veggies_dlc_chaliced,
        locationnames.loc_level_boss_veggies_event_dlc_chaliced,
    ]),
    regionnames.level_boss_slime: LevelData(regionnames.world_inkwell_1, [
        locationnames.loc_level_boss_slime,
        locationnames.loc_level_boss_slime_topgrade,
        locationnames.loc_level_boss_slime_event_agrade,
        locationnames.loc_level_boss_slime_dlc_chaliced,
        locationnames.loc_level_boss_slime_event_dlc_chaliced,
    ]),
    regionnames.level_boss_frogs: LevelData(regionnames.world_inkwell_1, [
        locationnames.loc_level_boss_frogs,
        locationnames.loc_level_boss_frogs_topgrade,
        locationnames.loc_level_boss_frogs_event_agrade,
        locationnames.loc_level_boss_frogs_dlc_chaliced,
        locationnames.loc_level_boss_frogs_event_dlc_chaliced,
    ]),
    regionnames.level_boss_flower: LevelData(regionnames.world_inkwell_1, [
        locationnames.loc_level_boss_flower,
        locationnames.loc_level_boss_flower_topgrade,
        locationnames.loc_level_boss_flower_event_agrade,
        locationnames.loc_level_boss_flower_dlc_chaliced,
        locationnames.loc_level_boss_flower_event_dlc_chaliced,
    ]),
    regionnames.level_boss_baroness: LevelData(regionnames.world_inkwell_2, [
        locationnames.loc_level_boss_baroness,
        locationnames.loc_level_boss_baroness_topgrade,
        locationnames.loc_level_boss_baroness_event_agrade,
        locationnames.loc_level_boss_baroness_dlc_chaliced,
        locationnames.loc_level_boss_baroness_event_dlc_chaliced,
    ]),
    regionnames.level_boss_clown: LevelData(regionnames.world_inkwell_2, [
        locationnames.loc_level_boss_clown,
        locationnames.loc_level_boss_clown_topgrade,
        locationnames.loc_level_boss_clown_event_agrade,
        locationnames.loc_level_boss_clown_dlc_chaliced,
        locationnames.loc_level_boss_clown_event_dlc_chaliced,
    ]),
    regionnames.level_boss_dragon: LevelData(regionnames.world_inkwell_2, [
        locationnames.loc_level_boss_dragon,
        locationnames.loc_level_boss_dragon_topgrade,
        locationnames.loc_level_boss_dragon_event_agrade,
        locationnames.loc_level_boss_dragon_dlc_chaliced,
        locationnames.loc_level_boss_dragon_event_dlc_chaliced,
    ]),
    regionnames.level_boss_bee: LevelData(regionnames.world_inkwell_3, [
        locationnames.loc_level_boss_bee,
        locationnames.loc_level_boss_bee_topgrade,
        locationnames.loc_level_boss_bee_event_agrade,
        locationnames.loc_level_boss_bee_dlc_chaliced,
        locationnames.loc_level_boss_bee_event_dlc_chaliced,
    ]),
    regionnames.level_boss_pirate: LevelData(regionnames.world_inkwell_3, [
        locationnames.loc_level_boss_pirate,
        locationnames.loc_level_boss_pirate_topgrade,
        locationnames.loc_level_boss_pirate_event_agrade,
        locationnames.loc_level_boss_pirate_dlc_chaliced,
        locationnames.loc_level_boss_pirate_event_dlc_chaliced,
    ]),
    regionnames.level_boss_mouse: LevelData(regionnames.world_inkwell_3, [
        locationnames.loc_level_boss_mouse,
        locationnames.loc_level_boss_mouse_topgrade,
        locationnames.loc_level_boss_mouse_event_agrade,
        locationnames.loc_level_boss_mouse_dlc_chaliced,
        locationnames.loc_level_boss_mouse_event_dlc_chaliced,
    ]),
    regionnames.level_boss_sallystageplay: LevelData(regionnames.world_inkwell_3, [
        locationnames.loc_level_boss_sallystageplay,
        locationnames.loc_level_boss_sallystageplay_topgrade,
        locationnames.loc_level_boss_sallystageplay_secret,
        locationnames.loc_level_boss_sallystageplay_event_agrade,
        locationnames.loc_level_boss_sallystageplay_dlc_chaliced,
        locationnames.loc_level_boss_sallystageplay_event_dlc_chaliced,
    ]),
    regionnames.level_boss_train: LevelData(regionnames.world_inkwell_3, [
        locationnames.loc_level_boss_train,
        locationnames.loc_level_boss_train_topgrade,
        locationnames.loc_level_boss_train_event_agrade,
        locationnames.loc_level_boss_train_dlc_chaliced,
        locationnames.loc_level_boss_train_event_dlc_chaliced,
    ]),
    regionnames.level_boss_kingdice: LevelData(regionnames.world_inkwell_hell, [
        locationnames.loc_level_boss_kingdice,
        locationnames.loc_level_boss_kingdice_topgrade,
        locationnames.loc_level_boss_kingdice_event_agrade,
        locationnames.loc_level_boss_kingdice_dlc_chaliced,
        locationnames.loc_level_boss_kingdice_event_dlc_chaliced,
    ]), # Has special rules set in rules.py
}
level_boss_plane: dict[str, LevelData] = {
    regionnames.level_boss_plane_blimp: LevelData(regionnames.world_inkwell_1, [
        locationnames.loc_level_boss_plane_blimp,
        locationnames.loc_level_boss_plane_blimp_topgrade,
        locationnames.loc_level_boss_plane_blimp_event_agrade,
        locationnames.loc_level_boss_plane_blimp_dlc_chaliced,
        locationnames.loc_level_boss_plane_blimp_event_dlc_chaliced,
    ]),
    regionnames.level_boss_plane_genie: LevelData(regionnames.world_inkwell_2, [
        locationnames.loc_level_boss_plane_genie,
        locationnames.loc_level_boss_plane_genie_topgrade,
        locationnames.loc_level_boss_plane_genie_secret,
        locationnames.loc_level_boss_plane_genie_event_agrade,
        locationnames.loc_level_boss_plane_genie_dlc_chaliced,
        locationnames.loc_level_boss_plane_genie_event_dlc_chaliced,
    ]),
    regionnames.level_boss_plane_bird: LevelData(regionnames.world_inkwell_2, [
        locationnames.loc_level_boss_plane_bird,
        locationnames.loc_level_boss_plane_bird_topgrade,
        locationnames.loc_level_boss_plane_bird_event_agrade,
        locationnames.loc_level_boss_plane_bird_dlc_chaliced,
        locationnames.loc_level_boss_plane_bird_event_dlc_chaliced,
    ]),
    regionnames.level_boss_plane_mermaid: LevelData(regionnames.world_inkwell_3, [
        locationnames.loc_level_boss_plane_mermaid,
        locationnames.loc_level_boss_plane_mermaid_topgrade,
        locationnames.loc_level_boss_plane_mermaid_event_agrade,
        locationnames.loc_level_boss_plane_mermaid_dlc_chaliced,
        locationnames.loc_level_boss_plane_mermaid_event_dlc_chaliced,
    ]),
    regionnames.level_boss_plane_robot: LevelData(regionnames.world_inkwell_3, [
        locationnames.loc_level_boss_plane_robot,
        locationnames.loc_level_boss_plane_robot_topgrade,
        locationnames.loc_level_boss_plane_robot_event_agrade,
        locationnames.loc_level_boss_plane_robot_dlc_chaliced,
        locationnames.loc_level_boss_plane_robot_event_dlc_chaliced,
    ]),
}
level_boss: dict[str, LevelData] = {
    **level_boss_regular,
    **level_boss_plane
}
level_boss_final: dict[str, LevelData] = {
    regionnames.level_boss_devil: LevelData(regionnames.world_inkwell_hell, [
        locationnames.loc_level_boss_devil,
        locationnames.loc_level_boss_devil_topgrade,
        locationnames.loc_level_boss_devil_event_agrade,
        locationnames.loc_level_boss_devil_dlc_chaliced,
        locationnames.loc_level_boss_devil_event_dlc_chaliced,
        locationnames.loc_event_goal_devil,
    ])
}
level_dlc_boss_regular: dict[str, LevelData] = {
    regionnames.level_dlc_boss_oldman: LevelData(regionnames.world_dlc_inkwell_4, [
        locationnames.loc_level_dlc_boss_oldman,
        locationnames.loc_level_dlc_boss_oldman_topgrade,
        #locationnames.loc_level_dlc_boss_oldman_event_agrade,
        locationnames.loc_level_dlc_boss_oldman_dlc_chaliced,
        locationnames.loc_level_dlc_boss_oldman_event_dlc_chaliced,
    ]),
    regionnames.level_dlc_boss_rumrunners: LevelData(regionnames.world_dlc_inkwell_4, [
        locationnames.loc_level_dlc_boss_rumrunners,
        locationnames.loc_level_dlc_boss_rumrunners_topgrade,
        #locationnames.loc_level_dlc_boss_rumrunners_event_agrade,
        locationnames.loc_level_dlc_boss_rumrunners_dlc_chaliced,
        locationnames.loc_level_dlc_boss_rumrunners_event_dlc_chaliced,
    ]),
    regionnames.level_dlc_boss_snowcult: LevelData(regionnames.world_dlc_inkwell_4, [
        locationnames.loc_level_dlc_boss_snowcult,
        locationnames.loc_level_dlc_boss_snowcult_topgrade,
        #locationnames.loc_level_dlc_boss_snowcult_event_agrade,
        locationnames.loc_level_dlc_boss_snowcult_dlc_chaliced,
        locationnames.loc_level_dlc_boss_snowcult_event_dlc_chaliced,
    ]),
    regionnames.level_dlc_boss_airplane: LevelData(regionnames.world_dlc_inkwell_4, [
        locationnames.loc_level_dlc_boss_airplane,
        locationnames.loc_level_dlc_boss_airplane_topgrade,
        locationnames.loc_level_dlc_boss_airplane_secret,
        #locationnames.loc_level_dlc_boss_airplane_event_agrade,
        locationnames.loc_level_dlc_boss_airplane_dlc_chaliced,
        locationnames.loc_level_dlc_boss_airplane_event_dlc_chaliced,
    ]),
}
level_dlc_boss_plane: dict[str, LevelData] = {
    regionnames.level_dlc_boss_plane_cowboy: LevelData(regionnames.world_dlc_inkwell_4, [
        locationnames.loc_level_dlc_boss_plane_cowboy,
        locationnames.loc_level_dlc_boss_plane_cowboy_topgrade,
        #locationnames.loc_level_dlc_boss_plane_cowboy_event_agrade,
        locationnames.loc_level_dlc_boss_plane_cowboy_dlc_chaliced,
        locationnames.loc_level_dlc_boss_plane_cowboy_event_dlc_chaliced,
    ]),
}
level_dlc_boss: dict[str, LevelData] = {
    **level_dlc_boss_regular,
    **level_dlc_boss_plane
}
level_dlc_boss_final: dict[str, LevelData] = {
    regionnames.level_dlc_boss_saltbaker: LevelData(regionnames.world_dlc_inkwell_4, [
        locationnames.loc_level_dlc_boss_saltbaker,
        locationnames.loc_level_dlc_boss_saltbaker_topgrade,
        locationnames.loc_level_dlc_boss_saltbaker_event_agrade,
        locationnames.loc_level_dlc_boss_saltbaker_dlc_chaliced,
        locationnames.loc_level_dlc_boss_saltbaker_event_dlc_chaliced,
        locationnames.loc_event_dlc_goal_saltbaker,
    ]),
}
level_dicepalace_boss: dict[str, LevelData] = {
    regionnames.level_dicepalace_boss_booze: LevelData(regionnames.level_boss_kingdice, [
        locationnames.loc_level_dicepalace_boss_booze,
        locationnames.loc_level_dicepalace_boss_booze_dlc_chaliced,
    ]),
    regionnames.level_dicepalace_boss_chips: LevelData(regionnames.level_boss_kingdice, [
        locationnames.loc_level_dicepalace_boss_chips,
        locationnames.loc_level_dicepalace_boss_chips_dlc_chaliced,
    ]),
    regionnames.level_dicepalace_boss_cigar: LevelData(regionnames.level_boss_kingdice, [
        locationnames.loc_level_dicepalace_boss_cigar,
        locationnames.loc_level_dicepalace_boss_cigar_dlc_chaliced,
    ]),
    regionnames.level_dicepalace_boss_domino: LevelData(regionnames.level_boss_kingdice, [
        locationnames.loc_level_dicepalace_boss_domino,
        locationnames.loc_level_dicepalace_boss_domino_dlc_chaliced,
    ]),
    regionnames.level_dicepalace_boss_rabbit: LevelData(regionnames.level_boss_kingdice, [
        locationnames.loc_level_dicepalace_boss_rabbit,
        locationnames.loc_level_dicepalace_boss_rabbit_dlc_chaliced,
    ]),
    regionnames.level_dicepalace_boss_plane_horse: LevelData(regionnames.level_boss_kingdice, [
        locationnames.loc_level_dicepalace_boss_plane_horse,
        locationnames.loc_level_dicepalace_boss_plane_horse_dlc_chaliced,
    ]),
    regionnames.level_dicepalace_boss_roulette: LevelData(regionnames.level_boss_kingdice, [
        locationnames.loc_level_dicepalace_boss_roulette,
        locationnames.loc_level_dicepalace_boss_roulette_dlc_chaliced,
    ]),
    regionnames.level_dicepalace_boss_eightball: LevelData(regionnames.level_boss_kingdice, [
        locationnames.loc_level_dicepalace_boss_eightball,
        locationnames.loc_level_dicepalace_boss_eightball_dlc_chaliced,
    ]),
    regionnames.level_dicepalace_boss_plane_memory: LevelData(regionnames.level_boss_kingdice, [
        locationnames.loc_level_dicepalace_boss_plane_memory,
        locationnames.loc_level_dicepalace_boss_plane_memory_dlc_chaliced,
    ]),
}
level_rungun: dict[str, LevelData] = {
    regionnames.level_rungun_forest: LevelData(regionnames.world_inkwell_1, [
        locationnames.loc_level_rungun_forest,
        locationnames.loc_level_rungun_forest_agrade,
        locationnames.loc_level_rungun_forest_pacifist,
        locationnames.loc_level_rungun_forest_coin1,
        locationnames.loc_level_rungun_forest_coin2,
        locationnames.loc_level_rungun_forest_coin3,
        locationnames.loc_level_rungun_forest_coin4,
        locationnames.loc_level_rungun_forest_coin5,
        locationnames.loc_level_rungun_forest_dlc_chaliced,
        locationnames.loc_level_rungun_forest_event_agrade,
        locationnames.loc_level_rungun_forest_event_pacifist,
    ]),
    regionnames.level_rungun_tree: LevelData(regionnames.world_inkwell_1, [
        locationnames.loc_level_rungun_tree,
        locationnames.loc_level_rungun_tree_agrade,
        locationnames.loc_level_rungun_tree_pacifist,
        locationnames.loc_level_rungun_tree_coin1,
        locationnames.loc_level_rungun_tree_coin2,
        locationnames.loc_level_rungun_tree_coin3,
        locationnames.loc_level_rungun_tree_coin4,
        locationnames.loc_level_rungun_tree_coin5,
        locationnames.loc_level_rungun_tree_dlc_chaliced,
        locationnames.loc_level_rungun_tree_event_agrade,
        locationnames.loc_level_rungun_tree_event_pacifist,
    ]),
    regionnames.level_rungun_circus: LevelData(regionnames.world_inkwell_2, [
        locationnames.loc_level_rungun_circus,
        locationnames.loc_level_rungun_circus_agrade,
        locationnames.loc_level_rungun_circus_pacifist,
        locationnames.loc_level_rungun_circus_coin1,
        locationnames.loc_level_rungun_circus_coin2,
        locationnames.loc_level_rungun_circus_coin3,
        locationnames.loc_level_rungun_circus_coin4,
        locationnames.loc_level_rungun_circus_coin5,
        locationnames.loc_level_rungun_circus_dlc_chaliced,
        locationnames.loc_level_rungun_circus_event_agrade,
        locationnames.loc_level_rungun_circus_event_pacifist,
    ]),
    regionnames.level_rungun_funhouse: LevelData(regionnames.world_inkwell_2, [
        locationnames.loc_level_rungun_funhouse,
        locationnames.loc_level_rungun_funhouse_agrade,
        locationnames.loc_level_rungun_funhouse_pacifist,
        locationnames.loc_level_rungun_funhouse_coin1,
        locationnames.loc_level_rungun_funhouse_coin2,
        locationnames.loc_level_rungun_funhouse_coin3,
        locationnames.loc_level_rungun_funhouse_coin4,
        locationnames.loc_level_rungun_funhouse_coin5,
        locationnames.loc_level_rungun_funhouse_dlc_chaliced,
        locationnames.loc_level_rungun_funhouse_event_agrade,
        locationnames.loc_level_rungun_funhouse_event_pacifist,
    ]),
    regionnames.level_rungun_harbour: LevelData(regionnames.world_inkwell_3, [
        locationnames.loc_level_rungun_harbour,
        locationnames.loc_level_rungun_harbour_agrade,
        locationnames.loc_level_rungun_harbour_pacifist,
        locationnames.loc_level_rungun_harbour_coin1,
        locationnames.loc_level_rungun_harbour_coin2,
        locationnames.loc_level_rungun_harbour_coin3,
        locationnames.loc_level_rungun_harbour_coin4,
        locationnames.loc_level_rungun_harbour_coin5,
        locationnames.loc_level_rungun_harbour_dlc_chaliced,
        locationnames.loc_level_rungun_harbour_event_agrade,
        locationnames.loc_level_rungun_harbour_event_pacifist,
    ]),
    regionnames.level_rungun_mountain: LevelData(regionnames.world_inkwell_3, [
        locationnames.loc_level_rungun_mountain,
        locationnames.loc_level_rungun_mountain_agrade,
        locationnames.loc_level_rungun_mountain_pacifist,
        locationnames.loc_level_rungun_mountain_coin1,
        locationnames.loc_level_rungun_mountain_coin2,
        locationnames.loc_level_rungun_mountain_coin3,
        locationnames.loc_level_rungun_mountain_coin4,
        locationnames.loc_level_rungun_mountain_coin5,
        locationnames.loc_level_rungun_mountain_dlc_chaliced,
        locationnames.loc_level_rungun_mountain_event_agrade,
        locationnames.loc_level_rungun_mountain_event_pacifist,
    ]),
}
level_mausoleum: dict[str, LevelData] = {
    regionnames.level_mausoleum_i: LevelData(
        regionnames.world_inkwell_1, [locationnames.loc_level_mausoleum_i]
    ),
    regionnames.level_mausoleum_ii: LevelData(
        regionnames.world_inkwell_2, [locationnames.loc_level_mausoleum_ii]
    ),
    regionnames.level_mausoleum_iii: LevelData(
        regionnames.world_inkwell_3, [locationnames.loc_level_mausoleum_iii]
    ),
}
level_dlc_chesscastle_boss: dict[str, LevelData] = {
    regionnames.level_dlc_chesscastle_pawn: LevelData(regionnames.level_dlc_chesscastle, [
        locationnames.loc_level_dlc_chesscastle_pawn,
        locationnames.loc_level_dlc_chesscastle_pawn_dlc_chaliced,
    ]),
    regionnames.level_dlc_chesscastle_knight: LevelData(regionnames.level_dlc_chesscastle, [
        locationnames.loc_level_dlc_chesscastle_knight,
        locationnames.loc_level_dlc_chesscastle_knight_dlc_chaliced,
    ]),
    regionnames.level_dlc_chesscastle_bishop: LevelData(regionnames.level_dlc_chesscastle, [
        locationnames.loc_level_dlc_chesscastle_bishop,
        locationnames.loc_level_dlc_chesscastle_bishop_dlc_chaliced,
    ]),
    regionnames.level_dlc_chesscastle_rook: LevelData(regionnames.level_dlc_chesscastle, [
        locationnames.loc_level_dlc_chesscastle_rook,
        locationnames.loc_level_dlc_chesscastle_rook_dlc_chaliced,
    ]),
    regionnames.level_dlc_chesscastle_queen: LevelData(regionnames.level_dlc_chesscastle, [
        locationnames.loc_level_dlc_chesscastle_queen,
        locationnames.loc_level_dlc_chesscastle_queen_dlc_chaliced,
    ]),
    regionnames.level_dlc_chesscastle_run: LevelData(regionnames.level_dlc_chesscastle, [
        locationnames.loc_level_dlc_chesscastle_run,
        locationnames.loc_level_dlc_chesscastle_run_dlc_chaliced,
    ]),
}
level_special: dict[str, LevelData] = {
    regionnames.level_tutorial: LevelData(
        regionnames.level_house,
        [locationnames.loc_level_tutorial, locationnames.loc_level_tutorial_coin,]
    )
}
level_dlc_special: dict[str, LevelData] = {
    regionnames.level_dlc_tutorial: LevelData(
        regionnames.level_dlc_tutorial,
        [locationnames.loc_level_dlc_tutorial, locationnames.loc_level_dlc_tutorial_coin],
    )
    #regionnames.level_dlc_graveyard: LevelData(
    #    regionnames.world_dlc_inkwell_4,
    #    [locationnames.loc_level_dlc_graveyard,],
    #    lr.lrule_dlc_relic
    #),
}

levels_base: dict[str, LevelData] = {
    **level_boss,
    **level_boss_final,
    **level_rungun,
    **level_mausoleum
}
levels_dlc: dict[str, LevelData] = {
    **level_dlc_boss,
    **level_dlc_boss_final,
    **level_dlc_chesscastle_boss,
}
levels_all: dict[str, LevelData] = {
    **levels_base,
    **level_dicepalace_boss,
    **levels_dlc,
    **level_special,
    **level_dlc_special,
}
