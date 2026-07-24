from BaseClasses import Location

from .Routes import ROUTES, ROUTE_NAMES, UNDERWORLD, SURFACE, NIGHTMARE, MAX_ROOMS, \
    WEAPON_ROOM_STRIDE, boss_event, active_routes, NPC_ROUTE_LOCK, NPC_RANDOMIZED_HELPERS, \
    COMBAT_HELPER_NPCS, COMBAT_HELPER_NATIVE_ROUTE, ZJ_RANDOMIZED_ONLY, \
    combat_helper_native_fallback
from .Items import keepsake_titles, KEEPSAKE_NO_LOCATION, WEAPON_SHORT_NAMES, KEEPSAKE_NPC

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

# Location-system option values (match Options.LocationSystem).
POINT_BASED = 0
ROOM_BASED = 1
PER_WEAPON_ROOM_BASED = 2

# separate_checks option value (match Options.SeparateChecks; split_pools is 0).
COMBINE_POOLS = 1

# --- Location auto-scaling (room systems) ------------------------------------
# When a seed has more items than locations, the room-based systems can't just raise a
# number (a run is only ~50 rooms), so instead each room depth grants several checks. Each
# extra check is a "slot" 0..m-1 living in a disjoint id block, so ids stay stable across
# seeds. MAX_LOCATION_MULTIPLIER caps m and is what the datapackage reserves ids for; the
# slot strides below must keep every slot inside its route's reserved id range (see the ID
# layout map above): plain rooms get MAX_ROOMS ids per slot, per-weapon rooms get 1000.
MAX_LOCATION_MULTIPLIER = 8
WEAPON_ROOM_SLOT_STRIDE = 1000

# Combined (separate_checks=combine_pools) pools use route-agnostic names in their own id
# space, distinct from the per-route "Underworld Room NNNN" / "Underworld Score NNNN" ids.
# Combined means ONE shared pool that any route contributes to:
#   rooms  -- keyed on room DEPTH: clearing depth N the first time on EITHER route earns it.
#   score  -- one shared point pool: every route's cleared rooms bank into it and every check
#             is route-agnostic, so the whole pool can be earned on a single route.
COMBINED_ROOM_PREFIX = "Room"
combined_room_id_base = 9000           # "Room NNNN"            -> base + (depth-1)
combined_weapon_id_base = 60000        # "Room NNNN <Weapon>"   -> base + weapon*stride + (depth-1)
COMBINED_SCORE_PREFIX = "Score"
combined_score_id_base = 3000          # "Score NNNN"           -> base + (n-1); 1000 ids reserved
MAX_SCORE_CHECKS = 1000                # Options.ScoreRewardsAmount.range_end (id space reserved)

# Per-route, per-seed zone tables. Each maps a location name -> id (or None for
# the boss-event location). Rebuilt by setup_location_table_with_settings().
# Structured as zone_tables[route][zone_name] = { location: id_or_None }.
zone_tables = {}


def _pad(number: int) -> str:
    return f"{number:04d}"


def _room_name(prefix: str, depth: int, slot: int, weapon: str = None) -> str:
    """Build a room / per-weapon check name. slot 0 keeps the original name (backward
    compatible with pre-scaling seeds); higher slots append ' +k'. Any weapon stays the
    LAST token so the rules' weapon parsing (rsplit / last-token) keeps working."""
    name = prefix + " " + _pad(depth)
    if slot > 0:
        name += " +" + str(slot)
    if weapon:
        name += " " + weapon
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


def fill_room_checks(route: str, count: int, multiplier: int = 1) -> None:
    """room_based: one check per room-depth (1..count), depth aligned to its zone. With
    multiplier m, each depth gets m checks (slots 0..m-1) in disjoint id blocks."""
    prefix = ROUTES[route]["room_prefix"]
    id_base = hades2_base_location_id + ROUTES[route]["room_id_base"]
    zones = ROUTES[route]["zones"]
    bounds = _zone_bounds(count)
    for slot in range(multiplier):
        for z in range(4):
            zone = zones[z]
            for i in range(bounds[z], bounds[z + 1]):
                zone_tables[route][zone][_room_name(prefix, i + 1, slot)] = \
                    id_base + slot * MAX_ROOMS + i


