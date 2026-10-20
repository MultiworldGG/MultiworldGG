from BaseClasses import CollectionState
from .bases import PokemonSnapTestBase
from ..locations import species_data_tables, wonderful, multiple
from ..items import item_dictionary
from ..constants import APPLE, PESTER_BALL, POKEFLUTE, DASH_ENGINE
from itertools import chain, combinations

def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

class TestRuleInheritance(PokemonSnapTestBase):

    options = {
        "photo_bonuses": "technique_and_multiple",
        "rng_checks": True,
        "hard_checks": True
    }

    def test_multiple_implies_wonderful(self):
        '''Professor Oak will not give you the multiple species bonus if the picture is not Wonderful'''
        for _, species_data_list in species_data_tables.items():
            for species_data in species_data_list:
                if not (species_data.multiple and species_data.wonderful):
                    continue

                with self.subTest(name=species_data.name):
                    self._assert_multiple_implies_wonderful(species_data.name)
    
    def _assert_multiple_implies_wonderful(self, species_name):
        mult_rule = self.multiworld.get_location(multiple(species_name), self.player).access_rule
        wdfl_rule = self.multiworld.get_location(wonderful(species_name), self.player).access_rule

        tools = [self.get_item_by_name(name)
                 for name, item in item_dictionary.items() 
                 if item.name in [APPLE, PESTER_BALL, POKEFLUTE, DASH_ENGINE]]

        for combo in powerset(tools):
            state = CollectionState(self.multiworld)
            for tool in combo:
                state.collect(self.get_item_by_name(tool.name))

            if mult_rule(state) and not wdfl_rule(state):
                self.fail(f'"{wonderful(species_name)}" can not be collected with {combo}, but "{multiple(species_name)}" can')