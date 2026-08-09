"""
Author: Louis M
Date: Sat, 05 Apr 2025 16:53:42 +0000
Description: Unit test for the Sun Temple Save Crystal glitch off
"""

from . import AquariaTestBase
from ..Items import ItemNames
from ..Locations import AquariaLocationNames
from ..Options import SunTempleSaveCristalGlitch, UnconfineHomeWater


class SunTempleSaveCrystalGlitchOffTest(AquariaTestBase):
    """Unit test for the Sun Temple Save Crystal glitch off"""
    options = {
        "sun_temple_save_cristal_glitch": SunTempleSaveCristalGlitch.option_false,
        "unconfine_home_water": UnconfineHomeWater.option_via_transturtle
    }


    def test_sun_temple_save_crystal_glitch_off(self) -> None:
        """Test Region accessible without Sun Temple Save Crystal glitch"""
        regions = [
            "The Veil top right area, left of temple",
            "Sun Temple left area entrance"
        ]
        tested_items = [ItemNames.TRANSTURTLE_VEIL_TOP_RIGHT]
        self.assertAccessWith(regions, tested_items, resolution_hint="Region")
