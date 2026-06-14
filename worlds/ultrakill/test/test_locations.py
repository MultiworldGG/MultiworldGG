from . import UltrakillTestBase
from ..Regions import Regions
from ..Locations import location_list


class TestLocationRegions(UltrakillTestBase):
    def test_location_regions(self) -> None:
        for location in location_list:
            if location.name[3] == ":":
                self.assertEqual(Regions.get_from_short_name(location.name[:3:]), location.region)