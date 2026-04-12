"""This module represents location definitions for Rabi-Ribi"""
from typing import Dict
from BaseClasses import Location
from .options import RabiRibiOptions
from .names import LocationName
from .utility import get_rabi_ribi_base_id

class RabiRibiLocation(Location):
    """Rabi Ribi Location Definition"""
    game: str = "Rabi-Ribi"

# Item Locations
southern_woodland_locations = {
    LocationName.nature_orb                   : get_rabi_ribi_base_id() + 0x01,
    LocationName.pack_up_forest_night         : get_rabi_ribi_base_id() + 0x02,
    LocationName.hp_up_west_spectral          : get_rabi_ribi_base_id() + 0x03,
    LocationName.atk_up_forest_night          : get_rabi_ribi_base_id() + 0x04,
    LocationName.pack_up_spectral             : get_rabi_ribi_base_id() + 0x05,
    LocationName.mp_up_cave                   : get_rabi_ribi_base_id() + 0x06,
    LocationName.hp_up_cave                   : get_rabi_ribi_base_id() + 0x07,
    LocationName.toxic_strike                 : get_rabi_ribi_base_id() + 0x08,
    LocationName.piko_hammer                  : get_rabi_ribi_base_id() + 0x09,
    LocationName.mp_up_forest_cave            : get_rabi_ribi_base_id() + 0x0A,
    LocationName.tough_skin                   : get_rabi_ribi_base_id() + 0x0B,
    LocationName.regen_up_cave                : get_rabi_ribi_base_id() + 0x0C,
    LocationName.hp_up_north_forest           : get_rabi_ribi_base_id() + 0x0D,
    LocationName.wall_jump                    : get_rabi_ribi_base_id() + 0x0E,
    LocationName.regen_up_mid_forest          : get_rabi_ribi_base_id() + 0x0F,
    LocationName.mp_up_mid_spectral           : get_rabi_ribi_base_id() + 0x10,
    LocationName.hp_up_mid_spectral           : get_rabi_ribi_base_id() + 0x11,
    LocationName.carrot_bomb                  : get_rabi_ribi_base_id() + 0x12,
    LocationName.def_trade                    : get_rabi_ribi_base_id() + 0x13,
    LocationName.light_orb                    : get_rabi_ribi_base_id() + 0x14,
    LocationName.hp_up_forest_post_cocoa      : get_rabi_ribi_base_id() + 0x15,
    LocationName.charge_ring                  : get_rabi_ribi_base_id() + 0x16,
    LocationName.arm_strength                 : get_rabi_ribi_base_id() + 0x17,
    LocationName.regen_up_east_forest         : get_rabi_ribi_base_id() + 0x18,
    LocationName.mana_wager                   : get_rabi_ribi_base_id() + 0x19,
    LocationName.mp_up_east_forest            : get_rabi_ribi_base_id() + 0x1A,
    LocationName.pack_up_east_forest          : get_rabi_ribi_base_id() + 0x1B,
    LocationName.mp_up_cicini                 : get_rabi_ribi_base_id() + 0x1C,
    LocationName.mp_up_northeast_forest       : get_rabi_ribi_base_id() + 0x1D,
}

