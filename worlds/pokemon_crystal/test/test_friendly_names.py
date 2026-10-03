from .bases import PokemonCrystalTestBase
from ..data import data, FRIENDLY_CONNECTION_NAMES, FRIENDLY_CONNECTION_NAME_OVERRIDES, \
    friendly_entrance_name, internal_entrance_name

# Edges regions.py synthesizes with default names rather than reading from regions.json.
_SYNTHESIZED_EDGES = {
    "REGION_ROUTE_42:WEST -> REGION_ROUTE_42:CENTER",
    "REGION_ROUTE_42:CENTER -> REGION_ROUTE_42:WEST",
    "REGION_ROUTE_42:EAST -> REGION_ROUTE_42:CENTER",
    "REGION_ROUTE_42:CENTER -> REGION_ROUTE_42:EAST",
    "REGION_DARK_CAVE_BLACKTHORN_ENTRANCE:SOUTHWEST -> REGION_DARK_CAVE_BLACKTHORN_ENTRANCE:NORTHWEST",
}


class FriendlyConnectionNamesTest(PokemonCrystalTestBase):
    """Verify friendly_connection_names.json invariants without generating a world."""
    auto_construct = False

    def test_every_connection_has_friendly_name(self):
        missing = [name for name in data.entrance_connections if name not in FRIENDLY_CONNECTION_NAMES]
        self.assertEqual(missing, [], f"Connections without a friendly name: {missing}")

    def test_friendly_names_unique(self):
        # Case-insensitive: the plando lookup map is keyed lowercase.
        seen: dict[str, str] = {}
        for internal, friendly in FRIENDLY_CONNECTION_NAMES.items():
            self.assertNotIn(friendly.lower(), seen,
                             f"Friendly name {friendly!r} used by both {seen.get(friendly.lower())!r} "
                             f"and {internal!r}")
            seen[friendly.lower()] = internal

    def test_every_friendly_key_is_real_edge(self):
        edges = {f"{name} -> {region_exit}"
                 for name, region in data.regions.items() for region_exit in region.exits}
        orphans = set(FRIENDLY_CONNECTION_NAMES) - edges - set(data.entrance_connections) - _SYNTHESIZED_EDGES
        self.assertEqual(orphans, set(), f"Friendly name keys that match no region edge: {sorted(orphans)}")

    def test_names_round_trip(self):
        for internal in data.entrance_connections:
            self.assertEqual(internal_entrance_name(friendly_entrance_name(internal)), internal)
        self.assertEqual(friendly_entrance_name("Fly"), "Fly")
        self.assertEqual(internal_entrance_name("Fly"), "Fly")

    def test_case_insensitive_resolution(self):
        # PlandoConnections validation lowercases names, so resolution must match.
        internal = "REGION_AZALEA_TOWN -> REGION_AZALEA_GYM"
        self.assertEqual(internal_entrance_name("azalea gym entrance"), internal)
        self.assertEqual(internal_entrance_name("AZALEA GYM ENTRANCE"), internal)
        self.assertEqual(internal_entrance_name(internal.lower()), internal)

    def test_no_collision_with_generated_names(self):
        all_names = set(FRIENDLY_CONNECTION_NAMES.values())
        for columns in FRIENDLY_CONNECTION_NAME_OVERRIDES.values():
            for overrides in columns.values():
                all_names |= set(overrides.values())
        generated = {f"Fly to {fr.name}" for fr in data.fly_regions}
        generated |= {f"Start in {town.name}" for town in data.starting_towns}
        self.assertEqual(all_names & generated, set())
        for name in all_names:
            self.assertFalse(name.startswith(("Free Fly to ", "Fly Destination ", "Fly Slot ")), name)
            self.assertNotIn(" Flypoint (", name)

    def test_one_way_suffix_round_trip(self):
        internal = next(iter(data.entrance_connections))
        suffixed = f"{internal} (one-way target)"
        friendly = friendly_entrance_name(suffixed)
        self.assertTrue(friendly.endswith(" (one-way target)"))
        self.assertEqual(internal_entrance_name(friendly), suffixed)

    def test_override_keys_are_real_edges(self):
        edges = {f"{name} -> {region_exit}"
                 for name, region in data.regions.items() for region_exit in region.exits}
        edges |= _SYNTHESIZED_EDGES
        for group, columns in FRIENDLY_CONNECTION_NAME_OVERRIDES.items():
            for column, overrides in columns.items():
                orphans = set(overrides) - edges
                self.assertEqual(orphans, set(), f"{group}/{column}: unknown connections {sorted(orphans)}")

    def test_override_groups_are_real_options(self):
        from ..options import PokemonCrystalOptions
        type_hints = PokemonCrystalOptions.type_hints
        for option_name, columns in FRIENDLY_CONNECTION_NAME_OVERRIDES.items():
            self.assertIn(option_name, type_hints, f"{option_name} is not a world option")
            valid_values = set(type_hints[option_name].name_lookup.values())
            unknown = set(columns) - valid_values
            self.assertEqual(unknown, set(), f"{option_name}: invalid value keys {sorted(unknown)}")

    def test_override_columns_cover_same_connections(self):
        for group, columns in FRIENDLY_CONNECTION_NAME_OVERRIDES.items():
            key_sets = {column: set(overrides) for column, overrides in columns.items()}
            first_column, first_keys = next(iter(key_sets.items()))
            for column, keys in key_sets.items():
                self.assertEqual(keys, first_keys, f"{group}: {column} names different connections "
                                                   f"than {first_column}")

    def test_override_names_unique_across_connections(self):
        # Case-insensitive: the plando lookup map is keyed lowercase.
        seen = {name.lower(): conn for conn, name in FRIENDLY_CONNECTION_NAMES.items()}
        for columns in FRIENDLY_CONNECTION_NAME_OVERRIDES.values():
            for overrides in columns.values():
                for conn, name in overrides.items():
                    self.assertEqual(seen.setdefault(name.lower(), conn), conn,
                                     f"{name!r} used by both {seen[name.lower()]!r} and {conn!r}")

    def test_no_friendly_name_shadows_internal(self):
        # Internal-name identity entries win in the lowercase lookup map; a friendly
        # name matching one would silently stop resolving.
        internal_lower = {conn.lower() for conn in FRIENDLY_CONNECTION_NAMES}
        internal_lower |= {conn.lower() for conn in data.entrance_connections}
        all_names = set(FRIENDLY_CONNECTION_NAMES.values())
        for columns in FRIENDLY_CONNECTION_NAME_OVERRIDES.values():
            for overrides in columns.values():
                all_names |= set(overrides.values())
        shadowed = {name for name in all_names if name.lower() in internal_lower}
        self.assertEqual(shadowed, set())


