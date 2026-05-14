import os

import yaml

from typing import TYPE_CHECKING
from BaseClasses import ItemClassification
from ..patching.ProcedurePatch import OoAProcedurePatch
from ..data.Constants import *
from ..Options import *


if TYPE_CHECKING:
    from .. import OracleOfAgesWorld

def ooa_create_appp_patch(world: "OracleOfAgesWorld") -> OoAProcedurePatch:
    patch = OoAProcedurePatch()

    patch.player = world.player
    patch.player_name = world.multiworld.get_player_name(world.player)

    patch_data = {
        "version": f"{world.version()}",

        "options": world.options.as_dict(
            *[option_name for option_name in OracleOfAgesOptions.type_hints
              if hasattr(OracleOfAgesOptions.type_hints[option_name], "include_in_patch")]),
        "warp_to_start_variables": world.determine_warp_to_start_variables(),

        "dungeon_entrances": {a.replace(" entrance", ""): b.replace("enter ", "")
                              for a, b in world.dungeon_entrances.items()},
        "locations": {},
        "shop_prices": world.shop_prices,
        "music_order": {}
    }

    for loc in world.multiworld.get_locations(world.player):
        if loc.address is None:
            continue
        if loc.item.player == loc.player:
            item_name = loc.item.name
        elif loc.item.classification in [ItemClassification.progression, ItemClassification.progression_skip_balancing]:
            item_name = "Archipelago Progression Item"
        else:
            item_name = "Archipelago Item"
        loc_patcher_name = loc.name
        if loc_patcher_name != "":
            patch_data["locations"][loc_patcher_name] = item_name

    patch.write_file("patch.dat", yaml.dump(patch_data).encode('utf-8'))
    return patch