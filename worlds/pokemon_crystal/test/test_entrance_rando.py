from .bases import PokemonCrystalTestBase
from ..data import data, load_json_data, is_tile_warp, OUTDOOR_ENVIRONMENTS
from ..entrance_rando import (ENTRANCE_CATEGORIES, ER_BIPARTITE_CATEGORIES, ER_BIPARTITE_SUFFIX,
                              WARP_TO_ENTRANCES, base_category, build_reverse_conn_lookup)


# Raw categories as they appear in the data, i.e. with the " Entrance"/" Exit"
# suffix on the bipartite ones. The option-facing names are the stripped ones.
_VALID_CATEGORIES = frozenset(load_json_data("entrance_types.json").values())


def _oracle_tile_ids() -> dict:
    """(map, warp_index) -> id, derived from warp_ids.json independently of production."""
    return {(w["map"], w["warp_index"]): w["id"]
            for w in load_json_data("warp_ids.json")["warps"] if is_tile_warp(w)}


def _bipartite_side(category: str) -> str | None:
    """"Entrance", "Exit", or None for a category that is not bipartite."""
    match = ER_BIPARTITE_SUFFIX.search(category)
    return match.group(1) if match else None


def _connection_is_outdoor(conn) -> bool | None:
    """Whether this connection's door mouth stands outdoors, or None if unknown."""
    if not conn.exit_warps:
        return None
    map_data = data.maps.get(conn.exit_warps[0].map_name)
    if map_data is None:
        return None
    return map_data.environment in OUTDOOR_ENVIRONMENTS


class EntranceDataStructureTest(PokemonCrystalTestBase):
    """Verify entrance_data.json structural invariants without generating a world."""
    auto_construct = False

    VALID_CATEGORIES = _VALID_CATEGORIES

    def test_every_connection_has_a_category(self):
        """Every connection in entrance_data.json must have a valid category."""
        for name, conn in data.entrance_connections.items():
            self.assertIn(conn.category, self.VALID_CATEGORIES,
                          f"{name} has invalid category {conn.category!r}")

    def test_no_orphan_entries_in_entrance_types(self):
        """Every key in entrance_types.json must correspond to a real connection."""
        entrance_types = load_json_data("entrance_types.json")
        connection_names = set(data.entrance_connections.keys())
        orphans = set(entrance_types.keys()) - connection_names
        self.assertEqual(orphans, set(), f"Orphan entrance_types.json entries: {orphans}")

    def test_all_connections_have_reverse_lookup(self):
        """Every two-way connection should have a reverse in the lookup."""
        conns = data.entrance_connections
        reverse_lookup = build_reverse_conn_lookup(conns)
        for name, conn in conns.items():
            if conn.one_way:
                continue
            self.assertIn(name, reverse_lookup,
                          f"Two-way connection {name} has no reverse in lookup")

    def test_reverse_lookup_is_symmetric(self):
        """If A's reverse is B, then B's reverse should be A."""
        conns = data.entrance_connections
        reverse_lookup = build_reverse_conn_lookup(conns)
        for name, reverse_name in reverse_lookup.items():
            if conns[name].one_way:
                continue
            self.assertIn(reverse_name, reverse_lookup,
                          f"Reverse of {name} is {reverse_name} but {reverse_name} has no reverse")
            self.assertEqual(reverse_lookup[reverse_name], name,
                             f"Reverse is not symmetric: {name} -> {reverse_name} -> {reverse_lookup.get(reverse_name)}")

    def test_two_way_pairs_have_matching_types(self):
        """Both directions of a two-way pair should have the same entrance type."""
        conns = data.entrance_connections
        reverse_lookup = build_reverse_conn_lookup(conns)
        for name, conn in conns.items():
            if conn.one_way:
                continue
            reverse_name = reverse_lookup.get(name)
            if reverse_name is None:
                continue
            reverse_conn = conns[reverse_name]
            self.assertEqual(base_category(conn.category), base_category(reverse_conn.category),
                             f"{name} has category '{conn.category}' but reverse {reverse_name} "
                             f"has category '{reverse_conn.category}'")

    def test_bipartite_pairs_face_opposite_ways(self):
        """A bipartite category's two directions must carry opposite suffixes. If a pair
        ends up on the same side, its pool can pair the two doors of one wall together and
        strand whatever they led to."""
        conns = data.entrance_connections
        reverse_lookup = build_reverse_conn_lookup(conns)
        for name, conn in conns.items():
            if conn.one_way or base_category(conn.category) not in ER_BIPARTITE_CATEGORIES:
                continue
            reverse_name = reverse_lookup.get(name)
            self.assertIsNotNone(reverse_name, f"{name} is bipartite but has no reverse")
            reverse_conn = conns[reverse_name]
            self.assertIn(_bipartite_side(conn.category), ("Entrance", "Exit"),
                          f"{name} has no bipartite suffix but its category is bipartite")
            self.assertNotEqual(_bipartite_side(conn.category), _bipartite_side(reverse_conn.category),
                                f"{name} ({conn.category}) and its reverse {reverse_name} "
                                f"({reverse_conn.category}) face the same way")

    def test_every_bipartite_category_has_both_sides(self):
        """A bipartite category missing one side would build a pool that maps to an
        empty group, which GER cannot satisfy."""
        sides: dict[str, set[str]] = {}
        for category in _VALID_CATEGORIES:
            base = base_category(category)
            if base in ER_BIPARTITE_CATEGORIES:
                sides.setdefault(base, set()).add(_bipartite_side(category))
        self.assertEqual(sides, {base: {"Entrance", "Exit"} for base in ER_BIPARTITE_CATEGORIES})

    def test_door_categories_enter_from_outdoors(self):
        """For the categories that are a door in a wall, "Entrance" is the overworld side
        and "Exit" is the interior side. Guards against a flipped label, which would let a
        pool join two overworld mouths and island off the interiors behind them."""
        door_categories = {"Building", "Gym", "Mart", "Pokecenter"}
        self.assertLessEqual(door_categories, set(ER_BIPARTITE_CATEGORIES))
        for name, conn in data.entrance_connections.items():
            base, side = base_category(conn.category), _bipartite_side(conn.category)
            if base not in door_categories:
                continue
            self.assertEqual(_connection_is_outdoor(conn), side == "Entrance",
                             f"{name} is a {conn.category} but its door mouth is on the other side")

    def test_exit_warps_have_resolvable_labels(self):
        """Every exit_warp label should exist in rom_addresses."""
        rom_addrs = data.rom_addresses
        for name, conn in data.entrance_connections.items():
            for ew in conn.exit_warps:
                label = ew.label or f"AP_Warp_{ew.map_name}_{ew.warp_index}"
                self.assertIn(label, rom_addrs,
                              f"{name}: label {label} not found in rom_addresses")

    def test_exit_warp_ids_match_warp_ids_json(self):
        """Every traversal-source exit warp's warp_id must equal the id derived
        independently from warp_ids.json; boarding-side warps must have none."""
        id_by_tile = _oracle_tile_ids()
        id_by_label = {w["label"]: w["id"]
                       for w in load_json_data("warp_ids.json")["warps"] if w.get("label")}
        for name, conn in data.entrance_connections.items():
            for ew in conn.exit_warps:
                if ew.addr_offset == 4:
                    self.assertIsNone(ew.warp_id, f"{name}: boarding-side warp has a warp_id")
                    continue
                expected = id_by_label.get(ew.label) if ew.addr_offset == 1 else \
                    id_by_tile.get((ew.map_name, ew.warp_index))
                self.assertIsNotNone(expected, f"{name}: {ew.map_name}/{ew.warp_index} "
                                               f"has no id in warp_ids.json")
                self.assertEqual(ew.warp_id, expected, f"{name}: {ew.map_name}/{ew.warp_index}")

    def test_arrival_map_consts_are_valid(self):
        """Every connection's arrival_map_const should exist in map_constants."""
        map_consts = data.map_constants
        for name, conn in data.entrance_connections.items():
            if not conn.arrival_map_const:
                continue
            self.assertIn(conn.arrival_map_const, map_consts,
                          f"{name}: arrival_map_const '{conn.arrival_map_const}' not in map_constants")


