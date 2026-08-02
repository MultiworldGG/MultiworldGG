from .Items import _all_items, key_item_names, DSRItemCategory, DSRItemData, item_dictionary, _all_items_base, DSRUpgradeType
from .Skips import get_user_selected_skips
from .Groups import item_name_groups
from .Locations import location_dictionary, DSRLocationCategory


# Type, id, max level
infusion_types = [
    ("Normal", 0, 15, 0),
    ("Crystal", 1, 5, 10),
    ("Lightning", 2, 5, 10),
    ("Raw", 3, 5, 5),
    ("Magic", 4, 10, 5),
    ("Enchanted", 5, 5, 10),
    ("Divine", 6, 10, 5),
    ("Occult", 7, 5, 10),
    ("Fire", 8, 10, 5),
    ("Chaos", 9, 5, 10)
]

# No raw, occult, enchanted, or chaos (for shields, crossbow, etc)
restricted_infusion_types = [
    ("Normal", 0, 15, 0),
    ("Crystal", 1, 5, 10),
    ("Lightning", 2, 5, 10),
    ("Magic", 4, 10, 5),
    ("Divine", 6, 10, 5),
    ("Fire", 8, 10, 5),
]

# Unique only
unique_infusion_types = [
        ("Normal", 0, 5, 0)
]

def BuildRequiredItemPool(world, count):
    item_pool = []
    remaining_count = count

    key_items = [item for item in _all_items if item.name in key_item_names or item.category == DSRItemCategory.KEY_ITEM]
    for item in key_items:
        if item.name not in ["Dungeon Cell Key", "Estus Flask", "Undead Asylum F2 East Key", "Big Pilgrim's Key", "Master Key"]:
            item_pool.append(item)
            remaining_count = remaining_count - 1

    if(world.options.fogwall_sanity.value == True):
        fogwalls = [item for item in _all_items if item.category in [DSRItemCategory.FOGWALL] and item.name != "Fog Wall Key - Northern Undead Asylum"]
        for item in fogwalls:
            item_pool.append(item)
            remaining_count = remaining_count - 1

    if (world.options.boss_fogwall_sanity.value == True):
        bossfogwalls = [item for item in _all_items if item.category in [DSRItemCategory.BOSSFOGWALL]]
        for item in bossfogwalls:
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

def UpgradeEquipment(itemcode, options, world):
    upg = None
    if itemcode == None:
        return upg
    # Find the weapon by getting matching row from base
    for row in _all_items_base:
        if itemcode == row[1] + 11110000: 
            if (row[2] != DSRItemCategory.WEAPON and row[2] != DSRItemCategory.SHIELD): # Item found but not a weapon
                break
            if (world.random.randint(1,100) > options.upgraded_weapons_percentage): # Didn't roll RNG well enough
                break
            # print(f'upgrading, itemcode = {itemcode} name={row[0]}')
            # print(f'row {row[0]} {row[1]} {row[2]}')
            if row[4] == DSRUpgradeType.Infusable: 
                itype = world.random.choice([typ for typ in infusion_types if typ[0] in options.upgraded_weapons_allowed_infusions])
            elif row[4] == DSRUpgradeType.InfusableRestricted:
                allowed_types = [typ for typ in restricted_infusion_types if typ[0] in options.upgraded_weapons_allowed_infusions]
                if len(allowed_types) == 0: # Can't upgrade restricted items because none of its types are allowed
                    break;
                itype = world.random.choice(allowed_types)
            elif row[4] == DSRUpgradeType.Unique: 
                if "Normal" not in options.upgraded_weapons_allowed_infusions:
                    break
                itype = unique_infusion_types[0]
            else:
                break  # an unhandled infusion type - done with item

            # Normal types - exclude +0 weapon, and don't include name prefix
            if (itype[0] == "Normal"):
                minlvl = max(1, options.upgraded_weapons_min_level.value)
                # If min level > normal max, skip upg (happens for unique items))
                if options.upgraded_weapons_min_level.value > itype[2]:
                    break;
                maxlvl = min(itype[2], options.upgraded_weapons_max_level.value)
                
                if maxlvl < minlvl:  # could never use this infusion
                    break;  #done with item

                lvl = world.random.randint(minlvl, maxlvl)
                
                upg = f'{itype[0]}:{lvl}'
                # print(f"{upg}")
                return upg
            # Everything else - Include +0 weapon, and add prefix to name
            else:
                adj = options.upgraded_weapons_adjusted_levels

                # Min level is greater of "0" or "user specified min level minus potential adjustment"
                minlvl = max(0, options.upgraded_weapons_min_level.value - (itype[3] if adj else 0))
                # Min level is lesser of "type max level" or "user specified max level minus potential adjustment"
                maxlvl = min(itype[2], options.upgraded_weapons_max_level.value - (itype[3] if adj else 0))
                
                if maxlvl < minlvl:  # could never use this infusion
                    break;  #done with item
                lvl = world.random.randint(minlvl, maxlvl)
                
                upg = f'{itype[0]}:{lvl}'
                # print(f"{upg}")
                return upg
            break;
    return upg

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
def ReplaceItem(name, world):
    if (name in titanite_replacements):
        replacements = titanite_replacements[name]
        weights = titanite_replacement_weights[name]
        newname = world.random.choices(replacements, weights=weights)[0]
        return newname

    return name
