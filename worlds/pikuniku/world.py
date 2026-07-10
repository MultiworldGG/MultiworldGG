import random
from collections.abc import Mapping
from typing import Any

from worlds.AutoWorld import World

from . import items, locations, regions, rules, web_world
from . import options as pikuniku_options


class PikunikuWorld(World):
    """
    Pikuniku is a puzzle platformer game about a little red bean going on a big adventure to gain FREE MONEY!!!!
    But uncovering a deep mysterious conspiracy along the way...
    """

    game = "Pikuniku"

    web = web_world.PikunikuWebWorld()

    options_dataclass = pikuniku_options.PikunikuOptions
    options: pikuniku_options.PikunikuOptions

    location_name_to_id = locations.LOCATION_NAME_TO_ID
    item_name_to_id = items.ITEM_NAME_TO_ID

    item_name_groups = items.ITEM_NAME_GROUPS
    location_name_groups = locations.LOCATION_NAME_GROUPS

    origin_region_name = "The Valley"

    ut_can_gen_without_yaml = True

    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:
        # Returning the slot_data tells Universal Tracker to do a second generation pass,
        # during which it is available as multiworld.re_gen_passthrough.
        return slot_data

    def generate_early(self) -> None:
        # When Universal Tracker re-generates this world, restore the options that affect
        # generation from the connected slot's slot_data.
        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if "Pikuniku" in re_gen_passthrough:
            passthrough = re_gen_passthrough["Pikuniku"]
            self.options.coinsanity.value = passthrough["coinsanity"]
            self.options.coop_levels.value = passthrough["coop_levels"]

        if self.options.early_pencil_hat == pikuniku_options.EarlyPencilHat.option_early_local:
            self.multiworld.local_early_items[self.player]["Pencil Hat"] = 1
        elif self.options.early_pencil_hat == pikuniku_options.EarlyPencilHat.option_early_global:
            self.multiworld.early_items[self.player]["Pencil Hat"] = 1

    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.create_all_items(self)

    def create_item(self, name: str) -> items.PikunikuItem:
        return items.create_item_with_correct_classification(self, name)

    def get_filler_item_name(self) -> str:
        return items.get_filler_item_name(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        # Every option that affects generation must be in slot_data for Universal Tracker.
        # death_link, death_link_amnesty and piku_color don't affect logic, but the client needs them.
        slot_data = self.options.as_dict("coinsanity", "coop_levels", "death_link", "death_link_amnesty")
        # piku_color resolves to either a mode name ("off", "random_per_screen", "random_per_seed")
        # or a normalized "#RRGGBB" hex string, so the client gets a single consistent string type.
        piku_color = self.options.piku_color.current_key
        if piku_color == "random_per_seed":
            # Generate a random hex color for this seed
            piku_color = f"#{random.randint(0, 0xFFFFFF):06X}"
        slot_data["piku_color"] = piku_color
        return slot_data
