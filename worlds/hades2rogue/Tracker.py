"""Data model for the client's "Hades 2" tab (Client.py draws it; nothing in here imports Kivy).

Everything is computed from four inputs the client already has: slot_data, the received item
names, THIS slot's own location names (the server's list, so it is exactly what this seed
generated) and which of them are checked -- plus, when Universal Tracker is installed and has a
working regen, the location ids it currently considers in logic.

Counting from the slot's real location list instead of re-deriving totals from slot_data is
deliberate: the old tab rebuilt totals from room_count * multiplier and matched names against
per-route prefixes, which silently showed 0/N forever for per_aspect_room_based (its names start
with "<Aspect> <Weapon>", not the route) and had no Dream column at all.

The model is plain lists/dicts/tuples so the UI can compare two models with == and only rebuild
its widgets when something actually changed.
"""
from typing import Dict, List, Optional, Set, Tuple

from .Items import WEAPON_SHORT_NAMES, vow_names, aspect_titles, ASPECT_BASE_TITLE_BY_WEAPON, \
    ASPECT_TITLES_BY_WEAPON, ASPECT_MAX_RANK, INITIAL_WEAPON_BY_VALUE, ASPECT_BASE_DISPLAY_KEY, \
    ASPECT_DISPLAY_KEY_BY_TITLE, godsanity_gods_for, helper_story_npcs, \
    helper_story_npcs_nightmare, combat_helper_npcs
from .Locations import location_keepsakes, location_enemies, location_npc_intro, \
    location_npc_meet, location_npc_boss, ZAGREUS_MET_LOCATION, ZAGREUS_DEFEATED_LOCATION
from .Routes import ROUTES, UNDERWORLD, SURFACE, NIGHTMARE, DREAM

# Every string the tab shows a player, in one place. Route, zone, boss, weapon, Aspect, god, NPC
# and enemy names are not in here -- they come from the game data / location names.
LABELS = {
    "rooms": "Rooms Cleared",
    "score": "Score Locations",
    "goal_complete": "Goal Complete!",
    "goal_title": "Goal",
    "goal_mode_all": "Complete all:",
    "goal_mode_any": "Complete any:",
    "goal_clears": "clears",
    "goal_weapons": "Weapons",
    "shared_title": "Shared pool",
    "weapons_title": "Weapons",
    "rank": "Rank",
    "keepsakes_title": "Keepsakes",
    "npcs_title": "NPCs",
    "enemies_title": "Enemies",
    "other_title": "Other",
    "gods_title": "Gods",
    "helpers_title": "Helpers",
    "vows_title": "Vows",
    "in_logic": "{n} in logic",
    "entry_in_logic": "in logic",
    "show": "Show",
    "hide": "Hide",
    "unknown": "?",
}

ROUTE_ORDER = [UNDERWORLD, SURFACE, NIGHTMARE, DREAM]
POINT_BASED, ROOM_BASED, PER_WEAPON_ROOM_BASED, PER_ASPECT_ROOM_BASED = 0, 1, 2, 3
DREAM_COUNTER_PREFIXES = ("Dream Enemy", "Dream Miniboss", "Dream Boss")
ASPECT_DISPLAY_KEYS = {ASPECT_BASE_DISPLAY_KEY, *ASPECT_DISPLAY_KEY_BY_TITLE.values()}
# display key -> internal aspect key ("base" or the alt's full title), per weapon -- the key
# aspect_rank() takes, same mapping as Rules._internal_aspect_key.
_ASPECT_KEY_BY_DISPLAY = {(weapon, ASPECT_BASE_DISPLAY_KEY): "base" for weapon in WEAPON_SHORT_NAMES}
_ASPECT_KEY_BY_DISPLAY.update({(weapon, ASPECT_DISPLAY_KEY_BY_TITLE[title]): title
                               for title, weapon in aspect_titles})
_NPC_LOCATIONS = set(location_npc_intro) | set(location_npc_meet) | set(location_npc_boss) \
    | {ZAGREUS_MET_LOCATION}
