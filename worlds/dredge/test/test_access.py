from BaseClasses import CollectionState, LocationProgressType
from .bases import DredgeTestBase
from ..locations import location_table, ItemsReq

PASSAGE_ITEM_BY_REGION = {
    "Gale Cliffs": "The Windward Litany",
    "Stellar Basin": "The Astral Testament",
    "Twisted Strand": "The Mangrove Canticle",
    "Devil's Spine": "The Cinder Gospel",
    "The Pale Reach": "The Rimebound Chronicle",
}

LICENSE_BY_REGION = {
    "Gale Cliffs": "Gale Cliffs Fishing License",
    "Stellar Basin": "Stellar Basin Fishing License",
    "Twisted Strand": "Twisted Strand Fishing License",
    "Devil's Spine": "Devil's Spine Fishing License",
    "Open Ocean": "Open Ocean Fishing License",
    "The Pale Reach": "Pale Reach Fishing License",
}


class TestPassageAccess(DredgeTestBase):
    options = {
        "include_pale_reach_dlc": True,
        "add_passage_items": True,
    }
    run_default_tests = False

    def test_regions_need_their_passage(self) -> None:
        for region_name, passage_item in PASSAGE_ITEM_BY_REGION.items():
            with self.subTest(region=region_name):
                region = self.multiworld.get_region(region_name, self.player)
                locations = [location.name for location in region.locations if location.address is not None]
                self.assertTrue(locations, f"No locations in {region_name}")
                self.assertAccessDependency(locations, [[passage_item]], only_check_listed=True)


class TestIronRigPhaseAccess(DredgeTestBase):
    options = {
        "include_iron_rig_dlc": True,
        "add_passage_items": True,
    }
    run_default_tests = False

    def test_phase_locations_need_rig_access(self) -> None:
        locations = [
            location.name
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
            and any(req.type == "iron_rig_phase" for req in location_table[location.name].requirements)
        ]
        self.assertTrue(locations, "No Iron Rig phase locations")
        self.assertAccessDependency(locations, [["The Pelagic Psalm"]], only_check_listed=True)


class TestIcebreakerAccess(DredgeTestBase):
    options = {
        "include_pale_reach_dlc": True,
    }
    run_default_tests = False

    def test_icebreaker_or_all_parts(self) -> None:
        locations = [
            location.name
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
            and any(isinstance(req, ItemsReq) and "Icebreaker" in req.all_of
                    for req in location_table[location.name].requirements)
        ]
        self.assertTrue(locations, "No locations require the Icebreaker")
        self.assertAccessDependency(
            locations,
            [["Icebreaker"], ["Icebreaker Plow Half 1", "Icebreaker Plow Half 2", "Icebreaker Bracing"]],
            only_check_listed=True)


class TestLicenseAccess(DredgeTestBase):
    options = {
        "include_pale_reach_dlc": True,
        "add_fishing_licenses": True,
    }
    run_default_tests = False

    def test_encyclopedia_locations_need_their_license(self) -> None:
        for region_name, license_item in LICENSE_BY_REGION.items():
            with self.subTest(region=region_name):
                locations = [
                    location.name
                    for location in self.multiworld.get_locations(self.player)
                    if location.address is not None
                    and location_table[location.name].location_group == "Encyclopedia"
                    and location_table[location.name].region == region_name
                ]
                self.assertTrue(locations, f"No encyclopedia locations in {region_name}")
                self.assertAccessDependency(locations, [[license_item]], only_check_listed=True)


