from __future__ import annotations

import logging
from typing import List, TYPE_CHECKING

from BaseClasses import Item, ItemClassification, Location

from .ALttPDoorRandomizer.BaseClasses import LocationType
from .ALttPDoorRandomizer.Items import ItemFactory, item_table
from .Regions import get_event_locations

if TYPE_CHECKING:
    from .World import ALttPRWorld


logger = logging.getLogger("alttpr")

# TODO: This feels inefficient to run every time, there must be a way to store the result without copy/pasting code from Door Rando
item_name_to_id = {}
for item_name, item_data in item_table.items():
    id = item_data[3]
    if id == 999 or type(id) is not int or id == 0x6A:  # 0x6A is the Triforce
        id = None
    item_name_to_id[item_name] = id

# TODO: Pretty sure this can be deleted? Maybe?
default_items_dict = {
    "bow": 0,
    "progressivebow": 2,
    "boomerang": 1,
    "redmerang": 1,
    "hookshot": 1,
    "mushroom": 1,
    "powder": 1,
    "firerod": 1,
    "icerod": 1,
    "bombos": 1,
    "ether": 1,
    "quake": 1,
    "lamp": 1,
    "hammer": 1,
    "shovel": 1,
    "flute": 1,
    "bugnet": 1,
    "book": 1,
    "bottle": 4,
    "somaria": 1,
    "byrna": 1,
    "cape": 1,
    "mirror": 1,
    "boots": 1,
    "powerglove": 0,
    "titansmitt": 0,
    "progressiveglove": 2,
    "flippers": 1,
    "pearl": 1,
    "heartpiece": 24,
    "heartcontainer": 10,
    "sancheart": 1,
    "sword1": 0,
    "sword2": 0,
    "sword3": 0,
    "sword4": 0,
    "progressivesword": 4,
    "shield1": 0,
    "shield2": 0,
    "shield3": 0,
    "progressiveshield": 3,
    "mail2": 0,
    "mail3": 0,
    "progressivemail": 2,
    "halfmagic": 1,
    "quartermagic": 0,
    "bombsplus5": 0,
    "bombsplus10": 0,
    "arrowsplus5": 0,
    "arrowsplus10": 0,
    "arrow1": 1,
    "arrow10": 12,
    "bomb1": 0,
    "bomb3": 16,
    "bomb10": 1,
    "rupee1": 2,
    "rupee5": 4,
    "rupee20": 28,
    "rupee50": 7,
    "rupee100": 1,
    "rupee300": 5,
    "blueclock": 0,
    "greenclock": 0,
    "redclock": 0,
    "silversupgrade": 0,
    "generickeys": 0,
    "triforcepieces": 0,
    "triforcepiecesgoal": 0,
    "triforce": 0,
    "rupoor": 0,
    "rupoorcost": 10
}

# Some of the internal Door Randomizer names for items are not the community standard names for items (e.g. Ocarina instead of Flute),
# we should try to keep names as standardized as possible to avoid confusion.
# TODO: Better name.
# TODO: Should have two separate dicts/functions, one for dr_to_ap and one for ap_to_dr
dr_ap_different_names = {
    "Cape": "Magic Cape",
    "Magic Cape": "Cape",
    "Progressive Armor": "Progressive Mail",
    "Progressive Mail": "Progressive Armor",
}