western_coast_locations = {
    LocationName.survival                     : get_rabi_ribi_base_id() + 0x1E,
    LocationName.health_wager                 : get_rabi_ribi_base_id() + 0x1F,
    LocationName.atk_up_beach_cave            : get_rabi_ribi_base_id() + 0x20,
    LocationName.mp_up_graveyard_warp         : get_rabi_ribi_base_id() + 0x21,
    LocationName.hp_up_graveyard              : get_rabi_ribi_base_id() + 0x22,
    LocationName.sunny_beam                   : get_rabi_ribi_base_id() + 0x23,
    LocationName.mp_up_upper_graveyard        : get_rabi_ribi_base_id() + 0x24,
    LocationName.auto_earrings                : get_rabi_ribi_base_id() + 0x25,
    LocationName.health_plus                  : get_rabi_ribi_base_id() + 0x26,
    LocationName.mp_up_pyramid_dark_room      : get_rabi_ribi_base_id() + 0x27,
    LocationName.crisis_boost                 : get_rabi_ribi_base_id() + 0x28,
    LocationName.atk_up_graveyard             : get_rabi_ribi_base_id() + 0x29,
    LocationName.hp_up_inner_pyramid          : get_rabi_ribi_base_id() + 0x2A,
    LocationName.hp_up_beach                  : get_rabi_ribi_base_id() + 0x2B,
    LocationName.atk_up_pyramid               : get_rabi_ribi_base_id() + 0x2C,
    LocationName.pack_up_pyramid              : get_rabi_ribi_base_id() + 0x2D,
    LocationName.armored                      : get_rabi_ribi_base_id() + 0x2E,
    LocationName.chaos_rod                    : get_rabi_ribi_base_id() + 0x2F,
    LocationName.pack_up_beach                : get_rabi_ribi_base_id() + 0x30,
    LocationName.top_form                     : get_rabi_ribi_base_id() + 0x31,
    LocationName.hp_up_pyramid_entrance       : get_rabi_ribi_base_id() + 0x32,
    LocationName.mp_up_pyramid_bombblock_room : get_rabi_ribi_base_id() + 0x33,
    LocationName.air_dash                     : get_rabi_ribi_base_id() + 0x34,
    LocationName.regen_up_pyramid             : get_rabi_ribi_base_id() + 0x35,
    LocationName.pure_love                    : get_rabi_ribi_base_id() + 0x36,
    LocationName.mp_up_beach_tunnel           : get_rabi_ribi_base_id() + 0x37,
    LocationName.hourglass                    : get_rabi_ribi_base_id() + 0x38,
    LocationName.hp_up_sky_island             : get_rabi_ribi_base_id() + 0x39,
    LocationName.pack_up_sky_island           : get_rabi_ribi_base_id() + 0x3A,
    LocationName.regen_up_sky_island          : get_rabi_ribi_base_id() + 0x3B,
    LocationName.mp_up_beach_pillar           : get_rabi_ribi_base_id() + 0x3C,
}

island_core_locations = {
    LocationName.def_grow                     : get_rabi_ribi_base_id() + 0x3D,
    LocationName.atk_up_park                  : get_rabi_ribi_base_id() + 0x3E,
    LocationName.atk_trade                    : get_rabi_ribi_base_id() + 0x3F,
    LocationName.hp_up_park                   : get_rabi_ribi_base_id() + 0x40,
    LocationName.rabi_slippers                : get_rabi_ribi_base_id() + 0x41,
    LocationName.regen_up_park                : get_rabi_ribi_base_id() + 0x42,
    LocationName.health_surge                 : get_rabi_ribi_base_id() + 0x43,
    LocationName.mp_up_sky_bridge             : get_rabi_ribi_base_id() + 0x44,
    LocationName.mp_up_uprprc_hq              : get_rabi_ribi_base_id() + 0x45,
    LocationName.mp_up_park                   : get_rabi_ribi_base_id() + 0x46,
    LocationName.hex_cancel                   : get_rabi_ribi_base_id() + 0x47,
    LocationName.hp_up_sky_bridge             : get_rabi_ribi_base_id() + 0x48,
    LocationName.pack_up_sky_bridge           : get_rabi_ribi_base_id() + 0x49,
    LocationName.regen_up_sky_bridge          : get_rabi_ribi_base_id() + 0x4A,
    LocationName.lucky_seven                  : get_rabi_ribi_base_id() + 0x4B,
    LocationName.atk_up_vanilla               : get_rabi_ribi_base_id() + 0x4C,
    LocationName.hammer_wave                  : get_rabi_ribi_base_id() + 0x4D,
    LocationName.atk_up_west_ravine           : get_rabi_ribi_base_id() + 0x4E,
    LocationName.hp_up_south_ravine           : get_rabi_ribi_base_id() + 0x4F,
    LocationName.atk_up_north_ravine          : get_rabi_ribi_base_id() + 0x50,
    LocationName.hp_up_mid_ravine             : get_rabi_ribi_base_id() + 0x51,
    LocationName.mp_up_ravine                 : get_rabi_ribi_base_id() + 0x52,
    LocationName.regen_up_ravine              : get_rabi_ribi_base_id() + 0x53,
    LocationName.mana_surge                   : get_rabi_ribi_base_id() + 0x54,
}

