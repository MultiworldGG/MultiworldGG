from ...core.rule_builder.rule_import import And, Has, Or, True_
from ...options import (
    OracleOfSeasonsBusinessScrubsShuffle,
    OracleOfSeasonsOptions,
)
from ...world import OracleOfSeasonsWorld
from ..items import ItemName
from ..regions import RegionName
from ..transition_type import TransitionType
from . import LogicLine
from .boss_logic import CanBeatBoss
from .logic_predicates import (
    oos_can_break_bush,
    oos_can_break_crystal,
    oos_can_break_pot,
    oos_can_complete_d11_puzzle,
    oos_can_flip_spiked_beetle,
    oos_can_harvest_regrowing_bush,
    oos_can_jump_1_wide_pit,
    oos_can_jump_2_wide_liquid,
    oos_can_jump_2_wide_pit,
    oos_can_jump_3_wide_liquid,
    oos_can_jump_3_wide_pit,
    oos_can_jump_4_wide_pit,
    oos_can_jump_5_wide_liquid,
    oos_can_jump_5_wide_pit,
    oos_can_jump_6_wide_liquid,
    oos_can_jump_6_wide_pit,
    oos_can_kill_armored_enemy,
    oos_can_kill_d2_far_moblin,
    oos_can_kill_d2_hardhat,
    oos_can_kill_facade,
    oos_can_kill_magunesu,
    oos_can_kill_moldorm,
    oos_can_kill_normal_enemy,
    oos_can_kill_normal_enemy_no_cane,
    oos_can_kill_spiked_beetle,
    oos_can_kill_stalfos,
    oos_can_kill_vire,
    oos_can_push_enemy,
    oos_can_remove_rockslide,
    oos_can_swim,
    oos_can_trigger_lever,
    oos_can_trigger_lever_from_minecart,
    oos_can_use_ember_seeds,
    oos_can_use_gale_seeds_offensively,
    oos_can_use_mystery_seeds,
    oos_can_use_pegasus_seeds,
    oos_can_use_scent_seeds,
    oos_has_biggoron_sword,
    oos_has_bombchus_for_bombjump,
    oos_has_bombchus_for_tiles,
    oos_has_bombchus_to_fight,
    oos_has_bombs,
    oos_has_bombs_for_bombjump,
    oos_has_bombs_for_tiles,
    oos_has_bombs_to_fight,
    oos_has_boomerang,
    oos_has_boss_key,
    oos_has_bracelet,
    oos_has_cane,
    oos_has_cape,
    oos_has_ember_seeds,
    oos_has_feather,
    oos_has_flippers,
    oos_has_flute,
    oos_has_fools_ore,
    oos_has_gale_seeds,
    oos_has_hearts,
    oos_has_hearts_by_difficulty,
    oos_has_hyper_slingshot,
    oos_has_magic_boomerang,
    oos_has_magnet_gloves,
    oos_has_mystery_seeds,
    oos_has_noble_sword,
    oos_has_rod,
    oos_has_rupees_for_shop,
    oos_has_satchel,
    oos_has_scent_seeds,
    oos_has_seed_thrower,
    oos_has_shield,
    oos_has_shooter,
    oos_has_shovel,
    oos_has_slingshot,
    oos_has_small_keys,
    oos_has_switch_hook,
    oos_has_sword,
    oos_has_tight_switch_hook,
    oos_has_unlock,
    oos_option_hard_logic,
    oos_option_hell_logic,
    oos_option_medium_logic,
    oos_option_no_d0_alt_entrance,
    oos_self_locking_item,
    oos_self_locking_small_key,
    oos_shoot_beams,
)
from .rulebuilder import OoSCanReachRegion, from_option, from_world_field


def make_d0_logic() -> list[LogicLine]:
    return [
        # 0 keys
        (RegionName.enter_d0, RegionName.d0_key_chest, TransitionType.BASIC_ONE_WAY, True_()),
        (
            RegionName.enter_d0,
            RegionName.d0_rupee_chest,
            TransitionType.BASIC_ONE_WAY,
            # If hole is removed, stairs are added inside dungeon to make the chest reachable
            oos_option_no_d0_alt_entrance(),
        ),
        (RegionName.d0_rupee_chest, RegionName.enter_d0, TransitionType.BASIC_ONE_WAY, True_()),
        (
            RegionName.enter_d0,
            RegionName.d0_hidden_2d_section,
            TransitionType.BASIC_ONE_WAY,
            Or(oos_can_kill_normal_enemy(), oos_has_boomerang(), oos_has_switch_hook()),
        ),
        # 1 key
        (
            RegionName.enter_d0,
            RegionName.d0_sword_chest,
            TransitionType.BASIC_ONE_WAY,
            Or(
                oos_has_small_keys(0, 1, keylock_name=ItemName.heros_cave_keydoor_unlock),
                oos_self_locking_small_key("Hero's Cave: Final Chest", 0),
                oos_self_locking_item("Hero's Cave: Final Chest", "Master Key (Hero's Cave)"),
            ),
        ),
    ]


def make_d1_logic() -> list[LogicLine]:
    return [
        # 0 keys
        (
            RegionName.enter_d1,
            RegionName.d1_stalfos_drop,
            TransitionType.BASIC_ONE_WAY,
            Or(
                oos_can_kill_stalfos(),
                And(
                    # Medium logic expects the player to be able to use bushes
                    oos_option_medium_logic(),
                    oos_has_bracelet(),
                ),
            ),
        ),
        (
            RegionName.enter_d1,
            RegionName.d1_floormaster_room,
            TransitionType.BASIC_ONE_WAY,
            oos_can_use_ember_seeds(True),
        ),
        (
            RegionName.d1_floormaster_room,
            RegionName.d1_boss,
            TransitionType.BASIC_ONE_WAY,
            And(oos_has_boss_key(1), CanBeatBoss(1)),
        ),
        # 1 key
        (
            RegionName.enter_d1,
            RegionName.d1_stalfos_chest,
            TransitionType.BASIC_ONE_WAY,
            And(
                oos_has_small_keys(1, 1, keylock_name=ItemName.gnarled_root_dungeon_keydoor_left_of_entrance_unlock),
                oos_can_kill_stalfos(),
            ),
        ),
        (
            RegionName.d1_stalfos_chest,
            RegionName.d1_goriya_chest,
            TransitionType.BASIC_ONE_WAY,
            And(oos_can_use_ember_seeds(True), oos_can_kill_normal_enemy(True)),
        ),
        (RegionName.d1_stalfos_chest, RegionName.d1_lever_room, TransitionType.BASIC_ONE_WAY, True_()),
        (
            RegionName.d1_stalfos_chest,
            RegionName.d1_block_pushing_room,
            TransitionType.BASIC_ONE_WAY,
            Or(oos_can_kill_normal_enemy(), And(oos_option_hard_logic(), oos_has_bracelet())),
        ),
        (
            RegionName.d1_stalfos_chest,
            RegionName.d1_railway_chest,
            TransitionType.BASIC_ONE_WAY,
            Or(oos_can_trigger_lever(), And(oos_option_hard_logic(), oos_has_bracelet())),
        ),
        (RegionName.d1_railway_chest, RegionName.d1_button_chest, TransitionType.BASIC_ONE_WAY, True_()),
        # 2 keys
        (
            RegionName.d1_railway_chest,
            RegionName.d1_basement,
            TransitionType.BASIC_ONE_WAY,
            Or(
                oos_self_locking_small_key("Gnarled Root Dungeon: Item in Basement", 1),
                And(
                    oos_can_remove_rockslide(False),
                    oos_has_small_keys(1, 2, keylock_name=ItemName.gnarled_root_dungeon_miniboss_keydoor_unlock),
                    oos_can_kill_armored_enemy(False, True),
                ),
            ),
        ),
    ]


