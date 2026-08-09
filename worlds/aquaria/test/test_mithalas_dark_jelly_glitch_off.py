"""
Author: Louis M
Date: Sun, 06 Apr 2025 14:00:32 +0000
Description: Unit test for the Mithalas Dark Jelly glitch off
"""

from . import AquariaTestBase
from ..Items import ItemNames
from ..Options import MithalasDarkJellyGlitch, UnconfineHomeWater


class MithalasDarkJellyGlitchOffTest(AquariaTestBase):
    """Unit test for the Mithalas Dark Jelly glitch off"""
    options = {
        "mithalas_dark_jelly_glitch": MithalasDarkJellyGlitch.option_false,
        "unconfine_home_water": UnconfineHomeWater.option_via_energy_door
    }


    def test_mithalas_dark_jelly_glitch_off(self) -> None:
        """Test Region accessible without Mithalas Dark Jelly glitch"""
        regions = [
            'Sprite cave after the plant tube'
        ]
        initial_items = [ItemNames.ENERGY_FORM]
        tested_items = [ItemNames.NATURE_FORM]
        self.assertAccessWith(regions, tested_items, initial_items, resolution_hint="Region")
