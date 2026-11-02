from __future__ import annotations

from dataclasses import dataclass
from itertools import chain, islice

from BaseClasses import CollectionState
from Fill import FillError, swap_location_item

from .requirements import (
    CRAFTMETAL_ITEM,
    CRAFTMETAL_PURCHASE_LOCATIONS,
    CREST_SLOT_LOCATION_NAMES,
    MEMORY_LOCKET_ITEM,
    RUINED_TOOL_REPAIR_LOCATIONS,
)


@dataclass
class SpendingFailure:
    state: CollectionState
    bought: int
    exhausted: bool = False


class SpendingAudit:
    state_limit = 4096
    swap_limit = 64

    def __init__(self, multiworld, worlds, *, finalized=True):
        self.multiworld = multiworld
        self.finalized = finalized
        self.worlds = {world.player: world for world in worlds}
        self.recipients = {player: {player} for player in self.worlds}
        self.recipients.update({group: data['players'] & self.worlds.keys()
                                for group, data in multiworld.groups.items()})
        self.locations = tuple(multiworld.get_filled_locations())
        self.purchases = tuple(sorted(
            (location for location in self.locations
             if location.player in self.worlds
             and location.name in CRAFTMETAL_PURCHASE_LOCATIONS),
            key=lambda location: (location.player, location.name),
        ))
        self.indices = {location: index for index, location in enumerate(self.purchases)}
        self.free = tuple(location for location in self.locations if location not in self.indices)
        self.free_by_player = {
            player: tuple(location for location in self.free if location.player == player)
            for player in self.worlds
        }
        self.foreign_free = tuple(location for location in self.free if location.player not in self.worlds)
        self.reach_cache = {}
        self.masks = {player: 0 for player in self.worlds}
        self.repairs = self.masks.copy()
        self.refunds = {
            player: world.get_category_mode('Tool') != 'vanilla'
            for player, world in self.worlds.items()
        }
        for index, location in enumerate(self.purchases):
            self.masks[location.player] |= 1 << index
            if location.name in RUINED_TOOL_REPAIR_LOCATIONS:
                self.repairs[location.player] |= 1 << index
        self.full = {player for player, world in multiworld.worlds.items()
                     if world.options.accessibility == 'full'}
        self.minimal = {player for player, world in multiworld.worlds.items()
                        if world.options.accessibility == 'minimal'}
        self.foreign_full = tuple(location for location in self.foreign_free if location.player in self.full)
        self.baseline_locations = set()
        self.baseline_purchases = (1 << len(self.purchases)) - 1
        self.goals = set()
        self.alternatives = {
            location for location in self.purchases
            if location.name in RUINED_TOOL_REPAIR_LOCATIONS
            and not self.refunds[location.player]
        }
        self.visited = {}
        self.states = 0
        self.run_states = 0

    def spent(self, player, bought):
        repairs = self.repairs[player]
        total = (bought & self.masks[player] & ~repairs).bit_count()
        if repairs:
            total += (bought & repairs == repairs) if self.refunds[player] else bool(bought & repairs)
        return total

    def available(self, player, state, bought):
        # AP counts receipts. The wallet also counts what we spent.
        return state.count(CRAFTMETAL_ITEM, player) - self.spent(player, bought)

    def remaining_cost(self, player, bought):
        repairs = self.repairs[player]
        remaining = self.masks[player] & self.baseline_purchases & ~bought
        total = (remaining & ~repairs).bit_count()
        if remaining & repairs:
            total += (bought & repairs != repairs) if self.refunds[player] else not bool(bought & repairs)
        return total

    def excluded_repair(self, index, bought):
        location = self.purchases[index]
        repairs = self.repairs[location.player]
        return (not self.refunds[location.player] and bool(repairs & (1 << index))
                and bool(repairs & bought) and not bool(bought & (1 << index)))

    def buy(self, state, bought, index):
        location = self.purchases[index]
        state.collect(location.item, True, location)
        state.advancements.add(location)
        return bought | (1 << index)

    def reachable(self, player, state):
        key = player, frozenset(state.prog_items[player].items())
        cached = self.reach_cache.get(key)
        if cached is None:
            free = tuple(location for location in self.free_by_player[player]
                         if location.advancement and location.can_reach(state))
            purchases = sum(1 << index for index, location in enumerate(self.purchases)
                            if location.player == player and location.can_reach(state))
            cached = self.reach_cache[key] = free, purchases
        return cached

    def sweep(self, state):
        while True:
            previous = len(state.advancements)
            for player in self.worlds:
                for location in self.reachable(player, state)[0]:
                    if location not in state.advancements:
                        state.collect(location.item, True, location)
                        state.advancements.add(location)
            if self.foreign_free:
                state.sweep_for_advancements(locations=self.foreign_free)
            for location in self.foreign_full:
                if location not in state.advancements and location.can_reach(state):
                    state.collect(location.item, True, location)
                    state.advancements.add(location)
            if len(state.advancements) == previous:
                return

    def reachable_purchases(self, state):
        return sum(self.reachable(player, state)[1] for player in self.worlds)

    def settle(self, state, bought):
        while True:
            self.sweep(state)
            reachable = self.reachable_purchases(state)
            funded = {
                player for player in self.worlds
                if self.available(player, state, bought) >= self.remaining_cost(player, bought)
            }
            previous = bought
            for index, location in enumerate(self.purchases):
                bit = 1 << index
                player = location.player
                if bought & bit or self.excluded_repair(index, bought):
                    continue
                if self.available(player, state, bought) < 1 or not reachable & bit:
                    continue
                repairs = self.repairs[player]
                if repairs & bit and not self.refunds[player]:
                    continue
                if player in funded or self.filler & bit:
                    bought = self.buy(state, bought, index)
            if bought == previous:
                return bought

    def finished(self, state, bought):
        # Other worlds may still have post-fill work left.
        if not self.finalized and all(bought & (1 << index) or self.excluded_repair(index, bought)
                                      for index in range(len(self.purchases))):
            return True
        if not all(self.multiworld.has_beaten_game(state, player) for player in self.goals):
            return False
        for location in self.required:
            index = self.indices.get(location)
            if index is not None:
                if not bought & (1 << index) and not self.excluded_repair(index, bought):
                    return False
            elif location not in state.advancements and not location.can_reach(state):
                return False
        return True

    def covered(self, bought, sleeping):
        return any(previous & sleeping == previous for previous in self.visited.get(bought, ()))

    def search(self, state, bought=0, sleeping=0):
        if self.covered(bought, sleeping):
            return None
        incoming = bought
        bought = self.settle(state, bought)
        for player, mask in self.masks.items():
            if (bought ^ incoming) & mask:
                sleeping &= ~mask
        sleeping &= ~bought
        if self.covered(bought, sleeping):
            return None
        self.visited[bought] = [previous for previous in self.visited.get(bought, ())
                                if previous & sleeping != sleeping] + [sleeping]
        self.states += 1
        self.run_states += 1
        if self.finished(state, bought):
            return None
        if self.run_states > self.state_limit:
            return SpendingFailure(state, bought, exhausted=True)
        reachable = self.reachable_purchases(state)
        choices = [index for index, location in enumerate(self.purchases)
                   if not bought & (1 << index) and not self.excluded_repair(index, bought)
                   and self.available(location.player, state, bought) > 0
                   and reachable & (1 << index)]
        if not choices:
            return SpendingFailure(state, bought)
        for index in choices:
            bit = 1 << index
            location = self.purchases[index]
            if sleeping & bit:
                continue
            # Different players don't spend from the same wallet.
            next_sleeping = sleeping & ~self.masks[location.player]
            if self.covered(bought | bit, next_sleeping):
                sleeping |= bit
                continue
            next_state = state.copy()
            failure = self.search(next_state, self.buy(next_state, bought, index), next_sleeping)
            if failure is not None:
                return failure
            sleeping |= bit
        return None

    def update_baseline(self, initial_state=None):
        state = initial_state.copy() if initial_state is not None else CollectionState(self.multiworld)
        bought = 0
        while True:
            self.sweep(state)
            reachable = self.reachable_purchases(state)
            previous = bought
            for index in range(len(self.purchases)):
                if reachable & (1 << index) and not bought & (1 << index):
                    bought = self.buy(state, bought, index)
            if bought == previous:
                break
        # Keep earlier guarantees when a repair moves a reward.
        self.baseline_locations.update(location for location in self.locations
                                       if location in state.advancements or location.can_reach(state))
        self.baseline_purchases = sum(1 << index for index, location in enumerate(self.purchases)
                                      if location in self.baseline_locations)
        self.goals.update(player for player in self.multiworld.player_ids
                          if self.multiworld.has_beaten_game(state, player))

    def run(self, base_state=None):
        self.visited.clear()
        self.reach_cache.clear()
        self.run_states = 0
        # Reachable filler purchases spend the same coin without opening anything.
        self.filler = sum(1 << index for index, location in enumerate(self.purchases)
                          if not location.item.advancement and self.recipients.get(location.item.player)
                          and location.address is not None and not self.repairs[location.player] & (1 << index))
        initial_state = base_state.copy() if base_state is not None else CollectionState(self.multiworld)
        self.sweep(initial_state)
        self.update_baseline(initial_state)
        self.required = tuple(
            location for location in self.locations
            if location in self.baseline_locations
            and location not in self.alternatives and (location.player in self.full or (
                location.advancement and location.item.player not in self.minimal))
        )
        return self.search(initial_state)

    def repair_sources(self, failure, ranks):
        sources = sorted(
            (location for index, location in enumerate(self.purchases)
             if not failure.bought & (1 << index)
             and location in self.baseline_locations
             and location.address is not None and not location.locked
             and location.item.advancement and location.item.name != MEMORY_LOCKET_ITEM),
            key=lambda location: location.item.name == CRAFTMETAL_ITEM,
        )
        sources.extend(sorted(
            (location for location in self.free
             if location in self.baseline_locations
             and location.address is not None and not location.locked
             and location.item.name == CRAFTMETAL_ITEM
             and any(self.available(player, failure.state, failure.bought)
                     < self.remaining_cost(player, failure.bought)
                     for player in self.recipients.get(location.item.player, ()))
             and not location.can_reach(failure.state)),
            key=lambda location: (ranks.get(location, -1), location.player, location.name),
        ))
        optional_rewards = sorted(
            (location for location in self.free
             if location.player not in self.full and location in self.baseline_locations
             and location.address is not None and not location.locked and location.item.advancement
             and location.item.name not in (CRAFTMETAL_ITEM, MEMORY_LOCKET_ITEM)
             and not location.can_reach(failure.state)),
            key=lambda location: (ranks.get(location, -1), location.player, location.name),
        )
        return chain(sources, self.funding_sources(failure, ranks), optional_rewards)

    def repair(self, failure, ranks):
        targets = sorted(
            (location for location in self.free
             if location.address is not None and not location.locked
             and not location.item.advancement
             and location.name not in CREST_SLOT_LOCATION_NAMES
             and location.item.name not in (CRAFTMETAL_ITEM, MEMORY_LOCKET_ITEM)
             and location.can_reach(failure.state)),
            key=lambda location: (-ranks.get(location, -1), location.player, location.name),
        )
        candidates = []
        for source in self.repair_sources(failure, ranks):
            candidates.append(source)
            for target in targets:
                if ranks.get(target, -1) > ranks.get(source, -1):
                    continue
                if (source.can_fill(failure.state, target.item, False)
                        and target.can_fill(failure.state, source.item, False)):
                    item = source.item
                    swap_location_item(source, target)
                    return {'item': item.name, 'player': item.player,
                            'from': (source.player, source.name), 'to': (target.player, target.name)}
        return self.repair_progression(failure, candidates, ranks)

    def swap_candidates(self, failure, sources, ranks, *, progression_only=True):
        sources = sorted(sources, key=lambda location: (not location.can_reach(failure.state),
                                                       ranks.get(location, -1), location.player, location.name))
        targets = sorted(
            (location for location in self.free
             if location.address is not None and not location.locked
             and (not progression_only or location.item.advancement)
             and location.name not in CREST_SLOT_LOCATION_NAMES
             and location.item.name not in (CRAFTMETAL_ITEM, MEMORY_LOCKET_ITEM)
             and location.can_reach(failure.state)),
            key=lambda location: (location.item.advancement, ranks.get(location, -1), location.player, location.name),
        )
        for source in sources:
            for target in targets:
                if (source.item.name, source.item.player) == (target.item.name, target.item.player):
                    continue
                if not (source.can_fill(failure.state, target.item, False)
                        and target.can_fill(failure.state, source.item, False)):
                    continue
                yield source, target

    def check_swap(self, source, target):
        item = source.item
        swap_location_item(source, target)
        accepted = False
        try:
            trial = self.repair_trial()
            failure = trial.run()
            accepted = failure is None
        finally:
            if not accepted:
                swap_location_item(source, target)
        change = {'item': item.name, 'player': item.player,
                  'from': (source.player, source.name), 'to': (target.player, target.name)}
        return failure, change

    def repair_trial(self):
        trial = SpendingAudit(self.multiworld, self.worlds.values())
        trial.baseline_locations.update(self.baseline_locations)
        trial.goals.update(self.goals)
        return trial

    def repair_progression(self, failure, sources, ranks):
        parents = []
        for source, target in islice(self.swap_candidates(failure, sources, ranks), self.swap_limit):
            blocked, change = self.check_swap(source, target)
            if blocked is None:
                return change
            if not blocked.exhausted:
                parents.append((len(blocked.state.advancements), source, target, change))

        # Some shortages need two moves before either one can help.
        parent_limit = 8
        followup_limit = self.swap_limit // parent_limit
        if not followup_limit:
            return None
        seen = set()
        for score, source, target, change in sorted(parents, key=lambda entry: entry[0], reverse=True):
            signature = source.item.name, source.item.player, score
            if signature in seen:
                continue
            seen.add(signature)
            swap_location_item(source, target)
            accepted = False
            try:
                trial = self.repair_trial()
                blocked = trial.run()
                if blocked is not None and not blocked.exhausted:
                    candidates = trial.swap_candidates(blocked, trial.repair_sources(blocked, ranks), ranks,
                                                       progression_only=False)
                    for next_source, next_target in islice(candidates, followup_limit):
                        next_blocked, followup = self.check_swap(next_source, next_target)
                        if next_blocked is None:
                            change['followup'] = followup
                            accepted = True
                            return change
            finally:
                if not accepted:
                    swap_location_item(source, target)
            if len(seen) >= parent_limit:
                break
        return None

    def funding_sources(self, failure, ranks):
        underfunded = {
            player for player in self.worlds
            if self.available(player, failure.state, failure.bought)
            < self.remaining_cost(player, failure.bought)
        }
        if not any(location.locked and location.item.name == CRAFTMETAL_ITEM
                   and self.recipients.get(location.item.player, set()) & underfunded
                   and not location.can_reach(failure.state) for location in self.free):
            return
        candidates = sorted(
            (location for location in self.free
             if location.address is not None and not location.locked
             and location in self.baseline_locations and location.item.advancement
             and location.item.name not in (CRAFTMETAL_ITEM, MEMORY_LOCKET_ITEM)
             and not location.can_reach(failure.state)),
            key=lambda location: (ranks.get(location, -1), location.player, location.name),
        )
        for location in candidates:
            state = failure.state.copy()
            state.collect(location.item, True, location)
            self.sweep(state)
            if any(state.count(CRAFTMETAL_ITEM, player) > failure.state.count(CRAFTMETAL_ITEM, player)
                   for player in underfunded):
                yield location


