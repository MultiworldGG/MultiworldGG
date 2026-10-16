from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from BaseClasses import CollectionState, LocationProgressType
from Options import OptionError

from .items import get_vanilla_reward_name


def _placement_category(value) -> str | None:
    return getattr(value, "silksong_placement_category", None)


def _assign_items(locations: list, items: list) -> None:
    for location in locations:
        if location.item is not None:
            location.item.location = None
        location.item = None
    for location, item in zip(locations, items):
        location.item = item
        item.location = location


def _can_fill_without_access(multiworld, location, item) -> bool:
    return location.player == item.player and location.can_fill(
        multiworld.state,
        item,
        check_access=False,
    )


def _items_obey_fill_rules(
    multiworld,
    locations: list,
    items: list,
) -> bool:
    return all(
        _can_fill_without_access(multiworld, location, item)
        for location, item in zip(locations, items)
    )


def _match_items_to_locations(
    multiworld,
    category: str,
    locations: list,
    preferred_items: list,
) -> list:
    """Find a rule-safe perfect matching, preferring the native baseline."""

    if _items_obey_fill_rules(multiworld, locations, preferred_items):
        return preferred_items

    item_index_by_id = {
        id(item): index
        for index, item in enumerate(preferred_items)
    }
    candidates_by_location: dict[int, list[int]] = {}
    for location_index, location in enumerate(locations):
        preferred_index = item_index_by_id[
            id(preferred_items[location_index])
        ]
        candidates = [
            item_index
            for item_index, item in enumerate(preferred_items)
            if _can_fill_without_access(multiworld, location, item)
        ]
        if preferred_index in candidates:
            candidates.remove(preferred_index)
            candidates.insert(0, preferred_index)
        if not candidates:
            raise ValueError(
                f"{category} shuffle has no legal reward for "
                f"{location.name!r}. Check excluded/local item settings."
            )
        candidates_by_location[location_index] = candidates

    location_by_item: dict[int, int] = {}

    def assign_location(
        location_index: int,
        seen_items: set[int],
    ) -> bool:
        for item_index in candidates_by_location[location_index]:
            if item_index in seen_items:
                continue
            seen_items.add(item_index)
            previous_location = location_by_item.get(item_index)
            if (
                previous_location is None
                or assign_location(previous_location, seen_items)
            ):
                location_by_item[item_index] = location_index
                return True
        return False

    for location_index in sorted(
        range(len(locations)),
        key=lambda index: len(candidates_by_location[index]),
    ):
        if not assign_location(location_index, set()):
            raise ValueError(
                f"{category} shuffle cannot satisfy all location safety, "
                "exclusion and locality rules."
            )

    item_by_location = {
        location_index: preferred_items[item_index]
        for item_index, location_index in location_by_item.items()
    }
    return [
        item_by_location[location_index]
        for location_index in range(len(locations))
    ]


def _pop_matching(items: list, predicate):
    for index, item in enumerate(items):
        if predicate(item):
            return items.pop(index)
    return None


def _build_native_baseline(
    category: str,
    locations: list,
    items: list,
) -> list:
    """Pair each player's category items with their native source first."""

    remaining = list(items)
    assigned: dict[object, object] = {}
    deferred = []

    for location in locations:
        reward_name = get_vanilla_reward_name(
            location.name,
            category,
        )
        item = _pop_matching(
            remaining,
            lambda candidate: (
                candidate.player == location.player
                and candidate.name == reward_name
            ),
        )
        if item is None:
            deferred.append(location)
        else:
            assigned[location] = item

    for location in deferred:
        assigned[location] = remaining.pop(0)

    if remaining:
        raise ValueError(
            f"Could not build the {category} shuffle baseline. "
            f"{len(remaining)} items were left over."
        )
    return [assigned[location] for location in locations]


