from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region

if TYPE_CHECKING:
    from .world import SimpsonsHitNRunWorld


def create_and_connect_regions(world: SimpsonsHitNRunWorld) -> None:
    create_all_regions(world)
    connect_regions(world)

def create_all_regions(world: SimpsonsHitNRunWorld) -> None:
    regions = [Region("Hub", world.player, world.multiworld)]

    for i in range(7):
        regions += [Region(f"Level {i + 1}", world.player, world.multiworld),
                    Region(f"Level {i + 1} Missions", world.player, world.multiworld),
                    Region(f"Level {i + 1} Races", world.player, world.multiworld),
                    Region(f"Level {i + 1} Wasps", world.player, world.multiworld),
                    Region(f"Level {i + 1} Cards", world.player, world.multiworld),
                    Region(f"Level {i + 1} Gags", world.player, world.multiworld),
                    Region(f"Level {i + 1} Shops", world.player, world.multiworld)]

    world.multiworld.regions += regions

def connect_regions(world: SimpsonsHitNRunWorld) -> None:
    characters = ["Homer", "Bart", "Lisa", "Marge", "Apu", "Bart", "Homer"]

    hub = world.get_region("Hub")

    level_regions = [world.get_region("Level 1"), world.get_region("Level 2"), world.get_region("Level 3"),
                     world.get_region("Level 4"), world.get_region("Level 5"), world.get_region("Level 6"),
                     world.get_region("Level 7")]

    level_mission_regions = [world.get_region("Level 1 Missions"), world.get_region("Level 2 Missions"),
                             world.get_region("Level 3 Missions"),
                             world.get_region("Level 4 Missions"), world.get_region("Level 5 Missions"),
                             world.get_region("Level 6 Missions"), world.get_region("Level 7 Missions")]

    level_race_regions = [world.get_region("Level 1 Races"), world.get_region("Level 2 Races"),
                          world.get_region("Level 3 Races"),
                          world.get_region("Level 4 Races"), world.get_region("Level 5 Races"),
                          world.get_region("Level 6 Races"), world.get_region("Level 7 Races")]

    level_wasp_regions = [world.get_region("Level 1 Wasps"), world.get_region("Level 2 Wasps"),
                          world.get_region("Level 3 Wasps"),
                          world.get_region("Level 4 Wasps"), world.get_region("Level 5 Wasps"),
                          world.get_region("Level 6 Wasps"), world.get_region("Level 7 Wasps")]

    level_card_regions = [world.get_region("Level 1 Cards"), world.get_region("Level 2 Cards"),
                          world.get_region("Level 3 Cards"),
                          world.get_region("Level 4 Cards"), world.get_region("Level 5 Cards"),
                          world.get_region("Level 6 Cards"), world.get_region("Level 7 Cards")]

    level_gag_regions = [world.get_region("Level 1 Gags"), world.get_region("Level 2 Gags"),
                         world.get_region("Level 3 Gags"),
                         world.get_region("Level 4 Gags"), world.get_region("Level 5 Gags"),
                         world.get_region("Level 6 Gags"), world.get_region("Level 7 Gags")]

    level_shop_regions = [world.get_region("Level 1 Shops"), world.get_region("Level 2 Shops"),
                          world.get_region("Level 3 Shops"),
                          world.get_region("Level 4 Shops"), world.get_region("Level 5 Shops"),
                          world.get_region("Level 6 Shops"), world.get_region("Level 7 Shops")]

    for i in range(7):
        level_num = i + 1
        character = characters[i]

        if world.options.Lock_Levels:
            hub.connect(level_regions[i], f"Hub to Level {level_num}", lambda state, num=level_num: state.has(f"Level {num}", world.player) or \
                                                                                                          state.has("Progressive Level", world.player, num))
        else:
            hub.connect(level_regions[i], f"Hub to Level {level_num}")

        level_regions[i].connect(level_mission_regions[i], f"Level {level_num} to Missions", lambda state, num=level_num: state.has(f"Level {num}", world.player) or \
                                                                                                                              state.has("Progressive Level", world.player, num))

        if "All" in world.options.Shuffle_Checkered_Flags or (character in world.options.Shuffle_Checkered_Flags and "None" not in world.options.Shuffle_Checkered_Flags):
            level_regions[i].connect(level_race_regions[i], f"Level {level_num} to Races", lambda state, char=character: state.has(f"{char} Checkered Flag", world.player))
        else:
            level_regions[i].connect(level_race_regions[i], f"Level {level_num} to Races", lambda state, num=level_num: state.has(f"Level {num}", world.player) or \
                                                                                                                              state.has("Progressive Level", world.player, num))

        level_regions[i].connect(level_wasp_regions[i], f"Level {level_num} to Wasps")

        level_regions[i].connect(level_card_regions[i], f"Level {level_num} to Cards")

        if "All" in world.options.Shuffle_Gagfinder or (character in world.options.Shuffle_Gagfinder and "None" not in world.options.Shuffle_Gagfinder):
            level_regions[i].connect(level_gag_regions[i], f"Level {level_num} to Gags", lambda state, char=character: state.has(f"{char} Gagfinder", world.player))
        else:
            level_regions[i].connect(level_gag_regions[i], f"Level {level_num} to Gags", lambda state, num=level_num: state.has(f"Level {num}", world.player) or \
                                                                                                                            state.has("Progressive Level", world.player, num))

        level_regions[i].connect(level_shop_regions[i], f"Level {level_num} to Shops", lambda state, num=level_num: state.has("Progressive Wallet Upgrade", world.player, num))
