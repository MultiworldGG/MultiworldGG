from BaseClasses import MultiWorld, Region, ItemClassification, LocationProgressType
from .enums import Locations, Regions, Events

from .levels import boss_connections, level_map, regional_events, level_region_data
from .locations import DKC3Location
from .items import DKC3Item
from .options import Goal

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import DKC3World


def create_regions(world: "DKC3World", active_locations):
    multiworld = world.multiworld
    player = world.player

    multiworld.regions += [
        Region(Regions.lake_orangatanga.value, player, multiworld),
        Region(Regions.kremwood_forest.value, player, multiworld),
        Region(Regions.cotton_top_cove.value, player, multiworld),
        Region(Regions.mekanos.value, player, multiworld),
        Region(Regions.k3.value, player, multiworld),
        Region(Regions.razor_ridge.value, player, multiworld),
        Region(Regions.kaos_kore.value, player, multiworld),
        Region(Regions.krematoa.value, player, multiworld),

        Region(Regions.northern_kremisphere_south.value, player, multiworld),
        Region(Regions.northern_kremisphere_center.value, player, multiworld),
        Region(Regions.northern_kremisphere_north.value, player, multiworld),
        Region(Regions.northern_kremisphere_flying.value, player, multiworld),
        Region(Regions.northern_kremisphere_kore.value, player, multiworld),
    ]

    active_kong_checks = world.options.kong_checks.value
    active_dk_coin_checks = world.options.dk_coin_checks.value
    active_balloon_checks = world.options.balloon_checks.value
    active_coin_checks = world.options.coin_checks.value
    active_banana_checks = world.options.banana_checks.value

    for region_name, region_data in level_region_data.items():
        region = Region(region_name.value, player, multiworld)
        region_map =  Region(region_name.value.replace(": Level", ": Map"), player, multiworld)
        multiworld.regions += [region, region_map]

        for loc_type, locations in region_data.items():
            if loc_type == "KONG" and not active_kong_checks:
                continue
            elif loc_type == "DK Coin" and not active_dk_coin_checks:
                continue
            elif loc_type == "Balloons" and not active_balloon_checks:
                continue
            elif loc_type == "Coins" and not active_coin_checks:
                continue
            elif loc_type == "Bananas" and not active_banana_checks:
                continue
            for location in locations:
                loc_id = active_locations.get(location, 0)
                if loc_id:
                    region.locations.append(DKC3Location(player, location, loc_id, region))

    add_location_to_region(multiworld, player, active_locations, Regions.belchas_barn_level, Locations.defeated_belcha)
    add_location_to_region(multiworld, player, active_locations, Regions.arichs_ambush_level, Locations.defeated_arich)
    add_location_to_region(multiworld, player, active_locations, Regions.squirt_showdown_level, Locations.defeated_squirt)
    add_location_to_region(multiworld, player, active_locations, Regions.kaos_karnage_level, Locations.defeated_kaos)
    add_location_to_region(multiworld, player, active_locations, Regions.bleaks_house_level, Locations.defeated_bleak)
    add_location_to_region(multiworld, player, active_locations, Regions.barbos_barrier_level, Locations.defeated_barbos)

    if world.options.bird_checks:
        add_location_to_region(multiworld, player, active_locations, Regions.northern_kremisphere_south, Locations.bird_bounty_beach)
        add_location_to_region(multiworld, player, active_locations, Regions.northern_kremisphere_center, Locations.bird_kong_cave)
        add_location_to_region(multiworld, player, active_locations, Regions.northern_kremisphere_north, Locations.bird_undercover_cove)
        add_location_to_region(multiworld, player, active_locations, Regions.northern_kremisphere_flying, Locations.bird_belchas_burrow)
        add_location_to_region(multiworld, player, active_locations, Regions.northern_kremisphere_flying, Locations.bird_ks_kache)
        add_location_to_region(multiworld, player, active_locations, Regions.northern_kremisphere_flying, Locations.bird_hill_top_hoard)
        add_location_to_region(multiworld, player, active_locations, Regions.lake_orangatanga, Locations.bird_smugglers_cove)
        add_location_to_region(multiworld, player, active_locations, Regions.kremwood_forest, Locations.bird_arichs_hoard)
        add_location_to_region(multiworld, player, active_locations, Regions.cotton_top_cove, Locations.bird_bounty_bay)
        #add_location_to_region(multiworld, player, active_locations, Regions.mekanos, Locations.bird_sky_high_secret)
        add_location_to_region(multiworld, player, active_locations, Regions.k3, Locations.bird_glacial_grotto)
        #add_location_to_region(multiworld, player, active_locations, Regions.razor_ridge, Locations.bird_clifftop_cache)
        add_location_to_region(multiworld, player, active_locations, Regions.kaos_kore, Locations.bird_sewer_stockpile)

    # Level clears (Events)
    regional_event_count: dict[str, int] = {
        Regions.lake_orangatanga: 0,
        Regions.kremwood_forest: 0,
        Regions.cotton_top_cove: 0,
        Regions.mekanos: 0,
        Regions.k3: 0,
        Regions.razor_ridge: 0,
        Regions.kaos_kore: 0,
        Regions.krematoa: 0,
    }
    for map_level, level in world.level_connections.items():
        current_world = level_map[map_level]
        if map_level in boss_connections.keys():
            continue
        level_clear = level_region_data[level]["Clear"][0]
        if level_clear in world.options.exclude_locations.value:
            continue
        event_name = level.replace(": Level", " - Clear (Map Event)")
        event_item = regional_events[current_world]
        regional_event_count[current_world] += 1
        add_event_to_region(multiworld, player, level, event_name, event_item)

    # Reduce level clears in case a lot of levels are excluded per world
    world.options.required_lake_levels.value = min(world.options.required_lake_levels.value, regional_event_count[Regions.lake_orangatanga])
    world.options.required_forest_levels.value = min(world.options.required_forest_levels.value, regional_event_count[Regions.kremwood_forest])
    world.options.required_cove_levels.value = min(world.options.required_cove_levels.value, regional_event_count[Regions.cotton_top_cove])
    world.options.required_mekanos_levels.value = min(world.options.required_mekanos_levels.value, regional_event_count[Regions.mekanos])
    world.options.required_k3_levels.value = min(world.options.required_k3_levels.value, regional_event_count[Regions.k3])
    world.options.required_ridge_levels.value = min(world.options.required_ridge_levels.value, regional_event_count[Regions.razor_ridge])
    world.options.required_kore_levels.value = min(world.options.required_kore_levels.value, regional_event_count[Regions.kaos_kore])
    world.options.required_krematoa_levels.value = min(world.options.required_krematoa_levels.value, regional_event_count[Regions.krematoa])

    # Goal regions
    # TODO: Banana :b:ird hunt
    if world.options.goal != Goal.option_krematoa:
        add_event_to_region(multiworld, player, Regions.kastle_kaos_level, Locations.kastle_kaos_clear, Events.k_rool_at_kore)

    if world.options.goal != Goal.option_kore:
        add_event_to_region(multiworld, player, Regions.knautilus_level, Locations.knautilus_clear, Events.k_rool_at_knautilus)


