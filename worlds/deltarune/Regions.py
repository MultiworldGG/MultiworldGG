from enum import StrEnum

from BaseClasses import Region
from typing import TYPE_CHECKING, Optional
from worlds.deltarune.Locations import DeltaruneLocation, LocationData, locations as all_locations

if TYPE_CHECKING:
    from . import DeltaruneWorld


class Regions(StrEnum):
    chapter_select = "Chapter Select"
    fusion = "Fusion"
    lost_rabbick = "Cross Chapter: Lost Rabbick"

    chapter_1 = "Chapter 1"
    ch1_unknown = "CH1: ??????"
    ch1_castle_town = "CH1: Castle Town"
    ch1_fields = "CH1: Fields"
    ch1_fields_post_hathy = "CH1: Fields (Post-Hathy)"
    ch1_seam_seap = "CH1: Seam's Seap"
    ch1_great_board = "CH1: Great Board"
    ch1_forest = "CH1: Forest"
    ch1_bake_sale = "CH1: Bake Sale"
    ch1_forest_post_bake_sale = "CH1: Forest (Post-Bake Sale)"
    ch1_card_castle = "CH1: Card Castle"
    ch1_rouxls = "CH1: Rouxls' shop"
    ch1_jevil = "CH1: Jevil"
    ch1_light_world = "CH1: Light World"

    chapter_2 = "Chapter 2"
    ch2_castle_town = "CH2: Castle Town"
    ch2_dojo = "CH2: Dojo"
    ch2_cyber_field = "CH2: Cyber Field"
    ch2_cyber_field_post_dj = "CH2: Cyber Field (Post-DJ)"
    ch2_music_shop = "CH2: Music Shop"
    ch2_trash_zone = "CH2: Trash Zone"
    ch2_spamton_shop = "CH2: Spamton's Shop"
    ch2_cyber_city = "CH2: Cyber City"
    ch2_cyber_city_spamton_fight = "CH2: Cyber City (Spamton fight)"
    ch2_cyber_city_post_spamton = "CH2: Cyber City (Post-Spamton)"
    ch2_mansion_lobby = "CH2: Mansion Lobby"
    ch2_swatch_cafe = "CH2: Swatch's Cafe"
    ch2_mansion = "CH2: Mansion"
    ch2_mansion_basement = "CH2: Mansion Basement"
    ch2_tunnel_of_love = "CH2: Tunnel of love"
    ch2_mansion_recruits = "CH2: Mansion Recruits"
    ch2_werewerewire = "CH2: Werewerewire"
    ch2_spamton_neo = "CH2: Spamton Neo"
    ch2_post_chapter_castle_town = "CH2: Post-Chapter Castle Town"

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
    ch3_cold_place = "CH3: Cold Place"

    chapter_4 = "Chapter 4"
    ch4_castle_town = "CH4: Castle Town"
    ch4_dojo = "CH4: Dojo"
    ch4_mike_room = "CH4: Mike Room"
    ch4_dark_sanctuary = "CH4: Dark Sanctuary"
    ch4_old_man_shop = "CH4: Old Man's Shop"
    ch4_dark_sanctuary_claimbclaws = "CH4: Dark Sanctuary (ClaimbClaws Required)"
    ch4_gerson = "CH4: Gerson"
    ch4_second_sanctuary = "CH4: Second Sanctuary"
    ch4_third_sanctuary = "CH4: Third Sanctuary"
    ch4_titan_fight = "CH4: Titan Fight"
    ch4_light_world = "CH4: Light World"

    chapter_5 = "Chapter 5"


def add_location_to_region(region: Region, locations: list[LocationData], world: "DeltaruneWorld"):
    for location in locations:
        if location.should_be_included(world):
            region.locations.append(
                DeltaruneLocation(region.player, all_locations[location.id], location.id.value, region)
            )


def get_entrance_name(origin: Region, destination: Region, complement: str = None):
    text = f"{origin.name.replace(":", "")} -> {destination.name.replace(":", "")}"

    if complement != None:
        text += f" ({complement})"

    return text
