"""
Author: Louis M
Date: Sun, 06 Apr 2025 14:00:32 +0000
Description: Unit test used to test the Trident Head With Fish Form Glitch "on" option
"""
from BaseClasses import CollectionState
from . import AquariaTestBase
from ..Items import ItemNames
from ..Options import UnconfineHomeWater, TridentHeadWithFishFormGlitch
from ..Locations import AquariaLocationNames


class TridentHeadWithFishFormGlitchOnTest(AquariaTestBase):
    """Unit test used to test the Trident Head With Fish Form Glitch "on" option"""
    options = {
        "unconfine_home_water": UnconfineHomeWater.option_via_energy_door,
        "trident_head_with_fish_form_glitch": TridentHeadWithFishFormGlitch.option_true
    }

    def test_trident_head_with_fish_form_glitch_on(self) -> None:
        """Test the Trident Head With Fish Form Glitch "on" option"""
        state = CollectionState(self.multiworld)
        trident_location = self.multiworld.get_location(
            AquariaLocationNames.MITHALAS_CITY_CASTLE_TRIDENT_HEAD, 1)
        self.assertFalse(trident_location.can_reach(state))
        state.collect(self.get_item_by_name(ItemNames.FISH_FORM))
        trident_location = self.multiworld.get_location(
            AquariaLocationNames.MITHALAS_CITY_CASTLE_TRIDENT_HEAD, 1)
        self.assertTrue(trident_location.can_reach(state))