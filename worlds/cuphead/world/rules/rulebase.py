### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Location, Region

if TYPE_CHECKING:
    from ... import CupheadWorld


# Rule helper functions

def get_entrance_name(exit: str, entrance: str) -> str:
    return f"({exit})->({entrance})"
def get_entrance_by_name(world: "CupheadWorld", entrance_name: str) -> Entrance:
    return world.multiworld.get_entrance(entrance_name, world.player)
def get_entrance(world: "CupheadWorld", exit: str, entrance: str) -> Entrance:
    return get_entrance_by_name(world, get_entrance_name(exit, entrance))
def get_location(world: "CupheadWorld", location: str) -> Location:
    return world.multiworld.get_location(location, world.player)
def get_region(world: "CupheadWorld", region: str) -> Region:
    return world.multiworld.get_region(region, world.player)
