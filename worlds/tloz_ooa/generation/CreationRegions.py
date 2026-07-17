

from BaseClasses import Item, Location, Region, ItemClassification, LocationProgressType
from ..data.Regions import REGIONS
from ..data.Locations import LOCATIONS_DATA
from ..data.Entrances import WARPS_DATA, OUTSIDE_TAG, INSIDE_TAG
from ..data.Constants import *
from .. import OracleOfAgesWorld
from ..Options import *

# -----------------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------------
def location_is_active(world: OracleOfAgesWorld, location_name, location_data):
    if "conditional" not in location_data or location_data["conditional"] is False:
        return True

    region_id = location_data["region_id"]
    if region_id == "advance shop":
        return world.options.advance_shop.value
    
    if "dungeon" in location_data:
        if location_data["dungeon"] == 11:
            return world.options.linked_heros_cave.value > 0
        if location_data["symbolic_name"] == f"d{location_data["dungeon"]}Miniboss":
            return world.options.miniboss_locations
        
    if "secret_location" in location_data and not False:
        return world.options.secret_locations
    
    if "vasu" in region_id:
        return not world.options.vasu_ring_checks_requirement["disable_entirely"]

    if location_name == "Lynna City: Shop Item #3":
        return world.options.enforce_potion_in_shop != OracleOfAgesEnforcePotionInShop.option_lynna_shop

    if location_name == "Yoll Graveyard: Syrup Shop Item #3":
        return world.options.enforce_potion_in_shop != OracleOfAgesEnforcePotionInShop.option_syrup_hut

    if location_name.startswith("Gasha Nut #"):
        return int(location_name[11:]) <= world.options.deterministic_gasha_locations
    
    # TODO FUNNY LOCATION ?

    return False

# -----------------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------------
def create_event(world: OracleOfAgesWorld, region_name, event_item_name):
    region = world.multiworld.get_region(region_name, world.player)
    location = Location(world.player, region_name + ".event", None, region)
    region.locations.append(location)
    location.place_locked_item(Item(event_item_name, ItemClassification.progression, None, world.player))

# -----------------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------------
def create_events(world: OracleOfAgesWorld):
    create_event(world, "maku seed", "Maku Seed")

    if world.options.goal == OracleOfAgesGoal.option_beat_veran:
        create_event(world, "veran beaten", "_beaten_game")
    elif world.options.goal == OracleOfAgesGoal.option_beat_ganon:
        create_event(world, "ganon beaten", "_beaten_game")

    create_event(world,"ridge move vine seed", "_access_cart")

    create_event(world,"d3 S crystal", "_d3_S_crystal")
    create_event(world,"d3 E crystal", "_d3_E_crystal")
    create_event(world,"d3 W crystal", "_d3_W_crystal")
    create_event(world,"d3 N crystal", "_d3_N_crystal")
    create_event(world,"d3 B1F spinner", "_d3_B1F_spinner")

    create_event(world,"d6 wall B bombed", "_d6_wall_B_bombed")
    create_event(world,"d6 canal expanded", "_d6_canal_expanded")

    create_event(world,"d7 boss", "_finished_d7")
    
    # Create events for reaching Gasha spots, used when Gasha-sanity is on
    for region_name in GASHA_SPOT_REGIONS:
        create_event(world, region_name, f"_reached_{region_name}")

# -----------------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------------
def exclude_problematic_locations(world: OracleOfAgesWorld):
    locations_to_exclude = []
    # If goal essence requirement is set to a specific value, prevent essence-bound checks which require more
    # essences than this goal to hold anything of value
    #if self.options.required_essences < 7:
    #    locations_to_exclude.append("Horon Village: Item Inside Maku Tree (7+ Essences)")
    #    if self.options.required_essences < 5:
    #        locations_to_exclude.append("Horon Village: Item Inside Maku Tree (5+ Essences)")
    #        if self.options.required_essences < 3:
    #            locations_to_exclude.append("Horon Village: Item Inside Maku Tree (3+ Essences)")

    # TODO PROBLEMATIC LOCATIONS

    for name in locations_to_exclude:
        world.multiworld.get_location(name, world.player).progress_type = LocationProgressType.EXCLUDED

# -----------------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------------
def create_location(world: OracleOfAgesWorld, region_name: str, location_name: str, local: bool):
    region = world.multiworld.get_region(region_name, world.player)
    location = Location(world.player, location_name, world.location_name_to_id[location_name], region)
    region.locations.append(location)
    if local:
        location.item_rule = lambda item: item.player == world.player

# -----------------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------------
def ooa_create_region(world: OracleOfAgesWorld):
    # Create regions
    regions = REGIONS.copy()

    for warpName, warpData in WARPS_DATA.items():
        regions.append(OUTSIDE_TAG + warpName)
        regions.append(INSIDE_TAG + warpName)

    for region_name in regions:
        region = Region(region_name, world.player, world.multiworld)
        world.multiworld.regions.append(region)
        

    if world.options.deterministic_gasha_locations > 0:
        for i in range(world.options.deterministic_gasha_locations):
            region = Region(f"gasha tree {i+1}", world.player, world.multiworld)
            world.multiworld.regions.append(region)

    # Create locations
    for location_name, location_data in LOCATIONS_DATA.items():
        if not location_is_active(world, location_name, location_data):
            continue

        is_local = "local" in location_data and location_data["local"] is True
        create_location(world, location_data['region_id'], location_name, is_local)

    create_events(world)
    exclude_problematic_locations(world)