import inspect
import json

from Options import PerGameCommonOptions

from . import InscryptionTestBase
from ..Items import filler_items_by_act, trap_items
from ..Options import InscryptionOptions


TRAP_NAMES = {item["name"] for item in trap_items}


class OptionTestBase(InscryptionTestBase):
    def location_names(self):
        return [location.name for location in self.multiworld.get_unfilled_locations(self.player)]

    def pool_names(self):
        return [item.name for item in self.multiworld.itempool]

    def precollected_names(self):
        return [item.name for item in self.multiworld.precollected_items[self.player]]

    def assert_only_acts(self, *expected_acts: str) -> None:
        prefixes = {name.split(" - ")[0] for name in self.location_names()}
        self.assertEqual(prefixes, set(expected_acts))

    def assert_pool_matches_locations(self) -> None:
        self.assertEqual(len(self.pool_names()), len(self.location_names()))

    # Currency and card packs only have an effect in their own act, so a disabled act's
    # filler would be dead weight in the pool.
    def assert_filler_only_for_acts(self, *acts: int) -> None:
        pool = set(self.pool_names())
        allowed = {name for act in acts for name in filler_items_by_act[act]}
        forbidden = {name for act, names in filler_items_by_act.items() if act not in acts
                     for name in names}
        self.assertTrue(pool & allowed)
        self.assertEqual(pool & forbidden, set())


class TestActOneOnly(OptionTestBase):
    options = {"enable_act_2": 0, "enable_act_3": 0}

    def test_only_act_1_is_generated(self) -> None:
        self.assert_only_acts("Act 1")
        self.assert_pool_matches_locations()
        self.assert_filler_only_for_acts(1)


class TestActTwoOnly(OptionTestBase):
    options = {"enable_act_1": 0, "enable_act_3": 0}

    def test_only_act_2_is_generated(self) -> None:
        self.assert_only_acts("Act 2")
        self.assert_pool_matches_locations()
        self.assert_filler_only_for_acts(2)


class TestActThreeOnly(OptionTestBase):
    options = {"enable_act_1": 0, "enable_act_2": 0}

    def test_only_act_3_is_generated(self) -> None:
        self.assert_only_acts("Act 3")
        self.assert_pool_matches_locations()
        self.assert_filler_only_for_acts(3)


class TestTwoActsEnabled(OptionTestBase):
    options = {"enable_act_3": 0}

    def test_only_enabled_acts_are_generated(self) -> None:
        self.assert_only_acts("Act 1", "Act 2")
        self.assert_pool_matches_locations()
        self.assert_filler_only_for_acts(1, 2)


class ReleaseTestBase(OptionTestBase):
    # The release rule wraps each location's own rule in a lambda carrying both as defaults, which
    # is what distinguishes it from Archipelago's own default "always reachable" lambda.
    def release_wrapped_locations(self):
        return [loc for loc in self.multiworld.get_locations(self.player)
                if len(getattr(loc.access_rule, "__defaults__", None) or ()) == 2]


class TestReleaseOnActCompletion(ReleaseTestBase):
    options = {"release_on_act_completion": 1}

    def test_option_reaches_the_mod(self) -> None:
        self.assertEqual(self.world.fill_slot_data()["release_on_act_completion"], 1)

    def test_every_act_location_gains_the_release_rule(self) -> None:
        self.assertEqual(len(self.release_wrapped_locations()), len(self.location_names()))


class TestReleaseOnActCompletionDisabled(ReleaseTestBase):
    options = {"release_on_act_completion": 0}

    def test_locations_keep_their_own_rules(self) -> None:
        self.assertEqual(self.release_wrapped_locations(), [])


class TestActUnlocksOpen(OptionTestBase):
    options = {"act_unlocks": 1}

    def test_no_act_items_exist(self) -> None:
        self.assertEqual([n for n in self.pool_names() if n in ("Act 1", "Act 2", "Act 3")], [])
        self.assertEqual(self.precollected_names(), [])