_ALL_CATEGORIES = sorted(ENTRANCE_CATEGORIES)


def _count_cross_category(world) -> int:
    conns = data.entrance_connections
    cross = 0
    for src, tgt in world.er_pairings:
        cs, ct = conns.get(src), conns.get(tgt)
        if cs and ct and base_category(cs.category) != base_category(ct.category):
            cross += 1
    return cross


def _same_side_pairings(world) -> list[tuple[str, str]]:
    """Pairings inside a bipartite category that join two doors facing the same way.
    Under coupled ER that glues two mouths of one wall together."""
    conns = data.entrance_connections
    offenders = []
    for src, tgt in world.er_pairings:
        cs, ct = conns.get(src), conns.get(tgt)
        if cs is None or ct is None:
            continue
        if base_category(cs.category) not in ER_BIPARTITE_CATEGORIES:
            continue
        if _bipartite_side(cs.category) == _bipartite_side(ct.category):
            offenders.append((src, tgt))
    return offenders


def _orphan_er_entrances(world) -> list:
    return [e.name for e, _v in world.er_entrances if e.connected_region is None]


def _assert_pool_balanced(test, note: str) -> None:
    exits, targets = _free_pool_counts(test.world)
    test.assertEqual(exits, targets, f"pool unbalanced {note}: {exits} exits vs {targets} targets")


def _free_pool_counts(world) -> tuple[int, int]:
    """(unplaced exits, unclaimed ER targets) currently in the region graph."""
    exits = targets = 0
    for region in world.multiworld.get_regions(world.player):
        exits += sum(1 for ex in region.exits if not ex.connected_region)
        targets += sum(1 for ent in region.entrances if not ent.parent_region)
    return exits, targets


class ERAllMixedCoupledTest(PokemonCrystalTestBase):
    """Default mix_entrances (all categories mixed) with coupling on."""
    options = {
        "randomize_entrances": _ALL_CATEGORIES,
        "coupled_entrances": True,
    }

    def test_er_pairings_generated(self):
        self.assertTrue(len(self.world.er_pairings) > 0)

    def test_every_pairing_has_valid_source(self):
        conns = data.entrance_connections
        for source_name, _ in self.world.er_pairings:
            self.assertIn(source_name, conns,
                          f"Pairing source '{source_name}' not in entrance_connections")

    def test_every_pairing_resolves_for_patching(self):
        conns = data.entrance_connections
        reverse_lookup = build_reverse_conn_lookup(conns)
        map_consts = data.map_constants
        unresolved = []
        for source_name, target_name in self.world.er_pairings:
            source_conn = conns.get(source_name)
            if source_conn is None or not source_conn.exit_warps:
                continue
            if target_name.endswith(" (one-way target)"):
                target_conn = conns.get(target_name.removesuffix(" (one-way target)"))
            else:
                reverse_target_name = reverse_lookup.get(target_name)
                target_conn = conns.get(reverse_target_name) if reverse_target_name else None
            if target_conn is None:
                unresolved.append((source_name, target_name, "no reverse target"))
            elif target_conn.arrival_map_const not in map_consts:
                unresolved.append((source_name, target_name, "bad arrival_map_const"))
        self.assertEqual(len(unresolved), 0,
                         "Unresolved pairings:\n" + "\n".join(
                             f"  {s} => {t}: {reason}" for s, t, reason in unresolved))

    def test_no_duplicate_source_pairings(self):
        seen = set()
        for source_name, _ in self.world.er_pairings:
            self.assertNotIn(source_name, seen,
                             f"'{source_name}' appears as source multiple times")
            seen.add(source_name)


