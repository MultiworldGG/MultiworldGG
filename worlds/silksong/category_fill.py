from __future__ import annotations

from collections import defaultdict

from BaseClasses import CollectionState, LocationProgressType
from Options import OptionError

from .items import get_vanilla_reward_name


def _placement_category(value) -> str | None:
    return getattr(value, "silksong_placement_category", None)


def validate_excluded_filler(multiworld, game):
    solo = multiworld.players == 1 and not multiworld.groups
    maximum = multiworld.get_all_state() if solo else None
    if maximum is not None and not multiworld.has_beaten_game(maximum):
        maximum = None
    locations = [location for world in multiworld.get_game_worlds(game) for location in world.get_locations()
                 if location.item is None and location.address is not None
                 and (location.progress_type == LocationProgressType.EXCLUDED
                      or maximum is not None and world.options.accessibility != 'minimal' and not location.can_reach(maximum))]
    if not locations:
        return
    items = [item for item in multiworld.itempool if not item.advancement and not item.useful]
    candidates = {location: [index for index, item in enumerate(items)
                            if location.can_fill(multiworld.state, item, check_access=False)]
                  for location in locations}
    assigned = {}
    owned = {}

    def assign(location):
        pending = [location]
        visited = {location}
        previous = {}
        for current in pending:
            for index in candidates[current]:
                if index in previous:
                    continue
                previous[index] = current
                if index not in assigned:
                    while True:
                        current = previous[index]
                        old = owned.get(current)
                        assigned[index] = current
                        owned[current] = index
                        if old is None:
                            return True
                        index = old
                owner = assigned[index]
                if owner not in visited:
                    visited.add(owner)
                    pending.append(owner)
        return False

    missing = [location for location in sorted(locations, key=lambda loc: len(candidates[loc]))
               if not assign(location)]
    if missing:
        names = ', '.join(f'P{location.player} {location.name}' for location in missing[:8])
        if len(missing) > 8:
            names += f' and {len(missing) - 8} more'
        raise OptionError(
            f'The selected options leave {len(missing)} excluded or unreachable checks without compatible filler or traps: {names}. '
            'Progression and useful items cannot fill these checks. Set a filler category such as Rosary Caches '
            'to Anywhere or adjust exclusion, locality or plando settings.'
        )


def _flea_pool_is_placeable(multiworld, player, candidates=(), *, assume_wishes=False):
    from .display_names import FLEA_ITEM_NAMES
    from .requirement_rules import sweep_native_sources

    if multiworld.groups:
        return True
    fleas = [item for item in multiworld.itempool
             if item.player == player and item.name in FLEA_ITEM_NAMES]
    if not fleas:
        return True
    world = multiworld.worlds[player]
    flea_ids = {id(item) for item in fleas}
    state = CollectionState(multiworld)
    if assume_wishes:
        _assume_wish_offers(state)
    for item in multiworld.itempool:
        if item.advancement and id(item) not in flea_ids:
            state.collect(item, True)
    filled = multiworld.get_filled_locations()
    targets = multiworld.get_unfilled_locations()
    supplied = 0
    pending = defaultdict(list)
    for location in candidates:
        pending[location.player, _placement_category(location)].append(location)
    while True:
        sweep_native_sources(state, filled)
        opened = [lane for lane, locations in pending.items()
                  if any(location.can_reach(state) for location in locations)]
        if opened:
            for lane in opened:
                for location in pending.pop(lane):
                    state.collect(location.item, True)
            continue
        if supplied == len(fleas) or (
                world.options.accessibility == "minimal" and multiworld.has_beaten_game(state, player)):
            return True
        reachable = [location for location in targets if location.can_reach(state)]
        choices = [tuple(location for location in reachable
                         if location.can_fill(state, flea, check_access=False)) for flea in fleas]
        if all(choice == choices[0] for choice in choices):
            available = min(len(choices[0]), len(fleas))
        else:
            matches = {}

            def match(index, seen):
                for location in choices[index]:
                    if location in seen:
                        continue
                    seen.add(location)
                    if location not in matches or match(matches[location], seen):
                        matches[location] = index
                        return True
                return False

            for index in range(len(fleas)):
                match(index, set())
            available = len(matches)
        if available <= supplied:
            return False
        for _ in range(available - supplied):
            state.collect(world.create_item("Flea"), True)
        supplied = available


