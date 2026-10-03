# Shared definitions for the three routes (Underworld, Surface, Nightmare). All are clean
# 4-zone paths, so Locations/Regions/Rules parameterize over this table.

UNDERWORLD = "Underworld"
SURFACE = "Surface"
NIGHTMARE = "Nightmare"
# Dream Dive (Hypnos's vanilla postgame content, extended via the third-party DreamDiveTweaks mod).
# Unlike the other 3 routes, Dream has no fixed zone count (dream_region_count is a per-seed option,
# 1-12) and no fixed boss identity per region (DreamDiveTweaks randomizes which biome -- and therefore
# which native boss -- lands in each region slot, every attempt). It is deliberately NOT added to
# ROUTES/ROUTE_NAMES below: every consumer of ROUTES[route]["zones"/"bosses"] assumes a static,
# import-time-fixed 4-zone/4-boss shape (Locations._zone_bounds hardcodes //4, Rules.set_rules's
# per-route loop walks a fixed 4-entry BOSS_TIER_PERCENT, __init__.py's Progressive-item pool count
# hardcodes 3 = len(zones)-1) -- none of which fits a variable-length, boss-identity-less route. Dream
# gets its own dedicated code paths in Locations.py/Rules.py/Regions.py/Items.py instead (see
# dream_zones() below for the one piece that IS reused generically: goal/victory wiring via
# _BOSS_ROUTES/GOAL_BOSSES, which only needs a boss-keyword->route mapping and one Victory item, not a
# zone list).
DREAM = "Dream"

# Room-check id space reserved per route, per location-multiplier slot, in the room-based
# systems. Room ids key on (zone index, depth within that zone) -- see
# Locations.ZONE_ROOM_STRIDE -- so this is really 4 zones * ZONE_ROOM_STRIDE(15), and the
# binding constraint is per-zone (no zone may exceed ZONE_ROOM_STRIDE), NOT each route's
# "room_count" total below. Raising either means raising both together and re-checking every
# route's id range in Locations.py's ID layout map.
MAX_ROOMS = 60
# Per-weapon room locations reserve this many ids per weapon, per route.
WEAPON_ROOM_STRIDE = 100

