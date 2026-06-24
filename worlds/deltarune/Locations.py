from BaseClasses import Location, LocationProgressType
from typing import TYPE_CHECKING, NamedTuple, Optional, Callable
from enum import Enum, IntEnum

if TYPE_CHECKING:
    from . import DeltaruneWorld


class LocationGroups(str, Enum):
    castle_town = "Castle Town"
    cross_chapter = "Cross Chapter"
    chapter1 = "Chapter 1"
    chapter2 = "Chapter 2"
    chapter3 = "Chapter 3"
    chapter4 = "Chapter 4"


class DeltaruneLocation(Location):
    game: str = "Deltarune"


class LocationIDs(IntEnum):
    ch1_unknown_hidden_item = 1
    ch1_field_dark_candy_tree_1 = 2
    ch1_field_dark_candy_tree_2 = 3
    ch1_field_dark_candy_tree_3 = 4
    ch1_field_dark_candy_tree_4 = 5
    ch1_bake_sale_repair_top_cake = 6
    ch1_bake_sale_diamond_stand = 7
    ch1_bake_sale_heart_stand = 8
    ch1_bake_sale_spade_stand = 9
    ch1_card_castle_rudinn_gift = 10
    ch1_field_return_top_cake = 11
    ch1_castle_town_manual = 12
    ch1_field_maze_of_death_chest = 13
    ch1_field_chest_before_great_board = 14
    ch1_forest_scissor_dancers_chest = 15
    ch1_forest_hidden_chest_near_dancers = 16
    ch1_forest_coat_rack_chest = 17
    ch1_forest_letter_block_chest = 18
    ch1_forest_chest_near_worm = 19
    ch1_card_castle_2f_chest = 20
    ch1_card_castle_4f_chest = 21
    ch1_throw_away_manual = 22
    ch1_field_brokencake = 23
    ch1_forest_man = 24
    ch1_card_castle_jevil_1 = 25
    ch1_card_castle_jevil_2 = 26
    ch1_card_castle_jevil_3 = 27
    ch1_bake_sale_repair_door_key = 28
    ch1_seam_seap_talk_about_strange_prisoner = 29
    ch1_card_castle_ironshackle = 30
    ch1_field_warp_door = 31
    ch1_forest_warp_door = 32
    ch1_bake_sale_warp_door = 33
    ch1_card_castle_warp_door = 34
    ch1_card_castle_moss = 35
    ch2_castle_town_jigsaw_joe_challenge = 36
    ch2_castle_town_graze_challenge_1 = 37
    ch2_castle_town_clover_rematch_challenge = 38
    ch2_castle_town_top_chef_gift = 39
    cc_castle_town_dd_burger_fusion = 40
    cc_castle_town_silver_card_fusion = 41
    cc_castle_town_spike_band_fusion = 42
    ch2_cyber_field_first_chest = 43
    ch2_cyber_field_nubert_chest = 44
    ch2_cyber_field_tasque_maze_checkmark = 45
    ch2_cyber_field_chest_near_music_shop = 46
    ch2_cyber_field_virovirokun_puzzle_chest = 47
    ch2_cyber_field_teacup_puzzle_chest = 48
    ch2_recruit_werewire = 49
    ch1_seam_seap_1 = 50
    ch1_seam_seap_2 = 51
    ch1_seam_seap_3 = 52
    ch1_seam_seap_4 = 53
    ch2_recruit_tasque = 54
    ch2_recruit_virovirokun = 55
    ch2_trash_zone_trash_can = 56
    ch2_cyber_city_trash_can_1 = 57
    ch2_cyber_city_trash_can_2 = 58
    ch2_cyber_city_queen_poster_chest = 59
    ch1_rouxls_shop_1 = 60
    ch1_rouxls_shop_2 = 61
    ch1_rouxls_shop_3 = 62
    ch1_rouxls_shop_4 = 63
    ch2_cyber_city_chest_guarded_by_virovirokun = 64
    ch2_cyber_city_purchase_mannequin = 65
    ch2_cyber_city_annoying_dog = 66
    ch2_cyber_city_man = 67
    ch2_cyber_city_cheese_maze_chest = 68
    ch2_cyber_city_trash_can_3 = 69
    ch2_music_shop_1 = 70
    ch2_music_shop_2 = 71
    ch2_music_shop_3 = 72
    ch2_music_shop_4 = 73
    ch2_cyber_city_trash_can_4 = 74
    ch2_cyber_city_trash_can_5 = 75
    ch2_recruit_poppup = 76
    ch2_recruit_ambyu_lance = 77
    ch2_recruit_maus = 78
    ch2_mansion_painting_chest = 79
    ch2_swatchs_cafe_1 = 80
    ch2_swatchs_cafe_2 = 81
    ch2_swatchs_cafe_3 = 82
    ch2_swatchs_cafe_4 = 83
    ch2_mansion_sculpture_room_chest = 84
    ch2_mansion_platter_chest = 85
    ch2_mansion_tunnel_of_love_chest = 86
    ch2_recruit_swatchling = 87
    ch2_recruit_tasque_manager = 88
    ch2_recruit_mauswheel = 89
    ch2_spamton_shop_1 = 90
    ch2_spamton_shop_2 = 91
    ch2_spamton_shop_3 = 92
    ch2_spamton_shop_4 = 93
    ch2_recruit_werewerewire = 94
    ch2_mansion_basement_chest = 95
    ch2_mansion_basement_mechanism = 96
    ch2_mansion_spamton_neo_defeat_item_1 = 97
    ch2_mansion_spamton_neo_defeat_item_2 = 98
    ch2_mansion_spamton_neo_defeat_item_3 = 99
    ch2_castle_town_tasque_manager_says_challenge = 100
    ch2_castle_town_all_stars_challenge = 101
    cc_castle_town_twin_ribbon_fusion = 102
    cc_castle_town_tensionbow_fusion = 103
    ch2_cyber_field_warp_door = 104
    ch2_trash_zone_warp_door = 105
    ch2_mansion_warp_door = 106
    ch2_cyber_city_moss = 107
    ch2_cyber_city_purchase_kris_tea = 108
    ch2_cyber_city_purchase_noelle_tea = 109
    ch2_cyber_city_purchase_susie_tea = 110
    ch2_cyber_city_purchase_ralsei_tea = 111
    ch2_cyber_city_purchase_freezering = 112
    ch2_cyber_city_purchase_thornring = 113
    ch3_couch_cliffs_dust_pile_chest = 114
    ch3_board_1_c_rank = 115
    ch3_board_1_b_rank = 116
    ch3_board_1_a_rank = 117
    ch3_board_1_s_rank = 118
    ch3_board_1_t_rank = 119
    ch3_green_room_vending_machine_1 = 120
    ch3_green_room_vending_machine_2 = 121
    ch3_green_room_vending_machine_3 = 122
    ch3_green_room_vending_machine_4 = 123
    ch3_green_room_vending_machine_5 = 124
    ch3_green_room_vending_machine_6 = 125
    ch3_green_room_vending_machine_7 = 126
    ch3_green_room_vending_machine_8 = 127
    ch3_green_room_board_1_ramb_gift = 128
    ch3_recruit_water_cooler = 129
    ch3_b_rank_room_golden_prize_1 = 130
    ch3_b_rank_room_golden_prize_2 = 131
    ch3_b_rank_room_golden_prize_3 = 132
    ch3_b_rank_room_golden_prize_4 = 133
    ch3_b_rank_room_golden_prize_5 = 134
    ch3_s_rank_room_person_behind_curtain = 136
    ch3_s_rank_room_vending_machine_1 = 137
    ch3_s_rank_room_vending_machine_2 = 138
    ch3_s_rank_room_vending_machine_3 = 139
    ch3_s_rank_room_vending_machine_4 = 140
    ch3_s_rank_room_oddcontroller = 141
    ch3_board_2_c_rank = 142
    ch3_board_2_b_rank = 143
    ch3_board_2_a_rank = 144
    ch3_board_2_s_rank = 145
    ch3_board_2_t_rank = 146
    ch3_green_room_board_2_ramb_gift = 147
    ch3_tv_world_chest_near_shadowmen = 148
    ch3_tv_world_board_puzzle_1_chest = 149
    ch3_tv_world_trash_can_1 = 150
    ch3_tv_world_trash_can_2 = 151
    ch3_tv_world_trash_can_3 = 152
    ch3_tv_world_water_cooler_chest = 153
    ch3_tv_world_trash_can_4 = 154
    ch3_tv_world_trash_can_5 = 155
    ch3_tv_world_board_puzzle_2_chest = 156
    ch3_tv_world_serious_trashy_chest = 157
    ch3_tv_world_bonus_zone_chest_1 = 158
    ch3_tv_world_bonus_zone_chest_2 = 159
    ch3_tv_world_bonus_zone_chest_3 = 160
    ch3_recruit_elnina = 161
    ch3_recruit_lanino = 162
    ch3_tv_world_chest_outside_green_room = 163
    ch3_recruit_shadowguy = 164
    ch3_recruit_shuttah = 165
    ch3_recruit_zapper = 166
    ch3_recruit_ribbick = 167
    ch3_recruit_pippins = 168
    ch3_tv_world_tripticket = 169
    ch3_tv_world_man = 170
    ch3_mantle_defeat = 171
    ch3_cold_place_knight_defeat_item_1 = 172
    ch3_cold_place_knight_defeat_item_2 = 173
    ch3_couch_cliffs_warp_door = 174
    ch3_green_room_warp_door = 175
    ch3_tv_world_entrance_warp_door = 176
    ch3_tv_world_goulden_sam_warp_door = 177
    ch3_board_1_extra_key = 179
    ch3_board_2_extra_photo = 180
    ch3_board_2_moss = 181
    ch3_mantle_out_of_bounds_chest = 182
    ch3_mantle_northern_light_item = 183
    ch3_mantle_susie_gift = 184
    ch1_fountain_sealed = 185
    ch2_fountain_sealed = 186
    ch3_fountain_sealed = 187
    ch4_castle_town_lanino_elnina_challenge = 188
    ch4_castle_town_top_chef_gift = 189
    ch4_dark_sanctuary_jockington_prophecy_chest = 190
    ch4_dark_sanctuary_chest_in_first_dark_area = 191
    ch4_old_man_shop_1 = 192
    ch4_old_man_shop_2 = 193
    ch4_old_man_shop_3 = 194
    ch4_old_man_shop_4 = 195
    ch4_dark_sanctuary_library_chest_1 = 196
    ch4_dark_sanctuary_worship_room_chest = 197
    ch4_dark_sanctuary_lantern_puzzle_chest = 198
    ch4_dark_sanctuary_library_chest_2 = 199
    ch4_dark_sanctuary_jackenstein_gift = 200
    ch4_dark_sanctuary_climbing_tutorial_chest = 201
    ch4_dark_sanctuary_cuptain_pillar_chest = 202
    ch4_dark_sanctuary_sleeping_mizzle_chest = 203
    ch4_dark_sanctuary_hidden_climbing_chest = 204
    ch4_dark_sanctuary_sheetmusic = 205
    ch4_dark_sanctuary_hammer_of_justice_defeat_item_1 = 206
    ch4_dark_sanctuary_hammer_of_justice_defeat_item_2 = 207
    ch4_dark_sanctuary_fountain_sealed = 208
    ch4_second_sanctuary_wall_climbing_chest = 209
    ch4_second_sanctuary_waterfall_chest = 210
    ch4_second_sanctuary_man = 211
    ch4_second_sanctuary_gallery_prophecy_chest = 212
    ch4_second_sanctuary_fountain_sealed = 213
    ch4_third_sanctuary_annoying_dog = 214
    ch4_third_sanctuary_speed_climbing_chest = 215
    ch4_third_sanctuary_dark_area_chest = 216
    ch4_recruit_guei = 217
    ch4_recruit_balthizard = 218
    ch4_recruit_bibliox = 219
    ch4_recruit_mizzle = 220
    ch4_recruit_miss_mizzle = 221
    ch4_recruit_wicabel = 222
    ch4_recruit_winglade = 223
    ch4_recruit_organikk = 224
    ch4_third_sanctuary_fountain_sealed = 225
    ch4_second_sanctuary_moss = 226
    ch4_third_sanctuary_titan_defeat = 227
    ch4_second_sanctuary_destroyed_piano_block_chest = 228
    ch2_cyber_field_teacup_ride_checkmark = 229
    ch2_cyber_field_giasfelfebrehber_checkmark = 230
    ch4_castle_town_mike_defeat = 231
    ch4_mike_battat_bronze = 232
    ch4_mike_battat_silver = 233
    ch4_mike_battat_gold = 234
    ch4_mike_battat_platinum = 235
    ch4_mike_jongler_bronze = 236
    ch4_mike_jongler_silver = 237
    ch4_mike_jongler_gold = 238
    ch4_mike_jongler_platinum = 239
    ch4_mike_pluey_bronze = 240
    ch4_mike_pluey_silver = 241
    ch4_mike_pluey_gold = 242
    ch4_mike_pluey_platinum = 243
    cc_castle_town_twistedsword_fusion = 244
    ch1_throw_away_manual_again = 245
    ch2_cyber_field_fun_gang_actions_unlock = 246
    ch3_board_1_extra_extra_key = 247
    ch1_recruit_hathy = 248
    ch1_recruit_ponman = 249
    ch1_recruit_rabbick = 250
    ch1_recruit_bloxer = 251
    ch1_recruit_jigsawry = 252
    ch1_recruit_rudinn_ranger = 253
    ch1_recruit_head_hathy = 254
    ch1_recruit_rudinn = 255
    ch3_board_1_z_rank = 256
    ch3_board_2_z_rank = 257
    ch2_lost_werewire = 1049
    ch2_lost_tasque = 1054
    ch2_lost_virovirokun = 1055
    ch2_lost_poppup = 1076
    ch2_lost_ambyu_lance = 1077
    ch2_lost_maus = 1078
    ch2_lost_swatchlings = 1087
    ch2_lost_tasque_manager = 1088
    ch2_lost_mauswheel = 1089
    ch2_lost_werewerewire = 1094
    ch3_lost_water_cooler = 1129
    ch3_lost_shadowguy = 1164
    ch3_lost_shuttah = 1165
    ch3_lost_zapper = 1166
    ch3_lost_ribbick = 1167
    ch3_lost_pippins = 1168
    ch4_lost_guei = 1217
    ch4_lost_balthizard = 1218
    ch4_lost_bibliox = 1219
    ch4_lost_mizzle = 1220
    ch4_lost_miss_mizzle = 1221
    ch4_lost_wicabel = 1222
    ch4_lost_winglade = 1223
    ch4_lost_organikk = 1224
    ch1_lost_hathy = 1248
    ch1_lost_ponman = 1249
    cc_lost_rabbick = 1250
    ch1_lost_bloxer = 1251
    ch1_lost_jigsawry = 1252
    ch1_lost_rudinn_ranger = 1253
    ch1_lost_head_hathy = 1254
    ch1_lost_rudinn = 1255


