from typing import NamedTuple, Dict, Callable

from BaseClasses import Location, LocationProgressType, CollectionState
from .names import item_names as i
from .names import location_names as l
from .names import region_names as r
from .names import combat_names as c
from .items import BASE_ID
from .rules_helpers import can_fight, can_fight_all, can_burn, can_burn_underwater
from .combat import Difficulty

class FrogmonsterLocation(Location):
    game = "Frogmonster"

class FrogmonsterLocationData(NamedTuple):
    region: str
    id: int | None = None
    progress_type: LocationProgressType = LocationProgressType.DEFAULT
    access_rule: Callable[[int, Difficulty, CollectionState], bool] = lambda player, dif, state: True
    groups: list[str] = []

location_data_table: Dict[str, FrogmonsterLocationData] = {

    # Locations
    l.dash: FrogmonsterLocationData(
        region=r.marvins,
        id=BASE_ID + 0,
        access_rule=lambda player, dif, state: can_fight(c.marvin, player, dif, state)
    ),
    l.sticky_hands: FrogmonsterLocationData(
        region=r.outskirts,
        id=BASE_ID + 1,
        access_rule=lambda player, dif, state: can_fight_all([c.outskirts_arena_1, c.snake], player, dif, state) or state.can_reach(r.city, "Region", player)
    ),
    l.tongue_swing: FrogmonsterLocationData(
        region=r.forest_floor,
        id=BASE_ID + 2,
        access_rule=lambda player, dif, state: can_fight_all([c.forest_floor_arena_1, c.chroma], player, dif, state)
    ),
    l.runi_key: FrogmonsterLocationData(
        region=r.well,
        id=BASE_ID + 3,
        access_rule=lambda player, dif, state: can_fight_all([c.well_general_lower, c.dekula], player, dif, state)
    ),
    l.glowbug: FrogmonsterLocationData(
        region=r.bug,
        id=BASE_ID + 4
    ),
    l.frog: FrogmonsterLocationData(
        region=r.bug,
        id=BASE_ID + 5
    ),
    l.fly: FrogmonsterLocationData(
        region=r.bug,
        id=BASE_ID + 6
    ),
    l.dragonfly: FrogmonsterLocationData(
        region=r.bug,
        id=BASE_ID + 7
    ),
    l.eel: FrogmonsterLocationData(
        region=r.bug,
        id=BASE_ID + 8
    ),
    l.bass: FrogmonsterLocationData(
        region=r.bug,
        id=BASE_ID + 9
    ),
    l.blue_snack: FrogmonsterLocationData(
        region=r.bug,
        id=BASE_ID + 10
    ),
    l.purple_snack: FrogmonsterLocationData(
        region=r.bug,
        id=BASE_ID + 11
    ),
    l.magnet_roach: FrogmonsterLocationData(
        region=r.bug,
        id=BASE_ID + 12
    ),
    l.mushroll: FrogmonsterLocationData(
        region=r.bug,
        id=BASE_ID + 13
    ),
    l.mushfrog: FrogmonsterLocationData(
        region=r.bug,
        id=BASE_ID + 14
    ),
    l.beet: FrogmonsterLocationData(
        region=r.bug,
        id=BASE_ID + 15
    ),
    l.skater: FrogmonsterLocationData(
        region=r.bug,
        id=BASE_ID + 16
    ),
    l.soul_frog: FrogmonsterLocationData(
        region=r.bug,
        id=BASE_ID + 17
    ),
    l.river_fish: FrogmonsterLocationData(
        region=r.bug,
        id=BASE_ID + 18
    ),
    l.bird: FrogmonsterLocationData(
        region=r.bug,
        id=BASE_ID + 19
    ),
    l.leafbug: FrogmonsterLocationData(
        region=r.bug,
        id=BASE_ID + 20
    ),
    l.wormy: FrogmonsterLocationData(
        region=r.bug,
        id=BASE_ID + 21
    ),
    l.minnow: FrogmonsterLocationData(
        region=r.bug,
        id=BASE_ID + 22
    ),
    l.turtle: FrogmonsterLocationData(
        region=r.bug,
        id=BASE_ID + 23
    ),
    l.blue_jelly: FrogmonsterLocationData(
        region=r.bug,
        id=BASE_ID + 24
    ),
    l.roof_snail: FrogmonsterLocationData(
        region=r.bug,
        id=BASE_ID + 25
    ),
    l.crab: FrogmonsterLocationData(
        region=r.bug,
        id=BASE_ID + 26
    ),
    l.bridge_frog: FrogmonsterLocationData(
        region=r.bug,
        id=BASE_ID + 27
    ),
    l.cricket: FrogmonsterLocationData(
        region=r.bug,
        id=BASE_ID + 28
    ),
    l.spider: FrogmonsterLocationData(
        region=r.bug,
        id=BASE_ID + 29
    ),
    l.moth: FrogmonsterLocationData(
        region=r.bug,
        id=BASE_ID + 30
    ),
    l.ammofly: FrogmonsterLocationData(
        region=r.bug,
        id=BASE_ID + 31
    ),
    l.pecker: FrogmonsterLocationData(
        region=r.bug,
        id=BASE_ID + 32
    ),
    l.soul_fish: FrogmonsterLocationData(
        region=r.bug,
        id=BASE_ID + 33
    ),
    l.fog_fly: FrogmonsterLocationData(
        region=r.bug,
        id=BASE_ID + 34
    ),
    l.cicada: FrogmonsterLocationData(
        region=r.bug,
        id=BASE_ID + 35
    ),
    l.mantis: FrogmonsterLocationData(
        region=r.bug,
        id=BASE_ID + 36
    ),
    l.jungle_snack: FrogmonsterLocationData(
        region=r.bug,
        id=BASE_ID + 37
    ),
    l.gecko: FrogmonsterLocationData(
        region=r.bug,
        id=BASE_ID + 38
    ),
    l.bee: FrogmonsterLocationData(
        region=r.bug,
        id=BASE_ID + 39
    ),
    l.mushroom: FrogmonsterLocationData(
        region=r.bug,
        id=BASE_ID + 40
    ),
    l.tang: FrogmonsterLocationData(
        region=r.bug,
        id=BASE_ID + 41
    ),
    l.axolotyl: FrogmonsterLocationData(
        region=r.bug,
        id=BASE_ID + 42
    ),
    l.mite: FrogmonsterLocationData(
        region=r.bug,
        id=BASE_ID + 43
    ),
    l.health_1: FrogmonsterLocationData(
        region=r.outskirts,
        id=BASE_ID + 44,
        access_rule=lambda player, dif, state: can_fight(c.snake, player, dif, state)
    ),
    l.health_2: FrogmonsterLocationData(
        region=r.very_lost_swamp,
        id=BASE_ID + 45,
        access_rule=lambda player, dif, state: can_fight(c.yanoy, player, dif, state)
    ),
    l.health_3: FrogmonsterLocationData(
        region=r.hive,
        id=BASE_ID + 46,
        access_rule=lambda player, dif, state: state.has(i.tongue_swing, player) and can_fight_all([c.foraz, c.hive_general], player, dif, state)
    ),
    l.health_4: FrogmonsterLocationData(
        region=r.yellow_forest_town,
        id=BASE_ID + 47,
    ),
    l.health_5: FrogmonsterLocationData(
        region=r.yellow_forest_town,
        id=BASE_ID + 48,
    ),
    l.health_6: FrogmonsterLocationData(
        region=r.thickness,
        id=BASE_ID + 49,
        access_rule=lambda player, dif, state: state.can_reach(r.city, None, player) and can_fight_all([c.thickness_arena_1, c.djumbo], player, dif, state)
    ),
    l.mana_1: FrogmonsterLocationData(
        region=r.yellow_forest,
        id=BASE_ID + 50,
        access_rule=lambda player, dif, state: can_fight(c.limbs, player, dif, state)
    ),
    l.mana_2: FrogmonsterLocationData(
        region=r.thickness,
        id=BASE_ID + 51,
        access_rule=lambda player, dif, state: can_fight_all([c.djumbo, c.thickness_arena_1], player, dif, state)
    ),
    l.mana_3: FrogmonsterLocationData(
        region=r.city,
        id=BASE_ID + 52
    ),
    l.mana_4: FrogmonsterLocationData(
        region=r.city,
        id=BASE_ID + 53
    ),
    l.mana_5: FrogmonsterLocationData(
        region=r.workshop,
        id=BASE_ID + 54,
        access_rule=lambda player, dif, state: state.has_all([i.dash, i.sticky_hands], player) and can_fight(c.xoto, player, dif, state)
    ),
    l.mana_6: FrogmonsterLocationData(
        region=r.treetops,
        id=BASE_ID + 55,
        access_rule=lambda player, dif, state: state.has_all([i.sticky_hands, i.tongue_swing], player) and can_fight(c.treetops_arena_1, player, dif, state)
    ),
    l.reeder: FrogmonsterLocationData(
        region=r.lost_swamp,
        id=BASE_ID + 56
    ),
    l.machine_gun: FrogmonsterLocationData(
        region=r.marvins,
        id=BASE_ID + 57
    ),
    l.weepwood_bow: FrogmonsterLocationData(
        region=r.very_lost_swamp,
        id=BASE_ID + 58,
        access_rule=lambda player, dif, state: can_fight(c.yanoy, player, dif, state)
    ),
    l.finisher: FrogmonsterLocationData(
        region=r.yellow_forest_town,
        id=BASE_ID + 59,
        access_rule=lambda player, dif, state: state.has(i.eel_trophy, player)
    ),
    l.fire_fruit_juicer: FrogmonsterLocationData(
        region=r.old_road,
        id=BASE_ID + 60,
        access_rule= lambda player, dif, state: can_fight(c.valda, player, dif, state) and (
            (can_burn(state, player) and can_fight(c.old_road_general, player, dif, state)) or
            can_fight_all([c.old_road_arena_1, c.old_road_arena_2], player, dif, state)
        )
    ),
    l.gatling_gun: FrogmonsterLocationData(
        region=r.cicada_cove,
        id=BASE_ID + 61,
        access_rule= lambda player, dif, state: can_fight(c.tymbal, player, dif, state)  # You can get this earlier by killing supo, but don't 
    ),
    l.wooden_cannon: FrogmonsterLocationData(
        region=r.fog_garden,
        id=BASE_ID + 62,
        access_rule= lambda player, dif, state: can_fight_all([c.fog_garden_arena_1, c.hedgeward], player, dif, state)
    ),
    l.fireball: FrogmonsterLocationData(
        region=r.lost_swamp,
        id=BASE_ID + 63
    ),
    l.mushbomb: FrogmonsterLocationData(
        region=r.marvins,
        id=BASE_ID + 64
    ),
    l.sharp_shot: FrogmonsterLocationData(
        region=r.outskirts,
        id=BASE_ID + 65
    ),
    l.beans: FrogmonsterLocationData(
        region=r.yellow_forest_town,
        id=BASE_ID + 66
    ),
    l.zap: FrogmonsterLocationData(
        region=r.green_sea_key,
        id=BASE_ID + 67,
        access_rule=lambda player, dif, state: can_fight(c.green_sea_arena_3, player, dif, state)
    ),
    l.slam: FrogmonsterLocationData(
        region=r.fog_garden_key,
        id=BASE_ID + 68,
        access_rule=lambda player, dif, state: can_fight(c.fog_garden_arena_2, player, dif, state)
    ),
    l.hive: FrogmonsterLocationData(
        region=r.hive,
        id=BASE_ID + 69,
        access_rule=lambda player, dif, state: state.has(i.tongue_swing, player) and state.can_reach(r.city, None, player) and can_fight(c.foraz, player, dif, state)
    ),
    l.puff: FrogmonsterLocationData(
        region=r.treetops_key,
        id=BASE_ID + 70,
        access_rule=lambda player, dif, state: can_fight(c.treetops_arena_2, player, dif, state)
    ),
    l.bug_slot_1: FrogmonsterLocationData(
        region=r.yellow_forest,
        id=BASE_ID + 71,
        access_rule=lambda player, dif, state: can_fight(c.placeholder, player, dif, state)
    ),
    l.bug_slot_2: FrogmonsterLocationData(
        region=r.lost_swamp,
        id=BASE_ID + 72,
        access_rule=lambda player, dif, state: can_fight(c.groth, player, dif, state)
    ),
    l.bug_slot_3: FrogmonsterLocationData(
        region=r.city,
        id=BASE_ID + 73,
        access_rule=lambda player, dif, state: state.has_group_unique("Bug", player, 10)
    ),
    l.bug_slot_4: FrogmonsterLocationData(
        region=r.city,
        id=BASE_ID + 74,
        access_rule=lambda player, dif, state: state.has_group_unique("Bug", player, 20)
    ),
    l.bug_slot_5: FrogmonsterLocationData(
        region=r.city,
        id=BASE_ID + 75,
        access_rule=lambda player, dif, state: state.has_group_unique("Bug", player, 30)
    ),
    l.bug_slot_6: FrogmonsterLocationData(
        region=r.city,
        id=BASE_ID + 76,
        access_rule=lambda player, dif, state: state.has_group_unique("Bug", player, 40),
        progress_type=LocationProgressType.EXCLUDED # 40 bugs potentially being required is kinda miserable. Excluded for now.
    ),
    l.bug_slot_7: FrogmonsterLocationData(
        region=r.cicada_cove,
        id=BASE_ID + 77,
        access_rule=lambda player, dif, state: can_fight(c.tymbal, player, dif, state)
    ),
    l.metal_ore_1: FrogmonsterLocationData(
        region=r.lost_swamp,
        id=BASE_ID + 78
    ),
    l.metal_ore_2: FrogmonsterLocationData(
        region=r.marvins,
        id=BASE_ID + 79
    ),
    l.metal_ore_3: FrogmonsterLocationData(
        region=r.very_lost_swamp,
        id=BASE_ID + 80,
        access_rule=lambda player, dif, state: can_fight(c.very_lost_swamp_arena_1, player, dif, state)
    ),
    l.metal_ore_4: FrogmonsterLocationData(
        region=r.yellow_forest_town,
        id=BASE_ID + 81
    ),
    l.metal_ore_5: FrogmonsterLocationData(
        region=r.under_city,
        id=BASE_ID + 82,
        access_rule=lambda player, dif, state: state.has(i.dash, player)
    ),
    l.metal_ore_6: FrogmonsterLocationData(
        region=r.old_road,
        id=BASE_ID + 83,
        access_rule=lambda player, dif, state: 
            can_fight(c.old_road_arena_1, player, dif, state) or
            (can_fight_all([c.old_road_arena_2, c.valda], player, dif, state) and can_burn(state, player)),
    ),
    l.metal_ore_7: FrogmonsterLocationData(
        region=r.well,
        id=BASE_ID + 84,
        access_rule=lambda player, dif, state: can_fight(c.well_general_lower, player, dif, state)
    ),
    l.metal_ore_8: FrogmonsterLocationData(
        region=r.very_lost_swamp,
        id=BASE_ID + 85,
        access_rule=lambda player, dif, state: state.can_reach(r.city, None, player) and can_fight(c.very_lost_swamp_general, player, dif, state)
    ),
    l.metal_ore_9: FrogmonsterLocationData(
        region=r.fog_garden_key,
        id=BASE_ID + 86,
    ),
    l.metal_ore_10: FrogmonsterLocationData(
        region=r.forest_floor,
        id=BASE_ID + 87,
        access_rule=lambda player, dif, state: can_fight(c.forest_floor_arena_1, player, dif, state) and state.has_all([i.tongue_swing, i.sticky_hands], player)
    ),
    l.metal_ore_11: FrogmonsterLocationData(
        region=r.cicada_cove,
        id=BASE_ID + 88
    ),
    l.metal_ore_12: FrogmonsterLocationData(
        region=r.under_under_city,
        id=BASE_ID + 89,
        access_rule=lambda player, dif, state: can_burn(state, player) and can_fight(c.under_under_arena_1, player, dif, state)
    ),
    l.metal_ore_13: FrogmonsterLocationData(
        region=r.moridonos,
        id=BASE_ID + 90,
        access_rule=lambda player, dif, state: can_fight_all([c.moridonos_arena_1, c.moridonos_arena_2], player, dif, state)
    ),
    l.metal_ore_14: FrogmonsterLocationData(
        region=r.quarry,
        id=BASE_ID + 91
    ),
    l.metal_ore_15: FrogmonsterLocationData(
        region=r.rootden,
        id=BASE_ID + 92
    ),
    l.metal_ore_16: FrogmonsterLocationData(
        region=r.deep,
        id=BASE_ID + 93
    ),
    l.metal_ore_17: FrogmonsterLocationData(
        region=r.outskirts,
        id=BASE_ID + 94,
        access_rule=lambda player, dif, state: can_fight(c.borp, player, dif, state)
    ),
    l.metal_ore_18: FrogmonsterLocationData(
        region=r.forest_floor,
        id=BASE_ID + 95,
        access_rule=lambda player, dif, state: can_fight_all([c.mud, c.chroma], player, dif, state)
    ),
    l.metal_ore_19: FrogmonsterLocationData(
        region=r.old_road,
        id=BASE_ID + 96,
        access_rule=lambda player, dif, state: can_fight_all([c.valda, c.balsam], player, dif, state)
    ),
    l.eel_trophy: FrogmonsterLocationData(
        region=r.green_sea_after,
        id=BASE_ID + 97,
        access_rule=lambda player, dif, state: can_fight(c.eels, player, dif, state)
    ),
    l.eye_fragment: FrogmonsterLocationData(
        region=r.myzand,
        id=BASE_ID + 98
    ),
    l.key_1: FrogmonsterLocationData(
        region=r.yellow_forest_town,
        id=BASE_ID + 99
    ),
    l.key_2: FrogmonsterLocationData(
        region=r.thickness,
        id=BASE_ID + 100,
        access_rule=lambda player, dif, state: can_fight(c.thickness_general, player, dif, state)
    ),
    l.key_3: FrogmonsterLocationData(
        region=r.city,
        id=BASE_ID + 101
    ),
    l.smooth_stone_1: FrogmonsterLocationData(
        region=r.lost_swamp,
        id=BASE_ID + 102,
        access_rule=lambda player, dif, state: can_fight(c.groth, player, dif, state)
    ),
    l.smooth_stone_2: FrogmonsterLocationData(
        region=r.lost_swamp,
        id=BASE_ID + 103,
    ),
    l.smooth_stone_3: FrogmonsterLocationData(
        region=r.marvins,
        id=BASE_ID + 104,
        access_rule=lambda player, dif, state: can_fight(c.marvin_arena_1, player, dif, state)
    ),
    l.smooth_stone_4: FrogmonsterLocationData(
        region=r.outskirts,
        id=BASE_ID + 105,
        access_rule=lambda player, dif, state: can_fight_all([c.outskirts_arena_1, c.snake], player, dif, state)
    ),
    l.smooth_stone_5: FrogmonsterLocationData(
        region=r.green_sea_after,
        id=BASE_ID + 106,
        access_rule=lambda player, dif, state: can_burn_underwater(state, player)
    ),
    l.smooth_stone_6: FrogmonsterLocationData(
        region=r.old_road,
        id=BASE_ID + 107,
        access_rule=lambda player, dif, state: can_fight(c.old_road_general, player, dif, state)
    ),
#    l.smooth_stone_7: FrogmonsterLocationData(
#        region=r.well,
#        id=BASE_ID + 108
#    ), So this just doesn't exist???
    l.smooth_stone_8: FrogmonsterLocationData(
        region=r.forest_floor,
        id=BASE_ID + 109,
        access_rule=lambda player, dif, state: can_fight(c.forest_floor_general, player, dif, state)
    ),
    l.smooth_stone_9: FrogmonsterLocationData(
        region=r.under_under_city,
        id=BASE_ID + 110
    ),
    l.smooth_stone_10: FrogmonsterLocationData(
        region=r.reef,
        id=BASE_ID + 111,
        access_rule=lambda player, dif, state: can_fight(c.reef_arena_1, player, dif, state)
    ),
    l.smooth_stone_11: FrogmonsterLocationData(
        region=r.moridonos_layer_worm,
        id=BASE_ID + 112,
        access_rule=lambda player, dif, state: can_fight(c.moridonos_general, player, dif, state)
    ),
    l.smooth_stone_12: FrogmonsterLocationData(
        region=r.rootden,
        id=BASE_ID + 113,
        access_rule=lambda player, dif, state: can_fight(c.rootden_general, player, dif, state)
    ),
    l.square_rock_1: FrogmonsterLocationData(
        region=r.yellow_forest_side,
        id=BASE_ID + 114
    ),
    l.square_rock_2: FrogmonsterLocationData(
        region=r.outskirts,
        id=BASE_ID + 115,
        access_rule=lambda player, dif, state: can_fight(c.outskirts_arena_1, player, dif, state)
    ),
    l.square_rock_3: FrogmonsterLocationData(
        region=r.green_sea_key,
        id=BASE_ID + 116
    ),
    l.square_rock_4: FrogmonsterLocationData(
        region=r.old_wood,
        id=BASE_ID + 117,
        access_rule=lambda player, dif, state: can_fight(c.old_wood_arenas, player, dif, state) and state.has(i.dash, player)
    ),
    l.square_rock_5: FrogmonsterLocationData(
        region=r.hive,
        id=BASE_ID + 118,
        access_rule=lambda player, dif, state: can_fight(c.hive_general, player, dif, state)
    ),
    l.square_rock_6: FrogmonsterLocationData(
        region=r.city,
        id=BASE_ID + 119
    ),
    l.square_rock_7: FrogmonsterLocationData(
        region=r.treetops_key,
        id=BASE_ID + 120
    ),
    l.square_rock_8: FrogmonsterLocationData(
        region=r.temple_top,
        id=BASE_ID + 121
    ),
    l.square_rock_9: FrogmonsterLocationData(
        region=r.deep,
        id=BASE_ID + 122,
        access_rule=lambda player, dif, state: can_fight(c.deep_arena_1, player, dif, state)
    ),
    l.square_rock_10: FrogmonsterLocationData(
        region=r.estate,
        id=BASE_ID + 123,
        access_rule=lambda player, dif, state: state.has(i.wooden_cannon, player) and can_fight(c.estate_general, player, dif, state)
    ),
    l.dark_pebble_1: FrogmonsterLocationData(
        region=r.marvins,
        id=BASE_ID + 124,
    ),
    l.dark_pebble_2: FrogmonsterLocationData(
        region=r.yellow_forest,
        id=BASE_ID + 125
    ),
    l.dark_pebble_3: FrogmonsterLocationData(
        region=r.thickness,
        id=BASE_ID + 126,
        access_rule=lambda player, dif, state: can_fight(c.thickness_arena_1, player, dif, state)
    ),
    l.dark_pebble_4: FrogmonsterLocationData(
        region=r.city,  # I'm pretty sure this requires nothing other than advancing the Blue story in Lost Swamp -> City -> Undercity -> City. Maybe.
        id=BASE_ID + 127
    ),
    l.dark_pebble_5: FrogmonsterLocationData(
        region=r.under_city,
        id=BASE_ID + 128,
        access_rule=lambda player, dif, state: can_burn(state, player)
    ),
    l.dark_pebble_6: FrogmonsterLocationData(
        region=r.moridonos_warp,
        id=BASE_ID + 129,
        access_rule=lambda player, dif, state: can_fight(c.moridonos_general, player, dif, state)
    ),
    l.dark_pebble_7: FrogmonsterLocationData(
        region=r.city,
        id=BASE_ID + 130,
        access_rule=lambda player, dif, state: state.has(i.wooden_cannon, player)
    ),
    l.dark_pebble_8: FrogmonsterLocationData(
        region=r.barge_arena,
        id=BASE_ID + 131,
        access_rule=lambda player, dif, state: state.has_all([i.dash, i.tongue_swing], player) and can_fight(c.barge, player, dif, state)
    ),
    l.sparkling_gem_1: FrogmonsterLocationData(
        region=r.marvins,
        id=BASE_ID + 132,
        access_rule=lambda player, dif, state: state.has(i.sticky_hands, player) and can_fight(c.marvin_arena_1, player, dif, state)
    ),
    l.sparkling_gem_2: FrogmonsterLocationData(
        region=r.yellow_forest_town,
        id=BASE_ID + 133,
        access_rule=lambda player, dif, state: state.has(i.dash, player)
    ),
    l.sparkling_gem_3: FrogmonsterLocationData(
        region=r.well,
        id=BASE_ID + 134,
        access_rule=lambda player, dif, state: can_fight(c.well_general_upper, player, dif, state)
    ),
    l.sparkling_gem_4: FrogmonsterLocationData(
        region=r.city,
        id=BASE_ID + 135,
        access_rule=lambda player, dif, state: state.can_reach(l.bug_slot_7, "Location", player),
        progress_type=LocationProgressType.EXCLUDED # Possible to permanently miss this if you kill Supo, force excluded for now.
    ),
    l.sparkling_gem_5: FrogmonsterLocationData(
        region=r.temple_top,
        id=BASE_ID + 136
    ),
    l.sparkling_gem_6: FrogmonsterLocationData(
        region=r.estate,
        id=BASE_ID + 137,
        access_rule=lambda player, dif, state: can_fight(c.estate_general, player, dif, state)
    ),
    l.seedling_myzand_upgrade: FrogmonsterLocationData(
        region=r.orchus_tree,
        id=BASE_ID + 138,
        access_rule=lambda player, dif, state: can_fight(c.runi, player, dif, state)
    ),
    l.reeder_myzand_upgrade: FrogmonsterLocationData(
        region=r.barge_arena,
        id=BASE_ID + 139,
        access_rule=lambda player, dif, state: can_fight(c.barge, player, dif, state)
    ),
    l.machine_gun_myzand_upgrade: FrogmonsterLocationData(
        region=r.moridono_arena,
        id=BASE_ID + 140,
        access_rule=lambda player, dif, state: can_fight(c.moridono, player, dif, state)
    ),
    l.weepwood_bow_myzand_upgrade: FrogmonsterLocationData(
        region=r.krogar_arena,
        id=BASE_ID + 141,
        access_rule=lambda player, dif, state: can_fight(c.krogar, player, dif, state)
    ),
    l.finisher_myzand_upgrade: FrogmonsterLocationData(
        region=r.temple,
        id=BASE_ID + 142,
        access_rule=lambda player, dif, state: can_fight_all([c.door_crab, c.temple_general], player, dif, state)
    ),
    l.fire_fruit_juicer_myzand_upgrade: FrogmonsterLocationData(
        region=r.ridge,
        id=BASE_ID + 143,
        access_rule=lambda player, dif, state: can_fight(c.brothers, player, dif, state)
    ),
    l.gatling_gun_myzand_upgrade: FrogmonsterLocationData(
        region=r.rootden,
        id=BASE_ID + 144,
        access_rule=lambda player, dif, state: can_fight_all([c.zythida, c.rootden_general], player, dif, state)
    ),
    l.wooden_cannon_myzand_upgrade: FrogmonsterLocationData(
        region=r.temple_top,
        id=BASE_ID + 145,
        access_rule=lambda player, dif, state: can_fight(c.lazaro, player, dif, state)
    ),
    l.yellow_forest_puzzle: FrogmonsterLocationData(
        region=r.yellow_forest_town,
        id=BASE_ID + 146
    ),
    l.city_puzzle_1: FrogmonsterLocationData(
        region=r.city,
        id=BASE_ID + 147,
        access_rule=lambda player, dif, state: can_burn(state, player)
    ),
    l.city_puzzle_2: FrogmonsterLocationData(
        region=r.city,
        id=BASE_ID + 148,
    ),
    l.mansion_puzzle_1: FrogmonsterLocationData(
        region=r.estate,
        id=BASE_ID + 149,
        access_rule=lambda player, dif, state: can_fight(c.estate_general, player, dif, state)
    ),
    l.mansion_puzzle_2: FrogmonsterLocationData(
        region=r.estate,
        id=BASE_ID + 150,
        access_rule=lambda player, dif, state: can_fight(c.estate_general, player, dif, state)
    ),
    l.fog_garden_puzzle_1: FrogmonsterLocationData(
        region=r.fog_garden,
        id=BASE_ID + 151,
        access_rule=lambda player, dif, state: can_fight(c.fog_garden_arena_1, player, dif, state) and can_burn(state, player)
    ),
    l.fog_garden_puzzle_2: FrogmonsterLocationData(
        region=r.fog_garden,
        id=BASE_ID + 152,
        access_rule=lambda player, dif, state: can_fight(c.fog_garden_arena_1, player, dif, state) and can_burn(state, player)
    ),
    l.coin_chest_1: FrogmonsterLocationData(
        region=r.lost_swamp,
        id=BASE_ID + 153,
    ),
    l.coin_chest_2: FrogmonsterLocationData(
        region=r.yellow_forest,
        id=BASE_ID + 154,
        access_rule=lambda player, dif, state: can_fight(c.yellow_forest_arena_1, player, dif, state)
    ),
    l.coin_chest_3: FrogmonsterLocationData(
        region=r.thickness,
        id=BASE_ID + 155,
        access_rule=lambda player, dif, state: can_fight(c.thickness_arena_1, player, dif, state)
    ),
    l.coin_chest_4: FrogmonsterLocationData(
        region=r.well,
        id=BASE_ID + 156,
        access_rule=lambda player, dif, state: can_fight(c.well_general_lower, player, dif, state)
    ),
    l.coin_chest_5: FrogmonsterLocationData(
        region=r.well,
        id=BASE_ID + 157,
        access_rule=lambda player, dif, state: can_fight(c.well_general_upper, player, dif, state)
    ),
    l.coin_chest_6: FrogmonsterLocationData(
        region=r.very_lost_swamp,
        id=BASE_ID + 158,
        access_rule=lambda player, dif, state: can_fight(c.very_lost_swamp_general, player, dif, state)
    ),
    l.workshop_access: FrogmonsterLocationData(
        region=r.workshop,
        id=BASE_ID + 159,
        access_rule=lambda player, dif, state: state.can_reach(l.mana_5, "Location", player)
    ),
    l.orchus_key: FrogmonsterLocationData(
        region=r.orchus_tree,
        id=BASE_ID + 160,
        access_rule=lambda player, dif, state: can_fight(c.runi, player, dif, state)
    ),
    # Events
    l.goal: FrogmonsterLocationData(
        region=r.myzand,
        access_rule=lambda player, dif, state: can_fight_all([c.myzand_1, c.myzand_2], player, dif, state)
    ),
}

location_id_table = {name: data.id for name, data in location_data_table.items() if data.id is not None}
post_ridge_regions = ["Ridge:", "Under Under City:", "Reef:", "Moridono's Domain:", "Quarry:", "Rootden:", "Drywood:" "Deep:", "Temple:", "Myzand's Forest:", l.mite, l.axolotyl, l.mushroom, l.tang]
location_name_groups = {
    "Puzzles": {
        l.yellow_forest_puzzle,
        l.city_puzzle_1,
        l.city_puzzle_2,
        l.mansion_puzzle_1,
        l.mansion_puzzle_2,
        l.fog_garden_puzzle_1,
        l.fog_garden_puzzle_2
    },
    "Post-Ridge": {name for name in location_data_table.keys() if any(region in name for region in post_ridge_regions)},
}