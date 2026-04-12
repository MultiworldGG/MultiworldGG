from __future__ import annotations
from ..names import LocationNames
from .levellocrulebase import LevelLocRuleData, LRule, LevelRuleModes
from . import levelrules as lr

level_loc_rules_boss: list[LevelLocRuleData] = [
    LevelLocRuleData(LocationNames.level_boss_frogs, lr.lrule_parry_or_psugar, {
        LocationNames.loc_level_boss_frogs_dlc_chaliced: LRule(lr.lrule_dlc_boss_chaliced_parry),
        LocationNames.loc_level_boss_frogs_event_dlc_chaliced: LRule(lr.lrule_dlc_boss_chaliced_parry),
    }),
    LevelLocRuleData(LocationNames.level_boss_plane_genie, None, {
        LocationNames.loc_level_boss_plane_genie_secret: LRule(lr.lrule_plane_shrink),
    }),
    LevelLocRuleData(LocationNames.level_boss_sallystageplay, None, {
        LocationNames.loc_level_boss_sallystageplay_secret: LRule(lr.lrule_sallystageplay_secret),
        LocationNames.loc_level_boss_sallystageplay_dlc_chaliced: LRule(lr.lrule_dlc_boss_chaliced_parry),
        LocationNames.loc_level_boss_sallystageplay_event_dlc_chaliced: LRule(lr.lrule_dlc_boss_chaliced_parry),
    }),
]

level_loc_rules_boss_final: list[LevelLocRuleData] = [
    LevelLocRuleData(LocationNames.level_boss_devil, lr.lrule_parry_or_psugar, {
        LocationNames.loc_level_boss_devil_dlc_chaliced: LRule(lr.lrule_dlc_boss_chaliced_parry),
        LocationNames.loc_level_boss_devil_event_dlc_chaliced: LRule(lr.lrule_dlc_boss_chaliced_parry),
    }),
]

level_loc_rules_dlc_boss: list[LevelLocRuleData] = [
    LevelLocRuleData(LocationNames.level_dlc_boss_oldman, None, {
        LocationNames.loc_level_dlc_boss_oldman_dlc_chaliced: LRule(lr.lrule_dlc_boss_chaliced_parry),
        LocationNames.loc_level_dlc_boss_oldman_event_dlc_chaliced: LRule(lr.lrule_dlc_boss_chaliced_parry)
    }),
    LevelLocRuleData(LocationNames.level_dlc_boss_rumrunners, None, {
        LocationNames.loc_level_dlc_boss_rumrunners_dlc_chaliced: LRule(lr.lrule_dlc_boss_chaliced_parry),
        LocationNames.loc_level_dlc_boss_rumrunners_event_dlc_chaliced: LRule(lr.lrule_dlc_boss_chaliced_parry)
    }),
]

level_loc_rules_dlc_boss_final: list[LevelLocRuleData] = [
    LevelLocRuleData(LocationNames.level_dlc_boss_saltbaker, None, {
        LocationNames.loc_level_dlc_boss_saltbaker_dlc_chaliced: LRule(
            lr.lrule_and(lr.lrule_dlc_boss_chaliced_parry, lr.lrule_dlc_doublejump)
        ),
        LocationNames.loc_level_dlc_boss_saltbaker_event_dlc_chaliced: LRule(
            lr.lrule_and(lr.lrule_dlc_boss_chaliced_parry, lr.lrule_dlc_doublejump)
        )
    }),
]