class ERDeferredReconnectCoupledTest(PokemonCrystalTestBase):
    """Deferred (Universal Tracker) reconnection under coupled ER.

    Regression: walking through a door must only open that door and the
    partner door the player arrives at (the coupled walk-back), never the
    vanilla string-reverse of the door's name, which is an unrelated,
    independently-randomized entrance the player never discovered.
    """
    options = {
        "randomize_entrances": _ALL_CATEGORIES,
        "coupled_entrances": True,
    }

    def _enter_deferred_mode(self):
        world = self.world
        world.multiworld.re_gen_passthrough = {world.game: {
            "er_pairings": list(world.er_pairings),
            "coupled_entrances": True,
        }}
        world.multiworld.enforce_deferred_connections = "on"
        world._reconnect_ut_entrances()

    def test_coupled_walk_back_opens_partner_not_vanilla_reverse(self):
        conns = data.entrance_connections
        warp_id_by_tile = _oracle_tile_ids()
        self._enter_deferred_mode()
        world = self.world
        targets = world._deferred_entrance_targets
        partners = world._deferred_entrance_partners
        w2e = WARP_TO_ENTRANCES

        # A two-way door whose oracle-derived id maps unambiguously to itself,
        # with a coupled partner differing from the vanilla string-reverse.
        candidate = None
        for source, partner in partners.items():
            conn = conns.get(source)
            if conn is None or not conn.exit_warps:
                continue
            first = conn.exit_warps[0]
            expected_id = warp_id_by_tile.get((first.map_name, first.warp_index))
            if expected_id is None or w2e.get(expected_id) != [source]:
                continue
            left, right = source.split(" -> ", 1)
            reverse = f"{right} -> {left}"
            if reverse == partner or reverse not in targets:
                continue
            candidate = (source, partner, reverse, expected_id)
            break

        self.assertIsNotNone(candidate, "No suitable coupled door found for the test")
        source, partner, reverse, warp_id = candidate

        get = lambda name: world.multiworld.get_entrance(name, world.player)
        # Deferred: nothing connected until its warp is discovered.
        self.assertIsNone(get(source).connected_region)
        self.assertIsNone(get(partner).connected_region)
        self.assertIsNone(get(reverse).connected_region)

        world.reconnect_found_entrances("k", [warp_id])

        self.assertIsNotNone(get(source).connected_region,
                             "Walked door did not open")
        self.assertIsNotNone(get(partner).connected_region,
                             "Coupled partner (walk-back) did not open")
        self.assertIsNone(get(reverse).connected_region,
                          "Vanilla string-reverse was opened without being discovered")


class ERAllMixedDecoupledTest(PokemonCrystalTestBase):
    """Same as above but decoupled. One-ways remain structurally one-way either way."""
    options = {
        "randomize_entrances": _ALL_CATEGORIES,
        "coupled_entrances": False,
    }

    def test_decoupled_generates(self):
        self.assertTrue(len(self.world.er_pairings) > 0)


class ERGymIsolatedTest(PokemonCrystalTestBase):
    """Gym and Gym Interior removed from mix_entrances — gym entrances shuffle only
    with each other. There is no fallback that mixes categories, so this holds on
    every seed."""
    options = {
        "randomize_entrances": _ALL_CATEGORIES,
        "mix_entrances": [c for c in _ALL_CATEGORIES if not c.startswith("Gym")],
        "coupled_entrances": True,
    }

    def test_gym_pairings_respect_isolation(self):
        conns = data.entrance_connections
        reverse_lookup = build_reverse_conn_lookup(conns)
        self.assertTrue(len(self.world.er_pairings) > 0, "expected some ER pairings")

        for source_name, target_name in self.world.er_pairings:
            src = conns[source_name]
            if base_category(src.category) != "Gym":
                continue
            if target_name.endswith(" (one-way target)"):
                tgt_name = target_name.removesuffix(" (one-way target)")
            else:
                tgt_name = reverse_lookup.get(target_name, target_name)
            tgt = conns.get(tgt_name)
            if tgt is None:
                continue
            self.assertEqual(base_category(tgt.category), "Gym",
                             f"Gym source {source_name} paired to non-Gym target "
                             f"{tgt_name} (category={tgt.category})")


class ERMultipleIsolatedTest(PokemonCrystalTestBase):
    """Multiple closed pools — Gym and Mart each shuffle only within themselves."""
    options = {
        "randomize_entrances": _ALL_CATEGORIES,
        "mix_entrances": [c for c in _ALL_CATEGORIES
                          if not c.startswith("Gym") and not c.startswith("Mart")],
        "coupled_entrances": True,
    }

    def test_generates(self):
        self.assertTrue(len(self.world.er_pairings) > 0)


class EROffTest(PokemonCrystalTestBase):
    """Empty randomize_entrances disables ER entirely."""
    options = {
        "randomize_entrances": [],
    }

    def test_no_er_pairings(self):
        self.assertEqual(len(self.world.er_pairings), 0)


class EROneWayOnlyTest(PokemonCrystalTestBase):
    """Only One-Ways randomized. Validates the One-Way-isolated pool works on its own."""
    options = {
        "randomize_entrances": ["One-Way"],
    }

    def test_oneway_generate(self):
        conns = data.entrance_connections
        self.assertTrue(len(self.world.er_pairings) > 0)
        for source_name, _ in self.world.er_pairings:
            self.assertEqual(conns[source_name].category, "One-Way")


class ERSpawnPokecenterPinnedTest(PokemonCrystalTestBase):
    """The spawn town's pokecenter is kept vanilla so the player always has healing.
    Regression: the pin is selected by category name, which silently matched nothing
    once Pokecenter gained its Entrance/Exit sides."""
    options = {
        "randomize_entrances": _ALL_CATEGORIES,
        "coupled_entrances": True,
    }

    # Default spawn is New Bark Town, whose pokecenter region is Cherrygrove.
    _PINNED = ("REGION_CHERRYGROVE_CITY -> REGION_CHERRYGROVE_POKECENTER_1F",
               "REGION_CHERRYGROVE_POKECENTER_1F -> REGION_CHERRYGROVE_CITY")

    def test_spawn_pokecenter_stays_vanilla(self):
        sources = {src for src, _ in self.world.er_pairings}
        pool = {entrance.name for entrance, _v in self.world.er_entrances}
        for name in self._PINNED:
            self.assertNotIn(name, sources, f"{name} was randomized despite being pinned")
            self.assertNotIn(name, pool, f"{name} is still in the ER pool")
            entrance = self.world.multiworld.get_entrance(name, self.world.player)
            self.assertEqual(entrance.connected_region.name, name.split(" -> ", 1)[1])

    def test_other_pokecenters_are_still_randomized(self):
        sources = {src for src, _ in self.world.er_pairings}
        self.assertIn("REGION_VIOLET_CITY -> REGION_VIOLET_POKECENTER_1F", sources)


