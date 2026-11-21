from ...core.rule_builder.rule_import import And, Has, Or, True_
from ...options import (
    OracleOfSeasonsIncludeSecretLocations,
)
from ..regions import RegionName
from ..transition_type import TransitionType
from . import LogicLine
from .logic_predicates import (
    oos_can_break_sign,
    oos_can_buy_market,
    oos_can_date_rosa,
    oos_can_jump_1_wide_liquid,
    oos_can_jump_1_wide_pit,
    oos_can_jump_2_wide_liquid,
    oos_can_jump_2_wide_pit,
    oos_can_jump_3_wide_liquid,
    oos_can_jump_3_wide_pit,
    oos_can_jump_4_wide_liquid,
    oos_can_jump_4_wide_pit,
    oos_can_trigger_far_switch,
    oos_can_use_pegasus_seeds,
    oos_has_bombs,
    oos_has_bombs_for_bombjump,
    oos_has_bracelet,
    oos_has_ember_seeds,
    oos_has_feather,
    oos_has_magic_boomerang,
    oos_has_magnet_gloves,
    oos_has_seed_thrower,
    oos_has_shield,
    oos_has_shovel,
    oos_has_switch_hook,
    oos_option_hard_logic,
    oos_option_hell_logic,
    oos_option_medium_logic,
    oos_self_locking_item,
)
from .rulebuilder import OoSCanReachRegion, from_option