def fill_weapon_room_checks(route: str, count: int, multiplier: int = 1, included_weapons=None) -> None:
    """per_weapon_room_based: one check per (room-depth, weapon), depth aligned to zone.
    With multiplier m, each (depth, weapon) gets m checks in disjoint id blocks. Weapons
    excluded via IncludedWeapons (Options.py) get no checks at all this seed -- `w`'s id
    offset still comes from the weapon's fixed WEAPON_SHORT_NAMES position, so ids stay
    stable regardless of which weapons this particular seed includes. included_weapons=None
    (give_all_locations_table's datapackage build) means "every weapon" -- the max universe."""
    prefix = ROUTES[route]["room_prefix"]
    id_base = hades2_base_location_id + ROUTES[route]["weapon_room_id_base"]
    zones = ROUTES[route]["zones"]
    bounds = _zone_bounds(count)
    for slot in range(multiplier):
        for w, weapon in enumerate(WEAPON_SHORT_NAMES):
            if included_weapons is not None and weapon not in included_weapons:
                continue
            for z in range(4):
                zone = zones[z]
                for i in range(bounds[z], bounds[z + 1]):
                    zone_tables[route][zone][_room_name(prefix, i + 1, slot, weapon)] = \
                        id_base + slot * WEAPON_ROOM_SLOT_STRIDE + w * WEAPON_ROOM_STRIDE + i


def combine_active(options) -> bool:
    """combine_pools only does anything when both routes are actually generated; with a
    single route there's nothing to combine, so it behaves like split_pools."""
    return options.separate_checks.value == COMBINE_POOLS and len(active_routes(options)) > 1


def _combined_room_count() -> int:
    """Size of the shared (combined) room pool. Both routes use the same room_count, so a
    single shared pool of that size covers a run's depth either way."""
    return ROUTES[UNDERWORLD]["room_count"]


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
    count = _combined_room_count()
    table = {}
    if system == ROOM_BASED:
        for slot in range(multiplier):
            for i in range(count):
                table[_room_name(COMBINED_ROOM_PREFIX, i + 1, slot)] = \
                    hades2_base_location_id + combined_room_id_base + slot * MAX_ROOMS + i
    elif system == PER_WEAPON_ROOM_BASED:
        included_weapons = options.included_weapons.value
        for slot in range(multiplier):
            for w, weapon in enumerate(WEAPON_SHORT_NAMES):
                if weapon not in included_weapons:
                    continue
                for i in range(count):
                    table[_room_name(COMBINED_ROOM_PREFIX, i + 1, slot, weapon)] = \
                        hades2_base_location_id + combined_weapon_id_base \
                        + slot * WEAPON_ROOM_SLOT_STRIDE + w * WEAPON_ROOM_STRIDE + i
    return table


def fill_route_checks(route: str, options, multiplier: int = 1) -> None:
    """Fill a route's zone tables according to the chosen location system. Under
    combine_pools NOTHING is filled per-route here -- every system's checks live in a shared
    region instead ("Combined Rooms" / "Combined Score"); only the per-route boss events
    remain."""
    system = options.location_system.value
    if combine_active(options):
        return
    if system in (ROOM_BASED, PER_WEAPON_ROOM_BASED):
        if system == ROOM_BASED:
            fill_room_checks(route, ROUTES[route]["room_count"], multiplier)
        else:
            fill_weapon_room_checks(route, ROUTES[route]["room_count"], multiplier,
                                    options.included_weapons.value)
    else:
        fill_score_checks(route, _score_count_for(route, options))


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


# --- Enemy locations (enemy_locations) ----------------------------------------
# First-time defeat checks, one per enemy type. Each enemy is mapped to the route + zone
# (layer) it appears in, so the location lives in that zone's region and is reachable
# exactly when that zone is. (Boss enemies are listed here as distinct checks from the
# "Beat <Boss>" route events.) Order is fixed so ids stay stable.
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
         "Scylla and the Sirens",
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

