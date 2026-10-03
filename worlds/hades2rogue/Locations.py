from BaseClasses import Location

from .Routes import ROUTES, ROUTE_NAMES, UNDERWORLD, SURFACE, NIGHTMARE, DREAM, MAX_ROOMS, \
    WEAPON_ROOM_STRIDE, boss_event, active_routes, NPC_ROUTE_LOCK, NPC_RANDOMIZED_HELPERS, \
    COMBAT_HELPER_NPCS, COMBAT_HELPER_NATIVE_ROUTE, ZJ_RANDOMIZED_ONLY, \
    combat_helper_native_fallback
from .Items import keepsake_titles, KEEPSAKE_NO_LOCATION, WEAPON_SHORT_NAMES, KEEPSAKE_NPC, \
    weapon_aspect_slots

hades2_base_location_id = 1

# ID layout (offsets from hades2_base_location_id), per route:
#   Underworld point checks:  0    .. 999      Surface point checks:  2000 .. 2999
#   Keepsake unlock checks:   6100 .. 6132
#   Underworld room checks:   7000 .. 7000+MAX Surface room checks:   8000 .. 8000+MAX
#   Underworld per-weapon:    10000 + weapon*WEAPON_ROOM_STRIDE + depth
#   Surface per-weapon:       20000 + weapon*WEAPON_ROOM_STRIDE + depth
#   Combined room checks:     9000 .. 9000+MAX  (separate_checks=combine_pools)
#   Combined per-weapon:      60000 + weapon*WEAPON_ROOM_STRIDE + depth
#   Combined point checks:    3000 .. 3999      (separate_checks=combine_pools)
# (Weapon-unlock check ids 4000..4005 are retired -- weapon-shop checks were removed.)
#   Underworld per-aspect:    100000 + lane*ASPECT_ROOM_STRIDE + depth  (lane = weapon*4 + aspect)
#   Surface per-aspect:       130000 + lane*ASPECT_ROOM_STRIDE + depth
#   Nightmare per-aspect:     160000 + lane*ASPECT_ROOM_STRIDE + depth
#   Combined per-aspect:      190000 + lane*ASPECT_ROOM_STRIDE + depth  (separate_checks=combine_pools)
# (Each per-aspect block reserves 20000 ids: MAX_LOCATION_MULTIPLIER(8) * ASPECT_ROOM_SLOT_STRIDE(2500).)
#   Dream Score checks:       220000 .. 220000+MAX_SCORE_CHECKS (1000 reserved)
#   Dream Room checks:        221500 .. 221500+2000 (comfortable headroom over today's 144 max)
#   Dream per-weapon Room:    224000 + weapon*DREAM_WEAPON_ROOM_STRIDE(500) + depth
#   Dream per-aspect Room:    228000 + lane*DREAM_ASPECT_ROOM_STRIDE(500) + depth
#   Dream Enemy counter:      241000 .. +~1000    Dream Miniboss counter: 242000 .. +~1000
#   Dream Boss counter:       243000 .. +12        "Beat Dream" event: no id (locked event)
# (Dream has no fixed 4-zone shape -- see Routes.DREAM's definition comment for why it doesn't
# reuse ROUTES/_zone_bounds. All Dream ids are reserved fresh, clear of every range above.)
# NOTE: this id layout is unaffected by the per-zone room-check renumbering (_room_name/
# _aspect_room_name) -- ids still come from a route-wide global position (see _explicit_zone_
# bounds), only the DISPLAY name ("Underworld Erebus Room 07" instead of "Underworld Room
# 0030") changed. Room-check names below this comment that still show the old flat
# "Underworld Room NNNN" shape are illustrative/id-map shorthand, not the real current format.

# Location-system option values (match Options.LocationSystem).
POINT_BASED = 0
ROOM_BASED = 1
PER_WEAPON_ROOM_BASED = 2
PER_ASPECT_ROOM_BASED = 3

# separate_checks option value (match Options.SeparateChecks; split_pools is 0).
COMBINE_POOLS = 1

# EnemySanity option values (match Options.EnemySanity).
ENEMYSANITY_VANILLA = 0
ENEMYSANITY_VANILLA_PLUS_LOCATIONS = 1
ENEMYSANITY_SHUFFLED = 2
ENEMYSANITY_SHUFFLED_PLUS_LOCATIONS = 3
ENEMYSANITY_PURE_RANDOM = 4

# --- Location auto-scaling (room systems) ------------------------------------
# When a seed has more items than locations, the room-based systems can't just raise a
# number (a run is only ~50 rooms), so instead each room depth grants several checks. Each
# extra check is a "slot" 0..m-1 living in a disjoint id block, so ids stay stable across
# seeds. MAX_LOCATION_MULTIPLIER caps m and is what the datapackage reserves ids for; the
# slot strides below must keep every slot inside its route's reserved id range (see the ID
# layout map above): plain rooms get MAX_ROOMS ids per slot, per-weapon rooms get 1000.
MAX_LOCATION_MULTIPLIER = 8
WEAPON_ROOM_SLOT_STRIDE = 1000

# Room-check ids are keyed on (zone index, depth WITHIN that zone), NOT a route-wide running
# index -- exactly like the check NAMES are ("<Route> <Zone> Room NN"). This coupling is
# load-bearing, not a style choice: give_all_locations_table (the datapackage) reserves the FULL
# per-zone headroom below, while a real seed only fills each zone's real zone_room_counts, so
# the two disagree about how many rooms precede a given zone. Deriving the id from a running
# index made the same NAME resolve to different ids in the datapackage vs. the seed -- the
# client would then credit an entirely different location than the one actually checked. Keying
# both on (zone, local depth) makes them agree by construction, and additionally means
# re-tuning one zone's count never shifts any other zone's ids.
# 4 zones * 15 == MAX_ROOMS (60), so a slot's id block stays exactly MAX_ROOMS wide and every
# existing per-route id budget (see the ID layout map above) is untouched.
ZONE_ROOM_STRIDE = 15

# per_aspect_room_based reserves its own, much bigger per-lane stride: 6 weapons * 4 aspect
# slots (Items.weapon_aspect_slots) = 24 lanes per route, vs. 6 for the per-weapon systems.
# ASPECT_ROOM_STRIDE (100) comfortably covers MAX_ROOMS depths per lane, same as
# WEAPON_ROOM_STRIDE; ASPECT_ROOM_SLOT_STRIDE (2500) covers all 24 lanes with headroom.
ASPECT_ROOM_STRIDE = 100
ASPECT_ROOM_SLOT_STRIDE = 2500
ASPECT_LANES_PER_WEAPON = 4

# Combined (separate_checks=combine_pools) pools use route-agnostic names in their own id
# space, distinct from the per-route "Underworld Room NNNN" / "Underworld Score NNNN" ids.
# Combined means ONE shared pool that any route contributes to:
#   rooms  -- keyed on room DEPTH: clearing depth N the first time on EITHER route earns it.
#   score  -- one shared point pool: every route's cleared rooms bank into it and every check
#             is route-agnostic, so the whole pool can be earned on a single route.
COMBINED_ROOM_PREFIX = "Room"
combined_room_id_base = 9000           # "Room NNNN"            -> base + (depth-1)
combined_weapon_id_base = 60000        # "Room NNNN <Weapon>"   -> base + weapon*stride + (depth-1)
combined_aspect_id_base = 190000       # "<Aspect> <Weapon> Room NN" -> base + lane*stride + (depth-1)
COMBINED_SCORE_PREFIX = "Score"
combined_score_id_base = 3000          # "Score NNNN"           -> base + (n-1); 1000 ids reserved
MAX_SCORE_CHECKS = 1000                # Options.ScoreRewardsAmount.range_end (id space reserved)

# --- Dream Dive route (variable region count, no fixed boss identity -- see Routes.DREAM's
# definition comment for why this can't reuse ROUTES/_zone_bounds/fill_route_checks). Strides
# are wider than the normal WEAPON_ROOM_STRIDE(100)/ASPECT_ROOM_STRIDE(100) because Dream's max
# depth (DREAM_MAX_REGIONS * DREAM_ROOM_LOCATIONS_PER_REGION = 144 today) already exceeds 100,
# and DREAM_ROOM_LOCATIONS_PER_REGION is a placeholder expected to grow -- generous headroom
# avoids an id-range rework the next time it's tuned. -------------------------------------
DREAM_MAX_REGIONS = 12                 # Options.DreamRegionCount.range_end
DREAM_ROOM_LOCATIONS_PER_REGION = 12   # N for every Dream region (see Routes.ROUTES' room-count note)
# K for every Dream region: a region's biome is random per attempt, so this is the minimum over
# biomes. Mirrored in the mod's Routes.DREAM_ROOM_GUARANTEED_PER_REGION.
DREAM_ROOM_GUARANTEED_PER_REGION = 2
DREAM_REGIONS_AVAILABLE_NO_ZJ = 8      # native DreamDiveTweaks biome pool without Nightmare/ZJ
DREAM_REGIONS_AVAILABLE_ZJ = 12        # native pool with Nightmare/ZJ folded in
DREAM_WEAPON_ROOM_STRIDE = 500         # per-weapon depth stride (vs. WEAPON_ROOM_STRIDE=100)
DREAM_ASPECT_ROOM_STRIDE = 500         # per-aspect-lane depth stride (vs. ASPECT_ROOM_STRIDE=100)
dream_score_id_base = 220000                   # "Dream Score NNNN" -- 1000 ids reserved
dream_room_id_base = 221500                    # "Dream Room DDDD" -- 2000 ids reserved
dream_weapon_room_id_base = 224000              # "Dream Room DDDD <Weapon>" -- base+weapon*500+depth
dream_aspect_room_id_base = 228000              # "<Aspect> <Weapon> Dream Room DD" -- base+lane*500+depth
dream_enemy_id_base = 241000                    # "Dream Enemy NNN" (cumulative counter)
dream_miniboss_id_base = 242000                 # "Dream Miniboss NN" (cumulative counter)
dream_boss_id_base = 243000                     # "Dream Boss NN" (cumulative counter, always exists)
# How many "Dream Enemy NNNN" / "Dream Miniboss NN" names the datapackage reserves. Fixed rather
# than derived from the roster: moving a species between the two counters (9/24: six miniboss-room
# headliners moved to Miniboss) would otherwise shrink one range and drop names that shipped.
# Only ever raise these; give_all_locations_table refuses a roster that outgrows them.
DREAM_ENEMY_ID_SLOTS = 100
DREAM_MINIBOSS_ID_SLOTS = 60

# Per-route, per-seed zone tables. Each maps a location name -> id (or None for
# the boss-event location). Rebuilt by setup_location_table_with_settings().
# Structured as zone_tables[route][zone_name] = { location: id_or_None }.
zone_tables = {}


def _pad(number: int) -> str:
    return f"{number:04d}"


def _pad2(number: int) -> str:
    return f"{number:02d}"


def _room_name(route: str, zone_display: str, local_depth: int, slot: int, weapon: str = None) -> str:
    """Build a room / per-weapon check name: '<Route> <Zone> Room DD[ +k][ Weapon]'.
    local_depth resets per zone (ROUTES[route]['zone_room_counts'] / Dream's per-region count),
    unlike the old route-wide continuous depth. slot 0 keeps the bare name (backward compatible
    with pre-scaling seeds); higher slots append ' +k'. Any weapon stays the LAST token so the
    rules' weapon parsing (rsplit / last-token) keeps working."""
    name = f"{route} {zone_display} Room {_pad2(local_depth)}"
    if slot > 0:
        name += " +" + str(slot)
    if weapon:
        name += " " + weapon
    return name


def _aspect_room_name(route: str, zone_display: str, local_depth: int, slot: int, weapon: str,
                      aspect_key: str) -> str:
    """Build a per_aspect_room_based check name: '<Aspect> <Weapon> <Route> <Zone> Room DD[ +k]'.
    Unlike _room_name, Aspect+Weapon are a FRONT prefix rather than a trailing token --
    Rules.py's per-aspect parser reads the first two space-separated tokens back out as
    (aspect, weapon)."""
    name = f"{aspect_key} {weapon} {route} {zone_display} Room {_pad2(local_depth)}"
    if slot > 0:
        name += " +" + str(slot)
    return name


def _flat_room_name(prefix: str, depth: int, slot: int, weapon: str = None) -> str:
    """Pre-per-zone-renumbering room name shape: '<prefix> NNNN[ +k][ Weapon]' (4-digit,
    route-agnostic depth). Used only by combine_pools' shared "Room NNNN" pool (out of scope
    for the per-zone renumbering -- see project plan), which has no zone concept of its own."""
    name = prefix + " " + _pad(depth)
    if slot > 0:
        name += " +" + str(slot)
    if weapon:
        name += " " + weapon
    return name


def _flat_aspect_room_name(prefix: str, depth: int, slot: int, weapon: str, aspect_key: str) -> str:
    """combine_pools counterpart of _flat_room_name: '<Aspect> <Weapon> <prefix> DD[ +k]'."""
    name = f"{aspect_key} {weapon} {prefix} {_pad2(depth)}"
    if slot > 0:
        name += " +" + str(slot)
    return name


def _empty_zone_tables() -> dict:
    tables = {}
    for route in ROUTE_NAMES:
        tables[route] = {}
        for i, zone in enumerate(ROUTES[route]["zones"]):
            # Each zone seeds with its boss-defeat event location.
            boss = ROUTES[route]["bosses"][i]
            tables[route][zone] = {boss_event(boss): None}
    return tables


def clear_tables() -> None:
    global zone_tables
    zone_tables = _empty_zone_tables()


