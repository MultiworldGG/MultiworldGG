from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import CollectionState, Location
from worlds.generic.Rules import set_rule, add_rule
from .fitting import best_total, hulls_needed
from .items import item_table, CATCH_TOOL_INDEX
from .locations import (location_table, DREDGELocationData, ItemsReq, CatchTypeReq, ResearchReq, IronRigPhaseReq,
                        LocationsReq, RegionsReq, AberrationsReq, ItemCountReq)
from .options import DREDGEOptions

if TYPE_CHECKING:
    from . import DREDGEWorld

def set_all_rules(world: DREDGEWorld) -> None:
    set_region_rules(world)
    set_location_rules(world)
    set_completion_condition(world)
    #set_prototype_rules(world)

def set_prototype_rules(world: DREDGEWorld) -> None:
    set_rule(
        world.get_location("A Place to Rest - Materials Delivered Event"),
        lambda state: state.has("Dredge Crane", world.player),
    )
    set_rule(
        world.get_location("A Place to Rest - Returned to Builder Event"),
        lambda state: state.has(
            "A Place to Rest - Materials Delivered",
            world.player,
        ),
    )

def set_region_rules(world: "DREDGEWorld") -> None:
    player = world.player

    world.get_entrance("The Marrows to Open Ocean").access_rule = \
        lambda state: not world.options.add_passage_items or has_passage_item("The Pelagic Psalm", state, player)
    world.get_entrance("Open Ocean to Gale Cliffs").access_rule = \
        lambda state: (not world.options.add_passage_items or has_passage_item("The Windward Litany", state, player)) and has_boat_performance(world, MID_REGIONS_PERFORMANCE, state)
    world.get_entrance("Open Ocean to Stellar Basin").access_rule = \
        lambda state: (not world.options.add_passage_items or has_passage_item("The Astral Testament", state, player)) and has_boat_performance(world, MID_REGIONS_PERFORMANCE, state)
    world.get_entrance("Open Ocean to Twisted Strand").access_rule = \
        lambda state: (not world.options.add_passage_items or has_passage_item("The Mangrove Canticle", state, player)) and has_boat_performance(world, MID_REGIONS_PERFORMANCE, state)
    world.get_entrance("Open Ocean to Devil's Spine").access_rule = \
        lambda state: (not world.options.add_passage_items or has_passage_item("The Cinder Gospel", state, player)) and has_boat_performance(world, MID_REGIONS_PERFORMANCE, state)
    world.get_entrance("Open Ocean to The Iron Rig").access_rule = \
        lambda state: has_boat_performance(world, OPEN_OCEAN_PERFORMANCE, state)
    world.get_entrance("Open Ocean to The Pale Reach").access_rule = \
        lambda state: (not world.options.add_passage_items or has_passage_item("The Rimebound Chronicle", state, player)) and has_boat_performance(world, PALE_REACH_PERFORMANCE, state)
    world.get_entrance("Open Ocean to Insanity").access_rule = \
        lambda state: has_relics(state, player)

def set_location_rules(world: "DREDGEWorld") -> None:
    player = world.player
    include_iron_rig = bool(world.options.include_iron_rig_dlc)
    for world_location in world.get_locations():
        location = location_table.get(world_location.name)
        if location is None:
            continue
        if world.options.add_fishing_licenses and location.location_group == "Encyclopedia":
            add_license_rule(world_location, location, player)
        if location.is_aberration and location.location_group == "Encyclopedia":
            add_rule(world_location, lambda state: can_get_aberrations(world, state))
        if location.region == "Open Ocean" and location.location_group in AT_SEA_LOCATION_GROUPS:
            add_rule(world_location, lambda state: has_boat_performance(world, OPEN_OCEAN_PERFORMANCE, state))
        for requirement in location.requirements:
            match requirement:
                case ItemsReq():
                    add_item_rules(requirement, world_location, player, include_iron_rig)
                case CatchTypeReq():
                    add_catch_type_rule(world_location, location, player, world.options)
                case ResearchReq():
                    pass
                case IronRigPhaseReq():
                    add_iron_rig_phase_rule(requirement, world_location, player, include_iron_rig)
                case LocationsReq():
                    add_rule(world_location, lambda state, names=requirement.all_of:
                             all(state.can_reach_location(name, player) for name in names))
                case ItemCountReq():
                    add_rule(world_location, lambda state, req=requirement: state.has(req.item, player, req.count))
                case AberrationsReq():
                    add_rule(world_location, lambda state: can_get_aberrations(world, state))
                case RegionsReq():
                    add_rule(world_location, lambda state, names=requirement.any_of:
                             any(state.can_reach_region(name, player) for name in names))
                case _:
                    raise ValueError(f"Unhandled requirement {requirement!r} for {world_location.name}")