class FriendlyEntranceRenameTest(PokemonCrystalTestBase):
    """The post-generation rename pass swaps entrance names to friendly ones and keeps
    the internal name resolvable as a cache alias."""
    options = {
        "randomize_entrances": ["Gym", "Gym Interior"],
        "coupled_entrances": True,
    }

    def test_rename_pass(self):
        internal = "REGION_AZALEA_TOWN -> REGION_AZALEA_GYM"
        friendly = friendly_entrance_name(internal)
        self.assertEqual(friendly, "Azalea Gym Entrance")

        # Test gen stops before post_fill, so names are still internal here.
        entrance = self.multiworld.get_entrance(internal, self.player)
        self.assertEqual(entrance.name, internal)

        self.world.post_fill()
        self.assertEqual(entrance.name, friendly)
        # Both names resolve to the same entrance.
        self.assertIs(self.multiworld.get_entrance(friendly, self.player), entrance)
        self.assertIs(self.multiworld.get_entrance(internal, self.player), entrance)
        # Unmapped names (synthetic edges) are untouched.
        self.assertEqual(self.multiworld.get_entrance("Fly", self.player).name, "Fly")

        # Generated fly-system names.
        fly_dest = self.multiworld.get_entrance("REGION_FLY -> REGION_ECRUTEAK_CITY", self.player)
        self.assertEqual(fly_dest.name, "Fly to Ecruteak City")
        flypoint = self.multiworld.get_entrance(
            "REGION_MAHOGANY_TOWN:EAST -> REGION_MAHOGANY_TOWN:FLY", self.player)
        self.assertEqual(flypoint.name, "Mahogany Town Flypoint (Mahogany Town East)")

        # A second pass is a no-op.
        self.world.post_fill()
        self.assertEqual(entrance.name, friendly)

    def test_names_unique_post_rename(self):
        from collections import Counter
        self.world.post_fill()
        # get_entrances yields renamed entrances under both cache keys; dedupe by object.
        entrances = {id(e): e for e in self.multiworld.get_entrances(self.player)}.values()
        counts = Counter(e.name for e in entrances)
        dupes = {name: n for name, n in counts.items() if n > 1}
        self.assertEqual(dupes, {})


