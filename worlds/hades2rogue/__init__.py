import copy
import logging
import string

from BaseClasses import CollectionState, Entrance, Item, ItemClassification, MultiWorld, Region, \
    Tutorial
from .Items import item_table, item_table_weapons, \
    item_table_arcana, item_table_arcana_progressive, \
    item_table_keepsakes_randomized, item_table_keepsakes_progressive_per, \
    item_table_familiars_randomized, item_table_familiars_progressive_per, WEAPON_SHORT_NAMES, ASPECT_MAX_RANK, \
    INITIAL_WEAPON_BY_VALUE, ASPECT_BASE_TITLE_BY_WEAPON, included_aspect_alts, \
    KEEPSAKE_PROGRESSIVE_COUNT, FAMILIAR_PROGRESSIVE_COUNT, \
    incantation_always, incantation_underworld, incantation_surface, incantation_nightmare, \
    incantation_keepsake_nonprog, INCANTATION_SURFACE_ONLY_EXTRA, INCANTATION_RETIRED, \
    INCANTATION_NIGHTMARE_RETIRED, INCANTATION_AUTO_GRANTED, INCANTATION_COMBINED_AWAY, \
    combined_incantation_counts, \
    vow_names, event_item_pairs, Hades2Item, item_name_groups, \
    NPC_GIFT_ITEMS, godsanity_gods_for, GODSANITY_CHAOS, helper_story_npcs, \
    helper_story_npcs_nightmare, combat_helper_npcs, KEEPSAKE_NIGHTMARE_TITLES, \
    GOD_KEEPSAKE_TITLE
from .Routes import ROUTES, UNDERWORLD, SURFACE, NIGHTMARE, DREAM, goal_includes
from .Locations import setup_location_table_with_settings, give_all_locations_table, \
    Hades2Location, location_name_groups, POINT_BASED, MAX_LOCATION_MULTIPLIER, \
    combine_active, compute_enemysanity_shuffle_map, serialize_shuffle_map, \
    parse_shuffle_map, _repair_shuffle_map, enemy_zone_placement, compute_miniboss_room_map, \
    combined_relabel, DREAM_REGIONS_AVAILABLE_ZJ, \
    DREAM_REGIONS_AVAILABLE_NO_ZJ
from .Options import Hades2Options, hades2_option_groups, hades2_option_presets
from .Regions import create_regions
from .Rules import set_rules
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import Component, components, Type, launch_subprocess


def launch_client(*args):
    # A crash inside launch() itself is now logged + shown to the player (see
    # Client.py's own launch()) -- but that only covers the client module once it's
    # successfully imported. A failure in the import itself (e.g. a stale/mismatched
    # apworld release, or another installed world colliding with it) happens one step
    # earlier than that and would otherwise be just as invisible.
    try:
        from .Client import launch
    except Exception:
        import traceback
        traceback.print_exc()
        import Utils
        Utils.messagebox(
            "Hades 2 Rogue Client Error",
            "The Hades 2 Rogue Client failed to load, before it could even start.\n\n"
            "This usually means another installed world is conflicting with it, or "
            "the installed Hades2Rogue.apworld is out of date. Please report this.",
            error=True,
        )
        return
    # args = whatever the Launcher forwards: CLI args after `--`
    # (e.g. --connect host:port --name Slot), or an archipelago:// url.
    launch_subprocess(launch, "Hades2RogueClient", args)


# game_name + supports_uri: the Launcher offers a component for archipelago:// links
# whose ?game= matches its game_name.
components.append(Component("Hades 2 Rogue Client",
                            func=launch_client, component_type=Type.CLIENT,
                            game_name="Hades2Rogue", supports_uri=True))


class Hades2Web(WebWorld):
    display_name = "Hades 2 (Rogue)"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Hades 2 for MultiworldGG.",
        "English",
        "setup_en.md",
        "hades2/en",
        ["BrittisH39"]
    )]
    options_presets = hades2_option_presets
    option_groups = hades2_option_groups


