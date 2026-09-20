from __future__ import annotations

from typing import TYPE_CHECKING

from worlds.dredge.items import DREDGEItem
from worlds.dredge.locations import DREDGELocation

if TYPE_CHECKING:
    from . import DREDGEWorld

def add_event(world: DREDGEWorld, region_name: str, location_name:str, item_name:str) -> None:
    region = world.get_region(region_name)

    region.add_event(
        location_name,
        item_name,
        location_type=DREDGELocation,
        item_type=DREDGEItem,
    )

def create_a_place_to_rest_events(world: DREDGEWorld) -> None:
    add_event(
        world,
        "The Marrows",
        "A Place to Rest - Materials Delivered Event",
        "A Place to Rest - Materials Delivered",
    )

    add_event(
        world,
        "The Marrows",
        "A Place to Rest - Returned to Builder Event",
        "A Place to Rest - Returned to Builder"
    )

def create_victory_event_location(world: DREDGEWorld) -> None:
    add_event(
        world,
        "Insanity",
        "The Collector",
        "Victory",
    )

def create_all_events(world: DREDGEWorld) -> None:
    #create_a_place_to_rest_events(world)
    create_victory_event_location(world)