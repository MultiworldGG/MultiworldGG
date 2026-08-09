from enum import Flag, auto

from attr import dataclass
from BaseClasses import Location
from .ItemNames import *
from .LocationNames import *

portal_2_base_id = 98275000
offset_index = 0

class LocationType(Flag):
    MAP_COMPLETION = auto()
    CUTSCENE_COMPLETION = auto()
    STORY_ACHIEVEMENT = auto()
    ITEM = auto()
    ACHIEVEMENT = auto()
    WHEATLY_MONITOR = auto()
    RATMAN_DEN = auto()
    OTHER = auto()

class Portal2LocationData:
    def __init__(self, map_name: str = None, location_type: LocationType = None, required_items: list[str] = [], chapter: int = None):
        self.map_name = map_name
        self.location_type = location_type

        self.required_items = required_items
        self.chapter = chapter

        global portal_2_base_id, offset_index
        self.id = portal_2_base_id + offset_index
        offset_index += 1

class Portal2Location(Location):
    game: str = "Portal 2"

map_complete_table: dict[str, Portal2LocationData] = {
    # Chapter 1
    container_ride_completion: Portal2LocationData("sp_a1_intro1", LocationType.MAP_COMPLETION, [weighted_cube, floor_button], 1),
    portal_carousel_completion: Portal2LocationData("sp_a1_intro2", LocationType.MAP_COMPLETION, [button, weighted_cube, floor_button], 1),
    portal_gun_completion: Portal2LocationData("sp_a1_intro3", LocationType.MAP_COMPLETION, [], 1),
    smooth_jazz_completion: Portal2LocationData("sp_a1_intro4", LocationType.MAP_COMPLETION, [weighted_cube, floor_button], 1),
    cube_momentum_completion: Portal2LocationData("sp_a1_intro5", LocationType.MAP_COMPLETION, [button, weighted_cube, floor_button], 1),
    future_starter_completion: Portal2LocationData("sp_a1_intro6", LocationType.MAP_COMPLETION, [weighted_cube, floor_button], 1),
    secret_panel_completion: Portal2LocationData("sp_a1_intro7", LocationType.MAP_COMPLETION, [], 1),
    wake_up_completion: Portal2LocationData("sp_a1_wakeup", LocationType.MAP_COMPLETION, [], 1),
    incinerator_completion: Portal2LocationData("sp_a2_intro", LocationType.MAP_COMPLETION, [portal_gun_2], 1),
    # Chapter 2
    laser_intro_completion: Portal2LocationData("sp_a2_laser_intro", LocationType.MAP_COMPLETION, [portal_gun_2, laser, laser_catcher], 2),
    laser_stairs_completion: Portal2LocationData("sp_a2_laser_stairs", LocationType.MAP_COMPLETION, [portal_gun_2, reflection_cube, floor_button, laser, laser_catcher], 2),
    dual_lasers_completion: Portal2LocationData("sp_a2_dual_lasers", LocationType.MAP_COMPLETION, [portal_gun_2, reflection_cube, laser, laser_catcher], 2),
    laser_over_goo_completion: Portal2LocationData("sp_a2_laser_over_goo", LocationType.MAP_COMPLETION, [button, floor_button, weighted_cube,  portal_gun_2, laser, laser_catcher], 2),
    catapult_intro_completion: Portal2LocationData("sp_a2_catapult_intro", LocationType.MAP_COMPLETION, [faith_plate, button, weighted_cube, floor_button], 2),
    trust_fling_completion: Portal2LocationData("sp_a2_trust_fling", LocationType.MAP_COMPLETION, [portal_gun_2, faith_plate, button, weighted_cube, floor_button], 2),
    pit_flings_completion: Portal2LocationData("sp_a2_pit_flings", LocationType.MAP_COMPLETION, [portal_gun_2, weighted_cube, laser, laser_catcher, floor_button], 2),
    fizzler_intro_completion: Portal2LocationData("sp_a2_fizzler_intro", LocationType.MAP_COMPLETION, [portal_gun_2, laser, reflection_cube, laser_catcher, button], 2),
    # Chapter 3
    ceiling_catapult_completion: Portal2LocationData("sp_a2_sphere_peek", LocationType.MAP_COMPLETION, [portal_gun_2, faith_plate, button, reflection_cube, laser, laser_catcher], 3),
    ricochet_completion: Portal2LocationData("sp_a2_ricochet", LocationType.MAP_COMPLETION, [portal_gun_2, faith_plate, weighted_cube, laser, laser_catcher, reflection_cube, floor_button, button], 3),
    bridge_intro_completion: Portal2LocationData("sp_a2_bridge_intro", LocationType.MAP_COMPLETION, [portal_gun_2, bridge, floor_button, button, weighted_cube], 3),
    bridge_the_gap_completion: Portal2LocationData("sp_a2_bridge_the_gap", LocationType.MAP_COMPLETION, [portal_gun_2, bridge, floor_button, button, weighted_cube], 3),
    turret_intro_completion: Portal2LocationData("sp_a2_turret_intro", LocationType.MAP_COMPLETION, [portal_gun_2, weighted_cube, floor_button, turrets], 3),
    laser_relays_completion: Portal2LocationData("sp_a2_laser_relays", LocationType.MAP_COMPLETION, [portal_gun_2, laser, reflection_cube, laser_relays], 3),
    turret_blocker_completion: Portal2LocationData("sp_a2_turret_blocker", LocationType.MAP_COMPLETION, [portal_gun_2, bridge, faith_plate, floor_button, weighted_cube], 3),
    laser_vs_turret_completion: Portal2LocationData("sp_a2_laser_vs_turret", LocationType.MAP_COMPLETION, [portal_gun_2, laser, laser_catcher, weighted_cube, reflection_cube, floor_button], 3),
    pull_the_rug_completion: Portal2LocationData("sp_a2_pull_the_rug", LocationType.MAP_COMPLETION, [portal_gun_2, bridge, weighted_cube, floor_button, laser, laser_catcher], 3),
    # Chapter 4
    column_blocker_completion: Portal2LocationData("sp_a2_column_blocker", LocationType.MAP_COMPLETION, [portal_gun_2, bridge, laser, laser_catcher, laser_relays, button, reflection_cube, faith_plate], 4),
    laser_chaining_completion: Portal2LocationData("sp_a2_laser_chaining", LocationType.MAP_COMPLETION, [portal_gun_2, laser, laser_catcher, laser_relays, reflection_cube, faith_plate], 4),
    triple_laser_completion: Portal2LocationData("sp_a2_triple_laser", LocationType.MAP_COMPLETION, [portal_gun_2, laser, laser_catcher, reflection_cube], 4),
    jailbreak_completion: Portal2LocationData("sp_a2_bts1", LocationType.MAP_COMPLETION, [portal_gun_2, bridge, button, weighted_cube], 4),
    escape_completion: Portal2LocationData("sp_a2_bts2", LocationType.MAP_COMPLETION, [portal_gun_2, turrets], 4),
    # Chapter 5
    turret_factory_completion: Portal2LocationData("sp_a2_bts3", LocationType.MAP_COMPLETION, [portal_gun_2], 5),
    turret_sabotage_completion: Portal2LocationData("sp_a2_bts4", LocationType.MAP_COMPLETION, [portal_gun_2, turrets], 5),
    neurotoxin_sabotage_completion: Portal2LocationData("sp_a2_bts5", LocationType.MAP_COMPLETION, [portal_gun_2, laser], 5),
    core_completion: Portal2LocationData("sp_a2_core", LocationType.MAP_COMPLETION, [portal_gun_2, button, turrets], 5),
    # Chapter 6
    underground_completion: Portal2LocationData("sp_a3_01", LocationType.MAP_COMPLETION, [portal_gun_2], 6),
    cave_johnson_completion: Portal2LocationData("sp_a3_03", LocationType.MAP_COMPLETION, [portal_gun_2], 6),
    repulsion_intro_completion: Portal2LocationData("sp_a3_jump_intro", LocationType.MAP_COMPLETION, [portal_gun_2, blue_gel, old_button, old_floor_button, antique_cube], 6),
    bomb_flings_completion: Portal2LocationData("sp_a3_bomb_flings", LocationType.MAP_COMPLETION, [portal_gun_2, old_button, blue_gel], 6),
    crazy_box_completion: Portal2LocationData("sp_a3_crazy_box", LocationType.MAP_COMPLETION, [portal_gun_2, old_button, blue_gel, antique_cube, old_floor_button], 6),
    potatos_completion: Portal2LocationData("sp_a3_transition01", LocationType.MAP_COMPLETION, [portal_gun_2, potatos], 6),
    # Chapter 7
    propulsion_intro_completion: Portal2LocationData("sp_a3_speed_ramp", LocationType.MAP_COMPLETION, [portal_gun_2, blue_gel, orange_gel, antique_cube, old_floor_button, old_button], 7),
    propulsion_flings_completion: Portal2LocationData("sp_a3_speed_flings", LocationType.MAP_COMPLETION, [portal_gun_2, blue_gel, orange_gel, antique_cube, old_floor_button], 7),
    conversion_intro_completion: Portal2LocationData("sp_a3_portal_intro", LocationType.MAP_COMPLETION, [portal_gun_2, blue_gel, orange_gel, white_gel], 7),
    three_gels_completion: Portal2LocationData("sp_a3_end", LocationType.MAP_COMPLETION, [portal_gun_2, blue_gel, orange_gel, white_gel], 7),
    # Chapter 8
    test_completion: Portal2LocationData("sp_a4_intro", LocationType.MAP_COMPLETION, [portal_gun_2, frankenturret, floor_button, button], 8),
    funnel_intro_completion: Portal2LocationData("sp_a4_tb_intro", LocationType.MAP_COMPLETION, [portal_gun_2, funnel, frankenturret, floor_button], 8),
    ceiling_button_completion: Portal2LocationData("sp_a4_tb_trust_drop", LocationType.MAP_COMPLETION, [portal_gun_2, funnel, frankenturret, floor_button, button], 8),
    wall_button_completion: Portal2LocationData("sp_a4_tb_wall_button", LocationType.MAP_COMPLETION, [portal_gun_2, funnel, frankenturret, floor_button, button, faith_plate], 8),
    polarity_completion: Portal2LocationData("sp_a4_tb_polarity", LocationType.MAP_COMPLETION, [portal_gun_2, funnel, frankenturret, floor_button], 8),
    funnel_catch_completion: Portal2LocationData("sp_a4_tb_catch", LocationType.MAP_COMPLETION, [portal_gun_2, funnel, frankenturret, floor_button, button, faith_plate], 8),
    stop_the_box_completion: Portal2LocationData("sp_a4_stop_the_box", LocationType.MAP_COMPLETION, [portal_gun_2, frankenturret, floor_button, button, faith_plate, bridge], 8),
    laser_catapult_completion: Portal2LocationData("sp_a4_laser_catapult", LocationType.MAP_COMPLETION, [portal_gun_2, frankenturret, floor_button, faith_plate, reflection_cube, laser, laser_catcher, funnel], 8),
    laser_platform_completion: Portal2LocationData("sp_a4_laser_platform", LocationType.MAP_COMPLETION, [portal_gun_2, button, reflection_cube, laser, laser_catcher, funnel], 8),
    propulsion_catch_completion: Portal2LocationData("sp_a4_speed_tb_catch", LocationType.MAP_COMPLETION, [portal_gun_2, floor_button, funnel, button, frankenturret, orange_gel], 8),
    repulsion_polarity_completion: Portal2LocationData("sp_a4_jump_polarity", LocationType.MAP_COMPLETION, [portal_gun_2, blue_gel, white_gel, funnel, floor_button, button], 8),
    # Chapter 9
    finale_1_completion: Portal2LocationData("sp_a4_finale1", LocationType.MAP_COMPLETION, [portal_gun_2, faith_plate, funnel, white_gel], 9),
    finale_2_completion: Portal2LocationData("sp_a4_finale2", LocationType.MAP_COMPLETION, [portal_gun_2, funnel, blue_gel, floor_button, turrets], 9),
    finale_3_completion: Portal2LocationData("sp_a4_finale3", LocationType.MAP_COMPLETION, [portal_gun_2, orange_gel, white_gel, funnel], 9),
    finale_4_completion: Portal2LocationData("sp_a4_finale4", LocationType.MAP_COMPLETION, [portal_gun_2, potatos, blue_gel, orange_gel, white_gel, adventure_core, space_core, fact_core], 9),
}