def add_license_rule(world_location, location, player):
    match location.region:
        case "Gale Cliffs":
            add_rule(world_location, lambda state: state.has("Gale Cliffs Fishing License", player))
        case "Stellar Basin":
            add_rule(world_location, lambda state: state.has("Stellar Basin Fishing License", player))
        case "Twisted Strand":
            add_rule(world_location, lambda state: state.has("Twisted Strand Fishing License", player))
        case "Devil's Spine":
            add_rule(world_location, lambda state: state.has("Devil's Spine Fishing License", player))
        case "Open Ocean":
            add_rule(world_location, lambda state: state.has("Open Ocean Fishing License", player))
        case "The Pale Reach":
            add_rule(world_location, lambda state: state.has("Pale Reach Fishing License", player))

def add_iron_rig_phase_rule(requirement, world_location, player, include_iron_rig: bool) -> None:
    def can_equip_rod_for(catch_type: str):
        return lambda state: can_equip_any(tools_for(catch_type, "Rod"), state, player, include_iron_rig)

    if requirement.value > 4:
        add_rule(world_location, can_equip_rod_for("Infused Mangrove"))
    if requirement.value > 3:
        add_rule(world_location, can_equip_rod_for("Infused Hadal"))
        add_rule(world_location, can_equip_rod_for("Infused Abyssal"))
    if requirement.value > 2:
        add_rule(world_location, can_equip_rod_for("Infused Oceanic"))
        add_rule(world_location, lambda state: can_equip("Siphon Trawler", state, player, include_iron_rig))
    if requirement.value > 1:
        add_rule(world_location, can_equip_rod_for("Infused Shallow"))
        add_rule(world_location, can_equip_rod_for("Infused Coastal"))
    if requirement.value > 0:
        add_rule(world_location, lambda state: state.has("Dredge Crane", player))
        add_rule(world_location, lambda state: state.can_reach_region("The Iron Rig", player))

ICEBREAKER_PARTS = ("Icebreaker Plow Half 1", "Icebreaker Plow Half 2", "Icebreaker Bracing")

def has_item(item_name: str, state: CollectionState, player: int, include_iron_rig: bool) -> bool:
    if item_name == "Icebreaker":
        return state.has(item_name, player) or state.has_all(ICEBREAKER_PARTS, player)
    return can_equip(item_name, state, player, include_iron_rig)

def add_item_rules(requirement, world_location, player, include_iron_rig: bool) -> None:
    if requirement.all_of:
        add_rule(world_location, lambda state: all(has_item(name, state, player, include_iron_rig)
                                                   for name in requirement.all_of))
    if requirement.any_of:
        add_rule(world_location, lambda state: any(has_item(name, state, player, include_iron_rig)
                                                   for name in requirement.any_of))
    return

def can_equip(item_name: str, state: CollectionState, player: int, include_iron_rig: bool) -> bool:
    return (state.has(item_name, player)
            and state.has("Progressive Hull", player, hulls_needed(item_name, include_iron_rig)))

def can_equip_any(item_names, state: CollectionState, player: int, include_iron_rig: bool) -> bool:
    return any(can_equip(item_name, state, player, include_iron_rig) for item_name in item_names)

def has_passage_item(passage_item, state, player):
    return state.has(passage_item, player)