class TestBoatPerformanceAccess(DredgeTestBase):
    options = {
        "include_pale_reach_dlc": True,
        "require_boat_performance": True,
    }
    run_default_tests = False

    def state_with(self, *item_names: str) -> CollectionState:
        state = CollectionState(self.multiworld)
        for name in item_names:
            state.collect(self.world.create_item(name), True)
        return state

    def test_lights_are_progression(self) -> None:
        self.assertTrue(self.world.create_item("Cracked Bulb").advancement)

    def test_mid_regions(self) -> None:
        ready = ("Progressive Hull", "Twin Prop Engine", "Halogen Spotlight")
        for region in ("Gale Cliffs", "Stellar Basin", "Twisted Strand", "Devil's Spine"):
            with self.subTest(region=region):
                self.assertTrue(self.state_with(*ready).can_reach_region(region, self.player))
                for missing in ready:
                    items = [name for name in ready if name != missing]
                    self.assertFalse(self.state_with(*items).can_reach_region(region, self.player), missing)

    def test_open_ocean_locations_need_more_light(self) -> None:
        dim = self.state_with("Progressive Hull", "Twin Prop Engine", "Halogen Spotlight")
        bright = self.state_with("Progressive Hull", "Twin Prop Engine", "Tungsten Floodlight")
        for state in (dim, bright):
            state.collect(self.world.create_item("Dredge Crane"), True)
        locations = [location for location in self.multiworld.get_region("Open Ocean", self.player).locations
                     if location.address is not None
                     and location_table[location.name].location_group in ("Dredge", "Encyclopedia", "World")
                     and location.can_reach(bright)]
        self.assertTrue(locations, "No Open Ocean location reachable with a Tungsten Floodlight")
        for location in locations:
            with self.subTest(location=location.name):
                self.assertFalse(location.can_reach(dim))

    def test_pale_reach_needs_more_speed(self) -> None:
        state = self.state_with("Progressive Hull", "Twin Prop Engine", "Tungsten Floodlight")
        self.assertFalse(state.can_reach_region("The Pale Reach", self.player))
        state.collect(self.world.create_item("Engine Stack"), True)
        self.assertTrue(state.can_reach_region("The Pale Reach", self.player))


class TestLightsUsefulWithoutBoatPerformance(DredgeTestBase):
    run_default_tests = False

    def test_lights_are_useful(self) -> None:
        self.assertFalse(self.world.create_item("Cracked Bulb").advancement)


class TestResearchUnlockEvents(DredgeTestBase):
    run_default_tests = False

    def test_unlocks_are_events(self) -> None:
        self.assertNotIn("Flexible Fishing Pole Researched", self.world.item_name_to_id)
        self.assertNotIn("Flexible Fishing Pole Researched", self.world.location_name_to_id)
        location = self.multiworld.get_location("Flexible Fishing Pole Researched", self.player)
        self.assertIsNone(location.address)
        self.assertIsNone(location.item.code)
        self.assertTrue(location.item.advancement)

    def test_unlock_events_gate_later_research(self) -> None:
        location = self.multiworld.get_location("Heat-Resistant Line Researched", self.player)
        state = CollectionState(self.multiworld)
        self.assertFalse(location.can_reach(state))
        state.collect(self.multiworld.get_location("Flexible Fishing Pole Researched", self.player).item, True)
        self.assertTrue(location.can_reach(state))


BASE_PURSUITS = {
    "Fishmonger's Gift", "Shipwright's Gift", "Little Marrow Trader's Gift", "Travelling Merchant's Gift",
    "Package Delivery", "Craven Courier", "Figure in Blue", "Figure in Gold", "Figure in Purple", "Figure in Red",
    "Research Assistant", "A Place to Rest", "Grotesque Fish", "The Collector - Ornate Key",
    "The Collector - Rusted Music Box", "The Collector - Jewel Encrusted Band", "The Collector - Shimmering Necklace",
    "The Collector - Antique Pocket Watch", "A Fresh Start", "Castaway", "Caught to Order", "Lost Dog", "Lost at Sea",
    "Recording Rarities - Oarfish", "Recording Rarities - Gulper Eel", "Recording Rarities - Goliath Tigerfish",
    "Recording Rarities - Coelacanth", "The Bitter End - Dog Tags", "The Bitter End", "Flames of The Deep", "Stone Tablets",
}


def pursuit_locations(test: DredgeTestBase) -> dict[str, object]:
    return {location.name: location for location in test.multiworld.get_locations(test.player)
            if location.name in location_table and location_table[location.name].location_group == "Pursuit"}


