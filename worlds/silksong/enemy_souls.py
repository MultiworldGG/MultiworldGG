from __future__ import annotations

import json
import pkgutil
from dataclasses import replace
from functools import lru_cache

CATALOGUE = tuple(json.loads(pkgutil.get_data(__package__, 'enemy_souls.json')))
BY_NAME = {row['name']: row for row in CATALOGUE}
SCOPE_CATEGORIES = frozenset(category for row in CATALOGUE
                             for items in row.get('scope_items', {}).values()
                             for category in items.values())

from .silk_economy import enabled as silk_enabled
from .boss_souls import CATALOGUE as BOSS_CATALOGUE
from .combat import profiles, requirement_name
BOSS_COMBAT = frozenset(requirement_name(key) for key in profiles() if key.startswith('boss:')) | frozenset(
    name for row in BOSS_CATALOGUE for name in row['combat'])
BOSS_EVENTS = frozenset(name for row in BOSS_CATALOGUE for name in row['events'])


def item_name(name):
    return 'Enemy Soul: ' + name


def location_name(name):
    return 'First Kill: ' + name


def enabled_enemies(world):
    if not world.options.enemy_souls:
        return ()
    passthrough = getattr(world.multiworld, 're_gen_passthrough', {}).get(world.game)
    if passthrough is not None:
        validate_slot_data(passthrough)
        return tuple(passthrough.get('enemy_soul_species', ()))
    act = int(world.get_content_scope().removeprefix('act_'))
    anywhere = frozenset(category for category in SCOPE_CATEGORIES
                         if world.get_category_mode(category) == 'anywhere')
    return _scoped_enemies(act, anywhere)


@lru_cache(maxsize=16)
def _scoped_enemies(act, anywhere):
    return tuple(row['name'] for row in CATALOGUE
                 if any(route['act'] <= act for route in row['routes'])
                 and all(category in anywhere
                         for category in row.get('scope_items', {}).get(str(act), {}).values()))


def required_pool_items(world):
    scope = world.get_content_scope().removeprefix('act_')
    return tuple(dict.fromkeys(item for name in enabled_enemies(world)
                               for item in BY_NAME[name].get('scope_items', {}).get(scope, {})))


def validate_slot_data(data):
    names = data.get('enemy_soul_species', [])
    if (not isinstance(names, list) or any(not isinstance(n, str) for n in names)
            or len(set(names)) != len(names) or any(n not in BY_NAME for n in names)):
        raise ValueError('Unsupported Enemy Souls configuration.')
    if names and not data.get('enemy_souls', False):
        raise ValueError('Enemy Souls setting does not match its species.')
    if data.get('enemy_souls', False) and 'enemy_soul_species' not in data:
        raise ValueError('Enemy Souls configuration is missing.')


def check_requirements(name, enabled=None):
    from .requirements import req
    enabled = frozenset(BY_NAME if enabled is None else enabled)
    return tuple(req(item_name(name), *(('Act: ' + str(route['act']),) if route['act'] > 1 else ()),
                     *route.get('events', ()),
                     *(item_name(soul) for soul in route.get('souls', ()) if soul in enabled),
                     *('Room Node: ' + node for node in route['nodes']))
                 for route in BY_NAME[name]['routes'])


def add_souls_to_pool(world, entries):
    from .items import ItemPoolEntry
    entries.extend(ItemPoolEntry(item_name(name), 'EnemySoul') for name in enabled_enemies(world))


def create_locations(world, region):
    from .locations import SilksongLocation
    for name in enabled_enemies(world):
        region.locations.append(SilksongLocation(world.player, location_name(name), BY_NAME[name]['location_id'], region))


def set_rules(world):
    from .native_regions import native_rule_options
    from .requirement_rules import build_requirements_rule
    for name in enabled_enemies(world):
        location = world.multiworld.get_location(location_name(name), world.player)
        world.set_rule(location, build_requirements_rule(check_requirements(name, enabled_enemies(world)),
            extra_abstract_requirement_names=world._silksong_native_abstract_names, **native_rule_options(world)))


