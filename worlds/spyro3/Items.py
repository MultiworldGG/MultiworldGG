from enum import IntEnum
import math
from typing import NamedTuple
from BaseClasses import Item
from .Options import MoneybagsOptions, SparxUpgradeOptions, GemsanityOptions, GoalOptions, SparxForGemsOptions, LevelLockOptions, PowerupLockOptions
from Options import OptionError


class Spyro3ItemCategory(IntEnum):
    EGG = 0,
    SKIP = 1,
    EVENT = 2,
    MISC = 3,
    TRAP = 4,
    SKILLPOINT_GOAL = 5,
    MONEYBAGS = 6,
    HINT = 7,
    GEMSANITY = 8,
    SPARX_POWERUP = 13,
    WORLD_KEY = 14,
    LEVEL_KEY = 15,
    TYPE_POWERUP = 16,
    INDIVIDUAL_POWERUP = 17,
    UT_ITEM = 99  # Universal tracker


class Spyro3ItemData(NamedTuple):
    name: str
    s3_code: int
    category: Spyro3ItemCategory


class Spyro3Item(Item):
    game: str = "Spyro 3"

    @staticmethod
    def get_name_to_id() -> dict:
        base_id = 1230000
        return {item_data.name: (base_id + item_data.s3_code if item_data.s3_code is not None else None) for item_data in _all_items}


key_item_names = {
    "Egg"
}


