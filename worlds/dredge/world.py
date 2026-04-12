from worlds.AutoWorld import World
from collections.abc import Mapping
from typing import Any

from . import items, locations, regions, rules, web_world
from .options import DREDGEOptions

class DREDGEWorld(World):
    """
    Sell your catch, upgrade your boat, and dredge the depths for long-buried secrets. Explore a mysterious archipelago
    and discover why some things are best left forgotten.
    """

    game = "DREDGE"
    web = web_world.DREDGEWebWorld()
    options: DREDGEOptions
    options_dataclass = DREDGEOptions
    item_name_to_id = items.ITEM_NAME_TO_ID
    item_name_groups = items.ITEM_NAME_GROUPS
    location_name_to_id = locations.LOCATION_NAME_TO_ID
    location_name_groups = locations.LOCATION_NAME_GROUPS

    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        self.multiworld.push_precollected(self.create_item("Starting Gear - Basic Fishing Pole"))
        self.multiworld.push_precollected(self.create_item("Starting Gear - Peculiar Engine"))
        items.create_all_items(self)

    def create_item(self, name: str) -> items.DREDGEItem:
        item_data = items.item_table[name]
        return items.DREDGEItem(name, item_data.classification, self.item_name_to_id[name], self.player)

    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        # If you need access to the player's chosen options on the client side, there is a helper for that.
        return self.options.as_dict(
            "include_iron_rig_dlc", "include_pale_reach_dlc"
        )