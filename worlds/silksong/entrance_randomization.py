from __future__ import annotations

import json
import pkgutil
from functools import lru_cache
from dataclasses import replace

from BaseClasses import CollectionState, Region
from Options import OptionError
from entrance_rando import EntranceRandomizationError, disconnect_entrance_for_randomization, randomize_entrances

from .room_graph import load_room_graph
from .room_graph_logic import compile_room_graph, compile_transition_requirements, room_node_name, CompiledRoomClause, _append_requirements

OPPOSITE_GROUP = {'left': 'right', 'right': 'left', 'top': 'bot', 'bot': 'top',
                  'door_in': 'door_out', 'door_out': 'door_in'}

POOL = {entry['id']: entry for entry in json.loads(pkgutil.get_data(__package__, 'entrance_pool.json'))}

WARP_DESTINATIONS = {
    'bone_bottom': ('Bone Bottom', 'bone-bottom/bone-bottom-bellway#room'),
    'bellhart': ('Bellhart', 'bellhart/belltown#lower-area'),
    'songclave': ('Songclave', 'choral-chambers/bellshrine-enclave#room'),
    'slab': ('The Slab', 'the-slab/slab-cell#upper'),
}


ACT_ONE_AREAS = frozenset({
    'moss-grotto', 'bone-bottom', 'the-marrow', 'weavenest-atla', 'wormways',
    'deep-docks', 'far-fields', 'hunter-s-march', 'shellwood', 'bellhart',
    'greymoor', 'wisp-thicket', 'blasted-steps', 'sinner-s-road', 'bilewater',
    'sands-of-karak',
})
ACT_TWO_AREAS = frozenset({
    'grand-gate', 'underworks', 'choral-chambers', 'cogwork-core',
    'whispering-vaults', 'whiteward', 'high-halls', 'memorium', 'the-slab',
    'mount-fay', 'putrified-ducts', 'the-cradle',
})
ACT_THREE_ROOMS = frozenset({
    'deep-docks/deep-docks-magma-slug-tunnels',
    'deep-docks/deep-docks-diving-bell-room',
    'far-fields/far-fields-deep-entrance',
    'far-fields/far-fields-deep-bench',
    'far-fields/hunters-march-pilgrims-rest-deep-passage',
    'far-fields/far-fields-deep-lower-west',
    'far-fields/far-fields-deep-lower-east',
    'far-fields/far-fields-deep-fort-passage',
    'far-fields/far-fields-deep-fort',
    'far-fields/current-karmelita',
    'far-fields/sprintmaster-cave',
    'grand-gate/shrine-guardian-seth',
    'grand-gate/nyleth-shrine',
    'sands-of-karak/watcher-at-the-edge',
    'cogwork-core/cogwork-core-architect-s-melody-act-3',
    'the-cradle/act3-connection-to-gms',
    'the-cradle/act3-gms-arena',
    'the-cradle/act3-lace2-arena',
    'the-cradle/cradle-path-of-pain-first-room',
    'the-cradle/path-of-pain-bench',
    'the-cradle/path-of-pain-silksong',
    'the-cradle/the-surface',
})


def room_act(source):
    if source.split('@', 1)[0] in ACT_THREE_ROOMS:
        return 3
    return 1 if area(source) in ACT_ONE_AREAS else 2 if area(source) in ACT_TWO_AREAS else 3


def enabled(world):
    return bool(world.options.entrance_randomization)


def scope(world):
    option = getattr(world.options, 'entrance_randomization_scope', None)
    return option.current_key if option is not None else 'full'


def area(source):
    return source.split('/', 1)[0]


def pairing_group(source, scope_name):
    data = POOL[source]
    # Memory entrances must keep their native entry and death-return setup.
    return (area(source) if scope_name == 'within_areas' else '',
            data.get('shuffle_region', ''), data['group'])


