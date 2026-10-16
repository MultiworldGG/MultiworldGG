from __future__ import annotations

import json
import logging
import pkgutil
from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, TYPE_CHECKING, DefaultDict

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import DREDGEWorld

class DREDGEItem(Item):
    game: str = "DREDGE"


CATCH_TOOL_GROUPS = {"Rod", "Net", "Crab Pot", "Consumable"}
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
    speed: int = 0
    lumens: int = 0
    rebuyable: bool = False
    max_quantity: int = 1
    shape: List[str] = field(default_factory=list)


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
        speed=entry.get("speed", 0),
        lumens=entry.get("lumens", 0),
        rebuyable=entry.get("rebuyable", False),
        shape=entry.get("shape", []),
        max_quantity=entry.get("max_quantity", 1),
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

def is_expansion_enabled(world: DREDGEWorld, expansion: str) -> bool:
    if expansion == "Base":
        return True
    if expansion == "PaleReach":
        return bool(world.options.include_pale_reach_dlc)
    if expansion == "IronRig":
        return bool(world.options.include_iron_rig_dlc)
    return False

def progressive_hull_count(world: DREDGEWorld) -> int:
    return 4 if world.options.include_iron_rig_dlc else 3

def limit_starting_hulls(world: DREDGEWorld) -> None:
    # Archipelago grants every requested start_inventory_from_pool item, even ones missing from the pool,
    # which would hand a seed without the Iron Rig its Iron Rig hull.
    requested = world.options.start_inventory_from_pool.value.get("Progressive Hull", 0)
    available = progressive_hull_count(world)
    if requested > available:
        logging.warning(f"[DREDGE - '{world.player_name}'] start_inventory_from_pool asks for {requested} "
                        f"Progressive Hulls but this seed only has {available}; starting with {available}.")
        world.options.start_inventory_from_pool.value["Progressive Hull"] = available

def get_random_filler_item_name(world: DREDGEWorld) -> str:
    traps = sorted(world.options.enabled_traps.value)
    if traps and world.random.randrange(100) < world.options.trap_percentage.value:
        return world.random.choice(traps)

    filler_pool = [
        item
        for item, data in item_table.items()
        if data.classification == ItemClassification.filler
           and is_expansion_enabled(world, data.expansion)
    ]

    random_filler_item = world.random.choice(filler_pool)

    return random_filler_item

def create_all_items(world: DREDGEWorld) -> None:
    item_pool: list[Item] = []

    progression_classes = {ItemClassification.progression, ItemClassification.progression_skip_balancing}
    for item, data in item_table.items():
        if (data.classification not in progression_classes
                or data.item_group == "Research"
                or not is_expansion_enabled(world, data.expansion)):
            continue

        if item.startswith("Starting Gear") or item == "Progressive Hull":
            continue

        if not world.options.add_fishing_licenses and data.item_group == "Virtual License":
            continue

        if not world.options.add_passage_items and data.item_group == "Virtual Passage Item":
            continue

        for _ in range(data.max_quantity):
            item_pool.append(world.create_item(item))

    for _ in range(progressive_hull_count(world)):
        item_pool.append(world.create_item("Progressive Hull"))

    for item, data in item_table.items():
        if (data.classification == ItemClassification.useful and is_expansion_enabled(world, data.expansion)
                and data.item_group != "Aberration Chance"):
            item_pool.append(world.create_item(item))

    for _ in range(world.options.progressive_aberration_chance_items.value):
        item_pool.append(world.create_item("Progressive Aberration Chance"))
    if world.options.guaranteed_aberrations_item:
        item_pool.append(world.create_item("Guaranteed Aberrations"))

    number_of_items = len(item_pool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items

    if needed_number_of_filler_items < 0:
        raise Exception(f"[DREDGE - '{world.player_name}'] {number_of_items} items for only "
                        f"{number_of_unfilled_locations} locations")

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


def add_precollected_items(world: DREDGEWorld) -> None:
    world.multiworld.push_precollected(world.create_item("Starting Gear - Basic Fishing Pole"))
    world.multiworld.push_precollected(world.create_item("Starting Gear - Peculiar Engine"))
