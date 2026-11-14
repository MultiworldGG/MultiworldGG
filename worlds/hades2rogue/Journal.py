"""Pages for the in-game tracker: the "Archipelago" chapter the mod adds to the Codex.

The client builds every page here, as finished text in the game's own markup, and sends them to
the mod (JOURNAL message, see PROTOCOL.md); the mod only shows them. Keeping the layout on this
side means the pages come from the same Tracker.build_model the "Hades 2" tab draws, and a wording
or layout change needs a new apworld only, not a new mod.

Nothing in here imports Kivy or the Archipelago client, so tools/journal_check.py can run it
against real location tables.
"""
from typing import Dict, List, Optional, Tuple

from . import Tracker
from .Locations import enemy_zone_placement, combined_relabel, parse_shuffle_map, \
    SHARED_ENEMY_ZONES, NPC_BOSS_MEET
from .Routes import ROUTES, UNDERWORLD, SURFACE, NIGHTMARE, DREAM

# Every string a page shows that isn't a name from the game data or one of Tracker.LABELS (which
# the book reuses on purpose: one set of words for both trackers). Wording chosen by the project
# owner on 2026-10-04; don't reword without asking.
LABELS = {
    "chapter": "Archipelago",
    "page_enemies": "{route} Enemies",
    "page_overview": "Overview",
    "page_unlocks": "Unlocks",
    "checks": "Checks",
    "page_hints": "Hints",
    "page_continued": "{title} {n}",        # n is a Roman numeral: "Weapons II"
    "bosses": "Bosses",
    "enemies_elsewhere": "Elsewhere",
    "hints_here": "Hinted in your world",
    "hints_away": "Your items in other worlds",
    "hint_here": "{location}: {item} for {player}",
    "hint_away": "{item}: {location} in {player}'s world",
    "goal_row": "{name}: {have}/{need} {label}",
    "progress": "{checked}/{total}",
    "progress_logic": "{checked}/{total} ({logic})",
    "left": "Remaining:",
    "left_in_logic": "In logic:",
    "left_out_of_logic": "Out of logic:",
    "unlocked": "Unlocked:",
    "locked": "Locked:",
    "more": "+{n} more",
}

# Pages are words and numbers, not a glyph per entry: a list shows only what is still left to do,
# split by a label into what is in logic and what isn't. The one inline icon (UIData.lua Icons) is
# the padlock on a zone or weapon the player's items haven't opened. What can't be done yet is
# also dimmed, always next to a label or the padlock saying why, never by tone alone.
MARK_LOCKED = "{!Icons.Locked}"
HEADER = "{{#CodexBoldFormat}}{text}{{#Prev}}"
DIM = "{{#LockedFormat}}{text}{{#Prev}}"
# The engine's line break inside a text box is the two characters backslash + n.
LINE_BREAK = " \\n "

# How much a Codex page holds. Measured from a screenshot of the book in game (2026-10-09): the
# 14th line already sits on the page's bottom edge. The width is kept on the safe side, since a
# line the engine wraps on its own would push the page past the bottom of the book.
MAX_LINES = 13
CHARS_PER_LINE = 66
ICON_WIDTH = 3          # an inline icon, counted in characters
MAX_HINT_PAGES = 3

# Portrait shown beside each page: Codex portraits the game already has (CodexData.lua).
PORTRAITS = {
    "goal": "Codex_Portrait_Fates",
    UNDERWORLD: "Codex_Portrait_BiomeErebus",
    SURFACE: "Codex_Portrait_BiomeEphyra",
    NIGHTMARE: "Codex_Portrait_BiomeHouseOfHades",
    DREAM: "Codex_Portrait_Hypnos",
    "keepsake": "Codex_Portrait_Charon",
    "npc": "Codex_Portrait_BiomeCrossroads",
    "weapons": "Codex_Portrait_WeaponStaff",
    "unlocks": "Codex_Portrait_Chaos",
    "hints": "Codex_Portrait_Moros",
    "other": "Codex_Portrait_BiomeCrossroads",
}


def _wire(text) -> str:
    """One field of the JOURNAL line: no newline, and none of the two separators."""
    return str(text).replace("\r", " ").replace("\n", " ").replace("|", "/").replace("~", "-")


def _visible_len(text: str) -> int:
    """Rough rendered width in characters: format tags take no room, an icon takes ICON_WIDTH."""
    width, i = 0, 0
    while i < len(text):
        if text[i] == "{":
            end = text.find("}", i)
            if end != -1:
                if text[i + 1:i + 2] == "!":
                    width += ICON_WIDTH
                i = end + 1
                continue
        width += 1
        i += 1
    return width


