from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, Rule

from BaseClasses import Entrance, Region

if TYPE_CHECKING:
    from .world import BuildJetpackWorld

def create_and_connect_regions(world: BuildJetpackWorld) -> None:
    create_all_regions(world)
    connect_regions(world)

def create_all_regions(world: BuildJetpackWorld) -> None:
    raft = Region("Raft", world.player, world.multiworld)
    regions = [raft]
    for i in range(3):
        sky = Region("Sky "+str(i+1), world.player, world.multiworld)
        regions.append(sky)
    for i in range(8):
        sea = Region("Sea "+str(i+1), world.player, world.multiworld)
        regions.append(sea)

    world.multiworld.regions += regions

def connect_regions(world: BuildJetpackWorld) -> None:
    # this method sucks. maybe i'll optimize it at some point but right now i really don't care, i don't plan to PR this
    # sky regions are based on what jetpack level you need to reach them
    sky3 = world.get_region("Sky 3") # top of the world
    sky2 = world.get_region("Sky 2") # middle section (4km to go)
    sky1 = world.get_region("Sky 1") # lower section (6km to go)
    raft = world.get_region("Raft")
    sea1 = world.get_region("Sea 1")
    sea2 = world.get_region("Sea 2")
    sea3 = world.get_region("Sea 3")
    sea4 = world.get_region("Sea 4")
    sea5 = world.get_region("Sea 5")
    sea6 = world.get_region("Sea 6")
    sea7 = world.get_region("Sea 7")
    sea8 = world.get_region("Sea 8")

    raft.connect(sky1, "Raft to Lower Sky", Has("Jetpack", count=1))
    sky1.connect(sky2, "Lower Sky to Middle Sky", Has("Jetpack", count=2))
    sky2.connect(sky3, "Middle Sky to Upper Sky", Has("Jetpack", count=3))
    raft.connect(sea1, "Raft to Sea 1")
    sea1.connect(sea2, "Sea 1 to Sea 2", Has("Diving Suit", count=1) & Has("Oxygen Mask", count=1))
    sea2.connect(sea3, "Sea 2 to Sea 3", Has("Diving Suit", count=2) & Has("Oxygen Mask", count=2))
    sea3.connect(sea4, "Sea 3 to Sea 4", Has("Diving Suit", count=3) & Has("Oxygen Mask", count=3))
    sea4.connect(sea5, "Sea 4 to Sea 5", Has("Diving Suit", count=4) & Has("Oxygen Mask", count=4))
    sea5.connect(sea6, "Sea 5 to Sea 6", Has("Diving Suit", count=5) & Has("Oxygen Mask", count=5))
    sea6.connect(sea7, "Sea 6 to Sea 7", Has("Diving Suit", count=6) & Has("Oxygen Mask", count=6))
    sea7.connect(sea8, "Sea 7 to Sea 8", Has("Diving Suit", count=7) & Has("Oxygen Mask", count=6)) # not a typo; at this point you can get away with having a bit less max oxygen than depth