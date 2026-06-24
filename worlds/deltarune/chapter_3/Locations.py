from BaseClasses import LocationProgressType
from typing import TYPE_CHECKING

from worlds.deltarune.Locations import LocationData, LocationGroups, LocationIDs
from worlds.deltarune.Regions import Regions

if TYPE_CHECKING:
    from .. import DeltaruneWorld

chapter3_locations = {
    Regions.ch3_couch_cliffs: [
        LocationData(
            LocationIDs.ch3_couch_cliffs_dust_pile_chest,
            group=LocationGroups.chapter3,
        ),
        LocationData(LocationIDs.ch3_couch_cliffs_warp_door, group=LocationGroups.chapter3),
    ],
    Regions.ch3_board_1: [
        LocationData(LocationIDs.ch3_board_1_z_rank, group=LocationGroups.chapter3),
        LocationData(LocationIDs.ch3_board_1_c_rank, group=LocationGroups.chapter3),
        LocationData(LocationIDs.ch3_board_1_b_rank, group=LocationGroups.chapter3),
        LocationData(LocationIDs.ch3_board_1_a_rank, group=LocationGroups.chapter3),
        LocationData(LocationIDs.ch3_board_1_s_rank, group=LocationGroups.chapter3),
        LocationData(LocationIDs.ch3_board_1_t_rank, group=LocationGroups.chapter3),
        LocationData(LocationIDs.ch3_board_1_extra_key, group=LocationGroups.chapter3),
        LocationData(LocationIDs.ch3_board_1_extra_extra_key, group=LocationGroups.chapter3),
        LocationData(
            LocationIDs.ch3_green_room_board_1_ramb_gift,
            group=LocationGroups.chapter3,
        ),
        LocationData(
            LocationIDs.ch3_lost_shadowguy,
            should_be_included=lambda world: world.is_weird_route(),
            group=LocationGroups.chapter3,
        ),
    ],
    Regions.ch3_sword_1: [
        LocationData(LocationIDs.ch3_mantle_out_of_bounds_chest, group=LocationGroups.chapter3),
    ],
    Regions.ch3_green_room: [
        LocationData(
            LocationIDs.ch3_green_room_vending_machine_1,
            group=LocationGroups.chapter3,
        ),
        LocationData(
            LocationIDs.ch3_green_room_vending_machine_2,
            group=LocationGroups.chapter3,
        ),
        LocationData(
            LocationIDs.ch3_green_room_vending_machine_3,
            group=LocationGroups.chapter3,
        ),
        LocationData(
            LocationIDs.ch3_green_room_vending_machine_4,
            group=LocationGroups.chapter3,
        ),
        LocationData(
            LocationIDs.ch3_green_room_vending_machine_5,
            group=LocationGroups.chapter3,
        ),
        LocationData(
            LocationIDs.ch3_green_room_vending_machine_6,
            group=LocationGroups.chapter3,
        ),
        LocationData(
            LocationIDs.ch3_green_room_vending_machine_7,
            group=LocationGroups.chapter3,
        ),
        LocationData(
            LocationIDs.ch3_green_room_vending_machine_8,
            group=LocationGroups.chapter3,
        ),
        LocationData(
            LocationIDs.ch3_b_rank_room_golden_prize_1,
            group=LocationGroups.chapter3,
        ),
        LocationData(
            LocationIDs.ch3_b_rank_room_golden_prize_2,
            group=LocationGroups.chapter3,
        ),
        LocationData(
            LocationIDs.ch3_b_rank_room_golden_prize_3,
            group=LocationGroups.chapter3,
        ),
        LocationData(
            LocationIDs.ch3_b_rank_room_golden_prize_4,
            group=LocationGroups.chapter3,
        ),
        LocationData(
            LocationIDs.ch3_b_rank_room_golden_prize_5,
            group=LocationGroups.chapter3,
        ),
        LocationData(
            LocationIDs.ch3_s_rank_room_person_behind_curtain,
            group=LocationGroups.chapter3,
        ),
        LocationData(
            LocationIDs.ch3_s_rank_room_vending_machine_1,
            group=LocationGroups.chapter3,
        ),
        LocationData(
            LocationIDs.ch3_s_rank_room_vending_machine_2,
            group=LocationGroups.chapter3,
        ),
        LocationData(
            LocationIDs.ch3_s_rank_room_vending_machine_3,
            group=LocationGroups.chapter3,
        ),
        LocationData(
            LocationIDs.ch3_s_rank_room_vending_machine_4,
            group=LocationGroups.chapter3,
        ),
        LocationData(LocationIDs.ch3_s_rank_room_oddcontroller, group=LocationGroups.chapter3),
        LocationData(LocationIDs.ch3_green_room_warp_door, group=LocationGroups.chapter3),
        LocationData(
            LocationIDs.ch3_recruit_water_cooler,
            should_be_included=lambda world: world.is_all_recruits(),
            group=LocationGroups.chapter3,
        ),
        LocationData(
            LocationIDs.ch3_lost_water_cooler,
            should_be_included=lambda world: world.is_weird_route(),
            group=LocationGroups.chapter3,
        ),
    ],
    Regions.ch3_board_2: [
        LocationData(LocationIDs.ch3_board_2_z_rank, group=LocationGroups.chapter3),
        LocationData(LocationIDs.ch3_board_2_c_rank, group=LocationGroups.chapter3),
        LocationData(LocationIDs.ch3_board_2_b_rank, group=LocationGroups.chapter3),
        LocationData(LocationIDs.ch3_board_2_a_rank, group=LocationGroups.chapter3),
        LocationData(LocationIDs.ch3_board_2_s_rank, group=LocationGroups.chapter3),
        LocationData(LocationIDs.ch3_board_2_t_rank, group=LocationGroups.chapter3),
        LocationData(LocationIDs.ch3_board_2_extra_photo, group=LocationGroups.chapter3),
        LocationData(LocationIDs.ch3_board_2_moss, group=LocationGroups.chapter3),
        LocationData(LocationIDs.ch3_green_room_board_2_ramb_gift, group=LocationGroups.chapter3),
        LocationData(
            LocationIDs.ch3_recruit_pippins,
            should_be_included=lambda world: world.is_all_recruits(),
            group=LocationGroups.chapter3,
        ),
        LocationData(
            LocationIDs.ch3_lost_pippins,
            should_be_included=lambda world: world.is_weird_route(),
            group=LocationGroups.chapter3,
        ),
        LocationData(
            LocationIDs.ch3_lost_shuttah,
            should_be_included=lambda world: world.is_weird_route(),
            group=LocationGroups.chapter3,
        ),
    ],
    Regions.ch3_sword_2: [
        LocationData(LocationIDs.ch3_mantle_northern_light_item, group=LocationGroups.chapter3),
    ],
    Regions.ch3_doom_board: [
        LocationData(
            LocationIDs.ch3_lost_zapper,
            should_be_included=lambda world: world.is_weird_route(),
            group=LocationGroups.chapter3,
        ),
        LocationData(
            LocationIDs.ch3_tv_world_entrance_warp_door,
            group=LocationGroups.chapter3,
        ),
    ],
    Regions.ch3_tv_world: [
        LocationData(
            LocationIDs.ch3_tv_world_chest_near_shadowmen,
            group=LocationGroups.chapter3,
        ),
        LocationData(
            LocationIDs.ch3_tv_world_board_puzzle_1_chest,
            group=LocationGroups.chapter3,
        ),
        LocationData(
            LocationIDs.ch3_tv_world_goulden_sam_warp_door,
            group=LocationGroups.chapter3,
        ),
        LocationData(LocationIDs.ch3_tv_world_trash_can_1, group=LocationGroups.chapter3),
        LocationData(LocationIDs.ch3_tv_world_trash_can_2, group=LocationGroups.chapter3),
        LocationData(LocationIDs.ch3_tv_world_trash_can_3, group=LocationGroups.chapter3),
        LocationData(LocationIDs.ch3_tv_world_trash_can_4, group=LocationGroups.chapter3),
        LocationData(LocationIDs.ch3_tv_world_trash_can_5, group=LocationGroups.chapter3),
        LocationData(
            LocationIDs.ch3_tv_world_board_puzzle_2_chest,
            group=LocationGroups.chapter3,
        ),
        LocationData(
            LocationIDs.ch3_tv_world_serious_trashy_chest,
            group=LocationGroups.chapter3,
        ),
        LocationData(LocationIDs.ch3_tv_world_bonus_zone_chest_1, group=LocationGroups.chapter3),
        LocationData(LocationIDs.ch3_tv_world_bonus_zone_chest_2, group=LocationGroups.chapter3),
        LocationData(LocationIDs.ch3_tv_world_bonus_zone_chest_3, group=LocationGroups.chapter3),
        LocationData(
            LocationIDs.ch3_tv_world_chest_outside_green_room,
            group=LocationGroups.chapter3,
        ),
        LocationData(LocationIDs.ch3_tv_world_water_cooler_chest, group=LocationGroups.chapter3),
        LocationData(
            LocationIDs.ch3_tv_world_man,
            should_be_included=lambda world: world.is_not_weird_route_only(),
            group=LocationGroups.chapter3,
        ),
        LocationData(
            LocationIDs.ch3_tv_world_tripticket,
            should_be_included=lambda world: world.is_not_weird_route_only(),
            group=LocationGroups.chapter3,
        ),
        LocationData(
            LocationIDs.ch3_recruit_shuttah,
            should_be_included=lambda world: world.is_all_recruits(),
            group=LocationGroups.chapter3,
        ),
        LocationData(
            LocationIDs.ch3_recruit_shadowguy,
            should_be_included=lambda world: world.is_all_recruits(),
            group=LocationGroups.chapter3,
        ),
        LocationData(
            LocationIDs.ch3_recruit_zapper,
            should_be_included=lambda world: world.is_all_recruits(),
            group=LocationGroups.chapter3,
        ),
        LocationData(
            LocationIDs.ch3_recruit_ribbick,
            should_be_included=lambda world: world.is_all_recruits(),
            group=LocationGroups.chapter3,
        ),
        LocationData(
            LocationIDs.ch3_recruit_lanino,
            should_be_included=lambda world: world.is_all_recruits(),
            group=LocationGroups.chapter3,
        ),
        LocationData(
            LocationIDs.ch3_recruit_elnina,
            should_be_included=lambda world: world.is_all_recruits(),
            group=LocationGroups.chapter3,
        ),
        LocationData(
            LocationIDs.ch3_lost_ribbick,
            should_be_included=lambda world: world.is_weird_route(),
            group=LocationGroups.chapter3,
        ),
    ],
    Regions.ch3_sword_3: [
        LocationData(
            LocationIDs.ch3_mantle_defeat,
            should_be_included=lambda world: not world.is_mantleless(),
            group=LocationGroups.chapter3,
        ),
        LocationData(
            LocationIDs.ch3_mantle_susie_gift,
            should_be_included=lambda world: not world.is_mantleless(),
            group=LocationGroups.chapter3,
        ),
    ],
    Regions.ch3_cold_place: [
        LocationData(
            LocationIDs.ch3_cold_place_knight_defeat_item_1,
            group=LocationGroups.chapter3,
        ),
        LocationData(
            LocationIDs.ch3_cold_place_knight_defeat_item_2,
            group=LocationGroups.chapter3,
        ),
        LocationData(LocationIDs.ch3_fountain_sealed, group=LocationGroups.chapter3),
    ],
}
