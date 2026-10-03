from typing import Any, Iterable, cast

from BaseClasses import Item, ItemClassification, Location, LocationProgressType, Region

from ..data.Constants import (
    ESSENCES,
    LOCATION_GROUPS,
    RUPEE_OLD_MAN_LOCATIONS,
    SCRUB_LOCATIONS,
    SECRETS,
    SUBROSIA_HIDDEN_DIGGING_SPOTS_LOCATIONS,
)
from ..data.locations import LOCATIONS_DATA
from ..data.regions import (
    D11_REGIONS,
    GASHA_REGIONS,
    GASHA_SPOT_REGIONS,
    NATZU_REGIONS,
    SCRUB_REGIONS,
    SECRET_REGIONS,
    RegionNames,
)
from ..options import (
    OracleOfSeasonsGoal,
    OracleOfSeasonsLogicDifficulty,
    OracleOfSeasonsOldMenShuffle,
    OracleOfSeasonsStartingPosition,
)
from ..world import OracleOfSeasonsWorld


def location_is_active(world: OracleOfSeasonsWorld, location_name: str, location_data: dict[str, Any]) -> Any:
    if not location_data.get("conditional", False):
        return True

    region_id = location_data["region_id"]
    if region_id == "advance shop":
        return world.options.advance_shop
    if location_name in SUBROSIA_HIDDEN_DIGGING_SPOTS_LOCATIONS:
        return world.options.shuffle_golden_ore_spots
    if location_name in RUPEE_OLD_MAN_LOCATIONS:
        return world.options.shuffle_old_men == OracleOfSeasonsOldMenShuffle.option_turn_into_locations
    if location_name in SCRUB_LOCATIONS:
        return world.options.shuffle_business_scrubs
    if location_name.startswith("Gasha Nut #"):
        return int(location_name[11:]) <= world.options.deterministic_gasha_locations
    if location_name == "Horon Village: Item Inside Maku Tree (3+ Essences)":
        return len(world.essences_in_game) >= 3
    if location_name == "Horon Village: Item Inside Maku Tree (5+ Essences)":
        return len(world.essences_in_game) >= 5
    if location_name == "Horon Village: Item Inside Maku Tree (7+ Essences)":
        return len(world.essences_in_game) >= 7
    if location_name in SECRETS:
        return world.options.secret_locations
    if location_name in LOCATION_GROUPS["D11"]:
        return world.options.linked_heros_cave
    if "owl_id" in location_data:
        return world.options.bird_hint.owl()
    return False


def create_location(
        world: OracleOfSeasonsWorld, region_name: str, location_name: str, local: bool, event: bool
) -> Location:
    region = world.multiworld.get_region(region_name, world.player)
    location_id = None if event else world.location_name_to_id[location_name]
    location = Location(world.player, location_name, location_id, region)
    region.locations.append(location)
    if local:
        location.item_rule = lambda item: item.player == world.player
    return location


def create_regions(world: OracleOfSeasonsWorld) -> None:
    # Create regions
    for region_name in cast(Iterable[RegionNames], RegionNames):
        region = Region(region_name, world.player, world.multiworld)
        world.multiworld.regions.append(region)

    for region_name in NATZU_REGIONS[world.options.animal_companion.current_key]:
        region = Region(region_name, world.player, world.multiworld)
        world.multiworld.regions.append(region)

    if world.options.advance_shop:
        region = Region("advance shop", world.player, world.multiworld)
        world.multiworld.regions.append(region)

    if world.options.logic_difficulty == OracleOfSeasonsLogicDifficulty.option_hell:
        region = Region("rooster adventure", world.player, world.multiworld)
        world.multiworld.regions.append(region)

    if world.options.deterministic_gasha_locations > 0:
        for i in range(world.options.deterministic_gasha_locations):
            region = Region(GASHA_REGIONS[i], world.player, world.multiworld)
            world.multiworld.regions.append(region)
        for region_name in GASHA_SPOT_REGIONS:
            region = Region(region_name, world.player, world.multiworld)
            world.multiworld.regions.append(region)

    if world.options.shuffle_business_scrubs:
        for region_name in SCRUB_REGIONS:
            region = Region(region_name, world.player, world.multiworld)
            world.multiworld.regions.append(region)

    if world.options.secret_locations:
        for region_name in SECRET_REGIONS:
            region = Region(region_name, world.player, world.multiworld)
            world.multiworld.regions.append(region)

    if world.options.linked_heros_cave:
        for region_name in D11_REGIONS:
            world.multiworld.regions.append(Region(region_name, world.player, world.multiworld))

    # Create locations
    for location_name, location_data in LOCATIONS_DATA.items():
        if not location_is_active(world, location_name, location_data):
            continue

        is_local = "local" in location_data and location_data["local"] is True
        is_owl = "owl_id" in location_data
        location = create_location(world, location_data["region_id"], location_name, is_local, is_owl)
        if is_owl:
            location.place_locked_item(Item("Hint", ItemClassification.filler, None, world.player))

    create_events(world)
    exclude_locations_automatically(world)

    if world.options.start_position == OracleOfSeasonsStartingPosition.option_horon_village:
        world.origin_region_name = RegionNames.impas_house
    elif world.options.start_position == OracleOfSeasonsStartingPosition.option_sunken_city:
        world.origin_region_name = RegionNames.sunken_city
        inventory_location = create_location(world, world.origin_region_name, "Server", True, True)
        inventory_location.address = -2
        inventory_location.show_in_spoiler = False
        inventory_location_2 = create_location(world, world.origin_region_name, "Cheat Console", True, True)
        inventory_location_2.address = -1
        inventory_location_2.show_in_spoiler = False
        world.inventory_locations = [inventory_location, inventory_location_2]
    elif world.options.start_position == OracleOfSeasonsStartingPosition.option_samasa_desert:
        world.origin_region_name = RegionNames.samasa_desert
        inventory_location = create_location(world, world.origin_region_name, "Server", True, True)
        inventory_location.address = -2
        inventory_location.show_in_spoiler = False
        inventory_location_2 = create_location(world, world.origin_region_name, "Cheat Console", True, True)
        inventory_location_2.address = -1
        inventory_location_2.show_in_spoiler = False
        world.inventory_locations = [inventory_location, inventory_location_2]
    elif world.options.start_position == OracleOfSeasonsStartingPosition.option_temple_of_seasons:
        world.origin_region_name = RegionNames.subrosia_temple_sector
    elif world.options.start_position == OracleOfSeasonsStartingPosition.option_tarm_entrance:
        world.origin_region_name = RegionNames.spool_swamp_north
        inventory_location = create_location(world, world.origin_region_name, "Server", True, True)
        inventory_location.address = -2
        inventory_location.show_in_spoiler = False
        inventory_location_2 = create_location(world, world.origin_region_name, "Cheat Console", True, True)
        inventory_location_2.address = -1
        inventory_location_2.show_in_spoiler = False
        world.inventory_locations = [inventory_location, inventory_location_2]
    else:
        raise NotImplementedError


