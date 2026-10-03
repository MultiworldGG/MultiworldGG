from typing import cast

from BaseClasses import Item, MultiWorld
from worlds.tloz_oos import OracleOfSeasonsWorld


def stage_pre_fill_check_prog(multiworld: MultiWorld):
    prog_per_player: dict[int, int] = dict.fromkeys(multiworld.get_game_players(OracleOfSeasonsWorld.game), 0)
    for item in multiworld.itempool:
        if item.player in prog_per_player and item.advancement:
            prog_per_player[item.player] += 1

    for location in multiworld.get_locations():
        item: Item | None = location.item
        if item is None:
            continue
        if item.player in prog_per_player and item.advancement:
            prog_per_player[item.player] += 1

    for player, prog_count in prog_per_player.items():
        world = cast(OracleOfSeasonsWorld, multiworld.worlds[player])
        world.num_prog = prog_count
