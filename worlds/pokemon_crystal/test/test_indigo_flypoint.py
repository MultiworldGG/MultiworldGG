from .bases import PokemonCrystalTestBase


class IndigoFlyRegionRegisteredTest(PokemonCrystalTestBase):
    options = {}

    def test_indigo_in_fly_regions(self):
        from ..data import data
        indigo = next((fr for fr in data.fly_regions if fr.name == "Indigo Plateau"), None)
        self.assertIsNotNone(indigo)
        self.assertEqual(indigo.id, 23)
        self.assertEqual(indigo.base_identifier, "INDIGO")
        self.assertEqual(indigo.unlock_region, "REGION_ROUTE_23")
        self.assertEqual(indigo.exit_region, "REGION_ROUTE_23")
        self.assertTrue(indigo.johto)


class IndigoFlyUnlockTest(PokemonCrystalTestBase):
    options = {
        "randomize_fly_unlocks": "on",
    }

    def test_visit_location_exists_on_route_23(self):
        location = self.multiworld.get_location("Visit Indigo Plateau", self.player)
        self.assertEqual(location.parent_region.name, "REGION_ROUTE_23")

    def test_fly_item_exists(self):
        item_names = {item.name for item in self.multiworld.get_items()
                      if item.player == self.player}
        self.assertIn("Fly Indigo Plateau", item_names)


class IndigoFlyUnlockJohtoOnlyTest(PokemonCrystalTestBase):
    options = {
        "johto_only": "on",
        "randomize_fly_unlocks": "on",
    }

    def test_visit_location_exists_on_route_23(self):
        location = self.multiworld.get_location("Visit Indigo Plateau", self.player)
        self.assertEqual(location.parent_region.name, "REGION_ROUTE_23")

    def test_fly_item_exists(self):
        item_names = {item.name for item in self.multiworld.get_items()
                      if item.player == self.player}
        self.assertIn("Fly Indigo Plateau", item_names)

    def test_no_kanto_fly_unlocks(self):
        item_names = {item.name for item in self.multiworld.get_items()
                      if item.player == self.player}
        self.assertNotIn("Fly Pallet Town", item_names)
        self.assertNotIn("Fly Viridian City", item_names)


class IndigoFlyUnlockVanillaJohtoOnlyTest(PokemonCrystalTestBase):
    options = {
        "johto_only": "on",
    }

    def test_fly_hub_edge_requires_visit(self):
        entrance = self.multiworld.get_entrance("REGION_FLY -> REGION_ROUTE_23", self.player)
        empty_state = self.multiworld.state.copy()
        for player_items in empty_state.prog_items.values():
            player_items.clear()
        self.assertFalse(entrance.access_rule(empty_state))

    def test_visit_event_exists(self):
        location = self.multiworld.get_location("EVENT_VISITED_INDIGO", self.player)
        self.assertEqual(location.parent_region.name, "REGION_ROUTE_23")


class IndigoFlyDestinationsTest(PokemonCrystalTestBase):
    options = {
        "randomize_fly_destinations": "on",
    }

    def test_all_23_slots_populated(self):
        self.assertEqual(len(self.world.fly_destinations), 23)


class IndigoFlyDestinationsJohtoOnlyTest(PokemonCrystalTestBase):
    options = {
        "johto_only": "on",
        "randomize_fly_destinations": "on",
        "free_fly_location": "free_fly_and_map_card",
    }

    def test_free_fly_within_slots(self):
        from ..fly import fly_flag_index
        for fly_location in (self.world.free_fly_location, self.world.map_card_fly_location):
            self.assertLess(fly_flag_index(self.world, fly_location), len(self.world.fly_destinations))

    def test_slots_stay_contiguous(self):
        from ..fly import get_fly_regions
        from ..data import data
        fly_regions = get_fly_regions(self.world)
        self.assertEqual(len(self.world.fly_destinations), len(fly_regions))
        # Johto is contiguous, up until Indigo which is last
        self.assertEqual([fr.id for fr in fly_regions], list(range(1, len(fly_regions))) +
                                                            [max(fr.id for fr in data.fly_regions)])


class IndigoBlocklistAcceptsIndigoTest(PokemonCrystalTestBase):
    options = {
        "free_fly_location": "free_fly",
        "free_fly_blocklist": ["Indigo Plateau"],
    }

    def test_blocklist_accepts_indigo(self):
        self.assertNotEqual(self.world.free_fly_location.name, "Indigo Plateau")


class IndigoFlyRegionNameValidForBlocklistTest(PokemonCrystalTestBase):
    options = {}

    def test_indigo_in_blocklist_valid_keys(self):
        from ..options import FlyLocationBlocklist
        self.assertIn("Indigo Plateau", FlyLocationBlocklist.valid_keys)