def connect_regions(world: "DKC3World"):
    connect(world, Regions.northern_kremisphere_south, Regions.northern_kremisphere_center)
    connect(world, Regions.northern_kremisphere_center, Regions.northern_kremisphere_north)
    connect(world, Regions.northern_kremisphere_north, Regions.northern_kremisphere_kore)
    connect(world, Regions.northern_kremisphere_south, Regions.northern_kremisphere_flying)
    connect(world, Regions.northern_kremisphere_flying, Regions.northern_kremisphere_kore)

    connect(world, Regions.northern_kremisphere_south, Regions.lake_orangatanga)
    connect(world, Regions.northern_kremisphere_south, Regions.kremwood_forest)
    connect(world, Regions.northern_kremisphere_center, Regions.cotton_top_cove)
    connect(world, Regions.northern_kremisphere_center, Regions.mekanos)
    connect(world, Regions.northern_kremisphere_north, Regions.k3)
    connect(world, Regions.northern_kremisphere_north, Regions.razor_ridge)
    connect(world, Regions.northern_kremisphere_kore, Regions.kaos_kore)
    connect(world, Regions.northern_kremisphere_center, Regions.krematoa)

    connect(world, Regions.lake_orangatanga, Regions.lakeside_limbo_map)
    connect(world, Regions.lake_orangatanga, Regions.doorstop_dash_map)
    connect(world, Regions.lake_orangatanga, Regions.tidal_trouble_map)
    connect(world, Regions.lake_orangatanga, Regions.skiddas_row_map)
    connect(world, Regions.lake_orangatanga, Regions.murky_mill_map)
    connect(world, Regions.lake_orangatanga, Regions.belchas_barn_map)

    connect(world, Regions.kremwood_forest, Regions.barrel_shield_bust_up_map)
    connect(world, Regions.kremwood_forest, Regions.riverside_race_map)
    connect(world, Regions.kremwood_forest, Regions.squeals_on_wheels_map)
    connect(world, Regions.kremwood_forest, Regions.springing_spiders_map)
    connect(world, Regions.kremwood_forest, Regions.bobbing_barrel_brawl_map)
    connect(world, Regions.kremwood_forest, Regions.arichs_ambush_map)
    
    connect(world, Regions.cotton_top_cove, Regions.bazzas_blockade_map)
    connect(world, Regions.cotton_top_cove, Regions.rocket_barrel_ride_map)
    connect(world, Regions.cotton_top_cove, Regions.kreeping_klasps_map)
    connect(world, Regions.cotton_top_cove, Regions.tracker_barrel_trek_map)
    connect(world, Regions.cotton_top_cove, Regions.fish_food_frenzy_map)
    connect(world, Regions.cotton_top_cove, Regions.squirt_showdown_map)
    
    connect(world, Regions.mekanos, Regions.fireball_frenzy_map)
    connect(world, Regions.mekanos, Regions.demolition_drain_pipe_map)
    connect(world, Regions.mekanos, Regions.ripsaw_rage_map)
    connect(world, Regions.mekanos, Regions.blazing_bazukas_map)
    connect(world, Regions.mekanos, Regions.low_g_labyrinth_map)
    connect(world, Regions.mekanos, Regions.kaos_karnage_map)
    
    connect(world, Regions.k3, Regions.krevice_kreepers_map)
    connect(world, Regions.k3, Regions.tearaway_toboggan_map)
    connect(world, Regions.k3, Regions.barrel_drop_bounce_map)
    connect(world, Regions.k3, Regions.krackshot_krock_map)
    connect(world, Regions.k3, Regions.lemguin_lunge_map)
    connect(world, Regions.k3, Regions.bleaks_house_map)
    
    connect(world, Regions.razor_ridge, Regions.buzzer_barrage_map)
    connect(world, Regions.razor_ridge, Regions.kongfused_cliffs_map)
    connect(world, Regions.razor_ridge, Regions.floodlit_fish_map)
    connect(world, Regions.razor_ridge, Regions.pot_hole_panic_map)
    connect(world, Regions.razor_ridge, Regions.ropey_rumpus_map)
    connect(world, Regions.razor_ridge, Regions.barbos_barrier_map)
    
    connect(world, Regions.kaos_kore, Regions.konveyor_rope_klash_map)
    connect(world, Regions.kaos_kore, Regions.creepy_caverns_map)
    connect(world, Regions.kaos_kore, Regions.lightning_look_out_map)
    connect(world, Regions.kaos_kore, Regions.koindozer_klamber_map)
    connect(world, Regions.kaos_kore, Regions.poisonous_pipeline_map)
    connect(world, Regions.kaos_kore, Regions.kastle_kaos_map)

    connect(world, Regions.krematoa, Regions.stampede_sprint_map)
    connect(world, Regions.krematoa, Regions.criss_kross_cliffs_map)
    connect(world, Regions.krematoa, Regions.tyrant_twin_tussle_map)
    connect(world, Regions.krematoa, Regions.swoopy_salvo_map)
    connect(world, Regions.krematoa, Regions.rocket_rush_map)
    connect(world, Regions.krematoa, Regions.knautilus_map)

    connect(world, Regions.kastle_kaos_map, Regions.kastle_kaos_level)
    connect(world, Regions.knautilus_map, Regions.knautilus_level)
    
    for map_level, level in world.level_connections.items():
        connect(world, map_level, level)

def add_location_to_region(multiworld: MultiWorld, player: int, active_locations, region_name: Regions, location_name: Locations):
    region = multiworld.get_region(region_name.value, player)
    loc_id = active_locations.get(location_name.value, 0)
    if loc_id:
        location = DKC3Location(player, location_name.value, loc_id, region)
        region.locations.append(location)


def add_event_to_region(multiworld: MultiWorld, player: int, region_name: Regions, event_name: str, event_item=None):
    region = multiworld.get_region(str(region_name), player)
    event = DKC3Location(player, event_name, None, region)
    if event_item:
        event.place_locked_item(DKC3Item(event_item, ItemClassification.progression, None, player))
    else:
        event.place_locked_item(DKC3Item(event_name, ItemClassification.progression, None, player))
    region.locations.append(event)


def connect(world: "DKC3World", source: Regions, target: Regions):
    source_region: Region = world.multiworld.get_region(str(source), world.player)
    target_region: Region = world.multiworld.get_region(str(target), world.player)
    source_region.connect(target_region)
