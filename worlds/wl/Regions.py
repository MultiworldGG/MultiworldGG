import typing

from BaseClasses import MultiWorld, Region, Entrance, CollectionState
from .Locations import WLLocation, unlock_locations, level_location_table
from .Levels import level_info_dict
from .Names import LocationName, ItemName
from .Blocks import block_info_dict
from .Items import powerup_order, course_unlock_names
from worlds.generic.Rules import add_rule, set_rule


def can_defeat_final_boss(
    player, state: CollectionState, world: MultiWorld, options
) -> bool:
    return state.has(ItemName.boss_token, player, options.bosses_required.value)


def can_powerup(player, state: CollectionState, powerup: str) -> bool:
    index = powerup_order.index(powerup)
    return state.has(powerup, player) or state.has(
        ItemName.progressive_powerup, player, index + 1
    ) or (
        state.multiworld.worlds[player].options.get_previous_powerups
        and state.has_any(powerup_order[index + 1:], player)
    )


def can_garlic(player, state: CollectionState) -> bool:
    return can_powerup(player, state, ItemName.wario_garlic)


def can_bull(player, state: CollectionState) -> bool:
    return can_powerup(player, state, ItemName.wario_bull)


def can_dragon(player, state: CollectionState) -> bool:
    return can_powerup(player, state, ItemName.wario_dragon)


def can_jet(player, state: CollectionState) -> bool:
    return can_powerup(player, state, ItemName.wario_jet)


def can_create_coin(player, state: CollectionState) -> bool:
    return state.has(ItemName.wario_createcoin, player)


def can_climb(player, state: CollectionState) -> bool:
    return state.has(ItemName.wario_climb, player)


def can_highjump(player, state: CollectionState) -> bool:
    return state.has(ItemName.wario_highjump, player)


def can_duck(player, state: CollectionState) -> bool:
    return state.has(ItemName.wario_duck, player)


def can_dash(player, state: CollectionState) -> bool:
    return state.has(ItemName.wario_dash, player) and (
        can_garlic(player, state) or can_bull(player, state)
    )


def can_open_treasure(player, state: CollectionState) -> bool:
    return (
        can_jet(player, state) or can_dragon(player, state) or can_dash(player, state)
    )


def can_hit_groundblock(player, state: CollectionState) -> bool:
    return (
        can_jet(player, state)
        or (can_dragon(player, state) and can_duck(player, state))
        or can_dash(player, state)
    )


def can_hit_elevated_groundblock(player, state: CollectionState) -> bool:
    return (
        can_jet(player, state) or can_dragon(player, state) or can_dash(player, state)
    )


def can_grow(player, state: CollectionState) -> bool:
    return (
        can_garlic(player, state)
        or can_bull(player, state)
        or can_dragon(player, state)
        or can_jet(player, state)
    )


