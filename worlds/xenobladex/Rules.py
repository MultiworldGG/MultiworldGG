from typing import Dict
from BaseClasses import MultiWorld
from .Items import create_item


def set_rules(world: MultiWorld, player: int, item_name_to_id: Dict[str, int]):
    """Setting all the rules for region connections and region->item connections"""
    world.get_location("EBK: Lao - Chp 12: Story", player).place_locked_item(
        create_item("KEY: Victory", player, item_name_to_id["KEY: Victory"]))
    world.completion_condition[player] = lambda state: state.has("KEY: Victory", player)
