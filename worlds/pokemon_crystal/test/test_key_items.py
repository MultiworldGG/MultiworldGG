from .bases import PokemonCrystalTestBase, swept_state


class KeyItemsTest(PokemonCrystalTestBase):
    options = {}

    def _can_reach_ecruteak(self, withheld):
        self.multiworld.state = swept_state(self, withheld)
        return self.can_reach_region("REGION_ECRUTEAK_CITY")

    def test_ecruteak_squirtbottle(self):
        self.assertFalse(self._can_reach_ecruteak(["Squirtbottle", "Pass", "S.S. Ticket"]))
        self.assertTrue(self._can_reach_ecruteak(["Pass", "S.S. Ticket"]))

    def test_ecruteak_pass_ticket(self):
        self.assertFalse(self._can_reach_ecruteak(["Squirtbottle", "Pass", "S.S. Ticket"]))
        self.assertFalse(self._can_reach_ecruteak(["Squirtbottle", "S.S. Ticket"]))
        self.assertTrue(self._can_reach_ecruteak(["Squirtbottle"]))