# Per-zone room checks (2026-09-22 stability pass, user decision). Two numbers per zone:
#  - "zone_room_counts" (N): how many room checks the zone has -- the most rooms player logs showed
#    scoring before the zone's boss, +1 for the boss room, capped at Locations.ZONE_ROOM_STRIDE.
#  - "zone_room_guaranteed" (K): how many rooms every run scores before the boss (the minimum
#    across player logs -- a safe lower bound; lowering K is always safe, raise it only with
#    evidence). Rooms 1..K are in logic as soon as the zone is reachable; rooms K+1..N need the
#    zone's boss to be beatable (Rules._set_room_tail_rules). Beating the zone's boss sends every
#    unsent room check in that zone (the mod's LocationManager.on_zone_boss_defeated), so the tail
#    can never be stranded by a short run.
# Mirrored by hand in the mod's Routes.ZONE_ROOM_COUNTS / Routes.ZONE_ROOM_GUARANTEED
# (tools/sync_check.py compares them).
ROUTES = {
    UNDERWORLD: {
        "zones": ["Erebus", "Oceanus", "Fields of Mourning", "Tartarus"],
        "zone_display": ["Erebus", "Oceanus", "Fields of Mourning", "Tartarus"],
        "zone_room_counts": [13, 10, 10, 12],
        "zone_room_guaranteed": [10, 6, 4, 2],
        "bosses": ["Hecate", "Scylla", "Cerberus", "Chronos"],
        "score_prefix": "Underworld Score",      # point-based check-name prefix
        "score_id_base": 0,                      # point ids: base + 0..999
        "room_id_base": 7000,                    # room ids: base + 7000..7000+MAX_ROOMS
        "weapon_room_id_base": 10000,            # per-weapon ids: base + 10000 + weapon*stride + depth
        "aspect_room_id_base": 100000,           # per-aspect ids: base + 100000 + lane*stride + depth
        "combined_room_depth": 43,               # combine_pools' shared-pool depth (see Locations._combined_room_count)
        "progressive": "Progressive Underworld",
        "final_boss": "Chronos",
    },
    SURFACE: {
        "zones": ["City of Ephyra", "Rift of Thessaly", "Mount Olympus", "The Summit"],
        "zone_display": ["City of Ephyra", "Rift of Thessaly", "Mount Olympus", "The Summit"],
        "zone_room_counts": [10, 14, 10, 10],
        "zone_room_guaranteed": [8, 12, 9, 3],
        "bosses": ["Cyclops", "Eris", "Prometheus", "Typhon"],
        "score_prefix": "Surface Score",
        "score_id_base": 2000,                   # point ids: base + 2000..2999
        "room_id_base": 8000,                    # room ids: base + 8000..8000+MAX_ROOMS
        "weapon_room_id_base": 20000,            # per-weapon ids: base + 20000 + weapon*stride + depth
        "aspect_room_id_base": 130000,           # per-aspect ids: base + 130000 + lane*stride + depth
        "combined_room_depth": 39,
        "progressive": "Progressive Surface",
        "final_boss": "Typhon",
    },
    NIGHTMARE: {
        # Hades 1's original route, ported into Hades II by the third-party "Zagreus'
        # Journey" mod (opt-in, see Options.IncludeNightmare -- default off since it needs that
        # mod installed). Zone 0's boss is a random pick of one of the three Furies; zone 2's
        # bosses (Theseus & Asterius) are fought together but tracked as separate enemy/NPC
        # checks -- see Locations.py/Rules.py for how those are handled around this shared
        # "bosses" list (which only drives the single zone-clear event per zone).
        # "Tartarus" is disambiguated to "Tartarus (Nightmare)": Hades II's own Underworld
        # route already has a zone literally named "Tartarus" (its 4th zone) -- AP regions
        # must have a globally unique name per player, so an exact duplicate would silently
        # collide (two Region objects sharing one name/entrance-cache key). The other 3
        # zone names (Asphodel/Elysium/Styx) don't collide with anything existing.
        # zone_display drops the "(Nightmare)" disambiguation suffix -- room-check names are
        # already prefixed with the route word ("Nightmare Tartarus Room 01"), so it isn't
        # needed there the way it is for AP's globally-unique Region name.
        "zones": ["Tartarus (Nightmare)", "Asphodel", "Elysium", "Styx"],
        "zone_display": ["Tartarus", "Asphodel", "Elysium", "Styx"],
        "zone_room_counts": [13, 10, 11, 12],
        "zone_room_guaranteed": [10, 6, 8, 8],
        "bosses": ["The Furies", "Bone Hydra", "Theseus and Asterius", "Hades"],
        "score_prefix": "Nightmare Score",
        "score_id_base": 4000,                   # point ids: base + 4000..4999
        "room_id_base": 8500,                    # room ids: base + 8500..8500+MAX_ROOMS (slots up to +479)
        "weapon_room_id_base": 40000,            # per-weapon ids: base + 40000 + weapon*stride + depth
        "aspect_room_id_base": 160000,           # per-aspect ids: base + 160000 + lane*stride + depth
        "combined_room_depth": 40,
        "progressive": "Progressive Nightmare",
        "final_boss": "Hades",
    },
}

ROUTE_NAMES = [UNDERWORLD, SURFACE, NIGHTMARE]
for _route in ROUTE_NAMES:
    ROUTES[_route]["room_count"] = sum(ROUTES[_route]["zone_room_counts"])