# Optional Checks

cutscene_completion_table: dict[str, Portal2LocationData] = {
    tube_ride_completion: Portal2LocationData("sp_a2_bts6", LocationType.CUTSCENE_COMPLETION, [], 5),
    long_fall_completion: Portal2LocationData("sp_a3_00", LocationType.CUTSCENE_COMPLETION, [], 6),
}

maps_in_chapters: dict[str, list[str]] = {
    "Chapter 1": [container_ride_completion, portal_carousel_completion, portal_gun_completion, smooth_jazz_completion, cube_momentum_completion, future_starter_completion, secret_panel_completion, wake_up_completion, incinerator_completion],
    "Chapter 2": [laser_intro_completion, laser_stairs_completion, dual_lasers_completion, laser_over_goo_completion, catapult_intro_completion, trust_fling_completion, pit_flings_completion, fizzler_intro_completion],
    "Chapter 3": [ceiling_catapult_completion, ricochet_completion, bridge_intro_completion, bridge_the_gap_completion, turret_intro_completion, laser_relays_completion, turret_blocker_completion, laser_vs_turret_completion, pull_the_rug_completion],
    "Chapter 4": [column_blocker_completion, laser_chaining_completion, triple_laser_completion, jailbreak_completion, escape_completion],
    "Chapter 5": [turret_factory_completion, turret_sabotage_completion, neurotoxin_sabotage_completion, core_completion, tube_ride_completion],
    "Chapter 6": [long_fall_completion, underground_completion, cave_johnson_completion, repulsion_intro_completion, bomb_flings_completion, crazy_box_completion, potatos_completion],
    "Chapter 7": [propulsion_intro_completion, propulsion_flings_completion, conversion_intro_completion, three_gels_completion],
    "Chapter 8": [test_completion, funnel_intro_completion, ceiling_button_completion, wall_button_completion, polarity_completion, funnel_catch_completion, stop_the_box_completion, laser_catapult_completion, laser_platform_completion, propulsion_catch_completion, repulsion_polarity_completion],
    "Chapter 9": [finale_1_completion, finale_2_completion, finale_3_completion, finale_4_completion]
}