def make_d2_logic(world: OracleOfSeasonsWorld, options: OracleOfSeasonsOptions) -> list[LogicLine]:
    return [
        # 0 keys
        (
            RegionName.enter_d2,
            RegionName.d2_torch_room,
            # Do not allow for turning back if the dungeon is excluded
            TransitionType.BASIC_TWO_WAY
            if not options.exclude_dungeons_without_essence.value or "Gift of Time" in world.essences_in_game
            else TransitionType.BASIC_ONE_WAY,
            True_(),
        ),
        (RegionName.d2_torch_room, RegionName.d2_left_from_entrance, TransitionType.BASIC_ONE_WAY, True_()),
        (
            RegionName.d2_torch_room,
            RegionName.d2_rope_drop,
            TransitionType.BASIC_ONE_WAY,
            Or(oos_can_kill_normal_enemy(), oos_has_switch_hook()),
        ),
        (
            RegionName.d2_torch_room,
            RegionName.d2_arrow_room,
            TransitionType.BASIC_ONE_WAY,
            oos_can_use_ember_seeds(True),
        ),
        (RegionName.d2_arrow_room, RegionName.d2_torch_room, TransitionType.BASIC_ONE_WAY, oos_can_kill_normal_enemy()),
        (
            RegionName.d2_arrow_room,
            RegionName.d2_rupee_room,
            TransitionType.BASIC_ONE_WAY,
            oos_can_remove_rockslide(False),
        ),
        (
            RegionName.d2_arrow_room,
            RegionName.d2_rope_chest,
            TransitionType.BASIC_ONE_WAY,
            Or(oos_can_kill_normal_enemy(), oos_has_switch_hook()),
        ),
        (
            RegionName.d2_arrow_room,
            RegionName.d2_blade_chest,
            TransitionType.BASIC_ONE_WAY,
            oos_can_kill_normal_enemy(),
        ),
        (RegionName.d2_blade_chest, RegionName.d2_arrow_room, TransitionType.BASIC_ONE_WAY, True_()),  # Backwards path
        (RegionName.d2_blade_chest, RegionName.d2_alt_entrances, TransitionType.BASIC_TWO_WAY, oos_has_bracelet()),
        (
            RegionName.d2_blade_chest,
            RegionName.d2_roller_chest,
            TransitionType.BASIC_ONE_WAY,
            And(
                oos_can_remove_rockslide(False),
                oos_has_bracelet(),
            ),
        ),
        (
            RegionName.d2_alt_entrances,
            RegionName.d2_spiral_chest,
            TransitionType.BASIC_ONE_WAY,
            And(
                oos_can_break_bush(False, True),
                Or(
                    oos_has_bombs_for_tiles(),
                    And(
                        # It's tight but doable
                        oos_option_medium_logic(),
                        oos_can_use_pegasus_seeds(),
                        oos_has_bombchus_for_tiles(),
                    ),
                ),
            ),
        ),
        (
            RegionName.d2_alt_entrances,
            RegionName.d2_scrub,
            TransitionType.BASIC_ONE_WAY,
            And(
                from_option(OracleOfSeasonsBusinessScrubsShuffle, OracleOfSeasonsBusinessScrubsShuffle.option_true),
                oos_has_rupees_for_shop("d2Scrub"),
            ),
        ),
        # 2 keys
        (
            RegionName.d2_roller_chest,
            RegionName.d2_spinner,
            TransitionType.BASIC_ONE_WAY,
            And(
                oos_has_small_keys(2, 2, keylock_name=ItemName.snakes_remains_miniboss_keydoor_unlock),
                oos_can_kill_facade(),
            ),
        ),
        (
            RegionName.d2_spinner,
            RegionName.d2_wild_bombs,
            TransitionType.BASIC_ONE_WAY,
            And(
                Or(
                    oos_can_remove_rockslide(False),
                    oos_has_small_keys(
                        2, 3, ItemName.snakes_remains_spinner_keyblock_unlock
                    ),  # spin the spinner to access the pol's voice room
                ),
                Or(
                    oos_can_harvest_regrowing_bush(),
                    oos_has_bombs(),  # Bombs for more bombs is ok in any amount
                ),
            ),
        ),
        # You can take the Facade miniboss teleporter to reach dungeon entrance, even if you entered the dungeon
        # through the alt-entrance
        (RegionName.d2_spinner, RegionName.d2_torch_room, TransitionType.BASIC_ONE_WAY, True_()),
        (RegionName.d2_spinner, RegionName.dodongo_owl, TransitionType.BASIC_ONE_WAY, oos_can_use_mystery_seeds()),
        (
            RegionName.d2_spinner,
            RegionName.d2_boss,
            TransitionType.BASIC_ONE_WAY,
            And(
                Or(
                    oos_can_remove_rockslide(False),
                    oos_has_small_keys(2, 3, keylock_name=ItemName.snakes_remains_spinner_keyblock_unlock),
                ),
                oos_has_boss_key(2),
                CanBeatBoss(2),
            ),
        ),
        # 3 keys
        (
            RegionName.d2_arrow_room,
            RegionName.d2_hardhat_room,
            TransitionType.BASIC_ONE_WAY,
            oos_has_small_keys(2, 3, keylock_name=ItemName.snakes_remains_keydoor_to_hardhats_unlock),
        ),
        (RegionName.d2_hardhat_room, RegionName.d2_pot_chest, TransitionType.BASIC_ONE_WAY, oos_can_break_pot()),
        (
            RegionName.d2_hardhat_room,
            RegionName.d2_moblin_chest,
            TransitionType.BASIC_ONE_WAY,
            And(
                oos_can_kill_d2_hardhat(),
                Or(
                    oos_can_kill_d2_far_moblin(),
                    oos_can_harvest_regrowing_bush(),
                    oos_has_bombs(),  # Bombs for more bombs is ok in any amount
                ),
            ),
        ),
        (
            RegionName.d2_hardhat_room,
            RegionName.d2_wild_bombs,
            TransitionType.BASIC_ONE_WAY,
            And(oos_can_kill_d2_hardhat(), oos_can_harvest_regrowing_bush()),
        ),
        (
            RegionName.d2_spinner,
            RegionName.d2_terrace_chest,
            TransitionType.BASIC_ONE_WAY,
            oos_has_small_keys(2, 3, keylock_name=ItemName.snakes_remains_spinner_keyblock_unlock),
        ),
    ]


def make_d3_logic() -> list[LogicLine]:
    return [
        # 0 keys
        (RegionName.enter_d3, RegionName.spiked_beetles_owl, TransitionType.BASIC_ONE_WAY, oos_can_use_mystery_seeds()),
        (
            RegionName.enter_d3,
            RegionName.d3_center,
            TransitionType.BASIC_ONE_WAY,
            Or(
                oos_can_kill_spiked_beetle(),
                And(
                    # Break pots to refill mysteries, and use them on the beetles to gale them away
                    oos_option_medium_logic(),
                    oos_can_use_mystery_seeds(),
                    oos_can_break_pot(),
                ),
                And(oos_option_medium_logic(), oos_can_flip_spiked_beetle(), oos_has_bracelet()),
            ),
        ),
        (RegionName.d3_center, RegionName.d3_water_room, TransitionType.BASIC_ONE_WAY, oos_has_feather()),
        (
            RegionName.d3_center,
            RegionName.d3_mimic_stairs,
            TransitionType.BASIC_ONE_WAY,
            Or(oos_has_bracelet(), And(oos_can_break_pot(), oos_has_cane())),
        ),
        (
            RegionName.d3_center,
            RegionName.trampoline_owl,
            TransitionType.BASIC_ONE_WAY,
            And(oos_has_feather(), oos_can_use_mystery_seeds()),
        ),
        (RegionName.d3_center, RegionName.d3_trampoline_chest, TransitionType.BASIC_ONE_WAY, oos_has_feather()),
        (RegionName.d3_center, RegionName.d3_zol_chest, TransitionType.BASIC_ONE_WAY, oos_has_feather()),
        (RegionName.d3_mimic_stairs, RegionName.d3_water_room, TransitionType.BASIC_TWO_WAY, True_()),
        (RegionName.d3_mimic_stairs, RegionName.d3_roller_chest, TransitionType.BASIC_ONE_WAY, oos_has_bracelet()),
        (RegionName.d3_mimic_stairs, RegionName.d3_quicksand_terrace, TransitionType.BASIC_ONE_WAY, oos_has_feather()),
        (
            RegionName.d3_quicksand_terrace,
            RegionName.omuai_owl,
            TransitionType.BASIC_ONE_WAY,
            And(oos_can_use_mystery_seeds()),
        ),
        (RegionName.d3_mimic_stairs, RegionName.d3_moldorm_chest, TransitionType.BASIC_ONE_WAY, oos_can_kill_moldorm()),
        (
            RegionName.d3_mimic_stairs,
            RegionName.d3_bombed_wall_chest,
            TransitionType.BASIC_ONE_WAY,
            oos_can_remove_rockslide(False),
        ),
        # 2 keys
        (
            RegionName.d3_water_room,
            RegionName.d3_mimic_chest,
            TransitionType.BASIC_ONE_WAY,
            And(
                Or(
                    oos_has_small_keys(3, 2, ItemName.poison_moth_lair_keydoor_to_mimics_unlock),
                    oos_self_locking_small_key("Poison Moth's Lair (1F): Chest in Mimics Room", 3),
                ),
                oos_can_kill_normal_enemy(),
            ),
        ),
        (
            RegionName.d3_mimic_stairs,
            RegionName.d3_omuai_stairs,
            TransitionType.BASIC_ONE_WAY,
            And(
                Or(
                    oos_has_feather(),
                    # With switch hook, even with pegasus, you can barely see the pots, so it's not casual friendly
                    And(oos_option_medium_logic(), oos_has_switch_hook(2)),
                    And(oos_option_medium_logic(), oos_can_use_pegasus_seeds(), oos_has_switch_hook()),
                ),
                oos_has_small_keys(3, 2, ItemName.poison_moth_lair_miniboss_keydoor_unlock),
                oos_has_bracelet(),
                oos_can_kill_armored_enemy(False, False),
            ),
        ),
        (RegionName.d3_omuai_stairs, RegionName.d3_quicksand_terrace, TransitionType.BASIC_ONE_WAY, True_()),
        (
            RegionName.d3_omuai_stairs,
            RegionName.d3_giant_blade_room,
            TransitionType.BASIC_ONE_WAY,
            Or(oos_has_feather(), oos_option_hard_logic()),
        ),
        (
            RegionName.d3_omuai_stairs,
            RegionName.d3_boss,
            TransitionType.BASIC_ONE_WAY,
            And(oos_has_boss_key(3), Or(oos_has_feather(), oos_option_medium_logic()), CanBeatBoss(3)),
        ),
    ]