northern_tundra_locations = {
    LocationName.hp_up_palace                 : get_rabi_ribi_base_id() + 0x55,
    LocationName.water_orb                    : get_rabi_ribi_base_id() + 0x56,
    LocationName.hp_up_west_aquarium          : get_rabi_ribi_base_id() + 0x57,
    LocationName.mana_plus                    : get_rabi_ribi_base_id() + 0x58,
    LocationName.atk_up_palace                : get_rabi_ribi_base_id() + 0x59,
    LocationName.atk_up_snowland              : get_rabi_ribi_base_id() + 0x5A,
    LocationName.regen_up_palace              : get_rabi_ribi_base_id() + 0x5B,
    LocationName.stamina_plus                 : get_rabi_ribi_base_id() + 0x5C,
    LocationName.mp_up_palace                 : get_rabi_ribi_base_id() + 0x5D,
    LocationName.self_defense                 : get_rabi_ribi_base_id() + 0x5E,
    LocationName.hp_up_upper_aquarium         : get_rabi_ribi_base_id() + 0x5F,
    LocationName.gold_carrot                  : get_rabi_ribi_base_id() + 0x60,
    LocationName.atk_up_upper_aquarium        : get_rabi_ribi_base_id() + 0x61,
    LocationName.pack_up_icy_summit           : get_rabi_ribi_base_id() + 0x62,
    LocationName.atk_up_icy_summit            : get_rabi_ribi_base_id() + 0x63,
    LocationName.atk_up_mid_aquarium          : get_rabi_ribi_base_id() + 0x64,
    LocationName.mp_up_icy_summit             : get_rabi_ribi_base_id() + 0x65,
    LocationName.mp_up_snowland               : get_rabi_ribi_base_id() + 0x66,
    LocationName.quick_barrette               : get_rabi_ribi_base_id() + 0x67,
    LocationName.hp_up_icy_summit             : get_rabi_ribi_base_id() + 0x68,
    LocationName.super_carrot                 : get_rabi_ribi_base_id() + 0x69,
    LocationName.regen_up_snowland_water      : get_rabi_ribi_base_id() + 0x6A,
    LocationName.mp_up_aquarium               : get_rabi_ribi_base_id() + 0x6B,
    LocationName.hp_up_snowland               : get_rabi_ribi_base_id() + 0x6C,
    LocationName.carrot_boost                 : get_rabi_ribi_base_id() + 0x6D,
    LocationName.regen_up_aquarium            : get_rabi_ribi_base_id() + 0x6E,
    LocationName.pack_up_aquarium             : get_rabi_ribi_base_id() + 0x6F,
}

