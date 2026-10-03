from BaseClasses import CollectionState
from .bases import PokemonCrystalTestBase
from ..data import EncounterType, GrassTimeOfDay


TOD_ITEM_NAMES = {"Morn", "Day", "Nite"}


class UnlockableTodDisabledTest(PokemonCrystalTestBase):
    options = {
        "time_of_day_encounters": True,
        "unlockable_time_of_day": False,
    }

    def test_no_tod_items_in_pool(self):
        item_names = {item.name for item in self.multiworld.itempool}
        self.assertFalse(item_names & TOD_ITEM_NAMES,
                         "ToD items should not be in pool when option is off")

    def test_no_tod_items_precollected(self):
        precollected = {item.name for item in self.multiworld.precollected_items[self.player]}
        self.assertFalse(precollected & TOD_ITEM_NAMES,
                         "ToD items should not be precollected when option is off")


class UnlockableTodEnabledTest(PokemonCrystalTestBase):
    options = {
        "time_of_day_encounters": True,
        "unlockable_time_of_day": True,
        "wild_encounter_methods_required": ["Land"],
    }

    def test_one_tod_item_precollected(self):
        precollected = [item.name for item in self.multiworld.precollected_items[self.player]
                        if item.name in TOD_ITEM_NAMES]
        self.assertEqual(len(precollected), 1,
                         "Exactly one ToD item should be precollected")

    def test_two_tod_items_in_pool(self):
        pool_tod = [item.name for item in self.multiworld.itempool if item.name in TOD_ITEM_NAMES]
        self.assertEqual(len(pool_tod), 2,
                         "Two ToD items should be in the item pool")

    def test_all_three_tod_items_present(self):
        precollected = {item.name for item in self.multiworld.precollected_items[self.player]}
        pool = {item.name for item in self.multiworld.itempool}
        all_items = precollected | pool
        self.assertEqual(all_items & TOD_ITEM_NAMES, TOD_ITEM_NAMES,
                         "All three ToD items should be present across precollected + pool")

    def test_grass_locations_require_tod_item(self):
        grass_keys = [k for k in self.world.generated_wild
                      if k.encounter_type is EncounterType.Grass and k.time_of_day is not None]
        self.assertGreater(len(grass_keys), 0)

        # Find which ToD items are NOT precollected (those are in the pool and can be withheld)
        precollected_names = {item.name for item in self.multiworld.precollected_items[self.player]}
        non_precollected_tods = [tod for tod in GrassTimeOfDay if tod.name not in precollected_names]
        self.assertGreater(len(non_precollected_tods), 0)

        for tod in non_precollected_tods:
            tod_keys = [k for k in grass_keys if k.time_of_day is tod]
            if not tod_keys:
                continue
            location_name = f"{tod_keys[0].region_name()}_1"
            self.multiworld.state = CollectionState(self.multiworld)
            self.collect_all_but([tod.name])
            self.assertFalse(self.can_reach_location(location_name),
                             f"Location {location_name} should not be reachable without {tod.name}")


class UnlockableTodWithoutGrassTodTest(PokemonCrystalTestBase):
    options = {
        "time_of_day_encounters": False,
        "unlockable_time_of_day": True,
    }

    def test_no_tod_items_when_grass_tod_off(self):
        item_names = {item.name for item in self.multiworld.itempool}
        precollected = {item.name for item in self.multiworld.precollected_items[self.player]}
        all_items = item_names | precollected
        self.assertFalse(all_items & TOD_ITEM_NAMES,
                         "ToD items should not exist when time_of_day_encounters is off")
