from .bases import PokemonCrystalTestBase
from ..data import EncounterType, FishTimeOfDay, FishingRodType, EncounterKey, data as crystal_data


def assert_nite_keys_hold_only_time_slots(test: PokemonCrystalTestBase):
    """Nite fish keys own only their time-varying slots; shared slots live on the Day key."""
    for (region, rod), time_slots in crystal_data.fish_time_slots.items():
        if not time_slots:
            continue
        nite_key = EncounterKey.fish(region, rod, FishTimeOfDay.Nite)
        test.assertIn(nite_key, test.world.generated_wild)
        test.assertEqual(len(test.world.generated_wild[nite_key]), len(time_slots),
                         f"{region}/{rod} Nite key must hold exactly its time-varying slots")


class FishTimeOfDayDisabledTest(PokemonCrystalTestBase):
    options = {
        "time_of_day_encounters": False,
    }

    def test_fish_keys_have_no_time_of_day(self):
        fish_keys = [k for k in self.world.generated_wild
                     if k.encounter_type is EncounterType.Fish]
        self.assertGreater(len(fish_keys), 0)
        for k in fish_keys:
            self.assertIsNone(k.time_of_day,
                              f"Fish key {k.region_id}/{k.fishing_rod} should have time_of_day=None when option is off")

    def test_region_names_have_no_time_suffix(self):
        fish_keys = [k for k in self.world.generated_wild
                     if k.encounter_type is EncounterType.Fish]
        for k in fish_keys:
            self.assertNotIn("_Day", k.region_name())
            self.assertNotIn("_Nite", k.region_name())

    def test_friendly_names_have_no_time_suffix(self):
        fish_keys = [k for k in self.world.generated_wild
                     if k.encounter_type is EncounterType.Fish]
        for k in fish_keys:
            self.assertNotIn(" - Day", k.friendly_region_name())
            self.assertNotIn(" - Nite", k.friendly_region_name())


class FishTimeOfDayEnabledTest(PokemonCrystalTestBase):
    options = {
        "time_of_day_encounters": True,
    }

    def test_only_vanilla_differing_rods_have_tod_split(self):
        """Only (region, rod) pairs whose vanilla data differs by ToD should have Day/Nite keys."""
        fish_keys = [k for k in self.world.generated_wild
                     if k.encounter_type is EncounterType.Fish]
        by_region_rod: dict[tuple[str, FishingRodType], set] = {}
        for k in fish_keys:
            by_region_rod.setdefault((k.region_id, k.fishing_rod), set()).add(k.time_of_day)
        for (region, rod), tods in by_region_rod.items():
            has_time_slots = bool(crystal_data.fish_time_slots.get((region, rod), []))
            if has_time_slots:
                self.assertEqual(tods, {FishTimeOfDay.Day, FishTimeOfDay.Nite},
                                 f"{region}/{rod} has time_slots and should have Day+Nite keys")
            else:
                self.assertEqual(tods, {None},
                                 f"{region}/{rod} has no time_slots and should have a single un-suffixed key")

    def test_split_keys_present_for_shore(self):
        """Vanilla differing slots are Shore Good and Shore Super."""
        fish_keys = {(k.region_id, k.fishing_rod, k.time_of_day)
                     for k in self.world.generated_wild
                     if k.encounter_type is EncounterType.Fish}
        for rod in (FishingRodType.Good, FishingRodType.Super):
            self.assertIn(("Shore", rod, FishTimeOfDay.Day), fish_keys)
            self.assertIn(("Shore", rod, FishTimeOfDay.Nite), fish_keys)

    def test_region_names_match_tod_state(self):
        for k in self.world.generated_wild:
            if k.encounter_type is not EncounterType.Fish:
                continue
            if k.time_of_day is not None:
                self.assertIn(k.time_of_day.name, k.region_name())
            else:
                self.assertNotIn("_Day", k.region_name())
                self.assertNotIn("_Nite", k.region_name())

    def test_friendly_names_match_tod_state(self):
        for k in self.world.generated_wild:
            if k.encounter_type is not EncounterType.Fish:
                continue
            friendly = k.friendly_region_name()
            if k.time_of_day is not None:
                self.assertIn(f"Rod - {k.time_of_day.name}", friendly)
            else:
                self.assertNotIn(" - Day", friendly)
                self.assertNotIn(" - Nite", friendly)

    def test_vanilla_time_group_split(self):
        """With randomize_wilds off, time-varying slots should reflect the vanilla Day/Nite split."""
        # Shore Good rod: vanilla last slot is Corsola (Day) / Staryu (Nite) via TimeFishGroups[0].
        day_key = EncounterKey.fish("Shore", FishingRodType.Good, FishTimeOfDay.Day)
        nite_key = EncounterKey.fish("Shore", FishingRodType.Good, FishTimeOfDay.Nite)
        day_encounters = self.world.generated_wild[day_key]
        nite_encounters = self.world.generated_wild[nite_key]
        # Last slot is the time-varying one; the Nite key holds only that slot
        self.assertEqual(day_encounters[-1].pokemon, "CORSOLA")
        self.assertEqual(nite_encounters[-1].pokemon, "STARYU")

    def test_nite_keys_hold_only_time_slots(self):
        assert_nite_keys_hold_only_time_slots(self)

    def test_round_trip_region_name(self):
        """from_string should round-trip ToD-suffixed fish keys."""
        for k in self.world.generated_wild:
            if k.encounter_type is not EncounterType.Fish:
                continue
            parsed = EncounterKey.from_string(k.region_name())
            self.assertEqual(parsed, k)


