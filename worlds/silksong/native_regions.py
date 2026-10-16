from __future__ import annotations

from .options import get_silk_and_soul_points

from collections.abc import Mapping
from functools import lru_cache

from BaseClasses import Region
from rule_builder.rules import Rule

from .requirement_rules import build_location_rule, build_requirements_rule
from .requirements import (
    LocationRequirement,
    POLLIP_HEART_COUNT,
    get_abstract_requirements,
)
from .prices import get_shell_shard_donation_tool_pouch_requirements
from .room_graph_logic import ROOM_NODE_PREFIX, native_region_name


def native_rule_options(world) -> dict[str, object]:
    return {
        "split_dash_and_sprint": world.is_split_dash_and_sprint(),
        "silk_heart_logic": bool(world.options.silk_heart_logic.value),
        "allow_bellways_before_bell_beast": (
            world.allows_bellways_before_bell_beast()
        ),
        "proficient_combat": world.get_proficient_combat_mode(),
        "proficient_movement": bool(getattr(getattr(world.options, "proficient_movement", None), "value", 0)),
        "flea_brew_jump_logic": bool(getattr(getattr(world.options, "flea_brew_jump_logic", None), "value", 0)),
        "sharpdart_logic": bool(getattr(getattr(world.options, "sharpdart_logic", None), "value", 0)),
        "red_tool_stall_tier": int(world.options.red_tool_stall_logic.value),
        "crest_pogo_tier": int(world.options.crest_pogo_logic.value),
        "needle_strike_tier": int(world.options.needle_strike_logic.value),
        "enemy_pogo_tier": int(world.options.enemy_pogo_logic.value),
        "drill_crystal_pogo_tier": int(world.options.drill_crystal_pogo_logic.value),
        "heal_stall_tier": int(world.options.heal_stall_logic.value),
        "hazard_respawn_tier": int(world.options.hazard_respawn_logic.value),
        "scuttlebrace_tier": int(world.options.scuttlebrace_logic.value),
        "bell_shrine_sanity": world.get_category_mode("BellShrine") != "vanilla",
        "steel_soul": world.is_steel_soul(),
        "silk_and_soul_points": get_silk_and_soul_points(world.options),
        "randomized_crest_slots_enabled": (
            world.get_category_mode("CrestSlot") != "vanilla"
        ),
        "starting_location": world.get_starting_location_key(),
        "trails_end_requirement": world.get_trails_end_requirement_key(),
        "scuttlebrace_logic_enabled": (
            world.is_scuttlebrace_logic_enabled()
        ),
        "randomize_ledge_grab": (
            world.is_ledgegrab_ability_rando_enabled()
        ),
        "randomize_swim": world.is_swim_ability_rando_enabled(),
        "native_abstract_regions": True,
    }


def get_native_abstract_requirements(world):
    from .entrance_randomization import node_overrides
    from .enemy_souls import node_overrides as enemy_nodes

    requirements = dict(get_abstract_requirements(
        world.allows_bellways_before_bell_beast(),
        world.get_category_mode("CrestSlot") != "vanilla",
        world.get_starting_location_key(),
        world.get_trails_end_requirement_key(),
        (
            POLLIP_HEART_COUNT
            if world.get_category_mode("PollipHeart") != "vanilla"
            else 0
        ),
        randomize_ledge_grab=(
            world.is_ledgegrab_ability_rando_enabled()
        ),
        randomize_swim=world.is_swim_ability_rando_enabled(),
        proficient_combat=world.get_proficient_combat_mode(),
        proficient_movement=bool(getattr(getattr(world.options, "proficient_movement", None), "value", 0)),
        flea_brew_jump_logic=bool(getattr(getattr(world.options, "flea_brew_jump_logic", None), "value", 0)),
        sharpdart_logic=bool(getattr(getattr(world.options, "sharpdart_logic", None), "value", 0)),
        red_tool_stall_tier=int(world.options.red_tool_stall_logic.value),
        crest_pogo_tier=int(world.options.crest_pogo_logic.value),
        needle_strike_tier=int(world.options.needle_strike_logic.value),
        enemy_pogo_tier=int(world.options.enemy_pogo_logic.value),
        drill_crystal_pogo_tier=int(world.options.drill_crystal_pogo_logic.value),
        heal_stall_tier=int(world.options.heal_stall_logic.value),
        hazard_respawn_tier=int(world.options.hazard_respawn_logic.value),
        scuttlebrace_tier=int(world.options.scuttlebrace_logic.value),
        bell_shrine_sanity=world.get_category_mode("BellShrine") != "vanilla",
        steel_soul=world.is_steel_soul(),
        steel_soul_sites=world._steel_soul_sites,
        silk_and_soul_points=get_silk_and_soul_points(world.options),
        donation_tool_pouch_requirements=get_shell_shard_donation_tool_pouch_requirements(world.get_purchase_prices()),
        room_node_overrides=enemy_nodes(world, node_overrides(world)),
    ))
    from .game_modes import RESTING_SITES_VISITED, resting_site_requirements
    requirements[RESTING_SITES_VISITED] = resting_site_requirements(world._steel_soul_sites)
    return requirements