# Not implemented
story_achievements_table: dict[str, Portal2LocationData] = {
    "Achievement: Wake Up Call": Portal2LocationData("sp_a1_intro1", LocationType.STORY_ACHIEVEMENT),
    "Achievement: You Monster": Portal2LocationData("sp_a1_wakeup", LocationType.STORY_ACHIEVEMENT),
    "Achievement: Undiscouraged": Portal2LocationData("sp_a2_laser_intro", LocationType.STORY_ACHIEVEMENT),
    "Achievement: Bridge Over Troubling Water": Portal2LocationData("sp_a2_bridge_intro", LocationType.STORY_ACHIEVEMENT),
    "Achievement: SaBOTour": Portal2LocationData("sp_a2_bts1", LocationType.STORY_ACHIEVEMENT),
    "Achievement: Vertically Unchallenged": Portal2LocationData("sp_a3_jump_intro", LocationType.STORY_ACHIEVEMENT),
    "Achievement: Stranger Than Friction": Portal2LocationData("sp_a3_speed_ramp", LocationType.STORY_ACHIEVEMENT),
    "Achievement: White Out": Portal2LocationData("sp_a3_portal_intro", LocationType.STORY_ACHIEVEMENT),
    "Achievement: Dual Pit Experiment": Portal2LocationData("sp_a4_intro", LocationType.STORY_ACHIEVEMENT),
    "Achievement: Tunnel of Funnel": Portal2LocationData("sp_a4_speed_catch", LocationType.STORY_ACHIEVEMENT),
    "Achievement: The Part Where He Kills You": Portal2LocationData("sp_a4_finale1", LocationType.STORY_ACHIEVEMENT),
    "Achievement: Lunacy": Portal2LocationData("sp_a4_finale4", LocationType.STORY_ACHIEVEMENT),
    "Achievement: Drop Box": Portal2LocationData(None, LocationType.STORY_ACHIEVEMENT),
}