def create_event(world: OracleOfSeasonsWorld, region_name: str, event_item_name: str) -> None:
    region = world.multiworld.get_region(region_name, world.player)
    location = Location(world.player, region_name + f".{event_item_name}", None, region)
    region.locations.append(location)
    location.place_locked_item(Item(event_item_name, ItemClassification.progression, None, world.player))


def create_events(world: OracleOfSeasonsWorld) -> None:
    # Events for beating golden beasts
    create_event(world, "golden darknut", "_beat_golden_darknut")
    create_event(world, "golden lynel", "_beat_golden_lynel")
    create_event(world, "golden octorok", "_beat_golden_octorok")
    create_event(world, "golden moblin", "_beat_golden_moblin")
    # Events for "wild" seeds that can be found inside respawnable bushes in dungeons
    create_event(world, "d2 wild bombs", "_wild_bombs")
    create_event(world, "d4 miniboss room wild embers", "_wild_ember_seeds")
    create_event(world, "d5 armos chest", "_wild_ember_seeds")
    create_event(world, "d5 armos chest", "_wild_bombs")
    create_event(world, "d7 entrance wild embers", "_wild_ember_seeds")
    create_event(world, "frypolar room wild mystery", "_wild_mystery_seeds")
    # Various events to help with logic
    create_event(world, "bomb temple remains", "_triggered_volcano")
    create_event(world, "subrosia pirates sector", "_met_pirates")
    if world.options.logic_difficulty >= OracleOfSeasonsLogicDifficulty.option_medium:
        create_event(world, "d2 rupee room", "_reached_d2_rupee_room")
        create_event(world, "d6 rupee room", "_reached_d6_rupee_room")
    create_event(world, "maku seed", "Maku Seed")

    if world.options.goal == OracleOfSeasonsGoal.option_beat_onox:
        create_event(world, "onox beaten", "_beaten_game")
    elif world.options.goal == OracleOfSeasonsGoal.option_beat_ganon:
        create_event(world, "ganon beaten", "_beaten_game")

    # Create events for reaching Gasha spots, used when Gasha-sanity is on
    if world.options.deterministic_gasha_locations > 0:
        for region_name in GASHA_SPOT_REGIONS:
            create_event(world, region_name, f"_reached_{region_name}")

    # Create event items to represent rupees obtained from Old Men, unless they are turned into locations
    if world.options.shuffle_old_men != OracleOfSeasonsOldMenShuffle.option_turn_into_locations:
        for region_name in world.old_man_rupee_values:
            create_event(world, region_name, "rupees from " + region_name)


def exclude_locations_automatically(world: OracleOfSeasonsWorld) -> None:
    locations_to_exclude = set()
    # If goal essence requirement is set to a specific value, prevent essence-bound checks which require more
    # essences than this goal to hold anything of value
    if world.options.required_essences < 7 <= len(world.essences_in_game):
        locations_to_exclude.add("Horon Village: Item Inside Maku Tree (7+ Essences)")
        if world.options.required_essences < 5 <= len(world.essences_in_game):
            locations_to_exclude.add("Horon Village: Item Inside Maku Tree (5+ Essences)")
            if world.options.required_essences < 3 <= len(world.essences_in_game):
                locations_to_exclude.add("Horon Village: Item Inside Maku Tree (3+ Essences)")
    if world.options.required_essences < world.options.treehouse_old_man_requirement:
        locations_to_exclude.add("Holodrum Plain: Old Man in Treehouse")

    # If dungeons without essence need to be excluded, do it if conditions are met
    if world.options.exclude_dungeons_without_essence and not world.options.shuffle_essences:
        for i, essence_name in enumerate(ESSENCES):
            if essence_name not in world.essences_in_game:
                locations_to_exclude.update(world.location_name_groups[f"D{i + 1}"])

    if not world.options.shuffle_business_scrubs:
        locations_to_exclude.difference_update(SCRUB_LOCATIONS)

    if world.options.randomize_ai:
        locations_to_exclude.add("Western Coast: Black Beast's Chest")

    for name in locations_to_exclude:
        world.multiworld.get_location(name, world.player).progress_type = LocationProgressType.EXCLUDED