def audit_craftmetal_spending(multiworld, worlds, *, finalized=True, base_state=None):
    audit = SpendingAudit(multiworld, worlds, finalized=finalized)
    if not audit.purchases:
        return
    repairs = []
    ranks = None
    while (failure := audit.run(base_state)) is not None:
        if ranks is None:
            ranks = {location: index for index, sphere in enumerate(multiworld.get_spheres())
                     for location in sphere}
        repair = audit.repair(failure, ranks)
        if repair is None:
            spent = ', '.join(
                f'{multiworld.player_name[player]}: {audit.spent(player, failure.bought)} spent, '
                f'{audit.available(player, failure.state, failure.bought)} left'
                for player in audit.worlds
            )
            blocked = [str(location) for location in audit.required
                       if location not in failure.state.advancements and not location.can_reach(failure.state)]
            goals = [multiworld.player_name[player] for player in sorted(audit.goals)
                     if not multiworld.has_beaten_game(failure.state, player)]
            pending = [str(location) for index, location in enumerate(audit.purchases)
                       if location in audit.baseline_locations
                       and not failure.bought & (1 << index) and not audit.excluded_repair(index, failure.bought)]
            details = (f' Unreachable checks: {", ".join(blocked[:8])}.' if blocked else '')
            details += (f' Unfinished goals: {", ".join(goals[:8])}.' if goals else '')
            if not pending:
                raise FillError('Craftmetal spending left previously reachable checks or goals inaccessible.'
                                + details, multiworld=multiworld)
            if failure.exhausted:
                raise FillError('Craftmetal spending validation exceeded its search limit. '
                                'No safe reward swap was found. This seed could not be verified.'
                                + details, multiworld=multiworld)
            raise FillError(
                'Craftmetal purchases can leave required progression unreachable '
                f'({spent}). No safe reward swap was found. '
                'Check locked placements, exclusions or vanilla tool settings.'
                f' Unbought checks: {", ".join(pending[:8])}.' + details,
                multiworld=multiworld,
            )
        repairs.append(repair)
        base_state = None
    previous = getattr(multiworld, '_silksong_craftmetal_audit', {'states': 0, 'repairs': []})
    multiworld._silksong_craftmetal_audit = {
        'states': previous['states'] + audit.states,
        'repairs': previous['repairs'] + repairs,
    }


