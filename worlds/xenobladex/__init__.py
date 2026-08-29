from BaseClasses import Tutorial
from rule_builder.cached_world import CachedRuleBuilderWorld
from ..AutoWorld import WebWorld
from worlds.LauncherComponents import Component, components, launch_subprocess, Type
from functools import partial
from typing import ClassVar, cast

from . import Slot, Items, Locations, Rules, Options, Settings


def launch_client(*args: str) -> None:
    from .Client import launch
    launch_subprocess(partial(launch, *args), name="XenobladeXClient")


components.append(Component("Xenoblade X Client", func=launch_client, component_type=Type.CLIENT,
                            game_name="Xenoblade X", supports_uri=True))


class XenobladeXWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Xenoblade Chronicles X for Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Maragon", "Nina"]
    )]

    option_groups = Options.option_groups


class XenobladeXWorld(CachedRuleBuilderWorld):
    """
     Xenoblade Chronicles X another 100+ hour game. Sounds like fun?
    """

    game = "Xenoblade X"
    topology_present = True
    web = XenobladeXWeb()

    data_version = 16
    base_id: int = 4100000

    options_dataclass = Options.XenobladeXOptions

    settings: ClassVar[Settings.XenobladeXSettings]  # pyright: ignore[reportIncompatibleVariableOverride]

    item_name_to_id = (lambda b_id: {item.get_item(): b_id + item.id
                                     for item in Items.xenobladeXItems.values() if item.id is not None})(base_id)
    location_name_to_id = (lambda b_id: {location.get_location(): b_id + location.id
                                         for location in Locations.xenobladeXLocations.values()
                                         if location.id is not None})(base_id)

    item_name_groups = {
        prefix: {itm.get_item() for itm in Items.xenobladeXItems.values() if itm.prefix == prefix}
        for prefix in {itm.prefix for itm in Items.xenobladeXItems.values()} if prefix
    }

    def create_regions(self) -> None:
        Locations.create_locations(self)

    def create_items(self) -> None:
        Items.create_items(self)

    def create_item(self, name: str) -> Items.XenobladeXItem:
        return Items.create_item(self, name)

    def get_filler_item_name(self) -> str:
        return Items.get_random_filler_item_name(self)

    def set_rules(self) -> None:
        Rules.set_rules(self)

    def generate_early(self) -> None:
        pass

    def generate_basic(self) -> None:
        pass

    def fill_slot_data(self) -> dict[str, object]:
        return Slot.generate_slot_data(cast(Options.XenobladeXOptions, self.options))