# Room Based logic is "soft": a zone's whole room range counts as reachable the instant that
# zone's boss/weapon/arcana exit gate is met, with nothing tracking how deep a single real run
# actually gets. Players were finding the last couple rooms of a zone still out of reach at that
# point, so each interior boundary is pulled this many rooms earlier -- the last couple rooms of
# every zone fall into the next (harder-gated) tier instead, giving a buffer against that gap.
# Raised 2->3 (with room_count=50 this pulls the first zone down to 11 rooms) after a real
# playtest on Surface: a player without the 3rd area unlocked only ever reached Room 0021 in a
# run, 3 short of the old bound's Room 0024 -- the 2-room buffer wasn't enough slack against how
# short Rift of Thessaly's real room count can run.
ZONE_SAFETY_MARGIN_ROOMS = 3


def _zone_bounds(count: int) -> list:
    """Split `count` checks into 4 zone-aligned ranges; the first zone takes the
    remainder so totals always add up, then each interior boundary is pulled
    ZONE_SAFETY_MARGIN_ROOMS earlier (see ZONE_SAFETY_MARGIN_ROOMS)."""
    quarter = count // 4
    first = count - 3 * quarter
    raw = [0, first, first + quarter, first + 2 * quarter, count]
    bounds = [raw[0]]
    for b in raw[1:-1]:
        bounds.append(max(bounds[-1], b - ZONE_SAFETY_MARGIN_ROOMS))
    bounds.append(raw[-1])
    return bounds


def _zone_room_counts(route: str) -> list:
    """A route's hand-set per-zone room-check counts (ROUTES[route]['zone_room_counts']).
    Guarded against silently overflowing a zone's reserved id block: with ids keyed on
    (zone, local depth) via ZONE_ROOM_STRIDE, a zone bigger than that stride would collide
    into the NEXT zone's ids instead of erroring, so re-tuning a count too high must fail
    loudly here rather than corrupt the datapackage."""
    counts = ROUTES[route]["zone_room_counts"]
    for z, c in enumerate(counts):
        if c > ZONE_ROOM_STRIDE:
            raise ValueError(
                f"{route} zone {z} has {c} rooms, over the per-zone id budget "
                f"(ZONE_ROOM_STRIDE={ZONE_ROOM_STRIDE}). Raise ZONE_ROOM_STRIDE and MAX_ROOMS "
                f"together (4 * stride must equal MAX_ROOMS) and re-check each route's id range.")
    return list(counts)


def zone_room_prefixes(route: str) -> list:
    """The zone-relative room-check name prefixes for `route` (Underworld/Surface/Nightmare --
    not Dream, whose region list is a per-seed option rather than a fixed ROUTES entry), in zone
    order: [(prefix, zone_index), ...]. A plain room_based check name is
    `f"{prefix} {local:02d}"`, where local is 1..that zone's own room count -- room checks are
    counted per zone, so there is no route-wide depth to convert to. Shared by Rules.py/
    Client.py/CheatClient.py instead of each hand-rolling the same 4 zone prefixes."""
    zone_display = ROUTES[route]["zone_display"]
    return [(f"{route} {zone_display[z]} Room", z) for z in range(4)]


def _dream_bounds(count: int, n: int) -> list:
    """n-way generalization of _zone_bounds for Dream (n = dream_region_count instead of a
    fixed 4 zones). No ZONE_SAFETY_MARGIN_ROOMS pull-back -- that exists for room-based
    routes' "soft" depth-guessing reachability gap; Dream regions are gated by the
    resource-percent curve instead (Rules._set_dream_rules), not room-depth guessing, so
    there's no equivalent gap here. First region takes any remainder so totals add up."""
    if n <= 0:
        return [0]
    base = count // n
    extra = count - base * n
    bounds = [0]
    for i in range(n):
        bounds.append(bounds[-1] + base + (1 if i < extra else 0))
    return bounds


def fill_score_checks(route: str, count: int) -> None:
    """point_based: distribute `count` score checks for a route across its 4 zones."""
    prefix = ROUTES[route]["score_prefix"]
    id_base = hades2_base_location_id + ROUTES[route]["score_id_base"]
    zones = ROUTES[route]["zones"]
    bounds = _zone_bounds(count)
    for z in range(4):
        zone = zones[z]
        for i in range(bounds[z], bounds[z + 1]):
            zone_tables[route][zone][prefix + " " + _pad(i + 1)] = id_base + i


def fill_room_checks(route: str, multiplier: int = 1, zone_counts: list = None) -> None:
    """room_based: one check per room-depth (1..that zone's own room count), reset each zone
    (ROUTES[route]['zone_room_counts'] -- real per-zone data, not a formula split). With
    multiplier m, each depth gets m checks (slots 0..m-1) in disjoint id blocks. `zone_counts`
    overrides the real per-zone counts -- give_all_locations_table passes the full
    ZONE_ROOM_STRIDE per zone so the datapackage reserves headroom for future re-tuning.
    Because ids key on (zone, local depth) rather than a running index, that headroom build
    produces the exact same id for a given name as a real, smaller seed does -- see
    ZONE_ROOM_STRIDE's comment for why that equivalence is load-bearing."""
    id_base = hades2_base_location_id + ROUTES[route]["room_id_base"]
    zones = ROUTES[route]["zones"]
    zone_display = ROUTES[route]["zone_display"]
    counts = zone_counts if zone_counts is not None else _zone_room_counts(route)
    for slot in range(multiplier):
        for z in range(4):
            zone = zones[z]
            for local_depth in range(1, counts[z] + 1):
                name = _room_name(route, zone_display[z], local_depth, slot)
                zone_tables[route][zone][name] = (
                    id_base + slot * MAX_ROOMS + z * ZONE_ROOM_STRIDE + local_depth - 1)


def fill_weapon_room_checks(route: str, multiplier: int = 1, included_weapons=None,
                            zone_counts: list = None) -> None:
    """per_weapon_room_based: one check per (room-depth, weapon), depth reset each zone.
    With multiplier m, each (depth, weapon) gets m checks in disjoint id blocks. Weapons
    excluded via IncludedWeapons (Options.py) get no checks at all this seed -- `w`'s id
    offset still comes from the weapon's fixed WEAPON_SHORT_NAMES position, so ids stay
    stable regardless of which weapons this particular seed includes. included_weapons=None
    (give_all_locations_table's datapackage build) means "every weapon" -- the max universe.
    `zone_counts` overrides the real per-zone counts -- see fill_room_checks' docstring."""
    id_base = hades2_base_location_id + ROUTES[route]["weapon_room_id_base"]
    zones = ROUTES[route]["zones"]
    zone_display = ROUTES[route]["zone_display"]
    counts = zone_counts if zone_counts is not None else _zone_room_counts(route)
    for slot in range(multiplier):
        for w, weapon in enumerate(WEAPON_SHORT_NAMES):
            if included_weapons is not None and weapon not in included_weapons:
                continue
            for z in range(4):
                zone = zones[z]
                for local_depth in range(1, counts[z] + 1):
                    name = _room_name(route, zone_display[z], local_depth, slot, weapon)
                    zone_tables[route][zone][name] = (
                        id_base + slot * WEAPON_ROOM_SLOT_STRIDE + w * WEAPON_ROOM_STRIDE
                        + z * ZONE_ROOM_STRIDE + local_depth - 1)


def fill_aspect_room_checks(route: str, multiplier: int = 1, included_weapons=None,
                            included_aspects: int = 4, zone_counts: list = None) -> None:
    """per_aspect_room_based: one check per (room-depth, weapon, aspect), depth reset each
    zone. A lane's id offset comes from the weapon's fixed WEAPON_SHORT_NAMES position and the
    aspect's fixed slot within Items.weapon_aspect_slots (0=base Aspect of Melinoe, 1-3=alts in
    ASPECT_TITLES_BY_WEAPON order), so ids stay stable regardless of which weapons/aspects this
    seed actually includes. included_weapons=None / included_aspects=4 (give_all_locations_
    table's datapackage build) means "every weapon, every aspect slot" -- the max universe.
    `zone_counts` overrides the real per-zone counts -- see fill_room_checks' docstring."""
    id_base = hades2_base_location_id + ROUTES[route]["aspect_room_id_base"]
    zones = ROUTES[route]["zones"]
    zone_display = ROUTES[route]["zone_display"]
    counts = zone_counts if zone_counts is not None else _zone_room_counts(route)
    for slot in range(multiplier):
        for w, weapon in enumerate(WEAPON_SHORT_NAMES):
            if included_weapons is not None and weapon not in included_weapons:
                continue
            for a, (_aspect_key, display_key) in enumerate(weapon_aspect_slots(weapon)):
                if a >= included_aspects:
                    continue
                lane = w * ASPECT_LANES_PER_WEAPON + a
                for z in range(4):
                    zone = zones[z]
                    for local_depth in range(1, counts[z] + 1):
                        name = _aspect_room_name(route, zone_display[z], local_depth, slot,
                                                 weapon, display_key)
                        zone_tables[route][zone][name] = (
                            id_base + slot * ASPECT_ROOM_SLOT_STRIDE + lane * ASPECT_ROOM_STRIDE
                            + z * ZONE_ROOM_STRIDE + local_depth - 1)


def combine_active(options) -> bool:
    """combine_pools only does anything when both routes are actually generated; with a
    single route there's nothing to combine, so it behaves like split_pools."""
    return options.separate_checks.value == COMBINE_POOLS and len(active_routes(options)) > 1


def _combined_room_count(options=None) -> int:
    """Size of the shared (combined) room pool: the SMALLEST combined_room_depth among the seed's
    active 4-zone routes. combine_pools' whole premise is that the shared pool is earnable on a
    single route (any one of them), so it can only be as deep as the shallowest route -- a depth
    past that is unreachable on that route, and if it's the only route left in the seed,
    unreachable outright. combined_room_depth is deliberately NOT the sum of zone_room_counts:
    those are per-zone maxima (the zone boss releases the tail), while the shared pool is
    route-wide depth with no such release, so it keeps its pre-0.10 sizes (43/39/40).
    options=None (datapackage/no-seed-context callers) falls back to the min across ALL routes,
    the widest safe assumption."""
    routes = [r for r in active_routes(options) if r in ROUTES] if options is not None else []
    if not routes:
        routes = list(ROUTE_NAMES)
    return min(ROUTES[r]["combined_room_depth"] for r in routes)


def _score_count_for(route: str, options) -> int:
    """point_based score-check count for one route's OWN pool. split_pools: each route gets
    the full score_rewards_amount. combine_pools: no per-route pool exists at all -- there's a
    single shared, route-agnostic one instead (see _combined_score_count), so this is 0."""
    if combine_active(options):
        return 0
    return options.score_rewards_amount.value


def _combined_score_count(options) -> int:
    """Size of the shared (combined) point_based score pool: the full score_rewards_amount.
    Every active route banks into this one pool, so all of it is earnable on a single route --
    combine_pools shares the checks rather than dividing them up."""
    return options.score_rewards_amount.value


def combined_score_table(options) -> dict:
    """The shared score pool's locations (name -> id) for this seed: route-agnostic
    "Score NNNN". Unlike the room pools there's no multiplier -- point_based scales by
    raising score_rewards_amount instead (see __init__.generate_early)."""
    return {
        f"{COMBINED_SCORE_PREFIX} {_pad(i + 1)}":
            hades2_base_location_id + combined_score_id_base + i
        for i in range(_combined_score_count(options))
    }


def combined_room_table(options, multiplier: int = 1) -> dict:
    """The shared room pool's locations (name -> id) for this seed: route-agnostic
    "Room NNNN" (room_based) or "Room NNNN <Weapon>" (per_weapon_room_based). With
    multiplier m, each depth (and weapon) gets m checks in disjoint id blocks."""
    system = options.location_system.value
    count = _combined_room_count(options)
    table = {}
    if system == ROOM_BASED:
        for slot in range(multiplier):
            for i in range(count):
                table[_flat_room_name(COMBINED_ROOM_PREFIX, i + 1, slot)] = \
                    hades2_base_location_id + combined_room_id_base + slot * MAX_ROOMS + i
    elif system == PER_WEAPON_ROOM_BASED:
        included_weapons = options.included_weapons.value
        for slot in range(multiplier):
            for w, weapon in enumerate(WEAPON_SHORT_NAMES):
                if weapon not in included_weapons:
                    continue
                for i in range(count):
                    table[_flat_room_name(COMBINED_ROOM_PREFIX, i + 1, slot, weapon)] = \
                        hades2_base_location_id + combined_weapon_id_base \
                        + slot * WEAPON_ROOM_SLOT_STRIDE + w * WEAPON_ROOM_STRIDE + i
    elif system == PER_ASPECT_ROOM_BASED:
        included_weapons = options.included_weapons.value
        included_aspects = int(options.included_aspects.value)
        for slot in range(multiplier):
            for w, weapon in enumerate(WEAPON_SHORT_NAMES):
                if weapon not in included_weapons:
                    continue
                for a, (_aspect_key, display_key) in enumerate(weapon_aspect_slots(weapon)):
                    if a >= included_aspects:
                        continue
                    lane = w * ASPECT_LANES_PER_WEAPON + a
                    for i in range(count):
                        name = _flat_aspect_room_name(COMBINED_ROOM_PREFIX, i + 1, slot, weapon, display_key)
                        table[name] = hades2_base_location_id + combined_aspect_id_base \
                            + slot * ASPECT_ROOM_SLOT_STRIDE + lane * ASPECT_ROOM_STRIDE + i
    return table