# NPCs who are only ever encountered on one route (Known Bugs/"Logic is all out of
# whack"). Their "<NPC> Keepsake" and "Met <NPC>" locations only exist in the per-seed
# table when that route is active (see Locations._route_locked); Rules.py reuses this to
# gate reachability once the location *does* exist.
#
# July 18: this table shrank from 16 entries to 3. The story-room NPCs
# (zerp-NPCRoomRandomizer shuffles WHO appears in every story slot, across ALL routes --
# Patroclus really was met in an Underworld run, replacing Arachne) and the combat-assist
# NPCs (zerp-Extended_NPC_Encounters gives all of them encounters in every route's zones)
# are no longer route-bound at all; they moved to NPC_RANDOMIZED_HELPERS below. What
# remains here are NPCs genuinely nailed to one route's own content:
#   - Eris: met via the Surface boss fight / bath appearances (her Underworld curse-ambush
#     cameo is deliberately not trusted -- see Locations.ALWAYS_MET_BOSSES note).
#   - Orpheus: spawns only in ZJ's Tartarus rooms (NPC_Orpheus_01, additionally gated on
#     the "Allow Orpheus to Spawn in Tartarus" item -- Rules.KEEPSAKE_ITEM_GATE).
# Megaera is NOT here -- she's a route boss, not Crossroads cast, so her "Met Megaera"
# gating comes from her NPC_BOSS_MEET zone tuple instead (Locations.py).
# Achilles used to be here too (Nightmare-locked, native Elysium content alongside
# Patroclus) but his "Met Achilles"/"Achilles Keepsake" were removed as locations entirely
# July 31 (user ruling) -- no route lock needed for a location that no longer exists.
NPC_ROUTE_LOCK = {
    "Eris": SURFACE,
    "Orpheus": NIGHTMARE,
}

# NPCs whose meet/gift moment is a RANDOMIZED helper appearance, reachable on whatever
# route the player can actually play (July 18). Two mechanisms, both hard dependencies of
# the game mod (manifest.json), both rerolled every run:
#   - Story rooms: zerp-NPCRoomRandomizer swaps any of the 10 story rooms (F/G/H_Bridge01/
#     I/N/O/P_Story01 + ZJ's A/X/Y_Story01) into any story slot on any route. Every route's
#     FIRST zone hosts a story slot (F/N/A_Story01), so each of these NPCs is reachable
#     (over repeated runs) once any active route's zone 0 is.
#   - Combat-assist encounters: zerp-Extended_NPC_Encounters adds each combat NPC's
#     encounters to every route's zones (verified per-NPC zone tables in its
#     artemis/heracles/icarus/nemesis/athena/thanatos.lua), with our
#     ItemManager.apply_extended_npc_unlock stripping the lifetime intro gates.
# Their locations therefore ALWAYS exist (any active route can produce them). "Hades" is
# here because his I_Story01 room shuffles like the rest (he was previously the lone
# NPC_MULTI_ROUTE_LOCK entry -- that table and Rules._set_hades_met_rule are gone,
# subsumed by this). Nemesis isn't listed: she's KEEPSAKE_FREE (met at the Crossroads from
# the start), so nothing route-gates her anyway.
NPC_RANDOMIZED_HELPERS = {
    # story-room NPCs (zerp-NPCRoomRandomizer)
    "Arachne", "Narcissus", "Echo", "Hades", "Medea", "Circe", "Dionysus",
    "Sisyphus", "Eurydice", "Patroclus",
    # combat-assist NPCs (zerp-Extended_NPC_Encounters)
    "Artemis", "Heracles", "Icarus", "Athena", "Thanatos",
}

# The subset of NPC_RANDOMIZED_HELPERS that only exist because Zagreus' Journey is installed:
# Sisyphus/Eurydice/Patroclus are ZJ's own story-room cast (borrowed into other routes by
# zerp-NPCRoomRandomizer), and Thanatos's spawn -- native AND foreign-zone alike -- calls
# through ZJ's own HandleThanatosSpawn (reload.lua). Unlike the rest of NPC_RANDOMIZED_HELPERS,
# these 4 are never reachable when IncludeZagreusJourney is off, regardless of which routes are
# active -- see Locations._route_locked_out and ItemManager.zj_content_enabled (mod side).
ZJ_RANDOMIZED_ONLY = {"Sisyphus", "Eurydice", "Patroclus", "Thanatos"}

# Combat-assist cast (CombatHelperSanity) -- the zerp-Extended_NPC_Encounters half of
# NPC_RANDOMIZED_HELPERS, as opposed to the story-room half (helper_story_npcs/
# helper_story_npcs_nightmare in Items.py, gated by the separate HelperRoomSanity option).
# Nemesis is deliberately excluded from COMBAT_HELPER_NPCS: she's in KEEPSAKE_FREE
# (Rules.py) and is met at the Crossroads from the start regardless of this option -- her
# "Met"/"Keepsake" locations never get an item or area rule from CombatHelperSanity. She
# still gets her own "Nemesis Helper" item (COMBAT_HELPER_NPCS_ALL) -- under items/
# items_random it gates whether her combat encounter can actually fire in-game, just not
# her (separately, always-reachable) Crossroads meet.
COMBAT_HELPER_NPCS = ["Artemis", "Heracles", "Icarus", "Athena", "Thanatos"]
COMBAT_HELPER_NPCS_ALL = COMBAT_HELPER_NPCS + ["Nemesis"]

