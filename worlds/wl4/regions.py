from __future__ import annotations

import itertools
from typing import Iterable, TYPE_CHECKING

from rule_builder.rules import CanReachLocation, Has, HasAll, HasAllCounts, OptionFilter, Rule, True_
from worlds.generic.Rules import CollectionRule, add_item_rule
from BaseClasses import Item, Region

from .data import Passage
from .items import JewelPieceItemData, WL4EventItem, WL4Item, get_jewel_pieces_by_passage
from .locations import WL4EventLocation, WL4Location
from .region_data import LocationData, LocationType, RegionData, passage_levels, level_table, passage_boss_table, golden_diva
from .rules import has_treasures
from .options import OpenDoors, Portal

if TYPE_CHECKING:
    from . import WL4World


AccessRule = CollectionRule | None


class WL4Region(Region):
    def __init__(self, name: str, world: WL4World):
        super().__init__(name, world.player, world.multiworld)


class WL4Level:
    world: WL4World
    items: list[WL4Item]
    locations: list[WL4Location]

    def __init__(self, world: WL4World):
        self.world = world
        self.items = []
        self.locations = []


def filter_out_locations(locations: Iterable[LocationData], location_type: LocationType):
    return filter(lambda location: location.type != location_type, locations)


def get_locations(world: WL4World, level: str, region: RegionData):
    locations = filter(lambda location: world.options.difficulty.value in location.difficulties, region.locations)
    if not world.options.diamond_shuffle.value:
        locations = filter_out_locations(locations, LocationType.DIAMOND)
    if world.options.portal.value == Portal.option_open:
        locations = filter_out_locations(locations, LocationType.SWITCH)

    for location_data in locations:
        if (
            location_data.type == LocationType.KEYZER
            and world.options.open_doors.value != OpenDoors.option_off
            and not world.options.keyzer_shuffle.value
        ):
            if world.options.open_doors.value == OpenDoors.option_open:
                continue
            if level != "Golden Passage":
                continue
        yield location_data


def get_region_name(level: str, region: str | None):
    return level if region is None else f"{level} - {region}"


def get_level_entrance_name(level: str):
    return f"{level} - Entrance" if level in level_table and level_table[level].use_entrance_region else level


def create_event(region: Region, location_name: str, item_name: str | None = None):
    if item_name is None:
        item_name = location_name
    location = WL4EventLocation(region.player, location_name, region)
    location.place_locked_item(WL4EventItem(item_name, region.player))
    return location


def connect_entrance(world: WL4World, name: str, source: str, target: str, rule: Rule[WL4World] = True_()):
    world.create_entrance(world.get_region(source), world.get_region(target), rule, name)


def create_regions(world: WL4World):
    regions = []

    pyramid = WL4Region("Pyramid", world)
    regions.append(pyramid)

    for passage in Passage:
        regions.append(WL4Region(passage.long_name(), world))

    for level_name, level_data in level_table.items():
        level = WL4Level(world)
        world.levels[level_name] = level

        for region_data in level_data.regions:
            region_name = get_region_name(level_name, region_data.name)
            region = WL4Region(region_name, world)

            for location_data in get_locations(world, level_name, region_data):
                location_name = f"{level_name} - {location_data.name}"
                if location_data.type == LocationType.SWITCH:
                    item_name = f"{location_data.name} ({level_name})"
                    location = create_event(region, location_name, item_name)
                elif location_data.type == LocationType.KEYZER and not world.options.keyzer_shuffle.value:
                    location = WL4Location(world.player, location_name, region, force_event=True)
                else:
                    location = WL4Location(world.player, location_name, region)
                    level.locations.append(location)

                region.locations.append(location)
            regions.append(region)

    for passage, boss_data in passage_boss_table.items():
        boss_region = WL4Region(f"{passage.long_name()} Boss", world)
        location = create_event(boss_region, boss_data.name, f"{passage.long_name()} Clear")
        boss_region.locations.append(location)
        regions.append(boss_region)

        if world.options.goal.needs_treasure_hunt():
            prize_region = WL4Region(f"{boss_data.name} - Prizes", world)
            for time in ("15", "35", "55"):
                location = WL4Location(world.player, f"{boss_data.name} - 0:{time}", prize_region)
                prize_region.locations.append(location)
            regions.append(prize_region)

    golden_diva_region = WL4Region("Golden Pyramid Boss", world)
    if world.options.goal.needs_diva():
        diva_location = create_event(golden_diva_region, golden_diva.name, "Escape the Pyramid")
        golden_diva_region.locations.append(diva_location)
    regions.append(golden_diva_region)

    if world.options.goal.is_treasure_hunt():
        emergency_exit = create_event(pyramid, "Sound Room Emergency Exit", "Escape the Pyramid")
        pyramid.locations.append(emergency_exit)

    world.multiworld.regions.extend(regions)


