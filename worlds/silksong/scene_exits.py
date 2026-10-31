from dataclasses import dataclass, replace
from functools import lru_cache

from .room_graph import load_room_graph
from .room_graph_logic import compile_transition, room_node_name, _append_requirements


@dataclass(frozen=True)
class SceneExit:
    transition_ids: tuple[str, ...]
    id: str
    name: str
    source: str
    destination: str
    requirements: tuple
    transport_requirements: tuple | None = None

    @property
    def shuffled(self):
        return self.transport_requirements is not None


@lru_cache(maxsize=1)
def exit_names():
    from .entrance_randomization import POOL, members

    names = {port.id: f'{room.name} - {port.name} ({port.alias})'
             for room in load_room_graph().authoritative_rooms for port in room.transitions}
    names.update((member, data['name']) for data in POOL.values() for member in members(data))
    return names


def entrance_name(transition_id):
    return exit_names()[transition_id]


@lru_cache(maxsize=8)
def _scene_exits(enemy_names, silk, scope_name, content_scope, bosses):
    from .enemy_souls import pogo_graph, _combat_gate
    from .requirements import _compiled_room_clause_requirement
    from .silk_economy import gate
    from .progression_shuffle import story_route_rules
    from .entrance_randomization import POOL, scoped_pool, members, endpoint_name, exit_clauses

    graph = pogo_graph(enemy_names)
    ports = graph.transition_by_id
    nodes = {node.id for room in graph.authoritative_rooms for node in room.nodes}
    selected = scoped_pool(scope_name, content_scope) if scope_name is not None else {}
    shuffled = {member for data in selected.values() for member in members(data)}
    exits = {}
    for room in graph.authoritative_rooms:
        for port in room.transitions:
            target = ports.get(port.target.port_id)
            if (port.id in shuffled or not port.is_compilable or target is None
                    or target.source_node_id not in nodes):
                continue
            compiled = compile_transition(port, silk_costs=silk)
            name = entrance_name(compiled.id)
            destination = room_node_name(target.source_node_id)
            clauses = {}
            _append_requirements(clauses, destination, compiled.requirements)
            rules = tuple(_combat_gate(_compiled_room_clause_requirement(clause), enemy_names)
                          for clause in clauses[destination])
            rules = story_route_rules(destination, rules, bosses)
            if silk:
                rules = tuple(gate(rule) for rule in rules)
            if name in exits:
                previous = exits[name]
                if (compiled.source, destination, rules) != (previous.source, previous.destination, previous.requirements):
                    raise ValueError('Scene exit aliases have different routes: ' + name)
                exits[name] = replace(previous, transition_ids=(*previous.transition_ids, port.id))
            else:
                exits[name] = SceneExit((port.id,), port.id, name, compiled.source, destination, rules)
    for source, data in selected.items():
        node = endpoint_name(data, ports)
        destination = endpoint_name(POOL[data['vanilla']], ports)
        clauses = exit_clauses(data, ports, include_source=False, silk_costs=silk)
        transport = tuple(_compiled_room_clause_requirement(clause) for clause in clauses)
        rules = (tuple(gate(replace(rule, all_of=(node, *rule.all_of))) for rule in transport)
                 if silk else transport)
        exits[data['name']] = SceneExit(members(data), source, data['name'], node, destination, rules, transport)
    return tuple(exits.values())


def scene_exits(world):
    result = getattr(world, '_scene_exit_definitions', None)
    if result is None:
        from .enemy_souls import enabled_enemies
        from .entrance_randomization import enabled, scope
        from .silk_economy import enabled as silk_enabled
        from .requirements import BONE_BOTTOM_BELLWAY_NODE, bone_bottom_bellway_requirements

        exits = _scene_exits(enabled_enemies(world), silk_enabled(world), scope(world) if enabled(world) else None,
                             world.get_content_scope(), tuple(boss.identity for boss in world._progression_bosses))
        graph = world._silksong_native_abstract_requirements
        result = tuple(exit if exit.shuffled or graph[exit.destination] else replace(exit, requirements=())
                       for exit in exits)
        result = tuple(replace(exit, requirements=bone_bottom_bellway_requirements(
            exit.requirements, world.get_starting_location_key()))
            if exit.destination == BONE_BOTTOM_BELLWAY_NODE else exit for exit in result)
        world._scene_exit_definitions = result
    return result


def fixed_exits(world):
    return tuple(exit for exit in scene_exits(world) if not exit.shuffled)


def shuffled_exits(world):
    return tuple(exit for exit in scene_exits(world) if exit.shuffled)


def create_exits(world, regions):
    from BaseClasses import EntranceType
    from .native_regions import native_rule_options
    from .requirement_rules import build_requirements_rule
    from .entrance_randomization import pairing_group, scope
    from .silk_economy import attach_exit

    world.scene_exits = {}
    world._entrance_exits = {}
    options = native_rule_options(world)
    for exit in scene_exits(world):
        if exit.source not in regions or exit.destination not in regions:
            missing = {exit.source, exit.destination} - regions.keys()
            assert missing <= world._silksong_unreachable_abstract_names
            continue
        entrance = world.create_entrance(
            regions[exit.source], regions[exit.destination],
            build_requirements_rule(exit.requirements, anchor_requirement_name=exit.source,
                                    extra_abstract_requirement_names=world._silksong_native_abstract_names,
                                    **options),
            exit.name, force_creation=True,
        )
        entrance.display_name = exit.name
        for transition_id in exit.transition_ids:
            world.scene_exits[transition_id] = entrance
        if exit.shuffled:
            attach_exit(world, entrance, exit.transport_requirements)
            entrance.randomization_type = EntranceType.TWO_WAY
            entrance.randomization_group = pairing_group(exit.id, scope(world))
            world._entrance_exits[exit.id] = entrance
