"""
Author: Louis M
Date: Sat, 05 Apr 2025 16:53:42 +0000
Description: Unit test used to test the far_away_sing_bulb "off" option
"""
from BaseClasses import CollectionState
from . import AquariaTestBase
from ..Items import ItemNames
from ..Options import UnconfineHomeWater, FarAwaySingBulb
from ..Locations import AquariaLocationNames


class FarAwaySingBulbOffTest(AquariaTestBase):
    """Unit test used to test the far_away_sing_bulb "off" option"""
    options = {
        "unconfine_home_water": UnconfineHomeWater.option_via_energy_door,
        "far_away_sing_bulb": FarAwaySingBulb.option_false
    }

    def test_far_away_sing_off(self) -> None:
        """Test the far_away_sing_bulb "off" option"""
        state = CollectionState(self.multiworld)
        state.collect(self.get_item_by_name(ItemNames.BEAST_FORM))
        naija_energy_door_bulb_location = self.multiworld.get_location(
            AquariaLocationNames.NAIJA_S_HOME_BULB_AFTER_THE_ENERGY_DOOR, 1)
        self.assertFalse(naija_energy_door_bulb_location.can_reach(state))
        veil_bottom_spirit_cristal_bulb = self.multiworld.get_location(
            AquariaLocationNames.THE_VEIL_BOTTOM_AREA_BULB_IN_THE_SPIRIT_PATH, 1)
        self.assertFalse(veil_bottom_spirit_cristal_bulb.can_reach(state))