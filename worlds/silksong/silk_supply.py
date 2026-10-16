from __future__ import annotations

from collections import OrderedDict, defaultdict, deque
from dataclasses import dataclass, replace
from heapq import heappop, heappush

from rule_builder.rules import Rule
from worlds.AutoWorld import LogicMixin

from .requirements import req
from .silk_economy import MAX_SILK, at, capacity, clean, rule_cost, source_node


class _UnsupportedCondition(Exception):
    pass


class _SupplyState:
    def __init__(self, program):
        self.program = program
        self.revision = program.revision
        self.levels = [-1] * len(program.node_names)
        self.active = bytearray(len(program.conditions))
        self.pending = set(range(len(program.conditions)))
        self.queue = []
        self.entries = set()
        self.entry_nodes = set()
        self.refresh = True
        self.regeneration = 0
        self.capacity = 9


    def copy(self):
        result = _SupplyState.__new__(_SupplyState)
        result.program = self.program
        result.revision = self.revision
        result.levels = self.levels.copy()
        result.active = self.active.copy()
        result.pending = self.pending.copy()
        result.queue = self.queue.copy()
        result.entries = self.entries.copy()
        result.entry_nodes = self.entry_nodes.copy()
        result.refresh = self.refresh
        result.regeneration = self.regeneration
        result.capacity = self.capacity
        return result


def copy_silk_supply(state, target, player):
    cached = getattr(state, '_silksong_silk_supply', {}).get(player)
    if cached is None or cached.revision != cached.program.revision:
        return
    if not hasattr(target, '_silksong_silk_supply'):
        target._silksong_silk_supply = {}
    target._silksong_silk_supply[player] = cached.copy()


class SilkSupplyState(LogicMixin):
    def copy_mixin(self, new_state):
        for player in getattr(self, '_silksong_silk_supply', ()):
            copy_silk_supply(self, new_state, player)
        return new_state


