from BaseClasses import CollectionState
from .bases import PokemonSnapTestBase
from ..constants import POKEMON_FOOD, APPLE, PESTER_BALL, POKEFLUTE, DASH_ENGINE, SIGN_DETECTOR, ALL_MAIN_LEVELS


class TestPokemonFoodRename(PokemonSnapTestBase):

    def test_pokemon_food_and_apple_give_same_accessibility(self):
        state = CollectionState(self.multiworld)
        for item_name in [PESTER_BALL, POKEFLUTE, DASH_ENGINE, SIGN_DETECTOR, *ALL_MAIN_LEVELS]:
            state.collect(self.world.create_item(item_name))

        apple_state = state.copy()
        food_state  = state.copy()

        apple_state.collect(self.world.create_item(APPLE))
        food_state.collect(self.world.create_item(POKEMON_FOOD))

        mismatches = [
            loc.name for loc in self.multiworld.get_locations(self.player)
            if loc.can_reach(apple_state) != loc.can_reach(food_state)
        ]
        self.assertEqual(mismatches, [], "Apple and Pokemon Food accessibility differs at these locations")

        