import logging
from functools import partial
from typing import cast
# from line_profiler import profile
from BaseClasses import CollectionState, MultiWorld, Region, Entrance, Location
from dataclasses import astuple, dataclass, field

from .Options import XenobladeXOptions


@dataclass(frozen=True, eq=True)
class Requirement:
    name: str
    count: int = 1


@dataclass(frozen=True)
class Rule:
    region: str
    requirements: set[Requirement] = field(default_factory=lambda: set())


@dataclass(frozen=True)
class Miranium:
    st: int = 0
    dp: int = 0
    b1: int = 0
    b2: int = 0
    mech: int = 1


@dataclass(frozen=True)
class Credits:
    r1: int = 0
    r2: int = 0
    r3: int = 0
    r4: int = 0
    r5: int = 0
    r6: int = 0
    dp: int = 0
    b1: int = 0
    b2: int = 0
    mech: int = 1


from .regions.chapters import chapter_regions  # noqa: E402
from .regions.fieldSkills import field_skill_regions  # noqa: E402
from .regions.fnet import fnet_regions  # noqa: E402
from .regions.friends import friends_regions  # noqa: E402
from .regions.importantItems import important_item_regions  # noqa: E402
from .regions.key import key_regions  # noqa: E402
from .regions.shop import shop_regions  # noqa: E402
from .regions.zones import zones_regions  # noqa: E402
from .regions.quests import quest_regions  # noqa: E402
from .regions.level import level_regions  # noqa: E402
from .fnet.miranium import fnet_miranium_data  # noqa: E402
from .fnet.credits import fnet_credits_data  # noqa: E402

xenobladeXRegions = [
    *chapter_regions,
    *field_skill_regions,
    *fnet_regions,
    *friends_regions,
    *key_regions,
    *shop_regions,
    *zones_regions,
    *quest_regions,
    *level_regions,
    *important_item_regions,
]


# Save all requirements for each region
xenobladex_region_requirements: dict[int, dict[str, set[Requirement]]] = {}


def init_region(world: MultiWorld, player: int, region_name: str) -> str:
    """Initialize the new region if it was not done before and establish the connection rules,
        based on its predecessors, if applicable"""
    region_names = [region.name for region in world.get_regions(player)]
    regions = set([rule.region for rule in xenobladeXRegions])

    assert set(region_name.split("+")) <= regions, f"{set(region_name.split('+')) - regions} not in available regions"
    if player not in xenobladex_region_requirements:
        xenobladex_region_requirements[player] = {}
    if region_name == "Menu" and "Menu" not in region_names:
        world.regions += [Region(region_name, player, world, region_name)]
        xenobladex_region_requirements[player]["Menu"] = set()
        return "Menu"

    # Add connections to this region
    requirements: set[Requirement] = set()
    for subregion in region_name.split("+"):
        region_found = False
        for rule in reversed(xenobladeXRegions):
            if rule.region != subregion and not region_found:
                continue
            region_found = True
            if rule.region == "Menu":
                break
            requirements = requirements.union(rule.requirements)

    # Remove same requirements with lower count
    highest_requirements: dict[str, Requirement] = {}
    for requirement in requirements:
        existing = highest_requirements.get(requirement.name)
        if existing is None or requirement.count > existing.count:
            highest_requirements[requirement.name] = requirement
    requirements = set(highest_requirements.values())

    # Check if region with same requirements already exists
    dup_region = False
    for req_region_name, region_requirements in xenobladex_region_requirements[player].items():
        if req_region_name != region_name and requirements == region_requirements:
            dup_region = True
            logging.debug(f"Duplicate Region: {region_name} ||| {req_region_name}")
            region_name = req_region_name
            break
    if not dup_region and region_name not in region_names:
        logging.debug(f"Region Name: {region_name}")
        xenobladex_region_requirements[player][region_name] = requirements
        world.regions += [Region(region_name, player, world, region_name)]
        connect_regions(world, player, "Menu", region_name,
                        partial(has_items, player=player, requirements=requirements))
    return region_name


def trim_regions(regions: set[str]) -> list[str]:
    subrules: set[str] = set()
    duplicate_regions: set[str] = set()
    if "Menu" in regions and len(regions) > 1:
        regions.remove("Menu")
    for rule in xenobladeXRegions:
        if rule.region == "Menu":
            subrules = set()
        else:
            if rule.region in regions:
                duplicate_regions.update(subrules)
            subrules.add(rule.region)
    return list(regions.difference(duplicate_regions))


def add_region_location(world: MultiWorld, player: int, region_name: str, location: Location) -> Location:
    region = world.get_region(region_name, player)
    region.locations += [location]
    return location