progressive_items = [
    "Big Key (Escape)",
    "Big Key (Eastern Palace)",
    "Big Key (Desert Palace)",
    "Big Key (Tower of Hera)",
    "Big Key (Agahnims Tower)",
    "Big Key (Palace of Darkness)",
    "Big Key (Swamp Palace)",
    "Big Key (Skull Woods)",
    "Big Key (Thieves Town)",
    "Big Key (Ice Palace)",
    "Big Key (Misery Mire)",
    "Big Key (Turtle Rock)",
    "Big Key (Ganons Tower)",
    "Blue Boomerang",
    "Blue Pendant",
    "Bomb Upgrade (+10)",
    "Bombos",
    "Book of Mudora",
    "Bottle",
    "Bottle (Red Potion)",
    "Bottle (Green Potion)",
    "Bottle (Blue Potion)",
    "Bottle (Fairy)",
    "Bottle (Bee)",
    "Bottle (Good Bee)",
    "Cane of Byrna",
    "Cane of Somaria",
    "Crystal 1",
    "Crystal 2",
    "Crystal 3",
    "Crystal 4",
    "Crystal 5",
    "Crystal 6",
    "Crystal 7",
    "Ether",
    "Fire Rod",
    "Flippers",
    "Green Pendant",
    "Hammer",
    "Hookshot",
    "Ice Rod",
    "Lamp",
    "Magic Cape",
    "Magic Mirror",
    "Magic Powder",
    "Magic Upgrade (1/2)",
    "Moon Pearl",
    "Mushroom",
    "Ocarina",
    "Ocarina (Activated)",
    "Pegasus Boots",
    "Progressive Bow",
    "Progressive Glove",
    "Progressive Shield",
    "Progressive Sword",
    "Quake",
    "Red Boomerang",
    "Red Pendant",
    "Shovel",
    "Small Key (Escape)",
    "Small Key (Eastern Palace)",
    "Small Key (Desert Palace)",
    "Small Key (Tower of Hera)",
    "Small Key (Agahnims Tower)",
    "Small Key (Palace of Darkness)",
    "Small Key (Swamp Palace)",
    "Small Key (Skull Woods)",
    "Small Key (Thieves Town)",
    "Small Key (Ice Palace)",
    "Small Key (Misery Mire)",
    "Small Key (Turtle Rock)",
    "Small Key (Ganons Tower)",
    "Triforce Piece",
    "Green Clock",  # Placeholder for progressive AP items
]

useful_items = [
    "Arrow Upgrade (+5)",
    "Blue Potion",
    "Bomb Upgrade (+5)",
    "Boss Heart Container",
    "Green Potion",
    "Progressive Mail",
    "Red Potion",
    "Rupees (300)",
    "Sanctuary Heart Container",
    "Blue Clock",  # Placeholder for useful AP items
]

filler_items = [
    "Arrows (5)",
    "Arrows (10)",
    "Bee",
    "Big Magic",
    "Blue Shield",
    "Bombs (3)",
    "Bombs (10)",
    "Bug Catching Net",
    "Chicken",
    "Compass (Escape)",
    "Compass (Eastern Palace)",
    "Compass (Desert Palace)",
    "Compass (Tower of Hera)",
    "Compass (Agahnims Tower)",
    "Compass (Palace of Darkness)",
    "Compass (Swamp Palace)",
    "Compass (Skull Woods)",
    "Compass (Thieves Town)",
    "Compass (Ice Palace)",
    "Compass (Misery Mire)",
    "Compass (Turtle Rock)",
    "Compass (Ganons Tower)",
    "Fairy",
    "Map (Escape)",
    "Map (Eastern Palace)",
    "Map (Desert Palace)",
    "Map (Tower of Hera)",
    "Map (Agahnims Tower)",
    "Map (Palace of Darkness)",
    "Map (Swamp Palace)",
    "Map (Skull Woods)",
    "Map (Thieves Town)",
    "Map (Ice Palace)",
    "Map (Misery Mire)",
    "Map (Turtle Rock)",
    "Map (Ganons Tower)",
    "Nothing",
    "Piece of Heart",
    "Red Clock",  # Placeholder for filler AP items
    "Red Shield",
    "Rupee (1)",
    "Rupees (5)",
    "Rupees (20)",
    "Rupees (50)",
    "Rupees (100)",
    "Single Arrow",
    "Single Bomb",
    "Small Heart",
    "Small Magic",
]


class ALttPRItem(Item):
    game = "The Legend of Zelda: A Link to the Past"


def get_dungeon_items(world: ALttPRWorld) -> List[str]:
    dungeon_items = []
    if not world.options.map_shuffle.value:
        dungeon_items.extend([item for item in filler_items if item.startswith("Map")])
    if not world.options.compass_shuffle.value:
        dungeon_items.extend([item for item in filler_items if item.startswith("Compass")])

    if not (world.door_rando_world.keyshuffle == "wild" and world.door_rando_world.dropshuffle[1] != "none"):
        dungeon_items.extend([item for item in progressive_items if item.startswith("Small Key")])

    if not world.options.big_key_shuffle.value:
        dungeon_items.extend([item for item in progressive_items if item.startswith("Big Key")])
    elif world.door_rando_world.dropshuffle[1] == "none":
        # Big keys are shuffled, except for the HC BK, or the BK for the dungeon Zelda's cell is in, if door rando
        dungeon_items.append(world.door_rando_world.get_location("Hyrule Castle - Big Key Drop", 1).item.name)

    return dungeon_items


def get_random_filler_item_name(world: ALttPRWorld) -> str:
    raise NotImplementedError("get_random_filler_item_name is not implemented yet")


