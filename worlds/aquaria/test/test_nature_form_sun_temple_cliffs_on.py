"""
Author: Louis M
Date: Sun, 06 Apr 2025 14:00:32 +0000
Description: Unit test used to test the sun_temple_cliff_nature_jump_glitch Glitch "off" option
"""
from BaseClasses import CollectionState
from . import AquariaTestBase
from ..Items import ItemNames
from ..Options import UnconfineHomeWater, SunTempleCliffNatureJumpGlitch
from ..Locations import AquariaLocationNames


class SunTempleCliffNatureFormGlitchOffTest(AquariaTestBase):
    """Unit test used to test the sun_temple_cliff_nature_jump_glitch Glitch "off" option"""
    options = {
        "unconfine_home_water": UnconfineHomeWater.option_via_energy_door,
        "sun_temple_cliff_nature_jump_glitch": SunTempleCliffNatureJumpGlitch.option_true
    }

    def test_sun_temple_cliff_nature_jump_glitch_off(self) -> None:
        """Test the sun_temple_cliff_nature_jump_glitch Glitch "off" option"""
        state = CollectionState(self.multiworld)
        state.collect(self.get_item_by_name(ItemNames.BEAST_FORM))
        state.collect(self.get_item_by_name(ItemNames.SUN_FORM))
        first_cliff_location = self.multiworld.get_location(
            AquariaLocationNames.SUN_TEMPLE_BOSS_PATH_FIRST_CLIFF_BULB, 1)
        self.assertFalse(first_cliff_location.can_reach(state))
        second_cliff_location = self.multiworld.get_location(
            AquariaLocationNames.SUN_TEMPLE_BOSS_PATH_SECOND_CLIFF_BULB, 1)
        self.assertFalse(second_cliff_location.can_reach(state))
        state.collect(self.get_item_by_name(ItemNames.NATURE_FORM))
        self.assertTrue(first_cliff_location.can_reach(state))
        self.assertTrue(second_cliff_location.can_reach(state))