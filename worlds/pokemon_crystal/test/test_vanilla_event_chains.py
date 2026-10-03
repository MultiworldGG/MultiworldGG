from BaseClasses import CollectionState

from .bases import PokemonCrystalTestBase

surf_items = ["HM03 Surf"]

misty_locations = [
    "Cerulean Gym - Cascade Badge from Misty",
    "Cerulean Gym - Leader Misty",
    "Cerulean Gym - Swimmer Diana",
    "Cerulean Gym - Swimmer Briana",
    "Cerulean Gym - Swimmer Parker",
]


def swept_state(test, withheld):
    state = CollectionState(test.multiworld)
    for item in test.multiworld.itempool:
        if item.name not in withheld:
            state.collect(item, prevent_sweep=True)
    state.sweep_for_advancements()
    return state


class VanillaMistyOnTest(PokemonCrystalTestBase):
    options = {
        "vanilla_event_chains": ["Misty"],
        "johto_only": "off",
        "randomize_hidden_items": "on",
        "johto_trainersanity": "full",
        "kanto_trainersanity": "full",
    }

    def test_cascade_requires_power_plant(self):
        loc = self.multiworld.get_location("Cerulean Gym - Cascade Badge from Misty", self.player)
        self.assertFalse(loc.can_reach(swept_state(self, surf_items)),
                         "Cascade Badge should be unreachable without Power Plant access (no surf).")
        self.assertTrue(loc.can_reach(swept_state(self, [])),
                        "Cascade Badge should be reachable once the chain regions are accessible.")

    def test_machine_part_requires_power_plant(self):
        loc = self.multiworld.get_location("Cerulean Gym - Machine Part in Water", self.player)
        self.assertFalse(loc.can_reach(swept_state(self, surf_items)),
                         "Machine part should stay hidden until the Power Plant manager step.")
        self.assertTrue(loc.can_reach(swept_state(self, [])))

    def test_route_24_rocket_requires_chain(self):
        loc = self.multiworld.get_location("Route 24 - Grunt", self.player)
        self.assertFalse(loc.can_reach(swept_state(self, surf_items)),
                         "Route 24 rocket should be unreachable until the gym grunt scene.")
        self.assertTrue(loc.can_reach(swept_state(self, [])))

    def test_completable(self):
        state = self.multiworld.get_all_state(False)
        for location in misty_locations + ["Cerulean Gym - Machine Part in Water", "Route 24 - Grunt"]:
            self.assertTrue(self.multiworld.get_location(location, self.player).can_reach(state),
                            f"{location} unreachable with all items collected (broken chain or cycle).")


class VanillaMistyTeamRocketGoalTest(PokemonCrystalTestBase):
    options = {
        "goal": ["Defeat Team Rocket"],
        "vanilla_event_chains": ["Misty"],
        "johto_only": "off",
    }

    def test_goal_uses_defeat_event(self):
        completion = self.multiworld.completion_condition[self.player]
        self.assertFalse(completion(swept_state(self, surf_items)),
                         "Team Rocket goal should be incomplete while the Route 24 rocket is unreachable.")
        self.assertTrue(completion(self.multiworld.get_all_state(False)),
                        "Team Rocket goal should be completable with everything reachable.")


class VanillaMistyOffTest(PokemonCrystalTestBase):
    options = {
        "johto_only": "off",
        "randomize_hidden_items": "on",
        "johto_trainersanity": "full",
        "kanto_trainersanity": "full",
    }

    def test_cascade_not_power_plant_gated(self):
        loc = self.multiworld.get_location("Cerulean Gym - Cascade Badge from Misty", self.player)
        self.assertTrue(loc.can_reach(swept_state(self, surf_items)),
                        "Cascade Badge should not depend on Power Plant access without vanilla Misty.")


class VanillaClairTest(PokemonCrystalTestBase):
    options = {
        "vanilla_event_chains": ["Clair"],
    }

    def test_rising_badge_at_shrine(self):
        self.multiworld.get_location("Dragon Shrine - Rising Badge from Clair", self.player)
        self.assertRaises(KeyError, self.multiworld.get_location,
                          "Blackthorn Gym - Rising Badge from Clair", self.player)


class VanillaClairOffTest(PokemonCrystalTestBase):
    options = {}

    def test_rising_badge_at_gym(self):
        self.multiworld.get_location("Blackthorn Gym - Rising Badge from Clair", self.player)
        self.assertRaises(KeyError, self.multiworld.get_location,
                          "Dragon Shrine - Rising Badge from Clair", self.player)


class VanillaJasmineTest(PokemonCrystalTestBase):
    options = {
        "vanilla_event_chains": ["Jasmine"],
        "johto_only": "off",
    }

    def test_secretpotion_requires_meeting_jasmine(self):
        loc = self.multiworld.get_location("Cianwood Pharmacy - Secretpotion", self.player)
        self.assertFalse(loc.access_rule(CollectionState(self.multiworld)),
                         "SecretPotion should require having met Jasmine at the lighthouse.")
        self.assertTrue(loc.access_rule(self.multiworld.get_all_state(False)))


class VanillaJasmineOffTest(PokemonCrystalTestBase):
    options = {
        "johto_only": "off",
    }

    def test_secretpotion_not_gated(self):
        loc = self.multiworld.get_location("Cianwood Pharmacy - Secretpotion", self.player)
        self.assertTrue(loc.access_rule(CollectionState(self.multiworld)),
                        "SecretPotion should not depend on meeting Jasmine without vanilla Jasmine.")


class VanillaCopycatTest(PokemonCrystalTestBase):
    options = {
        "vanilla_event_chains": ["Copycat"],
        "johto_only": "off",
    }

    def test_lost_item_requires_meeting_copycat(self):
        loc = self.multiworld.get_location("Vermilion City - Lost Item from Guy in Fan Club", self.player)
        state = CollectionState(self.multiworld)
        state.collect(self.world.create_event("EVENT_RESTORED_POWER_TO_KANTO"), prevent_sweep=True)
        self.assertFalse(loc.access_rule(state),
                         "Lost Item should still require having met the Copycat.")
        state.collect(self.world.create_event("EVENT_MET_COPYCAT_FOUND_OUT_ABOUT_LOST_ITEM"), prevent_sweep=True)
        self.assertTrue(loc.access_rule(state))


class VanillaCopycatOffTest(PokemonCrystalTestBase):
    options = {
        "johto_only": "off",
    }

    def test_lost_item_not_gated_on_copycat(self):
        loc = self.multiworld.get_location("Vermilion City - Lost Item from Guy in Fan Club", self.player)
        state = CollectionState(self.multiworld)
        state.collect(self.world.create_event("EVENT_RESTORED_POWER_TO_KANTO"), prevent_sweep=True)
        self.assertTrue(loc.access_rule(state),
                        "Lost Item should not depend on the Copycat without vanilla Copycat.")


class VanillaEventChainsDefaultTest(PokemonCrystalTestBase):
    options = {}

    def test_default_empty(self):
        self.assertEqual(set(self.world.options.vanilla_event_chains.value), set())


class VanillaEventChainsSlotDataTest(PokemonCrystalTestBase):
    options = {
        "vanilla_event_chains": ["Misty"],
        "johto_only": "off",
    }

    def test_in_slot_data(self):
        slot_data = self.world.fill_slot_data()
        self.assertIn("vanilla_event_chains", slot_data)
        self.assertIn("Misty", slot_data["vanilla_event_chains"])
