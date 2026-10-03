import heapq
import logging
import math

from ... import RaceRandom as random
from ...BaseClasses import Entrance, RegionType, Terrain
from .EntranceShuffle2 import connect_simple
from ...OWEdges import OWTileRegions
from ...DungeonGenerator import GenerationException

LARGE_SCREENS = frozenset({0x00, 0x03, 0x05, 0x18, 0x1b, 0x1e, 0x35})
PORTAL_OWIDS = frozenset({
    0x03, 0x05, 0x07, 0x10, 0x1b, 0x2f, 0x33, 0x35,
    0x43, 0x45, 0x47, 0x50, 0x6f, 0x73, 0x75,
})

# Graph distance costs
DIST_REGION_STEP = 0.1
DIST_OWID_HOP = 1.0
DIST_LARGE_EXIT = 1.0

# Coverage quality: typical walk, with a lighter worst-case term.
COVERAGE_MAX_WEIGHT = 0.3

# Heatmap: score every remaining candidate, then pick from the top pool.
# Higher attractiveness is more likely.
LAYER_WEIGHT_COVERAGE = 1.0
LAYER_WEIGHT_PORTAL = 0.25
LAYER_WEIGHT_NEIGHBOR = 0.5
NEIGHBOR_PENALTY_1 = 3.0
NEIGHBOR_PENALTY_2 = 1.0
PORTAL_BONUS = 1.0
PORTAL_NEIGHBOR_BONUS = 0.5
HEATMAP_POOL_SIZE = 6
HEATMAP_TEMPERATURE = 0.35
EXCLUDE_HOP1_FROM_POOL = True


def shuffle_flute_spots(world, player):
    def connect_flutes(flute_destinations):
        for o, owid in enumerate(flute_destinations):
            regions = flute_data[owid][0]
            if not world.is_tile_swapped(owid, player):
                connect_simple(world, 'Flute Spot ' + str(o + 1), regions[0], player)
            else:
                connect_simple(world, 'Flute Spot ' + str(o + 1), regions[1], player)

    if world.owFluteShuffle[player] == 'vanilla':
        flute_spots = default_flute_connections.copy()
        sort_flute_spots(world, player, flute_spots)
        world.owflutespots[player] = flute_spots
        connect_flutes(flute_spots)
        create_dynamic_flute_exits(world, player)
        return

    logger = logging.getLogger('')

    remaining_spots = 8
    flute_pool = list(flute_data.keys())
    new_spots = []
    forbidden_spots = set()
    forced_intents = []  # (owid, region_name)

    def flute_region_name(owid):
        return flute_data[owid][0][1 if world.is_tile_swapped(owid, player) else 0]

    def place(owid, candidates=None, forced=False):
        if owid not in flute_pool:
            logger.warning(f'Warning: Attempted to place flute spot not in pool: {hex(owid)}')
            return False
        flute_pool.remove(owid)
        logger.debug(f'Placing flute at: {hex(owid)}')
        new_spots.append(owid)
        if candidates is not None and owid in candidates:
            candidates.remove(owid)
        return True

    if world.customizer:
        custom_spots = world.customizer.get_owflutespots()
        if custom_spots and player in custom_spots:
            if 'forbid' in custom_spots[player]:
                for spot_id in custom_spots[player]['forbid']:
                    owid = spot_id & 0xBF
                    if owid in flute_data:
                        forbidden_spots.add(owid)
                        if owid in flute_pool:
                            flute_pool.remove(owid)
            if 'force' in custom_spots[player]:
                for spot_id in custom_spots[player]['force']:
                    owid = spot_id & 0xBF
                    if owid not in flute_data:
                        logger.warning(f'Invalid flute spot in customizer: {hex(owid)}')
                        continue
                    if owid in forbidden_spots:
                        logger.warning(f'Forced flute spot is also forbidden: {hex(owid)}')
                        continue
                    forced_intents.append((owid, flute_region_name(owid)))

    portal_neighbors = _compute_portal_neighbors(world, player)
    debug = FluteDebugLog(world, player, logger=logger)

    # Same sector partition and quota inputs as FluteShuffle: candidate regions only
    # for allocation, with the full sector region list kept for coverage distances.
    flute_regions = {
        (f[0][0] if (o not in world.owswaps[player][0]) != (world.mode[player] == 'inverted') else f[0][1]): o
        for o, f in flute_data.items()
        if o not in forbidden_spots
    }
    flute_sectors = []
    for sector_groups in world.owsectors[player]:
        all_regions = [r for group in sector_groups for r in group]
        candidate_regions = [r for r in all_regions if r in flute_regions]
        if candidate_regions:
            flute_sectors.append((len(all_regions), candidate_regions, all_regions))

    region_total = sum(count for count, _, _ in flute_sectors)
    sector_total = len(flute_sectors)
    sector_has_spot = []
    empty_sector_total = 0
    forced_region_names = {region for _, region in forced_intents}

    for _, candidate_regions, _ in flute_sectors:
        already_has_spot = any(region in candidate_regions for region in forced_region_names)
        sector_has_spot.append(already_has_spot)
        if not already_has_spot:
            empty_sector_total += 1

    if remaining_spots < empty_sector_total:
        logger.warning('Warning: Not every sector can have a flute spot, generation might fail')
        for i in range(len(flute_sectors)):
            if not sector_has_spot[i]:
                sector_has_spot[i] = True
                empty_sector_total -= 1
                if remaining_spots == empty_sector_total:
                    break

    for i, (sector_count, candidate_regions, all_regions) in enumerate(flute_sectors):
        sector_total -= 1
        if not sector_has_spot[i]:
            empty_sector_total -= 1
        spots_to_place = min(
            remaining_spots - empty_sector_total,
            max(0 if sector_has_spot[i] else 1, round((sector_count * (remaining_spots - sector_total) / region_total) + 0.5)),
        )
        spots_to_place = max(0, spots_to_place)
        target_spots = len(new_spots) + spots_to_place
        logger.debug(f'Sector of {sector_count} regions gets {spots_to_place} spot(s)')
        debug.log(f'Sector regions={sector_count} candidates={len(candidate_regions)} allocated={spots_to_place}')

        placed_before = len(new_spots)
        sector_candidate_set = set(candidate_regions)

        if (0x30 in flute_pool and 0x30 not in forbidden_spots and len(new_spots) < target_spots
                and ('Desert Teleporter Ledge' in candidate_regions or 'Mire Teleporter Ledge' in candidate_regions)):
            place(0x30, forced=True)

        for owid, region in forced_intents:
            if region in sector_candidate_set and owid in flute_pool:
                place(owid, forced=True)

        candidates = []
        seen_owids = set()
        for region in candidate_regions:
            owid = flute_regions.get(region)
            if owid is not None and owid in flute_pool and owid not in seen_owids:
                seen_owids.add(owid)
                candidates.append(owid)

        if world.owFluteShuffle[player] == 'balanced':
            _place_balanced_spots(
                world, player, candidates, new_spots, target_spots, all_regions,
                portal_neighbors, debug, place,
            )
        else:
            _place_random_spots(candidate_regions, flute_regions, new_spots, forbidden_spots, target_spots, place)

        remaining_spots -= (len(new_spots) - placed_before)
        region_total -= sector_count

    for owid, _region in forced_intents:
        if owid in flute_pool:
            place(owid, forced=True)

    sort_flute_spots(world, player, new_spots)
    world.owflutespots[player] = new_spots
    connect_flutes(new_spots)
    debug.write()
    _write_spoiler_map(world, player, new_spots)
    create_dynamic_flute_exits(world, player)


