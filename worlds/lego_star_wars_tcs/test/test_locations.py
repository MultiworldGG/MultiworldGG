from unittest import TestCase

from ..data.items.all_character_items import CHARACTER_TO_ITEM_DATA
from ..data.characters import CHARACTER_TO_STORY_AREA, CHARACTER_TO_PURCHASE_AREA
from ..data.locations import LOCATION_NAME_TO_ID
from ..data.shop import CHARACTER_SHOP_SLOTS


_EXPECTED_LOCATION_COUNT = 657


class TestLocations(TestCase):
    def test_shop_slot_locations(self):
        for character in CHARACTER_SHOP_SLOTS:
            self.assertIn(character, CHARACTER_TO_ITEM_DATA)
            self.assertIn(character.get_purchase_location_name(), LOCATION_NAME_TO_ID)

    def test_datapackage_count(self):
        self.assertEqual(_EXPECTED_LOCATION_COUNT, len(LOCATION_NAME_TO_ID))

    def test_datapackage_unique_names(self):
        self.assertEqual(len(LOCATION_NAME_TO_ID), len(set(LOCATION_NAME_TO_ID.values())))

    def test_story_characters_have_locations(self):
        for character in CHARACTER_TO_STORY_AREA:
            self.assertIn(character.get_level_completion_unlock_location_name(), LOCATION_NAME_TO_ID)

    def test_purchase_characters_have_locations(self):
        for character in CHARACTER_TO_PURCHASE_AREA:
            self.assertIn(character.get_purchase_location_name(), LOCATION_NAME_TO_ID)