@lru_cache(maxsize=9)
def scoped_pool(scope_name, content_scope='act_3'):
    if scope_name not in {'full', 'interiors', 'within_areas'}:
        raise OptionError('Unknown entrance randomization scope.')
    if content_scope not in {'act_1', 'act_2', 'act_3'}:
        raise OptionError('Unknown entrance randomization content scope.')
    act = int(content_scope[-1])
    return {
        source: data for source, data in POOL.items()
        if max(room_act(source), room_act(data['vanilla'])) <= act
        and (scope_name == 'full'
            or scope_name == 'interiors' and data['group'] in {'door_in', 'door_out'}
            or scope_name == 'within_areas' and area(source) == area(data['vanilla']))
    }


def validate_pairs(pairs, scope_name='full', content_scope='act_3'):
    if not isinstance(pairs, dict) or not pairs or not set(pairs) <= set(scoped_pool(scope_name, content_scope)):
        raise OptionError('Entrance beta slot data does not match the verified transition pool.')
    for source, target in pairs.items():
        if (POOL[source]['vanilla'] not in pairs
                or not isinstance(target, str) or target not in pairs or pairs.get(target) != source
                or OPPOSITE_GROUP.get(POOL[source]['group']) != POOL[target]['group']
                or POOL[source].get('shuffle_region', '') != POOL[target].get('shuffle_region', '')
                or scope_name == 'within_areas' and area(source) != area(target)):
            raise OptionError('Entrance beta requires reciprocal, direction-compatible pairs.')
    return dict(pairs)


def members(data):
    return tuple(data.get('members', (data['id'],)))


def endpoint_name(data, ports):
    if data.get('arrival_requires'):
        return f"Entrance landing: {data['name']}"
    return room_node_name(ports[data['id']].source_node_id)


def exit_clauses(data, ports, include_source=True, silk_costs=False):
    if not data.get('arrival_requires'):
        return compile_transition_requirements(ports[data['id']], include_source=include_source, silk_costs=silk_costs)
    clauses = (compile_transition_requirements(ports[data['return_requires']], include_source=False, silk_costs=silk_costs)
               if data.get('return_requires') else (CompiledRoomClause(),))
    if include_source:
        return tuple(replace(clause, all_of=(endpoint_name(data, ports), *clause.all_of)) for clause in clauses)
    return clauses


def _validate_pool(ports):
    gates = {}
    claimed = set()
    for source, data in POOL.items():
        partner = POOL.get(data['vanilla'])
        port = ports.get(source)
        group_members = members(data)
        if (port is None or partner is None or partner['vanilla'] != source
                or OPPOSITE_GROUP.get(data['group']) != partner['group']
                or data.get('shuffle_region', '') != partner.get('shuffle_region', '')
                or source not in group_members or len(set(group_members)) != len(group_members)
                or claimed.intersection(group_members)):
            raise OptionError(f'Entrance beta audit is out of date: {source}')
        claimed.update(group_members)
        expected = compile_transition_requirements(port, include_source=False)
        for member in group_members:
            candidate = ports.get(member)
            if (candidate is None or not candidate.is_compilable or not candidate.requirement.dnf
                    or candidate.source_node_id != port.source_node_id
                    or candidate.target.port_id not in members(partner)
                    or compile_transition_requirements(candidate, include_source=False) != expected):
                raise OptionError(f'Entrance beta group has incompatible logic: {source}')
        arrival = data.get('arrival_requires')
        if arrival and (arrival not in group_members or not ports[arrival].requirement.dnf):
            raise OptionError(f'Entrance beta has an invalid arrival requirement: {source}')
        returning = data.get('return_requires')
        if returning and (not arrival or returning not in group_members):
            raise OptionError(f'Entrance beta has an invalid return requirement: {source}')
        rows = ({'port': source, **data}, *data.get('aliases', ()))
        if {row['port'] for row in rows} != set(group_members):
            raise OptionError(f'Entrance beta group is missing a native gate: {source}')
        for row in rows:
            key = (data['scene'], row['gate'])
            if key in gates:
                raise OptionError(f'Entrance beta has duplicate native gates: {source}')
            gates[key] = (source, row)
    for source, row in gates.values():
        target = gates.get((row['target_scene'], row['target_gate']))
        if target is None or target[0] != POOL[source]['vanilla']:
            raise OptionError(f'Entrance beta native destination is inconsistent: {source}')