def _shuffle_is_accessible(
    multiworld,
    shuffled_locations: Iterable,
    silksong_players: Iterable[int],
    reachability_context=None,
    *, check_capacity=True,
) -> bool:
    unreachable_locations, unbeaten_players = (
        _shuffle_reachability_failures(
            multiworld,
            shuffled_locations,
            silksong_players,
            reachability_context,
            check_capacity=check_capacity,
        )
    )
    return not unreachable_locations and not unbeaten_players


def _minimal_accessibility_players(multiworld) -> frozenset[int]:
    players = set()
    for player in multiworld.player_ids:
        options = getattr(multiworld.worlds[player], "options", None)
        accessibility = getattr(options, "accessibility", None)
        if accessibility is None:
            continue
        value = getattr(accessibility, "value", accessibility)
        minimal_value = getattr(accessibility, "option_minimal", 2)
        if value == minimal_value or value in ("minimal", "none"):
            players.add(player)
    return frozenset(players)


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


def _shuffle_reachability_failures(
    multiworld,
    shuffled_locations: Iterable,
    silksong_players: Iterable[int],
    reachability_context=None,
    maximum_state=None,
    check_capacity=True,
) -> tuple[list[str], list[int]]:
    from .requirement_rules import sweep_native_pool as sweep_from_pool

    if maximum_state is None:
        if reachability_context is None:
            maximum_state = sweep_from_pool(multiworld.state, multiworld.itempool)
        else:
            maximum_pool_state, filled_locations = reachability_context
            maximum_state = sweep_from_pool(maximum_pool_state, locations=filled_locations)
    minimal_players = _minimal_accessibility_players(multiworld)
    unreachable_locations = sorted(
        (
            f"P{location.player} {location.name}"
            for location in shuffled_locations
            if (
                not location.can_reach(maximum_state)
                and getattr(
                    location,
                    "progress_type",
                    LocationProgressType.DEFAULT,
                ) != LocationProgressType.EXCLUDED
                and (
                    location.player not in minimal_players
                    or (
                        location.item is not None
                        and location.item.advancement
                        and location.item.player not in minimal_players
                    )
                )
            )
        ),
        key=str.casefold,
    )
    unbeaten_players = sorted(
        player
        for player in silksong_players
        if not multiworld.has_beaten_game(maximum_state, player)
    )
    if check_capacity and not unreachable_locations and not unbeaten_players:
        unbeaten_players = [player for player in silksong_players
                            if not _flea_pool_is_placeable(multiworld, player)]
    return unreachable_locations, unbeaten_players


def _build_shuffle_reachability_context(multiworld):
    from .requirement_rules import sweep_native_pool as sweep_from_pool

    return (
        sweep_from_pool(
            multiworld.state,
            multiworld.itempool,
            locations=(),
        ),
        tuple(multiworld.get_filled_locations()),
    )


def _repair_shuffle_swaps(
    multiworld, shuffled_locations, silksong_players,
    candidates, reachability_context,
) -> bool:
    from .requirement_rules import sweep_native_pool as sweep_from_pool

    candidates = sorted(
        candidates,
        key=lambda location: (location.player, location.name),
    )
    if len(candidates) < 2:
        return False
    pool_state, filled_locations = reachability_context
    all_items_state = sweep_from_pool(pool_state, locations=filled_locations)
    for location in candidates:
        all_items_state.collect(location.item, True)
    if not _shuffle_is_accessible(
        multiworld, shuffled_locations, silksong_players,
        (all_items_state, filled_locations), check_capacity=False,
    ):
        return False

    baseline = [location.item for location in candidates]
    accepted = False
    attempts = 0
    try:
        failures = tuple(map(set, _shuffle_reachability_failures(
            multiworld, shuffled_locations, silksong_players, reachability_context,
        )))
        while any(failures) and attempts < 128:
            state = sweep_from_pool(pool_state, locations=filled_locations)
            reachable_count = sum(location.can_reach(state) for location in filled_locations)
            reached = [location for location in candidates if location.can_reach(state)]
            blocked = [location for location in candidates
                       if location.item.advancement and not location.can_reach(state)]
            improved = False
            for source in blocked:
                for target in reached:
                    if (source.player != target.player
                            or _placement_category(source) != _placement_category(target)
                            or not _can_fill_without_access(multiworld, source, target.item)
                            or not _can_fill_without_access(multiworld, target, source.item)):
                        continue
                    before = [source.item, target.item]
                    _assign_items([source, target], before[::-1])
                    attempts += 1
                    trial_state = sweep_from_pool(pool_state, locations=filled_locations)
                    remaining = tuple(map(set, _shuffle_reachability_failures(
                        multiworld, shuffled_locations, silksong_players, reachability_context,
                        maximum_state=trial_state,
                    )))
                    improves_reach = (remaining == failures and
                                     sum(location.can_reach(trial_state) for location in filled_locations)
                                     > reachable_count)
                    if all(a <= b for a, b in zip(remaining, failures)) and (remaining != failures or improves_reach):
                        failures = remaining
                        improved = True
                        break
                    _assign_items([source, target], before)
                    if attempts >= 128:
                        break
                if improved or attempts >= 128:
                    break
            if not improved:
                return False
        accepted = not any(failures)
        return accepted
    finally:
        if not accepted:
            _assign_items(candidates, baseline)