level_loc_rules_rungun: list[LevelLocRuleData] = [
    LevelLocRuleData(LocationNames.level_rungun_forest, lr.lrule_dash, {
        LocationNames.loc_level_rungun_forest_coin1: LRule(lr.lrule_none),
        LocationNames.loc_level_rungun_forest_coin2: LRule(lr.lrule_none),
        LocationNames.loc_level_rungun_forest_coin3: LRule(lr.lrule_parry),
        LocationNames.loc_level_rungun_forest_coin4: LRule(lr.lrule_dash),
        LocationNames.loc_level_rungun_forest_coin5: LRule(lr.lrule_dash),
        LocationNames.loc_level_rungun_forest_agrade: LRule(
            lr.lrule_rungun_topgrade, LevelRuleModes.INHERIT
        ),
        #LocationNames.loc_level_rungun_forest_pacifist: LRule(lr.lrule_none, LevelRuleModes.INHERIT),
        LocationNames.loc_level_rungun_forest_dlc_chaliced: LRule(
            lr.lrule_dlc_rungun_chaliced, LevelRuleModes.INHERIT
        ),
    }),
    LevelLocRuleData(LocationNames.level_rungun_tree, lr.lrule_dash, {
        LocationNames.loc_level_rungun_tree_coin1: LRule(lr.lrule_parry),
        LocationNames.loc_level_rungun_tree_coin2: LRule(lr.lrule_none),
        LocationNames.loc_level_rungun_tree_coin3: LRule(lr.lrule_none),
        LocationNames.loc_level_rungun_tree_coin4: LRule(lr.lrule_dash),
        LocationNames.loc_level_rungun_tree_coin5: LRule(lr.lrule_dash),
        LocationNames.loc_level_rungun_tree_agrade: LRule(
            lr.lrule_rungun_topgrade, LevelRuleModes.INHERIT
        ),
        #LocationNames.loc_level_rungun_tree_pacifist: LRule(lr.lrule_none, LevelRuleModes.INHERIT),
        LocationNames.loc_level_rungun_tree_dlc_chaliced: LRule(
            lr.lrule_dlc_rungun_chaliced, LevelRuleModes.INHERIT
        ),
    }),
    LevelLocRuleData(LocationNames.level_rungun_circus, lr.lrule_parry_or_psugar, {
        LocationNames.loc_level_rungun_circus_coin1: LRule(lr.lrule_none),
        LocationNames.loc_level_rungun_circus_coin2: LRule(lr.lrule_none),
        LocationNames.loc_level_rungun_circus_coin3: LRule(lr.lrule_parry_or_psugar),
        LocationNames.loc_level_rungun_circus_coin4: LRule(lr.lrule_parry_or_psugar),
        LocationNames.loc_level_rungun_circus_coin5: LRule(lr.lrule_parry_or_psugar),
        LocationNames.loc_level_rungun_circus_agrade: LRule(
            lr.lrule_rungun_topgrade, LevelRuleModes.INHERIT
        ),
        #LocationNames.loc_level_rungun_circus_pacifist: LRule(lr.lrule_none, LevelRuleModes.INHERIT),
        LocationNames.loc_level_rungun_circus_dlc_chaliced: LRule(lr.lrule_dlc_rungun_chaliced),
    }),
    LevelLocRuleData(LocationNames.level_rungun_funhouse, lr.lrule_funhouse, {
        LocationNames.loc_level_rungun_funhouse_coin1: LRule(lr.lrule_parry_or_psugar),
        LocationNames.loc_level_rungun_funhouse_coin2: LRule(lr.lrule_parry_or_psugar),
        LocationNames.loc_level_rungun_funhouse_coin3: LRule(lr.lrule_parry_or_psugar),
        LocationNames.loc_level_rungun_funhouse_coin4: LRule(lr.lrule_parry_or_psugar),
        LocationNames.loc_level_rungun_funhouse_coin5: LRule(lr.lrule_funhouse),
        LocationNames.loc_level_rungun_funhouse_agrade: LRule(
            lr.lrule_rungun_topgrade, LevelRuleModes.INHERIT
        ),
        #LocationNames.loc_level_rungun_funhouse_pacifist: LRule(lr.lrule_none, LevelRuleModes.INHERIT),
        LocationNames.loc_level_rungun_funhouse_dlc_chaliced: LRule(
            lr.lrule_dlc_rungun_chaliced, LevelRuleModes.INHERIT
        ),
    }),
    LevelLocRuleData(LocationNames.level_rungun_harbour, lr.lrule_harbour, {
        LocationNames.loc_level_rungun_harbour_coin1: LRule(lr.lrule_dash_parry_or_psugar),
        LocationNames.loc_level_rungun_harbour_coin2: LRule(lr.lrule_none),
        LocationNames.loc_level_rungun_harbour_coin3: LRule(lr.lrule_parry_or_psugar),
        LocationNames.loc_level_rungun_harbour_coin4: LRule(
            lr.lrule_or(lr.lrule_parry, lr.lrule_and(lr.lrule_psugar, lr.lrule_dash))
        ),
        LocationNames.loc_level_rungun_harbour_coin5: LRule(lr.lrule_harbour),
        LocationNames.loc_level_rungun_harbour_agrade: LRule(
            lr.lrule_rungun_topgrade, LevelRuleModes.INHERIT
        ),
        #LocationNames.loc_level_rungun_harbour_pacifist: LRule(lr.lrule_none, LevelRuleModes.INHERIT),
        LocationNames.loc_level_rungun_harbour_dlc_chaliced: LRule(
            lr.lrule_dlc_rungun_chaliced, LevelRuleModes.INHERIT
        ),
    }),
    LevelLocRuleData(LocationNames.level_rungun_mountain, lr.lrule_dash_or_dlc_doublejump, {
        LocationNames.loc_level_rungun_mountain_coin1: LRule(lr.lrule_none),
        LocationNames.loc_level_rungun_mountain_coin2: LRule(lr.lrule_dash_or_dlc_doublejump),
        LocationNames.loc_level_rungun_mountain_coin3: LRule(lr.lrule_none),
        LocationNames.loc_level_rungun_mountain_coin4: LRule(lr.lrule_none),
        LocationNames.loc_level_rungun_mountain_coin5: LRule(lr.lrule_dash_or_dlc_doublejump),
        LocationNames.loc_level_rungun_mountain_agrade: LRule(
            lr.lrule_rungun_topgrade, LevelRuleModes.INHERIT
        ),
        #LocationNames.loc_level_rungun_mountain_pacifist: LRule(lr.lrule_none, LevelRuleModes.INHERIT),
        LocationNames.loc_level_rungun_mountain_dlc_chaliced: LRule(
            lr.lrule_dlc_rungun_chaliced, LevelRuleModes.INHERIT
        ),
    }),
]