@lru_cache(maxsize=8)
def _base_node_overrides(scope_name, content_scope, enemy_species, silk):
    from .enemy_souls import pogo_graph
    graph = pogo_graph(enemy_species) if enemy_species else load_room_graph()
    ports = graph.transition_by_id
    _validate_pool(ports)
    selected = scoped_pool(scope_name, content_scope)
    removed = {member: None for data in selected.values() for member in members(data)}
    compiled = compile_room_graph(graph, transition_targets=removed, silk_costs=silk)
    affected = {room_node_name(ports[member].source_node_id) for member in removed}
    clauses = {name: list(compiled.node_requirements[name]) for name in affected}
    for data in selected.values():
        if data.get('arrival_requires'):
            landing = endpoint_name(data, ports)
            clauses[landing] = list(compile_transition_requirements(ports[data['id']], silk_costs=silk))
            interior = room_node_name(ports[data['id']].source_node_id)
            clauses[interior].extend(
                replace(clause, all_of=(landing, *clause.all_of))
                for clause in compile_transition_requirements(ports[data['arrival_requires']], include_source=False, silk_costs=silk)
            )
    return {name: tuple(alternatives) for name, alternatives in clauses.items()}


@lru_cache(maxsize=8)
def _node_overrides(pairs, scope_name='full', content_scope='act_3', enemy_species=(), silk=False):
    from .requirements import _compiled_room_clause_requirement
    from .enemy_souls import pogo_graph

    clauses = {name: list(rules) for name, rules in
               _base_node_overrides(scope_name, content_scope, enemy_species, silk).items()}
    if pairs:
        graph = pogo_graph(enemy_species) if enemy_species else load_room_graph()
        ports = graph.transition_by_id
        selected = scoped_pool(scope_name, content_scope)
        destinations = dict(pairs)
        for source, data in selected.items():
            target = POOL[destinations.get(source, data['vanilla'])]
            requirements = exit_clauses(data, ports, silk_costs=silk)
            _append_requirements(clauses, endpoint_name(target, ports), requirements)
    result = {
        name: tuple(dict.fromkeys(_compiled_room_clause_requirement(clause) for clause in alternatives))
        for name, alternatives in clauses.items()
    }
    return result


def node_overrides(world, connected=False):
    if not enabled(world):
        return None
    pairs = getattr(world, '_entrance_pairs', None) if connected else None
    if connected and pairs is None:
        raise OptionError('Entrance layout has not been generated.')
    from .enemy_souls import enabled_enemies
    from .silk_economy import enabled as silk_enabled
    return _node_overrides(tuple(sorted(pairs.items())) if pairs else (), scope(world), world.get_content_scope(), enabled_enemies(world), silk_enabled(world))


def _disconnect(entrance):
    if entrance.connected_region is not None:
        entrance.connected_region.entrances.remove(entrance)
        entrance.connected_region = None


def _early_sweep_locations(world):
    locations = world.multiworld.get_filled_locations()
    if any(location.player != world.player and location.item.player == world.player for location in locations):
        return locations
    return [location for location in locations if location.player == world.player]


def _early_item_assignment(world):
    state = CollectionState(world.multiworld)
    state.sweep_for_advancements(locations=(
        location for location in _early_sweep_locations(world)
        if location.address is None or location in getattr(world, '_soul_opening_locations', ())
    ))
    pending = dict(world.multiworld.local_early_items[world.player])
    items = []
    for item in world.multiworld.itempool:
        if item.player == world.player and pending.get(item.name, 0) > 0:
            items.append(item)
            pending[item.name] -= 1
    locations = [location for location in world.get_locations()
                 if location.item is None and location.can_reach(state)]
    assigned = {}

    def place(index, visited):
        for location in locations:
            if location in visited or not location.can_fill(state, items[index], check_access=False):
                continue
            visited.add(location)
            if location not in assigned or place(assigned[location], visited):
                assigned[location] = index
                return True
        return False

    fits = all(place(index, set()) for index in range(len(items)))
    return state, items, assigned, fits