def create_regions(world, player: int, options, active_locations):
    menu_region = create_region(world, player, active_locations, "Menu", None)

    overworld_region_locations = []
    overworld_region = create_region(
        world,
        player,
        active_locations,
        LocationName.overworld_region,
        overworld_region_locations,
    )

    # Rice Beach
    ricebeach_region = create_region(
        world, player, active_locations, LocationName.ricebeach_region, None
    )

    ricebeach_1_tile = create_region(
        world, player, active_locations, LocationName.ricebeach_1_tile, None
    )
    ricebeach_1_region = create_region(
        world, player, active_locations, LocationName.ricebeach_1_region, None
    )
    ricebeach_1_exit_1 = create_region(
        world,
        player,
        active_locations,
        LocationName.ricebeach_1_exit_1,
        [LocationName.ricebeach_1_exit_1],
    )

    ricebeach_2_tile = create_region(
        world, player, active_locations, LocationName.ricebeach_2_tile, None
    )
    ricebeach_2_region = create_region(
        world, player, active_locations, LocationName.ricebeach_2_region, None
    )
    ricebeach_2_exit_1 = create_region(
        world,
        player,
        active_locations,
        LocationName.ricebeach_2_exit_1,
        [LocationName.ricebeach_2_exit_1],
    )

    ricebeach_3_tile = create_region(
        world, player, active_locations, LocationName.ricebeach_3_tile, None
    )
    ricebeach_3_region = create_region(
        world, player, active_locations, LocationName.ricebeach_3_region, None
    )
    ricebeach_3_exit_1 = create_region(
        world,
        player,
        active_locations,
        LocationName.ricebeach_3_exit_1,
        [LocationName.ricebeach_3_exit_1],
    )
    ricebeach_3_exit_2 = create_region(
        world,
        player,
        active_locations,
        LocationName.ricebeach_3_exit_2,
        [LocationName.ricebeach_3_exit_2],
    )

    ricebeach_4_tile = create_region(
        world, player, active_locations, LocationName.ricebeach_4_tile, None
    )
    ricebeach_4_region = create_region(
        world, player, active_locations, LocationName.ricebeach_4_region, None
    )
    ricebeach_4_exit_1 = create_region(
        world,
        player,
        active_locations,
        LocationName.ricebeach_4_exit_1,
        [LocationName.ricebeach_4_exit_1],
    )

    ricebeach_5_tile = create_region(
        world, player, active_locations, LocationName.ricebeach_5_tile, None
    )
    ricebeach_5_region = create_region(
        world, player, active_locations, LocationName.ricebeach_5_region, None
    )
    # ricebeach_5_exit_1 = create_region(world, player, active_locations, LocationName.ricebeach_5_exit_1,[LocationName.ricebeach_5_exit_1, LocationName.ricebeach_boss])
    ricebeach_boss = create_region(
        world,
        player,
        active_locations,
        LocationName.ricebeach_boss,
        [LocationName.ricebeach_boss, LocationName.ricebeach_boss_item],
    )

    ricebeach_6_tile = create_region(
        world, player, active_locations, LocationName.ricebeach_6_tile, None
    )
    ricebeach_6_region = create_region(
        world, player, active_locations, LocationName.ricebeach_6_region, None
    )
    ricebeach_6_exit_1 = create_region(
        world,
        player,
        active_locations,
        LocationName.ricebeach_6_exit_1,
        [LocationName.ricebeach_6_exit_1],
    )

    # Mt. Teapot
    mtteapot_region = create_region(
        world, player, active_locations, LocationName.mtteapot_region, None
    )

    mtteapot_7_tile = create_region(
        world, player, active_locations, LocationName.mtteapot_7_tile, None
    )
    mtteapot_7_region = create_region(
        world, player, active_locations, LocationName.mtteapot_7_region, None
    )
    mtteapot_7_exit_1 = create_region(
        world,
        player,
        active_locations,
        LocationName.mtteapot_7_exit_1,
        [LocationName.mtteapot_7_exit_1],
    )

    mtteapot_8_tile = create_region(
        world, player, active_locations, LocationName.mtteapot_8_tile, None
    )
    mtteapot_8_region = create_region(
        world, player, active_locations, LocationName.mtteapot_8_region, None
    )
    mtteapot_8_exit_1 = create_region(
        world,
        player,
        active_locations,
        LocationName.mtteapot_8_exit_1,
        [LocationName.mtteapot_8_exit_1],
    )
    mtteapot_8_exit_2 = create_region(
        world,
        player,
        active_locations,
        LocationName.mtteapot_8_exit_2,
        [LocationName.mtteapot_8_exit_2],
    )

    mtteapot_9_tile = create_region(
        world, player, active_locations, LocationName.mtteapot_9_tile, None
    )
    mtteapot_9_region = create_region(
        world, player, active_locations, LocationName.mtteapot_9_region, None
    )
    mtteapot_9_exit_1 = create_region(
        world,
        player,
        active_locations,
        LocationName.mtteapot_9_exit_1,
        [LocationName.mtteapot_9_exit_1],
    )

    mtteapot_10_tile = create_region(
        world, player, active_locations, LocationName.mtteapot_10_tile, None
    )
    mtteapot_10_region = create_region(
        world, player, active_locations, LocationName.mtteapot_10_region, None
    )
    mtteapot_10_exit_1 = create_region(
        world,
        player,
        active_locations,
        LocationName.mtteapot_10_exit_1,
        [LocationName.mtteapot_10_exit_1],
    )

    mtteapot_11_tile = create_region(
        world, player, active_locations, LocationName.mtteapot_11_tile, None
    )
    mtteapot_11_region = create_region(
        world, player, active_locations, LocationName.mtteapot_11_region, None
    )
    mtteapot_11_exit_1 = create_region(
        world,
        player,
        active_locations,
        LocationName.mtteapot_11_exit_1,
        [LocationName.mtteapot_11_exit_1],
    )

    mtteapot_12_tile = create_region(
        world, player, active_locations, LocationName.mtteapot_12_tile, None
    )
    mtteapot_12_region = create_region(
        world, player, active_locations, LocationName.mtteapot_12_region, None
    )
    mtteapot_12_exit_1 = create_region(
        world,
        player,
        active_locations,
        LocationName.mtteapot_12_exit_1,
        [LocationName.mtteapot_12_exit_1],
    )

    mtteapot_13_tile = create_region(
        world, player, active_locations, LocationName.mtteapot_13_tile, None
    )
    mtteapot_13_region = create_region(
        world, player, active_locations, LocationName.mtteapot_13_region, None
    )
    # mtteapot_13_exit_1 = create_region(world, player, active_locations, LocationName.mtteapot_13_exit_1,[LocationName.mtteapot_13_exit_1, LocationName.mtteapot_boss])
    mtteapot_boss = create_region(
        world,
        player,
        active_locations,
        LocationName.mtteapot_boss,
        [LocationName.mtteapot_boss, LocationName.mtteapot_boss_item],
    )

    # Sherbet Land
    sherbetland_region = create_region(
        world, player, active_locations, LocationName.sherbetland_region, None
    )

    sherbetland_14_tile = create_region(
        world, player, active_locations, LocationName.sherbetland_14_tile, None
    )
    sherbetland_14_region = create_region(
        world, player, active_locations, LocationName.sherbetland_14_region, None
    )
    sherbetland_14_exit_1 = create_region(
        world,
        player,
        active_locations,
        LocationName.sherbetland_14_exit_1,
        [LocationName.sherbetland_14_exit_1],
    )

    sherbetland_15_tile = create_region(
        world, player, active_locations, LocationName.sherbetland_15_tile, None
    )
    sherbetland_15_region = create_region(
        world, player, active_locations, LocationName.sherbetland_15_region, None
    )
    sherbetland_15_exit_1 = create_region(
        world,
        player,
        active_locations,
        LocationName.sherbetland_15_exit_1,
        [LocationName.sherbetland_15_exit_1],
    )
    sherbetland_15_exit_2 = create_region(
        world,
        player,
        active_locations,
        LocationName.sherbetland_15_exit_2,
        [LocationName.sherbetland_15_exit_2],
    )

    sherbetland_16_tile = create_region(
        world, player, active_locations, LocationName.sherbetland_16_tile, None
    )
    sherbetland_16_region = create_region(
        world, player, active_locations, LocationName.sherbetland_16_region, None
    )
    # leads to 19
    sherbetland_16_exit_1 = create_region(
        world,
        player,
        active_locations,
        LocationName.sherbetland_16_exit_1,
        [LocationName.sherbetland_16_exit_1],
    )
    # leads to 18
    sherbetland_16_exit_2 = create_region(
        world,
        player,
        active_locations,
        LocationName.sherbetland_16_exit_2,
        [LocationName.sherbetland_16_exit_2],
    )

    sherbetland_17_tile = create_region(
        world, player, active_locations, LocationName.sherbetland_17_tile, None
    )
    sherbetland_17_region = create_region(
        world, player, active_locations, LocationName.sherbetland_17_region, None
    )
    sherbetland_17_exit_1 = create_region(
        world,
        player,
        active_locations,
        LocationName.sherbetland_17_exit_1,
        [LocationName.sherbetland_17_exit_1],
    )

    sherbetland_18_tile = create_region(
        world, player, active_locations, LocationName.sherbetland_18_tile, None
    )
    sherbetland_18_region = create_region(
        world, player, active_locations, LocationName.sherbetland_18_region, None
    )
    sherbetland_18_exit_1 = create_region(
        world,
        player,
        active_locations,
        LocationName.sherbetland_18_exit_1,
        [LocationName.sherbetland_18_exit_1],
    )

    sherbetland_19_tile = create_region(
        world, player, active_locations, LocationName.sherbetland_19_tile, None
    )
    sherbetland_19_region = create_region(
        world, player, active_locations, LocationName.sherbetland_19_region, None
    )
    # sherbetland_19_exit_1 = create_region(world, player, active_locations, LocationName.sherbetland_19_exit_1,[LocationName.sherbetland_19_exit_1, LocationName.sherbetland_boss])
    sherbetland_boss = create_region(
        world,
        player,
        active_locations,
        LocationName.sherbetland_boss,
        [LocationName.sherbetland_boss, LocationName.sherbetland_boss_item],
    )

    # Stove Canyon
    stovecanyon_region = create_region(
        world, player, active_locations, LocationName.stovecanyon_region, None
    )

    stovecanyon_20_tile = create_region(
        world, player, active_locations, LocationName.stovecanyon_20_tile, None
    )
    stovecanyon_20_region = create_region(
        world, player, active_locations, LocationName.stovecanyon_20_region, None
    )
    stovecanyon_20_exit_1 = create_region(
        world,
        player,
        active_locations,
        LocationName.stovecanyon_20_exit_1,
        [LocationName.stovecanyon_20_exit_1],
    )

    stovecanyon_21_tile = create_region(
        world, player, active_locations, LocationName.stovecanyon_21_tile, None
    )
    stovecanyon_21_region = create_region(
        world, player, active_locations, LocationName.stovecanyon_21_region, None
    )
    stovecanyon_21_exit_1 = create_region(
        world,
        player,
        active_locations,
        LocationName.stovecanyon_21_exit_1,
        [LocationName.stovecanyon_21_exit_1],
    )

    stovecanyon_22_tile = create_region(
        world, player, active_locations, LocationName.stovecanyon_22_tile, None
    )
    stovecanyon_22_region = create_region(
        world, player, active_locations, LocationName.stovecanyon_22_region, None
    )
    stovecanyon_22_exit_1 = create_region(
        world,
        player,
        active_locations,
        LocationName.stovecanyon_22_exit_1,
        [LocationName.stovecanyon_22_exit_1],
    )

    stovecanyon_23_tile = create_region(
        world, player, active_locations, LocationName.stovecanyon_23_tile, None
    )
    stovecanyon_23_region = create_region(
        world, player, active_locations, LocationName.stovecanyon_23_region, None
    )
    stovecanyon_23_exit_1 = create_region(
        world,
        player,
        active_locations,
        LocationName.stovecanyon_23_exit_1,
        [LocationName.stovecanyon_23_exit_1],
    )
    stovecanyon_23_exit_2 = create_region(
        world,
        player,
        active_locations,
        LocationName.stovecanyon_23_exit_2,
        [LocationName.stovecanyon_23_exit_2],
    )

    stovecanyon_24_tile = create_region(
        world, player, active_locations, LocationName.stovecanyon_24_tile, None
    )
    stovecanyon_24_region = create_region(
        world, player, active_locations, LocationName.stovecanyon_24_region, None
    )
    stovecanyon_24_exit_1 = create_region(
        world,
        player,
        active_locations,
        LocationName.stovecanyon_24_exit_1,
        [LocationName.stovecanyon_24_exit_1],
    )

    stovecanyon_25_tile = create_region(
        world, player, active_locations, LocationName.stovecanyon_25_tile, None
    )
    stovecanyon_25_region = create_region(
        world, player, active_locations, LocationName.stovecanyon_25_region, None
    )
    # stovecanyon_25_exit_1 = create_region(world, player, active_locations, LocationName.stovecanyon_25_exit_1,[LocationName.stovecanyon_25_exit_1, LocationName.stovecanyon_boss])
    stovecanyon_boss = create_region(
        world,
        player,
        active_locations,
        LocationName.stovecanyon_boss,
        [LocationName.stovecanyon_boss, LocationName.stovecanyon_boss_item],
    )

    # SS Teacup
    ssteacup_region = create_region(
        world, player, active_locations, LocationName.ssteacup_region, None
    )

    ssteacup_26_tile = create_region(
        world, player, active_locations, LocationName.ssteacup_26_tile, None
    )
    ssteacup_26_region = create_region(
        world, player, active_locations, LocationName.ssteacup_26_region, None
    )
    ssteacup_26_exit_1 = create_region(
        world,
        player,
        active_locations,
        LocationName.ssteacup_26_exit_1,
        [LocationName.ssteacup_26_exit_1],
    )

    ssteacup_27_tile = create_region(
        world, player, active_locations, LocationName.ssteacup_27_tile, None
    )
    ssteacup_27_region = create_region(
        world, player, active_locations, LocationName.ssteacup_27_region, None
    )
    ssteacup_27_exit_1 = create_region(
        world,
        player,
        active_locations,
        LocationName.ssteacup_27_exit_1,
        [LocationName.ssteacup_27_exit_1],
    )

    ssteacup_28_tile = create_region(
        world, player, active_locations, LocationName.ssteacup_28_tile, None
    )
    ssteacup_28_region = create_region(
        world, player, active_locations, LocationName.ssteacup_28_region, None
    )
    ssteacup_28_exit_1 = create_region(
        world,
        player,
        active_locations,
        LocationName.ssteacup_28_exit_1,
        [LocationName.ssteacup_28_exit_1],
    )

    ssteacup_29_tile = create_region(
        world, player, active_locations, LocationName.ssteacup_29_tile, None
    )
    ssteacup_29_region = create_region(
        world, player, active_locations, LocationName.ssteacup_29_region, None
    )
    ssteacup_29_exit_1 = create_region(
        world,
        player,
        active_locations,
        LocationName.ssteacup_29_exit_1,
        [LocationName.ssteacup_29_exit_1],
    )

    ssteacup_30_tile = create_region(
        world, player, active_locations, LocationName.ssteacup_30_tile, None
    )
    ssteacup_30_region = create_region(
        world, player, active_locations, LocationName.ssteacup_30_region, None
    )
    # ssteacup_30_exit_1 = create_region(world, player, active_locations, LocationName.ssteacup_30_exit_1,[LocationName.ssteacup_30_exit_1, LocationName.ssteacup_boss])
    ssteacup_boss = create_region(
        world,
        player,
        active_locations,
        LocationName.ssteacup_boss,
        [LocationName.ssteacup_boss, LocationName.ssteacup_boss_item],
    )

    # Parsley Woods
    parsleywoods_region = create_region(
        world, player, active_locations, LocationName.parsleywoods_region, None
    )

    parsleywoods_31_tile = create_region(
        world, player, active_locations, LocationName.parsleywoods_31_tile, None
    )
    parsleywoods_31_region = create_region(
        world, player, active_locations, LocationName.parsleywoods_31_region, None
    )
    parsleywoods_31_exit_1 = create_region(
        world,
        player,
        active_locations,
        LocationName.parsleywoods_31_exit_1,
        [LocationName.parsleywoods_31_exit_1],
    )

    parsleywoods_32_tile = create_region(
        world, player, active_locations, LocationName.parsleywoods_32_tile, None
    )
    parsleywoods_32_region = create_region(
        world, player, active_locations, LocationName.parsleywoods_32_region, None
    )
    parsleywoods_32_exit_1 = create_region(
        world,
        player,
        active_locations,
        LocationName.parsleywoods_32_exit_1,
        [LocationName.parsleywoods_32_exit_1],
    )

    parsleywoods_33_tile = create_region(
        world, player, active_locations, LocationName.parsleywoods_33_tile, None
    )
    parsleywoods_33_region = create_region(
        world, player, active_locations, LocationName.parsleywoods_33_region, None
    )
    parsleywoods_33_exit_1 = create_region(
        world,
        player,
        active_locations,
        LocationName.parsleywoods_33_exit_1,
        [LocationName.parsleywoods_33_exit_1],
    )

    parsleywoods_34_tile = create_region(
        world, player, active_locations, LocationName.parsleywoods_34_tile, None
    )
    parsleywoods_34_region = create_region(
        world, player, active_locations, LocationName.parsleywoods_34_region, None
    )
    parsleywoods_34_exit_1 = create_region(
        world,
        player,
        active_locations,
        LocationName.parsleywoods_34_exit_1,
        [LocationName.parsleywoods_34_exit_1],
    )

    parsleywoods_35_tile = create_region(
        world, player, active_locations, LocationName.parsleywoods_35_tile, None
    )
    parsleywoods_35_region = create_region(
        world, player, active_locations, LocationName.parsleywoods_35_region, None
    )
    parsleywoods_35_exit_1 = create_region(
        world,
        player,
        active_locations,
        LocationName.parsleywoods_35_exit_1,
        [LocationName.parsleywoods_35_exit_1],
    )

    parsleywoods_36_tile = create_region(
        world, player, active_locations, LocationName.parsleywoods_36_tile, None
    )
    parsleywoods_36_region = create_region(
        world, player, active_locations, LocationName.parsleywoods_36_region, None
    )
    # parsleywoods_36_exit_1 = create_region(world, player, active_locations, LocationName.parsleywoods_36_exit_1,[LocationName.parsleywoods_36_exit_1, LocationName.parsleywoods_boss])
    parsleywoods_boss = create_region(
        world,
        player,
        active_locations,
        LocationName.parsleywoods_boss,
        [LocationName.parsleywoods_boss, LocationName.parsleywoods_boss_item],
    )

    # Syrup Castle
    syrupcastle_region = create_region(
        world, player, active_locations, LocationName.syrupcastle_region, None
    )

    syrupcastle_37_tile = create_region(
        world, player, active_locations, LocationName.syrupcastle_37_tile, None
    )
    syrupcastle_37_region = create_region(
        world, player, active_locations, LocationName.syrupcastle_37_region, None
    )
    syrupcastle_37_exit_1 = create_region(
        world,
        player,
        active_locations,
        LocationName.syrupcastle_37_exit_1,
        [LocationName.syrupcastle_37_exit_1],
    )

    syrupcastle_38_tile = create_region(
        world, player, active_locations, LocationName.syrupcastle_38_tile, None
    )
    syrupcastle_38_region = create_region(
        world, player, active_locations, LocationName.syrupcastle_38_region, None
    )
    syrupcastle_38_exit_1 = create_region(
        world,
        player,
        active_locations,
        LocationName.syrupcastle_38_exit_1,
        [LocationName.syrupcastle_38_exit_1],
    )

    syrupcastle_39_tile = create_region(
        world, player, active_locations, LocationName.syrupcastle_39_tile, None
    )
    syrupcastle_39_region = create_region(
        world, player, active_locations, LocationName.syrupcastle_39_region, None
    )
    syrupcastle_39_exit_1 = create_region(
        world,
        player,
        active_locations,
        LocationName.syrupcastle_39_exit_1,
        [LocationName.syrupcastle_39_exit_1],
    )

    syrupcastle_40_tile = create_region(
        world, player, active_locations, LocationName.syrupcastle_40_tile, None
    )
    syrupcastle_40_region = create_region(
        world, player, active_locations, LocationName.syrupcastle_40_region, None
    )
    # syrupcastle_40_exit_1 = create_region(world, player, active_locations, LocationName.syrupcastle_40_exit_1,[LocationName.syrupcastle_40_exit_1])
    syrupcastle_boss_locations = []
    syrupcastle_boss = create_region(
        world,
        player,
        active_locations,
        LocationName.syrupcastle_boss,
        syrupcastle_boss_locations,
    )

    world.regions += [
        menu_region,
        overworld_region,
        ricebeach_region,
        ricebeach_1_tile,
        ricebeach_1_region,
        ricebeach_1_exit_1,
        ricebeach_2_tile,
        ricebeach_2_region,
        ricebeach_2_exit_1,
        ricebeach_3_tile,
        ricebeach_3_region,
        ricebeach_3_exit_1,
        ricebeach_3_exit_2,
        ricebeach_4_tile,
        ricebeach_4_region,
        ricebeach_4_exit_1,
        ricebeach_5_tile,
        ricebeach_5_region,
        # ricebeach_5_exit_1,
        ricebeach_6_tile,
        ricebeach_6_region,
        ricebeach_6_exit_1,
        ricebeach_boss,
        mtteapot_region,
        mtteapot_7_tile,
        mtteapot_7_region,
        mtteapot_7_exit_1,
        mtteapot_8_tile,
        mtteapot_8_region,
        mtteapot_8_exit_1,
        mtteapot_8_exit_2,
        mtteapot_9_tile,
        mtteapot_9_region,
        mtteapot_9_exit_1,
        mtteapot_10_tile,
        mtteapot_10_region,
        mtteapot_10_exit_1,
        mtteapot_11_tile,
        mtteapot_11_region,
        mtteapot_11_exit_1,
        mtteapot_12_tile,
        mtteapot_12_region,
        mtteapot_12_exit_1,
        mtteapot_13_tile,
        mtteapot_13_region,
        # mtteapot_13_exit_1,
        mtteapot_boss,
        sherbetland_region,
        sherbetland_14_tile,
        sherbetland_14_region,
        sherbetland_14_exit_1,
        sherbetland_15_tile,
        sherbetland_15_region,
        sherbetland_15_exit_1,
        sherbetland_15_exit_2,
        sherbetland_16_tile,
        sherbetland_16_region,
        sherbetland_16_exit_1,
        sherbetland_16_exit_2,
        sherbetland_17_tile,
        sherbetland_17_region,
        sherbetland_17_exit_1,
        sherbetland_18_tile,
        sherbetland_18_region,
        sherbetland_18_exit_1,
        sherbetland_19_tile,
        sherbetland_19_region,
        # sherbetland_19_exit_1,
        sherbetland_boss,
        stovecanyon_region,
        stovecanyon_20_tile,
        stovecanyon_20_region,
        stovecanyon_20_exit_1,
        stovecanyon_21_tile,
        stovecanyon_21_region,
        stovecanyon_21_exit_1,
        stovecanyon_22_tile,
        stovecanyon_22_region,
        stovecanyon_22_exit_1,
        stovecanyon_23_tile,
        stovecanyon_23_region,
        stovecanyon_23_exit_1,
        stovecanyon_23_exit_2,
        stovecanyon_24_tile,
        stovecanyon_24_region,
        stovecanyon_24_exit_1,
        stovecanyon_25_tile,
        stovecanyon_25_region,
        # stovecanyon_25_exit_1,
        stovecanyon_boss,
        ssteacup_region,
        ssteacup_26_tile,
        ssteacup_26_region,
        ssteacup_26_exit_1,
        ssteacup_27_tile,
        ssteacup_27_region,
        ssteacup_27_exit_1,
        ssteacup_28_tile,
        ssteacup_28_region,
        ssteacup_28_exit_1,
        ssteacup_29_tile,
        ssteacup_29_region,
        ssteacup_29_exit_1,
        ssteacup_30_tile,
        ssteacup_30_region,
        # ssteacup_30_exit_1,
        ssteacup_boss,
        parsleywoods_region,
        parsleywoods_31_tile,
        parsleywoods_31_region,
        parsleywoods_31_exit_1,
        parsleywoods_32_tile,
        parsleywoods_32_region,
        parsleywoods_32_exit_1,
        parsleywoods_33_tile,
        parsleywoods_33_region,
        parsleywoods_33_exit_1,
        parsleywoods_34_tile,
        parsleywoods_34_region,
        parsleywoods_34_exit_1,
        parsleywoods_35_tile,
        parsleywoods_35_region,
        parsleywoods_35_exit_1,
        parsleywoods_36_tile,
        parsleywoods_36_region,
        # parsleywoods_36_exit_1,
        parsleywoods_boss,
        syrupcastle_region,
        syrupcastle_37_tile,
        syrupcastle_37_region,
        syrupcastle_37_exit_1,
        syrupcastle_38_tile,
        syrupcastle_38_region,
        syrupcastle_38_exit_1,
        syrupcastle_39_tile,
        syrupcastle_39_region,
        syrupcastle_39_exit_1,
        syrupcastle_40_tile,
        syrupcastle_40_region,
        # genie_region,
        syrupcastle_boss,
    ]
    goal_region = overworld_region if options.goal == "garlic_hunt" else syrupcastle_boss
    goal_name = LocationName.garlic_goal if options.goal == "garlic_hunt" else LocationName.syrupcastle_boss
    goal_region.locations.append(WLLocation(player, goal_name, None, goal_region))

    # Handle blocksanity logic
    if options.blocksanity == 1:
        for block_index in block_info_dict:
            level_id = block_index >> 16
            block_data = block_info_dict[block_index]
            level_data = level_info_dict[level_id]
            add_location_to_region(
                world,
                player,
                active_locations,
                level_data.levelName,
                block_data.blockName,
            )
        # Handle blocks that require logic for access
        # Rice Beach Blocks
        add_rule(
            world.get_location(LocationName.ricebeach_1_block3, player),
            lambda state: can_hit_groundblock(player, state),
        )
        add_rule(
            world.get_location(LocationName.ricebeach_1_block10, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.ricebeach_1_block11, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.ricebeach_1_block12, player),
            lambda state: (
                (
                    state.can_reach(LocationName.ricebeach_boss, "", player)
                    and can_dash(player, state)
                    and can_climb(player, state)
                )
                or (can_bull(player, state) and can_dash(player, state))
                or (can_dragon(player, state) and can_duck(player, state))
            ),
        )
        add_rule(
            world.get_location(LocationName.ricebeach_1_block18, player),
            lambda state: can_climb(player, state)
            and (
                (can_highjump(player, state) and can_grow(player, state))
                or state.can_reach(LocationName.ricebeach_boss, "", player)
            ),
        )
        add_rule(
            world.get_location(LocationName.ricebeach_2_block2, player),
            lambda state: can_hit_groundblock(player, state)
            or can_dragon(player, state),
        )
        add_rule(
            world.get_location(LocationName.ricebeach_2_block4, player),
            lambda state: can_hit_elevated_groundblock(player, state)
            or can_bull(player, state),
        )
        add_rule(
            world.get_location(LocationName.ricebeach_2_block5, player),
            lambda state: can_hit_elevated_groundblock(player, state)
            or can_bull(player, state),
        )
        add_rule(
            world.get_location(LocationName.ricebeach_2_block19, player),
            lambda state: can_climb(player, state)
            or can_hit_elevated_groundblock(player, state)
            or can_bull(player, state),
        )
        add_rule(
            world.get_location(LocationName.ricebeach_3_block4, player),
            lambda state: (
                (can_dragon(player, state) and can_duck(player, state))
                or can_jet(player, state)
            ),
        )
        add_rule(
            world.get_location(LocationName.ricebeach_3_block7, player),
            lambda state: can_hit_groundblock(player, state),
        )
        add_rule(
            world.get_location(LocationName.ricebeach_4_block1, player),
            lambda state: can_hit_groundblock(player, state),
        )
        add_rule(
            world.get_location(LocationName.ricebeach_4_block2, player),
            lambda state: can_hit_groundblock(player, state),
        )
        add_rule(
            world.get_location(LocationName.ricebeach_4_block3, player),
            lambda state: can_hit_groundblock(player, state),
        )
        add_rule(
            world.get_location(LocationName.ricebeach_4_block4, player),
            lambda state: can_hit_groundblock(player, state),
        )
        add_rule(
            world.get_location(LocationName.ricebeach_4_block5, player),
            lambda state: can_hit_groundblock(player, state),
        )
        add_rule(
            world.get_location(LocationName.ricebeach_4_block6, player),
            lambda state: can_hit_groundblock(player, state),
        )

        # Mt Teapot Blocks
        add_rule(
            world.get_location(LocationName.mtteapot_7_block1, player),
            lambda state: can_jet(player, state) or can_dragon(player, state),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_7_block23, player),
            lambda state: can_jet(player, state)
            or (can_climb(player, state) and can_dragon(player, state)),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_7_block24, player),
            lambda state: can_jet(player, state)
            or (can_climb(player, state) and can_dragon(player, state)),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_8_block22, player),
            lambda state: (
                can_jet(player, state)
                or can_dragon(player, state)
                or can_dash(player, state)
            ),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_9_block6, player),
            lambda state: can_climb(player, state) or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_9_block7, player),
            lambda state: can_climb(player, state) or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_9_block8, player),
            lambda state: can_climb(player, state) or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_9_block9, player),
            lambda state: can_climb(player, state) or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_9_block10, player),
            lambda state: can_climb(player, state) or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_9_block11, player),
            lambda state: can_climb(player, state) or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_9_block12, player),
            lambda state: can_climb(player, state) or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_9_block13, player),
            lambda state: (can_climb(player, state) or can_jet(player, state))
            and can_hit_groundblock(player, state),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_9_block14, player),
            lambda state: can_climb(player, state) or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_9_block15, player),
            lambda state: can_climb(player, state) or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_10_block5, player),
            lambda state: can_highjump(player, state) or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_10_block7, player),
            lambda state: can_bull(player, state)
            or can_jet(player, state)
            or can_dragon(player, state),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_10_block10, player),
            lambda state: can_dragon(player, state) or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_10_block11, player),
            lambda state: can_climb(player, state) or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_10_block12, player),
            lambda state: (can_climb(player, state) or can_jet(player, state))
            and can_bull(player, state),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_10_block13, player),
            lambda state: (can_climb(player, state) or can_jet(player, state))
            and can_bull(player, state),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_10_block14, player),
            lambda state: (can_climb(player, state) or can_jet(player, state))
            and can_bull(player, state),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_10_block15, player),
            lambda state: can_climb(player, state) or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_10_block16, player),
            lambda state: can_climb(player, state) or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_10_block17, player),
            lambda state: can_climb(player, state) or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_10_block18, player),
            lambda state: can_climb(player, state) or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_10_block19, player),
            lambda state: can_climb(player, state) or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_10_block20, player),
            lambda state: can_climb(player, state) or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_10_block21, player),
            lambda state: can_climb(player, state) or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_10_block22, player),
            lambda state: can_climb(player, state) or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_11_block15, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_11_block16, player),
            lambda state: can_climb(player, state) and can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_11_block17, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_11_block18, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_13_block1, player),
            lambda state: (
                state.can_reach(LocationName.mtteapot_12_exit_1, "", player)
            ),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_13_block2, player),
            lambda state: (
                state.can_reach(LocationName.mtteapot_12_exit_1, "", player)
            ),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_13_block3, player),
            lambda state: (
                state.can_reach(LocationName.mtteapot_12_exit_1, "", player)
            ),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_13_block4, player),
            lambda state: (
                state.can_reach(LocationName.mtteapot_12_exit_1, "", player)
            ),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_13_block5, player),
            lambda state: (
                state.can_reach(LocationName.mtteapot_12_exit_1, "", player)
            ),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_13_block6, player),
            lambda state: (
                state.can_reach(LocationName.mtteapot_12_exit_1, "", player)
            ),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_13_block7, player),
            lambda state: (
                state.can_reach(LocationName.mtteapot_12_exit_1, "", player)
            ),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_13_block8, player),
            lambda state: (
                state.can_reach(LocationName.mtteapot_12_exit_1, "", player)
            ),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_13_block9, player),
            lambda state: (
                state.can_reach(LocationName.mtteapot_12_exit_1, "", player)
                and can_hit_groundblock(player, state)
            ),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_13_block10, player),
            lambda state: (
                state.can_reach(LocationName.mtteapot_12_exit_1, "", player)
                and can_hit_groundblock(player, state)
            ),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_13_block11, player),
            lambda state: (
                state.can_reach(LocationName.mtteapot_12_exit_1, "", player)
                and can_climb(player, state)
            ),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_13_block12, player),
            lambda state: (
                state.can_reach(LocationName.mtteapot_12_exit_1, "", player)
                and can_climb(player, state)
            ),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_13_block13, player),
            lambda state: (
                state.can_reach(LocationName.mtteapot_12_exit_1, "", player)
                and can_climb(player, state)
            ),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_13_block14, player),
            lambda state: (
                state.can_reach(LocationName.mtteapot_12_exit_1, "", player)
                and can_climb(player, state)
            ),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_13_block15, player),
            lambda state: (
                state.can_reach(LocationName.mtteapot_12_exit_1, "", player)
                and can_climb(player, state)
            ),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_13_block16, player),
            lambda state: (
                state.can_reach(LocationName.mtteapot_12_exit_1, "", player)
                and can_climb(player, state)
                and can_hit_groundblock(player, state)
            ),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_13_block17, player),
            lambda state: (
                state.can_reach(LocationName.mtteapot_12_exit_1, "", player)
                and can_climb(player, state)
                and can_hit_groundblock(player, state)
            ),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_13_block18, player),
            lambda state: (
                state.can_reach(LocationName.mtteapot_12_exit_1, "", player)
                and can_climb(player, state)
                and can_hit_groundblock(player, state)
            ),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_13_block19, player),
            lambda state: (
                state.can_reach(LocationName.mtteapot_12_exit_1, "", player)
                and can_climb(player, state)
                and can_hit_groundblock(player, state)
            ),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_13_block20, player),
            lambda state: (
                state.can_reach(LocationName.mtteapot_12_exit_1, "", player)
                and can_climb(player, state)
                and can_hit_groundblock(player, state)
            ),
        )
        add_rule(
            world.get_location(LocationName.mtteapot_13_block21, player),
            lambda state: (
                state.can_reach(LocationName.mtteapot_12_exit_1, "", player)
                and can_climb(player, state)
                and can_hit_groundblock(player, state)
            ),
        )

        # Sherbet Land Blocks
        add_rule(
            world.get_location(LocationName.sherbetland_15_block1, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.sherbetland_15_block2, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.sherbetland_15_block3, player),
            lambda state: can_climb(player, state)
            and (can_dash(player, state) or can_dragon(player, state)),
        )
        add_rule(
            world.get_location(LocationName.sherbetland_15_block4, player),
            lambda state: can_climb(player, state)
            and (
                can_dash(player, state)
                or can_dragon(player, state)
                or can_jet(player, state)
            ),
        )
        add_rule(
            world.get_location(LocationName.sherbetland_15_block5, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.sherbetland_15_block6, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.sherbetland_15_block7, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.sherbetland_15_block8, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.sherbetland_15_block9, player),
            lambda state: can_climb(player, state)
            and can_hit_groundblock(player, state),
        )
        add_rule(
            world.get_location(LocationName.sherbetland_15_block10, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.sherbetland_15_block11, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.sherbetland_15_block12, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.sherbetland_15_block13, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.sherbetland_16_block4, player),
            lambda state: can_hit_groundblock(player, state) or can_bull(player, state),
        )
        add_rule(
            world.get_location(LocationName.sherbetland_16_block8, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.sherbetland_17_block6, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.sherbetland_17_block7, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.sherbetland_17_block8, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.sherbetland_17_block9, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.sherbetland_17_block10, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.sherbetland_17_block11, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.sherbetland_17_block12, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.sherbetland_17_block13, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.sherbetland_17_block14, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.sherbetland_17_block15, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.sherbetland_18_block5, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.sherbetland_18_block6, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.sherbetland_18_block7, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.sherbetland_18_block8, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.sherbetland_18_block9, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.sherbetland_19_block1, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.sherbetland_19_block2, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.sherbetland_19_block3, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.sherbetland_19_block4, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.sherbetland_19_block5, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.sherbetland_19_block6, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.sherbetland_19_block7, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.sherbetland_19_block8, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.sherbetland_19_block9, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.sherbetland_19_block10, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.sherbetland_19_block11, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.sherbetland_19_block12, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.sherbetland_19_block13, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.sherbetland_19_block14, player),
            lambda state: can_climb(player, state),
        )

        # Stove Canyon Blocks
        add_rule(
            world.get_location(LocationName.stovecanyon_20_block2, player),
            lambda state: can_climb(player, state) or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.stovecanyon_20_block3, player),
            lambda state: can_climb(player, state) or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.stovecanyon_20_block4, player),
            lambda state: can_climb(player, state) or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.stovecanyon_20_block5, player),
            lambda state: can_climb(player, state) or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.stovecanyon_20_block6, player),
            lambda state: can_hit_groundblock(player, state)
            and (can_climb(player, state) or can_jet(player, state)),
        )
        add_rule(
            world.get_location(LocationName.stovecanyon_20_block7, player),
            lambda state: can_hit_groundblock(player, state)
            and (can_climb(player, state) or can_jet(player, state)),
        )
        add_rule(
            world.get_location(LocationName.stovecanyon_20_block8, player),
            lambda state: can_climb(player, state) or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.stovecanyon_20_block9, player),
            lambda state: can_climb(player, state) or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.stovecanyon_20_block10, player),
            lambda state: can_climb(player, state) or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.stovecanyon_20_block11, player),
            lambda state: can_climb(player, state) or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.stovecanyon_21_block3, player),
            lambda state: can_dragon(player, state) and can_duck(player, state),
        )
        add_rule(
            world.get_location(LocationName.stovecanyon_21_block4, player),
            lambda state: can_dragon(player, state) and can_duck(player, state),
        )
        add_rule(
            world.get_location(LocationName.stovecanyon_22_block1, player),
            lambda state: can_climb(player, state) or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.stovecanyon_22_block2, player),
            lambda state: (
                can_climb(player, state)
                and (can_dash(player, state) or can_dragon(player, state))
            )
            or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.stovecanyon_22_block3, player),
            lambda state: can_climb(player, state) or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.stovecanyon_22_block4, player),
            lambda state: can_climb(player, state) or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.stovecanyon_22_block5, player),
            lambda state: can_climb(player, state) or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.stovecanyon_22_block6, player),
            lambda state: can_climb(player, state) or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.stovecanyon_22_block7, player),
            lambda state: can_climb(player, state) or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.stovecanyon_23_block7, player),
            lambda state: can_hit_groundblock(player, state),
        )
        add_rule(
            world.get_location(LocationName.stovecanyon_24_block2, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.stovecanyon_24_block3, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.stovecanyon_24_block4, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.stovecanyon_24_block5, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.stovecanyon_24_block6, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.stovecanyon_24_block7, player),
            lambda state: can_climb(player, state) or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.stovecanyon_24_block8, player),
            lambda state: can_climb(player, state) or can_jet(player, state),
        )

        # SS Teacup Blocks
        add_rule(
            world.get_location(LocationName.ssteacup_26_block8, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_26_block9, player),
            lambda state: can_climb(player, state)
            and can_hit_groundblock(player, state),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_26_block10, player),
            lambda state: can_climb(player, state)
            and can_hit_groundblock(player, state),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_26_block11, player),
            lambda state: can_climb(player, state)
            and can_hit_groundblock(player, state),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_27_block1, player),
            lambda state: can_dragon(player, state),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_27_block11, player),
            lambda state: (
                can_climb(player, state)
                and (
                    (can_dash(player, state) and can_bull(player, state))
                    or can_jet(player, state)
                )
            ),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_27_block12, player),
            lambda state: can_grow(player, state) and can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_27_block13, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_27_block14, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_27_block15, player),
            lambda state: can_climb(player, state)
            and (can_duck(player, state) and can_dragon(player, state)),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_27_block16, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_27_block17, player),
            lambda state: can_climb(player, state) and can_grow(player, state),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_27_block18, player),
            lambda state: can_climb(player, state) and can_grow(player, state),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_27_block19, player),
            lambda state: can_climb(player, state) and can_grow(player, state),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_27_block20, player),
            lambda state: can_climb(player, state) and can_grow(player, state),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_27_block21, player),
            lambda state: can_climb(player, state) and can_grow(player, state),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_27_block22, player),
            lambda state: can_climb(player, state) and can_grow(player, state),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_27_block23, player),
            lambda state: can_climb(player, state) and can_grow(player, state),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_27_block24, player),
            lambda state: can_climb(player, state) and can_grow(player, state),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_27_block25, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_29_block2, player),
            lambda state: can_climb(player, state) or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_29_block3, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_29_block4, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_29_block5, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_29_block6, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_29_block7, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_29_block8, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_29_block9, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_29_block10, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_29_block11, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_30_block2, player),
            lambda state: can_dash(player, state)
            or can_bull(player, state)
            or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_30_block3, player),
            lambda state: can_dash(player, state)
            or can_bull(player, state)
            or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_30_block4, player),
            lambda state: can_dash(player, state)
            or can_bull(player, state)
            or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_30_block7, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_30_block8, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_30_block9, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_30_block10, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_30_block11, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_30_block12, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_30_block13, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_30_block14, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_30_block15, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_30_block16, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_30_block17, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_30_block18, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_30_block19, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_30_block20, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_30_block21, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_30_block22, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.ssteacup_30_block23, player),
            lambda state: can_climb(player, state),
        )

        # Parsley Woods Blocks
        add_rule(
            world.get_location(LocationName.parsleywoods_31_drained_block2, player),
            lambda state: can_hit_elevated_groundblock(player, state),
        )
        add_rule(
            world.get_location(LocationName.parsleywoods_31_drained_block3, player),
            lambda state: can_hit_elevated_groundblock(player, state),
        )
        add_rule(
            world.get_location(LocationName.parsleywoods_31_drained_block4, player),
            lambda state: can_jet(player, state) or can_highjump(player, state),
        )
        add_rule(
            world.get_location(LocationName.parsleywoods_31_drained_block5, player),
            lambda state: can_climb(player, state) or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.parsleywoods_31_drained_block6, player),
            lambda state: can_climb(player, state) or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.parsleywoods_31_drained_block7, player),
            lambda state: (can_climb(player, state) and can_dragon(player, state))
            or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.parsleywoods_31_drained_block8, player),
            lambda state: (can_climb(player, state) and can_dragon(player, state))
            or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.parsleywoods_31_drained_block9, player),
            lambda state: can_climb(player, state) or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.parsleywoods_31_drained_block10, player),
            lambda state: can_climb(player, state) or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.parsleywoods_31_drained_block11, player),
            lambda state: can_climb(player, state) or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.parsleywoods_31_drained_block12, player),
            lambda state: can_climb(player, state) or can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.parsleywoods_31_drained_block13, player),
            lambda state: can_jet(player, state),
        )
        add_rule(
            world.get_location(LocationName.parsleywoods_33_block6, player),
            lambda state: can_hit_elevated_groundblock(player, state),
        )
        add_rule(
            world.get_location(LocationName.parsleywoods_33_block7, player),
            lambda state: can_hit_elevated_groundblock(player, state),
        )
        add_rule(
            world.get_location(LocationName.parsleywoods_33_block8, player),
            lambda state: can_hit_elevated_groundblock(player, state),
        )
        add_rule(
            world.get_location(LocationName.parsleywoods_33_block9, player),
            lambda state: can_hit_elevated_groundblock(player, state),
        )
        add_rule(
            world.get_location(LocationName.parsleywoods_34_block3, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.parsleywoods_34_block4, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.parsleywoods_34_block5, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.parsleywoods_34_block6, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.parsleywoods_34_block7, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.parsleywoods_34_block8, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.parsleywoods_34_block9, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.parsleywoods_34_block10, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.parsleywoods_34_block11, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.parsleywoods_34_block12, player),
            lambda state: can_climb(player, state),
        )

        # Syrup Castle Blocks
        add_rule(
            world.get_location(LocationName.syrupcastle_37_block20, player),
            lambda state: can_grow(player, state),
        )
        add_rule(
            world.get_location(LocationName.syrupcastle_38_block4, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.syrupcastle_38_block5, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.syrupcastle_38_block6, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.syrupcastle_38_block7, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.syrupcastle_38_block8, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.syrupcastle_38_block9, player),
            lambda state: can_climb(player, state),
        )
        add_rule(
            world.get_location(LocationName.syrupcastle_39_block3, player),
            lambda state: can_hit_elevated_groundblock(player, state),
        )
        add_rule(
            world.get_location(LocationName.syrupcastle_39_block4, player),
            lambda state: can_hit_elevated_groundblock(player, state),
        )
        add_rule(
            world.get_location(LocationName.syrupcastle_39_block5, player),
            lambda state: can_bull(player, state)
            or (can_dragon(player, state) and can_duck(player, state)),
        )
        add_rule(
            world.get_location(LocationName.syrupcastle_39_block9, player),
            lambda state: can_bull(player, state) and can_duck(player, state),
        )
        add_rule(
            world.get_location(LocationName.syrupcastle_39_block10, player),
            lambda state: can_bull(player, state) and can_duck(player, state),
        )
        add_rule(
            world.get_location(LocationName.syrupcastle_39_block11, player),
            lambda state: can_bull(player, state)
            and can_dash(player, state)
            and can_duck(player, state),
        )
        add_rule(
            world.get_location(LocationName.syrupcastle_40_block7, player),
            lambda state: can_dragon(player, state)
            or (can_bull(player, state) and can_dash(player, state)),
        )
        add_rule(
            world.get_location(LocationName.syrupcastle_40_block8, player),
            lambda state: can_dragon(player, state)
            or (can_bull(player, state) and can_dash(player, state)),
        )
        add_rule(
            world.get_location(LocationName.syrupcastle_40_block18, player),
            lambda state: can_climb(player, state),
        )

    if options.treasure_checks:
        add_location_to_region(
            world,
            player,
            active_locations,
            LocationName.ricebeach_3_region,
            LocationName.ricebeach_3_treasure,
            lambda state: (
                (
                    can_jet(player, state)
                    or (can_dragon(player, state) and can_duck(player, state))
                )
                and state.can_reach(LocationName.ricebeach_boss, "", player)
            ),
        )
        add_location_to_region(
            world,
            player,
            active_locations,
            LocationName.mtteapot_9_region,
            LocationName.mtteapot_9_treasure,
            lambda state: (
                (
                    can_jet(player, state)
                    or (can_dragon(player, state) and can_duck(player, state))
                    or can_dash(player, state)
                )
                and (can_jet(player, state) or can_climb(player, state))
            ),
        )
        add_location_to_region(
            world,
            player,
            active_locations,
            LocationName.mtteapot_11_region,
            LocationName.mtteapot_11_treasure,
            lambda state: (can_jet(player, state) and can_climb(player, state)),
        )

        add_location_to_region(
            world,
            player,
            active_locations,
            LocationName.sherbetland_16_region,
            LocationName.sherbetland_16_treasure,
            lambda state: (can_open_treasure(player, state)),
        )
        add_location_to_region(
            world,
            player,
            active_locations,
            LocationName.sherbetland_17_region,
            LocationName.sherbetland_17_treasure,
            lambda state: (
                can_open_treasure(player, state) and can_climb(player, state)
            ),
        )
        add_location_to_region(
            world,
            player,
            active_locations,
            LocationName.sherbetland_18_region,
            LocationName.sherbetland_18_treasure,
            lambda state: (
                can_open_treasure(player, state) and can_climb(player, state)
            ),
        )

        add_location_to_region(
            world,
            player,
            active_locations,
            LocationName.stovecanyon_20_region,
            LocationName.stovecanyon_20_treasure,
            lambda state: (
                can_climb(player, state)
                and (
                    can_jet(player, state)
                    or can_dash(player, state)
                    or (can_dragon(player, state) and can_duck(player, state))
                )
            ),
        )
        add_location_to_region(
            world,
            player,
            active_locations,
            LocationName.stovecanyon_24_region,
            LocationName.stovecanyon_24_treasure,
            lambda state: (
                can_open_treasure(player, state) and can_climb(player, state)
            ),
        )

        add_location_to_region(
            world,
            player,
            active_locations,
            LocationName.ssteacup_26_region,
            LocationName.ssteacup_26_treasure,
            lambda state: (
                can_climb(player, state)
                and (
                    can_jet(player, state)
                    or can_dash(player, state)
                    or (can_dragon(player, state) and can_duck(player, state))
                )
            ),
        )
        add_location_to_region(
            world,
            player,
            active_locations,
            LocationName.ssteacup_29_region,
            LocationName.ssteacup_29_treasure,
            lambda state: (
                can_open_treasure(player, state) and can_climb(player, state)
            ),
        )
        add_location_to_region(
            world,
            player,
            active_locations,
            LocationName.ssteacup_30_region,
            LocationName.ssteacup_30_treasure,
            lambda state: (
                can_open_treasure(player, state) and can_climb(player, state)
            ),
        )

        add_location_to_region(
            world,
            player,
            active_locations,
            LocationName.parsleywoods_31_region,
            LocationName.parsleywoods_31_treasure,
            lambda state: (
                can_climb(player, state)
                and (
                    can_jet(player, state)
                    or can_dash(player, state)
                    or (can_dragon(player, state) and can_duck(player, state))
                )
                and state.can_reach(LocationName.parsleywoods_32_exit_1, "", player)
            ),
        )
        add_location_to_region(
            world,
            player,
            active_locations,
            LocationName.parsleywoods_34_region,
            LocationName.parsleywoods_34_treasure,
            lambda state: (
                can_open_treasure(player, state) and can_climb(player, state)
            ),
        )

        add_location_to_region(
            world,
            player,
            active_locations,
            LocationName.syrupcastle_37_region,
            LocationName.syrupcastle_37_treasure,
            lambda state: (can_open_treasure(player, state)),
        )
        add_location_to_region(
            world,
            player,
            active_locations,
            LocationName.syrupcastle_39_region,
            LocationName.syrupcastle_39_treasure,
            lambda state: (
                can_dash(player, state)
                and can_duck(player, state)
                and can_bull(player, state)
            ),
        )