def make_subrosia_logic() -> list[LogicLine]:
    return [
        # Portals ###############################################################
        (RegionName.eastern_suburbs_portal, RegionName.volcanoes_east_portal, TransitionType.PORTAL, True_()),
        (RegionName.spool_swamp_portal, RegionName.subrosia_market_portal, TransitionType.PORTAL, True_()),
        (RegionName.mt_cucco_portal, RegionName.strange_brothers_portal, TransitionType.PORTAL, True_()),
        (RegionName.horon_village_portal, RegionName.house_of_pirates_portal, TransitionType.PORTAL, True_()),
        (RegionName.eyeglass_lake_portal, RegionName.great_furnace_portal, TransitionType.PORTAL, True_()),
        (RegionName.temple_remains_lower_portal, RegionName.volcanoes_west_portal, TransitionType.PORTAL, True_()),
        (RegionName.temple_remains_upper_portal, RegionName.d8_entrance_portal, TransitionType.PORTAL, True_()),
        (RegionName.volcanoes_east_portal, RegionName.subrosia_temple_sector, TransitionType.BASIC_TWO_WAY, True_()),
        (RegionName.subrosia_market_portal, RegionName.subrosia_market_sector, TransitionType.BASIC_TWO_WAY, True_()),
        (
            RegionName.strange_brothers_portal,
            RegionName.subrosia_hide_and_seek_sector,
            TransitionType.BASIC_TWO_WAY,
            oos_has_feather(),
        ),
        (RegionName.house_of_pirates_portal, RegionName.subrosia_pirates_sector, TransitionType.BASIC_TWO_WAY, True_()),
        (RegionName.great_furnace_portal, RegionName.subrosia_furnace_sector, TransitionType.BASIC_TWO_WAY, True_()),
        (RegionName.volcanoes_west_portal, RegionName.subrosia_volcano_sector, TransitionType.BASIC_TWO_WAY, True_()),
        (RegionName.d8_entrance_portal, RegionName.d8_entrance, TransitionType.BASIC_TWO_WAY, True_()),
        (RegionName.d8_entrance, RegionName.enter_d8, TransitionType.DUNGEON, True_()),
        (RegionName.pirates_after_bell, RegionName.western_coast_after_ship, TransitionType.BASIC_ONE_WAY, True_()),
        # Regions ###############################################################
        (
            RegionName.subrosia_temple_sector,
            RegionName.subrosia_market_sector,
            TransitionType.BASIC_ONE_WAY,
            oos_can_jump_1_wide_liquid(False),
        ),
        (
            RegionName.subrosia_market_sector,
            RegionName.subrosia_temple_sector,
            TransitionType.BASIC_ONE_WAY,
            Or(oos_can_date_rosa(), oos_can_jump_1_wide_liquid(False)),
        ),
        (
            RegionName.subrosia_market_sector,
            RegionName.subrosia_east_junction,
            TransitionType.BASIC_ONE_WAY,
            Or(
                oos_has_magnet_gloves(),
                # As it is a "diagonal" pit, it is considered as a 3.5-wide pit
                oos_can_jump_3_wide_liquid(),
                And(
                    # It's very tight, but a good jump clears the hole
                    oos_option_hard_logic(),  # Maybe upgrade to hell if too many complain
                    oos_can_jump_3_wide_pit(),
                ),
            ),
        ),
        (
            RegionName.subrosia_east_junction,
            RegionName.subrosia_market_sector,
            TransitionType.BASIC_ONE_WAY,
            Or(
                # This backwards route adds itself on top of the two-way route right above this one, adding the option
                # to remove the rock using the bracelet to turn this pit into a 2-wide jump
                And(oos_has_bracelet(), oos_can_jump_2_wide_pit()),
                oos_has_magnet_gloves(),
                # As it is a "diagonal" pit, it is considered as a 3.5-wide pit
                oos_can_jump_3_wide_liquid(
                    allow_bombchus=True
                ),  # bombjump could deserve an upgrade but isn't quite worth a hell classification
            ),
        ),
        (
            RegionName.subrosia_temple_sector,
            RegionName.subrosia_bridge_sector,
            TransitionType.BASIC_TWO_WAY,
            oos_has_feather(),
        ),
        (
            RegionName.subrosia_volcano_sector,
            RegionName.subrosia_bridge_sector,
            TransitionType.BASIC_ONE_WAY,
            And(oos_has_bracelet(), oos_can_jump_3_wide_liquid(allow_bombchus=True)),
        ),
        (
            RegionName.subrosia_volcano_sector,
            RegionName.bomb_temple_remains,
            TransitionType.BASIC_ONE_WAY,
            oos_has_bombs(),
        ),
        (
            RegionName.subrosia_hide_and_seek_sector,
            RegionName.subrosia_market_sector,
            TransitionType.BASIC_ONE_WAY,
            And(
                oos_has_bracelet(),
                oos_has_feather(),
                Or(oos_can_jump_2_wide_liquid(allow_bombchus=True), oos_has_magnet_gloves()),
            ),
        ),
        (
            RegionName.subrosia_market_sector,
            RegionName.subrosia_hide_and_seek_sector,
            TransitionType.BASIC_ONE_WAY,
            And(
                # H&S skip, with bracelet : https://youtu.be/lH1yvshG3LE
                # H&S skip, without bracelet : https://youtube.com/clip/Ugkx6EcYk0akEEgfO1SuhSfAO3Px5KCTtUKD
                oos_option_hell_logic(),
                oos_has_feather(),
                oos_can_use_pegasus_seeds(),
                oos_has_bombs_for_bombjump(),
                # Old H&S skip doesn't require bracelet
            ),
        ),
        (
            RegionName.subrosia_hide_and_seek_sector,
            RegionName.subrosia_temple_sector,
            TransitionType.BASIC_TWO_WAY,
            oos_can_jump_4_wide_liquid(allow_bombchus=True),
        ),
        (
            RegionName.subrosia_hide_and_seek_sector,
            RegionName.subrosia_pirates_sector,
            TransitionType.BASIC_TWO_WAY,
            oos_has_feather(),
        ),
        (
            RegionName.subrosia_east_junction,
            RegionName.subrosia_furnace_sector,
            TransitionType.BASIC_ONE_WAY,
            oos_has_feather(),
        ),
        (
            RegionName.subrosia_furnace_sector,
            RegionName.subrosia_east_junction,
            TransitionType.BASIC_ONE_WAY,
            Or(oos_has_feather(), And(oos_option_medium_logic(), oos_has_switch_hook())),
        ),
        # Locations ###############################################################
        (RegionName.subrosia_temple_sector, RegionName.subrosian_dance_hall, TransitionType.BASIC_ONE_WAY, True_()),
        (RegionName.subrosia_temple_sector, RegionName.reach_sign, TransitionType.BASIC_ONE_WAY, True_()),
        (
            RegionName.subrosia_temple_sector,
            RegionName.subrosian_smithy_ore,
            TransitionType.BASIC_ONE_WAY,
            Or(Has("Hard Ore"), oos_self_locking_item("Subrosia: Smithy Hard Ore Reforge", "Hard Ore")),
        ),
        (
            RegionName.subrosia_temple_sector,
            RegionName.subrosian_smithy_bell,
            TransitionType.BASIC_ONE_WAY,
            Or(Has("Rusty Bell"), oos_self_locking_item("Subrosia: Smithy Rusty Bell Reforge", "Rusty Bell")),
        ),
        (
            RegionName.subrosia_temple_sector,
            RegionName.smith_secret,
            TransitionType.BASIC_ONE_WAY,
            And(
                from_option(OracleOfSeasonsIncludeSecretLocations, OracleOfSeasonsIncludeSecretLocations.option_true),
                oos_has_shield(),
            ),
        ),
        (RegionName.subrosia_temple_sector, RegionName.temple_of_seasons, TransitionType.BASIC_ONE_WAY, True_()),
        (
            RegionName.subrosia_temple_sector,
            RegionName.tower_of_winter,
            TransitionType.BASIC_ONE_WAY,
            Or(oos_has_feather(), oos_can_trigger_far_switch()),
        ),
        (
            RegionName.subrosia_temple_sector,
            RegionName.tower_of_summer,
            TransitionType.BASIC_ONE_WAY,
            And(
                oos_can_date_rosa(),
                oos_has_bracelet(),
            ),
        ),
        (
            RegionName.subrosia_temple_sector,
            RegionName.tower_of_autumn,
            TransitionType.BASIC_ONE_WAY,
            And(oos_has_feather(), Has("Bomb Flower")),
        ),
        (
            RegionName.subrosia_temple_sector,
            RegionName.subrosian_secret,
            TransitionType.BASIC_ONE_WAY,
            And(
                from_option(OracleOfSeasonsIncludeSecretLocations, OracleOfSeasonsIncludeSecretLocations.option_true),
                oos_can_jump_1_wide_pit(False),
                oos_has_magic_boomerang(),
            ),
        ),
        (RegionName.subrosia_market_sector, RegionName.reach_sign, TransitionType.BASIC_ONE_WAY, True_()),
        (
            RegionName.subrosia_market_sector,
            RegionName.subrosia_seaside,
            TransitionType.BASIC_ONE_WAY,
            oos_has_shovel(),
        ),
        (
            RegionName.subrosia_market_sector,
            RegionName.subrosia_market_star_ore,
            TransitionType.BASIC_ONE_WAY,
            Or(Has("Star Ore"), oos_self_locking_item("Subrosia: Market #1", "Star Ore")),
        ),
        (
            RegionName.subrosia_market_sector,
            RegionName.subrosia_market_ore_chunks,
            TransitionType.BASIC_ONE_WAY,
            oos_can_buy_market(),
        ),
        (
            RegionName.subrosia_hide_and_seek_sector,
            RegionName.subrosia_hide_and_seek,
            TransitionType.BASIC_ONE_WAY,
            oos_has_shovel(),
        ),
        (
            RegionName.subrosia_hide_and_seek_sector,
            RegionName.tower_of_spring,
            TransitionType.BASIC_ONE_WAY,
            oos_has_feather(),
        ),
        (
            RegionName.subrosia_hide_and_seek_sector,
            RegionName.subrosian_wilds_chest,
            TransitionType.BASIC_ONE_WAY,
            And(oos_has_feather(), Or(oos_has_magnet_gloves(), oos_can_jump_4_wide_pit())),
        ),
        (
            RegionName.subrosian_wilds_chest,
            RegionName.subrosian_wilds_digging_spot,
            TransitionType.BASIC_ONE_WAY,
            And(Or(oos_can_jump_3_wide_pit(), oos_has_magnet_gloves()), oos_has_feather(), oos_has_shovel()),
        ),
        (
            RegionName.subrosia_hide_and_seek_sector,
            RegionName.subrosian_house,
            TransitionType.BASIC_ONE_WAY,
            oos_has_feather(),
        ),
        (
            RegionName.subrosia_hide_and_seek_sector,
            RegionName.subrosian_2d_cave,
            TransitionType.BASIC_ONE_WAY,
            oos_has_feather(),
        ),
        (RegionName.subrosia_bridge_sector, RegionName.subrosia_open_cave, TransitionType.BASIC_ONE_WAY, True_()),
        (
            RegionName.subrosia_bridge_sector,
            RegionName.subrosia_locked_cave,
            TransitionType.BASIC_ONE_WAY,
            And(oos_can_date_rosa(), oos_has_feather()),
        ),
        (
            RegionName.subrosia_bridge_sector,
            RegionName.subrosian_chef_trade,
            TransitionType.BASIC_ONE_WAY,
            Or(Has("Iron Pot"), oos_self_locking_item("Subrosia: Subrosian Chef Trade", "Iron Pot")),
        ),
        (
            RegionName.subrosia_east_junction,
            RegionName.subrosia_village_chest,
            TransitionType.BASIC_ONE_WAY,
            Or(
                oos_has_magnet_gloves(),
                oos_can_jump_4_wide_pit(),
                And(
                    # early red ore : https://youtu.be/fB10dV2Gunk
                    oos_option_hell_logic(),
                    oos_has_feather(),
                    oos_can_use_pegasus_seeds(),
                    oos_has_bombs_for_bombjump(),
                ),
            ),
        ),
        (
            RegionName.subrosia_furnace_sector,
            RegionName.great_furnace,
            TransitionType.BASIC_ONE_WAY,
            And(
                OoSCanReachRegion(RegionName.tower_of_autumn),
                Or(Has("Red Ore"), oos_self_locking_item("Subrosia: Item Smelted in Great Furnace", "Red Ore")),
                Or(Has("Blue Ore"), oos_self_locking_item("Subrosia: Item Smelted in Great Furnace", "Blue Ore")),
            ),
        ),
        (
            RegionName.subrosia_east_junction,
            RegionName.reach_sign,
            TransitionType.BASIC_ONE_WAY,
            True_(),
        ),
        (RegionName.reach_sign, RegionName.break_sign, TransitionType.BASIC_ONE_WAY, oos_can_break_sign()),
        (
            RegionName.subrosia_furnace_sector,
            RegionName.subrosian_sign_guy,
            TransitionType.BASIC_ONE_WAY,
            OoSCanReachRegion(RegionName.break_sign),
        ),
        (
            RegionName.subrosia_furnace_sector,
            RegionName.subrosian_buried_bomb_flower,
            TransitionType.BASIC_ONE_WAY,
            And(oos_has_feather(), oos_has_bracelet()),
        ),
        (
            RegionName.subrosia_furnace_sector,
            RegionName.break_sign,
            TransitionType.BASIC_ONE_WAY,
            # Throw an ember on the sign in east junction. Switch hook is already used to get there
            And(oos_option_medium_logic(), oos_has_ember_seeds(), oos_has_seed_thrower()),
        ),
        (
            RegionName.subrosia_temple_sector,
            RegionName.subrosia_temple_digging_spot,
            TransitionType.BASIC_ONE_WAY,
            oos_has_shovel(),
        ),
        (
            RegionName.subrosia_temple_sector,
            RegionName.subrosia_bath_digging_spot,
            TransitionType.BASIC_ONE_WAY,
            And(
                oos_can_jump_1_wide_pit(False),
                Or(oos_can_jump_3_wide_liquid(allow_bombchus=True), oos_has_magnet_gloves()),
                oos_has_shovel(),
            ),
        ),
        (
            RegionName.subrosia_market_sector,
            RegionName.subrosia_market_digging_spot,
            TransitionType.BASIC_ONE_WAY,
            oos_has_shovel(),
        ),
        (
            RegionName.subrosia_bridge_sector,
            RegionName.subrosia_bridge_digging_spot,
            TransitionType.BASIC_ONE_WAY,
            oos_has_shovel(),
        ),
        (
            RegionName.subrosia_pirates_sector,
            RegionName.pirates_after_bell,
            TransitionType.BASIC_ONE_WAY,
            Has("Pirate's Bell"),
        ),
    ]
