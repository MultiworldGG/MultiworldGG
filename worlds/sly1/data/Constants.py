LEVELS = {
    "Tide of Terror": [
        "Stealthy Approach",
        "Prowling the Grounds",
        "High Class Heist",
        "Into the Machine",
        "Cunning Disguise",
        "Fire Down Below",
        "Treasure in the Depths",
        "Gunboat Graveyard"
    ],
    "Sunset Snake Eyes": [
        "Rocky Start",
        "Muggshot's Turf",
        "Boneyard Casino",
        "Murray's Big Gamble",
        "At the Dog Track",
        "Two to Tango",
        "Straight to the Top",
        "Back Alley Heist"
    ],
    "Vicious Voodoo": [
        "Dread Swamp Path",
        "The Swamp's Dark Center",
        "Lair of the Beast",
        "Grave Undertaking",
        "Piranha Lake",
        "Descent into Danger",
        "Ghastly Voyage",
        "Down Home Cooking"
    ],
    "Fire in the Sky": [
        "Perilous Ascent",
        "Inside the Stronghold",
        "Flaming Temple of Flame",
        "Unseen Foe",
        "King of the Hill",
        "Rapid Fire Assault",
        "Duel by the Dragon",
        "Desperate Race"
    ]
}

BOSSES = [
    ("Eye of the Storm", 5),
    ("Last Call", 7),
    ("Deadly Dance", 9),
    ("Flame Fu!", 11),
    ("Beat Clockwerk", 13)
]

MOVE_NAMES = [
    "Progressive Dive Attack",
    "Progressive Roll",
    "Progressive Slow Motion",
    "Coin Magnet",
    "Mine",
    "Fast",
    "Progressive Safety",
    "Decoy",
    "Hacking",
    "Progressive Invisibility",
    "Tide of Terror Blueprints",
    "Sunset Snake Eyes Blueprints",
    "Vicious Voodoo Blueprints",
    "Fire in the Sky Blueprints"
]

MOVES = {
    "Progressive Dive Attack": [2, 16],
    "Progressive Roll": [4, 1024],
    "Progressive Slow Motion": [8, 4096, 32768],
    "Coin Magnet": 32,
    "Mine": 64,
    "Fast": 128,
    "Progressive Safety": [256, 16384],
    "Decoy": 512,
    "Hacking": 2048,
    "Progressive Invisibility": [65536, 8192],
    "Tide of Terror Blueprints": 536870912,
    "Sunset Snake Eyes Blueprints": 1073741824,
    "Vicious Voodoo Blueprints": 2147483648,
    "Fire in the Sky Blueprints": [0x10000000]
}