def make_d4_logic(options: OracleOfSeasonsOptions) -> list[LogicLine]:
    return [
        # 0 keys
        (
            RegionName.enter_d4,
            RegionName.d4_north_of_entrance,
            TransitionType.BASIC_ONE_WAY,
            Or(oos_has_flippers(), oos_has_cape()),
        ),
        (
            RegionName.d4_north_of_entrance,
            RegionName.d4_pot_puzzle,
            TransitionType.BASIC_ONE_WAY,
            And(oos_can_remove_rockslide(False), oos_has_bracelet()),
        ),
        (
            RegionName.d4_north_of_entrance,
            RegionName.d4_maze_chest,
            TransitionType.BASIC_ONE_WAY,
            Or(oos_can_trigger_lever_from_minecart(), And(oos_option_hard_logic(), oos_has_bracelet())),
        ),
        (RegionName.d4_maze_chest, RegionName.d4_dark_room, TransitionType.BASIC_ONE_WAY, oos_has_feather()),
        # 1 key
        (
            RegionName.enter_d4,
            RegionName.d4_water_ring_room,
            TransitionType.BASIC_ONE_WAY,
            And(
                oos_has_small_keys(4, 1, keylock_name=ItemName.dancing_dragon_dungeon_entrance_keydoor_unlock),
                Or(
                    oos_has_cape(),
                    And(
                        # Feather is required to jump above spike lines
                        oos_has_feather(),
                        oos_has_flippers(),
                    ),
                ),
                oos_can_remove_rockslide(False),
                Or(
                    oos_can_kill_normal_enemy(),
                    And(  # killing enemies with pots
                        oos_option_medium_logic(),
                        oos_has_bracelet(),
                    ),
                    And(  # pushing enemies in the water
                        oos_can_push_enemy(), Or(oos_has_boomerang(), oos_has_switch_hook())
                    ),
                ),
            ),
        ),
        (
            RegionName.enter_d4,
            RegionName.d4_roller_minecart,
            TransitionType.BASIC_ONE_WAY,
            And(
                oos_has_small_keys(4, 1, keylock_name=ItemName.dancing_dragon_dungeon_entrance_keydoor_unlock),
                oos_has_feather(),
                Or(
                    oos_has_flippers(),
                    And(
                        oos_option_hell_logic(),
                        oos_has_cape(),
                        oos_can_use_pegasus_seeds(),
                        oos_has_bombs_for_bombjump() | oos_has_bombchus_for_bombjump(),
                    ),
                ),
            ),
        ),
        (
            RegionName.d4_roller_minecart,
            RegionName.d4_pool,
            TransitionType.BASIC_ONE_WAY,
            And(
                Or(oos_has_flippers(), oos_option_medium_logic()),
                Or(
                    oos_can_kill_normal_enemy(),
                    And(oos_option_medium_logic(), oos_has_bracelet()),
                    And(oos_can_push_enemy(), oos_has_switch_hook()),
                ),
                Or(oos_can_trigger_lever_from_minecart(), And(oos_option_hard_logic(), oos_has_bracelet())),
            ),
        ),
        # 2 keys
        (
            RegionName.d4_roller_minecart,
            RegionName.greater_distance_owl,
            TransitionType.BASIC_ONE_WAY,
            And(
                oos_has_small_keys(4, 2, keylock_name=ItemName.dancing_dragon_dungeon_minecart_keyblock_unlock),
                oos_can_use_mystery_seeds(),
            ),
        ),
        (
            RegionName.d4_roller_minecart,
            RegionName.d4_stalfos_stairs,
            TransitionType.BASIC_ONE_WAY,
            And(
                oos_has_small_keys(4, 2, keylock_name=ItemName.dancing_dragon_dungeon_minecart_keyblock_unlock),
                Or(
                    oos_can_kill_stalfos(),
                    And(
                        # Kill Stalfos by using pots in the room
                        oos_option_medium_logic(),
                        oos_has_bracelet(),
                    ),
                ),
                oos_can_jump_2_wide_pit(),
            ),
        ),
        (RegionName.d4_stalfos_stairs, RegionName.d4_terrace, TransitionType.BASIC_ONE_WAY, True_()),
        (
            RegionName.d4_terrace,
            RegionName.d4_scrub,
            TransitionType.BASIC_ONE_WAY,
            And(
                from_option(OracleOfSeasonsBusinessScrubsShuffle, OracleOfSeasonsBusinessScrubsShuffle.option_true),
                oos_has_rupees_for_shop("d4Scrub"),
            ),
        ),
        (
            RegionName.d4_stalfos_stairs,
            RegionName.d4_torch_chest,
            TransitionType.BASIC_ONE_WAY,
            And(oos_has_seed_thrower(), oos_has_ember_seeds()),
        ),
        (RegionName.d4_stalfos_stairs, RegionName.d4_miniboss_room, TransitionType.BASIC_ONE_WAY, True_()),
        (
            RegionName.d4_miniboss_room,
            RegionName.d4_miniboss_room_wild_embers,
            TransitionType.BASIC_ONE_WAY,
            oos_can_harvest_regrowing_bush(),
        ),
        (
            RegionName.d4_miniboss_room,
            RegionName.d4_final_minecart,
            TransitionType.BASIC_ONE_WAY,
            And(oos_can_use_ember_seeds(False), oos_can_kill_armored_enemy(False, False)),
        ),
        # 5 keys
        (
            RegionName.d4_final_minecart,
            RegionName.d4_cracked_floor_room,
            TransitionType.BASIC_ONE_WAY,
            Or(
                oos_has_small_keys(4, 5, keylock_name=ItemName.dancing_dragon_dungeon_crumbling_floor_keydoor_unlock),
                oos_self_locking_small_key("Dancing Dragon Dungeon (1F): Crumbling Room Chest", 4),
            ),
        ),
        (
            RegionName.d4_final_minecart,
            RegionName.d4_dive_spot,
            TransitionType.BASIC_ONE_WAY,
            And(
                Or(
                    And(
                        Or(  # hit distant levers
                            oos_has_magic_boomerang(), oos_has_seed_thrower()
                        ),
                        # In medium, switch is also valid, but a feather is required to get there anyway
                        oos_can_jump_2_wide_pit(),
                        oos_has_small_keys(4, 5, keylock_name=ItemName.dancing_dragon_dungeon_pool_keyblock_unlock),
                    ),
                    # For self-locking, we don't need to check if the player is able to
                    # waste the key first to then get it back, only to get it back if they waste it
                    oos_self_locking_small_key("Dancing Dragon Dungeon (1F): Eye Diving Spot Item", 4),
                ),
                oos_has_flippers(),
            ),
        ),
        (
            RegionName.d4_final_minecart,
            RegionName.d4_basement_stairs,
            TransitionType.BASIC_ONE_WAY,
            And(
                oos_has_small_keys(4, 5, keylock_name=ItemName.dancing_dragon_dungeon_boss_keyblock_unlock),
                Or(oos_has_boomerang(), oos_has_seed_thrower(), oos_has_switch_hook(), oos_option_hard_logic()),
            ),
        ),
        (
            RegionName.d4_basement_stairs,
            RegionName.gohma_owl,
            TransitionType.BASIC_ONE_WAY,
            oos_can_use_mystery_seeds(),
        ),
        (
            RegionName.d4_basement_stairs,
            RegionName.enter_gohma,
            TransitionType.BASIC_ONE_WAY,
            And(
                oos_has_boss_key(4),
                Or(
                    And(oos_has_seed_thrower(), oos_can_use_ember_seeds(True)),
                    oos_can_jump_3_wide_pit(),
                    And(  # throw seeds using satchel during a jump
                        oos_option_hard_logic(), oos_has_feather(), oos_can_use_ember_seeds(False)
                    ),
                ),
            ),
        ),
        (RegionName.enter_gohma, RegionName.d4_boss, TransitionType.BASIC_ONE_WAY, CanBeatBoss(4)),
    ]