def choose_requirement_anchor(
    requirement: LocationRequirement,
    abstract_names: frozenset[str],
    owner: str | None = None,
) -> str | None:
    candidates = tuple(
        name
        for name in requirement.all_of
        if name in abstract_names
    )
    return next(
        (name for name in candidates if name != owner),
        candidates[0] if candidates else None,
    )


def choose_location_anchor(
    requirements: tuple[LocationRequirement, ...],
    abstract_names: frozenset[str],
) -> str | None:
    if not requirements:
        return None
    common = set(
        name
        for name in requirements[0].all_of
        if name in abstract_names
    )
    for requirement in requirements[1:]:
        common.intersection_update(
            name
            for name in requirement.all_of
            if name in abstract_names
        )
    if not common:
        return None
    return next(
        (
            name
            for name in sorted(common)
            if name.startswith(ROOM_NODE_PREFIX)
        ),
        sorted(common)[0],
    )


@lru_cache(maxsize=16)
def _intern_abstract_names(names):
    return names


def create_native_logic_region_map(world) -> Mapping[str, Region]:
    from .progression_shuffle import prepare_world
    requirements = prepare_world(world, get_native_abstract_requirements(world))
    abstract_names = _intern_abstract_names(frozenset(requirements))
    world._silksong_native_abstract_names = abstract_names
    world._silksong_native_abstract_requirements = requirements
    from .silk_supply import compile_regions
    compiled_requirements = compile_regions(world, requirements)
    world._silksong_native_compiled_requirements = compiled_requirements
    world._silksong_native_region_names = frozenset(compiled_requirements)
    region_names = abstract_names if compiled_requirements is requirements else compiled_requirements
    regions = {
        name: Region(native_region_name(name), world.player, world.multiworld)
        for name in region_names
    }
    world.multiworld.regions.extend(regions.values())
    return regions


def _native_source_dependencies(world, name):
    from .native_graph import compact_requirements

    graph = getattr(world, '_silksong_source_graph', None)
    if graph is None:
        graph = compact_requirements(world, world._silksong_native_abstract_requirements)
        world._silksong_source_graph = graph
        world._silksong_source_dependencies = {}
    cache = world._silksong_source_dependencies
    if name not in cache:
        if name not in graph:
            return None
        names = world._silksong_native_abstract_names
        grouped = {}
        for requirement in graph[name]:
            anchor = choose_requirement_anchor(requirement, names, name)
            grouped.setdefault(anchor, []).append(requirement)
        items, regions = set(), set()
        external = False
        for anchor, rules in grouped.items():
            rule = build_requirements_rule(
                tuple(rules), anchor_requirement_name=anchor,
                extra_abstract_requirement_names=names, **native_rule_options(world),
            ).resolve(world)
            if rule.always_false:
                continue
            items.update(rule.item_dependencies())
            regions.update(rule.region_dependencies())
            regions.add(native_region_name(anchor) if anchor is not None else 'Menu')
            external |= bool(rule.location_dependencies() or rule.entrance_dependencies())
        cache[name] = frozenset(items), frozenset(regions), external
    items, regions, external = cache[name]
    supply = getattr(world, '_silk_supply', None)
    if supply is not None:
        exit_items, exit_regions = supply.exit_dependencies(name)
        items, regions = items | exit_items, regions | exit_regions
    return items, regions, external


