"""
Author: Louis M
Date: Sun, 06 Apr 2025 14:00:32 +0000
Description: Unit test used to test the Trident Head With Fish Form Glitch "off" option
"""
from BaseClasses import CollectionState
from . import AquariaTestBase
from ..Items import ItemNames
from ..Options import UnconfineHomeWater, TridentHeadWithFishFormGlitch
from ..Locations import AquariaLocationNames


class TridentHeadWithFishFormGlitchOffTest(AquariaTestBase):
    """Unit test used to test the Trident Head With Fish Form Glitch "off" option"""
    options = {
        "unconfine_home_water": UnconfineHomeWater.option_via_energy_door,
        "trident_head_with_fish_form_glitch": TridentHeadWithFishFormGlitch.option_false
    }

    def test_trident_head_with_fish_form_glitch_off(self) -> None:
        """Test the Trident Head With Fish Form Glitch "off" option"""
        state = CollectionState(self.multiworld)
        state.collect(self.get_item_by_name(ItemNames.FISH_FORM))
        trident_location = self.multiworld.get_location(
            AquariaLocationNames.MITHALAS_CITY_CASTLE_TRIDENT_HEAD, 1)
        self.assertFalse(trident_location.can_reach(state))