def connect_regions(world, player, options, level_to_tile_dict):
    names: typing.Dict[str, int] = {}
    connect(
        world, player, names, LocationName.menu_region, LocationName.overworld_region
    )

    # Overworld -> World
    if options.world_unlocks == 1:
        connect(
            world,
            player,
            names,
            LocationName.overworld_region,
            LocationName.ricebeach_region,
            lambda state: state.has(ItemName.ricebeach, player),
        )
        connect(
            world,
            player,
            names,
            LocationName.overworld_region,
            LocationName.mtteapot_region,
            lambda state: state.has(ItemName.mtteapot, player),
        )
        connect(
            world,
            player,
            names,
            LocationName.overworld_region,
            LocationName.sherbetland_region,
            lambda state: state.has(ItemName.sherbetland, player),
        )
        connect(
            world,
            player,
            names,
            LocationName.overworld_region,
            LocationName.stovecanyon_region,
            lambda state: state.has(ItemName.stovecanyon, player),
        )
        connect(
            world,
            player,
            names,
            LocationName.overworld_region,
            LocationName.ssteacup_region,
            lambda state: state.has(ItemName.ssteacup, player),
        )
        connect(
            world,
            player,
            names,
            LocationName.overworld_region,
            LocationName.parsleywoods_region,
            lambda state: state.has(ItemName.parsleywoods, player),
        )
        connect(
            world,
            player,
            names,
            LocationName.overworld_region,
            LocationName.syrupcastle_region,
            lambda state: state.has(ItemName.syrupcastle, player),
        )
    else:
        connect(
            world,
            player,
            names,
            LocationName.overworld_region,
            LocationName.ricebeach_region,
        )
        connect(
            world,
            player,
            names,
            LocationName.overworld_region,
            LocationName.mtteapot_region,
        )
        connect(
            world,
            player,
            names,
            LocationName.overworld_region,
            LocationName.sherbetland_region,
        )
        connect(
            world,
            player,
            names,
            LocationName.overworld_region,
            LocationName.stovecanyon_region,
        )
        connect(
            world,
            player,
            names,
            LocationName.overworld_region,
            LocationName.ssteacup_region,
        )
        connect(
            world,
            player,
            names,
            LocationName.overworld_region,
            LocationName.parsleywoods_region,
        )
        connect(
            world,
            player,
            names,
            LocationName.overworld_region,
            LocationName.syrupcastle_region,
        )

    # Level -> Level Exit
    connect(
        world,
        player,
        names,
        LocationName.ricebeach_1_region,
        LocationName.ricebeach_1_exit_1,
    )
    connect(
        world,
        player,
        names,
        LocationName.ricebeach_2_region,
        LocationName.ricebeach_2_exit_1,
        lambda state: (can_create_coin(player, state)),
    )
    connect(
        world,
        player,
        names,
        LocationName.ricebeach_3_region,
        LocationName.ricebeach_3_exit_1,
        lambda state: (can_create_coin(player, state)),
    )
    connect(
        world,
        player,
        names,
        LocationName.ricebeach_3_region,
        LocationName.ricebeach_3_exit_2,
        lambda state: (
            can_create_coin(player, state)
            and (
                can_highjump(player, state)
                or (state.can_reach(LocationName.ricebeach_boss, "", player))
            )
        ),
    )
    connect(
        world,
        player,
        names,
        LocationName.ricebeach_4_region,
        LocationName.ricebeach_4_exit_1,
        lambda state: (
            can_dash(player, state)
            or (
                can_duck(player, state)
                and (can_jet(player, state) or can_dragon(player, state))
            )
        ),
    )
    connect(
        world,
        player,
        names,
        LocationName.ricebeach_5_region,
        LocationName.ricebeach_boss,
    )
    connect(
        world,
        player,
        names,
        LocationName.ricebeach_6_region,
        LocationName.ricebeach_6_exit_1,
        lambda state: (can_create_coin(player, state)),
    )

    connect(
        world,
        player,
        names,
        LocationName.mtteapot_7_region,
        LocationName.mtteapot_7_exit_1,
        lambda state: (can_create_coin(player, state)),
    )
    connect(
        world,
        player,
        names,
        LocationName.mtteapot_8_region,
        LocationName.mtteapot_8_exit_1,
        lambda state: (can_create_coin(player, state)),
    )
    connect(
        world,
        player,
        names,
        LocationName.mtteapot_8_region,
        LocationName.mtteapot_8_exit_2,
        lambda state: (can_create_coin(player, state) and can_jet(player, state)),
    )
    connect(
        world,
        player,
        names,
        LocationName.mtteapot_9_region,
        LocationName.mtteapot_9_exit_1,
        lambda state: (
            can_create_coin(player, state)
            and (can_jet(player, state) or can_climb(player, state))
        ),
    )
    connect(
        world,
        player,
        names,
        LocationName.mtteapot_10_region,
        LocationName.mtteapot_10_exit_1,
        lambda state: (
            can_create_coin(player, state)
            and (can_jet(player, state) or can_climb(player, state))
        ),
    )
    connect(
        world,
        player,
        names,
        LocationName.mtteapot_11_region,
        LocationName.mtteapot_11_exit_1,
        lambda state: (can_climb(player, state)),
    )
    connect(
        world,
        player,
        names,
        LocationName.mtteapot_12_region,
        LocationName.mtteapot_12_exit_1,
        lambda state: (can_jet(player, state) or can_climb(player, state)),
    )
    connect(
        world,
        player,
        names,
        LocationName.mtteapot_13_region,
        LocationName.mtteapot_boss,
        lambda state: (
            can_climb(player, state)
            and state.can_reach(LocationName.mtteapot_12_exit_1, "", player)
        ),
    )

    connect(
        world,
        player,
        names,
        LocationName.sherbetland_14_region,
        LocationName.sherbetland_14_exit_1,
    )
    connect(
        world,
        player,
        names,
        LocationName.sherbetland_15_region,
        LocationName.sherbetland_15_exit_1,
        lambda state: (can_create_coin(player, state) and can_climb(player, state)),
    )
    connect(
        world,
        player,
        names,
        LocationName.sherbetland_15_region,
        LocationName.sherbetland_15_exit_2,
        lambda state: (can_create_coin(player, state) and can_climb(player, state)),
    )
    connect(
        world,
        player,
        names,
        LocationName.sherbetland_16_region,
        LocationName.sherbetland_16_exit_1,
        lambda state: (can_create_coin(player, state) and can_climb(player, state)),
    )
    connect(
        world,
        player,
        names,
        LocationName.sherbetland_16_region,
        LocationName.sherbetland_16_exit_2,
        lambda state: (can_create_coin(player, state)),
    )
    connect(
        world,
        player,
        names,
        LocationName.sherbetland_17_region,
        LocationName.sherbetland_17_exit_1,
        lambda state: (can_create_coin(player, state)),
    )
    connect(
        world,
        player,
        names,
        LocationName.sherbetland_18_region,
        LocationName.sherbetland_18_exit_1,
        lambda state: (can_create_coin(player, state)),
    )
    connect(
        world,
        player,
        names,
        LocationName.sherbetland_19_region,
        LocationName.sherbetland_boss,
        lambda state: (can_climb(player, state)),
    )
    # connect(world, player, names, LocationName.sherbetland_19_region, LocationName.sherbetland_boss,
    #        lambda state : (can_climb(player, state) and (can_dash(player, state) or can_jet(player, state))))

    connect(
        world,
        player,
        names,
        LocationName.stovecanyon_20_region,
        LocationName.stovecanyon_20_exit_1,
        lambda state: (can_climb(player, state)),
    )
    connect(
        world,
        player,
        names,
        LocationName.stovecanyon_21_region,
        LocationName.stovecanyon_21_exit_1,
        lambda state: (can_create_coin(player, state)),
    )
    connect(
        world,
        player,
        names,
        LocationName.stovecanyon_22_region,
        LocationName.stovecanyon_22_exit_1,
        lambda state: (can_create_coin(player, state) and can_climb(player, state)),
    )
    connect(
        world,
        player,
        names,
        LocationName.stovecanyon_23_region,
        LocationName.stovecanyon_23_exit_1,
        lambda state: (can_create_coin(player, state)),
    )
    connect(
        world,
        player,
        names,
        LocationName.stovecanyon_23_region,
        LocationName.stovecanyon_23_exit_2,
        lambda state: (can_create_coin(player, state)),
    )
    connect(
        world,
        player,
        names,
        LocationName.stovecanyon_24_region,
        LocationName.stovecanyon_24_exit_1,
        lambda state: (can_create_coin(player, state) and can_climb(player, state)),
    )
    connect(
        world,
        player,
        names,
        LocationName.stovecanyon_25_region,
        LocationName.stovecanyon_boss,
    )

    connect(
        world,
        player,
        names,
        LocationName.ssteacup_26_region,
        LocationName.ssteacup_26_exit_1,
        lambda state: (can_create_coin(player, state)),
    )
    connect(
        world,
        player,
        names,
        LocationName.ssteacup_27_region,
        LocationName.ssteacup_27_exit_1,
        lambda state: (
            can_create_coin(player, state)
            and (can_climb(player, state) or can_jet(player, state))
        ),
    )
    connect(
        world,
        player,
        names,
        LocationName.ssteacup_28_region,
        LocationName.ssteacup_28_exit_1,
        lambda state: (can_create_coin(player, state)),
    )
    connect(
        world,
        player,
        names,
        LocationName.ssteacup_29_region,
        LocationName.ssteacup_29_exit_1,
        lambda state: (can_create_coin(player, state) and can_climb(player, state)),
    )
    connect(
        world,
        player,
        names,
        LocationName.ssteacup_30_region,
        LocationName.ssteacup_boss,
        lambda state: (can_climb(player, state)),
    )

    connect(
        world,
        player,
        names,
        LocationName.parsleywoods_31_region,
        LocationName.parsleywoods_31_exit_1,
        lambda state: (can_create_coin(player, state)),
    )
    connect(
        world,
        player,
        names,
        LocationName.parsleywoods_32_region,
        LocationName.parsleywoods_32_exit_1,
    )
    connect(
        world,
        player,
        names,
        LocationName.parsleywoods_33_region,
        LocationName.parsleywoods_33_exit_1,
    )
    connect(
        world,
        player,
        names,
        LocationName.parsleywoods_34_region,
        LocationName.parsleywoods_34_exit_1,
        lambda state: (can_create_coin(player, state) and can_climb(player, state)),
    )
    connect(
        world,
        player,
        names,
        LocationName.parsleywoods_35_region,
        LocationName.parsleywoods_35_exit_1,
    )
    connect(
        world,
        player,
        names,
        LocationName.parsleywoods_36_region,
        LocationName.parsleywoods_boss,
    )

    connect(
        world,
        player,
        names,
        LocationName.syrupcastle_37_region,
        LocationName.syrupcastle_37_exit_1,
        lambda state: (can_create_coin(player, state)),
    )
    connect(
        world,
        player,
        names,
        LocationName.syrupcastle_38_region,
        LocationName.syrupcastle_38_exit_1,
        lambda state: (can_climb(player, state)),
    )
    connect(
        world,
        player,
        names,
        LocationName.syrupcastle_39_region,
        LocationName.syrupcastle_39_exit_1,
    )
    # connect(world, player, names, LocationName.syrupcastle_40_region, LocationName.syrupcastle_40_exit_1,
    #        lambda state : (can_defeat_final_boss(player, state)))
    connect(
        world,
        player,
        names,
        LocationName.syrupcastle_40_region,
        LocationName.syrupcastle_boss,
        lambda state: can_defeat_final_boss(player, state, world, options) and can_climb(player, state),
    )

    # Connect Worlds -> Tiles for openworld
    if options.boss_unlocks == 1:
        connect(
            world,
            player,
            names,
            LocationName.ricebeach_region,
            LocationName.ricebeach_5_tile,
            lambda state: state.has(ItemName.ricebeach_bossunlock, player),
        )
        connect(
            world,
            player,
            names,
            LocationName.mtteapot_region,
            LocationName.mtteapot_13_tile,
            lambda state: state.has(ItemName.mtteapot_bossunlock, player),
        )
        connect(
            world,
            player,
            names,
            LocationName.sherbetland_region,
            LocationName.sherbetland_19_tile,
            lambda state: state.has(ItemName.sherbetland_bossunlock, player),
        )
        connect(
            world,
            player,
            names,
            LocationName.stovecanyon_region,
            LocationName.stovecanyon_25_tile,
            lambda state: state.has(ItemName.stovecanyon_bossunlock, player),
        )
        connect(
            world,
            player,
            names,
            LocationName.ssteacup_region,
            LocationName.ssteacup_30_tile,
            lambda state: state.has(ItemName.ssteacup_bossunlock, player),
        )
        connect(
            world,
            player,
            names,
            LocationName.parsleywoods_region,
            LocationName.parsleywoods_36_tile,
            lambda state: state.has(ItemName.parsleywoods_bossunlock, player),
        )
    else:
        connect(
            world,
            player,
            names,
            LocationName.ricebeach_region,
            LocationName.ricebeach_5_tile,
        )
        connect(
            world,
            player,
            names,
            LocationName.mtteapot_region,
            LocationName.mtteapot_13_tile,
        )
        connect(
            world,
            player,
            names,
            LocationName.sherbetland_region,
            LocationName.sherbetland_19_tile,
        )
        connect(
            world,
            player,
            names,
            LocationName.stovecanyon_region,
            LocationName.stovecanyon_25_tile,
        )
        connect(
            world,
            player,
            names,
            LocationName.ssteacup_region,
            LocationName.ssteacup_30_tile,
        )
        connect(
            world,
            player,
            names,
            LocationName.parsleywoods_region,
            LocationName.parsleywoods_36_tile,
        )

    connect(
        world,
        player,
        names,
        LocationName.ricebeach_region,
        LocationName.ricebeach_1_tile,
    )
    connect(
        world,
        player,
        names,
        LocationName.ricebeach_region,
        LocationName.ricebeach_2_tile,
    )
    connect(
        world,
        player,
        names,
        LocationName.ricebeach_region,
        LocationName.ricebeach_3_tile,
    )
    connect(
        world,
        player,
        names,
        LocationName.ricebeach_region,
        LocationName.ricebeach_4_tile,
    )

    connect(
        world,
        player,
        names,
        LocationName.ricebeach_region,
        LocationName.ricebeach_6_tile,
    )
    connect(
        world, player, names, LocationName.mtteapot_region, LocationName.mtteapot_7_tile
    )
    connect(
        world, player, names, LocationName.mtteapot_region, LocationName.mtteapot_8_tile
    )
    connect(
        world, player, names, LocationName.mtteapot_region, LocationName.mtteapot_9_tile
    )
    connect(
        world,
        player,
        names,
        LocationName.mtteapot_region,
        LocationName.mtteapot_10_tile,
    )
    connect(
        world,
        player,
        names,
        LocationName.mtteapot_region,
        LocationName.mtteapot_11_tile,
    )
    connect(
        world,
        player,
        names,
        LocationName.mtteapot_region,
        LocationName.mtteapot_12_tile,
    )

    connect(
        world,
        player,
        names,
        LocationName.sherbetland_region,
        LocationName.sherbetland_14_tile,
    )
    connect(
        world,
        player,
        names,
        LocationName.sherbetland_region,
        LocationName.sherbetland_15_tile,
    )
    connect(
        world,
        player,
        names,
        LocationName.sherbetland_region,
        LocationName.sherbetland_16_tile,
    )
    connect(
        world,
        player,
        names,
        LocationName.sherbetland_region,
        LocationName.sherbetland_17_tile,
    )
    connect(
        world,
        player,
        names,
        LocationName.sherbetland_region,
        LocationName.sherbetland_18_tile,
    )

    connect(
        world,
        player,
        names,
        LocationName.stovecanyon_region,
        LocationName.stovecanyon_20_tile,
    )
    connect(
        world,
        player,
        names,
        LocationName.stovecanyon_region,
        LocationName.stovecanyon_21_tile,
    )
    connect(
        world,
        player,
        names,
        LocationName.stovecanyon_region,
        LocationName.stovecanyon_22_tile,
    )
    connect(
        world,
        player,
        names,
        LocationName.stovecanyon_region,
        LocationName.stovecanyon_23_tile,
    )
    connect(
        world,
        player,
        names,
        LocationName.stovecanyon_region,
        LocationName.stovecanyon_24_tile,
    )

    connect(
        world,
        player,
        names,
        LocationName.ssteacup_region,
        LocationName.ssteacup_26_tile,
    )
    connect(
        world,
        player,
        names,
        LocationName.ssteacup_region,
        LocationName.ssteacup_27_tile,
    )
    connect(
        world,
        player,
        names,
        LocationName.ssteacup_region,
        LocationName.ssteacup_28_tile,
    )
    connect(
        world,
        player,
        names,
        LocationName.ssteacup_region,
        LocationName.ssteacup_29_tile,
    )

    connect(
        world,
        player,
        names,
        LocationName.parsleywoods_region,
        LocationName.parsleywoods_31_tile,
    )
    connect(
        world,
        player,
        names,
        LocationName.parsleywoods_region,
        LocationName.parsleywoods_32_tile,
    )
    connect(
        world,
        player,
        names,
        LocationName.parsleywoods_region,
        LocationName.parsleywoods_33_tile,
    )
    connect(
        world,
        player,
        names,
        LocationName.parsleywoods_region,
        LocationName.parsleywoods_34_tile,
    )
    connect(
        world,
        player,
        names,
        LocationName.parsleywoods_region,
        LocationName.parsleywoods_35_tile,
    )

    connect(
        world,
        player,
        names,
        LocationName.syrupcastle_region,
        LocationName.syrupcastle_37_tile,
    )
    connect(
        world,
        player,
        names,
        LocationName.syrupcastle_region,
        LocationName.syrupcastle_38_tile,
    )
    connect(
        world,
        player,
        names,
        LocationName.syrupcastle_region,
        LocationName.syrupcastle_39_tile,
    )
    # Syrup Castle boss is always locked by boss tokens
    connect(
        world,
        player,
        names,
        LocationName.syrupcastle_region,
        LocationName.syrupcastle_40_tile,
        lambda state: (can_defeat_final_boss(player, state, world, options)),
    )

    # Connect levels to each other

    # TODO: Special case for level shuffle
    # Flooded Rice Beach
    # 0x17:       WLLevel(LocationName.ricebeach_1_region, 0x23f02, 0x17,),
    # 0x24:       WLLevel(LocationName.ricebeach_3_region, 0x23ef9, 0x24,),
    # Parsley Woods
    # 0x2A: Drained
    for current_level_id, current_level_data in level_info_dict.items():
        # Connect tile regions to correct level regions
        if current_level_id not in level_to_tile_dict.keys():
            continue

        current_tile_id = level_to_tile_dict[current_level_id]
        current_tile_data = level_info_dict[current_tile_id]
        current_tile_name = current_tile_data.levelName
        current_tile_name += " - Tile"
        unlock = course_unlock_names.get(current_level_id)
        rule = (lambda state, name=unlock: state.has(name, player)) if options.level_unlocks and unlock else None
        connect(world, player, names, current_tile_name, current_level_data.levelName, rule)
        # (TODO: More level shuffle work)
        # if current_tile_data.exit1Path:
        #    next_tile_id = current_tile_data.exit1Path
        #    next_tile_name = level_info_dict[next_tile_id].levelName
        #    next_tile_name += " - Tile"
        #    current_exit_name = (current_level_data.levelName + " - Normal Exit")
        #    connect(world, player, names, current_exit_name, next_tile_name)
        # if current_tile_data.exit2Path:
        #    next_tile_id = current_tile_data.exit2Path
        #    next_tile_name = level_info_dict[next_tile_id].levelName
        #    next_tile_name += " - Tile"
        #    current_exit_name = (current_level_data.levelName + " - Secret Exit")
        #    connect(world, player, names, current_exit_name, next_tile_name)


