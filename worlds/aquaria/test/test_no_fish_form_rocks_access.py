"""
Author: Louis M
Date: Sat, 05 Apr 2025 16:53:42 +0000
Description: Unit test used to test the go_around_rocks_with_fish_form "off" option
"""

from . import AquariaTestBase
from ..Items import ItemNames
from ..Options import UnconfineHomeWater, GoAroundRocksWithFishForm
from ..Locations import AquariaLocationNames


class NoFishFormRocksAccessTest(AquariaTestBase):
    """Unit test used to test the go_around_rocks_with_fish_form "off" option"""
    options = {
        "unconfine_home_water": UnconfineHomeWater.option_via_energy_door,
        "go_around_rocks_with_fish_form": GoAroundRocksWithFishForm.option_off
    }

    def test_fish_form_location(self) -> None:
        """Test the go_around_rocks_with_fish_form "off" option"""
        locations = [
            AquariaLocationNames.OPEN_WATERS_BOTTOM_LEFT_AREA_BULB_INSIDE_THE_LOWEST_FISH_PASS,
            AquariaLocationNames.MITHALAS_CITY_DOLL,
            AquariaLocationNames.KELP_FOREST_TOP_RIGHT_AREA_BULB_IN_THE_TOP_FISH_PASS,
            AquariaLocationNames.KELP_FOREST_BOTTOM_LEFT_AREA_BULB_CLOSE_TO_THE_SPIRIT_CRYSTALS,
            AquariaLocationNames.MERMOG_CAVE_BULB_IN_THE_LEFT_PART_OF_THE_CAVE,
            AquariaLocationNames.ARNASSI_RUINS_TRANSTURTLE,
            AquariaLocationNames.ARNASSI_RUINS_ARNASSI_ARMOR,
            AquariaLocationNames.MITHALAS_CITY_URN_INSIDE_A_HOME_FISH_PASS,
            AquariaLocationNames.THE_VEIL_TOP_LEFT_AREA_BULB_INSIDE_THE_FISH_PASS
        ]
        initial_item = [ItemNames.BEAST_FORM]
        tested_items = [ItemNames.FISH_FORM]
        self.assertAccessWith(locations, tested_items, initial_item, resolution_hint="Location")
