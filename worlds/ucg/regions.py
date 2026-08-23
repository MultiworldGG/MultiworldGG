from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Region

if TYPE_CHECKING:
    from .world import UncannyCatWorld

ALL_REGIONS = [
    "Menu",
    "World 0 (Tutorial)",
    "World 1 (Golf Central)",
    "World 2 (Glowstick City)",
    "World 3 (Chuckle Park)",
    "World 4 (Final Frontier)",
    "World 5 (Elysian Fields)",
    "World P (Cosmic Championship)",
    "World E (Endless Levels)",
    "Summer Villa", # Minigame area
]


def create_and_connect_regions(world: UncannyCatWorld) -> None:
    regions = {name: Region(name, world.player, world.multiworld) for name in ALL_REGIONS}
    for region in regions.values():
        world.multiworld.regions.append(region)

    def connect(from_name: str, to_name: str, rule=None) -> None:
        world.create_entrance(regions[from_name], regions[to_name], rule)

    connect("Menu", "World 0 (Tutorial)")
    connect("Menu", "World 1 (Golf Central)")
    connect("Menu", "World 2 (Glowstick City)")
    connect("Menu", "World 3 (Chuckle Park)")
    connect("Menu", "World 4 (Final Frontier)")
    connect("Menu", "World 5 (Elysian Fields)")
    connect("Menu", "World P (Cosmic Championship)")
    connect("Menu", "World E (Endless Levels)")
    connect("Menu", "Summer Villa")
