from typing_extensions import Any

from BaseClasses import Item, ItemClassification, Location, Region, LocationProgressType
from ..Options import OraclesGoal, OraclesOldMenShuffle, OraclesLogicDifficulty
from ...data import LOCATIONS_DATA
from ...data.Constants import GASHA_SPOT_REGIONS, ITEM_GROUPS, SCRUB_LOCATIONS, RUPEE_OLD_MAN_LOCATIONS, \
    SECRETS, LOCATION_GROUPS
from ...data.Regions import REGIONS, GASHA_REGIONS, D11_REGIONS


def create_location(world, region_name: str, location_name: str, local: bool) -> None:
    """
    Creates a location for the game.

    Parameters:
        world: The world used for location creation.
        region_name (str): A region that is being used for the creation.
        location_name (str): The name of the location that is being created.
        local (bool): States whatever or not an item is local to the player.
    """
    region = world.multiworld.get_region(region_name, world.player)
    location = Location(world.player, location_name, world.location_name_to_id[location_name], region)
    region.locations.append(location)
    if local:
        location.item_rule = lambda item: item.player == world.player


def create_regions(world) -> None:
    """
    Creates regions for a game.

    Parameters:
        world: The world used to create a region.
    """
    # Create regions
    for region_name in REGIONS:
        region = Region(region_name, world.player, world.multiworld)
        world.multiworld.regions.append(region)

    if world.seasons:
        from ...data.Regions import NATZU_REGIONS
        for region_name in NATZU_REGIONS[world.options.animal_companion.current_key]:
            region = Region(region_name, world.player, world.multiworld)
            world.multiworld.regions.append(region)

        if world.options.logic_difficulty == OraclesLogicDifficulty.option_hell:
            region = Region("rooster adventure", world.player, world.multiworld)
            world.multiworld.regions.append(region)

    if world.options.deterministic_gasha_locations > 0:
        for i in range(world.options.deterministic_gasha_locations):
            region = Region(GASHA_REGIONS[i], world.player, world.multiworld)
            world.multiworld.regions.append(region)

    if world.options.linked_heros_cave.value > 0:
        for region_name in D11_REGIONS:
            world.multiworld.regions.append(Region(region_name, world.player, world.multiworld))

    # Create locations
    for location_name, location_data in LOCATIONS_DATA.items():
        if not world.location_is_active(location_name, location_data):
            continue

        is_local = "local" in location_data and location_data["local"] is True
        create_location(world, location_data["region_id"], location_name, is_local)
    world.create_events()
    exclude_locations_automatically(world)


def create_event(world, region_name: str, event_item_name: str) -> None:
    """
    Creates an event for a game.

    Parameters:
        world: The world used to create the event.
        region_name (str): A region used for creating the event.
        event_item_name (str): The name of the event.
    """
    region = world.multiworld.get_region(region_name, world.player)
    location = Location(world.player, region_name + ".event", None, region)
    region.locations.append(location)
    location.place_locked_item(Item(event_item_name, ItemClassification.progression, None, world.player))


def exclude_locations_automatically(world) -> None:
    """
    Automatically excludes locations from a game.

    Parameters:
        world: The world used to exclude the locations.
    """
    locations_to_exclude = set()
    # If goal essence requirement is set to a specific value, prevent essence-bound checks which require more
    # essences than this goal to hold anything of value
    if world.options.required_essences < 7 <= len(world.essences_in_game):
        locations_to_exclude.add(world.city_name + ": Item Inside Maku Tree (7+ Essences)")
        if world.options.required_essences < 5 <= len(world.essences_in_game):
            locations_to_exclude.add(world.city_name + ": Item Inside Maku Tree (5+ Essences)")
            if world.options.required_essences < 3 <= len(world.essences_in_game):
                locations_to_exclude.add(world.city_name + ": Item Inside Maku Tree (3+ Essences)")
    if world.seasons and world.options.required_essences < world.options.treehouse_old_man_requirement:
        locations_to_exclude.add("Holodrum Plain: Old Man in Treehouse")

    # If dungeons without essence need to be excluded, do it if conditions are met
    if world.options.exclude_dungeons_without_essence and not world.options.shuffle_essences:
        for i, essence_name in enumerate(ITEM_GROUPS["Essences"]):
            if essence_name not in world.essences_in_game:
                locations_to_exclude.update(world.location_name_groups[f"D{i + 1}"])

    if not world.options.shuffle_business_scrubs:
        locations_to_exclude.difference_update(SCRUB_LOCATIONS)

    if world.seasons and world.options.randomize_ai:
        locations_to_exclude.add("Western Coast: Black Beast's Chest")

    for name in locations_to_exclude:
        world.multiworld.get_location(name, world.player).progress_type = LocationProgressType.EXCLUDED