def fill_route_checks(route: str, options, multiplier: int = 1, dream_met: bool = True) -> None:
    """Fill a route's zone tables according to the chosen location system. Under
    combine_pools NOTHING is filled per-route here -- every system's checks live in a shared
    region instead ("Combined Rooms" / "Combined Score"); only the per-route boss events
    remain."""
    if route == DREAM:
        # Dream can't reuse _zone_bounds/fill_*_checks below (variable region count, no fixed
        # ROUTES entry) -- see Routes.DREAM's definition comment. combine_pools handling is
        # inside fill_dream_checks itself (same early-return shape as this function).
        fill_dream_checks(options, dream_met)
        return
    system = options.location_system.value
    if combine_active(options):
        return
    if system in (ROOM_BASED, PER_WEAPON_ROOM_BASED, PER_ASPECT_ROOM_BASED):
        if system == ROOM_BASED:
            fill_room_checks(route, multiplier)
        elif system == PER_WEAPON_ROOM_BASED:
            fill_weapon_room_checks(route, multiplier, options.included_weapons.value)
        else:
            fill_aspect_room_checks(route, multiplier, options.included_weapons.value,
                                    int(options.included_aspects.value))
    else:
        fill_score_checks(route, _score_count_for(route, options))


# Mirrors Lua LocationManager.DREAM_BOSS_NAMES (keep in sync by hand): species the mod counts on
# the Dream BOSS counter, so they can never advance the Miniboss counter even though several are
# in MINIBOSS_ENEMY_NAMES.
DREAM_BOSS_NAMES = {
    "Headmistress Hecate", "Scylla", "Roxy", "Jetty", "Infernal Beast", "Chronos",
    "The Cyclops Polyphemus", "Eris", "Prometheus", "Typhon", "Megaera", "Alecto", "Tisiphone",
    "Bone Hydra", "Theseus", "Asterius", "Hades",
}
# Regular species that only spawn in the Underworld's Asphodel "Anomaly" detour, which a Dream
# Dive never visits -- they can't advance the Dream Enemy counter.
DREAM_UNOBTAINABLE_REGULAR = {
    "Wretched Witch", "Bloodless", "Bone-Raker", "Wave-Maker", "Inferno-Bomber", "Slam-Dancer",
    "Burn-Flinger",
}


def _dream_roster_counts(routes_included, obtainable_only: bool = True) -> tuple:
    """(Y, Z): how many distinct species can advance Dream's Enemy / Miniboss counters across the
    given routes' ENEMY_LAYERS (recomputed from the roster every time). Without ZJ this is
    (Underworld, Surface); with ZJ, Nightmare's roster folds in too. obtainable_only=False gives
    the raw name counts, which the datapackage reserves ids for."""
    y = z = 0
    for route in routes_included:
        for layer in ENEMY_LAYERS[route]:
            for name in layer:
                if name in MINIBOSS_ENEMY_NAMES:
                    if not obtainable_only or name not in DREAM_BOSS_NAMES:
                        z += 1
                elif not obtainable_only or name not in DREAM_UNOBTAINABLE_REGULAR:
                    y += 1
    return y, z


