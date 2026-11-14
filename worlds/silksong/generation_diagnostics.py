from collections import defaultdict, deque
from functools import lru_cache
import logging

from .room_graph import load_room_graph
from .room_graph_logic import ROOM_NODE_PREFIX


@lru_cache(maxsize=1)
def _mapped_approaches():
    graph = load_room_graph()
    incoming, checks, labels = defaultdict(list), defaultdict(list), {}
    ports = graph.transition_by_id
    for room in graph.authoritative_rooms:
        for node in room.nodes:
            labels[node.id] = f'{room.name} ({node.name})'
        for check in room.checks:
            if check.canonical_location and check.node_id:
                checks[check.canonical_location].append(check.node_id)
        for route in room.connections:
            if route.source_node_id and route.target_node_id:
                incoming[route.target_node_id].append((route.source_node_id, route.requirement.raw))
        for port in room.transitions:
            target = ports.get(port.target.port_id)
            if port.source_node_id and target and target.source_node_id:
                incoming[target.source_node_id].append((port.source_node_id, port.requirement.raw))
    return incoming, checks, labels


def blocked_approach(world, name, state):
    if world.options.entrance_randomization:
        return ''
    incoming, checks, labels = _mapped_approaches()
    pending = deque(checks.get(name, ()))
    seen = set()
    reached = {}

    def can_reach(node):
        if node not in reached:
            try:
                reached[node] = world.get_region(ROOM_NODE_PREFIX + node).can_reach(state)
            except KeyError:
                reached[node] = False
        return reached[node]

    while pending:
        node = pending.popleft()
        if node in seen or can_reach(node):
            continue
        seen.add(node)
        for source, requirement in incoming[node]:
            if can_reach(source):
                return (f' Blocked approach: {labels[source]} -> {labels[node]}. '
                        f'Mapped requirement: {requirement}.')
            pending.append(source)
    return ''


def unavailable_native_rewards(world, state):
    from .items import get_vanilla_reward_name
    from .locations import location_data_table, PAIRED_LOCATION_CATEGORIES

    result = []
    excluded = world.get_goal_excluded_location_names()
    for name in sorted(world.get_logic_unknown_locations() - excluded):
        data = location_data_table.get(name)
        if (data is None or data.category not in PAIRED_LOCATION_CATEGORIES
                or world.get_location_randomization_mode(name, data.category) != 'vanilla'):
            continue
        reward = get_vanilla_reward_name(name, data.category)
        if world.create_item(reward).advancement and not state.has(reward, world.player):
            result.append((name, reward))
    return result


def native_failure_detail(world, state):
    missing = unavailable_native_rewards(world, state)
    if not missing:
        return ''
    names = ', '.join(name for name, _ in missing[:4])
    if len(missing) > 4:
        names += f' and {len(missing) - 4} more'
    return (f' Vanilla progression sources unavailable with the selected logic options: {names}.'
            + blocked_approach(world, missing[0][0], state))


def validate_plando(multiworld, game):
    from Options import OptionError

    for blocks in getattr(multiworld, 'plando_item_blocks', {}).values():
        for block in blocks:
            if (not block.count.get('min', 0) or not block.items or not block.resolved_locations
                    or {'early_locations', 'non_early_locations'} & set(block.locations)):
                continue
            owner = multiworld.worlds[block.player]
            if not all((item := owner.create_item(name)).advancement or item.useful for name in block.items):
                continue
            targets = block.resolved_locations
            if not all(multiworld.worlds[loc.player].game == game
                       and loc.name in multiworld.worlds[loc.player].get_logic_unknown_locations()
                       for loc in targets):
                continue
            names = ', '.join(str(loc) for loc in targets[:4])
            first = targets[0]
            world = multiworld.worlds[first.player]
            message = (f'Item plando cannot place progression or useful items at {names}: '
                       'these locations allow only filler and traps because their mapped access is unresolved '
                       'or unavailable with the selected logic options.'
                       + blocked_approach(world, first.name, multiworld.get_all_state(False))
                       + ' Choose another location or compatible traversal settings.')
            if block.force is True:
                raise OptionError(message)
            (logging.warning if block.force is False else logging.debug)(message)