def _assume_wish_offers(state):
    from .room_graph_logic import native_region_name

    for world in state.multiworld.worlds.values():
        for wish in getattr(world, "_progression_wishes", ()):
            region = state.multiworld.get_region(native_region_name("Wish Offer: " + wish.identity), world.player)
            state.reachable_regions[world.player].add(region)
            state.blocked_connections[world.player].update(region.exits)
        state.rule_builder_cache[world.player].clear()
        state.stale[world.player] = True


def _validate_category_order(multiworld, shuffled, players, candidates, context):
    from .requirement_rules import sweep_native_sources

    state = context[0].copy()
    pending = defaultdict(list)
    for location in candidates:
        pending[location.player, _placement_category(location)].append(location)
    memo = getattr(multiworld, "_silksong_native_source_memo", None)
    multiworld._silksong_native_source_memo = None
    try:
        _assume_wish_offers(state)
        while True:
            sweep_native_sources(state, context[1])
            opened = [lane for lane, locations in pending.items()
                      if any(location.can_reach(state) for location in locations)]
            if not opened:
                break
            for lane in opened:
                for location in pending.pop(lane):
                    state.collect(location.item, True)
        unreachable, unbeaten = _shuffle_reachability_failures(
            multiworld, shuffled, players, maximum_state=state, check_capacity=False,
        )
        capacity_blocked = [player for player in players
                            if not _flea_pool_is_placeable(
                                multiworld, player, candidates, assume_wishes=True)]
        if capacity_blocked and not unreachable and not unbeaten:
            raise OptionError(
                "Flea randomization has too few reachable locations to open progression, even "
                "assuming every other Anywhere item, all wish offers and any reachable category reward. "
                "Set more early check categories to Anywhere, change the starting crest "
                "or provide starting movement."
            )
        if unreachable or unbeaten:
            blocked = ", ".join(f"P{player} {category}" for player, category in sorted(pending))
            raise OptionError(
                "Simple Key Shuffle cannot open progression with these starting settings, even "
                "assuming every Anywhere item and all wish offers. "
                + (f"Blocked categories: {blocked}. " if blocked else "")
                + "Choose another starting crest, set Simple Keys to Anywhere "
                "or provide a starting movement item."
            )
    finally:
        multiworld._silksong_native_source_memo = memo


