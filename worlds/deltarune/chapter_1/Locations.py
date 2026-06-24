from enum import StrEnum

from worlds.deltarune.Locations import LocationData, LocationData, LocationGroups, LocationIDs
from worlds.deltarune.Regions import Regions

chapter1_locations = {
    Regions.ch1_unknown: [
        LocationData(
            LocationIDs.ch1_unknown_hidden_item,
            group=LocationGroups.chapter1,
        ),
    ],
    Regions.ch1_castle_town: [
        LocationData(LocationIDs.ch1_castle_town_manual, group=LocationGroups.chapter1),
        LocationData(LocationIDs.ch1_throw_away_manual, group=LocationGroups.chapter1),
        LocationData(
            LocationIDs.ch1_throw_away_manual_again,
            group=LocationGroups.chapter1,
        ),
    ],
    Regions.ch1_fields: [
        LocationData(LocationIDs.ch1_field_dark_candy_tree_1, group=LocationGroups.chapter1),
        LocationData(LocationIDs.ch1_field_dark_candy_tree_2, group=LocationGroups.chapter1),
        LocationData(LocationIDs.ch1_field_dark_candy_tree_3, group=LocationGroups.chapter1),
        LocationData(LocationIDs.ch1_field_dark_candy_tree_4, group=LocationGroups.chapter1),
        LocationData(LocationIDs.ch1_field_brokencake, group=LocationGroups.chapter1),
        LocationData(LocationIDs.ch1_field_return_top_cake, group=LocationGroups.chapter1),
        LocationData(
            LocationIDs.ch1_field_maze_of_death_chest,
            group=LocationGroups.chapter1,
        ),
    ],
    Regions.ch1_fields_post_hathy: [
        LocationData(
            LocationIDs.ch1_field_chest_before_great_board,
            group=LocationGroups.chapter1,
        ),
        LocationData(
            LocationIDs.ch1_field_warp_door,
            group=LocationGroups.chapter1,
        ),
        LocationData(
            LocationIDs.ch1_recruit_rudinn,
            should_be_included=lambda world: world.is_chapter_1_recruit_system_enabled() and world.is_all_recruits(),
            group=LocationGroups.chapter1,
        ),
        LocationData(
            LocationIDs.ch1_recruit_hathy,
            should_be_included=lambda world: world.is_chapter_1_recruit_system_enabled() and world.is_all_recruits(),
            group=LocationGroups.chapter1,
        ),
        LocationData(
            LocationIDs.ch1_recruit_jigsawry,
            should_be_included=lambda world: world.is_chapter_1_recruit_system_enabled() and world.is_all_recruits(),
            group=LocationGroups.chapter1,
        ),
        LocationData(
            LocationIDs.ch1_lost_rudinn,
            should_be_included=lambda world: world.is_chapter_1_recruit_system_enabled() and world.is_weird_route(),
            group=LocationGroups.chapter1,
        ),
        LocationData(
            LocationIDs.ch1_lost_hathy,
            should_be_included=lambda world: world.is_chapter_1_recruit_system_enabled() and world.is_weird_route(),
            group=LocationGroups.chapter1,
        ),
        LocationData(
            LocationIDs.ch1_lost_jigsawry,
            should_be_included=lambda world: world.is_chapter_1_recruit_system_enabled() and world.is_weird_route(),
            group=LocationGroups.chapter1,
        ),
    ],
    Regions.ch1_seam_seap: [
        LocationData(LocationIDs.ch1_seam_seap_1, group=LocationGroups.chapter1),
        LocationData(LocationIDs.ch1_seam_seap_2, group=LocationGroups.chapter1),
        LocationData(LocationIDs.ch1_seam_seap_3, group=LocationGroups.chapter1),
        LocationData(LocationIDs.ch1_seam_seap_4, group=LocationGroups.chapter1),
        LocationData(
            LocationIDs.ch1_seam_seap_talk_about_strange_prisoner,
            group=LocationGroups.chapter1,
        ),
    ],
    Regions.ch1_great_board: [
        LocationData(
            LocationIDs.ch1_recruit_ponman,
            should_be_included=lambda world: world.is_chapter_1_recruit_system_enabled() and world.is_all_recruits(),
            group=LocationGroups.chapter1,
        ),
        LocationData(
            LocationIDs.ch1_lost_ponman,
            should_be_included=lambda world: world.is_chapter_1_recruit_system_enabled() and world.is_weird_route(),
            group=LocationGroups.chapter1,
        ),
    ],
    Regions.ch1_forest: [
        LocationData(LocationIDs.ch1_forest_warp_door, group=LocationGroups.chapter1),
        LocationData(LocationIDs.ch1_forest_coat_rack_chest, group=LocationGroups.chapter1),
        LocationData(
            LocationIDs.ch1_forest_letter_block_chest,
            group=LocationGroups.chapter1,
        ),
        LocationData(
            LocationIDs.ch1_recruit_rabbick,
            should_be_included=lambda world: world.is_chapter_1_recruit_system_enabled() and world.is_all_recruits(),
            group=LocationGroups.chapter1,
        ),
        LocationData(
            LocationIDs.ch1_recruit_bloxer,
            should_be_included=lambda world: world.is_chapter_1_recruit_system_enabled() and world.is_all_recruits(),
            group=LocationGroups.chapter1,
        ),
        # lost Rabbick is in cross chapter
        LocationData(
            LocationIDs.ch1_lost_bloxer,
            should_be_included=lambda world: world.is_chapter_1_recruit_system_enabled() and world.is_weird_route(),
            group=LocationGroups.chapter1,
        ),
    ],
    Regions.ch1_bake_sale: [
        LocationData(LocationIDs.ch1_bake_sale_warp_door, group=LocationGroups.chapter1),
        LocationData(
            LocationIDs.ch1_bake_sale_repair_door_key,
            group=LocationGroups.chapter1,
        ),
        LocationData(
            LocationIDs.ch1_bake_sale_repair_top_cake,
            group=LocationGroups.chapter1,
        ),
        LocationData(
            LocationIDs.ch1_bake_sale_diamond_stand,
            group=LocationGroups.chapter1,
        ),
        LocationData(
            LocationIDs.ch1_bake_sale_heart_stand,
            group=LocationGroups.chapter1,
        ),
        LocationData(
            LocationIDs.ch1_bake_sale_spade_stand,
            group=LocationGroups.chapter1,
        ),
    ],
    Regions.ch1_forest_post_bake_sale: [
        LocationData(
            LocationIDs.ch1_forest_scissor_dancers_chest,
            group=LocationGroups.chapter1,
        ),
        LocationData(
            LocationIDs.ch1_forest_hidden_chest_near_dancers,
            group=LocationGroups.chapter1,
        ),
        LocationData(
            LocationIDs.ch1_forest_chest_near_worm,
            group=LocationGroups.chapter1,
        ),
        LocationData(LocationIDs.ch1_forest_man, group=LocationGroups.chapter1),
    ],
    Regions.ch1_card_castle: [
        LocationData(
            LocationIDs.ch1_card_castle_warp_door,
            group=LocationGroups.chapter1,
        ),
        LocationData(
            LocationIDs.ch1_card_castle_ironshackle,
            group=LocationGroups.chapter1,
        ),
        LocationData(LocationIDs.ch1_card_castle_moss, group=LocationGroups.chapter1),
        LocationData(
            LocationIDs.ch1_card_castle_rudinn_gift,
            group=LocationGroups.chapter1,
        ),
        LocationData(
            LocationIDs.ch1_card_castle_2f_chest,
            group=LocationGroups.chapter1,
        ),
        LocationData(
            LocationIDs.ch1_card_castle_4f_chest,
            group=LocationGroups.chapter1,
        ),
        LocationData(
            LocationIDs.ch1_recruit_rudinn_ranger,
            should_be_included=lambda world: world.is_chapter_1_recruit_system_enabled() and world.is_all_recruits(),
            group=LocationGroups.chapter1,
        ),
        LocationData(
            LocationIDs.ch1_recruit_head_hathy,
            should_be_included=lambda world: world.is_chapter_1_recruit_system_enabled() and world.is_all_recruits(),
            group=LocationGroups.chapter1,
        ),
        LocationData(
            LocationIDs.ch1_lost_rudinn_ranger,
            should_be_included=lambda world: world.is_chapter_1_recruit_system_enabled() and world.is_weird_route(),
            group=LocationGroups.chapter1,
        ),
        LocationData(
            LocationIDs.ch1_lost_head_hathy,
            should_be_included=lambda world: world.is_chapter_1_recruit_system_enabled() and world.is_weird_route(),
            group=LocationGroups.chapter1,
        ),
    ],
    Regions.ch1_rouxls: [
        LocationData(LocationIDs.ch1_rouxls_shop_1, group=LocationGroups.chapter1),
        LocationData(LocationIDs.ch1_rouxls_shop_2, group=LocationGroups.chapter1),
        LocationData(LocationIDs.ch1_rouxls_shop_3, group=LocationGroups.chapter1),
        LocationData(LocationIDs.ch1_rouxls_shop_4, group=LocationGroups.chapter1),
    ],
    Regions.ch1_jevil: [
        LocationData(
            LocationIDs.ch1_card_castle_jevil_1,
            group=LocationGroups.chapter1,
        ),
        LocationData(
            LocationIDs.ch1_card_castle_jevil_2,
            group=LocationGroups.chapter1,
        ),
        LocationData(
            LocationIDs.ch1_card_castle_jevil_3,
            group=LocationGroups.chapter1,
        ),
    ],
    Regions.ch1_light_world: [LocationData(LocationIDs.ch1_fountain_sealed, group=LocationGroups.chapter1)],
}
