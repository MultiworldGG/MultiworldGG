
from typing import Dict, TYPE_CHECKING, Any

from rule_builder.rules import False_, Has, True_, Rule

from .strings.regions_entrances import CrystalEntrance, WitchyWoodsEntrance, SpiritCityEntrance, GhostCastleEntrance, \
    JigokuEntrance, FungalForestEntrance, TengokuEntrance, UmiUmiEntrance, ChaosCastleEntrance
from .strings.items import Coin, Upgrade, QuestItem, Unlock, Costume, Key, Power, Warp, QuestEventItem, GoalItem, Custom
from .strings.locations import WitchyWoods, Quest, Gacha, SpiritCity, ShadySewers, GhostCastle, Jigoku, ClubDemon, Tengoku, AngelicHallway, \
    FungalForest, SlimeCitadel, \
    UmiUmi, ChaosCastle, SexEventsLocation, QuestEventLocation, Potsanity

if TYPE_CHECKING:
    from . import FlipwitchWorld


class FlipwitchRules:
    player: int
    world: "FlipwitchWorld"
    region_rules: Dict[str, Rule[Any]]
    entrance_rules: Dict[str, Rule[Any]]
    location_rules: Dict[str, Rule[Any]]

    def __init__(self, world: "FlipwitchWorld") -> None:
        self.player = world.player
        self.world = world
        self.world.options = world.options
        # ONLY USE THIS IF BEWITCHED BUBBLE CHECK ALREADY DONE.  Can save some logic checks IMO.
        self.startedFemale = False_
        if world.options.starting_gender == world.options.starting_gender.option_female:
            self.startedFemale = True_
        self.startedMale = False_
        if self.startedFemale == False_:
            self.startedMale = True_
        self.tengoku_start = False_
        if world.options.starting_area == world.options.starting_area.option_tengoku:
            self.tengoku_start = True_
        self.slime_start = False_
        if world.options.starting_area == world.options.starting_area.option_slime_citadel:
            self.slime_start = True_

        self.entrance_rules = {
            # Crystal Hub Logic
            CrystalEntrance.hub_to_beatrice_house: self.can_warp(0),
            CrystalEntrance.hub_to_goblin_cave: self.can_warp(1),
            CrystalEntrance.hub_to_outside_spirit_city: Has(Warp.witchy),
            CrystalEntrance.hub_to_spirit_city: self.can_warp(2),
            CrystalEntrance.hub_to_slums: Has(Warp.shady),
            CrystalEntrance.hub_to_outside_ghost_castle: Has(Warp.ghost_entrance),
            CrystalEntrance.hub_to_ghost_castle: self.can_warp(3),
            CrystalEntrance.hub_to_jigoku: self.can_warp(4),
            CrystalEntrance.hub_to_club_demon: self.can_warp(5),
            CrystalEntrance.hub_to_tengoku: self.can_warp(6),
            CrystalEntrance.hub_to_angelic_hallway: Has(Warp.angelic_hallway),
            CrystalEntrance.hub_to_fungal_forest: Has(Warp.fungal_forest),
            CrystalEntrance.hub_to_slime_citadel: self.can_warp(7),
            CrystalEntrance.hub_to_slimy_depths: Has(Warp.slimy_depths),
            CrystalEntrance.hub_to_umi_umi: self.can_warp(8),

            # Witchy Woods
            # The additional rule for the first layer should be removed later, when we find a way to let Beatrice give you experience without railroading you in-game
            WitchyWoodsEntrance.beatrice_hut_to_sex_layer_1: Has(QuestItem.fairy_bubble) & Has(Upgrade.bewitched_bubble),
            WitchyWoodsEntrance.sex_layer_1_to_sex_layer_2: self.can_present_gender("Female"),
            WitchyWoodsEntrance.sex_layer_2_to_sex_layer_3: Has(Upgrade.bewitched_bubble),
            WitchyWoodsEntrance.double_jump_tutorial_to_attack_tutorial: self.can_roll() | self.can_double_jump() | Has(Upgrade.demon_wings),
            WitchyWoodsEntrance.double_jump_tutorial_to_male_laser_secret: self.can_present_gender("Male"),
            WitchyWoodsEntrance.gacha_tutorial_to_rundown_house: Has(Key.rundown_house),
            WitchyWoodsEntrance.rundown_house_to_gacha_tutorial: Has(Key.rundown_house),
            WitchyWoodsEntrance.goblin_camp_start_to_goblin_camp_mid: self.can_double_jump(),
            WitchyWoodsEntrance.goblin_camp_bottom_to_goblin_camp_mid: self.can_double_jump(),
            WitchyWoodsEntrance.goblin_camp_bottom_to_ex_bf: Has(QuestItem.goblin_apartment) & Has(Upgrade.peachy_peach),
            WitchyWoodsEntrance.man_cave_entrance_to_goblin_tower: self.can_double_jump(),
            WitchyWoodsEntrance.fairy_ruins_to_spirit_city_bridge: Has(Unlock.crystal_block),
            WitchyWoodsEntrance.spirit_city_bridge_to_fairy_ruins: Has(Unlock.crystal_block),
            WitchyWoodsEntrance.man_cave_entrance_to_man_cave: self.can_present_gender("Male"),
            WitchyWoodsEntrance.tall_chasm_to_small_cavern: (Has(Upgrade.bewitched_bubble) & self.can_double_jump()) |
                                                                          (self.can_present_gender("Female") & self.can_triple_jump() &
                                                                           Has(Upgrade.demon_wings)),
            WitchyWoodsEntrance.ramp_to_cave_heart: self.can_double_jump(),
            WitchyWoodsEntrance.goblin_boss_entrance_to_goblin_queen: Has(Key.goblin_queen) & Has(Upgrade.peachy_peach),

            # Spirit City
            SpiritCityEntrance.shopping_district_to_bathroom_male: Has(Upgrade.bewitched_bubble),
            SpiritCityEntrance.shopping_district_to_bathroom_female: Has(Upgrade.bewitched_bubble),
            SpiritCityEntrance.shopping_district_to_cabaret_cafe: Has(QuestEventItem.rover_1) &
                                                                                Has(QuestEventItem.belle_1) &
                                                                                Has(QuestEventItem.cat_girls_1),
            SpiritCityEntrance.cabaretcafe_to_cabaret_wizardtoilet: self.can_present_gender("Male"),
            SpiritCityEntrance.cabaretcafe_to_cabaret_witchtoilet: self.can_present_gender("Female"),
            SpiritCityEntrance.cabaret_wizardtoilet_to_cabaret_wizardtoilet_subboss: Has(Power.slime_form),
            SpiritCityEntrance.cabaretcafe_to_viproom_cabaret: Has(QuestItem.vip_key),
            SpiritCityEntrance.clinic_front_to_clinic_back: self.can_wear_costume(Costume.nurse),
            SpiritCityEntrance.city_stairwell_to_residential_lane: Has(Unlock.goblin_crystal_block),
            SpiritCityEntrance.cemetery_a_to_waterfall_tomb: Has(Unlock.goblin_crystal_block),
            SpiritCityEntrance.residential_lane_to_city_stairwell: Has(Unlock.goblin_crystal_block),
            SpiritCityEntrance.ghost_castle_rd_to_pig_mansion_entrance: Has(Upgrade.bewitched_bubble) |
                                                                                      (self.can_present_gender("Female") &
                                                                                       self.can_triple_jump()),
            SpiritCityEntrance.pig_mansion_entrance_to_pig_mansion_lobby: self.can_wear_costume(Costume.maid) |
                                                                                        self.can_wear_costume(Costume.pigman),
            SpiritCityEntrance.shady_alley_to_abandoned_apartment: Has(Key.abandoned_apartment) &
                                                                                 (self.can_present_gender("Female") | self.can_triple_jump()),
            SpiritCityEntrance.shady_alley_to_goblin_office: Has(QuestEventItem.goblin_model_3),
            SpiritCityEntrance.cult_hall_lobby_to_cult_hall_left: self.can_wear_costume(Costume.nun),
            SpiritCityEntrance.cult_hall_lobby_to_cult_hall_right: self.can_wear_costume(Costume.priest),
            SpiritCityEntrance.city_stairwell_to_pipeworld_entrance: self.can_ghost_dodge(),
            SpiritCityEntrance.pipeworld_entrance_to_city_stairwell: self.can_ghost_dodge(),

            SpiritCityEntrance.jigoku_path_to_pipe_entrance: Has(Power.slime_form),
            SpiritCityEntrance.tall_pipe_to_secret: self.can_double_jump(),
            SpiritCityEntrance.pipe_sub_boss_to_pipe_chest: Has(Upgrade.peachy_peach),
            SpiritCityEntrance.pipe_chest_to_scale_tutorial: Has(Upgrade.mermaid_scale),

            # Ghost Castle
            GhostCastleEntrance.ghost_castle_door_to_three_gardens: Has(Key.ghostly_castle),
            GhostCastleEntrance.three_gardens_to_ghost_castle_door: Has(Key.ghostly_castle),
            GhostCastleEntrance.three_gardens_to_ghost_gardens_secret: Has(Power.slime_form),
            GhostCastleEntrance.ghost_castle_back_exit_to_fungal_forest: self.can_ghost_dodge(),
            GhostCastleEntrance.fungal_forest_to_ghost_castle_back_exit: self.can_ghost_dodge(),
            GhostCastleEntrance.fungal_forest_to_pathway_to_umi_umi: Has(Upgrade.mermaid_scale),
            GhostCastleEntrance.pathway_to_umi_umi_to_fungal_forest: Has(Upgrade.mermaid_scale) & self.can_double_jump(),
            GhostCastleEntrance.three_gardens_to_four_gardens: self.can_double_jump(),
            GhostCastleEntrance.four_gardens_to_secret: self.can_triple_jump(),
            GhostCastleEntrance.ghost_stairwell_lower_to_ghost_stairwell_mid: Has(Upgrade.bewitched_bubble) |
                                                                                            (self.can_present_gender("Male") &
                                                                                             self.can_triple_jump()),
            GhostCastleEntrance.ghost_stairwell_mid_to_small_hallway: Has(Upgrade.bewitched_bubble),
            GhostCastleEntrance.small_hallway_to_ghost_stairwell_mid: Has(Upgrade.bewitched_bubble),
            GhostCastleEntrance.large_hall_bottom_to_large_hall_top: self.can_double_jump(),
            GhostCastleEntrance.large_hall_top_to_shrub_room: Has(Key.rose_garden) & (self.can_double_jump() | self.can_roll()),
            GhostCastleEntrance.shrub_room_to_large_hall_top: Has(Key.rose_garden),
            GhostCastleEntrance.shrub_room_to_ladder_room: self.can_double_jump(),
            GhostCastleEntrance.ladder_room_to_upper_halls: Has(Upgrade.bewitched_bubble) | (self.can_roll() & self.can_double_jump()) |
                                                                          self.can_triple_jump() | Has(Upgrade.demon_wings),
            GhostCastleEntrance.fashion_room_to_upper_halls: self.can_double_jump() &
                                                                           (Has(Upgrade.bewitched_bubble) |
                                                                            (self.startedMale() & (self.can_triple_jump() | self.can_roll() |
                                                                                                         Has(Upgrade.demon_wings)))
                                                                            | (Has(Upgrade.demon_wings))),
            GhostCastleEntrance.sniff_subboss_to_circular_room: Has(Upgrade.peachy_peach),
            GhostCastleEntrance.tall_tower_to_large_key_room: self.can_ghost_dodge(),
            GhostCastleEntrance.large_key_room_to_tall_tower: self.can_ghost_dodge(),
            GhostCastleEntrance.large_key_room_to_upper_halls: (Has(Upgrade.bewitched_bubble) &
                                                                              self.can_double_jump()) | (self.can_triple_jump() |
                                                                                                               Has(Upgrade.demon_wings)),
            GhostCastleEntrance.tall_tower_to_tutorial_room: self.can_ghost_dodge(),
            GhostCastleEntrance.ghost_castle_door_top_to_cellar_hall: Has(Key.secret_garden),
            GhostCastleEntrance.cellar_hall_to_ghost_castle_door_top: Has(Key.secret_garden) & self.can_triple_jump(),
            GhostCastleEntrance.crumbling_room_to_parkour: Has(Upgrade.bewitched_bubble) & self.can_ghost_dodge(),
            GhostCastleEntrance.boss_save_to_ghost_boss: Has(Upgrade.peachy_peach),

            # Jigoku

            JigokuEntrance.start_drop_to_stone_shrine: Has(Power.slime_form),
            JigokuEntrance.demon_entrance_to_lava_jump_top: self.can_double_jump() | Has(Upgrade.demon_wings),
            JigokuEntrance.lava_jump_top_to_the_mound: Has(Upgrade.bewitched_bubble) |
                                                                         (self.can_present_gender("Male") & self.can_triple_jump()),
            JigokuEntrance.the_mound_to_fencing: self.can_present_gender("Female") & self.can_double_jump(),
            JigokuEntrance.the_mound_to_lava_jump_top: (Has(Upgrade.bewitched_bubble) & self.can_double_jump()) |
                                                                     (self.can_triple_jump()),
            JigokuEntrance.fencing_to_long_hallway: Has(Key.beast) & Has(Upgrade.peachy_peach),
            JigokuEntrance.first_drop_to_jigoku_ruins: Has(Upgrade.bewitched_bubble) |
                                                                     (self.can_present_gender("Male") & self.can_triple_jump()),
            JigokuEntrance.tall_ruins_bottom_to_multi_story_lower: self.can_present_gender("Female") | self.can_double_jump(),
            JigokuEntrance.anthill_lower_to_multi_story_lower: self.can_triple_jump() | (self.can_double_jump() & Has(Upgrade.bewitched_bubble)),
            JigokuEntrance.anthill_lower_to_top: (self.can_present_gender("Female") & self.can_triple_jump()) |
                                                               (self.can_present_gender("Male") & self.can_double_jump()),
            JigokuEntrance.anthill_top_to_multi_story_top: self.can_triple_jump() | Has(Upgrade.demon_wings),
            JigokuEntrance.small_vertical_to_evil_room: self.can_roll() | self.can_double_jump() | Has(Upgrade.demon_wings),
            JigokuEntrance.tall_ruins_top_to_lava_jump_bottom: self.can_double_jump(),
            JigokuEntrance.neon_ruins_to_ruins_hall: Has(Upgrade.bewitched_bubble) | self.can_triple_jump(),
            JigokuEntrance.ruins_hall_to_tall_ruins_mid: Has(Key.collapsed_temple),
            JigokuEntrance.tall_ruins_mid_to_multi_story_mid: self.can_double_jump(),
            JigokuEntrance.small_room_to_boxy_drop: self.can_double_jump(),
            JigokuEntrance.small_room_to_late_drop: self.can_triple_jump() |
                                                                  (Has(Upgrade.demon_wings) &
                                                                   self.can_double_jump()),
            JigokuEntrance.goat_guy_room_to_evil_stairs: Has(Upgrade.bewitched_bubble),
            JigokuEntrance.purple_orange_to_purple_tunnel: Has(Key.secret_club),
            JigokuEntrance.lava_pit_to_gender_puzzle: Has(Upgrade.bewitched_bubble) |
                                                                    (self.can_present_gender("Male") & self.can_triple_jump()),
            JigokuEntrance.lava_pit_to_neon_stairs: Has(Upgrade.bewitched_bubble) |
                                                                    (self.can_present_gender("Male") & self.can_triple_jump()),
            JigokuEntrance.gender_puzzle_to_gacha_coin: Has(Upgrade.bewitched_bubble) &
                                                                      (self.can_triple_jump() | Has(Upgrade.demon_wings)),
            JigokuEntrance.reward_room_to_demon_boss: Has(Key.demon_boss) & Has(Upgrade.peachy_peach),

            # Fungal Forest
            FungalForestEntrance.mini_drop_to_shroom_room: Has(QuestItem.fungal) & Has(Upgrade.peachy_peach),
            FungalForestEntrance.vertical_junction_to_tower_entrance: self.can_double_jump() &
                                                                  (Has(Upgrade.demon_wings) |
                                                                   self.can_triple_jump()),
            FungalForestEntrance.vertical_junction_to_cute_hall: self.can_triple_jump(),
            FungalForestEntrance.cute_hall_to_vertical_junction: Has(Upgrade.demon_wings) | self.can_double_jump(),
            FungalForestEntrance.plummet_to_moving_platforms: self.can_double_jump() & (Has(Upgrade.bewitched_bubble) | self.slime_start()),
            FungalForestEntrance.mushroom_alter_to_on_top: self.can_present_gender("Male"),
            FungalForestEntrance.mushroom_alter_to_circle_back: self.can_double_jump() | self.can_roll() | Has(Upgrade.demon_wings),
            FungalForestEntrance.gender_lifts_to_tutorial_room: Has(Power.slime_form) & Has(Key.forgotten_fungal) &
                                                                              self.can_double_jump() &
                                                                              (Has(Upgrade.bewitched_bubble) |
                                                                               (self.can_present_gender("Male") & self.can_triple_jump())),
            FungalForestEntrance.moving_east_to_long_puzzle: Has(Upgrade.bewitched_bubble) |
                                                                           (self.can_present_gender("Male") &
                                                                            (self.can_triple_jump() | (self.can_double_jump() &
                                                                                                             Has(Upgrade.demon_wings)))),
            FungalForestEntrance.long_puzzle_to_journey_down: self.can_double_jump(),
            FungalForestEntrance.mushroom_cellar_to_jump_room: self.can_double_jump(),
            FungalForestEntrance.end_to_slime_entrance: Has(Key.slime_citadel) & Has(Power.slime_form),
            FungalForestEntrance.slime_entrance_to_end: Has(Key.slime_citadel),
            FungalForestEntrance.phone_booth_to_slime_entrance: Has(Power.slime_form),
            FungalForestEntrance.drop_down_to_neon_banana: Has(Power.slime_form),
            FungalForestEntrance.bunny_drop_down_to_sexy_statue: self.can_present_gender("Female") | self.can_double_jump(),
            FungalForestEntrance.sexy_statue_to_slime_gap: Has(Power.slime_form),
            FungalForestEntrance.statue_sisters_to_candle_hall: Has(Key.slimy_sub_boss) & Has(Upgrade.peachy_peach),
            FungalForestEntrance.long_hallway_to_tall_room: Has(Key.slime_boss) & Has(Upgrade.peachy_peach),

            FungalForestEntrance.brick_hall_to_mossy_room: self.can_present_gender("Male") | self.can_double_jump(),
            FungalForestEntrance.brick_hall_to_tower_entrance: self.can_double_jump(),
            FungalForestEntrance.hook_to_platforms: self.can_triple_jump() | Has(Upgrade.bewitched_bubble),
            FungalForestEntrance.tower_hall_to_large_tower_room: self.tengoku_start() | Has(Upgrade.bewitched_bubble),
            # Since this rule only matters in one direction, & if you cannot triple jump you must have bewitched bubble...
            FungalForestEntrance.large_tower_room_to_tower_hall: self.can_triple_jump() |
                                                                               (self.can_double_jump() & Has(Upgrade.demon_wings)),
            FungalForestEntrance.tower_hall_to_big_tower: self.can_triple_jump() | self.can_double_jump(),

            # Tengoku

            TengokuEntrance.cloud_up_lower_to_cloud_up_top: Has(Upgrade.bewitched_bubble) |
                                                                          (self.can_present_gender("Female") & self.can_double_jump()),
            TengokuEntrance.pillars_up_to_flower_garden: self.can_triple_jump(),
            TengokuEntrance.tree_garden_to_cloudy_room: self.can_double_jump() | Has(Upgrade.demon_wings),
            TengokuEntrance.jump_hallway_to_cloudy_drop: self.can_triple_jump() |
                                                                       (self.can_present_gender("Female") & self.can_double_jump()),
            TengokuEntrance.jump_hallway_left_to_chaos_room: self.can_double_jump() | self.can_roll() | Has(Upgrade.demon_wings),
            TengokuEntrance.long_jump_to_stone_climb: Has(Upgrade.bewitched_bubble),
            TengokuEntrance.maze_up_lower_to_gender_platforms: self.can_ghost_dodge(),
            TengokuEntrance.maze_up_lower_to_maze_up_top: self.can_triple_jump() | (Has(Upgrade.bewitched_bubble) & self.can_double_jump()),
            TengokuEntrance.switch_floor_to_yellow_door: (Has(Upgrade.bewitched_bubble) & ((self.can_roll() & self.can_double_jump()) | Has(Upgrade.demon_wings)))
                                                         | (self.startedMale() & (self.can_triple_jump() | (self.can_double_jump() & Has(Upgrade.demon_wings))))
                                                         | (self.can_triple_jump() & Has(Upgrade.demon_wings)),
            TengokuEntrance.color_jumps_to_three_switches: (self.startedFemale() & (self.can_triple_jump() | Has(Upgrade.demon_wings))) |
                                                                         self.can_triple_jump(),
            TengokuEntrance.highest_point_to_tutorial_room: Has(Upgrade.angel_feathers),  # It just makes the door show up
            TengokuEntrance.three_switches_to_cloud_ramp: self.can_triple_jump() & self.can_present_gender("Female"),
            TengokuEntrance.maze_up_lower_to_tall_puzzle_lower: Has(Upgrade.bewitched_bubble) & (self.can_double_jump() | self.can_roll()),
            TengokuEntrance.angel_boss_to_angel_reward: Has(Upgrade.peachy_peach),
            TengokuEntrance.cloudia_to_cloudia_treasure: Has(Upgrade.peachy_peach),

            # Umi Umi

            UmiUmiEntrance.quad_ladder_to_flip_six: self.can_present_gender("Male"),
            UmiUmiEntrance.flip_six_to_water_pillars: Has(Upgrade.bewitched_bubble),
            UmiUmiEntrance.pre_boss_to_frog_boss: Has(Key.frog_boss) & Has(Upgrade.peachy_peach),
            UmiUmiEntrance.diving_to_diving_deeper: self.can_double_jump(),
            UmiUmiEntrance.diving_deeper_to_dead_mans_drop: self.can_present_gender("Female") | self.can_triple_jump(),
            UmiUmiEntrance.swim_up_to_ocean_puzzle: Has(Upgrade.bewitched_bubble) & self.can_triple_jump(),
            UmiUmiEntrance.coral_junction_to_deep_drop: Has(Upgrade.bewitched_bubble) |
                                                                      (self.can_present_gender("Female") & self.can_triple_jump()),
            UmiUmiEntrance.water_junction_to_deep_drop: self.can_triple_jump() |
                                                                      (self.can_present_gender("Male") & self.can_double_jump()),
            UmiUmiEntrance.trident_hall_to_water_reward: Has(Upgrade.peachy_peach),

            # Chaos Castle

            ChaosCastleEntrance.cc_giant_door_to_cc_entrance_hall: Has(GoalItem.chaos_piece, 6),
            ChaosCastleEntrance.cc_entrance_hall_to_cc_thorn_drop: Has(Upgrade.bewitched_bubble),
            ChaosCastleEntrance.cc_entrance_hall_to_outside_upper_corner: self.can_triple_jump() & Has(Upgrade.demon_wings),
            ChaosCastleEntrance.cc_torch_cave_a_to_cc_triangles_upper: self.can_double_jump(),
            ChaosCastleEntrance.cc_honey_up_to_cc_ghost_torches_b: self.can_ghost_dodge(),
            ChaosCastleEntrance.cc_honey_up_to_ghost_torches_a: self.can_ghost_dodge(),
            ChaosCastleEntrance.cc_ghost_torches_b_to_cc_honey_bend_a: self.can_double_jump(),
            ChaosCastleEntrance.cc_junction_a_to_cc_tengoku_ladder: self.can_triple_jump() & Has(Key.chaos_sanctum),
            ChaosCastleEntrance.cc_honey_jumps_to_cc_stairwell_a: self.can_triple_jump() & Has(Upgrade.demon_wings),
            ChaosCastleEntrance.cc_blue_triangle_upper_right_to_cc_slime_pipes: Has(Power.slime_form),
            ChaosCastleEntrance.cc_l_shape_a_to_cc_triangles_lower: self.can_double_jump(),
            ChaosCastleEntrance.cc_sub_entrance_to_cc_sub_boss: Has(Upgrade.peachy_peach),
            }

        self.location_rules = {
            # Witchy Woods
            WitchyWoods.red_costume: self.can_present_gender("Male"),
            WitchyWoods.sexual_experience_1: self.seen_enough_sex_scenes(4),
            WitchyWoods.sexual_experience_2: self.seen_enough_sex_scenes(8),
            WitchyWoods.sexual_experience_3: self.seen_enough_sex_scenes(8),
            WitchyWoods.sexual_experience_4: self.seen_enough_sex_scenes(12),
            WitchyWoods.sexual_experience_5: self.seen_enough_sex_scenes(16),
            WitchyWoods.sexual_experience_6: self.seen_enough_sex_scenes(16),
            WitchyWoods.sexual_experience_7: self.seen_enough_sex_scenes(20),
            WitchyWoods.sexual_experience_8: self.seen_enough_sex_scenes(24),
            WitchyWoods.sexual_experience_9: self.seen_enough_sex_scenes(24),
            WitchyWoods.sexual_experience_10: self.seen_enough_sex_scenes(28),
            WitchyWoods.sexual_experience_11: self.seen_enough_sex_scenes(32),
            WitchyWoods.sexual_experience_12: self.seen_enough_sex_scenes(32),
            WitchyWoods.sexual_experience_13: self.seen_enough_sex_scenes(36),
            WitchyWoods.sexual_experience_14: self.seen_enough_sex_scenes(40),
            WitchyWoods.rundown_outside_chest: self.can_double_jump(),
            WitchyWoods.man_cave: Has(QuestItem.goblin_headshot) & self.can_present_gender("Male")
                                                & Has(QuestEventItem.goblin_model_1),
            WitchyWoods.past_man_cave: Has(Upgrade.demon_wings) | self.can_double_jump(),
            WitchyWoods.red_wine: self.can_triple_jump(),
            WitchyWoods.before_fairy: self.can_triple_jump(),
            WitchyWoods.flip_platform: self.can_triple_jump() & self.can_present_gender("Female"),
            WitchyWoods.post_fight: Has(Power.slime_form),
            WitchyWoods.fairy_reward: Has(QuestEventItem.queen_defeat),

            # Witchy Woods Events
            SexEventsLocation.beatrice_1: self.seen_enough_sex_scenes(8) & self.can_present_gender("Female"),
            SexEventsLocation.beatrice_2: self.seen_enough_sex_scenes(24) & Has(Upgrade.bewitched_bubble),
            SexEventsLocation.belle_1: Has(QuestItem.cowbell),
            SexEventsLocation.fairy: self.can_wear_costume(Costume.fairy),
            SexEventsLocation.mimic: Has(QuestItem.mimic_chest),
            SexEventsLocation.gobliana_1: Has(QuestItem.business_card) &
                                                        Has(QuestEventItem.goblin_model_1) &
                                                        Has(QuestEventItem.goblin_model_2),
            SexEventsLocation.goblin_princess: self.can_wear_costume(Costume.goblin),
            QuestEventLocation.goblin_model_2: Has(QuestItem.goblin_headshot) &
                                                             self.can_present_gender("Male") &
                                                             Has(QuestEventItem.goblin_model_1),
            QuestEventLocation.goblin_model_3: Has(QuestItem.business_card) &
                                                        Has(QuestEventItem.goblin_model_1) &
                                                        Has(QuestEventItem.goblin_model_2),
            QuestEventLocation.belle_1: Has(QuestItem.cowbell),

            # Spirit City
            SpiritCity.toilet_coin: self.can_triple_jump() | (self.can_double_jump() & Has(Upgrade.demon_wings)),
            SpiritCity.cabaret_cherry_key: Has(QuestEventItem.belle_2_b),
            SpiritCity.shop_roof: self.can_double_jump(),
            SpiritCity.cemetery: Has(Upgrade.mermaid_scale) & Has(Unlock.goblin_crystal_block),
            SpiritCity.ghost_key: Has(Upgrade.bewitched_bubble) & Has(Unlock.goblin_crystal_block),
            SpiritCity.alley: Has(Power.slime_form),
            SpiritCity.chaos: Has(Key.abandoned_apartment),
            SpiritCity.home_2: self.can_triple_jump() | (self.can_double_jump() & Has(Upgrade.demon_wings)),
            SpiritCity.home_1: self.can_ghost_dodge(),
            SpiritCity.home_6: Has(Upgrade.mermaid_scale),
            SpiritCity.green_house: Has(Power.slime_form),
            SpiritCity.fungal_key: self.can_wear_costume(Costume.pigman),
            SpiritCity.maid_contract: self.can_wear_costume(Costume.maid),
            SpiritCity.lone_house: self.can_triple_jump(),
            SpiritCity.special_milkshake: Has(QuestEventItem.belle_2_a) & Has(QuestItem.delicious_milk),

            Potsanity.spc_green_house_3: Has(Power.slime_form),
            Potsanity.spc_green_house_4: Has(Power.slime_form),

            ShadySewers.side_chest: self.can_triple_jump(),
            ShadySewers.shady_hp: (self.can_present_gender("Female") & self.can_double_jump()) |
                                                   (self.can_present_gender("Male") & self.can_triple_jump()),
            ShadySewers.shady_chest: (self.can_present_gender("Female") & self.can_double_jump()) |
                                                   (self.can_present_gender("Male") & self.can_triple_jump()),
            ShadySewers.ratchel_coin: self.can_present_gender("Male") | self.can_triple_jump(),
            ShadySewers.dwd_tutorial: Has(Power.slime_form),

            # Spirit City Events
            SexEventsLocation.rover_1: self.can_ghost_dodge() & self.can_present_gender("Female"),
            SexEventsLocation.bottom_ghost: self.can_wear_costume(Costume.dominating),
            SexEventsLocation.rover_3: Has(QuestItem.legendary_halo),
            SexEventsLocation.belle_2: Has(QuestEventItem.belle_2_b),
            SexEventsLocation.belle_3: Has(QuestEventItem.belle_3),
            SexEventsLocation.cat_girls_3: Has(QuestEventItem.cat_girls_3_b),
            SexEventsLocation.merchant: Has(QuestItem.blue_jelly_mushroom),
            SexEventsLocation.cat: self.can_triple_jump() & Has(Upgrade.bewitched_bubble),
            SexEventsLocation.rat: self.can_wear_costume(Costume.rat),
            SexEventsLocation.tatil: Has(QuestItem.deed) & Has(QuestEventItem.tatil_2) & self.can_wear_costume(Costume.pigman),
            SexEventsLocation.pig: Has(QuestItem.maid_contract) & self.can_wear_costume(Costume.maid),
            SexEventsLocation.kyoni_1: Has(QuestEventItem.belle_2_b) & Has(QuestItem.hellish_dango),
            SexEventsLocation.kyoni_2: Has(QuestEventItem.kyoni_1) & Has(QuestItem.heavenly_daikon),
            SexEventsLocation.bunny_boys: self.can_wear_costume(Costume.bunny),
            SexEventsLocation.bunny_girls: self.can_present_gender( "Male") & Has(QuestItem.silky_slime),
            SexEventsLocation.ghost: Has(QuestEventItem.cat_girls_3_b) & self.can_wear_costume(Costume.cat),
            SexEventsLocation.momo_boy: Has(QuestItem.mono_password),
            SexEventsLocation.momo_girl: Has(QuestItem.mono_password),

            QuestEventLocation.rover_1: self.can_ghost_dodge() & self.can_present_gender("Female"),
            QuestEventLocation.rover_3: Has(QuestItem.legendary_halo),
            QuestEventLocation.cat_girls_3_b: Has(QuestEventItem.cat_girls_3_a),
            QuestEventLocation.belle_2_a: Has(QuestEventItem.belle_1) & Has(QuestEventItem.rover_1)
                                                        & Has(QuestEventItem.cat_girls_1) &
                                                        Has(QuestItem.delicious_milk),
            QuestEventLocation.belle_2_b: Has(QuestEventItem.belle_2_a) & Has(QuestItem.belle_milkshake),
            QuestEventLocation.belle_3: Has(QuestEventItem.belle_2_b) & Has(QuestItem.cherry_key),
            QuestEventLocation.bunny_1: Has(QuestItem.red_wine) & self.can_present_gender("Female"),
            QuestEventLocation.bunny_2: Has(QuestEventItem.rover_3) & Has(QuestEventItem.belle_3)
                                                      & Has(QuestEventItem.cat_girls_3_b) & Has(QuestEventItem.bunny_1),
            QuestEventLocation.kyoni_1: Has(QuestEventItem.belle_2_b) & Has(QuestItem.hellish_dango),
            QuestEventLocation.gobliana_luggage_3: Has(QuestItem.gobliana_luggage)
                                                                 & Has(QuestEventItem.gobliana_luggage_1) &
                                                                 Has(QuestEventItem.gobliana_luggage_2),
            QuestEventLocation.tatil_1: self.can_wear_costume(Costume.pigman),

            # Ghost Castle

            GhostCastle.below_entrance: self.can_ghost_dodge(),
            GhostCastle.slime_3: (Has(Upgrade.bewitched_bubble) & (self.can_double_jump() |
                                                                                                      Has(Upgrade.demon_wings))) |
                                               (self.can_present_gender("Female") & ((self.can_double_jump() &
                                                                                               Has(Upgrade.demon_wings)) |
                                                                                              self.can_triple_jump())) |
                                               (self.can_present_gender("Male") & self.can_double_jump()),
            GhostCastle.up_ladder: self.can_triple_jump(),
            GhostCastle.giant_flip: Has(Key.ghostly_castle) &
                                                  (Has(Upgrade.bewitched_bubble) | (self.can_present_gender("Male") &
                                                                                                        self.can_triple_jump() & Has(
                                                              Upgrade.demon_wings))),
            GhostCastle.elf: Has(Upgrade.bewitched_bubble) | self.can_move_horizontally_enough(),
            GhostCastle.elf_chest: self.can_triple_jump() | (self.can_present_gender("Male") &
                                                                                 self.can_double_jump() &
                                                                                 Has(Upgrade.demon_wings)),
            GhostCastle.across_boss: self.can_triple_jump() | (self.can_double_jump() & Has(Upgrade.demon_wings)),
            GhostCastle.behind_vines: self.can_double_jump(),
            Potsanity.gc_large_gardens_1: self.can_double_jump(),
            Potsanity.gc_large_gardens_2: self.can_double_jump(),
            Potsanity.gc_large_gardens_3: self.can_double_jump(),
            Potsanity.gc_large_gardens_4: self.can_double_jump(),

            # Ghost Castle Events
            QuestEventLocation.cat_girls_1: Has(QuestItem.clothes) & self.can_present_gender("Male"),

            SexEventsLocation.cat_girls_1: Has(QuestItem.clothes) & self.can_present_gender("Male"),

            # Jigoku

            Jigoku.hidden_flip: self.can_present_gender("Male"),
            Jigoku.early_ledge: self.can_double_jump() | Has(Upgrade.demon_wings),
            Jigoku.cat_shrine: Has(QuestEventItem.cat_statue_start),
            Jigoku.far_ledge: self.can_triple_jump() | (Has(Upgrade.demon_wings) &
                                                                            (self.can_roll() | self.can_double_jump())),
            Jigoku.hidden_flip_chest: (self.can_double_jump() & Has(Upgrade.bewitched_bubble)) |
                                                    (self.can_present_gender("Male") & Has(Upgrade.demon_wings) &
                                                     (self.can_triple_jump() | self.can_roll())),
            Jigoku.spring_chest: self.can_double_jump(),
            Jigoku.hidden_ledge: Has(Upgrade.bewitched_bubble) |
                                               (self.can_present_gender("Male") & self.can_double_jump()) |
                                               (self.can_present_gender("Female") & self.can_triple_jump()),
            Jigoku.demon_tutorial: Has(Upgrade.demon_wings),
            Jigoku.northern_cat_shrine: Has(QuestEventItem.cat_statue_start),
            Jigoku.hidden_hole: self.can_double_jump(),
            Potsanity.jg_first_drop_1: self.can_double_jump(),
            Potsanity.jg_first_drop_2: self.can_double_jump(),
            Potsanity.jg_first_drop_3: self.can_double_jump(),

            ClubDemon.demon_letter: Has(QuestItem.angelic_letter) & Has(QuestEventItem.angel_letter),
            ClubDemon.door: Has(Key.demon_club) &
                                          self.can_double_jump() & (Has(Upgrade.demon_wings) |
                                                                           self.can_triple_jump()),
            ClubDemon.flip_magic_chest: self.can_triple_jump() |
                                                      (self.can_present_gender("Female") &
                                                       self.can_double_jump() & (self.can_roll() |
                                                                                        Has(Upgrade.demon_wings))),
            ClubDemon.flip_magic_coin: Has(Upgrade.bewitched_bubble),
            ClubDemon.demonic_gauntlet: Has(Upgrade.bewitched_bubble) & self.can_double_jump(),
            ClubDemon.cat_shrine: Has(QuestEventItem.cat_statue_start),
            ClubDemon.demon_boss_chest: Has(Key.secret_club),
            ClubDemon.demon_boss_chaos: Has(Key.demon_boss) & Has(Upgrade.bewitched_bubble),
            ClubDemon.demon_boss_mp: Has(Key.demon_boss) & Has(Upgrade.bewitched_bubble),

            # Jigoku Events
            SexEventsLocation.cat_statue: Has(QuestEventItem.cat_statue_1) &
                                                        Has(QuestEventItem.cat_statue_2) &
                                                        Has(QuestEventItem.cat_statue_3) & Has(QuestItem.soul_fragment, 3),
            SexEventsLocation.goat: self.can_wear_costume(Costume.farmer),

            QuestEventLocation.cat_statue_start: self.can_wear_costume(Costume.miko),
            QuestEventLocation.cat_statue_1: Has(QuestEventItem.cat_statue_start),
            QuestEventLocation.cat_statue_2: Has(QuestEventItem.cat_statue_start),
            QuestEventLocation.cat_statue_3: Has(QuestEventItem.cat_statue_start),
            QuestEventLocation.goat_guy: Has(QuestItem.angelic_letter) &
                                                       Has(QuestEventItem.angel_letter),

            # Tengoku

            Tengoku.birby: Has(Upgrade.bewitched_bubble) | self.can_double_jump() | Has(
                Upgrade.demon_wings) & Has(Upgrade.peachy_peach),

            AngelicHallway.hidden_foliage_1: self.can_triple_jump() | (self.can_double_jump() &
                                                                                           Has(Upgrade.demon_wings)),
            AngelicHallway.hidden_foliage_2: self.can_triple_jump(),
            AngelicHallway.below_thimble: Has(Upgrade.bewitched_bubble) | self.can_triple_jump(),
            AngelicHallway.thimble_chest: Has(Upgrade.bewitched_bubble) | (self.startedFemale() & self.can_double_jump()),
            AngelicHallway.thimble_1: Has(Upgrade.bewitched_bubble) | (self.startedFemale() & self.can_double_jump()),
            AngelicHallway.thimble_2: Has(Upgrade.bewitched_bubble) | (self.startedFemale() & self.can_double_jump()),
            AngelicHallway.angel_letter: self.can_wear_costume(Costume.postman),
            AngelicHallway.behind_vines: self.can_ghost_dodge(),

            # Tengoku Events

            SexEventsLocation.angel: Has(QuestItem.demonic_letter) & Has(QuestEventItem.goat_guy),
            QuestEventLocation.angel_letter: self.can_wear_costume(Costume.postman),

            # Fungal Forest

            FungalForest.heavenly_daikon: self.can_triple_jump() & Has(Upgrade.demon_wings),
            FungalForest.flip_magic: self.can_double_jump() & (Has(Upgrade.bewitched_bubble) |
                                                                              (self.can_present_gender("Female") &
                                                                               (self.can_roll() & self.can_triple_jump())
                                                                               | Has(Upgrade.demon_wings)) |
                                                                              (self.can_present_gender("Male") &
                                                                               (self.can_roll() | self.can_triple_jump() |
                                                                                Has(Upgrade.demon_wings)))),
            FungalForest.past_chaos: self.can_double_jump() & (self.can_present_gender("Female") |
                                                                                    (self.can_present_gender("Male") &
                                                                                     self.can_triple_jump())),
            FungalForest.fungal_gauntlet: self.can_present_gender("Male"),
            FungalForest.blue_jelly: self.can_present_gender("Male"),
            FungalForest.slime_form: Has(Key.forgotten_fungal) & self.can_double_jump() &
                                     (Has(Upgrade.bewitched_bubble) | (self.can_present_gender("Male") & self.can_triple_jump())),
            FungalForest.slime_citadel_key: Has(Power.slime_form),

            SlimeCitadel.secret_spring_coin: self.can_double_jump(),
            SlimeCitadel.secret_spring_stone: Has(QuestEventItem.stone_start),
            SlimeCitadel.silky_slime_stone: Has(QuestEventItem.stone_start),
            SlimeCitadel.slurp_stone: Has(QuestEventItem.stone_start),
            SlimeCitadel.slurp_chest: Has(Key.slimy_sub_boss),
            SlimeCitadel.slimy_princess_chaos: Has(Key.slime_boss),
            SlimeCitadel.slimy_princess_mp: Has(Key.slime_boss),

            Tengoku.hidden_flip: self.can_present_gender("Female"),

            # Fungal Forest Events
            SexEventsLocation.natasha: Has(QuestEventItem.stone_1) &
                                                     Has(QuestEventItem.stone_2) &
                                                     Has(QuestEventItem.stone_3) & Has(QuestItem.summon_stone, 3),

            QuestEventLocation.stone_start: self.can_wear_costume(Costume.alchemist),

            # Umi Umi

            UmiUmi.early_coin: self.can_triple_jump() | (self.can_double_jump() & Has(Upgrade.demon_wings)),
            UmiUmi.flip_magic_chest: self.can_triple_jump() | (self.can_double_jump() & Has(Upgrade.demon_wings)),
            UmiUmi.save_chest: self.can_triple_jump(),
            UmiUmi.chaos_fight: self.can_triple_jump() | (self.can_double_jump() & self.can_roll()) | Has(Upgrade.demon_wings),

            # Umi Umi Event

            SexEventsLocation.frog: self.can_wear_costume(Costume.angler),

            # Chaos Castle

            ChaosCastle.ghost_coin: self.can_ghost_dodge(),
            ChaosCastle.citadel: Has(Power.slime_form),
            ChaosCastle.fungal: Has(Power.slime_form),
            ChaosCastle.pandora_key: Has(Power.slime_form),
            ChaosCastle.pandora_mp: Has(Power.slime_form),
            ChaosCastle.jump_chest: Has(Upgrade.angel_feathers) & Has(Upgrade.demon_wings),
            ChaosCastle.jump_hp: Has(Upgrade.angel_feathers) & Has(Upgrade.demon_wings),

            # Quests

            Quest.magic_mentor: Has(QuestItem.fairy_bubble),
            Quest.need_my_cowbell: Has(QuestItem.cowbell),
            Quest.giant_chest_key: Has(QuestItem.mimic_chest),
            Quest.fairy_mushroom: self.can_wear_costume(Costume.fairy),
            Quest.model_goblin: Has(QuestItem.business_card) &
                                              Has(QuestEventItem.goblin_model_1) &
                                              Has(QuestEventItem.goblin_model_2),
            Quest.goblin_stud: self.can_wear_costume(Costume.goblin),

            Quest.legendary_chewtoy: Has(QuestItem.legendary_halo),
            Quest.deluxe_milkshake: Has(QuestItem.delicious_milk) &
                                                  Has(QuestItem.belle_milkshake),
            Quest.rat_problem: Has(QuestItem.cherry_key) & Has(QuestEventItem.belle_2_b),
            Quest.haunted_bedroom: Has(Power.slime_form),
            Quest.ectogasm: Has(QuestEventItem.cat_girls_3_b) & self.can_wear_costume(Costume.cat),
            Quest.jelly_mushroom: Has(QuestItem.blue_jelly_mushroom),
            Quest.booze_bunny: Has(QuestItem.red_wine),
            Quest.help_wanted: Has(QuestEventItem.rover_3) & Has(QuestEventItem.belle_3) &
                                             Has(QuestEventItem.cat_girls_3_b) & Has(QuestEventItem.bunny_1),
            Quest.medical_emergency: self.can_wear_costume(Costume.nurse),
            Quest.let_the_dog_out: self.can_ghost_dodge() & self.can_present_gender("Female"),
            Quest.stop_democracy: self.can_wear_costume(Costume.dominating),
            Quest.bunny_club: self.can_wear_costume(Costume.bunny),
            Quest.silky_slime: Has(QuestItem.silky_slime) & self.can_present_gender("Male"),
            Quest.emotional_baggage: Has(QuestItem.gobliana_luggage) &
                                                   Has(QuestEventItem.gobliana_luggage_1)
                                                   & Has(QuestEventItem.gobliana_luggage_2),
            Quest.dirty_debut: Has(QuestEventItem.gobliana_luggage_3) &
                                             Has(QuestEventItem.gobliana_photographer),
            Quest.devilicious: Has(QuestEventItem.belle_2_b) & Has(QuestItem.hellish_dango),
            Quest.daikon: Has(QuestEventItem.kyoni_1) & Has(QuestItem.heavenly_daikon),
            Quest.out_of_service: Has(QuestItem.mono_password),
            Quest.whorus: self.can_wear_costume(Costume.nun),
            Quest.priest: self.can_wear_costume(Costume.priest),
            Quest.alley_cat: self.can_triple_jump() & Has(Upgrade.bewitched_bubble),
            Quest.tatils_tale: Has(QuestEventItem.tatil_2) & Has(QuestItem.deed) & 
                                             self.can_wear_costume(Costume.pigman),
            Quest.signing_bonus: Has(QuestItem.maid_contract) & self.can_wear_costume(Costume.maid),

            Quest.cardio_day: self.can_wear_costume(Costume.rat),
            Quest.panty_raid: Has(QuestItem.clothes) & self.can_present_gender("Male"),
            Quest.unlucky_cat: Has(QuestItem.soul_fragment, 3) & Has(QuestEventItem.cat_statue_1) & 
                               Has(QuestEventItem.cat_statue_2) & Has(QuestEventItem.cat_statue_3),
            Quest.harvest_season: self.can_wear_costume(Costume.farmer),
            Quest.long_distance: Has(QuestEventItem.goat_guy) & Has(QuestItem.demonic_letter),
            Quest.summoning_stones: Has(QuestItem.summon_stone, 3) & Has(QuestEventItem.stone_1) &
                                    Has(QuestEventItem.stone_2) & Has(QuestEventItem.stone_3),
            Quest.semen_with_a: self.can_wear_costume(Costume.angler) & Has(Key.frog_boss),

            Gacha.gacha_sp1: Has(Coin.promotional_coin),
            Gacha.gacha_ad1: self.has_enough_coins(Gacha.gacha_ad1),
            Gacha.gacha_ad2: self.has_enough_coins(Gacha.gacha_ad2),
            Gacha.gacha_ad3: self.has_enough_coins(Gacha.gacha_ad3),
            Gacha.gacha_ad4: self.has_enough_coins(Gacha.gacha_ad4),
            Gacha.gacha_ad5: self.has_enough_coins(Gacha.gacha_ad5),
            Gacha.gacha_ad6: self.has_enough_coins(Gacha.gacha_ad6),
            Gacha.gacha_ad7: self.has_enough_coins(Gacha.gacha_ad7),
            Gacha.gacha_ad8: self.has_enough_coins(Gacha.gacha_ad8),
            Gacha.gacha_ad9: self.has_enough_coins(Gacha.gacha_ad9),
            Gacha.gacha_ad0: self.has_enough_coins(Gacha.gacha_ad0),
            Gacha.gacha_mg1: self.has_enough_coins(Gacha.gacha_mg1),
            Gacha.gacha_mg2: self.has_enough_coins(Gacha.gacha_mg2),
            Gacha.gacha_mg3: self.has_enough_coins(Gacha.gacha_mg3),
            Gacha.gacha_mg4: self.has_enough_coins(Gacha.gacha_mg4),
            Gacha.gacha_mg5: self.has_enough_coins(Gacha.gacha_mg5),
            Gacha.gacha_mg6: self.has_enough_coins(Gacha.gacha_mg6),
            Gacha.gacha_mg7: self.has_enough_coins(Gacha.gacha_mg7),
            Gacha.gacha_mg8: self.has_enough_coins(Gacha.gacha_mg8),
            Gacha.gacha_mg9: self.has_enough_coins(Gacha.gacha_mg9),
            Gacha.gacha_mg0: self.has_enough_coins(Gacha.gacha_mg0),
            Gacha.gacha_bg1: self.has_enough_coins(Gacha.gacha_bg1),
            Gacha.gacha_bg2: self.has_enough_coins(Gacha.gacha_bg2),
            Gacha.gacha_bg3: self.has_enough_coins(Gacha.gacha_bg3),
            Gacha.gacha_bg4: self.has_enough_coins(Gacha.gacha_bg4),
            Gacha.gacha_bg5: self.has_enough_coins(Gacha.gacha_bg5),
            Gacha.gacha_bg6: self.has_enough_coins(Gacha.gacha_bg6),
            Gacha.gacha_bg7: self.has_enough_coins(Gacha.gacha_bg7),
            Gacha.gacha_bg8: self.has_enough_coins(Gacha.gacha_bg8),
            Gacha.gacha_bg9: self.has_enough_coins(Gacha.gacha_bg9),
            Gacha.gacha_bg0: self.has_enough_coins(Gacha.gacha_bg0),
            Gacha.gacha_ag1: self.has_enough_coins(Gacha.gacha_ag1),
            Gacha.gacha_ag2: self.has_enough_coins(Gacha.gacha_ag2),
            Gacha.gacha_ag3: self.has_enough_coins(Gacha.gacha_ag3),
            Gacha.gacha_ag4: self.has_enough_coins(Gacha.gacha_ag4),
            Gacha.gacha_ag5: self.has_enough_coins(Gacha.gacha_ag5),
            Gacha.gacha_ag6: self.has_enough_coins(Gacha.gacha_ag6),
            Gacha.gacha_ag7: self.has_enough_coins(Gacha.gacha_ag7),
            Gacha.gacha_ag8: self.has_enough_coins(Gacha.gacha_ag8),
            Gacha.gacha_ag9: self.has_enough_coins(Gacha.gacha_ag9),
            Gacha.gacha_ag0: self.has_enough_coins(Gacha.gacha_ag0),
        }

    def can_roll(self) -> Rule[Any]:
        shuffle_dodge_rule = True_
        if self.world.options.shuffle_dodge:
            shuffle_dodge_rule = False_
        return shuffle_dodge_rule() | Has(Upgrade.orb_of_avoidance)
    
    def can_ghost_dodge(self) -> Rule[Any]:
        return Has(Power.ghost_form) & (self.can_roll() | Has(Upgrade.demon_wings))

    def can_double_jump(self) -> Rule[Any]:
        shuffle_double_jump_rule = True_
        if self.world.options.shuffle_double_jump:
            shuffle_double_jump_rule = False_
        return shuffle_double_jump_rule() | Has(Upgrade.rose_ribbon) | Has(Upgrade.angel_feathers)

    def can_triple_jump(self) -> Rule[Any]:
        shuffle_double_jump_rule = True_
        if self.world.options.shuffle_double_jump:
            shuffle_double_jump_rule = False_
        return Has(Upgrade.angel_feathers) & (shuffle_double_jump_rule() | Has(Upgrade.rose_ribbon))

    def can_warp(self, area: int) -> Rule[Any]:
        was_starting_world = False_
        if self.world.options.starting_area.value == area:
            was_starting_world = True_
        return was_starting_world() | Has(Warp.area_to_warp[area])

    def seen_enough_sex_scenes(self, amount: int) -> Rule[Any]:
        return Has(Custom.sex_experience, amount)

    def can_move_horizontally_enough(self) -> Rule[Any]:
        return Has(Upgrade.angel_feathers) | Has(Upgrade.demon_wings)

    def can_wear_costume(self, costume: str) -> Rule[Any]:
        if costume in Costume.male_costumes:
            return Has(costume) & self.can_present_gender("Male")
        else:
            return Has(costume) & self.can_present_gender("Female")

    def can_present_gender(self, gender: str) -> Rule[Any]:
        is_male = False_
        if gender == "Male":
            is_male = True_
        is_female = False_
        if gender == "Female":
            is_female = True_
        if self.world.options.starting_gender == self.world.options.starting_gender.option_male:
            return Has(Upgrade.bewitched_bubble) | is_male()
        else:
            return Has(Upgrade.bewitched_bubble) | is_female()

    def has_enough_coins(self, gacha: str) -> Rule[Any]:
        if "Animal" in gacha:
            amount = self.world.animal_order.index(gacha) + 1
            return Has(Coin.animal_coin, amount)
        if "Bunny" in gacha:
            amount = self.world.bunny_order.index(gacha) + 1
            return Has(Coin.bunny_coin, amount)
        if "Monster" in gacha:
            amount = self.world.monster_order.index(gacha) + 1
            return Has(Coin.monster_coin, amount)
        if "Angel" in gacha:
            amount = self.world.angel_order.index(gacha) + 1
            return Has(Coin.angel_demon_coin, amount)
        return False_()

    def set_flipwitch_rules(self) -> None:
        multiworld = self.world.multiworld
        for region in multiworld.get_regions(self.player):
            for entrance in region.entrances:
                if entrance.name in self.entrance_rules:
                    self.world.set_rule(entrance, self.entrance_rules[entrance.name])
            for loc in region.locations:
                if loc.name in self.location_rules:
                    self.world.set_rule(loc, self.location_rules[loc.name])
