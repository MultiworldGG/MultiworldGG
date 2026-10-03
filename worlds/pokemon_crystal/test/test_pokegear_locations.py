from BaseClasses import CollectionState

from .bases import PokemonCrystalTestBase

EXPN = "Lavender Radio Tower - EXPN Card"


class ExpnCardRemoteItemsTest(PokemonCrystalTestBase):
    """remote_items creates the Pokegear locations even with randomize_pokegear off."""
    options = {
        "johto_only": "off",
        "remote_items": "true",
        "randomize_pokegear": "false",
    }

    def test_expn_card_requires_power(self):
        state = CollectionState(self.multiworld)
        for name in (EXPN, "EVENT_GOT_EXPN_CARD"):
            loc = self.multiworld.get_location(name, self.player)
            self.assertFalse(loc.access_rule(state), f"{name} should require power restored.")
        state.collect(self.world.create_event("EVENT_RESTORED_POWER_TO_KANTO"), prevent_sweep=True)
        for name in (EXPN, "EVENT_GOT_EXPN_CARD"):
            self.assertTrue(self.multiworld.get_location(name, self.player).access_rule(state))


class ExpnCardRandomizedPokegearTest(PokemonCrystalTestBase):
    options = {
        "johto_only": "off",
        "randomize_pokegear": "true",
    }

    def test_expn_card_requires_power(self):
        loc = self.multiworld.get_location(EXPN, self.player)
        self.assertFalse(loc.access_rule(CollectionState(self.multiworld)))
