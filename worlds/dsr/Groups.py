import typing
from BaseClasses import Location, Region
from .Locations import location_tables, location_skip_categories, location_dictionary
from .Items import item_dictionary, DSRItemCategory, DSRWeaponType, _all_items_base

multiplayer_items = [
    "Eye of Death",
    "Eye of Death x3",
    "Cracked Red Eye Orb",
    "Cracked Red Eye Orb x4",
    "Cracked Red Eye Orb x6",
    "Indictment",
    "White Sign Soapstone",
    "Red Sign Soapstone",
    "Red Eye Orb",
    "Black Separation Crystal",
    "Orange Guidance Soapstone",
    "Book of the Guilty",
    "Servant Roster",
    "Blue Eye Orb",
    "Dragon Eye",
    "Black Eye Orb",
    "Purple Coward's Crystal",
    "Dried Finger",
    "Cat Covenant Ring",
    "Darkmoon Blade Covenant Ring",
]

covenant_items = [
    "Sunlight Medal",
    "Sunlight Medal x3",
    "Cat Covenant Ring",
    "Souvenir of Reprisal",
]

progression_items = [
    "Annex Key",
    "Archive Prison Extra Key",
    "Archive Tower Cell Key",
    "Archive Tower Giant Cell Key",
    "Archive Tower Giant Door Key",
    "Bequeathed Lord Soul Shard (Four Kings)",
    "Bequeathed Lord Soul Shard (Seath)",
    "Big Pilgrim's Key",
    "Blighttown Key",
    "Broken Pendant",
    "Cage Key",
    "Covenant of Artorias",
    "Crest Key",
    "Crest of Artorias",
    "Darkmoon Seance Ring",
    "Dungeon Cell Key",
    "Key to Depths",
    "Key to New Londo Ruins",
    "Lord Soul (Bed of Chaos)",
    "Lord Soul (Nito)",
    "Lordvessel",
    "Peculiar Doll",
    "Residence Key",
    "Skull Lantern",
    "Undead Asylum F2 East Key",
    "Undead Asylum F2 West Key",
    "Watchtower Basement Key",
]

item_name_groups = {
    "Key items"         : [item.name for item in item_dictionary.values() if item.category in [DSRItemCategory.KEY_ITEM]] + ["Covenant of Artorias","Orange Charred Ring", "Skull Lantern", "Darkmoon Seance Ring"],
    "Fog Wall Keys"     : [item.name for item in item_dictionary.values() if item.category in [DSRItemCategory.FOGWALL]],
    "Boss Fog Wall Keys": [item.name for item in item_dictionary.values() if item.category in [DSRItemCategory.BOSSFOGWALL]],
    "Consumables"       : [item.name for item in item_dictionary.values() if item.category in [DSRItemCategory.CONSUMABLE] and "soul" not in item.name.lower() and "fire keeper" not in item.name.lower()],
    "Souls"             : [item.name for item in item_dictionary.values() if item.category in [DSRItemCategory.CONSUMABLE] and "soul" in item.name.lower() and "fire keeper" not in item.name.lower()],
    "Rings"             : [item.name for item in item_dictionary.values() if item.category in [DSRItemCategory.RING]],
    "Upgrade Materials" : [item.name for item in item_dictionary.values() if item.category in [DSRItemCategory.UPGRADE_MATERIAL]],
    "Spells"            : [item.name for item in item_dictionary.values() if item.category in [DSRItemCategory.SPELL]],
    "Armor"             : [item.name for item in item_dictionary.values() if item.category in [DSRItemCategory.ARMOR]],
    "Weapons"           : [item.name for item in item_dictionary.values() if item.category in [DSRItemCategory.WEAPON]],
    "Shields"           : [item.name for item in item_dictionary.values() if item.category in [DSRItemCategory.SHIELD]],
    "Traps"             : [item.name for item in item_dictionary.values() if item.category in [DSRItemCategory.TRAP]],
    "Boss Souls"        : [item.name for item in item_dictionary.values() if item.category in [DSRItemCategory.BOSS_SOUL]],
    "Embers"            : [item.name for item in item_dictionary.values() if item.category in [DSRItemCategory.EMBER]],
    # Weapon types
    "Ammunition"        : [item[0] for item in _all_items_base if item[2] == DSRItemCategory.WEAPON and item[3] == DSRWeaponType.RangedAmmunition],
    "Spell Tools"       : [item[0] for item in _all_items_base if item[2] == DSRItemCategory.WEAPON and item[3] == DSRWeaponType.SpellTool],
    "Melee Weapons"     : [item[0] for item in _all_items_base if item[2] == DSRItemCategory.WEAPON and item[3] == DSRWeaponType.Melee],
    "Ranged Weapons"    : [item[0] for item in _all_items_base if item[2] == DSRItemCategory.WEAPON and item[3] == DSRWeaponType.Ranged],
    "Bows"              : [item[0] for item in _all_items_base if item[2] == DSRItemCategory.WEAPON and item[3] == DSRWeaponType.Ranged and "bow" in item[0].lower() and not "cross" in item[0].lower()],
    # Spell Tool types
    "Catalysts"         : [item for item in item_dictionary.keys() if "catalyst" in item.lower()],
    "Talismans"         : [item for item in item_dictionary.keys() if "talisman" in item.lower() and "lloyd" not in item.lower()],
    # Useful items
    "Progression Items" : [item for item in progression_items],
    "Lord Souls"        : [item for item in item_dictionary.keys() if "lord soul" in item.lower()],
    "Fire Keeper Souls" : [item for item in item_dictionary.keys() if "fire keeper" in item.lower()],
    # Mostly useless items
    "Carvings"          : [item for item in item_dictionary.keys() if "carving" in item.lower()],
    "Multiplayer Items" : [item for item in multiplayer_items],
    "Covenant Items"    : [item for item in covenant_items],
    "Junk"              : [item for item in item_dictionary.keys() if "carving" in item.lower()] + [item for item in multiplayer_items] + [item for item in covenant_items] + ["Pendant", "Prism Stone x20", "Gold Coin", "Silver Coin x5"],

    # Following groups are used for skips
    # These items can be wielded by almost (max needs 5 levels of investment) any character from beginning of the game. 

    # Strength requirement for these is max 10 
    "Skip Tools - Medium Shields" :  ["Bloodshield","Caduceus Kite Shield","Crest Shield", 
                                    "Dragon Crest Shield", "East-West Shield", "Grass Crest Shield", "Heater Shield",
                                    "Knight Shield", "Large Leather Shield", "Sanctus", "Spider Shield", 
                                    "Spiked Shield", "Tower Kite Shield", "Wooden Shield"],

    # INT requirement for these is max 12
    "Skip Tools - Catalysts" :       ["Sorcerer's Catalyst", "Beatrice's Catalyst", 'Tin Banishment Catalyst', 
                                     'Oolacile Ivory Catalyst', "Demon's Catalyst", 'Oolacile Catalyst'],

    # Max requirements DEX 14 STR 11
    "Skip Tools - Bows" :            ['Short Bow', 'Longbow', 'Composite Bow'],
    "Skip Tools - Ranged Weapons": ['Short Bow', 'Longbow', 'Composite Bow', "Light Crossbow"],

    # Following are used in runs with disabled item requirement
    "Medium Shields"    : ["Balder Shield","Black Knight Shield","Bloodshield","Caduceus Kite Shield","Crest Shield", "Crystal Shield", 
                    "Dragon Crest Shield", "East-West Shield", "Gargoyle's Shield", "Grass Crest Shield", "Heater Shield", "Hollow Soldier Shield", 
                    "Iron Round Shield", "Knight Shield", "Large Leather Shield","Pierce Shield", "Sanctus", "Silver Knight Shield", "Spider Shield", 
                    "Spiked Shield", "Sunlight Shield", "Tower Kite Shield", "Wooden Shield"],
}


