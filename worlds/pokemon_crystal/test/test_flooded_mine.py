from .bases import PokemonCrystalTestBase


class FloodedMineOffTest(PokemonCrystalTestBase):
    options = {
        "flooded_mine": "off",
        "randomize_hidden_items": "on",
    }

    def test_regions_excluded(self):
        region_names = {r.name for r in self.multiworld.get_regions(self.player)}
        self.assertNotIn("REGION_FLOODED_MINE", region_names)
        self.assertNotIn("REGION_FLOODED_MINE:NORTH_ENTRANCE", region_names)
        self.assertNotIn("REGION_FLOODED_MINE:SOUTH_ENTRANCE", region_names)
        self.assertNotIn("REGION_CHERRYGROVE_CITY:FLOODED_MINE_ENTRANCE", region_names)

    def test_locations_absent(self):
        location_names = {loc.name for loc in self.multiworld.get_locations(self.player)}
        self.assertNotIn("Flooded Mine - Item", location_names)
        self.assertNotIn("Flooded Mine - Hidden Item Near Cherrygrove Entrance", location_names)
        self.assertNotIn("Flooded Mine - Hidden Item Southeast", location_names)
        self.assertNotIn("Flooded Mine - Hidden Item Northwest", location_names)


class FloodedMineOnTest(PokemonCrystalTestBase):
    options = {
        "flooded_mine": "on",
        "randomize_hidden_items": "on",
    }

    def test_regions_included(self):
        region_names = {r.name for r in self.multiworld.get_regions(self.player)}
        self.assertIn("REGION_FLOODED_MINE", region_names)
        self.assertIn("REGION_FLOODED_MINE:NORTH_ENTRANCE", region_names)
        self.assertIn("REGION_FLOODED_MINE:SOUTH_ENTRANCE", region_names)
        self.assertIn("REGION_CHERRYGROVE_CITY:FLOODED_MINE_ENTRANCE", region_names)

    def test_locations_present(self):
        location_names = {loc.name for loc in self.multiworld.get_locations(self.player)}
        self.assertIn("Flooded Mine - Item", location_names)
        self.assertIn("Flooded Mine - Hidden Item Near Cherrygrove Entrance", location_names)
        self.assertIn("Flooded Mine - Hidden Item Southeast", location_names)
        self.assertIn("Flooded Mine - Hidden Item Northwest", location_names)

    def test_beatable(self):
        self.collect_all_but(["EVENT_BEAT_ELITE_FOUR"])
        self.assertBeatable(True)


class FloodedMineEntranceRandoTest(PokemonCrystalTestBase):
    options = {
        "flooded_mine": "on",
        "randomize_entrances": ["Dungeon", "Dungeon Interior"],
    }

    def test_external_entrances_two_way(self):
        from ..data import data
        for name in (
            "REGION_ROUTE_32:SOUTH -> REGION_FLOODED_MINE:NORTH_ENTRANCE",
            "REGION_FLOODED_MINE:NORTH_ENTRANCE -> REGION_ROUTE_32:SOUTH",
            "REGION_CHERRYGROVE_CITY:FLOODED_MINE_ENTRANCE -> REGION_FLOODED_MINE:SOUTH_ENTRANCE",
            "REGION_FLOODED_MINE:SOUTH_ENTRANCE -> REGION_CHERRYGROVE_CITY:FLOODED_MINE_ENTRANCE",
        ):
            self.assertIn(name, data.entrance_connections)
            self.assertFalse(data.entrance_connections[name].one_way, f"{name} should be two-way")

    def test_internal_warps_two_way(self):
        from ..data import data
        for name in (
            "REGION_FLOODED_MINE:NORTH_ENTRANCE -> REGION_FLOODED_MINE",
            "REGION_FLOODED_MINE -> REGION_FLOODED_MINE:NORTH_ENTRANCE",
            "REGION_FLOODED_MINE:SOUTH_ENTRANCE -> REGION_FLOODED_MINE",
            "REGION_FLOODED_MINE -> REGION_FLOODED_MINE:SOUTH_ENTRANCE",
        ):
            self.assertIn(name, data.entrance_connections)
            self.assertFalse(data.entrance_connections[name].one_way, f"{name} should be two-way")

    def test_beatable(self):
        self.collect_all_but(["EVENT_BEAT_ELITE_FOUR"])
        self.assertBeatable(True)


