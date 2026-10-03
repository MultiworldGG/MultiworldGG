import json
from collections import defaultdict
from typing import Any, cast

from BaseClasses import Location
from Options import Option
from worlds.tloz_oos.data.locations import LOCATIONS_DATA

from ..data.Constants import VALID_RUPEE_PRICE_VALUES
from ..options import OracleOfSeasonsOptions, OracleOfSeasonsShopPrices
from ..patching.procedure_patch import OoSProcedurePatch
from ..world import OracleOfSeasonsWorld
from .create_regions import location_is_active


def oos_create_ap_procedure_patch(world: OracleOfSeasonsWorld) -> OoSProcedurePatch:
    patch = OoSProcedurePatch()

    patch.player = world.player
    patch.player_name = world.multiworld.get_player_name(world.player)

    if (
        world.options.shop_prices == OracleOfSeasonsShopPrices.option_vanilla
        or world.options.shop_prices == OracleOfSeasonsShopPrices.option_free
    ):
        shop_prices = world.shop_prices
    else:
        # Make excludable items cheaper so they have a chance to be bought
        # TODO: Would be better if it used a different "value" system, probably, when implemented in AP
        shop_prices = {}
        for location_name, location_data in LOCATIONS_DATA.items():
            if "symbolic_name" not in location_data:
                continue
            symbolic_name = location_data["symbolic_name"]
            if symbolic_name not in world.shop_prices:
                continue
            if not location_is_active(world, location_name, location_data):
                continue
            location = world.get_location(location_name)
            item = location.item
            assert item is not None
            if not item.excludable or (
                # Potion is very good, as renewable, so it goes in the non-excludable pile
                "renewable" in location_data and item.player == world.player and item.name == "Potion"
            ):
                shop_prices[symbolic_name] = world.shop_prices[symbolic_name]
                continue
            new_price = world.shop_prices[symbolic_name] / 10
            shop_prices[symbolic_name] = min(VALID_RUPEE_PRICE_VALUES, key=lambda x: abs(x - new_price))

    type_hints = cast(dict[str, type[Option[Any]]], cast(object, OracleOfSeasonsOptions.type_hints))
    patch_data = {
        "version": f"{world.version()}",
        "seed": world.multiworld.seed,
        "options": world.options.as_dict(
            *[option_name for option_name in type_hints if hasattr(type_hints[option_name], "include_in_patch")]
        ),
        "samasa_gate_sequence": " ".join([str(x) for x in world.samasa_gate_code]),
        "lost_woods_item_sequence": world.lost_woods_item_sequence,
        "lost_woods_main_sequence": world.lost_woods_main_sequence,
        "default_seasons": world.default_seasons,
        "old_man_rupee_values": world.old_man_rupee_values,
        "dungeon_entrances": {
            a.replace(" entrance", ""): b.replace("enter ", "") for a, b in world.dungeon_entrances.items()
        },
        "locations": {},
        "subrosia_portals": world.portal_connections,
        "shop_prices": shop_prices,
        "subrosia_seaside_location": world.random.randint(0, 3),
        "region_hints": world.region_hints,
        "boss_mapping": world.boss_mapping,
    }

    for loc in world.multiworld.get_locations(world.player):
        # Skip event locations which are not real in-game locations that need to be patched
        if loc.address is None:
            continue
        assert loc.item
        if loc.item.player == loc.player:
            patch_data["locations"][loc.name] = {"item": loc.item.name}
        else:
            patch_data["locations"][loc.name] = {
                "item": loc.item.name,
                "player": world.multiworld.get_player_name(loc.item.player),
                "progression": loc.item.advancement,
            }

    patch_data_item_hints = []
    for item_hint in world.item_hints:
        if item_hint is None:
            # Joke hint
            patch_data_item_hints.append(None)
            continue
        location = cast(Location, item_hint.location)
        player = location.player
        if player == world.player:
            player_name = None
        else:
            player_name = world.multiworld.get_player_name(player)
        patch_data_item_hints.append((item_hint.name, location.name, player_name))
    patch_data["item_hints"] = patch_data_item_hints

    start_inventory = defaultdict(int)
    for item in world.multiworld.precollected_items[world.player]:
        start_inventory[item.name] += 1
    patch_data["start_inventory"] = dict(start_inventory)

    patch.write_file("patch.json", json.dumps(patch_data).encode("utf-8"))
    return patch
