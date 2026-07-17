
from BaseClasses import Item, ItemClassification
from ..data.Items import *
from ..data.Locations import *
from ..data.Constants import *
from typing import TYPE_CHECKING
from .. import OraclesMasterKeys
from Options import OptionError
from .CreationRegions import location_is_active

from .. import OracleOfAgesWorld

# -----------------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------------
def build_item_pool_dict(world: OracleOfAgesWorld):
    item_pool_dict = {}
    filler_item_count = 0
    remaining_rings = len({name for name, idata in ITEMS_DATA.items() if "ring" in idata}) - len(world.options.excluded_rings.value)
    for loc_name, loc_data in LOCATIONS_DATA.items():

        if "vanilla_item" not in loc_data:
            #print("Can't create item from location '",loc_name ,"' because it doesn't have one")
            continue

        item_name = loc_data['vanilla_item']

        if "randomized" in loc_data and loc_data["randomized"] is False:
            item = world.create_item(item_name)
            location = world.multiworld.get_location(loc_name, world.player)
            location.place_locked_item(item)
            #print("placing locked item '",loc_data['vanilla_item'] ,"' in '",loc_name ,"'")
            continue
        if not location_is_active(world, loc_name, loc_data):
            #print("Can't create item '",loc_data['vanilla_item'] ,"' because '",loc_name ,"' is not active")
            continue
    
        if item_name == "Filler Item":
            filler_item_count += 1
            continue

        if world.options.master_keys != OraclesMasterKeys.option_disabled and "Small Key" in item_name:
            # Small Keys don't exist if Master Keys are set to replace them
            filler_item_count += 1
            continue
        if world.options.master_keys == OraclesMasterKeys.option_all_dungeon_keys and "Boss Key" in item_name:
            # Boss keys don't exist if Master Keys are set to replace them
            filler_item_count += 1
            continue

        item_name = loc_data['vanilla_item']
        if "Ring" in item_name:
            if remaining_rings > 0:
                item_name = "Random Ring"
                remaining_rings -= 1
            else:
                filler_item_count += 1
                continue

        if "essence" in loc_data and loc_data["essence"] is True:
            # If essences are not shuffled, place and lock this item directly on the pedestal.
            # Otherwise, the fill algorithm will take care of placing them anywhere in the multiworld.
            if not world.options.shuffle_essences:
                essence_item = world.create_item(item_name)
                loc = world.multiworld.get_location(loc_name, world.player)
                loc.place_locked_item(essence_item)
                continue

        item_pool_dict[item_name] = item_pool_dict.get(item_name, 0) + 1

    # If Master Keys are enabled, put one for every dungeon
    if world.options.master_keys != OraclesMasterKeys.option_disabled:
        for small_key_name in ITEM_GROUPS["Master Keys"]:
            if world.options.linked_heros_cave.value > 0 or small_key_name != "Master Key (Linked Hero's Cave)":
                item_pool_dict[small_key_name] = 1
                filler_item_count -= 1

    # Add the required rings
    ring_copy = sorted(world.options.required_rings.value.copy())
    for _ in range(len(ring_copy)):
        ring_name = f"{ring_copy.pop()}!USEFUL"
        item_pool_dict[ring_name] = item_pool_dict.get(ring_name, 0) + 1

        if item_pool_dict["Random Ring"] > 0:
            # Take from set ring pool first
            item_pool_dict["Random Ring"] -= 1
        else:
            # Take from filler after
            filler_item_count -= 1

    # Add as many filler items as required
    for _ in range(filler_item_count):
        random_filler_item = ooa_get_filler_item_name(world)
        item_pool_dict[random_filler_item] = item_pool_dict.get(random_filler_item, 0) + 1
    
    # Perform adjustments on the item pool
    item_pool_adjustements = [
        ["Flute", world.options.animal_companion.current_key.title() + "'s Flute"],  # Put a specific flute
        ["Gasha Seed", "Seed Satchel"],             # Add a 3rd satchel that is usually obtained in linked games (99 seeds)
        ["Gasha Seed", "Bombs (10)"],               # Add one more bomb compared to vanilla to reach 99 max bombs
        ["Gasha Seed", "Potion"],                   # Replace some Gasha Seed by 2 potions.
        ["Gasha Seed", "Potion"],                   # ^
        ["Gasha Seed", "Rupees (200)"],              # and one by rupees
        ["Gasha Seed", "Progressive Sword"],        # Need an additionnal sword to go to L3
    ]

    for i, pair in enumerate(item_pool_adjustements):
        original_name = pair[0]
        replacement_name = pair[1]
        item_pool_dict[original_name] -= 1
        item_pool_dict[replacement_name] = item_pool_dict.get(replacement_name, 0) + 1

    return item_pool_dict


