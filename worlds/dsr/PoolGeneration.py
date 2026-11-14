from .Items import _all_items, key_item_names, DSRItemCategory, DSRItemData, item_dictionary, _all_items_base, DSRUpgradeType
from .Skips import get_user_selected_skips
from .Groups import item_name_groups, dlc_prog_items, pw_prog_items, gh_prog_items, post_os_prog_items
from .Options import GoalConditionOption
from .Locations import location_dictionary, DSRLocationCategory

def BuildRequiredItemPool(world, count, ignorable_items):
    item_pool = []
    remaining_count = count

    key_items = [item for item in _all_items if item.name in key_item_names or item.category == DSRItemCategory.KEY_ITEM]

    # print(f"DSR [{world.player_name}]: poolgen key items = {key_items}")

    for item in key_items:
        if item.name not in ignorable_items and item.name not in ["Dungeon Cell Key", "Estus Flask", "Undead Asylum F2 East Key", "Big Pilgrim's Key", "Master Key"]:
            item_pool.append(item)
            remaining_count = remaining_count - 1
            # print(f"DSR [{world.player_name}]: added key item to pool: {item.name}")

    # print(f"DSR [{world.player_name}]: itempool1: {item_pool}")

    if(world.options.fogwall_sanity.value == True):
        fogwalls = [item for item in _all_items if item.category in [DSRItemCategory.FOGWALL] and item.name != "Fog Wall Key - Northern Undead Asylum"]
        for item in fogwalls:
            if item.name not in ignorable_items:
                item_pool.append(item)
                remaining_count = remaining_count - 1

    if (world.options.boss_fogwall_sanity.value == True):
        bossfogwalls = [item for item in _all_items if item.category in [DSRItemCategory.BOSSFOGWALL]]
        for item in bossfogwalls:
            if item.name not in ignorable_items:
                item_pool.append(item)
                remaining_count = remaining_count - 1

    useful_items = [item for item in _all_items if item.category in [DSRItemCategory.EMBER, DSRItemCategory.FIRE_KEEPER_SOUL] ]
    for item in useful_items:
        item_pool.append(item)
        remaining_count = remaining_count - 1

    if world.options.soul_multiplier_steps > 0:
        for i in range(world.options.soul_multiplier_steps):
            item = item_dictionary["Progressive Soul Multiplier"]
            item_pool.append(item)
            remaining_count = remaining_count - 1

    if world.options.weight_multiplier_steps > 0:
        for i in range(world.options.weight_multiplier_steps):
            item = item_dictionary["Progressive Weight Reducer"]
            item_pool.append(item)
            remaining_count = remaining_count - 1

    if world.options.incoming_weapon_upgrade_steps > 0:
        for i in range(world.options.incoming_weapon_upgrade_steps):
            item = item_dictionary["Progressive Incoming Weapon Upgrade"]
            item_pool.append(item)
            remaining_count = remaining_count - 1
    # print(f"DSR [{world.player_name}]: itempool1: {item_pool}")
    # print(f"item pool = [{item_pool}]")

    # Start commenting out of skips
    # allow_skips_options: list[OptionCounter] = [world.options.skip_logic_easy, 
    #                        world.options.skip_logic_medium, 
    #                        world.options.skip_logic_hard, 
    #                        world.options.skip_logic_very_hard]
    # skip_progression_item_groups: set[str] = set()
    # skip_progression_items: set[str] = set()


    # for skip in get_user_selected_skips(allow_skips_options):
    #     skip_progression_item_groups = skip_progression_item_groups.union(skip.required_items_groups)
    #     skip_progression_items = skip_progression_items.union(skip.required_items)

    # for group in skip_progression_item_groups:
    #     if not world.options.no_weapon_requirements:
    #         group = f"Skip Tools - {group}"

    #     skip_progression_items.update(item_name_groups[group])

    # result: list[DSRItemData] = []
    # for item in skip_progression_items:
    #     dsr_item = item_dictionary[item]

    #     # TODO Temporary up to the other comment, remove this when enemy drops or shop items get added into logic, otherwise too many items get generated
    #     is_tracked_by_logic = True
    #     if item not in [loc.default_item for loc in location_dictionary.values()]:
    #         is_tracked_by_logic = False

    #     for loc in location_dictionary.values():
    #         if loc.default_item == item: 
    #             if loc.category in [DSRLocationCategory.ENEMY_DROP, DSRLocationCategory.SHOP_ITEM, DSRLocationCategory.SKIP]:
    #                 is_tracked_by_logic = False
        
    #     if not is_tracked_by_logic:
    #         continue
    #     #### 
    #     if dsr_item not in item_pool:
    #         result.append(dsr_item)

    # generated_skip_items_names = [x.name for x in result]

    # item_pool.extend(result)
    # remaining_count = remaining_count - len(result)

    # End commenting out of skips
    generated_skip_items_names = []


    world.random.shuffle(item_pool)
    return item_pool, generated_skip_items_names

def BuildGuaranteedItemPool(world):
    item_pool = []
    if world.options.guaranteed_items.value:
        for item_name, item_quant in world.options.guaranteed_items.value.items():
            item = item_dictionary[item_name]
            item_pool += [item] * item_quant
    world.random.shuffle(item_pool)
    return item_pool

titanite_replacements = {
    # 25% 2 large, 41.67% chunk, 8.33% 2 chunk
    "Extra Titanite" : ["Large Titanite Shard x2", "Titanite Chunk", "Titanite Chunk x2"],
    # 25% 2 green, 41.67% red chunk, 8.33% 2 red chunk
    "Extra Red Titanite" : ["Green Titanite Shard x2", "Red Titanite Chunk", "Red Titanite Chunk x2"],
    # 25% 2 green, 41.67% blue chunk, 8.33% 2 blue chunk
    "Extra Blue Titanite" : ["Green Titanite Shard x2", "Blue Titanite Chunk", "Blue Titanite Chunk x2"],
    # 25% 2 green, 41.67% white chunk, 8.33% 2 white chunk
    "Extra White Titanite" : ["Green Titanite Shard x2", "White Titanite Chunk", "White Titanite Chunk x2"],
    # 20% 2 large, 20% 2 green, 10% chunk, 10% blue chunk, 10% red chunk, 10% white chunk, 10% titanite slab
    "Extra GH Titanite" : ["Large Titanite Shard x2", "Green Titanite Shard x2", "Titanite Chunk", "Blue Titanite Chunk", "Red Titanite Chunk", "White Titanite Chunk", "Titanite Slab"],
}
titanite_replacement_weights = {
    "Extra Titanite" : [3, 5, 1],
    "Extra Red Titanite" : [3, 5, 1],
    "Extra Blue Titanite" : [3, 5, 1],
    "Extra White Titanite" : [3, 5, 1],
    "Extra GH Titanite" : [2, 2, 1, 1, 1, 1, 1],
}
def ReplaceItem(world, name):
    if (name in titanite_replacements):
        replacements = titanite_replacements[name]
        weights = titanite_replacement_weights[name]
        newname = world.random.choices(replacements, weights=weights)[0]
        return newname

    return name
