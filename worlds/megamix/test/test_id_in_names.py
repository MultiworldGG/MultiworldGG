import re

from . import MegaMixTestBase


class IDNames(MegaMixTestBase):
    """Test that item/location names contain a song ID then verify that ID matches its item/loc ID."""
    item_regex = r"(?P<name>.*?) \[(?P<id>\d+)\]$"
    location_regex = r"(?P<name>.*?) \[(?P<id>\d+)\]-(?P<suffix>\d+)$"

    def test_item_names_have_id(self):
        """Test all song item names include *a* song ID.
        As of writing, song item IDs start at 10. 1-9 are reserved for non-song items."""
        world = self.get_world()

        quick = [name for name, locID in world.item_name_to_id.items() if not re.search(self.item_regex, name) and locID >= 100]
        self.assertEqual(0, len(quick), f"Item names without song IDs: {quick}")

    def test_loc_names_have_id(self):
        """Test all location names include *a* song ID."""
        world = self.get_world()

        quick = [name for name in world.location_name_to_id if not re.search(self.location_regex, name)]
        self.assertEqual(0, len(quick), f"Location names without song IDs: {quick}")

    def test_verify_item_names_for_id(self):
        """Verify the ID in an item name matches its item ID.
        As of writing, items IDs are originalSongID*10."""
        world = self.get_world()

        for name, itemID in world.item_name_to_id.items():
            if itemID < 100:
                continue

            match = re.match(self.item_regex, name)
            self.assertIsNotNone(match, f"Failed to match item_regex to item name: {name}")

            given_id = int(match.group('id'))

            self.assertEqual(given_id, (itemID // 100), f"Song ID in item name does not match item ID: {name}")

    def test_verify_loc_names_for_id(self):
        """Verify the ID in a location name matches its location ID.
        As of writing, location IDs are originalSongID*10."""
        world = self.get_world()

        for name, locID in world.location_name_to_id.items():
            match = re.match(self.location_regex, name)
            self.assertIsNotNone(match, f"Failed to match location_regex to location name: {name}")

            given_id = int(match.group('id'))

            self.assertEqual(given_id, (locID // 100), f"Song ID in location name does not match location ID: {name}")