def _named_lookup(randomize: set[str], mix: set[str]) -> dict[str, list[str]]:
    """build_er_group_lookup's target map, keyed by pool name instead of group id."""
    from ..entrance_rando import build_er_group_lookup
    lookup, group_map = build_er_group_lookup(randomize, mix)
    names = {gid: name for name, gid in group_map.items()}
    return {names[gid]: sorted(names[target] for target in targets) for gid, targets in lookup.items()}


class ERGroupLookupTest(PokemonCrystalTestBase):
    """Unit tests for build_er_group_lookup (no world gen)."""
    auto_construct = False

    def test_option_categories_are_the_data_categories_without_side_suffixes(self):
        """randomize_entrances/mix_entrances are named without the bipartite suffix, so the
        option keys and the data categories have to agree after stripping."""
        from ..options import RandomizeEntrances, MixEntrances
        self.assertEqual(set(ENTRANCE_CATEGORIES), {base_category(c) for c in _VALID_CATEGORIES})
        for option in (RandomizeEntrances, MixEntrances):
            keys = {k for k in option.valid_keys if not k.startswith("_")}
            self.assertEqual(keys, set(ENTRANCE_CATEGORIES), option.__name__)
        self.assertEqual(set(MixEntrances.default), set(ENTRANCE_CATEGORIES))

    def test_bipartite_categories_are_the_expected_ones(self):
        """Guards against data drift silently dropping a bipartition, which would let a
        pool pair two doors that face the same way."""
        self.assertEqual(set(ER_BIPARTITE_CATEGORIES),
                         {"Building", "Dungeon", "Elevator", "Gate", "Gym", "Mart", "Pokecenter"})

    def test_isolated_bipartite_pool_only_targets_its_other_side(self):
        lookup = _named_lookup({"Gym", "Mart", "Pokemon League"}, set())
        self.assertEqual(lookup["Gym Entrance"], ["Gym Exit"])
        self.assertEqual(lookup["Gym Exit"], ["Gym Entrance"])
        self.assertEqual(lookup["Mart Entrance"], ["Mart Exit"])
        self.assertEqual(lookup["Mart Exit"], ["Mart Entrance"])

    def test_isolated_non_bipartite_pool_maps_to_itself(self):
        self.assertNotIn("Pokemon League", ER_BIPARTITE_CATEGORIES)
        lookup = _named_lookup({"Pokemon League"}, set())
        self.assertEqual(lookup["Pokemon League"], ["Pokemon League"])

    def test_mixed_categories_reach_each_other_but_not_isolated_ones(self):
        """Building and Mart mix; Gym stays isolated, so neither side may reach it."""
        lookup = _named_lookup({"Gym", "Mart", "Building"}, {"Mart", "Building"})
        self.assertEqual(lookup["Building Entrance"], ["Building Exit", "Mart Exit"])
        self.assertEqual(lookup["Building Exit"], ["Building Entrance", "Mart Entrance"])
        self.assertEqual(lookup["Gym Entrance"], ["Gym Exit"])
        self.assertEqual(lookup["Gym Exit"], ["Gym Entrance"])

    def test_mixing_preserves_the_bipartition(self):
        """Mixing widens which categories a pool may reach; it must never let a pool reach
        its own side, which is what keeps the two mouths of one wall apart."""
        lookup = _named_lookup(set(_ALL_CATEGORIES), set(_ALL_CATEGORIES))
        for pool, targets in lookup.items():
            side = _bipartite_side(pool)
            if side is None:
                continue
            for target in targets:
                self.assertNotEqual(side, _bipartite_side(target),
                                    f"mixed pool {pool} may target same-side {target}")

    def test_non_bipartite_category_splits_when_mixed_with_a_bipartite_one(self):
        """An unsplit category in a walled pool would drain one side of the wall and
        deadlock GER, so mixing with a bipartite category forces a virtual split."""
        lookup = _named_lookup({"Pokemon League", "Gym"}, {"Pokemon League", "Gym"})
        self.assertEqual(lookup["Pokemon League Entrance"], ["Gym Exit", "Pokemon League Exit"])
        self.assertEqual(lookup["Pokemon League Exit"], ["Gym Entrance", "Pokemon League Entrance"])
        self.assertEqual(lookup["Gym Entrance"], ["Gym Exit", "Pokemon League Exit"])

    def test_non_bipartite_categories_mixed_together_stay_unsplit(self):
        """With no wall in the pool there is nothing to drain, so the pool keeps the
        full pairing space."""
        lookup = _named_lookup({"Pokemon League", "Gym Interior"}, {"Pokemon League", "Gym Interior"})
        self.assertEqual(lookup["Pokemon League"], ["Gym Interior", "Pokemon League"])
        self.assertEqual(lookup["Gym Interior"], ["Gym Interior", "Pokemon League"])

    def test_virtual_sides_cover_reverse_pairs(self):
        """Every splittable connection has a side, and its reverse sits on the other one."""
        from ..entrance_rando import ER_VIRTUAL_SIDES, ER_VIRTUAL_SPLITTABLE
        self.assertEqual(set(ER_VIRTUAL_SPLITTABLE),
                         {"Building Interior", "Dungeon Interior", "Gym Interior",
                          "Mart Interior", "Pokemon League"})
        reverse_lookup = build_reverse_conn_lookup(data.entrance_connections)
        for name, conn in data.entrance_connections.items():
            if conn.category not in ER_VIRTUAL_SPLITTABLE:
                continue
            self.assertIn(name, ER_VIRTUAL_SIDES)
            self.assertNotEqual(ER_VIRTUAL_SIDES[name], ER_VIRTUAL_SIDES[reverse_lookup[name]],
                                f"{name} and its reverse share a virtual side")

    def test_oneway_always_isolated(self):
        from ..entrance_rando import ER_GROUP_ONEWAY
        # Even with One-Ways in mix_entrances (which is the default), it gets its own pool.
        for mix in ({"One-Way", "Building"}, {"Building"}, set()):
            with self.subTest(mix=sorted(mix)):
                lookup = _named_lookup({"One-Way", "Building"}, mix)
                self.assertEqual(lookup["One-Way"], ["One-Way"])
        from ..entrance_rando import build_er_group_lookup
        lookup, _ = build_er_group_lookup({"Building"}, {"Building"})
        self.assertNotIn(ER_GROUP_ONEWAY, lookup,
                         "One-Way got a pool despite not being randomized")

    def test_unrandomized_categories_get_no_pool(self):
        lookup = _named_lookup({"Gym"}, set(_ALL_CATEGORIES))
        self.assertEqual(set(lookup), {"Gym Entrance", "Gym Exit"})

    def test_target_lists_are_ordered_and_unique(self):
        """GER concatenates a pool's target groups in the order given before shuffling, so
        an order that came out of an unordered set would make the same seed generate
        differently from one process to the next."""
        from ..entrance_rando import build_er_group_lookup
        for mix in (set(), {"Building", "Mart"}, set(_ALL_CATEGORIES)):
            with self.subTest(mix=sorted(mix)):
                lookup, _ = build_er_group_lookup(set(_ALL_CATEGORIES), mix)
                for gid, targets in lookup.items():
                    self.assertEqual(targets, sorted(targets), f"group {gid} targets are unordered")
                    self.assertEqual(len(targets), len(set(targets)), f"group {gid} has duplicate targets")

    def test_every_pool_has_at_least_one_target(self):
        """A pool that targets nothing is an instant GER deadlock."""
        for mix in (set(), {"Building", "Mart"}, set(_ALL_CATEGORIES)):
            with self.subTest(mix=sorted(mix)):
                for pool, targets in _named_lookup(set(_ALL_CATEGORIES), mix).items():
                    self.assertTrue(targets, f"pool {pool} has no targets")