def create_region(
    world: MultiWorld, player: int, active_locations, name: str, locations=None
):
    ret = Region(name, player, world)
    if locations:
        for locationName in locations:
            loc_id = active_locations.get(locationName, 0)
            if loc_id:
                location = WLLocation(player, locationName, loc_id, ret)
                ret.locations.append(location)
    return ret


def add_location_to_region(
    world: MultiWorld,
    player: int,
    active_locations,
    region_name: str,
    location_name: str,
    rule: typing.Optional[typing.Callable] = None,
):
    region = world.get_region(region_name, player)
    loc_id = active_locations.get(location_name, 0)
    if loc_id:
        location = WLLocation(player, location_name, loc_id, region)
        region.locations.append(location)
        if rule:
            add_rule(location, rule)


def connect(
    world: MultiWorld,
    player: int,
    used_names: typing.Dict[str, int],
    source: str,
    target: str,
    rule: typing.Optional[typing.Callable] = None,
):
    source_region = world.get_region(source, player)
    target_region = world.get_region(target, player)

    if target not in used_names:
        used_names[target] = 1
        name = target
    else:
        used_names[target] += 1
        name = target + (" " * used_names[target])

    connection = Entrance(player, name, source_region)

    if rule:
        connection.access_rule = rule

    source_region.exits.append(connection)
    connection.connect(target_region)
