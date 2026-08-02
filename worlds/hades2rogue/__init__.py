import logging
import string

from BaseClasses import Entrance, Item, ItemClassification, MultiWorld, Region, Tutorial
from .Items import item_table, item_table_weapons, \
    item_table_arcana, item_table_arcana_progressive, \
    item_table_keepsakes_randomized, \
    item_table_familiars_randomized, WEAPON_SHORT_NAMES, ASPECT_MAX_RANK, \
    INITIAL_WEAPON_BY_VALUE, ASPECT_BASE_TITLE_BY_WEAPON, included_aspect_alts, \
    KEEPSAKE_PROGRESSIVE_COUNT, FAMILIAR_PROGRESSIVE_COUNT, \
    incantation_always, incantation_underworld, incantation_surface, incantation_nightmare, \
    incantation_keepsake_nonprog, INCANTATION_SURFACE_ONLY_EXTRA, INCANTATION_RETIRED, \
    INCANTATION_NIGHTMARE_RETIRED, INCANTATION_AUTO_GRANTED, INCANTATION_COMBINED_AWAY, \
    combined_incantation_counts, \
    vow_names, event_item_pairs, Hades2Item, item_name_groups, \
    NPC_GIFT_ITEMS, godsanity_gods, godsanity_shop_gods, helper_story_npcs, \
    helper_story_npcs_nightmare, combat_helper_npcs, KEEPSAKE_NIGHTMARE_TITLES, \
    GOD_KEEPSAKE_COMBINED_GODS, GOD_KEEPSAKE_TITLE
from .Routes import ROUTES, UNDERWORLD, SURFACE, NIGHTMARE, goal_includes
from .Locations import setup_location_table_with_settings, give_all_locations_table, \
    Hades2Location, location_name_groups, POINT_BASED, MAX_LOCATION_MULTIPLIER, \
    combine_active
from .Options import Hades2Options, hades2_option_groups, hades2_option_presets
from .Regions import create_regions
from .Rules import set_rules
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import Component, components, Type, launch_subprocess


def launch_client():
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
    launch_subprocess(launch, "Hades2RogueClient")


