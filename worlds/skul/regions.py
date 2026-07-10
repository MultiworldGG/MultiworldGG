from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Region
from rule_builder.rules import Has

if TYPE_CHECKING:
    from .world import SkulWorld


def create_and_connect_regions(world: SkulWorld) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: SkulWorld) -> None:
    regions = [
        Region("Stronghold", world.player, world.multiworld),
        Region("Forest of Harmony", world.player, world.multiworld),
        Region("Grand Hall", world.player, world.multiworld),
        Region("The Black Lab", world.player, world.multiworld),
        Region("Fortress of Fate", world.player, world.multiworld),
        Region("Sacred Grounds", world.player, world.multiworld),
    ]
    world.multiworld.regions += regions


def connect_regions(world: SkulWorld) -> None:
    stronghold = world.get_region("Stronghold")
    forest = world.get_region("Forest of Harmony")
    grand_hall = world.get_region("Grand Hall")
    black_lab = world.get_region("The Black Lab")
    fortress = world.get_region("Fortress of Fate")
    sacred_grounds = world.get_region("Sacred Grounds")

    # Each stage area requires a certain number of Progressive Stage items.
    world.create_entrance(stronghold, forest, Has("Progressive Stage", count=1),
                          name="Stronghold to Forest of Harmony")
    world.create_entrance(forest, grand_hall, Has("Progressive Stage", count=2),
                          name="Forest of Harmony to Grand Hall")
    world.create_entrance(grand_hall, black_lab, Has("Progressive Stage", count=3),
                          name="Grand Hall to The Black Lab")
    world.create_entrance(black_lab, fortress, Has("Progressive Stage", count=4),
                          name="The Black Lab to Fortress of Fate")
    world.create_entrance(fortress, sacred_grounds, Has("Progressive Stage", count=5),
                          name="Fortress of Fate to Sacred Grounds")