def _repair_shuffle_forward(multiworld, shuffled, players, candidates, context):
    from .requirement_rules import sweep_native_pool

    locations = list(candidates)
    baseline = [location.item for location in locations]
    pending = list(baseline)
    fixed = [location for location in context[1] if location not in locations]
    accepted = False
    try:
        for location in locations:
            location.item.location = None
            location.item = None
        state = sweep_native_pool(context[0], locations=fixed)
        while pending:
            empty = [location for location in locations if location.item is None]
            reached = [location for location in empty if location.can_reach(state)]
            if not reached:
                return False
            if len(reached) == len(empty):
                for category, player in sorted({(_placement_category(item), item.player) for item in pending}):
                    lane = [location for location in empty
                            if location.player == player and _placement_category(location) == category]
                    items = [item for item in pending
                             if item.player == player and _placement_category(item) == category]
                    _assign_items(lane, _match_items_to_locations(multiworld, category, lane, items))
                break
            best = None
            for item in pending:
                target = next((location for location in reached
                               if _can_fill_without_access(multiworld, location, item)), None)
                if target is None:
                    continue
                trial = state.copy()
                trial.collect(item, True)
                trial = sweep_native_pool(trial, locations=fixed)
                score = sum(location.can_reach(trial) for location in empty)
                score += sum(len(trial.reachable_regions[player]) for player in players)
                if best is None or score > best[0]:
                    best = score, target, item, trial
            if best is None:
                return False
            _, target, item, state = best
            target.item = item
            item.location = target
            pending.remove(item)
        accepted = _shuffle_is_accessible(multiworld, shuffled, players, context)
        return accepted
    finally:
        if not accepted:
            _assign_items(locations, baseline)


def _repair_shuffle_bootstrap(
    multiworld, shuffled_locations, silksong_players,
    candidates, reachability_context,
) -> bool:
    from Fill import FillError, fill_restrictive, sweep_from_pool

    _validate_category_order(multiworld, shuffled_locations, silksong_players, candidates, reachability_context)
    if _repair_shuffle_swaps(
        multiworld, shuffled_locations, silksong_players,
        candidates, reachability_context,
    ):
        return True

    if _repair_shuffle_forward(
        multiworld, shuffled_locations, silksong_players, candidates, reachability_context,
    ):
        return True

    locations = list(candidates)
    baseline = [location.item for location in locations]
    maximum_state = sweep_from_pool(
        reachability_context[0], baseline, locations=reachability_context[1],
    )
    if any(_shuffle_reachability_failures(
        multiworld, shuffled_locations, silksong_players, maximum_state=maximum_state,
    )):
        return False
    progression = [item for item in baseline if item.advancement]
    non_progression = [item for item in baseline if not item.advancement]
    accepted = False
    try:
        for location in locations:
            location.item.location = None
            location.item = None
        fill_restrictive(
            multiworld, reachability_context[0], locations[:], progression,
            lock=True, one_item_per_player=False, name="Category shuffle",
        )
        if progression:
            return False
        for category, player in sorted({(_placement_category(item), item.player) for item in non_progression}):
            lane_locations = [location for location in locations
                              if location.item is None and location.player == player
                              and _placement_category(location) == category]
            lane_items = [item for item in non_progression
                          if item.player == player and _placement_category(item) == category]
            _assign_items(lane_locations, _match_items_to_locations(
                multiworld, category, lane_locations, lane_items,
            ))
        accepted = all(location.item is not None for location in locations) and _shuffle_is_accessible(
            multiworld, shuffled_locations, silksong_players, reachability_context,
        )
        return accepted
    except FillError:
        return False
    finally:
        if not accepted:
            _assign_items(locations, baseline)


def _opening_shuffle_swaps(multiworld, candidates, assumed=()):
    from itertools import combinations
    from .requirement_rules import sweep_native_pool, _invalidate_native_source_player

    locations = list(candidates)
    targets = multiworld.get_unfilled_locations()
    opening = sweep_native_pool(CollectionState(multiworld), assumed)
    original_count = sum(location.can_reach(opening) for location in targets)
    lanes = defaultdict(list)
    for location in locations:
        lanes[location.player, _placement_category(location)].append(location)
    for lane in lanes.values():
        for first, second in combinations(lane, 2):
            previous = [first.item, second.item]
            if not any(item.advancement for item in previous):
                continue
            if not _items_obey_fill_rules(multiworld, [first, second], previous[::-1]):
                continue
            try:
                _assign_items([first, second], previous[::-1])
                _invalidate_native_source_player(multiworld, first.player)
                trial = sweep_native_pool(CollectionState(multiworld), assumed)
                expands = sum(location.can_reach(trial) for location in targets) > original_count
            finally:
                _assign_items([first, second], previous)
                _invalidate_native_source_player(multiworld, first.player)
            if expands:
                yield (first, second), previous[::-1]


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


