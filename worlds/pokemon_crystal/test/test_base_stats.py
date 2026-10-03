import random
from unittest import TestCase

from .bases import PokemonCrystalTestBase
from ..data import data
from ..pokemon import get_random_base_stats


class BaseStatStreamTest(TestCase):
    def test_get_random_base_stats(self):
        r = random.Random(1)

        self.assertEqual(get_random_base_stats(r), [46, 56, 24, 26, 54, 42])
        self.assertEqual(get_random_base_stats(r, 5), [75, 105, 150, 95, 120, 135])
        self.assertEqual(get_random_base_stats(r, 1, 318), [48, 62, 37, 73, 71, 27])


class BaseStatsFollowEvolutionsTest(PokemonCrystalTestBase):
    options = {
        "randomize_base_stats": "completely_random",
        "base_stats_evolution_mode": "follow_evolutions",
    }

    def test_evolutions_increase_bst(self):
        for pkmn_name, pkmn_data in self.world.generated_pokemon.items():
            for evo in pkmn_data.evolutions:
                evo_data = self.world.generated_pokemon[evo.pokemon]
                self.assertGreater(evo_data.bst, pkmn_data.bst,
                                   f"{evo.pokemon} has a lower bst than {pkmn_name}")

    def test_stats_within_bounds(self):
        for pkmn_name, pkmn_data in self.world.generated_pokemon.items():
            self.assertEqual(sum(pkmn_data.base_stats), pkmn_data.bst, pkmn_name)
            for stat in pkmn_data.base_stats:
                self.assertTrue(0 < stat <= 255, f"{pkmn_name} has an out of range base stat: {stat}")

    def test_evolutions_inherit_spread(self):
        for pkmn_name, pkmn_data in self.world.generated_pokemon.items():
            shares = [stat / pkmn_data.bst for stat in pkmn_data.base_stats]
            for evo in pkmn_data.evolutions:
                if evo.pokemon in ("FLAREON", "JOLTEON", "VAPOREON", "ESPEON", "UMBREON"): continue
                evo_data = self.world.generated_pokemon[evo.pokemon]
                evo_shares = [stat / evo_data.bst for stat in evo_data.base_stats]
                for stat_index, (share, evo_share) in enumerate(zip(shares, evo_shares)):
                    self.assertAlmostEqual(share, evo_share, delta=0.11,
                                           msg=f"{evo.pokemon} stat {stat_index} does not follow {pkmn_name}")


class BaseStatsFollowEvolutionsKeepBSTTest(PokemonCrystalTestBase):
    options = {
        "randomize_base_stats": "keep_bst",
        "base_stats_evolution_mode": "follow_evolutions",
        "base_stats_multiples_of_five": True,
    }

    def test_bst_preserved(self):
        for pkmn_name, pkmn_data in self.world.generated_pokemon.items():
            self.assertEqual(pkmn_data.bst, data.pokemon[pkmn_name].bst, pkmn_name)

    def test_evolutions_do_not_decrease_bst(self):
        for pkmn_name, pkmn_data in self.world.generated_pokemon.items():
            for evo in pkmn_data.evolutions:
                self.assertGreaterEqual(self.world.generated_pokemon[evo.pokemon].bst, pkmn_data.bst,
                                        f"{evo.pokemon} has a lower bst than {pkmn_name}")