@lru_cache(maxsize=8)
def pogo_graph(names):
    from .room_graph import load_room_graph
    graph = load_room_graph()
    connections = {}
    for name in names:
        for connection in BY_NAME[name].get('connections', ()):
            connections.setdefault(connection, []).append('received:' + item_name(name))
    rooms = []
    for room in graph.rooms:
        souls = tuple('received:' + item_name(name) for name in names
                      if room.id in BY_NAME[name]['rooms']
                      and room.id not in BY_NAME[name].get('black_thread_only_rooms', ()))
        def update(row):
            spec = row.requirement
            dnf = []
            for branch in spec.dnf:
                needed = souls if any(atom.startswith('mapper:enemy-pogo:') for atom in branch) else ()
                needed += tuple(connections.get(row.id, ()))
                records = {atom.split(':')[2] for atom in branch if atom.startswith('mapper:enemy-type-pogo:')}
                if records:
                    needed += tuple('received:' + item_name(name) for name in names if BY_NAME[name]['record'] in records)
                if ('Skullwing' in names and room.id in BY_NAME['Skullwing']['rooms']
                        and any(atom == 'item:clawline' or atom.startswith('mapper:clawline:') for atom in branch)):
                    needed = (*needed, 'received:' + item_name('Skullwing'))
                dnf.append(tuple(dict.fromkeys((*branch, *needed))))
            dnf = tuple(dnf)
            return replace(row, requirement=replace(spec, dnf=dnf))
        rooms.append(replace(room, connections=tuple(map(update, room.connections)),
                             transitions=tuple(map(update, room.transitions)),
                             checks=tuple(map(update, room.checks)), events=tuple(map(update, room.events))))
    return replace(graph, rooms=tuple(rooms))


@lru_cache(maxsize=8)
def _pogo_changes(names, silk=False):
    from .room_graph_logic import compile_room_graph
    from .requirements import _compiled_room_clause_requirement, _SOURCE_COMPILED_ROOM_GRAPH
    before = _SOURCE_COMPILED_ROOM_GRAPH
    after = compile_room_graph(pogo_graph(names), silk_costs=silk)
    result = {}
    for field in ('node_requirements', 'event_requirements', 'check_requirements'):
        changes = {}
        old, new = getattr(before, field), getattr(after, field)
        for name, clauses in old.items():
            if clauses != new[name]:
                removed = tuple(_compiled_room_clause_requirement(c) for c in clauses if c not in new[name])
                added = tuple(_compiled_room_clause_requirement(c) for c in new[name] if c not in clauses)
                changes[name] = removed, added
        result[field] = changes
    return result


def node_overrides(world, overrides):
    from .requirements import ROOM_NODE_REQUIREMENTS
    names = enabled_enemies(world)
    if not names:
        return overrides
    result = dict(overrides or {})
    for name, (removed, added) in _pogo_changes(names, silk_enabled(world))['node_requirements'].items():
        if name in result:
            continue
        current = ROOM_NODE_REQUIREMENTS[name]
        if any(rule not in current for rule in removed):
            raise ValueError('Enemy Souls cannot resolve a changed pogo route: ' + name)
        result[name] = tuple(rule for rule in current if rule not in removed) + added
    return result


def gate_graph(world, graph):
    names = enabled_enemies(world)
    if not names:
        return graph
    result = dict(graph)
    for name, (removed, added) in _pogo_changes(names, silk_enabled(world))['event_requirements'].items():
        current = result[name]
        if any(rule not in current for rule in removed):
            from .silk_economy import clean
            if set(map(clean, added)) == set(removed):
                continue
            raise ValueError('Enemy Souls cannot resolve a changed pogo event: ' + name)
        result[name] = tuple(rule for rule in current if rule not in removed) + added
    from .room_graph import load_room_graph
    for room in load_room_graph().rooms:
        souls = tuple(item_name(name) for name in names if room.id in BY_NAME[name]['rooms'])
        for event in room.events:
            owner = 'Room Event: ' + event.id
            if souls and event.kind in {'enemy', 'miniboss', 'gauntlet'} and owner in result and owner not in BOSS_EVENTS:
                result[owner] = tuple(rule if BOSS_COMBAT.intersection(rule.all_of) else
                                      replace(rule, all_of=tuple(dict.fromkeys((*rule.all_of, *souls)))) for rule in result[owner])
    for name in names:
        for event in BY_NAME[name].get('events', ()):
            result[event] = tuple(replace(rule, all_of=tuple(dict.fromkeys((*rule.all_of, item_name(name)))))
                                  for rule in result[event])
    for combat, souls in _boss_summons(names).items():
        result[combat] = tuple(replace(rule, all_of=tuple(dict.fromkeys((*rule.all_of, *souls))))
                               for rule in result[combat])
    for owner, rules in tuple(result.items()):
        result[owner] = tuple(_combat_gate(rule, names) for rule in rules)
    return result