class ERBipartitePoolIsolationTest(PokemonCrystalTestBase):
    """Isolating the bipartite categories must hold, and every pairing must join doors
    that face opposite ways."""
    auto_construct = False

    def test_bipartite_pools_stay_isolated(self):
        self.options = {
            "randomize_entrances": _ALL_CATEGORIES,
            "mix_entrances": [c for c in _ALL_CATEGORIES if c not in ER_BIPARTITE_CATEGORIES],
            "coupled_entrances": True,
        }
        conns = data.entrance_connections

        for seed in range(1, 4):
            with self.subTest(seed=seed):
                self.world_setup(seed=seed)

                for source_name, target_name in self.world.er_pairings:
                    source = conns.get(source_name)
                    if source is None or base_category(source.category) not in ER_BIPARTITE_CATEGORIES:
                        continue
                    target = conns.get(target_name)
                    if target is None:
                        self.fail(f"{target_name} is not a connection")
                    self.assertEqual(base_category(target.category), base_category(source.category),
                                     f"{source_name} ({source.category}) paired outside its pool "
                                     f"to {target_name} ({target.category})")
                    self.assertNotEqual(_bipartite_side(source.category), _bipartite_side(target.category),
                                        f"{source_name} paired to same-side {target_name}; "
                                        f"this strands the interiors they led to")

    def test_default_mix_keeps_the_bipartition_and_needs_no_pins(self):
        """The shipped default mixes every category together. Doors still may not pair with
        doors facing the same way, One-Ways still shuffle only among themselves, and the
        whole pool places without falling back to vanilla pins."""
        import logging
        import worlds.pokemon_crystal.entrance_rando as crystal_er

        self.options = {
            "randomize_entrances": _ALL_CATEGORIES,
            "coupled_entrances": True,
        }
        conns = data.entrance_connections
        logger = logging.getLogger(crystal_er.__name__)
        with self.assertLogs(logger, level="WARNING") as log_ctx:
            logger.warning("test-guard: setup starting")
            self.world_setup(seed=1)
        self.assertNotIn("pin round", "\n".join(log_ctx.output),
                         "the default mix should place without vanilla pins")
        self.assertEqual(_same_side_pairings(self.world), [])
        for source_name, target_name in self.world.er_pairings:
            source = conns.get(source_name)
            if source is None or source.category != "One-Way":
                continue
            self.assertTrue(target_name.endswith(" (one-way target)"),
                            f"One-Way {source_name} paired to two-way target {target_name}")


class ERTransientFailureRetryTest(PokemonCrystalTestBase):
    """A transient ER failure is recovered by retrying with a fresh RNG draw,
    keeping pools isolated instead of mixing them together."""
    auto_construct = False

    def test_retry_recovers_without_mixing(self):
        from unittest.mock import patch

        self.options = {
            "randomize_entrances": _ALL_CATEGORIES,
            "mix_entrances": [],  # everything isolated
            "coupled_entrances": False,
        }

        import entrance_rando
        from entrance_rando import EntranceRandomizationError

        call_count = {"n": 0}
        real_randomize = entrance_rando.randomize_entrances

        def flaky_randomize(*args, **kwargs):
            call_count["n"] += 1
            if call_count["n"] == 1:
                raise EntranceRandomizationError("simulated transient failure")
            return real_randomize(*args, **kwargs)

        with patch.object(entrance_rando, "randomize_entrances", flaky_randomize):
            self.world_setup(seed=1)

        self.assertGreaterEqual(call_count["n"], 2,
                                "Expected a retry after the transient failure")
        self.assertEqual(_orphan_er_entrances(self.world), [],
                         "ER entrances left unconnected after retry recovery")
        self.assertEqual(_count_cross_category(self.world), 0,
                         "Isolated pools were mixed despite a recoverable failure")


class ERDecoupledEmptyMixIsolationTest(PokemonCrystalTestBase):
    """Regression: decoupled + empty mix_entrances must produce fully isolated
    pools (the reported bug mixed everything when an isolated pool failed once)."""
    auto_construct = False

    def test_decoupled_empty_mix_stays_isolated(self):
        self.options = {
            "randomize_entrances": _ALL_CATEGORIES,
            "mix_entrances": [],
            "coupled_entrances": False,
        }
        for seed in range(1, 6):
            with self.subTest(seed=seed):
                self.world_setup(seed=seed)
                self.assertEqual(_orphan_er_entrances(self.world), [],
                                 "ER entrances left unconnected")
                self.assertEqual(_count_cross_category(self.world), 0,
                                 "decoupled empty mix produced cross-category pairings")