ADDRESSES = {
    "SCUS-97198": {
        "world id": 0x27DBF8,
        "level id": 0x27DBFC,
        "paris files": 0x27C66C,
        "cutscene pointer": 0x27051C,
        "sly control": 0x262C68,
        "binocucom": 0x270458,
        "FMV": 0x269A18,
        "FMV skip": 0x269A60,
        "game completion": 0x27DC18,
        "thief moves": 0x27DC10,
        "fits progress": 0x27D7A8,
        "lives": 0x27DC00,
        "charms": 0x27DC04,
        "sly struct pointer": 0x262E10,
        "sly action offset": 0x2220,
        "slope control": 0x274AD0,
        "time control": 0x261850,
        "active thief move": 0x274F74,
        "button pressed": 0x262D18, #Which button the player is pressing
        "button held": 0x262D22, #Whether a button is being held
        "game paused": 0x261858,
        "sly opacity offset": 0x2724,
        "charm offset": 0x584,
        "glow offset": 0x34,
        "cane offset": 0x1570,
        "sly shadow": 0x261F6C,
        "levels":
        [
            [  # Tide Of Terror
                0x27C67C,  # Stealthy Approach
                0x27C6F4,  # Prowling the Grounds
                0x27C76C,  # High Class Heist
                0x27C7E4,  # Into the Machine
                0x27C85C,  # Cunning Disguise
                0x27C8D4,  # Fire Down Below
                0x27C94C,  # Treasure in the Depths
                0x27C9C4   # Gunboat Graveyard
            ],
            [  # Sunset Snake Eyes
                0x27CAC8,  # Rocky Start
                0x27CB40,  # Muggshot's Turf
                0x27CBB8,  # Boneyard Casino
                0x27CC30,  # Murray's Big Gamble
                0x27CCA8,  # At the Dog Track
                0x27CD20,  # Two to Tango
                0x27CD98,  # Straight to the Top
                0x27CE10   # Back Alley Heist
            ],
            [  # Vicious Voodoo
                0x27CF14,  # Dread Swamp Path
                0x27CF8C,  # The Swamp's Dark Center
                0x27D004,  # Lair of the Beast
                0x27D07C,  # Grave Undertaking
                0x27D0F4,  # Piranha Lake
                0x27D16C,  # Descent into Danger
                0x27D1E4,  # Ghastly Voyage
                0x27D25C   # Down Home Cooking
            ],
            [  # Fire In The Sky
                0x27D360,  # Perilous Ascent
                0x27D3D8,  # Inside the Stronghold
                0x27D450,  # Flaming Temple of Flame
                0x27D4C8,  # Unseen Foe
                0x27D540,  # King of the Hill
                0x27D5B8,  # Rapid Fire Assault
                0x27D630,  # Duel by the Dragon
                0x27D6A8   # Desperate Race
            ]
        ],
        "bottle addresses":
        [
            [  # Tide Of Terror
                0x27C6E0,  # Stealthy Approach
                0,         # Prowling the Grounds (no bottles)
                0x27C7D0,  # High Class Heist
                0x27C848,  # Into the Machine
                0x27C8C0,  # Cunning Disguise
                0x27C938,  # Fire Down Below
                0,         # Treasure in the Depths (no bottles)
                0x27CA28   # Gunboat Graveyard
            ],
            [  # Sunset Snake Eyes
                0x27CB2C,  # Rocky Start
                0,         # Muggshot's Turf (no bottles)
                0x27CC1C,  # Boneyard Casino
                0,         # Murray's Big Gamble (no bottles)
                0,         # At the Dog Track (no bottles)
                0x27CD84,  # Two to Tango
                0x27CDFC,  # Straight to the Top
                0x27CE74   # Back Alley Heist
            ],
            [  # Vicious Voodoo
                0x27CF78,  # Dread Swamp Path
                0,         # The Swamp's Dark Center (no bottles)
                0x27D068,  # Lair of the Beast
                0x27D0E0,  # Grave Undertaking
                0,         # Piranha Lake (no bottles)
                0x27D1D0,  # Descent into Danger
                0,         # Ghastly Voyage (no bottles)
                0          # Down Home Cooking (no bottles)
            ],
            [  # Fire In The Sky
                0x27D3C4,  # Perilous Ascent
                0,         # Inside the Stronghold (no bottles)
                0x27D4B4,  # Flaming Temple of Flame
                0x27D52C,  # Unseen Foe
                0,         # King of the Hill (no bottles)
                0,         # Rapid Fire Assault (no bottles)
                0x27D694,  # Duel by the Dragon
                0          # Desperate Race (no bottles)
            ]
        ],
        "maps":
        [
            0x27CAC4,
            0x27CF10,
            0x27D35C,
            0x27D7A8
        ],
        "keys":
        [
            0x27CAB4,
            0x27CF00,
            0x27D34C,
            0x27D798
        ],
        "hubs":
        [
            0x27C67C,
            0x27CAC8,
            0x27CF14,
            0x27D360
        ],
        "name pointers":
        [
            [
                0x247B98, # Stealthy Approach
                0,        # Prowling the Grounds
                0x247BF0, # High Class Heist
                0x247C1C, # Into the Machine
                0x247C48, # Cunning Disguise
                0x247C74, # Fire Down Below
                0,        # Treasure in the Depths
                0x247CCC  # Gunboat Graveyard
            ],
            [
                0x247D24, # Rocky Start
                0,        # Muggshot's Turf
                0x247D7C, # Boneyard Casino
                0,        # Murray's Big Gamble
                0,        # At the Dog Track
                0x247E00, # Two to Tango
                0x247E2C, # Straight to the Top
                0x247E58  # Back Alley Heist
            ],
            [
                0x247EB0, # Dread Swamp Path
                0,        # The Swamp's Dark Center
                0x247F08, # Lair of the Beast
                0x247F34, # Grave Undertaking
                0,        # Piranha Lake
                0x247F8C, # Descent into Danger
                0,        # Ghastly Voyage
                0         # Down Home Cooking
            ],
            [
                0x24803C,  # Perilous Ascent
                0,         # Inside the Stronghold
                0x248094,  # Flaming Temple of Flame
                0x2480C0,  # Unseen Foe
                0,         # King of the Hill
                0,         # Rapid Fire Assault
                0x248144,  # Duel by the Dragon
                0          # Desperate Race
            ]
        ],
        "hub name pointers":
        [
            0x274434,
            0x274438,
            0x27443C,
            0x274440
        ],
        "anticheat":
        [
            0x261080,
            0x262310,
            0x269B48,
            0x275C34,
            0x27C828,
            0x27C829,
            0x27C82C,
            0x27C82D
        ]
    }
}