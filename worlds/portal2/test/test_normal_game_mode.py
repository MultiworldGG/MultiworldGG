from .bases import Portal2TestBase
from ..Options import GameModeOption


class NormalGameMode(Portal2TestBase):
    options = {
        "game_mode": GameModeOption.NORMAL
    }
    
    run_default_tests = False
    
    def test_no_duplicate_locations(self) -> None:
        """Test there are no duplicate locations"""
        location_names = [loc.name for loc in self.world.get_locations()]
        location_names_dupes_removed = list(set(location_names))
        self.assertListEqual(sorted(location_names), sorted(location_names_dupes_removed))