class ERCoupledEmptyMixSucceedsTest(PokemonCrystalTestBase):
    """Coupled + empty mix_entrances must always generate successfully with no orphaned
    entrances (retries then vanilla pinning guarantee completion)."""
    auto_construct = False

    def test_coupled_empty_mix_generates(self):
        self.options = {
            "randomize_entrances": _ALL_CATEGORIES,
            "mix_entrances": [],
            "coupled_entrances": True,
        }
        for seed in range(1, 6):
            with self.subTest(seed=seed):
                self.world_setup(seed=seed)
                self.assertEqual(_orphan_er_entrances(self.world), [],
                                 "ER entrances left unconnected")


class ERPlandoCrossPoolTest(PokemonCrystalTestBase):
    """A one-directional plando pairing crossing pools that cannot mix is unsatisfiable
    and must raise an OptionError naming the pairing."""
    auto_construct = False

    def test_cross_pool_pairing_fails_fast(self):
        self.options = {
            "randomize_entrances": _ALL_CATEGORIES,
            "mix_entrances": [],
            "coupled_entrances": False,
            "plando_connections": [{
                "entrance": "REGION_AZALEA_TOWN -> REGION_KURTS_HOUSE",  # Building
                "exit": "REGION_VIOLET_CITY -> REGION_VIOLET_GYM",       # Gym
                "direction": "entrance",
            }],
        }
        with self.assertRaises(Exception) as ctx:
            self.world_setup(seed=1)
        self.assertIn("Kurt's House Entrance", str(ctx.exception))
        self.assertIn("unsatisfiable", str(ctx.exception))

    def test_same_side_pairing_fails_fast(self):
        """Naming the door you come back out of instead of the one you walk into lands a
        Gym Entrance exit on a Gym Entrance stub. Same category, but the bipartition means
        that pool can only draw from the other side, so it is just as unsatisfiable."""
        self.options = {
            "randomize_entrances": _ALL_CATEGORIES,
            "mix_entrances": [],
            "coupled_entrances": False,
            "plando_connections": [{
                "entrance": "REGION_AZALEA_TOWN -> REGION_AZALEA_GYM",    # Gym Entrance
                "exit": "REGION_VIOLET_GYM -> REGION_VIOLET_CITY",        # arrives Gym Entrance
                "direction": "entrance",
            }],
        }
        with self.assertRaises(Exception) as ctx:
            self.world_setup(seed=1)
        self.assertIn("unsatisfiable", str(ctx.exception))

    def test_mixed_categories_are_not_a_crossing(self):
        """The same pairing is satisfiable once the two categories mix, so the check must
        read mix_entrances rather than rejecting every category crossing."""
        self.options = {
            "randomize_entrances": _ALL_CATEGORIES,
            "mix_entrances": _ALL_CATEGORIES,
            "coupled_entrances": False,
            "plando_connections": [{
                "entrance": "REGION_AZALEA_TOWN -> REGION_KURTS_HOUSE",  # Building
                "exit": "REGION_VIOLET_CITY -> REGION_VIOLET_GYM",       # Gym
                "direction": "entrance",
            }],
        }
        self.world_setup(seed=1)
        self.assertEqual(_orphan_er_entrances(self.world), [])
        self.assertIn("REGION_AZALEA_TOWN -> REGION_KURTS_HOUSE",
                      [src for src, _ in self.world.er_pairings])


class ERUnsolvableIsolationRaisesTest(PokemonCrystalTestBase):
    """When the requested grouping is genuinely unsolvable even with vanilla pins, ER
    must fail generation loudly rather than silently mixing categories together."""
    auto_construct = False

    def test_unsolvable_grouping_raises(self):
        from unittest.mock import patch

        self.options = {
            "randomize_entrances": _ALL_CATEGORIES,
            "mix_entrances": [],
            "coupled_entrances": False,
        }

        import entrance_rando
        from entrance_rando import EntranceRandomizationError
        import worlds.pokemon_crystal.world as crystal_world

        def always_fail(world, *, coupled, target_group_lookup, preserve_group_order):
            raise EntranceRandomizationError("forced failure")

        # Empty stranded set so pin rounds cannot make progress.
        with patch.object(entrance_rando, "randomize_entrances", always_fail), \
             patch.object(crystal_world.PokemonCrystalWorld,
                          "_find_unplaced_er_entrances", lambda self: set()), \
             self.assertRaises(Exception) as ctx:
            self.world_setup(seed=1)

        self.assertIn("Entrance randomization failed", str(ctx.exception))


class ERPodPreplacementTest(PokemonCrystalTestBase):
    """Coupled ER detects pods (contentless closed clusters) from the live region graph
    and pre-places them; every pre-placed pod must be paired both ways, in-category when
    its pool is isolated."""
    options = {
        "randomize_entrances": _ALL_CATEGORIES,
        "mix_entrances": [],
        "coupled_entrances": True,
    }

    def test_pods_detected(self):
        pods = self.world._er_pods
        reverse_lookup = build_reverse_conn_lookup(data.entrance_connections)
        self.assertIn("REGION_BLACKTHORN_CITY -> REGION_MOVE_DELETERS_HOUSE", pods.values())
        self.assertGreater(len(pods), 20)
        for interior, door in pods.items():
            self.assertEqual(reverse_lookup[door], interior)

    def test_pod_regions_have_no_locations(self):
        for door in self.world._er_pods.values():
            arrival = door.split(" -> ", 1)[1]
            self.assertFalse(self.world.get_region(arrival).locations,
                             f"pod region {arrival} has locations")

    def test_pod_pairings_in_category(self):
        conns = data.entrance_connections
        pairs = dict(self.world.er_pairings)
        placed = 0
        for interior in self.world._er_pods:
            if interior not in pairs:
                # Skipped by pre-placement (mixed group or plando).
                continue
            placed += 1
            partner = pairs[interior]
            self.assertEqual(base_category(conns[partner].category),
                             base_category(conns[interior].category),
                             f"pod {interior} paired outside its pool to {partner}")
            if base_category(conns[interior].category) in ER_BIPARTITE_CATEGORIES:
                self.assertNotEqual(_bipartite_side(conns[partner].category),
                                    _bipartite_side(conns[interior].category),
                                    f"pod {interior} paired to same-side {partner}")
            self.assertEqual(pairs[partner], interior, f"pod {interior} pairing not coupled")
        self.assertGreater(placed, 30, "pod pre-placement did not run")