def make_d5_logic() -> list[LogicLine]:
    return [
        # 0 keys
        (
            RegionName.enter_d5,
            RegionName.d5_left_chest,
            TransitionType.BASIC_ONE_WAY,
            Or(
                oos_has_magnet_gloves(),
                oos_has_cape(),
                And(
                    # Tight bomb jump to reach the chest
                    oos_option_hell_logic(),
                    oos_can_jump_3_wide_liquid(),
                ),
            ),
        ),
        (
            RegionName.enter_d5,
            RegionName.d5_spiral_chest,
            TransitionType.BASIC_ONE_WAY,
            And(oos_can_kill_moldorm(True), oos_can_kill_normal_enemy(True)),
        ),
        (RegionName.enter_d5, RegionName.d5_terrace_chest, TransitionType.BASIC_ONE_WAY, oos_has_magnet_gloves()),
        (
            RegionName.d5_terrace_chest,
            RegionName.armos_knights_owl,
            TransitionType.BASIC_ONE_WAY,
            oos_can_use_mystery_seeds(),
        ),
        (
            RegionName.d5_terrace_chest,
            RegionName.d5_armos_chest,
            TransitionType.BASIC_ONE_WAY,
            And(oos_can_kill_moldorm(), oos_can_kill_normal_enemy()),
        ),
        (
            RegionName.enter_d5,
            RegionName.d5_cart_bay,
            TransitionType.BASIC_ONE_WAY,
            Or(oos_has_flippers(), oos_can_jump_2_wide_liquid(allow_bombchus=True)),
        ),
        (
            RegionName.d5_cart_bay,
            RegionName.d5_terrace_chest,
            TransitionType.BASIC_ONE_WAY,
            And(
                oos_has_feather(),
                oos_can_remove_rockslide(False),  # Bombchus can be thrown from the middle platform
            ),
        ),
        (
            RegionName.d5_cart_bay,
            RegionName.d5_cart_chest,
            TransitionType.BASIC_ONE_WAY,
            oos_can_trigger_lever_from_minecart(),
        ),
        (
            RegionName.d5_cart_bay,
            RegionName.d5_spinner_chest,
            TransitionType.BASIC_ONE_WAY,
            Or(
                oos_has_magnet_gloves(),
                oos_can_jump_5_wide_pit(),
                And(
                    # Switch with the pots on the bottom left
                    oos_option_medium_logic(),
                    oos_has_switch_hook(2),
                ),
                And(
                    # Wait for le helmasaur to be on the left side of the hole.
                    # By being on the right border, you can see pixels of it and switch hook 1 with it
                    oos_option_hell_logic(),
                    oos_has_switch_hook(),
                ),
            ),
        ),
        (
            RegionName.d5_cart_bay,
            RegionName.d5_drop_ball,
            TransitionType.BASIC_ONE_WAY,
            And(
                oos_can_trigger_lever_from_minecart(),
                Or(
                    oos_can_kill_armored_enemy(True, True),
                    oos_has_shield(),
                    And(oos_option_medium_logic(), oos_has_shovel()),
                    And(
                        oos_option_medium_logic(),
                        # Pull the darknut in the water
                        oos_has_magnet_gloves(),
                    ),
                ),
            ),
        ),
        (
            RegionName.enter_d5,
            RegionName.d5_pot_room,
            TransitionType.BASIC_ONE_WAY,
            And(oos_has_magnet_gloves(), oos_can_remove_rockslide(False), oos_has_feather()),
        ),
        (
            RegionName.d5_cart_bay,
            RegionName.d5_pot_room,
            TransitionType.BASIC_ONE_WAY,
            Or(oos_has_feather(), And(oos_option_hard_logic(), oos_can_use_pegasus_seeds())),
        ),
        (
            RegionName.d5_pot_room,
            RegionName.d5_gibdo_zol_chest,
            TransitionType.BASIC_ONE_WAY,
            oos_can_kill_normal_enemy(),
        ),
        (
            RegionName.d5_cart_bay,
            RegionName.d5_syger_lobby,
            TransitionType.BASIC_ONE_WAY,
            Or(
                oos_has_magnet_gloves(),
                oos_has_cape(),
            ),
        ),
        (
            RegionName.d5_pot_room,
            RegionName.d5_syger_lobby,
            TransitionType.BASIC_ONE_WAY,
            Or(
                oos_has_magnet_gloves(),
                oos_has_cape(),
            ),
        ),
        (RegionName.d5_syger_lobby, RegionName.d5_stalfos_room, TransitionType.BASIC_ONE_WAY, True_()),
        # 5 keys
        (
            RegionName.d5_syger_lobby,
            RegionName.d5_post_syger,
            TransitionType.BASIC_ONE_WAY,
            And(
                oos_has_small_keys(5, 3, keylock_name=ItemName.unicorns_cave_miniboss_keydoor_unlock),
                oos_can_kill_armored_enemy(False, False),
                oos_has_hearts_by_difficulty(5, 4, 3),
            ),
        ),
        (
            RegionName.enter_d5,
            RegionName.d5_magnet_ball_chest,
            TransitionType.BASIC_ONE_WAY,
            oos_self_locking_small_key("Unicorn's Cave: Magnet Gloves Chest", 5),
        ),
        (
            RegionName.enter_d5,
            RegionName.d5_basement,
            TransitionType.BASIC_ONE_WAY,
            And(
                oos_self_locking_small_key("Unicorn's Cave: Treadmills Basement Item", 5),
                OoSCanReachRegion(RegionName.d5_drop_ball),
                oos_has_small_keys(5, 3),
                oos_has_magnet_gloves(),
                Or(oos_can_kill_magunesu(), And(oos_option_medium_logic(), oos_has_feather())),
            ),
        ),
        (
            RegionName.d5_pot_room,
            RegionName.d5_magnet_ball_chest,
            TransitionType.BASIC_ONE_WAY,
            And(
                Or(
                    oos_has_flippers(),
                    And(
                        # Lower route pushing secret blocks requires knowledge, therefore is medium+.
                        # Going there requires jumping a 3.2 wide liquid gap which corresponds the best to a
                        # "4 wide pit" in terms of logic requirements.
                        oos_can_jump_4_wide_pit(),
                        oos_option_medium_logic(),
                        # Upper route would require 6 wide liquid that can only be jumped above with a bomb jump,
                        # which makes the lower route always better when in medium+.
                    ),
                ),
                oos_has_small_keys(5, 5, keylock_name=ItemName.unicorns_cave_magnet_gloves_keydoor_unlock),
            ),
        ),
        (
            RegionName.d5_post_syger,
            RegionName.d5_basement,
            TransitionType.BASIC_ONE_WAY,
            And(
                Or(
                    oos_has_small_keys(5, 5),
                    oos_self_locking_small_key("Unicorn's Cave: Treadmills Basement Item", 5),
                    And(
                        oos_has_unlock(ItemName.unicorns_cave_wall_of_flames_keydoor_unlock),
                        oos_has_unlock(ItemName.unicorns_cave_basement_keydoor_unlock),
                    ),
                ),
                # Magnet ball button
                Or(
                    And(
                        OoSCanReachRegion(RegionName.d5_drop_ball),
                        oos_has_magnet_gloves(),
                    ),
                    oos_has_cane(),
                ),
                # Flamme wall
                Or(
                    And(
                        oos_has_magnet_gloves(),
                        oos_can_kill_magunesu(),
                    ),
                    And(oos_option_medium_logic(), oos_has_feather(), oos_has_hearts(5)),
                ),
                # Basement
                Or(oos_has_magnet_gloves(), And(oos_has_cane(), oos_can_jump_3_wide_pit())),
            ),
        ),
        (
            RegionName.d5_post_syger,
            RegionName.d5_boss,
            TransitionType.BASIC_ONE_WAY,
            And(
                oos_has_small_keys(5, 5, keylock_name=ItemName.unicorns_cave_boss_keyblock_unlock),
                Or(
                    # Go through the basement
                    oos_has_magnet_gloves(),
                    And(
                        oos_option_hell_logic(),
                        oos_has_cape(),
                        oos_can_use_pegasus_seeds(),
                    ),
                ),
                Or(oos_option_medium_logic(), oos_has_feather()),
                Or(
                    # Pass the pot blocking access to the first magnet block
                    oos_option_hard_logic(),  # Just use the magnet from above the pot
                    oos_can_jump_2_wide_pit(),
                    oos_can_break_pot(),
                ),
                oos_has_boss_key(5),
                CanBeatBoss(5),
            ),
        ),
    ]