# -----------------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------------
def create_rings(world: OracleOfAgesWorld, amount):
    # Get a subset of as many rings as needed
    ring_names = [name for name, idata in ITEMS_DATA.items() if "ring" in idata]
    # Remove excluded rings, and required rings because they'll be added later anyway
    ring_names = [name for name in ring_names if name not in world.options.required_rings.value and name not in world.options.excluded_rings.value]

    world.random.shuffle(ring_names)
    del ring_names[amount:]
    for ring_name in ring_names:
        world.multiworld.itempool.append(world.create_item(ring_name))
    world.random_rings_pool = ring_names

# -----------------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------------
def ooa_get_filler_item_name(world: OracleOfAgesWorld) -> str:
    FILLER_ITEM_NAMES = [
        "Rupees (1)", "Rupees (5)", "Rupees (5)", "Rupees (10)", "Rupees (10)",
        "Rupees (20)", "Rupees (30)",
        "Gasha Seed", "Gasha Seed",
        "Potion"
    ]

    item_name = world.random.choice(FILLER_ITEM_NAMES)
    return item_name



# -----------------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------------
def place_seed(world: OracleOfAgesWorld, seed_name: str, location_name: str):
    seed_item = world.create_item(seed_name)
    world.pre_fill_seeds[location_name] = seed_item
    world.pre_fill_items.append(seed_item)

# -----------------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------------
def ooa_create_seeds_items(world: OracleOfAgesWorld):
    
    # Grab/validate the duplicate trees setting
    duplicate_trees = world.options.duplicate_seed_trees.value

    if len(duplicate_trees) > 3:
        raise OptionError("Can't select more than 3 duplicate seed trees")

    for entry in duplicate_trees:
        if entry not in TREES_TABLE:
            raise OptionError(f"Invalid duplicate seed tree entry: {entry}")

    duplicate_trees_to_process = [TREES_TABLE[tree] for tree in duplicate_trees]

    # If all is good, proceed to seed placement...

    # Grab the seeds to place. We'll shuffle the duplicate seeds list, since we're only getting 3 (or 2...) of the 5 types
    seeds_to_place = list(SEED_ITEMS)
    duplicate_seeds_to_place = list(SEED_ITEMS)

    # Consolidate the lists of non-duplicate trees and duplicates
    manually_placed_trees = ["Lynna City: Seed Tree"] + duplicate_trees_to_process
    trees_to_process = [
        name for key, name in TREES_TABLE.items() if name not in manually_placed_trees
    ]

    # If there are fewer than 3 duplicates specified, choose random ones (other than Lynna) to get it up to 3
    world.random.shuffle(trees_to_process)
    for i in range(3 - len(duplicate_trees_to_process)):
        duplicate_trees_to_process.append(trees_to_process.pop())

    # Place default seed type in Lynna tree
    place_seed(world, SEED_ITEMS[world.options.default_seed.value], "Lynna City: Seed Tree")

    # Cleanup depending on whether Lynna was specified as a duplicate...
    if "Lynna City: Seed Tree" not in duplicate_trees_to_process:
        # If Lynna was NOT specified as a duplicate, we just need to remove the default seed type from the list of seeds.
        # In this case, it's not going to be in either trees_to_process or duplicate_trees_to_process
        del seeds_to_place[world.options.default_seed.value]
    else:
        # If Lynna is specified as a duplicate, then we just remove it from the list of duplicates, since we already placed
        # something there. We don't need to worry about anything else; in this case trees_to_process will contain 5 trees
        # representing all 5 types. One of those will match whatever Lynna is, guaranteeing it to be a duplicate as desired.
        del duplicate_seeds_to_place[world.options.default_seed.value]
        duplicate_trees_to_process.remove("Lynna City: Seed Tree")

    # Place remaining seeds on remaining trees
    for seed in seeds_to_place:
        place_seed(world, seed, trees_to_process.pop())

    # Fill out the duplicates
    world.random.shuffle(duplicate_seeds_to_place)
    for tree in duplicate_trees_to_process:
        place_seed(world, duplicate_seeds_to_place.pop(), tree)

# -----------------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------------
def ooa_create_items(world: OracleOfAgesWorld):
    ooa_create_seeds_items(world)
    item_pool_dict = build_item_pool_dict(world)
    
    # Create items following the dictionary that was previously constructed
    if (item_pool_dict.get("Random Ring")):
        create_rings(world, item_pool_dict["Random Ring"])
        del item_pool_dict["Random Ring"]

    for item_name, quantity in item_pool_dict.items():
        for i in range(quantity):
            prefill_item = None
            if ("Small Key" in item_name or "Master Key" in item_name) and not world.options.keysanity_small_keys:
                prefill_item = world.create_item(item_name)
            elif "Boss Key" in item_name and not world.options.keysanity_boss_keys:
                prefill_item = world.create_item(item_name)
            elif ("Compass" in item_name or "Dungeon Map" in item_name) and not world.options.keysanity_maps_compasses:
                prefill_item = world.create_item(item_name)
            elif "Slate" in item_name and not world.options.keysanity_slates:
                prefill_item = world.create_item(item_name)
            else:
                world.multiworld.itempool.append(world.create_item(item_name))        
            if (prefill_item is not None):
                world.dungeon_items.append(prefill_item)
                world.pre_fill_items.append(prefill_item)