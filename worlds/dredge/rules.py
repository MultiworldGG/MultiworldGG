from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import CollectionState, Location
from worlds.generic.Rules import set_rule, add_rule
from .items import item_table, CATCH_TOOL_INDEX
from .locations import location_table, DREDGELocationData, ItemsReq, CatchTypeReq, ResearchReq, IronRigPhaseReq
from .options import DREDGEOptions

if TYPE_CHECKING:
    from . import DREDGEWorld

def set_all_rules(world: DREDGEWorld) -> None:
    set_region_rules(world)
    set_location_rules(world)
    set_completion_condition(world)

def set_region_rules(world: "DREDGEWorld") -> None:
    player = world.player

    world.get_entrance("Open Ocean to Gale Cliffs").access_rule = \
        lambda state: not world.options.require_engines or has_engines(1, state, player)
    world.get_entrance("Open Ocean to Stellar Basin").access_rule = \
        lambda state: not world.options.require_engines or has_engines(1, state, player)
    world.get_entrance("Open Ocean to Twisted Strand").access_rule = \
        lambda state: not world.options.require_engines or has_engines(1, state, player)
    world.get_entrance("Open Ocean to Devil's Spine").access_rule = \
        lambda state: not world.options.require_engines or has_engines(1, state, player)
    world.get_entrance("Open Ocean to The Iron Rig").access_rule = \
        lambda state: not world.options.require_engines or has_engines(2, state, player)
    world.get_entrance("Open Ocean to The Pale Reach").access_rule = \
        lambda state: not world.options.require_engines or has_engines(2, state, player)
    world.get_entrance("Open Ocean to Insanity").access_rule = \
        lambda state: has_relics(state, player)


def set_location_rules(world: "DREDGEWorld") -> None:
    player = world.player
    for world_location in world.get_locations():
        if world_location.name == "The Collector":
            continue
        location = location_table[world_location.name]
        for requirement in location.requirements:
            match requirement:
                case ItemsReq():
                    add_item_rules(requirement, world_location, player)
                case CatchTypeReq():
                    add_catch_type_rule(world_location, location, player, world.options)
                case ResearchReq():
                    add_research_rule(requirement, world_location, player)
                case IronRigPhaseReq():
                    add_iron_rig_phase_rule(requirement, world_location, player)
                case _:
                    set_rule(world_location, lambda state: True)

def add_iron_rig_phase_rule(requirement, world_location, player) -> None:
    if requirement.value > 4:
        add_rule(world_location, lambda state: state.has_any(tools_for("Infused Mangrove", "Rod"), player))
    if requirement.value > 3:
        add_rule(world_location, lambda state: state.has_any(tools_for("Infused Hadal", "Rod"), player))
        add_rule(world_location, lambda state: state.has_any(tools_for("Infused Abyssal", "Rod"), player))
    if requirement.value > 2:
        add_rule(world_location, lambda state: state.has_any(tools_for("Infused Oceanic", "Rod"), player))
        add_rule(world_location, lambda state: state.has("Siphon Trawler", player))
    if requirement.value > 1:
        add_rule(world_location, lambda state: state.has_any(tools_for("Infused Shallow", "Rod"), player))
        add_rule(world_location, lambda state: state.has_any(tools_for("Infused Coastal", "Rod"), player))
    if requirement.value > 0:
        add_rule(world_location, lambda state: state.has("Dredge Crane", player))

def add_research_rule(requirement, world_location, player) -> None:
    add_rule(world_location, lambda state: state.has("Research Part", player, requirement.cost))
    return

def add_item_rules(requirement, world_location, player) -> None:
    if requirement.all_of:
        add_rule(world_location, lambda state: state.has_all(requirement.all_of, player))
    if requirement.any_of:
        add_rule(world_location, lambda state: state.has_any(requirement.any_of, player))
    return

def has_engines(distance: int, state: CollectionState, player: int) -> bool:
    valid_engines = [name for name, item in item_table.items() if item.item_value >= distance]
    return state.has_any(valid_engines, player)

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
    return CATCH_TOOL_INDEX.get((catch_type, tool_group))


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

    has_rod = (
        location.can_catch_rod
        and state.has_any(tools_for(catch_type, "Rod"), player)
    )

    allow_net_logic = location.can_catch_net and (not location.can_catch_rod or options.logical_nets)
    has_net = (
        allow_net_logic
        and state.has_any(tools_for(catch_type, "Net"), player)
    )

    return has_rod or has_net


def set_completion_condition(world: DREDGEWorld) -> None:
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)