def make_d6_logic() -> list[LogicLine]:
    return [
        # 0 keys
        (
            RegionName.enter_d6,
            RegionName.d6_1F_east,
            TransitionType.BASIC_ONE_WAY,
            Or(
                # In room 4b3:
                # Walk through the holes
                oos_option_hard_logic(),
                # jump over the hole
                oos_has_feather(),
                # Break the crystals (with crumbling floor)
                oos_has_sword(accept_biggoron=False),
                And(oos_option_medium_logic(), oos_has_biggoron_sword()),
                oos_has_bombs_for_tiles(),
                And(oos_option_medium_logic(), Has("Expert's Ring")),
                And(oos_option_medium_logic(), Has(ItemName.rocs_ring), oos_has_bracelet()),
            ),
        ),
        (
            RegionName.d6_1F_east,
            RegionName.d6_rupee_room,
            TransitionType.BASIC_ONE_WAY,
            oos_can_remove_rockslide(False),
        ),
        (RegionName.d6_1F_east, RegionName.d6_1F_terrace, TransitionType.BASIC_ONE_WAY, True_()),
        (
            RegionName.enter_d6,
            RegionName.d6_1F_terrace,
            TransitionType.BASIC_ONE_WAY,
            And(
                Or(
                    oos_has_small_keys(6, 2),
                    oos_has_unlock(ItemName.ancient_ruins_entrance_keyblock_unlock),
                    oos_has_unlock(ItemName.ancient_ruins_right_path_keydoor_unlock),
                ),
                Or(oos_has_magnet_gloves(), oos_has_cane()),
            ),
        ),
        (
            RegionName.d6_1F_terrace,
            RegionName.d6_magnet_ball_drop,
            TransitionType.BASIC_ONE_WAY,
            Or(
                And(oos_has_feather(), oos_has_magnet_gloves()),
                oos_can_jump_4_wide_pit(),
                And(
                    # Cane through the block
                    oos_option_medium_logic(),
                    oos_has_cane(),
                ),
            ),
        ),
        (RegionName.d6_1F_terrace, RegionName.d6_crystal_trap_room, TransitionType.BASIC_ONE_WAY, True_()),
        (
            RegionName.d6_1F_terrace,
            RegionName.d6_U_room,
            TransitionType.BASIC_ONE_WAY,
            And(
                oos_can_break_crystal(),
                Or(
                    oos_has_magic_boomerang(),
                    And(
                        # Clip into the right statues for the first orb,
                        # then manipulate the position to clip into the bottom right of the opening for the second one
                        oos_option_hell_logic(),
                        oos_has_shooter(),
                        oos_has_sword(False),
                        oos_can_use_pegasus_seeds(),
                    ),
                    And(
                        # Just do the first one in hard, then use bombchus to kill the keese then hit the orb
                        oos_option_hard_logic(),
                        oos_has_shooter(),
                        oos_has_bombchus_to_fight(),
                    ),
                ),
            ),
        ),
        (
            RegionName.d6_U_room,
            RegionName.d6_torch_stairs,
            TransitionType.BASIC_ONE_WAY,
            And(
                Or(
                    # In easy, logic expects slingshot, but medium+ can expect satchel
                    # as well since the distance between platforms & torches is a half-tile
                    oos_has_seed_thrower(),
                    oos_option_medium_logic(),
                ),
                oos_can_use_ember_seeds(False),
            ),
        ),
        (RegionName.d6_torch_stairs, RegionName.d6_escape_room, TransitionType.BASIC_ONE_WAY, oos_has_feather()),
        (RegionName.d6_escape_room, RegionName.d6_vire_chest, TransitionType.BASIC_ONE_WAY, oos_can_kill_stalfos()),
        # 3 keys
        (
            RegionName.enter_d6,
            RegionName.d6_beamos_room,
            TransitionType.BASIC_ONE_WAY,
            oos_has_small_keys(6, 3, keylock_name=ItemName.ancient_ruins_right_path_keydoor_unlock),
        ),
        (RegionName.d6_beamos_room, RegionName.d6_2F_gibdo_chest, TransitionType.BASIC_ONE_WAY, True_()),
        (
            RegionName.d6_beamos_room,
            RegionName.d6_2F_armos_chest,
            TransitionType.BASIC_ONE_WAY,
            oos_can_remove_rockslide(False),
        ),
        (RegionName.d6_2F_armos_chest, RegionName.d6_armos_hall, TransitionType.BASIC_ONE_WAY, oos_has_feather()),
        (
            RegionName.enter_d6,
            RegionName.d6_spinner_north,
            TransitionType.BASIC_ONE_WAY,
            And(
                oos_can_break_crystal(),
                Or(
                    oos_has_magnet_gloves(),
                    And(  # Clip into the blocks to place the somaria block on the button
                        oos_option_hard_logic(), oos_has_cane()
                    ),
                ),
                Or(
                    oos_option_medium_logic(),  # Iframes through the spikes
                    oos_has_feather(),
                ),
                Or(
                    And(
                        oos_has_small_keys(6, 1),
                        # Go through beamos room
                        oos_can_remove_rockslide(False),
                        oos_has_feather(),
                        oos_can_kill_vire(),
                    ),
                    And(
                        oos_has_small_keys(6, 2),
                        Or(
                            # Go through beamos room
                            And(oos_can_remove_rockslide(False), oos_has_feather()),
                            oos_can_kill_vire(),
                        ),
                    ),
                    oos_has_small_keys(6, 3, keylock_name=ItemName.ancient_ruins_entrance_keyblock_unlock),
                    And(
                        oos_has_unlock(ItemName.ancient_ruins_miniboss_keydoor_unlock),
                        oos_can_kill_vire(),
                    ),
                    And(
                        oos_has_unlock(ItemName.ancient_ruins_right_path_keydoor_unlock),
                        oos_can_remove_rockslide(False),
                        oos_has_feather(),
                    ),
                ),
            ),
        ),
        (
            RegionName.d6_vire_chest,
            RegionName.d6_enter_vire,
            TransitionType.BASIC_ONE_WAY,
            And(
                oos_has_small_keys(6, 3, keylock_name=ItemName.ancient_ruins_miniboss_keydoor_unlock),
                oos_can_kill_vire(),
            ),
        ),
        (
            RegionName.d6_enter_vire,
            RegionName.d6_pre_boss_room,
            TransitionType.BASIC_ONE_WAY,
            And(
                Or(
                    # Kill hardhats
                    oos_has_magnet_gloves(),
                    And(
                        oos_option_medium_logic(),
                        oos_has_gale_seeds(),
                        Or(oos_has_seed_thrower(), And(oos_option_hard_logic(), oos_has_satchel())),
                    ),
                ),
                oos_has_feather(),  # jump on trampoline
                Or(
                    # Trigger the orbs
                    oos_has_boomerang(),
                    oos_has_seed_thrower(),
                    oos_has_bombchus_for_tiles(),
                    oos_has_switch_hook(),
                    And(
                        # Could be medium, but we can only get there without magic boomerang in hard
                        oos_option_hard_logic(),
                        Has("Toss Ring"),
                        oos_has_bombs_for_tiles(),
                        oos_has_sword(True),  # Spin/biggoron for the farthest orb
                    ),
                ),
            ),
        ),
        (
            RegionName.d6_pre_boss_room,
            RegionName.d6_boss,
            TransitionType.BASIC_ONE_WAY,
            And(oos_has_boss_key(6), CanBeatBoss(6)),
        ),
    ]


