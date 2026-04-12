from typing import List

from . import LunacidOptions
from .data.location_data import (all_locations, base_locations, shop_locations, unique_drop_locations,
                                 other_drop_locations, quench_locations, alchemy_locations,
                                 LunacidLocation, spooky_locations, crimpus_locations, level_locations, lore_locations, grass_locations, break_locations)
from .strings.locations import SpookyLocation

location_table = all_locations
locations_by_name = {location.name: location for location in location_table}


def create_locations(options: LunacidOptions, month: int, level: int) -> List[LunacidLocation]:
    locations = base_locations.copy()
    create_shop_locations(options, locations)
    create_drop_locations(options, locations)
    create_quench_locations(options, locations)
    create_alchemy_locations(options, locations)
    create_spooky_locations(options, month, locations)
    create_crimpus_locations(month, locations)
    create_stat_locations(level, options, locations)
    create_lore_locations(options, locations)
    create_grass_locations(options, locations)
    create_break_locations(options, locations)
    return locations


def create_shop_locations(options: LunacidOptions, locations: List[LunacidLocation]) -> List[LunacidLocation]:
    if not options.shopsanity:
        return locations
    for location in shop_locations:
        locations.append(location)
    return locations


def create_drop_locations(options: LunacidOptions, locations: List[LunacidLocation]) -> List[LunacidLocation]:
    if not options.dropsanity:
        return locations
    for location in unique_drop_locations:
        locations.append(location)
    if options.dropsanity == options.dropsanity.option_randomized:
        for location in other_drop_locations:
            locations.append(location)
    return locations


def create_quench_locations(options: LunacidOptions, locations: List[LunacidLocation]) -> List[LunacidLocation]:
    if not options.quenchsanity:
        return locations
    for location in quench_locations:
        locations.append(location)
    return locations


def create_alchemy_locations(options: LunacidOptions, locations: List[LunacidLocation]) -> List[LunacidLocation]:
    if not options.etnas_pupil:
        return locations
    for location in alchemy_locations:
        locations.append(location)
    return locations


def create_spooky_locations(options: LunacidOptions, month: int, locations: List[LunacidLocation]) -> List[LunacidLocation]:
    if month != 10:
        return locations
    for location in spooky_locations:
        if location.name == SpookyLocation.headless_horseman and not options.dropsanity:
            continue
        locations.append(location)
    return locations


def create_crimpus_locations(month: int, locations: List[LunacidLocation]) -> List[LunacidLocation]:
    if month != 12:
        return locations
    for location in crimpus_locations:
        locations.append(location)
    return locations


def create_stat_locations(level: int, options: LunacidOptions, locations: List[LunacidLocation]):
    if not options.levelsanity:
        return locations
    required_locations = [location for location in level_locations if location.location_id - 800 > level]
    locations.extend(required_locations)
    return locations


def create_lore_locations(options: LunacidOptions, locations: List[LunacidLocation]):
    if not options.bookworm:
        return locations
    locations.extend(lore_locations)
    return locations


def create_grass_locations(options: LunacidOptions, locations: List[LunacidLocation]):
    if not options.grasssanity:
        return locations
    locations.extend(grass_locations)
    return locations


def create_break_locations(options: LunacidOptions, locations: List[LunacidLocation]):
    if not options.breakables:
        return locations
    locations.extend(break_locations)
    return locations
