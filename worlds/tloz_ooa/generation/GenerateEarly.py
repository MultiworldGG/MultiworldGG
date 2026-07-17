
from typing import Any, Optional, Type
from Options import Option
from ..Options import OracleOfAgesOptions, OracleOfAgesWarpToStartLocation
from Options import OptionError
from ..data.Entrances import WARPS_DATA
from .. import OracleOfAgesWorld
from ..common.Util import get_prices_pool
from ..data.Constants import VALID_RUPEE_VALUES

# -----------------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------------
def restrict_non_local_items(world: OracleOfAgesWorld):
    # Restrict non_local_items option in cases where it's incompatible with other options that enforce items
    # to be placed locally (e.g. dungeon items with keysanity off)
    if not world.options.keysanity_small_keys:
        world.options.non_local_items.value -= world.item_name_groups["Small Keys"]
    if not world.options.keysanity_boss_keys:
        world.options.non_local_items.value -= world.item_name_groups["Boss Keys"]
    if not world.options.keysanity_maps_compasses:
        world.options.non_local_items.value -= world.item_name_groups["Dungeon Maps"]
        world.options.non_local_items.value -= world.item_name_groups["Compasses"]
    if not world.options.keysanity_slates:
        world.options.non_local_items.value -= set(["Slate"])

# -----------------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------------
def shuffle_entrances(world: OracleOfAgesWorld):
    shuffled = list(world.randomized_entrances.values())
    world.random.shuffle(shuffled)
    world.randomized_entrances = dict(zip(world.randomized_entrances, shuffled))

# -----------------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------------
def randomize_shop_prices(world: OracleOfAgesWorld):
    prices_pool = get_prices_pool()
    world.random.shuffle(prices_pool)
    global_prices_factor = world.options.shop_prices_factor.value / 100.0
    for key, divider in world.shop_prices.items():
        floating_price = prices_pool.pop() * global_prices_factor / divider
        for i, value in enumerate(VALID_RUPEE_VALUES):
            if value > floating_price:
                world.shop_prices[key] = VALID_RUPEE_VALUES[i-1]
                break
            
# -----------------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------------
def ooa_generate_early(world: OracleOfAgesWorld):

    world.remaining_progressive_gasha_seeds = world.options.deterministic_gasha_locations.value

    if world.interpret_slot_data(None):
        return
    conflicting_rings = world.options.required_rings.value & world.options.excluded_rings.value
    if len(conflicting_rings) > 0:
        raise OptionError("Required Rings and Excluded Rings contain the same element(s)", conflicting_rings)
    
    if world.options.shuffle_dungeons:
        world.randomized_entrances = {}
        for warpName, warpData in WARPS_DATA.items():
            if "dungeon" not in warpData: # Not a dungeon, skip it
                continue; 
            if "require_option" not in warpData or hasattr(world.options, warpData["require_option"]) and getattr(world.options, warpData["require_option"]):
                world.randomized_entrances[warpName] = warpName
        shuffle_entrances(world)
    
    restrict_non_local_items(world)
    randomize_shop_prices(world)