def _has_early_item_space(world):
    state, items, assigned, fits = _early_item_assignment(world)
    if not fits:
        return False
    for item in items:
        state.collect(item, True)
    state.sweep_for_advancements(_early_sweep_locations(world))
    if world.multiworld.completion_condition[world.player](state):
        return True
    pending = [item for item in world.multiworld.itempool
               if item.player == world.player and item.advancement and item not in items]
    remaining = [location for location in world.get_locations()
                 if location.item is None and location not in assigned]
    reachable = [location for location in remaining if location.can_reach(state)
                 and any(location.can_fill(state, item, check_access=False) for item in pending)]
    if len(reachable) != 1 or world.multiworld.players != 1:
        return bool(reachable)
    # One spare check isn't enough if the next route needs two new items.
    target = reachable[0]
    seen = set()
    for item in pending:
        if item.name in seen or not target.can_fill(state, item, check_access=False):
            continue
        seen.add(item.name)
        trial = state.copy()
        trial.collect(item, True)
        trial.sweep_for_advancements(_early_sweep_locations(world))
        if (world.multiworld.completion_condition[world.player](trial)
                or any(location is not target and location.can_reach(trial)
                       and any(location.can_fill(trial, next_item, check_access=False)
                               for next_item in pending if next_item is not item)
                       for location in remaining)):
            return True
    return False


def _has_possible_category_progression(world):
    from collections import defaultdict
    from .category_fill import _placement_category

    multiworld = world.multiworld
    state = CollectionState(multiworld)
    pending = defaultdict(list)
    for item in multiworld.itempool:
        category = _placement_category(item)
        if item.player == world.player and category:
            pending[category].append(item)
        else:
            state.collect(item, True)
    for location in multiworld.get_filled_locations():
        if location.item.code is not None and (
                location.player != world.player or location.item.player != world.player):
            state.collect(location.item, True)
    locations = defaultdict(list)
    for location in world.get_locations():
        category = _placement_category(location)
        if location.item is None and category:
            locations[category].append(location)
    changed = True
    while changed:
        state.sweep_for_advancements(world.get_locations())
        changed = False
        for category, items in tuple(pending.items()):
            if any(location.can_reach(state) and any(
                    location.can_fill(state, item, check_access=False) for item in items)
                    for location in locations[category]):
                for item in items:
                    state.collect(item, True)
                del pending[category]
                changed = True
    return (not pending and multiworld.has_beaten_game(state, world.player)
            and _has_possible_category_order(world, 'BellShrine')
            and _has_possible_category_order(world, 'Melody'))


def _has_possible_category_order(world, category):
    from .category_fill import _placement_category

    multiworld = world.multiworld
    items = [item for item in multiworld.itempool
             if item.player == world.player and _placement_category(item) == category]
    if not items:
        return True
    locations = [location for location in world.get_locations()
                 if location.item is None and _placement_category(location) == category]
    state = CollectionState(multiworld)
    for item in multiworld.itempool:
        if item not in items:
            state.collect(item, True)
    for location in multiworld.get_filled_locations():
        if location.item.code is not None and (
                location.player != world.player or location.item.player != world.player):
            state.collect(location.item, True)
    pending_states = [(state, tuple(range(len(items))), tuple(range(len(locations))))]
    visited = set()
    while pending_states:
        state, pending, slots = pending_states.pop()
        key = pending, slots
        if key in visited:
            continue
        visited.add(key)
        if len(visited) > 128:
            return False
        state.sweep_for_advancements(world.get_locations())
        if not pending:
            return True
        for location_index in slots:
            location = locations[location_index]
            if not location.can_reach(state):
                continue
            for item_index in pending:
                if _placement_category(items[item_index]) != _placement_category(location):
                    continue
                if not location.can_fill(state, items[item_index], check_access=False):
                    continue
                trial = state.copy()
                trial.collect(items[item_index], True)
                pending_states.append((
                    trial,
                    tuple(index for index in pending if index != item_index),
                    tuple(index for index in slots if index != location_index),
                ))
    return False


