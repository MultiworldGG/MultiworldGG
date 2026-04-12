from __future__ import annotations

import json
import pkgutil
from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, TYPE_CHECKING, DefaultDict

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import DREDGEWorld

class DREDGEItem(Item):
    game: str = "DREDGE"


CATCH_TOOL_GROUPS = {"Rod", "Net", "Crab Pot"}
EXCLUDED_CATCH_TOOLS = {"Tendon Rod", "Viscera Crane"}

ToolIndexKey = tuple[str, str]  # (catch_type, tool_group, expansion)
ToolIndex = dict[ToolIndexKey, tuple[str, ...]]

@dataclass
class DREDGEItemData:
    base_id_offset: int
    classification: ItemClassification
    item_group: str
    expansion: str
    can_catch: List[str] = field(default_factory=list)
    size: int = 0
    item_value: int = 0
    max_quantity: int = 1


item_base_id = 3459028911689314


def load_data_file(*args) -> dict:
    fname = "/".join(["data", *args])
    return json.loads(pkgutil.get_data(__name__, fname).decode())


item_table = {
    name: DREDGEItemData(
        base_id_offset=entry["base_id_offset"],
        classification=ItemClassification[entry["classification"]],
        item_group=entry["item_group"],
        expansion=entry["expansion"],
        can_catch=entry.get("can_catch", []),
        size=entry.get("size", 0),
        item_value=entry.get("item_value", 0),
    )
    for name, entry in load_data_file("items.json").items()
}


def get_item_group(item_name: str) -> str:
    return item_table[item_name].item_group


ITEM_NAME_TO_ID = {name: item_base_id + data.base_id_offset for name, data in item_table.items()}

ITEM_NAME_GROUPS = defaultdict(set)
for name, data in item_table.items():
    if data.item_group:
        ITEM_NAME_GROUPS[data.item_group].add(name)

def get_random_filler_item_name(world: DREDGEWorld) -> str:
    filler_pool = [
        item
        for item, data in item_table.items()
        if data.classification == ItemClassification.filler
           and (
                   data.expansion == "Base"
                   or (world.options.include_pale_reach_dlc and data.expansion == "PaleReach")
                   or (world.options.include_iron_rig_dlc and data.expansion == "IronRig")
           )
    ]

    random_filler_item = world.random.choice(filler_pool)

    return random_filler_item

def create_all_items(world: DREDGEWorld) -> None:
    item_pool: list[Item] = []

    progression_classes = {ItemClassification.progression, ItemClassification.progression_skip_balancing}
    for item, data in item_table.items():
        if data.classification not in progression_classes or data.item_group == "Research":
            continue

        for index in range(data.classification):
            if data.expansion == "Base":
                item_pool.append(world.create_item(item))
            elif world.options.include_pale_reach_dlc and data.expansion == "PaleReach":
                item_pool.append(world.create_item(item))
            elif world.options.include_iron_rig_dlc and data.expansion == "IronRig":
                item_pool.append(world.create_item(item))

    num_base_hull_upgrades = 2
    for _ in range(num_base_hull_upgrades):
        item_pool.append(world.create_item("Progressive Hull"))
    if world.options.include_iron_rig_dlc:
        item_pool.append(world.create_item("Progressive Hull"))

    num_research_parts = 30
    for _ in range(num_research_parts):
        item_pool.append(world.create_item("Research Part"))

    for item, data in item_table.items():
        if data.classification == ItemClassification.useful:
            item_pool.append(world.create_item(item))

    number_of_items = len(item_pool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items

    if needed_number_of_filler_items > 0:
        for _ in range(needed_number_of_filler_items):
            item_pool.append(world.create_item(get_random_filler_item_name(world)))

    world.multiworld.itempool += item_pool

def build_catch_tool_index() -> ToolIndex:
    idx: DefaultDict[ToolIndexKey, list[str]] = defaultdict(list)

    for name, item in item_table.items():
        if getattr(item, "item_group", None) not in CATCH_TOOL_GROUPS:
            continue

        can_catch = getattr(item, "can_catch", None)
        if not can_catch:
            continue

        if name in EXCLUDED_CATCH_TOOLS:
            continue

        for catch_type in can_catch:
            idx[(catch_type, item.item_group)].append(name)


    return {k: tuple(v) for k, v in idx.items()}

CATCH_TOOL_INDEX: ToolIndex = build_catch_tool_index()