# Not implementd
achievements_table: dict[str, Portal2LocationData] = {}

wheatley_monitor_table: dict[str, Portal2LocationData] = {
    wheatley_monitor_1_funnel_intro: Portal2LocationData("sp_a4_tb_intro", LocationType.WHEATLY_MONITOR, [portal_gun_2, funnel, frankenturret]),
    wheatley_monitor_2_ceiling_button: Portal2LocationData("sp_a4_tb_trust_drop", LocationType.WHEATLY_MONITOR, [portal_gun_2, button, funnel, frankenturret]),
    wheatley_monitor_3_wall_button: Portal2LocationData("sp_a4_tb_wall_button", LocationType.WHEATLY_MONITOR, [portal_gun_2]),
    wheatley_monitor_4_polarity: Portal2LocationData("sp_a4_tb_polarity", LocationType.WHEATLY_MONITOR, [turrets]),
    wheatley_monitor_5_funnel_catch: Portal2LocationData("sp_a4_tb_catch 1", LocationType.WHEATLY_MONITOR, [portal_gun_2, frankenturret, funnel, faith_plate, button]), #monitor1
    wheatley_monitor_6_funnel_catch: Portal2LocationData("sp_a4_tb_catch 2", LocationType.WHEATLY_MONITOR, [portal_gun_2, frankenturret, funnel, faith_plate, button]), #monitor2
    wheatley_monitor_7_stop_the_box: Portal2LocationData("sp_a4_stop_the_box", LocationType.WHEATLY_MONITOR, [faith_plate]),
    wheatley_monitor_8_laser_catapult: Portal2LocationData("sp_a4_laser_catapult", LocationType.WHEATLY_MONITOR, [portal_gun_2, frankenturret, faith_plate, funnel, reflection_cube, laser, laser_catcher]),
    wheatley_monitor_9_laser_platform: Portal2LocationData("sp_a4_laser_platform", LocationType.WHEATLY_MONITOR, [portal_gun_2, laser, laser_catcher, reflection_cube, button]),
    wheatley_monitor_10_propulsion_catch: Portal2LocationData("sp_a4_speed_tb_catch", LocationType.WHEATLY_MONITOR, [portal_gun_2]),
    wheatley_monitor_11_repulsion_polarity: Portal2LocationData("sp_a4_jump_polarity", LocationType.WHEATLY_MONITOR, [portal_gun_2, blue_gel, white_gel, funnel, turrets, floor_button, button]),
    wheatley_monitor_12_finale_3: Portal2LocationData("sp_a4_finale3", LocationType.WHEATLY_MONITOR, [portal_gun_2, white_gel]),
}

