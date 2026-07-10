from .. import locations
from .bases import PikunikuTestBase


class TestCoopLevels(PikunikuTestBase):
    options = {
        "coop_levels": True,
    }

    def test_all_coop_locations_exist(self) -> None:
        location_names = {location.name for location in self.multiworld.get_locations(self.player)}
        for coop_location in locations.COOP_LOCATIONS:
            self.assertIn(coop_location.name, location_names)

    def test_coop_access_item_exists(self) -> None:
        self.assertTrue(self.get_items_by_name("Co-op Level Access"))

    def test_coop_locations_require_access(self) -> None:
        coop_location_names = [data.name for data in locations.COOP_LOCATIONS]
        self.assertAccessDependency(coop_location_names, [["Co-op Level Access"]])
