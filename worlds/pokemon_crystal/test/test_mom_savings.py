from BaseClasses import CollectionState

from .bases import PokemonCrystalTestBase


class MomsanityTest(PokemonCrystalTestBase):
    options = {
        "momsanity": "on"
    }

    def test_milestones_exist(self):
        self.multiworld.get_location("Mom's Savings - 900", self.player)
        self.multiworld.get_location("Mom's Savings - 100000", self.player)

    def test_milestone_is_gated(self):
        # The rule is non-trivial: unreachable from an empty state (needs the
        # Mystery Egg returned to Elm), reachable once everything is collected.
        location = self.multiworld.get_location("Mom's Savings - 900", self.player)
        self.assertFalse(location.can_reach(CollectionState(self.multiworld)))
        self.assertTrue(location.can_reach(self.multiworld.get_all_state(False)))


class MomsanityOffTest(PokemonCrystalTestBase):
    options = {
        "momsanity": "off"
    }

    def test_locations_absent(self):
        self.assertRaises(KeyError, self.multiworld.get_location, "Mom's Savings - 900", self.player)