# Note: these are the names used in game to identify the monitors
# most are just the map name but some have a number after due to multiple monitors in the same map
wheatley_maps_to_monitor_names: dict[str, str] = {value.map_name: key for key, value in wheatley_monitor_table.items()}

item_location_table: dict[str, Portal2LocationData] = {
    portal_gun_1: Portal2LocationData("sp_a1_intro3", LocationType.ITEM),
    portal_gun_2: Portal2LocationData("sp_a2_intro", LocationType.ITEM),
    potatos: Portal2LocationData("sp_a3_transition01", LocationType.ITEM, [portal_gun_2]),
}

item_maps_to_item_location : dict[str, str] = {value.map_name:key for key, value in item_location_table.items()}

ratman_den_locations_table: dict[str, Portal2LocationData] = {
    ratman_den_1_smooth_jazz: Portal2LocationData("sp_a1_intro4", LocationType.RATMAN_DEN, [weighted_cube, floor_button]),
    ratman_den_2_dual_lasers: Portal2LocationData("sp_a2_dual_lasers", LocationType.RATMAN_DEN),
    ratman_den_3_trust_fling: Portal2LocationData("sp_a2_trust_fling", LocationType.RATMAN_DEN, [portal_gun_2, faith_plate]),
    ratman_den_4_bridge_intro: Portal2LocationData("sp_a2_bridge_intro", LocationType.RATMAN_DEN),
    ratman_den_5_bridge_the_gap: Portal2LocationData("sp_a2_bridge_the_gap", LocationType.RATMAN_DEN, [portal_gun_2, bridge]),
    ratman_den_6_laser_vs_turret: Portal2LocationData("sp_a2_laser_vs_turret", LocationType.RATMAN_DEN, [portal_gun_2, laser, floor_button, reflection_cube]),
    ratman_den_7_pull_the_rug: Portal2LocationData("sp_a2_pull_the_rug", LocationType.RATMAN_DEN, [portal_gun_2, bridge])
}