class FloodedMineJohtoOnlyTest(PokemonCrystalTestBase):
    options = {
        "flooded_mine": "on",
        "johto_only": "on",
    }

    def test_regions_included(self):
        region_names = {r.name for r in self.multiworld.get_regions(self.player)}
        self.assertIn("REGION_FLOODED_MINE", region_names)


class FloodedMineSurfGateTest(PokemonCrystalTestBase):
    options = {
        "flooded_mine": "on",
    }

    def test_cherrygrove_to_entrance_requires_surf(self):
        entrance = self.multiworld.get_entrance(
            "REGION_CHERRYGROVE_CITY -> REGION_CHERRYGROVE_CITY:FLOODED_MINE_ENTRANCE",
            self.player,
        )
        empty_state = self.multiworld.state.copy()
        for player_items in empty_state.prog_items.values():
            player_items.clear()
        self.assertFalse(entrance.access_rule(empty_state))

    def test_entrance_to_cherrygrove_requires_surf(self):
        entrance = self.multiworld.get_entrance(
            "REGION_CHERRYGROVE_CITY:FLOODED_MINE_ENTRANCE -> REGION_CHERRYGROVE_CITY",
            self.player,
        )
        empty_state = self.multiworld.state.copy()
        for player_items in empty_state.prog_items.values():
            player_items.clear()
        self.assertFalse(entrance.access_rule(empty_state))

    def test_mine_unreachable_without_surf_via_cherrygrove(self):
        entrance = self.multiworld.get_entrance(
            "REGION_ROUTE_32:SOUTH -> REGION_FLOODED_MINE:NORTH_ENTRANCE",
            self.player,
        )
        empty_state = self.multiworld.state.copy()
        for player_items in empty_state.prog_items.values():
            player_items.clear()
        self.assertTrue(entrance.access_rule(empty_state))


class FloodedMineGrasssanityTest(PokemonCrystalTestBase):
    options = {
        "flooded_mine": "on",
        "grasssanity": "full",
    }

    def test_no_grass_locations_in_mine(self):
        from ..data import data
        for region_id in (
            "REGION_FLOODED_MINE",
            "REGION_FLOODED_MINE:NORTH_ENTRANCE",
            "REGION_FLOODED_MINE:SOUTH_ENTRANCE",
        ):
            self.assertNotIn(region_id, data.grass_tiles)
        location_names = {loc.name for loc in self.multiworld.get_locations(self.player)}
        mine_grass = {name for name in location_names if name.startswith("Flooded Mine - Grass")}
        self.assertEqual(mine_grass, set())


class FloodedMineFlyDestinationRandoTest(PokemonCrystalTestBase):
    options = {
        "flooded_mine": "on",
        "randomize_fly_destinations": "on",
    }

    def test_mine_not_in_fly_destinations(self):
        from ..data import data
        fly_map_consts = {fly.base_identifier for fly in data.fly_regions}
        self.assertNotIn("FLOODED_MINE", fly_map_consts)

    def test_beatable(self):
        self.collect_all_but(["EVENT_BEAT_ELITE_FOUR"])
        self.assertBeatable(True)


class FloodedMineOffFlyDestinationRandoTest(PokemonCrystalTestBase):
    options = {
        "flooded_mine": "off",
        "randomize_fly_destinations": "on",
    }

    def test_world_generates(self):
        self.assertTrue(self.multiworld.get_regions(self.player))

    def test_no_fly_dest_resolves_to_gated_region(self):
        region_names = {r.name for r in self.multiworld.get_regions(self.player)}
        self.assertNotIn("REGION_CHERRYGROVE_CITY:FLOODED_MINE_ENTRANCE", region_names)
        for warp in self.world.fly_destinations or []:
            self.assertNotEqual(
                (warp.map_name, warp.warp_index), ("CherrygroveCity", 6),
                "fly destination picked the Flooded Mine entrance tile while option is off",
            )


