from __future__ import annotations

import json
import pkgutil
from collections import defaultdict
from dataclasses import replace

MAX_SILK = 18
COST_PREFIX = 'Silk Cost: '
SOURCES = tuple(json.loads(pkgutil.get_data(__package__, 'silk_sources.json')))


def enabled(world):
    if not world.options.enemy_souls:
        return False
    passthrough = getattr(world.multiworld, 're_gen_passthrough', {}).get(world.game)
    return passthrough is None or passthrough.get('enemy_soul_silk_logic', 0) == 1


def location_overrides(world, overrides):
    if not enabled(world):
        return overrides
    from .requirements import REQUIREMENTS
    result = dict(overrides)
    for name, rules in REQUIREMENTS.items():
        original = result.get(name, rules)
        updated = gate_location(world, original)
        if updated != original:
            result[name] = updated
    return result


def atom_cost(atoms, clause):
    if is_wish_menu(clause):
        return 0
    counts = {'clawline': 0, 'sharpdart': 0}
    for atom in atoms:
        for name in counts:
            if atom.startswith('mapper:' + name + ':'):
                counts[name] = max(counts[name], int(atom.rsplit(':', 1)[1]))
    return (rule_cost(clause) + max(0, counts['clawline'] - 1)
            + 4 * max(0, counts['sharpdart'] - 1))


def is_wish_menu(rule):
    return (source_node(rule) or '').startswith('Room Node: wish-menus/')


def rule_cost(rule):
    if is_wish_menu(rule):
        return 0
    names = set(rule.all_of)
    explicit = [int(n[len(COST_PREFIX):]) for n in names if n.startswith(COST_PREFIX)]
    if explicit:
        return max(explicit)
    return (int('Ancestral Art: Clawline' in names)
            + int('Ancestral Art: Silk Soar' in names)
            + int('Ancestral Art: Needolin' in names)
            + 4 * sum(n in names for n in ('Usable Sharpdart', 'Usable Rune Rage', 'Usable Thread Storm'))
            + 4 * int(rule.require_silk_spear)
            + 9 * int(any(n.startswith('Technique: Heal Stall ') for n in names)))


def clean(rule):
    return replace(rule, all_of=tuple(n for n in rule.all_of if not n.startswith(COST_PREFIX)))


def at(node, amount):
    return node if amount == 0 else f'Silk ({amount}): {node.removeprefix("Room Node: ")}'


def source_node(rule):
    return next((n for n in rule.all_of if n.startswith(('Room Node: ', 'Entrance landing: '))), None)


def gate(rule):
    node = source_node(rule)
    cost = rule_cost(rule) if node else 0
    rule = clean(rule)
    if not cost:
        return rule
    return replace(rule, all_of=tuple(dict.fromkeys((*rule.all_of, at(node, cost)))))


def gate_location(world, rules):
    return tuple(gate(rule) for rule in rules) if enabled(world) else rules


def capacity(amount):
    from .requirements import item_count, req, SPOOL_FRAGMENT_ITEM_NAMES
    return req(crest=False, item_counts=(item_count(2 * (amount - 9), *SPOOL_FRAGMENT_ITEM_NAMES),)) if amount > 9 else req(crest=False)


