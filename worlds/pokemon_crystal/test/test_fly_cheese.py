from .bases import PokemonCrystalTestBase
from ..data import data


def _clear_state(test):
    empty_state = test.multiworld.state.copy()
    for player_items in empty_state.prog_items.values():
        player_items.clear()
    return empty_state


class FlyCheeseVanillaTest(PokemonCrystalTestBase):
    options = {}

    def test_fly_hub_edge_exists(self):
        entrance = self.multiworld.get_entrance("REGION_FLY -> REGION_LAKE_OF_RAGE", self.player)
        self.assertEqual(entrance.parent_region.name, "REGION_FLY")
        self.assertEqual(entrance.connected_region.name, "REGION_LAKE_OF_RAGE")

    def test_fly_to_town_requires_visit(self):
        entrance = self.multiworld.get_entrance("REGION_FLY -> REGION_LAKE_OF_RAGE", self.player)
        self.assertFalse(entrance.access_rule(_clear_state(self)))

    def test_all_fly_regions_have_hub_edge(self):
        region_names = {r.name for r in self.multiworld.get_regions(self.player)}
        entrance_names = {e.name for r in self.multiworld.get_regions(self.player) for e in r.exits}
        for fr in data.fly_regions:
            if fr.exit_region not in region_names:
                continue
            self.assertIn(f"REGION_FLY -> {fr.exit_region}", entrance_names,
                          f"Missing fly hub edge for {fr.name}")

    def test_unlock_source_edges_exist(self):
        region_names = {r.name for r in self.multiworld.get_regions(self.player)}
        entrance_names = {e.name for r in self.multiworld.get_regions(self.player) for e in r.exits}
        for fr in data.fly_regions:
            if fr.unlock_region not in region_names:
                continue
            for src in fr.unlock_sources:
                if src not in region_names:
                    continue
                self.assertIn(f"{src} -> {fr.unlock_region}", entrance_names,
                              f"Missing unlock-source edge {src} -> {fr.unlock_region}")


class VermilionFlyEntryPointsTest(PokemonCrystalTestBase):
    options = {}

    def test_extra_unlock_edges_exist(self):
        entrance_names = {e.name for r in self.multiworld.get_regions(self.player) for e in r.exits}
        self.assertIn("REGION_ROUTE_11 -> REGION_VERMILION_CITY:FLY", entrance_names)
        self.assertIn("REGION_VERMILION_CITY:DIGLETTS_CAVE_ENTRANCE -> REGION_VERMILION_CITY:FLY",
                      entrance_names)

    def test_fly_into_town_requires_visit(self):
        entrance = self.multiworld.get_entrance("REGION_FLY -> REGION_VERMILION_CITY", self.player)
        self.assertFalse(entrance.access_rule(_clear_state(self)))


class VermilionFlyEntryPointsJohtoOnlyTest(PokemonCrystalTestBase):
    options = {
        "johto_only": "on",
    }

    def test_no_kanto_unlock_edges(self):
        entrance_names = {e.name for r in self.multiworld.get_regions(self.player) for e in r.exits}
        self.assertNotIn("REGION_ROUTE_11 -> REGION_VERMILION_CITY:FLY", entrance_names)
        self.assertNotIn("REGION_VERMILION_CITY:DIGLETTS_CAVE_ENTRANCE -> REGION_VERMILION_CITY:FLY",
                         entrance_names)


class MahoganyEastRegionTest(PokemonCrystalTestBase):
    options = {}

    def test_east_region_links(self):
        region_names = {r.name for r in self.multiworld.get_regions(self.player)}
        self.assertIn("REGION_MAHOGANY_TOWN:EAST", region_names)
        entrance_names = {e.name for r in self.multiworld.get_regions(self.player) for e in r.exits}
        self.assertIn("REGION_MAHOGANY_TOWN:EAST -> REGION_ROUTE_44", entrance_names)
        self.assertIn("REGION_MAHOGANY_TOWN:EAST -> REGION_MAHOGANY_RED_GYARADOS_SPEECH_HOUSE",
                      entrance_names)
        self.assertIn("REGION_MAHOGANY_TOWN:EAST -> REGION_MAHOGANY_TOWN:FLY", entrance_names)

    def test_salesman_gate_both_directions(self):
        empty_state = _clear_state(self)
        for name in ("REGION_MAHOGANY_TOWN -> REGION_MAHOGANY_TOWN:EAST",
                     "REGION_MAHOGANY_TOWN:EAST -> REGION_MAHOGANY_TOWN"):
            entrance = self.multiworld.get_entrance(name, self.player)
            self.assertFalse(entrance.access_rule(empty_state))

    def test_route_44_into_east_is_free(self):
        entrance = self.multiworld.get_entrance("REGION_ROUTE_44 -> REGION_MAHOGANY_TOWN:EAST", self.player)
        self.assertTrue(entrance.access_rule(_clear_state(self)))


class RemoteFlyUnlocksVanillaTest(PokemonCrystalTestBase):
    options = {
        "remote_items": "true",
    }

    def test_no_visit_locations(self):
        location_names = {loc.name for loc in self.multiworld.get_locations(self.player)}
        for fr in data.fly_regions:
            self.assertNotIn(f"Visit {fr.name}", location_names)


class FlyCheeseDestinationRandomTest(PokemonCrystalTestBase):
    options = {
        "randomize_fly_destinations": "on",
    }

    def test_destination_edges_replace_hub_edges(self):
        entrance_names = {e.name for r in self.multiworld.get_regions(self.player) for e in r.exits}
        self.assertIn("Fly Destination 1", entrance_names)
        for fr in data.fly_regions:
            self.assertNotIn(f"REGION_FLY -> {fr.exit_region}", entrance_names)