class ERIsolatedPinFallbackTest(PokemonCrystalTestBase):
    """When isolated retries keep failing but pinning the stranded connections to vanilla
    lets the grouping balance, the ladder must recover there, keeping every pool
    isolated."""
    auto_construct = False

    def test_pin_fallback_keeps_isolation(self):
        import logging
        from unittest.mock import patch

        self.options = {
            "randomize_entrances": _ALL_CATEGORIES,
            "mix_entrances": [],
            "coupled_entrances": False,
        }

        import entrance_rando
        from entrance_rando import EntranceRandomizationError
        import worlds.pokemon_crystal.entrance_rando as crystal_er

        real_randomize = entrance_rando.randomize_entrances
        pool_size = {"n": None}

        # Fail while the pool is untouched; succeed once a pin round has shrunk it.
        def fail_until_pinned(world, *, coupled, target_group_lookup, preserve_group_order):
            if pool_size["n"] is None:
                pool_size["n"] = len(world.er_entrances)
            if len(world.er_entrances) == pool_size["n"]:
                raise EntranceRandomizationError("forced isolated failure")
            return real_randomize(world, coupled=coupled, target_group_lookup=target_group_lookup,
                                  preserve_group_order=preserve_group_order)

        with patch.object(entrance_rando, "randomize_entrances", fail_until_pinned), \
             self.assertLogs(logging.getLogger(crystal_er.__name__), level="WARNING") as log_ctx:
            self.world_setup(seed=1)

        log_text = "\n".join(log_ctx.output)
        self.assertIn("pin round", log_text, "Expected a vanilla pin round")
        self.assertEqual(_orphan_er_entrances(self.world), [],
                         "ER entrances left unconnected after pin fallback")
        self.assertEqual(_count_cross_category(self.world), 0,
                         "pin fallback must keep pools isolated")


_PLANDO_SOURCE = "REGION_AZALEA_TOWN -> REGION_AZALEA_GYM"
_PLANDO_ARRIVAL = "REGION_VIOLET_CITY -> REGION_VIOLET_GYM"


class ERPlandoResetBalanceTest(PokemonCrystalTestBase):
    """A plando pairing claims an ER target whose connection keeps its entrance in the pool
    (its exit still needs randomizing), and leaves behind a target whose entrance is gone
    from the pool. Reset rebuilt the first and dropped the second, so retries drifted out of
    balance and died at GER's count guard."""
    auto_construct = False

    def _setup(self, coupled: bool, direction: str):
        self.options = {
            "randomize_entrances": _ALL_CATEGORIES,
            "mix_entrances": [],
            "coupled_entrances": coupled,
            "plando_connections": [{
                "entrance": _PLANDO_SOURCE,
                "exit": _PLANDO_ARRIVAL,
                "direction": direction,
            }],
        }
        self.world_setup(seed=1)

    def test_generates_and_reset_keeps_the_pool_balanced(self):
        """Reset must neither resurrect a plando-claimed target nor lose the one the
        forced exit left behind."""
        for coupled, direction in ((True, "both"), (False, "entrance"), (False, "both")):
            with self.subTest(coupled=coupled, direction=direction):
                self._setup(coupled, direction)
                self.assertEqual(_orphan_er_entrances(self.world), [],
                                 "ER entrances left unconnected")
                self.assertIn(_PLANDO_SOURCE, [src for src, _ in self.world.er_pairings],
                              "forced pairing missing from er_pairings")
                self.assertTrue(self.world._plando_consumed_targets,
                                "expected plando to claim at least one target")
                for reset_round in range(2):
                    self.world._reset_er_entrances_to_vanilla()
                    _assert_pool_balanced(self, f"after reset {reset_round + 1}")

    def test_survives_a_transient_failure(self):
        """The first attempt failing forces a second pass through the reset path."""
        from unittest.mock import patch
        import entrance_rando
        from entrance_rando import EntranceRandomizationError

        calls = {"n": 0}
        real_randomize = entrance_rando.randomize_entrances

        def flaky_randomize(*args, **kwargs):
            calls["n"] += 1
            if calls["n"] == 1:
                raise EntranceRandomizationError("simulated transient failure")
            return real_randomize(*args, **kwargs)

        with patch.object(entrance_rando, "randomize_entrances", flaky_randomize):
            self._setup(coupled=False, direction="entrance")

        self.assertGreaterEqual(calls["n"], 2, "expected a retry after the transient failure")
        self.assertEqual(_orphan_er_entrances(self.world), [],
                         "ER entrances left unconnected after retry")

    def test_one_directional_is_promoted_to_both_when_coupled(self):
        """Coupling already forces the return trip, so a one-directional pairing is
        corrected to 'both' rather than left to strand half of itself in ER."""
        for direction in ("entrance", "exit"):
            with self.subTest(direction=direction):
                self.options = {
                    "randomize_entrances": ["Gym"],
                    "coupled_entrances": True,
                    "plando_connections": [{
                        "entrance": _PLANDO_SOURCE,
                        "exit": _PLANDO_ARRIVAL,
                        "direction": direction,
                    }],
                }
                self.world_setup(seed=1)
                self.assertEqual(
                    [c.direction for c in self.world.options.plando_connections.value],
                    ["both"])
                self.assertEqual(_orphan_er_entrances(self.world), [],
                                 "ER entrances left unconnected")

    def test_mirrored_pairings_written_by_hand_are_accepted(self):
        """Promotion to 'both' regenerates the pairing the player already spelled out in
        the other direction. The duplicate is identical, so it must not be a conflict."""
        self.options = {
            "randomize_entrances": ["Gym"],
            "coupled_entrances": True,
            "plando_connections": [
                {"entrance": _PLANDO_SOURCE, "exit": _PLANDO_ARRIVAL, "direction": "entrance"},
                {"entrance": "REGION_VIOLET_GYM -> REGION_VIOLET_CITY",
                 "exit": "REGION_AZALEA_GYM -> REGION_AZALEA_TOWN", "direction": "entrance"},
            ],
        }
        self.world_setup(seed=1)
        sources = [src for src, _ in self.world.er_pairings]
        self.assertIn(_PLANDO_SOURCE, sources)
        self.assertIn("REGION_VIOLET_GYM -> REGION_VIOLET_CITY", sources)
        self.assertEqual(_orphan_er_entrances(self.world), [])