def _refresh_silk_connections(placement, exits, entrances):
    state = placement.collection_state
    player = placement.world.player
    added = {edge for entrance in exits for edge in getattr(entrance, '_silk_edges', ())
             if edge.parent_region in state.reachable_regions[player]
             and edge.connected_region not in state.reachable_regions[player]}
    state.blocked_connections[player].update(added)
    return bool(added)


def _randomize_group(world, exits):
    destinations = {entrance: entrance.connected_region for entrance in exits.values()}
    incoming = {entrance.parent_region: list(entrance.parent_region.entrances) for entrance in exits.values()}
    groups = {group: [(*group[:-1], OPPOSITE_GROUP[group[-1]])]
              for source in exits for group in (pairing_group(source, scope(world)),)}
    for attempt in range(10):
        for entrance in exits.values():
            disconnect_entrance_for_randomization(entrance)
        try:
            native_items = tuple(
                location.item for location in world.get_locations()
                if location.item is not None and location.item.code is not None
                and location.item.advancement and location.item.player == world.player
            ) if attempt else ()
            world._entrance_construction_items = native_items
            try:
                result = randomize_entrances(world, coupled=True, target_group_lookup=groups,
                                             exits=list(exits.values()), on_connect=_refresh_silk_connections)
            finally:
                world._entrance_construction_items = ()
            if native_items and not _has_reachable_exits(world, exits):
                raise EntranceRandomizationError('Entrance layout blocks native-item progression.')
            if scope(world) != 'within_areas' and not _has_early_item_space(world):
                raise EntranceRandomizationError('Entrance layout has insufficient checks for local early items.')
            if scope(world) != 'within_areas' and not _has_possible_category_progression(world):
                raise EntranceRandomizationError('Entrance layout blocks category progression.')
            return result
        except EntranceRandomizationError as error:
            for region, entrances in incoming.items():
                region.entrances[:] = entrances
            for entrance, destination in destinations.items():
                entrance.connected_region = destination
            world.multiworld.state.stale[world.player] = True
            if attempt == 9:
                raise OptionError('Entrance beta could not find a valid coupled layout after ten attempts. '
                                  'Generate with a different seed.') from error


def _has_reachable_exits(world, exits):
    state = world.multiworld.get_all_state(perform_sweep=False)
    state.sweep_for_advancements(world.get_locations())
    return all(entrance.can_reach(state) for entrance in exits.values())


def _randomize_exits(world, exits):
    if scope(world) != 'within_areas':
        return _randomize_group(world, exits).pairings
    destinations = {entrance: entrance.connected_region for entrance in exits.values()}
    incoming = {entrance.parent_region: list(entrance.parent_region.entrances) for entrance in exits.values()}
    area_names = sorted({area(source) for source in exits})
    for attempt in range(10):
        if attempt:
            world.random.shuffle(area_names)
        pairings = []
        try:
            for area_name in area_names:
                selected = {source: entrance for source, entrance in exits.items() if area(source) == area_name}
                pairings.extend(_randomize_group(world, selected).pairings)
            if (not _has_early_item_space(world) or not _has_possible_category_progression(world)
                    or not _has_reachable_exits(world, exits)):
                raise OptionError('Entrance layout blocks category progression.')
            return pairings
        except OptionError:
            for region, entrances in incoming.items():
                region.entrances[:] = entrances
            for entrance, destination in destinations.items():
                entrance.connected_region = destination
            world.multiworld.state.stale[world.player] = True
            if attempt == 9:
                raise


