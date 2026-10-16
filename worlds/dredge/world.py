import logging
from BaseClasses import ItemClassification
from worlds.AutoWorld import World
from collections.abc import Mapping
from typing import Any

from . import items, locations, regions, rules, web_world, events
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

    def generate_early(self) -> None:
        items.limit_starting_hulls(self)
        if (self.options.include_aberrations and not self.options.progressive_aberration_chance_items
                and not self.options.guaranteed_aberrations_item):
            logging.warning(f"[DREDGE - '{self.player_name}'] include_aberrations is on without "
                            f"progressive_aberration_chance_items or guaranteed_aberrations_item; catching every "
                            f"aberration at the normal chance can be slow.")

    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)
        events.create_all_events(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.add_precollected_items(self)
        items.create_all_items(self)

    def create_item(self, name: str) -> items.DREDGEItem:
        item_data = items.item_table[name]
        classification = item_data.classification
        if item_data.item_group == "Light" and self.options.require_boat_performance:
            classification = ItemClassification.progression
        # Logic gates aberrations on these (rules.can_get_aberrations).
        if item_data.item_group == "Aberration Chance":
            classification = ItemClassification.progression
        return items.DREDGEItem(name, classification, self.item_name_to_id[name], self.player)

    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        # If you need access to the player's chosen options on the client side, there is a helper for that.
        return self.options.as_dict(
            "death_link",
            "include_iron_rig_dlc",
            "include_pale_reach_dlc",
            "add_fishing_licenses",
            "add_passage_items",
            "logical_nets",
            "require_boat_performance",
            "progressive_aberration_chance_items",
            "guaranteed_aberrations_item"
        )