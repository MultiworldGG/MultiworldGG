from BaseClasses import CollectionState

from .bases import PokemonCrystalTestBase
from ..data import LogicalAccess


def _sphere_1_species(world):
    state = CollectionState(world.multiworld)
    locations = world.multiworld.get_reachable_locations(state=state, player=world.player)
    early_keys = {
        loc.parent_region.key for loc in locations
        if "wild encounter" in loc.tags
        and world.logic.wild_regions[loc.parent_region.key] is LogicalAccess.InLogic
    }
    species = set()
    for key in early_keys:
        for enc in world.generated_wild.get(key, ()):
            species.add(enc.pokemon)
        if key in world.generated_static:
            species.add(world.generated_static[key].pokemon)
    return species


class EarlyFlyEnsuresFlyLearnerTest(PokemonCrystalTestBase):
    options = {
        "early_fly": "true",
        "randomize_wilds": "completely_random",
    }

    def test_sphere_1_has_fly_learner(self):
        species = _sphere_1_species(self.world)
        self.assertTrue(species, "no sphere 1 species found")
        fly_learners = set(self.world.logic.compatible_hm_pokemon["FLY"])
        self.assertTrue(species & fly_learners,
                        f"no sphere 1 species learns Fly: {sorted(species)}")


class EarlyFlyVanillaWildsTest(PokemonCrystalTestBase):
    options = {
        "early_fly": "true",
        "randomize_wilds": "vanilla",
    }

    def test_sphere_1_has_fly_learner(self):
        species = _sphere_1_species(self.world)
        self.assertTrue(species, "no sphere 1 species found")
        fly_learners = set(self.world.logic.compatible_hm_pokemon["FLY"])
        self.assertTrue(species & fly_learners,
                        f"no sphere 1 species learns Fly: {sorted(species)}")


class EarlyFlyDisabledIsNoOpTest(PokemonCrystalTestBase):
    options = {
        "early_fly": "false",
        "randomize_wilds": "vanilla",
    }

    def test_no_mutation_when_disabled(self):
        from ..data import data as crystal_data
        species = _sphere_1_species(self.world)
        for s in species:
            vanilla_tm_hm = crystal_data.pokemon[s].tm_hm
            current_tm_hm = self.world.generated_pokemon[s].tm_hm
            if "FLY" in current_tm_hm and "FLY" not in vanilla_tm_hm:
                self.fail(f"{s} gained FLY despite early_fly being disabled")