def fill_dream_checks(options, dream_met: bool = True) -> None:
    """Dream's dedicated location-filling function. Not fill_route_checks/_zone_bounds --
    Dream has a variable region count (dream_region_count, 1-12, clamped to whatever the
    native DreamDiveTweaks pool actually supports) and no fixed boss identity per region (see
    Routes.DREAM's definition comment). Populates zone_tables[DREAM] with the same
    {location_name: id} dict shape every other route uses, so Regions.py/Rules.py read it
    identically -- they just populate it differently. dream_met=False rebuilds a seed generated
    before Dream had boss "Met" checks (Hades2World._resolve_dream_met_checks)."""
    zj_active = NIGHTMARE in active_routes(options)
    regions_available = DREAM_REGIONS_AVAILABLE_ZJ if zj_active else DREAM_REGIONS_AVAILABLE_NO_ZJ
    n = min(int(options.dream_region_count.value), regions_available)
    zones = [f"Dream Region {i}" for i in range(1, n + 1)]
    zone_tables[DREAM] = {zone: {} for zone in zones}
    # Seed the final region with the "Beat Dream" event location, same as _empty_zone_tables
    # seeds every normal route's last zone with its boss event -- Regions.create_regions reads
    # locs straight out of zone_tables[DREAM][zone], so without this the event is never placed
    # in any region even though setup_location_table_with_settings's flat table still lists it
    # (KeyError in create_items' place_locked_item, since the location object never existed).
    zone_tables[DREAM][zones[-1]][boss_event("Dream")] = None
    # Boss "Met" checks only a dive can send this seed (dream_boss_met_locations_for), in the
    # final region -- see DREAM_MET_ROUTES for why there.
    if dream_met and options.npc_locations:
        zone_tables[DREAM][zones[-1]].update(dream_boss_met_locations_for(options))

    # Score/Room: location_system-dependent, same dispatch shape as fill_route_checks. Under
    # combine_pools, Dream's Score/Room checks are skipped here too (deferred -- see plan/
    # project memory: combine_pools' shared-pool math growing with dream_region_count is
    # explicitly out of scope for this pass).
    if not combine_active(options):
        system = options.location_system.value
        if system == POINT_BASED:
            count = _score_count_for(DREAM, options)
            bounds = _dream_bounds(count, n)
            for z in range(n):
                zone = zones[z]
                for i in range(bounds[z], bounds[z + 1]):
                    zone_tables[DREAM][zone][f"Dream Score {_pad(i + 1)}"] = \
                        hades2_base_location_id + dream_score_id_base + i
        else:
            per_region = DREAM_ROOM_LOCATIONS_PER_REGION
            if system == ROOM_BASED:
                for z in range(n):
                    zone = zones[z]
                    zone_display = f"Region {z + 1}"
                    for i in range(per_region):
                        depth = z * per_region + i + 1        # global depth: id math only
                        name = _room_name(DREAM, zone_display, i + 1, 0)
                        zone_tables[DREAM][zone][name] = \
                            hades2_base_location_id + dream_room_id_base + depth - 1
            elif system == PER_WEAPON_ROOM_BASED:
                included_weapons = options.included_weapons.value
                for z in range(n):
                    zone = zones[z]
                    zone_display = f"Region {z + 1}"
                    for w, weapon in enumerate(WEAPON_SHORT_NAMES):
                        if weapon not in included_weapons:
                            continue
                        for i in range(per_region):
                            depth = z * per_region + i + 1     # global depth: id math only
                            name = _room_name(DREAM, zone_display, i + 1, 0, weapon)
                            zone_tables[DREAM][zone][name] = hades2_base_location_id + \
                                dream_weapon_room_id_base + w * DREAM_WEAPON_ROOM_STRIDE + depth - 1
            else:  # PER_ASPECT_ROOM_BASED
                included_weapons = options.included_weapons.value
                included_aspects = int(options.included_aspects.value)
                for z in range(n):
                    zone = zones[z]
                    zone_display = f"Region {z + 1}"
                    for w, weapon in enumerate(WEAPON_SHORT_NAMES):
                        if weapon not in included_weapons:
                            continue
                        for a, (_aspect_key, display_key) in enumerate(weapon_aspect_slots(weapon)):
                            if a >= included_aspects:
                                continue
                            lane = w * ASPECT_LANES_PER_WEAPON + a
                            for i in range(per_region):
                                depth = z * per_region + i + 1     # global depth: id math only
                                name = _aspect_room_name(DREAM, zone_display, i + 1, 0, weapon,
                                                         display_key)
                                zone_tables[DREAM][zone][name] = hades2_base_location_id + \
                                    dream_aspect_room_id_base + lane * DREAM_ASPECT_ROOM_STRIDE + depth - 1

    # Enemy/Miniboss/Boss cumulative counters (only meaningful when enemysanity adds
    # locations at all -- gated by the caller via enemysanity_has_locations, same as every
    # other route's enemy_locations_for).
    if not enemysanity_has_locations(options):
        return
    routes_for_roster = [UNDERWORLD, SURFACE] + ([NIGHTMARE] if zj_active else [])
    y, z_count = _dream_roster_counts(routes_for_roster)
    enemy_loc_setting = min(int(options.dream_enemy_locations.value), regions_available)
    dream_enemy_count = (y * enemy_loc_setting) // regions_available
    # Boss counter always exists regardless of include_minibosses (route-ending bosses are
    # core content, not optional) -- and needs no Y/regions ratio since each route contributes
    # exactly 4 named bosses, already equal to regions_available (8 or 12) in both cases.
    dream_boss_count = enemy_loc_setting
    # Miniboss counter only exists when include_minibosses is on; when off it's dropped
    # entirely (0 locations, not folded into the Enemy counter) -- matches filter_minibosses'
    # existing drop behavior for every other route's miniboss-tagged enemies.
    include_mb = bool(options.include_minibosses)
    dream_miniboss_count = ((z_count * enemy_loc_setting) // regions_available) if include_mb else 0

    for count, id_base, prefix, pad_fn in (
        (dream_enemy_count, dream_enemy_id_base, "Dream Enemy", _pad),
        (dream_miniboss_count, dream_miniboss_id_base, "Dream Miniboss", _pad2),
        (dream_boss_count, dream_boss_id_base, "Dream Boss", _pad2),
    ):
        if count <= 0:
            continue
        bounds = _dream_bounds(count, n)
        for z in range(n):
            zone = zones[z]
            for i in range(bounds[z], bounds[z + 1]):
                zone_tables[DREAM][zone][f"{prefix} {pad_fn(i + 1)}"] = \
                    hades2_base_location_id + id_base + i


# (Weapon-unlock locations removed: weapons are still shuffled as items, but buying them
# at the Crossroads weapon shop is blocked outright and earns no check, so players never
# need to grind Silver / mining tools to obtain them.)

# (Incantation checks removed: incantationsanity was dropped, and the Cauldron is blocked
# entirely in-game. Surface access still comes from the Surface Access / Penalty Cure items.)

# Keepsake unlock checks (keepsakesanity, randomized/progressive). Gifting an NPC
# enough Nectar sends the check. Chronos's "Time Piece" is intentionally NOT a location
# (unreachable here), though it still exists as an item.
# Aspects and Familiars are items-only (no check locations) by design.
keepsake_location_base = hades2_base_location_id + 6100
location_keepsakes = {
    f"{KEEPSAKE_NPC[title]} Keepsake": keepsake_location_base + i
    for i, title in enumerate(keepsake_titles)
    if title not in KEEPSAKE_NO_LOCATION
}


# --- Enemy locations (enemysanity) --------------------------------------------
# First-time defeat checks, one per enemy type. Each enemy is mapped to the route + zone
# (layer) it appears in, so the location lives in that zone's region and is reachable
# exactly when that zone is. (Boss enemies are listed here as distinct checks from the
# "Beat <Boss>" route events.) Ids come from ENEMY_LOCATION_OFFSETS below, not list order.
ENEMY_LAYERS = {
    UNDERWORLD: [
        ["Casket", "Lanthorn", "Sister of the Dead", "Spindle", "Wailer", "Wastrel",
         "Whisper", "Thorn-Weeper", "Root-Stalker", "Shadow-Spiller", "Headmistress Hecate",
         "Master-Slicer"],
        # Zone 2 (Oceanus) + the Asphodel "Anomaly" detour foes. Asphodel only becomes reachable
        # once Oceanus is your second area, so its enemies share Oceanus's sphere (Test Run 5
        # #13). Display names from HelpText: SpreadShotUnit=Wretched Witch, BloodlessNaked=Bloodless,
        # BloodlessBerserker=Bone-Raker, BloodlessWaveFist=Wave-Maker, BloodlessGrenadier=
        # Inferno-Bomber, BloodlessSelfDestruct=Slam-Dancer, BloodlessPitcher=Burn-Flinger.
        ["Hippo", "Lurker", "Pinhead", "Sea-Serpent", "Shellback", "Sop-Spindle",
         "Wet-Whisper", "Wretched Pest", "Deep Serpent", "Hellifish", "King Vermin",
         # Scylla's fight (EncounterData_Boss.lua's BossScylla01/02) spawns three independent
         # units sharing one group health bar: Scylla herself, and her two bandmates -- the
         # drummer and keytarist, nicknamed "Roxy" and "Jetty" in her own hype voice lines.
         # Each gets its own Defeated check (previously one combined "Scylla and the Sirens").
         "Scylla", "Roxy", "Jetty",
         "Wretched Witch", "Bloodless", "Bone-Raker", "Wave-Maker", "Inferno-Bomber",
         "Slam-Dancer", "Burn-Flinger"],
        # Dread-Wailer (Screamer2) belongs here, not Zone 1: its real spawn is
        # EncounterData_Generated.lua GeneratedH_Screamer2 (InheritFrom GeneratedH = Mourning
        # Fields/Biome H), gated on CurrentRun.BiomeDepthCache >= 4 within this zone plus the
        # GameState.EncountersCompletedCache.ScreamerIntro meta flag. It was previously placed
        # in Zone 1 (Erebus) based on misreading CodexData.lua's EnemiesUW bestiary-page list
        # (a Codex UI grouping, not a spawn-biome list) -- that put it in logic from turn one.
        ["Bawlder", "Blight-Shade", "Bloat-Shade", "Blood-Shade", "Canine", "Holeheart",
         "Lamia", "Lycaon", "Mourner", "Smacker", "Sorrow-Spiller", "Phantom",
         "Queen Lamia", "Brush-Stalker", "Infernal Beast", "Dread-Wailer"],
        ["Crawler", "Goldwraith", "Numbskull", "Sandskull", "Satyr Hoplite",
         "Satyr Supplicant", "Satyr Vierophant", "Tempus", "Wretched Thug", "Goldwrath",
         "The Verminancer", "Wringer", "Chronos"],
    ],
    SURFACE: [
        ["Bronzebeak", "Cutthroat", "Eidolon", "Lubber", "Shambler", "Tombstone",
         "Satyr Champion", "Erymanthian Boar", "The Cyclops Polyphemus"],
        ["Anchor", "Blasket", "Boozer", "Droplet", "Harpy Talon", "Sea-Shambler",
         "Seesword", "Stickler", "Charybdis", "The Yargonaut", "Eris"],
        ["Auto-Forcer", "Auto-Seeker", "Auto-Watcher", "Harpy Raptor", "Satyr Goldpike",
         "Satyr Raider", "Satyr Sapper", "Sky-Dracon", "Snow-Shambler", "Mega-Dracon",
         "Talos", "Prometheus"],
        ["Eyesore", "Headstone", "Horror", "Land-Dracon", "Polyp", "Stalker",
         "Eye of Typhon", "Spawn of Typhon", "Tail of Typhon", "Twins of Typhon", "Typhon"],
    ],
    # Nightmare (Zagreus' Journey, opt-in). Roster from the original Hades 1 game, one list per
    # biome. 13 enemy names here are EXACT duplicates of existing Underworld entries above
    # (Hades II's own Tartarus/Oceanus already recycle these H1 monster types) -- those are
    # deliberately NOT repeated here to avoid a location-name collision (see
    # SHARED_ENEMY_ZONES below, which instead makes the existing Underworld location
    # also reachable via its Nightmare zone). Within-Nightmare repeats (Brimstone/Numbskull in
    # both Tartarus+Asphodel; Voidstone in Asphodel+Elysium) are listed only in their
    # earliest zone -- later zones are already gated behind it. Elite mini-boss variants
    # (Styx's elite Gigantic Vermin/Bother/Snakestone/Satyr Cultist) don't get separate
    # checks, matching the existing elite-suffix-strip precedent
    # ([[reference_enemy_codex_source]]-adjacent fix, see project_enemy_elite_variant_bug).
    # "Barge of Death" (Asphodel) is a survival encounter, not a killable unit -- no check.
    NIGHTMARE: [
        # Tartarus: Numbskull/Wringer/Wretched Witch/Wretched Thug/Wretched Pest excluded
        # (collide with Underworld's Tartarus/Oceanus -- see SHARED_ENEMY_ZONES).
        ["Skullomat", "Wretched Lout", "Brimstone",
         "Dire Inferno-Bomber", "Doomstone", "Wretched Sneak",
         "Megaera", "Alecto", "Tisiphone"],
        # Asphodel: Bloodless/Bone-Raker/Inferno-Bomber/Wave-Maker/Burn-Flinger/Slam-Dancer
        # excluded (collide with Underworld's Oceanus). Numbskull/Brimstone already listed
        # in Tartarus above.
        ["Spreader", "Voidstone", "Skull-Crusher", "Gorgon", "Dracon",
         "Megagorgon", "Dire Spreader", "Bone Hydra"],
        # Elysium: Voidstone already listed in Asphodel above. Soul Catcher covers both its
        # standard and mini-boss appearance (same entity); Asterius's "Warden" mini-boss
        # appearance is the same entity as the zone's main boss, no separate check.
        ["Splitter", "Nemean Chariot", "Flame Wheel", "Brightsword", "Longspear",
         "Strongbow", "Greatshield", "Soul Catcher", "Theseus", "Asterius"],
        # Styx: Crawler/King Vermin excluded (Crawler collides with Underworld's Tartarus;
        # King Vermin collides with Underworld's Oceanus).
        ["Gigantic Vermin", "Bother", "Snakestone", "Satyr Cultist", "Hades"],
    ],
}

# 12 enemy names that exist identically in the Underworld roster above (Hades II's own
# Tartarus/Oceanus already recycle these H1 monster types) and ALSO appear in Nightmare --
# name -> every (route, zone index) it can be found in. A location's PARENT REGION is a
# hard reachability gate in AP (region unreachable => location unreachable, regardless of
# any access_rule), so a name that's reachable via either of two different zones can't stay
# placed in one of those zones' regions with an "or" rule bolted on -- that would only ever
# relax its OWN rule, not bypass the other zone's region requirement. Instead these 12 are
# pulled out of their normal zone placement entirely (see the enemy-index loop below, which
# tracks them in SHARED_ENEMY_LOCATIONS instead of ENEMY_BY_ZONE) and placed in the
# Crossroads hub instead (always immediately reachable), with their real gating done purely
# via an access_rule checking "any of these zones reachable" (Rules._set_shared_enemy_rules)
# -- the same "neutral bucket + access_rule" shape already used for the Combined Rooms pool.
# ids/route-ownership (location_enemies/ENEMY_ROUTE) are unchanged, but existence is gated
# on the NIGHTMARE route alone (July 18 user ruling): the H1 route spawns these names
# consistently, while their Underworld-side appearances (Asphodel-anomaly detours, the odd
# H2 Tartarus/Oceanus callback) are too rare to justify putting 12 checks in a seed that
# can't reach the H1 route. When Nightmare IS active, kills on EITHER route still count
# (the mod's send gate is seed-level) -- and reachability likewise only trusts the
# Nightmare zones (Rules._set_shared_enemy_rules).
SHARED_ENEMY_ZONES = {
    "Numbskull Defeated": [(UNDERWORLD, 3), (NIGHTMARE, 0)],
    "Wringer Defeated": [(UNDERWORLD, 3), (NIGHTMARE, 0)],
    "Wretched Thug Defeated": [(UNDERWORLD, 3), (NIGHTMARE, 0)],
    "Crawler Defeated": [(UNDERWORLD, 3), (NIGHTMARE, 3)],
    "Wretched Witch Defeated": [(UNDERWORLD, 1), (NIGHTMARE, 0)],
    "Wretched Pest Defeated": [(UNDERWORLD, 1), (NIGHTMARE, 0)],
    "Bloodless Defeated": [(UNDERWORLD, 1), (NIGHTMARE, 1)],
    "Bone-Raker Defeated": [(UNDERWORLD, 1), (NIGHTMARE, 1)],
    "Wave-Maker Defeated": [(UNDERWORLD, 1), (NIGHTMARE, 1)],
    "Inferno-Bomber Defeated": [(UNDERWORLD, 1), (NIGHTMARE, 1)],
    "Slam-Dancer Defeated": [(UNDERWORLD, 1), (NIGHTMARE, 1)],
    "Burn-Flinger Defeated": [(UNDERWORLD, 1), (NIGHTMARE, 1)],
}

# Each shared name's spawn slot as the enemy SHUFFLE sees it: its Nightmare zone, the one zone
# logic trusts for it. 9/26: these 12 used to be held out of the shuffle entirely, and they are
# most of Nightmare's Tartarus and Asphodel rosters, so those zones barely shuffled at all
# (reported live: "Nightmare doesn't seem to be giving me random enemies"). Once a shared name is
# in the permutation, enemy_zone_placement treats this slot like any zone bucket entry: whatever
# replaces the name is killable here, and the name itself moves to its preimage's zone.
SHARED_ENEMY_SLOT = {
    name: (NIGHTMARE, ROUTES[NIGHTMARE]["zones"][zi])
    for name, zones in SHARED_ENEMY_ZONES.items()
    for route, zi in zones if route == NIGHTMARE
}

# King Vermin is a miniboss on both routes: G_MiniBoss02 in Oceanus (Underworld) and
# HadesCrawlerMiniBoss in Styx (Zagreus' Journey). It is a normal Underworld Oceanus check (so it
# follows the miniboss ROOM shuffle like the other 17 arenas); when only Nightmare is in the seed
# it lives in Nightmare's Styx instead. A Styx kill still sends it either way.
KING_VERMIN_LOCATION = "King Vermin Defeated"
NIGHTMARE_KING_VERMIN_ZONE_INDEX = 3

# "Mini-boss" enemy checks (July 17): the only enemy names whose reachability is gated behind
# their zone's own boss being beaten (Rules.py) rather than just the zone being reachable --
# every OTHER enemy (regular/trash spawns) only needs its zone reachable, same as before the
# July 17 tightening pass. Two kinds of name land here:
#  - Real secondary mini-boss encounters, identified from the mod's own unit-id data
#    (Hades2Rogue_mod/LocationManager.lua's "_Miniboss"/"MiniBoss"/"Miniboss"-suffixed unit ids,
#    e.g. ZombieAssassin_Miniboss -> Master-Slicer, Boar -> Erymanthian Boar "City of Ephyra
#    miniboss") -- these are genuinely tougher, optional-feeling fights within a zone.
#  - Names that are the SAME encounter as the zone's own listed boss (e.g. "Chronos", "The
#    Cyclops Polyphemus", "Scylla"/"Roxy"/"Jetty") -- their enemy-defeat check can only ever
#    fire by beating that exact boss, so gating them on anything looser would be logically
#    wrong regardless of the July 17 tightening.
MINIBOSS_ENEMY_NAMES = {
    # Underworld
    "Headmistress Hecate", "Master-Slicer", "Thorn-Weeper",       # Erebus (boss-identical + mini-bosses):
    # Thorn-Weeper only spawns as a regular enemy after you first defeat it in a dedicated
    # mini-boss room, so its "Defeated" check needs the same boss-tier gate as a real mini-boss.
    "Scylla", "Roxy", "Jetty", "Hellifish", "Deep Serpent",       # Oceanus (boss-identical + mini-bosses)
    "Queen Lamia", "Infernal Beast",                              # Fields of Mourning (mini-boss + boss-identical:
    # "Infernal Beast" is the enemy-check name for the InfestedCerberus unit -- the same fight as
    # the zone's "Met/Beat Cerberus" boss event (see _NPC_BOSS_NAMES/"Met Cerberus"). Missed in
    # the original audit because its boss-event name ("Cerberus") differs from its enemy-check
    # name; confirmed only ever spawning via EncounterData_Boss.lua's dedicated Cerberus fight
    # (grepped the whole installed game -- InfestedCerberus appears nowhere else), same class of
    # bug as [[project_boss_rival_met_fix]]/the Chronos-Polyphemus-Scylla precedent above.
    "Chronos", "Goldwrath", "The Verminancer",                    # Tartarus (boss-identical + mini-bosses)
    # Surface
    "The Cyclops Polyphemus", "Erymanthian Boar",                 # City of Ephyra
    "Eris",                                                       # Rift of Thessaly (boss-identical)
    "Mega-Dracon", "Prometheus",                                  # Mount Olympus (boss-identical + mini-boss)
    "Typhon", "Spawn of Typhon", "Twins of Typhon",               # The Summit
    # Nightmare
    "Megaera", "Alecto", "Tisiphone",                             # Tartarus (Nightmare) -- boss-identical:
    # the zone's boss is a random pick of one of these three, so whichever is fought IS "Beat
    # The Furies"; all three stay boss-gated since any could be the real fight. Alecto/Tisiphone
    # are additionally pushed to the zone-2 (Tier 3) requirement -- see MINIBOSS_ZONE_OVERRIDE.
    "Wretched Sneak", "Doomstone", "Dire Inferno-Bomber",         # Tartarus (Nightmare, mini-bosses)
    "Bone Hydra", "Dire Spreader",                                # Asphodel
    "Theseus", "Asterius",                                        # Elysium (fought together)
    "Hades",                                                      # Styx (final boss)
    "King Vermin",     # Oceanus / Styx (CrawlerMiniboss / HadesCrawlerMiniBoss) -- see KING_VERMIN_LOCATION
    # 2026-08-16 audit: four miniboss-only units were missing from this list entirely, so
    # compute_enemysanity_shuffle_map's split_pools put them in the REGULAR pool and shuffled-mode
    # seeds could drop a miniboss into an ordinary trash slot (observed live). Derived by walking
    # every MiniBoss* encounter referenced by a RoomData*.lua LegalEncounters line and mapping its
    # headline spawn through LocationManager.lua's UNIT_TO_ENEMY_CHECK; each was then confirmed
    # absent from every generic BiomeX pool in the game's EnemySets.lua, i.e. it can ONLY be
    # reached via its own miniboss room -- which is also why the boss-tier logic gate this list
    # applies is the correct rule for them.
    "Root-Stalker",    # Treant, MiniBossTreant (Erebus)
    "Phantom",         # Vampire, MiniBossVampire (Fields of Mourning)
    "Satyr Champion",  # SatyrCrossbow, MiniBossSatyrCrossbow (City of Ephyra)
    "Headstone",       # EarthElemental, MiniBossStalker (The Summit)
    # 2026-09-24: the remaining miniboss-room headliners (see MINIBOSS_ROOMS). They were kept out
    # of this set so include_minibosses=off still left them in the pool, and the Dream counters
    # counted them as ordinary enemies -- neither is what "Include Minibosses" says.
    "Shadow-Spiller",  # FogEmitter_Elite, F_MiniBoss02 (Erebus)
    "Charybdis",       # O_MiniBoss01 (Rift of Thessaly)
    "The Yargonaut",   # Captain, O_MiniBoss02 (Rift of Thessaly)
    "Talos",           # P_MiniBoss01 (Mount Olympus)
    "Tail of Typhon",  # TyphonTail, Q_MiniBoss03 (The Summit)
    "Eye of Typhon",   # TyphonEye, Q_MiniBoss04 (The Summit)
}

# Per-name override: use a LATER zone's boss-tier requirement instead of the mini-boss's own
# zone (name -> (route, zone index) to borrow the tier from). Alecto and Tisiphone still live
# in Nightmare's zone 0 (Tartarus) region, but are deliberately made logically available only
# once the zone-2 boss (Theseus and Asterius, Elysium, Tier 3/60%) is beatable, not zone 0's own
# (Tier 1/20%) -- Megaera is the sole eligible Tartarus boss below that threshold, and the
# in-game mod hook (ItemManager.apply_nightmare_fury_unlock) forces the exact same zone-2 gate
# at runtime so the sisters' logical and in-game availability stay in lockstep.
MINIBOSS_ZONE_OVERRIDE = {
    "Alecto": (NIGHTMARE, 2),
    "Tisiphone": (NIGHTMARE, 2),
}

enemy_location_base = hades2_base_location_id + 30000

# Each enemy check's id, as an offset from enemy_location_base. FROZEN: an id is part of every
# generated seed's datapackage, so an existing entry must never change and a retired offset must
# never be reused. These were originally assigned by position in ENEMY_LAYERS, which meant moving
# or inserting a name silently renumbered every check after it; the values below are exactly what
# that positional scheme produced, so no shipped id changed when this table replaced it.
# A new enemy gets the next unused offset (currently 137). ENEMY_LAYERS decides placement only.
ENEMY_LOCATION_OFFSETS = {
    # Underworld
    "Casket": 0, "Lanthorn": 1, "Sister of the Dead": 2, "Spindle": 3, "Wailer": 4,
    "Wastrel": 5, "Whisper": 6, "Thorn-Weeper": 7, "Root-Stalker": 8, "Shadow-Spiller": 9,
    "Headmistress Hecate": 10, "Master-Slicer": 11,
    "Hippo": 12, "Lurker": 13, "Pinhead": 14, "Sea-Serpent": 15, "Shellback": 16,
    "Sop-Spindle": 17, "Wet-Whisper": 18, "Wretched Pest": 19, "Deep Serpent": 20,
    "Hellifish": 21, "King Vermin": 22, "Scylla": 23, "Roxy": 24, "Jetty": 25,
    "Wretched Witch": 26, "Bloodless": 27, "Bone-Raker": 28, "Wave-Maker": 29,
    "Inferno-Bomber": 30, "Slam-Dancer": 31, "Burn-Flinger": 32,
    "Bawlder": 33, "Blight-Shade": 34, "Bloat-Shade": 35, "Blood-Shade": 36, "Canine": 37,
    "Holeheart": 38, "Lamia": 39, "Lycaon": 40, "Mourner": 41, "Smacker": 42,
    "Sorrow-Spiller": 43, "Phantom": 44, "Queen Lamia": 45, "Brush-Stalker": 46,
    "Infernal Beast": 47, "Dread-Wailer": 48,
    "Crawler": 49, "Goldwraith": 50, "Numbskull": 51, "Sandskull": 52, "Satyr Hoplite": 53,
    "Satyr Supplicant": 54, "Satyr Vierophant": 55, "Tempus": 56, "Wretched Thug": 57,
    "Goldwrath": 58, "The Verminancer": 59, "Wringer": 60, "Chronos": 61,
    # Surface
    "Bronzebeak": 62, "Cutthroat": 63, "Eidolon": 64, "Lubber": 65, "Shambler": 66,
    "Tombstone": 67, "Satyr Champion": 68, "Erymanthian Boar": 69, "The Cyclops Polyphemus": 70,
    "Anchor": 71, "Blasket": 72, "Boozer": 73, "Droplet": 74, "Harpy Talon": 75,
    "Sea-Shambler": 76, "Seesword": 77, "Stickler": 78, "Charybdis": 79, "The Yargonaut": 80,
    "Eris": 81,
    "Auto-Forcer": 82, "Auto-Seeker": 83, "Auto-Watcher": 84, "Harpy Raptor": 85,
    "Satyr Goldpike": 86, "Satyr Raider": 87, "Satyr Sapper": 88, "Sky-Dracon": 89,
    "Snow-Shambler": 90, "Mega-Dracon": 91, "Talos": 92, "Prometheus": 93,
    "Eyesore": 94, "Headstone": 95, "Horror": 96, "Land-Dracon": 97, "Polyp": 98, "Stalker": 99,
    "Eye of Typhon": 100, "Spawn of Typhon": 101, "Tail of Typhon": 102, "Twins of Typhon": 103,
    "Typhon": 104,
    # Nightmare
    "Skullomat": 105, "Wretched Lout": 106, "Brimstone": 107, "Dire Inferno-Bomber": 108,
    "Doomstone": 109, "Wretched Sneak": 110, "Megaera": 111, "Alecto": 112, "Tisiphone": 113,
    "Spreader": 114, "Voidstone": 115, "Skull-Crusher": 116, "Gorgon": 117, "Dracon": 118,
    "Megagorgon": 119, "Dire Spreader": 120, "Bone Hydra": 121,
    "Splitter": 122, "Nemean Chariot": 123, "Flame Wheel": 124, "Brightsword": 125,
    "Longspear": 126, "Strongbow": 127, "Greatshield": 128, "Soul Catcher": 129,
    "Theseus": 130, "Asterius": 131,
    "Gigantic Vermin": 132, "Bother": 133, "Snakestone": 134, "Satyr Cultist": 135, "Hades": 136,
}


def _check_enemy_offsets() -> None:
    """Fail at import, not at generation, when the table and ENEMY_LAYERS disagree."""
    listed = [name for route in ROUTE_NAMES for layer in ENEMY_LAYERS[route] for name in layer]
    missing = [name for name in listed if name not in ENEMY_LOCATION_OFFSETS]
    if missing:
        raise ValueError(f"ENEMY_LOCATION_OFFSETS has no id for {missing}; give each the next "
                         f"unused offset ({max(ENEMY_LOCATION_OFFSETS.values()) + 1} upward)")
    if len(set(ENEMY_LOCATION_OFFSETS.values())) != len(ENEMY_LOCATION_OFFSETS):
        raise ValueError("ENEMY_LOCATION_OFFSETS reuses an offset")
    if len(set(listed)) != len(listed):
        raise ValueError("an enemy name appears in ENEMY_LAYERS more than once")


_check_enemy_offsets()

location_enemies = {}          # name -> id (every enemy, both routes)
ENEMY_ROUTE = {}               # name -> route (existence gate: only in the table when active)
ENEMY_BY_ZONE = {}             # (route, zone) -> [enemy names] (normal single-zone placement)
SHARED_ENEMY_LOCATIONS = []    # names placed in Crossroads instead -- see SHARED_ENEMY_ZONES
for _route in ROUTE_NAMES:
    for _zi, _layer in enumerate(ENEMY_LAYERS[_route]):
        _zone = ROUTES[_route]["zones"][_zi]
        ENEMY_BY_ZONE.setdefault((_route, _zone), [])
        for _name in _layer:
            _loc = f"{_name} Defeated"
            location_enemies[_loc] = enemy_location_base + ENEMY_LOCATION_OFFSETS[_name]
            ENEMY_ROUTE[_loc] = _route
            if _loc in SHARED_ENEMY_ZONES:
                SHARED_ENEMY_LOCATIONS.append(_loc)
            else:
                ENEMY_BY_ZONE[(_route, _zone)].append(_loc)


def _is_miniboss_check(name: str) -> bool:
    return name.endswith(" Defeated") and name[:-len(" Defeated")] in MINIBOSS_ENEMY_NAMES


def filter_minibosses(location_names, include_minibosses: bool):
    """Drop MINIBOSS_ENEMY_NAMES-tagged checks from `location_names` unless
    include_minibosses is set. Shared by enemy_locations_for and Regions.py (which builds its
    per-zone/Crossroads lists straight from ENEMY_BY_ZONE/SHARED_ENEMY_LOCATIONS, not through
    enemy_locations_for)."""
    if include_minibosses:
        return list(location_names)
    return [n for n in location_names if not _is_miniboss_check(n)]


def enemysanity_has_locations(options) -> bool:
    """True for the two enemysanity modes that add 'X Defeated' check locations."""
    return options.enemysanity.value in (
        ENEMYSANITY_VANILLA_PLUS_LOCATIONS, ENEMYSANITY_SHUFFLED_PLUS_LOCATIONS,
    )


def enemysanity_is_shuffled(options) -> bool:
    """True for the two enemysanity modes using a fixed per-seed substitution permutation
    (as opposed to pure_random's per-spawn roll, which needs no precomputed map)."""
    return options.enemysanity.value in (
        ENEMYSANITY_SHUFFLED, ENEMYSANITY_SHUFFLED_PLUS_LOCATIONS,
    )


def enemy_locations_for(route: str, include_minibosses: bool = True) -> dict:
    """Every enemy check owned by `route`, plus -- when `route` is Nightmare -- the 12
    shared-name checks (SHARED_ENEMY_ZONES) and King Vermin (KING_VERMIN_LOCATION). July 18 (user ruling): the shared H1-callback
    names only exist in the pool when the NIGHTMARE route is in the seed. Their Underworld-
    side spawns (H2's own Oceanus/Asphodel-anomaly/Tartarus callbacks) are too rare/
    inconsistent to be the thing that puts them in the pool -- but when Nightmare IS in
    the seed, an Underworld-side kill still satisfies the check (the mod's send gate is
    seed-level, not current-route -- see LocationManager's ROUTE_GATED_CHECKS). The 12
    are skipped from ENEMY_ROUTE's own Underworld emission via their SHARED_ENEMY_ZONES
    membership. include_minibosses=False drops MINIBOSS_ENEMY_NAMES-tagged checks entirely."""
    table = {name: location_enemies[name]
             for name, r in ENEMY_ROUTE.items()
             if r == route and name not in SHARED_ENEMY_ZONES}
    if route == NIGHTMARE:
        for name in SHARED_ENEMY_ZONES:
            table[name] = location_enemies[name]
        table[KING_VERMIN_LOCATION] = location_enemies[KING_VERMIN_LOCATION]
    if not include_minibosses:
        table = {name: loc_id for name, loc_id in table.items() if not _is_miniboss_check(name)}
    return table


# Mirrors EnemySanity.SCRIPTED_ONLY_CHECK_NAMES in the Lua mod exactly (hand-duplicated, same
# convention as MINIBOSS_ENEMY_NAMES). These units only ever spawn through a dedicated scripted
# encounter, so the mod refuses to substitute them in either direction. Python must know the same
# set: the permutation it generates is what LOGIC is derived from, and a name the mod silently
# refuses to route through would leave the rules describing spawns that never happen.
SCRIPTED_ONLY_CHECK_NAMES = {
    "Charybdis", "Talos", "Scylla", "Roxy", "Jetty", "Chronos", "Eris", "Prometheus", "Typhon",
    "Megaera", "Alecto", "Tisiphone", "Theseus", "Asterius", "Hades", "Bone Hydra",
    "Headmistress Hecate", "The Cyclops Polyphemus", "Infernal Beast",
    # 2026-08-16: SatyrCultist is in no EnemySet whatsoever -- referenced only by
    # EncounterData_Boss.lua's Chronos fight and WeaponData_Chronos.lua's summons, and its art
    # lives in the Chronos package rather than a Biome<X> one. Chronos-fight-only.
    "Satyr Supplicant",
    # 2026-09-23: units that never come through a spawn the mod can rewrite. Substitution only
    # touches encounter SpawnWaves entries it can map to a check, so a name whose spawns all
    # come from somewhere else is a dead end in the permutation: whatever it maps TO is never
    # produced (an unobtainable check the rules still put in logic), and whatever maps to it
    # spawns a unit that doesn't belong in a normal room.
    #   Eye/Tail of Typhon: 25,000-HP BaseBossEnemy arena units, pre-placed by their own
    #     Summit miniboss encounters (BossTyphonEye01/BossTyphonTail01).
    #   Lanthorn: summoned only by Master-Slicer's attack (WeaponData_Zombie.lua); it's
    #     commented out of EnemySets.BiomeF.
    #   Canine: summoned only by Lycaon (WeaponData_Lycan.lua).
    #   Pinhead / Polyp: their pools spawn them as FishSwarmerSquad / SimpleSquad unit groups,
    #     which have no check mapping, so those spawns are never rewritten.
    #   Sister of the Dead: only Hecate's boss-fight adds (HecateSpawns01/02).
    "Eye of Typhon", "Tail of Typhon", "Lanthorn", "Canine", "Pinhead", "Polyp",
    "Sister of the Dead",
}

# Checks only obtainable inside another enemy's fight: summoned by it, spawned as its arena's
# adds, or part of its boss encounter. Logic places each one wherever its host ends up (after
# the enemy and miniboss-room shuffles) and gives it the host's gate -- see
# enemy_zone_placement and Rules._is_miniboss_location. All of these are also held out of the
# enemy shuffle above (or are minibosses), so their host is the only place they appear.
ENEMY_COMPANIONS = {
    "Lanthorn": "Master-Slicer",            # F_MiniBoss03: Master-Slicer summons them
    "Headstone": "Twins of Typhon",         # Q_MiniBoss05: MiniBossStalker's adds
    "Canine": "Lycaon",                     # Lycaon's summon; follows Lycaon through the shuffle
    "Sister of the Dead": "Headmistress Hecate",
    "Satyr Supplicant": "Chronos",
}


def _repair_shuffle_map(pairs: dict) -> dict:
    """Drop every entry the mod won't actually honour, walking the cycle past it so the
    permutation stays a bijection over the names that DO substitute.

    Mirrors EnemySanity.induced_map in the Lua mod. Refusing to substitute FROM a name orphans
    whatever it mapped TO, so the fix is to take the permutation induced on the surviving names:
    walk each target forward until it lands on one we'll really use. Two things are skipped --
    SCRIPTED_ONLY_CHECK_NAMES, and any target whose miniboss class differs from the source's
    (Python already deranges those pools separately, so that half is a no-op here and exists only
    to keep the two implementations provably identical).

    Doing this Python-side is what makes logic trustworthy: `set_rules` derives each enemy check's
    zone from its preimage in THIS dict, so it has to be the same dict the mod ends up using --
    not the raw derangement it was built from.
    """
    out = {}
    for src, dst in pairs.items():
        if src in SCRIPTED_ONLY_CHECK_NAMES:
            continue
        src_is_miniboss = src in MINIBOSS_ENEMY_NAMES
        target, guard = dst, 0
        while target is not None and guard < 512 and (
                target in SCRIPTED_ONLY_CHECK_NAMES
                or (target in MINIBOSS_ENEMY_NAMES) != src_is_miniboss):
            target = pairs.get(target)
            guard += 1
        if (target is not None and target != src
                and target not in SCRIPTED_ONLY_CHECK_NAMES
                and (target in MINIBOSS_ENEMY_NAMES) == src_is_miniboss):
            out[src] = target
    return out


def serialize_shuffle_map(pairs: dict) -> str:
    """Wire format for the settings bridge: "NameA:NameB,NameC:NameD,..." (bare enemy names)."""
    return ",".join(f"{k}:{v}" for k, v in sorted(pairs.items()))


def parse_shuffle_map(raw: str) -> dict:
    """Inverse of serialize_shuffle_map. Used to restore the REAL seed's permutation under
    Universal Tracker, which regenerates the world in an isolated multiworld -- recomputing from
    self.random there would produce a different permutation, and since logic now follows the map,
    UT would track against enemy placements the real seed never had."""
    pairs = {}
    for entry in (raw or "").split(","):
        src, sep, dst = entry.partition(":")
        if sep and src and dst:
            pairs[src] = dst
    return pairs


# Every miniboss room in the game, mapped to the route/zone it lives in and the AP check its
# headline miniboss satisfies. Mirrored in MinibossRooms.lua (keep both in sync by hand, same
# convention as MINIBOSS_ENEMY_NAMES).
#
# Derivation rule, because three earlier attempts got this wrong: a room's headline miniboss is
# the unit named by its encounter's WipeEnemiesOnKill / WipeEnemiesOnKillAllTypes -- the one whose
# death ends the fight -- falling back to LegalTypes for the ActivatePrePlaced arenas (Charybdis,
# Talos). Do NOT read it off the encounter's `Name =` spawns: "_Shadow" units are the shrine-
# upgrade reskins of the trash ADDS and sort first, which is how Q_MiniBoss02 kept resolving to
# "Horror" instead of "Spawn of Typhon".
#
# Every check here was verified miniboss-EXCLUSIVE (none of their unit ids appears in a generic
# Biome* spawn pool), so relabelling them here can never collide with the enemy shuffle, which
# no longer touches minibosses at all. Note F_MiniBoss02's check is "Shadow-Spiller", a name that
# LOOKS regular -- its miniboss FogEmitter_Elite strips to FogEmitter -- but plain FogEmitter is
# not in any biome pool either, so it too is miniboss-exclusive.
MINIBOSS_ROOMS = {
    "F_MiniBoss01": (UNDERWORLD, 1, "Root-Stalker"),
    "F_MiniBoss02": (UNDERWORLD, 1, "Shadow-Spiller"),
    "F_MiniBoss03": (UNDERWORLD, 1, "Master-Slicer"),
    "G_MiniBoss01": (UNDERWORLD, 2, "Deep Serpent"),
    "G_MiniBoss02": (UNDERWORLD, 2, "King Vermin"),
    "G_MiniBoss03": (UNDERWORLD, 2, "Hellifish"),
    "H_MiniBoss01": (UNDERWORLD, 3, "Phantom"),
    "H_MiniBoss02": (UNDERWORLD, 3, "Queen Lamia"),
    "I_MiniBoss01": (UNDERWORLD, 4, "The Verminancer"),
    "I_MiniBoss02": (UNDERWORLD, 4, "Goldwrath"),
    "N_MiniBoss01": (SURFACE, 1, "Satyr Champion"),
    "N_MiniBoss02": (SURFACE, 1, "Erymanthian Boar"),
    "O_MiniBoss01": (SURFACE, 2, "Charybdis"),
    "O_MiniBoss02": (SURFACE, 2, "The Yargonaut"),
    "P_MiniBoss01": (SURFACE, 3, "Talos"),
    "P_MiniBoss02": (SURFACE, 3, "Mega-Dracon"),
    "Q_MiniBoss02": (SURFACE, 4, "Spawn of Typhon"),
    "Q_MiniBoss03": (SURFACE, 4, "Tail of Typhon"),
    "Q_MiniBoss04": (SURFACE, 4, "Eye of Typhon"),
    "Q_MiniBoss05": (SURFACE, 4, "Twins of Typhon"),
}
# Not listed, on purpose:
#   Q_MiniBoss01 (BossTyphonArm01, the "Hand of Typhon" TyphonArm) and I_MiniBoss03 are both
#     `DebugOnly = true` in RoomData -- the game never offers them, and TyphonArm spawns nowhere
#     else (the TyphonArm_Incursion units elsewhere are scripted hazards, not a fight). A check or
#     room slot for either could never be satisfied.
#   Zagreus' Journey miniboss rooms. ZJ only loads its rooms' packages and runs its enemy setup
#     when the whole run is a ZJ run (CurrentRun.ModsNikkelMHadesBiomesIsModdedRun) and the room's
#     RoomSetName is one of its biomes (its Scripts/RoomLogic.lua), so one of its rooms swapped into
#     a Hades II run would load neither -- and swap_for stamps the host's RoomSetName anyway.


# The checks the miniboss-ROOM shuffle is responsible for placing. Held out of the enemy shuffle
# so exactly one map owns each check's zone -- the collision assert in combined_relabel caught
# "Shadow-Spiller" doing both, which is the whole reason this set is derived rather than assumed:
# it is F_MiniBoss02's miniboss (FogEmitter_Elite) but reads as an ordinary name, so
# MINIBOSS_ENEMY_NAMES never held it back. All are miniboss-exclusive (their units appear in no
# generic Biome* pool), so removing them from enemy substitution costs nothing real -- they were
# never obtainable from trash anyway.
MINIBOSS_ROOM_CHECK_NAMES = {check for (_route, _zone, check) in MINIBOSS_ROOMS.values()}


def compute_miniboss_room_map(options, rand, routes=None) -> dict:
    """Permute which miniboss ROOM occupies each miniboss room slot (2026-08-16 user ruling:
    minibosses stop shuffling as enemies -- their rooms shuffle instead, so the miniboss you fight
    is always in the room it belongs to, but you might meet Charybdis' room while running Erebus).

    "host: dest" means the run's `host` slot loads `dest`'s room instead. The mod keeps routing in
    the host region via ChooseNextRoomData's own ForceNextRoomSet, so the run's shape is unchanged.

    Pooled across the seed's ACTIVE routes only -- Zagreus' Journey rooms are excluded when the
    YAML excludes ZJ (user ruling), and a route that isn't generated contributes no rooms, so a
    check can never be gated behind a region this seed doesn't contain. Returns {} unless
    enemysanity actually places miniboss checks, since with no locations there is nothing for the
    permutation to be consistent with.
    """
    if not enemysanity_has_locations(options) or not options.include_minibosses:
        return {}
    active = set(routes) if routes is not None else set(ROUTE_NAMES)
    rooms = sorted(r for r, (route, _z, _c) in MINIBOSS_ROOMS.items() if route in active)
    n = len(rooms)
    if n < 2:
        return {}
    # Sattolo's algorithm -- a random cyclic permutation, so no room ever maps to itself and every
    # room hosts exactly one other. Same generator the enemy shuffle uses.
    shuffled = rooms[:]
    i = n - 1
    while i > 0:
        j = rand.randrange(i)
        shuffled[i], shuffled[j] = shuffled[j], shuffled[i]
        i -= 1
    return {rooms[k]: shuffled[k] for k in range(n)}


def miniboss_check_relabel(room_map: dict) -> dict:
    """{check of the room that USED to be here: check of the room that is here now}.

    Same shape as the enemy shuffle map, so enemy_zone_placement can apply both in one pass: the
    zone slot that used to yield the host room's miniboss now yields the destination room's.
    """
    out = {}
    for host, dest in room_map.items():
        host_check = MINIBOSS_ROOMS.get(host, (None, None, None))[2]
        dest_check = MINIBOSS_ROOMS.get(dest, (None, None, None))[2]
        if host_check and dest_check:
            out[host_check] = dest_check
    return out


def enemy_zone_placement(shuffle_map: dict, routes=None) -> dict:
    """ENEMY_BY_ZONE remapped so each zone lists the checks actually OBTAINABLE there.

    The map is directional -- "src: dst" means a spawn of `src` produces `dst` instead -- so after
    shuffling, enemy D is only killable where its preimage spawns, NOT where D natively lives.
    Applying the map to each zone's bucket expresses exactly that: the slot that used to hold
    "S Defeated" now holds "map[S] Defeated", i.e. zone(D) becomes zone(preimage(D)).

    Because the map is a bijection over the shuffled roster, the relabel itself keeps every
    location exactly once. Names outside the map (scripted-only, anything from a route not in this
    seed) keep their native placement, except ENEMY_COMPANIONS, which then move into whichever
    zone their host landed in.

    Shared names (SHARED_ENEMY_ZONES) live in Crossroads, outside every zone bucket. The ones in
    the map join the bucket of their SHARED_ENEMY_SLOT first, so they relabel like any other name;
    the ones that aren't (seeds generated before 9/26) stay in Crossroads.

    `routes` (the seed's active routes) moves King Vermin to Nightmare's Styx when Nightmare is in
    the seed and Underworld isn't -- see KING_VERMIN_LOCATION.
    """
    buckets = {key: list(names) for key, names in ENEMY_BY_ZONE.items()}
    for loc, slot in SHARED_ENEMY_SLOT.items():
        if loc[:-len(" Defeated")] in shuffle_map:
            buckets[slot].append(loc)
    out = {}
    for (route, zone), names in buckets.items():
        remapped = []
        for loc in names:
            bare = loc[:-len(" Defeated")] if loc.endswith(" Defeated") else loc
            target = shuffle_map.get(bare)
            remapped.append(f"{target} Defeated" if target else loc)
        out[(route, zone)] = remapped
    # Companions go wherever their host is: e.g. Lanthorn only ever appears in Master-Slicer's
    # fight, so when the miniboss-room shuffle sends F_MiniBoss03 to the Summit, Lanthorn is
    # obtainable there and nowhere in Erebus.
    zone_of = {loc: key for key, names in out.items() for loc in names}
    for companion, host in ENEMY_COMPANIONS.items():
        loc, host_loc = f"{companion} Defeated", f"{host} Defeated"
        src, dst = zone_of.get(loc), zone_of.get(host_loc)
        if src is not None and dst is not None and src != dst:
            out[src] = [name for name in out[src] if name != loc]
            out[dst] = out[dst] + [loc]
            zone_of[loc] = dst
    if routes is not None and NIGHTMARE in routes and UNDERWORLD not in routes:
        styx = (NIGHTMARE, ROUTES[NIGHTMARE]["zones"][NIGHTMARE_KING_VERMIN_ZONE_INDEX])
        out[styx] = out[styx] + [KING_VERMIN_LOCATION]
    return out


def combined_relabel(enemy_map: dict, room_map: dict) -> dict:
    """The enemy-substitution map and the miniboss-room map merged into one relabelling.

    They are disjoint by construction -- the enemy shuffle no longer touches miniboss names, and
    all miniboss-room checks were verified miniboss-exclusive -- so a single dict can carry
    both and enemy_zone_placement stays a one-pass relabel. Asserting the disjointness rather
    than assuming it: an overlap would mean one check had two different zones, silently picking
    whichever won the merge.
    """
    merged = dict(enemy_map)
    for src, dst in miniboss_check_relabel(room_map).items():
        if src in merged:
            raise ValueError(
                f"miniboss room relabel collides with the enemy shuffle on {src!r} -- "
                "a check cannot be placed by both maps")
        merged[src] = dst
    return merged


def compute_enemysanity_shuffle_map(options, rand, routes=None) -> dict:
    """Build the shuffled-mode ('shuffled'/'shuffled_plus_locations') enemy substitution map,
    deterministic from `rand` (the world's seeded Random). Returns {} for every other mode --
    pure_random needs no precomputed map, since the mod rolls a fresh in-scope random pick
    per spawn itself (and adds no locations, so it has no logic to get wrong).

    `routes` is the seed's ACTIVE routes; names from a route that isn't generated are excluded
    entirely. They have no "Defeated" locations, so letting them into the permutation would put
    enemies with no checks into the rotation and -- now that logic follows this map -- could gate
    a real check behind a route the seed doesn't contain. Passing None means "all routes", which
    only the standalone tooling does.

    Scope within that: per-route (each route shuffles only within itself) unless
    include_zagreus_journey is on, in which case the active routes' rosters pool into one global
    scope (user ruling). Minibosses (MINIBOSS_ENEMY_NAMES) only ever substitute with other
    minibosses in the same scope, and are left out entirely (never substituted) when
    include_minibosses is off -- regular/trash names never mix with the miniboss pool.

    Two groups are held out of the permutation so they keep spawning natively:
      - SCRIPTED_ONLY_CHECK_NAMES: the mod refuses to substitute them in either direction.
      - MINIBOSS_ROOM_CHECK_NAMES: placed by the miniboss-ROOM shuffle instead, so that exactly
        one map owns each check's zone (see combined_relabel's collision guard).
    The 12 SHARED_ENEMY_ZONES names were a third group until 9/26; they now shuffle through their
    Nightmare slot (SHARED_ENEMY_SLOT). They only exist when Nightmare is in the seed, and
    enemy_locations_for only adds them to Nightmare's roster, so they only enter the map then.
    Excluding both UP FRONT (rather than generating them and letting _repair_shuffle_map walk
    past them, which is what used to happen for the scripted-only set) means the derangement is
    already over exactly the names that substitute -- so it is a clean bijection with no coverage
    lost to the walk, and the repair pass downstream is a no-op safety net.

    Returns a dict; serialize_shuffle_map puts it on the wire for the settings bridge.
    """
    if not enemysanity_is_shuffled(options):
        return {}
    include_minibosses = bool(options.include_minibosses)
    global_scope = bool(options.include_zagreus_journey)
    active = list(routes) if routes is not None else list(ROUTE_NAMES)

    def bare(name: str) -> str:
        return name[:-len(" Defeated")] if name.endswith(" Defeated") else name

    def roster_for(route) -> list:
        # include_minibosses=True here to get the full roster; the miniboss/regular split
        # (and the include_minibosses gate on whether minibosses shuffle at all) happens below.
        return [bare(n) for n in enemy_locations_for(route, include_minibosses=True)
                if bare(n) not in SCRIPTED_ONLY_CHECK_NAMES
                and bare(n) not in MINIBOSS_ROOM_CHECK_NAMES]

    def derange(names: list) -> dict:
        # Sattolo's algorithm: a random cyclic permutation, guaranteeing no element maps to
        # itself (for len(names) >= 2 -- a single-name pool trivially maps to itself).
        items = list(names)
        n = len(items)
        if n == 0:
            return {}
        if n == 1:
            return {items[0]: items[0]}
        shuffled = items[:]
        i = n - 1
        while i > 0:
            j = rand.randrange(i)
            shuffled[i], shuffled[j] = shuffled[j], shuffled[i]
            i -= 1
        return {items[k]: shuffled[k] for k in range(n)}

    def split_pools(names) -> tuple:
        # 2026-08-16 (user ruling): minibosses no longer shuffle as ENEMIES at all -- their ROOMS
        # get shuffled instead. Classifying by name can't express "this spawn is the room's
        # miniboss", and both directions broke live: Thorn-Weeper is miniboss-classified but
        # spawns as ordinary trash, so normal rooms drew real minibosses out of the miniboss pool
        # (four minibosses in a room built for one), while the actual miniboss unit
        # FogEmitter_Elite strips to the REGULAR check "Shadow-Spiller" and got replaced by a
        # regular enemy. The mod additionally skips any "MiniBoss*" encounter outright.
        # include_minibosses still governs whether miniboss CHECKS exist, just not shuffling.
        regular = sorted(n for n in names if n not in MINIBOSS_ENEMY_NAMES)
        return regular, []

    pairs = {}
    if global_scope:
        all_names = sorted({n for route in active for n in roster_for(route)})
        regular, minibosses = split_pools(all_names)
        pairs.update(derange(regular))
        pairs.update(derange(minibosses))
    else:
        for route in active:
            regular, minibosses = split_pools(roster_for(route))
            pairs.update(derange(regular))
            pairs.update(derange(minibosses))

    # No-op on a correctly-built map (nothing scripted-only or class-crossing is in `pairs` any
    # more), kept so Python and the mod provably agree on the final permutation even if one side
    # gains a hold-out the other doesn't know about yet.
    return _repair_shuffle_map(pairs)


# --- NPC / "Met" locations (npc_locations) ------------------------------------
# Intro story beats and Crossroads meets are reachable from the start. Each route boss
# "Met" check lives in the boss's zone region, so it unlocks once that layer is reachable
# (mirroring the wishlist: Scylla at layer 2, Cerberus at layer 3, etc.). EXCEPTION: "Met
# Chronos" is deliberately pulled forward to zone 0 with an added access_rule (see Rules.py
# set_rules) so it opens at the same moment as "Beat Hecate", instead of waiting on Tartarus.
NPC_INTRO = ["SHUSH Homer", "Find Hecate 1", "Find Hecate 2", "Find Hecate 3"]

# Bosses meet checks, keyed to the zone that gates them.
NPC_BOSS_MEET = [
    ("Met Hecate", UNDERWORLD, 0),
    ("Met Scylla", UNDERWORLD, 1),
    ("Met Roxy", UNDERWORLD, 1),
    ("Met Jetty", UNDERWORLD, 1),
    ("Met Cerberus", UNDERWORLD, 2),
    # Zone left at 3 would be Tartarus (Chronos's own zone, gated behind all 3 prior boss
    # victories); moved to zone 0 (Erebus, Hecate's zone) instead, with an explicit access_rule
    # in Rules.py pinning it to the exact "Beat Hecate" predicate -- see set_rules -- so "Met
    # Chronos" opens up at the same moment defeating Hecate becomes possible, not after the
    # whole route is cleared.
    ("Met Chronos", UNDERWORLD, 0),
    ("Met Polyphemus", SURFACE, 0),
    ("Met Eris", SURFACE, 1),
    ("Met Prometheus", SURFACE, 2),
    ("Met Typhon", SURFACE, 3),
    # Nightmare. Theseus and Asterius each get their own (fought together, but tracked
    # separately per NPC_ROUTE_LOCK precedent for distinctly-named characters). The final
    # boss does NOT get a "Met" location of his own -- he's the same NPC as the Underworld's
    # "Hades" (Jeweled Pom keepsake-giver), so defeating him here instead satisfies the
    # shared "Met Hades" location (a randomized-helper location as of July 18 -- his
    # I_Story01 shuffles across routes, see Routes.NPC_RANDOMIZED_HELPERS).
    ("Met Bone Hydra", NIGHTMARE, 1),
    ("Met Theseus", NIGHTMARE, 2),
    ("Met Asterius", NIGHTMARE, 2),
    # Appended (not inserted in zone order) to keep existing location ids stable for seeds
    # already generated against this table -- see location_npc_boss below.
    ("Met Megaera", NIGHTMARE, 0),
]
_NPC_BOSS_NAMES = {"Hecate", "Scylla", "Cerberus", "Chronos",
                   "Polyphemus", "Eris", "Prometheus", "Typhon",
                   "Megaera", "Bone Hydra", "Theseus", "Asterius"}

# Route bosses you meet regardless of which routes the seed generates, so their "Met" check
# must always exist and be reachable from the start instead of being gated behind their route's
# zone. Hecate mentors you at the Crossroads from the very first run, so a Surface-only seed
# (Underworld excluded) still meets her -- previously that fired a "Met Hecate" check for a
# location that was never generated ("Unknown location checked by game"). NOT included: Eris --
# even though she also ambushes you mid-run in the Underworld as the "Curse of Eris" NPC
# encounter (SpawnErisForCurse -> NPC_Eris_01), we deliberately do NOT want "Met Eris" to exist
# on Underworld-only seeds (better safe than sorry re: reachability if that encounter turns out
# to be rare/conditional). She stays Surface-gated: when Surface IS in the seed, the mod fires
# "Met Eris" from EITHER the Underworld curse encounter or the Surface boss fight (whichever
# happens first) -- see LocationManager.NPC_UNIT_OVERRIDE["NPC_Eris_01"] in the mod.
ALWAYS_MET_BOSSES = {"Hecate"}
ALWAYS_MET_BOSS_LOCATIONS = {"Met " + boss for boss in ALWAYS_MET_BOSSES}

# NPCs who can't be met in normal Archipelago play, so their "Met <NPC>" check would be a
# dead location. Zagreus is only reachable through the scripted Elysium "memory" rescue, which
# the mod doesn't force open -- and his Calling Card keepsake is likewise item-only (see
# KEEPSAKE_NO_LOCATION), so he has no obtainable check at all. Megaera doesn't need an entry
# here since she's excluded via _NPC_BOSS_NAMES instead (she has her own "Met Megaera" tuple
# in NPC_BOSS_MEET above). Achilles IS meetable in normal play (native Elysium progression)
# but is excluded here anyway (July 31, user ruling): "Met Achilles" was removed as a
# location entirely, same as his keepsake (see KEEPSAKE_NPC.values() feeding NPC_CAST below
# -- without this exclusion he'd fall right back into NPC_CAST since he's no longer in
# NPC_EXTRA_CAST either).
NPC_NO_MEET = {"Zagreus", "Achilles"}

# The Crossroads cast: every keepsake-giving character who isn't a route boss (or otherwise
# unmeetable), plus a few meet-able NPCs who don't give keepsakes. Hypnos (Test Run 5 #5) wasn't
# in the keepsake cast, so "Met Hypnos" never existed; he's added here (met once he's awake).
# Thanatos/Orpheus (Nightmare cast, re-added July 16 -- see Routes.NPC_ROUTE_LOCK) are
# deliberately appended at the END, after Hypnos, instead of taking their natural
# KEEPSAKE_NPC positions: location_npc_meet numbers ids by NPC_CAST order, and slotting them
# mid-list would shift "Met Hypnos"'s established id. Achilles was in this list too (July 16)
# but "Met Achilles"/"Achilles Keepsake" were removed as locations July 31 (user ruling);
# his keepsake item stays in the pool item-only (Items.KEEPSAKE_NO_LOCATION).
NPC_EXTRA_CAST = ["Hypnos", "Thanatos", "Orpheus"]
NPC_CAST = [npc for npc in dict.fromkeys(KEEPSAKE_NPC.values())
            if npc not in _NPC_BOSS_NAMES and npc not in NPC_NO_MEET
            and npc not in NPC_EXTRA_CAST]
NPC_CAST += [npc for npc in NPC_EXTRA_CAST if npc not in NPC_CAST]

npc_location_base = hades2_base_location_id + 31000
location_npc_intro = {name: npc_location_base + i for i, name in enumerate(NPC_INTRO)}
location_npc_meet = {f"Met {npc}": npc_location_base + 100 + i
                     for i, npc in enumerate(NPC_CAST)}
location_npc_boss = {name: npc_location_base + 200 + i
                     for i, (name, _r, _z) in enumerate(NPC_BOSS_MEET)}
# Crossroads-resident NPC checks (reachable from the start): intro beats, the Crossroads cast,
# and any always-met boss (Hecate) whose "Met" lives in the hub rather than behind a route.
location_npc_crossroads = {**location_npc_intro, **location_npc_meet,
                           **{name: location_npc_boss[name] for name in ALWAYS_MET_BOSS_LOCATIONS}}

NPC_BOSS_BY_ZONE = {}          # (route, zone) -> [boss "Met" names]
for _name, _route, _zi in NPC_BOSS_MEET:
    if _name in ALWAYS_MET_BOSS_LOCATIONS:
        continue               # always met at the Crossroads; not gated behind its route's zone
    _zone = ROUTES[_route]["zones"][_zi]
    NPC_BOSS_BY_ZONE.setdefault((_route, _zone), []).append(_name)


def npc_boss_locations_for(route: str) -> dict:
    return {name: location_npc_boss[name]
            for name, r, _zi in NPC_BOSS_MEET if r == route}


# Boss "Met" checks through Dream Dive (9/30). A Dream region is a whole vanilla biome played
# through to its own boss (see DREAM_BOSS_NAMES), so a dive meets the Underworld's and the
# Surface's bosses whether or not those routes are in the seed. When one isn't, its boss "Met"
# checks are generated for Dream instead (fill_dream_checks) and live in Dream's FINAL region:
# which biome lands in which region slot is rerolled every attempt, so only a dive that can reach
# its last region is sure to pass the boss in question -- the same "final zone" bar
# Routes.NPC_RANDOMIZED_ZONE_INDEX sets for the other randomized meets. (When the route IS in the
# seed its checks stay in their own zones; a dive can still send them, just out of logic.)
# Nightmare's bosses need no entry: its biomes only join the dive's pool when the Nightmare route
# is itself in the seed (fill_dream_checks' zj_active), where their checks already exist.
# Mirrored by the mod's LocationManager.DREAM_MET_ROUTES.
DREAM_MET_ROUTES = (UNDERWORLD, SURFACE)


def dream_boss_met_locations_for(options) -> dict:
    """Boss "Met" checks only a Dream Dive can send this seed: those of a DREAM_MET_ROUTES route
    that isn't active (an active route generates its own). Empty without Dream."""
    routes = active_routes(options)
    if DREAM not in routes:
        return {}
    return {name: location_npc_boss[name] for name, route, _zi in NPC_BOSS_MEET
            if route in DREAM_MET_ROUTES and route not in routes
            and name not in ALWAYS_MET_BOSS_LOCATIONS}


def _route_locked_out(npc: str, routes: list, options=None) -> bool:
    """True if npc's location requires a route that isn't active this seed (Known Bugs/
    "Logic is all out of whack"): their Keepsake/Met location shouldn't exist at all --
    rather than exist but just lose its area gate -- when that route is excluded.
    Randomized helper NPCs (Routes.NPC_RANDOMIZED_HELPERS) are never locked out: the
    story-room/combat-assist randomizers can produce them on whatever route IS active
    (July 18 -- this is why "Met Patroclus" must exist on a Nightmare-less seed).
    EXCEPTION (CombatHelperSanity): a combat-assist NPC (Routes.COMBAT_HELPER_NPCS) under
    "unlocked"/"items" (native-only, modes 0/1) can ONLY ever spawn in its own native route
    -- the whole point of native-only mode is that the any-location randomizer is turned
    off for them (see ItemManager.apply_combat_helper_random, mod side). If that native
    route isn't in the seed at all, there's nowhere they can ever spawn, so their location
    must be dropped instead of left permanently unreachable -- same reasoning NPC_ROUTE_LOCK
    already uses for Eris/Orpheus, just conditioned on this option's mode.
    SUB-EXCEPTION (Thanatos/IncludeZagreusJourney, July 22): Routes.combat_helper_native_fallback
    carves Thanatos back out of that native-route lock when IncludeZagreusJourney is still on --
    ItemManager.apply_combat_helper_random forces his foreign-zone (Underworld/Surface) flags on
    regardless of mode in that situation (mod side), since he'd otherwise have nowhere to ever
    spawn without Nightmare active. He falls through to the NPC_RANDOMIZED_HELPERS branch below
    instead, same as any other randomized helper.
    EXCEPTION (IncludeZagreusJourney): Routes.ZJ_RANDOMIZED_ONLY (Sisyphus/Eurydice/Patroclus/
    Thanatos) are randomized helpers that nonetheless only exist because Zagreus' Journey is
    installed -- when that option is off they're locked out unconditionally, even though
    they'd otherwise be exempt as randomized helpers. Orpheus/Megaera need no such
    exception: they're NPC_ROUTE_LOCK'd (or zone-keyed) to Nightmare already, so they drop for
    free once IncludeZagreusJourney forces Nightmare out of `routes` (__init__.py).
    SUB-EXCEPTION (Sisyphus/Eurydice/Patroclus, HelperRoomSanity native-only, July 22): under
    "unlocked"/"items" (modes 0/1), zerp-NPCRoomRandomizer never swaps a story door's identity
    at all (ItemManager.helper_room_random_allowed is false, reload.lua's SelectRandomStoryRoom
    returns the door's own native pick unchanged) -- EXCEPT reload.lua special-cases exactly this
    scenario (IncludeZagreusJourney on, Nightmare not in the seed) to still let zerp's randomizer
    swap one of these 3 in, since their own native A/X/Y_Story01 doors never occur otherwise. So
    they stay exempt (not locked out) here too, same as the mode 2/3 case."""
    if npc in COMBAT_HELPER_NPCS and options is not None \
            and getattr(options, "combat_helper_sanity", None) is not None \
            and options.combat_helper_sanity.value in (0, 1) \
            and not combat_helper_native_fallback(npc, options, routes):
        native_route = COMBAT_HELPER_NATIVE_ROUTE.get(npc)
        return native_route is not None and native_route not in routes
    if npc in ZJ_RANDOMIZED_ONLY and options is not None \
            and not getattr(options, "include_zagreus_journey", True):
        return True
    if npc in NPC_RANDOMIZED_HELPERS:
        return False
    required = NPC_ROUTE_LOCK.get(npc)
    return required is not None and required not in routes


def keepsake_locations_for(options) -> dict:
    """Active-seed "<NPC> Keepsake" locations: drops route-locked NPCs whose route isn't
    included this seed, instead of leaving an ungated dead check behind. Nothing extra is
    dropped with Dream the only route: vanilla won't take gifts during a Dream run, but the mod
    keeps every giver giftable there (reload.lua's SilenceForDreamRun wrap)."""
    routes = active_routes(options)
    return {name: loc_id for name, loc_id in location_keepsakes.items()
            if not _route_locked_out(name[:-len(" Keepsake")], routes, options)}


def npc_meet_locations_for(options) -> dict:
    """Active-seed "Met <NPC>" locations (Crossroads cast): same route-lock filter as
    keepsake_locations_for, so e.g. "Met Icarus" doesn't exist in an Underworld-only seed."""
    routes = active_routes(options)
    return {name: loc_id for name, loc_id in location_npc_meet.items()
            if not _route_locked_out(name[len("Met "):], routes, options)}


def npc_intro_locations_for(options) -> dict:
    """SHUSH Homer / Find Hecate 1-3 REMOVED from every seed (2026-08-04, user request): all
    four were part of Hecate's hide-and-seek flashback sequence (Flashback01), which the mod
    now permanently disables (ItemManager.apply_flashback_disable) -- these checks could never
    fire in-game again. Always returns {} rather than deleting NPC_INTRO/location_npc_intro
    outright, so their reserved id block (npc_location_base + 0..3) stays stable and doesn't
    reflow anything defined after it, matching this file's existing "keep ids stable" precedent
    (see the NPC_BOSS_MEET append-only comment above). Rules.py's matching access-rule loop
    already no-ops via `except KeyError: continue` when a location isn't in the table, so no
    change needed there."""
    return {}


# Zagreus "Met" / "Defeated" (July 17): two REAL checks living at the always-open Crossroads,
# distinct from the "Beat Zagreus" goal event -- gated in Rules.py by how beatable the OTHER
# bosses are (Met = any route's 1st boss beatable; Defeated = stricter than the hardest boss
# tier). Existence mirrors their naming siblings: Met follows npc_locations, Defeated follows
# enemysanity_has_locations -- AND (July 21) both also require goal_requires_zagreus, since
# neither is actually reachable in-game unless it's on (see setup_location_table_with_settings).
ZAGREUS_MET_LOCATION = "Met Zagreus"
ZAGREUS_DEFEATED_LOCATION = "Zagreus Defeated"
zagreus_extra_location_base = hades2_base_location_id + 6140


# -----------------------------------------------------------------------------


def setup_location_table_with_settings(options, multiplier: int = 1, dream_met: bool = True) -> dict:
    """Build the flat active location table (name -> id) for this seed. multiplier scales
    the room-based check pools (see MAX_LOCATION_MULTIPLIER). dream_met: whether Dream gets
    boss "Met" checks (fill_dream_checks)."""
    clear_tables()
    for route in active_routes(options):
        fill_route_checks(route, options, multiplier, dream_met)

    total = {}
    for route in active_routes(options):
        for zone, locs in zone_tables[route].items():
            total.update(locs)

    # Zagreus (secret superboss): a standalone event, not tied to either route's zone-boss
    # list, so it isn't in zone_tables. Always present, like the Chronos/Typhon boss events
    # (harmless if the goal doesn't need it -- see Rules.py's access rule).
    total[boss_event("Zagreus")] = None

    # Dream's single "Beat Dream" event (no fixed boss identity -- see Routes.DREAM's
    # definition comment). Unlike Zagreus this is NOT always present: it only makes sense
    # when Dream is actually part of this seed.
    if DREAM in active_routes(options):
        total[boss_event("Dream")] = None

    # combine_pools: the shared pools' checks live outside the per-route zone tables.
    if combine_active(options):
        if options.location_system.value in (ROOM_BASED, PER_WEAPON_ROOM_BASED, PER_ASPECT_ROOM_BASED):
            total.update(combined_room_table(options, multiplier))
        else:
            total.update(combined_score_table(options))

    # Keepsake checks exist in randomized (1) and progressive (2), not normal (0).
    if options.keepsakesanity.value != 0:
        total.update(keepsake_locations_for(options))

    # Enemy first-defeat checks, per active route (vanilla_plus_locations / shuffled_plus_locations).
    if enemysanity_has_locations(options):
        for route in active_routes(options):
            total.update(enemy_locations_for(route, bool(options.include_minibosses)))

    # NPC "Met" checks: intro + Crossroads cast (route-locked NPCs filtered out) always,
    # boss meets per active route.
    if options.npc_locations:
        total.update(npc_intro_locations_for(options))
        total.update(npc_meet_locations_for(options))
        total.update({name: location_npc_boss[name] for name in ALWAYS_MET_BOSS_LOCATIONS})
        for route in active_routes(options):
            total.update(npc_boss_locations_for(route))
    # "Met Zagreus" / "Zagreus Defeated" (user request, July 21): both are only reachable by
    # actually entering the Zagreus contract fight, and the mod's contract spawn / redirect
    # logic is itself a no-op unless goal_requires_zagreus is on (ItemManager.goal_includes_
    # zagreus -- see LocationManager.on_zagreus_met/on_zagreus_cleared). Without this gate a
    # seed that doesn't need Zagreus could still place a required item behind a check the
    # player has no in-game way to trigger.
    if options.npc_locations and options.goal_requires_zagreus:
        total[ZAGREUS_MET_LOCATION] = zagreus_extra_location_base
    if enemysanity_has_locations(options) and options.goal_requires_zagreus:
        total[ZAGREUS_DEFEATED_LOCATION] = zagreus_extra_location_base + 1
    return total


def give_all_locations_table() -> dict:
    """Every location this world can define, for the AP datapackage (max counts across
    all routes and all location systems)."""
    clear_tables()
    # The FULL ZONE_ROOM_STRIDE per zone, not each route's real (smaller) zone_room_counts, so
    # the datapackage reserves headroom for re-tuning those counts later. Safe precisely because
    # room ids key on (zone, local depth): every name this build emits carries the same id a
    # real, smaller seed gives it -- see ZONE_ROOM_STRIDE's comment.
    headroom_counts = [ZONE_ROOM_STRIDE] * 4
    for route in ROUTE_NAMES:
        fill_score_checks(route, 1000)
        fill_room_checks(route, MAX_LOCATION_MULTIPLIER, headroom_counts)
        fill_weapon_room_checks(route, MAX_LOCATION_MULTIPLIER, None, headroom_counts)
        fill_aspect_room_checks(route, MAX_LOCATION_MULTIPLIER, None, 4, headroom_counts)
    table = {}
    for route in ROUTE_NAMES:
        for zone, locs in zone_tables[route].items():
            for name, loc_id in locs.items():
                if loc_id is not None:
                    table[name] = loc_id
    # Combined score pool (separate_checks=combine_pools + point_based), full id range so ids
    # stay stable no matter what score_rewards_amount a seed lands on.
    for i in range(MAX_SCORE_CHECKS):
        table[f"{COMBINED_SCORE_PREFIX} {_pad(i + 1)}"] = \
            hades2_base_location_id + combined_score_id_base + i
    # Combined room pools (separate_checks=combine_pools), full depth range and every slot up
    # to MAX_LOCATION_MULTIPLIER, for stable ids across seeds.
    for slot in range(MAX_LOCATION_MULTIPLIER):
        for i in range(MAX_ROOMS):
            table[_flat_room_name(COMBINED_ROOM_PREFIX, i + 1, slot)] = \
                hades2_base_location_id + combined_room_id_base + slot * MAX_ROOMS + i
        for w, weapon in enumerate(WEAPON_SHORT_NAMES):
            for i in range(MAX_ROOMS):
                table[_flat_room_name(COMBINED_ROOM_PREFIX, i + 1, slot, weapon)] = \
                    hades2_base_location_id + combined_weapon_id_base \
                    + slot * WEAPON_ROOM_SLOT_STRIDE + w * WEAPON_ROOM_STRIDE + i
            for a, (_aspect_key, display_key) in enumerate(weapon_aspect_slots(weapon)):
                lane = w * ASPECT_LANES_PER_WEAPON + a
                for i in range(MAX_ROOMS):
                    name = _flat_aspect_room_name(COMBINED_ROOM_PREFIX, i + 1, slot, weapon, display_key)
                    table[name] = hades2_base_location_id + combined_aspect_id_base \
                        + slot * ASPECT_ROOM_SLOT_STRIDE + lane * ASPECT_ROOM_STRIDE + i
    table.update(location_keepsakes)
    table.update(location_enemies)
    table.update(location_npc_crossroads)
    table.update(location_npc_boss)
    table[ZAGREUS_MET_LOCATION] = zagreus_extra_location_base
    table[ZAGREUS_DEFEATED_LOCATION] = zagreus_extra_location_base + 1

    # Dream Dive: max reservation across every location_system, DREAM_MAX_REGIONS, and both
    # roster sizes (with/without ZJ) -- mirrors the pattern above (fill with MAX_* constants,
    # not a real per-seed options object, since this function takes none). Dream has no fixed
    # ROUTES entry so it can't reuse fill_route_checks/fill_*_checks -- built inline instead.
    n = DREAM_MAX_REGIONS
    per_region = DREAM_ROOM_LOCATIONS_PER_REGION
    for i in range(MAX_SCORE_CHECKS):
        table[f"Dream Score {_pad(i + 1)}"] = hades2_base_location_id + dream_score_id_base + i
    for i in range(n * per_region):
        z, local = divmod(i, per_region)
        name = _room_name(DREAM, f"Region {z + 1}", local + 1, 0)
        table[name] = hades2_base_location_id + dream_room_id_base + i
    for w, weapon in enumerate(WEAPON_SHORT_NAMES):
        for i in range(n * per_region):
            z, local = divmod(i, per_region)
            name = _room_name(DREAM, f"Region {z + 1}", local + 1, 0, weapon)
            table[name] = hades2_base_location_id + \
                dream_weapon_room_id_base + w * DREAM_WEAPON_ROOM_STRIDE + i
        for a, (_aspect_key, display_key) in enumerate(weapon_aspect_slots(weapon)):
            lane = WEAPON_SHORT_NAMES.index(weapon) * ASPECT_LANES_PER_WEAPON + a
            for i in range(n * per_region):
                z, local = divmod(i, per_region)
                name = _aspect_room_name(DREAM, f"Region {z + 1}", local + 1, 0, weapon, display_key)
                table[name] = hades2_base_location_id + \
                    dream_aspect_room_id_base + lane * DREAM_ASPECT_ROOM_STRIDE + i
    # Enemy/Miniboss/Boss counters: max possible count is the full ZJ-inclusive roster (Y/Z at
    # dream_enemy_locations=12/regions_available=12 collapses to Y/Z directly). The reserved
    # blocks are fixed-size (DREAM_*_ID_SLOTS) and must cover it.
    y_max, z_max = _dream_roster_counts([UNDERWORLD, SURFACE, NIGHTMARE], obtainable_only=False)
    if y_max > DREAM_ENEMY_ID_SLOTS or z_max > DREAM_MINIBOSS_ID_SLOTS:
        raise ValueError(f"Dream roster ({y_max} enemies, {z_max} minibosses) outgrew "
                         f"DREAM_ENEMY_ID_SLOTS/DREAM_MINIBOSS_ID_SLOTS")
    for i in range(DREAM_ENEMY_ID_SLOTS):
        table[f"Dream Enemy {_pad(i + 1)}"] = hades2_base_location_id + dream_enemy_id_base + i
    for i in range(DREAM_MINIBOSS_ID_SLOTS):
        table[f"Dream Miniboss {_pad2(i + 1)}"] = hades2_base_location_id + dream_miniboss_id_base + i
    for i in range(DREAM_MAX_REGIONS):
        table[f"Dream Boss {_pad2(i + 1)}"] = hades2_base_location_id + dream_boss_id_base + i
    # No "Beat Dream" entry: this table is the datapackage (location_name_to_id), and event
    # locations have no id -- a None value here leaked into every client's name/id lookups.
    return table


# --- Name groups --------------------------------------------------------------
location_name_groups = {
    "keepsakes": location_keepsakes.keys(),
    "enemies": list(location_enemies.keys()) + [ZAGREUS_DEFEATED_LOCATION],
    # location_npc_crossroads already contains the always-met boss entries, so dedupe.
    "npcs": list(dict.fromkeys(list(location_npc_crossroads) + list(location_npc_boss)
                                + [ZAGREUS_MET_LOCATION])),
}


class Hades2Location(Location):
    game: str = "Hades2Rogue"

    def __init__(self, player: int, name: str, address=None, parent=None):
        super(Hades2Location, self).__init__(player, name, address, parent)
        if address is None:
            self.locked = True
