from .Routes import ROUTES, active_routes, boss_event


def create_regions(ctx, location_database: dict) -> None:
    from . import create_region
    from .Locations import zone_tables, keepsake_locations_for, ENEMY_BY_ZONE, \
        NPC_BOSS_BY_ZONE, npc_intro_locations_for, npc_meet_locations_for, \
        ALWAYS_MET_BOSS_LOCATIONS, combine_active, combined_room_table, \
        combined_score_table, ROOM_BASED, PER_WEAPON_ROOM_BASED, SHARED_ENEMY_LOCATIONS, \
        ZAGREUS_MET_LOCATION, ZAGREUS_DEFEATED_LOCATION

    routes = active_routes(ctx.options)
    combined_rooms = combine_active(ctx.options) \
        and ctx.options.location_system.value in (ROOM_BASED, PER_WEAPON_ROOM_BASED)
    combined_score = combine_active(ctx.options) \
        and ctx.options.location_system.value not in (ROOM_BASED, PER_WEAPON_ROOM_BASED)

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
        zones = ROUTES[route]["zones"]
        for i, zone in enumerate(zones):
            locs = [loc for loc in zone_tables[route][zone]]
            if ctx.options.enemy_locations:
                locs += ENEMY_BY_ZONE.get((route, zone), [])
            if ctx.options.npc_locations:
                locs += NPC_BOSS_BY_ZONE.get((route, zone), [])
            exits = ["Die " + zone]
            if i < len(zones) - 1:
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
    if ctx.options.enemy_locations:
        # Enemy names Nightmare shares with the Underworld roster live here instead of their
        # normal zone (Crossroads is always immediately reachable) -- their real gating is
        # an access_rule checking whichever of their zones is reachable, set in Rules.py's
        # _set_shared_enemy_rules. Filtered to the ones actually in this seed's table (i.e.
        # Underworld active this seed -- see Locations.SHARED_ENEMY_ZONES).
        crossroads_locs += [loc for loc in SHARED_ENEMY_LOCATIONS if loc in location_database]
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
        zones = ROUTES[route]["zones"]
        ctx.multiworld.get_entrance("Descend " + route, ctx.player).connect(
            ctx.multiworld.get_region(zones[0], ctx.player))
        for i, zone in enumerate(zones):
            ctx.multiworld.get_entrance("Die " + zone, ctx.player).connect(
                ctx.multiworld.get_region("Crossroads", ctx.player))
            if i < len(zones) - 1:
                ctx.multiworld.get_entrance("Exit " + zone, ctx.player).connect(
                    ctx.multiworld.get_region(zones[i + 1], ctx.player))