location_name_groups = {
    "Fog Walls": set(),
    "Boss Fog Walls": set(),
    "Shop Basic Items": set(),
    "Shop Extended Items": set(),
    "Boss Souls" : set(),
    "Boss Humanity" : set(),
    "Boss Bones" : set(),
    "Boss Drops" : set(),
    "Lord Souls" : set(),
    "Mimic Drops" : set(),
    "Black Knight Titanites" : set(),
    "Black Knight Weapons" : set(),
    "Crystal Lizards" : set(),
    "Chest Items" : set(),
    "Corpse Filler Items": set(),
    "Corpse Prog Items": set(),
    "Corpse Useful Items": set(),
    "Hostile Npc Drops": set(),
    "Miniboss Drops": set(),
    "Misc Drops": set(),
    "Frozen Blacksmiths": set(),
    "Corpse Ring Items": set(),
    "Npc Prog Items": set(),
}

category_to_loc_name_map = {
    "FOG_WALL": "Fog Walls",
    "BOSS_FOG_WALL": "Boss Fog Walls",
    "SHOP_ITEM": "Shop Basic Items",
    "SHOP_EXTENDED_ITEM": "Shop Extended Items",
    "BOSS_SOUL": "Boss Souls",
    "BOSS_HUMANITY": "Boss Humanity",
    "BOSS_BONE": "Boss Bones",
    "BOSS_DROP": "Boss Drops",
    "LORD_SOUL": "Lord Souls",
    "MIMIC_DROP": "Mimic Drops",
    "BK_TITANITE": "Black Knight Titanites",
    "BK_WEAPON": "Black Knight Weapons",
    "CRYSTAL_LIZARD": "Crystal Lizards",
    "CHEST_ITEM": "Chest Items",
    "CORPSE_FILLER_ITEM": "Corpse Filler Items",
    "CORPSE_PROG_ITEM": "Corpse Prog Items",
    "CORPSE_USEFUL_ITEM": "Corpse Useful Items",
    "HOSTILE_NPC_DROP": "Hostile Npc Drops",
    "MINIBOSS_DROP": "Miniboss Drops",
    "MISC_DROP": "Misc Drops",
    "FROZEN_BLACKSMITH": "Frozen Blacksmiths",
    "CORPSE_RING_ITEM": "Corpse Ring Items",
    "NPC_PROG_ITEM": "Npc Prog Items",
}

