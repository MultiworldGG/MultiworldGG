from BaseClasses import CollectionState
from .bases import PokemonSnapTestBase
from ..constants import POKEMON_TOTAL_40, ALL_MAIN_LEVELS, LVL_BEACH, LVL_RIVER, LVL_CAVE, LVL_VOLCANO, PESTER_BALL, DASH_ENGINE

class Test40PokemonNotAvailable(PokemonSnapTestBase):

    def test_40_pokemon_check_unavailable(self):
        rule_40_pokemon = self.multiworld.get_location(POKEMON_TOTAL_40, self.player).access_rule
        state = CollectionState(self.multiworld, self.player)
        for item in ALL_MAIN_LEVELS:
            state.remove_item(item, self.player)
        for item in [LVL_BEACH, LVL_RIVER, LVL_CAVE, LVL_VOLCANO, PESTER_BALL, DASH_ENGINE]:
            state.add_item(item, self.player)

        if rule_40_pokemon(state):
            self.fail(f"Should not be able to reach 40 Pokemon")