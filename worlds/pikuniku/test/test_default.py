from .. import locations
from .bases import PikunikuTestBase


class TestDefaultOptions(PikunikuTestBase):
    options = {
        "coinsanity": False,
        "coop_levels": False,
    }

    def test_no_coin_locations(self) -> None:
        location_names = {location.name for location in self.multiworld.get_locations(self.player)}
        for coin_location in locations.COIN_LOCATIONS:
            self.assertNotIn(coin_location.name, location_names)

    def test_no_coop_locations_or_items(self) -> None:
        location_names = {location.name for location in self.multiworld.get_locations(self.player)}
        for coop_location in locations.COOP_LOCATIONS:
            self.assertNotIn(coop_location.name, location_names)
        self.assertFalse(self.get_items_by_name("Co-op Level Access"))

    def test_coins_are_not_progression(self) -> None:
        for coin_item in self.get_items_by_name("5 Coins"):
            self.assertFalse(coin_item.advancement)

    def test_victory_requirements(self) -> None:
        self.assertBeatable(False)
        for item_name in locations.SUNSHINE_HQ:
            self.collect_by_name(item_name)
        self.assertBeatable(True)
