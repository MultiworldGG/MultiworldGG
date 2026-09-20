from .Constants import *


HINT_DATA = {

    # Shops
    "Island Shop Power Gem": {
        "scenes": [0xB11, 0xC0E, 0x1014],
        "has_slot_data": ["shop_hints"]
    },
    "Island Shop Quiver": {
        "scenes": [0xB11, 0xC0E, 0x1014],
        "has_slot_data": ["shop_hints"],
        "any_has_items": ["Bow (Progressive)", "Bow"]
    },
    "Island Shop Bombchu Bag Plus": {
        "locations": ["Island Shop Bombchu Bag", "Island Shop Heart Container"],
        "scenes": [0xB11, 0xC0E, 0x1014],
        "has_slot_data": ["shop_hints"],
        "has_items": ["Bow (Progressive)", "Bombchus (Progressive)"]
    },
    "Island Shop Bombchu Bag Plus alt": {
        "locations": ["Island Shop Bombchu Bag", "Island Shop Heart Container"],
        "scenes": [0xB11, 0xC0E, 0x1014],
        "has_slot_data": ["shop_hints"],
        "has_items": ["Bow", "Bombchu Bag"]
    },
    "Mercay Shop": {
        "locations": ["Mercay Shop Shield", "Mercay Shop Treasure",
                      "Mercay Shop Red Potion"],
        "scenes": [0xB11],
        "has_slot_data": ["shop_hints"]
    },
    "Mercay Shop Purp1": {
        "locations": ["Mercay Shop Purple Potion"],
        "scenes": [0xB11],
        "has_items": ["Shield"],
        "has_slot_data": ["shop_hints", "shield_in_pool", ("shopsanity", "potions")]
    },
    "Mercay Shop Purp2": {
        "locations": ["Mercay Shop Purple Potion"],
        "scenes": [0xB11],
        "has_slot_data": ["shop_hints", ["shield_in_pool", 0], ("shopsanity", "potions")]
    },
    "Mercay Shop Bomb Refill": {
        "scenes": [0xB11],
        "has_slot_data": ["shop_hints"],
        "any_has_items": ["Bombs (Progressive)", "Bomb Bag"]
    },
    "Molida Shop": {
        "locations": ["Molida Shop Red Potion", "Molida Shop Shield"],
        "scenes": [0xC0E],
        "has_slot_data": ["shop_hints"]
    },
    "Molida Shop Purp1": {
        "locations": ["Molida Shop Purple Potion"],
        "scenes": [0xC0E],
        "has_items": ["Shield"],
        "has_slot_data": ["shop_hints", "shield_in_pool", ("shopsanity", "potions")]
    },
    "Molida Shop Purp2": {
        "locations": ["Molida Shop Purple Potion"],
        "scenes": [0xC0E],
        "has_slot_data": ["shop_hints", ["shield_in_pool", 0], ("shopsanity", "potions")]
    },
    "Molida Shop Bomb Refill": {
        "scenes": [0xC0E],
        "has_slot_data": ["shop_hints"],
        "any_has_items": ["Bombs (Progressive)", "Bomb Bag"]
    },
    "Molida Shop Arrow Refill": {
        "scenes": [0xC0E],
        "has_slot_data": ["shop_hints"],
        "any_has_items": ["Bow (Progressive)", "Bow"]
    },
    "Goron Shop": {
        "locations": ["Goron Shop Shield", "Goron Shop Yellow Potion"],
        "scenes": [0x1014],
        "has_slot_data": ["shop_hints"]
    },
    "Goron Shop Purp1": {
        "locations": ["Goron Shop Purple Potion"],
        "scenes": [0x1014],
        "has_items": ["Shield"],
        "has_slot_data": ["shop_hints", "shield_in_pool", ("shopsanity", "potions")]
    },
    "Goron Shop Purp2": {
        "locations": ["Goron Shop Purple Potion"],
        "scenes": [0x1014],
        "has_slot_data": ["shop_hints", ["shield_in_pool", 0], ("shopsanity", "potions")]
    },
    "Goron Shop Arrow Refill": {
        "scenes": [0x1014],
        "has_slot_data": ["shop_hints"],
        "any_has_items": ["Bow (Progressive)", "Bow"]
    },
    "Goron Shop Bombchu Refill": {
        "scenes": [0x1014],
        "has_slot_data": ["shop_hints"],
        "any_has_items": ["Bombchus (Progressive)", "Bombchu Bag"]
    },


    # Beedle
    "Beedle Shop": {
        "locations": ["Beedle Shop Wisdom Gem", "Beedle Shop Red Potion",
                      "Beedle Shop Bottom Ship Part", "Beedle Shop Treasure",
                      "Beedle Shop Purple Potion"],
        "scenes": [0x500],
        "has_slot_data": ["shop_hints"],
    },
    "Beedle Shop Bomb Bag": {
        "scenes": [0x500],
        "locations": ["Beedle Shop Top Ship Part", "Beedle Shop Bomb Bag"],
        "has_slot_data": ["shop_hints"],
        "any_has_items": ["Bombs (Progressive)", "Bomb Bag"]
    },
    "Masked Beedle": {
        "locations": ["Masked Beedle Heart Container", "Masked Beedle Courage Gem",
                      "Masked Beedle Red Potion", "Masked Beedle Yellow Potion",
                      "Masked Beedle Top Ship Part", "Masked Beedle Bottom Ship Part",
                      "Masked Beedle Treasure"],
        "scenes": [0x500],
        "has_slot_data": ["shop_hints", "randomize_masked_beedle"],
    },

    # Eddo
    "Cannon Island": {
        "locations": ["Eddo's Cannon", "Eddo's Salvage Arm"],
        "has_slot_data": ["shop_hints"],
        "scenes": [0x130B],
    },

    # Spirit Island
    "Spirit Island 1": {
        "locations": LOCATION_GROUPS["Spirit Upgrades"],
        "scenes": [0x1701],
        "has_slot_data": [("spirit_island_hints", 0)]
    },
    "Spirit Island 2": {
        "locations": ["Spirit Shrine Power Upgrade Level 2",
                      "Spirit Shrine Wisdom Upgrade Level 2",
                      "Spirit Shrine Courage Upgrade Level 2"],
        "scenes": [0x1701],
        "has_slot_data": [("spirit_island_hints", 1)]
    },

    # Dungeon Hints
    "Oshus Dungeon Hints": {
        "scenes": [0xb0A],
        "has_slot_data": [("dungeon_hint_location", 1), ("goal_requirements", [1, 2])],
        "locations": ["Dungeon Hints"]
    },
    "TotOK Dungeon Hints": {
        "scenes": [0x2600],
        "has_slot_data": [("dungeon_hint_location", 2), ("goal_requirements", [1, 2])],
        "locations": ["Dungeon Hints"]
    },

    # Minigame Hints
    "Bannan Island East Cannon Game": {
        "scenes": [0x1400],
        "any_has_items": ["Bombs (Progressive)", "Bomb Bag"],
        "has_slot_data": [("randomize_minigames", 1)],
    },
    "Archery Minigame 1700": {
        "scenes": [0xC0B],
        "has_slot_data": [("randomize_minigames", 1)],
    },
    "Archery Minigame 2000": {
        "scenes": [0xC0B],
        "has_slot_data": [("randomize_minigames", 1), ("logic", [1, 2])],
    },
    "Dee Ess Win Goron Game": {
        "scenes": [0x1B00],
        "has_slot_data": [("randomize_minigames", 1)],
    },
    "Harrow Island": {
        "scenes": [0x1800],
        "has_slot_data": [("randomize_harrow", 1)],
        "locations": ["Harrow Island Dig 1", "Harrow Island Dig 2", "Harrow Island Dig 3", "Harrow Island Dig 4"]
    },
    "Maze Island": {
        "scenes": [0x1900],
        "has_slot_data": [("randomize_minigames", 1)],
        "locations": ["Maze Island Beginner", "Maze Island Normal", "Maze Island Expert", "Maze Island Bonus Reward"]
    },
    "Prince of Red Lions Combat Reward": {
        "scenes": [0x700],
        "has_slot_data": [("randomize_minigames", 1)],
    },
    "Fishing Hints": {
        "scenes": [0x1401],
        "has_slot_data": [("randomize_fishing", 1)],
        "locations": LOCATION_GROUPS["Fish"]
    },

}
