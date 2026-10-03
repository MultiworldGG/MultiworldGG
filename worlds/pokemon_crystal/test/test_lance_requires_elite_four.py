from BaseClasses import CollectionState

from .bases import PokemonCrystalTestBase

E4_EVENTS = (
    "EVENT_BEAT_ELITE_4_WILL",
    "EVENT_BEAT_ELITE_4_KOGA",
    "EVENT_BEAT_ELITE_4_BRUNO",
    "EVENT_BEAT_ELITE_4_KAREN",
)


def swept_state(test, excluded_locations):
    state = CollectionState(test.multiworld)
    for item in test.multiworld.itempool:
        state.collect(item, prevent_sweep=True)
    locations = [loc for loc in test.multiworld.get_locations(test.player)
                 if loc.name not in excluded_locations]
    state.sweep_for_advancements(locations=locations)
    return state


class LanceRequiresEliteFourOnTest(PokemonCrystalTestBase):
    options = {
        "lance_requires_elite_four": "on",
    }

    def test_champion_requires_all_e4_events(self):
        beat_e4 = self.multiworld.get_location("EVENT_BEAT_ELITE_FOUR", self.player)
        hall_of_fame = self.multiworld.get_region("REGION_HALL_OF_FAME", self.player)
        for event in E4_EVENTS:
            state = swept_state(self, [event])
            self.assertFalse(beat_e4.can_reach(state),
                             f"EVENT_BEAT_ELITE_FOUR reachable without {event}.")
            self.assertFalse(hall_of_fame.can_reach(state),
                             f"Hall of Fame reachable without {event}.")
        state = swept_state(self, [])
        self.assertTrue(beat_e4.can_reach(state))
        self.assertTrue(hall_of_fame.can_reach(state))

    def test_beatable(self):
        self.collect_all_but(["EVENT_BEAT_ELITE_FOUR"])
        self.assertBeatable(True)


class LanceRequiresEliteFourOffTest(PokemonCrystalTestBase):
    options = {
        "lance_requires_elite_four": "off",
    }

    def test_champion_does_not_require_e4_events(self):
        beat_e4 = self.multiworld.get_location("EVENT_BEAT_ELITE_FOUR", self.player)
        state = swept_state(self, E4_EVENTS)
        self.assertTrue(beat_e4.can_reach(state))


class LanceRequiresEliteFourSkipTest(PokemonCrystalTestBase):
    options = {
        "lance_requires_elite_four": "on",
        "skip_elite_four": "on",
    }

    def test_option_disabled(self):
        self.assertEqual(self.world.options.lance_requires_elite_four.value, 0)

    def test_beatable(self):
        self.collect_all_but(["EVENT_BEAT_ELITE_FOUR"])
        self.assertBeatable(True)


class LanceRequiresEliteFourLeagueERTest(PokemonCrystalTestBase):
    options = {
        "lance_requires_elite_four": "on",
        "randomize_entrances": ["Pokemon League"],
    }

    def test_beatable(self):
        self.collect_all_but(["EVENT_BEAT_ELITE_FOUR"])
        self.assertBeatable(True)
