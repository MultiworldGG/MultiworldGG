from .. import locations
from .bases import PikunikuTestBase


class TestCoinsanity(PikunikuTestBase):
    options = {
        "coinsanity": True,
    }

    def test_all_coin_locations_exist(self) -> None:
        location_names = {location.name for location in self.multiworld.get_locations(self.player)}
        for coin_location in locations.COIN_LOCATIONS:
            self.assertIn(coin_location.name, location_names)

    def test_one_five_coins_item_per_coin_location(self) -> None:
        self.assertEqual(len(self.get_items_by_name("5 Coins")), len(locations.COIN_LOCATIONS))

    def test_exact_amount_of_five_coins_are_progression(self) -> None:
        progression_coins = [item for item in self.get_items_by_name("5 Coins") if item.advancement]
        self.assertEqual(len(progression_coins), locations.PROGRESSION_FIVE_COINS_COUNT)
        self.assertEqual(locations.PROGRESSION_FIVE_COINS_COUNT, 18)

    def test_shops_require_coins(self) -> None:
        all_shop_locations = sorted(locations.SHOP_PRICES)
        self.assertAccessDependency(all_shop_locations, [["5 Coins"]])

    def test_most_expensive_shop_needs_all_progression_coins(self) -> None:
        # The X-Ray Goggles (70 coins) plus all cheaper purchases (26 coins) require all 20 progression
        # "5 Coins" items, since coins are spent on purchase and logic must stay affordable.
        progression_coins = [item for item in self.get_items_by_name("5 Coins") if item.advancement]
        self.collect_all_but("5 Coins")

        goggles = self.world.get_location("Forest X-Ray Goggles Purchase")
        self.collect(progression_coins[:-1])
        self.assertFalse(goggles.can_reach(self.multiworld.state))
        self.collect(progression_coins[-1:])
        self.assertTrue(goggles.can_reach(self.multiworld.state))

    def test_cheapest_shop_needs_one_five_coins(self) -> None:
        # The Sunglasses cost 1 coin, so a single "5 Coins" item is enough.
        progression_coins = [item for item in self.get_items_by_name("5 Coins") if item.advancement]
        self.collect_all_but("5 Coins")

        sunglasses = self.world.get_location("Forest Sunglasses Purchase")
        self.assertFalse(sunglasses.can_reach(self.multiworld.state))
        self.collect(progression_coins[:1])
        self.assertTrue(sunglasses.can_reach(self.multiworld.state))
