import unittest

from BaseClasses import MultiWorld, CollectionState, ItemClassification
from . import LunacidTestBase
from .. import LunacidWorld, location_table, all_drops_by_enemy, Endings
from ..data.location_data import *
from ..data.item_data import all_items
from ..strings.items import GenericItem, Alchemy, Creation


class TestGeneric(LunacidTestBase):

    def test_if_base_locations_appended(self):
        for location in wings_rest:
            self.assertIn(location, base_locations)
        for location in the_fetid_mire:
            self.assertIn(location, base_locations)
        for location in yosei_forest:
            self.assertIn(location, base_locations)
        for location in forest_canopy:
            self.assertIn(location, base_locations)
        for location in hollow_basin:
            self.assertIn(location, base_locations)
        for location in forbidden_archives:
            self.assertIn(location, base_locations)
        for location in accursed_tomb:
            self.assertIn(location, base_locations)
        for location in the_sanguine_sea:
            self.assertIn(location, base_locations)
        for location in laetus_chasm:
            self.assertIn(location, base_locations)
        for location in great_well_surface:
            self.assertIn(location, base_locations)
        for location in castle_le_fanu:
            self.assertIn(location, base_locations)
        for location in tower_of_abyss:
            self.assertIn(location, base_locations)
        for location in sealed_ballroom:
            self.assertIn(location, base_locations)
        for location in boiling_grotto:
            self.assertIn(location, base_locations)
        for location in throne_room:
            self.assertIn(location, base_locations)
        for location in terminus_prison:
            self.assertIn(location, base_locations)
        for location in labyrinth_of_ash:
            self.assertIn(location, base_locations)
        for location in forlorn_arena:
            self.assertIn(location, base_locations)
        for location in chamber_of_fate:
            self.assertIn(location, base_locations)
        self.assertTrue(229 == len(base_locations), f"Location count mismatch, got {len(base_locations)}.")

    def test_no_duplicate_ids(self):
        constructed_item_table = {}
        for item in all_items:
            if item.name not in constructed_item_table:
                constructed_item_table[item.name] = item.code
                continue
            self.assertFalse(item.name not in constructed_item_table, f"Found duplicate ID for {item.name}: {item.code} vs {constructed_item_table[item.name]}")
        constructed_location_table = {}
        for location in location_table:
            if location.name not in constructed_location_table:
                constructed_item_table[location.name] = location.location_id
                continue
            self.assertFalse(location.name not in constructed_location_table,
                             f"Found duplicate ID for {location.name}: {location.location_id} vs {constructed_item_table[location.name]}")