# 13 enemy names that exist identically in the Underworld roster above (Hades II's own
# Tartarus/Oceanus already recycle these H1 monster types) and ALSO appear in Nightmare --
# name -> every (route, zone index) it can be found in. A location's PARENT REGION is a
# hard reachability gate in AP (region unreachable => location unreachable, regardless of
# any access_rule), so a name that's reachable via either of two different zones can't stay
# placed in one of those zones' regions with an "or" rule bolted on -- that would only ever
# relax its OWN rule, not bypass the other zone's region requirement. Instead these 13 are
# pulled out of their normal zone placement entirely (see the enemy-index loop below, which
# tracks them in SHARED_ENEMY_LOCATIONS instead of ENEMY_BY_ZONE) and placed in the
# Crossroads hub instead (always immediately reachable), with their real gating done purely
# via an access_rule checking "any of these zones reachable" (Rules._set_shared_enemy_rules)
# -- the same "neutral bucket + access_rule" shape already used for the Combined Rooms pool.
# ids/route-ownership (location_enemies/ENEMY_ROUTE) are unchanged, but existence is gated
# on the NIGHTMARE route alone (July 18 user ruling): the H1 route spawns these names
# consistently, while their Underworld-side appearances (Asphodel-anomaly detours, the odd
# H2 Tartarus/Oceanus callback) are too rare to justify putting 13 checks in a seed that
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
    "King Vermin Defeated": [(UNDERWORLD, 1), (NIGHTMARE, 3)],
}

