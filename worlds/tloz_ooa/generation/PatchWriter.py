import os

import json

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

        "randomized_entrances": world.randomized_entrances,
        "locations": {},
        "shop_prices": world.shop_prices,
        "music_order": {},
        "region_hints": world.region_hints,
    }

    for loc in world.multiworld.get_locations(world.player):
        if loc.address is None:
            continue
        if loc.item.player == loc.player:
            item_name = loc.item.name
        elif loc.item.advancement:
            item_name = "Archipelago Progression Item"
        else:
            item_name = "Archipelago Item"
        loc_patcher_name = loc.name
        if loc_patcher_name != "":
            patch_data["locations"][loc_patcher_name] = item_name

    
    always_available_potion_option = patch_data["options"]["enforce_potion_in_shop"]
    if always_available_potion_option == OracleOfAgesEnforcePotionInShop.option_lynna_shop:
        patch_data["locations"]["Lynna City: Shop Item #3"] = "Potion"
    if always_available_potion_option == OracleOfAgesEnforcePotionInShop.option_syrup_hut:
        patch_data["locations"]["Yoll Graveyard: Syrup Shop Item #3"] = "Potion"

    patch_data_item_hints = []
    for item_hint in world.item_hints:
        if item_hint is None:
            # Joke hint
            patch_data_item_hints.append(None)
            continue
        location = item_hint.location
        player = location.player
        if player == world.player:
            player = None
        else:
            player = world.multiworld.get_player_name(player)
        patch_data_item_hints.append((item_hint.name, location.name, player))
    patch_data["item_hints"] = patch_data_item_hints

    patch.write_file("patch.json", json.dumps(patch_data).encode('utf-8'))
    return patch