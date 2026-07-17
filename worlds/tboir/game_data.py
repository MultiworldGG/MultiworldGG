data = {
	"rooms": {
		"Treasure Room": {},
		"Shop": {},
		"Secret Room": {},
		"Super Secret Room": {},
		"Boss Room": {},
		"Closet": {},
		"Arcade": {},
		"Challenge Room": {},
		"Curse Room": {},
		"Sacrifice Room": {},
		"Miniboss Room": {},
		"Deal Room": {},
		"Vault": {"type": "rng"},
		"Dice Room": {"type": "rng"},
		"Bedroom": {"type": "rng"},
		"Library": {"type": "rng"},
		"Knife Piece": {},
		"Crawl Space": {"type": "crawl_space", "requires": {"or": [{"has": "We Need To Go Deeper!"}, {"has": "Ehwaz"}]}},
		"I AM ERROR": {"type": "error_room", "requires": {"has": "Undefined"}},
		"Planetarium": {"type": "planetarium", "requires": {"has": "Telescope Lens"}},
		"Ultra Secret Room": {"type": "ultra_secret_room", "requires": {"or": [{"has": "Red Key"}, {"has": "Soul of Cain"}, {"has": "Cracked Key"}]}}
	},
	"items": [
		"Angel Deal Item",
		"Boss Item",
		"Curse Room Item",
		"Devil Deal Item",
		"Golden Chest Item",
		"Library Item",
		"Planetarium Item",
		"Red Chest Item",
		"Secret Room Item",
		"Shop Item",
		"Treasure Room Item",
		"1-UP",
		"Random Bomb",
		"Random Card",
		"Random Chest",
		"Random Heart",
		"Random Key",
		"Random Pill",
		"Random Trinket",
		"Random Coin",
		"Curse Trap",
		"Paralysis Trap",
		"Retro Vision Trap",
		"Teleport Trap",
		"Troll Bomb Trap",
		"Wavy Cap Trap",
		"Progressive Map Upgrade",
		"Progressive Inventory Upgrade",
		"Permanent Damage Up",
		"Permanent Tears Up",
		"Permanent Range Up",
		"Permanent Speed Up",
		"Permanent Luck Up"
	],
	"characters": [
		"Isaac",
        "Magdalene",
        "Cain",
        "Judas",
        "???",
        "Eve",
        "Samson",
        "Azazel",
        "Lazarus",
        "Eden",
        "The Lost",
        "Lilith",
        "Keeper",
        "Apollyon",
        "The Forgotten",
        "Bethany",
        "Jacob & Esau",
        "Tainted Isaac",
        "Tainted Magdalene",
        "Tainted Cain",
        "Tainted Judas",
        "Tainted ???",
        "Tainted Eve",
        "Tainted Samson",
        "Tainted Azazel",
        "Tainted Lazarus",
        "Tainted Eden",
        "Tainted Lost",
        "Tainted Lilith",
        "Tainted Keeper",
        "Tainted Apollyon",
        "Tainted Forgotten",
        "Tainted Bethany",
        "Tainted Jacob"
	],
	"unlocks": {
		"Cellar": {"type": ["variant"]},
		"Burning Basement": {"type": ["variant"]},
		"Catacombs": {"type": ["variant"]},
		"Flooded Caves": {"type": ["variant"]},
		"Necropolis": {"type": ["variant"]},
		"Dank Depths": {"type": ["variant"]},
		"Boss Rush": {"type": ["timed"]},
		"Womb": {},
		"Utero": {"type": ["variant"]},
		"Scarred Womb": {"type": ["variant"]},
		"???": {"type": ["timed"]},
		"Cathedral": {},
		"Sheol": {},
		"The Polaroid": {},
		"The Negative": {},
		"Downpour": {"type": ["alt"]},
		"Dross": {"type": ["alt","variant"]},
		"Mines": {"type": ["alt"]},
		"Ashpit": {"type": ["alt","variant"]},
		"Mausoleum": {"type": ["alt"]},
		"Gehenna": {"type": ["alt","variant"]},
		"Key Pieces": {"type": ["mega_satan"]},
		"Void Portal": {"type": ["void"]},
		"Strange Door": {"type": ["ascend"]},
		"Knife Pieces": {"type": ["alt"]},
		"We Need To Go Deeper!": {"type": ["shovel"]},
		"Ehwaz": {"type": ["ehwaz"]},
		"Undefined": {"type": ["undefined"]},
		"Telescope Lens": {"type": ["telescope_lens"]},
		"Red Key": {"type": ["red_key"]},
		"Soul of Cain": {"type": ["soul_of_cain"]},
		"Cracked Key": {"type": ["cracked_key"]}
	},
	"regions": {
		"Menu": {
			"connects_to": ["Basement", "Cellar", "Burning Basement"]
		},
		"Chapter 1": {
			"rooms": ["Vault", "Dice Room", "Bedroom", "Library", "Crawl Space", "I AM ERROR", "Planetarium", "Ultra Secret Room"],
			"connects_to" : ["Dark Room&sacrifice_room_logic"],
			"tracker_location": {
                "x": 90,
                "y": 265
            }
		},
		"Chapter 2": {
			"rooms": ["Vault", "Dice Room", "Bedroom", "Library", "Crawl Space", "I AM ERROR", "Planetarium", "Ultra Secret Room"],
			"connects_to" : ["Dark Room&sacrifice_room_logic"],
			"tracker_location": {
                "x": 380,
                "y": 265
            }
		},
		"Chapter 3": {
			"rooms": ["Vault", "Dice Room", "Bedroom", "Library", "Crawl Space", "I AM ERROR", "Planetarium", "Ultra Secret Room"],
			"connects_to" : ["Dark Room&sacrifice_room_logic"],
			"tracker_location": {
                "x": 670,
                "y": 265
            }
		},
		"Chapter 4": {
			"rooms": ["Vault", "Dice Room", "Library", "Crawl Space", "I AM ERROR", "Planetarium&planetarium_chapter_four", "Ultra Secret Room"],
			"connects_to" : ["Dark Room&sacrifice_room_logic"],
			"tracker_location": {
                "x": 960,
                "y": 85
            }
		},
		"Chapter 5": {
			"rooms": ["Vault", "Dice Room", "Library", "Crawl Space", "I AM ERROR", "Ultra Secret Room"],
			"tracker_location": {
                "x": 1330,
                "y": 165
            }
		},
		"Basement": {
			"rooms": ["Treasure Room", "Shop", "Secret Room", "Super Secret Room", "Boss Room", "Arcade", "Challenge Room", "Curse Room", "Sacrifice Room", "Miniboss Room", "Deal Room"],
			"connects_to": ["Caves", "Catacombs", "Flooded Caves", "Downpour", "Dross", "Chapter 1"],
			"tracker_location": {
                "x": 65,
                "y": 345
            }
		},
		"Cellar": {
			"rooms": ["Treasure Room", "Shop", "Secret Room", "Super Secret Room", "Boss Room", "Arcade", "Challenge Room", "Curse Room", "Sacrifice Room", "Miniboss Room", "Deal Room"],
			"connects_to": ["Caves", "Catacombs", "Flooded Caves", "Downpour", "Dross", "Chapter 1"],
			"requires": {"has": "Cellar"},
			"variant_of": "Basement",
			"tracker_location": {
                "x": 95,
                "y": 345
            }
		},
		"Burning Basement": {
			"rooms": ["Treasure Room", "Shop", "Secret Room", "Super Secret Room", "Boss Room", "Arcade", "Challenge Room", "Curse Room", "Sacrifice Room", "Miniboss Room", "Deal Room"],
			"connects_to": ["Caves", "Catacombs", "Flooded Caves", "Downpour", "Dross", "Chapter 1"],
			"requires": {"has": "Burning Basement"},
			"variant_of": "Basement",
			"tracker_location": {
                "x": 125,
                "y": 345
            }
		},
		"Caves": {
			"rooms": ["Treasure Room", "Shop", "Secret Room", "Super Secret Room", "Boss Room", "Arcade", "Challenge Room", "Curse Room", "Sacrifice Room", "Miniboss Room", "Deal Room"],
			"connects_to": ["Depths", "Necropolis", "Dank Depths", "Mines", "Ashpit", "Chapter 2"],
			"tracker_location": {
                "x": 355,
                "y": 345
            }
		},
		"Catacombs": {
			"rooms": ["Treasure Room", "Shop", "Secret Room", "Super Secret Room", "Boss Room", "Arcade", "Challenge Room", "Curse Room", "Sacrifice Room", "Miniboss Room", "Deal Room"],
			"connects_to": ["Depths", "Necropolis", "Dank Depths", "Mines", "Ashpit", "Chapter 2"],
			"requires": {"has": "Catacombs"},
			"variant_of": "Caves",
			"tracker_location": {
                "x": 385,
                "y": 345
            }
		},
		"Flooded Caves": {
			"rooms": ["Treasure Room", "Shop", "Secret Room", "Super Secret Room", "Boss Room", "Arcade", "Challenge Room", "Curse Room", "Sacrifice Room", "Miniboss Room", "Deal Room"],
			"connects_to": ["Depths", "Necropolis", "Dank Depths", "Mines", "Ashpit", "Chapter 2"],
			"requires": {"has": "Flooded Caves"},
			"variant_of": "Caves",
			"tracker_location": {
                "x": 415,
                "y": 345
            }
		},
		"Depths": {
			"rooms": ["Treasure Room", "Shop", "Secret Room", "Super Secret Room", "Boss Room", "Arcade", "Challenge Room", "Curse Room", "Sacrifice Room", "Miniboss Room", "Deal Room"],
			"connects_to": ["Womb", "Utero", "Scarred Womb", "Mausoleum", "Gehenna", "Boss Rush", "Home", "Chapter 3"],
			"boss": "Mom",
			"tracker_location": {
                "x": 645,
                "y": 345
            }
		},
		"Necropolis": {
			"rooms": ["Treasure Room", "Shop", "Secret Room", "Super Secret Room", "Boss Room", "Arcade", "Challenge Room", "Curse Room", "Sacrifice Room", "Miniboss Room", "Deal Room"],
			"connects_to": ["Womb", "Utero", "Scarred Womb", "Mausoleum", "Gehenna", "Boss Rush", "Home", "Chapter 3"],
			"boss": "Mom",
			"requires": {"has": "Necropolis"},
			"variant_of": "Depths",
			"tracker_location": {
                "x": 675,
                "y": 345
            }
		},
		"Dank Depths": {
			"rooms": ["Treasure Room", "Shop", "Secret Room", "Super Secret Room", "Boss Room", "Arcade", "Challenge Room", "Curse Room", "Sacrifice Room", "Miniboss Room", "Deal Room"],
			"connects_to": ["Womb", "Utero", "Scarred Womb", "Mausoleum", "Gehenna", "Boss Rush", "Home", "Chapter 3"],
			"boss": "Mom",
			"requires": {"has": "Dank Depths"},
			"variant_of": "Depths",
			"tracker_location": {
                "x": 705,
                "y": 345
            }
		},
		"Boss Rush": {
			"type": "timed",
			"rooms": ["Boss Room"],
			"boss": "Boss Rush",
			"requires": {"has": "Boss Rush"},
			"tracker_location": {
                "x": 835,
                "y": 255
            }
		},
		"Womb": {
			"rooms": ["Secret Room", "Super Secret Room", "Boss Room", "Arcade", "Challenge Room", "Curse Room", "Sacrifice Room", "Miniboss Room", "Deal Room"],
			"connects_to": ["Cathedral", "Sheol", "???", "Chapter 4"],
			"boss": "Mom's Heart",
			"requires": {
				"or": [
					{"has": "Womb"},
					{"hasIfOption": {"has" : "We Need To Go Deeper!", "options": [("trapdoor_logic", True), ("crawl_space", 3)]}},
					{"hasIfOption": {"has" : "Ehwaz", "options": [("trapdoor_logic", True), ("crawl_space", 4)]}},
					{"hasIfOption": {"has" : "Undefined", "options": [("error_room_logic", True), ("error_room", 3)]}},
					{"hasIfOption": {"has" : "Red Key", "options": [("error_room_logic", True), ("ultra_secret_room", 3)]}}
					]},
			"tracker_location": {
                "x": 935,
                "y": 345
            }
		},
		"Utero": {
			"rooms": ["Secret Room", "Super Secret Room", "Boss Room", "Arcade", "Challenge Room", "Curse Room", "Sacrifice Room", "Miniboss Room", "Deal Room"],
			"connects_to": ["Cathedral", "Sheol", "???", "Chapter 4"],
			"boss": "Mom's Heart",
			"requires": {"has": "Utero"},
			"variant_of": "Womb",
			"tracker_location": {
                "x": 965,
                "y": 345
            }
		},
		"Scarred Womb": {
			"rooms": ["Secret Room", "Super Secret Room", "Boss Room", "Arcade", "Challenge Room", "Curse Room", "Sacrifice Room", "Miniboss Room", "Deal Room"],
			"connects_to": ["Cathedral", "Sheol", "???", "Chapter 4"],
			"boss": "Mom's Heart",
			"requires": {"has": "Scarred Womb"},
			"variant_of": "Womb",
			"tracker_location": {
                "x": 995,
                "y": 345
            }
		},
		"???": {
			"type": "timed",
			"rooms": ["Treasure Room", "Shop", "Boss Room"],
			"connects_to": ["Cathedral", "Sheol", "The Void"],
			"boss": "Hush",
			"requires": {"has": "???"},
			"tracker_location": {
                "x": 935,
                "y": 165
            }
		},
		"Cathedral": {
			"rooms": ["Secret Room", "Super Secret Room", "Boss Room", "Challenge Room", "Curse Room", "Sacrifice Room", "Miniboss Room"],
			"connects_to": ["Chest", "Chapter 5"],
			"boss": "Isaac",
			"requires": {
				"or": [
					{"has": "Cathedral"},
					{"hasIfOption": {"has" : "Undefined", "options": [("error_room_logic", True), ("error_room", 3)]}},
					{"hasIfOption": {"has" : "Red Key", "options": [("error_room_logic", True), ("ultra_secret_room", 3)]}}
					]},
			"tracker_location": {
                "x": 1305,
                "y": 245
            }
		},
		"Sheol": {
			"rooms": ["Secret Room", "Super Secret Room", "Boss Room", "Challenge Room", "Curse Room", "Sacrifice Room", "Miniboss Room"],
			"connects_to": ["Dark Room", "Chapter 5"],
			"boss": "Satan",
			"requires": {
				"or": [
					{"has": "Sheol"},
					{"hasIfOption": {"has" : "We Need To Go Deeper!", "options": [("trapdoor_logic", True), ("crawl_space", 3)]}},
					{"hasIfOption": {"has" : "Ehwaz", "options": [("trapdoor_logic", True), ("crawl_space", 4)]}},
					{"hasIfOption": {"has" : "Undefined", "options": [("error_room_logic", True), ("error_room", 3)]}},
					{"hasIfOption": {"has" : "Red Key", "options": [("error_room_logic", True), ("ultra_secret_room", 3)]}}
					]},
			"tracker_location": {
                "x": 1305,
                "y": 445
            }
		},
		"Chest": {
			"rooms": ["Secret Room", "Super Secret Room", "Boss Room"],
			"connects_to": ["Mega Satan", "The Void"],
			"boss": "Blue Baby",
			"requires": {
				"or": [
					{"has": "The Polaroid"},
					{"hasIfOption": {"has" : "Undefined", "options": [("error_room_logic", True), ("error_room", 3)]}},
					{"hasIfOption": {"has" : "Red Key", "options": [("error_room_logic", True), ("ultra_secret_room", 3)]}}
					]},
			"tracker_location": {
                "x": 1595,
                "y": 245
            }
		},
		"Dark Room": {
			"rooms": ["Secret Room", "Super Secret Room", "Boss Room"],
			"connects_to": ["Mega Satan", "The Void"],
			"boss": "The Lamb",
			"requires": {
				"or": [
					{"has": "The Negative"},
					{"hasIfOption": {"has" : "Undefined", "options": [("error_room_logic", True), ("error_room", 3)]}},
					{"hasIfOption": {"has" : "Red Key", "options": [("error_room_logic", True), ("ultra_secret_room", 3)]}},
                    {"option": ("sacrifice_room_logic", True)}
					]},
			"tracker_location": {
                "x": 1595,
                "y": 445
            }
		},
		"Mega Satan": {
			"type": "mega_satan",
			"rooms": ["Boss Room"],
			"connects_to": ["The Void"],
			"boss": "Mega Satan",
			"requires": {
                "or": [
                	{"has": "Key Pieces"},
					{"hasIfOption": {"has" : "Soul of Cain", "options": [("soul_of_cain_logic", True), ("ultra_secret_room", 4)]}},
				]},
			"tracker_location": {
                "x": 1760,
                "y": 350
            }
		},
		"The Void": {
			"type": "void",
			"rooms": ["Secret Room", "Super Secret Room", "Boss Room"],
			"connects_to": [],
			"boss": "Delirium",
			"requires": {"has": "Void Portal"},
			"tracker_location": {
                "x": 1445,
                "y": 885
            }
		},
		"Downpour": {
			"type": "alt",
			"rooms": ["Treasure Room", "Shop", "Secret Room", "Super Secret Room", "Boss Room", "Arcade", "Challenge Room", "Curse Room", "Sacrifice Room", "Miniboss Room", "Deal Room"],
			"connects_to": ["Caves", "Catacombs", "Flooded Caves", "Mines", "Ashpit", "Mirrorworld", "Chapter 1"],
			"requires": {"has": "Downpour"},
			"tracker_location": {
                "x": 145,
                "y": 545
            }
		},
		"Dross": {
			"type": "alt",
			"rooms": ["Treasure Room", "Shop", "Secret Room", "Super Secret Room", "Boss Room", "Arcade", "Challenge Room", "Curse Room", "Sacrifice Room", "Miniboss Room", "Deal Room"],
			"connects_to": ["Caves", "Catacombs", "Flooded Caves", "Mines", "Ashpit", "Mirrorworld", "Chapter 1"],
			"requires": {"has": "Dross"},
			"variant_of": "Downpour",
			"tracker_location": {
                "x": 175,
                "y": 545
            }
		},
		"Mirrorworld": {
			"type": "alt",
			"rooms": ["Treasure Room", "Boss Room"],
			"tracker_location": {
                "x": 315,
                "y": 545
            }
		},
		"Mines": {
			"type": "alt",
			"rooms": ["Treasure Room", "Shop", "Secret Room", "Super Secret Room", "Boss Room", "Arcade", "Challenge Room", "Curse Room", "Sacrifice Room", "Miniboss Room", "Deal Room"],
			"connects_to": ["Depths", "Necropolis", "Dank Depths", "Mausoleum", "Gehenna", "The Escape", "Chapter 2"],
			"requires": {"has": "Mines"},
			"tracker_location": {
                "x": 435,
                "y": 545
            }
		},
		"Ashpit": {
			"type": "alt",
			"rooms": ["Treasure Room", "Shop", "Secret Room", "Super Secret Room", "Boss Room", "Arcade", "Challenge Room", "Curse Room", "Sacrifice Room", "Miniboss Room", "Deal Room"],
			"connects_to": ["Depths", "Necropolis", "Dank Depths", "Mausoleum", "Gehenna", "The Escape", "Chapter 2"],
			"requires": {"has": "Ashpit"},
			"variant_of": "Mines",
			"tracker_location": {
                "x": 465,
                "y": 545
            }
		},
		"The Escape": {
			"type": "alt",
			"rooms": ["Knife Piece"],
			"requires": {
				"and": [
					{"has": "Knife Pieces"},
					{"reach": "Mirrorworld"}
				]
			},
			"tracker_location": {
                "x": 605,
                "y": 545
            }
		},
		"Mausoleum": {
			"type": "alt",
			"rooms": ["Treasure Room", "Shop", "Secret Room", "Super Secret Room", "Boss Room", "Arcade", "Challenge Room", "Curse Room", "Sacrifice Room", "Miniboss Room", "Deal Room"],
			"connects_to": ["Womb", "Utero", "Scarred Womb", "Corpse", "Boss Rush", "Home", "Chapter 3"],
			"requires": {"has": "Mausoleum"},
			"tracker_location": {
                "x": 725,
                "y": 545
            }
		},
		"Gehenna": {
			"type": "alt",
			"rooms": ["Treasure Room", "Shop", "Secret Room", "Super Secret Room", "Boss Room", "Arcade", "Challenge Room", "Curse Room", "Sacrifice Room", "Miniboss Room", "Deal Room"],
			"connects_to": ["Womb", "Utero", "Scarred Womb", "Corpse", "Boss Rush", "Home", "Chapter 3"],
			"requires": {"has": "Gehenna"},
			"variant_of": "Mausoleum",
			"tracker_location": {
                "x": 755,
                "y": 545
            }
		},
		"Corpse": {
			"type": "alt",
			"rooms": ["Secret Room", "Super Secret Room", "Boss Room", "Arcade", "Challenge Room", "Curse Room", "Sacrifice Room", "Miniboss Room", "Deal Room"],
			"connects_to": ["Chapter 4"],
			"boss": "Mother",
			"requires": {
                "or": [
                	{"reach": "The Escape"},
					{"hasIfOption": {"has" : "Soul of Cain", "options": [("soul_of_cain_logic", True), ("ultra_secret_room", 4)]}},
				]},
			"tracker_location": {
                "x": 1015,
                "y": 545
            }
		},
		"Home": {
			"type": "ascend",
			"rooms": ["Closet", "Boss Room"],
			"connects_to": [],
			"boss": "Beast",
			"requires": {
				"and": [
					{"has": "Strange Door"},
					{"or": [
						{"has": "The Polaroid"},
						{"has": "The Negative"},
						{"hasIfOption": {"has" : "Soul of Cain", "options": [("soul_of_cain_logic", True), ("ultra_secret_room", 4)]}},
					]}
				]
			},
			"tracker_location": {
                "x": 535,
                "y": 915
            }
		}		
	},
    "boss_rewards": {
        "Mom": { 
			"amount": 1, 
			"tracker_location": {
                "x": 815,
                "y": 345
			}
		},
        "Mom's Heart": { 
			"amount": 2, 
			"tracker_location": {
                "x": 1105,
                "y": 345
			}
		},
        "Boss Rush": { 
			"amount": 2, 
			"tracker_location": {
                "x": 835,
                "y": 255
			}
		},
        "Isaac": { 
			"amount": 3, 
			"tracker_location": {
                "x": 1475,
                "y": 245
			}
		},
        "Satan": { 
			"amount": 3, 
			"tracker_location": {
                "x": 1475,
                "y": 445
			}
		},
        "Hush": { 
			"amount": 3, 
			"tracker_location": {
                "x": 1125,
                "y": 95
			}
		},
        "Blue Baby": { 
			"amount": 4, 
			"tracker_location": {
                "x": 1765,
                "y": 245
			}
		},
        "The Lamb": { 
			"amount": 4, 
			"tracker_location": {
                "x": 1765,
                "y": 445
			}
		},
        "Mega Satan": { 
			"amount": 5, 
			"tracker_location": {
                "x": 1760,
                "y": 350
			}
		},
        "Mother": { 
			"amount": 5, 
			"tracker_location": {
                "x": 1100,
                "y": 695
			}
		},
        "Beast": { 
			"amount": 5, 
			"tracker_location": {
                "x": 620,
                "y": 745
			}
		},
        "Delirium": { 
			"amount": 5, 
			"tracker_location": {
                "x": 1660,
                "y": 765
			}
		}
   }
}