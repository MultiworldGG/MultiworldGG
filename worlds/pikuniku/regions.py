from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Region

from . import locations

if TYPE_CHECKING:
    from .world import PikunikuWorld

# Entry requirements per the logic sheet's area table, minus the Valley, which has no requirements.
REGION_ENTRY_REQUIREMENTS: dict[str, tuple[str, ...]] = {
    "Apple Temple": locations.APPLE_TEMPLE,
    "The Valley Road": locations.VALLEY_MAIN,
    "The Forest": locations.VALLEY_MAIN,
    "Temple of the Silver Frog": locations.FROG_TEMPLE,
    "The Valley (Revisited)": locations.VALLEY_REVISITED,
    "The Lake": locations.LAKE,
    "The Cave": locations.CAVE,
    "Sunshine HQ": locations.SUNSHINE_HQ,
    "Co-op Levels": locations.COOP,
}


def get_active_region_names(world: PikunikuWorld) -> list[str]:
    region_names = [name for name in REGION_ENTRY_REQUIREMENTS if name != "Co-op Levels"]
    if world.options.coop_levels:
        region_names.append("Co-op Levels")
    return region_names


def create_and_connect_regions(world: PikunikuWorld) -> None:
    valley = Region("The Valley", world.player, world.multiworld)
    regions = [valley]
    regions += [Region(name, world.player, world.multiworld) for name in get_active_region_names(world)]
    world.multiworld.regions += regions

    for region in regions[1:]:
        # Entrance rules are set in rules.py.
        valley.connect(region, f"The Valley -> {region.name}")