def _with_entrance_candidates(world, exits, predicate):
    destinations = {entrance: entrance.connected_region for entrance in exits.values()}
    incoming = {entrance.parent_region: list(entrance.parent_region.entrances) for entrance in exits.values()}
    groups = {}
    for source, entrance in exits.items():
        key = pairing_group(source, scope(world))
        groups.setdefault(key, []).append(entrance)
    portals = []
    try:
        for key, entrances in groups.items():
            target_key = (*key[:-1], OPPOSITE_GROUP[key[-1]])
            portal = Region(f'Entrance candidates: {key}', world.player, world.multiworld)
            portals.append(portal)
            for region in dict.fromkeys(entrance.parent_region for entrance in groups[target_key]):
                portal.connect(region)
            for entrance in entrances:
                _disconnect(entrance)
                entrance.connect(portal)
        return predicate()
    finally:
        for portal in portals:
            for entrance in portal.exits:
                _disconnect(entrance)
            portal.exits.clear()
        for region, entrances in incoming.items():
            region.entrances[:] = entrances
        for entrance, destination in destinations.items():
            entrance.connected_region = destination
        world.multiworld.state.stale[world.player] = True


def _validate_fixed_start(world, exits):
    state, items, assigned, fits = _early_item_assignment(world)
    if any(entrance.can_reach(state) for entrance in exits.values()):
        return
    if not fits:
        names = ', '.join(sorted({item.name for item in items}))
        raise OptionError(
            f'The fixed starting area has too few eligible checks for local early items: {names}. '
            'No shuffled entrance is reachable from this start, so entrance rerolls cannot help. '
            'Change the starting abilities, starting location, or early-item settings.'
        )
    if world.multiworld.players != 1:
        return
    for item in items:
        state.collect(item, True)
    state.sweep_for_advancements(world.get_locations())
    if (not world.multiworld.has_beaten_game(state, world.player)
            and not any(entrance.can_reach(state) for entrance in exits.values())
            and not any(location.item is None and location not in assigned and location.can_reach(state)
                        for location in world.get_locations())):
        raise OptionError(
            'The local early items use every starting check without opening a route forward. '
            'No shuffled entrance is reachable, so entrance rerolls cannot help. '
            'Change the starting abilities, starting location, or early-item settings.'
        )


def _sufficient_shuffle(world, pairs):
    groups = {}
    for source in pairs:
        groups.setdefault(pairing_group(source, scope(world)), []).append(source)
    movable = [source for group in groups.values() if len(group) > 1 for source in group]
    changed = sum(pairs[source] != POOL[source]['vanilla'] for source in movable)
    minimum = 50 if scope(world) == 'within_areas' else 80
    return 100 * changed >= minimum * len(movable)


def _repair_entrance_layout(world, exits):
    pairs = {source: POOL[source]['vanilla'] for source in exits}
    original_destinations = {entrance: entrance.connected_region for entrance in exits.values()}
    original_incoming = {entrance.parent_region: list(entrance.parent_region.entrances) for entrance in exits.values()}
    completed = False

    def connect(changes):
        for source, target in changes.items():
            _disconnect(exits[source])
            exits[source].connect(exits[target].parent_region)

    def valid():
        return (_has_early_item_space(world) and _has_possible_category_progression(world)
                and _has_reachable_exits(world, exits))

    def swap(first, second):
        changes = {first: pairs[second], second: pairs[first], pairs[first]: second, pairs[second]: first}
        connect(changes)
        if valid():
            pairs.update(changes)
            return True
        connect({source: pairs[source] for source in changes})
        return False

    groups = {}
    for source in exits:
        groups.setdefault(pairing_group(source, scope(world)), []).append(source)
    try:
        connect(pairs)
        if not valid():
            state = CollectionState(world.multiworld)
            state.sweep_for_advancements()
            starts = [source for source, entrance in exits.items() if entrance.can_reach(state)]
            world.random.shuffle(starts)
            found = False
            for first in starts:
                candidates = [source for source in groups[pairing_group(first, scope(world))] if source != first]
                world.random.shuffle(candidates)
                if any(swap(first, second) for second in candidates):
                    found = True
                    break
            if not found:
                return None
        sources = [source for key, group in groups.items() if key[-1] in {'left', 'top', 'door_in'}
                   and len(group) > 1 for source in group]
        for _ in range(4):
            world.random.shuffle(sources)
            for first in sources:
                if pairs[first] != POOL[first]['vanilla']:
                    continue
                candidates = [source for source in groups[pairing_group(first, scope(world))] if source != first]
                world.random.shuffle(candidates)
                for second in candidates[:8]:
                    if swap(first, second):
                        break
            if _sufficient_shuffle(world, pairs):
                validate_pairs(pairs, scope(world), world.get_content_scope())
                completed = True
                return [(exits[source].name, exits[target].name) for source, target in pairs.items()]
        return None
    finally:
        if not completed:
            for region, entrances in original_incoming.items():
                region.entrances[:] = entrances
            for entrance, destination in original_destinations.items():
                entrance.connected_region = destination
        world.multiworld.state.stale[world.player] = True