ratman_map_to_ratman_den: dict[str, str] = {value.map_name: key for key, value in ratman_den_locations_table.items()}

vitrified_door_locations_table: dict[str, Portal2LocationData] = {
    vitrified_door_1_cave_johnson: Portal2LocationData("sp_a3_03", LocationType.OTHER, [portal_gun_2], 6),
    vitrified_door_2_cave_johnson: Portal2LocationData("sp_a3_03", LocationType.OTHER, [portal_gun_2], 6),
    vitrified_door_3_cave_johnson: Portal2LocationData("sp_a3_03", LocationType.OTHER, [portal_gun_2], 6),
    vitrified_door_4_potatos: Portal2LocationData("sp_a3_transition01", LocationType.OTHER, [portal_gun_2], 6),
    vitrified_door_5_potatos: Portal2LocationData("sp_a3_transition01", LocationType.OTHER, [portal_gun_2], 6),
    vitrified_door_6_potatos: Portal2LocationData("sp_a3_transition01", LocationType.OTHER, [portal_gun_2], 6),
}

vitrified_map_to_vitrified_door: dict[str, list[str]] = {
    "sp_a3_03": [vitrified_door_1_cave_johnson, vitrified_door_2_cave_johnson, vitrified_door_3_cave_johnson],
    "sp_a3_transition01": [vitrified_door_4_potatos, vitrified_door_5_potatos, vitrified_door_6_potatos]
}

all_locations_table: dict[str, Portal2LocationData] = map_complete_table.copy()
all_locations_table.update(cutscene_completion_table)

location_names_to_map_codes: dict[str, str] = {name: value.map_name for
                                               name, value in all_locations_table.items()}
map_codes_to_location_names: dict[str, str] = {value: key for key, value in location_names_to_map_codes.items()}

# all_locations_table.update(story_achievements_table)
all_locations_table.update(wheatley_monitor_table)
all_locations_table.update(item_location_table)
all_locations_table.update(ratman_den_locations_table)
all_locations_table.update(vitrified_door_locations_table)
# all_locations_table.update(achievements_table)

location_groups: dict[str, set[str]] = {
    "Chambers": {name for name in map_complete_table} | {name for name in cutscene_completion_table},
    "Wheatley Monitors": {name for name in wheatley_monitor_table},
    "Ratman Dens": {name for name in ratman_den_locations_table},
    "Pickups": {name for name in item_location_table}
}

