from __future__ import annotations

from dataclasses import dataclass

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
        total = (self.masks[player] & ~repairs & ~bought).bit_count()
        if repairs:
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
        key = player, tuple(sorted(state.prog_items[player].items()))
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
        if not self.multiworld.has_beaten_game(state):
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

    def run(self):
        self.visited.clear()
        self.reach_cache.clear()
        self.run_states = 0
        # Reachable filler purchases spend the same coin without opening anything.
        self.filler = sum(1 << index for index, location in enumerate(self.purchases)
                          if not location.item.advancement and self.recipients.get(location.item.player)
                          and location.address is not None and not self.repairs[location.player] & (1 << index))
        self.required = tuple(
            location for location in self.locations
            if location not in self.alternatives and (location.player in self.full or (
                location.advancement and location.item.player not in self.minimal))
        )
        return self.search(CollectionState(self.multiworld))

    def repair(self, failure, ranks):
        sources = sorted(
            (location for index, location in enumerate(self.purchases)
             if not failure.bought & (1 << index)
             and location.address is not None and not location.locked
             and location.item.advancement and location.item.name != MEMORY_LOCKET_ITEM),
            key=lambda location: location.item.name == CRAFTMETAL_ITEM,
        )
        sources.extend(sorted(
            (location for location in self.free
             if location.address is not None and not location.locked
             and location.item.name == CRAFTMETAL_ITEM
             and any(self.available(player, failure.state, failure.bought)
                     < self.remaining_cost(player, failure.bought)
                     for player in self.recipients.get(location.item.player, ()))
             and not location.can_reach(failure.state)),
            key=lambda location: (ranks.get(location, -1), location.player, location.name),
        ))
        targets = sorted(
            (location for location in self.free
             if location.address is not None and not location.locked
             and not location.item.advancement
             and location.name not in CREST_SLOT_LOCATION_NAMES
             and location.item.name not in (CRAFTMETAL_ITEM, MEMORY_LOCKET_ITEM)
             and location.can_reach(failure.state)),
            key=lambda location: (-ranks.get(location, -1), location.player, location.name),
        )
        for source in sources:
            for target in targets:
                if ranks.get(target, -1) > ranks.get(source, -1):
                    continue
                if (source.can_fill(failure.state, target.item, False)
                        and target.can_fill(failure.state, source.item, False)):
                    item = source.item
                    swap_location_item(source, target)
                    return {'item': item.name, 'player': item.player,
                            'from': (source.player, source.name), 'to': (target.player, target.name)}
        return None


def audit_craftmetal_spending(multiworld, worlds, *, finalized=True):
    audit = SpendingAudit(multiworld, worlds, finalized=finalized)
    if not audit.purchases:
        return
    repairs = []
    ranks = None
    while (failure := audit.run()) is not None:
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
            goals = [multiworld.player_name[player] for player in multiworld.player_ids
                     if not multiworld.has_beaten_game(failure.state, player)]
            pending = [str(location) for index, location in enumerate(audit.purchases)
                       if not failure.bought & (1 << index) and not audit.excluded_repair(index, failure.bought)]
            details = (f' Unreachable checks: {", ".join(blocked[:8])}.' if blocked else '')
            details += (f' Unfinished goals: {", ".join(goals[:8])}.' if goals else '')
            if not pending:
                raise FillError('All Craftmetal purchases were reachable, but final accessibility validation failed.'
                                + details, multiworld=multiworld)
            if failure.exhausted:
                raise FillError('Craftmetal spending validation exceeded its search limit. '
                                'No legal reward swap remains. This seed could not be verified.'
                                + details, multiworld=multiworld)
            raise FillError(
                'Craftmetal purchases can leave required progression unreachable '
                f'({spent}). No legal reward swap remains. '
                'Check locked placements, exclusions or vanilla tool settings.'
                f' Unbought checks: {", ".join(pending[:8])}.' + details,
                multiworld=multiworld,
            )
        repairs.append(repair)
    previous = getattr(multiworld, '_silksong_craftmetal_audit', {'states': 0, 'repairs': []})
    multiworld._silksong_craftmetal_audit = {
        'states': previous['states'] + audit.states,
        'repairs': previous['repairs'] + repairs,
    }