def _refills(world, graph):
    from .enemy_souls import enabled_enemies, item_name, pogo_graph
    from .room_graph_logic import compile_transition_requirements, _compile_spec
    from .requirements import _compiled_room_clause_requirement, req
    from .entrance_randomization import enabled, scoped_pool, scope, members

    names = enabled_enemies(world)
    mapped = pogo_graph(names)
    ports = mapped.transition_by_id
    removed = {p for row in scoped_pool(scope(world), world.get_content_scope()).values() for p in members(row)} if enabled(world) else set()
    refills = defaultdict(list)
    for room in mapped.authoritative_rooms:
        for event in room.events:
            owner = 'Room Event: ' + event.id
            if event.kind == 'bench' and event.is_compilable and owner in graph:
                refills['Room Node: ' + event.node_id].append(req(owner, 'Sylphsong', crest=False))
        candidates = [row for row in SOURCES if row['room'] == room.id and row['name'] in names]
        if not candidates:
            continue
        exits = []
        for port in room.transitions:
            back = ports.get(port.target.port_id)
            if (not port.is_compilable or back is None or not back.is_compilable
                    or back.target.port_id != port.id or port.id in removed or back.id in removed
                    or back.source_node_id.split('#')[0] == room.id):
                continue
            outward = [clean(_compiled_room_clause_requirement(c)) for c in compile_transition_requirements(port, include_source=False, silk_costs=True) if not c.silk_cost]
            inward = [clean(_compiled_room_clause_requirement(c)) for c in compile_transition_requirements(back, include_source=False, silk_costs=True) if not c.silk_cost]
            if outward and inward:
                exits.append((port.id, port.source_node_id, outward, inward))
        for index, (port_id, anchor, outward, inward) in enumerate(exits):
            prefix = f'Silk restock ({room.id}, {index}): '
            node_names = {n.id for n in room.nodes}
            forward = {n: [] for n in node_names}
            reverse = {n: [] for n in node_names}
            forward[anchor].append(req('Room Node: ' + anchor, crest=False))
            reverse[anchor].append(req('Room Node: ' + anchor, crest=False))
            for edge in room.connections:
                if not edge.is_compilable:
                    continue
                for clause in _compile_spec(edge.requirement, silk_costs=True):
                    if clause.silk_cost:
                        continue
                    rule = clean(_compiled_room_clause_requirement(clause))
                    forward[edge.target_node_id].append(replace(rule, all_of=(prefix + 'out/' + edge.source_node_id, *rule.all_of)))
                    reverse[edge.source_node_id].append(replace(rule, all_of=(prefix + 'back/' + edge.target_node_id, *rule.all_of)))
            for n in node_names:
                graph[prefix + 'out/' + n] = tuple(forward[n])
                graph[prefix + 'back/' + n] = tuple(reverse[n])
            loop = prefix + 'exit'
            graph[loop] = tuple(req(*dict.fromkeys((*a.all_of, *b.all_of)), crest=False,
                                   item_counts=tuple(dict.fromkeys((*a.item_counts, *b.item_counts))),
                                   skip_tier=max(a.minimum_skip_tier, b.minimum_skip_tier))
                                for a in outward for b in inward)
            for row in candidates:
                if port_id not in row['exits']:
                    continue
                refill = req(item_name(row['name']), loop,
                             *(('Act: ' + str(row['act']),) if row['act'] > 1 else ()),
                             *(prefix + direction + n for n in row['nodes'] for direction in ('out/', 'back/')))
                for n in row['nodes']:
                    refills['Room Node: ' + n].append(refill)
    return refills


def prepare_world(world, graph):
    if not enabled(world):
        return graph
    from .requirements import req, item_count

    original = dict(graph)
    graph = {owner: tuple(gate(rule) if source_node(rule) else clean(rule) for rule in rules)
             for owner, rules in original.items()}
    refills = _refills(world, graph)
    nodes = {name: rules for name, rules in original.items() if name.startswith(('Room Node: ', 'Entrance landing: '))}
    world._silk_node_rules = nodes
    for amount in range(1, MAX_SILK + 1):
        graph[f'Silk capacity: {amount}'] = (capacity(amount),)
        graph[f'Silk regeneration: {amount}'] = (req(crest=False, item_counts=(item_count(amount, 'Progressive Silkheart'),)),) if amount <= 3 else ()
    impossible = {name for name, rules in original.items() if not rules and name not in nodes}
    skip = int(getattr(getattr(world.options, 'skips', 0), 'value', 0))
    def possible(rule):
        return rule.minimum_skip_tier <= skip and not impossible.intersection(rule.all_of)
    while True:
        added = {name for name, rules in original.items() if name not in impossible and name not in nodes and not any(possible(rule) for rule in rules)}
        if not added:
            break
        impossible.update(added)
    route_index = 0
    for node, incoming in sorted(nodes.items()):
        routes = defaultdict(list)
        for rule in incoming:
            source = source_node(rule)
            if source is not None and possible(rule):
                routes[(source, rule_cost(rule))].append(replace(clean(rule), all_of=tuple(n for n in clean(rule).all_of if n != source)))
        transfers = []
        for (source, cost), rules in sorted(routes.items()):
            route = f'Silk route: {route_index}'
            route_index += 1
            graph[route] = tuple(dict.fromkeys(rules))
            transfers.append((source, cost, route))
        refill = 'Silk refill: ' + node.removeprefix('Room Node: ')
        graph[refill] = tuple(refills.get(node, ()))
        for amount in range(1, MAX_SILK + 1):
            rules = []
            if node not in impossible:
                if amount <= 3:
                    rules.append(req(node, f'Silk regeneration: {amount}', crest=False))
                if graph[refill]:
                    rules.append(req(node, refill, f'Silk capacity: {amount}', crest=False))
                rules.extend(req(at(source, amount + cost), route, crest=False)
                             for source, cost, route in transfers if amount + cost <= MAX_SILK)
            graph[at(node, amount)] = tuple(rules)
    for owner, rules in graph.items():
        for rule in rules:
            for name in rule.all_of:
                if name.startswith('Silk (') and name not in graph:
                    raise ValueError('Unresolved silk route: ' + owner + ' -> ' + name)
    return graph