def _assume_wish_offers(state):
    from .room_graph_logic import native_region_name

    for world in state.multiworld.worlds.values():
        for wish in getattr(world, "_progression_wishes", ()):
            region = state.multiworld.get_region(native_region_name("Wish Offer: " + wish.identity), world.player)
            state.reachable_regions[world.player].add(region)
            state.blocked_connections[world.player].update(region.exits)
        state.rule_builder_cache[world.player].clear()
        state.stale[world.player] = True


def validate_flea_capacity(multiworld, game_name):
    for world in multiworld.get_game_worlds(game_name):
        if not _flea_pool_is_placeable(multiworld, world.player):
            raise OptionError(
                f'Player {world.player}: too few reachable checks can hold the required fleas, '
                'even with every other randomized item available. Enable additional reachable '
                'check categories, randomize movement abilities or choose another starting location.'
            )


def _reserve_solo_opening(world, pool, locations, *, minimum_gain=2):
    from .requirement_rules import sweep_native_pool

    reserved = False
    for step in range(8):
        state = sweep_native_pool(CollectionState(world.multiworld))
        empty = [location for location in locations if location.item is None]
        reached = [location for location in empty if location.can_reach(state)]
        if step == 0 and len(reached) > 5:
            return False
        best = None
        seen = set()
        for item in pool:
            if item.name in seen:
                continue
            seen.add(item.name)
            target = next((location for location in reached if location.can_fill(state, item)), None)
            if target is None:
                continue
            trial = sweep_native_pool(state, [item])
            score = sum(location.can_reach(trial) for location in empty)
            if best is None or score > best[0]:
                best = score, target, item
        if best is None or best[0] < len(reached) + minimum_gain:
            break
        _, target, item = best
        target.item = item
        item.location = target
        pool.remove(item)
        reserved = True
    return reserved


def validate_goal(world, all_state):
    if not world.multiworld.has_beaten_game(all_state, world.player):
        blocked = [f'{location.item.name} at {location.name}' for location in world.get_locations()
                   if location.name in world.location_name_to_id and location.locked and location.item is not None
                   and location.item.advancement and not location.can_reach(all_state)]
        detail = (' Blocked fixed rewards: ' + ', '.join(blocked[:8]) + '.') if blocked else ''
        raise OptionError(
            f'Player {world.player}: the goal cannot be reached with all available items under the current mapped logic. '
            'Check vanilla ability settings and fixed reward access before generating again.'
            + detail
        )


def fill_solo_progression(world, progression, locations):
    from Fill import FillError, fill_restrictive, sweep_from_pool

    multiworld = world.multiworld
    if world is next(iter(multiworld.get_game_worlds(world.game))):
        all_state = multiworld.get_all_state()
        for candidate in multiworld.get_game_worlds(world.game):
            validate_goal(candidate, all_state)
    if multiworld.players != 1 or multiworld.groups or not progression:
        return
    if world.options.accessibility == 'full':
        unreachable = [location.name for location in world.get_locations()
                       if location.name in world.location_name_to_id and not location.can_reach(all_state)]
        if unreachable:
            detail = ''
            if 'Egg of Flealia' in unreachable:
                from .display_names import FLEA_ITEM_NAMES
                fleas = sum(all_state.count(name, world.player) for name in FLEA_ITEM_NAMES)
                if fleas < 30:
                    detail = f' Egg of Flealia needs 30 fleas, but only {fleas} are available in logic.'
            raise OptionError(
                'Full accessibility cannot reach every enabled check with the selected items and logic options: '
                + ', '.join(unreachable[:8]) + (f' and {len(unreachable) - 8} more' if len(unreachable) > 8 else '')
                + '.' + detail + ' Check vanilla reward access, disabled techniques and removed abilities.'
            )
    if any(location.progress_type == LocationProgressType.PRIORITY for location in locations):
        return
    available = [location for location in locations
                 if location.progress_type == LocationProgressType.DEFAULT]
    failure = None
    accepted = False

    attempted_normal = False
    opening_attempted = False

    def attempts():
        yield False
        yield False
        for _ in range(4):
            multiworld.random.shuffle(progression)
            multiworld.random.shuffle(available)
            yield False
        yield True

    for neutral_opening in attempts():
        try:
            pool = list(progression)
            if neutral_opening:
                if not _reserve_solo_opening(world, pool, available, minimum_gain=1):
                    continue
            elif not attempted_normal:
                attempted_normal = True
            elif not opening_attempted:
                opening_attempted = True
                if not _reserve_solo_opening(world, pool, available):
                    continue
            fill_restrictive(multiworld, sweep_from_pool(multiworld.state),
                             [location for location in available if location.item is None], pool,
                             single_player_placement=True, name="Silksong progression")
            reached = sweep_from_pool(multiworld.state)
            if pool or not multiworld.has_beaten_game(reached) or any(
                    world.options.accessibility != "minimal"
                    and location.item.advancement and not location.can_reach(reached)
                    for location in multiworld.get_filled_locations()):
                continue
            progression.clear()
            locations[:] = [location for location in locations if location.item is None]
            accepted = True
            return
        except FillError as error:
            if failure is None:
                failure = error
        finally:
            if not accepted:
                for location in available:
                    if location.item is not None:
                        location.item.location = None
                        location.item = None
    if failure is not None:
        raise failure


