from __future__ import annotations
from ..names import LocationNames
from .levelbase import LevelData
from . import levelrules as lr

# Levels
level_boss_regular: dict[str, LevelData] = {
    LocationNames.level_boss_veggies: LevelData(LocationNames.world_inkwell_1, [
        LocationNames.loc_level_boss_veggies,
        LocationNames.loc_level_boss_veggies_topgrade,
        LocationNames.loc_level_boss_veggies_secret,
        LocationNames.loc_level_boss_veggies_event_agrade,
        LocationNames.loc_level_boss_veggies_dlc_chaliced,
        LocationNames.loc_level_boss_veggies_event_dlc_chaliced,
    ]), # No rules
    LocationNames.level_boss_slime: LevelData(LocationNames.world_inkwell_1, [
        LocationNames.loc_level_boss_slime,
        LocationNames.loc_level_boss_slime_topgrade,
        LocationNames.loc_level_boss_slime_event_agrade,
        LocationNames.loc_level_boss_slime_dlc_chaliced,
        LocationNames.loc_level_boss_slime_event_dlc_chaliced,
    ], lr.lrule_duck_or_dash),
    LocationNames.level_boss_frogs: LevelData(LocationNames.world_inkwell_1, [
        LocationNames.loc_level_boss_frogs,
        LocationNames.loc_level_boss_frogs_topgrade,
        LocationNames.loc_level_boss_frogs_event_agrade,
        LocationNames.loc_level_boss_frogs_dlc_chaliced,
        LocationNames.loc_level_boss_frogs_event_dlc_chaliced,
    ], lr.lrule_parry_or_psugar),
    LocationNames.level_boss_flower: LevelData(LocationNames.world_inkwell_1, [
        LocationNames.loc_level_boss_flower,
        LocationNames.loc_level_boss_flower_topgrade,
        LocationNames.loc_level_boss_flower_event_agrade,
        LocationNames.loc_level_boss_flower_dlc_chaliced,
        LocationNames.loc_level_boss_flower_event_dlc_chaliced,
    ]), # No rules
    LocationNames.level_boss_baroness: LevelData(LocationNames.world_inkwell_2, [
        LocationNames.loc_level_boss_baroness,
        LocationNames.loc_level_boss_baroness_topgrade,
        LocationNames.loc_level_boss_baroness_event_agrade,
        LocationNames.loc_level_boss_baroness_dlc_chaliced,
        LocationNames.loc_level_boss_baroness_event_dlc_chaliced,
    ], lr.lrule_parry_or_psugar),
    LocationNames.level_boss_clown: LevelData(LocationNames.world_inkwell_2, [
        LocationNames.loc_level_boss_clown,
        LocationNames.loc_level_boss_clown_topgrade,
        LocationNames.loc_level_boss_clown_event_agrade,
        LocationNames.loc_level_boss_clown_dlc_chaliced,
        LocationNames.loc_level_boss_clown_event_dlc_chaliced,
    ], lr.lrule_dash_or_parry),
    LocationNames.level_boss_dragon: LevelData(LocationNames.world_inkwell_2, [
        LocationNames.loc_level_boss_dragon,
        LocationNames.loc_level_boss_dragon_topgrade,
        LocationNames.loc_level_boss_dragon_event_agrade,
        LocationNames.loc_level_boss_dragon_dlc_chaliced,
        LocationNames.loc_level_boss_dragon_event_dlc_chaliced,
    ]), # No Rules
    LocationNames.level_boss_bee: LevelData(LocationNames.world_inkwell_3, [
        LocationNames.loc_level_boss_bee,
        LocationNames.loc_level_boss_bee_topgrade,
        LocationNames.loc_level_boss_bee_event_agrade,
        LocationNames.loc_level_boss_bee_dlc_chaliced,
        LocationNames.loc_level_boss_bee_event_dlc_chaliced,
    ]), # No Rules
    LocationNames.level_boss_pirate: LevelData(LocationNames.world_inkwell_3, [
        LocationNames.loc_level_boss_pirate,
        LocationNames.loc_level_boss_pirate_topgrade,
        LocationNames.loc_level_boss_pirate_event_agrade,
        LocationNames.loc_level_boss_pirate_dlc_chaliced,
        LocationNames.loc_level_boss_pirate_event_dlc_chaliced,
    ], lr.lrule_pirate),
    LocationNames.level_boss_mouse: LevelData(LocationNames.world_inkwell_3, [
        LocationNames.loc_level_boss_mouse,
        LocationNames.loc_level_boss_mouse_topgrade,
        LocationNames.loc_level_boss_mouse_event_agrade,
        LocationNames.loc_level_boss_mouse_dlc_chaliced,
        LocationNames.loc_level_boss_mouse_event_dlc_chaliced,
    ], lr.lrule_mouse),
    LocationNames.level_boss_sallystageplay: LevelData(LocationNames.world_inkwell_3, [
        LocationNames.loc_level_boss_sallystageplay,
        LocationNames.loc_level_boss_sallystageplay_topgrade,
        LocationNames.loc_level_boss_sallystageplay_secret,
        LocationNames.loc_level_boss_sallystageplay_event_agrade,
        LocationNames.loc_level_boss_sallystageplay_dlc_chaliced,
        LocationNames.loc_level_boss_sallystageplay_event_dlc_chaliced,
    ], lr.lrule_parry),
    LocationNames.level_boss_train: LevelData(LocationNames.world_inkwell_3, [
        LocationNames.loc_level_boss_train,
        LocationNames.loc_level_boss_train_topgrade,
        LocationNames.loc_level_boss_train_event_agrade,
        LocationNames.loc_level_boss_train_dlc_chaliced,
        LocationNames.loc_level_boss_train_event_dlc_chaliced,
    ], lr.lrule_parry),
    LocationNames.level_boss_kingdice: LevelData(LocationNames.world_inkwell_hell, [
        LocationNames.loc_level_boss_kingdice,
        LocationNames.loc_level_boss_kingdice_topgrade,
        LocationNames.loc_level_boss_kingdice_event_agrade,
        LocationNames.loc_level_boss_kingdice_dlc_chaliced,
        LocationNames.loc_level_boss_kingdice_event_dlc_chaliced,
    ], lr.lrule_kingdice), # Has special rules set in rules.py
}
level_boss_plane: dict[str, LevelData] = {
    LocationNames.level_boss_plane_blimp: LevelData(LocationNames.world_inkwell_1, [
        LocationNames.loc_level_boss_plane_blimp,
        LocationNames.loc_level_boss_plane_blimp_topgrade,
        LocationNames.loc_level_boss_plane_blimp_event_agrade,
        LocationNames.loc_level_boss_plane_blimp_dlc_chaliced,
        LocationNames.loc_level_boss_plane_blimp_event_dlc_chaliced,
    ], lr.lrule_plane),
    LocationNames.level_boss_plane_genie: LevelData(LocationNames.world_inkwell_2, [
        LocationNames.loc_level_boss_plane_genie,
        LocationNames.loc_level_boss_plane_genie_topgrade,
        LocationNames.loc_level_boss_plane_genie_secret,
        LocationNames.loc_level_boss_plane_genie_event_agrade,
        LocationNames.loc_level_boss_plane_genie_dlc_chaliced,
        LocationNames.loc_level_boss_plane_genie_event_dlc_chaliced,
    ], lr.lrule_plane),
    LocationNames.level_boss_plane_bird: LevelData(LocationNames.world_inkwell_2, [
        LocationNames.loc_level_boss_plane_bird,
        LocationNames.loc_level_boss_plane_bird_topgrade,
        LocationNames.loc_level_boss_plane_bird_event_agrade,
        LocationNames.loc_level_boss_plane_bird_dlc_chaliced,
        LocationNames.loc_level_boss_plane_bird_event_dlc_chaliced,
    ], lr.lrule_bird),
    LocationNames.level_boss_plane_mermaid: LevelData(LocationNames.world_inkwell_3, [
        LocationNames.loc_level_boss_plane_mermaid,
        LocationNames.loc_level_boss_plane_mermaid_topgrade,
        LocationNames.loc_level_boss_plane_mermaid_event_agrade,
        LocationNames.loc_level_boss_plane_mermaid_dlc_chaliced,
        LocationNames.loc_level_boss_plane_mermaid_event_dlc_chaliced,
    ], lr.lrule_plane),
    LocationNames.level_boss_plane_robot: LevelData(LocationNames.world_inkwell_3, [
        LocationNames.loc_level_boss_plane_robot,
        LocationNames.loc_level_boss_plane_robot_topgrade,
        LocationNames.loc_level_boss_plane_robot_event_agrade,
        LocationNames.loc_level_boss_plane_robot_dlc_chaliced,
        LocationNames.loc_level_boss_plane_robot_event_dlc_chaliced,
    ], lr.lrule_robot),
}
level_boss: dict[str, LevelData] = {
    **level_boss_regular,
    **level_boss_plane
}
level_boss_final: dict[str, LevelData] = {
    LocationNames.level_boss_devil: LevelData(LocationNames.world_inkwell_hell, [
        LocationNames.loc_level_boss_devil,
        LocationNames.loc_level_boss_devil_topgrade,
        LocationNames.loc_level_boss_devil_event_agrade,
        LocationNames.loc_level_boss_devil_dlc_chaliced,
        LocationNames.loc_level_boss_devil_event_dlc_chaliced,
        LocationNames.loc_event_goal_devil,
    ], lr.lrule_final)
}
level_dlc_boss_regular: dict[str, LevelData] = {
    LocationNames.level_dlc_boss_oldman: LevelData(LocationNames.world_dlc_inkwell_4, [
        LocationNames.loc_level_dlc_boss_oldman,
        LocationNames.loc_level_dlc_boss_oldman_topgrade,
        #LocationNames.loc_level_dlc_boss_oldman_event_agrade,
        LocationNames.loc_level_dlc_boss_oldman_dlc_chaliced,
        LocationNames.loc_level_dlc_boss_oldman_event_dlc_chaliced,
    ], lr.lrule_dlc_oldman),
    LocationNames.level_dlc_boss_rumrunners: LevelData(LocationNames.world_dlc_inkwell_4, [
        LocationNames.loc_level_dlc_boss_rumrunners,
        LocationNames.loc_level_dlc_boss_rumrunners_topgrade,
        #LocationNames.loc_level_dlc_boss_rumrunners_event_agrade,
        LocationNames.loc_level_dlc_boss_rumrunners_dlc_chaliced,
        LocationNames.loc_level_dlc_boss_rumrunners_event_dlc_chaliced,
    ], lr.lrule_duck_and_parry),
    LocationNames.level_dlc_boss_snowcult: LevelData(LocationNames.world_dlc_inkwell_4, [
        LocationNames.loc_level_dlc_boss_snowcult,
        LocationNames.loc_level_dlc_boss_snowcult_topgrade,
        #LocationNames.loc_level_dlc_boss_snowcult_event_agrade,
        LocationNames.loc_level_dlc_boss_snowcult_dlc_chaliced,
        LocationNames.loc_level_dlc_boss_snowcult_event_dlc_chaliced,
    ]), # No Rules
    LocationNames.level_dlc_boss_airplane: LevelData(LocationNames.world_dlc_inkwell_4, [
        LocationNames.loc_level_dlc_boss_airplane,
        LocationNames.loc_level_dlc_boss_airplane_topgrade,
        LocationNames.loc_level_dlc_boss_airplane_secret,
        #LocationNames.loc_level_dlc_boss_airplane_event_agrade,
        LocationNames.loc_level_dlc_boss_airplane_dlc_chaliced,
        LocationNames.loc_level_dlc_boss_airplane_event_dlc_chaliced,
    ], lr.lrule_duck),
}
level_dlc_boss_plane: dict[str, LevelData] = {
    LocationNames.level_dlc_boss_plane_cowboy: LevelData(LocationNames.world_dlc_inkwell_4, [
        LocationNames.loc_level_dlc_boss_plane_cowboy,
        LocationNames.loc_level_dlc_boss_plane_cowboy_topgrade,
        #LocationNames.loc_level_dlc_boss_plane_cowboy_event_agrade,
        LocationNames.loc_level_dlc_boss_plane_cowboy_dlc_chaliced,
        LocationNames.loc_level_dlc_boss_plane_cowboy_event_dlc_chaliced,
    ], lr.lrule_plane),
}
level_dlc_boss: dict[str, LevelData] = {
    **level_dlc_boss_regular,
    **level_dlc_boss_plane
}
level_dlc_boss_final: dict[str, LevelData] = {
    LocationNames.level_dlc_boss_saltbaker: LevelData(LocationNames.world_dlc_inkwell_4, [
        LocationNames.loc_level_dlc_boss_saltbaker,
        LocationNames.loc_level_dlc_boss_saltbaker_topgrade,
        LocationNames.loc_level_dlc_boss_saltbaker_event_agrade,
        LocationNames.loc_level_dlc_boss_saltbaker_dlc_chaliced,
        LocationNames.loc_level_dlc_boss_saltbaker_event_dlc_chaliced,
        LocationNames.loc_event_dlc_goal_saltbaker,
    ], lr.lrule_final),
}
level_dicepalace_boss: dict[str, LevelData] = {
    LocationNames.level_dicepalace_boss_booze: LevelData(LocationNames.level_boss_kingdice, [
        LocationNames.loc_level_dicepalace_boss_booze,
        LocationNames.loc_level_dicepalace_boss_booze_dlc_chaliced,
    ]),
    LocationNames.level_dicepalace_boss_chips: LevelData(LocationNames.level_boss_kingdice, [
        LocationNames.loc_level_dicepalace_boss_chips,
        LocationNames.loc_level_dicepalace_boss_chips_dlc_chaliced,
    ]),
    LocationNames.level_dicepalace_boss_cigar: LevelData(LocationNames.level_boss_kingdice, [
        LocationNames.loc_level_dicepalace_boss_cigar,
        LocationNames.loc_level_dicepalace_boss_cigar_dlc_chaliced,
    ]),
    LocationNames.level_dicepalace_boss_domino: LevelData(LocationNames.level_boss_kingdice, [
        LocationNames.loc_level_dicepalace_boss_domino,
        LocationNames.loc_level_dicepalace_boss_domino_dlc_chaliced,
    ]),
    LocationNames.level_dicepalace_boss_rabbit: LevelData(LocationNames.level_boss_kingdice, [
        LocationNames.loc_level_dicepalace_boss_rabbit,
        LocationNames.loc_level_dicepalace_boss_rabbit_dlc_chaliced,
    ]),
    LocationNames.level_dicepalace_boss_plane_horse: LevelData(LocationNames.level_boss_kingdice, [
        LocationNames.loc_level_dicepalace_boss_plane_horse,
        LocationNames.loc_level_dicepalace_boss_plane_horse_dlc_chaliced,
    ]),
    LocationNames.level_dicepalace_boss_roulette: LevelData(LocationNames.level_boss_kingdice, [
        LocationNames.loc_level_dicepalace_boss_roulette,
        LocationNames.loc_level_dicepalace_boss_roulette_dlc_chaliced,
    ]),
    LocationNames.level_dicepalace_boss_eightball: LevelData(LocationNames.level_boss_kingdice, [
        LocationNames.loc_level_dicepalace_boss_eightball,
        LocationNames.loc_level_dicepalace_boss_eightball_dlc_chaliced,
    ]),
    LocationNames.level_dicepalace_boss_plane_memory: LevelData(LocationNames.level_boss_kingdice, [
        LocationNames.loc_level_dicepalace_boss_plane_memory,
        LocationNames.loc_level_dicepalace_boss_plane_memory_dlc_chaliced,
    ]),
}
level_rungun: dict[str, LevelData] = {
    LocationNames.level_rungun_forest: LevelData(LocationNames.world_inkwell_1, [
        LocationNames.loc_level_rungun_forest,
        LocationNames.loc_level_rungun_forest_agrade,
        LocationNames.loc_level_rungun_forest_pacifist,
        LocationNames.loc_level_rungun_forest_coin1,
        LocationNames.loc_level_rungun_forest_coin2,
        LocationNames.loc_level_rungun_forest_coin3,
        LocationNames.loc_level_rungun_forest_coin4,
        LocationNames.loc_level_rungun_forest_coin5,
        LocationNames.loc_level_rungun_forest_dlc_chaliced,
        LocationNames.loc_level_rungun_forest_event_agrade,
        LocationNames.loc_level_rungun_forest_event_pacifist,
    ]),
    LocationNames.level_rungun_tree: LevelData(LocationNames.world_inkwell_1, [
        LocationNames.loc_level_rungun_tree,
        LocationNames.loc_level_rungun_tree_agrade,
        LocationNames.loc_level_rungun_tree_pacifist,
        LocationNames.loc_level_rungun_tree_coin1,
        LocationNames.loc_level_rungun_tree_coin2,
        LocationNames.loc_level_rungun_tree_coin3,
        LocationNames.loc_level_rungun_tree_coin4,
        LocationNames.loc_level_rungun_tree_coin5,
        LocationNames.loc_level_rungun_tree_dlc_chaliced,
        LocationNames.loc_level_rungun_tree_event_agrade,
        LocationNames.loc_level_rungun_tree_event_pacifist,
    ]),
    LocationNames.level_rungun_circus: LevelData(LocationNames.world_inkwell_2, [
        LocationNames.loc_level_rungun_circus,
        LocationNames.loc_level_rungun_circus_agrade,
        LocationNames.loc_level_rungun_circus_pacifist,
        LocationNames.loc_level_rungun_circus_coin1,
        LocationNames.loc_level_rungun_circus_coin2,
        LocationNames.loc_level_rungun_circus_coin3,
        LocationNames.loc_level_rungun_circus_coin4,
        LocationNames.loc_level_rungun_circus_coin5,
        LocationNames.loc_level_rungun_circus_dlc_chaliced,
        LocationNames.loc_level_rungun_circus_event_agrade,
        LocationNames.loc_level_rungun_circus_event_pacifist,
    ]),
    LocationNames.level_rungun_funhouse: LevelData(LocationNames.world_inkwell_2, [
        LocationNames.loc_level_rungun_funhouse,
        LocationNames.loc_level_rungun_funhouse_agrade,
        LocationNames.loc_level_rungun_funhouse_pacifist,
        LocationNames.loc_level_rungun_funhouse_coin1,
        LocationNames.loc_level_rungun_funhouse_coin2,
        LocationNames.loc_level_rungun_funhouse_coin3,
        LocationNames.loc_level_rungun_funhouse_coin4,
        LocationNames.loc_level_rungun_funhouse_coin5,
        LocationNames.loc_level_rungun_funhouse_dlc_chaliced,
        LocationNames.loc_level_rungun_funhouse_event_agrade,
        LocationNames.loc_level_rungun_funhouse_event_pacifist,
    ]),
    LocationNames.level_rungun_harbour: LevelData(LocationNames.world_inkwell_3, [
        LocationNames.loc_level_rungun_harbour,
        LocationNames.loc_level_rungun_harbour_agrade,
        LocationNames.loc_level_rungun_harbour_pacifist,
        LocationNames.loc_level_rungun_harbour_coin1,
        LocationNames.loc_level_rungun_harbour_coin2,
        LocationNames.loc_level_rungun_harbour_coin3,
        LocationNames.loc_level_rungun_harbour_coin4,
        LocationNames.loc_level_rungun_harbour_coin5,
        LocationNames.loc_level_rungun_harbour_dlc_chaliced,
        LocationNames.loc_level_rungun_harbour_event_agrade,
        LocationNames.loc_level_rungun_harbour_event_pacifist,
    ]),
    LocationNames.level_rungun_mountain: LevelData(LocationNames.world_inkwell_3, [
        LocationNames.loc_level_rungun_mountain,
        LocationNames.loc_level_rungun_mountain_agrade,
        LocationNames.loc_level_rungun_mountain_pacifist,
        LocationNames.loc_level_rungun_mountain_coin1,
        LocationNames.loc_level_rungun_mountain_coin2,
        LocationNames.loc_level_rungun_mountain_coin3,
        LocationNames.loc_level_rungun_mountain_coin4,
        LocationNames.loc_level_rungun_mountain_coin5,
        LocationNames.loc_level_rungun_mountain_dlc_chaliced,
        LocationNames.loc_level_rungun_mountain_event_agrade,
        LocationNames.loc_level_rungun_mountain_event_pacifist,
    ]),
}
level_mausoleum: dict[str, LevelData] = {
    LocationNames.level_mausoleum_i: LevelData(
        LocationNames.world_inkwell_1, [LocationNames.loc_level_mausoleum_i], lr.lrule_parry
    ),
    LocationNames.level_mausoleum_ii: LevelData(
        LocationNames.world_inkwell_2, [LocationNames.loc_level_mausoleum_ii], lr.lrule_parry
    ),
    LocationNames.level_mausoleum_iii: LevelData(
        LocationNames.world_inkwell_3, [LocationNames.loc_level_mausoleum_iii], lr.lrule_parry
    ),
}
level_dlc_chesscastle_boss: dict[str, LevelData] = {
    LocationNames.level_dlc_chesscastle_pawn: LevelData(LocationNames.level_dlc_chesscastle, [
        LocationNames.loc_level_dlc_chesscastle_pawn,
        LocationNames.loc_level_dlc_chesscastle_pawn_dlc_chaliced,
    ], lr.lrule_parry),
    LocationNames.level_dlc_chesscastle_knight: LevelData(LocationNames.level_dlc_chesscastle, [
        LocationNames.loc_level_dlc_chesscastle_knight,
        LocationNames.loc_level_dlc_chesscastle_knight_dlc_chaliced,
    ], lr.lrule_parry),
    LocationNames.level_dlc_chesscastle_bishop: LevelData(LocationNames.level_dlc_chesscastle, [
        LocationNames.loc_level_dlc_chesscastle_bishop,
        LocationNames.loc_level_dlc_chesscastle_bishop_dlc_chaliced,
    ], lr.lrule_parry),
    LocationNames.level_dlc_chesscastle_rook: LevelData(LocationNames.level_dlc_chesscastle, [
        LocationNames.loc_level_dlc_chesscastle_rook,
        LocationNames.loc_level_dlc_chesscastle_rook_dlc_chaliced,
    ], lr.lrule_parry),
    LocationNames.level_dlc_chesscastle_queen: LevelData(LocationNames.level_dlc_chesscastle, [
        LocationNames.loc_level_dlc_chesscastle_queen,
        LocationNames.loc_level_dlc_chesscastle_queen_dlc_chaliced,
    ], lr.lrule_parry),
    LocationNames.level_dlc_chesscastle_run: LevelData(LocationNames.level_dlc_chesscastle, [
        LocationNames.loc_level_dlc_chesscastle_run,
        LocationNames.loc_level_dlc_chesscastle_run_dlc_chaliced,
    ], lr.lrule_parry),
}
level_special: dict[str, LevelData] = {
    LocationNames.level_tutorial: LevelData(
        LocationNames.level_house,
        [LocationNames.loc_level_tutorial, LocationNames.loc_level_tutorial_coin,],
        lr.lrule_duck_dash_and_parry
    )
}
level_dlc_special: dict[str, LevelData] = {
    LocationNames.level_dlc_tutorial: LevelData(
        LocationNames.level_dlc_tutorial,
        [LocationNames.loc_level_dlc_tutorial, LocationNames.loc_level_dlc_tutorial_coin],
    )
    #LocationNames.level_dlc_graveyard: LevelData(
    #    LocationNames.world_dlc_inkwell_4,
    #    [LocationNames.loc_level_dlc_graveyard,],
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