def _roman(number: int) -> str:
    out = ""
    for value, numeral in ((10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")):
        while number >= value:
            out += numeral
            number -= value
    return out


def _header(text: str) -> str:
    return HEADER.format(text=text)


def _dim(text: str) -> str:
    return DIM.format(text=text)


def _progress(checked: int, total: int, logic: Optional[int]) -> str:
    if logic:
        return LABELS["progress_logic"].format(
            checked=checked, total=total, logic=Tracker.LABELS["in_logic"].format(n=logic))
    return LABELS["progress"].format(checked=checked, total=total)


def _name_lines(label: str, names: List[str], dim: bool = False) -> List[str]:
    """label, then the names with commas, broken into lines the page can hold. Each line carries
    its own format tags, so a page break between two of them leaves nothing open."""
    lines, current = [], label
    for index, name in enumerate(names):
        piece = name if index == len(names) - 1 else name + ","
        if current and len(current) + 1 + len(piece) > CHARS_PER_LINE:
            lines.append(current)
            current = piece
        else:
            current = f"{current} {piece}" if current else piece
    if current:
        lines.append(current)
    return [_dim(line) for line in lines] if dim else lines


def _left(entries: list, uses_logic: bool, show=None) -> List[str]:
    """The checks of a list that are still to do; the ones already sent are only counted, in the
    section's header. entries is [(name, checked, in logic)]; show turns a name into its text."""
    left = [(show(name) if show else name, in_logic) for name, checked, in_logic in entries if not checked]
    if not uses_logic:
        return _name_lines(LABELS["left"], [name for name, _logic in left]) if left else []
    lines = []
    logic = [name for name, in_logic in left if in_logic]
    other = [name for name, in_logic in left if not in_logic]
    if logic:
        lines += _name_lines(LABELS["left_in_logic"], logic)
    if other:
        lines += _name_lines(LABELS["left_out_of_logic"], other, dim=True)
    return lines


def _line_cost(line: str) -> int:
    return max(1, -(-_visible_len(line) // CHARS_PER_LINE))


def _paginate(key: str, title: str, portrait: str, lines: List[str], max_pages: int = 0) -> List[dict]:
    """Split a page that is too long for the book. A section (a header and the lines under it)
    stays on one page when it fits on one; a longer one repeats its header on the next page.
    max_pages > 0 drops what doesn't fit and says how many lines were left out."""
    chunks, current, used, section = [], [], 0, None
    for index, line in enumerate(lines):
        cost = _line_cost(line)
        is_header = line.startswith("{#CodexBoldFormat}")
        next_cost = 0
        if is_header:
            # Cost of the section's body: it moves to the next page whole if it fits on one but
            # not in what is left of this one; a longer one keeps at least a line with its header.
            body = 0
            for later in lines[index + 1:]:
                if later.startswith("{#CodexBoldFormat}"):
                    break
                body += _line_cost(later)
                next_cost = next_cost or body
            if cost + body <= MAX_LINES:
                next_cost = body
        if current and used + cost + next_cost > MAX_LINES:
            chunks.append(current)
            current, used = [], 0
            if section is not None and not is_header:
                # A section cut in two starts the next page under its header again.
                current.append(section)
                used = _line_cost(section)
        if is_header:
            section = line
        current.append(line)
        used += cost
    if current:
        chunks.append(current)
    if max_pages and len(chunks) > max_pages:
        def is_header(line: str) -> bool:
            return line.startswith("{#CodexBoldFormat}")
        # Counted in entries: a section header repeated on a dropped page isn't one.
        dropped = sum(1 for chunk in chunks[max_pages:] for line in chunk if not is_header(line))
        chunks = chunks[:max_pages]
        last = chunks[-1]
        # Room for the closing line is measured the way the page was filled (an entry can wrap
        # onto several lines), and the page doesn't end on a header with nothing under it.
        while len(last) > 1 and (sum(_line_cost(line) for line in last) + 1 > MAX_LINES
                                 or is_header(last[-1])):
            if not is_header(last.pop()):
                dropped += 1
        last.append(LABELS["more"].format(n=dropped))
    pages = []
    for number, chunk in enumerate(chunks, start=1):
        pages.append({
            "key": key if number == 1 else f"{key}_{number}",
            "title": title if number == 1 else LABELS["page_continued"].format(title=title, n=_roman(number)),
            "portrait": portrait,
            "body": LINE_BREAK.join(chunk),
        })
    return pages


# ---------------- where each enemy check is ------------------------------------------------

def enemy_places(slot_data: dict) -> Dict[str, List[Tuple[str, int]]]:
    """Enemy name -> the (route, zone index) pairs where its check can be earned in this seed:
    the same placement the world's logic uses (Locations.enemy_zone_placement over the seed's
    enemy shuffle and miniboss-room maps), so a shuffled enemy is listed where it now spawns."""
    routes = [r for r in Tracker.active_routes(slot_data) if r in ROUTES]
    enemy_map = parse_shuffle_map(str(slot_data.get("enemysanity_shuffle_map") or ""))
    room_map = parse_shuffle_map(str(slot_data.get("miniboss_room_map") or ""))
    try:
        relabel = combined_relabel(enemy_map, room_map)
    except ValueError:
        relabel = dict(enemy_map)
    suffix = len(" Defeated")
    places: Dict[str, List[Tuple[str, int]]] = {}
    for (route, zone), names in enemy_zone_placement(relabel, routes).items():
        zone_index = ROUTES[route]["zones"].index(zone)
        for location in names:
            places.setdefault(location[:-suffix], []).append((route, zone_index))
    # Shared names the shuffle left alone sit in no zone bucket; a kill in any of their zones counts.
    for location, zones in SHARED_ENEMY_ZONES.items():
        places.setdefault(location[:-suffix], list(zones))
    return places


def boss_places() -> Dict[str, Tuple[str, int]]:
    return {name[len("Met "):]: (route, zone_index) for name, route, zone_index in NPC_BOSS_MEET}


# ---------------- pages ---------------------------------------------------------------------

def _check_totals(model: dict) -> List[tuple]:
    """(label, checked, total, in logic) for each kind of check in the seed, all routes together."""
    rows = list(model.get("shared") or [])
    for route_model in model.get("routes", []):
        rows += route_model["rows"]
    rows += [(category["title"], category["checked"], category["total"], category["in_logic"])
             for category in model.get("categories", [])]
    totals: Dict[str, list] = {}
    for label, checked, total, logic in rows:
        entry = totals.setdefault(label, [0, 0, None])
        entry[0] += checked
        entry[1] += total
        if logic is not None:
            entry[2] = (entry[2] or 0) + logic
    return [(label, *entry) for label, entry in totals.items()]


def _overview_page(model: dict) -> List[dict]:
    """First page: what the goal still needs, then how many checks of each kind are left."""
    goal = model.get("goal")
    lines = []
    if goal:
        lines.append(_header(Tracker.LABELS["goal_complete" if goal["complete"] else "goal_title"]))
        if len(goal["rows"]) > 1:
            lines.append(Tracker.LABELS["goal_mode_all" if goal["mode_all"] else "goal_mode_any"])
        for row in goal["rows"]:
            have = Tracker.LABELS["unknown"] if row["have"] is None else row["have"]
            lines.append(LABELS["goal_row"].format(name=row["name"], have=have, need=row["need"],
                                                   label=row["label"]).rstrip())
    totals = _check_totals(model)
    if totals:
        logic = [row[3] for row in totals if row[3] is not None]
        everything = _progress(sum(row[1] for row in totals), sum(row[2] for row in totals),
                               sum(logic) if logic else None)
        lines.append(_header(f"{LABELS['checks']}: {everything}"))
        for label, checked, total, in_logic in totals:
            lines.append(f"{label}: {_progress(checked, total, in_logic)}")
    if not lines:
        return []
    return _paginate("goal", LABELS["page_overview"], PORTRAITS["goal"], lines)


def _route_page(route_model: dict) -> List[dict]:
    route = route_model["route"]
    lines = []
    if route_model["progressive"]:
        name, have, need = route_model["progressive"]
        lines.append(f"{name}: {LABELS['progress'].format(checked=have, total=need)}")
    for label, checked, total, logic in route_model["rows"]:
        lines.append(f"{label}: {_progress(checked, total, logic)}")
    for zone in route_model["zones"]:
        text = zone["name"]
        if zone["total"] is not None:
            text += f": {_progress(zone['checked'], zone['total'], zone['in_logic'])}"
        lines.append(text if zone["open"] else _dim(f"{text} {MARK_LOCKED}"))
    if not lines:
        return []
    return _paginate(f"route_{route.lower()}", route, PORTRAITS.get(route, ""), lines)


def _uses_logic(category: dict) -> bool:
    """Tracker.build_model leaves a category's in-logic count None without Universal Tracker."""
    return category["in_logic"] is not None


def _enemy_pages(slot_data: dict, routes: List[str], category: dict) -> List[dict]:
    """One page per route, its enemy checks under the zone where each can be earned."""
    places = enemy_places(slot_data)
    uses_logic = _uses_logic(category)
    by_name = {name: (name, checked, in_logic) for name, checked, in_logic in category["entries"]}
    by_zone: Dict[Tuple[str, int], List[str]] = {}
    unplaced = []
    for name in sorted(by_name):
        spots = [spot for spot in places.get(name, []) if spot[0] in routes]
        if not spots:
            unplaced.append(name)
        for spot in spots:
            by_zone.setdefault(spot, []).append(name)

    def section(title: str, names: List[str]) -> List[str]:
        entries = [by_name[name] for name in names]
        done = sum(1 for entry in entries if entry[1])
        header = _header(f"{title}: {LABELS['progress'].format(checked=done, total=len(names))}")
        return [header] + _left(entries, uses_logic)

    pages = []
    listed_routes = [r for r in routes if r in ROUTES]
    for route in listed_routes:
        lines = []
        for zone_index, zone in enumerate(ROUTES[route]["zone_display"]):
            names = by_zone.get((route, zone_index), [])
            if names:
                lines += section(zone, names)
        if route == listed_routes[-1] and unplaced:
            lines += section(LABELS["enemies_elsewhere"], unplaced)
        if lines:
            title = LABELS["page_enemies"].format(route=route)
            pages += _paginate(f"enemies_{route.lower()}", title, PORTRAITS.get(route, ""), lines)
    if not listed_routes and unplaced:
        lines = section(Tracker.LABELS["enemies_title"], unplaced)
        pages += _paginate("enemies", Tracker.LABELS["enemies_title"], PORTRAITS["other"], lines)
    return pages


def _list_page(key: str, title: str, portrait: str, category: dict) -> List[dict]:
    header = _header(f"{title}: {_progress(category['checked'], category['total'], category['in_logic'])}")
    lines = [header] + _left(category["entries"], _uses_logic(category))
    return _paginate(key, title, portrait, lines)


def _npc_page(slot_data: dict, category: dict) -> List[dict]:
    """Met checks: the Crossroads cast as one list, then the route bosses with their zone."""
    bosses = boss_places()
    uses_logic = _uses_logic(category)
    cast = [entry for entry in category["entries"] if entry[0] not in bosses]
    met_bosses = [entry for entry in category["entries"] if entry[0] in bosses]
    title = Tracker.LABELS["npcs_title"]
    lines = [_header(f"{title}: {_progress(category['checked'], category['total'], category['in_logic'])}")]
    lines += _left(cast, uses_logic)
    if met_bosses:
        done = sum(1 for entry in met_bosses if entry[1])
        lines.append(_header(f"{LABELS['bosses']}: "
                             f"{LABELS['progress'].format(checked=done, total=len(met_bosses))}"))
        order = {route: index for index, route in enumerate(Tracker.ROUTE_ORDER)}
        met_bosses.sort(key=lambda entry: (order.get(bosses[entry[0]][0], 9), bosses[entry[0]][1]))
        lines += _left(met_bosses, uses_logic,
                       lambda name: f"{name} ({ROUTES[bosses[name][0]]['zone_display'][bosses[name][1]]})")
    return _paginate("npcs", title, PORTRAITS["npc"], lines)


def _weapons_page(model: dict) -> List[dict]:
    """Seeds whose room checks aren't per weapon get one short list. Otherwise each weapon is a
    section: its room checks per route, then a line per Aspect (all routes added up)."""
    weapons = model.get("weapons") or {}
    rows, columns = weapons.get("rows", []), weapons.get("columns", [])
    title = Tracker.LABELS["weapons_title"]

    def named(row: dict) -> str:
        if row["rank"] is None:
            return row["name"]
        return f"{row['name']}, {Tracker.LABELS['rank']} {row['rank']}"

    lines = []
    if not columns:
        top = [row for row in rows if not row["indent"]]
        owned = [named(row).replace(",", "") for row in top if row["owned"]]
        missing = [row["name"] for row in top if not row["owned"]]
        if top:
            lines.append(_header(f"{title}: {LABELS['progress'].format(checked=len(owned), total=len(top))}"))
        if owned:
            lines += _name_lines(LABELS["unlocked"], owned)
        if missing:
            lines += _name_lines(LABELS["locked"], missing, dim=True)
    for row in rows if columns else []:
        cells = [(column, cell) for column, cell in zip(columns, row["cells"]) if cell]
        if row["indent"]:
            checked = sum(cell[0] for _column, cell in cells)
            total = sum(cell[1] for _column, cell in cells)
            logic = [cell[2] for _column, cell in cells if cell[2] is not None]
            lines.append(f"- {named(row)}: {_progress(checked, total, sum(logic) if logic else None)}")
        else:
            lines.append(_header(named(row) if row["owned"] else f"{named(row)} {MARK_LOCKED}"))
            lines += _name_lines("", [f"{column or Tracker.LABELS['shared_title']} {_progress(*cell)}"
                                      for column, cell in cells])
    if not lines:
        return []
    return _paginate("weapons", title, PORTRAITS["weapons"], lines)


def _unlocks_page(model: dict) -> List[dict]:
    lines = []
    for title, rows in ((Tracker.LABELS["gods_title"], model.get("gods")),
                        (Tracker.LABELS["helpers_title"], model.get("helpers"))):
        if rows:
            owned = [name for name, have in rows if have]
            missing = [name for name, have in rows if not have]
            lines.append(_header(f"{title}: {LABELS['progress'].format(checked=len(owned), total=len(rows))}"))
            if owned:
                lines += _name_lines(LABELS["unlocked"], owned)
            if missing:
                lines += _name_lines(LABELS["locked"], missing, dim=True)
    if model.get("vows"):
        lines.append(_header(Tracker.LABELS["vows_title"]))
        lines += _name_lines("", [f"{vow} {current}/{configured}"
                                  for vow, current, configured in model["vows"]])
    if not lines:
        return []
    return _paginate("unlocks", LABELS["page_unlocks"], PORTRAITS["unlocks"], lines)


def _plain(text) -> str:
    """A name from another world, safe to put on a page: braces are the game's markup, and an
    item called "{Key}" would be read as a format tag."""
    return str(text).replace("{", "(").replace("}", ")")


def _hints_page(hints_here: list, hints_away: list) -> List[dict]:
    lines = []
    if hints_here:
        lines.append(_header(LABELS["hints_here"]))
        lines += [LABELS["hint_here"].format(location=_plain(location), item=_plain(item),
                                             player=_plain(player))
                  for location, item, player in hints_here]
    if hints_away:
        lines.append(_header(LABELS["hints_away"]))
        lines += [LABELS["hint_away"].format(item=_plain(item), location=_plain(location),
                                             player=_plain(player))
                  for item, location, player in hints_away]
    if not lines:
        return []
    return _paginate("hints", LABELS["page_hints"], PORTRAITS["hints"], lines, MAX_HINT_PAGES)


def build_pages(slot_data: Optional[dict], model: dict, hints_here: Optional[list] = None,
                hints_away: Optional[list] = None) -> List[dict]:
    """The chapter's pages in order: [{"key", "title", "portrait", "body"}].

    model is Tracker.build_model's. hints_here is [(location, item, receiving player)] for unfound
    hints on this slot's own locations; hints_away is [(item, location, finding player)] for this
    slot's hinted items sitting in other worlds."""
    if not slot_data or not model:
        return []
    routes = Tracker.active_routes(slot_data)
    categories = {category["key"]: category for category in model.get("categories", [])}
    pages = _overview_page(model)
    for route_model in model.get("routes", []):
        pages += _route_page(route_model)
    if "enemy" in categories:
        pages += _enemy_pages(slot_data, routes, categories["enemy"])
    if "keepsake" in categories:
        pages += _list_page("keepsakes", Tracker.LABELS["keepsakes_title"], PORTRAITS["keepsake"],
                            categories["keepsake"])
    if "npc" in categories:
        pages += _npc_page(slot_data, categories["npc"])
    pages += _weapons_page(model)
    pages += _unlocks_page(model)
    pages += _hints_page(hints_here or [], hints_away or [])
    if "other" in categories:
        pages += _list_page("other", Tracker.LABELS["other_title"], PORTRAITS["other"],
                            categories["other"])
    return pages


def encode(pages: List[dict]) -> str:
    """JOURNAL payload: "<chapter title>|<key>~<title>~<portrait>~<body>|..."."""
    fields = [_wire(LABELS["chapter"])]
    for page in pages:
        fields.append("~".join(_wire(page[name]) for name in ("key", "title", "portrait", "body")))
    return "|".join(fields)
