from .bases import PokemonCrystalTestBase
from ..data import data
from ..items import create_item_label_to_code_map


class TestItemValuePlandoVanilla(PokemonCrystalTestBase):
    options = {
        "randomize_item_values": "false",
        "item_value_plando": {
            "Poke Ball": 150,
            "Rare Candy": 5000,
        },
    }

    def test_plando_values_applied(self) -> None:
        world = self.multiworld.worlds[1]
        label_to_id = create_item_label_to_code_map()
        self.assertEqual(world.generated_item_values[label_to_id["Poke Ball"]], 150)
        self.assertEqual(world.generated_item_values[label_to_id["Rare Candy"]], 5000)
        ultra_ball = label_to_id["Ultra Ball"]
        self.assertEqual(world.generated_item_values[ultra_ball], data.items[ultra_ball].price)


class TestItemValuePlandoRandomized(PokemonCrystalTestBase):
    options = {
        "randomize_item_values": "true",
        "minimum_item_value": 300,
        "maximum_item_value": 400,
        "item_value_plando": {
            "Poke Ball": 150,
        },
    }

    def test_plando_overrides_randomized(self) -> None:
        world = self.multiworld.worlds[1]
        label_to_id = create_item_label_to_code_map()
        self.assertEqual(world.generated_item_values[label_to_id["Poke Ball"]], 150)
        self.assertTrue(300 <= world.generated_item_values[label_to_id["Ultra Ball"]] <= 400)
