from .bases import PokemonCrystalTestBase


class DexcountsanityStarterEncounterTest(PokemonCrystalTestBase):
    """place_starters_in_early_wilds (dexsanity_starters: available_early) must only relocate a
    starter between encounter types that dexsanity_logic counts. Otherwise a starter can be swapped
    from a counted type (e.g. Fishing) into an uncounted one (e.g. Land), silently dropping it from
    the logical dex pool after the dexcountsanity milestones were already snapshotted -- which made
    Pokedex - Final Catch demand more catches than are obtainable under full accessibility.

    Options mirror the failing fuzz seed: dexsanity_logic excludes Land, starters are forced early,
    entrance randomization is on. The pool drop is seed-dependent, so sweep several seeds; without
    the fix a number of these leave Final Catch unreachable.
    """

    options = {
        "dexcountsanity": 251,
        "dexcountsanity_step": 250,
        "dexsanity_starters": "available_early",
        "dexsanity_logic": ["Fishing", "Headbutt", "Trades"],
        "randomize_wilds": "completely_random",
        "randomize_starters": "completely_random",
        "randomize_entrances": ["Building"],
        "accessibility": "full",
    }

    def test_final_catch_reachable_across_seeds(self):
        for seed in range(1, 16):
            self.world_setup(seed=seed)
            world = self.world
            self.assertTrue(world.generated_dexcountsanity, f"seed {seed}: no dexcountsanity milestones")
            self.assertLessEqual(world.generated_dexcountsanity[-1],
                                 world.pokemon_pool.dexcountsanity_total, f"seed {seed}")
            final_catch = self.multiworld.get_location("Pokedex - Final Catch", self.player)
            self.assertTrue(final_catch.can_reach(self.multiworld.get_all_state()),
                            f"seed {seed}: Final Catch unreachable")