def connect_regions(world: MultiWorld, player: int, source: str, target: str, rule):
    """Connect a single region to another with a specified rule"""
    source_region = world.get_region(source, player)
    target_region = world.get_region(target, player)

    connection = Entrance(player, target, source_region)
    connection.access_rule = rule

    source_region.exits.append(connection)
    connection.connect(target_region)


# Convert the logic level into the required logic count
def get_logic_level_count(logic_level: int, step_size: int):
    return int(min(logic_level, 50) / step_size) + int(min(logic_level - 50, 0) / (step_size + 5))


# Used by rules to improve performance of zone completion checks. player - zone - region - seg count
segment_completion_lookup: dict[int, dict[str, dict[str, int]]] = {}


# Only after items are inside itempool and before fill
def prepare_regions(world: MultiWorld, player: int) -> None:
    segment_completion_lookup[player] = {}
    zones = ["MIRA", "PRIM", "NOCT", "OBLI", "SYLV", "CAUL"]
    regions = world.get_regions(player)
    for zone in zones:
        # Create segment_completion_lookup for region rules
        zone_dict: dict[str, int] = {}
        # Add indirect conditions to regions
        indirect_regions: set[Region] = set()
        for region in regions:
            count: int = 0
            for loc in region.get_locations():
                if loc.name.startswith(("SEG", "FNO")):
                    if zone == "MIRA":
                        count += 1
                        indirect_regions.add(region)
                    elif f"- {zone.capitalize()}" in loc.name:
                        count += 1
                        indirect_regions.add(region)
            zone_dict[region.name] = count
        segment_completion_lookup[player][zone] = zone_dict
        # Find all affected entrances
        for entrance in world.get_entrances(player):
            if zone in [req.name for req in xenobladex_region_requirements[player][entrance.name]]:
                for region in indirect_regions:
                    world.register_indirect_condition(region, entrance)


# @profile
def has_items(state: CollectionState, player, requirements: set[Requirement]) -> bool:
    """Returns true if the state satifies the item requirements"""
    result = True
    logic_level_steps = cast(XenobladeXOptions, state.multiworld.worlds[player].options).logic_level_steps.value
    important_items_enabled: bool = cast(XenobladeXOptions, state.multiworld.worlds[player].options).impit.value != 0
    for requirement in requirements:
        if requirement.name == "MIRANIUM":
            result = result and has_miranium(state, player, requirement.count)
        elif requirement.name == "CREDITS":
            result = result and has_credits(state, player, requirement.count)
        elif requirement.name in state.multiworld.worlds[player].item_name_groups:
            result = result and state.has_group(requirement.name, player)
        elif requirement.name in ["MIRA", "PRIM", "NOCT", "OBLI", "SYLV", "CAUL"]:
            zone_segment_count = 0
            for region, count in segment_completion_lookup[player][requirement.name].items():
                if state.can_reach_region(region, player):
                    zone_segment_count += count
                if zone_segment_count >= requirement.count:
                    break
            result = result and zone_segment_count >= requirement.count
        elif requirement.name == "LVL" and logic_level_steps != 0:
            result = result and state.has("KEY: Level", player,
                                          get_logic_level_count(requirement.count, logic_level_steps))
        else:
            if (not requirement.name.startswith("IMPIT")) or important_items_enabled:
                result = result and state.has(requirement.name, player, requirement.count)
        if not result:
            break
    return result


def has_miranium(state: CollectionState, player, target: int) -> bool:
    st = state.count("DP: Storage Probe", player)
    dp = state.count("DP: Duplicator Probe", player)
    b1 = state.count("DP: Booster Probe G1", player)
    b2 = state.count("DP: Booster Probe G2", player)
    mech = state.count("FLDSK: Mechanical", player) + 1
    mir_state = Miranium(st, dp, b1, b2, mech)
    miranium = 6  # fnet default
    for value, mirs in fnet_miranium_data.items():
        for mir in mirs:
            possible = True
            for it1, it2 in zip(astuple(mir), astuple(mir_state)):
                possible = possible and it1 <= it2
            if possible:
                miranium = value
    return miranium >= target


def has_credits(state: CollectionState, player, target) -> bool:
    r = [state.count(f"DP: Research Probe G{i}", player) for i in range(1, 7)]
    dp = state.count("DP: Duplicator Probe", player)
    b1 = state.count("DP: Booster Probe G1", player)
    b2 = state.count("DP: Booster Probe G2", player)
    mech = state.count("FLDSK: Mechanical", player) + 1
    crd_state = Credits(r[0], r[1], r[2], r[3], r[4], r[5], dp, b1, b2, mech)
    credits = 0
    for value, crds in fnet_credits_data.items():
        for crd in crds:
            possible = True
            for it1, it2 in zip(astuple(crd), astuple(crd_state)):
                possible = possible and it1 <= it2
            if possible:
                credits = value
    return credits >= target