# Alternate logic for speedrunners
speedrun_logic_table: dict[str, list[str]] = {
    # Chapter 1
    portal_carousel_completion: [button, floor_button],
    smooth_jazz_completion: [floor_button],
    cube_momentum_completion: [floor_button],
    future_starter_completion: [floor_button],
    incinerator_completion: [weighted_cube],
    # Chapter 2
    laser_intro_completion: [portal_gun_2],
    laser_stairs_completion: [portal_gun_2, floor_button],
    dual_lasers_completion: [portal_gun_2, laser, laser_catcher],
    laser_over_goo_completion: [portal_gun_2, floor_button],
    catapult_intro_completion: [portal_gun_2, floor_button],
    trust_fling_completion: [portal_gun_2, faith_plate, floor_button],
    pit_flings_completion: [portal_gun_2],
    fizzler_intro_completion: [portal_gun_2, laser, laser_catcher],
    # Chapter 3
    ricochet_completion: [portal_gun_2, weighted_cube, floor_button],
    bridge_intro_completion: [portal_gun_2, floor_button],
    bridge_the_gap_completion: [weighted_cube, button, floor_button],
    turret_intro_completion: [floor_button],
    laser_relays_completion: [laser_relays, laser, reflection_cube],
    turret_blocker_completion: [floor_button],
    laser_vs_turret_completion: [portal_gun_2],
    pull_the_rug_completion: [floor_button, weighted_cube, bridge, portal_gun_2],
    # Chapter 4
    column_blocker_completion: [portal_gun_2],
    laser_chaining_completion: [reflection_cube, laser, laser_relays],
    triple_laser_completion: [reflection_cube, portal_gun_2],
    jailbreak_completion: [portal_gun_2, button, weighted_cube],
    escape_completion: [],
    # Chapter 5
    turret_sabotage_completion: [portal_gun_2],
    neurotoxin_sabotage_completion: [portal_gun_2],
    core_completion: [turrets],
    # Chapter 6
    repulsion_intro_completion: [blue_gel, old_floor_button, portal_gun_2],
    bomb_flings_completion: [portal_gun_2, blue_gel, old_button],
    crazy_box_completion: [portal_gun_2, old_floor_button],
    # Chapter 7
    propulsion_intro_completion: [portal_gun_2],
    propulsion_flings_completion: [portal_gun_2, blue_gel],
    conversion_intro_completion: [portal_gun_2],
    three_gels_completion: [portal_gun_2, blue_gel],
    # Chapter 8
    funnel_intro_completion: [floor_button, funnel],
    ceiling_button_completion: [floor_button, frankenturret, button, portal_gun_2],
    wall_button_completion: [floor_button, funnel, portal_gun_2],
    polarity_completion: [portal_gun_2, funnel],
    funnel_catch_completion: [portal_gun_2],
    stop_the_box_completion: [floor_button, portal_gun_2],
    laser_catapult_completion: [portal_gun_2],
    laser_platform_completion: [portal_gun_2, funnel],
    propulsion_catch_completion: [floor_button, funnel],
    repulsion_polarity_completion: [turrets, button, blue_gel],
    # Chapter 9
    finale_1_completion: [portal_gun_2, frankenturret, faith_plate],
    finale_2_completion: [portal_gun_2],
    finale_3_completion: [portal_gun_2, funnel],
    finale_4_completion: [portal_gun_2, potatos, white_gel, adventure_core, space_core, fact_core],
}

sub_locations_in_maps: dict[str, list[str]] = {
    portal_gun_completion: [portal_gun_1],
    incinerator_completion: [portal_gun_2],
    potatos_completion: [potatos, vitrified_door_4_potatos, vitrified_door_5_potatos, vitrified_door_6_potatos],
    funnel_intro_completion: [wheatley_monitor_1_funnel_intro],
    ceiling_button_completion: [wheatley_monitor_2_ceiling_button],
    wall_button_completion: [wheatley_monitor_3_wall_button],
    polarity_completion: [wheatley_monitor_4_polarity],
    funnel_catch_completion: [wheatley_monitor_5_funnel_catch, wheatley_monitor_6_funnel_catch],
    stop_the_box_completion: [wheatley_monitor_7_stop_the_box],
    laser_catapult_completion: [wheatley_monitor_8_laser_catapult],
    laser_platform_completion: [wheatley_monitor_9_laser_platform],
    propulsion_catch_completion: [wheatley_monitor_10_propulsion_catch],
    repulsion_polarity_completion: [wheatley_monitor_11_repulsion_polarity],
    finale_3_completion: [wheatley_monitor_12_finale_3],
    smooth_jazz_completion: [ratman_den_1_smooth_jazz],
    dual_lasers_completion: [ratman_den_2_dual_lasers],
    trust_fling_completion: [ratman_den_3_trust_fling],
    bridge_intro_completion: [ratman_den_4_bridge_intro],
    bridge_the_gap_completion: [ratman_den_5_bridge_the_gap],
    laser_vs_turret_completion: [ratman_den_6_laser_vs_turret],
    pull_the_rug_completion: [ratman_den_7_pull_the_rug],
    cave_johnson_completion: [vitrified_door_1_cave_johnson, vitrified_door_2_cave_johnson, vitrified_door_3_cave_johnson],
}
