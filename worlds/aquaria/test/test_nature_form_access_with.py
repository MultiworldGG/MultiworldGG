"""
Author: Louis M
Date: Thu, 18 Apr 2024 18:45:56 +0000
Description: Unit test used to test accessibility of locations with and without the nature form
"""

from . import AquariaTestBase
from ..Items import ItemNames
from ..Locations import AquariaLocationNames
from ..Options import UnconfineHomeWater
from ...osrs import LocationNames


class NatureFormAccessTest(AquariaTestBase):
    """Unit test used to test accessibility of locations with and without the nature form"""
    options = {
        "unconfine_home_water": UnconfineHomeWater.option_via_energy_door,
    }

    def test_nature_form_location(self) -> None:
        """Test locations that require nature form"""
        locations = [
            AquariaLocationNames.SONG_CAVE_ANEMONE_SEED,
            AquariaLocationNames.MITHALAS_CITY_FIRST_URN_IN_THE_CITY_RESERVE,
            AquariaLocationNames.MITHALAS_CITY_SECOND_URN_IN_THE_CITY_RESERVE,
            AquariaLocationNames.MITHALAS_CITY_THIRD_URN_IN_THE_CITY_RESERVE,
            AquariaLocationNames.MITHALAS_CITY_FIRST_URN_IN_ONE_OF_THE_HOMES,
            AquariaLocationNames.MITHALAS_CITY_SECOND_URN_IN_ONE_OF_THE_HOMES,
            AquariaLocationNames.MITHALAS_CITY_CASTLE_FIRST_URN_ON_THE_ENTRANCE_PATH,
            AquariaLocationNames.MITHALAS_CITY_CASTLE_SECOND_URN_ON_THE_ENTRANCE_PATH,
            AquariaLocationNames.MITHALAS_CITY_CASTLE_FIRST_URN_OF_THE_SINGLE_LAMP_PATH,
            AquariaLocationNames.MITHALAS_CITY_CASTLE_SECOND_URN_OF_THE_SINGLE_LAMP_PATH,
            AquariaLocationNames.MITHALAS_CITY_CASTLE_URN_IN_THE_BEDROOM,
            AquariaLocationNames.MITHALAS_CITY_CASTLE_URN_IN_THE_BOTTOM_ROOM,
            AquariaLocationNames.KELP_FOREST_SPRITE_CAVE_BULB_IN_THE_SECOND_ROOM,
            AquariaLocationNames.KELP_FOREST_SPRITE_CAVE_SEED_BAG


        ]
        items = [ItemNames.NATURE_FORM]
        self.assertAccessWith(locations, items)
