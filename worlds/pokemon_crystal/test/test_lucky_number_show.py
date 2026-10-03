from BaseClasses import CollectionState

from .bases import PokemonCrystalTestBase

PRIZE_LABELS = [
    "Radio Tower 1F - Lucky Number Show 1st Prize",
    "Radio Tower 1F - Lucky Number Show 2nd Prize",
    "Radio Tower 1F - Lucky Number Show 3rd Prize",
]
EVENT_NAMES = ["Lucky Number Trade 1", "Lucky Number Trade 2", "Lucky Number Trade 3"]
JOHTO_TRADES = {"TRADE_MIKE", "TRADE_KYLE", "TRADE_TIM", "TRADE_EMY"}


class LuckyNumberShowTest(PokemonCrystalTestBase):
    options = {
        "randomize_lucky_number_show": "true",
        "randomize_wilds": "completely_random",
    }

    def test_locations_present(self):
        names = {loc.name for loc in self.multiworld.get_locations(self.player)}
        for label in PRIZE_LABELS:
            self.assertIn(label, names)
        for event in EVENT_NAMES:
            self.assertIn(event, names)

    def test_three_distinct_trades_chosen(self):
        chosen = self.world.generated_lucky_number_trades
        self.assertEqual(len(chosen), 3)
        self.assertEqual(len(set(chosen)), 3)

    def test_prize_requires_trade_event(self):
        state = CollectionState(self.multiworld)
        for event, prize in zip(EVENT_NAMES, PRIZE_LABELS):
            rule = self.world.get_location(prize).access_rule
            self.assertFalse(rule(state))
            state.collect(self.world.create_event(event), prevent_sweep=True)
            self.assertTrue(rule(state))

    def test_event_requires_trade_species(self):
        # Each trade-access event is gated on the requested species: unreachable from empty
        # state, reachable once everything is collected.
        empty = CollectionState(self.multiworld)
        all_state = self.multiworld.get_all_state(False)
        for event in EVENT_NAMES:
            location = self.world.get_location(event)
            self.assertFalse(location.access_rule(empty))
            self.assertTrue(location.can_reach(all_state))

    def test_slot_data_round_trip(self):
        # The option and chosen trades must reach slot_data, or Universal Tracker
        # reconstructs the world with the feature off.
        slot_data = self.world.fill_slot_data()
        self.assertEqual(slot_data["randomize_lucky_number_show"], 1)
        self.assertEqual(slot_data["lucky_number_trades"], self.world.generated_lucky_number_trades)


class LuckyNumberShowOffTest(PokemonCrystalTestBase):
    options = {}

    def test_locations_absent(self):
        names = {loc.name for loc in self.multiworld.get_locations(self.player)}
        for label in PRIZE_LABELS:
            self.assertNotIn(label, names)
        self.assertEqual(self.world.generated_lucky_number_trades, [])


class LuckyNumberShowJohtoOnlyTest(PokemonCrystalTestBase):
    options = {
        "randomize_lucky_number_show": "true",
        "randomize_wilds": "completely_random",
        "johto_only": "on"
    }

    def test_only_johto_trades_chosen(self):
        for trade_id in self.world.generated_lucky_number_trades:
            self.assertIn(trade_id, JOHTO_TRADES)


VANILLA_TRADE_OPTIONS = {
    "randomize_lucky_number_show": "true",
    "trades_required": "true",
    "randomize_wilds": "vanilla",
    "randomize_trades": "vanilla",
}


def assert_vanilla_trades_disabled(test: PokemonCrystalTestBase):
    test.assertFalse(test.world.options.randomize_lucky_number_show)
    test.assertFalse(test.world.options.trades_required)
    test.assertEqual(test.world.generated_lucky_number_trades, [])
    names = {loc.name for loc in test.multiworld.get_locations(test.player)}
    for label in PRIZE_LABELS:
        test.assertNotIn(label, names)


def assert_vanilla_trades_reachable(test: PokemonCrystalTestBase):
    test.assertTrue(test.world.options.randomize_lucky_number_show)
    test.assertTrue(test.world.options.trades_required)
    all_state = test.multiworld.get_all_state(False)
    locations = [loc for loc in test.multiworld.get_locations(test.player)
                 if loc.name.startswith("TRADE_") or loc.name in EVENT_NAMES]
    test.assertTrue(locations)
    for location in locations:
        test.assertTrue(location.can_reach(all_state), f"{location.name} unreachable with everything collected")


class VanillaTradesKantoWithoutTimeOfDayTest(PokemonCrystalTestBase):
    # Haunter is night-only, so the Pewter trade can't be met.
    options = VANILLA_TRADE_OPTIONS

    def test_disabled(self):
        assert_vanilla_trades_disabled(self)


class VanillaTradesKantoWithTimeOfDayTest(PokemonCrystalTestBase):
    options = VANILLA_TRADE_OPTIONS | {"time_of_day_encounters": "true"}

    def test_enabled(self):
        assert_vanilla_trades_reachable(self)


class VanillaTradesJohtoOnlyTest(PokemonCrystalTestBase):
    options = VANILLA_TRADE_OPTIONS | {"johto_only": "on"}

    def test_enabled(self):
        assert_vanilla_trades_reachable(self)


class VanillaTradesDragonairByEvolutionTest(PokemonCrystalTestBase):
    options = VANILLA_TRADE_OPTIONS | {"johto_only": "on", "wild_encounter_methods_required": ["Land", "Surfing"]}

    def test_enabled(self):
        assert_vanilla_trades_reachable(self)


class VanillaTradesNoDragonairSourceTest(PokemonCrystalTestBase):
    options = VANILLA_TRADE_OPTIONS | {"johto_only": "on", "wild_encounter_methods_required": ["Land"],
                                      "static_pokemon_required": "false"}

    def test_disabled(self):
        assert_vanilla_trades_disabled(self)


class VanillaTradesNoLandTest(PokemonCrystalTestBase):
    options = VANILLA_TRADE_OPTIONS | {"johto_only": "on",
                                      "wild_encounter_methods_required": ["Surfing", "Fishing", "Rock Smash"]}

    def test_disabled(self):
        assert_vanilla_trades_disabled(self)
