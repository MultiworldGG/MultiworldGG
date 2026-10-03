from .bases import PokemonCrystalTestBase
from ..data import EncounterType, GrassTimeOfDay


class GrassTimeOfDayDisabledTest(PokemonCrystalTestBase):
    options = {
        "time_of_day_encounters": False,
    }

    def test_grass_keys_have_no_time_of_day(self):
        grass_keys = [k for k in self.world.generated_wild
                      if k.encounter_type is EncounterType.Grass]
        self.assertGreater(len(grass_keys), 0)
        for k in grass_keys:
            self.assertIsNone(k.time_of_day,
                              f"Grass key {k.region_id} should have time_of_day=None when option is off")

    def test_region_names_have_no_time_suffix(self):
        grass_keys = [k for k in self.world.generated_wild
                      if k.encounter_type is EncounterType.Grass]
        for k in grass_keys:
            self.assertNotIn("Morn", k.region_name())
            self.assertNotIn("Day", k.region_name())
            self.assertNotIn("Nite", k.region_name())

    def test_friendly_names_have_no_time_suffix(self):
        grass_keys = [k for k in self.world.generated_wild
                      if k.encounter_type is EncounterType.Grass]
        for k in grass_keys:
            self.assertNotIn("Morn", k.friendly_region_name())
            self.assertNotIn("Nite", k.friendly_region_name())
            self.assertNotIn("- Day", k.friendly_region_name())


class GrassTimeOfDayEnabledTest(PokemonCrystalTestBase):
    options = {
        "time_of_day_encounters": True,
    }

    def test_grass_keys_have_all_three_time_periods(self):
        # Phone-trainer swarms are single-slot synthetics and intentionally don't have ToD variants.
        grass_keys = [k for k in self.world.generated_wild
                      if k.encounter_type is EncounterType.Grass and not k.is_swarm]
        region_ids = set(k.region_id for k in grass_keys)

        for region_id in region_ids:
            region_keys = [k for k in grass_keys if k.region_id == region_id]
            tods = {k.time_of_day for k in region_keys}
            self.assertEqual(tods, {GrassTimeOfDay.Morn, GrassTimeOfDay.Day, GrassTimeOfDay.Nite},
                             f"Region {region_id} should have all 3 time periods")

    def test_region_names_include_time_suffix(self):
        grass_keys = [k for k in self.world.generated_wild
                      if k.encounter_type is EncounterType.Grass and not k.is_swarm]
        for k in grass_keys:
            self.assertIn(k.time_of_day.name, k.region_name())

    def test_friendly_names_include_time_suffix(self):
        grass_keys = [k for k in self.world.generated_wild
                      if k.encounter_type is EncounterType.Grass and not k.is_swarm]
        for k in grass_keys:
            self.assertIn(f"Land - {k.time_of_day.name}", k.friendly_region_name())

    def test_triple_grass_key_count(self):
        """Enabled should have 3x the grass keys compared to disabled."""
        grass_keys = [k for k in self.world.generated_wild
                      if k.encounter_type is EncounterType.Grass and not k.is_swarm]
        region_ids = set(k.region_id for k in grass_keys)
        self.assertEqual(len(grass_keys), len(region_ids) * 3)


class GrassTimeOfDayRandomizedTest(PokemonCrystalTestBase):
    options = {
        "time_of_day_encounters": True,
        "randomize_wilds": "completely_random",
    }

    def test_different_pokemon_across_time_periods(self):
        """With randomization, at least some areas should have different Pokemon across time periods."""
        grass_keys = [k for k in self.world.generated_wild
                      if k.encounter_type is EncounterType.Grass]
        region_ids = set(k.region_id for k in grass_keys)

        different_count = 0
        for region_id in region_ids:
            region_keys = [k for k in grass_keys if k.region_id == region_id]
            encounter_sets = [
                frozenset(e.pokemon for e in self.world.generated_wild[k])
                for k in region_keys
            ]
            if len(set(encounter_sets)) > 1:
                different_count += 1

        self.assertGreater(different_count, 0,
                           "At least some areas should have different Pokemon across time periods")
