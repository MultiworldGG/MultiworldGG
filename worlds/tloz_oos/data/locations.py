from enum import StrEnum
from typing import Any

from .constants import (
    COLLECT_CHEST,
    COLLECT_D4_SCRUB_ROOM,
    COLLECT_D5_ARMOS_PUZZLE,
    COLLECT_DIG,
    COLLECT_DIVE,
    COLLECT_DIVER_ROOM,
    COLLECT_DROP,
    COLLECT_MAKU_TREE,
    COLLECT_POE_SKIP_ROOM,
    COLLECT_POOF,
    COLLECT_TOUCH,
)


class LocationName(StrEnum):
    north_horon_chest_across_bridge = "North Horon: Chest Across Bridge"
    horon_village_maku_tree_gift = "Horon Village: Maku Tree Gift"
    horon_village_chest_behind_mushrooms = "Horon Village: Chest Behind Mushrooms"
    horon_village_chest_in_dr_lefts_backyard = "Horon Village: Chest in Dr. Left's Backyard"
    woods_of_winter_hollys_gift = "Woods of Winter: Holly's Gift"
    woods_of_winter_chest_on_d2_roof = "Woods of Winter: Chest on D2 Roof"
    holodrum_plain_blainos_gym_prize = "Holodrum Plain: Blaino's Gym Prize"
    holodrum_plain_underwater_item_below_natzu_bridge = "Holodrum Plain: Underwater Item Below Natzu Bridge"
    spool_swamp_digging_spot_near_vasus_sign = "Spool Swamp: Digging Spot Near Vasu's Sign"
    spool_swamp_item_in_floodgate_keepers_house = "Spool Swamp: Item in Floodgate Keeper's House"
    spool_swamp_chest_in_winter_cave = "Spool Swamp: Chest in Winter Cave"
    natzu_region_chest_after_moblin_keep = "Natzu Region: Chest after Moblin Keep"
    sunken_city_master_divers_challenge_chest = "Sunken City: Master Diver's Challenge Chest"
    sunken_city_masters_plaque_trade = "Sunken City: Master's Plaque Trade"
    sunken_city_chest_in_master_divers_cave = "Sunken City: Chest in Master Diver's Cave"
    mt_cucco_spring_banana_tree = "Mt. Cucco: Spring Banana Tree"
    goron_mountain_item_across_pits = "Goron Mountain: Item Across Pits"
    mt_cucco_moving_platform_cave = "Mt. Cucco: Moving Platform Cave"
    mt_cucco_diving_spot_outside_d4 = "Mt. Cucco: Diving Spot Outside D4"
    western_coast_black_beasts_chest = "Western Coast: Black Beast's Chest"
    holodrum_plain_old_man_in_treehouse = "Holodrum Plain: Old Man in Treehouse"
    lost_woods_pedestal_item = "Lost Woods: Pedestal Item"
    samasa_desert_item_in_quicksand_pit = "Samasa Desert: Item in Quicksand Pit"
    samasa_desert_chest_on_cliff = "Samasa Desert: Chest on Cliff"
    western_coast_chest_on_beach = "Western Coast: Chest on Beach"
    western_coast_chest_in_house = "Western Coast: Chest in House"
    holodrum_plain_chest_in_flooded_cave_south_of_mrs_ruul = "Holodrum Plain: Chest in Flooded Cave South of Mrs. Ruul"
    holodrum_plain_chest_in_flooded_cave_behind_mushrooms = "Holodrum Plain: Chest in Flooded Cave Behind Mushrooms"
    woods_of_winter_chest_in_autumn_cave_near_d2 = "Woods of Winter: Chest in Autumn Cave Near D2"
    woods_of_winter_chest_in_cave_behind_rockslide = "Woods of Winter: Chest in Cave Behind Rockslide"
    sunken_city_chest_in_summer_cave = "Sunken City: Chest in Summer Cave"
    sunken_city_syrup_shop_1 = "Sunken City: Syrup Shop #1"
    sunken_city_syrup_shop_2 = "Sunken City: Syrup Shop #2"
    sunken_city_syrup_shop_3 = "Sunken City: Syrup Shop #3"
    eyeglass_lake_chest_in_dried_lake_east_cave = "Eyeglass Lake: Chest in Dried Lake East Cave"
    goron_mountain_chest_across_lava = "Goron Mountain: Chest Across Lava"
    natzu_region_chest_in_northern_cave = "Natzu Region: Chest in Northern Cave"
    mt_cucco_chest_behind_talon = "Mt. Cucco: Chest Behind Talon"
    tarm_ruins_chest_in_rabbit_hole_under_tree = "Tarm Ruins: Chest in Rabbit Hole Under Tree"
    eastern_suburbs_chest_in_spring_cave = "Eastern Suburbs: Chest in Spring Cave"
    eyeglass_lake_chest_in_dried_lake_west_cave = "Eyeglass Lake: Chest in Dried Lake West Cave"
    woods_of_winter_chest_in_waterfall_cave = "Woods of Winter: Chest in Waterfall Cave"
    horon_village_shop_1 = "Horon Village: Shop #1"
    horon_village_shop_2 = "Horon Village: Shop #2"
    horon_village_shop_3 = "Horon Village: Shop #3"
    horon_village_members_shop_1 = "Horon Village: Member's Shop #1"
    horon_village_members_shop_2 = "Horon Village: Member's Shop #2"
    horon_village_members_shop_3 = "Horon Village: Member's Shop #3"
    horon_village_advance_shop_1 = "Horon Village: Advance Shop #1"
    horon_village_advance_shop_2 = "Horon Village: Advance Shop #2"
    horon_village_advance_shop_3 = "Horon Village: Advance Shop #3"
    subrosia_tower_of_winter = "Subrosia: Tower of Winter"
    subrosia_tower_of_summer = "Subrosia: Tower of Summer"
    subrosia_tower_of_spring = "Subrosia: Tower of Spring"
    subrosia_tower_of_autumn = "Subrosia: Tower of Autumn"
    subrosia_dance_hall_reward = "Subrosia: Dance Hall Reward"
    subrosia_temple_of_seasons = "Subrosia: Temple of Seasons"
    subrosia_seaside_digging_spot = "Subrosia: Seaside Digging Spot"
    subrosia_wilds_chest = "Subrosia: Wilds Chest"
    subrosia_wilds_digging_spot = "Subrosia: Wilds Digging Spot"
    subrosia_chest_above_magnet_cave = "Subrosia: Chest Above Magnet Cave"
    subrosia_northwest_open_cave = "Subrosia: Northwest Open Cave"
    subrosia_northwest_locked_cave = "Subrosia: Northwest Locked Cave"
    subrosia_market_1 = "Subrosia: Market #1"
    subrosia_market_2 = "Subrosia: Market #2"
    subrosia_market_3 = "Subrosia: Market #3"
    subrosia_market_4 = "Subrosia: Market #4"
    subrosia_market_5 = "Subrosia: Market #5"
    subrosia_item_smelted_in_great_furnace = "Subrosia: Item Smelted in Great Furnace"
    subrosia_smithy_hard_ore_reforge = "Subrosia: Smithy Hard Ore Reforge"
    subrosia_smithy_rusty_bell_reforge = "Subrosia: Smithy Rusty Bell Reforge"
    heros_cave_topmost_chest = "Hero's Cave: Topmost Chest"
    heros_cave_final_chest = "Hero's Cave: Final Chest"
    heros_cave_item_in_basement_under_keese_room = "Hero's Cave: Item in Basement Under Keese Room"
    heros_cave_alternative_entrance_chest = "Hero's Cave: Alternative Entrance Chest"
    gnarled_root_dungeon_drop_in_right_stalfos_room = "Gnarled Root Dungeon: Drop in Right Stalfos Room"
    gnarled_root_dungeon_item_in_basement = "Gnarled Root Dungeon: Item in Basement"
    gnarled_root_dungeon_chest_in_block_pushing_room = "Gnarled Root Dungeon: Chest in Block-pushing Room"
    gnarled_root_dungeon_chest_near_railway = "Gnarled Root Dungeon: Chest Near Railway"
    gnarled_root_dungeon_chest_in_floormaster_room = "Gnarled Root Dungeon: Chest in Floormaster Room"
    gnarled_root_dungeon_chest_near_railway_lever = "Gnarled Root Dungeon: Chest Near Railway Lever"
    gnarled_root_dungeon_chest_in_left_stalfos_room = "Gnarled Root Dungeon: Chest in Left Stalfos Room"
    gnarled_root_dungeon_hidden_chest_revealed_by_button = "Gnarled Root Dungeon: Hidden Chest Revealed by Button"
    gnarled_root_dungeon_chest_in_goriya_room = "Gnarled Root Dungeon: Chest in Goriya Room"
    gnarled_root_dungeon_boss_reward = "Gnarled Root Dungeon: Boss Reward"
    snakes_remains_drop_in_left_rope_room = "Snake's Remains: Drop in Left Rope Room"
    snakes_remains_chest_in_distant_moblins_room = "Snake's Remains: Chest in Distant Moblins Room"
    snakes_remains_chest_in_rollers_section = "Snake's Remains: Chest in Rollers Section"
    snakes_remains_chest_left_from_entrance = "Snake's Remains: Chest Left from Entrance"
    snakes_remains_chest_behind_pots_in_hardhat_room = "Snake's Remains: Chest Behind Pots in Hardhat Room"
    snakes_remains_chest_in_right_rope_room = "Snake's Remains: Chest in Right Rope Room"
    snakes_remains_chest_in_moving_blades_room = "Snake's Remains: Chest in Moving Blades Room"
    snakes_remains_chest_in_bomb_spiral_maze_room = "Snake's Remains: Chest in Bomb Spiral Maze Room"
    snakes_remains_chest_on_terrace = "Snake's Remains: Chest on Terrace"
    snakes_remains_boss_reward = "Snake's Remains: Boss Reward"
    poison_moths_lair_b1f_chest_in_roller_room = "Poison Moth's Lair (B1F): Chest in Roller Room"
    poison_moths_lair_1f_chest_in_mimics_room = "Poison Moth's Lair (1F): Chest in Mimics Room"
    poison_moths_lair_1f_chest_above_east_trampoline = "Poison Moth's Lair (1F): Chest Above East Trampoline"
    poison_moths_lair_b1f_chest_in_watery_room = "Poison Moth's Lair (B1F): Chest in Watery Room"
    poison_moths_lair_b1f_chest_on_quicksand_terrace = "Poison Moth's Lair (B1F): Chest on Quicksand Terrace"
    poison_moths_lair_1f_chest_in_moldorm_room = "Poison Moth's Lair (1F): Chest in Moldorm Room"
    poison_moths_lair_1f_chest_above_west_trampoline_owl = "Poison Moth's Lair (1F): Chest Above West Trampoline & Owl"
    poison_moths_lair_1f_chest_in_room_behind_hidden_cracked_wall = (
        "Poison Moth's Lair (1F): Chest in Room Behind Hidden Cracked Wall"
    )
    poison_moths_lair_b1f_chest_in_moving_blade_room = "Poison Moth's Lair (B1F): Chest in Moving Blade Room"
    poison_moths_lair_1f_boss_reward = "Poison Moth's Lair (1F): Boss Reward"
    dancing_dragon_dungeon_2f_pots_on_buttons_puzzle_drop = "Dancing Dragon Dungeon (2F): Pots on Buttons Puzzle Drop"
    dancing_dragon_dungeon_2f_chest_north_of_entrance = "Dancing Dragon Dungeon (2F): Chest North of Entrance"
    dancing_dragon_dungeon_1f_chest_in_southwest_quadrant_of_beamos_room = (
        "Dancing Dragon Dungeon (1F): Chest in Southwest Quadrant of Beamos Room"
    )
    dancing_dragon_dungeon_1f_dark_room_chest = "Dancing Dragon Dungeon (1F): Dark Room Chest"
    dancing_dragon_dungeon_2f_chest_in_water_donut_room = "Dancing Dragon Dungeon (2F): Chest in Water Donut Room"
    dancing_dragon_dungeon_2f_pool_drop = "Dancing Dragon Dungeon (2F): Pool Drop"
    dancing_dragon_dungeon_1f_chest_on_small_terrace = "Dancing Dragon Dungeon (1F): Chest on Small Terrace"
    dancing_dragon_dungeon_1f_chest_revealed_by_minecart_torches = (
        "Dancing Dragon Dungeon (1F): Chest Revealed by Minecart Torches"
    )
    dancing_dragon_dungeon_1f_crumbling_room_chest = "Dancing Dragon Dungeon (1F): Crumbling Room Chest"
    dancing_dragon_dungeon_1f_eye_diving_spot_item = "Dancing Dragon Dungeon (1F): Eye Diving Spot Item"
    dancing_dragon_dungeon_b1f_boss_reward = "Dancing Dragon Dungeon (B1F): Boss Reward"
    unicorns_cave_right_cart_chest = "Unicorn's Cave: Right Cart Chest"
    unicorns_cave_chest_left_from_entrance = "Unicorn's Cave: Chest Left from Entrance"
    unicorns_cave_magnet_gloves_chest = "Unicorn's Cave: Magnet Gloves Chest"
    unicorns_cave_terrace_chest = "Unicorn's Cave: Terrace Chest"
    unicorns_cave_armos_puzzle_room_chest = "Unicorn's Cave: Armos Puzzle Room Chest"
    unicorns_cave_gibdo_room_chest = "Unicorn's Cave: Gibdo Room Chest"
    unicorns_cave_quicksand_spiral_chest = "Unicorn's Cave: Quicksand Spiral Chest"
    unicorns_cave_magnet_spinner_chest = "Unicorn's Cave: Magnet Spinner Chest"
    unicorns_cave_chest_in_right_half_of_minecart_bay_room = "Unicorn's Cave: Chest in Right Half of Minecart Bay Room"
    unicorns_cave_treadmills_basement_item = "Unicorn's Cave: Treadmills Basement Item"
    unicorns_cave_boss_reward = "Unicorn's Cave: Boss Reward"
    ancient_ruins_1f_magnet_ball_puzzle_drop = "Ancient Ruins (1F): Magnet Ball Puzzle Drop"
    ancient_ruins_2f_chest_north_of_main_spinner = "Ancient Ruins (2F): Chest North of Main Spinner"
    ancient_ruins_3f_armos_hall_chest = "Ancient Ruins (3F): Armos Hall Chest"
    ancient_ruins_1f_crystal_maze_room_chest = "Ancient Ruins (1F): Crystal Maze Room Chest"
    ancient_ruins_1f_crumbling_ground_room_chest = "Ancient Ruins (1F): Crumbling Ground Room Chest"
    ancient_ruins_2f_chest_in_gibdo_room = "Ancient Ruins (2F): Chest in Gibdo Room"
    ancient_ruins_2f_chest_between_4_armos = "Ancient Ruins (2F): Chest Between 4 Armos"
    ancient_ruins_1f_chest_in_beamos_room = "Ancient Ruins (1F): Chest in Beamos Room"
    ancient_ruins_1f_chest_on_terrace_left_of_entrance = "Ancient Ruins (1F): Chest on Terrace Left of Entrance"
    ancient_ruins_2f_chest_after_time_trial = "Ancient Ruins (2F): Chest After Time Trial"
    ancient_ruins_2f_chest_on_red_terrace_before_vire = "Ancient Ruins (2F): Chest on Red Terrace Before Vire"
    ancient_ruins_5f_boss_reward = "Ancient Ruins (5F): Boss Reward"
    explorers_crypt_1f_chest_in_wizzrobe_room = "Explorer's Crypt (1F): Chest in Wizzrobe Room"
    explorers_crypt_b1f_chest_in_fast_moving_platform_room = (
        "Explorer's Crypt (B1F): Chest in Fast Moving Platform Room"
    )
    explorers_crypt_b2f_stair_maze_chest = "Explorer's Crypt (B2F): Stair Maze Chest"
    explorers_crypt_1f_chest_right_of_entrance = "Explorer's Crypt (1F): Chest Right of Entrance"
    explorers_crypt_1f_chest_behind_cracked_wall = "Explorer's Crypt (1F): Chest Behind Cracked Wall"
    explorers_crypt_b1f_zol_button_drop = "Explorer's Crypt (B1F): Zol Button Drop"
    explorers_crypt_b2f_armos_puzzle_drop = "Explorer's Crypt (B2F): Armos Puzzle Drop"
    explorers_crypt_b1f_chest_connected_to_magnet_ball_button = (
        "Explorer's Crypt (B1F): Chest Connected to Magnet Ball Button"
    )
    explorers_crypt_1f_chest_above_trampoline_near_2nd_poe = (
        "Explorer's Crypt (1F): Chest Above Trampoline Near 2nd Poe"
    )
    explorers_crypt_b2f_drop_in_room_north_of_stair_maze = "Explorer's Crypt (B2F): Drop in Room North of Stair Maze"
    explorers_crypt_b1f_chest_in_jumping_stalfos_room = "Explorer's Crypt (B1F): Chest in Jumping Stalfos Room"
    explorers_crypt_b1f_boss_reward = "Explorer's Crypt (B1F): Boss Reward"
    sword_shield_dungeon_1f_eye_drop_near_entrance = "Sword & Shield Dungeon (1F): Eye Drop Near Entrance"
    sword_shield_dungeon_1f_three_eyes_chest = "Sword & Shield Dungeon (1F): Three Eyes Chest"
    sword_shield_dungeon_1f_drop_in_hardhat_magnet_ball_room = (
        "Sword & Shield Dungeon (1F): Drop in Hardhat & Magnet Ball Room"
    )
    sword_shield_dungeon_1f_u_shaped_spiky_freezer_chest = "Sword & Shield Dungeon (1F): U-Shaped Spiky Freezer Chest"
    sword_shield_dungeon_b1f_chest_right_of_spinner = "Sword & Shield Dungeon (B1F): Chest Right of Spinner"
    sword_shield_dungeon_1f_top_chest_in_lava_bridge_room = "Sword & Shield Dungeon (1F): Top Chest in Lava Bridge Room"
    sword_shield_dungeon_1f_bottom_chest_in_lava_bridge_room = (
        "Sword & Shield Dungeon (1F): Bottom Chest in Lava Bridge Room"
    )
    sword_shield_dungeon_1f_chest_in_bombable_blocks_room = "Sword & Shield Dungeon (1F): Chest in Bombable Blocks Room"
    sword_shield_dungeon_1f_chest_on_terrace_after_pols_voice_room = (
        "Sword & Shield Dungeon (1F): Chest on Terrace After Pols Voice Room"
    )
    sword_shield_dungeon_1f_ghost_armos_puzzle_drop = "Sword & Shield Dungeon (1F): Ghost Armos Puzzle Drop"
    sword_shield_dungeon_b1f_southeast_lava_chest = "Sword & Shield Dungeon (B1F): Southeast Lava Chest"
    sword_shield_dungeon_b1f_southwest_lava_chest = "Sword & Shield Dungeon (B1F): Southwest Lava Chest"
    sword_shield_dungeon_1f_chest_in_sparks_pots_room = "Sword & Shield Dungeon (1F): Chest in Sparks & Pots Room"
    sword_shield_dungeon_b1f_boss_reward = "Sword & Shield Dungeon (B1F): Boss Reward"
    horon_village_item_behind_small_tree = "Horon Village: Item Behind Small Tree"
    woods_of_winter_item_below_lake = "Woods of Winter: Item Below Lake"
    mt_cucco_item_on_ledge = "Mt. Cucco: Item on Ledge"
    eastern_suburbs_item_in_windmill_cave = "Eastern Suburbs: Item in Windmill Cave"
    western_coast_item_in_graveyard = "Western Coast: Item in Graveyard"
    spool_swamp_item_amidst_currents_in_spring = "Spool Swamp: Item Amidst Currents in Spring"
    temple_remains_item_in_cave_behind_rockslide = "Temple Remains: Item in Cave Behind Rockslide"
    horon_village_item_behind_cracked_wall_in_mayors_house = "Horon Village: Item Behind Cracked Wall in Mayor's House"
    subrosia_item_in_house_above_strange_brothers_portal = "Subrosia: Item in House Above Strange Brothers Portal"
    subrosia_item_in_basement_to_tower_of_spring = "Subrosia: Item in Basement to Tower of Spring"
    horon_village_mayors_gift = "Horon Village: Mayor's Gift"
    horon_village_vasus_gift = "Horon Village: Vasu's Gift"
    goron_mountain_lonely_gorons_gift = "Goron Mountain: Lonely Goron's Gift"
    horon_village_dr_left_reward = "Horon Village: Dr. Left Reward"
    north_horon_malon_trade = "North Horon: Malon Trade"
    maple_trade = "Maple Trade"
    holodrum_plain_mrs_ruul_trade = "Holodrum Plain: Mrs. Ruul Trade"
    subrosian_chef_trade = "Subrosia: Subrosian Chef Trade"
    biggoron_trade = "Goron Mountain: Biggoron Trade"
    sunken_city_ingo_trade = "Sunken City: Ingo Trade"
    north_horon_yelling_old_man_trade = "North Horon: Yelling Old Man Trade"
    mt_cucco_talon_trade = "Mt. Cucco: Talon Trade"
    sunken_city_syrup_trade = "Sunken City: Syrup Trade"
    horon_village_tick_tock_trade = "Horon Village: Tick Tock Trade"
    eastern_suburbs_guru_guru_trade = "Eastern Suburbs: Guru-Guru Trade"
    subrosia_buried_bomb_flower = "Subrosia: Buried Bomb Flower"
    subrosia_sign_loving_guy_reward = "Subrosia: Sign-Loving Guy Reward"
    horon_village_old_man = "Horon Village: Old Man"
    north_horon_old_man_near_d1 = "North Horon: Old Man Near D1"
    holodrum_plain_old_man_near_blainos_gym = "Holodrum Plain: Old Man Near Blaino's Gym"
    goron_mountain_old_man = "Goron Mountain: Old Man"
    western_coast_old_man = "Western Coast: Old Man"
    woods_of_winter_old_man = "Woods of Winter: Old Man"
    holodrum_plain_old_man_near_mrs_ruuls_house = "Holodrum Plain: Old Man Near Mrs. Ruul's House"
    tarm_ruins_old_man_near_d6 = "Tarm Ruins: Old Man Near D6"
    north_horon_golden_beasts_old_man = "North Horon: Golden Beasts Old Man"
    horon_village_seed_tree = "Horon Village: Seed Tree"
    woods_of_winter_seed_tree = "Woods of Winter: Seed Tree"
    holodrum_plain_seed_tree = "Holodrum Plain: Seed Tree"
    spool_swamp_seed_tree = "Spool Swamp: Seed Tree"
    sunken_city_seed_tree = "Sunken City: Seed Tree"
    tarm_ruins_seed_tree = "Tarm Ruins: Seed Tree"
    gnarled_root_dungeon_essence = "Gnarled Root Dungeon: Essence"
    snakes_remains_essence = "Snake's Remains: Essence"
    poison_moths_lair_essence = "Poison Moth's Lair: Essence"
    dancing_dragon_dungeon_essence = "Dancing Dragon Dungeon: Essence"
    unicorns_cave_essence = "Unicorn's Cave: Essence"
    ancient_ruins_essence = "Ancient Ruins: Essence"
    explorers_crypt_essence = "Explorer's Crypt: Essence"
    sword_shield_dungeon_essence = "Sword & Shield Dungeon: Essence"
    horon_village_item_inside_maku_tree_3_essences = "Horon Village: Item Inside Maku Tree (3+ Essences)"
    horon_village_item_inside_maku_tree_5_essences = "Horon Village: Item Inside Maku Tree (5+ Essences)"
    horon_village_item_inside_maku_tree_7_essences = "Horon Village: Item Inside Maku Tree (7+ Essences)"
    subrosia_strange_brothers_backyard_treasure = "Subrosia: Strange Brothers' Backyard Treasure"
    subrosia_hot_bath_digging_spot = "Subrosia: Hot Bath Digging Spot"
    subrosia_market_portal_digging_spot = "Subrosia: Market Portal Digging Spot"
    subrosia_hard_working_subrosian_digging_spot = "Subrosia: Hard-Working Subrosian Digging Spot"
    subrosia_temple_of_seasons_digging_spot = "Subrosia: Temple of Seasons Digging Spot"
    subrosia_northern_volcanoes_digging_spot = "Subrosia: Northern Volcanoes Digging Spot"
    subrosia_d8_portal_digging_spot = "Subrosia: D8 Portal Digging Spot"
    subrosia_western_volcanoes_digging_spot = "Subrosia: Western Volcanoes Digging Spot"
    gasha_nut_1 = "Gasha Nut #1"
    gasha_nut_2 = "Gasha Nut #2"
    gasha_nut_3 = "Gasha Nut #3"
    gasha_nut_4 = "Gasha Nut #4"
    gasha_nut_5 = "Gasha Nut #5"
    gasha_nut_6 = "Gasha Nut #6"
    gasha_nut_7 = "Gasha Nut #7"
    gasha_nut_8 = "Gasha Nut #8"
    gasha_nut_9 = "Gasha Nut #9"
    gasha_nut_10 = "Gasha Nut #10"
    gasha_nut_11 = "Gasha Nut #11"
    gasha_nut_12 = "Gasha Nut #12"
    gasha_nut_13 = "Gasha Nut #13"
    gasha_nut_14 = "Gasha Nut #14"
    gasha_nut_15 = "Gasha Nut #15"
    gasha_nut_16 = "Gasha Nut #16"
    spool_swamp_business_scrub = "Spool Swamp: Business Scrub"
    samasa_desert_business_scrub = "Samasa Desert: Business Scrub"
    snakes_remains_business_scrub = "Snake's Remains: Business Scrub"
    dancing_dragon_dungeon_1f_business_scrub = "Dancing Dragon Dungeon (1F): Business Scrub"
    horon_village_clock_shop_secret = "Horon Village: Clock Shop Secret"
    western_coast_graveyard_secret = "Western Coast: Graveyard Secret"
    subrosia_subrosian_secret = "Subrosia: Subrosian Secret"
    sunken_city_diver_secret = "Sunken City: Diver Secret"
    subrosia_smith_secret = "Subrosia: Smith Secret"
    subrosia_piratian_secret = "Subrosia: Piratian Secret"
    subrosia_temple_secret = "Subrosia: Temple Secret"
    natzu_region_deku_secret = "Natzu Region: Deku Secret"
    goron_mountain_biggoron_secret = "Goron Mountain: Biggoron Secret"
    horon_village_mayor_secret = "Horon Village: Mayor Secret"
    dodongo_owl = "Dodongo Owl"
    gohma_owl = "Gohma Owl"
    armos_knights_owl = "Armos Knights Owl"
    silent_watch_owl = "Silent Watch Owl"
    magical_ice_owl = "Magical Ice Owl"
    mystery_owl = "Mystery Owl"
    omuai_owl = "Omuai Owl"
    poe_curse_owl = "Poe Curse Owl"
    spiked_beetles_owl = "Spiked Beetles Owl"
    trampoline_owl = "Trampoline Owl"
    greater_distance_owl = "Greater Distance Owl"
    frypolar_owl = "Frypolar Owl"
    shining_blue_owl = "Shining Blue Owl"
    floodgate_owl = "Floodgate Owl"
    linked_heros_cave_alternate_entrance_chest = "Linked Hero's Cave: Alternate Entrance Chest"
    linked_heros_cave_first_reward = "Linked Hero's Cave: First Reward"
    linked_heros_cave_checkerboard_drop = "Linked Hero's Cave: Checkerboard Drop"
    linked_heros_cave_second_reward = "Linked Hero's Cave: Second Reward"
    linked_heros_cave_torch_chest = "Linked Hero's Cave: Torch Chest"
    linked_heros_cave_flooded_room_drop = "Linked Hero's Cave: Flooded Room Drop"
    linked_heros_cave_third_reward = "Linked Hero's Cave: Third Reward"
    linked_heros_cave_fourth_reward = "Linked Hero's Cave: Fourth Reward"
    linked_heros_cave_gauntlet = "Linked Hero's Cave: Gauntlet"
    linked_heros_cave_boomerang_maze = "Linked Hero's Cave: Boomerang Maze"
    linked_heros_cave_final_reward = "Linked Hero's Cave: Final Reward"
    maple_rare_drop_1 = "Maple Rare Drop #1"
    maple_rare_drop_2 = "Maple Rare Drop #2"
    maple_rare_drop_3 = "Maple Rare Drop #3"
    maple_rare_drop_4 = "Maple Rare Drop #4"