def _place_random_spots(candidate_regions, flute_regions, new_spots, forbidden_spots, target_spots, place):
    order = list(candidate_regions)
    random.shuffle(order)
    f = 0
    t = 0
    while len(new_spots) < target_spots:
        if f >= len(order):
            f = 0
            t += 1
            if t > 5:
                raise GenerationException('Infinite loop detected in flute shuffle')
        owid = flute_regions[order[f]]
        if owid not in new_spots and owid not in forbidden_spots:
            place(owid)
        f += 1


def _place_balanced_spots(world, player, candidates, new_spots, target_spots, all_regions, portal_neighbors, debug, place):
    if not candidates or len(new_spots) >= target_spots:
        return

    coverage = _CoverageIndex(world, player, all_regions)
    owid_neighbors = {}

    while len(new_spots) < target_spots and candidates:
        placed_in_sector = [owid for owid in new_spots if coverage.has_start(owid)]
        field = coverage.combined(placed_in_sector)
        heat = _score_all_candidates(coverage, candidates, placed_in_sector, field, portal_neighbors, owid_neighbors, world, player)

        debug.log(f"Placed={[hex(o) for o in new_spots]} remaining={target_spots - len(new_spots)}")
        debug.print_map(coverage.region_owid_scores(field), set(new_spots), 'Coverage field (dist to nearest placed):')
        debug.print_map({owid: heat.get(owid, 0.0) for owid in flute_data}, set(new_spots), 'Heatmap attractiveness:')

        pool = _heatmap_pool(candidates, placed_in_sector, heat, owid_neighbors, world, player)
        if not pool:
            pick = random.choice(candidates)
            debug.log(f'Empty heatmap pool, fallback pick: {hex(pick)}')
            place(pick, candidates)
            continue

        pick, pool_weights = _weighted_heatmap_pick(pool, heat)
        debug.log(f"Heatmap pool: {', '.join(f'{hex(o)}={w:.3f}' for o, w in pool_weights)}")
        debug.log(f'Picked: {hex(pick)}')
        place(pick, candidates)


def _coverage_improvement(coverage, field, owid):
    current = coverage.score(field)
    added = coverage.score(coverage.merge_onto(field, (owid,)))
    current_metric = current[1]
    added_metric = added[1]
    if current_metric == math.inf and added_metric == math.inf:
        return 0.0
    if current_metric == math.inf:
        return 1.0 / (1.0 + added_metric)
    return current_metric - added_metric