_all_items = [Spyro3ItemData(row[0], row[1], row[2]) for row in [
    ("Sunny Villa Complete", 2000, Spyro3ItemCategory.EVENT),
    ("Cloud Spires Complete", 2001, Spyro3ItemCategory.EVENT),
    ("Molten Crater Complete", 2002, Spyro3ItemCategory.EVENT),
    ("Seashell Shore Complete", 2003, Spyro3ItemCategory.EVENT),
    ("Sheila's Alp Complete", 2004, Spyro3ItemCategory.EVENT),
    ("Buzz Defeated", 2005, Spyro3ItemCategory.EVENT),
    ("Crawdad Farm Complete", 2006, Spyro3ItemCategory.EVENT),

    ("Icy Peak Complete", 2007, Spyro3ItemCategory.EVENT),
    ("Enchanted Towers Complete", 2008, Spyro3ItemCategory.EVENT),
    ("Spooky Swamp Complete", 2009, Spyro3ItemCategory.EVENT),
    ("Bamboo Terrace Complete", 2010, Spyro3ItemCategory.EVENT),
    ("Sgt. Byrd's Base Complete", 2011, Spyro3ItemCategory.EVENT),
    ("Spike Defeated", 2012, Spyro3ItemCategory.EVENT),
    ("Spider Town Complete", 2013, Spyro3ItemCategory.EVENT),

    ("Frozen Altars Complete", 2014, Spyro3ItemCategory.EVENT),
    ("Lost Fleet Complete", 2015, Spyro3ItemCategory.EVENT),
    ("Fireworks Factory Complete", 2016, Spyro3ItemCategory.EVENT),
    ("Charmed Ridge Complete", 2017, Spyro3ItemCategory.EVENT),
    ("Bentley's Outpost Complete", 2018, Spyro3ItemCategory.EVENT),
    ("Scorch Defeated", 2019, Spyro3ItemCategory.EVENT),
    ("Starfish Reef Complete", 2020, Spyro3ItemCategory.EVENT),

    ("Crystal Islands Complete", 2021, Spyro3ItemCategory.EVENT),
    ("Desert Ruins Complete", 2022, Spyro3ItemCategory.EVENT),
    ("Haunted Tomb Complete", 2023, Spyro3ItemCategory.EVENT),
    ("Dino Mines Complete", 2024, Spyro3ItemCategory.EVENT),
    ("Agent 9's Lab Complete", 2025, Spyro3ItemCategory.EVENT),
    ("Sorceress Defeated", 2026, Spyro3ItemCategory.EVENT),
    ("Bugbot Factory Complete", 2027, Spyro3ItemCategory.EVENT),
    ("Super Bonus Round Complete", 2028, Spyro3ItemCategory.EVENT),
    ("Moneybags Chase Complete", 2029, Spyro3ItemCategory.EVENT),


    ("Egg", 1000, Spyro3ItemCategory.EGG),
    ("Extra Life", 1001, Spyro3ItemCategory.MISC),
    ("Lag Trap", 1002, Spyro3ItemCategory.TRAP),
    ("Filler", 1003, Spyro3ItemCategory.MISC),
    ("Damage Sparx Trap", 1004, Spyro3ItemCategory.TRAP),
    ("Sparxless Trap", 1005, Spyro3ItemCategory.TRAP),
    ("Invincibility (15 seconds)", 1006, Spyro3ItemCategory.MISC),
    ("Invincibility (30 seconds)", 1007, Spyro3ItemCategory.MISC),
    ("Turn Spyro Red", 1008, Spyro3ItemCategory.MISC),
    ("Turn Spyro Blue", 1009, Spyro3ItemCategory.MISC),
    ("Turn Spyro Pink", 1010, Spyro3ItemCategory.MISC),
    ("Turn Spyro Yellow", 1011, Spyro3ItemCategory.MISC),
    ("Turn Spyro Green", 1012, Spyro3ItemCategory.MISC),
    ("Turn Spyro Black", 1013, Spyro3ItemCategory.MISC),
    ("Big Head Mode", 1014, Spyro3ItemCategory.MISC),
    ("Flat Spyro Mode", 1015, Spyro3ItemCategory.MISC),
    ("(Over)heal Sparx", 1016, Spyro3ItemCategory.MISC),
    ("Progressive Sparx Health Upgrade", 1017, Spyro3ItemCategory.MISC),
    ("Skill Point", 1018, Spyro3ItemCategory.SKILLPOINT_GOAL),
    ("Increased Sparx Range", 1019, Spyro3ItemCategory.SPARX_POWERUP),
    ("Sparx Gem Finder", 1020, Spyro3ItemCategory.SPARX_POWERUP),
    ("Extra Hit Point", 1021, Spyro3ItemCategory.SPARX_POWERUP),
    ("Progressive Sparx Basket Break", 1022, Spyro3ItemCategory.SPARX_POWERUP),
    ("World Key", 1023, Spyro3ItemCategory.WORLD_KEY),
    ("Normal Spyro", 1024, Spyro3ItemCategory.MISC),

    ("Moneybags Unlock - Cloud Spires Bellows", 3000, Spyro3ItemCategory.MONEYBAGS),
    ("Moneybags Unlock - Spooky Swamp Door", 3001, Spyro3ItemCategory.MONEYBAGS),
    ("Moneybags Unlock - Sheila", 3002, Spyro3ItemCategory.MONEYBAGS),
    ("Moneybags Unlock - Icy Peak Nancy Door", 3003, Spyro3ItemCategory.MONEYBAGS),
    ("Moneybags Unlock - Molten Crater Thieves Door", 3004, Spyro3ItemCategory.MONEYBAGS),
    ("Moneybags Unlock - Charmed Ridge Stairs", 3005, Spyro3ItemCategory.MONEYBAGS),
    ("Moneybags Unlock - Sgt. Byrd", 3006, Spyro3ItemCategory.MONEYBAGS),
    ("Moneybags Unlock - Bentley", 3007, Spyro3ItemCategory.MONEYBAGS),
    ("Moneybags Unlock - Desert Ruins Door", 3008, Spyro3ItemCategory.MONEYBAGS),
    ("Moneybags Unlock - Agent 9", 3009, Spyro3ItemCategory.MONEYBAGS),
    ("Moneybags Unlock - Frozen Altars Cat Hockey Door", 3010, Spyro3ItemCategory.MONEYBAGS),
    ("Moneybags Unlock - Crystal Islands Bridge", 3011, Spyro3ItemCategory.MONEYBAGS),

    ("Hint 1", 4000, Spyro3ItemCategory.HINT),
    ("Hint 2", 4001, Spyro3ItemCategory.HINT),
    ("Hint 3", 4002, Spyro3ItemCategory.HINT),
    ("Hint 4", 4003, Spyro3ItemCategory.HINT),
    ("Hint 5", 4004, Spyro3ItemCategory.HINT),
    ("Hint 6", 4005, Spyro3ItemCategory.HINT),
    ("Hint 7", 4006, Spyro3ItemCategory.HINT),
    ("Hint 8", 4007, Spyro3ItemCategory.HINT),
    ("Hint 9", 4008, Spyro3ItemCategory.HINT),
    ("Hint 10", 4009, Spyro3ItemCategory.HINT),
    ("Hint 11", 4010, Spyro3ItemCategory.HINT),
    ("Hint 12", 4011, Spyro3ItemCategory.HINT),
    ("Hint 13", 4012, Spyro3ItemCategory.HINT),

    ("Sunrise Spring 100 Gems", 5000, Spyro3ItemCategory.GEMSANITY),
    ("Sunny Villa 100 Gems", 5001, Spyro3ItemCategory.GEMSANITY),
    ("Cloud Spires 100 Gems", 5002, Spyro3ItemCategory.GEMSANITY),
    ("Molten Crater 100 Gems", 5003, Spyro3ItemCategory.GEMSANITY),
    ("Seashell Shore 100 Gems", 5004, Spyro3ItemCategory.GEMSANITY),
    ("Mushroom Speedway 100 Gems", 5005, Spyro3ItemCategory.GEMSANITY),
    ("Sheila's Alp 100 Gems", 5006, Spyro3ItemCategory.GEMSANITY),
    ("Crawdad Farm 50 Gems", 5007, Spyro3ItemCategory.GEMSANITY),
    ("Midday Gardens 100 Gems", 5008, Spyro3ItemCategory.GEMSANITY),
    ("Icy Peak 100 Gems", 5009, Spyro3ItemCategory.GEMSANITY),
    ("Enchanted Towers 100 Gems", 5010, Spyro3ItemCategory.GEMSANITY),
    ("Spooky Swamp 100 Gems", 5011, Spyro3ItemCategory.GEMSANITY),
    ("Bamboo Terrace 100 Gems", 5012, Spyro3ItemCategory.GEMSANITY),
    ("Country Speedway 100 Gems", 5013, Spyro3ItemCategory.GEMSANITY),
    ("Sgt. Byrd's Base 100 Gems", 5014, Spyro3ItemCategory.GEMSANITY),
    ("Spider Town 50 Gems", 5015, Spyro3ItemCategory.GEMSANITY),
    ("Evening Lake 100 Gems", 5016, Spyro3ItemCategory.GEMSANITY),
    ("Frozen Altars 100 Gems", 5017, Spyro3ItemCategory.GEMSANITY),
    ("Lost Fleet 100 Gems", 5018, Spyro3ItemCategory.GEMSANITY),
    ("Fireworks Factory 100 Gems", 5019, Spyro3ItemCategory.GEMSANITY),
    ("Charmed Ridge 100 Gems", 5020, Spyro3ItemCategory.GEMSANITY),
    ("Honey Speedway 100 Gems", 5021, Spyro3ItemCategory.GEMSANITY),
    ("Bentley's Outpost 100 Gems", 5022, Spyro3ItemCategory.GEMSANITY),
    ("Starfish Reef 50 Gems", 5023, Spyro3ItemCategory.GEMSANITY),
    ("Midnight Mountain 100 Gems", 5024, Spyro3ItemCategory.GEMSANITY),
    ("Crystal Islands 100 Gems", 5025, Spyro3ItemCategory.GEMSANITY),
    ("Desert Ruins 100 Gems", 5026, Spyro3ItemCategory.GEMSANITY),
    ("Haunted Tomb 100 Gems", 5027, Spyro3ItemCategory.GEMSANITY),
    ("Dino Mines 100 Gems", 5028, Spyro3ItemCategory.GEMSANITY),
    ("Harbor Speedway 100 Gems", 5029, Spyro3ItemCategory.GEMSANITY),
    ("Agent 9's Lab 100 Gems", 5030, Spyro3ItemCategory.GEMSANITY),
    ("Bugbot Factory 50 Gems", 5031, Spyro3ItemCategory.GEMSANITY),

    ("Molten Crater Unlock", 6000, Spyro3ItemCategory.LEVEL_KEY),
    ("Seashell Shore Unlock", 6001, Spyro3ItemCategory.LEVEL_KEY),
    ("Mushroom Speedway Unlock", 6002, Spyro3ItemCategory.LEVEL_KEY),
    ("Spooky Swamp Unlock", 6003, Spyro3ItemCategory.LEVEL_KEY),
    ("Bamboo Terrace Unlock", 6004, Spyro3ItemCategory.LEVEL_KEY),
    ("Country Speedway Unlock", 6005, Spyro3ItemCategory.LEVEL_KEY),
    ("Fireworks Factory Unlock", 6006, Spyro3ItemCategory.LEVEL_KEY),
    ("Charmed Ridge Unlock", 6007, Spyro3ItemCategory.LEVEL_KEY),
    ("Honey Speedway Unlock", 6008, Spyro3ItemCategory.LEVEL_KEY),
    ("Haunted Tomb Unlock", 6009, Spyro3ItemCategory.LEVEL_KEY),
    ("Dino Mines Unlock", 6010, Spyro3ItemCategory.LEVEL_KEY),
    ("Harbor Speedway Unlock", 6011, Spyro3ItemCategory.LEVEL_KEY),
    ("Sunny Villa Unlock", 6012, Spyro3ItemCategory.LEVEL_KEY),
    ("Cloud Spires Unlock", 6013, Spyro3ItemCategory.LEVEL_KEY),
    ("Icy Peak Unlock", 6014, Spyro3ItemCategory.LEVEL_KEY),
    ("Enchanted Towers Unlock", 6015, Spyro3ItemCategory.LEVEL_KEY),
    ("Frozen Altars Unlock", 6016, Spyro3ItemCategory.LEVEL_KEY),
    ("Lost Fleet Unlock", 6017, Spyro3ItemCategory.LEVEL_KEY),
    ("Crystal Islands Unlock", 6018, Spyro3ItemCategory.LEVEL_KEY),
    ("Desert Ruins Unlock", 6019, Spyro3ItemCategory.LEVEL_KEY),

    ("Superfly Powerup", 7000, Spyro3ItemCategory.TYPE_POWERUP),
    ("Fireball Powerup", 7001, Spyro3ItemCategory.TYPE_POWERUP),
    ("Invincibility Powerup", 7002, Spyro3ItemCategory.TYPE_POWERUP),
    ("Sunrise Superfly Powerup", 7003, Spyro3ItemCategory.INDIVIDUAL_POWERUP),
    ("Cloud Superfly Powerup", 7004, Spyro3ItemCategory.INDIVIDUAL_POWERUP),
    ("Midday Fireball Powerup", 7005, Spyro3ItemCategory.INDIVIDUAL_POWERUP),
    ("Bamboo Fireball Powerup", 7006, Spyro3ItemCategory.INDIVIDUAL_POWERUP),
    ("Evening Invincibility Powerup", 7007, Spyro3ItemCategory.INDIVIDUAL_POWERUP),
    ("Fireworks Combo Powerup", 7008, Spyro3ItemCategory.INDIVIDUAL_POWERUP),
    ("Fleet Invincibility Powerup", 7009, Spyro3ItemCategory.INDIVIDUAL_POWERUP),
    ("Charmed Fireball Powerup", 7010, Spyro3ItemCategory.INDIVIDUAL_POWERUP),
    ("Crystal Superfly Powerup", 7011, Spyro3ItemCategory.INDIVIDUAL_POWERUP),
    ("Super Bonus Round Combo Powerup", 7012, Spyro3ItemCategory.INDIVIDUAL_POWERUP),

    ("Glitched Item", 9000, Spyro3ItemCategory.UT_ITEM)
]]

