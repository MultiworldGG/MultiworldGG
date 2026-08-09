"""
Author: Louis M
Date: Sun, 06 Apr 2025 14:00:32 +0000
Description: Unit test used to test the bind_rock_urchin_costume Glitch "off" option
"""
from BaseClasses import CollectionState
from . import AquariaTestBase
from ..Items import ItemNames
from ..Options import UnconfineHomeWater, BindRockUrchinCostume
from ..Locations import AquariaLocationNames


class BindRockUrchinCostumeOffTest(AquariaTestBase):
    """Unit test used to test the bind_rock_urchin_costume Glitch "off" option"""
    options = {
        "unconfine_home_water": UnconfineHomeWater.option_via_transturtle,
        "bind_rock_urchin_costume": BindRockUrchinCostume.option_false
    }

    def test_bind_rock_urchin_costume_off(self) -> None:
        """Test the bind_rock_urchin_costume Glitch "off" option"""
        state = CollectionState(self.multiworld)
        state.collect(self.get_item_by_name(ItemNames.TRANSTURTLE_VEIL_TOP_LEFT))
        state.collect(self.get_item_by_name(ItemNames.BIND_SONG))
        location = self.multiworld.get_location(
            AquariaLocationNames.TURTLE_CAVE_URCHIN_COSTUME, 1)
        self.assertFalse(location.can_reach(state))