def fill_solo_progression(world, progression, locations):
    from Fill import FillError, fill_restrictive, sweep_from_pool
    from .requirement_rules import _invalidate_native_source_player

    multiworld = world.multiworld
    if (multiworld.players != 1 or multiworld.groups
            or not progression
            or any(location.progress_type == LocationProgressType.PRIORITY for location in locations)):
        return
    available = [location for location in locations
                 if location.progress_type == LocationProgressType.DEFAULT]
    failure = None
    accepted = False

    attempted_normal = False
    opening_attempted = False

    def attempts():
        yield (), (), False
        yield (), (), False
        for changed, items in _opening_shuffle_swaps(
            multiworld, getattr(world, "_silksong_shuffle_locations", ()),
        ):
            yield changed, items, False
        from .display_names import FLEA_ITEM_NAMES

        if any(item.name in FLEA_ITEM_NAMES for item in progression):
            for changed, items in _opening_shuffle_swaps(
                multiworld, getattr(world, "_silksong_shuffle_locations", ()),
                assumed=[item for item in progression if item.name not in FLEA_ITEM_NAMES],
            ):
                yield changed, items, False
                for _ in range(2):
                    multiworld.random.shuffle(progression)
                    multiworld.random.shuffle(available)
                    yield changed, items, False
        for _ in range(4):
            multiworld.random.shuffle(progression)
            multiworld.random.shuffle(available)
            yield (), (), False

        yield (), (), True

    for changed, items, neutral_opening in attempts():
        previous = [location.item for location in changed]
        if changed:
            if not _items_obey_fill_rules(multiworld, changed, items):
                continue
            _assign_items(changed, items)
            _invalidate_native_source_player(multiworld, world.player)
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
                if changed:
                    _assign_items(changed, previous)
                    _invalidate_native_source_player(multiworld, world.player)
    if failure is not None:
        raise failure


def _validate_unrestricted_opening(multiworld):
    if multiworld.players != 1:
        return
    items = [item for item in multiworld.itempool
             if item.advancement and _placement_category(item) is None]
    if not items:
        return
    state = CollectionState(multiworld)
    for item in multiworld.itempool:
        if _placement_category(item) is not None:
            state.collect(item, True)
    for location in multiworld.get_filled_locations():
        if _placement_category(location) is not None:
            state.collect(location.item, True)
    state.sweep_for_advancements()
    if multiworld.has_beaten_game(state):
        return
    if any(location.can_reach(state) and any(
            location.can_fill(state, item, check_access=False) for item in items)
            for location in multiworld.get_unfilled_locations()):
        return
    raise OptionError(
        "The starting and entrance settings leave no reachable check that can hold "
        "unrestricted progression, even with all category-shuffled items available. "
        "Set an early check category to Anywhere, change the starting location, "
        "or provide a starting movement item."
    )


def _restore_reserved_filler(multiworld):
    for location in multiworld.get_filled_locations():
        item = location.item
        category = _placement_category(item)
        if (location.address is None or category is None or not item.excludable
                or (location.player == item.player and _placement_category(location) == category)):
            continue
        replacement_index = next((index for index, candidate in enumerate(multiworld.itempool)
                                  if _placement_category(candidate) is None and candidate.excludable
                                  and location.can_fill(multiworld.state, candidate, check_access=False)), None)
        if replacement_index is None:
            raise OptionError(
                f"{location} took a reserved {category} shuffle item during pre-fill, "
                "and no compatible filler remains to replace it."
            )
        replacement = multiworld.itempool[replacement_index]
        location.item = None
        item.location = None
        location.place_locked_item(replacement)
        multiworld.itempool[replacement_index] = item