def make_d7_logic() -> list[LogicLine]:
    return [
        # 0 keys
        (RegionName.enter_d7, RegionName.poe_curse_owl, TransitionType.BASIC_ONE_WAY, oos_can_use_mystery_seeds()),
        (
            RegionName.enter_d7,
            RegionName.d7_wizzrobe_chest,
            TransitionType.BASIC_ONE_WAY,
            oos_can_kill_normal_enemy_no_cane(),
        ),
        (
            RegionName.enter_d7,
            RegionName.d7_bombed_wall_chest,
            TransitionType.BASIC_ONE_WAY,
            oos_can_remove_rockslide(False),
        ),
        (
            RegionName.enter_d7,
            RegionName.d7_entrance_wild_embers,
            TransitionType.BASIC_ONE_WAY,
            oos_can_harvest_regrowing_bush(),
        ),
        # 1 key
        (
            RegionName.enter_d7,
            RegionName.enter_poe_A,
            TransitionType.BASIC_ONE_WAY,
            And(
                oos_has_small_keys(7, 1, keylock_name=ItemName.explorers_crypt_entrance_keydoor_unlock),
                oos_has_seed_thrower(),
                oos_can_use_ember_seeds(True),
            ),
        ),
        (
            RegionName.enter_poe_A,
            RegionName.d7_pot_room,
            TransitionType.BASIC_ONE_WAY,
            And(
                Or(
                    # Kill poe sister
                    oos_can_kill_armored_enemy(False, False),
                    And(
                        oos_option_medium_logic(),
                        oos_has_rod(),
                    ),
                    And(
                        # Mystery isn't reasonable due to having only
                        # ~8.8% chance of not getting a gale before killing the sister
                        oos_has_ember_seeds(),
                        Or(oos_option_medium_logic(), oos_has_satchel(2)),
                    ),
                ),
                oos_has_bracelet(),
            ),
        ),
        (
            RegionName.enter_d7,
            RegionName.d7_pot_room,
            TransitionType.BASIC_ONE_WAY,
            And(
                # Poe skip
                oos_option_hell_logic(),
                oos_can_remove_rockslide(False),
                oos_can_use_pegasus_seeds(),
                oos_has_feather(),
                oos_has_bracelet(),
            ),
        ),
        (RegionName.d7_pot_room, RegionName.d7_zol_button, TransitionType.BASIC_ONE_WAY, oos_has_feather()),
        (
            RegionName.d7_pot_room,
            RegionName.d7_armos_puzzle,
            TransitionType.BASIC_ONE_WAY,
            Or(oos_can_jump_3_wide_pit(), oos_has_magnet_gloves()),
        ),
        (RegionName.d7_pot_room, RegionName.d7_magunesu_chest, TransitionType.BASIC_ONE_WAY, oos_has_cane()),
        (
            RegionName.d7_armos_puzzle,
            RegionName.d7_magunesu_chest,
            TransitionType.BASIC_ONE_WAY,
            And(
                oos_can_kill_magunesu(),
                oos_has_magnet_gloves(),
                Or(
                    oos_can_jump_3_wide_pit(),
                    And(
                        # Really precise bomb jumps to cross the 3-holes
                        oos_option_hell_logic(),
                        oos_can_jump_2_wide_liquid(),
                    ),
                ),
            ),
        ),
        # 2 keys
        (
            RegionName.d7_pot_room,
            RegionName.d7_quicksand_chest,
            TransitionType.BASIC_ONE_WAY,
            And(
                oos_has_small_keys(7, 2, keylock_name=ItemName.explorers_crypt_keydoor_to_enclosed_trampoline_unlock),
                oos_has_feather(),
            ),
        ),
        (
            RegionName.d7_pot_room,
            RegionName.d7_water_stairs,
            TransitionType.BASIC_ONE_WAY,
            And(
                # poe skip 2 : https://youtu.be/MIMm6q_yGyQ
                oos_option_hell_logic(),
                oos_has_small_keys(7, 2, keylock_name=ItemName.explorers_crypt_keydoor_to_enclosed_trampoline_unlock),
                oos_has_bombs_for_bombjump(),
                oos_has_cape(),
                oos_can_use_pegasus_seeds(),
                oos_has_flippers(),
                Has("Swimmer's Ring"),
            ),
        ),
        # 3 keys
        (
            RegionName.d7_pot_room,
            RegionName.enter_poe_B,
            TransitionType.BASIC_ONE_WAY,
            And(
                Or(
                    oos_has_small_keys(7, 3),
                    And(
                        oos_has_unlock(ItemName.explorers_crypt_keydoor_to_enclosed_trampoline_unlock),
                        oos_has_unlock(ItemName.explorers_crypt_margrets_keydoor_unlock),
                    ),
                ),
                oos_can_use_ember_seeds(False),
                Or(
                    oos_can_use_pegasus_seeds(),
                    # Hard logic can do it without pegasus, it's very tight but doable
                    oos_option_hard_logic(),
                ),
            ),
        ),
        (
            RegionName.enter_poe_B,
            RegionName.d7_water_stairs,
            TransitionType.BASIC_ONE_WAY,
            And(oos_has_flippers(), oos_has_hearts_by_difficulty(5, 3)),
        ),
        (
            RegionName.d7_water_stairs,
            RegionName.d7_darknut_bridge_trampolines,
            TransitionType.BASIC_ONE_WAY,
            Or(
                And(
                    # Boomerang to activate the switch then magnet gloves to go to the trampolines
                    oos_has_magnet_gloves(),
                    oos_has_magic_boomerang(),
                ),
                And(oos_option_hard_logic(), oos_has_feather(), oos_has_magnet_gloves()),
            ),
        ),
        (
            RegionName.d7_water_stairs,
            RegionName.d7_past_darknut_bridge,
            TransitionType.BASIC_ONE_WAY,
            Or(
                # Just jump to the other side directly
                oos_can_jump_4_wide_pit(),
                oos_has_tight_switch_hook(),  # or hook to the other side
                And(oos_has_seed_thrower(), oos_has_scent_seeds()),
                And(
                    # Kill one darknut then pull the others
                    oos_has_magnet_gloves(),
                    Or(
                        oos_can_kill_armored_enemy(True, True),
                        oos_has_shield(),  # To push the darknut, the rod not really working
                        # Pull the right darknut by just going and stalling in the hole
                        oos_option_medium_logic(),
                    ),
                ),
                oos_shoot_beams(),
            ),
        ),
        (
            RegionName.d7_past_darknut_bridge,
            RegionName.d7_darknut_bridge_trampolines,
            TransitionType.BASIC_ONE_WAY,
            Or(
                # Reach trampolines directly
                oos_can_jump_3_wide_pit(),
                And(
                    Or(
                        # Trigger the spinner switch
                        oos_has_sword(),
                        oos_has_fools_ore(),
                        oos_has_rod(),
                        oos_has_bombs_for_tiles(),
                        oos_has_bombchus_for_tiles(),
                    ),
                    # Reach trampolines using the magnet gloves
                    oos_has_feather(),
                    oos_has_magnet_gloves(),
                ),
            ),
        ),
        (
            RegionName.d7_darknut_bridge_trampolines,
            RegionName.d7_spike_chest,
            TransitionType.BASIC_ONE_WAY,
            oos_can_kill_stalfos(),
        ),
        # 4 keys
        (
            RegionName.d7_water_stairs,
            RegionName.d7_maze_chest,
            TransitionType.BASIC_ONE_WAY,
            And(
                oos_has_small_keys(7, 4, keylock_name=ItemName.explorers_crypt_flying_tile_keyblock_unlock),
                Or(
                    oos_can_kill_armored_enemy(False, False),
                    And(
                        Or(oos_option_medium_logic() & oos_can_kill_moldorm(True), oos_can_kill_moldorm()),
                        Or(
                            # Kill poe sisters
                            oos_has_rod(),
                            And(
                                # 18 embers are needed to kill the boss
                                oos_has_ember_seeds(),
                                Or(
                                    oos_option_hard_logic(),
                                    oos_can_harvest_regrowing_bush(),  # refill embers in the middle
                                    oos_has_satchel(2),
                                ),
                            ),
                        ),
                    ),
                ),
                Or(
                    oos_can_jump_3_wide_liquid(),  # Technically not a liquid but a diagonal pit
                    And(
                        # Switch hook from above with the pot next to the button then jump in the hole
                        oos_option_medium_logic(),
                        oos_has_switch_hook(),
                        oos_can_jump_3_wide_pit(),  # To pass the flying tiles room
                    ),
                    # Casual could switch 2 from the left, but they'd have to jump in the hole to move out
                    # which is against casual logic's spirit
                ),
            ),
        ),
        (
            RegionName.d7_maze_chest,
            RegionName.d7_B2F_drop,
            TransitionType.BASIC_ONE_WAY,
            Or(
                oos_has_magnet_gloves(),
                And(
                    # The jumps in this room being pretty intricate, precise and counterintuitive,
                    # we chose to put that in hard logic only.
                    oos_option_hard_logic(),
                    oos_can_jump_6_wide_pit(),
                ),
            ),
        ),
        # 5 keys
        (
            RegionName.enter_d7,
            RegionName.d7_stalfos_chest,
            TransitionType.BASIC_ONE_WAY,
            And(
                oos_has_small_keys(7, 4),
                oos_self_locking_small_key("Explorer's Crypt (B1F): Chest in Jumping Stalfos Room", 7),
                Or(oos_can_jump_5_wide_pit(), And(oos_option_hard_logic(), oos_can_jump_1_wide_pit(False))),
                oos_can_kill_stalfos(),
            ),
        ),
        (
            RegionName.d7_maze_chest,
            RegionName.d7_stalfos_chest,
            TransitionType.BASIC_ONE_WAY,
            And(
                oos_has_small_keys(7, 5, keylock_name=ItemName.explorers_crypt_shining_blue_puzzle_keydoor_unlock),
                Or(oos_can_jump_5_wide_pit(), And(oos_option_hard_logic(), oos_can_jump_1_wide_pit(False))),
                oos_can_kill_stalfos(),
            ),
        ),
        (
            RegionName.d7_stalfos_chest,
            RegionName.shining_blue_owl,
            TransitionType.BASIC_ONE_WAY,
            oos_can_use_mystery_seeds(),
        ),
        (
            RegionName.enter_d7,
            RegionName.d7_right_of_entrance,
            TransitionType.BASIC_ONE_WAY,
            And(
                oos_can_kill_normal_enemy(),
                Or(
                    oos_has_small_keys(7, 5, keylock_name=ItemName.explorers_crypt_entrance_keydoor_unlock),
                    And(
                        oos_has_small_keys(7, 1),
                        oos_self_locking_small_key("Explorer's Crypt (1F): Chest Right of Entrance", 7),
                    ),
                ),
            ),
        ),
        (
            RegionName.d7_maze_chest,
            RegionName.d7_boss,
            TransitionType.BASIC_ONE_WAY,
            And(oos_has_boss_key(7), CanBeatBoss(7)),
        ),
    ]