eastern_highlands_locations = {
    LocationName.regen_up_northwest_riverbank : get_rabi_ribi_base_id() + 0x70,
    LocationName.pack_up_riverbank            : get_rabi_ribi_base_id() + 0x71,
    LocationName.mp_up_southwest_riverbank    : get_rabi_ribi_base_id() + 0x72,
    LocationName.atk_grow                     : get_rabi_ribi_base_id() + 0x73,
    LocationName.regen_up_south_riverbank     : get_rabi_ribi_base_id() + 0x74,
    LocationName.atk_up_riverbank_pit         : get_rabi_ribi_base_id() + 0x75,
    LocationName.bunny_whirl                  : get_rabi_ribi_base_id() + 0x76,
    LocationName.explode_shot                 : get_rabi_ribi_base_id() + 0x77,
    LocationName.mp_up_mid_riverbank          : get_rabi_ribi_base_id() + 0x78,
    LocationName.atk_up_east_riverbank        : get_rabi_ribi_base_id() + 0x79,
    LocationName.spike_barrier                : get_rabi_ribi_base_id() + 0x7A,
    LocationName.frame_cancel                 : get_rabi_ribi_base_id() + 0x7B,
    LocationName.hp_up_lab_slide_tunnel       : get_rabi_ribi_base_id() + 0x7C,
    LocationName.mp_up_lab                    : get_rabi_ribi_base_id() + 0x7D,
    LocationName.hp_up_riverbank              : get_rabi_ribi_base_id() + 0x7E,
    LocationName.mp_up_evernight              : get_rabi_ribi_base_id() + 0x7F,
    LocationName.hp_up_evernight              : get_rabi_ribi_base_id() + 0x80,
    LocationName.hp_up_lab_pit                : get_rabi_ribi_base_id() + 0x81,
    LocationName.sliding_powder               : get_rabi_ribi_base_id() + 0x82,
    LocationName.atk_up_evernight_uprprc      : get_rabi_ribi_base_id() + 0x83,
    LocationName.cashback                     : get_rabi_ribi_base_id() + 0x84,
    LocationName.plus_necklace                : get_rabi_ribi_base_id() + 0x85,
    LocationName.weaken                       : get_rabi_ribi_base_id() + 0x86,
    LocationName.atk_up_lab_computer          : get_rabi_ribi_base_id() + 0x87,
    LocationName.pack_up_south_evernight      : get_rabi_ribi_base_id() + 0x88,
    LocationName.pack_up_north_evernight      : get_rabi_ribi_base_id() + 0x89,
    LocationName.regen_up_evernight           : get_rabi_ribi_base_id() + 0x8A,
    LocationName.atk_up_evernight             : get_rabi_ribi_base_id() + 0x8B,
    LocationName.atk_up_east_lab              : get_rabi_ribi_base_id() + 0x8C,
    LocationName.pack_up_lab                  : get_rabi_ribi_base_id() + 0x8D,
    LocationName.hammer_roll                  : get_rabi_ribi_base_id() + 0x8E,

    LocationName.pbpb_box                     : get_rabi_ribi_base_id() + 0xDE,
}

subterranean_area_locations = {
    LocationName.hp_up_volcanic               : get_rabi_ribi_base_id() + 0x8F,
    LocationName.fire_orb                     : get_rabi_ribi_base_id() + 0x90,
    LocationName.pack_up_volcanic             : get_rabi_ribi_base_id() + 0x91,
}

system_interior_locations = {
    LocationName.regen_up_cyberspace          : get_rabi_ribi_base_id() + 0x92,
    LocationName.pack_up_cyberspace           : get_rabi_ribi_base_id() + 0x93,
    LocationName.air_jump                     : get_rabi_ribi_base_id() + 0x94,
    LocationName.hp_up_cyberspace             : get_rabi_ribi_base_id() + 0x95,
    LocationName.atk_up_cyberspace            : get_rabi_ribi_base_id() + 0x96,
    LocationName.mp_up_cyberspace             : get_rabi_ribi_base_id() + 0x97,
}

# Shufflable Gift Item Locations
shufflable_gift_item_plurkwood_locations = {
    LocationName.p_hairpin                    : get_rabi_ribi_base_id() + 0x98,
}

shufflable_gift_item_town_locations = {
    LocationName.speed_boost                  : get_rabi_ribi_base_id() + 0x99,
    LocationName.bunny_strike                 : get_rabi_ribi_base_id() + 0x9A,
}

