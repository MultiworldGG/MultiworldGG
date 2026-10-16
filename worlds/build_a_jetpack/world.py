from collections.abc import Mapping
from typing import Any

from worlds.AutoWorld import World

from . import items, locations, regions, rules, web_world
from . import options as buildjetpack_options

class BuildJetpackWorld(World):
    """
    Build a Jetpack is a PICO-8 game where you dive into the ocean to gather fish and materials.
    The goal of the game is to build a powerful jetpack to fly into the skies.
    """

    game = "Build a Jetpack"
    web = web_world.BuildJetpackWebWorld()
    options_dataclass = buildjetpack_options.BuildJetpackOptions
    options: buildjetpack_options.BuildJetpackOptions
    location_name_to_id = locations.LOCATION_NAME_TO_ID
    item_name_to_id = items.ITEM_NAME_TO_ID
    origin_region_name = "Raft"

    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.create_all_items(self)

    def create_item(self, name: str) -> items.BuildJetpackItem:
        return items.create_item_with_correct_classification(self, name)
    
    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    def fill_slot_data(self) -> dict[str, Any]:
        return {
            "options": self.options.as_dict("death_link", "fishsanity", "harsh_pressure"),
        }