def fill_multiworld_progression(multiworld, game_name, progression, locations):
    from Fill import FillError, accessibility_corrections, fill_restrictive, sweep_from_pool
    from .items import item_name_groups

    if (multiworld.players < 2 or multiworld.groups or not progression
            or any(world.game != game_name for world in multiworld.worlds.values())
            or any(location.progress_type == LocationProgressType.PRIORITY for location in locations)):
        return
    available = [location for location in locations
                 if location.progress_type == LocationProgressType.DEFAULT]
    pool = list(progression)
    filled = False
    seen = set()
    swaps = 0

    class RetryFill(Exception):
        pass

    def placed(location):
        nonlocal swaps
        if location in seen:
            swaps += 1
            if swaps > max(8, 2 * multiworld.players):
                raise RetryFill()
        seen.add(location)

    try:
        fill_restrictive(multiworld, sweep_from_pool(multiworld.state), available[:], pool,
                         on_place=placed, name="Silksong progression")
        filled = not pool
    except (RetryFill, FillError):
        pass
    finally:
        if not filled:
            for location in available:
                if location.item is not None:
                    location.item.location = None
                    location.item = None
    if filled:
        progression.clear()
        remaining = [location for location in available if location.item is None]
        accessibility_corrections(multiworld, multiworld.state, remaining)
        locations[:] = [location for location in locations
                        if location.progress_type != LocationProgressType.DEFAULT] + remaining
        return
    # Leave movement for the opening when the usual order gets stuck.
    movement = item_name_groups["Skills"] | item_name_groups["Innate Abilities"]
    for player in multiworld.player_ids:
        indices = [index for index, item in enumerate(progression) if item.player == player]
        ordered = sorted((progression[index] for index in indices),
                         key=lambda item: item.name not in movement)
        for index, item in zip(indices, ordered):
            progression[index] = item


def validate_opening(multiworld, game_name):
    if any(world.game != game_name for world in multiworld.worlds.values()):
        return
    items = [item for item in multiworld.itempool
             if item.advancement]
    if not items:
        return
    state = CollectionState(multiworld)
    state.sweep_for_advancements()
    if multiworld.has_beaten_game(state):
        return
    if any(location.can_reach(state) and any(
            location.can_fill(state, item, check_access=False) for item in items)
            for location in multiworld.get_unfilled_locations()):
        return
    advice = (
        "Set an early check category to Anywhere, change the starting location "
        "or provide starting movement through Start Inventory from Pool."
    )
    cache_players = [str(world.player) for world in multiworld.get_game_worlds(game_name)
                     if getattr(world.options, 'ledgegrab_ability_rando', False)
                     and world.get_starting_location_key() == 'bone_bottom'
                     and world.options.rosary_cache_randomization == 'vanilla']
    if cache_players:
        advice = (
            f"For the blocked Bone Bottom Ledge Grab starts (players {', '.join(cache_players)}), "
            "enable Rosary Cache Randomization by setting rosary_cache_randomization: anywhere. "
            "In a multiworld, enabling it for one of these players can provide an opening. "
            "Another starting location or starting movement through Start Inventory from Pool can also help."
        )
    raise OptionError(
        "The starting and entrance settings leave no reachable check that can hold "
        "progression in any world. "
        + advice
    )