# Egg Locations
southern_woodland_egg_locations = {
    LocationName.egg_forestnight_aruraune     : get_rabi_ribi_base_id() + 0x9B,
    LocationName.egg_spectral_west            : get_rabi_ribi_base_id() + 0x9C,
    LocationName.egg_cave_under_hammer        : get_rabi_ribi_base_id() + 0x9D,
    LocationName.egg_forestnight_east         : get_rabi_ribi_base_id() + 0x9E,
    LocationName.egg_spectral_slide           : get_rabi_ribi_base_id() + 0x9F,
    LocationName.egg_cave_cocoa               : get_rabi_ribi_base_id() + 0xA0,
    LocationName.egg_forest_ne_ledge          : get_rabi_ribi_base_id() + 0xA1,
    LocationName.egg_forest_ne_pedestal       : get_rabi_ribi_base_id() + 0xA2,
}

western_coast_egg_locations = {
    LocationName.egg_beach_to_aquarium        : get_rabi_ribi_base_id() + 0xA3,
    LocationName.egg_graveyard_near_library   : get_rabi_ribi_base_id() + 0xA4,
    LocationName.egg_pyramid_beach            : get_rabi_ribi_base_id() + 0xA5,
    LocationName.egg_pyramid_lower            : get_rabi_ribi_base_id() + 0xA6,
    LocationName.egg_sky_town                 : get_rabi_ribi_base_id() + 0xA7,
}

island_core_egg_locations = {
    LocationName.egg_park_spikes              : get_rabi_ribi_base_id() + 0xA8,
    LocationName.egg_park_green_kotri         : get_rabi_ribi_base_id() + 0xA9,
    LocationName.egg_uprprc_base              : get_rabi_ribi_base_id() + 0xAA,
    LocationName.egg_sky_bridge_warp          : get_rabi_ribi_base_id() + 0xAB,
    LocationName.egg_sky_bridge_by_vanilla    : get_rabi_ribi_base_id() + 0xAC,
    LocationName.egg_ravine_above_chocolate   : get_rabi_ribi_base_id() + 0xAD,
    LocationName.egg_ravine_mid               : get_rabi_ribi_base_id() + 0xAE,

    LocationName.egg_sky_bridge_above_warp    : get_rabi_ribi_base_id() + 0xDF,
}

northern_tundra_egg_locations = {
    LocationName.egg_snowland_to_evernight    : get_rabi_ribi_base_id() + 0xAF,
    LocationName.egg_palace_bridge            : get_rabi_ribi_base_id() + 0xB0,
    LocationName.egg_aquarium                 : get_rabi_ribi_base_id() + 0xB1,
    LocationName.egg_palace_wall              : get_rabi_ribi_base_id() + 0xB2,
    LocationName.egg_snowland_warp            : get_rabi_ribi_base_id() + 0xB3,
    LocationName.egg_icy_summit_nixie         : get_rabi_ribi_base_id() + 0xB4,
    LocationName.egg_icy_summit_warp          : get_rabi_ribi_base_id() + 0xB5,
    LocationName.egg_snowland_lake            : get_rabi_ribi_base_id() + 0xB6,

    LocationName.egg_snowland_spikes_room     : get_rabi_ribi_base_id() + 0xE0,
}

eastern_highlands_egg_locations = {
    LocationName.egg_riverbank_spider_spike   : get_rabi_ribi_base_id() + 0xB7,
    LocationName.egg_riverbank_wall           : get_rabi_ribi_base_id() + 0xB8,
    LocationName.egg_lab                      : get_rabi_ribi_base_id() + 0xB9,
    LocationName.egg_evernight_mid            : get_rabi_ribi_base_id() + 0xBA,
    LocationName.egg_evernight_saya           : get_rabi_ribi_base_id() + 0xBB,

    LocationName.egg_lab_entrance             : get_rabi_ribi_base_id() + 0xE1,
}

rabi_rabi_town_egg_locations = {
    LocationName.egg_town                     : get_rabi_ribi_base_id() + 0xBC,
}

plurkwood_egg_locations = {
    LocationName.egg_plurk_cats               : get_rabi_ribi_base_id() + 0xBD,
    LocationName.egg_plurk_cave               : get_rabi_ribi_base_id() + 0xBE,
    LocationName.egg_plurk_east               : get_rabi_ribi_base_id() + 0xBF,
}