def set_rules(world: WL4World):
    def restrict_jewel_piece_on_boss(passage: Passage):
        def rule(item: Item):
            if item.player != world.player:
                return True
            assert type(item) is WL4Item
            return type(item.data) is not JewelPieceItemData or item.data.passage != passage
        return rule

    def restrict_jewel_piece_in_golden_passage(item: Item):
        if item.player != world.player:
            return True
        assert type(item) is WL4Item
        return type(item.data) is not JewelPieceItemData or item.data.passage == Passage.GOLDEN

    for level_name, level_data in level_table.items():
        for region_data in level_data.regions:
            for location_data in get_locations(world, level_name, region_data):
                location = world.get_location(f"{level_name} - {location_data.name}")

                rule = location_data.access_rule
                if world.options.portal.value == Portal.option_vanilla and location_data.type != LocationType.SWITCH:
                    rule &= CanReachLocation(f"{level_name} - Frog Switch")
                world.set_rule(location, rule)
                if world.options.restrict_self_locking_jewel_pieces.value and level_name == "Golden Passage":
                    add_item_rule(location, restrict_jewel_piece_in_golden_passage)

    for passage, boss_data in passage_boss_table.items():
        world.set_rule(world.get_location(boss_data.name), boss_data.kill_rule)

        if world.options.goal.needs_treasure_hunt():
            for time in ("15", "35", "55"):
                location = world.get_location(f"{boss_data.name} - 0:{time}")
                if world.options.restrict_self_locking_jewel_pieces.value:
                    add_item_rule(location, restrict_jewel_piece_on_boss(passage))

    if world.options.goal.needs_diva():
        diva_location = world.get_location(golden_diva.name)
        rule = golden_diva.kill_rule
        if world.options.goal.needs_treasure_hunt():
            rule &= has_treasures
        world.set_rule(diva_location, rule)

    if world.options.goal.is_treasure_hunt():
        world.set_rule(world.get_location("Sound Room Emergency Exit"), has_treasures)

    world.set_completion_rule(Has("Escape the Pyramid"))


def make_boss_access_rule(passage: Passage, jewels_needed: int):
    return HasAllCounts({name: jewels_needed for name in get_jewel_pieces_by_passage(passage)})


def place_keyzer(world: WL4World, level: str, keyzer: str):
    try:
        location = world.get_location(f"{level} - Keyzer")
    except KeyError:
        pass
    else:
        location.place_locked_item(WL4Item(keyzer, world.player))


def connect_regions(world: WL4World):
    required_jewels = world.options.required_jewels.value
    required_jewels_entry = min(1, required_jewels)

    for passage, levels in passage_levels.items():
        connect_entrance(
            world,
            f"{passage.long_name()} Entrance",
            "Pyramid",
            passage.long_name(),
            HasAll("Emerald Passage Clear", "Ruby Passage Clear", "Topaz Passage Clear", "Sapphire Passage Clear")
                if passage == Passage.GOLDEN else True_()
        )

        connect_entrance(world, f"{levels[0]} Entrance", passage.long_name(), get_level_entrance_name(levels[0]))
        for i, (source, destination) in enumerate(itertools.pairwise(levels), 1):
            keyzer_name = f"Keyzer ({passage.long_name()} {i})"
            if not world.options.keyzer_shuffle:
                place_keyzer(world, source, keyzer_name)
            connect_entrance(
                world,
                f"{destination} Entrance",
                get_level_entrance_name(source),
                get_level_entrance_name(destination),
                Has(keyzer_name) | OptionFilter(OpenDoors, OpenDoors.option_off, "ne")
            )

        keyzer_name = f"Keyzer ({passage.long_name()} Boss)"
        if not world.options.keyzer_shuffle:
            place_keyzer(world, levels[-1], keyzer_name)
        if passage != Passage.ENTRY:
            boss_access = make_boss_access_rule(passage, required_jewels_entry if passage == Passage.GOLDEN else required_jewels)
            if passage == Passage.GOLDEN:
                boss_access &= Has(keyzer_name) | OptionFilter(OpenDoors, OpenDoors.option_open)
            else:
                boss_access &= Has(keyzer_name) | OptionFilter(OpenDoors, OpenDoors.option_off, "ne")
            connect_entrance(
                world,
                f"{passage.long_name()} Boss Door",
                get_level_entrance_name(levels[-1]),
                f"{passage.long_name()} Boss",
                boss_access
            )

    for level_name, level_data in level_table.items():
        for region_data in level_data.regions:
            source = get_region_name(level_name, region_data.name)
            for exit_data in region_data.exits:
                destination = get_region_name(level_name, exit_data.destination)

                connect_entrance(
                    world,
                    f"{level_name} - {region_data.name or 'Main area'} to {exit_data.destination or 'Main area'}",
                    source,
                    destination,
                    exit_data.access_rule
                )

    if (world.options.goal.needs_treasure_hunt()):
        for passage, boss_data in passage_boss_table.items():
            connect_entrance(
                world,
                f"{passage.long_name()} Quick Kill",
                f"{passage.long_name()} Boss",
                f"{boss_data.name} - Prizes",
                boss_data.kill_rule & boss_data.quick_kill_rule
            )
