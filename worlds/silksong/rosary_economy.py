from contextlib import contextmanager
from dataclasses import replace
import json
import pkgutil

FARM = 'Renewable Rosaries'
DATA = json.loads(pkgutil.get_data(__package__, 'enemy_drops.json'))
SHOPS = json.loads(pkgutil.get_data(__package__, 'rosary_shops.json'))
PAYMENTS = json.loads(pkgutil.get_data(__package__, 'rosary_payments.json'))


def enabled(world):
    return bool(world.options.enemy_souls or world.options.ledgegrab_ability_rando
                or world.options.entrance_randomization)


@contextmanager
def entrance_memo(world):
    if not enabled(world) or not world.options.entrance_randomization:
        yield
        return
    from .requirement_rules import _enable_native_source_memo, _invalidate_native_source_player
    previous = getattr(world.multiworld, '_silksong_native_source_memo', None)
    _enable_native_source_memo(world.multiworld, frozenset((world.player,)))
    try:
        yield
    finally:
        world.multiworld._silksong_native_source_memo = previous
        _invalidate_native_source_player(world.multiworld, world.player)


def gate(world, rules, location=None, anchor=None):
    from .silk_economy import source_node
    result = []
    prices = world.get_purchase_prices() if enabled(world) else {}
    for rule in rules:
        node = source_node(rule) or anchor
        if enabled(world) and location in PAYMENTS:
            rule = replace(rule, rosary_prices=tuple(PAYMENTS[location]))
        if enabled(world) and location in SHOPS:
            rows = [row for row in SHOPS[location] if row['node'] == node]
            if not rows:
                from .npc_souls import CATALOGUE
                events = {event for npc in CATALOGUE for event in npc.get('alternatives', {}).get(location, ())}
                if node is not None or not (events & PAYMENTS.keys() & set(rule.all_of)):
                    raise ValueError('Shop purchase position needs a currency binding: ' + location + ' / ' + str(node))
            else:
                keys = {key for row in rows for key in row['prices']}
                rule = replace(rule, rosary_prices=(min(keys,key=lambda k:prices[k]),) if keys else ())
        paid = enabled(world) and any(
            int(key.split(':', 1)[1]) > 0 if key.startswith('fixed:') else prices[key] > 0
            for key in rule.rosary_prices)
        if paid and node is None:
            raise ValueError('Rosary payment has no physical source: ' + repr(rule))
        result.append(replace(rule, rosary_prices=(),
            all_of=tuple(dict.fromkeys((*rule.all_of, *((FARM,) if paid else ()))))))
    return tuple(result)


def prepare(world, graph):
    from .requirements import REQUIREMENTS
    if not enabled(world):
        return graph
    graph = {name: gate(world, rules, name) for name, rules in graph.items()}
    overrides = world._progression_location_rules
    for name, original in REQUIREMENTS.items():
        rules = overrides.get(name, original)
        updated = gate(world, rules, name)
        if updated != rules:
            overrides[name] = updated
    graph[FARM] = farm_requirements(world, graph)
    return graph


def export_world(world, slot_data):
    if not enabled(world):
        return
    from .requirements import _export_requirement_group
    from .entrance_randomization import node_overrides
    from .silk_economy import gate_location
    graph = dict(world._silksong_native_abstract_requirements)
    disconnected = node_overrides(world) or {}
    for node, rules in (node_overrides(world, connected=True) or {}).items():
        added = tuple(rule for rule in rules if rule not in disconnected[node])
        graph[node] = tuple(dict.fromkeys((*graph[node], *gate(world, gate_location(world,added)))))
    for name, rules in graph.items():
        if name.startswith('Silk '):
            continue
        slot_data['abstract_requirements'].setdefault(name, {}).update(_export_requirement_group(rules))
    for name,rules in world._progression_location_rules.items():
        slot_data['requirements'][name] = _export_requirement_group(rules)


def farm_requirements(world, graph):
    from .room_graph import load_room_graph, RequirementSpec, RequirementMode
    from .room_graph_logic import _compile_spec
    from .requirements import _compiled_room_clause_requirement, NON_ARCHITECT_CREST_ITEMS
    from .enemy_souls import enabled_enemies, _combat_gate
    from .silk_economy import gate_location

    if DATA['mapper_source'] != load_room_graph().source_aggregate_sha256:
        raise ValueError('Enemy currency data needs a mapper refresh.')
    names = frozenset(enabled_enemies(world))
    rules = []
    for source in DATA['enemies'].values():
        if (not source.get('farm') or source.get('drops') not in ('rosaries', 'both')
                or source.get('reset') not in ('rest', 'scene')):
            continue
        node = 'Room Node: ' + source['node']
        if node not in graph:
            continue
        for route in source['routes']:
            if route['act'] > int(world.get_content_scope()[-1]):
                continue
            dnf = tuple(tuple(c) for c in route['dnf'])
            spec = RequirementSpec('', RequirementMode.EXPRESSION, dnf, (), (), 0)
            for clause in _compile_spec(spec, node):
                rule = _compiled_room_clause_requirement(clause)
                extra = [*route['events'], *(('Act: ' + str(route['act']),) if route['act'] > 1 else ())]
                extra.extend('Soul of ' + n for n in (source['species'], *route['souls']) if n in names)
                rule = replace(rule, all_of=tuple(dict.fromkeys((*rule.all_of, *extra))))
                rules.extend(_combat_gate(replace(rule, all_of=(*rule.all_of, crest)), names)
                             for crest in sorted(NON_ARCHITECT_CREST_ITEMS))
    return gate_location(world, tuple(dict.fromkeys(rules)))