subterranean_area_egg_locations = {
    LocationName.egg_volcanic_bomb_bunnies    : get_rabi_ribi_base_id() + 0xC0,
    LocationName.egg_volcanic_fire_orb        : get_rabi_ribi_base_id() + 0xC1,
    LocationName.egg_volcanic_ne              : get_rabi_ribi_base_id() + 0xC2,
    LocationName.egg_volcanic_big_drop        : get_rabi_ribi_base_id() + 0xC3,
}

warp_destination_egg_locations = {
    LocationName.egg_crespirit                : get_rabi_ribi_base_id() + 0xC4,
}

system_interior_egg_locations = {
    LocationName.egg_sysint1                  : get_rabi_ribi_base_id() + 0xC5,
}

# Post Game Locations
southern_woodland_post_game_locations = {
    LocationName.blessed                      : get_rabi_ribi_base_id() + 0xC6,
    LocationName.egg_rumi                     : get_rabi_ribi_base_id() + 0xC7,
}

western_coast_post_game_locations = {
    LocationName.auto_trigger                 : get_rabi_ribi_base_id() + 0xC8,
    LocationName.hitbox_down                  : get_rabi_ribi_base_id() + 0xC9,
    LocationName.egg_library                  : get_rabi_ribi_base_id() + 0xCA,
}

subterranean_area_post_game_locations = {
    LocationName.carrot_shooter               : get_rabi_ribi_base_id() + 0xCB,
    LocationName.egg_memories_sysint          : get_rabi_ribi_base_id() + 0xCC,
    LocationName.egg_memories_ravine          : get_rabi_ribi_base_id() + 0xCD,

    LocationName.egg_memories_cars_room       : get_rabi_ribi_base_id() + 0xE2,
}

warp_destination_post_game_locations = {
    LocationName.egg_hospital_wall            : get_rabi_ribi_base_id() + 0xCE,
    LocationName.egg_hospital_box             : get_rabi_ribi_base_id() + 0xCF,
}

system_interior_post_game_locations = {
    LocationName.cyber_flower                 : get_rabi_ribi_base_id() + 0xD0,
    LocationName.egg_sysint2                  : get_rabi_ribi_base_id() + 0xD1,

    LocationName.egg_sysint2_long_jump        : get_rabi_ribi_base_id() + 0xE3
}

# Post Irisu Locations
rabi_rabi_town_post_irisu_locations = {
    LocationName.ribbon_badge                 : get_rabi_ribi_base_id() + 0xD2,
    LocationName.erina_badge                  : get_rabi_ribi_base_id() + 0xD3,
}

# Halloween Locations
western_coast_halloween_locations = {
    LocationName.egg_halloween_cicini_room    : get_rabi_ribi_base_id() + 0xD4,
    LocationName.egg_halloween_west           : get_rabi_ribi_base_id() + 0xD5,
    LocationName.egg_halloween_mid            : get_rabi_ribi_base_id() + 0xD6,
    LocationName.egg_halloween_sw_slide       : get_rabi_ribi_base_id() + 0xD7,
    LocationName.egg_halloween_near_boss      : get_rabi_ribi_base_id() + 0xD8,
    LocationName.egg_halloween_warp_zone      : get_rabi_ribi_base_id() + 0xD9,
    LocationName.egg_halloween_left_pillar    : get_rabi_ribi_base_id() + 0xDA,
    LocationName.egg_halloween_right_pillar   : get_rabi_ribi_base_id() + 0xDB,
    LocationName.egg_halloween_past_pillars1  : get_rabi_ribi_base_id() + 0xDC,
    LocationName.egg_halloween_past_pillars2  : get_rabi_ribi_base_id() + 0xDD,
}

# Area Location Tables
southern_woodland_table = {
    **southern_woodland_locations,
    **southern_woodland_egg_locations,
    **southern_woodland_post_game_locations,
}

