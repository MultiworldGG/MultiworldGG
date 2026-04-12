from . import RabiRibiTestBase
from ..names import ItemName

class GoalTestEggRounding(RabiRibiTestBase):
    options = {
        "max_number_of_easter_eggs": 19,
        "percentage_of_easter_eggs": 75
    }

    def test_egg_rounding(self) -> None:
        """
        Ensure that egg requirements are rounded down.
        """
        self.assertBeatable(False)
        for _ in range(14):
            item = self.get_item_by_name(ItemName.easter_egg)
            self.collect(item)
        self.assertBeatable(True)

class GoalTestEggNonZero(RabiRibiTestBase):
    options = {
        "max_number_of_easter_eggs": 10,
        "percentage_of_easter_eggs": 1
    }

    def test_egg_non_zero(self) -> None:
        """
        Ensure that at least one egg is always required to beat the game.
        """
        self.assertBeatable(False)
        for _ in range(1):
            item = self.get_item_by_name(ItemName.easter_egg)
            self.collect(item)
        self.assertBeatable(True)