components.append(Component("Hades 2 Rogue Client",
                            func=launch_client, component_type=Type.CLIENT))


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
    mod_version = "0.9.0"

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

        # sr option values: 0=random, 1=underworld, 2=surface, 3=all, 4=nightmare.
        sr_by_route = {UNDERWORLD: 1, SURFACE: 2, NIGHTMARE: 4}
        start_choices = [r for r in (UNDERWORLD, SURFACE, NIGHTMARE) if r in included_set]
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

    def generate_early(self) -> None:
        from .Routes import active_routes
        self._apply_ut_passthrough()
        self._normalize_weapon_options()
        self._normalize_route_options()
        # Every route's zones 2-4 are gated by its Progressive <Route> count (see below);
        # a non-starting route additionally needs one extra copy just to unlock its own
        # first zone (offset 1), so its full clear costs 4 total instead of 3. Surface/
        # Nightmare ALSO have their own in-fiction entry gate (Access item, or -- when
        # non-starting -- their first Progressive copy doubles as the door key per Test Run
        # 5 #14); that's a separate, additional mechanic layered on top of the same offset,
        # not a substitute for it -- so all three routes set their offset identically below.
        self.route_offsets = {UNDERWORLD: 0, SURFACE: 0, NIGHTMARE: 0}
        # Which routes this seed actually generates (include_* toggles + whatever the goal
        # forces in). Excluded routes get no regions, locations, items, or events.
        self.active_routes = active_routes(self.options)

        # Which route(s) start open (their Access item precollected / no Underworld offset),
        # driven by starting_route (0=random already resolved by _normalize_route_options,
        # 1=underworld, 2=surface, 3=all active routes, 4=nightmare).
        sr = self.options.starting_route.value
        sr_route = {1: UNDERWORLD, 2: SURFACE, 4: NIGHTMARE}.get(sr)
        if sr == 3:
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

        # --- Auto-scale locations so every item fits with ~40 filler to spare ----------
        # point_based bumps score_rewards_amount (each added score check is one location);
        # the room systems grow a multiplier so each room depth grants more checks. Both
        # are capped (score ids per route, MAX_LOCATION_MULTIPLIER); if a seed is still too
        # full after the cap, create_items logs a warning and Archipelago drops the excess.
        self.location_multiplier = 1
        target = len(self._main_pool_item_names()[0]) + 40
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
        table = setup_location_table_with_settings(self.options, multiplier)
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
        # (see ItemManager.lua apply_starting_aspect).
        self.starting_aspect_index = 0
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
            self.starting_aspect_index = self._resolve_starting_aspect_index()
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
            # included_aspects doesn't apply here (per Options.py's docstring, only
            # randomized/per_aspect truncate individual Aspects) -- only included_weapons does.
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
            self.starting_aspect_index = self._resolve_starting_aspect_index()
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
        # are active, the 11 GodSanity gods' own "<God> Unlock" item and keepsake item fuse
        # into a single "<God> Unlock + Keepsake" item (see Items.GOD_KEEPSAKE_TITLE) --
        # receiving it unlocks that god's boons AND makes their keepsake giftable at once,
        # instead of needing both items separately. Computed here (before both blocks below)
        # so the keepsake loop can skip the 11 fused titles and the godsanity block can add
        # the combined items instead of the plain "<God> Unlock" ones.
        combine_god_keepsake = keep == 1 and self.options.godsanity.value != 0
        if keep == 1:
            for name in item_table_keepsakes_randomized:
                if not zj_on and name in KEEPSAKE_NIGHTMARE_TITLES:
                    continue
                if combine_god_keepsake and name in GOD_KEEPSAKE_TITLE.values():
                    continue
                prog.add(name)
                pool.append(name)
        elif keep == 2:
            prog.add("Progressive Keepsake")
            pool += ["Progressive Keepsake"] * KEEPSAKE_PROGRESSIVE_COUNT

        # Familiars (petsanity): 1 = randomized, 2 = progressive, 0 = unlocked (no items).
        pet = self.options.petsanity.value
        if pet == 1:
            pool += list(item_table_familiars_randomized)
        elif pet == 2:
            pool += ["Progressive Familiar"] * FAMILIAR_PROGRESSIVE_COUNT

        # Boon gods (godsanity): any value other than "unlocked" (0) locks each of the 9
        # boon gods behind its own "<God> Unlock" item -- progression, since Rules.py gates
        # that god's "Met"/"Keepsake" locations on holding it (see Items.item_table_gods).
        if self.options.godsanity.value != 0 and combine_god_keepsake:
            # KeepsakeSanity=randomized too: fused items replace both halves for all 11 gods
            # (see Items.GOD_KEEPSAKE_COMBINED_GODS / GOD_KEEPSAKE_TITLE above).
            for god in GOD_KEEPSAKE_COMBINED_GODS:
                name = f"{god} Unlock + Keepsake"
                prog.add(name)
                pool.append(name)
        elif self.options.godsanity.value != 0:
            pool += [f"{god} Unlock" for god in godsanity_gods]
            # Hermes/Selene: same item shape and pool condition, gated in Lua via an
            # existence-only check instead (see Items.godsanity_shop_gods).
            pool += [f"{god} Unlock" for god in godsanity_shop_gods]

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
        # NPC selected in starting_npc_gifts -- see Items.NPC_GIFT_ITEMS).
        pool += ["Daedalus Upgrade"] * int(self.options.daedalus_upgrade)
        for npc in self.options.starting_npc_gifts.value:
            pool.append(NPC_GIFT_ITEMS[npc])

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

        # Incantation items (Cauldron unlocks, shuffled): always-on set, plus route- and
        # keepsake-gated sets. Each grants its world-upgrade in-game; no check locations.
        underworld_on = UNDERWORLD in self.active_routes
        surface_on = SURFACE in self.active_routes
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
        # aren't progressive (progressive controls leveling via its own items).
        if self.options.keepsakesanity.value != 2:
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
        # one extra per unit of a route's lock offset (see generate_early).
        if self.options.lock_routes:
            for route in self.active_routes:
                pool += [ROUTES[route]["progressive"]] * (3 + self.route_offsets[route])

        return pool, precollect, prog

    def create_items(self) -> None:
        local_location_table = setup_location_table_with_settings(
            self.options, self.location_multiplier).copy()

        pool_names, precollect_names, prog_names = self._main_pool_item_names()
        pool = []
        for name in pool_names:
            item = Hades2Item(name, self.player)
            if name in prog_names:
                item.classification = ItemClassification.progression
            pool.append(item)
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
        if len(pool) > fillable:
            logging.warning(
                "Hades 2 (player %s): %d non-filler items but only %d fillable locations - "
                "Archipelago will drop %d of them. Raise score_rewards_amount (point_based), "
                "use a location system with more checks, or turn off some sanities, to keep every item.",
                self.player_name, len(pool), fillable, len(pool) - fillable)
        total_fillers_needed = fillable - len(pool)
        if total_fillers_needed > 0:
            pool += self.build_filler_pool(total_fillers_needed)

        self.multiworld.itempool += pool

    def build_filler_pool(self, amount: int) -> list:
        percentages = {
            "Nectar": int(self.options.nectar_pack_percentage),
            "Starting Max Health": int(self.options.starting_health_percentage),
            "Starting Max Magick": int(self.options.starting_magick_percentage),
            "Starting Gold": int(self.options.starting_gold_percentage),
            "Starting Armor": int(self.options.starting_armor_percentage),
            "Rarity Increase": int(self.options.rarity_increase_percentage),
            "Increased Odds of Major Finds": int(self.options.major_finds_percentage),
            # "Increased Help Odds": int(self.options.help_odds_percentage),  # REMOVED: stubbed out
        }

        # The "absorber" soaks up the rounding remainder; it must be a filler we are keeping.
        absorber = next((n for n in ("Nectar", "Starting Max Health", "Starting Gold", "Rarity Increase",
                                     "Increased Odds of Major Finds",
                                     "Starting Max Magick", "Starting Armor")  # "Increased Help Odds" REMOVED
                         ), "Nectar")
        total_percentage = sum(percentages.values())
        if total_percentage == 0:
            percentages[absorber] = 1
            total_percentage = 1

        filler = []
        allocated = 0
        names = [n for n in ("Nectar",
                             "Starting Max Health", "Starting Max Magick", "Starting Gold", "Starting Armor",
                             "Rarity Increase", "Increased Odds of Major Finds")
                 if n != absorber]  # "Increased Help Odds" REMOVED
        for name in names:
            count = int(amount * percentages[name] / total_percentage)
            for _ in range(count):
                filler.append(Hades2Item(name, self.player))
            allocated += count
        for _ in range(amount - allocated):
            filler.append(Hades2Item(absorber, self.player))
        return filler

    def should_ignore_weapon(self, name: str) -> bool:
        weapon_name = name[:-len(" Weapon Unlock Item")]
        starting_weapon = INITIAL_WEAPON_BY_VALUE.get(self.options.initial_weapon.value)
        return weapon_name == starting_weapon or weapon_name not in self.options.included_weapons.value

    def set_rules(self) -> None:
        starting_weapon = INITIAL_WEAPON_BY_VALUE.get(self.options.initial_weapon.value)
        set_rules(self.multiworld, self.player, self.options, self.route_offsets,
                  self.surface_access_via_progressive, self.nightmare_access_via_progressive,
                  starting_weapon, self.starting_aspect_index)

    def create_item(self, name: str) -> Item:
        return Hades2Item(name, self.player)

    def create_regions(self) -> None:
        local_location_table = setup_location_table_with_settings(
            self.options, self.location_multiplier).copy()
        create_regions(self, local_location_table)

    def fill_slot_data(self) -> dict:
        # Every option read anywhere in generate_early/create_regions/create_items/set_rules
        # must be listed here: this doubles as the payload _apply_ut_passthrough restores on
        # a Universal Tracker regen (see ut_can_gen_without_yaml above), and UT's own
        # yaml-less-generation path regenerates from ONLY this dict, no YAML at all -- an
        # option missing here silently falls back to its default under that path.
        slot_data = self.options.as_dict(
            "included_weapons", "weapon_amount", "initial_weapon", "included_aspects", "location_system",
            "score_rewards_amount", "enemy_locations", "npc_locations",
            "grasp_intervals", "grasp_count", "arcanasanity",
            "aspectsanity", "keepsakesanity", "petsanity",
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
        slot_data["surface_start"] = 1 if self.surface_start else 0
        slot_data["nightmare_start"] = 1 if self.nightmare_start else 0
        # Which routes the seed actually generated, so the mod can force a route open and
        # avoid expecting checks from an excluded route.
        slot_data["underworld_active"] = 1 if UNDERWORLD in self.active_routes else 0
        slot_data["surface_active"] = 1 if SURFACE in self.active_routes else 0
        slot_data["nightmare_active"] = 1 if NIGHTMARE in self.active_routes else 0
        # Per-route room-check counts, so the mod knows the cap and can flush all
        # remaining room checks when the route's final boss is defeated (boss cascade).
        slot_data["underworld_room_count"] = ROUTES[UNDERWORLD]["room_count"]
        slot_data["surface_room_count"] = ROUTES[SURFACE]["room_count"]
        slot_data["nightmare_room_count"] = ROUTES[NIGHTMARE]["room_count"]
        # Room-check multiplier from the location auto-scaler: in the room systems each room
        # depth grants this many checks (slots), so the mod must send that many per clear.
        slot_data["location_multiplier"] = self.location_multiplier
        slot_data["seed"] = "".join(self.random.choice(string.ascii_letters) for _ in range(16))
        slot_data["version_check"] = self.mod_version
        return slot_data

    def get_filler_item_name(self) -> str:
        return "Nectar"


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
