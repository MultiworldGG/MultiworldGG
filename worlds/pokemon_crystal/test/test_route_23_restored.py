from .bases import PokemonCrystalTestBase


class Route23RestoredOffTest(PokemonCrystalTestBase):
    options = {
        "route_23_restored": "off",
        "randomize_hidden_items": "on",
        "randomize_berry_trees": "on",
    }

    def test_regions_excluded(self):
        region_names = {r.name for r in self.multiworld.get_regions(self.player)}
        self.assertNotIn("REGION_ROUTE_23_RESTORED:SOUTH", region_names)
        self.assertNotIn("REGION_ROUTE_23_RESTORED:NORTH", region_names)
        self.assertNotIn("REGION_ROUTE_23_RESTORED:SURF", region_names)

    def test_locations_absent(self):
        location_names = {loc.name for loc in self.multiworld.get_locations(self.player)}
        self.assertNotIn("Route 23 - Hidden Item in Bush", location_names)
        self.assertNotIn("Route 23 - Hidden Item on Island", location_names)
        self.assertNotIn("Route 23 - Berry Tree", location_names)


class Route23RestoredOnTest(PokemonCrystalTestBase):
    options = {
        "route_23_restored": "on",
        "randomize_hidden_items": "on",
        "randomize_berry_trees": "on",
    }

    def test_regions_included(self):
        region_names = {r.name for r in self.multiworld.get_regions(self.player)}
        self.assertIn("REGION_ROUTE_23_RESTORED:SOUTH", region_names)
        self.assertIn("REGION_ROUTE_23_RESTORED:NORTH", region_names)
        self.assertIn("REGION_ROUTE_23_RESTORED:SURF", region_names)

    def test_vanilla_edge_removed(self):
        for region in self.multiworld.get_regions(self.player):
            for exit_ in region.exits:
                self.assertNotEqual(
                    exit_.name,
                    "REGION_VICTORY_ROAD:1F:ENTRANCE -> REGION_VICTORY_ROAD_GATE:NORTH",
                )
                self.assertNotEqual(
                    exit_.name,
                    "REGION_VICTORY_ROAD_GATE:NORTH -> REGION_VICTORY_ROAD:1F:ENTRANCE",
                )

    def test_locations_present(self):
        location_names = {loc.name for loc in self.multiworld.get_locations(self.player)}
        self.assertIn("Route 23 - Hidden Item in Bush", location_names)
        self.assertIn("Route 23 - Hidden Item on Island", location_names)
        self.assertIn("Route 23 - Berry Tree", location_names)

    def test_beatable(self):
        self.collect_all_but(["EVENT_BEAT_ELITE_FOUR"])
        self.assertBeatable(True)


class Route23RestoredEntranceRandoTest(PokemonCrystalTestBase):
    options = {
        "route_23_restored": "on",
        "randomize_entrances": ["Dungeon"],
    }

    def test_r23r_entrances_two_way(self):
        from ..data import data
        for name in (
            "REGION_ROUTE_23_RESTORED:NORTH -> REGION_VICTORY_ROAD:1F:ENTRANCE",
            "REGION_ROUTE_23_RESTORED:SOUTH -> REGION_VICTORY_ROAD_GATE:NORTH",
            "REGION_VICTORY_ROAD:1F:ENTRANCE -> REGION_ROUTE_23_RESTORED:NORTH",
            "REGION_VICTORY_ROAD_GATE:NORTH -> REGION_ROUTE_23_RESTORED:SOUTH",
        ):
            self.assertIn(name, data.entrance_connections)
            self.assertFalse(data.entrance_connections[name].one_way, f"{name} should be two-way")

    def test_beatable(self):
        self.collect_all_but(["EVENT_BEAT_ELITE_FOUR"])
        self.assertBeatable(True)


class Route23RestoredUnownHuntTest(PokemonCrystalTestBase):
    options = {
        "route_23_restored": "on",
        "goal": ["Unown Hunt"],
    }

    def test_world_generates(self):
        self.assertTrue(self.multiworld.get_regions(self.player))


class Route23RestoredJohtoOnlyTest(PokemonCrystalTestBase):
    options = {
        "route_23_restored": "on",
        "johto_only": "on",
    }

    def test_regions_included(self):
        region_names = {r.name for r in self.multiworld.get_regions(self.player)}
        self.assertIn("REGION_ROUTE_23_RESTORED:SOUTH", region_names)


class Route23RestoredSuppressWildsTest(PokemonCrystalTestBase):
    auto_construct = False

    def test_wild_table_labels_present(self):
        from ..data import data
        self.assertIn("AP_WildGrass_ROUTE_23_RESTORED", data.rom_addresses)
        self.assertIn("AP_WildWater_ROUTE_23_RESTORED", data.rom_addresses)


class Route23RestoredGrasssanityTest(PokemonCrystalTestBase):
    options = {
        "route_23_restored": "on",
        "grasssanity": "full",
    }

    def test_grass_tiles_present(self):
        from ..data import data
        self.assertIn("REGION_ROUTE_23_RESTORED:NORTH", data.grass_tiles)
        self.assertEqual(len(data.grass_tiles["REGION_ROUTE_23_RESTORED:NORTH"]), 64)

    def test_grass_locations_created(self):
        location_names = {loc.name for loc in self.multiworld.get_locations(self.player)}
        r23r_grass = {name for name in location_names if name.startswith("Route 23 - Grass")}
        self.assertEqual(len(r23r_grass), 64)
