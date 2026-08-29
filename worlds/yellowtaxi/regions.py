from __future__ import annotations

from .data_loader import regions_json_data, original_level_order, special_starting_areas
from typing import Any, Dict, TYPE_CHECKING

from BaseClasses import Entrance, Region


if TYPE_CHECKING:
    from .world import YellowTaxiWorld

def create_and_connect_regions(world: YellowTaxiWorld) -> None:
    create_all_regions(world)
    connect_regions(world)

def create_all_regions(world: YellowTaxiWorld) -> None:
    regions = [Region("Menu", world.player, world.multiworld)]
    if world.using_ut:
        ut_sorted_sublevels: dict[str, int] = {}
        ut_sort_region_counters: dict[str, int] = {}
        ut_sorted_levels: dict[str, int] = {}
        include_oob_areas: bool = (
                    world.options.include_out_of_bounds == world.options.include_out_of_bounds.option_full)
    else:
        include_oob_areas: bool = (
                    world.options.include_out_of_bounds == world.options.include_out_of_bounds.option_full
                    and world.options.expert_level >= 1)
    for reg_name in regions_json_data.keys():
        if reg_name in world.excluded_regions:
            continue
        if world.options.expert_level < 1 and "(EXPERTS ONLY)" in reg_name:
            continue
        if not include_oob_areas and "out-of-bounds" in reg_name.lower():
            continue
        if not world.has_golden_propeller_access and "golden propeller" in reg_name.lower():
            continue
        if (world.options.include_out_of_bounds == world.options.include_out_of_bounds.option_none and
                "hidden coins" in reg_name.lower()):
            continue
        reg = regions_json_data[reg_name]
        if reg["level"] not in world.included_levels and reg["level"] not in world.special_levels and reg["level"] not in world.goal_levels:
            continue
        if reg["level"] == "Mosk's Rocket" and reg["kaizolevel"] not in world.included_levels:
            continue
        regions += [Region(reg_name, world.player, world.multiworld)]
        # UT sorting. Basically it adds level # * 100 and sublevel # based on order defined in the json
        # TODO: Make this more accurate based on level order, especially when level rando is in
        # May need to move this elsewhere if doing so, since level order may not yet be able to be inferred
        # Also this could probably be simplified significantly but it works for the time being
        if world.using_ut:
            if reg["level"] not in ut_sorted_levels.keys():
                if reg["level"] == "Hub":
                    ut_sorted_levels[reg["level"]] = 0
                elif reg["level"] in world.special_levels:
                    ut_sorted_levels[reg["level"]] = -1
                else:
                    ut_sorted_levels[reg["level"]] = world.level_order.index(reg["level"]) + 1
            if reg["sublevel"] not in ut_sorted_sublevels:
                if reg["level"] in ut_sort_region_counters.keys():
                    ut_sort_region_counters[reg["level"]] += 1
                else:
                    ut_sort_region_counters[reg["level"]] = 1
                ut_sorted_sublevels[reg["sublevel"]] = ((ut_sorted_levels[reg["level"]] * 100) +
                                                        ut_sort_region_counters[reg["level"]])
            world.ut_sort_region_dict[reg_name] = ut_sorted_sublevels[reg["sublevel"]]

    world.multiworld.regions += regions


def connect_regions(world: YellowTaxiWorld) -> None:
    for region in world.get_regions():
        if region.name == "Menu":
            # Connect starting area
            if world.lab_start:
                region.connect(world.get_region("Morio's Lab - Ground Floor"))
            else:
                region.connect(world.get_region("Granny's Island - Starting Area"))
            continue
        reg = regions_json_data[region.name]

        # Connect basic connections
        if "connections" in reg.keys():
            for connect in reg["connections"].items():
                try:
                    connecting_region = world.get_region(connect[0])
                except KeyError:
                    continue
                region.connect(connecting_region, f"{region.name} -> {connecting_region.name}")

        # Connect subwarps
        # TODO: Entrance Rando
        if "subwarps" in reg.keys():
            for subwarp in reg["subwarps"].items():
                try:
                    connecting_region = world.get_region(subwarp[1][0])
                except KeyError:
                    continue
                region.connect(connecting_region, subwarp[0])

        # Connect full warps
        # TODO: Full Entrance Rando
        if "warps" in reg.keys():
            for warp in reg["warps"].items():
                warp_index : int = -1
                if warp[1][0].startswith("{PORTAL}"):
                    # Get the starting area that corresponds to this entrance
                    warp_index = original_level_order.index(warp[1][0][8:])
                    connecting_level : str = world.level_order[warp_index]
                    if connecting_level == "Excluded":
                        continue
                    starting_area : str = connecting_level
                    if starting_area in special_starting_areas.keys():
                        starting_area = special_starting_areas[starting_area]
                    if starting_area == "":
                        if not world.using_ut:
                            continue
                        starting_area = "Menu"
                    else:
                        starting_area = starting_area + " - Starting Area"
                    connecting_region = world.get_region(starting_area)
                else:
                    try:
                        connecting_region = world.get_region(warp[1][0])
                    except KeyError:
                        continue
                entrance = region.connect(connecting_region, warp[0])
                if world.using_ut and world.defer_entrances and warp_index != -1:
                    if world.level_order[warp_index] in world.goal_levels:
                        continue
                    world.disconnected_entrances[warp_index] = entrance, connecting_region
                    entrance.connected_region = None

        # Connect Mori-O-Trons
        # TODO: Entrance Rando. Until then, only relevant in Maurizio's City and Crash Test Industries
        if reg["level"] in ["Maurizio's City", "Crash Test Industries"]:
            if "moriotrons" in reg.keys() and (world.options.expert_level >= 2 or world.using_ut):
                for moriotron in reg["moriotrons"].items():
                    try:
                        connecting_region = world.get_region(moriotron[1])
                    except KeyError:
                        continue
                    region.connect(connecting_region, moriotron[0])