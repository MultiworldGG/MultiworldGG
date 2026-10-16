from collections.abc import Mapping
from typing import Any

from BaseClasses import Region, Location, Item, ItemClassification, Tutorial
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import (
    Component,
    components,
    Type as component_type,
    )
from collections import defaultdict
from rule_builder.rules import Rule, Or, HasAll, Has

from . import Options as islestrials_options

json_world = {
    "region_map": {
        "main": {
            "central": [["progressive weapon"], ["progressive weapon (alt)"], ["fireball spell"], ["sprinting boots"]],
            "torch": [["progressive weapon", "progressive weapon (alt)", "fireball spell"], ["sprinting boots", "fireball spell"], ["bubbles"]],
            "lake": [["progressive weapon", "progressive weapon (alt)"], ["sprinting boots"], ["fireball spell", "bubbles"]],
            "distant": [["bubbles"]]
        },
        "central": {
            "private": [["yellow key"]]
        },
        "lake": {
            "rocky": [["progressive weapon", "progressive weapon (alt)"]],
            "snake": [["progressive weapon"], ["progressive weapon (alt)"], ["fireball spell"]],
            "gauntlet": [["bubbles"]]
        },
        "snake": {
            "goal": [["progressive weapon", "progressive weapon (alt)", "fireball spell", "sprinting boots", "green key", "bubbles"]]
        }
    },
    "location_map": {
        "main": {
            "easiest chest": None,
            "spike obstacle chest": None,
            "torch puzzle chest": [["progressive weapon", "progressive weapon (alt)", "fireball spell"]]
        },

        "central": {
            "easy blade path chest": None,
            "minor obstruction chest": [["progressive weapon"], ["progressive weapon (alt)"], ["fireball spell"]],
            "blade squeeze chest": [["progressive weapon"], ["progressive weapon (alt)"], ["fireball spell"]],
            "blade corridor chest": [["progressive weapon"], ["progressive weapon (alt)"], ["fireball spell"]],
            "cheesable chest": [["progressive weapon", "progressive weapon (alt)"], ["progressive weapon", "spike boots"], ["progressive weapon (alt)", "spike boots"]],
            "rock shortcut chest": [["progressive weapon", "progressive weapon (alt)"]],
            "mud shortcut chest": [["sprinting boots"]]
        },

        "private": {
            "spinner introduction chest": None,
            "miniature forest chest": [["progressive weapon"], ["progressive weapon (alt)"], ["fireball spell"]],
            "spike weave chest": [["progressive weapon", "progressive weapon (alt)"], ["spike boots"]],
            "spike path chest": [["spike boots"]]
        },

        "torch": {
            "dangerous torch puzzle chest": [["fireball spell"]]
        },

        "lake": {
            "mud run chest": [["sprinting boots"]]
        },

        "distant": {
            "rock pile chest": [["progressive weapon", "progressive weapon (alt)"]],
            "spike gap chest": [["spike boots"]],
            "mud obstacle course chest": [["sprinting boots"]],
            "mud torch secret chest": [["sprinting boots", "fireball spell"]]
        },

        "rocky": {
            "rocky spinners chest": None,
            "rocky torch secret chest": [["fireball spell"]]
        },

        "snake": {
            "eye of the snake chest": None
        },

        "gauntlet": {
            "gauntlet checkpoint chest": [["progressive weapon", "progressive weapon (alt)"]],
            "gauntlet chest": [["progressive weapon", "progressive weapon (alt)", "fireball spell", "sprinting boots"]]
        },

        "goal": {
            "victory": None
        }
    },
    "items": {
        "prog_items": [
            "progressive weapon",
            "progressive weapon (alt)",
            "fireball spell",
            "sprinting boots",
            "spike boots",
            "bubbles",
            "yellow key",
            "green key"
        ],
        "useful_items": [
            "heart container",
            "heart container 2",
            "heart container 3",
            "swift feather",
            "swift feather 2",
            "swift feather 3"
        ],
        "filler_items": [
            "mysterious shape",
            "temporary heart"
        ]
    },
    "base_id": 19827373737,
    "game_name": "Isles of Trials",
    "filler_name": "temporary heart",
    "item_name_groups": {
        "Weapons": [
            "progressive weapon",
            "progressive weapon (alt)"
        ],
        "Progression": [
            "progressive weapon",
            "progressive weapon (alt)",
            "fireball spell",
            "sprinting boots",
            "spike boots",
            "bubbles",
            "yellow key",
            "green key"
        ],
        "Hearts": [
            "heart container",
            "heart container 2",
            "heart container 3"
        ],
        "Feathers": [
            "swift feather",
            "swift feather 2",
            "swift feather 3"
        ]
    }
}


class TemplateItem(Item):
    game = json_world["game_name"]


class TemplateLocation(Location):
    game = json_world["game_name"]


class IslesTrialsWeb(WebWorld):
    setup_en = Tutorial(
        "setup",
        "A guide for setting up Isles of Trials for MWGG",
        "en",
        "setup_en.md",
        "setup/en",
        ["ChromaNyan"]
    )
    tutorials = [setup_en]


# flatten lists of locations and items so they are indexed for name_to_id
location_list = [location for locations in json_world["location_map"].values() for location in locations.keys()]
item_list = [item for item_lists in json_world["items"].values() for item in item_lists]