def _portal_bonus(owid, portal_neighbors):
    if owid in PORTAL_OWIDS:
        return PORTAL_BONUS
    if owid in portal_neighbors:
        return PORTAL_NEIGHBOR_BONUS
    return 0.0


def _neighbor_penalty(owid, placed_spots, owid_neighbors, world, player):
    penalty = 0.0
    closest = None
    for placed in placed_spots:
        hop = _owid_hop_distance(owid, placed, owid_neighbors, world, player)
        if hop is None:
            continue
        if closest is None or hop < closest:
            closest = hop
        if hop == 1:
            penalty += NEIGHBOR_PENALTY_1
        elif hop == 2:
            penalty += NEIGHBOR_PENALTY_2
    return penalty, closest


def _score_all_candidates(coverage, candidates, placed_spots, field, portal_neighbors, owid_neighbors, world, player):
    raw_improve = {}
    raw_portal = {}
    raw_neighbor = {}
    for owid in candidates:
        raw_improve[owid] = _coverage_improvement(coverage, field, owid)
        raw_portal[owid] = _portal_bonus(owid, portal_neighbors)
        penalty, _closest = _neighbor_penalty(owid, placed_spots, owid_neighbors, world, player)
        raw_neighbor[owid] = penalty

    improve_vals = list(raw_improve.values())
    min_imp = min(improve_vals)
    max_imp = max(improve_vals)
    spread = max_imp - min_imp

    heat = {}
    for owid in candidates:
        if spread > 1e-9:
            coverage_layer = (raw_improve[owid] - min_imp) / spread
        else:
            coverage_layer = 0.5
        heat[owid] = (
            LAYER_WEIGHT_COVERAGE * coverage_layer
            + LAYER_WEIGHT_PORTAL * raw_portal[owid]
            - LAYER_WEIGHT_NEIGHBOR * raw_neighbor[owid]
        )
    return heat


def _heatmap_pool(candidates, placed_spots, heat, owid_neighbors, world, player):
    ranked = sorted(candidates, key=lambda owid: heat.get(owid, float('-inf')), reverse=True)
    if EXCLUDE_HOP1_FROM_POOL and placed_spots:
        filtered = []
        for owid in ranked:
            _penalty, closest = _neighbor_penalty(owid, placed_spots, owid_neighbors, world, player)
            if closest == 1:
                continue
            filtered.append(owid)
        if filtered:
            ranked = filtered
    return ranked[:max(1, min(HEATMAP_POOL_SIZE, len(ranked)))]


def _weighted_heatmap_pick(pool, heat):
    scores = [heat.get(owid, 0.0) for owid in pool]
    max_score = max(scores)
    weights = [math.exp((score - max_score) / HEATMAP_TEMPERATURE) for score in scores]
    total = sum(weights)
    if total <= 0:
        pick = random.choice(list(pool))
        return pick, [(owid, 0.0) for owid in pool]
    pick = random.choices(list(pool), weights=weights, k=1)[0]
    return pick, [(owid, weight / total) for owid, weight in zip(pool, weights)]


class _CoverageIndex:
    def __init__(self, world, player, sector_regions):
        self.world = world
        self.player = player
        self.region_names = list(sector_regions)
        self.region_index = {name: i for i, name in enumerate(self.region_names)}
        self.graph = _build_sector_graph(world, player, self.region_names)
        self._profiles = {}
        self._inf = [math.inf] * len(self.region_names)
        # Score barren *screens*, not raw region count. Kak/Castle/Lake have many
        # subregions and were pulling spots into already-dense areas.
        self.owid_groups = {}
        for i, name in enumerate(self.region_names):
            owid = OWTileRegions.get(name)
            key = owid if owid is not None else ('region', name)
            self.owid_groups.setdefault(key, []).append(i)

    def flute_start(self, owid):
        return flute_data[owid][0][1 if self.world.is_tile_swapped(owid, self.player) else 0]

    def has_start(self, owid):
        return self.flute_start(owid) in self.region_index

    def profile(self, owid):
        cached = self._profiles.get(owid)
        if cached is not None:
            return cached
        start = self.flute_start(owid)
        start_i = self.region_index.get(start)
        if start_i is None:
            self._profiles[owid] = list(self._inf)
            return self._profiles[owid]
        self._profiles[owid] = _dijkstra(self.graph, start_i, len(self.region_names))
        return self._profiles[owid]

    def combined(self, owids):
        merged = list(self._inf)
        return self.merge_onto(merged, owids)

    def merge_onto(self, base, owids):
        merged = list(base)
        for owid in owids:
            prof = self.profile(owid)
            for i, dist in enumerate(prof):
                if dist < merged[i]:
                    merged[i] = dist
        return merged

    def score(self, combined):
        uncovered = 0
        total = 0.0
        max_d = 0.0
        covered = 0
        for indexes in self.owid_groups.values():
            best = math.inf
            for i in indexes:
                if combined[i] < best:
                    best = combined[i]
            if best == math.inf:
                uncovered += 1
            else:
                covered += 1
                total += best
                if best > max_d:
                    max_d = best
        if not covered:
            return (uncovered, math.inf, math.inf, math.inf)
        avg = total / covered
        metric = avg + COVERAGE_MAX_WEIGHT * max_d
        return (uncovered, metric, avg, max_d)

    def worst_area_index(self, combined):
        worst_key = None
        worst_i = 0
        for indexes in self.owid_groups.values():
            best_i = indexes[0]
            best = combined[best_i]
            for i in indexes[1:]:
                if combined[i] < best:
                    best = combined[i]
                    best_i = i
            key = math.inf if best == math.inf else best
            if worst_key is None or key > worst_key:
                worst_key = key
                worst_i = best_i
        return worst_i

    def owid_distance(self, owid, combined):
        start = self.flute_start(owid)
        idx = self.region_index.get(start)
        if idx is not None:
            return combined[idx]
        for name in flute_data[owid][0]:
            idx = self.region_index.get(name)
            if idx is not None:
                return combined[idx]
        return math.inf

    def region_owid_scores(self, combined):
        scores = {}
        for owid in flute_data:
            scores[owid] = self.owid_distance(owid, combined)
        return scores