class FloodedMineOffJohtoOnlyFlyDestinationRandoTest(PokemonCrystalTestBase):
    options = {
        "flooded_mine": "off",
        "randomize_fly_destinations": "on",
        "johto_only": "on",
    }

    def test_world_generates(self):
        self.assertTrue(self.multiworld.get_regions(self.player))


class FloodedMineCherrygroveFlyUnlockTest(PokemonCrystalTestBase):
    options = {
        "flooded_mine": "on",
        "randomize_fly_unlocks": "on",
    }

    def test_visit_location_reachable_from_mine_without_surf(self):
        location = self.multiworld.get_location("Visit Cherrygrove City", self.player)
        empty_state = self.multiworld.state.copy()
        for player_items in empty_state.prog_items.values():
            player_items.clear()
        mine_south = self.multiworld.get_region(
            "REGION_FLOODED_MINE:SOUTH_ENTRANCE", self.player,
        )
        empty_state.reachable_regions[self.player].add(mine_south)
        for exit_ in mine_south.exits:
            empty_state.blocked_connections[self.player].add(exit_)
        empty_state.update_reachable_regions(self.player)
        self.assertTrue(location.can_reach(empty_state))


class FloodedMineVanillaFlyEdgeTest(PokemonCrystalTestBase):
    options = {
        "flooded_mine": "on",
    }

    def test_fly_hub_edge_exists(self):
        entrance = self.multiworld.get_entrance("REGION_FLY -> REGION_CHERRYGROVE_CITY", self.player)
        self.assertEqual(entrance.parent_region.name, "REGION_FLY")
        self.assertEqual(entrance.connected_region.name, "REGION_CHERRYGROVE_CITY")

    def test_fly_to_town_requires_visit(self):
        entrance = self.multiworld.get_entrance("REGION_FLY -> REGION_CHERRYGROVE_CITY", self.player)
        empty_state = self.multiworld.state.copy()
        for player_items in empty_state.prog_items.values():
            player_items.clear()
        self.assertFalse(entrance.access_rule(empty_state))

    def test_azalea_fly_hub_edge_exists(self):
        entrance = self.multiworld.get_entrance("REGION_FLY -> REGION_AZALEA_TOWN", self.player)
        self.assertEqual(entrance.connected_region.name, "REGION_AZALEA_TOWN")


class FloodedMineFlyEdgeUnlockRandoTest(PokemonCrystalTestBase):
    options = {
        "flooded_mine": "on",
        "randomize_fly_unlocks": "on",
    }

    def test_fly_hub_edges_exist(self):
        from ..data import data
        region_names = {r.name for r in self.multiworld.get_regions(self.player)}
        entrance_names = {e.name for r in self.multiworld.get_regions(self.player) for e in r.exits}
        for fr in data.fly_regions:
            if fr.exit_region not in region_names:
                continue
            self.assertIn(f"REGION_FLY -> {fr.exit_region}", entrance_names)

    def test_fly_requires_unlock_item(self):
        entrance = self.multiworld.get_entrance("REGION_FLY -> REGION_CHERRYGROVE_CITY", self.player)
        empty_state = self.multiworld.state.copy()
        for player_items in empty_state.prog_items.values():
            player_items.clear()
        self.assertFalse(entrance.access_rule(empty_state))


class FloodedMineLabelsTest(PokemonCrystalTestBase):
    auto_construct = False

    def test_wild_table_labels_present(self):
        from ..data import data
        self.assertIn("AP_WildGrass_FLOODED_MINE", data.rom_addresses)
        self.assertIn("AP_WildWater_FLOODED_MINE", data.rom_addresses)

    def test_landmark_label_present(self):
        from ..data import data
        self.assertIn("AP_Landmark_FLOODED_MINE", data.rom_addresses)