def make_d8_logic() -> list[LogicLine]:
    return [
        # 0 keys
        (
            RegionName.enter_d8,
            RegionName.d8_eye_drop,
            TransitionType.BASIC_ONE_WAY,
            And(
                oos_can_break_pot(),
                Or(
                    oos_has_seed_thrower(),
                    And(
                        oos_option_medium_logic(),
                        oos_has_feather(),
                        Or(
                            oos_can_use_ember_seeds(False),
                            oos_can_use_scent_seeds(),
                            oos_can_use_mystery_seeds(),
                        ),
                    ),
                ),
            ),
        ),
        (
            RegionName.enter_d8,
            RegionName.d8_three_eyes_chest,
            TransitionType.BASIC_ONE_WAY,
            And(
                oos_has_feather(),
                Or(
                    oos_has_hyper_slingshot(),
                    And(
                        oos_option_hell_logic(),
                        Or(
                            oos_has_satchel(),
                        ),
                        Or(
                            oos_can_use_ember_seeds(False),
                            oos_can_use_scent_seeds(),
                            oos_can_use_mystery_seeds(),
                        ),
                    ),
                    And(
                        oos_option_hell_logic(),
                        oos_has_slingshot(),
                        Or(
                            oos_can_use_ember_seeds(False),
                            oos_can_use_scent_seeds(),
                            oos_can_use_pegasus_seeds(),
                            oos_can_use_mystery_seeds(),
                        ),
                    ),
                    And(
                        oos_option_hell_logic(),
                        oos_has_shooter(),
                        Or(
                            oos_can_use_ember_seeds(False),
                            oos_can_use_scent_seeds(),
                            oos_can_use_pegasus_seeds(),
                            oos_can_use_mystery_seeds(),
                        ),
                    ),
                ),
            ),
        ),
        (RegionName.enter_d8, RegionName.d8_hardhat_room, TransitionType.BASIC_ONE_WAY, oos_can_kill_magunesu()),
        (
            RegionName.d8_hardhat_room,
            RegionName.d8_hardhat_drop,
            TransitionType.BASIC_ONE_WAY,
            Or(
                And(
                    oos_can_remove_rockslide(
                        False
                    ),  # For the bombchus, leave the hardhat stuck in the upper line to guide the bombchus
                    oos_has_magnet_gloves(),
                ),
                oos_can_use_gale_seeds_offensively(),
            ),
        ),
        # 1 key
        (
            RegionName.d8_hardhat_room,
            RegionName.d8_spike_room,
            TransitionType.BASIC_ONE_WAY,
            And(
                oos_has_hearts_by_difficulty(6, 5, 3),
                oos_has_small_keys(8, 1, keylock_name=ItemName.sword_shield_dungeon_entrance_keyblock_unlock),
                Or(
                    oos_has_cape(),
                    And(  # Tight 2D section jump is hard mode without cape
                        oos_option_hard_logic(), oos_has_feather(), oos_can_use_pegasus_seeds()
                    ),
                ),
            ),
        ),
        # 2 keys
        (
            RegionName.d8_spike_room,
            RegionName.d8_spinner,
            TransitionType.BASIC_ONE_WAY,
            oos_has_small_keys(8, 2, keylock_name=ItemName.sword_shield_dungeon_spinner_keydoor_unlock),
        ),
        (RegionName.d8_spinner, RegionName.silent_watch_owl, TransitionType.BASIC_ONE_WAY, oos_can_use_mystery_seeds()),
        (RegionName.d8_spinner, RegionName.d8_magnet_ball_room, TransitionType.BASIC_ONE_WAY, True_()),
        (
            RegionName.d8_spinner,
            RegionName.d8_armos_chest,
            TransitionType.BASIC_ONE_WAY,
            Or(
                oos_has_magnet_gloves(),
                # Jump from the right side onto the button directly
                oos_can_jump_6_wide_liquid(allow_bombchus=True),
                And(
                    # Clip into the block right of staircase with pegasus seeds and use the cane of somaria to
                    # activate the bridge, save&exit and redo the whole dungeon to get to the other side
                    oos_option_hard_logic(),
                    oos_can_use_pegasus_seeds(),
                    oos_has_cane(),
                ),
            ),
        ),
        (
            RegionName.d8_spinner,
            RegionName.d8_spinner_chest,
            TransitionType.BASIC_ONE_WAY,
            oos_has_magnet_gloves(),
            # Jump 2 liquid also, but this is covered earlier
        ),
        (
            RegionName.d8_spinner,
            RegionName.frypolar_entrance,
            TransitionType.BASIC_ONE_WAY,
            Or(
                oos_has_magnet_gloves(),
                And(
                    oos_option_hell_logic(),
                    oos_can_use_pegasus_seeds(),
                    oos_has_cape(),
                    oos_has_bombs_for_bombjump() | oos_has_bombchus_for_bombjump(),
                ),
            ),
        ),
        (
            RegionName.frypolar_entrance,
            RegionName.frypolar_owl,
            TransitionType.BASIC_ONE_WAY,
            oos_can_use_mystery_seeds(),
        ),
        (
            RegionName.frypolar_entrance,
            RegionName.d8_darknut_chest,
            TransitionType.BASIC_ONE_WAY,
            And(
                Or(
                    oos_has_hyper_slingshot(),
                    And(
                        oos_option_hell_logic(),
                        Or(
                            oos_has_satchel(),
                        ),
                        Or(
                            oos_can_use_ember_seeds(False),
                            oos_can_use_scent_seeds(),
                            oos_can_use_mystery_seeds(),
                        ),
                    ),
                    And(
                        oos_option_hell_logic(),
                        oos_has_slingshot(),
                        Or(
                            oos_can_use_ember_seeds(False),
                            oos_can_use_scent_seeds(),
                            oos_can_use_pegasus_seeds(),
                            oos_can_use_mystery_seeds(),
                        ),
                    ),
                    And(
                        # This one is way easier to time by just bouncing on the left
                        # then going down as the seed spawns in the eye
                        oos_option_hard_logic(),
                        oos_has_shooter(),
                        Or(
                            oos_can_use_ember_seeds(False),
                            oos_can_use_scent_seeds(),
                            oos_can_use_pegasus_seeds(),
                            oos_can_use_mystery_seeds(),
                        ),
                    ),
                ),
                # oos_can_kill_armored_enemy(),
                oos_can_remove_rockslide(False),
            ),
        ),
        # 3 keys
        (
            RegionName.frypolar_entrance,
            RegionName.frypolar_room,
            TransitionType.BASIC_ONE_WAY,
            oos_has_small_keys(8, 3, keylock_name=ItemName.sword_shield_dungeon_miniboss_keydoor_unlock),
        ),
        (
            RegionName.frypolar_room,
            RegionName.frypolar_room_wild_mystery,
            TransitionType.BASIC_ONE_WAY,
            oos_can_harvest_regrowing_bush(),
        ),
        (
            RegionName.frypolar_room,
            RegionName.beat_frypolar,
            TransitionType.BASIC_ONE_WAY,
            Or(
                # Requirements to kill Frypolar
                And(
                    # Casual logic: mystery seeds method is considered mandatory since it's the easiest one
                    oos_has_mystery_seeds(),
                    oos_has_bracelet(),
                ),
                And(
                    # Medium logic: allow killing Frypolar with ember only, but with at least a Lv2 satchel
                    # (the miniboss require 15 embers to die, so 20 max is a bit tight)
                    oos_option_medium_logic(),
                    oos_can_use_ember_seeds(False),
                    oos_has_satchel(2),
                ),
                And(
                    # Hard logic: yolo
                    oos_option_hard_logic(),
                    oos_can_use_ember_seeds(False),
                ),
                # The means of throwing the seeds do not matter:
                # beat frypolar only leads to d8 ice puzzle room in hard-, which requires a HSS.
                # In hell, this is the only place where this region is used without HSS,
                # but then, even satchel is enough
                # (In all honesty, hell players are probably doing HSS skip to come here,
                # so the route is not *that* bad)
            ),
        ),
        (RegionName.beat_frypolar, RegionName.d8_spinner_chest, TransitionType.BASIC_ONE_WAY, True_()),
        (
            RegionName.beat_frypolar,
            RegionName.d8_ice_puzzle_room,
            TransitionType.BASIC_ONE_WAY,
            And(
                oos_has_hyper_slingshot(),
                oos_can_use_ember_seeds(False),
            ),
        ),
        (
            RegionName.d8_ice_puzzle_room,
            RegionName.d8_pols_voice_chest,
            TransitionType.BASIC_ONE_WAY,
            Or(
                oos_has_magic_boomerang(),
                oos_can_jump_6_wide_pit(),
                oos_has_shooter(),
                And(oos_option_medium_logic(), oos_has_bombchus_to_fight()),
            ),
        ),
        # 4 keys
        (
            RegionName.d8_ice_puzzle_room,
            RegionName.d8_crystal_room,
            TransitionType.BASIC_ONE_WAY,
            oos_has_small_keys(8, 4, keylock_name=ItemName.sword_shield_dungeon_ice_crystals_keydoor_unlock),
        ),
        (
            RegionName.d8_crystal_room,
            RegionName.magical_ice_owl,
            TransitionType.BASIC_ONE_WAY,
            oos_can_use_mystery_seeds(),
        ),
        (
            RegionName.d8_crystal_room,
            RegionName.d8_ghost_armos_drop,
            TransitionType.BASIC_ONE_WAY,
            oos_can_remove_rockslide(False),
        ),
        (
            RegionName.d8_crystal_room,
            RegionName.d8_NE_crystal,
            TransitionType.BASIC_ONE_WAY,
            And(oos_has_bracelet(), oos_can_trigger_lever()),
        ),
        (RegionName.d8_crystal_room, RegionName.d8_SE_crystal, TransitionType.BASIC_ONE_WAY, oos_has_bracelet()),
        (RegionName.d8_crystal_room, RegionName.d8_SW_lava_chest, TransitionType.BASIC_ONE_WAY, True_()),
        (RegionName.d8_SE_crystal, RegionName.d8_SE_lava_chest, TransitionType.BASIC_ONE_WAY, True_()),
        (RegionName.d8_SE_crystal, RegionName.d8_spark_chest, TransitionType.BASIC_ONE_WAY, True_()),
        (
            RegionName.d8_ice_puzzle_room,
            RegionName.d8_spark_chest,
            TransitionType.BASIC_ONE_WAY,
            And(
                # Switch hook from the ice puzzle, then s&q
                oos_option_medium_logic(),
                oos_has_switch_hook(),
            ),
        ),
        # 7 keys
        (
            RegionName.d8_crystal_room,
            RegionName.d8_boss,
            TransitionType.BASIC_ONE_WAY,
            And(
                CanBeatBoss(8),
                oos_has_bracelet(),
                Or(
                    oos_has_small_keys(8, 7),
                    And(
                        oos_has_unlock(ItemName.sword_shield_dungeon_lava_hole_keyblock_unlock),
                        oos_has_unlock(ItemName.sword_shield_dungeon_beamos_keydoor_unlock),
                        oos_has_unlock(ItemName.sword_shield_dungeon_boss_keyblock_unlock),
                    ),
                ),
                oos_has_boss_key(8),
            ),
        ),
    ]