class TestPursuitAccess(DredgeTestBase):
    options = {
        "add_passage_items": True,
    }
    run_default_tests = False

    def test_base_pursuits_present(self) -> None:
        self.assertEqual(set(pursuit_locations(self)), BASE_PURSUITS)

    def test_a_place_to_rest_only_needs_dredge_crane(self) -> None:
        location = pursuit_locations(self)["A Place to Rest"]
        self.assertEqual(location.progress_type, LocationProgressType.DEFAULT)
        self.assertEqual(location_table["A Place to Rest"].requirements, [ItemsReq(all_of=["Dredge Crane"])])

    def test_hooded_figure_needs_its_fish_regions(self) -> None:
        # Tiger Mackerel is a Gale Cliffs fish and Snake Mackerel a Devil's Spine one.
        self.assertAccessDependency(["Figure in Blue"], [["The Windward Litany"]], only_check_listed=True)
        self.assertAccessDependency(["Figure in Blue"], [["The Cinder Gospel"]], only_check_listed=True)

    def test_travelling_merchant_needs_open_ocean(self) -> None:
        self.assertAccessDependency(["Travelling Merchant's Gift"], [["The Pelagic Psalm"]], only_check_listed=True)

    def test_trader_and_builder_need_dredge_crane(self) -> None:
        self.assertAccessDependency(["Little Marrow Trader's Gift", "A Place to Rest"], [["Dredge Crane"]],
                                    only_check_listed=True)


class TestPaleReachPursuit(DredgeTestBase):
    options = {
        "include_pale_reach_dlc": True,
        "include_aberrations": True,
    }
    run_default_tests = False

    def test_figure_in_white_present_and_not_excluded(self) -> None:
        pursuits = pursuit_locations(self)
        self.assertEqual(set(pursuits), BASE_PURSUITS | {
            "Figure in White", "Ice Shaper", "Under The Ice - Central Camp", "Under The Ice - Eastern Terminus",
            "Under The Ice - Western Bearing", "Under The Ice - Southern Locus"})
        self.assertEqual(pursuits["Figure in White"].progress_type, LocationProgressType.DEFAULT)


class TestPursuitLicenseAccess(DredgeTestBase):
    options = {
        "add_fishing_licenses": True,
    }
    run_default_tests = False

    def test_hooded_figure_needs_its_fish_licenses(self) -> None:
        for license_name in ("Gale Cliffs Fishing License", "Devil's Spine Fishing License"):
            with self.subTest(license=license_name):
                self.assertAccessDependency(["Figure in Blue"], [[license_name]], only_check_listed=True)


class TestCollectorAccess(DredgeTestBase):
    run_default_tests = False

    def test_relic_hand_ins_need_their_relic(self) -> None:
        self.assertAccessDependency(["The Collector - Ornate Key"], [["Ornate Key"]], only_check_listed=True)

    def test_atrophy_catches_spot_fish_without_tackle(self) -> None:
        state = CollectionState(self.multiworld)
        sailfish = self.multiworld.get_location("Sailfish", self.player)
        self.assertFalse(sailfish.can_reach(state))
        state.collect(self.world.create_item("Atrophy"), True)
        self.assertTrue(sailfish.can_reach(state))

    def test_atrophy_doesnt_catch_crabs(self) -> None:
        state = CollectionState(self.multiworld)
        state.collect(self.world.create_item("Atrophy"), True)
        self.assertFalse(self.multiworld.get_location("Common Crab", self.player).can_reach(state))


class TestRewardGridPursuitAccess(DredgeTestBase):
    run_default_tests = False

    def test_research_assistant_needs_sampling_device(self) -> None:
        self.assertAccessDependency(["Research Assistant"], [["Sampling Device"]], only_check_listed=True)

    def test_quest_item_pursuits_need_their_items(self) -> None:
        self.assertAccessDependency(["Lost at Sea"], [["Bronze Belt Buckle"]], only_check_listed=True)
        self.assertAccessDependency(["The Bitter End - Dog Tags"], [["Dog Tags"]], only_check_listed=True)
        self.assertAccessDependency(["The Bitter End"], [["Mortar Frame"]], only_check_listed=True)
        self.assertAccessDependency(["The Bitter End"], [["Mortar Barrel"]], only_check_listed=True)



class TestWorldLocationAccess(DredgeTestBase):
    run_default_tests = False

    def test_shrines_caches_and_loot_spots_present(self) -> None:
        world = {location.name for location in self.multiworld.get_locations(self.player)
                 if location.name in location_table and location_table[location.name].location_group == "World"}
        self.assertEqual(len(world), 23)

    def test_stone_tablets_need_the_tablets(self) -> None:
        for tablet in ("Stone Tablet 1", "Stone Tablet 2", "Stone Tablet 3"):
            with self.subTest(tablet=tablet):
                self.assertAccessDependency(["Stone Tablets"], [[tablet]], only_check_listed=True)