def validate_native_supply(world, state):
    from Options import OptionError

    if (world.options.accessibility == 'minimal' or world.get_category_mode('Craftmetal') != 'vanilla'
            or world.options.accessibility != 'full' and world.get_category_mode('Tool') != 'vanilla'):
        return
    purchases = {location.name for location in world.get_locations()
                 if location.name in CRAFTMETAL_PURCHASE_LOCATIONS and location.can_reach(state)}
    needed = len(purchases.difference(RUINED_TOOL_REPAIR_LOCATIONS))
    needed += bool(purchases.intersection(RUINED_TOOL_REPAIR_LOCATIONS))
    available = state.count(CRAFTMETAL_ITEM, world.player)
    if available >= needed:
        return
    if world.options.accessibility != 'full':
        multiworld = world.multiworld
        audit = SpendingAudit(multiworld, [world])
        assumed = CollectionState(multiworld)
        for item in multiworld.itempool:
            multiworld.worlds[item.player].collect(assumed, item)
        for player in multiworld.player_ids:
            for item in multiworld.worlds[player].get_pre_fill_items():
                multiworld.worlds[item.player].collect(assumed, item)
        # Give movable rewards up front, fixed local purchases still cost metal.
        for location in audit.locations:
            if location in audit.indices:
                continue
            if location.player != world.player or location.address is not None:
                assumed.collect(location.item, True, location)
                assumed.advancements.add(location)
        failure = audit.run(assumed)
        if failure is None or failure.exhausted:
            return
    raise OptionError(
        f'Player {world.player}: reachable purchases can spend {needed} Craftmetals, '
        f'but only {available} are obtainable with these settings. '
        f'Enable Craftmetal Randomization or add {needed - available} Craftmetal to Start Inventory.'
    )