def make_d11_logic(options: OracleOfSeasonsOptions) -> list[LogicLine]:
    if not options.linked_heros_cave.value:
        return []
    return [
        (RegionName.enter_d11, RegionName.d11_floor_1_chest, TransitionType.BASIC_ONE_WAY, oos_has_bracelet()),
        (
            RegionName.d11_floor_1_chest,
            RegionName.d11_floor_2_keydrop,
            TransitionType.BASIC_ONE_WAY,
            oos_can_jump_2_wide_pit(),
        ),
        (
            RegionName.d11_floor_2_keydrop,
            RegionName.d11_floor_2_chest,
            TransitionType.BASIC_ONE_WAY,
            oos_has_small_keys(11, keylock_name=ItemName.linked_heros_cave_floor_2_keydoor_unlock),
        ),
        (
            RegionName.d11_floor_2_chest,
            RegionName.d11_floor_3_torch_keydrop,
            TransitionType.BASIC_ONE_WAY,
            And(
                Or(
                    oos_can_swim(False),
                    And(
                        # Jump and break the pot
                        oos_option_hell_logic(),
                        oos_can_jump_5_wide_liquid(),
                        Or(
                            oos_has_noble_sword(),
                            oos_has_biggoron_sword(),
                        ),
                    ),
                ),
                oos_can_use_ember_seeds(True),
            ),
        ),
        (
            RegionName.d11_floor_2_chest,
            RegionName.d11_floor_3_flooded_room,
            TransitionType.BASIC_ONE_WAY,
            And(
                oos_can_swim(False),
                oos_has_small_keys(11, 2, keylock_name=ItemName.linked_heros_cave_floor_3_keyblock_unlock),
                oos_can_use_ember_seeds(True),
                oos_has_seed_thrower(),
            ),
        ),
        (
            RegionName.d11_floor_3_flooded_room,
            RegionName.d11_floor_3_flooded_keydrop,
            TransitionType.BASIC_ONE_WAY,
            Or(oos_can_kill_normal_enemy(), oos_has_switch_hook()),
        ),
        (
            RegionName.d11_floor_3_flooded_room,
            RegionName.d11_floor_3_chest,
            TransitionType.BASIC_ONE_WAY,
            And(
                oos_can_remove_rockslide(False),
                oos_has_small_keys(11, 3, keylock_name=ItemName.linked_heros_cave_floor_3_keydoor_unlock),
            ),
        ),
        (
            RegionName.d11_floor_3_chest,
            RegionName.d11_floor_4_chest,
            TransitionType.BASIC_ONE_WAY,
            oos_has_magnet_gloves(),
        ),
        (
            RegionName.d11_floor_4_chest,
            RegionName.d11_floor_5_gauntlet,
            TransitionType.BASIC_ONE_WAY,
            And(
                oos_can_jump_3_wide_pit(),
                Or(
                    And(
                        Or(oos_has_flute(), oos_has_bombs_to_fight(), oos_has_bombchus_to_fight()),
                        oos_can_kill_magunesu(),
                        oos_can_kill_spiked_beetle(),
                        oos_has_hearts_by_difficulty(5, 4, 3),
                    ),
                    And(
                        # Use the cane press a button at the same time Link is on the button to skip the lowest wave
                        # Counting starts at the top and goes clockwise, waves are:
                        # 0- Spiked Beetle
                        # 1- Gibdo
                        # 2- Arrow Darknut
                        # 3- Magunesu
                        # 4- Lynel
                        # 5- Iron Mask
                        # 6- Pol's Voice
                        # 7- Stalfos
                        # We need to fight at least 5 of these 8 waves,
                        # minimal requirement is oos_can_kill_normal_enemy_no_cane
                        # Waves 1, 5 and 7 can be beaten by it
                        # oos_can_kill_armored_enemy can clear waves 2 and 4, skipping 0, 3 and 6
                        # Otherwise, since we know we have embers already, we can also beat 4, but we need more seeds
                        # (only the seeds aren't in oos_can_kill_armored_enemy)
                        # Skip waves 0, 3 and 6 while finishing the waves 1, 5 and 7 with embers
                        # Now there are two waves left, 4 and 2, which can be beaten by cane
                        # A route can be wave 4 -> wave 5 (skip 3) -> wave 7 (skip 6) -> wave 1 (skip 0) -> wave 2
                        # (With enough bombs left,
                        # it's probably easier to switch wave 6 and wave 4 as lynels hurt a lot)
                        oos_option_hard_logic(),
                        oos_has_cane(),
                        Or(oos_can_kill_armored_enemy(False, True), oos_has_satchel(2)),
                    ),
                ),
            ),
        ),
        (
            RegionName.d11_floor_4_chest,
            RegionName.d11_floor_5_boomerang_maze,
            TransitionType.BASIC_ONE_WAY,
            And(
                oos_can_jump_3_wide_pit(),
                oos_has_small_keys(11, 4, keylock_name=ItemName.linked_heros_cave_boomerang_maze_keydoor_unlock),
                Or(
                    oos_has_magic_boomerang(),
                    oos_has_bombchus_to_fight(),
                    And(
                        oos_option_medium_logic(),
                        oos_has_sword(True),
                    ),
                ),
            ),
        ),
        (
            RegionName.d11_floor_4_chest,
            RegionName.d11_final_chest,
            TransitionType.BASIC_ONE_WAY,
            And(
                oos_can_jump_3_wide_pit(),
                Or(
                    oos_has_small_keys(11, 5),
                    And(
                        oos_has_unlock(ItemName.linked_heros_cave_boomerang_maze_keydoor_unlock),
                        oos_has_unlock(ItemName.linked_heros_cave_final_challenge_keydoor_unlock),
                    ),
                ),
                # oos_has_rupees(80),
                oos_can_complete_d11_puzzle(),
            ),
        ),
        (
            RegionName.enter_d11,
            RegionName.d11_alt_entrance,
            TransitionType.BASIC_ONE_WAY,
            from_world_field("options.linked_heros_cave.is_no_alt_entrance", True),
        ),
        (
            RegionName.d11_alt_entrance,
            RegionName.enter_d11,
            TransitionType.BASIC_ONE_WAY,
            from_world_field("options.linked_heros_cave.is_alt_entrance", True),
        ),
        (
            RegionName.enter_d0,
            RegionName.enter_d11,
            TransitionType.BASIC_ONE_WAY,
            from_world_field("options.linked_heros_cave.is_heros_cave", True),
        ),
    ]