_ENEMY_LOCATIONS = set(location_enemies) | {ZAGREUS_DEFEATED_LOCATION}


def _int(slot_data: dict, key: str, default: int = 0) -> int:
    try:
        return int(slot_data.get(key, default))
    except (TypeError, ValueError):
        return default


def active_routes(slot_data: dict) -> List[str]:
    return [route for route in ROUTE_ORDER if _int(slot_data, f"{route.lower()}_active")]


def zone_names(route: str, slot_data: dict) -> List[str]:
    """Display names of a route's zones, in order. Dream's regions are "Region N", the same zone
    token its location names use ("Dream Region 3 Room 07")."""
    if route == DREAM:
        return [f"Region {i}" for i in range(1, _int(slot_data, "dream_region_count_actual") + 1)]
    return list(ROUTES[route]["zone_display"])


# ---------------- location classification --------------------------------------------------

def classify_locations(slot_data: dict, locations: Dict[int, str]) -> Dict[int, tuple]:
    """location id -> a key saying where the tab counts it. Built once per connection (a slot's
    location list never changes), then counted against checked/in-logic sets every refresh.

      ("room", route, zone_index, lane)   split-pool room check; lane is None, a weapon, or
                                           (weapon, aspect display key) for per_aspect
      ("shared_room", lane)                combine_pools' route-agnostic "Room NN" pool
      ("score", route) / ("shared_score",) point_based
      ("dream_counter", prefix)            "Dream Enemy/Miniboss/Boss NN"
      ("keepsake", npc) / ("npc", name) / ("enemy", name)
      ("other", name)                      anything unrecognized -- shown rather than hidden
    """
    zone_prefixes = []
    for route in active_routes(slot_data):
        for zi, zone in enumerate(zone_names(route, slot_data)):
            zone_prefixes.append((f"{route} {zone} Room ", route, zi))
    return {loc_id: _classify(name, zone_prefixes) for loc_id, name in locations.items()}


def _classify(name: str, zone_prefixes: list) -> tuple:
    if name in location_keepsakes:
        return ("keepsake", name[:-len(" Keepsake")])
    if name in _NPC_LOCATIONS:
        return ("npc", name[len("Met "):] if name.startswith("Met ") else name)
    if name in _ENEMY_LOCATIONS:
        return ("enemy", name[:-len(" Defeated")])
    for prefix in DREAM_COUNTER_PREFIXES:
        if name.startswith(prefix + " "):
            return ("dream_counter", prefix)
    for route in ROUTE_ORDER:
        if name.startswith(f"{route} Score "):
            return ("score", route)
    if name.startswith("Score "):
        return ("shared_score",)

    # Room checks. per_aspect names lead with "<Aspect> <Weapon> "; per_weapon names end with
    # " <Weapon>" (after the optional " +k" multiplier slot).
    lane = None
    rest = name
    parts = name.split(" ", 2)
    if len(parts) == 3 and parts[0] in ASPECT_DISPLAY_KEYS and parts[1] in WEAPON_SHORT_NAMES:
        lane = (parts[1], parts[0])
        rest = parts[2]
    for prefix, route, zi in zone_prefixes:
        if rest.startswith(prefix):
            tail = rest[len(prefix):].split()
            if lane is None and len(tail) > 1 and tail[-1] in WEAPON_SHORT_NAMES:
                lane = tail[-1]
            return ("room", route, zi, lane)
    if rest.startswith("Room "):
        tail = rest[len("Room "):].split()
        if lane is None and len(tail) > 1 and tail[-1] in WEAPON_SHORT_NAMES:
            lane = tail[-1]
        return ("shared_room", lane)
    return ("other", name)


# ---------------- items: access, weapons, unlocks -------------------------------------------