locations = {
    LocationIDs.cc_castle_town_twin_ribbon_fusion: "Castle Town - Twin Ribbon Fusion",
    LocationIDs.cc_castle_town_tensionbow_fusion: "Castle Town - TensionBow Fusion",
    LocationIDs.cc_castle_town_dd_burger_fusion: "Castle Town - DD-Burger Fusion",
    LocationIDs.cc_castle_town_silver_card_fusion: "Castle Town - Silver Card Fusion",
    LocationIDs.cc_castle_town_spike_band_fusion: "Castle Town - Spike Band Fusion",
    LocationIDs.cc_castle_town_twistedsword_fusion: "Castle Town - TwistedSwd Fusion",
    LocationIDs.ch1_unknown_hidden_item: "CH1: ?????? - Hidden Item",
    LocationIDs.ch1_castle_town_manual: "CH1: Castle Town - Manual",
    LocationIDs.ch1_throw_away_manual: "CH1: Throw Away Manual",
    LocationIDs.ch1_throw_away_manual_again: "CH1: Throw Away Manual (Again...)",
    LocationIDs.ch1_field_warp_door: "CH1: Fields - Warp Door",
    LocationIDs.ch1_field_dark_candy_tree_1: "CH1: Fields - Dark Candy Tree 1",
    LocationIDs.ch1_field_dark_candy_tree_2: "CH1: Fields - Dark Candy Tree 2",
    LocationIDs.ch1_field_dark_candy_tree_3: "CH1: Fields - Dark Candy Tree 3",
    LocationIDs.ch1_field_dark_candy_tree_4: "CH1: Fields - Dark Candy Tree 4",
    LocationIDs.ch1_field_brokencake: "CH1: Fields - BrokenCake",
    LocationIDs.ch1_field_return_top_cake: "CH1: Fields - Return Top Cake",
    LocationIDs.ch1_field_maze_of_death_chest: "CH1: Fields - Maze of Death Chest",
    LocationIDs.ch1_field_chest_before_great_board: "CH1: Fields - Chest Before Great Board",
    LocationIDs.ch1_seam_seap_talk_about_strange_prisoner: "CH1: Seam's Seap - Talk About Strange Prisoner",
    LocationIDs.ch1_seam_seap_1: "CH1: Seam's Seap 1",
    LocationIDs.ch1_seam_seap_2: "CH1: Seam's Seap 2",
    LocationIDs.ch1_seam_seap_3: "CH1: Seam's Seap 3",
    LocationIDs.ch1_seam_seap_4: "CH1: Seam's Seap 4",
    LocationIDs.ch1_forest_warp_door: "CH1: Forest - Warp Door",
    LocationIDs.ch1_forest_scissor_dancers_chest: "CH1: Forest - Scissor Dancers Chest",
    LocationIDs.ch1_forest_hidden_chest_near_dancers: "CH1: Forest - Hidden Chest Near Dancers",
    LocationIDs.ch1_forest_coat_rack_chest: "CH1: Forest - Coat Rack's Chest",
    LocationIDs.ch1_forest_letter_block_chest: "CH1: Forest - Letter Block Chest",
    LocationIDs.ch1_forest_chest_near_worm: "CH1: Forest - Chest Near Worm",
    LocationIDs.ch1_forest_man: "CH1: Forest - Man",
    LocationIDs.ch1_bake_sale_warp_door: "CH1: Bake Sale - Warp Door",
    LocationIDs.ch1_bake_sale_repair_top_cake: "CH1: Bake Sale - Repair Top Cake",
    LocationIDs.ch1_bake_sale_repair_door_key: "CH1: Bake Sale - Repair Door Key",
    LocationIDs.ch1_bake_sale_diamond_stand: "CH1: Bake Sale - Diamond Stand",
    LocationIDs.ch1_bake_sale_heart_stand: "CH1: Bake Sale - Heart Stand",
    LocationIDs.ch1_bake_sale_spade_stand: "CH1: Bake Sale - Spade Stand",
    LocationIDs.ch1_card_castle_warp_door: "CH1: Card Castle - Warp Door",
    LocationIDs.ch1_card_castle_ironshackle: "CH1: Card Castle - IronShackle",
    LocationIDs.ch1_card_castle_moss: "CH1: Card Castle - Moss",
    LocationIDs.ch1_card_castle_rudinn_gift: "CH1: Card Castle - Rudinn Gift",
    LocationIDs.ch1_card_castle_2f_chest: "CH1: Card Castle - 2F Chest",
    LocationIDs.ch1_card_castle_4f_chest: "CH1: Card Castle - 4F Chest",
    LocationIDs.ch1_card_castle_jevil_1: "CH1: Card Castle - Jevil Defeat Item #1",
    LocationIDs.ch1_card_castle_jevil_2: "CH1: Card Castle - Jevil Defeat Item #2",
    LocationIDs.ch1_card_castle_jevil_3: "CH1: Card Castle - Jevil Defeat Item #3",
    LocationIDs.ch1_rouxls_shop_1: "CH1: Rouxls' Shop 1",
    LocationIDs.ch1_rouxls_shop_2: "CH1: Rouxls' Shop 2",
    LocationIDs.ch1_rouxls_shop_3: "CH1: Rouxls' Shop 3",
    LocationIDs.ch1_rouxls_shop_4: "CH1: Rouxls' Shop 4",
    LocationIDs.ch1_fountain_sealed: "CH1: Card Kingdom - Fountain Sealed",
    LocationIDs.ch1_recruit_rudinn: "CH1: Fields - Recruit Rudinn",
    LocationIDs.ch1_recruit_hathy: "CH1: Fields - Recruit Hathy",
    LocationIDs.ch1_recruit_jigsawry: "CH1: Fields - Recruit Jigsawry",
    LocationIDs.ch1_recruit_ponman: "CH1: Great Board - Recruit Ponman",
    LocationIDs.ch1_recruit_rabbick: "CH1: Forest - Recruit Rabbick",
    LocationIDs.ch1_recruit_bloxer: "CH1: Forest - Recruit Bloxer",
    LocationIDs.ch1_recruit_rudinn_ranger: "CH1: Card Castle - Recruit Rudinn Ranger",
    LocationIDs.ch1_recruit_head_hathy: "CH1: Card Castle - Recruit Head Hathy",
    LocationIDs.ch1_lost_rudinn: "CH1: Fields - Lost Rudinn",
    LocationIDs.ch1_lost_hathy: "CH1: Fields - Lost Hathy",
    LocationIDs.ch1_lost_jigsawry: "CH1: Fields - Lost Jigsawry",
    LocationIDs.ch1_lost_ponman: "CH1: Great Board - Lost Ponman",
    LocationIDs.cc_lost_rabbick: "Cross Chapter - Lost Rabbick",
    LocationIDs.ch1_lost_bloxer: "CH1: Forest - Lost Bloxer",
    LocationIDs.ch1_lost_rudinn_ranger: "CH1: Card Castle - Lost Rudinn Ranger",
    LocationIDs.ch1_lost_head_hathy: "CH1: Card Castle - Lost Head Hathy",
    LocationIDs.ch2_castle_town_jigsaw_joe_challenge: "CH2: Castle Town - Jigsaw Joe Challenge",
    LocationIDs.ch2_castle_town_graze_challenge_1: "CH2: Castle Town - Graze Challenge 1",
    LocationIDs.ch2_castle_town_clover_rematch_challenge: "CH2: Castle Town - Clover Rematch Challenge",
    LocationIDs.ch2_castle_town_tasque_manager_says_challenge: "CH2: Castle Town - Tasque Manager Says Challenge",
    LocationIDs.ch2_castle_town_all_stars_challenge: "CH2: Castle Town - Ch2 All Stars Challenge",
    LocationIDs.ch2_castle_town_top_chef_gift: "CH2: Castle Town - Top Chef Gift",
    LocationIDs.ch2_cyber_field_first_chest: "CH2: Cyber Field - First Chest",
    LocationIDs.ch2_cyber_field_nubert_chest: "CH2: Cyber Field - Nubert's Chest",
    LocationIDs.ch2_cyber_field_tasque_maze_checkmark: "CH2: Cyber Field - Tasque Maze Checkmark",
    LocationIDs.ch2_cyber_field_teacup_ride_checkmark: "CH2: Cyber Field - Teacup Ride Checkmark",
    LocationIDs.ch2_cyber_field_giasfelfebrehber_checkmark: "CH2: Cyber Field - Giasfelfebrehber Checkmark",
    LocationIDs.ch2_cyber_field_fun_gang_actions_unlock: "CH2: Cyber Field - S/R/N-Actions unlock",
    LocationIDs.ch2_cyber_field_chest_near_music_shop: "CH2: Cyber Field - Chest Near Music Shop",
    LocationIDs.ch2_cyber_field_virovirokun_puzzle_chest: "CH2: Cyber Field - Virovirokun Puzzle Chest",
    LocationIDs.ch2_cyber_field_teacup_puzzle_chest: "CH2: Cyber Field - Teacup Puzzle Chest",
    LocationIDs.ch2_music_shop_1: "CH2: Music Shop 1",
    LocationIDs.ch2_music_shop_2: "CH2: Music Shop 2",
    LocationIDs.ch2_music_shop_3: "CH2: Music Shop 3",
    LocationIDs.ch2_music_shop_4: "CH2: Music Shop 4",
    LocationIDs.ch2_trash_zone_trash_can: "CH2: Trash Zone - Trash Can",
    LocationIDs.ch2_cyber_city_trash_can_1: "CH2: Cyber City - Trash Can #1",
    LocationIDs.ch2_cyber_city_trash_can_2: "CH2: Cyber City - Trash Can #2",
    LocationIDs.ch2_cyber_city_queen_poster_chest: "CH2: Cyber City - Queen Poster Chest",
    LocationIDs.ch2_cyber_city_chest_guarded_by_virovirokun: "CH2: Cyber City - Chest Guarded By Virovirokun",
    LocationIDs.ch2_cyber_city_purchase_mannequin: "CH2: Cyber City - Purchase Mannequin",
    LocationIDs.ch2_cyber_city_annoying_dog: "CH2: Cyber City - Annoying Dog...?",
    LocationIDs.ch2_cyber_city_man: "CH2: Cyber City - Man",
    LocationIDs.ch2_cyber_city_moss: "CH2: Cyber City - Moss",
    LocationIDs.ch2_cyber_city_purchase_kris_tea: "CH2: Cyber City - Purchase Kris Tea",
    LocationIDs.ch2_cyber_city_purchase_noelle_tea: "CH2: Cyber City - Purchase Noelle Tea",
    LocationIDs.ch2_cyber_city_purchase_susie_tea: "CH2: Cyber City - Purchase Susie Tea",
    LocationIDs.ch2_cyber_city_purchase_ralsei_tea: "CH2: Cyber City - Purchase Ralsei Tea",
    LocationIDs.ch2_cyber_city_cheese_maze_chest: "CH2: Cyber City - Cheese Maze Chest",
    LocationIDs.ch2_cyber_city_trash_can_3: "CH2: Cyber City - Trash Can #3",
    LocationIDs.ch2_cyber_city_trash_can_4: "CH2: Cyber City - Trash Can #4",
    LocationIDs.ch2_cyber_city_trash_can_5: "CH2: Cyber City - Trash Can #5",
    LocationIDs.ch2_mansion_painting_chest: "CH2: Mansion - Painting Chest",
    LocationIDs.ch2_mansion_sculpture_room_chest: "CH2: Mansion - Sculpture Room Chest",
    LocationIDs.ch2_mansion_platter_chest: "CH2: Mansion - Platter Chest",
    LocationIDs.ch2_mansion_tunnel_of_love_chest: "CH2: Mansion - Tunnel of Love Chest",
    LocationIDs.ch2_mansion_basement_chest: "CH2: Mansion - Basement Chest",
    LocationIDs.ch2_mansion_basement_mechanism: "CH2: Mansion - Basement Mechanism",
    LocationIDs.ch2_mansion_spamton_neo_defeat_item_1: "CH2: Mansion - Spamton NEO Defeat Item #1",
    LocationIDs.ch2_mansion_spamton_neo_defeat_item_2: "CH2: Mansion - Spamton NEO Defeat Item #2",
    LocationIDs.ch2_mansion_spamton_neo_defeat_item_3: "CH2: Mansion - Spamton NEO Defeat Item #3",
    LocationIDs.ch2_swatchs_cafe_1: "CH2: Swatch's Cafe 1",
    LocationIDs.ch2_swatchs_cafe_2: "CH2: Swatch's Cafe 2",
    LocationIDs.ch2_swatchs_cafe_3: "CH2: Swatch's Cafe 3",
    LocationIDs.ch2_swatchs_cafe_4: "CH2: Swatch's Cafe 4",
    LocationIDs.ch2_spamton_shop_1: "CH2: Spamton's Shop 1",
    LocationIDs.ch2_spamton_shop_2: "CH2: Spamton's Shop 2",
    LocationIDs.ch2_spamton_shop_3: "CH2: Spamton's Shop 3",
    LocationIDs.ch2_spamton_shop_4: "CH2: Spamton's Shop 4",
    LocationIDs.ch2_fountain_sealed: "CH2: Cyber World - Fountain Sealed",
    LocationIDs.ch2_cyber_field_warp_door: "CH2: Cyber Field - Warp Door",
    LocationIDs.ch2_trash_zone_warp_door: "CH2: Trash Zone - Warp Door",
    LocationIDs.ch2_mansion_warp_door: "CH2: Mansion - Warp Door",
    LocationIDs.ch2_recruit_werewire: "CH2: Recruit Werewire",
    LocationIDs.ch2_recruit_tasque: "CH2: Recruit Tasque",
    LocationIDs.ch2_recruit_virovirokun: "CH2: Recruit Virovirokun",
    LocationIDs.ch2_recruit_poppup: "CH2: Recruit Poppup",
    LocationIDs.ch2_recruit_ambyu_lance: "CH2: Recruit Ambyu-lance",
    LocationIDs.ch2_recruit_maus: "CH2: Recruit Maus",
    LocationIDs.ch2_recruit_swatchling: "CH2: Recruit Swatchling",
    LocationIDs.ch2_recruit_tasque_manager: "CH2: Recruit Tasque Manager",
    LocationIDs.ch2_recruit_mauswheel: "CH2: Recruit Mauswheel",
    LocationIDs.ch2_recruit_werewerewire: "CH2: Recruit Werewerewire",
    LocationIDs.ch2_cyber_city_purchase_freezering: """CH2: Cyber City - "Purchase" FreezeRing""",
    LocationIDs.ch2_cyber_city_purchase_thornring: "CH2: Cyber City - Purchase ThornRing",
    LocationIDs.ch2_lost_werewire: "CH2: Lost Werewire",
    LocationIDs.ch2_lost_tasque: "CH2: Lost Tasque",
    LocationIDs.ch2_lost_virovirokun: "CH2: Lost Virovirokun",
    LocationIDs.ch2_lost_poppup: "CH2: Lost Poppup",
    LocationIDs.ch2_lost_ambyu_lance: "CH2: Lost Ambyu-lance",
    LocationIDs.ch2_lost_maus: "CH2: Lost Maus",
    LocationIDs.ch2_lost_swatchlings: "CH2: Lost Swatchling",
    LocationIDs.ch2_lost_tasque_manager: "CH2: Lost Tasque Manager",
    LocationIDs.ch2_lost_mauswheel: "CH2: Lost Mauswheel",
    LocationIDs.ch2_lost_werewerewire: "CH2: Lost Werewerewire",
    LocationIDs.ch3_couch_cliffs_dust_pile_chest: "CH3: Couch Cliffs - Dust Pile Chest",
    LocationIDs.ch3_board_1_c_rank: "CH3: Board 1 - C-Rank",
    LocationIDs.ch3_board_1_b_rank: "CH3: Board 1 - B-Rank",
    LocationIDs.ch3_board_1_a_rank: "CH3: Board 1 - A-Rank",
    LocationIDs.ch3_board_1_s_rank: "CH3: Board 1 - S-Rank",
    LocationIDs.ch3_board_1_t_rank: "CH3: Board 1 - T-Rank",
    LocationIDs.ch3_board_1_z_rank: "CH3: Board 1 - Z-Rank",
    LocationIDs.ch3_board_1_extra_key: "CH3: Board 1 - Extra Key",
    LocationIDs.ch3_board_1_extra_extra_key: "CH3: Board 1 - Extra Extra Key",
    LocationIDs.ch3_green_room_vending_machine_1: "CH3: Green Room - Vending Machine 1",
    LocationIDs.ch3_green_room_vending_machine_2: "CH3: Green Room - Vending Machine 2",
    LocationIDs.ch3_green_room_vending_machine_3: "CH3: Green Room - Vending Machine 3",
    LocationIDs.ch3_green_room_vending_machine_4: "CH3: Green Room - Vending Machine 4",
    LocationIDs.ch3_green_room_vending_machine_5: "CH3: Green Room - Vending Machine 5",
    LocationIDs.ch3_green_room_vending_machine_6: "CH3: Green Room - Vending Machine 6",
    LocationIDs.ch3_green_room_vending_machine_7: "CH3: Green Room - Vending Machine 7",
    LocationIDs.ch3_green_room_vending_machine_8: "CH3: Green Room - Vending Machine 8",
    LocationIDs.ch3_green_room_board_1_ramb_gift: "CH3: Green Room - Board 1 Ramb Gift",
    LocationIDs.ch3_green_room_board_2_ramb_gift: "CH3: Green Room - Board 2 Ramb Gift",
    LocationIDs.ch3_b_rank_room_golden_prize_1: "CH3: B-Rank Room - Golden Prize 1",
    LocationIDs.ch3_b_rank_room_golden_prize_2: "CH3: B-Rank Room - Golden Prize 2",
    LocationIDs.ch3_b_rank_room_golden_prize_3: "CH3: B-Rank Room - Golden Prize 3",
    LocationIDs.ch3_b_rank_room_golden_prize_4: "CH3: B-Rank Room - Golden Prize 4",
    LocationIDs.ch3_b_rank_room_golden_prize_5: "CH3: B-Rank Room - Golden Prize 5",
    LocationIDs.ch3_s_rank_room_person_behind_curtain: "CH3: S-Rank Room - Person Behind Curtain",
    LocationIDs.ch3_s_rank_room_vending_machine_1: "CH3: S-Rank Room - Vending Machine 1",
    LocationIDs.ch3_s_rank_room_vending_machine_2: "CH3: S-Rank Room - Vending Machine 2",
    LocationIDs.ch3_s_rank_room_vending_machine_3: "CH3: S-Rank Room - Vending Machine 3",
    LocationIDs.ch3_s_rank_room_vending_machine_4: "CH3: S-Rank Room - Vending Machine 4",
    LocationIDs.ch3_s_rank_room_oddcontroller: "CH3: S-Rank Room - OddController",
    LocationIDs.ch3_board_2_c_rank: "CH3: Board 2 - C-Rank",
    LocationIDs.ch3_board_2_b_rank: "CH3: Board 2 - B-Rank",
    LocationIDs.ch3_board_2_a_rank: "CH3: Board 2 - A-Rank",
    LocationIDs.ch3_board_2_s_rank: "CH3: Board 2 - S-Rank",
    LocationIDs.ch3_board_2_t_rank: "CH3: Board 2 - T-Rank",
    LocationIDs.ch3_board_2_z_rank: "CH3: Board 2 - Z-Rank",
    LocationIDs.ch3_board_2_extra_photo: "CH3: Board 2 - Extra Photo",
    LocationIDs.ch3_board_2_moss: "CH3: Board 2 - Moss",
    LocationIDs.ch3_tv_world_chest_near_shadowmen: "CH3: TV World - Chest Near Shadowmen",
    LocationIDs.ch3_tv_world_board_puzzle_1_chest: "CH3: TV World - Board Puzzle 1 Chest",
    LocationIDs.ch3_tv_world_trash_can_1: "CH3: TV World - Trash Can 1",
    LocationIDs.ch3_tv_world_trash_can_2: "CH3: TV World - Trash Can 2",
    LocationIDs.ch3_tv_world_trash_can_3: "CH3: TV World - Trash Can 3",
    LocationIDs.ch3_tv_world_trash_can_4: "CH3: TV World - Trash Can 4",
    LocationIDs.ch3_tv_world_trash_can_5: "CH3: TV World - Trash Can 5",
    LocationIDs.ch3_tv_world_water_cooler_chest: "CH3: TV World - Water Cooler Chest",
    LocationIDs.ch3_tv_world_board_puzzle_2_chest: "CH3: TV World - Board Puzzle 2 Chest",
    LocationIDs.ch3_tv_world_serious_trashy_chest: "CH3: TV World - Serious Trashy Chest",
    LocationIDs.ch3_tv_world_bonus_zone_chest_1: "CH3: TV World - Bonus Zone Chest 1",
    LocationIDs.ch3_tv_world_bonus_zone_chest_2: "CH3: TV World - Bonus Zone Chest 2",
    LocationIDs.ch3_tv_world_bonus_zone_chest_3: "CH3: TV World - Bonus Zone Chest 3",
    LocationIDs.ch3_tv_world_chest_outside_green_room: "CH3: TV World - Chest Outside Green Room",
    LocationIDs.ch3_tv_world_tripticket: "CH3: TV World - TripTicket",
    LocationIDs.ch3_tv_world_man: "CH3: TV World - Man",
    LocationIDs.ch3_recruit_elnina: "CH3: Recruit Elnina",
    LocationIDs.ch3_recruit_lanino: "CH3: Recruit Lanino",
    LocationIDs.ch3_recruit_shadowguy: "CH3: Recruit Shadowguy",
    LocationIDs.ch3_recruit_shuttah: "CH3: Recruit Shuttah",
    LocationIDs.ch3_recruit_zapper: "CH3: Recruit Zapper",
    LocationIDs.ch3_recruit_ribbick: "CH3: Recruit Ribbick",
    LocationIDs.ch3_recruit_pippins: "CH3: Recruit Pippins",
    LocationIDs.ch3_recruit_water_cooler: "CH3: Recruit Water Cooler",
    LocationIDs.ch3_lost_shadowguy: "CH3: Lost Shadowguy",
    LocationIDs.ch3_lost_shuttah: "CH3: Lost Shuttah",
    LocationIDs.ch3_lost_zapper: "CH3: Lost Zapper",
    LocationIDs.ch3_lost_ribbick: "CH3: Lost Ribbick",
    LocationIDs.ch3_lost_pippins: "CH3: Lost Pippins",
    LocationIDs.ch3_lost_water_cooler: "CH3: Lost Water Cooler",
    LocationIDs.ch3_mantle_out_of_bounds_chest: "CH3: MANTLE - Out of Bounds Chest",
    LocationIDs.ch3_mantle_northern_light_item: "CH3: MANTLE - Northern Light Item",
    LocationIDs.ch3_mantle_defeat: "CH3: MANTLE - Defeat",
    LocationIDs.ch3_mantle_susie_gift: "CH3: MANTLE - Susie's Gift",
    LocationIDs.ch3_cold_place_knight_defeat_item_1: "CH3: Cold Place - Knight Defeat Item #1",
    LocationIDs.ch3_cold_place_knight_defeat_item_2: "CH3: Cold Place - Knight Defeat Item #2",
    LocationIDs.ch3_couch_cliffs_warp_door: "CH3: Couch Cliffs - Warp Door",
    LocationIDs.ch3_green_room_warp_door: "CH3: Green Room - Warp Door",
    LocationIDs.ch3_tv_world_entrance_warp_door: "CH3: TV World - Entrance Warp Door",
    LocationIDs.ch3_tv_world_goulden_sam_warp_door: "CH3: TV World - Goulden Sam Warp Door",
    LocationIDs.ch3_fountain_sealed: "CH3: TV World - Fountain Sealed",
    LocationIDs.ch4_castle_town_lanino_elnina_challenge: "CH4: Castle Town - Lanino&Elnina Challenge",
    LocationIDs.ch4_castle_town_top_chef_gift: "CH4: Castle Town - Top Chef Gift",
    LocationIDs.ch4_dark_sanctuary_jockington_prophecy_chest: "CH4: Dark Sanctuary - Jockington Prophecy Chest",
    LocationIDs.ch4_dark_sanctuary_chest_in_first_dark_area: "CH4: Dark Sanctuary - Chest in First Dark Area",
    LocationIDs.ch4_dark_sanctuary_worship_room_chest: "CH4: Dark Sanctuary - Worship Room Chest",
    LocationIDs.ch4_dark_sanctuary_library_chest_1: "CH4: Dark Sanctuary - Library Chest 1",
    LocationIDs.ch4_dark_sanctuary_lantern_puzzle_chest: "CH4: Dark Sanctuary - Lantern Puzzle Chest",
    LocationIDs.ch4_dark_sanctuary_library_chest_2: "CH4: Dark Sanctuary - Library Chest 2",
    LocationIDs.ch4_dark_sanctuary_jackenstein_gift: "CH4: Dark Sanctuary - Jackenstein Gift",
    LocationIDs.ch4_dark_sanctuary_climbing_tutorial_chest: "CH4: Dark Sanctuary - Climbing Tutorial Chest",
    LocationIDs.ch4_dark_sanctuary_cuptain_pillar_chest: "CH4: Dark Sanctuary - Cuptain Pillar Chest",
    LocationIDs.ch4_dark_sanctuary_sleeping_mizzle_chest: "CH4: Dark Sanctuary - Sleeping Mizzle Chest",
    LocationIDs.ch4_dark_sanctuary_hidden_climbing_chest: "CH4: Dark Sanctuary - Hidden Climbing Chest",
    LocationIDs.ch4_dark_sanctuary_sheetmusic: "CH4: Dark Sanctuary - SheetMusic",
    LocationIDs.ch4_dark_sanctuary_hammer_of_justice_defeat_item_1: "CH4: Dark Sanctuary - Hammer of Justice Defeat Item #1",
    LocationIDs.ch4_dark_sanctuary_hammer_of_justice_defeat_item_2: "CH4: Dark Sanctuary - Hammer of Justice Defeat Item #2",
    LocationIDs.ch4_dark_sanctuary_fountain_sealed: "CH4: Dark Sanctuary - Fountain Sealed",
    LocationIDs.ch4_second_sanctuary_wall_climbing_chest: "CH4: Second Sanctuary - Wall Climbing Chest",
    LocationIDs.ch4_second_sanctuary_waterfall_chest: "CH4: Second Sanctuary - Waterfall Chest",
    LocationIDs.ch4_second_sanctuary_destroyed_piano_block_chest: "CH4: Second Sanctuary - Destroyed Piano Block Chest",
    LocationIDs.ch4_second_sanctuary_man: "CH4: Second Sanctuary - Man",
    LocationIDs.ch4_second_sanctuary_gallery_prophecy_chest: "CH4: Second Sanctuary - Gallery Prophecy Chest",
    LocationIDs.ch4_second_sanctuary_moss: "CH4: Second Sanctuary - Moss",
    LocationIDs.ch4_second_sanctuary_fountain_sealed: "CH4: Second Sanctuary - Fountain Sealed",
    LocationIDs.ch4_third_sanctuary_annoying_dog: "CH4: Third Sanctuary - Annoying Dog...?",
    LocationIDs.ch4_third_sanctuary_speed_climbing_chest: "CH4: Third Sanctuary - Speed Climbing Chest",
    LocationIDs.ch4_third_sanctuary_dark_area_chest: "CH4: Third Sanctuary - Dark Area Chest",
    LocationIDs.ch4_third_sanctuary_titan_defeat: "CH4: Third Sanctuary - Titan Defeat",
    LocationIDs.ch4_third_sanctuary_fountain_sealed: "CH4: Third Sanctuary - Fountain Sealed",
    LocationIDs.ch4_old_man_shop_1: "CH4: Old Man's Shop 1",
    LocationIDs.ch4_old_man_shop_2: "CH4: Old Man's Shop 2",
    LocationIDs.ch4_old_man_shop_3: "CH4: Old Man's Shop 3",
    LocationIDs.ch4_old_man_shop_4: "CH4: Old Man's Shop 4",
    LocationIDs.ch4_recruit_guei: "CH4: Recruit Guei",
    LocationIDs.ch4_recruit_balthizard: "CH4: Recruit Balthizard",
    LocationIDs.ch4_recruit_bibliox: "CH4: Recruit Bibliox",
    LocationIDs.ch4_recruit_mizzle: "CH4: Recruit Mizzle",
    LocationIDs.ch4_recruit_miss_mizzle: "CH4: Recruit Miss Mizzle",
    LocationIDs.ch4_recruit_wicabel: "CH4: Recruit Wicabel",
    LocationIDs.ch4_recruit_winglade: "CH4: Recruit Winglade",
    LocationIDs.ch4_recruit_organikk: "CH4: Recruit Organikk",
    LocationIDs.ch4_lost_guei: "CH4: Lost Guei",
    LocationIDs.ch4_lost_balthizard: "CH4: Lost Balthizard",
    LocationIDs.ch4_lost_bibliox: "CH4: Lost Bibliox",
    LocationIDs.ch4_lost_mizzle: "CH4: Lost Mizzle",
    LocationIDs.ch4_lost_miss_mizzle: "CH4: Lost Miss Mizzle",
    LocationIDs.ch4_lost_wicabel: "CH4: Lost Wicabel",
    LocationIDs.ch4_lost_winglade: "CH4: Lost Winglade",
    LocationIDs.ch4_lost_organikk: "CH4: Lost Organikk",
    LocationIDs.ch4_castle_town_mike_defeat: "CH4: Mike - Defeat Mike",
    LocationIDs.ch4_mike_battat_bronze: "CH4: Mike - Battat (Bronze Rank)",
    LocationIDs.ch4_mike_battat_silver: "CH4: Mike - Battat (Silver Rank)",
    LocationIDs.ch4_mike_battat_gold: "CH4: Mike - Battat (Gold Rank)",
    LocationIDs.ch4_mike_battat_platinum: "CH4: Mike - Battat (Platinum Rank)",
    LocationIDs.ch4_mike_jongler_bronze: "CH4: Mike - Jongler (Bronze Rank)",
    LocationIDs.ch4_mike_jongler_silver: "CH4: Mike - Jongler (Silver Rank)",
    LocationIDs.ch4_mike_jongler_gold: "CH4: Mike - Jongler (Gold Rank)",
    LocationIDs.ch4_mike_jongler_platinum: "CH4: Mike - Jongler (Platinum Rank)",
    LocationIDs.ch4_mike_pluey_bronze: "CH4: Mike - Pluey (Bronze Rank)",
    LocationIDs.ch4_mike_pluey_silver: "CH4: Mike - Pluey (Silver Rank)",
    LocationIDs.ch4_mike_pluey_gold: "CH4: Mike - Pluey (Gold Rank)",
    LocationIDs.ch4_mike_pluey_platinum: "CH4: Mike - Pluey (Platinum Rank)",
}


class LocationData(NamedTuple):
    id: LocationIDs
    group: Optional[LocationGroups]
    should_be_included: Callable[["DeltaruneWorld"], bool] = lambda world: True
    progress_type: LocationProgressType = LocationProgressType.DEFAULT


def get_location_groups(locations_data: list[LocationData]):
    groups: dict[str : set[str]] = {}

    for location_data in locations_data:
        groups.setdefault(location_data.group.value, set()).add(locations[LocationIDs(location_data.id)])

    return groups