# (knots, lumens). 1800 lumens keeps a full-sanity boat above 0.25 sanity, where Phantom Sharks and Monster Ray
# attacks start, through a whole 12-hour night.
MID_REGIONS_PERFORMANCE = (50, 1800)
OPEN_OCEAN_PERFORMANCE = (50, 2100)
PALE_REACH_PERFORMANCE = (60, 2100)

# Research and shop locations are filed under Open Ocean but aren't done out at sea; pursuits there are met at sea.
AT_SEA_LOCATION_GROUPS = {"Dredge", "Encyclopedia", "World", "Message", "Pursuit"}

BASE_SPEED = 10
ENGINES = tuple(name for name, item in item_table.items() if item.item_group == "Engine")
LIGHTS = tuple(name for name, item in item_table.items() if item.item_group == "Light")


def has_boat_performance(world: DREDGEWorld, performance: tuple[int, int], state: CollectionState) -> bool:
    if not world.options.require_boat_performance:
        return True
    knots, lumens = performance
    player = world.player
    hull_count = state.count("Progressive Hull", player)
    include_iron_rig = bool(world.options.include_iron_rig_dlc)
    engines = [name for name in ENGINES if state.has(name, player)]
    lights = [name for name in LIGHTS if state.has(name, player)]
    return (BASE_SPEED + best_total(engines, "speed", hull_count, include_iron_rig) >= knots
            and best_total(lights, "lumens", hull_count, include_iron_rig) >= lumens)

def can_get_aberrations(world: "DREDGEWorld", state: CollectionState) -> bool:
    """
    Aberrations are in logic once the aberration chance items raise the minimum chance to at least half, or the
    Guaranteed Aberrations item is found. Without either item in the pool they're left to the vanilla chance.
    """
    progressive_count = world.options.progressive_aberration_chance_items.value
    has_guaranteed = bool(world.options.guaranteed_aberrations_item)
    if not progressive_count and not has_guaranteed:
        return True
    player = world.player
    return ((has_guaranteed and state.has("Guaranteed Aberrations", player))
            or (progressive_count > 0
                and state.has("Progressive Aberration Chance", player, (progressive_count + 1) // 2)))

def has_relics(state: CollectionState, player: int) -> bool:
    return state.has("Ornate Key", player) \
        and state.has("Rusted Music Box", player) \
        and state.has("Jewel Encrusted Band", player) \
        and state.has("Shimmering Necklace", player) \
        and state.has("Antique Pocket Watch", player)

def get_catch_type(location: DREDGELocationData) -> str | None:
    for req in location.requirements:
        match req:
            case CatchTypeReq(value=v):
                return v
    return None

def tools_for(catch_type: str, tool_group: str) -> tuple[str, ...]:
    return CATCH_TOOL_INDEX.get((catch_type, tool_group), ())


def add_catch_type_rule(world_location: Location, location: DREDGELocationData, player: int, options: DREDGEOptions) -> None:
    add_rule(world_location, lambda state: can_catch_location(location, state, player, options))


def can_catch_location(location: DREDGELocationData, state: CollectionState, player: int, options: DREDGEOptions) -> bool:
    catch_type = get_catch_type(location)
    if catch_type is None:
        return False

    if catch_type == "Crab":
        return state.has_any(tools_for("Crab", "Crab Pot"), player)

    return can_catch_fish(catch_type, location, state, player, options)


def can_catch_fish(
    catch_type: str,
    location: DREDGELocationData,
    state: CollectionState,
    player: int,
    options: DREDGEOptions,
) -> bool:

    fish_expansion = location.expansion
    include_iron_rig = bool(options.include_iron_rig_dlc)

    has_rod = (
        location.can_catch_rod
        and can_equip_any(tools_for(catch_type, "Rod"), state, player, include_iron_rig)
    )

    allow_net_logic = location.can_catch_net and (not location.can_catch_rod or options.logical_nets)
    has_net = (
        allow_net_logic
        and can_equip_any(tools_for(catch_type, "Net"), state, player, include_iron_rig)
    )

    # Atrophy harvests a whole fishing spot without any tackle.
    has_atrophy = location.can_catch_rod and state.has("Atrophy", player)

    return has_rod or has_net or has_atrophy


def set_completion_condition(world: DREDGEWorld) -> None:
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)