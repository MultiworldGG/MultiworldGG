

HINT_DATA = {
    # Minigames
    "Hyrule Castle 1F Sword Minigame 60 Points": {
        "scenes": [0x2807],
        "slot_data": [("minigame_hints", 1), ("randomize_minigames", [1, 2, 3, 4, 5])],
    },
    "Castle Town Take 'em All On Level 1": {
        "scenes": [0x290B],
        "slot_data": [("minigame_hints", 1), ("randomize_minigames", [1, 3, 4])],
    },
    "Castle Town Take 'em All On Level 2": {
        "scenes": [0x290B],
        "slot_data": [("minigame_hints", 1), ("randomize_minigames", [2, 3, 4])],
    },
    "Castle Town Take 'em All 3": {
        "scenes": [0x290B],
        "slot_data": [("minigame_hints", 1), ("randomize_minigames", [4, 5])],
        "locations": ["Castle Town Take 'em All On Level 3",
                      "Castle Town Take 'em All On Level 3 Capbone Chest"]
    },
    "Mayscore Whip Race 1:05-1:15": {
        "scenes": [0x3800],
        "slot_data": [("minigame_hints", 1), ("randomize_minigames", [2, 3, 4])],
    },
    "Mayscore Whip Race 1:15-1:30": {
        "scenes": [0x3800],
        "slot_data": [("minigame_hints", 1), ("randomize_minigames", [1, 3, 4])],
    },
    "Mayscore Whip Race Sub 1:05": {
        "scenes": [0x3800],
        "slot_data": [("minigame_hints", 1), ("randomize_minigames", [4, 5])],
    },
    # "Woodland Sanctuary Song of Restoration": {
    #     "scenes": [0x3001],
    #     "slot_data": [("minigame_hints", 1), ("randomize_minigames", [1, 2, 3, 4])],
    # },
    # "Snowfall Sanctuary Song of Restoration": {
    #     "scenes": [0x3102],
    #     "slot_data": [("minigame_hints", 1), ("randomize_minigames", [1, 2, 3, 4])],
    # },
    "Slippery Station Amateur Reward": {
        "scenes": [0x3f06],
        "slot_data": [("minigame_hints", 1), ("randomize_minigames", [1, 3, 4])],
    },
    "Slippery Station Pro Reward": {
        "scenes": [0x3f06],
        "slot_data": [("minigame_hints", 1), ("randomize_minigames", [2, 3, 4])],
    },
    "Slippery Station Champion Reward": {
        "scenes": [0x3f06],
        "slot_data": [("minigame_hints", 1), ("randomize_minigames", [4, 5])],
    },
    "Goron Target Range": {
        "scenes": [0x3c00, 0x3c01],
        "slot_data": [("minigame_hints", 1), ("randomize_minigames", [1, 2, 3, 4, 5])],
    },
    "Pirate Hideout Minigame 3000-4000": {
        "scenes": [0x3a00],
        "slot_data": [("minigame_hints", 1), ("randomize_minigames", [1, 3, 4])],
    },
    "Pirate Hideout Minigame 4000-5000": {
        "scenes": [0x3a00],
        "slot_data": [("minigame_hints", 1), ("randomize_minigames", [2, 3, 4])],
    },
    "Pirate Hideout Minigame 5000+": {
        "scenes": [0x3a00],
        "slot_data": [("minigame_hints", 1), ("randomize_minigames", [4, 5])],
    },
    "Ends of the Earth Master": {
        "scenes": [0x4101],
        "locations": ["Ends of the Earth Master Big Chest", "Ends of the Earth Master Small Chest"],
        "slot_data": [("minigame_hints", 1), ("randomize_minigames", [1, 3, 4])],
    },
    "Ends of the Earth Tempered": {
        "scenes": [0x4105],
        "locations": ["Ends of the Earth Tempered Big Chest", "Ends of the Earth Tempered Small Chest"],
        "slot_data": [("minigame_hints", 1), ("randomize_minigames", [2, 3, 4])],
    },
    "Ends of the Earth Golden": {
        "scenes": [0x4109],
        "locations": ["Ends of the Earth Golden Big Chest", "Ends of the Earth Golden Small Chest"],
        "slot_data": [("minigame_hints", 1), ("randomize_minigames", [4, 5])],
    },
    # Shops
    "Castle Town Shop Treasures": {
        "scenes": [0x290a],
        "slot_data": [("shopsanity", "treasure"), ("shop_hints", 1)],
        "locations": ["Castle Town Shop Treasure 1", "Castle Town Shop Treasure 2"]
    },
    "Castle Town Shop Red Potion": {
        "scenes": [0x290a],
        "slot_data": [("shopsanity", "potions"), ("shop_hints", 1)],
    },
    "Mayscore Shop Treasures": {
        "scenes": [0x2a05],
        "slot_data": [("shopsanity", "treasure"), ("shop_hints", 1)],
        "locations": ["Mayscore Shop Treasure 1", "Mayscore Shop Treasure 2"]
    },
    "Mayscore Shop Red Potion": {
        "scenes": [0x2a05],
        "slot_data": [("shopsanity", "potions"), ("shop_hints", 1)],
    },
    "Beedle Shop Rare Treasure": {
        "scenes": [0x4503],
        "slot_data": [("shopsanity", "treasure"), ("shop_hints", 1)]
    },
    "Beedle Shop Uncommon Treasure": {
        "scenes": [0x4503],
        "slot_data": [("shopsanity", "treasure"), ("shop_hints", 1)]
    },
    "Beedle Shop Bomb Bag": {
        "scenes": [0x4503],
        "slot_data": [("shopsanity", "uniques"), ("shop_hints", 1)]
    },
    "Beedle Shop Red Potion": {
        "scenes": [0x4503],
        "slot_data": [("shopsanity", "potions"), ("shop_hints", 1)]
    },
    "Beedle Shop Purple Potion": {
        "scenes": [0x4503],
        "slot_data": [("shopsanity", "potions"), ("shopsanity", "uniques", "not"), ("shop_hints", 1)]
    },
    "Snowfall Supermarket Heart Container": {
        "scenes": [0x3103],
        "slot_data": [("shopsanity", "uniques"), ("shop_hints", 1)]
    },
    "Snow Sanc Shop potions": {
        "scenes": [0x3103],
        "slot_data": [("shopsanity", "potions"), ("shop_hints", 1)],
        "locations": ["Snowfall Supermarket Red Potion", "Snowfall Supermarket Purple Potion"]
    },
    "Snowfall Supermarket Shield": {
        "scenes": [0x3103],
        "slot_data": [("shopsanity", "shields"), ("shop_hints", 1)]
    },
    "Castle Town Shop Shield": {
        "scenes": [0x290a],
        "slot_data": [("shopsanity", "shields"), ("shop_hints", 1)]
    },
    "Mayscore Shop Shield": {
        "scenes": [0x2a05],
        "slot_data": [("shopsanity", "shields"), ("shop_hints", 1)]
    },
    "Goron Shop Shield": {
        "scenes": [0x2e06],
        "slot_data": [("shopsanity", "shields"), ("shop_hints", 1)]
    },
    "Goron Shop Quiver": {
        "scenes": [0x2e06],
        "slot_data": [("shopsanity", "uniques"), ("shop_hints", 1)]
    },
    "Goron Shop Bomb Refill": {
        "scenes": [0x2e06],
        "slot_data": [("shopsanity", "ammo"), ("shop_hints", 1)]
    },
    "Trading Post Buy Shield": {
        "scenes": [0x370a],
        "slot_data": [("shopsanity", "shields"), ("shop_hints", 1)]
    },
    "Mayscore Shop Postcards": {
        "scenes": [0x2a05],
        "slot_data": [("shopsanity", "postcards"), ("shop_hints", 1)]
    },
    "Castle Town Shop Postcards": {
        "scenes": [0x290a],
        "slot_data": [("shopsanity", "postcards"), ("shop_hints", 1)]
    },
    "Snowfall Supermarket Postcards": {
        "scenes": [0x3103],
        "slot_data": [("shopsanity", "postcards"), ("shop_hints", 1)]
    },
    "Snowfall Supermarket Treasure": {
        "scenes": [0x3103],
        "slot_data": [("shopsanity", "treasure"), ("shopsanity", "uniques", "not"), ("shop_hints", 1)]
    },
    "Papuzia Shop Postcards": {
        "scenes": [0x2c02],
        "slot_data": [("shopsanity", "postcards"), ("shop_hints", 1)]
    },
    "Papuzia Shop Potions": {
        "scenes": [0x2c02],
        "slot_data": [("shopsanity", "potions"), ("shop_hints", 1)],
        "locations": ["Papuzia Shop Purple Potion", "Papuzia Shop Yellow Potion"]
    },
    "Goron Shop Potions": {
        "scenes": [0x2e06],
        "slot_data": [("shopsanity", "potions"), ("shop_hints", 1)],
        "locations": ["Goron Shop Purple Potion", "Goron Shop Yellow Potion"]
    },
    "Goron Shop Postcards": {
        "scenes": [0x2e06],
        "slot_data": [("shopsanity", "postcards"), ("shopsanity", "uniques", "not"), ("shop_hints", 1)]
    },
    "Papuzia Shop Ammo": {
        "scenes": [0x2c02],
        "slot_data": [("shopsanity", "ammo"), ("shop_hints", 1)],
        "locations": ["Papuzia Shop Bombs", "Papuzia Shop Arrows"]
    },
    "Beedle Shop Bomb Refill": {
        "scenes": [0x4503],
        "slot_data": [("shopsanity", "ammo"), ("shop_hints", 1)],
    }
}