class FriendlyPlandoTest(PokemonCrystalTestBase):
    """Plando accepts friendly names case-insensitively (option validation lowercases)."""
    options = {
        "randomize_entrances": ["Gym", "Gym Interior"],
        "coupled_entrances": True,
        "plando_connections": [{
            "entrance": "azalea gym entrance",
            "exit": "VIOLET GYM ENTRANCE",
            "direction": "both",
        }],
    }

    def test_friendly_plando_applied(self):
        pairings = dict(self.world.er_pairings)
        self.assertEqual(pairings["REGION_AZALEA_TOWN -> REGION_AZALEA_GYM"],
                         "REGION_VIOLET_GYM -> REGION_VIOLET_CITY")


class FlyDestinationRandoNameTest(PokemonCrystalTestBase):
    options = {"randomize_fly_destinations": "true"}

    def test_fly_slot_named(self):
        self.world.post_fill()
        entrance = self.multiworld.get_entrance("Fly Destination 1", self.player)
        self.assertRegex(entrance.name, r"^Fly Slot 1 \(.+\)$")
        self.assertIs(self.multiworld.get_entrance(entrance.name, self.player), entrance)


class StartingTownNameTest(PokemonCrystalTestBase):
    options = {"randomize_starting_town": "true"}

    def test_start_edge_named(self):
        self.world.post_fill()
        town = self.world.starting_town
        entrance = self.multiworld.get_entrance(f"Menu -> {town.region_id}", self.player)
        self.assertEqual(entrance.name, f"Start in {town.name}")


class EliteFourSkipNameTest(PokemonCrystalTestBase):
    options = {"skip_elite_four": "true"}

    def test_skip_edge_named(self):
        self.world.post_fill()
        entrance = self.multiworld.get_entrance(
            "REGION_INDIGO_PLATEAU_POKECENTER_1F:E4_GATE -> REGION_LANCES_ROOM", self.player)
        self.assertEqual(entrance.name, "Indigo Plateau Elite Four Skip")


class OptionConditionalNamesDefaultTest(PokemonCrystalTestBase):
    options = {}

    def test_default_option_names(self):
        overrides = self.world._friendly_name_overrides()
        # Every override group resolved into the merged dict.
        expected = {conn for columns in FRIENDLY_CONNECTION_NAME_OVERRIDES.values()
                    for overrides_ in columns.values() for conn in overrides_}
        self.assertEqual(set(overrides), expected)

        self.world.post_fill()
        ilex = self.multiworld.get_entrance("REGION_ILEX_FOREST:NORTH -> REGION_ILEX_FOREST:SOUTH", self.player)
        self.assertEqual(ilex.name, "Ilex Forest Cut Passage (Southbound)")
        route_42 = self.multiworld.get_entrance("REGION_ROUTE_42:WEST -> REGION_ROUTE_42:CENTER", self.player)
        self.assertEqual(route_42.name, "Route 42 Water Crossing (West -> Center)")


class OptionConditionalNamesVariantTest(PokemonCrystalTestBase):
    options = {
        "remove_ilex_cut_tree": "true",
        "route_42_access": "whirlpool",
        "victory_road_strength": "true",
        "blackthorn_dark_cave_access": "waterfall",
    }

    def test_variant_option_names(self):
        self.world.post_fill()
        ilex = self.multiworld.get_entrance("REGION_ILEX_FOREST:NORTH -> REGION_ILEX_FOREST:SOUTH", self.player)
        self.assertEqual(ilex.name, "Ilex Forest Traversal (Southbound)")
        route_42 = self.multiworld.get_entrance("REGION_ROUTE_42:WEST -> REGION_ROUTE_42:CENTER", self.player)
        self.assertEqual(route_42.name, "Route 42 Whirlpool Crossing (West -> Center)")
        victory_road = self.multiworld.get_entrance(
            "REGION_VICTORY_ROAD:1F:ENTRANCE -> REGION_VICTORY_ROAD:1F", self.player)
        self.assertEqual(victory_road.name, "Victory Road 1F Strength Passage (Northbound)")
        # The waterfall-only edge is synthesized in regions.py, not regions.json.
        dark_cave = self.multiworld.get_entrance(
            "REGION_DARK_CAVE_BLACKTHORN_ENTRANCE:SOUTHWEST -> REGION_DARK_CAVE_BLACKTHORN_ENTRANCE:NORTHWEST",
            self.player)
        self.assertEqual(dark_cave.name, "Dark Cave (Blackthorn Side) Traversal (Southwest -> Northwest)")