# Each combat-assist NPC's native (earliest-hosting) route -- the route half of Rules.
# KEEPSAKE_HARD's (route, area, tier) entries for the same 5 NPCs, duplicated here (route
# only, no area/tier) so Locations.py can use it without importing Rules.py (which itself
# imports Routes.py -- importing the other way would be circular). Used only when
# CombatHelperSanity is "unlocked"/"items" (native-only, modes 0/1): if the NPC's native
# route isn't in the seed at all, they have nowhere to ever spawn, so their "Met"/"Keepsake"
# locations must be dropped instead of left permanently unreachable (mirrors NPC_ROUTE_LOCK's
# existing drop-on-excluded-route behavior for Eris/Orpheus). Keep in sync with
# Rules.KEEPSAKE_HARD if either ever changes.
COMBAT_HELPER_NATIVE_ROUTE = {
    "Artemis": UNDERWORLD, "Heracles": SURFACE, "Icarus": SURFACE, "Athena": SURFACE,
    "Thanatos": NIGHTMARE,
}


def combat_helper_native_fallback(npc: str, options, routes: list) -> bool:
    """True when `npc`'s native route (COMBAT_HELPER_NATIVE_ROUTE) isn't part of this seed, but
    it's a ZJ-exclusive helper (ZJ_RANDOMIZED_ONLY -- today only Thanatos) and IncludeZagreusJourney
    is still on. Unlike the other 4 combat-assist NPCs, Thanatos has no real "native" location once
    Nightmare itself isn't in the seed -- so under combat_helper_sanity's native-only modes (0/1),
    ItemManager.apply_combat_helper_random (mod side) forces his zerp-Extended_NPC_Encounters
    foreign-zone flags (Underworld/Surface) on regardless of mode in exactly this situation, instead
    of leaving him with nowhere to ever spawn. Callers (Locations._route_locked_out, Rules.py's
    KEEPSAKE_HARD loop) use this to treat him like a normal randomized helper -- reachable via
    whichever OTHER routes are active -- instead of native-route-locking him out."""
    if npc not in ZJ_RANDOMIZED_ONLY:
        return False
    native_route = COMBAT_HELPER_NATIVE_ROUTE.get(npc)
    if native_route is None or native_route in routes:
        return False
    return bool(getattr(options, "include_zagreus_journey", True))

# Area gate for NPC_RANDOMIZED_HELPERS (July 19, second revision -- user rejected both an
# earlier zone-0 pass as "too early" AND a flat "reach zone 3 on any one route" pass as
# still too generous when several routes are active): reachable once the player can reach
# a route's own FINAL zone (index 3) on at least ceil(active_routes / 2) of the active
# routes -- 1 needed with 1 or 2 routes active, 2 needed with 3. Region reachability is
# cumulative along a route's own zone chain (you can't reach zone 3 without having already
# cleared zones 0-2), so this doesn't require the story-room/combat-assist mechanism to
# specifically spawn IN zone 3 -- reaching that deep already means many earlier
# opportunities (in the zones that DO host these NPCs) have passed, which is what "late but
# not impossible" is actually about. No per-NPC override needed for this reason: every
# NPC in NPC_RANDOMIZED_HELPERS has at least one hosting slot/encounter somewhere in zones
# 0-2 of every route it can appear on (verified against the story-room table and each
# combat-assist NPC's own zone-letter tables in artemis/heracles/icarus/athena/thanatos.lua).
NPC_RANDOMIZED_ZONE_INDEX = 3