def item_counts(received: List[str]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for name in received:
        counts[name] = counts.get(name, 0) + 1
    return counts


def route_access(route: str, slot_data: dict, counts: Dict[str, int]) -> dict:
    """Which of a route's zones the player's items open, from Progressive/Access item counts and
    the same thresholds Rules.set_rules uses for "Descend <route>"/"Exit <zone>". Item gates only:
    it does NOT model the boss-tier gates (arcana/grasp/weapons...) Rules.py adds on top -- that is
    what Universal Tracker's in-logic counts are for."""
    zones = zone_names(route, slot_data)
    locked = bool(_int(slot_data, "lock_routes"))
    offset = _int(slot_data, f"{route.lower()}_offset")
    prog_name = "Progressive Dream" if route == DREAM else ROUTES[route]["progressive"]
    p = counts.get(prog_name, 0)

    if route == UNDERWORLD:
        entered = (p >= offset) if locked else True
    else:
        start = bool(_int(slot_data, f"{route.lower()}_start"))
        if locked and not start:
            # The first Progressive <Route> opens the door itself (no separate Access item),
            # and route_offsets is 1 for a non-starting locked route, so the ladder below still
            # counts that copy as spent on the door.
            entered = p >= 1
        else:
            entered = start or counts.get(f"{route} Access", 0) > 0

    zone_open = []
    for k in range(len(zones)):
        if k == 0 or not locked:
            zone_open.append(entered)
        else:
            zone_open.append(entered and p >= k + offset)
    progressive = (prog_name, p, len(zones) - 1 + offset) if locked and zones else None
    return {"entered": entered, "zone_open": zone_open, "progressive": progressive}


def weapon_owned(weapon: str, slot_data: dict, counts: Dict[str, int]) -> bool:
    """Mirrors Rules.Hades2Logic._hades2_has_weapon."""
    if INITIAL_WEAPON_BY_VALUE.get(_int(slot_data, "initial_weapon")) == weapon:
        return True
    if counts.get(f"{weapon} Weapon Unlock Item", 0) or counts.get(f"Progressive {weapon}", 0):
        return True
    asp = _int(slot_data, "aspectsanity")
    if asp == 1:
        names = [ASPECT_BASE_TITLE_BY_WEAPON[weapon]] + ASPECT_TITLES_BY_WEAPON.get(weapon, [])
        return any(counts.get(n, 0) for n in names)
    if asp == 3:
        names = [f"Progressive {weapon} Base Aspect"] + \
            [f"Progressive {title}" for title in ASPECT_TITLES_BY_WEAPON.get(weapon, [])]
        return any(counts.get(n, 0) for n in names)
    return False


def aspect_rank(weapon: str, aspect_key: str, slot_data: dict, counts: Dict[str, int]) -> Optional[int]:
    """Mirrors Rules.Hades2Logic._hades2_aspect_rank; aspect_key is "base" or an alt's full title.
    None under aspectsanity "unlocked", where ranks aren't items at all.
    per_aspect's pre-collected starting copy is already in items_received (the server sends
    start inventory like any other item), so it is not added again here."""
    asp = _int(slot_data, "aspectsanity")
    if asp == 0:
        return None
    if asp == 2:
        return min(counts.get(f"Progressive {weapon}", 0), ASPECT_MAX_RANK)
    if asp == 1:
        name = ASPECT_BASE_TITLE_BY_WEAPON[weapon] if aspect_key == "base" else aspect_key
        if counts.get(name, 0):
            return ASPECT_MAX_RANK
        # The starting weapon's starting Aspect sits at rank 1 without its item in this mode.
        alts = ASPECT_TITLES_BY_WEAPON.get(weapon, [])
        index = _int(slot_data, "starting_aspect_index")
        starting = INITIAL_WEAPON_BY_VALUE.get(_int(slot_data, "initial_weapon")) == weapon and (
            (index == 0 and aspect_key == "base")
            or (0 < index <= len(alts) and aspect_key == alts[index - 1]))
        return 1 if starting else 0
    if asp == 3:
        name = f"Progressive {weapon} Base Aspect" if aspect_key == "base" else f"Progressive {aspect_key}"
        return min(counts.get(name, 0), ASPECT_MAX_RANK)
    return 0


def weapon_rank(weapon: str, slot_data: dict, counts: Dict[str, int]) -> Optional[int]:
    keys = ["base"] + ASPECT_TITLES_BY_WEAPON.get(weapon, [])
    ranks = [aspect_rank(weapon, key, slot_data, counts) for key in keys]
    if ranks[0] is None:
        return None
    return max(ranks)


def included_weapons(slot_data: dict) -> List[str]:
    included = slot_data.get("included_weapons") or WEAPON_SHORT_NAMES
    return [w for w in WEAPON_SHORT_NAMES if w in included]


def god_status(slot_data: dict, counts: Dict[str, int]) -> List[Tuple[str, bool]]:
    """GodSanity's gods; empty when godsanity is "unlocked" (no unlock items exist). Either the
    plain unlock item or the fused keepsakesanity=randomized one counts. Chaos only shows on a
    seed that has its item (slot_data godsanity_chaos; older seeds never sent it)."""
    if not _int(slot_data, "godsanity"):
        return []
    return [(god, bool(counts.get(f"{god} Unlock", 0) or counts.get(f"{god} Unlock + Keepsake", 0)))
            for god in godsanity_gods_for(include_chaos=bool(_int(slot_data, "godsanity_chaos")))]


def helper_status(slot_data: dict, counts: Dict[str, int]) -> List[Tuple[str, bool]]:
    """Helper NPCs whose sanity is an item mode (option values 1 "items" / 3 "items_random").
    Same membership as the item pool (__init__._main_pool_item_names): the Nightmare trio and
    Thanatos depend on include_zagreus_journey, not on Nightmare being an active route."""
    result = []
    zj_on = bool(_int(slot_data, "include_zagreus_journey"))
    if _int(slot_data, "helper_room_sanity") % 2 == 1:
        npcs = list(helper_story_npcs)
        if zj_on:
            npcs += helper_story_npcs_nightmare
        result += [(npc, bool(counts.get(f"{npc} Room", 0))) for npc in npcs]
    if _int(slot_data, "combat_helper_sanity") % 2 == 1:
        result += [(npc, bool(counts.get(f"{npc} Helper", 0))) for npc in combat_helper_npcs
                   if zj_on or npc != "Thanatos"]
    return result


def vow_status(slot_data: dict, counts: Dict[str, int]) -> List[Tuple[str, int, int]]:
    """reverse_vow only: (vow, currently applied, configured) for every configured vow -- the
    configured level minus "<Vow> Vow Removal" items received, same as the mod's apply_all_vows."""
    if not _int(slot_data, "reverse_vow"):
        return []
    result = []
    for vow in vow_names:
        configured = _int(slot_data, f"vow_{vow.lower()}")
        if configured > 0:
            result.append((vow, max(0, configured - counts.get(f"{vow} Vow Removal", 0)), configured))
    return result


# ---------------- goal ----------------------------------------------------------------------

GOAL_BOSS_BY_ROUTE = {UNDERWORLD: "chronos", SURFACE: "typhon", NIGHTMARE: "hades", DREAM: "dream"}


def route_goal_done(route: str, slot_data: dict, stats: Optional[dict]) -> bool:
    """The route's final boss has met its clear count and the shared weapon-variety count, from
    the latest VICTORY stats -- same test as evaluate_goal."""
    if not stats:
        return False
    boss = GOAL_BOSS_BY_ROUTE[route]
    if stats["clears"].get(boss, 0) < _int(slot_data, f"{route.lower()}_wins_needed", 1):
        return False
    return stats["weapons"].get(boss, 0) >= _int(slot_data, "weapons_clears_needed", 1)


def goal_model(slot_data: dict, stats: Optional[dict], finished: bool) -> Optional[dict]:
    """Rows for each thing the goal needs. stats is {"clears": {boss: n}, "weapons": {boss: n},
    "zagreus": n} from the mod's VICTORY payload, or None before any has been seen for this slot
    (shown as unknown rather than 0)."""
    required = [r for r in ROUTE_ORDER if r in (slot_data.get("goals_required") or [])]
    zagreus = bool(_int(slot_data, "goal_requires_zagreus"))
    if not required and not zagreus:
        return None
    rows = []
    for route in required:
        boss = GOAL_BOSS_BY_ROUTE[route]
        need = _int(slot_data, f"{route.lower()}_wins_needed", 1)
        have = stats["clears"].get(boss, 0) if stats else None
        name = "Dream" if route == DREAM else ROUTES[route]["final_boss"]
        rows.append({"kind": "boss", "name": name, "label": LABELS["goal_clears"], "have": have,
                     "need": need, "done": have is not None and have >= need})
    if zagreus:
        need = _int(slot_data, "zagreus_defeats_needed", 1)
        have = stats["zagreus"] if stats else None
        rows.append({"kind": "boss", "name": "Zagreus", "label": LABELS["goal_clears"], "have": have,
                     "need": need, "done": have is not None and have >= need})
    if required:
        # One shared count: the mod unions the weapons used across every route's clears and sends
        # the same number in each boss's slot (LocationManager.distinct_weapons_combined).
        need = _int(slot_data, "weapons_clears_needed", 1)
        have = max(stats["weapons"].values(), default=0) if stats else None
        rows.append({"kind": "weapons", "name": LABELS["goal_weapons"], "label": "", "have": have,
                     "need": need, "done": have is not None and have >= need})
    return {"complete": finished, "mode_all": _int(slot_data, "goal_mode", 1) == 0, "rows": rows}


# ---------------- the whole tab -------------------------------------------------------------

def _tally(keys: Dict[int, tuple], checked: Set[int], in_logic: Optional[Set[int]]) -> Dict[tuple, list]:
    """Group key -> [checked, total, in_logic] for every grouping the tab shows. A location adds
    to several groups (its zone, its lane, its lane within the route...)."""
    tally: Dict[tuple, list] = {}

    def add(group: tuple, loc_id: int) -> None:
        entry = tally.setdefault(group, [0, 0, 0])
        entry[1] += 1
        if loc_id in checked:
            entry[0] += 1
        elif in_logic is not None and loc_id in in_logic:
            entry[2] += 1

    for loc_id, key in keys.items():
        kind = key[0]
        add((kind,) + key[1:], loc_id)
        if kind == "room":
            _, route, zi, lane = key
            add(("zone", route, zi), loc_id)
            add(("route_rooms", route), loc_id)
            if lane is not None:
                weapon = lane if isinstance(lane, str) else lane[0]
                add(("lane", route, lane), loc_id)
                if not isinstance(lane, str):
                    add(("lane", route, weapon), loc_id)
        elif kind == "shared_room":
            lane = key[1]
            add(("shared_rooms",), loc_id)
            if lane is not None and not isinstance(lane, str):
                add(("shared_room", lane[0]), loc_id)
        elif kind in ("keepsake", "npc", "enemy", "other"):
            add(("category", kind), loc_id)
    return tally


def _progress(tally: Dict[tuple, list], group: tuple, uses_logic: bool) -> Tuple[int, int, Optional[int]]:
    checked, total, logic = tally.get(group, [0, 0, 0])
    return checked, total, (logic if uses_logic else None)


def build_model(slot_data: Optional[dict], received: List[str], locations: Dict[int, str],
                keys: Dict[int, tuple], checked: Set[int], in_logic: Optional[Set[int]],
                goal_stats: Optional[dict], finished: bool) -> dict:
    """The full tab. in_logic is None when Universal Tracker isn't available, and every
    "in logic" count is then None too (hidden), never a misleading 0."""
    if not slot_data:
        return {}
    counts = item_counts(received)
    uses_logic = in_logic is not None
    tally = _tally(keys, checked, in_logic)
    system = _int(slot_data, "location_system", ROOM_BASED)
    routes = active_routes(slot_data)

    def progress(group: tuple) -> Tuple[int, int, Optional[int]]:
        return _progress(tally, group, uses_logic)

    shared = []
    if ("shared_rooms",) in tally:
        shared.append((LABELS["rooms"],) + progress(("shared_rooms",)))
    if ("shared_score",) in tally:
        shared.append((LABELS["score"],) + progress(("shared_score",)))

    route_models = []
    for route in routes:
        access = route_access(route, slot_data, counts)
        rows = []
        if ("route_rooms", route) in tally:
            rows.append((LABELS["rooms"],) + progress(("route_rooms", route)))
        if ("score", route) in tally:
            rows.append((LABELS["score"],) + progress(("score", route)))
        if route == DREAM:
            for prefix in DREAM_COUNTER_PREFIXES:
                if ("dream_counter", prefix) in tally:
                    rows.append((prefix,) + progress(("dream_counter", prefix)))
        zones = []
        for zi, zone in enumerate(zone_names(route, slot_data)):
            if ("zone", route, zi) in tally:
                checked_n, total, logic = progress(("zone", route, zi))
            else:
                checked_n = total = logic = None    # point_based / combine_pools: no zone counts
            zones.append({"name": zone, "open": access["zone_open"][zi],
                          "checked": checked_n, "total": total, "in_logic": logic})
        route_models.append({"route": route, "progressive": access["progressive"],
                             "goal_done": route_goal_done(route, slot_data, goal_stats),
                             "rows": rows, "zones": zones})

    # Weapons: one row per included weapon (owned + rank), plus -- in the per-weapon/per-aspect
    # systems -- its room progress per route (or in the shared pool); per_aspect adds one
    # indented row per Aspect lane that has checks this seed.
    columns = []
    if system in (PER_WEAPON_ROOM_BASED, PER_ASPECT_ROOM_BASED):
        if any(("shared_room", w) in tally for w in WEAPON_SHORT_NAMES):
            columns = [None]
        else:
            columns = [r for r in routes if any(("lane", r, w) in tally for w in WEAPON_SHORT_NAMES)]

    def lane_cells(lane) -> list:
        cells = []
        for column in columns:
            group = ("shared_room", lane) if column is None else ("lane", column, lane)
            cells.append(progress(group) if group in tally else None)
        return cells

    weapon_rows = []
    for weapon in included_weapons(slot_data):
        weapon_rows.append({"name": weapon, "indent": False,
                            "owned": weapon_owned(weapon, slot_data, counts),
                            "rank": weapon_rank(weapon, slot_data, counts),
                            "cells": lane_cells(weapon)})
        if system == PER_ASPECT_ROOM_BASED:
            for display_key in [ASPECT_BASE_DISPLAY_KEY] + \
                    [ASPECT_DISPLAY_KEY_BY_TITLE[t] for t in ASPECT_TITLES_BY_WEAPON.get(weapon, [])]:
                lane = (weapon, display_key)
                cells = lane_cells(lane)
                if not any(cells):
                    continue    # IncludedAspects left this Aspect without checks this seed
                weapon_rows.append({"name": display_key, "indent": True, "owned": None,
                                    "rank": aspect_rank(weapon, _ASPECT_KEY_BY_DISPLAY[lane],
                                                        slot_data, counts),
                                    "cells": cells})

    # (name, checked, in logic) per location, for the expandable lists.
    entries_by_kind: Dict[str, list] = {}
    for loc_id, key in keys.items():
        if key[0] in ("keepsake", "npc", "enemy", "other"):
            entries_by_kind.setdefault(key[0], []).append(
                (key[1], loc_id in checked, uses_logic and loc_id not in checked and loc_id in in_logic))
    categories = []
    for kind, title in (("keepsake", "keepsakes_title"), ("npc", "npcs_title"),
                        ("enemy", "enemies_title"), ("other", "other_title")):
        entries = sorted(entries_by_kind.get(kind, []))
        if entries:
            checked_n, total, logic = progress(("category", kind))
            categories.append({"key": kind, "title": LABELS[title], "checked": checked_n,
                               "total": total, "in_logic": logic, "entries": entries})

    return {
        "goal": goal_model(slot_data, goal_stats, finished),
        "shared": shared,
        "routes": route_models,
        "weapons": {"columns": columns, "rows": weapon_rows},
        "categories": categories,
        "gods": god_status(slot_data, counts),
        "helpers": helper_status(slot_data, counts),
        "vows": vow_status(slot_data, counts),
    }
