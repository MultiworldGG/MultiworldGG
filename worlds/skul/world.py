from collections.abc import Mapping
from typing import Any
from worlds.AutoWorld import World
from . import items, locations, regions, rules, web_world
from . import options as skul_options 

class SkulWorld(World):
    """
    Skul The Hero Slayer is a 2D action platformer where you play as Skul, a skeleton who can swap out his head to gain different abilities.
    """

    game = "Skul: The Hero Slayer"
    web = web_world.SkulWebWorld()

    options_dataclass = skul_options.SkulOptions
    options: skul_options.SkulOptions 
    location_name_to_id = locations.LOCATION_NAME_TO_ID
    item_name_to_id = items.ITEM_NAME_TO_ID
    origin_region_name = "Stronghold"
    
    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.create_all_items(self)

    def create_item(self, name: str) -> items.SkulItem:
        return items.create_item_with_correct_classification(self, name)

    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        return self.options.as_dict("quartz_mult", "req_room_count", "shrine_checks_count", "de_skull_trap_weight", "death_link")