# The bosses whose defeat can be part of the Goal, and (when it's a route's final boss)
# which route that is. "zagreus" maps to no route -- he's a secret superboss reachable via
# either route's zone index 1, not tied to a specific route's zone chain. "dream" maps to
# DREAM the same way chronos/typhon/hades map to their routes -- a single "Beat Dream"/
# "Dream Victory" event+item pair, exactly mirroring every other route (see manual comment
# above DREAM's definition for why Dream can't reuse the rest of ROUTES' machinery). This is
# the one piece of Dream's wiring that generalizes for free: goal_includes/_goal_toggle/
# _hades2_can_get_victory (Rules.py) only care about a boss-keyword->route mapping and
# one-time ownership of "<Boss> Victory", never about zone shape.
GOAL_BOSSES = ["chronos", "typhon", "hades", "zagreus", "dream"]
_BOSS_ROUTES = {"chronos": UNDERWORLD, "typhon": SURFACE, "hades": NIGHTMARE, "dream": DREAM}

ALL_SELECTED = 0
ANY_SELECTED = 1


def _goal_toggle(options, boss: str) -> bool:
    if boss == "zagreus":
        return bool(options.goal_requires_zagreus)
    return _BOSS_ROUTES[boss] in options.goals_required.value


def zagreus_reachable(routes) -> bool:
    """Whether Zagreus can be fought on a seed made of `routes`. His contract only spawns from
    the 4-zone routes (Rules.set_rules' zagreus_final_zones) -- a Dream Dive never offers it --
    so a seed whose only route is Dream can't have him in its goal."""
    return any(route in routes for route in ROUTE_NAMES)


def _goal_forced_routes(options) -> list:
    """The route(s) the current Goal forces to be included (so the goal stays reachable
    even if the player excluded that route). goal_mode=all_selected forces every route named
    by an entry in Goals Required. goal_mode=any_selected normally forces nothing --
    whichever route the player kept satisfies it -- but only while at least one selected
    boss is actually achievable: zagreus (tied to no route, reachable from any included
    4-zone route -- a Dream Dive never meets him, see zagreus_reachable), or a boss whose
    route the player included. When NONE are (e.g. only "Underworld" in
    Goals Required with the Underworld excluded from Include Regions), the goal is
    impossible and generation used to die deep in fill with an opaque "Game appears as
    unbeatable" -- so force the first selected boss's route in instead, mirroring
    all_selected's "keep the goal reachable" behavior."""
    toggled = [(boss, _BOSS_ROUTES[boss]) for boss in GOAL_BOSSES
               if boss in _BOSS_ROUTES and _goal_toggle(options, boss)]
    if options.goal_mode.value == ANY_SELECTED:
        if not toggled:
            return []
        included = set(options.include_regions.value)
        if _goal_toggle(options, "zagreus") and zagreus_reachable(included):
            return []
        if any(route in included for _boss, route in toggled):
            return []
        return [toggled[0][1]]
    return [route for _boss, route in toggled]


def active_routes(options) -> list:
    """The routes actually generated for this seed: the player's Include Regions selection,
    plus any route the goal forces in (so the goal is always reachable). ROUTE_NAMES stays the
    3 static routes on purpose (see DREAM's definition comment) -- DREAM is appended separately
    so callers that still need "just the 4-zone routes" can keep iterating ROUTE_NAMES directly."""
    routes = set(options.include_regions.value)
    for route in _goal_forced_routes(options):
        routes.add(route)
    return [route for route in ROUTE_NAMES + [DREAM] if route in routes]


def dream_zones(options) -> list:
    """Dream's per-seed synthetic zone list -- one entry per configured region
    (dream_region_count, 1-12), built fresh from options instead of a static ROUTES entry since
    the count varies per seed. Named "Dream Region <i>" (1-indexed) rather than a real biome
    name since DreamDiveTweaks randomizes which biome lands in each slot every attempt -- the
    slot POSITION is what's stable, not the biome identity (see project memory
    project_dream_dive_feature_design for the full reasoning). Regions.py creates one real
    Region per entry and chains them exactly like every other route's zone list."""
    return [f"Dream Region {i}" for i in range(1, int(options.dream_region_count.value) + 1)]


def goal_includes(options, boss: str) -> bool:
    """Whether `boss` ("chronos"/"typhon"/"hades"/"zagreus") is part of the active goal."""
    return _goal_toggle(options, boss)


def boss_event(boss: str) -> str:
    return "Beat " + boss


def boss_victory(boss: str) -> str:
    return boss + " Victory"