def export_world(world, slot_data):
    slot_data['enemy_soul_silk_logic'] = int(enabled(world))
    if not enabled(world):
        return
    from .requirements import _export_requirement_group
    from .entrance_randomization import node_overrides
    graph = dict(world._silksong_native_abstract_requirements)
    for node, incoming in (node_overrides(world, connected=True) or {}).items():
        graph[node] = tuple(gate(rule) for rule in incoming)
        for amount in range(1, MAX_SILK + 1):
            transfers = []
            for rule in incoming:
                if rule in world._silk_node_rules.get(node, ()):
                    continue
                source = source_node(rule)
                cost = rule_cost(rule)
                if source is None or amount + cost > MAX_SILK:
                    continue
                rule = clean(rule)
                transfers.append(replace(rule, all_of=tuple(at(n, amount + cost) if n == source else n for n in rule.all_of)))
            graph[at(node, amount)] = tuple(dict.fromkeys((*graph[at(node, amount)], *transfers)))
    for name, rules in graph.items():
        group = _export_requirement_group(rules)
        if name.startswith('Silk '):
            group['alternatives'] = [{key: value for key, value in rule.items() if value}
                                     for rule in group['alternatives']]
        slot_data['abstract_requirements'].setdefault(name, {}).update(group)
    for name, rules in world._progression_location_rules.items():
        slot_data['requirements'][name] = _export_requirement_group(rules)


def attach_exit(world, entrance, rules):
    if not enabled(world):
        return
    from BaseClasses import Entrance
    from .native_regions import native_rule_options
    from .requirement_rules import build_requirements_rule

    supply = getattr(world, '_silk_supply', None)

    class SilkEntrance(Entrance):
        @property
        def connected_region(self):
            return self._silk_destination

        @connected_region.setter
        def connected_region(self, region):
            self._silk_destination = region
            if supply is not None:
                supply.connect_exit(self.name, region)
                return
            for edge in self._silk_edges:
                edge.parent_region.exits.remove(edge)
                if edge.connected_region is not None:
                    edge.connected_region.entrances.remove(edge)
                for name in edge.access_rule.region_dependencies():
                    connections = world.multiworld.indirect_connections.get(world.get_region(name))
                    if connections is not None:
                        connections.discard(edge)
            self._silk_edges.clear()
            if region is None:
                return
            destinations = [region] if region.name in world._silk_node_rules else [edge.connected_region for edge in region.exits if edge.connected_region is not None]
            for index, (amount, cost, rule) in enumerate(self._silk_patterns):
                for destination in destinations:
                    if destination.name not in world._silk_node_rules:
                        continue
                    edge = world.create_entrance(
                        world.get_region(at(self.parent_region.name, amount + cost)),
                        world.get_region(at(destination.name, amount)),
                        rule,
                        f'{self.name} / silk {index} / {destination.name}', force_creation=True)
                    edge.hide_path = True
                    self._silk_edges.append(edge)

    destination = entrance.connected_region
    entrance._silk_destination = destination
    entrance._silk_edges = []
    entrance._silk_patterns = []
    if supply is None:
        for rule in rules:
            cost = rule_cost(rule)
            resolved = build_requirements_rule((clean(rule),),
                extra_abstract_requirement_names=world._silksong_native_abstract_names,
                **native_rule_options(world))
            for amount in range(1, MAX_SILK - cost + 1):
                entrance._silk_patterns.append((amount, cost, resolved))
    entrance.__dict__.pop('connected_region', None)
    entrance.__class__ = SilkEntrance
    entrance.connected_region = destination
