from worlds.deltarune.Locations import LocationData, LocationGroups, LocationIDs
from worlds.deltarune.Regions import Regions
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .. import DeltaruneWorld

chapter2_locations = {
    Regions.ch2_castle_town: [
        LocationData(
            LocationIDs.ch2_castle_town_top_chef_gift,
            group=LocationGroups.chapter2,
        ),
    ],
    Regions.ch2_dojo: [
        LocationData(
            LocationIDs.ch2_castle_town_jigsaw_joe_challenge,
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_castle_town_graze_challenge_1,
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_castle_town_clover_rematch_challenge,
            group=LocationGroups.chapter2,
        ),
    ],
    Regions.ch2_cyber_field: [
        LocationData(
            LocationIDs.ch2_cyber_field_first_chest,
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_cyber_field_nubert_chest,
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_cyber_field_tasque_maze_checkmark,
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_cyber_field_teacup_ride_checkmark,
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_cyber_field_giasfelfebrehber_checkmark,
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_cyber_field_warp_door,
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_recruit_werewire,
            should_be_included=lambda world: world.is_all_recruits(),
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_recruit_tasque,
            should_be_included=lambda world: world.is_all_recruits(),
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_recruit_virovirokun,
            should_be_included=lambda world: world.is_all_recruits(),
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_lost_werewire,
            should_be_included=lambda world: world.is_weird_route(),
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_lost_tasque,
            should_be_included=lambda world: world.is_weird_route(),
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_lost_virovirokun,
            should_be_included=lambda world: world.is_weird_route(),
            group=LocationGroups.chapter2,
        ),
    ],
    Regions.ch2_cyber_field_post_dj: [
        LocationData(
            LocationIDs.ch2_cyber_field_fun_gang_actions_unlock,
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_cyber_field_chest_near_music_shop,
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_cyber_field_virovirokun_puzzle_chest,
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_cyber_field_teacup_puzzle_chest,
            group=LocationGroups.chapter2,
        ),
    ],
    Regions.ch2_music_shop: [
        LocationData(
            LocationIDs.ch2_music_shop_1,
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_music_shop_2,
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_music_shop_3,
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_music_shop_4,
            group=LocationGroups.chapter2,
        ),
    ],
    Regions.ch2_trash_zone: [
        LocationData(
            LocationIDs.ch2_trash_zone_warp_door,
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_trash_zone_trash_can,
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_cyber_city_trash_can_2,
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_recruit_poppup,
            should_be_included=lambda world: world.is_all_recruits(),
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_lost_poppup,
            should_be_included=lambda world: world.is_weird_route(),
            group=LocationGroups.chapter2,
        ),
    ],
    Regions.ch2_spamton_shop: [
        LocationData(
            LocationIDs.ch2_spamton_shop_1,
            should_be_included=lambda world: world.is_not_weird_route_only(),
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_spamton_shop_2,
            should_be_included=lambda world: world.is_not_weird_route_only(),
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_spamton_shop_3,
            should_be_included=lambda world: world.is_not_weird_route_only(),
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_spamton_shop_4,
            should_be_included=lambda world: world.is_not_weird_route_only(),
            group=LocationGroups.chapter2,
        ),
    ],
    Regions.ch2_cyber_city: [
        LocationData(
            LocationIDs.ch2_cyber_city_trash_can_1,
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_cyber_city_queen_poster_chest,
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_cyber_city_chest_guarded_by_virovirokun,
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_cyber_city_cheese_maze_chest,
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_cyber_city_trash_can_3,
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_cyber_city_trash_can_4,
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_cyber_city_trash_can_5,
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_cyber_city_purchase_mannequin,
            should_be_included=lambda world: world.is_not_weird_route_only(),
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_cyber_city_annoying_dog,
            should_be_included=lambda world: world.is_not_weird_route_only(),
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_cyber_city_man,
            should_be_included=lambda world: world.is_not_weird_route_only(),
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_cyber_city_moss,
            should_be_included=lambda world: world.is_not_weird_route_only(),
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_cyber_city_purchase_kris_tea,
            should_be_included=lambda world: world.is_not_weird_route_only(),
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_cyber_city_purchase_noelle_tea,
            should_be_included=lambda world: world.is_not_weird_route_only(),
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_cyber_city_purchase_susie_tea,
            should_be_included=lambda world: world.is_not_weird_route_only(),
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_cyber_city_purchase_ralsei_tea,
            should_be_included=lambda world: world.is_not_weird_route_only(),
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_recruit_ambyu_lance,
            should_be_included=lambda world: world.is_all_recruits(),
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_recruit_maus,
            should_be_included=lambda world: world.is_all_recruits(),
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_lost_ambyu_lance,
            should_be_included=lambda world: world.is_weird_route(),
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_lost_maus,
            should_be_included=lambda world: world.is_weird_route(),
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_cyber_city_purchase_freezering,
            should_be_included=lambda world: world.is_weird_route(),
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_cyber_city_purchase_thornring,
            should_be_included=lambda world: world.is_weird_route(),
            group=LocationGroups.chapter2,
        ),
    ],
    Regions.ch2_mansion_lobby: [
        LocationData(
            LocationIDs.ch2_mansion_warp_door,
            group=LocationGroups.chapter2,
        ),
    ],
    Regions.ch2_swatch_cafe: [
        LocationData(
            LocationIDs.ch2_swatchs_cafe_1,
            should_be_included=lambda world: world.is_not_weird_route_only(),
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_swatchs_cafe_2,
            should_be_included=lambda world: world.is_not_weird_route_only(),
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_swatchs_cafe_3,
            should_be_included=lambda world: world.is_not_weird_route_only(),
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_swatchs_cafe_4,
            should_be_included=lambda world: world.is_not_weird_route_only(),
            group=LocationGroups.chapter2,
        ),
    ],
    Regions.ch2_mansion: [
        LocationData(
            LocationIDs.ch2_mansion_painting_chest,
            should_be_included=lambda world: world.is_not_weird_route_only(),
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_mansion_sculpture_room_chest,
            should_be_included=lambda world: world.is_not_weird_route_only(),
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_mansion_platter_chest,
            should_be_included=lambda world: world.is_not_weird_route_only(),
            group=LocationGroups.chapter2,
        ),
    ],
    Regions.ch2_mansion_basement: [
        LocationData(
            LocationIDs.ch2_mansion_basement_chest,
            should_be_included=lambda world: world.is_not_weird_route_only(),
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_mansion_basement_mechanism,
            should_be_included=lambda world: world.is_not_weird_route_only(),
            group=LocationGroups.chapter2,
        ),
    ],
    Regions.ch2_tunnel_of_love: [
        LocationData(
            LocationIDs.ch2_mansion_tunnel_of_love_chest,
            should_be_included=lambda world: world.is_not_weird_route_only(),
            group=LocationGroups.chapter2,
        ),
    ],
    Regions.ch2_werewerewire: [
        LocationData(
            LocationIDs.ch2_recruit_werewerewire,
            should_be_included=lambda world: world.is_all_recruits(),
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_lost_werewerewire,
            should_be_included=lambda world: world.is_weird_route(),
            group=LocationGroups.chapter2,
        ),
    ],
    Regions.ch2_mansion_recruits: [
        LocationData(
            LocationIDs.ch2_recruit_swatchling,
            should_be_included=lambda world: world.is_all_recruits(),
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_recruit_tasque_manager,
            should_be_included=lambda world: world.is_all_recruits(),
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_recruit_mauswheel,
            should_be_included=lambda world: world.is_all_recruits(),
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_lost_swatchlings,
            should_be_included=lambda world: world.is_weird_route()
            and world.options.include_lose_swatchling.value == 1,
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_lost_tasque_manager,
            should_be_included=lambda world: world.is_weird_route(),
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_lost_mauswheel,
            should_be_included=lambda world: world.is_weird_route(),
            group=LocationGroups.chapter2,
        ),
    ],
    Regions.ch2_spamton_neo: [
        LocationData(
            LocationIDs.ch2_mansion_spamton_neo_defeat_item_1,
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_mansion_spamton_neo_defeat_item_2,
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_mansion_spamton_neo_defeat_item_3,
            should_be_included=lambda world: world.is_not_weird_route_only(),
            group=LocationGroups.chapter2,
        ),
    ],
    Regions.ch2_post_chapter_castle_town: [
        LocationData(
            LocationIDs.ch2_fountain_sealed,
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_castle_town_tasque_manager_says_challenge,
            should_be_included=lambda world: world.is_all_recruits(),
            group=LocationGroups.chapter2,
        ),
        LocationData(
            LocationIDs.ch2_castle_town_all_stars_challenge,
            should_be_included=lambda world: world.is_all_recruits(),
            group=LocationGroups.chapter2,
        ),
    ],
}