class FishTimeSlotsMetadataTest(PokemonCrystalTestBase):
    options = {}

    def test_time_slots_only_for_shore(self):
        """Only Shore Good and Shore Super have vanilla day/nite differences."""
        for (region, rod), slots in crystal_data.fish_time_slots.items():
            if region == "Shore" and rod in (FishingRodType.Good, FishingRodType.Super):
                self.assertEqual(len(slots), 1, f"{region}/{rod} should have 1 time slot")
            else:
                self.assertEqual(slots, [], f"{region}/{rod} should have no time slots")
        self.assertEqual(crystal_data.fish_time_slots[("Shore", FishingRodType.Good)], [(3, 0)])
        self.assertEqual(crystal_data.fish_time_slots[("Shore", FishingRodType.Super)], [(1, 1)])


class FishTimeOfDayRandomizedTest(PokemonCrystalTestBase):
    options = {
        "time_of_day_encounters": True,
        "randomize_wilds": "completely_random",
    }

    def test_different_pokemon_across_time_periods(self):
        """With randomization, time-varying fish slots should produce different Pokemon across Day/Nite."""
        fish_keys = [k for k in self.world.generated_wild
                     if k.encounter_type is EncounterType.Fish]
        by_region_rod: dict[tuple[str, FishingRodType], dict[FishTimeOfDay, list]] = {}
        for k in fish_keys:
            by_region_rod.setdefault((k.region_id, k.fishing_rod), {})[k.time_of_day] = \
                [e.pokemon for e in self.world.generated_wild[k]]

        different_count = 0
        for (region, rod), tod_map in by_region_rod.items():
            time_slots = crystal_data.fish_time_slots.get((region, rod), [])
            if not time_slots:
                continue  # No time-varying slots → single un-suffixed key
            day_list = tod_map[FishTimeOfDay.Day]
            nite_list = tod_map[FishTimeOfDay.Nite]
            for i, (slot_index, _) in enumerate(time_slots):
                if day_list[slot_index] != nite_list[i]:
                    different_count += 1
                    break

        self.assertGreater(different_count, 0,
                           "Time-varying fish slots should yield different Pokemon across Day/Nite under randomization")

    def test_nite_keys_hold_only_time_slots(self):
        assert_nite_keys_hold_only_time_slots(self)


class FishTimeOfDayMutatorPathsTest(PokemonCrystalTestBase):
    """Must-place (DITTO/MAGIKARP/requests) and early-starter placement mutate generated_wild after
    randomization; the Nite-key shape must survive them."""
    options = {
        "time_of_day_encounters": True,
        "randomize_wilds": "completely_random",
        "breeding_methods_required": "with_ditto",
        "randomize_pokemon_requests": "items",
        "dexsanity": 50,
        "dexsanity_starters": "available_early",
    }

    def test_nite_keys_hold_only_time_slots(self):
        assert_nite_keys_hold_only_time_slots(self)