class TestActUnlocksItemsStartingActOne(OptionTestBase):
    options = {"act_unlocks": 2, "starting_act": 0}

    def test_starting_act_is_precollected_and_others_are_in_pool(self) -> None:
        self.assertIn("Act 1", self.precollected_names())
        pool = self.pool_names()
        self.assertNotIn("Act 1", pool)
        self.assertIn("Act 2", pool)
        self.assertIn("Act 3", pool)


class TestActUnlocksItemsStartingActTwo(OptionTestBase):
    options = {"act_unlocks": 2, "starting_act": 1}

    def test_starting_act_is_precollected_and_others_are_in_pool(self) -> None:
        self.assertIn("Act 2", self.precollected_names())
        pool = self.pool_names()
        self.assertNotIn("Act 2", pool)
        self.assertIn("Act 1", pool)
        self.assertIn("Act 3", pool)


class TestActUnlocksItemsStartingActDisabled(OptionTestBase):
    options = {"act_unlocks": 2, "starting_act": 0, "enable_act_1": 0}

    def test_starting_act_falls_back_to_an_enabled_act(self) -> None:
        precollected = self.precollected_names()
        self.assertEqual(len(precollected), 1)
        self.assertIn(precollected[0], ("Act 2", "Act 3"))
        self.assertNotIn("Act 1", self.pool_names())


class TestHammerVanilla(OptionTestBase):
    options = {"randomize_hammer": 0}

    def test_hammer_is_not_an_item(self) -> None:
        self.assertNotIn("Hammer", self.pool_names())


class TestHammerRandomized(OptionTestBase):
    options = {"randomize_hammer": 1}

    def test_hammer_is_an_item(self) -> None:
        self.assertIn("Hammer", self.pool_names())


class TestHammerRemoved(OptionTestBase):
    options = {"randomize_hammer": 2}

    def test_hammer_is_not_an_item(self) -> None:
        self.assertNotIn("Hammer", self.pool_names())


class TestRandomizeNodes(OptionTestBase):
    options = {"randomize_nodes": 1}

    def test_adds_locations_and_pool_still_fits(self) -> None:
        self.assert_pool_matches_locations()
        self.assertGreater(len(self.location_names()), 100)


class TestRandomizeChallenges(OptionTestBase):
    options = {"randomize_challenges": 2}

    def test_adds_locations_and_pool_still_fits(self) -> None:
        self.assert_pool_matches_locations()
        self.assertGreater(len(self.location_names()), 100)


class TestRandomizeChallengesNoGrizzlies(OptionTestBase):
    options = {"randomize_challenges": 1}

    def test_pool_still_fits(self) -> None:
        self.assert_pool_matches_locations()


class TestRandomizeShortcuts(OptionTestBase):
    options = {"randomize_shortcuts": 1}

    def test_adds_locations_and_pool_still_fits(self) -> None:
        self.assert_pool_matches_locations()
        self.assertGreater(len(self.location_names()), 100)


class TestRandomizeVesselUpgrades(OptionTestBase):
    options = {"randomize_vessel_upgrades": 1}

    def test_adds_locations_and_pool_still_fits(self) -> None:
        self.assert_pool_matches_locations()
        self.assertGreater(len(self.location_names()), 100)


class TestAct3Overhaul(OptionTestBase):
    options = {"act3_overhaul": 1}

    def test_adds_a_location_and_pool_still_fits(self) -> None:
        self.assert_pool_matches_locations()
        self.assertGreater(len(self.location_names()), 100)


class TestAct2RandomizeBridge(OptionTestBase):
    options = {"act2_randomize_bridge": 1}

    def test_pool_still_fits(self) -> None:
        self.assert_pool_matches_locations()


class TestExtraSigils(OptionTestBase):
    options = {"extra_sigils": 1}

    def test_pool_still_fits(self) -> None:
        self.assert_pool_matches_locations()


