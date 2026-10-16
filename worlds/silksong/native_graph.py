from collections import defaultdict
from dataclasses import replace

from .requirements import req


def _components(graph, mutable=frozenset()):
    edges = {name: set() for name in graph}
    reverse = {name: set() for name in graph}
    for owner, rules in graph.items():
        for all_of, any_of, predicate in rules:
            if owner in mutable:
                continue
            if len(all_of) == 1 and not any_of and predicate == 0:
                source = next(iter(all_of))
                if source in graph and source not in mutable:
                    edges[source].add(owner)
                    reverse[owner].add(source)
    visited = set()
    order = []
    for name in graph:
        if name in visited:
            continue
        visited.add(name)
        stack = [(name, iter(edges[name]))]
        while stack:
            node, children = stack[-1]
            child = next(children, None)
            if child is None:
                order.append(node)
                stack.pop()
            elif child not in visited:
                visited.add(child)
                stack.append((child, iter(edges[child])))
    visited.clear()
    for name in reversed(order):
        if name in visited:
            continue
        group = set()
        pending = [name]
        while pending:
            node = pending.pop()
            if node in visited:
                continue
            visited.add(node)
            group.add(node)
            pending.extend(reverse[node] - visited)
        if len(group) > 1:
            yield group


def _simplify(graph, mutable=frozenset()):
    aliases = {name: name for name in graph}
    empty = (frozenset(), frozenset(), 0)
    while True:
        changed = False
        true = {n for n, rules in graph.items() if n not in mutable and empty in rules}
        false = {n for n, rules in graph.items() if n not in mutable and not rules}
        for owner, rules in graph.items():
            updated = set()
            for all_of, any_of, predicate in rules:
                all_of = frozenset(aliases.get(n, n) for n in all_of)
                any_of = frozenset(aliases.get(n, n) for n in any_of)
                if owner in all_of or all_of & false:
                    continue
                all_of -= true
                if any_of & true:
                    any_of = frozenset()
                elif any_of:
                    any_of -= false
                    if not any_of:
                        continue
                updated.add((all_of, any_of, predicate))
            if empty in updated:
                updated = {empty}
            else:
                groups = defaultdict(list)
                for all_of, any_of, predicate in updated:
                    groups[any_of, predicate].append(all_of)
                updated = set()
                for (any_of, predicate), group in groups.items():
                    smaller = []
                    for atoms in sorted(group, key=len):
                        if not any(previous <= atoms for previous in smaller):
                            smaller.append(atoms)
                            updated.add((atoms, any_of, predicate))
            changed |= updated != rules
            graph[owner] = updated
        merges = {}
        for group in _components(graph, mutable):
            canonical = min(group)
            merges.update((name, canonical) for name in group if name != canonical)
        signatures = {}
        for name in sorted(graph):
            if name in merges or name in mutable:
                continue
            signature = frozenset(graph[name])
            other = signatures.setdefault(signature, name)
            if other != name:
                merges[name] = other
        if merges:
            def canonical(name):
                while name in merges:
                    name = merges[name]
                return name
            merged = defaultdict(set)
            for name, rules in graph.items():
                merged[canonical(name)].update(rules)
            graph = dict(merged)
            aliases = {name: canonical(target) for name, target in aliases.items()}
            changed = True
        if not changed:
            return graph, aliases


def _external_roots(world):
    if getattr(world, "_silk_node_rules", None):
        prefixes = ('Silk (', 'Silk route: ', 'Silk capacity: ',
                    'Silk regeneration: ', 'Silk refill: ', 'Silk restock (')
        return {name for name in world._silksong_native_abstract_names
                if not name.startswith(prefixes)}
    from .requirements import REQUIREMENTS, GOAL_EVENT_BY_KEY, get_pinmaster_oil_requirements
    from .progression_shuffle import world_location_requirements
    from .wish_events import WISH_LOGIC_EVENTS
    from .enemy_souls import enabled_enemies, check_requirements
    from .entrance_randomization import WARP_DESTINATIONS
    from .room_graph_logic import room_node_name

    roots = set(world._progression_events)
    roots.update(GOAL_EVENT_BY_KEY.values())
    roots.update(event.source_region for event in WISH_LOGIC_EVENTS if event.source_region)
    roots.update(room_node_name(node) for _, node in WARP_DESTINATIONS.values())
    groups = [*REQUIREMENTS.values(), *world._progression_events.values(),
              *world._progression_location_rules.values(), get_pinmaster_oil_requirements(True)]
    groups.extend(world_location_requirements(world, name) for name in REQUIREMENTS)
    groups.extend(check_requirements(name) for name in enabled_enemies(world))
    from .scene_exits import fixed_exits
    groups.extend(exit.requirements for exit in fixed_exits(world))
    from .requirement_rules import build_requirements_rule
    from .native_regions import native_rule_options
    from .room_graph_logic import native_region_name
    names = world._silksong_native_abstract_names
    options = native_rule_options(world)
    by_region = {native_region_name(name): name for name in names}
    for rules in dict.fromkeys(groups):
        resolved = build_requirements_rule(
            rules, extra_abstract_requirement_names=names, **options,
        ).resolve(world)
        roots.update(by_region[n] for n in resolved.region_dependencies() if n in by_region)
    return roots


