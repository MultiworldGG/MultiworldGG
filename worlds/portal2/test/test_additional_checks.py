from .bases import Portal2TestBase
from ..Options import GameModeOption
from ..Locations import wheatley_monitor_table, ratman_den_locations_table, cutscene_completion_table, map_complete_table, item_location_table


class AdditionalChecks(Portal2TestBase):
    options = {
        "game_mode": GameModeOption.NORMAL,
        "cutscene_levels": True,
        "wheatley_monitors": True,
        "ratman_dens": True
    }
    
    def test_all_additional_locations_placed(self) -> None:
        """Test all additional locations are placed"""
        location_names = [loc.name for loc in self.world.get_locations() if not(loc.name in map_complete_table or loc.name in item_location_table)]
        location_names.remove("Beat Final Level")
        additional_locations = list(wheatley_monitor_table) + list(ratman_den_locations_table) + list(cutscene_completion_table)
        self.assertListEqual(sorted(additional_locations), sorted(location_names))