class ERPlandoPoolAccountingTest(PokemonCrystalTestBase):
    """Plando mutates the ER pool outside er_entrances, so every path that rebuilds or
    shrinks the pool has to agree with it. Each case here previously desynced the free
    exit and free target counts, which GER rejects outright."""
    auto_construct = False

    def _setup(self, categories, coupled, plando, seed=1):
        self.options = {
            "randomize_entrances": categories,
            "mix_entrances": [],
            "coupled_entrances": coupled,
            "plando_connections": plando,
        }
        self.world_setup(seed=seed)

    def test_skipped_pairing_does_not_claim_a_target(self):
        """A pairing naming a connection outside randomize_entrances is skipped with a
        warning, so it consumes nothing and reset must keep rebuilding that target."""
        self._setup(["Gym"], True, [{
            "entrance": "REGION_AZALEA_TOWN -> REGION_KURTS_HOUSE",  # Building, not randomized
            "exit": "REGION_VIOLET_CITY -> REGION_VIOLET_GYM",
            "direction": "both",
        }], seed=7)
        self.assertEqual(self.world._plando_consumed_targets, set())
        self.assertEqual(_orphan_er_entrances(self.world), [])
        self.assertGreater(len(self.world.er_pairings), 30,
                           "Gym shuffle collapsed to vanilla")

    def test_one_way_source_keeps_its_target_stub(self):
        """A one-way source's target lives in the child region under a suffixed name.
        Its entrance leaves er_entrances, so reset has to rebuild the stub from the
        orphan record or the pool loses a target the first time an attempt claims it."""
        # seed 1: this configuration shuffles fully on stage 1; the >800 guard below is
        # only meaningful without a legitimate pin-fallback recovery shrinking the pool.
        self._setup(_ALL_CATEGORIES, True, [{
            "entrance": "REGION_OLIVINE_LIGHTHOUSE_6F -> REGION_OLIVINE_LIGHTHOUSE_5F",
            "exit": "REGION_BLACKTHORN_GYM_2F -> REGION_BLACKTHORN_GYM_1F:HOLE_1",
            "direction": "both",
        }], seed=1)
        orphan_names = [orphan.name for orphan in self.world._plando_orphan_targets]
        self.assertIn("REGION_OLIVINE_LIGHTHOUSE_6F -> REGION_OLIVINE_LIGHTHOUSE_5F (one-way target)",
                      orphan_names)
        for reset_round in range(2):
            self.world._reset_er_entrances_to_vanilla()
            _assert_pool_balanced(self, f"after reset {reset_round + 1}")
        self.assertGreater(len(self.world.er_pairings), 800,
                           "entrance shuffle collapsed to vanilla")

    def test_pinning_a_consumed_targets_owner_keeps_the_pool_balanced(self):
        """Pinning retires an exit and its target stub together, but plando already took
        that stub. Such a connection has to be left unpinned."""
        consumed_owner = "REGION_VIOLET_GYM -> REGION_VIOLET_CITY"
        self._setup(_ALL_CATEGORIES, False, [{
            "entrance": _PLANDO_SOURCE,
            "exit": _PLANDO_ARRIVAL,
            "direction": "entrance",
        }])
        self.assertIn(consumed_owner, self.world._plando_consumed_targets)

        self.world._reset_er_entrances_to_vanilla()
        _assert_pool_balanced(self, "before pinning")
        self.world._pin_connections_to_vanilla({consumed_owner})
        _assert_pool_balanced(self, "after pinning")
        self.world._reset_er_entrances_to_vanilla()
        _assert_pool_balanced(self, "after the reset that follows pinning")

    def test_balanced_plando_keeps_its_bipartite_pool_isolated(self):
        """One uncoupled pairing takes a Gym Exit target and leaves a Gym Entrance orphan
        behind, so both halves of the Gym pool stay even and isolation survives."""
        self._setup(_ALL_CATEGORIES, False, [{
            "entrance": "REGION_AZALEA_TOWN -> REGION_AZALEA_GYM",
            "exit": "REGION_VIOLET_CITY -> REGION_VIOLET_GYM", "direction": "entrance",
        }], seed=5)
        self.assertEqual(_orphan_er_entrances(self.world), [])
        self.assertGreater(len(self.world.er_pairings), 800,
                           "entrance shuffle collapsed to vanilla")
        self.assertEqual(_count_cross_category(self.world), 0,
                         "isolation was lost to the mixed-pool fallback")
        self.assertEqual(_same_side_pairings(self.world), [])

    def test_plando_skewing_one_side_of_a_pool_is_rejected(self):
        """The second pairing sends a Gym Exit source at another Gym Exit stub, leaving
        that half of the pool one short with no way to rebalance. Rejected up front rather
        than burning ten pin rounds and failing generation with a wall of pinned names."""
        with self.assertRaises(Exception) as ctx:
            self._setup(_ALL_CATEGORIES, False, [
                {"entrance": "REGION_AZALEA_TOWN -> REGION_AZALEA_GYM",
                 "exit": "REGION_VIOLET_CITY -> REGION_VIOLET_GYM", "direction": "entrance"},
                {"entrance": "REGION_AZALEA_GYM -> REGION_AZALEA_TOWN",
                 "exit": "REGION_ECRUTEAK_CITY -> REGION_ECRUTEAK_GYM", "direction": "entrance"},
            ], seed=5)
        self.assertIn("Azalea Gym Exit", str(ctx.exception))
        self.assertIn("unsatisfiable", str(ctx.exception))
