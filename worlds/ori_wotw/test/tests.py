from . import WotWTestBase
from ..LocationGroups import location_regions, loc_sets
from ..Locations import loc_table

class TestLocations(WotWTestBase):
    def test_location_groups(self) -> None:
        """Test that the location groups contain all locations, and without duplicates."""
        tested_locations: list[str] = []
        remaining_locations: list[str] = list(loc_table.keys()).copy()
        for locs in location_regions.values():
            for loc in locs:
                assert loc in loc_table, f"{loc} is present in `location_regions`, but not in `loc_table`"
                assert loc not in tested_locations, f"{loc} is present multiple times in `location_regions`"
                tested_locations.append(loc)
                remaining_locations.remove(loc)
        assert not remaining_locations, f"{remaining_locations} are not present in `location_regions`"

        tested_locations = []
        remaining_locations= list(loc_table.keys()).copy()
        for locs in loc_sets.values():
            for loc in locs:
                assert loc in loc_table, f"{loc} is present in `loc_sets`, but not in `loc_table`"
                assert loc not in tested_locations, f"{loc} is present multiple times in `loc_sets`"
                tested_locations.append(loc)
                remaining_locations.remove(loc)
        assert not remaining_locations, f"{remaining_locations} are not present in `loc_sets`"