western_coast_table = {
    **western_coast_locations,
    **western_coast_egg_locations,
    **western_coast_post_game_locations,
    **western_coast_halloween_locations,
}

island_core_table = {
    **island_core_locations,
    **island_core_egg_locations,
}

northern_tundra_table = {
    **northern_tundra_locations,
    **northern_tundra_egg_locations,
}

eastern_highlands_table = {
    **eastern_highlands_locations,
    **eastern_highlands_egg_locations,
}

rabi_rabi_town_table = {
    **rabi_rabi_town_egg_locations,
    **rabi_rabi_town_post_irisu_locations
}

plurkwood_table = {
    **plurkwood_egg_locations,
}

subterranean_area_table = {
    **subterranean_area_locations,
    **subterranean_area_egg_locations,
    **subterranean_area_post_game_locations,
}

warp_destination_table = {
    **warp_destination_egg_locations,
    **warp_destination_post_game_locations
}

system_interior_table = {
    **system_interior_locations,
    **system_interior_egg_locations,
    **system_interior_post_game_locations
}

shufflable_gift_item_table = {
    **shufflable_gift_item_town_locations,
    **shufflable_gift_item_plurkwood_locations
}

# Combined Location Table
all_locations = {
    **southern_woodland_table,
    **western_coast_table,
    **island_core_table,
    **northern_tundra_table,
    **eastern_highlands_table,
    **rabi_rabi_town_table,
    **plurkwood_table,
    **subterranean_area_table,
    **warp_destination_table,
    **system_interior_table,
    **shufflable_gift_item_table
}

default_locations = {
    **southern_woodland_locations,
    **southern_woodland_egg_locations,
    **western_coast_locations,
    **western_coast_egg_locations,
    **island_core_locations,
    **island_core_egg_locations,
    **northern_tundra_locations,
    **northern_tundra_egg_locations,
    **eastern_highlands_locations,
    **eastern_highlands_egg_locations,
    **shufflable_gift_item_town_locations,
    **rabi_rabi_town_egg_locations,
    **subterranean_area_locations,
    **subterranean_area_egg_locations,
    **system_interior_locations,
    **system_interior_egg_locations,
}

lookup_location_id_to_name = {code: name for name, code in all_locations.items()}

location_groups = {
    LocationName.southern_woodland_region   : set(southern_woodland_table.keys()),
    LocationName.western_coast_region       : set(western_coast_table.keys()),
    LocationName.island_core_region         : set(island_core_table.keys()),
    LocationName.northern_tundra_region     : set(northern_tundra_table.keys()),
    LocationName.eastern_highlands_region   : set(eastern_highlands_table.keys()),
    LocationName.rabi_rabi_town_region      : set(rabi_rabi_town_table.keys()),
    LocationName.plurkwood_region           : set(plurkwood_table.keys()),
    LocationName.subterranean_area_region   : set(subterranean_area_table.keys()),
    LocationName.system_interior_region     : set(system_interior_table.keys()),
    LocationName.shufflable_gift_items      : set(shufflable_gift_item_table.keys())
}

def setup_locations(options: RabiRibiOptions):
    location_table: Dict[str, int] = {
        **default_locations
    }

    if options.include_plurkwood:
        location_table.update(**shufflable_gift_item_plurkwood_locations)
        location_table.update(**plurkwood_egg_locations)

    if options.include_warp_destination:
        location_table.update(**warp_destination_egg_locations)
        if options.include_post_game:
            location_table.update(**warp_destination_post_game_locations)
    
    if options.include_post_game:
        location_table.update(**southern_woodland_post_game_locations)
        location_table.update(**western_coast_post_game_locations)
        location_table.update(**subterranean_area_post_game_locations)
        location_table.update(**system_interior_post_game_locations)

    if options.include_post_irisu:
        location_table.update(**rabi_rabi_town_post_irisu_locations)

    if options.include_halloween:
        location_table.update(**western_coast_halloween_locations)

    return location_table