ABERRATION_DELIVERIES = ["Caught to Order", "Flames of The Deep", "Twisted Strand - Aberration Shrine(D-13)",
                         "Devil's Spine - Shrine 3(O-14)"]


def aberration_fish(test: DredgeTestBase) -> list[str]:
    return [location.name for location in test.multiworld.get_locations(test.player)
            if location.name in location_table and location_table[location.name].is_aberration
            and location_table[location.name].location_group == "Encyclopedia"]


class TestProgressiveAberrationGating(DredgeTestBase):
    options = {
        "progressive_aberration_chance_items": 4,
    }
    run_default_tests = False

    def test_aberrations_need_chance_items(self) -> None:
        self.assertAccessDependency(aberration_fish(self) + ABERRATION_DELIVERIES,
                                    [["Progressive Aberration Chance"]], only_check_listed=True)

    def test_half_the_items_are_enough(self) -> None:
        state = self.multiworld.get_all_state()
        state.remove(self.world.create_item("Progressive Aberration Chance"))
        state.remove(self.world.create_item("Progressive Aberration Chance"))
        self.assertTrue(self.multiworld.get_location("Twisted Strand - Aberration Shrine(D-13)", self.player)
                        .can_reach(state))
        state.remove(self.world.create_item("Progressive Aberration Chance"))
        self.assertFalse(self.multiworld.get_location("Twisted Strand - Aberration Shrine(D-13)", self.player)
                         .can_reach(state))


class TestGuaranteedAberrationGating(DredgeTestBase):
    options = {
        "guaranteed_aberrations_item": True,
    }
    run_default_tests = False

    def test_aberrations_need_guaranteed_item(self) -> None:
        self.assertAccessDependency(aberration_fish(self) + ABERRATION_DELIVERIES,
                                    [["Guaranteed Aberrations"]], only_check_listed=True)


class TestPaleReachIceAxes(DredgeTestBase):
    options = {
        "include_pale_reach_dlc": True,
    }
    run_default_tests = False

    def test_four_ice_axes_in_pool(self) -> None:
        axes = [item for item in self.multiworld.itempool if item.player == self.player and item.name == "Ice Axe"]
        self.assertEqual(len(axes), 4)

    def test_shards_need_all_four_axes(self) -> None:
        state = self.multiworld.get_all_state()
        state.remove(self.world.create_item("Ice Axe"))
        for location in ("Under The Ice - Central Camp", "The Pale Reach - Shrine(K--4)"):
            with self.subTest(location=location):
                self.assertFalse(self.multiworld.get_location(location, self.player).can_reach(state))

    def test_captains_logs_present(self) -> None:
        logs = [location.name for location in self.multiworld.get_locations(self.player) if "Log" in location.name]
        self.assertEqual(len(logs), 9)


class TestIronRigRewards(DredgeTestBase):
    options = {
        "include_iron_rig_dlc": True,
    }
    run_default_tests = False

    def test_rig_rewards_need_dredge_crane(self) -> None:
        self.assertAccessDependency(["Getting Power - Rig Built", "Getting Power - Science Lab Built",
                                     "Getting Power - Generator Fuelled", "Drilling in the Deep - Factory"],
                                    [["Dredge Crane"]], only_check_listed=True)


class TestResearchChecks(DredgeTestBase):
    run_default_tests = False

    def test_research_is_free_and_parts_not_in_pool(self) -> None:
        parts = [item for item in self.multiworld.itempool if item.player == self.player and item.name == "Research Part"]
        self.assertEqual(parts, [])
        state = CollectionState(self.multiworld)
        self.assertTrue(self.multiworld.get_location("Flexible Fishing Pole", self.player).can_reach(state))


class TestNoResearchChecks(DredgeTestBase):
    options = {
        "include_research_checks": False,
    }
    run_default_tests = False

    def test_no_research_locations(self) -> None:
        research = [location.name for location in self.multiworld.get_locations(self.player)
                    if location.name in location_table
                    and location_table[location.name].location_group in ("Research", "Research Unlock")]
        self.assertEqual(research, [])