def prefill_category_shuffles(
    multiworld,
    game_name: str,
) -> None:
    """Place shuffled Simple Keys before the global fill."""

    _restore_reserved_filler(multiworld)
    _validate_unrestricted_opening(multiworld)
    shuffled_items = [
        item
        for item in multiworld.itempool
        if _placement_category(item) is not None
    ]
    active_shuffled_locations = [
        location
        for location in (
            multiworld.get_locations()
            if callable(getattr(multiworld, "get_locations", None))
            else multiworld.get_unfilled_locations()
        )
        if _placement_category(location) is not None
    ]
    shuffled_locations = [
        location
        for location in multiworld.get_unfilled_locations()
        if _placement_category(location) is not None
    ]
    if not shuffled_items and not active_shuffled_locations:
        return

    items_by_lane: dict[tuple[str, int], list] = defaultdict(list)
    locations_by_lane: dict[tuple[str, int], list] = defaultdict(list)
    for item in shuffled_items:
        items_by_lane[(_placement_category(item), item.player)].append(item)
    for location in shuffled_locations:
        locations_by_lane[
            (_placement_category(location), location.player)
        ].append(location)

    lanes = sorted(set(items_by_lane) | set(locations_by_lane))
    for category, player in lanes:
        category_items = items_by_lane[(category, player)]
        category_locations = locations_by_lane[(category, player)]
        if len(category_items) != len(category_locations):
            raise ValueError(
                f"P{player} {category} shuffle has "
                f"{len(category_items)} items but "
                f"{len(category_locations)} available locations. Check "
                "plando, start_inventory_from_pool, Item Links and category "
                "settings for incompatible placements."
            )
        category_items.sort(key=lambda item: item.name)
        category_locations.sort(key=lambda location: location.name)

    planned_items_by_lane: dict[tuple[str, int], list] = {}
    for category, player in lanes:
        lane = (category, player)
        category_items = items_by_lane[lane]
        category_locations = locations_by_lane[lane]
        planned_items = _build_native_baseline(
            category,
            category_locations,
            category_items,
        )
        planned_items_by_lane[lane] = _match_items_to_locations(
            multiworld,
            category,
            category_locations,
            planned_items,
        )

    silksong_players = sorted(
        player
        for player in multiworld.player_ids
        if multiworld.worlds[player].game == game_name
    )

    for category, player in lanes:
        lane = (category, player)
        if not _items_obey_fill_rules(
            multiworld,
            locations_by_lane[lane],
            planned_items_by_lane[lane],
        ):
            raise ValueError(
                f"The P{player} {category} bootstrap layout conflicts with "
                "a location safety, exclusion or locality rule."
            )

    for lane in lanes:
        for location, item in zip(
            locations_by_lane[lane],
            planned_items_by_lane[lane],
        ):
            multiworld.push_item(location, item, False)
            location.locked = True

    for player in silksong_players:
        multiworld.worlds[player]._silksong_shuffle_locations = tuple(
            location for lane, locations in locations_by_lane.items() if lane[1] == player
            for location in locations
        )
    placed_item_ids = {id(item) for item in shuffled_items}
    multiworld.itempool[:] = [
        item
        for item in multiworld.itempool
        if id(item) not in placed_item_ids
    ]
    reachability_context = _build_shuffle_reachability_context(multiworld)

    all_shuffled_locations = active_shuffled_locations
    if not _shuffle_is_accessible(
        multiworld,
        all_shuffled_locations,
        silksong_players,
        reachability_context,
    ) and not _repair_shuffle_bootstrap(
        multiworld, all_shuffled_locations, silksong_players,
        [location for locations in locations_by_lane.values() for location in locations],
        reachability_context,
    ):
        unreachable_locations, unbeaten_players = (
            _shuffle_reachability_failures(
                multiworld,
                all_shuffled_locations,
                silksong_players,
                reachability_context,
            )
        )
        details = []
        if unreachable_locations:
            details.append(
                "Unreachable tagged locations: "
                + ", ".join(unreachable_locations)
                + "."
            )
        if unbeaten_players:
            details.append(
                "Unbeaten players: "
                + ", ".join(f"P{player}" for player in unbeaten_players)
                + "."
            )
        raise ValueError(
            "The safe category-shuffle baseline is not reachable. "
            + " ".join(details)
            + " "
            "This indicates a logic or plando conflict."
        )

    local_contexts = {}
    if (
        not getattr(multiworld, "groups", {})
        and all(location.item is None or location.item.player == location.player
                for location in reachability_context[1])
        and all(
            callable(getattr(multiworld.worlds[player], "get_regions", None))
            and all(exit.connected_region is None or exit.connected_region.player == player
                    for region in multiworld.worlds[player].get_regions()
                    for exit in region.exits)
            for player in silksong_players
        )
    ):
        for player in silksong_players:
            local_contexts[player] = (
                tuple(location for location in all_shuffled_locations if location.player == player),
                (player,),
                (reachability_context[0], tuple(location for location in reachability_context[1]
                                               if location.player == player)),
            )

    # Try a full permutation per lane. If it creates a progression cycle,
    # walk outward from the valid baseline through a handful of individually
    # validated swaps instead. Non-progression rewards can always permute
    # freely after progression positions are settled.
    for lane in lanes:
        check_locations, check_players, check_context = local_contexts.get(
            lane[1], (all_shuffled_locations, silksong_players, reachability_context)
        )
        locations = locations_by_lane[lane]
        if len(locations) < 2:
            continue

        original_items = [location.item for location in locations]
        if not any(item.advancement for item in original_items):
            for _attempt in range(4):
                randomized_items = list(original_items)
                multiworld.random.shuffle(randomized_items)
                if _items_obey_fill_rules(
                    multiworld,
                    locations,
                    randomized_items,
                ):
                    _assign_items(locations, randomized_items)
                    break
            continue

        randomized_items = list(original_items)
        multiworld.random.shuffle(randomized_items)
        accepted_full_shuffle = False
        if _items_obey_fill_rules(
            multiworld,
            locations,
            randomized_items,
        ):
            _assign_items(locations, randomized_items)
            accepted_full_shuffle = _shuffle_is_accessible(
                multiworld,
                check_locations,
                check_players,
                check_context,
            )
        if not accepted_full_shuffle:
            _assign_items(locations, original_items)
            attempts = min(12, max(4, len(locations)))
            for _attempt in range(attempts):
                first, second = multiworld.random.sample(locations, 2)
                if not (
                    _can_fill_without_access(
                        multiworld,
                        first,
                        second.item,
                    )
                    and _can_fill_without_access(
                        multiworld,
                        second,
                        first.item,
                    )
                ):
                    continue
                first.item, second.item = second.item, first.item
                first.item.location = first
                second.item.location = second
                if not _shuffle_is_accessible(
                    multiworld,
                    check_locations,
                    check_players,
                    check_context,
                ):
                    first.item, second.item = second.item, first.item
                    first.item.location = first
                    second.item.location = second

        non_progression_locations = [
            location
            for location in locations
            if not location.item.advancement
        ]
        if len(non_progression_locations) > 1:
            original_non_progression_items = [
                location.item
                for location in non_progression_locations
            ]
            for _attempt in range(4):
                non_progression_items = list(
                    original_non_progression_items
                )
                multiworld.random.shuffle(non_progression_items)
                if _items_obey_fill_rules(
                    multiworld,
                    non_progression_locations,
                    non_progression_items,
                ):
                    _assign_items(
                        non_progression_locations,
                        non_progression_items,
                    )
                    break

    if local_contexts and not _shuffle_is_accessible(
        multiworld, all_shuffled_locations, silksong_players, reachability_context,
    ):
        raise ValueError("Category shuffle failed its final multiworld accessibility check.")