item_descriptions = {}

item_dictionary = {item_data.name: item_data for item_data in _all_items}


def BuildItemPool(world, count, preplaced_eggs, options, locked_levels):
    item_pool = []
    included_itemcount = 0
    multiworld = world.multiworld

    if options.guaranteed_items.value:
        for item_name in options.guaranteed_items.value:
            item = item_dictionary[item_name]
            item_pool.append(item)
            included_itemcount = included_itemcount + 1
    remaining_count = count - included_itemcount
    eggs_to_place = 150
    if world.generation_options["goal"] == GoalOptions.EGG_HUNT:
        eggs_to_place = math.ceil(world.generation_options["egg_count"] * (1.0 + world.generation_options["percent_extra_eggs"] / 100.0))
        # Game caps egg count at 150 and can encounter issues above this number.
        if eggs_to_place > 150:
            eggs_to_place = 150
    eggs_to_place = eggs_to_place - preplaced_eggs
    # Portals with egg requirements can't be set to require 0, so start with 1 egg to ensure level unlocks
    # work correctly when unlocks are not vanilla or keys and eggs.
    if world.generation_options["level_lock_option"] not in [LevelLockOptions.VANILLA]:
        multiworld.push_precollected(world.create_item("Egg"))
        eggs_to_place = eggs_to_place - 1
    for i in range(eggs_to_place):
        item_pool.append(item_dictionary["Egg"])
    remaining_count = remaining_count - eggs_to_place

    if world.generation_options["enable_gemsanity"] in [GemsanityOptions.PARTIAL, GemsanityOptions.FULL_BUNDLES]:
        for i in range(4):
            item_pool.append(item_dictionary["Crawdad Farm 50 Gems"])
            item_pool.append(item_dictionary["Spider Town 50 Gems"])
            item_pool.append(item_dictionary["Starfish Reef 50 Gems"])
            if world.generation_options["goal"] != GoalOptions.EGG_HUNT or world.generation_options["egg_count"] > world.generation_options["sorceress_door_requirement"]:
                item_pool.append(item_dictionary["Bugbot Factory 50 Gems"])
            else:
                remaining_count = remaining_count + 1
        for i in range(4):
            item_pool.append(item_dictionary["Sunrise Spring 100 Gems"])
            item_pool.append(item_dictionary["Sunny Villa 100 Gems"])
            item_pool.append(item_dictionary["Cloud Spires 100 Gems"])
            item_pool.append(item_dictionary["Molten Crater 100 Gems"])
            item_pool.append(item_dictionary["Seashell Shore 100 Gems"])
            item_pool.append(item_dictionary["Mushroom Speedway 100 Gems"])
            item_pool.append(item_dictionary["Sheila's Alp 100 Gems"])
            item_pool.append(item_dictionary["Midday Gardens 100 Gems"])
            item_pool.append(item_dictionary["Country Speedway 100 Gems"])
            item_pool.append(item_dictionary["Evening Lake 100 Gems"])
            item_pool.append(item_dictionary["Honey Speedway 100 Gems"])
            item_pool.append(item_dictionary["Midnight Mountain 100 Gems"])
            item_pool.append(item_dictionary["Harbor Speedway 100 Gems"])
        for i in range(5):
            item_pool.append(item_dictionary["Icy Peak 100 Gems"])
            item_pool.append(item_dictionary["Enchanted Towers 100 Gems"])
            item_pool.append(item_dictionary["Spooky Swamp 100 Gems"])
            item_pool.append(item_dictionary["Bamboo Terrace 100 Gems"])
            item_pool.append(item_dictionary["Sgt. Byrd's Base 100 Gems"])
        for i in range(6):
            item_pool.append(item_dictionary["Frozen Altars 100 Gems"])
            item_pool.append(item_dictionary["Lost Fleet 100 Gems"])
            item_pool.append(item_dictionary["Fireworks Factory 100 Gems"])
            item_pool.append(item_dictionary["Charmed Ridge 100 Gems"])
            item_pool.append(item_dictionary["Bentley's Outpost 100 Gems"])
        for i in range(7):
            item_pool.append(item_dictionary["Crystal Islands 100 Gems"])
            item_pool.append(item_dictionary["Desert Ruins 100 Gems"])
            item_pool.append(item_dictionary["Haunted Tomb 100 Gems"])
            item_pool.append(item_dictionary["Dino Mines 100 Gems"])
            item_pool.append(item_dictionary["Agent 9's Lab 100 Gems"])
        remaining_count -= 158

    if world.generation_options["moneybags_settings"] in [MoneybagsOptions.COMPANIONSANITY, MoneybagsOptions.MONEYBAGSSANITY]:
        item_pool.append(item_dictionary["Moneybags Unlock - Sheila"])
        item_pool.append(item_dictionary["Moneybags Unlock - Sgt. Byrd"])
        item_pool.append(item_dictionary["Moneybags Unlock - Bentley"])
        item_pool.append(item_dictionary["Moneybags Unlock - Agent 9"])
        remaining_count = remaining_count - 4
    if world.generation_options["moneybags_settings"] == MoneybagsOptions.MONEYBAGSSANITY:
        item_pool.append(item_dictionary["Moneybags Unlock - Cloud Spires Bellows"])
        item_pool.append(item_dictionary["Moneybags Unlock - Spooky Swamp Door"])
        item_pool.append(item_dictionary["Moneybags Unlock - Icy Peak Nancy Door"])
        item_pool.append(item_dictionary["Moneybags Unlock - Molten Crater Thieves Door"])
        item_pool.append(item_dictionary["Moneybags Unlock - Charmed Ridge Stairs"])
        item_pool.append(item_dictionary["Moneybags Unlock - Desert Ruins Door"])
        item_pool.append(item_dictionary["Moneybags Unlock - Frozen Altars Cat Hockey Door"])
        item_pool.append(item_dictionary["Moneybags Unlock - Crystal Islands Bridge"])
        remaining_count = remaining_count - 8

    if world.generation_options["enable_progressive_sparx_health"] in [SparxUpgradeOptions.BLUE, SparxUpgradeOptions.GREEN, SparxUpgradeOptions.SPARXLESS]:
        item_pool.append(item_dictionary["Progressive Sparx Health Upgrade"])
        remaining_count = remaining_count - 1
    if world.generation_options["enable_progressive_sparx_health"] in [SparxUpgradeOptions.GREEN, SparxUpgradeOptions.SPARXLESS]:
        item_pool.append(item_dictionary["Progressive Sparx Health Upgrade"])
        remaining_count = remaining_count - 1
    if world.generation_options["enable_progressive_sparx_health"] in [SparxUpgradeOptions.SPARXLESS]:
        item_pool.append(item_dictionary["Progressive Sparx Health Upgrade"])
        remaining_count = remaining_count - 1

    if world.generation_options["sparx_power_settings"]:
        item_pool.append(item_dictionary["Increased Sparx Range"])
        if world.generation_options["enable_progressive_sparx_logic"] and world.generation_options["require_sparx_for_max_gems"] == SparxForGemsOptions.SPARX_FINDER:
            multiworld.push_precollected(world.create_item("Sparx Gem Finder"))
            remaining_count = remaining_count + 1
        else:
            item_pool.append(item_dictionary["Sparx Gem Finder"])
        item_pool.append(item_dictionary["Extra Hit Point"])
        item_pool.append(item_dictionary["Progressive Sparx Basket Break"])
        item_pool.append(item_dictionary["Progressive Sparx Basket Break"])
        remaining_count = remaining_count - 5

    if world.generation_options["level_lock_option"] == LevelLockOptions.KEYS:
        possible_locked_levels = [
            "Sunny Villa", "Cloud Spires", "Molten Crater", "Seashell Shore", "Mushroom Speedway",
            "Icy Peak", "Enchanted Towers", "Spooky Swamp", "Bamboo Terrace", "Country Speedway",
            "Frozen Altars", "Lost Fleet", "Fireworks Factory", "Charmed Ridge", "Honey Speedway",
            "Crystal Islands", "Desert Ruins", "Haunted Tomb", "Dino Mines", "Harbor Speedway"
        ]

        for level in possible_locked_levels:
            if level in locked_levels:
                item_pool.append((item_dictionary[f"{level} Unlock"]))
                remaining_count = remaining_count - 1
            else:
                multiworld.push_precollected(world.create_item(f"{level} Unlock"))

    if world.generation_options["powerup_lock_settings"] == PowerupLockOptions.TYPE:
        item_pool.append(item_dictionary["Superfly Powerup"])
        item_pool.append(item_dictionary["Fireball Powerup"])
        item_pool.append(item_dictionary["Invincibility Powerup"])
        remaining_count = remaining_count - 3
    elif world.generation_options["powerup_lock_settings"] == PowerupLockOptions.INDIVIDUAL:
        item_pool.append(item_dictionary["Sunrise Superfly Powerup"])
        item_pool.append(item_dictionary["Cloud Superfly Powerup"])
        item_pool.append(item_dictionary["Midday Fireball Powerup"])
        item_pool.append(item_dictionary["Bamboo Fireball Powerup"])
        item_pool.append(item_dictionary["Evening Invincibility Powerup"])
        item_pool.append(item_dictionary["Fireworks Combo Powerup"])
        item_pool.append(item_dictionary["Fleet Invincibility Powerup"])
        item_pool.append(item_dictionary["Charmed Fireball Powerup"])
        item_pool.append(item_dictionary["Crystal Superfly Powerup"])
        item_pool.append(item_dictionary["Super Bonus Round Combo Powerup"])
        remaining_count = remaining_count - 10

    if world.generation_options["enable_world_keys"]:
        for i in range(3):
            item_pool.append(item_dictionary["World Key"])
        remaining_count = remaining_count - 3

    if remaining_count < 0:
        raise OptionError(f"The options you have selected require at least {remaining_count * -1} more checks to be enabled.")

    # Build a weighted list of allowed filler items.
    # Make changing Spyro's color in general the same weight as other items.
    allowed_misc_items = []
    allowed_trap_items = []

    for item in _all_items:
        if item.name == 'Extra Life' and options.enable_filler_extra_lives:
            for i in range(0, 6):
                allowed_misc_items.append(item)
        elif item.name.startswith('Invincibility (') and options.enable_filler_invincibility:
            for i in range(0, 3):
                allowed_misc_items.append(item)
        elif item.name.startswith('Turn Spyro ') and options.enable_filler_color_change:
            allowed_misc_items.append(item)
        elif (item.name == 'Big Head Mode' or item.name == 'Flat Spyro Mode') and options.enable_filler_big_head_mode:
            for i in range(0, 3):
                allowed_misc_items.append(item)
        elif item.name == '(Over)heal Sparx' and options.enable_filler_heal_sparx:
            for i in range(0, 6):
                allowed_misc_items.append(item)
        elif item.name == 'Damage Sparx Trap' and options.enable_trap_damage_sparx:
            allowed_trap_items.append(item)
        elif item.name == 'Sparxless Trap' and options.enable_trap_sparxless:
            allowed_trap_items.append(item)
        elif item.name == "Normal Spyro" and (options.enable_filler_color_change or options.enable_filler_big_head_mode or len(allowed_misc_items) == 0):
            for i in range(0, 4):
                allowed_misc_items.append(item)

    if remaining_count > 0 and world.generation_options["trap_filler_percent"] > 0 and len(allowed_trap_items) == 0:
        # Likely user error, but causes problems during UT generation with random settings.
        world.generation_options["trap_filler_percent"] = 0

    # Get the correct blend of traps and filler items.
    for i in range(remaining_count):
        if multiworld.random.random() * 100 < world.generation_options["trap_filler_percent"]:
            itemList = [item for item in allowed_trap_items]
        else:
            itemList = [item for item in allowed_misc_items]
        item = multiworld.random.choice(itemList)
        item_pool.append(item)

    multiworld.random.shuffle(item_pool)
    return item_pool

item_name_groups = {"Moneybags Unlocks": set(), "Level Unlocks": set(), "Gems": set(), "Powerups": set()}
for item in item_dictionary.keys():
    if "Moneybags Unlock" in item:
        item_name_groups["Moneybags Unlocks"].add(item)
    if item.endswith(" Unlock"):
        item_name_groups["Level Unlocks"].add(item)
    if item.endswith(" Gems"):
        item_name_groups["Gems"].add(item)
    if item.endswith(" Powerup"):
        item_name_groups["Powerups"].add(item)
