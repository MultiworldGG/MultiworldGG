from enum import StrEnum

from BaseClasses import Region
from typing import TYPE_CHECKING, Optional
from worlds.deltarune.Locations import DeltaruneLocation, LocationData, locations as all_locations

if TYPE_CHECKING:
    from . import DeltaruneWorld


class Regions(StrEnum):
    chapter_select = "Chapter Select"
    fusion = "Fusion"
    ch5_fusion = "Chapter 5+ Fusion"
    lost_rabbick = "Cross Chapter: Lost Rabbick"

    chapter_1 = "Chapter 1"
    ch1_unknown = "CH1: ??????"
    ch1_castle_town = "CH1: Castle Town"
    ch1_fields = "CH1: The Fields of Hopes and Dreams"
    ch1_fields_post_hathy = "CH1: The Fields of Hopes and Dreams (Post-Hathy)"
    ch1_seam_seap = "CH1: Seam's Seap"
    ch1_great_board = "CH1: Great Board"
    ch1_forest = "CH1: Scarlet Forest"
    ch1_bake_sale = "CH1: Bake Sale"
    ch1_forest_post_bake_sale = "CH1: Scarlet Forest (Post-Bake Sale)"
    ch1_card_castle = "CH1: Card Castle"
    ch1_rouxls = "CH1: Rouxls' shop"
    ch1_jevil = "CH1: Jevil"
    ch1_light_world = "CH1: Light World"

    chapter_2 = "Chapter 2"
    ch2_castle_town = "CH2: Castle Town"
    ch2_dojo = "CH2: Battle Dojo"
    ch2_cyber_field = "CH2: Cyber Field"
    ch2_cyber_field_post_dj = "CH2: Cyber Field (Post-DJ)"
    ch2_music_shop = "CH2: Music Shop"
    ch2_trash_zone = "CH2: Trash Zone"
    ch2_trash_zone_no_character_required = "CH2: Trash Zone (No Character required)"
    ch2_spamton_shop = "CH2: Spamton's Shop"
    ch2_cyber_city = "CH2: Cyber City"
    ch2_cyber_city_spamton_fight = "CH2: Cyber City (Spamton fight)"
    ch2_cyber_city_post_spamton = "CH2: Cyber City (Post-Spamton)"
    ch2_mansion_lobby_main_route = "CH2: Mansion Lobby Main Route"
    ch2_mansion_lobby_weird_route = "CH2: Mansion Lobby Weird Route"
    ch2_mansion_lobby_warp_door = "CH2: Mansion Lobby Warp Door"
    ch2_swatch_cafe = "CH2: Swatch's Cafe"
    ch2_mansion_main_route = "CH2: Mansion Main Route"
    ch2_mansion_both_route = "CH2: Mansion (Both Route)"
    ch2_mansion_basement = "CH2: Mansion Basement"
    ch2_tunnel_of_love = "CH2: Tunnel of Love"
    ch2_mansion_recruits = "CH2: Mansion Recruits"
    ch2_mansion_losts = "CH2: Mansion Losts"
    ch2_recruit_werewerewire = "CH2: Recruit Werewerewire"
    ch2_lose_werewerewire = "CH2: Lose Werewerewire"
    ch2_spamton_neo = "CH2: Spamton Neo"
    ch2_fountain = "CH2: Fountain"
    ch2_fountain_weird_route = "CH2: Fountain (Weird Route)"

    chapter_3 = "Chapter 3"
    ch3_couch_cliffs = "CH3: Couch Cliffs"
    ch3_board_1 = "CH3: Board 1"
    ch3_lost_shadowguy = "CH3: Lost Shadowguy"
    ch3_lost_pippins = "CH3: Lost Pippins"
    ch3_lost_shuttah = "CH3: Lost Shuttah"
    ch3_lost_water_cooler = "CH3: Lost Water Cooler"
    ch3_lost_zapper = "CH3: Lost Zapper"
    ch3_green_room = "CH3: Green Room"
    ch3_sword_1 = "CH3: Sword 1"
    ch3_board_2 = "CH3: Board 2"
    ch3_sword_2 = "CH3: Sword 2"
    ch3_doom_board = "CH3: Doom Board"
    ch3_tv_world = "CH3: TV World"
    ch3_sword_3 = "CH3: Sword 3"
    ch3_knight = "CH3: Roaring Knight Fight"
    ch3_cold_place = "CH3: Cold Place"
    ch3_fountain = "CH3: Fountain"

    chapter_4 = "Chapter 4"
    ch4_castle_town = "CH4: Castle Town"
    ch4_dojo = "CH4: Dojo"
    ch4_mike_room = "CH4: Mike Room"
    ch4_dark_sanctuary = "CH4: Dark Sanctuary"
    ch4_old_man_shop = "CH4: Old Man's Shop"
    ch4_dark_sanctuary_claimbclaws = "CH4: Dark Sanctuary (ClaimbClaws Required)"
    ch4_gerson = "CH4: Gerson"
    ch4_second_sanctuary = "CH4: Second Sanctuary"
    ch4_second_sanctuary_post_wicabel = "CH4: Second Sanctuary (Post-Wicabel)"
    ch4_third_sanctuary = "CH4: Third Sanctuary"
    ch4_titan_fight = "CH4: Titan Fight"
    ch4_light_world = "CH4: Light World"

    chapter_5 = "Chapter 5"
    ch5_castle_town = "CH5: Castle Town"
    ch5_dojo = "CH5: Dojo"
    ch5_garden_no_character_required = "CH5: The Garden of Hopes and Dreams (No Character required)"
    ch5_garden = "CH5: The Garden of Hopes and Dreams"
    ch5_greens_cafe = "CH5: Green's Cafe"
    ch5_dark_garden = "CH5: Dark Garden"
    ch5_garden_aqua = "CH5: Aqua Fight"
    ch5_garden_petal_feather = "CH5: Garden (PetalFeather Required)"
    ch5_dark_garden_petal_feather = "CH5: Dark Garden (PetalFeather Required)"
    ch5_cliffs = "CH5: Cliffs"
    ch5_pinks_shop = "CH5: Pink's Shop"
    ch5_flower_castle = "CH5: Flower Castle"
    ch5_vending_machine = "CH5: Vending Machine"
    ch5_castle_west = "CH5: Castle West"
    ch5_castle_east = "CH5: Castle East"
    ch5_castle_top = "CH5: Top of Castle"
    ch5_pink_room = "CH5: Pink Room"
    ch5_flower_rewards = "CH5: Flower Rewards"
    ch5_fountains = "CH5: Fountains"
    ch5_weird_route = "CH5: Weird Route"


def add_location_to_region(region: Region, locations: list[LocationData], world: "DeltaruneWorld"):
    for location in locations:
        if location.should_be_included(world):
            region.locations.append(
                DeltaruneLocation(region.player, all_locations[location.id], location.id.value, region)
            )


def get_entrance_name(origin: Region, destination: Region, complement: str = None):
    text = f"{origin.name.replace(':', '')} -> {destination.name.replace(':', '')}"

    if complement != None:
        text += f" ({complement})"

    return text
