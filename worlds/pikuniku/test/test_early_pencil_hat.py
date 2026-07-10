from BaseClasses import CollectionState
from Fill import distribute_items_restrictive

from .bases import PikunikuTestBase


class EarlyPencilHatTestMixin:
    def assert_pencil_hat_is_in_sphere_one(self) -> None:
        distribute_items_restrictive(self.multiworld)

        pencil_hat_location = next(
            location
            for location in self.multiworld.get_filled_locations()
            if location.item.name == "Pencil Hat" and location.item.player == self.player
        )

        empty_state = CollectionState(self.multiworld)
        self.assertTrue(pencil_hat_location.can_reach(empty_state))


class TestEarlyLocalPencilHat(PikunikuTestBase, EarlyPencilHatTestMixin):
    options = {
        "early_pencil_hat": "early_local",
    }

    def test_pencil_hat_is_in_sphere_one(self) -> None:
        self.assert_pencil_hat_is_in_sphere_one()

    def test_pencil_hat_is_local(self) -> None:
        self.assertIn("Pencil Hat", self.multiworld.local_early_items[self.player])


class TestEarlyGlobalPencilHat(PikunikuTestBase, EarlyPencilHatTestMixin):
    options = {
        "early_pencil_hat": "early_global",
    }

    # In a solo multiworld, "early global" still means sphere 1 of this world.
    def test_pencil_hat_is_in_sphere_one(self) -> None:
        self.assert_pencil_hat_is_in_sphere_one()


class TestShuffledPencilHat(PikunikuTestBase):
    options = {
        "early_pencil_hat": "shuffled",
    }

    def test_no_early_item_registered(self) -> None:
        self.assertNotIn("Pencil Hat", self.multiworld.early_items[self.player])
        self.assertNotIn("Pencil Hat", self.multiworld.local_early_items[self.player])
