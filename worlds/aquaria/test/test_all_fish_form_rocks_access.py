"""
Author: Louis M
Date: Sat, 05 Apr 2025 16:53:42 +0000
Description: Unit test used to test the go_around_rocks_with_fish_form "all" option
"""

from . import AquariaTestBase
from ..Items import ItemNames
from ..Options import UnconfineHomeWater, GoAroundRocksWithFishForm
from ..Locations import AquariaLocationNames


class AllFishFormRocksAccessTest(AquariaTestBase):
    """Unit test used to test the go_around_rocks_with_fish_form "all" option"""
    options = {
        "unconfine_home_water": UnconfineHomeWater.option_via_energy_door,
        "go_around_rocks_with_fish_form": GoAroundRocksWithFishForm.option_all
    }

    def test_all_fish_form_rocks_location(self) -> None:
        """Test the go_around_rocks_with_fish_form "all" option"""
        locations = [
            AquariaLocationNames.OPEN_WATERS_BOTTOM_LEFT_AREA_BULB_INSIDE_THE_LOWEST_FISH_PASS,
            AquariaLocationNames.MITHALAS_CITY_DOLL,
            AquariaLocationNames.KELP_FOREST_TOP_RIGHT_AREA_BULB_IN_THE_TOP_FISH_PASS,
            AquariaLocationNames.KELP_FOREST_BOTTOM_LEFT_AREA_BULB_CLOSE_TO_THE_SPIRIT_CRYSTALS,
            AquariaLocationNames.MERMOG_CAVE_BULB_IN_THE_LEFT_PART_OF_THE_CAVE,
            AquariaLocationNames.ARNASSI_RUINS_TRANSTURTLE,
            AquariaLocationNames.ARNASSI_RUINS_ARNASSI_ARMOR,
            AquariaLocationNames.MITHALAS_CITY_URN_INSIDE_A_HOME_FISH_PASS,
            AquariaLocationNames.THE_VEIL_TOP_LEFT_AREA_BULB_INSIDE_THE_FISH_PASS,
            AquariaLocationNames.HOME_WATERS_TRANSTURTLE,
            AquariaLocationNames.HOME_WATERS_BULB_IN_THE_BOTTOM_LEFT_ROOM,
            AquariaLocationNames.HOME_WATERS_BULB_IN_THE_PATH_BELOW_NAUTILUS_PRIME,
            AquariaLocationNames.THE_VEIL_BOTTOM_AREA_VERSE_EGG,
            AquariaLocationNames.THE_VEIL_TOP_LEFT_AREA_BULB_HIDDEN_BEHIND_THE_BLOCKING_ROCK,
            AquariaLocationNames.ENERGY_TEMPLE_FIRST_AREA_BEATING_THE_ENERGY_STATUE,
            AquariaLocationNames.ENERGY_TEMPLE_FIRST_AREA_BULB_IN_THE_BOTTOM_ROOM_BLOCKED_BY_A_ROCK,
            AquariaLocationNames.ENERGY_TEMPLE_ENERGY_IDOL,
            AquariaLocationNames.SONG_CAVE_VERSE_EGG,
            AquariaLocationNames.TURTLE_CAVE_TURTLE_EGG
        ]
        initial_item = [ItemNames.BEAST_FORM]
        tested_items = [ItemNames.FISH_FORM]
        self.assertAccessWith(locations, tested_items, initial_item, resolution_hint="Location")