LOCATIONS_DATA: dict[LocationName, dict[str, Any]] = {
    LocationName.north_horon_chest_across_bridge: {
        "region_id": "eyeglass lake, across bridge",
        "vanilla_item": "Gasha Seed",
        "room": 0x00B8,
        "collect": COLLECT_CHEST,
    },
    LocationName.horon_village_maku_tree_gift: {
        "region_id": "maku tree",
        "vanilla_item": "Gnarled Key",
        # Maku Tree has several rooms depending on the amount of essences owned
        "flag_byte": 0xC80B,
        "room": [0x020B, 0x020C, 0x022B, 0x022C, 0x022D, 0x025B, 0x025C, 0x025D, 0x025E, 0x027B],
        "collect": COLLECT_MAKU_TREE,
        "map_tile": 0xC9,
        "symbolic_name": "makuTree",
    },
    LocationName.horon_village_chest_behind_mushrooms: {
        "region_id": "horon village SW chest",
        "vanilla_item": "Rupees (20)",
        "room": 0x00F5,
        "collect": COLLECT_CHEST,
    },
    LocationName.horon_village_chest_in_dr_lefts_backyard: {
        "region_id": "horon village SE chest",
        "vanilla_item": "Rupees (20)",
        "room": 0x00F9,
        "collect": COLLECT_CHEST,
    },
    LocationName.woods_of_winter_hollys_gift: {
        "region_id": "holly's house",
        "vanilla_item": "Shovel",
        "room": 0x03A3,
        "collect": COLLECT_TOUCH,
        "map_tile": 0x7F,
        "symbolic_name": "hollyGift",
    },
    LocationName.woods_of_winter_chest_on_d2_roof: {
        "region_id": "d2 roof",
        "vanilla_item": "Gasha Seed",
        "room": 0x008E,
        "collect": COLLECT_CHEST,
    },
    LocationName.holodrum_plain_blainos_gym_prize: {
        "region_id": "blaino prize",
        "vanilla_item": "Ricky's Gloves",
        "room": 0x03B4,
        "collect": COLLECT_TOUCH,
        "map_tile": 0x78,
        "symbolic_name": "blainoPrize",
    },
    LocationName.holodrum_plain_underwater_item_below_natzu_bridge: {
        "region_id": "underwater item below natzu bridge",
        "vanilla_item": "Gasha Seed",
        "conditional": True,
        "room": 0x0066,
        "collect": COLLECT_DIVE,
        "symbolic_name": "underwaterItemBelowNatzuBridge",
    },
    LocationName.spool_swamp_digging_spot_near_vasus_sign: {
        "region_id": "spool swamp digging spot",
        "vanilla_item": "Armor Ring L-1",  # Random ring in vanilla, but rings are randomized anyway
        "room": 0x0082,
        "collect": COLLECT_DIG,
        "symbolic_name": "spoolSwampDiggingSpot",
    },
    LocationName.spool_swamp_item_in_floodgate_keepers_house: {
        "region_id": "floodgate keeper's house",
        "vanilla_item": "Floodgate Key",
        "room": 0x03B5,
        "collect": COLLECT_TOUCH,
        "map_tile": 0x62,
        "symbolic_name": "floodgateKeeperHouse",
    },
    LocationName.spool_swamp_chest_in_winter_cave: {
        "region_id": "spool swamp cave",
        "vanilla_item": "Square Jewel",
        "room": 0x04FA,
        "collect": COLLECT_CHEST,
        "map_tile": 0xC2,
    },
    LocationName.natzu_region_chest_after_moblin_keep: {
        "region_id": "moblin keep chest",
        "vanilla_item": "Piece of Heart",
        "room": 0x005B,
        "collect": COLLECT_CHEST,
    },
    LocationName.sunken_city_master_divers_challenge_chest: {
        "region_id": "master diver's challenge",
        "vanilla_item": "Master's Plaque",
        "room": 0x05BC,
        "collect": COLLECT_CHEST,
        "map_tile": 0x2E,
    },
    LocationName.sunken_city_masters_plaque_trade: {
        "region_id": "master diver's reward",
        "vanilla_item": "Flippers",
        "bit_mask": 0x80,
        "room": 0x05BD,
        "collect": COLLECT_DIVER_ROOM,
        "map_tile": 0x2E,
        "symbolic_name": "masterPlaqueTrade",
    },
    LocationName.sunken_city_chest_in_master_divers_cave: {
        "region_id": "chest in master diver's cave",
        "vanilla_item": "Rupees (50)",
        "room": 0x05BD,
        "collect": COLLECT_DIVER_ROOM,
        "is_chest": True,
        "map_tile": 0x2E,
    },
    LocationName.mt_cucco_spring_banana_tree: {
        "region_id": "spring banana tree",
        "vanilla_item": "Spring Banana",
        "room": 0x000F,
        "collect": COLLECT_TOUCH,
        "symbolic_name": "springBananaTree",
    },
    LocationName.goron_mountain_item_across_pits: {
        "region_id": "goron mountain, across pits",
        "vanilla_item": "Dragon Key",
        "room": 0x001A,
        "collect": COLLECT_TOUCH,
        "symbolic_name": "goronMountainPits",
    },
    LocationName.mt_cucco_moving_platform_cave: {
        "region_id": "mt. cucco, platform cave",
        "vanilla_item": "Green Joy Ring",
        "room": 0x05BB,
        "collect": COLLECT_DROP,
        "map_tile": 0x1F,
        "symbolic_name": "mtCuccoPlatformCave",
    },
    LocationName.mt_cucco_diving_spot_outside_d4: {
        "region_id": "diving spot outside D4",
        "vanilla_item": "Pyramid Jewel",
        "room": 0x07E5,
        "collect": COLLECT_TOUCH,
        "map_tile": 0x1D,
        "symbolic_name": "divingSpotOutsideD4",
    },
    LocationName.western_coast_black_beasts_chest: {
        "region_id": "black beast's chest",
        "vanilla_item": "X-Shaped Jewel",
        "room": 0x00F4,
        "collect": COLLECT_CHEST,
    },
    LocationName.holodrum_plain_old_man_in_treehouse: {
        "region_id": "old man in treehouse",
        "vanilla_item": "Round Jewel",
        "room": 0x0394,
        "collect": COLLECT_TOUCH,
        "map_tile": 0xB5,
        "symbolic_name": "oldManInTreehouse",
    },
    LocationName.lost_woods_pedestal_item: {
        "region_id": "lost woods",
        "vanilla_item": "Progressive Sword",
        "room": 0x00C9,
        "collect": COLLECT_TOUCH,
        "map_tile": 0x40,
        "symbolic_name": "lostWoodsPedestal",
    },
    LocationName.samasa_desert_item_in_quicksand_pit: {
        "region_id": "samasa desert pit",
        "vanilla_item": "Rusty Bell",
        "room": 0x05D2,
        "collect": COLLECT_TOUCH,
        "map_tile": 0xBF,
        "symbolic_name": "samasaDesertPit",
    },
    LocationName.samasa_desert_chest_on_cliff: {
        "region_id": "samasa desert chest",
        "vanilla_item": "Rang Ring L-1",
        "room": 0x00FF,
        "collect": COLLECT_CHEST,
    },
    LocationName.western_coast_chest_on_beach: {
        "region_id": "western coast after ship",
        "vanilla_item": "Blast Ring",
        "room": 0x00E3,
        "collect": COLLECT_CHEST,
    },
    LocationName.western_coast_chest_in_house: {
        "region_id": "western coast after ship",
        "vanilla_item": "Bombs (10)",
        "room": 0x0388,
        "collect": COLLECT_CHEST,
        "map_tile": 0xD2,
    },
    LocationName.holodrum_plain_chest_in_flooded_cave_south_of_mrs_ruul: {
        "region_id": "cave south of mrs. ruul",
        "vanilla_item": "Octo Ring",
        "room": 0x04E0,
        "collect": COLLECT_CHEST,
        "map_tile": 0xB3,
    },
    LocationName.holodrum_plain_chest_in_flooded_cave_behind_mushrooms: {
        "region_id": "cave north of D1",
        "vanilla_item": "Quicksand Ring",
        "room": 0x04E1,
        "collect": COLLECT_CHEST,
        "map_tile": 0x87,
    },
    LocationName.woods_of_winter_chest_in_autumn_cave_near_d2: {
        "region_id": "cave outside D2",
        "vanilla_item": "Moblin Ring",
        "room": 0x05B3,
        "collect": COLLECT_CHEST,
        "map_tile": 0x8E,
    },
    LocationName.woods_of_winter_chest_in_cave_behind_rockslide: {
        "region_id": "woods of winter, 1st cave",
        "vanilla_item": "Rupees (30)",
        "room": 0x05B4,
        "collect": COLLECT_CHEST,
        "map_tile": 0x7D,
    },
    LocationName.sunken_city_chest_in_summer_cave: {
        "region_id": "sunken city, summer cave",
        "vanilla_item": "Gasha Seed",
        "room": 0x05B5,
        "collect": COLLECT_CHEST,
        "map_tile": 0x4F,
    },
    LocationName.sunken_city_syrup_shop_1: {
        "region_id": "syrup shop",
        "vanilla_item": "Potion",
        "conditional": True,
        "flag_byte": 0xC63F,
        "bit_mask": 0x80,
        "scouting_byte": 0xC89C,
        "scouting_mask": 0x40,
        "room": 0x039C,
        "collect": COLLECT_TOUCH,
        "map_tile": 0x5E,
        "symbolic_name": "syrupShop1",
        "shop": True,
        "repeatable": True,
    },
    LocationName.sunken_city_syrup_shop_2: {
        "region_id": "syrup shop",
        "vanilla_item": "Gasha Seed",
        "conditional": True,
        "flag_byte": 0xC63F,
        "bit_mask": 0x20,
        "scouting_byte": 0xC89C,
        "scouting_mask": 0x40,
        "room": 0x039C,
        "collect": COLLECT_TOUCH,
        "map_tile": 0x5E,
        "symbolic_name": "syrupShop2",
        "shop": True,
        "repeatable": True,
    },
    LocationName.sunken_city_syrup_shop_3: {
        "region_id": "syrup shop",
        "vanilla_item": "Bombchus (10)",
        "conditional": True,
        "flag_byte": 0xC63F,
        "bit_mask": 0x40,
        "scouting_byte": 0xC89C,
        "scouting_mask": 0x40,
        "room": 0x039C,
        "collect": COLLECT_TOUCH,
        "map_tile": 0x5E,
        "symbolic_name": "syrupShop3",
        "shop": True,
        "repeatable": True,
    },
    LocationName.eyeglass_lake_chest_in_dried_lake_east_cave: {
        "region_id": "dry eyeglass lake, east cave",
        "vanilla_item": "Piece of Heart",
        "room": 0x05C0,
        "collect": COLLECT_CHEST,
        "map_tile": 0xAA,
    },
    LocationName.goron_mountain_chest_across_lava: {
        "region_id": "chest in goron mountain",
        "vanilla_item": "Armor Ring L-2",
        "room": 0x05C8,
        "collect": COLLECT_CHEST,
        "map_tile": 0x18,
    },
    LocationName.natzu_region_chest_in_northern_cave: {
        "region_id": "natzu region, across water",
        "vanilla_item": "Rupees (50)",
        "room": 0x050E,
        "collect": COLLECT_CHEST,
        "map_tile": 0x49,
    },
    LocationName.mt_cucco_chest_behind_talon: {
        "region_id": "talon trade",
        "vanilla_item": "Subrosian Ring",
        "conditional": True,
        "bit_mask": 0x60,  # 0x60 is needed here to ensure we're not sending Talon's wakeup item as a false positive
        "room": 0x05B6,
        "collect": COLLECT_CHEST,
        "map_tile": 0x1B,
    },
    LocationName.tarm_ruins_chest_in_rabbit_hole_under_tree: {
        "region_id": "tarm ruins, under tree",
        "vanilla_item": "Gasha Seed",
        "room": 0x039B,
        "collect": COLLECT_CHEST,
        "map_tile": 0x10,
    },
    LocationName.eastern_suburbs_chest_in_spring_cave: {
        "region_id": "eastern suburbs spring cave",
        "vanilla_item": "Gasha Seed",
        "room": 0x04F7,
        "collect": COLLECT_CHEST,
        "map_tile": 0xCC,
    },
    LocationName.eyeglass_lake_chest_in_dried_lake_west_cave: {
        "region_id": "dry eyeglass lake, west cave",
        "vanilla_item": "Rupees (100)",
        "room": 0x04FB,
        "collect": COLLECT_CHEST,
        "map_tile": 0xA7,
    },
    LocationName.woods_of_winter_chest_in_waterfall_cave: {
        "region_id": "woods of winter, 2nd cave",
        "vanilla_item": "Gasha Seed",
        "room": 0x0512,
        "collect": COLLECT_CHEST,
        "map_tile": 0x7E,
    },
    LocationName.horon_village_shop_1: {
        "region_id": "horon shop",
        "vanilla_item": "Bombs (10)",
        "flag_byte": 0xC640,
        "bit_mask": 0x20,
        "scouting_byte": 0xC8A6,
        "room": 0x03A6,
        "collect": COLLECT_TOUCH,
        "map_tile": 0xE6,
        "symbolic_name": "horonShop1",
        "shop": True,
        "repeatable": True,
    },
    LocationName.horon_village_shop_2: {
        "region_id": "horon shop",
        "vanilla_item": "Progressive Shield",
        "flag_byte": 0xC640,
        "bit_mask": 0x40,
        "scouting_byte": 0xC8A6,
        "room": 0x03A6,
        "collect": COLLECT_TOUCH,
        "map_tile": 0xE6,
        "symbolic_name": "horonShop2",
        "shop": True,
        "repeatable": True,
    },
    LocationName.horon_village_shop_3: {
        "region_id": "horon shop",
        "vanilla_item": "Flute",
        "flag_byte": 0xC640,
        "bit_mask": 0x80,
        "scouting_byte": 0xC8A6,
        "room": 0x03A6,
        "collect": COLLECT_TOUCH,
        "map_tile": 0xE6,
        "symbolic_name": "horonShop3",
        "shop": True,
        "repeatable": True,
    },
    LocationName.horon_village_members_shop_1: {
        "region_id": "member's shop",
        "vanilla_item": "Seed Satchel",
        "flag_byte": 0xC63F,
        "bit_mask": 0x01,
        "scouting_byte": 0xC8B0,
        "room": 0x03B0,
        "collect": COLLECT_TOUCH,
        "map_tile": 0xE6,
        "symbolic_name": "memberShop1",
        "shop": True,
        "repeatable": True,
    },
    LocationName.horon_village_members_shop_2: {
        "region_id": "member's shop",
        "vanilla_item": "Gasha Seed",
        "flag_byte": 0xC63F,
        "bit_mask": 0x02,
        "scouting_byte": 0xC8B0,
        "room": 0x03B0,
        "collect": COLLECT_TOUCH,
        "map_tile": 0xE6,
        "symbolic_name": "memberShop2",
        "shop": True,
        "repeatable": True,
    },
    LocationName.horon_village_members_shop_3: {
        "region_id": "member's shop",
        "vanilla_item": "Seed Satchel",
        # Add a 3rd satchel that is usually obtained in linked games (99 seeds)
        # while removing the treasure map which is not implemented yet
        "flag_byte": 0xC63F,
        "bit_mask": 0x08,
        "scouting_byte": 0xC8B0,
        "room": 0x03B0,
        "collect": COLLECT_TOUCH,
        "map_tile": 0xE6,
        "symbolic_name": "memberShop3",
        "shop": True,
        "repeatable": True,
    },
    LocationName.horon_village_advance_shop_1: {
        "region_id": "advance shop",
        "vanilla_item": "Gasha Seed",
        "flag_byte": 0xC640,
        "bit_mask": 0x01,
        "conditional": True,
        "scouting_byte": 0xC8AF,
        "room": 0x03AF,
        "collect": COLLECT_TOUCH,
        "map_tile": 0xC5,
        "symbolic_name": "advanceShop1",
        "shop": True,
        "repeatable": True,
    },
    LocationName.horon_village_advance_shop_2: {
        "region_id": "advance shop",
        "vanilla_item": "GBA Nature Ring",
        "flag_byte": 0xC640,
        "bit_mask": 0x02,
        "conditional": True,
        "scouting_byte": 0xC8AF,
        "room": 0x03AF,
        "collect": COLLECT_TOUCH,
        "map_tile": 0xC5,
        "symbolic_name": "advanceShop2",
        "shop": True,
        "repeatable": True,
    },
    LocationName.horon_village_advance_shop_3: {
        "region_id": "advance shop",
        "vanilla_item": "Random Ring",
        "flag_byte": 0xC640,
        "bit_mask": 0x04,
        "conditional": True,
        "scouting_byte": 0xC8AF,
        "room": 0x03AF,
        "collect": COLLECT_TOUCH,
        "map_tile": 0xC5,
        "symbolic_name": "advanceShop3",
        "shop": True,
        "repeatable": True,
    },
    LocationName.subrosia_tower_of_winter: {
        "region_id": "tower of winter",
        "vanilla_item": "Rod of Seasons (Winter)",
        "room": 0x05F2,
        "collect": COLLECT_TOUCH,
        "map_tile": 0xB0,
        "symbolic_name": "towerOfWinter",
    },
    LocationName.subrosia_tower_of_summer: {
        "region_id": "tower of summer",
        "vanilla_item": "Rod of Seasons (Summer)",
        "room": 0x05F8,
        "collect": COLLECT_TOUCH,
        "map_tile": 0xB0,
        "symbolic_name": "towerOfSummer",
    },
    LocationName.subrosia_tower_of_spring: {
        "region_id": "tower of spring",
        "vanilla_item": "Rod of Seasons (Spring)",
        "room": 0x05F5,
        "collect": COLLECT_TOUCH,
        "map_tile": 0x1E,
        "symbolic_name": "towerOfSpring",
    },
    LocationName.subrosia_tower_of_autumn: {
        "region_id": "tower of autumn",
        "vanilla_item": "Rod of Seasons (Autumn)",
        "room": 0x05FB,
        "collect": COLLECT_TOUCH,
        "map_tile": 0xB0,
        "symbolic_name": "towerOfAutumn",
    },
    LocationName.subrosia_dance_hall_reward: {
        "region_id": "subrosian dance hall",
        "vanilla_item": "Progressive Boomerang",
        "room": 0x0395,
        "collect": COLLECT_TOUCH,
        "map_tile": 0x9A,
        "symbolic_name": "subrosianDanceHall",
    },
    LocationName.subrosia_temple_of_seasons: {
        "region_id": "temple of seasons",
        "vanilla_item": "Fool's Ore",  # Originally Rod of Seasons which is not used in the rando
        "room": 0x03AC,
        "collect": COLLECT_TOUCH,
        "map_tile": 0xB0,
        "symbolic_name": "templeOfSeasons",
    },
    LocationName.subrosia_seaside_digging_spot: {
        "region_id": "subrosia seaside",
        "vanilla_item": "Star Ore",
        "flag_byte": 0xC866,
        "room": [0x0165, 0x0166, 0x0175, 0x0176],
        "collect": COLLECT_DIG,
        "map_tile": 0xB0,
        "symbolic_name": "subrosiaSeaside",
    },
    LocationName.subrosia_wilds_chest: {
        "region_id": "subrosian wilds chest",
        "vanilla_item": "Blue Ore",
        "room": 0x0141,
        "collect": COLLECT_CHEST,
        "map_tile": 0x1E,
    },
    LocationName.subrosia_wilds_digging_spot: {
        "region_id": "subrosian wilds digging spot",
        "vanilla_item": "Power Ring L-2",  # Random ring in vanilla, but this doesn't exist in rando
        "room": 0x0140,
        "collect": COLLECT_DIG,
        "map_tile": 0x1E,
        "symbolic_name": "subrosianWildsDiggingSpot",
    },
    LocationName.subrosia_chest_above_magnet_cave: {
        "region_id": "subrosia village chest",
        "vanilla_item": "Red Ore",
        "room": 0x0158,
        "collect": COLLECT_CHEST,
        "map_tile": 0xB0,
    },
    LocationName.subrosia_northwest_open_cave: {
        "region_id": "subrosia, open cave",
        "vanilla_item": "Gasha Seed",
        "room": 0x04F1,
        "collect": COLLECT_CHEST,
        "map_tile": 0x25,
    },
    LocationName.subrosia_northwest_locked_cave: {
        "region_id": "subrosia, locked cave",
        "vanilla_item": "Gasha Seed",
        "room": 0x05C6,
        "collect": COLLECT_CHEST,
        "map_tile": 0x25,
    },
    LocationName.subrosia_market_1: {
        "region_id": "subrosia market star ore",
        "vanilla_item": "Ribbon",
        "flag_byte": 0xC642,
        "bit_mask": 0x01,
        "scouting_byte": 0xC8A0,
        "room": 0x03A0,
        "collect": COLLECT_TOUCH,
        "map_tile": 0xB0,
        "symbolic_name": "subrosianMarket1",
    },
    LocationName.subrosia_market_2: {
        "region_id": "subrosia market ore chunks",
        "vanilla_item": "Rare Peach Stone",
        "flag_byte": 0xC642,
        "bit_mask": 0x02,
        "scouting_byte": 0xC8A0,
        "room": 0x03A0,
        "collect": COLLECT_TOUCH,
        "map_tile": 0xB0,
        "symbolic_name": "subrosianMarket2",
    },
    LocationName.subrosia_market_3: {
        "region_id": "subrosia market ore chunks",
        "vanilla_item": "Progressive Shield",
        "flag_byte": 0xC642,
        "bit_mask": 0x04,
        "scouting_byte": 0xC8A0,
        "room": 0x03A0,
        "collect": COLLECT_TOUCH,
        "map_tile": 0xB0,
        "symbolic_name": "subrosianMarket3",
    },
    LocationName.subrosia_market_4: {
        "region_id": "subrosia market ore chunks",
        "vanilla_item": "Bombs (10)",
        "flag_byte": 0xC642,
        "bit_mask": 0x08,
        "scouting_byte": 0xC8A0,
        "room": 0x03A0,
        "collect": COLLECT_TOUCH,
        "map_tile": 0xB0,
        "symbolic_name": "subrosianMarket4",
    },
    LocationName.subrosia_market_5: {
        "region_id": "subrosia market ore chunks",
        "vanilla_item": "Member's Card",
        "flag_byte": 0xC642,
        "bit_mask": 0x10,
        "scouting_byte": 0xC8A0,
        "room": 0x03A0,
        "collect": COLLECT_TOUCH,
        "map_tile": 0xB0,
        "symbolic_name": "subrosianMarket5",
    },
    LocationName.subrosia_item_smelted_in_great_furnace: {
        "region_id": "great furnace",
        "vanilla_item": "Hard Ore",
        "room": 0x038E,
        "collect": COLLECT_TOUCH,
        "map_tile": 0xB9,
        "symbolic_name": "greatFurnace",
    },
    LocationName.subrosia_smithy_hard_ore_reforge: {
        "region_id": "subrosian smithy ore",
        "vanilla_item": "Progressive Shield",
        "bit_mask": 0x40,
        "room": 0x0397,
        "collect": COLLECT_TOUCH,
        "map_tile": 0x1E,
        "symbolic_name": "subrosianSmithyOre",
    },
    LocationName.subrosia_smithy_rusty_bell_reforge: {
        "region_id": "subrosian smithy bell",
        "vanilla_item": "Pirate's Bell",
        "bit_mask": 0x80,
        "room": 0x0397,
        "collect": COLLECT_TOUCH,
        "map_tile": 0x1E,
        "symbolic_name": "subrosianSmithyBell",
    },
    LocationName.heros_cave_topmost_chest: {
        "region_id": "d0 key chest",
        "vanilla_item": "Small Key (Hero's Cave)",
        "dungeon": 0,
        "room": 0x0403,
        "collect": COLLECT_CHEST,
        "map_tile": 0xD4,
    },
    LocationName.heros_cave_final_chest: {
        "region_id": "d0 sword chest",
        "vanilla_item": "Progressive Sword",
        "dungeon": 0,
        "room": 0x0406,
        # Not a real chest, so we don't apply the usual COLLECT_CHEST
        "map_tile": 0xD4,
        "symbolic_name": "d0SwordChest",
    },
    LocationName.heros_cave_item_in_basement_under_keese_room: {
        "region_id": "d0 hidden 2d section",
        "vanilla_item": "Gasha Seed",
        "dungeon": 0,
        "room": 0x0601,
        "collect": COLLECT_TOUCH,
        "map_tile": 0xD4,
        "symbolic_name": "d0HiddenBasement",
    },
    LocationName.heros_cave_alternative_entrance_chest: {
        "region_id": "d0 rupee chest",
        "vanilla_item": "Rupees (30)",
        "dungeon": 0,
        "room": 0x0405,
        "collect": COLLECT_CHEST,
        "map_tile": 0xD4,
    },
    LocationName.gnarled_root_dungeon_drop_in_right_stalfos_room: {
        "region_id": "d1 stalfos drop",
        "vanilla_item": "Small Key (Gnarled Root Dungeon)",
        "dungeon": 1,
        "room": 0x041B,
        "collect": COLLECT_DROP,
        "map_tile": 0x96,
        "symbolic_name": "d1StalfosDrop",
    },
    LocationName.gnarled_root_dungeon_item_in_basement: {
        "region_id": "d1 basement",
        "vanilla_item": "Seed Satchel",
        "dungeon": 1,
        "room": 0x0609,
        "collect": COLLECT_TOUCH,
        "map_tile": 0x96,
        "symbolic_name": "d1Basement",
    },
    LocationName.gnarled_root_dungeon_chest_in_block_pushing_room: {
        "region_id": "d1 block-pushing room",
        "vanilla_item": "Gasha Seed",
        "dungeon": 1,
        "room": 0x040D,
        "collect": COLLECT_CHEST,
        "map_tile": 0x96,
    },
    LocationName.gnarled_root_dungeon_chest_near_railway: {
        "region_id": "d1 railway chest",
        "vanilla_item": "Bombs (10)",
        "dungeon": 1,
        "room": 0x0410,
        "collect": COLLECT_CHEST,
        "map_tile": 0x96,
    },
    LocationName.gnarled_root_dungeon_chest_in_floormaster_room: {
        "region_id": "d1 floormaster room",
        "vanilla_item": "Discovery Ring",
        "dungeon": 1,
        "room": 0x0417,
        "collect": COLLECT_CHEST,
        "map_tile": 0x96,
    },
    LocationName.gnarled_root_dungeon_chest_near_railway_lever: {
        "region_id": "d1 lever room",
        "vanilla_item": "Compass (Gnarled Root Dungeon)",
        "dungeon": 1,
        "room": 0x040F,
        "collect": COLLECT_CHEST,
        "map_tile": 0x96,
    },
    LocationName.gnarled_root_dungeon_chest_in_left_stalfos_room: {
        "region_id": "d1 stalfos chest",
        "vanilla_item": "Dungeon Map (Gnarled Root Dungeon)",
        "dungeon": 1,
        "room": 0x0419,
        "collect": COLLECT_CHEST,
        "map_tile": 0x96,
    },
    LocationName.gnarled_root_dungeon_hidden_chest_revealed_by_button: {
        "region_id": "d1 button chest",
        "vanilla_item": "Small Key (Gnarled Root Dungeon)",
        "dungeon": 1,
        "room": 0x0411,
        "collect": COLLECT_CHEST,
        "map_tile": 0x96,
    },
    LocationName.gnarled_root_dungeon_chest_in_goriya_room: {
        "region_id": "d1 goriya chest",
        "vanilla_item": "Boss Key (Gnarled Root Dungeon)",
        "dungeon": 1,
        "room": 0x0414,
        "collect": COLLECT_CHEST,
        "map_tile": 0x96,
    },
    LocationName.gnarled_root_dungeon_boss_reward: {
        "region_id": "d1 boss",
        "vanilla_item": "Heart Container",
        "dungeon": 1,
        "room": 0x0412,
        "collect": COLLECT_POOF,
        "map_tile": 0x96,
        "symbolic_name": "d1Boss",
    },
    LocationName.snakes_remains_drop_in_left_rope_room: {
        "region_id": "d2 rope drop",
        "vanilla_item": "Small Key (Snake's Remains)",
        "dungeon": 2,
        "room": 0x0434,
        "collect": COLLECT_DROP,
        "map_tile": 0x8D,
        "symbolic_name": "d2RopeDrop",
    },
    LocationName.snakes_remains_chest_in_distant_moblins_room: {
        "region_id": "d2 moblin chest",
        "vanilla_item": "Power Bracelet",
        "dungeon": 2,
        "room": 0x042A,
        "collect": COLLECT_CHEST,
        "map_tile": 0x8D,
    },
    LocationName.snakes_remains_chest_in_rollers_section: {
        "region_id": "d2 roller chest",
        "vanilla_item": "Rupees (10)",
        "dungeon": 2,
        "room": 0x041F,
        "collect": COLLECT_CHEST,
        "map_tile": 0x8D,
    },
    LocationName.snakes_remains_chest_left_from_entrance: {
        "region_id": "d2 left from entrance",
        "vanilla_item": "Rupees (5)",
        "dungeon": 2,
        "room": 0x0438,
        "collect": COLLECT_CHEST,
        "map_tile": 0x8D,
    },
    LocationName.snakes_remains_chest_behind_pots_in_hardhat_room: {
        "region_id": "d2 pot chest",
        "vanilla_item": "Dungeon Map (Snake's Remains)",
        "dungeon": 2,
        "room": 0x042B,
        "collect": COLLECT_CHEST,
        "map_tile": 0x8D,
    },
    LocationName.snakes_remains_chest_in_right_rope_room: {
        "region_id": "d2 rope chest",
        "vanilla_item": "Compass (Snake's Remains)",
        "dungeon": 2,
        "room": 0x0436,
        "collect": COLLECT_CHEST,
        "map_tile": 0x8D,
    },
    LocationName.snakes_remains_chest_in_moving_blades_room: {
        "region_id": "d2 blade chest",
        "vanilla_item": "Small Key (Snake's Remains)",
        "dungeon": 2,
        "room": 0x0431,
        "collect": COLLECT_CHEST,
        "map_tile": 0x8D,
    },
    LocationName.snakes_remains_chest_in_bomb_spiral_maze_room: {
        "region_id": "d2 spiral chest",
        "vanilla_item": "Small Key (Snake's Remains)",
        "dungeon": 2,
        "room": 0x042D,
        "collect": COLLECT_CHEST,
        "map_tile": 0x8D,
    },
    LocationName.snakes_remains_chest_on_terrace: {
        "region_id": "d2 terrace chest",
        "vanilla_item": "Boss Key (Snake's Remains)",
        "dungeon": 2,
        "room": 0x0424,
        "collect": COLLECT_CHEST,
        "map_tile": 0x8D,
    },
    LocationName.snakes_remains_boss_reward: {
        "region_id": "d2 boss",
        "vanilla_item": "Heart Container",
        "dungeon": 2,
        "room": 0x0429,
        "collect": COLLECT_POOF,
        "map_tile": 0x8D,
        "symbolic_name": "d2Boss",
    },
    LocationName.poison_moths_lair_b1f_chest_in_roller_room: {
        "region_id": "d3 roller chest",
        "vanilla_item": "Small Key (Poison Moth's Lair)",
        "dungeon": 3,
        "room": 0x044C,
        "collect": COLLECT_CHEST,
        "map_tile": 0x60,
    },
    LocationName.poison_moths_lair_1f_chest_in_mimics_room: {
        "region_id": "d3 mimic chest",
        "vanilla_item": "Progressive Feather",
        "dungeon": 3,
        "room": 0x0450,
        "collect": COLLECT_CHEST,
        "map_tile": 0x60,
    },
    LocationName.poison_moths_lair_1f_chest_above_east_trampoline: {
        "region_id": "d3 zol chest",
        "vanilla_item": "Small Key (Poison Moth's Lair)",
        "dungeon": 3,
        "room": 0x044F,
        "collect": COLLECT_CHEST,
        "map_tile": 0x60,
    },
    LocationName.poison_moths_lair_b1f_chest_in_watery_room: {
        "region_id": "d3 water room",
        "vanilla_item": "Rupees (30)",
        "dungeon": 3,
        "room": 0x0441,
        "collect": COLLECT_CHEST,
        "map_tile": 0x60,
    },
    LocationName.poison_moths_lair_b1f_chest_on_quicksand_terrace: {
        "region_id": "d3 quicksand terrace",
        "vanilla_item": "Gasha Seed",
        "dungeon": 3,
        "room": 0x0444,
        "collect": COLLECT_CHEST,
        "map_tile": 0x60,
    },
    LocationName.poison_moths_lair_1f_chest_in_moldorm_room: {
        "region_id": "d3 moldorm chest",
        "vanilla_item": "Bombs (10)",
        "dungeon": 3,
        "room": 0x0454,
        "collect": COLLECT_CHEST,
        "map_tile": 0x60,
    },
    LocationName.poison_moths_lair_1f_chest_above_west_trampoline_owl: {
        "region_id": "d3 trampoline chest",
        "vanilla_item": "Compass (Poison Moth's Lair)",
        "dungeon": 3,
        "room": 0x044D,
        "collect": COLLECT_CHEST,
        "map_tile": 0x60,
    },
    LocationName.poison_moths_lair_1f_chest_in_room_behind_hidden_cracked_wall: {
        "region_id": "d3 bombed wall chest",
        "vanilla_item": "Dungeon Map (Poison Moth's Lair)",
        "dungeon": 3,
        "room": 0x0451,
        "collect": COLLECT_CHEST,
        "map_tile": 0x60,
    },
    LocationName.poison_moths_lair_b1f_chest_in_moving_blade_room: {
        "region_id": "d3 giant blade room",
        "vanilla_item": "Boss Key (Poison Moth's Lair)",
        "dungeon": 3,
        "room": 0x0446,
        "collect": COLLECT_CHEST,
        "map_tile": 0x60,
    },
    LocationName.poison_moths_lair_1f_boss_reward: {
        "region_id": "d3 boss",
        "vanilla_item": "Heart Container",
        "dungeon": 3,
        "room": 0x0453,
        "collect": COLLECT_POOF,
        "map_tile": 0x60,
        "symbolic_name": "d3Boss",
    },
    LocationName.dancing_dragon_dungeon_2f_pots_on_buttons_puzzle_drop: {
        "region_id": "d4 pot puzzle",
        "vanilla_item": "Small Key (Dancing Dragon Dungeon)",
        "dungeon": 4,
        "room": 0x047B,
        "collect": COLLECT_DROP,
        "map_tile": 0x1D,
        "symbolic_name": "d4PotPuzzle",
    },
    LocationName.dancing_dragon_dungeon_2f_chest_north_of_entrance: {
        "region_id": "d4 north of entrance",
        "vanilla_item": "Bombs (10)",
        "dungeon": 4,
        "room": 0x047F,
        "collect": COLLECT_CHEST,
        "map_tile": 0x1D,
    },
    LocationName.dancing_dragon_dungeon_1f_chest_in_southwest_quadrant_of_beamos_room: {
        "region_id": "d4 maze chest",
        "vanilla_item": "Dungeon Map (Dancing Dragon Dungeon)",
        "dungeon": 4,
        "room": 0x0469,
        "collect": COLLECT_CHEST,
        "map_tile": 0x1D,
    },
    LocationName.dancing_dragon_dungeon_1f_dark_room_chest: {
        "region_id": "d4 dark room",
        "vanilla_item": "Small Key (Dancing Dragon Dungeon)",
        "dungeon": 4,
        "room": 0x046D,
        "collect": COLLECT_CHEST,
        "map_tile": 0x1D,
    },
    LocationName.dancing_dragon_dungeon_2f_chest_in_water_donut_room: {
        "region_id": "d4 water ring room",
        "vanilla_item": "Compass (Dancing Dragon Dungeon)",
        "dungeon": 4,
        "room": 0x0483,
        "collect": COLLECT_CHEST,
        "map_tile": 0x1D,
    },
    LocationName.dancing_dragon_dungeon_2f_pool_drop: {
        "region_id": "d4 pool",
        "vanilla_item": "Small Key (Dancing Dragon Dungeon)",
        "dungeon": 4,
        "room": 0x0475,
        "collect": COLLECT_DROP,
        "map_tile": 0x1D,
        "symbolic_name": "d4Pool",
    },
    LocationName.dancing_dragon_dungeon_1f_chest_on_small_terrace: {
        "region_id": "d4 terrace",
        "vanilla_item": "Small Key (Dancing Dragon Dungeon)",
        "dungeon": 4,
        "room": 0x0463,
        "collect": COLLECT_D4_SCRUB_ROOM,
        "is_chest": True,
        "map_tile": 0x1D,
    },
    LocationName.dancing_dragon_dungeon_1f_chest_revealed_by_minecart_torches: {
        "region_id": "d4 torch chest",
        "vanilla_item": "Small Key (Dancing Dragon Dungeon)",
        "dungeon": 4,
        "room": 0x0464,
        "collect": COLLECT_CHEST,
        "map_tile": 0x1D,
    },
    LocationName.dancing_dragon_dungeon_1f_crumbling_room_chest: {
        "region_id": "d4 cracked floor room",
        "vanilla_item": "Progressive Slingshot",
        "dungeon": 4,
        "room": 0x0473,
        "collect": COLLECT_CHEST,
        "map_tile": 0x1D,
    },
    LocationName.dancing_dragon_dungeon_1f_eye_diving_spot_item: {
        "region_id": "d4 dive spot",
        "vanilla_item": "Boss Key (Dancing Dragon Dungeon)",
        "dungeon": 4,
        "room": 0x046C,
        "collect": COLLECT_DIVE,
        "map_tile": 0x1D,
        "symbolic_name": "d4DiveSpot",
    },
    LocationName.dancing_dragon_dungeon_b1f_boss_reward: {
        "region_id": "d4 boss",
        "vanilla_item": "Heart Container",
        "dungeon": 4,
        "room": 0x045F,
        "collect": COLLECT_POOF,
        "map_tile": 0x1D,
        "symbolic_name": "d4Boss",
    },
    LocationName.unicorns_cave_right_cart_chest: {
        "region_id": "d5 cart chest",
        "vanilla_item": "Small Key (Unicorn's Cave)",
        "dungeon": 5,
        "room": 0x0499,
        "collect": COLLECT_CHEST,
        "map_tile": 0x8A,
    },
    LocationName.unicorns_cave_chest_left_from_entrance: {
        "region_id": "d5 left chest",
        "vanilla_item": "Small Key (Unicorn's Cave)",
        "dungeon": 5,
        "room": 0x04A3,
        "collect": COLLECT_CHEST,
        "map_tile": 0x8A,
    },
    LocationName.unicorns_cave_magnet_gloves_chest: {
        "region_id": "d5 magnet ball chest",
        "vanilla_item": "Magnetic Gloves",
        "dungeon": 5,
        "room": 0x0489,
        "collect": COLLECT_CHEST,
        "map_tile": 0x8A,
    },
    LocationName.unicorns_cave_terrace_chest: {
        "region_id": "d5 terrace chest",
        "vanilla_item": "Rupees (100)",
        "dungeon": 5,
        "room": 0x0497,
        "collect": COLLECT_CHEST,
        "map_tile": 0x8A,
    },
    LocationName.unicorns_cave_armos_puzzle_room_chest: {
        "region_id": "d5 armos chest",
        "vanilla_item": "Small Key (Unicorn's Cave)",
        "dungeon": 5,
        "room": 0x0491,
        "collect": COLLECT_D5_ARMOS_PUZZLE,
        "map_tile": 0x8A,
        "symbolic_name": "d5ArmosChest",
    },
    LocationName.unicorns_cave_gibdo_room_chest: {
        "region_id": "d5 gibdo/zol chest",
        "vanilla_item": "Dungeon Map (Unicorn's Cave)",
        "dungeon": 5,
        "room": 0x048F,
        "collect": COLLECT_CHEST,
        "map_tile": 0x8A,
    },
    LocationName.unicorns_cave_quicksand_spiral_chest: {
        "region_id": "d5 spiral chest",
        "vanilla_item": "Compass (Unicorn's Cave)",
        "dungeon": 5,
        "room": 0x049D,
        "collect": COLLECT_CHEST,
        "map_tile": 0x8A,
    },
    LocationName.unicorns_cave_magnet_spinner_chest: {
        "region_id": "d5 spinner chest",
        "vanilla_item": "Small Key (Unicorn's Cave)",
        "dungeon": 5,
        "room": 0x049F,
        "collect": COLLECT_CHEST,
        "map_tile": 0x8A,
    },
    LocationName.unicorns_cave_chest_in_right_half_of_minecart_bay_room: {
        "region_id": "d5 stalfos room",
        "vanilla_item": "Small Key (Unicorn's Cave)",
        "dungeon": 5,
        "room": 0x04A5,
        "collect": COLLECT_CHEST,
        "map_tile": 0x8A,
    },
    LocationName.unicorns_cave_treadmills_basement_item: {
        "region_id": "d5 basement",
        "vanilla_item": "Boss Key (Unicorn's Cave)",
        "dungeon": 5,
        "room": 0x068B,
        "collect": COLLECT_TOUCH,
        "map_tile": 0x8A,
        "symbolic_name": "d5Basement",
    },
    LocationName.unicorns_cave_boss_reward: {
        "region_id": "d5 boss",
        "vanilla_item": "Heart Container",
        "dungeon": 5,
        "room": 0x048C,
        "collect": COLLECT_POOF,
        "map_tile": 0x8A,
        "symbolic_name": "d5Boss",
    },
    LocationName.ancient_ruins_1f_magnet_ball_puzzle_drop: {
        "region_id": "d6 magnet ball drop",
        "vanilla_item": "Small Key (Ancient Ruins)",
        "dungeon": 6,
        "room": 0x04AB,
        "collect": COLLECT_DROP,
        "map_tile": 0x00,
        "symbolic_name": "d6MagnetBallDrop",
    },
    LocationName.ancient_ruins_2f_chest_north_of_main_spinner: {
        "region_id": "d6 spinner north",
        "vanilla_item": "Small Key (Ancient Ruins)",
        "dungeon": 6,
        "room": 0x04C2,
        "collect": COLLECT_CHEST,
        "map_tile": 0x00,
    },
    LocationName.ancient_ruins_3f_armos_hall_chest: {
        "region_id": "d6 armos hall",
        "vanilla_item": "Progressive Boomerang",
        "dungeon": 6,
        "room": 0x04D0,
        "collect": COLLECT_CHEST,
        "map_tile": 0x00,
    },
    LocationName.ancient_ruins_1f_crystal_maze_room_chest: {
        "region_id": "d6 crystal trap room",
        "vanilla_item": "Rupees (10)",
        "dungeon": 6,
        "room": 0x04AF,
        "collect": COLLECT_CHEST,
        "map_tile": 0x00,
    },
    LocationName.ancient_ruins_1f_crumbling_ground_room_chest: {
        "region_id": "d6 1F east",
        "vanilla_item": "Rupees (5)",
        "dungeon": 6,
        "room": 0x04B3,
        "collect": COLLECT_CHEST,
        "map_tile": 0x00,
    },
    LocationName.ancient_ruins_2f_chest_in_gibdo_room: {
        "region_id": "d6 2F gibdo chest",
        "vanilla_item": "Bombs (10)",
        "dungeon": 6,
        "room": 0x04BF,
        "collect": COLLECT_CHEST,
        "map_tile": 0x00,
    },
    LocationName.ancient_ruins_2f_chest_between_4_armos: {
        "region_id": "d6 2F armos chest",
        "vanilla_item": "Rupees (5)",
        "dungeon": 6,
        "room": 0x04C3,
        "collect": COLLECT_CHEST,
        "map_tile": 0x00,
    },
    LocationName.ancient_ruins_1f_chest_in_beamos_room: {
        "region_id": "d6 beamos room",
        "vanilla_item": "Compass (Ancient Ruins)",
        "dungeon": 6,
        "room": 0x04AD,
        "collect": COLLECT_CHEST,
        "map_tile": 0x00,
    },
    LocationName.ancient_ruins_1f_chest_on_terrace_left_of_entrance: {
        "region_id": "d6 1F terrace",
        "vanilla_item": "Dungeon Map (Ancient Ruins)",
        "dungeon": 6,
        "room": 0x04B0,
        "collect": COLLECT_CHEST,
        "map_tile": 0x00,
    },
    LocationName.ancient_ruins_2f_chest_after_time_trial: {
        "region_id": "d6 escape room",
        "vanilla_item": "Boss Key (Ancient Ruins)",
        "dungeon": 6,
        "room": 0x04C4,
        "collect": COLLECT_CHEST,
        "map_tile": 0x00,
    },
    LocationName.ancient_ruins_2f_chest_on_red_terrace_before_vire: {
        "region_id": "d6 vire chest",
        "vanilla_item": "Small Key (Ancient Ruins)",
        "dungeon": 6,
        "room": 0x04C1,
        "collect": COLLECT_CHEST,
        "map_tile": 0x00,
    },
    LocationName.ancient_ruins_5f_boss_reward: {
        "region_id": "d6 boss",
        "vanilla_item": "Heart Container",
        "dungeon": 6,
        "room": 0x04D5,
        "collect": COLLECT_POOF,
        "map_tile": 0x00,
        "symbolic_name": "d6Boss",
    },
    LocationName.explorers_crypt_1f_chest_in_wizzrobe_room: {
        "region_id": "d7 wizzrobe chest",
        "vanilla_item": "Small Key (Explorer's Crypt)",
        "dungeon": 7,
        "room": 0x0554,
        "collect": COLLECT_CHEST,
        "map_tile": 0xD0,
    },
    LocationName.explorers_crypt_b1f_chest_in_fast_moving_platform_room: {
        "region_id": "d7 spike chest",
        "vanilla_item": "Progressive Feather",
        "dungeon": 7,
        "room": 0x0544,
        "collect": COLLECT_CHEST,
        "map_tile": 0xD0,
    },
    LocationName.explorers_crypt_b2f_stair_maze_chest: {
        "region_id": "d7 maze chest",
        "vanilla_item": "Rupees (1)",
        "dungeon": 7,
        "room": 0x0543,
        "collect": COLLECT_CHEST,
        "map_tile": 0xD0,
    },
    LocationName.explorers_crypt_1f_chest_right_of_entrance: {
        "region_id": "d7 right of entrance",
        "vanilla_item": "Power Ring L-1",
        "dungeon": 7,
        "room": 0x055A,
        "collect": COLLECT_CHEST,
        "map_tile": 0xD0,
    },
    LocationName.explorers_crypt_1f_chest_behind_cracked_wall: {
        "region_id": "d7 bombed wall chest",
        "vanilla_item": "Compass (Explorer's Crypt)",
        "dungeon": 7,
        "room": 0x0552,
        "collect": COLLECT_POE_SKIP_ROOM,
        "is_chest": True,
        "map_tile": 0xD0,
    },
    LocationName.explorers_crypt_b1f_zol_button_drop: {
        "region_id": "d7 zol button",
        "vanilla_item": "Small Key (Explorer's Crypt)",
        "dungeon": 7,
        "room": 0x0545,
        "collect": COLLECT_DROP,
        "map_tile": 0xD0,
        "symbolic_name": "d7ZolButton",
    },
    LocationName.explorers_crypt_b2f_armos_puzzle_drop: {
        "region_id": "d7 armos puzzle",
        "vanilla_item": "Small Key (Explorer's Crypt)",
        "dungeon": 7,
        "room": 0x0535,
        "collect": COLLECT_DROP,
        "map_tile": 0xD0,
        "symbolic_name": "d7ArmosPuzzle",
    },
    LocationName.explorers_crypt_b1f_chest_connected_to_magnet_ball_button: {
        "region_id": "d7 magunesu chest",
        "vanilla_item": "Small Key (Explorer's Crypt)",
        "dungeon": 7,
        "room": 0x0547,
        "collect": COLLECT_CHEST,
        "map_tile": 0xD0,
    },
    LocationName.explorers_crypt_1f_chest_above_trampoline_near_2nd_poe: {
        "region_id": "d7 quicksand chest",
        "vanilla_item": "Dungeon Map (Explorer's Crypt)",
        "dungeon": 7,
        "room": 0x0558,
        "collect": COLLECT_CHEST,
        "map_tile": 0xD0,
    },
    LocationName.explorers_crypt_b2f_drop_in_room_north_of_stair_maze: {
        "region_id": "d7 B2F drop",
        "vanilla_item": "Small Key (Explorer's Crypt)",
        "dungeon": 7,
        "room": 0x053D,
        "collect": COLLECT_DROP,
        "map_tile": 0xD0,
        "symbolic_name": "d7DropNorthOfStairMaze",
    },
    LocationName.explorers_crypt_b1f_chest_in_jumping_stalfos_room: {
        "region_id": "d7 stalfos chest",
        "vanilla_item": "Boss Key (Explorer's Crypt)",
        "dungeon": 7,
        "room": 0x0548,
        "collect": COLLECT_CHEST,
        "map_tile": 0xD0,
    },
    LocationName.explorers_crypt_b1f_boss_reward: {
        "region_id": "d7 boss",
        "vanilla_item": "Heart Container",
        "dungeon": 7,
        "room": 0x0550,
        "collect": COLLECT_POOF,
        "map_tile": 0xD0,
        "symbolic_name": "d7Boss",
    },
    LocationName.sword_shield_dungeon_1f_eye_drop_near_entrance: {
        "region_id": "d8 eye drop",
        "vanilla_item": "Small Key (Sword & Shield Dungeon)",
        "dungeon": 8,
        "room": 0x0582,
        "collect": COLLECT_DROP,
        "map_tile": 0x04,
        "symbolic_name": "d8EyeDrop",
    },
    LocationName.sword_shield_dungeon_1f_three_eyes_chest: {
        "region_id": "d8 three eyes chest",
        "vanilla_item": "Steadfast Ring",
        "dungeon": 8,
        "room": 0x057D,
        "collect": COLLECT_CHEST,
        "map_tile": 0x04,
    },
    LocationName.sword_shield_dungeon_1f_drop_in_hardhat_magnet_ball_room: {
        "region_id": "d8 hardhat drop",
        "vanilla_item": "Small Key (Sword & Shield Dungeon)",
        "dungeon": 8,
        "room": 0x0575,
        "collect": COLLECT_DROP,
        "map_tile": 0x04,
        "symbolic_name": "d8HardhatDrop",
    },
    LocationName.sword_shield_dungeon_1f_u_shaped_spiky_freezer_chest: {
        "region_id": "d8 spike room",
        "vanilla_item": "Compass (Sword & Shield Dungeon)",
        "dungeon": 8,
        "room": 0x058B,
        "collect": COLLECT_CHEST,
        "map_tile": 0x04,
    },
    LocationName.sword_shield_dungeon_b1f_chest_right_of_spinner: {
        "region_id": "d8 spinner chest",
        "vanilla_item": "Small Key (Sword & Shield Dungeon)",
        "dungeon": 8,
        "room": 0x0570,
        "collect": COLLECT_CHEST,
        "map_tile": 0x04,
    },
    LocationName.sword_shield_dungeon_1f_top_chest_in_lava_bridge_room: {
        "region_id": "d8 armos chest",
        "vanilla_item": "Progressive Slingshot",
        "dungeon": 8,
        "room": 0x058D,
        "collect": COLLECT_CHEST,
        "map_tile": 0x04,
    },
    LocationName.sword_shield_dungeon_1f_bottom_chest_in_lava_bridge_room: {
        "region_id": "d8 magnet ball room",
        "vanilla_item": "Dungeon Map (Sword & Shield Dungeon)",
        "dungeon": 8,
        "room": 0x058E,
        "collect": COLLECT_CHEST,
        "map_tile": 0x04,
    },
    LocationName.sword_shield_dungeon_1f_chest_in_bombable_blocks_room: {
        "region_id": "d8 darknut chest",
        "vanilla_item": "Small Key (Sword & Shield Dungeon)",
        "dungeon": 8,
        "room": 0x058C,
        "collect": COLLECT_CHEST,
        "map_tile": 0x04,
    },
    LocationName.sword_shield_dungeon_1f_chest_on_terrace_after_pols_voice_room: {
        "region_id": "d8 pols voice chest",
        "vanilla_item": "Boss Key (Sword & Shield Dungeon)",
        "dungeon": 8,
        "room": 0x0580,
        "collect": COLLECT_CHEST,
        "map_tile": 0x04,
    },
    LocationName.sword_shield_dungeon_1f_ghost_armos_puzzle_drop: {
        "region_id": "d8 ghost armos drop",
        "vanilla_item": "Small Key (Sword & Shield Dungeon)",
        "dungeon": 8,
        "room": 0x057F,
        "collect": COLLECT_DROP,
        "map_tile": 0x04,
        "symbolic_name": "d8GhostArmosDrop",
    },
    LocationName.sword_shield_dungeon_b1f_southeast_lava_chest: {
        "region_id": "d8 SE lava chest",
        "vanilla_item": "Small Key (Sword & Shield Dungeon)",
        "dungeon": 8,
        "room": 0x056B,
        "collect": COLLECT_CHEST,
        "map_tile": 0x04,
    },
    LocationName.sword_shield_dungeon_b1f_southwest_lava_chest: {
        "region_id": "d8 SW lava chest",
        "vanilla_item": "Bombs (10)",
        "dungeon": 8,
        "room": 0x056A,
        "collect": COLLECT_CHEST,
        "map_tile": 0x04,
    },
    LocationName.sword_shield_dungeon_1f_chest_in_sparks_pots_room: {
        "region_id": "d8 spark chest",
        "vanilla_item": "Small Key (Sword & Shield Dungeon)",
        "dungeon": 8,
        "room": 0x058A,
        "collect": COLLECT_CHEST,
        "map_tile": 0x04,
    },
    LocationName.sword_shield_dungeon_b1f_boss_reward: {
        "region_id": "d8 boss",
        "vanilla_item": "Heart Container",
        "dungeon": 8,
        "room": 0x0564,
        "collect": COLLECT_POOF,
        "map_tile": 0x04,
        "symbolic_name": "d8Boss",
    },
    LocationName.horon_village_item_behind_small_tree: {
        "region_id": "horon heart piece",
        "vanilla_item": "Piece of Heart",
        "conditional": True,
        "room": 0x00D8,
        "collect": COLLECT_TOUCH,
        "symbolic_name": "horonHeartPiece",
    },
    LocationName.woods_of_winter_item_below_lake: {
        "region_id": "woods of winter heart piece",
        "vanilla_item": "Piece of Heart",
        "conditional": True,
        "room": 0x00AF,
        "collect": COLLECT_TOUCH,
        "symbolic_name": "woodsOfWinterHeartPiece",
    },
    LocationName.mt_cucco_item_on_ledge: {
        "region_id": "mt. cucco heart piece",
        "vanilla_item": "Piece of Heart",
        "conditional": True,
        "room": 0x002D,
        "collect": COLLECT_TOUCH,
        "symbolic_name": "mtCuccoHeartPiece",
    },
    LocationName.eastern_suburbs_item_in_windmill_cave: {
        "region_id": "windmill heart piece",
        "vanilla_item": "Piece of Heart",
        "conditional": True,
        "room": 0x05B2,
        "collect": COLLECT_TOUCH,
        "map_tile": 0xEA,
        "symbolic_name": "windmillHeartPiece",
    },
    LocationName.western_coast_item_in_graveyard: {
        "region_id": "graveyard heart piece",
        "vanilla_item": "Piece of Heart",
        "conditional": True,
        "room": 0x00D1,
        "collect": COLLECT_TOUCH,
        "symbolic_name": "graveyardHeartPiece",
    },
    LocationName.spool_swamp_item_amidst_currents_in_spring: {
        "region_id": "spool swamp heart piece",
        "vanilla_item": "Piece of Heart",
        "conditional": True,
        "room": 0x00B1,
        "collect": COLLECT_TOUCH,
        "symbolic_name": "spoolSwampHeartPiece",
    },
    LocationName.temple_remains_item_in_cave_behind_rockslide: {
        "region_id": "temple remains heart piece",
        "vanilla_item": "Piece of Heart",
        "conditional": True,
        "room": 0x05C7,
        "collect": COLLECT_TOUCH,
        "map_tile": 0x15,
        "symbolic_name": "templeRemainsHeartPiece",
    },
    LocationName.horon_village_item_behind_cracked_wall_in_mayors_house: {
        "region_id": "mayor's house secret room",
        "vanilla_item": "Gasha Seed",
        "conditional": True,
        "room": 0x0387,
        "collect": COLLECT_TOUCH,
        "map_tile": 0xC8,
        "symbolic_name": "mayorsHouseSecretRoom",
    },
    LocationName.subrosia_item_in_house_above_strange_brothers_portal: {
        "region_id": "subrosian house",
        "vanilla_item": "Gasha Seed",
        "conditional": True,
        "room": 0x03A1,
        "collect": COLLECT_TOUCH,
        "map_tile": 0x1E,
        "symbolic_name": "subrosianHouse",
    },
    LocationName.subrosia_item_in_basement_to_tower_of_spring: {
        "region_id": "subrosian 2d cave",
        "vanilla_item": "Gasha Seed",
        "conditional": True,
        "room": 0x07E3,
        "collect": COLLECT_TOUCH,
        "map_tile": 0x1E,
        "symbolic_name": "subrosian2dCave",
    },
    LocationName.horon_village_mayors_gift: {
        "region_id": "mayor's gift",
        "vanilla_item": "Gasha Seed",
        "room": 0x0386,
        "collect": COLLECT_TOUCH,
        "map_tile": 0xC8,
        "symbolic_name": "mayorGift",
    },
    LocationName.horon_village_vasus_gift: {
        "region_id": "vasu's gift",
        "vanilla_item": "Friendship Ring",
        "room": 0x0391,
        "collect": COLLECT_TOUCH,
        "map_tile": 0xE8,
        "symbolic_name": "vasuGift",
    },
    LocationName.goron_mountain_lonely_gorons_gift: {
        "region_id": "goron's gift",
        "vanilla_item": "Biggoron's Sword",  # Ring Box doesn't really exist anymore
        "room": 0x05C5,
        "collect": COLLECT_TOUCH,
        "map_tile": 0x19,
        "symbolic_name": "goronGift",
    },
    LocationName.horon_village_dr_left_reward: {
        "region_id": "dr. left reward",
        "vanilla_item": "Cuccodex",
        "conditional": True,
        "room": 0x03A4,
        "collect": COLLECT_TOUCH,
        "map_tile": 0xF9,
        "symbolic_name": "drLeftReward",
    },
    LocationName.north_horon_malon_trade: {
        "region_id": "malon trade",
        "vanilla_item": "Lon Lon Egg",
        "conditional": True,
        "room": 0x0380,
        "collect": COLLECT_TOUCH,
        "map_tile": 0x88,
        "symbolic_name": "malonTrade",
    },
    LocationName.maple_trade: {
        "region_id": "maple trade",
        "vanilla_item": "Ghastly Doll",
        "conditional": True,
        "flag_byte": 0xC640,
        "bit_mask": 0x08,
        "room": [],
        "symbolic_name": "mapleTrade",
    },
    LocationName.holodrum_plain_mrs_ruul_trade: {
        "region_id": "mrs. ruul trade",
        "vanilla_item": "Iron Pot",
        "conditional": True,
        "room": 0x03B3,
        "collect": COLLECT_TOUCH,
        "map_tile": 0xA3,
        "symbolic_name": "mrsRuulTrade",
    },
    LocationName.subrosian_chef_trade: {
        "region_id": "subrosian chef trade",
        "vanilla_item": "Lava Soup",
        "conditional": True,
        "room": 0x038F,
        "collect": COLLECT_TOUCH,
        "map_tile": 0x9A,
        "symbolic_name": "subrosianChefTrade",
    },
    LocationName.biggoron_trade: {
        "region_id": "biggoron trade",
        "vanilla_item": "Goron Vase",
        "conditional": True,
        "bit_mask": 0x40,
        "room": 0x0008,
        "collect": COLLECT_TOUCH,
        "symbolic_name": "biggoronTrade",
    },
    LocationName.sunken_city_ingo_trade: {
        "region_id": "ingo trade",
        "vanilla_item": "Fish",
        "conditional": True,
        "room": 0x0399,
        "collect": COLLECT_TOUCH,
        "map_tile": 0x4D,
        "symbolic_name": "ingoTrade",
    },
    LocationName.north_horon_yelling_old_man_trade: {
        "region_id": "old man trade",
        "vanilla_item": "Megaphone",
        "conditional": True,
        "room": 0x00B7,
        "collect": COLLECT_TOUCH,
        "symbolic_name": "yellingOldManTrade",
    },
    LocationName.mt_cucco_talon_trade: {
        "region_id": "talon trade",
        "vanilla_item": "Mushroom",
        "conditional": True,
        "bit_mask": 0x40,
        "room": 0x05B6,
        "map_tile": 0x1B,
        "symbolic_name": "talonTrade",
    },
    LocationName.sunken_city_syrup_trade: {
        "region_id": "syrup trade",
        "vanilla_item": "Wooden Bird",
        "conditional": True,
        "room": 0x039C,
        "collect": COLLECT_TOUCH,
        "map_tile": 0x5E,
        "symbolic_name": "syrupTrade",
    },
    LocationName.horon_village_tick_tock_trade: {
        "region_id": "tick tock trade",
        "vanilla_item": "Engine Grease",
        "conditional": True,
        "room": 0x0383,
        "collect": COLLECT_TOUCH,
        "map_tile": 0xD7,
        "symbolic_name": "tickTockTrade",
    },
    LocationName.eastern_suburbs_guru_guru_trade: {
        "region_id": "guru-guru trade",
        "vanilla_item": "Phonograph",
        "conditional": True,
        "room": 0x00DA,
        "collect": COLLECT_TOUCH,
        "symbolic_name": "guruguruTrade",
    },
    LocationName.subrosia_buried_bomb_flower: {
        "region_id": "subrosian buried bomb flower",
        "vanilla_item": "Bomb Flower",
        "room": 0x0169,
        "collect": COLLECT_TOUCH,
        "map_tile": 0xB9,
        "symbolic_name": "bombFlower",
    },
    LocationName.subrosia_sign_loving_guy_reward: {
        "region_id": "subrosian sign guy",
        "vanilla_item": "Sign Ring",
        "room": 0x03A9,
        "collect": COLLECT_TOUCH,
        "map_tile": 0xB9,
        "symbolic_name": "subrosianSignLovingGuy",
    },
    # Maku seed is 0xC85D
    LocationName.horon_village_old_man: {
        "region_id": "old man in horon",
        "bit_mask": 0x40,
        "vanilla_item": "Filler Item",
        "conditional": True,
        "room": 0x0505,
        "collect": COLLECT_TOUCH,
        "map_tile": 0xF9,
        "symbolic_name": "oldManHoronVillage",
    },
    LocationName.north_horon_old_man_near_d1: {
        "region_id": "old man near d1",
        "bit_mask": 0x40,
        "vanilla_item": "Filler Item",
        "conditional": True,
        "room": 0x0503,
        "collect": COLLECT_TOUCH,
        "map_tile": 0x97,
        "symbolic_name": "oldManNearD1",
    },
    LocationName.holodrum_plain_old_man_near_blainos_gym: {
        "region_id": "old man near blaino",
        "bit_mask": 0x40,
        "vanilla_item": "Filler Item",
        "conditional": True,
        "room": 0x0502,
        "collect": COLLECT_TOUCH,
        "map_tile": 0x76,
        "symbolic_name": "oldManNearBlaino",
    },
    LocationName.goron_mountain_old_man: {
        "region_id": "old man in goron mountain",
        "bit_mask": 0x40,
        "vanilla_item": "Filler Item",
        "conditional": True,
        "room": 0x0501,
        "collect": COLLECT_TOUCH,
        "map_tile": 0x28,
        "symbolic_name": "oldManGoronMountain",
    },
    LocationName.western_coast_old_man: {
        "region_id": "old man near western coast house",
        "bit_mask": 0x40,
        "vanilla_item": "Filler Item",
        "conditional": True,
        "room": 0x0504,
        "collect": COLLECT_TOUCH,
        "map_tile": 0xD2,
        "symbolic_name": "oldManWesternCoast",
    },
    LocationName.woods_of_winter_old_man: {
        "region_id": "old man near holly's house",
        "bit_mask": 0x40,
        "vanilla_item": "Filler Item",
        "conditional": True,
        "room": 0x0507,
        "collect": COLLECT_TOUCH,
        "map_tile": 0x8F,
        "symbolic_name": "oldManWoodsOfWinter",
    },
    LocationName.holodrum_plain_old_man_near_mrs_ruuls_house: {
        "region_id": "old man near mrs. ruul",
        "bit_mask": 0x40,
        "vanilla_item": "Filler Item",
        "conditional": True,
        "room": 0x0508,
        "collect": COLLECT_TOUCH,
        "map_tile": 0xA4,
        "symbolic_name": "oldManGhastlyStump",
    },
    LocationName.tarm_ruins_old_man_near_d6: {
        "region_id": "old man near d6",
        "bit_mask": 0x40,
        "vanilla_item": "Filler Item",
        "conditional": True,
        "room": 0x0506,
        "collect": COLLECT_TOUCH,
        "map_tile": 0x02,
        "symbolic_name": "oldManTarmRuins",
    },
    LocationName.north_horon_golden_beasts_old_man: {
        "region_id": "golden beasts old man",
        "vanilla_item": "Red Ring",
        "room": 0x0511,
        "collect": COLLECT_TOUCH,
        "map_tile": 0xA6,
        "symbolic_name": "goldenBeastsOldMan",
    },
    LocationName.horon_village_seed_tree: {
        "region_id": "horon village tree",
        "vanilla_item": "Ember Seeds",
        "local": True,
        "room": 0x00F8,
        "collect": COLLECT_TOUCH,
        "symbolic_name": "horonVillageSeedTree",
    },
    LocationName.woods_of_winter_seed_tree: {
        "region_id": "woods of winter tree",
        "vanilla_item": "Mystery Seeds",
        "local": True,
        "room": 0x009E,
        "collect": COLLECT_TOUCH,
        "symbolic_name": "woodsOfWinterSeedTree",
    },
    LocationName.holodrum_plain_seed_tree: {
        "region_id": "north horon tree",
        "vanilla_item": "Scent Seeds",
        "local": True,
        "room": 0x0067,
        "collect": COLLECT_TOUCH,
        "symbolic_name": "northHoronSeedTree",
    },
    LocationName.spool_swamp_seed_tree: {
        "region_id": "spool swamp tree",
        "vanilla_item": "Pegasus Seeds",
        "local": True,
        "room": 0x0072,
        "collect": COLLECT_TOUCH,
        "symbolic_name": "spoolSwampSeedTree",
    },
    LocationName.sunken_city_seed_tree: {
        "region_id": "sunken city tree",
        "vanilla_item": "Gale Seeds",
        "local": True,
        "room": 0x005F,
        "collect": COLLECT_TOUCH,
        "symbolic_name": "sunkenCitySeedTree",
    },
    LocationName.tarm_ruins_seed_tree: {
        "region_id": "tarm ruins tree",
        "vanilla_item": "Gale Seeds",
        "local": True,
        "room": 0x0010,
        "collect": COLLECT_TOUCH,
        "symbolic_name": "tarmRuinsSeedTree",
    },
    LocationName.gnarled_root_dungeon_essence: {
        "region_id": "d1 boss",
        "dungeon": 1,
        "room": 0x0413,
        "vanilla_item": "Fertile Soil",
        "essence": True,
        "symbolic_name": "essenceD1",
    },
    LocationName.snakes_remains_essence: {
        "region_id": "d2 boss",
        "dungeon": 2,
        "room": 0x042C,
        "vanilla_item": "Gift of Time",
        "essence": True,
        "symbolic_name": "essenceD2",
    },
    LocationName.poison_moths_lair_essence: {
        "region_id": "d3 boss",
        "dungeon": 3,
        "room": 0x0440,
        "vanilla_item": "Bright Sun",
        "essence": True,
        "symbolic_name": "essenceD3",
    },
    LocationName.dancing_dragon_dungeon_essence: {
        "region_id": "d4 boss",
        "dungeon": 4,
        "room": 0x0460,
        "vanilla_item": "Soothing Rain",
        "essence": True,
        "symbolic_name": "essenceD4",
    },
    LocationName.unicorns_cave_essence: {
        "region_id": "d5 boss",
        "dungeon": 5,
        "room": 0x0488,
        "vanilla_item": "Nurturing Warmth",
        "essence": True,
        "symbolic_name": "essenceD5",
    },
    LocationName.ancient_ruins_essence: {
        "region_id": "d6 boss",
        "dungeon": 6,
        "room": 0x0398,
        "vanilla_item": "Blowing Wind",
        "essence": True,
        "symbolic_name": "essenceD6",
    },
    LocationName.explorers_crypt_essence: {
        "region_id": "d7 boss",
        "dungeon": 7,
        "room": 0x054F,
        "vanilla_item": "Seed of Life",
        "essence": True,
        "symbolic_name": "essenceD7",
    },
    LocationName.sword_shield_dungeon_essence: {
        "region_id": "d8 boss",
        "dungeon": 8,
        "room": 0x055F,
        "vanilla_item": "Changing Seasons",
        "essence": True,
        "symbolic_name": "essenceD8",
    },
    LocationName.horon_village_item_inside_maku_tree_3_essences: {
        "region_id": "maku tree, 3 essences",
        "conditional": True,
        "vanilla_item": "Gasha Seed",
        "room": 0x023B,
        "bit_mask": 0x20,
        "collect": COLLECT_TOUCH,
        "map_tile": 0xC9,
        "symbolic_name": "makuTree3Essences",
    },
    LocationName.horon_village_item_inside_maku_tree_5_essences: {
        "region_id": "maku tree, 5 essences",
        "conditional": True,
        "vanilla_item": "Gasha Seed",
        "room": 0x023B,
        "bit_mask": 0x40,
        "collect": COLLECT_TOUCH,
        "map_tile": 0xC9,
        "symbolic_name": "makuTree5Essences",
    },
    LocationName.horon_village_item_inside_maku_tree_7_essences: {
        "region_id": "maku tree, 7 essences",
        "conditional": True,
        "vanilla_item": "Gasha Seed",
        "room": 0x023B,
        "bit_mask": 0x80,
        "collect": COLLECT_TOUCH,
        "map_tile": 0xC9,
        "symbolic_name": "makuTree7Essences",
    },
    LocationName.subrosia_strange_brothers_backyard_treasure: {
        "region_id": "subrosia hide and seek",
        "vanilla_item": "Ore Chunks (50)",
        "room": 0x0160,
        "collect": COLLECT_DIG,
        "map_tile": 0x1E,
        "symbolic_name": "subrosiaHideAndSeek",
    },
    LocationName.subrosia_hot_bath_digging_spot: {
        "region_id": "subrosia bath digging spot",
        "vanilla_item": "Ore Chunks (50)",
        "conditional": True,
        "room": 0x0106,
        "collect": COLLECT_DIG,
        "map_tile": 0x1E,
        "symbolic_name": "subrosiaBathOreDiggingSpot",
    },
    LocationName.subrosia_market_portal_digging_spot: {
        "region_id": "subrosia market digging spot",
        "vanilla_item": "Ore Chunks (50)",
        "conditional": True,
        "room": 0x0157,
        "collect": COLLECT_DIG,
        "map_tile": 0xB0,
        "symbolic_name": "subrosiaMarketPortalOreDiggingSpot",
    },
    LocationName.subrosia_hard_working_subrosian_digging_spot: {
        "region_id": "subrosia market digging spot",
        "vanilla_item": "Ore Chunks (50)",
        "conditional": True,
        "room": 0x0147,
        "collect": COLLECT_DIG,
        "map_tile": 0xB0,
        "symbolic_name": "subrosiaWorkerOreDiggingSpot",
    },
    LocationName.subrosia_temple_of_seasons_digging_spot: {
        "region_id": "subrosia temple digging spot",
        "vanilla_item": "Ore Chunks (50)",
        "conditional": True,
        "room": 0x013A,
        "collect": COLLECT_DIG,
        "map_tile": 0x1E,
        "symbolic_name": "subrosiaTempleOreDiggingSpot",
    },
    LocationName.subrosia_northern_volcanoes_digging_spot: {
        "region_id": "subrosia temple digging spot",
        "vanilla_item": "Ore Chunks (50)",
        "conditional": True,
        "room": 0x0107,
        "collect": COLLECT_DIG,
        "map_tile": 0x1E,
        "symbolic_name": "subrosiaNorthernVolcanoesOreDiggingSpot",
    },
    LocationName.subrosia_d8_portal_digging_spot: {
        "region_id": "subrosia bridge digging spot",
        "vanilla_item": "Ore Chunks (50)",
        "conditional": True,
        "room": 0x0120,
        "collect": COLLECT_DIG,
        "map_tile": 0x1E,
        "symbolic_name": "subrosiaD8PortalOreDiggingSpot",
    },
    LocationName.subrosia_western_volcanoes_digging_spot: {
        "region_id": "subrosia bridge digging spot",
        "vanilla_item": "Ore Chunks (50)",
        "conditional": True,
        "room": 0x0142,
        "collect": COLLECT_DIG,
        "map_tile": 0x1E,
        "symbolic_name": "subrosiaWesternVolcanoesOreDiggingSpot",
    },
    LocationName.gasha_nut_1: {
        "region_id": "gasha tree 1",
        "vanilla_item": "Piece of Heart",
        "conditional": True,
        "flag_byte": None,
        "id": 0xC64900,
        "room": [],
    },
    LocationName.gasha_nut_2: {
        "region_id": "gasha tree 2",
        "vanilla_item": "Filler Item",
        "conditional": True,
        "flag_byte": None,
        "id": 0xC64901,
        "room": [],
    },
    LocationName.gasha_nut_3: {
        "region_id": "gasha tree 3",
        "vanilla_item": "Filler Item",
        "conditional": True,
        "flag_byte": None,
        "id": 0xC64902,
        "room": [],
    },
    LocationName.gasha_nut_4: {
        "region_id": "gasha tree 4",
        "vanilla_item": "Filler Item",
        "conditional": True,
        "flag_byte": None,
        "id": 0xC64903,
        "room": [],
    },
    LocationName.gasha_nut_5: {
        "region_id": "gasha tree 5",
        "vanilla_item": "Filler Item",
        "conditional": True,
        "flag_byte": None,
        "id": 0xC64904,
        "room": [],
    },
    LocationName.gasha_nut_6: {
        "region_id": "gasha tree 6",
        "vanilla_item": "Filler Item",
        "conditional": True,
        "flag_byte": None,
        "id": 0xC64905,
        "room": [],
    },
    LocationName.gasha_nut_7: {
        "region_id": "gasha tree 7",
        "vanilla_item": "Filler Item",
        "conditional": True,
        "flag_byte": None,
        "id": 0xC64906,
        "room": [],
    },
    LocationName.gasha_nut_8: {
        "region_id": "gasha tree 8",
        "vanilla_item": "Filler Item",
        "conditional": True,
        "flag_byte": None,
        "id": 0xC64907,
        "room": [],
    },
    LocationName.gasha_nut_9: {
        "region_id": "gasha tree 9",
        "vanilla_item": "Filler Item",
        "conditional": True,
        "flag_byte": None,
        "id": 0xC64908,
        "room": [],
    },
    LocationName.gasha_nut_10: {
        "region_id": "gasha tree 10",
        "vanilla_item": "Filler Item",
        "conditional": True,
        "flag_byte": None,
        "id": 0xC64909,
        "room": [],
    },
    LocationName.gasha_nut_11: {
        "region_id": "gasha tree 11",
        "vanilla_item": "Filler Item",
        "conditional": True,
        "flag_byte": None,
        "id": 0xC6490A,
        "room": [],
    },
    LocationName.gasha_nut_12: {
        "region_id": "gasha tree 12",
        "vanilla_item": "Filler Item",
        "conditional": True,
        "flag_byte": None,
        "id": 0xC6490B,
        "room": [],
    },
    LocationName.gasha_nut_13: {
        "region_id": "gasha tree 13",
        "vanilla_item": "Filler Item",
        "conditional": True,
        "flag_byte": None,
        "id": 0xC6490C,
        "room": [],
    },
    LocationName.gasha_nut_14: {
        "region_id": "gasha tree 14",
        "vanilla_item": "Filler Item",
        "conditional": True,
        "flag_byte": None,
        "id": 0xC6490D,
        "room": [],
    },
    LocationName.gasha_nut_15: {
        "region_id": "gasha tree 15",
        "vanilla_item": "Filler Item",
        "conditional": True,
        "flag_byte": None,
        "id": 0xC6490E,
        "room": [],
    },
    LocationName.gasha_nut_16: {
        "region_id": "gasha tree 16",
        "vanilla_item": "Filler Item",
        "conditional": True,
        "flag_byte": None,
        "id": 0xC6490F,
        "room": [],
    },
    LocationName.spool_swamp_business_scrub: {
        "region_id": "spool swamp scrub",
        "vanilla_item": "Filler Item",
        "conditional": True,
        "flag_byte": 0xC63F,
        "bit_mask": 0x04,
        "scouting_byte": 0xC780,
        "room": 0x0080,
        "collect": COLLECT_TOUCH,
        "map_tile": 0x80,
        "symbolic_name": "spoolSwampScrub",
    },
    LocationName.samasa_desert_business_scrub: {
        "region_id": "samasa desert scrub",
        "vanilla_item": "Filler Item",
        "conditional": True,
        "flag_byte": 0xC63F,
        "bit_mask": 0x10,
        "scouting_byte": 0xCAD1,
        "room": 0x05D1,
        "collect": COLLECT_TOUCH,
        "map_tile": 0xBF,
        "symbolic_name": "samasaCaveScrub",
    },
    LocationName.snakes_remains_business_scrub: {
        "region_id": "d2 scrub",
        "vanilla_item": "Filler Item",
        "conditional": True,
        "dungeon": 2,
        "flag_byte": 0xC642,
        "bit_mask": 0x20,
        "scouting_byte": 0xC933,
        "room": 0x0433,
        "collect": COLLECT_TOUCH,
        "map_tile": 0x8D,
        "symbolic_name": "d2Scrub",
    },
    LocationName.dancing_dragon_dungeon_1f_business_scrub: {
        "region_id": "d4 scrub",
        "vanilla_item": "Filler Item",
        "conditional": True,
        "dungeon": 4,
        "flag_byte": 0xC642,
        "bit_mask": 0x40,
        "scouting_byte": 0xC963,
        "room": 0x0463,
        "collect": COLLECT_D4_SCRUB_ROOM,
        "map_tile": 0x1D,
        "symbolic_name": "d4Scrub",
    },
    # Linked locations
    LocationName.horon_village_clock_shop_secret: {
        "region_id": "clock shop secret",
        "vanilla_item": "Filler Item",
        "conditional": True,
        "flag_byte": 0xC6D5,
        "bit_mask": 0x04,
        "room": 0x050F,
        "collect": COLLECT_TOUCH,
        "map_tile": 0xD7,
        "symbolic_name": "clockSecret",
    },
    LocationName.western_coast_graveyard_secret: {
        "region_id": "graveyard secret",
        "vanilla_item": "Filler Item",
        "conditional": True,
        "flag_byte": 0xC6D5,
        "bit_mask": 0x08,
        "room": 0x03BA,
        "collect": COLLECT_TOUCH,
        "map_tile": 0xE0,
        "symbolic_name": "graveyardSecret",
    },
    LocationName.subrosia_subrosian_secret: {
        "region_id": "subrosian secret",
        "vanilla_item": "Filler Item",
        "conditional": True,
        "flag_byte": 0xC6D5,
        "bit_mask": 0x10,
        "room": 0x04F0,
        "collect": COLLECT_TOUCH,
        "map_tile": 0x9A,
        "symbolic_name": "subrosianSecret",
    },
    LocationName.sunken_city_diver_secret: {
        "region_id": "diver secret",
        "vanilla_item": "Filler Item",
        "conditional": True,
        "flag_byte": 0xC6D5,
        "bit_mask": 0x20,
        "room": 0x03B6,
        "collect": COLLECT_TOUCH,
        "map_tile": 0x5D,
        "symbolic_name": "diverSecret",
    },
    LocationName.subrosia_smith_secret: {
        "region_id": "smith secret",
        "vanilla_item": "Filler Item",
        "conditional": True,
        "flag_byte": 0xC6D5,
        "bit_mask": 0x40,
        "room": 0x0397,
        "collect": COLLECT_TOUCH,
        "map_tile": 0x1E,
        "symbolic_name": "smithSecret",
    },
    LocationName.subrosia_piratian_secret: {
        "region_id": "pirates after bell",
        "vanilla_item": "Filler Item",
        "conditional": True,
        "flag_byte": 0xC6D5,
        "bit_mask": 0x80,
        "room": 0x038B,
        "collect": COLLECT_TOUCH,
        "map_tile": 0xF7,
        "symbolic_name": "pirateSecret",
    },
    LocationName.subrosia_temple_secret: {
        "region_id": "temple of seasons",
        "vanilla_item": "Filler Item",
        "conditional": True,
        "flag_byte": 0xC6D6,
        "bit_mask": 0x01,
        "room": 0x03AD,
        "collect": COLLECT_TOUCH,
        "map_tile": 0xB0,
        "symbolic_name": "templeSecret",
    },
    LocationName.natzu_region_deku_secret: {
        "region_id": "deku secret",
        "vanilla_item": "Filler Item",
        "conditional": True,
        "flag_byte": 0xC6D6,
        "bit_mask": 0x02,
        "room": [0x050B, 0x050C, 0x050D],
        "collect": COLLECT_TOUCH,
        # "map_tile": ???,
        "symbolic_name": "dekuSecret",
    },
    LocationName.goron_mountain_biggoron_secret: {
        "region_id": "biggoron trade",
        "vanilla_item": "Filler Item",
        "conditional": True,
        "flag_byte": 0xC6D6,
        "bit_mask": 0x04,
        "room": 0x0008,
        "collect": COLLECT_TOUCH,
        "map_tile": 0x08,
        "symbolic_name": "biggoronSecret",
    },
    LocationName.horon_village_mayor_secret: {
        "region_id": "mayor's gift",
        "vanilla_item": "Filler Item",
        "conditional": True,
        "flag_byte": 0xC6D6,
        "bit_mask": 0x08,
        "room": 0x0385,
        "collect": COLLECT_TOUCH,
        "map_tile": 0xC8,
        "symbolic_name": "mayorSecret",
    },
    # Placeholder locations for the owls
    LocationName.dodongo_owl: {
        "region_id": "dodongo owl",
        "vanilla_item": "Hint",
        "conditional": True,
        "flag_byte": None,
        "owl_id": 0,
        "scouting_byte": 0xC928,
        "scouting_mask": 0x40,
        "room": 0x0428,
    },
    LocationName.gohma_owl: {
        "region_id": "gohma owl",
        "vanilla_item": "Hint",
        "conditional": True,
        "flag_byte": None,
        "owl_id": 1,
        "scouting_byte": 0xC961,
        "scouting_mask": 0x40,
        "room": 0x0461,
    },
    LocationName.armos_knights_owl: {
        "region_id": "armos knights owl",
        "vanilla_item": "Hint",
        "conditional": True,
        "flag_byte": None,
        "owl_id": 2,
        "scouting_byte": 0xC992,
        "scouting_mask": 0x40,
        "room": 0x0492,
    },
    LocationName.silent_watch_owl: {
        "region_id": "silent watch owl",
        "vanilla_item": "Hint",
        "conditional": True,
        "flag_byte": None,
        "owl_id": 3,
        "scouting_byte": 0xCA73,
        "scouting_mask": 0x40,
        "room": 0x0573,
    },
    LocationName.magical_ice_owl: {
        "region_id": "magical ice owl",
        "vanilla_item": "Hint",
        "conditional": True,
        "flag_byte": None,
        "owl_id": 4,
        "scouting_byte": 0xCA84,
        "scouting_mask": 0x40,
        "room": 0x0584,
    },
    LocationName.mystery_owl: {
        "region_id": "mystery owl",
        "vanilla_item": "Hint",
        "conditional": True,
        "flag_byte": None,
        "owl_id": 5,
        "scouting_byte": 0xC79E,
        "scouting_mask": 0x40,
        "room": 0x009E,
    },
    LocationName.omuai_owl: {
        "region_id": "omuai owl",
        "vanilla_item": "Hint",
        "conditional": True,
        "flag_byte": None,
        "owl_id": 6,
        "scouting_byte": 0xC949,
        "scouting_mask": 0x40,
        "room": 0x0449,
    },
    LocationName.poe_curse_owl: {
        "region_id": "poe curse owl",
        "vanilla_item": "Hint",
        "conditional": True,
        "flag_byte": None,
        "owl_id": 7,
        "scouting_byte": 0xCA59,
        "scouting_mask": 0x40,
        "room": 0x0559,
    },
    LocationName.spiked_beetles_owl: {
        "region_id": "spiked beetles owl",
        "vanilla_item": "Hint",
        "conditional": True,
        "flag_byte": None,
        "owl_id": 8,
        "scouting_byte": 0xC946,
        "scouting_mask": 0x40,
        "room": 0x0446,
    },
    LocationName.trampoline_owl: {
        "region_id": "trampoline owl",
        "vanilla_item": "Hint",
        "conditional": True,
        "flag_byte": None,
        "owl_id": 9,
        "scouting_byte": 0xC93E,
        "scouting_mask": 0x40,
        "room": 0x043E,
    },
    LocationName.greater_distance_owl: {
        "region_id": "greater distance owl",
        "vanilla_item": "Hint",
        "conditional": True,
        "flag_byte": None,
        "owl_id": 10,
        "scouting_byte": 0xC978,
        "scouting_mask": 0x40,
        "room": 0x0478,
    },
    LocationName.frypolar_owl: {
        "region_id": "frypolar owl",
        "vanilla_item": "Hint",
        "conditional": True,
        "flag_byte": None,
        "owl_id": 11,
        "scouting_byte": 0xCA71,
        "scouting_mask": 0x40,
        "room": 0x0571,
    },
    LocationName.shining_blue_owl: {
        "region_id": "shining blue owl",
        "vanilla_item": "Hint",
        "conditional": True,
        "flag_byte": None,
        "owl_id": 12,
        "scouting_byte": 0xCA57,
        "scouting_mask": 0x40,
        "room": 0x0557,
    },
    LocationName.floodgate_owl: {
        "region_id": "floodgate owl",
        "vanilla_item": "Hint",
        "conditional": True,
        "flag_byte": None,
        "owl_id": 13,
        "scouting_byte": 0xC9E7,
        "scouting_mask": 0x40,
        "room": 0x04E7,
    },
    # d11 locations
    LocationName.linked_heros_cave_alternate_entrance_chest: {
        "region_id": "d11 alt entrance",
        "vanilla_item": "Rupees (20)",
        "conditional": True,
        "dungeon": 11,
        "room": 0x052C,
        "collect": COLLECT_CHEST,
    },
    LocationName.linked_heros_cave_first_reward: {
        "region_id": "d11 floor 1 chest",
        "vanilla_item": "Gasha Seed",
        "conditional": True,
        "dungeon": 11,
        "room": 0x0531,
        "collect": COLLECT_CHEST,
    },
    LocationName.linked_heros_cave_checkerboard_drop: {
        "region_id": "d11 floor 2 keydrop",
        "vanilla_item": "Small Key (Linked Hero's Cave)",
        "conditional": True,
        "dungeon": 11,
        "room": 0x0532,
        "collect": COLLECT_DROP,
        "symbolic_name": "d11CheckerboardDrop",
    },
    LocationName.linked_heros_cave_second_reward: {
        "region_id": "d11 floor 2 chest",
        "vanilla_item": "Gasha Seed",
        "conditional": True,
        "dungeon": 11,
        "room": 0x052F,
        "collect": COLLECT_CHEST,
    },
    LocationName.linked_heros_cave_torch_chest: {
        "region_id": "d11 floor 3 torch keydrop",
        "vanilla_item": "Small Key (Linked Hero's Cave)",
        "conditional": True,
        "dungeon": 11,
        "room": 0x0529,
        "collect": COLLECT_CHEST,
    },
    LocationName.linked_heros_cave_flooded_room_drop: {
        "region_id": "d11 floor 3 flooded keydrop",
        "vanilla_item": "Small Key (Linked Hero's Cave)",
        "conditional": True,
        "dungeon": 11,
        "room": 0x052A,
        "collect": COLLECT_DROP,
        "symbolic_name": "d11FloodedDrop",
    },
    LocationName.linked_heros_cave_third_reward: {
        "region_id": "d11 floor 3 chest",
        "vanilla_item": "Gasha Seed",
        "conditional": True,
        "dungeon": 11,
        "room": 0x0528,
        "collect": COLLECT_CHEST,
    },
    LocationName.linked_heros_cave_fourth_reward: {
        "region_id": "d11 floor 4 chest",
        "vanilla_item": "Gasha Seed",
        "conditional": True,
        "dungeon": 11,
        "room": 0x0524,
        "collect": COLLECT_CHEST,
    },
    LocationName.linked_heros_cave_gauntlet: {
        "region_id": "d11 floor 5 gauntlet",
        "vanilla_item": "Small Key (Linked Hero's Cave)",
        "conditional": True,
        "dungeon": 11,
        "room": 0x0522,
        "collect": COLLECT_DROP,
        "symbolic_name": "d11GauntletDrop",
    },
    LocationName.linked_heros_cave_boomerang_maze: {
        "region_id": "d11 floor 5 boomerang maze",
        "vanilla_item": "Small Key (Linked Hero's Cave)",
        "conditional": True,
        "dungeon": 11,
        "room": 0x0523,
        "collect": COLLECT_DROP,
        "symbolic_name": "d11BoomerangDrop",
    },
    LocationName.linked_heros_cave_final_reward: {
        "region_id": "d11 final chest",
        "vanilla_item": "Power Ring L-3",
        "conditional": True,
        "dungeon": 11,
        "room": 0x0534,
        "collect": COLLECT_CHEST,
    },
    # Maple locations, disabled for now
    LocationName.maple_rare_drop_1: {  # There are technically 2 of them but this is not visible, and we only have room for 4 items
        "region_id": "maple rare item 1",
        "vanilla_item": "Random Ring",
        "conditional": True,
        "flag_byte": 0xC641,
        "bit_mask": 0x20,
        "symbolic_name": "mapleItem1",
        "repeatable": True,
    },
    LocationName.maple_rare_drop_2: {
        "region_id": "maple rare item 2",
        "vanilla_item": "Potion",
        "conditional": True,
        "flag_byte": 0xC641,
        "bit_mask": 0x10,
        "symbolic_name": "mapleItem2",
        "repeatable": True,
    },
    LocationName.maple_rare_drop_3: {
        "region_id": "maple rare item 3",
        "vanilla_item": "Gasha Seed",
        "conditional": True,
        "flag_byte": 0xC641,
        "bit_mask": 0x40,
        "symbolic_name": "mapleItem3",
        "repeatable": True,
    },
    LocationName.maple_rare_drop_4: {
        "region_id": "maple rare item 4",
        "vanilla_item": "Piece of Heart",
        "conditional": True,
        "flag_byte": 0xC641,
        "bit_mask": 0x80,
        "symbolic_name": "mapleItem4",
        "repeatable": True,
    },
}

for location in LOCATIONS_DATA.values():
    if "flag_byte" not in location:
        room = location["room"]
        if room >= 0x200:
            if room >= 0x300:
                if room >= 0x600:
                    room -= 0x200
                room -= 0x100
            room -= 0x100
        location["flag_byte"] = 0xC700 + room