def connect_exits(world):
    passthrough = getattr(world.multiworld, 're_gen_passthrough', {}).get(world.game)
    if not enabled(world):
        if passthrough is None:
            _validate_fixed_start(world, {})
        return
    all_exits = world._entrance_exits
    restored = (passthrough or {}).get('entrance_pairs')
    deferred = getattr(world.multiworld, 'enforce_deferred_connections', 'off') != 'off'
    if restored is not None:
        pairs = validate_pairs(restored, scope(world), world.get_content_scope())
        exits = {source: all_exits[source] for source in pairs}
        for source, entrance in exits.items():
            _disconnect(entrance)
            if not deferred:
                entrance.connect(exits[pairs[source]].parent_region)
    else:
        from .category_fill import _placement_category

        all_state = world.multiworld.get_all_state()
        blocked = sorted(location.name for location in world.get_locations()
                         if _placement_category(location) and not location.can_reach(all_state))
        if blocked:
            raise OptionError(
                'The current room logic cannot reach these shuffled checks even with all available items: '
                + ', '.join(blocked)
                + '. Entrance randomization cannot repair checks outside its reachable transition pool.'
            )
        reachable = {source for source, entrance in all_exits.items() if entrance.can_reach(all_state)}
        exits = {source: entrance for source, entrance in all_exits.items()
                 if source in reachable and POOL[source]['vanilla'] in reachable}
        if not exits:
            raise OptionError('No verified entrance pairs are reachable with these settings.')
        _validate_fixed_start(world, exits)
        if not world.multiworld.has_beaten_game(all_state, world.player):
            candidate_state = None

            def goal_is_possible():
                nonlocal candidate_state
                candidate_state = world.multiworld.get_all_state()
                return world.multiworld.has_beaten_game(candidate_state, world.player)

            if not _with_entrance_candidates(world, exits, goal_is_possible):
                from .wish_events import SILK_AND_SOUL_WISH_POINT_ITEM, SILK_AND_SOUL_WISH_HALF_POINT_ITEM
                from .options import get_silk_and_soul_points

                points = (candidate_state.count(SILK_AND_SOUL_WISH_POINT_ITEM, world.player)
                          + candidate_state.count(SILK_AND_SOUL_WISH_HALF_POINT_ITEM, world.player) // 2)
                required = get_silk_and_soul_points(world.options)
                if world.get_goal_key() == 'act_3' and points < required:
                    raise OptionError(
                        f'Silk and Soul requires {required} points, but only {points} are reachable with these settings '
                        'even with every compatible entrance destination available. Lower Silk and Soul points.'
                    )
                raise OptionError(
                    'The goal cannot be reached with these settings even with all available items and every '
                    'compatible entrance destination available. Entrance rerolls cannot fix this setup.'
                )
        try:
            result = _randomize_exits(world, exits)
        except OptionError:
            result = _repair_entrance_layout(world, exits)
            if result is None:
                raise OptionError('Entrance beta could not find a valid, sufficiently shuffled layout. '
                                  'Generate with a different seed.') from None
        by_name = {entrance.name: source for source, entrance in exits.items()}
        pairs = validate_pairs({by_name[source]: by_name[target] for source, target in result}, scope(world), world.get_content_scope())
        if deferred:
            for entrance in exits.values():
                _disconnect(entrance)
    world._entrance_exits = exits
    world._entrance_pairs = pairs
    world._entrance_deferred = deferred
    world.multiworld.state.stale[world.player] = True
    if not deferred:
        for source, target in sorted(pairs.items()):
            if pairs.get(target) == source:
                if source > target:
                    continue
                direction = 'both'
            else:
                direction = 'entrance'
            world.multiworld.spoiler.set_entrance(POOL[source]['name'], POOL[target]['name'], direction, world.player)


def reconnect_found(world, value):
    if not enabled(world) or not getattr(world, '_entrance_deferred', False) or not isinstance(value, dict):
        return
    for source, target in value.items():
        if not isinstance(source, str) or not isinstance(target, str):
            continue
        if source not in world._entrance_pairs or world._entrance_pairs[source] != target:
            continue
        for start, end in ((source, target), (target, source)):
            entrance = world._entrance_exits[start]
            if entrance.connected_region is None:
                entrance.connect(world._entrance_exits[end].parent_region)
    world.multiworld.state.stale[world.player] = True


def reconnect_warps(world, value):
    if (getattr(world.multiworld, 'enforce_deferred_connections', 'off') == 'off'
            or not isinstance(value, dict)):
        return
    entrances = getattr(world, '_unlocked_warp_entrances', {})
    menu = world.multiworld.get_region('Menu', world.player)
    from rule_builder.rules import True_
    for key, (label, node) in WARP_DESTINATIONS.items():
        entrance = entrances.get(key)
        if value.get(key) is True:
            destination = world.multiworld.get_region(room_node_name(node), world.player)
            if entrance is None:
                entrance = world.create_entrance(menu, destination, True_(), f'F4 Warp: {label}')
                entrances[key] = entrance
            elif entrance.connected_region is None:
                entrance.connect(destination)
        elif entrance is not None:
            _disconnect(entrance)
    world._unlocked_warp_entrances = entrances
    world.multiworld.state.stale[world.player] = True


def slot_entrances(world):
    if not enabled(world):
        return {'entrance_randomization': 'off', 'entrance_randomization_scope': scope(world)}
    pairs = validate_pairs(world._entrance_pairs, scope(world), world.get_content_scope())
    return {
        'entrance_randomization': 'coupled',
        'entrance_randomization_scope': scope(world),
        'entrance_pairs': pairs,
        'entrance_layout': {
            source: {
                'scene': data['scene'], 'gate': data['gate'],
                'group': data['group'], 'is_door': data['is_door'],
                'shuffle_region': data.get('shuffle_region', ''),
                'vanilla_scene': data['target_scene'], 'vanilla_gate': data['target_gate'],
                'target': pairs[source], 'target_scene': POOL[pairs[source]]['scene'],
                'target_gate': POOL[pairs[source]]['gate'],
                'aliases': [{'gate': alias['gate'], 'vanilla_scene': alias['target_scene'],
                             'vanilla_gate': alias['target_gate']} for alias in data.get('aliases', ())],
            }
            for source, data in POOL.items() if source in pairs
        },
    }


def _hint_path(path, names):
    route = []
    visited = set()
    while path is not None:
        if id(path) in visited:
            return None
        visited.add(id(path))
        name, path = path
        if name in names:
            route.append(names[name])
    route.reverse()
    if not route:
        return None
    return "Via " + ("... -> " if len(route) > 2 else "") + " -> ".join(route[-2:])


def extend_hints(world, hint_data):
    if not getattr(world, '_entrance_pairs', None) or getattr(world, '_entrance_deferred', False):
        return
    state = world.multiworld.get_all_state()
    names = {entrance.name: POOL[source]['name']
             for source, entrance in world._entrance_exits.items()}
    hints = hint_data.setdefault(world.player, {})
    for location in world.get_locations():
        if location.address is None or not location.parent_region.can_reach(state):
            continue
        path = _hint_path(state.path.get(location.parent_region), names)
        if path:
            hints[location.address] = path