def _build_sector_graph(world, player, region_names):
    sector_set = set(region_names)
    index = {name: i for i, name in enumerate(region_names)}
    graph = [[] for _ in region_names]
    for name in region_names:
        src_i = index[name]
        src_owid = OWTileRegions.get(name)
        region = world.get_region(name, player)
        if region is None or src_owid is None:
            continue
        for exit in region.exits:
            dest = exit.connected_region
            if dest is None or dest.name not in sector_set:
                continue
            dst_owid = OWTileRegions.get(dest.name)
            if dst_owid is None:
                continue
            if src_owid == dst_owid:
                cost = DIST_REGION_STEP
            else:
                cost = DIST_OWID_HOP
                if (dst_owid & 0x3F) in LARGE_SCREENS:
                    cost += DIST_LARGE_EXIT
            graph[src_i].append((index[dest.name], cost))
    return graph


def _dijkstra(graph, start_i, node_count):
    dist = [math.inf] * node_count
    dist[start_i] = 0.0
    heap = [(0.0, start_i)]
    while heap:
        current, node = heapq.heappop(heap)
        if current > dist[node]:
            continue
        for nbr, cost in graph[node]:
            candidate = current + cost
            if candidate < dist[nbr]:
                dist[nbr] = candidate
                heapq.heappush(heap, (candidate, nbr))
    return dist


def _get_adjacent_owids(owid, cache, world, player):
    cached = cache.get(owid)
    if cached is not None:
        return cached
    region_names = OWTileRegions.inverse.get(owid) or []
    pending = list(region_names)
    visited = set(pending)
    neighbors = set()
    while pending:
        region_name = pending.pop()
        region = world.get_region(region_name, player)
        if region is None:
            continue
        for entrance in region.entrances:
            parent = entrance.parent_region
            if parent is None or parent.name not in OWTileRegions:
                continue
            parent_owid = OWTileRegions[parent.name]
            if parent_owid == owid:
                if parent.name not in visited:
                    visited.add(parent.name)
                    pending.append(parent.name)
            else:
                neighbors.add(parent_owid)
    cache[owid] = neighbors
    return neighbors


def _owid_hop_distance(start_owid, target_owid, cache, world, player, max_depth=2):
    if start_owid == target_owid:
        return 0
    visited = {start_owid}
    frontier = {start_owid}
    depth = 0
    while frontier and depth < max_depth:
        depth += 1
        next_frontier = set()
        for current in frontier:
            for neighbor in _get_adjacent_owids(current, cache, world, player):
                if neighbor == target_owid:
                    return depth
                if neighbor not in visited:
                    visited.add(neighbor)
                    next_frontier.add(neighbor)
        frontier = next_frontier
    return None


def _compute_portal_neighbors(world, player):
    neighbors = set()
    cache = {}
    for owid in PORTAL_OWIDS:
        for parent_owid in _get_adjacent_owids(owid, cache, world, player):
            if parent_owid not in PORTAL_OWIDS:
                neighbors.add(parent_owid)
    return neighbors


