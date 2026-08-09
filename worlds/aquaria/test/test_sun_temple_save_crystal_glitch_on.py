"""
Author: Louis M
Date: Sat, 05 Apr 2025 16:53:42 +0000
Description: Unit test for the Sun Temple Save Crystal glitch on
"""

from . import AquariaTestBase
from ..Items import ItemNames
from ..Locations import AquariaLocationNames
from ..Options import SunTempleSaveCristalGlitch, UnconfineHomeWater


class SunTempleSaveCrystalGlitchOnTest(AquariaTestBase):
    """Unit test for the Sun Temple Save Crystal glitch on"""
    options = {
        "sun_temple_save_cristal_glitch": SunTempleSaveCristalGlitch.option_true,
        "unconfine_home_water": UnconfineHomeWater.option_via_transturtle
    }


    def test_sun_temple_save_crystal_glitch_on(self) -> None:
        """Test Region accessible with Sun Temple Save Crystal glitch"""
        regions = [
            "The Veil top right area, left of temple",
            "Sun Temple left area entrance",
            "Open Waters top left area",
            "Open Waters top right area", 
            "Open Waters bottom left area",
            "Open Waters bottom right area", 
            "Open Waters skeleton path", 
            "Mithalas City", 
            "Mithalas castle",
            "Kelp Forest top left area", 
            "Kelp Forest top right area", 
            "Kelp Forest bottom left area",
            "Kelp Forest bottom right area", 
            "Kelp Forest Drunian God room entrance", 
            "Sprite cave",
            "Kelp Forest fish cave", 
            "The Veil top left area",
            "The Veil top right area, right of temple", 
            "The Veil bottom left area", 
            "The Veil bottom right area",
            "The Veil top left area, turtle cave", 
            "The Veil top left area, turtle cave Bubble Cliff",
            "Sun Temple right area"
        ]
        tested_items = [ItemNames.TRANSTURTLE_VEIL_TOP_RIGHT]
        self.assertAccessWith(regions, tested_items, resolution_hint="Region")
