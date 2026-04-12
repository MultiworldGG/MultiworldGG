from BaseClasses import CollectionState
from typing import Dict, List, TYPE_CHECKING

from worlds.generic.Rules import CollectionRule

from .strings.regions_entrances import CrystalEntrance, WitchyWoodsEntrance, SpiritCityRegion, SpiritCityEntrance, GhostCastleEntrance, \
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
    region_rules: Dict[str, CollectionRule]
    entrance_rules: Dict[str, CollectionRule]
    location_rules: Dict[str, CollectionRule]
    animal_order: List[str]
    bunny_order: List[str]
    monster_order: List[str]
    angel_order: List[str]

    def __init__(self, world: "FlipwitchWorld") -> None:
        self.player = world.player
        self.world = world
        self.world.options = world.options
        # ONLY USE THIS IF BEWITCHED BUBBLE CHECK ALREADY DONE.  Can save some logic checks IMO.
        self.startedFemale = world.options.starting_gender == world.options.starting_gender.option_female
        self.tengoku_start = world.options.starting_area == world.options.starting_area.option_tengoku
        self.slime_start = world.options.starting_area == world.options.starting_area.option_slime_citadel

        self.region_rules = {
        }

        self.entrance_rules = {
            # Crystal Hub Logic
            CrystalEntrance.hub_to_beatrice_house: lambda state: self.can_warp(0, state),
            CrystalEntrance.hub_to_goblin_cave: lambda state: self.can_warp(1, state),
            CrystalEntrance.hub_to_outside_spirit_city: lambda state: state.has(Warp.witchy, self.player),
            CrystalEntrance.hub_to_spirit_city: lambda state: self.can_warp(2, state),
            CrystalEntrance.hub_to_slums: lambda state: state.has(Warp.shady, self.player),
            CrystalEntrance.hub_to_outside_ghost_castle: lambda state: state.has(Warp.ghost_entrance, self.player),
            CrystalEntrance.hub_to_ghost_castle: lambda state: self.can_warp(3, state),
            CrystalEntrance.hub_to_jigoku: lambda state: self.can_warp(4, state),
            CrystalEntrance.hub_to_club_demon: lambda state: self.can_warp(5, state),
            CrystalEntrance.hub_to_tengoku: lambda state: self.can_warp(6, state),
            CrystalEntrance.hub_to_angelic_hallway: lambda state: state.has(Warp.angelic_hallway, self.player),
            CrystalEntrance.hub_to_fungal_forest: lambda state: state.has(Warp.fungal_forest, self.player),
            CrystalEntrance.hub_to_slime_citadel: lambda state: self.can_warp(7, state),
            CrystalEntrance.hub_to_slimy_depths: lambda state: state.has(Warp.slimy_depths, self.player),
            CrystalEntrance.hub_to_umi_umi: lambda state: self.can_warp(8, state),

            # Witchy Woods
            # The additional rule for the first layer should be removed later, when we find a way to let Beatrice give you experience without railroading you in-game
            WitchyWoodsEntrance.beatrice_hut_to_sex_layer_1: lambda state: state.has(QuestItem.fairy_bubble, self.player) and state.has(Upgrade.bewitched_bubble, self.player),
            WitchyWoodsEntrance.sex_layer_1_to_sex_layer_2: lambda state: self.can_present_gender(state, "Female"),
            WitchyWoodsEntrance.sex_layer_2_to_sex_layer_3: lambda state: state.has(Upgrade.bewitched_bubble, self.player),
            WitchyWoodsEntrance.double_jump_tutorial_to_attack_tutorial: lambda state: self.can_roll(state) or
                                                                     self.can_double_jump(state) or
                                                                     state.has(Upgrade.demon_wings, self.player),
            WitchyWoodsEntrance.double_jump_tutorial_to_male_laser_secret: lambda state: self.can_present_gender(state, "Male"),
            WitchyWoodsEntrance.gacha_tutorial_to_rundown_house: lambda state: state.has(Key.rundown_house, self.player),
            WitchyWoodsEntrance.rundown_house_to_gacha_tutorial: lambda state: state.has(Key.rundown_house, self.player),
            WitchyWoodsEntrance.goblin_camp_start_to_goblin_camp_mid: lambda state: self.can_double_jump(state),
            WitchyWoodsEntrance.goblin_camp_bottom_to_goblin_camp_mid: lambda state: self.can_double_jump(state),
            WitchyWoodsEntrance.goblin_camp_bottom_to_ex_bf: lambda state: state.has(QuestItem.goblin_apartment, self.player) and state.has(Upgrade.peachy_peach, self.player),
            WitchyWoodsEntrance.man_cave_entrance_to_goblin_tower: lambda state: self.can_double_jump(state),
            WitchyWoodsEntrance.fairy_ruins_to_spirit_city_bridge: lambda state: state.has(Unlock.crystal_block, self.player),
            WitchyWoodsEntrance.spirit_city_bridge_to_fairy_ruins: lambda state: state.has(Unlock.crystal_block, self.player),
            WitchyWoodsEntrance.man_cave_entrance_to_man_cave: lambda state: self.can_present_gender(state, "Male"),
            WitchyWoodsEntrance.tall_chasm_to_small_cavern: lambda state: (state.has(Upgrade.bewitched_bubble, self.player) and self.can_double_jump(state)) or
                                                                          (self.can_present_gender(state, "Female") and self.can_triple_jump(state) and
                                                                           state.has(Upgrade.demon_wings, self.player)),
            WitchyWoodsEntrance.ramp_to_cave_heart: lambda state: self.can_double_jump(state),
            WitchyWoodsEntrance.goblin_boss_entrance_to_goblin_queen: lambda state: state.has(Key.goblin_queen, self.player) and state.has(Upgrade.peachy_peach, self.player),

            # Spirit City
            SpiritCityEntrance.shopping_district_to_bathroom_male: lambda state: state.has(Upgrade.bewitched_bubble, self.player),
            SpiritCityEntrance.shopping_district_to_bathroom_female: lambda state: state.has(Upgrade.bewitched_bubble, self.player),
            SpiritCityEntrance.shopping_district_to_cabaret_cafe: lambda state: state.has(QuestEventItem.rover_1, self.player) and
                                                                                state.has(QuestEventItem.belle_1, self.player) and
                                                                                state.has(QuestEventItem.cat_girls_1, self.player),
            SpiritCityEntrance.cabaretcafe_to_cabaret_wizardtoilet: lambda state: self.can_present_gender(state, "Male"),
            SpiritCityEntrance.cabaretcafe_to_cabaret_witchtoilet: lambda state: self.can_present_gender(state, "Female"),
            SpiritCityEntrance.cabaret_wizardtoilet_to_cabaret_wizardtoilet_subboss: lambda state: state.has(Power.slime_form, self.player),
            SpiritCityEntrance.cabaretcafe_to_viproom_cabaret: lambda state: state.has(QuestItem.vip_key, self.player),
            SpiritCityEntrance.clinic_front_to_clinic_back: lambda state: self.can_wear_costume(state, Costume.nurse),
            SpiritCityEntrance.city_stairwell_to_residential_lane: lambda state: state.has(Unlock.goblin_crystal_block, self.player),
            SpiritCityEntrance.cemetery_a_to_waterfall_tomb: lambda state: state.has(Unlock.goblin_crystal_block, self.player),
            SpiritCityEntrance.residential_lane_to_city_stairwell: lambda state: state.has(Unlock.goblin_crystal_block, self.player),
            SpiritCityEntrance.ghost_castle_rd_to_pig_mansion_entrance: lambda state: state.has(Upgrade.bewitched_bubble, self.player) or
                                                                                      (self.can_present_gender(state, "Female") and
                                                                                       self.can_triple_jump(state)),
            SpiritCityEntrance.pig_mansion_entrance_to_pig_mansion_lobby: lambda state: self.can_wear_costume(state, Costume.maid) or
                                                                                        self.can_wear_costume(state, Costume.pigman),
            SpiritCityEntrance.shady_alley_to_abandoned_apartment: lambda state: state.has(Key.abandoned_apartment, self.player),
            SpiritCityEntrance.shady_alley_to_goblin_office: lambda state: state.has(QuestEventItem.goblin_model_3, self.player),
            SpiritCityEntrance.cult_hall_lobby_to_cult_hall_left: lambda state: self.can_wear_costume(state, Costume.nun),
            SpiritCityEntrance.cult_hall_lobby_to_cult_hall_right: lambda state: self.can_wear_costume(state, Costume.priest),
            SpiritCityEntrance.city_stairwell_to_pipeworld_entrance: lambda state: self.can_ghost_dodge(state),
            SpiritCityEntrance.pipeworld_entrance_to_city_stairwell: lambda state: self.can_ghost_dodge(state),

            SpiritCityEntrance.jigoku_path_to_pipe_entrance: lambda state: state.has(Power.slime_form, self.player),
            SpiritCityEntrance.tall_pipe_to_secret: lambda state: self.can_double_jump(state),
            SpiritCityEntrance.pipe_sub_boss_to_pipe_chest: lambda state: state.has(Upgrade.peachy_peach, self.player),
            SpiritCityEntrance.pipe_chest_to_scale_tutorial: lambda state: state.has(Upgrade.mermaid_scale, self.player),

            # Ghost Castle
            GhostCastleEntrance.ghost_castle_door_to_three_gardens: lambda state: state.has(Key.ghostly_castle, self.player),
            GhostCastleEntrance.three_gardens_to_ghost_castle_door: lambda state: state.has(Key.ghostly_castle, self.player),
            GhostCastleEntrance.three_gardens_to_ghost_gardens_secret: lambda state: state.has(Power.slime_form, self.player),
            GhostCastleEntrance.ghost_castle_back_exit_to_fungal_forest: lambda state: self.can_ghost_dodge(state),
            GhostCastleEntrance.fungal_forest_to_ghost_castle_back_exit: lambda state: self.can_ghost_dodge(state),
            GhostCastleEntrance.fungal_forest_to_pathway_to_umi_umi: lambda state: state.has(Upgrade.mermaid_scale, self.player),
            GhostCastleEntrance.pathway_to_umi_umi_to_fungal_forest: lambda state: state.has(Upgrade.mermaid_scale, self.player) and self.can_double_jump(state),
            GhostCastleEntrance.three_gardens_to_four_gardens: lambda state: self.can_double_jump(state),
            GhostCastleEntrance.four_gardens_to_secret: lambda state: self.can_triple_jump(state),
            GhostCastleEntrance.ghost_stairwell_lower_to_ghost_stairwell_mid: lambda state: state.has(Upgrade.bewitched_bubble, self.player) or
                                                                                            (self.can_present_gender(state, "Male") and
                                                                                             self.can_triple_jump(state)),
            GhostCastleEntrance.ghost_stairwell_mid_to_small_hallway: lambda state: state.has(Upgrade.bewitched_bubble, self.player),
            GhostCastleEntrance.small_hallway_to_ghost_stairwell_mid: lambda state: state.has(Upgrade.bewitched_bubble, self.player),
            GhostCastleEntrance.large_hall_bottom_to_large_hall_top: lambda state: self.can_double_jump(state),
            GhostCastleEntrance.large_hall_top_to_shrub_room: lambda state: state.has(Key.rose_garden, self.player) and (self.can_double_jump(state) or self.can_roll(state)),
            GhostCastleEntrance.shrub_room_to_large_hall_top: lambda state: state.has(Key.rose_garden, self.player),
            GhostCastleEntrance.shrub_room_to_ladder_room: lambda state: self.can_double_jump(state),
            GhostCastleEntrance.ladder_room_to_upper_halls: lambda state: state.has(Upgrade.bewitched_bubble, self.player) or (self.can_roll(state) and self.can_double_jump(state)) or
                                                                          self.can_triple_jump(state) or state.has(Upgrade.demon_wings, self.player),
            GhostCastleEntrance.fashion_room_to_upper_halls: lambda state: self.can_double_jump(state) and
                                                                           (state.has(Upgrade.bewitched_bubble, self.player) or
                                                                            (not self.startedFemale and (self.can_triple_jump(state) or self.can_roll(state) or
                                                                                                         state.has(Upgrade.demon_wings, self.player)))
                                                                            or (state.has(Upgrade.demon_wings, self.player))),
            GhostCastleEntrance.sniff_subboss_to_circular_room: lambda state: state.has(Upgrade.peachy_peach, self.player),
            GhostCastleEntrance.tall_tower_to_large_key_room: lambda state: self.can_ghost_dodge(state),
            GhostCastleEntrance.large_key_room_to_tall_tower: lambda state: self.can_ghost_dodge(state),
            GhostCastleEntrance.large_key_room_to_upper_halls: lambda state: (state.has(Upgrade.bewitched_bubble, self.player) and
                                                                              self.can_double_jump(state)) or (self.can_triple_jump(state) or
                                                                                                               state.has(Upgrade.demon_wings, self.player)),
            GhostCastleEntrance.tall_tower_to_tutorial_room: lambda state: self.can_ghost_dodge(state),
            GhostCastleEntrance.ghost_castle_door_top_to_cellar_hall: lambda state: state.has(Key.secret_garden, self.player),
            GhostCastleEntrance.cellar_hall_to_ghost_castle_door_top: lambda state: state.has(Key.secret_garden, self.player) and self.can_triple_jump(state),
            GhostCastleEntrance.crumbling_room_to_parkour: lambda state: state.has(Upgrade.bewitched_bubble, self.player) and self.can_ghost_dodge(state),
            GhostCastleEntrance.boss_save_to_ghost_boss: lambda state: state.has(Upgrade.peachy_peach, self.player),

            # Jigoku

            JigokuEntrance.start_drop_to_stone_shrine: lambda state: state.has(Power.slime_form, self.player),
            JigokuEntrance.demon_entrance_to_lava_jump_top: lambda state: self.can_double_jump(state) or state.has(Upgrade.demon_wings, self.player),
            JigokuEntrance.lava_jump_top_to_the_mound: lambda state: state.has(Upgrade.bewitched_bubble, self.player) or
                                                                         (self.can_present_gender(state, "Male") and self.can_triple_jump(state)),
            JigokuEntrance.the_mound_to_fencing: lambda state: self.can_present_gender(state, "Female") and self.can_double_jump(state),
            JigokuEntrance.the_mound_to_lava_jump_top: lambda state: (state.has(Upgrade.bewitched_bubble, self.player) and self.can_double_jump(state)) or
                                                                     (self.can_triple_jump(state)),
            JigokuEntrance.fencing_to_long_hallway: lambda state: state.has(Key.beast, self.player) and state.has(Upgrade.peachy_peach, self.player),
            JigokuEntrance.first_drop_to_jigoku_ruins: lambda state: state.has(Upgrade.bewitched_bubble, self.player) or
                                                                     (self.can_present_gender(state, "Male") and self.can_triple_jump(state)),
            JigokuEntrance.tall_ruins_bottom_to_multi_story_lower: lambda state: self.can_present_gender(state, "Female") or self.can_double_jump(state),
            JigokuEntrance.anthill_lower_to_multi_story_lower: lambda state: self.can_triple_jump(state) or (self.can_double_jump(state) and state.has(Upgrade.bewitched_bubble, self.player)),
            JigokuEntrance.anthill_lower_to_top: lambda state: (self.can_present_gender(state, "Female") and self.can_triple_jump(state)) or
                                                               (self.can_present_gender(state, "Male") and self.can_double_jump(state)),
            JigokuEntrance.anthill_top_to_multi_story_top: lambda state: self.can_triple_jump(state) or state.has(Upgrade.demon_wings, self.player),
            JigokuEntrance.small_vertical_to_evil_room: lambda state: self.can_roll(state) or self.can_double_jump(state) or state.has(Upgrade.demon_wings, self.player),
            JigokuEntrance.tall_ruins_top_to_lava_jump_bottom: lambda state: self.can_double_jump(state),
            JigokuEntrance.neon_ruins_to_ruins_hall: lambda state: state.has(Upgrade.bewitched_bubble, self.player) or self.can_triple_jump(state),
            JigokuEntrance.ruins_hall_to_tall_ruins_mid: lambda state: state.has(Key.collapsed_temple, self.player),
            JigokuEntrance.tall_ruins_mid_to_multi_story_mid: lambda state: self.can_double_jump(state),
            JigokuEntrance.small_room_to_boxy_drop: lambda state: self.can_double_jump(state),
            JigokuEntrance.small_room_to_late_drop: lambda state: self.can_triple_jump(state) or
                                                                  (state.has(Upgrade.demon_wings, self.player) and
                                                                   self.can_double_jump(state)),
            JigokuEntrance.goat_guy_room_to_evil_stairs: lambda state: state.has(Upgrade.bewitched_bubble, self.player),
            JigokuEntrance.purple_orange_to_purple_tunnel: lambda state: state.has(Key.secret_club, self.player),
            JigokuEntrance.lava_pit_to_gender_puzzle: lambda state: state.has(Upgrade.bewitched_bubble, self.player) or
                                                                    (self.can_present_gender(state, "Male") and self.can_triple_jump(state)),
            JigokuEntrance.lava_pit_to_neon_stairs: lambda state: state.has(Upgrade.bewitched_bubble, self.player) or
                                                                    (self.can_present_gender(state, "Male") and self.can_triple_jump(state)),
            JigokuEntrance.gender_puzzle_to_gacha_coin: lambda state: state.has(Upgrade.bewitched_bubble, self.player) and
                                                                      (self.can_triple_jump(state) or state.has(Upgrade.demon_wings, self.player)),
            JigokuEntrance.reward_room_to_demon_boss: lambda state: state.has(Key.demon_boss, self.player) and state.has(Upgrade.peachy_peach, self.player),

            # Fungal Forest
            FungalForestEntrance.mini_drop_to_shroom_room: lambda state: state.has(QuestItem.fungal, self.player) and state.has(Upgrade.peachy_peach, self.player),
            FungalForestEntrance.vertical_junction_to_tower_entrance: lambda state: self.can_double_jump(state) and
                                                                  (state.has(Upgrade.demon_wings, self.player) or
                                                                   self.can_triple_jump(state)),
            FungalForestEntrance.vertical_junction_to_cute_hall: lambda state: self.can_triple_jump(state),
            FungalForestEntrance.cute_hall_to_vertical_junction: lambda state: state.has(Upgrade.demon_wings, self.player) or self.can_double_jump(state),
            FungalForestEntrance.plummet_to_moving_platforms: lambda state: self.can_double_jump(state) and (state.has(Upgrade.bewitched_bubble, self.player) or self.slime_start),
            FungalForestEntrance.mushroom_alter_to_on_top: lambda state: self.can_present_gender(state, "Male"),
            FungalForestEntrance.mushroom_alter_to_circle_back: lambda state: self.can_double_jump(state) or self.can_roll(state) or state.has(Upgrade.demon_wings),
            FungalForestEntrance.gender_lifts_to_tutorial_room: lambda state: state.has(Power.slime_form, self.player) and state.has(Key.forgotten_fungal, self.player) and
                                                                              self.can_double_jump(state) and
                                                                              (state.has(Upgrade.bewitched_bubble, self.player) or
                                                                               (self.can_present_gender(state, "Male") and self.can_triple_jump(state))),
            FungalForestEntrance.moving_east_to_long_puzzle: lambda state: state.has(Upgrade.bewitched_bubble, self.player) or
                                                                           (self.can_present_gender(state, "Male") and
                                                                            (self.can_triple_jump(state) or (self.can_double_jump(state) and
                                                                                                             state.has(Upgrade.demon_wings, self.player)))),
            FungalForestEntrance.long_puzzle_to_journey_down: lambda state: self.can_double_jump(state),
            FungalForestEntrance.mushroom_cellar_to_jump_room: lambda state: self.can_double_jump(state),
            FungalForestEntrance.end_to_slime_entrance: lambda state: state.has(Key.slime_citadel, self.player) and state.has(Power.slime_form, self.player),
            FungalForestEntrance.slime_entrance_to_end: lambda state: state.has(Key.slime_citadel, self.player),
            FungalForestEntrance.phone_booth_to_slime_entrance: lambda state: state.has(Power.slime_form, self.player),
            FungalForestEntrance.drop_down_to_neon_banana: lambda state: state.has(Power.slime_form, self.player),
            FungalForestEntrance.bunny_drop_down_to_sexy_statue: lambda state: self.can_present_gender(state, "Female") or self.can_double_jump(state),
            FungalForestEntrance.sexy_statue_to_slime_gap: lambda state: state.has(Power.slime_form, self.player),
            FungalForestEntrance.statue_sisters_to_candle_hall: lambda state: state.has(Key.slimy_sub_boss, self.player) and state.has(Upgrade.peachy_peach, self.player),
            FungalForestEntrance.long_hallway_to_tall_room: lambda state: state.has(Key.slime_boss, self.player) and state.has(Upgrade.peachy_peach, self.player),

            FungalForestEntrance.brick_hall_to_mossy_room: lambda state: self.can_present_gender(state, "Male") or self.can_double_jump(state),
            FungalForestEntrance.brick_hall_to_tower_entrance: lambda state: self.can_double_jump(state),
            FungalForestEntrance.hook_to_platforms: lambda state: self.can_triple_jump(state) or state.has(Upgrade.bewitched_bubble, self.player),
            FungalForestEntrance.tower_hall_to_large_tower_room: lambda state: self.tengoku_start or state.has(Upgrade.bewitched_bubble, self.player),
            # Since this rule only matters in one direction, and if you cannot triple jump you must have bewitched bubble...
            FungalForestEntrance.large_tower_room_to_tower_hall: lambda state: self.can_triple_jump(state) or
                                                                               (self.can_double_jump(state) and state.has(Upgrade.demon_wings, self.player)),
            FungalForestEntrance.tower_hall_to_big_tower: lambda state: self.can_triple_jump(state) or self.can_double_jump(state),

            # Tengoku

            TengokuEntrance.cloud_up_lower_to_cloud_up_top: lambda state: state.has(Upgrade.bewitched_bubble, self.player) or
                                                                          (self.can_present_gender(state, "Female") and self.can_double_jump(state)),
            TengokuEntrance.pillars_up_to_flower_garden: lambda state: self.can_triple_jump(state),
            TengokuEntrance.tree_garden_to_cloudy_room: lambda state: self.can_double_jump(state) or state.has(Upgrade.demon_wings, self.player),
            TengokuEntrance.jump_hallway_to_cloudy_drop: lambda state: self.can_triple_jump(state) or
                                                                       (self.can_present_gender(state, "Female") and self.can_double_jump(state)),
            TengokuEntrance.jump_hallway_left_to_chaos_room: lambda state: self.can_double_jump(state) or self.can_roll(state) or state.has(Upgrade.demon_wings, self.player),
            TengokuEntrance.long_jump_to_stone_climb: lambda state: state.has(Upgrade.bewitched_bubble, self.player),
            TengokuEntrance.maze_up_lower_to_gender_platforms: lambda state: self.can_ghost_dodge(state),
            TengokuEntrance.maze_up_lower_to_maze_up_top: lambda state: self.can_triple_jump(state) or (state.has(Upgrade.bewitched_bubble, self.player) and self.can_double_jump(state)),
            TengokuEntrance.switch_floor_to_yellow_door: lambda state: (state.has(Upgrade.bewitched_bubble, self.player) and
                                                                        ((self.can_roll(state) and self.can_double_jump(state)) or
                                                                         state.has(Upgrade.demon_wings, self.player))) or
                                                                       (not self.startedFemale and
                                                                        (self.can_triple_jump(state) or
                                                                         (self.can_double_jump(state) and state.has(Upgrade.demon_wings, self.player)))) or
                                                                       (self.can_triple_jump(state) and state.has(Upgrade.demon_wings, self.player)),
            TengokuEntrance.color_jumps_to_three_switches: lambda state: (self.startedFemale and (self.can_triple_jump(state) or state.has(Upgrade.demon_wings, self.player))) or
                                                                         self.can_triple_jump(state),
            TengokuEntrance.highest_point_to_tutorial_room: lambda state: state.has(Upgrade.angel_feathers, self.player),  # It just makes the door show up
            TengokuEntrance.three_switches_to_cloud_ramp: lambda state: self.can_triple_jump(state) and self.can_present_gender(state, "Female"),
            TengokuEntrance.maze_up_lower_to_tall_puzzle_lower: lambda state: state.has(Upgrade.bewitched_bubble, self.player) and (self.can_double_jump(state) or self.can_roll(state)),
            TengokuEntrance.angel_boss_to_angel_reward: lambda state: state.has(Upgrade.peachy_peach, self.player),
            TengokuEntrance.cloudia_to_cloudia_treasure: lambda state: state.has(Upgrade.peachy_peach, self.player),

            # Umi Umi

            UmiUmiEntrance.quad_ladder_to_flip_six: lambda state: self.can_present_gender(state, "Male"),
            UmiUmiEntrance.flip_six_to_water_pillars: lambda state: state.has(Upgrade.bewitched_bubble, self.player),
            UmiUmiEntrance.pre_boss_to_frog_boss: lambda state: state.has(Key.frog_boss, self.player) and state.has(Upgrade.peachy_peach, self.player),
            UmiUmiEntrance.diving_to_diving_deeper: lambda state: self.can_double_jump(state),
            UmiUmiEntrance.diving_deeper_to_dead_mans_drop: lambda state: self.can_present_gender(state, "Female") or self.can_triple_jump(state),
            UmiUmiEntrance.swim_up_to_ocean_puzzle: lambda state: state.has(Upgrade.bewitched_bubble, self.player) and self.can_triple_jump(state),
            UmiUmiEntrance.coral_junction_to_deep_drop: lambda state: state.has(Upgrade.bewitched_bubble, self.player) or
                                                                      (self.can_present_gender(state, "Female") and self.can_triple_jump(state)),
            UmiUmiEntrance.water_junction_to_deep_drop: lambda state: self.can_triple_jump(state) or
                                                                      (self.can_present_gender(state, "Male") and self.can_double_jump(state)),
            UmiUmiEntrance.trident_hall_to_water_reward: lambda state: state.has(Upgrade.peachy_peach, self.player),

            # Chaos Castle

            ChaosCastleEntrance.cc_giant_door_to_cc_entrance_hall: lambda state: state.has(GoalItem.chaos_piece, self.player, 6),
            ChaosCastleEntrance.cc_entrance_hall_to_cc_thorn_drop: lambda state: state.has(Upgrade.bewitched_bubble, self.player),
            ChaosCastleEntrance.cc_entrance_hall_to_outside_upper_corner: lambda state: self.can_triple_jump(state) and state.has(Upgrade.demon_wings, self.player),
            ChaosCastleEntrance.cc_torch_cave_a_to_cc_triangles_upper: lambda state: self.can_double_jump(state),
            ChaosCastleEntrance.cc_honey_up_to_cc_ghost_torches_b: lambda state: self.can_ghost_dodge(state),
            ChaosCastleEntrance.cc_honey_up_to_ghost_torches_a: lambda state: self.can_ghost_dodge(state),
            ChaosCastleEntrance.cc_ghost_torches_b_to_cc_honey_bend_a: lambda state: self.can_double_jump(state),
            ChaosCastleEntrance.cc_junction_a_to_cc_tengoku_ladder: lambda state: self.can_triple_jump(state) and state.has(Key.chaos_sanctum, self.player),
            ChaosCastleEntrance.cc_honey_jumps_to_cc_stairwell_a: lambda state: self.can_triple_jump(state) and state.has(Upgrade.demon_wings, self.player),
            ChaosCastleEntrance.cc_blue_triangle_upper_right_to_cc_slime_pipes: lambda state: state.has(Power.slime_form, self.player),
            ChaosCastleEntrance.cc_l_shape_a_to_cc_triangles_lower: lambda state: self.can_double_jump(state),
            ChaosCastleEntrance.cc_sub_entrance_to_cc_sub_boss: lambda state: state.has(Upgrade.peachy_peach, self.player),
            }

        self.location_rules = {
            # Witchy Woods
            WitchyWoods.red_costume: lambda state: self.can_present_gender(state, "Male"),
            WitchyWoods.sexual_experience_1: lambda state: self.seen_enough_sex_scenes(state, 4),
            WitchyWoods.sexual_experience_2: lambda state: self.seen_enough_sex_scenes(state, 8),
            WitchyWoods.sexual_experience_3: lambda state: self.seen_enough_sex_scenes(state, 8),
            WitchyWoods.sexual_experience_4: lambda state: self.seen_enough_sex_scenes(state, 12),
            WitchyWoods.sexual_experience_5: lambda state: self.seen_enough_sex_scenes(state, 16),
            WitchyWoods.sexual_experience_6: lambda state: self.seen_enough_sex_scenes(state, 16),
            WitchyWoods.sexual_experience_7: lambda state: self.seen_enough_sex_scenes(state, 20),
            WitchyWoods.sexual_experience_8: lambda state: self.seen_enough_sex_scenes(state, 24),
            WitchyWoods.sexual_experience_9: lambda state: self.seen_enough_sex_scenes(state, 24),
            WitchyWoods.sexual_experience_10: lambda state: self.seen_enough_sex_scenes(state, 28),
            WitchyWoods.sexual_experience_11: lambda state: self.seen_enough_sex_scenes(state, 32),
            WitchyWoods.sexual_experience_12: lambda state: self.seen_enough_sex_scenes(state, 32),
            WitchyWoods.sexual_experience_13: lambda state: self.seen_enough_sex_scenes(state, 36),
            WitchyWoods.sexual_experience_14: lambda state: self.seen_enough_sex_scenes(state, 40),
            WitchyWoods.rundown_outside_chest: lambda state: self.can_double_jump(state),
            WitchyWoods.man_cave: lambda state: state.has(QuestItem.goblin_headshot, self.player) and self.can_present_gender(state, "Male")
                                                and state.has(QuestEventItem.goblin_model_1, self.player),
            WitchyWoods.past_man_cave: lambda state: state.has(Upgrade.demon_wings, self.player) or self.can_double_jump(state),
            WitchyWoods.red_wine: lambda state: self.can_triple_jump(state),
            WitchyWoods.before_fairy: lambda state: self.can_triple_jump(state),
            WitchyWoods.flip_platform: lambda state: self.can_triple_jump(state) and self.can_present_gender(state, "Female"),
            WitchyWoods.post_fight: lambda state: state.has(Power.slime_form, self.player),
            WitchyWoods.fairy_reward: lambda state: state.has(QuestEventItem.queen_defeat, self.player),

            # Witchy Woods Events
            SexEventsLocation.beatrice_1: lambda state: self.seen_enough_sex_scenes(state, 8) and self.can_present_gender(state, "Female"),
            SexEventsLocation.beatrice_2: lambda state: self.seen_enough_sex_scenes(state, 24) and state.has(Upgrade.bewitched_bubble, self.player),
            SexEventsLocation.belle_1: lambda state: state.has(QuestItem.cowbell, self.player),
            SexEventsLocation.fairy: lambda state: self.can_wear_costume(state, Costume.fairy),
            SexEventsLocation.mimic: lambda state: state.has(QuestItem.mimic_chest, self.player),
            SexEventsLocation.gobliana_1: lambda state: state.has(QuestItem.business_card, self.player) and
                                                        state.has(QuestEventItem.goblin_model_1, self.player) and
                                                        state.has(QuestEventItem.goblin_model_2, self.player),
            SexEventsLocation.goblin_princess: lambda state: self.can_wear_costume(state, Costume.goblin),
            QuestEventLocation.goblin_model_2: lambda state: state.has(QuestItem.goblin_headshot, self.player) and
                                                             self.can_present_gender(state, "Male") and
                                                             state.has(QuestEventItem.goblin_model_1, self.player),
            QuestEventLocation.goblin_model_3: lambda state: state.has(QuestItem.business_card, self.player) and
                                                        state.has(QuestEventItem.goblin_model_1, self.player) and
                                                        state.has(QuestEventItem.goblin_model_2, self.player),
            QuestEventLocation.belle_1: lambda state: state.has(QuestItem.cowbell, self.player),

            # Spirit City
            SpiritCity.toilet_coin: lambda state: self.can_triple_jump(state) or (self.can_double_jump(state) and state.has(Upgrade.demon_wings, self.player)),
            SpiritCity.cabaret_cherry_key: lambda state: state.has(QuestEventItem.belle_2_b, self.player),
            SpiritCity.shop_roof: lambda state: self.can_double_jump(state),
            SpiritCity.cemetery: lambda state: state.has(Upgrade.mermaid_scale, self.player) and state.has(Unlock.goblin_crystal_block, self.player),
            SpiritCity.ghost_key: lambda state: state.has(Upgrade.bewitched_bubble, self.player) and state.has(Unlock.goblin_crystal_block, self.player),
            SpiritCity.alley: lambda state: state.has(Power.slime_form, self.player),
            SpiritCity.chaos: lambda state: state.has(Key.abandoned_apartment, self.player),
            SpiritCity.home_2: lambda state: self.can_triple_jump(state) or (self.can_double_jump(state) and state.has(Upgrade.demon_wings, self.player)),
            SpiritCity.home_1: lambda state: self.can_ghost_dodge(state),
            SpiritCity.home_6: lambda state: state.has(Upgrade.mermaid_scale, self.player),
            SpiritCity.green_house: lambda state: state.has(Power.slime_form, self.player),
            SpiritCity.fungal_key: lambda state: self.can_wear_costume(state, Costume.pigman),
            SpiritCity.maid_contract: lambda state: self.can_wear_costume(state, Costume.maid),
            SpiritCity.lone_house: lambda state: self.can_triple_jump(state),
            SpiritCity.special_milkshake: lambda state: state.can_reach_region(SpiritCityRegion.cabaret_cafe, self.player) and state.has(QuestItem.delicious_milk,
                                                                                                                                         self.player),

            Potsanity.spc_green_house_3: lambda state: state.has(Power.slime_form, self.player),
            Potsanity.spc_green_house_4: lambda state: state.has(Power.slime_form, self.player),

            ShadySewers.side_chest: lambda state: self.can_triple_jump(state),
            ShadySewers.shady_hp: lambda state: (self.can_present_gender(state, "Female") and self.can_double_jump(state)) or
                                                   (self.can_present_gender(state, "Male") and self.can_triple_jump(state)),
            ShadySewers.shady_chest: lambda state: (self.can_present_gender(state, "Female") and self.can_double_jump(state)) or
                                                   (self.can_present_gender(state, "Male") and self.can_triple_jump(state)),
            ShadySewers.ratchel_coin: lambda state: self.can_present_gender(state, "Male") or self.can_triple_jump(state),
            ShadySewers.dwd_tutorial: lambda state: state.has(Power.slime_form, self.player),

            # Spirit City Events
            SexEventsLocation.rover_1: lambda state: self.can_ghost_dodge(state) and self.can_present_gender(state, "Female"),
            SexEventsLocation.bottom_ghost: lambda state: self.can_wear_costume(state, Costume.dominating),
            SexEventsLocation.rover_3: lambda state: state.has(QuestItem.legendary_halo, self.player),
            SexEventsLocation.belle_2: lambda state: state.has(QuestEventItem.belle_2_b, self.player),
            SexEventsLocation.belle_3: lambda state: state.has(QuestEventItem.belle_3, self.player),
            SexEventsLocation.cat_girls_3: lambda state: state.has(QuestEventItem.cat_girls_3_b, self.player),
            SexEventsLocation.merchant: lambda state: state.has(QuestItem.blue_jelly_mushroom, self.player),
            SexEventsLocation.cat: lambda state: self.can_triple_jump(state) and state.has(Upgrade.bewitched_bubble, self.player),
            SexEventsLocation.rat: lambda state: self.can_wear_costume(state, Costume.rat),
            SexEventsLocation.tatil: lambda state: state.has(QuestItem.deed, self.player) and state.has(QuestEventItem.tatil_2, self.player),
            SexEventsLocation.pig: lambda state: state.has(QuestItem.maid_contract, self.player),
            SexEventsLocation.kyoni_1: lambda state: state.has(QuestEventItem.belle_2_b, self.player) and state.has(QuestItem.hellish_dango, self.player),
            SexEventsLocation.kyoni_2: lambda state: state.has(QuestEventItem.kyoni_1, self.player) and state.has(QuestItem.heavenly_daikon, self.player),

            QuestEventLocation.rover_1: lambda state: self.can_ghost_dodge(state) and self.can_present_gender(state, "Female"),
            QuestEventLocation.rover_3: lambda state: state.has(QuestItem.legendary_halo, self.player),
            QuestEventLocation.cat_girls_3_b: lambda state: state.has(QuestEventItem.cat_girls_3_a, self.player),
            QuestEventLocation.belle_2_a: lambda state: state.has(QuestEventItem.belle_1, self.player) and state.has(QuestEventItem.rover_1, self.player)
                                                        and state.has(QuestEventItem.cat_girls_1, self.player) and
                                                        state.has(QuestItem.delicious_milk, self.player),
            QuestEventLocation.belle_2_b: lambda state: state.has(QuestEventItem.belle_2_a, self.player) and state.has(QuestItem.belle_milkshake, self.player),
            QuestEventLocation.belle_3: lambda state: state.has(QuestEventItem.belle_2_b, self.player) and state.has(QuestItem.cherry_key, self.player),
            QuestEventLocation.bunny_1: lambda state: state.has(QuestItem.red_wine, self.player) and self.can_present_gender(state, "Female"),
            QuestEventLocation.bunny_2: lambda state: state.has(QuestEventItem.rover_3, self.player) and state.has(QuestEventItem.belle_3, self.player)
                                                      and state.has(QuestEventItem.cat_girls_3_b, self.player) and state.has(QuestEventItem.bunny_1, self.player),
            QuestEventLocation.kyoni_1: lambda state: state.has(QuestEventItem.belle_2_b, self.player) and state.has(QuestItem.hellish_dango, self.player),
            QuestEventLocation.gobliana_luggage_3: lambda state: state.has(QuestItem.gobliana_luggage, self.player)
                                                                 and state.has(QuestEventItem.gobliana_luggage_1, self.player) and
                                                                 state.has(QuestEventItem.gobliana_luggage_2, self.player),

            # Ghost Castle

            GhostCastle.below_entrance: lambda state: self.can_ghost_dodge(state),
            GhostCastle.slime_3: lambda state: (state.has(Upgrade.bewitched_bubble, self.player) and (self.can_double_jump(state) or
                                                                                                      state.has(Upgrade.demon_wings, self.player))) or
                                               (self.can_present_gender(state, "Female") and ((self.can_double_jump(state) and
                                                                                               state.has(Upgrade.demon_wings, self.player)) or
                                                                                              self.can_triple_jump(state))) or
                                               (self.can_present_gender(state, "Male") and self.can_double_jump(state)),
            GhostCastle.up_ladder: lambda state: self.can_triple_jump(state),
            GhostCastle.giant_flip: lambda state: state.has(Key.ghostly_castle, self.player) and
                                                  (state.has(Upgrade.bewitched_bubble, self.player) or (self.can_present_gender(state, "Male") and
                                                                                                        self.can_triple_jump(state) and state.has(
                                                              Upgrade.demon_wings, self.player))),
            GhostCastle.elf: lambda state: state.has(Upgrade.bewitched_bubble, self.player) or self.can_move_horizontally_enough(state),
            GhostCastle.elf_chest: lambda state: self.can_triple_jump(state) or (self.can_present_gender(state, "Male") and
                                                                                 self.can_double_jump(state) and
                                                                                 state.has(Upgrade.demon_wings, self.player)),
            GhostCastle.across_boss: lambda state: self.can_triple_jump(state) or (self.can_double_jump(state) and state.has(Upgrade.demon_wings, self.player)),
            GhostCastle.behind_vines: lambda state: self.can_double_jump(state),
            Potsanity.gc_large_gardens_1: lambda state: self.can_double_jump(state),
            Potsanity.gc_large_gardens_2: lambda state: self.can_double_jump(state),
            Potsanity.gc_large_gardens_3: lambda state: self.can_double_jump(state),
            Potsanity.gc_large_gardens_4: lambda state: self.can_double_jump(state),

            # Ghost Castle Events
            QuestEventLocation.cat_girls_1: lambda state: state.has(QuestItem.clothes, self.player) and self.can_present_gender(state, "Male"),

            SexEventsLocation.cat_girls_1: lambda state: state.has(QuestItem.clothes, self.player) and self.can_present_gender(state, "Male"),

            # Jigoku

            Jigoku.hidden_flip: lambda state: self.can_present_gender(state, "Male"),
            Jigoku.early_ledge: lambda state: self.can_double_jump(state) or state.has(Upgrade.demon_wings, self.player),
            Jigoku.cat_shrine: lambda state: state.has(QuestEventItem.cat_statue_start, self.player),
            Jigoku.far_ledge: lambda state: self.can_triple_jump(state) or (state.has(Upgrade.demon_wings, self.player) and
                                                                            (self.can_roll(state) or self.can_double_jump(state))),
            Jigoku.hidden_flip_chest: lambda state: (self.can_double_jump(state) and state.has(Upgrade.bewitched_bubble, self.player)) or
                                                    (self.can_present_gender(state, "Male") and state.has(Upgrade.demon_wings, self.player) and
                                                     (self.can_triple_jump(state) or self.can_roll(state))),
            Jigoku.spring_chest: lambda state: self.can_double_jump(state),
            Jigoku.hidden_ledge: lambda state: state.has(Upgrade.bewitched_bubble, self.player) or
                                               (self.can_present_gender(state, "Male") and self.can_double_jump(state)) or
                                               (self.can_present_gender(state, "Female") and self.can_triple_jump(state)),
            Jigoku.demon_tutorial: lambda state: state.has(Upgrade.demon_wings, self.player),
            Jigoku.northern_cat_shrine: lambda state: state.has(QuestEventItem.cat_statue_start, self.player),
            Jigoku.hidden_hole: lambda state: self.can_double_jump(state),
            Potsanity.jg_first_drop_1: lambda state: self.can_double_jump(state),
            Potsanity.jg_first_drop_2: lambda state: self.can_double_jump(state),
            Potsanity.jg_first_drop_3: lambda state: self.can_double_jump(state),

            ClubDemon.demon_letter: lambda state: state.has(QuestItem.angelic_letter, self.player) and state.has(QuestEventItem.angel_letter, self.player),
            ClubDemon.door: lambda state: state.has(Key.demon_club, self.player) and
                                          self.can_double_jump(state) and (state.has(Upgrade.demon_wings, self.player) or
                                                                           self.can_triple_jump(state)),
            ClubDemon.flip_magic_chest: lambda state: self.can_triple_jump(state) or
                                                      (self.can_present_gender(state, "Female") and
                                                       self.can_double_jump(state) and (self.can_roll(state) or
                                                                                        state.has(Upgrade.demon_wings, self.player))),
            ClubDemon.flip_magic_coin: lambda state: state.has(Upgrade.bewitched_bubble, self.player),
            ClubDemon.demonic_gauntlet: lambda state: state.has(Upgrade.bewitched_bubble, self.player) and self.can_double_jump(state),
            ClubDemon.cat_shrine: lambda state: state.has(QuestEventItem.cat_statue_start, self.player),
            ClubDemon.demon_boss_chest: lambda state: state.has(Key.secret_club, self.player),
            ClubDemon.demon_boss_chaos: lambda state: state.has(Key.demon_boss, self.player) and state.has(Upgrade.bewitched_bubble, self.player),
            ClubDemon.demon_boss_mp: lambda state: state.has(Key.demon_boss, self.player) and state.has(Upgrade.bewitched_bubble, self.player),

            # Jigoku Events
            SexEventsLocation.cat_statue: lambda state: state.has(QuestEventItem.cat_statue_1, self.player) and
                                                        state.has(QuestEventItem.cat_statue_2, self.player) and
                                                        state.has(QuestEventItem.cat_statue_3, self.player),
            SexEventsLocation.goat: lambda state: self.can_wear_costume(state, Costume.farmer),

            QuestEventLocation.cat_statue_start: lambda state: self.can_wear_costume(state, Costume.miko),
            QuestEventLocation.cat_statue_1: lambda state: state.has(QuestEventItem.cat_statue_start, self.player),
            QuestEventLocation.cat_statue_2: lambda state: state.has(QuestEventItem.cat_statue_start, self.player),
            QuestEventLocation.cat_statue_3: lambda state: state.has(QuestEventItem.cat_statue_start, self.player),
            QuestEventLocation.goat_guy: lambda state: state.has(QuestItem.angelic_letter, self.player) and
                                                       state.has(QuestEventItem.angel_letter, self.player),

            # Tengoku

            Tengoku.birby: lambda state: state.has(Upgrade.bewitched_bubble, self.player) or self.can_double_jump(state) or state.has(
                Upgrade.demon_wings, self.player) and state.has(Upgrade.peachy_peach, self.player),

            AngelicHallway.hidden_foliage_1: lambda state: self.can_triple_jump(state) or (self.can_double_jump(state) and
                                                                                           state.has(Upgrade.demon_wings, self.player)),
            AngelicHallway.hidden_foliage_2: lambda state: self.can_triple_jump(state),
            AngelicHallway.below_thimble: lambda state: state.has(Upgrade.bewitched_bubble, self.player) or self.can_triple_jump(state),
            AngelicHallway.thimble_chest: lambda state: state.has(Upgrade.bewitched_bubble, self.player) or (self.startedFemale and self.can_double_jump(state)),
            AngelicHallway.thimble_1: lambda state: state.has(Upgrade.bewitched_bubble, self.player) or (self.startedFemale and self.can_double_jump(state)),
            AngelicHallway.thimble_2: lambda state: state.has(Upgrade.bewitched_bubble, self.player) or (self.startedFemale and self.can_double_jump(state)),
            AngelicHallway.angel_letter: lambda state: self.can_wear_costume(state, Costume.postman),
            AngelicHallway.behind_vines: lambda state: self.can_ghost_dodge(state),

            # Tengoku Events

            SexEventsLocation.angel: lambda state: state.has(QuestItem.demonic_letter, self.player) and state.has(QuestEventItem.goat_guy, self.player),
            QuestEventLocation.angel_letter: lambda state: self.can_wear_costume(state, Costume.postman),

            # Fungal Forest

            FungalForest.heavenly_daikon: lambda state: self.can_triple_jump(state) and state.has(Upgrade.demon_wings, self.player),
            FungalForest.flip_magic: lambda state: self.can_double_jump(state) and (state.has(Upgrade.bewitched_bubble, self.player) or
                                                                              (self.can_present_gender(state, "Female") and
                                                                               (self.can_roll(state) and (self.can_triple_jump(state) or
                                                                                                          state.has(Upgrade.demon_wings, self.player)))
                                                                               or self.can_double_jump(state) and state.has(Upgrade.demon_wings, self.player)) or
                                                                              (self.can_present_gender(state, "Male") and
                                                                               (self.can_roll(state) or self.can_triple_jump(state) or
                                                                                state.has(Upgrade.demon_wings, self.player)))),
            FungalForest.past_chaos: lambda state: self.can_double_jump(state) and (self.can_present_gender(state, "Female") or
                                                                                    (self.can_present_gender(state, "Male") and
                                                                                     self.can_triple_jump(state))),
            FungalForest.fungal_gauntlet: lambda state: self.can_present_gender(state, "Male"),
            FungalForest.blue_jelly: lambda state: self.can_present_gender(state, "Male"),
            FungalForest.slime_form: lambda state: state.has(Key.forgotten_fungal, self.player) and self.can_double_jump(state) and
                                                   (state.has(Upgrade.bewitched_bubble, self.player) or (self.can_present_gender(state, "Male") and
                                                    self.can_triple_jump(state))),
            FungalForest.slime_citadel_key: lambda state: state.has(Power.slime_form, self.player),

            SlimeCitadel.secret_spring_coin: lambda state: self.can_double_jump(state),
            SlimeCitadel.secret_spring_stone: lambda state: state.has(QuestEventItem.stone_start, self.player),
            SlimeCitadel.silky_slime_stone: lambda state: state.has(QuestEventItem.stone_start, self.player),
            SlimeCitadel.slurp_stone: lambda state: state.has(QuestEventItem.stone_start, self.player),
            SlimeCitadel.slurp_chest: lambda state: state.has(Key.slimy_sub_boss, self.player),
            SlimeCitadel.slimy_princess_chaos: lambda state: state.has(Key.slime_boss, self.player),
            SlimeCitadel.slimy_princess_mp: lambda state: state.has(Key.slime_boss, self.player),

            Tengoku.hidden_flip: lambda state: self.can_present_gender(state, "Female"),

            # Fungal Forest Events
            SexEventsLocation.natasha: lambda state: state.has(QuestEventItem.stone_1, self.player) and
                                                     state.has(QuestEventItem.stone_2, self.player) and
                                                     state.has(QuestEventItem.stone_3, self.player),

            QuestEventLocation.stone_start: lambda state: self.can_wear_costume(state, Costume.alchemist),

            # Umi Umi

            UmiUmi.early_coin: lambda state: self.can_triple_jump(state) or (self.can_double_jump(state) and state.has(Upgrade.demon_wings, self.player)),
            UmiUmi.flip_magic_chest: lambda state: self.can_triple_jump(state) or (self.can_double_jump(state) and state.has(Upgrade.demon_wings, self.player)),
            UmiUmi.save_chest: lambda state: self.can_triple_jump(state),
            UmiUmi.chaos_fight: lambda state: self.can_triple_jump(state) or (self.can_double_jump(state) and self.can_roll(state)) or state.has(Upgrade.demon_wings, self.player),

            # Umi Umi Event

            SexEventsLocation.frog: lambda state: self.can_wear_costume(state, Costume.angler),

            # Chaos Castle

            ChaosCastle.ghost_coin: lambda state: self.can_ghost_dodge(state),
            ChaosCastle.citadel: lambda state: state.has(Power.slime_form, self.player),
            ChaosCastle.fungal: lambda state: state.has(Power.slime_form, self.player),
            ChaosCastle.pandora_key: lambda state: state.has(Power.slime_form, self.player),
            ChaosCastle.pandora_mp: lambda state: state.has(Power.slime_form, self.player),
            ChaosCastle.jump_chest: lambda state: state.has(Upgrade.angel_feathers, self.player) and state.has(Upgrade.demon_wings, self.player),
            ChaosCastle.jump_hp: lambda state: state.has(Upgrade.angel_feathers, self.player) and state.has(Upgrade.demon_wings, self.player),

            # Quests

            Quest.magic_mentor: lambda state: state.has(QuestItem.fairy_bubble, self.player),
            Quest.need_my_cowbell: lambda state: state.has(QuestItem.cowbell, self.player),
            Quest.giant_chest_key: lambda state: state.has(QuestItem.mimic_chest, self.player),
            Quest.fairy_mushroom: lambda state: self.can_wear_costume(state, Costume.fairy),
            Quest.model_goblin: lambda state: state.has(QuestItem.business_card, self.player) and
                                              state.has(QuestEventItem.goblin_model_1, self.player) and
                                              state.has(QuestEventItem.goblin_model_2, self.player),
            Quest.goblin_stud: lambda state: self.can_wear_costume(state, Costume.goblin),

            Quest.legendary_chewtoy: lambda state: state.has(QuestItem.legendary_halo, self.player),
            Quest.deluxe_milkshake: lambda state: state.has(QuestItem.delicious_milk, self.player) and
                                                  state.has(QuestItem.belle_milkshake, self.player),
            Quest.rat_problem: lambda state: state.has(QuestItem.cherry_key, self.player) and state.has(QuestEventItem.belle_2_b, self.player),
            Quest.haunted_bedroom: lambda state: state.has(Power.slime_form, self.player),
            Quest.ectogasm: lambda state: state.has(QuestEventItem.cat_girls_3_b, self.player) and self.can_wear_costume(state, Costume.cat),
            Quest.jelly_mushroom: lambda state: state.has(QuestItem.blue_jelly_mushroom, self.player),
            Quest.booze_bunny: lambda state: state.has(QuestItem.red_wine, self.player),
            Quest.help_wanted: lambda state: state.has(QuestEventItem.rover_3, self.player) and state.has(QuestEventItem.belle_3, self.player) and
                                             state.has(QuestEventItem.cat_girls_3_b, self.player) and state.has(QuestEventItem.bunny_1, self.player),
            Quest.medical_emergency: lambda state: self.can_wear_costume(state, Costume.nurse),
            Quest.let_the_dog_out: lambda state: self.can_ghost_dodge(state) and self.can_present_gender(state, "Female"),
            Quest.stop_democracy: lambda state: self.can_wear_costume(state, Costume.dominating),
            Quest.bunny_club: lambda state: self.can_wear_costume(state, Costume.bunny),
            Quest.silky_slime: lambda state: state.has(QuestItem.silky_slime, self.player) and self.can_present_gender(state, "Male"),
            Quest.emotional_baggage: lambda state: state.has(QuestItem.gobliana_luggage, self.player) and
                                                   state.has(QuestEventItem.gobliana_luggage_1, self.player)
                                                   and state.has(QuestEventItem.gobliana_luggage_2, self.player),
            Quest.dirty_debut: lambda state: state.has(QuestEventItem.gobliana_luggage_3, self.player) and
                                             state.has(QuestEventItem.gobliana_photographer, self.player),
            Quest.devilicious: lambda state: state.has(QuestEventItem.belle_2_b, self.player) and state.has(QuestItem.hellish_dango, self.player),
            Quest.daikon: lambda state: state.has(QuestEventItem.kyoni_1, self.player) and state.has(QuestItem.heavenly_daikon, self.player),
            Quest.out_of_service: lambda state: state.has(QuestItem.mono_password, self.player),
            Quest.whorus: lambda state: self.can_wear_costume(state, Costume.nun),
            Quest.priest: lambda state: self.can_wear_costume(state, Costume.priest),
            Quest.alley_cat: lambda state: self.can_triple_jump(state) and state.has(Upgrade.bewitched_bubble, self.player),
            Quest.tatils_tale: lambda state: state.has(QuestEventItem.tatil_2, self.player) and state.has(QuestItem.deed, self.player) and
                                             self.can_wear_costume(state, Costume.pigman),
            Quest.signing_bonus: lambda state: state.has(QuestItem.maid_contract, self.player) and self.can_wear_costume(state, Costume.maid),

            Quest.cardio_day: lambda state: self.can_wear_costume(state, Costume.rat),
            Quest.panty_raid: lambda state: state.has(QuestItem.clothes, self.player) and self.can_present_gender(state, "Male"),
            Quest.unlucky_cat: lambda state: state.has(QuestItem.soul_fragment, self.player, 3) and
                                             state.has(QuestEventItem.cat_statue_1, self.player) and
                                             state.has(QuestEventItem.cat_statue_2, self.player) and
                                             state.has(QuestEventItem.cat_statue_3, self.player),
            Quest.harvest_season: lambda state: self.can_wear_costume(state, Costume.farmer),
            Quest.long_distance: lambda state: state.has(QuestEventItem.goat_guy, self.player) and state.has(QuestItem.demonic_letter, self.player),
            Quest.summoning_stones: lambda state: state.has(QuestItem.summon_stone, self.player, 3) and
                                                  state.has(QuestEventItem.stone_1, self.player) and state.has(QuestEventItem.stone_2, self.player)
                                                  and state.has(QuestEventItem.stone_3, self.player),
            Quest.semen_with_a: lambda state: self.can_wear_costume(state, Costume.angler) and state.has(Key.frog_boss, self.player),

            Gacha.gacha_sp1: lambda state: state.has(Coin.promotional_coin, self.player),
            Gacha.gacha_ad1: lambda state: self.has_enough_coins(Gacha.gacha_ad1, state),
            Gacha.gacha_ad2: lambda state: self.has_enough_coins(Gacha.gacha_ad2, state),
            Gacha.gacha_ad3: lambda state: self.has_enough_coins(Gacha.gacha_ad3, state),
            Gacha.gacha_ad4: lambda state: self.has_enough_coins(Gacha.gacha_ad4, state),
            Gacha.gacha_ad5: lambda state: self.has_enough_coins(Gacha.gacha_ad5, state),
            Gacha.gacha_ad6: lambda state: self.has_enough_coins(Gacha.gacha_ad6, state),
            Gacha.gacha_ad7: lambda state: self.has_enough_coins(Gacha.gacha_ad7, state),
            Gacha.gacha_ad8: lambda state: self.has_enough_coins(Gacha.gacha_ad8, state),
            Gacha.gacha_ad9: lambda state: self.has_enough_coins(Gacha.gacha_ad9, state),
            Gacha.gacha_ad0: lambda state: self.has_enough_coins(Gacha.gacha_ad0, state),
            Gacha.gacha_mg1: lambda state: self.has_enough_coins(Gacha.gacha_mg1, state),
            Gacha.gacha_mg2: lambda state: self.has_enough_coins(Gacha.gacha_mg2, state),
            Gacha.gacha_mg3: lambda state: self.has_enough_coins(Gacha.gacha_mg3, state),
            Gacha.gacha_mg4: lambda state: self.has_enough_coins(Gacha.gacha_mg4, state),
            Gacha.gacha_mg5: lambda state: self.has_enough_coins(Gacha.gacha_mg5, state),
            Gacha.gacha_mg6: lambda state: self.has_enough_coins(Gacha.gacha_mg6, state),
            Gacha.gacha_mg7: lambda state: self.has_enough_coins(Gacha.gacha_mg7, state),
            Gacha.gacha_mg8: lambda state: self.has_enough_coins(Gacha.gacha_mg8, state),
            Gacha.gacha_mg9: lambda state: self.has_enough_coins(Gacha.gacha_mg9, state),
            Gacha.gacha_mg0: lambda state: self.has_enough_coins(Gacha.gacha_mg0, state),
            Gacha.gacha_bg1: lambda state: self.has_enough_coins(Gacha.gacha_bg1, state),
            Gacha.gacha_bg2: lambda state: self.has_enough_coins(Gacha.gacha_bg2, state),
            Gacha.gacha_bg3: lambda state: self.has_enough_coins(Gacha.gacha_bg3, state),
            Gacha.gacha_bg4: lambda state: self.has_enough_coins(Gacha.gacha_bg4, state),
            Gacha.gacha_bg5: lambda state: self.has_enough_coins(Gacha.gacha_bg5, state),
            Gacha.gacha_bg6: lambda state: self.has_enough_coins(Gacha.gacha_bg6, state),
            Gacha.gacha_bg7: lambda state: self.has_enough_coins(Gacha.gacha_bg7, state),
            Gacha.gacha_bg8: lambda state: self.has_enough_coins(Gacha.gacha_bg8, state),
            Gacha.gacha_bg9: lambda state: self.has_enough_coins(Gacha.gacha_bg9, state),
            Gacha.gacha_bg0: lambda state: self.has_enough_coins(Gacha.gacha_bg0, state),
            Gacha.gacha_ag1: lambda state: self.has_enough_coins(Gacha.gacha_ag1, state),
            Gacha.gacha_ag2: lambda state: self.has_enough_coins(Gacha.gacha_ag2, state),
            Gacha.gacha_ag3: lambda state: self.has_enough_coins(Gacha.gacha_ag3, state),
            Gacha.gacha_ag4: lambda state: self.has_enough_coins(Gacha.gacha_ag4, state),
            Gacha.gacha_ag5: lambda state: self.has_enough_coins(Gacha.gacha_ag5, state),
            Gacha.gacha_ag6: lambda state: self.has_enough_coins(Gacha.gacha_ag6, state),
            Gacha.gacha_ag7: lambda state: self.has_enough_coins(Gacha.gacha_ag7, state),
            Gacha.gacha_ag8: lambda state: self.has_enough_coins(Gacha.gacha_ag8, state),
            Gacha.gacha_ag9: lambda state: self.has_enough_coins(Gacha.gacha_ag9, state),
            Gacha.gacha_ag0: lambda state: self.has_enough_coins(Gacha.gacha_ag0, state),
        }

    def can_roll(self, state: CollectionState) -> bool:
        return not self.world.options.shuffle_dodge or state.has(Upgrade.orb_of_avoidance, self.player)
    
    def can_ghost_dodge(self, state: CollectionState) -> bool:
        return state.has(Power.ghost_form, self.player) and (self.can_roll(state) or state.has(Upgrade.demon_wings, self.player))

    def can_double_jump(self, state: CollectionState) -> bool:
        return not self.world.options.shuffle_double_jump or state.has(Upgrade.rose_ribbon, self.player) or state.has(Upgrade.angel_feathers, self.player)

    def can_triple_jump(self, state: CollectionState):
        return state.has(Upgrade.angel_feathers, self.player) and (not self.world.options.shuffle_double_jump or state.has(Upgrade.rose_ribbon, self.player))

    def can_warp(self, area: int, state: CollectionState) -> bool:
        return self.world.options.starting_area.value == area or state.has(Warp.area_to_warp[area], self.player)

    def seen_enough_sex_scenes(self, state: CollectionState, amount: int):
        return state.has(Custom.sex_experience, self.player, amount)

    def can_move_horizontally_enough(self, state: CollectionState):
        return state.has(Upgrade.angel_feathers, self.player) or state.has(Upgrade.demon_wings, self.player)

    def can_wear_costume(self, state: CollectionState, costume: str):
        if costume in Costume.male_costumes:
            return state.has(costume, self.player) and self.can_present_gender(state, "Male")
        else:
            return state.has(costume, self.player) and self.can_present_gender(state, "Female")

    def can_present_gender(self, state: CollectionState, gender: str):
        if self.world.options.starting_gender == self.world.options.starting_gender.option_male:
            return state.has(Upgrade.bewitched_bubble, self.player) or gender == "Male"
        else:
            return state.has(Upgrade.bewitched_bubble, self.player) or gender == "Female"

    def has_enough_coins(self, gacha: str, state: CollectionState):
        if "Animal" in gacha:
            amount = self.animal_order.index(gacha) + 1
            return state.has(Coin.animal_coin, self.player, amount)
        if "Bunny" in gacha:
            amount = self.bunny_order.index(gacha) + 1
            return state.has(Coin.bunny_coin, self.player, amount)
        if "Monster" in gacha:
            amount = self.monster_order.index(gacha) + 1
            return state.has(Coin.monster_coin, self.player, amount)
        if "Angel" in gacha:
            amount = self.angel_order.index(gacha) + 1
            return state.has(Coin.angel_demon_coin, self.player, amount)
        return False

    def has_upgrade_stage(self, stage: int, state: CollectionState):
        return state.has(Upgrade.health, self.player, stage) and state.has(Upgrade.peachy_peach, self.player, stage)

    def set_flipwitch_rules(self, animal_order: List[str], bunny_order: List[str], monster_order: List[str], angel_order: List[str]) -> None:
        self.angel_order = angel_order
        self.bunny_order = bunny_order
        self.monster_order = monster_order
        self.animal_order = animal_order
        multiworld = self.world.multiworld
        for region in multiworld.get_regions(self.player):
            if region.name in self.region_rules:
                for entrance in region.entrances:
                    entrance.access_rule = self.region_rules[region.name]
                for location in region.locations:
                    location.access_rule = self.region_rules[region.name]
            for entrance in region.entrances:
                multiworld.register_indirect_condition(region, entrance)
                if entrance.name in self.entrance_rules:
                    entrance.access_rule = entrance.access_rule and self.entrance_rules[entrance.name]
            for loc in region.locations:
                if loc.name in self.location_rules:
                    loc.access_rule = loc.access_rule and self.location_rules[loc.name]