class TestAllRandomizationEnabled(OptionTestBase):
    options = {
        "randomize_nodes": 1,
        "randomize_challenges": 2,
        "randomize_shortcuts": 1,
        "randomize_vessel_upgrades": 1,
        "randomize_hammer": 1,
        "act2_randomize_bridge": 1,
        "act3_overhaul": 1,
        "extra_sigils": 1,
    }

    def test_every_location_is_generated(self) -> None:
        self.assert_pool_matches_locations()
        self.assertEqual(len(self.location_names()), len(self.multiworld.worlds[self.player].all_locations))


class TestNoTraps(OptionTestBase):
    options = {"trap_chance": 0}

    def test_no_traps_are_generated(self) -> None:
        self.assertEqual([n for n in self.pool_names() if n in TRAP_NAMES], [])


class TestAllTraps(OptionTestBase):
    options = {"trap_chance": 100}

    def test_traps_replace_filler(self) -> None:
        self.assertGreater(len([n for n in self.pool_names() if n in TRAP_NAMES]), 0)
        self.assert_pool_matches_locations()


class TestSingleTrapType(OptionTestBase):
    options = {
        "trap_chance": 100,
        "trap_type_weights": {"Bleach Trap": 1, "Trash Trap": 0,
                              "Deck Size Trap": 0, "Reinforcements Trap": 0},
    }

    def test_only_the_weighted_trap_is_generated(self) -> None:
        traps = {n for n in self.pool_names() if n in TRAP_NAMES}
        self.assertEqual(traps, {"Bleach Trap"})


class TestUniversalTrackerPassthrough(OptionTestBase):
    options = {"act_unlocks": 2, "starting_act": 0, "enable_act_1": 0}

    # start_inventory_from_pool is Archipelago's own option; the tracker handles start inventory
    # itself, so it is the one world-dataclass entry deliberately kept out of slot data.
    core_options_not_in_slot_data = {"start_inventory_from_pool"}

    def test_slot_data_covers_every_world_option(self) -> None:
        world_options = set(InscryptionOptions.type_hints) - set(PerGameCommonOptions.type_hints)
        expected = world_options - self.core_options_not_in_slot_data
        self.assertEqual(expected - set(self.world.fill_slot_data()), set())

    def test_interpret_slot_data_is_static_and_requests_regeneration(self) -> None:
        self.assertIsInstance(inspect.getattr_static(type(self.world), "interpret_slot_data"), staticmethod)
        self.assertIsNotNone(self.world.interpret_slot_data(self.world.fill_slot_data()))

    def test_world_declares_it_can_generate_without_a_yaml(self) -> None:
        self.assertTrue(getattr(self.world, "ut_can_gen_without_yaml", False))

    def test_passthrough_restores_options_that_were_not_in_the_yaml(self) -> None:
        slot_data = json.loads(json.dumps(self.world.fill_slot_data()))
        slot_data.update({"act3_overhaul": 1, "randomize_nodes": 1,
                          "trap_chance": 40, "painting_checks_balancing": 2})
        self.world.multiworld.re_gen_passthrough = {self.world.game: slot_data}
        self.world.generate_early()
        self.assertEqual(self.world.options.act3_overhaul.value, 1)
        self.assertEqual(self.world.options.randomize_nodes.value, 1)
        self.assertEqual(self.world.options.trap_chance.value, 40)
        self.assertEqual(self.world.options.painting_checks_balancing.value, 2)

    def test_passthrough_overrides_the_reroll(self) -> None:
        for act in (1, 2):
            self.world.options.starting_act.value = 0
            self.world.multiworld.re_gen_passthrough = {self.world.game: {"starting_act": act}}
            self.world.generate_early()
            self.assertEqual(self.world.options.starting_act.value, act)

    def test_reroll_still_happens_without_passthrough(self) -> None:
        self.world.options.starting_act.value = 0
        self.world.generate_early()
        self.assertIn(self.world.options.starting_act.value, (1, 2))