level_loc_rules_dlc_tutorial: list[LevelLocRuleData] = [
    LevelLocRuleData(LocationNames.level_dlc_tutorial, lr.lrule_dlc_cookie, {
        LocationNames.loc_level_dlc_tutorial: LRule(lr.lrule_none),
        LocationNames.loc_level_dlc_tutorial_coin: LRule(lr.lrule_dlc_tutorial_coin),
    }),
]

level_loc_rules_dlc_chesscastle: list[LevelLocRuleData] = [
    LevelLocRuleData(LocationNames.level_dlc_chesscastle_pawn, None, {
        LocationNames.loc_level_dlc_chesscastle_pawn_dlc_chaliced: LRule(lr.lrule_dash_and_parry)
    }),
    LevelLocRuleData(LocationNames.level_dlc_chesscastle_knight, None, {
        LocationNames.loc_level_dlc_chesscastle_knight_dlc_chaliced: LRule(lr.lrule_dash_and_parry)
    }),
    LevelLocRuleData(LocationNames.level_dlc_chesscastle_bishop, None, {
        LocationNames.loc_level_dlc_chesscastle_bishop_dlc_chaliced: LRule(lr.lrule_dash_and_parry)
    }),
    LevelLocRuleData(LocationNames.level_dlc_chesscastle_rook, None, {
        LocationNames.loc_level_dlc_chesscastle_rook_dlc_chaliced: LRule(lr.lrule_dash_and_parry)
    }),
    LevelLocRuleData(LocationNames.level_dlc_chesscastle_queen, None, {
        LocationNames.loc_level_dlc_chesscastle_queen_dlc_chaliced: LRule(lr.lrule_dash_and_parry)
    }),
    LevelLocRuleData(LocationNames.level_dlc_chesscastle_run, None, {
        LocationNames.loc_level_dlc_chesscastle_run_dlc_chaliced: LRule(lr.lrule_dash_and_parry)
    })
]

level_loc_rules: list[LevelLocRuleData] = [
    *level_loc_rules_boss,
    *level_loc_rules_boss_final,
    *level_loc_rules_dlc_boss,
    *level_loc_rules_dlc_boss_final,
    *level_loc_rules_rungun,
    *level_loc_rules_dlc_tutorial,
    *level_loc_rules_dlc_chesscastle,
]