def get_classification(name: str, progressive_bug_net: bool) -> ItemClassification:
    if name in progressive_items:
        classification = ItemClassification.progression
    elif name in useful_items:
        classification = ItemClassification.useful
    elif name in filler_items:
        if progressive_bug_net and name == "Bug Catching Net":
            # Bug net can be progression in doors to kill Agahnim
            classification = ItemClassification.progression
        else:
            classification = ItemClassification.filler
    else:
        logger.error(f"Item {name} not found in any item list, cannot determine classification.")
        raise Exception()


    return classification


def create_item(world: ALttPRWorld, name: str, classification: ItemClassification) -> ALttPRItem:
    door_rando_item = ItemFactory(name, 1)
    item_name_to_id[name] = door_rando_item.code
    new_name = dr_ap_different_names[name] if name in dr_ap_different_names else name
    return ALttPRItem(new_name, classification, door_rando_item.code, world.player)


def create_all_items(world: ALttPRWorld) -> None:
    # If we're playing Standard mode with keysanity, we need to manually place the escape keys to prevent
    # getting BK'd in the escape sequence. This key is placed later in the pre_fill() stage of generation.
    dr_itempool = world.door_rando_world.itempool.copy()
    if world.options.world_mode == "standard" and world.options.door_shuffle == "vanilla":
        if world.door_rando_world.keyshuffle[1] == "wild":
            escape_keys = [item for item in dr_itempool if item.name == "Small Key (Escape)"]
            for key in escape_keys:
                dr_itempool.remove(key)
        if world.options.big_key_shuffle.value and world.door_rando_world.dropshuffle[1] != "none":
            escape_keys = [item for item in dr_itempool if item.name == "Big Key (Escape)"]
            if len(escape_keys) > 0:
                dr_itempool.remove(escape_keys[0])

    # Remove bomb and arrow capacity upgrades from the item pool for shopsanity. They will be added
    # to a random shop in the pre_fill() stage of generation.
    if world.options.shopsanity:
        upgrades = [item for item in dr_itempool if "Arrow Upgrade" in item.name or (not world.options.bombless_start and "Bomb Upgrade" in item.name)]
        for upgrade in upgrades:
            dr_itempool.remove(upgrade)

    # Itempool will not include dungeon items unless keysanity is enabled.
    # Key drop keys are also not in the item pool unless key drop in enabled.
    itempool = []
    for item in dr_itempool:
        ap_item_name = item.name if item.name not in dr_ap_different_names else dr_ap_different_names[item.name]
        code = item.code
        classification = get_classification(ap_item_name, world.options.door_shuffle != "vanilla" or world.options.boss_shuffle != "vanilla")

        if world.options.shopsanity.value and (ap_item_name == "Bee" or (ap_item_name == "Red Potion" and not item.priority)):
            # Having bees and potions as randomized items is kinda wonky. Usually when you receive them they
            # show up as rupees, and these items (currently) only appear in Shopsanity, so let's just turn them into rupees.
            # One red potion should always be available for purchase in shops, and it will have True priority.
            ap_item_name = "Rupees (50)"
            classification = ItemClassification.filler
            code = ItemFactory(ap_item_name, 1).code

        ap_item = ALttPRItem(ap_item_name, classification, code, world.player)
        itempool.append(ap_item)

    world.multiworld.itempool += itempool