class FluteDebugLog:
    def __init__(self, world, player, logger=None):
        self.enabled = world.owFluteShuffle[player] == 'balanced' and (logger and logger.isEnabledFor(logging.DEBUG))
        self.lines = []
        self.grid = None
        if self.enabled and hasattr(world, 'spoiler') and hasattr(world.spoiler, 'maps'):
            entry = world.spoiler.maps.get(('layout_grid_lw', player))
            if entry:
                self.grid = entry.get('data')
                text = entry.get('text')
                if text:
                    self.log('Light World Layout:')
                    self.log('')
                    for line in text.rstrip().splitlines():
                        self.log(line)
                    self.log('')

    def log(self, line=''):
        if self.enabled:
            self.lines.append(line)

    def write(self):
        if self.enabled:
            with open('flute_debug.txt', 'w', encoding='utf-8') as debug_file:
                debug_file.write('\n'.join(self.lines) + '\n')

    def print_map(self, score_map, placed_spots, title):
        if not self.enabled or not self.grid:
            return
        large_screen_ids = [0x00, 0x03, 0x05, 0x18, 0x1B, 0x1E, 0x30, 0x35, 0x40, 0x43, 0x45, 0x58, 0x5B, 0x5E, 0x70, 0x75]
        grid = self.grid
        cell_width = 4

        def is_same_large_screen(row1, col1, row2, col2):
            id1 = grid[row1 % 8][col1 % 8]
            id2 = grid[row2 % 8][col2 % 8]
            if id1 == -1 or id2 == -1:
                return False
            return id1 == id2 and id1 in large_screen_ids

        self.log(title)
        header = '      '
        for col in range(8):
            header += f' {col:^{cell_width}}'
        self.log(header)

        for row in range(8):
            border_line = '     +'
            for col in range(8):
                if row > 0 and is_same_large_screen(row, col, row - 1, col):
                    border_line += ' ' * cell_width
                else:
                    border_line += '-' * cell_width
                if col < 7:
                    has_horizontal_left = row == 0 or not is_same_large_screen(row, col, row - 1, col)
                    has_horizontal_right = row == 0 or not is_same_large_screen(row, col + 1, row - 1, col + 1)
                    has_vertical_top = row == 0 or not is_same_large_screen(row - 1, col, row - 1, col + 1)
                    has_vertical_bottom = not is_same_large_screen(row, col, row, col + 1)
                    if has_vertical_bottom or has_vertical_top:
                        border_line += '+' if (has_horizontal_left or has_horizontal_right) else '|'
                    else:
                        border_line += '-' if (has_horizontal_left or has_horizontal_right) else ' '
                else:
                    border_line += '+'
            self.log(border_line)

            row_name = 'ABCDEFGH'[row]
            content_line = f'{row_name}({row * 8:02X})|'
            for col in range(8):
                screen_id = grid[row][col]
                if screen_id == -1:
                    cell = ' ' * cell_width
                else:
                    owid = screen_id & 0xBF
                    value = score_map.get(owid)
                    if value is None:
                        cell = ' ' * (cell_width - 2) + '--'
                    elif value == math.inf:
                        text = ' inf'
                        if owid in placed_spots:
                            text = '*' + text[1:]
                        cell = text
                    else:
                        text = f'{value:.1f}'.rjust(cell_width)
                        if owid in placed_spots:
                            text = '*' + text[1:]
                        cell = text
                content_line += cell
                if col < 7:
                    content_line += '|' if not is_same_large_screen(row, col, row, col + 1) else ' '
                else:
                    content_line += '|'
            self.log(content_line)

        bottom_border = '     +'
        for col in range(8):
            bottom_border += '-' * cell_width
            if col < 7:
                bottom_border += '-' if is_same_large_screen(7, col, 7, col + 1) else '+'
            else:
                bottom_border += '+'
        self.log(bottom_border)


def _write_spoiler_map(world, player, new_spots):
    s = list(map(lambda x: ' ' if x not in new_spots else 'F', [i for i in range(0x40)]))
    text_output = flute_spoiler_table.replace('s', '%s') % (
                                 s[0x02],                                s[0x07],
                                                     s[0x00],                s[0x03],        s[0x05],
        s[0x00],        s[0x02],s[0x03],        s[0x05],        s[0x07],                 s[0x0a],                                s[0x0f],
                        s[0x0a],                                s[0x0f],
        s[0x10],s[0x11],s[0x12],s[0x13],s[0x14],s[0x15],s[0x16],s[0x17], s[0x10],s[0x11],s[0x12],s[0x13],s[0x14],s[0x15],s[0x16],s[0x17],
        s[0x18],        s[0x1a],s[0x1b],        s[0x1d],s[0x1e],
                        s[0x22],                s[0x25],                                 s[0x1a],                s[0x1d],
        s[0x28],s[0x29],s[0x2a],s[0x2b],s[0x2c],s[0x2d],s[0x2e],s[0x2f],     s[0x18],                s[0x1b],                s[0x1e],
        s[0x30],        s[0x32],s[0x33],s[0x34],s[0x35],        s[0x37],                 s[0x22],                s[0x25],
                        s[0x3a],s[0x3b],s[0x3c],                s[0x3f],
                                                                     s[0x28],s[0x29],s[0x2a],s[0x2b],s[0x2c],s[0x2d],s[0x2e],s[0x2f],
                                                                                     s[0x32],s[0x33],s[0x34],                s[0x37],
                                                         s[0x30],                                s[0x35],
                                                                                     s[0x3a],s[0x3b],s[0x3c],                s[0x3f])
    world.spoiler.set_map('flute', text_output, new_spots, player)