def native_source_requires_assumption(
    world,
    location_name: str,
    reward_name: str,
    pollip_heart_count: int,
    anchor_requirement_name: str | None,
    rule_dependencies: dict[str, tuple[frozenset[str], frozenset[str], bool]] | None = None,
) -> bool:
    if reward_name == "Memory Locket" or reward_name.startswith(("Bellway: ", "Ventrica: ")):
        return False
    child = build_location_rule(
        location_name,
        pollip_heart_count=pollip_heart_count,
        anchor_requirement_name=anchor_requirement_name,
        **native_rule_options(world),
    ).resolve(world)
    if (
        child.player != world.player
        or reward_name in child.item_dependencies()
        or child.location_dependencies()
        or child.entrance_dependencies()
    ):
        return True
    pending = set(child.region_dependencies())
    if anchor_requirement_name is not None:
        pending.add(native_region_name(anchor_requirement_name))
    source_names = {}
    if getattr(world, '_silk_supply', None) is not None:
        source_names = getattr(world, '_silksong_source_names', None)
        if source_names is None:
            source_names = {native_region_name(name): name for name in world._silksong_native_abstract_names}
            world._silksong_source_names = source_names
    dependencies_by_region = rule_dependencies if rule_dependencies is not None else {}
    visited: set[str] = set()
    while pending:
        region_name = pending.pop()
        if region_name in visited:
            continue
        dependencies = dependencies_by_region.get(region_name)
        if dependencies is None:
            if region_name in source_names:
                dependencies = _native_source_dependencies(world, source_names[region_name])
                if dependencies is None:
                    return True
            else:
                try:
                    region = world.multiworld.get_region(region_name, world.player)
                except KeyError:
                    return True
                if region.player != world.player:
                    return True
                items, regions = set(), set()
                external = False
                for entrance in region.entrances:
                    access_rule = entrance.access_rule
                    if access_rule is not type(entrance).access_rule:
                        if not isinstance(access_rule, Rule.Resolved) or access_rule.player != world.player:
                            return True
                        items.update(access_rule.item_dependencies())
                        regions.update(access_rule.region_dependencies())
                        external |= bool(access_rule.location_dependencies() or access_rule.entrance_dependencies())
                    parent_region = entrance.parent_region
                    if parent_region is None or parent_region.player != world.player:
                        return True
                    regions.add(parent_region.name)
                dependencies = frozenset(items), frozenset(regions), external
            dependencies_by_region[region_name] = dependencies
        items, regions, external = dependencies
        if reward_name in items or external:
            return True
        visited.add(region_name)
        pending.update(regions)
    return False


def _native_entrance_groups(world, requirements, anchor_names):
    from .scene_exits import fixed_exits

    scene_connections = {(exit.destination, exit.source) for exit in fixed_exits(world)}
    for owner, alternatives in requirements.items():
        grouped = {}
        for requirement in alternatives:
            anchor = choose_requirement_anchor(requirement, anchor_names, owner)
            if (owner, anchor) not in scene_connections:
                grouped.setdefault(anchor, []).append(requirement)
        for anchor, rules in grouped.items():
            source = native_region_name(anchor) if anchor is not None else 'Menu'
            yield owner, anchor, f'{source} -> {native_region_name(owner)}', rules


def connect_native_logic_regions(
    world,
    menu: Region,
    regions: Mapping[str, Region],
) -> None:
    requirements = world._silksong_native_compiled_requirements
    abstract_names = world._silksong_native_abstract_names
    anchor_names = world._silksong_native_region_names
    options = native_rule_options(world)

    for owner, anchor, name, grouped_requirements in _native_entrance_groups(world, requirements, anchor_names):
        rule = build_requirements_rule(
            tuple(grouped_requirements),
            anchor_requirement_name=anchor,
            extra_abstract_requirement_names=abstract_names,
            **options,
        )
        entrance = world.create_entrance(
            regions[anchor] if anchor is not None else menu,
            regions[owner],
            rule,
            name,
        )
        if entrance is not None:
            entrance.display_name = f'{region_label(anchor or "Menu")} -> {region_label(owner)}'

    supply = getattr(world, '_silk_supply', None)
    if supply is not None:
        from .silk_supply import SilkSupplyRule
        for name in sorted(supply.boundaries):
            world.create_entrance(menu, regions[name], SilkSupplyRule(name), f'Silksong Silk: {name}')


@lru_cache(maxsize=1)
def _room_node_labels():
    from .room_graph import load_room_graph
    return {ROOM_NODE_PREFIX + node.id: f'{room.name} ({node.name})'
            for room in load_room_graph().authoritative_rooms for node in room.nodes}


def region_label(name):
    return _room_node_labels().get(name, native_region_name(name))


def explain_path(entrance, state):
    label = getattr(entrance, 'display_name', None)
    if label is None:
        return []
    result = [{'type': 'color', 'color': 'blue', 'text': label}]
    if hasattr(entrance.access_rule, 'explain_json'):
        result.append({'type': 'text', 'text': ':\n    '})
        result.extend(entrance.access_rule.explain_json(state))
    return result