class SilkSupply:

    def __init__(self, world, original):
        from .native_regions import native_rule_options
        from .requirement_rules import build_requirements_rule

        self.player = world.player
        nodes = world._silk_node_rules
        self.node_names = tuple(sorted(nodes))
        self.nodes = {name: i for i, name in enumerate(self.node_names)}
        self.queries = {at(name, amount): (i, amount)
                        for name, i in self.nodes.items() for amount in range(MAX_SILK + 1)}
        self.conditions = []
        condition_ids = {}
        self.item_conditions = defaultdict(set)
        self.region_conditions = defaultdict(set)
        self.actions = defaultdict(list)
        self.routes = [[] for _ in nodes]
        self.incoming = [[] for _ in nodes]
        self.source_conditions = [[] for _ in nodes]
        self.refill_conditions = {}
        self.refills = set()
        self._dependencies = {}
        self._solutions = OrderedDict()
        self.revision = 0
        self.exit_patterns = {}
        self.exit_edges = {}
        self.exit_incoming = defaultdict(list)
        self.exit_queries = set()
        options = native_rule_options(world)

        def resolve(rules):
            return build_requirements_rule(
                tuple(rules), extra_abstract_requirement_names=world._silksong_native_abstract_names,
                **options,
            ).resolve(world)

        def condition(rules):
            resolved = resolve(rules)
            if resolved.location_dependencies() or resolved.entrance_dependencies():
                raise _UnsupportedCondition()
            if resolved.always_false:
                return None
            if resolved not in condition_ids:
                index = len(self.conditions)
                condition_ids[resolved] = index
                self.conditions.append(resolved)
                for name in resolved.item_dependencies():
                    self.item_conditions[name].add(index)
                for name in resolved.region_dependencies():
                    self.region_conditions[name].add(index)
            return condition_ids[resolved]

        for node, index in self.nodes.items():
            refill = 'Silk refill: ' + node.removeprefix('Room Node: ')
            if original[refill]:
                self.refills.add(refill)
                predicate = condition((req(refill, crest=False),))
                if predicate is not None:
                    self.refill_conditions[index] = predicate
                    self.source_conditions[index].append(predicate)
                    self.actions[predicate].append(('refill', index))
            incoming = defaultdict(list)
            for rule in nodes[node]:
                source = source_node(rule)
                if source is None:
                    predicate = condition((clean(rule),))
                    if predicate is not None:
                        self.source_conditions[index].append(predicate)
                        self.actions[predicate].append(('seed', index))
                elif source in self.nodes:
                    incoming[source, rule_cost(rule)].append(replace(
                        clean(rule), all_of=tuple(n for n in clean(rule).all_of if n != source)))
            for (source, cost), rules in incoming.items():
                if cost > MAX_SILK:
                    continue
                predicate = condition(rules)
                if predicate is None:
                    continue
                edge = (self.nodes[source], index, cost, predicate)
                self.routes[edge[0]].append(edge)
                self.incoming[index].append(edge)
                self.actions[predicate].append(('route', edge))
        self._compile_exits(world, condition)
        self.capacity_rules = [resolve((capacity(amount),)) for amount in range(10, MAX_SILK + 1)]
        self.capacity_items = {name for rule in self.capacity_rules for name in rule.item_dependencies()}
        self.region_updates = {
            name: (self.region_conditions.get(name, ()), self.nodes.get(name))
            for name in self.region_conditions.keys() | self.nodes.keys()
        }
        self._compile_dependencies()
        for rule in (*self.conditions, *self.capacity_rules):
            world.register_rule_dependencies(rule)

    def _compile_exits(self, world, condition):
        from .scene_exits import shuffled_exits

        for exit in shuffled_exits(world):
            node, rules = exit.source, exit.transport_requirements
            grouped = defaultdict(list)
            for rule in rules:
                cost = rule_cost(rule)
                if cost <= MAX_SILK:
                    grouped[cost].append(clean(rule))
                    if cost:
                        self.exit_queries.add(at(node, cost))
            patterns = []
            for cost, alternatives in grouped.items():
                predicate = condition(alternatives)
                if predicate is not None:
                    patterns.append((self.nodes[node], cost, predicate))
            self.exit_patterns[exit.name] = tuple(patterns)

    def connect_exit(self, name, region):
        destinations = []
        if region is not None:
            destinations = ([region] if region.name in self.nodes else
                            [edge.connected_region for edge in region.exits if edge.connected_region is not None])
        edges = tuple((source, self.nodes[target.name], cost, predicate)
                      for source, cost, predicate in self.exit_patterns[name]
                      for target in destinations if target.name in self.nodes)
        previous = self.exit_edges.get(name, ())
        if previous == edges:
            return
        for edge in previous:
            self.routes[edge[0]].remove(edge)
            self.actions[edge[3]].remove(('route', edge))
            self.exit_incoming[edge[1]].remove(edge)
        for edge in edges:
            self.routes[edge[0]].append(edge)
            self.actions[edge[3]].append(('route', edge))
            self.exit_incoming[edge[1]].append(edge)
        self.exit_edges[name] = edges
        self.revision += 1
        self._solutions.clear()

    def exit_dependencies(self, name):
        query = self.queries.get(name)
        items, regions = set(), set()
        if query is not None:
            node, amount = query
            for source, _, cost, predicate in self.exit_incoming[node]:
                if amount + cost > MAX_SILK:
                    continue
                rule = self.conditions[predicate]
                items.update(rule.item_dependencies())
                regions.update(rule.region_dependencies())
                regions.add(at(self.node_names[source], amount + cost))
                if amount == 0:
                    regions.add(self.node_names[source])
        return items, regions

    def _compile_dependencies(self):
        if self.exit_patterns:
            items = frozenset(self.capacity_items | {'Progressive Silkheart'} | set(self.item_conditions))
            regions = frozenset(self.region_conditions)
            self._dependencies = {index: (items, regions) for index in range(len(self.node_names))}
            return
        dependencies = [(frozenset(rule.item_dependencies()), frozenset(rule.region_dependencies()))
                        for rule in self.conditions]
        atoms = sorted({('item', name) for items, regions in dependencies for name in items}
                       | {('region', name) for items, regions in dependencies for name in regions})
        indices = {atom: i for i, atom in enumerate(atoms)}
        conditions = [sum(1 << indices['item', name] for name in items)
                      | sum(1 << indices['region', name] for name in regions)
                      for items, regions in dependencies]
        bits = []
        for i in range(len(self.node_names)):
            value = 0
            for predicate in self.source_conditions[i]:
                value |= conditions[predicate]
            for source, target, cost, predicate in self.incoming[i]:
                value |= conditions[predicate]
            bits.append(value)
        pending = deque(range(len(bits)))
        queued = set(pending)
        while pending:
            source = pending.popleft()
            queued.remove(source)
            for _, target, cost, predicate in self.routes[source]:
                value = bits[target] | bits[source]
                if value != bits[target]:
                    bits[target] = value
                    if target not in queued:
                        queued.add(target)
                        pending.append(target)
        self.dependency_bits = bits
        self.dependency_atoms = atoms

    def dependencies(self, node):
        if node not in self._dependencies:
            items = self.capacity_items | {'Progressive Silkheart'}
            regions = set()
            bits = self.dependency_bits[node]
            while bits:
                flag = bits & -bits
                bits -= flag
                kind, name = self.dependency_atoms[flag.bit_length() - 1]
                (items if kind == 'item' else regions).add(name)
            self._dependencies[node] = frozenset(items), frozenset(regions)
        return self._dependencies[node]

    def _cached(self, state):
        try:
            cached = state._silksong_silk_supply[self.player]
        except (AttributeError, KeyError):
            return None
        return cached if cached.program is self and cached.revision == self.revision else None

    def collect(self, state, name):
        affected = self.item_conditions.get(name, ())
        refresh = name in self.capacity_items or name == 'Progressive Silkheart'
        if not affected and not refresh:
            return
        cached = self._cached(state)
        if cached is not None:
            cached.pending.update(p for p in affected if not cached.active[p])
            cached.refresh |= refresh

    def reached(self, state, region):
        update = self.region_updates.get(region.name)
        if update is None:
            return
        cached = self._cached(state)
        if cached is None:
            return
        affected, index = update
        if affected:
            cached.pending.update(p for p in affected if not cached.active[p])
        if index is not None and cached.levels[index] < 0:
            cached.entries.add(index)

    def evaluate(self, state, node, amount):
        if state.stale[self.player]:
            state.update_reachable_regions(self.player)
        cached = self._cached(state)
        if cached is None:
            cached = _SupplyState(self)
            cached.entries.update(self.nodes[r.name] for r in state.reachable_regions[self.player]
                                  if r.name in self.nodes)
            if not hasattr(state, '_silksong_silk_supply'):
                state._silksong_silk_supply = {}
            state._silksong_silk_supply[self.player] = cached
        levels, active, pending, queue = cached.levels, cached.active, cached.pending, cached.queue
        if levels[node] >= amount:
            return True
        if not pending and not cached.refresh and not queue and not cached.entries:
            return False

        def offer(index, value):
            if value >= 0:
                if value < cached.regeneration:
                    value = cached.regeneration
                refill = self.refill_conditions.get(index)
                if refill is not None and active[refill] and value < cached.capacity:
                    value = cached.capacity
                if value > levels[index]:
                    levels[index] = value
                    heappush(queue, (-value, index))

        if cached.refresh:
            cached.regeneration = min(3, state.count('Progressive Silkheart', self.player))
            cached.capacity = 9
            for capacity_rule in self.capacity_rules:
                if not capacity_rule(state):
                    break
                cached.capacity += 1
            cached.refresh = False
            for index, value in enumerate(levels):
                if value >= 0:
                    offer(index, value)
        for predicate in tuple(pending):
            pending.remove(predicate)
            if active[predicate] or not self.conditions[predicate](state):
                continue
            active[predicate] = 1
            for kind, argument in self.actions[predicate]:
                if kind == 'seed':
                    offer(argument, 0)
                elif kind == 'refill':
                    if levels[argument] >= 0:
                        offer(argument, cached.capacity)
                else:
                    source, target, cost, _ = argument
                    offer(target, levels[source] - cost)
        for index in cached.entries:
            offer(index, 0)
        cached.entry_nodes.update(cached.entries)
        cached.entries.clear()
        key = (bytes(active), cached.regeneration, cached.capacity, frozenset(cached.entry_nodes))
        solution = self._solutions.get(key)
        if solution is not None:
            self._solutions.move_to_end(key)
            levels[:] = solution
            queue.clear()
            return levels[node] >= amount
        while queue:
            negative, source = heappop(queue)
            value = -negative
            if value != levels[source]:
                continue
            for _, target, cost, predicate in self.routes[source]:
                if active[predicate]:
                    offer(target, value - cost)
        self._solutions[key] = tuple(levels)
        if len(self._solutions) > 512:
            self._solutions.popitem(last=False)
        return levels[node] >= amount


