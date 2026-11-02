"""build a compact, current-world walking table from received course unlocks"""

from collections import deque
from .MapData import COURSES, PATHS, PATH_IDS, POSITIONS

DIRECTIONS = (0x10, 0x20, 0x40, 0x80)
ALIASES = {0x17: 7, 0x24: 14, 0x2A: 38}
ENTRY_COURSES = (7, 6, 3, 38, 0, 33, 37)


def course_navigation(world, available, world_open, lid_down=False, current=None):
    """return the A500:A5DF cache. native path steps run entirely in the ROM."""
    nodes = {i for i, (_, w) in COURSES.items() if w == world}
    graph = {}
    for source in nodes:
        if (
            source == 10
        ):  # C13 shares C10's native paths, but must remain a separate stop
            graph[source] = [(0x80, b"", 5)] if lid_down else []
            continue
        graph[source] = []
        for direction, data, path_id in zip(
            DIRECTIONS, PATHS[source], PATH_IDS[source]
        ):
            if data is None:
                continue
            data = bytes.fromhex(data)
            destination = ALIASES.get(data[-1], data[-1])
            if destination == 0xFA and not world_open[5]:
                continue
            # sherbet's right exit stops on the overworld instead of entering mt teapot
            graph[source].append((direction, bytes([path_id]), destination))
        if source == 5 and lid_down:
            graph[source].append((0x40, b"", 10))
    sources = {i for i in nodes if available[i]} | {ENTRY_COURSES[world]}
    if world == 1:
        sources |= {16, 10}  # bridge entry and C12's native lid-change automove
    if current in nodes:
        sources.add(current)
    records = {}
    for source in sorted(sources):
        queue = deque([(source, b"", 0)])
        visited = {source}
        targets = {}
        while queue:
            node, steps, first_direction = queue.popleft()
            for direction, data, destination in graph[node]:
                if destination in visited:
                    continue
                joined = steps + data
                initial = first_direction or direction
                if destination >= 0xF8 or available[destination]:
                    targets[destination] = (
                        initial,
                        joined + bytes([0xFF, destination]),
                    )
                    visited.add(destination)
                elif destination in nodes:
                    visited.add(destination)
                    queue.append((destination, joined, initial))
        assert len(targets) <= 4, (world, source, targets.keys())
        assigned = {}
        deferred = []
        # keep native directions where possible
        for destination, (direction, data) in sorted(
            targets.items(), key=lambda pair: (len(pair[1][1]), pair[0])
        ):
            if direction not in assigned:
                assigned[direction] = data
            else:
                deferred.append((destination, data))
        for destination, data in deferred:
            y, x = POSITIONS[source]
            ty, tx = POSITIONS.get(destination, (y, x))
            scores = {0x10: tx - x, 0x20: x - tx, 0x40: y - ty, 0x80: ty - y}
            direction = max(
                (d for d in DIRECTIONS if d not in assigned), key=lambda d: scores[d]
            )
            assigned[direction] = data
        records[source] = assigned
    cache = bytearray([48] * 48 + [0] * 5)
    offsets = {}
    for data in sorted(
        {p for paths in records.values() for p in paths.values()}, key=len, reverse=True
    ):
        offset = bytes(cache[53:]).find(data)
        if offset >= 0:
            offsets[data] = offset + 53
        else:
            offsets[data] = len(cache)
            cache.extend(data)
    for source, paths in records.items():
        record = bytes(
            [
                sum(paths),
                *(offsets[paths[d]] if d in paths else 0xFF for d in DIRECTIONS),
            ]
        )
        if not paths:
            continue
        offset = bytes(cache).find(record, 53)
        if offset < 0:
            offset = len(cache)
            cache.extend(record)
        cache[source] = offset
    for alias, original in ALIASES.items():
        cache[alias] = cache[original]
    if len(cache) > 0xE0:
        raise ValueError(
            f"Course navigation exceeds its SRAM cache: {len(cache)} bytes"
        )
    cache.extend(bytes(0xE0 - len(cache)))
    return bytes(cache)