def compact_requirements(world, original, additional_roots=(), *, silk_supply=False):
    from .requirement_rules import build_requirements_rule
    from .native_regions import native_rule_options
    from .entrance_randomization import enabled as entrances_enabled

    if entrances_enabled(world) and not getattr(world, "_silk_node_rules", None):
        return original
    names = world._silksong_native_abstract_names
    options = native_rule_options(world)
    graph = {}
    constants = {}
    predicates = {req(crest=False): 0}
    for owner, rules in original.items():
        retained = set()
        for rule in rules:
            refs = tuple(n for n in rule.all_of if n in names)
            condition = replace(rule, all_of=tuple(n for n in rule.all_of if n not in names))
            if condition not in constants:
                resolved = build_requirements_rule(
                    (condition,), extra_abstract_requirement_names=names, **options,
                ).resolve(world)
                predicate_id = 0
                if not resolved.always_true and not resolved.always_false:
                    predicate = replace(condition, all_of=(), any_of=())
                    predicate_id = predicates.setdefault(predicate, len(predicates))
                constants[condition] = (resolved.always_true, resolved.always_false, predicate_id)
            always_true, always_false, predicate_id = constants[condition]
            if always_false:
                continue
            if always_true:
                retained.add((frozenset(refs), frozenset(), 0))
            else:
                retained.add((frozenset(rule.all_of), frozenset(rule.any_of), predicate_id))
        graph[owner] = retained
    boundaries = set()
    if entrances_enabled(world) and not silk_supply:
        from .entrance_randomization import node_overrides, WARP_DESTINATIONS
        from .silk_economy import at, MAX_SILK
        boundaries.update(node_overrides(world))
        boundaries.update("Room Node: " + node for _, node in WARP_DESTINATIONS.values())
        boundaries.update(at(node, amount) for node in tuple(boundaries)
                          for amount in range(1, MAX_SILK + 1))
    assumed = frozenset(world._progression_events) | boundaries
    from .scene_exits import fixed_exits
    boundaries.update(node for exit in fixed_exits(world) for node in (exit.source, exit.destination) if node in original)
    mutable = frozenset(world._progression_events) | boundaries
    graph, aliases = _simplify(graph, mutable)
    if not getattr(world, '_silk_node_rules', None):
        from .entrance_randomization import WARP_DESTINATIONS
        from .room_graph_logic import room_node_name
        possible = set(assumed) | set(additional_roots)
        possible.update(aliases.get(room_node_name(node), room_node_name(node))
                        for _, node in WARP_DESTINATIONS.values())
        pending = set(graph) - possible
        while pending:
            reached = {
                name for name in pending
                if any(all(n not in graph or n in possible for n in all_of)
                       and (not any_of or any(n not in graph or n in possible for n in any_of))
                       for all_of, any_of, _ in graph[name])
            }
            if not reached:
                break
            possible.update(reached)
            pending.difference_update(reached)
        world._silksong_unreachable_abstract_names = frozenset(
            name for name, target in aliases.items() if target not in possible)
    blocked = getattr(world, '_silksong_unreachable_abstract_names', frozenset())
    predicates = tuple(predicates)

    def anchor_order(name):
        if name.startswith('Silk ('):
            return 0, name
        if name.startswith(('Room Node: ', 'Entrance landing: ', 'Silk restock ')):
            return 1, name
        return 2, name

    result = {}
    for name, target in aliases.items():
        if name in blocked:
            continue
        if name != target:
            result[name] = (req(target, crest=False),)
        else:
            result[name] = tuple(sorted((
                replace(predicates[predicate],
                        all_of=tuple(sorted(all_of, key=anchor_order)),
                        any_of=tuple(sorted(any_of)))
                for all_of, any_of, predicate in graph[name]
            ), key=repr))
    roots = _external_roots(world) & result.keys()
    roots.update(name for name in (*additional_roots, *boundaries) if name in result)
    retained_rules = (*world._progression_location_rules.values(),
                      *(original[name] for name in world._progression_events))
    for rules in retained_rules:
        for rule in rules:
            roots.update(n for n in (*rule.all_of, *rule.any_of) if n in result)
    needed = set()
    pending = list(roots)
    while pending:
        name = pending.pop()
        if name in needed:
            continue
        needed.add(name)
        for rule in result[name]:
            pending.extend(n for n in (*rule.all_of, *rule.any_of) if n in result and n not in needed)
    return {name: rules for name, rules in result.items() if name in needed}
