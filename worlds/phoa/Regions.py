from typing import Dict, Callable, Optional, NamedTuple
from BaseClasses import MultiWorld, Region, Location, CollectionState
from worlds.phoa import get_location_data, PhoaOptions
from worlds.phoa.Locations import PhoaLocationData
from worlds.phoa.LogicExtensions import PhoaLogic


class PhoaExit(NamedTuple):
    name: str
    region: str
    connection: str
    rule: Optional[Callable[[CollectionState], bool]] = None
    one_way: bool = False


def get_exit_data(player: int, options: PhoaOptions) -> list[PhoaExit]:
    logic = PhoaLogic(player)

    exits: list[PhoaExit] = [
        # Menu
        PhoaExit(
            name="game_start",
            region="Menu",
            connection="panselo_village",
            one_way=True,
        ),
        # panselo_village
        PhoaExit(
            name="panselo_gate",
            region="panselo_village",
            connection="panselo_region",
            rule=lambda state: logic.can_deal_damage(state, exclude_rocket_boots=True)
                               or options.open_panselo_gates > 0,
        ),
        PhoaExit(
            name="rutea's_lab_gate",
            region="panselo_village",
            connection="panselo_village_rutea's_lab",
            rule=lambda state: logic.can_hit_switch_from_a_distance(state),
        ),
        # panselo_region
        PhoaExit(
            name="anuri_temple_entrance",
            region="panselo_region",
            connection="anuri_temple(main_entrance)",
            rule=lambda state: logic.can_hit_switch_from_a_distance(state),
        ),
        PhoaExit(
            name="anuri_temple_side_entrance",
            region="panselo_region",
            connection="anuri_temple(side_entrance)",
            rule=lambda state: logic.has_explosives(state),
        ),
        PhoaExit(
            name="over_anuri_temple",
            region="panselo_region",
            connection="anuri_temple(slargummy_boss)",
            rule=lambda state: logic.has_sonic_spear(state),
            one_way=True,
        ),
        PhoaExit(
            name="panselo_region_to_atai_region",
            region="panselo_region",
            connection="atai_region",
        ),
        # anuri_temple(main_entrance)
        PhoaExit(
            name="anuri_temple_main_exit",
            region="anuri_temple(main_entrance)",
            connection="panselo_region",
        ),
        PhoaExit(
            name="anuri_temple_pearl_entrance",
            region="anuri_temple(main_entrance)",
            connection="anuri_temple(main)",
            rule=lambda state: logic.has_anuri_pearlstones(1, state)
        ),
        PhoaExit(
            name="anuri_temple_top_floor_boulder",
            region="anuri_temple(main_entrance)",
            connection="anuri_temple(top_floor)",
            rule=lambda state: logic.has_explosives(state)
                               or (logic.has_sonic_spear(state)
                                   and state.has("Rocket Boots", player)),
        ),
        # anuri_temple(top_floor)
        PhoaExit(
            name="anuri_temple_drop_to_throne",
            region="anuri_temple(top_floor)",
            connection="anuri_temple(main)",
            one_way=True,
        ),
        PhoaExit(
            name="anuri_temple_door_to_scaber_maze",
            region="anuri_temple(top_floor)",
            connection="anuri_temple(scaber_switch_maze)",
            rule=lambda state: logic.has_anuri_pearlstones(10, state)
        ),
        # anuri_temple(main)
        PhoaExit(
            name="anuri_temple_to_main_entrance",
            region="anuri_temple(main)",
            connection="anuri_temple(main_entrance)",
        ),
        PhoaExit(
            name="anuri_temple_to_tall_tower_puzzle_room",
            region="anuri_temple(main)",
            connection="anuri_temple(tall_tower_puzzle_room)",
            rule=lambda state: logic.has_anuri_pearlstones(10, state),
        ),
        PhoaExit(
            name="anuri_temple_to_side_entrance",
            region="anuri_temple(main)",
            connection="anuri_temple(side_entrance)",
        ),
        PhoaExit(
            name="anuri_temple_to_basement",
            region="anuri_temple(main)",
            connection="anuri_temple(basement)",
            rule=lambda state: logic.has_explosives(state),
        ),
        PhoaExit(
            name="anuri_temple_bridge_switch",
            region="anuri_temple(main)",
            connection="anuri_temple(moveable_bridge_area)",
            rule=lambda state: logic.can_hit_switch_from_a_distance(state)
                               or state.has("Rocket Boots", player),
        ),
        PhoaExit(
            name="anuri_temple_to_slargummy",
            region="anuri_temple(main)",
            connection="anuri_temple(slargummy_boss)",
            rule=lambda state: logic.has_anuri_pearlstones(6, state),
        ),
        # anuri_temple(side_entrance)
        PhoaExit(
            name="anuri_temple_side_exit",
            region="anuri_temple(side_entrance)",
            connection="panselo_region",
            rule=lambda state: logic.has_explosives(state),
        ),
        PhoaExit(
            name="anuri_temple_side_to_main",
            region="anuri_temple(side_entrance)",
            connection="anuri_temple(main)",
            rule=lambda state: state.has("Anuri Temple - Side entrance gate opened", player),
        ),
        # anuri_temple(slargummy_boss)
        PhoaExit(
            name="anuri_temple_slargummy_to_main",
            region="anuri_temple(slargummy_boss)",
            connection="anuri_temple(main)",
            rule=lambda state: logic.can_reasonably_kill_enemies(state),
        ),
        PhoaExit(
            name="anuri_temple_slargummy_to_pond",
            region="anuri_temple(slargummy_boss)",
            connection="anuri_temple(pond)",
            rule=lambda state: logic.can_reasonably_kill_enemies(state),
        ),
        # anuri_temple(pond)
        PhoaExit(
            name="anuri_temple_to_post_pond",
            region="anuri_temple(pond)",
            connection="anuri_temple(post_pond)",
            rule=lambda state: logic.has_anuri_pearlstones(9, state),
        ),
        # anuri_temple(post_pond)
        PhoaExit(
            name="anuri_temple_to_dive_room",
            region="anuri_temple(post_pond)",
            connection="anuri_temple(dive_room)",
            rule=lambda state: logic.has_anuri_pearlstones(10, state),
        ),
        PhoaExit(
            name="anuri_temple_to_urn_room",
            region="anuri_temple(post_pond)",
            connection="anuri_temple(urn_room)",
            rule=lambda state: logic.has_bombs(state)
                               or state.has("Rocket Boots", player),
        ),
        # atai_region
        PhoaExit(
            name="atai_region_to_panselo",
            region="atai_region",
            connection="panselo_region",
        ),
        PhoaExit(
            name="atai_region_to_adars_house",
            region="atai_region",
            connection="adars_house",
        ),
        PhoaExit(
            name="atai_region_to_town",
            region="atai_region",
            connection="atai_town",
        ),
        PhoaExit(
            name="atai_region_to_sand_drifts_access_cave",
            region="atai_region",
            connection="sand_drifts_region(access_cave)",
        ),
        PhoaExit(
            name="atai_region_to_sand_drifts_region",
            region="atai_region",
            connection="sand_drifts_region",
            rule=lambda state: logic.has_explosives(state),
        ),
        # adars_house
        PhoaExit(
            name="adars_house_east_exit",
            region="adars_house",
            connection="atai_region",
        ),
        PhoaExit(
            name="adars_house_to_cave",
            region="adars_house",
            connection="adars_house(cave)",
            rule=lambda state: logic.has_explosives(state),
        ),
        PhoaExit(
            name="adars_house_to_top_of_cave",
            region="adars_house",
            connection="adars_house(cave_top)",
            rule=lambda state: state.has("Rocket Boots", player),
        ),
        # adars_house(cave)
        PhoaExit(
            name="adars_cave_to_top",
            region="adars_house(cave)",
            connection="adars_house(cave_top)",
        ),
        PhoaExit(
            name="adars_cave_to_ancient_vault",
            region="adars_house(cave)",
            connection="ancient_vault",
            rule=lambda state: logic.has_light_source(state)
                               and logic.has_explosives(state)
                               and state.has("Spheralis", player),
        ),
        # adars_house(cave_top)
        PhoaExit(
            name="adar_top_of_cave_to_main_cave",
            region="adars_house(cave_top)",
            connection="adars_house(cave)",
            rule=lambda state: logic.has_explosives(state),
        ),
        # ancient_vault
        PhoaExit(
            name="ancient_vault_to_printer_room",
            region="ancient_vault",
            connection="ancient_vault(printer_room)",
            rule=lambda state: logic.can_clear_ancient_vault(state),
        ),
        # atai_town
        PhoaExit(
            name="atai_town_exit",
            region="atai_town",
            connection="atai_region",
        ),
        PhoaExit(
            name="atai_town_to_weapon_shop_dropper",
            region="atai_town",
            connection="atai_town(weapons_shop_dropper)",
            rule=lambda state: state.has("Rocket Boots", player),
        ),
        PhoaExit(
            name="atai_town_to_sewer",
            region="atai_town",
            connection="atai_town(sewer)",
            rule=lambda state: logic.has_light_source(state),
        ),
        # atai_town(metro)
        PhoaExit(
            name="atai_town_metro_to_sand_drifts",
            region="atai_town(metro)",
            connection="sand_drifts(metro_stairwell)",
            rule=lambda state: state.has("Ouro Guard Key", player, 5),
        ),
        PhoaExit(
            name="atai_metro_to_town",
            region="atai_town(metro)",
            connection="atai_town(sewer)",
            rule=lambda state: logic.has_light_source(state),
        ),
        # atai_town(sewer)
        PhoaExit(
            name="atai_sewer_to_town",
            region="atai_town(sewer)",
            connection="atai_town",
        ),
        PhoaExit(
            name="atai_sewer_to_metro",
            region="atai_town(sewer)",
            connection="atai_town(metro)",
            rule=lambda state: state.has_any({"Life Saver", "Rocket Boots"}, player),
        ),
        # sand_drifts_region(access_cave)
        PhoaExit(
            name="sand_drifts_access_cave_to_atai_region",
            region="sand_drifts_region(access_cave)",
            connection="atai_region",
        ),
        PhoaExit(
            name="sand_drifts_access_cave_to_sand_drifts_region",
            region="sand_drifts_region(access_cave)",
            connection="sand_drifts_region",
            rule=lambda state: logic.has_music_instrument(state)
                               and state.has("Song of Ouroboros", player),
        ),
        # sand_drifts_region
        PhoaExit(
            name="sand_drifts_region_to_access_cave",
            region="sand_drifts_region",
            connection="sand_drifts_region(access_cave)",
            rule=lambda state: logic.has_music_instrument(state)
                               and state.has("Song of Ouroboros", player),
        ),
        PhoaExit(
            name="sand_drifts_region_to_ancient_geo_dungeon",
            region="sand_drifts_region",
            connection="sand_drifts_region(ancient_geo_dungeon)",
            rule=lambda state: logic.has_music_instrument(state)
                               or (logic.has_sonic_spear(state)
                                   and state.has_any({"Life Saver", "Rocket Boots"}, player)),
        ),
        PhoaExit(
            name="sand_drifts_region_to_main",
            region="sand_drifts_region",
            connection="sand_drifts",
        ),
        # sand_drifts
        PhoaExit(
            name="sand_drifts_east_exit",
            region="sand_drifts",
            connection="sand_drifts_region",
        ),
        PhoaExit(
            name="sand_drifts_to_metro_stairwell",
            region="sand_drifts",
            connection="sand_drifts(metro_stairwell)",
            rule=lambda state: logic.has_explosives(state),
        ),
        PhoaExit(
            name="sand_drifts_to_ouroboros_hideout_tower_top",
            region="sand_drifts",
            connection="ouroboros_hideout(tower_top)",
            rule=lambda state: logic.has_sonic_spear(state)
                               or state.has("Rocket Boots", player),
        ),
        PhoaExit(
            name="sand_drifts_to_chest_trap",
            region="sand_drifts",
            connection="sand_drifts(chest_trap_room)",
            rule=lambda state: logic.can_deal_damage(state, exclude_lamp=True),
        ),
        PhoaExit(
            name="sand_drifts_to_storage_room",
            region="sand_drifts",
            connection="sand_drifts(storage_room)",
            rule=lambda state: logic.can_deal_damage(state, exclude_lamp=True),
        ),
        PhoaExit(
            name="sand_drifts_to_shrine",
            region="sand_drifts",
            connection="sand_drifts(ouroboros_shrine)",
            rule=lambda state: logic.has_music_instrument(state)
                               and state.has_all({"Song of Ouroboros", "Rocket Boots"}, player),
        ),
        PhoaExit(
            name="sand_drifts_to_forlorn_ruins",
            region="sand_drifts",
            connection="forlorn_ruins",
            rule=lambda state: logic.has_music_instrument(state)
                               and state.has("Song of Ouroboros", player),
        ),
        PhoaExit(
            name="sand_drifts_to_forlorn_ruins_top_path",
            region="sand_drifts",
            connection="forlorn_ruins(top_path)",
            rule=lambda state: state.has("Rocket Boots", player),
        ),
        # sand_drifts(metro_stairwell)
        # Could use an exit to ouroboros hideout but logic doesn't require one
        PhoaExit(
            name="sand_drifts_metro_stairwell_to_main",
            region="sand_drifts(metro_stairwell)",
            connection="sand_drifts",
        ),
        PhoaExit(
            name="sand_drifts_metro_stairwell_to_atai_metro",
            region="sand_drifts(metro_stairwell)",
            connection="atai_town(metro)",
            rule=lambda state: state.has("Ouro Guard Key", player, 5),
        ),
        # ouroboros_hideout(tower_top)
        PhoaExit(
            name="ouroboros_tower_top_to_sand_drifts",
            region="ouroboros_hideout(tower_top)",
            connection="sand_drifts",
        ),
        PhoaExit(
            name="ouroboros_tower_downwards",
            region="ouroboros_hideout(tower_top)",
            connection="ouroboros_hideout(tower)",
            one_way=True,
        ),
        # ouroboros_hideout(tower)
        PhoaExit(
            name="ouroboros_hideout_tower_to_top",
            region="ouroboros_hideout(tower)",
            connection="ouroboros_hideout(tower_top)",
            rule=lambda state: logic.has_sonic_spear(state),
        ),
        PhoaExit(
            name="ouroboros_hideout_tower_to_main",
            region="ouroboros_hideout(tower)",
            connection="ouroboros_hideout",
        ),
        # forlorn_ruins(top_path)
        PhoaExit(
            name="forlorn_ruins_top_path_to_main",
            region="forlorn_ruins(top_path)",
            connection="forlorn_ruins",
            one_way=True,
        ),
        PhoaExit(
            name="forlorn_ruins_top_path_to_fountain",
            region="forlorn_ruins(top_path)",
            connection="forlorn_ruins(fountain_room)",
            rule=lambda state: state.has("Rocket Boots", player)
                               or logic.has_sonic_spear(state),
            one_way=True,
        ),
        # forlorn_ruins(fountain_room)
        PhoaExit(
            name="forlorn_ruins_fountain_to_main",
            region="forlorn_ruins(fountain_room)",
            connection="forlorn_ruins",
        ),
        PhoaExit(
            name="forlorn_ruins_fountain_to_top_path",
            region="forlorn_ruins(fountain_room)",
            connection="forlorn_ruins(top_path)",
            rule=lambda state: logic.has_sonic_spear(state),
        ),
        # forlorn_ruins
        PhoaExit(
            name="forlorn_ruins_to_top_path",
            region="forlorn_ruins",
            connection="forlorn_ruins(top_path)",
            rule=lambda state: logic.has_sonic_spear(state),
        ),
        PhoaExit(
            name="forlorn_ruins_to_fountain",
            region="forlorn_ruins",
            connection="forlorn_ruins(fountain_room)",
            rule=lambda state: logic.can_reasonably_kill_enemies(state),
        ),
        PhoaExit(
            name="forlorn_ruins_to_bombable_wall",
            region="forlorn_ruins",
            connection="forlorn_ruins(bombable_wall)",
            rule=lambda state: logic.has_explosives(state),
        ),
        PhoaExit(
            name="forlorn_ruins_through_key_door_to_obstacle_course",
            region="forlorn_ruins",
            connection="forlorn_ruins(arrow_obstacle_room)",
            rule=lambda state: state.has("Ouro Guard Key", player, 5),
        ),
        PhoaExit(
            name="forlorn_ruins_to_metal_crates_puzzle_area",
            region="forlorn_ruins",
            connection="forlorn_ruins(metal_crates_puzzle_area)",
            rule=lambda state: logic.has_bombs(state)
                               or logic.has_sonic_spear(state),
        ),
        # forlorn_ruins(metal_crates_puzzle_area)
        PhoaExit(
            name="forlorn_ruins_puzzle_area_to_main",
            region="forlorn_ruins(metal_crates_puzzle_area)",
            connection="forlorn_ruins",
            one_way=True,
        ),
        PhoaExit(
            name="forlorn_ruins_puzzle_area_to_trap_switches",
            region="forlorn_ruins(metal_crates_puzzle_area)",
            connection="forlorn_ruins(trap_switches_puzzle_area)",
            rule=lambda state: logic.has_explosives(state),
        ),
        # forlorn_ruins(trap_switches_puzzle_area)
        PhoaExit(
            name="forlorn_ruins_trap_switches_to_metal_creates_puzzle_area",
            region="forlorn_ruins(trap_switches_puzzle_area)",
            connection="forlorn_ruins(metal_crates_puzzle_area)",
            rule=lambda state: logic.has_explosives(state),
        ),
        PhoaExit(
            name="forlorn_ruins_trap_switches_puzzle_area_to_east",
            region="forlorn_ruins(trap_switches_puzzle_area)",
            connection="forlorn_ruins(east)",
            rule=lambda state: logic.has_slingshot(state)
                               or logic.has_bombs(state)
                               or state.has("Kobold Blaster", player)
                               or logic.has_sonic_spear(state),
        ),
        # forlorn_ruins(east)
        PhoaExit(
            name="forlorn_ruins_east_to_trap_switches_puzzle_area",
            region="forlorn_ruins(east)",
            connection="forlorn_ruins(trap_switches_puzzle_area)",
            one_way=True,
        ),
        PhoaExit(
            name="forlorn_ruins_east_key_door_in_basement",
            region="forlorn_ruins(east)",
            connection="forlorn_ruins(dragon_snare_puzzle_room)",
            rule=lambda state: state.has("Ouro Guard Key", player, 5),
        ),
        PhoaExit(
            name="forlorn_ruins_to_ouroboros_hideout",
            region="forlorn_ruins(east)",
            connection="ouroboros_hideout",
            rule=lambda state: logic.has_explosives(state)
                               and logic.has_music_instrument(state)
                               and state.has("Song of Ouroboros", player),
        ),
        # ouroboros_hideout
        PhoaExit(
            name="ouroboros_hideout_to_forlorn_ruins",
            region="ouroboros_hideout",
            connection="forlorn_ruins(east)",
            rule=lambda state: logic.has_explosives(state)
                               and logic.has_music_instrument(state)
                               and state.has("Song of Ouroboros", player),
        ),
        PhoaExit(
            name="ouroboros_hideout_to_prison",
            region="ouroboros_hideout",
            connection="ouroboros_hideout(prison)",
            rule=lambda state: state.has("Ouro Guard Key", player, 5),
        ),
        PhoaExit(
            name="ouroboros_hideout_to_storage",
            region="ouroboros_hideout",
            connection="ouroboros_hideout(storage)",
            rule=lambda state: state.has("Ouro Guard Key", player, 5),
        ),
        PhoaExit(
            name="ouroboros_hideout_to_infant_drake_arena",
            region="ouroboros_hideout",
            connection="ouroboros_hideout(infant_drake_arena)",
            rule=lambda state: logic.can_reasonably_kill_enemies(state, exclude_slingshot=True),
        ),
        PhoaExit(
            name="ouroboros_hideout_to_treasure_room",
            region="ouroboros_hideout",
            connection="ouroboros_hideout(treasure_room)",
            rule=lambda state: logic.has_music_instrument(state),
        ),
        PhoaExit(
            name="sand_drifts_metro_stairwell_to_ouroboros_hideout",
            region="ouroboros_hideout",
            connection="sand_drifts(metro_stairwell)",
            rule=lambda state: logic.has_bat(state)
                               or state.has("Kobold Blaster", player),
        ),
        PhoaExit(
            name="ouroboros_hideout_to_great_drake_arena",
            region="ouroboros_hideout",
            connection="ouroboros_hideout(great_drake_arena)",
            rule=lambda state: state.has("Ouroboros Proof", player, 3),
        ),
        # ouroboros_hideout(storage)
        PhoaExit(
            name="ouroboros_hideout_storage_to_back_side",
            region="ouroboros_hideout(storage)",
            connection="ouroboros_hideout(storage_back)",
            rule=lambda state: logic.has_bombs(state),
        ),
        # ouroboros_hideout(treasure_room)
        PhoaExit(
            name="ouroboros_hideout_treasure_room_to_hidden_area",
            region="ouroboros_hideout(treasure_room)",
            connection="ouroboros_hideout(treasure_room_hidden_area)",
            rule=lambda state: logic.has_explosives(state),
        ),
        # ouroboros_hideout(great_drake_arena)
    ]

    return exits


