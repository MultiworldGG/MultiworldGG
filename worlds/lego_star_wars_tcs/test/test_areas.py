from unittest import TestCase

from ..data.areas import Area, ALL_CHAPTER_AREAS
from ..data.extras import Extra
from ..data.locations import LOCATION_NAME_TO_ID


class TestAreas(TestCase):
    def test_character_shop_unlocks(self):
        for area in Area:
            purchase_characters = area.get_purchase_characters()
            for character in purchase_characters:
                self.assertIn(character.get_purchase_location_name(), LOCATION_NAME_TO_ID)

    def test_power_bricks(self):
        for area in Area:
            extra = area.extra
            if area in ALL_CHAPTER_AREAS:
                self.assertIsNotNone(extra)
                self.assertIn(extra, Extra)
                self.assertIn(extra.get_purchase_location_name(), LOCATION_NAME_TO_ID)
            else:
                self.assertIsNone(extra)

    def test_playable_level_ids(self):
        all_ids_so_far = set()
        for area in Area:
            with self.subTest(area.name):
                levels = area.levels
                self.assertEqual(len(levels), len(set(levels)))
                self.assertTrue(all_ids_so_far.isdisjoint(levels))
                all_ids_so_far.update(levels)