def place_pre_fill_items(world: ALttPRWorld) -> None:
    # Place all items that cannot be randomized into any world, such as pendants/crystals, dungeon items, and special events like killing Agahnim
    event_locations = get_event_locations(world)
    for event_location_name, event_item_name in event_locations.items():
        ap_item = ALttPRItem(event_item_name, ItemClassification.progression, None, world.player)
        event_location = world.multiworld.get_location(event_location_name, world.player)
        event_location.place_locked_item(ap_item)

    if not world.options.prize_shuffle:
        prize_locations = [location for location in world.multiworld.get_unfilled_locations(world.player) if " - Prize" in location.name]
        for prize_location in prize_locations:
            dr_prize_location = world.door_rando_world.get_location(prize_location.name, 1)
            ap_item = ALttPRItem(dr_prize_location.item.name, ItemClassification.progression, None, world.player)
            target_location = world.multiworld.get_location(prize_location.name, world.player)
            target_location.place_locked_item(ap_item)
            target_location.address = None

    for dungeon_item in get_dungeon_items(world):
        dr_item_name = dungeon_item if dungeon_item not in dr_ap_different_names else dr_ap_different_names[dungeon_item]

        # All dungeon items should already be placed in a location. If keysanity is enabled but not key drop shuffle, then
        # small keys dropped by pots/enemies will already be placed, but other small keys won't.
        item_locations = world.door_rando_world.find_items(dr_item_name, 1)
        if not item_locations:
                continue

        for location in item_locations:
            dr_dungeon_item = location.item
            if dr_dungeon_item.smallkey or dr_dungeon_item.bigkey:
                classification = ItemClassification.progression
            else:
                classification = ItemClassification.filler
            code = dr_dungeon_item.code if not world.is_excluded_key_drop_location(location) else None
            ap_item = ALttPRItem(dungeon_item, classification, code, world.player)
            target_location = world.multiworld.get_location(location.name, world.player)
            target_location.place_locked_item(ap_item)

    # Standard mode requires a weapon and enough keys to be available early
    if world.options.world_mode == "standard":
        # In Standard mode, Link's Uncle will always have a weapon which was not added to the multiworld itempool,
        # unless the player starts with a sword or hammer.
        uncle_item = world.door_rando_world.get_location("Link's Uncle", 1).item
        if uncle_item is not None:
            ap_item = ALttPRItem(uncle_item.name, ItemClassification.progression, uncle_item.code, world.player)
            links_uncle_location = world.multiworld.get_location("Link's Uncle", world.player)
            links_uncle_location.place_locked_item(ap_item)

        # If keysanity is enabled, the keys for the escape sequence should still be sphere 0,
        # to prevent the player from being near-instantly BK'd.
        if world.door_rando_world.keyshuffle[1] == "wild":
            if world.options.door_shuffle != "vanilla":
                world.options.local_items.value.add("Small Key (Escape)")
            elif world.door_rando_world.dropshuffle[1] != "none":
                key_locations = ["Secret Passage", "Hyrule Castle - Map Chest", "Hyrule Castle - Map Guard Key Drop"]
                key_location = place_escape_key(key_locations, world, "Small")
                key_locations.remove(key_location)

                key_locations.extend(["Hyrule Castle - Boomerang Chest", "Hyrule Castle - Boomerang Guard Key Drop"])
                key_location = place_escape_key(key_locations, world, "Small")
                key_locations.remove(key_location)

                key_locations.extend(["Hyrule Castle - Big Key Drop", "Hyrule Castle - Zelda's Chest", "Sewers - Dark Cross"])
                key_location = place_escape_key(key_locations, world, "Small")
                key_locations.remove(key_location)

                key_locations.append("Hyrule Castle - Key Rat Key Drop")
                place_escape_key(key_locations, world, "Small")
            else:
                small_key_locations = ["Secret Passage", "Hyrule Castle - Map Chest",
                                    "Hyrule Castle - Boomerang Chest", "Hyrule Castle - Zelda's Chest", "Sewers - Dark Cross"]
                place_escape_key(small_key_locations, world, "Small")

        if world.options.big_key_shuffle and world.door_rando_world.dropshuffle[1] != "none":
            if world.options.door_shuffle != "vanilla":
                # No clue what the valid locations would be, good luck AP
                world.options.local_items.value.add("Big Key (Escape)")
            else:
                big_key_locations = ["Secret Passage", "Hyrule Castle - Map Chest", "Hyrule Castle - Map Guard Key Drop",
                                     "Hyrule Castle - Boomerang Chest", "Hyrule Castle - Boomerang Guard Key Drop", "Hyrule Castle - Big Key Drop"]
                place_escape_key(big_key_locations, world, "Big")

    # If Shopsanity is enabled, there should be one each of Red/Green/Blue Potions that can be repeatedly purchased
    if world.options.shopsanity:
        shop_locations = [location for location in world.door_rando_world.get_locations() if location.type == LocationType.Shop]
        for shop_item in ["Red Potion", "Green Potion", "Blue Potion"]:
            location = world.door_rando_world.find_items(shop_item, 1)[0]
            potion = ALttPRItem(shop_item, ItemClassification.useful, ItemFactory(shop_item, 1).code, world.player)
            world.multiworld.get_location(location.name, world.player).place_locked_item(potion)
            shop_locations.remove(location)

        # Set the arrow and bomb capacity upgrades to be in a shop.
        # The randomizer does this by moving items around after placing everything, which isn't an option for us.
        # The bomb upgrade will not exist if starting without bombs.
        world.random.shuffle(shop_locations)
        upgrades = [item for item in world.door_rando_world.itempool if item.name == "Arrow Upgrade (+5)" or item.name == "Bomb Upgrade (+5)"]
        for upgrade in upgrades:
            location = shop_locations.pop()
            if not location.item:  # Should always be true
                new_item = ALttPRItem(upgrade.name, ItemClassification.useful, ItemFactory(upgrade.name, 1).code, world.player)
                world.multiworld.get_location(location.name, world.player).place_locked_item(new_item)