def sort_flute_spots(world, player, flute_spots):
    if world.owLayout[player] != 'grid':
        flute_spots.sort(key=lambda id: flute_data[id][1] if id != 0x03 or not world.is_tile_swapped(0x03, player) else 0x04)
    else:
        world_layout = world.owgrid[player][0] if world.mode[player] != 'inverted' else world.owgrid[player][1]
        layout_list = sum(world_layout, [])
        layout_map = {id & 0xBF: i for i, id in enumerate(layout_list)}
        flute_spots.sort(key=lambda id: layout_map[flute_data[id][1] if id != 0x03 or not world.is_tile_swapped(0x03, player) else 0x04])


def create_dynamic_flute_exits(world, player):
    flute_in_pool = True if player not in world.customitemarray else any(i for i, n in world.customitemarray[player].items() if i == 'flute' and n > 0)
    if not flute_in_pool:
        return
    for region in (r for r in world.regions if r.player == player and r.terrain == Terrain.Land and r.name not in ['Zoras Domain', 'Master Sword Meadow', 'Hobo Bridge']):
        if region.type == (RegionType.LightWorld if world.mode[player] != 'inverted' else RegionType.DarkWorld):
            exitname = 'Flute From ' + region.name
            exit = Entrance(region.player, exitname, region)
            exit.spot_type = 'Flute'
            exit.connect(world.get_region('Flute Sky', player))
            region.exits.append(exit)
    world.initialize_regions()


default_flute_connections = [
    0x03, 0x16, 0x18, 0x2c, 0x2f, 0x30, 0x3b, 0x3f
]