def create_regions_and_locations(world: MultiWorld, player: int, options: PhoaOptions):
    locations_per_region: Dict[str, Dict[str, PhoaLocationData]] = split_locations_per_region(
        get_location_data(player, options))

    regions = [
        create_region(world, player, locations_per_region, "Menu"),
        create_region(world, player, locations_per_region, "panselo_village"),
        create_region(world, player, locations_per_region, "panselo_village_rutea's_lab"),
        create_region(world, player, locations_per_region, "panselo_region"),
        create_region(world, player, locations_per_region, "anuri_temple(main_entrance)"),
        create_region(world, player, locations_per_region, "anuri_temple(top_floor)"),
        create_region(world, player, locations_per_region, "anuri_temple(scaber_switch_maze)"),
        create_region(world, player, locations_per_region, "anuri_temple(main)"),
        create_region(world, player, locations_per_region, "anuri_temple(tall_tower_puzzle_room)"),
        create_region(world, player, locations_per_region, "anuri_temple(side_entrance)"),
        create_region(world, player, locations_per_region, "anuri_temple(basement)"),
        create_region(world, player, locations_per_region, "anuri_temple(moveable_bridge_area)"),
        create_region(world, player, locations_per_region, "anuri_temple(slargummy_boss)"),
        create_region(world, player, locations_per_region, "anuri_temple(pond)"),
        create_region(world, player, locations_per_region, "anuri_temple(post_pond)"),
        create_region(world, player, locations_per_region, "anuri_temple(dive_room)"),
        create_region(world, player, locations_per_region, "anuri_temple(urn_room)"),
        create_region(world, player, locations_per_region, "atai_region"),
        create_region(world, player, locations_per_region, "adars_house"),
        create_region(world, player, locations_per_region, "atai_town"),
        create_region(world, player, locations_per_region, "atai_town(sewer)"),
        create_region(world, player, locations_per_region, "atai_town(weapons_shop_dropper)"),
        create_region(world, player, locations_per_region, "atai_town(metro)"),
        create_region(world, player, locations_per_region, "adars_house(cave)"),
        create_region(world, player, locations_per_region, "adars_house(cave_top)"),
        create_region(world, player, locations_per_region, "ancient_vault"),
        create_region(world, player, locations_per_region, "ancient_vault(printer_room)"),
        create_region(world, player, locations_per_region, "sand_drifts_region(access_cave)"),
        create_region(world, player, locations_per_region, "sand_drifts_region"),
        create_region(world, player, locations_per_region, "sand_drifts_region(ancient_geo_dungeon)"),
        create_region(world, player, locations_per_region, "sand_drifts"),
        create_region(world, player, locations_per_region, "sand_drifts(metro_stairwell)"),
        create_region(world, player, locations_per_region, "sand_drifts(chest_trap_room)"),
        create_region(world, player, locations_per_region, "sand_drifts(storage_room)"),
        create_region(world, player, locations_per_region, "sand_drifts(ouroboros_shrine)"),
        create_region(world, player, locations_per_region, "forlorn_ruins"),
        create_region(world, player, locations_per_region, "forlorn_ruins(top_path)"),
        create_region(world, player, locations_per_region, "forlorn_ruins(fountain_room)"),
        create_region(world, player, locations_per_region, "forlorn_ruins(bombable_wall)"),
        create_region(world, player, locations_per_region, "forlorn_ruins(arrow_obstacle_room)"),
        create_region(world, player, locations_per_region, "forlorn_ruins(metal_crates_puzzle_area)"),
        create_region(world, player, locations_per_region, "forlorn_ruins(trap_switches_puzzle_area)"),
        create_region(world, player, locations_per_region, "forlorn_ruins(east)"),
        create_region(world, player, locations_per_region, "forlorn_ruins(dragon_snare_puzzle_room)"),
        create_region(world, player, locations_per_region, "ouroboros_hideout"),
        create_region(world, player, locations_per_region, "ouroboros_hideout(tower_top)"),
        create_region(world, player, locations_per_region, "ouroboros_hideout(tower)"),
        create_region(world, player, locations_per_region, "ouroboros_hideout(prison)"),
        create_region(world, player, locations_per_region, "ouroboros_hideout(storage)"),
        create_region(world, player, locations_per_region, "ouroboros_hideout(storage_back)"),
        create_region(world, player, locations_per_region, "ouroboros_hideout(infant_drake_arena)"),
        create_region(world, player, locations_per_region, "ouroboros_hideout(treasure_room)"),
        create_region(world, player, locations_per_region, "ouroboros_hideout(treasure_room_hidden_area)"),
        create_region(world, player, locations_per_region, "ouroboros_hideout(great_drake_arena)"),
    ]

    world.regions += regions

    connect_regions(world, player, get_exit_data(player, options))


