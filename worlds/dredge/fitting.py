from __future__ import annotations

from collections.abc import Iterable
from functools import cache

from .items import item_table, load_data_file

# Hull cells each equipment group can use: N cells take rods or nets, R cells take rods only.
CELL_KINDS_BY_ITEM_GROUP = {"Rod": "RN", "Net": "N", "Engine": "E", "Light": "L"}

HULL_LAYOUTS = load_data_file("hulls.json")

Cell = tuple[int, int]


def parse_cells(rows: list[str], kinds: str) -> set[Cell]:
    return {(x, y) for y, row in enumerate(rows) for x, kind in enumerate(row) if kind in kinds}


def rotations(shape: set[Cell]) -> list[set[Cell]]:
    result = []
    for _ in range(4):
        min_x = min(x for x, _ in shape)
        min_y = min(y for _, y in shape)
        result.append({(x - min_x, y - min_y) for x, y in shape})
        shape = {(y, -x) for x, y in shape}
    return result


def placements(shape: set[Cell], cells: set[Cell]) -> list[frozenset[Cell]]:
    result = set()
    for rotation in rotations(shape):
        anchor_x, anchor_y = next(iter(rotation))
        for cell_x, cell_y in cells:
            dx, dy = cell_x - anchor_x, cell_y - anchor_y
            placed = frozenset((x + dx, y + dy) for x, y in rotation)
            if placed <= cells:
                result.add(placed)
    return list(result)


def fits_together(options: list[list[frozenset[Cell]]], used: frozenset[Cell] = frozenset(), start: int = 0) -> bool:
    """Whether every item can be placed without overlap. Copies of one item share the same options list and sit next
    to each other, so each copy only tries placements after the previous one's to skip reordered duplicates."""
    if not options:
        return True
    first, rest = options[0], options[1:]
    for index in range(start, len(first)):
        placed = first[index]
        if placed.isdisjoint(used):
            next_start = index + 1 if rest and rest[0] is first else 0
            if fits_together(rest, used | placed, next_start):
                return True
    return False


def layout_rows(hull_count: int, include_iron_rig: bool) -> list[str]:
    layouts = HULL_LAYOUTS["with_iron_rig" if include_iron_rig else "without_iron_rig"]
    return layouts[min(hull_count, len(layouts) - 1)]


def best_total(item_names: Iterable[str], stat: str, hull_count: int, include_iron_rig: bool) -> int:
    """The highest summed stat (speed or lumens) of items that can all be equipped on the hull at once, counting
    extra copies of rebuyable items."""
    return _best_total(frozenset(item_names), stat, hull_count, include_iron_rig)


@cache
def _item_placements(item_name: str, hull_count: int, include_iron_rig: bool) -> list[frozenset[Cell]]:
    item = item_table[item_name]
    cells = parse_cells(layout_rows(hull_count, include_iron_rig), CELL_KINDS_BY_ITEM_GROUP[item.item_group])
    return placements(parse_cells(item.shape, "X"), cells)


def _loadouts(names: list[str], free_cells: int) -> list[tuple[str, ...]]:
    """Every combination of the items that could fill at most free_cells, taking rebuyable items more than once."""
    if not names:
        return [()]
    name, rest = names[0], names[1:]
    item = item_table[name]
    size = len(parse_cells(item.shape, "X"))
    max_copies = free_cells // size if item.rebuyable else min(1, free_cells // size)
    return [(name,) * copies + loadout
            for copies in range(max_copies + 1)
            for loadout in _loadouts(rest, free_cells - copies * size)]


@cache
def _best_total(item_names: frozenset[str], stat: str, hull_count: int, include_iron_rig: bool) -> int:
    options = {name: _item_placements(name, hull_count, include_iron_rig) for name in item_names}
    fitting_names = sorted(name for name in item_names if options[name])
    if not fitting_names:
        return 0
    kinds = CELL_KINDS_BY_ITEM_GROUP[item_table[fitting_names[0]].item_group]
    free_cells = len(parse_cells(layout_rows(hull_count, include_iron_rig), kinds))
    loadouts = _loadouts(fitting_names, free_cells)
    loadouts.sort(key=lambda loadout: sum(getattr(item_table[name], stat) for name in loadout), reverse=True)
    for loadout in loadouts:
        if fits_together([options[name] for name in loadout]):
            return sum(getattr(item_table[name], stat) for name in loadout)
    return 0


@cache
def hulls_needed(item_name: str, include_iron_rig: bool) -> int:
    item = item_table.get(item_name)
    kinds = CELL_KINDS_BY_ITEM_GROUP.get(item.item_group) if item else None
    if kinds is None or not item.shape:
        return 0

    shape = parse_cells(item.shape, "X")
    layouts = HULL_LAYOUTS["with_iron_rig" if include_iron_rig else "without_iron_rig"]
    for hull_count, rows in enumerate(layouts):
        if placements(shape, parse_cells(rows, kinds)):
            return hull_count
    raise ValueError(f"{item_name} doesn't fit on any hull")