def place_escape_key(possible_locations: List[str], world: ALttPRWorld, key_size: str) -> str:
    world.random.shuffle(possible_locations)
    for key_location_name in possible_locations:
        key_location = world.multiworld.get_location(key_location_name, world.player)
        if key_location.item is None:
            key_item = ALttPRItem(f"{key_size} Key (Escape)", ItemClassification.progression, ItemFactory(f"{key_size} Key (Escape)", 0).code, world.player)
            key_location.place_locked_item(key_item)
            return key_location_name

    # Should never reach this
    raise Exception("ALttPR: Could not place escape small key, no empty locations found.")



def place_junk_items_in_pots(progitempool: List[Item], usefulitempool: List[Item], filleritempool: List[Item], fill_locations: List[Location], world) -> None:
    # There is a technical limit of 256 multiworld items under pots
    local_pot_item_names = [
        "Big Magic",
        "Blue Shield",
        "Chicken",
        "Fairy",
        "Red Shield",
        "Rupee (1)",
        "Rupees (5)",
        "Single Bomb",
        "Small Heart",
        "Small Magic",
        "Triforce Piece",
    ]

    # These items look wonky anywhere other than under a pot
    priority_pot_items = [
        "Arrows (5)",
        "Nothing",
    ]

    local_pot_items = ([item for item in filleritempool if item.player == world.player and item.name in local_pot_item_names])
    num_filler_items = len(local_pot_items)
    local_pot_items.extend([item for item in progitempool if item.player == world.player and item.name in local_pot_item_names])
    local_pot_items.sort()
    world.random.shuffle(local_pot_items)
    local_pot_items.extend([item for item in filleritempool if item.name in priority_pot_items])
    local_pot_items.reverse()  # Prioritize Nothing and Arrows (5) in pots
    local_pot_items = [item for item in local_pot_items if item.name not in world.options.non_local_items]
    pot_locations = [location for location in fill_locations if location.player == world.player and "Pot" in location.name]
    num_filler_items_placed = 0

    if len(pot_locations) > 256:
        pot_locations.sort()
        world.random.shuffle(pot_locations)
        local_pot_locations = pot_locations[256:]
        assert len(local_pot_items) >= len(local_pot_locations), "Not enough local junk items to place in pots"

        # TODO: A smarter algorithm could distribute items better, so that e.g. two Zelda players with lottery
        # would always have 256 pots filled with the other player's items
        for i in range(0, len(local_pot_locations)):
            item = local_pot_items[i]
            location = local_pot_locations[i]
            location.place_locked_item(item)
            fill_locations.remove(location)
            if item.name == "Triforce Piece":
                # All items with the same name are considered equal, so it can't differentiate between
                # a Triforce Piece placed in a location vs. one not placed yet. Removing the wrong Triforce Piece
                # screws up the item pool.
                for i in range(0, len(progitempool)):
                    if progitempool[i] == item and progitempool[i].location:
                        progitempool.pop(i)
                        break
            else:
                filleritempool.remove(item)
                num_filler_items_placed = num_filler_items_placed + 1

    local_fill_percent = world.options.local_fill_percent
    if local_fill_percent > 0:
        num_filler_items_to_place = num_filler_items * (local_fill_percent / 100)
        junk_items = ([item for item in filleritempool if item.player == world.player and
                       (item.name in local_pot_item_names or item.name in priority_pot_items) and
                       item.name not in world.options.non_local_items])
        junk_items.sort()
        world.random.shuffle(junk_items)

        locations = [location for location in fill_locations if location.player == world.player]
        locations.sort()
        world.random.shuffle(locations)

        while num_filler_items_to_place > num_filler_items_placed and junk_items and locations:
            item = junk_items.pop(0)
            location = locations.pop(0)
            location.place_locked_item(item)
            filleritempool.remove(item)
            fill_locations.remove(location)
            num_filler_items_placed = num_filler_items_placed + 1