def create_region(world: MultiWorld, player: int, locations_per_region: Dict[str, Dict[str, PhoaLocationData]],
                  name: str) -> Region:
    region = Region(name, player, world)

    if name in locations_per_region:
        for location_name, location_data in locations_per_region[name].items():
            location = create_location(player, location_name, location_data, region)
            region.locations.append(location)

    return region


def create_location(player: int, location_name: str, location_data: PhoaLocationData, region: Region):
    location = Location(player, location_name, location_data.address, region)

    if location_data.rule:
        location.access_rule = location_data.rule

    return location


def connect_regions(world: MultiWorld, player: int, exits: list[PhoaExit]):
    for regionExit in exits:
        connect(world, player, regionExit.region, regionExit.connection, regionExit.rule, regionExit.name)


def connect(world: MultiWorld, player: int, source: str, target: str,
            rule: Optional[Callable[[CollectionState], bool]] = None, name: str = None):
    source_region = world.get_region(source, player)
    target_region = world.get_region(target, player)
    entrance = source_region.create_exit(name)

    if rule is not None:
        entrance.access_rule = rule

    entrance.connect(target_region)


def split_locations_per_region(locations: Dict[str, PhoaLocationData]):
    locations_per_region: Dict[str, Dict[str, PhoaLocationData]] = {}

    for location_name, location_data in locations.items():
        if location_data.region not in locations_per_region:
            locations_per_region[location_data.region] = {}

        locations_per_region[location_data.region][location_name] = location_data

    return locations_per_region