dlc_prog_items = [
    "Broken Pendant",
    "Crest Key",
    "Boss Fog Wall Key - Sanctuary Guardian",
    "Boss Fog Wall Key - Artorias",
    "Boss Fog Wall Key - Manus",
    # sunlight maggot and lantern?
]

pw_prog_items = [
    "Peculiar Doll",
    "Annex Key",
    "Fog Wall Key - Painted World",
    "Boss Fog Wall Key - Crossbreed Priscilla",
]

gh_prog_items = [
    "Fog Wall Key - Ash Lake Entrance",
]

#Post Ornstein And Smough
post_os_prog_items = [
    "Lordvessel",
    "Boss Fog Wall Key - Seath First Encounter",
    "Archive Tower Cell Key",
    "Archive Prison Extra Key",
    "Archive Tower Giant Cell Key",
    "Archive Tower Giant Door Key",
    "Boss Fog Wall Key - Demon Firesage",
    "Boss Fog Wall Key - Centipede Demon",
    "Boss Fog Wall Key - Bed of Chaos",
    "Boss Fog Wall Key - Gwyn",
    "Boss Fog Wall Key - Sanctuary Guardian",
    "Boss Fog Wall Key - Artorias",
    "Boss Fog Wall Key - Manus",
    "Boss Fog Wall Key - Nito",
    "Key to the Seal",
    "Fog Wall Key - New Londo (Lower)",
    "Covenant of Artorias",
    "Boss Fog Wall Key - Four Kings",
    "Lord Soul (Nito)",
    "Lord Soul (Bed of Chaos)",
    "Bequeathed Lord Soul Shard (Four Kings)",
    "Bequeathed Lord Soul Shard (Seath)",
    "Orange Charred Ring",
]

post_os_cata_prog_items = [
    "Fog Wall Key - Catacombs",
    "Fog Wall Key - Tomb of the Giants",
    "Boss Fog Wall Key - Pinwheel",
    "Skull Lantern", # light only needed in dlc and TotG, and dlc is known excluded if this is included
    "Sunlight Maggot", # light only needed in dlc and TotG, and dlc is known excluded if this is included
    "Darkmoon Seance Ring",
    "Boss Fog Wall Key - Gwyndolin",
]

# Map door+shortcut regions to their "parent" region
region_parents = {
    "Undead Asylum Cell Door"   : "Undead Asylum Cell",
    "Undead Burg Basement Door" : "Upper Undead Burg",
    "Depths to Blighttown Door" : "Depths",
    "Door between Upper New Londo and Valley of the Drakes" : "Upper New Londo Ruins",
    "New Londo Ruins Door to the Seal" : "Upper New Londo Ruins",
    "Demon Ruins Shortcut" : "Demon Ruins",
}

## Add all locations to their region, DLC, and category groups
for region in location_tables.keys(): # For each region
    location_name_groups[region] = set() # Create a location name group
    for location in location_tables[region]: # For each location in each region
        # Add each location to its region location group
        location_name_groups[region].add(location.name)
        # Add each location to its category type location group (e.g. DOOR -> All Doors, ITEM_LOT -> All ITEM_LOTs, etc)
        if location.category.name in category_to_loc_name_map.keys():
            location_name_groups[category_to_loc_name_map[location.category.name]].add(location.name)

# Combine region groups into their un-conditioned selves (e.g. "Northern Undead Asylum - After F2 East Door" -> "Northern Undead Asylum")
for group in list(location_name_groups.keys()):
    gsplit = group.split(' - ')
    if len(gsplit) > 1 and gsplit[0] in location_name_groups.keys():
        location_name_groups[gsplit[0]] = location_name_groups[gsplit[0]].union(location_name_groups[group])
        del location_name_groups[group]

# Further, combine any remaining regions that have differently-named parents into those parents
for group in list(location_name_groups.keys()):
    if group in region_parents.keys():
        pgroup = region_parents[group]
        location_name_groups[pgroup] = location_name_groups[pgroup].union(location_name_groups[group])
        del location_name_groups[group]

# Cleanup loc groups to not bother with skipped locations: those are locked / will give warnings during generate if we exclude them
for group in list(location_name_groups.keys()):
    for location in list(location_name_groups[group]):
        if location_dictionary[location].category in location_skip_categories:
            location_name_groups[group].remove(location)

# Finally, remove any empty groups (e.g. Firelink Altar
for group in list(location_name_groups.keys()):
    if len(list(location_name_groups[group])) == 0:
        location_name_groups.pop(group)

# Print loc groups and how many elements they have
# for group in location_name_groups.keys():
#     print (f'Location Group {group} has {len(location_name_groups[group])} elements')
# # Print item groups and how many elements they have
# for group in item_name_groups.keys():
#     print (f'Item Group {group} has {len(item_name_groups[group])} elements')