# "Mini-boss" enemy checks (July 17): the only enemy names whose reachability is gated behind
# their zone's own boss being beaten (Rules.py) rather than just the zone being reachable --
# every OTHER enemy (regular/trash spawns) only needs its zone reachable, same as before the
# July 17 tightening pass. Two kinds of name land here:
#  - Real secondary mini-boss encounters, identified from the mod's own unit-id data
#    (Hades2Rogue_mod/LocationManager.lua's "_Miniboss"/"MiniBoss"/"Miniboss"-suffixed unit ids,
#    e.g. ZombieAssassin_Miniboss -> Master-Slicer, Boar -> Erymanthian Boar "City of Ephyra
#    miniboss") -- these are genuinely tougher, optional-feeling fights within a zone.
#  - Names that are the SAME encounter as the zone's own listed boss (e.g. "Chronos", "The
#    Cyclops Polyphemus", "Scylla and the Sirens") -- their enemy-defeat check can only ever
#    fire by beating that exact boss, so gating them on anything looser would be logically
#    wrong regardless of the July 17 tightening.
MINIBOSS_ENEMY_NAMES = {
    # Underworld
    "Headmistress Hecate", "Master-Slicer", "Thorn-Weeper",       # Erebus (boss-identical + mini-bosses):
    # Thorn-Weeper only spawns as a regular enemy after you first defeat it in a dedicated
    # mini-boss room, so its "Defeated" check needs the same boss-tier gate as a real mini-boss.
    "Scylla and the Sirens", "Hellifish", "Deep Serpent",         # Oceanus (boss-identical + mini-bosses)
    "Queen Lamia",                                                # Fields of Mourning (mini-boss)
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
    # Shared (Underworld/Nightmare): the only one of the 13 SHARED_ENEMY_ZONES names that's an
    # actual mini-boss (CrawlerMiniboss/HadesCrawlerMiniBoss) -- the other 12 are regular spawns.
    "King Vermin",
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
location_enemies = {}          # name -> id (every enemy, both routes)
ENEMY_ROUTE = {}               # name -> route (existence gate: only in the table when active)
ENEMY_BY_ZONE = {}             # (route, zone) -> [enemy names] (normal single-zone placement)
SHARED_ENEMY_LOCATIONS = []    # names placed in Crossroads instead -- see SHARED_ENEMY_ZONES
_enemy_index = 0
for _route in ROUTE_NAMES:
    for _zi, _layer in enumerate(ENEMY_LAYERS[_route]):
        _zone = ROUTES[_route]["zones"][_zi]
        ENEMY_BY_ZONE.setdefault((_route, _zone), [])
        for _name in _layer:
            _loc = f"{_name} Defeated"
            location_enemies[_loc] = enemy_location_base + _enemy_index
            ENEMY_ROUTE[_loc] = _route
            if _loc in SHARED_ENEMY_ZONES:
                SHARED_ENEMY_LOCATIONS.append(_loc)
            else:
                ENEMY_BY_ZONE[(_route, _zone)].append(_loc)
            _enemy_index += 1


def enemy_locations_for(route: str) -> dict:
    """Every enemy check owned by `route`, plus -- when `route` is Nightmare -- the 13
    shared-name checks (SHARED_ENEMY_ZONES). July 18 (user ruling): the shared H1-callback
    names only exist in the pool when the NIGHTMARE route is in the seed. Their Underworld-
    side spawns (H2's own Oceanus/Asphodel-anomaly/Tartarus callbacks) are too rare/
    inconsistent to be the thing that puts them in the pool -- but when Nightmare IS in
    the seed, an Underworld-side kill still satisfies the check (the mod's send gate is
    seed-level, not current-route -- see LocationManager's ROUTE_GATED_CHECKS). The 13
    are skipped from ENEMY_ROUTE's own Underworld emission via their SHARED_ENEMY_ZONES
    membership."""
    table = {name: location_enemies[name]
             for name, r in ENEMY_ROUTE.items()
             if r == route and name not in SHARED_ENEMY_ZONES}
    if route == NIGHTMARE:
        for name in SHARED_ENEMY_ZONES:
            table[name] = location_enemies[name]
    return table


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
# in NPC_BOSS_MEET above).
NPC_NO_MEET = {"Zagreus"}

# The Crossroads cast: every keepsake-giving character who isn't a route boss (or otherwise
# unmeetable), plus a few meet-able NPCs who don't give keepsakes. Hypnos (Test Run 5 #5) wasn't
# in the keepsake cast, so "Met Hypnos" never existed; he's added here (met once he's awake).
# Thanatos/Orpheus/Achilles (Nightmare cast, re-added July 16 -- see Routes.NPC_ROUTE_LOCK)
# are deliberately appended at the END, after Hypnos, instead of taking their natural
# KEEPSAKE_NPC positions: location_npc_meet numbers ids by NPC_CAST order, and slotting them
# mid-list would shift "Met Hypnos"'s established id.
NPC_EXTRA_CAST = ["Hypnos", "Thanatos", "Orpheus", "Achilles"]
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
    already uses for Eris/Orpheus/Achilles, just conditioned on this option's mode.
    SUB-EXCEPTION (Thanatos/IncludeZagreusJourney, July 22): Routes.combat_helper_native_fallback
    carves Thanatos back out of that native-route lock when IncludeZagreusJourney is still on --
    ItemManager.apply_combat_helper_random forces his foreign-zone (Underworld/Surface) flags on
    regardless of mode in that situation (mod side), since he'd otherwise have nowhere to ever
    spawn without Nightmare active. He falls through to the NPC_RANDOMIZED_HELPERS branch below
    instead, same as any other randomized helper.
    EXCEPTION (IncludeZagreusJourney): Routes.ZJ_RANDOMIZED_ONLY (Sisyphus/Eurydice/Patroclus/
    Thanatos) are randomized helpers that nonetheless only exist because Zagreus' Journey is
    installed -- when that option is off they're locked out unconditionally, even though
    they'd otherwise be exempt as randomized helpers. Orpheus/Achilles/Megaera need no such
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
    included this seed, instead of leaving an ungated dead check behind."""
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
    """Active-seed intro-beat locations (SHUSH Homer, Find Hecate 1-3): all four are part of
    Hecate's hide-and-seek flashback sequence, which the game only triggers after enough
    completed Underworld runs specifically -- on a seed that excludes the Underworld it can
    never fire in-game. Mirrors keepsake_locations_for/npc_meet_locations_for's route-lock
    filter: drop them from the table entirely rather than leave an unreachable dead check
    that AP's fill could still place a required item behind."""
    if UNDERWORLD in active_routes(options):
        return dict(location_npc_intro)
    return {}


# Zagreus "Met" / "Defeated" (July 17): two REAL checks living at the always-open Crossroads,
# distinct from the "Beat Zagreus" goal event -- gated in Rules.py by how beatable the OTHER
# bosses are (Met = any route's 1st boss beatable; Defeated = stricter than the hardest boss
# tier). Existence mirrors their naming siblings: Met follows npc_locations, Defeated follows
# enemy_locations -- AND (July 21) both also require goal_requires_zagreus, since neither is
# actually reachable in-game unless it's on (see setup_location_table_with_settings).
ZAGREUS_MET_LOCATION = "Met Zagreus"
ZAGREUS_DEFEATED_LOCATION = "Zagreus Defeated"
zagreus_extra_location_base = hades2_base_location_id + 6140


# -----------------------------------------------------------------------------


def setup_location_table_with_settings(options, multiplier: int = 1) -> dict:
    """Build the flat active location table (name -> id) for this seed. multiplier scales
    the room-based check pools (see MAX_LOCATION_MULTIPLIER)."""
    clear_tables()
    for route in active_routes(options):
        fill_route_checks(route, options, multiplier)

    total = {}
    for route in active_routes(options):
        for zone, locs in zone_tables[route].items():
            total.update(locs)

    # Zagreus (secret superboss): a standalone event, not tied to either route's zone-boss
    # list, so it isn't in zone_tables. Always present, like the Chronos/Typhon boss events
    # (harmless if the goal doesn't need it -- see Rules.py's access rule).
    total[boss_event("Zagreus")] = None

    # combine_pools: the shared pools' checks live outside the per-route zone tables.
    if combine_active(options):
        if options.location_system.value in (ROOM_BASED, PER_WEAPON_ROOM_BASED):
            total.update(combined_room_table(options, multiplier))
        else:
            total.update(combined_score_table(options))

    # Keepsake checks exist in randomized (1) and progressive (2), not normal (0).
    if options.keepsakesanity.value != 0:
        total.update(keepsake_locations_for(options))

    # Enemy first-defeat checks, per active route.
    if options.enemy_locations:
        for route in active_routes(options):
            total.update(enemy_locations_for(route))

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
    if options.enemy_locations and options.goal_requires_zagreus:
        total[ZAGREUS_DEFEATED_LOCATION] = zagreus_extra_location_base + 1
    return total


def give_all_locations_table() -> dict:
    """Every location this world can define, for the AP datapackage (max counts across
    all routes and all location systems)."""
    clear_tables()
    for route in ROUTE_NAMES:
        fill_score_checks(route, 1000)
        fill_room_checks(route, MAX_ROOMS, MAX_LOCATION_MULTIPLIER)
        fill_weapon_room_checks(route, MAX_ROOMS, MAX_LOCATION_MULTIPLIER)
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
            table[_room_name(COMBINED_ROOM_PREFIX, i + 1, slot)] = \
                hades2_base_location_id + combined_room_id_base + slot * MAX_ROOMS + i
        for w, weapon in enumerate(WEAPON_SHORT_NAMES):
            for i in range(MAX_ROOMS):
                table[_room_name(COMBINED_ROOM_PREFIX, i + 1, slot, weapon)] = \
                    hades2_base_location_id + combined_weapon_id_base \
                    + slot * WEAPON_ROOM_SLOT_STRIDE + w * WEAPON_ROOM_STRIDE + i
    table.update(location_keepsakes)
    table.update(location_enemies)
    table.update(location_npc_crossroads)
    table.update(location_npc_boss)
    table[ZAGREUS_MET_LOCATION] = zagreus_extra_location_base
    table[ZAGREUS_DEFEATED_LOCATION] = zagreus_extra_location_base + 1
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
            self.event = True
            self.locked = True
