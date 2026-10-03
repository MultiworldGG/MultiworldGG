from .Routes import ROUTES, DREAM, active_routes, boss_event


def create_regions(ctx, location_database: dict) -> None:
    from . import create_region
    from .Locations import zone_tables, keepsake_locations_for, ENEMY_BY_ZONE, \
        NPC_BOSS_BY_ZONE, npc_intro_locations_for, npc_meet_locations_for, \
        ALWAYS_MET_BOSS_LOCATIONS, combine_active, combined_room_table, \
        combined_score_table, ROOM_BASED, PER_WEAPON_ROOM_BASED, PER_ASPECT_ROOM_BASED, \
        SHARED_ENEMY_LOCATIONS, \
        ZAGREUS_MET_LOCATION, ZAGREUS_DEFEATED_LOCATION, enemysanity_has_locations, \
        filter_minibosses

    routes = active_routes(ctx.options)
    # Dream's zone list is NOT ROUTES[DREAM]["zones"] (no such static entry -- see
    # Routes.DREAM's definition comment). ctx.dream_zone_tables (this player's snapshot of
    # zone_tables[DREAM], taken in Hades2World.create_regions) is the single source of truth for
    # which regions actually exist THIS seed (already clamped to the native
    # DreamDiveTweaks pool by Locations.fill_dream_checks, which may be < the raw
    # dream_region_count option if ZJ isn't active) -- reading it here instead of
    # recomputing keeps Regions.py/Rules.py from ever disagreeing on region count.
    dream_zone_list = list(ctx.dream_zone_tables.keys()) if DREAM in routes else []
    room_systems = (ROOM_BASED, PER_WEAPON_ROOM_BASED, PER_ASPECT_ROOM_BASED)
    combined_rooms = combine_active(ctx.options) and ctx.options.location_system.value in room_systems
    combined_score = combine_active(ctx.options) and ctx.options.location_system.value not in room_systems

    crossroads_exits = ["Descend " + route for route in routes]

    menu_exits = ["Start"]
    if combined_rooms:
        menu_exits.append("To Combined Rooms")
    if combined_score:
        menu_exits.append("To Combined Score")
    ctx.multiworld.regions += [
        create_region(ctx.multiworld, ctx.player, location_database, "Menu", None, menu_exits),
    ]

    # Each active route's 4 zones: an exit to the next zone, plus a death exit to the hub.
    for route in routes:
        if route == DREAM:
            continue  # handled separately below (variable region count, no ENEMY_BY_ZONE/NPC)
        zones = ROUTES[route]["zones"]
        for i, zone in enumerate(zones):
            locs = [loc for loc in zone_tables[route][zone]]
            if enemysanity_has_locations(ctx.options):
                # Shuffled modes place each enemy check in the zone where it is actually
                # killable (its preimage's zone), not its native one -- see
                # Locations.enemy_zone_placement. Falls back to the native table for every other
                # mode and for callers that never built one.
                placement = getattr(ctx, "enemy_zone_placement", None) or ENEMY_BY_ZONE
                locs += filter_minibosses(placement.get((route, zone), []),
                                           bool(ctx.options.include_minibosses))
            if ctx.options.npc_locations:
                locs += NPC_BOSS_BY_ZONE.get((route, zone), [])
            exits = ["Die " + zone]
            if i < len(zones) - 1:
                exits.append("Exit " + zone)
            ctx.multiworld.regions += [
                create_region(ctx.multiworld, ctx.player, location_database, zone, locs, exits),
            ]

    # Dream's regions: variable count (dream_zone_list), no ENEMY_BY_ZONE/NPC_BOSS_BY_ZONE lookup
    # (its Enemy/Miniboss/Boss counter locations, and the boss "Met" checks only a dive can
    # send, already live directly in zone_tables[DREAM][zone] -- see fill_dream_checks). Every
    # location for a region already lives in its zone_tables entry, so locs is just that.
    for i, zone in enumerate(dream_zone_list):
        locs = [loc for loc in ctx.dream_zone_tables[zone]]
        exits = ["Die " + zone]
        if i < len(dream_zone_list) - 1:
            exits.append("Exit " + zone)
        ctx.multiworld.regions += [
            create_region(ctx.multiworld, ctx.player, location_database, zone, locs, exits),
        ]

    # The Crossroads hub holds the keepsake unlock checks (when keepsakesanity isn't
    # "normal"). Aspects and pets are items-only; incantations were removed.
    crossroads_locs = [boss_event("Zagreus")]
    if ctx.options.keepsakesanity.value != 0:
        crossroads_locs += [loc for loc in keepsake_locations_for(ctx.options)]
    if ctx.options.npc_locations:
        crossroads_locs += [loc for loc in npc_intro_locations_for(ctx.options)]
        crossroads_locs += [loc for loc in npc_meet_locations_for(ctx.options)]
        crossroads_locs += list(ALWAYS_MET_BOSS_LOCATIONS)
    if enemysanity_has_locations(ctx.options):
        # Enemy names Nightmare shares with the Underworld roster live here instead of their
        # normal zone (Crossroads is always immediately reachable) -- their real gating is
        # an access_rule checking whichever of their zones is reachable, set in Rules.py's
        # _set_shared_enemy_rules. Filtered to the ones actually in this seed's table (i.e.
        # Underworld active this seed -- see Locations.SHARED_ENEMY_ZONES). Shuffled ones are
        # already in a zone above (Locations.enemy_zone_placement), so they're skipped here.
        placed = {loc for names in (getattr(ctx, "enemy_zone_placement", None) or {}).values()
                  for loc in names}
        shared = filter_minibosses(SHARED_ENEMY_LOCATIONS, bool(ctx.options.include_minibosses))
        crossroads_locs += [loc for loc in shared if loc in location_database and loc not in placed]
        if ZAGREUS_DEFEATED_LOCATION in location_database:
            crossroads_locs.append(ZAGREUS_DEFEATED_LOCATION)
    if ctx.options.npc_locations and ZAGREUS_MET_LOCATION in location_database:
        crossroads_locs.append(ZAGREUS_MET_LOCATION)

    ctx.multiworld.regions += [
        create_region(ctx.multiworld, ctx.player, location_database, "Crossroads",
                      crossroads_locs, crossroads_exits),
    ]

    # combine_pools: a single shared room region, reached from the Menu (its per-check
    # reachability — depth's zone on either route, plus the weapon for per-weapon — is set
    # in Rules._set_combined_room_rules).
    if combined_rooms:
        combined_locs = list(combined_room_table(ctx.options, ctx.location_multiplier).keys())
        ctx.multiworld.regions += [
            create_region(ctx.multiworld, ctx.player, location_database, "Combined Rooms",
                          combined_locs, None),
        ]

    # combine_pools + point_based: the same shape for the shared score pool -- one region off
    # the Menu holding every route-agnostic "Score NNNN" check (per-check reachability is set
    # in Rules._set_combined_score_rules).
    if combined_score:
        ctx.multiworld.regions += [
            create_region(ctx.multiworld, ctx.player, location_database, "Combined Score",
                          list(combined_score_table(ctx.options).keys()), None),
        ]

    # --- Link everything up ---------------------------------------------------
    ctx.multiworld.get_entrance("Start", ctx.player).connect(
        ctx.multiworld.get_region("Crossroads", ctx.player))
    if combined_rooms:
        ctx.multiworld.get_entrance("To Combined Rooms", ctx.player).connect(
            ctx.multiworld.get_region("Combined Rooms", ctx.player))
    if combined_score:
        ctx.multiworld.get_entrance("To Combined Score", ctx.player).connect(
            ctx.multiworld.get_region("Combined Score", ctx.player))

    for route in routes:
        zones = dream_zone_list if route == DREAM else ROUTES[route]["zones"]
        ctx.multiworld.get_entrance("Descend " + route, ctx.player).connect(
            ctx.multiworld.get_region(zones[0], ctx.player))
        for i, zone in enumerate(zones):
            ctx.multiworld.get_entrance("Die " + zone, ctx.player).connect(
                ctx.multiworld.get_region("Crossroads", ctx.player))
            if i < len(zones) - 1:
                ctx.multiworld.get_entrance("Exit " + zone, ctx.player).connect(
                    ctx.multiworld.get_region(zones[i + 1], ctx.player))
