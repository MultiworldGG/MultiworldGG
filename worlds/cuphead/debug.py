### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from collections.abc import Iterable
from typing import TYPE_CHECKING, TypeVar

import Utils
from BaseClasses import Region
from worlds.AutoWorld import World

from .world.auxiliary import format_list
from .world.items.itemdefs import items_all
from .world.locations.locationdefs import locations_all

if TYPE_CHECKING:
    from . import CupheadWorld

T = TypeVar("T")

def test_duplicates(ls: Iterable[T]) -> int:
    seen: set[T] = set()
    dups: list[T] = []
    for x in ls:
        if x in seen:
            dups.append(x)
        else:
            seen.add(x)
    print("Duplicates: "+str(dups))
    print("Total Duplicates: "+str(len(dups)))
    return len(dups)

def print_list_each_line(ls: Iterable[T]):
    for item in ls:
        print(item)

def print_list(ls: Iterable[T]):
    print(format_list(ls))

def print_locations(world: World):
    locations = world.multiworld.get_locations(world.player)
    for loc in locations:
        print(f"{loc.name}: {loc.access_rule}")

def print_all_items():
    print("-- Items --")
    for item, data in items_all.items():
        print(f"{item}: {data.id} | {data.item_type}")
    print("")

def print_all_locations():
    print("-- Locations --")
    for item, data in locations_all.items():
        print(f"{item}: {data.id} | {data.progress_type}")
    print("")

def debug_print_regions(world: "CupheadWorld"):
    for rname,r in world.multiworld.regions.region_cache[world.player].items():
        print(f"{rname}:")
        for loc in r.locations:
            print(f" {loc}")

def visualize_regions_ext(
        root_region: Region,
        highlight_regions: set[Region] | None,
        file_name: str,
        show_entrance_names: bool = True,
        show_locations: bool = True,
        show_other_regions: bool = True,
        linetype_ortho: bool = True,
    ):
    Utils.visualize_regions(
        root_region,
        file_name,
        show_entrance_names=show_entrance_names,
        show_locations=show_locations,
        show_other_regions=show_other_regions,
        linetype_ortho=linetype_ortho,
        regions_to_highlight=highlight_regions
    )

def visualize_regions(root_region: Region, highlight_regions: set[Region] | None, file_name: str):
    visualize_regions_ext(
        root_region,
        highlight_regions,
        file_name,
    )

def debug_visualize_regions(world: "CupheadWorld", highlight_reachable: bool = False, output_name: str | None = None):
    state = world.multiworld.get_all_state(allow_partial_entrances=True)
    output_name = f"_{output_name}" if output_name else ""
    visualize_regions(
        world.multiworld.get_region("Start", world.player),
        set(state.reachable_regions[world.player]) if highlight_reachable else None,
        f"./output/AP_{world.multiworld.seed_name}{output_name}-regionmap.puml"
    )