# for my particular get_item_classification
classification_lookup = defaultdict(lambda: ItemClassification.useful, {
    **{n: ItemClassification.progression for n in json_world["items"]["prog_items"]},
    **{n: ItemClassification.useful for n in json_world["items"]["useful_items"]},
    **{n: ItemClassification.filler for n in json_world["items"]["filler_items"]}
})

class IslesTrialsWorld(World):
    """
    Travel between islands and loot chests in this small PICO-8 adventure game.
    """
    game = json_world["game_name"]
    web = IslesTrialsWeb()
    options_dataclass = islestrials_options.IslesTrialsOptions
    options: islestrials_options.IslesTrialsOptions
    location_name_to_id = {name: json_world["base_id"]+location_list.index(name) for name in location_list}
    item_name_to_id = {name: json_world["base_id"]+item_list.index(name) for name in item_list}
    item_name_groups = {name: set(items) for name, items in json_world["item_name_groups"].items()}
    origin_region_name = "main"

    ut_can_gen_without_yaml = True

# basic getters for json_world data, any option based modifications can be done here; may cache these later
# expect authors to modify the return of super() per options, or fully override if their format is different
    def get_region_list(self) -> list[str]:
        """
        Parser method to return the list of all regions to be created.
        Currently flattens region_map to create all regions with a connection in or out
        """
        ret = {
            r for connections in json_world["region_map"].values()
            for r in connections.keys()
        }.union(json_world["region_map"].keys())
        return ret

    def get_connections(self) -> dict[str, dict[str, Rule | None]]:
        """
        Parser method to convert the region definitions in the json_world object
        into a dict of connection entries formatted as {parent_region_name: {target_region_name: rule}}
        """
        return {
            region1: {
                region2: None if rule is None else Or(*[HasAll(*inner) for inner in rule])
                for region2, rule in connections.items()
                }
            for region1, connections in json_world["region_map"].items()
        }

    def get_location_map(self) -> dict[str, dict[str, Rule | None]]:
        """
        Parser method to convert the location definitions in the json_world object
        into a list of location entries formatted as {parent_region_name: {location_name: rule}}
        """
        return {
            region: {
                location: None if rule is None else Or(*[HasAll(*inner) for inner in rule])
                for location, rule in placements.items()
                }
            for region, placements in json_world["location_map"].items()
        }

# black box methods
    def set_victory(self) -> None:
        """
        current black box to set and setup victory condition,
        run after all region/locations have been created (but currently before items)
        """
        victory = self.get_location("victory")
        victory.address = None
        victory.place_locked_item(TemplateItem("victory", ItemClassification.progression, None, self.player))
        self.set_completion_rule(Has("victory"))
        # currently finds victory location, adds locked victory event, and requires victory event for completion

    def get_item_list(self) -> list[str]:
        """
        current black box to create a list of item names per count that need to be created
        """
        return item_list
        # currently my items in my datapackage should all be created once, so this list functions

    def get_item_classification(self, name: str) -> ItemClassification:
        """
        current black box to convert item names to their respective ItemClassification
        """
        return classification_lookup[name]

    def get_filler_item_name(self) -> str:
        # filler_name should be a list and this should choose with self.random
        if self.random.randint(0,1) == 0:
            return "mysterious shape"
        else:
            return "temporary heart"

# common World methods
    def create_regions(self) -> None:
        # create a local map of get_region_list names to region object
        # for referencing in create_regions and adding those regions to the multiworld
        regions = {region: None for region in self.get_region_list()}
        for region in regions.keys():
            regions[region] = Region(region, self.player, self.multiworld)
            self.multiworld.regions.append(regions[region])

        # loop through get_region_map, letting add_exits add rules if present
        for region, connections in self.get_connections().items():
            regions[region].add_exits(connections.keys(), connections)

        # loop through get_location_map, adding the rules if present to the location
        for region, placements in self.get_location_map().items():
            for location, rule in placements.items():
                loc = TemplateLocation(self.player, location, self.location_name_to_id[location], regions[region])
                if rule is not None:
                    self.set_rule(loc, rule)
                regions[region].locations.append(loc)

        self.set_victory()

    def create_items(self) -> None:
        # create all items in get_item_list()
        itempool = [self.create_item(item) for item in self.get_item_list()]

        # fill in any difference in itempool with filler item and submit to multiworld
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))
        missing_items = total_locations - len(itempool)
        if missing_items > 0:
            itempool += [self.create_filler() for _ in range(missing_items)]
        self.multiworld.itempool += itempool

    def create_item(self, name: str) -> "Item":
        # this is really janky i'm so sorry
        truename = name
        if (truename == "heart container 2" or truename == "heart container 3"):
            truename = "heart container"
        if (truename == "swift feather 2" or truename == "swift feather 3"):
            truename = "swift feather"
        return TemplateItem(
            truename,
            self.get_item_classification(truename),
            self.item_name_to_id.get(truename, None),
            self.player)
    
    def fill_slot_data(self) -> Mapping[str, Any]:
        # If you need access to the player's chosen options on the client side, there is a helper for that.
        return self.options.as_dict(
            "player_sprite"
        )