class Hades2World(World):
    """
    Hades 2 is a rogue-like dungeon crawler in which the witch Melinoe battles
    through the Underworld to defeat the Titan of Time, Chronos.
    """

    options: Hades2Options
    options_dataclass = Hades2Options
    game = "Hades2Rogue"
    topology_present = False
    web = Hades2Web()
    required_client_version = (0, 6, 4)
    # Universal Tracker: skip its "cold" pre-connect generation (rolled from the local YAML,
    # which can pick different random values -- initial_weapon, starting_route, etc. -- than
    # the real seed) and regenerate straight from fill_slot_data on connect instead. Without
    # this, if that post-connect regen throws for any reason, UT silently keeps showing the
    # wrong cold-pass world forever with no error (e.g. reported: Underworld enemy checks
    # in logic despite Lock Routes on and zero Progressive Underworld -- the cold pass can
    # roll a starting_route/lock state that leaves Underworld open). Requires fill_slot_data
    # to carry every option that affects generation -- see its docstring below.
    ut_can_gen_without_yaml = True

    # Shipped in slot_data as version_check and compared against Client.py's MOD_VERSION on
    # connect. KEEP ALL THREE IN STEP ON EVERY RELEASE: this, Client.MOD_VERSION, and the
    # mod's manifest.json version_number -- and bump them on any breaking datapackage or
    # protocol change, or the mismatch warning can never fire (it sat at "0.1" for seven
    # releases, spanning a breaking keepsake-id relocation).
    mod_version = "0.10.0"

    item_name_to_id = {name: data.code for name, data in item_table.items() if data.code is not None}
    location_name_to_id = give_all_locations_table()

    item_name_groups = item_name_groups
    location_name_groups = location_name_groups

    def _normalize_weapon_options(self) -> None:
        """Reconcile included_weapons against initial_weapon/weapons_clears_needed, the same
        shape as _normalize_route_options does for routes/starting_route: a player-facing
        toggle can otherwise leave the seed internally contradictory (a starting weapon that
        was excluded, or a clears-needed higher than the weapon pool can ever satisfy)."""
        from Options import OptionError

        included = set(self.options.included_weapons.value)
        if not included:
            raise OptionError(
                "Hades 2 Rogue: no weapon is included (Included Weapons is empty) -- at "
                "least one weapon must be reachable.")

        # weapon_amount randomly downselects included_weapons to that many entries, writing
        # the result back so every downstream reader of included_weapons.value (item pool,
        # Rules.py's weapon-count gates, Client.py's tracker columns, slot_data) sees the
        # trimmed set automatically. A no-op once len(included) <= amount (also what keeps
        # this idempotent across UT's passthrough restore, which re-applies the already-
        # downselected included_weapons before this method runs again).
        amount = self.options.weapon_amount.value
        if amount < len(included):
            included = set(self.random.sample(sorted(included), amount))
            self.options.included_weapons.value = included

        # initial_weapon must be one of the included weapons; an excluded pick (or a
        # resolved "random" that landed on one) snaps to a random included weapon instead.
        starting_weapon = INITIAL_WEAPON_BY_VALUE.get(self.options.initial_weapon.value)
        if starting_weapon not in included:
            by_weapon = {w: v for v, w in INITIAL_WEAPON_BY_VALUE.items()}
            self.options.initial_weapon.value = by_weapon[self.random.choice(sorted(included))]

        # weapons_clears_needed can never exceed how many weapons actually exist this seed.
        self.options.weapons_clears_needed.value = min(
            self.options.weapons_clears_needed.value, len(included))

    def _normalize_route_options(self) -> None:
        """Reconcile route/goal/start settings that can otherwise contradict each other, so
        the seed generates coherently and slot_data tells the mod the truth.

        - starting_route must be a route the player actually included; an out-of-set choice
          (or a resolved "random"/"all") snaps to an included route. A goal-forced route is
          reachable but never the starting route -- it stays locked behind its unlock item.
        - vows only matter with reverse_vow on; otherwise they're zeroed (see below).
        - separate_checks / starting_route are rewritten to match what will actually
          generate, so the values shipped in slot_data don't lie to the mod.
        """
        from .Routes import active_routes
        from Options import OptionError

        # IncludeZagreusJourney off: Nightmare can't exist at all (it IS Zagreus' Journey's
        # content), so force it out of both sets before any of the validation/forcing logic
        # below runs -- otherwise a goal or Include Regions entry naming Nightmare would
        # silently keep it in play. Doing this first means the "no route"/"no goal" checks
        # just below see the truth and raise a clear error if stripping Nightmare left nothing.
        if not self.options.include_zagreus_journey:
            self.options.include_regions.value = set(self.options.include_regions.value) - {NIGHTMARE}
            self.options.goals_required.value = set(self.options.goals_required.value) - {NIGHTMARE}

        # Same for Zagreus on a seed whose only route is Dream: a Dream Dive never offers his
        # contract (Routes.zagreus_reachable), so he can't be part of that seed's goal. Left
        # on, "Beat Zagreus" -- and "Met Zagreus"/"Zagreus Defeated", which only exist while
        # he's in the goal -- could never be reached, and generation died in fill with "Game
        # appears as unbeatable". When he was the only goal, the goal becomes the one route
        # the seed does have. (No route at all is left alone: the check below reports it.)
        if self.options.goal_requires_zagreus and active_routes(self.options) == [DREAM]:
            self.options.goal_requires_zagreus.value = 0
            if not self.options.goals_required.value:
                self.options.goals_required.value = {DREAM}

        # A goal with NO boss selected can never be completed (the completion condition
        # checks the selected set) -- generation would otherwise die deep in fill with an
        # opaque "Game appears as unbeatable". Fail here with a clear message instead.
        if not self.options.goals_required.value and not self.options.goal_requires_zagreus:
            raise OptionError(
                "Hades 2 Rogue: no Goal is selected (Goals Required is empty and Goal "
                "Requires Zagreus is off) -- the goal can never be completed. Select at "
                "least one.")

        # Routes the player explicitly included (before the goal forces any in).
        included_set = set(self.options.include_regions.value)
        if not included_set and not active_routes(self.options):
            raise OptionError(
                "Hades 2 Rogue: no route is included (Include Regions is empty) and no "
                "Goals Required entry forces one in -- at least one route must be "
                "reachable. (Goal Requires Zagreus alone doesn't force one: he's reachable "
                "from any route, so include at least one.)")

        # sr option values: 0=random, 1=underworld, 2=surface, 3=all, 4=nightmare, 5=dream.
        sr_by_route = {UNDERWORLD: 1, SURFACE: 2, NIGHTMARE: 4, DREAM: 5}
        start_choices = [r for r in (UNDERWORLD, SURFACE, NIGHTMARE, DREAM) if r in included_set]
        if not start_choices:
            # Include Regions is empty but Goals Required forces a route in (e.g. only
            # "Surface" selected): the forced route is the only thing there is to start on.
            # Without this, the start_choices[0] fallbacks below IndexError.
            start_choices = list(active_routes(self.options))
        sr = self.options.starting_route.value
        route_of_sr = {v: k for k, v in sr_by_route.items()}
        if sr == 0:                                    # random -> among included routes
            sr = sr_by_route[self.random.choice(start_choices)]
        elif sr == 3:                                  # all -> valid only if 2+ included
            if len(included_set) < 2:
                sr = sr_by_route[start_choices[0]]
        elif route_of_sr.get(sr) not in included_set:
            sr = sr_by_route[start_choices[0]]
        self.options.starting_route.value = sr

        # Vows only matter with reverse_vow on (only then are the removal items that walk
        # them back created); zero them otherwise so the mod isn't told to apply vows that
        # can never be removed.
        if not self.options.reverse_vow:
            for vow in vow_names:
                getattr(self.options, "vow_" + vow.lower()).value = 0

        # Reconcile the stored values with what will actually generate (goal-forced routes
        # included). One active route => nothing to split, and the start is that route.
        active = active_routes(self.options)
        self.options.include_regions.value = set(active)
        if len(active) == 1:
            self.options.separate_checks.value = 0
            self.options.starting_route.value = sr_by_route[active[0]]

    def interpret_slot_data(self, slot_data: dict) -> dict:
        """Universal Tracker hook -- REQUIRED to make the re_gen_passthrough restore below fire.
        UT only sets multiworld.re_gen_passthrough for worlds that implement this method: it
        calls interpret_slot_data with the real seed's slot_data and, on a truthy return,
        stashes that dict in re_gen_passthrough and re-runs generation. Without it UT never
        populates re_gen_passthrough, so _apply_ut_passthrough finds nothing and every "random"
        option (initial_weapon, starting_route, ...) re-rolls -- e.g. initial_weapon can land on
        the Coat, making all Coat-gated per-weapon checks show as in-logic when you don't
        actually have the Coat. Return slot_data unchanged so the passthrough carries the real
        resolved values (see _apply_ut_passthrough)."""
        return slot_data

    def _apply_ut_passthrough(self) -> None:
        """Universal Tracker regenerates this world from the player's YAML in an isolated
        solo multiworld rather than replaying the real generation, so any option resolved
        from "random" (initial_weapon, starting_route, ...) can re-roll to a DIFFERENT value
        than the real seed used -- UT would then compute logic (e.g. which per-weapon rooms
        are reachable) against a weapon/route you don't actually have. UT sets
        multiworld.re_gen_passthrough = {game: <the real slot_data>} precisely so worlds can
        restore the actually-resolved values instead of re-rolling; do that for every option
        fill_slot_data sent (a plain attribute copy -- non-option slot_data keys like
        "seed"/"version_check"/the *_offset ints just fail the hasattr check and are skipped)."""
        passthrough = getattr(self.multiworld, "re_gen_passthrough", {}).get(self.game)
        self._ut_passthrough = passthrough
        if not passthrough:
            return
        for key, value in passthrough.items():
            option = getattr(self.options, key, None)
            if option is not None:
                # from_any(...).value (not a raw .value= assignment) so OptionSets (e.g.
                # starting_npc_gifts) round-trip correctly: slot_data survives JSON as a
                # list, but OptionSet.value must stay a set for downstream `in`/equality
                # checks against valid_keys members. from_any returns a whole new Option
                # instance, not the bare value, so it must be unwrapped here.
                option.value = option.from_any(value).value

    def _resolve_starting_aspect_index(self) -> int:
        """Which of the starting weapon's 4 Aspects is active at rank 1 (see
        _main_pool_item_names). Not an Option, so _apply_ut_passthrough can't restore it via
        attribute copy -- pull it from the passthrough directly instead of re-rolling, for the
        same reason (a re-rolled index can precollect a different Aspect item under
        aspectsanity=per_aspect than the real seed did, which is also a logic-affecting pick)."""
        if self._ut_passthrough and "starting_aspect_index" in self._ut_passthrough:
            return self._ut_passthrough["starting_aspect_index"]
        return self.random.randint(0, int(self.options.included_aspects) - 1)

    def _resolve_godsanity_gated_gods(self) -> list:
        """The gods GodSanity gates this seed, in pool order (Items.godsanity_gods_for). Chaos
        joined 9/30: a seed generated before that has no "Chaos Unlock" item, and its slot_data
        has no godsanity_chaos key. A Universal Tracker regen of such a seed must leave Chaos
        out -- otherwise "Met Chaos" waits forever on an item the real seed never placed, and
        the boss-tier god count (Rules._god_cap) could never reach 100% of 12."""
        legacy_seed = bool(self._ut_passthrough) and not self._ut_passthrough.get("godsanity_chaos")
        return godsanity_gods_for(include_chaos=not legacy_seed)

    def _resolve_dream_met_checks(self) -> bool:
        """Whether this seed counts a Dream Dive as somewhere NPCs are met (9/30): boss "Met"
        checks generated for Dream (Locations.dream_boss_met_locations_for), and Dream's final
        region counted in the randomized helpers' rule and required for Chaos when a dive is
        the only source of Chaos Gates (both Rules._set_keepsake_rules). False only
        on a Universal Tracker regen of a seed generated before that, whose slot_data never
        carried dream_met_checks -- there the old location table and rules are rebuilt, so the
        tracker counts what the seed was actually filled against (the extra locations would
        also shift generate_early's location auto-scaling off the real seed's)."""
        if self._ut_passthrough:
            return bool(self._ut_passthrough.get("dream_met_checks"))
        return True

    def generate_early(self) -> None:
        from .Routes import active_routes
        self._apply_ut_passthrough()
        self._normalize_weapon_options()
        self._normalize_route_options()
        self.godsanity_gated_gods = self._resolve_godsanity_gated_gods()
        self.dream_met_checks = self._resolve_dream_met_checks()
        # Every route's zones 2-4 are gated by its Progressive <Route> count (see below);
        # a non-starting route additionally needs one extra copy just to unlock its own
        # first zone (offset 1), so its full clear costs 4 total instead of 3. Surface/
        # Nightmare ALSO have their own in-fiction entry gate (Access item, or -- when
        # non-starting -- their first Progressive copy doubles as the door key per Test Run
        # 5 #14); that's a separate, additional mechanic layered on top of the same offset,
        # not a substitute for it -- so all three routes set their offset identically below.
        self.route_offsets = {UNDERWORLD: 0, SURFACE: 0, NIGHTMARE: 0, DREAM: 0}
        # Which routes this seed actually generates (include_* toggles + whatever the goal
        # forces in). Excluded routes get no regions, locations, items, or events.
        self.active_routes = active_routes(self.options)

        # Which route(s) start open (their Access item precollected / no Underworld offset),
        # driven by starting_route (0=random already resolved by _normalize_route_options,
        # 1=underworld, 2=surface, 3=all active routes, 4=nightmare) -- UNLESS lock_routes is
        # off, in which case starting_route doesn't apply at all (its own option text: "If
        # lock_routes is on, which route is open from the start") and every active route starts
        # open. Without this, a non-starting route's Access item (Surface/Nightmare/Dream) still
        # only got precollected when starting_route was literally "all", so lock_routes=false +
        # starting_route=underworld (the common case) left Surface/Nightmare/Dream's Access item
        # sitting in the shuffled pool same as with lock_routes on -- silently relocking a route
        # the option was supposed to leave fully open.
        sr = self.options.starting_route.value
        sr_route = {1: UNDERWORLD, 2: SURFACE, 4: NIGHTMARE, 5: DREAM}.get(sr)
        if not self.options.lock_routes or sr == 3:
            start_open = set(self.active_routes)
        elif sr_route in self.active_routes:
            start_open = {sr_route}
        else:
            # Shouldn't happen post-normalization, but fall back safely rather than start
            # with nothing open.
            start_open = {UNDERWORLD} if UNDERWORLD in self.active_routes \
                else set(self.active_routes[:1])

        self.surface_start = SURFACE in start_open
        self.nightmare_start = NIGHTMARE in start_open
        self.dream_start = DREAM in start_open

        # Enemy substitution permutation. Computed HERE, not in fill_slot_data, because logic
        # depends on it: the map is directional ("src: dst" = a spawn of src produces dst), so a
        # shuffled enemy is only killable where its PREIMAGE spawns, not where it natively lives.
        # Deriving each "X Defeated" location's zone from that (enemy_zone_placement below) is the
        # only way the rules describe reachable checks -- previously the map was rolled in
        # fill_slot_data, i.e. AFTER set_rules had already written zones from the native roster,
        # which left 36% of enemy checks gated looser than they really were (measured on a live
        # seed: 42 of 118 too loose, some by three zones -- a real BK risk whenever a progression
        # item landed on one). Scoped to active_routes so no check can be gated behind a route
        # this seed doesn't generate. fill_slot_data ships this same object, so the mod and the
        # rules are guaranteed to be describing one permutation rather than two.
        # Under Universal Tracker, restore the real seed's permutation instead of rolling a new
        # one -- same problem and same fix as starting_aspect_index above: it isn't an Option, so
        # _apply_ut_passthrough's attribute copy skips it. Rolling fresh here would have UT
        # tracking enemy checks in zones the actual seed never put them in.
        if self._ut_passthrough and self._ut_passthrough.get("enemysanity_shuffle_map"):
            # Repaired the same way the mod repairs it (EnemySanity.induced_map), so an older
            # seed whose map still routes through a name held out since is tracked the way it
            # actually plays. A no-op on maps generated by this version.
            self.enemysanity_shuffle_map = _repair_shuffle_map(parse_shuffle_map(
                self._ut_passthrough["enemysanity_shuffle_map"]))
        else:
            self.enemysanity_shuffle_map = compute_enemysanity_shuffle_map(
                self.options, self.random, self.active_routes)

        # Miniboss ROOM shuffle (2026-08-16 ruling -- minibosses no longer shuffle as enemies).
        # "host: dest" = the run's `host` miniboss-room slot loads `dest`'s room, so dest's
        # miniboss becomes killable at host's zone. Same generate_early/UT-passthrough discipline
        # as the enemy map, and for the same reason: logic is derived from it.
        if self._ut_passthrough and self._ut_passthrough.get("miniboss_room_map"):
            self.miniboss_room_map = parse_shuffle_map(
                self._ut_passthrough["miniboss_room_map"])
        else:
            self.miniboss_room_map = compute_miniboss_room_map(
                self.options, self.random, self.active_routes)

        self.enemy_zone_placement = enemy_zone_placement(
            combined_relabel(self.enemysanity_shuffle_map, self.miniboss_room_map),
            self.active_routes)
        # A non-starting route stays locked from its FIRST zone too (not just zones 2-4): it
        # needs one extra Progressive <Route> just to unlock zone 1, so its full clear costs 4
        # total copies instead of 3. Applies uniformly to all three routes when locked and not
        # started open -- Rules.py already scales every zone gate by this offset, and
        # create_items adds the matching extra Progressive <Route> so zone 4 stays reachable.
        if self.options.lock_routes:
            for route in self.active_routes:
                if route not in start_open:
                    self.route_offsets[route] = 1

        # When routes are locked and Surface/Nightmare is a non-starting route, its door is
        # instead opened by the first Progressive <Route> item (the mod grants the
        # unlock-flag on it), so there is no separate Access item needed -- "Descend <Route>"
        # then needs 1 Progressive <Route> instead (Test Run 5 #14, extended to Nightmare).
        self.surface_access_via_progressive = (
            SURFACE in self.active_routes
            and bool(self.options.lock_routes)
            and not self.surface_start
        )
        self.nightmare_access_via_progressive = (
            NIGHTMARE in self.active_routes
            and bool(self.options.lock_routes)
            and not self.nightmare_start
        )
        self.dream_access_via_progressive = (
            DREAM in self.active_routes
            and bool(self.options.lock_routes)
            and not self.dream_start
        )

        # --- Auto-scale locations so every item fits with ~40 filler to spare ----------
        # point_based bumps score_rewards_amount (each added score check is one location);
        # the room systems grow a multiplier so each room depth grants more checks. Both
        # are capped (score ids per route, MAX_LOCATION_MULTIPLIER); if a seed is still too
        # full after the cap, create_items logs a warning and Archipelago drops the excess.
        self.location_multiplier = 1
        # _main_pool_item_names reads zone_tables[DREAM] (lock_routes' Progressive Dream
        # count) -- normally populated by create_items calling setup_location_table_with_
        # settings first, but that hasn't run yet here, so prime it ourselves or a Dream
        # seed crashes with KeyError('Dream') the first time this runs.
        from .Locations import setup_location_table_with_settings
        setup_location_table_with_settings(self.options, 1, self.dream_met_checks)
        # Rolled once, here: _main_pool_item_names runs again in create_items and must see the
        # same pick (it used to re-roll on every call).
        self.starting_aspect_index = self._resolve_starting_aspect_index() \
            if self.options.aspectsanity.value in (1, 3) else 0
        pool_names, _precollect, prog_names = self._main_pool_item_names()
        # Items promoted to progression for THIS seed (Grasp, Arcana, Keepsakes, Vow Removals,
        # combined Aspects...). create_item applies it, so start_inventory(_from_pool) and
        # Universal Tracker, which both build items through create_item, count them in logic.
        self._progression_items = frozenset(prog_names)
        target = len(pool_names) + 40
        if self.options.location_system.value == POINT_BASED:
            deficit = target - self._fillable_count()
            if deficit > 0:
                n = len(self.active_routes)
                # split_pools gives EACH route `score` checks, so +1 to the option adds n
                # locations (raise by ceil(deficit/n)); combine_pools has one shared pool of
                # `score` checks total, so +1 adds exactly 1 (raise by deficit).
                add = deficit if combine_active(self.options) else -(-deficit // n)
                self.options.score_rewards_amount.value = min(
                    1000, self.options.score_rewards_amount.value + add)
        else:
            m = 1
            while m < MAX_LOCATION_MULTIPLIER and self._fillable_count(m) < target:
                m += 1
            self.location_multiplier = m

    def _fillable_count(self, multiplier: int = 1) -> int:
        """How many real (non-event) locations this seed generates at the given room
        multiplier -- i.e. how many items (filler included) it can hold."""
        table = setup_location_table_with_settings(self.options, multiplier, self.dream_met_checks)
        events = sum(1 for name in table if name in event_item_pairs)
        return len(table) - events

    def _main_pool_item_names(self):
        """The non-filler itempool as (pool_names, precollect_names, prog_names): names that
        go into the itempool, names to pre-collect, and which pool names must be progression.
        Pure (no multiworld side effects) so generate_early can size locations against the
        item count and create_items can build the real items. Keep in sync with create_items.

        Items that gate logic (Rules.py) must be progression, or Archipelago's reachability
        sweep (which only collects progression items) can never satisfy those gates -- so
        Grasp, Arcana and Keepsakes are promoted while their sanity is active."""
        pool, precollect, prog = [], [], set()

        asp = self.options.aspectsanity.value

        # Weapon/Aspect combine: whether Aspect items also carry weapon unlocks this seed.
        # progressive (asp==2): fuses into a single "Progressive <Weapon>" item (unchanged).
        # randomized (asp==1): keeps the normal per-aspect items, but the first one you get
        # for a weapon also unlocks it (Rules._hades2_has_weapon / ItemManager.unlock_aspect).
        # per_aspect (asp==3): same cascade.
        # unlocked (asp==0): nothing to combine, so this never applies.
        combine_on = asp in (1, 2, 3)

        # Non-starting weapons (always shuffled). When combine_on, the Aspect items above
        # carry the weapon unlocks instead, so the standalone unlock items are skipped.
        if not combine_on:
            for name in item_table_weapons:
                if not self.should_ignore_weapon(name):
                    pool.append(name)

        # Grasp: grasp_count Progressive Grasp; gates later bosses/areas.
        if int(self.options.grasp_intervals) > 0:
            prog.add("Progressive Grasp")
            pool += ["Progressive Grasp"] * int(self.options.grasp_count)

        # Arcana (arcanasanity): one "<Card> Arcana" each (Arcana), or 3 "Progressive
        # <Card> Arcana" each (Progressive_Arcana). Gates bosses/areas + deep score checks.
        if self.options.arcanasanity == 1:
            for name in item_table_arcana:
                prog.add(name)
                pool.append(name)
        elif self.options.arcanasanity == 2:
            for name in item_table_arcana_progressive:
                prog.add(name)
                pool += [name] * 3

        # Aspects (aspectsanity): 1 = randomized, 2 = progressive (per weapon),
        # 3 = per_aspect (per individual aspect), 0 = none.
        # starting_aspect_index: which of the starting weapon's 4 Aspects (0 = default
        # Aspect of Melinoe, 1-3 = its alternates in Items.ASPECT_TITLES_BY_WEAPON order) is
        # already active at the start of the run, instead of always Melinoe's. Only rolled
        # for randomized/per_aspect -- progressive and unlocked don't have a "starting pick"
        # concept (progressive always starts on Melinoe's; unlocked has everything already).
        # Sent to the mod as slot_data so it can seed the pick at rank 1 and force-equip it
        # (see ItemManager.lua apply_starting_aspect). Rolled once in generate_early.
        starting_weapon = INITIAL_WEAPON_BY_VALUE.get(self.options.initial_weapon.value)
        included_weapons = self.options.included_weapons.value
        included_aspects = int(self.options.included_aspects)
        if asp == 1:
            # randomized: an Aspect item per accessible Aspect -- the default Aspect of
            # Melinoe plus included_aspects-1 alternates (Items.included_aspect_alts), for
            # each weapon in included_weapons only. Excluded weapons/aspects simply never
            # get an item, so they can never unlock (see ItemManager.apply_aspect_base_lock/
            # the Nocturnal Arms shop block -- the mod is entirely item-gated already).
            # Receiving any of them grants that Aspect at MAX rank. combine_on doesn't change
            # the pool, only what receiving one does -- see Rules.py / ItemManager.unlock_aspect.
            # When combined they gate weapon access, so they must be progression; otherwise
            # they're just useful.
            # NOTHING is precollected: the starting weapon's random Aspect pick starts at rank 1
            # only (seeded in-game by the mod from starting_aspect_index), so its item stays in
            # the pool as the way to level that Aspect the rest of the way to max.
            for weapon in WEAPON_SHORT_NAMES:
                if weapon not in included_weapons:
                    continue
                names = [ASPECT_BASE_TITLE_BY_WEAPON[weapon]] + included_aspect_alts(weapon, included_aspects)
                for name in names:
                    if combine_on:
                        prog.add(name)
                    pool.append(name)
        elif asp == 2:
            # progressive: fuses into "Progressive <Weapon>" when combined (1st copy unlocks
            # the weapon + all Aspects, later copies rank them up); otherwise the weapon
            # unlock is separate and "Progressive <Weapon> Aspect" only handles Aspects.
            # included_aspects doesn't change the copy count here (every copy ranks the whole
            # weapon); the mod applies it by only unlocking the included Aspects
            # (ItemManager.included_alt_ids).
            weapon_name = "Progressive {}" if combine_on else "Progressive {} Aspect"
            for weapon in WEAPON_SHORT_NAMES:
                if weapon not in included_weapons:
                    continue
                pool += [weapon_name.format(weapon)] * ASPECT_MAX_RANK
        elif asp == 3:
            # Every accessible Aspect of an included weapon (default "Aspect of Melinoe" +
            # included_aspects-1 alternates) gets its own 5-copy progressive line, always
            # (combine_on doesn't change the item pool here either). When combined, the first
            # copy of any of them unlocks the weapon (Rules._hades2_has_weapon); otherwise a
            # separate weapon-unlock item is needed instead (added above). One of your starting
            # weapon's accessible Aspects is already active in-game at rank 1 (a random pick,
            # not always the default Aspect of Melinoe), so its first copy is pre-collected
            # instead of placed in the pool.
            for weapon in WEAPON_SHORT_NAMES:
                if weapon not in included_weapons:
                    continue
                names = [f"Progressive {weapon} Base Aspect"] + \
                    [f"Progressive {title}" for title in included_aspect_alts(weapon, included_aspects)]
                for i, name in enumerate(names):
                    copies = [name] * ASPECT_MAX_RANK
                    if weapon == starting_weapon and i == self.starting_aspect_index:
                        precollect.append(copies.pop(0))
                    pool += copies

        # Keepsakes (keepsakesanity): 1 = randomized (one per keepsake), 2 = progressive
        # (3 Progressive Keepsake), 0 = normal. Keepsake count gates the unlock checks.
        # The 7 Nightmare keepsakes rejoin the pool on EVERY seed (July 18, reverting the
        # July 16 audit-B6 route filter): Zagreus' Journey + SharedKeepsakePort are hard
        # dependencies of the game mod now, so the H1 keepsakes are equippable regardless
        # of the seed's routes -- and the randomized helpers mean Sisyphus/Eurydice/
        # Patroclus/Thanatos can be MET and GIFTED on any route, so their gift locations
        # exist on every seed too (Routes.NPC_RANDOMIZED_HELPERS). Keeping all 40 titles in
        # the pool also keeps the keepsake-count tier denominator (Rules._keepsake_pool_size)
        # honest on every seed. EXCEPTION: IncludeZagreusJourney off drops the 7 Nightmare
        # titles regardless -- without ZJ they're not equippable at all (see
        # Rules._keepsake_pool_size, which shrinks the denominator to match).
        zj_on = bool(self.options.include_zagreus_journey)
        keep = self.options.keepsakesanity.value
        # Combined God Unlock + Keepsake: when both KeepsakeSanity=randomized and GodSanity
        # are active, the GodSanity gods' own "<God> Unlock" item and keepsake item fuse
        # into a single "<God> Unlock + Keepsake" item (see Items.GOD_KEEPSAKE_TITLE) --
        # receiving it unlocks that god's boons AND makes their keepsake giftable at once,
        # instead of needing both items separately. Computed here (before both blocks below)
        # so the keepsake loop can skip the fused titles and the godsanity block can add
        # the combined items instead of the plain "<God> Unlock" ones.
        combine_god_keepsake = keep == 1 and self.options.godsanity.value != 0
        fused_titles = {GOD_KEEPSAKE_TITLE[god] for god in self.godsanity_gated_gods}
        if keep == 1:
            for name in item_table_keepsakes_randomized:
                if not zj_on and name in KEEPSAKE_NIGHTMARE_TITLES:
                    continue
                if combine_god_keepsake and name in fused_titles:
                    continue
                prog.add(name)
                pool.append(name)
        elif keep == 2:
            prog.add("Progressive Keepsake")
            pool += ["Progressive Keepsake"] * KEEPSAKE_PROGRESSIVE_COUNT
        elif keep == 3:
            # progressive_per: each keepsake gets its own "Progressive <Title>" copies
            # instead of sharing one pool -- same zj_on filter as mode 1's loop above (the 7
            # Nightmare titles only exist when Zagreus' Journey is in play this seed).
            for name in item_table_keepsakes_progressive_per:
                title = name[len("Progressive "):]
                if not zj_on and title in KEEPSAKE_NIGHTMARE_TITLES:
                    continue
                prog.add(name)
                pool += [name] * KEEPSAKE_PROGRESSIVE_COUNT

        # Familiars (petsanity): 1 = randomized, 2 = progressive, 3 = progressive_per,
        # 0 = unlocked (no items).
        pet = self.options.petsanity.value
        if pet == 1:
            pool += list(item_table_familiars_randomized)
        elif pet == 2:
            pool += ["Progressive Familiar"] * FAMILIAR_PROGRESSIVE_COUNT
        elif pet == 3:
            # progressive_per: each familiar gets its own "Progressive <Name>" copies instead
            # of sharing one pool. Not progression (mirrors mode 2 -- items-only, no location
            # depends on them).
            for name in item_table_familiars_progressive_per:
                pool += [name] * FAMILIAR_PROGRESSIVE_COUNT

        # Boon gods (godsanity): any value other than "unlocked" (0) locks each of the 9
        # boon gods behind its own "<God> Unlock" item -- progression, since Rules.py gates
        # that god's "Met"/"Keepsake" locations on holding it (see Items.item_table_gods).
        # Hermes/Selene and Chaos ride the same list: same item shape and pool condition, gated
        # in Lua via an existence-only check instead (see Items.godsanity_shop_gods /
        # GODSANITY_CHAOS).
        if self.options.godsanity.value != 0 and combine_god_keepsake:
            # KeepsakeSanity=randomized too: fused items replace both halves for every gated
            # god (see Items.GOD_KEEPSAKE_COMBINED_GODS / GOD_KEEPSAKE_TITLE above).
            for god in self.godsanity_gated_gods:
                name = f"{god} Unlock + Keepsake"
                prog.add(name)
                pool.append(name)
        elif self.options.godsanity.value != 0:
            pool += [f"{god} Unlock" for god in self.godsanity_gated_gods]

        # Helper Room Sanity: "items"/"items_random" (1/3) locks each story-room helper NPC
        # behind its own "<NPC> Room" item -- progression, since Rules.py gates that NPC's
        # "Met"/"Keepsake" locations on holding it (see Items.item_table_helper_npcs). The 3
        # Nightmare-cast helpers (Sisyphus/Eurydice/Patroclus) join the pool whenever
        # IncludeZagreusJourney is on, NOT just when Nightmare is an active route (July 22 fix):
        # zerp-NPCRoomRandomizer can swap their identity into any OTHER active route's story
        # slot too (Routes.NPC_RANDOMIZED_HELPERS), so gating their item on Nightmare being
        # selected left a real seed shape -- ZJ on, Nightmare off -- where their "Met"/"Keepsake"
        # locations existed (Locations._route_locked_out never dropped them) but could never
        # actually be unlocked, since the item that gates them never entered the pool.
        hrs = self.options.helper_room_sanity.value
        if hrs in (1, 3):
            names = helper_story_npcs + (helper_story_npcs_nightmare if zj_on else [])
            pool += [f"{npc} Room" for npc in names]

        # Combat Helper Sanity: "items"/"items_random" (1/3) locks each combat-assist NPC
        # behind its own "<NPC> Helper" item -- progression, since Rules.py gates that NPC's
        # "Met"/"Keepsake" locations on holding it (all but Nemesis, who's always reachable
        # at the Crossroads -- see Items.combat_helper_npcs). Unlike helper_room_sanity's
        # Nightmare-only trio, Thanatos otherwise joins the pool unconditionally: he already
        # spawns in base Underworld/Surface zones too (zerp-Extended_NPC_Encounters), not just
        # Nightmare -- but that spawn still calls through Zagreus' Journey's own
        # HandleThanatosSpawn (reload.lua), so IncludeZagreusJourney off drops his item too.
        chs = self.options.combat_helper_sanity.value
        if chs in (1, 3):
            pool += [f"{npc} Helper" for npc in combat_helper_npcs if zj_on or npc != "Thanatos"]

        # Daedalus Upgrades (run-start Hammer) and NPC Gifts (run-start trait, one item per
        # NPC selected in starting_npc_gifts -- see Items.NPC_GIFT_ITEMS). Walked in
        # NPC_GIFT_ITEMS' fixed order, not the option's: that value is a set, whose order
        # changes from one Python process to the next, and the itempool's order has to be the
        # same every time the same seed is generated.
        pool += ["Daedalus Upgrade"] * int(self.options.daedalus_upgrade)
        for npc, gift in NPC_GIFT_ITEMS.items():
            if npc in self.options.starting_npc_gifts.value:
                pool.append(gift)

        # Progressive Boon Level: each raises the base level of every acquired leveled boon.
        pool += ["Progressive Boon Level"] * int(self.options.progressive_boon_level)

        # Zagreus Weaken (Empowered mode only, and only when Zagreus is part of the goal):
        # one Progressive Zagreus Weaken per configured tier. Statically progression already
        # (Items.item_table_extras) -- Rules._set_victory_rules gates both the Zagreus goal
        # event and Zagreus Defeated on holding a share of these, so it does gate location
        # reachability; no prog.add needed here since Items.py already marks it True.
        if goal_includes(self.options, "zagreus") and self.options.zagreus_encounter_mode.value == 1:
            pool += ["Progressive Zagreus Weaken"] * int(self.options.zagreus_weaken_tiers)

        # Vow removal items (reverse_vow): one per starting level. These gate the vow-weight
        # share of _tier_requirement_met (Rules._hades2_vow_weight_state), the same boss-tier
        # check grasp/arcana/progressive-weapon/god items feed into -- so, like those, they
        # must be progression or AP's progression-only reachability sweep can never see any
        # vow weight as "removed", permanently failing that check whenever vow is an active
        # pool (found while auditing why stricter logic kept failing generation).
        if self.options.reverse_vow:
            for vow in vow_names:
                levels = int(getattr(self.options, "vow_" + vow.lower()))
                if levels > 0:
                    prog.add(f"{vow} Vow Removal")
                    pool += [f"{vow} Vow Removal"] * levels

        # Surface unlocks (open the door + remove the lethal penalty), only when the Surface
        # is in this seed. Surface Access is pre-collected on a surface start (and skipped
        # entirely when the first Progressive Surface opens the door instead); the Penalty
        # Cure is always pre-collected, regardless of starting route.
        if SURFACE in self.active_routes:
            precollect.append("Surface Penalty Cure")
            if not self.surface_access_via_progressive:
                (precollect if self.surface_start else pool).append("Surface Access")

        # Nightmare Access opens the Crossroads Chaos Gate, only when Nightmare is in this seed.
        # Precollected on a Nightmare start (and skipped entirely when the first Progressive
        # Nightmare opens the gate instead, same shape as Surface Access above). No penalty-
        # cure equivalent -- the mod has no early-game damage curse to counter.
        if NIGHTMARE in self.active_routes and not self.nightmare_access_via_progressive:
            (precollect if self.nightmare_start else pool).append("Nightmare Access")

        # Dream Access mirrors Surface/Nightmare's own Access item shape (see Routes.DREAM's
        # definition comment for why Dream otherwise skips ROUTES-driven code paths).
        if DREAM in self.active_routes and not self.dream_access_via_progressive:
            (precollect if self.dream_start else pool).append("Dream Access")

        # Incantation items (Cauldron unlocks, shuffled): always-on set, plus route- and
        # keepsake-gated sets. Each grants its world-upgrade in-game; no check locations.
        # A Dream Dive deals the real Underworld and Surface biomes into its regions, so for
        # incantations Dream counts as both (mirrored by the mod's incantation_route_active).
        dream_on = DREAM in self.active_routes
        underworld_on = UNDERWORLD in self.active_routes or dream_on
        surface_on = SURFACE in self.active_routes or dream_on
        nightmare_on = NIGHTMARE in self.active_routes
        incantations = list(incantation_always)
        if underworld_on:
            incantations += incantation_underworld
        if surface_on:
            incantations += incantation_surface
            # Exhumed Troves normally rides with the underworld set; add it for surface-only.
            if not underworld_on:
                incantations.append(INCANTATION_SURFACE_ONLY_EXTRA)
        if nightmare_on:
            incantations += incantation_nightmare
        # Quickening of Sentimental Value (doubles keepsake leveling) only when keepsakes
        # aren't progressive/progressive_per (both control leveling via their own items).
        if self.options.keepsakesanity.value not in (2, 3):
            incantations += incantation_keepsake_nonprog
        incantations = [name for name in incantations
                        if name not in INCANTATION_RETIRED
                        and name not in INCANTATION_NIGHTMARE_RETIRED
                        and name not in INCANTATION_AUTO_GRANTED
                        and name not in INCANTATION_COMBINED_AWAY]
        pool += incantations
        # The 7 combined incantations (July 19 simplification pass): a single item each that
        # unlocks everything its constituent route/tier-scoped names (filtered out above) used
        # to unlock separately, in one shot. combined_incantation_counts() is a 0/1 presence
        # check per seed, not a copy count -- see its docstring.
        for combined_name, present in combined_incantation_counts(underworld_on, surface_on, nightmare_on).items():
            if present:
                pool.append(combined_name)

        # Route-unlock progressives (lock_routes): 3 per active route gate zones 2-4, plus
        # one extra per unit of a route's lock offset (see generate_early). Dream generalizes
        # the hardcoded 3 (= len(zones)-1 for every other route's fixed 4 zones) to n-1, where
        # n is THIS seed's actual (already-clamped) Dream region count. Computed the same way
        # Locations.fill_dream_checks derives it (NOT read from zone_tables[DREAM] -- this can
        # run during generate_early, before setup_location_table_with_settings has populated
        # it for the first time, so depending on that table here is a KeyError waiting to
        # happen).
        if self.options.lock_routes:
            for route in self.active_routes:
                if route == DREAM:
                    regions_available = DREAM_REGIONS_AVAILABLE_ZJ if NIGHTMARE in self.active_routes \
                        else DREAM_REGIONS_AVAILABLE_NO_ZJ
                    dream_n = min(int(self.options.dream_region_count.value), regions_available)
                    pool += ["Progressive Dream"] * ((dream_n - 1) + self.route_offsets[DREAM])
                else:
                    pool += [ROUTES[route]["progressive"]] * (3 + self.route_offsets[route])

        return pool, precollect, prog

    def create_items(self) -> None:
        local_location_table = setup_location_table_with_settings(
            self.options, self.location_multiplier, self.dream_met_checks).copy()

        pool_names, precollect_names, prog_names = self._main_pool_item_names()
        self._progression_items = frozenset(prog_names)
        pool = [self.create_item(name) for name in pool_names]
        for name in precollect_names:
            self.multiworld.push_precollected(self.create_item(name))

        # --- Lock boss-victory event items onto their event locations (active routes) ---
        active_event_pairs = {
            event: item for event, item in event_item_pairs.items()
            if event in local_location_table
        }
        for event, item in active_event_pairs.items():
            event_item = Hades2Item(item, self.player)
            self.multiworld.get_location(event, self.player).place_locked_item(event_item)

        # --- Fill the rest with filler currencies by configured proportions ---
        # The boss events are placed above and are not real, fillable locations.
        fillable = len(local_location_table) - len(active_event_pairs)
        excess = len(pool) - fillable
        if excess > 0:
            # The location auto-scaler (generate_early) hit its cap and the seed still has more
            # items than locations. The two counts have to match exactly, so the excess is cut
            # here rather than handed to Archipelago to leave unplaced: only items that gate
            # nothing can go, picked with the seed's own random so the same seed always loses
            # the same ones. If progression alone doesn't fit there is nothing left to cut.
            droppable = [i for i, item in enumerate(pool) if not item.advancement]
            if excess > len(droppable):
                from Options import OptionError
                raise OptionError(
                    f"Hades 2 Rogue ({self.player_name}): {len(pool) - len(droppable)} progression "
                    f"items but only {fillable} locations to hold them. Raise score_rewards_amount "
                    "(point_based), use a location system or route selection with more checks, "
                    "or turn off some sanities.")
            logging.warning(
                "Hades 2 (player %s): %d non-filler items but only %d fillable locations - "
                "Archipelago will drop %d of them. Raise score_rewards_amount (point_based), "
                "use a location system with more checks, or turn off some sanities, to keep every item.",
                self.player_name, len(pool), fillable, excess)
            dropped = set(self.random.sample(droppable, excess))
            pool = [item for i, item in enumerate(pool) if i not in dropped]
        total_fillers_needed = fillable - len(pool)
        if total_fillers_needed > 0:
            pool += self.build_filler_pool(total_fillers_needed)

        self.multiworld.itempool += pool

    # Absorber preference order for the filler rounding remainder (see _filler_absorber).
    FILLER_ABSORBER_ORDER = ("Nectar", "Starting Max Health", "Starting Gold", "Rarity Increase",
                             "Increased Odds of Major Finds", "Starting Max Magick", "Starting Armor")

    def _filler_percentages(self) -> dict:
        return {
            "Nectar": int(self.options.nectar_pack_percentage),
            "Starting Max Health": int(self.options.starting_health_percentage),
            "Starting Max Magick": int(self.options.starting_magick_percentage),
            "Starting Gold": int(self.options.starting_gold_percentage),
            "Starting Armor": int(self.options.starting_armor_percentage),
            "Rarity Increase": int(self.options.rarity_increase_percentage),
            "Increased Odds of Major Finds": int(self.options.major_finds_percentage),
        }

    def _filler_absorber(self, percentages: dict) -> str:
        """The filler that soaks up the rounding remainder: the first one in
        FILLER_ABSORBER_ORDER the player gave a nonzero share. (It used to be Nectar
        unconditionally, so a YAML with Nectar at 0% still got Nectar.)"""
        return next((n for n in self.FILLER_ABSORBER_ORDER if percentages.get(n, 0) > 0), "Nectar")

    def build_filler_pool(self, amount: int) -> list:
        percentages = self._filler_percentages()
        absorber = self._filler_absorber(percentages)
        total_percentage = sum(percentages.values())
        if total_percentage == 0:
            percentages[absorber] = 1
            total_percentage = 1

        filler = []
        allocated = 0
        names = [n for n in percentages if n != absorber]
        for name in names:
            count = int(amount * percentages[name] / total_percentage)
            for _ in range(count):
                filler.append(Hades2Item(name, self.player))
            allocated += count
        for _ in range(amount - allocated):
            filler.append(Hades2Item(absorber, self.player))
        return filler

    # Fewer open checks than this at the very start and the fill tends to bury the few of them
    # under unrelated items (measured 10/1 on random solo seeds: every such failure started
    # with under 15).
    START_CHECKS_MIN = 15
    # This many open at the start and the seed is left alone without looking any further (same
    # measurement: 2,240 seeds that started with 20+, none failed).
    START_CHECKS_PLENTY = 20
    # Hard cap on how much reachability checking the walk below may do, counted in location
    # checks rather than seconds so the same seed always stops at the same point.
    START_SIM_BUDGET = 500_000

    def pre_fill(self) -> None:
        self._grant_starting_items()

    def _grant_starting_items(self) -> None:
        """Hand out free starting items (user ruling 10/1) when the seed has too few open checks
        to hold the items it takes to open more -- e.g. per_aspect_room_based with npc_locations
        and keepsakesanity off, where nothing at all is reachable until an Aspect item turns up,
        or a Dream start whose first gate wants a dozen items with five checks open. A solo seed
        like that can't be filled ("No more spots to place N items").

        Walks the seed the way a player would: find the smallest set of items that opens a new
        check, then "find" it in the checks already open. Two things make items free instead
        (precollected, replaced in the pool by filler so the item and location counts still
        match): fewer than START_CHECKS_MIN checks open at the start, and a set bigger than the
        open checks can be trusted to hold (spare). Stops once the spare checks outnumber the
        progression items left -- nothing can run short after that.

        Solo seeds only, and only ones that start with fewer than START_CHECKS_PLENTY open
        checks (user ruling 10/1: a normal seed, and any real multiworld, must not be touched
        or slowed down). Runs in pre_fill so start_inventory_from_pool and plando have already
        been applied."""
        mw, player = self.multiworld, self.player
        if mw.players > 1:
            return      # other players' checks can hold the early items; nothing is given away
        if hasattr(mw, "generation_is_fake"):
            return      # Universal Tracker: it tracks with the items the server sends, free ones included
        pending = [loc for loc in mw.get_locations(player) if loc.item is None]   # not open yet
        filled = [loc for loc in mw.get_locations(player) if loc.item is not None]
        state = CollectionState(mw)
        opened = 0
        work = 0        # location checks spent, against START_SIM_BUDGET

        def opens(items) -> bool:
            nonlocal work
            work += len(pending)
            trial = state.copy()
            for item in items:
                trial.collect(item, True)
            trial.sweep_for_advancements(filled)
            return any(loc.can_reach(trial) for loc in pending)

        def explore() -> None:
            nonlocal opened
            state.sweep_for_advancements(filled)
            still_shut = [loc for loc in pending if not loc.can_reach(state)]
            opened += len(pending) - len(still_shut)
            pending[:] = still_shut

        def spare() -> float:
            # Only half the unclaimed open checks: the fill puts whatever it likes in the rest.
            return (opened - used) / 2

        explore()
        if opened >= self.START_CHECKS_PLENTY:
            return      # the usual case: one reachability pass and done
        remaining = [item for item in mw.itempool if item.player == player and item.advancement]
        used = 0        # open checks already spoken for by the items found so far
        granted = []
        while remaining and pending and spare() < len(remaining) and work < self.START_SIM_BUDGET:
            by_name = {}
            for item in remaining:
                by_name.setdefault(item.name, []).append(item)
            unlock = [copies[0] for copies in by_name.values() if opens(copies[:1])]
            if unlock:
                # Items that each open something on their own are found one after another; one
                # is free only while the start is still too small or there's nowhere to find it.
                short = 0
                if opened < self.START_CHECKS_MIN or spare() < 1:
                    unlock, short = unlock[:1], 1
            else:
                # No single item opens anything: take one copy of every item, then two, ... until
                # something does, then put back each one that turns out not to be needed.
                depth = 1
                while True:
                    unlock = [item for copies in by_name.values() for item in copies[:depth]]
                    if opens(unlock) or len(unlock) == len(remaining):
                        break
                    depth += 1
                if not opens(unlock):
                    break       # nothing left can open anything more
                for i in range(len(unlock) - 1, -1, -1):
                    if work >= self.START_SIM_BUDGET:
                        break
                    trial = unlock[:i] + unlock[i + 1:]
                    if trial and opens(trial):
                        unlock = trial
                if work >= self.START_SIM_BUDGET:
                    break       # not trimmed down to what's really needed: don't give it away
                short = len(unlock) if opened < self.START_CHECKS_MIN \
                    else min(len(unlock), max(0, len(unlock) - int(spare())))
            granted += unlock[:short]
            used += len(unlock) - short
            for item in unlock:
                state.collect(item, True)
                remaining.remove(item)
            explore()

        if not granted:
            return
        for item in granted:
            mw.itempool.remove(item)
            mw.push_precollected(item)
        mw.itempool += self.build_filler_pool(len(granted))
        logging.info("Hades 2 (player %s): %d free starting item(s), too few checks open at the "
                     "start to hold them: %s", self.player_name, len(granted),
                     ", ".join(item.name for item in granted))

    def should_ignore_weapon(self, name: str) -> bool:
        weapon_name = name[:-len(" Weapon Unlock Item")]
        starting_weapon = INITIAL_WEAPON_BY_VALUE.get(self.options.initial_weapon.value)
        return weapon_name == starting_weapon or weapon_name not in self.options.included_weapons.value

    def set_rules(self) -> None:
        starting_weapon = INITIAL_WEAPON_BY_VALUE.get(self.options.initial_weapon.value)
        set_rules(self.multiworld, self.player, self.options, self.route_offsets,
                  self.surface_access_via_progressive, self.nightmare_access_via_progressive,
                  starting_weapon, self.starting_aspect_index,
                  self.dream_access_via_progressive,
                  self.enemy_zone_placement)

    def create_item(self, name: str) -> Item:
        item = Hades2Item(name, self.player)
        if name in getattr(self, "_progression_items", ()):
            item.classification = ItemClassification.progression
        return item

    def create_regions(self) -> None:
        local_location_table = setup_location_table_with_settings(
            self.options, self.location_multiplier, self.dream_met_checks).copy()
        # Locations.zone_tables is module-global and holds whatever the LAST player's setup
        # built, so in a multiworld with several Hades2Rogue slots it can belong to someone
        # else by set_rules/fill_slot_data time. Keep this player's own Dream regions.
        from .Locations import zone_tables
        self.dream_zone_tables = copy.deepcopy(zone_tables.get(DREAM, {}))
        create_regions(self, local_location_table)

    def fill_slot_data(self) -> dict:
        # Every option read anywhere in generate_early/create_regions/create_items/set_rules
        # must be listed here: this doubles as the payload _apply_ut_passthrough restores on
        # a Universal Tracker regen (see ut_can_gen_without_yaml above), and UT's own
        # yaml-less-generation path regenerates from ONLY this dict, no YAML at all -- an
        # option missing here silently falls back to its default under that path.
        slot_data = self.options.as_dict(
            "included_weapons", "weapon_amount", "initial_weapon", "included_aspects", "location_system",
            "score_rewards_amount", "npc_locations",
            "grasp_intervals", "grasp_count", "arcanasanity",
            "aspectsanity", "keepsakesanity", "enemysanity", "include_minibosses", "petsanity",
            "helper_room_sanity", "combat_helper_sanity", "godsanity",
            "starting_npc_gifts",
            "reverse_vow", "reverse_rivals",
            "vow_pain", "vow_grit", "vow_wards", "vow_frenzy", "vow_hordes",
            "vow_menace", "vow_return", "vow_fangs", "vow_scars", "vow_debt",
            "vow_shadow", "vow_forfeit", "vow_time", "vow_void", "vow_hubris",
            "vow_denial", "vow_rivals",
            "goals_required", "goal_requires_zagreus", "goal_mode",
            "zagreus_encounter_mode",
            "include_regions", "include_zagreus_journey",
            "separate_checks",
            "starting_route", "lock_routes",
            "underworld_wins_needed", "surface_wins_needed", "nightmare_wins_needed",
            "dream_region_count", "dream_wins_needed", "dream_enemy_locations",
            "zagreus_defeats_needed",
            "zagreus_weaken_tiers", "weapons_clears_needed",
            "nectar_pack_value", "nectar_pack_percentage",
            "starting_health_value", "starting_health_percentage",
            "starting_magick_value", "starting_magick_percentage",
            "starting_gold_value", "starting_gold_percentage",
            "starting_armor_value", "starting_armor_percentage",
            "rarity_increase_percentage", "major_finds_percentage",  # "help_odds_percentage" REMOVED: stubbed out
            "daedalus_upgrade", "progressive_boon_level",
            "deathlink", "deathlink_percent", "deathlink_amnesty")
        # Which of the starting weapon's 4 Aspects is already active at rank 1 (random
        # already decided; 0 = default Aspect of Melinoe, 1-3 = its alternates in
        # Items.ASPECT_TITLES_BY_WEAPON order). Only meaningful when aspectsanity is
        # randomized/per_aspect -- see _main_pool_item_names.
        slot_data["starting_aspect_index"] = self.starting_aspect_index
        # Resolved route-locking offsets (random already decided), for the mod.
        slot_data["underworld_offset"] = self.route_offsets[UNDERWORLD]
        slot_data["surface_offset"] = self.route_offsets[SURFACE]
        slot_data["nightmare_offset"] = self.route_offsets[NIGHTMARE]
        slot_data["dream_offset"] = self.route_offsets[DREAM]
        slot_data["surface_start"] = 1 if self.surface_start else 0
        slot_data["nightmare_start"] = 1 if self.nightmare_start else 0
        slot_data["dream_start"] = 1 if self.dream_start else 0
        # Which routes the seed actually generated, so the mod can force a route open and
        # avoid expecting checks from an excluded route.
        slot_data["underworld_active"] = 1 if UNDERWORLD in self.active_routes else 0
        slot_data["surface_active"] = 1 if SURFACE in self.active_routes else 0
        slot_data["nightmare_active"] = 1 if NIGHTMARE in self.active_routes else 0
        slot_data["dream_active"] = 1 if DREAM in self.active_routes else 0
        # GodSanity gates Chaos too (a "Chaos Unlock" item is in the pool). A seed generated
        # before Chaos joined never sends this, so the mod keeps Chaos Gates open on it instead
        # of sealing them behind an item that doesn't exist (ItemManager.god_eligible).
        slot_data["godsanity_chaos"] = 1 if (
            self.options.godsanity.value != 0
            and GODSANITY_CHAOS in self.godsanity_gated_gods) else 0
        # A Dream Dive is somewhere NPCs are met (_resolve_dream_met_checks). Sent as 1 even when
        # Dream isn't in the seed: Universal Tracker reads this back to tell a current seed from
        # an older one. The mod only acts on it during a dive -- it then knows every Underworld/
        # Surface boss "Met" check exists, whichever routes are active.
        slot_data["dream_met_checks"] = 1 if self.dream_met_checks else 0
        # Per-route room-check totals (sum of the zones' counts) for the client's progress display.
        slot_data["underworld_room_count"] = ROUTES[UNDERWORLD]["room_count"]
        slot_data["surface_room_count"] = ROUTES[SURFACE]["room_count"]
        slot_data["nightmare_room_count"] = ROUTES[NIGHTMARE]["room_count"]
        # combine_pools' shared pool depth. NOT any single route's count: routes have genuinely
        # different totals now (43/39/40, each the sum of its own real per-zone counts), and the
        # shared pool has to be earnable on whichever single route the player is on -- so it's
        # the min across active routes (Locations._combined_room_count). The mod's
        # combined_room_limit and the client's progress display both read it.
        from .Locations import _combined_room_count
        slot_data["combined_room_count"] = _combined_room_count(self.options)
        # Dream: actual (already-clamped) region count this seed, plus the real Enemy/
        # Miniboss/Boss counter sizes -- counted directly from the generated location table
        # (not recomputed from the Y/Z formula a third time) so the mod can never disagree
        # with what Locations.fill_dream_checks actually built.
        if DREAM in self.active_routes:
            dream_names = [name for zone in self.dream_zone_tables.values() for name in zone]
            slot_data["dream_region_count_actual"] = len(self.dream_zone_tables)
            slot_data["dream_enemy_count"] = sum(1 for n in dream_names if n.startswith("Dream Enemy "))
            slot_data["dream_miniboss_count"] = sum(1 for n in dream_names if n.startswith("Dream Miniboss "))
            slot_data["dream_boss_count"] = sum(1 for n in dream_names if n.startswith("Dream Boss "))
        # Room-check multiplier from the location auto-scaler: in the room systems each room
        # depth grants this many checks (slots), so the mod must send that many per clear.
        slot_data["location_multiplier"] = self.location_multiplier
        slot_data["seed"] = "".join(self.random.choice(string.ascii_letters) for _ in range(16))
        slot_data["version_check"] = self.mod_version
        # Fixed enemy-substitution permutation for shuffled/shuffled_plus_locations. Built in
        # generate_early (see there for why it can't be rolled here) and merely serialized now,
        # so the permutation the mod applies is byte-for-byte the one set_rules derived logic
        # from. Empty string for every other enemysanity mode, including pure_random (which rolls
        # its own random pick per spawn, mod-side, and adds no locations).
        slot_data["enemysanity_shuffle_map"] = serialize_shuffle_map(self.enemysanity_shuffle_map)
        # Miniboss room permutation, same wire format ("Host:Dest,..."). Built in generate_early
        # alongside the enemy map so set_rules could place the miniboss checks against it.
        slot_data["miniboss_room_map"] = serialize_shuffle_map(self.miniboss_room_map)
        return slot_data

    def get_filler_item_name(self) -> str:
        # Used by core for extra filler (item links, start_inventory_from_pool replacements).
        return self._filler_absorber(self._filler_percentages())


def create_region(multiworld: MultiWorld, player: int, location_database, name: str,
                  locations=None, exits=None) -> Region:
    ret = Region(name, player, multiworld)
    if locations:
        for location in locations:
            loc_id = location_database.get(location, None)
            ret.locations.append(Hades2Location(player, location, loc_id, ret))
    if exits:
        for exit_name in exits:
            ret.exits.append(Entrance(player, exit_name, ret))
    return ret