@lru_cache(maxsize=8)
def _boss_summons(names):
    def guards(row):
        return {('state', s['scene'], s['path'], s['fsm'], state)
                for s in row.get('states', ()) for state in s['states']} | {
                    ('battle', b['scene'], b['path']) for b in row.get('battles', ())}
    enemies = {name: guards(BY_NAME[name]) for name in names}
    result = {}
    for boss in BOSS_CATALOGUE:
        required = tuple(item_name(name) for name, guarded in enemies.items() if guards(boss) & guarded)
        if required:
            for combat in boss['combat']:
                result[combat] = required
    return result


def _combat_gate(rule, names):
    if BOSS_COMBAT.intersection(rule.all_of) or not any(token.startswith('Combat: ') for token in rule.all_of):
        return rule
    rooms = {token.removeprefix('Room Node: ').split('#')[0] for token in rule.all_of if token.startswith('Room Node: ')}
    souls = tuple(item_name(name) for name in names if rooms.intersection(BY_NAME[name]['rooms']))
    return replace(rule, all_of=tuple(dict.fromkeys((*rule.all_of, *souls))))


def _apply_pogo_changes(name, rules, removed, added):
    result = []
    matched = set()
    for rule in rules:
        replacements = []
        for old in removed:
            if (set(old.all_of).issubset(rule.all_of) and set(old.item_counts).issubset(rule.item_counts)
                    and replace(old, all_of=rule.all_of, item_counts=rule.item_counts) == rule):
                for new in added:
                    if replace(new, all_of=tuple(n for n in new.all_of if not n.startswith("Silk Cost: ")), item_counts=old.item_counts) == old:
                        replacements.append(replace(rule, all_of=tuple(dict.fromkeys((*rule.all_of, *new.all_of))), item_counts=tuple(dict.fromkeys((*rule.item_counts, *new.item_counts)))))
                        matched.add(old)
        result.extend(replacements or (rule,))
    unresolved = [old for old in removed if old not in matched and any(
        token.startswith('Technique: Enemy Pogo') and token in rule.all_of
        for token in old.all_of for rule in rules)]
    if unresolved:
        raise ValueError('Enemy Souls cannot resolve a changed pogo check: ' + name)
    return tuple(dict.fromkeys(result))


@lru_cache(maxsize=8)
def _pogo_check_changes(names, silk):
    from .locations import canonicalize_location_name
    result = {}
    for name, changes in _pogo_changes(names, silk)['check_requirements'].items():
        result.setdefault(canonicalize_location_name(name), []).append(changes)
    return {name: tuple(changes) for name, changes in result.items()}


@lru_cache(maxsize=8)
def _location_souls(names):
    from .locations import canonicalize_location_name
    result = {}
    for species in names:
        for name in BY_NAME[species].get('locations', ()):
            result.setdefault(canonicalize_location_name(name), []).append(item_name(species))
    return {name: tuple(dict.fromkeys(souls)) for name, souls in result.items()}


def gate_location(world, name, rules):
    names = enabled_enemies(world)
    if not names:
        return rules
    for removed, added in _pogo_check_changes(names, silk_enabled(world)).get(name, ()):
        rules = _apply_pogo_changes(name, rules, removed, added)
    souls = _location_souls(names).get(name, ())
    if souls:
        rules = tuple(replace(rule, all_of=tuple(dict.fromkeys((*rule.all_of, *souls)))) for rule in rules)
    if name == 'Marrowmaw - Beast Shard' and 'Marrowmaw' in names:
        rules = tuple(replace(rule, all_of=tuple(dict.fromkeys((*rule.all_of, item_name('Marrowmaw'))))) for rule in rules)
    return tuple(_combat_gate(rule, names) for rule in rules)


def location_overrides(world, rules):
    if not enabled_enemies(world):
        return rules
    from .requirements import REQUIREMENTS
    result = dict(rules)
    for name, requirements in REQUIREMENTS.items():
        original = result.get(name, requirements)
        gated = gate_location(world, name, original)
        if gated != original:
            result[name] = gated
    return result


def export_world(world, slot_data):
    from .requirements import _export_requirement_group
    names = enabled_enemies(world)
    slot_data['enemy_souls'] = bool(world.options.enemy_souls)
    slot_data['enemy_soul_species'] = list(names)
    if not names:
        return
    for name in names:
        slot_data['requirements'][location_name(name)] = _export_requirement_group(check_requirements(name, names))
    from .entrance_randomization import node_overrides as entrance_nodes
    connected_nodes = entrance_nodes(world, connected=True) or {}
    for name, rules in world._silksong_native_abstract_requirements.items():
        if name not in connected_nodes:
            slot_data['abstract_requirements'][name] = _export_requirement_group(rules)