@dataclass
class SilkSupplyRule(Rule, game='Hollow Knight: Silksong'):
    name: str

    def _instantiate(self, world):
        program = world._silk_supply
        node, amount = program.queries[self.name]
        return self.Resolved(node, amount, program, player=world.player)

    class Resolved(Rule.Resolved):
        node: int
        amount: int
        program: object
        force_recalculate = True

        def _evaluate(self, state):
            if not state.stale[self.player]:
                try:
                    cached = state._silksong_silk_supply[self.player]
                except (AttributeError, KeyError):
                    return self.program.evaluate(state, self.node, self.amount)
                if cached.program is self.program and cached.revision == self.program.revision:
                    if cached.levels[self.node] >= self.amount:
                        return True
                    if not cached.pending and not cached.refresh and not cached.queue and not cached.entries:
                        return False
            return self.program.evaluate(state, self.node, self.amount)

        __call__ = _evaluate

        def item_dependencies(self):
            return {name: {id(self)} for name in self.program.dependencies(self.node)[0]}

        def region_dependencies(self):
            return {name: {id(self)} for name in self.program.dependencies(self.node)[1]}

        def explain_str(self, state=None):
            room = self.program.node_names[self.node].removeprefix('Room Node: ')
            return f'Reach {room}' + (f' with at least {self.amount} silk' if self.amount else '')

        def explain_json(self, state=None):
            color = 'yellow' if state is None else 'green' if self(state) else 'salmon'
            return [{'type': 'color', 'color': color, 'text': self.explain_str(state)}]

        def __str__(self):
            return self.explain_str()


def compile_regions(world, original):
    from .native_graph import compact_requirements
    from .silk_economy import enabled

    if getattr(world.multiworld, "generation_is_fake", False):
        return original
    if not enabled(world):
        return compact_requirements(world, original)
    try:
        supply = SilkSupply(world, original)
    except _UnsupportedCondition:
        return compact_requirements(world, original)
    graph = {name: rules for name, rules in original.items() if name not in supply.queries}
    result = compact_requirements(world, graph, additional_roots=supply.refills, silk_supply=True)
    from .scene_exits import fixed_exits
    roots = set(supply.nodes) | supply.exit_queries
    for rules in (*result.values(), *(exit.requirements for exit in fixed_exits(world)),
                  *world._progression_location_rules.values(),
                  *(original[name] for name in world._progression_events)):
        for rule in rules:
            roots.update(name for name in (*rule.all_of, *rule.any_of) if name.startswith('Silk ('))
    result.update((name, ()) for name in roots)
    supply.boundaries = frozenset(roots)
    world._enable_silk_supply(supply)
    world.explicit_indirect_conditions = False
    return result