flute_data = {
    #OWID    LW Region                         DW Region                            Slot   VRAM    BG Y    BG X   Link Y  Link X   Cam Y   Cam X   Unk1    Unk2   IconY   IconX    AltY    AltX  AltVRAM  AltBGY  AltBGX  AltCamY AltCamX AltUnk1 AltUnk2 AltIconY AltIconX
    0x00: (['Lost Woods East Area',           'Skull Woods Forest'],                0x09, 0x1042, 0x022e, 0x0202, 0x0290, 0x0288, 0x029b, 0x028f, 0xfff2, 0x000e, 0x0290, 0x0288, 0x0290, 0x0290),
    0x02: (['Lumberjack Area',                'Dark Lumberjack Area'],              0x02, 0x059c, 0x00d6, 0x04e6, 0x0138, 0x0558, 0x0143, 0x0563, 0xfffa, 0xfffa, 0x01d8, 0x0518),
    0x03: (['West Death Mountain (Bottom)',   'West Dark Death Mountain (Top)'],    0x0b, 0x1600, 0x02ca, 0x060e, 0x0328, 0x0678, 0x0337, 0x0683, 0xfff6, 0xfff2, 0x03bb, 0x0680, 0x0118, 0x0860, 0x05c0, 0x00b8, 0x07ec, 0x0127, 0x086b, 0xfff8, 0x0004, 0x0148, 0x0850),
    0x05: (['East Death Mountain (Bottom)',   'East Dark Death Mountain (Bottom)'], 0x0e, 0x1860, 0x031e, 0x0d00, 0x0388, 0x0da8, 0x038d, 0x0d7d, 0x0000, 0x0000, 0x03c8, 0x0d98),
    0x07: (['Death Mountain TR Pegs Area',    'Turtle Rock Area'],                  0x07, 0x0804, 0x0102, 0x0e1a, 0x0160, 0x0e90, 0x016f, 0x0e97, 0xfffe, 0x0006, 0x0150, 0x0ea0),
    0x0a: (['Mountain Pass Area',             'Bumper Cave Area'],                  0x0a, 0x0180, 0x0220, 0x0406, 0x0280, 0x0488, 0x028f, 0x0493, 0x0000, 0xfffa, 0x0390, 0x04d8),
    0x0f: (['Zora Waterfall Area',            'Catfish Area'],                      0x0f, 0x0316, 0x025c, 0x0eb2, 0x02c0, 0x0f28, 0x02cb, 0x0f2f, 0x0002, 0xfffe, 0x0360, 0x0f58),
    0x10: (['Lost Woods Pass West Area',      'Skull Woods Pass West Area'],        0x10, 0x0080, 0x0400, 0x0000, 0x0448, 0x0058, 0x046f, 0x0085, 0x0000, 0x0000, 0x04f8, 0x0088),
    0x11: (['Kakariko Fortune Area',          'Dark Fortune Area'],                 0x11, 0x0912, 0x051e, 0x0292, 0x0588, 0x0318, 0x058d, 0x031f, 0x0000, 0xfffe, 0x05f8, 0x0318),
    0x12: (['Kakariko Pond Area',             'Outcast Pond Area'],                 0x12, 0x0890, 0x051a, 0x0476, 0x0578, 0x04f8, 0x0587, 0x0503, 0xfff6, 0x000a, 0x05b8, 0x04f8),
    0x13: (['Sanctuary Area',                 'Dark Chapel Area'],                  0x13, 0x051c, 0x04aa, 0x06de, 0x0508, 0x0758, 0x0517, 0x0763, 0xfff6, 0x0002, 0x05b8, 0x0738),
    0x14: (['Graveyard Area',                 'Dark Graveyard Area'],               0x14, 0x089c, 0x051e, 0x08e6, 0x0580, 0x0958, 0x058b, 0x0963, 0x0000, 0xfffa, 0x05f0, 0x0918, 0x0580, 0x0948),
    0x15: (['River Bend East Bank',           'Qirn Jump East Bank'],               0x15, 0x041a, 0x0486, 0x0ad2, 0x04e8, 0x0b48, 0x04f3, 0x0b4f, 0x0008, 0xfffe, 0x0548, 0x0b78),
    0x16: (['Potion Shop Area',               'Dark Witch Area'],                   0x16, 0x0888, 0x0516, 0x0c4e, 0x0578, 0x0cc8, 0x0583, 0x0cd3, 0xfffa, 0xfff2, 0x05e8, 0x0c9f),
    0x17: (['Zora Approach Ledge',            'Catfish Approach Ledge'],            0x17, 0x039e, 0x047e, 0x0ef2, 0x04e0, 0x0f68, 0x04eb, 0x0f6f, 0x0000, 0xfffe, 0x0580, 0x0f48),
    0x18: (['Kakariko Village',               'Village of Outcasts'],               0x18, 0x0b30, 0x0759, 0x017e, 0x07b7, 0x0200, 0x07c6, 0x020b, 0x0007, 0x0002, 0x0830, 0x0240, 0x07c8, 0x01f8),
    0x1a: (['Forgotten Forest Area',          'Shield Shop Fence'],                 0x1a, 0x081a, 0x070f, 0x04d2, 0x0770, 0x0548, 0x077c, 0x054f, 0xffff, 0xfffe, 0x0770, 0x0518),
    0x1b: (['Hyrule Castle Courtyard',        'Pyramid Area'],                      0x1b, 0x0c30, 0x077a, 0x0786, 0x07d8, 0x07f8, 0x07e7, 0x0803, 0x0006, 0xfffa, 0x07f8, 0x07f8),
    0x1d: (['Wooden Bridge Area',             'Broken Bridge Northeast'],           0x1d, 0x0602, 0x06c2, 0x0a0e, 0x0720, 0x0a80, 0x072f, 0x0a8b, 0xfffe, 0x0002, 0x0750, 0x0a70),
    0x1e: (['Eastern Palace Area',            'Palace of Darkness Area'],           0x26, 0x1802, 0x091e, 0x0c0e, 0x09c0, 0x0c80, 0x098b, 0x0c8b, 0x0000, 0x0002, 0x09a0, 0x0cb0),
    0x22: (['Blacksmith Area',                'Hammer Pegs Area'],                  0x22, 0x058c, 0x08aa, 0x0462, 0x0908, 0x04d8, 0x0917, 0x04df, 0x0006, 0xfffe, 0x0978, 0x04e8),
    0x25: (['Sand Dunes Area',                'Dark Dunes Area'],                   0x25, 0x030e, 0x085a, 0x0a76, 0x08b8, 0x0ae8, 0x08c7, 0x0af3, 0x0006, 0xfffa, 0x0918, 0x0b18),
    0x28: (['Maze Race Area',                 'Dig Game Area'],                     0x28, 0x0908, 0x0b1e, 0x003a, 0x0b88, 0x00b8, 0x0b8d, 0x00bf, 0x0000, 0x0006, 0x0ba8, 0x00b8),
    0x29: (['Kakariko Suburb Area',           'Frog Area'],                         0x29, 0x0408, 0x0a7c, 0x0242, 0x0ae0, 0x02c0, 0x0aeb, 0x02c7, 0x0002, 0xfffe, 0x0b30, 0x02e0),
    0x2a: (['Flute Boy Area',                 'Stumpy Area'],                       0x2a, 0x058e, 0x0aac, 0x046e, 0x0b10, 0x04e8, 0x0b1b, 0x04f3, 0x0002, 0x0002, 0x0b60, 0x04f8),
    0x2b: (['Central Bonk Rocks Area',        'Dark Bonk Rocks Area'],              0x2b, 0x0620, 0x0acc, 0x0700, 0x0b30, 0x0790, 0x0b3b, 0x0785, 0xfff2, 0x0000, 0x0b80, 0x0760),
    0x2c: (['Links House Area',               'Big Bomb Shop Area'],                0x2c, 0x0588, 0x0ab9, 0x0840, 0x0b17, 0x08b8, 0x0b26, 0x08bf, 0xfff7, 0x0000, 0x0bb0, 0x08a8),
    0x2d: (['Stone Bridge South Area',        'Hammer Bridge South Area'],          0x2d, 0x0886, 0x0b1e, 0x0a2a, 0x0ba0, 0x0aa8, 0x0b8b, 0x0aaf, 0x0000, 0x0006, 0x0bf0, 0x0ab8),
    0x2e: (['Tree Line Area',                 'Dark Tree Line Area'],               0x2e, 0x0100, 0x0a1a, 0x0c00, 0x0a78, 0x0c30, 0x0a87, 0x0c7d, 0x0006, 0x0000, 0x0ac8, 0x0c70),
    0x2f: (['Eastern Nook Area',              'Darkness Nook Area'],                0x2f, 0x0798, 0x0afa, 0x0eb2, 0x0b58, 0x0f30, 0x0b67, 0x0f37, 0xfff6, 0x000e, 0x0bc0, 0x0f00),
    0x30: (['Desert Teleporter Ledge',        'Mire Teleporter Ledge'],             0x38, 0x1880, 0x0f1e, 0x0000, 0x0fa8, 0x0078, 0x0f8d, 0x008d, 0x0000, 0x0000, 0x0ff0, 0x0070),
    0x32: (['Flute Boy Approach Area',        'Stumpy Approach Area'],              0x32, 0x03a0, 0x0c6c, 0x0500, 0x0cd0, 0x05a8, 0x0cdb, 0x0585, 0x0002, 0x0000, 0x0d00, 0x0528),
    0x33: (['C Whirlpool Outer Area',         'Dark C Whirlpool Outer Area'],       0x33, 0x0180, 0x0c20, 0x0600, 0x0c80, 0x0628, 0x0c8f, 0x067d, 0x0000, 0x0000, 0x0ce0, 0x0688),
    0x34: (['Statues Area',                   'Hype Cave Area'],                    0x34, 0x088e, 0x0d00, 0x0866, 0x0d60, 0x08d8, 0x0d6f, 0x08e3, 0x0000, 0x000a, 0x0dd0, 0x08e8),
    #0x35: (['Lake Hylia Northwest Bank',      'Ice Lake Northwest Bank'],           0x35, 0x0d00, 0x0da6, 0x0a06, 0x0e08, 0x0a80, 0x0e13, 0x0a8b, 0xfffa, 0xfffa, 0x0dc8, 0x0a90),
    0x35: (['Lake Hylia South Shore',         'Ice Lake Southeast Ledge'],          0x3e, 0x1860, 0x0f1e, 0x0d00, 0x0f98, 0x0da8, 0x0f8b, 0x0d85, 0x0000, 0x0000, 0x0fd8, 0x0da8),
    0x37: (['Ice Cave Area',                  'Shopping Mall Area'],                0x37, 0x0786, 0x0cf6, 0x0e2e, 0x0d58, 0x0ea0, 0x0d63, 0x0eab, 0x000a, 0x0002, 0x0d98, 0x0ed0),
    0x3a: (['Desert Pass Area',               'Swamp Nook Area'],                   0x3a, 0x001a, 0x0e08, 0x04c6, 0x0e70, 0x0540, 0x0e7d, 0x054b, 0x0006, 0x000a, 0x0ee0, 0x0570),
    0x3b: (['Dam Area',                       'Swamp Area'],                        0x3b, 0x069e, 0x0edf, 0x06f2, 0x0f3d, 0x0778, 0x0f4c, 0x077f, 0xfff1, 0xfffe, 0x0fd0, 0x0770),
    0x3c: (['South Pass Area',                'Dark South Pass Area'],              0x3c, 0x0584, 0x0ed0, 0x081e, 0x0f38, 0x0898, 0x0f45, 0x08a3, 0xfffe, 0x0002, 0x0fa8, 0x0898),
    0x3f: (['Octoballoon Area',               'Bomber Corner Area'],                0x3f, 0x0810, 0x0f05, 0x0e75, 0x0f67, 0x0ef3, 0x0f72, 0x0efa, 0xfffb, 0x000b, 0x0fd0, 0x0ef0)
}

flute_spoiler_table = \
"""                       0 1 2 3 4 5 6 7
                      +---+-+---+---+-+
      01234567   A(00)|   |s|   |   |s|
     +--------+       | s +-+ s | s +-+
A(00)|s ss s s|  B(08)|   |s|   |   |s|
B(08)|  s    s|       +-+-+-+-+-+-+-+-+
C(10)|ssssssss|  C(10)|s|s|s|s|s|s|s|s|
D(18)|s ss ss |       +-+-+-+-+-+-+-+-+
E(20)|  s  s  |  D(18)|   |s|   |s|   |
F(28)|ssssssss|       | s +-+ s +-+ s |
G(30)|s ssss s|  E(20)|   |s|   |s|   |
H(38)|  sss  s|       +-+-+-+-+-+-+-+-+
     +--------+  F(28)|s|s|s|s|s|s|s|s|
                      +-+-+-+-+-+-+-+-+
                 G(30)|   |s|s|s|   |s|
                      | s +-+-+-+ s +-+
                 H(38)|   |s|s|s|   |s|
                      +---+-+-+-+---+-+"""

